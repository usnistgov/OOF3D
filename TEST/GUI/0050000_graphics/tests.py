# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

layerlist = "OOF2 Graphics 1:Pane0:LayerScroll:LayerList"
    
def layerMenuSensitization(menuitem, sensitivity):
    actual = menuSensitive("OOF2 Graphics 1:MenuBar", "Layer:" + menuitem)
    if actual != sensitivity:
        print >> sys.stderr, "Layer menu sensitization failed for", menuitem
        return 0
    return 1
        

def sensitizationCheck0():
    return (layerMenuSensitization("New", 1) and
            layerMenuSensitization("Edit", 0) and
            layerMenuSensitization("Delete", 0) and
            layerMenuSensitization("Hide", 0) and
            layerMenuSensitization("Show", 0) and
            layerMenuSensitization("Hide_Contour_Map", 0) and
            layerMenuSensitization("Show_Contour_Map", 0) and
            layerMenuSensitization("Raise", 0) and
            layerMenuSensitization("Lower", 0) and
            layerMenuSensitization("Reorder_All", 0)
            )

def sensitizationCheck1():
    return (layerMenuSensitization("New", 1) and
            layerMenuSensitization("Edit", 1) and
            layerMenuSensitization("Delete", 1) and
            layerMenuSensitization("Hide", 1) and
            layerMenuSensitization("Show", 0) and
            layerMenuSensitization("Hide_Contour_Map", 0) and
            layerMenuSensitization("Show_Contour_Map", 0) and
            layerMenuSensitization("Raise", 1) and
            layerMenuSensitization("Lower", 1) and
            layerMenuSensitization("Reorder_All", 0)
            )

def sensitizationCheck2():
    return (layerMenuSensitization("New", 1) and
            layerMenuSensitization("Edit", 1) and
            layerMenuSensitization("Delete", 1) and
            layerMenuSensitization("Hide", 1) and
            layerMenuSensitization("Show", 0) and
            layerMenuSensitization("Hide_Contour_Map", 0) and
            layerMenuSensitization("Show_Contour_Map", 0) and
            layerMenuSensitization("Raise", 1) and
            layerMenuSensitization("Lower", 1) and
            layerMenuSensitization("Reorder_All", 1)
            )

def sensitizationCheck3():
    return (layerMenuSensitization("New", 1) and
            layerMenuSensitization("Edit", 1) and
            layerMenuSensitization("Delete", 1) and
            layerMenuSensitization("Hide", 1) and
            layerMenuSensitization("Show", 0) and
            layerMenuSensitization("Hide_Contour_Map", 0) and
            layerMenuSensitization("Show_Contour_Map", 0) and
            layerMenuSensitization("Raise", 0) and
            layerMenuSensitization("Lower", 1) and
            layerMenuSensitization("Reorder_All", 1)
            )

def sensitizationCheck4():
    return (layerMenuSensitization("New", 1) and
            layerMenuSensitization("Edit", 1) and
            layerMenuSensitization("Delete", 1) and
            layerMenuSensitization("Hide", 1) and
            layerMenuSensitization("Show", 0) and
            layerMenuSensitization("Hide_Contour_Map", 0) and
            layerMenuSensitization("Show_Contour_Map", 0) and
            layerMenuSensitization("Raise", 1) and
            layerMenuSensitization("Lower", 0) and
            layerMenuSensitization("Reorder_All", 0)
            )

def sensitizationCheck5():
    return (layerMenuSensitization("New", 1) and
            layerMenuSensitization("Edit", 1) and
            layerMenuSensitization("Delete", 1) and
            layerMenuSensitization("Hide", 0) and
            layerMenuSensitization("Show", 1) and
            layerMenuSensitization("Hide_Contour_Map", 0) and
            layerMenuSensitization("Show_Contour_Map", 0) and
            layerMenuSensitization("Raise", 1) and
            layerMenuSensitization("Lower", 1) and
            layerMenuSensitization("Reorder_All", 0)
            )

def sensitizationCheck6():
    return (layerMenuSensitization("New", 1) and
            layerMenuSensitization("Edit", 1) and
            layerMenuSensitization("Delete", 1) and
            layerMenuSensitization("Hide", 1) and
            layerMenuSensitization("Show", 0) and
            layerMenuSensitization("Hide_Contour_Map", 1) and
            layerMenuSensitization("Show_Contour_Map", 0) and
            layerMenuSensitization("Raise", 1) and
            layerMenuSensitization("Lower", 1) and
            layerMenuSensitization("Reorder_All", 0)
            )

def _gfxWindow(name):
    from ooflib.common.IO import gfxmanager
    return gfxmanager.gfxManager.getWindow(name)

# Layer tests also appear in 03200.  If they're copied again, put them
# in a common file.
def _listedLayers(windowname):
    return [l.name() for l in _gfxWindow(windowname).listedLayers()]

def layerCheck(*layers):
    names = _listedLayers("Graphics_1")
    ok = names == list(layers)
    if not ok:
        print >> sys.stderr, names
    return ok

def selectedLayerCheck(layer):
    sl = _gfxWindow("Graphics_1").selectedLayer
    if sl is not None:
        return layer == sl.name()
    return layer is None

def allLayerNames(*layers):
    names = [l.name() for l in treeViewColValues(layerlist, 0)]
    ok = names == list(layers)
    if not ok:
        print names
    return ok

def contourLabels():
    return (gtklogger.findWidget(
        "OOF2 Graphics 1:Pane0:Pane1:ContourMap:MapMin"),
            gtklogger.findWidget(
        "OOF2 Graphics 1:Pane0:Pane1:ContourMap:MapMax"))


def contourBounds(min, max, tolerance=1.e-6):
    minlabel, maxlabel = contourLabels()
    return (abs(float(maxlabel.get_text()) - max) < tolerance and
            abs(float(minlabel.get_text()) - min) < tolerance)

def noContourBounds():
    minlabel, maxlabel = contourLabels()
    return minlabel.get_text() == "min" and maxlabel.get_text() == "max"
