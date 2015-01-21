# -*- python -*-
# $RCSfile: mesh_test.py,v $
# $Revision: 1.34 $
# $Author: langer $
# $Date: 2009/07/07 18:42:44 $

# Test suite for the menu commands under OOF.Mesh.*

import unittest, os, filecmp
import file_compare
import memorycheck

## TODO: Check that Skeleton modifications are propagated correctly to
## Meshes, and that Mesh.outOfSync is correct when making, undoing,
## and redoing Skeleton modifications.

# Basic mesh operations -- creation, destruction, copying.
# Modify might be complicated.
class OOF_Mesh(unittest.TestCase):
    def setUp(self):
        # Probably import some mesh stuff, so you can tell if there are any...
        global mesh, subproblemcontext, femesh, cskeleton, cmicrostructure
        from ooflib.engine import mesh
        from ooflib.engine import subproblemcontext
        from ooflib.SWIG.engine import femesh
        from ooflib.SWIG.engine import cskeleton
        from ooflib.SWIG.common import cmicrostructure
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="meshtest",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="meshtest:small.ppm")
        OOF.Skeleton.New(
            name="skeleton", microstructure="meshtest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))

    @memorycheck.check("meshtest")
    def New(self):
        OOF.Mesh.New(name="test", skeleton="meshtest:skeleton",
                     element_types=['T3_3', 'Q4_4'])
        msh = mesh.meshes["meshtest:skeleton:test"]
        self.assertNotEqual(msh, None)
        self.assertEqual(mesh.meshes.nActual(), 1)

    @memorycheck.check("meshtest")
    def Delete(self):
        OOF.Mesh.New(name="test", skeleton="meshtest:skeleton",
                     element_types=['T3_3', 'Q4_4'])
        OOF.Mesh.Delete(mesh="meshtest:skeleton:test")
        self.assertEqual(mesh.meshes.nActual(), 0)
        self.assertEqual(subproblemcontext.subproblems.nActual(), 0)

    @memorycheck.check("meshtest")
    def Copy(self):
        OOF.Mesh.New(name="test", skeleton="meshtest:skeleton",
                     element_types=['T3_3', 'Q4_4'])
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
                     element_types=['T3_3', 'Q4_4'])
        msh = mesh.meshes["meshtest:skeleton:test"]
        OOF.Mesh.Rename(mesh="meshtest:skeleton:test",name="bob")
        msh2 = mesh.meshes["meshtest:skeleton:bob"]
        self.assertEqual(mesh.meshes.nActual(), 1)
        self.assertEqual(id(msh),id(msh2))
        self.assertEqual(id(msh.getObject()), id(msh2.getObject()) )
    

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
                     element_types=['T3_3', 'Q4_4'])
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


    @memcheck
    def In_PlaneField(self):
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        self.assert_(not self.msh_obj.in_plane(Temperature))
        OOF.Mesh.Field.In_Plane(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        self.assert_(self.msh_obj.in_plane(Temperature))

    @memcheck
    def Out_of_PlaneField(self):
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        OOF.Mesh.Field.In_Plane(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        OOF.Mesh.Field.Out_of_Plane(mesh="meshtest:skeleton:fe_test",
                                    field=Temperature)
        self.assert_(not self.msh_obj.in_plane(Temperature))


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
    def Copy_Field_State(self):
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:fe_test",
                                field=Temperature)
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Displacement)
        OOF.Mesh.New(name="fe_copy_test",
                     skeleton="meshtest:skeleton",
                     element_types=['T3_3','Q4_4'])
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
                     element_types=['T3_3','Q4_4'])
        subp = subproblemcontext.subproblems[
            'meshtest:skeleton:fe_copy_test:default'].getObject()
        self.assert_(not subp.is_active_equation(Heat_Eqn))
        OOF.Mesh.Copy_Equation_State(source="meshtest:skeleton:fe_test",
                                     target="meshtest:skeleton:fe_copy_test")
        self.assert_(subp.is_active_equation(Heat_Eqn))
        self.assert_(not subp.is_active_equation(Force_Balance))
        
    @memcheck
    def Initialize(self):
        from ooflib.SWIG.engine import mastercoord
        MasterCoord = mastercoord.MasterCoord
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:fe_test",
                              field=Temperature)
        OOF.Mesh.Set_Field_Initializer(
            mesh="meshtest:skeleton:fe_test",
            field=Temperature,
            initializer=FuncScalarFieldInit(function="x*y"))
        OOF.Mesh.Apply_Field_Initializers(mesh="meshtest:skeleton:fe_test")
        # Check the center of each element.
        for e in self.msh_obj.element_iterator():
            m_coord = MasterCoord(0.0,0.0)
            lab_coord = e.from_master(MasterCoord(0.0,0.0))
            o = e.outputField(self.msh_obj, Temperature, MasterCoord(0.0,0.0))
            self.assertEqual(o.valuePtr().value(),
                             lab_coord[0]*lab_coord[1])
        # Create a second mesh and initialize it from the first.
        OOF.Mesh.New(name='mesh<2>', skeleton='meshtest:skeleton',
                     element_types=['D2_2', 'T3_3', 'Q4_4'])
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:mesh<2>",
                              field=Temperature)
        OOF.Mesh.Set_Field_Initializer(
            mesh='meshtest:skeleton:mesh<2>',
            field=Temperature,
            initializer=TwoVectorOtherMeshInit(mesh='meshtest:skeleton:fe_test')
            )
        OOF.Mesh.Apply_Field_Initializers(mesh="meshtest:skeleton:mesh<2>")
        # Check the center of each element in the copied mesh.
        other_msh_obj = mesh.meshes["meshtest:skeleton:mesh<2>"].getObject()
        for e in other_msh_obj.element_iterator():
            m_coord = MasterCoord(0.0,0.0)
            lab_coord = e.from_master(MasterCoord(0.0,0.0))
            o = e.outputField(other_msh_obj, Temperature, MasterCoord(0.0,0.0))
            self.assertEqual(o.valuePtr().value(),
                             lab_coord[0]*lab_coord[1])
        OOF.Mesh.Delete(mesh="meshtest:skeleton:mesh<2>")



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
        

