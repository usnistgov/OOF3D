# -*- python -*-
# $RCSfile: nonlinear_timedependent_test.py,v $
# $Revision: 1.1.2.4 $
# $Author: langer $
# $Date: 2014/09/27 22:34:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.


# Test nonlinear solvers with *uniform* time stepping.  The RHS is
# nonlinear, but the modulus is linear, so Newton and Picard should
# give the same answer.

import unittest, os
import memorycheck
from math import *
import exact_solns

## NonlinearHeatSource results

# n    dt     solver        L2

## test_no=2, soln_no=3

#  4  0.001   BE/Picard     0.336
#  4  0.001   BE/Newton     0.336
#  4  0.001   CN/Picard     0.336
#  4  0.001   CN/Newton     0.336
#  4  0.001   SS22/Picard   0.336
#  4  0.001   SS22/Newton   0.336

#  8  0.001   BE/Picard     0.153
#  8  0.01    BE/Picard     0.153

#  8  0.01    CN/Picard     0.105
#  8  0.01    CN/Newton     0.105
#  8  0.01    SS22/Picard   0.105
#  8  0.01    SS22/Newton   0.105
# 16  0.01    BE/Picard     0.0578
# 16  0.01    BE/Newton     0.0578
# 16  0.01    CN/Picard     0.0268
# 16  0.01    CN/Newton     0.0268
# 16  0.01    SS22/Picard   0.0268
# 16  0.01    SS22/Newton   0.0268

## test_no=4, soln_no=4

#  8  0.01    BE/Picard     0.00295
#  8  0.01    BE/Newton     0.00295
#  8  0.01    CN/Picard     0.00316
#  8  0.01    CN/Newton     0.00316
#  8  0.01    SS22/Picard   0.00316
#  8  0.01    SS22/Newton   0.00316
# 16  0.01    BE/Picard     0.0009932
# 16  0.01    BE/Newton     0.0009932
# 16  0.01    CN/Picard     0.001251
# 16  0.01    CN/Newton     0.001251
# 16  0.01    SS22/Picard   0.001251
# 16  0.01    SS22/Newton   0.001251
## TODO: For this test, BE seems to do better than CN and SS22, which
## is strange.  Check that CN and SS22 converge faster than BE as dt
## is decreased.

## test_no=5, soln_no=5

#  8  0.01    BE/Picard     0.00764
#  8  0.01    BE/Newton     0.00764
#  8  0.01    CN/Picard     0.00717
#  8  0.01    CN/Newton     0.00717
#  8  0.01    SS22/Picard   0.00717
#  8  0.01    SS22/Newton   0.00717


## NonlinearForceDensity results

## test_no=2, soln_no=1

#  8  0.01    BE/Picard     0.152244481174
#  8  0.01    BE/Newton     0.152244478906
#  8  0.01    CN/Picard     0.194585980822
#  8  0.01    CN/Newton     0.194585980643
#  8  0.01    SS22/Picard   0.19458598067
#  8  0.01    SS22/Newton   0.194585980643
# 16  0.01    BE/Picard     0.0404963759716
# 16  0.01    BE/Newton     0.0404963723841
# 16  0.01    CN/Picard     0.0681129098557
# 16  0.01    CN/Newton     0.0681129618367
# 16  0.01    SS22/Picard   
# 16  0.01    SS22/Newton   


