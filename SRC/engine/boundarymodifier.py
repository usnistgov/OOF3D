# -*- python -*-
# $RCSfile: boundarymodifier.py,v $
# $Revision: 1.16.10.12 $
# $Author: langer $
# $Date: 2014/08/20 02:21:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file defines registered class objects which modify boundaries.

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletonboundary
from ooflib.engine.IO import skeletongroupparams

# Classes for adding or removing points, segments, or faces from a
# skeleton boundary.  Each modifier's registration must have a
# "targets" datum, which is a tuple of the boundary classes to which
# the modifier applies.

## TODO 3.1: RemoveFaces and RemoveSegments don't check that the
## resulting boundaries are nonempty and simply connected.  The GUI
## does check, and prevents the modifiers from being applied, but
## scripted commands don't have any checking.  They should, because
## subsequent operations on improperly formed boundaries might fail.
## (Changed from 3.0 to 3.1 because OOF2 doesn't check either, so it's
## apparently not a crucial issue.  The same problem presumably exists
## for AddFaces and AddSegments.)

class BoundaryModifier(registeredclass.RegisteredClass):
    registry = []
    tip = "Tools to modify Skeleton boundaries."
    discussion = """<para>
    <classname>BoundaryModifiers</classname> are used as the
    <varname>modifier</varname> parameter in <xref
    linkend='MenuItem:OOF.Skeleton.Boundary.Modify'/>.  They make
    changes in a &skel; <link
    linkend='Section-Concepts-Skeleton-Boundary'>boundary</link>.
    </para>"""

    def __call__(self, skelcontext, boundary):
        self.apply(skelcontext, boundary)
        switchboard.notify("new boundary configuration", skelcontext)
        switchboard.notify("redraw")

# Special parameter so we can have a special widget.
class BoundaryModifierParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.RegisteredParameter.__init__(
            self, name, BoundaryModifier, value=value,
            default=default, tip=tip, auxData=auxData)

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

# Special parameter class, so we can have a context-aware widget which
# will only be valid for legal operations.
class BdyModSegmentAggregateParameter(
    skeletongroupparams.SegmentAggregateParameter):
    pass

# Modifier that adds selected segments (from a group or selection) to
# the indicated boundary.  Obviously this will fail if the boundary is
# not an edge boundary.
class AddSegments(BoundaryModifier):
    def __init__(self, group):
        self.group = group
        
    def attempt(self, skelcontext, boundary):
        ## TODO OPT: Do this without creating a Python list of segments.
        seg_set = skelcontext.segments_from_seg_aggregate(self.group)
        return skelcontext.try_appendSegsToBdy(boundary, seg_set)
        
    def apply(self, skelcontext, boundary):
        ## TODO OPT: Do this without creating a Python list of segments.
        seg_set = skelcontext.segments_from_seg_aggregate(self.group)
        skelcontext.appendSegsToBdy(boundary, seg_set)

