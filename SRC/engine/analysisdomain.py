# -*- python -*-
# $RCSfile: analysisdomain.py,v $
# $Revision: 1.40.2.28 $
# $Author: langer $
# $Date: 2014/08/20 02:21:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Domain objects.  These are part of the post-solution mesh analysis
# process.  A "domain" is a user-specified portion of a mesh or that
# mesh's microstructure, specified in terms of mesh or microstructure
# objects, like pixels, elements, cross-sections, etc.

# One cannot actually evalute an output on a domain -- it's necessary
# to sample the domain first, and the sample objects are the
# numerically savvy components.  There can be more than one sampling
# of a domain.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import direction
from ooflib.SWIG.common import pixelgroup
from ooflib.SWIG.engine import element
from ooflib.SWIG.engine import elementshape
from ooflib.SWIG.engine import masterelement
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import microstructure
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelgroupparam
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
from ooflib.engine import analysissample
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import meshcsparams
from ooflib.engine.IO import meshparameters
from ooflib.engine.IO import skeletongroupparams
from ooflib.common import parallel_enable
import ooflib.engine.mesh

import math
import sys

## TODO OPT: Give Domains XXXXsize() methods, which can be used by the
## SampleSets to determine the size without generating the samples.
## This will allow SampleSets that use iterators or generators to know
## if their make_samples() methods should return False, and to use
## progress bars.  Some domains have more than one kind of size
## (number of voxels and number of elements, for example) so there
## can't just be a generic size() method.

class Domain(registeredclass.RegisteredClass):
    registry = []
    def set_mesh(self, mesh):
        if mesh is not None:
            self.mesh = mesh
            self.meshctxt = ooflib.engine.mesh.meshes[mesh]
            self.femesh = self.meshctxt.getObject()
            self.skeleton = self.femesh.skeleton
            self.skelcontext = skeletoncontext.skeletonContexts[
                skeletoncontext.extractSkeletonPath(mesh)]
            self.ms = self.meshctxt.getMicrostructure()
            self.mscontext = self.skelcontext.getParent()
        else:
            self.mesh = None
            self.meshctxt = None
            self.femesh = None
            self.skeleton = None
            self.skelcontext = None
            self.ms = None
            self.mscontext = None
    def read_lock(self):
        self.meshctxt.begin_reading()
        self.skelcontext.begin_reading()
        self.mscontext.begin_reading()
    def read_release(self):
        self.mscontext.end_reading()
        self.skelcontext.end_reading()
        self.meshctxt.end_reading()

    tip = "A specified region of &mesh; or its &micro; for sampling."
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/domain.xml')

# SurfaceDomains are ones where a normal vector can be computed.
# BulkDomains are all the rest, even linear and point domains.  An
# Output that can only be computed on surfaces cannot be computed on a
# bulk domain.  However, an Output that can only be computed in the
# bulk *can* be computed on a surface domain, because the surface
# points can be translated into points in the neighboring bulk
# elements.

class BulkDomain(Domain):
    def compatible(self, output):
        return not output.isSurfaceOnly()

class SurfaceDomain(Domain):
    def compatible(self, output):
        return True

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Each subclass implements some subset of retrieval functions, which
# return information about the domain, in the form of a bounding-box
# rectangle, or a list of objects (elements, points).  The caller is
# expected to be something that will then construct sample objects, or
# wrap the returned objects in sample objects.

# Retrieval functions are things like get_bounds, get_pixels, or
# get_elements.  Not all retrieval functions exist for all domains,
# and some retrieval functions might be expensive.  They should return
# None or an empty list if the domain is empty.

# Units, where they make sense, are physical units on the
# microstructure.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# An object for operating on the entire mesh.
class EntireMesh(BulkDomain):
    # Returns a bounding rectangle.
    def get_bounds(self):
        return primitives.rectangleFactory(primitives.origin(),
                                           self.ms.size())
    
    # Returns a iterable object containing iPoint pixel indices.  It's
    # a memory-efficient iteratable, not an actual list or tuple.
    def get_pixels(self):
        return self.ms.coords() 

    def contains(self, pt):
        return True

    # Returns a "list" of all the elements.  It's not really a list,
    # but an iterable FEMeshElementProxy object.  See femesh.spy.
    def get_elements(self):
        return self.femesh.elements()
        

