# -*- python -*-
# $RCSfile: nonlinear_floatbc_test.py,v $
# $Revision: 1.1.2.4 $
# $Author: langer $
# $Date: 2014/09/27 22:34:46 $

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

# A trivial linear thermal diffusion problem, with T=1 fixed on the
# left edge, initialized to T=0 in the interior.  Check that the
# solution is the same whether or not there's a floating boundary
# condition on the right edge.

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
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
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
        # OOF.Mesh.Scheduled_Output.New(
        #     mesh='microstructure:skeleton:mesh',
        #     name=AutomaticName('GraphicsUpdate'),
        #     output=GraphicsUpdate())
        # OOF.Mesh.Scheduled_Output.Schedule.Set(
        #     mesh='microstructure:skeleton:mesh',
        #     output=AutomaticName('GraphicsUpdate'),
        #     scheduletype=AbsoluteOutputSchedule(), 
        #     schedule=Periodic(delay=0.0,interval=0.1))

        # OOF.Mesh.Scheduled_Output.New(
        #     mesh='microstructure:skeleton:mesh',
        #     name='right.out', output=GraphicsUpdate())
        # OOF.Mesh.Scheduled_Output.Edit(
        #     mesh='microstructure:skeleton:mesh', 
        #     output='right.out', 
        #     new_output=BoundaryAnalysis(
        #         operation=AverageField(field=Temperature),
        #         boundary='right'))
        # OOF.Mesh.Scheduled_Output.Schedule.Set(
        #     mesh='microstructure:skeleton:mesh',
        #     output='right.out', 
        #     scheduletype=AbsoluteOutputSchedule(),
        #     schedule=Periodic(delay=0.0,interval=0.1))
        # OOF.Mesh.Scheduled_Output.Destination.Set(
        #     mesh='microstructure:skeleton:mesh',
        #     output='right.out',
        #     destination=OutputStream(filename='right.out',mode='w'))

        # Select segments through the middle of the Skeleton,
        # construct a Boundary on those segments, and measure the
        # average temperature on it, in order to have a check that's
        # *not* on the floating BC.
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Toolbox.Viewer.Clip.New(
            normal=VectorDirection(x=1.0,y=0.0,z=0.0), 
            offset=0.499)
        OOF.Graphics_1.Toolbox.Viewer.Restore_Named_View(
            view='Left')
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.543102,0.45989)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.540382,0.465056)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.535488,0.484092)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.542286,0.491162)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.544461,0.505575)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.534944,0.515908)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.535216,0.534128)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.543646,0.54283)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.511557,0.545277)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.518084,0.529777)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.518084,0.518356)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.510198,0.506934)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.509926,0.49361)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.51754,0.481644)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.519715,0.465056)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.508566,0.453091)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.494969,0.45853)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.484364,0.46696)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.48246,0.48382)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.491162,0.493066)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.491706,0.506934)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.484092,0.516452)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.48246,0.536847)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.493066,0.546637)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.456082,0.545005)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.464784,0.534672)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.4656,0.515092)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.457714,0.506119)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.45853,0.490346)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.467232,0.484364)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.467776,0.460977)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='microstructure:skeleton', points=[Point(-2.11376,0.456626,0.456354)], view=View(cameraPosition=Coord(-2.42583,0.5,0.5), focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30, clipPlanes=[[1.0, 0.0, 0.0, 0.499, 0]], invertClip=0, size_x=621, size_y=615), shift=1, ctrl=0)
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

        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='centerpoint.out',
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Temperature),
                operation=DirectOutput(),
                domain=SinglePoint(point=Point(0.5,0.5,0.5)),
                sampling=PointSampleSet(show_x=True,show_y=True,show_z=True)),
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

    def check(self, tolerance):
        self.assert_(file_utils.fp_file_compare(
                'center.out',
                os.path.join('mesh_data', 'simplecenter.out'),
                tolerance))
        file_utils.remove('center.out')

        self.assert_(file_utils.fp_file_compare(
                'middle.out',
                os.path.join('mesh_data', 'simplemiddle.out'),
                tolerance))
        file_utils.remove('middle.out')
                             
        self.assert_(file_utils.fp_file_compare(
                'right.out',
                os.path.join('mesh_data', 'simpleright.out'),
                tolerance))
        file_utils.remove('right.out')

    def tearDown(self):
        from ooflib.engine.IO import outputdestination
        outputdestination.forgetTextOutputStreams()
        OOF.Material.Delete(name='material')
        OOF.Graphics_1.File.Close()

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
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
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

        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Temperature, 
            initializer=ConstScalarFieldInit(value=0.0))

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

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    OOF_SimpleFloat("LinearFree"),
    OOF_SimpleFloat("LinearFloat"),
    OOF_SimpleFloat("NonlinearFree"),
    OOF_SimpleFloat("NonlinearFloat"),
    OOF_SimpleFloat("NonlinearUniformFloat"),
    
    OOF_FloatBC1("LinearCN"),
    OOF_FloatBC1("NewtonCN"),
    OOF_FloatBC1("NewtonSS22")
]

