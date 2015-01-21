# -*- python -*-
# $RCSfile: skeleton_pinnodes_test.py,v $
# $Revision: 1.1.2.5 $
# $Author: fyc $
# $Date: 2014/07/30 20:24:42 $

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
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(4.98382,7.2055,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
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
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(2.34153,7.68003,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(2.80528,7.18393,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        self.assertEqual(self.pinnedIDs(), [19, 20])
        OOF.Graphics_1.Toolbox.Pin_Nodes.UnPin(
            skeleton='skeltest:skeleton',
            point=Point(2.77293,7.19472,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        self.assertEqual(self.pinnedIDs(), [20])

    @memorycheck.check("skeltest")
    def TogglePin(self):
        # Pin two, and toggle one.
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(2.34153,7.68003,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(2.80528,7.18393,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        self.assertEqual(self.pinnedIDs(), [19, 20])
        OOF.Graphics_1.Toolbox.Pin_Nodes.TogglePin(
            skeleton='skeltest:skeleton',
            point=Point(2.77293,7.19472,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        self.assertEqual(self.pinnedIDs(), [20])
        # Toggle back
        OOF.Graphics_1.Toolbox.Pin_Nodes.TogglePin(
            skeleton='skeltest:skeleton',
            point=Point(2.77293,7.19472,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        self.assertEqual(self.pinnedIDs(), [19, 20])

    @memorycheck.check("skeltest")
    def UndoRedo(self):
        pin0 = self.skelctxt.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(7.65847,7.66925,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        self.assertEqual(self.pinnedIDs(), [26])
        pin1 = self.skelctxt.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Undo(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [])
        pin2 = self.skelctxt.pinnednodes.stack.current()
        self.assertEqual(id(pin0), id(pin2))
        self.assertNotEqual(id(pin0), id(pin1))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Redo(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [26])
        pin3 = self.skelctxt.pinnednodes.stack.current()
        self.assertNotEqual(id(pin0), id(pin3))
        self.assertEqual(id(pin1), id(pin3))

    @memorycheck.check("skeltest")
    def Invert(self):
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(7.65847,7.66925,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
        self.assertEqual(self.pinnedIDs(), [26])
        OOF.Graphics_1.Toolbox.Pin_Nodes.Invert(
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
        OOF.Graphics_1.Toolbox.Pin_Nodes.Invert(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), range(27))
        OOF.Graphics_1.Toolbox.Pin_Nodes.UnPinAll(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.pinnedIDs(), [])

    # Test the Undo, Redo, Invert, and UnpinAll methods invoked from
    # the Pin Nodes page.  The previous tests tested the invocations
    # from the graphics window toolbox.

    @memorycheck.check("skeltest")
    def UndoRedo2(self):
        pin0 = self.skelctxt.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(7.65847,7.66925,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
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
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='skeltest:skeleton',
            point=Point(7.65847,7.66925,21.2376),
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647))
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
    def UnpinAll2(self):
        self.assertEqual(self.pinnedIDs(), [])
        OOF.Skeleton.PinNodes.Invert(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), range(27))
        OOF.Skeleton.PinNodes.UnPinAll(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.pinnedIDs(), [])

    @memorycheck.check("skeltest")
    def Pin_Node_Selection(self):
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.76214,5.00539,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647),
            shift=0, ctrl=0)
        self.assertEqual(self.selectedIDs(), [10])
        OOF.Skeleton.PinNodes.Pin_Node_Selection(
            skeleton="skeltest:skeleton")
        self.assertEqual(self.pinnedIDs(), [10])
                
    @memorycheck.check("skeltest")
    def UnPin_Node_Selection(self):
        # Select one node
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.76214,5.00539,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647),
            shift=0, ctrl=0)
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
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(3.26903,5.98681,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(6.20251,6.46135,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=647),
            shift=1, ctrl=0)
        OOF.Skeleton.PinNodes.Pin_Selected_Segments(
            skeleton='skeltest:skeleton')
        self.assertEqual(self.pinnedIDs(), [11, 17, 23])

#     def Pin_Selected_Faces(self):
#         # Select a bunch of elements, so we can determine correct
#         # operation of internal.
#         OOF.Graphics_1.Toolbox.Select_Segment.Single_Element(
#             skeleton="skeltest:skelselect",
#             points=[Point(3.75,2.75,6.0)], shift=0, ctrl=0)
#         OOF.Skeleton.PinNodes.Pin_Selected_Elements(
#             skeleton="skeltest:skelselect", internal=False, boundary=True)
#         OOF.Graphics_1.Toolbox.Select_Element.Clear(
#             skeleton="skeltest:skelselect")
#         for nidx in range(125): 
#             n = self.sk_context.getObject().getNode(nidx)
#             if n.getUid() in [10,11,12,19,21,28,29,30]:
#                 self.assert_(n.pinned())
#             else:
#                 self.assert_(not n.pinned())



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
        OOF.ElementSelection.Select_Group(
            skeleton='bluegreen:skeleton',
            group='#a1fc93')
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
        # Pin a couple of nodes on either side of the blue/green boundary.
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='bluegreen:skeleton', 
            point=Point(-15.7509,25.046,0.586289),
            view=View(cameraPosition=Coord(-15.8018,25.0947,0.579851),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.143933,-0.0681609,-0.987237), 
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=690, size_y=618))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='bluegreen:skeleton',
            point=Point(-15.7517,25.0469,0.593985), 
            view=View(cameraPosition=Coord(-15.8018,25.0947,0.579851),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.143933,-0.0681609,-0.987237),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=690, size_y=618))
        # Get the original positions of the pinned nodes.
        pinnedIDs = self.pinnedIDs()
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
        # Move the nodes again
        OOF.Skeleton.Modify(
            skeleton='bluegreen:skeleton',
            modifier=SnapNodes(targets=SnapAll(),
                               criterion=AverageEnergy(alpha=1)))
        # Check that one of the pinned nodes has moved. (Since we're
        # using SnapNodes and the two pinned nodes were only opposite
        # sides of the interface and in the same element, only of the
        # nodes can move.)
        self.assertEqual(skel.getNode(101).position(),
                         primitives.Point(0, 10, 4)) # moved
        self.assertEqual(skel.getNode(102).position(), position[102]) # not

    @memorycheck.check("bluegreen")
    def Save_Pinned(self):
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='bluegreen:skeleton', 
            point=Point(-15.7509,25.046,0.586289),
            view=View(cameraPosition=Coord(-15.8018,25.0947,0.579851),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.143933,-0.0681609,-0.987237), 
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=690, size_y=618))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton='bluegreen:skeleton',
            point=Point(-15.7517,25.0469,0.593985), 
            view=View(cameraPosition=Coord(-15.8018,25.0947,0.579851),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.143933,-0.0681609,-0.987237),
                      angle=30, clipPlanes=[], invertClip=0,
                      size_x=690, size_y=618))
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
    PinTest222("UnpinAll2"),
    BlueGreen444("Save_Pinned"),
    NoInitialization("Load_Pinned"),
]

pin_modifier_set = [
    PinTest222("Pin_Node_Selection"),
    PinTest222("UnPin_Node_Selection"),
    BlueGreen444("Pin_Internal_Boundary_Nodes"),
    PinTest222("Pin_Selected_Segments"),
    BlueGreen444("Pin_Selected_Elements"),
    BlueGreen444("Move_Pinned"),
]

## TODO 3.0: Interaction of pinned nodes with skeleton undo/redo.

test_set = basic_pin_set + pin_modifier_set
#test_set = pin_modifier_set
