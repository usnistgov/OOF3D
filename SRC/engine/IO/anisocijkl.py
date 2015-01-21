# -*- python -*-
# $RCSfile: anisocijkl.py,v $
# $Revision: 1.43.18.2 $
# $Author: langer $
# $Date: 2014/04/26 22:57:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Anisotropic Cijkl objects are mostly non-registered non-convertible
# structured types, with the exception of Cubic.


from ooflib.SWIG.engine.property.elasticity import cijkl
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
import struct

FloatParameter = parameter.FloatParameter
Comparable = parameter.Comparable

# Base class.  Should be able to answer questions about its values
# in different representations, using the member registrations'
# to_base and from_base functionality.  This works differently from the
# otherwise-prototypical "Color" class, because the conversion calls
# here are relatively infrequent, so a slightly cleaner structure can
# be used.  This (hopefully) avoids putting conversion code in
# more than one place.
class CubicRank4Tensor(registeredclass.ConvertibleRegisteredClass):
    registry = []
    tip = "Representations of a cubic 4th rank tensor."
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/cubic_rank4.xml')
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        cbase = self.to_base()
        modulus[0,0] = modulus[1,1] = modulus[2,2] = cbase.c11
        modulus[0,1] = modulus[0,2] = modulus[1,2] = cbase.c12
        modulus[3,3] = modulus[4,4] = modulus[5,5] = cbase.c44
        return modulus
        
    
# Base value type for the CubicRank4Tensor.  This is necessary for convertible
# types, because the from_base conversion routine needs to have some
# confidence that it's getting a value it can cope with, which it
# does by type-checking against this type.
class CubicCijklValueBase:
    def __init__(self,c11,c12,c44):
        self.c11 = c11
        self.c12 = c12
        self.c44 = c44
        

# Registration object hosts the "call points" for to_base
# routines.  These are used by the GUI when switching types.
class CubicCijklRegistration(registeredclass.ConvertibleRegistration):
    def __init__(self, name, subclass, ordering,
                 from_base, to_base, params=[], tip=None, discussion=None):
        registeredclass.Registration.__init__(self, name, CubicRank4Tensor,
                                              subclass,
                                              ordering, from_base=from_base,
                                              to_base=to_base, params=params,
                                              tip=tip, discussion=discussion)
##    def getParamValuesAsBase(self):
##        return self.to_base(self)

# Define a special Parameter type so that it can have special widgets
# assigned to it in GUI mode.

