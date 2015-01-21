# -*- python -*-
# $RCSfile: solver_test.py,v $
# $Revision: 1.1.4.27 $
# $Author: langer $
# $Date: 2014/09/27 22:34:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import unittest, os
import memorycheck
import math
from UTILS import file_utils
reference_file = file_utils.reference_file
file_utils.generate = False

## TODO 3.1: This file doesn't just test the solvers, it also tests the
## Output mechanism, because checking outputs is an easy way to verify
## solutions.  It's not really a good idea to convolute the tests this
## way, though.  We should test the solvers by verifying the actual
## values of the degrees of freedom in the solutions, and test the
## Outputs in a separate file using verified solutions (or on
## artificial field values).

# Shortening is set to 0.1 when running the short versions of the
# time-dependent tests.
shortening = 1.0

class SaveableMeshTest(unittest.TestCase):
    def saveAndLoad(self, filename, suffix=""):
        # Save the mesh in ascii format, and compare with a reference file.
        asciifilename = filename + suffix + "-ascii.dat"
        OOF.File.Save.Mesh(
            filename=asciifilename, mode='w', format='ascii',
            mesh = 'microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
                asciifilename,
                os.path.join('mesh_data', asciifilename),
                1.e-6))
        # Reload the mesh and compare it to the original.  In order to
        # prevent conflicts when reloading, rename the original
        # Microstructure before reloading the saved mesh.
        OOF.Microstructure.Rename(
            microstructure='microstructure', name='original')
        OOF.File.Load.Data(filename=reference_file('mesh_data', asciifilename))
        from ooflib.engine import mesh
        reloaded = mesh.meshes['microstructure:skeleton:mesh']
        original = mesh.meshes['original:skeleton:mesh']
        self.assertEqual(reloaded.compare(original, 1.e-6), 0)
        
        # Delete the reloaded Microstructure, and restore the name of
        # the original Microstructure.
        del reloaded
        OOF.Microstructure.Delete(microstructure='microstructure')
        OOF.Microstructure.Rename(
            microstructure='original', name='microstructure')

        # Save the mesh in binary format, reload it, and compare with the
        # original.
        binaryfilename = filename + suffix + "-binary.dat"
        OOF.File.Save.Mesh(
            filename=binaryfilename, mode='w', format='binary',
            mesh='microstructure:skeleton:mesh')
        OOF.Microstructure.Rename(
            microstructure='microstructure', name='original')
        OOF.File.Load.Data(filename=binaryfilename)
        reloaded = mesh.meshes['microstructure:skeleton:mesh']
        original = mesh.meshes['original:skeleton:mesh']
        self.assertEqual(reloaded.compare(original, 1.e-6), 0)
        print >> sys.stderr, "Successful binary mesh file comparison."
        file_utils.remove(asciifilename)
        file_utils.remove(binaryfilename)
        OOF.Microstructure.Delete(microstructure='original')
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class OOF_StaticIsoElastic(SaveableMeshTest):
    ## Simple test of a microstructure with dimension 1. x 1. x 1. and
    ## a 4x4x4 Skeleton.  The only material property is isotropic
    ## elasticity.  Boundary conditions defined in the file set the
    ## normal component of the displacement on each face to be zero.
    def setUp(self):
        global mesh
        from ooflib.engine import mesh
        OOF.File.Load.Data(filename=reference_file("mesh_data", "simple_mesh"))
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=BasicSolverMode(
                time_stepper=BasicStaticDriver(),
                matrix_method=BasicIterative(
                    tolerance=1e-13,max_iterations=1000)))

    def tearDown(self):
        OOF.Material.Delete(name="material")

    @memorycheck.check("microstructure")
    def Null(self):             # Establish baseline for memory leak tests
        pass

    def checkUniformSolution(self, dx, dy, dz):
        msh_obj = mesh.meshes["microstructure:skeleton:mesh"].getObject()
        for fn in msh_obj.funcnodes():
            pos = fn.displaced_position(msh_obj, 1.0) # a Point
            self.assertAlmostEqual(pos[0], (1+dx)*fn[0], 10)
            self.assertAlmostEqual(pos[1], (1+dy)*fn[1], 10)
            self.assertAlmostEqual(pos[2], (1+dz)*fn[2], 10)


    def checkSolution(self, fx=lambda x,y,z:x, fy=lambda x,y,z:y,
                      fz=lambda x,y,z:z):
        msh_obj = mesh.meshes["microstructure:skeleton:mesh"].getObject()
        for fn in msh_obj.funcnodes():
            pos = fn.displaced_position(msh_obj, 1.0)
            print >> sys.stderr, fn, \
                "actual=(%g,%g,%g)"% (pos[0], pos[1], pos[2]),\
                "expected=(%g,%g,%g)" % (
                    fx(fn[0], fn[1], fn[2]),
                    fy(fn[0], fn[1], fn[2]),
                    fz(fn[0], fn[1], fn[2]))
            self.assertAlmostEqual(pos[0], fx(fn[0], fn[1], fn[2]), 8)
            self.assertAlmostEqual(pos[1], fy(fn[0], fn[1], fn[2]), 8)
            self.assertAlmostEqual(pos[2], fz(fn[0], fn[1], fn[2]), 8)
        
    # Test with 0 displacement on all faces
    @memorycheck.check("microstructure")
    def Solve0(self):
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)

        # Then look for evidence that it worked.  Direct evidence
        # would be that the solution exists and is right, so poll
        # DOFs.  The exact solution is displacement(x,y,z) = (0, 0, 0)
        self.checkUniformSolution(0, 0, 0)
        self.saveAndLoad("static-isotropic-null")

    ## Tests with Dirichlet BCs.

    # Positive x displacement of the right face.
    @memorycheck.check("microstructure")
    def SolvePlusX(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.1),
                boundary='Xmax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.checkUniformSolution(0.1, 0.0, 0.0)
        self.saveAndLoad("static-isotropic-plusX")

    # Negative x displacement of the right face.
    @memorycheck.check("microstructure")
    def SolveMinusX(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=-0.1),
                boundary='Xmax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.checkUniformSolution(-0.1, 0.0, 0.0)
        self.saveAndLoad("static-isotropic-minusX")

    # Positive y displacement of the top face.
    @memorycheck.check("microstructure")
    def SolvePlusY(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<3>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.1),
                boundary='Ymax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.checkUniformSolution(0.0, 0.1, 0.0)
        self.saveAndLoad("static-isotropic-plusY")

    # Negative y displacement of the top face.
    @memorycheck.check("microstructure")
    def SolveMinusY(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<3>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=-0.1),
                boundary='Ymax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.checkUniformSolution(0.0, -0.1, 0.0)
        self.saveAndLoad("static-isotropic-minusY")

    # Positive z displacement of the right face.
    @memorycheck.check("microstructure")
    def SolvePlusZ(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<5>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=0.1),
                boundary='Zmax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.checkUniformSolution(0.0, 0.0, 0.1)
        self.saveAndLoad("static-isotropic-plusZ")

    # Negative y displacement of the top face.
    @memorycheck.check("microstructure")
    def SolveMinusZ(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<5>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=-0.1),
                boundary='Zmax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.checkUniformSolution(0.0, 0.0, -0.1)
        self.saveAndLoad("static-isotropic-minusZ")

    ## Tests with floating BCs.

    @memorycheck.check("microstructure")
    def SolveFloatFlatX(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc',
            mesh='microstructure:skeleton:mesh', 
            condition=FloatBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=1),
                boundary='Xmax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.checkUniformSolution(0, 0, 0)
        self.saveAndLoad("static-isotropic-float-flatX")

    @memorycheck.check("microstructure")
    def SolveFloatTiltX(self):
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc',
            mesh='microstructure:skeleton:mesh', 
            condition=FloatBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ContinuumProfile(function='0.1*(y+z)'),
                boundary='Xmax'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.saveAndLoad("static-isotropic-float-tiltX")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# OOF_AnisoRotation tests that an anisotropic property is rotated
