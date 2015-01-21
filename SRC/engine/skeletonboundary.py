# -*- python -*-
# $RCSfile: skeletonboundary.py,v $
# $Revision: 1.88.2.39 $
# $Author: langer $
# $Date: 2014/08/23 15:53:31 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# This is the SkeletonContext-level object that represents a boundary.
# It has methods allowing the boundary to be propagated throughout the
# context's stack.  It is not, itself, a boundary, i.e. it has no
# edges of its own.  The "boundaryset" dictionary contains weak
# references to all the boundaries in the context which have the name.

# TODO 3.1: Skeleton boundaries only have limited editability at
# present -- one has to construct a selection of nodes or segments,
# and then delete the segments from the boundary.  Eventually, we'd
# like to have more direct editabilty, probably from a toolbox, where
# boundary components can be added or removed in one step by clicking
# on them.

# TODO MER: Can the functions try_appendXXX, try_removeXXX, appendXXX, and
# removeXXX be made generic, instead of having a version for each type
# of boundary?  Also in SkelContextBoundary subclasses and in
# SkeletonContext.appendXXXToBdy, etc.


from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.SWIG.engine import cskeletonselectable
from ooflib.common import debug

import math
import weakref

class SkelContextBoundary:
    def __init__(self, skelcontext, name, skeleton=None, boundary=None):
        self.skelcontext = skelcontext
        self.name = name
        self.boundaryset = weakref.WeakKeyDictionary()
        if skeleton is None:
            skeleton = skelcontext.getObject()

        if boundary:
            # DeputySkeletons don't have independent boundary
            # information, so all data has to be associated with the
            # sheriff skeleton.  See comments for resolveCSkeleton in
            # skeletoncontext.py.
            key = self.skelcontext.resolveCSkeleton(skeleton.sheriffSkeleton())
            self.boundaryset[key] = boundary

        ## TODO 3.1: Is this timestamp still needed?  It's set in many
        ## places here, but its value isn't used.  Is it used
        ## elsewhere?
        self.timestamp = timestamp.TimeStamp()

    def getBoundarySet(self, skeleton):
        return self.boundaryset[self.skelcontext.resolveCSkeleton(
                skeleton.sheriffSkeleton())]

    def size(self, skeleton):
        return self.boundary(skeleton).size()

    def boundary(self, skeleton):
        try:
            return self.boundaryset[
                self.skelcontext.resolveCSkeleton(skeleton.sheriffSkeleton())]
        except KeyError:        # TODO 3.1: Is this still necessary?
            pass                # temporary kludge

    def current_size(self):
        skel = self.skelcontext.getObject()
        return self.size(skel)

    def current_boundary(self):
        skel = self.skelcontext.getObject()
        return self.boundary(skel)
    
    def rename(self, newname):
        for skeleton in self.boundaryset:
            skeleton.renameBoundary(self.name, newname)
        self.name = newname

    # Removal function -- if a skeleton is specified, remove the
    # corresponding SkeletonBoundary from the skeleton.  Otherwise, do
    # it for all of them.  If a deputy skeleton is specified, this
    # fails.
    def remove(self, skeleton=None):
        if skeleton:
            self.boundaryset[skeleton].remove()
            del self.boundaryset[skeleton]
            skeleton.removeBoundary(self.name)
        else:
            for b in self.boundaryset.values():
                b.remove()
            for k in self.boundaryset:
                k.removeBoundary(self.name)
            self.boundaryset.clear()
        if len(self.boundaryset) == 0:
            del self.skelcontext

    # This doesn't have a meaning for point boundaries, but the
    # procedure is shared between face and edge boundaries, so it goes
    # here.  TODO MER: Should there be an intermediate OrientableBoundary
    # class for face and edge boundaries, so that reverse doesn't have
    # to be defined for point boundaries?  Or is that adding too much
    # extra complication just to make a small pedantic point?
    def reverse(self):
        # omar = self.skelcontext.getObject().sheriffSkeleton()
        # skelbdy = self.boundaryset[omar]
        skelbdy = self.current_boundary()
        skelbdy.reverse()
        self.timestamp.increment()

    # This calls the right C++ class, which does the heavy lifting.
    def map(self, skeleton, new_skeleton,
            direction=cskeletonselectable.MAP_DOWN, exterior=False, local=True):
        old_bdy = self.boundaryset[skeleton]
        new_bdy = old_bdy.map(new_skeleton, direction, exterior)
        if local:
            self.boundaryset[new_skeleton] = new_bdy

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkelContextFaceBoundary(SkelContextBoundary):
    def __init__(self, context, name, skeleton=None, boundary=None):
        SkelContextBoundary.__init__(self, context, name,
                                     skeleton, boundary)
        #Interface branch
        #self._interfacematerial=None
    def boundaryType(self):
        return "face"

    # draw() is called by SelectedSkeletonBoundaryDisplay.draw(),
    # which is only used in the 2D version.  After the 3D merge, when
    # 2D graphics is done in vtk, it won't be used at all.
    def draw(self, displaylayer, gfxwindow, device, skeleton): # 2D only
        displaylayer.drawFaceBoundary(self, skeleton, gfxwindow, device)

    def buildDisplayLayer(self, bdydisplay, skeleton, canvaslayer):
        bdydisplay.buildFaceLayer(self, skeleton, canvaslayer)

    def try_appendFaces(self, faces):
        skelbdy = self.current_boundary()
        return skelbdy.try_appendFaces(self.skelcontext.getObject(), faces)

    def appendFaces(self, faces):
        skelbdy = self.current_boundary()
        skelbdy.appendFaces(self.skelcontext.getObject(), faces)
        self.timestamp.increment()

    def try_removeFaces(self, faces):
        skelbdy = self.current_boundary()
        return skelbdy.try_removeFaces(self.skelcontext.getObject(), faces)

    def removeFaces(self, faces):
        skelbdy = self.current_boundary()
        skelbdy.removeFaces(self.skelcontext.getObject(), faces)
        self.timestamp.increment()
 
