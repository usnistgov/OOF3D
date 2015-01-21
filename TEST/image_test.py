# -*- python -*-
# $RCSfile: image_test.py,v $
# $Revision: 1.18 $
# $Author: langer $
# $Date: 2008/09/07 02:19:48 $

# Test suite for the menu commands under OOF.Image.*

# These functions make use of OOF.Microstructure commands as if they
# work -- for proper regression testing, run microstructure_test first,
# then this one.

import unittest, os
import memorycheck

class OOF_Image(unittest.TestCase):
    def setUp(self):
        pass

    # OOF.File.Load.Image loads an image into a microstructure, but
    # the usual way to get them is to create a microstructure from an
    # image file.  There's also an OOF.File.Save.Image that needs testing.
    
    @memorycheck.check("rectangle.ppm")
    def Delete(self):
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","rectangle.ppm"),
            microstructure_name="rectangle.ppm",
            height=automatic, width=automatic)
        OOF.Image.Delete(image="rectangle.ppm:rectangle.ppm")
        ms = getMicrostructure("rectangle.ppm")
        self.assertEqual(len(ms.imageNames()),0)
        self.assertEqual(len(ms.getImageContexts()), 0)

    @memorycheck.check("rectangle.ppm", "other")
    def Copy(self):
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","rectangle.ppm"),
            microstructure_name="rectangle.ppm",
            height=automatic, width=automatic)
        OOF.Microstructure.New(name="other", width=150.0, height=121.0,
                               width_in_pixels=150, height_in_pixels=121)
        OOF.Image.Copy(image="rectangle.ppm:rectangle.ppm",
                       microstructure="other", name=automatic)
        ms_0 = getMicrostructure("rectangle.ppm")
        ms_1 = getMicrostructure("other")
        self.assertEqual(len(ms_1.imageNames()),1)
        self.assert_("rectangle.ppm" in ms_1.imageNames())
        # Ensure they're separate objects.
        self.assertNotEqual(id(ms_0.getImageContexts()[0]),
                            id(ms_1.getImageContexts()[0]))

    @memorycheck.check("rectangle.ppm")
    def Rename(self):
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","rectangle.ppm"),
            microstructure_name="rectangle.ppm",
            height=automatic, width=automatic)
        ms_0 = getMicrostructure("rectangle.ppm")
        image_id = id(ms_0.getImageContexts()[0])
        OOF.Image.Rename(image="rectangle.ppm:rectangle.ppm",
                         name="newname")
        ms_0 = getMicrostructure("rectangle.ppm")
        image_id = id(ms_0.getImageContexts()[0])
        self.assertEqual(len(ms_0.imageNames()),1)
        self.assert_("newname" in ms_0.imageNames())
        self.assertEqual(image_id, id(ms_0.getImageContexts()[0]))

    # This test just checks that the groups are created and add up to
    # the right size.  Group operations are tested in more detail
    # elsewhere.
    @memorycheck.check("rectangle.ppm")
    def AutoGroup(self):
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","rectangle.ppm"),
            microstructure_name="rectangle.ppm",
            height=automatic, width=automatic)
        OOF.Image.AutoGroup(image="rectangle.ppm:rectangle.ppm")
        ms = getMicrostructure("rectangle.ppm")
        self.assertEqual(ms.nGroups(), 7)
        self.assertEqual(ms.nCategories(), 7)
        # Check that the groups add up to the total size.
        size = 0
        for gname in ms.groupNames():
            size += len(ms.findGroup(gname))
        self.assertEqual(size, 121*150) # 121x150 is the size of the image.

    # Test for OOF.File.Image.Save, which is technically not in the
    # OOF.Image menu hierarchy.
    @memorycheck.check("save_test")
    def Save(self):
        import filecmp, os
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","rectangle.ppm"),
            microstructure_name="save_test",
            height=automatic, width=automatic)
        OOF.File.Save.Image(filename="image_save_test",
                            image="save_test:rectangle.ppm")
        self.assert_(filecmp.cmp("image_save_test",
                                 os.path.join("image_data",
                                              "saved_rectangle")))
        os.remove("image_save_test")

    # Test for OOF.File.Image.Load, which is technically not in the
    # OOF.Image menu hierarchy.
    @memorycheck.check("load_test")
    def Load(self):
        OOF.Microstructure.New(name="load_test",
                               width=150, height=121,
                               width_in_pixels=150, height_in_pixels=121)
        OOF.File.Load.Image(filename=os.path.join("ms_data","rectangle.ppm"),
                            microstructure="load_test",
                            height=automatic, width=automatic)
        ms = getMicrostructure("load_test")
        ms_images = ms.imageNames()
        self.assertEqual(len(ms_images),1)
        self.assert_("rectangle.ppm" in ms_images)
        
    @memorycheck.check()
    def Modify(self):
        import filecmp, os, random
        from ooflib.SWIG.common import crandom
        from ooflib.SWIG.image import oofimage
        global image_modify_args
        menuitem = OOF.Image.Modify
        for m in menuitem.items:
            try:
                test_list = image_modify_args[m.name]
            except KeyError:
                print >> sys.stderr, "No test data for image modifier ", m.name
            else:
                for (datafilename, argdict) in test_list:
                    argdict['image']="imagemod_test:image_test.ppm"
                    OOF.Microstructure.Create_From_ImageFile(
                        filename=os.path.join("image_data","image_test.ppm"),
                        microstructure_name="imagemod_test",
                        height=automatic, width=automatic)
                    random.seed(17)
                    crandom.rndmseed(17)
                    m.callWithArgdict(argdict)

                    OOF.Microstructure.Create_From_ImageFile(
                        filename=os.path.join("image_data", datafilename),
                        microstructure_name="comparison",
                        height=automatic, width=automatic)
                    im1 = oofimage.imageContexts[
                        "imagemod_test:image_test.ppm"].getObject()
                    im2 = oofimage.imageContexts[
                        "comparison:"+datafilename].getObject()
                    # Tolerance is 1./65535., which is the level of
                    # "quantization noise" for 16-bit color channels.
                    self.assert_(im1.compare(im2, 1./65535.))
                    
                    OOF.Microstructure.Delete(
                        microstructure="comparison")
                    OOF.Microstructure.Delete(
                        microstructure="imagemod_test")
                
    # Undo and Redo have the "Gray" test hard-coded.  They'd be a tad
    # more flexible if they just used the first test in the list.
    @memorycheck.check("undo_test")
    def Undo(self):
        from ooflib.SWIG.image import oofimage
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("image_data","image_test.ppm"),
            microstructure_name="undo_test",
            height=automatic, width=automatic)
        image_context = oofimage.imageContexts["undo_test:image_test.ppm"]
        im_0 = image_context.getObject()
        self.assert_(not oofimage.undoable("undo_test:image_test.ppm"))
        OOF.Image.Modify.Gray(image="undo_test:image_test.ppm")
        im_1 = image_context.getObject()
        self.assertNotEqual(id(im_0), id(im_1))
        self.assert_(oofimage.undoable("undo_test:image_test.ppm"))
        OOF.Image.Undo(image="undo_test:image_test.ppm")
        im_2 = image_context.getObject()
        self.assertNotEqual(id(im_2), id(im_1))
        self.assertEqual(id(im_0), id(im_2))

    @memorycheck.check("redo_test")
    def Redo(self):
        from ooflib.SWIG.image import oofimage
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("image_data","image_test.ppm"),
            microstructure_name="redo_test",
            height=automatic, width=automatic)
        image_context = oofimage.imageContexts["redo_test:image_test.ppm"]
        OOF.Image.Modify.Gray(image="redo_test:image_test.ppm")
        im_0 = image_context.getObject()
        OOF.Image.Undo(image="redo_test:image_test.ppm")
        OOF.Image.Redo(image="redo_test:image_test.ppm")
        im_1 = image_context.getObject()
        self.assertEqual(id(im_0), id(im_1))
        
    def tearDown(self):
        pass


