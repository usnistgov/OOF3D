# -*- python -*-
# $RCSfile: worker.py,v $
# $Revision: 1.94.2.5 $
# $Author: langer $
# $Date: 2014/10/03 17:41:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


## A worker is a wrapped generalized callback (from a menuitem) that
## will run in a separate thread. This callback is monitored through
## progress bars and gtk progress bars.

from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import threadstate
from ooflib.common import debug
from ooflib.common import excepthook
from ooflib.common import mainthread
from ooflib.common import parallel_enable
from ooflib.common import subthread
from ooflib.common import threadmanager
from ooflib.common.IO import reporter

if parallel_enable.enabled():
    from ooflib.common.IO.socket2me import pipeToSocket

import sys
import threading
import time

# Worker classes.  The basic highest-level interface is that workers
# must have a "start" routine, which is called from the menu item
# after the worker is created.

# Threading is handled with an extra layer of indirection -- the
# "ThreadedWorker" and subclasses are actually wrappers, which contain
# a "ThreadedWorkerCore" object.  These wrapper objects call their
# core object's "start" routine, and then manage the main thread,
# which may want to do complicated things before (or instead of)
# returning control to the caller.  The TextThreadedWorker draws the
# progress bar for the command.  The GUIThreadedWorkerBlock object,
# used in GUI mode, blocks until the just-launched thread terminates.
# This is useful when running scripts, for instance, when each script
# menu item (threadable or otherwise) runs on a subthread, but must
# not run concurrently with previous script commands.  This technique
# allows the GUI to be responsive and a script-reading progress bar to
# be presented during the read.

# Parallelization is fairly straightforward at this level -- menu
# items which are parallelized require a worker which is a subclass of
# ParallelWork, which itself only ensures that all the back-end
# machines receive the same menu item.

# Flag to indicate how to handle exceptions.  If False, workers should
# catch exceptions and send them to the reporter.  If True, workers
# should allow exceptions to propagate to the caller.  In the case of
# threaded workers, the core should propagate the exception data to
# the calling worker, which should re-raise it. propagate_exceptions
# is normally False. It's True in batch mode or when running without
# an interpreter (regression test mode).
propagate_exceptions = False

# Worker is the the base class for the workers that are invoked by the
# menu items.  Subclasses either actually call the menu item's
# callback, or invoke a WorkerCore that calls the callback.  In the
# first case, the Worker and the WorkerCore may be the same object.

# Keep track of existing workers for debugging and testing.
import weakref
allWorkers = weakref.WeakKeyDictionary()
allWorkerCores = weakref.WeakKeyDictionary()

class Worker(object):
    def __init__(self):
        allWorkers[self] = 1
        # toplevel is true if this worker wasn't started either
        # directly or indirectly by another worker.
        self.toplevel = self.isTopLevel()
    # Subclasses must redefine start().
    def start(self):
        raise ooferror.ErrPyProgrammingError("Worker.start must be redefined.")
    def stop(self):
        pass

# WorkerCore is a base class for the part of the Worker that actually
# runs menu commands.  WorkerCore always runs on the same thread as
# the menu command.

class WorkerCore(object):
    def __init__(self, menuitem, args, kwargs):
        self.menuitem = menuitem
        self.args = args
        self.kwargs = kwargs
        self._finished = False
        allWorkerCores[self] = 1
    def __getattr__(self, attrname):    # Stunt double for the menuitem
        return getattr(self.menuitem, attrname)    
    def initialize(self):       # called on subthread
#         debug.fmsg("assigning excepthook, menuitem=", self.menuitem.path())
        self.excepthook = excepthook.assign_excepthook(
            excepthook.OOFexceptHook())
    def finalize(self):
        self._finished = True
    def finished(self):
        return self._finished

###########################

_allNonThreadedWorkers = {}

class NonThreadedWorker(Worker, WorkerCore):
    def __init__(self, menuitem, args, kwargs):
        _allNonThreadedWorkers[self] = None
        WorkerCore.__init__(self, menuitem, args, kwargs)
        Worker.__init__(self)

    def isTopLevel(self):
        return len(_allNonThreadedWorkers) == 1

    # "Unthreadable" really means "Run on the same thread as the GUI,
    # and block until finished".  This code actually puts the callback
    # on the GUI thread no matter what.
    def start(self):
        if self.menuitem.callback is not None:
            try:
                self.initialize()
                try:
                    mainthread.runBlock(self.menuitem.precall)
                    mainthread.runBlock(self.menuitem.callback,
                                        (self,)+self.args,
                                        self.kwargs)
                    # remove_excepthook is called here only if no
                    # exception occured.  If an exception occured,
                    # remove_excepthook can't be called until after
                    # the exception is handled.
                    excepthook.remove_excepthook(self.excepthook)
                except SystemExit:
                    raise
                # TODO 3.1: After conversion to SWIG 2.x, OOF
                # exceptions will probably be subclasses of Exception.
                except (Exception, ooferror.ErrErrorPtr), exception:
                    mainthread.runBlock(self.menuitem.postcall, (False,))
                    if propagate_exceptions or not self.toplevel:
                        excepthook.remove_excepthook(self.excepthook)
                        raise
                    else:
                        reporter.error(exception)
                        sys.excepthook(*sys.exc_info())
                else:           # no exception
                    mainthread.runBlock(self.menuitem.postcall, (True,))
            finally:
                self.finalize()
    def finalize(self):
        del _allNonThreadedWorkers[self]
        WorkerCore.finalize(self)
                
