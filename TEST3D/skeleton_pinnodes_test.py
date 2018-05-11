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
reference_file = file_utils.reference_file
file_utils.generate = False

# Node pinning tests

# OOF.Graphics_1.Toolbox.Pin_Nodes:
# Pin UnPin TogglePin Undo Redo Invert.

class PinTestBase(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        OOF.Windows.Graphics.New()
        OOF.Settings.Random_Seed(seed=17)

    def tearDown(self):
        OOF.Graphics_1.File.Close()

    def pinnedIDs(self):
        nodes = self.skelctxt.pinnednodes.retrieve()
        return [n.uiIdentifier() for n in nodes]
    
    def selectedIDs(self):
        nodes = self.skelctxt.nodeselection.retrieve()
        return [n.uiIdentifier() for n in nodes]


# Tests that use a 2x2x2 Skeleton in an undifferentiated
# Microstructure.

class PinTest222(PinTestBase):
    def setUp(self):
        PinTestBase.setUp(self)
        OOF.Microstructure.New(
            name='skeltest',
            width=10.0, height=10.0, depth=10.0,
            width_in_pixels=10, height_in_pixels=10, depth_in_pixels=10)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=2, y_elements=2, z_elements=2, 
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        self.skelctxt = skeletoncontext.skeletonContexts["skeltest:skeleton"]

    @memorycheck.check("skeltest")
    def Pin(self):
        OOF.Skeleton.PinNodes.Pin(
            skeleton='skeltest:skeleton',
            node=Coord(5, 10, 5))
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 1)
        skel = self.skelctxt.getObject()
        for nindx in range(skel.nnodes()):
            n = skel.getNode(nindx)
            if nindx == 22:
                self.assert_(n.pinned())
            else:
                self.assert_(not n.pinned())
        self.assertEqual(self.pinnedIDs(), [22])

    @memorycheck.check("skeltest")
    def UnPin(self):
        # Pin two, and unpin one.
        OOF.Skeleton.PinNodes.Pin(
            skeleton='skeltest:skeleton',
            node=Coord(0,10,10))
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='skeltest:skeleton',
            node=Coord(0,10,5))
        self.assertEqual(self.pinnedIDs(), [19, 20])
        OOF.Skeleton.PinNodes.UnPin(
            skeleton='skeltest:skeleton',
            node=Coord(0,10,5))
        self.assertEqual(self.pinnedIDs(), [20])

    @memorycheck.check("skeltest")
    def TogglePin(self):
        # Pin two, and toggle one.
        OOF.Skeleton.PinNodes.Pin(
            skeleton='skeltest:skeleton',
            node=Coord(0,10,10))
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='skeltest:skeleton',
            node=Coord(0,10,5))
        self.assertEqual(self.pinnedIDs(), [19, 20])
        OOF.Skeleton.PinNodes.TogglePin(
            skeleton='skeltest:skeleton',
            node=Coord(0,10,5))
        self.assertEqual(self.pinnedIDs(), [20])
        # Toggle back
        OOF.Skeleton.PinNodes.TogglePin(
            skeleton='skeltest:skeleton',
            node=Coord(0,10,5))
        self.assertEqual(self.pinnedIDs(), [19, 20])

    @memorycheck.check("skeltest")
    def UndoRedo(self):
        pin0 = self.skelctxt.pinnednodes.stack.current()
        OOF.Skeleton.PinNodes.Pin(
            skeleton='skeltest:skeleton',
            node=Coord(10,10,10))        
        self.assertEqual(self.pinnedIDs(), [26])
        pin1 = self.skelctxt.pinnednodes.stack.current()
        OOF.Skeleton.PinNodes.Undo(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [])
        pin2 = self.skelctxt.pinnednodes.stack.current()
        self.assertEqual(id(pin0), id(pin2))
        self.assertNotEqual(id(pin0), id(pin1))
        OOF.Skeleton.PinNodes.Redo(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [26])
        pin3 = self.skelctxt.pinnednodes.stack.current()
        self.assertNotEqual(id(pin0), id(pin3))
        self.assertEqual(id(pin1), id(pin3))

    @memorycheck.check("skeltest")
    def Invert(self):
        OOF.Skeleton.PinNodes.Pin(
            skeleton='skeltest:skeleton',
            node=Coord(10,10,10))        
        self.assertEqual(self.pinnedIDs(), [26])
        OOF.Skeleton.PinNodes.Invert(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 26)
        # Ensure that only node 26 is unpinned.
        skel = self.skelctxt.getObject()
        for nidx in range(skel.nnodes()):
            n = skel.getNode(nidx)
            if nidx == 26:
                self.assert_(not n.pinned())
            else:
                self.assert_(n.pinned())

    @memorycheck.check("skeltest")
    def UnpinAll(self):
        self.assertEqual(self.pinnedIDs(), [])
        OOF.Skeleton.PinNodes.Invert(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), range(27))
        OOF.Skeleton.PinNodes.UnPinAll(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.pinnedIDs(), [])

    # Test the Undo, Redo, Invert, and UnpinAll methods invoked from
    # the Pin Nodes page.  The previous tests tested the invocations
    # from the graphics window toolbox.

    @memorycheck.check("skeltest")
    def UndoRedo2(self):
        pin0 = self.skelctxt.pinnednodes.stack.current()
        OOF.Skeleton.PinNodes.Pin(
            skeleton='skeltest:skeleton',
            node=Coord(10,10,10))        
        self.assertEqual(self.pinnedIDs(), [26])
        pin1 = self.skelctxt.pinnednodes.stack.current()
        OOF.Skeleton.PinNodes.Undo(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [])
        pin2 = self.skelctxt.pinnednodes.stack.current()
        self.assertEqual(id(pin0), id(pin2))
        self.assertNotEqual(id(pin0), id(pin1))
        OOF.Skeleton.PinNodes.Redo(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [26])
        pin3 = self.skelctxt.pinnednodes.stack.current()
        self.assertNotEqual(id(pin0), id(pin3))
        self.assertEqual(id(pin1), id(pin3))

    @memorycheck.check("skeltest")
    def Invert2(self):
        OOF.Skeleton.PinNodes.Pin(
            skeleton='skeltest:skeleton',
            node=Coord(10,10,10))        
        self.assertEqual(self.pinnedIDs(), [26])
        OOF.Skeleton.PinNodes.Invert(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 26)
        # Ensure that only node 26 is unpinned.
        skel = self.skelctxt.getObject()
        for nidx in range(skel.nnodes()):
            n = skel.getNode(nidx)
            if nidx == 26:
                self.assert_(not n.pinned())
            else:
                self.assert_(n.pinned())

    @memorycheck.check("skeltest")
    def Pin_Node_Selection(self):
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,5,5),
                                    operator=Select()))
        self.assertEqual(self.selectedIDs(), [10])
        OOF.Skeleton.PinNodes.Pin_Node_Selection(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [10])
                
    @memorycheck.check("skeltest")
    def UnPin_Node_Selection(self):
        # Select one node
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,5,5),
                                    operator=Select()))
        self.assertEqual(self.selectedIDs(), [10])
        # Pin all nodes
        OOF.Skeleton.PinNodes.Invert(
            skeleton="skeltest:skeleton")
        # Unpin the selected one
        OOF.Skeleton.PinNodes.UnPin_Node_Selection(
            skeleton="skeltest:skeleton")
        nodes = range(0, 10) + range(11, 27)
        self.assertEqual(self.pinnedIDs(), nodes)

    @memorycheck.check("skeltest")
    def Pin_Selected_Segments(self):
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[11, 23],
                                       operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 17],
                                       operator=AddSelection()))        
        OOF.Skeleton.PinNodes.Pin_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.pinnedIDs(), [11, 17, 23])

    @memorycheck.check("skeltest")
    def Pin_Selected_Faces(self):
        # Select a bunch of elements, so we can determine correct
        # operation of internal.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[24, 15, 21],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 12, 21],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[12, 15, 3],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 6, 3],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[7, 6, 15],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[16, 7, 15],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[25, 16, 15],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 24, 25],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[21, 12, 9],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[12, 3, 9],
                                    operator=AddSelection()))

        OOF.Skeleton.PinNodes.Pin_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='All')
        self.assertEqual(self.pinnedIDs(), [3, 6, 7, 9, 12, 15, 16, 21, 24, 25])
        OOF.Skeleton.PinNodes.UnPinAll(
            skeleton='skeltest:skeleton')
        OOF.Skeleton.PinNodes.Pin_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertEqual(self.pinnedIDs(), [3, 6, 7, 9, 16, 21, 24, 25])
        OOF.Skeleton.PinNodes.UnPinAll(
            skeleton='skeltest:skeleton')
        OOF.Skeleton.PinNodes.Pin_Selected_Faces(
            skeleton='skeltest:skeleton',
            coverage='Interior')
        self.assertEqual(self.pinnedIDs(), [12, 15])