class ExteriorSkelContextFaceBoundary(SkelContextFaceBoundary):
    def map(self, skeleton, new_skeleton,
            direction=cskeletonselectable.MAP_DOWN, local=True):
        SkelContextFaceBoundary.map(self, skeleton, new_skeleton,
                                     direction=direction,
                                     local=local, exterior=1)
        # if debug.debug():
        #     old_bdy = self.boundaryset[skeleton]
        #     new_bdy = self.boundaryset[new_skeleton]
        #     a1 = old_bdy.area()
        #     a2 = new_bdy.area()
        #     if math.fabs(a1-a2)/a1 > 0.00001:
        #         raise ooferror.ErrPyProgrammingError(
        #             "Face boundary area mismatch: %g != %g (%g)" %
        #             (a1, a2, (a1-a2)/a1))
    def try_appendFaces(self, faces):
        if not self.skelcontext.getObject().checkExteriorFaces(faces):
            return False
        return SkelContextFaceBoundary.try_appendFaces(self, faces)
            
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkelContextEdgeBoundary(SkelContextBoundary):
    def __init__(self, context, name, skeleton=None, boundary=None):
        SkelContextBoundary.__init__(self, context, name,
                                     skeleton, boundary)
        #Interface branch
        self._interfacematerial=None

    #Interface branch
#     def sequenceableflag(self, skeleton):
#         try:
#             return self.boundaryset[skeleton.sheriffSkeleton()]._sequenceable
#         except KeyError:
#             return 1

    def boundaryType(self):
        return "edge"

    # Addition of new segments.  The added segments and nodes are
    # from the current .obj of self.skelcontext.  They're actually
    # added to the sheriff of the current object of the current
    # context.
    def appendSegs(self, segments):
        skelbdy = self.current_boundary()
        skelbdy.appendSegs(segments)
        self.timestamp.increment()

    # Trial versions of the above -- these make no changes, they just
    # check if the result will be legal.
    def try_appendSegs(self, segments):
        skelbdy = self.current_boundary()
        return skelbdy.try_appendSegs(segments)

    # Deletion, also operates on the sheriff. (overridden for point
    # boundaries.)  It's called "removeSegs" because "delete" is a
    # reserved word in C++ and using swig to change the name would
    # just be confusing.
    def removeSegs(self, segments):
        skelbdy = self.current_boundary()
        skelbdy.removeSegs(segments)
        self.timestamp.increment()

    def try_removeSegs(self,segments):
        skelbdy = self.current_boundary()

        ## TODO 3.1: The following seems like a good idea, even not on the
        ## interface branch.  Can it be done without changing the
        ## structure of the CSkeletonEdgeBoundary class?  It currently
        ## holds a list of oriented segments.  If the boundary is
        ## allowed to be (temporarily) unsequenceable, does it make
        ## sense for the segments to be oriented?
        # #Interface branch
        # #The delete/remove operation should always work for
        # #a boundary that is originally non-sequenceable.
        # #Can almost do the same for try_append above, but
        # #the segments that are to be added do not carry
        # #orientation information.
        # if skelbdy._sequenceable==0:
        #     return 1
        return skelbdy.try_removeSegs(segments)