class OOF_Mesh_ProfileBC(OOF_Mesh_FieldEquation):
    def setUp(self):
        global profile
        from ooflib.engine import profile
        self.all_profiles = profile.AllProfiles
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
                                   equation=Plane_Heat_Flux)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Force_Balance)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:fe_test",
                                   equation=Plane_Stress)

        # Parent-class tear-down removes the microstructure, so
        # nothing to do here.
        
    @memcheck
    def NewProfile(self):
        OOF.Mesh.Profiles.New(name="p_test",
                              profile=LinearProfile(start=0.0, end=10.0))
        self.assertEqual(len(self.all_profiles.keys()),1)
        prf = self.all_profiles['p_test']
        self.assertEqual(prf.start, 0.0)
        self.assertEqual(prf.end, 10.0)
        
    # Delete assumes "p_test" profile was successfully created.
    @memcheck
    def DeleteProfile(self):
        OOF.Mesh.Profiles.Delete(name="p_test")
        self.assertEqual(len(self.all_profiles.keys()),0)

    @memcheck
    def RenameProfile(self):
        OOF.Mesh.Profiles.New(name="p_test",
                              profile=LinearProfile(start=0.0, end=10.0))
        prf1 = self.all_profiles['p_test']
        OOF.Mesh.Profiles.Rename(profile="p_test", name="fred")
        prf2 = self.all_profiles['fred']
        self.assertEqual(len(self.all_profiles.keys()),1)
        self.assertEqual(id(prf1),id(prf2))
        OOF.Mesh.Profiles.Delete(name="fred")

    @memcheck
    def CopyProfile(self):
        OOF.Mesh.Profiles.New(name="p_test",
                              profile=LinearProfile(start=0.0, end=10.0))
        prf1 = self.all_profiles['p_test']
        OOF.Mesh.Profiles.Copy(profile="p_test", name="fred")
        self.assertEqual(len(self.all_profiles.keys()),2)
        prf2 = self.all_profiles['fred']
        self.assertNotEqual(id(prf1),id(prf2))
        OOF.Mesh.Profiles.Delete(name="p_test")
        OOF.Mesh.Profiles.Delete(name="fred")

    @memcheck
    def EditProfile(self):
        from ooflib.engine import profilefunction
        OOF.Mesh.Profiles.New(name="p_test",
                              profile=LinearProfile(start=0.0, end=10.0))
        OOF.Mesh.Profiles.Edit(name="p_test",
                               profile=ContinuumProfile(function="x"))
        self.assertEqual(len(self.all_profiles.keys()),1)
        prf1 = self.all_profiles['p_test']
        self.assertEqual(prf1.function,
                         profilefunction.ProfileFunction("x"))
        OOF.Mesh.Profiles.Delete(name="p_test")

    # Still fairly basic.
    @memcheck
    def NewBC(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="top"))
        self.assertEqual(len(self.msh.allBoundaryConds()), 1)
        bc = self.msh.getBdyCondition("bc_test")
        self.assertEqual(bc.__class__, bdycondition.DirichletBC)
        
        
    @memcheck
    def DeleteBC(self):
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="top"))
        OOF.Mesh.Boundary_Conditions.Delete(
            mesh="meshtest:skeleton:fe_test", name="bc_test")
        self.assertEqual(len(self.msh.allBoundaryConds()), 0)
        

    @memcheck
    def RenameBC(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="top"))
        OOF.Mesh.Boundary_Conditions.Rename(
            mesh="meshtest:skeleton:fe_test", bc="bc_test", name="bob")
        self.assertEqual(len(self.msh.allBoundaryConds()), 1)
        bc = self.msh.getBdyCondition("bob")
        self.assertEqual(bc.__class__, bdycondition.DirichletBC)
                                        

    @memcheck
    def CopyBC(self):
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="top"))
        OOF.Mesh.Boundary_Conditions.Copy(
            current="meshtest:skeleton:fe_test",
            mesh="meshtest:skeleton:fe_test", bc="bc_test",
            name="bc_test_copy", boundary="bottom")
        self.assertEqual(len(self.msh.allBoundaryConds()),2)
        bc1 = self.msh.getBdyCondition("bc_test")
        bc2 = self.msh.getBdyCondition("bc_test_copy")
        self.assertNotEqual(id(bc1),id(bc2))

    @memcheck
    def Copy_AllBC(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test1", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="top"))
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test2", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="bottom"))
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
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="top"))
        OOF.Mesh.Boundary_Conditions.Edit(
            name="bc_test", mesh="meshtest:skeleton:fe_test",
            condition=DirichletBC(field=Displacement,
                                  field_component="x",
                                  equation=Force_Balance,
                                  eqn_component="x",
                                  profile=ContinuumProfile(function="x"),
                                  boundary="top"))
        self.assertEqual(len(self.msh.allBoundaryConds()),1)
        bc = self.msh.getBdyCondition("bc_test")
        self.assertEqual(bc.__class__, bdycondition.DirichletBC)
        self.assertEqual(bc.field, Displacement)
        self.assertEqual(bc.equation, Force_Balance)
            


