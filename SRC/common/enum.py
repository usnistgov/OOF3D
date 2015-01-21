# -*- python -*-
# $RCSfile: enum.py,v $
# $Revision: 1.30.10.5 $
# $Author: fyc $
# $Date: 2014/07/21 18:08:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# EnumClass is a function that creates a class that can take on a
# discrete set of values, determined by the list of strings passed in
# to the function.  You use it by deriving a class from its return value:

# class MyEnum(EnumClass('three', 'two', 'one', 'blastoff')): pass
# x = MyEnum('three')

# The arguments can also be 2-tuples of strings, in which case the
# second string of each pair is a help string:

# class MyOtherEnum(EnumClass(('one', 'number 1'), ('two', 'number 2'))): pass

# Since EnumClass returns a new class called 'Enum' each time it's
# called, there's no way to test if something is an Enum with
# isinstance().  So we derive all Enum classes from EnumBase, and
# check against EnumBase.

# EnumClasses can have 'tip' and 'discussion' strings, which will
# appear in the manual.  For example:
# class MyThirdEnum(EnumClass('a', 'b', 'c')):
#    tip = "A short help string."
#    discussion = "<para>A much longer explanation.</para>"


from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import parameter
import struct
import types

class EnumBase: pass

def EnumClass(*args):
    class Enum(EnumBase):
        def __init__(self, name):
            if not name in self.names:
                raise ValueError('"%s" is not one of %s' % (name, self.names))
            self.name = name

        # The repr returns just the name of the Enum, and not the
        # class, so that scripts look neater.  Instead of this:
        #   OOF.Command(myenum = MyEnum('three'))
        # we have this:
        #   OOF.Command(myenum = 'three')
        # The EnumParameter converts the string to the appropriate
        # EnumClass type before calling the command's callback
        # function.

        # However, when a script contains an Enum Parameter that's
        # *not* a menu parameter, like this:
        #   OOF.Command(regpar = ABC(myenum='three'))
        # where regpar is a RegisteredClass parameter, the
        # EnumParameter mechanism is not invoked.  This means that
        # although the ABC constructor is expecting an Enum, it's
        # getting a string.  But since Enums are pretty much only used
        # by comparing them to other Enums, we can get around the
        # problem by allowing them to be compared with strings.
        
        def __repr__(self):
            return `self.name`
        def __cmp__(self, other):
            if type(other) == types.InstanceType:
                # Comparison between objects in a class hierarchy is allowed.
                if not (issubclass(other.__class__,self.__class__) or
                        issubclass(self.__class__,other.__class__)):
                    # classes aren't related, so the objects can't be equal
                    if self.__class__ < other.__class__: return -1
                    if self.__class__ > other.__class__: return 1
                # Classes are identical or related by inheritance. 
                if self.name < other.name: return -1
                if self.name > other.name: return 1
                return 0
            # See comment above about comparison with strings.
            elif type(other) == types.StringType:
                if self.name < other: return -1
                if self.name > other: return 1
                return 0
            return 1
        def string(self):
            return self.name
        def index(self):
            return self.names.index(self.name)
        def __hash__(self):
            return hash((self.__class__, self.name))

    # Each arg in args is either a string, in which case it's an Enum
    # name, or it's a tuple of two strings, in which case the first
    # string is the Enum name and the second is the help string for
    # that Enum.
    Enum.names = []
    Enum.helpdict = {}
    for arg in args:
        if type(arg) is types.StringType:
            Enum.names.append(arg)
        else:
            Enum.names.append(arg[0])
            if arg[1]:
                Enum.helpdict[arg[0]] = arg[1]

    return Enum

def addEnumName(enumclass, name, help=None):
    enumclass.names.append(name)
    if help is not None:
        enumclass.helpdict[name] = help
    switchboard.notify(enumclass)

# Create a subclass of an existing Enum.  The subclass gets all of the
# names from the base class, plus any extras listed in args.  args can
# be either a list of names or of (name, help) tuples.  Any new
# entries added to the base class by addEnumName after the subclass is
# created will *not* be included in the subclass.

