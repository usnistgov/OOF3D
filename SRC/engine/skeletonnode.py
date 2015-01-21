# -*- python -*-
# $RCSfile: skeletonnode.py,v $
# $Revision: 1.78.6.18 $
# $Author: fyc $
# $Date: 2014/08/06 21:41:29 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import config
#from ooflib.SWIG.engine import cskeleton
from ooflib.common import debug
from ooflib.common import object_id
from ooflib.common import parallel_enable
from ooflib.common import primitives
from ooflib.common import ringbuffer
from ooflib.engine import skeletonselectable
from ooflib.SWIG.engine import cskeletonnode2
import weakref

## Everything except PinnedNodeSet and PinnedNodeSelection is
## commented out of this file.  The rest has been moved to C++.

# Most of this code is dimension independent.

# in order to keep the nodes lightweight when moving to c++, we won't
# include an elements -- instead any methods that modify the elements
# can be called through the skeleton

# class SkeletonNode(skeletonselectable.SkeletonSelectable):
# #                   cskeleton.CSkeletonNode):

#     if config.dimension() == 2:
#         def __init__(self, x, y, index):
#             skeletonselectable.SkeletonSelectable.__init__(self, index)
# #            cskeleton.CSkeletonNode.__init__(self, x, y)
#             self.dimIndependentInit(index)

#     elif config.dimension() == 3:
#         def __init__(self, x, y, z, points, index):
#             skeletonselectable.SkeletonSelectable.__init__(self, index)
# #            cskeleton.CSkeletonNode.__init__(self, x, y, z, points, index)
#             self.dimIndependentInit(index)

#         def moveTo(self, point):
#             # TODO MER: 3D this could be cleaned up if the elements were stored in C
#             # See note in cskeleton.C
# #            cskeleton.CSkeletonNode.moveTo(self, point)
#             for element in self._elements:
#                 element.updateVtkCellPoints()

#         def unconstrainedMoveTo(self, point):
#             # TODO MER: 3D this could be cleaned up if the elements were stored in C
#             # See note in cskeleton.C
# #            cskeleton.CSkeletonNode.unconstrainedMoveTo(self, point)
#             for element in self._elements:
#                 element.updateVtkCellPoints()

#         def moveBy(self, delta):
# #            cskeleton.CSkeletonNode.moveBy(self, delta)
#             for element in self._elements:
#                 element.updateVtkCellPoints()
             

#     def dimIndependentInit(self, index):
#         self._elements = []
#         self.ID = object_id.ObjectID()
        
#         # parallel attributes
#         if parallel_enable.enabled():
#             self._owners = []  # only for the initial Skeleton
#             self._shared_with = []  # except me
#             self._remote_index = {}  # procID : remote index
        
#     def __repr__(self):
# ##        p = self.position()
# ##        return "SkeletonNode#%d(%f, %f)" % (self.index, p.x, p.y)
#         return "SkeletonNode(%d)" % self.index

#     def repr_position(self):
#         return self.position()

#     def getIndex(self):
#         return self.index
    
#     def destroy(self, skeleton):
#         skeleton.removeNode(self)
#         self.disconnect()
#         del self._elements

#     def active(self, skeleton):
#         return skeleton.MS.activePoint(self.position())

#     def illegal(self):
#         # A node is illegal if any of its elements are illegal.  This
#         # is used when testing possible node motions, so it's assumed
#         # that the node being tested is the one causing the elements
#         # to be illegal.
#         for element in self._elements:
#             if element.illegal():
#                 return 1
#         return 0

#     def addElement(self, element):
#         self._elements.append(element)

#     def removeElement(self, skeleton, element):
#         self._elements.remove(element)
#         if not self._elements:
#             self.destroy(skeleton)

#     def getPartners(self):
#         return []

#     # TODO 3.1: throw exception?
#     def addPartner(self,node):
#         pass

#     def getPartnerPair(self,node):
#         return None

#     def getDirectedPartner(self, direction):
#         return None
        
#     def aperiodicNeighborElements(self, skeleton):
#         return self._elements

#     def neighborElements(self, skeleton):
#         return self.aperiodicNeighborElements(skeleton)

