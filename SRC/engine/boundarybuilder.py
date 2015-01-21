# -*- python -*-
# $RCSfile: boundarybuilder.py,v $
# $Revision: 1.65.2.21 $
# $Author: langer $
# $Date: 2014/08/20 02:21:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This file defines registered class objects which actually
# build boundaries.  Structure is similar to skeletonselectionmod.

from ooflib.SWIG.common import config 
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.engine import cskeletonface
from ooflib.SWIG.engine import cskeletonsegment
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import director
from ooflib.common import registeredclass
from ooflib.common import primitives
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import coverage
from ooflib.engine import skeletoncontext
#from ooflib.engine import skeletonsegment # for the segSequence function.
from ooflib.engine.IO import skeletongroupparams
import math
#Interface branch
from ooflib.engine.IO import interfaceparameters

# A Note on Direction Parameters and Widgets:
#
# Edge and face boundary construction commands need a "direction"
# parameter.  The relevant direction parameters depend on whether or
# the the set of edges or faces is open or closed.  For example, a
# closed loop can be counterclockwise or clockwise, but an open curve
# can be left to right.  The DirectorWidgets that present the choices
# of directions are defined in engine.IO.GUI.boundarybuilderGUI.  They
# rely on being able to find the SkeletonAggregateWidget that selects
# the set of source objects (groups or selections of elements, edges,
# etc) and asking it for the set of objects.  The DirectorWidget then
# checks to see if the set forms a valid boundary, and if it's open or
# closed.
#
# For this to work, the SkeletonAggregateWidget classes need to set
# the segmentExtractor and faceExtractor dicts in
# engine.IO.skeletongroupwidgets.  The values in these dicts are
# functions from *this* file that extract sets of segments and faces
# from aggregates (groups or selections) of other Skeleton objects.

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

# Boundary naming components.

# This resolver can return "None" in the skelname==None case, which
# occurs when the registeredclassfactory switches around.
def bdynameresolver(param, startname):
    if param.automatic():
        basename='boundary'
    else:
        basename = startname
    skelname = param.group['skeleton'].value
    skelcontext = skeletoncontext.skeletonContexts[skelname]
    return skelcontext.uniqueBoundaryName(basename)


skeletonparam = whoville.WhoParameter(
    'skeleton',
    skeletoncontext.skeletonContexts,
    tip="The Skeleton containing the  boundary.")

nameparam = parameter.AutomaticNameParameter(
    'name', 
    bdynameresolver, value=automatic.automatic,
    tip="Name for this boundary.")

paramgroup = parameter.ParameterGroup(skeletonparam, nameparam)

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

class BoundaryConstructor(registeredclass.RegisteredClass):
    registry = []
    tip = "Tools to build Skeleton boundaries."
    discussion = """<para>
    <classname>BoundaryConstructor</classname> objects are used by the
    <xref linkend='MenuItem-OOF.Skeleton.Boundary.Construct'/> command
    to build <link
    linkend='Section-Concepts-Skeleton-Boundary'>boundaries</link> in
    a &skel;.
    </para>"""

## The "ordering" data in the Registrations is the sum of two of the
## following.
# The type of boundary being constructed:
_nodeBdyConstructor = 1000 
_edgeBdyConstructor = 2000
_faceBdyConstructor = 3000
# What it's being constructed from:
_nodeBdySource = 100
_edgeBdySource = 200
_faceBdySource = 300
_elemBdySource = 400

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