## TODO OPT: The C++ version of this routine (CSkeletonEdgeBoundary::map)
## contains a comment "This is a simplified translation of the python
## routine.  Update if necessary."  Don't delete this commented-out
## block until that's been checked.
#    # Propagate a boundary up to its parent or down to its child.
#    # Caller must ensure that the skeleton passed through as
#    # "new_skeleton" in fact contains the appropriately-related
#    # segments (parents for MAP_UP, children for MAP_DOWN) with
#    # respect to first skeleton.  Caller is also responsible for
#    # issuing the "new_boundaries" signal.
#     def map(self, skeleton, new_skeleton,
#             direction=MAP_DOWN, exterior=None, local=1):
#         old_bdy = self.boundaryset[skeleton]
#         new_bdy = old_bdy.map(new_skeleton, direction, exterior)
#         if local:
#             self.boundaryset[new_skeleton] = new_bdy

#         old_bdy = self.boundaryset[skeleton]
        
#         #Interface branch (reverting for now)
# #         if old_bdy._sequenceable==1: # TODO OPT: use a boolean
# #             new_bdy = new_skeleton.makeEdgeBoundary(
# #                 self.name, exterior=exterior)
# #         else:
# #             new_bdy = new_skeleton.makeNonsequenceableEdgeBoundary(
# #                 self.name, exterior=exterior)

#         new_bdy = new_skeleton.makeEdgeBoundary(self.name, [], None, exterior)

#         if local:
#             self.boundaryset[new_skeleton] = new_bdy

#         #TODO 3.1: Interface branch. Should this be modified to handle
#         #non-sequenceable segments? Gut feeling is it already does.
        
#         # Deduce the corresponding edges in the new mesh.
#         old_edges = old_bdy.getSegments()
#         print old_edges
#         while len(old_edges) > 0:
#             # Start from the back, so list removal is efficient.
#             e = old_edges[-1]
            
#             if direction==MAP_DOWN:
#                 m = e.get_segment().map()
#                 map_start = m.source
#                 map_end = m.target
#             else: # direction==MAP_UP
#                 if len(e.get_segment().getParents())==0:
#                     del old_edges[-1]
#                     continue
#                 m = e.get_segment().getParents()[0].map()
#                 map_start = m.target
#                 map_end = m.source
                

#             if len(map_start)==1:
#                 # One-to-many case -- Sequence and edge-ify.
#                 new_eset = edgesFromSegs(e, map_end, direction)
#                 for e in new_eset:
#                     new_bdy.addEdge(e)
#                 del old_edges[-1]
#             else:
#                 # Many-to-one or many-to-many case.
#                 # First, find all the edges of this bdy in the parent part.
#                 source_eset = [e]
#                 for seg in map_start:
#                     for edg in seg.edges:
#                         if edg in old_edges:
#                             if edg not in source_eset:
#                                 source_eset.append(edg)

#                 # Remove them from the old-edge list.
#                 for e in source_eset:
#                     del old_edges[-1]
                                
#                 # Sequence the source edges -- this is the path the
#                 # original boundary takes through the source part
#                 # of the map.
#                 try:
#                     (edge_seq, node_seq, winding) = skeletonsegment.segSequence(
#                         source_eset)
#                 except skeletonsegment.SequenceError:
#                     continue # Re-enter the while loop.
                
#                 # Direct the resulting edge-sequence correctly.  Edges
#                 # always return their nodes in order.
#                 if node_seq[0]!=edge_seq[0].get_nodes()[0]:
#                     edge_seq.reverse()
#                     node_seq.reverse()
                    
