# -*- python -*-
# $RCSfile: plasticity.py,v $
# $Revision: 1.43.2.3 $
# $Author: fyc $
# $Date: 2014/07/31 21:00:01 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Prototype plasticity property, primarily for figuring out what
# the requirements on the solver ought to be to make plasticity
# work.
#   First cut:  Perfect plasticity, assuming von Mises yield
# condition.
#   Second cut: Just subtracts the nodal plastic strain field.


from ooflib.SWIG.common import config
from ooflib.SWIG.common import smallmatrix
from ooflib.SWIG.engine import field
from ooflib.SWIG.engine import fieldindex
from ooflib.SWIG.engine import pypropertywrapper 
from ooflib.SWIG.engine import symmmatrix
from ooflib.SWIG.engine.property.elasticity import cijkl 
from ooflib.common.IO import parameter
from ooflib.engine import propertyregistration
from ooflib.engine import problem
import math

SymTensorIndex = fieldindex.SymTensorIndex
SymmMatrix = symmmatrix.SymmMatrix

Displacement = problem.Displacement
Stress = problem.Stress


class TestPlasticityProp(pypropertywrapper.PyFluxProperty):
    def __init__(self, registration, name, yield_stress):
        self.name_ = name
        self.elasticity = None
        self.current_el_data=None
        self.yield_stress = yield_stress
        pypropertywrapper.PyFluxProperty.__init__(self, registration, name)

    def order(self, function_order):
        return function_order+1

    def integration_order(self, subproblem, element):
        return element.shapefun_degree();

    def cross_reference(self, material):
        try:
            self.elasticity = material.fetchProperty("Elasticity")
        except:
            self.elasticity = None
            raise

    # def precompute(self, mesh):
    #     pass
    
    # We only have a fluxrhs, because we just subtract the
    # elastic constants times the stress-free strain from the
    # stress.
    def flux_offset(self, mesh, element, flux, masterpos, time, smallsystem):

        # Retrieve the plastic strain field and evaluate it at this
        # masterposition.
        ep_val = symmmatrix.SymmMatrix3()
        ep = field.getField('Plastic')
        efi = element.funcnode_iterator()
        while not efi.end():
            coef = efi.shapefunction(masterpos)
            ep_output = ep.output(mesh, efi.funcnode()) 
            ep_val += ep_output.valuePtr()*coef
            efi += 1 

        # Now ep_val contains the plastic strain at this gausspoint.
        # We can do the arithmetic.  Note that this assumes the same
        # gausspoint set from one iteration to the next, which will in
        # general be a bad assumption.
        modulus = self.elasticity.cijkl(mesh, element, masterpos)
        ij = fieldindex.SymTensorIterator()
        while (not ij.end()):
            offset = 0.0
            kl = ep_val.getIterator()
            while (not kl.end()):
                idx = kl.integer()
                cijkl = modulus[ij.integer(),kl.integer()]
                if idx<3:
                    offset += cijkl*ep_val[kl]
                else:
                    offset += 2.0*cijkl*ep_val[kl]
                kl.next()
            smallsystem.add_offset_element(ij, offset)
            ij.next()

    # Evaluate the constraint equation at a gausspoint.
    def evaluate_constraint(self, mesh, element, eqn, masterpos, smallsystem):

        # TODO 3.1: Test for the right equation.
        
        # Compute the stress -- start with the strain.
        strain = symmmatrix.SymmMatrix3
        ep = field.getField('Plastic')
        efi = element.funcnode_iterator()
        while not efi.end():
            coef = efi.shapefunction(masterpos)
            ep_output = ep.output(mesh, efi.funcnode())
            strain -= ep_output.valuePtr()*coef
            efi += 1

        disp = field.getField('Displacement')
        efi = element.funcnode_iterator()
        while not efi.end():
            ddx = efi.dshapefunction(0,masterpos)
            ddy = efi.dshapefunction(1,masterpos)
            uxx = disp(efi,0).value()*ddx
            uxy = disp(efi,0).value()*ddy
            uyx = disp(efi,1).value()*ddx
            uyy = disp(efi,1).value()*ddy
            strain.set(0,0,strain.get(0,0)+uxx)
            strain.set(0,1,strain.get(0,1)+(0.5*uxy+uyx))
            strain.set(1,1,strain.get(1,1)+uyy)

        try:
            ops = field.getField('Displacement_z')
        except:
            pass
        else:
            efi = element.funcnode_iterator()
            while not efi.end():
                uxz = ops(efi,0).value()
                uyz = ops(efi,1).value()
                uyz = ops(efi,2).value()
                strain.set(0,2,strain.get(0,2)+uxz)
                strain.set(1,2,strain.get(1,2)+uyz)
                strain.set(2,2,strain.get(2,2)+uzz)

        # At this point, "strain" contains the elastic strain,
        # geometric minus plastic.

            
        modulus = self.elasticity.cijkl(mesh, element, masterpos)
        ij = fieldindex.SymTensorIterator()
        while (not ij.end()):
            stressij = 0.0
            kl = ep_val.getIterator()
            while (not kl.end()):
                idx = kl.integer
                cijkl = modulus[ij.integer(),kl.integer()]
                if idx<3:
                    stressij += cijkl*strain[kl]
                else:
                    stressij += 2.0*cijkl*strain[kl]
                kl.next()
            # Accumulate the stress somewhere.
            ij.next()

        # Now call the yield function at this gausspoint with the
        # actual stress, and use this as our contribution to the
        # equation.
        
    
    # Yield-test checks the yield condition and modifies the
    # plastic strain, if necessary.  Currently does hard-coded
    # "associated flow" for the von Mises yield criterion.
    def yield_test(self, pointset, total_strain, plastic_strain,
                   stress, modulus):
        # Locally-defined tolerances -- these should maybe be
        # parameters for the property itself.  When these
        # tolerances are met, the Newton-Raphson iterations are over.
        yield_tolerance = 1.E-06
        resid_tolerance = 1.E-06
        iteration_max = 100
        for (p, e, ep, sigma, cijkl) in zip(pointset, total_strain,
                                            plastic_strain, stress, modulus):
            yld = self.yield_func(sigma)
            print "Yield function gives ", yld
            if yld > 0.0:

                # "Initial guess" for plastic increment amounts.
                gamma = 0.0
                delta_ep = SymmMatrix(3)

                # Allocate "work" matrices.
                mtx = smallmatrix.SmallMatrix(7,7)
                rhs = smallmatrix.SmallMatrix(7,1)

                # Compute matrix r, measure norm.
                r_matrix = SymmMatrix(3)
                r_norm = 0.0
                dyld = self.d_yield_func(sigma)
                for kl in SymTensorIndex(0,0):
                    klr = kl.row()
                    klc = kl.col()
                    r_matrix[klr,klc]=delta_ep[klr,klc] - gamma*dyld[klr,klc]
                    r_norm += r_matrix[klr,klc]**2
                r_norm = math.sqrt(r_norm)
                #
                # Repeat until converged....
                iteration_count = 0
                # On entry to the loop, you must have a valid yield
                # function value yld, derivative dyld, and both
                # r_matrix and r_norm computed for the current stress,
                # and gamma and delta_ep must be valid.
                while ((math.fabs(yld)>yield_tolerance) or \
                       (r_norm > resid_tolerance)) and \
                       iteration_count<iteration_max:
                    iteration_count += 1
                    #
                    # RHS is easy.
                    for kl in SymTensorIndex(0,0):
                        rhs[kl.integer(),0] = -r_matrix[kl.row(),
                                                        kl.col()]
                    rhs[6,0] = -yld
                    
                    mtx.clear()

                    # 
                    # MTX is slightly more involved.
                    for kl in SymTensorIndex(0,0):
                        klr = kl.row()
                        klc = kl.col()

                        mtx[kl.integer(),6]= -dyld[klr,klc]

                        for mn in SymTensorIndex(0,0):
                            mnr = mn.row()
                            mnc = mn.col()
                            #
                            if (klr==mnr)and(klc==mnc):
                                mtx[kl.integer(), mn.integer()] += 1.0
                                
                            mtx[6,mn.integer()] -= ( dyld[klr,klc] *
                                                     cijkl[kl.integer(),
                                                           mn.integer()] )

                            if gamma!=0.0:
                                for op in SymTensorIndex(0,0):
                                    opr = op.row()
                                    opc = op.col()
                                    #
                                    mtx[kl.integer(), mn.integer()] += ( 
                                        gamma * cijkl[op.integer(),
                                                      mn.integer()]*\
                                        self.d_d_yield_func(klr,klc, opr,opc,
                                                            sigma))
                                
                    # Mtx is now built.  Whee.
                    rcode = mtx.solve(rhs)

                    if rcode!=0:
                        raise ErrUserError(
                            "Nonzero return code in matrix solver.")


                    # Increment gamma and delta_ep, then use them to
                    # recompute sigma, yld, dyld, r_matrix and r_norm.
                    # then go around again.
                    for kl in SymTensorIndex(0,0):
                        kli = kl.integer()
                        klr = kl.row()
                        klc = kl.col()
                        delta_ep[klr, klc] += rhs[kli,0]
                    gamma += rhs[6,0]

                    # Modify stress according to the increment of
                    # delta_ep (*not* delta_ep itself!)
                    for kl in SymTensorIndex(0,0):
                        for mn in SymTensorIndex(0,0):
                            sigma[kl.integer()] -= cijkl[kl.integer(),
                                                         mn.integer()]*\
                                                         rhs[mn.integer(),0]

                    yld = self.yield_func(sigma)
                    dyld = self.d_yield_func(sigma)

                    r_norm = 0.0
                    for kl in SymTensorIndex(0,0):
                        klr = kl.row()
                        klc = kl.col()
                        r_matrix[klr,klc]=delta_ep[klr,klc] -\
                                           gamma*dyld[klr,klc]
                        r_norm += r_matrix[klr,klc]**2
                    r_norm = math.sqrt(r_norm)

                # Exit the convergence while loop.
                if iteration_count==1:
                    print "Exiting while loop after 1 iteration." 
                else:
                    print "Exiting while loop after %d iterations." %\
                          iteration_count
                print "Yield, resid are ", yld, r_norm
                
                for ij in SymTensorIndex(0,0):
                    ijr = ij.row()
                    ijc = ij.col()
                    ep[ijr,ijc] += delta_ep[ijr,ijc]

                print "Plastic strain modified."

    # The yield function, which for perfect plasticity is only
    # a function of the stress.
    def yield_func(self, stress):
        l2=0.0
        trace=0.0
        for ij in SymTensorIndex(0,0):
            if ij.integer()<3:
                trace += stress[ij.integer()]
                l2 += stress[ij.integer()]*stress[ij.integer()]
            else:
                l2 += 2.0*stress[ij.integer()]*stress[ij.integer()]
        # Danger: round-off could make the sqrt argument
        # slightly negative, causing a crash here.
        return math.sqrt(l2-(1.0/3.0)*trace*trace)-self.yield_stress

    

    # The first derivative of the yield function with respect
    # to stress.  Takes a list, returns a SymmMatrix objects.
    def d_yield_func(self, stress):
        trace = 0
        res = SymmMatrix(3)
        denom = self.yield_func(stress)+self.yield_stress
        for i in range(3):
            trace += stress[SymTensorIndex(i,i).integer()]
            for j in range(i,3):
                res[i,j] = stress[SymTensorIndex(i,j).integer()]
                if i!=j:
                    res[i,j] *= 2.0
        for i in range(3):
            res[i,i] -= (1.0/3.0)*trace

        res *= (1.0/denom)
        
        return res

    # Second derivative of the yield function with respect to
    # stress, which is a linear combination of delta functions
    # and the first derivative.  It's a four-index quantity, and
    # here we take the indices as arguments.
    def d_d_yield_func(self, idx, jdx, kdx, ldx, stress):
        denom = self.yield_func(stress)+self.yield_stress
        d_y = self.d_yield_func(stress)

        res = -d_y[idx, jdx]*d_y[kdx, ldx]
        if idx==kdx and jdx==ldx:
            res += 1.0
            # in i!=j case, there are two of these.
            if idx==jdx:
                res += 1.0
        if idx==jdx and kdx==ldx:
            res -= 1.0/3.0

        return res/denom


if False:
    reg = propertyregistration.PropertyRegistration(
        'Mechanical:Plasticity:TestPlasticity', TestPlasticityProp,
        "ooflib.engine.property.plasticity.plasticity", 
        105,
        params=[parameter.FloatParameter("yield_stress", 1.0,
                                         tip="Yield stress.")],
        propertyType="Plasticity")

    ## TODO 3.1: I have no idea if this is correct.  This whole file probably
    ## has to be redone entirely in any case. I just added this line when
    ## adding the fluxInfo calls to all the PropertyRegistrations. --SAL
    reg.fluxInfo(fluxes=[Stress], fields=[Displacement], time_derivs=[0],
                 nonlinear=True)

    # TODO 3.1: Should specify fields here, too, but only the ones we require
    # to evaluate the constraint.  We need plastic strain, of course.
    # Hardening types of plasticity will also need the appropriate
    # hardening-variable fields.  We do *not* need the plastic parameter
    # (lambda) field here, nor do we need the various increment fields.
    reg.constraintInfo(equations=[problem.YieldEquation])
