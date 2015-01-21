# -*- python -*-
# $RCSfile: image_test.py,v $
# $Revision: 1.2.16.17 $
# $Author: fyc $
# $Date: 2014/07/30 20:24:38 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Test suite for the menu commands under OOF.Image.*

# These functions make use of OOF.Microstructure commands as if they
# work -- for proper regression testing, run microstructure_test first,
# then this one.

import unittest, os
import memorycheck

from UTILS import file_utils
reference_file = file_utils.reference_file
binary_file_compare = file_utils.binary_file_compare


class OOF_Image(unittest.TestCase):
    def setUp(self):
        global primitives, imagecontext
        from ooflib.common import primitives
        from ooflib.image import imagecontext

    # OOF.File.Load.Image loads an image into a microstructure, but
    # the usual way to get them is to create a microstructure from an
    # image file.  There's also an OOF.File.Save.Image that needs testing.

    @memorycheck.check("jpeg")
    def CreateMSDirectory1(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data", "jpeg"),
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        self.assertEqual(getMicrostructure("jpeg").sizeInPixels(),
                         (100, 100, 100))
        self.assertEqual(getMicrostructure("jpeg").sizeOfPixels(),
                         (1., 1., 1.))
        self.assertEqual(getMicrostructure("jpeg").size(),
                         primitives.Point(100., 100., 100.))
        images = getMicrostructure("jpeg").imageNames()
        self.assert_("jpeg" in images)
        self.assertEqual(len(images), 1)

    @memorycheck.check("jpeg")
    def CreateMSDirectory2(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data", "jpeg"),
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=1.0, width=2.0, depth=3.0)
        self.assertEqual(getMicrostructure("jpeg").sizeInPixels(),
                         (100, 100, 100))
        self.assertEqual(getMicrostructure("jpeg").sizeOfPixels(),
                         (0.02, 0.01, 0.03)) # width, height, depth
        images = getMicrostructure("jpeg").imageNames()
        self.assert_("jpeg" in images)
        self.assertEqual(len(images), 1)

    @memorycheck.check("jpeg")
    def CreateMSPattern1(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data", 'jpeg'),
                pattern='slice\\.jpg\\.(0|([1-9][0-9]*))$',
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        self.assertEqual(getMicrostructure("jpeg").sizeInPixels(),
                         (100, 100, 100))
        images = getMicrostructure("jpeg").imageNames()
        self.assert_("jpeg" in images)
        self.assertEqual(len(images), 1)

    @memorycheck.check("jpeg")
    def CreateMSPattern2(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data", 'jpeg'),
                pattern='slice.jpg.[0-9][0-9]',
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        self.assertEqual(getMicrostructure("jpeg").sizeInPixels(),
                         (100, 100, 90))
        images = getMicrostructure("jpeg").imageNames()
        self.assert_("jpeg" in images)
        self.assertEqual(len(images), 1)

    @memorycheck.check()
    def CreateMSErrors(self):
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Microstructure.Create_From_ImageFile,
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data", 'jpeg'),
                pattern='slouse.jpig.[0-9]+',
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Microstructure.Create_From_ImageFile,
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data", "empty"),
                sort=NumericalOrder()),
            microstructure_name="empty",
            height=automatic, width=automatic, depth=automatic)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Microstructure.Create_From_ImageFile,
            filenames=ThreeDImageList(
                directory=reference_file('ms_data', 'jpeg'),
                files=['slice.jpg.0', 'slouse.jpig.1', 'slice.jpg.10'],
                sort=NumericalOrder()),
            microstructure_name="micro",
            height=automatic, width=automatic, depth=automatic)

    @memorycheck.check("jpeg")
    def CreateMSList(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageList(
                directory=reference_file('ms_data', 'jpeg'),
                files=['slice.jpg.0', 'slice.jpg.20', 'slice.jpg.32'],
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        self.assertEqual(getMicrostructure("jpeg").sizeInPixels(),
                         (100, 100, 3))
        images = getMicrostructure("jpeg").imageNames()
        self.assert_("jpeg" in images)
        self.assertEqual(len(images), 1)

    @memorycheck.check("new")
    def CreateMSFromImage(self):
        from ooflib.common import primitives
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data","jpeg"),
                sort=NumericalOrder()),
            microstructure_name=automatic,
            height=20.0, width=20.0, depth=20.0)
        OOF.Microstructure.Create_From_Image(
            name="new", width=automatic, height=automatic,
            image="jpeg:jpeg")
        ms_0 = getMicrostructure("jpeg")
        ms_1 = getMicrostructure("new")
        # Ensure images are separate objects.
        ms_1_image_id = id(ms_1.getImageContexts()[0])
        # Make sure the image wasn't copied in the source microstructure.
        self.assertEqual(len(ms_0.imageNames()), 1)
        # Make sure the newly constructed microstructure is the right size.
        self.assertEqual(ms_1.sizeInPixels(), primitives.iPoint(100,100,100))
        self.assertEqual(ms_1.size(), primitives.Point(20.0, 20.0, 20.0))
        self.assertEqual(ms_1.sizeOfPixels(), (20.0/100, 20.0/100, 20.0/100))
        OOF.Microstructure.Delete(microstructure="jpeg")
        # Ensure that after the originating microstructure has been
        # deleted, the derived one still has the same image.
        self.assert_("jpeg" in ms_1.imageNames())
        self.assertEqual(ms_1_image_id, id(ms_1.getImageContexts()[0]))
        

    @memorycheck.check("jpeg")
    def Delete(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data", "jpeg"),
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        images = getMicrostructure("jpeg").imageNames()
        self.assert_("jpeg" in images)
        self.assertEqual(len(images), 1)
        OOF.Image.Delete(image="jpeg:jpeg")
        ms = getMicrostructure("jpeg")
        self.assertEqual(len(ms.imageNames()),0)
        self.assertEqual(len(ms.getImageContexts()), 0)
        
    @memorycheck.check("jpeg", "other")
    def Copy(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data", "jpeg"),
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        OOF.Microstructure.New(name="other", width=100.0,
                               height=100.0, depth=100.0,
                               width_in_pixels=100,
                               height_in_pixels=100,
                               depth_in_pixels=100)
        OOF.Image.Copy(
            image="jpeg:jpeg",
            microstructure="other",
            name=automatic)
        ms_0 = getMicrostructure("jpeg")
        ms_1 = getMicrostructure("other")
        self.assertEqual(len(ms_1.imageNames()),1)
        self.assert_("jpeg" in ms_1.imageNames())
        # Ensure they're separate objects.
        self.assertNotEqual(id(ms_0.getImageContexts()[0]),
                            id(ms_1.getImageContexts()[0]))

    @memorycheck.check("jpeg")
    def Rename(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data", "jpeg"),
                sort=NumericalOrder()),
            microstructure_name='jpeg',
            height=automatic, width=automatic, depth=automatic)
        ms_0 = getMicrostructure("jpeg")
        image_id = id(ms_0.getImageContexts()[0])
        OOF.Image.Rename(
            image="jpeg:jpeg",
            name="newname")
        ms_0 = getMicrostructure("jpeg")
        image_id = id(ms_0.getImageContexts()[0])
        self.assertEqual(len(ms_0.imageNames()),1)
        self.assert_("newname" in ms_0.imageNames())
        self.assertEqual(image_id, id(ms_0.getImageContexts()[0]))

    # This test just checks that the groups are created and add up to
    # the right size.  Group operations are tested in more detail
    # elsewhere.
    @memorycheck.check("slice*.tif")
    def AutoGroup(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data","5color"),
                pattern=r"slice(0|([1-9][0-9]*))\.tif",
                sort=NumericalOrder()),
            microstructure_name="slice*.tif",
            height=automatic, width=automatic, depth=automatic)
        OOF.Image.AutoGroup(image="slice*.tif:5color")
        ms = getMicrostructure("slice*.tif")
        self.assertEqual(ms.nGroups(), 5)
        self.assertEqual(ms.nCategories(), 5)
        # Check that the groups add up to the total size.
        size = 0
        for gname in ms.groupNames():
            size += len(ms.findGroup(gname))
        self.assertEqual(size, 20*20*20)

    # Test for OOF.File.Image.Save, which is technically not in the
    # OOF.Image menu hierarchy.  This also tests that tif and png
    # versions of the same image are read identically. 
    @memorycheck.check()
    def Save(self):
        self._Save("slice(0|([1-9][0-9]*))\\.tif")
        self._Save("slice(0|([1-9][0-9]*))\\.png")
    def _Save(self, pattern):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data", "5color"),
                pattern=pattern,
                sort=NumericalOrder()),
            microstructure_name='save_test',
            height=automatic, width=automatic, depth=automatic)
        OOF.File.Save.Image(filename="image_save_test_%i",
                            image="save_test:5color",
                            format="pnm")
        for i in xrange(20):
            filename = "image_save_test_%d" % i
            self.assert_(binary_file_compare(
                filename, 
                os.path.join("image_data", "saved_image_%d"%i)))
            file_utils.remove(filename)
        OOF.Microstructure.Delete(microstructure="save_test")

    # Test for OOF.File.Image.Load, which is technically not in the
    # OOF.Image menu hierarchy.
    @memorycheck.check("load_test")
    def Load(self):
        OOF.Microstructure.New(name="load_test", width=100,
                               height=100, depth=100,
                               width_in_pixels=100,
                               height_in_pixels=100,
                               depth_in_pixels=100)
        OOF.File.Load.Image(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data","jpeg"),
                sort=NumericalOrder()),
            microstructure="load_test",
            height=automatic, width=automatic, depth=automatic)
        ms = getMicrostructure("load_test")
        ms_images = ms.imageNames()
        self.assertEqual(len(ms_images),1)
        self.assert_("jpeg" in ms_images)

    ## Check that an Image saved in a Microstructure data file is
    ## loaded properly.
    @memorycheck.check("5color", "original", "original<2>")
    def LoadFromMicrostructureFile(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file('ms_data','5color'),
                pattern='slice(0|([1-9][0-9]*))\\.png',
                sort=NumericalOrder()),
            microstructure_name='5color',
            height=automatic, width=automatic, depth=automatic)
        for frmt in ('ascii', 'binary'):
            OOF.File.Save.Microstructure(
                filename='testms.dat', mode='w', format=frmt,
                microstructure='5color')
            OOF.Microstructure.Rename(
                microstructure='5color', name='original')
            OOF.File.Load.Data(filename='testms.dat')
            im1 = imagecontext.imageContexts['5color:5color'].getObject()
            im2 = imagecontext.imageContexts['original:5color'].getObject()
            self.assert_(im1.compare(im2, 0))
            os.remove('testms.dat')
                            
    @memorycheck.check()
    def Modify(self):
        global image_modify_args
        menuitem = OOF.Image.Modify
        for m in menuitem.items:
            try:
                test_list = image_modify_args[m.name]
            except KeyError:
                print "No test data for image modifier ", m.name
            else:
                for (datadirname, argdict) in test_list:
                    argdict['image']="imagemod_test:5color"
                    OOF.Microstructure.Create_From_ImageFile(
                        filenames=ThreeDImagePattern(
                            directory=reference_file("ms_data","5color"),
                            pattern="slice(0|([1-9][0-9]*))\\.tif",
                            sort=NumericalOrder()),
                        microstructure_name="imagemod_test",
                        height=automatic, width=automatic, depth=automatic)

                    m.callWithArgdict(argdict)

                    OOF.Microstructure.Create_From_ImageFile(
                        filenames=ThreeDImageDirectory(
                            directory=reference_file("image_data", datadirname),
                            sort=NumericalOrder()),
                        microstructure_name="comparison",
                        height=automatic, width=automatic, depth=automatic)
                    im1 = imagecontext.imageContexts[
                        "imagemod_test:5color"].getObject()
                    im2 = imagecontext.imageContexts[
                        "comparison:"+datadirname].getObject()
                    # Tolerance is 1./65535., which is the level of
                    # "quantization noise" for 16-bit color channels.
                    ## TODO 3.1: For vtk images, tolerance should be
                    ## 1./255.  Why does 1./65535 work?  Does 0 work?
                    self.assert_(im1.compare(im2, 0./65535.))
                    
                    OOF.Microstructure.Delete(
                        microstructure="comparison")
                    OOF.Microstructure.Delete(
                        microstructure="imagemod_test")
                
    # Undo and Redo have the "Gray" test hard-coded.  They'd be a tad
    # more flexible if they just used the first test in the list.

    @memorycheck.check("undo_test")
    def Undo(self):
        from ooflib.SWIG.image import oofimage3d
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data","jpeg"),
                sort=NumericalOrder()),
            microstructure_name="undo_test",
            height=automatic, width=automatic, depth=automatic)
        image_context = imagecontext.imageContexts["undo_test:jpeg"]
        im_0 = image_context.getObject()
        self.assert_(not oofimage3d.undoable("undo_test:jpeg"))
        OOF.Image.Modify.Gray(image="undo_test:jpeg")
        im_1 = image_context.getObject()
        self.assertNotEqual(id(im_0), id(im_1))
        self.assert_(oofimage3d.undoable("undo_test:jpeg"))
        OOF.Image.Undo(image="undo_test:jpeg")
        im_2 = image_context.getObject()
        self.assertNotEqual(id(im_2), id(im_1))
        self.assertEqual(id(im_0), id(im_2))
                     
    @memorycheck.check("redo_test")
    def Redo(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file("ms_data","jpeg"),
                sort=NumericalOrder()),
            microstructure_name="redo_test",
            height=automatic, width=automatic, depth=automatic)
        image_context = imagecontext.imageContexts["redo_test:jpeg"]
        OOF.Image.Modify.Gray(image="redo_test:jpeg")
        im_0 = image_context.getObject()
        OOF.Image.Undo(image="redo_test:jpeg")
        OOF.Image.Redo(image="redo_test:jpeg")
        im_1 = image_context.getObject()
        self.assertEqual(id(im_0), id(im_1))
        
    def tearDown(self):
        pass


