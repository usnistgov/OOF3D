# -*- python -*-
# $RCSfile: cregisteredclass.py,v $
# $Revision: 1.22.4.7 $
# $Author: langer $
# $Date: 2014/11/24 21:44:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# The registerCClass() function makes a swigged C++ class act like
# RegisteredClass.  For documentation on the individual functions, see
# registeredclass.py, where the Python RegisteredClass class is
# defined.

# The Registrations for the subclasses of a C++ registered class must
# be instances of the Registration class in this file
# (cregisteredclass.py) rather than the one in registeredclass.py.

from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import registeredclass
import string
import struct
import sys

def registerCClass(klass):
    klass.registry = []

    if not hasattr(klass, 'getRegistration'):
        def getRegistration(self):
            for reg in self.registry:
                # reg.subclass is the non-Ptr version of the swigged
                # class, which is derived from the Ptr version.  self
                # might be either one.
                if issubclass(reg.subclass, self.__class__):
                    return reg
        klass.getRegistration = getRegistration

    if not hasattr(klass, 'getParamValues'):
        def getParamValues(ego):
            return ego._keepargs
        klass.getParamValues = getParamValues

    if not hasattr(klass, 'setDefaultParams'):
        def setDefaultParams(self):
            registration = self.getRegistration()
            registration.setDefaultParams(self.getParamValues())
        klass.setDefaultParams = setDefaultParams

    if not hasattr(klass, 'getDefaultParams'):
        def getDefaultParams(self):
            return self.getRegistration().params
        klass.getDefaultParams = getDefaultParams

    if not hasattr(klass, 'clone'):
        # clone() defined like this can be dangerous, if subclasses
        # contain have parameters that are themselves registered
        # parameters, and if those objects contain references to their
        # parent objects.  This causes an infinite loop.  Such
        # subclasses must redefine clone().
        def clone(self):
            self.setDefaultParams()
            return self.getRegistration()()
        klass.clone = clone

    if not hasattr(klass, 'paramrepr'):
        def paramrepr(self):
            values = self.getParamValues()
            names = [p.name for p in self.getRegistration().params]
            return string.join(['%s=%s' % (name, `value`)
                                for (name, value) in zip(names, values)], ',')
        klass.paramrepr = paramrepr

    if not hasattr(klass, 'shortrepr'):
        def shortrepr(self):
            return self.getRegistration().name()
        klass.shortrepr = shortrepr

    if not hasattr(klass, '__eq__'):
        def __eq__(self, other):
            if other is None:
                return 0
            if self.__class__ != other.__class__:
                return 0
            reg = self.getRegistration()
            if hasattr(reg, "to_base"):
                self_base = self.to_base
                other_base = other.to_base()
                return self_base.getParamValues() == other_base.getParamValues()
            return self.getParamValues() == other.getParamValues()
        klass.__eq__ = __eq__

    if not hasattr(klass, '__ne__'):
        def __ne__(self, other):
            return not self.__eq__(other) #1 - self.__eq__(other)
        klass.__ne__ = __ne__

    if not hasattr(klass, 'binaryRepr'):
        def binaryRepr(self, datafile):
            repstrings = []
            registration = self.getRegistration()
            regkey = datafile.oofObjID(registration)
            repstrings.append(struct.pack('>i', regkey))
            for param,value in zip(registration.params, self.getParamValues()):
                repstrings.append(param.binaryRepr(datafile, value))
            return string.join(repstrings, '')
        klass.binaryRepr = binaryRepr

    if not hasattr(klass, 'tip'):
        klass.tip = None
    if not hasattr(klass, 'discussion'):
        klass.discussion = None

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Registration(registeredclass.Registration):
    def __init__(self, name, regclass, subclass, ordering,
                 params=[], secret=0, **kwargs):

        registeredclass.Registration.__init__(self, name, regclass, subclass,
                                              ordering, params, secret,
                                              **kwargs)
        self.monkeypatch(reprname=subclass.__name__)

    def monkeypatch(self, reprname):
        # Redefine the subclass's __init__ so that it keeps a list of
        # its arguments.
        self.subclass.oldinit = self.subclass.__init__
        def newinit(ego, *args):
            # Registration.setDefaultParams expects a list, not a
            # tuple, so we have to convert args here.
            ego._keepargs = list(args[:])
            ego.oldinit(*args)
        self.subclass.__init__ = newinit

        # __repr__ has to be redefined here, instead of in the
        # baseclass, so that it overrides the swig-generated __repr__
        # in the subclass.
        def repr(ego, reprname=reprname):
            return '%s(%s)' % (reprname, ego.paramrepr())
        self.subclass.__repr__ = repr
        self.subclass.__str__ = repr
        
        # Actually, __repr__ has to be redefined in the xxxxPtr
        # version of the subclass, which is the parent of the class we
        # have.  The repr for this class, however, should *not* print
        # the 'Ptr' part of the class name, since that name should be
        # hidden from the user, and anyhow there's no way to construct
        # xxxxPtr objects directly from a script.
        def repr(ego, reprname=reprname):
            return '%s(%s)' % (reprname, ego.paramrepr())
        # Just in case there is more than one base class, check for
        # the one that's derived from regclass.
        for base in self.subclass.__bases__:
            if issubclass(base, self.registeredclasses[0]):
                base.__repr__ = repr
                return

    def substituteClass(self, newclass):
        # Sometimes a module is loaded that redefines the behavior of
        # an existing RegisteredClass subclass, for example by adding
        # graphics routines to it.  If the subclass is a Python class,
        # that's no problem, but changing a C++ class at run time is
        # more difficult.  The substituteClass() routine allows a
        # derived class to be substituted for a previously registered
        # C++ class.  The underlying C++ version of the new class must
        # be a subclass of the C++ version of the old class, although
        # this isn't checked for (since it would be a pain to do.. we
        # only have the non-Ptr swigged classes here).  Note that the
        # repr of the class is *not* changed, so scripted commands
        # still refer to the old class.  This is the correct behavior
        # when the modification class is just adding graphics
        # capability.
        oldclass = self.subclass
        self.subclass = newclass
        self.monkeypatch(reprname=oldclass.__name__)

    def __call__(self, *args, **kwargs):
        for arg, param in zip(args, self.params):
            param.value = arg
        for p in self.params:
            try:
                p.value = kwargs[p.name]
            except KeyError:
                pass
        argvals = [p.value for p in self.params]
        object = self.subclass(*argvals)
        
        # # Keep an extra reference to the arguments to ensure that the
        # # Python garbage collector won't destroy them before the
        # # registered class object itself is destroyed.  Also, this
        # # allows getParamValues to return the original Python form of
        # # the arguments.  If getParamValues goes into C++ to return
        # # the arguments, it will return the Ptr form, which will
        # # confuse the RegisteredClass type checking.
        # object._keepargs = argvals

        return object
