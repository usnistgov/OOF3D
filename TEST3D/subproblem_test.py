# -*- python -*-
# $RCSfile: subproblem_test.py,v $
# $Revision: 1.1.2.11 $
# $Author: langer $
# $Date: 2014/09/19 03:28:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test suite for the menu commands under OOF.Subproblem.

import unittest, os, sys
import memorycheck
from UTILS.file_utils import reference_file

# Basic subproblem operations

class OOF_Subproblem(unittest.TestCase):
    def setUp(self):
        global mesh
        global subproblemcontext
        from ooflib.engine import subproblemcontext
        from ooflib.engine.skeletoncontext import skeletonContexts
        from ooflib.engine import mesh
        OOF.Microstructure.New(
            name='subptest',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Windows.Graphics.New()
        OOF.Graphics_1.Layer.New(
            category='Microstructure',
            what='subptest',
            how=MicrostructureMaterialDisplay(
                no_material=Gray(value=0.0),
                no_color=RGBColor(red=0.00000,green=0.00000,blue=1.00000),
                filter=AllVoxels()))

        OOF.PixelSelection.Region(
            microstructure='subptest', 
            shape=BoxSelectionShape(point0=Point(0,0,0),
                                    point1=Point(0.4,0.4,1)),
            units=PhysicalUnits(),
            operator=Select())

        OOF.PixelGroup.New(name='corner', microstructure='subptest')
        OOF.PixelGroup.AddSelection(microstructure='subptest', group='corner')
        OOF.Material.New(name='salami', material_type='bulk')
        OOF.Material.Assign(material='salami', microstructure='subptest',
                            pixels='corner')
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='subptest',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))

    def tearDown(self):
        OOF.Material.Delete(name='salami')
        OOF.Graphics_1.File.Close()

    @memorycheck.check('subptest')
    def New(self):
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
        self.assertEqual(subp0.nelements(), 320)
        self.assertEqual(subp0.nfuncnodes(), 125)
        self.assertEqual(subp0.nnodes(), 125)
        self.assertEqual(subp1.nelements(), 48)
        self.assertEqual(subp1.nnodes(), 30)
        self.assertEqual(subp1.nfuncnodes(), 30)
        

    @memorycheck.check('subptest')
    def Delete(self):
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])

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
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
        self.assertEqual(subp.nelements(), 48)

