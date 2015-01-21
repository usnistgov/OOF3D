# -*- python -*-
# $RCSfile: rationalsharp.py,v $
# $Revision: 1.27.12.2 $
# $Author: langer $
# $Date: 2014/08/20 02:21:22 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# This file is not used in 3D.

from ooflib.SWIG.common import config
assert config.dimension() == 2

from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import rationalize
from ooflib.engine import skeleton
from ooflib.engine import skeletonelement
import math

ProvisionalTriangle = skeletonelement.ProvisionalTriangle
ProvisionalQuad = skeletonelement.ProvisionalQuad

class RemoveBadTriangle(rationalize.Rationalizer):
    #
    #             C
    #            /|
    #           / |  If an interior angle A-C-B is too small,
    #          /  |  it's better to remove this triangle.
    #         /   |  
    #        /____|  This case involves a "merging" process.
    #        A    B  (merging of two nodes, A and B)
    #
    def __init__(self, acute_angle, obtuse_angle):
        self.acute_angle = acute_angle
        self.obtuse_angle = obtuse_angle
        self.acute = math.cos(acute_angle*math.pi/180.0)
        self.obtuse = math.cos(obtuse_angle*math.pi/180.0)

    def findAndFix(self, skel, element):
        if element.nnodes() == 4:
            return []
        
        obtuse_angle = None
        acuteCheck = None
        for i in range(3):
            if element.cosCornerAngle(i) <= self.obtuse:
                obtuse_angle = i
        for i in range(3):
            if element.cosCornerAngle(i) >= self.acute:
                acuteCheck = i
                break

        # See if there is any violation ....
        if obtuse_angle is None and acuteCheck is None:
            return []

        # Let's fix them.
        if obtuse_angle is None:
            obtuse_angle = element.getBiggestAngle()
        acute_angles = [(obtuse_angle+1)%3, (obtuse_angle+2)%3]
        return self.fix(skel, element, obtuse_angle, acute_angles)

    def fixAll(self, skel, element):
        if element.nnodes() == 4:
            return []
        obtuse_angle = element.getBiggestAngle()
        acute_angles = [(obtuse_angle+1)%3, (obtuse_angle+2)%3]
        return self.fix(skel, element, obtuse_angle, acute_angles)

    def fix(self, skel, element, obtuse_angle, acute_angles):
        return (_obtuseHandler(skel, element, obtuse_angle)
                + _acuteHandler(skel, element, acute_angles[0])
                + _acuteHandler(skel, element, acute_angles[1]))

def _acuteHandler(skel, element, index):
    # Merge the two nodes opposite the sharp angle.
    node0 = element.nodes[(index+1)%3]
    node1 = element.nodes[(index+2)%3]
    return [skel.mergeNodePairs((node0, node1)),
            skel.mergeNodePairs((node1, node0))]

def _obtuseHandler(skel, element, index):
    # A obtuse triangle. What we do depends on what kind of element
    # borders the side joining the two sharp angles.
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
              for el in anchor.aperiodicNeighborElements()
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
                      for el in anchor.aperiodicNeighborElements()
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

#########################################################

registeredclass.Registration(
    'Remove Bad Triangles',
    rationalize.Rationalizer,
    RemoveBadTriangle,
    gerund = 'removing bad triangles',
    ordering=20000,                     # do this last!
    params=[
    parameter.FloatRangeParameter('acute_angle', (0.0, 45.0, 0.5),
                                  value = 15.0,
                                  tip = 'Minimum acceptable acute interior angle, in degrees'),
    parameter.FloatRangeParameter('obtuse_angle', (90.0, 180.0, 1.0),
                                  value = 150.0,
                                  tip = 'Maximum acceptable obtuse interior angle, in degrees')],
    tip = 'Remove triangles with extreme interior angles.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/ration_sharp.xml'))