# correctly by solving a thermal conductivity problem.  To regenerate
# the reference file for this test, change the first line
# mesh_data/anisotherm.log to "generate=True", load that file into
# oof2, and save the resulting mesh into mesh_data/anisotherm.mesh.

class OOF_AnisoRotation(SaveableMeshTest):
    def setUp(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='materialx',
            material_type='bulk')
        OOF.Property.Copy(
            property='Orientation', 
            new_name='flexible')
        OOF.Property.Parametrize.Orientation.flexible(
            angles=Abg(alpha=0,beta=30,gamma=0))
        OOF.Material.Add_property(
            name='materialx', property='Orientation:flexible')
        OOF.Property.Copy(
            property='Thermal:Conductivity:Anisotropic:Monoclinic', 
            new_name='mono')
        OOF.Property.Parametrize.Thermal.Conductivity.Anisotropic.Monoclinic.mono(
            kappa=MonoclinicRank2Tensor(xx=10.0, yy=1.0, zz=1.0, xz=0.5))
        OOF.Material.Add_property(
            name='materialx', 
            property='Thermal:Conductivity:Anisotropic:Monoclinic:mono')
        OOF.Material.Assign(
            material='materialx', microstructure='microstructure', pixels=every)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=6, y_elements=6, z_elements=6,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh', 
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                profile=ConstantProfile(value=0.0),
                boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='Ymin'))
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default', 
            solver_mode=BasicSolverMode(
                time_stepper=BasicStaticDriver(),
                matrix_method=BasicIterative(
                    tolerance=1e-13,max_iterations=1000)))

    # First, check the trivial case with isotropic conductivity.
    @memorycheck.check("microstructure")
    def Solve00(self):
        OOF.Material.New(
            name='isotropic', material_type='bulk')
        OOF.Material.Add_property(
            name='isotropic',
            property='Thermal:Conductivity:Isotropic')
        OOF.Material.Assign(
            material='isotropic', 
            microstructure='microstructure',
            pixels=every)
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        self.saveAndLoad("aniso00")
        OOF.Material.Delete(name="isotropic")

    # Then check with anisotropic conductivity, but unrotated.
    @memorycheck.check("microstructure")
    def Solve0(self):
        OOF.Property.Parametrize.Orientation.flexible(
            angles=Abg(alpha=0,beta=0,gamma=0))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        self.saveAndLoad("aniso0")

    # Finally the full rotated anisotropic system.
    @memorycheck.check("microstructure")
    def Solve(self):
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        self.saveAndLoad("aniso")

    def tearDown(self):
        OOF.Material.Delete(name="materialx")
        OOF.Property.Delete(property='Orientation:flexible')
        OOF.Property.Delete(
            property='Thermal:Conductivity:Anisotropic:Monoclinic:mono')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Basic Neumann boundary condition tests for elasticity and thermal
# conductivity.  Different Microstructure sizes are tested by having
# subclasses that contain microstructureSize and skeletonSize tuples.
# microstructureSize is the physical size of the Microstructure.
# skeletonSize is the element size of the Skeleton.  Subclasses also
# need to define 'testname', which is embedded in the reference data
# file names to distinguish one test from another.

class OOF_NeumannBase(unittest.TestCase):
    def setUp(self):
        mx, my, mz = self.microstructureSize
        sx, sy, sz = self.skeletonSize
        OOF.Microstructure.New(
            name='microstructure', 
            width=mx, height=my, depth=mz, 
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material',
            microstructure='microstructure',
            pixels=every)
        OOF.Property.Copy(
            property='Mechanical:Elasticity:Isotropic',
            new_name='instance')
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic:instance')
        OOF.Property.Copy(
            property='Thermal:Conductivity:Isotropic', 
            new_name='instance')
        OOF.Material.Add_property(
            name='material',
            property='Thermal:Conductivity:Isotropic:instance')
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=sx, y_elements=sy, z_elements=sz,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'Q4_4', 'T3_3', 'D2_2'])
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default', 
            solver_mode=BasicSolverMode(
                time_stepper=BasicStaticDriver(),
                matrix_method=BasicIterative(
                    tolerance=1e-13,max_iterations=1000)))
    def solve(self):
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh', 
            endtime=0.0)

    def compare(self, filename):
        realfilename = filename + '-' + self.testname
        OOF.File.Save.Mesh(
            filename=realfilename,
            mode='w', format='ascii',
            mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            realfilename,
            os.path.join('mesh_data', realfilename),
            1.e-6))
        file_utils.remove(realfilename)
    def tearDown(self):
        OOF.Material.Delete(name='material')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:instance')
        OOF.Property.Delete(property='Thermal:Conductivity:Isotropic:instance')

