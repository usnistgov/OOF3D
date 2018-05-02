# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# File for testing pixel grouping and selection operations on
# microstructures.  This includes re-running the Microstructure
# save/load and copy operations to ensure that they save/load/copy the
# pixel groups correctly.

# Need to be able to open a graphics window and make selections,
# also, of course.

## TODO 3.1: Add tests for pixel selection clicks with and without
## clipping and excluded voxels.

## TODO 3.1: Add tests using active areas.  Those will have to be in a
## separate file that is run after activearea_test.py.


import memorycheck
import unittest, os
import math
from UTILS import file_utils
file_utils.generate = False
reference_file = file_utils.reference_file


# Prerequisite for making toolbox selections is the existence of a
# graphics window.  These tests just open and close a graphics window.
class Graphics_Ops(unittest.TestCase):
    def setUp(self):
        global gfxmanager
        from ooflib.common.IO import gfxmanager

    # Opens a new graphics window, assuming that none are open (so
    # that the name will be "Graphics_1").
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

class PixelTest(unittest.TestCase):
    def setUp(self, msname):
        global pixelselection
        from ooflib.common import pixelselection
        OOF.Windows.Graphics.New()
        self.msname = msname
    def tearDown(self):
        OOF.Graphics_1.File.Close()
    def selectionSize(self):
        ps = pixelselection.pixelselectionWhoClass[self.msname]
        return ps.getObject().len()
    def isSelected(self, x, y, z):
        ps = pixelselection.pixelselectionWhoClass[self.msname]
        return ps.getObject().isSelected(iPoint(x, y, z))

        

