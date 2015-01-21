# -*- python -*-
# $RCSfile: skeletonsegment.py,v $
# $Revision: 1.49.2.4 $
# $Author: langer $
# $Date: 2013/06/06 19:37:20 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import config
from ooflib.SWIG.common import timestamp
#from ooflib.engine import skeletonselectable
#from ooflib.engine import skeletonnode
from ooflib.common import debug
from ooflib.common import object_id
from ooflib.common import utils
from ooflib.common import primitives
import math

## THIS FILE IS ONLY USED IN 2D
assert config.dimension() == 2

#if config.dimension() == 3:
#    import vtk

# A SkeletonSegment is a connection between two nodes.  There is a
# SkeletonSegment for every adjacent pair of nodes in an element, but the
# SkeletonSegment does not belong to an element, nor does it know its
# direction.  
class SkeletonSegment(skeletonselectable.SkeletonSelectable):
    def __init__(self, nodes, index):
        ## nodes is a tuple containing two SkeletonNodes in canonical
        ## order (see skeletonnode.canonical_order().
        skeletonselectable.SkeletonSelectable.__init__(self, index)
        self._nodes = nodes
        self._elements = []
        self.edges = []

        ## parallel processing variables
        self._rank = -1
        self.ID = object_id.ObjectID()
    def set_rank(self, _rank):
        self.ID.set_rank(_rank)
        
    def repr_position(self):
        return 0.5*(self.nodes()[0].position() + self.nodes()[1].position())

    def length(self):
        n0 = self.nodes()[0].position()
        n1 = self.nodes()[1].position()
        if config.dimension() == 2:
            return math.sqrt((n1.x-n0.x)*(n1.x-n0.x)+(n1.y-n0.y)*(n1.y-n0.y))
        if config.dimension() == 3:
            return math.sqrt((n1.x-n0.x)*(n1.x-n0.x)+
                             (n1.y-n0.y)*(n1.y-n0.y)+(n1.z-n0.z)*(n1.z-n0.z))

    def getIndex(self):
        return self.index

    def active(self, skeleton):
        return self._nodes[0].active(skeleton) or \
               self._nodes[1].active(skeleton)

    def homogeneity(self, microstructure):
        pos0 = self._nodes[0].position()
        pos1 = self._nodes[1].position()
        return microstructure.edgeHomogeneity(pos0, pos1)


    def dominantPixel(self, microstructure):
        n0 = self.nodes()[0].position()
        n1 = self.nodes()[1].position()
        homog, cat = microstructure.edgeHomogeneityCat(n0, n1)
        return cat

    def nodes(self):
        return self._nodes

    def nodeIndices(self):
        return [self._nodes[0].getIndex(), self._nodes[1].getIndex()]

    def addElement(self, element):
        if element in self._elements:
            raise ooferror.ErrPyProgrammingError("Element already in Segment!")
        self._elements.append(element)

    def getElements(self):
        return self._elements

    def nElements(self):
        return len(self._elements)

    def removeElement(self, skeleton, element):
        self._elements.remove(element)
        if not self._elements:
            self.destroy(skeleton)
            
    def destroy(self, skeleton):
        skeleton.removeSegment(self._nodes)
        self.disconnect()
        del self._elements
        del self._nodes
        # Don't del self.edges -- it'll be cleared when boundaries are
        # destroyed.

    # Generic node-retrieval function, common to segments and edges,
    # allowing both to be sequenced by segSequence (see below).
    def get_nodes(self):
        return self._nodes

    # Return the node in the segment other than the node passed in.
    # The argument "node" can also be a periodic partner of one of the
    # nodes in the segment.  In this case, it might not be stored in
    # self._nodes.  We only return the periodic partner of "node" if
    # "node" is in self._nodes, i.e. it is a 1 element wide periodic
    # skeleton.  Note that in cases where we have periodicity in both
    # directions, the segment spans the entire skeleton, and the node
    # passed in is a periodic partner of one of the nodes, the "other
    # node" cannot be determined.
    def get_other_node(self, node):
        for n in self._nodes:
            if n != node and (node not in n.getPartners() or \
                              node in self._nodes):
                return n
        # if we get this far, it's because we've passed an invalid node for this segment.
        raise ooferror.ErrPyProgrammingError("Cannot determine which node is the 'other node' for this segment!")
        
    # New_child is called after new nodes and elements have been
    # created -- it is assumed that the most-recent children are
    # the correct ones.  
    def new_child(self, index):
        n0 = self._nodes[0].getChildren()[-1]
        n1 = self._nodes[1].getChildren()[-1]
        new = SkeletonSegment(skeletonnode.canonical_order(n0, n1), index)
        new._elements = [ x.getChildren()[-1] for x in self._elements ]
        return new

    def getOtherElement(self, element):
        for el in self._elements:
            if el is not element:
                return el

    def getPartner(self, skeleton):     # PBC partner
        pnodes = self._nodes[0].getPartnerPair(self._nodes[1])
        if pnodes:
            return skeleton.findSegment(pnodes[0], pnodes[1])

    def __repr__(self):
        return "SkeletonSegment(%s, %s)" % ( `self._nodes[0]`, `self._nodes[1]`)

    def get_ownership(self):
        return self._rank

    def set_ownership(self, ownr):
        self._rank = ownr

    def getVtkLine(self):
        line = vtk.vtkLine()
        line.GetPointIds().SetId(0, self._nodes[0].getIndex())
        line.GetPointIds().SetId(1, self._nodes[1].getIndex())
        p0 = self._nodes[0].position()
        p1 = self._nodes[1].position()
        line.GetPoints().SetPoint(0,p0.x,p0.y,p0.z)
        line.GetPoints().SetPoint(1,p1.x,p1.y,p1.z)
        return line

    def isExternal(self, MS):
        p0 = self._nodes[0].position()
        p1 = self._nodes[1].position()
        if p0.x == 0.0 and p1.x == 0.0:
            return True
        if p0.x == MS.size()[0] and p1.x == MS.size()[0]:
            return True
        if p0.y == 0.0 and p1.y == 0.0:
            return True
        if p0.y == MS.size()[1] and p1.y == MS.size()[1]:
            return True
        if config.dimension() == 3:
            if p0.z == 0.0 and p1.z == 0.0:
                return True
            if p0.z == MS.size()[2] and p1.z == MS.size()[2]:
                return True
        return False

    def material(self, skelctxt):
        pass

    def boundaryNames(self, skeleton):
        # Which boundaries is this segment part of?
        return [key for key, bdy in skeleton.edgeboundaries.items()
                if self in (e.segment for e in bdy.edges)]
