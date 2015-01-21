# -*- python -*-
# $RCSfile: analysissample.py,v $
# $Revision: 1.53.2.21 $
# $Author: langer $
# $Date: 2014/10/05 03:10:26 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Sampling objects.  A sampling object applies to a particular domain,
# and upon invocation (with appropriate parameters), returns a list of
# samples.  In principle, samples can answer quantitative questions
# about themselves, such as:
#  - What is your location?
#  - What is the value of output O(location)^n on you?
#  - (advanced) What fraction of you satisfies x < O(location) < y?
#
# Element samples understand "value" to mean "integral".  The area
# (volume) of an element can be found by evaluating an output to the
# zeroth power.
# 
# With that caveat, all of the analysis operations should be able to
# compute themselves by asking questions of this type of their
# samples.  For efficiency, samples can cache expensive data, such as
# their area or important area-fractions.

# Some samples make sense to evaluate directly, like points on a grid
# or points on a line, and others do not, because they have no fixed
# location, like elements and pixels.  Directly-evaluate-able sample
# sets should register themselves with "direct=True", and others
# should not.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.engine import element
from ooflib.SWIG.engine import outputval
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import automatic
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
import math
import string
import types

# Sample objects should have a "columnNames" attribute, which is a
# list of strings which identify the columns of data which are
# provided, and a "columnData" routine, which provides a list of
# strings which make up this data.

# The base class has the output-wrapping "columnData" routine -- this
# takes as input a list of strings identifying the headers that are
# actually used, and picks those items out of the data result from the
# subclass's outputData routine.  This base class routine returns a
# list-enclosed list -- subclasses which need to return multiple data
# sets can return several lists.  The length of the top-level list
# returned from this function is the number of data sets.

## TODO: A lot of this machinery should probably be moved to C++,
## although that may be hard to do since it will require Outputs to be
## defined in C++.

## TODONT: Add NodeSample, for printing values directly at Nodes.
## This is hard to do, because we don't have a way of specifying sets
## of Mesh nodes, and it's not a good operation mathematically,
## because it not mesh size invariant.  About the only thing that
## makes sense to do at Nodes is to evaluate Fields, which can be done
## in the MeshInfo toolbox.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# AnalysisDomain Registrations should list the SampleSet classes that
# they're compatible with.  No need for the old SamplingType enums.

# DiscreteSampleSets have a columnNames attribute, which contains the
# names of the columns which might be used to identify the Sample,
# when an analysis prints information point by point.  In that case,
# parameters are automatically generated of the form "show_xxxx" where
# xxxx is a columnName.

# SamplingTypes that make sense only in 3D can safely be defined here,
# even in the 2D code.  They'll never be used.

class SampleSet(registeredclass.RegisteredClass):
    registry = []
    def __init__(self):
        self.sample_list = []
    def get_col_names():
        return []
    def clearSamples(self):
        self.sample_list = []

    tip = "Container for samples.  Outputs are evaluated at samples."
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/sampleset.xml')

class SampleSetRegistration(registeredclass.Registration):
    def __init__(self, name, subclass, ordering, params=[],
                 secret=False, tip=None, discussion=None,
                 direct=False, **kwargs):
        registeredclass.Registration.__init__(
            self, name, SampleSet, subclass, ordering,
            params=params,
            secret=secret,
            tip=tip,
            discussion=discussion,
            direct=direct,       # used by GUI
            **kwargs)

