# -*- python -*-
# $RCSfile: skeletonelement.py,v $
# $Revision: 1.174.2.3 $
# $Author: langer $
# $Date: 2013/11/08 20:44:49 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

## THIS FILE IS USED ONLY IN 2D
from ooflib.SWIG.common import config
assert config.dimension() == 2

from ooflib.SWIG.common import coord
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.engine import cskeleton
from ooflib.SWIG.engine import material
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import object_id
from ooflib.common import parallel_enable
from ooflib.common import primitives
from ooflib.engine import skeletonnode
from ooflib.engine import skeletonselectable
import ooflib.common.microstructure
import math

#########################################

class ElementShapeType(enum.EnumClass(('triangle', 'triangular elements'),
                                      ('quad', 'quadrilateral elements'))):
    tip = "Shapes of Skeleton Elements."
    discussion = """<para>
    <classname>ElementShapeType</classname> objects are used in a few
    cases where it's necessary to distinguish between &elem; shapes in
    the &oof2; commands.
    </para>"""
    


# The SkeletonElementBase is the base class for both the
# SkeletonElement and the ProvisionalElement.  It can compute
# geometrical stuff like homogeneity and shape energy, but knows
# nothing about selectability, segments, or neighbors.

class SkeletonElementBase:
    def __init__(self, nodes):
        self.nodes = nodes
        
    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, id(self))
#         return "%s(%s)" % (self.__class__.__name__, self.nodes)

    def material(self, skeletonctxt):
        # This is the default function for assigning a material to an
        # element.  When a Mesh is created, a different function may
        # be used in some circumstances (see Relax).

        # If this element is part of an ElementGroup that has an
        # explicitly assigned Material, return that Material.  If it's
        # part of more than one such group, return the Material that
        # was assigned most recently.  Otherwise, return the material
        # assigned to the element's dominant pixel.
        
        lasttime = timestamp.timeZero
        lastmaterial = None
        for group in self.groups:
            matl, ts = skeletonctxt.elementgroups.getMaterialAndTime(group)
            if matl is not None and ts > lasttime:
                lastmaterial, lasttime = matl, ts
        if lastmaterial is not None:
            return lastmaterial
        ms = skeletonctxt.getObject().MS
        dominantpixel = self.dominantPixel(ms)
        if dominantpixel is not None:
            return material.getMaterialFromCategory(ms, dominantpixel)

    def underlyingPixels(self, microstructure):
        # Returns a list of all pixels that overlap with this element.
        dx, dy = microstructure.sizeOfPixels()
        nx, ny = microstructure.sizeInPixels()
        return self.underlying_pixels(microstructure) # C++

    def transitionPoint(self, skeleton, edgeno):
        ok, point = \
            cskeleton.CSkeletonElementPtr.transitionPoint(self, skeleton.MS,
                                                          edgeno)
        if ok:
            return point
    
    def energyTotal(self, skeleton, alpha):
        if alpha == 0.0:
            return self.energyShape()
        if alpha == 1.0:
            return self.energyHomogeneity(skeleton.MS)
        return alpha*self.energyHomogeneity(skeleton.MS) + \
               (1.-alpha)*self.energyShape()

    def getPositionHash(self):
        sortedpositions = [n.position() for n in self.nodes]
        sortedpositions.sort()
        hashable = []
        for pos in sortedpositions:
            for i in range(2):
                hashable.append(pos[i])
        return hash(tuple(hashable))

##########################
        
