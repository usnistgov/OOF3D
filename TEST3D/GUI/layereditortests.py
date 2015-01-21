# -*- python -*-
# $RCSfile: layereditortests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/23 14:34:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from generics import *

categoryChooser = "OOF2 Graphics Layer Editor:ObjectScroll:category"
objectChooser = "OOF2 Graphics Layer Editor:ObjectScroll:object"
methodList = "OOF2 Graphics Layer Editor:DisplayMethods:ListScroll:List"

def _gfxWindow(name):
    from ooflib.common.IO import gfxmanager
    return gfxmanager.gfxManager.getWindow(name)

def _listedLayers(windowname):
    return [l.name() for l in _gfxWindow(windowname).listedLayers()]

def layerCheck(gfxwindow, *layers):
    ok = _listedLayers(gfxwindow) == list(layers)
    if not ok:
        print >> sys.stderr, _listedLayers(gfxwindow)
    return ok

def selectedLayerCheck(gfxwindow, layer):
    sl = _gfxWindow(gfxwindow).selectedLayer
    if sl is not None:
        return layer == sl.name()
    return layer is None

def objectCheck(category, object):
    return chooserStateCheck(objectChooser+":"+category, object)

def categoryCheck(category):
    return chooserStateCheck(categoryChooser, category)

def newMethodCheck(category, object, method):
    return chooserStateCheck(
        "Dialog-New Display Method for " + category + " " + object +
        ":method:Chooser",
        method)
                             
def layerEditorListCheck(*layers):
    return chooserCheck(methodList, layers)

def layerEditorSelectionCheck(layer=None):
    if layer:
        return chooserListStateCheck(methodList, [layer])
    return chooserListStateCheck(methodList, [])

def layerEditorSelectionWhichCheck(n):
    return chooserListStateCheckN(methodList, [n])

def newElementEdgeWidthCheck(width):
    # Check that the edge width show in the layer editing window is
    # correct.  This is a quick way of checking that the right layer
    # is being edited, because the test suite fiddles with the width.
    return gtkTextCompare(
        "Dialog-New Display Method for Skeleton skeleton:method:Element Edges:width:entry",
        `width`)

def layerEditorDestination(dest):
    return chooserStateCheck("OOF2 Graphics Layer Editor:Destination", dest)

def layerEditorDestinationList(*dests):
    return chooserCheck("OOF2 Graphics Layer Editor:Destination", dests)
