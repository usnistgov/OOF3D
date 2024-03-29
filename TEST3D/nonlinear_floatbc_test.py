# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import os
import unittest

import memorycheck
from UTILS import file_utils
file_utils.generate = False

# A trivial linear thermal diffusion problem, with T=1 fixed at X=0,
# initialized to T=0 in the interior.  Check that the solution is the
# same whether or not there's a floating boundary condition at X=1.

linearElements = ['TET4_4', 'D2_2', 'T3_3', 'Q4_4']
quadraticElements = ['TET4_10', 'D2_3', 'T3_6', 'Q4_8']

class OOF_SimpleFloat(unittest.TestCase):
    def setUp(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material',
            microstructure='microstructure',
            pixels=all)
        OOF.Material.Add_property(
            name='material',
            property='Thermal:Conductivity:Isotropic')
        OOF.Material.Add_property(
            name='material',
            property='Thermal:HeatCapacity:ConstantHeatCapacity')
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh', skeleton='microstructure:skeleton',
            element_types=self.elementTypes())
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Heat_Eqn)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='Xmin'))

        # Measure the average temperature on the right edge, which
        # will sometimes be the location of a floating BC.
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name=AutomaticName('Temperature//Average'), 
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Temperature),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Xmax',side='BACK'),
                sampling=ContinuumSampleSet(order=automatic)), 
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=0.1), 
            destination=OutputStream(filename='right.out',mode='w'))

        # Select faces through the middle of the Skeleton at x=0.5,
        # construct a Boundary on those faces, and measure the average
        # temperature on it, in order to have a check that's *not* on
        # the floating BC.
        
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[89, 114, 113],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[88, 89, 113],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[88, 113, 87],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[113, 112, 87],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[87, 112, 111],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[86, 87, 111],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[86, 111, 85],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[111, 110, 85],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[60, 61, 85],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[61, 86, 85],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[87, 86, 61],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[62, 87, 61],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[62, 63, 87],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[63, 88, 87],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[89, 88, 63],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[64, 89, 63],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[39, 64, 63],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[38, 39, 63],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[38, 63, 37],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[63, 62, 37],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[37, 62, 61],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[36, 37, 61],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[36, 61, 35],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[61, 60, 35],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[11, 36, 35],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[10, 11, 35],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[37, 36, 11],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[12, 37, 11],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[12, 13, 37],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[13, 38, 37],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[39, 38, 13],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='microstructure:skeleton',
            method=SingleFaceSelect(nodes=[14, 39, 13],
                                    operator=AddSelection()))

        OOF.Skeleton.Boundary.Construct(
            skeleton='microstructure:skeleton',
            name='midfield',
            constructor=FaceFromFaces(
                group=selection,
                direction='-X to +X'))
        OOF.Mesh.Modify(
            mesh='microstructure:skeleton:mesh',
            modifier=RebuildMesh())

        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='middle.out',
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Temperature),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='midfield',side='BACK'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(), 
            schedule=Periodic(delay=0.0,interval=0.1),
            destination=OutputStream(
                filename='middle.out',mode='w'))

        # OOF.Mesh.Scheduled_Output.New(
        #     mesh='microstructure:skeleton:mesh',
        #     name='centerpoint.out',
        #     output=ScheduledAnalysis(
        #         data=getOutput('Field:Value',field=Temperature),
        #         operation=DirectOutput(),
        #         domain=SinglePoint(point=Point(0.5,0.5,0.5)),
        #         sampling=PointSampleSet(show_x=True,show_y=True,show_z=True)),
        #     scheduletype=AbsoluteOutputSchedule(),
        #     schedule=Periodic(delay=0.0,interval=0.1),
        #     destination=OutputStream(
        #         filename='center.out',mode='w'))

        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='centerpoint.out',
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Temperature),
                operation=AverageOutput(),
                domain=SinglePoint(point=Point(0.5, 0.5, 0.5)),
                sampling=StatPointSampleSet()),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=0.1),
            destination=OutputStream(
                filename='center.out',mode='w'))

        # # Output the full mesh, for debugging.
        # OOF.Mesh.Scheduled_Output.New(
        #     mesh='microstructure:skeleton:mesh',
        #     name='mesh',
        #     output=MeshFileOutput(),
        #     scheduletype=AbsoluteOutputSchedule(), 
        #     schedule=Periodic(delay=0.0,interval=0.1),
        #     destination=DataFileOutput(
        #         filename='temptop.mesh',mode='w',format='ascii'))

        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh', 
            field=Temperature, 
            initializer=ConstScalarFieldInit(value=0.0))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh', time=0.0)

    def check(self, tolerance,
              centerfile=None, middlefile=None, rightfile=None):
        self.assert_(file_utils.fp_file_compare(
                'center.out',
                os.path.join('mesh_data', centerfile or 'simplecenter.out'),
                tolerance))
        file_utils.remove('center.out')

        self.assert_(file_utils.fp_file_compare(
                'middle.out',
                os.path.join('mesh_data', middlefile or 'simplemiddle.out'),
                tolerance))
        file_utils.remove('middle.out')
                             
        self.assert_(file_utils.fp_file_compare(
                'right.out',
                os.path.join('mesh_data', rightfile or 'simpleright.out'),
                tolerance))
        file_utils.remove('right.out')

    def tearDown(self):
        from ooflib.engine.IO import outputdestination
        outputdestination.forgetTextOutputStreams()
        OOF.Material.Delete(name='material')

    def linearSolver(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=1.e-06,
                    minstep=1.e-06,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=CrankNicolson())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)))

    def nonlinearSolver(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=1.e-05,
                    minstep=1.e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=CrankNicolson())),
                nonlinear_solver=Newton(
                    relative_tolerance=1.e-08,
                    absolute_tolerance=1.e-13,
                    maximum_iterations=200),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)))

    def nonlinearUniformSolver(self, stepsize):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=UniformDriver(
                    stepsize=stepsize,
                    stepper=CrankNicolson()),
                nonlinear_solver=Newton(
                    relative_tolerance=1.e-08,
                    absolute_tolerance=1.e-13,
                    maximum_iterations=200),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)))

    def floatBC(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh', 
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.Set_BC_Initializer(
            mesh='microstructure:skeleton:mesh',
            bc='bc<2>',
            initializer=FloatBCInitMin(value=0.0))

    def solve(self):
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=3.0)

    # The reference calculation uses a linear solver and a free BC on
    # the right side.
    @memorycheck.check("microstructure")
    def LinearFree(self):
        self.linearSolver()
        self.solve()
        self.check(1.e-6)
    
    # Sanity-check calculation, still linear, but with a FloatBC on
    # the right.
    @memorycheck.check("microstructure")
    def LinearFloat(self):
        self.linearSolver()
        self.floatBC()
        self.solve()
        self.check(1.e-2)

    # Now check the nonlinear solver with the free BC.
    @memorycheck.check("microstructure")
    def NonlinearFree(self):
        self.nonlinearSolver()
        self.solve()
        self.check(1.e-2)

    # And again with the floating BC.
    @memorycheck.check("microstructure")
    def NonlinearFloat(self):
        self.nonlinearSolver()
        self.floatBC()
        self.solve()
        self.check(1.e-2)

    # And again with the floating BC, with a uniform stepper
    @memorycheck.check("microstructure")
    def NonlinearUniformFloat(self):
        self.nonlinearUniformSolver(stepsize=0.01)
        self.floatBC()
        self.solve()
        self.check(1.e-2)

