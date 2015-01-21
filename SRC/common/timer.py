# -*- python -*-
# $RCSfile: timer.py,v $
# $Revision: 1.4.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


import time

class Timer:
    alltimers = {}
    def __init__(self, name):
        self.elapsed_time = 0.
        self.on = 0
        self.name = name
        Timer.alltimers[name] = self
    def start(self):
        self.on = 1
        self.starttime = time.clock()
    def stop(self):
        self.on = 0
        dt = time.clock() - self.starttime
        self.elapsed_time += dt
    def elapsed(self):
        if self.on:
            return self.elapsed_time + time.clock() - self.starttime
        else:
            return self.elapsed_time
    def delete(self):
        del Timer.alltimers[self.name]

def getTimer(name):
    try:
        return Timer.alltimers[name]
    except KeyError:
        return Timer(name)
