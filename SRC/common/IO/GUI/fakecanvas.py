# -*- python -*-
# $RCSfile: fakecanvas.py,v $
# $Revision: 1.3.18.1 $
# $Author: langer $
# $Date: 2014/09/27 22:34:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# For debugging only

import gtk
from ooflib.SWIG.common import coord
from ooflib.SWIG.common import geometry

def dummyfunc(*args, **kwargs):
    global dummyfunc
    return dummyfunc

class FakeCanvas:
    def __init__(self, *args):
        pass
    def __getattr__(self, *args):
        global dummyfunc
        return dummyfunc
    def widget(self):
        return gtk.Frame()
    def get_pixels_per_unit(self):
        return 1
    def get_scrollregion(self):
        return geometry.CRectangle(coord.Coord(0,0), coord.Coord(1,1))
    def get_bounds(self):
        return geometry.CRectangle(coord.Coord(0,0), coord.Coord(1,1))
    def get_width_in_pixels(self):
        return 1
    def get_height_in_pixels(self):
        return 1
    def world_coord(self, *args):
        return coord.Coord(1,1)
    def window_coord(self, *args):
        return coord.Coord(1,1)
    def newLayer(self):
        return FakeCanvasLayer()
    def is_empty(self):
        return 0
    def __nonzero__(self):
        return 1

class FakeCanvasLayer:
    def __init__(self, *args):
        pass
    def __getattr__(self, *args):
        global dummyfunc
        return dummyfunc
