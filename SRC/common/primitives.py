# -*- python -*-
# $RCSfile: primitives.py,v $
# $Revision: 1.50.10.17 $
# $Author: langer $
# $Date: 2014/09/15 19:53:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Classes representing primitive graphics objects.  Each class should
## have an enclosing_rectangle() function which returns a Rectangle.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import utils
from ooflib.common.IO import parameter
import math
import struct
import types

## TODO OPT: It would be better to have two separate classes, Point2
## and Point3, and set Point to Point2 or Point3 according to the
## value of config.dimension.  That would reduce the number of "if"s.

class Point(object):
    # Point class represents a point in 2 or 3 dimensions.  It is more
    # or less redundant with coord.Coord, but doesn't have the
    # overhead of calling C++ routines for simple operations.  Python
    # graphics routines should generally be prepared to receive either
    # Point or coord.Coord.

    def __init__(self, x, y, z=0.):
        # This should possibly coerce x and y to floats, since other
        # routines might want to take their ratio.  This *isn't* done
        # here, because it might be slow.
        self.x = x
        self.y = y
        if config.dimension() == 3:
            self.z = z
            
    def __getitem__(self, idx):
        if idx==0: return self.x
        if idx==1: return self.y
        if config.dimension() == 3 and idx==2: return self.z
        raise IndexError
    
    def __setitem__(self, idx, val):
        if idx==0:
            self.x = val
        elif idx==1:
            self.y = val
        elif config.dimension() == 3 and idx==2:
            self.z = val
        else:
            raise IndexError

    def __len__(self):
        return config.dimension()

    def asTuple(self):
        return tuple(self[i] for i in range(config.dimension()))

    if config.dimension() == 2:
        def enclosing_rectangle(self):
            return Rectangle(self, self)
        def clone(self):
            return self.__class__(self.x, self.y)
        def scale(self, factors):
            return self.__class__(self.x*factors[0], self.y*factors[1])
    elif config.dimension() == 3:
        def enclosing_rectangle(self):
            return RectangularPrism(self, self)
        def clone(self):
            return self.__class__(self.x, self.y, self.z)
        def scale(self, factors):
            return self.__class__(self.x*factors[0], self.y*factors[1],
                                  self.z*factors[2])

    # Multiply accepts mixed point/ipoint objects for dot products,
    # and preserves i-ness if possible.
    if config.dimension() == 2:
        def __mul__(self, other):
            if (isinstance(other, self.__class__) or 
                isinstance(self, other.__class__)):
                return self.x*other.x+self.y*other.y
            elif type(other)==types.FloatType:
                return Point(other*self.x, other*self.y)
            elif type(other)==types.IntType:
                # Return whatever class you already are.
                return self.__class__(other*self.x, other*self.y)
            raise TypeError("Invalid arguments.")
    else:
        def __mul__(self, other):
            if (isinstance(other, self.__class__) or 
                isinstance(self, other.__class__)):
                return self.x*other.x+self.y*other.y+self.z*other.z
            elif type(other)==types.FloatType:
                return Point(other*self.x, other*self.y, other*self.z)
            elif type(other)==types.IntType:
                # Return whatever class you already are.
                return self.__class__(other*self.x, other*self.y, other*self.z)
            raise TypeError("Invalid arguments.")

    if config.dimension() == 2:
        def cross(self, other):
            # Use [0] instead of .x so that this will work with Coords too.
            return self.x*other[1] - self.y*other[0]
    else:
        def cross(self, other):
            return Point(self.y*other[2]-self.z*other[1],
                         self.z*other[0]-self.x*other[2],
                         self.x*other[1]-self.y*other[0])

    if config.dimension() == 2:
        def dot(self, other):
            return self.x*other[0] + self.y*other[1]
    else:
        def dot(self, other):
            return self.x*other[0] + self.y*other[1] + self.z*other[2]

    # Power defined only for squaring -- finds the squared magnitude.
    def __pow__(self, other):
        if other!=2:
            raise ooferror.ErrPyProgrammingError(
                "Power operation only defined for exponent equal to 2.")
        if config.dimension() == 2:
            return self.x*self.x+self.y*self.y
        elif config.dimension() == 3:
            return self.x*self.x+self.y*self.y+self.z*self.z

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        # other may not be a Point, so used [0] instead of .x
        if config.dimension() == 2:
            return self.__class__(self.x + other[0], self.y + other[1])
        elif config.dimension() == 3:
            return self.__class__(self.x + other[0], self.y + other[1],
                                  self.z + other[2])

    def __sub__(self, other):
        if config.dimension() == 2:
            return self.__class__(self.x - other[0], self.y - other[1])
        elif config.dimension() == 3:
            return self.__class__(self.x - other[0], self.y - other[1],
                                  self.z - other[2])  
    def __rsub__(self, other):
        return -1*self.__sub__(other)

    def __neg__(self):
        if config.dimension() == 2:
            return self.__class__(-self.x, -self.y)
        elif config.dimension() == 3:
            return self.__class__(-self.x, -self.y, -self.z)

    def __div__(self, other):
        if config.dimension() == 2:
            return Point(self.x/other, self.y/other)
        elif config.dimension() == 3:
            return Point(self.x/other, self.y/other, self.z/other)

    def __hash__(self):
        # Comparison operators are written in terms of __getitem__ so that
        # comparison to Coords and ICoords will work.
        if config.dimension() == 2:
            return hash(self.x) & hash(self.y)
        elif config.dimension() == 3:
            return hash(self.x) & hash(self.y) & hash(self.z)

    def __cmp__(self, other):
        try:
            if self[0] < other[0]: return -1
            if self[0] > other[0]: return 1
            if self[1] < other[1]: return -1
            if self[1] > other[1]: return 1
            if config.dimension() == 3:
                if self[2] < other[2]: return -1
                if self[2] > other[2]: return 1
            return 0
        except:
            return 1

    def __lt__(self, other):
        try:
            if self[0] < other[0]: return 1
            if self[0] > other[0]: return 0
            if self[1] < other[1]: return 1
            if self[1] > other[1]: return 0
            if config.dimension() == 3:
                if self[2] < other[2]: return 1
                if self[2] > other[2]: return 0
        except:
            return 0

    def __gt__(self, other):
        try:
            if self[0] > other[0]: return 1
            if self[0] < other[0]: return 0
            if self[1] > other[1]: return 1
            if self[1] < other[1]: return 0
            if config.dimension() == 3:
                if self[2] > other[2]: return 1
                if self[2] < other[2]: return 0
        except:
            return 1

    def __eq__(self, other):
        try:
            if config.dimension() == 2:
                return self[0]==other[0] and self[1]==other[1]
            if config.dimension() == 3:
                return (self[0]==other[0] and self[1]==other[1] and
                        self[2]==other[2])
        except:
            return 0

    def __ne__(self, other):
        try:
            if config.dimension() == 2:
                return self[0]!=other[0] or self[1]!=other[1]
            if config.dimension() == 3:
                return (self[0]!=other[0] or self[1]!=other[1] or
                        self[2]!=other[2])
        except:
            return 1

    def __repr__(self):
        fmt = ",".join(("%g",)*config.dimension())
        return "Point(" + fmt%self.asTuple() + ")"
    
