# -*- python -*-
# $RCSfile: skeletonselectiontoolboxGUI.py,v $
# $Revision: 1.29.10.11 $
# $Author: langer $
# $Date: 2014/11/05 16:54:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO.GUI import rubberband3d as rubberband
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common.IO.GUI import genericselectGUI
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.engine import skeletonselectionmethod
from ooflib.engine import skeletonselmodebase
import gtk

# The SkeletonSelectionToolbox GUI is a ToolboxGUI that contains other
# ToolboxGUI's.  The inner GUI's are instances of
# SkeletonSelectionToolboxModeGUI.  Inner toolboxes are selected by a
# set of radio buttons at the top of the outer toolbox.  The inner
# toolboxes and the buttons are created automatically from the
# SkeletonSelectionMode classes.  Each of the inner gui toolboxes
# corresponds to a non-gui toolbox class.  From the gfxwindow's point
# of view, though, there's only one gui toolbox (the outer one), so
# only one of the non-gui toolboxes has a makeGUI routine attached to
# it.

class SkeletonSelectionToolboxModeGUI(genericselectGUI.GenericSelectToolboxGUI):
    def __init__(self, mode, tb):
        self.mode = mode
        genericselectGUI.GenericSelectToolboxGUI.__init__(self, mode.name,
                                                          tb, mode.methodclass)
        # Switchboard callbacks that should be performed even when the
        # toolbox isn't active go here.  Callbacks that are performed
        # only when the toolbox IS active are installed in activate().
        self.sbcallbacks.append(
            switchboard.requestCallbackMain(self.mode.newselectionsignal,
                                            self.newSelection)
            )

    def methodFactory(self):
        return regclassfactory.RegisteredClassFactory(
            self.method.registry, title="Method:", name="Method")
                                                          
    def activate(self):
        genericselectGUI.GenericSelectToolboxGUI.activate(self)
        self.activecallbacks = [
            switchboard.requestCallbackMain((self.gfxwindow(),
                                             'layers changed'),
                                            self.layerChangeCB) ,
            switchboard.requestCallbackMain(self.mode.changedselectionsignal,
                                            self.changedSelection)
            ]
    def deactivate(self):
        genericselectGUI.GenericSelectToolboxGUI.deactivate(self)
        map(switchboard.removeCallback, self.activecallbacks)
        self.activecallbacks = []

    def getSource(self):
        return self.gfxwindow().topwho('Skeleton')

    def finish_up(self, ptlist, view, shift, ctrl, selmeth):
        self.selectionMethodFactory.set_defaults()
        # The callback for this menuitem is
        # GenericSelectToolbox.selectCB in genericselecttoolbox.py.
        menuitem = getattr(self.toolbox.menu, selmeth.name())
        menuitem.callWithDefaults(skeleton=self.getSourceName(),
                                  points=ptlist, 
                                  view=view,
                                  shift=shift, ctrl=ctrl)
    def undoCB(self, button):
        self.toolbox.menu.Undo(skeleton=self.getSourceName())

    def redoCB(self, button):
        self.toolbox.menu.Redo(skeleton=self.getSourceName())

    def clearCB(self, button):
        self.toolbox.menu.Clear(skeleton=self.getSourceName())

    def invertCB(self, button):
        self.toolbox.menu.Invert(skeleton=self.getSourceName())

    def hide(self):
        self.gtk.hide()

    def show(self):
        self.gtk.show_all()

        