#     # Two versions of neighborNodes are provided to keep the
#     # interface for SkeletonNode and PeriodicSkeletonNode the same.
#     # Two versions are needed for PeriodicSkeletonNode because in most
#     # contexts we want the neighbors across the boundary, but in
#     # others, such as when drawing rubber band lines, we don't want
#     # the neighbors of the partners.
#     def neighborNodes(self, skeleton):
#         neighborDict = {}
#         for e in self._elements:
#             for nd in e.nodes:
#                 if nd is not self:
#                     if skeleton.findSegment(nd, self) is not None:
#                         neighborDict[nd] = 1
#         return neighborDict.keys()

#     def aperiodicNeighborNodes(self, skeleton):
#         return self.neighborNodes(skeleton)


#     # "Segments for which I am an endpoint."
#     def localSegments(self,skeleton):
#         result = set()
#         for e in self._elements:
#             for nd in e.nodes:
#                 if nd is not self:
#                     s = skeleton.findSegment(nd, self)
#                     if s:
#                         result.add(s)
#         return result           # TODO OPT: Any reason to convert from set to list?

#     # Segments which have only one element.
#     def exteriorSegments(self, skeleton):
#         result = set()
#         for seg in self.localSegments(skeleton):
#             if len(seg.getElements()) == 1:
#                 result.add(seg)
#         return result
        
#     def moveBack(self):
# #        cskeleton.CSkeletonNode.moveBack(self)
#         for el in self._elements:
#             el.revertHomogeneity()
#             if config.dimension() == 3:
#                 el.updateVtkCellPoints()


#     if config.dimension() == 2:        
#         def new_child(self, index):
#             p = self.position()
#             new = self.__class__(p.x, p.y, index)
#             new.copyMobility(self)
#             return new
#     elif config.dimension() == 3:        
#         def new_child(self, index, points):
#             p = self.position()
#             new = self.__class__(p.x, p.y, p.z, points, index)
#             new.copyMobility(self)
#             return new

#     ####################

#     # pin and unpin are analogous to select and deselect in the
#     # SkeletonSelectable class.  They pin and unpin this node and its
#     # children and parents.  The clist and plist args are lists of
#     # trackers corresponding to the children and parents in the
#     # SkeletonContext's stack of skeletons.  Some of those Skeletons
#     # may be DeputySkeletons, which share nodes instead of having
#     # parent/child nodes.  For those Skeletons the tracker is a
#     # DeputyPinnedNodeTracker instead of a PinnedNodeTracker.

#     def pin(self, clist, plist):
#         self.setPinned(1)
#         here = self.position()
#         self.pinDown(clist, here)
#         self.pinUp(plist, here)
#     def pinDown(self, clist, here):
#         if clist[0].nodePosition(self) == here:
#             clist[0].add(self)
#             if len(clist) > 1:
#                 clist[1].pinDown(self, clist[1:], here)
#     def pinUp(self, plist, here):
#         if plist[0].nodePosition(self) == here:
#             plist[0].add(self)
#             if len(plist) > 1:
#                 plist[0].pinUp(self, plist[1:], here)
            
#     def unpin(self, clist, plist):
#         self.setPinned(0)
#         here = self.position()
#         self.unpinDown(clist, here)
#         self.unpinUp(plist, here)
#     def unpinDown(self, clist, here):
#         if clist[0].nodePosition(self) == here:
#             clist[0].remove(self)
#             if len(clist) > 1:
#                 clist[1].unpinDown(self, clist[1:], here)
#     def unpinUp(self, plist, here):
#         if plist[0].nodePosition(self) == here:
#             plist[0].remove(self)
#             if len(plist) > 1:
#                 plist[0].unpinUp(self, plist[1:], here)

#     ##############
                
#     ## dominantPixel returns the category of the pixel under the node.

#     def dominantPixel(self, ms):
#         return ms.categoryFromPoint(self.position())

#     ######## PARALLEL STUFF ########
#     if parallel_enable.enabled():
#         def owners(self):
#             return self._owners

#         def nowners(self):
#             return len(self._owners)

#         def addOwner(self, id):
#             if id not in self._owners:
#                 self._owners.append(id)

