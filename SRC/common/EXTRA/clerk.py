import time, sys, os
import threading
from ooflib.SWIG.common import threadstate
class  Clerk(threading.Thread):
    def __init__(self, function, args=(), kwargs={}):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        threading.Thread.__init__(self)
        self.threadstate = None
        threadstate.cleanList()
        
    def run(self):
        print os.getpid()
        ## startTime = time.time()
        try:
            try:
                self.threadstate = threadstate.findThreadState()
                self.function(*self.args, **self.kwargs)
                return
            except Exception, exception:
                print exception
                sys.stdout.flush()
        finally:
            self.threadstate.make_defunct()
            ##  endTime = time.time()
            ##print "processing time=", endTime -startTime
            ## sys.stdout.flush()
            
    
