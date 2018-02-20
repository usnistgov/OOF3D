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
from ooflib.common import registeredclass
from ooflib.common import subthread
from ooflib.common import voxelselectionmethod
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import chooser
import gtk, sys

class VoxelSelectionToolboxGUI(toolboxGUI.GfxToolbox):
    def __init__(self, toolbox):
        debug.mainthreadTest()
        toolboxGUI.GfxToolbox.__init__(self, toolbox)

        self.gtk = gtk.Frame()
        outerbox = gtk.VBox(spacing=2)
        self.gtk.add(outerbox)

        self.methodChooser = chooser.ChooserWidget(
            [], callback=self.methodCB, name="Method")
        self.methodBox = gtk.VBox()
        outerbox.add
        
        
        # Create instances of each selection method's subtoolbox.
        self.selectionMethodGUIs = {}
        for reg in selectorBaseClass.registry:
            self.selectionMethodGUIs[reg.subclass] = reg.makeGUI(self)
        self.mouseHandler = None
        

        
        # Switchboard callbacks that should be performed even when the
        # toolbox isn't active go here.  Callbacks that are performed
        # only when the toolbox IS active are installed in activate().
        self.sbcallbacks.extend([
            switchboard.requestCallbackMain(
                (self.gfxwindow(), 'layers changed'), self.layerChangeCB)
        ])

    def methodFactory(self):
        return VoxelSelectionMethodFactory(self.method.registry,
                                           title="Method:",
                                           name="Method",
                                           scope=self,
                                           callback=self.updateMouseHandler,
                                           widgetdict=self.selectionmethodGUIs)

    def getSource(self):
        return self.gfxwindow().topwho('Microstructure', 'Image')
    
    def layerChangeCB(self):
        # This must be called even when the toolbox isn't active,
        # because the selection method factory has to list only those
        # methods that are valid for the current top layer.
        # set_whoclass_name has to be called whenever the top layer
        # changes, or it has to be called when the toolbox is
        # activated AND when the toolbox is active and the layer
        # changes.
        source = self.getSource()
        if source:
            self.selectionMethodFactory.set_whoclass_name(source.getClassName())
        else:
            self.selectionMethodFactory.set_whoclass_name(None)
        self.updateSelectionMethods()
        genericselectGUI.GenericSelectToolboxGUI.layerChangeCB(self)

    # installMouseHandler is called when the gfxwindow switches from
    # one toolbox to another, or when control is otherwise given to
    # the toolbox.  updateMouseHandler is called when the toolbox
    # switches from one selection mode to another.

    def installMouseHandler(self):
        self.updateMouseHandler(self.selectionMethodFactory.getRegistration())
    def updateMouseHandler(self, registration):
        if self.mouseHandler is not None:
            self.mouseHandler.stop() # waits for thread to finish
        if registration is not None:
            subtoolbox = self.selectionMethodGUIs[reg.subclass]
            self.mousehandler = subtoolbox.mouseHandler()
            self.gfxwindow.setMouseHandler(self.mouseHandler)
        
