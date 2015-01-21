# -*- python -*-
# $RCSfile: registeredclass.py,v $
# $Revision: 1.68.4.9 $
# $Author: langer $
# $Date: 2014/08/02 03:14:46 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


## A RegisteredClass is one that keeps a registry of all of its
## subclasses, enabling objects of the class to be constructed by the
## UI.  The registry is a list of Registrations, each of which
## contains a name, the class object to be instantiated, and a list of
## Parameters whose values are the arguments to the classes
## constructor, and an ordering.  Classes are listed in order of
## increasing ordering when they're listed by the UI.  Additional
## keyword arguments to the Registration constructor are stored as
## data within the Registration object.

## Invoking a Registration's __call__ method creates an instance of
## the registered subclass, using the current values of the Parameters
## for constructor arguments.

## Classes derived from RegisteredClass must have a list called
## 'registry' at the class level.  Eg,
##   class MyRegisteredClass(RegisteredClass):
##      registry = []
##      def __init__(self): etc.

## If the class's Parameters aren't stored as internal variables whose
## names are the corresponding Parameter.name's, then the class must
## override RegisteredClass.getParamValues().

## DOCUMENTATION:

## Registered classes should have 'discussion' and 'tip' members that
## contain docbook xml that can go into <para> and <refsect1>
## elements, respectively.  They describe the purpose of the *base*
## class and are data members of the *base* class:
##    class MyRegisteredClass(RegisteredClass):
##        tip = "Don't take any wooden nickels"
##        discussion = "<para>.... and that's what it's all about!</para>"
## The 'tip' is a short one-line description of the class.  The
## 'discussion' should be longer and in-depth.  It can be read from a
## file using xmlmenudump.loadFile.

## Registrations also have 'tip' and 'discussion' strings.  They are
## given as arguments to the Registration constructor, and are
## instance data, not class data.  The tip is used for both the table
## of contents in the manual and for the tooltip in the GUI, so it
## should not contain xml tags.

####

## QUESTION Can this be made to work even if the registry isn't a
## simple list?  If it's a LabelTree?  The RegisteredClassFactory will
## have to be able to create a heirarchical GtkOptionMenu.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
# from ooflib.SWIG.common import timestamp
from ooflib.common import debug
from ooflib.common import utils
from types import *
import string
import struct

class Registration(object):
    def __init__(self, name, registeredclass, subclass, ordering,
                 params=[], secret=0, tip=None, discussion=None, **kwargs):

        self._name = name
        self.subclass = subclass
        if type(registeredclass) in (ListType, TupleType):
            self.registeredclasses = tuple(registeredclass[:])
        else:
            self.registeredclasses = (registeredclass,)
        self.ordering = ordering
        self.params = params
        self.secret = secret
        self.tip = tip
        self.discussion = discussion
        # Registered subclasses must have unique names in the main OOF
        # namespace:
        try:
            scls = utils.OOFeval(subclass.__name__)
        except NameError:
            # ok, name isn't already defined.
            self.exportToOOF()
        else:
            raise NameError("RegisteredClass subclass '%s' is already defined."
                            % subclass.__name__)

        self.__dict__.update(kwargs)
        # Store the registration.  Extract it first, so that it also
        # works for the RegisteredCClasses.
        for registeredclass in self.registeredclasses:
            registeredclass.registry.append(self)
            # Sorting each time is inefficient, but doesn't happen often.
            registeredclass.registry.sort()
            switchboard.notify(registeredclass)

    def name(self):
        return self._name
    def binReprName(self):              # the name used in the binary reprs.
        return self.subclass.__name__
    def exportToOOF(self):
        # The Registration is put into the OOF namespace with the name
        # of the *subclass*.  This means that any script that creates
        # an object of the subclass actually will call
        # Registration.__call__, and the Parameter arguments will be
        # processed correctly.  (Eg, specialized Parameter.set
        # functions will be called.)
        utils.OOFdefine(self.binReprName(), self)

    # Registrations contain lists of params, making them unhashable.
    # For dictionary use, hash the non-list entries.
    def __hash__(self):
        return hash(self.name())^hash(self.subclass)^hash(self.ordering)

    # Some registration objects need to know when the parameters have
    # been updated.  They should over-ride "new_params" and do
    # whatever needs doing in that. TODO OPT: Is this comment obsolete?
    # There's no new_params.
    def setDefaultParams(self, values):
        # Given a list, tuple, or dictionary of values, set the values
        # of the Parameters.
        if type(values) is ListType:
            for param, value in zip(self.params, values):
                param.value = value
        elif type(values) is DictType:
            for param in self.params:
                param.value = values[param.name]

    def getParameter(self, name):
        for p in self.params:
            if name == p.name:
                return p
        return None

    def getParamValues(self):
        # Return a list of the values of the parameters.
        return [ p.value for p in self.params ]
            
    def __cmp__(self, other):
        if isinstance(other, Registration):
            if self.ordering < other.ordering: return -1
            if self.ordering > other.ordering: return 1
            if self._name < other._name: return -1
            if self._name > other._name: return 1
            return 0
        return -1
    
    # Set any parameters that you can from the keyword arguments,
    # and then create an instance of the RegisteredClass.
    def __call__(self,**kwargs):
        # Check for extra arguments
        paramnames = [p.name for p in self.params]
        for argname in kwargs.keys():
            if argname not in paramnames:
                debug.fmsg("params=", self.params)
                debug.fmsg("paramnames=", paramnames)
                raise ooferror.ErrUserError(
                    "Unexpected argument '%s' in %s constructor"
                    % (argname, self.subclass.__name__))
        pdict = {}
        for p in self.params:
            try:
                p.value = kwargs[p.name]
            except KeyError:
                pass
            pdict[p.name] = p.value
        try:
            object = self.subclass(**pdict)
        except TypeError:
            debug.fmsg("Error creating", self.subclass)
            debug.fmsg("got arguments=", pdict)
            debug.fmsg("expected arguments=", self.params)
            raise
        
        # if not hasattr(object, 'timestamp'):
        #     object.timestamp = timestamp.TimeStamp()
        return object

    def __repr__(self):
        return "%s('%s', subclass=%s, ordering=%s, params=%s)" % \
               (self.__class__.__name__,
                self.name(), self.subclass.__name__,
                `self.ordering`, `self.params`)

