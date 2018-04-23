# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# See NOTES/selection_machinery.txt.  

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import selectionoperators
from ooflib.common.IO import parameter
from ooflib.common.IO import pointparameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletonselectable

from ooflib.engine.skeletonselection import \
    NodeSelectionMethod, SegmentSelectionMethod, FaceSelectionMethod, \
    ElementSelectionMethod, \
    NodeSelectionMethodRegistration, SegmentSelectionMethodRegistration, \
    FaceSelectionMethodRegistration, ElementSelectionMethodRegistration

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Hack. We don't have selection couriers for skeleton selections yet,
# so using the SelectionOperators that are used for voxel selections
# isn't going to work.  But we'd like to make the interface for
# skeleton selections look just like the one for voxel selections, so
# this dict here maps the SelectionOperations to
# skeletonselection.Selection methods.  TODO: Once couriers are
# implemented, we should be able to adapt the SelectionOperator
# classes so that they can be used directly here, and get rid of
# _operatorDict and applyOperator.

_operatorDict = {
    # selectionoperators.Select : skeletonselectable.Selection.select,
    # selectionoperators.AddSelection : skeletonselectable.Selection.addSelect,
    # selectionoperators.Unselect : skeletonselectable.Selection.deselect,
    # selectionoperators.Toggle : skeletonselectable.Selection.toggle,
    # selectionoperators.Intersect : skeletonselectable.Selection.selectSelected
}

def applyOperator(operator, selection, selectees):
    # _operatorDict values are unbound methods of the Selection class,
    # so they need an explicit 'self' argument when they're called.
    _operatorDict[operator.__class__](selection, selectees)
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SingleNodeSelect(NodeSelectionMethod):
    def __init__(self, point, operator):
        self.point = point
        self.operator = operator
    def select(self, source, selection):
        # Calling nearestNode here seems to be repeating the work that
        # was already doen in findClickedPoint, but that's not
        # actually the case.  findClickedPoint works on a subgrid
        # consisting only of points beneath the mouse and doesn't use
        # the same vtkPoints as the skeleton, so it can't compute the
        # Node index.
        node = source.getObject().nearestNode(self.point)
        applyOperator(self.operator, selection, [node])
        
NodeSelectionMethodRegistration(
    'Single_Node',
    SingleNodeSelect,
    ordering=0,
    params=[
        parameter.passive(
            pointparameter.PointParameter('point')),
        selectionoperators.SelectionOperatorParam('operator', passive=1)],
    tip="Select a single node.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/single_node.xml'))


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Segment selection is like node selection, except for details.

class SingleSegmentSelect(SegmentSelectionMethod):
    def __init__(self, point, operator):
        self.point = point
        self.operator = operator
    def select(self, source, selection):
        segment = source.getObject().nearestSegment(self.point)
        applyOperator(self.operator, selection, [segment])

SegmentSelectionMethodRegistration(
    'Single_Segment',
    SingleSegmentSelect, ordering=0,
    params=[
        parameter.hidden(pointparameter.PointParameter('point')),
        selectionoperators.SelectionOperatorParam('operator', passive=1)],
    tip="Select a segment joining two nodes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/single_segment.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SingleFaceSelect(FaceSelectionMethod):
    def __init__(self, nodes, operator):
        self.nodes = nodes     
        self.operator = operator
    def select(self, source, selection):
        face = source.getObject().findExistingFaceByIds(self.nodes)
        applyOperator(self.operator, selection, [face])

FaceSelectionMethodRegistration(
    'Single_Face',
    SingleFaceSelect,
    ordering=0,
    params=[
        parameter.hidden(
            parameter.ListOfIntsParameter('nodes', tip="List of node IDs.")),
        selectionoperators.SelectionOperatorParam('operator', passive=1)],
    tip="Select a face joining three nodes.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/single_face.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SingleElementSelect(ElementSelectionMethod):
    def __init__(self, element, operator):
        self.element = element
        self.operator = operator
    def select(self, source, selection):
        el = source.getObject().getElement(self.element)
        applyOperator(self. operator, selection, [el])

ElementSelectionMethodRegistration(
    'Single_Element',
    SingleElementSelect,
    ordering=0,
    params=[
        parameter.hidden(
            parameter.IntParameter('element', tip="An element index.")),
        selectionoperators.SelectionOperatorParam('operator', passive=1)],
    tip="Select an element.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/single_element.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PixelElementSelect(ElementSelectionMethod):
    def select(self, skeletoncontext, gfxwindow, pointlist, view, selector):
        ms = skeletoncontext.getMicrostructure()
        if config.dimension() == 3:
            pt = gfxwindow.findClickedPosition(skeletoncontext, pointlist[0],
                                               view)
            if pt is None:
                selector([])
                return
            category = ms.category(ms.pixelFromPoint(pt))
        else:                   # 2D
            category = ms.category(pointlist[0])

        ## TODO OPT: There should be something like a
        ## SkeletonSelectionCourier so that large lists of elements
        ## don't have to be constructed here.
        reslist = []
        skel = skeletoncontext.getObject()
        for i in xrange(skel.nelements()):
            el = skel.getElement(i)
            if el.dominantPixel(skel) == category:
                reslist.append(el)
        selector(reslist)

ElementSelectionMethodRegistration(
    'ByDominantPixel',
    PixelElementSelect, ordering=4,
    events=['up'],
    tip=
    'Click on a pixel to select all elements with that type of dominant pixel.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/dominant_pixel.xml')
    )