# end Point
utils.OOFdefine('Point', Point)

class iPoint(Point):
    "A Point made up of integers. Arithmetic may convert it to a regular Point."
    # Should probably not be derived from Point, for efficiency and so
    # that arithmetic operators don't convert iPoints to Points.
    def __init__(self, x, y, z=0):
        if config.dimension() == 2:
            Point.__init__(self, int(math.floor(x)), int(math.floor(y)))
        elif config.dimension() == 3:
            Point.__init__(self, int(math.floor(x)), int(math.floor(y)),
                           int(math.floor(z)))
    def __repr__(self):
        fmt = ",".join(("%d",)*config.dimension()) 
        return "iPoint(" + fmt%self.asTuple() + ")"

utils.OOFdefine('iPoint', iPoint)

# origin and iOrigin are defined as functions instead of just
# variables so that we're not tempted to do this:
#   sum = origin
#   for x in points:
#     sum += x
# which would (might?) change the value of origin.  I'm not sure of
# the semantics of +=.  The manual says that it changes objects in
# place if possible, but doesn't say when it's possible.

if config.dimension() == 2:
    def origin():
        return Point(0., 0)
    def iOrigin():
        return iPoint(0, 0)
else:
    def origin():
        return Point(0., 0., 0.)
    def iOrigin():
        return iPoint(0, 0, 0)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class PointParameter(parameter.Parameter):
    types = (Point,)

    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        if value is None:
            value = origin()
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    structfmt = '>' + 'd'*config.dimension()
    structlen = struct.calcsize(structfmt)

    def binaryRepr(self, datafile, value):
        return struct.pack(PointParameter.structfmt, *value.asTuple())

    def binaryRead(self, parser):
        b = parser.getBytes(PointParameter.structlen)
        vals = struct.unpack(PointParameter.structfmt, b)
        return Point(*vals)

    def valueDesc(self):
        return "A <link linkend='Object:Point'><classname>Point</classname></link> object (eg, <userinput>Point(1.1, 2.0)</userinput>)."

