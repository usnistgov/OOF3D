# -*- python -*-
# $RCSfile: skeleton_select_test.py,v $
# $Revision: 1.1.2.30 $
# $Author: langer $
# $Date: 2014/12/01 20:48:38 $

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
        OOF.Windows.Graphics.New()
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
        OOF.Graphics_1.File.Close()
        OOF.Material.Delete(name="thing1")
        OOF.Material.Delete(name="thing2")

class Skeleton_Selection_BlueGreen50(Skeleton_Selection):
    # The bluegreen50 image is a 10x10x10 cube, divided into two equal
    # parts at z=5.  The small z half is blue (#868cfe) and the large
    # z half is green (#a1fc93).
    def setUp(self):
        Skeleton_Selection.setUp(self)
        OOF.Windows.Graphics.New()
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file('ms_data','bluegreen50'),
                sort=NumericalOrder()),
            microstructure_name='skeltest',
            height=automatic, width=automatic, depth=automatic)
        OOF.Image.AutoGroup(image="skeltest:bluegreen50", name_template='%c')
    def tearDown(self):
        OOF.Graphics_1.File.Close()

class Skeleton_Selection_TwoWalls(Skeleton_Selection):
    skeletonpath = "two_walls:skeleton"
    def setUp(self):
        Skeleton_Selection.setUp(self)
        OOF.Windows.Graphics.New()
        OOF.File.LoadStartUp.Data(
            filename=reference_file("skeleton_data", 'two_walls.skeleton'))
    def tearDown(self):
        OOF.Graphics_1.File.Close()

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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(6.37197,13.4461,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        ids = self.selectionIDs()
        self.assertEqual(ids, [255])
        # Select an interior element by clipping the display
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(-38.3282,7.57619,40.5221)], 
            view=View(cameraPosition=Coord(-39.4091,7.48683,41.251),
                      focalPoint=Coord(10,10,10),
                      up=Coord(-0.0411954,0.999035,0.0152096),
                      angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.01]], 
                      invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [205])
        # shift-click to select an additional element on the unclipped
        # display
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(13.9736,5.34458,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertEqual(self.selectionIDs(), [75, 205])
        # control-click to toggle it off
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(14.698,5.17413,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=1)
        self.assertEqual(self.selectionIDs(), [205])
        # control-click to toggle it back on
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(14.698,5.17413,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=1)
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(8.81206,10.2569,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(14.1417,14.5377,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(14.1417,14.5377,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(7.37797,13.81,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [26])
        OOF.ElementSelection.Invert(skeleton='skeltest:skeleton')
        elist.remove(26)
        self.assertEqual(self.selectionIDs(), elist)

    @memorycheck.check("skeltest")
    def DominantPixel(self):
        self.makeSkeleton(4, 4, 4)
        # Click on a green voxel
        OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel(
            skeleton='skeltest:skeleton',
            points=[Point(14.9979,5.65493,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 38)
        indices = [40, 43, 44, 46, 48, 60, 61, 63, 64, 65, 66, 67, 68, 69,
                   70, 71, 72, 73, 74, 75, 77, 125, 127, 145, 146, 147, 148,
                   149, 150, 151, 152, 153, 154, 156, 158, 230, 233, 234]
        self.assertEqual(indices, self.selectionIDs())
        # Click on a different green voxel, from a different point of view.
        OOF.Graphics_1.Toolbox.Select_Element.ByDominantPixel(
            skeleton='skeltest:skeleton',
            points=[Point(6.95145,5.4335,-48.1508)],
            view=View(cameraPosition=Coord(6.93943,5.4413,-48.2585), 
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.155032,0.984232,-0.0851602),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(indices, self.selectionIDs())

    @memorycheck.check("skeltest")
    def Homogeneity(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        OOF.ElementSelection.Select_by_Homogeneity(
            skeleton='skeltest:skeleton', 
            threshold=0.6)
        self.assertEqual(self.selection().size(), 41)
        indices = [21, 24, 42, 50, 52, 53, 54, 70, 96, 131, 132, 133,
                   134, 141, 143, 144, 147, 151, 165, 172, 175, 177, 
                   178, 179, 181, 183, 184, 187, 191, 192, 198, 201, 
                   211, 212, 216, 229, 230, 250, 268, 280, 295]
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def ShapeEnergy(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        # In a cubically symmetric Skeleton the tets at the corners of
        # each cubical subunit have shape energy 0.159104 and the ones
        # at the centers have shape energy 0.0.
        OOF.ElementSelection.Select_by_Shape_Energy(
            skeleton='skeltest:skeleton',
            threshold=1.0)
        # No elements have shape energy >= 1
        self.assertEqual(self.selection().size(), 0)
        OOF.ElementSelection.Select_by_Shape_Energy(
            skeleton='skeltest:skeleton',
            threshold=0.1)
        # Only the corners are selected.
        self.assertEqual(self.selection().size(), 256)
        OOF.ElementSelection.Select_by_Shape_Energy(
            skeleton='skeltest:skeleton',
            threshold=0.0)
        # All elements are selected.
        self.assertEqual(self.selection().size(), 320)

    @memorycheck.check("skeltest")
    def Material(self):
        self.makeSkeleton(4, 4, 4)
        OOF.ElementSelection.Select_by_Material(
            skeleton='skeltest:skeleton', material='thing1')
        self.assertEqual(self.selection().size(), 110)
        OOF.ElementSelection.Select_by_Material(
            skeleton='skeltest:skeleton', material='thing2')
        self.assertEqual(self.selection().size(), 91)
        OOF.ElementSelection.Select_by_Material(
            skeleton='skeltest:skeleton', material='<Any>')
        self.assertEqual(self.selection().size(), 201)
        OOF.ElementSelection.Select_by_Material(
            skeleton='skeltest:skeleton', material='<None>')
        self.assertEqual(self.selection().size(), 119)

    @memorycheck.check("skeltest")
    def Expand(self):
        self.makeSkeleton(4, 4, 4)
        # Select an interior element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(-38.3282,7.57619,40.5221)], 
            view=View(cameraPosition=Coord(-39.4091,7.48683,41.251),
                      focalPoint=Coord(10,10,10),
                      up=Coord(-0.0411954,0.999035,0.0152096),
                      angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 10.01]], 
                      invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [205])
        # Expand via faces
        OOF.ElementSelection.Expand(
            skeleton='skeltest:skeleton', mode='Faces')        
        indices = [126, 185, 205, 209, 213]
        self.assertEqual(indices, self.selectionIDs())
        # Undo
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual([205], self.selectionIDs())
        # Expand via segments
        OOF.ElementSelection.Expand(
            skeleton='skeltest:skeleton', mode='Segments')
        indices = [106, 126, 127, 129, 132, 185, 187, 189, 193,
                   205, 206, 207, 208, 209, 212, 213, 214]
        self.assertEqual(indices, self.selectionIDs())
        # Undo
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual([205], self.selectionIDs())
        # Expand via nodes
        OOF.ElementSelection.Expand(
            skeleton='skeltest:skeleton', mode='Nodes')
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(9.28624,15.0176,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(10.5646,14.975,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=1, ctrl=0)

        
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(5.49945,6.25114,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), 
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [35])
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [35])
        # Select another element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(5.31783,4.16255,21.9826)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(5.49945,6.25114,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), 
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [35])
        # Select the elements in the empty group
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [])
        # Undo the selection of the empty group
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        # Make the group non-empty
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.Graphics_1.Toolbox.Select_Element.Clear(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select the element in the group
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [35])
        # Select a different element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(-22.723,-3.11097,0.735203)],
            view=View(cameraPosition=Coord(-22.7831,-3.12125,0.734417), 
                      focalPoint=Coord(5,5,5), 
                      up=Coord(-0.177623,0.859443,-0.479382), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [3])
        # Select the element in the group and make sure that the
        # different element is not selected.
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [35])

    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select an element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(5.49945,6.25114,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), 
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [35])
        # Add the elements in the empty group to the selection and
        # make sure the selected element stays selected.
        OOF.ElementSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [35])
        # Make the group non-empty
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.Graphics_1.Toolbox.Select_Element.Clear(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection.
        OOF.ElementSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [35])
        # Select a different element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(-22.723,-3.11097,0.735203)],
            view=View(cameraPosition=Coord(-22.7831,-3.12125,0.734417), 
                      focalPoint=Coord(5,5,5), 
                      up=Coord(-0.177623,0.859443,-0.479382), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [3])
        # Add the group to the selection and make sure both elements
        # are selected.
        OOF.ElementSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [3, 35])

    @memorycheck.check("skeltest")
    def SelectFromPixelGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementSelection.Select_by_Pixel_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_elems)
        OOF.ElementSelection.Select_by_Pixel_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
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
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Select the other
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), self.blue_elems)

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Unselect the empty group
        OOF.ElementSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Unselect a non-empty but non intersecting group
        OOF.ElementSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Unselect the green group
        OOF.ElementSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), [])
        # Select a single element and put it in newgroup
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(-22.7261,-3.10941,0.752654)],
            view=View(cameraPosition=Coord(-22.7831,-3.12125,0.734417), 
                      focalPoint=Coord(5,5,5), 
                      up=Coord(-0.177623,0.859443,-0.479382),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [5])
        # Reselect the green group
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Unselect the single element in newgroup
        OOF.ElementSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
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
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Intersect it with itself
        OOF.ElementSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Intersect it with the (disjoint) blue group
        OOF.ElementSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the green group and intersect it with the empty
        # group
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        OOF.ElementSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [])
        # Add all the elements to newgroup
        OOF.ElementSelection.Invert(skeleton='skeltest:skeleton')
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group and intersect it with the full group
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        OOF.ElementSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), self.green_elems)
        # Reselect the full group and intersect it with the green group
        OOF.ElementSelection.Select_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        OOF.ElementSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_elems)
        
    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Use autogroup to create the groups
        OOF.ElementGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        # Select a single green element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(6.2906,5.79847,21.9826)], 
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
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
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(4.99467,4.96271,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        self.assertEqual(self.selectionIDs(), [6, 16, 25, 35])
        # Select three nodes along the bottom edge
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.34205,2.31009,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(4.96271,2.34205,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655), 
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(7.66861,2.33139,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=1, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        self.assertEqual(self.selectionIDs(), [5, 6, 8, 9, 15, 16, 18, 19])
        # Select the 4 nodes of the upper front left tet
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.33936,7.67199,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0, size_x=621,
                      size_y=615),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.98298,7.64929,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0, size_x=621,
                      size_y=615),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.7932,7.19545,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0, size_x=621,
                      size_y=615),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.35071,4.98298,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0, size_x=621,
                      size_y=615),
            shift=1, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=2)
        self.assertEqual(self.selectionIDs(), [25, 26, 27, 28, 29])
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=3)
        self.assertEqual(self.selectionIDs(), [26, 29])
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=4)
        self.assertEqual(self.selectionIDs(), [26])
    

    @memorycheck.check("skeltest")
    def SelectFromSegments(self):
        self.makeSkeleton(2, 2, 2)
        # Select a segment on the top edge
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(5.90019,7.66861,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [36])
        # Select one on the front face
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(6.27305,5.03729,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [16, 35])
        # Select two segments that share elements
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.20219,-6.264,28.4005)],
            view=View(cameraPosition=Coord(4.97981,-7.82366,31.2983),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.00634074,0.898813,0.438286), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.28479,-6.37816,28.3449)],
            view=View(cameraPosition=Coord(4.97981,-7.82366,31.2983),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.00634074,0.898813,0.438286), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=1, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [11, 16, 17, 19, 30, 35, 38, 39])

    @memorycheck.check("skeltest")
    def SelectFromFaces(self):
        self.makeSkeleton(2, 2, 2)
        # Select a face on the front
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.783,5.45276,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [35])
        # Select two internal faces
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-21.1376,5.27189,4.58318)],
            view=View(cameraPosition=Coord(-24.2583,5,5),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 3.0, 0]], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(-21.1376,5.33602,4.71143)], 
            view=View(cameraPosition=Coord(-24.2583,5,5),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 3.0, 0]], invertClip=0,
                      size_x=691, size_y=652),
            shift=1, ctrl=0)


        OOF.ElementSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [21, 23, 24])
      
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
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(10.5886,11.3485,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1237])
        # Select an interior face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(-39.9119,15.3349,37.4114)], 
            view=View(cameraPosition=Coord(-41.0587,15.4379,38.0648),
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.131699,0.990139,0.0477514), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 5.0]], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1030])
        # shift-click to select an additional face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(10.5859,10.3942,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertEqual(self.selectionIDs(), [1030, 1237])
        # control-click
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(10.5859,10.3942,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=1)
        self.assertEqual(self.selectionIDs(), [1030])
        # control-click again
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(10.5859,10.3942,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=1)
        self.assertEqual(self.selectionIDs(), [1030, 1237])

    @memorycheck.check("skeltest")
    def UndoRedo(self):
        self.makeSkeleton(4, 4, 4)
        sel0 = id(self.selection().currentSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(9.41408,11.1825,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        sel1 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel1)
        self.assertEqual(self.selectionIDs(), [1151])
        # Undo
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        sel2 = id(self.selection().currentSelection())
        self.assertEqual(sel0, sel2)
        self.assertEqual(self.selectionIDs(), [])
        # Redo
        OOF.FaceSelection.Redo(skeleton='skeltest:skeleton')
        sel3 = id(self.selection().currentSelection())
        self.assertEqual(sel1, sel3)
        self.assertEqual(self.selectionIDs(), [1151])
        # Select another face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.7494,5.34458,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        sel4 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel4)
        self.assertNotEqual(sel1, sel4)
        self.assertEqual(self.selectionIDs(), [238])
        # Undo
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel1)
        self.assertEqual(self.selectionIDs(), [1151])
        # Undo again
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel0)
        self.assertEqual(self.selectionIDs(), [])
        # Redo twice
        OOF.FaceSelection.Redo(skeleton='skeltest:skeleton')     
        OOF.FaceSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel4)
        self.assertEqual(self.selectionIDs(), [238])
        
    @memorycheck.check("skeltest")
    def Clear(self):
        self.makeSkeleton(4, 4, 4)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(6.82146,8.86557,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [680])
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
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(8.83347,8.54451,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [86])
        OOF.FaceSelection.Invert(skeleton='skeltest:skeleton')
        facelist.remove(86)
        self.assertEqual(self.selectionIDs(), facelist)

