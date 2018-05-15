# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Test suite for skeleton selection and group commands, not including
# boundary commands, which are tested separately.  

# This file assumes that microstructures, images, and pixel group
# menu items have all been tested and work, and that the skeleton_basic
# tests also work.

## TODO 3.1: Query group, create groups from materials

## TODO 3.1: Add tests using active areas.

## TODO: Add tests for saving and restoring selections on modified
## skeletons, where the node indexing might have changed.

import unittest, os
import memorycheck
from UTILS import file_utils 
file_utils.generate = False
reference_file = file_utils.reference_file

class Skeleton_Selection(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        from ooflib.SWIG.engine import cskeletonselectable
        self.uidOffset = cskeletonselectable.peekUID()

    def makeSkeleton(self, nx, ny, nz):
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=nx, y_elements=ny, z_elements=nz,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))

    # Subclasses should redefine skeletonpath if they don't use the
    # default methods for making microstructures and skeletons.
    skeletonpath = "skeltest:skeleton"
    def skelContext(self):
        return skeletoncontext.skeletonContexts[self.skeletonpath]
    def skeleton(self):
        return self.skelContext().getObject()

    # For Faces and Segments, uiIdentifier() returns the "uid"
    # assigned to the object in the CSkeletonSelectable constructor.
    # This isn't an appropriate identifier to use during the tests,
    # because its value is history dependent.  fixUID() offsets the
    # uid by its value at the beginning of the test, making it
    # independent of what's come before. 

    def selectionIDs(self):
        objs = self.selection().retrieve() # selection() defined in subclasses
        return [self.fixUID(o.uiIdentifier()) for o in objs]
    def groupIDs(self, grpname):
        grp = self.groups().get_group(grpname) # groups() defined in subclasses
        return [self.fixUID(o.uiIdentifier()) for o in grp]
    def groupNames(self):
        return list(self.groups().allGroups())
    def groupSize(self, grpname):
        return len(self.groups().get_group(grpname))

    def rawSelectionIDs(self):
        objs = self.selection().retrieve() # selection() defined in subclasses
        return [o.uiIdentifier() for o in objs]

        

# Subclasses of Skeleton_Selection for loading different Images and
# creating different Skeletons.

class Skeleton_Selection_5Color(Skeleton_Selection):
    def setUp(self):
        Skeleton_Selection.setUp(self)
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImagePattern(
                directory=reference_file("ms_data","5color"),
                pattern="slice(0|([1-9][0-9]*))\\.tif",
                sort=NumericalOrder()),
            microstructure_name="skeltest",
            height=20.0, width=20.0, depth=20.0)
        OOF.Image.AutoGroup(image="skeltest:5color", name_template='%c')
        OOF.Material.New(name='thing1', material_type='bulk')
        OOF.Material.New(name='thing2', material_type='bulk')
        OOF.Material.Assign(
            material='thing1', microstructure='skeltest', pixels='#fefefe')
        OOF.Material.Assign(
            material='thing2', microstructure='skeltest', pixels='#f3f359')

    def tearDown(self):
        OOF.Material.Delete(name="thing1")
        OOF.Material.Delete(name="thing2")

class Skeleton_Selection_BlueGreen50(Skeleton_Selection):
    # The bluegreen50 image is a 10x10x10 cube, divided into two equal
    # parts at z=5.  The small z half is blue (#868cfe) and the large
    # z half is green (#a1fc93).
    def setUp(self):
        Skeleton_Selection.setUp(self)
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file('ms_data','bluegreen50'),
                sort=NumericalOrder()),
            microstructure_name='skeltest',
            height=automatic, width=automatic, depth=automatic)
        OOF.Image.AutoGroup(image="skeltest:bluegreen50", name_template='%c')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The actual test classes are derived from a Skeleton_Selection
# subclass, above, and one of these four classes for each type of
# selectable.

class Element_Selection:
    def selection(self):
        return self.skelContext().elementselection
    def groups(self):
        return self.skelContext().elementgroups
    def fixUID(self, uid):
        return uid

class Face_Selection:
    def selection(self):
        return self.skelContext().faceselection
    def groups(self):
        return self.skelContext().facegroups
    def fixUID(self, uid):
        return uid - self.uidOffset

class Segment_Selection:
    def selection(self):
        return self.skelContext().segmentselection
    def groups(self):
        return self.skelContext().segmentgroups
    def fixUID(self, uid):
        return uid - self.uidOffset

class Node_Selection:
    def selection(self):
        return self.skelContext().nodeselection
    def groups(self):
        return self.skelContext().nodegroups
    def fixUID(self, uid):
        return uid

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Element_Selection_5Color(Skeleton_Selection_5Color, Element_Selection):
    @memorycheck.check("skeltest")
    def SingleElement(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=255,operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        ids = self.selectionIDs()
        self.assertEqual(ids, [255])
        # Select an interior element by clipping the display. (Now
        # that the menu command stores the element ID and not the
        # click position and view information, this test is sort of
        # meaningless.)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=205,operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [205])
        # shift-click to select an additional element on the unclipped
        # display
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=75,operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [75, 205])
        # control-click to toggle it off
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=75,operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [205])
        # control-click to toggle it back on
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=75,operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [75, 205])

    @memorycheck.check("skeltest")
    def UndoRedo(self):
        # The actual selection dictionary for the whole skeleton-context's
        # stack is at self.elementselection.currentSelection().  This is
        # the thing whose ID should change when Undo/Redo events occur.
        self.makeSkeleton(4, 4, 4)
        # Get the original (empty) selection object
        sel0 = id(self.selection().currentSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=195,operator=Select()))
        # Check that the selection object is different
        sel1 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel1)
        # And that the right object is selected
        self.assertEqual(self.selectionIDs(), [195])
        # Undo the selection
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        # Check that the selection object is the original one
        sel2 = id(self.selection().currentSelection())
        self.assertEqual(sel0, sel2)
        self.assertEqual(self.selectionIDs(), [])
        # Redo
        OOF.ElementSelection.Redo(skeleton='skeltest:skeleton')
        sel3 = id(self.selection().currentSelection())
        self.assertEqual(sel1, sel3)
        self.assertEqual(self.selectionIDs(), [195])
        # Select another element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=316,operator=Select()))
        sel4 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel4)
        self.assertNotEqual(sel1, sel4)
        self.assertEqual(self.selectionIDs(), [316])
        # Undo and check that we got the right thing
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel1)
        self.assertEqual(self.selectionIDs(), [195])
        # Undo again
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel0)
        self.assertEqual(self.selectionIDs(), [])
        # Redo twice
        OOF.ElementSelection.Redo(skeleton='skeltest:skeleton')     
        OOF.ElementSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel4)
        self.assertEqual(self.selectionIDs(), [316])

    @memorycheck.check("skeltest")
    def Clear(self):
        self.makeSkeleton(4, 4, 4)
        # Select an element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=316,operator=Select()))
        self.assertEqual(self.selectionIDs(), [316])
        OOF.ElementSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])

    @memorycheck.check("skeltest")
    def Invert(self):
        self.makeSkeleton(2, 2, 2)
        self.assertEqual(self.selectionIDs(), [])
        # Invert
        OOF.ElementSelection.Invert(skeleton='skeltest:skeleton')
        # Everything should be selected
        elist = range(40)
        self.assertEqual(self.selectionIDs(), elist)
        # Invert again
        OOF.ElementSelection.Invert(skeleton='skeltest:skeleton')
        # Nothing should be selected 
        self.assertEqual(self.selectionIDs(), [])
        # Select a single element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=26,operator=Select()))
        self.assertEqual(self.selectionIDs(), [26])
        OOF.ElementSelection.Invert(skeleton='skeltest:skeleton')
        elist.remove(26)
        self.assertEqual(self.selectionIDs(), elist)

    @memorycheck.check("skeltest")
    def DominantPixel(self):
        self.makeSkeleton(4, 4, 4)
        # Click on a green voxel
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=PixelElementSelect(category=1,operator=Select()))
        self.assertEqual(self.selection().size(), 38)
        indices = [40, 43, 44, 46, 48, 60, 61, 63, 64, 65, 66, 67, 68, 69,
                   70, 71, 72, 73, 74, 75, 77, 125, 127, 145, 146, 147, 148,
                   149, 150, 151, 152, 153, 154, 156, 158, 230, 233, 234]
        self.assertEqual(indices, self.selectionIDs())

    @memorycheck.check("skeltest")
    def Homogeneity(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementHomogeneity(
                min_homogeneity=0,
                max_homogeneity=0.601, # some elements have homog=0.6
                operator=Select()))
        self.assertEqual(self.selection().size(), 42)
        indices = [21, 24, 42, 50, 52, 53, 54, 70, 96, 123, 131, 132,
                   133, 134, 141, 143, 144, 147, 151, 165, 172, 175,
                   177, 178, 179, 181, 183, 184, 187, 191, 192, 198,
                   201, 211, 212, 216, 229, 230, 250, 268, 280, 295]
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def ShapeEnergy(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        # In a cubically symmetric Skeleton the tets at the corners of
        # each cubical subunit have shape energy 0.159104 and the ones
        # at the centers have shape energy 0.0.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementShapeEnergy(
                min_energy=1,
                max_energy=1,
                operator=Select()))
        # No elements have shape energy >= 1
        self.assertEqual(self.selection().size(), 0)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementShapeEnergy(
                min_energy=0.1,
                max_energy=1,
                operator=Select()))
        # Only the corners are selected.
        self.assertEqual(self.selection().size(), 256)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementShapeEnergy(
                min_energy=0,
                max_energy=1,
                operator=Select()))
        # All elements are selected.
        self.assertEqual(self.selection().size(), 320)

    @memorycheck.check("skeltest")
    def Material(self):
        self.makeSkeleton(4, 4, 4)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ByElementMaterial(material='thing1',
                                     operator=Select()))
        self.assertEqual(self.selection().size(), 110)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ByElementMaterial(material='thing2',
                                     operator=Select()))
        self.assertEqual(self.selection().size(), 91)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ByElementMaterial(material='<Any>',
                                     operator=Select()))
        self.assertEqual(self.selection().size(), 201)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ByElementMaterial(material='<None>',
                                     operator=Select()))
        self.assertEqual(self.selection().size(), 119)

    @memorycheck.check("skeltest")
    def Expand(self):
        self.makeSkeleton(4, 4, 4)
        # Select an interior element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=205,operator=Select()))
        self.assertEqual(self.selectionIDs(), [205])
        # Expand via faces
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandElementSelection(mode='Faces'))
        # OOF.ElementSelection.Expand(
        #     skeleton='skeltest:skeleton', mode='Faces')        
        indices = [126, 185, 205, 209, 213]
        self.assertEqual(indices, self.selectionIDs())
        # Undo
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual([205], self.selectionIDs())
        # Expand via segments
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandElementSelection(mode='Segments'))
        # OOF.ElementSelection.Expand(
        #     skeleton='skeltest:skeleton', mode='Segments')
        indices = [106, 126, 127, 129, 132, 185, 187, 189, 193,
                   205, 206, 207, 208, 209, 212, 213, 214]
        self.assertEqual(indices, self.selectionIDs())
        # Undo
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual([205], self.selectionIDs())
        # Expand via nodes
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandElementSelection(mode='Nodes'))
        # OOF.ElementSelection.Expand(
        #     skeleton='skeltest:skeleton', mode='Nodes')
        indices = [100, 101, 102, 104, 106, 107, 108, 109, 112, 120, 121,
                   122, 124, 125, 126, 127, 128, 129, 131, 132, 133, 134,
                   145, 146, 147, 149, 151, 152, 153, 154, 180, 181, 183,
                   184, 185, 186, 187, 188, 189, 191, 192, 193, 194, 200,
                   201, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
                   213, 214, 225, 226, 228, 229, 230, 232, 233, 234, 265,
                   266, 268, 269, 270, 272, 273, 274, 285, 286, 288, 289,
                   290, 292, 293, 294]
        self.assertEqual(indices, self.selectionIDs())
        # Now try starting with two adjacent elements on a boundary
        # and do the tests again.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=276,operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=296,operator=AddSelection()))

        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandElementSelection(mode='Faces'))
        indices = [276, 279, 296, 299]
        self.assertEqual(indices, self.selectionIDs())
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')

        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandElementSelection(mode='Segments'))
        indices = [275, 276, 277, 278, 279, 295, 296, 297, 298, 299]
        self.assertEqual(indices, self.selectionIDs())
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')

        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandElementSelection(mode='Nodes'))
        indices = [195, 196, 197, 199, 215, 216, 217, 219, 255, 256, 257,
                   259, 270, 271, 272, 274, 275, 276, 277, 278, 279, 290,
                   291, 292, 294, 295, 296, 297, 298, 299, 315, 316, 317, 319]
        self.assertEqual(indices, self.selectionIDs())
        