class ListOfPointsParameter(parameter.Parameter):

    def __init__(self, name, value=None, default=[], tip=None):
        parameter.Parameter.__init__(self, name, value, default, tip)

    def checker(self, x):
        if type(x) is not types.ListType:
            parameter.raiseTypeError(type(x), "list of Points")
        for y in x:
            if not isinstance(y, Point):
                parameter.raiseTypeError("list of %s" % type(y),
                                         "list of Points")
    def valueDesc(self):
        return "A list of <link linkend='Object:Point'><classname>Point</classname></link> objects."


class iPointParameter(parameter.Parameter):
    types = (iPoint,)
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        if value is None:
            value = iOrigin()
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    structfmt = '>' + 'i'*config.dimension()
    structlen = struct.calcsize(structfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(iPointParameter.structfmt, *value.asTuple())
    def binaryRead(self, parser):
        b = parser.getBytes(iPointParameter.structlen)
        vals = struct.unpack(iPointParameter.structfmt, b)
        return iPoint(*vals)
    def valueDesc(self):
        return "An <link linkend='Object:iPoint'><classname>iPoint</classname></link> (integer Point) object (eg <userinput>iPoint(1,2)</userinput>)."


def pontify(ptlist):
    # Convert a Thing of Stuff to a Thing of Points.  Thing is
    # probably Curve or Polygon, and Stuff is probably MasterCoord or
    # Coord, but it doeesn't really matter.  Points can be faster to
    # use since they don't have any swig overhead.
    if config.dimension() == 2:
        if type(ptlist) == types.ListType:
            return [Point(pt[0], pt[1]) for pt in ptlist]
        return ptlist.__class__([Point(pt[0], pt[1]) for pt in ptlist])
    elif config.dimension() == 3:
        if type(ptlist) == types.ListType:
            return [Point(pt[0], pt[1], pt[2]) for pt in ptlist]
        return ptlist.__class__([Point(pt[0], pt[1], pt[2]) for pt in ptlist])

## Documentation for Point and iPoint classes

from ooflib.common.IO import xmlmenudump
xmlmenudump.XMLObjectDoc(
    'iPoint',
    xmlmenudump.loadFile('DISCUSSIONS/common/object/ipoint.xml'))

xmlmenudump.XMLObjectDoc(
    'Point',
    xmlmenudump.loadFile('DISCUSSIONS/common/object/point.xml'))


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Rectangle(object):
    # A Rectangle is a pair of points at diagonally opposite corners.
    def __init__(self, pt0, pt1):
        # Don't assume that args pt0 and pt1 have .x and .y data
        self.lowleft = Point(min(pt0[0], pt1[0]), min(pt0[1], pt1[1]))
        self.upright = Point(max(pt0[0], pt1[0]), max(pt0[1], pt1[1]))
    def enclosing_rectangle(self):
        return self
    def xmin(self):
        return self.lowleft.x
    def xmax(self):
        return self.upright.x
    def ymin(self):
        return self.lowleft.y
    def ymax(self):
        return self.upright.y
    def lowerleft(self):
        return self.lowleft
    def upperright(self):
        return self.upright
    def swallow(self, obj):
        """
        Expand a Rectangle to include the given obj.  The obj must have
        an enclosing_rectangle() function.
        """
        try:
            encl = obj.enclosing_rectangle()
        except AttributeError:
            print obj
            raise
        self.lowleft.x = min(self.lowleft.x, encl.xmin())
        self.lowleft.y = min(self.lowleft.y, encl.ymin())
        self.upright.x = max(self.upright.x, encl.xmax())
        self.upright.y = max(self.upright.y, encl.ymax())
    def area(self):
        return (self.xmax()-self.xmin())*(self.ymax()-self.ymin())
    def __repr__(self):
        return "Rectangle(%s,%s)" % (`self.lowleft`, `self.upright`)

utils.OOFdefine('Rectangle', Rectangle)

class iRectangle(Rectangle):
    def __init__(self, pt0, pt1):
        self.lowleft = iPoint(min(pt0[0], pt1[0]), min(pt0[1], pt1[1]))
        self.upright = iPoint(max(pt0[0], pt1[0]), max(pt0[1], pt1[1]))
    def points(self):
        return [iPoint(i,j)
                for i in range(self.lowleft.x, self.upright.x)
                for j in range(self.lowleft.y, self.upright.y)]
    def inclusivePoints(self):
        return [iPoint(i,j)
                for i in range(self.lowleft.x, self.upright.x+1)
                for j in range(self.lowleft.y, self.upright.y+1)]

utils.OOFdefine('iRectangle', Rectangle)

# new classes for 3D - or we could generalize the classes above, but
# the terminology would be confusing
class RectangularPrism:
    # A Rectangular is a pair of 3D points at diagonally opposite corners.
    def __init__(self, pt0, pt1):
        # Don't assume that args pt0 and pt1 have .x and .y data
        self.lowleftback = Point(min(pt0[0], pt1[0]), min(pt0[1], pt1[1]),
                                 min(pt0[2],pt1[2]))
        self.uprightfront = Point(max(pt0[0], pt1[0]), max(pt0[1], pt1[1]),
                                  max(pt0[2],pt1[2]))
    def enclosing_rectangle(self):
        return self
    def xmin(self):
        return self.lowleftback.x
    def xmax(self):
        return self.uprightfront.x
    def ymin(self):
        return self.lowleftback.y
    def ymax(self):
        return self.uprightfront.y
    def zmin(self):
        return self.lowleftback.z
    def zmax(self):
        return self.uprightfront.z
    def lowerleftback(self):
        return self.lowleftback
    def upperrightfront(self):
        return self.uprightfront
    def swallow(self, obj):
        """
        Expand a Rectangle to include the given obj.  The obj must have
        an enclosing_rectangle() function.
        """
        try:
            encl = obj.enclosing_rectangle()
        except AttributeError:
            print obj
            raise
        self.lowleftback.x = min(self.lowleftback.x, encl.xmin())
        self.lowleftback.y = min(self.lowleftback.y, encl.ymin())
        self.lowleftback.z = min(self.lowleftback.z, encl.zmin())
        self.uprightfront.x = max(self.uprightfront.x, encl.xmax())
        self.uprightfront.y = max(self.uprightfront.y, encl.ymax())
        self.uprightfront.z = max(self.uprightfront.z, encl.zmax())
    def volume(self):
        return ((self.xmax()-self.xmin())*(self.ymax()-self.ymin())*
                (self.zmax()-self.zmin()))
    def empty(self):
        return self.lowleftback == self.uprightfront
    def __repr__(self):
        return "RectangularPrism(%s,%s)" % (`self.lowleftback`,
                                            `self.uprightfront`)

utils.OOFdefine('RectangularPrism', RectangularPrism)

class iRectangularPrism(RectangularPrism):
    def __init__(self, pt0, pt1):
        self.lowleftback = iPoint(min(pt0[0], pt1[0]), min(pt0[1], pt1[1]),
                                  min(pt0[2],pt1[2]))
        self.uprightfront = iPoint(max(pt0[0], pt1[0]), max(pt0[1], pt1[1]),
                                   max(pt0[2],pt1[2]))
    def points(self):
        return [iPoint(i,j,k)
                for i in range(self.lowleftback.x, self.uprightfront.x)
                for j in range(self.lowleftback.y, self.uprightfront.y)
                for k in range(self.lowleftback.z, self.uprightfront.z)]
    def inclusivePoints(self):
        return [iPoint(i,j,k)
                for i in range(self.lowleftback.x, self.uprightfront.x+1)
                for j in range(self.lowleftback.y, self.uprightfront.y+1)
                for k in range(self.lowleftback.z, self.uprightfront.z+1)]

utils.OOFdefine('iRectangularPrism', RectangularPrism)

#################################

if config.dimension() == 2:
    def rectangleFactory(p0, p1):
        return Rectangle(p0, p1)
    def iRectangleFactory(p0, pi):
        return iRectangle(p0, p1)
else:
    def rectangleFactory(p0, p1):
        return RectangularPrism(p0, p1)
    def iRectangleFactory(p0, p1):
        return iRectangularPrism(p0, p1)

#################################

# Utility function for finding intersections between the segment
# p1->p2 and the segment p3->p4 in 2D.

## TODO 3.1: Move this to C++?  It looks like a lot of arithmetic for Python.
def _point_intersect2D(p1, p2, p3, p4):
    # Check endpoints explicitly first.  If we didn't do this here,
    # then intersections that were supposed to be exactly at endpoints
    # might not be (due to roundoff error) and checks for endpoint
    # intersections (such as in Polygon.intersections) might fail.
    if p1 == p3 or p1 == p4:
        return p1
    if p2 == p3 or p2 == p4:
        return p2

    # Guard against argument-order-induced round-off inconsistencies
    # by putting the arguments in standard order.
    if p1>p2:
        t=p1
        p1=p2
        p2=t

    if p3>p4:
        t=p3
        p3=p4
        p4=t
        
    x1 = p1.x;  y1 = p1.y
    x2 = p2.x;  y2 = p2.y
    x3 = p3.x;  y3 = p3.y
    x4 = p4.x;  y4 = p4.y

    denom = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
    if denom==0.0: return None # Lines are parallel.

    # Check for existence of an intersection -- this is necessary
    # because end-point-to-interior intersections can be missed due to
    # round-off if you do a bounds-check on the intersection point
    # after it has been computed.

    # Are p1 and p2 on the same side of p3->p4?  They are if the
    # cross-product has the same sign.
    c1 = (p4-p3).cross(p1-p3)
    c2 = (p4-p3).cross(p2-p3)
    p34mag = (p4-p3)**2
    
    if c1*c2 > 0:
        return None

    # Explicitly check the cross-product-is-zero "tee" case, which
    # otherwise is subject to roundoff in the generic point-finder.
    
    if c1==0: # p1 lies on p3->p4, do bounds check.
        f = ((p1-p3)*(p4-p3))/p34mag
        if (f>0) and (f<1):
            return p1

    if c2==0: # p2 lies on p3->p4.
        f = ((p2-p3)*(p4-p3))/p34mag
        if (f>0) and (f<1):
            return p2
        
        
    # Are p3 and p4 on the same side of p1->p2?
    c3 = (p2-p1).cross(p3-p1)
    c4 = (p2-p1).cross(p4-p1)
    p12mag = (p2-p1)**2

    if c3*c4 > 0:
        return None

    # Check "tee" case.
    
    if c3==0: # p3 lies on p1->p2.
        f = ((p3-p1)*(p2-p1))/p12mag
        if (f>0) and (f<1):
            return p3

    if c4==0: # p4 lies on p1->p2
        f = ((p4-p1)*(p2-p1))/p12mag
        if (f>0) and (f<1):
            return p4

    # Intersection is generic.  Find it.
    ua_nu = (x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)
    ua = ua_nu/denom
    return p1 + ua*(p2-p1)


class SegmentBase(object):
    # A Segment is a directed pair of points.
    def __init__(self, end1, end2):
        self.startpt = end1
        self.endpt = end2
    def start(self):
        return self.startpt
    def end(self):
        return self.endpt
    def __cmp__(self, other):
        try:
            if self.startpt < other.startpt: return -1
            if self.startpt > other.startpt: return 1
            if self.endpt < other.endpt: return -1
            if self.endpt > other.endpt: return 1
            return 0
        except AttributeError:
            return 1
    def __lt__(self, other):
        try:
            if self.startpt < other.startpt: return 1
            if self.startpt > other.startpt: return 0
            if self.endpt < other.endpt: return 1
            return 0
        except AttributeError:
            return 0
    def __gt__(self, other):
        try:
            if self.startpt > other.startpt: return 1
            if self.startpt < other.startpt: return 0
            if self.endpt > other.endpt: return 1
            return 0
        except AttributeError:
            return 0
    def __eq__(self, other):
        try:
            return self.startpt == other.startpt and self.endpt == other.endpt
        except AttributeError:
            return 0
    def __ne__(self, other):
        try:
            return self.startpt != other.startpt or self.endpt != other.endpt
        except AttributeError:
            return 1
    
    def __hash__(self):
        return hash(self.startpt) & hash(self.endpt)

    def __repr__(self):
        return "Segment(%s, %s)" % (`self.startpt`, `self.endpt`)

if config.dimension() == 2:
    class Segment(SegmentBase):
        def intersection(self, other):
            return _point_intersect2D(self.startpt, self.endpt,
                                        other.startpt, other.endpt)
        def enclosing_rectangle(self):
            return Rectangle(self.startpt, self.endpt)
else:                           # 3D
    class Segment(SegmentBase):
        def enclosing_rectangle(self):
            return RectangularPrism(self.startpt, self.endpt)

        
utils.OOFdefine('Segment', Segment)

######################

class CurveBase(object):
    # Base class for 2D Curves and 3D SpaceCurves.  Both are directed
    # lists of points.
    def __init__(self, ptlist):
        if type(ptlist) == type(()) or type(ptlist) == types.GeneratorType:
            self.pts = list(ptlist)
        elif isinstance(ptlist, CurveBase):
            self.pts = ptlist.pts
        else:
            self.pts = ptlist
    def points(self):
        return self.pts
    def append(self, pt):
        self.pts.append(pt)
    def prepend(self, pt):
        self.pts = [pt] + self.pts
    def join(self, curve):
        self.pts += curve.pts
    def join_front(self, curve):
        self.pts = curve.pts + self.pts
    def __len__(self):
        # The length of a curve is the number of points it contains,
        # not the number of segments!
        return len(self.pts)
    def __getitem__(self, idx):
        return self.pts[idx]
    def __setitem__(self, idx, val):
        self.pts[idx] = val
    def __getslice__(self, i, j):
        return self.__class__(self.pts[i:j])

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, `self.pts`)

    class CurveEdges:
        # Aux class used when viewing a Curve as a list of Segments.
        def __init__(self, curve):
            self.curve = curve
        def __getitem__(self, idx):
            return Segment(self.curve.pts[idx], self.curve.pts[idx+1])
        def __len__(self):
            return len(self.curve.pts)-1
    def edges(self):
        return Curve.CurveEdges(self)