# Data for the image modifier tests.  This is a dictionary indexed by
# image modifier name, and for each modifier, there is a set of
# arguments to supply to the modifier menu item for the test, and the
# name of a file containing correct results for that test.

# Commented-out entries in this list are modifications provided
# directly by ImageMagick.  These have proven to have some variability
# between different versions of the ImageMagick library, and so cannot
# be reliably tested here.  They're kept in and commented out so we'll
# know we didn't just forget.
image_modify_args = {"Gray" : [ ("gray", {}) ],
                     "Flip" : [ ("flip_x", {"axis" : "x"}),
                                ("flip_y", {"axis" : "y"}),
                                ("flip_xy", {"axis" : "xy"})],
                     "Fade" : [ ("fade", {"factor" : 0.3}) ],
                     "Dim"  : [ ("dim", {"factor" : 0.7}) ],
                     # "Blur" : [ ("blur", {"radius" : 1.0,
                     #                                 "sigma" : 3.0} ) ],
                     # "Despeckle" : [ ("despeckle", {})],
                     # "Edge" : [ ("edge", {"radius" : 0.0})],
                     # "Enhance" : [ ("enhance", {})],
                     # "Equalize" : [ ("equalize", {})],
                     # "MedianFilter" : [ ("median",
                     #                     {"radius" : 1.0}) ],
                     # "Negate" : [("negate", {})],
                     # "Normalize" : [("normalize", {})],
                     # "ReduceNoise" : [("reduce_noise",
                     #                   {"radius" : 1.0})],
                     # "Sharpen" : [("sharpen", {"radius" : 1.0,
                     #                           "sigma" : 3.0})],
                     "Reilluminate" : [("reilluminate", {"radius" : 10})],
                     "CloseImage" : [("closeimage", {"n" : 7})],
                     "Connect_Edges" : [("connect_edges",
                                         {"Threshold" : 0.5, "d" : 7,
                                          "n" : 9, "B" : 5,
                                          "trimYN" : 0, "t" : 0.5})],
                     "SkeletonizeImage" : [("skeletonize", {})],
                     "FullEdgeDetection" : [("fulledgedetection",
                                             {"a": 3, "b": 3, "numAngles" : 6,
                                              "Threshold" : 0.5,
                                              "Line_color" : 2,
                                              "d" : 7, "n" : 9, "B" : 5,
                                              "trimYN" : 0, "t" : 0.5})],
                     "HysteresisThreshold" : [("hysteresisthreshold",
                                               {"T1" : 0.5, "T2" : 0.5})],
                     "ImaginaryGabor" : [("imaginarygabor",
                                          {"a" : 3, "b" : 3,
                                           "numAngles" : 6,
                                           "Threshold" : 0.5} )],
                     "ModifiedGabor" : [("modifiedgabor",
                                         {"a" : 3, "b" : 3,
                                          "numAngles" : 6,
                                          "Threshold" : 0.5} )],
                     "NewGabor" : [("newgabor",
                                    {"a" : 3, "b" : 3,
                                     "numAngles" : 4,
                                     "Threshold" : 0.5,
                                     "Line_color" : 2 } )],
                     "NormalGabor" : [("normalgabor",
                                       {"a" : 3, "b" : 3,
                                        "numAngles" : 6,
                                        "Threshold" : 0.5} )],
                     "RealGabor" : [("realgabor",
                                     {"a" : 3, "b" : 3,
                                      "numAngles" : 6,
                                      "Threshold" : 0.5} )],
                     "ThresholdImage" : [("threshold", {"T" : 0.5})],
                     "Add_Gaussian_Noise" : [("add_gaussian_noise",
                                              {"Standard_deviation" : 0.2})],
                     "Canny" : [("canny", {"stdDev" : 1.0})],
                     "GaussianSmoothing" : [("gaussiansmoothing",
                                             {"stdDev" : 1.0})],
                     "LaplacianFilter" : [("laplacianfilter", {})],
                     "LaplacianGaussFilter" : [("laplaciangaussfilter",
                                                {"stdDev" : 1.0})],
                     "Sobel" : [("sobel", {})],
                     "SpreadDataValues" : [("spreaddatavalues", {"T" : 0.3})],
                     "SpreadDataValues2" : [("spreaddatavalues2",
                                             {"T" : 0.3})]
                     }

# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.
def run_tests():
    test_set = [OOF_Image("Undo"),
                OOF_Image("Redo"),
                OOF_Image("Delete"),
                OOF_Image("Copy"),
                OOF_Image("Rename"),
                OOF_Image("AutoGroup"),
                OOF_Image("Modify")
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