#                 # Extract the subset of the target that has some
#                 # relation to the boundary part of the parent.
#                 sub_target = []
#                 for e in edge_seq:
#                     if direction==MAP_DOWN:
#                         for c in e.get_segment().getChildren():
#                             if c not in sub_target:
#                                 sub_target.append(c)
#                     else: # direction==MAP_UP:
#                         for p in e.get_segment().getParents():
#                             if p not in sub_target:
#                                 sub_target.append(p)

#                 # Exterior check -- for the exterior case, the only
#                 # valid target segments are those which have exactly one
#                 # element.
#                 if exterior:
#                     narrow_target = []
#                     for s in sub_target:
#                         if s.nElements()==1:
#                             narrow_target.append(s)
#                     sub_target = narrow_target
                        
#                 # Find the counterparts of the endpoints of the path, if
#                 # they exist and are unique, otherwise fail.
#                 if direction==MAP_DOWN:
#                     start_shadow = node_seq[0].getChildren()
#                     end_shadow = node_seq[-1].getChildren()
#                 else:
#                     start_shadow = node_seq[0].getParents()
#                     end_shadow = node_seq[-1].getParents()

#                 if len(start_shadow)==1:
#                     target_start = start_shadow[0]
#                 else:
#                     continue


#                 if len(end_shadow)==1:
#                     target_end = end_shadow[0]
#                 else:
#                     continue

#                 # If the points are not distinct, fail.
#                 if target_start == target_end:
#                     continue
                
#                 # Find the paths in the target subset segment set from
#                 # the start node to the end node.  The returned path
#                 # is sequenced.
#                 path_set = skeletonsegment.segPath(
#                     target_start, target_end, sub_target)

#                 # If the path is not unique, fail.
#                 if len(path_set)!=1:
#                     continue

#                 # Success!  We have a single unique sequenced set of
#                 # segments from child_start to child_end.  Convert
#                 # them to edges and add them to the boundary.
#                 n1 = target_start
#                 for seg in path_set[0]:
#                     nodes = seg.get_nodes()
#                     if nodes[0]==n1:
#                         e = skeletonsegment.SkeletonEdge(seg, direction=1)
#                         n2 = nodes[1]
#                     else:
#                         e = skeletonsegment.SkeletonEdge(seg, direction=-1)
#                         n2 = nodes[0]
#                     new_bdy.addEdge(e)
#                     n1 = n2 # Reset n1 for next iteration.
                                
    # draw() is called by SelectedSkeletonBoundaryDisplay.draw(),
    # which is only used in the 2D version.  After the 3D merge, when
    # 2D graphics is done in vtk, it won't be used at all.
    def draw(self, displaylayer, gfxwindow, device, skeleton):
        displaylayer.drawEdgeBoundary(self, skeleton, gfxwindow, device)

    def buildDisplayLayer(self, bdydisplay, skeleton, canvaslayer):
        bdydisplay.buildEdgeLayer(self, skeleton, canvaslayer)
    
class ExteriorSkelContextEdgeBoundary(SkelContextEdgeBoundary):
    # Exterior version needs to restrict itself to new segments which
    # have only one element (or faces with only one element in 3D).
    # Set the flag in the base class and call it.
    def map(self, skeleton, new_skeleton, 
            direction=cskeletonselectable.MAP_DOWN, local=True):
        SkelContextEdgeBoundary.map(self, skeleton, new_skeleton,
                                    direction=direction,
                                    local=local, exterior=1)

    def try_appendSegs(self, segments):
        if not self.skelcontext.getObject().checkExteriorSegments(segments):
            return False
        return SkelContextEdgeBoundary.try_appendSegs(self, segments)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
            