class OOF_SimpleFloat_Linear(OOF_SimpleFloat):
    def elementTypes(self):
        return linearElements

class OOF_SimpleFloat_Quadratic(OOF_SimpleFloat):
    def elementTypes(self):
        return quadraticElements
    def check(self, tol):
        # Quadratic elements cause large differences in reference
        # files at early times, so rather than compare with loose
        # tolerance for all points, use separate reference files for
        # linear and quadratic elements.  This sort of violates the
        # spirit of the test...
        OOF_SimpleFloat.check(self, tol,
                              centerfile="simplecenter-quad.out",
                              middlefile="simplemiddle-quad.out",
                              rightfile="simpleright-quad.out")

# A time-dependent linear diffusion problem that includes a floating
# boundary condition, solved in a variety of ways, all of which should
# give the same answer. 

class OOF_FloatBC1(unittest.TestCase):
    def setUp(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material', microstructure='microstructure', pixels=all)
        OOF.Material.Add_property(
            name='material', property='Thermal:Conductivity:Isotropic')
        OOF.Material.Add_property(
            name='material', 
            property='Thermal:HeatCapacity:ConstantHeatCapacity')
        OOF.Skeleton.New(
            name='skeleton', 
            microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh', skeleton='microstructure:skeleton',
            element_types=self.elementTypes())
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default', 
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Heat_Eqn)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.Set_BC_Initializer(
            mesh='microstructure:skeleton:mesh',
            bc='bc',
            initializer=FloatBCInitMin(value=0.0))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='XminYminZmin'))

        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh', 
            name=AutomaticName('Temperature//Average'),
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Temperature),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Ymax',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=0.1),
            destination=OutputStream(filename='temptop.out',mode='w'))
        # OOF.Mesh.Scheduled_Output.New(
        #     mesh='microstructure:skeleton:mesh',
        #     name=AutomaticName('Average Temperature on top'),
        #     output=BoundaryAnalysis(
        #         operation=AverageField(field=Temperature),
        #         boundary='Ymax'))
        # OOF.Mesh.Scheduled_Output.Schedule.Set(
        #     mesh='microstructure:skeleton:mesh',
        #     output=AutomaticName('Average Temperature on top'),
        #     scheduletype=AbsoluteOutputSchedule(),
        #     schedule=Periodic(delay=0.0,interval=0.1))
        # OOF.Mesh.Scheduled_Output.Destination.Set(
        #     mesh='microstructure:skeleton:mesh',
        #     output=AutomaticName('Average Temperature on top'),
        #     destination=OutputStream(filename='temptop.out',mode='w'))

        # Set the initial values so that they're the same for the
        # linear and quadratic elements.
        def initfn(x,y,z,t):
            if x + y + z < 0.25:
                return 1 - 4*(x+y+z)
            return 0
        utils.OOFdefine('initfn', initfn)
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Temperature, 
            # initializer=ConstScalarFieldInit(value=0.0)
            initializer=FuncScalarFieldInit(function="initfn(x,y,z,t)")
        )

    def solve(self):
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh', time=0.0)
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh', endtime=4.0)

    def check(self, tolerance):
        self.assert_(file_utils.fp_file_compare(
                'temptop.out',
                os.path.join('mesh_data', 'temptop.out'),
                tolerance))
        file_utils.remove('temptop.out')

    @memorycheck.check("microstructure")
    def LinearCN(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default', 
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    tolerance=1.e-06,
                    initialstep=0,
                    minstep=1.e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=CrankNicolson())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000)))
        self.solve()
        self.check(1.e-6)

    @memorycheck.check("microstructure")
    def NewtonCN(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default', 
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    tolerance=1.e-06,
                    initialstep=0,
                    minstep=1.e-06,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=CrankNicolson())),
                nonlinear_solver=Newton(
                    relative_tolerance=1.e-08,
                    absolute_tolerance=1.e-13,
                    maximum_iterations=200),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000)))
        self.solve()
        self.check(1.e-6)

    @memorycheck.check("microstructure")
    def NewtonSS22(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default', 
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    tolerance=1.e-06,
                    initialstep=0,
                    minstep=1.e-06,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=SS22(theta1=0.5,theta2=0.5))),
                nonlinear_solver=Newton(
                    relative_tolerance=1.e-08,
                    absolute_tolerance=1.e-13,
                    maximum_iterations=200),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000)))
        self.solve()
        self.check(1.e-6)

    def tearDown(self):
        from ooflib.engine.IO import outputdestination
        outputdestination.forgetTextOutputStreams()
        OOF.Material.Delete(name='material')

