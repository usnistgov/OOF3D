# -*- python -*-
# $RCSfile: subproblem_test.py,v $
# $Revision: 1.20 $
# $Author: langer $
# $Date: 2008/09/23 19:33:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# Test suite for the menu commands under OOF.Subproblem.

import unittest, os
import memorycheck

# Basic subproblem operations

class OOF_Subproblem(unittest.TestCase):
    def setUp(self):
        global mesh
        global subproblemcontext
        from ooflib.engine import subproblemcontext
        from ooflib.engine.skeletoncontext import skeletonContexts
        from ooflib.engine import mesh
        global femesh, cskeleton, cmicrostructure
        from ooflib.SWIG.engine import cskeleton
        from ooflib.SWIG.engine import femesh
        from ooflib.SWIG.common import cmicrostructure
        OOF.Microstructure.New(name='subptest',
                               width=1.0, height=1.0,
                               width_in_pixels=10, height_in_pixels=10)
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Settings.Hide_Empty_Mesh_Elements(0)
        OOF.LayerEditor.LayerSet.New(window='Graphics_1')
        OOF.LayerEditor.LayerSet.DisplayedObject(
            category='Microstructure',
            object='subptest')
        OOF.LayerEditor.LayerSet.Add_Method(
            method=MicrostructureMaterialDisplay(no_material=Gray(value=0.0),
                                                 no_color=RGBColor(red=0.0,
                                                                   green=0.0,
                                                                   blue=1.0)))
        OOF.LayerEditor.LayerSet.Send(window='Graphics_1')
        OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle(source='subptest',
            points=[Point(0.442218,0.463619), Point(-0.109922,1.04144)],
            shift=0, ctrl=0)
        OOF.PixelGroup.New(name='corner', microstructure='subptest')
        OOF.PixelGroup.AddSelection(microstructure='subptest', group='corner')
        OOF.Material.New(name='salami')
        OOF.Material.Assign(material='salami', microstructure='subptest',
                            pixels='corner')
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='subptest',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))

    def tearDown(self):
        OOF.Material.Delete(name='salami')
        OOF.Graphics_1.File.Close()

    @memorycheck.check('subptest')
    def New(self):
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        # check for default subproblem
        subp = subproblemcontext.subproblems['subptest:skeleton:mesh:default']
        self.assertNotEqual(subp, None)
        self.assertEqual(subproblemcontext.subproblems.nActual(), 1)
        # create a new one
        OOF.Subproblem.New(name='sub',
                           mesh='subptest:skeleton:mesh',
                           subproblem=MaterialSubProblem(material='salami'))
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        subp0 = subproblemcontext.subproblems['subptest:skeleton:mesh:default']
        subp1 = subproblemcontext.subproblems['subptest:skeleton:mesh:sub']
        self.assertNotEqual(subp0, None)
        self.assertNotEqual(subp1, None)
        self.assertEqual(subp0.nelements(), 16)
        self.assertEqual(subp0.nfuncnodes(), 25)
        self.assertEqual(subp0.nnodes(), 25)
        self.assertEqual(subp1.nelements(), 4)
        self.assertEqual(subp1.nnodes(), 9)
        self.assertEqual(subp1.nfuncnodes(), 9)

    @memorycheck.check('subptest')
    def Delete(self):
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        OOF.Subproblem.New(name='sub',
                           mesh='subptest:skeleton:mesh',
                           subproblem=EntireMeshSubProblem())
        OOF.Subproblem.Delete(subproblem='subptest:skeleton:mesh:sub')
        self.assertEqual(subproblemcontext.subproblems.nActual(), 1)
        self.assertRaises(KeyError,
                          subproblemcontext.subproblems.__getitem__,
                          'subptest:skeleton:mesh:sub')
        # Check that default subproblem is still present
        subp = subproblemcontext.subproblems['subptest:skeleton:mesh:default']
        self.assertNotEqual(subp, None)
        # Check that default subproblem can't be deleted.
        self.assertRaises(ooferror.ErrUserError,
                          OOF.Subproblem.Delete,
                          subproblem='subptest:skeleton:mesh:default')
        self.assertEqual(subproblemcontext.subproblems.nActual(), 1)
        subp = subproblemcontext.subproblems['subptest:skeleton:mesh:default']
        self.assertNotEqual(subp, None)

        OOF.Mesh.Delete(mesh='subptest:skeleton:mesh')
        self.assertEqual(subproblemcontext.subproblems.nActual(), 0)

        # Now try it with two non-trivial subproblems.
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        OOF.Subproblem.New(name='sub1',
                           mesh='subptest:skeleton:mesh',
                           subproblem=EntireMeshSubProblem())
        OOF.Subproblem.New(name='sub2',
                           mesh='subptest:skeleton:mesh',
                           subproblem=EntireMeshSubProblem())
        self.assertEqual(subproblemcontext.subproblems.nActual(), 3)
        OOF.Subproblem.Delete(subproblem='subptest:skeleton:mesh:sub1')
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        self.assertRaises(KeyError,
                          subproblemcontext.subproblems.__getitem__,
                          'subptest:skeleton:mesh:sub1')
        subp = subproblemcontext.subproblems['subptest:skeleton:mesh:sub2']
        self.assertNotEqual(subp, None)
        OOF.Subproblem.Delete(subproblem='subptest:skeleton:mesh:sub2')
        self.assertEqual(subproblemcontext.subproblems.nActual(), 1)
        self.assertRaises(KeyError,
                          subproblemcontext.subproblems.__getitem__,
                          'subptest:skeleton:mesh:sub2')

    @memorycheck.check('subptest')
    def Copy(self):
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])

        # Copy to same mesh
        OOF.Subproblem.Copy(subproblem='subptest:skeleton:mesh:default',
                            mesh='subptest:skeleton:mesh', name='facsimile')
        sub = subproblemcontext.subproblems['subptest:skeleton:mesh:default']
        sub2 = subproblemcontext.subproblems['subptest:skeleton:mesh:facsimile']
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        self.assertNotEqual(id(sub), id(sub2))
        self.assertNotEqual(id(sub.getObject()), id(sub2.getObject()))
        # Copy to another mesh
        OOF.Mesh.New(name='mesh2', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        OOF.Subproblem.Copy(subproblem='subptest:skeleton:mesh:default',
                            mesh='subptest:skeleton:mesh2', name='facsimile')
        self.assertEqual(subproblemcontext.subproblems.nActual(), 4)
        sub3 = subproblemcontext.subproblems[
            'subptest:skeleton:mesh2:facsimile']
        self.assertNotEqual(sub3, None)
        self.assertNotEqual(id(sub), id(sub3))
        self.assertNotEqual(id(sub2), id(sub3))
        self.assertNotEqual(id(sub.getObject()), id(sub3.getObject()))
        self.assertNotEqual(id(sub2.getObject()), id(sub3.getObject()))

    @memorycheck.check('subptest')
    def Rename(self):
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        subp = subproblemcontext.subproblems['subptest:skeleton:mesh:default']
        self.assertRaises(ooferror.ErrUserError,
                          OOF.Subproblem.Rename,
                          subproblem='subptest:skeleton:mesh:default',
                          name='grinder')
        OOF.Subproblem.New(name='sub1',
                           mesh='subptest:skeleton:mesh',
                           subproblem=EntireMeshSubProblem())
        subp1 = subproblemcontext.subproblems['subptest:skeleton:mesh:sub1']
        OOF.Subproblem.Rename(subproblem='subptest:skeleton:mesh:sub1',
                              name='grinder')
        subp2 = subproblemcontext.subproblems['subptest:skeleton:mesh:grinder']
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        self.assertEqual(id(subp1), id(subp2))
        self.assertEqual(id(subp1.getObject()), id(subp2.getObject()))

    @memorycheck.check('subptest')
    def Edit(self):
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        self.assertRaises(ooferror.ErrUserError,
                          OOF.Subproblem.Edit,
                          name='subptest:skeleton:mesh:default',
                          subproblem=MaterialSubProblem(material='salami'))
        OOF.Subproblem.New(name='sub1',
                           mesh='subptest:skeleton:mesh',
                           subproblem=EntireMeshSubProblem())
        OOF.Subproblem.Edit(name='subptest:skeleton:mesh:sub1',
                            subproblem=MaterialSubProblem(material='salami'))
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        subp = subproblemcontext.subproblems['subptest:skeleton:mesh:sub1']
        self.assertEqual(subp.nelements(), 4)

class OOF_Subproblem_Varieties(unittest.TestCase):
    def setUp(self):
        global mesh
        global subproblemcontext
        from ooflib.engine import subproblemcontext
        from ooflib.engine import mesh
        global femesh, cskeleton, cmicrostructure
        from ooflib.SWIG.engine import cskeleton
        from ooflib.SWIG.engine import femesh
        from ooflib.SWIG.common import cmicrostructure

        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join('ms_data', 'small.ppm'),
            microstructure_name='small.ppm', height=automatic, width=automatic)
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source='small.ppm:small.ppm',
            points=[Point(37.4416,59.9125), Point(81.0992,45.7879)],
            shift=0, ctrl=0)
        OOF.PixelGroup.New(name='spot1', microstructure='small.ppm')
        OOF.PixelGroup.AddSelection(microstructure='small.ppm', group='spot1')
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source='small.ppm:small.ppm',
            points=[Point(84.3093,56.7023), Point(125.399,41.2938)],
            shift=0, ctrl=0)
        OOF.PixelGroup.New(name='spot2', microstructure='small.ppm')
        OOF.PixelGroup.AddSelection(microstructure='small.ppm', group='spot2')
        OOF.Graphics_1.File.Close()
        OOF.Skeleton.New(
            name='skeleton', microstructure='small.ppm',
            x_elements=20, y_elements=20,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))
        OOF.Mesh.New(name='mesh', skeleton='small.ppm:skeleton',
                     element_types=['T3_3', 'Q4_4'])
    def get_subproblem(self, name):
        return subproblemcontext.subproblems['small.ppm:skeleton:mesh:'+name]

    @memorycheck.check('small.ppm')
    def Material(self):
        OOF.Material.New(name='material')
        OOF.Material.Assign(material='material', microstructure='small.ppm',
                            pixels='spot1')
        OOF.Subproblem.New(name='matspot1', mesh='small.ppm:skeleton:mesh',
                           subproblem=MaterialSubProblem(material='material'))
        self.assert_(self.get_subproblem('matspot1').nelements() == 114)
        self.assert_(self.get_subproblem('matspot1').nnodes() == 138)
        OOF.Material.Assign(material='material', microstructure='small.ppm',
                            pixels='spot2')
        self.assert_(self.get_subproblem('matspot1').nelements() == 178)
        self.assert_(self.get_subproblem('matspot1').nnodes() == 208)

    @memorycheck.check('small.ppm')
    def PixelGroup(self):
        OOF.Subproblem.New(name='spot1', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        self.assert_(self.get_subproblem('spot1').nelements() == 114)

    @memorycheck.check('small.ppm')
    def Union(self):
        OOF.Subproblem.New(name='spot1', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        OOF.Subproblem.New(name='spot2', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot2'))
        OOF.Subproblem.New(
            name='union', mesh='small.ppm:skeleton:mesh',
            subproblem=UnionSubProblem(one='small.ppm:skeleton:mesh:spot1',
                                       another='small.ppm:skeleton:mesh:spot2'))
        self.assert_(self.get_subproblem('union').nelements() == 178)
        # Check that modifying a pixelgroup changes both the
        # pixelgroup subproblem and the union subproblem.
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle(
            source='small.ppm:small.ppm',
            points=[Point(7.26654,117.695), Point(37.4416,8.55058)],
            shift=0, ctrl=0)
        OOF.Graphics_1.File.Close()
        OOF.PixelGroup.RemoveSelection(microstructure='small.ppm',
                                       group='spot1')
        self.assert_(self.get_subproblem('spot1').nelements() == 68)
        self.assert_(self.get_subproblem('spot1').nnodes() == 97)
        self.assert_(self.get_subproblem('union').nelements() == 132)
        self.assert_(self.get_subproblem('union').nnodes() == 167)
        # Check that dependent subproblems are removed when their
        # dependencies are removed.
        OOF.Subproblem.Delete(subproblem='small.ppm:skeleton:mesh:spot1')
        # Only 'default' and 'spot2' should be left.  'union' should
        # have been deleted.
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        self.assertRaises(KeyError,
                          subproblemcontext.subproblems.__getitem__,
                          'small.ppm:skeleton:mesh:union')
        
    @memorycheck.check('small.ppm')
    def Intersection(self):
        OOF.Subproblem.New(name='spot1', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        OOF.Subproblem.New(name='spot2', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot2'))
        OOF.Subproblem.New(
            name='intersection', mesh='small.ppm:skeleton:mesh',
            subproblem=IntersectionSubProblem(
            one='small.ppm:skeleton:mesh:spot1',
            another='small.ppm:skeleton:mesh:spot2'))
        self.assert_(self.get_subproblem('intersection').nelements() == 42)

    @memorycheck.check('small.ppm')
    def Xor(self):
        OOF.Subproblem.New(name='spot1', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        OOF.Subproblem.New(name='spot2', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot2'))
        OOF.Subproblem.New(
            name='xor', mesh='small.ppm:skeleton:mesh',
            subproblem=XorSubProblem(
            one='small.ppm:skeleton:mesh:spot1',
            another='small.ppm:skeleton:mesh:spot2'))
        self.assert_(self.get_subproblem('xor').nelements() == 136)

    @memorycheck.check('small.ppm')
    def Complement(self):
        OOF.Subproblem.New(name='spot1', mesh='small.ppm:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        OOF.Subproblem.New(
            name='comp', mesh='small.ppm:skeleton:mesh',
            subproblem=ComplementSubProblem(
            complement_of='small.ppm:skeleton:mesh:spot1'))
        self.assert_(self.get_subproblem('comp').nelements() == 286)
        self.assert_(self.get_subproblem('comp').nnodes() == 342)
        # Check that adding more pixels to the pixel group changes the
        # complement subproblem.
        OOF.PixelSelection.Select_Group(microstructure='small.ppm',
                                        group='spot2')
        OOF.PixelGroup.AddSelection(microstructure='small.ppm', group='spot1')
        self.assert_(self.get_subproblem('comp').nelements() == 222)
        self.assert_(self.get_subproblem('comp').nnodes() == 284)
        
        # Check that dependent subproblems are removed when their
        # dependencies are removed.
        OOF.Subproblem.Delete(subproblem='small.ppm:skeleton:mesh:spot1')
        # Only 'default' and should be left.  'comp' should have been
        # deleted.
        self.assertEqual(subproblemcontext.subproblems.nActual(), 1)
        self.assertRaises(KeyError,
                          subproblemcontext.subproblems.__getitem__,
                          'small.ppm:skeleton:mesh:comp')
        
    @memorycheck.check('small.ppm')
    def Entire(self):
        OOF.Subproblem.New(name='entire', mesh='small.ppm:skeleton:mesh',
                           subproblem=EntireMeshSubProblem())
        self.assert_(self.get_subproblem("entire").nelements() == 400)

class OOF_Subproblem_FieldEquation(OOF_Subproblem):
    def setUp(self):
        OOF_Subproblem.setUp(self)
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        OOF.Subproblem.New(name='sub',
                           mesh='subptest:skeleton:mesh',
                           subproblem=MaterialSubProblem(material='salami'))
        # These references to subproblems will break the memory leak
        # tests, so the individual tests in this class have to
        # explicitly delete the references.
        self.subp0 = subproblemcontext.subproblems[
            'subptest:skeleton:mesh:default'].getObject()
        self.subp1 = subproblemcontext.subproblems[
            'subptest:skeleton:mesh:sub'].getObject()
 
    @memorycheck.check('subptest')
    def DefineField(self):
        self.assert_(not Temperature.is_defined(self.subp0) and
                     not Temperature.is_defined(self.subp1))
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:sub',
                                    field=Temperature)
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:default',
                                    field=Displacement)
        self.assert_(Temperature.is_defined(self.subp1) and
                     not Temperature.is_defined(self.subp0))
        self.assert_(Displacement.is_defined(self.subp0) and
                     not Displacement.is_defined(self.subp1))
        del self.subp0
        del self.subp1

    @memorycheck.check('subptest')
    def UndefineField(self):
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:sub',
                                    field=Temperature)
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:default',
                                    field=Displacement)
        OOF.Subproblem.Field.Undefine(
            subproblem='subptest:skeleton:mesh:sub', field=Temperature)
        self.assert_(not Temperature.is_defined(self.subp1))
        self.assert_(Displacement.is_defined(self.subp0))
        OOF.Subproblem.Field.Undefine(
            subproblem='subptest:skeleton:mesh:default', field=Displacement)
        self.assert_(not Displacement.is_defined(self.subp0))
        del self.subp0
        del self.subp1

    @memorycheck.check('subptest')
    def ActivateField(self):
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:sub',
                                    field=Temperature)
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:default',
                                    field=Displacement)
        self.assert_(not Temperature.is_active(self.subp0))
        self.assert_(not Displacement.is_active(self.subp0))
        self.assert_(not Temperature.is_active(self.subp1))
        self.assert_(not Displacement.is_active(self.subp1))
        OOF.Subproblem.Field.Activate(subproblem='subptest:skeleton:mesh:sub',
                                      field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='subptest:skeleton:mesh:default', field=Displacement)
        self.assert_(not Temperature.is_active(self.subp0))
        self.assert_(Displacement.is_active(self.subp0))
        self.assert_(Temperature.is_active(self.subp1))
        self.assert_(not Displacement.is_active(self.subp1))
        OOF.Subproblem.Field.Deactivate(subproblem='subptest:skeleton:mesh:sub',
                                      field=Temperature)
        OOF.Subproblem.Field.Deactivate(
            subproblem='subptest:skeleton:mesh:default', field=Displacement)
        self.assert_(not Temperature.is_active(self.subp0))
        self.assert_(not Displacement.is_active(self.subp0))
        self.assert_(not Temperature.is_active(self.subp1))
        self.assert_(not Displacement.is_active(self.subp1))
        del self.subp0
        del self.subp1

    @memorycheck.check('subptest')
    def In_PlaneField(self):
        # This is already tested in mesh_test.py, but not for Fields
        # defined on non-trivial Subproblems.
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:sub',
                                    field=Temperature)
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:default',
                                    field=Displacement)
        fmsh = mesh.meshes['subptest:skeleton:mesh'].getObject()
        self.assert_(not fmsh.in_plane(Temperature))
        self.assert_(not fmsh.in_plane(Displacement))
        OOF.Mesh.Field.In_Plane(mesh="subptest:skeleton:mesh",
                                     field=Displacement)
        OOF.Mesh.Field.In_Plane(mesh="subptest:skeleton:mesh",
                                     field=Temperature)
        self.assert_(fmsh.in_plane(Temperature))
        self.assert_(fmsh.in_plane(Displacement))
        OOF.Mesh.Field.Out_of_Plane(mesh="subptest:skeleton:mesh",
                                     field=Displacement)
        OOF.Mesh.Field.Out_of_Plane(mesh="subptest:skeleton:mesh",
                                     field=Temperature)
        self.assert_(not fmsh.in_plane(Temperature))
        self.assert_(not fmsh.in_plane(Displacement))
        del self.subp0
        del self.subp1

    @memorycheck.check('subptest')
    def ActivateEquation(self):
        self.assert_(not self.subp0.is_active_equation(Heat_Eqn))
        self.assert_(not self.subp1.is_active_equation(Heat_Eqn))
        OOF.Subproblem.Equation.Activate(
            subproblem="subptest:skeleton:mesh:sub", equation=Heat_Eqn)
        self.assert_(self.subp1.is_active_equation(Heat_Eqn))
        self.assert_(not self.subp0.is_active_equation(Heat_Eqn))
        OOF.Subproblem.Equation.Deactivate(
            subproblem="subptest:skeleton:mesh:sub", equation=Heat_Eqn)
        self.assert_(not self.subp0.is_active_equation(Heat_Eqn))
        self.assert_(not self.subp1.is_active_equation(Heat_Eqn))
        del self.subp0
        del self.subp1