# Tests that use a 4x4x4 Skeleton and the bluegreen image.

class BlueGreen444(PinTestBase):
    def setUp(self):
        global primitives
        from ooflib.common import primitives
        PinTestBase.setUp(self)
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file('ms_data','bluegreen'),
                sort=NumericalOrder()),
            microstructure_name='bluegreen', height=automatic,
            width=automatic, depth=automatic)
        OOF.Image.AutoGroup(image='bluegreen:bluegreen', name_template='%c')
        OOF.Skeleton.New( 
            name='skeleton',
            microstructure='bluegreen',
            x_elements=4, y_elements=4, z_elements=4,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        self.skelctxt = skeletoncontext.skeletonContexts["bluegreen:skeleton"]

    @memorycheck.check("bluegreen")
    def Pin_Internal_Boundary_Nodes(self):
        OOF.Skeleton.PinNodes.Pin_Internal_Boundary_Nodes(
            skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), 
                         [1, 7, 11, 17, 21, 27, 31, 37, 41, 47, 51, 57, 61, 67,
                          71, 77, 81, 87, 91, 97, 101, 107, 111, 117, 121])


    @memorycheck.check("bluegreen")
    def Pin_Selected_Elements(self):
        # Autogroup the bluegreen image, and create a skeleton and
        # autogroup it, so that one group of elements can be selected.
        # Then test that the internal and external nodes of the
        # selected set of elements can be pinned.
        OOF.ElementGroup.Auto_Group(
            skeleton='bluegreen:skeleton')
        OOF.ElementSelection.Select(
            skeleton='bluegreen:skeleton',
            method=ElementSelectGroup(group='#a1fc93',
                                      operator=Select()))
        OOF.Skeleton.PinNodes.Pin_Selected_Elements(
            skeleton='bluegreen:skeleton',
            coverage='All')
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 88)
        OOF.Skeleton.PinNodes.UnPinAll(
            skeleton='bluegreen:skeleton')
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 0)
        OOF.Skeleton.PinNodes.Pin_Selected_Elements(
            skeleton='bluegreen:skeleton', 
            coverage='Exterior')
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 74)        
        OOF.Skeleton.PinNodes.UnPinAll(
            skeleton='bluegreen:skeleton')
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 0)
        OOF.Skeleton.PinNodes.Pin_Selected_Elements(
            skeleton='bluegreen:skeleton', 
            coverage='Interior')
        self.assertEqual(self.skelctxt.pinnednodes.npinned(), 14) 

    @memorycheck.check("bluegreen")
    def Move_Pinned(self):
        # Check that pinned nodes don't move when skeleton modifiers
        # are applied.
        global primitives
        from ooflib.common import primitives
        skel = self.skelctxt.getObject()
        # Pin two nodes on either side of the blue/green boundary.
        OOF.Skeleton.PinNodes.Pin(
            skeleton='bluegreen:skeleton', node=Coord(0,10,5))
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='bluegreen:skeleton', node=Coord(0,10,2.5))
        # Get the original positions of the pinned nodes.
        pinnedIDs = self.pinnedIDs()
        self.assertEqual(pinnedIDs, [101, 102])
        position = {}
        for nodeID in pinnedIDs:
            position[nodeID] = skel.getNode(nodeID).position()
        # Move the nodes
        OOF.Skeleton.Modify(
            skeleton='bluegreen:skeleton',
            modifier=SnapNodes(targets=SnapAll(),
                               criterion=AverageEnergy(alpha=1)))
        # Check that the pinned nodes haven't moved.
        for nodeID in pinnedIDs:
            self.assertEqual(position[nodeID],
                             skel.getNode(nodeID).position())
        # Undo the modification
        OOF.Skeleton.Undo(skeleton='bluegreen:skeleton')
        # Unpin the nodes.
        OOF.Skeleton.PinNodes.UnPinAll(
            skeleton='bluegreen:skeleton')
        # Move the nodes again. The first snap doesn't actually move
        # either node, so do it twice.
        OOF.Skeleton.Modify(
            skeleton='bluegreen:skeleton',
            modifier=SnapNodes(targets=SnapAll(),
                               criterion=AverageEnergy(alpha=1)))
        OOF.Skeleton.Modify(
            skeleton='bluegreen:skeleton',
            modifier=SnapNodes(targets=SnapAll(),
                               criterion=AverageEnergy(alpha=1)))
        # Check that one of the pinned nodes has moved. (Since we're
        # using SnapNodes and the two pinned nodes were only opposite
        # sides of the interface and in the same element, only of the
        # nodes can move.)
        movedNode = 102
        unmovedNode = 101
        self.assertEqual(skel.getNode(movedNode).position(),
                         primitives.Point(0, 10, 4)) 
        self.assertEqual(skel.getNode(unmovedNode).position(),
                         position[unmovedNode])

    @memorycheck.check("bluegreen")
    def Skeleton_Mod(self):
        # Check that nodes stay pinned when they're supposed to when
        # the Skeleton is modified.

        # First, move nodes and undo the move.
        OOF.Skeleton.Modify(
            skeleton='bluegreen:skeleton',
            modifier=SnapNodes(targets=SnapAll(),
                               criterion=AverageEnergy(alpha=1)))
        OOF.Skeleton.Undo(skeleton='bluegreen:skeleton')
        
        OOF.Skeleton.PinNodes.Pin(
            skeleton='bluegreen:skeleton', node=Coord(0,0,2.5))
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='bluegreen:skeleton', node=Coord(0,0,5))
        self.assertEqual(self.pinnedIDs(), [1,2])
        # Redo the skeleton modification, which moves node 1, so it is
        # automatically unpinned.
        OOF.Skeleton.Redo(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [2])
        # Undo the modification and check that node 1 is pinned again.
        OOF.Skeleton.Undo(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [1, 2])
        # In the modified skeleton, pin a node which hadn't moved, and
        # make sure it's pinned in the unmodified skeleton.
        OOF.Skeleton.Redo(skeleton='bluegreen:skeleton')
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='bluegreen:skeleton', node=Coord(5,0,7.5))
        self.assertEqual(self.pinnedIDs(), [2, 13])
        OOF.Skeleton.Undo(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [1, 2, 13])

        # Redo the node moves, and then refine the Skeleton
        OOF.Skeleton.Redo(skeleton='bluegreen:skeleton')
        OOF.Skeleton.Modify(skeleton='bluegreen:skeleton',
                            modifier=Refine(targets=CheckAllElements(),
                                            criterion=Unconditionally(),
                                            alpha=0))
        self.assertEqual(self.pinnedIDs(), [2, 13])
        # Pin a newly created node and another old one
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='bluegreen:skeleton', node=Coord(1.25,0,8.75))
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='bluegreen:skeleton', node=Coord(0,0,10))
        self.assertEqual(self.pinnedIDs(), [2, 4, 13, 565])
        # Undo the refinement
        OOF.Skeleton.Undo(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [2, 4, 13])
        # Undo the snap nodes
        OOF.Skeleton.Undo(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [1, 2, 4, 13])
        # Unpin all nodes and redo the modifications
        OOF.Skeleton.PinNodes.UnPinAll(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [])
        OOF.Skeleton.Redo(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [])
        OOF.Skeleton.Redo(skeleton='bluegreen:skeleton')
        self.assertEqual(self.pinnedIDs(), [])


    @memorycheck.check("bluegreen")
    def Save_Pinned(self):
        OOF.Skeleton.PinNodes.Pin(
            skeleton='bluegreen:skeleton',
            node=Coord(0,10,2.5))
        OOF.Skeleton.PinNodes.AddPin(
            skeleton='bluegreen:skeleton',
            node=Coord(0,10,5))
        OOF.File.Save.Skeleton(
            filename='pinnedskel.dat',
            mode='w', format='ascii',
            skeleton='bluegreen:skeleton')
        self.assert_(file_utils.fp_file_compare(
                "pinnedskel.dat",
                os.path.join("skeleton_data", "pintest"),
                1.e-9))
        file_utils.remove("pinnedskel.dat")

