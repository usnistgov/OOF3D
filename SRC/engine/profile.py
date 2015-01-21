# -*- python -*-
# $RCSfile: profile.py,v $
# $Revision: 1.76.10.4 $
# $Author: fyc $
# $Date: 2014/07/28 22:15:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import profilefunction
import string, types, struct


# Object for aggregating location information for boundaries. 
# All profile __call__ methods take one of these as an argument.

# Time is included here, but handled differently from the spatial
# data, because the spatial data can be cached, being a function of
# the geometry of the boundary, but the time data varies more rapidly.
# Setting the time is optional, it defaults to t=0.
class Location:
    def __init__(self, position, normal=None,
                 index=None, s=None, alpha=None, time=0):
        self.position = position # Expect a Coord or Point object.
        self.normal = normal
        self.index = index
        self.distance = s
        self.fraction = alpha
        self.time = time
    def set_time(self, time):
        self.time = time
    def __repr__(self):
        result = "Location("
        attrlist = []
        for s in ['position', 'normal', 'index',
                  'distance', 'fraction', 'time']:
            val = getattr(self, s)
            if val is not None:
                attrlist.append("%s=%s" % (s, `val`) )
        result += string.join(attrlist, ", ") + ")"
        return result
                                
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Profile(registeredclass.RegisteredClass):
    # registry is in intermediate derived classes
    def __init__(self):
        self._name = None
        self.conditions = []

    # Why is object identity used for comparison?
    def __eq__(self, other):
        return id(self)==id(other)

    # Separate equivalence function, to identify functional sameness.
    # This sense of profile equivalence does not depend on which
    # conditions they are applied to, or their names, only on their
    # class and function.  Should be implemented in the subclasses.
    def equiv(self, other):
        return False
        
    # Cloning works via the registration, which means it resets the
    # default parameters.  This is probably harmless.
    def clone(self):
        self.setDefaultParams()
        return self.getRegistration()() # Retrieve and run the registration.

    def isTimeDependent(self):
        return False

    def timeDerivative(self, location):
        return 0.0

    def timeDerivative2(self, location):
        return 0.0

    def addCondition(self, condition):
        self.conditions.append(condition)

    def removeCondition(self, condition):
        self.conditions.remove(condition)

# Actual concrete Profile classes must be derived from one of
# ProfileX, ProfileXT, or ProfileXTd, as well as from Profile.
# ProfileX, etc, aren't derived from Profile so that the concrete
# Profile subclasses can share code without creating messy multiple
# inheritance relationships.

#  Space-dependent profiles.

class ProfileX(object):
    tip="Space-dependent boundary condition profiles."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/profilex.xml')
    registry = []

# Space- and time-dependent profiles.

class ProfileXT(object):
    tip="Space- and time-dependent boundary condition profiles."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/profilext.xml')
    registry = []

# Space- and time-dependent profiles, for which time derivative
# information is provided.

class ProfileXTd(object):
    tip="Space- and time-dependent boundary condition profiles, with derivatives."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/profilextd.xml')
    registry = []

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class _ContinuumProfileX(Profile):
    def __init__(self, function):
        self.function = function
        Profile.__init__(self)
    def funcargs(self, location):
        if config.dimension() == 2:
            if location.normal is not None:
                nx = location.normal[0]
                ny = location.normal[1]
            else:
                nx = ny = None
            return (location.position[0],
                    location.position[1],
                    nx,
                    ny,
                    location.index,
                    location.distance,
                    location.fraction)
        else:                   # 3D
            if location.normal is not None:
                nx = location.normal[0]
                ny = location.normal[1]
                nz = location.normal[2]
            else:
                nx = ny = nz = None
            return (location.position[0],
                    location.position[1],
                    location.position[2],
                    nx,
                    ny,
                    nz, 
                    location.index)
    def __call__(self, location):
        return self.function(*self.funcargs(location))
    # Output.
    def description(self):
        return `self.function`
    def equiv(self,other):
        return (other.__class__==self.__class__ and
                self.function == other.function)


class _ContinuumProfileXT(_ContinuumProfileX):
    def __init__(self, function):
        _ContinuumProfileX.__init__(self, function)
        self._timeDependent = function.dependsOn('t')

    # Convert a Location object into a tuple of arguments for a
    # Profile call.
    def funcargs(self, location):
        if config.dimension() == 2:
            if location.normal is not None:
                nx = location.normal[0]
                ny = location.normal[1]
            else:
                nx = ny = None
            return (location.position[0],
                    location.position[1],
                    location.time,
                    nx,
                    ny,
                    location.index,
                    location.distance,
                    location.fraction)
        else:                   # 3D
            if location.normal is not None:
                nx = location.normal[0]
                ny = location.normal[1]
                nz = location.normal[2]
            else:
                nx = ny = nz = None
            return (location.position[0],
                    location.position[1],
                    location.position[2],
                    location.time,
                    nx,
                    ny,
                    nz,
                    location.index)

    def isTimeDependent(self):
        return self._timeDependent