class NeumannElastic(OOF_NeumannBase):
    def setUp(self):
        OOF_NeumannBase.setUp(self)
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default', 
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
    def makeDirichletBCs(self, exclude=[]):
        for bdyname in ('Xmax', 'Xmin', 'Ymax', 'Ymin', 'Zmax', 'Zmin'):
            if bdyname not in exclude:
                comp = bdyname[0].lower()
                # restrict out of plane motion only
                OOF.Mesh.Boundary_Conditions.New(
                    name='dirichlet-'+bdyname, 
                    mesh='microstructure:skeleton:mesh',
                    condition=DirichletBC(
                        field=Displacement, field_component=comp,
                        equation=Force_Balance, eqn_component=comp,
                        profile=ConstantProfile(value=0.0),
                        boundary=bdyname))
    def normalForce(self, bdyname, force):
        comp = bdyname[0].lower()
        profile=[ConstantProfile(value=0.0),
                 ConstantProfile(value=0.0),
                 ConstantProfile(value=0.0)]
        which = 'xyz'.index(comp)
        profile[which] = ConstantProfile(value=force)
        OOF.Mesh.Boundary_Conditions.New(
            name='neumann-'+bdyname,
            mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(
                flux=Stress,
                profile=profile,
                boundary=bdyname))

    @memorycheck.check("microstructure")
    def NullXmin(self):
        self.makeDirichletBCs(exclude=['Xmin'])
        self.normalForce('Xmin', 0.0)
        self.solve()
        self.compare('neumann-elasticity-xmin-0')

    @memorycheck.check("microstructure")
    def NullZmax(self):
        self.makeDirichletBCs(exclude=['Zmax'])
        self.normalForce('Zmax', 0.0)
        self.solve()
        self.compare('neumann-elasticity-zmax-0')

    @memorycheck.check("microstructure")
    def Xmax01(self):
        self.makeDirichletBCs(exclude=['Xmax'])
        self.normalForce('Xmax', 0.1)
        self.solve()
        self.compare('neumann-elasticity-xmax-0.1')

    @memorycheck.check("microstructure")
    def Ymax01(self):
        self.makeDirichletBCs(exclude=['Ymax'])
        self.normalForce('Ymax', 0.1)
        self.solve()
        self.compare('neumann-elasticity-ymax-0.1')

    @memorycheck.check("microstructure")
    def Zmin01(self):
        self.makeDirichletBCs(exclude=["Zmin"])
        self.normalForce('Zmin', 0.1)
        self.solve()
        self.compare('neumann-elasticity-zmin-0.1')

class NeumannThermal(OOF_NeumannBase):
    def setUp(self):
        OOF_NeumannBase.setUp(self)
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Heat_Eqn)
    def makeDirichletBCs(self, include=[]):
        for bdyname in include:
            OOF.Mesh.Boundary_Conditions.New(
                name='dirichlet-'+bdyname, 
                mesh='microstructure:skeleton:mesh',
                condition=DirichletBC(
                    field=Temperature, field_component='',
                    equation=Heat_Eqn, eqn_component='',
                    profile=ConstantProfile(value=0.0),
                    boundary=bdyname))
    def heatFlux(self, bdyname, flux):
        OOF.Mesh.Boundary_Conditions.New(
            name=bdyname, 
            mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(
                flux=Heat_Flux,
                profile=ConstantProfile(value=flux),
                boundary=bdyname))

    @memorycheck.check("microstructure")
    def NullXmin(self):
        self.makeDirichletBCs(['Xmax'])
        self.heatFlux('Xmin', 0)
        self.solve()
        self.compare("neumann-thermal-xmin-0")

    @memorycheck.check("microstructure")
    def NullZmax(self):
        self.makeDirichletBCs(['Zmin'])
        self.heatFlux('Zmax', 0)
        self.solve()
        self.compare("neumann-thermal-zmax-0")

    @memorycheck.check("microstructure")
    def Xmax01(self):
        self.makeDirichletBCs(['Xmin'])
        self.heatFlux('Xmax', 0.1)
        self.solve()
        self.compare("neumann-thermal-xmax-0.1")

    @memorycheck.check("microstructure")
    def Ymax01(self):
        self.makeDirichletBCs(['Ymin'])
        self.heatFlux('Ymax', 0.1)
        self.solve()
        self.compare("neumann-thermal-ymax-0.1")

    @memorycheck.check("microstructure")
    def Zmin01(self):
        self.makeDirichletBCs(['Zmax'])
        self.heatFlux('Zmin', 0.1)
        self.solve()
        self.compare("neumann-thermal-zmin-0.1")


class MeshGeometry1:
    testname = "m1s4"
    microstructureSize = (1., 1., 1.)
    skeletonSize = (4, 4, 4)

class MeshGeometry2:
    testname = "m2s4"
    microstructureSize = (2., 2., 2.)
    skeletonSize = (4, 4, 4)

class MeshGeometry3:
    testname = "m1s6"
    microstructureSize = (1., 1., 1.)
    skeletonSize = (6, 6, 6)

class MeshGeometry4:
    testname = "m123s4"
    microstructureSize = (1., 2., 3.)
    skeletonSize = (4, 4, 4)

class OOF_ElasticNeumann1(NeumannElastic, MeshGeometry1):
    pass

class OOF_ElasticNeumann2(NeumannElastic, MeshGeometry2):
    pass

class OOF_ElasticNeumann3(NeumannElastic, MeshGeometry3):
    pass
    
class OOF_ElasticNeumann4(NeumannElastic, MeshGeometry4):
    pass

class OOF_ThermalNeumann1(NeumannThermal, MeshGeometry1):
    pass

class OOF_ThermalNeumann2(NeumannThermal, MeshGeometry2):
    pass

class OOF_ThermalNeumann3(NeumannThermal, MeshGeometry3):
    pass

class OOF_ThermalNeumann4(NeumannThermal, MeshGeometry4):
    pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## OOF_NonrectMixedBCStaticElastic is a full blown test of a lot of
## features.  It creates a microstructure by selecting pixels and
## assigning a Material to *some* of them, so the microstructure isn't
## rectangular.  (Actually, the 3D version loads a pre-created
## Microstructure and Mesh).  It then solves a simple static
## elasticity problem with Dirichlet, Neumann, and Floating BCs all
## mixed together.