class SkeletonElement(SkeletonElementBase,
                      skeletonselectable.SkeletonSelectable):
    def __init__(self, nodes, index):
        SkeletonElementBase.__init__(self, nodes)
        skeletonselectable.SkeletonSelectable.__init__(self, index)

        # Although the CSkeletonElement keeps a list of
        # CSkeletonNodes, the extra information in the Python
        # SkeletonNodes isn't available unless we keep a list of them
        # here, as well.  It's possible that we could move all the
        # extra info into the CSkeletonNode class and swig it.
        # Canonical ordering will still work, because it's based on
        # indices.
        self.nodes = nodes
        
        for node in nodes:
            node.addElement(self)
            
        # When a real mesh is made from the skeleton in which this
        # element lives, self.meshindex gets assigned the index of
        # that element.  This index is the same for all the real meshes.
        self.meshindex = None

        self.ID = object_id.ObjectID()

        # process ID (only meaningful in parallel mode)
        if parallel_enable.enabled():
            from ooflib.SWIG.common import mpitools
            self._procID = mpitools.Rank()
        else:
            self._procID = None


    # There may be some temptation to provide elements with an
    # index-based equality comparison function.  Doing this is
    # dangerous, as it screws up the parent/child addition machinery
    # in the parent SkeletonSelection class. 

    def repr_position(self):
        return self.center()

    def getIndex(self):
        return self.index

    #Interface branch
    def getNodeIndexIntoList(self,node):
        ## TODO OPT: This seems to be called a lot.  Why not create a
        ## lookup table, or store the index in the node?
        return self.nodes.index(node)

    def type(self):
        return self.shapetype

    def destroy(self, skeleton):
        self.disconnect()
        nnodes = self.nnodes()
        lastnode = self.nodes[-1]
        for node in self.nodes:
            skeleton.findSegment(lastnode, node).removeElement(skeleton, self)
            node.removeElement(skeleton, self)
            lastnode = node
        self.nodes = []

    # def getFEelement(self):
    #     return self.element

    def getSegments(self, skeleton):
        segments = []
        lastnode = self.nodes[-1]
        for node in self.nodes:
            segments.append(skeleton.findSegment(node, lastnode))
            lastnode = node
        return segments

    #Interface branch
    #Get the segment opposite seg1 and that is incident on node1.
    #seg1 and the segment we are looking for form a 'V'.
    def getOppositeSegment(self, node1, seg1, skeleton):
        for node in self.nodes:
            if node!=node1:
                oseg=skeleton.findSegment(node,node1)
                if oseg is not None and oseg!=seg1:
                    return oseg
    def nodesInOrder(self, node0, node1):
        lastnode = self.nodes[-1]
        for node in self.nodes:
            if node0==lastnode and \
                   node1==node:
                return 1
            lastnode=node
        return 0
    def getSegmentOrderNumber(self, seg, skeleton):
        lastnode = self.nodes[-1]
        i=0
        for node in self.nodes:
            if seg==skeleton.findSegment(node, lastnode):
                return i
            lastnode=node
            i+=1
        return -1
    def getSegmentFromOrderNumber(self, ordernumber, skeleton):
        lastnode = self.nodes[-1]
        i=0
        for node in self.nodes:
            if i==ordernumber:
                return skeleton.findSegment(node, lastnode)
            lastnode=node
            i+=1
        return None

    def active(self, skeleton):
        for node in self.nodes:
            if node.active(skeleton):
                return 1
        return 0

    def new_child(self,index):
        raise ooferror2.ErrPyProgrammingError(
            "Attempt to clone element parent class.")

    def getNumberOfEdges(self):
        return self.nnodes()

    def segment_node_iterator(self):
        segment_nodes = []
        for i in range(self.nnodes()):
            n0 = self.nodes[i]
            n1 = self.nodes[(i+1)%self.nnodes()]
            segment_nodes.append((n0,n1))
        return segment_nodes

    def segment_iterator(self, skel):
        segments = []
        for i in range(self.nnodes()):
            n0 = self.nodes[i]
            n1 = self.nodes[(i+1)%self.nnodes()]
            segments.append(skel.findSegment(n0, n1))
        return segments

    def edgeNeighbors(self, skeleton, loopRange=0):
        # Search for edge-sharing neighborhood for a given element and return
        # a list of them.
        nnodes = self.nnodes()
        edgeNeighborList = [None]*nnodes
        for i in range(nnodes):
            segment = skeleton.findSegment(self.nodes[i],
                                           self.nodes[(i+1)%nnodes])
            if segment is not None:
                edgeNeighborList[i] = segment.getOtherElement(self)

            # this should only work if the segment is on a periodic boundary
            # in which case the above call to getOtherElement should have
            # returned nothing
            partners = self.nodes[i].getPartnerPair(self.nodes[(i+1)%nnodes])
            if partners is not None:
                segment = skeleton.findSegment(partners[0],partners[1])
                if segment is not None:
                    edgeNeighborList[i] = segment.getOtherElement(self)

        return edgeNeighborList

    def getEdgeLengthsList(self):
        list = []
        for i in range(self.nnodes()):
            list.append(self.edgeLength(i))
        return list

    def getShortestEdge(self):
        list = self.getEdgeLengthsList()
        minEdge = list[0]
        index = 0
        for i in range(1, self.nnodes()):
            if list[i] < minEdge:
                minEdge = list[i]
                index = i
        return index
    
    def getAnglesList(self):
