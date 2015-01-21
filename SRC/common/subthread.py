# -*- python -*-
# $RCSfile: subthread.py,v $
# $Revision: 1.36.2.3 $
# $Author: langer $
# $Date: 2014/08/02 03:14:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Routines for submitting functions to be run in a subthread.  A
## "subthread" is a thread that's not associated directly with a
## menuitem or worker, but may have been spawned by such a thread.
## When threads are enabled, a thread is launched executing the
## proposed function. If threads are not enabled, the function is
## simply called on the main thread.

from ooflib.SWIG.common import lock
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import threadstate
from ooflib.common import debug
from ooflib.common import excepthook
from ooflib.common import thread_enable
import exceptions
import sys
import threading


class StopThread(exceptions.Exception):
    def __init__ (self):
        exceptions.Exception.__init__(self)
    

class MiniThread(threading.Thread):
    def __init__(self, function, args=(), kwargs={}):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.immortal = False
        threading.Thread.__init__(self)
        self.threadstate = None

    def immortalize(self):
        self.immortal = True
        
    def run(self):
        miniThreadManager.add(self)
        try:
            try:
                self.threadstate = threadstate.ThreadState()
#                 debug.fmsg("assigning excepthook, function=", self.function)
                hook = excepthook.assign_excepthook(excepthook.OOFexceptHook())
                self.function(*self.args, **self.kwargs)
                excepthook.remove_excepthook(hook)
            except StopThread:
                excepthook.remove_excepthook(hook)
                return
            # TODO 3.1: After conversion to SWIG 2.x, if that ever
            # happens, OOF exceptions will probably be subclasses of
            # Exception.
            except (Exception, ooferror.ErrErrorPtr), exception:
                from ooflib.common.IO import reporter
                reporter.error(exception)
                sys.excepthook(*sys.exc_info())
        finally:
            miniThreadManager.remove(self)
            self.threadstate = None

    def stop_it(self):
        if not self.immortal:
            threadstate.cancelThread(self.threadstate)

def execute(function, args=(), kwargs={}):
    if thread_enable.query():
        littlethread = MiniThread(function, args, kwargs)
        littlethread.start()
    else:
        function(*args, **kwargs)

def execute_immortal(function, args=(), kwargs={}):
    if thread_enable.query():
        littlethread = MiniThread(function, args, kwargs)
        littlethread.immortalize()
        littlethread.start()
    else:
        function(*args, **kwargs)


## The purpose of the MiniThreadManager is to administer the running
## (mini) threads, so that when quitting time comes all minithreads
## are asked to stop properly, releasing their locks, and freeing the
## main thread. The main thread is left to execute other quitting
## tasks.

class MiniThreadManager:
    def __init__(self):
        self.listofminithreads =[]
        self.lock = lock.SLock()

    def add(self, minithread):
        self.lock.acquire()
        try:
            self.listofminithreads.append(minithread)
        finally:
            self.lock.release()


    def remove(self,minithread):
        self.lock.acquire()
        try:
            self.listofminithreads.remove(minithread)
        finally:
            self.lock.release()

    def stopAll(self):
        threadlist = []
        self.lock.acquire()
        try:
            threadlist = self.listofminithreads[:]
        finally:
            self.lock.release()
        for minithread in threadlist:
            minithread.stop_it()
            
    def waitForAllThreads(self):
        threadlist = []
        self.lock.acquire()
        try:
            threadlist = self.listofminithreads[:]
        finally:
            self.lock.release()
#         debug.fmsg("waiting for subthreads", 
#                    [ts.threadstate.id() for ts in threadlist 
#                     if not ts.immortal])
        for minithread in threadlist:
            if not minithread.immortal:
                minithread.join()

    # Return the calling thread's MiniThread object, if it has one, or
    # None.
    def getMiniThread(self):
        callers_ts = threadstate.findThreadState()
        if callers_ts:
            self.lock.acquire()
            try:
                for mini in self.listofminithreads:
                    if mini.threadstate == callers_ts:
                        return mini
            finally:
                self.lock.release()
        
    def quit(self):
        # Waiting for threads is a bad idea if this function is
        # called on the main thread, since it will block the main
        # thread.
        debug.subthreadTest()
        if len(self.listofminithreads) > 0:
            # This is done differently than it is for Worker threads.
            # Worker threads are stopped by setting the stop flag in
            # their Progress objects.  It is assumed that all Workers
            # working on long tasks are using Progress objects.
            # MiniThreads are probably not using them, so this calls
            # stopAll which ultimately calls pthread_cancel.
            # Unfortunately, pthread_cancel doesn't seem to work
            # reliably on all systems.
            self.stopAll()

            self.waitForAllThreads()
            
miniThreadManager = MiniThreadManager()