# Tests of actual pixel selection operations.
# OOF.Toolbox.Pixel_Select items:
#   Point, Brush, Rectangle, Circle, Ellipse, Color, Burn.
# Selection modifiers from the same menu, Clear, Undo, Redo, Invert
class Direct_Pixel_Selection(PixelTest):
    def setUp(self):
        PixelTest.setUp(self, 'jpeg')
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data","jpeg"),
                sort=NumericalOrder()),
            microstructure_name=automatic,
            height=automatic, width=automatic, depth=automatic)

    # Direct selection operations -- these are toolbox ops in the
    # graphics window.

    # # Select circle, rectangle, ellipse, point.
    # def Circle(self):
    #     OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
    #         source="jpeg:jpeg",
    #         points=[Point(66.0,55.0), Point(87.6,41.8)],
    #         shift=0, ctrl=0)
    #     ps = pixelselection.pixelselectionWhoClass['jpeg']
    #     # Size should be 2000 pixels.
    #     self.assertEqual(ps.getObject().len(), 2000)

    def select1(self):
        OOF.VoxelSelection.Select(
            source='jpeg:jpeg',
            method=PointSelector(point=iPoint(31,49,99),
                                 operator=Select()))
    @memorycheck.check("jpeg")
    def Point(self):
        self.select1()
        # Size should be 1 pixel, of course.
        self.assertEqual(self.selectionSize(), 1)
        self.assert_(self.isSelected(31,49,99))

    @memorycheck.check("jpeg")
    def PointRotated(self):
        OOF.Graphics_1.Settings.Camera.View(
            view=View(Coord(-111.325,205.675,223.124), Coord(50,50,50),
                      Coord(0.211865,0.81662,-0.536885), 30, [], 0))
        OOF.VoxelSelection.Select(
            source='jpeg:jpeg',
            method=PointSelector(point=iPoint(0, 51, 51),
                                 operator=Select()))
        self.assertEqual(self.selectionSize(), 1)
        self.assert_(self.isSelected(0,51,51))

    # Makes and clears a selection.
    @memorycheck.check("jpeg")
    def Clear(self):
        self.select1()
        self.assertNotEqual(self.selectionSize(), 0)
        OOF.VoxelSelection.Clear(microstructure='jpeg')
        self.assertEqual(self.selectionSize(), 0)

    # Remining direct selection methods --
    # Point, Brush, Rectangle, Ellipse, Color, Burn.

    # # Brush points were recorded from an actual user session.
    # def Brush(self):
    #     OOF.Graphics_1.Toolbox.Pixel_Select.Brush(
    #         source='jpeg:jpeg',
    #         style=CircleBrush(radius=2.0),
    #         points=[Point(19.12,61.2829), Point(19.642,61.2829),
    #                 Point(20.1639,61.2829), Point(21.2078,61.2829),
    #                 Point(21.7298,60.761), Point(22.2518,60.761),
    #                 Point(22.7737,60.761), Point(23.2957,60.761), 
    #                 Point(23.8176,60.761), Point(24.3396,60.761), 
    #                 Point(24.8616,60.761), Point(25.3835,60.761), 
    #                 Point(25.9055,60.761), Point(26.4275,60.761), 
    #                 Point(26.9494,60.761), Point(27.4714,60.761), 
    #                 Point(27.9933,60.761), Point(28.5153,60.761), 
    #                 Point(29.0373,60.761), Point(29.0373,60.239), 
    #                 Point(29.5592,60.239), Point(30.0812,60.239), 
    #                 Point(30.6031,60.239), Point(31.1251,60.239), 
    #                 Point(31.6471,60.239), Point(32.169,60.239), 
    #                 Point(32.691,60.239), Point(33.2129,60.239), 
    #                 Point(33.7349,60.239), Point(34.2569,60.239), 
    #                 Point(34.7788,60.239), Point(35.3008,60.239), 
    #                 Point(35.8227,60.239), Point(36.3447,60.239), 
    #                 Point(36.8667,60.239), Point(37.3886,60.239), 
    #                 Point(37.9106,60.239), Point(38.4325,60.239), 
    #                 Point(38.9545,60.239), Point(39.4765,60.239), 
    #                 Point(39.9984,60.239)], shift=0, ctrl=0)
    #     ps =  pixelselection.pixelselectionWhoClass['jpeg']
    #     self.assertEqual(ps.getObject().len(), 94)


    # def Rectangle(self):
    #     OOF.Graphics_1.Toolbox.Pixel_Select.Rectangle(
    #         source='jpeg:jpeg',
    #         points=[Point(23.3,57.0), Point(123.0,24.75)],
    #         shift=0, ctrl=0)
    #     ps = pixelselection.pixelselectionWhoClass['jpeg']
    #     self.assertEqual(ps.getObject().len(), 3434)
        
    # def Ellipse(self):
    #     OOF.Graphics_1.Toolbox.Pixel_Select.Ellipse(
    #         source='jpeg:jpeg',
    #         points=[Point(23.3,57.0), Point(123.0,24.75)],
    #         shift=0, ctrl=0)
    #     ps = pixelselection.pixelselectionWhoClass['jpeg']
    #     self.assertEqual(ps.getObject().len(), 2526)

    @memorycheck.check("jpeg")
    def Color(self):
        OOF.VoxelSelection.Select(
            source='jpeg:jpeg',
            method=ColorSelector(
                point=iPoint(27,24,99),
                range=DeltaRGB(delta_red=0.3,delta_green=0.3,delta_blue=0.3),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 315647)

    @memorycheck.check("jpeg")
    def Burn(self):
        OOF.VoxelSelection.Select(
            source='jpeg:jpeg',
            method=Burn(point=iPoint(51,49,99),
                        local_flammability=0.1,
                        global_flammability=0.2,
                        color_space_norm='L1',
                        next_nearest=False,
                        operator=Select()))
        self.assertEqual(self.selectionSize(), 348922)
        # Click on same blob with smaller flammabilities
        OOF.VoxelSelection.Select(
            source='jpeg:jpeg',
            method=Burn(point=iPoint(50,51,99),
                        local_flammability=0.05,
                        global_flammability=0.1,
                        color_space_norm='L1',
                        next_nearest=False,
                        operator=Select()))
        self.assertEqual(self.selectionSize(), 280340)
        # Click on different blob
        OOF.VoxelSelection.Select(
            source='jpeg:jpeg',
            method=Burn(point=iPoint(91,48,99),
                        local_flammability=0.05,
                        global_flammability=0.1,
                        color_space_norm='L1',
                        next_nearest=False,
                        operator=Select()))
        self.assertEqual(self.selectionSize(), 4186)

    # Then, mechanical ones -- Undo, Redo, Invert.

    @memorycheck.check("jpeg")
    def Undo(self):
        ps = pixelselection.pixelselectionWhoClass['jpeg']
        self.assertEqual(self.selectionSize(), 0)
        self.assert_(not ps.undoable())
        ps_0_id = id(ps.getObject())
        self.select1()
        self.assert_(ps.undoable())
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        OOF.VoxelSelection.Undo(
            microstructure="jpeg")
        ps_2_id = id(ps.getObject())
        self.assertEqual(ps_0_id, ps_2_id)
        self.assertEqual(self.selectionSize(), 0)

    @memorycheck.check("jpeg")
    def Redo(self):
         ps = pixelselection.pixelselectionWhoClass['jpeg']
         ps_0_id = id(ps.getObject())
         self.select1()
         ps_1_id = id(ps.getObject())
         OOF.VoxelSelection.Undo(
             microstructure="jpeg")
         self.assert_(ps.redoable())
         OOF.VoxelSelection.Redo(
             microstructure="jpeg")
         self.assertEqual(id(ps.getObject()), ps_1_id)
         self.assert_(not ps.redoable())

    @memorycheck.check("jpeg")
    def Invert(self):
         self.select1()
         OOF.VoxelSelection.Invert(
             microstructure="jpeg")
         self.assertEqual(self.selectionSize(), 999999)
         
# Direct_Pixel_Selection2 is just like Direct_Pixel_Selection, but it
# uses a different image and the pixels aren't 1x1x1.  These tests
# made more sense when the voxel selection menu commands contained
# mouse click and view information.  Now they contain voxel
# coordinates and the mouse click and graphics configuration are
# irrelevant.

class Direct_Pixel_Selection2(PixelTest):
    def setUp(self):
        PixelTest.setUp(self, '5color')
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file('ms_data','5color'),
                pattern='slice(0|([1-9][0-9]*))\\.png',
                sort=NumericalOrder()),
            microstructure_name='5color',
            height=2.0, width=automatic, depth=automatic)

    # Clip, rotate, and select.
    @memorycheck.check("5color")
    def PointClipped0(self):
        OOF.Graphics_1.Toolbox.Viewer.Clip.New(
            normal=VectorDirection(x=1.0,y=0.0,z=0.0), offset=10.5)
        OOF.Graphics_1.Settings.Camera.View(
            view=View(cameraPosition=Coord(-39.6793,22.8537,38.1238),
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.094381,0.957917,-0.271087), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.5]],
                      invertClip=1))
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=PointSelector(point=iPoint(10, 8, 10),
                                 operator=Select()))
        
        self.assert_(self.isSelected(10, 8, 10))

    def tearDown(self):
        OOF.Graphics_1.File.Close()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Utility functions and data

