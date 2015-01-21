# -*- python -*-
# $RCSfile: skeleton.py,v $
# $Revision: 1.346.2.6 $
# $Author: langer $
# $Date: 2014/09/17 21:26:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# A Skeleton contains the geometry of a finite element mesh, without
# any of the details.  It has lists of SkeletonElements,
# SkeletonNodes, and SkeletonEdgeBoundary (made up of SkeletonEdges).
# but no intermediate nodes, materials, or shape functions.

## THIS FILE IS NOT USED IN 3D AND SHOULD NOT BE IMPORTED
from ooflib.SWIG.common import config
assert config.dimension() == 2

from ooflib.SWIG.common import coord
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import progress
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import timestamp
from ooflib.SWIG.engine import femesh
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import microstructure
from ooflib.common import parallel_enable
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import runtimeflags
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletonboundary
from ooflib.engine import skeletoncontext
from ooflib.engine import skeletondiff
from ooflib.engine import skeletonelement
from ooflib.engine import skeletongroups
from ooflib.engine import skeletonnode
from ooflib.engine import skeletonsegment
from ooflib.engine import skeletonselectable

from ooflib.engine import materialmanager

import math
import random
import time
import types
import weakref
import sys

Registration = registeredclass.Registration

SkeletonNode = skeletonnode.SkeletonNode
PeriodicSkeletonNode = skeletonnode.PeriodicSkeletonNode
SkeletonEdgeBoundary = skeletonboundary.SkeletonEdgeBoundary
ExteriorSkeletonEdgeBoundary = skeletonboundary.ExteriorSkeletonEdgeBoundary
SkeletonPointBoundary = skeletonboundary.SkeletonPointBoundary
ExteriorSkeletonPointBoundary = skeletonboundary.ExteriorSkeletonPointBoundary
SkeletonEdge = skeletonsegment.SkeletonEdge
SkeletonQuad = skeletonelement.SkeletonQuad
SkeletonTriangle = skeletonelement.SkeletonTriangle
SkeletonSegment = skeletonsegment.SkeletonSegment
#PeriodicSkeletonSegment = skeletonsegment.PeriodicSkeletonSegment

# Triangular skeleton arrangements

class Arrangement(
    enum.EnumClass(('conservative', 'leaning to the right'),
                   ('liberal', 'leaning to the left'),
                   ('moderate', 'going both ways'),
                   ('middling', 'going both ways, the other way'),
                   ('anarchic', 'going every which way'))):
    tip = "Arrangement for triangular initial Skeleton."
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/enum/arrangement.xml')
    
utils.OOFdefine('Arrangement', Arrangement)

# Known arrangements.
conservative = Arrangement('conservative')
liberal = Arrangement('liberal')
moderate = Arrangement('moderate')
anarchic = Arrangement('anarchic')
middling = Arrangement('middling')


class SegmentData:
    def __init__(self,matname,leftskelel,rightskelel,interfacename):
        self._materialname=matname
        self._leftskelel=leftskelel
        self._rightskelel=rightskelel
        self._interfacenames=[interfacename]
    def setData(self,matname,leftskelel,rightskelel,interfacename):
        self._materialname=matname
        self._leftskelel=leftskelel
        self._rightskelel=rightskelel
        self._interfacenames.append(interfacename)

class SkeletonGeometry(registeredclass.RegisteredClass):
    registry = []
    def __init__(self, type):
        self.type = type
    tip = "Element shape for the initial Skeleton."
    discussion = """<para>
    <classname>SkeletonGeometry</classname> objects are used to
    specify the shape of the &elems; in the uniform &skel; created by
    <xref linkend='MenuItem-OOF.Skeleton.New'/>.
    </para>"""

    # much of the code needed by TriSkeleton and QuadSkeleton is repeated
    def createGridOfNodes(self, skel, prog, m, n):
        # both the QuadSkeleton and TriSkeleton begin with a
        # rectangular grid of nodes

        ## TODO MER: Change names of boundaries Xmin, Ymax, etc. to be
        ## compatible with 3D.

        btmlft = skel.getPointBoundary('bottomleft', exterior=1)
        btmrgt = skel.getPointBoundary('bottomright', exterior=1)
        toplft = skel.getPointBoundary('topleft', exterior=1)
        toprgt = skel.getPointBoundary('topright', exterior=1)

        ## create nodes and selected point boundaries.
        dx = (skel.MS.size()[0]*1.0)/m   # Promote numerators to floating-point.
        dy = (skel.MS.size()[1]*1.0)/n
        tot_items = (m + 1)*(n + 1)
        for i in range(n+1):
            for j in range(m+1):
                # set upper and right edges exactly to avoid roundoff
                if i == n:
                    y = skel.MS.size()[1]
                else:
                    y = i*dy
                if j == m:
                    x = skel.MS.size()[0]
                else:
                    x = j*dx

                node = skel.newNode(x,y)
                # set node partners
                if self.top_bottom_periodicity and i==n:
                    node.addPartner(skel.getNode(j))
                if self.left_right_periodicity and j==m:
                    node.addPartner(skel.getNode(i*(m+1)))
                # set partners diagonal from each other as well
                if self.left_right_periodicity and self.top_bottom_periodicity:
                    if i==n and j==0:
                        node.addPartner(skel.getNode(m))
                    if i==n and j==m:
                        node.addPartner(skel.getNode(0))
                # add nodes to corner boundaries
                if i==0 and j==0:
                    btmlft.addNode(node)
                if i==0 and j==m:
                    btmrgt.addNode(node)
                if i==n and j==0:
                    toplft.addNode(node)
                if i==n and j==m:
                    toprgt.addNode(node)
                if prog.stopped():
                    return
                nn = i*(n+1)+j+1
                prog.setFraction(1.0*nn/tot_items)
                prog.setMessage("Allocated %d/%d nodes" % (nn, tot_items))
                               


    def addGridSegmentsToBoundaries(self, skel, i, j, m, n):
        # both the QuadSkeleton and TriSkeleton add the same
        # segments to the edge boundaries
        if j == 0: 
            ll = i*(m+1) + j            # lower left node index
            ul = (i+1)*(m+1) + j        # upper left  
            lft = skel.getEdgeBoundary('left', exterior=1)
            segment = skel.segments[
                skeletonnode.canonical_order(skel.nodes[ul],
                                             skel.nodes[ll])]
            edge = SkeletonEdge(segment)
            edge.set_direction(skel.nodes[ul], skel.nodes[ll])
            lft.addEdge(edge)

        if j == (m-1):
            lr = i*(m+1) + j+1          # lower right
            ur = (i+1)*(m+1) + j+1      # upper right
            rgt = skel.getEdgeBoundary('right', exterior=1)
            segment = skel.segments[
                skeletonnode.canonical_order(skel.nodes[lr],
                                             skel.nodes[ur])]
            edge = SkeletonEdge(segment)
            edge.set_direction(skel.nodes[lr], skel.nodes[ur])
            rgt.addEdge(edge)
##             if self.left_right_periodicity:
##                 skel.makeSegmentPartners(segment,skel.segments[
##                     skeletonnode.canonical_order(skel.nodes[i*(m+1)],
##                                                  skel.nodes[(i+1)*(m+1)])])

        if i == 0:
            ll = i*(m+1) + j            # lower left node index
            lr = i*(m+1) + j+1          # lower right
            btm = skel.getEdgeBoundary('bottom', exterior=1)
            segment = skel.segments[
                skeletonnode.canonical_order(skel.nodes[ll],
                                             skel.nodes[lr])]
            edge = SkeletonEdge(segment)
            edge.set_direction(skel.nodes[ll], skel.nodes[lr])
            btm.addEdge(edge)

        if i == (n-1):
            ur = (i+1)*(m+1) + j+1      # upper right
            ul = (i+1)*(m+1) + j        # upper left
            top = skel.getEdgeBoundary('top', exterior=1)
            segment = skel.segments[
                skeletonnode.canonical_order(skel.nodes[ur],
                                             skel.nodes[ul])]
            edge = SkeletonEdge(segment)
            edge.set_direction(skel.nodes[ur], skel.nodes[ul])
            top.addEdge(edge)

           

class QuadSkeleton(SkeletonGeometry):
    def __init__(self, left_right_periodicity=False,
                 top_bottom_periodicity=False):
        SkeletonGeometry.__init__(self, 'quad')
        self.left_right_periodicity = left_right_periodicity
        self.top_bottom_periodicity = top_bottom_periodicity
    def __call__(self, m, n, microStructure, preset_homog=0):
        # Create a skeleton of quadrilateral elements, n rows by m
        # columns.  The width and height of the entire skeleton are h
        # and w.
        prog = progress.getProgress("Skeleton", progress.DEFINITE)
        try:
            skel = Skeleton(microStructure, self.left_right_periodicity,
                            self.top_bottom_periodicity)
            skel.reserveNodes((m+1)*(n+1))
            skel.reserveElements(m*n)

            ## create nodes and selected point boundaries.
            self.createGridOfNodes(skel, prog, m, n)

            ## create elements and edges
            tot_items = m*n
            for i in range(n):                  # loop over rows of elements
                for j in range(m):              # loop over columns of elements
                    ll = i*(m+1) + j            # lower left node index
                    lr = i*(m+1) + j+1          # lower right
                    ur = (i+1)*(m+1) + j+1      # upper right
                    ul = (i+1)*(m+1) + j        # upper left
                    el = skel.newElement([skel.nodes[ll],skel.nodes[lr],
                                          skel.nodes[ur],skel.nodes[ul]])
                    # Simple skeleton -- set the homogeneity to "1".
                    if preset_homog:
                        dom_pixel = microStructure.categoryFromPoint(
                            el.repr_position())
                        el.setHomogeneous(dom_pixel)
    ##                    el.cachedHomogData.value = cskeleton.HomogeneityData(
    ##                        1.0,dom_pixel)

                    # Element constructors make the segments, we can use them
                    # to make the edges and add them to the boundaries.

                    #To create default boundaries as interfaces
                    #instead of skeleton boundaries, comment or remove
                    #the following line.
                    self.addGridSegmentsToBoundaries(skel, i, j, m, n)
                    el.findHomogeneityAndDominantPixel(skel.MS)

                    if prog.stopped():
                        return None
                    rectangle_count = i*m+j+1
                    prog.setFraction(float(rectangle_count)/tot_items)
                    prog.setMessage("Created %d/%d elements"
                                    % (rectangle_count, tot_items))
            return skel
        finally:
            prog.finish()
Registration(
    'QuadSkeleton',
    SkeletonGeometry,
    QuadSkeleton,
    0,
    params=[parameter.BooleanParameter('left_right_periodicity',value=False,default=False,
                  tip="Whether or not the skeleton has periodicity in the horizontal direction"),
            parameter.BooleanParameter('top_bottom_periodicity',value=False,default=False,
                  tip="Whether or not the skeleton has periodicity in the vertical direction")],
    tip="A Skeleton of quadrilateral elements.",
    discussion="""<para>
    <classname>QuadSkeleton</classname> is used as the
    <varname>skeleton_geometry</varname> argument of <xref
    linkend='MenuItem-OOF.Skeleton.New'/>, specifying that it is to
    create a &skel; with quadrilateral &elems;.
    </para>""")
    

class TriSkeleton(SkeletonGeometry):
    def __init__(self, arrangement=moderate, left_right_periodicity=False,
                 top_bottom_periodicity=False):
        SkeletonGeometry.__init__(self, 'tri')
        self.arrangement = arrangement
        self.left_right_periodicity = left_right_periodicity
        self.top_bottom_periodicity = top_bottom_periodicity
    def __call__(self, m, n, microStructure, preset_homog=0):
        prog = progress.getProgress("Skeleton", progress.DEFINITE)
        try:
            skel = Skeleton(microStructure, self.left_right_periodicity,
                     self.top_bottom_periodicity)
            skel.reserveNodes((m+1)*(n+1))
            skel.reserveElements(2*m*n)

            ## create nodes
            self.createGridOfNodes(skel, prog, m, n)

            ## create elements and edges
            tot_items = m*n
            rightdiag = 1
            for i in range(n):                  # loop over rows of elements
                for j in range(m):              # loop over columns of elements
                    ll = i*(m+1) + j            # lower left node index
                    lr = i*(m+1) + j+1          # lower right
                    ur = (i+1)*(m+1) + j+1      # upper right
                    ul = (i+1)*(m+1) + j        # upper left

                    if self.arrangement == conservative:
                        rightdiag = 1
                    elif self.arrangement == liberal:
                        rightdiag = 0
                    elif self.arrangement == moderate:
                        rightdiag = (i+j)%2
                    elif self.arrangement == middling:
                        rightdiag = 1-(i+j)%2
                    elif self.arrangement == anarchic:
                        rightdiag = random.choice([0,1])
                    else:
                        debug.fmsg('unknown arrangement!', self.arrangement)


                    #  ul  _________  ur
                    #      |       /|
                    #      | el1  / |
                    #      |     /  |
                    #      |    /   |
                    #      |   /    |
                    #      |  /     |
                    #      | /  el2 |
                    #  ll  |/_______| lr
                    #
                    if rightdiag==1:
                        el1 = skel.newElement([skel.nodes[ll],skel.nodes[ur],
                                               skel.nodes[ul]])
                        el2 = skel.newElement([skel.nodes[ur],skel.nodes[ll],
                                               skel.nodes[lr]])
                    #
                    #  ul  _________  ur
                    #      |\       |
                    #      | \      |
                    #      |  \ el2 |
                    #      |   \    |
                    #      |    \   |
                    #      |     \  |
                    #      | el1  \ |
                    #  ll  |_______\| lr
                    #
                    else:
                        el1 = skel.newElement([skel.nodes[lr],skel.nodes[ul],
                                               skel.nodes[ll]])
                        el2 = skel.newElement([skel.nodes[ul],skel.nodes[lr],
                                               skel.nodes[ur]])

                    # Simple skeleton -- set the homogeneity to "1".
                    if preset_homog:
                        # In the preset case, both elements are on the
                        # same pixel, so only do this once.
                        dom_pixel = microStructure.categoryFromPoint(
                            el1.repr_position())
                        el1.setHomogeneous(dom_pixel)
                        el2.setHomogeneous(dom_pixel)

                    # Element constructors make the segments, we can
                    # use them to make the edges and add them to the
                    # boundaries.

                    #To create default boundaries as interfaces
                    #instead of skeleton boundaries, comment or remove
                    #the following line.
                    self.addGridSegmentsToBoundaries(skel,i,j,m,n)

                    el1.findHomogeneityAndDominantPixel(skel.MS)
                    el2.findHomogeneityAndDominantPixel(skel.MS)

                    if prog.stopped():
                        return None
                    rectangle_count = i*m+j
                    prog.setFraction(float(rectangle_count)/tot_items)
                    prog.setMessage("Created %d/%d elements"
                                    % (2*rectangle_count, 2*tot_items))
            return skel
        finally:
            prog.finish()