#         bdys = []
#         for key, bdy in skeleton.edgeboundaries.items():
#             for edge in bdy.edges:
#                 if edge.segment == self:
#                     bdys.append(key)
#         return bdys

#######################

class SequenceError(ooferror.ErrError):
    def __init__(self, message):
        self.message = message
    def __repr__(self):
        return "SequenceError: %s" % self.message
    

# Utility function for sequencing a group of segments.  Takes as
# input an un-ordered list of segments, and an optional starting
# node, and provides as output the segments in adjacency order, plus
# the list of nodes in the same sequence.  Should fail gracefully if
# there is a problem with the segments' adjacency.  Used by the boundary
# code.  Return value is the tuple, (segment_list, node_list, winding_vector)
# Calls "get_nodes" so it can also sequence SkeletonEdges.
# (In fact, it can sequence anything that has a get_nodes method...)
# The sequenced set is a loop if the node list is circular, i.e.
# node[0]==node[-1].

def segSequence(seglist, startnode=None):
    # seglist can be a Set or a List

    if len(seglist)==0:
        return ([], [], [])  # Always return the correct form, even if empty.
    
    adjacency = {}
    # Insert the segment into the adjacency dict at both of its nodes.
    for s in seglist:
        n = s.get_nodes()
        try:
            adjacency[n[0]].append(s)
        except KeyError:
            adjacency[n[0]] = [s]

        for p in n[0].getPartners():
            try:
                adjacency[p].append(s)
            except KeyError:
                adjacency[p] = [s]

        try:
            adjacency[n[1]].append(s)
        except KeyError:
            adjacency[n[1]] = [s]

        for p in n[1].getPartners():
            try:
                adjacency[p].append(s)
            except KeyError:
                adjacency[p] = [s]

    endpoints = []

    # remove any grazed corners (nodes added to adjacency dictionary
    # because of partnerships, that are not directly connected to
    # segments in the boundary) before doing the topology check
    for (n,l) in adjacency.items():
        grazedCorner = True
        for seg in l:
            if n in seg.get_nodes():
                grazedCorner = False
        if grazedCorner:
            del adjacency[n]

    # Basic topology check -- if any node occurs in 3 or more
    # segments, there's a self-intersection, and we can't sequence.
    # This loop would also detect zero-length segment lists, but since
    # the nodes used are deduced from the passed-in segments, that
    # can't happen.
    for (n,l) in adjacency.items():
        if len(l)==1:
            endpoints.append(n)
        elif len(l)!=2:
            raise SequenceError(
                "Branch in segment set, unable to sequence.")

    # Find the user's start node, or pick our own.
    if len(endpoints)==2:  # Line case.
        # If there are two endpoints, and the passed-in start is one, OK.
        if startnode:
            if startnode == endpoints[0] or startnode == endpoints[1]:
                begin_node = startnode
            else:
                raise SequenceError(
                    "Start node not found in sequence set.")
        else:
            begin_node = endpoints[0] # Arbitrary choice.

    elif len(endpoints)==0: # Loop case.
        if startnode:
            if startnode in adjacency.keys():
                begin_node = startnode
            else:
                raise SequenceError(
                    "Start node not found in sequence loop.")
                
        else:
            begin_node = adjacency.keys()[0]  # Again, arbitrary.
    else:
        # We reach this point if the number of nodes with only one
        # corresponding segment in the passed-in set is not 0 or 2.
        # This could happen for disjoint segments that don't link up
        # properly.
        raise SequenceError(
            "Disjoint segments in segment-set, unable to sequence.")


    # Build the correctly-sequenced list now.
    seg_sequence = []
    node_sequence = [begin_node]
    winding_vector = [0,0]

    # The case where we begin with a node that is on a periodic
    # boundary but the first segment is across the boundary is
    # confusing, so we simply reverse the list of segments in the
    # adjacency dict for the starting node
    for partner in begin_node.getPartners():
        if partner in adjacency.keys():
            seg = adjacency[begin_node][0]
            if begin_node not in seg.get_nodes():
                adjacency[begin_node].reverse()

    while len( adjacency[node_sequence[-1]] ) > 0:

        seg = adjacency[node_sequence[-1]][0]
        seg_sequence.append(seg)
        adjacency[node_sequence[-1]].remove(seg)
        # in case we've just crossed a periodic boundary, we must
        # remove the seg from the partner on the other side  
        for partner in node_sequence[-1].getPartners():
            if partner in adjacency.keys():
                adjacency[partner].remove(seg)
        node_sequence.append(seg.get_other_node(node_sequence[-1]))
        adjacency[node_sequence[-1]].remove(seg)

        # cross the periodic boundary.
        for partner in node_sequence[-1].getPartners():
            if partner in adjacency.keys():
                setWindingVector(node_sequence[-1], partner, winding_vector)
                node_sequence.append(partner)
                adjacency[partner].remove(seg)

    # Could remove used-up lists from the dict, then this check
    # is for any remaining entries.
    # Check completeness -- leftovers indicate an overlooked loop.
    for v in adjacency.values():
        if len(v)!=0:
            raise SequenceError(
                "Disconnected loop in segment set, unable to sequence.")

    return (seg_sequence, node_sequence, winding_vector)