class OOF_NonrectMixedBCStaticElastic(SaveableMeshTest):
    def setUp(self):
        OOF.File.Load.Data(
            filename=reference_file("mesh_data", "everythingbagel0.mesh"))

    @memorycheck.check("solved", "microstructure")
    def Solve1(self):
        OOF.Mesh.Solve(mesh="microstructure:skeleton:mesh", endtime=0.0)
        # Rename the microstructure, load in a pre-solved version, and
        # compare.
        OOF.Microstructure.Rename(
            microstructure='microstructure', 
            name='solved')
        OOF.File.Load.Data(
            filename=reference_file("mesh_data", "everythingbagel1.mesh"))
        
        from ooflib.engine import mesh
        saved = mesh.meshes["solved:skeleton:mesh"]
        damned = mesh.meshes["microstructure:skeleton:mesh"]
        self.assertEqual(saved.compare(damned, 1.0e-13), 0)

        # Check that re-solving the mesh works. 
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh', endtime=0.0)
        self.assertEqual(saved.compare(damned, 1.0e-13), 0)

    @memorycheck.check("microstructure")
    def Solve2(self):
        OOF.Mesh.Solve(mesh="microstructure:skeleton:mesh", endtime=0.0)
        # Change the value of the Neumann condition
        OOF.Mesh.Boundary_Conditions.Edit(
            name='weight',
            mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(
                flux=Stress,profile=[ConstantProfile(value=0.0),
                                     ConstantProfile(value=-0.02),
                                     ConstantProfile(value=0.0)],
                boundary='rightface'))
        # Change the profile of the Floating condition
        OOF.Mesh.Boundary_Conditions.Edit(
            name='float',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ContinuumProfile(function='0.1*(0.5-z)**2'),
                boundary='topedge'))
        # Resolve
        OOF.Mesh.Solve(mesh="microstructure:skeleton:mesh", endtime=0.0)
        self.saveAndLoad("everythingbagel2")
        # Change the Neumann condition again
        OOF.Mesh.Boundary_Conditions.Edit(
            name='weight', 
            mesh='microstructure:skeleton:mesh', 
            condition=NeumannBC(
                flux=Stress,
                profile=[ConstantProfile(value=0.0),
                         ConstantProfile(value=0.02), 
                         ConstantProfile(value=0.0)],
                boundary='rightface'))
        # Solve again
        OOF.Mesh.Solve(mesh="microstructure:skeleton:mesh", endtime=0.0)
        self.saveAndLoad("everythingbagel3")

    def tearDown(self):
        OOF.Material.Delete(name='material')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:stuff')
        OOF.Property.Delete(property="Color:gray")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class OOF_SimplePiezo(SaveableMeshTest):
    @memorycheck.check("microstructure")
    def Solve(self):
        from ooflib.engine.IO import outputdestination
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material', microstructure='microstructure', pixels=all)
        # Reset the default parameter values for Properties..  This
        # shouldn't be necessary if earlier tests clean up after
        # themselves properly.
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic(
            cijkl=IsotropicRank4TensorCij(c11=1.0,c12=0.5))
        OOF.Material.Add_property(
            name='material', property='Mechanical:Elasticity:Isotropic')
        OOF.Property.Parametrize.Electric.DielectricPermittivity.Isotropic(
            epsilon=1.0)
        OOF.Material.Add_property(
            name='material',
            property='Electric:DielectricPermittivity:Isotropic')
        OOF.Property.Parametrize.Couplings.PiezoElectricity.Cubic.Td(
            dijk=TdRank3Tensor(d14=1))
        OOF.Material.Add_property(
            name='material', property='Couplings:PiezoElectricity:Cubic:Td')
        OOF.Property.Parametrize.Orientation(
            angles=Abg(alpha=0,beta=0,gamma=0))
        OOF.Material.Add_property(
            name='material', property='Orientation')
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=3, y_elements=3, z_elements=3,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh', 
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Voltage)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Voltage)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Coulomb_Eqn)
        # Displacement is defined and initialized non-trivially, but
        # not activated, so it should lead to a non-zero polarization.
        # We only need a trivial boundary condition on Voltage.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Voltage,field_component='',
                equation=Coulomb_Eqn,eqn_component='',
                profile=ContinuumProfileXTd(
                    function='0',timeDerivative='0',timeDerivative2='0'),
                boundary='XminYminZmin'))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh', 
            field=Displacement,
            initializer=FuncThreeVectorFieldInit(
                fx='0.1*y',fy='0.1*z',fz='0.1*x'))
        OOF.Mesh.Apply_Field_Initializers(mesh="microstructure:skeleton:mesh")
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=BasicSolverMode(
                time_stepper=BasicStaticDriver(),
                matrix_method=BasicIterative(tolerance=1e-13,
                                             max_iterations=1000)))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.Mesh.Analyze.Average(
            mesh='microstructure:skeleton:mesh',
            data=getOutput('Flux:Value',flux=Total_Polarization),
            time=latest,
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic),
            destination=OutputStream(filename='test.dat', mode='w'))

        outputdestination.forgetTextOutputStreams()
        self.assert_(
            file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'piezopolar.dat'),
                1.e-10))
        file_utils.remove('test.dat')
        OOF.Mesh.Analyze.Average(
            mesh='microstructure:skeleton:mesh',
            data=getOutput('Field:Value',field=Voltage),
            time=latest,
            domain=EntireMesh(),
            sampling=ContinuumSampleSet(order=automatic),
            destination=OutputStream(filename='test.dat', mode='w'))
        outputdestination.forgetTextOutputStreams()
        self.assert_(
            file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'piezovoltage.dat'),
                1.e-10))
        file_utils.remove('test.dat')
    def tearDown(self):
        OOF.Material.Delete(name='material')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Check that solving a static problem after a nonstatic problem on the
# same mesh works correctly.

class OOF_NonstaticThenStatic(SaveableMeshTest):
    @memorycheck.check("microstructure")
    def Solve(self):
        OOF.File.Load.Script(filename=reference_file("mesh_data",
                                                   "timenotime.log"))
        from ooflib.engine import mesh
        mesh0 = mesh.meshes["microstructure:skeleton:mesh"]
        mesh1 = mesh.meshes["microstructure:skeleton:mesh<2>"]
        self.assertEqual(mesh0.compare(mesh1, 1.0e-13), 0)
    def tearDown(self):
        OOF.Material.Delete(name='material')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Check that a simple time dependent problem is solved correctly.  The
# 1x1 linear quad grid with isotropic elasticity (default parameters)
# has an oscillation period of 2*pi/sqrt(3).  This test runs the time
# evolution for one period and checks it against the exact solution of
# the discretized problem.

## TODO MER: Repeat this test in 3D.  Print out the M and K matrices to
## figure out what the frequency ought to be.