Registration(
    'TriSkeleton',
    SkeletonGeometry,
    TriSkeleton,
    1,
    params=[enum.EnumParameter('arrangement', Arrangement, moderate,
                       tip="How to arrange triangular elements in a Skeleton"),
            parameter.BooleanParameter('left_right_periodicity',value=False, default=False,
                  tip="Whether or not the skeleton has periodicity in the horizontal direction"),
            parameter.BooleanParameter('top_bottom_periodicity',value=False, default=False,
                  tip="Whether or not the skeleton has periodicity in the vertical direction")],
    tip='A Skeleton of triangular elements.',
    discussion="""<para>
    <classname>TriSkeleton</classname> is used as the
    <varname>skeleton_geometry</varname> argument of <xref
    linkend='MenuItem-OOF.Skeleton.New'/>, specifying that it is to
    create a &skel; with right triangular &elems;.  The
    <varname>arrangement</varname> describes how the hypotenuses of
    the triangles are to be arranged.
    </para>""" )

######################

# SkeletonBase is provided just so different kinds of skeletons
# (Skeleton, DeputySkeleton) can be checked for in a single
# isinstance() call.

class SkeletonBase:
    def __init__(self):
        self._illegal = 0
        # Appears in the Skeleton Page
        self.homogeneityIndex = None
        self.illegalCount = None
        
        # Keep track of when the skeleton geometry last changed, and
        # when the homogeneity index was last updated.  Geometry
        # changes happen when new elements are added to the skeleton,
        # or when they are detected in the
        # findHomogeneityandDominantPixel routine of member skeleton
        # elements.
        self.homogeneity_index_computation_time = timestamp.TimeStamp()
        self.homogeneity_index_computation_time.backdate()
        self.most_recent_geometry_change = timestamp.TimeStamp()
        self.illegal_count_computation_time = timestamp.TimeStamp()
        self.illegal_count_computation_time.backdate()

    def destroy(self):
        pass

    def updateGeometry(self):
        self.most_recent_geometry_change.increment()
        
    def setHomogeneityIndex(self):
        # Tempting though it may be, do not lock the MS here.  This
        # can be called with the skeleton already locked, which
        # implicitly locks the MS.
        homogIndex = 0.0
        illegalcount = 0
        for e in self.elements:
            if not e.illegal():
                homogIndex += e.area()*e.homogeneity(self.MS)
            else:
                illegalcount += 1
                
        homogIndex /= self.area()

        self.illegalCount = illegalcount
        self.homogeneityIndex = homogIndex
        self.homogeneity_index_computation_time.increment()
        self.illegal_count_computation_time.increment()

    def getIllegalCount(self):
        if self.illegalCount is None or (self.illegal_count_computation_time
                                         < self.most_recent_geometry_change):
            illegalCount = 0
            for e in self.elements:
                if e.illegal():
                    illegalCount += 1
            self.illegalCount = illegalCount
            self.illegal_count_computation_time.increment()
        return self.illegalCount

    def getIllegalElements(self):
        return [e for e in self.elements if e.illegal()]
    
    def getHomogeneityIndex(self):
        if (self.homogeneity_index_computation_time < self.MS.getTimeStamp()
            or self.homogeneity_index_computation_time <
            self.most_recent_geometry_change):
            self.setHomogeneityIndex()
        return self.homogeneityIndex

    # Utility function, finds all the intersections of passed-in
    # segment (a primitives.Segment object) with the passed-in
    # skeleton element.  Needs the skeleton object in order to extract
    # skeleton segments. Actually returns a dictionary, indexed by
    # points, whose values are lists of the intersecting segments, as
    # a tuple, (intersection-point, next-element)
    def _get_intersections_with_element(self, local_seg, skel_el):
        skel_segs = skel_el.getSegments(self)
        isec_set = {}
        for s in skel_segs:
            nds = s.nodes()
            c1 = nds[0].position()
            c2 = nds[1].position()
            seg = primitives.Segment(c1,c2)
            isec = local_seg.intersection(seg)
            if isec:
                try:
                    isec_set[isec].append(s)
                except KeyError:
                    isec_set[isec]=[s]
        return isec_set


    # Element traversal function -- given a skeleton element, local
    # segment, and entry point, returns either (None, None) if the
    # segment terminates inside the current element, or otherwise, the
    # next element along the segment.
    def get_intersection_and_next_element(self, local_seg, skel_el, entry):

        # First, see if we're already done -- if the current element
        # encloses the trailing point of the local segment, there is
        # no next element.
        if skel_el.interior(local_seg.end()):
            return (None, None)
        
        # Find all the intersections with this element.
        isec_set = self._get_intersections_with_element(local_seg, skel_el)

        # Remove the intersection we already know about -- it's not an
        # allowed "exit" intersection.

        ## TODO MER: The keys in the isec_set dictionary need to be
        ## tuples containing both the intersection point and the
        ## element from which the traversal is arriving.  This
        ## function needs to know that previous element as well.  If
        ## the current element is degenerate, the entry point and exit
        ## point might be identical, so using the entry point alone as
        ## a key is insufficient.  This may have been fixed already.
        if entry:
            del isec_set[entry]

        # If there is no exit intersection, but the interiority check
        # on the end-point failed (i.e. it gave the result "exterior"
        # for the end-point of local_seg), then the end-point must be
        # within round-off of the boundary of the element.  In this
        # case, there is again no next element.
        if len(isec_set)==0:
            return (None, None)


        # Now the intersection set must be of length one, consisting
        # of the "exit wound".  If it's not 1 (and not zero, above)
        # then something has gone horribly wrong.  Throw an exception.

        ## TODO MER: The horribly wrong situation must be that the element
        ## is an illegal chevron shaped quad.  We could handle such
        ## quads if they were split into two triangles (at least one
        ## of which would be illegal, but the algorithm works on
        ## illegal triangles).
        if len(isec_set) !=1:
            raise ooferror.ErrPyProgrammingError(
                "Segment exits element multiple times.")
            
        isec_point = isec_set.keys()[0]
        isec_segs = isec_set.values()[0]

        # Now get the *segments* corresponding to the exit point.
        # If there's one, then this is the generic case.
        if len(isec_segs)==1:
            next_el = isec_segs[0].getOtherElement(skel_el)
            
        # If there are two segments, then we exit through a corner.
        elif len(isec_segs)==2:
            # Find the node common to the two segments.
            nds1 = isec_segs[0].nodes()
            nds2 = isec_segs[1].nodes()
            for n in nds1:
                if n in nds2:
                    common_node = n
                    break
            # Find all the elements connected to this corner which
            # have new intersections.
            corner_elements = common_node.aperiodicNeighborElements()
            new_elements = []
            for e in [x for x in corner_elements if x!=skel_el]:
                new_isecs = self._get_intersections_with_element(
                    local_seg, e)
                try:
                    # Remove the one we already know about.
                    del new_isecs[isec_point]
                except KeyError:
                    pass

                # Also remove any new intersections which precede
                # isec_point along the local segment.  These can sneak
                # in in the case where the local segment intersects
                # two segments in the current element, but only one in
                # the previous element -- in that case, the current
                # element will find an exit intersection in the prior
                # element, and incorrectly select it as next, leading
                # to an infinite loop.
                kill_list = []
                mp = (isec_point-local_seg.start())**2
                for k in new_isecs:
                    mk = (k-local_seg.start())**2
                    if mk < mp:
                        kill_list.append(k)
                for k in kill_list:
                    del new_isecs[k]

                # For elements where valid intersections occur,
                # add them to the list of candidates.
                if len(new_isecs)>0:
                    new_elements.append(e)

            # If we found zero elements, then the cross-section must
            # terminate inside one of these.  Figure out which one
            # by testing interiority.
            if len(new_elements)==0:
                for e in [x for x in corner_elements if x!=skel_el]:
                    if e.interior(local_seg.end()):
                        next_el = e
                        break
                else:
                    raise ooferror.ErrPyProgrammingError("get_intersection_and_next_element failed, case 0")
                    
            # If we found exactly one element, then just return it.
            elif len(new_elements)==1:
                next_el = new_elements[0]
            else:
                # If there's more than one, then the local segment
                # must pass directly between two elements along their
                # shared skeleton segment.  Pick the one on the right,
                # which is the one whose center has a positive cross
                # product with the segment itself, viewed from the
                # start of the segment.
                for e in new_elements:
                    v1 = e.center()-local_seg.start()
                    v2 = local_seg.end()-local_seg.start()
                    if v1.cross(v2)>0:
                        next_el = e
                        break
                else:
                    raise ooferror.ErrPyProgrammingError("get_intersection_and_next_element failed, case n")
        else:
            # Impossible!
            raise ooferror.ErrPyProgrammingError(
                "Linear path crosses an element more than twice, or fewer than zero times.")

        return (isec_point, next_el)
            

    def enclosingElement(self, point):
        # Find the element containing the given point.
        # Start at the last element found (if any).  Draw a line
        # between the center of the element and the target point.
        # Find which side of the element intersects the line, and move
        # to the neighboring element across that side.  Repeat.  If no
        # side crosses the line, the current element is the one we're
        # looking for.

        # The algorithm relies on starting inside an element, any
        # element.  We use the last element found because it's likely
        # to be near the element that the user is interested in.
        # However, if the last element is illegal, its inside may not
        # be well defined.  Since we use the element's center to find
        # an interior point, and the center of an illegal element may
        # be outside of the element, we don't start at illegal
        # elements.
        
        # _found_element is either None or a weak reference to the
        # last el found
        el = self._found_element and self._found_element()

        # If the (clicked) point is outside of the skeleton,
        # this scheme doesn't work. So, here's a reasonable fix to that.
        if point.x < 0.0:
            point[0] = 0.0
        if point.x > self.MS.size()[0]:
            point[0] = self.MS.size()[0]
        if point.y < 0.0:
            point[1] = 0.0
        if point.y > self.MS.size()[1]:
            point[1] = self.MS.size()[1]

        # If we don't have a good starting point, we look for one.
        if el is None or el.illegal():
            for ell in self.elements:
                if not ell.illegal():
                    el = ell
                    break
            else:               
                raise ooferror.ErrSetupError("All elements are illegal!")
                         
            
        center = el.center()
        straw = primitives.Segment(center, point)

        entry = None
        while(el):
            last_el = el
            (entry, el) = self.get_intersection_and_next_element(
                straw, last_el, entry)
            
        self._found_element = weakref.ref(last_el)
        return last_el

        

    def nearestSgmt(self, point):
        # Local function to compute the distance between a point pt
        # and segment.  The return value is a tuple whose first entry
        # is the distance squared from the point to the closest point
        # on the segment.  If the projection of the point onto the
        # line of the segment is *not* on the segment, the second
        # member of the tuple is the distance squared along the line
        # from the projected point to the closest endpoint of the
        # segment.  Simply comparing tuples then gives the closest
        # segment to the given point.
        def distance(pt, segment):
            nodes = segment.nodes()
            p0 = nodes[0].position()
            p1 = nodes[1].position()
            a = pt-p0
            b = p1-p0
            seglength2 = b**2
            if seglength2 == 0:
                return (a**2, 0.0)
            f = ((a*b)/seglength2) #  projection's fractional distance from p0
            if f < 0:
                alpha = -f
                r = pt - p0
            elif f > 1:
                alpha = f-1
                r = pt - p1
            else:
                r = a-f*b
                alpha = 0
            return (r**2, alpha*alpha*seglength2)

        # First, see if the point is inside an element.  If it is, the
        # closest segment must be one of the element's edges.
        element = self.enclosingElement(point)
        if element is not None:
            mindist = None
            nearseg = None
            for i in range(element.nnodes()):
                node0 = element.nodes[i]
                node1 = element.nodes[(i+1)%element.nnodes()]
                seg = self.getSegment(node0, node1)
                d = distance(point, seg)
                if mindist is None or d < mindist:
                    mindist = d
                    nearseg = seg
        else:
            # Not inside any element.  Search all boundary segments.
            mindist = None
            nearseg = None
            for seg in self.segments.values():
                if seg.nElements() == 1: # it's a boundary segment
                    d = distance(point, seg)
                    if mindist is None or d < mindist:
                        mindist = d
                        nearseg = seg
        return nearseg

    ## Call setIllegal() after creating an illegal element.
    def setIllegal(self):
        self._illegal = 1
    def illegal(self):
        return self._illegal

    ## Call checkIllegality after any operation that may have changed
    ## an illegal skeleton into a legal one.  Operations that change
    ## legal skeletons into illegal ones should be able to check
    ## legality themselves (without searching all elements) and should
    ## call setIllegal() directly.
    def checkIllegality(self):
        for el in self.elements:
            if el.illegal():
                self._illegal = 1
                return
        self._illegal = 0

    def countShapes(self):
        shapecounts = {}
        for name in skeletonelement.ElementShapeType.names:
            shapecounts[name] = 0
        for e in self.elements:
            shapecounts[e.type().name] += 1
        return shapecounts