class OOF_Subproblem_Varieties(unittest.TestCase):
    def setUp(self):
        global mesh
        global subproblemcontext
        from ooflib.engine import subproblemcontext
        from ooflib.engine import mesh

        OOF.Microstructure.New(
            name='subptest',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=15, height_in_pixels=15, depth_in_pixels=15)
        OOF.PixelSelection.Region(
            microstructure='subptest',
            shape=CircleSelectionShape(
                center=Point(0.25, 0.25, 0.75),
                radius=0.2),
            units=PhysicalUnits(),
            operator=Select())
        OOF.PixelGroup.New(name='spot1', microstructure='subptest')
        OOF.PixelGroup.AddSelection(microstructure='subptest', group='spot1')

        OOF.PixelSelection.Clear(microstructure='subptest')
        OOF.PixelSelection.Region(
            microstructure='subptest',
            shape=CircleSelectionShape(
                center=Point(0.75, 0.75, 0.25),
                radius=0.2),
            units=PhysicalUnits(),
            operator=Select())
        OOF.PixelGroup.New(name='spot2', microstructure='subptest')
        OOF.PixelGroup.AddSelection(microstructure='subptest', group='spot2')

        OOF.PixelSelection.Clear(microstructure='subptest')
        OOF.PixelSelection.Region(
            microstructure='subptest', 
            shape=BoxSelectionShape(point0=Point(0,0,0),
                                    point1=Point(0.25,0.25,1)),
            units=PhysicalUnits(),
            operator=SelectOnly())
        OOF.PixelGroup.New(
            name='box', microstructure='subptest')
        OOF.PixelGroup.AddSelection(
            microstructure='subptest', group='box')

        OOF.Skeleton.New(
            name='skeleton', 
            microstructure='subptest',
            x_elements=15, y_elements=15, z_elements=15,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])

    def get_subproblem(self, name):
        return subproblemcontext.subproblems['subptest:skeleton:mesh:'+name]

    @memorycheck.check('subptest')
    def Material(self):
        OOF.Material.New(name='material')
        OOF.Material.Assign(material='material', microstructure='subptest',
                            pixels='spot1')
        OOF.Subproblem.New(name='matspot1', mesh='subptest:skeleton:mesh',
                           subproblem=MaterialSubProblem(material='material'))
        self.assertEqual(self.get_subproblem('matspot1').nelements(), 570)
        self.assertEqual(self.get_subproblem('matspot1').nnodes(), 217)
        OOF.Material.Assign(material='material', microstructure='subptest',
                            pixels='spot2')
        self.assertEqual(self.get_subproblem('matspot1').nelements(), 1140)
        self.assertEqual(self.get_subproblem('matspot1').nnodes(), 434)
        OOF.Material.Delete(name="material")

    @memorycheck.check('subptest')
    def PixelGroup(self):
        OOF.Subproblem.New(
            name='spot1', 
            mesh='subptest:skeleton:mesh',
            subproblem=PixelGroupSubProblem(group='spot1'))
        self.assertEqual(self.get_subproblem('spot1').nelements(), 570)
        ## TODO 3.1: Delete the PixelGroup and check that the subproblem
        ## is deleted (not yet implemented).

    @memorycheck.check('subptest')
    def Union(self):
        OOF.Subproblem.New(name='spot1', mesh='subptest:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        OOF.Subproblem.New(name='spot2', mesh='subptest:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot2'))
        OOF.Subproblem.New(
            name='union', mesh='subptest:skeleton:mesh',
            subproblem=UnionSubProblem(one='subptest:skeleton:mesh:spot1',
                                       another='subptest:skeleton:mesh:spot2'))
        self.assertEqual(self.get_subproblem('union').nelements(), 1140)

        # Check that modifying a pixelgroup changes both the
        # pixelgroup subproblem and the union subproblem.
        OOF.PixelSelection.Region(
            microstructure='subptest',
            shape=BoxSelectionShape(point0=Point(0,0,0),
                                    point1=Point(0.1,0.1,0.1)),
            units=PhysicalUnits(),
            operator=SelectOnly())
        OOF.PixelGroup.AddSelection(
            microstructure='subptest', group='spot1')
        self.assertEqual(self.get_subproblem('spot1').nelements(), 610)
        self.assertEqual(self.get_subproblem('union').nelements(), 1180)

        # Check that dependent subproblems are removed when their
        # dependencies are removed.
        OOF.Subproblem.Delete(subproblem='subptest:skeleton:mesh:spot1')
        # Only 'default' and 'spot2' should be left.  'union' should
        # have been deleted.
        self.assertEqual(subproblemcontext.subproblems.nActual(), 2)
        self.assertRaises(KeyError,
                          subproblemcontext.subproblems.__getitem__,
                          'subptest:skeleton:mesh:union')
        
    @memorycheck.check('subptest')
    def Intersection(self):
        OOF.Subproblem.New(name='spot1', mesh='subptest:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        # Select a region that intersects roughly a quarter of spot1.
        # spot1 isn't symmetric, so it's not exactly a quarter.
        OOF.Subproblem.New(
            name='box',
            mesh='subptest:skeleton:mesh',
            subproblem=PixelGroupSubProblem(group='box'))
        OOF.Subproblem.New(
            name='intersection', mesh='subptest:skeleton:mesh',
            subproblem=IntersectionSubProblem(
            one='subptest:skeleton:mesh:spot1',
            another='subptest:skeleton:mesh:box'))
        self.assertEqual(self.get_subproblem('intersection').nelements(), 175)

    @memorycheck.check('subptest')
    def Xor(self):
        OOF.Subproblem.New(name='spot1', mesh='subptest:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        OOF.Subproblem.New(name='box', mesh='subptest:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='box'))
        OOF.Subproblem.New(
            name='xor', mesh='subptest:skeleton:mesh',
            subproblem=XorSubProblem(
            one='subptest:skeleton:mesh:spot1',
            another='subptest:skeleton:mesh:box'))
        self.assertEqual(self.get_subproblem('xor').nelements(), 1420)

    @memorycheck.check('subptest')
    def Complement(self):
        OOF.Subproblem.New(name='spot1', mesh='subptest:skeleton:mesh',
                           subproblem=PixelGroupSubProblem(group='spot1'))
        OOF.Subproblem.New(
            name='comp', mesh='subptest:skeleton:mesh',
            subproblem=ComplementSubProblem(
            complement_of='subptest:skeleton:mesh:spot1'))
        self.assertEqual(self.get_subproblem('comp').nelements(), 16305)
        # Check that adding more pixels to the pixel group changes the
        # complement subproblem.
        OOF.PixelSelection.Group(
            microstructure='subptest',
            group='spot2',
            operator=SelectOnly())
        OOF.PixelGroup.AddSelection(
            microstructure='subptest',
            group='spot1')
        self.assertEqual(self.get_subproblem('comp').nelements(), 15735)
        self.assertEqual(self.get_subproblem('comp').nnodes(), 4002)
        
        # Check that dependent subproblems are removed when their
        # dependencies are removed.
        OOF.Subproblem.Delete(subproblem='subptest:skeleton:mesh:spot1')
        # Only 'default' and should be left.  'comp' should have been
        # deleted.
        self.assertEqual(subproblemcontext.subproblems.nActual(), 1)
        self.assertRaises(KeyError,
                          subproblemcontext.subproblems.__getitem__,
                          'subptest:skeleton:mesh:comp')
        
    @memorycheck.check('subptest')
    def Entire(self):
        OOF.Subproblem.New(name='entire', mesh='subptest:skeleton:mesh',
                           subproblem=EntireMeshSubProblem())
        self.assertEqual(self.get_subproblem("entire").nelements(), 16875)

class OOF_Subproblem_FieldEquation(OOF_Subproblem):
    def setUp(self):
        OOF_Subproblem.setUp(self)
        OOF.Mesh.New(name='mesh', skeleton='subptest:skeleton',
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
                               width=1.0, height=1.0, depth=1.0,
                               width_in_pixels=10, height_in_pixels=10,
                               depth_in_pixels=10)
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
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Mesh.New(name='mesh',
                     skeleton='microstructure:skeleton',
                     element_types=['TET4_4', 'T3_3', 'Q4_4', 'D2_2'])
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
            equation=Force_Balance)
        OOF.Subproblem.Equation.Activate(
            subproblem='microstructure:skeleton:mesh:default',
            equation=Coulomb_Eqn)
        # If there's no solver assigned, properties won't be
        # activated, and symmetry can't be checked.
        OOF.Subproblem.Set_Solver(
            subproblem='microstructure:skeleton:mesh:default',
            solver_mode=AdvancedSolverMode(
                nonlinear_solver=NoNonlinearSolver(),
                time_stepper=StaticDriver(),
                symmetric_solver= ConjugateGradient(
                    preconditioner=ILUPreconditioner(),tolerance=1e-13,
                    max_iterations=1000)))
        
    def tearDown(self):
        OOF.Material.Delete(name="material")

    @memorycheck.check('microstructure')
    def Basic(self):
        OOF.Subproblem.SymmetryTest.K(
            subproblem='microstructure:skeleton:mesh:default',
            material='material',
            symmetric=True)

    @memorycheck.check('microstructure')
    def ThermalExpansion(self):
        OOF.Material.Add_property(
            name='material', property='Couplings:ThermalExpansion:Isotropic')
        # Thermal expansion makes the problem unsymmetric.
        OOF.Subproblem.SymmetryTest.K(
            subproblem='microstructure:skeleton:mesh:default',
            material='material',
            symmetric=False)

    @memorycheck.check('microstructure')
    def PiezoElectricity(self):
        OOF.Material.Add_property(
            name='material',
            property='Couplings:PiezoElectricity:Cubic:Td')
        OOF.Material.Add_property(
            name='material',
            property='Orientation')
        # Piezoelectricity does *not* destroy the symmetry.
        OOF.Subproblem.SymmetryTest.K(
            subproblem='microstructure:skeleton:mesh:default',
            material='material',
            symmetric=True)

    @memorycheck.check('microstructure')
    def PyroElectricity(self):
        OOF.Material.Add_property(
            name='material', property='Couplings:PyroElectricity')
        # Pyroelectricity makes the problem unsymmetric.
        OOF.Subproblem.SymmetryTest.K(
            subproblem='microstructure:skeleton:mesh:default',
            material='material',
            symmetric=False)
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

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

test_set = (basic_set + variety_set + field_equation_set + 
           extra_set + symmetry_set)
    
#test_set = [OOF_Subproblem_Varieties("Complement")]
