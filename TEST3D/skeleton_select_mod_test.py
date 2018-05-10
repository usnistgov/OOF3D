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
reference_file = file_utils.reference_file

# Check that selections and groups behave correctly when a Skeleton is
# modified.

import skeleton_select_test

class SelectionTest(skeleton_select_test.Skeleton_Selection):
    def setUp(self):
        OOF.Settings.Random_Seed(seed=17)
        skeleton_select_test.Skeleton_Selection.setUp(self)
        OOF.Windows.Graphics.New()
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file('ms_data', 'bluegreen'),
                sort=NumericalOrder()),
            microstructure_name="skeltest",
            height=automatic, width=automatic, depth=automatic)
        OOF.Image.AutoGroup(image='skeltest:bluegreen', name_template='%c')
        ## We can't simply call
        ## skeleton_select_test.Skeleton_Selection.makeSkeleton here,
        ## because it relies on the oof globals which haven't been
        ## imported into that module.  See run_modules in
        ## regression.py.
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=2, y_elements=2, z_elements=3,
            skeleton_geometry=TetraSkeleton(arrangement='middling'))

    def tearDown(self):
        OOF.Graphics_1.File.Close()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
        
class ElementSelection(SelectionTest, skeleton_select_test.Element_Selection):

    def setUp(self):
        SelectionTest.setUp(self)
        OOF.ElementGroup.Auto_Group(skeleton='skeltest:skeleton')
        
    # Original contents of the green and blue element groups.
    green_elems = [
        5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 21, 22, 23, 24, 25, 26, 27, 28,
        29, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 50, 51, 52, 53, 54, 55, 56,
        57, 58, 59]
    blue_elems = [
        0, 1, 2, 3, 4, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 45, 46, 47, 48,
        49]

    def selectCorner(self):
        # Select a single corner element in the green ("#a1fc93")
        # group.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=41,
                                       operator=Select()))        

    @memorycheck.check("skeltest")
    def RefineSelectedElement(self):
        self.selectCorner()
        self.assertEqual(self.selectionIDs(), [41])
        self.assertEqual(self.skeleton().nelements(), 60)
        self.assertEqual(self.groupSize("#a1fc93"), 40)
        self.assertEqual(self.groupSize("#868cfe"), 20)
        
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton', name='corner')
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='corner')
        self.assertEqual(self.groupIDs("corner"), [41])

        # Refine the selected element.  It gets split into 8 elements,
        # all of which should be selected.  There are 6 additional
        # elements created when the neighbors are divided, so there
        # are net 13 more elements afterwards.
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckSelectedElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))
        self.assertEqual(self.selectionIDs(), 
                         [35, 36, 37, 38, 39, 40, 41, 42])
        self.assertEqual(self.groupIDs("corner"),
                         [35, 36, 37, 38, 39, 40, 41, 42])
        self.assertEqual(self.skeleton().nelements(), 73)
        refined_green = [
            0, 1, 2, 3, 4, 8, 9, 10, 11, 12, 15, 17, 19, 20, 23, 24, 25, 28,
            30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46,
            47, 51, 52, 53, 54, 55, 57, 59, 61, 62, 63, 64, 65, 66, 67, 68, 
            69, 70, 72]
        refined_blue =  [
            5, 6, 7, 13, 14, 16, 18, 21, 22, 26, 27, 29, 33, 48, 49, 50, 56,
            58, 60, 71]
        self.assertEqual(self.groupIDs("#a1fc93"), refined_green)
        self.assertEqual(self.groupIDs("#868cfe"), refined_blue)

        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [41])
        self.assertEqual(self.skeleton().nelements(), 60)
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_elems)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_elems)

        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), 
                         [35, 36, 37, 38, 39, 40, 41, 42])
        self.assertEqual(self.skeleton().nelements(), 73)
        self.assertEqual(
            self.groupIDs("#a1fc93"), refined_green)
        self.assertEqual(self.groupIDs("#868cfe"), refined_blue)

        ## Check that selecting and deselecting and refining and
        ## unrefining commute properly. 

        # Deselect one of the refined elements, then unrefine.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=42,
                                       operator=Toggle()))
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        # The unrefined element should still be selected.
        self.assertEqual(self.selectionIDs(), [41])
        self.assertEqual(self.groupIDs("corner"), [41])
        
        # Deselect the element and re-refine.
        OOF.ElementSelection.Clear(skeleton='skeltest:skeleton')
        # OOF.Graphics_1.Toolbox.Select_Element.Clear(
        #     skeleton='skeltest:skeleton')
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        # Nothing should be selected.
        self.assertEqual(self.selectionIDs(), [])
        # But the group should contain the refined elements
        self.assertEqual(self.groupIDs("corner"),
                         [35, 36, 37, 38, 39, 40, 41, 42])

        # Select some but not all of the refined corner elements.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=38,operator=AddSelection()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=37,operator=AddSelection()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=35,operator=AddSelection()))
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=36,operator=AddSelection()))

       # Undo the refinement.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        # Nothing should be selected.
        self.assertEqual(self.selectionIDs(), [])
        self.assertEqual(self.groupIDs("corner"), [41])
        
        # Redo the refinement.
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        # Select all of the corner elements.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='corner',
                                      operator=Select()))
        # OOF.ElementSelection.Select_Group(
        #     skeleton='skeltest:skeleton', group='corner')
        # Undo the refinement.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        # The corner element should be selected.
        self.assertEqual(self.selectionIDs(), [41])
        self.assertEqual(self.groupIDs("corner"), [41])

    
    @memorycheck.check("skeltest")
    def Commute(self):
        # Check that Skeleton Undo and Redo commute properly with
        # Selection Undo and Redo.  This is slightly different from
        # the above tests, which didn't use Selection Undo and Redo.
        
        # Select one element and undo the selection.
        self.selectCorner()
        self.assertEqual(self.selectionIDs(), [41])
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')

        # Refine all elements and undo the modification.
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton', 
            modifier=Refine(targets=CheckAllElements(),
                            criterion=Unconditionally(),alpha=0.3))
        self.assertEqual(self.skeleton().nelements(), 480)
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.skeleton().nelements(), 60)

        # Redo the selection.
        OOF.ElementSelection.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.skeleton().nelements(), 60)
        self.assertEqual(self.selectionIDs(), [41])
        # Redo the modification.
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), 
                         [264, 265, 266, 267, 268, 269, 270, 271])
        # Undo the selection.
        OOF.ElementSelection.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.skeleton().nelements(), 480)
        self.assertEqual(self.selectionIDs(), [])
        # Undo the modification.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.skeleton().nelements(), 60)
        self.assertEqual(self.selectionIDs(), [])

    @memorycheck.check("skeltest")
    def Anneal(self):
        # Annealing shouldn't change the groups or selection.
        self.selectCorner()
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton', 
            modifier=Anneal(targets=AllNodes(),
                            criterion=AverageEnergy(alpha=0.8),
                            T=0.0,delta=1.0,
                            iteration=FixedIteration(iterations=10)))
        self.assertEqual(self.selectionIDs(), [41])
        self.assertEqual(self.skeleton().nelements(), 60)
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_elems)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_elems)
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [41])
        self.assertEqual(self.skeleton().nelements(), 60)
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_elems)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_elems)

    @memorycheck.check("skeltest")
    def AnnealRefine(self):
        # Refining after annealing checks that the selection and
        # groups are propagated properly through deputy skeletons.
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton', 
            modifier=Anneal(targets=AllNodes(),
                            criterion=AverageEnergy(alpha=0.8),
                            T=0.0,delta=1.0,
                            iteration=FixedIteration(iterations=10)))
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckAllElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))
        # Undo both modifications
        OOF.Skeleton.Undo(
            skeleton='skeltest:skeleton')
        OOF.Skeleton.Undo(
            skeleton='skeltest:skeleton')
        
        # Select a single element in the original skeleton and check
        # the selections in the modified skeletons.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=10,
                                       operator=Select()))        
        self.assertEqual(self.selectionIDs(), [10])
        # Create a group and add the element to it.
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='groupOne')
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='groupOne')
        self.assertEqual(self.groupIDs('groupOne'), [10])
        # Redo the Anneal and check that the selection and groups
        # haven't changed.
        OOF.Skeleton.Redo(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [10])
        self.assertEqual(self.groupIDs('groupOne'), [10])
        # Just for kicks, re-add the selection to the group.  Nothing
        # should happen to the group.
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='groupOne')
        self.assertEqual(self.groupIDs('groupOne'), [10])
        # Redo the refinement.
        OOF.Skeleton.Redo(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(),
                         [320, 321, 322, 323, 324, 325, 326, 327])
        self.assertEqual(self.groupIDs('groupOne'),
                         [320, 321, 322, 323, 324, 325, 326, 327])

        # Select a bunch of elements in the most modified skeleton and
        # check the selections in the earlier ones.  The first eight
        # elements selected here are all of the child elements of an
        # element in the unrefined skeleton.
        def selectElement(e):
            OOF.ElementSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleElementSelect(element=e,operator=AddSelection()))
        OOF.ElementSelection.Clear(skeleton='skeltest:skeleton')
        map(selectElement, [344, 345, 346, 347, 348, 349, 350, 351])
        # The next two selections don't select complete unrefined elements.
        selectElement(320)
        selectElement(376)
        tenElements = [320, 344, 345, 346, 347, 348, 349, 350, 351, 376]
        self.assertEqual(self.selectionIDs(), tenElements)
        OOF.ElementGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='groupTwo')
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='groupTwo')
        self.assertEqual(self.groupIDs('groupTwo'), tenElements)
        OOF.Skeleton.Undo(
             skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [56])
        self.assertEqual(self.groupIDs('groupTwo'), [56])
        OOF.Skeleton.Undo(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [56])
        self.assertEqual(self.groupIDs('groupTwo'), [56])
        OOF.Skeleton.Redo(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [56])
        self.assertEqual(self.groupIDs('groupTwo'), [56])
        OOF.Skeleton.Redo(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), tenElements)
        self.assertEqual(self.groupIDs('groupTwo'), tenElements)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SegmentSelection(SelectionTest, skeleton_select_test.Segment_Selection):
    def setUp(self):
        SelectionTest.setUp(self)
        OOF.SegmentGroup.Auto_Group(skeleton='skeltest:skeleton')

    # Original contents of the green and blue segment groups
    green_segs = [
        76, 77, 78, 79, 80, 81, 87, 88, 89, 90, 91, 97, 102, 108, 109, 110,
        111, 112, 113, 119, 120, 121, 122, 123, 129, 134, 172, 173, 174, 179,
        180, 181, 182, 183, 192, 198, 199, 200, 201, 202, 203, 209, 210, 215,
        256, 257, 258, 263, 264, 265, 266, 267, 273, 282, 283, 284, 289, 290,
        291, 292, 293, 299, 334, 335, 336, 341, 342, 347, 355, 359, 360, 361,
        362, 363]
    blue_segs = [
        37, 38, 39, 40, 41, 42, 48, 49, 50, 51, 52, 58, 59, 60, 61, 67, 68,
        69, 140, 141, 142, 143, 144, 145, 151, 152, 157, 158, 159, 160, 166,
        224, 225, 226, 231, 232, 233, 234, 235, 241, 242, 243, 244, 250, 308,
        312, 313, 314, 315, 316, 322, 323, 328]

    def selectSegment(self):
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[31, 18],
                                       operator=Select()))

    @memorycheck.check("skeltest")
    def RefineSelectedSegment(self):
        self.selectSegment()

        self.assertEqual(self.selectionIDs(), [284])
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_segs)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_segs)

        OOF.SegmentGroup.New_Group(
            skeleton='skeltest:skeleton', name='seggroup')
        OOF.SegmentGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='seggroup')
        self.assertEqual(self.groupIDs("seggroup"), [284])

        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckSelectedEdges(),
                            criterion=Unconditionally(),
                            alpha=0.8))
        self.assertEqual(self.selectionIDs(), [520, 527])
        self.assertEqual(self.groupIDs("seggroup"), [520, 527])
        refined_green = [
            412, 413, 414, 415, 416, 417, 423, 424, 425, 426, 427, 433, 434,
            435, 436, 437, 438, 444, 445, 446, 486, 490, 491, 492, 493, 494,
            500, 501, 502, 503, 504, 519, 520, 525, 526, 527, 546, 561, 562,
            563, 564, 565, 577, 598, 600, 608, 612, 626, 627, 628, 629, 630,
            639, 643, 644, 649, 658, 662, 663, 664, 665, 671, 678, 679, 680, 
            687, 706, 707, 723, 724, 736, 742, 743, 744, 779]
        refined_blue = [
            447, 453, 454, 455, 456, 457, 458, 464, 465, 466, 467, 468, 469,
            475, 476, 477, 478, 479, 480, 532, 533, 534, 539, 540, 541, 551,
            552, 553, 554, 555, 571, 576, 578, 585, 586, 587, 592, 593, 599,
            601, 602, 619, 620, 621, 654, 691, 695, 699, 700, 701, 750, 762,
            789]
        self.assertEqual(self.groupIDs("#a1fc93"), refined_green)
        self.assertEqual(self.groupIDs("#868cfe"), refined_blue)

        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [284])
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_segs)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_segs)

        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [520, 527])
        self.assertEqual(self.groupIDs("#a1fc93"), refined_green)
        self.assertEqual(self.groupIDs("#868cfe"), refined_blue)

        ## TODO 3.0: Check that segment selection and deselection commute
        ## properly with Skeleton Undo and Redo, selecting 'seggroup'
        ## or parts of it.

        ## TODO 3.0: Check that segment selection Undo and Redo commute
        ## properly with Skeleton Undo and Redo.


    @memorycheck.check("skeltest")
    def Anneal(self):
        self.selectSegment()
        self.assertEqual(self.selectionIDs(), [284])
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_segs)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_segs)
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton', 
            modifier=Anneal(targets=AllNodes(),
                            criterion=AverageEnergy(alpha=0.8),
                            T=0.0,delta=1.0,
                            iteration=FixedIteration(iterations=10)))
        self.assertEqual(self.selectionIDs(), [284])
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_segs)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_segs)
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')        
        self.assertEqual(self.selectionIDs(), [284])
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_segs)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_segs)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class NodeSelection(SelectionTest, skeleton_select_test.Node_Selection):
    def setUp(self):
        SelectionTest.setUp(self)
        OOF.NodeGroup.Auto_Group(skeleton='skeltest:skeleton')

    green_nodes = [
        2, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23, 26, 27, 30, 31, 34, 35]
    blue_nodes = [
        0, 1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29, 32, 33]

    def selectNodes(self):
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,10,6.66667),
                                    operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,10,10),
                                    operator=AddSelection()))

    @memorycheck.check("skeltest")
    def RefineSelectedElement(self):
        # Select two nodes.
        self.selectNodes()
        self.assertEqual(self.selectionIDs(), [26, 27])
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_nodes)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_nodes)
        # Select and refine the element containing the two nodes.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=41,
                                       operator=Select()))
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckSelectedElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))
        # Node groups and selections are not affected by refinement!
        self.assertEqual(self.selectionIDs(), [26, 27])
        self.assertEqual(self.groupIDs("#a1fc93"), self.green_nodes)
        self.assertEqual(self.groupIDs("#868cfe"), self.blue_nodes)
        # Select one of the new nodes and put the three selected nodes
        # in a group.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,10,8.33333),
                                    operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [26, 27, 40])
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton', name='nodegroup')
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='nodegroup')
        self.assertEqual(self.groupIDs("nodegroup"), [26, 27, 40])
        # Undo the refinement and check the membership of the new
        # group and the selection.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.groupIDs("nodegroup"), [26, 27])
        self.assertEqual(self.selectionIDs(), [26, 27])
        # And Redo
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.groupIDs("nodegroup"), [26, 27, 40])
        self.assertEqual(self.selectionIDs(), [26, 27, 40])

        ## TODO 3.0: Check that Node selection and deselection commute
        ## properly with Skeleton Undo and Redo. 

        ## TODO 3.0: Check that Node selection Undo and Redo commute
        ## properly with Skeleton Undo and Redo.
        
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#


