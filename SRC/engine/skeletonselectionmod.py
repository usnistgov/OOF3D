# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import crandom
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import skeletonselectioncourier
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import selectionoperators
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelgroupparam
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import materialmanager
from ooflib.engine.IO import materialparameter
from ooflib.engine.IO import pbcparams
from ooflib.engine.IO import skeletongroupparams

import types
#Interface branch
from ooflib.engine.IO import interfaceparameters

import ooflib.engine.coverage

from ooflib.engine.skeletonselection import \
    NodeSelectionModifier, SegmentSelectionModifier, \
    FaceSelectionModifier, ElementSelectionModifier, \
    NodeSelectionModRegistration, SegmentSelectionModRegistration, \
    FaceSelectionModRegistration, ElementSelectionModRegistration
    

## TODO : Use couriers as in pixel selection.

## TODO 3.1: Add more face selection methods.  Select by aspect ratio?
## Area?

## TODO 3.1: Add Region selection methods, in the style of BoxSelection
## for voxels.

# TODO 3.1: Can the Segment/Element/Node/Face operations here all be
# derived from common SkeletonSelectable classes?

## TODO: None of these methods should call selection.start().  That's
## called in the menu item callback.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Ordering: The order in which the skeleton selection modifiers appear
# in the menus should be as similar as possible for the different
# selection modes.  The order is determined by the "ordering" arg in
# the registrations.

## TODO: These aren't used consistently below.  Make sure that all
## orderings use them.

# The group selection methods, Select Group, Unselect Group, Add
# Group, and Intersect Group, come first, in that order, with
# ordering=0.x, where x=1,2,3,4.
_selectGroupOrdering = 0.0
_unselectGroupOrdering = 0.1
_addGroupOrdering = 0.2
_intersectGroupOrdering=0.3

# The "Select from Selected Object" methods have ordering=1.x, where
# x is the dimension of the Object.
_selectFromNodesOrdering = 1.0
_selectFromSegmentsOrdering = 1.1
_selectFromFacesOrdering = 1.2
_selectFromElementsOrdering = 1.3

# Other selection methods have ordering >= 2.0
_homogeneityOrdering = 3.3
_internalBoundaryOrdering = 3.5
_namedBoundaryOrdering = 3.6
_interfaceOrdering = 3.7

_periodicPartnerOrdering = 8

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Node selection modifiers

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
    
