# -*- python -*-
# $RCSfile: pixel_extra_test.py,v $
# $Revision: 1.5 $
# $Author: langer $
# $Date: 2008/09/08 18:30:07 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

# These tests are "extra" in the sense that they re-run menu items
# which have already been run, but they do so under more challenging
# circumstances than the initial test, or because they rely on other
# features that weren't tested at the time that the first tests were
# run.

import unittest, os
import memorycheck

class OOF_Pixel_Extra(unittest.TestCase):
    def setUp(self):
        global microstructure
        from ooflib.common import microstructure
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="skeltest",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="skeltest:small.ppm")

    @memorycheck.check("skeltest")
    def SelectMaterialPixels(self):
        OOF.Material.New(name='material')
        OOF.Material.Assign(
            material='material', microstructure='skeltest',
                            pixels='RGBColor(red=0.00000,green=0.00000,blue=0.00000)')
        OOF.Material.New(name='otherstuff')
        OOF.Material.Assign(
            material='otherstuff', microstructure='skeltest',
            pixels='RGBColor(red=0.97255,green=0.00000,blue=0.00000)')
        ms = microstructure.microStructures['skeltest']
        pixelselection = ms.getSelectionContext()
        self.assertEqual(pixelselection.size(), 0)
        # Select pixels with either material.
        OOF.PixelSelection.Select_Material(
            microstructure='skeltest', material='<Any>')
        self.assertEqual(pixelselection.size(), 2955)
        # Select pixels with no material.
        OOF.PixelSelection.Clear(microstructure='skeltest')
        OOF.PixelSelection.Select_Material(
            microstructure='skeltest', material='<None>')
        self.assertEqual(pixelselection.size(), 19545)
        # Select pixels with a specified material.
        OOF.PixelSelection.Clear(microstructure='skeltest')
        OOF.PixelSelection.Select_Material(
            microstructure='skeltest', material='material')
        self.assertEqual(pixelselection.size(), 2585)
        # Try again with no materials assigned.  This test is
        # important because it ensures that the iterators are looking
        # at every pixel.
        OOF.Material.Remove(microstructure='skeltest', pixels=all)
        OOF.PixelSelection.Clear(microstructure='skeltest')
        OOF.PixelSelection.Select_Material(
            microstructure='skeltest', material='<Any>')
        self.assertEqual(pixelselection.size(), 0)
        OOF.PixelSelection.Clear(microstructure='skeltest')
        OOF.PixelSelection.Select_Material(
            microstructure='skeltest', material='<None>')
        self.assertEqual(pixelselection.size(), 22500)
        OOF.PixelSelection.Clear(microstructure='skeltest')
        OOF.PixelSelection.Select_Material(
            microstructure='skeltest', material='material')
        self.assertEqual(pixelselection.size(), 0)
        
    

def run_tests():

    test_set = [
        OOF_Pixel_Extra("SelectMaterialPixels")
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
