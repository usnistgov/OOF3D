# -*- python -*-
# $RCSfile: activearea_test.py,v $
# $Revision: 1.2.16.8 $
# $Author: langer $
# $Date: 2014/09/27 22:34:45 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test suite for active area commands.
# OOF.ActiveArea:
# Override Store Restore Rename Delete
#
# Activate_All
# Activate_Selection_Only
# Activate_Selection
# Activate_Pixel_Group_Only
# Activate_Pixel_Group
# Deactivate_Selection
# Deactivate_Group
# Invert, Copy, Undo, Redo

import unittest
from UTILS.file_utils import reference_file
import memorycheck

# The system starts up with no stored/named active areas, and with all
# pixels in the microstructure active.  Active areas are stored in the
# microstructure object, in an "activearea" attribute, which is a
# WhoDoUndo.

class ActiveArea(unittest.TestCase):
    def setUp(self):
        global microstructure
        from ooflib.common import microstructure
        from ooflib.common.IO import gfxmanager
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data","5color"),
                pattern="slice(0|([1-9][0-9]*))\\.tif",
                sort=NumericalOrder()),
            microstructure_name="active",
            height=20.0, width=20.0, depth=20.0)
        OOF.Image.AutoGroup(image="active:5color")
        OOF.Windows.Graphics.New()
        
    def tearDown(self):
        OOF.Graphics_1.File.Close()

    def getMS(self):
        return microstructure.getMicrostructure("active")

    # Utility function for making a pixel selection.
    def select_pixels(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='active:5color',
            points=[Point(10.0749,10.5779,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10),
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)

        # OOF.Graphics_1.Toolbox.Pixel_Select.Point(
        #     source="active:5color",
        #     points=[Point(8.8,7.3333,5.5)],
        #     shift=0,ctrl=0)

    # Finds the blue and magenta (red) groups.  In principle, it could
    # find all of them, if that were needed.  (Why not just use the
    # hex names that we know from the image?  Was this necessary
    # before we used hex colors for group names?)
    def find_groups(self):
        from ooflib.common import color
        def colordiff(c1,c2):
            return (c1.red-c2.red)**2 + \
                   (c1.green-c2.green)**2 + \
                   (c1.blue-c2.blue)**2
        mdiff = None
        bdiff = None
        red_name = None
        blue_name = None
        for g in self.getMS().groupNames():
            gcolor = color.rgb_from_hex(g)
            cdiff = colordiff(gcolor, color.red)
            if (mdiff is None) or (cdiff < mdiff):
                red_name = g
                mdiff=cdiff
            cdiff = colordiff(gcolor, color.blue)
            if (bdiff is None) or (cdiff < bdiff):
                blue_name = g
                bdiff=cdiff
        return (red_name, blue_name)
                

    # Simplest nontrivial action is to activate a pixel selection.
    @memorycheck.check("active")
    def Activate_Selection_Only(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        self.assertEqual(self.getMS().activearea.size(), 7999)

    # Make sure this sets the flag.  Effects of it are important in
    # the next test.
    @memorycheck.check("active")
    def Override(self):
        OOF.ActiveArea.Override(override=True, microstructure="active")
        self.assert_(self.getMS().activearea.getOverride())
        OOF.ActiveArea.Override(override=False, microstructure="active")
        self.assert_(not self.getMS().activearea.getOverride())
        
    @memorycheck.check("active")
    def Activate_Selection(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Override(override=True, microstructure="active")
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='active:5color',
            points=[Point(5.0,10.,42.)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10),
                      up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0),
            shift=0, ctrl=0)

        OOF.ActiveArea.Activate_Selection(microstructure="active")
        OOF.ActiveArea.Override(override=False, microstructure="active")
        self.assertEqual(self.getMS().activearea.size(), 7998)

    @memorycheck.check("active")
    def Activate_All(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Activate_All(microstructure="active")
        self.assertEqual(self.getMS().activearea.size(), 0)

    ## Tests that check the value of activearea.size() need to
    ## remember that the ActiveArea stores the *inactive* pixels, so
    ## the number checked here is not the number displayed in the GUI.
    ## That number is the total number of voxels (8000 in this case)
    ## minus the number checked here.

    # Our image has been autogrouped, of course...
    @memorycheck.check("active")
    def Activate_Pixel_Group_Only(self):
        (red_name, blue_name) = self.find_groups()
        OOF.ActiveArea.Activate_Pixel_Group_Only(
            microstructure="active", group=red_name)
        self.assertEqual(self.getMS().activearea.size(), 6923)

    @memorycheck.check("active")
    def Activate_Pixel_Group(self):
        (red_name, blue_name) = self.find_groups()
        OOF.ActiveArea.Activate_Pixel_Group_Only(
            microstructure="active", group=red_name)
        OOF.ActiveArea.Activate_Pixel_Group(
            microstructure="active", group=blue_name)
        self.assertEqual(self.getMS().activearea.size(), 5718)
                
    @memorycheck.check("active")
    def Deactivate_Selection(self):
        self.select_pixels()
        OOF.ActiveArea.Deactivate_Selection(microstructure="active")
        self.assertEqual(self.getMS().activearea.size(), 1)

    @memorycheck.check("active")
    def Deactivate_Group(self):
        (red_name, blue_name) = self.find_groups()
        OOF.ActiveArea.Deactivate_Group(microstructure="active",
                                        group=red_name)
        self.assertEqual(self.getMS().activearea.size(), 1077)

    @memorycheck.check("active")
    def Expand(self):
        OOF.ActiveArea.Activate_Pixel_Group_Only(
            microstructure='active', group='#f3f359')
        self.assertEqual(self.getMS().activearea.size(), 5687)
        OOF.ActiveArea.Expand(microstructure="active", radius=1.0)
        self.assertEqual(self.getMS().activearea.size(), 5262)

    @memorycheck.check("active")
    def Shrink(self):
        OOF.ActiveArea.Activate_Pixel_Group_Only(
            microstructure='active', group='#f3f359')
        self.assertEqual(self.getMS().activearea.size(), 5687)
        # You can't disintegrate me!
        OOF.ActiveArea.Shrink(microstructure="active", radius=1.0)
        self.assertEqual(self.getMS().activearea.size(), 6087)
        
    @memorycheck.check("active")
    def Invert(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Invert(microstructure="active")
        self.assertEqual(self.getMS().activearea.size(), 1)

    # Copies between microstructures.
    @memorycheck.check("active", "copy")
    def Copy(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.Microstructure.Copy(microstructure="active", name="copy")
        cms = microstructure.getMicrostructure("copy")
        # Initially-copied MS has default active area.
        self.assertEqual(cms.activearea.size(), 0)
        OOF.ActiveArea.Copy(microstructure="copy", source="active")
        OOF.ActiveArea.Activate_All(microstructure="active")
        self.assertEqual(cms.activearea.size(), 7999)

    @memorycheck.check("active")
    def Undo(self):
        aa1 = self.getMS().activearea.getObject()
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        aa2 = self.getMS().activearea.getObject()
        OOF.ActiveArea.Undo(microstructure="active")
        aa3 = self.getMS().activearea.getObject()
        self.assertEqual(id(aa1),id(aa3))
        self.assertNotEqual(id(aa1),id(aa2))

    @memorycheck.check("active")
    def Redo(self):
        aa1 = self.getMS().activearea.getObject()
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        aa2 = self.getMS().activearea.getObject()
        OOF.ActiveArea.Undo(microstructure="active")
        aa3 = self.getMS().activearea.getObject()
        OOF.ActiveArea.Redo(microstructure="active")
        aa4 = self.getMS().activearea.getObject()
        self.assertEqual(id(aa1),id(aa3))
        self.assertEqual(id(aa2),id(aa4))
        self.assertNotEqual(id(aa1),id(aa2))
    
    # Construction operations.
    @memorycheck.check("active")
    def Store(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Store(microstructure="active", name="test")
        OOF.ActiveArea.Undo(microstructure="active")
        namedAA = self.getMS().namedActiveAreas
        # Make sure it's been stored, and that it's not still active.
        self.assertEqual(len(namedAA),1)
        self.assertEqual(namedAA[0].name(), "test")
        self.assertEqual(self.getMS().activearea.size(),0)

    @memorycheck.check("active")
    def Restore(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Store(microstructure="active", name="test")
        OOF.ActiveArea.Undo(microstructure="active")
        OOF.ActiveArea.Restore(microstructure="active", name="test")
        self.assertEqual(self.getMS().activearea.size(), 7999)
        aa1 = self.getMS().namedActiveAreas[0]
        aa2 = self.getMS().activearea.getObject()
        self.assertEqual(id(aa1),id(aa2))

    @memorycheck.check("active")
    def Rename(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Store(microstructure="active", name="test")
        aa1 = self.getMS().namedActiveAreas[0]
        OOF.ActiveArea.Rename(microstructure="active",
                              oldname="test", newname="rename")
        self.assertEqual(len(self.getMS().namedActiveAreas), 1)
        aa2 = self.getMS().namedActiveAreas[0]
        self.assertEqual(id(aa1),id(aa2))
        self.assertEqual(aa2.name(), "rename")
        
    @memorycheck.check("active")
    def Delete(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Store(microstructure="active", name="test")
        aa1 = self.getMS().namedActiveAreas[0]
        OOF.ActiveArea.Delete(microstructure="active", name="test")
        self.assertEqual(len(self.getMS().namedActiveAreas), 0)


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    ActiveArea("Activate_Selection_Only"),
    ActiveArea("Override"),
    ActiveArea("Activate_Selection"),
    ActiveArea("Activate_All"),
    ActiveArea("Activate_Pixel_Group_Only"),
    ActiveArea("Activate_Pixel_Group"),
    ActiveArea("Deactivate_Selection"),
    ActiveArea("Deactivate_Group"),
    ActiveArea("Expand"),
    ActiveArea("Shrink"),
    ActiveArea("Invert"),
    ActiveArea("Copy"),
    ActiveArea("Undo"),
    ActiveArea("Redo"),
    ActiveArea("Store"),
    ActiveArea("Restore"),
    ActiveArea("Rename"),
    ActiveArea("Delete")
    ]