#=--=##=--=##=--=##=--=#

class ConvertibleRegistration(Registration):
    def __init__(self, name, registeredclasses, subclass, ordering,
                 params=[], secret=0, to_base=None, from_base=None, **kwargs):
        self.to_base = to_base
        self.from_base = from_base
        Registration.__init__(self, name, registeredclasses,
                              subclass, ordering, params, secret, **kwargs) 
        
    # Convertible equivalent of getParamValues, returns a base object.
    def getParamValuesAsBase(self):
        return self.to_base(self)

    def setParamsFromBase(self, base):
        ## Called by ConvertibleRegisteredClassFactory.setParams.
        ## 'base' ultimately comes from
        ## ConvertibleRegistration.getParamValuesAsBase, which gets
        ## them from ConvertibleRegistration.to_base...
        
        ## TODO 3.1: Remove the 1st arg from from_base?
        # 'base' is the list of parameters for the base constructor (?)
        self.setDefaultParams(self.from_base(self, base))
            
    def __repr__(self):
        t = "%s('%s', subclass=%s, ordering=%s, params=%s."
        return t % (self.__class__.__name__,
                    self.name(), self.subclass.__name__,
                    `self.ordering`, `self.params`)
               
#=--=##=--=##=--=##=--=#

# Instead of filling the code with 'if config.dimension() == 3', the
# registrations for classes that make sense in only one dimensionality
# can be obtained by these functions:

def TwoDOnlyRegistration(*args, **kwargs):
    if config.dimension() == 2:
        return Registration(*args, **kwargs)

def ThreeDOnlyRegistration(*args, **kwargs):
    if config.dimension() == 3:
        return Registration(*args, **kwargs)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class RegisteredClass(object):
#     def getRegistrationIndex(self):
#         # Return the position of this object's subclass in the list of
#         # all subclasses (ie in the registry).
#         for i in range(len(self.registry)):
#             if self.__class__ == self.registry[i].subclass:
#                 return i

