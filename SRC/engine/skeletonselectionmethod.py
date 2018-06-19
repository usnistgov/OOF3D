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
from ooflib.SWIG.engine import skeletonselectioncourier
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

class SingleNodeSelect(NodeSelectionMethod):
    def __init__(self, point, operator):
        self.point = point
        self.operator = operator
    def select(self, skelctxt, selection):
        # Calling nearestNode here seems to be repeating the work that
        # was already doen in findClickedPoint, but that's not
        # actually the case.  findClickedPoint works on a subgrid
        # consisting only of points beneath the mouse and doesn't use
        # the same vtkPoints as the skeleton, so it can't compute the
        # Node index.
        node = skelctxt.getObject().nearestNode(self.point)
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SingleObjectCourier(
            skelctxt.getObject(), node, clist, plist)
        self.operator.operate(selection, courier)
        
NodeSelectionMethodRegistration(
    'Single Node',
    SingleNodeSelect,
    ordering=0,
    params=[
        parameter.passive(pointparameter.PointParameter('point')),
        selectionoperators.SelectionOperatorParam('operator', passive=1)],
    tip="Select a single node.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/single_node.xml'))


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Segment selection is like node selection, except for details.

class SingleSegmentSelect(SegmentSelectionMethod):
    def __init__(self, nodes, operator):
        self.nodes = nodes
        self.operator = operator
    def select(self, skelctxt, selection):
        segment = skelctxt.getObject().findExistingSegmentByIds(self.nodes)
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SingleObjectCourier(
            skelctxt.getObject(), segment, clist, plist)
        self.operator.operate(selection, courier)

SegmentSelectionMethodRegistration(
    'Single Segment',
    SingleSegmentSelect, ordering=0,
    params=[
        parameter.hidden(
            parameter.ListOfIntsParameter('nodes', tip="List of node IDs.")),
        selectionoperators.SelectionOperatorParam('operator', passive=1)],
    tip="Select a segment joining two nodes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/single_segment.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SingleFaceSelect(FaceSelectionMethod):
    def __init__(self, nodes, operator):
        self.nodes = nodes     
        self.operator = operator
    def select(self, skelctxt, selection):
        face = skelctxt.getObject().findExistingFaceByIds(self.nodes)
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SingleObjectCourier(
            skelctxt.getObject(), face, clist, plist)
        self.operator.operate(selection, courier)

FaceSelectionMethodRegistration(
    'Single Face',
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
    def select(self, skelctxt, selection):
        el = skelctxt.getObject().getElement(self.element)
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.SingleObjectCourier(
            skelctxt.getObject(), el, clist, plist)
        self. operator.operate(selection, courier)

ElementSelectionMethodRegistration(
    'Single Element',
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
    def __init__(self, category, operator):
        self.category = category
        self.operator = operator
    def select(self, skelctxt, selection):
        clist, plist = selection.trackerlist()
        courier = skeletonselectioncourier.CategoryElementCourier(
            skelctxt.getObject(), self.category, clist, plist)
        self.operator.operate(selection, courier)

ElementSelectionMethodRegistration(
    'By Dominant Pixel',
    PixelElementSelect, ordering=4,
    params=[
        parameter.passive(
            parameter.IntParameter(
                'category',
                tip="Select elements whose dominant pixel is in this cateogory."
            )),
        selectionoperators.SelectionOperatorParam('operator', passive=1)
    ],
    events=['up'],
    whoclasses=['Microstructure', 'Image'],
    tip=
    'Click on a pixel to select all elements with that type of dominant pixel.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/dominant_pixel.xml')
    )