class CubicCijklParameter(parameter.ConvertibleRegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.ConvertibleRegisteredParameter.__init__(
            self, name, CubicRank4Tensor, value=value, default=default, tip=tip,
            auxData=auxData)
    def clone(self):
        return CubicCijklParameter(self.name, self.value, self.default,
                                   self.tip)
    def valueDesc(self):
        return "A <link linkend='RegisteredClass-CubicRank4Tensor'><classname>CubicRank4Tensor</classname></link> object."

#########################################################################
#########################################################################

# Conversion for the symmetric matrix representation of the Cijkl
# matrix.  This uses the same internal data representation as
# the base value type, so the to_base and from_base routines
# are conspicuously trivial.

class CubicRank4TensorCij(CubicRank4Tensor):
    def __init__(self, c11, c12, c44):
        # Set the parameters in the registration object.  This is
        # redundant (but harmless) when the object is instanced from
        # the registration.
        self.c11 = c11
        self.c12 = c12
        self.c44 = c44

def _cij_to_base(cijkl_reg, values=None):
    vset = values or cijkl_reg.getParamValues() # This case is trivial.
    return CubicCijklValueBase(c11=vset[0], c12=vset[1], c44=vset[2])

def _cij_from_base(cijkl_reg, base):
    if isinstance(base, CubicCijklValueBase):
        return [base.c11,base.c12,base.c44]

CubicCijklRegistration(
    'Cij',
    CubicRank4TensorCij,
    100,
    from_base=_cij_from_base,
    to_base=_cij_to_base,
    params=[FloatParameter('c11', 10.0, tip=parameter.emptyTipString),
            FloatParameter('c12', 5.0, tip=parameter.emptyTipString),
            FloatParameter('c44', 2.5, tip=parameter.emptyTipString)],
    tip="Explicit representation in terms of tensor components.",
    discussion="""<para>

    <classname>CubicRank4TensorCij</classname> is a rank 4 tensor with
    cubic symmetry.  It is parametrized explicitly by its independent
    components, <varname>c11</varname>, <varname>c12</varname>, and
    <varname>c44</varname>.

    </para>""")



# Lame coefficients for cubic elasticity.
class CubicRank4TensorLame(CubicRank4Tensor):
    def __init__(self, lmbda, mu, aniso):
        self.lmbda = lmbda
        self.mu = mu
        self.aniso = aniso

def _lame_to_base(lame_reg, values=None):
    (lmbda, mu, aniso) = values or lame_reg.getParamValues()
    c11 = lmbda + 2.0*mu
    c12 = lmbda
    c44 = 0.5*(c11-c12)*aniso
    return CubicCijklValueBase(c11=c11, c12=c12, c44=c44)

def _lame_from_base(lame_reg, base):
    if isinstance(base, CubicCijklValueBase):
        lmbda = base.c12
        mu = (base.c11-base.c12)/2.0
        aniso = 2.0*base.c44/(base.c11-base.c12)
        return [lmbda,mu,aniso]

anisotip = "Zener's anisotropy index. (1.0 is isotropic.)"

CubicCijklRegistration(
    'Lame',
    CubicRank4TensorLame,
    101,
    from_base=_lame_from_base,
    to_base=_lame_to_base,
    # parameters are equivalent to default Cij 
    params=[FloatParameter('lmbda', 0.5, tip="lambda."),
            FloatParameter('mu', 0.25, tip=parameter.emptyTipString),
            FloatParameter('aniso', 1.0, tip=anisotip)],
    tip="Cubic rank 4 tensor in terms of Lame coefficients.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/cubic_rank4_lame.xml')
    )


# Young modulus and Poisson ratio.
class CubicRank4TensorEnu(CubicRank4Tensor):
    def __init__(self, young, poisson, aniso):
        self.young = young
        self.poisson = poisson
        self.aniso = aniso

def _enu_to_base(enu_reg, values=None):
    (young, poisson, aniso) = values or enu_reg.getParamValues()
    if poisson == 0.5:
        raise ValueError("poisson=0.5 is pathological.  Values not converted!")
    if poisson == -1.0:
        raise ValueError("poisson=-1 is pathological.  Values not converted!")
    c11 = young*(1.0-poisson)/((1.0+poisson)*(1.0-2.0*poisson))
    c12 = young*poisson/((1.0+poisson)*(1.0-2.0*poisson))
    c44 = 0.5*(c11-c12)*aniso
    return CubicCijklValueBase(c11=c11, c12=c12, c44=c44)

def _enu_from_base(enu_reg, base):
    if isinstance(base, CubicCijklValueBase):
        c11 = base.c11
        c12 = base.c12
        young = ((c11-c12)*(c11+2.0*c12)/(c11+c12))
        poisson = c12/(c11+c12)
        aniso = 2.0*base.c44/(c11-c12)
        return [young, poisson, aniso]

CubicCijklRegistration(
    'E and nu',
    CubicRank4TensorEnu,
    102,
    from_base=_enu_from_base,
    to_base=_enu_to_base,
    # parameters are equivalent to default Cij 
    params=[FloatParameter('young', 2./3., tip="Young's modulus"),
            FloatParameter('poisson', 1./3., tip="Poisson ratio"),
            FloatParameter('aniso',  1.0, tip=anisotip)],
    tip="Cubic rank 4 tensor in terms of Young's modulus and Poisson ratio.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/cubic_rank4_enu.xml')
    )


# Bulk and shear modulus scheme.
class CubicRank4TensorBulkShear(CubicRank4Tensor):
    def __init__(self, bulk, shear, aniso):
        self.bulk = bulk
        self.shear = shear
        self.aniso = aniso

def _bs_to_base(bs_reg, values=None):
    (bulk, shear, aniso) = values or  bs_reg.getParamValues()
    c11 = bulk+(4.0/3.0)*shear
    c12 = bulk-(2.0/3.0)*shear
    c44 = 0.5*(c11-c12)*aniso
    return CubicCijklValueBase(c11=c11, c12=c12, c44=c44)

def _bs_from_base(bs_reg, base):
    if isinstance(base, CubicCijklValueBase):
        bulk = (1.0/3.0)*(base.c11+2.0*base.c12)
        shear = (base.c11-base.c12)/2.0
        aniso = 2.0*base.c44/(base.c11-base.c12)
        return [bulk, shear, aniso]

CubicCijklRegistration(
    'Bulk and Shear',
    CubicRank4TensorBulkShear,
    103,
    from_base=_bs_from_base,
    to_base=_bs_to_base,
    # parameters are equivalent to default Cij 
    params=[FloatParameter('bulk', 2./3., tip='Bulk modulus'),
            FloatParameter('shear', 0.25, tip='Shear modulus'),
            FloatParameter('aniso', 1.0, tip=anisotip)],
    tip="Cubic rank 4 tensor in terms of bulk and shear moduli.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/cubic_rank4_bs.xml')
    )


###########################################################################
###########################################################################

# Other crystallographic symmetries do not have multiple representations
# (yet).  They still have custom types, though, so that there can
# be special matrix-like widgets for them, and so that it is an error
# to attempt to assign outside the allowed variables.

# Because these modulus objects are not registered classes, they need
# explicit reprs and need to be explicitly injected into the main OOF
# namespace.

class HexagonalRank4TensorCij(Comparable):
    def __init__(self,c11,c12,c13,c33,c44):
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c33 = c33
        self.c44 = c44
    def __repr__(self):
        return "HexagonalRank4TensorCij(c11=%s, c12=%s, c13=%s, c33=%s, c44=%s)" % \
               (self.c11, self.c12, self.c13, self.c33, self.c44)
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        modulus[0,0] = modulus[1,1] = self.c11
        modulus[2,2] = self.c33
        modulus[0,1] = self.c12
        modulus[0,2] = modulus[1,2] = self.c13
        modulus[3,3] = modulus[4,4] = self.c44
        modulus[5,5] = 0.5*(self.c11 - self.c12)
        return modulus

utils.OOFdefine('HexagonalRank4TensorCij', HexagonalRank4TensorCij)

class HexagonalCijklParameter(parameter.Parameter):
    types = (HexagonalRank4TensorCij,)
    packfmt = ">5d"
    packsize = struct.calcsize(packfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(HexagonalCijklParameter.packfmt,
                           value.c11, value.c12, value.c13, value.c33,
                           value.c44)
    def binaryRead(self, parser):
        b = parser.getBytes(HexagonalCijklParameter.packsize)
        args = struct.unpack(HexagonalCijklParameter.packfmt, b)
        return HexagonalRank4TensorCij(*args)
    def valueDesc(self):
        return "A <link linkend='Object-HexagonalRank4TensorCij'><classname>HexagonalRank4TensorCij</classname></link> object."

xmlmenudump.XMLObjectDoc(
    'Rank 4 Tensors:HexagonalRank4TensorCij',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/hexagonalrank4.xml'),
    ordering=400)

class TetragonalRank4TensorCij(Comparable):
    def __init__(self,c11,c12,c13,c33,c44,c66,c16):
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c16 = c16
        self.c33 = c33
        self.c44 = c44
        self.c66 = c66
    def __repr__(self):
        return "TetragonalRank4TensorCij(c11=%s, c12=%s, c13=%s, c33=%s, c44=%s, c66=%s, c16=%s)" % \
               (self.c11, self.c12, self.c13, self.c33, self.c44,
                self.c66, self.c16)
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        modulus[0,0] = modulus[1,1] = self.c11
        modulus[0,1] = self.c12
        modulus[0,2] = modulus[1,2] = self.c13
        modulus[2,2] = self.c33
        modulus[3,3] = modulus[4,4] = self.c44
        modulus[5,5] = self.c66
        modulus[0,5] = self.c16
        modulus[1,5] = -self.c16
        return modulus

utils.OOFdefine('TetragonalRank4TensorCij', TetragonalRank4TensorCij)

# Parameter for this class.
class TetragonalCijklParameter(parameter.Parameter):
    types = (TetragonalRank4TensorCij,)
    packfmt = ">7d"
    packsize = struct.calcsize(packfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(TetragonalCijklParameter.packfmt,
                           value.c11, value.c12, value.c13,
                           value.c33, value.c44, value.c66, value.c16)
    def binaryRead(self, parser):
        b = parser.getBytes(TetragonalCijklParameter.packsize)
        args = struct.unpack(TetragonalCijklParameter.packfmt, b)
        return TetragonalRank4TensorCij(*args)
    def valueDesc(self):
        return "A <link linkend='Object-TetragonalRank4TensorCij'><classname>TetragonalRank4TensorCij</classname></link> object."

xmlmenudump.XMLObjectDoc(
    'Rank 4 Tensors:TetragonalRank4TensorCij',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/tetragonalrank4.xml'),
    ordering=401)

class TrigonalARank4TensorCij(Comparable):
    def __init__(self,c11,c12,c13,c33,c44,c14,c15):
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c33 = c33
        self.c44 = c44
        self.c14 = c14
        self.c15 = c15
    def __repr__(self):
        return "TrigonalARank4TensorCij(c11=%s, c12=%s, c13=%s, c33=%s, c44=%s, c14=%s, c15=%s)" % \
               (self.c11, self.c12, self.c13, self.c33, self.c44,
                self.c14, self.c15)
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        modulus[0,0] = modulus[1,1] = self.c11
        modulus[0,1] = self.c12
        modulus[0,2] = modulus[1,2] = self.c13
        modulus[2,2] = self.c33
        modulus[3,3] = modulus[4,4] = self.c44
        modulus[5,5] = 0.5*(self.c11 - self.c12)
        
        modulus[0,3] = self.c14
        modulus[1,3] = -self.c14
        modulus[4,5] = self.c14
        
        modulus[0,4] = self.c15
        modulus[1,4] = -self.c15
        modulus[3,5] = -self.c15
        return modulus


utils.OOFdefine('TrigonalARank4TensorCij', TrigonalARank4TensorCij)

# Parameter for this class.
class TrigonalACijklParameter(parameter.Parameter):
    types = (TrigonalARank4TensorCij,)
    packfmt = ">7d"
    packsize = struct.calcsize(packfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(TrigonalACijklParameter.packfmt,
                           value.c11, value.c12, value.c13,
                           value.c33, value.c44, value.c14, value.c15)
    def binaryRead(self, parser):
        b = parser.getBytes(TrigonalACijklParameter.packsize)
        args = struct.unpack(TrigonalACijklParameter.packfmt, b)
        return TrigonalARank4TensorCij(*args)
    def valueDesc(self):
        return "A <link linkend='Object-TrigonalARank4TensorCij'><classname>TrigonalARank4TensorCij</classname></link> object."

xmlmenudump.XMLObjectDoc(
    'Rank 4 Tensors:TrigonalARank4TensorCij',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/trigonalArank4.xml'),
    ordering=402)


class TrigonalBRank4TensorCij(Comparable):
    def __init__(self,c11,c12,c13,c33,c44,c14):
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c33 = c33
        self.c44 = c44
        self.c14 = c14
    def __repr__(self):
        return "TrigonalBRank4TensorCij(c11=%s, c12=%s, c13=%s, c33=%s, c44=%s, c14=%s)" % \
               (self.c11, self.c12, self.c13, self.c33, self.c44,
                self.c14)
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        modulus[0,0] = modulus[1,1] = self.c11
        modulus[0,1] = self.c12
        modulus[0,2] = modulus[1,2] = self.c13
        modulus[2,2] = self.c33
        modulus[3,3] = modulus[4,4] = self.c44
        modulus[5,5] = 0.5*(self.c11 - self.c12)
        modulus[0,3] = self.c14
        modulus[1,3] = -self.c14
        modulus[4,5] = self.c14
        return modulus

utils.OOFdefine('TrigonalBRank4TensorCij', TrigonalBRank4TensorCij)

# Parameter for this class.
class TrigonalBCijklParameter(parameter.Parameter):
    types = (TrigonalBRank4TensorCij,)
    packfmt = ">dddddd"
    packsize = struct.calcsize(packfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(TrigonalBCijklParameter.packfmt,
                           value.c11, value.c12, value.c13,
                           value.c33, value.c44, value.c14)
    def binaryRead(self, parser):
        b = parser.getBytes(TrigonalBCijklParameter.packsize)
        args = struct.unpack(TrigonalBCijklParameter.packfmt, b)
        return TrigonalBRank4TensorCij(*args) 
    def valueDesc(self):
        return "A <link linkend='Object-TrigonalBRank4TensorCij'><classname>TrigonalBRank4TensorCij</classname></link> object."

xmlmenudump.XMLObjectDoc(
    'Rank 4 Tensors:TrigonalBRank4TensorCij',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/trigonalBrank4.xml'),
    ordering=403)



class OrthorhombicRank4TensorCij(Comparable):
    def __init__(self,c11,c12,c13,c22,c23,c33,c44,c55,c66):
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c22 = c22
        self.c23 = c23
        self.c33 = c33
        self.c44 = c44
        self.c55 = c55
        self.c66 = c66
    def __repr__(self):
        return "OrthorhombicRank4TensorCij(c11=%s, c12=%s, c13=%s, c22=%s, c23=%s, c33=%s, c44=%s, c55=%s, c66=%s)" % \
               (self.c11, self.c12, self.c13, self.c22, self.c23,
                self.c33, self.c44, self.c55, self.c66)
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        modulus[0, 0] = self.c11
        modulus[0, 1] = self.c12
        modulus[0, 2] = self.c13
        modulus[1, 1] = self.c22
        modulus[1, 2] = self.c23
        modulus[2, 2] = self.c33
        modulus[3, 3] = self.c44
        modulus[4, 4] = self.c55
        modulus[5, 5] = self.c66
        return modulus

utils.OOFdefine('OrthorhombicRank4TensorCij', OrthorhombicRank4TensorCij)

# Parameter for this class.
class OrthorhombicCijklParameter(parameter.Parameter):
    types = (OrthorhombicRank4TensorCij,)
    packfmt = ">9d"
    packsize = struct.calcsize(packfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(OrthorhombicCijklParameter.packfmt,
                           value.c11, value.c12, value.c13,
                           value.c22, value.c23, value.c33, 
                           value.c44, value.c55, value.c66)
    def binaryRead(self, parser):
        b = parser.getBytes(OrthorhombicCijklParameter.packsize)
        args = struct.unpack(OrthorhombicCijklParameter.packfmt, b)
        return OrthorhombicRank4TensorCij(*args)
    def valueDesc(self):
        return "A <link linkend='Object-OrthorhombicRank4TensorCij'><classname>OrthorhombicRank4TensorCij</classname></link> object."

xmlmenudump.XMLObjectDoc(
    'Rank 4 Tensors:OrthorhombicRank4TensorCij',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/orthorhombicrank4.xml'),
    ordering=404)
    

class MonoclinicRank4TensorCij(Comparable):
    def __init__(self,c11,c12,c13,c15,c22,c23,c25,c33,c35,c44,c46,c55,c66):
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c15 = c15
        self.c22 = c22
        self.c23 = c23
        self.c25 = c25
        self.c33 = c33
        self.c35 = c35
        self.c44 = c44
        self.c46 = c46
        self.c55 = c55
        self.c66 = c66
    def __repr__(self):
        return "MonoclinicRank4TensorCij(c11=%s, c12=%s, c13=%s, c15=%s, c22=%s, c23=%s, c25=%s, c33=%s, c35=%s, c44=%s, c46=%s, c55=%s, c66=%s)" % \
               (self.c11, self.c12, self.c13, self.c15, self.c22,
                self.c23, self.c25, self.c33, self.c35, self.c44,
                self.c46, self.c55, self.c66)
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        modulus[0, 0] = self.c11
        modulus[0, 1] = self.c12
        modulus[0, 2] = self.c13
        modulus[0, 4] = self.c15
        modulus[1, 1] = self.c22
        modulus[1, 2] = self.c23
        modulus[1, 4] = self.c25
        modulus[2, 2] = self.c33
        modulus[2, 4] = self.c35
        modulus[3, 3] = self.c44
        modulus[3, 5] = self.c46
        modulus[4, 4] = self.c55
        modulus[5, 5] = self.c66
        return modulus

utils.OOFdefine('MonoclinicRank4TensorCij', MonoclinicRank4TensorCij)

# Parameter for this class.
class MonoclinicCijklParameter(parameter.Parameter):
    types = (MonoclinicRank4TensorCij,)
    packfmt = ">13d"
    packsize = struct.calcsize(packfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(MonoclinicCijklParameter.packfmt,
                           value.c11, value.c12, value.c13, value.c15,
                           value.c22, value.c23, value.c25, value.c33,
                           value.c35, value.c44, value.c46, value.c55,
                           value.c66)
    def binaryRead(self, parser):
        b = parser.getBytes(MonoclinicCijklParameter.packsize)
        args = struct.unpack(MonoclinicCijklParameter.packfmt, b)
        return MonoclinicRank4TensorCij(*args)
    def valueDesc(self):
        return "A <link linkend='Object-MonoclinicRank4TensorCij'><classname>MonoclinicRank4TensorCij</classname></link> object."

xmlmenudump.XMLObjectDoc(
    'Rank 4 Tensors:MonoclinicRank4TensorCij',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/monoclinicrank4.xml'),
    ordering=405)


# The general case.
class TriclinicRank4TensorCij(Comparable):
    def __init__(self,c11,c12,c13,c14,c15,c16,c22,c23,c24,c25,c26,
                 c33,c34,c35,c36,c44,c45,c46,c55,c56,c66):
        self.c11 = c11
        self.c12 = c12
        self.c13 = c13
        self.c14 = c14
        self.c15 = c15
        self.c16 = c16
        self.c22 = c22
        self.c23 = c23
        self.c24 = c24
        self.c25 = c25
        self.c26 = c26
        self.c33 = c33
        self.c34 = c34
        self.c35 = c35
        self.c36 = c36
        self.c44 = c44
        self.c45 = c45
        self.c46 = c46
        self.c55 = c55
        self.c56 = c56
        self.c66 = c66
    def __repr__(self):
        return "TriclinicRank4TensorCij(c11=%s, c12=%s, c13=%s, c14=%s, c15=%s, c16=%s, c22=%s, c23=%s, c24=%s, c25=%s, c26=%s, c33=%s, c34=%s, c35=%s, c36=%s, c44=%s, c45=%s, c46=%s, c55=%s, c56=%s, c66=%s)" % \
               (self.c11, self.c12, self.c13, self.c14, self.c15, self.c16,
                self.c22, self.c23, self.c24, self.c25, self.c26,
                self.c33, self.c34, self.c35, self.c36,
                self.c44, self.c45, self.c46, self.c55, self.c56, self.c66)
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        modulus[0,0] = self.c11
        modulus[0,1] = self.c12
        modulus[0,2] = self.c13
        modulus[0,3] = self.c14
        modulus[0,4] = self.c15
        modulus[0,5] = self.c16

        modulus[1,1] = self.c22
        modulus[1,2] = self.c23
        modulus[1,3] = self.c24
        modulus[1,4] = self.c25
        modulus[1,5] = self.c26

        modulus[2,2] = self.c33
        modulus[2,3] = self.c34
        modulus[2,4] = self.c35
        modulus[2,5] = self.c36

        modulus[3,3] = self.c44
        modulus[3,4] = self.c45
        modulus[3,5] = self.c46

        modulus[4,4] = self.c55
        modulus[4,5] = self.c56

        modulus[5,5] = self.c66

        return modulus

utils.OOFdefine('TriclinicRank4TensorCij', TriclinicRank4TensorCij)

# Parameter for this class.
class TriclinicCijklParameter(parameter.Parameter):
    types = (TriclinicRank4TensorCij,)
    packfmt = ">21d"
    packsize = struct.calcsize(packfmt)
    def binaryRepr(self, datafile, value):
        return struct.pack(TriclinicCijklParameter.packfmt,
                           value.c11, value.c12, value.c13, value.c14,
                           value.c15, value.c16, value.c22, value.c23,
                           value.c24, value.c25, value.c26, value.c33,
                           value.c34, value.c35, value.c36, value.c44,
                           value.c45, value.c46, value.c55, value.c56, 
                           value.c66)
    def binaryRead(self, parser):
        b = parser.getBytes(TriclinicCijklParameter.packsize)
        args = struct.unpack(TriclinicCijklParameter.packfmt, b)
        return TriclinicRank4TensorCij(*args) 
    def valueDesc(self):
        return "A <link linkend='Object-TriclinicRank4TensorCij'><classname>TriclinicRank4TensorCij</classname></link> object."


xmlmenudump.XMLObjectDoc(
    'Rank 4 Tensors:TriclinicRank4TensorCij',
    xmlmenudump.loadFile('DISCUSSIONS/engine/object/triclinicrank4.xml'),
    ordering=406)