class Sample(object):
    pass
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class DiscreteSampleSet(SampleSet):
    columnNames = []
    def __init__(self, **kwargs):
        # kwargs are show_xxxx for all xxxx in columnNames.  They're
        # booleans.  They have to be stored in self.__dict__ because
        # they're Parameters too.  All subclasses must have **kwargs
        # in their __init__s, so that the columnName args can be
        # automatically added.
        self.__dict__.update(kwargs)
        SampleSet.__init__(self)

    def get_col_names(self):
        return [x for x in self.columnNames
                if getattr(self, _attr_from_colname(x))]
    def columnData(self, header, sample):
        datalist = sample.outputData()
        return [[datalist[self.columnNames.index(x)] for x in header]]

    def evaluate(self, domain, output):
        results = self.evaluateWithExponents(domain, output, (1,))
        return results[1]

    def evaluateWithExponents(self, domain, output, exponents):
        # Return a dictionary keyed by the exponents.  Each entry is a
        # list of output values for each point in the domain,
        # appropriately exponentiated.
        results = {}

        # Exponent 0 is a special case, since it doesn't require
        # evaluating the output. 
        if 0 in exponents:
            r0 = results[0] = []
            for sample in self.sample_list:
                val = output.instancefn(output).one()
                r0.append((sample, val))
            # If 0 is the only exponent requested, we're done.  Don't
            # evaluate the output at all.
            if len(exponents) == 1:
                return results

        remainingexponents = [x for x in exponents if x != 0]
        if remainingexponents:
            femesh = domain.femesh
            skeleton = domain.skeleton
            ## TODO: It would be nice to make only one call to
            ## output.evaluate() here, outside the loop over
            ## samples. But since the element and mastercoord lists
            ## are separate, it would be difficult to combine the
            ## evaluate() calls without making copies of the lists
            ## (which would be inefficient if they're really iterators
            ## and not explicit lists) and/or calling
            ## enclosingElement() extra times.  A solution would be to
            ## change the structure of the args to Output.evaluate,
            ## using a list of (Element, (mcoord, mcoord, ...)) tuples
            ## instead of two lists (or maybe a dict of lists of
            ## MasterCoords, keyed by Elements?).  That would require
            ## extensive modification to the Output class.

            ## TODO: exponent=1 should be another special case, so we
            ## can avoid the call to __pow__.
            for sample in self.sample_list:
                element = femesh.enclosingElement(skeleton, sample.point)
                mcoord = element.to_master(sample.point)
                val = output.evaluate(femesh, domain, [element], [[mcoord]])[0]
                for power in remainingexponents:
                    results.setdefault(power, []).append((sample, val**power))
        return results
    
    # Integration of a discrete SampleSet is just summation.
    def integrate(self, domain, output):
        sums = self.integrateWithExponents(domain, output, (1,))
        return sums[1]
    def integrateWithExponents(self, domain, output, exponents):
        sums = {}
        vals = self.evaluateWithExponents(domain, output, exponents)
        for exponent in exponents:
            s = output.instancefn(output).zero()
            for sample, val in vals[exponent]:
                s += val
            sums[exponent] = s
        return sums

# Utility function, for encapsulating the transformation from column
# names to attribute names for DiscreteSampleSets.  The booleans that
# indicate which columns should be shown are stored in the instance
# __dict__ as "show_<column_name>".  It's done this way because the
# RegisteredClass machinery requires that each parameter correspond to
# an object attribute with the same name.

def _attr_from_colname(colname):
    return "show_"+string.lower(colname)

coordNames = ["X", "Y"]
if config.dimension() == 3:
    coordNames.append("Z")

# Trick function which creates the registrations for SampleSet
# objects.  Makes both a "direct" and an "indirect" version of each
# sample set, the former used for point-wise data output, and the
# latter used for statistical or composite data output.  The
# non-direct subclass is created locally and registered in this
# function, but its registration is not returned, so it's a bit sneaky
# that way.

# The 'direct' flag passed to the Registration is used by the GUI
# widget to help it decide which Registrations to list.


