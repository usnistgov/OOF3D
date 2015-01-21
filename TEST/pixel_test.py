# -*- python -*-
# $RCSfile: pixel_test.py,v $
# $Revision: 1.22 $
# $Author: langer $
# $Date: 2008/09/07 02:19:48 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# File for testing pixel grouping and selection operations on
# microstructures.  This includes re-running the Microstructure
# save/load and copy operations to ensure that they save/load/copy the
# pixel groups correctly.

# Need to be able to open a graphics window and make selections,
# also, of course.


import unittest, os
import memorycheck

# Prerequisite for making toolbox selections is the existence of a
# graphics window.  These tests just open and close a graphics window.
class Graphics_Ops(unittest.TestCase):
    def setUp(self):
        global gfxmanager
        from ooflib.common.IO import gfxmanager

    # Opens a new graphics window, assuming that none are open (so
    # that the name will be "Graphics_1").
    @memorycheck.check()
    def New(self):
        self.assertRaises(AttributeError,
                          OOF.Windows.__getattr__,
                          attr="Graphics_1")
        OOF.Windows.Graphics.New()
        self.assert_(hasattr(OOF.Windows.Graphics, "Graphics_1"))
        self.assert_(hasattr(OOF, "Graphics_1"))
        self.assertEqual(len(gfxmanager.gfxManager.windows), 1)

    # "Close" Assumes that a graphics window is open.  The "Close"
    # item is actually in OOF.Graphics_n, not in OOF.Windows.Graphics.
    @memorycheck.check()
    def Close(self):
        # Find the graphics window.
        self.assert_(len(OOF.Windows.Graphics.items)==2)
        for item in OOF.Windows.Graphics.items:
            if item.name[:8]=="Graphics":
                item_name=item.name
                break
        self.assert_(item_name is not None)
        # Get the corresponding item from the OOF menu.
        gw_item = OOF.__getattr__(item_name)
        gw_item.File.Close()
        self.assert_(len(OOF.Windows.Graphics.items)==1)
        self.assert_(not hasattr(OOF.Windows.Graphics, item_name))

    def tearDown(self):
        pass