#####################

# The Skeleton contains the geometrical information for a mesh,
# without any of the complications of nodes, shapefunctions, or
# materials.

# Skeleton objects live in a SkeletonContext stack, and many of their
# operations are invoked via the Context, which does important
# bookkeeppiinngg.

class Skeleton(SkeletonBase):
    def __init__(self, microStructure, left_right_periodicity=False,
                 top_bottom_periodicity=False):
        SkeletonBase.__init__(self)
        self.MS = microStructure        # Microstructure object, not context
        self._size = self.MS.size()
        self._area = self._size[0]*self._size[1]
        self.nodemovehistory = skeletondiff.NodeMoveHistory()
        self.elements = utils.ReservableList()
        self._found_element = None      # used in enclosingElement().
        self.nodes = utils.ReservableList()
        self.segments = {}              # Nondirected edges.
        self.edgeboundaries = {}
        self.pointboundaries = {}
        self.timestamp = timestamp.TimeStamp()
        self.left_right_periodicity = left_right_periodicity
        self.top_bottom_periodicity = top_bottom_periodicity
        
        # When elements and nodes are deleted from the mesh, they
        # aren't immediately removed from the lists in the Skeleton.
        # They're only removed when cleanUp() is called.  washMe
        # indicates whether or not cleanUp() is necessary.
        self.washMe = 0
        
        self.hashedNodes = None

        self.deputy = None              # currently active DeputySkeleton
        self.deputylist = []            # all deputies
        self._deferreddestruction = 0
        self._destroyed = 0

        self.setIndexBase() # Default is to start from zero.
        
        # Decided not to meddle with the exisiting indexing and also not to
        # introduce a new indexing.
        # Instead, dictionaries -- ex) node.index: index in self.nodes
        # With this a node can be fetched with "index" efficiently,
        # which is crucial in parallel mode.
        # ex) def getNodeWithIndex(index):
        #         return self.nodes[node_index_dict[index]]
        # The first values for these dictionaries always starts from 0,
        # which is not a surprise.
        # It could be useful in serial mode too, but at this point
        # these are only maintained in parallel mode.
        self.node_index_count = 0
        self.elem_index_count = 0
        self.node_index_dict = {}
        self.elem_index_dict = {}

        self.cachedHomogeneities = {}

        # geometric info of all Skeletons (in parallel mode)
        if parallel_enable.enabled():
            self.all_skeletons = None
        
    # Current index data for each of the three types of skeleton
    # objects are stored here -- these get incremented when new
    # objects of the indicated type are created in this skeleton.
    # These indices should start at zero, and proceed contiguously
    # within a skeleton context.
    def setIndexBase(self, node_index_base=0,
                     segment_index_base=0,
                     element_index_base=0):
        self.node_index = node_index_base
        self.segment_index = segment_index_base
        self.element_index = element_index_base

        # Used in parallel mode -- these will not be changed
        if parallel_enable.enabled():
            self.node_index0 = node_index_base
            self.segment_index0 = segment_index_base
            self.element_index0 = element_index_base

    def reserveElements(self, n):
#         self.elements.reserve(n)
        pass

    def reserveNodes(self, n):
        self.nodes.reserve(n)

    def isDeputy(self):
        return 0

    def clearCachedHomogeneities(self):
        self.cachedHomogeneities = {}
        
    def destroy(self, skelcontext):
        SkeletonBase.destroy(self)
        ## NOTE: destroy() may be called more than once, if the
        ## Skeleton has deputies.  If the Skeleton has deputies when
        ## it is destroyed, the _deferreddestruction flag is set, and
        ## destroy() will be called again when the last deputy is
        ## destroyed.  That means that destroy() can't leave lists of
        ## destroyed objects lying around -- it must actually replace
        ## the lists with empty lists.

        self._destroyed = True  # see NOTE above

 #        for el in self.elements:
 #            el.destroy(self)
 #        self.elements = []
 #        self.nodes = []
 #        self.hashedNodes = None
        
        # Any data shared with deputies must not be deleted until the
        # deputies are done with it.
        if self.ndeputies() == 0:

            for el in self.elements:
                el.destroy(self)
            self.elements = []
            self.nodes = []
            self.hashedNodes = None
            
            for ebdy in skelcontext.edgeboundaries.values():
                ebdy.remove(self)
            for pbdy in skelcontext.pointboundaries.values():
                pbdy.remove(self)
            del self.MS
            self.disconnect()
        else:
            self._deferreddestruction = 1
            
    def destroyed(self):
        return self._destroyed

    def __repr__(self):
        return 'Skeleton(%d)' % id(self)
    
    def disconnect(self):
        for s in self.nodes + self.segments.values() + self.elements:
            s.disconnect()

    def getTimeStamp(self):
        return self.timestamp
##         return max(self.timestamp, self.MS.getTimeStamp())

    def hashNodes(self):
        # Computing preliminary information
        nnodes = self.nnodes()  # no. of nodes
        x_size = self.size()[0]
        y_size = self.size()[1]
        ratio = x_size/y_size  # aspect ratio of skeleton
        if ratio < 1.0:
            ratio = 1.0/ratio
        nndtile = int( 0.5*math.sqrt(nnodes)*ratio )  # no. of nodes per tile
        ntiles = int( nnodes/nndtile )  # no. of tiles

        if x_size >= y_size:
            nx = int( math.sqrt(ratio*ntiles) )  # tiles in the x-direction
            ny = int( (1.0*nx)/ratio )           # tiles in the y-direction
        else:
            ny = int( math.sqrt(ratio*ntiles) )
            nx = int( (1.0*ny)/ratio )

        # For large ratios, the int can yield zero.  Fix these.
        if nx==0: nx=1
        if ny==0: ny=1
        
        self.hashedNodes = skeletonnode.HashedNodes((nx,ny), self.size())

        self.hashedNodes.hash(self)

    def needsHash(self):
        self.hashedNodes = None

    def nnodes(self):
        self.cleanUp()
        return len(self.nodes)
                                   
    def nelements(self):                # for compatiblity w/ Element output
        self.cleanUp()
        return len(self.elements)

    def element_iterator(self):         # for compatiblity w/ Element output
        self.cleanUp()
        return self.elements

    def node_iterator(self):
        self.cleanUp()
        return self.nodes

    def segment_iterator(self):
        self.cleanUp()
        return self.segments.values()

    # This returns the position in the skeleton's node list
    # which is not the same as node.getIndex()
    # Is this used?