class SkelContextPointBoundary(SkelContextBoundary):
    def __init__(self, context, name, skeleton=None, boundary=None):
        SkelContextBoundary.__init__(self, context, name,
                                     skeleton, boundary)
    def boundaryType(self):
        return "node"

    def appendNodes(self, nodes):
        skelbdy = self.boundaryset[self.skelcontext.getObject()]
        skelbdy.appendNodes(list(nodes))
        self.timestamp.increment()

    def removeNodes(self, nodes):
        skelbdy = self.boundaryset[self.skelcontext.getObject()]
        skelbdy.removeNodes(nodes)
        self.timestamp.increment()

    def reverse(self):
        pass
            
    # draw() is called by SelectedSkeletonBoundaryDisplay.draw(),
    # which is only used in the 2D version.  After the 3D merge, when
    # 2D graphics is done in vtk, it won't be used at all.
    def draw(self, displaylayer, gfxwindow, device, skeleton):
        displaylayer.drawPointBoundary(self, skeleton, gfxwindow, device)

    def buildDisplayLayer(self, bdydisplay, skeleton, canvaslayer):
        bdydisplay.buildPointLayer(self, skeleton, canvaslayer)
    
class ExteriorSkelContextPointBoundary(SkelContextPointBoundary):
    def map(self, skeleton, new_skeleton, 
            direction=cskeletonselectable.MAP_DOWN, local=True):
        SkelContextPointBoundary.map(self, skeleton, new_skeleton,
                                     direction=direction,
                                     local=local, exterior=1)
        
# class SkeletonEdgeBoundary: # corresponds to a realskeleton's EdgeBoundary
#     def __init__(self, name):
#         self._name = name
#         self.edges = []
        
#         #Interface branch
#         self._sequenceable=1

#     def size(self):
#         return len(self.edges)
#     def addEdge(self, edge):
#         self.edges.append(edge)

#     # This routine removes all the edges from their associated segments.
#     # It should be called at boundary-deletion time. 
#     def remove(self):
#         for e in self.edges:
#             e.remove()
#         self.edges = []


#     # Function for ensuring that the "self.edges" list is in the
#     # correct order, and proceeds from start to finish.  Should work
#     # in such a way that it's very fast if the boundary is already
#     # sequenced.
#     def sequence(self):
#         #Interface branch
#         if self._sequenceable==0:
#             return

#         if len(self.edges)==0 or len(self.edges)==1:
#             return
#         for i in range(len(self.edges)-1):
#             if self.edges[i].get_nodes()[1]!=self.edges[i+1].get_nodes()[0]:
#                 break
#         else:
#             return

#         # Edges are not correctly sequenced.  Do it here, remembering
#         # that nodes within edges are already ordered.
#         ndict = {}
#         startnodes = []
#         endnodes = []
#         for e in self.edges:
#             startnode = e.get_nodes()[0]
#             try:
#                 ndict[startnode]
#             except KeyError:
#                 ndict[startnode]=e
#                 startnodes.append(startnode)
#                 endnodes.append(e.get_nodes()[1])
#             else:
#                 raise skeletonsegment.SequenceError(
#                     "Cannot sequence boundary %s" % `self._name`)

#         # At this point, you have a list of start nodes, a list of end
#         # nodes, and a dictionary of edges keyed by start node.

#         # Topology check -- eliminate start nodes with corresponding
#         # end nodes, and look at the sizes of the remainder lists --
#         # they must be equal, and if they're both 1, it's a line, if
#         # they're 0, it's a loop, otherwise it's an error.
#         unmatchedendnodes = []
#         for e in endnodes:
#             try:
#                 startnodes.remove(e)
#             except ValueError:
#                 unmatchedendnodes.append(e)

#         if len(unmatchedendnodes)==1 and len(startnodes)==1:
#             # Straightforward case.
#             sequence_node = startnodes[0]
#         elif len(unmatchedendnodes)==0 and len(startnodes)==0:
#             # Loop case.  Doesn't matter where you start.
#             sequence_node = self.edges[0].get_nodes()[0]
#         else:
#             raise skeletonsegment.SequenceError(
#                 "Topology problem with boundary %s, unable to sequence." % `self._name`)

#         # Now, finally, we have a starting node.  Chain the edges
#         # together from this node.  Proceed until dictionary retrieval
#         # on the next node fails.

#         # This really wants to be a "do...while" loop, but Python
#         # doesn't offer this construction.
#         newedgelist = []
#         while 1:
#             try:
#                 edge = ndict[sequence_node]
#             except KeyError:
#                 break
#             else:
#                 newedgelist.append(edge)
#                 sequence_node = edge.get_nodes()[1]

#         if len(newedgelist)==len(self.edges):
#             self.edges = newedgelist
#         else:
#             # This can occur if the boundary is made up of disjoint loops.
#             raise skeletonsegment.SequenceError(
#                 "Sequenced boundary %s did not use all edges." % `self._name`)
        
