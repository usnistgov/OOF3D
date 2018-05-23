# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# Parameter classes for primitives.Point and primitives.iPoint.  These
# classes were moved out of primitives.py to avoid an import loop.
# primitives.py and coord.py were importing each other so that
# PointParameter and CoordParameter could each accept the 'wrong'
# class in assignments.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import coord
from ooflib.common import primitives
from ooflib.common.IO import parameter
import struct
import types

class PointParameter(parameter.Parameter):
    types = (primitives.Point, coord.CoordPtr) # allow assignment from Coord too

    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        if value is None:
            value = primitives.origin()
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    structfmt = '>' + 'd'*config.dimension()
    structlen = struct.calcsize(structfmt)

    def binaryRepr(self, datafile, value):
        return struct.pack(PointParameter.structfmt, *value.asTuple())

    def binaryRead(self, parser):
        b = parser.getBytes(PointParameter.structlen)
        vals = struct.unpack(PointParameter.structfmt, b)
        return primitives.Point(*vals)

    def valueDesc(self):
        return "A <link linkend='Object:Point'><classname>Point</classname></link> object (eg, <userinput>Point(1.1, 2.0)</userinput>)."

class ListOfPointsParameter(parameter.Parameter):

    def __init__(self, name, value=None, default=[], tip=None):
        parameter.Parameter.__init__(self, name, value, default, tip)

    def checker(self, x):
        if type(x) is not types.ListType:
            parameter.raiseTypeError(type(x), "list of Points")
        for y in x:
            if not isinstance(y, primitives.Point):
                parameter.raiseTypeError("list of %s" % type(y),
                                         "list of Points")
    def valueDesc(self):
        return "A list of <link linkend='Object:Point'><classname>Point</classname></link> objects."


class iPointParameter(parameter.Parameter):
    types = (primitives.iPoint,)
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        if value is None:
            value = primitives.iOrigin()
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    structfmt = '>' + 'i'*config.dimension()
    structlen = struct.calcsize(structfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(iPointParameter.structfmt, *value.asTuple())
    def binaryRead(self, parser):
        b = parser.getBytes(iPointParameter.structlen)
        vals = struct.unpack(iPointParameter.structfmt, b)
        return primitives.iPoint(*vals)
    def valueDesc(self):
        return "An <link linkend='Object:iPoint'><classname>iPoint</classname></link> (integer Point) object (eg <userinput>iPoint(1,2)</userinput>)."


