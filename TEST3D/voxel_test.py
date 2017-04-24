# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test routines for constructing and clipping a voxel set boundary.

import unittest, os, sys, math
import memorycheck

from UTILS import file_utils
file_utils.generate = True


from ooflib.SWIG.common import voxelsetboundary
from ooflib.SWIG.common.geometry import COrientedPlane
from ooflib.common import microstructure
from ooflib.common import pixelselection
from ooflib.common import primitives

# For selecting voxels and defining a voxel set.
vox000 = voxelsetboundary.cvar.vox000
vox100 = voxelsetboundary.cvar.vox100
vox010 = voxelsetboundary.cvar.vox010
vox110 = voxelsetboundary.cvar.vox110
vox001 = voxelsetboundary.cvar.vox001
vox101 = voxelsetboundary.cvar.vox101
vox011 = voxelsetboundary.cvar.vox011
vox111 = voxelsetboundary.cvar.vox111

voxels = {vox000 : (0, 0, 0),
          vox100 : (1, 0, 0),
          vox010 : (0, 1, 0),
          vox110 : (1, 1, 0),
          vox001 : (0, 0, 1),
          vox101 : (1, 0, 1),
          vox011 : (0, 1, 1),
          vox111 : (1, 1, 1)}

# Define some planes to clip the voxel set boundaries.
skew = primitives.Point(1.1, 0.9, 1.0)
skew = skew/math.sqrt(skew*skew)
xyz = primitives.Point(1, 1, 1)
xyz = xyz/math.sqrt(xyz*xyz)

planes = [
    COrientedPlane(primitives.Point(1, 0, 0), 0.0),            # 0 empty
    COrientedPlane(primitives.Point(1, 0, 0), 4.0).reversed(), # 1 empty
    COrientedPlane(primitives.Point(1, 0, 0), 0.0).reversed(), # 2 all
    COrientedPlane(primitives.Point(1, 0, 0), 4.0),            # 3 all
    COrientedPlane(primitives.Point(1, 0, 0), 2.0),            # 4 through center
    COrientedPlane(primitives.Point(1, 0, 0), 2.5),            # 5
    COrientedPlane(primitives.Point(0, 1, 0), 2.5).reversed(), # 6
    COrientedPlane(primitives.Point(0, 0, 1), 1.5),            # 7
    COrientedPlane(skew, 2.5),                                 # 8
    COrientedPlane(skew, 2.5).reversed(),                      # 9
    COrientedPlane(xyz, 2*math.sqrt(3.)),                      # 10
]


