# -*- python -*-
# $RCSfile: parameter.py,v $
# $Revision: 1.118.4.13 $
# $Author: langer $
# $Date: 2014/10/03 14:29:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

#--------------

# Parameter objects are named, type-aware containers, and are known to
# the user interface.  There are subclasses of Parameter for all
# the basic types, and a number of composite but not object types
# (i.e. TupleOfInts parameter).  Although the functionality of the
# classes is similar, having separate classes allows for custom
# widgets to be attached to the class for the GUI, as well as for
# customized binary representations of the parameter values.

# Parameter objects are used extensively in the user interface.  The
# name of the parameter will very likely be exposed to the user, and
# so should make sense in that context -- sometimes this may result in
# confusion in other contexts, e.g. there are parameters whose names
# are "skeleton", but which return strings, rather than skeleton
# objects -- this is because the user is in fact being prompted for
# the *name* of a skeleton.

# Most parameters have simple constructors which take a name, an
# initial value, a default value, and various class-specific keyword
# arguments, one of which should be a string-valued thing called a
# "tip" -- this is used by the GUI to put helpful tooltips up for the
# user.

from ooflib.SWIG.common import ooferror
# from ooflib.SWIG.common import timestamp
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import automatic
from ooflib.common.IO.typename import typename
from types import *
import string
import struct

ErrPyProgrammingError = ooferror.ErrPyProgrammingError

structIntFmt = '>i'
structIntSize = struct.calcsize(structIntFmt)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Parameters that don't use TypeChecker should call raiseTypeError if
# they dectect a type mismatch.

def raiseTypeError(got, expected):
    raise TypeError(typeErrorMsg(expected, got))

def typeErrorMsg(got, expected):
    return 'Bad type!\nExpected %s\nGot %s' % (`expected`, `got`)

# TypeChecker is a fairly generic way of checking that a Parameter
# value is of an acceptable type.  It has a __call__ method that
# raises an exception if the types don't match, and a test() method
# that returns None if the types *do* match, and an error message if
# they don't.

class TypeChecker:
    def __init__(self, *types):
        classes = []
        objects = []
        for t in types:
            tt = type(t)
            if tt is ClassType or tt is TypeType:
                classes.append(t)
            else:
                objects.append(t)
        self.classes = tuple(classes)
        self.objects = tuple(objects)
        self.types = types
    def __call__(self, x):
        error = self.test(x)
        if error is not None:
            raise TypeError(error)
    def test(self, x):               # raise TypeError if x is not allowed
        if x is None: # None is a special case that matches everything
            return
        if isinstance(x, (ClassType, TypeType)):
            if issubclass(x, self.classes):
                return
            return typeErrorMsg(x, self.types)
        if isinstance(x, TypeChecker):
            # Check that all types allowed by x are allowed by self.
            for tx in x.classes:
                if not issubclass(tx, self.classes):
                    return typeErrorMsg(x.types, self.types)
            for ox in x.objects:
                for o in self.objects:
                    if type(o) == type(ox) and o == x:
                        break
                return typeErrorMsg(x.types, self.types)
            return
        # x is an instance, or maybe a built in function, or something else...
        if isinstance(x, self.classes):
            return
        for c in self.objects:
            # Checking types before checking equality protects us
            # against poorly written __eq__ methods.
            if type(c) is type(x) and x == c:
                return
        # debug.fmsg("classes=", self.classes, "objects=", self.objects,
        #            "x=", x, type(x))
        return typeErrorMsg(type(x), self.types)
    def __repr__(self):
        if len(self.types)==1:
            return typename(self.types[0])
        return '[' + string.join([typename(t) for t in self.types], ',') + ']'
    def __len__(self):
        return len(self.types)
    def __getitem__(self, i):
        return self.types[i]

class ParameterMismatch(TypeError): pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Code for checking that all Parameter.makeWidget methods have the new
# 'verbose' argument.  To use this, make ParameterMetaClass the
# metaclass for Parameter, and call checkMakeWidget after the GUI is
# started (in oofGUI.start(), for example).

import inspect
_allParameterClasses = []

class ParameterMetaClass(type):
    def __init__(cls, name, bases, dict):
        super(ParameterMetaClass, cls).__init__(name, bases, dict)
        _allParameterClasses.append(cls)

def checkMakeWidget():
    for paramclass in _allParameterClasses:
        try:
            makeWidget = paramclass.makeWidget
        except AttributeError:
            # Some Parameter subclasses are never used in the GUI and
            # intentionally don't have a makeWidget method.
            pass
        else:
            argspec = inspect.getargspec(makeWidget)
            if 'verbose' not in argspec.args:
                print "%s.makeWidget has no verbose arg (%s)" % (
                    paramclass.__name__, inspect.getfile(makeWidget))
                
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Base class for Parameters.

## There are three ways that Parameters subclasses can specify the
## type of the values that they represent.  Which method is used
## depends on how much type checking is desired and on how the
## Parameter is going to be used.  This is *not* an ideal situation....

## Method 1:  Define a member function called 'checker'.  Calling
## checker(x) should raise a TypeError if x is not a valid value for
## the Parameter.

## Method 2:  Don't define 'checker'. Instead place a list or tuple
## called 'types' in the subclass.  Any types in the list will be
## accepted.  Type checking will be done by a TypeChecker.

## Method 3: Redefine Parameter.set in the derived class, and have it
## do the checking.  The base class's set() routine uses method 1, if
## possible, and method 2 otherwise.