#     def reverse(self):
#         self.edges.reverse()            # reverses list in place
#         for edge in self.edges:
#             edge.reverse()

#     # Double dispatch, returns the right type of context object.
#     def makeContextBoundary(self, context, name, skeleton):
#         return SkelContextEdgeBoundary(context, name, skeleton, self)

#     # Determine if the proposed append operation will leave this
#     # boundary legal.  Do not actually modify the boundary.  Used by
#     # widgets to determine the legality of operations.
#     #
#     # TODO OPT: In the legal case, this should cache the
#     # results, and, if the cache remains valid, the "append" operation
#     # should not repeat the computation.  Through the GUI, any call to
#     # append will be immediately preceded by a call to try_append from
#     # the widget, so cache invalidation doesn't occur until after the
#     # append call completes.  This is not true in script mode or from
#     # the console, but since the skeleton boundary modify dialog box
#     # is modal, the cache can be invalidated whenever that box is
#     # closed.
#     def try_append(self, new_segments):
#         if len(self.edges)==0:
#             return 0
#         self.sequence()
        
#         all_segments = new_segments.union([x.segment for x in self.edges])

#         try:
#             (seg_list, node_list, winding) = skeletonsegment.segSequence(all_segments)
#             return 1
#         except skeletonsegment.SequenceError:
#             return 0
        
#     # Add the indicated segments to this boundary.  They are
#     # not sequenced, and may be disjoint, although the resulting
#     # boundary should not be disjoint, self-intersecting, or otherwise
#     # weird.  We are responsible for calling "sequence", and must
#     # ensure that exceptional conditions do not alter the boundary.
#     def append(self, new_segments):

#         if len(self.edges)==0:
#             raise ooferror.ErrUserError(
#                 "Cannot append to an empty boundary.")
        
#         self.sequence()  # Make sure we're in order, first.  
#         all_segments = new_segments.union([x.segment for x in self.edges])

#         (seg_list, node_list, winding) = skeletonsegment.segSequence(all_segments)

#         # Explicitly check for the loop case -- if it occurs, the
#         # seg_list needs to be "manually" brought into correspondence
#         # with the current edge list, otherwise the following code can
#         # be confused by the wrap-around and fail to add the new
#         # segments.
#         if node_list[0]==node_list[-1]:
#             # First, check orientation -- only meaningful if there was
#             # more than one edge to begin with.
#             if len(self.edges)>1:
#                 s0_idx = seg_list.index(self.edges[0].segment)
#                 s1_idx = seg_list.index(self.edges[1].segment)
#                 # If s1 is the successor of s0, mod the length, it's OK.
#                 if ((s0_idx+1) % len(seg_list)) != s1_idx:
#                     seg_list.reverse()
                    
#             # Now rotate the seg_list so that self.edges[0].segment
#             # is at the beginning.
#             s0_idx = seg_list.index(self.edges[0].segment)
#             seg_list = seg_list[s0_idx:]+seg_list[:s0_idx]

#         # At this point, seg_list is topologically OK -- either it's a
#         # loop starting from s0, or it's a line straight from the
#         # sequencer.  In the latter case, it still might be backwards.
#         s0 = self.edges[0].segment
#         s1 = self.edges[-1].segment

#         # If it is backwards, fix it.
#         if seg_list.index(s0) > seg_list.index(s1):
#             seg_list.reverse()

#         first_original_edge = self.edges[0]
#         last_original_edge = self.edges[-1]
        
#         # Check the front.
#         idx = seg_list.index(s0)
#         if idx!=0: # There are edges to prepend to the front.
#             contact_node = first_original_edge.get_nodes()[0]
#             for jdx in range(idx-1,-1,-1): # Count down to zero.
#                 seg = seg_list[jdx]
#                 nodes = seg.get_nodes()
#                 if nodes[1]==contact_node:
#                     self.addEdge(
#                         skeletonsegment.SkeletonEdge(seg,direction=1))
#                     contact_node = nodes[0]
#                 elif nodes[0]==contact_node:
#                     self.addEdge(
#                         skeletonsegment.SkeletonEdge(seg,direction=-1))
#                     contact_node = nodes[1]
#                 else:
#                     # If there's no place to put the segment, then
#                     # something's gone badly wrong.
#                     raise ooferror.ErrPyProgrammingError(
#                         "No adjacent node for new segment in boundary!")