class OOF_1x1ElasticDynamic(SaveableMeshTest):
    def setUp(self):
        global outputdestination
        from ooflib.engine.IO import outputdestination
        OOF.File.LoadStartUp.Data(
            filename=reference_file('mesh_data', 'simplespring.mesh'))

    @memorycheck.check("microstructure")
    def Static(self):
        # OOF.Mesh.Set_Field_Initializer(
        #     mesh='microstructure:skeleton:mesh',
        #     field=Displacement,
        #     initializer=ConstTwoVectorFieldInit(cx=0, cy=0))
        # OOF.Mesh.Apply_Field_Initializers_at_Time(
        #     mesh='microstructure:skeleton:mesh', time=0.0)
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=StaticDriver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        # Check that all displacements are zero.
        from ooflib.engine import mesh
        msh_obj = mesh.meshes['microstructure:skeleton:mesh'].getObject()
        for fn in msh_obj.funcnodes():
            dispx = Displacement.value(msh_obj, fn, 0)
            dispy = Displacement.value(msh_obj, fn, 1)
            rr = dispx*dispx + dispy*dispy
            self.assertAlmostEqual(rr, 0.0, 6)

    @memorycheck.check("microstructure")
    def Dynamic(self):
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name=AutomaticName('Average Displacement on right'),
            output=BoundaryAnalysis(
                operation=AverageField(field=Displacement),boundary='right'))
        OOF.Mesh.Scheduled_Output.Schedule.Set(
            mesh='microstructure:skeleton:mesh',
            output=AutomaticName('Average Displacement on right'),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=0.01*shortening))
        OOF.Mesh.Scheduled_Output.Destination.Set(
            mesh='microstructure:skeleton:mesh',
            output=AutomaticName('Average Displacement on right'),
            destination=OutputStream(filename='springtest.out',mode='w'))
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=AdaptiveDriver(
                    tolerance=1.e-6,
                    initialstep=0,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=SS22(theta1=0.5,theta2=0.5))
                    ),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000)
                )
            )
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Displacement_t,
            initializer=ConstTwoVectorFieldInit(cx=0.0,cy=0.0))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh', time=0.0)
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=3.6275987284684357*shortening)

        self.assert_(file_utils.fp_file_compare(
                'springtest.out',
                os.path.join('mesh_data', 'springtest.exact'),
                1.e-4))
        file_utils.remove('springtest.out')
    def tearDown(self):
        outputdestination.forgetTextOutputStreams()
        OOF.Material.Delete(name='material')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Use various time steppers to solve a simple thermal diffusion
# problem.

class OOF_ThermalDiffusionTimeSteppers(SaveableMeshTest):
    def setUp(self):
        global outputdestination
        from ooflib.engine.IO import outputdestination
        global mesh
        from ooflib.engine import mesh
        OOF.Microstructure.New(
            name='microstructure', width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(name='material', material_type='bulk')
        OOF.Material.Add_property(
            name='material', property='Thermal:Conductivity:Isotropic')
        OOF.Material.Add_property(
            name='material',
            property='Thermal:HeatCapacity:ConstantHeatCapacity')
        OOF.Material.Assign(
            material='material', microstructure='microstructure', pixels=all)
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
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
                profile=ConstantProfile(value=2),boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),boundary='Xmax'))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Temperature,
            initializer=ConstScalarFieldInit(value=4))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh', time=0.0)
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name=AutomaticName('Average Temperature on top'),
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Temperature),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Ymax',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=0.05*shortening),
            destination=OutputStream(filename='test.dat',mode='w'))

    @memorycheck.check('microstructure')
    def CNdirect(self):
        # Use CN to generate the reference files, and do it with a
        # tight tolerance.
        if file_utils.generate:
            tol = 1.e-8
        else:
            tol = 1.e-6

        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    tolerance=tol,
                    initialstep=0.01,
                    minstep=1e-06,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=CrankNicolson())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=DirectMatrixSolver(),
                asymmetric_solver=DirectMatrixSolver()))

        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-5))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def SS22directSaveRestore(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=1.e-6,
                    minstep=1e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=SS22(theta1=0.5,theta2=0.5))),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=DirectMatrixSolver(),
                asymmetric_solver=DirectMatrixSolver()
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-3))
        file_utils.remove('test.dat')

        self.saveAndLoad('timedep-thermo')

    @memorycheck.check('microstructure')
    def BEdirect(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-5,
                    minstep=1e-6,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=BackwardEuler())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=DirectMatrixSolver(),
                asymmetric_solver=DirectMatrixSolver()
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-3))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def RK4direct(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-6,
                    minstep=1e-5,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=RK4())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=DirectMatrixSolver(),
                asymmetric_solver=DirectMatrixSolver()
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-6))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def RK2direct(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-5,
                    minstep=1e-5,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=RK2())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=DirectMatrixSolver(),
                asymmetric_solver=DirectMatrixSolver()
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-3))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def SS22(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=1e-6,
                    minstep=1e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=SS22(theta1=0.5,theta2=0.5))),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-3))

        # Repeat, because there seems to be some problem with repeated
        # SS22 nonlinear solutions, so it's good to know if repeated
        # linear solutions work.
        OOF.Mesh.Scheduled_Output.RewindAll(
            mesh='microstructure:skeleton:mesh')
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh', time=0.0)

        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-3))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def CN(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-7,
                    minstep=1e-5,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=CrankNicolson())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-6))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def CNdouble(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-7,
                    minstep=1e-5,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=CrankNicolson())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        # Get there in two stages.
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.25*shortening)
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-6))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def BE(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-5,
                    minstep=1e-06,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=BackwardEuler())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-3))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def RK4(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-6,
                    minstep=1e-5,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=RK4())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-6))
        file_utils.remove('test.dat')

    @memorycheck.check('microstructure')
    def RK2(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0.001,
                    tolerance=1e-5,
                    minstep=1e-5,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(singlestep=RK2())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.5*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgtemp.dat'),
                1.e-3))
        file_utils.remove('test.dat')

    def tearDown(self):
        outputdestination.forgetTextOutputStreams()
        OOF.Material.Delete(name='material')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Check that a simple elasticity problem can be solved exactly.

