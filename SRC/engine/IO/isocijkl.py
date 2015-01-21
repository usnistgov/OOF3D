# -*- python -*-
# $RCSfile: isocijkl.py,v $
# $Revision: 1.30.18.2 $
# $Author: langer $
# $Date: 2014/04/26 22:57:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# The IsoCijkl registered-class hierarchy.  IsoCijkl hierarchy members
# are convertible registered class objects, which provide access to the
# various different ways of parametrizing an isotropic fourth-rank
# index-exchange-symmetric tensor in three dimensions.

from ooflib.SWIG.engine.property.elasticity import cijkl
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
FloatParameter = parameter.FloatParameter


# Base class.  Should be able to answer questions about its values
# in different representations, using the member *instance*'s to_base
# functions.  These should use the code from the registration's
# to_base and from_base routines, but operate on the attributes of the
# Cijkl instance, and not the default parameters.  These are used
# by the properties internally to set their Cijkl objects for
# computation.
class IsotropicRank4Tensor(registeredclass.ConvertibleRegisteredClass):
    registry = []
    tip = "Representations of an isotropic 4th rank tensor."
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/isotropic_rank4.xml')
    def tensorForm(self):
        modulus = cijkl.Cijkl()
        ibase = self.to_base()
        modulus[0,0] = modulus[1,1] = modulus[2,2] = ibase.c11
        modulus[0,1] = modulus[0,2] = modulus[1,2] = ibase.c12
        modulus[3,3] = modulus[4,4] = modulus[5,5] = 0.5*(ibase.c11-ibase.c12)
        return modulus

# base value type for the IsotropicRank4Tensor.  This is necessary for
# convertible types, because the from_base conversion routine needs to
# have some confidence that it's getting a value it can cope with,
# which it does by type-checking against this type.
class IsoCijklValueBase:
    def __init__(self,c11,c12):
        self.c11 = c11
        self.c12 = c12
    def __repr__(self):
        return "IsoCijklValueBase(c11=%s, c12=%s)" % (self.c11, self.c12)


# Registration object hosts the "call points" for to_base
# routines.  These are used by the GUI when switching types.
class IsoCijklRegistration(registeredclass.ConvertibleRegistration):
    def __init__(self, name, subclass, ordering,
                 from_base, to_base, params=[], tip=None, discussion=None):
        registeredclass.Registration.__init__(self, name, IsotropicRank4Tensor,
                                              subclass,
                                              ordering, from_base=from_base,
                                              to_base=to_base, params=params,
                                              tip=tip, discussion=discussion)
##    def getParamValuesAsBase(self):
##        return self.to_base(self)

    

#########################################################################
#########################################################################

# Conversion for the symmetric matrix representation of the Cijkl
# matrix.  Same internal data representation as the base value type.

class IsotropicRank4TensorCij(IsotropicRank4Tensor):
    def __init__(self, c11, c12):
        # Set the parameters in the registration object.  This is
        # redundant (but harmless) when the object is instanced from
        # the registration.
        self.c11 = c11
        self.c12 = c12

# vlist, if provided, should be an indexable with vlist[0]=c11,
# vlist[1]=c12.  
def _cij_to_base(cijkl_reg, vlist = None):
    vset = vlist or cijkl_reg.getParamValues() # Gets c11 and c12.
    return IsoCijklValueBase(c11=vset[0], c12=vset[1])

def _cij_from_base(cijkl_reg, base):
    if isinstance(base, IsoCijklValueBase):
        return [base.c11,base.c12]

IsoCijklRegistration(
    'Cij',
    IsotropicRank4TensorCij,
    100,
    from_base=_cij_from_base,
    to_base=_cij_to_base,
    params=[FloatParameter('c11', 10.0, tip=parameter.emptyTipString),
            FloatParameter('c12', 5.0, tip=parameter.emptyTipString)],
    tip="Explicit representation in terms of tensor components.",
    discussion="""<para>
    <classname>IsotropicRank4TensorCij</classname> is a rank 4 tensor
    with isotropic symmetry.  It is parametrized by its two
    independent components, <varname>c11</varname> and
    <varname>c12</varname>.
    </para>""")


###########################################################################
###########################################################################

# Lame coefficients for isotropic elasticity.
class IsotropicRank4TensorLame(IsotropicRank4Tensor):
    def __init__(self, lmbda, mu):
        self.lmbda = lmbda
        self.mu = mu