registeredclass.Registration(
    "Add segments",
    BoundaryModifier,
    AddSegments,
    ordering=200,
    params=[BdyModSegmentAggregateParameter(
        'group', tip="The segments to add to the boundary.")],
    targets=(skeletonboundary.SkelContextEdgeBoundary,),
    tip="Add a set of segments to an existing edge boundary.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/add_segments.xml'))


class RemoveSegments(BoundaryModifier):
    def __init__(self, group):
        self.group = group

    def attempt(self, skelcontext, boundary):
        seg_set = skelcontext.segments_from_seg_aggregate(self.group)
        return skelcontext.try_removeSegsFromBdy(boundary, seg_set)
        
    def apply(self, skelcontext, boundary):
        seg_set = skelcontext.segments_from_seg_aggregate(self.group)
        skelcontext.removeSegsFromBdy(boundary, seg_set)

registeredclass.Registration(
    "Remove segments",
    BoundaryModifier,
    RemoveSegments,
    ordering=201,
    targets=(skeletonboundary.SkelContextEdgeBoundary,),
    params=[BdyModSegmentAggregateParameter(
        'group', tip="The segments to remove from the boundary.")],
    tip="Remove a set of segments from an existing boundary.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/remove_segments.xml')
    )

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## # 
 
# Modifier for adding nodes from a group or the selection to a point boundary.
class AddNodes(BoundaryModifier):
    def __init__(self, group):
        self.group = group
    def apply(self, skelcontext, boundary):
        skelobj = skelcontext.getObject()
        node_set = skelcontext.nodes_from_node_aggregate(self.group)
        skelcontext.addNodesToBdy(boundary, node_set)

registeredclass.Registration(
    "Add nodes",
    BoundaryModifier,
    AddNodes,
    ordering=302,
    targets=(skeletonboundary.SkelContextPointBoundary,),
    params=[skeletongroupparams.NodeAggregateParameter(
        'group', tip="The nodes to add to the boundary.")],
    tip="Add a set of nodes to an existing point boundary.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/add_nodes.xml')
    )

class RemoveNodes(BoundaryModifier):
    def __init__(self, group):
        self.group = group
    def apply(self, skelcontext, boundary):
        node_set = skelcontext.nodes_from_node_aggregate(self.group)
        skelcontext.removeNodesfromBdy(boundary, node_set)

registeredclass.Registration(
    "Remove nodes",
    BoundaryModifier,
    RemoveNodes,
    ordering=303,
    targets=(skeletonboundary.SkelContextPointBoundary,),
    params=[skeletongroupparams.NodeAggregateParameter(
        'group', tip="The nodes to remove from the boundary")],
    tip="Remove a set of nodes from an existing point boundary.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/remove_nodes.xml')
    )

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

# Special parameter class, so that we can have a context-aware widget
# which will only be valid for legal operations.
class BdyModFaceAggregateParameter(skeletongroupparams.FaceAggregateParameter):
    pass

class AddFaces(BoundaryModifier):
    def __init__(self, group):
        self.group = group

    def attempt(self, skelcontext, boundary):
        ## TODO OPT: Do this without creating a Python list of faces.
        faces = skelcontext.faces_from_face_aggregate(self.group)
        return skelcontext.try_appendFacesToBdy(boundary, faces)

    def apply(self, skelcontext, boundary):
        ## TODO OPT: Do this without creating a Python list of faces.
        faces = skelcontext.faces_from_face_aggregate(self.group)
        skelcontext.appendFacesToBdy(boundary, faces)
                             
registeredclass.ThreeDOnlyRegistration(
    "Add faces",
    BoundaryModifier,
    AddFaces,
    ordering=401,
    targets=(skeletonboundary.SkelContextFaceBoundary,),
    params=[BdyModFaceAggregateParameter(
        'group', tip="The faces to add to the boundary.")],
    tip="Add a set of faces to an existing face boundary.")
            

class RemoveFaces(BoundaryModifier):
    def __init__(self, group):
        self.group = group

    def attempt(self, skelcontext, boundary):
        faces = skelcontext.faces_from_face_aggregate(self.group)
        return skelcontext.try_removeFacesFromBdy(boundary, faces)

    def apply(self, skelcontext, boundary):
        faces = skelcontext.faces_from_face_aggregate(self.group)
        skelcontext.removeFacesFromBdy(boundary, faces)

registeredclass.ThreeDOnlyRegistration(
    "Remove faces",
    BoundaryModifier,
    RemoveFaces,
    ordering=402,
    targets=(skeletonboundary.SkelContextFaceBoundary,),
    params=[BdyModFaceAggregateParameter(
        'group', tip="The faces to remove from the boundary.")],
    tip="Remove a set of faces from an existing boundary.")
        
# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

class ReverseBoundary(BoundaryModifier):
    def apply(self, skelcontext, boundary):
        skelcontext.reverseBoundary(boundary)

registeredclass.Registration(
    "Reverse direction",
    BoundaryModifier,
    ReverseBoundary,
    ordering=202,
    targets=(skeletonboundary.SkelContextEdgeBoundary, 
             skeletonboundary.SkelContextFaceBoundary),
    tip="Reverse the direction of an edge boundary.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/reverse_bdy.xml')
    )