def DiscreteSampleSetRegistration(name, subclass, ordering, params=[],
                                secret=False, tip=None, discussion=None,
                                **kwargs):
    # Create a trivial subclass that doesn't have Parameters or data
    # columns for the Sample-identifying data, for use in the
    # "non-direct" DataOperations that combine multiple samples.
    class NonDirectSubclass(subclass):
        def get_col_names(self):
            return []
    NonDirectSubclass.__name__ = "Stat" + subclass.__name__
    non_direct_params = params[:]
    SampleSetRegistration(
        name, 
        subclass=NonDirectSubclass, 
        ordering=ordering,
        params=non_direct_params,
        secret=secret, tip=tip,
        direct=False,
        discussion="""<para>
        <classname>%(statname)s</classname> is a version of <xref
        linkend='RegisteredClass-%(name)s'/> that is used when the
        <link linkend='MenuItem-OOF.Mesh.Analyze'>analysis
        operation</link> is one of the statistics functions.  It is
        identical, except that it does not have the
        <varname>show_*</varname> parameters, which would be
        meaningless in this context.
        </para>""" % {'name': subclass.__name__,
                      'statname' : NonDirectSubclass.__name__ },
        **kwargs)
    
    for colname in subclass.columnNames:
        params.append(parameter.BooleanParameter(
            _attr_from_colname(colname), True, default=True,
            tip="Include or exclude this data from the output."))
    SampleSetRegistration(
        name, subclass, ordering, params=params, secret=secret,
        direct=True,
        tip=tip, discussion=discussion, **kwargs)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Sample subclasses used by DiscreteSampleSets.  Each sample has a
# "point" datum which is used by DiscreteSampleSet.evaluate().  Other
# data is used to identify the sample in the output.

class DiscreteSample(Sample):
    pass

class PointSample(DiscreteSample):
    def __init__(self, point):
        self.point = point
    def outputData(self):
        return [`v` for v in self.point]

class PointOnALineSample(Sample):
    def __init__(self, point, index, distance, length):
        self.point = point
        self.index = index
        self.distance = distance
        self.length = length
    def outputData(self):
        return [`v` for v in self.point] + [`self.index`, `self.distance`,
                                            `self.distance/self.length`]
    def __repr__(self):
        return "PointOnALineSample(%s)" % self.point

class PixelSample(DiscreteSample):
    def __init__(self, pixel, size):
        self.pixel = pixel
        self.point = primitives.Point(
            *(float(pixel[i])*size[i] + 0.5*size[i]
              for i in range(config.dimension())))
    def outputData(self):
        frmt = "(" + " ".join(["%d"]*config.dimension()) + ")"
        return [frmt % tuple(v for v in self.pixel)] + [`v` for v in self.point]
    
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Subclasses of DiscreteSampleSet

# Base for GridSampleSet and SpacedGridSampleSet
class GridSampleSetBase(DiscreteSampleSet):
    pass