class NoInitialization(PinTestBase):
    @memorycheck.check("bluegreen")
    def Load_Pinned(self):
        OOF.File.Load.Data(filename=reference_file("skeleton_data",
                                                   "pintest"))
        self.skelctxt = skeletoncontext.skeletonContexts["bluegreen:skeleton"]
        self.assertEqual(self.pinnedIDs(), [101, 102])

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

basic_pin_set = [
    PinTest222("Pin"),
    PinTest222("UnPin"),
    PinTest222("TogglePin"),
    PinTest222("UndoRedo"),
    PinTest222("Invert"),
    PinTest222("UnpinAll"),
    PinTest222("UndoRedo2"),
    PinTest222("Invert2"),
    BlueGreen444("Save_Pinned"),
    NoInitialization("Load_Pinned"),
]

pin_modifier_set = [
    PinTest222("Pin_Node_Selection"),
    PinTest222("UnPin_Node_Selection"),
    BlueGreen444("Pin_Internal_Boundary_Nodes"),
    PinTest222("Pin_Selected_Segments"),
    PinTest222("Pin_Selected_Faces"),
    BlueGreen444("Pin_Selected_Elements"),
]

skeleton_modifier_set = [
    BlueGreen444("Move_Pinned"),
    BlueGreen444("Skeleton_Mod")
]

test_set = basic_pin_set + pin_modifier_set + skeleton_modifier_set

#test_set = [BlueGreen444("Skeleton_Mod")]
    
