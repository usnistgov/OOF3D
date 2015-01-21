# -*- python -*-
# $RCSfile: threadmanager.py,v $
# $Revision: 1.2.2.5 $
# $Author: langer $
# $Date: 2014/09/16 00:42:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import string
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import thread_enable
from ooflib.common.IO import reporter

## ThreadManager coordinates the thread-enabled menu items of OOF.  It
## administers the existing running threaded processes.  It also
## sends/receives instructions for automatically stopping them when
## the appropriate flag is set.

class ThreadManager:
    def __init__(self):
        ## Keep list of workers in order to quit properly.  At exit
        ## time, the ThreadManager loops over the running workers and
        ## forces them to stop and join.
        self.listofworkers = []
        self.lock = lock.SLock() 
        
    def quit(self, menuitem = None):
        self.lock.acquire()
        workers = self.listofworkers[:]
        self.lock.release()
        for worker in workers:
            worker.stop()
        # Wait for all Workers to finish. This should *not* be called
        # on the mainthread, because blocking here may prevent threads
        # from finishing if they need to use the main thread.
        for worker in workers:
            worker.join()
        
    def nWorkers(self):
        return len(self.listofworkers)
    def allWorkers(self):
        self.lock.acquire()
        try:
            return self.listofworkers[:]
        finally:
            self.lock.release()

    def stopAll(self):
        ## called by activityViewer and by ThreadManager.quit.
        self.lock.acquire()
        try:
            for worker in self.listofworkers[:]:
                worker.stop()
        finally:
            self.lock.release()

#     def cancelAll(self):
#         ## for internal use only.
#         ## Must run in main thread (TODO OPT: Why?)
#         self.lock.acquire()
#         try:
#             for worker in self.listofworkers :
#                 worker.cancel()
#         finally:
#             self.lock.release()

    def newWorker (self, newworker):
        self.lock.acquire()
        try:
            self.listofworkers.append(newworker)
        finally:
            self.lock.release()

    def removeWorker(self, oldworker):
        self.lock.acquire()
        try:
            # TODO: This used to catch and discard all exceptions, for
            # no obvious reason.  If the reason becomes obvious, it
            # should be documented here!
            self.listofworkers.remove(oldworker)
        finally:
            self.lock.release()


threadManager = ThreadManager() 