def setWindingVector(node, partner, winding_vector):
    ppos = partner.position()
    npos = node.position()
    if ppos[0] > npos[0]:
        winding_vector[0] -= 1
    if ppos[0] < npos[0]:
        winding_vector[0] += 1
    if ppos[1] > npos[1]:
        winding_vector[1] -= 1
    if ppos[1] < npos[1]:
        winding_vector[1] += 1
        

# Utility function to find a path from the indicated start node to the
# indicated end node in the provided set of segments.  Returns a list
# of sequenced paths.  All of the returned paths begin at the
# indicated start point, end at the indicated end point, and do not
# repeat any segments.  They are not guaranteed to be monotonic, they
# may self-intersect, and, since all paths are returned, obviously
# they're not minimal, in general.
def segPath(start, end, segments):
    # Easy case first.
    if len(segments)==0:
        return []

    # Next easiest case -- a single segment.
    if len(segments)==1:
        n = segments[0].get_nodes()
        if (start in n) and (end in n):
            return [segments]
        else:
            return []

    # We could call segSequence at this point, which would throw an
    # exception if the segments were not a ring or a line, and thus
    # identify the path-is-obviously-unique case, but the amount of
    # effort involved is almost the same as doing the all-paths
    # construction, so we just go ahead and do that.

    # Connectivity dictionary.
    connect = {}
    for s in segments:
        n = s.get_nodes()
        try:
            connect[n[0]].append(s)
        except KeyError:
            connect[n[0]] = [s]

        try:
            connect[n[1]].append(s)
        except KeyError:
            connect[n[1]] = [s]

    # Call a helper function to recursively traverse the paths.
    return segPathFind(start, end, connect, [])


