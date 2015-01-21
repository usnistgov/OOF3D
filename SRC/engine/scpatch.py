# -*- python -*-
# $RCSfile: scpatch.py,v $
# $Revision: 1.14.12.4 $
# $Author: langer $
# $Date: 2014/09/17 21:26:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug

class SCPatch:
    def __init__(self, skel, subproblem, realcndindex, mat):
        self.skel = skel
        #AMR subproblem
        self.subproblem=subproblem
        self.femesh=subproblem.mesh
        #Interface branch
        #self.assembly_node = cnd
        #store index of realmesh assembly node instead of a skeleton node
        self.assembly_node_index=realcndindex
        self.mat = mat  # material
        self.elements = []  # Skeleton elements
        self.segments = {}  # Skeleton segments, stored to be looked at later
        self.recovery_nodes = {}  # FEMesh nodes for recovery

    def getMaterial(self):
        return self.mat

    def nElements(self):
        return len(self.elements)

    def getElements(self):  # returns a copy of self.elements
        return self.elements[:]

    def addElement(self, el):           # el is a Skeleton element
        self.elements.append(el)
        snd0 = el.nodes[-1]  # Skeleton node
        #Interface branch
        realel=self.femesh.getElement(el.meshindex)
        for snd1 in el.nodes:
            # If the edge is on boundary (external or internal),
            # all the nodes on the edge are recovery nodes.
            irealsnd0=el.getNodeIndexIntoList(snd0)
            realsnd0=realel.getCornerNode(irealsnd0)
            irealsnd1=el.getNodeIndexIntoList(snd1)
            realsnd1=realel.getCornerNode(irealsnd1)
            if (self.subproblem.bdy_node_map[realsnd0.index()] and \
                self.subproblem.bdy_node_map[realsnd1.index()]):
                self.recovery_nodes[realsnd0.index()] = 1
                self.recovery_nodes[realsnd1.index()] = 1
                if self.femesh.order() > 1:  # higher order femesh
                    edge_nodes = self.subproblem.getRealEdgeNodes(
                        realel,
                        irealsnd0, realsnd0,
                        irealsnd1, realsnd1)
                    for fnd in edge_nodes:
                        self.recovery_nodes[fnd.index()] = 1
            else:
                # Non-boundary edges(segments) need to be looked at later.
                self.segments[self.skel.findSegment(snd0, snd1)] = 1

            snd0 = snd1  # for the next iteration

    def findRecoveryNodes(self, qualified=1):
        # nodes on patch boundary but not on actual boundary.
        patch_boundary = {}
        for seg in self.segments:
            elcount = 0
            for el in seg.getElements():
                if el in self.elements:
                    elcount += 1
            if elcount == 1:  # the segment is on patch boundary
                #Interface branch
                skelel=seg.getElements()[0]
                realel=self.femesh.getElement(skelel.meshindex)
                for nd in seg.nodes():
                    realnd=realel.getCornerNode(skelel.getNodeIndexIntoList(nd))
                    if not self.subproblem.bdy_node_map[realnd.index()]:
                        patch_boundary[nd] = 1
                self.segments[seg] = 0  # no need to look at it again.

        # recovery nodes that are inside patch (except internal nodes).
        for seg, need2look in self.segments.items():
            if not need2look:
                continue
            seg_nodes = seg.nodes()
            #Interface branch
            #self.segments is constructed such that its keys (skeleton segments)
            #are segments that are not on a boundary (external or internal)
            #or interface (see addElement).
            #Sufficient to get one skeleton element here.
            skelel=seg.getElements()[0]
            realel=self.femesh.getElement(skelel.meshindex)
            for nd in seg_nodes:
                if nd not in patch_boundary:
                    realnd=realel.getCornerNode(skelel.getNodeIndexIntoList(nd))
                    self.recovery_nodes[realnd.index()] = 1
            if self.femesh.order() > 1:  # higher order femesh
                #Assume there are two nodes in a skeleton segment
                irealn0=skelel.getNodeIndexIntoList(seg_nodes[0])
                realn0=realel.getCornerNode(irealn0)
                irealn1=skelel.getNodeIndexIntoList(seg_nodes[1])
                realn1=realel.getCornerNode(irealn1)
                edge_nodes = self.subproblem.getRealEdgeNodes(realel,
                                                          irealn0,realn0,
                                                          irealn1,realn1)
                for nd in edge_nodes:
                    self.recovery_nodes[nd.index()] = 1

        # Add any internal nodes
        if self.femesh.internal_nodes:
            for el in self.elements:
                for nd in self.femesh.getInternalNodes(el):
                    self.recovery_nodes[nd.index()] = 1

        # Create a C++ CSCPatch object that will do actual
        # computation. The CSCPatch is *not* a base class or member of
        # SCPatch. The CSCPatches are the only permanent objects
        # created by CSubProblem.create_scpatch(skel).
        self.subproblem.add_scpatch(self.assembly_node_index, self.mat,
                                    self.femesh.order(),
                                    [el.meshindex for el in self.elements],
                                    self.recovery_nodes.keys(),
                                    qualified)