## Method 2 is the simplest, but it won't work if you need to check
## that a value is a list of lists of floats, or something similarly
## complicated.  Method 2 uses the TypeChecker mechanism, which means
## that Parameters using this method can be used as the input argument
## for Outputs.  Method 1 Parameters can't be used as Output inputs,
## unless their checkers explicitly allow comparison to TypeCheckers,
## like TypeChecker itself does.

## Any Parameter likely to be used in an Output must have a
## checker that will accept a TypeChecker(xtype) instead of xtype
## itself.  That's a good reason for them to use Method 2 for their
## own type checking.

## The reason for this mess is that way back in the old days, before
## version 1.99 of this file, some Parameters had the line
## 'self.checker = TypeChecker(...)  in their __init__.  This had to
## come *before* the call to the base class __init__, because the base
## class __init__ calls set(), which calls checker().  That created a
## problem for subclasses that were themselves used as base classes
## for other Parameters-- there would be no correct place for the
## derived class to redefine self.checker.  The solution to that
## problem is to not have the subclasses invoke TypeChecker
## explicitly, but instead to define a list of types (Method 2).  Then
## the types belonging to the most derived class are used.

## This design is ugly for at least two reasons. (1) If any base class
## defines checker(), then the 'types' list in the subclass will be
## ignored.  (2) Classes to be used as Outputs' inputs *must* use
## TypeChecker, and so have to use Method 2, but this requirement
## isn't enforced by the class hierarchy.

## Derived classes must also provide __repr__(), binaryRepr(),
## binaryRead() and possibly clone() (if the supplied clone() is
## insufficient).

## The 'default' argument to the constructor is used in cases where
## it's necessary to distinguish between variables that are set and
## those that are unset (ie have value==None) but it's nonetheless
## necessary to display a value for the unset variables.  The
## displayed value can be retrieved from 'default'.  For an example,
## see the Output class in common/IO/output.py.

class Parameter(object):
    #__metaclass__ = ParameterMetaClass ## For checking subclasses
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        self.name = name
        self.tip = tip
        # self.timestamp = timestamp.TimeStamp()
        self.group = None
        self.default = default  # used by Output

        # Additional data for external use, set by set_data and
        # retrieved by get_data()
        self.auxData = auxData.copy()

        if not hasattr(self, 'checker'):
            try:
                self.checker = TypeChecker(*self.types)
            except AttributeError:
                # Subclasses that get here have to have their own
                # set() function that doesn't call self.checker()!
                pass
            
        # Internally, don't use "self.value = x" unless you really
        # want to call self.set(x)!
        self._value = None
        if value is not None:
            self.set(value)

    def __eq__(self, other):
        return (self.__class__ is other.__class__ and
                self.name == other.name and 
                self.tip == other.tip and 
                self.value == other.value)

    def __hash__(self):
        return hash((self.name, self.__class__))

    # Parameter.value is a property so that its type can be checked
    # when its value is set.  Parameter.set() does the type checking,
    # and it assigns the value to Parameter._value (with an
    # underscore).  Subclasses must either redefine the default
    # Parameter.set(), below, or keep set() and redefine
    # Parameter.checker().
    def _getvalue(self):
        return self._value
    def _setvalue(self, val):
        self.set(val)
    value = property(_getvalue, _setvalue)

    def set(self, value):
        if value is not None:
            try:
                self.checker(value)
            except TypeError, msg:
                raise ParameterMismatch(str(msg) + '\nfor Parameter: '
                                        + self.name)
        self._value = self.converter(value)
        # self.timestamp.increment()

    # Subclasses can override converter() to ensure that stored values
    # have the correct form.
    def converter(self, value):
        return value

    def __repr__(self):
        return "%s(name='%s', value=%s, default=%s)" % \
               (self.__class__.__name__, self.name, self.value, self.default)

    # def getTimeStamp(self):             # When was this parameter changed?
    #     return self.timestamp

    def incomputable(self, context):    # used by Output
        if self.value is None:
            return "Parameter '%s' has no assigned value." % self.name

    def groupsize(self):        # used by ParameterGroup
        return 1

    def set_group(self, group):
        # Called by ParameterGroup when this Parameter is added to a group.
        self.group = group

    def set_data(self, tag, data):
        self.auxData[tag] = data

    def get_data(self, tag):
        return self.auxData.get(tag, None)
            
    def clone(self):
        # Override this if the derived class has any local data!
        bozo = self.__class__(self.name, self.value, self.default, self.tip,
                              self.auxData)
        return bozo

    def makeWidget(self, scope, verbose, *args, **kwargs):
        # This function must be overridden in derived classes in GUI mode.
        raise ooferror.ErrPyProgrammingError(
            'No widget for %s!' % self.__class__.__name__)


    def binaryRepr(self, datafile, value):
        raise ooferror.ErrPyProgrammingError(
            "Somebody forgot to define %s.binaryRepr()!"
            % self.__class__.__name__)

    def binaryRead(self, parser):
        raise ooferror.ErrPyProgrammingError(
            "Somebody forgot to define %s.binaryRead()!" 
            % self.__class__.__name__)

    # The following three functions are used for documenting the user
    # interface.
    def classRepr(self):
        # Returns the name of the type of parameter.  For most
        # parameters, this is just the class name, but for some (such
        # as RegisteredParameters) the class name isn't sufficient.
        return self.__class__.__name__
    def valueRepr(self):
        # Returns a string representing the legal values for the
        # parameter.  If the classRepr is sufficient, this doesn't
        # need to return anything.
        pass
    def valueDesc(self):
        # valueDesc returns a string that describes the allowable
        # values for the parameter.  It's used in the automatically
        # generated xml documentation.  It can contain any docbook
        # markup allowed within a <para> element.
        raise "Someone forgot to define %s.valueDesc" % self.__class__.__name__