#     def getNonSecretRegistrationIndex(self):
#         # Return the position of this object's subclass in the list of
#         # all subclasses, not counting subclasses with
#         # Registration.secret==1.
#         count = 0
#         for registration in self.registry:
#             if isinstance(self, registration.subclass):
#                 return count
#             if not registration.secret:
#                 count += 1
            
    def getRegistration(self):
        # Return this object's subclass's registration. 
        for reg in self.registry:
            if self.__class__ == reg.subclass:
                return reg
        
    def getParamValues(self):
        # Return a list of the values of the registered Parameters of
        # this object.
        registration = self.getRegistration()
        return [self.__dict__[p.name] for p in registration.params]

    def getParamValue(self, paramname):
        registration = self.getRegistration()
        for p in registration.params:
            if p.name == paramname:
                return self.__dict__[paramname]
        raise KeyError("RegisteredClass %s has no parameter named %s!"
                       % (self.__class__.__name__, paramname))

    def setDefaultParams(self):
        # Make the Parameter values for this object the default values
        # for new objects.  The default values are stored in the
        # class's Registration.
        registration = self.getRegistration()
        registration.setDefaultParams(self.getParamValues())

    def getDefaultParams(self):
        return self.getRegistration().params

    # clone() defined like this can be dangerous, if subclasses
    # contain have parameters that are themselves registered
    # parameters, and if those objects contain references to their
    # parent objects.  This causes an infinite loop.  Such subclasses
    # must redefine clone(). (TODO 3.1: Really?  If such an class is
    # found, please document it here.)
    def clone(self):
        self.setDefaultParams()
        return self.getRegistration()()
    
    def paramrepr(self):
        values = self.getParamValues()
        names = [p.name for p in self.getRegistration().params]
        return string.join(['%s=%s' % (name, `value`)
                           for (name, value) in zip(names, values)], ',')

    def shortparamrepr(self):
        values = self.getParamValues()
        names = [p.name for p in self.getRegistration().params]
        valreprs = []
        for val in values:
            try:
                valreprs.append(val.shortrepr())
            except AttributeError:
                valreprs.append(`val`)
        return ','.join(['%s=%s' % (name, valrepr)
                         for (name, valrepr) in zip(names, valreprs)])

    # Equality and inequality booleans.  Does piecewise comparison of
    # attributes in the class, or in the base rep if convertible.
    # This relies on the base rep being an instancetype.
    ## TODO 3.1: This function can lead to surprise recursion if
    ## member attributes of a registeredclass are also
    ## registeredclasses, and there are circular references.  It
    ## probably should be eliminated.
    def __eq__(self,other):
        return (self.__class__ == other.__class__ and
                self.getParamValues() == other.getParamValues())

    def __ne__(self,other):
        return not self.__eq__(other)
    
    def __hash__(self):
        result = hash(self.__class__)
        for paramvalue in self.getParamValues():
            result = result ^ hash(paramvalue)
        return result

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.paramrepr())
## Including the module name, as below, clutters up the scripts and is
## unnecessary since Registration.__init__ checks for uniqueness in
## the OOF namespace.
##        classname = self.__class__.__name__
##        modulename = string.split(self.__module__, '.')[-1]
##        return '%s.%s(%s)' % (modulename, classname, self.paramrepr())

    def shortrepr(self):
        params = self.shortparamrepr()
        if params:
            return '%s(%s)' % (self.__class__.__name__, params)
        else:
            return self.__class__.__name__

    def binaryRepr(self, datafile):
        repstrings = []
        registration = self.getRegistration()
        regkey = datafile.oofObjID(registration)
        repstrings.append(struct.pack('>i', regkey))
        for param,value in zip(registration.params, self.getParamValues()):
            if value is None:
                nonekey = datafile.oofObjID(None)
                repstrings.append(struct.pack('>i', nonekey))
            else:
                repstrings.append(param.binaryRepr(datafile, value))
        return string.join(repstrings, '')
    # def getTimeStamp(self):
    #     # The timestamp is created by Registration.__call__.
    #     return self.timestamp

def getRegistration(regclass, registry):
    # TODO 3.1: Make registries instances of a Registry class, which can
    # do this lookup more efficiently.
    for registration in registry:
        if registration.subclass is regclass:
            return registration

def binaryReadRegClass(parser, registry):
    (regkey,) = struct.unpack('>i', parser.getBytes(struct.calcsize('>i')))
    registration = parser.getObject(regkey)
    if registration is None:
        return None
    argdict = {}
    for param in registration.params:
        argdict[param.name] = param.binaryRead(parser)
    return registration(**argdict)
        
#=--=##=--=##=--=##=--=#

class ConvertibleRegisteredClass(RegisteredClass):
    # Instance-level conversion machinery is the only addition to
    # the ordinary RegisteredClass.
    def to_base(self):
        reg = self.getRegistration()
        return reg.to_base(reg, self.getParamValues())
    # Compare base representations in the convertible case.
    def __eq__(self, other):
        if other is None:
            return False
        reg = self.getRegistration()
        for registeredclass in reg.registeredclasses:
            if issubclass(other.__class__, registeredclass):
                self_base = self.to_base()
                other_base = other.to_base()
                if self_base.__class__ != other_base.__class__:
                    return False
                for k in self_base.__dict__:
                    if getattr(self_base, k) != getattr(other_base, k):
                        return False
                return True
        # If other is from a different class hierarchy, it's not equal.
        return False