################

class ThreadedWorkerCore(threading.Thread, WorkerCore):
    def __init__(self, menuitem, args, kwargs):
        WorkerCore.__init__(self, menuitem, args, kwargs)
        self.exception_data = None
        self.threadstate = None
        threading.Thread.__init__(self)

    def cleanUp(self):
        # Called after ThreadedWorkerCore finishes.
        self.exception_data = None

    # ThreadedWorkerCore.run() is called on a subthread by
    # threading.Thread.start().
    def run(self):
        if self.menuitem.callback is not None:
            self.threadstate = threadstate.ThreadState()
            threadmanager.threadManager.newWorker(self)
            try:
                self.initialize()
                try:
                    self.menuitem.precall()
                    self.menuitem.callback(self, *self.args, **self.kwargs)
                    # remove_excepthook is called here only if no
                    # exception occured.  If an exception occured,
                    # remove_excepthook can't be called until after
                    # the exception is handled.
                    excepthook.remove_excepthook(self.excepthook)
                except SystemExit:
                    raise
                # TODO 3.1: After conversion to SWIG 2.x, OOF
                # exceptions will probably be subclasses of Exception.
                except (Exception, ooferror.ErrErrorPtr), exception:
                    self.menuitem.postcall(False)
                    if propagate_exceptions or not self.toplevel:
                        self.exception_data = sys.exc_info()
                        sys.exc_clear()
                    else:
                        reporter.error(exception)
                        sys.excepthook(*sys.exc_info())
                else:           # no exception
                    self.menuitem.postcall(True)
            finally:
                self.finalize()
                threadmanager.threadManager.removeWorker(self)

    def stop(self):
        # Set the 'stopped' flag in each of the thread's Progress
        # objects.  This relies on the menuitem callback code's
        # inspecting the flag and quitting voluntarily.
        if self.threadstate:
            self.threadstate.impedeProgress()


class ThreadedWorker(Worker):
    def __init__(self, menuitem, args, kwargs):
        self.worker = ThreadedWorkerCore(menuitem, args, kwargs)
        self.menuitem = menuitem        # for debugging
        # self.lock prevents changes to the worker at inauspicious
        # times.
        self.lock = lock.SLock()
        Worker.__init__(self)
        self.worker.toplevel = self.toplevel

    def isTopLevel(self):
        return mainthread.mainthread()
    def start(self):
        self.worker.start()
        self.meanwhile()                # back in the main thread...
    def stop(self):
        self.worker.stop()

    def meanwhile(self):  # Default, should be overridden if nontrivial
        pass              # behavior is needed.
    
    def join(self):                     # waits for thread to finish
        self.worker.join()
        # This seems like a silly way to use a lock, but if it's
        # removing the last reference to worker.threadstate, it may be
        # imporant to lock the worker until the threadstate is
        # actually deleted.  TODO SOMETIME: Check that.
        self.lock.acquire()
        self.worker.threadstate = None
        self.lock.release()
        # Save the exception data, if any, before finalizing the
        # worker.
        exception_data = self.worker.exception_data
        self.worker.cleanUp()
        self.worker = None
        reporter.removeProgressBar()
        # Check if the core has caught an exception and placed it in
        # exception_data.  Re-raise it so it gets passed through to
        # the caller of the menu item.
        if ((propagate_exceptions or not self.toplevel)
            and exception_data is not None):
            raise exception_data[0], exception_data[1], exception_data[2]

    def finished(self):
        return self.worker.finished()
    def threadstate(self):
        return self.worker.threadstate


class TextThreadedWorker(ThreadedWorker):
    def _drawProgressBars(self, prgrsbars):
        progtexts = []          # list of messages to display for prog. bars.
        self.lock.acquire()
        try:
            ts = self.worker.threadstate
            if ts is None:
                return
            ts.acquireProgressLock();
            try:
                pnames = ts.getProgressNames()
            except:
                # Worker must be finished.
                return
            for pname in pnames:
                try:
                    # Look for an old ProgressBar
                    pbar = prgrsbars[pname]
                except KeyError:
                    # There's no ProgressBar for a Progress object
                    # with that name.  Get the Progress object,
                    # and make a new ProgressBar for it.
                    try:
                        prog = ts.findProgress(pname)
                        pbar = prog.makeTextBar()
                        prgrsbars[pname] = pbar
                    except ooferror.ErrNoProgress, exc:
                        print exc
                        # Oops, the Progress object vanished already.
                        pass
                    except (ooferror.ErrError, Exception):
                        print "Error when constructing progress bar!"
                        raise
                else:
                    # Re-use an old ProgressBar.
                    prog = pbar.progress
                if prog.started() and not prog.stopped():
                    progtexts.append(pbar.bar())
        finally:
            if ts is not None:
                ts.releaseProgressLock()
            self.lock.release()
            # end loop over pnames
            if progtexts:
                reporter.showProgressBar(progtexts)
            
    def meanwhile(self):
        ## This function should only be called if in text mode and on
        ## the main thread.  It checks to see if the thread is
        ## finished and redraws the progress bars.  It sleeps a bit
        ## after each check so that it doesn't eat up cpu.  The sleep
        ## time is initially short, but grows (up to a point) on each
        ## iteration.
        naptime = 0.001                 # initial length of sleep time
        maxnap = 0.3                    # maximum length of sleep time
        napfactor = 2.0                 # amount to increase on each iteration
        prgrsbars = {}                  # progressbar representations
        try:
            while not self.worker.finished():
                subthread.execute(self._drawProgressBars, args=(prgrsbars,))
                
                time.sleep(naptime)
                naptime *= napfactor
                if naptime > maxnap:
                    naptime = maxnap
            # end while not worker.finished
        except KeyboardInterrupt:
            self.worker.threadstate.impedeProgress()

        # Wait for thread to finish before OOF-ing some more.  Text
        # mode doesn't support concurrent operations.
        self.join()