#         # Now check the back.
#         idx = seg_list.index(s1)
#         if idx<len(seg_list):
#             contact_node = last_original_edge.get_nodes()[1]
#             for jdx in range(idx+1,len(seg_list)):
#                 seg = seg_list[jdx]
#                 nodes = seg.get_nodes()
#                 if nodes[0]==contact_node:
#                     self.addEdge(
#                         skeletonsegment.SkeletonEdge(seg,direction=1))
#                     contact_node = nodes[1]
#                 elif nodes[1]==contact_node:
#                     self.addEdge(
#                         skeletonsegment.SkeletonEdge(seg,direction=-1))
#                     contact_node = nodes[0]
#                 else:
#                     raise ooferror.ErrPyProgrammingError(
#                         "No adjacent node for new segment in boundary!")

#         self.sequence() # Clean up.

        
#     # Determine if the proposed delete operation will leave this
#     # boundary legal.  Do not actually modify the boundary.  Used by
#     # widgets to determine the legality of operations.
#     #  
#     # TODO OPT: See caching comment for try_append, above.
#     def try_delete(self, segments):
#         self.sequence()
#         old_segments =  [x.segment for x in self.edges]

#         index_set = []
#         for s in segments:
#             try:
#                 index_set.append(old_segments.index(s))
#             except ValueError:
#                 pass   # It's ok if s isn't in the boundary.  Just go on.

#         dead_segments = [old_segments[idx] for idx in index_set]
#         for d in dead_segments:
#             old_segments.remove(d)

#         try:
#             (seg_list, node_list, winding) = skeletonsegment.segSequence(old_segments)
#             return 1
#         except skeletonsegment.SequenceError:
#             return 0
        

#     # Make sure all the segments are present in the boundary.  Remove
#     # them, and raise an exception if the resulting boundary cannot
#     # be sequenced.
#     def delete(self, segments):

#         self.sequence()
#         old_segments = [x.segment for x in self.edges]

#         index_set = []
#         for s in segments:
#             try:
#                 index_set.append(old_segments.index(s))
#             except ValueError:
#                 pass   # It's ok if s isn't in the boundary.  Just go on.

#         dead_segments = [old_segments[idx] for idx in index_set]
#         for d in dead_segments:
#             old_segments.remove(d)

#         #Interface branch
#         if self._sequenceable==1:
#             (seg_list, node_list, winding) = skeletonsegment.segSequence(old_segments)

#         # If sequencing worked, then the modified boundary is
#         # topologically OK.  It is permissible to modify our edges list.

#         dead_edges = [self.edges[idx] for idx in index_set]
#         for d in dead_edges:
#             d.remove() # Remove yourself from the segment's list of edges.
#             self.edges.remove(d)

#         self.sequence() # Clean up.
            
#     # temp __repr__ for skeleton save
#     def __repr__(self):
#         return "SkeletonEdgeBoundary("+self._name+")"
    
#     def get_name(self):
#         return self._name

#     def rename(self, newname):
#         self._name = newname

#     def exterior(self):
#         return 0
        
# class ExteriorSkeletonEdgeBoundary(SkeletonEdgeBoundary):
#     def addEdge(self, edge):
#         if config.dimension() == 2 and edge.segment.nElements() != 1:
#             raise ooferror.ErrPyProgrammingError(
#                 "Attempt to insert interior segment in exterior boundary.")
#         self.edges.append(edge)
#     def makeContextBoundary(self, context, name, skeleton):
#         return ExteriorSkelContextEdgeBoundary(context, name, skeleton, self)
#     # temp __repr__ for skeleton save
#     def __repr__(self):
#         return "ExteriorSkeletonEdgeBoundary("+self._name+")"

#     def exterior(self):
#         return 1

# class SkeletonPointBoundary: # corresponds to a realskeleton's NodeSet
#     def __init__(self, name):
#         self._name = name
#         self.nodes = []
#     def size(self):
#         return len(self.nodes)
#     def addNode(self, node):
#         self.nodes.append(node)
    