class OOF_Mesh_SaveLoad(OOF_Mesh_FieldEquation):
    def setUp(self):
        OOF_Mesh_FieldEquation.setUp(self)
        from ooflib.engine import profile
        self.all_profiles = profile.AllProfiles

    @memcheck
    def ProfileSave(self):
        OOF.Mesh.Profiles.New(name="save_test",
                              profile=LinearProfile(start=10.0,end=3.141))
        OOF.File.Save.Profile(filename="profile_save_test",
                              mode="w", format="ascii", profile="save_test")
        self.assert_(filecmp.cmp(os.path.join("mesh_data","saved_profile"),
                                 "profile_save_test"))
        os.remove("profile_save_test")
        OOF.Mesh.Profiles.Delete(name="save_test")

    @memcheck
    def ProfileLoad(self):
        OOF.File.Load.Data(filename=os.path.join("mesh_data",
                                                 "load_profile"))
        self.assertEqual(len(self.all_profiles.keys()),1)
        prf = self.all_profiles["load_test"]
        self.assertEqual(prf.start, 10.0)
        self.assertEqual(prf.end, 3.141)
        OOF.Mesh.Profiles.Delete(name="load_test")
        

    @memcheck
    def Save(self):
        # Before saving, define some fields and bcs.
        OOF.Mesh.Rename(mesh="meshtest:skeleton:fe_test", name="save_test")
        OOF.Mesh.Field.Define(mesh="meshtest:skeleton:save_test",
                              field=Temperature)
        OOF.Mesh.Set_Field_Initializer(
            mesh="meshtest:skeleton:save_test",
            field=Temperature,
            initializer=ConstScalarFieldInit(value=0.0))
        OOF.Mesh.Set_Field_Initializer(
            mesh="meshtest:skeleton:save_test",
            field=Temperature_z,
            initializer=ConstScalarFieldInit(value=0.0))
        OOF.Mesh.Field.Activate(mesh="meshtest:skeleton:save_test",
                                field=Temperature)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:save_test",
                                   equation=Heat_Eqn)
        OOF.Mesh.Equation.Activate(mesh="meshtest:skeleton:save_test",
                                   equation=Plane_Heat_Flux)
        OOF.Mesh.Boundary_Conditions.New(
            name="high", mesh="meshtest:skeleton:save_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ConstantProfile(value=1.0),
                                  boundary="top"))
        OOF.Mesh.Boundary_Conditions.New(
            name="low", mesh="meshtest:skeleton:save_test",
            condition=DirichletBC(field=Temperature,
                                  field_component="",
                                  equation=Heat_Eqn,
                                  eqn_component="",
                                  profile=ConstantProfile(value=0.0),
                                  boundary="bottom"))
        OOF.File.Save.Mesh(filename="mesh_save_test",
                           mode="w", format="ascii",
                           mesh="meshtest:skeleton:save_test")
        self.assert_(filecmp.cmp(os.path.join("mesh_data", "saved_mesh"),
                                 "mesh_save_test"))
        os.remove("mesh_save_test")

    @memcheck
    def Load(self):
        from ooflib.engine import bdycondition
        OOF.File.Load.Data(filename=os.path.join("mesh_data", "load_mesh"))
        msh = mesh.meshes["meshtest:skeleton:load_test"]
        subp = msh.get_default_subproblem().getObject()
        self.assert_(Temperature.is_defined(subp))
        self.assert_(Temperature.is_active(subp))
        self.assert_(subp.is_active_equation(Heat_Eqn))
        self.assert_(subp.is_active_equation(Plane_Heat_Flux))
        bc1 = msh.getBdyCondition("high")
        bc2 = msh.getBdyCondition("low")
        self.assertEqual(bc1.__class__, bdycondition.DirichletBC)
        self.assertEqual(bc2.__class__, bdycondition.DirichletBC)
        