if config.dimension() == 2:
    class Curve(CurveBase):
        def enclosing_rectangle(self):
            xmin = self.pts[0][0]
            xmax = xmin
            ymax = self.pts[0][1]
            ymin = ymax
            for pt in self.pts:
                xmin = min(xmin, pt[0])
                xmax = max(xmax, pt[0])
                ymin = min(ymin, pt[1])
                ymax = max(ymax, pt[1])
            return Rectangle(Point(xmin, ymin), Point(xmax, ymax))
    ## The above function could be written like this, but it would probably be
    ## substantially slower, since swallow(obj) converts obj to a Rectangle:
    ##    def enclosing_rectangle(self):
    ##        rect = self.pts[0].enclosing_rectangle()
    ##        for pt in self.pts[1:]:
    ##            rect.swallow(pt)
    ##        return rect
    
    #utils.OOFdefine('Curve', Curve)  ## TODO OPT: Is this needed?

else: # 3D
    class SpaceCurve(CurveBase):
        def enclosing_rectangle(self):
            mins = Point(*pts[0].asTuple()) # make a copy
            maxs = Point(*pts[0].asTuple())
            for pt in self.pts:
                for i in range(config.dimension()):
                    mins[i] = min(mins[i], pt[i])
                    maxs[i] = max(maxs[i], pt[i])
            return RectangularPrism(mins, maxs)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