#         debug.fmsg(self.assembly_node_index, [el.meshindex for el in self.elements], self.recovery_nodes.keys())
        
    def __repr__(self):
        return `[el.meshindex for el in self.elements]`

#########################################

class SCPatchCollection:
    #AMR subproblem, pass subproblem
    def __init__(self, subproblem):
        self.subproblem=subproblem
        self.femesh=subproblem.mesh
        self.patches = {}  # keyed by (node, material) pair
        ## TODO 3.1: Why not call initialize() and finalize() directly
        ## from __init__()?  What this class really does is
        ## encapsulate a buildPatches routine, which can be turned
        ## into a standalone function.  There's no need for a class
        ## here at all.  But with the widespread use of self.XXX, I'll
        ## just leave it as is.

    def buildPatches(self, skel):
        self.initialize(skel)
        self.finalize()

    def initialize(self, skel):
        # pre-processing -- finding nodes on boundaries (material & geometric).
        # it helps find recovery nodes more efficiently.
        self.skel = skel

        #Interface branch
        #Treat interface as some sort of boundary
        self.subproblem.create_bdy_node_map(skel)

        for cnd in skel.node_iterator():  # Skeleton node!
            # Among neighbors, elements will be grouped according to their
            # respective materials.
            #Interface branch
            #AMR subproblem
            for el in cnd.neighborElements():
                realel=self.femesh.getElement(el.meshindex)
                if self.subproblem.contains(realel):
                    realnode=realel.getCornerNode(el.getNodeIndexIntoList(cnd))
                    self.addElementToPatch(skel, realnode.index(), el)

    #Interface branch
    #Changed cnd (skeleton node) to a realmesh node index
    def addElementToPatch(self, skel, realcndindex, el):  # Skeleton element
        mat = self.femesh.getElement(el.meshindex).material()
        # Do not add elements or create patches where no material exists.
        if mat:
            try:  # existing entity
                self.patches[(realcndindex, mat)].addElement(el)
            except KeyError:  # new entity
                self.patches[(realcndindex, mat)] = SCPatch(skel, self.subproblem, realcndindex, mat)
                self.patches[(realcndindex, mat)].addElement(el)

    def finalize(self):
        # Augment patches and assign recovery nodes to patches.
        # For linear femesh, at least 3 elements are needed to
        # determine coefficients for [1, x, y]
        # For quadratic femesh, 2 elements are needed -- [1,x,y,x,y,x^2,y^2]
        if self.femesh.order() == 1:  # Linear
            min_els = 4
        else:  # Quadratic
            min_els = 4  # 4 seems to do better than 2
        for patch in self.patches.values():
            if patch.nElements() < min_els:
                # Collect every available neighbor element from
                # all the nodes in the current patch.
                for el in patch.getElements():
                    #Interface branch
                    fel = self.femesh.getElement(el.meshindex)
                    for nd in el.nodes:
                        #AMR subproblem
                        for el2 in nd.neighborElements():
                            fel2 = self.femesh.getElement(el2.meshindex)
                            if self.subproblem.contains(fel2):
                                fel2_mat = fel2.material()
                                if fel2_mat == patch.getMaterial() and \
                                       el2 not in patch.elements:
                                    #Interface branch
                                    #Add el2 and expand the patch
                                    #if el and el2 share the same realmesh
                                    #node at skeleton node nd
                                    realnode=fel.getCornerNode(el.getNodeIndexIntoList(nd))
                                    realnode2=fel2.getCornerNode(el2.getNodeIndexIntoList(nd))
                                    if realnode==realnode2:
                                        patch.addElement(el2)

            # If still not enough elements, then it's a disqualified patch.
            if patch.nElements() < min_els:
                patch.findRecoveryNodes(qualified=0)
            else:
                patch.findRecoveryNodes()