# Extra test, to make sure the NeumannBC Edit/New bug does not recur.
# The pathology was, if you create Nuemann BCs, then edit the
# most-recently-created one, the "New" command would fail with an
# exception.  This should now not fail.
class OOF_Mesh_BC_Extra(OOF_Mesh_ProfileBC):
    @memcheck
    def NeumannBCNewEdit(self):
        from ooflib.engine import bdycondition
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test_1", mesh="meshtest:skeleton:fe_test",
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=0.1)],
                                boundary='top',normal=False))
        OOF.Mesh.Boundary_Conditions.Edit(
            name="bc_test_1", mesh="meshtest:skeleton:fe_test",
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=0.2)],
                                boundary='top',normal=False))
        OOF.Mesh.Boundary_Conditions.New(
            name="bc_test_2", mesh="meshtest:skeleton:fe_test",
            condition=NeumannBC(flux=Stress,
                                profile=[ConstantProfile(value=0.0),
                                         ConstantProfile(value=-0.2)],
                                boundary='bottom',normal=False))
        self.assertEqual(len(self.msh.allBoundaryConds()), 2)
        bc1 = self.msh.getBdyCondition("bc_test_1")
        bc2 = self.msh.getBdyCondition("bc_test_2")
        self.assertEqual(bc1.__class__, bdycondition.NeumannBC)
        self.assertEqual(bc2.__class__, bdycondition.NeumannBC)
        # Parent class tearDown routine removes the mesh, so no need
        # to delete the BCs.