class OOF_ElasticExact(SaveableMeshTest):
    def setUp(self):
        global outputdestination
        from ooflib.engine.IO import outputdestination

        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material', microstructure='microstructure', pixels=all)
        OOF.Property.Copy(
            property='Mechanical:Elasticity:Isotropic',
            new_name='iso8')
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.iso8(
            cijkl=IsotropicRank4TensorEnu(young=0.66666666666666663,
                                          poisson=0.2))
        OOF.Material.Add_property(
            name='material', property='Mechanical:Elasticity:Isotropic:iso8')
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh', skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
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
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.0),boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.1),boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<5>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=0.0),boundary='Zmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<6>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=0.0),boundary='Zmax'))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Displacement,
            initializer=ConstThreeVectorFieldInit(cx=0.0,cy=0.0,cz=0.0))

    @memorycheck.check("microstructure")
    def Solve(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=StaticDriver(),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.Mesh.Analyze.Integral(
            mesh='microstructure:skeleton:mesh',
            time=latest,
            data=getOutput('Flux:Normal:Value',flux=Stress),
            domain=FaceBoundaryDomain(boundary='Xmax',side='FRONT'),
            sampling=ContinuumSampleSet(order=automatic),
            destination=OutputStream(filename='test.dat', mode='w'))
        self.assert_(file_utils.compare_last('test.dat',
                                             (0.0, 0.0740740741, 0.0, 0.0)))
        OOF.Mesh.Analyze.Integral(
            mesh='microstructure:skeleton:mesh',
            time=latest,
            data=getOutput('Flux:Normal:Value',flux=Stress),
            domain=FaceBoundaryDomain(boundary='Xmin',side='FRONT'),
            sampling=ContinuumSampleSet(order=automatic),
            destination=OutputStream(filename='test.dat', mode='w'))
        self.assert_(file_utils.compare_last('test.dat',
                                             (0.0, -0.0740740741, 0.0, 0.0)))
        OOF.Mesh.Analyze.Average(
            mesh='microstructure:skeleton:mesh',
            time=latest, 
            data=getOutput('Flux:Value',flux=Stress),
            domain=FaceBoundaryDomain(boundary='Xmax',side='FRONT'),
            sampling=ContinuumSampleSet(order=automatic),
            destination=OutputStream(filename='test.dat', mode='w'))
        self.assert_(file_utils.compare_last(
            'test.dat',
            (0.0, 0.0740740740741, 0.0185185185185, 0.0185185185185, 0.0, 0.0,
             0.0)))
        file_utils.remove('test.dat')

    def tearDown(self):
        outputdestination.forgetTextOutputStreams()
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:iso8')
        OOF.Material.Delete(name="material")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# ElasticTimeSteppers is a dynamic version of ElasticExact, except
# that it's done with a smaller z-size, for speed, and the right hand
# BC is Neumann. We're not comparing to an exact solution, but are
# checking that different steppers give the same answer.

class OOF_ElasticTimeSteppers(OOF_ElasticExact):
    def setUp(self):
        global outputdestination
        from ooflib.engine.IO import outputdestination

        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=0.3,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=3)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material', microstructure='microstructure', pixels=all)
        OOF.Property.Copy(
            property='Mechanical:Elasticity:Isotropic',
            new_name='iso8')
        OOF.Property.Parametrize.Mechanical.Elasticity.Isotropic.iso8(
            cijkl=IsotropicRank4TensorEnu(young=0.66666666666666663,
                                          poisson=0.2))
        OOF.Material.Add_property(
            name='material', property='Mechanical:Elasticity:Isotropic:iso8')

        OOF.Property.Copy(
            property='Mechanical:MassDensity:ConstantMassDensity',
            new_name='massdensity')
        OOF.Property.Parametrize.Mechanical.MassDensity.ConstantMassDensity.massdensity(
        rho=1.0)
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:MassDensity:ConstantMassDensity:massdensity')

        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=1,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh', skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
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
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.0),boundary='Xmin'))
        # BC on the right face is Neumann.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(
                flux=Stress,
                profile=[ConstantProfile(value=0.1),
                         ConstantProfile(value=0.0), 
                         ConstantProfile(value=0.0)],
                boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<5>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=0.0),boundary='Zmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<6>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=0.0),boundary='Zmax'))

        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='right',
            output=ScheduledAnalysis(
                data=getOutput('Field:Value',field=Displacement),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Xmax',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=0.1*shortening),
        destination=OutputStream(filename='test.dat', mode='w'))

        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='zz',
            output=ScheduledAnalysis(
                data=getOutput('Flux:Value',flux=Stress),
                operation=AverageOutput(),
                domain=EntireMesh(),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0,interval=0.1*shortening),
        destination=OutputStream(filename='testz.dat',mode='w'))

        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Displacement,
            initializer=ConstThreeVectorFieldInit(cx=0.0,cy=0.0,cz=0.0))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Displacement_t,
            initializer=ConstThreeVectorFieldInit(cx=0.0,cy=0.0,cz=0.0))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh',
            time=0.0)

    def tearDown(self):
        OOF.Property.Delete(
            property='Mechanical:MassDensity:ConstantMassDensity:massdensity')
        OOF_ElasticExact.tearDown(self)

    @memorycheck.check("microstructure")
    def SS22(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=0.000001,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=SS22(theta1=0.5,theta2=0.5))),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=2.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgdisp.dat'),
                1.e-6))
        self.assert_(file_utils.fp_file_compare(
                'testz.dat',
                os.path.join('mesh_data', 'stress.dat'),
                1.e-6))
        file_utils.remove('test.dat')
        file_utils.remove('testz.dat')

    @memorycheck.check("microstructure")
    def CNSaveRestore(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=0.00001,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=CrankNicolson())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=2.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgdisp.dat'),
                1.e-4))
        self.assert_(file_utils.fp_file_compare(
                'testz.dat',
                os.path.join('mesh_data', 'stress.dat'),
                1.e-4))
        file_utils.remove('test.dat')
        file_utils.remove('testz.dat')

        self.saveAndLoad("timedep-elastic")

    @memorycheck.check("microstructure")
    def RK4(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    tolerance=0.00001,
                    initialstep=0,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=RK4())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=2.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgdisp.dat'),
                1.e-4,
                ))
        self.assert_(file_utils.fp_file_compare(
                'testz.dat',
                os.path.join('mesh_data', 'stress.dat'),
                1.e-4,
                ))
        file_utils.remove('test.dat')
        file_utils.remove('testz.dat')

    @memorycheck.check("microstructure")
    def RK2(self):
        # This test is slow, so it's only done up to t=1.0.
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=0.00001,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=RK2())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=1.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgdisp.dat'),
                1.e-4,
                nlines=20
                ))
        self.assert_(file_utils.fp_file_compare(
                'testz.dat',
                os.path.join('mesh_data', 'stress.dat'),
                1.e-4,
                nlines=23
                ))
        file_utils.remove('test.dat')
        file_utils.remove('testz.dat')

    @memorycheck.check("microstructure")
    def BackwardEuler(self):
        # This test is slow, so it's only done up to t=1.0, and uses
        # loose tolerances.
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=1e-4,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=BackwardEuler())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=1.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgdisp.dat'),
                1.e-3,
                nlines=20,
                ))
        self.assert_(file_utils.fp_file_compare(
                'testz.dat',
                os.path.join('mesh_data', 'stress.dat'),
                1.e-3,
                nlines=23
                ))
        file_utils.remove('test.dat')
        file_utils.remove('testz.dat')


    @memorycheck.check("microstructure")
    def ForwardEuler(self):
        # This test is slow, so it's only done up to t=1.0 with loose
        # tolerances.
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    tolerance=1e-4,
                    initialstep=0,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=ForwardEuler())),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1.e-13,
                    max_iterations=1000),
                asymmetric_solver=BiConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=1.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgdisp.dat'),
                1.e-3,
                nlines=20
                ))
        self.assert_(file_utils.fp_file_compare(
                'testz.dat',
                os.path.join('mesh_data', 'stress.dat'),
                1.e-3,
                nlines=23
                ))
        file_utils.remove('test.dat')
        file_utils.remove('testz.dat')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Check anisotropic elasticity for a simple plane stress and plane