# end Face_Selection_5Color

def makeFaceGroups():
     # The Element, Segment, and Node tests use AutoGroup to create
     # groups, but AutoGroup hasn't been implemented for Faces yet.
     # Instead, this utility function creates and populates two
     # groups.  

    # This function is called from other test modules, and when it's
    # called that way, the oof namespace isn't imported to this
    # module, so we have to import some classes manually.
    from ooflib.common.IO.mainmenu import OOF
    from ooflib.SWIG.common.coord import Coord
    from ooflib.common.primitives import Point
    from ooflib.SWIG.common.IO.view import View
    def clickPt(pt, shift):
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[pt],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=shift, ctrl=0)
    clickPt(Point(3.71355,6.5841,21.9826), 0)
    clickPt(Point(4.33912,6.1906,21.9826), 1)
    clickPt(Point(5.18666,6.20069,21.9826), 1)
    clickPt(Point(6.30663,6.70518,21.9826), 1)
    OOF.FaceGroup.New_Group(
        skeleton='skeltest:skeleton', name='groupA')
    OOF.FaceGroup.Add_to_Group(
        skeleton='skeltest:skeleton', group='groupA')

    clickPt(Point(3.78418,4.16255,21.9826), 0)
    clickPt(Point(3.50166,3.32509,21.9826), 1)
    clickPt(Point(5.3481,3.96075,21.9826), 1)
    clickPt(Point(6.47816,3.20401,21.9826), 1)
    OOF.FaceGroup.New_Group(
        skeleton='skeltest:skeleton', name='groupB')
    OOF.FaceGroup.Add_to_Group(
        skeleton='skeltest:skeleton', group='groupB')

