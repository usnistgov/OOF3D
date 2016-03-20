# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import unittest, os
import memorycheck
from UTILS import file_utils
file_utils.generate = False

## TODO 3.1: These tests don't work because active areas and
## unmeshable groups aren't stored and loaded correctly.  See the
## TODOs in cmicrostructure.spy and pixelgroupmenu.py.

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
    @memorycheck.check("microstructure")
    def Rich_Save(self):
        OOF.Microstructure.New(
            name='microstructure',
            width=1.0, height=1.0, depth=1.0,
            width_in_pixels=3, height_in_pixels=3, depth_in_pixels=3)
        OOF.PixelSelection.Region(
            microstructure='microstructure',
            shape=CircleSelectionShape(center=Point(0.5,0.5,0.5),radius=0.5),
            units=PhysicalUnits(),
            operator=Select())
        OOF.ActiveArea.Activate_Selection_Only(
            microstructure='microstructure')
        OOF.ActiveArea.Store(
            microstructure='microstructure', name='sphere')
        OOF.PixelSelection.Region(
            microstructure='microstructure', 
            shape=BoxSelectionShape(point0=Point(0.5,0.5,0.5),
                                    point1=Point(0,0,0)),
            units=PhysicalUnits(),
            operator=SelectOnly())
        OOF.Graphics_1.Layer.New(
            category='Microstructure',
            what='microstructure', 
            how=MicrostructureMaterialDisplay(
                no_material=Gray(value=0.47619047619047616),
                no_color=RGBColor(red=0.00000,green=0.00000,blue=1.00000),
                filter=AllVoxels()))
        OOF.Graphics_1.Settings.Camera.View(
            view=View(cameraPosition=Coord(-1.42454,-0.917537,-1.18737),
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(-0.330656,0.873688,-0.356841), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0,
                      size_x=621, size_y=615))
        OOF.PixelGroup.New(
            name='meshable',
            microstructure='microstructure')
        OOF.PixelGroup.New(
            name='unmeshable',
            microstructure='microstructure')
        OOF.PixelGroup.Meshable(
            microstructure='microstructure',
            group='unmeshable',
            meshable=False)
        OOF.PixelGroup.AddSelection(
            microstructure='microstructure',
            group='meshable')
        OOF.ActiveArea.Activate_All(
            microstructure='microstructure')
        OOF.Graphics_1.Toolbox.Pixel_Select.Point(
            source='microstructure',
            points=[Point(-1.41896,-0.9132,-1.18442)],
            view=View(cameraPosition=Coord(-1.42454,-0.917537,-1.18737),
                      focalPoint=Coord(0.5,0.5,0.5),
                      up=Coord(-0.330656,0.873688,-0.356841), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0,
                      size_x=621,
                      size_y=615),
            shift=0, ctrl=0)
        OOF.PixelGroup.AddSelection(
            microstructure='microstructure',
            group='unmeshable')

        OOF.File.Save.Microstructure(
            filename="rich_save_test",
            mode="w", format="ascii",
            microstructure="microstructure")
        self.assert_(file_utils.fp_file_compare(
            "rich_save_test",
            os.path.join("ms_data","rich_ms"),
            1.e-6))
        file_utils.remove("rich_save_test")

    @memorycheck.check("rich")
    def Rich_Load(self):
        OOF.File.Load.Data(
            filename=file_utils.reference_file("ms_data", "rich_ms"))
        ms = microstructure.getMicrostructure("microstructure")
        group = ms.findGroup("meshable")
        self.assertEqual(len(group), 7)
        group2 = ms.findGroup("unmeshable")
        self.assertEqual(len(group2), 1)

        # Find the "act1" stored active area, and check the size.
        act1 = ms.getNamedActiveArea("sphere")
        self.assertEqual(len(act1.activearea.members()), 19)
        
test_set = [
    Microstructure_Extra("Rich_Save"),
    Microstructure_Extra("Rich_Load")
]
