# -*- python -*-
# $RCSfile: aniso_test.py,v $
# $Revision: 1.2 $
# $Author: vrc $
# $Date: 2007/09/26 22:03:36 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# Test suite for anisotropic material properties.  Creates and solves
# a system with an anisotropic property, and then solves it again with
# a different orientation.  The two solutions are compared to
# reference solutions.

import unittest, os

import file_compare
fp_file_compare = file_compare.fp_file_compare
# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
file_compare.generate = True

tolerance = 1.e-9

class AnisoTest(unittest.TestCase):
    def setUp(self):
        OOF.File.Load.Data(filename=os.path.join("aniso_data", "mesh.dat"))
    def tearDown(self):
        OOF.Microstructure.Delete(microstructure="microstructure")
        OOF.Property.Delete(property='Color:light')
        OOF.Property.Delete(property='Color:dark')
        OOF.Material.Delete(name='middle')
        OOF.Material.Delete(name='edges')
        try:
            os.remove('mesh.dat')
        except:
            if file_compare.generate:
                pass
            else:
                raise


    def Elasticity(self):
        OOF.Material.Add_property(
            name='edges',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Orthorhombic(
            cijkl=OrthorhombicRank4TensorCij(c11=1, c12=0.5, c13=0.5,
                                             c22=1, c23=0.5, c33=10,
                                             c44=0.25, c55=0.25, c66=0.25))
        OOF.Property.Parametrize.Orientation(
            angles=Axis(angle=90,x=0.0,y=1.0,z=1.0))
        OOF.Material.Add_property(name='middle', property='Orientation')
        OOF.Material.Add_property(
            name='middle',
            property='Mechanical:Elasticity:Anisotropic:Orthorhombic')
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Mesh.Field.In_Plane(
            mesh='microstructure:skeleton:mesh', field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='left'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='left'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ConstantProfile(value=0.1),
                                  boundary='right'))
        OOF.Solver.Solve(
            subproblem='microstructure:skeleton:mesh:default',
            solver=LinearDriver(
            method=CGSolver(max_iterations=1000, tolerance=1e-13,
                            preconditioner=ILUPreconditioner())))
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'elasticity1.dat'),
            tolerance))

        OOF.Property.Parametrize.Orientation(
            angles=Axis(angle=0,x=0.0,y=1.0,z=1.0))
        OOF.Solver.Solve(
            subproblem='microstructure:skeleton:mesh:default',
            solver=LinearDriver(
            method=CGSolver(max_iterations=1000, tolerance=1e-13,
                            preconditioner=ILUPreconditioner())))
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'elasticity2.dat'),
            tolerance))

    def StressFreeStrain(self):
        OOF.Material.Add_property(
            name='middle',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Material.Add_property(
            name='edges',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Material.Add_property(
            name='middle',
            property='Mechanical:StressFreeStrain:Anisotropic:Orthorhombic')
        OOF.Property.Parametrize.Mechanical.StressFreeStrain.Anisotropic.Orthorhombic(
            epsilon0=OrthorhombicRank2Tensor(xx=0.0, yy=0.0, zz=0.1))
        OOF.Material.Add_property(name='middle', property='Orientation')
        OOF.Property.Parametrize.Orientation(
            angles=Axis(angle=90,x=0.0,y=1,z=1.0))
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Mesh.Field.In_Plane(
            mesh='microstructure:skeleton:mesh', field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='x',
                                  equation=Force_Balance,eqn_component='x',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='left'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Displacement,field_component='y',
                                  equation=Force_Balance,eqn_component='y',
                                  profile=ContinuumProfile(function='0'),
                                  boundary='left'))
        OOF.Solver.Solve(
            subproblem='microstructure:skeleton:mesh:default',
            solver=LinearDriver(method=CGSolver(
            max_iterations=1000,tolerance=1e-13,
            preconditioner=ILUPreconditioner())))
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'stressfreestrain1.dat'),
            tolerance))
        OOF.Property.Parametrize.Orientation(
            angles=Axis(angle=0,x=0.0,y=1.0,z=1.0))
        OOF.Solver.Solve(
            subproblem='microstructure:skeleton:mesh:default',
            solver=LinearDriver(method=CGSolver(
            max_iterations=1000,tolerance=1e-13,
            preconditioner=ILUPreconditioner())))
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'stressfreestrain2.dat'),
            tolerance))

    def ThermalConductivity(self):
        OOF.Material.Add_property(
            name='edges', property='Thermal:Conductivity:Isotropic')
        OOF.Property.Parametrize.Thermal.Conductivity.Anisotropic.Orthorhombic(
            kappa=OrthorhombicRank2Tensor(xx=1.0, yy=1.0, zz=10.0))
        OOF.Material.Add_property(
            name='middle',
            property='Thermal:Conductivity:Anisotropic:Orthorhombic')
        OOF.Property.Parametrize.Orientation(
            angles=Axis(angle=90,x=0.0,y=1.0,z=1.0))
        OOF.Material.Add_property(name='middle', property='Orientation')
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Mesh.Field.In_Plane(
            mesh='microstructure:skeleton:mesh', field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Heat_Eqn)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ContinuumProfile(function='1.0'),
                                  boundary='bottomleft'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ContinuumProfile(function='0.0'),
                                  boundary='topright'))
        OOF.Solver.Solve(
            subproblem='microstructure:skeleton:mesh:default',
            solver=LinearDriver(method=CGSolver(
            max_iterations=1000,tolerance=1e-13,
            preconditioner=ILUPreconditioner())))
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'heatcond1.dat'),
            tolerance))
        OOF.Property.Parametrize.Orientation(
            angles=Axis(angle=0,x=0.0,y=1.0,z=1.0))
        OOF.Solver.Solve(
            subproblem='microstructure:skeleton:mesh:default',
            solver=LinearDriver(method=CGSolver(
            max_iterations=1000,tolerance=1e-13,
            preconditioner=ILUPreconditioner())))
        OOF.File.Save.Mesh(filename='mesh.dat', mode='w', format='ascii',
                           mesh='microstructure:skeleton:mesh')
        self.assert_(fp_file_compare(
            'mesh.dat',
            os.path.join('aniso_data', 'heatcond2.dat'),
            tolerance))

    ## TODO: Add tests for the remaining anisotropic properties.

# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.

def run_tests():

    from ooflib.SWIG.common import config
    if config.devel():
        print "Devel mode detected, solver testing skipped."
        return 0
    
    test_set = [
        AnisoTest("Elasticity"),
        AnisoTest("StressFreeStrain"),
        AnisoTest("ThermalConductivity")
        ]


    logan = unittest.TextTestRunner()
    for t in test_set:
        print "\n *** Running test: %s\n" % t.id()
        res = logan.run(t)
        if not res.wasSuccessful():
            return 0
    return 1

###################################################################
# The code below this line should be common to all testing files. #
###################################################################

if __name__=="__main__":
    # If directly run, then start oof, and run the local tests, then quit.
    import sys
    try:
        os.remove("test.dat")
    except:
        pass
    try:
        import oof2
        sys.path.append(os.path.dirname(oof2.__file__))
        from ooflib.common import oof
    except ImportError:
        print "OOF is not correctly installed on this system."
        sys.exit(4)
    sys.argv.append("--text")
    sys.argv.append("--quiet")
    sys.argv.append("--seed=17")
    oof.run(no_interp=1)

    success = run_tests()

    OOF.File.Quit()
    
    if success:
        print "All tests passed."
    else:
        print "Test failure."
