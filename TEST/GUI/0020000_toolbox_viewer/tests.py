# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:12:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import sys, math, time

def checkCanvasPPU(initial_ppu, factor, tol=1.0e-6):
    # Assume there is only one graphics window.
    ppu = initial_ppu*factor
    import ooflib.common.IO.gfxmanager as gfxmanager
    gw = gfxmanager.gfxManager.windows[-1]
    res = gw.oofcanvas.get_pixels_per_unit()
    check = math.fabs(res-ppu)
    if not check<tol:
        print >> sys.stderr, "Canvas PPU failed, %f !< %f." % (check, tol)
        return False
    return True
    

def getCanvasPPU():
    import ooflib.common.IO.gfxmanager as gfxmanager
    gw = gfxmanager.gfxManager.windows[-1]
    return gw.oofcanvas.get_pixels_per_unit()
