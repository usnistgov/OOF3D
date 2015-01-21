# -*- python -*-
# $RCSfile: microstructure_extra_test.py,v $
# $Revision: 1.10 $
# $Author: langer $
# $Date: 2008/09/07 02:19:48 $

# Test suite for the menu commands under OOF.Microstructure.*

import unittest, os, filecmp
import memorycheck


class Microstructure_Extra(unittest.TestCase):
    def setUp(self):
        global microstructure
        from ooflib.common import microstructure
        from ooflib.common.IO import gfxmanager
        OOF.Windows.Graphics.New()

    def tearDown(self):
        OOF.Graphics_1.File.Close()
        
    # Create a microstructure with a pixel group and several categories,
    # and save it, and see if it's the same as the previously-saved version.
    @memorycheck.check("rich")
    def Rich_Save(self):
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="rich",
            height=automatic, width=automatic)
        OOF.Image.AutoGroup(image="rich:small.ppm")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="rich:small.ppm",
            points=[Point(66.0,55.0),Point(87.6,41.8)],
            shift=0, ctrl=0)
        OOF.PixelGroup.New(name="test", microstructure="rich")
        OOF.PixelGroup.AddSelection(microstructure="rich", group="test")
        OOF.Graphics_1.Toolbox.Pixel_Select.Circle(
            source="rich:small.ppm",
            points=[Point(31.2,40.4),Point(60.1,41.2)],
            shift=0,ctrl=0)
        OOF.ActiveArea.Activate_Selection_Only(microstructure="rich")
        OOF.ActiveArea.Store(microstructure="rich", name="act1")
        OOF.Graphics_1.Toolbox.Pixel_Select.Clear(
            source="rich:small.ppm")
        OOF.File.Save.Microstructure(filename="rich_save_test",
                                     mode="w", format="ascii",
                                     microstructure="rich")
        self.assert_(filecmp.cmp("rich_save_test",
                                 os.path.join("ms_data","rich_ms")))
        os.remove("rich_save_test")

    @memorycheck.check("rich")
    def Rich_Load(self):
        OOF.File.Load.Data(filename=os.path.join("ms_data", "rich_ms"))
        ms = microstructure.getMicrostructure("rich")
        group = ms.findGroup("test")
        self.assertEqual(len(group), 2000)

        colorgroups = ms.groupNames()
        colorgroups.remove("test")

        from ooflib.common import color
        def colordiff(c1,c2):
            return (c1.red-c2.red)**2 + \
                   (c1.green-c2.green)**2 + \
                   (c1.blue-c2.blue)**2
        
        # This is a reprise of the AutoGroup test in pixel_test.
        expected_sizes = {color.magenta : 2404,
                          color.RGBColor(1.0,1.0,1.0) : 4781,
                          color.RGBColor(0.0,0.0,0.0) : 2585,
                          color.blue : 2947,
                          color.green : 4795,
                          color.cyan : 1001,
                          color.yellow : 3617,
                          color.red : 370 }

        for name in colorgroups:
            rgb = eval(name)
            key = None
            diff = None
            for c in expected_sizes.keys():
                cdiff = colordiff(rgb,c)
                if (diff is None) or (cdiff < diff):
                    key = c
                    diff = cdiff
            self.assertEqual(len(ms.findGroup(name)), expected_sizes[key])

        # Find the "act1" stored active area, and check the size.
        act1 = ms.getNamedActiveArea("act1")
        self.assertEqual(len(act1.activearea.members()), 19872)
        

def run_tests():
    test_set = [
        Microstructure_Extra("Rich_Save"),
        Microstructure_Extra("Rich_Load")
        ]

    logan = unittest.TextTestRunner()
    for t in test_set:
        print >> sys.stderr, "\n *** Running test: %s\n" % t.id()
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
