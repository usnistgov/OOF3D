# -*- python -*-
# $RCSfile: orientationmatrix.py,v $
# $Revision: 1.40.18.4 $
# $Author: langer $
# $Date: 2014/09/17 17:48:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Orientation is another convertible registered type, similar
# to isocijkl.  Orientation can be expressed in terms of various
# angle conventions, all of which get converted to the base
# type, which is a SWIG'd COrientABG object.

# These classes are just wrappers for the COrientation classes, which
# do all the work.  The purpose of the wrappers is to avoid having to
# think about how to make CRegisteredClasses Convertible, and to
# handle the conversion from degrees (used in the UI) to radians (used
# internally in COrientation subclasses).
# TODO 3.1: Use Convertible CRegisteredClasses instead.

# TODO 3.1: Move this file to common/IO or common?

from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.SWIG.common import corientation
import math

FloatParameter = parameter.FloatParameter
FloatRangeParameter = parameter.FloatRangeParameter

# TODO 3.1: Do the *_from_base functions need to check the type of their
# argument?  Some of them, before COrientation, used to accept either
# an EulerAngle or a matrix.

# Base class.  Should be able to answer questions about its values
# in different representations, using the member *instance*'s to_base
# functions.  
class Orientation(registeredclass.ConvertibleRegisteredClass):
    __metaclass__ = utils.PrintableClass
    registry = []
    # Orientation needs a special equality checker, because
    # its value is not a composite Python object, as assumed by
    # RegisteredClass.  TODO 3.1: Is this still needed?
    def __eq__(self, other):
        return other is not None and other.corient==self.corient
    def __ne__(self, other):
        return not self==other
    def to_base(self):
        return self.corient

    tip = "The orientation of a three dimensional object."

    discussion = """<para>
    There are many different ways of describing the orientation of a
    three dimensional object.  <application>OOF1</application> used
    only Euler angles, assuming that everybody used Euler angles, but
    it turns out that not only does everybody not use Euler angles,
    but there are differences of opinion about how Euler angles should
    be defined.  So &oof2; allows you to choose among many different
    ways of defining orientations, some of which are Euler angles, and
    none of which are called Euler angles.  The <link
    linkend='RegisteredClass-Abg'><classname>Abg</classname></link>
    definition is the one used in <application>OOF1</application>.
    </para>"""

    # rotateXY() redefines the reference location by rotating by
    # 'angle' in the xy plane.  This is used to compensate for strange
    # coordinate systems in some EBSD files. 'angle' should be in
    # degrees.
    def rotateXY(self, angle):
        # Redefined in the Bunge and Abg classes to avoid extra
        # conversions between angle representations.

        abg = self.corient.abg()
        # from_base() expects an Orientation, not a COrientation, so
        # we have to convert back to degrees here.  Urgh.
        alpha, beta, gamma = map(math.degrees,
                                 (abg.alpha(), abg.beta(), abg.gamma()))
        newabg = Abg(alpha, beta, gamma+angle)
        reg = self.getRegistration()
        args = reg.from_base(reg, newabg)
        reg.setDefaultParams(args)
        return reg()
        

# Registration object hosts the "call points" for to_base
# routines.  These are used by the GUI when switching types.
class OrientationRegistration(registeredclass.ConvertibleRegistration):
    def __init__(self, name, subclass, ordering,
                 from_base, to_base, params=[], tip=None, discussion=None):
        registeredclass.ConvertibleRegistration.__init__(
            self, name,
            Orientation, subclass,
            ordering,
            from_base=from_base,
            to_base=to_base,
            params=params,
            tip=tip, discussion=discussion)

## The base representation for the ConvertibleRegisteredClass
## mechansim (which is not the same thing as the base class) is the
## Abg subclass.  corient_to_base converts any COrientation subclass
## to an Abg object.

def corient_to_base(corient):
    abg = corient.abg()
    return Abg(*map(math.degrees, (abg.alpha(), abg.beta(), abg.gamma())))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Abg(Orientation):
    def __init__(self, alpha, beta, gamma):
        self.corient = corientation.COrientABG(
            *map(math.radians, (alpha, beta, gamma)))
        # Set the parameters in the registration object.  This is
        # redundant (but harmless) when the object is instanced from
        # the registration.
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
    @staticmethod
    def radians2Degrees(alpha, beta, gamma):
        return map(math.degrees, (alpha, beta, gamma))
    def rotateXY(self, angle):
        return Abg(self.alpha, self.beta, self.gamma+angle)
        