a_faces = [194, 204, 243, 253]
b_faces = [76, 86, 140, 146]

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
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(4.44884,5.90968,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [194])
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [194])
        # Select another face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.58327,4.0047,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [146])
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [146, 194])
        # Re-add the same face
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [146, 194])

    @memorycheck.check("skeltest")
    def SelectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.49945,6.25114,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), 
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [243])
        # Select the faces in the empty group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [])
        # Undo the selection of the empty group
        OOF.FaceSelection.Undo(skeleton='skeltest:skeleton')
        # Make the group non-empty
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.Graphics_1.Toolbox.Select_Face.Clear(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select the face in the group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [243])
        # Select a different face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(3.34652,3.69434,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [76])
        # Select the face in the group and make sure that the
        # different face is not selected.
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [243])

    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(3.12834,5.89799,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [204])
        # Add the faces in the empty group to the selection and
        # make sure the selected face stays selected.
        OOF.FaceSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [204])
        # Make the group non-empty
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', 
            group='newgroup')
        # Clear the selection
        OOF.Graphics_1.Toolbox.Select_Face.Clear(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection.
        OOF.FaceSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [204])
        # Select a different face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(6.9322,3.7085,21.9826)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [140])
        # Add the group to the selection and make sure both faces
        # are selected.
        OOF.FaceSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [140, 204])

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton', group='groupA')
        # Unselect the empty group
        OOF.FaceSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), a_faces)
        # Unselect a non-empty but non intersecting group
        OOF.FaceSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='groupB')
        self.assertEqual(self.selectionIDs(), a_faces)
        # Unselect the actually selected group
        OOF.FaceSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='groupA')
        self.assertEqual(self.selectionIDs(), [])
        # Select a single face and put it in newgroup.  The selected
        # face is already in groupA.
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(5.50835,6.27356,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [243])
        # Reselect the first group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton', group='groupA')
        # Unselect the single face in newgroup
        OOF.FaceSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        indices = a_faces[:]
        indices.remove(243)
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def IntersectGroup(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the A group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton', group='groupA')
        # Intersect it with itself
        OOF.FaceSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='groupA')
        self.assertEqual(self.selectionIDs(), a_faces)
        # Intersect it with the (disjoint) B group
        OOF.FaceSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='groupB')
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the A group and intersect it with the empty
        # group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton', group='groupA')
        OOF.FaceSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [])
        # Add all the faces to newgroup
        OOF.FaceSelection.Invert(skeleton='skeltest:skeleton')
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the A group and intersect it with the full group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton', group='groupA')
        OOF.FaceSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), a_faces)
        # Reselect the full group and intersect it with the A group
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        OOF.FaceSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='groupA')
        self.assertEqual(self.selectionIDs(), a_faces)

    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        makeFaceGroups()
        # Select a single A face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(3.87499,6.7859,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [204])
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
        indices.remove(204)
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
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(4.2455,5.9739,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(self.selectionIDs(), [83, 192, 193, 194])
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Interior')
        self.assertEqual(self.selectionIDs(), [])
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertEqual(self.selectionIDs(), [83, 192, 193, 194])
        # Select another adjacent element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(4.42744,3.82276,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(self.selectionIDs(), [83, 84, 85, 86, 192, 193, 194])
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertEqual(self.selectionIDs(), [84, 85, 86, 192, 193, 194])
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Interior')
        self.assertEqual(self.selectionIDs(), [83])

    @memorycheck.check("skeltest")
    def SelectFromNodes(self):
        self.makeSkeleton(2, 2, 2)
        # Select a corner node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(3.08967,6.86217,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        self.assertEqual(self.selectionIDs(), [178, 179, 181])
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=2)
        self.assertEqual(self.selectionIDs(), [])
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=3)
        self.assertEqual(self.selectionIDs(), [])
        # Select an adjacent node as well
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(5.01605,6.87288,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        self.assertEqual(
            self.selectionIDs(),
            [169, 170, 171, 178, 179, 180, 181, 184, 185, 186, 224, 225,
             232, 233, 234, 237, 238])
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=2)
        self.assertEqual(self.selectionIDs(), [179, 181])
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=3)
        self.assertEqual(self.selectionIDs(), [])
        # Select just the center node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(4.98247,12.0767,24.4841)], 
            view=View(cameraPosition=Coord(5,15.0069,32.4938),
                      focalPoint=Coord(5,5,5), up=Coord(0,0.939693,-0.34202),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        self.assertEqual(
            self.selectionIDs(),        
            [34, 35, 37, 45, 46, 47, 53, 54, 56, 83, 84, 85, 90, 91, 94, 96,
             102, 104, 111, 113, 114, 119, 120, 144, 145, 149, 150, 153, 161,
             162, 170, 171, 172, 184, 186, 192, 193, 207, 209, 211, 218, 220,
             225, 226, 237, 242, 255, 258])
        OOF.FaceSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=2)
        self.assertEqual(self.selectionIDs(), [])

    @memorycheck.check("skeltest")
    def SelectFromSegments(self):
        self.makeSkeleton(2, 2, 2)
        # Start with a segment along an edge
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(2.30841,6.28426,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.FaceSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [201, 204])
        # Add a segment that shares a tet with the first one.
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.54986,6.23075,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.FaceSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [192, 194, 201, 203, 204])

    @memorycheck.check("skeltest")
    def InternalBoundaries(self):
        self.makeSkeleton(4, 4, 4)
        OOF.FaceSelection.Select_Internal_Boundaries(
            skeleton='skeltest:skeleton')
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

