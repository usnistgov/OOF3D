# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import labeltree
from ooflib.common.IO import genericselecttoolbox
from ooflib.common import toolbox
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.engine import skeletonselectionmethod
from ooflib.engine.IO import skeletonselectmenu
from ooflib.engine import skeletonselmodebase
from ooflib.engine import skeletonselectionmodes

class SkeletonSelectionToolboxBase(genericselecttoolbox.GenericSelectToolbox):
    def __init__(self, name, method, menu, gfxwindow, **extrakwargs):
        genericselecttoolbox.GenericSelectToolbox.__init__(
            self, name=name, method=method, menu=menu,
            gfxwindow=gfxwindow, **extrakwargs)
    def getSelectionSource(self):
        return self.gfxwindow().topwho('Skeleton')
    def sourceName(self):
        return "Skeleton"
    def emptyMessage(self):
        return "No Skeleton!"           # you spineless bastard

    discussion = "Methods for selecting &skel; components in a graphics window."

ordering = 2.5

skeletonselectionmodes.initialize()

for mode in skeletonselmodebase.SkeletonSelectionMode.modes:
    class SkeletonSelectionToolbox(SkeletonSelectionToolboxBase):
        def __init__(self, gfxwindow, selmode=mode):
            SkeletonSelectionToolboxBase.__init__(
                self,
                name=selmode.toolboxName(),
                method=selmode.methodclass,
                menu=selmode.getSelectionMenu(),
                mode=selmode,
                gfxwindow=gfxwindow)
    SkeletonSelectionToolbox.tip = "Select " + mode.name + "s in a Skeleton"
    mode.toolboxclass = SkeletonSelectionToolbox
    toolbox.registerToolboxClass(SkeletonSelectionToolbox, ordering=ordering)
    ordering += 0.01

# TODO?  Earlier versions allowed new toolbox modes to be added after
# initialization time via a switchboard signal sent from
# SkeletonSelectionMode.__init__.  Is that at all useful?