#     def Rectangle(self):
#         self.assertEqual(self.e_selection.size(), 0)
#         self.selection_menu.Rectangle(
#             skeleton="skeltest:skelselect",
#             points=[Point(3.0,5.0), Point(12.0,18.0)],
#             shift=0,ctrl=0)
#         self.assertEqual(self.e_selection.size(), 8)
#         e_set = self.e_selection.retrieve()
#         self.assertEqual(len(e_set),8)
#         index_list = [26,27,34,35,42,43,50,51]
#         for e in e_set:
#             self.assert_( e.getUid() in index_list)
#             index_list.remove(e.getUid())

#     def Circle(self):
#         self.assertEqual(self.e_selection.size(), 0)
#         self.selection_menu.Circle(
#             skeleton="skeltest:skelselect",
#             points=[Point(7.0,10.0), Point(11.0,7.0)],
#             shift=0,ctrl=0)
#         self.assertEqual(self.e_selection.size(), 4)
#         e_set = self.e_selection.retrieve()
#         self.assertEqual(len(e_set),4)
#         index_list = [26,27,34,35]
#         for e in e_set:
#             self.assert_( e.getUid() in index_list)
#             index_list.remove(e.getUid())

#     def Ellipse(self):
#         self.assertEqual(self.e_selection.size(), 0)
#         self.selection_menu.Ellipse(
#             skeleton="skeltest:skelselect",
#             points=[Point(3.0,5.0), Point(12.0,18.0)],
#             shift=0,ctrl=0)
#         self.assertEqual(self.e_selection.size(), 6)
#         e_set = self.e_selection.retrieve()
#         self.assertEqual(len(e_set),6)
#         index_list = [26,27,34,35,42,43]
#         for e in e_set:
#             self.assert_( e.getUid() in index_list)
#             index_list.remove(e.getUid())

# end Element_Selection_5Color

# Element group tests are done on bluegreen50, which is half blue and
# half green, because it's easy to check that the correct elements are
# in the groups.

class Element_Selection_BlueGreen50(Skeleton_Selection_BlueGreen50,
                                    Element_Selection):
    # When selecting elements via pixel groups or automatically
    # creating element groups from pixel groups, these are the
    # elements that should be in each group:
    green_elems = [5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 25, 26, 27, 28, 29,
                   35, 36, 37, 38, 39]
    blue_elems = [0, 1, 2, 3, 4, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24,
                  30, 31, 32, 33, 34]

    @memorycheck.check("skeltest")
    def NewGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        self.assertEqual(self.groupSize("newgroup"), 0)

    @memorycheck.check("skeltest")
    def RenameGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='knights who say Ni')
        OOF.ElementGroup.Rename_Group(
            skeleton='skeltest:skeleton',
            group='knights who say Ni',
            new_name='knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg')
        self.assertEqual(
            self.groupNames(),
            ['knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg'])

    @memorycheck.check("skeltest")
    def AddToGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=35,operator=Select()))
        self.assertEqual(self.selectionIDs(), [35])
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [35])
        # Select another element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=16,operator=Select()))
        self.assertEqual(self.selectionIDs(), [16])
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [16, 35])
        # Re-add the same element
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [16, 35])

    @memorycheck.check("skeltest")
    def SelectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select an element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=35,operator=Select()))
        self.assertEqual(self.selectionIDs(), [35])
        # Select the elements in the empty group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Undo the selection of the empty group
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        # Make the group non-empty
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.ElementSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select the element in the group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Select()))
        self.assertEqual(self.selectionIDs(), [35])
        # Select a different element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=3,operator=Select()))
        self.assertEqual(self.selectionIDs(), [3])
        # Select the element in the group and make sure that the
        # different element is not selected.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Select()))
        self.assertEqual(self.selectionIDs(), [35])

    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select an element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=35,operator=Select()))
        self.assertEqual(self.selectionIDs(), [35])
        # Add the elements in the empty group to the selection and
        # make sure the selected element stays selected.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [35])
        # Make the group non-empty
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.ElementSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [35])
        # Select a different element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=3,operator=Select()))
        self.assertEqual(self.selectionIDs(), [3])
        # Add the group to the selection and make sure both elements
        # are selected.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [3, 35])

    @memorycheck.check("skeltest")
    def SelectFromPixelGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementByPixelGroup(group='#a1fc93', operator=Select()))
        self.assertEqual(self.selectionIDs(), self.green_elems)
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementByPixelGroup(group='#868cfe', operator=Select()))
        self.assertEqual(self.selectionIDs(), self.blue_elems)

    @memorycheck.check("skeltest")
    def AutoGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        # Check that there are two groups with the right names
        self.assertEqual(self.groupNames(), ['#a1fc93', '#868cfe'])
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_elems)
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_elems)
        # Select one group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Select()))
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Select the other
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#868cfe',operator=Select()))
        self.assertEqual(self.selectionIDs(), self.blue_elems)

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Select()))
        # Unselect the empty group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Unselect()))
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Unselect a non-empty but non intersecting group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#868cfe',operator=Unselect()))
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Unselect the green group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Unselect()))
        self.assertEqual(self.selectionIDs(), [])
        # Select a single element and put it in newgroup
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=5,operator=Select()))
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [5])
        # Reselect the green group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Select()))
        # Unselect the single element in newgroup
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Unselect()))
        indices = self.green_elems[:]
        indices.remove(5)
        self.assertEqual(self.selectionIDs(), indices)
    
    @memorycheck.check("skeltest")
    def IntersectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Select()))
        # Intersect it with itself
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Intersect it with the (disjoint) blue group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#868cfe',operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the green group and intersect it with the empty
        # group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Add all the elements to newgroup
        OOF.ElementSelection.Invert(skeleton='skeltest:skeleton')
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group and intersect it with the full group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Reselect the full group and intersect it with the green group
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='newgroup',operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='#a1fc93',operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_elems)
        
    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Use autogroup to create the groups
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        # Select a single green element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=35,operator=Select()))
        self.assertEqual(self.selectionIDs(), [35])
        # Try to remove it from the blue group
        OOF.ElementGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_elems)
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_elems)
        # Now remove it from the green group
        OOF.ElementGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_elems)
        indices = self.green_elems[:]
        indices.remove(35)
        self.assertEqual(self.groupIDs('#a1fc93'), indices)

    @memorycheck.check("skeltest")
    def CopyGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Create and copy an empty group
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        OOF.ElementGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='newgroup',
            new_name='knewgroop')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop'])
        self.assertEqual(self.groupIDs('knewgroop'), [])
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.ElementGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='#868cfe',
            new_name='duplicate')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop',
                          '#a1fc93', '#868cfe', 'duplicate'])
        self.assertEqual(self.groupIDs('duplicate'), self.blue_elems)

    @memorycheck.check("skeltest")
    def DeleteGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        OOF.ElementGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.groupNames(), [])
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.ElementGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='#a1fc93')
        self.assertEqual(self.groupNames(), ['#868cfe'])
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_elems)

    @memorycheck.check("skeltest")
    def DeleteAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.ElementGroup.Delete_All(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.groupNames(), [])

    @memorycheck.check("skeltest")
    def ClearGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.ElementGroup.Clear_Group(
            skeleton='skeltest:skeleton',
            group='#a1fc93')
        self.assertEqual(self.groupIDs('#a1fc93'), [])
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_elems)

    @memorycheck.check("skeltest")
    def ClearAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(skeleton='skeltest:skeleton')
        OOF.ElementGroup.Clear_All(skeleton='skeltest:skeleton')
        self.assertEqual(self.groupIDs('#a1fc93'), [])
        self.assertEqual(self.groupIDs('#868cfe'), [])

    @memorycheck.check("skeltest")
    def SelectFromNodes(self):
        self.makeSkeleton(2, 2, 2)
        # Select the node in the center of the front face.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedNodes(min_nodes=1,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [6, 16, 25, 35])
        # Select three nodes along the bottom edge
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,0,10),
                                    operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,0,10),
                                    operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,0,10),
                                    operator=AddSelection()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedNodes(min_nodes=1,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [5, 6, 8, 9, 15, 16, 18, 19])
        # Select the 4 nodes of the upper front left tet
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,5,10),
                                    operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,10,10),
                                    operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,10,10),
                                    operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,10,5),
                                    operator=AddSelection()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedNodes(min_nodes=2,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [25, 26, 27, 28, 29])
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedNodes(min_nodes=3,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [26, 29])
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedNodes(min_nodes=4,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [26])
    

    @memorycheck.check("skeltest")
    def SelectFromSegments(self):
        self.makeSkeleton(2, 2, 2)
        # Select a segment on the top front edge
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 26],
                                       operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedSegments(min_segments=1,
                                               operator=Select()))
        self.assertEqual(self.selectionIDs(), [36])
        # Select one on the front face
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 14],
                                       operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedSegments(min_segments=1,
                                               operator=Select()))
        self.assertEqual(self.selectionIDs(), [25, 35])
        # Select two segments that share elements
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[20, 23],
                                       operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[11, 23],
                                       operator=AddSelection()))
        # Select elements with at least one selected segment
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedSegments(min_segments=1,
                                               operator=Select()))
        self.assertEqual(self.selectionIDs(), [25, 26, 29])
        # Select elements with at least two selected segments
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedSegments(min_segments=2,
                                               operator=Select()))
        self.assertEqual(self.selectionIDs(), [26])
        # Select elements with at least three selected segments
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedSegments(min_segments=3,
                                               operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Select elements with exactly one selected segment
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedSegments(min_segments=1,
                                               operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedSegments(min_segments=2,
                                               operator=Unselect()))
        self.assertEqual(self.selectionIDs(), [25, 29])
        
    @memorycheck.check("skeltest")
    def SelectFromFaces(self):
        self.makeSkeleton(2, 2, 2)
        # Select a face on the front
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[14, 17, 23],
                                    operator=Select()))
        # Select elements with at least one selected face
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedFaces(min_faces=1,
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(), [35])
        # Select elements with at least two selected faces
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedFaces(min_faces=2,
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(), [])
        # Select two internal faces
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 23, 13],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[23, 11, 19],
                                    operator=AddSelection()))
        # Select elements with one selected face
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedFaces(min_faces=1,
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(), [25, 26, 29])
        # Select elements with two selected faces
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedFaces(min_faces=2,
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(), [29])
        # Select elements with three selected faces
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedFaces(min_faces=3,
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(), [])
      
    @memorycheck.check("skeltest")
    def Save(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.File.Save.Skeleton(
            filename="skeleton_group_test",
            mode="w", format="ascii",
            skeleton="skeltest:skeleton")
        self.assert_(file_utils.fp_file_compare(
                'skeleton_group_test',
                reference_file('skeleton_data', 'egroups'), 1.e-9))
        file_utils.remove('skeleton_group_test')

    @memorycheck.check("skeltest")
    def Load(self):
        OOF.Microstructure.Delete(microstructure='skeltest')
        OOF.File.Load.Data(filename=reference_file("skeleton_data", "egroups"))
        self.assertEqual(self.groupNames(), ['#a1fc93', '#868cfe'])
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_elems)
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_elems)

