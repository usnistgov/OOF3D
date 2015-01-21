# -*- python -*-
# $RCSfile: pixel_test.py,v $
# $Revision: 1.2.16.19 $
# $Author: langer $
# $Date: 2014/09/19 03:28:58 $

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
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='jpeg:jpeg',
            points=[Point(40.6039,49.6023,212.283)], 
            view=View(cameraPosition=Coord(50,50,333.253),
                      focalPoint=Coord(50,50,50),
                      up=Coord(0,1,0),
                      angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)

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
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='jpeg:jpeg',
            points=[Point(-110.985,205.205,222.6)], 
            view=View(cameraPosition=Coord(-111.325,205.675,223.124),
                      focalPoint=Coord(50,50,50),
                      up=Coord(0.211865,0.81662,-0.536885),
                      angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 1)
        self.assert_(self.isSelected(0,51,51))

    @memorycheck.check("jpeg")
    def PointRotated2(self):
        # Just like PointRotated, but the view given in the selection
        # command is not the current view when the command is issued.
        OOF.Graphics_1.Toolbox.Viewer.Restore_Named_View(
            view='Right')
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='jpeg:jpeg',
            points=[Point(-110.985,205.205,222.6)], 
            view=View(cameraPosition=Coord(-111.325,205.675,223.124),
                      focalPoint=Coord(50,50,50),
                      up=Coord(0.211865,0.81662,-0.536885),
                      angle=30, clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 1)
        self.assert_(self.isSelected(0,51,51))

    # Makes and clears a selection.
    @memorycheck.check("jpeg")
    def Clear(self):
        self.select1()
        self.assertNotEqual(self.selectionSize(), 0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="jpeg:jpeg")
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
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='jpeg:jpeg',
            range=DeltaRGB(delta_red=0.3,delta_green=0.3,delta_blue=0.3),
            points=[Point(38.7148,45.6251,212.283)],
            view=View(cameraPosition=Coord(50,50,333.253), 
                      focalPoint=Coord(50,50,50),
                      up=Coord(0,1,0), 
                      angle=30, 
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 332104)

    @memorycheck.check("jpeg")
    def ColorRotated(self):
        OOF.Graphics_1.Settings.Camera.View(
            view=View(cameraPosition=Coord(185.464,154.852,275.584), 
                      focalPoint=Coord(50,50,50),
                      up=Coord(-0.40712,0.896951,-0.172429), 
                      angle=30,
                      clipPlanes=[], invertClip=0))
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='jpeg:jpeg', 
            range=DeltaRGB(delta_red=0.3,delta_green=0.3,delta_blue=0.3),
            points=[Point(175.356,147.521,262.265)], 
            view=View(cameraPosition=Coord(185.464,154.852,275.584),
                      focalPoint=Coord(50,50,50), 
                      up=Coord(-0.40712,0.896951,-0.172429), 
                      angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 318395)

    @memorycheck.check("jpeg")
    def ColorRotated2(self):
        # Just like ColorRotated, but the view given in the selection
        # command is not the current view when the command is issued.
        OOF.Graphics_1.Toolbox.Viewer.Restore_Named_View(
            view='Right')
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='jpeg:jpeg', 
            range=DeltaRGB(delta_red=0.3,delta_green=0.3,delta_blue=0.3),
            points=[Point(175.356,147.521,262.265)], 
            view=View(cameraPosition=Coord(185.464,154.852,275.584),
                      focalPoint=Coord(50,50,50), 
                      up=Coord(-0.40712,0.896951,-0.172429), 
                      angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 318395)

    @memorycheck.check("jpeg")
    def Burn(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Burn(
            source='jpeg:jpeg',
            local_flammability=0.1, global_flammability=0.2,
            color_space_norm='L1', next_nearest=False,
            points=[Point(29.7661,56.3635,212.283)],
            view=View(cameraPosition=Coord(50,50,333.253),
                      focalPoint=Coord(50,50,50),
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 347925)


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
        OOF.Graphics_1.Toolbox.Pixel_Select.Undo(
            source="jpeg:jpeg")
        ps_2_id = id(ps.getObject())
        self.assertEqual(ps_0_id, ps_2_id)
        self.assertEqual(self.selectionSize(), 0)

    @memorycheck.check("jpeg")
    def Redo(self):
         ps = pixelselection.pixelselectionWhoClass['jpeg']
         ps_0_id = id(ps.getObject())
         self.select1()
         ps_1_id = id(ps.getObject())
         OOF.Graphics_1.Toolbox.Pixel_Select.Undo(
             source="jpeg:jpeg")
         self.assert_(ps.redoable())
         OOF.Graphics_1.Toolbox.Pixel_Select.Redo(
             source="jpeg:jpeg")
         self.assertEqual(id(ps.getObject()), ps_1_id)
         self.assert_(not ps.redoable())

    @memorycheck.check("jpeg")
    def Invert(self):
         self.select1()
         OOF.Graphics_1.Toolbox.Pixel_Select.Invert(
             source="jpeg:jpeg")
         # Magic number is total minus circle-selected number.
         self.assertEqual(self.selectionSize(), 999999)
         
# Direct_Pixel_Selection2 is just like Direct_Pixel_Selection, but it
# uses a different image. 

class Direct_Pixel_Selection2(PixelTest):
    def setUp(self):
        PixelTest.setUp(self, '5color')
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file('ms_data','5color'),
                pattern='slice(0|([1-9][0-9]*))\\.png',
                sort=NumericalOrder()),
            microstructure_name='5color',
            height=automatic, width=automatic, depth=automatic)

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
                      invertClip=0))
        # This should select voxel (10, 8, 10)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='5color:5color',
            points=[Point(-39.5607,22.8204,38.0586)],
            view=View(cameraPosition=Coord(-39.6793,22.8537,38.1238), 
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.094381,0.957917,-0.271087), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.5]], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 1)
        self.assert_(self.isSelected(10, 8, 10))

    # Clip and then select from a rotated viewpoint, without
    # explicitly rotating.
    @memorycheck.check("5color")
    def PointClipped1(self):
        OOF.Graphics_1.Toolbox.Viewer.Clip.New(
            normal=VectorDirection(x=1.0,y=0.0,z=0.0), offset=10.5)
        # This should select voxel (10, 8, 10)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='5color:5color',
            points=[Point(-39.5607,22.8204,38.0586)],
            view=View(cameraPosition=Coord(-39.6793,22.8537,38.1238), 
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.094381,0.957917,-0.271087), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.5]], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 1)
        self.assert_(self.isSelected(10, 8, 10))

    # Select from a clipped and rotated viewpoint, without explicitly
    # either rotating or clipping.
    @memorycheck.check("5color")
    def PointClipped2(self):
        # This should select voxel (10, 9, 8)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='5color:5color', 
            points=[Point(-41.0493,11.8455,38.2788)], 
            view=View(cameraPosition=Coord(-41.1612,11.8497,38.3428), 
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.0205011,0.999392,-0.028217), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.5]], invertClip=0),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionSize(), 1)
        self.assert_(self.isSelected(10, 9, 8))

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
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="5color:5color",
            points=[Point(7.20603,12.9232,42.4565)], 
            view=View(cameraPosition=Coord(10,10,66.6506),
                      focalPoint=Coord(10,10,10), 
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0,ctrl=0)
        OOF.PixelGroup.AddSelection(
            microstructure="5color", group="test")
        sel_size = self.selectionSize()
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="5color:5color")
        group = ms.findGroup("test")
        self.assertEqual(len(group), sel_size)
       
    # Remove selected pixels from a group
    @memorycheck.check("5color")
    def RemoveSelection(self):
        OOF.PixelGroup.New(name="test", microstructure="5color")
        ms = microstructure.getMicrostructure("5color")
        # Select a lot of pixels
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='5color:5color',
            range=DeltaRGB(delta_red=0,delta_green=0,delta_blue=0),
            points=[Point(7.20603,12.9232,42.4565)], 
            view=View(cameraPosition=Coord(10,10,66.6506),
                      focalPoint=Coord(10,10,10), 
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)
        sel_large = self.selectionSize()
        OOF.PixelGroup.AddSelection(
            microstructure="5color", group="test")
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="5color:5color",
            points=[Point(7.20603,12.9232,42.4565)], 
            view=View(cameraPosition=Coord(10,10,66.6506),
                      focalPoint=Coord(10,10,10), 
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0,ctrl=0)
        sel_small = self.selectionSize()
        OOF.PixelGroup.RemoveSelection(
            microstructure="5color", group="test")
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="5color:5color")
        group = ms.findGroup("test")
        self.assertEqual(len(group), sel_large-sel_small)

    # Copy a pixel group
    @memorycheck.check("5color")
    def Copy(self):
        ms = microstructure.getMicrostructure("5color")
        OOF.PixelGroup.New(name="test", microstructure="5color")
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="5color:5color",
            points=[Point(7.20603,12.9232,42.4565)], 
            view=View(cameraPosition=Coord(10,10,66.6506),
                      focalPoint=Coord(10,10,10), 
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0,ctrl=0)
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
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source="5color:5color",
            points=[Point(7.20603,12.9232,42.4565)], 
            view=View(cameraPosition=Coord(10,10,66.6506),
                      focalPoint=Coord(10,10,10), 
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0,ctrl=0)
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

    def selectWhite(self, shift=0, ctrl=0):
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='5color:5color', 
            range=DeltaRGB(delta_red=0,delta_green=0,delta_blue=0),
            points=[Point(5.90108,9.44349,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=shift, ctrl=ctrl)


    def selectBlue(self, shift=0, ctrl=0):
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='5color:5color', 
            range=DeltaRGB(delta_red=0,delta_green=0,delta_blue=0),
            points=[Point(5.79406,14.0454,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0), 
            shift=shift, ctrl=ctrl)

    def selectYellow(self, shift=0, ctrl=0):
        OOF.Graphics_1.Toolbox.Pixel_Select.Color(
            source='5color:5color',
            range=DeltaRGB(delta_red=0,delta_green=0,delta_blue=0),
            points=[Point(8.16993,7.96659,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=shift, ctrl=ctrl)

    def selectInteriorWhitePoint(self, shift=0, ctrl=0):
        # This selects a white voxel completely surrounded by white
        # voxels.
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='5color:5color', 
            points=[Point(-39.9938,12.3018,40.071)], 
            view=View(cameraPosition=Coord(-40.1038,12.3068,40.1412),
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.0376411,0.999195,-0.0139001), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.5]], invertClip=0),
            shift=shift, ctrl=ctrl)

    def selectInteriorYellowPoint(self, shift=0, ctrl=0):
        # This selects a yellow voxel on the yellow/white boundary.
        # It has 12 yellow neighbors.
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='5color:5color',
            points=[Point(-39.9903,12.3024,40.0768)],
            view=View(cameraPosition=Coord(-40.1038,12.3068,40.1412),
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.0376411,0.999195,-0.0139001), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.5]],
                      invertClip=0),
            shift=shift, ctrl=ctrl)

    ############

    @memorycheck.check("5color")
    def Undo(self):
        # A lot of the obvious checks are already done in the undo
        # test in Direct_Pixel_Selection.
        ps = pixelselection.pixelselectionWhoClass["5color"]
        ps_0_id = id(ps.getObject())
        self.selectWhite()
        ps_1_id = id(ps.getObject())
        OOF.PixelSelection.Undo(microstructure="5color")
        ps_2_id = id(ps.getObject())
        self.assertEqual(ps_2_id, ps_0_id)
        self.assertNotEqual(ps_2_id, ps_1_id)

    @memorycheck.check("5color")
    def Redo(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        ps_0_id = id(ps.getObject())
        self.selectWhite()
        ps_1_id = id(ps.getObject())
        OOF.PixelSelection.Undo(microstructure="5color")
        OOF.PixelSelection.Redo(microstructure="5color")
        ps_2_id = id(ps.getObject())
        self.assert_(not ps.redoable())
        self.assertEqual(ps_2_id, ps_1_id)
        self.assertNotEqual(ps_2_id, ps_0_id)

    @memorycheck.check("5color")
    def Clear(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        ps_0_id = id(ps.getObject())
        self.selectWhite()
        OOF.PixelSelection.Clear(microstructure="5color")
        ps_1_id = id(ps.getObject())
        self.assertEqual(self.selectionSize(), 0)
        self.assertNotEqual(ps_0_id, ps_1_id)

    @memorycheck.check("5color")
    def Invert(self):
        self.selectWhite()
        OOF.PixelSelection.Invert(microstructure="5color")
        self.assertEqual(self.selectionSize(), 8000-color_counts["white"])

    @memorycheck.check("5color")
    def Copy(self):
        OOF.Microstructure.Copy(microstructure="5color", name="copy")
        copy_ps = pixelselection.pixelselectionWhoClass["copy"]
        self.selectWhite()
        self.assertEqual(copy_ps.getObject().len(), 0)
        OOF.PixelSelection.Copy(microstructure="copy", source="5color")
        self.assertEqual(copy_ps.getObject().len(),
                         copy_ps.getObject().len())
        OOF.Microstructure.Delete(microstructure="copy")

    @memorycheck.check("5color")
    def Select_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        self.selectWhite()
        ps_0_id = id(ps.getObject())
        OOF.PixelGroup.New(name="test", microstructure="5color")
        OOF.PixelGroup.AddSelection(microstructure="5color", group="test")
        OOF.PixelSelection.Undo(microstructure="5color")
        OOF.PixelSelection.Group(
            microstructure="5color", group="test", operator=SelectOnly())
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(self.selectionSize(), color_counts["white"])

    @memorycheck.check("5color")
    def Add_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        self.selectWhite()
        OOF.PixelGroup.New(name="test", microstructure="5color")
        OOF.PixelGroup.AddSelection(microstructure="5color", group="test")
        OOF.PixelSelection.Undo(microstructure="5color")
        self.selectBlue(shift=1)
        ps_0_id = id(ps.getObject())
        OOF.PixelSelection.Group(
            microstructure="5color", group="test", operator=Select())
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(self.selectionSize(),
                         color_counts["white"]+color_counts["blue"])
        
    @memorycheck.check("5color")
    def Unselect_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        # Select a bunch of voxels
        self.selectWhite()
        ps_0_id = id(ps.getObject())
        size0 = self.selectionSize()
        # Add them to a group
        OOF.PixelGroup.New(name='test', microstructure='5color')
        OOF.PixelGroup.AddSelection(microstructure='5color', group='test')
        # Select all of the voxels.
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(source='5color:5color')
        OOF.Graphics_1.Toolbox.Pixel_Select.Invert(source='5color:5color')
        ps_1_id = id(ps.getObject())
        size1 = self.selectionSize()
        # Unselect the voxels in the group.
        OOF.PixelSelection.Group(
            microstructure='5color', group='test', operator=Unselect())
        ps_2_id = id(ps.getObject())
        size2 = self.selectionSize()
        self.assertNotEqual(ps_0_id, ps_2_id)
        self.assertNotEqual(ps_1_id, ps_2_id)
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(size1-size0, size2)
        
    @memorycheck.check("5color")
    def Intersect_Group(self):
        ps = pixelselection.pixelselectionWhoClass["5color"]
        self.selectWhite()
        self.selectBlue(shift=1)
        self.assertEqual(self.selectionSize(), 
                         color_counts["white"] + color_counts["blue"])
        OOF.PixelGroup.New(name="test", microstructure="5color")
        OOF.PixelGroup.AddSelection(microstructure="5color", group="test")
        OOF.PixelSelection.Clear(microstructure="5color")
        self.selectYellow()
        self.selectWhite(shift=1)
        self.assertEqual(self.selectionSize(), 
                         color_counts["white"] + color_counts["yellow"])
        ps_0_id = id(ps.getObject())
        OOF.PixelSelection.Group(
            microstructure="5color", group="test", operator=Intersect())
        ps_1_id = id(ps.getObject())
        self.assertNotEqual(ps_0_id, ps_1_id)
        self.assertEqual(self.selectionSize(), color_counts["white"])

    @memorycheck.check("5color")
    def Despeckle(self):
        self.selectWhite()
        # Deselect a point completely within the white region
        self.selectInteriorWhitePoint(ctrl=1) 
        self.assertEqual(self.selectionSize(), color_counts["white"]-1)
        # Despecking with neighbors=26 should reselect just the one point
        OOF.PixelSelection.Despeckle(microstructure="5color", neighbors=26)
        self.assertEqual(self.selectionSize(), color_counts["white"])

    @memorycheck.check("5color")
    def Elkcepsed(self):
        self.selectBlue()
        # Elkcepseding the blue region with neighbors=3 doesn't do anything.
        OOF.PixelSelection.Elkcepsed(microstructure="5color", neighbors=3)
        self.assertEqual(self.selectionSize(), color_counts["blue"])
        # Add an isolated voxel to the selection.
        self.selectInteriorWhitePoint(shift=1)
        self.assertEqual(self.selectionSize(), color_counts["blue"]+1)
        # Elkcepseding deselects just the isolated voxel.
        OOF.PixelSelection.Elkcepsed(microstructure="5color", neighbors=3)
        self.assertEqual(self.selectionSize(), color_counts["blue"])

        # Run Elkcepsed with neighbors=10 on the white voxels.
        OOF.PixelSelection.Clear(microstructure="5color")
        self.selectWhite()
        OOF.PixelSelection.Elkcepsed(microstructure="5color", neighbors=10)
        n1 = self.selectionSize()
        self.assertEqual(n1, 2174)

        OOF.PixelSelection.Clear(microstructure="5color")
        
        # Select a single voxel that is adjacent to 9 white voxels.
        OOF.Image.AutoGroup(image='5color:5color', name_template='%c')
        # ... display the yellow voxels only
        OOF.Graphics_1.Layer.Edit(
            n=0, category='Image', what='5color:5color',
            how=BitmapDisplayMethod(filter=VoxelGroupFilter(group='#f3f359')))
        OOF.Graphics_1.Settings.Camera.View(
            view=View(cameraPosition=Coord(62.2089,-13.7614,-1.56859),
                      focalPoint=Coord(10,10,10), 
                      up=Coord(-0.417769,-0.90834,-0.0196926), angle=30, 
                      clipPlanes=[], invertClip=0))
        # ... and select one of them
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='5color:5color', 
            points=[Point(62.0759,-13.7173,-1.54606)],
            view=View(cameraPosition=Coord(62.2089,-13.7614,-1.56859),
                      focalPoint=Coord(10,10,10),
                      up=Coord(-0.417769,-0.90834,-0.0196926), angle=30,
                      clipPlanes=[], invertClip=0), 
            shift=0, ctrl=0)
        # Select the white voxels too.
        OOF.PixelSelection.Group(
            microstructure='5color', group='#fefefe', operator=Select())
        self.assertEqual(self.selectionSize(), color_counts["white"]+1)
        # Now run Elkcepsed with neighbors=9 again.  The single yellow
        # voxel shouldn't have made a difference.
        OOF.PixelSelection.Elkcepsed(microstructure="5color", neighbors=10)
        self.assertEqual(self.selectionSize(), n1)

    @memorycheck.check("5color")
    def Expand(self):
        self.selectInteriorWhitePoint()
        self.assertEqual(self.selectionSize(), 1)
        # Expanding with a radius of 0.9 doesn't do anything
        OOF.PixelSelection.Expand(microstructure="5color", radius=0.9)
        self.assertEqual(self.selectionSize(), 1)
        # radius=1 selects near neighbors
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.0)
        self.assertEqual(self.selectionSize(), 7)
        OOF.PixelSelection.Undo(microstructure="5color")
        # radius=sqrt(2) selects nearest neighbors and next-nearest
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.415)
        self.assertEqual(self.selectionSize(), 19)
        OOF.PixelSelection.Undo(microstructure="5color")
        # radius=sqrt(3) selects a full 3x3x3 voxel cube
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.733)
        self.assertEqual(self.selectionSize(), 27)
        # Add another layer
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.733)
        self.assertEqual(self.selectionSize(), 125)

    @memorycheck.check("5color")
    def Shrink(self): 
        # A single voxel should vanish.
        self.selectInteriorWhitePoint()
        OOF.PixelSelection.Shrink(microstructure="5color", radius=1.0)
        self.assertEqual(self.selectionSize(), 0)
        # A 3x3x3 cube ...
        self.selectInteriorWhitePoint()
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.733)
        # ... shrinking by 1 produces a 1x1x1 cube
        OOF.PixelSelection.Shrink(microstructure="5color", radius=1.0)
        self.assertEqual(self.selectionSize(), 1)
        # A 5x5x5 cube ...
        self.selectInteriorWhitePoint()
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.733)
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.733)
        # ... shrink by one produces a 3x3x3 cube
        OOF.PixelSelection.Shrink(microstructure="5color", radius=1.0)
        self.assertEqual(self.selectionSize(), 27)
        # 5x5 again
        OOF.PixelSelection.Expand(microstructure="5color", radius=1.733)
        # Shrink by 2 to get back to 1x1x1
        OOF.PixelSelection.Shrink(microstructure="5color", radius=2.0)
        self.assertEqual(self.selectionSize(), 1)

        self.selectWhite()
        OOF.PixelSelection.Shrink(microstructure="5color", radius=1.42)
        self.assertEqual(self.selectionSize(), 253)
        OOF.PixelSelection.Shrink(microstructure="5color", radius=1.)
        self.assertEqual(self.selectionSize(), 5)

    # Color range is a selector, not really a modifer, but there you go.
    @memorycheck.check("5color")
    def Color_Range(self):
        # Select the "white" pixels, which aren't quite white.
        OOF.PixelSelection.Color_Range(
            microstructure='5color', image='5color:5color',
            reference=RGBColor(red=1.00000,green=1.00000,blue=1.00000), 
            range=DeltaGray(delta_gray=0.174603))
        self.assertEqual(self.selectionSize(), color_counts["white"])
        # Fail to select any pixels, by restricting the range.
        OOF.PixelSelection.Color_Range(
            microstructure='5color', image='5color:5color',
            reference=RGBColor(red=1.00000,green=1.00000,blue=1.00000), 
            range=DeltaGray(delta_gray=0.001))
        self.assertEqual(self.selectionSize(), 0)   
        # Select the blue pixels
        OOF.PixelSelection.Color_Range(
            microstructure='5color', image='5color:5color', 
            reference=RGBColor(red=0.00000,green=0.00000,blue=1.00000),
            range=DeltaRGB(delta_red=0.380952,delta_green=0.396825,
                           delta_blue=0.0952381))
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
        self.selectInteriorYellowPoint()
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
        OOF.PixelSelection.Region(
            microstructure='5color',
            shape=BoxSelectionShape(point0=Point(0,0,0),point1=Point(2,3,4)),
            units=PhysicalUnits(),
            operator=Select())
        self.assertEqual(self.selectionSize(), 24)
        OOF.PixelSelection.Region(
            microstructure='5color', 
            shape=BoxSelectionShape(point0=Point(1,1,1),point1=Point(2,3,4)),
            units=PhysicalUnits(),
            operator=SelectOnly())
        self.assertEqual(self.selectionSize(), 6)
        # Only voxels with centers inside the region are selected.
        OOF.PixelSelection.Region(
            microstructure='5color', 
            shape=BoxSelectionShape(point0=Point(0.6,1,1),point1=Point(2,3,4)),
            units=PhysicalUnits(),
            operator=SelectOnly())
        self.assertEqual(self.selectionSize(), 6)
        OOF.PixelSelection.Region(
            microstructure='5color', 
            shape=BoxSelectionShape(point0=Point(0.4,1,1),point1=Point(2,3,4)),
            units=PhysicalUnits(),
            operator=SelectOnly())
        self.assertEqual(self.selectionSize(), 12)
        OOF.PixelSelection.Region(
            microstructure='5color',
            shape=BoxSelectionShape(point0=Point(0,0,0),point1=Point(0,0,0)),
            units=PhysicalUnits(),
            operator=SelectOnly())
        self.assertEqual(self.selectionSize(), 0)

    @memorycheck.check("5color")
    def Circle(self):
        OOF.PixelSelection.Region(
            microstructure='5color',
            shape=CircleSelectionShape(center=Point(10,10,10),radius=0.0),
            units=PhysicalUnits(),
            operator=SelectOnly())
        self.assertEqual(self.selectionSize(), 0)
        # The center is at the corner of 8 voxels. r=sqrt(3)/2 should
        # make the sphere include the centers of all 8.
        OOF.PixelSelection.Region(
            microstructure='5color',
            shape=CircleSelectionShape(center=Point(10,10,10), radius=0.867),
            units=PhysicalUnits(),
            operator=SelectOnly())
        self.assertEqual(self.selectionSize(), 8)
        # Move the center to the center of a voxel.
        OOF.PixelSelection.Region(
            microstructure='5color',
            shape=CircleSelectionShape(center=Point(10.5,10.5,10.5),
                                       radius=0.867),
            units=PhysicalUnits(),
            operator=SelectOnly())
        self.assertEqual(self.selectionSize(), 1)
        OOF.PixelSelection.Region(
            microstructure='5color',
            shape=CircleSelectionShape(center=Point(10.5,10.5,10.5),
                                       radius=1.00001),
            units=PhysicalUnits(),
            operator=SelectOnly())
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
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure', 
            points=[Point(0.342583,0.657046,2.57092)],
            view=View(cameraPosition=Coord(0.5,0.5,3.42583), 
                      focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), 
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=622, size_y=617),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(0.638854,0.619919,2.57092)],
            view=View(cameraPosition=Coord(0.5,0.5,3.42583),
                      focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(0.649249,0.416465,2.57092)],
            view=View(cameraPosition=Coord(0.5,0.5,3.42583),
                      focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(0.398273,0.383051,2.57092)],
            view=View(cameraPosition=Coord(0.5,0.5,3.42583),
                      focalPoint=Coord(0.5,0.5,0.5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617),
            shift=1, ctrl=0)
        OOF.Graphics_1.Settings.Camera.View(
            view=View(cameraPosition=Coord(-0.367231,0.596516,-2.29269),
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(0.237723,0.970497,-0.0402811), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617))
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(-0.364019,0.597374,-2.28699)],
            view=View(cameraPosition=Coord(-0.367231,0.596516,-2.29269),
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(0.237723,0.970497,-0.0402811), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(-0.365889,0.597349,-2.28641)],
            view=View(cameraPosition=Coord(-0.367231,0.596516,-2.29269),
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(0.237723,0.970497,-0.0402811), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(-0.36603,0.595397,-2.28643)],
            view=View(cameraPosition=Coord(-0.367231,0.596516,-2.29269),
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(0.237723,0.970497,-0.0402811), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(-0.364197,0.595208,-2.28701)],
            view=View(cameraPosition=Coord(-0.367231,0.596516,-2.29269),
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(0.237723,0.970497,-0.0402811), angle=30,
                      clipPlanes=[], invertClip=0, size_x=622, size_y=617),
            shift=1, ctrl=0)
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
        OOF.PixelSelection.Group(
            microstructure="microstructure",
            group="pixelgroup",
            operator=SelectOnly())
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
    Direct_Pixel_Selection("PointRotated2"),
    Direct_Pixel_Selection2("PointClipped0"),
    Direct_Pixel_Selection2("PointClipped1"),
    Direct_Pixel_Selection2("PointClipped2"),
    Direct_Pixel_Selection("Clear"),
    #Direct_Pixel_Selection("Brush"),
    #Direct_Pixel_Selection("Rectangle"),
    #Direct_Pixel_Selection("Ellipse"),
    Direct_Pixel_Selection("Color"),
    Direct_Pixel_Selection("ColorRotated"),
    Direct_Pixel_Selection("ColorRotated2"),
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

