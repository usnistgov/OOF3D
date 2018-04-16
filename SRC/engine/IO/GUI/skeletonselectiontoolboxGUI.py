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
from ooflib.engine import skeletonselectionmodes
from ooflib.engine import skeletonselmodebase
from ooflib.engine.IO import skeletonselectiontoolbox


# Generate selection toolbox GUI subclasses for each of the selection
# modes (Element, Node, etc) defined in skeletonselectionmodes.py.

class SkeletonSelectionToolboxGUI(genericselectGUI.GenericSelectToolboxGUI):
    pass

for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
    class SpecificSkeletonSelectToolboxGUI(SkeletonSelectionToolboxGUI):
        selectionMode = mode
        changeSignal = mode.changedselectionsignal
        def displayName(self, name=mode.name):
            return "Select " + name + "s"
    def _makeGUI(self, tbgui=SpecificSkeletonSelectToolboxGUI):
        return tbgui(self, self.method)
    mode.toolboxclass.makeGUI = _makeGUI
        


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## OLD CODE BELOW HERE

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

# class SkeletonSelectionToolboxModeGUI(genericselectGUI.GenericSelectToolboxGUI):
#     def __init__(self, mode, tb):
#         self.mode = mode
#         genericselectGUI.GenericSelectToolboxGUI.__init__(self, tb,
#                                                           mode.methodclass)
#         # Switchboard callbacks that should be performed even when the
#         # toolbox isn't active go here.  Callbacks that are performed
#         # only when the toolbox IS active are installed in activate().
#         self.sbcallbacks.append(
#             switchboard.requestCallbackMain(self.mode.newselectionsignal,
#                                             self.newSelection)
#             )

#     def methodFactory(self):
#         return regclassfactory.RegisteredClassFactory(
#             self.method.registry, title="Method:", name="Method")
                                                          
#     def activate(self):
#         genericselectGUI.GenericSelectToolboxGUI.activate(self)
#         self.activecallbacks = [
#             switchboard.requestCallbackMain((self.gfxwindow(),
#                                              'layers changed'),
#                                             self.layerChangeCB) ,
#             switchboard.requestCallbackMain(self.mode.changedselectionsignal,
#                                             self.changedSelection)
#             ]
#     def deactivate(self):
#         genericselectGUI.GenericSelectToolboxGUI.deactivate(self)
#         map(switchboard.removeCallback, self.activecallbacks)
#         self.activecallbacks = []

#     def getSource(self):
#         return self.gfxwindow().topwho('Skeleton')

#     def finish_up(self, ptlist, view, shift, ctrl, selmeth):
#         self.selectionMethodFactory.set_defaults()
#         # The callback for this menuitem is
#         # GenericSelectToolbox.selectCB in genericselecttoolbox.py.
#         menuitem = getattr(self.toolbox.menu, selmeth.name())
#         menuitem.callWithDefaults(skeleton=self.getSourceName(),
#                                   points=ptlist, 
#                                   view=view,
#                                   shift=shift, ctrl=ctrl)
#     def undoCB(self, button):
#         self.toolbox.menu.Undo(skeleton=self.getSourceName())

#     def redoCB(self, button):
#         self.toolbox.menu.Redo(skeleton=self.getSourceName())

#     def clearCB(self, button):
#         self.toolbox.menu.Clear(skeleton=self.getSourceName())

#     def invertCB(self, button):
#         self.toolbox.menu.Invert(skeleton=self.getSourceName())

#     def hide(self):
#         self.gtk.hide()

#     def show(self):
#         self.gtk.show_all()

        
# class SkeletonSelectionToolboxGUI(toolboxGUI.GfxToolbox):
#     def __init__(self, toolbox):
#         # The 'toolbox' argument here is the non-gui toolbox
#         # corresponding to one of the inner toolboxes.  It doesn't
#         # matter which one.
#         toolboxGUI.GfxToolbox.__init__(self, toolbox)
#         vbox = gtk.VBox(spacing=2)
#         self.gtk.add(vbox)
#         bbox = gtk.HBox(spacing=2)
#         gtklogger.setWidgetName(bbox, "Select")
#         vbox.pack_start(bbox, expand=0, fill=0)
#         bbox.pack_start(gtk.Label("Select: "), expand=0, fill=0)

#         self.tbbox = gtk.Frame()       # holds SkeletonSelectionToolboxModes
#         vbox.pack_start(self.tbbox, expand=1, fill=1)
        
#         group = None
#         self.tbdict = {}
#         modebuttons = []
#         for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
#             if group:
#                 button = gtk.RadioButton(label=mode.name, group=group)
#             else:
#                 button = gtk.RadioButton(label=mode.name)
#                 group = button
#             modebuttons.append(button)
#             # bbox.pack_start(button, expand=0, fill=0)
#             gtklogger.setWidgetName(button, mode.name)
#             gtklogger.connect(button, 'clicked', self.switchModeCB, mode.name)

#             ## Get the actual toolbox for each mode.
#             tb = self.gfxwindow().getToolboxByName(mode.toolboxName())
#             tbgui = SkeletonSelectionToolboxModeGUI(mode, tb)
#             self.tbdict[mode.name] = tbgui
#         if config.dimension() == 2:
#             for button in modebuttons:
#                 bbox.pack_start(button, expand=0, fill=0)
#         if config.dimension() == 3:
#             table = gtk.Table(columns=2, rows=2)
#             bbox.pack_start(table, expand=0, fill=0)
#             table.attach(modebuttons[0], 0,1, 0,1)
#             table.attach(modebuttons[1], 1,2, 0,1)
#             table.attach(modebuttons[2], 0,1, 1,2)
#             table.attach(modebuttons[3], 1,2, 1,2)

#         self.activecallbacks = []
#         self.currentMode = None

#     def switchModeCB(self, button, modename):
#         if button.get_active():
#             self.setMode(modename)
        
#     def setMode(self, modename):
#         debug.mainthreadTest()
#         if self.currentMode:
#             mode = self.tbdict[self.currentMode]
#             mode.deactivate()
#             self.tbbox.remove(self.tbbox.get_children()[0])
#         self.currentMode = modename
#         mode = self.tbdict[modename]
#         self.tbbox.add(mode.gtk)
#         self.installMouseHandler()
#         mode.show()
#         mode.activate()

#     def activate(self):
#         if not self.active:
#             if self.currentMode is None:
#                 self.setMode(
#                     skeletonselmodebase.SkeletonSelectionMode.modes[0].name)
#             self.tbdict[self.currentMode].activate()
#             toolboxGUI.GfxToolbox.activate(self)
#     def deactivate(self):
#         if self.active:
#             self.tbdict[self.currentMode].deactivate()
#             toolboxGUI.GfxToolbox.deactivate(self)

#     def close(self):
#         for tb in self.tbdict.values():
#             tb.close()

#     def installMouseHandler(self):
#         self.tbdict[self.currentMode].installMouseHandler()
