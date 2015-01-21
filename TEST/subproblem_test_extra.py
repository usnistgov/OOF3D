# -*- python -*-
# $RCSfile: subproblem_test_extra.py,v $
# $Revision: 1.16 $
# $Author: langer $
# $Date: 2008/09/23 20:48:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

import unittest, os, string
import memorycheck

# Subproblem operations that rely on stuff tested in solver_test.py.

# Flag that says whether to generate missing reference data files.
# Should be false unless you really know what you're doing.
generate = False

# If generate==True, compare_mesh saves the given mesh in a data file
# for future comparison.  Otherwise it compares the mesh with the one
# already in the data file.  It returns 0 if the comparison succeeds
# (to be like a __cmp__ function).

def compare_mesh(meshpath, filename, tolerance):
    microname, relativemeshpath = string.split(meshpath, ':', 1)
    referencemeshpath = "reference:"+relativemeshpath
    datafile = os.path.join("mesh_data", filename)
    if generate and not os.path.exists(datafile):
        OOF.Microstructure.Rename(microstructure=microname, name="reference")
        OOF.File.Save.Mesh(filename=datafile, mode="w",
                           format="ascii", mesh=referencemeshpath)
        OOF.Microstructure.Rename(microstructure="reference", name=microname)
        return 0
    else:
        OOF.File.Load.Data(filename=datafile)
        mesh1 = mesh.meshes[meshpath]
        mesh2 = mesh.meshes[referencemeshpath]
        result = mesh1.compare(mesh2, tolerance)
        OOF.Microstructure.Delete(microstructure="reference")
        if result != 0:
            print >> sys.stderr, ("Mesh comparison failed.  Saving mesh as"
                                  " subproblem_test_extra_failed.mesh")
            OOF.File.Save.Mesh(filename='subproblem_test_extra_failed.mesh',
                               mode="w", format='ascii', mesh=meshpath)
        return result

def fname(subpname, planarity, index):
    return "subptest%d_%s%d.mesh" % (planarity, subpname, index)