# The helper function "segPathFind" modifies the dictionary, and is
# recursive.  Return value is always a list of lists of sequenced
# segments, although this list can be empty.
def segPathFind(n1, n_target, connect, current_path):

    # Success -- if n1 is n_target, the current path is valid, return it.
    if n1==n_target:
        return [current_path]

    # If the node is not present in the dictionary, or its list
    # is of length zero, return an empty path.
    try:
        lst = connect[n1]
    except KeyError:
        return []
    else:
        if len(lst)==0:
            return []
        
    # Next-most-trivial case -- unique extension to the current path.
    if len(connect[n1])==1:
        seg = connect[n1][0]

        current_path.append(seg)
        connect[n1].remove(seg)
        # Find the other node of the segment.
        n2 = seg.get_other_node(n1)

        # Remove the other instance of the segment.
        connect[n2].remove(seg)
        # Recurse.
        return segPathFind(n2, n_target, connect, current_path)

    # Hard case -- more than one way to go at this junction.
    # Do all of them.
    seg_list = connect[n1]
    
    path_list = []
    for seg in seg_list:
        n2 = seg.get_other_node(n1)

        # Copy the dictionary.
        new_connect = {}
        for (k,v) in connect.items():
            new_connect[k]=v[:]

        # Copy the path.
        new_path = current_path[:]

        new_connect[n1].remove(seg)
        new_connect[n2].remove(seg)
        new_path.append(seg)

        path_list += segPathFind(n2, n_target, new_connect, new_path)


    return path_list



##############################

# A SkeletonEdge is a directed SkeletonSegment.  "Direction" is
# plus or minus, indicating either the same or opposite to the
# canonical ordering of the segment.
class SkeletonEdge:
    def __init__(self, segment, direction=1):
        self.segment = segment
        self.segment.edges.append(self)
        self.direction = direction

    # Useful but slow to be able to set the direction from an ordered
    # set of nodes.
    def set_direction(self, n1, n2):
        nodes = self.segment.nodes()
        if nodes[0]==n1 and nodes[1]==n2:
            self.direction = 1
        elif nodes[0]==n2 and nodes[1]==n1:
            self.direction = -1
        else:
            raise ooferror.ErrPyProgrammingError(
                "Incorrect node set in SkeletonEdge.")
    def reverse(self):
        self.direction *= -1

    if config.dimension() == 3:
        def getVtkLine(self):
            return self.segment.getVtkLine()

    # Retrieve the nodes in the correct order.  Used for drawing.
    def get_nodes(self):
        nodes = self.segment.nodes()
        if self.direction==1:
            return [nodes[0], nodes[1]]
        else:
            return [nodes[1], nodes[0]]

    #Interface branch
    #Get the left element if it exists.
    #Otherwise return the only element.
    def getLeftElement(self):
        els=self.segment.getElements()
        if len(els)<2:
            return els[0]
        if els[0].nodesInOrder(*self.get_nodes()):
            return els[0]
        else:
            return els[1]

    def get_other_node(self, node):
        return self.segment.get_other_node(node)
        
    # Remove yourself from your segment's edge list.
    def remove(self): 
        self.segment.edges.remove(self)

    # Function to assist with propagating boundaries.

    # This function returns a list of edges with the properties that:
    #  - The child list edges trace a path from this edge's start node
    #                      to this edge's stop node.
    #  - The child edge's segments are children of this edge's segment.
    #  - The edges are directed correctly from start to finish.
    def edgesFromSegs(self, child_segs):
        if len(child_segs)==0:
            return []
    
        # If the child segments are forked or otherwise complex,
        # return an empty list.
        try:
            (seg_list, node_list, winding) = segSequence( child_segs )
        except SequenceError:
            return []
    
        ordered_nodes = self.get_nodes()
        #debug.fmsg('ordered_nodes=', ordered_nodes)
        #debug.fmsg('ordered_nodes[0].getChildren()=', ordered_nodes[0].getChildren())
        #debug.fmsg('node_list=', node_list)
        if ordered_nodes[0].getChildren()[0] == node_list[0]: # Forward.
            pass
        elif ordered_nodes[0].getChildren()[0] == node_list[-1]:
            seg_list.reverse()
            node_list.reverse()
        else:
            raise ooferror.ErrPyProgrammingError(
                "Malformed segment sequence -- node child not found.")
    
        child_list = []
        for (s, n)  in map(None, seg_list, node_list[:-1]):
            if s.nodes()[0]==n:
                child_list.append(SkeletonEdge(s,direction=1))
            else:
                child_list.append(SkeletonEdge(s,direction=-1))
            
        return child_list

utils.OOFdefine('SkeletonEdge', SkeletonEdge)