class SkeletonSelectionToolboxGUI(toolboxGUI.GfxToolbox):
    def __init__(self, toolbox):
        # The 'toolbox' argument here is the non-gui toolbox
        # corresponding to one of the inner toolboxes.  It doesn't
        # matter which one.
        toolboxGUI.GfxToolbox.__init__(self, "Skeleton Selection", toolbox)
        vbox = gtk.VBox(spacing=2)
        self.gtk.add(vbox)
        bbox = gtk.HBox(spacing=2)
        gtklogger.setWidgetName(bbox, "Select")
        vbox.pack_start(bbox, expand=0, fill=0)
        bbox.pack_start(gtk.Label("Select: "), expand=0, fill=0)

        self.tbbox = gtk.Frame()       # holds SkeletonSelectionToolboxModes
        vbox.pack_start(self.tbbox, expand=1, fill=1)
        
        group = None
        self.tbdict = {}
        modebuttons = []
        for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
            if group:
                button = gtk.RadioButton(label=mode.name, group=group)
            else:
                button = gtk.RadioButton(label=mode.name)
                group = button
            modebuttons.append(button)
            # bbox.pack_start(button, expand=0, fill=0)
            gtklogger.setWidgetName(button, mode.name)
            gtklogger.connect(button, 'clicked', self.switchModeCB, mode.name)

            ## Get the actual toolbox for each mode.
            tb = self.gfxwindow().getToolboxByName(mode.toolboxName())
            tbgui = SkeletonSelectionToolboxModeGUI(mode, tb)
            self.tbdict[mode.name] = tbgui
        if config.dimension() == 2:
            for button in modebuttons:
                bbox.pack_start(button, expand=0, fill=0)
        if config.dimension() == 3:
            table = gtk.Table(columns=2, rows=2)
            bbox.pack_start(table, expand=0, fill=0)
            table.attach(modebuttons[0], 0,1, 0,1)
            table.attach(modebuttons[1], 1,2, 0,1)
            table.attach(modebuttons[2], 0,1, 1,2)
            table.attach(modebuttons[3], 1,2, 1,2)

        self.activecallbacks = []
        self.currentMode = None

    def switchModeCB(self, button, modename):
        self.setMode(modename)
        
    def setMode(self, modename):
        debug.mainthreadTest()
        if self.currentMode:
            mode = self.tbdict[self.currentMode]
            mode.deactivate()
            self.tbbox.remove(self.tbbox.get_children()[0])
        self.currentMode = modename
        mode = self.tbdict[modename]
        self.tbbox.add(mode.gtk)
        mode.show()
        mode.activate()

    def activate(self):
        if not self.active:
            if self.currentMode is None:
                self.setMode(
                    skeletonselmodebase.SkeletonSelectionMode.modes[0].name)
            self.tbdict[self.currentMode].activate()
            toolboxGUI.GfxToolbox.activate(self)
    def deactivate(self):
        if self.active:
            self.tbdict[self.currentMode].deactivate()
            toolboxGUI.GfxToolbox.deactivate(self)


######################################

## Although there are many non-gui SkeletonSelectionToolboxes, they
## all share a GUI panel, so only one of them has a makeGUI function.

def _makeGUI(self):
    return SkeletonSelectionToolboxGUI(self)

skeletonselmodebase.firstMode().tbclass.makeGUI = _makeGUI

#####################################

## Assignment of rubberband types to SkeletonSelectionRegistration
## instances.  Most assignments are to *instances*, and as such are
## not member functions.  The default assignment (no rubberband) is to
## the class, and so the function needs a 'self' argument.

def _NoRubberBand(self, reg):
    debug.mainthreadTest()
    return rubberband.NoRubberBand()

skeletonselectionmethod.SkeletonSelectionRegistration.getRubberBand = \
    _NoRubberBand

if config.dimension() == 2:


    def _RectangleSelectorRB(reg):
        return rubberband.RectangleRubberBand()

    def _CircleSelectorRB(reg):
        return rubberband.CircleRubberBand()

    def _EllipseSelectorRB(reg):
        return rubberband.EllipseRubberBand()

    skeletonselectionmethod.rectangleNodeSelector.getRubberBand = \
        _RectangleSelectorRB
    skeletonselectionmethod.circleNodeSelector.getRubberBand = \
        _CircleSelectorRB
    skeletonselectionmethod.ellipseNodeSelector.getRubberBand = \
        _EllipseSelectorRB
    skeletonselectionmethod.rectangleSegmentSelector.getRubberBand = \
        _RectangleSelectorRB
    skeletonselectionmethod.circleSegmentSelector.getRubberBand = \
        _CircleSelectorRB
    skeletonselectionmethod.ellipseSegmentSelector.getRubberBand = \
        _EllipseSelectorRB
    skeletonselectionmethod.rectangleElementSelector.getRubberBand = \
        _RectangleSelectorRB
    skeletonselectionmethod.circleElementSelector.getRubberBand = \
        _CircleSelectorRB
    skeletonselectionmethod.ellipseElementSelector.getRubberBand = \
        _EllipseSelectorRB