##     def getNodeIndex(self, node):
##         return self.nodes.index(node)

    def notPinnedNodes(self):
        return [n for n in self.node_iterator() if not n.pinned()]

    def getElementIndex(self, elem):
        return self.elements.index(elem)

    def nillegal(self):
        n = 0
        for e in self.elements:
            if e.illegal():
                n += 1
        return n

    # Returns a tuple containing maximum x-extent and maximum y-extent
    # of the skeleton. 
    def size(self):
        return self._size

    def area(self):
        return self._area
        
    def newNodeFromPoint(self, point):
        return self.newNode(point.x, point.y)

    def newNode(self, x, y):
        if (self.left_right_periodicity and (x == 0.0 or x == self.size()[0])) \
           or (self.top_bottom_periodicity and
               (y == 0.0 or y == self.size()[1])):
            c = PeriodicSkeletonNode(x,y, index=self.node_index)
        else:
            c = SkeletonNode(x,y, index=self.node_index)
        self.node_index += 1
        if x == 0.0 or x == self.size()[0]:
            c.setMobilityX(0)
        if y == 0.0 or y == self.size()[1]:
            c.setMobilityY(0)
        self.nodes.append(c)
        
        if parallel_enable.enabled():
            self.node_index_dict[c.index] = self.node_index_count
            self.node_index_count += 1
                
        return c

    # Only elements with nonzero area are constructed here.  The
    # line-elements are expected to be done in the boundary code.
    def newElement(self, nodes, parents=[]):
        nnodes = len(nodes)
        if nnodes==3:
            el = SkeletonTriangle(nodes, self.element_index)
            self.element_index += 1
        elif nnodes==4:
            el = SkeletonQuad(nodes, self.element_index)
            self.element_index += 1
        else:
            raise ooferror.ErrPyProgrammingError(
                "Unable to construct %d-noded element." % nnodes)
        self.elements.append(el)
        for parent in parents:
            el.add_parent(parent)
            parent.add_child(el)
            
        # Add this element's edges to the dictionary of segments.
        # fetchSegment returns an existing SkeletonSegment, or makes one
        # if necessary.
        lastnode = nodes[-1]
        for node in nodes:
            segment = self.fetchSegment(lastnode, node)
            segment.addElement(el)
            lastnode = node

        self.updateGeometry()

        if parallel_enable.enabled():
            self.elem_index_dict[el.index] = self.elem_index_count
            self.elem_index_count += 1
            
        return el

    def loadElement(self, *indices):
        nodes = [self.nodes[index] for index in indices]
        return self.newElement(nodes)

    def loadEdge(self, node0, node1):
        seg = self.getSegment(node0, node1)
        edge = skeletonsegment.SkeletonEdge(seg)
        if seg.nodes()[0] == node0:
            edge.direction = 1
        else:
            edge.direction = -1
        return edge

    def removeElements(self, *elements):
        self.washMe = 1
        for el in elements:
            el.defunct = 1
            el.destroy(self)

    def removeNode(self, node):
        # Called only by SkeletonNode.destroy() which is called by
        # SkeletonNode.removeElement() when the node's last element is
        # removed.
        self.washMe = 1
        node.defunct = 1
        
        # Need to update  self.node_index_dict in parallel mode
        if parallel_enable.enabled():
            node_index = node.getIndex()
            list_index = self.node_index_dict[node_index]
            # "node_index" will be deleted from the dict and all the nodes
            del self.node_index_dict[node_index]
            affected_nodes = [self.nodes[i].getIndex()
                              for i in range(list_index+1, self.nnodes())]
            for an in affected_nodes:
                self.node_index_dict[an] -= 1
            self.node_index_count -= 1
            
    def cleanUp(self):
        if self.washMe:
            self.elements = filter(lambda e: not hasattr(e, 'defunct'),
                                   self.elements)
            self.nodes = filter(lambda n: not hasattr(n, 'defunct'), self.nodes)
            self.washMe = 0

    def getElement(self, index):
        return self.elements[index]
    
    def getElementWithIndex(self, index):
        return self.elements[ self.elem_index_dict[index] ]

    # This returns a node based on its position in the skeleton's
    # node list.  
    def getNode(self, index):
        return self.nodes[index]

    # # This returns a node based on its unique index number: the inverse
    # # operation of node.getIndex().
    # ## TODO MER: change name of "index" to distinguish between list
    # ## position and unique ID - nodeID for instance...  this indexing
    # ## is only maintained in parallel... so it's commented out.
    # def getNodeWithIndex(self, index):
    #     return self.nodes[ self.node_index_dict[index] ]

    # getSegment returns an existing segment joining the given nodes,
    # or creates a segment if such a segment doesn't already exist.
    def getSegment(self, node0, node1):
        nodes = skeletonnode.canonical_order(node0, node1)
        try:
            return self.segments[nodes]
        except KeyError:
            segment = SkeletonSegment(nodes, self.segment_index)
            self.segment_index += 1
            self.segments[nodes] = segment
            return segment

    # fetchSegment is just like getSegment, but it should be faster in
    # the case where the Segment is likely *not* to be in the
    # dictionary already.  (Is this a significant optimization?)
    def fetchSegment(self, node0, node1):
        nodes = skeletonnode.canonical_order(node0, node1)
        if nodes in self.segments:
            return self.segments[nodes]
        segment = SkeletonSegment(nodes, self.segment_index)
        self.segment_index += 1
        self.segments[nodes] = segment
        return segment

    # findSegment returns an existing segment joining the given nodes,
    # or None if such a segment doesn't exist.
    def findSegment(self, node0, node1):
        try:
            return self.segments[skeletonnode.canonical_order(node0, node1)]
        except KeyError:
            return None

    def removeSegment(self, key):
        # Called only by SkeletonSegment.destroy(), which is called by
        # SkeletonSegment.removeElement when the segment's last
        # element is removed.
        del self.segments[key]

    # Geometry comparison function -- returns 0 if this skeleton has
    # the same size, area, elements, segments, and boundaries as the
    # other, and if all the nodes are within tolerance of the
    # positions of the other; otherwise returns a string describing
    # what went wrong.  Note that these objects must not only be
    # topologically equivalent, but must also be indexed the same for
    # the comparison to succeed.  Does not care about the skeleton
    # name, or about microstructure stuff like pixels, or about group
    # membership or selection status.  The former is properly the
    # responsibility of the microstructure, and the latter the
    # responsibility of the skeleton context.
    def compare(self, other, tolerance):
        if self._size != other._size:
            return "Size mismatch"
        if self._area != other._area:
            return "Area mismatch"

        if len(self.elements)!=len(other.elements):
            return "Element count mismatch"
        if len(self.segments)!=len(other.segments):
            return "Segment count mismatch"
        if len(self.nodes)!=len(other.nodes):
            return "Node count mismatch"

        # Make sure elements have the same node indices.  The elements
        # might not be in the same order in the two Skeletons, so we
        # can't just compare the node indices in the elements one by
        # one.  Instead, compare *sorted* lists of lists of node
        # indices, one (inner) list for each element.
        enodes = [ [n.index for n in e.nodes] for e in self.elements]
        onodes = [ [n.index for n in e.nodes] for e in other.elements]
        enodes.sort()
        onodes.sort()
        if enodes != onodes:
            return "Element node indexing mismatch"

        # Make sure segments have the same node indices.  Segments are
        # stored in a dictionary keyed by node pairs, so there's no
        # need to worry about segment order.
        for (s1,s2) in zip(self.segments.values(), other.segments.values()):
            if [x.index for x in s1.nodes()]!=[x.index for x in s2.nodes()]:
                return "Segment node indexing mismatch"

        # Basic topology is right, now quantitatively check node locations.
        tol2 = tolerance**2
        for (n1,n2) in zip(self.nodes, other.nodes):
            if (n1.position()-n2.position())**2 > tol2:
                return "Node outside of tolerance, %s-%s=%s" % \
                       (`n1.position()`, `n2.position()`,
                       `n1.position()-n2.position()`)

        if len(self.edgeboundaries)!=len(other.edgeboundaries):
            return "Edge boundary count mismatch"
        if len(self.pointboundaries)!=len(other.pointboundaries):
            return "Point boundary count mismatch"

        # The boundary tests do *not* assume that the boundaries are
        # in the same order in the two skeletons.
        for key, b1 in self.edgeboundaries.items():
            try:
                b2 = other.edgeboundaries[key]
            except KeyError:
                return "Edge boundary name mismatch: %s" % key
                
            if b1.size()!=b2.size():
                return "Edge boundary size mismatch: %s" % key
            for (e1,e2) in zip(b1.edges, b2.edges):
                if [x.index for x in e1.get_nodes()] != \
                       [x.index for x in e2.get_nodes()]:
                    return "Edge boundary node mismatch: %s" % key

        for key, b1 in self.pointboundaries.items():
            try:
                b2 = other.pointboundaries[key]
            except KeyError:
                return "Point boundary name mismatch: %s" % key
            if b1.size()!=b2.size():
                return "Point boundary size mismatch: %s" % key
            for (n1,n2) in zip(b1.nodes, b2.nodes):
                if n1.index != n2.index:
                    return "Point boundary node index mismatch: %s" % key

        return 0 # Success! 

    def properCopy(self, skeletonpath=None, fresh=False):
        # Copy the current skeleton properly so that the new skeleton
        # and the current skeleton are totally independent.  If
        # "fresh" is True, then node, segment, and element indices
        # start at zero.  Otherwise, index-base data is retrieved from
        # the skeleton context.  "fresh" will be true during adaptive
        # mesh refinement.

        # The only time skeletonpath is used is when fresh==False, and
        # only to be able to call setIndexBase. If fresh==True, there
        # is no need to supply skeletonpath.
        
        self.cleanUp()
        # create a new skeleton
        newSkeleton=Skeleton(self.MS)
        if not fresh:
            context = skeletoncontext.skeletonContexts[skeletonpath]
            newSkeleton.setIndexBase(*context.next_indices)

        # Make new nodes which have different indices, but are children
        # of the old nodes.
        #newSkeleton.nodes = []
        for n in self.nodes:
            newSkeleton.nodes.append(n.copy_child(newSkeleton.node_index))
            newSkeleton.node_index += 1

        newSkeleton.left_right_periodicity = self.left_right_periodicity
        newSkeleton.top_bottom_periodicity = self.top_bottom_periodicity

        # rebuild the node partnerships - must be done in separate loop
        # after all nodes are created
        for n in self.nodes:
            for p in n.getPartners():
                n.getChildren()[-1].addPartner(p.getChildren()[-1])

        #Copy the following information also:
        #SkeletonNode _shared_with = []  # except me
        #             _remote_index = {}  # procID : remote index
        if parallel_enable.enabled():
            for n1,n2 in zip(self.nodes,newSkeleton.nodes):
                n2._shared_with=n1._shared_with[:]
                n2._remote_index=n1._remote_index.copy()

        # newSkeleton.nodes = [ n.copy_child() for n in self.nodes ] 

        newSkeleton.elements = []
        for e in self.elements:
            newSkeleton.elements.append(
                e.copy_child(newSkeleton.element_index))
            newSkeleton.element_index += 1
            
        # newSkeleton.elements = [ e.copy_child() for e in self.elements ]

        # Make new segments which have equivalent indices (with new
        # nodes), but are children of the old segments.
        for s in self.segments.values():
            new_seg = s.copy_child(newSkeleton.segment_index)
            newSkeleton.segment_index += 1
            newSkeleton.segments[new_seg.nodes()] = new_seg

        newSkeleton._illegal = self._illegal
        return newSkeleton
            

    def improperCopy(self, skeletonpath=None, fresh=False):
        # Copy a Skeleton, but *not* the elements or segments.  Just
        # nodes.  Used when refining, where the elements and segments
        # are recreated by Refine.apply().

        # If "fresh" is True, then node, segment, and element indices
        # start at zero.  Otherwise, index-base data is retrieved from
        # the skeleton context.  The only time skeletonpath is used is
        # when fresh==False, and only to be able to call
        # setIndexBase. If fresh==True, there is no need to supply
        # skeletonpath.
        self.cleanUp()
        newSkeleton = Skeleton(self.MS)
        if not fresh:
            context = skeletoncontext.skeletonContexts[skeletonpath]
            newSkeleton.setIndexBase(*context.next_indices)
            
        for n in self.nodes:
            newSkeleton.nodes.append(n.copy_child(newSkeleton.node_index))
            newSkeleton.node_index += 1

        newSkeleton.left_right_periodicity = self.left_right_periodicity
        newSkeleton.top_bottom_periodicity = self.top_bottom_periodicity

        # rebuild the node partnerships - must be done in separate loop
        # after all nodes are created
        for n in self.nodes:
            for p in n.getPartners():
                n.getChildren()[-1].addPartner(p.getChildren()[-1])

        newSkeleton._illegal = self._illegal

        # In parallel mode, node keeps a dict of remote indices,
        # {rank: remote_index, ...}. This dict has been copied over but
        # it's useless -- the copied skeleton has new indices for nodes.
        if parallel_enable.enabled():
            from ooflib.SWIG.common import mpitools
            offsets = mpitools.Allgather_Int(newSkeleton.node_index0 - \
                                             self.node_index0)
            for on, nn in zip(self.nodes, newSkeleton.nodes):
                newSkeleton.node_index_dict[nn.index] = \
                    newSkeleton.node_index_count
                newSkeleton.node_index_count += 1
                if on.isShared():
                    for rank, index in on._remote_index.items():
                        nn.sharesWith(rank, index + offsets[rank])
        
        return newSkeleton

    ###################

    # The following routines are redefined in the DeputySkeleton
    # class.  A DeputySkeleton is a skeleton that differs from another
    # skeleton only in the position of its nodes.  See
    # engine/deputy.py. 

    def getIndexBase(self):
        return (self.node_index, self.segment_index, self.element_index)

    def deputyCopy(self):
        from ooflib.engine import deputy  # delayed import to avoid loops
        # A "copy" that doesn't actually make a copy, but just keeps
        # track of which nodes have been moved.
        return deputy.DeputySkeleton(self)

    def sheriffSkeleton(self):          # The sheriff isn't the deputy
        return self

    def deputize(self, deputy):         # install a new deputy
        if self.deputy:
            self.deputy.deactivate()
        self.deputy = deputy

    def addDeputy(self, dep):
        # Called by DeputySkeleton.__init__()
        self.deputylist.append(dep)

    def removeDeputy(self, dep, skelcontext):
        # Called by DeputySkeleton.destroy()
        self.deputylist.remove(dep)
        if self._deferreddestruction and self.ndeputies() == 0:
            self.destroy(skelcontext)

    def ndeputies(self):
        return len(self.deputylist)

    def activate(self):
        if self.deputy:
            self.deputy.deactivate()
            self.deputy = None

    def moveNodeTo(self, node, position):
        node.moveTo(position)
        for partner in node.getPartners():
            partner.moveTo(position)

    def moveNodeBy(self, node, delta):
        node.moveBy(delta)
        for partner in node.getPartners():
            partner.moveBy(delta)

    def moveNodeBack(self, node):
        node.moveBack()
        for partner in node.getPartners():
            partner.moveBack()

    def getMovedNodes(self):
        return {}

    def nodePosition(self, node):
        # Gets the position of the node in this skeleton even if a
        # deputy is active.
        if self.deputy:
            return self.deputy.originalPosition(node)
        return node.position()
            
    def newSelectionTracker(self, selectionset):
        return skeletonselectable.SelectionTracker()

    def newGroupTracker(self, groupset):
        return skeletongroups.GroupTracker()

    def newPinnedNodeTracker(self):
        return skeletonnode.PinnedNodeTracker(self)

    def promoteTrackers(self, context):
        pass

    #######################
    def weightedEnergyTotal(self, alpha):
        self.cleanUp()
        return reduce(lambda x,y: x+y,
                      [el.area()*el.energyTotal(self, alpha)
                       for el in self.elements])

    def energyTotal(self, alpha):
        self.cleanUp()
        total = 0.
        for el in self.elements:
            total += el.energyTotal(self, alpha)
        return total

    def illegalElements(self):
        return [e for e in self.elements if e.illegal()]

    def activeElements(self):
        self.cleanUp()
        return [e for e in self.elements if e.active(self)]

    def activeNodes(self):
        self.cleanUp()
        return [n for n in self.nodes if n.active(self)]

    def activeSegments(self):
        self.cleanUp()
        return [s for s in self.segments.values() if s.active(self)]
                    
    def nearestNode(self, point):
        if self.hashedNodes is None:
            self.hashNodes()
        return self.hashedNodes.nearestNode(point)

    #################

    def mergeNodePairs(self, *pairs):
        # Create a ProvisionalChanges object for merging the given
        # pairs of nodes in the Skeleton.  The arguments are 2-tuples
        # of SkeletonNodes.  The first node in each pair moves to and
        # merges with the second one.

        # Check the legality of the merges (as far as node mobility
        # goes).
        for pair in pairs:
            if not pair[0].canMergeWith(pair[1]):
                return None

        # Set of nodes that are moving
        movingNodes = set([pair[0] for pair in pairs])
        # List of segments that will vanish
        doomedSegments = [self.findSegment(*pair) for pair in pairs]
        # Set of all pairs -- this is just the 'pair's argument, but
        # will be extended to include periodic partners.
        mergingPairs = set(pairs)

        # Include periodic partners of the merging nodes.
        for pair in pairs:
            partners = pair[0].getPartnerPair(pair[1])
            if partners:
                movingNodes.add(partners[0])
                mergingPairs.add(partners)
                doomedSegments.append(self.findSegment(*partners))

        # Find the topologically changing elements.  These are
        # elements that have a doomed segment as a side.
        topElements = set()
        for seg in doomedSegments:
            topElements.update(seg.getElements())

        # Find the elements that don't change topology, but do change
        # shape.
        isoElements = set(
            [elem for node in movingNodes
             for elem in node.aperiodicNeighborElements()])
        isoElements -= topElements

        # Temporarily move nodes to their final positions to check the
        # legality of the elements whose topology doesn't change.  The
        # legality of the topologically changing elements can't be
        # checked here, because moving a node will make the element
        # illegal.
        for pair in mergingPairs:
            pair[0].moveTo(pair[1].position())
        try:
            for elephant in isoElements:
                if elephant.illegal():
                    return None
        finally:           
            # Make sure to move the nodes back, because the merge may
            # still be rejected.
            for pair in mergingPairs:
                pair[0].moveBack()

        change = ProvisionalMerges(self, *pairs)

        # Replace the non-topologically changing elements with new
        # ones, substituting nodes as necessary.
        for oldelement in isoElements:
            newnodes = oldelement.nodes[:]
            for node0, node1 in mergingPairs:
                try:
                    newnodes[newnodes.index(node0)] = node1
                except ValueError:
                    pass
            change.substituteElement(
                oldelement,
                skeletonelement.getProvisionalElement(newnodes,
                                                      oldelement.getParents()))

        # Replace or eliminate the topologically changing elements.
        for oldelement in topElements:
            change.removeElements(oldelement)
            newnodes = oldelement.nodes[:]
            for node0, node1 in mergingPairs:
                try:
                    newnodes.remove(node0)
                except ValueError:
                    pass
            if len(newnodes) >= 3:
                change.insertElements(
                    skeletonelement.getProvisionalElement(
                        newnodes, parents=oldelement.getParents()))
                                      
        return change

    ########################################################################

    def getPointBoundary(self, name, exterior=None):
        try:
            return self.pointboundaries[name]
        except KeyError:
            if exterior:
                bdy = ExteriorSkeletonPointBoundary(name)
            else:
                bdy = SkeletonPointBoundary(name)
            self.pointboundaries[name] = bdy
            return bdy

    def getEdgeBoundary(self, name, exterior=None):
        try:
            return self.edgeboundaries[name] # existing bdy with this name
        except KeyError:                 # didn't find existing bdy
            if exterior:
                bdy = ExteriorSkeletonEdgeBoundary(name)
            else:
                bdy = SkeletonEdgeBoundary(name)       # create it
            self.edgeboundaries[name] = bdy  # save it
            return bdy

    # The SkeletonContext has already ensured that there is no collision.
    # This routine is called from the SkelContextBoundary object's
    # rename routine.
    def renameBoundary(self, oldname, newname):
        if oldname in self.edgeboundaries:
            self.edgeboundaries[newname]=self.edgeboundaries[oldname]
            del self.edgeboundaries[oldname]
            self.edgeboundaries[newname].rename(newname)
        elif oldname in self.pointboundaries:
            self.pointboundaries[newname]=self.pointboundaries[oldname]
            del self.pointboundaries[oldname]
            self.pointboundaries[newname].rename(newname)

    # Build a new edge boundary from the passed-in list of segments,
    # and return it.  The boundary should "point" from the first
    # segment to the last.  Startnode is required if there is only
    # one segment, and is ignored in the other cases.
    #
    # Caller must provide a topologically trivial list of segments
    # with length greater than zero, so all we have to do here is
    # figure out the directions for the edges.
    def makeEdgeBoundary(self, name, segments=None, startnode=None,
                         exterior=None):
        if (name in self.edgeboundaries) or \
               (name in self.pointboundaries):
            raise ooferror.ErrPyProgrammingError(
                "Boundary '%s' already exists." % name)
        
        bdy = self.getEdgeBoundary(name, exterior) # Guaranteed to be new.
        
        if segments and len(segments)==1:
            if startnode:
                seg = segments[0]
                if startnode==seg.nodes()[0]:
                    bdy.addEdge(SkeletonEdge(seg, 1))
                else: # startnode==seg.nodes()[1]:
                    bdy.addEdge(SkeletonEdge(seg, -1))
            else:
                raise ooferror.ErrPyProgrammingError(
                    "Singleton segment boundaries require a starting node!")

        elif segments: # Length of the segment list is greater than one.
            for i in range(len(segments)-1):
                seg1 = segments[i]
                seg2 = segments[i+1]
                nodes_and_partners = list(seg2.nodes()) + \
                                     seg2.nodes()[0].getPartners() + \
                                     seg2.nodes()[1].getPartners()
                if seg1.nodes()[0] in nodes_and_partners: #seg2.nodes():
                    bdy.addEdge(SkeletonEdge(seg1, -1))
                else: #  seg1.nodes()[1] in nodes_and_partners: #seg2.nodes():
                    bdy.addEdge(SkeletonEdge(seg1, 1))
            # For the final segment, need to check the one previous.
            seg1 = segments[-2]
            seg2 = segments[-1]
            nodes_and_partners = list(seg1.nodes()) + \
                                 seg1.nodes()[0].getPartners() + \
                                 seg1.nodes()[1].getPartners()
            if seg2.nodes()[0] in nodes_and_partners: #seg1.nodes():
                bdy.addEdge(SkeletonEdge(seg2, 1))
            else: #  seg2.nodes()[1] in seg1.nodes():
                bdy.addEdge(SkeletonEdge(seg2, -1))

        return bdy # Return bdy even if it has no segments, for stack
                   # propagation.

    def makeNonsequenceableEdgeBoundary(self, name, segments=None,
                                        directions=None,
                                        exterior=None):
        if (name in self.edgeboundaries) or \
               (name in self.pointboundaries):
            raise ooferror.ErrPyProgrammingError(
                "Boundary '%s' already exists." % name)
        
        bdy = self.getEdgeBoundary(name, exterior) # Guaranteed to be new.
        bdy._sequenceable=0

        if segments is not None:
            for i in range(len(segments)):
                bdy.addEdge(SkeletonEdge(segments[i],directions[i]))
            
        return bdy


    # Build a new point boundary from the passed-in list of nodes,
    # and return it.  
    def makePointBoundary(self, name, nodes=None, exterior=None):
        if (name in self.pointboundaries) or \
               (name in self.edgeboundaries):
            raise ooferror.ErrPyProgrammingError(
                "Boundary '%s' already exists." % name)

        bdy = self.getPointBoundary(name, exterior)

        # Correctly returns an empty boundary if nodes==None.
        if nodes:
            for n in nodes:
                bdy.addNode(n)

        return bdy
    

    def removeBoundary(self, name):
        try:
            del self.pointboundaries[name]
        except KeyError:
            pass
        try:
            del self.edgeboundaries[name]
        except KeyError:
            pass


    # The named boundary has been modified -- change the versions in
    # the mesh to match.  Don't just remove and replace, as this
    # destroys valuable boundary condition info.
    def pushBoundaryToMesh(self, mctxt, name):
        if name in self.pointboundaries:
            b = self.pointboundaries[name]
            mctxt.replacePointBoundary(name, b)
        elif name in self.edgeboundaries:
            b = self.edgeboundaries[name]
            mctxt.replaceEdgeBoundary(name, b)


    def mapBoundary(self, bdy, skeleton, **kwargs):
        # double dispatch wrapper for SkelContextBoundary.map().

        # Copy boundary information from the given skeleton to this
        # skeleton.  The given skeleton might be a deputy, which
        # doesn't have any boundary information, so actually copy from
        # the deputy's sheriff.

        # mapBoundary is a no-op in the DeputySkeleton class, so we
        # don't have to worry about copying boundary data *to* a
        # deputy.  However, if the given source skeleton is a deputy,
        # there's a chance that this skeleton is its sheriff, or
        # shares the same sheriff, in which case we don't actually
        # have to copy anything.
        omar = skeleton.sheriffSkeleton()
        if omar is not self.sheriffSkeleton():
            bdy.map(omar, self, **kwargs)

