# -*- python -*-
# $RCSfile: pyelasticity.py,v $
# $Revision: 1.2.4.6 $
# $Author: langer $
# $Date: 2014/11/05 16:54:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# A simple elasticity property written in Python, as a test of the
# Python Property API.

## TODO 3.1: A C++ Property that gets a reference to this Property via
## cross_reference and expects to be able to call this Property's
## cijkl() method will be sorely disappointed, because from C++ this
## just looks like a PyFluxProperty, which doesn't have a cijkl
## method.  Fix this somehow.

## TODO 3.1:INDEXING This and the other Python Properties are quite a
## mess, and writing them isn't much easier than writing C++
## Properties.  A big part of the problem is that there are too many
## indexing and iterator classes, and different kinds of objects
## expect different kinds of indices.  These need to be unified.  For
## example, in this file, cijkl is indexed by passing a 2-tuple of
## integers, which are obtained by the 'integer' method of an
## IteratorP, to Cijkl.__getitem__.  In pystressfreestrain.py, getting
## a component of a SymmMatrix3 requires passing a SymTensorIterator's
## .col() and .row() to SymmMatrix3.get().
##
## Also, this code would be a lot neater if FieldIterator classes were
## really Python iterators.  The loop in flux_matrix(), below, should
## look something like this:
# for ij in problem.Stress.iterator(planarity.ALL_INDICES):
#     for ell in problem.Displacement.iterator(planarity.ALL_INDICES):
#         for k in (0, 1):
#             fluxdata.stiffness_matrix_element(
#                 ij, problem.Displacement, ell, node) += cijkl[ij, k, l]*dsf[k]
## SmallSystem.stiffness_matrix_element will have to return some kind
## of helper object whose += can be defined.  Cijkl will have to have
## some kind of flexible indexing that can take mixtures of
## SymTensorIndex, VectorFieldIndex, and integer arguments.

from ooflib.SWIG.common import config
from ooflib.SWIG.engine import cstrain
from ooflib.SWIG.engine import fieldindex
from ooflib.SWIG.engine import outputval
from ooflib.SWIG.engine import planarity
from ooflib.SWIG.engine import pypropertywrapper
from ooflib.SWIG.engine import symmmatrix
from ooflib.common import debug
from ooflib.engine import problem
from ooflib.engine import propertyregistration
from ooflib.engine.IO import isocijkl

class PyElasticity(pypropertywrapper.PyFluxProperty):
    def modulus(self):
        return isocijkl.IsotropicRank4TensorCij(c11=1.0, c12=0.5).tensorForm()

    def flux_matrix(self, mesh, element, nodeiterator, flux, point, time,
                    fluxdata):
        twoD = config.dimension() == 2
        sf = nodeiterator.shapefunction(point)
        dsf0 = nodeiterator.dshapefunction(0, point)
        dsf1 = nodeiterator.dshapefunction(1, point)
        if not twoD:
            dsf2 = nodeiterator.dshapefunction(2, point)
        cijkl = self.modulus()
        ij = problem.Stress.iterator(planarity.ALL_INDICES)
        while not ij.end():
            ell = problem.Displacement.iterator(planarity.ALL_INDICES)
            while not ell.end():
                ell0 = fieldindex.SymTensorIndex(0, ell.integer())
                ell1 = fieldindex.SymTensorIndex(1, ell.integer())
                val = (cijkl[(ij.integer(), ell0.integer())]*dsf0 + 
                       cijkl[(ij.integer(), ell1.integer())]*dsf1)
                if not twoD:
                    ell2 = fieldindex.SymTensorIndex(2, ell.integer())
                    val += cijkl[(ij.integer(), ell2.integer())]*dsf2
                fluxdata.add_stiffness_matrix_element(
                    ij,
                    problem.Displacement,
                    ell,
                    nodeiterator,
                    val
                    )
                ell.next()
            if twoD and not problem.Displacement.in_plane(mesh):
                oop = problem.Displacement.out_of_plane()
                kay = oop.iterator(planarity.ALL_INDICES)
                while not kay.end():
                    kl = fieldindex.SymTensorIndex(2, ell.integer)
                    fluxdata.add_stiffness_matrix_element(
                        ij, oop, kay, nodeiterator,
                        cijkl[(ij.integer(), kl.integer())]*sf
                        )
                    kay.next()
            ij.next()

    def integration_order(self, subproblem, element):
        if (config.dimension() == 2 and
            # get_mesh is commented out in OOF3D.
            problem.Displacement.in_plane(subproblem.get_mesh())):
            return element.dshapefun_degree()
        return element.shapefun_degree()

    def output(self, mesh, element, output, pos):
        if output.name() == "Energy":
            etype = output.getEnumParam("etype")
            if etype in ("Total", "Elastic"):
                mod = self.modulus()
                # strain is a SymmMatrix3.  modulus is a cijkl.Cijkl
                strain = cstrain.findGeometricStrain(mesh, element, pos, False)
                stress = mod*strain # another SymmMatrix3.
                return outputval.ScalarOutputVal(0.5*stress.contract(strain))
                # TODO INDEXING: It would be good to be able to write
                # that like this:
                ## e = 0
                ## for ij in stress.getIterator():
                ##     if ij.diagonal():
                ##         e += stress[ij]*strain[ij]
                ##     else:
                ##         e += 2*stress[ij]*strain[ij]
                ## return ScalarOutputVal(0.5*e)
                # Although it would be slower than the calling
                # SymmMatrix3.contract(), it would be more easily
                # modifiable and applicable to specialized Python
                # Properties. The reason that it's not currently
                # written that way is that stress.getIterator returns
                # a generic IteratorP object, which is what
                # SymmMatrix3.__getitem__ wants as a arg, but
                # IteratorP doesn't have a diagonal() method.
                    

reg = propertyregistration.PropertyRegistration(
    'Mechanical:Elasticity:PyIsotropic',
    PyElasticity,
    "ooflib.engine.property.elasticity.pyelasticity",
    ordering=10000,
    outputs=["Energy"],
    propertyType="Elasticity",
    secret=True,
    tip="Isotropic linear elasticity implemented in Python.")

reg.fluxInfo(fluxes=[problem.Stress], fields=[problem.Displacement],
             time_derivs=[0])
