# -*- python -*-
# $RCSfile: mainthread.py,v $
# $Revision: 1.12.2.2 $
# $Author: fyc $
# $Date: 2014/07/21 18:08:30 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

## TODO OPT: Why do we need mainthread()?  It's not used very much.  Just
## call threadstate.mainthread_query() directly.

from ooflib.SWIG.common import threadstate

def mainthread():
    return threadstate.mainthread_query()

############

# Routines for submitting functions to be run in the main thread.

# When not in threaded graphics mode, both run() and runBlock() just
# execute the given function.  In threaded graphics mode, they execute
# the function on the main thread.  In that case, run() doesn't wait
# for an answer, so it can't return a value.  runBlock() does wait, so
# it does return a value.


def _run(func, args=(), kwargs={}):
    func(*args, **kwargs)

def _runBlock(func, args=(), kwargs={}):
    return func(*args, **kwargs)

# These variables get overwritten by mainthreadGUI, when it's imported.
run = _run
runBlock = _runBlock

    