a_faces = [117, 127, 287, 297] # [287, 297, 357, 367]
b_faces = [207, 213, 357, 367] # [117, 127, 207, 213]

class FaceSelection(SelectionTest, skeleton_select_test.Face_Selection):
    def setUp(self):
        SelectionTest.setUp(self)
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 31, 27],operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 19, 31],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 7, 19],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[3, 7, 15],
                                    operator=AddSelection()))
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='groupA')
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='groupA')
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[31, 23, 35],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[19, 23, 31],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[7, 23, 19],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[7, 11, 23],
                                    operator=AddSelection()))
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='groupB')
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='groupB')

    @memorycheck.check("skeltest")
    def RefineSelectedFace(self):
        OOF.FaceSelection.Clear(skeleton='skeltest:skeleton')
        # Select one face
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 27, 26],
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [294])
        self.assertEqual(self.groupIDs("groupA"), a_faces)
        self.assertEqual(self.groupIDs("groupB"), b_faces)
        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton', name='facegroup')
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton', group='facegroup')
        self.assertEqual(self.groupIDs('facegroup'), [294])

        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckSelectedFaces(),
                            criterion=Unconditionally(),alpha=0.3))
        self.assertEqual(self.selectionIDs(), [676, 683, 688, 692])
        self.assertEqual(self.groupIDs('facegroup'), [676, 683, 688, 692])
        refined_A = [521, 530, 679, 686, 790]
        refined_B = [511, 708, 745, 755]
        self.assertEqual(self.groupIDs("groupA"), refined_A)
        self.assertEqual(self.groupIDs("groupB"), refined_B)
        
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [294])
        self.assertEqual(self.groupIDs("groupA"), a_faces)
        self.assertEqual(self.groupIDs("groupB"), b_faces)

        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [676, 683, 688, 692])
        self.assertEqual(self.groupIDs("groupA"), refined_A)
        self.assertEqual(self.groupIDs("groupB"), refined_B)
        
        ## TODO 3.0: Check that things still work with a longer sequence
        ## of skeleton modifications, including some that only move
        ## nodes.

        # Check that face selection and deselection commute
        # properly with Skeleton Undo and Redo.  Select or deselect
        # some of the faces in the refined 'facegroup' and see if the
        # unrefined face is selected appropriately when the
        # refinement is undone.
        
        # Deselect one of the refined faces.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[37, 27, 38],operator=Toggle()))
        self.assertEqual(self.selectionIDs(), [683, 688, 692])
        # Undo the refinement.  The face should be selected.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [294])
        # Redo the refinement.  The deselected face should still be
        # unselected.
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [683, 688, 692])
        self.assertEqual(self.groupIDs("facegroup"), [676, 683, 688, 692])
        # Clear the selection, and manually select some but not all of
        # the refined faces.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[37, 38, 36],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 37, 36],
                                    operator=AddSelection()))
        self.assertEqual(self.selectionIDs(), [683, 688])
        # Undo the refinement.  The face should *not* be selected.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [])
        # Redo the refinement and select all of the refined faces.
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='facegroup',
                                   operator=Select()))
        # Undo the refinement. The face should be selected.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [294])

    # ImplicitClear checks for a bug in which under some circumstances
    # a selected object that wasn't part of the current skeleton
    # wasn't deselected when a new selection was made.  The bug and
    # the fix were general, so we're only checking it for faces.
    ## TODO 3.0: This should probably be explicitly tested for elements
    ## and segments.
    @memorycheck.check("skeltest")
    def ImplicitClear(self):
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton', 
            modifier=Refine(targets=CheckAllElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))
        # Select faces that correspond to an unrefined face.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[137, 138, 27],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[137, 86, 138],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[86, 31, 138],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 86, 137],
                                    operator=AddSelection()))
        # Select another face too.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[156, 157, 35],
                                    operator=AddSelection()))
        self.assertEqual(self.selectionIDs(),[2287, 2297, 2306, 2324, 2888])
        # Undo the Skeleton modification.
        OOF.Skeleton.Undo(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), [297])
        # Click to select a *different* face, none of whose refined
        # subelements are selected.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[7, 11, 23],
                                    operator=Select()))
        self.assertEqual(self.selectionIDs(), [207])
        # Redo the modification.
        OOF.Skeleton.Redo(
            skeleton='skeltest:skeleton')
        # Check that only the children of the newly selected face are
        # selected.  In particular, the face selected in the "select
        # another face too" step, above, should not be selected, even
        # though its parent was not explicitly deselected by the last
        # click.
        self.assertEqual(self.selectionIDs(), [2430, 2436, 2446, 2460])

         
        
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Use skeleton_data/bad.skel and Rationalize it. Make sure that the
## boundaries survive the process.  At one time, not all of the faces
## geometrically on the modified boundary would be listed in the
## boundary, and the boundary would have gaps in it.