#     def append(self, nodes):
#         for n in nodes:
#             if n not in self.nodes:
#                 self.addNode(n)

#     def delete(self, nodes):
#         for n in nodes:
#             if n in self.nodes:
#                 self.nodes.remove(n)

#     def remove(self):
#         self.nodes = []
                
#     def has_node(self, node):
#         return node in self.nodes
#     # Double dispatch, to get correct type of context object.
#     def makeContextBoundary(self, context, name, skeleton):
#         return SkelContextPointBoundary(context, name, skeleton, self)
#     # temp __repr__ for skeleton save
#     def __repr__(self):
#         return "SkeletonPointBoundary("+self._name+")"
    
#     def get_name(self):
#         return self._name

#     def rename(self, newname):
#         self._name = newname

#     def exterior(self):
#         return 0
    
# class ExteriorSkeletonPointBoundary(SkeletonPointBoundary):
#     def makeContextBoundary(self, context, name, skeleton):
#         return ExteriorSkelContextPointBoundary(context, name, skeleton, self)
#     # temp __repr__ for skeleton save
#     def __repr__(self):
#         return "ExteriorSkeletonPointBoundary("+self._name+")"

#     def exterior(self):
#         return 1



# # This function returns a list of edges with the properties that:
# #  - The target list edges trace a path from the edge's start node
# #                      to the edge's stop node.
# #  - The target edge's segments are related (parents if
# #                      direction is up, children if direction
# #                      is down) to the edge's segment.
# #  - The new edges are directed correctly from start to finish.
# def edgesFromSegs(edge, target_segs, direction):
#     if len(target_segs)==0:
#         return []
    
#     # If the target segments are forked or otherwise complex,
#     # return an empty list.
#     try:
#         (seg_list, node_list, winding) = skeletonsegment.segSequence( target_segs )
#     except skeletonsegment.SequenceError:
#         return []
    
#     ordered_nodes = edge.get_nodes()

#     if direction==MAP_UP:
#         target_start = ordered_nodes[0].getParents()
#     else: # direction==MAP_DOWN
#         target_start = ordered_nodes[0].getChildren()
#         # the problem is that target_start is not in the "target"

#     if node_list[0] in target_start:
#         pass
#     elif node_list[-1] in target_start:
#         seg_list.reverse()
#         node_list.reverse()
#     else:
#         # In cases of boundaries that are loops, when no starting node
#         # is passed in, segSequence makes an arbitrary choice for the
#         # starting node that can be incorrect, but otherwise sequences
#         # the boundary correctly.  In this case, we must re-sequence
#         # the list.  The alternative is to pass in a target start to
#         # segSequence and then handle the case where the target start
#         # is not in the node list in there, but that seems more complicated.

#         # calculate overlap between node_list and target_start, this
#         # can be done in one line with python 2.4, eliminating nested if
#         overlap = []
#         for node in node_list:
#             if node in target_start:
#                 overlap.append(node)
        
#         if len(overlap): # elif node_list.intersection(target_start)
#             try:
#                 (seg_list, node_list, winding) = skeletonsegment.segSequence( target_segs, overlap[0] )
#             except skeletonsegment.SequenceError:
#                 return []

#         else:
#             raise ooferror.ErrPyProgrammingError(
#                 "Malformed segment sequence -- node counterpart not found.")
    
#     target_list = []
#     for (s, n)  in map(None, seg_list, node_list[:-1]):
#         # if the node_list constitutes a loop, it will be longer than
#         # needed, producing an extra item in the list returned by map.
#         # We can ignore the extra item in this case.
#         if s is None:
#             pass
#         elif s.nodes()[0]==n:
#             target_list.append(skeletonsegment.SkeletonEdge(s,direction=1))
#         else:
#             target_list.append(skeletonsegment.SkeletonEdge(s,direction=-1))
            
#     return target_list

# from ooflib.common import utils
# utils.OOFdefine('SkeletonEdgeBoundary', SkeletonEdgeBoundary)
# utils.OOFdefine('ExteriorSkeletonEdgeBoundary', ExteriorSkeletonEdgeBoundary)
# utils.OOFdefine('SkeletonPointBoundary', SkeletonPointBoundary)
# utils.OOFdefine('ExteriorSkeletonPointBoundary', ExteriorSkeletonPointBoundary)
