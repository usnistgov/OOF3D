# -*- python -*-
# $RCSfile: boundary_condition_test.py,v $
# $Revision: 1.1.2.3 $
# $Author: langer $
# $Date: 2014/05/09 20:51:36 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# Tests for the machinery that handles boundary condition
# intersections, floatBC promotion, and enabling and disabling of
# boundary conditions.

import unittest, os
import memorycheck
from UTILS import file_utils
file_utils.generate = False

class OOF_BCTest(unittest.TestCase):
    def setUp(self):
        global ooferror
        from ooflib.SWIG.common import ooferror
        OOF.File.Load.Data(
            filename=file_utils.reference_file("bc_data", "test_mesh.dat"))

    def solveAndCheck(self, filename):
        OOF.Mesh.Solve(
            mesh='microstructure:skeleton:mesh',
            endtime=0.0)
        OOF.File.Save.Mesh(
            filename='solved',
            mode='w', 
            format='ascii',
            mesh='microstructure:skeleton:mesh')
        self.assert_(file_utils.fp_file_compare(
            'solved', 
            os.path.join('bc_data', filename), 1.e-10))
        file_utils.remove("solved")
        

    @memorycheck.check("microstructure")
    def SimpleSolve(self):
        # Null case, for reference.  No boundary conditions.
        self.solveAndCheck("nulltest")

    @memorycheck.check("microstructure")
    def OneDirichlet(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature, field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='Ymin'))
        self.solveAndCheck("oneside")

    @memorycheck.check("microstructure")
    def TwoDirichlet(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature, field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature, field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=2),
                boundary='Ymax'))
        self.solveAndCheck("twosides")

    # Two conflicting Dirichlet boundary conditions on different
    # boundaries.  Conflicting Dirichlet conditions only raise a
    # Warning, which we can't detect here, unless this test is run in
    # NoWarnings mode.
    @memorycheck.check("microstructure")
    def DirichletClash1(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature, field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature, field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=2),
                boundary='Xmax'))
        OOF.Help.No_Warnings(True)
        self.assertRaises(ooferror.ErrWarning,
                          OOF.Mesh.Solve,
                          mesh='microstructure:skeleton:mesh',
                          endtime=0.0)
        OOF.Help.No_Warnings(False)
    
    # Two conflicting Dirichlet boundary conditions on the same
    # boundary.  This raises an error even if not in NoWarnings mode.
    @memorycheck.check("microstructure")
    def DirichletClash2(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature, field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1),
                boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature, field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=2),
                boundary='Ymin'))
        self.assertRaises(ooferror.ErrUserError,
                          OOF.Mesh.Solve,
                          mesh='microstructure:skeleton:mesh',
                          endtime=0.0)
        # Now fix the conflict and make sure the mesh is solvable.
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=2),
                boundary='Ymax'))
        self.solveAndCheck("twosides")

    # Two conflicting Dirichlet boundary conditions on different
    # boundaries.  This version of the test uses non-constant boundary
    # conditions.
    @memorycheck.check("microstructure")
    def DirichletClash3(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfileXTd(function='z',
                                            timeDerivative='0.0',
                                            timeDerivative2='0.0'),
                boundary='Ymin'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfileXTd(function='y',
                                            timeDerivative='0.0',
                                            timeDerivative2='0.0'),
                boundary='Xmin'))
        OOF.Help.No_Warnings(True)
        self.assertRaises(ooferror.ErrWarning,
                          OOF.Mesh.Solve,
                          mesh='microstructure:skeleton:mesh',
                          endtime=0.0)
        OOF.Help.No_Warnings(False)
        # Fix the error
        OOF.Mesh.Boundary_Conditions.Edit(
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfileXTd(function='z',
                                            timeDerivative='0.0',
                                            timeDerivative2='0.0'),
                boundary='Xmin'))
        self.solveAndCheck("resolved")

    # float intersecting float on faces
    @memorycheck.check("microstructure")
    def TwoFloats(self):
        # Fix T=0 at the origin
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        # Apply a constant FloatBC at Xmax
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='Xmax'))
        # Apply a spatially varying FloatBC at Ymax
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh', 
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='x'),
                boundary='Ymax'))
        self.solveAndCheck("twofloats")

    # face float intersecting edge float, along an edge of the same
    # face
    @memorycheck.check("microstructure")
    def TwoMoreFloats(self):
        # Fix T=0 at the origin
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        OOF.Mesh.Boundary_Conditions.New( 
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='y*z'),
                boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='XmaxYmin'))
        self.solveAndCheck("twofloats2")

    # Two floating conditions on intersecting edges
    @memorycheck.check("microstructure")
    def YetTwoMoreFloats(self):
        # Fix T=0 at the origin
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        OOF.Mesh.Boundary_Conditions.New( 
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='y+3'),
                boundary='XminZmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='x-2'),
                boundary='YminZmax'))
        self.solveAndCheck("twofloats3")

    # An edge float intersecting a face float at a single point
    @memorycheck.check("microstructure")
    def YetTwoMoreFloatsAgain(self):
        # Fix T=0 at the origin
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        OOF.Mesh.Boundary_Conditions.New( 
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='x+y'),
                boundary='Zmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=12), # dummy value
                boundary='XmaxYmin'))
        self.solveAndCheck("twofloats4")

    # loop of floats
    @memorycheck.check("microstructure")
    def FloatLoop(self):
        # Fix T=0 at the origin
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        # Apply FloatBCs to the edges of the Zmax face.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='YmaxZmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='0.5*y'),
                boundary='XmaxZmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='YminZmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='0.5*y'),
                boundary='XminZmax'))
        self.solveAndCheck("floatloop")

    @memorycheck.check("microstructure")
    def FloatLoopClash(self):
        # Fix T=0 at the origin
        OOF.Mesh.Boundary_Conditions.New(
            name='bc', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='XminYminZmin'))
        # Apply FloatBCs to the edges of the Zmax face.  The boundary
        # conditions are the same as in FloatLoop, except that the
        # profile of the XminZmax condition is reversed.
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='YmaxZmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='0.5*y'),
                boundary='XmaxZmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<4>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=0.0),
                boundary='YminZmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<5>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='-0.5*y'),
                boundary='XminZmax'))
        # Check that solving the system raises an exception.
        OOF.Help.No_Warnings(True)
        self.assertRaises(ooferror.ErrSetupError,
                          OOF.Mesh.Solve,
                          mesh='microstructure:skeleton:mesh',
                          endtime=0.0)
        OOF.Help.No_Warnings(False)
        # Disable one of the boundary conditions, breaking the loop,
        # and solve.
        OOF.Mesh.Boundary_Conditions.Disable(
            mesh='microstructure:skeleton:mesh',
            name='bc<2>')
        self.solveAndCheck('brokenfloatloop')
        # Re-enable the boundary condition and make sure that the
        # error reappears.
        OOF.Mesh.Boundary_Conditions.Enable(
            mesh='microstructure:skeleton:mesh',
            name='bc<2>')
        OOF.Help.No_Warnings(True)
        self.assertRaises(ooferror.ErrSetupError,
                          OOF.Mesh.Solve,
                          mesh='microstructure:skeleton:mesh',
                          endtime=0.0)
        OOF.Help.No_Warnings(False)

    # A face float and an incompatible edge float on one of the face's
    # edges.
    @memorycheck.check("microstructure")
    def InconsistentFloats(self):
        OOF.Mesh.Boundary_Conditions.New( 
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='x*y'),
                boundary='Zmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='x'),
                boundary='YminZmax'))
        OOF.Help.No_Warnings(True)
        self.assertRaises(ooferror.ErrWarning,
                          OOF.Mesh.Solve,
                          mesh='microstructure:skeleton:mesh',
                          endtime=0.0)
        OOF.Help.No_Warnings(False)

    # Two floats on the same boundary
    @memorycheck.check("microstructure")
    def MoreInconsistentFloats(self):
        OOF.Mesh.Boundary_Conditions.New( 
            name='bc<2>',
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='x*y'),
                boundary='Zmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function='x'),
                boundary='Zmax'))
        self.assertRaises(ooferror.ErrUserError,
                          OOF.Mesh.Solve,
                          mesh='microstructure:skeleton:mesh',
                          endtime=0.0)

    # float intersecting fixed
    @memorycheck.check("microstructure")
    def FloatAndFixed1(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function="y"),
                boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1.0),
                boundary='Ymax'))
        self.solveAndCheck("floatfixed")

    # float intersecting fixed, with a trivial offset added to the float.
    @memorycheck.check("microstructure")
    def FloatAndFixed2(self):
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<2>', 
            mesh='microstructure:skeleton:mesh',
            condition=FloatBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ContinuumProfile(function="y+1.234"),
                boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.New(
            name='bc<3>', 
            mesh='microstructure:skeleton:mesh', 
            condition=DirichletBC(
                field=Temperature,field_component='',
                equation=Heat_Eqn,eqn_component='',
                profile=ConstantProfile(value=1.0),
                boundary='Ymax'))
        self.solveAndCheck("floatfixed2")

 
    def tearDown(self):
        OOF.Property.Delete(property='Thermal:Conductivity:Isotropic:instance')
        OOF.Material.Delete(name='material')


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    OOF_BCTest("SimpleSolve"),
    OOF_BCTest("OneDirichlet"),
    OOF_BCTest("TwoDirichlet"),
    OOF_BCTest("DirichletClash1"),
    OOF_BCTest("DirichletClash2"),
    OOF_BCTest("DirichletClash3"),
    OOF_BCTest("TwoFloats"),
    OOF_BCTest("TwoMoreFloats"),
    OOF_BCTest("YetTwoMoreFloats"),
    OOF_BCTest("YetTwoMoreFloatsAgain"),
    OOF_BCTest("FloatLoop"),
    OOF_BCTest("FloatLoopClash"),
    OOF_BCTest("InconsistentFloats"),
    OOF_BCTest("MoreInconsistentFloats"),
    OOF_BCTest("FloatAndFixed1"),
    OOF_BCTest("FloatAndFixed2")
]

