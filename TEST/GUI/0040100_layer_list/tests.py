# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:40 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

layerlist ="OOF2 Graphics 1:Pane0:LayerScroll:LayerList"

# Layer tests also appear in 03100.  If they're copied again, put them
# in a common file.

def _gfxWindow(name):
    from ooflib.common.IO import gfxmanager
    return gfxmanager.gfxManager.getWindow(name)

def _listedLayers():
    return [l.name() for l in _gfxWindow('Graphics_1').listedlayers()]

def layerCheck(*layers):
    names = _listedLayers()
    ok = (names == list(layers))
    if not ok:
        print >> sys.stderr, names
    return ok

def allLayerNames(*layers):
    names = [l.name() for l in treeViewColValues(layerlist, 0)]
    ok = names == list(layers)
    if not ok:
        print names
    return ok

def selectedLayerCheck(layer):
    sl = _gfxWindow("Graphics_1").selectedLayer
    if sl is not None:
        if layer == sl.name():
            return True
        else:
            print >> sys.stderr, sl.name()
            return False
    return layer is None

def hiddenLayer(layername, hidden):
    names = [l.name() for l in treeViewColValues(layerlist, 0)]
    which = names.index(layername)
    # now what?