# end Element_Selection_BlueGreen50
  
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Face_Selection_5Color(Skeleton_Selection_5Color, Face_Selection):
    @memorycheck.check("skeltest")
    def SingleFace(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        # Select a face on the perimeter
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[109, 89, 114],
                                    operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1535])
        # Select an interior face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[87, 62, 57],
                                    operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1109])
        # shift-click to select an additional face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[123, 98, 97],
                                    operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [1109, 1684])

        # control-click
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[123, 98, 97],
                                    operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [1109])
        # control-click again
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[123, 98, 97],
                                    operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [1109, 1684])

    @memorycheck.check("skeltest")
    def UndoRedo(self):
        self.makeSkeleton(4, 4, 4)
        sel0 = id(self.selection().currentSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[109, 89, 114],
                                    operator=Select()))
        sel1 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel1)
        self.assertEqual(self.selectionIDs(), [1535])
        # Undo
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        sel2 = id(self.selection().currentSelection())
        self.assertEqual(sel0, sel2)
        self.assertEqual(self.selectionIDs(), [])
        # Redo
        OOF.FaceSelection.Redo(skeleton='skeltest:skeleton')
        sel3 = id(self.selection().currentSelection())
        self.assertEqual(sel1, sel3)
        self.assertEqual(self.selectionIDs(), [1535])
        # Select another face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[87, 62, 57],
                                    operator=Select()))
        sel4 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel4)
        self.assertNotEqual(sel1, sel4)
        self.assertEqual(self.selectionIDs(), [1109])
        # Undo
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel1)
        self.assertEqual(self.selectionIDs(), [1535])
        # Undo again
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel0)
        self.assertEqual(self.selectionIDs(), [])
        # Redo twice
        OOF.FaceSelection.Redo(skeleton='skeltest:skeleton')     
        OOF.FaceSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel4)
        self.assertEqual(self.selectionIDs(), [1109])
        
    @memorycheck.check("skeltest")
    def Clear(self):
        self.makeSkeleton(4, 4, 4)
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[87, 62, 57],
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [1109])
        OOF.FaceSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])

    @memorycheck.check("skeltest")
    def Invert(self):
        self.makeSkeleton(2, 2, 2)
        self.assertEqual(self.selectionIDs(), [])
        OOF.FaceSelection.Invert(skeleton='skeltest:skeleton')
        facelist = [
            34, 35, 36, 37, 44, 45, 46, 47, 53, 54, 55, 56, 61, 62, 63, 64,
            73, 74, 75, 76, 83, 84, 85, 86, 89, 90, 91, 94, 95, 96, 102, 103,
            104, 111, 112, 113, 114, 118, 119, 120, 125, 126, 127, 128, 137,
            138, 139, 140, 144, 145, 146, 149, 150, 151, 153, 154, 160, 161,
            162, 169, 170, 171, 172, 178, 179, 180, 181, 184, 185, 186, 192,
            193, 194, 201, 202, 203, 204, 207, 208, 209, 211, 212, 218, 219,
            220, 224, 225, 226, 232, 233, 234, 235, 237, 238, 242, 243, 250, 
            251, 252, 253, 255, 256, 258, 259]
        self.assertEqual(self.selectionIDs(), facelist)
        OOF.FaceSelection.Invert(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],operator=Select()))
        self.assertEqual(self.selectionIDs(), [194])
        OOF.FaceSelection.Invert(skeleton='skeltest:skeleton')
        facelist.remove(194)
        self.assertEqual(self.selectionIDs(), facelist)

# end Face_Selection_5Color

def makeFaceGroups():
    # The Element, Segment, and Node tests use AutoGroup to create
    # groups, but AutoGroup hasn't been implemented for Faces yet.
    # Instead, this utility function creates and populates two
    # groups.  

    # # This function is called from other test modules, and when it's
    # # called that way, the oof namespace isn't imported to this
    # # module, so we have to import some classes manually.
    # from ooflib.common.IO.mainmenu import OOF
    # from ooflib.engine.skeletonselectionmethod import SingleFaceSelect
    # from ooflib.common.selectionoperators import Select, AddSelection

    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[11, 23, 20],operator=Select()))
    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[11, 14, 23],operator=AddSelection()))
    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[11, 5, 14],operator=AddSelection()))
    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[2, 5, 11],operator=AddSelection()))

    OOF.FaceGroup.New_Group(
        skeleton='skeltest:skeleton', name='groupA')
    OOF.FaceGroup.Add_to_Group(
        skeleton='skeltest:skeleton', group='groupA')

    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[23, 17, 26],operator=Select()))
    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[14, 17, 23],operator=AddSelection()))
    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[5, 17, 14],operator=AddSelection()))
    OOF.FaceSelection.Select(
        skeleton='skeltest:skeleton',
        method=SingleFaceSelect(nodes=[5, 8, 17],operator=AddSelection()))

    OOF.FaceGroup.New_Group(
        skeleton='skeltest:skeleton', name='groupB')
    OOF.FaceGroup.Add_to_Group(
        skeleton='skeltest:skeleton', group='groupB')

a_faces = [76, 86, 194, 204]
b_faces = [140, 146, 243, 253]