# Tests of actual pixel selection operations.
# OOF.Toolbox.Pixel_Select items:
#   Point, Brush, Rectangle, Circle, Ellipse, Color, Burn.
# Selection modifiers from the same menu, Clear, Undo, Redo, Invert
class Direct_Pixel_Selection(unittest.TestCase):
    def setUp(self):
        global gfxmanager
        global pixelselection
        from ooflib.common.IO import gfxmanager
        from ooflib.common import pixelselection
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("image_data","image_test.ppm"),
            microstructure_name=automatic,
            height=automatic, width=automatic)
        OOF.Windows.Graphics.New()

    # Direct selection operations -- these are toolbox ops in the
    # graphics window.
    # Select circle, rectangle, ellipse, point.
    @memorycheck.check("image_test.ppm")
    def Circle(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="image_test.ppm:image_test.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0, ctrl=0)
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        # Size should be 2000 pixels.
        self.assertEqual(ps.getObject().len(), 2000)

    # Makes and clears a selection.  Uses the circle selector, so
    # that one should be tested first.
    @memorycheck.check("image_test.ppm")
    def Clear(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="image_test.ppm:image_test.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0, ctrl=0)
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        self.assertNotEqual(ps.getObject().len(), 0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="image_test.ppm:image_test.ppm")
        self.assertEqual(ps.getObject().len(), 0)

    # Remining direct selection methods --
    # Point, Brush, Rectangle, Ellipse, Color, Burn.

    @memorycheck.check("image_test.ppm")
    def Point(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="image_test.ppm:image_test.ppm",
            points=[Point(52.0, 70.0)], shift=0, ctrl=0)
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        # Size should be 1 pixel, of course.
        self.assertEqual(ps.getObject().len(), 1)
        psi = ps.getObject()
        self.assertEqual(psi.members(), [iPoint(52,70)])

    # Brush points were recorded from an actual user session.
    @memorycheck.check("image_test.ppm")
    def Brush(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Brush(
            source='image_test.ppm:image_test.ppm',
            style=CircleBrush(radius=2.0),
            points=[Point(19.12,61.2829), Point(19.642,61.2829),
                    Point(20.1639,61.2829), Point(21.2078,61.2829),
                    Point(21.7298,60.761), Point(22.2518,60.761),
                    Point(22.7737,60.761), Point(23.2957,60.761), 
                    Point(23.8176,60.761), Point(24.3396,60.761), 
                    Point(24.8616,60.761), Point(25.3835,60.761), 
                    Point(25.9055,60.761), Point(26.4275,60.761), 
                    Point(26.9494,60.761), Point(27.4714,60.761), 
                    Point(27.9933,60.761), Point(28.5153,60.761), 
                    Point(29.0373,60.761), Point(29.0373,60.239), 
                    Point(29.5592,60.239), Point(30.0812,60.239), 
                    Point(30.6031,60.239), Point(31.1251,60.239), 
                    Point(31.6471,60.239), Point(32.169,60.239), 
                    Point(32.691,60.239), Point(33.2129,60.239), 
                    Point(33.7349,60.239), Point(34.2569,60.239), 
                    Point(34.7788,60.239), Point(35.3008,60.239), 
                    Point(35.8227,60.239), Point(36.3447,60.239), 
                    Point(36.8667,60.239), Point(37.3886,60.239), 
                    Point(37.9106,60.239), Point(38.4325,60.239), 
                    Point(38.9545,60.239), Point(39.4765,60.239), 
                    Point(39.9984,60.239)], shift=0, ctrl=0)
        ps =  pixelselection.pixelselectionWhoClass['image_test.ppm']
        self.assertEqual(ps.getObject().len(), 94)


    @memorycheck.check("image_test.ppm")
    def Rectangle(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle(
            source='image_test.ppm:image_test.ppm',
            points=[Point(23.3,57.0), Point(123.0,24.75)],
            shift=0, ctrl=0)
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        self.assertEqual(ps.getObject().len(), 3434)
        
    @memorycheck.check("image_test.ppm")
    def Ellipse(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Ellipse(
            source='image_test.ppm:image_test.ppm',
            points=[Point(23.3,57.0), Point(123.0,24.75)],
            shift=0, ctrl=0)
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        self.assertEqual(ps.getObject().len(), 2526)

    @memorycheck.check("image_test.ppm")
    def Color(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='image_test.ppm:image_test.ppm',
            range=DeltaRGB(delta_red=0.3, delta_green=0.3, delta_blue=0.3),
            points=[Point(14.7,62.1)], shift=0, ctrl=0)
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        self.assertEqual(ps.getObject().len(), 4204)

    @memorycheck.check("image_test.ppm")
    def Burn(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Burn(
            source='image_test.ppm:image_test.ppm',
            local_flammability=0.1,global_flammability=0.2,
            color_space_norm="L1", next_nearest=False,
            points=[Point(14.7,62.1)], shift=0, ctrl=0)
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        self.assertEqual(ps.getObject().len(), 4195)


    # Then, mechanical ones -- Undo, Redo, Invert.

    @memorycheck.check("image_test.ppm")
    def Undo(self):
        ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
        self.assertEqual(ps.getObject().len(), 0)
        self.assert_(not ps.undoable())
        ps_0_id = id(ps.getObject())
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="image_test.ppm:image_test.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0, ctrl=0)
        self.assert_(ps.undoable())
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        OOF.Graphics_1.Toolbox.Pixel_Select.Undo(
            source="image_test.ppm:image_test.ppm")
        ps_2_id = id(ps.getObject())
        self.assertEqual(ps_0_id, ps_2_id)
        self.assertEqual(ps.getObject().len(), 0)

    @memorycheck.check("image_test.ppm")
    def Redo(self):
         ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
         ps_0_id = id(ps.getObject())
         OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
             source="image_test.ppm:image_test.ppm",
             points=[Point(66.2,55.0), Point(87.6,41.8)],
             shift=0, ctrl=0)
         ps_1_id = id(ps.getObject())
         OOF.Graphics_1.Toolbox.Pixel_Select.Undo(
             source="image_test.ppm:image_test.ppm")
         self.assert_(ps.redoable())
         OOF.Graphics_1.Toolbox.Pixel_Select.Redo(
             source="image_test.ppm:image_test.ppm")
         self.assertEqual(id(ps.getObject()), ps_1_id)
         self.assert_(not ps.redoable())

    @memorycheck.check("image_test.ppm")
    def Clear(self):
        ps = pixelselection.pixelselectionWhoClass["image_test.ppm"]
        ps_0_id = id(ps.getObject())
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
             source="image_test.ppm:image_test.ppm",
             points=[Point(66.2,55.0), Point(87.6,41.8)],
             shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="image_test.ppm:image_test.ppm")
        ps_1_id = id(ps.getObject())
        self.assertEqual(ps.getObject().len(), 0)
        self.assertNotEqual(ps_0_id, ps_1_id)

    @memorycheck.check("image_test.ppm")
    def Invert(self):
         OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
             source="image_test.ppm:image_test.ppm",
             points=[Point(66.2,55.0), Point(87.6,41.8)],
             shift=0, ctrl=0)
         ps = pixelselection.pixelselectionWhoClass['image_test.ppm']
         OOF.Graphics_1.Toolbox.Pixel_Select.Invert(
             source="image_test.ppm:image_test.ppm")
         # Magic number is total minus circle-selected number.
         self.assertEqual(ps.getObject().len(), 16166)
         

         
    def tearDown(self):
        OOF.Graphics_1.File.Close()
        

# Then pixel group creation/manipulation options.

# OOF.PixelGroup:
# New Rename Copy Delete Meshable AddSelection RemoveSelection Clear
# Query

# Pixel group creation/manipulation -- assume that selections are
# possible.  Also should test the autogroup from the image menu.
# These tests use the "small.ppm" image, which autogroups reasonably
# cleanly, rather than the more difficult image_test.ppm.
class Pixel_Groups(unittest.TestCase):
    def setUp(self):
        global microstructure
        global gfxmanager
        global pixelselection
        from ooflib.common import microstructure
        from ooflib.common.IO import gfxmanager
        from ooflib.common import pixelselection
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name=automatic,
            height=automatic, width=automatic)
        OOF.Windows.Graphics.New()

    @memorycheck.check("small.ppm")
    def AutoGroup(self):
        from ooflib.common import color
        def colordiff(c1,c2):
            return (c1.red-c2.red)**2 + \
                   (c1.green-c2.green)**2 + \
                   (c1.blue-c2.blue)**2
        # Dictionary of nearest pure colors and sizes of the
        # corresponding groups, which will not have exactly this
        # color, but will be closer to it than to any other color (in
        # colordiff measure).
        expected_sizes = {color.magenta : 2404,
                          color.RGBColor(1.0,1.0,1.0) : 4781,
                          color.RGBColor(0.0,0.0,0.0) : 2585,
                          color.blue : 2947,
                          color.green : 4795,
                          color.cyan : 1001,
                          color.yellow : 3617,
                          color.red : 370 }

        OOF.Image.AutoGroup(image="small.ppm:small.ppm")
        ms = microstructure.getMicrostructure("small.ppm")
        groups = ms.groupNames()
        self.assertEqual(len(groups), 8)
        for name in groups:
            rgb = eval(name)
            key = None
            diff = None
            for c in expected_sizes.keys():
                cdiff = colordiff(rgb,c)
                if (diff is None) or (cdiff < diff):
                    key = c
                    diff = cdiff
            self.assertEqual(len(ms.findGroup(name)), expected_sizes[key])
        
                            
    @memorycheck.check("small.ppm")
    def New(self):
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        ms = microstructure.getMicrostructure("small.ppm")
        groups = ms.groupNames()
        self.assertEqual(len(groups),1)
        self.assert_("test" in groups)

    @memorycheck.check("small.ppm")
    def Delete(self):
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        ms = microstructure.getMicrostructure("small.ppm")
        OOF.PixelGroup.Delete(microstructure="small.ppm", group="test")
        groups = ms.groupNames()
        self.assertEqual(len(groups),0)

    # Uses "circle" selection.  Clear the selection before measuring
    # the size of the group.
    @memorycheck.check("small.ppm")
    def AddSelection(self):
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        ms = microstructure.getMicrostructure("small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelGroup.AddSelection(
            microstructure="small.ppm", group="test")
        ps = pixelselection.pixelselectionWhoClass['small.ppm']
        sel_size = ps.getObject().len()
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="small.ppm:small.ppm")
        group = ms.findGroup("test")
        self.assertEqual(len(group), sel_size)
        
    @memorycheck.check("small.ppm")
    def RemoveSelection(self):
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        ms = microstructure.getMicrostructure("small.ppm")
        ps = pixelselection.pixelselectionWhoClass['small.ppm']
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        sel_large = ps.getObject().len()
        OOF.PixelGroup.AddSelection(
            microstructure="small.ppm", group="test")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(80.0,41.5)],
            shift=0,ctrl=0)
        sel_small = ps.getObject().len()
        OOF.PixelGroup.RemoveSelection(
            microstructure="small.ppm", group="test")
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="small.ppm:small.ppm")
        group = ms.findGroup("test")
        self.assertEqual(len(group), sel_large-sel_small)

    @memorycheck.check("small.ppm")
    def Copy(self):
        ms = microstructure.getMicrostructure("small.ppm")
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelGroup.AddSelection(
            microstructure="small.ppm", group="test")
        group = ms.findGroup("test")
        initial_group_size = len(group)
        OOF.PixelGroup.Copy(microstructure="small.ppm",
                            group="test", name="testcopy")
        OOF.PixelGroup.Delete(microstructure="small.ppm", group="test")
        self.assertEqual(ms.nGroups(), 1)
        group = ms.findGroup("testcopy")
        self.assertEqual(len(group), initial_group_size) 
        
    @memorycheck.check("small.ppm")
    def Rename(self):
        ms = microstructure.getMicrostructure("small.ppm")
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelGroup.AddSelection(
            microstructure="small.ppm", group="test")
        group = ms.findGroup("test")
        initial_group_size = len(group)
        OOF.PixelGroup.Rename(microstructure="small.ppm",
                              group="test", new_name="testrename")
        group = ms.findGroup("testrename")
        self.assertEqual(len(group), initial_group_size)
        # Still only one group.
        self.assertEqual(ms.nGroups(), 1)
        self.assert_( not "test" in ms.groupNames())
        

    # Meshable may be better tested at skel-mod time.
    # Query is just weird -- writes to stdout!
    
    def tearDown(self):
        OOF.Graphics_1.File.Close()