#         def master(self):
#             from ooflib.SWIG.common import mpitools
#             _rank = mpitools.Rank()
#             if self.isShared():
#                 if self._shared_with[0] < _rank:
#                     return self._shared_with[0]
#             return _rank

#         def sharesWith(self, id, index):
#             # only when u have a short list!
#             if id not in self._shared_with:
#                 self._shared_with.append(id)
#                 self._shared_with.sort()
#                 self._remote_index[id] = index

#         def sharedWith(self):
#             return self._shared_with

#         def nshared(self):
#             return len(self._shared_with)

#         def remoteIndex(self, id):
#             return self._remote_index[id]

#         def isShared(self):
#             return len(self._shared_with) != 0

#         def isSharedWith(self, id):
#             return (id in self._shared_with)
        
# #######################################################

# class PeriodicSkeletonNode(SkeletonNode):

#     if config.dimension() == 2:
#         def __init__(self, x, y, index=-1):
#             SkeletonNode.__init__(self,x,y,index)
#             self.partners = []
#     elif config.dimension() == 3:
#         def __init__(self, x, y, z=0, index=-1):
#             SkeletonNode.__init__(self,x,y,z,index)
#             self.partners = []

#     def destroy(self, skeleton):
#         self.partners = []
#         SkeletonNode.destroy(self, skeleton)

#     def getPartners(self):
#         return self.partners

#     def addPartner(self, node):
#         if node not in self.partners:
#             self.partners.append(node)
#         if self not in node.partners:
#             node.partners.append(self)

#     # Two versions of neighborNodes are needed for
#     # PeriodicSkeletonNode because in most contexts we want the
#     # neighbors accross the boundary, but in others, such as when
#     # drawing rubber band lines, we don't want the neighbors of the
#     # partners.  Rather than just calling SkeletonNode.neighborNodes
#     # on self and on the partners, we redo everything we do on self
#     # for the partners with the additional condition that the
#     # potential neighbor is neither the self nor the partner node.
#     # This handles pathological cases where neighbors and partners can
#     # overlap.
#     def neighborNodes(self, skeleton):
#         neighborDict = {}
#         for e in self._elements:
#             for nd in e.nodes:
#                 if nd is not self:
#                     if skeleton.findSegment(nd, self) is not None:
#                         neighborDict[nd] = 1

#         for partnerNode in self.getPartners():
#             for e in partnerNode._elements:
#                 for nd in e.nodes:
#                     if nd is not self and nd is not partnerNode:
#                         if skeleton.findSegment(nd, partnerNode) is not None:
#                             neighborDict[nd] = 1

#         return neighborDict.keys()

#     def aperiodicNeighborNodes(self, skeleton):
#         return SkeletonNode.neighborNodes(self, skeleton)
 
# <<<<<<< skeletonnode.py
#     # the function being overridden is in the skeletonselectable class
#     def makeSibling(self, newcomer):
#         SkeletonNode.makeSibling(self, newcomer)
#         partners = self.getPartnerPair(newcomer)
#         if partners is not None:
#             SkeletonNode.makeSibling(partners[0], partners[1])


#     # TODO MER: Will need to make this work in 3D

#     # given two nodes (self & node), getPartnerPair returns their
#     # partners with the same periodicity.  That is, if self has a
#     # partner in the +x direction and node has partners in both +x and
#     # -y, then the +x partners of both are returned.
#     def getPartnerPair(self,node):
#         # better criterion than position?
#         partner1 = None
#         partner2 = None
#         # This node can only be a partner of another node if the other
#         # node is different, but has the same x or y position, or both.
#         if self == node or node.getPartners() == [] or \
#            (self.position().x != node.position().x and
#             self.position().y != node.position().y):
#             return None
#         if len(self.getPartners()) == 1:
#             partner1 = self.getPartners()[0]
#         else:
#             partner1 = self.getCorrectPartner(node)
#         if len(node.getPartners()) == 1:
#             partner2 = node.getPartners()[0]
#         else:
#             partner2 = node.getCorrectPartner(self)