##########

# Special Parameter subclasses.  They have specialized widgets and
# BinaryReprs.

class BooleanParameter(Parameter):
    def __init__(self, name, value=None, default=False, tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        # Comparing to 0 and 1 works for both Booleans and Ints, so
        # it's ok even for versions of Python that don't have
        # types.BooleanType.
        if x!=0 and x!=1:
            raiseTypeError(type(x), "True or False")
    def set(self, value):
        if value is not None:
            if not (value==0 or value==1):
                raise ParameterMismatch('Got ' + `value` + ' for Parameter '
                                        + self.name)
        self._value = value
        # self.timestamp.increment()
    def binaryRepr(self, datafile, value):
        if value:
            return "1"
        return "0"
    def binaryRead(self, parser):
        v = parser.getBytes(1)
        return (v == "1")
    def valueDesc(self):
        return "Boolean, True or False (or 1 or 0)."

class _RangeParameter(Parameter):
    def __init__(self, name, range, types, value, default, tip, auxData={}):
        self.range = range
        self.types = types
        Parameter.__init__(self, name, value, default, tip, auxData)
    def clone(self):
        return self.__class__(self.name, self.range, self.value, self.default,
                              self.tip, self.auxData)
    def set(self, value):
        if value is not None:
            if type(value) not in self.types:
                raise ParameterMismatch('Got ' + `value` + ' for Parameter '
                                        + self.name)
            if self.range[0] <= value <= self.range[1]:
                self._value = value
                # self.timestamp.increment()
            else:
                raise ValueError('Parameter value out of range for '
                                 + self.name)
    def classRepr(self):
        return "%s%s" % (self.__class__.__name__, self.range)

class IntRangeParameter(_RangeParameter):
    def __init__(self, name, range, value=None, default=None, tip=None,
                 auxData={}):
        # range must be a tuple (min, max)
        _RangeParameter.__init__(self, name, range, [IntType], value, default,
                                 tip, auxData)
    def binaryRepr(self, datafile, value):
        return struct.pack(structIntFmt, value)
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (val,) = struct.unpack(structIntSize, b)
        return val
    def valueDesc(self):
        return "An integer in the range [%d, %d]." % \
               (self.range[0], self.range[1])

class FloatRangeParameter(_RangeParameter):
    structfmt = ">d"
    structsize = struct.calcsize(structfmt)
    def __init__(self, name, range, value=None, default=None, tip=None,
                 auxData={}):
        # range must be a tuple (min, max, step)
        _RangeParameter.__init__(self, name, range, [FloatType, IntType],
                                 value, default, tip, auxData)
    def binaryRepr(self, datafile, value):
        return struct.pack(FloatRangeParameter.structfmt, value)
    def binaryRead(self, parser):
        b = parser.getBytes(FloatRangeParameter.structsize)
        (val,) = struct.unpack(FloatRangeParameter.structfmt, b)
        return val
    def valueDesc(self):
        return "A real number in the range [%d, %d]." % \
               (self.range[0], self.range[1])
        
# Parameter class that can take a float or an integer,
# or the special value "automatic". 
class AutoNumericParameter(Parameter):
    types = (FloatType, IntType, automatic.Automatic)
    def valueRepr(self):
        return "Int, Float, or automatic"
    def valueDesc(self):
        return "An integer, a real number, or the string 'automatic'."


class AutoIntParameter(Parameter):
    structfmt = ">ii"
    structsize = struct.calcsize(structfmt)
    types = (IntType, automatic.Automatic)
    def valueRepr(self):
        return "Int or automatic"
    def valueDesc(self):
        return "An integer, or the string 'automatic'."
    def binaryRepr(self, datafile, value):
        auto = (value == automatic.automatic)
        if auto:
            return struct.pack(AutoIntParameter.structfmt, 1, 0)
        else:
            return struct.pack(AutoIntParameter.structfmt, 0, value)
    def binaryRead(self, parser):
        b = parser.getBytes(AutoIntParameter.structsize)
        (auto, val) = struct.unpack(AutoIntParameter.structfmt, b)
        if auto:
            return automatic.automatic
        return val
    

# Parameter type for an integer number of values or a list of specific
# float values -- used for the set of levels in the contour maps, but
# possibly useful elsewhere.

class ValueSetParameter(Parameter):
    types = (IntType, ListType, TupleType)
    def converter(self, value):
        if type(value) is ListType:
            return tuple(value)
        return value
    def valueRepr(self):
        return "Int or List of numbers"
    def valueDesc(self):
        return "An integer, or a list of numbers."


# Inherits parent class's "converter" function.
class AutomaticValueSetParameter(ValueSetParameter):
    types = (IntType, ListType, TupleType, automatic.Automatic)
    def valueRepr(self):
        return "Int or List of numbers, or automatic"
    def valueDesc(self):
        return "An integer, or a list of numbers, or 'automatic'."
    
        
  
# Special parameter type for strings.  Making a subclass allows for a
# widget that doesn't require the quotes.  Note that using this
# parameter means the user can't just type in the name of a variable
# containing a string.

class StringParameter(Parameter):
    types = (StringType,)
    def binaryRepr(self, datafile, value):
        length = len(value)
        return struct.pack(structIntFmt, length) + value
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        return parser.getBytes(length)
    def valueDesc(self):
        return "A character string."

class RestrictedStringParameter(StringParameter):
    def __init__(self, name, exclude, value=None, default="", tip=None, 
                 auxData={}):
        self.exclude = exclude
        Parameter.__init__(self, name, value=value, default=default, tip=tip,
                           auxData=auxData)
    def set(self, value):
        if value is not None:
            if type(value) is not StringType:
                raise ParameterMismatch(
                    "Expected a character string for Parameter: " + self.name)
            for c in self.exclude:
                if c in value:
                    if len(self.exclude) == 1:
                        raise ParameterMismatch(
                            "Parameter '%s' cannot contain the character '%s'"
                            % (self.name, self.exclude))
                    raise ParameterMismatch(
                        "Parameter '%s' cannot contain the characters '%s'"
                        % (self.name, self.exclude))
        self._value = self.converter(value)
        # self.timestamp.increment()
    def clone(self):
        return self.__class__(self.name, self.exclude, self.value,
                              self.default, self.tip, self.auxData)
    def __repr__(self):
        return "%s(name='%s', exclude='%s', value=%s, default=%s)" % \
               (self.__class__.__name__, self.name, self.exclude, self.value,
                self.default)
    def valueDesc(self):
        if len(self.exclude) == 1:
            return "A character string not containing '%s'." % self.exclude
        return ("A character string not containing any characters in '%s'."
                % self.exclude)

class ListOfStringsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raiseTypeError(type(x), "list of strings")
        for s in x:
            if type(s) is not StringType:
                raiseTypeError("list of %s" % typename(type(s)),
                               "list of strings")
    def binaryRepr(self, datafile, value):
        lengthstr = struct.pack(structIntFmt, len(value))
        strings = [lengthstr] + [struct.pack(structIntFmt, len(s)) + s
                                 for s in value]
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        strings = []
        for i in range(length):
            b = parser.getBytes(structIntSize)
            (strlen,) = struct.unpack(structIntFmt, b)
            strings.append(parser.getBytes(strlen))
        return strings
    def valueDesc(self):
        return "A list of character strings."

class FloatParameter(Parameter):
    types=(IntType, FloatType)
    def __init__(self, name, value=None, default=0.0, tip=None, auxData={}):
        Parameter.__init__(self, name, value=value, default=default, tip=tip,
                           auxData=auxData)
    structfmt = '>d'
    structsize = struct.calcsize(structfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(FloatParameter.structfmt, value)
    def binaryRead(self, parser):
        b = parser.getBytes(FloatParameter.structsize)
        (val,) = struct.unpack(FloatParameter.structfmt, b)
        return val
    def __repr__(self):
        return "FloatParameter(%s, value=%s, default=%s)" \
               % (`self.name`, `self.value`, `self.default`)
    def valueDesc(self):
        return "A real number."

class PositiveFloatParameter(FloatParameter):
    def valueDesc(self):
        return "A positive real number."

class NonNegativeFloatParameter(FloatParameter):
    def valueDesc(self):
        return "A non-negative real number."

class IntParameter(Parameter):
    types=(IntType,)
    def __init__(self, name, value=None, default=0, tip=None, auxData={}):
        Parameter.__init__(self, name, value=value, default=default, tip=tip,
                           auxData=auxData)
    def binaryRepr(self, datafile, value):
        return struct.pack(structIntFmt, value)
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (val,) = struct.unpack(structIntFmt, b)
        return val
    def __repr__(self):
        return "IntParameter(%s,%s)" % (`self.name`, `self.value`)
    def valueDesc(self):
        return "Integer."

class ListOfIntsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raiseTypeError(type(x), "list of Ints")
        for y in x:
            if type(y) is not IntType:
                raiseTypeError("list of %s" % type(y), "list of Ints")
    def binaryRepr(self, datafile, value):
        lengthstr = struct.pack(structIntFmt, len(value))
        datafmt = '>%di' % len(value)
        datastr = struct.pack(datafmt, *value)
        return lengthstr + datastr
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        format = '>%di' % length
        datasize = struct.calcsize(format)
        b = parser.getBytes(datasize)
        return list(struct.unpack(format, b))
    def valueDesc(self):
        return "A list of integers."

class ListOfFloatsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raiseTypeError(type(x), "list of Floats")
        for y in x:
            if type(y) not in (FloatType, IntType):
                raiseTypeError("list of %s" % type(y), "list of Floats")
    def binaryRepr(self, datafile, value):
        lengthstr = struct.pack(structIntFmt, len(value))
        datafmt = '>%dd' % len(value)
        datastr = struct.pack(datafmt, *value)
        return lengthstr + datastr
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        format = ">%dd" % length
        datasize = struct.calcsize(format)
        b = parser.getBytes(datasize)
        return list(struct.unpack(format, b))
    def valueDesc(self):
        return "A list of floating point numbers."

# The SkeletonInfo toolbox requires a tuple of ints parameter for
# which "None" is also a valid value.  
class TupleOfIntsParameter(Parameter):
    def __init__(self, name, value=None, default=(), tip=None, auxData={}):
        Parameter.__init__(self, name, value=value, default=default, tip=tip,
                           auxData=auxData)
    def checker(self, x):
        if x is not None:
            if type(x) is not TupleType:
                raiseTypeError(type(x), TupleType)
            for i in x:
                if type(i) is not IntType:
                    raisetypeError(
                        "Tuple of %s" % type(i), "Tuple of Ints.")
    def valueDesc(self):
        return "A tuple of integers, or None."
        

class ListOfUnsignedShortsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raiseTypeError(type(x), "list of unsigned shorts")
        for y in x:
            if type(y) is not IntType:
                raiseTypeError("list of %s" % type(y),
                               "list of unsigned shorts")
    def binaryRepr(self, datafile, value):
        lengthstr = struct.pack(structIntFmt, len(value))
        datafmt = '>%dH' % len(value)
        datastr = struct.pack(datafmt, *value)
        return lengthstr + datastr
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        format = '>%dH' % length
        datasize = struct.calcsize(format)
        b = parser.getBytes(datasize)
        return list(struct.unpack(format, b))
    def valueDesc(self):
        return "A list of unsigned short integers."

class ListOfUnsignedCharsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raiseTypeError(type(x), "list of unsigned chars")
        for y in x:
            if type(y) is not IntType:
                raiseTypeError("list of %s" % type(y),
                               "list of unsigned chars")
    def binaryRepr(self, datafile, value):
        lengthstr = struct.pack(structIntFmt, len(value))
        datafmt = '>%dB' % len(value)
        datastr = struct.pack(datafmt, *value)
        return lengthstr + datastr
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        format = '>%dB' % length
        datasize = struct.calcsize(format)
        b = parser.getBytes(datasize)
        return list(struct.unpack(format, b))
    def valueDesc(self):
        return "A list of unsigned chars (ie, bytes)."

class ListOfTuplesOfIntsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raise TypeError("Expected a List of Tuples of Ints!")
        # Type-check doesn't take much longer than assignment.
        for t in x:
            if type(t) is not TupleType:
                raise TypeError("Expected a List of Tuples of Ints!")
            for o in t:
                if type(o) is not IntType:
                    raise TypeError("Expected a List of Tuples of Ints!")
    def binaryRepr(self, datafile, value):
        length = struct.pack(structIntFmt, len(value))
        strings = [length]
        for tpl in value:
            tlen = len(tpl)
            lengthstr = struct.pack(structIntFmt, tlen)
            data = struct.pack('>%di'% tlen, *tpl)
            strings.append(lengthstr)
            strings.append(data)
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        val = [None]*length
        for i in range(length):
            b = parser.getBytes(structIntSize)
            (tlen,) = struct.unpack(structIntFmt, b)
            format = '>%di' % tlen
            b = parser.getBytes(struct.calcsize(format))
            val[i] = struct.unpack(format, b)
        return val
    def valueRepr(self):
        return "List of variably sized Tuples of Ints"
    def valueDesc(self):
        return "A list of tuples of integers.  The tuples do not all have to have the same size."

class ListOfListOfIntsParameter(Parameter):
    # The binary repr for this parameter assumes that all the sublists
    # are the same length.
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raise TypeError("Expected a List of Lists of Ints")
        for t in x:
            if type(t) is not ListType or len(t) != len(x[0]):
                raise TypeError("Expected a List of uniform Lists of Ints")
            for o in t:
                if type(o) is not IntType:
                    raise TypeError("Expected a List of Lists of Ints")
    def binaryRepr(self, datafile, value):
        h = len(value)
        w = len(value[0])
        size = struct.pack('>ii', h, w)
        strings = [size]
        for lst in value:
            strings.append(struct.pack('>%di' % w, *lst))
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(struct.calcsize('>ii'))
        (h, w) = struct.unpack('>ii', b)
        format = '>%di' % w
        chunksize = struct.calcsize(format)
        val = [None]*h
        for i in range(h):
            b = parser.getBytes(chunksize)
            val[i] = list(struct.unpack(format, b))
        return val
    def valueRepr(self):
        return "List of uniformly sized Lists of Ints"
    def valueDesc(self):
        return "A list of lists of integers.  The sublists must all have the same size."
                
class ListOfListOfFloatsParameter(Parameter):
    # The binary repr for this parameter assumes that all the sublists
    # are the same length.
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raise TypeError("Expected a List of Lists of Ints")
        for t in x:
            if type(t) is not ListType or len(t) != len(x[0]):
                raise TypeError("Expected a List of uniform Lists of Ints")
            for o in t:
                if type(o) not in (FloatType, IntType):
                    raise TypeError("Expected a List of Lists of Floats")
    def binaryRepr(self, datafile, value):
        h = len(value)
        w = len(value[0])
        size = struct.pack('>ii', h, w)
        strings = [size]
        for lst in value:
            strings.append(struct.pack('>%dd' % w, *lst))
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(struct.calcsize('>ii'))
        (h, w) = struct.unpack('>ii', b)
        format = '>%dd' % w
        chunksize = struct.calcsize(format)
        val = [None]*h
        for i in range(h):
            b = parser.getBytes(chunksize)
            val[i] = list(struct.unpack(format, b))
        return val
    def valueRepr(self):
        return "List of uniformly sized Lists of Floats"
    def valueDesc(self):
        return "A list of lists of floats.  The sublists must all have the same size."
                
class ListOfTuplesOfFloatsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raise TypeError("Expected a List of Tuples of Floats!")
        # Type-check doesn't take much longer than assignment.
        for t in x:
            if type(t) is not TupleType:
                raise TypeError("Expected a List of Tuples of Floats!")
            for o in t:
                if type(o) not in (FloatType, IntType):
                    raise TypeError("Expected a List of Tuples of Floats!")
    def binaryRepr(self, datafile, value):
        length = struct.pack(structIntFmt, len(value))
        strings = [length]
        for tpl in value:
            tlen = len(tpl)
            lengthstr = struct.pack(structIntFmt, tlen)
            data = struct.pack('>%dd' % tlen, *tpl)
            strings.append(lengthstr)
            strings.append(data)
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        val = [None]*length
        for i in range(length):
            b = parser.getBytes(structIntSize)
            (tlen,) = struct.unpack(structIntFmt, b)
            format = '>%dd' % tlen
            b = parser.getBytes(struct.calcsize(format))
            val[i] = struct.unpack(format, b)
        return val
    def valueRepr(self):
        return "List of variably sized Tuples of Floats"
    def valueDesc(self):
        return "A list of tuples of real numbers. The tuples do not all have to have the same size."

class ListOfTuplesOfIntFloatsParameter(Parameter):
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value=value, default=default, tip=tip,
                           auxData=auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raise TypeError("Expected a List of Tuples!")
        # Type-check doesn't take much longer than assignment.
        for t in x:
            if type(t) is not TupleType:
                raise TypeError("Expected Tuples in the List!")
            if type(t[0]) is not IntType:
                raise TypeError("Expected Int for the first slot in Tuple!")
            for o in t[1:]:
                if type(o) not in (FloatType, IntType):
                    raise TypeError("Expected Floats!")
    def binaryRepr(self, datafile, value):
        listlength = struct.pack(structIntFmt, len(value))
        strings = [listlength]
        for tpl in value:
            tlen = len(tpl)-1           # number of doubles in the tuple
            lengthstr = struct.pack(structIntFmt, tlen)
            data = struct.pack('>i%dd' % tlen, tpl[0], *(tpl[1:]))
            strings.append(lengthstr)
            strings.append(data)
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (listlength,) = struct.unpack(structIntFmt, b)
        val = [None]*listlength
        for i in range(listlength):
            b = parser.getBytes(structIntSize)
            (tlen,) = struct.unpack(structIntFmt, b)
            format = '>i%dd' % tlen
            b = parser.getBytes(struct.calcsize(format))
            val[i] = struct.unpack(format, b)
        return val
    def valueRepr(self):
        return "List of Tuples containing one Int followed by a variable number of Floats"
    def valueDesc(self):
        return "A list of tuples containing one integer followed by a variable number of real numbers."

# 3D versions
class ListOfListOfListOfIntsParameter(Parameter):
    # The binary repr for this parameter assumes that all the sublists
    # and subsublists are the same length
    def __init__(self, name, value=None, default=[], tip=None, auxData={}):
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        if type(x) is not ListType:
            raise TypeError("Expected a List of Lists of Lists of Ints")
        for t in x:
            if type(t) is not ListType or len(t) != len(x[0]):
                raise TypeError("Expected a List of Lists of Lists of Ints")
            for o in t:
                if type(o) is not ListType or len(o) != len(t[0]):
                    raise TypeError("Expected a List of Lists of Lists of Ints")
                for p in o:
                    if type(p) is not IntType:
                         raise TypeError("Expected a List of Lists of Lists of Ints")
    def binaryRepr(self, datafile, value):
        h = len(value)
        w = len(value[0])
        d = len(value[0][0])
        size = struct.pack('>iii', h, w, d)
        strings = [size]
        for lst in value:
            for lst2 in lst:
                strings.append(struct.pack('>%di' % d, *lst2))
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(struct.calcsize('>iii'))
        (h, w, d) = struct.unpack('>iii', b)
        format = '>%di' % d
        chunksize = struct.calcsize(format)
        val = [[None]*w for i in range(h)] # NOT [[None]*w]*h !!
        for i in range(h):
            for j in range(w):
                b = parser.getBytes(chunksize)
                val[i][j] = list(struct.unpack(format, b))
        return val
    def valueRepr(self):
        return "List of uniformly sized Lists of Ints"
    def valueDesc(self):
        return "A list of lists of integers.  The sublists must all have the same size."

# RegisteredParameter stores an instance of a RegisteredClass.
class RegisteredParameter(Parameter):
    def __init__(self, name, reg, value=None, default=None, tip=None, 
                 auxData={}):
        # reg must be a RegisteredClass class.
        self.registry = reg.registry
        self.reg = reg
        Parameter.__init__(self, name, value, default, tip, auxData)
    def checker(self, x):
        for registration in self.registry:
            if isinstance(x, registration.subclass):
                return
        # Type check failed. Compose a useful error message.
        if type(x) is InstanceType:
            gotname = x.__class__.__name__
        else:
            gotname = type(x)
        raise TypeError(
            'Bad type for RegisteredParameter! Got %s\nExpected one of %s'
            % (gotname, [reg.subclass.__name__ for reg in self.registry]))
    def clone(self):
        try:
            return self.__class__(self.name, self.reg, self.value, self.default,
                                  self.tip, self.auxData)
        except TypeError:
            debug.fmsg("Failed to clone RegisteredParameter of class",
                       self.__class__.__name__)
            raise
    def regname(self):
        if isinstance(self.reg, (ClassType, TypeType)):
            return self.reg.__name__
        # InstanceType.
        return self.reg.__class__
    def __repr__(self):
        return '%s(%s, %s, %s, %s)' %\
               (self.__class__.__name__, self.name, self.regname(),
                `self.value`, self.tip)

    # For registered class objects, the object itself has enough
    # information to write itself in binary, so the Parameter doesn't
    # have to do the work.  But for reading, there is no instance of
    # the RegisteredClass, so the parameter has to do it.
    def binaryRepr(self, datafile, value):
        return value.binaryRepr(datafile)
    def binaryRead(self, parser):
        return registeredclass.binaryReadRegClass(parser, self.registry)
    def classRepr(self):
        return "%s(%s)" % (self.__class__.__name__, self.regname())
    def valueRepr(self):
        return string.join([reg.subclass.__name__ for reg in self.registry],
                           '\n')
    def valueDesc(self):
        from ooflib.common.IO import xmlmenudump # delayed to avoid import loops
        nm = xmlmenudump.stripPtr(self.regname())
        try:
            # RegisteredClasses that are secret don't appear in the
            # manual, although menu commands in the manual may refer
            # to them.  Here we have to make sure that we don't
            # actually link to the nonexistent pages.
            if self.reg.secret:
                return "An object of the <classname>%s</classname> class." % nm
        except AttributeError:
            return \
         "An object of the <link linkend='RegisteredClass-%s'><classname>%s</classname></link> class." % (nm,nm)


# RegisteredListParameter stores a list of instances of
# RegisteredClasses.  No more than one member of each subclass can be
# present, although this restriction isn't enforced here.  The
# associated widget in GUI/regclassfactory.py does enforce it.

class RegisteredListParameter(RegisteredParameter):
    def __init__(self, name, reg, value=None, default=[], tip=None, 
                 auxData={}):
        # "value"s default value is different in RegisteredParameter.
        RegisteredParameter.__init__(self, name, reg, value, default, tip,
                                     auxData)
    def checker(self, x):
        if not (type(x)==ListType or type(x)==TupleType):
            raise TypeError('Type of RegisteredListParameter must be a List')
        for p in x:
            RegisteredParameter.checker(self, p)
    def binaryRepr(self, datafile, value):
        lengthstr = struct.pack(structIntFmt, len(value))
        strings = [lengthstr]
        for obj in value:
            strings.append(obj.binaryRepr(datafile))
        return string.join(strings, '')
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        val = [None]*length
        for i in range(length):
            val[i] = registeredclass.binaryReadRegClass(parser, self.registry)
        return val
    def valueDesc(self):
        return \
        "A list of objects of the <link linkend='RegisteredClass-%s'><classname>%s</classname></link> class." \
        % (self.regname(), self.regname())





# The AutomaticNameParameter can be set to either a string or the
# object automatic.automatic.  When asked for its value, however, it
# always returns a string, which is generated from the raw input by
# calling the provided 'resolver' function.  The arguments to the
# resolver are the parameter and the raw input.  The resolver can use
# the boolean function AutomaticNameParameter.automatic() to see if
# the raw input was automatic.automatic.

# In order for the resolver function to be useful,
# AutomaticNameParameters should probably be in ParameterGroups.  That
# gives the resolver access to other parameters in the group, which it
# can use to determine what names are available.

# Because the AutomaticNameParameter needs to intercept both the
# setting and getting of its value, it doesn't call
# Parameter.__init__.  It stores the raw input in
# self.truevalue.
## TODO OPT: It should use a Python property for that.

class AutomaticNameParameter(Parameter):
    types = (StringType, automatic.Automatic)
    def __init__(self, name, resolver, value=None, default=None, tip=None,
                 auxData={}):
        self.checker = TypeChecker(*self.types)
        self.name = name                # name of the parameter
        self.tip = tip
        self.default = default
        self.auxData = auxData.copy()
        
        # self.timestamp = timestamp.TimeStamp()
        self.group = None
        self.resolver = resolver
        if value is not None:
            self.set(value)
        else:
            self.truevalue=None

    def set(self, value):
        if value is not None:
            try:
                self.checker(value)
            except TypeError, msg:
                raise ParameterMismatch(
                    str(msg) + "\nfor AutomaticNameParameter: " + self.name)
        self.truevalue=value
        # self.timestamp.increment()

    def clone(self):
        return AutomaticNameParameter(self.name,
                                      self.resolver,
                                      self.truevalue,
                                      self.default,
                                      self.tip,
                                      self.auxData)
    def nontrivial(self):
        # The "trivial" values are either self.truevalue = None or "".
        # These are both logically false.
        return self.truevalue
        
    def automatic(self):
        return self.truevalue==automatic.automatic

    def __getattr__(self, attr):
        if attr=='value':
            return self.resolver(self, self.truevalue)
        raise AttributeError

    def __repr__(self):
        return 'AutomaticNameParameter(%s, resolver=%s, truevalue=%s, %s)' % \
               (self.name, self.resolver, self.truevalue, self.tip)
    def valueDesc(self):
        return \
          "A character string, or the variable <constant>automatic</constant>."

    def binaryRepr(self, datafile, value):
        length = len(value)
        return struct.pack(structIntFmt, length) + value
    
    def binaryRead(self, parser):
        b = parser.getBytes(structIntSize)
        (length,) = struct.unpack(structIntFmt, b)
        return parser.getBytes(length)

class RestrictedAutomaticNameParameter(AutomaticNameParameter):
    def __init__(self, name, exclude, resolver, value=None, default=None,
                 tip=None, auxData={}):
        self.name = name
        self.tip = tip
        self.default = default
        self.auxData = auxData.copy()
        # self.timestamp = timestamp.TimeStamp()
        self.group = None
        self.resolver = resolver
        self.exclude = exclude
        if value is not None:
            self.set(value)
        else:
            self.truevalue = None
    def set(self, value):
        if value is not None and value is not automatic.automatic:
            if type(value) is not StringType:
                raise ParameterMismatch(
                    "Expected a character string for Parameter: " + self.name)
            for c in self.exclude:
                if c in value:
                    if len(self.exclude) == 1:
                        raise ParameterMismatch(
                            "Parameter '%s' cannot contain the character '%s'"
                            % (self.name, self.exclude))
                    raise ParameterMismatch(
                        "Parameter '%s' cannot contain the characters '%s'"
                        % (self.name, self.exclude))
        self.truevalue = value
        # self.timestamp.increment()
    def clone(self):
        return RestrictedAutomaticNameParameter(self.name, self.exclude,
                                                self.resolver, self.value,
                                                self.default, self.tip,
                                                self.auxData)
    def __repr__(self):
        return "RestrictedAutomaticNameParameter(%s, exclude=%s, resolver=%s, truevalue=%s, tip=%s)" % (
            self.name, self.exclude, self.resolver, self.truevalue, self.tip)
    def valueDesc(self):
        if len(self.exclude) == 1:
            return "A character string not containing '%s', or the variable <constant>automatic</constant>." % self.exclude
        return  "A character string not containing any of the characters '%s', or the variable <constant>automatic</constant>." % self.exclude
  

    
##############################
        
# Specialized parameter classes with specialized 'set' methods (and
# widget constructors in GUI mode).  Trivial classes here are extended
# in common.IO.GUI.parameterwidgets.

class ConvertibleRegisteredParameter(RegisteredParameter):
    pass

        
###############################################

# The ParameterGroup class.  ParameterGroups store lists of
# Parameters, which may be intermixed hierarchically with other
# ParameterGroups.  Parameters in a group know which group they're in,
# and the group hierarchy may be searched to find other Parameters, if
# a Parameter needs to know the value of another Parameter when
# computing its own value. (See instances of AutomaticNameParameter,
# for example.)

# The hierarchical arrangement allows parameters in one menu item to
# be in different groups, which means that their widgets will be in
# different WidgetScopes in the GUI.  Hierarchical groups can be
# created by nesting the ParameterGroup constructors like this:
#    ParameterGroup(p0, p1, ParameterGroup(p2, p3), p4)
# or by concatenating groups like this:
#    ParameterGroup(p0, p1) + ParameterGroup(p2, p3)

# This class used to have a more list-list interface, but that was not
# compatible with the hierarchical modifications, so the most of the
# list-like API was deleted.

class ParameterGroup(object):
    def __init__(self, *params):
        self.params = list(params[:])
        self.group = None       # in case this group is nested.
        self._size = 0
        for p in params:
            p.set_group(self)   # either a Parameter or a ParameterGroup
            # We could use __len__ instead of groupsize, but it would
            # be weird to give Parameters a __len__ method.
            self._size += p.groupsize()

    def append(self, param):
        self.params.append(param)
        param.set_group(self)
        self._size += param.groupsize()

    def clone(self):
        return ParameterGroup(*[p.clone() for p in self.params])

    def __repr__(self):
        return "ParameterGroup(%s)" % ','.join([`p` for p in self.params])

    def set_group(self, group):
        self.group = group

    def groupsize(self):
        return self._size

    def __len__(self):          # total number of Parameters
        return self._size

    # Adding a ParameterGroup to another ParameterGroup or to a list
    # of Parameters creates a hierarchical ParameterGroup.
    def __radd__(self, other):
        if isinstance(other, ParameterGroup):
            return ParameterGroup(other, self)
        return ParameterGroup(*(other + [self]))

    def __add__(self, other):
        if isinstance(other, ParameterGroup):
            return ParameterGroup(self, other)
        return ParameterGroup(self, *other)

    def __iter__(self):         # Loop over self and subgroups.
        for p in self.params:
            if isinstance(p, ParameterGroup):
                for pp in p:
                    yield pp
            else:
                yield p

    # Hierarchical lookup by parameter name.
    def __getitem__(self, name):
        assert type(name) is StringType # ints used to be allowed.
        try:
            # Look in self and child groups.
            return self._lookdown(name)
        except IndexError:
            pass
        if self.group is not None:
            # Look in parent group.
            return self.group._lookdown(name, exclude=self)
        raise IndexError("Parameter %s not found in ParameterGroup." % name)

    def _lookdown(self, name, exclude=None):
        # Search for parameter 'name' in self and child groups, except
        # for the group 'exclude'.
        for p in self.params:
            if isinstance(p, Parameter):
                if p.name == name:
                    return p
        for p in self.params:
            if isinstance(p, ParameterGroup) and p is not exclude:
                try:
                    return p._lookdown(name)
                except IndexError:
                    pass
        raise IndexError("Parameter %s not found in ParameterGroup." % name)

############################################

# Some parameter values may want "deep" comparison operations on them.
# RegisteredClass already does this, but not all values are
# registered.  May have unexpected side-effects if the instance
# attributes have non-simple values.

class Comparable:
    def __eq__(self,other):
        if other is None:
            return 0

        if type(other) != InstanceType or self.__class__ != other.__class__:
            return 0

        for (k,v) in self.__dict__.items():
            if v != other.__dict__[k]:
                return 0
        return 1
    def __ne__(self,other):
        return 1 - self.__eq__(other)

#########################

# Parameters whose values are global objects that are stored in the
# OOF namespace (such as Fields & Equations) can be subclasses of
# ObjParameter.  ObjParameter only defines binaryRead and binaryRepr--
# subclasses must also be derived from Parameter.

class ObjParameter:
    def binaryRepr(self, datafile, value):
        classkey = datafile.oofObjID(value)
        return struct.pack('>i', classkey)
    def binaryRead(self, parser):
        (classkey,) = struct.unpack('>i',
                                    parser.getBytes(struct.calcsize('>i')))
        return parser.getObject(classkey)

#############################

# Parameters that don't need a tooltip should set their "tip" argument
# to emptyTipString.  This will prevent the api dump from complaining
# about a missing tip.

class EmptyTip:
    def __nonzero__(self):
        return 0
    def read(self, *args):              # for xmlmenudump.getHelp()
        return ""

emptyTipString = EmptyTip()