class Face_Selection_BlueGreen50(Skeleton_Selection_BlueGreen50,
                                 Face_Selection):

    @memorycheck.check("skeltest")
    def NewGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        self.assertEqual(self.groupSize("newgroup"), 0)

    @memorycheck.check("skeltest")
    def RenameGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='knights who say Ni')
        OOF.FaceGroup.Rename_Group(
            skeleton='skeltest:skeleton',
            group='knights who say Ni',
            new_name='knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg')
        self.assertEqual(
            self.groupNames(),
            ['knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg'])

    @memorycheck.check("skeltest")
    def AddToGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],operator=Select()))
        self.assertEqual(self.selectionIDs(), [194])
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [194])
        # Select another face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[14, 17, 23],operator=Select()))
        self.assertEqual(self.selectionIDs(), [243])
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [194, 243])
        # Re-add the same face
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [194, 243])

    @memorycheck.check("skeltest")
    def SelectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],operator=Select()))
        self.assertEqual(self.selectionIDs(), [194])
        # Select the faces in the empty group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup',operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Undo the selection of the empty group
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        # Make the group non-empty
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.FaceSelection.Clear(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select the face in the group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup',operator=Select()))
        self.assertEqual(self.selectionIDs(), [194])
        # Select a different face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[23, 17, 26],operator=Select()))
        self.assertEqual(self.selectionIDs(), [253])
        # Select the face in the group and make sure that the
        # different face is not selected.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup',operator=Select()))
        self.assertEqual(self.selectionIDs(), [194])

    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],operator=Select()))
        self.assertEqual(self.selectionIDs(), [194])
        # Add the faces in the empty group to the selection and
        # make sure the selected face stays selected.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup',operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [194])
        # Make the group non-empty
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.FaceSelection.Clear(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup',operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [194])
        # Select a different face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[23, 17, 26],operator=Select()))
        self.assertEqual(self.selectionIDs(), [253])
        # Add the group to the selection and make sure both faces
        # are selected.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup',operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [194, 253])

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA',operator=Select()))
        # Unselect the empty group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup', operator=Unselect()))
        self.assertEqual(self.selectionIDs(), a_faces)
        # Unselect a non-empty but non intersecting group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupB', operator=Unselect()))
        self.assertEqual(self.selectionIDs(), a_faces)
        # Unselect the actually selected group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA', operator=Unselect()))
        self.assertEqual(self.selectionIDs(), [])
        # Select a single face and put it in newgroup.  The selected
        # face is already in groupA.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],operator=Select()))
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [194])
        # Reselect the first group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA', operator=Select()))
        # Unselect the single face in newgroup
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup', operator=Unselect()))
        indices = a_faces[:]
        indices.remove(194)
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def IntersectGroup(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the A group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA', operator=Select()))
        # Intersect it with itself
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA', operator=Intersect()))
        self.assertEqual(self.selectionIDs(), a_faces)
        # Intersect it with the (disjoint) B group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupB', operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the A group and intersect it with the empty
        # group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA', operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup', operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Add all the faces to newgroup
        OOF.FaceSelection.Invert(skeleton='skeltest:skeleton')
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the A group and intersect it with the full group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA', operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup', operator=Intersect()))
        self.assertEqual(self.selectionIDs(), a_faces)
        # Reselect the full group and intersect it with the A group
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='newgroup', operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='groupA', operator=Intersect()))
        self.assertEqual(self.selectionIDs(), a_faces)

    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        # Select a single A face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],operator=Select()))
        self.assertEqual(self.selectionIDs(), [194])
        # Try to remove it from the B group
        OOF.FaceGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='groupB')
        self.assertEqual(self.groupIDs('groupB'), b_faces)
        self.assertEqual(self.groupIDs('groupA'), a_faces)
        # Now remove it from the A group
        OOF.FaceGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='groupA')
        self.assertEqual(self.groupIDs('groupB'), b_faces)
        indices = a_faces[:]
        indices.remove(194)
        self.assertEqual(self.groupIDs('groupA'), indices)

    @memorycheck.check("skeltest")
    def CopyGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Create and copy an empty group
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        OOF.FaceGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='newgroup',
            new_name='knewgroop')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop'])
        self.assertEqual(self.groupIDs('knewgroop'), [])
        makeFaceGroups()
        OOF.FaceGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='groupB',
            new_name='duplicate')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop',
                          'groupA', 'groupB', 'duplicate'])
        self.assertEqual(self.groupIDs('duplicate'), b_faces)

    @memorycheck.check("skeltest")
    def DeleteGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        OOF.FaceGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.groupNames(), [])
        makeFaceGroups()
        OOF.FaceGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='groupA')
        self.assertEqual(self.groupNames(), ['groupB'])
        self.assertEqual(self.groupIDs('groupB'), b_faces)

    @memorycheck.check("skeltest")
    def DeleteAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.FaceGroup.Delete_All(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.groupNames(), [])

    @memorycheck.check("skeltest")
    def ClearGroup(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.FaceGroup.Clear_Group(
            skeleton='skeltest:skeleton',
            group='groupA')
        self.assertEqual(self.groupIDs('groupA'), [])
        self.assertEqual(self.groupIDs('groupB'), b_faces)

    @memorycheck.check("skeltest")
    def ClearAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.FaceGroup.Clear_All(skeleton='skeltest:skeleton')
        self.assertEqual(self.groupIDs('groupA'), [])
        self.assertEqual(self.groupIDs('groupB'), [])

    @memorycheck.check("skeltest")
    def SelectFromElements(self):
        self.makeSkeleton(2, 2, 2)
        # Select one element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=35,
                                       operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='All',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [144, 193, 242, 243])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Interior',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Exterior',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [144, 193, 242, 243])
        # Select another adjacent element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=16,
                                       operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='All',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(),
                         [84, 144, 145, 146, 193, 242, 243])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Exterior',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [84, 145, 146, 193, 242, 243])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Interior',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [144])

    @memorycheck.check("skeltest")
    def SelectFromNodes(self):
        self.makeSkeleton(2, 2, 2)
        # Select a corner node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,0,10),
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=1,
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [73, 75, 76])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=2,
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=3,
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Select an adjacent node as well
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,0,10),
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=1,
                                         operator=Select()))
        self.assertEqual(
            self.selectionIDs(),
            [73, 74, 75, 76, 84, 85, 86, 94, 95,
             96, 137, 139, 140, 145, 146, 153, 154])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=2,
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [75, 76])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=3,
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Select just the center node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,5),
                                     operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=1,
                                         operator=Select()))
        self.assertEqual(
            self.selectionIDs(),
            [34, 35, 37, 45, 46, 47, 53, 54, 56, 83, 84, 85, 90,
             91, 94, 96, 102, 104, 111, 113, 114, 119, 120, 144,
             145, 149, 150, 153, 161, 162, 170, 171, 172, 184, 186,
             192, 193, 207, 209, 211, 218, 220, 225, 226, 237, 242, 255, 258])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedNodes(min_nodes=2,
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [])

    @memorycheck.check("skeltest")
    def SelectFromSegments(self):
        self.makeSkeleton(2, 2, 2)
        # Start with a segment along an edge
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[5, 2],
                                       operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedSegments(min_segments=1,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [75, 76])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedSegments(min_segments=2,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Add a segment that shares a tet with the first one.
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[11, 5],
                                       operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedSegments(min_segments=1,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [74, 75, 76, 85, 86])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedSegments(min_segments=2,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [76])
        # Select a third segment to make a triangle
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[2, 11],
                                       operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedSegments(min_segments=1,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [73, 74, 75, 76, 85, 86])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedSegments(min_segments=2,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [76])
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedSegments(min_segments=3,
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [76])

    @memorycheck.check("skeltest")
    def InternalBoundaries(self):
        self.makeSkeleton(4, 4, 4)
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SelectInternalBoundaryFaces(operator=Select()))
        self.assertEqual(
            self.selectionIDs(),
            [174, 184, 302, 308, 408, 418, 522, 528, 628, 638, 729, 739, 821,
             827, 907, 917, 1005, 1015, 1109, 1115, 1195, 1205, 1287, 1293,
             1382, 1392, 1483, 1493, 1575, 1581, 1661, 1671])


    @memorycheck.check("skeltest")
    def Save(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.File.Save.Skeleton(
            filename='skeleton_group_test',
            mode='w', format='ascii',
            skeleton='skeltest:skeleton')
        self.assert_(file_utils.fp_file_compare(
                'skeleton_group_test',
                reference_file('skeleton_data', 'fgroups'), 1.e-9))
        file_utils.remove('skeleton_group_test')

    @memorycheck.check('skeltest')
    def Load(self):
        OOF.Microstructure.Delete(microstructure='skeltest')
        OOF.File.Load.Data(filename=reference_file('skeleton_data', 'fgroups'))
        self.assertEqual(self.groupNames(), ['groupA', 'groupB'])
        self.assertEqual(self.groupIDs('groupA'), a_faces)
        self.assertEqual(self.groupIDs('groupB'), b_faces)
        
# end Face_Selection_BlueGreen50

    ## TODO 3.0: Add tests for the rest of the face selection and group
    ## operations when they are implemented.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Segment_Selection_5Color(Skeleton_Selection_5Color, Segment_Selection):
    @memorycheck.check("skeltest")
    def SingleSegment(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[63,83],
                                       operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1125])
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[109, 114],
                                       operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1527])
        # Shift-click
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[113, 83],
                                       operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [1502, 1527])
        # Control-click to deselect
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[83, 113],
                                       operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [1527])
        # Control-click to reselect
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[83, 113],
                                       operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [1502, 1527])
    
    @memorycheck.check("skeltest")
    def UndoRedo(self):
        self.makeSkeleton(4, 4, 4)
        sel0 = id(self.selection().currentSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one Segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[59, 89],
                                       operator=Select()))
        # Check that the selection object is different
        sel1 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel1)
        # And that the right Segment is selected
        self.assertEqual(self.selectionIDs(), [1146])
        # Undo
        OOF.SegmentSelection.Undo(skeleton='skeltest:skeleton')
        sel2 = id(self.selection().currentSelection())
        self.assertEqual(sel0, sel2)
        self.assertEqual(self.selectionIDs(), [])
        # Redo
        OOF.SegmentSelection.Redo(skeleton='skeltest:skeleton')
        sel3 = id(self.selection().currentSelection())
        self.assertEqual(sel1, sel3)
        self.assertEqual(self.selectionIDs(), [1146])
        # Select another Segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[59, 39],
                                       operator=Select()))
        sel4 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel4)
        self.assertNotEqual(sel1, sel4)
        self.assertEqual(self.selectionIDs(), [769])
        # Undo
        OOF.SegmentSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel1)
        self.assertEqual(self.selectionIDs(), [1146])
        # Undo again
        OOF.SegmentSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel0)
        self.assertEqual(self.selectionIDs(), [])
        # Redo twice
        OOF.SegmentSelection.Redo(skeleton='skeltest:skeleton')
        OOF.SegmentSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel4)
        self.assertEqual(self.selectionIDs(), [769])

    @memorycheck.check("skeltest")
    def Clear(self):
        self.makeSkeleton(4, 4, 4)
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[64, 39],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [774])
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])

    @memorycheck.check("skeltest")
    def Invert(self):
        self.makeSkeleton(2, 2, 2)
        self.assertEqual(self.selectionIDs(), [])
        edgelist = [
            28, 29, 30, 31, 32, 33, 39, 40, 41, 42, 43, 49, 50, 51, 52, 58,
            59, 60, 67, 68, 69, 70, 71, 72, 78, 79, 80, 81, 82, 88, 93, 99,
            100, 101, 106, 107, 108, 109, 110, 116, 117, 122, 123, 124, 131,
            132, 133, 134, 135, 136, 142, 143, 148, 157, 158, 159, 164, 165,
            166, 167, 168, 174, 175, 176, 177, 183, 189, 190, 191, 196, 197, 
            198, 199, 200, 206, 215, 216, 217, 222, 223, 228, 229, 230, 231,
            241, 245, 246, 247, 248, 249]
        # Invert.  Everything should be selected
        OOF.SegmentSelection.Invert(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), edgelist)
        # Invert again.  Nothing should be selected.
        OOF.SegmentSelection.Invert(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select one segment.
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 11],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [189])
        # Invert. All but one segment should be selected.
        OOF.SegmentSelection.Invert(skeleton='skeltest:skeleton')
        edgelist.remove(189)
        self.assertEqual(self.selectionIDs(), edgelist)

    @memorycheck.check("skeltest")
    def Homogeneity(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentHomogeneity(min_homogeneity=0,max_homogeneity=0.5,
                                      operator=Select()))
        indices = [432, 490, 602, 798, 843, 1011, 1054, 1084, 1148, 1201,
                   1326, 1597]
        self.assertEqual(self.selectionIDs(), indices)