if config.dimension() == 3:

    class PlaneOrientation(enum.EnumClass(
            ("FRONT", "The side in the direction of the positive normal."),
            ("BACK", "The side in the direction of the negative normal."))):
        pass

    recto = PlaneOrientation("FRONT")
    verso = PlaneOrientation("BACK")

    class Plane(object):
        def __init__(self, normal, offset):
            self.normalDirection = normal # a Direction
            self.offset = offset
        def segmentIntersect(self, pointA, pointB):
            # Returns None if the segment defined by (pointA, pointB)
            # does not intersect the plane.  Returns a tuple of one or
            # two intersection points otherwise: if both points are in
            # the plane, both are returned.  Otherwise a single
            # interpolating point is returned.
            # Used only by Element.intersectPlane in element.spy
            dotA = self.normalDirection.dot(pointA)
            dotB = self.normalDirection.dot(pointB)
            if ((dotA < self.offset and dotB < self.offset) or
                (dotA > self.offset and dotB > self.offset)):
                return None
            if dotA == self.offset and dotB == self.offset:
                # Both points are in the plane
                return (pointA, pointB)
            if dotA == self.offset:
                return (pointA,)
            if dotB == self.offset:
                return (pointB,)
            diff = pointA - pointB
            # Separation between A and B in the normal direction.
            # This can't be zero if we got to this point.
            proj = self.normalDirection.dot(diff)
            # Distance between the plane and B, relative to the
            # distance between A and B.
            alpha = (self.offset - dotB)/proj
            # Position of the intersection
            return (pointB + alpha*diff,)



    class OrientedPlane(Plane):
        def __init__(self, normal, offset, side=PlaneOrientation("FRONT")):
            Plane.__init__(self, normal, offset)
            self.side = side
        def sameSide(self):
            return self.side
        def otherSide(self):
            if self.side == recto:
                return verso
            return recto
        def findSide(self, point):
            if self.normalDirection.dot(point) >= self.offset:
                return self.sameSide()
            return self.otherSide()

        def polygonize(self, points):
            # Given a set of points in the plane, return them in an
            # order so that they traverse the counterclockwise
            # perimeter of a convex polygon.  There is no error
            # checking: if the points come from the intersection of
            # element edges with the plane, it's always possible to
            # form a suitable polygon.

            norm = self.normalDirection.coord()
            if self.side == "BACK":
                norm = -norm
            # ipts are the in-plane vectors from the center of mass to
            # the points.
            ipts = points[:]    # copy
            from ooflib.SWIG.common import coord
            center = origin()
            for ipt in ipts:
                center += ipt
            center /= len(ipts)
            for i in range(len(ipts)):
                ipts[i] -= center

            if len(points) == 3:
                return self._polygonize3(points, norm, ipts)
            elif len(points) == 4:
                return self._polygonize4(points, norm, ipts)
            raise ooferror.ErrPyProgrammingError(
                "Plane.polygonize() requires 3 or four points, got %d" %
                len(points))

        def _polygonize3(self, points, norm, ipts):
            # There are only two possible orderings, and only one of
            # them creates a polygon with positive area.
            for ordering in [(0,1,2), (0,2,1)]:
                area = 0.0
                for i in range(3):
                    crossprod = ipts[ordering[i]].cross(ipts[ordering[(i+1)%3]])
                    area += crossprod.dot(norm)
                if area > 0:
                    return SpaceCurve(points[i] for i in ordering)
            raise ooferror.ErrPyProgrammingError("Plane._polygonize3 failed.")
        def _polygonize4(self, points, norm, ipts):
            # The correct ordering of the points creates a polygon
            # with positive area and no contact between non-adjacent
            # edges.
            positives = []          # orderings that have positive areas
            for ordering in [(0,1,2,3), (0,1,3,2), (0,2,1,3), (0,2,3,1), 
                             (0,3,1,2), (0,3,2,1)]:
                area = 0.0
                for i in range(4):
                    crossprod = ipts[ordering[i]].cross(ipts[ordering[(i+1)%4]])
                    area += crossprod.dot(norm)
                if area > 0:
                    positives.append(ordering)
            if len(positives) == 1:
                return SpaceCurve(points[i] for i in positives[0])
            for ordering in positives:
                # Check that opposite edges don't cross.  Because the
                # polygon must be convex, it's sufficient to check
                # that the end points of one edge are on the same side
                # of the linear extension of the opposite edge.
                for i in (0,1):     # pairs of edges
                    pt0 = points[ordering[i]]
                    seg0 = points[ordering[i+1]] - pt0
                    ptA = points[ordering[i+2]] - pt0
                    ptB = points[ordering[(i+3)%4]] - pt0
                    crossA = seg0.cross(ptA).dot(norm)
                    crossB = seg0.cross(ptB).dot(norm)
                    if crossA * crossB < 0: # edges cross
                        break
                else:
                    # Neither pair of opposite edges cross.
                    return SpaceCurve(points[k] for k in ordering)
            raise ooferror.ErrPyProgrammingError(
                "Failed to find a well-formed element cross section.")

        def __repr__(self):
            return "OrientedPlane(normal=%s, offset=%g, side=%s)" \
                % (self.normalDirection, self.offset, self.side)

# end if dimension==3

######################
######################

if __name__ == '__main__':
    p1 = Point(0,0)
    p2 = Point(1,0)
    p3 = Point(1,1)
    p4 = Point(0,1)

    poly = Polygon([p1,p2,p3,p4])
    curve = Curve([p1,p2,p3,p4])
    print "Points"
    for point in poly.points():
        print point
    print "Curve Edges"
    for edge in curve.edges():
        print edge
    print "Polygon Edges"
    for edge in poly.edges():
        print edge

    print "p1=",p1
    print "poly=", poly
    print "curve=", curve
    print "curve.enclosing_rectangle=", curve.enclosing_rectangle()
        
