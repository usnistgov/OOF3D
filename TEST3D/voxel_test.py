# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import unittest, os, sys
import memorycheck

from UTILS import file_utils
reference_file = file_utils.reference_file
from ooflib.SWIG.common import voxelsetboundary


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

class VSB_ConfigTest(unittest.TestCase):
    def setUp(self):
        global pixelselection
        from ooflib.common import pixelselection
        global microstructure
        from ooflib.common import microstructure
        
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
            if nvox > 0:
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

                sigstr = sigstr.replace('|', '-')
                ms.dumpVSB(selectedCat, "selected_"+sigstr+".dat")
                ms.dumpVSB(unselectedCat, "unselected_"+sigstr+".dat")
                ms.dumpVSBLines(selectedCat, "selected_"+sigstr+".lines")
                ms.dumpVSBLines(unselectedCat, "unselected_"+sigstr+".lines")

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
                print "-------"

            
#=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=##=-=#

test_set = [
    VSB_ConfigTest("Trivial"),
    VSB_ConfigTest("All2x2x2")
    ]