def _abg_to_base(reg, vlist = None):
    vset = vlist or reg.getParamValues()
    return Abg(*vset)

def _abg_from_base(reg, base):
    return [base.alpha, base.beta, base.gamma]

OrientationRegistration(
    'Abg',
    Abg,
    1,
    from_base=_abg_from_base,
    to_base=_abg_to_base,
    params=[FloatRangeParameter('alpha', (0, 180., 0.1), 0.0, ## 'c-axis tilt'
                          tip='second rotation, about the y-axis, in degrees.'),
            FloatRangeParameter('beta', (-180., 180., 0.1), 0.0, ##  c-axis rot.
                          tip='first rotation, about the z-axis, in degrees.'),
            FloatRangeParameter('gamma', (-180., 180., 0.1), 0.0, ## z-axis rot
                          tip='third rotation, about the z-axis, in degrees.')],
    tip='Euler angles (alpha, beta, gamma) are applied: first beta about the z axis, then alpha about the y, and finally gamma about z. This operation brings the crystal axes into coincidence with the lab axes.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/abg.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Goldstein's "X" convention.  This may have some other more
# descriptive name, but I don't know what it is.  Rotations are z,x,z.
class X(Orientation):
    def __init__(self, phi, theta, psi):
        self.phi = phi
        self.theta = theta
        self.psi = psi
        self.corient = corientation.COrientX(
            *map(math.radians, (phi, theta, psi)))
    @staticmethod
    def radians2Degrees(phi, theta, psi):
        return map(math.degrees, (phi, theta, psi))

# vlist should again be an indexable with vlist[0]=phi,
# vlist[1]=theta, vlist[2]=psi.  Converts by way of the matrix.
def _x_to_base(x_reg, vlist=None):
    args = vlist or x_reg.getParamValues()  # (phi, theta, psi)
    return corient_to_base(corientation.COrientX(*map(math.radians, args)))

def _x_from_base(x_reg, base):
    x = base.corient.X()
    return map(math.degrees, (x.phi(), x.theta(), x.psi()))

OrientationRegistration(
    'X',
    X,
    2,
    from_base=_x_from_base,
    to_base=_x_to_base,
    params=[FloatRangeParameter('phi', (-180., 180., 0.1), 0.0,
                              tip="First rotation, about z axis, in degrees."),
            FloatRangeParameter('theta', (0., 180., 0.1), 0.0,
                              tip="Second rotation, about x axis, in degrees."),
            FloatRangeParameter('psi', (-180., 180., 0.1), 0.0,
                              tip="Third rotation, about z axis, in degrees.")],
    tip="Goldstein's X convention for 3D orientations, using rotations which bring the crystal axes into coincidence with the lab axes, in the order z, x, z.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/x.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The "aerodynamic" XYZ convention, with each rotation about a different
# principal axis.  Again the name is from Goldstein.

class XYZ(Orientation):
    def __init__(self, phi, theta, psi):
        self.phi = phi
        self.theta = theta
        self.psi = psi
        self.corient = corientation.COrientXYZ(
            *map(math.radians, (phi, theta, psi)))
    @staticmethod
    def radians2Degrees(phi, theta, psi):
        return map(math.degrees, (phi, theta, psi))

# vlist should again be an indexable with vlist[0]=phi, vlist[1]=theta,
# vlist[2]=phi.  Converts by way of the matrix.
def _xyz_to_base(xyz_reg, vlist=None):
    args = vlist or xyz_reg.getParamValues() # (phi, theta, psi)
    return corient_to_base(corientation.COrientXYZ(*map(math.radians, args)))

def _xyz_from_base(xyz_reg, base):
    xyz = base.corient.XYZ()
    return map(math.degrees, (xyz.phi(), xyz.theta(), xyz.psi()))

OrientationRegistration(
    'XYZ', XYZ, 3,
    from_base=_xyz_from_base,
    to_base=_xyz_to_base,
    params=[FloatRangeParameter('phi', (-180., 180., 0.1), 0.0,
                            tip="Initial rotation about x axis, in degrees."),
            FloatRangeParameter('theta', (0., 180., 0.1), 0.0,
                            tip="Second rotation, about y axis, in degrees."),
            FloatRangeParameter('psi', (-180., 180., 0.1), 0.0,
                            tip="Third rotation, about z axis, in degrees.")],
    tip='The "aerodynamic" XYZ convention for specifying an orientation.  Rotation by phi about x, then theta about y, then psi about z, brings the crystal axes into coincidence with the lab axes.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/xyz.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Quaternions, for two reasons:  Firstly, it's fun.  Secondly,
# if you're going to have the axis-and-angle parametrization, you've
# already done most of the work for the quaternions.

# One result of this is that there is substantial, informally-shared
# structure between the Quaternion and Axis representations.  This
# is the sort of thing that would normally be done by inheritance, but
# isn't, because the "to_base" and "from_base" function are not class
# members, but rather are data in the registration instances.
#   Be aware that _quaternion_to_base and _quaternion_from_matrix
# are also called by _axis_to_base and _axis_from_base (see below). 

class Quaternion(Orientation):
    def __init__(self, e0, e1, e2, e3):
        self.e0 = e0
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.corient = corientation.COrientQuaternion(e0, e1, e2, e3)
    @staticmethod
    def radians2Degrees(e0, e1, e2, e3):
        return e0, e1, e2, e3

# vlist should again be an indexable with vlist[0]=e0, vlist[1]=e1,
# vlist[2]=e2, vlist[3]=e3.
def _quaternion_to_base(quat_reg, vlist=None):
    args = vlist or quat_reg.getParamValues() #(e0, e1, e2, e3) 
    return corient_to_base(corientation.COrientQuaternion(*args))

def _quaternion_from_base(quat_reg, base):
    quat = base.corient.quaternion()
    return [quat.e0(), quat.e1(), quat.e2(), quat.e3()]
    
OrientationRegistration(
    'Quaternion',
    Quaternion,
    5,
    from_base=_quaternion_from_base,
    to_base=_quaternion_to_base,
    params=[FloatParameter('e0', 0.0, tip="Cosine of half the rotation angle.",),
            FloatParameter('e1', 0.0, tip="Rotation axis x-component times sine of half the rotation angle."),
            FloatParameter('e2', 0.0, tip="Rotation axis y-component times sine of half the rotation angle."),
            FloatParameter('e3', 0.0, tip="Rotation axis z-component times sine of half the rotation angle.")],
    tip="The Quaternion representation for 3D orientations.  e0 is the cosine of the half-angle of the rotation, and e1 through e3 are the x, y, and z components of the rotation axis times the sine of the half-angle.  The rotation brings the crystal axes into coincidence with the lab axes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/quaternion.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Axis-and-angle.  Also uses _quaternion_to_base_ and
# _quaternion_from_base, but since they're data, this isn't
# proper (structural) inheritance.


class Axis(Orientation):
    def __init__(self, angle, x, y, z):
        self.angle = angle
        self.x = x
        self.y = y
        self.z = z
        self.corient = corientation.COrientAxis(math.radians(angle), x, y, z)
    @staticmethod
    def radians2Degrees(angle, x, y, z):
        return math.degrees(angle), x, y, z
##    def __repr__(self):
##        return "Axis(angle=%f, x=%f, y=%f, z=%f)" % \
##               (self.angle, self.x, self.y, self.z)

# vlist should again be an indexable with vlist[0]=angle, vlist[1]=x,
# vlist[2]=y, vlist[3]=z.
def _axis_to_base(axis_reg, vlist=None):
    (angle, x, y, z) = vlist or axis_reg.getParamValues()
    return corient_to_base(
        corientation.COrientAxis(math.radians(angle), x, y, z))

def _axis_from_base(axis_reg, base):
    axis = base.corient.axis()
    return [math.degrees(axis.angle()), axis.x(), axis.y(), axis.z()]

OrientationRegistration(
    'Axis',
    Axis,
    4,
    from_base=_axis_from_base,
    to_base=_axis_to_base,
    params=[FloatRangeParameter('angle', (-180., 180., 0.1), 0.0,
                                tip='Rotation angle, in degrees.'),
            FloatParameter('x', 0.0, tip='x component of rotation axis.'),
            FloatParameter('y', 0.0, tip='y component of rotation axis.'),
            FloatParameter('z', 0.0, tip='z component of rotation axis.')],
    tip="Axis and angle representation of a 3D rotation.  The rotation brings the crystal axes into coincidence with the lab axes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/axis.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Rodrigues vector. Another way of describing crystal orientations.
## This form is quite popular in the texture community; it is particularly
## useful to describe fiber-texture and poling in ferroelectrics. --REG
class Rodrigues(Orientation):
    def __init__(self, r1, r2, r3):
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.corient = corientation.COrientRodrigues(r1, r2, r3)
    @staticmethod
    def radians2Degrees(r1, r2, r3):
        return r1, r2, r3

def _rodrigues_to_base(r_reg, vlist=None):
    (r1, r2, r3) = vlist or r_reg.getParamValues()
    return corient_to_base(corientation.COrientRodrigues(r1, r2, r3))

def _rodrigues_from_base(r_reg, base):
    rod = base.corient.rodrigues()
    return [rod.r1(), rod.r2(), rod.r3()]

OrientationRegistration(
    'Rodrigues',
    Rodrigues,
    6,
    from_base=_rodrigues_from_base,
    to_base=_rodrigues_to_base,
    params=[FloatParameter('r1', 0.0,
                           tip="x component of Rodrigues vector."),
            FloatParameter('r2', 0.0,
                           tip="y component of Rodrigues vector."),
            FloatParameter('r3', 0.0,
                           tip="z component of Rodrigues vector.")],
    tip='Rodrigues vector representation for 3D orientations.  The vector points along the axis of the rotation, and its magnitude is the tangent of half the angle of the rotation.  The rotation brings the crystal axes into coincidence with the lab axes.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/rodrigues.xml') )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Another way to specify orientations -- in the usual definitions, the
# rotations take the sample (ie, lab) axes into the crystal axes, and
# they are: phi1 about z, theta about the new x axis, and then phi2
# about the resulting z axis.  This is backwards from the way OOF does
# it, so we build the *transpose* of the matrix you would get from
# those rotations.  In fact, this matrix should just be the transpose
# of the Goldstein X matrix.
class Bunge(Orientation):
    def __init__(self,phi1,theta,phi2):
        self.phi1 = phi1
        self.theta = theta
        self.phi2 = phi2
        self.corient = corientation.COrientBunge(
            *map(math.radians, (phi1, theta, phi2)))
    def rotateXY(self, angle):
        return Bunge(self.phi1 - angle, self.theta, self.phi2)
    @staticmethod
    def radians2Degrees(phi1, theta, phi2):
        return map(math.degrees, (phi1, theta, phi2))

def _bunge_to_base(bunge_reg, vlist=None):
    args = vlist or bunge_reg.getParamValues() # (phi1, theta, phi2)
    return corient_to_base(
        corientation.COrientBunge(*map(math.radians, args)))

def _bunge_from_base(bunge_reg, base):
    bunge = base.corient.bunge()
    return map(math.degrees, (bunge.phi1(), bunge.theta(), bunge.phi2()))

OrientationRegistration(
    'Bunge', Bunge, 7,
    from_base=_bunge_from_base,
    to_base=_bunge_to_base,
    params=[FloatRangeParameter('phi1', (-180., 180., 0.1), 0.0,
                             tip="First rotation, about z axis, in degrees."),
            FloatRangeParameter('theta', (0., 180., 0.1), 0.0,
                             tip="Second rotation, about x axis, in degrees."),
            FloatRangeParameter('phi2', (-180., 180, 0.1), 0.0,
                             tip="Third rotation, about z axis, in degrees.")],
    tip="Bunge angles for defining a rotation which operates on the lab axes, bringing them into coincidence with the crystal axes, in the order z, x, z.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/bunge.xml') )

    
