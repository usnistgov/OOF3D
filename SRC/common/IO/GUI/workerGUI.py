# -*- python -*-
# $RCSfile: workerGUI.py,v $
# $Revision: 1.22.2.1 $
# $Author: langer $
# $Date: 2012/03/16 15:29:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import parallel_enable
from ooflib.common import thread_enable
from ooflib.common import threadmanager
from ooflib.common import worker


def getThreadedWorker(menuitem, argtuple, argdict):
    if not thread_enable.query():
        return worker.NonThreadedWorker(menuitem, argtuple, argdict)
    if mainthread.mainthread():
        return worker.ThreadedWorker(menuitem, argtuple, argdict)
    # Threading is enabled, but this isn't the main thread.  We must
    # be running a script, because that is the only way to create
    # workers that don't start on the main thread.  Scripts can't run
    # their commands concurrently, so we need to create a worker that
    # blocks until the command finishes.
    return GUIThreadedWorkerBlock(menuitem, argtuple, argdict)

worker.getThreadedWorker = getThreadedWorker

class GUIThreadedWorkerBlock(worker.ThreadedWorker):
    def isTopLevel(self):
        return False
    def meanwhile(self):
        self.join()              # waits for child thread to finish
        
###############


class GUIParallelThreadedWorker(worker.ThreadedWorker,
                                worker.ParallelWork):
    def __init__ (self, menuitem, args, kwargs):
        self.worker = worker.ParallelThreadedWorkerCore(menuitem, args, kwargs)
        threadmanager.threadManager.newWorker(self.worker)
        worker.ParallelWork.__init__(self, menuitem, args, kwargs)
        
class GUIParallelThreadedWorkerBlock(GUIThreadedWorkerBlock,
                                     worker.ParallelWork):
    def __init__ (self, menuitem, args, kwargs):
        self.worker = worker.ParallelThreadedWorkerCore(
            menuitem, args, kwargs)
        threadmanager.threadManager.newWorker(self.worker)
        worker.ParallelWork.__init__(self, menuitem, args, kwargs)

def getThreadedParallelWorker(menuitem, argtuple, argdict):
    ## parallel workers
    ## only called by front-end
    ## back-end is running on text-mode, without any text
    ## progress bars
    if not thread_enable.query():
        ## if GUI is not in place yet, do not 
        ## launch a thread. Instead run a serial
        ## parallel worker
        return worker.ParallelWorker(menuitem, argtuple, argdict)
    if mainthread.mainthread():
        ## if main thread launches a parallel thread
        ## launch a GUI worker
        return GUIParallelThreadedWorker(menuitem, argtuple, argdict)
    ## if subthread is attempting to launch a thread,
    ## block the subthread, until, sub-subthread joins
    return GUIParallelThreadedWorkerBlock(menuitem, argtuple, argdict)

worker.getThreadedParallelWorker = getThreadedParallelWorker
