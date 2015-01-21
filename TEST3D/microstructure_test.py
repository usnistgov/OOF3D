# -*- python -*-
# $RCSfile: microstructure_test.py,v $
# $Revision: 1.2.16.10 $
# $Author: langer $
# $Date: 2014/12/08 19:43:08 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test suite for the menu commands under OOF.Microstructure.*

import unittest, os
import memorycheck

from UTILS import file_utils
reference_file = file_utils.reference_file

class OOF_Microstructure(unittest.TestCase):
    def setUp(self):
        global microstructure
        global ooferror
        from ooflib.common import microstructure
        from ooflib.SWIG.common import ooferror

    # Don't run memorycheck.check on New, because it needs to leave a
    # Microstructure behind for Delete.
    def New(self):
        from ooflib.common import primitives
        self.assertRaises(ooferror.ErrUserError,
                          OOF.Microstructure.New,
                          name="one", width=-1.0, height=-1.0,
                          width_in_pixels=10,
                          height_in_pixels=10)
        OOF.Microstructure.New(
            name="one",
            width=4.0, height=5.0, depth=6.0,
            width_in_pixels=120, height_in_pixels=100, depth_in_pixels=120)
        ms = getMicrostructure("one")
        self.assertEqual(ms.name(), "one")
        labeltree_count=microstructure.microStructures.members.__len__()
        ms_and_proxies=microstructure.microStructures.nmembers
        # There should be one proxy in the tree.
        self.assertEqual(ms_and_proxies,3)
        # The labeltree object's len function counts the root and the proxy.
        self.assertEqual(labeltree_count,4)
        ms_count=microstructure.microStructures.nActual()
        # There should be only one non-proxy object.
        self.assertEqual(ms_count,1)
        self.assertEqual(ms.size(), primitives.Point(4.0,5.0,6.0))
        self.assertEqual(ms.sizeOfPixels(), (4.0/120, 5.0/100, 6.0/120))


    # "Delete" should be run only after "New" has succeeded.  Assumes
    # exactly one microstructure, named "one", has already been created.
    def Delete(self):
        ms_count=microstructure.microStructures.nActual()
        self.assertEqual(ms_count,1)
        self.assertRaises(KeyError,
                          OOF.Microstructure.Delete, microstructure="two")
        ms_count=microstructure.microStructures.nActual()
        self.assertEqual(ms_count,1)
        OOF.Microstructure.Delete(microstructure="one")
        labeltree_count=microstructure.microStructures.members.__len__()
        ms_and_proxies=microstructure.microStructures.nmembers
        # There should only be the proxy left.
        self.assertEqual(ms_and_proxies,2)
        # The labeltree object's len function counts the root and the proxy.
        self.assertEqual(labeltree_count,3)
        ms_count=microstructure.microStructures.nActual()
        # There should be only one non-proxy object.
        self.assertEqual(ms_count,0)

    # Check that the LabelTree in the Who class works correctly.
    @memorycheck.check("m")
    def LabelTree(self):
        # First check for errors when the tree is empty
        self.assertRaises(KeyError,
                          microstructure.microStructures.__getitem__, "m")
        self.assertRaises(KeyError,
                          microstructure.microStructures.__getitem__, "m:s")
        OOF.Microstructure.New(
            name="m",
            width=4.0, height=5.0, depth=6.0,
            width_in_pixels=120, height_in_pixels=100, depth_in_pixels=120)
        # This shouldn't raise an exception:
        mic = microstructure.microStructures["m"]
        # But these should:
        self.assertRaises(KeyError,
                          microstructure.microStructures.__getitem__, "mmm")
        self.assertRaises(KeyError,
                          microstructure.microStructures.__getitem__, "m:s")
        
    # Should be run after "New" and "Delete" are known to work.
    @memorycheck.check("three", "four")
    def Copy(self):
        start_ms_count = microstructure.microStructures.nActual()
        OOF.Microstructure.New(name="three", width=2.5, height=3.5, depth=4.5,
                               width_in_pixels=10, height_in_pixels=10,
                               depth_in_pixels=10)
        # Tests automatic name uniquification.
        OOF.Microstructure.Copy(microstructure="three", name="three")
        OOF.Microstructure.Copy(microstructure="three", name="four")
        ms_count = microstructure.microStructures.nActual()
        self.assertEqual(ms_count, start_ms_count + 3)
        name_list = microstructure.microStructures.keys()
        self.assert_(['three<2>'] in name_list)
        self.assert_(['four'] in name_list)
        OOF.Microstructure.Delete(microstructure="three<2>")
        ms_0 = getMicrostructure("three")
        ms_1 = getMicrostructure("four")
        self.assertEqual(ms_0.sizeInPixels(), ms_1.sizeInPixels())
        self.assertEqual(ms_0.volumeOfPixels(), ms_1.volumeOfPixels())
        self.assertEqual(ms_0.size(), ms_1.size())

    # Uses New, does not make assumptions about existing microstructures.
    @memorycheck.check("newname")
    def Rename(self):
        OOF.Microstructure.New(name="rename", width=2.5, height=3.5, depth=4.5,
                               width_in_pixels=10, height_in_pixels=10,
                               depth_in_pixels=10)
        ms_count = microstructure.microStructures.nActual()
        ms_0 = getMicrostructure("rename")
        OOF.Microstructure.Rename(microstructure="rename", name="newname")
        ms_1 = getMicrostructure("newname")
        self.assertEqual(id(ms_0),id(ms_1))
        new_ms_count = microstructure.microStructures.nActual()
        self.assertEqual(ms_count, new_ms_count)

    # Also test basic load and save.  This is currently only for the
    # MS itself -- as with "Copy", later versions should also test for
    # correct propagation of MS contents, like pixel groups.
    @memorycheck.check("save_test")
    def Save(self):
        OOF.Microstructure.New(
            name="save_test", width=2.5, height=3.5, depth=4.5,
            width_in_pixels=10, height_in_pixels=10,
            depth_in_pixels=10)
        OOF.File.Save.Microstructure(
            filename="ms_save_test",
            mode="w",
            format="ascii",
            microstructure="save_test")
        self.assert_(
            file_utils.fp_file_compare(
                "ms_save_test",
                os.path.join("ms_data", "saved_ms"),
                1.e-10))
        file_utils.remove("ms_save_test")
        OOF.File.Save.Microstructure(
            filename="ms_save_test",
            mode="w",
            format="binary",
            microstructure="save_test")
        self.assert_(
            file_utils.fp_file_compare(
                "ms_save_test",
                os.path.join("ms_data", "saved_ms_binary"),
                1.e-10))
        file_utils.remove("ms_save_test")

    @memorycheck.check("save_test")        
    def Load(self):
        from ooflib.common import primitives
        OOF.File.Load.Data(filename=reference_file("ms_data","saved_ms"))
        ms_0 = getMicrostructure("save_test")
        self.assertEqual(ms_0.sizeInPixels(), primitives.iPoint(10,10,10))
        self.assertEqual(ms_0.size(), primitives.Point(2.5, 3.5, 4.5))
        self.assertEqual(ms_0.sizeOfPixels(), (2.5/10, 3.5/10, 4.5/10))

    @memorycheck.check("save_test")
    def LoadBin(self):
        from ooflib.common import primitives
        OOF.File.Load.Data(filename=reference_file("ms_data","saved_ms_binary"))
        ms_0 = getMicrostructure("save_test")
        self.assertEqual(ms_0.sizeInPixels(), primitives.iPoint(10,10,10))
        self.assertEqual(ms_0.size(), primitives.Point(2.5, 3.5, 4.5))
        self.assertEqual(ms_0.sizeOfPixels(), (2.5/10, 3.5/10, 4.5/10))

    def tearDown(self):
        pass


test_set = [
    OOF_Microstructure("New"),
    OOF_Microstructure("Delete"),
    OOF_Microstructure("LabelTree"),
    OOF_Microstructure("Copy"),
    OOF_Microstructure("Rename"),
    OOF_Microstructure("Save"),
    OOF_Microstructure("Load"),
    OOF_Microstructure("LoadBin"),
    ]
