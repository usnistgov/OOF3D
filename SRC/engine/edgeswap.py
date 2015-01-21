# -*- python -*-
# $RCSfile: edgeswap.py,v $
# $Revision: 1.37.2.3 $
# $Author: fyc $
# $Date: 2014/07/24 21:36:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## TODO 3.1: Update for 3D.  This hasn't been modified since skeleton3d.py
## became cskeleton2.C.

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
if config.dimension() == 2:
    from ooflib.engine import skeleton
    from ooflib.engine import skeletonelement
elif config.dimension() == 3:
    from ooflib.engine import skeleton3d as skeleton
    from ooflib.engine import skeletonelement3d
from ooflib.engine import skeletonmodifier
from ooflib.common.IO import reporter
from ooflib.SWIG.common import progress
import random

if config.dimension() == 2:
    ProvisionalTriangle = skeletonelement.ProvisionalTriangle
    ProvisionalQuad = skeletonelement.ProvisionalQuad
elif config.dimension() == 3:
    ProvisionalTetra = skeletonelement3d.ProvisionalTetra

#################
        
class SwapEdges(skeletonmodifier.SkeletonModifier):
    def __init__(self, targets, criterion):
        self.targets = targets
        self.criterion = criterion

    def coreProcess(self, skel, processed, element):
        changes = []
        nnodes = element.nnodes()
        lastnode = element.nodes[-1] # lastnode only used in 2D
        for node in element.nodes:
            if config.dimension() == 2:
                sister = element.getSister(skel, lastnode, node)
            if config.dimension() == 3:
                oppnodes = [n for n in element.nodes if n is not node]
                sister = element.getSister(skel, oppnodes)
            if sister is not None and sister not in processed:
                if config.dimension() == 2:
                    snodes = sister.nnodes()
                    if nnodes == 3:
                        if snodes == 3:
                            changes += tritriSwap(skel, lastnode, node,
                                                  element, sister)
                        elif snodes == 4:
                            changes += triquadSwap(skel, lastnode, node,
                                                   element, sister)
                    elif nnodes == 4:
                        if snodes == 3:
                            changes += triquadSwap(skel, node, lastnode,
                                                   sister, element)
                        elif snodes == 4:
                            changes += quadquadSwap(skel, lastnode, node,
                                                    element, sister)
                elif config.dimension() == 3:
                    changes += twoToThreeSwap(skel, element, sister, oppnodes)
            lastnode = node
        return changes
    def apply(self, oldskeleton, context):
        prog = progress.getProgress("Edge swap", progress.DEFINITE)
        try:
            return self._apply(oldskeleton, context, prog)
        finally:
            prog.finish()
    def _apply(self, oldskeleton, context, prog):
        skel = oldskeleton.properCopy(skeletonpath=context.path())
        elements = self.targets(skel, context, copy=1)
        random.shuffle(elements)
        # A dict. keyed by element to prevent considering swapping an
        # element which does not exist any more.
        processed = {}
        done = 0  # No. of elements swapped
        savedE = 0  # Saved energy from swapping
        nel = len(elements)
        for i in range(nel):
            element = elements[i]
            if element not in processed and element.active(skel):
                # Loop over the neighbors, generating candidates for
                # the result of the swap.
                changes = self.coreProcess(skel, processed, element)
                bestchange = self.criterion(changes, skel)
                if bestchange is not None:
                    done += 2
                    savedE += bestchange.deltaE(skel,
                                                self.criterion.alpha)
                    bestchange.accept(skel)
                    # Newly created elements from swap should not be
                    # looked at again, not to mention the original pair
                    for elephant in bestchange.removed:
                        processed[elephant] = 1
                    for elephant in bestchange.inserted:
                        processed[elephant] = 1
                if prog.stopped():
                    return None
                prog.setFraction(1.0*(i+1)/nel)
                prog.setMessage("%d/%d" % (i+1, nel))

        reporter.report("Swapped %d elements, saving energy %g" %
                        (done, savedE))
        skel.cleanUp()
        return skel

