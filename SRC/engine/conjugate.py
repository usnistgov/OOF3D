# -*- python -*-
# $RCSfile: conjugate.py,v $
# $Revision: 1.21.2.2 $
# $Author: langer $
# $Date: 2013/11/08 20:43:13 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import config
from ooflib.SWIG.engine import cconjugate
from ooflib.SWIG.engine import material
from ooflib.SWIG.engine import fieldindex
from ooflib.common import debug
from ooflib.engine import propertyregistration
from ooflib.engine import symstate

FieldIndexPtr = fieldindex.FieldIndexPtr

# It is not possible to remove a ConjugatePair object from the list.
# This is OK, since the conjugate pair objects express simple facts
# about the relevant fields, equations, and property categories.

class ConjugatePairObj(cconjugate.CConjugatePair):
    def __init__(self, name, eqn, eqncomp, field, fieldcomp):
        self.name = name
        cconjugate.CConjugatePair.__init__(self, eqn, eqncomp, field, fieldcomp)
    def get_name(self):
        return self.name
    def __hash__(self):
        return (hash(self.name) ^ hash(self.get_equation()) ^
                hash(self.get_equation_component()) ^
                hash(self.get_field()) ^ hash(self.get_field_component()))
                
    

class ListOfConjugatePairs:
    def __init__(self):
        self.pairs = []
        self.lock = lock.SLock()

    def add(self, conjpair):
        self.lock.acquire()
        try:
            if conjpair not in self.pairs:
                self.pairs.append(conjpair)
        finally:
            self.lock.release()

    # There is no removal capability for this list.  The reason is
    # that there's no point -- there does not exist a scenario where
    # removing some conjugacy data helps you in any way.  If you're
    # using a bunch of exciting and strange new properties, then you
    # aren't using the regular ones, and the associated conjugacy data
    # will not be relevant, so there's no point in removing it.  If
    # you are using properties of the given type, then the conjugacy
    # data is correct.  If you have additional conjugacy data which
    # conflicts with it, this indicates a real inability to symmetrize
    # the problem, so the inconsistencies in the list reflect a real
    # physical inconsistency in the set-up of the problem.  This may
    # or may not be an error, but in any case, it is correct for this
    # list to report it.

    
    def relevant_property(self, property, pair):
        return property.is_property_type(pair.get_name())
    
    def sanity_check(self, relevant_pairs):
        # For a given list of properties, make sure that no field maps
        # to more than one equation, and vice versa.  Does not check
        # for completeness, some equations or fields may be unmapped
        # and the sanity_check will still pass.

        self.lock.acquire()
        try:
            # Loop over pairs of pairs.  If there are conflicts, in
            # that a field is conjugate to multiple equations or vice
            # versa, then the sanity check fails. 
            for i in range(len(relevant_pairs)):
                cpair1 = relevant_pairs[i]
                for j in range(i + 1, len(relevant_pairs)):
                    cpair2 = relevant_pairs[j]
                    # If equations match but fields differ, we are not sane.
                    if cpair1.get_equation() == cpair2.get_equation() \
                           and cpair1.get_equation_component() == \
                           cpair2.get_equation_component():
                        if cpair1.get_field() != cpair2.get_field() \
                               or cpair1.get_field_component() != \
                               cpair2.get_field_component():
                            return False
                    # Likewise, if fields match but equations differ,
                    # we are equally insane.
                    if cpair1.get_field()==cpair2.get_field() \
                       and cpair1.get_field_component() == \
                       cpair2.get_field_component():
                        if cpair1.get_equation() != cpair2.get_equation() \
                           or cpair1.get_equation_component() != \
                           cpair2.get_equation_component():
                            return False
                        
        finally:
            self.lock.release()
        return True

    def find_equation_mapping(self, subpctxt):
        self.lock.acquire()
        try:
            subproblem = subpctxt.getObject()
            subproblem.set_equation_mapping(find_relevant_pairs(subpctxt))
        finally:
            self.lock.release()

listofconjugatepairs = ListOfConjugatePairs()

######################################

def conjugatePair(name, equation, eqncomp, field, fieldcomp):
    # eqncomp and fieldcomp can either be a single FieldIndex object,
    # or a list of them.  The lists must have the same length.
    if isinstance(eqncomp, FieldIndexPtr):
        eqncomp = [eqncomp]
    if isinstance(fieldcomp, FieldIndexPtr):
        fieldcomp = [fieldcomp]
    if len(eqncomp) != len(fieldcomp):
        raise ooferror.ErrPyProgrammingError(
            "Bad index specification in conjugatePair")
    for (ecomp, fcomp) in zip(eqncomp, fieldcomp):
        listofconjugatepairs.add(
            ConjugatePairObj(name, equation, ecomp, field, fcomp))

######################################

