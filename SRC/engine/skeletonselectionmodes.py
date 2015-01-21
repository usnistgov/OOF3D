# -*- python -*-
# $RCSfile: skeletonselectionmodes.py,v $
# $Revision: 1.7.2.4 $
# $Author: langer $
# $Date: 2013/02/27 16:18:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common.IO import mainmenu
from ooflib.engine import skeletonselmodebase
from ooflib.engine import skeletonselectionmethod
from ooflib.engine import skeletonselectionmod
from ooflib.engine.IO import skeletongroupmenu
from ooflib.SWIG.engine import material

# Subclasses and singleton instances of SkeletonSelectionMode.  See
# comments in skeletonselmodebase.py.

class ElementSelectionMode(skeletonselmodebase.SkeletonSelectionMode):
    def __init__(self):
        skeletonselmodebase.SkeletonSelectionMode.__init__(
            self,
            name="Element",
            methodclass=skeletonselectionmethod.ElementSelectMethod,
            modifierclass=skeletonselectionmod.ElementSelectionModifier,
            modifierappliedsignal="element selection modified",
            newselectionsignal="new element selection",
            changedselectionsignal="changed element selection",
            groupmenu=skeletongroupmenu.elementgroupmenu,
            materialsallowed = material.MATERIALTYPE_BULK)
    def getSelectionContext(self, skeletoncontext):
        ## Called by SkeletonContext.getSelectionContext()
        return skeletoncontext.elementselection
    def getSelectionMenu(self):
        return mainmenu.OOF.ElementSelection
    def getGroups(self, skeletoncontext):
        return skeletoncontext.elementgroups
    def getGroupMenu(self):
        return skeletongroupmenu.elementgroupmenu


class NodeSelectionMode(skeletonselmodebase.SkeletonSelectionMode):
    def __init__(self):
        skeletonselmodebase.SkeletonSelectionMode.__init__(
            self,
            name="Node",
            methodclass=skeletonselectionmethod.NodeSelectMethod,
            modifierclass=skeletonselectionmod.NodeSelectionModifier,
            modifierappliedsignal="node selection modified",
            newselectionsignal="new node selection",
            changedselectionsignal="changed node selection",
            groupmenu=skeletongroupmenu.nodegroupmenu)
    def getSelectionContext(self, skeletoncontext):
        return skeletoncontext.nodeselection
    def getSelectionMenu(self):
        return mainmenu.OOF.NodeSelection
    def getGroups(self, skeletoncontext):
        return skeletoncontext.nodegroups
    def getGroupMenu(self):
        return skeletongroupmenu.nodegroupmenu

class SegmentSelectionMode(skeletonselmodebase.SkeletonSelectionMode):
    def __init__(self):
        skeletonselmodebase.SkeletonSelectionMode.__init__(
            self,
            name="Segment",
            methodclass=skeletonselectionmethod.SegmentSelectMethod,
            modifierclass=skeletonselectionmod.SegmentSelectionModifier,
            modifierappliedsignal="segment selection modified",
            newselectionsignal="new segment selection",
            changedselectionsignal="changed segment selection",
            groupmenu=skeletongroupmenu.segmentgroupmenu,
            ## Materials are *not* allowed to be assigned directly to
            ## segments, because segments aren't directed. Materials
            ## are assigned instead to boundaries.
            # materialsallowed=material.MATERIALTYPE_INTERFACE
            )
    def getSelectionContext(self, skeletoncontext):
        return skeletoncontext.segmentselection
    def getSelectionMenu(self):
        return mainmenu.OOF.SegmentSelection
    def getGroups(self, skeletoncontext):
        return skeletoncontext.segmentgroups
    def getGroupMenu(self):
        return skeletongroupmenu.segmentgroupmenu

if config.dimension() == 3:
    class FaceSelectionMode(skeletonselmodebase.SkeletonSelectionMode):
        def __init__(self):
            skeletonselmodebase.SkeletonSelectionMode.__init__(
                self,
                name="Face",
                methodclass=skeletonselectionmethod.FaceSelectMethod,
                modifierclass=skeletonselectionmod.FaceSelectionModifier,
                modifierappliedsignal="face selection modified",
                newselectionsignal="new face selection",
                changedselectionsignal="changed face selection",
                groupmenu=skeletongroupmenu.facegroupmenu)
        def getSelectionContext(self, skeletoncontext):
            return skeletoncontext.faceselection
        def getSelectionMenu(self):
            return mainmenu.OOF.FaceSelection
        def getGroups(self, skeletoncontext):
            return skeletoncontext.facegroups
        def getGroupMenu(self):
            return skeletongroupmenu.facegroupmenu

# Modes appear in the GUI in the order in which they're constructed
# here (for example, in the radio buttons at the top of the Skeleton
# Selection and Skeleton Info toolboxes). The order is chosen to be
# "Element", "Face", "Segment", "Node" in order of decreasing
# dimensionality.  Fortuitously, in 3D this order makes the labels in
# each column of the table of buttons in the gfxwindow toolbox have
# nearly the same size, thereby minimizing the width of the table.

ElementSelectionMode()
FaceSelectionMode()
SegmentSelectionMode()
NodeSelectionMode()


