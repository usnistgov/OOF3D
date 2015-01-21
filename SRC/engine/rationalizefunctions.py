# -*- python -*-
# $RCSfile: rationalizefunctions.py,v $
# $Revision: 1.11.2.5 $
# $Author: langer $
# $Date: 2014/11/05 16:54:30 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config

assert config.dimension() == 2

from ooflib.common import debug
from ooflib.common import primitives
if config.dimension() == 2:
    from ooflib.engine import skeleton
    from ooflib.engine import skeletonelement
elif config.dimension() == 3:
    from ooflib.engine import skeleton3d as skeleton
    from ooflib.engine import skeletonelement3d as skeletonelement

ProvisionalChanges = skeleton.ProvisionalChanges
if config.dimension() == 2:
    ProvisionalTriangle = skeletonelement.ProvisionalTriangle
    ProvisionalQuad = skeletonelement.ProvisionalQuad
elif config.dimension() == 3:
    ProvisionalTetra = skeletonelement.ProvisionalTetra




def removeShortSide(skel, element, which):
    node0 = element.nodes[which]
    node1 = element.nodes[(which+1)%4]
    return [skel.mergeNode(node0, node1),
            skel.mergeNode(node1, node0)]

#############################################################

def quadSplit(skel, element, which):
    nodes = element.nodes
    parents = element.getParents()
    if which%2 == 0:
        triangles = (ProvisionalTriangle([nodes[0], nodes[1], nodes[2]],
                                         parents=parents),
                     ProvisionalTriangle([nodes[0], nodes[2], nodes[3]],
                                         parents=parents))
    else:
        triangles = (ProvisionalTriangle([nodes[1], nodes[2], nodes[3]],
                                         parents=parents),
                     ProvisionalTriangle([nodes[0], nodes[1], nodes[3]],
                                         parents=parents))
    change = ProvisionalChanges(skel)
    change.removeElements(element)
    change.insertElements(*triangles)
    return [change]

#############################################################

def removeBadTriangle(skel, element, obtuse_angle, acute_angles):
    return obtuseHandler(skel, element, obtuse_angle) + \
           acuteHandler(skel, element, acute_angles[0]) + \
           acuteHandler(skel, element, acute_angles[1])
        
def acuteHandler(skel, element, index):
    # Merge the two nodes opposite the sharp angle.
    node0 = element.nodes[(index+1)%3]
    node1 = element.nodes[(index+2)%3]
    return [skel.mergeNode(node0, node1),
            skel.mergeNode(node1, node0)]

def obtuseHandler(skel, element, index):
    # A obute triangle. What we do depends on
    # what kind of element borders the side joining the
    # two sharp angles.
    anchor = element.nodes[index] # wide corner
    itchy = element.nodes[(index+1)%3] # sharp corner
    scratchy = element.nodes[(index+2)%3] # sharp corner
    borderelement = element.getSisterPeriodic(skel, itchy, scratchy)
    if borderelement is None:
        return triNoneSplit(skel, anchor, itchy, scratchy,
                            element)
    if borderelement.nnodes() == 3:
        return triTriSplit(skel, anchor, itchy, scratchy,
                           element, borderelement)
    if borderelement.nnodes() == 4:
        return triQuadSplit(skel, anchor, itchy, scratchy,
                            element, borderelement)
    return []

# Compute the midpoint between the given pair of nodes.  If the pair
# is along a periodic edge, also return the midpoint of the periodic
# partners, making sure that both midpoints are exactly on the
# periodic edge, and that they line up exactly with each other.

def _midpoints(skel, node0, node1):
    assert config.dimension() == 2
    n0pos = node0.position()
    n1pos = node1.position()
    partners = node0.getPartnerPair(node1)
    if not partners:
        return 0.5*(n0pos + n1pos), None
    
    if n0pos.x == n1pos.x: # vertical boundary
        ymid = 0.5*(n0pos.y + n1pos.y)
        if n0pos.x == 0.0:              # left boundary
            return (primitives.Point(n0pos.x, ymid),
                    primitives.Point(skel.MS.size()[0], ymid))
        return (primitives.Point(skel.MS.size()[0], ymid), # right boundary
                primitives.Point(0.0, ymid))
    if n0pos.y == n1pos.y:
        xmid = 0.5*(n0pos.x + n1pos.x)
        if n0pos.y == 0.0:              # bottom boundary
            return (primitives.Point(xmid, 0.0),
                    primitives.Point(xmid, skel.MS.size()[1]))
        return (primitives.Point(xmid, skel.MS.size()[1]), # top boundary
                primitives.Point(xmid, 0.0))
        

