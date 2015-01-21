# -*- python -*-
# $RCSfile: scheduled_output_test.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:47 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Tests for the ScheduledOutputs, using Boundary Analysis operations.

## TODO: Add tests that continue a solution.

import unittest, os, sys
import memorycheck

from UTILS import file_utils
# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
file_utils.generate = False

class OOF_ScheduledOutput(unittest.TestCase):
    def setUp(self):
        # Define a problem with both elasticity and thermal
        # conductivity.  The 'time evolution' will be trival because
        # the initial conditions are in equilibrium with the boundary
        # conditions.  This lets us test the outputs against exact
        # solutions, which are:
        #    displacement = (0.1*x, 0)
        #    temperature = y
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(name='material', material_type='bulk')
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic(
            cijkl=IsotropicRank4TensorEnu(
                young=0.66666666666666663,
                poisson=0.0))
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Property.Parametrize.Mechanical.MassDensity.ConstantMassDensity(
            rho=1.0)
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:MassDensity:ConstantMassDensity')
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
        OOF.Material.Assign(
            material='material',
            microstructure='microstructure',
            pixels=every)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Heat_Eqn)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default', 
            equation=Force_Balance)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.0),
                boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(
                    value=0.10000000000000001),
                boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0),
                boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<5>', 
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='Ymax'))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Temperature, 
            initializer=FuncScalarFieldInit(function='y'))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh', 
            field=Displacement, 
            initializer=FuncThreeVectorFieldInit(fx='0.1*x',fy='0.0', fz='0.0'))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh',
            time=0.0)
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=BasicSolverMode(
                time_stepper=BasicUniformDriver(stepsize=0.1),
                matrix_method=BasicIterative(tolerance=1e-13,
                                             max_iterations=1000)))

    def tearDown(self):
        OOF.Material.Delete(name='material')

    def solve(self):
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=1.0)

    def rewind(self):
        OOF.Mesh.Scheduled_Output.RewindAll(
            mesh='microstructure:skeleton:mesh')

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # Routines for creating named and unnamed scheduled outputs.  The
    # test routines all use one or more of these.

    def scheduleUnnamedVectorFluxNormal(self, filename, interval):
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='vfn',
            output=ScheduledAnalysis(
                data=getOutput('Flux:Normal:Value',flux=Heat_Flux),
                operation=IntegrateOutput(),
                domain=FaceBoundaryDomain(boundary='Ymax',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(), 
            schedule=Periodic(delay=0.0,interval=interval),
            destination=OutputStream(filename=filename,mode='w'))

    def scheduleNamedVectorFluxNormal(self, filename, interval):
        OOF.Named_Analysis.Create(
            name='vfn-named',
            operation=IntegrateOutput(),
            data=getOutput('Flux:Normal:Value',flux=Heat_Flux),
            domain=FaceBoundaryDomain(boundary='Ymax',side='FRONT'), 
            sampling=ContinuumSampleSet(order=automatic))
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='vfn<2>', 
            output=NamedAnalysisOutput(analysis='vfn-named'), 
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=interval),
            destination=OutputStream(filename=filename,mode='w'))

    def scheduleUnnamedTensorFluxNormal(self, filename, interval):
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='tfn',
            output=ScheduledAnalysis(
                data=getOutput('Flux:Normal:Value',flux=Stress),
                operation=IntegrateOutput(),
                domain=FaceBoundaryDomain(boundary='Xmin',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(), 
            schedule=Periodic(delay=0.0,interval=interval),
            destination=OutputStream(filename=filename,mode='w'))
        
    def scheduleNamedTensorFluxNormal(self, filename, interval):
        OOF.Named_Analysis.Create(
            name='tfn-named',
            operation=IntegrateOutput(),
            data=getOutput('Flux:Normal:Value',flux=Stress),
            domain=FaceBoundaryDomain(boundary='Xmin',side='FRONT'), 
            sampling=ContinuumSampleSet(order=automatic))
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='tfn<2>', 
            output=NamedAnalysisOutput(analysis='tfn-named'), 
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=interval),
            destination=OutputStream(filename=filename,mode='w'))

    def scheduleUnnamedScalarField(self, filename, interval):
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='sf',
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Temperature),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Xmin',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(), 
            schedule=Periodic(delay=0.0,interval=interval), 
            destination=OutputStream(filename=filename,mode='w'))

    def scheduleNamedScalarField(self, filename, interval):
        OOF.Named_Analysis.Create(
            name='sf-named', operation=AverageOutput(),
            data=getOutput('Field:Value',field=Temperature), 
            domain=FaceBoundaryDomain(boundary='Xmin',side='FRONT'), 
            sampling=ContinuumSampleSet(order=automatic))
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='sf<2>', 
            output=NamedAnalysisOutput(analysis='sf-named'), 
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=interval),
            destination=OutputStream(filename=filename,mode='w'))

    def scheduleUnnamedVectorField(self, filename, interval):
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='vf',
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Displacement),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Xmin',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(), 
            schedule=Periodic(delay=0.0,interval=interval), 
            destination=OutputStream(filename=filename,mode='w'))

    def scheduleNamedVectorField(self, filename, interval):
        OOF.Named_Analysis.Create(
            name='vf-named', operation=AverageOutput(),
            data=getOutput('Field:Value',field=Displacement), 
            domain=FaceBoundaryDomain(boundary='Xmin',side='FRONT'), 
            sampling=ContinuumSampleSet(order=automatic))
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='vf<2>', 
            output=NamedAnalysisOutput(analysis='vf-named'), 
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=interval),
            destination=OutputStream(filename=filename,mode='w'))

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # Actual test routines.
    
    @memorycheck.check('microstructure')
    def UnnamedVectorFlux(self):
        self.scheduleUnnamedVectorFluxNormal('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'vectorfluxoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def NamedVectorFlux(self):
        self.scheduleNamedVectorFluxNormal('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'vectorfluxoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def UnnamedTensorFlux(self):
        self.scheduleUnnamedTensorFluxNormal('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'tensorfluxoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')
    
    @memorycheck.check('microstructure')
    def NamedTensorFlux(self):
        self.scheduleNamedTensorFluxNormal('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'tensorfluxoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')


    @memorycheck.check('microstructure')
    def UnnamedScalarField(self):
        self.scheduleUnnamedScalarField('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'scalarfieldoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')
    
    @memorycheck.check('microstructure')
    def NamedScalarField(self):
        self.scheduleNamedScalarField('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'scalarfieldoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def UnnamedVectorField(self):
        self.scheduleUnnamedVectorField('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'vectorfieldoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')
    
    @memorycheck.check('microstructure')
    def NamedVectorField(self):
        self.scheduleNamedVectorField('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'vectorfieldoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def TwoSeparateUnnamed(self):
        # Two outputs sent to separate files.
        self.scheduleUnnamedVectorField('vtest.dat', 0.1)
        self.scheduleUnnamedTensorFluxNormal('ttest.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'vtest.dat',
                os.path.join('mesh_data', 'vectorfieldoutput.dat'),
                1.e-8))
        self.assert_(file_utils.fp_file_compare(
                'ttest.dat',
                os.path.join('mesh_data', 'tensorfluxoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('vtest.dat')
        file_utils.remove('ttest.dat')

    @memorycheck.check('microstructure')
    def TwoSeparateNamed(self):
        # Two outputs sent to separate files.
        self.scheduleNamedVectorField('vtest.dat', 0.1)
        self.scheduleNamedTensorFluxNormal('ttest.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'vtest.dat',
                os.path.join('mesh_data', 'vectorfieldoutput.dat'),
                1.e-8))
        self.assert_(file_utils.fp_file_compare(
                'ttest.dat',
                os.path.join('mesh_data', 'tensorfluxoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('vtest.dat')
        file_utils.remove('ttest.dat')

    @memorycheck.check('microstructure')
    def TwoTogetherUnnamed(self):
        # Two outputs sent to one file.
        self.scheduleUnnamedVectorField('test.dat', 0.1)
        self.scheduleUnnamedTensorFluxNormal('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'combooutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')
        
    @memorycheck.check('microstructure')
    def TwoTogetherNamed(self):
        # Two outputs sent to one file.
        self.scheduleNamedVectorField('test.dat', 0.1)
        self.scheduleNamedTensorFluxNormal('test.dat', 0.1)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'combooutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')
        
    @memorycheck.check('microstructure')
    def TwoTogetherAsync(self):
        # Two outputs sent to one file.
        self.scheduleUnnamedVectorField('test.dat', 0.1)
        self.scheduleUnnamedTensorFluxNormal('test.dat', 0.2)
        self.solve()
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'asyncoutput.dat'),
                1.e-8))
        self.rewind()
        file_utils.remove('test.dat')
        

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    OOF_ScheduledOutput("UnnamedVectorFlux"),
    OOF_ScheduledOutput("NamedVectorFlux"),
    OOF_ScheduledOutput("UnnamedTensorFlux"),
    OOF_ScheduledOutput("NamedTensorFlux"),
    OOF_ScheduledOutput("UnnamedScalarField"),
    OOF_ScheduledOutput("NamedScalarField"),
    OOF_ScheduledOutput("UnnamedVectorField"),
    OOF_ScheduledOutput("NamedVectorField"),
    OOF_ScheduledOutput("TwoSeparateUnnamed"),
    OOF_ScheduledOutput("TwoSeparateNamed"),
    OOF_ScheduledOutput("TwoTogetherUnnamed"),
    OOF_ScheduledOutput("TwoTogetherNamed"),
    OOF_ScheduledOutput("TwoTogetherAsync")
]
