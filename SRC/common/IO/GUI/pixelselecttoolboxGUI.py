# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import pixelselectionmethod
from ooflib.common import primitives
from ooflib.common.IO import pixelselectiontoolbox
from ooflib.common.IO.GUI import genericselectGUI
from ooflib.common.IO.GUI import pixelselectionmethodGUI

class PixelSelectToolboxGUI(genericselectGUI.GenericSelectToolboxGUI):
    def __init__(self, pixelselecttoolbox, method):
        debug.mainthreadTest()

        genericselectGUI.GenericSelectToolboxGUI.__init__(self,
                                                   pixelselecttoolbox,
                                                   method)

        # # Switchboard callbacks that should be performed even when the
        # # toolbox isn't active go here.  Callbacks that are performed
        # # only when the toolbox IS active are installed in activate().
        # self.sbcallbacks.extend([
        #     switchboard.requestCallbackMain('new pixel selection',
        #                                     self.newSelection),
        #     # switchboard.requestCallbackMain((self.gfxwindow(),
        #     #                                  'layers changed'),
        #     #                                 self.layerChangeCB)
        #     ])
    def displayName(self):
        return "Select Voxels"

    def activate(self):
        if not self.active:
            super(PixelSelectToolboxGUI, self).activate()
            # Switchboard callbacks that are performed only when the
            # toolbox is active:
            self.activecallbacks = [
                switchboard.requestCallbackMain('pixel selection changed',
                                                self.changedSelection)
            ]

    def deactivate(self):
        if self.active:
            map(switchboard.removeCallback, self.activecallbacks)
            super(PixelSelectToolboxGUI, self).deactivate()
            self.activecallbacks = []


def _makeGUI(self):
    return PixelSelectToolboxGUI(self, self.method)

pixelselectiontoolbox.PixelSelectToolbox.makeGUI = _makeGUI

