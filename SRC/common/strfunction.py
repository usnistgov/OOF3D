# -*- python -*-
# $RCSfile: strfunction.py,v $
# $Revision: 1.24.10.4 $
# $Author: langer $
# $Date: 2014/07/28 20:23:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import parameter
import types
import struct
import compiler
# import inspect                  # for debugging

class StrFunction:
    def __init__(self, arglist, funcstr):
        self.arglist = arglist
        self.funcstr = funcstr
        if funcstr:
            self.function = utils.OOFeval('lambda %s: %s' %
                                          (self.arglist, self.funcstr))
        else:
            self.function = None
    def __call__(self, *args):
        if self.function:
            # debug.fmsg("function args=", inspect.getargspec(self.function)[0])
            # debug.fmsg("args=", args)
            return self.function(*args)
    def string(self):
        return self.funcstr
    def __repr__(self):
        return "StrFunction('%s', '%s')" % (self.arglist, self.funcstr)
    def __str__(self):                  # used by shortrepr in FieldInit
        return "'%s'" % self.funcstr
    def __eq__(self,other):
        if other:
            if isinstance(other,StrFunction):
                if self.__class__==other.__class__:
                    if self.funcstr==other.funcstr:
                        return 1
        return 0

    # For reasons I don't quite understand, python doesn't want to
    # hash ProfileFunctions, which are derived from the StrFunction
    # class. I think it has something to do with the self.function
    # member and the fact that code objects are unhashable.  -VRC
    def __hash__(self):
        return hash((self.arglist,self.funcstr,self.__class__))

    def dependsOn(self, name):
        # Does the function actually depend on the variable 'name'?
        nodes = compiler.parse(self.funcstr).getChildNodes()
        return name in _findNames(nodes)

def _findNames(nodes):
    # Return the names of all compiler.ast.Name nodes in the given
    # Abstract Syntax Tree nodes.
    names = []
    for node in nodes:
        if isinstance(node, compiler.ast.Name):
            names.append(node.name)
        else:
            names.extend(_findNames(node.getChildNodes()))
    return names

# XYStrFunction is initialized from a string function of x,y or x,y,z,
# but it takes a single Coord or Point as its argument when it's being
# evaluated.

class XYStrFunction(StrFunction):
    def __init__(self, funcstr):
        if config.dimension() == 2:
            StrFunction.__init__(self, 'x, y', funcstr)
        elif config.dimension() == 3:
            StrFunction.__init__(self, 'x, y, z', funcstr)
    def __call__(self, coord):
        if self.function:
            return self.function(*coord) # unpacks Coord into x,y or x,y,z
    def __repr__(self):
        return "'%s'" % self.funcstr    # shorthand notation

class XYTStrFunction(StrFunction):
    def __init__(self, funcstr):
        if config.dimension() == 2:
            StrFunction.__init__(self, 'x, y, t', funcstr)
        elif config.dimension() == 3:
            StrFunction.__init__(self, 'x, y, z, t', funcstr)
    def __call__(self, coord, t):
        if self.function:
            args = tuple(coord) + (t,)
            return self.function(*args) # unpacks Coord into x,y,t or x,y,z,t
    def __repr__(self):
        return "'%s'" % self.funcstr    # shorthand notation


utils.OOFdefine('XYStrFunction', XYStrFunction)
utils.OOFdefine('XYTStrFunction', XYTStrFunction)
utils.OOFdefine('StrFunction', StrFunction)


class XYStrFunctionParameter(parameter.Parameter):
    types = (types.StringType, XYStrFunction)
    def __init__(self, name, value=None, default='0.0', tip=None, auxData={}):
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    def set(self, value):
        if type(value) is types.StringType:
            self._value = XYStrFunction(value)
        elif isinstance(value, XYStrFunction):
            self._value = value
        elif value is None:
            self._value = None
        else:
            raise parameter.ParameterMismatch(
                'Got ' + `value` + ' for Parameter ' + self.name)
        # self.timestamp.increment()
    def valueDesc(self):
        if config.dimension() == 2:
            return 'A string defining a function of x and y.'
        elif config.dimension() == 3:
            return 'A string defining a function of x, y, and z.'
    def binaryRepr(self, datafile, value):
        length = len(value.funcstr)
        return struct.pack('>i', length) + value.funcstr
    def binaryRead(self, parser):
        b = parser.getBytes(struct.calcsize('>i'))
        (length,) = struct.unpack('>i', b)
        return XYStrFunction(parser.getBytes(length))

class XYTStrFunctionParameter(parameter.Parameter):
    types = (types.StringType, XYStrFunction)
    def __init__(self, name, value=None, default='0.0', tip=None, auxData={}):
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    def set(self, value):
        if type(value) is types.StringType:
            self._value = XYTStrFunction(value)
        elif isinstance(value, XYTStrFunction):
            self._value = value
        elif value is None:
            self._value = None
        else:
            raise parameter.ParameterMismatch(
                'Got ' + `value` + ' for Parameter ' + self.name)
        # self.timestamp.increment()
    def valueDesc(self):
        if config.dimension() == 2:
            return 'A string defining a function of x, y, and t'
        elif config.dimension() == 3:
            return 'A string defining a function of x, y, z, and t.'
    def binaryRepr(self, datafile, value):
        length = len(value.funcstr)
        return struct.pack('>i', length) + value.funcstr
    def binaryRead(self, parser):
        b = parser.getBytes(struct.calcsize('>i'))
        (length,) = struct.unpack('>i', b)
        return XYTStrFunction(parser.getBytes(length))