# vlist should again be an indexable with vlist[0]=lmbda, vlist[1]=mu
def _lame_to_base(lame_reg, vlist=None):
    (lmbda, mu) = vlist or lame_reg.getParamValues()
    c11 = lmbda + 2.0*mu
    c12 = lmbda
    return IsoCijklValueBase(c11=c11, c12=c12)

def _lame_from_base(lame_reg, base):
    if isinstance(base, IsoCijklValueBase):
        lmbda = base.c12
        mu = (base.c11-base.c12)/2.0
        return [lmbda,mu]

IsoCijklRegistration(
    'Lame',
    IsotropicRank4TensorLame,
    101,
    from_base=_lame_from_base,
    to_base=_lame_to_base,
    # initial values of the parameters are equivalent to Cij's initial values
    params=[FloatParameter('lmbda', 0.5, tip='Lambda.'),
            FloatParameter('mu', 0.25, tip=parameter.emptyTipString)],
    tip="Isotropic rank 4 tensor in terms of Lame coefficients.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/isotropic_rank4_lame.xml')
    )


###########################################################################
###########################################################################

# Young modulus and Poisson ratio.
class IsotropicRank4TensorEnu(IsotropicRank4Tensor):
    def __init__(self, young, poisson):
        self.young = young
        self.poisson = poisson

# vlist, if provided, is indexable.
def _enu_to_base(enu_reg, vlist=None):
    (young, poisson) = vlist or enu_reg.getParamValues()
    if poisson == 0.5:
        raise ValueError("poisson=0.5 is pathological.  Values not converted!")
    if poisson == -1.0:
        raise ValueError("poisson=-1 is pathological.  Values not converted!")
    c11 = young*(1.0-poisson)/((1.0+poisson)*(1.0-2.0*poisson))
    c12 = young*poisson/((1.0+poisson)*(1.0-2.0*poisson))
        
    return IsoCijklValueBase(c11=c11, c12=c12)

def _enu_from_base(enu_reg, base):
    if isinstance(base, IsoCijklValueBase):
        c11 = base.c11
        c12 = base.c12
        young = ((c11-c12)*(c11+2.0*c12)/(c11+c12))
        poisson = c12/(c11+c12)
        return [young, poisson]

IsoCijklRegistration(
    'E and nu',
    IsotropicRank4TensorEnu,
    102, from_base=_enu_from_base,
    to_base=_enu_to_base,
    # initial values of the parameters are equivalent to Cij's initial values
    params=[FloatParameter('young', 2./3., tip="Young's modulus."),
            FloatParameter('poisson', 1./3., tip="Poisson's ratio.")],
    tip="Isotropic rank 4 tensor in terms of Young's modulus and Poisson's ratio.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/reg/isotropic_rank4_enu.xml"))

##########################################################################
##########################################################################

# Bulk and shear modulus scheme.
class IsotropicRank4TensorBulkShear(IsotropicRank4Tensor):
    def __init__(self, bulk, shear):
        self.bulk = bulk
        self.shear = shear

def _bs_to_base(bs_reg, vlist=None):
    (bulk, shear) = vlist or bs_reg.getParamValues()
    c11 = bulk+(4.0/3.0)*shear
    c12 = bulk-(2.0/3.0)*shear
    return IsoCijklValueBase(c11=c11, c12=c12)

def _bs_from_base(bs_reg, base):
    if isinstance(base, IsoCijklValueBase):
        bulk = (1.0/3.0)*(base.c11+2.0*base.c12)
        shear = (base.c11-base.c12)/2.0
        return [bulk, shear]

IsoCijklRegistration(
    'Bulk and Shear',
    IsotropicRank4TensorBulkShear,
    103,
    from_base=_bs_from_base,
    to_base=_bs_to_base,
    # initial values of the parameters are equivalent to Cij's initial values
    params=[FloatParameter('bulk', 2./3., tip='Bulk modulus.'),
            FloatParameter('shear', 0.25, tip='Shear modulus.')],
    tip='Isotropic rank 4 tensor in terms of bulk and shear moduli.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/isotropic_rank4_bs.xml')
    )

###########################################################################
###########################################################################

# Define a special Parameter type so that it can have special widgets
# assigned to it in GUI mode.

class IsotropicCijklParameter(parameter.ConvertibleRegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.ConvertibleRegisteredParameter.__init__(
            self, name, IsotropicRank4Tensor, value=value, default=default,
            tip=tip, auxData=auxData)
    def clone(self):
        return IsotropicCijklParameter(self.name, self.value,
                                             self.default, self.tip)

######################