def triQuadSplit(skel, anchor, itchy, scratchy, tri, quad):

    # If tri.dominantPixel is different from quad.dominantPixel ...
    # Pick the best of three configurations.
    #            ___________        ______      ______      ______
    # scratchy /|          Q1       |   /|      |   /|      |    |
    #         / |          |        |C / |      |B / |      |    |
    #        /  |          |        | /  |      | /  |      |  B |
    #       /tri|  quad    |  ===>  |/   |      |/   |      |    |
    # anchor\   |          |        |\ B |      |    |      |\   |
    #        \  |          |        | \  |      | A  |      | \  |
    #         \ |          |        |A \ |      |    |      |A \ |
    #   itchy  \|__________Q0       |___\|      |____|      |___\|
    #

    # If tri & quad have same dominantPixel and aren't separated by a
    # periodic boundary, consider this geometry as well:
    #            ___________            _________
    #          /|          |           /      . |
    #         / |          |          / C  .    |
    #        /  |          |         /  .       | 
    #       /tri|  quad    |  ===>  /.     B    | Three different cases
    #       \   |          |        \   .       | as in the above
    #        \  |          |         \     .    |
    #         \ |          |          \  A    . |
    #          \|__________|           \________|
    #

    # If itchy and scratchy are pinned, the process should be aborted
    if itchy.pinned() and scratchy.pinned():
        return []

    # Find the midpoint of the segment, and its periodic partner, if
    # it exists.
    midpoint, midpointQ = _midpoints(skel, itchy, scratchy)
    periodic = midpointQ is not None

    # Find the nodes of the quad that correspond to itchy and
    # scratchy.  If the border between tri and quad is a periodic
    # boundary, these nodes aren't the same as itchy and scratchy!
    if periodic:
        partners = itchy.getPartnerPair(scratchy)
        itchyQ, scratchyQ = partners
    else:
        itchyQ, scratchyQ = itchy, scratchy
    
    # Find nodes Q0 and Q1
    quadnodes = quad.nodes
    itchyindex = quadnodes.index(itchyQ)
    q0 = quadnodes[(itchyindex+1)%4]
    q1 = quadnodes[(itchyindex+2)%4]

    parents = quad.getParents()
    changes = []
    
    # Cases that move the anchor point.  Don't do these at all if the
    # anchor is a periodic node or not otherwise movable:
    if anchor.movable_x() and anchor.movable_y() and not anchor.getPartners():
        # Divide the quad into three triangles.  The periodic case is
        # complicated because it has to replace the aperiodic anchor
        # Node with a periodic one, and that requires replacing all of
        # the elements connected to the anchor point.  We do the
        # periodic and aperiodic cases completely separately here.
        if not periodic:
            change0 = skeleton.ProvisionalChanges(skel)
            change0.moveNode(anchor, midpoint)
            change0.removeElements(tri, quad)
            change0.insertElements(
                ProvisionalTriangle([anchor, itchy, q0], parents=parents),
                ProvisionalTriangle([anchor, q0, q1], parents=parents),
                ProvisionalTriangle([anchor, q1, scratchy], parents=parents))

            change1 = skeleton.ProvisionalChanges(skel)
            change1.moveNode(anchor, midpoint)
            change1.removeElements(tri, quad)
            parents = quad.getParents()
            change1.insertElements(
                ProvisionalQuad([anchor, itchy, q0, q1], parents=parents),
                ProvisionalTriangle([anchor, q1, scratchy], parents=parents))

            change2 = skeleton.ProvisionalChanges(skel)
            change2.moveNode(anchor, midpoint)
            change2.removeElements(tri, quad)
            parents = quad.getParents()
            change2.insertElements(
                ProvisionalTriangle([anchor, itchy, q0], parents=parents),
                ProvisionalQuad([anchor, q0, q1, scratchy], parents=parents))
        else:
            # Three ways of moving the anchor point to the *periodic*
            # boundary and dividing the quad.
            newanchor, anchorQ, elsubs = triquadhelper(skel, tri, anchor,
                                                       midpoint, midpointQ)
            change0 = skeleton.ProvisionalInsertion(skel)
            change0.removeElements(quad, tri)
            change0.addNode(newanchor)
            change0.addNode(anchorQ)
            for oldel, newel in elsubs:
                change0.substituteElement(oldel, newel)
            change0.insertElements(
                ProvisionalTriangle([anchorQ, itchyQ, q0], parents=parents),
                ProvisionalTriangle([anchorQ, q0, q1], parents=parents),
                ProvisionalTriangle([anchorQ, q1, scratchyQ], parents=parents))

            newanchor, anchorQ, elsubs = triquadhelper(skel, tri, anchor,
                                                       midpoint, midpointQ)
            change1 = skeleton.ProvisionalInsertion(skel)
            change1.removeElements(quad, tri)
            change1.addNode(newanchor)
            change1.addNode(anchorQ)
            for oldel, newel in elsubs:
                change1.substituteElement(oldel, newel)
            change1.insertElements(
                ProvisionalQuad([anchorQ, itchyQ, q0, q1], parents=parents),
                ProvisionalTriangle([anchorQ, q1, scratchyQ], parents=parents)
                )

            newanchor, anchorQ, elsubs = triquadhelper(skel, tri, anchor,
                                                       midpoint, midpointQ)
            change2 = skeleton.ProvisionalInsertion(skel)
            change2.removeElements(quad, tri)
            change2.addNode(newanchor)
            change2.addNode(anchorQ)
            for oldel, newel in elsubs:
                change2.substituteElement(oldel, newel)
            change2.insertElements(
                ProvisionalTriangle([anchorQ, itchyQ, q0], parents=parents),
                ProvisionalQuad([anchorQ, q0, q1, scratchyQ], parents=parents)
                )
            
        changes.extend([change0, change1, change2])


    # Cases for lazy (immobile) anchor.  These can only be done if tri
    # and quad don't span a periodic boundary.
    if not periodic:
        change3 = skeleton.ProvisionalChanges(skel)
        change3.removeElements(tri, quad)
        parents = quad.getParents() + tri.getParents()
        change3.insertElements(
            ProvisionalTriangle([anchor, itchy, q0], parents=parents),
            ProvisionalTriangle([anchor, q0, q1], parents=parents),
            ProvisionalTriangle([anchor, q1, scratchy], parents=parents))

        change4 = skeleton.ProvisionalChanges(skel)
        change4.removeElements(tri, quad)
        parents = quad.getParents()
        change4.insertElements(
            ProvisionalQuad([anchor, itchy, q0, q1], parents=parents),
            ProvisionalTriangle([anchor, q1, scratchy], parents=parents))

        change5 = skeleton.ProvisionalChanges(skel)
        change5.removeElements(tri, quad)
        parents = quad.getParents()
        change5.insertElements(
            ProvisionalTriangle([anchor, itchy, q0], parents=parents),
            ProvisionalQuad([anchor, q0, q1, scratchy], parents=parents))

        changes.extend([change3, change4, change5])
    
    return changes

