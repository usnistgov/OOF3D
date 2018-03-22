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
from ooflib.SWIG.image import burn
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.image import pixelselectionmethod
from ooflib.common.IO.GUI import genericselectGUI
import ooflib.common.IO.GUI.pixelselectionmethodGUI as pixselmethGUI

@genericselectGUI.selectionGUIfor(pixelselectionmethod.ColorSelector)
class ColorSelectorGUI(pixselmethGUI.SingleClickVoxelSelectionMethodGUI):
    def up(self, x, y, buttons):
        who, voxel = self.getVoxel(x, y)
        if voxel is not None:
            wrange = self.toolbox.getParamValues('range')
            self.toolbox.setParamValues(point=voxel)
            self.toolbox.invokeMenuItem(
                who, pixelselectionmethod.ColorSelector(voxel, wrange))
        

@genericselectGUI.selectionGUIfor(burn.Burn)
class BurnGUI(pixselmethGUI.SingleClickVoxelSelectionMethodGUI):
    def up(self, x, y, buttons):
        who, voxel = self.getVoxel(x, y)
        if voxel is not None:
            self.toolbox.setParamValues(point=voxel)
            (local_flammability,
             global_flammability,
             color_space_norm,
             next_nearest) = self.toolbox.getParamValues("local_flammability",
                                                         "global_flammability",
                                                         "color_space_norm",
                                                         "next_nearest")
            self.toolbox.invokeMenuItem(
                who, burn.Burn(voxel, local_flammability, global_flammability,
                               color_space_norm, next_nearest))
