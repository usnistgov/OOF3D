# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common.IO.GUI import genericselectGUI
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.engine import skeletonselectionmodes
from ooflib.engine import skeletonselmodebase
import gtk

# The SkeletonSelectionToolbox GUI is a ToolboxGUI that contains other
# ToolboxGUI's.  The inner GUI's are instances of
# SkeletonSelectionToolboxModeGUI.  Inner toolboxes are selected by a
# set of radio buttons at the top of the outer toolbox.  The inner
# toolboxes and the buttons are created automatically from the
# SkeletonSelectionMode classes.  Each of the inner gui toolboxes
# corresponds to a non-gui toolbox class.

tbclasses = {}

class SkeletonSelectionToolboxGUI(toolboxGUI.GfxToolbox):
    def __init__(self, toolbox):
        # The 'toolbox' argument here is the non-gui toolbox
        # corresponding to one of the inner toolboxes.  It doesn't
        # matter which one.
        toolboxGUI.GfxToolbox.__init__(self, toolbox)
        vbox = gtk.VBox(spacing=2)
        self.gtk.add(vbox)

        bbox = gtk.HBox(spacing=2)
        gtklogger.setWidgetName(bbox, "Select")
        vbox.pack_start(bbox, expand=0, fill=0)
        bbox.pack_start(gtk.Label("Select: "), expand=0, fill=0)

        self.tbbox = gtk.Frame() # holds SkelSelToolboxModeGUIs
        vbox.pack_start(self.tbbox, expand=1, fill=1)

        group = None
        self.tbdict = {}
        modebuttons = []
        skeletonselectionmodes.initialize()
        for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
            if group:
                button = gtk.RadioButton(label=mode.name, group=group)
            else:
                button = gtk.RadioButton(label=mode.name)
                group = button
            modebuttons.append(button)
            gtklogger.setWidgetName(button, mode.name)
            gtklogger.connect(button, 'clicked', self.switchModeCB, mode.name)

            # Get the actual toolbox for each mode
            tb = self.gfxwindow().getToolboxByName(mode.toolboxName())
            tbgui = tbclasses[mode.name](tb, tb.method)
            self.tbdict[mode.name] = tbgui

        table = gtk.Table(columns=2, rows=2)
        bbox.pack_start(table, expand=0, fill=0)
        table.attach(modebuttons[0], 0,1, 0,1)
        table.attach(modebuttons[1], 1,2, 0,1)
        table.attach(modebuttons[2], 0,1, 1,2)
        table.attach(modebuttons[3], 1,2, 1,2)

        self.currentMode = None
        self.setMode(skeletonselmodebase.firstMode().name)

    def displayName(self):
        return "Skeleton Selection"

    def switchModeCB(self, button, modename):
        if button.get_active():
            self.setMode(modename)

    def setMode(self, modename):
        debug.mainthreadTest()
        if self.currentMode:
            mode = self.tbdict[self.currentMode]
            mode.deactivate()
            self.tbbox.remove(self.tbbox.get_children()[0])
        self.currentMode = modename
        subtb = self.tbdict[modename]
        self.tbbox.add(subtb.gtk)
        self.installMouseHandler()
        subtb.show()
        subtb.activate()

    def close(self):
        for tb in self.tbdict.values():
            tb.close()

    def activate(self):
        if not self.active:
            if self.currentMode is None:
                self.setMode(skeletonselmodebase.firstMode().name)
            else:
                self.tbdict[self.currentMode].activate()
            toolboxGUI.GfxToolbox.activate(self)
    def deactivate(self):
        if self.active:
            if self.currentMode is not None:
                self.tbdict[self.currentMode].deactivate()
            toolboxGUI.GfxToolbox.deactivate(self)

    def installMouseHandler(self):
        if self.currentMode is not None:
            self.tbdict[self.currentMode].installMouseHandler()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Generate selection toolbox GUI subclasses for each of the selection
# modes (Element, Node, etc) defined in skeletonselectionmodes.py.

# Although there are many non-gui SkeletonSelectionToolboxes, they
# all share a GUI panel, so only one of them has a makeGUI function.
first = True

for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
    class SkelSelToolboxModeGUI(genericselectGUI.GenericSelectToolboxGUI):
        selectionMode = mode
        changeSignal = mode.changedselectionsignal
        def displayName(self, name=mode.name):
            return "Select " + name + "s"
    tbclasses[mode.name] = SkelSelToolboxModeGUI
    if first:
        def _makeGUI(self):
            return SkeletonSelectionToolboxGUI(self)
        mode.toolboxclass.makeGUI = _makeGUI
        first = False