# Helper function that contains code repeated in TriQuadRationalize
# for periodic skeletons.  The code has to be repeated because the
# nodes and elements used in a ProvisionalChanges object can't be
# shared with other ProvisionalChanges objects.

def triquadhelper(skel, tri, anchor, midpoint, midpointQ):
    newanchor = skel.newNode(midpoint.x, midpoint.y) # PeriodicSkeletonNode
    anchorQ = skel.newNode(midpointQ.x, midpointQ.y)
    newanchor.addPartner(anchorQ)
    elsubs = [(el, el.provisionalReplacement(anchor, newanchor))
              for el in anchor.aperiodicNeighborElements(skel)
              if el is not tri]
    return newanchor, anchorQ, elsubs
    

###########################################################################

def triTriSplit(skel, anchor, itchy, scratchy, tri1, tri2):
    #
    #                                  
    # scratchy /|\               |\    
    #         / | \              | \   
    #        /  |  \           C | A\   If tri1.dominantPixel is different
    #       /tri|tri\T0    ===>  |___\  from tri2.dominantPixel ...
    # anchor\ 1 | 2 /            |   / 
    #        \  |  /           D | B/  
    #         \ | /              | /   
    #   itchy  \|/               |/    
    #
    #
    #          /|\              / \
    #         / | \            /   \
    #        /  |  \          /     \   If tri1.dominantPixel is the same as
    #       /tri|tri\   ===> /_______\  from tri2.dominantPixel ...
    #       \ 1 | 2 /        \       /
    #        \  |  /          \     /
    #         \ | /            \   /
    #          \|/              \ /
    #                            

    # If itchy and scratchy are pinned, the process should be aborted
    if itchy.pinned() and scratchy.pinned():
        return []

    # Find the midpoint of the segment, and its periodic partner, if
    # it exists.
    midpoint, midpoint2 = _midpoints(skel, itchy, scratchy)
    periodic = midpoint2 is not None

    # Find the nodes of tri2 that correspond to itchy and scratchy.
    # If the border between tri and quad is a periodic boundary, these
    # nodes aren't the same as itchy and scratchy!
    if periodic:
        partners = itchy.getPartnerPair(scratchy)
        itchy2, scratchy2 = partners
    else:
        itchy2, scratchy2 = itchy, scratchy

    tri2nodes = tri2.nodes
    t0 = tri2nodes[(tri2nodes.index(itchy2) + 1) % 3]
    parents = tri2.getParents()
    changes = []

    if anchor.movable_x() and anchor.movable_y() and not anchor.getPartners():
        if not periodic:
            change0 = skeleton.ProvisionalChanges(skel)
            change0.moveNode(anchor, midpoint)
            change0.removeElements(tri1, tri2)
            change0.insertElements(
                ProvisionalTriangle([anchor, t0, scratchy], parents=parents),
                ProvisionalTriangle([anchor, itchy, t0], parents=parents))
        else:                           # periodic
            change0 = skeleton.ProvisionalInsertion(skel)
            newanchor = skel.newNode(midpoint.x, midpoint.y)
            anchor2 = skel.newNode(midpoint2.x, midpoint2.y)
            newanchor.addPartner(anchor2)
            elsubs = [(el, el.provisionalReplacement(anchor, newanchor))
                      for el in anchor.aperiodicNeighborElements(skel)
                      if el is not tri1]
            change0.removeElements(tri1, tri2)
            for oldel, newel in elsubs:
                change0.substituteElement(oldel, newel)
            change0.insertElements(
                ProvisionalTriangle([anchor2, t0, scratchy2], parents=parents),
                ProvisionalTriangle([anchor2, itchy2, t0], parents=parents))
            change0.addNode(newanchor)
            change0.addNode(anchor2)
        changes.append(change0)

    if not periodic:
        change1 = skeleton.ProvisionalChanges(skel)
        change1.removeElements(tri1, tri2)
        parents = tri1.getParents() + tri2.getParents()
        change1.insertElements(
            ProvisionalTriangle([anchor, t0, scratchy], parents=parents),
            ProvisionalTriangle([anchor, itchy, t0], parents=parents))
        changes.append(change1)

    return changes