##    def rmBoundary(self, bdy):
##        # double dispatch wrapper for SkelContextBoundary.remove()
##        bdy.remove(self)

    def find_geometrical_boundaries(self):
        for el in self.elements:
            el.exterior_edges = []

        for seg in self.segment_iterator():
            if seg.nElements() == 1:
                seg.getElements()[0].exterior_edges.append(seg.nodes())

    ##############################

    def quick_sanity_check(self):
        # Just check for illegal elements.  For a more thorough check,
        # see sanity_check(), below.
        sane = True
        area = 0.
        for element in self.elements:
            area += element.area()
            if element.illegal():
                reporter.report("illegal element", element.index,
                                [n.position() for n in element.nodes])
                sane = False
        reporter.report("Total element area is", area)
        reporter.report("Microstructure area is", self.MS.area())
        if sane:
            reporter.report("*** Skeleton quick sanity check passed. ***")
        else:
            reporter.report("*** Skeleton quick sanity check failed. ***")
        return sane

    def sanity_check(self):
        sane = True
        for element in self.elements:
            if element.illegal():
                reporter.report("illegal element", element.index,
                                [n.position() for n in element.nodes])
                sane = False
            for node in element.nodes:
                if node not in self.nodes:
                    reporter.report("element", element.index, "contains a node",
                                    node.index, "not in the skeleton")
                    sane = False
                if element not in node.aperiodicNeighborElements():
                    reporter.report("inconsistent neighborNodes for node",
                                    node.index, " and element", element.index)
                    sane = False
            segs = element.getSegments(self)
            if None in segs:
                reporter.report("Element", element.index,
                                "is missing a segment")
                sane = False
        for node in self.nodes:
            for element in node.aperiodicNeighborElements():
                if element not in self.elements:
                    reporter.report("node", node.index, "contains an element",
                                    element.index, "not in the skeleton")
                    sane = False
            if not node.aperiodicNeighborElements():
                reporter.report("Node", node.index, "at", node.position(),
                                "has no elements!")
                sane = False
            # Check that nodes on periodic boundaries have partners
            x = node.position().x
            y = node.position().y
            xmax = self.MS.size().x
            ymax = self.MS.size().y
            if self.left_right_periodicity and (x == 0.0 or x == xmax):
                p = node.getDirectedPartner('x')
                if not p or ((x == 0.0 and p.position().x != xmax) or
                             (x ==  xmax and p.position().x != 0.0)):
                    reporter.report(node.__class__.__name__, node.index,
                                    "at", node.position(),
                                    "has no periodic partner in x")
                    reporter.report("   partners are at",
                                    [(ptnr.position(), ptnr.index)
                                     for ptnr in node.getPartners()])
                    sane = False
            if self.top_bottom_periodicity and (y == 0.0 or y == ymax):
                p = node.getDirectedPartner('y')
                if not p or ((y == 0.0 and p.position().y != ymax) or
                             (y == ymax and p.position().y != 0.0)):
                    reporter.report(node.__class__.__name__, node.index,
                                    "at", node.position(),
                                    "has no periodic partner in y")
                    reporter.report("   partners are at",
                                    [(ptnr.position(), ptnr.index)
                                     for ptnr in node.getPartners()])
                    reporter.report([ptnr.position()-primitives.Point(x, ymax)
                                     for ptnr in node.getPartners()])
                    sane = False
            # Check self consistency of partner lists
            for partner in node.getPartners():
                if node not in partner.getPartners():
                    reporter.report("Inconsistent partner lists for",
                                    node.__class__.__name__, node.index,
                                    "at", node.position(), "and",
                                    partner.__class__.__name__, partner.index,
                                    "at", partner.position())
            
                    sane = False
        for segment in self.segments.values():
            elements = segment.getElements()
            if len(elements) > 2:
                reporter.report("segment", [n.index for n in segment.nodes()], 
                                "has too many elements:",
                                [el.index for el in elements])
                sane = False
            for element in elements:
                if element not in self.elements:
                    reporter.report("segment",
                                    [n.index for n in segment.nodes()],
                                    "contains an element", element.index, 
                                    "not in the skeleton")
                    sane = False
            for node in segment.nodes():
                if node not in self.nodes:
                    reporter.report("segment",
                                    [n.index for n in segment.nodes()], 
                                    "contains a node", node.index,
                                    "not in the skeleton")
                    sane = False
            
        if sane:
            reporter.report("*** Skeleton Sanity Check passed. ***")
        else:
            reporter.report("*** Skeleton sanity check failed. ***")
        return sane

                
# ## ### #### ##### ###### ####### ######## ####### ###### ##### #### ### ## #