## strain dynamic problem.  The reference files were generated by
## running the tests and aren't based on exact results, but they show
## the right symmetries.

class OOF_AnisoElasticDynamic(unittest.TestCase):
    def setUp(self):
        global outputdestination
        from ooflib.engine.IO import outputdestination
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=0.3,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=3)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material',
            microstructure='microstructure',
            pixels=every)
        OOF.Property.Copy(
            property='Mechanical:Elasticity:Anisotropic:Hexagonal',
            new_name='hex')
        OOF.Property.Parametrize.Mechanical.Elasticity.Anisotropic.Hexagonal.hex(
            cijkl=HexagonalRank4TensorCij(c11=4, c12=0.2, c13=0.1,
                                          c33=1.0, c44=0.5))
        OOF.Material.Add_property( 
            name='material',
            property='Mechanical:Elasticity:Anisotropic:Hexagonal:hex')
        OOF.Property.Copy(
            property='Mechanical:MassDensity:ConstantMassDensity',
            new_name='massdensity')
        OOF.Property.Parametrize.Mechanical.MassDensity.ConstantMassDensity.massdensity(
            rho=1.0)
        OOF.Material.Add_property( 
            name='material',
            property='Mechanical:MassDensity:ConstantMassDensity:massdensity')
        OOF.Property.Copy(
            property='Orientation', 
            new_name='hex')
        OOF.Material.Add_property(
            name='material',
            property='Orientation:hex')

        OOF.Skeleton.New( 
            name='skeleton',
            microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=2,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh', 
            skeleton='microstructure:skeleton', 
            element_types=['TET4_4', 'D2_2', 'T3_3', 'Q4_4'])
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
            name='bcx', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.0),boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bcy',
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Displacement,field_component='y',
                equation=Force_Balance,eqn_component='y',
                profile=ConstantProfile(value=0.0),boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bcz', 
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Displacement,field_component='z',
                equation=Force_Balance,eqn_component='z',
                profile=ConstantProfile(value=0.0),boundary='Xmin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='pull',
            mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(
                flux=Stress,
                profile=[
                    ConstantProfile(value=0.1), 
                    ConstantProfile(value=0.0),
                    ConstantProfile(value=0.0)],
                boundary='Xmax'))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh', 
            field=Displacement, 
            initializer=ConstThreeVectorFieldInit(cx=0.0,cy=0.0,cz=0.0))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Displacement_t, 
            initializer=ConstThreeVectorFieldInit(cx=0.0,cy=0.0,cz=0.0))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh',
            time=0.0)
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    tolerance=1e-04,
                    initialstep=0,
                    minstep=1e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=SS22(theta1=0.5,theta2=0.5))),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,max_iterations=1000),
                asymmetric_solver=None))

        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name=AutomaticName('front'),
            output=ScheduledAnalysis(
                data=getOutput('Field:Value', field=Displacement),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Zmax',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0, interval=0.05*shortening),
            destination=OutputStream(filename='testf.dat', mode='w'))
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name=AutomaticName('back'),
            output=ScheduledAnalysis(
                data=getOutput('Field:Value', field=Displacement),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Zmin',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0, interval=0.05*shortening),
            destination=OutputStream(filename='testb.dat', mode='w'))

    @memorycheck.check("microstructure")
    def Aniso1(self):
        OOF.Property.Parametrize.Orientation.hex(
            angles=Abg(alpha=90,beta=0,gamma=45))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=1.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'testf.dat',
                os.path.join('mesh_data',
                             'avgdisp_anisofront1.dat'),
                1.e-6))
        self.assert_(file_utils.fp_file_compare(
                'testb.dat',
                os.path.join('mesh_data',
                             'avgdisp_anisoback1.dat'),
                1.e-6))
        file_utils.remove('testf.dat')
        file_utils.remove('testb.dat')

    @memorycheck.check("microstructure")
    def Aniso2(self):
        OOF.Property.Parametrize.Orientation.hex(
            angles=Abg(alpha=45,beta=0,gamma=-45))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=1.0*shortening)
        self.assert_(file_utils.fp_file_compare(
                'testf.dat',
                os.path.join('mesh_data',
                             'avgdisp_anisofront2.dat'),
                1.e-6))
        self.assert_(file_utils.fp_file_compare(
                'testb.dat',
                os.path.join('mesh_data',
                             'avgdisp_anisoback2.dat'),
                1.e-6))
        file_utils.remove('testf.dat')
        file_utils.remove('testb.dat')

    def tearDown(self):
        OOF.Property.Delete(
            property='Mechanical:Elasticity:Anisotropic:Hexagonal:hex')
        OOF.Property.Delete(
            property='Orientation:hex')
        OOF.Property.Delete(
            property='Mechanical:MassDensity:ConstantMassDensity:massdensity')
        OOF.Material.Delete(name="material")
        outputdestination.forgetTextOutputStreams()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# OOF_StaticAndDynamic is just like OOF_ElasticTimeSteppers, but it
# also includes a separate quasistatic thermal diffusion subproblem,
# and only uses SS22.

## TODO MER: Technically, this test shouldn't be in this module.  It
## should be part of subproblem_test_extra.py.  But importing
## OOF_ElasticTimeSteppers into that file didn't work because when
## this module is imported into another module, the oofglobals aren't
## defined here.  That could be fixed.