class OOF_Subproblem_Extra(OOF_Subproblem_FieldEquation):
    @memorycheck.check('subptest')
    def Copy_Field_State(self):
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:sub',
                                    field=Temperature)
        OOF.Subproblem.Field.Activate(subproblem='subptest:skeleton:mesh:sub',
                                      field=Temperature)
        OOF.Subproblem.Field.Define(subproblem='subptest:skeleton:mesh:sub',
                                    field=Displacement)
        # copy to a new subproblem in the same mesh
        OOF.Subproblem.New(name='nautilus', mesh='subptest:skeleton:mesh',
                           subproblem=MaterialSubProblem(material='salami'))
        subp = subproblemcontext.subproblems[
            'subptest:skeleton:mesh:nautilus'].getObject()
        self.assert_(not Temperature.is_defined(subp))
        self.assert_(not Temperature.is_active(subp))
        self.assert_(not Displacement.is_defined(subp))
        OOF.Subproblem.Copy_Field_State(
            source="subptest:skeleton:mesh:sub",
            target="subptest:skeleton:mesh:nautilus")
        self.assert_(Temperature.is_defined(subp))
        self.assert_(Temperature.is_active(subp))
        self.assert_(Displacement.is_defined(subp))
        # copy to a new subproblem in a different mesh
        OOF.Mesh.New(name="mush", skeleton="subptest:skeleton",
                     element_types=['T3_3', 'Q4_4'])
        subp = subproblemcontext.subproblems[
            'subptest:skeleton:mush:default'].getObject()
        OOF.Subproblem.Copy_Field_State(
            source="subptest:skeleton:mesh:sub",
            target="subptest:skeleton:mush:default")
        self.assert_(Temperature.is_defined(subp))
        self.assert_(Temperature.is_active(subp))
        self.assert_(Displacement.is_defined(subp))
        OOF.Mesh.Delete(mesh='subptest:skeleton:mush')
        del self.subp0
        del self.subp1

    @memorycheck.check('subptest')
    def Copy_Equation_State(self):
        OOF.Subproblem.Equation.Activate(
            subproblem="subptest:skeleton:mesh:sub", equation=Heat_Eqn)
        # copy to a new subproblem in the same mesh
        OOF.Subproblem.New(name='nautilus', mesh='subptest:skeleton:mesh',
                           subproblem=MaterialSubProblem(material='salami'))
        subp = subproblemcontext.subproblems[
            'subptest:skeleton:mesh:nautilus'].getObject()
        self.assert_(not subp.is_active_equation(Heat_Eqn))
        OOF.Subproblem.Copy_Equation_State(
            source="subptest:skeleton:mesh:sub",
            target="subptest:skeleton:mesh:nautilus")
        self.assert_(subp.is_active_equation(Heat_Eqn))
        self.assert_(not subp.is_active_equation(Force_Balance))
        # copy to a new subproblem in a different mesh
        OOF.Mesh.New(name="mush", skeleton="subptest:skeleton",
                     element_types=['T3_3', 'Q4_4'])
        subp = subproblemcontext.subproblems[
            'subptest:skeleton:mush:default'].getObject()
        OOF.Subproblem.Copy_Equation_State(
            source="subptest:skeleton:mesh:sub",
            target="subptest:skeleton:mush:default")
        self.assert_(subp.is_active_equation(Heat_Eqn))
        self.assert_(not subp.is_active_equation(Force_Balance))
        del self.subp0
        del self.subp1

