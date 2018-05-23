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
from ooflib.common.IO import pixelselectiontoolbox
from ooflib.common.IO.GUI import genericselectGUI

## TODO: It's odd for changeSignal to be data while displayName is a
## function.  Make them both the same, here and in the skeleton
## selection toolboxes.

class PixelSelectToolboxGUI(genericselectGUI.GenericSelectToolboxGUI):
    changeSignal = "pixel selection changed"
    def displayName(self):
        return "Voxel Selection"

def _makeGUI(self):
    return PixelSelectToolboxGUI(self, self.method)

pixelselectiontoolbox.PixelSelectToolbox.makeGUI = _makeGUI

