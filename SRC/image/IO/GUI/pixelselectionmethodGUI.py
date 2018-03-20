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
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.image import pixelselectionmethod
from ooflib.common.IO.GUI import genericselectGUI
import ooflib.common.IO.GUI.pixelselectionmethodGUI as pixselmethGUI

@genericselectGUI.selectionGUIfor(pixelselectionmethod.ColorSelector)
class ColorSelectorGUI(pixselmethGUI.SingleClickVoxelSelectionMethodGUI):
    def up(self, x, y, buttons):
        voxel = self.getVoxel(x, y)
        wrange = self.toolbox.getParamValues('range')
        self.toolbox.setParamValues(point=voxel)
        self.toolbox.invokeMenuItem(
            pixelselectionmethod.ColorSelector(voxel, wrange))
        