class BadSkeleton(unittest.TestCase):
    def setUp(self):
        from ooflib.engine import skeletoncontext
        OOF.File.Load.Data(
            filename=reference_file('skeleton_data','bad.skel'))
        self.skelctxt = skeletoncontext.skeletonContexts['5color:skeleton']

    @memorycheck.check("5color")
    def Rationalize(self):
        OOF.FaceGroup.New_Group(
            skeleton='5color:skeleton',
            name='front')
        OOF.FaceSelection.Select(
            skeleton='5color:skeleton',
            method=SelectNamedBoundaryFaces(boundary='Zmax',
                                            operator=Select()))
        OOF.FaceGroup.Add_to_Group(
            skeleton='5color:skeleton',
            group='front')
        OOF.Skeleton.Modify(
            skeleton='5color:skeleton',
            modifier=Rationalize(
                targets=AllElements(),
                criterion=AverageEnergy(alpha=0.3),
                method=SpecificRationalization(
                    rationalizers=[RemoveBadTetrahedra(
                        acute_angle=15,obtuse_angle=150)])))
        # sanity_check checks the areas of the face boundaries, which
        # is sufficient here.
        self.assert_(self.skelctxt.sanity_check())

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Check that Skeleton Groups are created and populated properly when
# the Skeleton undobuffer is small.  Check both for refinement and
# annealing so that both non-deputy and deputy skeletons and trackers
# are tested.