#         list = []
#         for i in range(self.nnodes()):
#             list.append(self.cosCornerAngle(i))
#         return list
        return [self.cosCornerAngle(i) for i in range(self.nnodes())]
    
    
    def getBiggestAngle(self):
        list = self.getAnglesList()
        maxAngle = list[0]  # cosine of the angle
        index = 0
        for i in range(1, self.nnodes()):
            if list[i] < maxAngle:
                maxAngle = list[i]
                index = i
        return index

    def getSister(self, skeleton, node0, node1):
        # 4 _________ 3
        #   \       /
        #    \  A  /    If an edge 1-2 of the element A needs to be modified
        #     \   /     (for example, collapsing), it is important to update
        #    1 \_/ 2    its edge-sharing neighbor element B.
        #      / \      This function returns a sister element of "self" which
        #     /   \     shares an edge (node1-node2).
        #    /  B  \
        #   ---------

        segment = skeleton.findSegment(node0, node1)
        elements = segment.getElements()
##        if len(elements) > 2:
##            raise ooferror2.ErrPyProgrammingError("Too many sisters!")
        for e in elements:
            if e is not self:
                return e
        return None  # edge boundary
    
    def getSisterPeriodic(self, skeleton, node0, node1):
        segment = skeleton.findSegment(node0, node1)
        elements = segment.getElements()
        for e in elements:
            if e is not self:
                return e
        partnerseg = segment.getPartner(skeleton)
        if partnerseg:
            return partnerseg.getElements()[0]
        return None

    def replacementNodes(self, oldnode, newnode):
        nodelist = self.nodes[:]
        which = nodelist.index(oldnode)
        nodelist[which] = newnode
        return nodelist

    # Parallel stuff
    if parallel_enable.enabled():
        def belongTo(self, bbox):  # called from "engine.IO.skeletonIPC"
            c = self.center()
            xmin = bbox.lowerLeft[0]
            ymin = bbox.lowerLeft[1]
            xmax = bbox.upperRight[0]
            ymax = bbox.upperRight[1]
            return (xmin<=c[0] and c[0]<xmax) and (ymin<=c[1] and c[1]<ymax)

        def resetProcID(self, id):
            self._procID = id  # id is the id of the process
            # ... and for the nodes
            for nd in self.nodes:
                nd.addOwner(id)

        def procID(self):
            return self._procID

    #########################

    #Interface branch
    def realelement(self, skeletoncontext, mesh, index,
                    fe_node, seg_dict,
                    elemdict, materialfunc):
        # Create a real element corresponding to this skeleton
        # element. The elemdict argument is a dictionary (keyed by the
        # number of sides of the element) of MasterElement objects,
        # which contain the information needed to construct the real
        # elements.  "index" is the SkeletonElement's position in the
        # Skeleton's list, and "fe_node" is a dictionary of real nodes
        # in the FEMesh, indexed by their corresponding SkeletonNode
        # objects.  The lists give the nodes in the order in which
        # they were added to the element.
        
        # Be safe with indices.
        if self.meshindex is None: # Zero is nontrivial index.
            self.meshindex = index
        else:
            if index != self.meshindex:
                raise ooferror2.ErrPyProgrammingError(
                    "Index mismatch in element construction.")
                
        nnewnodes = 0
        ncn = len(self.nodes) # Corner nodes.

        # elemdict is a dictionary of MasterElements, keyed by number
        # of sides.
        elementtype = elemdict[self.nnodes()]
        nodes = []                      # real nodes for this element

        for i in range(len(self.nodes)):  # i.e. for each edge...
            c0 = self.nodes[i]
            nodes.append(fe_node[c0])     # Corner nodes already exist.
            c1 = self.nodes[(i+1)%ncn]
            cset = skeletonnode.canonical_order(c0, c1)


            # Look up this edge in the dictionary.  If it's there,
            # then nodes have been created on the edge already, and we
            # should reuse them.

            try:
                xtranodes = mesh.getEdgeNodes(cset)
                # The nodes were created by the neighboring element.
                # Since elements traverse their edges counterclockwise
                # when creating nodes, the preexisting nodes are in
                # the wrong order for the current element.
                xtranodes.reverse()
            except KeyError:
                # The edge wasn't in the dictionary.  It's a new edge.
                xtranodes  = []
                # Loop over all protonodes on the current
                # edge of the new element
                for newproto in elementtype.protodic[i]:
                    masterxy = primitives.Point(newproto.mastercoord()[0],
                                           newproto.mastercoord()[1])
                    realxy = self.frommaster(masterxy, 0)
                    newnode = _makenewnode(mesh, newproto,
                                           coord.Coord(realxy.x, realxy.y))
                    nnewnodes = nnewnodes + 1
                    xtranodes.append(newnode)
                #Interface branch
                try:
                    #If the segment represented by cset is a member of an
                    #interface, then new edge nodes (xtranodes) will
                    #not be shared by another element.
                    test=seg_dict[cset]
                except KeyError:
                    mesh.addEdgeNodes(cset, xtranodes)
            nodes = nodes + xtranodes

        # Interior nodes at the end.
        for newproto in elementtype.protodic['interior']:
            masterxy = primitives.Point(newproto.mastercoord()[0],
                                        newproto.mastercoord()[1])
            realxy = self.frommaster(masterxy, 0)
            newnode = _makenewnode(mesh, newproto,
                                   coord.Coord(realxy.x, realxy.y))
            nnewnodes = nnewnodes + 1
            nodes.append(newnode)
            mesh.addInternalNodes(self, newnode)

        # Having constructed the list of nodes, call the real
        # element's constructor.  materialfunc returns the element's
        # material.  In normal operation, materialfunc is
        # SkeletonElement.realmaterial.
        realel = elementtype.build(self, materialfunc(self, skeletoncontext),
                                   nodes)
        
        mesh.addElement(realel)               # Add to mesh.
        # Tell the element about its exterior edges.
        for edge in self.exterior_edges:
            realel.set_exterior(fe_node[edge[0]], fe_node[edge[1]])

        return nnewnodes

    #########################

    # For parallel mesh construction. Non-corner nodes are given
    # sharing information based on the corner nodes that bound the
    # segment where the non-corner nodes are found.  Called in
    # Skeleton.femesh_shares. These edge nodes are shared by at most
    # two processors (2D).  Assume the number of protonodes in an edge
    # can't be anywhere close to 50.
    
    def realelement_shares(self, skeleton, mesh, index, fe_node,
                    curnodeindex, elemdict, materialfunc):        
        # Be safe with indices.
        if self.meshindex is None: # Zero is nontrivial index.
            self.meshindex = index
        else:
            if index != self.meshindex:
                raise ooferror2.ErrPyProgrammingError(
                    "Index mismatch in element construction.")
                
        nnewnodes = 0
        ncn = len(self.nodes) # Corner nodes.

        # elemdict is a dictionary of MasterElements, keyed by number
        # of sides.
        elementtype = elemdict[self.nnodes()]
        nodes = []                      # real nodes for this element

        for i in range(len(self.nodes)):  # i.e. for each edge...
            c0 = self.nodes[i]
            nodes.append(fe_node[c0])     # Corner nodes already exist.
            c1 = self.nodes[(i+1)%ncn]
            cset = skeletonnode.canonical_order(c0, c1)

            # Look up this edge in the dictionary.  If it's there,
            # then nodes have been created on the edge already, and we
            # should reuse them.

            try:
                xtranodes = mesh.getEdgeNodes(cset)
                # The nodes were created by the neighboring element.
                # Since elements traverse their edges counterclockwise
                # when creating nodes, the preexisting nodes are in
                # the wrong order for the current element.
                xtranodes.reverse()
            except KeyError:
                newindexinc=0
                newindex=0
                protocount=0
                protodiclength=len(elementtype.protodic[i])
                if c0.index<c1.index:
                    newindexinc=1
                    newindex=skeleton.maxnnodes+100*c0.index
                else:
                    # Do this to distinguish the protonode on either
                    # side of a corner node that has a smaller index
                    # than either corner nodes of the collinear
                    # segments extending from that corner node.
                    newindexinc=-1
                    newindex=skeleton.maxnnodes+100*c1.index+50+protodiclength-1

                # The edge wasn't in the dictionary.  It's a new edge.
                xtranodes  = []
                # Loop over all protonodes on the current
                # edge of the new element
                for newproto in elementtype.protodic[i]:
                    masterxy = primitives.Point(newproto.mastercoord()[0],
                                           newproto.mastercoord()[1])
                    realxy = self.frommaster(masterxy, 0)
                    newnode = _makenewnode_shares(
                        mesh, newproto,
                        coord.Coord(realxy.x, realxy.y),
                        c0,c1,newindex,protocount,
                        protodiclength,skeleton.maxnnodes)
                    newindex+=newindexinc
                    protocount+=1
                    nnewnodes = nnewnodes + 1
                    xtranodes.append(newnode)
                mesh.addEdgeNodes(cset, xtranodes)
            #Should this be 'join'ed instead, for speed?
            nodes = nodes + xtranodes

        # Interior nodes at the end.
        for newproto in elementtype.protodic['interior']:
            masterxy = primitives.Point(newproto.mastercoord()[0],
                                        newproto.mastercoord()[1])
            realxy = self.frommaster(masterxy, 0)
            newnode = _makenewnode(mesh, newproto,
                                   coord.Coord(realxy.x, realxy.y))
            nnewnodes = nnewnodes + 1
            nodes.append(newnode)
            mesh.addInternalNodes(self, newnode)

        # Having constructed the list of nodes, call the real
        # element's constructor.
        realel = elementtype.build(self, materialfunc(self, skeleton), nodes)
        # Long-lost cousin of Kal-El and Jor-El.
        
        mesh.addElement(realel)               # Add to mesh.
        # Tell the element about its exterior edges.
        for edge in self.exterior_edges:
            realel.set_exterior(fe_node[edge[0]], fe_node[edge[1]])

        return nnewnodes

    def realmaterial(self, skeletoncontext):
        return self.material(skeletoncontext)

