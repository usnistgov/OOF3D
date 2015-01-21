# -*- python -*-
# $RCSfile: mesh_test.py,v $
# $Revision: 1.1.2.16 $
# $Author: langer $
# $Date: 2014/11/07 20:28:05 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test suite for the menu commands under OOF.Mesh.*

import unittest, os
from UTILS import file_utils
import memorycheck

file_utils.generate = True

reference_file = file_utils.reference_file

# Basic mesh operations -- creation, destruction, copying.
# Modify might be complicated.

class OOF_Mesh_Base(unittest.TestCase):
    def setUp(self):
        global mesh, subproblemcontext, femesh, cmicrostructure, skeletoncontext
        from ooflib.engine import mesh
        from ooflib.engine import skeletoncontext
        from ooflib.engine import subproblemcontext
        from ooflib.SWIG.engine import femesh
        from ooflib.SWIG.common import cmicrostructure
        # Some tests here use skeleton refinement, which uses random
        # numbers to shuffle element lists.  To make the tests
        # repeatable, the random number generator must be reseeded.
        OOF.Settings.Random_Seed(seed=17)

class OOF_Mesh(OOF_Mesh_Base):
    def setUp(self):
        OOF_Mesh_Base.setUp(self)

        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file('ms_data','bluegreen'),
                sort=NumericalOrder()),
            microstructure_name='meshtest',
            height=automatic, width=automatic, depth=automatic)
        OOF.Image.AutoGroup(
            image='meshtest:bluegreen',
            name_template='%c')
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='meshtest',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Windows.Graphics.New()

    def tearDown(self):
        OOF.Graphics_1.File.Close()

    @memorycheck.check("meshtest")
    def New(self):
        OOF.Mesh.New(
            name="test",
            skeleton="meshtest:skeleton",
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        msh = mesh.meshes["meshtest:skeleton:test"]
        self.assertNotEqual(msh, None)
        self.assertEqual(mesh.meshes.nActual(), 1)

    @memorycheck.check("meshtest")
    def Delete(self):
        OOF.Mesh.New(name="test", skeleton="meshtest:skeleton",
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        OOF.Mesh.Delete(mesh="meshtest:skeleton:test")
        self.assertEqual(mesh.meshes.nActual(), 0)
        self.assertEqual(subproblemcontext.subproblems.nActual(), 0)

    @memorycheck.check("meshtest")
    def Copy(self):
        OOF.Mesh.New(name="test", skeleton="meshtest:skeleton",
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        OOF.Mesh.Copy(mesh="meshtest:skeleton:test",
                      name="copy",
                      copy_field=True, copy_equation=True,
                      copy_bc=True)
        msh = mesh.meshes["meshtest:skeleton:test"]
        msh2 = mesh.meshes["meshtest:skeleton:copy"]
        self.assertEqual(mesh.meshes.nActual(), 2)
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        self.assertNotEqual(id(msh),id(msh2))
        self.assertNotEqual(id(msh.getObject()), id(msh2.getObject()) )
        # Rich copying needs to wait until after fields etc. work.

    @memorycheck.check("meshtest")
    def Rename(self):
        OOF.Mesh.New(name="test", skeleton="meshtest:skeleton",
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        msh = mesh.meshes["meshtest:skeleton:test"]
        OOF.Mesh.Rename(mesh="meshtest:skeleton:test",name="bob")
        msh2 = mesh.meshes["meshtest:skeleton:bob"]
        self.assertEqual(mesh.meshes.nActual(), 1)
        self.assertEqual(id(msh),id(msh2))
        self.assertEqual(id(msh.getObject()), id(msh2.getObject()) )
    
    @memorycheck.check("meshtest")
    def Skeleton_Delete(self):
        from ooflib.SWIG.engine import cskeletonelement
        from ooflib.SWIG.engine import cskeletonnode2

        OOF.Mesh.New(
            name="test",
            skeleton="meshtest:skeleton",
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        #
        OOF.Skeleton.Delete(skeleton="meshtest:skeleton")
        self.assertEqual(mesh.meshes.nActual(), 0)
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        self.assertEqual(femesh.get_globalFEMeshCount(), 0)
        self.assertEqual(cskeletonnode2.get_globalNodeCount(), 0)
        self.assertEqual(cskeletonelement.get_globalElementCount(), 0)

    @memorycheck.check("meshtest")
    def Mesh_Rebuild(self):
        OOF.Mesh.New(
            name="test",
            skeleton="meshtest:skeleton",
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        msh = mesh.meshes["meshtest:skeleton:test"]
        self.assertEqual(msh.nelements(), 320)
        # Select and refine a skeleton element.
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='meshtest:skeleton',
            points=[Point(4.53162,5.35128,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=690, size_y=618),
            shift=0, ctrl=0)
        OOF.Skeleton.Modify(
            skeleton='meshtest:skeleton',
            modifier=Refine(targets=CheckSelectedElements(),
                            criterion=Unconditionally(),alpha=0.3))
        # The mesh should not yet have changed.
        self.assertEqual(msh.nelements(), 320)
        self.assert_(msh.outOfSync())
        # Rebuild the mesh.
        OOF.Mesh.Modify(
            mesh='meshtest:skeleton:test',
            modifier=RebuildMesh())
        self.assertEqual(msh.nelements(), 344)
        self.assert_(not msh.outOfSync())
        # Undo the Skeleton modification
        OOF.Skeleton.Undo(
            skeleton='meshtest:skeleton')
        self.assertEqual(msh.nelements(), 344)
        self.assert_(msh.outOfSync())
        OOF.Mesh.Modify(
            mesh='meshtest:skeleton:test',
            modifier=RebuildMesh())
        self.assertEqual(msh.nelements(), 320)
        self.assert_(not msh.outOfSync())

# For the Field/Equation tests, we assume the prior existence of a
# temperature and displacement field.  These tests use the deprecated
# OOF.Mesh.Field and OOF.Mesh.Equation menus, which are retained for
# backwards compatibility with old scripts.  The preferred menu items
# are in the OOF.Subproblem menu, which is tested in
# subproblem_test.py.

# The memcheck decorator just runs the memorycheck.check decorator,
# but cleans up some local references first.
def memcheck(func):
    @memorycheck.check("meshtest")
    def cleanup(self, *args, **kwargs):
        val = func(self, *args, **kwargs)
        del self.msh
        del self.msh_obj
        del self.subp
        return val
    return cleanup

class OOF_Mesh_FieldEquation(OOF_Mesh):
    def setUp(self):
        global field
        from ooflib.SWIG.engine import field
        OOF_Mesh.setUp(self)
        OOF.Mesh.New(name="fe_test", skeleton="meshtest:skeleton",
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        self.msh = mesh.meshes["meshtest:skeleton:fe_test"]
        self.msh_obj = self.msh.getObject()
        self.subp = self.msh.get_default_subproblem().getObject()

    @memcheck
    def DefineField(self):
        self.assert_(not Temperature.is_defined(self.subp))
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        self.assert_(Temperature.is_defined(self.subp))
        self.assert_(not Displacement.is_defined(self.subp))
        
    @memcheck
    def UndefineField(self):
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Undefine(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        self.assert_(not Temperature.is_defined(self.subp))
        self.assert_(not Displacement.is_defined(self.subp))
        
        
    @memcheck
    def ActivateField(self):
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        self.assert_(not Temperature.is_active(self.subp))
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        self.assert_(Temperature.is_active(self.subp))
        self.assert_(not Displacement.is_defined(self.subp))
        self.assert_(not Displacement.is_active(self.subp))
        

    @memcheck
    def DeactivateField(self):
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        OOF.Mesh.Field.Deactivate(mesh="meshtest:skeleton:fe_test",
                                  field=Temperature)
        self.assert_(not Temperature.is_active(self.subp))
        self.assert_(not Displacement.is_defined(self.subp))
        self.assert_(not Displacement.is_active(self.subp))


    # @memcheck
    # def In_PlaneField(self):
    #     OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
    #                           field=Temperature)
    #     OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
    #                             field=Temperature)
    #     self.assert_(not self.msh_obj.in_plane(Temperature))
    #     OOF.Mesh.Field.In_Plane(mesh="meshtest:skeleton:fe_test",
    #                             field=Temperature)
    #     self.assert_(self.msh_obj.in_plane(Temperature))

    # @memcheck
    # def Out_of_PlaneField(self):
    #     OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
    #                           field=Temperature)
    #     OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
    #                             field=Temperature)
    #     OOF.Mesh.Field.In_Plane(mesh="meshtest:skeleton:fe_test",
    #                             field=Temperature)
    #     OOF.Mesh.Field.Out_of_Plane(mesh="meshtest:skeleton:fe_test",
    #                                 field=Temperature)
    #     self.assert_(not self.msh_obj.in_plane(Temperature))


    @memcheck
    def ActivateEquation(self):
        self.assert_(not self.subp.is_active_equation(Heat_Eqn))
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Heat_Eqn)
        self.assert_(self.subp.is_active_equation(Heat_Eqn))
        self.assert_(not self.subp.is_active_equation(Force_Balance))

    @memcheck
    def DeactivateEquation(self):
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Heat_Eqn)
        OOF.Mesh.Equation.Deactivate(mesh="meshtest:skeleton:fe_test",
                                     equation=Heat_Eqn)
        self.assert_(not self.subp.is_active_equation(Heat_Eqn))

# Mesh ops that have no real meaning unless fields and equations exist
# on them.  Same setup/teardown as OOF_Mesh_FieldEquation.
class OOF_Mesh_Extra(OOF_Mesh_FieldEquation):
    @memcheck
    def Copy(self):
        # Mesh copying with fields defined wasn't tested in the
        # previous "Copy" tests.
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Heat_Eqn)
        OOF.Mesh.Copy(mesh="meshtest:skeleton:fe_test",
                      name="copy",
                      copy_field=True, copy_equation=True, copy_bc=True)
        msh = mesh.meshes["meshtest:skeleton:fe_test"]
        msh2 = mesh.meshes["meshtest:skeleton:copy"]
        subp2 = subproblemcontext.subproblems[
            'meshtest:skeleton:copy:default'].getObject()
        self.assert_(Temperature.is_defined(subp2))
        self.assert_(not Displacement.is_defined(subp2))
        self.assert_(Temperature.is_active(subp2))
        self.assert_(subp2.is_active_equation(Heat_Eqn))
        self.assert_(not subp2.is_active_equation(Force_Balance))
    @memcheck
    def Copy_Field_State(self):
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Displacement)
        OOF.Mesh.New(name="fe_copy_test",
                     skeleton="meshtest:skeleton",
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        subp = subproblemcontext.subproblems[
            'meshtest:skeleton:fe_copy_test:default'].getObject()
        self.assert_(not Temperature.is_defined(subp))
        self.assert_(not Temperature.is_active(subp))
        self.assert_(not Displacement.is_defined(subp))
        OOF.Mesh.Copy_Field_State(source="meshtest:skeleton:fe_test",
                                  target="meshtest:skeleton:fe_copy_test")
        self.assert_(Temperature.is_defined(subp))
        self.assert_(Temperature.is_active(subp))
        self.assert_(Displacement.is_defined(subp))
        OOF.Mesh.Delete(mesh="meshtest:skeleton:fe_copy_test")
        

    @memcheck
    def Copy_Equation_State(self):
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Heat_Eqn)
        OOF.Mesh.New(name="fe_copy_test",
                     skeleton="meshtest:skeleton",
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        subp = subproblemcontext.subproblems[
            'meshtest:skeleton:fe_copy_test:default'].getObject()
        self.assert_(not subp.is_active_equation(Heat_Eqn))
        OOF.Mesh.Copy_Equation_State(source="meshtest:skeleton:fe_test",
                                     target="meshtest:skeleton:fe_copy_test")
        self.assert_(subp.is_active_equation(Heat_Eqn))
        self.assert_(not subp.is_active_equation(Force_Balance))
        
    @memcheck
    def Initialize(self):
        OOF.Mesh.Field.Define(
            mesh="meshtest:skeleton:fe_test",
            field=Temperature)
        OOF.Mesh.Set_Field_Initializer(
            mesh="meshtest:skeleton:fe_test",
            field=Temperature,
            initializer=FuncScalarFieldInit(function="x*y*z"))
        OOF.Mesh.Apply_Field_Initializers(mesh="meshtest:skeleton:fe_test")
        # Check the values on each node.
        for node in self.msh_obj.funcnodes():
            pos = node.position()
            val = Temperature.value(self.msh_obj, node, 0)
            self.assertEqual(val, pos[0]*pos[1]*pos[2])

        # Create a second mesh and initialize it from the first.
        OOF.Mesh.New(
            name='mesh<2>', skeleton='meshtest:skeleton',
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        OOF.Mesh.Field.Define(
            mesh="meshtest:skeleton:mesh<2>",
            field=Temperature)
        OOF.Mesh.Set_Field_Initializer(
            mesh='meshtest:skeleton:mesh<2>',
            field=Temperature,
            initializer=TwoVectorOtherMeshInit(mesh='meshtest:skeleton:fe_test')
            )
        OOF.Mesh.Apply_Field_Initializers(mesh="meshtest:skeleton:mesh<2>")
        # Check the field values at the nodes in the copied mesh
        other_msh_obj = mesh.meshes["meshtest:skeleton:mesh<2>"].getObject()
        for node in other_msh_obj.funcnodes():
            pos = node.position()
            val = Temperature.value(other_msh_obj, node, 0)
            self.assertEqual(val, pos[0]*pos[1]*pos[2])
        OOF.Mesh.Delete(mesh="meshtest:skeleton:mesh<2>")

    @memcheck
    def Interpolate(self):
        from ooflib.SWIG.engine import mastercoord
        MasterCoord = mastercoord.MasterCoord
        # Initialize a field and test the interpolated values inside
        # the elements.  Make sure that the field is linear, since
        # we're using linear elements.
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Set_Field_Initializer(
            mesh="meshtest:skeleton:fe_test",
            field=Temperature,
            initializer=FuncScalarFieldInit(function="x+2*y+3*z"))
        OOF.Mesh.Apply_Field_Initializers(mesh="meshtest:skeleton:fe_test")
        
        # Check a point inside each element
        m_coord = MasterCoord(0.15, 0.2, 0.25)
        for e in self.msh_obj.elements():
            lab_coord = e.from_master(m_coord)
            o = e.outputField(self.msh_obj, Temperature, m_coord)
            self.assertAlmostEqual(o.valuePtr().value(),
                             lab_coord[0]+2*lab_coord[1]+3*lab_coord[2])


# There is a toolbox for mesh cross-section operations, but it doesn't
# have a special menu, it just makes calls to the menu items tested
# here.
class OOF_Mesh_CrossSection(OOF_Mesh_FieldEquation):
    @memcheck
    def New(self):
        OOF.Mesh.Cross_Section.New(\
            name="testcs", mesh="meshtest:skeleton:fe_test",
            cross_section=StraightCrossSection(
            start=Point(0.2,0.5), end=Point(12.2,4.5)))
        self.assertEqual(len(self.msh.allCrossSectionNames()),1)
        cs = self.msh.cross_sections['testcs']
        self.assertEqual(cs.start, Point(0.2,0.5))
        self.assertEqual(cs.end, Point(12.2,4.5))
        

    @memcheck
    def Remove(self):
        OOF.Mesh.Cross_Section.New(mesh="meshtest:skeleton:fe_test",
            name="testcs", cross_section=StraightCrossSection(
            start=Point(0.2,0.5), end=Point(12.2,4.5)))
        OOF.Mesh.Cross_Section.Remove(
            mesh="meshtest:skeleton:fe_test", name="testcs")
        self.assertEqual(len(self.msh.allCrossSectionNames()),0)
        
        
    @memcheck
    def Copy(self):
        OOF.Mesh.Cross_Section.New(
            mesh="meshtest:skeleton:fe_test",
            name="testcs", cross_section=StraightCrossSection(
            start=Point(0.2,0.5), end=Point(12.2,4.5)))
        OOF.Mesh.Cross_Section.Copy(
            current="meshtest:skeleton:fe_test", cross_section="testcs",
            mesh="meshtest:skeleton:fe_test", name="testcs_copy")
        self.assertEqual(len(self.msh.allCrossSectionNames()),2)
        cs1 = self.msh.cross_sections['testcs']
        cs2 = self.msh.cross_sections['testcs_copy']
        self.assertNotEqual(id(cs1),id(cs2))

    @memcheck
    def Select(self):
        # Since the most recent cs is autoselected, we need at least
        # two before we can meaningfully test selection.
        OOF.Mesh.Cross_Section.New(
            mesh="meshtest:skeleton:fe_test",
            name="testcs1", cross_section=StraightCrossSection(
            start=Point(0.2,0.5), end=Point(12.2,4.5)))
        OOF.Mesh.Cross_Section.New(mesh="meshtest:skeleton:fe_test",
            name="testcs2", cross_section=StraightCrossSection(
            start=Point(4.5,12.2), end=Point(0.2,4.5)))
        self.assertEqual(self.msh.cross_sections.selectedName(),
                         "testcs2")
        OOF.Mesh.Cross_Section.Select(
            mesh="meshtest:skeleton:fe_test", cross_section="testcs1")
        self.assertEqual(self.msh.cross_sections.selectedName(),
                         "testcs1")
            

    @memcheck
    def Deselect(self):
        OOF.Mesh.Cross_Section.New(
            mesh="meshtest:skeleton:fe_test",
            name="testcs", cross_section=StraightCrossSection(
            start=Point(0.2,0.5), end=Point(12.2,4.5)))
        self.assertEqual(self.msh.cross_sections.selectedName(),"testcs")
        OOF.Mesh.Cross_Section.Deselect(mesh="meshtest:skeleton:fe_test")
        self.assertEqual(self.msh.cross_sections.selectedName(), None)


    @memcheck
    def Rename(self):
        OOF.Mesh.Cross_Section.New(
            mesh="meshtest:skeleton:fe_test",
            name="testcs", cross_section=StraightCrossSection(
            start=Point(0.2,0.5), end=Point(12.2,4.5)))
        cs1 = self.msh.cross_sections['testcs']
        OOF.Mesh.Cross_Section.Rename(mesh="meshtest:skeleton:fe_test",
                                      cross_section="testcs", name="bob")
        cs2 = self.msh.cross_sections['bob']
        self.assertEqual(len(self.msh.allCrossSectionNames()), 1)
        self.assertEqual(id(cs1),id(cs2))
            
    @memcheck
    def Edit(self):
        OOF.Mesh.Cross_Section.New(
            mesh="meshtest:skeleton:fe_test",
            name="testcs", cross_section=StraightCrossSection(
            start=Point(0.2,0.5), end=Point(12.2,4.5)))
        OOF.Mesh.Cross_Section.Edit(
            mesh="meshtest:skeleton:fe_test", name="testcs",
            cross_section=StraightCrossSection(
            start=Point(0.3,0.6), end=Point(12.1,4.2)))
        self.assertEqual(len(self.msh.allCrossSectionNames()), 1)
        cs = self.msh.cross_sections['testcs']
        self.assertEqual(cs.start, Point(0.3,0.6))
        self.assertEqual(cs.end, Point(12.1, 4.2))
        

class OOF_Mesh_BoundaryCondition(OOF_Mesh_FieldEquation):
    def setUp(self):
#         global profile
#         from ooflib.engine import profile
#         self.all_profiles = profile.AllProfiles
        OOF_Mesh_FieldEquation.setUp(self)
        # Activate temp and disp fields, set up a well-posed problem.
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Displacement)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Displacement)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Heat_Eqn)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Force_Balance)


    # Still fairly basic.
    @memcheck
    def NewBC(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymax"))
        self.assertEqual(len(self.msh.allBoundaryConds()), 1)
        bc = self.msh.getBdyCondition("bc_test")
        self.assertEqual(bc.__class__, bdycondition.DirichletBC)
        
        
    @memcheck
    def DeleteBC(self):
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymax"))
        OOF.Mesh.Boundary_Conditions.Delete(
            mesh="meshtest:skeleton:fe_test", name="bc_test")
        self.assertEqual(len(self.msh.allBoundaryConds()), 0)
        

    @memcheck
    def RenameBC(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymax"))
        OOF.Mesh.Boundary_Conditions.Rename(
            mesh="meshtest:skeleton:fe_test", bc="bc_test", name="bob")
        self.assertEqual(len(self.msh.allBoundaryConds()), 1)
        bc = self.msh.getBdyCondition("bob")
        self.assertEqual(bc.__class__, bdycondition.DirichletBC)
                                        

    @memcheck
    def CopyBC(self):
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymax"))
        OOF.Mesh.Boundary_Conditions.Copy(
            current="meshtest:skeleton:fe_test",
            mesh="meshtest:skeleton:fe_test", bc="bc_test",
            name="bc_test_copy", boundary="Ymin")
        self.assertEqual(len(self.msh.allBoundaryConds()),2)
        bc1 = self.msh.getBdyCondition("bc_test")
        bc2 = self.msh.getBdyCondition("bc_test_copy")
        self.assertNotEqual(id(bc1),id(bc2))

    @memcheck
    def Copy_AllBC(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test1", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymax"))
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test2", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymin"))
        OOF.Mesh.Copy(mesh="meshtest:skeleton:fe_test",
                      name="bc_target",
                      copy_field=True, copy_equation=True,
                      copy_bc=False)
        msh = mesh.meshes["meshtest:skeleton:bc_target"]
        OOF.Mesh.Boundary_Conditions.Copy_All(
            current="meshtest:skeleton:fe_test",
            mesh="meshtest:skeleton:bc_target")
        self.assertEqual(len(msh.allBoundaryConds()),2)
        bc1_1 = self.msh.getBdyCondition("bc_test1")
        bc1_2 = self.msh.getBdyCondition("bc_test2")
        bc1 = msh.getBdyCondition("bc_test1")
        bc2 = msh.getBdyCondition("bc_test2")
        self.assertNotEqual(id(bc1_1),id(bc1))
        self.assertNotEqual(id(bc1_2),id(bc2))
        OOF.Mesh.Delete(mesh="meshtest:skeleton:bc_target")
        

    @memcheck
    def EditBC(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymax"))
        OOF.Mesh.Boundary_Conditions.Edit(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(
                field=Displacement,
                field_component="x",
                equation=Force_Balance,
                eqn_component="x",
                profile=ContinuumProfileXTd(
                    function="x",timeDerivative='0',timeDerivative2='0'),
                boundary="Ymax"))
        self.assertEqual(len(self.msh.allBoundaryConds()),1)
        bc = self.msh.getBdyCondition("bc_test")
        self.assertEqual(bc.__class__, bdycondition.DirichletBC)
        self.assertEqual(bc.field, Displacement)
        self.assertEqual(bc.equation, Force_Balance)
            


class OOF_Mesh_SaveLoad(OOF_Mesh_FieldEquation):
    def setUp(self):
        OOF_Mesh_FieldEquation.setUp(self)

    @memcheck
    def Save(self):
        # Before saving, define some fields and bcs.
        OOF.Mesh.Rename(mesh="meshtest:skeleton:fe_test", name="save_test")
        OOF.Subproblem.Field.Define(
            subproblem="meshtest:skeleton:save_test:default",
            field=Temperature)
        OOF.Subproblem.Field.Define(
            subproblem="meshtest:skeleton:save_test:default",
            field=Displacement)
        OOF.Mesh.Set_Field_Initializer(
            mesh='meshtest:skeleton:save_test',
            field=Displacement,
            initializer=ConstThreeVectorFieldInit(cx=1,cy=2,cz=3))
        OOF.Mesh.Set_Field_Initializer(
            mesh='meshtest:skeleton:save_test',
            field=Temperature, 
            initializer=FuncScalarFieldInit(function='sin(x)'))
        OOF.Mesh.Apply_Field_Initializers(
            mesh='meshtest:skeleton:save_test')

        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:save_test",
                                field=Temperature)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:save_test",
                                   equation=Heat_Eqn)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:save_test",
                                   equation=Force_Balance)
        OOF.Mesh.Boundary_Conditions.New(
            name="high", mesh="meshtest:skeleton:save_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ConstantProfile(value=1.0),
                boundary="Ymax"))
        OOF.Mesh.Boundary_Conditions.New(
            name="low", mesh="meshtest:skeleton:save_test",
            condition=DirichletBC(
                field=Temperature,
                field_component="",
                equation=Heat_Eqn,
                eqn_component="",
                profile=ConstantProfile(value=0.0),
                boundary="Ymin"))
        OOF.Mesh.Boundary_Conditions.New(
            name="floatdisp", mesh="meshtest:skeleton:save_test",
            condition=FloatBC(
                field=Displacement, field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.0),
                boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.New(
            name="floattemp", mesh="meshtest:skeleton:save_test",
            condition=FloatBC(
                field=Temperature,
                field_component='x',
                equation=Heat_Eqn,
                eqn_component='x',
                profile=ConstantProfile(value=0.0),
                boundary='Xmin'))
        OOF.Subproblem.Set_Solver(
            subproblem='meshtest:skeleton:save_test:default',
            solver_mode=BasicSolverMode(
                time_stepper=BasicAdaptiveDriver(
                    tolerance=0.0001,minstep=1.0e-05),
                matrix_method=BasicIterative(
                    tolerance=1e-13,max_iterations=1234)))
        OOF.Mesh.Boundary_Conditions.Set_BC_Initializer(
            mesh='meshtest:skeleton:save_test',
            bc='floatdisp',
            initializer=FloatBCInitMin_td(value=0.2, time_derivative=0.1))
        OOF.Mesh.Boundary_Conditions.Set_BC_Initializer(
            mesh='meshtest:skeleton:save_test',
            bc='floattemp',
            initializer=FloatBCInitMin(value=0.3))
        OOF.File.Save.Mesh(
            filename="mesh_save_test",
            mode="w", format="ascii",
            mesh="meshtest:skeleton:save_test")
        self.assert_(
            file_utils.fp_file_compare(
                "mesh_save_test",
                os.path.join("mesh_data", "saved_mesh"),
                1.e-10))
        os.remove("mesh_save_test")

    @memcheck
    def Load(self):
        from ooflib.engine import bdycondition
        OOF.File.Load.Data(filename=reference_file("mesh_data", "saved_mesh"))
        msh = mesh.meshes["meshtest:skeleton:save_test"]
        subp = msh.get_default_subproblem().getObject()
        self.assert_(Temperature.is_defined(subp))
        self.assert_(Temperature.is_active(subp))
        self.assert_(subp.is_active_equation(Heat_Eqn))
        bc1 = msh.getBdyCondition("high")
        bc2 = msh.getBdyCondition("low")
        self.assertEqual(bc1.__class__, bdycondition.DirichletBC)
        self.assertEqual(bc2.__class__, bdycondition.DirichletBC)
        bc3 = msh.getBdyCondition("floattemp")
        bc4 = msh.getBdyCondition("floatdisp")
        self.assertEqual(bc3.__class__, bdycondition.FloatBC)
        self.assertEqual(bc4.__class__, bdycondition.FloatBC)
        self.assertEqual(bc3.initializer,
                         bdycondition.FloatBCInitMin(value=0.3))
        self.assertEqual(bc4.initializer,
                         bdycondition.FloatBCInitMin_td(value=0.2,
                                                        time_derivative=0.1))
        self.assertEqual(bc1.initializer, None)
        self.assertEqual(bc2.initializer, None)

        # Save again, and make sure the file is the same.
        OOF.File.Save.Mesh(
            filename="mesh_load_test",
            mode="w", format="ascii",
            mesh="meshtest:skeleton:save_test")
        self.assert_(
            file_utils.fp_file_compare(
                "mesh_load_test",
                os.path.join("mesh_data", "saved_mesh"),
                1.e-10))
        os.remove("mesh_load_test")

# Extra test, to make sure the NeumannBC Edit/New bug does not recur.
# The pathology was, if you create Neumann BCs, then edit the
# most-recently-created one, the "New" command would fail with an
# exception.  This should now not fail.
class OOF_Mesh_BC_Extra(OOF_Mesh_BoundaryCondition):
    @memcheck
    def NeumannBCNewEdit(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test_1", mesh="meshtest:skeleton:fe_test",
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=0.1),
                                         ConstantProfile(value=0.2)],
                                boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.Edit(
            name="bc_test_1", mesh="meshtest:skeleton:fe_test",
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=0.2),
                                         ConstantProfile(value=0.4)],
                                boundary='Ymax'))
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test_2", mesh="meshtest:skeleton:fe_test",
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=-0.2),
                                         ConstantProfile(value=0.0)],
                                boundary='Ymin'))
        self.assertEqual(len(self.msh.allBoundaryConds()), 2)
        bc1 = self.msh.getBdyCondition("bc_test_1")
        bc2 = self.msh.getBdyCondition("bc_test_2")
        self.assertEqual(bc1.__class__, bdycondition.NeumannBC)
        self.assertEqual(bc2.__class__, bdycondition.NeumannBC)
        # Parent class tearDown routine removes the mesh, so no need
        # to delete the BCs.