# Then pixel selection modifers.
# OOF.PixelSelection:
# Undo Redo Clear Invert Select_Group Add_Group Unselect_Group
# Intersect_Group Despeckle Elkcepsed Expand Shrink Color_Range Copy

## Tests for Select_Element_Pixels and Select_Segment_Pixels are in
## skeleton_extra_test.py, the test for Select_Material is in
## pixel_extra_test.py.

class Selection_Modify(unittest.TestCase):
    def setUp(self):
        global microstructure
        global gfxmanager
        global pixelselection
        from ooflib.common import microstructure
        from ooflib.common.IO import gfxmanager
        from ooflib.common import pixelselection
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name=automatic,
            height=automatic, width=automatic)
        OOF.Windows.Graphics.New()

    # A lot of the obvious checks are already done in the undo test in
    # Direct_Pixel_Selection.
    @memorycheck.check("small.ppm")
    def Undo(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        ps_0_id = id(ps.getObject())
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        ps_1_id = id(ps.getObject())
        OOF.PixelSelection.Undo(microstructure="small.ppm")
        ps_2_id = id(ps.getObject())
        self.assertEqual(ps_2_id, ps_0_id)
        self.assertNotEqual(ps_2_id, ps_1_id)

    @memorycheck.check("small.ppm")
    def Redo(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        ps_0_id = id(ps.getObject())
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        ps_1_id = id(ps.getObject())
        OOF.PixelSelection.Undo(microstructure="small.ppm")
        OOF.PixelSelection.Redo(microstructure="small.ppm")
        ps_2_id = id(ps.getObject())
        self.assert_(not ps.redoable())
        self.assertEqual(ps_2_id, ps_1_id)
        self.assertNotEqual(ps_2_id, ps_0_id)

    @memorycheck.check("small.ppm")
    def Clear(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        ps_0_id = id(ps.getObject())
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelSelection.Clear(microstructure="small.ppm")
        ps_1_id = id(ps.getObject())
        self.assertEqual(ps.getObject().len(), 0)
        self.assertNotEqual(ps_0_id, ps_1_id)

    @memorycheck.check("small.ppm")
    def Invert(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelSelection.Invert(microstructure="small.ppm")
        self.assertEqual(ps.getObject().len(), 20500)

    @memorycheck.check("small.ppm")
    def Copy(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        OOF.Microstructure.Copy(microstructure="small.ppm", name="copy")
        copy_ps = pixelselection.pixelselectionWhoClass["copy"]
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        self.assertEqual(copy_ps.getObject().len(), 0)
        OOF.PixelSelection.Copy(microstructure="copy",
                                source="small.ppm")
        self.assertEqual(copy_ps.getObject().len(),
                         ps.getObject().len())
        OOF.Microstructure.Delete(microstructure="copy")

    @memorycheck.check("small.ppm")
    def Select_Group(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        ps_0_id = id(ps.getObject())
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        OOF.PixelGroup.AddSelection(microstructure="small.ppm", group="test")
        OOF.PixelSelection.Undo(microstructure="small.ppm")
        OOF.PixelSelection.Select_Group(microstructure="small.ppm", group="test")
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(ps.getObject().len(), 2000)

    @memorycheck.check("small.ppm")
    def Add_Group(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        OOF.PixelGroup.AddSelection(microstructure="small.ppm", group="test")
        OOF.PixelSelection.Undo(microstructure="small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(57.0,84.0), Point(67.0, 70.0)],
            shift=0,ctrl=0)
        ps_0_id = id(ps.getObject())
        OOF.PixelSelection.Add_Group(microstructure="small.ppm", group="test")
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(ps.getObject().len(), 2690)
        
    @memorycheck.check("small.ppm")
    def Unselect_Group(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        OOF.PixelGroup.AddSelection(microstructure="small.ppm", group="test")
        OOF.PixelSelection.Undo(microstructure="small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(57.0,84.0), Point(67.0, 70.0)],
            shift=0,ctrl=0)
        ps_0_id = id(ps.getObject())
        OOF.PixelSelection.Unselect_Group(
            microstructure="small.ppm", group="test")
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(ps.getObject().len(), 690)
        
    @memorycheck.check("small.ppm")
    def Intersect_Group(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.PixelGroup.New(name="test", microstructure="small.ppm")
        OOF.PixelGroup.AddSelection(microstructure="small.ppm", group="test")
        OOF.PixelSelection.Undo(microstructure="small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(57.0,84.0), Point(67.0, 70.0)],
            shift=0,ctrl=0)
        ps_0_id = id(ps.getObject())
        OOF.PixelSelection.Intersect_Group(
            microstructure="small.ppm", group="test")
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(ps.getObject().len(), 238)

    # Helper function, to make a selection suitable for use
    # by the Despeckle, Ekcepsed, Expand, and Shrink tests.
    
    def select_helper(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(36.0, 81.0), Point(47.5,72.0)],
            shift=0,ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="small.ppm:small.ppm",
            points=[Point(37.0, 64.5)],
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="small.ppm:small.ppm",
            points=[Point(53.0, 81.0)],
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="small.ppm:small.ppm",
            points=[Point(36.0, 81.0)],
            shift=0, ctrl=1)
            
        
        
    @memorycheck.check("small.ppm")
    def Despeckle(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        self.select_helper()
        self.assertEqual(ps.getObject().len(), 681)
        OOF.PixelSelection.Despeckle(microstructure="small.ppm",
                                     neighbors=8)
        self.assertEqual(ps.getObject().len(), 682)


    @memorycheck.check("small.ppm")
    def Elkcepsed(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        self.select_helper()
        self.assertEqual(ps.getObject().len(), 681)
        OOF.PixelSelection.Elkcepsed(microstructure="small.ppm",
                                     neighbors=3)
        self.assertEqual(ps.getObject().len(), 679)

    @memorycheck.check("small.ppm")
    def Expand(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        self.select_helper()
        self.assertEqual(ps.getObject().len(), 681)
        OOF.PixelSelection.Expand(microstructure="small.ppm",
                                     radius=1.0)
        self.assertEqual(ps.getObject().len(), 773)

    @memorycheck.check("small.ppm")
    def Shrink(self): # You can't disintegrate me!!
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        self.select_helper()
        self.assertEqual(ps.getObject().len(), 681)
        OOF.PixelSelection.Shrink(microstructure="small.ppm",
                                     radius=1.0)
        self.assertEqual(ps.getObject().len(), 595)


    # Color range is a selector, not really a modifer, but there you go.
    @memorycheck.check("small.ppm")
    def Color_Range(self):
        ps = pixelselection.pixelselectionWhoClass["small.ppm"]
        OOF.PixelSelection.Color_Range(
            microstructure="small.ppm", image="small.ppm:small.ppm",
            reference=RGBColor(red=0.0,green=0.0,blue=0.0),
            range=DeltaRGB(delta_red=1.0,delta_green=0.0,delta_blue=1.0))
        self.assertEqual(ps.getObject().len(), 8306)
           


    # Element and segment ops can't be tested until skeletons exist.

    # Rich_MS_Copy is a test of the microstructure copying process now
    # that nontrivial groups and selections can be made -- these
    # should survive the copy process.  The magic numbers come from
    # the autogroup and circle-selection tests, also in this file.
    @memorycheck.check("small.ppm")
    def Rich_MS_Copy(self):
        from ooflib.common import color
        OOF.Image.AutoGroup(image="small.ppm:small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="small.ppm:small.ppm",
            points=[Point(66.0,55.0), Point(87.6,41.8)],
            shift=0,ctrl=0)
        OOF.Microstructure.Copy(microstructure="small.ppm",
                                name="copy")

        # Essentially a re-run of the autogroup test.
        def colordiff(c1,c2):
            return (c1.red-c2.red)**2 + \
                   (c1.green-c2.green)**2 + \
                   (c1.blue-c2.blue)**2
        # Dictionary of nearest pure colors and sizes of the
        # corresponding groups, which will not have exactly this
        # color, but will be closer to it than to any other color (in
        # colordiff measure).
        expected_sizes = {color.magenta : 2404,
                          color.RGBColor(1.0,1.0,1.0) : 4781,
                          color.RGBColor(0.0,0.0,0.0) : 2585,
                          color.blue : 2947,
                          color.green : 4795,
                          color.cyan : 1001,
                          color.yellow : 3617,
                          color.red : 370 }
        ms = microstructure.getMicrostructure("copy")
        groups = ms.groupNames()
        self.assertEqual(len(groups), 8)
        for name in groups:
            rgb = eval(name)
            key = None
            diff = None
            for c in expected_sizes.keys():
                cdiff = colordiff(rgb,c)
                if (diff is None) or (cdiff < diff):
                    key = c
                    diff = cdiff
            self.assertEqual(len(ms.findGroup(name)), expected_sizes[key])
        ps = pixelselection.pixelselectionWhoClass["copy"]
        # Selection should *not* be copied.
        self.assertEqual(ps.getObject().len(), 0)
        OOF.Microstructure.Delete(microstructure="copy")
        

    def tearDown(self):
        OOF.Graphics_1.File.Close()
    

    
# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.
def run_tests():
    test_set = [
        Graphics_Ops("New"),
        Graphics_Ops("Close"),
        Direct_Pixel_Selection("Circle"),
        Direct_Pixel_Selection("Clear"),
        Direct_Pixel_Selection("Point"),
        Direct_Pixel_Selection("Brush"),
        Direct_Pixel_Selection("Rectangle"),
        Direct_Pixel_Selection("Ellipse"),
        Direct_Pixel_Selection("Color"),
        Direct_Pixel_Selection("Burn"),
        Direct_Pixel_Selection("Undo"),
        Direct_Pixel_Selection("Redo"),
        Direct_Pixel_Selection("Clear"),
        Direct_Pixel_Selection("Invert"),
        Pixel_Groups("AutoGroup"),
        Pixel_Groups("New"),
        Pixel_Groups("Delete"),
        Pixel_Groups("AddSelection"),
        Pixel_Groups("RemoveSelection"),
        Pixel_Groups("Copy"),
        Pixel_Groups("Rename"),
        Selection_Modify("Undo"),
        Selection_Modify("Redo"),
        Selection_Modify("Clear"),
        Selection_Modify("Invert"),
        Selection_Modify("Copy"),
        Selection_Modify("Select_Group"),
        Selection_Modify("Add_Group"),
        Selection_Modify("Unselect_Group"),
        Selection_Modify("Intersect_Group"),
        Selection_Modify("Despeckle"),
        Selection_Modify("Elkcepsed"),
        Selection_Modify("Expand"),
        Selection_Modify("Shrink"),
        Selection_Modify("Color_Range"),
        Selection_Modify("Rich_MS_Copy")
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