class NonlinearTimedependentTest(unittest.TestCase):
    def tearDown(self):
        OOF.Material.Delete(name="material")

    def setUp(self):

        n = 16
        self.numX = n
        self.numY = n
        self.numZ = n
        self.time = 0.1
        self.timestep = 0.01

        self.time_steppers = [
            # ForwardEuler(),
            BackwardEuler(),
            CrankNicolson(),
            SS22(theta1=0.5,theta2=0.5),
            # RK4()  # has stability problems with the uniform time stepper
            ]

        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=self.numX, y_elements=self.numY, z_elements=self.numZ,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])

        self.heat_solns = exact_solns.exact_solns["scalar"]
        self.elasticity_solns = exact_solns.exact_solns["vector3D"]

        self.boundary_condition_count = 0


    def setBoundaryConditions(self,BC_type,BC_field,BC_equation,BC_list):

        BC_no = 0
        for BC in BC_list:

            BC_no = BC_no + 1

            if BC_type == 'Dirichlet':
                new_BC = DirichletBC(
                    field           = BC_field,
                    field_component = BC[1],
                    equation        = BC_equation,
                    eqn_component   = BC[2],
                    profile         = ContinuumProfileXTd(
                                          function        = BC[3],
                                          timeDerivative  = BC[4],
                                          timeDerivative2 = BC[5]),
                    boundary        = BC[0])

            elif BC_type == 'Neumann':
                new_BC = NeumannBC(
                    field           = BC_field,
                    field_component = BC[1],
                    equation        = BC_equation,
                    eqn_component   = BC[2],
                    profile         = ContinuumProfileXTd(
                                          function        = BC[3],
                                          timeDerivative  = BC[4],
                                          timeDerivative2 = BC[5]),
                    boundary        = BC[0])

            OOF.Mesh.Boundary_Conditions.New(
                name = 'bc<' + str(BC_no) + '>',
                mesh = 'microstructure:skeleton:mesh',
                condition = new_BC )

        self.boundary_condition_count = BC_no


    def removeBoundaryConditions(self):

        for bc_no in range(1, self.boundary_condition_count+1):
             OOF.Mesh.Boundary_Conditions.Delete(
                 mesh='microstructure:skeleton:mesh',
                 name='bc<' + str(bc_no) + '>')

        self.boundary_condition_count = 0


    @memorycheck.check("microstructure")
    def NonlinearHeatSource(self):

        # "test_no" refers to the index that's passed to
        # TestNonlinearHeatSource to determine the form of the heat
        # source nonlinearity.

        # "soln_no" is an index into the data structure defined in
        # exact_solns.py, which contains boundary conditions, initial
        # values, and solution functions.
        nonlin_heat_source_tests = [ 
            {"test_no":2, "soln_no":3, 'tolerance':0.15},
            {"test_no":4, "soln_no":4, 'tolerance':0.01},
            {"test_no":5, "soln_no":5, 'tolerance':0.01}
        ]


        # define the heat equation related quantities needed for this test
        OOF.Property.Parametrize.Thermal.Conductivity.Isotropic(
            kappa=1.0)
        OOF.Material.Add_property(
            name='material',
            property='Thermal:Conductivity:Isotropic')
        OOF.Property.Parametrize.Thermal.HeatCapacity.ConstantHeatCapacity(
            cv=1.0)
        OOF.Material.Add_property(
            name='material',
            property='Thermal:HeatCapacity:ConstantHeatCapacity')
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Heat_Eqn)

        # iterate through nonlinear heat source test by alternating
        # between various test examples and nonlinear solvers
        for test in nonlin_heat_source_tests:

            test_no = test["test_no"]
            soln_no = test["soln_no"]
            tolerance = test['tolerance']

            # add the nonlinear heat source property to the material
            OOF.Property.Parametrize.Thermal.HeatSource.TestNonlinearHeatSource(
                testno=test_no)
            OOF.Material.Add_property(
                name='material',
                property='Thermal:HeatSource:TestNonlinearHeatSource')
            OOF.Material.Assign(
                material='material', microstructure='microstructure',
                pixels=all)

            # set the boundary conditions for the given test no
            self.setBoundaryConditions('Dirichlet', Temperature, Heat_Eqn,
                                       self.heat_solns[soln_no]["DirichletBC"] )

            for test_stepper in self.time_steppers:

                # compute the solution using Picard iterations
                test_solver = Picard(
                    relative_tolerance=1e-08,
                    absolute_tolerance=1.0e-13,
                    maximum_iterations=20)

                self.heatEqnEngine( test_no, soln_no, test_solver, 
                                    test_stepper, tolerance )

                # compute the solution using Newton's method
                test_solver = Newton(
                    relative_tolerance=1e-08,
                    absolute_tolerance=1.0e-13,
                    maximum_iterations=20)

                self.heatEqnEngine( test_no, soln_no, test_solver,
                                    test_stepper, tolerance )

            # remove the boundary conditions for the given test no
            self.removeBoundaryConditions()

            # remove the current version of the nonlinear heat source property
            OOF.Material.Remove_property(
                name='material',
                property='Thermal:HeatSource:TestNonlinearHeatSource')

        # delete the other properties, fields, equations needed for this test
        OOF.Subproblem.Equation.Deactivate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Heat_Eqn)
        OOF.Subproblem.Field.Undefine(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Material.Remove_property(
            name='material',
            property='Thermal:Conductivity:Isotropic')
        OOF.Material.Remove_property(
            name='material',
            property='Thermal:HeatCapacity:ConstantHeatCapacity')


    def heatEqnEngine(self,test_no,soln_no,test_solver,test_stepper,tolerance):

        soln_func = self.heat_solns[soln_no]["Solution"]
        init_func = self.heat_solns[soln_no]["InitialValue"]

        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
               time_stepper=UniformDriver(
                    stepsize=self.timestep,
                    stepper=test_stepper),
               nonlinear_solver=test_solver,
               symmetric_solver=ConjugateGradient(
                   preconditioner=ILUPreconditioner(),
                   tolerance=1e-13,
                   max_iterations=1000),
               asymmetric_solver=BiConjugateGradient(
                   preconditioner=ILUPreconditioner(),
                   tolerance=1e-13,
                   max_iterations=1000)))

        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Temperature,
            initializer=FuncScalarFieldInit(
                function=init_func))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh',
            time=0.0)

        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=self.time)

        from ooflib.engine import mesh
        from ooflib.SWIG.engine import field

        mesh_obj  = mesh.meshes["microstructure:skeleton:mesh"].getObject()
        field_ptr = field.getField( "Temperature" )

        L2_error = exact_solns.computeScalarErrorL2( 
            soln_func, mesh_obj, field_ptr,
            self.numX, self.numY, self.numZ, time=self.time )
        print "L2 error: ", L2_error

        self.assert_( L2_error < tolerance )


    @memorycheck.check("microstructure")
    def NonlinearForceDensity(self):

        nonlin_force_density_tests = [
            {"test_no":2, "soln_no":1, "tolerance":1.0},
            #{"test_no":4, "soln_no":4} 
        ]

        # define the force density related quantities needed for this test
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic(
            cijkl=IsotropicRank4TensorLame(lmbda=-1,mu=1))
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Property.Parametrize.Mechanical.MassDensity.ConstantMassDensity(
            rho=1.0)
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:MassDensity:ConstantMassDensity')
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)

        # iterate through nonlinear force density test by alternating
        # between various test examples and nonlinear solvers
        for test in nonlin_force_density_tests:

            test_no = test["test_no"]
            soln_no = test["soln_no"]
            tolerance = test['tolerance']

            # add the nonlinear force density property to the material
            OOF.Property.Parametrize.Mechanical.ForceDensity.TestNonlinearForceDensity(
                testno=test_no)
            OOF.Material.Add_property(
                name='material',
                property='Mechanical:ForceDensity:TestNonlinearForceDensity')
            OOF.Material.Assign(
                material='material', microstructure='microstructure',
                pixels=all)

            # set the boundary conditions for the given test no
            self.setBoundaryConditions( 
                'Dirichlet', Displacement, Force_Balance,
                self.elasticity_solns[soln_no]["DirichletBC"] )

            for test_stepper in self.time_steppers:

                # compute the solution using Picard iterations
                test_solver = Picard(
                    relative_tolerance=1e-08,
                    absolute_tolerance=1.0e-13,
                    maximum_iterations=20)

                self.elasticityEqnEngine( test_no, soln_no, test_solver,
                                          test_stepper, tolerance )

                # compute the solution using Newton's method
                test_solver = Newton(
                    relative_tolerance=1e-08,
                    absolute_tolerance=1.0e-13,
                    maximum_iterations=20)

                self.elasticityEqnEngine( test_no, soln_no, test_solver,
                                          test_stepper, tolerance )

            # remove the boundary conditions for the given test no
            self.removeBoundaryConditions()

            # remove the current version of the nonlinear force density property
            OOF.Material.Remove_property(
                name='material',
                property='Mechanical:ForceDensity:TestNonlinearForceDensity')

        # delete the other properties, fields, equations needed for this test
        OOF.Subproblem.Equation.Deactivate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Subproblem.Field.Undefine(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Material.Remove_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Material.Remove_property(
            name='material',
            property='Mechanical:MassDensity:ConstantMassDensity')


    def elasticityEqnEngine(self,test_no,soln_no,test_solver,test_stepper,
                            tolerance):

        soln_func = self.elasticity_solns[soln_no]["Solution"]
        init_func = self.elasticity_solns[soln_no]["InitialValue"]
        init_deriv_func = self.elasticity_solns[soln_no]["InitialTimeDeriv"]

        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
               time_stepper=UniformDriver(
                    stepsize=self.timestep,
                    stepper = test_stepper ),
               nonlinear_solver = test_solver,
               symmetric_solver=ConjugateGradient(
                   preconditioner=ILUPreconditioner(),
                   tolerance=1e-13,
                   max_iterations=1000),
               asymmetric_solver=BiConjugateGradient(
                   preconditioner=ILUPreconditioner(),
                   tolerance=1e-13,
                   max_iterations=1000)))

        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Displacement,
            initializer=FuncThreeVectorFieldInit(
                fx = init_func[0], fy = init_func[1], fz = init_func[2]))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Displacement_t,
            initializer=FuncThreeVectorFieldInit(
                fx = init_deriv_func[0],
                fy = init_deriv_func[1],
                fz = init_deriv_func[2]))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh',
            time=0.0)

        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=self.time)

        from ooflib.engine import mesh
        from ooflib.SWIG.engine import field

        mesh_obj  = mesh.meshes["microstructure:skeleton:mesh"].getObject()
        field_ptr = field.getField( "Displacement" )

        L2_error = exact_solns.computeVector3DErrorL2(
            soln_func, mesh_obj, field_ptr,
            self.numX, self.numY, self.numZ, time=self.time)
        print "L2 error: ", L2_error

        self.assert_( L2_error < tolerance )


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    NonlinearTimedependentTest("NonlinearHeatSource"),
    NonlinearTimedependentTest("NonlinearForceDensity"),
]