#         if partner1 is None or partner2 is None:
#             return None
#         else:
#             return partner1, partner2
# =======
#     # the function being overridden is in the skeletonselectable class
#     def makeSibling(self, newcomer):
#         SkeletonNode.makeSibling(self, newcomer)
#         partners = self.getPartnerPair(newcomer)
#         if partners is not None:
#             SkeletonNode.makeSibling(partners[0], partners[1])


#     # TODO MER: Will need to make this work in 3D

#     # given two nodes (self & node), getPartnerPair returns their
#     # partners with the same periodicity.  That is, if self has a
#     # partner in the +x direction and node has partners in both +x and
#     # -y, then the +x partners of both are returned.
#     def getPartnerPair(self,node):
#         # better criterion than position?
#         partner1 = None
#         partner2 = None
#         # This node can only be a partner of another node if the other
#         # node is different, but has the same x or y position, or both.
#         if self == node or node.getPartners() == [] or \
#            (self.position().x != node.position().x and
#             self.position().y != node.position().y):
#             return None
#         if len(self.getPartners()) == 1:
#             partner1 = self.getPartners()[0]
#         else:
#             partner1 = self.getCorrectPartner(node)
#         if len(node.getPartners()) == 1:
#             partner2 = node.getPartners()[0]
#         else:
#             partner2 = node.getCorrectPartner(self)

#         if partner1 == None or partner2 == None:
#             return None
#         else:
#             return partner1, partner2
#>>>>>>> 1.77.2.3
        
#     # helper function for getPartnerPair used in cases where self
#     # has more than one partner (corner node)
#     def getCorrectPartner(self, node):
#         if self.position().x == node.position().x:
#             for p in self.getPartners():
#                 if p.position().x != self.position().x and \
#                    p.position().y == self.position().y:
#                     return p
        
#         if self.position().y == node.position().y:
#             for p in self.getPartners():
#                 if p.position().y != self.position().y and \
#                    p.position().x == self.position().x:
#                     return p
            
#     def __repr__(self):
#         return "PeriodicSkeletonNode(%d)" % self.index

#     def getDirectedPartner(self, direction):
#         if direction == 'x':
#             for p in self.getPartners():
#                 if p.position().y == self.position().y:
#                     return p
#         elif direction == 'y':
#             for p in self.getPartners():
#                 if p.position().x == self.position().x:
#                     return p

#     # TODO 3.1: Is the skeleton parameter necessary?
#     def neighborElements(self, skeleton):
#         nbrs = self.aperiodicNeighborElements(skeleton)[:]
#         for p in self.getPartners():
#             nbrs.extend(p.aperiodicNeighborElements(skeleton))
#         return nbrs
    
# #######################################################

# if config.dimension()==2:

#     class HashedNodes:
#         def __init__(self, size, skelsize):
#             self.size = size
# ##            if config.dimension() == 2:
#             n = size[0]*size[1]
#             self.scale = (1.0*self.size[0]/skelsize[0],
#                           1.0*self.size[1]/skelsize[1])
# ##             elif config.dimension() == 3:
# ##                 n = size[0]*size[1]*size[2]
# ##                 self.scale = (1.0*self.size[0]/skelsize[0],
# ##                               1.0*self.size[1]/skelsize[1],
# ##                               1.0*self.size[2]/skelsize[2])
#             self.data = [[] for i in range(n)]
#             self.outofthebox = []

#         def getSize(self):
#             return self.size

#         def getScale(self):
#             return self.scale

#         def properTile(self, point):
#             ix = int( point.x*self.scale[0] )
#             iy = int( point.y*self.scale[1] )
#             # When right or top skeleton edge was clicked ....
#             if ix==self.size[0]: ix -= 1
#             if iy==self.size[1]: iy -= 1
# ##            if config.dimension() == 2:
#             return primitives.iPoint(ix, iy)
# ##             elif config.dimension() == 3:
# ##                 iz = int( point.z*self.scale[2] )
# ##                 if iz==self.size[2]: iz -= 1
# ##                 return primitives.iPoint(ix, iy, iz)

#         def iterator(self):
#             return self.data

#         def __setitem__(self, where, val):
# ##            if config.dimension() == 2:
#             self.data[self.size[0]*where.y + where.x] = val
# ##             elif config.dimension() == 3:
# ##                 self.data[self.size[1]*self.size[0]*where.z + self.size[0]*where.y + where.x] = val