class GridSampleSet(GridSampleSetBase):
    columnNames = coordNames
    if config.dimension() == 2:
        def __init__(self, x_points, y_points, **kwargs):
            self.x_points = x_points
            self.y_points = y_points
            GridSampleSetBase.__init__(self, **kwargs)
        def make_samples(self, domain):
            self.sample_list = []
            box = domain.get_bounds()
            if box and not box.empty():
                bxmin = box.xmin()
                bymin = box.ymin()
                if self.x_points > 1:
                    dx = float(box.xmax()-bxmin)/float(self.x_points-1)
                else:
                    dx = 0
                if self.y_points > 1:
                    dy = float(box.ymax()-bymin)/float(self.y_points-1)
                else:
                    dy = 0
                for j in range(self.y_points):
                    y = bymin + j*dy
                    for i in range(self.x_points):
                        x = bxmin + i*dx
                        pt = primitives.Point(x, y)
                        if domain.contains(pt):
                            self.sample_list.append(PointSample(pt))
                return True
            return False
        _params=[
            parameter.IntParameter(
                'x_points', 10,
                tip="Total number of points in the x direction in the grid."),
            parameter.IntParameter(
                'y_points', 10,
                tip="Total number of points in the y direction in the grid.")]

    else:                       # 3D
        def __init__(self, x_points, y_points, z_points, **kwargs):
            self.x_points = x_points
            self.y_points = y_points
            self.z_points = z_points
            DiscreteSampleSet.__init__(self, **kwargs)
        def make_samples(self, domain):
            self.sample_list = []
            box = domain.get_bounds()
            if box and not box.empty():
                bxmin = box.xmin()
                bymin = box.ymin()
                bzmin = box.zmin()
                if self.x_points > 1:
                    dx = float(box.xmax()-bxmin)/float(self.x_points-1)
                else:
                    dx = 0
                if self.y_points > 1:
                    dy = float(box.ymax()-bymin)/float(self.y_points-1)
                else:
                    dy = 0
                if self.z_points > 1:
                    dz = float(box.zmax()-bzmin)/float(self.z_points-1)
                else:
                    dz = 0
                for k in range(self.z_points):
                    z = bzmin + k*dz
                    for j in range(self.y_points):
                        y = bymin + j*dy
                        for i in range(self.x_points):
                            x = bxmin + i*dx
                            pt = primitives.Point(x, y, z)
                            if domain.contains(pt):
                                self.sample_list.append(PointSample(pt))
                return True
            return False
        _params=[
            parameter.IntParameter(
                'x_points', 10,
                tip="Total number of points in the x direction in the grid."),
            parameter.IntParameter(
                'y_points', 10,
                tip="Total number of points in the y direction in the grid."),
            parameter.IntParameter(
                'z_points', 10,
                tip="Total number of points in the z direction in the grid.")]