class OOF_Material_Symmetry(unittest.TestCase):
    def setUp(self):
        global subproblemcontext
        global materialmanager
        global symstate
        from ooflib.engine import subproblemcontext
        from ooflib.engine import materialmanager
        from ooflib.engine import symstate
        # Build a trivial mesh, but with all the fields and "direct"
        # properties (i.e. no couplings.)
        OOF.Microstructure.New(name='microstructure',
                               width=1.0, height=1.0,
                               width_in_pixels=10, height_in_pixels=10)
        OOF.Material.New(name='material')
        OOF.Material.Add_property(name='material',
                                  property='Mechanical:Elasticity:Isotropic')
        OOF.Material.Add_property(name='material',
                                  property='Thermal:Conductivity:Isotropic')
        OOF.Material.Add_property(name='material',
                                  property='Electric:DielectricPermittivity:Isotropic')
        OOF.Material.Assign(material='material',
                            microstructure='microstructure', pixels=all)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='microstructure',
            x_elements=4, y_elements=4,
            skeleton_geometry=QuadSkeleton(
            left_right_periodicity=False,top_bottom_periodicity=False))
        OOF.Mesh.New(name='mesh',
                     skeleton='microstructure:skeleton',
                     element_types=['T3_3', 'Q4_4'])
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            field=Temperature)
        OOF.Subproblem.Field.Define(
            subproblem='microstructure:skeleton:mesh:default',
            field=Displacement)
        OOF.Subproblem.Field.Activate(
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
            equation=Heat_Eqn)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Plane_Heat_Flux)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Force_Balance)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Plane_Stress)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Coulomb_Eqn)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=InPlanePolarization)
        
    def tearDown(self):
        OOF.Material.Delete(name="material")

    @memorycheck.check('microstructure')
    def Basic(self):
        # Retrieve the material and the subproblem, then make the
        # call.
        subp = subproblemcontext.subproblems[
            'microstructure:skeleton:mesh:default']
        subpObj = subp.getObject()
        mat = materialmanager.getMaterial('material')
        self.assert_(mat.symmetric(subpObj))
        self.assertEqual(subp.get_symmetry_state(),
                         symstate.SYMMETRIC)

    @memorycheck.check('microstructure')
    def ThermalExpansion(self):
        OOF.Material.Add_property(
            name='material', property='Couplings:ThermalExpansion:Isotropic')
        subp = subproblemcontext.subproblems[
            'microstructure:skeleton:mesh:default']
        subpObj = subp.getObject()
        mat = materialmanager.getMaterial('material')
        # Thermal expansion makes the problem unsymmetric.
        self.assert_(not mat.symmetric(subpObj))
        self.assertEqual(subp.get_symmetry_state(),
                         symstate.UNSYMMETRIC)

    @memorycheck.check('microstructure')
    def PiezoElectricity(self):
        OOF.Material.Add_property(
            name='material',
            property='Couplings:PiezoElectricity:Cubic:Td')
        subp = subproblemcontext.subproblems[
            'microstructure:skeleton:mesh:default']
        subpObj = subp.getObject()
        mat = materialmanager.getMaterial('material')
        # Piezoelectricity does *not* destroy the symmetry.
        self.assert_(mat.symmetric(subpObj))
        self.assertEqual(subp.get_symmetry_state(),
                         symstate.SYMMETRIC)

    @memorycheck.check('microstructure')
    def PyroElectricity(self):
        OOF.Material.Add_property(
            name='material', property='Couplings:PyroElectricity')
        subp = subproblemcontext.subproblems[
            'microstructure:skeleton:mesh:default']
        subpObj = subp.getObject()
        mat = materialmanager.getMaterial('material')
        # Pyroelectricity makes the problem unsymmetric.
        self.assert_(not mat.symmetric(subpObj))
        self.assertEqual(subp.get_symmetry_state(),
                         symstate.UNSYMMETRIC)
    
# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.

def run_tests():
    basic_set = [
        OOF_Subproblem("New"),
        OOF_Subproblem("Delete"),
        OOF_Subproblem("Copy"),
        OOF_Subproblem("Rename"),
        OOF_Subproblem("Edit")
        ]

    variety_set = [
        OOF_Subproblem_Varieties("Material"),
        OOF_Subproblem_Varieties("PixelGroup"),
        OOF_Subproblem_Varieties("Union"),
        OOF_Subproblem_Varieties("Intersection"),
        OOF_Subproblem_Varieties("Xor"),
        OOF_Subproblem_Varieties("Complement"),
        OOF_Subproblem_Varieties("Entire")
        ]

    field_equation_set = [
        OOF_Subproblem_FieldEquation("DefineField"),
        OOF_Subproblem_FieldEquation("UndefineField"),
        OOF_Subproblem_FieldEquation("ActivateField"),
        OOF_Subproblem_FieldEquation("In_PlaneField"),
        OOF_Subproblem_FieldEquation("ActivateEquation")
        ]

    extra_set = [
        OOF_Subproblem_Extra("Copy_Field_State"),
        OOF_Subproblem_Extra("Copy_Equation_State")
        ]

    symmetry_set = [
        OOF_Material_Symmetry("Basic"),
        OOF_Material_Symmetry("ThermalExpansion"),
        OOF_Material_Symmetry("PiezoElectricity"),
        OOF_Material_Symmetry("PyroElectricity")
        ]
    
    test_set = basic_set + variety_set + field_equation_set + \
               extra_set + symmetry_set
    
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
