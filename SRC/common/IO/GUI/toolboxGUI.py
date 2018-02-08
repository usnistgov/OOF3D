# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import toolbox
from ooflib.common import primitives
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import widgetscope
import gtk
import sys

class GfxToolbox(widgetscope.WidgetScope):
    def __init__(self, toolbox):
        debug.mainthreadTest()
        self.toolbox = toolbox          # non-GUI toolbox
        self.gtk = gtk.Frame()          # root of toolbox's gtk widget tree
        gtklogger.setWidgetName(self.gtk, self.toolbox.name())
        self.gtk.set_shadow_type(gtk.SHADOW_NONE)
        self.active = 0
        widgetscope.WidgetScope.__init__(self, parent=None)
    def name(self):
        return self.toolbox.name()
    def close(self):
        pass

    def activate(self):
        ## TODO: active should only be in the Toolbox class.  No need
        ## to store it in GfxToolbox as well.  There may be places in
        ## the code that assume it's in GfxToolbox, which should be
        ## changed.
        self.active = True
        self.toolbox.active = True
        switchboard.notify("toolbox activated " + self.name(),
                           self.toolbox.gfxwindow())
    def deactivate(self):
        self.active = False
        self.toolbox.active = False
        switchboard.notify("toolbox deactivated " + self.name(),
                           self.toolbox.gfxwindow())
    def gfxwindow(self):
        return self.toolbox.gfxwindow()
    def installMouseHandler(self):
        # The default mouse handler is no mouse handler.  Subclasses
        # should override this if they need to handle mouse clicks on
        # the canvas when the window is in "select" mode.
        self.gfxwindow().removeMouseHandler()
        
    def __cmp__(self, other):           # for sorting in gfxwindow's list
        return cmp(self.toolbox.ordering, other.toolbox.ordering)

    # # convenience function to get a point object from mouseclick coordinates
    # def getPoint(self, x, y):
    #     if config.dimension() == 2:
    #         return primitives.Point(x,y)
    #     elif config.dimension() == 3:
    #         p = self.gfxwindow().oofcanvas.screen_coords_to_3D_coords(x,y) 
    #         if p:
    #             return primitives.Point(p[0],p[1],p[2])
    #         else:
    #             return None

# The base Toolbox class doesn't make a GUI, but it provides a trivial
# makeGUI function so that derived toolboxes that don't create a GUI
# don't have to define makeGUI themselves.

def _makeGUI(self):
    pass

toolbox.Toolbox.makeGUI = _makeGUI