#         def __getitem__(self, where):
#             try:
# ##                if config.dimension()==2 and (where.x>=0 and where.y>=0):
#                 return self.data[self.size[0]*where.y + where.x]
# ##                 elif config.dimension()==3 and (where.x>=0 and where.y>=0 and where.z>=0):
# ##                     return self.data[self.size[1]*self.size[0]*where.z +
# ##                                      self.size[0]*where.y + where.x]
# ##             else:
# ##                 return self.outofthebox
#             except IndexError:
#                 return self.outofthebox
            
#         def hash(self, skeleton):
#             # Putting nodes in corresponding tiles
#             for node in skeleton.nodes:
#                 where = self.properTile(node.position())
#                 self[where].append(node)

#         def nearestNode(self, point):
#             where = self.properTile(point)

#             count = 0  # No. of tile-bands containing nodes
#             iter = 1   # No. of tile-bands having been looked at
#             nodes = self[where][:]
#             while count < 2:   
#                 # Initial check
#                 if iter==1:
#                     if nodes: count += 1
#                 # Additional band of tiles
#                 addition = self.nextBand(
#                     ll=primitives.iPoint(where.x-iter, where.y-iter),
#                     ur=primitives.iPoint(where.x+iter, where.y+iter))
#                 if addition:
#                     nodes += addition
#                     count += 1
#                 else:
#                     if count==1:
#                         break  # No need to look for another band
#                 # Ready for the next round
#                 iter += 1

#             # Find the nearest node among collected nodes
#             nearest = nodes[0]
#             mindist = (nearest.position() - point)**2
#             for node in nodes[1:]:
#                 dd = (node.position() - point)**2
#                 if dd < mindist:
#                     mindist = dd
#                     nearest = node
#             return nearest

#         def nextBand(self, ll=None, ur=None):
#             nodes = []
#             # Bottom
#             j = ll.y
#             for i in range(ll.x, ur.x+1):
#                 nodes += self[primitives.iPoint(i,j)][:]
#             # Top
#             j = ur.y
#             for i in range(ll.x, ur.x+1):
#                 nodes += self[primitives.iPoint(i,j)][:]
#             # Left
#             i = ll.x
#             for j in range(ll.y+1, ur.y):
#                 nodes += self[primitives.iPoint(i,j)][:]
#             # Right
#             i = ur.x
#             for j in range(ll.y+1, ur.y):
#                 nodes += self[primitives.iPoint(i,j)][:]
#             return nodes

###############################################################
    
# The set of pinned nodes acts much like a set of selected objects, so
# it derives a lot of its code from skeletonselectable.  See comments
# in SelectionSetBase and SelectionSet in skeletonselectable.py.  A
# big difference between pinned nodes and selections is that when a
# node is pinned the pinning doesn't propagate to parents or children
# that are at different positions.  A deputy skeleton can have a
# different set of pinned nodes than its sheriff or its fellow
# deputies.

## TODO OPT: Move PinnedNodeSet and PinnedNodeSelection to C++ when
## Selection and SelectionBase are moved.

class PinnedNodeSet(skeletonselectable.SelectionSetBase):
    def __init__(self, *args, **kwargs):
        skeletonselectable.SelectionSetBase.__init__(self, *args, **kwargs)

    def implied_select(self, oldskel, newskel):
        # Called from SelectionBase.whoChanged0() when a new
        # Skeleton is pushed.  Creates a tracker for the new skeleton
        # with the same pinned nodes as the old skeleton, if those
        # nodes are at the old positions.
        tracker = newskel.newPinnedNodeTracker()
        self.selected[newskel] = tracker
        if oldskel != newskel:
            oldtracker = self.selected[oldskel]
            tracker.implied_pin(oldtracker)

    # def replace(self, oldskel, newskel):
    #     # Called just after a SkeletonContext undo or redo by
    #     # SkeletonContext.undoHookFn and SkeletonContext.redoHookFn.
    #     oldtracker = self.selected[oldskel]
    #     oldtracker.clearskeleton()
    #     newtracker = self.selected[newskel]
    #     newtracker.write()

    def clone(self):
        bozo = self.__class__(self.skeletoncontext)
        for skel, tracker in self.selected.items():
            trclone = tracker.clone()
            bozo.selected[skel] = trclone
        return bozo