# Utility function -- given a bunch of segments and an orientation,
# it returns (startnode, seg_list), where seg_list is suitably
# ordered, and startnode is at the start.  Throws an exception if
# it fails.  This is only for 2D.
def _segset2seglist(seg_set, direction, skel):

    if len(seg_set)==0:
        raise ooferror.ErrUserError(
            "Attempt to sequence null segment set.")
    
    (seg_list, node_list, winding_number) = skeletonsegment.segSequence(seg_set)
    
    # At this point, seg_list is an ordered list of adjacent
    # segments, and "node_list" is the corresponding set of nodes.
    # The path is a loop if node_list[0]==node_list[-1], otherwise
    # it's a simple path.

    # We may want to reverse this list, depending on the
    # setting of "direction".
    firstnode = node_list[0]
    lastnode = node_list[-1]
    
    startnode = firstnode
    # The winding number is used to handle the cases where the line
    # crosses a periodic boundary.
    if (firstnode != lastnode and firstnode not in lastnode.getPartners()) \
       or winding_number != [0,0]:
        # In case the first node and last node are partners, we set them
        # equal so that we can compare positions properly.
        if lastnode in firstnode.getPartners():
            lastnode = firstnode
        if direction == director.Director('Left to right'):
            if (firstnode.position().x > 
                lastnode.position().x + winding_number[0]*skel.MS.size()[0]):
                seg_list.reverse()
                startnode = lastnode
        elif direction == director.Director('Right to left'):
            if (firstnode.position().x < 
                lastnode.position().x + winding_number[0]*skel.MS.size()[0]):
                seg_list.reverse()
                startnode = lastnode
        elif direction == director.Director('Top to bottom'):
            if (firstnode.position().y < 
                lastnode.position().y + winding_number[1]*skel.MS.size()[1]):
                seg_list.reverse()
                startnode = lastnode
        elif direction == director.Director('Bottom to top'):
            if (firstnode.position().y > 
                lastnode.position().y + winding_number[1]*skel.MS.size()[1]):
                seg_list.reverse()
                startnode = lastnode
        else:
            # User specified clockwise or counterclockwise for a
            # non-loop segment set.  This is an error.
            raise ooferror.ErrUserError(
                "Clockwise or counterclockwise is for closed loops.")

    else: # firstnode==lastnode, loop case.
        # Use the total area swept out by vectors from the origin to the
        # nodes along the path as we traverse the path in order to
        # determine if the existing sequence traces a clockwise or
        # counterclockwise path.  If two consecutive nodes in the
        # node_list are not the endpoints of a segment, we are crossing a
        # periodic boundary.  In this case, use the positions not to find
        # the area swept out, but to increment the position_adjustment
        # needed to unwrap the periodic boundary conditions.
        startnode = None
        area = 0.0
        p0 = node_list[0].position()
        position_adjustment = primitives.Point(0,0)
        for i in range(1,len(node_list)):
            p1 = node_list[i].position() + position_adjustment
            if skel.findSegment(node_list[i],node_list[i-1]) is not None:
                area += p0.x * p1.y - p1.x * p0.y
                p0 = p1
            else:
                position_adjustment += p0 - p1
                # setting p0 = p1 here will be redundant as we
                # must now adjust positions by p0 - p1
            
        if direction == director.Director('Clockwise'):
            if area > 0.0:
                seg_list.reverse()
        elif direction == director.Director('Counterclockwise'):
            if area < 0.0:
                seg_list.reverse()
        else:
            # User specified an endpoint orientation on a loop.
            raise ooferror.ErrUserError(
                "Closed loops need clockwise or counterclockwise direction.")

    return (startnode, seg_list)

# 3D version.  This does not handle periodic boundary conditions yet.

## TODO MER: merge 2D and 3D by using the SegmentSequence class in 2D too.
## Add periodic boundary condition handling to it, and to
## _segset2seglist3D, which should be renamed back to _segset2seglist.
## Actually, it should have a better name than that.

def _segset2seglist3D(seg_set, direction):
    if len(seg_set) == 0:
        raise ooferror.ErrUserError("Segment sequence is empty.")
    # sequenceSegments returns a SegmentSequence obj
    sequence = cskeletonsegment.sequenceSegments(seg_set, None)

    ## TODO OPT: direction should be a RegisteredClass with a check()
    ## method that takes a sequence arg.  Then the rest of this
    ## routine could be replaced with
    ##   if not direction.check(sequence): sequence.reverse()
    if not sequence: 
        return
    if not sequence.closed():
        span = sequence.span()  # last point - first point
        if direction not in director.unclosedDirections:
            raise ooferror.ErrUserError(
                "Direction must be one of " + `director.unclosedDirections`)
        if ( (direction == '-X to +X' and span[0] < 0) or
             (direction == '+X to -X' and span[0] > 0) or 
             (direction == '-Y to +Y' and span[1] < 0) or
             (direction == '+Y to -Y' and span[1] > 0) or
             (direction == '-Z to +Z' and span[2] < 0) or
             (direction == '+Z to -Z' and span[2] > 0) ):
            sequence.reverse()
    else:
        # The sequence is a loop.  The direction is of the form
        # "Clockwise-x", "Counterclockwise-y", etc.  The segment
        # sequence should be clockwise or counterclockwise when
        # projected onto a plane in the given direction.
        if direction.string() not in director.closedLoopDirections:
            raise ooferror.ErrUserError(
                "Direction must be one of " + `director.closedLoopDirections`)
        chirality, axis = direction.string().split('-')
        area = sequence.projectedArea(axis)
        if ( chirality == 'Clockwise' and area > 0
             or chirality == 'Counterclockwise' and area < 0 ):
            sequence.reverse()
    return sequence
            
            
# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #


# Build an edge boundary from a segment set.
class EdgeFromSegments(BoundaryConstructor):
    def __init__(self, group, direction):
        self.group = group
        self.direction = direction

    def __call__(self, skelcontext, name):
        skelobj = skelcontext.getObject()

        seg_set = skelcontext.segments_from_seg_aggregate(self.group)
        
        if config.dimension() == 2:
            (startnode, seg_list) = _segset2seglist(seg_set, self.direction,
                                                    skelobj)
            # At this point, we have a correctly-sequenced list of segments.
            # Actually create the boundary.  The context will create it in
            # the underlying object.
            skelcontext.createEdgeBoundary(name, seg_list, startnode)
        else:                   # 3D
            segmentsequence = _segset2seglist3D(seg_set, self.direction)
            skelcontext.createEdgeBoundary3D(name, segmentsequence)

if config.dimension() == 2:
    director0 = director.Director('Left to right')
else:
    director0 = director.Director('-X to +X')

registeredclass.Registration(
    "Edge boundary from segments",
    BoundaryConstructor,
    EdgeFromSegments,
    ordering = _edgeBdyConstructor + _edgeBdySource,
    params = [
        skeletongroupparams.SegmentAggregateParameter(
            'group',
            tip="Construct the boundary from these segments"),
        director.DirectorParameter(
            'direction', director0,
            tip="Direction of the boundary.")
        ],
    tip="Construct an edge boundary from a set of segments.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/edge_from_segments.xml'))
    
# ## ### #### ##### ###### ####### ######## ####### ##### #### ### ## #
  
# Finds the perimeter of an elementgroup.  Unless we allow
# non-sequenceable boundaries, this requires that the element group
# have a topologically simple (non-self-intersecting, non-disjoint)
# boundary, which will never happen in 3D, so this is only provided in
# 2D.

def segments_from_el_aggregate(skelcontext, group):
    # Utility function for extracting a list of exterior segments from
    # a set of elements.  Also used by the DirectorWidget in
    # association with an ElementAggregateWidget.  Only works in 2D,
    # but that's ok because segments derived from elements are never
    # sequenceable in 3D.

    elements = skelcontext.elements_from_el_aggregate(group)
        
    skelobj = skelcontext.getObject()
    seg_set = {}
    # We want to retain the boundary segments -- these occur
    # exactly once in the element set, and all the others occur
    # exactly twice, so iterate over all the segments, adding them
    # to a dictionary, unless they already appear, in which case
    # remove them.
    for e in elements:
        for s in e.getSegments(skelcontext.getObject()):
            try:
                del seg_set[s]
            except KeyError:
                seg_set[s]=1
    # Now post process to see if any remaining segments coincide
    # on the periodic boundaries.
    ## TODO OPT: Perhaps partnered segments would be useful for this?
    for s in seg_set.keys():    # NOT 'for s in seg_set'.  seg_set changes.
        nodes = s.get_nodes()
        partners = nodes[0].getPartnerPair(nodes[1])
        if partners is not None:
            ps = skelobj.findSegment(partners[0],partners[1])
            if ps in seg_set:
                del seg_set[ps]
                del seg_set[s]
    return seg_set.keys()

class EdgeFromElements(BoundaryConstructor): # 2D only
    def __init__(self, group, direction):
        self.group = group
        self.direction = direction

    def __call__(self, skelcontext, name):
        skelobj = skelcontext.getObject()
        seg_list = segments_from_el_aggregate(skelcontext, self.group)
        (startnode, seg_list) = _segset2seglist(seg_list, self.direction,
                                                skelobj)
        skelcontext.createEdgeBoundary(name, seg_list, startnode)


registeredclass.TwoDOnlyRegistration(
    "Edge boundary from elements",
    BoundaryConstructor,
    EdgeFromElements,
    ordering = _edgeBdyConstructor + _elemBdySource,
    params = [
        skeletongroupparams.ElementAggregateParameter(
            'group',
            tip="Construct the boundary from these elements"),
        director.DirectorParameter(
            'direction',
            tip="Direction of Boundary.")
        ],
    tip="Construct an edge boundary around a set of elements.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/edge_from_elements.xml'))


# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

def segments_from_face_aggregate(skelcontext, group):
    faces = skelcontext.faces_from_face_aggregate(group)
    ## TODO OPT: If cskeletonsegment.sequenceSegments() could accept a set
    ## as well as a list, we wouldn't have to convert the set returned
    ## by exteriorSegmentsOfFaceSet to a list here.
    return list(skelcontext.exteriorSegmentsOfFaceSet(faces))

class EdgeFromFaces(BoundaryConstructor):
    def __init__(self, group, direction):
        self.group = group
        self.direction = direction
    def __call__(self, skelcontext, name):
        segs = segments_from_face_aggregate(skelcontext, self.group)
        skelobj = skelcontext.getObject()
        segmentsequence = _segset2seglist3D(segs, self.direction)
        skelcontext.createEdgeBoundary3D(name, segmentsequence)

registeredclass.ThreeDOnlyRegistration(
    "Edge boundary from faces",
    BoundaryConstructor,
    EdgeFromFaces,
    ordering = _edgeBdyConstructor + _faceBdySource,
    params = [
        skeletongroupparams.FaceAggregateParameter(
            'group',
            tip="Face group from which to get segments."),
        director.DirectorParameter(
            'direction',
            director.Director('Counterclockwise-x'),
            tip="Direction of the boundary.")],
    tip="Construct an edge boundary from a collection of faces")

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

# Constructing edge boundaries from sets of nodes is the most
# complicated operation. Some sets of nodes define unique sets of
# edges, but it's non-trivial to determine which edges they are.

# Path construction: Take a set of segments, and reduce them to a
# subset that includes all of the nodes in the original set, if the
# subset is unique.

# Stateful object for keeping track of where you are in the
# path-construction process.  Maintains a list of segments-or-None,
# and a dictionary, indexed by nodes, of pointers into this list.
# "None" in the list means that the segment in question has already
# been used in the current path.
class PathBuilder:
    # If a segment list is provided, it should be complete, with no
    # "None" entries in it.  This is only required at start-time.
    def __init__(self, segments=None):
        self.finished = False
        self.loop = False # Paths can be loops, or not.
        if segments:
            self.seg_list = segments[:]
            self.path = []         # List of segments used so far.
            self.last_node = None  # Trailing node of the path so far.
            self.node_dict = utils.OrderedDict()
            for i in range(len(segments)):
                # Build a node-indexed dictionary of indices into the
                # segments list. node_dict[n] is a list of indices,
                # indicating which segments in the segments list
                # connect to node n.
                seg_nodes = self.seg_list[i].getNodes()
                for n in seg_nodes:
                    self.node_dict.setdefault(n, []).append(i)

    # The iterate function -- returns a list of PathBuilder objects
    # one step farther along than the current one.
    def iterate(self):
        if self.finished:
            return []
        
        # Find a node to start from.
        if self.last_node is None:
            for (n,s) in self.node_dict.items():
                if len(s)==1:
                    node = n
                    index_list = self.node_dict[node]
                    break
            else:
                # Loop case -- no node has exactly one neighbor.  Find
                # one that has exactly two, and then proceed in only
                # one direction from it.  This looks expensive, but
                # for well-formed node sets, it will succeed in O(1).
                for (n,s) in self.node_dict.items():
                    if len(s)==2:
                        node = n
                        index_list = self.node_dict[node][:-1]
                        self.loop = True
                        break
                else:
                    # Pathological case -- no node has exactly two neighbors.
                    # Unique path is impossible.
                    self.finished = True
                    return []
        else:
            node = self.last_node
            index_list = self.node_dict[node]

        res = []
        for i in index_list:
            seg = self.seg_list[i]
            if seg:
                new_pb = PathBuilder()
                new_pb.loop = self.loop
                new_pb.seg_list = self.seg_list[:]
                new_pb.seg_list[i]=None
                new_pb.path = self.path[:] + [seg]
                new_pb.node_dict = self.node_dict # Shared reference
                new_pb.last_node = seg.get_other_node(node)
                res.append(new_pb)

        if res==[]:
            self.finished = True
        return res
    
    def __repr__(self):
        return "PathBuilder(" + `self.path` + ")"

    # Query: Does the current path use all the nodes?  If it's a loop,
    # does it, in fact, loop?  This test is probably too expensive.
    def well_formed_q(self):
        node_count_dict = {}
        for n in self.node_dict:
            node_count_dict[n] = 0
        for segment in self.path:
            for node in segment.getNodes():
                node_count_dict[node] += 1
        if self.loop:
            # All nodes in a non-self-intersecting loop must be part
            # of exactly two segments.
            for count in node_count_dict.values():
                if count != 2:
                    return False
        else:
            # Not a loop.  All nodes should be part of two segments,
            # except for two endpoints, which are part of just one.
            nEnds = 0           # number of nodes with just one segment
            for count in node_count_dict.values():
                if count == 1:
                    nEnds += 1
                elif count != 2:
                    return False
            if nEnds != 2:
                return False
        return True

# Routine which uses the PathBuilder class, above, to do an expensive
# but good-quality assessment of the segment set, and picks out a
# path, if there is one.

def _really_good_segs(segs):
    path_list = [ PathBuilder(segs) ]
    finished = False
    # Iterate the pathbuilders until they're all done.  This is the
    # expensive part, in the sense of scaling combinatorially badly in
    # the number of enclosed loops in the node set.
    while not finished:
        finished = True
        new_path_list = []
        for p in path_list:
            new_paths = p.iterate()
            if new_paths:
                new_path_list += new_paths
                finished = False
            else:
                new_path_list.append(p)
        path_list = new_path_list

    # Select only the paths which are well-formed, according to the
    # PathBuilder's routine.
    good_path = None
    for p in path_list:
        if p.well_formed_q():
            if good_path:
                # There's more than one well-formed path, so the
                # solution is not unique.  Bail.
                return []
            good_path = p
    if good_path:
        # There's just one well-formed path.
        return good_path.path
    # There are no well-formed paths.  Return nothing.
    return []

# A more primitive but faster segment-pruning scheme.  Given the
# initial segment set, find either two nodes with exactly one segment
# each (straight case), or, if no such nodes exist, one node with
# exactly two segments associated with it.  Then, traverse the segment
# set in each direction, using a "keep to the right" rule at
# branch-points, if any.  If either direction's traversal results in a
# set of segments which include each of the original nodes exactly
# once, then return that segment set -- you have pruned out extraneous
# segments.

# Another utility function -- given a segment, and the *trailing* node
# on that segment, it returns the next segment-and-trailing-node pair,
# keeping furthest to the right in case of branches.
def _right_traverse_step(segment, node, node_dict):
    sset = node_dict[node][:] # Make a local copy of this list.
    sset.remove(segment)      # Ditch the one we know about already.
    if len(sset)==0:  # Unable to proceed, nowhere to go.
        return None
    if len(sset)==1:  # Trivial case, no branch here.
        if node in sset[0].get_nodes():
            return (sset[0], sset[0].get_other_node(node))
        # the segment is on the other side of a periodic boundary
        else:
            for partner in node.getPartners():
                # there will only be one partner in the segment
                if partner in sset[0].get_nodes():
                    return (sset[0], sset[0].get_other_node(partner))
                
    # "Node" is the trailing node.
    if node in segment.get_nodes():
        incoming_vec = node.position() - segment.get_other_node(node).position()
    else:
        for partner in node.getPartners():
            if partner in segment.get_nodes():
                incoming_vec = partner.position() - \
                               segment.gett_other_node(partner).position()
    incoming_mag = math.sqrt(incoming_vec**2)
    normalized_iv = incoming_vec/incoming_mag
    maximal_pair = None
    maximal_angle = -math.pi
    for s in sset:
        if node in s.get_nodes():
            pair = (s, s.get_other_node(node))
            trailing_node = node
        else:
            for partner in node.getPartners():
                if partner in s.get_nodes():
                    pair = (s, s.get_other_node(partner))
                    trailing_node = partner
        outgoing_vec = pair[1].position()-trailing_node.position()
        outgoing_mag = math.sqrt(outgoing_vec**2)
        normalized_ov = outgoing_vec/outgoing_mag
        cos = normalized_iv*normalized_ov
        sin = normalized_ov.cross(normalized_iv) # Positive for rightward.
        angle = math.atan2(sin,cos)
        if angle > maximal_angle:
            maximal_angle = angle
            maximal_pair = pair
    return maximal_pair

# Higher-level utility function -- given a *starting* node and a
# segment, does a keep-to-the-right traverse of the node-dict until it
# can't go any farther.  If the resulting segment set uses all the
# nodes, then it returns the segments, in order, otherwise it raises
# the "IncompletePath" exception.

class IncompletePath(Exception): pass

def _right_traverse(node, segment, node_dict):
    nodelist = node_dict.keys()[:] # TODO OPT: Is [:] needed?  keys()
                                   # returns an independent list.
    nodelist.remove(node)
    for partner in node.getPartners():
        nodelist.remove(partner)
    seglist = []
    trailing_node = segment.get_other_node(node)
    
    while 1:
        seglist.append(segment)
        try:
            nodelist.remove(trailing_node)
            for partner in trailing_node.getPartners():
                nodelist.remove(partner)
        except ValueError:
            # Node has already been visited, but we're not done!  That
            # means that there's an internal loop.
            raise IncompletePath()
        next = _right_traverse_step(segment, trailing_node, node_dict)
        if not next: # Straight-through completion case.
            break
        segment, trailing_node = next
        # Loop completion case.
        if trailing_node==node or trailing_node in node.getPartners():
            seglist.append(segment)
            break

    if len(nodelist)==0:
        return seglist
    raise IncompletePath()
        

def _prune_segments(segs):              # part of a well balanced breakfast
    # create a list of segments for each node.
    # Only used in 2D.
    node_dict = {} 
    for s in segs:
        for n in s.get_nodes():
            node_dict.setdefault(n, []).append(s)
            # # include the partners
            # for p in n.getPartners():
            #     try:
            #         node_dict[p].append(s)
            #     except KeyError:
            #         node_dict[p] = [s]
                
    straight_start_points = []
    loop_start_point = None
    for (n,ss) in node_dict.items():
        if len(ss)==1:
            straight_start_points.append(n)
        elif len(ss)==2 and not loop_start_point:
            loop_start_point = n

    len_ssp = len(straight_start_points)

    # If there's a unique path, there must be either 0 endpoints (a
    # loop) or two endpoints.
    if len_ssp!=0 and len_ssp!=2:
        return []

    # Collect the approprate starting-node-and-segment pairs.
    if len_ssp==2:
        node1 = straight_start_points[0]
        seg1 = node_dict[node1][0]
        node2 = straight_start_points[1]
        seg2 = node_dict[node2][0]
    else: # len_ssp==0
        node1 = loop_start_point
        seg1 = node_dict[node1][0]
        node2 = node1
        seg2 = node_dict[node2][1]
        
    # Find paths. Accept the first one that works.  

    try:
        path = _right_traverse(node1, seg1, node_dict)
    except IncompletePath:
        try:
            path = _right_traverse(node2, seg2, node_dict)
        except IncompletePath:
            return []
    return path


def segments_from_node_aggregate(skelcontext, group):
    nodes = skelcontext.nodes_from_node_aggregate(group)

    seg_counts = utils.OrderedDict()
    node_counts = utils.OrderedDict()
    skel = skelcontext.getObject()

    # Look at all the segments connected to the nodes, and count how
    # many times each segment is found.
    for n in nodes:
        node_counts[n] = 0 # used later when checking for isolated nodes
        for s in skel.getNodeSegments(n):
            try:
                seg_counts[s] += 1
            except KeyError:
                seg_counts[s] = 1

    # Keep the segments that have two nodes in the node set.
    good_segs = [s for (s, count) in seg_counts.items() if count==2]

    if len(good_segs)==0:
        return []

    # Double-check that set of good segments includes all the nodes.
    # An isolated node won't be in good_segs, and means that the nodes
    # don't form a connected boundary.
    for s in good_segs:
        for n in s.getNodes():
            node_counts[n] += 1
    for count in node_counts.values():
        if count==0:
            return []

    # The segments in good_segs may form loops, which is not
    # necessarily an error.  What we really want is the unique path
    # that uses all the nodes, if there is one.
    if config.dimension() == 2:
        return _prune_segments(good_segs)
    else:
        # _really_good_segs is a very robust but combinatorially
        # badly-scaling algorithm, but it works in 3D.
        return _really_good_segs(good_segs)

    # Or there is the old way of just returning the segment set, which
    # will get tripped up on easily-resolvable loops in the segment
    # set:
    # return good_segs

class EdgeFromNodes(BoundaryConstructor):
    def __init__(self, group, direction):
        self.group = group
        self.direction = direction

    def __call__(self, skelcontext, name):
        skelobj = skelcontext.getObject()
        seg_set = segments_from_node_aggregate(skelcontext, self.group)
        if not seg_set:
            raise ooferror.ErrUserError(
                "A unique segment sequence cannot be created"
                " from the given nodes.")
        if config.dimension() == 2:
            (startnode, seg_list) = _segset2seglist(seg_set, self.direction,
                                                    skelobj)
            skelcontext.createEdgeBoundary(name, seg_list, startnode)
        else:                   # 3D
            segmentsequence = _segset2seglist3D(seg_set, self.direction)
            skelcontext.createEdgeBoundary3D(name, segmentsequence)

registeredclass.Registration(
    "Edge boundary from nodes",
    BoundaryConstructor,
    EdgeFromNodes,
    ordering = _edgeBdyConstructor + _nodeBdySource,
    params=[
        skeletongroupparams.NodeAggregateParameter(
            'group',
            tip="Node group from which to deduce segments"),
        director.DirectorParameter(
            'direction',
            director0,
            tip="Direction of Boundary.")],
    tip="Construct an edge boundary from a collection of nodes.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/edge_from_nodes.xml'))

# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

# Point boundary construction can be done from either
# segments or nodes, both cases are very simple.
class PointFromNodes(BoundaryConstructor):
    def __init__(self, group):
        self.group = group

    def __call__(self, skelcontext, name):
        nodelist = skelcontext.nodes_from_node_aggregate(self.group)
        skelcontext.createPointBoundary(name, nodelist)

registeredclass.Registration(
    "Point boundary from nodes",
    BoundaryConstructor,
    PointFromNodes,
    ordering = _nodeBdyConstructor + _nodeBdySource,
    params = [
        skeletongroupparams.NodeAggregateParameter(
            'group', tip="Construct the boundary from these nodes")],
    tip="Construct a point boundary from a set of nodes.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/point_from_nodes.xml')
    )


class PointFromSegments(BoundaryConstructor):
    def __init__(self, group):
        self.group = group

    def __call__(self, skelcontext, name):
        ## TODO OPT: If this causes reproducibility problems in the test
        ## suite, use utils.OrderedSet instead of set here.
        nodes = set()
        segments = skelcontext.segments_from_seg_aggregate(self.group)
        for s in segments:
            nodes.update(s.getNodes())
                
        skelcontext.createPointBoundary(name, nodes)

registeredclass.Registration(
    "Point boundary from segments",
    BoundaryConstructor,
    PointFromSegments,
    ordering = _nodeBdyConstructor + _edgeBdySource,
    params = [
        skeletongroupparams.SegmentAggregateParameter(
            'group',
            tip="Construct the boundary from these segments")],
    tip="Construct a point boundary from the endpoints of a set of segments.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/point_from_segments.xml'))

class PointFromFaces(BoundaryConstructor):
    def __init__(self, group):
        self.group = group

    def __call__(self, skelcontext, name):
        ## TODO OPT: If this causes reproducibility problems in the test
        ## suite, use utils.OrderedSet instead of set here.
        nodes = set()
        faces = skelcontext.faces_from_face_aggregate(self.group)
        for f in faces:
            nodes.update(f.getNodes())
        skelcontext.createPointBoundary(name, nodes)

if config.dimension() == 3:
    registeredclass.Registration(
        "Point boundary from faces",
        BoundaryConstructor,
        PointFromFaces,
        ordering = _nodeBdyConstructor + _faceBdySource,
        params = [
            skeletongroupparams.FaceAggregateParameter(
                'group',
                tip='Construct the boundary from these faces')],
        tip="Construct a point boundary from the vertices of a set of faces.",
    )


class PointFromElements(BoundaryConstructor):
    def __init__(self, group, coverage):
        self.group = group
        self.coverage = coverage

    def __call__(self, skelcontext, name):
        skelobj = skelcontext.getObject()

        elements = skelcontext.elements_from_el_aggregate(self.group)
        if config.dimension() == 2:
            nodes = set()
            for element in elements:
                for i in range(element.nnodes()):
                    n0 = element.nodes[i]
                    n1 = element.nodes[(i+1)%element.nnodes()]
                    seg = skelobj.getSegment(n0, n1)
                    # A segment is on the boundary of the selection if it
                    # belongs to only one element.
                    n = 0
                    for el in seg.getElements():
                        if el in elements: n += 1
                    if n == 1:
                        nodes.add(n0)
                        nodes.add(n1)

        else:                   # 3D
            if self.coverage == "All":
                nodes = skelcontext.allNodesOfElementSet(elements)
            elif self.coverage == "Exterior":
                nodes = skelcontext.exteriorNodesOfElementSet(elements)
            else:               # self.coverage == "Interior"
                nodes = (skelcontext.allNodesOfElementSet(elements) -
                         skelcontext.exteriorNodesOfElementSet(elements))
                
        skelcontext.createPointBoundary(name, nodes)

registeredclass.Registration(
    "Point boundary from elements",
    BoundaryConstructor,
    PointFromElements,
    ordering = _nodeBdyConstructor + _elemBdySource,
    params = [
        skeletongroupparams.ElementAggregateParameter(
            'group', tip="Construct the boundary from these elements"),
        enum.EnumParameter(
            'coverage', coverage.Coverage, 
            tip="Which nodes to choose from the set of elements.")
    ],
    tip="Construct a point boundary from a set of elements.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/point_from_elements.xml'))

###############################################################
#Interface branch


# Build an edge boundary from segments along an interface
class EdgeFromInterface(BoundaryConstructor):
    def __init__(self, interface, direction):
        self.interface = interface
        self.direction = direction

    def __call__(self, skelcontext, name):
        skelobj = skelcontext.getObject()

        (seg_set, direction_set)=skelobj.getInterfaceSegments(
            skelcontext, self.interface)

        if self.direction==director.Director('Non-sequenceable'):
            skelcontext.createNonsequenceableEdgeBoundary(name, seg_set,
                                                          direction_set)
        else:
            if config.dimension() == 2:
                (startnode, seg_list) = _segset2seglist(seg_set, self.direction,
                                                        skelobj)
                # At this point, we have a correctly-sequenced list of
                # segments.  Actually create the boundary.  The
                # context will create it in the underlying object.
                skelcontext.createEdgeBoundary(name, seg_list, startnode)
            else:               # 3D
                segmentsequence = _segset2seglist3D(seg_set, self.direction)
                skelcontext.createEdgeBoundary3D(name, segmentsequence)

if config.dimension() == 2:
    registeredclass.Registration(
        "Edge boundary from interface segments",
        BoundaryConstructor,
        EdgeFromInterface,
        ordering = _edgeBdyConstructor + _edgeBdySource + 1,
        params = [
        interfaceparameters.InterfacesParameter(
                'interface',
                tip='Construct the boundary from these interface segments.'),
            # skeletongroupparams.SegmentAggregateParameter(
            #     'group',
            #     tip="Construct the boundary from these segments"),
        director.DirectorInterfacesParameter(
                'direction', director0,
                tip="Direction of the boundary.")],
        tip="Construct an edge boundary from a set of interface segments.",
        discussion = """<para>

        Create an edge boundary from segments specified by an
        interface definition.  If the interface segments are
        disconnected, the corresponding edge boundary is also
        disconnected, and it will be labeled as not sequenceable.

        </para>"""
        )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## TODO 3.1: It's possible to create moebius strips, but not all boundary
## conditions make sense on them.  Do we need two classes of face
## boundaries?  (Do we need two classes of edge boundaries?  Not all
## edge sets are sequenceable.)

def constructOrientedSurface(skelcontext, faces, direction):
    # orientFaces() returns an OrientedSurface object, but its
    # orientation may not be correct.
    ofaces = cskeletonface.orientFaces(skelcontext.getObject(),
                                       faces, None)
    if not ofaces:
        raise ooferror.ErrUserError(
            "Failed to construct an orientable surface")

    if ofaces.closed():
        if direction.string() not in director.closedSurfaceDirections:
            raise ooferror.ErrUserError(
                "Direction must be one of " + `director.closedSurfaceDirections`
            )
        vol = ofaces.volume()
        if (vol > 0 and direction == "Inward"
            or vol < 0 and direction == "Outward"):
            ofaces.reverse()
    else:                       # not a closed surface
        if direction.string() not in director.unclosedDirections:
            raise ooferror.ErrUserError(
                "Direction must be one of " + `director.unclosedDirections`)
        normal = ofaces.normal()
        if ( (direction == '-X to +X' and normal[0] < 0) or
             (direction == '+X to -X' and normal[0] > 0) or 
             (direction == '-Y to +Y' and normal[1] < 0) or
             (direction == '+Y to -Y' and normal[1] > 0) or
             (direction == '-Z to +Z' and normal[2] < 0) or
             (direction == '+Z to -Z' and normal[2] > 0) ):
            ofaces.reverse()
    return ofaces

# For open sets of faces, the direction can be specified by whether
# the average normal is positive or negative along a given axis.  For
# closed sets, the direction is either inward or outward and can be
# found by computing the enclosed volume.

class FaceFromFaces(BoundaryConstructor):
    def __init__(self, group, direction):
        self.group = group
        self.direction = direction
    
    def __call__(self, skelcontext, name):
        faces = skelcontext.faces_from_face_aggregate(self.group)
        orientedsurface = constructOrientedSurface(skelcontext, faces,
                                                   self.direction)
        skelcontext.createFaceBoundary(name, orientedsurface)

registeredclass.ThreeDOnlyRegistration(
    "Face boundary from faces",
    BoundaryConstructor,
    FaceFromFaces,
    ordering = _faceBdyConstructor + _faceBdySource,
    params = [
        skeletongroupparams.FaceAggregateParameter(
            'group',
            tip="Construct the boundary from these faces."),
        director.SurfaceDirectorParameter("direction")
    ],
    tip="Construct a face boundary from a set of element faces.")


def faces_from_el_aggregate(skelcontext, group):
    elements = skelcontext.elements_from_el_aggregate(group)
    skelobj = skelcontext.getObject()
    face_count = {}
    for e in elements:
        for f in skelobj.getElementFaces(e):
            face_count[f] = face_count.get(f, 0) + 1
    faces = [f for (f, count) in face_count.items() if count == 1]
    return faces

class FaceFromElements(BoundaryConstructor):
    def __init__(self, group, direction):
        self.group = group
        self.direction = direction
    
    def __call__(self, skelcontext, name):
        faces = faces_from_el_aggregate(skelcontext, self.group)
        orientedsurface = constructOrientedSurface(skelcontext, faces,
                                                   self.direction)
        skelcontext.createFaceBoundary(name, orientedsurface)

registeredclass.ThreeDOnlyRegistration(
    "Face boundary from elements",
    BoundaryConstructor,
    FaceFromElements,
    ordering = _faceBdyConstructor + _elemBdySource,
    params = [
        skeletongroupparams.ElementAggregateParameter(
            'group',
            tip="Construct the boundary from the exterior faces of these elements."),
        director.SurfaceDirectorParameter("direction")
    ],
    tip="Construct a face boundary from the exterior faces of set of elementa.")

## TODO 3.1: Maybe also construct face boundaries from segments or nodes?
## That's probably difficult, since it usually wouldn't be obvious
## which faces should be included.
