# -*- python -*-
# $RCSfile: thread_enable.py,v $
# $Revision: 1.17.18.2 $
# $Author: langer $
# $Date: 2011/10/18 15:46:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

_enable = True

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import threadstate

def set(state):
    global _enable
    _enable = state
    threadstate.cvar.threading_enabled = state

def query():
    global _enable
    return _enable and guitop.getMainLoop() 

def enabled():
    global _enable
    return _enable

    