class _ContinuumProfileXTd(_ContinuumProfileXT):
    def __init__(self, function, timeDerivative, timeDerivative2):
        self.timeDerivative = timeDerivative
        self.timeDerivative2 = timeDerivative2
        _ContinuumProfileXT.__init__(self, function)

    def evalTimeDerivative(self, location):
        return self.timeDerivative(*self.funcargs(location))

    def evalTimeDerivative2(self, location):
        return self.timeDerivative2(*self.funcargs(location))
    
    def equiv(self,other):
        return (other.__class__==self.__class__ and
                (self.function==other.function and
                 self.timeDerivative == other.timeDerivative and
                 self.timeDerivative2 == other.timeDerivative2))

# This class is called "ContinuumProfile" instead of
# "ContinuumProfileX" for backwards compatibility.

class ContinuumProfile(ProfileX, _ContinuumProfileX):
    pass
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

if config.dimension() == 2:
    tipstr = "A function of x, y, nx, ny, i, s, and/or alpha."
else:
    tipstr = "A function of x, y, z, nx, ny, nz, and/or i."

registeredclass.Registration(
    "Continuum Profile",
    ProfileX,
    ContinuumProfile,
    ordering=2,
    params=[
        profilefunction.ProfileFunctionXParameter(
            "function",
            value=profilefunction.ProfileFunctionX("0.0"),
            tip=tipstr)
        ],
    tip="Boundary condition is an arbitrary function of position.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/continuumprofilex.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ContinuumProfileXT(ProfileXT, _ContinuumProfileXT):
    pass

if config.dimension() == 2:
    tipstr = "A function of x, y, nx, ny, i, s, alpha, and/or t."
else:
    tipstr = "A function of x, y, z, ny, ny, nz, and/or i."

registeredclass.Registration(
    "Continuum Profile",
    ProfileXT,
    ContinuumProfileXT,
    ordering=2,
    params=[
        profilefunction.ProfileFunctionXTParameter(
            "function",
            value=profilefunction.ProfileFunctionXT("0.0"),
            tip=tipstr)
        ],
    tip="Boundary condition is arbitrary function of position and time.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/continuumprofilext.xml') 
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ContinuumProfileXTd(ProfileXTd, _ContinuumProfileXTd):
    pass

if config.dimension() == 2:
    profargs = "x, y, nx, ny, i, s, alpha, and/or t"
else:
    profargs = "x, y, z, nx, ny, nz, i, and/or t"

registeredclass.Registration(
    "Continuum Profile",
    ProfileXTd,
    ContinuumProfileXTd,
    ordering=2,
    params=[
        profilefunction.ProfileFunctionXTParameter(
            "function",
            value=profilefunction.ProfileFunctionXT("0.0"),
            tip="A function of %s." % profargs),
        profilefunction.ProfileFunctionXTParameter(
            "timeDerivative",
            value=profilefunction.ProfileFunctionXT("0.0"),
            tip= "The time derivative of the profile function,"
            " as a function of %s." % profargs),
        profilefunction.ProfileFunctionXTParameter(
            "timeDerivative2",
            value=profilefunction.ProfileFunctionXT("0.0"),
            tip="The second time derivative of the profile function,"
            " as a function of %s." % profargs)
        ],
    tip="Boundary condition is arbitrary function of position and time.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/continuumprofilextd.xml') 
    )
   

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Subclasses for common special cases.

class ConstantProfile(Profile, ProfileX, ProfileXT, ProfileXTd):
    def __init__(self, value):
        self.value = value 
        Profile.__init__(self)

    # Caller will provide "location", but we can discard it.
    def __call__(self, location):
        return self.value

    def equiv(self,other):
        if self.__class__==other.__class__:
            if self.value==other.value:
                return 1
        return 0
    
    def description(self):
        return `self.value`
    
    def __repr__(self):
        return "ConstantProfile(value=%s)" % `self.value`


registeredclass.Registration(
    "Constant Profile",
    (ProfileX, ProfileXT, ProfileXTd),
    ConstantProfile,
    ordering=0,
    params=[parameter.FloatParameter("value", 0.0, 
                                     tip="Value of this profile.")],
    tip="Boundary condition has a constant value.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/constantprofile.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class LinearProfile(Profile, ProfileX, ProfileXT, ProfileXTd):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        Profile.__init__(self)

    def __call__(self, location):
        return location.fraction*(self.end-self.start)+self.start

    def equiv(self, other):
        if self.__class__==other.__class__:
            if self.start==other.start and self.end==other.end:
                return 1
        return 0

    def description(self):
        return "[%s->%s]" % (`self.start`, `self.end`)
##    def __repr__(self):
##        return "LinearProfile(start=%s, end=%s)" % (`self.start`, `self.end`)
        

registeredclass.TwoDOnlyRegistration(
    "Linear Profile",
    (ProfileX, ProfileXT, ProfileXTd),
    LinearProfile,
    ordering=1,
    params=[parameter.FloatParameter("start", 1.0, 
                                     tip="Start value of this profile."),
            parameter.FloatParameter("end", 1.0, 
                                     tip="End value of this profile.")],
    tip="Boundary condition is a linear function of arclength.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/linearprofile.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# ProfileSet object -- a Profile work-alike which is a container
# for one or more profiles.  __call__ method should return a
# tuple of results.  Supports a profile-like __call__ method,
# as well as unpack and descriptor, allowing it to sub for an
# actual profile in a NeumannBC.

# Currently only supports ProfileXT.  If other types of Profiles are
# required, there will have to be other varieties of FluxProfileSet.

# TODO 3.1: 3D profiles may have more components in general, so this
# object will probably be extended.  It will probably become more
# desirable at that point to make multicomponent profiles
# independently save- and loadable.

class FluxProfileSet:
    def __init__(self, profile_list):
        self.data = profile_list
    def __call__(self, location):
        return tuple([x(location) for x in self.data])
    def __len__(self):
        return len(self.data)
    def unpack(self):
        return self
    def get_profiles(self):
        return self.data[:]
    def addCondition(self, condition):
        for p in self.data:
            p.addCondition(condition)
    def removeCondition(self, condition):
        for p in self.data:
            p.removeCondition(condition)
    def isTimeDependent(self):
        for p in self.data:
            if p.isTimeDependent():
                return True
        return False
    def description(self):
        return "(%s)" % string.join([x.description() for x in self.data],", ")
    def __repr__(self):
        # The FluxProfileSetParameter accepts lists of Profiles or a
        # single Profile, so there's no need to write out
        # 'FluxProfileSet([<profiles>])'
        if len(self) == 1:
            return `self.data[0]`
        else:
            return `self.data`

utils.OOFdefine('FluxProfileSet', FluxProfileSet)

class FluxProfileSetParameter(parameter.Parameter):
    def checker(self, x):
        # A single ProfileXT or a FluxProfileSet is allowed
        if isinstance(x, ProfileXT) or isinstance(x, FluxProfileSet):
            return
        # A list or tuple of Profiles is allowed
        if type(x) in (types.ListType, types.TupleType):
            for y in x:
                if not isinstance(y, ProfileXT):
                    parameter.raiseTypeError('List or tuple of '+ type(y),
                                             'List of Profiles')
        parameter.raiseTypeError(type(x), 'List of Profiles, or FluxProfileSet')

    def set(self, value):
        if isinstance(value, FluxProfileSet):
            self._value = value
        elif type(value) in (types.ListType, types.TupleType):
            self._value = FluxProfileSet(value)
        elif isinstance(value, Profile):
            self._value = FluxProfileSet([value])
        else:
            raise parameter.ParameterMismatch(
                'Got ' + `value` + ' for Parameter ' + self.name)

    def binaryRepr(self, datafile, value):
        n = len(value)
        strs = [struct.pack(">i",n)]
        for p in value.get_profiles():
            strs.append(p.binaryRepr(datafile))
        return string.join(strs, "")
    
    def binaryRead(self, parser):
        b = parser.getBytes(struct.calcsize(">i"))
        (length,) = struct.unpack(">i",b)
        proflist = [None]*length
        for i in range(length):
            proflist[i]=registeredclass.binaryReadRegClass(
                parser, ProfileXT.registry)
        return FluxProfileSet(proflist)

    def valueDesc(self):
        return "A <xref linkend='Object-FluxProfileSet'/> object, or a <link linkend='Object-list'>list</link> of <link linkend='RegisteredClass-ProfileXT'><classname>ProfileXTs</classname></link>, or a single <classname>ProfileXT</classname>."

xmlmenudump.XMLObjectDoc(
    'FluxProfileSet',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/fluxprofileset.xml'))