class OOF_StaticAndDynamic(OOF_ElasticTimeSteppers):
    def setUp(self):
        OOF_ElasticTimeSteppers.setUp(self)
        OOF.Material.Add_property(
            name='material',
            property='Thermal:Conductivity:Isotropic')
        OOF.Subproblem.New(
            name='temp', 
            mesh='microstructure:skeleton:mesh',
            subproblem=EntireMeshSubProblem())
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:temp',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:temp',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:temp',
            equation=Heat_Eqn)
        OOF.Mesh.Scheduled_Output.New(
            mesh='microstructure:skeleton:mesh',
            name='tempo',
            output=ScheduledAnalysis(
                data=getOutput('Field:Value', field=Temperature),
                operation=AverageOutput(),
                domain=FaceBoundaryDomain(boundary='Xmax',side='FRONT'),
                sampling=ContinuumSampleSet(order=automatic)),
            scheduletype=AbsoluteOutputSchedule(),
            schedule=Periodic(delay=0.0, interval=0.1*shortening),
            destination=OutputStream(filename='testt.dat', mode='w'))
        # set boundary conditions: T=0 at y=0, T=t at y=1
        OOF.Mesh.Boundary_Conditions.New(
            name='bct',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfileXTd(
                    function='t',
                    timeDerivative='1',
                    timeDerivative2='0.0'),
                boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bct<2>', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='Ymin'))
        # set initial T=0 at t=0
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Temperature,
            initializer=ConstScalarFieldInit(value=0.0))
        OOF.Mesh.Set_Field_Initializer(
            mesh='microstructure:skeleton:mesh',
            field=Temperature_t,
            initializer=ConstScalarFieldInit(value=0.0))
        OOF.Mesh.Apply_Field_Initializers_at_Time(
            mesh='microstructure:skeleton:mesh',
            time=0.0)
        # set static solver for subproblem temp
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:temp',
            solver_mode=BasicSolverMode(
                time_stepper=BasicStaticDriver(),
                matrix_method=BasicIterative(
                    tolerance=1e-13,max_iterations=1000)))

    def timetest(self):
        # check that testt.dat contains T_avg =  t/2.
        datafile = file("testt.dat", "r")
        for line in datafile:
            if line[0] == '#':
                continue
            time, temp = map(eval, line.split(','))
            self.assertAlmostEqual(temp, 0.5*time, 6)

    @memorycheck.check("microstructure")
    def SS22(self):
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                time_stepper=AdaptiveDriver(
                    initialstep=0,
                    tolerance=0.00001,
                    minstep=1.0e-05,
                    errorscaling=AbsoluteErrorScaling(),
                    stepper=TwoStep(
                        singlestep=SS22(theta1=0.5,theta2=0.5))),
                nonlinear_solver=NoNonlinearSolver(),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),
                    tolerance=1e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=2.0*shortening)

        self.assert_(file_utils.fp_file_compare(
                'test.dat',
                os.path.join('mesh_data', 'avgdisp.dat'),
                1.e-4))
        self.assert_(file_utils.fp_file_compare(
                'testz.dat',
                os.path.join('mesh_data', 'stress.dat'),
                1.e-4))
        self.timetest()
        file_utils.remove('test.dat')
        file_utils.remove('testz.dat')
        file_utils.remove('testt.dat')

        self.saveAndLoad("static-dynamic")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#



static_set = [
    OOF_StaticIsoElastic("Null"),
    OOF_StaticIsoElastic("Solve0"),
    OOF_StaticIsoElastic("SolvePlusX"),
    OOF_StaticIsoElastic("SolveMinusX"),
    OOF_StaticIsoElastic("SolvePlusY"),
    OOF_StaticIsoElastic("SolveMinusY"),
    OOF_StaticIsoElastic("SolvePlusZ"),
    OOF_StaticIsoElastic("SolveMinusZ"),
    OOF_StaticIsoElastic("SolveFloatFlatX"),
    OOF_StaticIsoElastic("SolveFloatTiltX"),
    OOF_AnisoRotation("Solve00"),
    OOF_AnisoRotation("Solve0"),
    OOF_AnisoRotation("Solve"),
    OOF_SimplePiezo("Solve"),
    OOF_ElasticExact("Solve")
    ]

# Do a bunch of Neumann tests in a bunch of geometries.
neumanngeometries = (OOF_ElasticNeumann1,
                     OOF_ElasticNeumann2,
                     OOF_ElasticNeumann3,
                     OOF_ElasticNeumann4,
                     OOF_ThermalNeumann1,
                     OOF_ThermalNeumann2,
                     OOF_ThermalNeumann3,
                     OOF_ThermalNeumann4
                 )
neumanntestnames = ("NullXmin", "NullZmax", "Xmax01", "Ymax01", "Zmin01")
static_set.extend([geometry(testname)
                 for geometry in neumanngeometries
                 for testname in neumanntestnames])

static_set.extend([
    OOF_NonrectMixedBCStaticElastic("Solve1"),
    OOF_NonrectMixedBCStaticElastic("Solve2")]
)

dynamic_thermal_set = [
    OOF_ThermalDiffusionTimeSteppers("CNdirect"),
    OOF_ThermalDiffusionTimeSteppers("SS22directSaveRestore"),
    OOF_ThermalDiffusionTimeSteppers("BEdirect"),
    OOF_ThermalDiffusionTimeSteppers("RK4direct"),
    OOF_ThermalDiffusionTimeSteppers("RK2direct"),
    OOF_ThermalDiffusionTimeSteppers("SS22"),
    OOF_ThermalDiffusionTimeSteppers("CN"),
    OOF_ThermalDiffusionTimeSteppers("CNdouble"),
    OOF_ThermalDiffusionTimeSteppers("BE"),
    OOF_ThermalDiffusionTimeSteppers("RK4"),
    OOF_ThermalDiffusionTimeSteppers("RK2"),
]

dynamic_elastic_set = [
    # In "generate" mode, SS22 provides the reference data for the
    # rest of OOF_ElasticTimeSteppers, so it must precede the rest of
    # OOF_ElasticTimeSteppers in this list.
    OOF_ElasticTimeSteppers("SS22"),
    OOF_ElasticTimeSteppers("CNSaveRestore"),
    OOF_ElasticTimeSteppers("RK4"),
    OOF_ElasticTimeSteppers("RK2"),
    OOF_ElasticTimeSteppers("BackwardEuler"),
    OOF_ElasticTimeSteppers("ForwardEuler"),
    OOF_AnisoElasticDynamic("Aniso1"),
    OOF_AnisoElasticDynamic("Aniso2"),
    OOF_StaticAndDynamic("SS22")
]

test_set = static_set + dynamic_thermal_set + dynamic_elastic_set
#test_set = dynamic_elastic_set
# test_set = [
#     OOF_NonrectMixedBCStaticElastic("Solve2")
# ]
