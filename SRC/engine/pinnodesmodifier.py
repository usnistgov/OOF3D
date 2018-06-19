# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import registeredclass
from ooflib.common.IO import xmlmenudump
import ooflib.engine.coverage

class PinNodesModifier(registeredclass.RegisteredClass):
    registry = []

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PinNodeSelection(PinNodesModifier):
    def __call__(self, skelcontext):
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.pinSelection(
            skelcontext.nodeselection.currentSelectionTracker())

registeredclass.Registration(
    'Pin Node Selection',
    PinNodesModifier,
    PinNodeSelection,
    ordering=0,
    tip="Pin selected nodes.",
    discussion="""<para>
    <link linkend='MenuItem-OOF.Skeleton.PinNodes'>Pin</link> the
    currently <link
    linkend='MenuItem-OOF.NodeSelection'>selected</link> &nodes;.
    </para>""")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class UnPinNodeSelection(PinNodesModifier):
    def __call__(self, skelcontext):
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.unpinSelection(
            skelcontext.nodeselection.currentSelectionTracker())

registeredclass.Registration(
    'UnPin Node Selection',
    PinNodesModifier,
    UnPinNodeSelection,
    ordering=1,
    tip="Unpin selected nodes.",
    discussion="""<para>
    <link linkend='MenuItem-OOF.Skeleton.PinNodes'>Unpin</link> the
    currently <link
    linkend='MenuItem-OOF.NodeSelection'>selected</link> &nodes;.
    </para>""")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PinInternalBoundaryNodes(PinNodesModifier):
    def __call__(self, skelcontext):
        skel = skelcontext.getObject()
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.pinInternalBoundaryNodes(skel)

registeredclass.Registration(
    'Pin Internal Boundary Nodes',
    PinNodesModifier,
    PinInternalBoundaryNodes,
    ordering=2,
    tip="Pin all internal boundary nodes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/pininternal.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PinSelectedSegments(PinNodesModifier):
    def __call__(self, skelcontext):
        skelcontext.pinnednodes.start()
        skelcontext.pinnednodes.pinSelectedSegments(
            skelcontext.segmentselection.currentSelectionTracker())

registeredclass.Registration(
    'Pin Selected Segments',
    PinNodesModifier,
    PinSelectedSegments,
    ordering=4,
    tip="Pin nodes of selected segments.",
    discussion="""<para>
    <link linkend='MenuItem-OOF.Skeleton.PinNodes'>Pin</link> the
    &nodes; at the ends of the currently selected &sgmts; in the given
    &skel;.
    </para> """)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PinSelectedFaces(PinNodesModifier):
    def __init__(self, coverage):
        self.coverage = coverage
    def __call__(self, skelcontext):
        skel = skelcontext.getObject()
        skelcontext.pinnednodes.start()
        exterior = self.coverage == "Exterior" or self.coverage == "All"
        interior = self.coverage == "Interior" or self.coverage == "All"
        skelcontext.pinnednodes.pinSelectedFaces(
            skelcontext.faceselection.currentSelectionTracker(),
            skel, interior, exterior)
        
registeredclass.Registration(
    'Pin Selected Faces',
    PinNodesModifier,
    PinSelectedFaces,
    ordering=4.5,
    params=[
        enum.EnumParameter('coverage', ooflib.engine.coverage.Coverage)
    ],
    tip="Pin nodes of selected faces.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PinSelectedElements(PinNodesModifier):
    def __init__(self, coverage):
        self.coverage = coverage

    def __call__(self, skelcontext):
        skel = skelcontext.getObject()
        skelcontext.pinnednodes.start()
        exterior = self.coverage == "Exterior" or self.coverage == "All"
        interior = self.coverage == "Interior" or self.coverage == "All"
        skelcontext.pinnednodes.pinSelectedElements(
            skelcontext.elementselection.currentSelectionTracker(),
            skel, interior, exterior)

registeredclass.Registration(
    'Pin Selected Elements',
    PinNodesModifier,
    PinSelectedElements,
    ordering=5,
    params=[
        enum.EnumParameter('coverage', ooflib.engine.coverage.Coverage)
    ],
    tip="Pin nodes of selected elements.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/pinelements.xml'))