# Data for the image modifier tests.  This is a dictionary indexed by
# image modifier name, and for each modifier, there is a set of
# arguments to supply to the modifier menu item for the test, and the
# name of a file containing correct results for that test.


image_modify_args = {"Gray" : [ ("gray", {}) ],
                     "Flip" : [ ("flip_x", {"axis" : "x"}),
                                ("flip_y", {"axis" : "y"}),
                                ("flip_xy", {"axis" : "xy"}),
                                ("flip_yz", {"axis" : "yz"}),
                                ("flip_xz", {"axis" : "xz"}),
                                ("flip_xyz", {"axis" : "xyz"})],
                     "Fade" : [ ("fade", {"factor" : 0.3}) ],
                     "Dim"  : [ ("dim", {"factor" : 0.7}) ],
                     ## Blur and Normalize fail though the output
                     ## appears correct. Either these methods are VTK
                     ## version dependent, system dependent, or
                     ## something.
                     #"Blur" : [ ("blur*", {"radius" : 1.0, "sigma" : 3.0} ) ],
                     "Contrast" : [("contrast", {"factor" : 1.6})],
                     "MedianFilter" : [ ("median", {"radius" : 1}) ],
                     "Negate" : [("negate", {})],
                     #"Normalize" : [("normalize*", {})],
                     "ThresholdImage" : [("threshold", {"T" : 0.5})],
                     }

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    OOF_Image("CreateMSDirectory1"),
    OOF_Image("CreateMSDirectory2"),
    OOF_Image("CreateMSPattern1"),
    OOF_Image("CreateMSPattern2"),
    OOF_Image("CreateMSErrors"),
    OOF_Image("CreateMSList"),
    OOF_Image("CreateMSFromImage"),
    OOF_Image("Delete"),
    OOF_Image("Copy"),
    OOF_Image("Rename"),
    OOF_Image("Save"),
    OOF_Image("Load"),
    OOF_Image('LoadFromMicrostructureFile'),
    OOF_Image("AutoGroup"),
    OOF_Image("Modify"),
    OOF_Image("Undo"),
    OOF_Image("Redo"),
    ]

#test_set = [OOF_Image("LoadFromMicrostructureFile")]