class SmallBufferGroup(skeleton_select_test.Skeleton_Selection,
                       skeleton_select_test.Element_Selection):
    def setUp(self):
        skeleton_select_test.Skeleton_Selection.setUp(self)
        OOF.Microstructure.New(
            name='skeltest', width=10.0,
            height=10.0, depth=10.0, width_in_pixels=10,
            height_in_pixels=10, depth_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton', microstructure='skeltest',
            x_elements=2, y_elements=2, z_elements=2,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        OOF.Settings.UndoBuffer_Size.Skeleton(size=3)
        OOF.Windows.Graphics.New()

    def tearDown(self):
        OOF.Graphics_1.File.Close()

    @memorycheck.check("skeltest")
    def Refine(self):
        def prerefine():
            OOF.Settings.Random_Seed(seed=17)
            OOF.SegmentSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleSegmentSelect(nodes=[20, 23],
                                           operator=Select()))
        def refine():
            OOF.Skeleton.Modify(
                skeleton='skeltest:skeleton',
                modifier=Refine(targets=CheckSelectedEdges(),
                                criterion=Unconditionally(),alpha=0.3))
        def select():
            OOF.ElementSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleElementSelect(element=29,
                                           operator=Select()))
            OOF.ElementSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleElementSelect(element=3,
                                           operator=AddSelection()))            
        # The ids are the IDs of the selected elements at each stage
        # of refinement.  The selection is made at refinement level 1.
        ids0 = []
        ids1 = [3, 29]
        ids2 = [6, 7, 32, 33]
        ids3 = [0, 1, 16, 17, 29, 30, 49, 50]
        self.doTest(prerefine, refine, select, ids0, ids1, ids2, ids3)

    @memorycheck.check("skeltest")
    def Anneal(self):
        def preanneal():
            OOF.Settings.Random_Seed(seed=17)
            OOF.NodeSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleNodeSelect(point=Coord(5,10,10),
                                        operator=Select()))
            OOF.NodeSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleNodeSelect(point=Coord(5,5,10),
                                        operator=AddSelection()))
            OOF.NodeSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleNodeSelect(point=Coord(5,0,10),
                                        operator=AddSelection()))

        def anneal():
            OOF.Skeleton.Modify(
                skeleton='skeltest:skeleton', 
                modifier=Anneal(targets=SelectedNodes(),
                                criterion=AverageEnergy(alpha=1.0),
                                T=0.0,delta=1.0,
                                iteration=FixedIteration(iterations=1)))
        def select():
            OOF.ElementSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleElementSelect(element=26,
                                           operator=Select()))
            OOF.ElementSelection.Select(
                skeleton='skeltest:skeleton',
                method=SingleElementSelect(element=27,
                                           operator=AddSelection()))
        ids = [26, 27]
        self.doTest(preanneal, anneal, select,
                    [26, 27], [26, 27], [26, 27], [26, 27])

    def doTest(self, premodifierfn, modifierfn, selectfn,
               ids0, ids1, ids2, ids3):
        # Do enough modifications that the original Skeleton is pushed
        # off the bottom of the short undobuffer.
        premodifierfn()
        modifierfn()
        modifierfn()
        modifierfn()
        modifierfn()
        # Undo, but not all the way, and create a group.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        OOF.ElementGroup.New_Group( 
            skeleton='skeltest:skeleton',
            name='elementgroup')
        selectfn()
        self.assertEqual(self.selectionIDs(), ids1)
        OOF.ElementGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='elementgroup')
        self.assertEqual(self.groupIDs("elementgroup"), ids1)
        # Redo once and check the group 
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='elementgroup',
                                      operator=Select()))
        self.assertEqual(self.selectionIDs(), ids2)
        self.assertEqual(self.groupIDs("elementgroup"), ids2)
        # Redo again
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.assertEqual(self.selectionIDs(), ids3)
        self.assertEqual(self.groupIDs("elementgroup"), ids3)

        # Undo all the available modifications.
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        # Select the group, which may be empty at this stage of the
        # skeleton modification.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='elementgroup',
                                      operator=Select()))
        self.assertEqual(self.selectionIDs(), ids0)
        self.assertEqual(self.groupIDs("elementgroup"), ids0)
        # Redo all of the modifications.
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        # The group should not be empty, but the selection might be.
        # TODO: Huh?  There used to be an ids0g arg for the group.
        self.assertEqual(self.selectionIDs(), ids0)
        self.assertEqual(self.groupIDs("elementgroup"), ids3)
        # Select the group and check its contents.
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ElementSelectGroup(group='elementgroup',
                                      operator=Select()))
        # Undo all
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        # Check.  The selection might be empty
        self.assertEqual(self.selectionIDs(), ids0)
        self.assertEqual(self.groupIDs("elementgroup"), ids0)
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        # Redo all.  The selection should not be mempty.
        self.assertEqual(self.selectionIDs(), ids3)
        self.assertEqual(self.groupIDs("elementgroup"), ids3)



#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

test_set = [
    ElementSelection("RefineSelectedElement"),
    ElementSelection("Commute"),
    ElementSelection("Anneal"),
    ElementSelection("AnnealRefine"),
    SegmentSelection("RefineSelectedSegment"),
    SegmentSelection("Anneal"),
    NodeSelection("RefineSelectedElement"),
    FaceSelection("RefineSelectedFace"),
    FaceSelection("ImplicitClear"),
    BadSkeleton("Rationalize"),
    SmallBufferGroup("Refine"),
    SmallBufferGroup("Anneal"),
]