registeredclass.Registration(
    'Entire Mesh',
    Domain,
    EntireMesh,
    0,
    params=[],
    sampling=(analysissample.GridSampleSetBase, analysissample.PixelSampleSet,
              analysissample.ContinuumSampleSet),
    tip='Use the entire Mesh as a post-processing domain.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/entire_mesh.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Pixel selection or group -- these actually live on
# the host microstructure, so you have to go there to get 'em.
class PixelGroup(BulkDomain):
    def __init__(self, group):
        self.group = group
    def _pixels_from_group(self):
        ## TODO OPT: Use a function that returns an iterable that doesn't
        ## store all of its values.  See CMicrostructure.coords() in
        ## cmicrostructure.spy.
        if self.group == placeholder.selection:
            return  self.ms.pixelselection.getSelection()
        elif self.group == placeholder.every:
            return self.ms.coords()
        else:
            group = self.ms.findGroup(self.group)
            if group:
                return group.members()
    def get_pixels(self):
        return self._pixels_from_group()
    def contains(self, pt):
        ipt = self.ms.pixelFromPoint(pt)
        if self.group == placeholder.selection:
            return self.ms.pixelselection.getObject().isSelected(ipt)
        elif self.group == placeholder.every:
            return True
        else:
            cat = self.ms.category(ipt)
            groups = pixelgroup.pixelGroupNames(self.ms, cat)
            return self.group in groups
    def get_bounds(self):
        if self.group == placeholder.selection:
            if not self.ms.pixelselection.empty():
                pmin, pmax = self.ms.pixelselection.getBounds()
            else:
                pmin = pmax = primitives.iOrigin()
        elif self.group == placeholder.every:
            pmin = primitives.iOrigin()
            pmax = self.ms.sizeInPixels()
        else:
            group = self.ms.findGroup(self.group)
            if group:
                pmin, pmax = group.getBounds()
            else:
                pmin = pmax = primitives.iOrigin()
        return primitives.rectangleFactory(pmin, pmax)

if config.dimension() == 2:
    pname = 'pixel'
else:
    pname = 'voxel'
    
registeredclass.Registration(
    pname.capitalize() + " Group",
    Domain,
    PixelGroup,
    10,
    params=[pixelgroupparam.PixelAggregateParameter(
        'group',
        tip=parameter.emptyTipString)],
    sampling=(analysissample.GridSampleSetBase, analysissample.PixelSampleSet),
    tip="Use a %s group as a post-processing domain." % pname,
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/pixelgroup_domain.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Cross-section -- currently, all cross-sections are straight, so the
# endpoints provide a complete description.  Also, the elemental
# segments are straight.  This is named "CrossSectionDomain" to
# distinguish it from the CrossSection class which represents actual
# cross-sections in the mesh.

class LinearCrossSectionDomain(BulkDomain):
    def __init__(self, cross_section):
        self.cross_section=cross_section
        
    def get_endpoints(self):
        dim = config.dimension()
        cs_obj = self.meshctxt.getCrossSection(self.cross_section)
        bounds = self.meshctxt.size()
        errmsg = ("Segment %s, %s is entirely outside the mesh."
                  %(cs_obj.start, cs_obj.end))
        # Check that both endpoints aren't out of bounds on the same
        # side of the bounding box in any dimension.
        for i in range(dim):
            if ((cs_obj.start[i] < 0 and cs_obj.end[i] < 0) or
                (cs_obj.start[i] > bounds[i] and cs_obj.end[i] > bounds[i])):
                raise ooferror2.ErrUserError(errmsg)
        
        # If an endpoint is out of bounds in any dimension, project it
        # back onto the bounding planes.  First, clone the endpoints
        # so that we aren't modifying the data in the cross section
        # object.
        real_start = primitives.Point(*tuple(cs_obj.start))
        real_end = primitives.Point(*tuple(cs_obj.end))
        for i in range(dim):
            direction = real_end - real_start
            otherdims = [(i+j)%dim 
                         for j in range(1, dim)]
            if real_start[i] < 0:
                # direction[i] can't be zero if real_start[i] < 0 or
                # else the bounding box check above would have failed.
                alpha = -real_start[i]/direction[i]
                for j in otherdims:
                    real_start[j] += alpha*direction[j]
                real_start[i] = 0 # don't allow roundoff
            elif real_start[i] > bounds[i]:
                alpha = (real_start[i] - bounds[i])/direction[i]
                for j in otherdims:
                    real_start[j] -= alpha*direction[j]
                real_start[i] = bounds[i]

            if real_end[i] < 0:
                alpha = -real_end[i]/direction[i]
                for j in otherdims:
                    real_end[j] += alpha*direction[j]
                real_end[i] = 0
            elif real_end[i] > bounds[i]:
                alpha = (real_end[i] - bounds[i])/direction[i]
                for j in otherdims:
                    real_end[j] -= alpha*direction[j]
                real_end[i] = bounds[i]

        # Check that the clipped segment isn't infinitesimal.  This
        # can happen if it grazes a corner of the Microstructure.
        seg = real_end - real_start
        if seg*seg == 0:
            raise ooferror2.ErrUserError(errmsg)

        # Check that the modified points aren't out of bounds, which
        # can happen if the original points were placed sufficiently
        # perversely.
        for i in range(dim):
            if not (0 <= real_start[i] <= bounds[i] and
                    0 <= real_end[i] <= bounds[i]):
                raise ooferror2.ErrUserError(errmsg)

        return (real_start, real_end)

    def make1DElement(self, currentEl, master, segstart, segend):
        # debug.fmsg("Creating 1D element from", segstart, "to", 
        #            segend, "length=", math.sqrt((segend-segstart)**2))
        el1d = master.buildLite([segstart, segend])
        el1d.bulk_element = self.femesh.getElement(
            currentEl.getMeshIndex())
        return el1d

    def get_elements(self):
        elements = []           # list of 1D elements
        csstart, csend = self.get_endpoints()
        length2 = (csend - csstart)**2
        skelobj = self.meshctxt.getSkeleton()

        currentEl = skelobj.enclosingElement(csstart)

        eshape = elementshape.getShape("Line")
        # Create 1st order elements.  The integration routine in
        # ContinuumSample.integrate() doesn't use nodal values, so 1st
        # order elements are sufficient.
        master = masterelement.getMasterElementByShape(eshape, 1, 1)
        segstart = csstart

        # The first step is special
        intersectionPt = currentEl.startLinearXSection(skelobj, csstart, csend)
        segend = intersectionPt.position()
        elements.append(self.make1DElement(currentEl, master, segstart, segend))
        intersectionPt.addTraversedElement(currentEl)
        
        while not intersectionPt.done():
            segstart = segend
            intersectionPt = intersectionPt.next(skelobj)
            segend = intersectionPt.position()
            nextEl = intersectionPt.getElement()
            elements.append(
                self.make1DElement(nextEl, master, segstart, segend))
            intersectionPt.addTraversedElement(nextEl)

        return elements

    def convertToBulk(self, el1d):
        return el1d.bulk_element

if config.dimension() == 2:
    xsname = 'Cross Section'
else:
    xsname = 'Linear Cross Section'
registeredclass.Registration(
    xsname,
    Domain,
    LinearCrossSectionDomain,
    20,
    params=[
        meshcsparams.MeshCrossSectionParameter(
            'cross_section', tip='The cross section to sample.')
    ],
    sampling=(analysissample.LinearGridSampleSetBase,
              analysissample.ContinuumSampleSet),
    tip='Use a line through a Mesh as the post-processing domain.',
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/xsection_domain.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PlanarCrossSectionDomain(SurfaceDomain):
    def __init__(self, normal, offset, side):
        self.normal = normal
        self.offset = offset
        self.side = side
        self.plane = primitives.OrientedPlane(normal, offset, side)

    def get_elements(self):
        elements = []
        for el in self.femesh.elements():
            polygon = el.intersectPlane(self.femesh, self.plane)
            if polygon:
                # Create 1st order elements.  The integration routine in
                # ContinuumSample.integrate() doesn't use nodal values, so 1st
                # order elements are sufficient.
                el2d = element.createTwoDElementLite(polygon)
                el2d.bulk_element = el
                elements.append(el2d)
        return elements

    def convertToBulk(self, el2d):
        return el2d.bulk_element

registeredclass.ThreeDOnlyRegistration(
    "Planar Cross Section",
    Domain,
    PlanarCrossSectionDomain,
    20,
    params=[
        parameter.ConvertibleRegisteredParameter(
            "normal", direction.Direction,
            direction.VectorDirection(1., 0., 0.),
            "The normal direction to the cross section plane."),
        parameter.FloatParameter(
            "offset", 0.0,
            tip="The distance from the origin to the cross section plane."),
        enum.EnumParameter(
            "side", primitives.PlaneOrientation, "FRONT",
            tip="Evaluate the output with elements on this side of the plane.")
    ],
    sampling=(analysissample.ContinuumSampleSet,),
    tip="Use a plane through the Mesh as the post-processing domain."
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ElementGroup(BulkDomain):
    def __init__(self, elements):
        self.elements = elements # name of an element group
    def _elements_from_aggregate(self):
        skel_els = []
        if self.elements == placeholder.selection:
            skel_els = self.skelcontext.elementselection.retrieveFromSkeleton(
                self.skeleton)
        else:
            skel_els = self.skelcontext.elementgroups.get_groupFromSkeleton(
                self.elements, self.skeleton)
        return [self.femesh.getElement(s.getMeshIndex()) for s in skel_els]

    def get_bounds(self):
        minpos = self.meshctxt.size()
        maxpos = primitives.origin()
        dims = range(config.dimension())
        for e in self._elements_from_aggregate():
            for pos in e.cornernodePositions():
                for i in dims:
                    minpos[i] = min(minpos[i], pos[i])
                    maxpos[i] = max(maxpos[i], pos[i])
        return primitives.rectangleFactory(minpos, maxpos)

    def contains(self, pt):
        skelel = self.skeleton.enclosingElement(pt)
        if self.elements == placeholder.selection:
            return skelel.isSelected()
        return skelel.is_in_group(self.elements)
            
    def get_elements(self):
        return self._elements_from_aggregate()

registeredclass.Registration(
    'Element Group',
    Domain,
    ElementGroup,
    30,
    params=[skeletongroupparams.ElementAggregateParameter(
        'elements',
        tip='Elements to sample.')],
    sampling=(analysissample.GridSampleSetBase,
              analysissample.ContinuumSampleSet),
    tip='Use an element group as the post-processing domain.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/element_group_domain.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SinglePoint(BulkDomain):
    def __init__(self, point):
        self.point = point
    def get_points(self):
        return [self.point]

registeredclass.Registration(
    'Single Point',
    Domain,
    SinglePoint,
    ordering=0.5,
    params=[
        primitives.PointParameter(
            'point', tip='Undisplaced position of the sample point.')
    ],
    sampling=(analysissample.PointSampleSet,),
    tip='Use a single point for the post-processing domain.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/pointdomain.xml')
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Using an edge boundary as a domain doesn't make sense in 3D, because
# it's not possible to specify which elements to use.

## TODO OPT: Actually, it's possible to evaluate Fields if the nodes
## aren't split, and it's possible to evaluate Fluxes if we don't care
## which bulk element is used to do the computation.

## TODO MER: This hasn't been updated to work with the new (5/14)
## SampleSet code.

class SegmentSide(enum.EnumClass('LEFT', 'RIGHT')):
    tip="The side of an element edge on which output data should be computed."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/enum/segmentside.xml')

class SkeletonEdgeBoundaryDomain(BulkDomain):
    def __init__(self, boundary, side):
        self.boundary = boundary
        self.side = side
    # Builds (and returns) a list of tuples, each consisting of a
    # primitives.Segment object and a mesh element. 
    def get_elemental_segments(self):
        result = []
        skel = self.meshctxt.getParent().getObject()
        bdy = skel.getEdgeBoundaries()[self.boundary]
        for edge in bdy.getOrientedSegments():
            nodes = edge.get_nodes()
            if self.side == 'LEFT':
                el = edge.getLeftElement()
            else:
                el = edge.getRightElement()
            result.append((primitives.Segment(nodes[0].position(),
                                              nodes[1].position()),
                           self.femesh.getElement(el.meshindex)))
        return result

registeredclass.TwoDOnlyRegistration(
    'Edge Boundary',
    Domain,
    SkeletonEdgeBoundaryDomain,
    25,
    params=[
        skeletongroupparams.SkeletonEdgeBoundaryParameter(
            'boundary',
            tip="The name of the boundary on which to evaluate the output."),
        enum.EnumParameter(
            'side', SegmentSide,
            tip="Use the element on this side, if both exist.")],
    sampling=(analysissample.ContinuumSampleSet,),
    tip="Use a Skeleton edge boundary as the post-processing domain.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/skeledgedomain.xml')
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class FaceBoundaryDomain(SurfaceDomain):
    def __init__(self, boundary, side):
        self.boundary = boundary
        self.side = side
    def get_elements(self):
        bdy = self.meshctxt.getBoundary(self.boundary)
        # bdy.parts() is a SubDimensionalSetPtr, which is an iterable
        # object in Python.  It has an __iter__() method (defined in
        # edgeset.swg) which returns a SubDimensionalIterator, which
        # has a next() method (in edgeset.spy).  next() returns an
        # OrientedElement, which is just a wrapper around an Element
        # that says if it's reversed or not.
        return bdy.parts()   
    def convertToBulk(self, element):
        revrse = element.reversed()
        if ((self.side == "FRONT" and not revrse) or
            (self.side == "BACK" and revrse)):
            return element.getFrontBulk()
        return element.getBackBulk()
        

registeredclass.Registration(
    'Face Boundary',
    Domain,
    FaceBoundaryDomain,
    25,
    params=[
        meshparameters.MeshFaceBdyParameter("boundary"),
        enum.EnumParameter(
            "side", primitives.PlaneOrientation,
            tip="Use the element on this side of the interface, if both exist.")
        ],
    sampling=(analysissample.ContinuumSampleSet,),
    tip="Use a Mesh face boundary as the post processing domain."
)

# class EdgeBoundaryDomain(BoundaryDomain):
#     pass

# registeredclass.Registration(
#     'Edge Boundary',
#     Domain,
#     EdgeBoundaryDomain,
#     25,
#     params=[
#         meshparameters.MeshEdgeBdyParameter("boundary")],
#     sample_types = [analysissample.ORIENTEDELEMENT],
#     tip="Use a Mesh edge boundary as the post processing domain."
# )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Evaluating outputs at the nodes of a Skeleton PointBoundary is sort
# of weird, because if a point boundary contains more than one node,
# it's possible that the corresponding boundary in the Mesh should
# contain intermediate nodes, if the Mesh elements are high order.
# SkeletonPointBoundaryDomain is provided for completeness, but
# probably only makes sense when the boundary in question consists of
# a single node.  The same consideration applies to setting boundary
# conditions on a point boundary.

class SkeletonPointBoundaryDomain(BulkDomain):
    def __init__(self, boundary):
        self.boundary = boundary
    def get_points(self):
        skel = self.meshctxt.getParent().getObject()
        bdy = skel.getPointBoundaries()[self.boundary]
        return [n.position() for n in bdy.getNodes()]

registeredclass.Registration(
    'Point Boundary',
    Domain,
    SkeletonPointBoundaryDomain,
    26,
    params=[
        skeletongroupparams.SkeletonPointBoundaryParameter(
            'boundary',
            tip='The name of the boundary on which to evaluate the output.')],
    sampling=(analysissample.PointSampleSet,),
    tip="Use a Skeleton point boundary as the post-processing domain.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/skelptbdydomain.xml')
)