#####################################################

class ProvisionalElement(SkeletonElementBase):
    def __init__(self, nodes, parents):
        SkeletonElementBase.__init__(self, nodes)
        self.parents = parents
    def accept(self, skeleton):
        element = skeleton.newElement(self.nodes, parents=self.parents)
        element.copyHomogeneity(self)
        return element

#####################################################    

class SkeletonQuad(SkeletonElement, cskeleton.CSkeletonQuad):
    # A four-sided ghost element with master space (-1,-1) to (1,1).
    def __init__(self,nodes,index):
        SkeletonElement.__init__(self,nodes,index)
        cskeleton.CSkeletonQuad.__init__(self, *nodes)

    shapetype = ElementShapeType('quad')

##    def __repr__(self):
##        return "SkeletonQuad"

    def new_child(self,index):
        node_children = [ x.getChildren()[-1] for x in self.nodes ]
        new = SkeletonQuad(node_children, index)
        new.copyHomogeneity(self)
        return new

    def aspectRatio(self):
        #         ________d(max)_________
        #        |                      /
        # a(min) |                     / c
        #        |____________________/
        #                  b 
        #
        # aspect ratio : 1. Find a max ratio of two consecutive segments
        #                   => d/a
        #                2. Get an opposite segment of "a". => c
        #                3. A.R. => max(c,d)/min(c,d)
        #
        # The reason why not using d/a as A.R. is that if a quad. has
        # one short segment and three similarly long segments, d/a may
        # give a wrong impression about this quad.

        lengths = [self.edgeLength(i) for i in range(4)]
        max_ratio = 1.0
        long_side = None
        short_side = None
        for i in range(4):
            if lengths[i] >= lengths[(i+1)%4]:
                long = i
                short = (i+1)%4
            else:
                long = (i+1)%4
                short = i
            ratio = lengths[long]/lengths[short]
            if ratio >= max_ratio:
                max_ratio = ratio
                long_side = long
                short_side = short
        opposite = (short_side+2)%4
        return max(lengths[opposite], lengths[long_side])/\
               min(lengths[opposite], lengths[long_side])