# end Segment_Selection_5Color

class Segment_Selection_BlueGreen50(Skeleton_Selection_BlueGreen50,
                                    Segment_Selection):
    green_segs = [28, 29, 30, 39, 40, 67, 68, 69, 70, 71, 72, 78, 79, 80, 81,
                  82, 88, 93, 99, 100, 106, 107, 131, 132, 133, 134, 135, 136,
                  142, 143, 148, 157, 158, 164, 165, 189, 190, 191, 196, 197,
                  198, 199, 200, 206, 215, 216, 222, 241, 245, 246, 247, 248,
                  249]
    blue_segs = [31, 32, 33, 41, 42, 43, 49, 50, 51, 52, 58, 59, 60, 101, 108,
                 109, 110, 116, 117, 122, 123, 124, 159, 166, 167, 168, 174,
                 175, 176, 177, 183, 217, 223, 228, 229, 230, 231]

    @memorycheck.check("skeltest")
    def SingleSegment2(self):
        # When this test was first recorded, it seemed to select
        # segment 198 in text mode and 196 in gui mode.  Later that
        # inconsistency couldn't be reproduced.  That was of course
        # back when the menu command arguments contained view and
        # mouse click info, instead of node indices.  So this test is
        # presumably useless now, but is kept for completeness.
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[11, 19],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [198])
        
    @memorycheck.check("skeltest")
    def NewGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        self.assertEqual(self.groupSize("newgroup"), 0)

    @memorycheck.check("skeltest")
    def RenameGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='knights who say Ni')
        OOF.SegmentGroup.Rename_Group(
            skeleton='skeltest:skeleton',
            group='knights who say Ni',
            new_name='knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg')
        self.assertEqual(
            self.groupNames(),
            ['knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg'])
 
    @memorycheck.check("skeltest")
    def AddToGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 11],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [189])
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [189])
        # Select another segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[4, 13],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [29])
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [29, 189])
        # Re-add the same element
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [29, 189])

    @memorycheck.check("skeltest")
    def SelectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[4, 13],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [29])
        # Select the segments in the empty group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Undo the selection of the empty group
        OOF.SegmentSelection.Undo(skeleton='skeltest:skeleton')
        # Make the group non-empty
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        # Clear the selection
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select the segment in the group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Select()))
        self.assertEqual(self.selectionIDs(), [29])
        # Select a different segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 11],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [189])
        # Select the segment in the group again.  The previously
        # selected segment should be deselected.
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Select()))
        self.assertEqual(self.selectionIDs(), [29])

    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[4, 13],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [29])
        # Add the segments in the empty group to the selection and
        # make sure the selected segment stays selected.
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [29])
        # Make the group non-empty
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        # Clear the selection
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [29])
        # Select a different segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 11],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [189])
        # Add the group to the selection and make sure both segments
        # are selected.
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [29, 189])

    @memorycheck.check("skeltest")
    def AutoGroup(self):
        self.makeSkeleton(2, 2, 2)
        self.assertEqual(self.groupNames(), [])
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.groupNames(),
                         ['#a1fc93', '#868cfe'])
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_segs)
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_segs)
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Select()))
        self.assertEqual(self.selectionIDs(), self.green_segs)
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#868cfe',
                                      operator=Select()))
        self.assertEqual(self.selectionIDs(), self.blue_segs)

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Select()))
        # Unselect the empty group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Unselect()))
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Unselect a non-empty but non intersecting group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#868cfe',
                                      operator=Unselect()))
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Unselect the green group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Unselect()))
        self.assertEqual(self.selectionIDs(), [])
        # Select a single segment and put it in newgroup
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[8, 5],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [133])
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Select()))
        # Unselect the single segment in newgroup
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Unselect()))
        indices = self.green_segs[:]
        indices.remove(133)
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def IntersectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Select()))
        # Intersect it with itself
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Intersect it with the (disjoint) blue group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#868cfe',
                                      operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the green group and intersect it with the empty
        # group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Add all the segments to newgroup
        OOF.SegmentSelection.Invert(skeleton='skeltest:skeleton')
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group and intersect it with the full group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Reselect the full group and intersect it with the green group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='newgroup',
                                      operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegmentSelectGroup(group='#a1fc93',
                                      operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_segs)

    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        # Select a single segment that's in the green group
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[14, 5],
                                       operator=Select()))
        self.assertEqual(self.selectionIDs(), [79])
        # Try to remove it from the blue group
        OOF.SegmentGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_segs)
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_segs)
        # Now remove it from the green group
        OOF.SegmentGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_segs)
        indices = self.green_segs[:]
        indices.remove(79)
        self.assertEqual(self.groupIDs('#a1fc93'), indices)
        
    @memorycheck.check("skeltest")
    def CopyGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Create and copy an empty group
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        OOF.SegmentGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='newgroup',
            new_name='knewgroop')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop'])
        self.assertEqual(self.groupIDs('knewgroop'), [])
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='#868cfe',
            new_name='duplicate')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop',
                          '#a1fc93', '#868cfe', 'duplicate'])
        self.assertEqual(self.groupIDs('duplicate'), self.blue_segs)
        
    @memorycheck.check("skeltest")
    def DeleteGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        OOF.SegmentGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.groupNames(), [])
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='#a1fc93')
        self.assertEqual(self.groupNames(), ['#868cfe'])
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_segs)

    @memorycheck.check("skeltest")
    def DeleteAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.Delete_All(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.groupNames(), [])

    @memorycheck.check("skeltest")
    def ClearGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.Clear_Group(
            skeleton='skeltest:skeleton',
            group='#a1fc93')
        self.assertEqual(self.groupIDs('#a1fc93'), [])
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_segs)

    @memorycheck.check("skeltest")
    def ClearAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(skeleton='skeltest:skeleton')
        OOF.SegmentGroup.Clear_All(skeleton='skeltest:skeleton')
        self.assertEqual(self.groupIDs('#a1fc93'), [])
        self.assertEqual(self.groupIDs('#868cfe'), [])
      
    @memorycheck.check("skeltest")
    def SelectFromNodes(self):
        self.makeSkeleton(2, 2, 2)
        # Select the center node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,5),
                                    operator=Select()))
        # Select segments with one or two selected nodes
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedNodes(one=True,
                                        two=True,
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), 
                         [28, 29, 32, 40, 43, 49, 80, 81, 82, 99, 106,
                          108, 143, 158, 165, 168, 191, 215])
        # Select segments with  two selected nodes, of which there are none
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedNodes(one=False,
                                        two=True,
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        
        # Select an additional node in center of the front face
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedNodes(one=True,
                                        two=True,
                                        operator=Select()))
        
        self.assertEqual(self.selectionIDs(), 
                         [28, 29, 32, 40, 43, 49, 78, 79, 80, 81, 82, 99,
                          106, 108, 142, 143, 158, 165, 168, 190, 191, 215])
        # Select segments with just two selected nodes
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedNodes(one=False,
                                        two=True,
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [81])
                         
    @memorycheck.check("skeltest")
    def SelectFromElements(self):
        self.makeSkeleton(2, 2, 2)
        # Select a single element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=26,
                                       operator=Select()))
        OOF.SegmentSelection.Select(
             skeleton='skeltest:skeleton',
             method=SegFromSelectedElements(coverage='All',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(),
                         [189, 196, 197, 198, 199, 200])
        # Select the cluster of elements around the center node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,5),
                                    operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedNodes(min_nodes=1,
                                            operator=Select()))
        # Select all segments in the element cluster
        OOF.SegmentSelection.Select(
             skeleton='skeltest:skeleton',
             method=SegFromSelectedElements(coverage='All',
                                            operator=Select()))
        self.assertEqual(
            self.selectionIDs(), 
            [28, 29, 30, 31, 32, 33, 39, 40, 41, 42, 43, 49, 50, 51, 52, 68,
             71, 72, 78, 79, 80, 81, 82, 88, 93, 99, 100, 101, 106, 107, 108,
             109, 110, 116, 117, 131, 134, 135, 142, 143, 148, 157, 158, 159,
             164, 165, 166, 167, 168, 177, 183, 189, 190, 191, 198, 200, 206, 
             215, 216, 217, 222, 223, 230, 241, 247, 249])
        # Select just the external segments in the cluster
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedElements(coverage='Exterior',
                                            operator=Select()))
        self.assertEqual(
            self.selectionIDs(),
            [30, 31, 33, 39, 41, 42, 50, 51, 52, 68, 71, 72, 78, 79, 88, 93, 
             100, 101, 107, 109, 110, 116, 117, 131, 134, 135, 142, 148, 157, 
             159, 164, 166, 167, 177, 183, 189, 190, 198, 200, 206, 216, 217,
             222, 223, 230, 241, 247, 249])
        # Select just the internal segments
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedElements(coverage='Interior',
                                            operator=Select()))
        self.assertEqual(
            self.selectionIDs(),
            [28, 29, 32, 40, 43, 49, 80, 81, 82, 99, 106, 108, 143, 158, 165,
             168, 191, 215])

    @memorycheck.check("skeltest")
    def SelectFromFaces(self):
        self.makeSkeleton(2, 2, 2)
        # Select one face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[14, 17, 23],
                                    operator=Select()))
        # Select all segments of the face
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedFaces(coverage='All',
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [142, 190, 241])
        # Select the internal segments of the face
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedFaces(coverage='Interior',
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Select the external segments of the face
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedFaces(coverage='Exterior',
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [142, 190, 241])
        # Select an adjacent face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],
                                    operator=AddSelection()))
        # Select all segments of the faces
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedFaces(coverage='All',
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [78, 142, 189, 190, 241])
        # Select the internal segments of the faces
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedFaces(coverage='Interior',
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [190])
        # Select the external segments of the face
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SegFromSelectedFaces(coverage='Exterior',
                                        operator=Select()))
        self.assertEqual(self.selectionIDs(), [78, 142, 189, 241])
    
    @memorycheck.check('skeltest')
    def InternalBoundaries(self):
        self.makeSkeleton(4, 4, 4)
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SelectInternalBoundarySegments(operator=Select()))
        self.assertEqual(
            self.selectionIDs(),
            [165, 166, 167, 176, 177, 293, 294, 295, 304, 403, 404, 410, 411,
             513, 514, 515, 524, 623, 624, 630, 631, 727, 731, 732, 816, 817,
             823, 905, 909, 910, 1000, 1001, 1007, 1008, 1104, 1105, 1111, 1193,
             1197, 1198, 1282, 1283, 1289, 1377, 1378, 1384, 1385, 1481, 1485,
             1486, 1570, 1571, 1577, 1659, 1663, 1664])
            

    @memorycheck.check('skeltest')
    def Save(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.File.Save.Skeleton(
            filename='skeleton_group_test',
            mode='w', format='ascii',
            skeleton='skeltest:skeleton')
        self.assert_(file_utils.fp_file_compare(
                'skeleton_group_test',
                reference_file('skeleton_data', 'sgroups'), 1.e-9))
        file_utils.remove('skeleton_group_test')

    @memorycheck.check("skeltest")
    def Load(self):
        OOF.Microstructure.Delete(microstructure='skeltest')
        OOF.File.Load.Data(filename=reference_file("skeleton_data", "sgroups"))
        self.assertEqual(self.groupNames(), ['#a1fc93', '#868cfe'])
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_segs)
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_segs)