## Create a real mesh from a Skeleton, using the given element types.

    #Break-up elements along interface boundaries as the mesh elements
    #get created.
    def femesh(self, edict, set_materials, skelpath, split_interface=True):
        skelctxt = skeletoncontext.skeletonContexts[skelpath]

        # edict[n] is the n-sided master element.  Find the
        # interpolation order of the elements.  They all have the same
        # order, so just pick one.
        order = edict.values()[0].fun_order()

        # set_materials is a function that will be called to assign
        # materials to elements.
        prog = progress.getProgress("New Mesh", progress.DEFINITE)
        prog.setMessage("Preparing...")
        self.cleanUp()

        # Find which elements and edges are on the geometrical
        # boundaries of the system.
        self.find_geometrical_boundaries()

        # The interfaces included here include both interfaces
        # "induced" in the skeleton by microstructure interfaces
        # (e.g. between materials, around pixel groups, etc.) *and*
        # those corresponding to skeleton boundaries, which need not
        # have any microstructural counterpart.  The resulting
        # interface_seg_dict has as keys all of those segments, and as
        # values, SegmentData objects.  If a segment occurs in more
        # than one interface, it still only appears once in this dict,
        # with a segmentData object with all the interfaces included.
        interface_seg_dict = self.createInterfaceSegmentDict(skelpath)

        fe_splitnode={} #{key=skeleton node:
                        #value=list of mesh nodes, one for each zone
                        #around the skeleton node}
                        #If the skeleton node is not part of an interface,
                        #then fe_node should be used instead.


        # Local dictionary of finite-element nodes, indexed by
        # SkeletonNode objects.
        fe_node = {}
        

        realmesh = femesh.FEMesh(self.MS, order)
        realmesh.skeleton = self

        # Reserve space in FEMesh::funcnodes and FEMesh::mapnodes so
        # that the vectors aren't continually reallocated.
        nels = {}                       # number of elements of each type
        for n in edict:
            nels[n] = 0
        for el in self.elements:
            nels[el.nnodes()] += 1

        #TODO OPT: Do a smarter reserve when edgements are involved?
        nfuncnodes = self.nnodes() + len(self.segments)*(order-1)
        for n, masterelem in edict.items():
            nfuncnodes += nels[n]*masterelem.ninteriorfuncnodes()
        realmesh.reserveFuncNodes(nfuncnodes)

        masterel = edict[edict.keys()[0]]
        n_map_per_side = masterel.nexteriormapnodes_only()/masterel.nsides()
        nmapnodes = len(self.segments)*n_map_per_side
        for n, masterelem in edict.items():
            nmapnodes += nels[n]*masterelem.ninteriormapnodes_only()
        realmesh.reserveMapNodes(nmapnodes)

        # Make the real nodes at the corners of the elements.  These
        # nodes are always both mapping and function nodes.
        mnodecount = self.nnodes()
        for i in xrange(mnodecount):
            cur = self.nodes[i]
            if split_interface:
                splitcount=self.countInterfaceZonesAtNode(cur,
                                                          interface_seg_dict)
                if splitcount>0:
                    fe_splitnode[cur]=[None]*splitcount
                    for j in range(splitcount):
                        realnode = realmesh.newFuncNode(
                            coord.Coord(cur.position().x, cur.position().y))
                        fe_splitnode[cur][j]=realnode
                else:
                    #Do the usual
                    realnode = realmesh.newFuncNode(
                        coord.Coord(cur.position().x, cur.position().y)) 
                    fe_node[cur] = realnode
            else:
                realnode = realmesh.newFuncNode(
                    coord.Coord(cur.position().x, cur.position().y)) 
                fe_node[cur] = realnode

            if prog.stopped():
                prog.setMessage("Interrupted")
                return
            else:
                prog.setFraction(1.0*(i+1)/mnodecount)
                prog.setMessage("Allocated %d/%d nodes"%(i+1, mnodecount))

        # Loop over elements.
        numelements = self.nelements()
        realmesh.reserveElements(numelements)
        for mesh_idx in xrange(numelements):
            el = self.elements[mesh_idx]
            local_fe_node={}
            if split_interface:
                for nd in el.nodes:
                    zonenumber=self.getInterfaceZoneNumberAtElem(
                        nd, el, interface_seg_dict)
                    if zonenumber==-1:
                        local_fe_node[nd]=fe_node[nd]
                    else:
                        local_fe_node[nd]=fe_splitnode[nd][zonenumber]
            else:               # not splitting nodes at interfaces
                for nd in el.nodes:
                    local_fe_node[nd]=fe_node[nd]
            # Index correspondence happens here -- the skeleton
            # elements are assigned indices in the order that their
            # corresponding real elements are created/assigned.
            # (SkeletonElement.realelement sets self.meshindex when it
            # creates the real element.)
            mnodecount += el.realelement(skelctxt, realmesh, mesh_idx,
                                         local_fe_node, interface_seg_dict,
                                         edict, set_materials)
            if prog.stopped():
                prog.setMessage("Interrupted")
                return
            prog.setFraction(1.0*(mesh_idx+1)/numelements)
            prog.setMessage("Allocated %d/%d elements"
                            % (mesh_idx+1, numelements))

        # Then do boundaries.
        # Note that edgeboundaries and pointboundaries are in separate lists
        # in the skeleton, but in a single list in the real mesh.

        # Point boundaries first.
        dict_size = len(self.pointboundaries)
        dict_index = 0
        for bdkey, pointbndy in self.pointboundaries.items():
            realbndy = realmesh.newPointBoundary(bdkey)
            for node in pointbndy.nodes:
                #Interface branch
##                try:
##                    realbndy.addNode(fe_node[node]) # Preserve order of nodes.
##                except KeyError:
##                    #Add in all the mesh nodes associated with this skeleton node.
##                    #Would this work with profiles?
##                    for realnode in fe_splitnode[node]:
##                        realbndy.addNode(realnode)
                #Do the following to be consistent with mesh.py's newPointBoundary
                skelel = node.neighborElements()[0]
                realel = realmesh.getElement(skelel.meshindex)
                realbndy.addNode(realel.getCornerNode(skelel.getNodeIndexIntoList(node)))

                if prog.stopped():
                    prog.setMessage("Interrupted")
                    return
                else:
                    prog.setFraction(1.0*(dict_index+1)/dict_size)
                    prog.setMessage("Allocating point boundaries: %d/%d" 
                                    % (dict_index+1, dict_size))
            dict_index +=1
        # ... then edge boundaries.
        dict_size = len(self.edgeboundaries)
        dict_index = 0

        
        # Edge boundaries.
        
        for bdkey, edgebndy in self.edgeboundaries.items():
            edgebndy.sequence()
            realbndy = realmesh.newEdgeBoundary(bdkey)
            # Edges are directed, and the boundary is made up of
            # sequenced edges, so the geometry is deterministic.  When
            # we split nodes, we can in principle distinguish
            # left-side nodes from right-side nodes.  TODO 3.1: Do so.
            for skeletonedge in edgebndy.edges:
                # Look up the corresponding element from the skeleton.
                # When nodes are split, adjacent elements may no
                # longer share the same nodes, using getElements()[1]
                # instead of (if it exists) getElements()[0] would
                # give different results when boundary conditions on
                # an interfacial edge are set.  Make sure to use the
                # element to the left of the skeletonedge.
  
                # TODO 3.1: This doesn't make a lot of sense -- if there's
                # no far-side element, then the nodes aren't split, if
                # the splitting mechanism uses elements.  Also, even
                # if they are split, then it's still the "far side"
                # nodes that are the actual periphery of the system.
                skelel = skeletonedge.getLeftElement()
                realel = realmesh.getElement(skelel.meshindex)

                edge_nodes = skeletonedge.get_nodes()
                realn0 = realel.getCornerNode(
                    skelel.getNodeIndexIntoList(edge_nodes[0]) )
                realn1 = realel.getCornerNode(
                    skelel.getNodeIndexIntoList(edge_nodes[1]) )


                realbndy.addEdge(realel.getBndyEdge(realn0,realn1))
                if prog.stopped():
                    prog.setMessage("Interrupted")
                    return
                else:
                    prog.setFraction(1.0*(dict_index+1)/dict_size)
                    prog.setMessage("Allocating edge boundaries: %d/%d"
                                     % (dict_index+1, dict_size))
            dict_index +=1

        if runtimeflags.surface_mode:
            self.createMeshBdysFromInterfaces(skelctxt, 
                                              realmesh,interface_seg_dict)

        # InterfaceElements are created here.  The design intent at
        # this point is that the geometry is preserved, "left" and
        # "right" are correct for the interface of which this edgement
        # is a part, according to the interface definition.  For
        # exterior edgements, one or the other of the left or right
        # elements may not exist.  The InterfaceElement constructor is
        # responsible for handling this gracefully.
        
        try:
            el2 = edict[2]
        except KeyError: # Many scripts don't supply 1D masterelements
            pass
        else:
            self.createInterfaceElementsFromInterface(interface_seg_dict, 
                                                      realmesh, el2)

        prog.finish()
        return realmesh

    # Interfaces are fundamentally defined in the microstructure, as
    # existing between different materials, or surrounding certain
    # pixel groups.  They are "induced" in the skeleton, because
    # elements inherit the pixel group or material which makes up the
    # majority of their area.  The mesh gets the corresponding pixel
    # or material identities, but needs to do some physics.  These
    # structures do that.  Interfaces here include all skeleton
    # boundaries, including geometrical boundaries (top, bottom, left,
    # right).  The passed-in seg_dict is keyed by segments, and has
    # SegmentData objects as values.
    def createMeshBdysFromInterfaces(self,skelctxt,realmesh,seg_dict):
        interfacemsplugin=self.MS.getPlugIn("Interfaces")
        # Construct a dict interface_seglist[interfacename]=[seg1,seg2,...]
        # from the interface graph seg_dict.
        # An interface with zero segments would not show up in this dict.
        interface_seglist={}
        for segkey,data in seg_dict.items():
            for interfacename in data._interfacenames:
                try:
                    seglist=interface_seglist[interfacename]
                    seglist.append(self.segments[segkey])
                except KeyError:
                    interface_seglist[interfacename]=[self.segments[segkey]]
        #Construct realmesh boundaries from the interface segments
        for interfacename, seglist in interface_seglist.items():
            try:
                interfacedef=interfacemsplugin.namedinterfaces[interfacename]
            except KeyError:
                # Must not include skeleton boundary names
                continue
            # Sequence the segments. The sequenced segments may need
            # to be reversed.
            try:
                (seg_seq, node_seq, winding_vec)=skeletonsegment.segSequence(
                    seglist)
                if len(seg_seq)==0:
                    #Don't expect this to happen
                    raise ooferror.ErrPyProgrammingError(
                        "Got empty sequenced segment list!")
                iels = interfacedef.getAdjacentElements(seg_seq[0],skelctxt)
                if iels:
                    if iels.left:
                        if iels.left.nodesInOrder(node_seq[0],node_seq[1])==0:
                            seg_seq.reverse()
                    else:
                        #iels.left is allowed to be None. This occurs
                        #for segments lying on the exterior boundary
                        #and with a 'direction' such that the exterior
                        #space is to its 'left'.
                        #
                        #       exterior space,
                        #       to the 'left' of the arrow
                        #    ----------->-----------
                        #    |                     |
                        #    |    microstructure   |
                        #    |                     |
                        #
                        if iels.right.nodesInOrder(node_seq[0],node_seq[1]):
                            seg_seq.reverse()
                else:
                    raise ooferror.ErrPyProgrammingError(
                        "Expecting this segment to be part of the interface!")
            except skeletonsegment.SequenceError:
                #Non-sequenceable
                seg_seq=seglist
            #Create a new realmesh boundary for the interface.
            #Note that this mesh boundary does not originate from
            #a skeleton boundary!
            realbndy = realmesh.newEdgeBoundary(interfacename)
            #Add edges to the realmesh boundary
            for seg in seg_seq:
                iels = interfacedef.getAdjacentElements(seg,skelctxt)
                if iels:
                    if iels.left:
                        skelel = iels.left
                        #Make sure to have the nodes in the right order
                        #for the realmesh boundary edge.
                        if skelel.nodesInOrder(*seg.get_nodes()):
                            sn0=seg.get_nodes()[0]
                            sn1=seg.get_nodes()[1]
                        else:
                            sn0=seg.get_nodes()[1]
                            sn1=seg.get_nodes()[0]
                    else:
                        skelel = seg.getElements()[0] # Right-side? 
                        if skelel.nodesInOrder(*seg.get_nodes()):
                            sn0=seg.get_nodes()[1]
                            sn1=seg.get_nodes()[0]
                        else:
                            sn0=seg.get_nodes()[0]
                            sn1=seg.get_nodes()[1]
                else:
                    raise ooferror.ErrPyProgrammingError(
                        "Expecting this segment to be part of the interface!")
                realel = realmesh.getElement(skelel.meshindex)
                realn0 = realel.getCornerNode(skelel.getNodeIndexIntoList(sn0))
                realn1 = realel.getCornerNode(skelel.getNodeIndexIntoList(sn1))
                realbndy.addEdge(realel.getBndyEdge(realn0,realn1))

    def createInterfaceElementsFromInterface(self,seg_dict,realmesh,edgemaster):
        # seg_dict is the dictionary of segments in this interface.
        # realmesh is the mesh in which the InterfaceElements will live.
        # edgemaster is the 1D master element.
        for segkey,data in seg_dict.items():
            seg=self.segments[segkey]
            els=seg.getElements()
            #TODO MER: Interface may not have an interface material
            # Left and right are set, but either can be None.
            if data._materialname:
                cmat=materialmanager.materialmanager[data._materialname].actual
            else:
                cmat=None
            leftelem=data._leftskelel
            rightelem=data._rightskelel

            # Figure out the "boundary-first" and "boundary-last"
            # nodes -- these are needed later to compute the left-side
            # and right-side normals.

            # boundary_first_node and trailing_node can in principle be
            # undefined, if there was neither a right nor left
            # element.  We'll take that chance.

            # Skeleton nodes cannot be split, so we are done for now.

            leftnodes=None
            rightnodes=None

            # The inorder booleans indicate whether the respective
            # node lists are in interface-order or not, i.e. if the
            # first node in the list is the first one you encounter as
            # you traverse the interface with the left-side elements
            # on the left and the right-side elements on the right.
            # TODO OPT: It may be cleaner to just arrange for the node
            # lists to always be in order.  This is not done now
            # because there may be subtle order-dependencies
            # downstream.
            leftnodes_inorder = None
            rightnodes_inorder = None
            if leftelem:
                realel = realmesh.getElement(leftelem.meshindex)
                irealn0 = leftelem.getNodeIndexIntoList(segkey[0])
                realn0 = realel.getCornerNode( irealn0 )
                irealn1 = leftelem.getNodeIndexIntoList(segkey[1])
                realn1 = realel.getCornerNode( irealn1 )

                #Find the nodes on the edge between realn0 and realn1.
                #See skeletonelement.py to verify how real nodes
                #are added to the list and passed to the element.
                ncorners = realel.ncorners()
                found=False
                if (irealn0+1)%ncorners==irealn1:
                    leftnodes=[realn0]
                    for rn in realel.node_iterator():
                        if found:
                            if rn==realn1:
                                break
                            leftnodes.append(rn)
                        if rn==realn0:
                            found=True
                    leftnodes.append(realn1)
                    leftnodes_inorder = True
                else:
                    leftnodes=[realn1]
                    for rn in realel.node_iterator():
                        if found:
                            if rn==realn0:
                                break
                            leftnodes.append(rn)
                        if rn==realn1:
                            found=True
                    leftnodes.append(realn0)
                    leftnodes.reverse()
                    leftnodes_inorder = False
            if rightelem:
                realel = realmesh.getElement(rightelem.meshindex)
                irealn0 = rightelem.getNodeIndexIntoList(segkey[0])
                realn0 = realel.getCornerNode( irealn0 )
                irealn1 = rightelem.getNodeIndexIntoList(segkey[1])
                realn1 = realel.getCornerNode( irealn1 )

                if rightelem.nodesInOrder(*segkey):
                    right_first_node = realn1
                    right_last_node = realn0
                else:
                    right_first_node = realn0
                    right_last_node = realn1

                #Find the nodes on the edge between realn0 and realn1.
                #See skeletonelement.py to verify how real nodes
                #are added to the list and passed to the element.
                ncorners = realel.ncorners()
                found=False
                if (irealn0+1)%ncorners==irealn1:
                    rightnodes=[realn0]
                    for rn in realel.node_iterator():
                        if found:
                            if rn==realn1:
                                break
                            rightnodes.append(rn)
                        if rn==realn0:
                            found=True
                    rightnodes.append(realn1)
                    rightnodes_inorder = False
                else:
                    rightnodes=[realn1]
                    for rn in realel.node_iterator():
                        if found:
                            if rn==realn0:
                                break
                            rightnodes.append(rn)
                        if rn==realn1:
                            found=True
                    rightnodes.append(realn0)
                    rightnodes.reverse()
                    rightnodes_inorder = True
     
            # TODO MER: Double-check what this is about.  Historically,
            # the code did this to ensure that both node lists were
            # valid, by just passing redundant info in the case where
            # one of them is None.  This does not break the geometry,
            # so leave it in for now.

            # NB leftnodes and rightnodes can't *both* be None, that
            # only happens if the there are no elements on either side
            # of the segment, and in that case, we don't get called at
            # all.  TODO MER: Is this in fact true?  What about empty
            # elements?
                    
            if not leftnodes:
                leftnodes = rightnodes
                leftnodes_inorder = rightnodes_inorder
            else:
                if not rightnodes:
                    rightnodes = leftnodes
                    rightnodes_inorder = leftnodes_inorder


            if leftelem:
                #segmentordernumber is the index of the segment
                #in the list returned by skelel.getSegments().
                #It is passed to the edgement, so that it can
                #be used to retrieve the segment given the first
                #side1elem (or side2elem, if side1elem is None).
                segmentordernumber=leftelem.getSegmentOrderNumber(seg,self)
            else:
                # TODO MER: Check if this preserves the geometry.
                segmentordernumber=rightelem.getSegmentOrderNumber(seg,self)
            #Pass the realnodes on the edge of the element on 1 side
            #and the realnodes on the edge on the other side of the
            #interface segment. The list of nodes may be identical.
            #side1elem or side2elem (but not both) may be None.

            # The below is no longer true.  The first argument is
            # always the left side, even if there is no left side.

            #If the interface segment is at an exterior boundary,
            #side1elem is automatically the first element returned by
            #seg.getElements(), unless the element does not have a material
            #or pixel group.
                
            edgement=edgemaster.buildInterfaceElement(leftelem,
                                                      rightelem,
                                                      segmentordernumber,
                                                      cmat,
                                                      leftnodes,rightnodes,
                                                      leftnodes_inorder,
                                                      rightnodes_inorder,
                                                      data._interfacenames)
            realmesh.addInterfaceElement(edgement)
                                     
    def getInterfaceZoneNumberAtElem(self,skelnode,skelelem,seg_dict):
        # Returns -1 if there are no interfaces at the node.
        interfacesegments=self.getInterfaceSegmentsAtNode(skelnode,seg_dict)
        if len(interfacesegments)==0:
            return -1
        # Add in the exterior boundary segments incident on skelnode
        # if skelnode is at an exterior boundary.
        exteriorsegments = skelnode.exteriorSegments(self)
        isExteriorNode = len(exteriorsegments) > 0
        for seg in exteriorsegments:
            interfacesegments.add(seg)