class OOF_Mesh_Special(unittest.TestCase):
    # Now that meshes work, we can whether skeleton deletion removes
    # the mesh correctly.
    def Skeleton_Delete(self):
        from ooflib.engine import mesh
        from ooflib.engine import skeletoncontext
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="deltest",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="deltest:small.ppm")
        OOF.Skeleton.New(
            name="skeleton",
            microstructure="deltest",
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))
        OOF.Mesh.New(name="test", skeleton="deltest:skeleton",
                     element_types=['T3_3', 'Q4_4'])
        #
        OOF.Skeleton.Delete(skeleton="deltest:skeleton")
        self.assertEqual(mesh.meshes.nActual(), 0)
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        self.assertEqual(femesh.get_globalFEMeshCount(), 0)
        self.assertEqual(cskeleton.get_globalNodeCount(), 0)
        self.assertEqual(cskeleton.get_globalElementCount(), 0)
        OOF.Microstructure.Delete(microstructure="deltest")
        self.assertEqual(cmicrostructure.get_globalMicrostructureCount(), 0)
    
    # Check for a bug that raised an exception if a Mesh was deleted
    # after its Skeleton was modified.  TODO: Check this for Anneal as
    # well as Modify.
    def Skel_Mod_Mesh_Delete(self):
        OOF.Microstructure.New(
            name='microstructure', width=1.0, height=1.0,
            width_in_pixels=10, height_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton', microstructure='microstructure',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))
        OOF.Mesh.New(
            name='mesh', skeleton='microstructure:skeleton',
            element_types=['D2_2', 'T3_3', 'Q4_4'])
        OOF.Skeleton.Modify(
            skeleton='microstructure:skeleton',
            modifier=Refine(targets=CheckAllElements(),
                            criterion=Unconditionally(),
                            degree=Bisection(rule_set='conservative'),
                            alpha=0.29999999999999999))
        OOF.Mesh.Delete(mesh='microstructure:skeleton:mesh')
        # This line used to raise the exception:
        OOF.Microstructure.Delete(microstructure='microstructure')

    # Check abaqus output
    @memorycheck.check("solve_test")
    def AbaqusFormat(self):
        OOF.File.LoadStartUp.Data(
            filename=os.path.join('mesh_data', 'solveable'))
        OOF.File.Save.Mesh(filename='solveable.abq', mode='w', format='abaqus',
                           mesh='solve_test:skeleton:mesh')
        # Use fp_file_compare because it can ignore dates in files,
        # and the abaqus output contains the date in the header.
        self.assert_(file_compare.fp_file_compare(
            os.path.join('mesh_data', 'solveable.abq'), 'solveable.abq',
            tolerance=1.e-8, ignoretime=True))
        os.remove('solveable.abq')
        OOF.Material.Delete(name='mortar')
        OOF.Material.Delete(name='bricks')

###############################

def run_tests():
    basic_set = [
        OOF_Mesh("New"),
        OOF_Mesh("Delete"),
        OOF_Mesh("Copy"),
        OOF_Mesh("Rename")
        ]
    

    field_equation_set = [
        OOF_Mesh_FieldEquation("DefineField"),
        OOF_Mesh_FieldEquation("UndefineField"),
        OOF_Mesh_FieldEquation("ActivateField"),
        OOF_Mesh_FieldEquation("DeactivateField"),
        OOF_Mesh_FieldEquation("In_PlaneField"),
        OOF_Mesh_FieldEquation("Out_of_PlaneField"),
        OOF_Mesh_FieldEquation("ActivateEquation"),
        OOF_Mesh_FieldEquation("DeactivateEquation")
        ]

    extra_set = [
        OOF_Mesh_Extra("Copy_Field_State"),
        OOF_Mesh_Extra("Copy_Equation_State"),
        OOF_Mesh_Extra("Initialize")
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

    profile_bc_set = [
        OOF_Mesh_ProfileBC("NewProfile"),
        OOF_Mesh_ProfileBC("DeleteProfile"),
        OOF_Mesh_ProfileBC("RenameProfile"),
        OOF_Mesh_ProfileBC("CopyProfile"),
        OOF_Mesh_ProfileBC("EditProfile"),
        OOF_Mesh_ProfileBC("NewBC"),
        OOF_Mesh_ProfileBC("DeleteBC"),
        OOF_Mesh_ProfileBC("RenameBC"),
        OOF_Mesh_ProfileBC("CopyBC"),
        OOF_Mesh_ProfileBC("Copy_AllBC"),
        OOF_Mesh_ProfileBC("EditBC")
        ]

    file_set = [
        OOF_Mesh_SaveLoad("ProfileSave"),
        OOF_Mesh_SaveLoad("ProfileLoad"),
        OOF_Mesh_SaveLoad("Save"),
        OOF_Mesh_SaveLoad("Load")
        ]

    bc_extra_set = [
        OOF_Mesh_BC_Extra("NeumannBCNewEdit")
        ]

    special_set = [
        OOF_Mesh_Special("Skeleton_Delete"),
        OOF_Mesh_Special("Skel_Mod_Mesh_Delete"),
        OOF_Mesh_Special("AbaqusFormat")
        ]
    
    test_set = basic_set + field_equation_set + extra_set + \
               crosssection_set + profile_bc_set + file_set + bc_extra_set + \
               special_set
##     test_set = file_set


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