from ooflib.common import color

# These are the hex representations of the colors used in the 5color
# image.  They're also the group names.
color_values = {
    "blue" :   "#5959f3",
    "red"  :   "#f35959",
    "yellow" : "#f3f359",
    "green" :  "#59f359",
    "white" :  "#fefefe"
    }

# These are the number of voxels with each color in the 5color image.
color_counts = {
    "blue" : 1205,
    "red" : 1077,
    "yellow" : 2313,
    "green" : 1020,
    "white" : 2385
}


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Pixel group creation/manipulation tests

# OOF.PixelGroup:
# New Rename Copy Delete Meshable AddSelection RemoveSelection Clear
# Query

# Pixel group creation/manipulation -- assume that selections are
# possible.  Also should test the autogroup from the image menu.
# These tests use the 5color image, which autogroups reasonably
# cleanly, rather than the more difficult jpeg.
class Pixel_Groups(PixelTest):
    def setUp(self):
        global microstructure
        global color
        from ooflib.common import microstructure
        from ooflib.common import color
        PixelTest.setUp(self, '5color')
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data", "5color"),
                pattern="slice(0|([1-9][0-9]*))\\.tif",
                sort=NumericalOrder()),
            microstructure_name=automatic,
            height=automatic, width=automatic, depth=automatic)

    def select1(self):
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=PointSelector(point=iPoint(17,18,19),
                                 operator=Select()))

    @memorycheck.check("5color")
    def AutoGroup(self):
        OOF.Image.AutoGroup(image="5color:5color")
        ms = microstructure.getMicrostructure("5color")
        groups = ms.groupNames()
        self.assertEqual(len(groups), 5)
        for groupname in groups:
            for colorname, gname in color_values.items():
                if gname == groupname:
                    self.assertEqual(len(ms.findGroup(groupname)),
                                     color_counts[colorname])
                break
            else:
                self.fail("Got an unexpected group name: " + groupname)
                            
    @memorycheck.check("5color")
    def New(self):
        OOF.PixelGroup.New(name="test", microstructure="5color")
        ms = microstructure.getMicrostructure("5color")
        groups = ms.groupNames()
        self.assertEqual(len(groups),1)
        self.assert_("test" in groups)

    # Delete a group
    @memorycheck.check("5color")
    def Delete(self):           
        OOF.PixelGroup.New(name="test", microstructure="5color")
        ms = microstructure.getMicrostructure("5color")
        OOF.PixelGroup.Delete(microstructure="5color", group="test")
        groups = ms.groupNames()
        self.assertEqual(len(groups),0)

    # Add selected pixels to a group
    @memorycheck.check("5color")
    def AddSelection(self):
        OOF.PixelGroup.New(name="test", microstructure="5color")
        ms = microstructure.getMicrostructure("5color")
        OOF.VoxelSelection.Select(
            source="5color:5color",
            method=PointSelector(point=iPoint(1,2,3),
                                 operator=Select()))
        OOF.PixelGroup.AddSelection(
            microstructure="5color", group="test")
        sel_size = self.selectionSize()
        OOF.VoxelSelection.Clear(
            microstructure="5color")
        group = ms.findGroup("test")
        self.assertEqual(len(group), sel_size)
       
    # Remove selected pixels from a group
    @memorycheck.check("5color")
    def RemoveSelection(self):
        OOF.PixelGroup.New(name="test", microstructure="5color")
        ms = microstructure.getMicrostructure("5color")
        # Select a lot of pixels
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=ColorSelector(
                point=iPoint(10,15,2),
                range=DeltaRGB(delta_red=0.3,delta_green=0.3,delta_blue=0.3),
                operator=Select()))
        sel_large = self.selectionSize()
        OOF.PixelGroup.AddSelection(
            microstructure="5color", group="test")
        self.select1()
        
        sel_small = self.selectionSize()
        OOF.PixelGroup.RemoveSelection(
            microstructure="5color", group="test")
        OOF.VoxelSelection.Clear(
            microstructure="5color")
        group = ms.findGroup("test")
        self.assertEqual(len(group), sel_large-sel_small)

    # Copy a pixel group
    @memorycheck.check("5color")
    def Copy(self):
        ms = microstructure.getMicrostructure("5color")
        OOF.PixelGroup.New(name="test", microstructure="5color")
        self.select1()
        OOF.PixelGroup.AddSelection(
            microstructure="5color", group="test")
        group = ms.findGroup("test")
        initial_group_size = len(group)
        OOF.PixelGroup.Copy(microstructure="5color",
                            group="test", name="testcopy")
        OOF.PixelGroup.Delete(microstructure="5color", group="test")
        self.assertEqual(ms.nGroups(), 1)
        group = ms.findGroup("testcopy")
        self.assertEqual(len(group), initial_group_size) 
        
    # Rename a pixel group
    @memorycheck.check("5color")
    def Rename(self):
        ms = microstructure.getMicrostructure("5color")
        OOF.PixelGroup.New(name="test", microstructure="5color")
        self.select1()
        OOF.PixelGroup.AddSelection(
            microstructure="5color", group="test")
        group = ms.findGroup("test")
        initial_group_size = len(group)
        OOF.PixelGroup.Rename(microstructure="5color",
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

class Selection_Modify(PixelTest):
    def setUp(self):
        global microstructure
        global pixelselection
        from ooflib.common import microstructure
        from ooflib.common import pixelselection
        PixelTest.setUp(self, '5color')
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file('ms_data', '5color'),
                pattern='slice(0|([1-9][0-9]*))\\.png',
                sort=NumericalOrder()), 
            microstructure_name='5color',
            height=automatic, width=automatic, depth=automatic)

    def selectWhite(self, operator):
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=ColorSelector(
                point=iPoint(8,9,19),
                range=DeltaRGB(delta_red=0,delta_green=0,delta_blue=0),
                operator=operator))

    def selectBlue(self, operator):
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=ColorSelector(
                point=iPoint(3,16,9),
                range=DeltaRGB(delta_red=0,delta_green=0,delta_blue=0),
                operator=operator))

    def selectYellow(self, operator):
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=ColorSelector(
                point=iPoint(5,2,19),
                range=DeltaRGB(delta_red=0,delta_green=0,delta_blue=0),
                operator=operator))

    def selectInteriorWhitePoint(self, operator):
        # This selects a white voxel completely surrounded by white
        # voxels.
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=PointSelector(
                point=iPoint(8,15,12),
                operator=operator))

    def selectInteriorYellowPoint(self, operator):
        # This selects a yellow voxel on the yellow/white boundary.
        # It has 17 yellow neighbors. 
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=PointSelector(
                point=iPoint(7,13,10),
                operator=operator))

    ############

    @memorycheck.check("5color")
    def Undo(self):
        # A lot of the obvious checks are already done in the undo
        # test in Direct_Pixel_Selection.
        ps = pixelselection.pixelselectionWhoClass["5color"]
        ps_0_id = id(ps.getObject())
        self.selectWhite(operator=Select())
        ps_1_id = id(ps.getObject())
        OOF.VoxelSelection.Undo(microstructure="5color")
        ps_2_id = id(ps.getObject())
        self.assertEqual(ps_2_id, ps_0_id)
        self.assertNotEqual(ps_2_id, ps_1_id)

    @memorycheck.check("5color")
    def Redo(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        ps_0_id = id(ps.getObject())
        self.selectWhite(operator=Select())
        ps_1_id = id(ps.getObject())
        OOF.VoxelSelection.Undo(microstructure="5color")
        OOF.VoxelSelection.Redo(microstructure="5color")
        ps_2_id = id(ps.getObject())
        self.assert_(not ps.redoable())
        self.assertEqual(ps_2_id, ps_1_id)
        self.assertNotEqual(ps_2_id, ps_0_id)

    @memorycheck.check("5color")
    def Clear(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        ps_0_id = id(ps.getObject())
        self.selectWhite(operator=Select())
        OOF.VoxelSelection.Clear(microstructure="5color")
        ps_1_id = id(ps.getObject())
        self.assertEqual(self.selectionSize(), 0)
        self.assertNotEqual(ps_0_id, ps_1_id)

    @memorycheck.check("5color")
    def Invert(self):
        self.selectWhite(operator=Select())
        OOF.VoxelSelection.Invert(microstructure="5color")
        self.assertEqual(self.selectionSize(), 8000-color_counts["white"])

    @memorycheck.check("5color")
    def Copy(self):
        OOF.Microstructure.Copy(microstructure="5color", name="copy")
        copy_ps = pixelselection.pixelselectionWhoClass["copy"]
        self.selectWhite(operator=Select())
        self.assertEqual(copy_ps.getObject().len(), 0)
        OOF.VoxelSelection.Select(
            source='copy',
            method=CopyPixelSelection(
                source="5color",
                operator=Select()))
        self.assertEqual(copy_ps.getObject().len(),
                         copy_ps.getObject().len())
        # Select more pixels in 5color and add them to the selection in 'copy.
        self.selectBlue(operator=AddSelection())
        OOF.VoxelSelection.Select(
            source='copy',
            method=CopyPixelSelection(
                source="5color",
                operator=AddSelection()))
        self.assertEqual(copy_ps.getObject().len(),
                         color_counts['white'] + color_counts['blue'])
        OOF.Microstructure.Delete(microstructure="copy")

    @memorycheck.check("5color")
    def Select_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        self.selectWhite(operator=Select())
        ps_0_id = id(ps.getObject())
        OOF.PixelGroup.New(name="test", microstructure="5color")
        OOF.PixelGroup.AddSelection(microstructure="5color", group="test")
        OOF.VoxelSelection.Undo(microstructure="5color")
        OOF.VoxelSelection.Select(
            source="5color",
            method=GroupSelector(group="test", operator=Select()))
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(self.selectionSize(), color_counts["white"])

    @memorycheck.check("5color")
    def Add_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        self.selectWhite(operator=Select())
        OOF.PixelGroup.New(name="test", microstructure="5color")
        OOF.PixelGroup.AddSelection(microstructure="5color", group="test")
        OOF.VoxelSelection.Undo(microstructure="5color")
        self.assertEqual(self.selectionSize(), 0)
        self.selectBlue(operator=AddSelection())
        self.assertEqual(self.selectionSize(), color_counts["blue"])
        ps_0_id = id(ps.getObject())
        OOF.VoxelSelection.Select(
            source="5color",
            method=GroupSelector(group="test",
                                 operator=AddSelection()))
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(self.selectionSize(),
                         color_counts["white"]+color_counts["blue"])
        
    @memorycheck.check("5color")
    def Unselect_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        # Select a bunch of voxels
        self.selectWhite(operator=Select())
        ps_0_id = id(ps.getObject())
        size0 = self.selectionSize()
        # Add them to a group
        OOF.PixelGroup.New(name='test', microstructure='5color')
        OOF.PixelGroup.AddSelection(microstructure='5color', group='test')
        # Select all of the voxels.
        OOF.VoxelSelection.Clear(microstructure='5color')
        OOF.VoxelSelection.Invert(microstructure='5color')
        ps_1_id = id(ps.getObject())
        size1 = self.selectionSize()
        # Unselect the voxels in the group.
        OOF.VoxelSelection.Select(
            source='5color',
            method=GroupSelector(group='test',
                                 operator=Unselect()))
        ps_2_id = id(ps.getObject())
        size2 = self.selectionSize()
        self.assertNotEqual(ps_0_id, ps_2_id)
        self.assertNotEqual(ps_1_id, ps_2_id)
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(size1-size0, size2)
        
    @memorycheck.check("5color")
    def Intersect_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        self.selectWhite(operator=Select())
        self.selectBlue(operator=AddSelection())
        self.assertEqual(self.selectionSize(), 
                         color_counts["white"] + color_counts["blue"])
        OOF.PixelGroup.New(name="test", microstructure="5color")
        OOF.PixelGroup.AddSelection(microstructure="5color", group="test")
        OOF.VoxelSelection.Clear(microstructure="5color")
        self.selectYellow(operator=Select())
        self.selectWhite(operator=AddSelection())
        self.assertEqual(self.selectionSize(), 
                         color_counts["white"] + color_counts["yellow"])
        ps_0_id = id(ps.getObject())
        OOF.VoxelSelection.Select(
            source="5color",
            method=GroupSelector(group="test", operator=Intersect()))
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(self.selectionSize(), color_counts["white"])

    @memorycheck.check("5color")
    def Despeckle(self):
        self.selectWhite(operator=Select())
        # Deselect a point completely within the white region
        self.selectInteriorWhitePoint(operator=Unselect()) 
        self.assertEqual(self.selectionSize(), color_counts["white"]-1)
        # Despecking with neighbors=26 should reselect just the one point
        OOF.VoxelSelection.Select(
            source="5color",
            method= Despeckle(neighbors=26))
        self.assertEqual(self.selectionSize(), color_counts["white"])

    @memorycheck.check("5color")
    def Elkcepsed(self):
        self.selectBlue(operator=Select())
        # Elkcepseding the blue region with neighbors=3 doesn't do anything.
        OOF.VoxelSelection.Select(
            source="5color",
            method=Elkcepsed(neighbors=3))
        self.assertEqual(self.selectionSize(), color_counts["blue"])
        # Add an isolated voxel to the selection.
        self.selectInteriorWhitePoint(
            operator=AddSelection())
        self.assertEqual(self.selectionSize(), color_counts["blue"]+1)
        # Elkcepseding deselects just the isolated voxel.
        OOF.VoxelSelection.Select(
            source="5color",
            method=Elkcepsed(neighbors=3))
        self.assertEqual(self.selectionSize(), color_counts["blue"])

        # Run Elkcepsed with neighbors=10 on the white voxels.
        OOF.VoxelSelection.Clear(microstructure="5color")
        self.selectWhite(operator=Select())
        OOF.VoxelSelection.Select(
            source="5color",
            method=Elkcepsed(neighbors=10))
        n1 = self.selectionSize()
        self.assertEqual(n1, 2174)

        OOF.VoxelSelection.Clear(microstructure="5color")
        
        # Select a single yellow voxel that is adjacent to 9 white voxels.
        OOF.Image.AutoGroup(image='5color:5color', name_template='%c')
        OOF.VoxelSelection.Select(
            source='5color:5color',
            method=PointSelector(point=iPoint(6,13,11),
                                 operator=Select()))
        
        # Select the white voxels too.
        OOF.VoxelSelection.Select(
            source='5color',
            method=GroupSelector(group='#fefefe',
                                 operator=AddSelection()))
        self.assertEqual(self.selectionSize(), color_counts["white"]+1)
        # Now run Elkcepsed with neighbors=10 again.  The single yellow
        # voxel shouldn't have made a difference.
        OOF.VoxelSelection.Select(
            source='5color',
            method=Elkcepsed(neighbors=10))
        self.assertEqual(self.selectionSize(), n1)

    @memorycheck.check("5color")
    def Expand(self):
        self.selectInteriorWhitePoint(operator=Select())
        self.assertEqual(self.selectionSize(), 1)
        # Expanding with a radius of 0.9 doesn't do anything
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=0.9))
        self.assertEqual(self.selectionSize(), 1)
        # radius=1 selects near neighbors
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.0))
        self.assertEqual(self.selectionSize(), 7)
        OOF.VoxelSelection.Undo(microstructure="5color")
        # radius=sqrt(2) selects nearest neighbors and next-nearest
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.415))
        self.assertEqual(self.selectionSize(), 19)
        OOF.VoxelSelection.Undo(microstructure="5color")
        # radius=sqrt(3) selects a full 3x3x3 voxel cube
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.733))
        self.assertEqual(self.selectionSize(), 27)
        # Add another layer
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.733))
        self.assertEqual(self.selectionSize(), 125)

    @memorycheck.check("5color")
    def Shrink(self): 
        # A single voxel should vanish.
        self.selectInteriorWhitePoint(operator=Select())
        OOF.VoxelSelection.Select(
            source='5color',
            method=Shrink(radius=1.0))
        self.assertEqual(self.selectionSize(), 0)
        # A 3x3x3 cube ...
        self.selectInteriorWhitePoint(operator=Select())
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.733))
        # ... shrinking by 1 produces a 1x1x1 cube
        OOF.VoxelSelection.Select(
            source='5color',
            method=Shrink(radius=1.0))
        self.assertEqual(self.selectionSize(), 1)
        # A 5x5x5 cube ...
        self.selectInteriorWhitePoint(operator=Select())
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.733))
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.733))
        # ... shrink by one produces a 3x3x3 cube
        OOF.VoxelSelection.Select(
            source='5color',
            method=Shrink(radius=1.0))
        self.assertEqual(self.selectionSize(), 27)
        # 5x5 again
        OOF.VoxelSelection.Select(
            source='5color',
            method=Expand(radius=1.733))
        # Shrink by 2 to get back to 1x1x1
        OOF.VoxelSelection.Select(
            source='5color',
            method=Shrink(radius=2.0))
        self.assertEqual(self.selectionSize(), 1)

        self.selectWhite(operator=Select())
        OOF.VoxelSelection.Select(
            source='5color',
            method=Shrink(radius=1.42))
        self.assertEqual(self.selectionSize(), 253)
        OOF.VoxelSelection.Select(
            source='5color',
            method=Shrink(radius=1.))
        self.assertEqual(self.selectionSize(), 5)

    # Color range is a selector, not really a modifer, but there you go.
    @memorycheck.check("5color")
    def Color_Range(self):
        # Select the "white" pixels, which aren't quite white.
        OOF.VoxelSelection.Select(
            source='5color',
            method=ColorRange(
                image='5color:5color',
                reference=RGBColor(red=1.00000,green=1.00000,blue=1.00000), 
                range=DeltaGray(delta_gray=0.174603),
                operator=Select()))
        self.assertEqual(self.selectionSize(), color_counts["white"])
        # Fail to select any pixels, by restricting the range.
        OOF.VoxelSelection.Select(
            source='5color',
            method=ColorRange(
                image='5color:5color',
                reference=RGBColor(red=1.00000,green=1.00000,blue=1.00000), 
                range=DeltaGray(delta_gray=0.001),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 0)   
        # Select the blue pixels
        OOF.VoxelSelection.Select(
            source='5color',
            method=ColorRange(
                image='5color:5color', 
                reference=RGBColor(red=0.00000,green=0.00000,blue=1.00000),
                range=DeltaRGB(delta_red=0.380952,delta_green=0.396825,
                               delta_blue=0.0952381),
                operator=Select()))
        self.assertEqual(self.selectionSize(), color_counts["blue"])

    # Element and segment ops can't be tested until skeletons exist.

    # Rich_MS_Copy is a test of the microstructure copying process now
    # that nontrivial groups and selections can be made -- these
    # should survive the copy process.  The magic numbers come from
    # the autogroup and circle-selection tests, also in this file.
    @memorycheck.check("5color")
    def Rich_MS_Copy(self):
        from ooflib.common import color
        OOF.Image.AutoGroup(image="5color:5color")
        self.selectInteriorYellowPoint(operator=Select())
        OOF.Microstructure.Copy(microstructure="5color", name="copy")

        # Make sure that the groups were copied correctly.  This is
        # just like running the AutoGroup test in the copied
        # Microstructure.
        ms = microstructure.getMicrostructure("copy")
        groups = ms.groupNames()
        self.assertEqual(len(groups), 5)
        for groupname in groups:
            for colorname, gname in color_values.items():
                if gname == groupname:
                    self.assertEqual(len(ms.findGroup(groupname)),
                                     color_counts[colorname])
                    break
            else:
                self.fail("Got an unexpected group name: "+ groupname)

        # Selection should *not* be copied.
        ps = pixelselection.pixelselectionWhoClass["copy"]
        self.assertEqual(ps.getObject().len(), 0)
        OOF.Microstructure.Delete(microstructure="copy")
        
    @memorycheck.check("5color")
    def Box(self):
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=BoxSelectionShape(point0=Point(0,0,0),
                                        point1=Point(2,3,4)),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 24)
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=BoxSelectionShape(point0=Point(1,1,1),
                                        point1=Point(2,3,4)),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 6)
        # Only voxels with centers inside the region are selected.
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=BoxSelectionShape(point0=Point(0.6,1,1),
                                        point1=Point(2,3,4)),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 6)
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=BoxSelectionShape(point0=Point(0.4,1,1),
                                        point1=Point(2,3,4)),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 12)
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=BoxSelectionShape(point0=Point(0,0,0),
                                        point1=Point(0,0,0)),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 0)

    @memorycheck.check("5color")
    def Circle(self):
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=CircleSelectionShape(center=Point(10,10,10),radius=0.0),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 0)
        # The center is at the corner of 8 voxels. r=sqrt(3)/2 should
        # make the sphere include the centers of all 8.
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=CircleSelectionShape(center=Point(10,10,10),
                                           radius=0.867),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 8)
        # Move the center to the center of a voxel.
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=CircleSelectionShape(center=Point(10.5,10.5,10.5),
                                           radius=0.867),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 1)
        OOF.VoxelSelection.Select(
            source='5color',
            method=RegionSelector(
                shape=CircleSelectionShape(center=Point(10.5,10.5,10.5),
                                           radius=1.00001),
                units=PhysicalUnits(),
                operator=Select()))
        self.assertEqual(self.selectionSize(), 7)
        
    def tearDown(self):
        OOF.Graphics_1.File.Close()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SaveGroup(PixelTest):
    def setUp(self):
        PixelTest.setUp(self, "microstructure")
    @memorycheck.check("microstructure")
    def Save(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=3, height_in_pixels=3, depth_in_pixels=3)
        OOF.Graphics_1.Layer.New( 
            category='Microstructure',
            what='microstructure',
            how=MicrostructureMaterialDisplay(
                no_material=Gray(value=0.4444444444444444),
                no_color=RGBColor(red=0.00000,green=0.00000,blue=1.00000),
                filter=AllVoxels()))
        # Select the eight voxels at the corners of the microstructure.
        for x in (0,2):
            for y in (0,2):
                for z in (0,2):
                    OOF.VoxelSelection.Select(
                        source='microstructure',
                        method=PointSelector(point=iPoint(x,y,z),
                                             operator=AddSelection()))
        OOF.PixelGroup.New(
            name='pixelgroup', microstructure='microstructure')
        OOF.PixelGroup.AddSelection(
            microstructure='microstructure', group='pixelgroup')
        # Save ascii
        OOF.File.Save.Microstructure(
            filename='micro.dat',
            mode='w', 
            format='ascii',
            microstructure='microstructure')
        self.assert_(file_utils.fp_file_compare(
            "micro.dat",
            os.path.join("ms_data", "pixgrp_save_ascii"),
            1.e-9))
        file_utils.remove("micro.dat")
        # Save binary
        OOF.File.Save.Microstructure(
            filename='micro.dat',
            mode='w',
            format='binary',
            microstructure='microstructure')
        self.assert_(file_utils.binary_file_compare(
            "micro.dat", os.path.join("ms_data", "pixgrp_save_binary")))
        os.remove("micro.dat")

    @memorycheck.check("microstructure")
    def LoadAscii(self):
        OOF.File.Load.Data(filename=reference_file("ms_data",
                                                   "pixgrp_save_ascii"))
        ms = getMicrostructure("microstructure")
        self._checkVoxels()

    @memorycheck.check("microstructure")
    def LoadBinary(self):
        OOF.File.Load.Data(filename=reference_file("ms_data",
                                                   "pixgrp_save_binary"))
        ms = getMicrostructure("microstructure")
        self._checkVoxels()

    def _checkVoxels(self):
        # Check that only the corner voxels are in the pixel group.
        OOF.VoxelSelection.Select(
            source="microstructure",
            method=GroupSelector(
                group="pixelgroup", operator=Select()))
        self.assertEqual(self.selectionSize(), 8)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if i==1 or j==1 or k==1:
                        self.assert_(not self.isSelected(i, j, k))
                    else:
                        self.assert_(self.isSelected(i, j, k))
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
    
