# -*- python -*-
# $RCSfile: skeleton_basic_test.py,v $
# $Revision: 1.1.2.22 $
# $Author: langer $
# $Date: 2014/12/08 20:15:34 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Test suite for the menu commands under OOF.Skeleton.* Namely, New,
# Simple, Delete, Copy, Rename, Modify, Undo, Redo, but not including
# PinNodes or Boundary, which are done in other files.

# This file assumes that microstructures, images, and pixel group menu
# items have all been tested and work.

import unittest, os
import memorycheck
from UTILS import file_utils
file_utils.generate = False
reference_file = file_utils.reference_file

class OOF_Skeleton(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        global cskeletonnode2, cskeletonelement
        from ooflib.SWIG.engine import cskeletonnode2
        from ooflib.SWIG.engine import cskeletonelement
        global cmicrostructure
        from ooflib.SWIG.common import cmicrostructure
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data","5color"),
                pattern="slice(0|([1-9][0-9]*))\\.tif",
                sort=NumericalOrder()),
            microstructure_name="skeltest",
            height=20.0, width=20.0, depth=20.0)
        OOF.Image.AutoGroup(image="skeltest:5color", name_template='%c')

    @memorycheck.check("skeltest")
    def New(self):
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        from ooflib.common.IO import parameter
        self.assertRaises(
            parameter.ParameterMismatch,
            OOF.Skeleton.New,
            name='ske:leton',
            microstructure='5color',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate')
            )
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))

        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:skeleton"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 125)
        self.assertEqual(skel.nelements(), 320)
        self.assertEqual(skel.nfaces(), 736)
        self.assertEqual(skel.nsegments(), 540)
        self.assert_(skelctxt.sanity_check())

    @memorycheck.check("skeltest")
    def New2(self):
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        from ooflib.common.IO import parameter
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='middling'))

        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:skeleton"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 125)
        self.assertEqual(skel.nelements(), 320)
        self.assertEqual(skel.nfaces(), 736)
        self.assertEqual(skel.nsegments(), 540)
        self.assert_(skelctxt.sanity_check())
        
    @memorycheck.check("skeltest")
    def Delete(self):
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Skeleton.Delete(skeleton="skeltest:skeleton")
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)

    # Check that the LabelTree in the Who class works correctly.
    @memorycheck.check("m")
    def LabelTree(self):
        OOF.Microstructure.Delete(microstructure="skeltest")
        # First check for errors when the tree is empty
        self.assertRaises(KeyError,
                          skeletoncontext.skeletonContexts.__getitem__, "m")
        self.assertRaises(KeyError,
                          skeletoncontext.skeletonContexts.__getitem__, "m:s")
        OOF.Microstructure.New(
            name="m",
            width=4.0, height=5.0, depth=6.0,
            width_in_pixels=120, height_in_pixels=100, depth_in_pixels=120)
        OOF.Skeleton.New(
            name='s',
            microstructure='m',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='middling'))
        # This shouldn't raise an exception:
        mic = skeletoncontext.skeletonContexts["m:s"]
        # But these should:
        self.assertRaises(KeyError,
                          skeletoncontext.skeletonContexts.__getitem__, "m")
        self.assertRaises(KeyError,
                          skeletoncontext.skeletonContexts.__getitem__, "mm")
        self.assertRaises(KeyError,
                          skeletoncontext.skeletonContexts.__getitem__, "mm:s")
        self.assertRaises(KeyError,
                          skeletoncontext.skeletonContexts.__getitem__, "m:s:M")


    @memorycheck.check("skeltest")
    def Simple(self):
        OOF.Skeleton.Simple(
            name="simple",
            microstructure="skeltest",
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:simple"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nelements(), 40000)
        self.assertEqual(skel.nnodes(), 9261)
        self.assertEqual(skel.nfaces(), 82400)
        self.assertEqual(skel.nsegments(), 51660)
        # No sanity check here, because it takes too long.  The simple
        # skeleton uses the same code as the regular skeleton, so
        # checking shouldn't be necessary.

    @memorycheck.check("skeltest")
    def Copy(self):
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Skeleton.Copy(skeleton="skeltest:skeleton",
                          name="copy")
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 2)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:copy"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 125)
        self.assertEqual(skel.nelements(), 320)
        self.assertEqual(skel.nfaces(), 736)
        self.assertEqual(skel.nsegments(), 540)
        self.assert_(skelctxt.sanity_check())

    @memorycheck.check("skeltest")
    def Rename(self):
        OOF.Skeleton.New(
            name="skeleton", microstructure="skeltest",
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Skeleton.Rename(skeleton="skeltest:skeleton",
                            name="rename")
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        skelctxt = skeletoncontext.skeletonContexts["skeltest:rename"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 125)
        self.assertEqual(skel.nelements(), 320)
        self.assertEqual(skel.nfaces(), 736)
        self.assertEqual(skel.nsegments(), 540)
        self.assert_(skelctxt.sanity_check())

    @memorycheck.check("skeltest")
    def Save(self):
        OOF.Skeleton.New(
            name="savetest", microstructure="skeltest",
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.File.Save.Skeleton(filename="skeleton_save",
                               mode="w", format="ascii",
                               skeleton="skeltest:savetest")
        self.assert_(file_utils.fp_file_compare(
                "skeleton_save",
                os.path.join("skeleton_data", "savetest"),
                1.e-9))
        file_utils.remove("skeleton_save")

    @memorycheck.check("skeltest")
    def Load(self):
        OOF.File.Load.Data(filename=reference_file("skeleton_data",
                                                   "savetest"))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        self.assert_( ["skeltest", "savetest"] in
                      skeletoncontext.skeletonContexts.keys())
        skelctxt = skeletoncontext.skeletonContexts["skeltest:savetest"]
        skel = skelctxt.getObject()
        self.assertEqual(skel.nnodes(), 125)
        self.assertEqual(skel.nelements(), 320)
        self.assertEqual(skel.nfaces(), 736)
        self.assertEqual(skel.nsegments(), 540)
        self.assert_(skelctxt.sanity_check())
        
    def tearDown(self):
         pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#


# Extra tests that can't be in OOF_Skeleton for one reason or another.

class OOF_Skeleton_Special(unittest.TestCase):
    def setUp(self):
        global skeletoncontext, cskeletonnode2, cskeletonelement
        from ooflib.SWIG.engine import cskeletonelement
        from ooflib.SWIG.engine import cskeletonnode2
        from ooflib.engine import skeletoncontext
        global microstructure, cmicrostructure
        from ooflib.common import microstructure
        from ooflib.SWIG.common import cmicrostructure
        global imagecontext
        from ooflib.image import imagecontext

    def tearDown(self):
        pass

    # Now that skeletons are known to work, we can test if deleting a
    # microstructure which contains a skeleton does the right thing.
    # This test is pretty much redundant with the tests inserted by
    # the memorycheck decorator.

    def MS_Delete(self):
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data","5color"),
                pattern="slice(0|([1-9][0-9]*))\\.tif",
                sort=NumericalOrder()),
            microstructure_name="deltest",
            height=20.0, width=20.0, depth=20.0)
        OOF.Image.AutoGroup(image="deltest:5color")
        OOF.Skeleton.New(
            name="skeleton", microstructure="deltest",
            x_elements=3, y_elements=3, z_elements=3,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 1)
        OOF.Microstructure.Delete(microstructure="deltest")
        self.assertEqual(microstructure.microStructures.nActual(), 0)
        self.assertEqual(skeletoncontext.skeletonContexts.nActual(), 0)
        self.assertEqual(imagecontext.imageContexts.nActual(), 0)
        self.assertEqual(cskeletonnode2.get_globalNodeCount(), 0)
        self.assertEqual(cskeletonelement.get_globalElementCount(), 0)
        self.assertEqual(cmicrostructure.get_globalMicrostructureCount(), 0)


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    OOF_Skeleton("New"),
    OOF_Skeleton("New2"),
    OOF_Skeleton("Delete"),
    OOF_Skeleton("LabelTree"),
    OOF_Skeleton("Simple"),
    OOF_Skeleton("Copy"),
    OOF_Skeleton("Rename"),
    OOF_Skeleton("Save"),
    OOF_Skeleton("Load"),
    OOF_Skeleton_Special("MS_Delete"),
    ]
    