#         nodex=skelnode.position().x
#         nodey=skelnode.position().y
#         isExteriorNode=False
#         if (nodex==0 or nodex==self.size().x or \
#             nodey==0 or nodey==self.size().y):
#             isExteriorNode=True
#             localsegments=skelnode.localSegments(self)
#             for seg in localsegments:
#                 if seg.nElements()==1 and (seg not in interfacesegments):
#                     interfacesegments.append(seg)

        #Start at a segment that lies at an exterior boundary, if it exists
        if isExteriorNode:
            startsegment = exteriorsegments.pop()
            interfacesegments.remove(startsegment)
        else:
            startsegment = interfacesegments.pop()
#         startsegment=interfacesegments[0]
#         for seg in interfacesegments:
#             if seg.nElements()==1:
#                 startsegment=seg
#                 break
#         interfacesegments.remove(startsegment)
        #CW or CCW, it depends on the first element in getElements()
        startelement=startsegment.getElements()[0]
        if skelelem==startelement:
            return 0
        numzones=1
        while len(interfacesegments)>0:
            #Now starting at startsegment, get the 'fan' of adjacent elements
            #until we encounter the next interface segment.
            while 1:
                if skelelem==startelement:
                    return numzones-1
                nextsegment=startelement.getOppositeSegment(skelnode,
                                                        startsegment,
                                                        self)
                #TODO MER: Assign result directly to startsegment?
                startsegment=nextsegment
                nextelement=startsegment.getElements()[0]
                if nextelement==startelement:
                    #if getElements() has only one item, then
                    #startsegment is in interfacesegments
                    #(startsegment is on an exterior boundary)
                    #and the loops will terminate.
                    nextelement=startsegment.getElements()[-1]
                startelement=nextelement
                #Removing items from interfacesegments might not be
                #necessary (e.g. use a counter instead).
                if startsegment in interfacesegments:
                    interfacesegments.remove(startsegment)
                    numzones+=1
                    break
        if isExteriorNode:
            raise ooferror.ErrPyProgrammingError("This shouldn't happen!")
        return numzones-1

    def countInterfaceZonesAtNode(self,skelnode,seg_dict):
        # The number of interface zones at at node is the number of
        # interface segments that hit the node, if the node isn't an
        # external node.  If the node is external, it's the number of
        # non-external interface segments plus one. 
        interfacesegments = self.getInterfaceSegmentsAtNode(skelnode, seg_dict)
        if len(interfacesegments)==0:
            return 0
        exteriorsegments = skelnode.exteriorSegments(self)

        for seg in exteriorsegments:
            try:
                interfacesegments.remove(seg)
            except KeyError:
                pass
        numzones = len(interfacesegments)
        if exteriorsegments:
            numzones += 1
        return numzones

    def getInterfaceSegmentsAtNode(self,skelnode,seg_dict):
        neighbornodes = skelnode.neighborNodes(self)
        localsegments = set()
        for nd in neighbornodes:
            segkey = skeletonnode.canonical_order(nd,skelnode)
            if segkey in seg_dict:
                localsegments.add(self.segments[segkey])
        return localsegments

    # This function is used when creating a skeleton boundary from an
    # interface.  This function is also called by
    # DirectorInterfacesWidget (boundarybuilderGUI.py)
    def getInterfaceSegments(self,skelctxt,interfacename):
        interfacemsplugin=self.MS.getPlugIn("Interfaces")
        seglist=[]
        directionlist=[]
        try:
            interfacedef=interfacemsplugin.namedinterfaces[interfacename]
            for key,seg in self.segments.items():
           
                iels = interfacedef.getAdjacentElements(seg,skelctxt)
                if iels:
                    seglist.append(seg)
                    if iels.left:
                        if iels.left.nodesInOrder(*seg.get_nodes()):
                            directionlist.append(1)
                        else:
                            directionlist.append(-1)
                    else:
                        # iels.left is allowed to be None. This occurs
                        # for segments lying on the exterior boundary
                        # and with a 'direction' such that the
                        # exterior space is to its 'left'.
                        #
                        #       exterior space,
                        #       to the 'left' of the arrow
                        #    ----------->-----------
                        #    |                     |
                        #    |    microstructure   |
                        #    |                     |
                        #
                        # If iels.left is None but iels evaluates to True,
                        # then iels.right is guaranteed not to be None.
                        
                        if iels.right.nodesInOrder(*seg.get_nodes()):
                            directionlist.append(-1)
                        else:
                            directionlist.append(1)
        except KeyError:
            pass
        return seglist, directionlist
    
    # getAdjacentElements now returns left and right data.
    # SegmentData lists should use it.
    def createInterfaceSegmentDict(self,skelpath):
        seg_dict = {}
        skelctxt = skeletoncontext.skeletonContexts[skelpath]
        if runtimeflags.surface_mode:
            interfacemsplugin=self.MS.getPlugIn("Interfaces")
            # For each interface, for each segment of the skeleton,
            # check if the segment is a member of the interface (by
            # asking the interface itself, via the plug-in), and
            # retrieve the left-side and right-side elements.
            for interfacename, interfacedef in interfacemsplugin.namedinterfaces.items():
                for key,seg in self.segments.items():
                    iels = interfacedef.getAdjacentElements(seg,skelctxt)
                    if iels:
                        matname = interfacemsplugin.getInterfaceMaterialName(
                            interfacename)
                        try:
                            segmentdata=seg_dict[key]
                            # previous material and skeleton element get
                            # overwritten, but interfacename is added to
                            # the list.
                            segmentdata.setData(matname, 
                                                iels.left,
                                                iels.right,
                                                interfacename)
                        except KeyError:
                            seg_dict[key]=SegmentData(matname, 
                                                      iels.left,
                                                      iels.right,
                                                      interfacename)
# End of surface_mode conditional.

        #Generate segments along skeleton boundaries
        for bdkey, edgebndy in self.edgeboundaries.items():
            matname=skelctxt.getBoundary(bdkey)._interfacematerial
            self._createInterfaceSegmentDictFromSkelBoundary(bdkey, edgebndy,
                                                             matname,
                                                             seg_dict)
        return seg_dict

    # _createInterfaceSegmentDictFromSkelBoundary creates the
    # SegmentData objects needed to create interfaces from the
    # skeleton boundaries. This info is added to the given seg_dict.
    def _createInterfaceSegmentDictFromSkelBoundary(self,bdkey,skelbdy,
                                                    matname, seg_dict):
        skelbdy.sequence() #Should have been sequenced by this point
        bdylength=len(skelbdy.edges)
        for i in xrange(0,bdylength):
            skeledge=skelbdy.edges[i]
            # NOTE: skeledge.get_nodes() returns the nodes in the
            # order indicated by skeledge.direction.
            # skeledge.segment.get_nodes() returns the nodes already
             # in canonical order (see skeletonsegment.py)
            segkey=skeledge.segment.get_nodes()
            els=skeledge.segment.getElements()
            if len(els) == 1:
                #seg_dict[segkey]=(matname,els[0],bdkey)
                if els[0].nodesInOrder(*skeledge.get_nodes()):
                    #seg_dict[segkey]=(matname,els[0],bdkey)
                    leftelem=els[0]
                    rightelem=None
                else:
                    #seg_dict[segkey]=(matname,els[1],bdkey)
                    leftelem=None
                    rightelem=els[0]
            else:
                assert len(els) == 2
                # Nodes in an element are ordered in a CCW fashion.
                # If nodes in a directed segment have the same order
                # as in the element, then that element is to the left
                # of the directed segment.
                #
                #   s ----<------
                #     ----<------
                #     |         |
                #    \|/   e   /|\
                #     |         |
                #     ---->------
                #
                # (element e is to the 'left' of directed segment s)
                #
                if els[0].nodesInOrder(*skeledge.get_nodes()):
                    #seg_dict[segkey]=(matname,els[0],bdkey)
                    leftelem=els[0]
                    rightelem=els[1]
                else:
                    #seg_dict[segkey]=(matname,els[1],bdkey)
                    leftelem=els[1]
                    rightelem=els[0]
            try:
                segmentdata=seg_dict[segkey]
                # previous material and skeleton element get overwritten
                segmentdata.setData(matname,leftelem,rightelem,bdkey)
            except KeyError:
                seg_dict[segkey]=SegmentData(matname,leftelem,rightelem,bdkey)



############################################################################

