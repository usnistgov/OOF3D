# -*- python -*-
# $RCSfile: aniso_test.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/09/27 22:34:45 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test suite for anisotropic material properties.  Creates and solves
# a system with an anisotropic property, and then solves it again with
# a different orientation.  The two solutions are compared to
# reference solutions.

import unittest, os

from UTILS import file_utils
reference_file = file_utils.reference_file
# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
file_utils.generate = False

tolerance = 1.e-9

class AnisoTest(unittest.TestCase):
    def setUp(self):
        OOF.File.Load.Data(filename=reference_file("aniso_data", "mesh.dat"))
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=StaticDriver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000)))
    def tearDown(self):
        OOF.Microstructure.Delete(microstructure="microstructure")
        OOF.Property.Delete(property='Color:light')
        OOF.Property.Delete(property='Color:dark')
        OOF.Material.Delete(name='middle')
        OOF.Material.Delete(name='edges')

    def Elasticity(self):
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic(
            cijkl=IsotropicRank4TensorCij(c11=1.0,c12=0.5))
        OOF.Material.Add_property(
            name='edges',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Property.Copy(
            property='Mechanical:Elasticity:Anisotropic:Orthorhombic',
            new_name='new')
        OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Orthorhombic.new(
            cijkl=OrthorhombicRank4TensorCij(c11=1, c12=0.5, c13=0.5,
                                             c22=1, c23=0.5, c33=10,
                                             c44=0.25, c55=0.25, c66=0.25))
        OOF.Property.Copy(
            property='Orientation',
            new_name='new')
        OOF.Property.Parametrize.Orientation.new(
            angles=Axis(angle=90,x=0.0,y=1.0,z=1.0))
        OOF.Material.Add_property(name='middle', property='Orientation:new')
        OOF.Material.Add_property(
            name='middle',
            property='Mechanical:Elasticity:Anisotropic:Orthorhombic:new')
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='z',
                                  equation=Force_Balance,eqn_component='z',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ConstantProfile(value=0.1),
                                  boundary='Xmax'))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'elasticity1.dat'),
            tolerance))
        file_utils.remove('mesh.dat')

        OOF.Property.Parametrize.Orientation.new(
            angles=Axis(angle=0,x=0.0,y=1.0,z=1.0))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'elasticity2.dat'),
            tolerance))
        file_utils.remove('mesh.dat')

        OOF.Property.Delete(
            property='Mechanical:Elasticity:Anisotropic:Orthorhombic:new')
        OOF.Property.Delete(
            property='Orientation:new')

    def StressFreeStrain(self):
        OOF.Material.Add_property(
            name='middle',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Material.Add_property(
            name='edges',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Property.Copy(
            property='Mechanical:StressFreeStrain:Anisotropic:Orthorhombic',
            new_name='new')
        OOF.Material.Add_property(
            name='middle',
            property='Mechanical:StressFreeStrain:Anisotropic:Orthorhombic:new')
        OOF.Property.Parametrize.Mechanical.StressFreeStrain.Anisotropic.Orthorhombic.new(
            epsilon0=OrthorhombicRank2Tensor(xx=0.0, yy=0.0, zz=0.1))
        OOF.Property.Copy(
            property='Orientation',
            new_name='new')
        OOF.Material.Add_property(name='middle', property='Orientation:new')
        OOF.Property.Parametrize.Orientation.new(
            angles=Axis(angle=90,x=0.0,y=1,z=1.0))
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ContinuumProfileXTd(
                    function='0',timeDerivative='0',timeDerivative2='0'),
                boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ContinuumProfileXTd(
                    function='0',timeDerivative='0',timeDerivative2='0'),
                boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ContinuumProfileXTd(
                    function='0',timeDerivative='0',timeDerivative2='0'),
                boundary='Xmin'))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.File.Save.Mesh(filename='mesh1.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            'mesh1.dat',
            os.path.join('aniso_data', 'stressfreestrain1.dat'),
            tolerance))
        OOF.Property.Parametrize.Orientation.new(
            angles=Axis(angle=0,x=0.0,y=1.0,z=1.0))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.File.Save.Mesh(filename='mesh2.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            'mesh2.dat',
            os.path.join('aniso_data', 'stressfreestrain2.dat'),
            tolerance))
        file_utils.remove('mesh1.dat')
        file_utils.remove('mesh2.dat')

        OOF.Property.Delete(
            property='Orientation:new')
        OOF.Property.Delete(
            property='Mechanical:StressFreeStrain:Anisotropic:Orthorhombic:new')

    def ThermalConductivity(self):
        OOF.Material.Add_property(
            name='edges', property='Thermal:Conductivity:Isotropic')
        OOF.Property.Copy(
            property='Thermal:Conductivity:Anisotropic:Orthorhombic',
            new_name='new')
        OOF.Property.Parametrize.Thermal.Conductivity.Anisotropic.Orthorhombic.new(
            kappa=OrthorhombicRank2Tensor(xx=1.0, yy=1.0, zz=10.0))
        OOF.Material.Add_property(
            name='middle',
            property='Thermal:Conductivity:Anisotropic:Orthorhombic:new')
        OOF.Property.Copy(
            property='Orientation',
            new_name='new')
        OOF.Property.Parametrize.Orientation.new(
            angles=Axis(angle=90,x=0.0,y=1.0,z=1.0))
        OOF.Material.Add_property(name='middle', property='Orientation:new')
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
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfileXTd(
                    function='1.0',timeDerivative='0',timeDerivative2='0'),
                boundary='XminYminZmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfileXTd(
                    function='0.0',timeDerivative='0',timeDerivative2='0'),
                boundary='XmaxYmaxZmax'))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'heatcond1.dat'),
            tolerance))
        file_utils.remove('mesh.dat')
        OOF.Property.Parametrize.Orientation.new(
            angles=Axis(angle=0,x=0.0,y=1.0,z=1.0))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'heatcond2.dat'),
            tolerance))
        file_utils.remove('mesh.dat')
        OOF.Property.Delete(
            property='Thermal:Conductivity:Anisotropic:Orthorhombic:new')
        OOF.Property.Delete(
            property='Orientation:new')

    ## TODO: Add tests for the remaining anisotropic properties.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    AnisoTest("Elasticity"),
    AnisoTest("StressFreeStrain"),
    AnisoTest("ThermalConductivity")
]
