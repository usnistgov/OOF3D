# -*- python -*-
# $RCSfile: subproblem_test_extra.py,v $
# $Revision: 1.1.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:34:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test subproblem operations that rely on stuff tested in solver_test.py.

import unittest, os
import memorycheck
from UTILS import file_utils 
file_utils.generate = False

def fname(subpname, index):
    return "subptest_%s%d.mesh" % (subpname, index)

class OOF_Subproblem_Extra(unittest.TestCase):
    def setUp(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material')
        OOF.Material.Add_property(
            name='material',
            property='Thermal:Conductivity:Isotropic')
        OOF.Material.Assign(
            material='material',
            microstructure='microstructure',
            pixels=every)

        OOF.PixelSelection.Region(
            microstructure='microstructure', 
            shape=BoxSelectionShape(
                point0=Point(0.3,0,0), point1=Point(0.7,1,1)),
            units=PhysicalUnits(),
            operator=Select())
        OOF.PixelGroup.New(
            name='stripe', 
            microstructure='microstructure')
        OOF.PixelGroup.AddSelection(
            microstructure='microstructure',
            group='stripe')

        OOF.PixelSelection.Invert(
            microstructure='microstructure')
        OOF.PixelGroup.New(
            name='edges',
            microstructure='microstructure')
        OOF.PixelGroup.AddSelection(
            microstructure='microstructure',
            group='edges')

        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=5, y_elements=5, z_elements=5,
            skeleton_geometry=TetraSkeleton(
                arrangement='moderate'))
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='microstructure:skeleton', 
            points=[Point(0.446106,0.768333,2.12376)], 
            view=View(cameraPosition=Coord(0.5,0.5,3.42583),
                      focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0,
                      size_x=621, size_y=615),
            shift=0, ctrl=0)
        OOF.Graphics_1.File.Close()
        OOF.Skeleton.Boundary.Construct(
            skeleton='microstructure:skeleton',
            name='midtop',
            constructor=PointFromNodes(group=selection))
        OOF.Mesh.New(
            name='mesh', 
            skeleton='microstructure:skeleton', 
            element_types=['TET4_4', 'Q4_4', 'T3_3', 'D2_2'])
        OOF.Subproblem.New(
            name='edges',
            mesh='microstructure:skeleton:mesh', 
            subproblem=PixelGroupSubProblem(group='edges'))
        OOF.Subproblem.New(
            name='stripe',
            mesh='microstructure:skeleton:mesh', 
            subproblem=PixelGroupSubProblem(group='stripe'))
        OOF.Subproblem.Disable_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Disable_Solution(
            subproblem='microstructure:skeleton:mesh:stripe')
        OOF.Subproblem.Disable_Solution(
            subproblem='microstructure:skeleton:mesh:edges')
    def tearDown(self):
        OOF.Material.Delete(name="material")

    def compare(self, filename):
        OOF.File.Save.Mesh(
            filename=filename,
            mode='w', format='ascii',
            mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            filename,
            os.path.join('mesh_data', filename),
            1.e-6))
        file_utils.remove(filename)


    # solveSubproblem runs tests for all of the types of boundary
    # conditions for the given subproblem and planarity.
    
    @memorycheck.check("microstructure")
    def solveSubproblem(self, subpname):
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            field=Temperature)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            equation=Heat_Eqn)

        # First, fix T=0 on the bottom and T=1 on the top, and solve.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='Ymax'))
        OOF.Subproblem.Enable_Solution(
            subproblem='microstructure:skeleton:mesh:'+subpname)
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:'+subpname,
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=StaticDriver(),
                asymmetric_solver=GeneralizedMinResidual(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000,krylov_dimension=100),
                symmetric_solver=ConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1.e-13,
                    max_iterations=1000)
                )
            )
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        self.compare(fname(subpname, 0))

        # Change top bc to Float and re-solve.
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(field=Temperature,field_component='',
                              equation=Heat_Eqn,eqn_component='',
                              profile=ContinuumProfile(function='0'),
                              boundary='Ymax'))

        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        self.compare(fname(subpname, 1))

        # Fix T at a point outside the stripe subproblem and re-solve.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=2),
                                  boundary='XminYmaxZmax'))

        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        self.compare(fname(subpname, 2))

        # Replace top Floating and Fixed bcs with one Neumann
        # condition and re-solve.
        OOF.Mesh.Boundary_Conditions.Delete(
            mesh='microstructure:skeleton:mesh',
            name='bc<3>')
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=NeumannBC(flux=Heat_Flux,
                                profile=ConstantProfile(value=1.23),
                                boundary='Ymax'))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
                       endtime=0.0)
        self.compare(fname(subpname, 3))

        # Replace Neumann BC with a ForceBC and re-solve.
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>', mesh='microstructure:skeleton:mesh',
            condition=ForceBC(equation=Heat_Eqn,eqn_component='',
                              profile=ContinuumProfileXT(function='1'),
                              boundary='midtop'))
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        self.compare(fname(subpname, 4))

        OOF.Subproblem.Disable_Solution(
            subproblem='microstructure:skeleton:mesh:'+subpname)


    def SolveStripe(self):
        self.solveSubproblem('stripe')

    def SolveEdges(self):
        self.solveSubproblem('edges')

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
                                  boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='Ymax'))

        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:edges',
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=StaticDriver(),
                asymmetric_solver=GeneralizedMinResidual(
                    krylov_dimension=100,
                    preconditioner=ILUPreconditioner(), tolerance=1.e-13,
                    max_iterations=1000)))
        OOF.Subproblem.Disable_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Enable_Solution(
            subproblem='microstructure:skeleton:mesh:edges')
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0)
        self.compare('subp_delete_solve.mesh')

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
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='Ymax'))
        # Copy the subproblem *after* creating boundary conditions, to
        # make the bookkeeping as complicated as possible.
        OOF.Subproblem.Copy(
            subproblem='microstructure:skeleton:mesh:edges',
            mesh='microstructure:skeleton:mesh',
            name='copy')
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:copy',
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=StaticDriver(),
            asymmetric_solver=GeneralizedMinResidual(
                    krylov_dimension=100,
                    preconditioner=ILUPreconditioner(), tolerance=1.e-13,
                    max_iterations=1000)))
        OOF.Subproblem.Disable_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Enable_Solution(
            subproblem='microstructure:skeleton:mesh:copy')
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0)
        self.compare('subp_copy_solve.mesh')
        
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
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=0.0),
                                  boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(field=Temperature,field_component='',
                                  equation=Heat_Eqn,eqn_component='',
                                  profile=ConstantProfile(value=1),
                                  boundary='Ymax'))
        # Rename the subproblem *after* creating boundary conditions,
        # to make the bookkeeping as complicated as possible.
        OOF.Subproblem.Rename(
            subproblem='microstructure:skeleton:mesh:edges',
            name='Ishmael')
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:Ishmael',
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=StaticDriver(),
                asymmetric_solver=GeneralizedMinResidual(
                    krylov_dimension=100,
                    preconditioner=ILUPreconditioner(), tolerance=1.e-13,
                    max_iterations=1000)))
        OOF.Subproblem.Disable_Solution(
            subproblem='microstructure:skeleton:mesh:default')
        OOF.Subproblem.Enable_Solution(
            subproblem='microstructure:skeleton:mesh:Ishmael')
        OOF.Mesh.Solve(mesh='microstructure:skeleton:mesh',
                       endtime=0.0)
        self.compare('subp_rename_solve.mesh')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    OOF_Subproblem_Extra("SolveStripe"),
    OOF_Subproblem_Extra("SolveEdges"),
    OOF_Subproblem_Extra("DeleteAndSolve"),
    OOF_Subproblem_Extra("CopyAndSolve"),
    OOF_Subproblem_Extra("RenameAndSolve"),
]