####################### femesh_shares, for parallel  #####################
    # This version of the method indicates the funcnodes that are
    # shared between processes.  This sharing information is assumed
    # to have been created by Haan's code.  The sharing information
    # should reach the dofs, fields and equations later.
    def femesh_shares(self, edict, set_materials):
        # edict[n] is the n-sided master element.  Find the
        # interpolation order of the elements.  They all have the same
        # order, so just pick one.
        
        #order = edict[edict.keys()[0]].fun_order()
        #This should do the same thing
        order = edict.values()[0].fun_order()

        # set_materials is a function that will be called to assign
        # materials to elements.
        prog = progress.getProgress("parallel femesh", progress.DEFINITE)

        self.cleanUp()

        # Local dictionary of finite-element nodes, indexed by
        # SkeletonNode objects.
        fe_node = {}
        
        # Find which elements and edges are on the geometrical
        # boundaries of the system.
        self.find_geometrical_boundaries()

        realmesh = femesh.FEMesh(self.MS, order)

        # Reserve space in FEMesh::funcnodes and FEMesh::mapnodes so
        # that the vectors aren't continually reallocated.
        nels = {}                       # number of elements of each type
        for n in edict:
            nels[n] = 0
        for el in self.elements:
            nels[el.nnodes()] += 1

        nfuncnodes = self.nnodes() + len(self.segments)*(order-1)
        for n, masterelem in edict.items():
            nfuncnodes += nels[n]*masterelem.ninteriorfuncnodes()
        realmesh.reserveFuncNodes(nfuncnodes)

        masterel = edict[edict.keys()[0]]
        n_map_per_side = masterel.nexteriormapnodes_only()/masterel.nsides()
        nmapnodes = len(self.segments)*n_map_per_side
        for n, masterelem in edict.items():
            nmapnodes += nels[n]*masterelem.ninteriormapnodes_only()
        realmesh.reserveMapNodes(nmapnodes)

        # Make the real nodes at the corners of the elements.  These
        # nodes are always both mapping and function nodes.  A
        # "meshindex" attribute is written into the skeleton node.
        mnodecount = self.nnodes()
        for i in range(self.nnodes()):
            cur = self.nodes[i]
            #Have to include the local skeleton index and the
            #"remote" indices, as well as the processes that share that node.
            realnode = realmesh.newFuncNode_shares(
                coord.Coord(cur.position().x, cur.position().y),
                cur.sharedWith(),
                [cur.remoteIndex(procnum) for procnum in cur.sharedWith()],
                cur.index)
            
            fe_node[cur] = realnode
            #cur.setMeshIndex(realnode.index())
            if prog.stopped():
                return
            prog.setFraction(1.0*(i+1)/mnodecount)
            prog.setMessage("Allocated %d/%d nodes"%(i+1, mnodecount))
        
        # Loop over elements.
        numelements = self.nelements()
        realmesh.reserveElements(numelements)
        for mesh_idx in range(self.nelements()):
            el = self.elements[mesh_idx]

            # Index correspondence happens here -- the skeleton
            # elements are assigned indices in the order that their
            # corresponding real elements are created/assigned.
            # (SkeletonElement.realelement sets self.meshindex when it
            # creates the real element.)
            mnodecount += el.realelement_shares(
                self, realmesh, mesh_idx, fe_node, mnodecount,
                edict, set_materials)
            if prog.stopped():
                return
            prog.setFraction(1.0*(mesh_idx+1)/numelements)
            prog.setMessage("Allocated %d/%d elements"
                            % (mesh_idx+1, numelements))

        # Then do boundaries.
        # Note that edgeboundaries and pointboundaries are in separate lists
        # in the skeleton, but in a single list in the real mesh.

        # Point boundaries first.
        dict_size = len(self.pointboundaries)
        dict_index = 0
        for bdkey, pointbndy in self.pointboundaries.items():
            realbndy = realmesh.newPointBoundary(bdkey)
            for node in pointbndy.nodes:
                realbndy.addNode(fe_node[node]) # Preserve order of nodes.
                if prog.stopped():
                    return
                prog.setFraction(1.0*(dict_index+1)/dict_size)
                prog.setMessage("Allocated %d/%d point boundaries" 
                                % (dict_index+1, dict_size))
            dict_index +=1
        # ... then edge boundaries.
        dict_size = len(self.edgeboundaries)
        dict_index = 0
        for bdkey, edgebndy in self.edgeboundaries.items():
            edgebndy.sequence()
            realbndy = realmesh.newEdgeBoundary(bdkey)
            for skeletonedge in edgebndy.edges:
                # Look up the corresponding element from the skeleton.
                skelel = skeletonedge.segment.getElements()[0]
                realel = realmesh.getElement(skelel.meshindex)
                
                edge_nodes = skeletonedge.get_nodes()
                realn0 = fe_node[edge_nodes[0]]    # First real node.
                realn1 = fe_node[edge_nodes[1]]    # Second real node.
                realbndy.addEdge(realel.getBndyEdge(realn0,realn1))
                if prog.stopped():
                    return
                prog.setFraction(1.0*(dict_index+1)/dict_size)
                prog.setMessage("Allocated %d/%d edge boundaries"
                                % (dict_index+1, dict_size))
            dict_index +=1
        return realmesh

########################## end femesh_shares ###############################

## end of class Skeleton

########################################################################


def newEmptySkeleton(name, msname, left_right_periodicity=False,
             top_bottom_periodicity=False):
    mscontext = microstructure.microStructures[msname]
    ms = mscontext.getObject()
    skel = Skeleton(ms, left_right_periodicity, top_bottom_periodicity)
    skeletoncontext.skeletonContexts.add([msname, name], skel, parent=mscontext)
    return skel

# skeleton_geometry is an object of type SkeletonGeometry, class defined above.
def initialSkeleton(name, ms, nx, ny, skeleton_geometry):
    skel = skeleton_geometry(nx, ny, ms)
    if skel is not None:
        mscontext = microstructure.microStructures[ms.name()]
        skeletoncontext.skeletonContexts.add([ms.name(), name],
                                             skel, parent=mscontext)
    return skel

# Parallel initial skeleton
if parallel_enable.enabled():
    def initialSkeletonParallel(name, ms, nx, ny, skeleton_geometry):
        from ooflib.engine.IO import skeletonIPC
        skeletonIPC.smenu.Initialize(name=name, microstructure=ms,
                                     x_elements=nx, y_elements=ny,
                                     skeleton_geometry=skeleton_geometry)

# Create pixel-to-element skeleton. Thus, homogeneity of all elements will
# be set to "1".
def simpleSkeleton(name, ms, nx, ny, skeleton_geometry):
    skel = skeleton_geometry(nx, ny, ms, preset_homog=True)
    mscontext = microstructure.microStructures[ms.name()]
    skeletoncontext.skeletonContexts.add([ms.name(), name], skel,
                                         parent=mscontext)
    return skel

###########################

## TODO 3.1: Remove the 'skeleton' argument in all ProvisionalChanges
## methods, because self.skeleton can now be used instead.  It's
## probably necessary to give DeputyProvisionalChanges a self.skeleton
## as well.

class ProvisionalChanges:
    def __init__(self, skeleton):
        self.skeleton = skeleton        # Skeleton object. Not context.
        self.removed = []               # elements to be removed 
        self.inserted = []              # provisional elements added
        self.substitutions = []         # pairs (old, new) of el. substitutions
        self.seg_subs = {}              # {old:[new segs] ...}
        self.movednodes = []            # list of MoveNode objects
        self.cachedDeltaE = None        # Energy difference
        self.before = None              # Elements before the change
        self.after = None               # Elements after the change
    def removeAddedNodes(self, skeleton):
        # redefined by subclasses that add nodes
        pass
            
    class MoveNode:                     # nested class definition
        def __init__(self, node=None, position=None, mobility=None):
            self.node = node
            self.position = position
            self.mobility = mobility

    def removeElements(self, *elements):
        for element in elements:
            self.removed.append(element)

    def insertElements(self, *elements):
        for element in elements:
            self.inserted.append(element)

    def substituteElement(self, old, new):
        # Old and new elements must have the same number of nodes, and
        # corresponding nodes must be in the same positions in the
        # element's node lists, so that the correct parent-child
        # relationships may be made for the corresponding segments.
        self.substitutions.append([old, new])

    def substituteSegment(self, old, new):  # "new" has to be a list
        self.seg_subs[old] = new

    def moveNode(self, node, position, mobility=(1,1)):
        self.movednodes.append(
            self.MoveNode(node=node, position=position, mobility=mobility))

    def nRemoved(self):
        return len(self.removed)

    def elBefore(self):
        if self.before is None:
            self.before = self.removed + [o for o,n in self.substitutions]
            for mvnode in self.movednodes:
                for nbr in mvnode.node.neighborElements():
                    if nbr not in self.before:
                        self.before.append(nbr)
        return self.before

    def elAfter(self):
        if self.after is None:
            self.after = self.inserted + [n for o,n in self.substitutions]
            for mvnode in self.movednodes:
                for nbr in mvnode.node.neighborElements():
                    if (nbr not in self.removed) and (nbr not in self.after):
                        self.after.append(nbr)
        return self.after

    def makeNodeMove(self, skeleton):
        for mvnode in self.movednodes:
            mvnode.node.moveTo(mvnode.position)

    def moveNodeBack(self, skeleton):
        for mvnode in self.movednodes:
            mvnode.node.moveBack()        

    def illegal(self, skeleton):
        # Will this change produce any illegal elements?
        self.makeNodeMove(skeleton) # Move nodes to simulate the change
        try:
            # Check elements
            for element in self.elAfter():
                if element.illegal():
                    return True
        finally:
            self.moveNodeBack(skeleton) # Move nodes back
        return False

    def deltaE(self, skeleton, alpha):
        # Return the change in energy per element if this move were to
        # be accepted.
        if self.cachedDeltaE is None:
            # Energy before the change
            oldE = 0.0
            for element in self.elBefore():
                oldE += element.energyTotal(skeleton, alpha)
            oldE /= len(self.elBefore())
            # Move nodes accordingly to simulate the change
            self.makeNodeMove(skeleton)
            # Energy after the change
            newE = 0.0
            for element in self.elAfter():
                # TODO OPT: perhaps using cachedHomogeneities as in
                # the deputy would be helpful here too
                newE += element.energyTotal(skeleton, alpha)
            newE /= len(self.elAfter())
            # Move node back
            self.moveNodeBack(skeleton)
            # Energy differnce due to the change
            self.cachedDeltaE = newE - oldE
        return self.cachedDeltaE

    def deltaEBound(self, skeleton, alpha):
        # Return the maximum possible deltaE -- assuming all elements
        # become homogenous after the change
        if self.cachedDeltaEBound is None:
            # Energy before the change
            oldE = 0.0
            for element in self.elBefore():
                oldE += element.energyTotal(self.skeleton, alpha)
            oldE /= len(self.elBefore())
            # Move nodes accordingly to simulate the change
            self.makeNodeMove(self.skeleton)
            # Energy after the change
            newE = 0.0
            for element in self.elAfter():
                newE += (1.-alpha)*element.energyShape()+alpha
            newE /= len(self.elAfter())
            # Move node back
            self.moveNodeBack(self.skeleton)
            # Energy differnce due to the change
            self.cachedDeltaEBound = newE - oldE        
        return self.cachedDeltaEBound
            
    def accept(self, skeleton):
        # Create actual elements to replace the provisional ones.  The
        # actual elements replace their predecessors in the
        # ProvisionalChanges object, so that they're available to the
        # calling routine.
        ## TODO OPT: Remove argument and use self.skeleton instead?        
        self.inserted = [element.accept(skeleton) for element in self.inserted]
        for mvnode in self.movednodes:
            mvnode.node.moveTo(mvnode.position)
            if mvnode.mobility:
                mvnode.node.setMobilityX(mvnode.mobility[0])
                mvnode.node.setMobilityY(mvnode.mobility[1])
        for pair in self.substitutions:
            old, new = pair
            newelement = new.accept(skeleton)
            pair[1] = newelement
            oldsegments = old.getSegments(skeleton)
            newsegments = newelement.getSegments(skeleton)
            for oldseg, newseg in zip(oldsegments, newsegments):
                for parent in oldseg.getParents():
                    newseg.add_parent(parent)
                    parent.add_child(newseg)
            # Call Skeleton.removeElements only *after* the segment
            # parents have been reestablished, because removing the
            # elements may remove the segments from the skeleton.
            skeleton.removeElements(old)
        for old in self.seg_subs:
            new_segs = self.seg_subs[old]
            for new in new_segs:
                for parent in old.getParents():
                    new.add_parent(parent)
                    parent.add_child(new)
        skeleton.removeElements(*self.removed)

class ProvisionalInsertion(ProvisionalChanges):
    def __init__(self, skeleton):
        ProvisionalChanges.__init__(self, skeleton)
        self.addedNodes = []

    def addNode(self, node):
        self.addedNodes.append(node)
        
    def removeAddedNodes(self, skeleton):
        ## TODO OPT: Remove argument and use self.skeleton instead?
        for n in self.addedNodes:
            n.destroy(skeleton)

class ProvisionalMerge(ProvisionalChanges):
    def __init__(self, skeleton, node0, node1):
        ProvisionalChanges.__init__(self, skeleton)
        self.node0 = node0
        self.node1 = node1
    def accept(self, skeleton):
        ## TODO OPT: Remove argument and use self.skeleton instead?
        self.node0.makeSibling(self.node1)
        ProvisionalChanges.accept(self, skeleton)

class ProvisionalMerges(ProvisionalChanges):
    def __init__(self, skeleton, *pairs):
        ProvisionalChanges.__init__(self, skeleton)
        self.pairs = pairs
    def accept(self, skeleton):
        for pair in self.pairs:
            pair[0].makeSibling(pair[1])
        ProvisionalChanges.accept(self, skeleton)