class OOF_Subproblem_Extra(unittest.TestCase):
    def setUp(self):
        global mesh, femesh, cskeleton, cmicrostructure, subproblemcontext
        global subproblemcontext
        from ooflib.engine import subproblemcontext
        from ooflib.engine import mesh
        from ooflib.SWIG.common import cmicrostructure
        from ooflib.SWIG.engine import cskeleton, femesh
        OOF.Microstructure.New(name='microstructure', width=1.0, height=1.0,
                               width_in_pixels=10, height_in_pixels=10)
        OOF.Material.New(name='material')
        OOF.Material.Add_property(name='material',
                                  property='Thermal:Conductivity:Isotropic')
        OOF.Material.Assign(material='material',
                            microstructure='microstructure', pixels=all)
        OOF.Windows.Graphics.New()
        OOF.LayerEditor.LayerSet.New(window='Graphics_1')
        OOF.LayerEditor.LayerSet.DisplayedObject(category='Microstructure',
                                                 object='microstructure')
        OOF.LayerEditor.LayerSet.Add_Method(
            method=MicrostructureMaterialDisplay(
            no_material=Gray(value=0.0),
            no_color=RGBColor(red=0.0,green=0.0,blue=1.0)))
        OOF.LayerEditor.LayerSet.Send(window='Graphics_1')
        OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle(
            source='microstructure',
            points=[Point(0.22393,0.990078), Point(0.788911,-0.0200389)],
            shift=0, ctrl=0)
        OOF.PixelGroup.New(name='stripe', microstructure='microstructure')
        OOF.PixelGroup.AddSelection(microstructure='microstructure',
                                    group='stripe')
        OOF.Graphics_1.Toolbox.Pixel_Select.Invert(source='microstructure')
        OOF.PixelGroup.New(name='edges', microstructure='microstructure')
        OOF.PixelGroup.AddSelection(microstructure='microstructure',
                                    group='edges')
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(source='microstructure')
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=10, y_elements=10,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='microstructure:skeleton',
            points=[Point(0.403696,0.985798)], shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton='microstructure:skeleton', name='midtop',
            constructor=PointFromNodes(group=selection))
        OOF.Mesh.New(name='mesh', skeleton='microstructure:skeleton',
                     element_types=['T6_6', 'Q8_8'])
        OOF.Subproblem.New(name='stripe', mesh='microstructure:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='stripe'))
        OOF.Subproblem.New(name='edges', mesh='microstructure:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='edges'))
        OOF.Subproblem.Scrub_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Scrub_Solution(
            subproblem='microstructure:skeleton:mesh:stripe')
        OOF.Subproblem.Scrub_Solution(
            subproblem='microstructure:skeleton:mesh:edges')
        OOF.Graphics_1.File.Close()
    def tearDown(self):
        OOF.Material.Delete(name="material")

    # solveSubproblem runs tests for all of the types of boundary
    # conditions for the given subproblem and planarity.
    
    @memorycheck.check("microstructure")
    def solveSubproblem(self, subpname, planarity):
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            equation=Heat_Eqn)
        if planarity:
            OOF.Mesh.Field.In_Plane(mesh='microstructure:skeleton:mesh',
                                    field=Temperature)
        else:
            OOF.Subproblem.Equation.Activate(
                subproblem='microstructure:skeleton:mesh:'+subpname,
                equation=Plane_Heat_Flux)

        # First, fix T=0 on the bottom and T=1 on the top, and solve.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='top'))
        OOF.Subproblem.Schedule_Solution(
            subproblem='microstructure:skeleton:mesh:'+subpname)
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            linearity=Linear(),
            solver=StaticDriver(matrixmethod=GeneralizedMinResidual(
            preconditioner=ILUPreconditioner(),tolerance=1e-13,
            max_iterations=1000,krylov_dimension=100)))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        
        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      fname(subpname, planarity, 0),
                                      1.e-10), 0)

        # Change top bc to Float and re-solve.
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(field=Temperature,field_component='',
                              equation=Heat_Eqn,eqn_component='',
                              profile=ContinuumProfile(function='0'),
                              boundary='top'))

        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        
        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      fname(subpname, planarity, 1),
                                      1.e-10), 0)

        # Fix T at a point outside the stripe subproblem and re-solve.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=2),
                                  boundary='topleft'))

        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      fname(subpname, planarity, 2),
                                      1.e-10), 0)

        # Replace top Floating and Fixed bcs with one Neumann
        # condition and re-solve.
        OOF.Mesh.Boundary_Conditions.Delete(
            mesh='microstructure:skeleton:mesh', name='bc<3>')
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(flux=Heat_Flux,
                                profile=ConstantProfile(value=1.23),
                                boundary='top',normal=False))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)

        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      fname(subpname, planarity, 3),
                                      1.e-10), 0)

        # Replace Neumann BC with a ForceBC and re-solve.
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=ForceBC(equation=Heat_Eqn,eqn_component='',
                              profile=ContinuumProfile(function='1'),
                              boundary='midtop'))
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      fname(subpname, planarity, 4),
                                      1.e-10), 0)
        OOF.Subproblem.Scrub_Solution(
            subproblem='microstructure:skeleton:mesh:'+subpname)


    def SolveStripe(self):
        self.solveSubproblem('stripe', 0)

    def SolveEdges(self):
        self.solveSubproblem('edges', 0)

    def SolveStripePlaneFlux(self):
        self.solveSubproblem('stripe', 1)

    def SolveEdgesPlaneFlux(self):
        self.solveSubproblem('edges', 1)

    @memorycheck.check("microstructure")
    def DeleteAndSolve(self):
        # This test checks for the absence of a one-time bug that
        # created non-square stiffness matrices if a subproblem was
        # solved after a neighboring subproblem was deleted.  If it
        # completes without raising an exception, it passes.
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:edges',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:edges',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:edges',
            equation=Heat_Eqn)
        OOF.Mesh.Field.In_Plane(
            mesh='microstructure:skeleton:mesh',
            field=Temperature)
        OOF.Subproblem.Copy_Field_State(
            source='microstructure:skeleton:mesh:edges',
            target='microstructure:skeleton:mesh:stripe')
        OOF.Subproblem.Delete(subproblem='microstructure:skeleton:mesh:stripe')
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='top'))

        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:edges',
            linearity=Linear(),
            solver=StaticDriver(matrixmethod=GeneralizedMinResidual(
                    krylov_dimension=100,
                    preconditioner=ILUPreconditioner(), tolerance=1.e-13,
                    max_iterations=1000)))
        OOF.Subproblem.Scrub_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Schedule_Solution(
            subproblem='microstructure:skeleton:mesh:edges')
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      'subp_delete_solve.mesh', 1.e-10), 0)

    @memorycheck.check("microstructure")
    def CopyAndSolve(self):
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:edges',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:edges',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:edges',
            equation=Heat_Eqn)
        OOF.Mesh.Field.In_Plane(
            mesh='microstructure:skeleton:mesh',
            field=Temperature)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='top'))
        # Copy the subproblem *after* creating boundary conditions, to
        # make the bookkeeping as complicated as possible.
        OOF.Subproblem.Copy(
            subproblem='microstructure:skeleton:mesh:edges',
            mesh='microstructure:skeleton:mesh',
            name='copy')
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:copy',
            linearity=Linear(),
            solver=StaticDriver(matrixmethod=GeneralizedMinResidual(
                    krylov_dimension=100,
                    preconditioner=ILUPreconditioner(), tolerance=1.e-13,
                    max_iterations=1000)))
        OOF.Subproblem.Scrub_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Schedule_Solution(
            subproblem='microstructure:skeleton:mesh:copy')
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      'subp_copy_solve.mesh', 1.e-10), 0)
        
    @memorycheck.check("microstructure")
    def RenameAndSolve(self):
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:edges',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:edges',
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:edges',
            equation=Heat_Eqn)
        OOF.Mesh.Field.In_Plane(
            mesh='microstructure:skeleton:mesh',
            field=Temperature)
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='bottom'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='top'))
        # Rename the subproblem *after* creating boundary conditions,
        # to make the bookkeeping as complicated as possible.
        OOF.Subproblem.Rename(
            subproblem='microstructure:skeleton:mesh:edges',
            name='Ishmael')
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:Ishmael',
            linearity=Linear(),
            solver=StaticDriver(matrixmethod=GeneralizedMinResidual(
                    krylov_dimension=100,
                    preconditioner=ILUPreconditioner(), tolerance=1.e-13,
                    max_iterations=1000)))
        OOF.Subproblem.Scrub_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Schedule_Solution(
            subproblem='microstructure:skeleton:mesh:Ishmael')
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0, stepsize=0)
        self.assertEqual(compare_mesh("microstructure:skeleton:mesh",
                                      'subp_rename_solve.mesh', 1.e-10), 0)
    
def run_tests():

    test_set = [
        OOF_Subproblem_Extra("DeleteAndSolve"),
        OOF_Subproblem_Extra("CopyAndSolve"),
        OOF_Subproblem_Extra("RenameAndSolve")
        ]
    
    logan = unittest.TextTestRunner()
    for t in test_set:
        print >> sys.stderr,  "\n *** Running test: %s\n" % t.id()
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
