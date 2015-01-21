# -*- python -*-
# $RCSfile: activearea_test.py,v $
# $Revision: 1.9 $
# $Author: langer $
# $Date: 2008/09/07 02:19:48 $

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
# Expand, Shrink, Invert, Copy, Undo, Redo

import unittest, os, filecmp
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
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="active",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="active:small.ppm")
        OOF.Windows.Graphics.New()

    def ms(self):
        # We can't just set a data member self.ms in setUp, because it
        # would hold a reference to the microstructure and would make
        # the memorychecks fail.
        return microstructure.getMicrostructure("active")
        
    def tearDown(self):
        OOF.Graphics_1.File.Close()

    # Utility function for making a pixel selection.
    def select_pixels(self):
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="active:small.ppm",
            points=[Point(8.8,7.3333), Point(11.68,5.5733)],
            shift=0,ctrl=0)

    # Finds the blue and magenta groups.  In principle, it could find
    # all of them, if that were needed.
    def find_groups(self):
        from ooflib.common import color
        def colordiff(c1,c2):
            return (c1.red-c2.red)**2 + \
                   (c1.green-c2.green)**2 + \
                   (c1.blue-c2.blue)**2
        # Find the magenta group, and select it.
        mdiff = None
        bdiff = None
        magenta_name = None
        blue_name = None
        for g in self.ms().groupNames():
            gcolor = eval(g)
            cdiff = colordiff(gcolor, color.magenta)
            if (mdiff is None) or (cdiff < mdiff):
                magenta_name = g
                mdiff=cdiff
            cdiff = colordiff(gcolor, color.blue)
            if (bdiff is None) or (cdiff < bdiff):
                blue_name = g
                bdiff=cdiff
        return (magenta_name, blue_name)
                

    # Simplest nontrivial action is to activate a pixel selection.
    @memorycheck.check("active")
    def Activate_Selection_Only(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 20500)

    # Make sure this sets the flag.  Effects of it are important in
    # the next test.
    @memorycheck.check("active")
    def Override(self):
        OOF.ActiveArea.Override(override=True, microstructure="active")
        self.assert_(self.ms().activearea.getOverride())
        OOF.ActiveArea.Override(override=False, microstructure="active")
        self.assert_(not self.ms().activearea.getOverride())
        
    
    @memorycheck.check("active")
    def Activate_Selection(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Override(override=True, microstructure="active")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="active:small.ppm",
            points=[Point(11.68,5.5733), Point(8.8, 7.3333)],
            shift=0, ctrl=0)
        OOF.ActiveArea.Activate_Selection(microstructure="active")
        OOF.ActiveArea.Override(override=False, microstructure="active")
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 19270)

    @memorycheck.check("active")
    def Activate_All(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Activate_All(microstructure="active")
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 0)

    # Our image has been autogrouped, of course...
    @memorycheck.check("active")
    def Activate_Pixel_Group_Only(self):
        (magenta_name, blue_name) = self.find_groups()
        OOF.ActiveArea.Activate_Pixel_Group_Only(
            microstructure="active", group=magenta_name)
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 20096)

    @memorycheck.check("active")
    def Activate_Pixel_Group(self):
        (magenta_name, blue_name) = self.find_groups()
        OOF.ActiveArea.Activate_Pixel_Group_Only(
            microstructure="active", group=magenta_name)
        OOF.ActiveArea.Activate_Pixel_Group(
            microstructure="active", group=blue_name)
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 17149)
                
    @memorycheck.check("active")
    def Deactivate_Selection(self):
        self.select_pixels()
        OOF.ActiveArea.Deactivate_Selection(microstructure="active")
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 2000)

    @memorycheck.check("active")
    def Deactivate_Group(self):
        (magenta_name, blue_name) = self.find_groups()
        OOF.ActiveArea.Deactivate_Group(microstructure="active",
                                        group=magenta_name)
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 2404)

    @memorycheck.check("active")
    def Expand(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Expand(microstructure="active", radius=1.0)
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 22500-2144)

    @memorycheck.check("active")
    def Shrink(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        # You can't disintegrate me!
        OOF.ActiveArea.Shrink(microstructure="active", radius=1.0)
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 22500-1860)
        
    @memorycheck.check("active")
    def Invert(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Invert(microstructure="active")
        inactive_pixels = self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 22500-20500)


    # Copies between microstructures.
    @memorycheck.check("active", "copy")
    def Copy(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.Microstructure.Copy(microstructure="active", name="copy")
        cms = microstructure.getMicrostructure("copy")
        # Initially-copied MS has default active area.
        self.assertEqual(len(cms.activearea.getSelection()), 0)
        OOF.ActiveArea.Copy(microstructure="copy", source="active")
        OOF.ActiveArea.Activate_All(microstructure="active")
        self.assertEqual(len(cms.activearea.getSelection()), 20500)

    @memorycheck.check("active")
    def Undo(self):
        aa1 = self.ms().activearea.getObject()
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        aa2 = self.ms().activearea.getObject()
        OOF.ActiveArea.Undo(microstructure="active")
        aa3 = self.ms().activearea.getObject()
        self.assertEqual(id(aa1),id(aa3))
        self.assertNotEqual(id(aa1),id(aa2))

    @memorycheck.check("active")
    def Redo(self):
        aa1 = self.ms().activearea.getObject()
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        aa2 = self.ms().activearea.getObject()
        OOF.ActiveArea.Undo(microstructure="active")
        aa3 = self.ms().activearea.getObject()
        OOF.ActiveArea.Redo(microstructure="active")
        aa4 = self.ms().activearea.getObject()
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
        names = self.ms().namedActiveAreas
        # Make sure it's been stored, and that it's not still active.
        self.assertEqual(len(names),1)
        self.assertEqual(names[0].name, "test")
        self.assertEqual(len(self.ms().activearea.getSelection()),0)

    @memorycheck.check("active")
    def Restore(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Store(microstructure="active", name="test")
        OOF.ActiveArea.Undo(microstructure="active")
        OOF.ActiveArea.Restore(microstructure="active", name="test")
        inactive_pixels=self.ms().activearea.getSelection()
        self.assertEqual(len(inactive_pixels), 20500)
        aa1 = self.ms().namedActiveAreas[0].activearea
        aa2 = self.ms().activearea.getObject()
        self.assertEqual(id(aa1),id(aa2))


    @memorycheck.check("active")
    def Rename(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Store(microstructure="active", name="test")
        aa1 = self.ms().namedActiveAreas[0]
        OOF.ActiveArea.Rename(microstructure="active",
                              oldname="test", newname="rename")
        self.assertEqual(len(self.ms().namedActiveAreas), 1)
        aa2 = self.ms().namedActiveAreas[0]
        self.assertEqual(id(aa1.activearea),id(aa2.activearea))
        self.assertEqual(aa2.name, "rename")
        

    @memorycheck.check("active")
    def Delete(self):
        self.select_pixels()
        OOF.ActiveArea.Activate_Selection_Only(microstructure="active")
        OOF.ActiveArea.Store(microstructure="active", name="test")
        aa1 = self.ms().namedActiveAreas[0]
        OOF.ActiveArea.Delete(microstructure="active", name="test")
        self.assertEqual(len(self.ms().namedActiveAreas), 0)


        

def run_tests():
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