class OOF_Mesh_Special(OOF_Mesh_Base):
    # Check for a bug that raised an exception if a Mesh was deleted
    # after its Skeleton was modified. 
    def Skel_Mod_Mesh_Delete(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        OOF.Skeleton.Modify(
            skeleton='microstructure:skeleton',
            modifier=Refine(targets=CheckAllElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))
        OOF.Mesh.Delete(mesh='microstructure:skeleton:mesh')
        # This line used to raise the exception:
        OOF.Microstructure.Delete(microstructure='microstructure')

    # Same as Skel_Mod_Mesh_Delete, but for Anneal instead of Refine.
    def Skel_Mod_Mesh_Delete2(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton', 
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        OOF.Skeleton.Modify(
            skeleton='microstructure:skeleton',
            modifier=Anneal(targets=AllNodes(),
                            criterion=AverageEnergy(alpha=0.3),
                            T=0.0,delta=1.0,
                            iteration=FixedIteration(iterations=5)))
        OOF.Mesh.Delete(mesh='microstructure:skeleton:mesh')
        OOF.Microstructure.Delete(microstructure='microstructure')

    # Check that a boundary condition initializer can be copied from
    # one mesh to another.
    @memorycheck.check("microstructure")
    def Copy_BC_Init(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(
            name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material',
            microstructure='microstructure',
            pixels=every)
        OOF.Material.Add_property(
            name='material',
            property='Mechanical:Elasticity:Isotropic')
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'Q4_4', 'T3_3', 'D2_2'])
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
            condition=FloatBC(
                field=Displacement,field_component='x',
                equation=Force_Balance,eqn_component='x',
                profile=ConstantProfile(value=0.0),
                boundary='Xmax'))
        OOF.Mesh.Boundary_Conditions.Set_BC_Initializer(
            mesh='microstructure:skeleton:mesh',
            bc='bc',
            initializer=FloatBCInitMin(value=2))
        OOF.Mesh.New(
            name='mesh<2>',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'Q4_4', 'T3_3', 'D2_2'])
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh<2>:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh<2>:default',
            field=Displacement)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh<2>:default',
            equation=Force_Balance)
        OOF.Mesh.Boundary_Conditions.Copy(
            current='microstructure:skeleton:mesh',
            mesh='microstructure:skeleton:mesh<2>',
            bc='bc', name='bc',
            boundary='Xmax')
        OOF.Mesh.Copy_Field_Initializers(
            source='microstructure:skeleton:mesh',
            target='microstructure:skeleton:mesh<2>')
        OOF.File.Save.Mesh(
            filename='copy_bc_init.mesh',
            mode='w', format='ascii',
            mesh='microstructure:skeleton:mesh<2>')
        self.assert_(
            file_utils.fp_file_compare(
                "copy_bc_init.mesh",
                os.path.join("mesh_data", "copy_bc_init.mesh"),
                1.e-10))
        os.remove("copy_bc_init.mesh")


    # TODO 3.1: This Rebuild check uses materials assigned to skeleton
    # groups, which isn't implemented.  This test should be reinstated
    # when assigning materials is supported.  See TODO in
    # skeletongroupmenu.py.
    @memorycheck.check("microstructure")
    def RebuildOLD(self):
        global mesh
        from ooflib.engine import mesh
        OOF.Microstructure.New(
            name='microstructure', width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Material.New(name='material', material_type='bulk')
        OOF.Material.Assign(
            material='material', microstructure='microstructure', pixels=all)
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Windows.Graphics.New()
        # OOF.LayerEditor.LayerSet.New(window='Graphics_1')
        # OOF.LayerEditor.LayerSet.DisplayedObject(
        #     category='Microstructure', object='microstructure')
        # OOF.LayerEditor.LayerSet.Add_Method(
        #     method=MicrostructureMaterialDisplay(
        #         no_material=Gray(value=0.0),
        #         no_color=RGBColor(red=0.00000,green=0.00000,blue=1.00000)))
        # OOF.LayerEditor.LayerSet.Send(window='Graphics_1')
        OOF.Mesh.New(
            name='mesh',
            skeleton='microstructure:skeleton',
            element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
        msh = mesh.meshes["microstructure:skeleton:mesh"]

        # Assign a different material to one element
        OOF.Material.New(name='material<2>', material_type='bulk')
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='microstructure:skeleton',
            points=[Point(0.436771,0.54968,2.12376)],
            view=View(cameraPosition=Coord(0.5,0.5,3.42583), 
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=690, size_y=618),
            shift=0, ctrl=0)
        OOF.ElementGroup.New_Group(
            skeleton='microstructure:skeleton', name='elementgroup')
        OOF.ElementGroup.Add_to_Group(
            skeleton='microstructure:skeleton', group='elementgroup')
        OOF.ElementGroup.Assign_Material(
            skeleton='microstructure:skeleton', group='elementgroup',
            material='material<2>')
        
        # Check initial material assignments.
        mcounts = countMaterials(msh)
        self.assertEqual(mcounts['material'], 319)
        self.assertEqual(mcounts['material<2>'], 1)

        # Refine the Skeleton.
        OOF.Skeleton.Modify(
            skeleton='microstructure:skeleton',
            modifier=Refine(targets=CheckSelectedElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))

        # Check that mesh still has the same materials, and hasn't
        # been refined.
        mcounts = countMaterials(msh)
        self.assertEqual(mcounts['material'], 319)
        self.assertEqual(mcounts['material<2>'], 1)
        self.assert_(msh.outOfSync())

        # Propagate the refinement to the Mesh.
        OOF.Mesh.Modify(
            mesh='microstructure:skeleton:mesh', 
            modifier=RebuildMesh())
        
        # Check that the materials have been updated.
        mcounts = countMaterials(msh)
        self.assert_(mcounts['material'], 336)
        self.assertEqual(mcounts['material<2>'], 8)
        self.assert_(not msh.outOfSync())

        OOF.Skeleton.Undo(skeleton='microstructure:skeleton')
        
        # Check that material counts have not yet been updated.
        mcounts = countMaterials(msh)
        self.assert_(mcounts['material'], 336)
        self.assertEqual(mcounts['material<2>'], 8)
        self.assert_(msh.outOfSync())

        OOF.Mesh.Modify(
            mesh='microstructure:skeleton:mesh', modifier=RebuildMesh())

        mcounts = countMaterials(msh)
        self.assertEqual(mcounts['material'], 319)
        self.assertEqual(mcounts['material<2>'], 1)
        self.assert_(not msh.outOfSync())
        
        # Remove explicitly assigned material and check that the mesh
        # is updated automatically.
        OOF.ElementGroup.Remove_Material(
            skeleton='microstructure:skeleton', group='elementgroup')
        mcounts = countMaterials(msh)
        self.assertEqual(mcounts['material'], 320)
        self.assert_(not msh.outOfSync())
        OOF.Graphics_1.File.Close()

        OOF.Material.Delete(name="material")
        OOF.Material.Delete(name="material<2>")

    # Check abaqus output
    @memorycheck.check("solve_test")
    def AbaqusFormat(self):
        OOF.File.LoadStartUp.Data(
            filename=reference_file('mesh_data', 'solveable'))
        OOF.File.Save.Mesh(filename='solveable.abq', mode='w', format='abaqus',
                           mesh='solve_test:skeleton:mesh')
        # Use fp_file_compare because it can ignore dates in files,
        # and the abaqus output contains the date in the header.
        self.assert_(
            file_utils.fp_file_compare(
                'solveable.abq',
                os.path.join('mesh_data', 'solveable.abq'),
                tolerance=1.e-8, ignoretime=True))
        file_utils.remove('solveable.abq')
        OOF.Material.Delete(name='mortar')
        OOF.Material.Delete(name='bricks')
        OOF.Property.Delete(property='Color:bloo')
        OOF.Property.Delete(property='Color:wred')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:soft')
        OOF.Property.Delete(property='Mechanical:Elasticity:Isotropic:stiff')

def countMaterials(meshctxt):
    counts = {}
    total = 0
    for e in meshctxt.getObject().elements():
        total += 1
        m = e.material()
        if m:
            mname = m.name()
        else:
            mname = None
        counts[mname] = counts.get(mname, 0) + 1
    return counts

###############################

basic_set = [
    OOF_Mesh("New"),
    OOF_Mesh("Delete"),
    OOF_Mesh("Copy"),
    OOF_Mesh("Rename"),
    OOF_Mesh("Skeleton_Delete"),
    OOF_Mesh("Mesh_Rebuild"),
    ]


field_equation_set = [
    OOF_Mesh_FieldEquation("DefineField"),
    OOF_Mesh_FieldEquation("UndefineField"),
    OOF_Mesh_FieldEquation("ActivateField"),
    OOF_Mesh_FieldEquation("DeactivateField"),
    # OOF_Mesh_FieldEquation("In_PlaneField"),
    # OOF_Mesh_FieldEquation("Out_of_PlaneField"),
    OOF_Mesh_FieldEquation("ActivateEquation"),
    OOF_Mesh_FieldEquation("DeactivateEquation")
    ]

extra_set = [
    OOF_Mesh_Extra("Copy"),
    OOF_Mesh_Extra("Copy_Field_State"),
    OOF_Mesh_Extra("Copy_Equation_State"),
    OOF_Mesh_Extra("Initialize"),
    OOF_Mesh_Extra("Interpolate"),
    ]

crosssection_set = [
    OOF_Mesh_CrossSection("New"),
    OOF_Mesh_CrossSection("Remove"),
    OOF_Mesh_CrossSection("Copy"),
    OOF_Mesh_CrossSection("Select"),
    OOF_Mesh_CrossSection("Deselect"),
    OOF_Mesh_CrossSection("Rename"),
    OOF_Mesh_CrossSection("Edit")
    ]

bc_set = [
    OOF_Mesh_BoundaryCondition("NewBC"),
    OOF_Mesh_BoundaryCondition("DeleteBC"),
    OOF_Mesh_BoundaryCondition("RenameBC"),
    OOF_Mesh_BoundaryCondition("CopyBC"),
    OOF_Mesh_BoundaryCondition("Copy_AllBC"),
    OOF_Mesh_BoundaryCondition("EditBC")
    ]

file_set = [
    OOF_Mesh_SaveLoad("Save"),
    OOF_Mesh_SaveLoad("Load")
    ]

bc_extra_set = [
    OOF_Mesh_BC_Extra("NeumannBCNewEdit"),
    ]

special_set = [
    OOF_Mesh_Special("Skel_Mod_Mesh_Delete"),
    OOF_Mesh_Special("Skel_Mod_Mesh_Delete2"),
    OOF_Mesh_Special("Copy_BC_Init"),
    #OOF_Mesh_Special("Rebuild"),
    #OOF_Mesh_Special("AbaqusFormat")
    ]


test_set = (basic_set + field_equation_set + extra_set + bc_set + file_set
            + bc_extra_set
            ## TODO 3.1: Uncomment when crosssection toolbox is enabled
            # + crosssection_set
            + special_set
            )
#test_set = bc_extra_set