##############################################################################

def triNoneSplit(skel, anchor, itchy, scratchy, tri):
    #                                  
    # scratchy /|                |
    #         / |                |
    #        /  |              A |
    #   ____/tri|   ===>     ----|
    # anchor\   |                |
    #        \  |              B |
    #         \ |                |
    #   itchy  \|                |
    #

    # Exit conditions
    if anchor.pinned(): return []
    if itchy.pinned() and scratchy.pinned(): return []
    
    change = skeleton.ProvisionalChanges(skel)
    change.moveNode(anchor,
                    position=0.5*(itchy.position() + scratchy.position()),
                    mobility=(itchy.movable_x() or scratchy.movable_x(),
                              itchy.movable_y() or scratchy.movable_y()))
    change.removeElements(tri)
    change.substituteSegment(skel.getSegment(itchy,scratchy),
                             [skel.getSegment(anchor,itchy),
                              skel.getSegment(anchor,scratchy)])
    return [change]


# Compute the centroid for all the nodes as well as the midpoints for
# each pair of nodes. If the pair is along a periodic edge, also
# return the midpoint of the periodic partners, making sure that both
# midpoints are exactly on the periodic edge, and that they line up
# exactly with each other.

if config.dimension() == 3:

    def removeBadTetra(skel, element, obtuse_angles, acute_angles):
        faceToNodeMap = element.faceToNodeMap()

        merges = []
        for i,j in acute_angles:
            facenodes = faceToNodeMap[i]
            node0 = element.nodes[facenodes[(j+1)%3]]
            node1 = element.nodes[facenodes[(j+2)%3]]
            merges.append(skel.mergeNode(node0, node1))
            merges.append(skel.mergeNode(node1, node0))

        splits = []
        for i,j in obtuse_angles:
            obtusenodeidx = faceToNodeMap[i][j]
            for k in range(len(faceToNodeMap)):
                if obtusenodeidx not in faceToNodeMap[k]:
                    oppfacenodes = [element.nodes[l] for l in faceToNodeMap[k]]
            borderelement = element.getSisterPeriodic(skel, oppfacenodes)
            if borderelement is not None:
                for node in borderelement.nodes:
                    if node not in oppfacenodes:
                        oppnode = node
                splits.extend(tetTetSplit(skel, element.nodes[obtusenodeidx], 
                                     oppnode, element, borderelement))


        return merges+splits


    def _centroidAndMidpoints(skel, nodes):
        n = len(nodes)
        points = []
        pairs = [(nodes[i],nodes[(i+1)%n]) for i in range(n)]
        periodic = True
        for n0,n1 in pairs:
            points.append(_midpoints(skel,n0,n1))
            periodic = periodic and (points[-1][1] is not None)
        centroid = primitives.Point(0.0,0.0,0.0)
        for node in nodes:
            centroid = (1.0/n)*node.position()
        if not periodic:
            partner = None
        points.append((centroid,partner))
        return points


    def tetTetSplit(skel, obtusenode, oppnode, tet1, tet2):
        # obtusenode is the node in tet1 with a wide angle, oppnode is
        # the node in tet2 that is NOT shared between tet1 and tet2.

        # print "in tetTetSplit"
        # print obtusenode.position()

        changes = []
        faces = tet2.faceToNodeMap()
        
        unSharedFaces = []
        for face in faces:
            if oppnode in [tet2.nodes[i] for i in face]:
                unSharedFaces.append(face)
        sharedNodes = []
        for node in tet2.nodes:
            if node is not oppnode:
                sharedNodes.append(node)
        midpoints = _centroidAndMidpoints(skel, sharedNodes)
        periodic = midpoints[-1][1] is not None


        # first just split the two into three, without moving the obtusenode
        if not periodic:
            change = skeleton.ProvisionalChanges(skel)
            change.removeElements(tet1, tet2)
            parents = tet1.getParents() + tet2.getParents()
            tetra = []
            for face in unSharedFaces:
                nodes = [tet2.nodes[i] for i in face]
                nodes.reverse()
                nodes.append(obtusenode)
                change.insertElements(ProvisionalTetra(nodes,parents=parents))
            print change, change.illegal(skel)
            #print unSharedFaces, [el.illegal() for el in change.elAfter()]
            changes.append(change)

            # for the first three midpoints, we split into two tetra
            #for i in range(3):
            #    pair = (sharedNodes[i],sharedNodes[(i+1)%3])
            #    midpoint = midpoints[i][0]
            #    if obtusenode.canMoveTo(midpoint):
            #        change = skeleton.ProvisionalChanges(skel)
            #        change.moveNode(obtusenode, midpoint)
            #        change.removeElements(tet1, tet2)
            #        for face in unSharedFaces:
            #            nodes = [tet2.nodes[j] for j in face]
            #            nodes.reverse()
            #            nodes.append(obtusenode)
            #            if not (pair[0] in nodes and pair[1] in nodes):
            #                change.insertElements(ProvisionalTetra(nodes,parents=tet2.getParents()))
            #            else:
            #                otherneighbor = tet2.getSisterPeriodic(skel, nodes)
            #        print midpoint, pair, otherneighbor
            #        print "num elements", len(change.elAfter())
            #        for el in change.elAfter():
            #if el.illegal():
            #                print "illegal element:"
            #                nodes = el.nodes
            #                for node in el.nodes:
            #                    print node.position()
            #                testel = ProvisionalTetra([nodes[0],nodes[2],nodes[1],nodes[3]], parents=parents)
            #                print "reordering tetra: ", testel.illegal()
            #        if otherneighbor == None:
            #            changes.append(change)


            centroid = midpoints[3][0]
            if obtusenode.canMoveTo(centroid):
                change = skeleton.ProvisionalChanges(skel)
                change.moveNode(obtusenode, centroid)
                change.removeElements(tet1, tet2)
                tetra = []
                for face in unSharedFaces:
                    nodes = [tet2.nodes[i] for i in face]
                    nodes.reverse()
                    nodes.append(obtusenode)
                    change.insertElements(ProvisionalTetra(nodes,parents=tet2.getParents()))
                changes.append(change)


        return changes