class VSB_ConfigTest(unittest.TestCase):
    def setUp(self):
        
        OOF.Microstructure.New(
            name='microstructure', width=4.0, height=4.0, depth=4.0,
            width_in_pixels=4, height_in_pixels=4, depth_in_pixels=4)
        OOF.PixelGroup.New(
            name='pixelgroup', microstructure='microstructure')

    def selectionSize(self):
        ps = pixelselection.pixelselectionWhoClass['microstructure']
        return ps.getObject().len()

    def selectVoxel(self, i, j, k):
        OOF.PixelSelection.Region(
            microstructure='microstructure',
            shape=BoxSelectionShape(point0=Point(i,j,k)+Point(1,1,1),
                                    point1=Point(i,j,k)+Point(2,2,2)),
            units=PixelUnits(), operator=Select())

    def selectSig(self, sig):
        OOF.PixelSelection.Clear(
            microstructure='microstructure')
        OOF.PixelGroup.Clear(
            microstructure='microstructure',
            group='pixelgroup')
        # Select the voxels for the signature sig in the central
        # 2x2x2 cube of the microstructure.
        nvox = 0
        for (vox, loc) in voxels.items():
            if vox & sig:
                self.selectVoxel(*loc)
                nvox += 1
        return nvox
        

    @memorycheck.check("microstructure")
    def Trivial(self):
        ms = microstructure.getMicrostructure("microstructure")
        self.assertEqual(ms.nCategories(), 1)
        vol = ms.volumeOfCategory(0)
        self.assertEqual(vol, 64)

    # All2x2x2 makes two categories of voxels in a 4x4x4 cube.  The
    # outer surface voxels are always in the "unselected" category.
    # Voxels in the inner 2x2x2 cube are selected in all 255 possible
    # combinations, and the voxel set boundaries are verified.
    @memorycheck.check("microstructure")
    def All2x2x2(self):
        ms = microstructure.getMicrostructure('microstructure')
        # The non-trivial combinations of voxels correspond to voxel
        # signatures between 1 and 255.  Signature 0 has no voxels in
        # it, and would be equivalent to the Trivial test, above.
        sigs = range(1, 256)
        for sig in sigs:
            nvox = self.selectSig(sig)
            sigstr = voxelsetboundary.printSig(sig)
            print "Selected voxels:", sigstr, "(sig=%d)"% sig
            self.assertEqual(nvox, self.selectionSize())

            OOF.PixelGroup.AddSelection(
                microstructure='microstructure', group='pixelgroup')
            self.assertEqual(ms.nCategories(), 2) # triggers categorization

            unselectedCat = ms.category(Point(0,0,0))
            selectedCat = 1 - unselectedCat
            print "selectedCat=", selectedCat, "unselectedCat=",\
                unselectedCat

            ms.dumpVSB(selectedCat, "selected.dat")
            ms.dumpVSB(unselectedCat, "unselected.dat")
            # ms.dumpVSBLines(selectedCat, "selected_"+sigstr+".lines")
            # ms.dumpVSBLines(unselectedCat, "unselected_"+sigstr+".lines")

            selectedVol = ms.volumeOfCategory(selectedCat)
            unselectedVol = ms.volumeOfCategory(unselectedCat)
            print "selectedVol=", selectedVol, \
                "unselectedVol=", unselectedVol
            print "Checking connectivity for selected voxels, category",\
                selectedCat
            self.assert_(ms.checkVSB(selectedCat))
            print "Checking connectivity for unselected voxels, category",\
                unselectedCat
            self.assert_(ms.checkVSB(unselectedCat))
            self.assertAlmostEqual(selectedVol, nvox)
            self.assertAlmostEqual(unselectedVol, 64-nvox);
            # Check that the saved VSB graphs are correct
            sigstr = sigstr.replace('|', '-')
            self.assert_(file_utils.fp_file_compare(
                "selected.dat",
                os.path.join("vsb_data", "selected_"+sigstr+".dat"),
                1.e-9))
            self.assert_(file_utils.fp_file_compare(
                "unselected.dat",
                os.path.join("vsb_data", "unselected_"+sigstr+".dat"),
                1.e-9))
            print "-------"
            file_utils.remove("selected.dat")
            file_utils.remove("unselected.dat")

    @memorycheck.check("microstructure")
    def ClippedShape(self):
        # Check that a few carefully selected sets of voxels are
        # clipped properly by a single plane
        sigs = (
            vox000,
            vox111,
            vox000|vox100,
            vox000|vox110,
            vox010|vox100,
            vox000|vox100|vox010|vox111,
            )
        ms = microstructure.getMicrostructure('microstructure')
        for sig in sigs:
            sigstr = voxelsetboundary.printSig(sig)
            print "Selecting voxels", sigstr
            sigstr = sigstr.replace('|','-')
            nvox = self.selectSig(sig)
            OOF.PixelGroup.AddSelection(
                microstructure='microstructure', group='pixelgroup')
            unselectedCat = ms.category(Point(0,0,0))
            selectedCat = 1-unselectedCat
            for i, plane in enumerate(planes):
                # saveClippedVSB writes filename.dat and filename.lines
                ms.saveClippedVSB(selectedCat, plane, 'selected')
                ms.saveClippedVSB(unselectedCat, plane, 'unselected')

                fnamebase = "clipped_%s_p%02d" % (sigstr, i)
                self.assert_(file_utils.fp_file_compare(
                    'selected.dat',
                    os.path.join("vsb_data", 's'+fnamebase+'.dat'),
                    1.e-9))
                self.assert_(file_utils.fp_file_compare(
                    'unselected.dat',
                    os.path.join("vsb_data", 'u'+fnamebase+'.dat'),
                    1.e-9))
                self.assert_(file_utils.fp_file_compare(
                    'selected.lines',
                    os.path.join("vsb_data", 's'+fnamebase+'.lines'),
                    1.e-9))
                self.assert_(file_utils.fp_file_compare(
                    'unselected.lines',
                    os.path.join("vsb_data", 'u'+fnamebase+'.lines'),
                    1.e-9))

                file_utils.remove('selected.dat')
                file_utils.remove('unselected.dat')
                file_utils.remove('selected.lines')
                file_utils.remove('unselected.lines')

    @memorycheck.check("microstructure")
    def TrivialClippedVolume(self):
        ms = microstructure.getMicrostructure('microstructure')
        for plane in planes:
            v0 = ms.clipVSBVol(0, plane)
            v1 = ms.clipVSBVol(0, plane.reversed())
            self.assertAlmostEqual(v0+v1, 64.)

    @memorycheck.check("microstructure")
    def ClippedVolume(self):
        ms = microstructure.getMicrostructure('microstructure')
        sigs = range(1, 256)
        #sigs = (105,)
        for sig in sigs:
            print "voxels=%s"%voxelsetboundary.printSig(sig)
            nvox = self.selectSig(sig)
            OOF.PixelGroup.AddSelection(
                microstructure='microstructure', group='pixelgroup')
            unselectedCat = ms.category(Point(0,0,0))
            selectedCat = 1 - unselectedCat
            for plane in planes:
                print "plane=%s"%plane
                v00 = ms.clipVSBVol(selectedCat, plane)
                v10 = ms.clipVSBVol(unselectedCat, plane)
                opposite = plane.reversed()
                v01 = ms.clipVSBVol(selectedCat, opposite)
                v11 = ms.clipVSBVol(unselectedCat, opposite);
                self.assertAlmostEqual(nvox, v00+v01)
                self.assertAlmostEqual(64-nvox, v10+v11)
                self.assertAlmostEqual(v00+v01+v10+v11, 64)
            
#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

test_set = [
    VSB_ConfigTest("Trivial"),
    VSB_ConfigTest("All2x2x2"),
    VSB_ConfigTest("ClippedShape"),
    VSB_ConfigTest("TrivialClippedVolume"),
    VSB_ConfigTest("ClippedVolume")
]

# test_set = [
#     VSB_ConfigTest("ClippedShape"),
# ]
