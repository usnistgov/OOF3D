# -*- python -*-
# $RCSfile: pyheatconductivity.py,v $
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

# A simple heat conductivity property written in Python, as a test of
# the Python Property API.  This shouldn't ever be used in a real
# calculation, since it is much slower than the C++ code in
# heatconductivity.C.  It's used in the regression tests, though.

from ooflib.common import debug
from ooflib.SWIG.common import config
from ooflib.SWIG.engine import fieldindex
from ooflib.SWIG.engine import planarity
from ooflib.SWIG.engine import pypropertywrapper
from ooflib.SWIG.engine import symmmatrix
from ooflib.engine import problem
from ooflib.engine import propertyregistration

## TODO OPT: See the TODO OPT in pyelasticity.py about improving the Python
## Properties.

class PyHeatConductivity(pypropertywrapper.PyFluxProperty):
    def flux_matrix(self, mesh, element, nodeiterator, flux, point, time,
                    fluxdata):
        twoD = config.dimension() == 2
        sf = nodeiterator.shapefunction(point)
        dsf0 = nodeiterator.dshapefunction(0, point)
        dsf1 = nodeiterator.dshapefunction(1, point)
        if not twoD:
            dsf2 = nodeiterator.dshapefunction(2, point)
        cond = symmmatrix.SymmMatrix3(1., 1., 1., 0., 0., 0.)
        fluxiterator = problem.Heat_Flux.iterator(planarity.ALL_INDICES)
        while not fluxiterator.end():
            val = -(cond.get(fluxiterator.integer(), 0) * dsf0 +
                    cond.get(fluxiterator.integer(), 1) * dsf1)
            if not twoD:
                val -= cond.get(fluxiterator.integer(), 2) *dsf2
            fluxdata.add_stiffness_matrix_element(
                fluxiterator,
                problem.Temperature,
                problem.Temperature.getIndex(""), # scalar field dummy 'index'
                nodeiterator,
                val)
            if (twoD and not problem.Temperature.in_plane(mesh)):
                fluxdata.add_stiffness_matrix_element(
                    fluxiterator,
                    problem.Temperature.out_of_plane(), # also a scalar
                    problem.Temperature.getIndex(""),   # also a dummy
                    nodeiterator,
                    cond.get(fluxiterator.integer(), 2) * sf)
            
            fluxiterator.next()
    def integration_order(self, subproblem, element):
        if (config.dimension() == 2 and
            # get_mesh is commented out in OOF3D.
            problem.Temperature.in_plane(subproblem.get_mesh())):
            return element.dshapefun_degree()
        return element.shapefun_degree()

reg = propertyregistration.PropertyRegistration(
    'Thermal:Conductivity:PyIsotropic',
    PyHeatConductivity,
    "ooflib.engine.property.heatconductivity.pyheatconductivity",
    ordering=10000,
    propertyType="ThermalConductivity",
    secret=True
    )

reg.fluxInfo(fluxes=[problem.Heat_Flux], fields=[problem.Temperature],
             time_derivs=[0])