def subClassEnum(baseclass, *args):
    class Enum(baseclass):
        names = baseclass.names[:]
        helpdict = {}
    Enum.helpdict.update(baseclass.helpdict)
    for arg in args:
        if type(arg) is types.StringType:
            Enum.names.append(arg)
        else:
            Enum.names.append(arg[0])
            if arg[1]:
                Enum.helpdict[arg[0]] = arg[1]
    return Enum

class EnumParameter(parameter.Parameter):
    def __init__(self, name, enumclass, value=None, default=None, tip=None,
                 auxData={}):
        self.enumclass = enumclass
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    def _set(self, value):
        self._value = value
    def set(self, value):
        if value is None or isinstance(value, self.enumclass):
            self._set(value)
            return
        if type(value) is types.StringType and value in self.enumclass.names:
            self._set(self.enumclass(value))
            return
        raise parameter.ParameterMismatch(
            'Invalid Enum value %s.  Choices are: %s' %
            (`value`, self.enumclass.names))
    def clone(self):
        return self.__class__(self.name, self.enumclass, self.value,
                              self.default, self.tip, self.auxData)
    structfmt = '>i'
    structlen = struct.calcsize(structfmt)
    def binaryRepr(self, datafile, value):
        return  struct.pack(EnumParameter.structfmt, len(value.name)) + \
               value.name
    def binaryRead(self, parser):
        b = parser.getBytes(EnumParameter.structlen)
        (length,) = struct.unpack(EnumParameter.structfmt, b)
        return self.enumclass(parser.getBytes(length))
    def classRepr(self):
        return "Enum(%s)" % self.enumclass.__name__
    def valueDesc(self):
        return "An object from the <link linkend='Enum-%s'><classname>%s</classname></link> enumerated class." \
               % (self.enumclass.__name__, self.enumclass.__name__)


class ListOfEnumsParameter(parameter.Parameter):
    def __init__(self, name, enumclasses, value=None, default=None, tip=None,
                 auxData={}):
        ## TODO OPT: Use isinstance here?
        if (type(enumclasses) == types.ListType or
            type(enumclasses) is types.TupleType):
            self.enumclasses = enumclasses
        else:
            self.enumclasses = [enumclasses]
        parameter.Parameter.__init__(self, name, value, default, tip, auxData)
    def _set(self, value):
        self._value = value
    def classnames(self):
        return `[x.__name__ for x in self.enumclasses]`
    def set(self, value):
        if value is None:
            self._set(value)
        else:
            if type(value) is not types.ListType:
                parameter.raiseTypeError(
                    'list of objects from' + `self.classnames()`, value)
            convertedval = []
            for e in value:
                if type(e) is types.StringType: # string representation of enum
                    for ec in self.enumclasses:
                        if e in ec.names:
                            convertedval.append(ec(e))
                            break
                    else:
                        parameter.raiseTypeError(
                            'list of objects from' + `self.classnames()`, value)
                else:                   # not a string
                    for ec in self.enumclasses:
                        if isinstance(e, ec):
                            convertedval.append(e)
                            break
                    else:
                        parameter.raiseTypeError(
                            'list of objects from' + `self.classnames()`, value)
            self._set(convertedval)
    def clone(self):
        return self.__class__(self.name, self.enumclasses, self.value,
                              self.default, self.tip)
        
if __name__ == '__main__':

    class TestEnum(EnumClass('A', 'B', 'C')): pass

    class AnotherEnum(EnumClass('hey', 'B')): pass

    ThirdEnum = EnumClass('1', '2', '3')


    a = TestEnum('A')
    b = TestEnum('B')
    try:
        c = TestEnum('wrong!')
    except ValueError:
        print "couldn't create c!"

    print a
    print b

    hey = AnotherEnum('hey')
    bb = AnotherEnum('B')
    print hey
    print bb

    one = ThirdEnum('1')
    two = ThirdEnum('2')
    One = ThirdEnum('1')
    print one
    print two

    print 'one < two: ', one < two
    print 'one > two: ', one > two
    print 'one == two:', one == two
    print 'one == One:', one == One 
    print 'bb == b:', bb == b