class Face_Selection_TwoWalls(Skeleton_Selection_TwoWalls, Face_Selection):
    # This operation used to select the wrong faces because the front
    # and back vtk clipping planes weren't being reset correctly.
    @memorycheck.check("two_walls")
    def DefaultClipTest(self):
        OOF.Graphics_1.Layer.Edit(
            n=0, category='Image',
            what='two_walls:two_walls',
            how=BitmapDisplayMethod(
                filter=VoxelNot(a=VoxelGroupFilter(group='#000000'))))
        OOF.Graphics_1.Settings.Camera.View(
            view=View(cameraPosition=Coord(-26.9322,98.0598,93.9657),
                      focalPoint=Coord(25,25,5),
                      up=Coord(0.818648,-0.105512,0.56452), angle=30,
                      clipPlanes=[], invertClip=0, size_x=614, size_y=550))
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='two_walls:skeleton',
            points=[Point(-21.9322,90.7391,82.2603)],
            view=View(cameraPosition=Coord(-26.9322,98.0598,93.9657),
                      focalPoint=Coord(25,25,5),
                      up=Coord(0.818648,-0.105512,0.56452), angle=30,
                      clipPlanes=[], invertClip=0, size_x=614, size_y=550),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='two_walls:skeleton',
            points=[Point(-22.6394,90.233,82.263)],
            view=View(cameraPosition=Coord(-26.9322,98.0598,93.9657),
                      focalPoint=Coord(25,25,5),
                      up=Coord(0.818648,-0.105512,0.56452), angle=30,
                      clipPlanes=[], invertClip=0, size_x=614, size_y=550),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='two_walls:skeleton',
            points=[Point(-22.801,89.5835,82.7021)],
            view=View(cameraPosition=Coord(-26.9322,98.0598,93.9657),
                      focalPoint=Coord(25,25,5),
                      up=Coord(0.818648,-0.105512,0.56452), angle=30,
                      clipPlanes=[], invertClip=0, size_x=614, size_y=550),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='two_walls:skeleton',
            points=[Point(-22.2825,89.2607,83.2699)],
            view=View(cameraPosition=Coord(-26.9322,98.0598,93.9657),
                      focalPoint=Coord(25,25,5),
                      up=Coord(0.818648,-0.105512,0.56452), angle=30,
                      clipPlanes=[], invertClip=0, size_x=614, size_y=550),
            shift=1, ctrl=0)
        self.assertEqual(self.selectionIDs(), [301, 311, 411, 421])

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Segment_Selection_5Color(Skeleton_Selection_5Color, Segment_Selection):
    @memorycheck.check("skeltest")
    def SingleSegment(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selection().size(), 0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(5.92248,10.7706,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1026])
        # Selection from a clipped and rotated view
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(-39.4667,13.0117,40.867)],
            view=View(cameraPosition=Coord(-39.5685,13.0046,40.9538),
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.0384205,0.998634,-0.0354098), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 5.0]], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [1470])
        # Shift-click
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(10.5458,14.3237,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertEqual(self.selectionIDs(), [1470, 1591])
        # Control-click to deselect
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(8.72644,13.1678,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=1)
        self.assertEqual(self.selectionIDs(), [1591])
        # Control-click to reselect
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(8.72644,13.1678,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=1)
        self.assertEqual(self.selectionIDs(), [1470, 1591])
    
    @memorycheck.check("skeltest")
    def UndoRedo(self):
        self.makeSkeleton(4, 4, 4)
        sel0 = id(self.selection().currentSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one Segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(5.92248,10.7706,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        # Check that the selection object is different
        sel1 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel1)
        # And that the right Segment is selected
        self.assertEqual(self.selectionIDs(), [1026])
        # Undo
        OOF.SegmentSelection.Undo(skeleton='skeltest:skeleton')
        sel2 = id(self.selection().currentSelection())
        self.assertEqual(sel0, sel2)
        self.assertEqual(self.selectionIDs(), [])
        # Redo
        OOF.SegmentSelection.Redo(skeleton='skeltest:skeleton')
        sel3 = id(self.selection().currentSelection())
        self.assertEqual(sel1, sel3)
        self.assertEqual(self.selectionIDs(), [1026])
        # Select another Segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(-39.4667,13.0117,40.867)],
            view=View(cameraPosition=Coord(-39.5685,13.0046,40.9538),
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.0384205,0.998634,-0.0354098), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 5.0]], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        sel4 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel4)
        self.assertNotEqual(sel1, sel4)
        self.assertEqual(self.selectionIDs(), [1470])
        # Undo
        OOF.SegmentSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel1)
        self.assertEqual(self.selectionIDs(), [1026])
        # Undo again
        OOF.SegmentSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel0)
        self.assertEqual(self.selectionIDs(), [])
        # Redo twice
        OOF.SegmentSelection.Redo(skeleton='skeltest:skeleton')
        OOF.SegmentSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel4)
        self.assertEqual(self.selectionIDs(), [1470])

    @memorycheck.check("skeltest")
    def Clear(self):
        self.makeSkeleton(4, 4, 4)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(8.74785,7.28166,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [356])
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
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(7.5278,11.3057,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [177])
        # Invert. All but one segment should be selected.
        OOF.SegmentSelection.Invert(skeleton='skeltest:skeleton')
        edgelist.remove(177)
        self.assertEqual(self.selectionIDs(), edgelist)

    @memorycheck.check("skeltest")
    def Homogeneity(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        OOF.SegmentSelection.Select_by_Homogeneity(
            skeleton='skeltest:skeleton', threshold=0.5)
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
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(4.0566,6.65473,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [189])
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [189])
        # Select another segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(6.20573,4.43497,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [117])
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [117, 189])
        # Re-add the same element
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [117, 189])

    @memorycheck.check("skeltest")
    def SelectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.99934,6.53165,21.9826)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [241])
        # Select the segments in the empty group
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
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
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [241])
        # Select a different segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.50853,3.96049,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [68])
        # Select the segment in the group again.  The previously
        # selected segment should be deselected.
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [241])

    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.99934,6.53165,21.9826)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [241])
        # Add the segments in the empty group to the selection and
        # make sure the selected segment stays selected.
        OOF.SegmentSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [241])
        # Make the group non-empty
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        # Clear the selection
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection
        OOF.SegmentSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [241])
        # Select a different segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.50853,3.96049,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [68])
        # Add the group to the selection and make sure both segments
        # are selected.
        OOF.SegmentSelection.Add_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [68, 241])

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
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_segs)
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), self.blue_segs)

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Unselect the empty group
        OOF.SegmentSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Unselect a non-empty but non intersecting group
        OOF.SegmentSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Unselect the green group
        OOF.SegmentSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), [])
        # Select a single segment and put it in newgroup
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.50853,3.96049,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [68])
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Unselect the single segment in newgroup
        OOF.SegmentSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        indices = self.green_segs[:]
        indices.remove(68)
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def IntersectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Intersect it with itself
        OOF.SegmentSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Intersect it with the (disjoint) blue group
        OOF.SegmentSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the green group and intersect it with the empty
        # group
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        OOF.SegmentSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [])
        # Add all the segments to newgroup
        OOF.SegmentSelection.Invert(skeleton='skeltest:skeleton')
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group and intersect it with the full group
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        OOF.SegmentSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), self.green_segs)
        # Reselect the full group and intersect it with the green group
        OOF.SegmentSelection.Select_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        OOF.SegmentSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_segs)

    @memorycheck.check("skeltest")
    def SingleSegment2(self):
        self.makeSkeleton(2, 2, 2)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(2.66241,6.36212,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652
                      ),
            shift=0, ctrl=0)
        # When this test was recorded, it seemed to select segment 198
        # in text mode and 196 in gui mode.  I can't reproduce that
        # inconsistency.  It's selecting 198 in both modes now.
        self.assertEqual(self.selectionIDs(), [198])
        
    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.SegmentGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.40077,5.95853,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0,
                      size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [189])
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
        indices.remove(189)
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
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(0.770387,12.0376,27.9601)], 
            view=View(cameraPosition=Coord(-0.0632398,13.4496,32.5503),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.00274918,0.956184,-0.292753), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.SegmentSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        self.assertEqual(self.selectionIDs(), 
                         [28, 29, 32, 40, 43, 49, 80, 81, 82, 99, 106,
                          108, 143, 158, 165, 168, 191, 215])
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')
        OOF.SegmentSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=2)
        self.assertEqual(self.selectionIDs(), [])
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')
        # Select an additional node in center of the front face
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(0.947145,11.7666,28.0757)],
            view=View(cameraPosition=Coord(-0.0632398,13.4496,32.5503),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.00274918,0.956184,-0.292753), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.SegmentSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        self.assertEqual(self.selectionIDs(), 
                         [28, 29, 32, 40, 43, 49, 78, 79, 80, 81, 82, 99,
                          106, 108, 142, 143, 158, 165, 168, 190, 191, 215])
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')
        OOF.SegmentSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=2)
        self.assertEqual(self.selectionIDs(), [81])
                         
    @memorycheck.check("skeltest")
    def SelectFromElements(self):
        self.makeSkeleton(2, 2, 2)
        # Select a single element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(3.16458,5.67424,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(self.selectionIDs(), [78, 80, 81, 189, 190, 191])
        # Select the cluster of elements around the center node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(0.770387,12.0376,27.9601)], 
            view=View(cameraPosition=Coord(-0.0632398,13.4496,32.5503),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.00274918,0.956184,-0.292753), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton')
        # Select all segments in the element cluster
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(
            self.selectionIDs(), 
            [28, 29, 30, 31, 32, 33, 39, 40, 41, 42, 43, 49, 50, 51, 52, 68,
             71, 72, 78, 79, 80, 81, 82, 88, 93, 99, 100, 101, 106, 107, 108,
             109, 110, 116, 117, 131, 134, 135, 142, 143, 148, 157, 158, 159,
             164, 165, 166, 167, 168, 177, 183, 189, 190, 191, 198, 200, 206, 
             215, 216, 217, 222, 223, 230, 241, 247, 249])
        # Select just the external segments in the cluster
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertEqual(
            self.selectionIDs(),
            [30, 31, 33, 39, 41, 42, 50, 51, 52, 68, 71, 72, 78, 79, 88, 93, 
             100, 101, 107, 109, 110, 116, 117, 131, 134, 135, 142, 148, 157, 
             159, 164, 166, 167, 177, 183, 189, 190, 198, 200, 206, 216, 217,
             222, 223, 230, 241, 247, 249])
        # Select just the internal segments
        OOF.SegmentSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton', 
            coverage='Interior')
        self.assertEqual(
            self.selectionIDs(),
            [28, 29, 32, 40, 43, 49, 80, 81, 82, 99, 106, 108, 143, 158, 165,
             168, 191, 215])

    @memorycheck.check("skeltest")
    def SelectFromFaces(self):
        self.makeSkeleton(2, 2, 2)
        # Select one face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(4.65218,5.41738,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        # Select all segments of the face
        OOF.SegmentSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(self.selectionIDs(), [78, 189, 190])
        # Select the internal segments of the face
        OOF.SegmentSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='Interior')
        self.assertEqual(self.selectionIDs(), [])
        # Select the external segments of the face
        OOF.SegmentSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertEqual(self.selectionIDs(), [78, 189, 190])
        # Select an adjacent face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.52976,6.4769,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        # Select all segments of the faces
        OOF.SegmentSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(self.selectionIDs(), [78, 142, 189, 190, 241])
        # Select the internal segments of the face
        OOF.SegmentSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='Interior')
        self.assertEqual(self.selectionIDs(), [190])
        # Select the external segments of the face
        OOF.SegmentSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertEqual(self.selectionIDs(), [78, 142, 189, 241])
    
    @memorycheck.check('skeltest')
    def InternalBoundaries(self):
        self.makeSkeleton(4, 4, 4)
        OOF.SegmentSelection.Select_Internal_Boundaries(
            skeleton='skeltest:skeleton')
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
        # Click not on a node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(8.64083,11.3271,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 0)
        # Click on a node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(7.31376,9.95719,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [59])
        # Click from a clipped and rotated view
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(-30.1088,37.5285,42.246)],
            view=View(cameraPosition=Coord(-30.2019,37.6015,42.3445),
                      focalPoint=Coord(10,10,10),
                      up=Coord(0.288573,0.875226,-0.388207), angle=30, 
                      clipPlanes=[[1.0, 0.0, 0.0, 4.0]], invertClip=0,
                      size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selection().size(), 1)
        self.assertEqual(self.selectionIDs(), [56])
        # Shift-click
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(12.729,10.0214,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertEqual(self.selection().size(), 2)
        self.assertEqual(self.selectionIDs(), [56, 69])
        # Control-click to deselect
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(7.95589,9.93579,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=1)
        self.assertEqual(self.selectionIDs(), [69])
        # Control-click to reselect
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(7.95589,9.93579,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=1)
        self.assertEqual(self.selectionIDs(), [56, 69])

    @memorycheck.check("skeltest")
    def UndoRedo(self):
        self.makeSkeleton(4, 4, 4)
        sel0 = id(self.selection().currentSelection())
        self.assertEqual(self.selectionIDs(), [])
        # Select one Node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(15.319,10,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        # Check that the selection object is different
        sel1 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel1)
        # And that the right Node is selected
        self.assertEqual(self.selectionIDs(), [74])
        # Undo
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        sel2 = id(self.selection().currentSelection())
        self.assertEqual(sel0, sel2)
        self.assertEqual(self.selectionIDs(), [])
        # Redo
        OOF.NodeSelection.Redo(skeleton='skeltest:skeleton')
        sel3 = id(self.selection().currentSelection())
        self.assertEqual(sel1, sel3)
        self.assertEqual(self.selectionIDs(), [74])
        # Select another Node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.63823,9.9786,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652), 
            shift=0, ctrl=0)
        sel4 = id(self.selection().currentSelection())
        self.assertNotEqual(sel0, sel4)
        self.assertNotEqual(sel1, sel4)
        self.assertEqual(self.selectionIDs(), [54])
        # Undo
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel1)
        self.assertEqual(self.selectionIDs(), [74])
        # Undo again
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel0)
        self.assertEqual(self.selectionIDs(), [])
        # Redo twice
        OOF.NodeSelection.Redo(skeleton='skeltest:skeleton')
        OOF.NodeSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(id(self.selection().currentSelection()), sel4)
        self.assertEqual(self.selectionIDs(), [54])

    @memorycheck.check("skeltest")
    def Clear(self):
        self.makeSkeleton(4, 4, 4)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.63823,9.9786,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652), 
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [54])
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
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(5.55861,9.95719,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167), 
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [10])
        # Invert.  All but one Node should be selected.
        OOF.Graphics_1.Toolbox.Select_Node.Invert(
            skeleton='skeltest:skeleton')
        nodelist.remove(10)
        self.assertEqual(self.selectionIDs(), nodelist)

    @memorycheck.check("skeltest")
    def Expand(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        # Expand the empty selection
        OOF.NodeSelection.Expand(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select one Node along an edge, shared by two elements
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(10.0107,4.62752,42.4752)], 
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        # Expand
        OOF.NodeSelection.Expand(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [9, 13, 14, 19, 39])
        # Undo
        OOF.NodeSelection.Undo(
            skeleton='skeltest:skeleton')
        # Select an adjacent node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(12.622,4.62752,42.4752)],
            view=View(cameraPosition=Coord(10,10,68.5167),
                      focalPoint=Coord(10,10,10), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertEqual(self.selectionIDs(), [14, 19])
        OOF.NodeSelection.Expand(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(),
                         [9, 13, 14, 18, 19, 23, 24, 39, 43, 44, 49])

    @memorycheck.check("skeltest")
    def NamedBdy(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        idlist = [('XminYminZmax', 4),
                  ('XmaxYminZmax', 24),
                  ('XmaxYmaxZmin', 120),
                  ('XminYmaxZmin', 100)]
        for bdyname, nodeID in idlist:
            OOF.NodeSelection.Select_Named_Boundary(
            skeleton='skeltest:skeleton',
            boundary=bdyname)
            self.assertEqual(self.selectionIDs(), [nodeID])

# end class Node_Selection_5Color

class Node_Selection_BlueGreen50(Skeleton_Selection_BlueGreen50,
                                 Node_Selection):
    @memorycheck.check("skeltest")
    def InternalBoundaries(self):
        self.makeSkeleton(4, 4, 4)
        self.assertEqual(self.selectionIDs(), [])
        OOF.NodeSelection.Select_Internal_Boundaries(
            skeleton='skeltest:skeleton')
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
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.97478,7.12895,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [22])
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupSize('newgroup'), 1)
        self.assertEqual(self.groupIDs('newgroup'), [22])
        # Select another node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(7.08354,5,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [16])
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [16, 22])
        # Re-add the same element
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.groupIDs('newgroup'), [16, 22])

    @memorycheck.check("skeltest")
    def SelectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a Node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.97478,7.12895,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [22])
        # Select the nodes in the empty group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [])
        # Undo the selection of the empty group
        OOF.NodeSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [22])
        # Make the group non-empty
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Clear the selection
        OOF.NodeSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Select the Node in the group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [22])
        # Select a different Node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(7.08354,5,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [16])
        # Select the Node in the group again. The previously selected
        # Node should be deselected.
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='newgroup')
        self.assertEqual(self.selectionIDs(), [22])
        
    @memorycheck.check("skeltest")
    def AddGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select a Node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.97478,7.12895,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [22])
        ## Add the Nodes in the empty group to the selection and make
        ## sure the slected Node stays selected.
        OOF.NodeSelection.Add_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [22])
        # Make the group non-empty
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Clear the selection
        OOF.NodeSelection.Clear(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Add the non-empty group to the empty selection
        OOF.NodeSelection.Add_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [22])
        # Select a different Node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(7.08354,5,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [16])
        # Add the group to the selection and make sure that both Nodes
        # are selected.
        OOF.NodeSelection.Add_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [16, 22])
    
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
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Select the other
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), self.blue_nodes)

    @memorycheck.check("skeltest")
    def UnselectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Unselect the empty group
        OOF.NodeSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Unselect a non-empty but non intersecting group
        OOF.NodeSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Unselect the green group
        OOF.NodeSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), [])
        # Select a single node and put it in newgroup
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.47404,5.01507,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [11])
        # Reselect the green group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Unselect the single node in newgroup
        OOF.NodeSelection.Unselect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        indices = self.green_nodes[:]
        indices.remove(11)
        self.assertEqual(self.selectionIDs(), indices)

    @memorycheck.check("skeltest")
    def IntersectGroup(self):
        self.makeSkeleton(2, 2, 2)
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='newgroup')
        # Select the green group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        # Intersect it with itself
        OOF.NodeSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Intersect it with the (disjoint) blue group
        OOF.NodeSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#868cfe')
        self.assertEqual(self.selectionIDs(), [])
        # Reselect the green group and intersect it with the empty
        # group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        OOF.NodeSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), [])
        # Add all the nodes to newgroup
        OOF.NodeSelection.Invert(skeleton='skeltest:skeleton')
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        # Reselect the green group and intersect it with the full group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        OOF.NodeSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        self.assertEqual(self.selectionIDs(), self.green_nodes)
        # Reselect the full group and intersect it with the green group
        OOF.NodeSelection.Select_Group(
            skeleton='skeltest:skeleton', group='newgroup')
        OOF.NodeSelection.Intersect_Group(
            skeleton='skeltest:skeleton', group='#a1fc93')
        self.assertEqual(self.selectionIDs(), self.green_nodes)

    @memorycheck.check("skeltest")
    def RemoveFromGroup(self):
        self.makeSkeleton(2, 2, 2)
        # Use autogroup to create the groups
        OOF.NodeGroup.Auto_Group(
            skeleton='skeltest:skeleton')
        # Select a single green node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.47404,5.01507,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [11])
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
        indices.remove(11)
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
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.26887,6.02803,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.NodeSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [11, 23])
        # Select a second segment
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.83348,6.14521,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=1, ctrl=0)
        OOF.NodeSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [11, 13, 19, 23])
    
    @memorycheck.check("skeltest")
    def SelectFromElements(self):
        self.makeSkeleton(2, 2, 2)
        # Select a corner element
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(3.27952,6.50742,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=655),
            shift=0, ctrl=0)
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton', 
            coverage='All')
        self.assertEqual(self.selectionIDs(), [11, 19, 20, 23])
        # Select all but the corner elements, by selecting the center
        # node (13) and then all the elements that contain it.
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.99597,9.34013,23.9245)],
            view=View(cameraPosition=Coord(5,11.5817,33.5084),
                      focalPoint=Coord(5,5,5), up=Coord(0,0.97437,-0.224951),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=691, size_y=655),
            shift=0, ctrl=0)
        self.assertEqual(self.selectionIDs(), [13])
        # Select all the nodes of the selected elements
        OOF.ElementSelection.Select_from_Selected_Nodes(
            skeleton='skeltest:skeleton',
            min_nodes=1)
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(self.selectionIDs(),
                         [1, 3, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                          19, 21, 22, 23, 25])
        # Select just the boundary nodes
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertEqual(self.selectionIDs(),
                         # The center node, 13, is not in this list
                         [1, 3, 4, 5, 7, 9, 10, 11, 12, 14, 15, 16, 17,
                          19, 21, 22, 23, 25])
        # Select just the internal nodes, of which there is one.
        OOF.NodeSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Interior')
        self.assertEqual(self.selectionIDs(), [13])

    @memorycheck.check("skeltest")
    def SelectFromFaces(self):
        self.makeSkeleton(2, 2, 2)
        # Select a face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(3.70346,5.73656,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.NodeSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage="All")
        self.assertEqual(self.selectionIDs(), [11, 14, 23])
        # Select an additional adjacent face
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-21.1376,5.46427,5.46555)],
            view=View(cameraPosition=Coord(-24.2583,5,5),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 2.0]], invertClip=0,
                      size_x=691, size_y=652), 
            shift=1, ctrl=0)
        OOF.NodeSelection.Clear(skeleton='skeltest:skeleton')
        OOF.NodeSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage="All")
        self.assertEqual(self.selectionIDs(), [11, 14, 19, 23])
        OOF.NodeSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage="Interior")
        self.assertEqual(self.selectionIDs(), [])
        OOF.NodeSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage="Exterior")
        self.assertEqual(self.selectionIDs(), [11, 14, 19, 23])
        # Select more adjacent faces, so that now there are nodes
        # interior to the selection.
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.36153,6.29416,22.2326)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0,
                      size_x=621, size_y=615), 
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.77021,4.71183,22.2326)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0,
                      size_x=621, size_y=615),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(4.56512,4.61752,22.2326)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, suppressClip=0,
                      size_x=621, size_y=615),
            shift=1, ctrl=0)
        OOF.NodeSelection.Clear(skeleton='skeltest:skeleton')
        OOF.NodeSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage="All")
        self.assertEqual(self.selectionIDs(), [5, 11, 14, 17, 19, 23])
        OOF.NodeSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage="Interior")
        self.assertEqual(self.selectionIDs(), [14])
        OOF.NodeSelection.Select_from_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage="Exterior")
        self.assertEqual(self.selectionIDs(), [5, 11, 17, 19, 23])
        
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
    Face_Selection_TwoWalls("DefaultClipTest"),
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

test_set = (element_set + face_set + segment_set + node_set +
            element_set2 + node_set2 + segment_set2 + face_set2)

# test_set = [
#     Element_Selection_5Color("ShapeEnergy"),
# ]