test_set = [
    Graphics_Ops("New"),
    Graphics_Ops("Close"),
    #Direct_Pixel_Selection("Circle"),
    Direct_Pixel_Selection("Point"),
    Direct_Pixel_Selection("PointRotated"),
    Direct_Pixel_Selection2("PointClipped0"),
    ## Direct_Pixel_Selection2("PointClipped1"), ** obsolete **
    ## Direct_Pixel_Selection2("PointClipped2"), ** obsolete **
    Direct_Pixel_Selection("Clear"),
    #Direct_Pixel_Selection("Brush"),
    #Direct_Pixel_Selection("Rectangle"),
    #Direct_Pixel_Selection("Ellipse"),
    Direct_Pixel_Selection("Color"),
    ## Direct_Pixel_Selection("ColorRotated"),  ** obsolete **
    ## Direct_Pixel_Selection("ColorRotated2"), ** obsolete **
    Direct_Pixel_Selection("Burn"),
    Direct_Pixel_Selection("Undo"),
    Direct_Pixel_Selection("Redo"),
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
    Selection_Modify("Rich_MS_Copy"),

    Selection_Modify("Box"),
    Selection_Modify("Circle"),
    
    SaveGroup("Save"),
    SaveGroup("LoadAscii"),
    SaveGroup("LoadBinary"),
]