DiscreteSampleSetRegistration(
    "Grid Points",
    GridSampleSet,
    20,
    params=GridSampleSet._params,
    tip="Evaluate data on a rectangular grid of points.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/gridsampleset.xml')
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SpacedGridSampleSet(GridSampleSetBase):
    columnNames = coordNames
    if config.dimension() == 2:
        def __init__(self, delta_x, delta_y, **kwargs):
            self.delta_x = delta_x
            self.delta_y = delta_y
            GridSampleSetBase.__init__(self, **kwargs)
        def make_samples(self, domain):
            self.sample_list = []
            box = domain.get_bounds()
            if box and not box.empty():
                bxmin = box.xmin()
                bymin = box.ymin()
                bxmax = box.xmax()
                bymax = box.ymax()
                x = bxmin
                y = bymin
                while True:
                    pt = primitives.Point(x, y)
                    if domain.contains(pt):
                        self.sample_list.append(PointSample(pt))
                    x += self.delta_x
                    if x > bxmax:
                        x = bxmin
                        y += self.delta_y
                        if y > bymax:
                            return True
            return False
        _params = [
            parameter.FloatParameter(
                'delta_x', 0.1, tip="Horizontal spacing between grid points."),
            parameter.FloatParameter(
                'delta_y', 0.1, tip="Vertical spacing between grid points.")
        ]
    else:                       # 3D
        def __init__(self, delta_x, delta_y, delta_z, **kwargs):
            self.delta_x = delta_x
            self.delta_y = delta_y
            self.delta_z = delta_z
            assert self.delta_x > 0
            assert self.delta_y > 0
            assert self.delta_z > 0
            GridSampleSetBase.__init__(self, **kwargs)
        def make_samples(self, domain):
            self.sample_list = []
            box = domain.get_bounds()
            if box and not box.empty():
                bxmin = box.xmin()
                bymin = box.ymin()
                bxmax = box.xmax()
                bymax = box.ymax()
                bzmin = box.zmin()
                bzmax = box.zmax()
                x = bxmin
                y = bymin
                z = bzmin
                while True:
                    pt = primitives.Point(x, y, z)
                    if domain.contains(pt):
                        self.sample_list.append(PointSample(pt))
                    x += self.delta_x
                    if x > bxmax:
                        x = bxmin
                        y += self.delta_y
                        if y > bymax:
                            y = bymin
                            z += self.delta_z
                            if z > bzmax:
                                return True
            return False
        _params = [
            parameter.FloatParameter(
                'delta_x', 0.1, tip="X spacing between grid points."),
            parameter.FloatParameter(
                'delta_y', 0.1, tip="Y spacing between grid points."),
            parameter.FloatParameter(
                'delta_z', 0.1, tip="Z spacing between grid points.")
        ]

DiscreteSampleSetRegistration(
    "Spaced Grid Points",
    SpacedGridSampleSet,
    21,
    params=SpacedGridSampleSet._params,
    tip="Evaluate data on rectangular grid of points.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/spacedgridsampleset.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PixelSampleSet(DiscreteSampleSet):
    if config.dimension() == 2:
        columnNames = ["Pixel"] + coordNames
    else:
        columnNames = ["Voxel"] + coordNames
    def make_samples(self, domain):
        size = domain.ms.sizeOfPixels()
        # class PxlSmplFactory(object):
        #     def __init__(self, pxlsize):
        #         self.pxlsize = pxlsize
        #     def __call__(self, pxl):
        #         return PixelSample(pxl, self.pxlsize)
        # factory = PxlSmplFactory(size)
        # self.sample_list = utils.MappedIterable(factory, domain.get_pixels())
        pxls = domain.get_pixels()
        if pxls:
            self.sample_list = utils.MappedIterable(
                lambda x: PixelSample(x, size), domain.get_pixels())
            return True
        else:
            return False
        # self.sample_list = [PixelSample(x, size) for x in domain.get_pixels()]
        # return len(self.sample_list) > 0

DiscreteSampleSetRegistration(
    "Pixels" if config.dimension == 2 else "Voxels",
    PixelSampleSet,
    50,
    tip= ("Evaluate data at the centers of %s." % 
          ("pixels" if config.dimension()==2 else "voxels")),
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/pixelsampleset.xml')
)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class LinearGridSampleSetBase(DiscreteSampleSet):
    columnNames = coordNames + ["Index", "Distance", "Fraction"]

class LinearGridSampleSet(LinearGridSampleSetBase):
    def __init__(self, npts, **kwargs):
        self.npts = npts
        LinearGridSampleSetBase.__init__(self, **kwargs)
    def make_samples(self, domain):
        start, finish = domain.get_endpoints()
        npts = self.npts if self.npts > 1 else 2
        delta = (finish - start)/(npts - 1)
        lendel = math.sqrt(delta*delta)
        length = math.sqrt((finish-start)**2)
        self.sample_list = [PointOnALineSample(start + i*delta, i, i*lendel,
                                               length)
                            for i in range(npts)]
        return len(self.sample_list) > 0

DiscreteSampleSetRegistration(
    "Linear Points",
    LinearGridSampleSet,
    60,
    params=[
        parameter.IntParameter("npts", 10, "Number of points on the line.")],
    tip="Evaluate data at a given number of evenly spaced points on a line.")
    
class SpacedLinearGridSampleSet(LinearGridSampleSetBase):
    def __init__(self, delta, **kwargs):
        self.delta = delta
        LinearGridSampleSetBase.__init__(self, **kwargs)
    def make_samples(self, domain):
        start, finish = domain.get_endpoints()
        diff = finish - start
        length = math.sqrt(diff*diff)
        unitvec = diff/length
        npts = int(math.floor(length/self.delta)) + 1
        length = math.sqrt(diff*diff)
        self.sample_list = [PointOnALineSample(start + (i*self.delta)*unitvec,
                                               i, i*self.delta, length)
                            for i in range(npts)]
        return len(self.sample_list) > 0

DiscreteSampleSetRegistration(
    "Spaced Linear Points",
    SpacedLinearGridSampleSet,
    61,
    params=[
        parameter.FloatParameter(
            "delta", 0.1, "Distance between points on the line.")],
    tip="Evaluate data at a given spacing on a line.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PointSampleSet(DiscreteSampleSet):
    columnNames = coordNames
    def make_samples(self, domain):
        self.sample_list = [PointSample(pt) for pt in domain.get_points()]
        return len(self.sample_list) > 0

DiscreteSampleSetRegistration(
    "Discrete Points",
    PointSampleSet,
    ordering=1,
    params=[],
    tip="Evaluate data at all of the points in the domain.",
    discussion=xmlmenudump.loadFile(
        ## TODO: Class name has changed. Discussion file may need to
        ## be changed too.
        'DISCUSSIONS/engine/reg/discreteptsampleset.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# A ContinuumSampleSet is a set of 1D, 2D, or 3D Elements or
# ElementLites.  The AnalysisDomain constructs the elements.  Because
# all Elements have a generic method of doing integrals, we don't need
# subclasses of ContinuumSampleSet.

class ContinuumSample(Sample):
    def __init__(self, element):
        self.element = element
    def integrate(self, domain, output, order, exponents, integrals):
        femesh = domain.meshctxt.getObject()
        gauss_pts = self.element.integration_points(order)
        wgts = [x.weight() for x in gauss_pts]
        oval = output.instancefn(output)
        zero = oval.zero()      # Zero in the appropriate OutvalVal type 
        assert zero.thisown
        if 0 in exponents:
            one = oval.one()    # One in the appropriate OutvalVal type
            assert one.thisown
            intgrl = reduce(lambda x,y: x+y, wgts)*one
            integrals[0] = integrals.get(0, zero) + intgrl

        ## TODO: Special handling for exponent=1 too.
        remainingexponents = [x for x in exponents if x != 0]
        if remainingexponents:
            pts = [x.mastercoord() for x in gauss_pts]
            vals = output.evaluate(femesh, domain, [self.element], [pts])
            for power in remainingexponents:
                # OutputVal.__pow__ computes powers of each component
                # for multicomponent OutputVals.  It's not a dot
                # product or any other fancy tensor operation.
                integrals[power] = (integrals.get(power, zero) +
                                    reduce(lambda x,y: x+y[0]*(y[1]**power),
                                           zip(wgts, vals), zero))
                                       
class ContinuumSampleSet(SampleSet):
    def __init__(self, order):
        self.order = order
    def make_samples(self, domain):
        self.sample_list = []
        els = domain.get_elements() 
        ## Setting sample_list to a MappedIterable here allows us to
        ## avoid making a list of ContinuumSamples, which may be a bad
        ## idea if the SampleSet is very large.  However, we should
        ## check to see which method is actually faster.
        self.sample_list = utils.MappedIterable(ContinuumSample, els)
        ## See the TODO in analysisdomain.py about size(). Because els
        ## may be an iterator, we don't know whether or not the domain
        ## is empty here, so we have to assume that it's not, and
        ## always return True.
        return True
        ## This is what to do if not using the generator.
        # ok = False
        # for element in els:
        #     self.sample_list.append(ContinuumSample(element))
        #     ok = True
        # return ok

    def integrateWithExponents(self, domain, output, exponents):
        if self.order == automatic.automatic:
            order = 2           # TODO: Do something cleverer here.
        else:
            order = self.order
        integrals = {}
        n = 0
        for sample in self.sample_list:
            n += 1
            sample.integrate(domain, output, order, exponents, integrals)
        if n == 0:
            raise ooferror.ErrUserError("Vanishing integration range.")
        return integrals

    def integrate(self, domain, output):
        intgrls = self.integrateWithExponents(domain, output, (1,))
        return intgrls[1]

SampleSetRegistration(
    "Integrate",
    ContinuumSampleSet,
    ordering=1,
    params=[
        parameter.AutoIntParameter(
            "order", automatic.automatic,
            tip="Set the order of integration to use.")],
    direct=False,
    tip="Data will be integrated over volumes, areas, or lines.")


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SamplingParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.RegisteredParameter.__init__(self, name, reg=SampleSet,
                                               default=default, tip=tip,
                                               auxData=auxData)

