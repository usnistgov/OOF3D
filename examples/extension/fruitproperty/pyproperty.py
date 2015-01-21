# -*- python -*-
# $RCSfile: pyproperty.py,v $
# $Revision: 1.8.8.1 $
# $Author: langer $
# $Date: 2014/09/27 22:35:14 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Example of an all-Python property, using the PyPropertyWrapper
# mechanism to route callbacks through to Python routines contained
# here.

# Casting of flux and field to the "most-derived" class via the
# PythonExportable mechanism is thinkable, but probably not actually
# necessary.  The property knows its field and flux as derived types
# at construction/initialization time, and can get the appropriate
# iterators from them, rather than from the passed-in arguments to
# fluxmatrix, fluxrhs, etc.  Those it can just use for comparison,
# to detect which field is currently presenting its fluxmatrix.

from ooflib.SWIG.engine import fieldindex
from ooflib.SWIG.engine import outputval
from ooflib.SWIG.engine import planarity
from ooflib.SWIG.engine import pypropertywrapper 
from ooflib.SWIG.engine import symmmatrix
from ooflib.SWIG.engine.property.elasticity import cijkl
from ooflib.common import debug
from ooflib.engine import propertyregistration
from ooflib.engine import problem

Displacement = problem.Displacement
Stress = problem.Stress

class TestProp(pypropertywrapper.PyPropertyWrapper):
    def __init__(self, registration, name):
        self.modulus = cijkl.Cijkl();
        pypropertywrapper.PyPropertyWrapper.__init__(self,
                                                     registration,
                                                     name)
        # Fixed, hard-coded moduli, for now, numerically HexagonalElasticity
        self.modulus[0,0] = self.modulus[1,1] = 1.0
        self.modulus[0,1] = 0.5
        self.modulus[5,5] = 0.25

        # Explicitly set all others to zero.
        self.modulus[0,2] = self.modulus[0,3] = self.modulus[0,4] = 0.0
        self.modulus[0,5] = 0.0
        self.modulus[1,2] = self.modulus[1,3] = self.modulus[1,4] = 0.0
        self.modulus[1,5] = 0.0
        self.modulus[2,2] = self.modulus[2,3] = self.modulus[2,4] = 0.0
        self.modulus[2,5] = 0.0
        self.modulus[3,3] = self.modulus[3,4] = self.modulus[3,5] = 0.0
        self.modulus[4,4] = self.modulus[4,5] = 0.0

    # This property has a simple repr, with no parameters.
    def __repr__(self):
        return "Test(name='%s')" % self.name()
    def integration_order(self, mesh, element):
        return element.shapefun_degree()

    def cross_reference(self, material):
        # This property requires an orientation to be present in the
        # same Material.  It doesn't actually use it, though...
        self.orientation = material.fetchProperty('Orientation')

    def flux_matrix(self, mesh, element, funcnodeiterator, flux, 
                    masterpos, fluxdata):
        # Shape functions.
        sf = funcnodeiterator.shapefunction(masterpos)
        dshapedx = funcnodeiterator.dshapefunction(0,masterpos)
        dshapedy = funcnodeiterator.dshapefunction(1,masterpos)
        fluxcomp = Stress.iterator(planarity.ALL_INDICES)
        while not fluxcomp.end():
            fieldcomp = Displacement.iterator(planarity.IN_PLANE)
            while not fieldcomp.end():
                ell0 = fieldindex.SymTensorIndex(0, fieldcomp.integer())
                ell1 = fieldindex.SymTensorIndex(1, fieldcomp.integer())
                v = self.modulus[fluxcomp.integer(), ell0.integer()]*dshapedx+\
                    self.modulus[fluxcomp.integer(), ell1.integer()]*dshapedy
                fluxdata.add_stiffness_matrix_element(fluxcomp, Displacement,
                                                      fieldcomp,
                                                      funcnodeiterator, v)
                fieldcomp.next()
            # loop over out-of-plane strains
            if not Displacement.in_plane(mesh):
                dispz = Displacement.out_of_plane()
                ell = dispz.iterator(planarity.ALL_INDICES)
                while not ell.end():
                    if ell.integer() == 2:
                        diag_factor = 1.
                    else:
                        diag_factor = 0.5
                    v = self.modulus[fluxcomp.integer(),
                                     fieldindex.SymTensorIndex(
                        2,ell.integer()).integer() ] * sf * diag_factor
                    fluxdata.add_stiffness_matrix_element(fluxcomp,
                                                          dispz, ell,
                                                          funcnodeiterator, v)
                    ell.next()
            fluxcomp.next()
                
    def output(self, mesh, element, propertyoutput, position):
        if propertyoutput.name() == "Energy":
            return outputval.ScalarOutputVal(3.14)*position.mastercoord()[0]
        if propertyoutput.name() == "Strain":
            stype = propertyoutput.getRegisteredParamName("type")
            if stype == "Geometric":
                return symmmatrix.SymmMatrix3(0,1,2,3,4,5)
            

            
propertyregistration.PropertyRegistration('PyProperty', TestProp,
                                          "fruitproperty.pyproperty",
                                          1000,
                                          params=[],
                                          fields=[Displacement],
                                          fluxes=[Stress],
                                          outputs=["Energy", "Strain"],
                                          propertyType="Elasticity")
    
