# -*- python -*-
# $RCSfile: garbage.py,v $
# $Revision: 1.4.10.1 $
# $Author: langer $
# $Date: 2014/06/25 21:39:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This is an attempt to work around errors apparently arising when gtk
# objects are garbage collected in the wrong thread.  We disable
# automatic garbage collection, and run gc.collect() manually when
# we're sure we're on the main thread.

from ooflib.common import thread_enable
from ooflib.common import mainthread

disabled = False

try:
    import gc
except ImportError:
    def disable():
        pass
    def collect():
        pass
else:
    def disable():
        global disabled
        disabled = True
        gc.disable()
        
    def collect():
        if disabled:
            mainthread.runBlock(gc.collect)

    gc.set_debug(gc.DEBUG_UNCOLLECTABLE)