class OOF_FloatBC1_Linear(OOF_FloatBC1):
    def elementTypes(self):
        return linearElements

class OOF_FloatBC1_Quadratic(OOF_FloatBC1):
    def elementTypes(self):
        return quadraticElements

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    # Using linear finite elements
    OOF_SimpleFloat_Linear("LinearFree"),
    OOF_SimpleFloat_Linear("LinearFloat"),
    OOF_SimpleFloat_Linear("NonlinearFree"),
    OOF_SimpleFloat_Linear("NonlinearFloat"),
    OOF_SimpleFloat_Linear("NonlinearUniformFloat"),

    # Using quadratic finite elements
    OOF_SimpleFloat_Quadratic("NonlinearFree"), # Very slow!
    OOF_SimpleFloat_Quadratic("NonlinearFloat"), # Very slow!
    
    OOF_FloatBC1_Linear("LinearCN"),
    OOF_FloatBC1_Linear("NewtonCN"),
    OOF_FloatBC1_Linear("NewtonSS22"),

    ## OOF_FloatBC1_Quadratic is not a reliable test.  Because it uses
    ## a Dirichlet BC at XminYminZmin, it relies on flux through the
    ## corner of an element, which is different for linear and
    ## quadratic elements.
    # OOF_FloatBC1_Quadratic("LinearCN")
]

# test_set = [
#     OOF_SimpleFloat_Linear("NonlinearFree"),
#     OOF_SimpleFloat_Quadratic("NonlinearFree")
# ]