# end Segment_Selection_BlueGreen50

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Node_Selection_5Color(Skeleton_Selection_5Color, Node_Selection):
    @memorycheck.check("skeltest")
    def SingleNode(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        # Click on a node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,15,20),
                                    operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [89])
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(20,10,10),
                                    operator=Select()))
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [72])
        # Shift-click
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,10,20),
                                    operator=AddSelection()))
        self.assertEqual(self.selection().size(), 2)
        self.assertEqual(self.selectionIDs(), [64, 72])
        # Control-click to deselect
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,10,20),
                                    operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [72])
        # Control-click to reselect
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,10,20),
                                    operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [64, 72])

    @memorycheck.check("skeltest")
    def UndoRedo(self):
        self.makeSkeleton(4, 4, 4)
        sel0 = id(self.selection().currentSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one Node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,15,20),
                                    operator=Select()))
        # Check that the selection object is different
        sel1 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel1)
        # And that the right Node is selected
        self.assertEqual(self.selectionIDs(), [89])
        # Undo
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        sel2 = id(self.selection().currentSelection())
        self.assertEqual(sel0, sel2)
        self.assertEqual(self.selectionIDs(), [])
        # Redo
        OOF.NodeSelection.Redo(skeleton='skeltest:skeleton')
        sel3 = id(self.selection().currentSelection())
        self.assertEqual(sel1, sel3)
        self.assertEqual(self.selectionIDs(), [89])
        # Select another Node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,10,20),
                                    operator=Select()))
        sel4 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel4)
        self.assertNotEqual(sel1, sel4)
        self.assertEqual(self.selectionIDs(), [59])
        # Undo
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel1)
        self.assertEqual(self.selectionIDs(), [89])
        # Undo again
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel0)
        self.assertEqual(self.selectionIDs(), [])
        # Redo twice
        OOF.NodeSelection.Redo(skeleton='skeltest:skeleton')
        OOF.NodeSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel4)
        self.assertEqual(self.selectionIDs(), [59])

    @memorycheck.check("skeltest")
    def Clear(self):
        self.makeSkeleton(4, 4, 4)
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,15,20),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [89])
        OOF.NodeSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])

    @memorycheck.check("skeltest")
    def Invert(self):
        self.makeSkeleton(2, 2, 2)
        self.assertEqual(self.selectionIDs(), [])
        # Invert.  Everything should be selected.
        OOF.NodeSelection.Invert(skeleton='skeltest:skeleton')
        nodelist = range(27)
        self.assertEqual(self.selectionIDs(), nodelist)
        # Invert again.  Nothing should be selected.
        OOF.NodeSelection.Invert(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select one Node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,10,20),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [11])
        # Invert.  All but one Node should be selected.
        OOF.NodeSelection.Invert(skeleton='skeltest:skeleton')
        nodelist.remove(11)
        self.assertEqual(self.selectionIDs(), nodelist)

    @memorycheck.check("skeltest")
    def Expand(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        # Expand the empty selection
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandNodeSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one Node along an edge, shared by two elements
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,10,20),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [54])
        # Expand
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandNodeSelection())
        self.assertEqual(self.selectionIDs(), [29, 53, 54, 59, 79])
        # Undo
        OOF.NodeSelection.Undo(
            skeleton='skeltest:skeleton')
        # Select an additional adjacent node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,15,20),
                                    operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [54, 79])
        # Expand
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandNodeSelection())
        self.assertEqual(self.selectionIDs(),
                         [29, 53, 54, 59, 78, 79, 83, 84, 103, 104, 109])

    @memorycheck.check("skeltest")
    def NamedBdy(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        idlist = [('XminYminZmax', 4),
                  ('XmaxYminZmax', 24),
                  ('XmaxYmaxZmin', 120),
                  ('XminYmaxZmin', 100)]
        for bdyname, nodeID in idlist:
            OOF.NodeSelection.Select(
                skeleton='skeltest:skeleton',
                method=SelectNamedBoundaryNodes(boundary=bdyname,
                                                operator=Select()))
            self.assertEqual(self.selectionIDs(), [nodeID])

# end class Node_Selection_5Color

class Node_Selection_BlueGreen50(Skeleton_Selection_BlueGreen50,
                                 Node_Selection):
    @memorycheck.check("skeltest")
    def InternalBoundaries(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SelectInternalBoundaryNodes(operator=Select()))
        self.assertEqual(self.selectionIDs(),
                         [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57, 62,
                          67, 72, 77, 82, 87, 92, 97, 102, 107, 112, 117, 122])

    @memorycheck.check("skeltest")
    def NewGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        self.assertEqual(self.groupSize('newgroup'), 0)

    @memorycheck.check("skeltest")
    def RenameGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='knights who say Ni')
        OOF.NodeGroup.Rename_Group(
            skeleton='skeltest:skeleton',
            group='knights who say Ni',
            new_name='knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg')
        self.assertEqual(
            self.groupNames(),
            ['knights who say Ekke Ekke Ekke Ekke Ptangya Ziiinnggg'])
    
    @memorycheck.check("skeltest")
    def AddToGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        self.assertEqual(self.groupNames(), ['newgroup'])
        # Select a node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [14])
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [14])
        # Select another node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,5,10),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [11])
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [11, 14])
        # Re-add the same element
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [11, 14])

    @memorycheck.check("skeltest")
    def SelectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a Node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [14])
        # Select the nodes in the empty group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Undo the selection of the empty group
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [14])
        # Make the group non-empty
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Clear the selection
        OOF.NodeSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select the Node in the group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Select()))
        self.assertEqual(self.selectionIDs(), [14])
        # Select a different Node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,10,5),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [22])
        # Select the Node in the group again. The previously selected
        # Node should be deselected.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Select()))
        self.assertEqual(self.selectionIDs(), [14])
        
    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a Node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,10,5),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [22])
        # Add the Nodes in the empty group to the selection and make
        # sure the slected Node stays selected.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [22])
        # Make the group non-empty
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Clear the selection
        OOF.NodeSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [22])
        # Select a different Node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [14])
        # Add the group to the selection and make sure that both Nodes
        # are selected.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [14, 22])
    
    green_nodes = [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22,
                   23, 25, 26]
    blue_nodes = [0, 3, 6, 9, 12, 15, 18, 21, 24]

    @memorycheck.check("skeltest")
    def AutoGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.groupNames(), ['#a1fc93', '#868cfe'])
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_nodes)
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_nodes)
        # Select one group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Select()))
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Select the other
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#868cfe',
                                   operator=Select()))
        self.assertEqual(self.selectionIDs(), self.blue_nodes)

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Select()))
        # Unselect the empty group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Unselect()))
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Unselect a non-empty but non intersecting group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#868cfe',
                                   operator=Unselect()))
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Unselect the green group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Unselect()))
        self.assertEqual(self.selectionIDs(), [])
        # Select a single node which is already in the green group and
        # put it in newgroup
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=Select()))
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [14])
        # Reselect the green group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Select()))
        # Unselect the single node in newgroup
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Unselect()))
        indices = self.green_nodes[:]
        indices.remove(14)
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def IntersectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Select()))
        # Intersect it with itself
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Intersect it with the (disjoint) blue group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#868cfe',
                                   operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the green group and intersect it with the empty
        # group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Intersect()))
        self.assertEqual(self.selectionIDs(), [])
        # Add all the nodes to newgroup
        OOF.NodeSelection.Invert(skeleton='skeltest:skeleton')
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group and intersect it with the full group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Reselect the full group and intersect it with the green group
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='newgroup',
                                   operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeSelectGroup(group='#a1fc93',
                                   operator=Intersect()))
        self.assertEqual(self.selectionIDs(), self.green_nodes)

    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Use autogroup to create the groups
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        # Select a single green node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [14])
        # Try to remove it from the blue group
        OOF.NodeGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_nodes)
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_nodes)
        # Now remove it from the green group
        OOF.NodeGroup.Remove_from_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_nodes)
        indices = self.green_nodes[:]
        indices.remove(14)
        self.assertEqual(self.groupIDs('#a1fc93'), indices)

    @memorycheck.check("skeltest")
    def CopyGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Create and copy an empty group
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        OOF.NodeGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='newgroup',
            new_name='knewgroop')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop'])
        self.assertEqual(self.groupIDs('knewgroop'), [])
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.Copy_Group(
            skeleton='skeltest:skeleton',
            group='#868cfe',
            new_name='duplicate')
        self.assertEqual(self.groupNames(),
                         ['newgroup', 'knewgroop',
                          '#a1fc93', '#868cfe', 'duplicate'])
        self.assertEqual(self.groupIDs('duplicate'), self.blue_nodes)

    @memorycheck.check("skeltest")
    def DeleteGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='newgroup')
        OOF.NodeGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.groupNames(), [])
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.Delete_Group(
            skeleton='skeltest:skeleton',
            group='#a1fc93')
        self.assertEqual(self.groupNames(), ['#868cfe'])
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_nodes)

    @memorycheck.check("skeltest")
    def DeleteAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.Delete_All(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.groupNames(), [])

    @memorycheck.check("skeltest")
    def ClearGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.Clear_Group(
            skeleton='skeltest:skeleton',
            group='#a1fc93')
        self.assertEqual(self.groupIDs('#a1fc93'), [])
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_nodes)

    @memorycheck.check("skeltest")
    def ClearAllGroups(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(skeleton='skeltest:skeleton')
        OOF.NodeGroup.Clear_All(skeleton='skeltest:skeleton')
        self.assertEqual(self.groupIDs('#a1fc93'), [])
        self.assertEqual(self.groupIDs('#868cfe'), [])

    @memorycheck.check("skeltest")
    def SelectFromSegments(self):
        self.makeSkeleton(2, 2, 2)
        # Select a segment on the front face
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[17, 14],operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedSegments(operator=Select()))
        self.assertEqual(self.selectionIDs(), [14, 17])
        # Select a second segment without deselecting the first
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[19, 13],
                                       operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedSegments(operator=Select()))
        self.assertEqual(self.selectionIDs(), [13, 14, 17, 19])

        # Select another segment
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 11],operator=Select()))
        # Select its nodes without deselecting the previously selected ones
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedSegments(operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [11, 13, 14, 17, 19, 23])

    @memorycheck.check("skeltest")
    def SelectFromElements(self):
        self.makeSkeleton(2, 2, 2)
        # Select a corner element
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=36,operator=Select()))
        # Select its nodes
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedElements(coverage='All',
                                            operator=Select()))
        self.assertEqual(self.selectionIDs(), [17, 23, 25, 26])
        # Select all but the corner elements, by selecting the center
        # node (13) and then all the elements that contain it.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,5),
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [13])
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementFromSelectedNodes(min_nodes=1,
                                            operator=Select()))
        # Select all the nodes of the selected elements
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedElements(coverage='All',
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(),
                         [1, 3, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                          19, 21, 22, 23, 25])
        # Select just the exterior nodes
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedElements(coverage='Exterior',
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(),
                         # The center node, 13, is not in this list
                         [1, 3, 4, 5, 7, 9, 10, 11, 12, 14, 15, 16, 17,
                          19, 21, 22, 23, 25])
        # Select just the internal nodes, of which there is one.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedElements(coverage='Interior',
                                            operator=Select()))        
        self.assertEqual(self.selectionIDs(), [13])

    @memorycheck.check("skeltest")
    def SelectFromFaces(self):
        self.makeSkeleton(2, 2, 2)
        # Select a face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],
                                    operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='All',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [11, 14, 23])
        # Select an additional adjacent face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[14, 17, 23],
                                    operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='All',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [11, 14, 17, 23])
        # Select the internal nodes, of which there are none.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='Interior',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [])
        # Select the external nodes, which are the same as all the nodes
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='Exterior',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [11, 14, 17, 23])
        # Select more adjacent faces, so that now there are nodes
        # interior to the selection.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 5, 14],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[5, 17, 14],
                                    operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='All',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [5, 11, 14, 17, 23])
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='Interior',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [14])
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='Exterior',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [5, 11, 17, 23])

    @memorycheck.check("skeltest")
    def SelectFromMultipleFaces(self):
        # Select nodes on sets of faces that are joined in a
        # complicated fashion, not forming a simple sheet.
        self.makeSkeleton(2, 2, 2)
        # Select the faces of two elements that touch at a corner, and
        # one of the faces that joins the two elements.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=26,
                                       operator=Select()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=6,
                                       operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Exterior',
                                            operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],
                                    operator=AddSelection()))
        # Select the exterior nodes of the selected faces.  There are
        # just two -- the end points of the one segment that lies
        # along only one selected face.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='Exterior',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [14, 23])
        # Select all of the nodes of the selected faces.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='All',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [5, 11, 13, 14, 19, 20, 23])
        # Select just the interior nodes.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedFaces(coverage='Interior',
                                         operator=Select()))
        self.assertEqual(self.selectionIDs(), [5, 11, 13, 19, 20])

    @memorycheck.check('skeltest')
    def Save(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.File.Save.Skeleton(
            filename='skeleton_group_test',
            mode='w', format='ascii',
            skeleton='skeltest:skeleton')
        self.assert_(file_utils.fp_file_compare(
                'skeleton_group_test',
                reference_file('skeleton_data', 'ngroups'), 1.e-9))
        file_utils.remove('skeleton_group_test')

    @memorycheck.check('skeltest')
    def Load(self):
        OOF.Microstructure.Delete(microstructure='skeltest')
        OOF.File.Load.Data(filename=reference_file('skeleton_data', 'ngroups'))
        self.assertEqual(self.groupNames(), ['#a1fc93', '#868cfe'])
        self.assertEqual(self.groupIDs('#a1fc93'), self.green_nodes)
        self.assertEqual(self.groupIDs('#868cfe'), self.blue_nodes)


# end class Node_Selection_BlueGreen50

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## 2D tests that still have to be converted to 3D:

# class Skeleton_Element_Group(Skeleton_Selection):

# #     def Material_Group(self):
# #         # Select a 2x2 set of elements in the lower left corner and
# #         # store it as testgroup1.
# #         self.selection_menu.Rectangle(
# #             skeleton="skeltest:skelselect",
# #             points=[Point(-.5, 6, 0), Point(6, -.5, 0)], shift=0, ctrl=0)
# #         OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
# #                                    name="testgroup1")
# #         OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
# #                                       group="testgroup1")
# #         # Select a 2x2 set offset to the northeast by one element and
# #         # store them as testgroup2.  This group overlaps with
# #         # testgroup1.
# #         self.selection_menu.Rectangle(
# #             skeleton="skeltest:skelselect",
# #             points=[Point(2.1, 8.1), Point(8.1, 2.1)], shift=0, ctrl=0)
# #         OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
# #                                    name="testgroup2")
# #         OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
# #                                       group="testgroup2")
# #         # Create a third group with no overlap with the other two.
# #         self.selection_menu.Rectangle(
# #             skeleton="skeltest:skelselect",
# #             points=[Point(12.1, 18.1), Point(18.1, 12.1)], shift=0, ctrl=0)
# #         OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
# #                                    name="testgroup3")
# #         OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
# #                                       group="testgroup3")
        

# #         OOF.Material.New(name='material1', material_type='bulk')
# #         OOF.Material.New(name='material2', material_type='bulk')

# #         # Assign a material to one of the overlapping groups
# #         OOF.ElementGroup.Assign_Material(skeleton="skeltest:skelselect",
# #                                          group="testgroup1",
# #                                          material="material1")
# #         # Check that the four elements in testgroup1 have the right
# #         # material.
# #         for elem in self.e_groups.get_group("testgroup1"):
# #             material = elem.material(self.sk_context)
# #             self.assert_(material is not None)
# #             self.assertEqual(material.name(), "material1")
# #         # Check that the non-overlapping group has no materials
# #         for elem in self.e_groups.get_group("testgroup3"):
# #             self.assert_(elem.material(self.sk_context) is None)
            
# #         # Remove material
# #         OOF.ElementGroup.Remove_Material(skeleton="skeltest:skelselect",
# #                                          group="testgroup1")
# #         for elem in self.e_groups.get_group("testgroup1"):
# #             material = elem.material(self.sk_context)
# #             self.assertEqual(material, None)
# #         # Re-assign the material.
# #         OOF.ElementGroup.Assign_Material(skeleton="skeltest:skelselect",
# #                                          group="testgroup1",
# #                                          material="material1")

# #         # Assign a material to the other overlapping group.
# #         OOF.ElementGroup.Assign_Material(skeleton="skeltest:skelselect",
# #                                          group="testgroup2",
# #                                          material="material2")
# #         # Check that all of the elements in this group have the right
# #         # material.
# #         for elem in self.e_groups.get_group("testgroup2"):
# #             material = elem.material(self.sk_context)
# #             self.assert_(material is not None)
# #             self.assertEqual(material.name(), "material2")
# #         # Check that one element in the first group has had its
# #         # material overwritten by the second group's material.
# #         materials = [e.material(self.sk_context)
# #                      for e in self.e_groups.get_group("testgroup1")]
# #         self.assertEqual(materials.count(None), 0)
# #         matnames = [m.name() for m in materials]
# #         self.assertEqual(matnames.count("material2"), 1)
# #         self.assertEqual(matnames.count("material1"), 3)
# #         # Check that the non-overlapping group has no materials
# #         for elem in self.e_groups.get_group("testgroup3"):
# #             self.assert_(elem.material(self.sk_context) is None)

# #         # Remove material from testgroup2
# #         OOF.ElementGroup.Remove_Material(skeleton="skeltest:skelselect",
# #                                          group="testgroup2")
# #         # Check that all elements in testgroup1 are back to their
# #         # original material.
# #         for elem in self.e_groups.get_group("testgroup1"):
# #             material = elem.material(self.sk_context)
# #             self.assert_(material is not None)
# #             self.assertEqual(material.name(), "material1")
# #         # Check that one element in testgroup2 is material1, and the
# #         # others are None.
# #         materials = [e.material(self.sk_context)
# #                      for e in self.e_groups.get_group("testgroup2")]
# #         self.assertEqual(materials.count(None), 3)
# #         matnames = [m.name() for m in materials if m is not None]
# #         self.assertEqual(len(matnames), 1)
# #         self.assertEqual(matnames[0], "material1")
        
# #         # Check the non-overlapping group again, just to be sure.
# #         for elem in self.e_groups.get_group("testgroup3"):
# #             self.assert_(elem.material(self.sk_context) is None)
        
# #         OOF.Material.Delete(name='material1')
# #         OOF.Material.Delete(name='material2')
        

# class Skeleton_Node_Group(Direct_Node_Selection):
#     def populate_test_group(self):
#         OOF.NodeGroup.New_Group(skeleton="skeltest:skelselect",
#                                    name="testgroup")
#         self.selection_menu.Single_Node(
#             skeleton="skeltest:skelselect",
#             points=[Point(4.95,4.95,4.95)],
#             shift=0, ctrl=0)
#         OOF.NodeGroup.Add_to_Group(skeleton="skeltest:skelselect",
#                                       group="testgroup")
#     def Query_Group(self):
#         self.populate_test_group()
#         OOF.NodeGroup.Query_Group(skeleton="skeltest:skelselect",
#                                      group="testgroup")
#         # This menu item generates a message in the reporter -- see if
#         # it was the right one.
#         global reporter
#         from ooflib.common.IO import reporter
#         mstring = reporter.messagemanager.message_list[-1][0]
#         self.assertEqual(
#             ">>>  1  node",
#             mstring)
        



#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

element_set = [
    Element_Selection_5Color("SingleElement"),
    Element_Selection_5Color("UndoRedo"),
    Element_Selection_5Color("Clear"),
    Element_Selection_5Color("Invert"),
    Element_Selection_5Color("DominantPixel"),
    Element_Selection_5Color("Homogeneity"),
    Element_Selection_5Color("ShapeEnergy"),
    Element_Selection_5Color("Material"),
    Element_Selection_5Color("Expand"),
    #Direct_Element_Selection("Rectangle"),
    #Direct_Element_Selection("Circle"),
    #Direct_Element_Selection("Ellipse"),
    Element_Selection_BlueGreen50("NewGroup"),
    Element_Selection_BlueGreen50("RenameGroup"),
    Element_Selection_BlueGreen50("AddToGroup"),
    Element_Selection_BlueGreen50("SelectFromPixelGroup"),
    Element_Selection_BlueGreen50("SelectGroup"),
    Element_Selection_BlueGreen50("AddGroup"),
    Element_Selection_BlueGreen50("AutoGroup"),
    # For convenience, the remaining tests use AutoGroup to create the
    # groups that they operate on, so they occur after AutoGroup has
    # been tested.
    Element_Selection_BlueGreen50("UnselectGroup"),
    Element_Selection_BlueGreen50("IntersectGroup"),
    Element_Selection_BlueGreen50("RemoveFromGroup"),
    Element_Selection_BlueGreen50("CopyGroup"),
    Element_Selection_BlueGreen50("DeleteGroup"),
    Element_Selection_BlueGreen50("DeleteAllGroups"),
    Element_Selection_BlueGreen50("ClearGroup"),
    Element_Selection_BlueGreen50("ClearAllGroups"),
    Element_Selection_BlueGreen50("Save"),
    Element_Selection_BlueGreen50("Load"),
    ]

face_set = [
    Face_Selection_5Color("SingleFace"),
    Face_Selection_5Color("UndoRedo"),
    Face_Selection_5Color("Clear"),
    Face_Selection_5Color("Invert"),
    Face_Selection_BlueGreen50("NewGroup"),
    Face_Selection_BlueGreen50("RenameGroup"),
    Face_Selection_BlueGreen50("AddToGroup"),
    Face_Selection_BlueGreen50("SelectGroup"),
    Face_Selection_BlueGreen50("AddGroup"),
    # # Face_Selection_BlueGreen50("AutoGroup"),
    Face_Selection_BlueGreen50("UnselectGroup"),
    Face_Selection_BlueGreen50("IntersectGroup"),
    Face_Selection_BlueGreen50("RemoveFromGroup"),
    Face_Selection_BlueGreen50("CopyGroup"),
    Face_Selection_BlueGreen50("DeleteGroup"),
    Face_Selection_BlueGreen50("DeleteAllGroups"),
    Face_Selection_BlueGreen50("ClearGroup"),
    Face_Selection_BlueGreen50("ClearAllGroups"),
    Face_Selection_BlueGreen50("InternalBoundaries"),
    Face_Selection_BlueGreen50("Save"),
    Face_Selection_BlueGreen50("Load"),
    #Direct_Face_Selection("Rectangle"),
    #Direct_Face_Selection("Circle"),
    #Direct_Face_Selection("Ellipse"),
    # Direct_Face_Selection("Invert"),
    ]

segment_set = [
    Segment_Selection_5Color("SingleSegment"),
    Segment_Selection_BlueGreen50("SingleSegment2"),
    Segment_Selection_5Color("UndoRedo"),
    Segment_Selection_5Color("Clear"),
    Segment_Selection_5Color("Invert"),
    Segment_Selection_5Color("Homogeneity"),
    Segment_Selection_BlueGreen50("NewGroup"),
    Segment_Selection_BlueGreen50("RenameGroup"),
    Segment_Selection_BlueGreen50("AddToGroup"),
    Segment_Selection_BlueGreen50("SelectGroup"),
    Segment_Selection_BlueGreen50("AddGroup"),
    Segment_Selection_BlueGreen50("AutoGroup"),
    Segment_Selection_BlueGreen50("UnselectGroup"),
    Segment_Selection_BlueGreen50("IntersectGroup"),
    Segment_Selection_BlueGreen50("RemoveFromGroup"),
    Segment_Selection_BlueGreen50("CopyGroup"),
    Segment_Selection_BlueGreen50("DeleteGroup"),
    Segment_Selection_BlueGreen50("DeleteAllGroups"),
    Segment_Selection_BlueGreen50("ClearGroup"),
    Segment_Selection_BlueGreen50("ClearAllGroups"),
    Segment_Selection_BlueGreen50("InternalBoundaries"),
    Segment_Selection_BlueGreen50("Save"),
    Segment_Selection_BlueGreen50("Load"),
    ]

node_set = [
    Node_Selection_5Color("SingleNode"),
    Node_Selection_5Color("UndoRedo"),
    Node_Selection_5Color("Clear"),
    Node_Selection_5Color("Invert"),
    Node_Selection_5Color("Expand"),
    Node_Selection_BlueGreen50("InternalBoundaries"),
    Node_Selection_5Color("NamedBdy"),
    Node_Selection_BlueGreen50("NewGroup"),
    Node_Selection_BlueGreen50("RenameGroup"),
    Node_Selection_BlueGreen50("AddToGroup"),
    Node_Selection_BlueGreen50("SelectGroup"),
    Node_Selection_BlueGreen50("AddGroup"),
    Node_Selection_BlueGreen50("AutoGroup"),
    Node_Selection_BlueGreen50("UnselectGroup"),
    Node_Selection_BlueGreen50("IntersectGroup"),
    Node_Selection_BlueGreen50("RemoveFromGroup"),
    Node_Selection_BlueGreen50("CopyGroup"),
    Node_Selection_BlueGreen50("DeleteGroup"),
    Node_Selection_BlueGreen50("DeleteAllGroups"),
    Node_Selection_BlueGreen50("ClearGroup"),
    Node_Selection_BlueGreen50("ClearAllGroups"),
    #Node_Selection_5Color("Rectangle"),
    #Node_Selection_5Color("Circle"),
    #Node_Selection_5Color("Ellipse"),
    Node_Selection_BlueGreen50("Save"),
    Node_Selection_BlueGreen50("Load"),
    ]

# These sets of tests rely on earlier tests in other categories.

element_set2 = [
    Element_Selection_BlueGreen50("SelectFromNodes"),
    Element_Selection_BlueGreen50("SelectFromSegments"),
    Element_Selection_BlueGreen50("SelectFromFaces")
]

node_set2 = [
     Node_Selection_BlueGreen50("SelectFromSegments"),
     Node_Selection_BlueGreen50("SelectFromElements"),
     Node_Selection_BlueGreen50("SelectFromFaces"),
]

segment_set2 = [
    Segment_Selection_BlueGreen50("SelectFromNodes"),
    Segment_Selection_BlueGreen50("SelectFromElements"),
    Segment_Selection_BlueGreen50("SelectFromFaces"),
]

face_set2 = [
    Face_Selection_BlueGreen50("SelectFromElements"),
    Face_Selection_BlueGreen50("SelectFromNodes"),
    Face_Selection_BlueGreen50("SelectFromSegments"),
]

# These tests rely on tests in set2.

node_set3 = [
    Node_Selection_BlueGreen50("SelectFromMultipleFaces")
]

    

test_set = (element_set + face_set + segment_set + node_set +
            element_set2 + node_set2 + segment_set2 + face_set2 +
            node_set3)

#test_set = node_set3