##    def getLongSegments(self, skeleton):
##        lengths = [self.edgeLength(i) for i in range(4)]
##        long = lengths.index(max(lengths))
##        seg1 = skeleton.findSegment(self.nodes[long], self.nodes[(long+1)%4])
##        seg2 = skeleton.findSegment(self.nodes[(long+2)%4],
##                                    self.nodes[(long+3)%4])
##        return seg1, seg2

    def getAspectRatioSegments(self, threshold, skeleton):
        ## Return segments that should be refined by CheckAspectRatio.
        ## The long edges of quads can be refined if there are two
        ## long edges and two short ones, and the long ones are
        ## opposite to each other.  We check the ratio of the second
        ## longest to the second shortest, because this rules out
        ## cases in which one edge is much longer than the other
        ## three.
        segs = []
        lengths = map(self.edgeLength, (0,1,2,3))
        sortlengths = lengths[:]
        sortlengths.sort()
        if sortlengths[2] > sortlengths[1]*threshold:
            # find longest edges
            l0 = sortlengths[2]
            l1 = sortlengths[3]
            i0 = i1 = None
            for i in (0,1,2,3):
                leng = lengths[i]
                if leng == l0:
                    i0 = i
                if leng == l1:
                    i1 = i
            idiff = i0 - i1
            if idiff == 2 or idiff == -2:
                segs.append(skeleton.findSegment(self.nodes[i0],
                                                self.nodes[(i0+1)%4]))
                segs.append(skeleton.findSegment(self.nodes[i1],
                                                 self.nodes[(i1+1)%4]))
        return segs

    def provisionalReplacement(self, oldnode, newnode):
        return ProvisionalQuad(self.replacementNodes(oldnode, newnode),
                               self.getParents())