class NodeFromSelectedSegments(NodeSelectionModifier):
    def __init__(self, operator):
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.NodesFromSegmentsCourier(
            skelctxt.getObject(),
            skelctxt.segmentselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

NodeSelectionModRegistration(
    'Select from Selected Segments',
    NodeFromSelectedSegments,
    ordering=_selectFromSegmentsOrdering,
    params = [
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select nodes from selected segments.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/nodes_from_segments.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class NodeFromSelectedElements(NodeSelectionModifier):
    def __init__(self, coverage, operator):
        self.coverage = coverage
        self.operator = operator

    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.NodesFromElementsCourier(
            skelctxt.getObject(),
            self.coverage,
            skelctxt.elementselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

NodeSelectionModRegistration(
    'Select from Selected Elements',
    NodeFromSelectedElements,
    ordering=_selectFromElementsOrdering,
    params = [
        enum.EnumParameter('coverage', ooflib.engine.coverage.Coverage),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select nodes from selected elements.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/nodes_from_elements.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class NodeFromSelectedFaces(NodeSelectionModifier):
    def __init__(self, coverage, operator):
        self.coverage = coverage
        self.operator = operator

    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.NodesFromFacesCourier(
            skelctxt.getObject(),
            self.coverage,
            skelctxt.faceselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

NodeSelectionModRegistration(
    'Select from Selected Faces',
    NodeFromSelectedFaces,
    ordering=_selectFromFacesOrdering,
    params = [
        enum.EnumParameter('coverage', ooflib.engine.coverage.Coverage),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select nodes from selected faces.")
    

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectInternalBoundaryNodes(NodeSelectionModifier):
    def __init__(self, operator, ignorePBC=False):
        self.operator = operator
        self.ignorePBC = ignorePBC
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.InternalBoundaryNodesCourier(
            skelctxt.getObject(), clist, plist)
        self.operator.operate(selection, courier)
        
if config.dimension() == 2:
    params=[
        selectionoperators.SelectionOperatorParam('operator'),
        pbcparams.PBCBooleanParameter('ignorePBC', False,
                                          tip='Ignore periodicity?')]
else:
    params = [selectionoperators.SelectionOperatorParam('operator')]

NodeSelectionModRegistration(
    'Select Internal Boundaries',
    SelectInternalBoundaryNodes,
    ordering=_internalBoundaryOrdering,
    params=params,
    tip="Select all nodes on material or group boundaries.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/boundary_nodes.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectNamedBoundaryNodes(NodeSelectionModifier):
    def __init__(self, boundary, operator):
        self.boundary = boundary
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        bdy = skelctxt.getBoundary(self.boundary)
        courier = skeletonselectioncourier.PointBoundaryCourier(
            skelctxt.getObject(), bdy.getBoundarySet(skelctxt.getObject()),
            clist, plist)
        self.operator.operate(selection, courier)

NodeSelectionModRegistration(
    'Select Named Boundary',
    SelectNamedBoundaryNodes,
    ordering=_namedBoundaryOrdering,
    params=[
        skeletongroupparams.SkeletonPointBoundaryParameter(
            'boundary', tip="Select nodes in this boundary"),
        selectionoperators.SelectionOperatorParam('operator')
        ],
    tip="Select nodes belonging to the given skeleton point boundary.",
    discussion="""<para>

    Select all the &nodes; contained in the given &skel;
    <link linkend="Section-Concepts-Skeleton-Boundary">boundary</link>.
    The boundary must be a
    <link linkend="Section-Concepts-Skeleton-Boundary-Point">point</link>
    boundary.
    
    </para>"""
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectPeriodicPartnerNodes(NodeSelectionModifier):
    def select(self, skeleton, selection):
        oldnodes = skeleton.nodeselection.retrieve()
        newnodes = set()
        for node in oldnodes:
            for p in node.getPartners():
                newnodes.add(p)
        selection.start()
        selection.select(newnodes)

registeredclass.TwoDOnlyRegistration(
    'Select Periodic Partners',
    SelectPeriodicPartnerNodes,
    ordering=_periodicPartnerOrdering,
    tip="Select nodes whose periodic partners are already selected.",
    discussion="""<para>

    If the &skel; is <link
    linkend="Section-Concepts-Skeleton-Periodicity">periodic</link>,
    every &node; on a periodic boundary has a partner on the
    opposite boundary.  This command selects the periodic partners
    of the currently selected &nodes;, without unselecting any
    &nodes;.

    </para>"""
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Since we only have tetrahedral elements in 3D, there's no
## difference between expanding by shared elements, segments, or
## faces.  TODO 3.1: If we ever add non-tetrahedral elements, this
## should be rewritten to look like ExpandElementSelection.

class ExpandNodeSelection(NodeSelectionModifier):
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.ExpandNodeSelectionCourier(
            skelctxt.getObject(),
            skelctxt.nodeselection.currentSelectionTracker(),
            clist, plist);
        selection.select(courier)

NodeSelectionModRegistration(
    'Expand',
    ExpandNodeSelection,
    ordering=2.0,
    tip="Select the neighbors of selected Nodes.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Select the indicated group.

class NodeSelectGroup(NodeSelectionModifier):
    def __init__(self, group, operator):
        self.group = group
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SkeletonGroupCourier(
            skelctxt.getObject(),
            self.group,
            skelctxt.nodegroups.getTracker(skelctxt.getObject()),
            clist, plist)
        self.operator.operate(selection, courier)
        

NodeSelectionModRegistration(
    'Select Group',
    NodeSelectGroup,
    ordering=_selectGroupOrdering,
    params=[
        skeletongroupparams.NodeGroupParameter('group',
                                               tip="Node group to select."),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip='Select the members of a group.',
    discussion="""<para>
    Select all the &nodes; in the given <link
    linkend='Section-Concepts-Skeleton-Groups'>group</link>..
    </para>""")


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#      Segment Selection Modifiers
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#


class SegFromSelectedElements(SegmentSelectionModifier):
    def __init__(self, coverage, operator):
        self.coverage = coverage
        self.operator = operator

    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SegmentsFromElementsCourier(
            skelctxt.getObject(),
            self.coverage,
            skelctxt.elementselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionModRegistration(
    'Select from Selected Elements',
    SegFromSelectedElements,
    ordering=_selectFromElementsOrdering,
    params = [
        enum.EnumParameter("coverage", ooflib.engine.coverage.Coverage),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select segments from selected elements.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/segments_from_elements.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SegFromSelectedNodes(SegmentSelectionModifier):
    def __init__(self, one, two, operator):
        self.one = one
        self.two = two
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SegmentsFromNodesCourier(
            skelctxt.getObject(),
            self.one, self.two,
            skelctxt.nodeselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionModRegistration(
    "Select from Selected Nodes",
    SegFromSelectedNodes,
    params=[
        parameter.BooleanParameter(
            'one', value=True,
            tip='Select segments with one selected node.'),
        parameter.BooleanParameter(
            'two', value=True,
            tip='Select segments with two selected nodes.'),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    ordering=_selectFromNodesOrdering,
    tip="Select segments from the selected nodes.")
        
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SegFromSelectedFaces(SegmentSelectionModifier):
    def __init__(self, coverage, operator):
        self.coverage = coverage
        self.operator = operator

    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SegmentsFromFacesCourier(
            skelctxt.getObject(),
            self.coverage,
            skelctxt.faceselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionModRegistration(
    'Select from Selected Faces',
    SegFromSelectedFaces,
    ordering=_selectFromFacesOrdering,
    params=[
        enum.EnumParameter('coverage', ooflib.engine.coverage.Coverage),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select the edges of the selected faces.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectInternalBoundarySegments(SegmentSelectionModifier):
    def __init__(self, operator):
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.InternalBoundarySegmentsCourier(
            skelctxt.getObject(), clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionModRegistration(
    'Select Internal Boundaries',
    SelectInternalBoundarySegments,
    params=[selectionoperators.SelectionOperatorParam('operator')],
    ordering=_internalBoundaryOrdering,
    tip="Select segments on material or group boundaries.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

#Interface branch
class SelectInterfaceSegments(SegmentSelectionModifier):
    def __init__(self, interface):
        self.interface = interface
    def select(self, skeleton, selection):
        skel = skeleton.getObject()
        interfacemsplugin=skel.getMicrostructure().getPlugIn("Interfaces")
        try:
            interfacedef=interfacemsplugin.namedinterfaces[self.interface]
        except KeyError:
            #Should not happen
            raise ooferror.ErrPyProgrammingError("Interface not found!")
        seglist = []
        for segment in skel.segments.values():
            yes,side1elem=interfacedef.isInterfaceSegment(segment,skel)
            if yes:
                seglist.append(segment)
        selection.start()
        selection.clear()
        selection.select(seglist)

if config.dimension() == 2:
    SegmentSelectionModRegistration(
        'Select Interface Segments',
        SegmentSelectionModifier,
        SelectInterfaceSegments,
        ordering=_interfaceOrdering,
        params=[
        interfaceparameters.InterfacesParameter(
                'interface',
                tip='Select segments in this interface.')],
        tip="Select segments from an interface definition.",
        discussion="""<para>
        Select all the &sgmts; that belong to the given interface definition.
        </para>"""
        )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectNamedBoundarySegments(SegmentSelectionModifier):
    def __init__(self, boundary, operator):
        self.boundary = boundary
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        bdy = skelctxt.getBoundary(self.boundary) # A SkelContextEdgeBoundary
        courier = skeletonselectioncourier.EdgeBoundaryCourier(
            skelctxt.getObject(),
            bdy.getBoundarySet(skelctxt.getObject()),
            clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionModRegistration(
    'Select Named Boundary',
    SelectNamedBoundarySegments,
    ordering=_namedBoundaryOrdering,
    params=[
        skeletongroupparams.SkeletonEdgeBoundaryParameter(
            'boundary',
            tip="Select segments in this boundary"),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select segments belonging to the given skeleton edge boundary.",
    discussion="""<para>

    Select all the &sgmts; contained in the given &skel;
    <link linkend="Section-Concepts-Skeleton-Boundary">boundary</link>.
    The boundary must be a
    <link linkend="Section-Concepts-Skeleton-Boundary-Edge">edge</link>
    boundary.

    </para>"""
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectPeriodicPartnerSegments(SegmentSelectionModifier):
    def select(self, skeleton, selection):
        oldsegs = skeleton.segmentselection.retrieve()
        newsegs = set()
        skel = skeleton.getObject()
        for seg in oldsegs:
            partner = seg.getPartner(skel)
            if partner:
                newsegs.add(partner)
        selection.start()
        selection.select(newsegs)

registeredclass.TwoDOnlyRegistration(
    'Select Periodic Partners',
    SegmentSelectionModifier,
    SelectPeriodicPartnerSegments,
    ordering=8,
    tip="Select the periodic partners of the currently selected Segments.",
    discussion="""<para>

    If the &skel; is <link
    linkend="Section-Concepts-Skeleton-Periodicity">periodic</link>,
    every &sgmt; on a periodic boundary has a partner on the opposite
    boundary.  This command selects the periodic partners of the
    currently selected &sgmts;, without unselecting any &sgmts;.

        </para>"""
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SegmentHomogeneity(SegmentSelectionModifier):
    def __init__(self, threshold, operator):
        self.threshold = threshold
        self.operator = operator

    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.InhomogeneousSegmentCourier(
            skelctxt.getObject(), self.threshold, clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionModRegistration(
    'Select by Homogeneity',
    SegmentHomogeneity,
    ordering=_homogeneityOrdering,
    params = [parameter.FloatRangeParameter('threshold', (0.0, 1.0, 0.01),
                                            value=0.9,
                                            tip='The threshold homogeneity.'),
              selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select segments with homogeneity less than the given threshold.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/hetero_segments.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class RandomSegments(SegmentSelectionModifier):
    def __init__(self, probability, operator):
        self.probability = probability
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.RandomSegmentCourier(
            skelctxt.getObject(), self.probability, clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionModRegistration(
    'Select Randomly',
    RandomSegments,
    ordering=100,
    params = [
        parameter.FloatRangeParameter(
            'probability', (0.0, 1.0, 0.01),
            value=0.5,
            tip='The probability of selecting a segment.'),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select segments randomly.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Select the indicated group.
class SegmentSelectGroup(SegmentSelectionModifier):
    def __init__(self, group, operator):
        self.group = group
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SkeletonGroupCourier(
            skelctxt.getObject(),
            self.group,
            skelctxt.segmentgroups.getTracker(skelctxt.getObject()),
            clist, plist)
        self.operator.operate(selection, courier)
        
SegmentSelectionModRegistration(
    'Select Group',
    SegmentSelectGroup,
    ordering=_selectGroupOrdering,
    params=[
        skeletongroupparams.SegmentGroupParameter('group',
                                                  tip="Name of the group"),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip='Select the members of a group.',
    discussion="""<para>
    Select all of the &sgmts; in the given <link
    linkend='Section-Concepts-Skeleton-Groups'>group</link>.
    </para>"""
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#       Face Selection Modifiers
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#



# TODO 3.1: add more face selection modifiers.

class SelectInternalBoundaryFaces(FaceSelectionModifier):
    def __init__(self, operator):
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.InternalBoundaryFacesCourier(
            skelctxt.getObject(), clist, plist)
        self.operator.operate(selection, courier)

FaceSelectionModRegistration(
    'Select Internal Boundaries',
    SelectInternalBoundaryFaces,
    params=[selectionoperators.SelectionOperatorParam('operator')],
    ordering=_internalBoundaryOrdering,
    tip="Select faces on material or group boundaries.")
                

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectNamedBoundaryFaces(FaceSelectionModifier):
    def __init__(self, boundary, operator):
        self.boundary = boundary
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        bdy = skelctxt.getBoundary(self.boundary)
        courier = skeletonselectioncourier.FaceBoundaryCourier(
            skelctxt.getObject(),
            bdy.getBoundarySet(skelctxt.getObject()),
            clist, plist)
        self.operator.operate(selection, courier)

FaceSelectionModRegistration(
    'Select Named Boundary',
    SelectNamedBoundaryFaces,
    ordering=_namedBoundaryOrdering,
    params=[
        skeletongroupparams.SkeletonFaceBoundaryParameter(
            'boundary', tip='Select faces in this boundary'),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip='Select faces belonging to the given skeleton face boundary.')


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FaceSelectGroup(FaceSelectionModifier):
    def __init__(self, group, operator):
        self.group = group
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SkeletonGroupCourier(
            skelctxt.getObject(),
            self.group,
            skelctxt.segmentgroups.getTracker(skelctxt.getObject()),
            clist, plist)
        self.operator.operate(selection, courier)

FaceSelectionModRegistration(
    'Select Group',
    FaceSelectGroup,
    ordering=_selectGroupOrdering,
    params=[
        skeletongroupparams.FaceGroupParameter('group',
                                               tip="Face group to select."),
        selectionoperators.SelectionOperatorParam('operator')
        ],
    tip="Select the members of a group, discarding the current selection."
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FaceFromSelectedElements(FaceSelectionModifier):
    def __init__(self, coverage, operator):
        self.coverage = coverage
        self.operator = operator

    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.FacesFromElementsCourier(
            skelctxt.getObject(),
            self.coverage,
            skelctxt.elementselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)
    
FaceSelectionModRegistration(
    'Select from Selected Elements',
    FaceFromSelectedElements,
    ordering=_selectFromElementsOrdering,
    params = [
        enum.EnumParameter('coverage', ooflib.engine.coverage.Coverage),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select the faces of the selected elements.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FaceFromSelectedNodes(FaceSelectionModifier):
    def __init__(self, min_nodes, operator):
        self.min_nodes = min_nodes
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.FacesFromNodesCourier(
            skelctxt.getObject(),
            self.min_nodes,
            skelctxt.nodeselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

FaceSelectionModRegistration(
    'Select from Selected Nodes',
    FaceFromSelectedNodes,
    params=[
        parameter.IntRangeParameter(
            'min_nodes', (1, 3), value=1,
            tip="Select faces with at least this many selected nodes."),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    ordering=_selectFromNodesOrdering,
    tip="Select every face containing selected nodes.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FaceFromSelectedSegments(FaceSelectionModifier):
    def __init__(self, min_segments, operator):
        self.min_segments = min_segments
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.FacesFromSegmentsCourier(
            skelctxt.getObject(),
            self.min_segments,
            skelctxt.segmentselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)

FaceSelectionModRegistration(
    'Select from Selected Segments',
    FaceFromSelectedSegments,
    params=[
        parameter.IntRangeParameter(
            'min_segments', (1,3), value=1,
            tip="Select faces with at least this many selected segments."),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    ordering=_selectFromSegmentsOrdering,
    tip="Select every face adjacent to a selected segment.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ByElementMaterial(ElementSelectionModifier):
    def __init__(self, material, operator):
        self.material = material
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        if self.material == '<Any>':
            courier = skeletonselectioncourier.AnyMaterialElementCourier(
                skelctxt.getObject(),
                clist, plist)
        elif self.material == '<None>':
            courier = skeletonselectioncourier.NoMaterialElementCourier(
                skelctxt.getObject(),
                clist, plist)
        else:
            courier = skeletonselectioncourier.MaterialElementCourier(
                skelctxt.getObject(),
                materialmanager.getMaterial(self.material),
                clist, plist)
        self.operator.operate(selection, courier)

ElementSelectionModRegistration(
    'Select by Material',
    ByElementMaterial,
    ordering=2.2,
    params=[
        materialparameter.AnyMaterialParameter(
            'material', tip="Select elements with this material."),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select all Elements with a given Material.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/menu/bymaterial.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementHomogeneity(ElementSelectionModifier):
    def __init__(self, min_homogeneity, max_homogeneity, operator):
        self.min_homogeneity = min_homogeneity
        self.max_homogeneity = max_homogeneity
        self.operator = operator

    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.ElementHomogeneityCourier(
            skelctxt.getObject(),
            self.min_homogeneity, self.max_homogeneity,
            clist, plist)
        self.operator.operate(selection, courier)

ElementSelectionModRegistration(
    'Select by Homogeneity',
    ElementHomogeneity,
    ordering=2.3,
    params = [
        parameter.FloatRangeParameter(
            'min_homogeneity', (0.0, 1.0, 0.01), value=0.0,
            tip='Select elements with homogeneity greater than this.'),
        parameter.FloatRangeParameter(
            'max_homogeneity', (0.0, 1.0, 0.01), value=1.0,
            tip='Select elements with homogeneity less than this.'),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select Elements with homogeneity in a given range.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/hetero_elements.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementShapeEnergy(ElementSelectionModifier):
    def __init__(self, min_energy, max_energy, operator):
        self.min_energy = min_energy
        self.max_energy = max_energy
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.ElementShapeEnergyCourier(
            skelctxt.getObject(),
            self.min_energy, self.max_energy,
            clist, plist)
        self.operator.operate(selection, courier)

ElementSelectionModRegistration(
    'Select by Shape Energy',
    ElementShapeEnergy,
    ordering=2.4,
    params = [
        parameter.FloatRangeParameter(
            'min_energy', (0.0, 1.0, 0.01), value=0.0,
            tip='Select Elements with shape-energy greater than this.'),
        parameter.FloatRangeParameter(
            'max_energy', (0.0, 1.0, 0.01), value=1.0,
            tip='Select Elements with shape-energy less than this.'),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select elements by shape-energy."
    " The greater the shape-energy the uglier the element.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/element_by_shape.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementIllegal(ElementSelectionModifier):
    def __init__(self, operator):
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.IllegalElementCourier(
            skelctxt.getObject(), clist, plist)
        self.operator.operate(selection, courier)

ElementSelectionModRegistration(
    'Select Illegal Elements',
    ElementIllegal,
    ordering=2.5,
    params=[selectionoperators.SelectionOperatorParam('operator')],
    tip="Select illegal elements.",
    discussion="""  <para>
    <command>Select_Illegal_Elements</command> selects all of the
    <link
    linkend="Section-Concepts-Skeleton-Illegality">illegal</link>
    &elems; in the given &skel;.  Illegal &elems; are hard to create,
    but if they have been created somehow, this command can be useful
    in eradicating them.
    </para>""")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementSuspect(ElementSelectionModifier):
    def __init__(self, operator):
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SuspectElementCourier(
            skelctxt.getObject(), clist, plist)
        self.operator.operate(selection, courier)

# TODO 3.1: need link for suspect elements concept
ElementSelectionModRegistration(
    'Select Suspect Elements',
    ElementSuspect,
    ordering=2.6,
    params=[selectionoperators.SelectionOperatorParam('operator')],
    tip="Select suspect elements.",
    discussion="""  <para>
    <command>Select_Suspect_Elements</command> selects all of the
    <link
    linkend="Section-Concepts-Skeleton-Suspect">suspect</link>
    &elems; in the given &skel;.
    </para>""")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementFromSelectedNodes(ElementSelectionModifier):
    def __init__(self, min_nodes, operator):
        self.min_nodes = min_nodes
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.ElementsFromNodesCourier(
            skelctxt.getObject(),
            self.min_nodes,
            skelctxt.nodeselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)
            
ElementSelectionModRegistration(
    'Select from Selected Nodes',
    ElementFromSelectedNodes,
    ordering=_selectFromNodesOrdering,
    params=[
        parameter.IntRangeParameter(
            'min_nodes', (1,4), value=1,
            tip='Select elements with at least this many selected nodes.'),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip="Select elements containing a minimum number of selected nodes.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/elements_from_nodes.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementFromSelectedSegments(ElementSelectionModifier):
    def __init__(self, min_segments, operator):
        self.min_segments = min_segments
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.ElementsFromSegmentsCourier(
            skelctxt.getObject(),
            self.min_segments,
            skelctxt.segmentselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)
        
ElementSelectionModRegistration(
    'Select from Selected Segments',
    ElementFromSelectedSegments,
    ordering=_selectFromSegmentsOrdering,
    params=[
        parameter.IntRangeParameter(
            'min_segments', (1,6), value=1,
            tip="Select elements with at least this many selected segments."),
        selectionoperators.SelectionOperatorParam('operator')
        ],
    tip="Select elements with a minimum number of selected segments.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/menu/elements_from_segments.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementFromSelectedFaces(ElementSelectionModifier):
    def __init__(self, min_faces, operator):
        self.min_faces = min_faces
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.ElementsFromFacesCourier(
            skelctxt.getObject(),
            self.min_faces,
            skelctxt.faceselection.currentSelectionTracker(),
            clist, plist)
        self.operator.operate(selection, courier)
        
ElementSelectionModRegistration(
    'Select from Selected Faces',
    ElementFromSelectedFaces,
    params=[
        parameter.IntRangeParameter(
            'min_faces', (1,4), value=1,
            tip="Select elements with at least this many selected faces."),
        selectionoperators.SelectionOperatorParam('operator')
        ],
    ordering=_selectFromFacesOrdering,
    tip='Select every element adjacent to selected faces.')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementSelectionExpansionMode(enum.EnumClass(
        ("Faces",
         "Select Elements that share a Face with a selected Element."),
        ("Segments",
         "Select Elements that share a Segment with a selected Element."),
        ("Nodes", 
         "Select Elements that share a Node with a selected Element."))):
    tip="How to choose the neighboring Elements."

class ExpandElementSelection(ElementSelectionModifier):
    def __init__(self, mode):
        self.mode = mode
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.ExpandElementSelectionCourier(
            skelctxt.getObject(),
            self.mode,
            skelctxt.elementselection.currentSelectionTracker(),
            clist, plist)
        selection.select(courier)
    
ElementSelectionModRegistration(
    'Expand',
    ExpandElementSelection,
    ordering=2.0,
    params=[
        enum.EnumParameter(
            'mode', ElementSelectionExpansionMode,
            ElementSelectionExpansionMode("Faces"),
            tip="How to choose neighboring Elements")],
    tip="Select the neighbors of the selected Elements.")


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Select the indicated group.

class ElementSelectGroup(ElementSelectionModifier):
    def __init__(self, group, operator):
        self.group = group
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SkeletonGroupCourier(
            skelctxt.getObject(),
            self.group,
            skelctxt.elementgroups.getTracker(skelctxt.getObject()),
            clist, plist)
        self.operator.operate(selection, courier)

ElementSelectionModRegistration(
    'Select Group',
    ElementSelectGroup,
    ordering=_selectGroupOrdering,
    params=[
        skeletongroupparams.ElementGroupParameter('group',
                                                  tip="Name of the group."),
        selectionoperators.SelectionOperatorParam('operator')
    ],
    tip='Select the members of a group, discarding the current selection.',
    discussion="""<para>
    Select all the &elems; in the given <link
    linkend='Section-Concepts-Skeleton-Groups'>group</link>.
    </para>""")


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementByPixelGroup(ElementSelectionModifier):
    def __init__(self, group):
        self.group = group
    def select(self, skeleton, selection):
        selected = []
        ms = skeleton.getMicrostructure()
        skel = skeleton.getObject()
        pxlgrp = ms.findGroup(self.group)
        for i in xrange(skel.nelements()):
            grpnames = pixelgroup.pixelGroupNames(
                ms, skel.getElement(i).dominantPixel(skel))
            if self.group in grpnames:
                selected.append(skel.getElement(i))
        selection.start()
        selection.clear()
        selection.select(selected)

ElementSelectionModRegistration(
    'Select by Pixel Group',
    ElementByPixelGroup,
    ordering=2.1,
    params=[pixelgroupparam.PixelGroupParameter(
            'group', tip='The name of a pixel group.')],
    tip="Select all Elements whose dominant pixel is in a given pixel group.",
    discussion="""<para>
    This command selects all &skel; &elems; whose
    <link linkend="Section-Concepts-Skeleton-Homogeneity">dominant pixel</link>
    is a member of the given &pixelgroup;.
   </para>""")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