def find_relevant_pairs(subpcontext):
    materials = subpcontext.getObject().getMaterials()
    relevant_pairs = set()
    for matter in materials:
        for property in matter.properties():
            p_reg = property.registration()
            for pair in listofconjugatepairs.pairs:
                if listofconjugatepairs.relevant_property(p_reg, pair):
                    relevant_pairs.add(pair)
    return list(relevant_pairs)

def check_symmetry(subpName, *args):
    # Switchboard callback for "equation [de]activated" and "field
    # [de]activated".  Also called from the MaterialMSPlugIn, so it
    # gets run when the properties of a material in a mesh are
    # changed.  Also an indirect callback for "materials changed in
    # microstructure", see below.  subpName can be a colon-separated
    # string, or a list of strings.

    from ooflib.engine import subproblemcontext
    subpctxt = subproblemcontext.subproblems[subpName]
    subp = subpctxt.getObject()
    ms = subpctxt.getMicrostructure()

    # The matrix_symmetry_* objects in the SubProblemContext are
    # symstate.SymState instances.  Once they've been set to
    # "ASYMMETRIC" they can't be set to "SYMMETRIC" or "INCONSISTENT"
    # until they've been explicitly reset, which sets them to
    # "INCONSISTENT".
    subpctxt.matrix_symmetry_K.reset()
    subpctxt.matrix_symmetry_C.reset()
    subpctxt.matrix_symmetry_M.reset()

    # See if the Properties are explicitly asymmetric.
    materials = subpctxt.getObject().getMaterials()
    for m in materials:
        if (subpctxt.matrix_symmetry_K != symstate.ASYMMETRIC and
            not m.is_symmetric_K(subpctxt)):
            subpctxt.matrix_symmetry_K.set_asymmetric()
        if (subpctxt.matrix_symmetry_C != symstate.ASYMMETRIC and
            not m.is_symmetric_C(subpctxt)):
            subpctxt.matrix_symmetry_C.set_asymmetric()
        if (subpctxt.matrix_symmetry_M != symstate.ASYMMETRIC and
            not m.is_symmetric_M(subpctxt)):
            subpctxt.matrix_symmetry_M.set_asymmetric()

    relevant_pairs = find_relevant_pairs(subpctxt)

    # See if conjugacy data is missing for an equation.  If it is, we
    # can't construct the mappings that symmetrize the equations, so
    # we have to treat them as asymmetric.  The reason for checking
    # equations rather than fields here is that equations are the
    # things that actually get remapped in the mesh, so the process is
    # more sensitive to equation-counting errors.  Since a symmetric
    # matrix must have fields corresponding to equations, checking
    # fields should be equivalent.  There is, however, no reason to do
    # both.
    meqlist = subp.all_equations()
    for eq in meqlist:
        for p in relevant_pairs:
            if p.get_equation()==eq:
                break
        else:
            subpctxt.matrix_symmetry_K.set_asymmetric()
            subpctxt.matrix_symmetry_C.set_asymmetric()
            subpctxt.matrix_symmetry_M.set_asymmetric()
            return

    # If there are no equations, or no conjugate pairs, then our
    # symmetry state is, by fiat, inconsistent.  Sophomoric arguments
    # about the symmetry of a size-zero matrix, or trees falling in
    # forests, are not admissible here.
    if len(meqlist)==0 or len(relevant_pairs)==0:
        subpctxt.matrix_symmetry_K.set_inconsistent()
        subpctxt.matrix_symmetry_C.set_inconsistent()
        subpctxt.matrix_symmetry_M.set_inconsistent()
        return

    # If we've gotten to here the equation list is complete.  If the
    # conjugate pair set is consistent, a matrix not already flagged
    # as asymmetric is symmetric.  If the conjugate pair set is
    # inconsistent the equation mapping must not be attempted.
    if listofconjugatepairs.sanity_check(relevant_pairs):
        subpctxt.matrix_symmetry_K.set_symmetric()
        subpctxt.matrix_symmetry_C.set_symmetric()
        subpctxt.matrix_symmetry_M.set_symmetric()
    else:
        subpctxt.matrix_symmetry_K.set_inconsistent()
        subpctxt.matrix_symmetry_C.set_inconsistent()
        subpctxt.matrix_symmetry_M.set_inconsistent()


# Direct callback for the "mesh changed" signal.
def _meshChangedCB(mesh):
    meshpath = mesh.path()
    from ooflib.engine import subproblemcontext
    subppaths = subproblemcontext.subproblems.keys(base=meshpath)
    # subppaths is a list of paths.  Each path is a list containing a
    # single name, which is the path to the subproblem relative to the
    # mesh.
    for subppath in subppaths:
        check_symmetry(meshpath+":"+subppath[0])

switchboard.requestCallback("mesh changed", _meshChangedCB)
    
switchboard.requestCallback("equation activated", check_symmetry)
switchboard.requestCallback("equation deactivated", check_symmetry)

switchboard.requestCallback("field activated", check_symmetry)
switchboard.requestCallback("field deactivated", check_symmetry)