class ProvisionalQuad(ProvisionalElement, cskeleton.CSkeletonQuad):
    def __init__(self, nodes, parents):
        cskeleton.CSkeletonQuad.__init__(self, *nodes)
        ProvisionalElement.__init__(self, nodes, parents)

##################################
        
class SkeletonTriangle(SkeletonElement, cskeleton.CSkeletonTriangle):
    # A three-sided ghost element with master space (1,0) -> (0,1) -> (0,0)
    def __init__(self,nodes,index):
        SkeletonElement.__init__(self,nodes,index)
        cskeleton.CSkeletonTriangle.__init__(self,*nodes)

    shapetype = ElementShapeType('triangle')

    def new_child(self, index):
        node_children = [ x.getChildren()[-1] for x in self.nodes ]
        new = SkeletonTriangle(node_children, index)
        new.copyHomogeneity(self)
        return new

    def aspectRatio(self):
        lengths = [self.edgeLength(i) for i in range(3)]
        lengths.sort()
        ## This returns the ratio of the *middle* length to the
        ## *shortest* length, which might seem odd. It's a more
        ## conservative definition than using lengths[2]/lengths[0].
        ## The reason for using it is that aspectRatio is used to mark
        ## elements for refining, and not much is gained by refining
        ## high aspect triangles unless they're more or less
        ## isosceles, with only one small angle.
        return lengths[1]/lengths[0]

    def provisionalReplacement(self, oldnode, newnode):
        return ProvisionalTriangle(self.replacementNodes(oldnode, newnode),
                                   self.getParents())