###############################


mpiLock = lock.Lock()

## this lock is necessary because MPI does not
## support more than one subthread at a
## time, without running the risk of dead-locking. In order
## to avoid this potential deadlocking
## problem, every parallel worker
## acquires a lock and releases it upon
## completion of the assigned task.
## the MPI lock will not be necessary
## anymore when a fully threadable
## implementation of MPI becomes
## available (MPI-2?).

##################################


# ParallelWorker classes are not instanced unless you're in parallel
# mode, so they are free to use socket2me in this file.

class ParallelThreadedWorkerCore(ThreadedWorkerCore):
    def __init__(self, menuitem, args, kwargs):
        ThreadedWorkerCore.__init__(self, menuitem, args, kwargs)
    def initialize(self):
        global mpiLock
        mpiLock.acquire()
    def finalize(self):
        global mpiLock
        mpiLock.release()
        ThreadedWorkerCore.finalize(self)



class ParallelWork:
    ## ParallelWork encapsulates all the start-up
    ## and clean-up functions that the ParallelWorker
    ## subclasses do, such as communicating between
    ## the different machines behind the scenes
    ## through the adequate (socket) machinery
    def __init__(self, menuitem, args, kwargs):
        pipeToSocket(menuitem, args, kwargs)

        ## front-end tells back-end to execute
        ## same menuitem. self.callback() sorts what
        ## is the task that should be performed
        ## by each processor.
        ## back-end bypasses this function

        
class ParallelWorker(NonThreadedWorker, ParallelWork):
    ## Unthreaded Parallel Worker
    def __init__(self,  menuitem, args, kwargs):
        NonThreadedWorker.__init__(self, menuitem, args, kwargs)
        ParallelWork.__init__(self, menuitem, args, kwargs)
        
    
        
class ParallelThreadedWorker (ThreadedWorker, ParallelWork):
    ## Threaded Parallel Worker
    def __init__(self,  menuitem, args, kwargs):
        self.worker = ParallelThreadedWorkerCore(menuitem, args, kwargs)
        threadmanager.threadManager.newWorker(self.worker)
        ParallelWork.__init__(self, menuitem, args, kwargs)
        ThreadedWorker.__init__(self)
        
    def meanwhile(self):
        pass ## back-end should always pass and give control
    ## to socketinput, after launching the job
    
class ParallelTextThreadedWorker(TextThreadedWorker, ParallelWork):
    ## Text mode Threaded Parallel Worker
    ## sould only be called by front end
    def __init__(self,  menuitem, args, kwargs):
        ## TODO MER: PARALLEL This __init__ doesn't call
        ## TextThreadedWorker.__init__, and in fact it does things
        ## differently than that class does.  This seems to indicate
        ## that the class hierarchy is incorrect. Probably there
        ## should be a common base class for
        ## ParallelTextThreadedWorker and TextThreadedWorker.  That
        ## base class's __init__ would just set self.initialized and
        ## do nothing else.
        self.worker = ParallelThreadedWorkerCore(menuitem, args, kwargs)
        threadmanager.threadManager.newWorker(self.worker)
        TextThreadedWorker.__init__(self)
        ParallelWork.__init__(self, menuitem, args, kwargs)
        
def getThreadedParallelWorker(menuitem, argtuple, argdict):
    ## parallel workers
    try:
        from ooflib.SWIG.common import mpitools
        if mpitools.Rank() == 0:
            ## front-end runs threaded workers with text progress bars
            return ParallelTextThreadedWorker(menuitem, argtuple, argdict)
        ## back-end runs a threaded worker too, but no text progress bar
        ## is available. Back-end, instead, runs a thread, and the
        ## "front-end' of the back-end waits on the socket parser
        return ParallelThreadedWorker(menuitem, argtuple, argdict)
    except ImportError:
            raise


###############################

# getThreadedWorker() is redefined if the GUI is loaded in workerGUI.py

def getThreadedWorker(menuitem, argtuple, argdict):
    return TextThreadedWorker(menuitem, argtuple, argdict)