registeredclass.Registration(
    'Swap Edges',
    skeletonmodifier.SkeletonModifier,
    SwapEdges,
    ordering=4,
    params=[parameter.RegisteredParameter('targets',
                                          skeletonmodifier.SkelModTargets,
                                          tip = 'Which elements to modify.'),
    parameter.RegisteredParameter('criterion',
                                  skeletonmodifier.SkelModCriterion,
                                  tip='Acceptance criterion')            
            ],
    tip="Rearrange internal edges in pairs of neighboring elements.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/swapedges.xml'))
    
                             

#################################

#      BEGIN 2D RULES

#################################
if config.dimension() == 2:

    def tritriSwap(skel, n0, n1, tri0, tri1):
        #           n1
        #          /|\               / \
        #         / | \             /   \
        #        /  |  \           /  B  \   
        #     n2/ t0| t1\n3 ===>  /_______\  
        #       \   |   /         \       /
        #        \  |  /           \  A  /
        #         \ | /             \   /
        #          \|/               \ /
        #           n0
        #

        # Exit condition
        if (n0.pinned() and n1.pinned()):
            return []
        n2 = tri0.nodes[(tri0.nodes.index(n1)+1)%3]
        n3 = tri1.nodes[(tri1.nodes.index(n0)+1)%3]
        parents = tri0.getParents() + tri1.getParents()
        A = ProvisionalTriangle([n0, n3, n2], parents=parents)
        B = ProvisionalTriangle([n1, n2, n3], parents=parents)

        change = skeleton.ProvisionalChanges(skel)
        change.removeElements(tri0, tri1)
        change.insertElements(A, B)

        # If source elements are 100 % homogeneous with the same dominant pixel,
        # resulting elements will be so.
        if tri0.homogeneity(skel.MS)==1. and tri1.homogeneity(skel.MS)==1. and \
           tri0.dominantPixel(skel.MS)==tri1.dominantPixel(skel.MS):
            A.copyHomogeneity(tri0)
            B.copyHomogeneity(tri0)

        return [change]


    def triquadSwap(skel, n0, n1, tri, quad):
        #
        #      n3__ n0              
        #       |   |\              
        #       |   | \             [n4, n0, n3] & [n4, n1, n2, n0]
        #       |   |  \            [n4, n1, n2] & [n4, n2, n0, n3]
        #       |   |   \           [n4, n1, n3] & [n1, n2, n0, n3]
        #       | q |    \     ==>  [n0, n3, n2] & [n3, n4, n1, n2]
        #       |   | t  /n2        
        #       |   |   /                                  
        #       |   |  /           
        #       |   | /                                  
        #       |__ |/             
        #      n4   n1 
        #
        if (n0.pinned() and n1.pinned()) and \
           (tri.dominantPixel(skel.MS) != quad.dominantPixel(skel.MS)):
            return []

        n2 = tri.nodes[(tri.nodes.index(n1)+1)%3]
        i = quad.nodes.index(n0)
        n3 = quad.nodes[(i+1)%4]
        n4 = quad.nodes[(i+2)%4]

        parents = quad.getParents() + tri.getParents()

        A = ProvisionalQuad([n4, n1, n2, n0], parents=parents)
        B = ProvisionalTriangle([n4, n0, n3], parents=parents)
        change0 = skeleton.ProvisionalChanges(skel)
        change0.insertElements(A, B)
        change0.removeElements(quad, tri)

        C = ProvisionalQuad([n4, n2, n0, n3], parents=parents)
        D = ProvisionalTriangle([n4, n1, n2], parents=parents)
        change1 = skeleton.ProvisionalChanges(skel)
        change1.insertElements(C, D)
        change1.removeElements(quad, tri)

        E = ProvisionalQuad([n1, n2, n0, n3], parents=parents)
        F = ProvisionalTriangle([n4, n1, n3], parents=parents)
        change2 = skeleton.ProvisionalChanges(skel)
        change2.insertElements(E, F)
        change2.removeElements(quad, tri)

        G = ProvisionalQuad([n3, n4, n1, n2], parents=parents)
        H = ProvisionalTriangle([n0, n3, n2], parents=parents)
        change3 = skeleton.ProvisionalChanges(skel)
        change3.insertElements(G, H)
        change3.removeElements(quad, tri)

        # If source elements are 100 % homogeneous with the same dominant pixel,
        # resulting elements will be so.
        if tri.homogeneity(skel.MS)==1. and quad.homogeneity(skel.MS)==1. and \
           tri.dominantPixel(skel.MS)==quad.dominantPixel(skel.MS):
            A.copyHomogeneity(tri)
            B.copyHomogeneity(tri)
            C.copyHomogeneity(tri)
            D.copyHomogeneity(tri)
            E.copyHomogeneity(tri)
            F.copyHomogeneity(tri)
            G.copyHomogeneity(tri)
            H.copyHomogeneity(tri)

        return [change0, change1, change2, change3]


    def quadquadSwap(skel, n0, n1, quad0, quad1):
        #           n1      
        #          /|\            
        #         / | \      
        #        /  |  \          [n0, n4, n2, n3] & [n4, n5, n1, n2] 
        #     n2|   |   |n5       [n0, n4, n5, n3] & [n5, n1, n2, n3]
        #       |q0 |q1 |     ==>  
        #     n3|   |   |n4       
        #        \  |  /        
        #         \ | /           
        #          \|/       
        #           n0

        #           n1      
        #          /|\            
        #         / | \      
        #        /  |  \          
        #     n2|  /n6  |n5       
        #       | /   \ |     ==> [n0, n4, n6, n3] & [n3, n6, n1, n2] &
        #     n3|/     \|n4       [n6, n4, n5, n1]
        #        \     /           n6 = (n3+n4+n1)/3.
        #         \   /           
        #          \ /       
        #           n0

        #           n1      
        #          / \            
        #         /   \      
        #        /     \          
        #     n2|\     /|n5       
        #       | \   / |     ==> [n7, n5, n1, n2] & [n3, n0, n7, n2] &
        #     n3|  \n7  |n4       [n0, n4, n5, n7]
        #        \  |  /          n7 = (n2+n0+n5)/3.
        #         \ | /           
        #          \|/       
        #           n0

        if (n0.pinned() and n1.pinned()) and \
           (quad0.dominantPixel(skel.MS) != quad1.dominantPixel(skel.MS)):
            return []

        i = quad0.nodes.index(n1)
        n2 = quad0.nodes[(i+1)%4]
        n3 = quad0.nodes[(i+2)%4]
        i = quad1.nodes.index(n0)
        n4 = quad1.nodes[(i+1)%4]
        n5 = quad1.nodes[(i+2)%4]

        parents = quad0.getParents() + quad1.getParents()

        A = ProvisionalQuad([n0, n4, n2, n3], parents=parents)
        B = ProvisionalQuad([n4, n5, n1, n2], parents=parents)
        change0 = skeleton.ProvisionalChanges(skel)
        change0.insertElements(A,B)
        change0.removeElements(quad0, quad1)

        C = ProvisionalQuad([n0, n4, n5, n3], parents=parents)
        D = ProvisionalQuad([n5, n1, n2, n3], parents=parents)
        change1 = skeleton.ProvisionalChanges(skel)
        change1.insertElements(C, D)
        change1.removeElements(quad0, quad1)

        pos = (n3.position()+n4.position()+n1.position())/3.0
        n6 = skel.newNode(pos.x, pos.y)
        E = ProvisionalQuad([n0, n4, n6, n3], parents=parents)
        F = ProvisionalQuad([n3, n6, n1, n2], parents=quad0.getParents())
        G = ProvisionalQuad([n6, n4, n5, n1], parents=quad1.getParents())
        change2 = skeleton.ProvisionalInsertion(skel)
        change2.addNode(n6)
        change2.insertElements(E, F, G)
        change2.removeElements(quad0, quad1)

        pos = (n2.position()+n0.position()+n5.position())/3.0
        n7 = skel.newNode(pos.x, pos.y)
        H = ProvisionalQuad([n7, n5, n1, n2], parents=parents)
        I = ProvisionalQuad([n3, n0, n7, n2], parents=quad0.getParents())
        J = ProvisionalQuad([n0, n4, n5, n7], parents=quad1.getParents())
        change3 = skeleton.ProvisionalInsertion(skel)
        change3.addNode(n7)
        change3.insertElements(H, I, J)
        change3.removeElements(quad0, quad1)

        # If source elements are 100 % homogeneous with the same dominant pixel,
        # resulting elements will be so.
        if quad0.homogeneity(skel.MS)==1. and quad1.homogeneity(skel.MS)==1. and \
           quad0.dominantPixel(skel.MS)==quad1.dominantPixel(skel.MS):
            A.copyHomogeneity(quad0)
            B.copyHomogeneity(quad0)
            C.copyHomogeneity(quad0)
            D.copyHomogeneity(quad0)
            E.copyHomogeneity(quad0)
            F.copyHomogeneity(quad0)
            G.copyHomogeneity(quad0)
            H.copyHomogeneity(quad0)
            I.copyHomogeneity(quad0)
            J.copyHomogeneity(quad0)

        return [change0, change1, change2, change3]

########################################################

#     END 2D RULES BEGIN 3D RULES

#########################################################

elif config.dimension() == 3:

    def twoToThreeSwap(skel, tet1, tet2, sn):

        if (sn[0].pinned() and sn[1].pinned() and sn[2].pinned()):
            return []

        faceToNodeMap = tet1.faceToNodeMap()
        unsharedNode1 = [n for n in tet1.nodes if n not in sn][0]
        unsharedNode2 = [n for n in tet2.nodes if n not in sn][0]
        change = skeleton.ProvisionalChanges(skel)
        change.removeElements(tet1,tet2)
        uniform = (tet1.homogeneity(skel.MS)==1. and tet2.homogeneity(skel.MS)==1. and \
                       tet1.dominantPixel(skel.MS)==tet2.dominantPixel(skel.MS))
        for face in faceToNodeMap:
            nodes = [tet2.nodes[i] for i in face]
            if unsharedNode2 in nodes:
                nodes.reverse()
                nodes.append(unsharedNode1)
                tet = ProvisionalTetra(nodes,parents=[tet1,tet2])
                if not tet.onBoundary(skel):
                    change.insertElements(tet)
                    if uniform:
                        tet.copyHomogeneity(tet1)

        
        return [change]

                            


        