##    def getLongSegments(self, skeleton):
##        lengths = [self.edgeLength(i) for i in range(3)]
##        short = lengths.index(min(lengths))
##        seg1 = skeleton.findSegment(self.nodes[(short+1)%3],
##                                    self.nodes[(short+2)%3])
##        seg2 = skeleton.findSegment(self.nodes[(short+2)%3],
##                                    self.nodes[(short+3)%3])
##        return seg1, seg2

    def getAspectRatioSegments(self, threshold, skeleton):
        # return segments that should be refined by CheckAspectRatio.
        # See comment in aspectRatio(), above.
        
        lengths = [(self.edgeLength(i), i) for i in range(3)]
        lengths.sort()
        if lengths[1][0] > lengths[0][0] * threshold:
            n0 = lengths[2][1]
            n1 = lengths[1][1]
            return [skeleton.findSegment(self.nodes[n0],
                                         self.nodes[(n0+1)%3]),
                    skeleton.findSegment(self.nodes[n1],
                                         self.nodes[(n1+1)%3])]
        return []

class ProvisionalTriangle(ProvisionalElement, cskeleton.CSkeletonTriangle):
    def __init__(self, nodes, parents):
        cskeleton.CSkeletonTriangle.__init__(self, *nodes)
        ProvisionalElement.__init__(self, nodes, parents)

###########################

def getProvisionalElement(nodes, parents):
    if len(nodes) == 3:
        return ProvisionalTriangle(nodes, parents)
    if len(nodes) == 4:
        return ProvisionalQuad(nodes, parents)

###########################

def _makenewnode(mesh, protonode, coord):
    """Make a new node in mesh at coord, given a protonode."""
    if protonode.func():
        return mesh.newFuncNode(coord)
    return mesh.newMapNode(coord)

def _makenewnode_shares(mesh, protonode, coord,
                        edgenode0, edgenode1, newindex, protocount,
                        protodiclength, maxnnodes):
    if protonode.func():
        newProcList=[]
        newRemoteIndexList=[]
        #Find the processes that share both edgenode0 and edgenode1.
        #In this scheme, the same index for the node gets used by the sharing processes
        for procs0 in edgenode0.sharedWith():
            for procs1 in edgenode1.sharedWith():
                if procs0==procs1:
                    newProcList.append(procs0)
                    remoteindex0=edgenode0.remoteIndex(procs0)
                    remoteindex1=edgenode1.remoteIndex(procs1)
                    #The sense of edge traversal is from remoteindex1 to remoteindex0 in procs0
                    if remoteindex1 < remoteindex0:
                        newremoteindex=maxnnodes+100*remoteindex1+protodiclength- \
                                        protocount-1
                    else:
                        newremoteindex=maxnnodes+100*remoteindex0+50+protodiclength- \
                                        protocount-1
                    newRemoteIndexList.append(newremoteindex)
##        print "procs", newProcList
##        print "remoteindex", newRemoteIndexList
##        print "index", newindex
##        print "c0", edgenode0.index
##        print "c1", edgenode1.index
##        print "--------"
        return mesh.newFuncNode_shares(coord,
                                       newProcList,
                                       newRemoteIndexList,
                                       newindex)
    #Don't know yet how to handle mapnodes
    return mesh.newMapNode(coord)

############################