stacksize = 50

class PinnedNodeSelection(skeletonselectable.SelectionBase):
    def __init__(self, skeletoncontext):
        skeletonselectable.SelectionBase.__init__(self, skeletoncontext)
        self.stack = ringbuffer.RingBuffer(stacksize)
        self.stack.push(PinnedNodeSet(self.skeletoncontext))
        self.sbcallbacks.append(switchboard.requestCallback(
            'pinnednode ringbuffer resize', self.setUndoBufferSizeCB))
        # self.stack.overwrite = self.overwrite

    # def overwrite(self, tracker):
    #     pass

    # def replace(self, oldskel, newskel):
    #     # Called just after a SkeletonContext undo or redo by
    #     # SkeletonContext.undoHookFn and SkeletonContext.redoHookFn.
    #     self.stack.current().replace(oldskel, newskel)

    def signal(self):
        # signal() is called after each pinning operation (by the menu
        # commands in the toolbox & task page).  It's also called by
        # the generic SkeletonSelection mechanism, which is why the
        # menu commands don't just simply issue the "new pinned nodes"
        # message themselves.  "new pinned nodes" is caught by all the
        # toolboxes, which relay the message to their graphics
        # windows.
        switchboard.notify("new pinned nodes", self.skeletoncontext)
        switchboard.notify("redraw")

    def npinned(self):
        return len(self.retrieve())

    def pin(self, node):
        (clist, plist) = self.trackerlist()
        node.pin(clist, plist)
#             for partner in n.getPartners():
#                 partner.pin(clist, plist)
        # self.timestamp.increment()

    def pinList(self, nodelist):
        (clist, plist) = self.trackerlist()
        for node in nodelist:
            node.pin(clist, plist)
        # self.timestamp.increment()

    def pinSelection(self, tracker):
        (clist, plist) = self.trackerlist()
        cskeletonnode2.CSkeletonNode_pinSelection(tracker, clist, plist)
        # self.timestamp.increment()

    def unpinSelection(self, tracker):
        (clist, plist) = self.trackerlist()
        cskeletonnode2.CSkeletonNode_unpinSelection(tracker, clist, plist)
        # self.timestamp.increment()

    def pinSelectedSegments(self, tracker):
        (clist, plist) = self.trackerlist()
        cskeletonnode2.CSkeletonNode_pinSelectedSegments(tracker, clist, plist)
        # self.timestamp.increment()

    def pinSelectedElements(self, tracker, skel, internal, boundary):
        (clist, plist) = self.trackerlist()
        cskeletonnode2.CSkeletonNode_pinSelectedElements(
            tracker, skel, internal, boundary, clist, plist)
        # self.timestamp.increment()

    def pinInternalBoundaryNodes(self, skel):
        (clist, plist) = self.trackerlist()
        cskeletonnode2.CSkeletonNode_pinInternalBoundaryNodes(
            skel, clist, plist)
        # self.timestamp.increment()

    def unpin(self, node):
        (clist, plist) = self.trackerlist()
        # for n in nodelist:
        node.unpin(clist, plist)
#             for partner in n.getPartners():
#                 partner.unpin(clist, plist)
        # self.timestamp.increment()

    def toggle(self, node):
        (clist, plist) = self.trackerlist()
        # for n in nodelist:
        if node.pinned():
            node.unpin(clist, plist)
        else:
            node.pin(clist, plist)
        # self.timestamp.increment()

    def pinPoint(self, point):          # oxford
        skel = self.skeletoncontext.getObject()
        node = skel.nearestNode(point)
        self.pin(node)

    def unpinPoint(self, point):
        skel = self.skeletoncontext.getObject()
        node = skel.nearestNode(point)
        self.unpin(node)
                
    def togglepinPoint(self, point):
        skel = self.skeletoncontext.getObject()
        node = skel.nearestNode(point)
        self.toggle(node)

# def canonical_order(n0,n1):     # ONLY USED IN 2D
#     if n0.index < n1.index:
#         return (n0,n1)
#     return (n1,n0)
