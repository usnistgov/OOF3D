# -*- python -*-
# $RCSfile: skeleton_select_test.py,v $
# $Revision: 1.17 $
# $Author: langer $
# $Date: 2009/07/10 20:42:12 $


# Test suite for skeleton selection and group commands, not including
# boundary commands, which are tested separately.  


# This file assumes that microstructures, images, and pixel group
# menu items have all been tested and work, and that the skeleton_basic
# tests also work.

import unittest, os
import memorycheck

# Graphical selection stuff.
# OOF.Graphics_1.Toolbox.Select_Element,
# OOF.Graphics_1.Toolbox.Select_Segment,
# OOF.Graphics_1.Toolbox.Select_Node...
# Each of these has:
#  Single_<item>, Rectangle, Circle, Ellipse, Clear, Undo, Redo, Invert.
#  Element also has ByDominantPixel.

class Direct_Skeleton_Selection(unittest.TestCase):
    def setUp(self):
        global gfxmanager
        from ooflib.common.IO import gfxmanager
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        OOF.Microstructure.Create_From_ImageFile(
            filename="ms_data/small.ppm",
            microstructure_name="skeltest",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="skeltest:small.ppm", name_template="group%n")
        OOF.Skeleton.New(
            name="skelselect",
            microstructure="skeltest", 
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(left_right_periodicity=False,
                                           top_bottom_periodicity=False))
        OOF.Windows.Graphics.New()
        self.sk_context = skeletoncontext.skeletonContexts[
            "skeltest:skelselect"]
        self.e_selection = self.sk_context.elementselection
        self.s_selection = self.sk_context.segmentselection
        self.n_selection = self.sk_context.nodeselection
        #
        self.e_groups = self.sk_context.elementgroups
        self.s_groups = self.sk_context.segmentgroups
        self.n_groups = self.sk_context.nodegroups

    def tearDown(self):
        OOF.Graphics_1.File.Close()
#         OOF.Microstructure.Delete(microstructure="skeltest")


# Note: The skeleton context contains both the selection data and the
# skeleton.  The skeleton can be retrieved via getObject() on the
# context.  There are attributes in the context for each selection,
# and the list of currently selected objects (i.e. the
# currently-active selection as understood by the current skeleton)
# can be gotten through each selection's "retrieve" method.
class Direct_Element_Selection(Direct_Skeleton_Selection):
    def setUp(self):
        Direct_Skeleton_Selection.setUp(self)
        self.selection_menu = OOF.Graphics_1.Toolbox.Select_Element

    @memorycheck.check("skeltest")
    def SingleElement(self):
        self.assertEqual(self.e_selection.size(), 0)
        self.selection_menu.Single_Element(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.e_selection.size(), 1)
        e_set = self.e_selection.retrieve()
        self.assertEqual(len(e_set),1)
        self.assertEqual(list(e_set)[0].index, 9)

    @memorycheck.check("skeltest")
    def Rectangle(self):
        self.assertEqual(self.e_selection.size(), 0)
        self.selection_menu.Rectangle(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0), Point(12.0,18.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.e_selection.size(), 8)
        e_set = self.e_selection.retrieve()
        self.assertEqual(len(e_set),8)
        index_list = [26,27,34,35,42,43,50,51]
        for e in e_set:
            self.assert_( e.index in index_list)
            index_list.remove(e.index)

    @memorycheck.check("skeltest")
    def Circle(self):
        self.assertEqual(self.e_selection.size(), 0)
        self.selection_menu.Circle(
            skeleton="skeltest:skelselect",
            points=[Point(7.0,10.0), Point(11.0,7.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.e_selection.size(), 4)
        e_set = self.e_selection.retrieve()
        self.assertEqual(len(e_set),4)
        index_list = [26,27,34,35]
        for e in e_set:
            self.assert_( e.index in index_list)
            index_list.remove(e.index)

    @memorycheck.check("skeltest")
    def Ellipse(self):
        self.assertEqual(self.e_selection.size(), 0)
        self.selection_menu.Ellipse(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0), Point(12.0,18.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.e_selection.size(), 6)
        e_set = self.e_selection.retrieve()
        self.assertEqual(len(e_set),6)
        index_list = [26,27,34,35,42,43]
        for e in e_set:
            self.assert_( e.index in index_list)
            index_list.remove(e.index)

    @memorycheck.check("skeltest")
    def ByDominantPixel(self):
        self.assertEqual(self.e_selection.size(), 0)
        self.selection_menu.ByDominantPixel(
            skeleton="skeltest:skelselect",
            points=[Point(5.8,8.5)],
            shift=0,ctrl=0)
        self.assertEqual(self.e_selection.size(), 14)
        e_set = self.e_selection.retrieve()
        self.assertEqual(len(e_set),14)
        index_list = [16,17,24,25,26,27,28,32,33,34,35,36,41,42]
        for e in e_set:
            self.assert_( e.index in index_list)
            index_list.remove(e.index)

    # The actual selection dictionary for the whole skeleton-context's
    # stack is at self.elementselection.currentSelection().  This is
    # the thing whose ID should change when Undo/Redo events occur.
    @memorycheck.check("skeltest")
    def Invert(self):
        self.selection_menu.Single_Element(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        self.selection_menu.Invert(skeleton="skeltest:skelselect")
        e_set = self.e_selection.retrieve()
        self.assertEqual(len(e_set), 63)
        index_set = range(64)
        index_set.remove(9)
        for e in e_set:
            self.assert_( e.index in index_set)
            index_set.remove(e.index)
        
    @memorycheck.check("skeltest")
    def Undo(self):
        sel_id0 = id(self.e_selection.currentSelection())
        self.selection_menu.Single_Element(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id1 = id(self.e_selection.currentSelection())
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        sel_id2 = id(self.e_selection.currentSelection())
        self.assertEqual(len(self.e_selection.retrieve()), 0)
        self.assertNotEqual(sel_id0, sel_id1)
        self.assertEqual(sel_id0,sel_id2)

    @memorycheck.check("skeltest")
    def Redo(self):
        sel_id0 = id(self.e_selection.currentSelection())
        self.selection_menu.Single_Element(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id1 = id(self.e_selection.currentSelection())
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        self.selection_menu.Redo(skeleton="skeltest:skelselect")
        sel_id2 = id(self.e_selection.currentSelection())
        self.assertEqual(len(self.e_selection.retrieve()), 1)
        self.assertNotEqual(sel_id0, sel_id2)
        self.assertEqual(sel_id1,sel_id2)


    @memorycheck.check("skeltest")
    def Clear(self):
        self.selection_menu.Single_Element(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id0 = id(self.e_selection.currentSelection())
        self.selection_menu.Clear(skeleton="skeltest:skelselect")
        sel_id1 = id(self.e_selection.currentSelection())
        self.assertEqual(len(self.e_selection.retrieve()), 0)
        self.assertNotEqual(sel_id0, sel_id1)
                                           


class Direct_Segment_Selection(Direct_Skeleton_Selection):
    def setUp(self):
        Direct_Skeleton_Selection.setUp(self)
        self.selection_menu = OOF.Graphics_1.Toolbox.Select_Segment

    @memorycheck.check("skeltest")
    def SingleSegment(self):
        self.assertEqual(self.e_selection.size(), 0)
        self.selection_menu.Single_Segment(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.s_selection.size(), 1)
        s_set = self.s_selection.retrieve()
        self.assertEqual(len(s_set),1)
        self.assertEqual(list(s_set)[0].index, 29)

    @memorycheck.check("skeltest")
    def Rectangle(self):
        self.assertEqual(self.s_selection.size(), 0)
        self.selection_menu.Rectangle(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0), Point(12.0,18.0)],
            shift=0,ctrl=0)
        index_list = [48, 50, 62, 64, 65, 66, 67, 79, 81,
                      82, 83, 84, 96, 98, 99, 100, 101,
                      113, 115, 116, 117, 118]
        self.assertEqual(self.s_selection.size(), len(index_list))
        s_set = self.s_selection.retrieve()
        self.assertEqual(len(s_set),len(index_list))
        for s in s_set:
            self.assert_( s.index in index_list)
            index_list.remove(s.index)

    @memorycheck.check("skeltest")
    def Circle(self):
        self.assertEqual(self.s_selection.size(), 0)
        self.selection_menu.Circle(
            skeleton="skeltest:skelselect",
            points=[Point(7.0,10.0), Point(11.0,7.0)],
            shift=0,ctrl=0)
        index_list = [48, 50, 62, 63, 64, 65, 66, 67, 79, 81, 82, 83, 84]
        self.assertEqual(self.s_selection.size(), len(index_list))
        s_set = self.s_selection.retrieve()
        self.assertEqual(len(s_set),len(index_list))
        for s in s_set:
            self.assert_( s.index in index_list)
            index_list.remove(s.index)

    @memorycheck.check("skeltest")
    def Ellipse(self):
        self.assertEqual(self.s_selection.size(), 0)
        self.selection_menu.Ellipse(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0), Point(12.0,18.0)],
            shift=0,ctrl=0)
        index_list = [48, 50, 62, 64, 65, 66, 67, 79, 81, 82,
                      83, 84, 96, 98, 99, 100, 101, 115]
        self.assertEqual(self.s_selection.size(), len(index_list))
        s_set = self.s_selection.retrieve()
        self.assertEqual(len(s_set),len(index_list))
        for s in s_set:
            self.assert_( s.index in index_list)
            index_list.remove(s.index)

    # The actual selection dictionary for the whole skeleton-context's
    # stack is at self.segmentselection.currentSelection().  This is
    # the thing whose ID should change when Undo/Redo events occur.
    @memorycheck.check("skeltest")
    def Invert(self):
        self.selection_menu.Single_Segment(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        self.selection_menu.Invert(skeleton="skeltest:skelselect")
        s_set = self.s_selection.retrieve()
        self.assertEqual(len(s_set), 143)
        index_set = range(144)
        index_set.remove(29)
        for s in s_set:
            self.assert_( s.index in index_set)
            index_set.remove(s.index)
        
    @memorycheck.check("skeltest")
    def Undo(self):
        sel_id0 = id(self.s_selection.currentSelection())
        self.selection_menu.Single_Segment(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id1 = id(self.s_selection.currentSelection())
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        sel_id2 = id(self.s_selection.currentSelection())
        self.assertEqual(len(self.s_selection.retrieve()), 0)
        self.assertNotEqual(sel_id0, sel_id1)
        self.assertEqual(sel_id0,sel_id2)

    @memorycheck.check("skeltest")
    def Redo(self):
        sel_id0 = id(self.s_selection.currentSelection())
        self.selection_menu.Single_Segment(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id1 = id(self.s_selection.currentSelection())
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        self.selection_menu.Redo(skeleton="skeltest:skelselect")
        sel_id2 = id(self.s_selection.currentSelection())
        self.assertEqual(len(self.s_selection.retrieve()), 1)
        self.assertNotEqual(sel_id0, sel_id2)
        self.assertEqual(sel_id1,sel_id2)


    @memorycheck.check("skeltest")
    def Clear(self):
        self.selection_menu.Single_Segment(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id0 = id(self.s_selection.currentSelection())
        self.selection_menu.Clear(skeleton="skeltest:skelselect")
        sel_id1 = id(self.s_selection.currentSelection())
        self.assertEqual(len(self.s_selection.retrieve()), 0)
        self.assertNotEqual(sel_id0, sel_id1)
                                           




class Direct_Node_Selection(Direct_Skeleton_Selection):
    def setUp(self):
        Direct_Skeleton_Selection.setUp(self)
        self.selection_menu = OOF.Graphics_1.Toolbox.Select_Node

    @memorycheck.check("skeltest")
    def SingleNode(self):
        self.assertEqual(self.n_selection.size(), 0)
        self.selection_menu.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.n_selection.size(), 1)
        n_set = self.n_selection.retrieve()
        self.assertEqual(len(n_set),1)
        self.assertEqual(list(n_set)[0].index, 19)

    @memorycheck.check("skeltest")
    def Rectangle(self):
        self.assertEqual(self.n_selection.size(), 0)
        self.selection_menu.Rectangle(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0), Point(12.0,18.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.n_selection.size(), 15)
        n_set = self.n_selection.retrieve()
        self.assertEqual(len(n_set),15)
        index_list = [29, 30, 31, 38, 39, 40, 47, 48, 49,
                      56, 57, 58, 65, 66, 67]
        for n in n_set:
            self.assert_( n.index in index_list)
            index_list.remove(n.index)

    @memorycheck.check("skeltest")
    def Circle(self):
        self.assertEqual(self.n_selection.size(), 0)
        self.selection_menu.Circle(
            skeleton="skeltest:skelselect",
            points=[Point(7.0,10.0), Point(11.0,7.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.n_selection.size(), 10)
        n_set = self.n_selection.retrieve()
        self.assertEqual(len(n_set),10)
        index_list = [29, 30, 31, 37, 38, 39, 40, 47, 48, 49]
        for n in n_set:
            self.assert_( n.index in index_list)
            index_list.remove(n.index)

    @memorycheck.check("skeltest")
    def Ellipse(self):
        self.assertEqual(self.n_selection.size(), 0)
        self.selection_menu.Ellipse(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0), Point(12.0,18.0)],
            shift=0,ctrl=0)
        self.assertEqual(self.n_selection.size(), 13)
        n_set = self.n_selection.retrieve()
        self.assertEqual(len(n_set), 13)
        index_list = [29, 30, 31, 38, 39, 40, 47, 48, 49, 56, 57, 58, 66]
        for n in n_set:
            self.assert_( n.index in index_list)
            index_list.remove(n.index)

    # The actual selection dictionary for the whole skeleton-context's
    # stack is at self.elementselection.currentSelection().  This is
    # the thing whose ID should change when Undo/Redo events occur.
    @memorycheck.check("skeltest")
    def Invert(self):
        self.selection_menu.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        self.selection_menu.Invert(skeleton="skeltest:skelselect")
        n_set = self.n_selection.retrieve()
        self.assertEqual(len(n_set), 80)
        index_set = range(81)
        index_set.remove(19)
        for n in n_set:
            self.assert_( n.index in index_set)
            index_set.remove(n.index)
        
    @memorycheck.check("skeltest")
    def Undo(self):
        sel_id0 = id(self.n_selection.currentSelection())
        self.selection_menu.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id1 = id(self.n_selection.currentSelection())
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        sel_id2 = id(self.n_selection.currentSelection())
        self.assertEqual(len(self.n_selection.retrieve()), 0)
        self.assertNotEqual(sel_id0, sel_id1)
        self.assertEqual(sel_id0,sel_id2)

    @memorycheck.check("skeltest")
    def Redo(self):
        sel_id0 = id(self.n_selection.currentSelection())
        self.selection_menu.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id1 = id(self.n_selection.currentSelection())
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        self.selection_menu.Redo(skeleton="skeltest:skelselect")
        sel_id2 = id(self.n_selection.currentSelection())
        self.assertEqual(len(self.n_selection.retrieve()), 1)
        self.assertNotEqual(sel_id0, sel_id2)
        self.assertEqual(sel_id1,sel_id2)


    @memorycheck.check("skeltest")
    def Clear(self):
        self.selection_menu.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0,ctrl=0)
        sel_id0 = id(self.n_selection.currentSelection())
        self.selection_menu.Clear(skeleton="skeltest:skelselect")
        sel_id1 = id(self.n_selection.currentSelection())
        self.assertEqual(len(self.n_selection.retrieve()), 0)
        self.assertNotEqual(sel_id0, sel_id1)



########################################################################
# Node pinning stuff.                                                  #
########################################################################

# OOF.Graphics_1.Toolbox.Pin_Nodes:
# Pin UnPin TogglePin Undo Redo Invert.


class Direct_Pin_Nodes(Direct_Skeleton_Selection):
    @memorycheck.check("skeltest")
    def Pin(self):
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 1)
        for n in self.sk_context.getObject().nodes:
            if n.index == 20:
                self.assert_(n.pinned())
            else:
                self.assert_(not n.pinned())

    @memorycheck.check("skeltest")
    def UnPin(self):
        # Pin two, and unpin one.
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(7.25,5.25))
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 2)
        OOF.Graphics_1.Toolbox.Pin_Nodes.UnPin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 1)
        for n in self.sk_context.getObject().nodes:
            if n.index==21:
                self.assert_(n.pinned())
            else:
                self.assert_(not n.pinned())

    @memorycheck.check("skeltest")
    def TogglePin(self):
        # Pin two, and toggle one.
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(7.25,5.25))
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 2)
        OOF.Graphics_1.Toolbox.Pin_Nodes.TogglePin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 1)
        for n in self.sk_context.getObject().nodes:
            if n.index==21:
                self.assert_(n.pinned())
            else:
                self.assert_(not n.pinned())

    @memorycheck.check("skeltest")
    def Undo(self):
        pin0 = self.sk_context.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        pin1 = self.sk_context.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Undo(
            skeleton="skeltest:skelselect")
        pin2 = self.sk_context.pinnednodes.stack.current()
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 0)
        self.assertEqual(id(pin0), id(pin2))
        self.assertNotEqual(id(pin0), id(pin1))

    @memorycheck.check("skeltest")
    def Redo(self):
        pin0 = self.sk_context.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        pin1 = self.sk_context.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Undo(
            skeleton="skeltest:skelselect")
        pin2 = self.sk_context.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Redo(
            skeleton="skeltest:skelselect")
        pin3 = self.sk_context.pinnednodes.stack.current()
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 1)
        self.assertNotEqual(id(pin0), id(pin1))
        self.assertEqual(id(pin1),id(pin3))

    @memorycheck.check("skeltest")
    def Invert(self):
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        OOF.Graphics_1.Toolbox.Pin_Nodes.Invert(
            skeleton="skeltest:skelselect")
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 80)
        # Ensure that only node 20 is unpinned.
        for n in self.sk_context.getObject().nodes:
            if n.index==20:
                self.assert_(not n.pinned())
            else:
                self.assert_(n.pinned())



class Skeleton_PinNodes(Direct_Skeleton_Selection):
    @memorycheck.check("skeltest")
    def Pin_Node_Selection(self):
        # Selects the node with index 10.
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(2.75, 2.75)],
            shift=0, ctrl=0)
        OOF.Skeleton.PinNodes.Pin_Node_Selection(
            skeleton="skeltest:skelselect")
        OOF.Graphics_1.Toolbox.Select_Node.Clear(
            skeleton="skeltest:skelselect")
        # Verify that the right node is pinned.
        node = self.sk_context.getObject().getNode(10)
        self.assert_(node.pinned())
        # Verify that no others are.
        for n in self.sk_context.getObject().nodes:
            if n.index != 10:
                self.assert_(not n.pinned())
                
    @memorycheck.check("skeltest")
    def UnPin_Node_Selection(self):
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(2.75, 2.75)],
            shift=0, ctrl=0)
        OOF.Skeleton.PinNodes.Pin_Node_Selection(
            skeleton="skeltest:skelselect")
        OOF.Skeleton.PinNodes.UnPin_Node_Selection(
            skeleton="skeltest:skelselect")
        OOF.Graphics_1.Toolbox.Select_Node.Clear(
            skeleton="skeltest:skelselect")
        for n in self.sk_context.getObject().nodes:
            self.assert_(not n.pinned())

    @memorycheck.check("skeltest")
    def Pin_Internal_Boundary_Nodes(self):
        OOF.Skeleton.PinNodes.Pin_Internal_Boundary_Nodes(
            skeleton="skeltest:skelselect")
        nodes = self.sk_context.getObject().nodes
        pinned_set = [ x.index for x in nodes if x.pinned()]
        not_pinned_set = [x.index for x in nodes if not x.pinned()]
        self.assertEqual(
            pinned_set,
            [3, 4, 12, 13, 18, 19, 20, 21, 22, 23, 24, 25, 26, 29, 30,
             31, 32, 33, 41, 45, 46, 48, 49, 50, 51, 52, 53, 54, 55, 56,
             57, 58, 59, 60, 61, 62, 64, 65, 66, 67, 73, 74, 75, 76] )
        self.assertEqual(
            not_pinned_set,
            [0, 1, 2, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 27, 28, 34,
             35, 36, 37, 38, 39, 40, 42, 43, 44, 47, 63, 68, 69, 70, 71,
             72, 77, 78, 79, 80])

    @memorycheck.check("skeltest")
    def Pin_Selected_Segments(self):
        # Select segment with nodes 10 and 11.
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:skelselect",
            points=[Point(3.75,2.75)], shift=0, ctrl=0)
        OOF.Skeleton.PinNodes.Pin_Selected_Segments(
            skeleton="skeltest:skelselect")
        OOF.Graphics_1.Toolbox.Select_Segment.Clear(
            skeleton="skeltest:skelselect")
        for n in self.sk_context.getObject().nodes:
            if n.index==10 or n.index==11:
                self.assert_(n.pinned())
            else:
                self.assert_(not n.pinned())

    @memorycheck.check("skeltest")
    def Pin_Selected_Elements(self):
        # Select a bunch of elements, so we can determine correct
        # operation of internal.
        OOF.Graphics_1.Toolbox.Select_Element.Rectangle(
            skeleton="skeltest:skelselect",
            points=[Point(2.25,2.25),Point(7.75,7.75)], shift=0, ctrl=0)
        OOF.Skeleton.PinNodes.Pin_Selected_Elements(
            skeleton="skeltest:skelselect", internal=False, boundary=True)
        OOF.Graphics_1.Toolbox.Select_Element.Clear(
            skeleton="skeltest:skelselect")
        for n in self.sk_context.getObject().nodes:
            if n.index in [10,11,12,19,21,28,29,30]:
                self.assert_(n.pinned())
            else:
                self.assert_(not n.pinned())

    # Just select directly -- assumes the pinnodes toolbox has been
    # tested, and that the skeleton is automatically in the graphics
    # window, etc.
    @memorycheck.check("skeltest")
    def Undo(self):
        pin0 = self.sk_context.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        pin1 = self.sk_context.pinnednodes.stack.current()
        OOF.Skeleton.PinNodes.Undo(skeleton="skeltest:skelselect")
        pin2 = self.sk_context.pinnednodes.stack.current()
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 0)
        self.assertEqual(id(pin0), id(pin2))
        self.assertNotEqual(id(pin0), id(pin1))


    @memorycheck.check("skeltest")
    def Redo(self):
        pin0 = self.sk_context.pinnednodes.stack.current()
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        pin1 = self.sk_context.pinnednodes.stack.current()
        OOF.Skeleton.PinNodes.Undo(skeleton="skeltest:skelselect")
        pin2 = self.sk_context.pinnednodes.stack.current()
        OOF.Skeleton.PinNodes.Redo(skeleton="skeltest:skelselect")
        pin3 = self.sk_context.pinnednodes.stack.current()
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 1)
        self.assertNotEqual(id(pin0), id(pin1))
        self.assertEqual(id(pin1),id(pin3))


    @memorycheck.check("skeltest")
    def Invert(self):
        OOF.Graphics_1.Toolbox.Pin_Nodes.Pin(
            skeleton="skeltest:skelselect", point=Point(5.25,5.25))
        OOF.Skeleton.PinNodes.Invert(skeleton="skeltest:skelselect")
        self.assertEqual(self.sk_context.pinnednodes.npinned(), 80)
        # Ensure that only node 20 is unpinned.
        for n in self.sk_context.getObject().nodes:
            if n.index==20:
                self.assert_(not n.pinned())
            else:
                self.assert_(n.pinned())
        

# PinNodes:
# Pin_Node_Selection, UnPin_Node_Selection, Pin_Internal_Boundary_Nodes,
# Pin_Selected_Segments, Pin_Selected_Elements, UnpinAll,
# Undo, Redo, Invert.


########################################################################
# Group stuff.                                                         #
########################################################################


class Skeleton_Element_Group(Direct_Element_Selection):
    @memorycheck.check("skeltest")
    def New_Group(self):
        OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup")
        self.assert_(self.e_groups.isGroup("testgroup"))
        self.assertEqual(len(self.e_groups.get_group("testgroup")), 0)

    def populate_test_group(self):
        OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup")
        self.selection_menu.Single_Element(
            skeleton="skeltest:skelselect",
            points=[Point(3.0,5.0)],
            shift=0, ctrl=0)
        OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup")

    @memorycheck.check("skeltest")
    def Add_to_Group(self):
        self.populate_test_group()
        e_set = self.e_groups.get_group("testgroup")
        self.assertEqual(len(e_set), 1)
        self.assertEqual(list(e_set)[0].index, 9)
        
    @memorycheck.check("skeltest")
    def Remove_from_Group(self):
        self.populate_test_group()
        self.selection_menu.Single_Element(
            skeleton="skeltest:skelselect", points=[Point(6.25,3.75)],
            shift=0, ctrl=0)
        OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup")
        eset0 = self.e_groups.get_group("testgroup")
        self.assert_( 9 in [e.index for e in eset0] )
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        OOF.ElementGroup.Remove_from_Group(skeleton="skeltest:skelselect",
                                           group="testgroup")
        eset1 = self.e_groups.get_group("testgroup")
        self.assertEqual(len(eset1),1)
        self.assertNotEqual(list(eset1)[0].index, 9)

    @memorycheck.check("skeltest")
    def Copy_Group(self):
        self.populate_test_group()
        e_set0 = self.e_groups.get_group("testgroup")
        OOF.ElementGroup.Copy_Group(skeleton="skeltest:skelselect",
                                    group="testgroup",
                                    new_name="testcopy")
        self.assert_(self.e_groups.isGroup("testcopy"))
        e_set1 = self.e_groups.get_group("testcopy")
        self.assertNotEqual(id(e_set0), id(e_set1))
        self.assertEqual(len(e_set0),len(e_set1))
        # Since we only selected one element, both lists are of length 1.
        self.assertEqual(list(e_set0)[0], list(e_set1)[0])
        

    @memorycheck.check("skeltest")
    def Delete_Group(self):
        self.populate_test_group()
        e_set0 = self.e_groups.get_group("testgroup")
        OOF.ElementGroup.Delete_Group(skeleton="skeltest:skelselect",
                                    group="testgroup")
        self.assert_(not self.e_groups.isGroup("testgroup"))

    @memorycheck.check("skeltest")
    def Rename_Group(self):
        self.populate_test_group()
        e_set0 = self.e_groups.get_group("testgroup")
        OOF.ElementGroup.Rename_Group(skeleton="skeltest:skelselect",
                                      group="testgroup",
                                      new_name="testrename")
        self.assert_(not self.e_groups.isGroup("testgroup"))
        self.assert_(self.e_groups.isGroup("testrename"))
        e_set1 = self.e_groups.get_group("testrename")
        self.assertEqual(id(e_set0), id(e_set1))

    @memorycheck.check("skeltest")
    def Clear_Group(self):
        self.populate_test_group()
        OOF.ElementGroup.Clear_Group(skeleton="skeltest:skelselect",
                                     group="testgroup")
        e_set1 = self.e_groups.get_group("testgroup")
        self.assertEqual(len(e_set1),0)
        

    @memorycheck.check("skeltest")
    def Query_Group(self):
        self.populate_test_group()
        OOF.ElementGroup.Query_Group(skeleton="skeltest:skelselect",
                                     group="testgroup")
        # This menu item generates a message in the reporter -- see if
        # it was the right one.
        global reporter
        from ooflib.common.IO import reporter
        mstring = reporter.messagemanager.message_list[-1][0]
        self.assertEqual(
        "Group 'testgroup', 1 element, area=6.25, average homogeneity=0.993956",
            mstring)

    @memorycheck.check("skeltest")
    def Material_Group(self):
        # Select a 2x2 set of elements in the lower left corner and
        # store it as testgroup1.
        self.selection_menu.Rectangle(
            skeleton="skeltest:skelselect",
            points=[Point(-.5, 6), Point(6, -.5)], shift=0, ctrl=0)
        OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup1")
        OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup1")
        # Select a 2x2 set offset to the northeast by one element and
        # store them as testgroup2.  This group overlaps with
        # testgroup1.
        self.selection_menu.Rectangle(
            skeleton="skeltest:skelselect",
            points=[Point(2.1, 8.1), Point(8.1, 2.1)], shift=0, ctrl=0)
        OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup2")
        OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup2")
        # Create a third group with no overlap with the other two.
        self.selection_menu.Rectangle(
            skeleton="skeltest:skelselect",
            points=[Point(12.1, 18.1), Point(18.1, 12.1)], shift=0, ctrl=0)
        OOF.ElementGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup3")
        OOF.ElementGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup3")
        

        OOF.Material.New(name='material1', material_type='bulk')
        OOF.Material.New(name='material2', material_type='bulk')

        # Assign a material to one of the overlapping groups
        OOF.ElementGroup.Assign_Material(skeleton="skeltest:skelselect",
                                         group="testgroup1",
                                         material="material1")
        # Check that the four elements in testgroup1 have the right
        # material.
        for elem in self.e_groups.get_group("testgroup1"):
            material = elem.material(self.sk_context)
            self.assert_(material is not None)
            self.assertEqual(material.name(), "material1")
        # Check that the non-overlapping group has no materials
        for elem in self.e_groups.get_group("testgroup3"):
            self.assert_(elem.material(self.sk_context) is None)
            
        # Remove material
        OOF.ElementGroup.Remove_Material(skeleton="skeltest:skelselect",
                                         group="testgroup1")
        for elem in self.e_groups.get_group("testgroup1"):
            material = elem.material(self.sk_context)
            self.assertEqual(material, None)
        # Re-assign the material.
        OOF.ElementGroup.Assign_Material(skeleton="skeltest:skelselect",
                                         group="testgroup1",
                                         material="material1")

        # Assign a material to the other overlapping group.
        OOF.ElementGroup.Assign_Material(skeleton="skeltest:skelselect",
                                         group="testgroup2",
                                         material="material2")
        # Check that all of the elements in this group have the right
        # material.
        for elem in self.e_groups.get_group("testgroup2"):
            material = elem.material(self.sk_context)
            self.assert_(material is not None)
            self.assertEqual(material.name(), "material2")
        # Check that one element in the first group has had its
        # material overwritten by the second group's material.
        materials = [e.material(self.sk_context)
                     for e in self.e_groups.get_group("testgroup1")]
        self.assertEqual(materials.count(None), 0)
        matnames = [m.name() for m in materials]
        self.assertEqual(matnames.count("material2"), 1)
        self.assertEqual(matnames.count("material1"), 3)
        # Check that the non-overlapping group has no materials
        for elem in self.e_groups.get_group("testgroup3"):
            self.assert_(elem.material(self.sk_context) is None)

        # Remove material from testgroup2
        OOF.ElementGroup.Remove_Material(skeleton="skeltest:skelselect",
                                         group="testgroup2")
        # Check that all elements in testgroup1 are back to their
        # original material.
        for elem in self.e_groups.get_group("testgroup1"):
            material = elem.material(self.sk_context)
            self.assert_(material is not None)
            self.assertEqual(material.name(), "material1")
        # Check that one element in testgroup2 is material1, and the
        # others are None.
        materials = [e.material(self.sk_context)
                     for e in self.e_groups.get_group("testgroup2")]
        self.assertEqual(materials.count(None), 3)
        matnames = [m.name() for m in materials if m is not None]
        self.assertEqual(len(matnames), 1)
        self.assertEqual(matnames[0], "material1")
        
        # Check the non-overlapping group again, just to be sure.
        for elem in self.e_groups.get_group("testgroup3"):
            self.assert_(elem.material(self.sk_context) is None)
        
        OOF.Material.Delete(name='material1')
        OOF.Material.Delete(name='material2')
        

    @memorycheck.check("skeltest")
    def Auto_Group(self):
        OOF.ElementGroup.Auto_Group(skeleton='skeltest:skelselect')
        self.assert_(self.e_groups.isGroup("group0"))
        self.assert_(self.e_groups.isGroup("group1"))
        self.assert_(self.e_groups.isGroup("group2"))
        self.assert_(self.e_groups.isGroup("group3"))
        self.assert_(self.e_groups.isGroup("group4"))
        self.assert_(self.e_groups.isGroup("group5"))
        self.assert_(self.e_groups.isGroup("group6"))
        self.assert_(self.e_groups.isGroup("group7"))
        self.assertEqual(len(self.e_groups.get_group("group0")), 7)
        self.assertEqual(len(self.e_groups.get_group("group1")), 15)
        self.assertEqual(len(self.e_groups.get_group("group2")), 8)
        self.assertEqual(len(self.e_groups.get_group("group3")), 8)
        self.assertEqual(len(self.e_groups.get_group("group4")), 14)
        self.assertEqual(len(self.e_groups.get_group("group5")), 2)
        self.assertEqual(len(self.e_groups.get_group("group6")), 9)
        self.assertEqual(len(self.e_groups.get_group("group7")), 1)
        OOF.ElementGroup.Clear_All(skeleton='skeltest:skelselect')
        self.assertEqual(len(self.e_groups.get_group("group0")), 0)
        self.assertEqual(len(self.e_groups.get_group("group1")), 0)
        self.assertEqual(len(self.e_groups.get_group("group2")), 0)
        self.assertEqual(len(self.e_groups.get_group("group3")), 0)
        self.assertEqual(len(self.e_groups.get_group("group4")), 0)
        self.assertEqual(len(self.e_groups.get_group("group5")), 0)
        self.assertEqual(len(self.e_groups.get_group("group6")), 0)
        self.assertEqual(len(self.e_groups.get_group("group7")), 0)
        OOF.ElementGroup.Delete_All(skeleton='skeltest:skelselect')
        self.assert_(not self.e_groups.isGroup("group0"))
        self.assert_(not self.e_groups.isGroup("group1"))
        self.assert_(not self.e_groups.isGroup("group2"))
        self.assert_(not self.e_groups.isGroup("group3"))
        self.assert_(not self.e_groups.isGroup("group4"))
        self.assert_(not self.e_groups.isGroup("group5"))
        self.assert_(not self.e_groups.isGroup("group6"))
        self.assert_(not self.e_groups.isGroup("group7"))


class Skeleton_Segment_Group(Direct_Segment_Selection):
    @memorycheck.check("skeltest")
    def New_Group(self):
        OOF.SegmentGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup")
        self.assert_(self.s_groups.isGroup("testgroup"))
        self.assertEqual(len(self.s_groups.get_group("testgroup")), 0)

    def populate_test_group(self):
        OOF.SegmentGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup")
        self.selection_menu.Single_Segment(
            skeleton="skeltest:skelselect",
            points=[Point(3.75,4.95)],
            shift=0, ctrl=0)
        OOF.SegmentGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup")
        
    @memorycheck.check("skeltest")
    def Add_to_Group(self):
        self.populate_test_group()
        s_set = self.s_groups.get_group("testgroup")
        self.assertEqual(len(s_set), 1)
        self.assertEqual(list(s_set)[0].index, 29)
        
    @memorycheck.check("skeltest")
    def Remove_from_Group(self):
        self.populate_test_group()
        self.selection_menu.Single_Segment(
            skeleton="skeltest:skelselect", points=[Point(6.25,4.95)],
            shift=0, ctrl=0)
        OOF.SegmentGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup")
        sset0 = self.s_groups.get_group("testgroup")
        self.assert_( 29 in [s.index for s in sset0] )
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        OOF.SegmentGroup.Remove_from_Group(skeleton="skeltest:skelselect",
                                           group="testgroup")
        sset1 = self.s_groups.get_group("testgroup")
        self.assertEqual(len(sset1),1)
        self.assertNotEqual(list(sset1)[0].index, 29)

    @memorycheck.check("skeltest")
    def Copy_Group(self):
        self.populate_test_group()
        s_set0 = self.s_groups.get_group("testgroup")
        OOF.SegmentGroup.Copy_Group(skeleton="skeltest:skelselect",
                                    group="testgroup",
                                    new_name="testcopy")
        self.assert_(self.s_groups.isGroup("testcopy"))
        s_set1 = self.s_groups.get_group("testcopy")
        self.assertNotEqual(id(s_set0), id(s_set1))
        self.assertEqual(len(s_set0),len(s_set1))
        # Since we only selected one segment, both lists are of length 1.
        self.assertEqual(list(s_set0)[0], list(s_set1)[0])
        

    @memorycheck.check("skeltest")
    def Delete_Group(self):
        self.populate_test_group()
        s_set0 = self.s_groups.get_group("testgroup")
        OOF.SegmentGroup.Delete_Group(skeleton="skeltest:skelselect",
                                    group="testgroup")
        self.assert_(not self.s_groups.isGroup("testgroup"))

    @memorycheck.check("skeltest")
    def Rename_Group(self):
        self.populate_test_group()
        s_set0 = self.s_groups.get_group("testgroup")
        OOF.SegmentGroup.Rename_Group(skeleton="skeltest:skelselect",
                                      group="testgroup",
                                      new_name="testrename")
        self.assert_(not self.s_groups.isGroup("testgroup"))
        self.assert_(self.s_groups.isGroup("testrename"))
        s_set1 = self.s_groups.get_group("testrename")
        self.assertEqual(id(s_set0), id(s_set1))

    @memorycheck.check("skeltest")
    def Clear_Group(self):
        self.populate_test_group()
        OOF.SegmentGroup.Clear_Group(skeleton="skeltest:skelselect",
                                     group="testgroup")
        s_set1 = self.s_groups.get_group("testgroup")
        self.assertEqual(len(s_set1),0)
        

    @memorycheck.check("skeltest")
    def Query_Group(self):
        self.populate_test_group()
        OOF.SegmentGroup.Query_Group(skeleton="skeltest:skelselect",
                                     group="testgroup")
        # This menu item generates a message in the reporter -- see if
        # it was the right one.
        global reporter
        from ooflib.common.IO import reporter
        mstring = reporter.messagemanager.message_list[-1][0]
        self.assertEqual(
            ">>>  1  segment",
            mstring)
        
    @memorycheck.check("skeltest")
    def Auto_Group(self):
        OOF.SegmentGroup.Auto_Group(skeleton='skeltest:skelselect')
        self.assert_(self.s_groups.isGroup("group0"))
        self.assert_(self.s_groups.isGroup("group1"))
        self.assert_(self.s_groups.isGroup("group2"))
        self.assert_(self.s_groups.isGroup("group3"))
        self.assert_(self.s_groups.isGroup("group4"))
        self.assert_(self.s_groups.isGroup("group5"))
        self.assert_(self.s_groups.isGroup("group6"))
        self.assert_(self.s_groups.isGroup("group7"))
        self.assertEqual(len(self.s_groups.get_group("group0")), 17)
        self.assertEqual(len(self.s_groups.get_group("group1")), 27)
        self.assertEqual(len(self.s_groups.get_group("group2")), 18)
        self.assertEqual(len(self.s_groups.get_group("group3")), 18)
        self.assertEqual(len(self.s_groups.get_group("group4")), 30)
        self.assertEqual(len(self.s_groups.get_group("group5")), 9)
        self.assertEqual(len(self.s_groups.get_group("group6")), 22)
        self.assertEqual(len(self.s_groups.get_group("group7")), 3)
        OOF.SegmentGroup.Clear_All(skeleton='skeltest:skelselect')
        self.assertEqual(len(self.s_groups.get_group("group0")), 0)
        self.assertEqual(len(self.s_groups.get_group("group1")), 0)
        self.assertEqual(len(self.s_groups.get_group("group2")), 0)
        self.assertEqual(len(self.s_groups.get_group("group3")), 0)
        self.assertEqual(len(self.s_groups.get_group("group4")), 0)
        self.assertEqual(len(self.s_groups.get_group("group5")), 0)
        self.assertEqual(len(self.s_groups.get_group("group6")), 0)
        self.assertEqual(len(self.s_groups.get_group("group7")), 0)
        OOF.SegmentGroup.Delete_All(skeleton='skeltest:skelselect')
        self.assert_(not self.s_groups.isGroup("group0"))
        self.assert_(not self.s_groups.isGroup("group1"))
        self.assert_(not self.s_groups.isGroup("group2"))
        self.assert_(not self.s_groups.isGroup("group3"))
        self.assert_(not self.s_groups.isGroup("group4"))
        self.assert_(not self.s_groups.isGroup("group5"))
        self.assert_(not self.s_groups.isGroup("group6"))
        self.assert_(not self.s_groups.isGroup("group7"))

class Skeleton_Node_Group(Direct_Node_Selection):
    @memorycheck.check("skeltest")
    def New_Group(self):
        OOF.NodeGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup")
        self.assert_(self.n_groups.isGroup("testgroup"))
        self.assertEqual(len(self.n_groups.get_group("testgroup")), 0)

    def populate_test_group(self):
        OOF.NodeGroup.New_Group(skeleton="skeltest:skelselect",
                                   name="testgroup")
        self.selection_menu.Single_Node(
            skeleton="skeltest:skelselect",
            points=[Point(4.95,4.95)],
            shift=0, ctrl=0)
        OOF.NodeGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup")

    @memorycheck.check("skeltest")
    def Add_to_Group(self):
        self.populate_test_group()
        n_set = self.n_groups.get_group("testgroup")
        self.assertEqual(len(n_set), 1)
        self.assertEqual(list(n_set)[0].index, 20)
        
    @memorycheck.check("skeltest")
    def Remove_from_Group(self):
        self.populate_test_group()
        self.selection_menu.Single_Node(
            skeleton="skeltest:skelselect", points=[Point(7.25,4.95)],
            shift=0, ctrl=0)
        OOF.NodeGroup.Add_to_Group(skeleton="skeltest:skelselect",
                                      group="testgroup")
        nset0 = self.n_groups.get_group("testgroup")
        self.assert_( 20 in [n.index for n in nset0] )
        self.selection_menu.Undo(skeleton="skeltest:skelselect")
        OOF.NodeGroup.Remove_from_Group(skeleton="skeltest:skelselect",
                                           group="testgroup")
        nset1 = self.n_groups.get_group("testgroup")
        self.assertEqual(len(nset1),1)
        self.assertNotEqual(list(nset1)[0].index, 20)

    @memorycheck.check("skeltest")
    def Copy_Group(self):
        self.populate_test_group()
        n_set0 = self.n_groups.get_group("testgroup")
        OOF.NodeGroup.Copy_Group(skeleton="skeltest:skelselect",
                                    group="testgroup",
                                    new_name="testcopy")
        self.assert_(self.n_groups.isGroup("testcopy"))
        n_set1 = self.n_groups.get_group("testcopy")
        self.assertNotEqual(id(n_set0), id(n_set1))
        self.assertEqual(len(n_set0),len(n_set1))
        # Since we only selected one element, both lists are of length 1.
        self.assertEqual(list(n_set0)[0], list(n_set1)[0])
        

    @memorycheck.check("skeltest")
    def Delete_Group(self):
        self.populate_test_group()
        n_set0 = self.n_groups.get_group("testgroup")
        OOF.NodeGroup.Delete_Group(skeleton="skeltest:skelselect",
                                    group="testgroup")
        self.assert_(not self.n_groups.isGroup("testgroup"))

    @memorycheck.check("skeltest")
    def Rename_Group(self):
        self.populate_test_group()
        n_set0 = self.n_groups.get_group("testgroup")
        OOF.NodeGroup.Rename_Group(skeleton="skeltest:skelselect",
                                      group="testgroup",
                                      new_name="testrename")
        self.assert_(not self.n_groups.isGroup("testgroup"))
        self.assert_(self.n_groups.isGroup("testrename"))
        n_set1 = self.n_groups.get_group("testrename")
        self.assertEqual(id(n_set0), id(n_set1))

    @memorycheck.check("skeltest")
    def Clear_Group(self):
        self.populate_test_group()
        OOF.NodeGroup.Clear_Group(skeleton="skeltest:skelselect",
                                     group="testgroup")
        n_set1 = self.n_groups.get_group("testgroup")
        self.assertEqual(len(n_set1),0)
        

    @memorycheck.check("skeltest")
    def Query_Group(self):
        self.populate_test_group()
        OOF.NodeGroup.Query_Group(skeleton="skeltest:skelselect",
                                     group="testgroup")
        # This menu item generates a message in the reporter -- see if
        # it was the right one.
        global reporter
        from ooflib.common.IO import reporter
        mstring = reporter.messagemanager.message_list[-1][0]
        self.assertEqual(
            ">>>  1  node",
            mstring)
        
    @memorycheck.check("skeltest")
    def Auto_Group(self):
        OOF.NodeGroup.Auto_Group(skeleton='skeltest:skelselect')
        self.assert_(self.n_groups.isGroup("group0"))
        self.assert_(self.n_groups.isGroup("group1"))
        self.assert_(self.n_groups.isGroup("group2"))
        self.assert_(self.n_groups.isGroup("group3"))
        self.assert_(self.n_groups.isGroup("group4"))
        self.assert_(self.n_groups.isGroup("group5"))
        self.assert_(self.n_groups.isGroup("group6"))
        self.assert_(self.n_groups.isGroup("group7"))
        self.assertEqual(len(self.n_groups.get_group("group0")), 10)
        self.assertEqual(len(self.n_groups.get_group("group1")), 15)
        self.assertEqual(len(self.n_groups.get_group("group2")), 11)
        self.assertEqual(len(self.n_groups.get_group("group3")), 10)
        self.assertEqual(len(self.n_groups.get_group("group4")), 15)
        self.assertEqual(len(self.n_groups.get_group("group5")), 4)
        self.assertEqual(len(self.n_groups.get_group("group6")), 13)
        self.assertEqual(len(self.n_groups.get_group("group7")), 3)
        OOF.NodeGroup.Clear_All(skeleton='skeltest:skelselect')
        self.assertEqual(len(self.n_groups.get_group("group0")), 0)
        self.assertEqual(len(self.n_groups.get_group("group1")), 0)
        self.assertEqual(len(self.n_groups.get_group("group2")), 0)
        self.assertEqual(len(self.n_groups.get_group("group3")), 0)
        self.assertEqual(len(self.n_groups.get_group("group4")), 0)
        self.assertEqual(len(self.n_groups.get_group("group5")), 0)
        self.assertEqual(len(self.n_groups.get_group("group6")), 0)
        self.assertEqual(len(self.n_groups.get_group("group7")), 0)
        OOF.NodeGroup.Delete_All(skeleton='skeltest:skelselect')
        self.assert_(not self.n_groups.isGroup("group0"))
        self.assert_(not self.n_groups.isGroup("group1"))
        self.assert_(not self.n_groups.isGroup("group2"))
        self.assert_(not self.n_groups.isGroup("group3"))
        self.assert_(not self.n_groups.isGroup("group4"))
        self.assert_(not self.n_groups.isGroup("group5"))
        self.assert_(not self.n_groups.isGroup("group6"))
        self.assert_(not self.n_groups.isGroup("group7"))



# Routine to do regression-type testing on the items in this file.
# Tests must be run in the order they appear in the list.  This
# routine will stop after the first failure.
def run_tests():
    element_set = [
        Direct_Element_Selection("SingleElement"),
        Direct_Element_Selection("Rectangle"),
        Direct_Element_Selection("Circle"),
        Direct_Element_Selection("Ellipse"),
        Direct_Element_Selection("ByDominantPixel"),
        Direct_Element_Selection("Invert"),
        Direct_Element_Selection("Undo"),
        Direct_Element_Selection("Redo"),
        Direct_Element_Selection("Clear")
        ]

    segment_set = [
        Direct_Segment_Selection("SingleSegment"),
        Direct_Segment_Selection("Rectangle"),
        Direct_Segment_Selection("Circle"),
        Direct_Segment_Selection("Ellipse"),
        Direct_Segment_Selection("Invert"),
        Direct_Segment_Selection("Undo"),
        Direct_Segment_Selection("Redo"),
        Direct_Segment_Selection("Clear")
        ]
    
    node_set = [
        Direct_Node_Selection("SingleNode"),
        Direct_Node_Selection("Rectangle"),
        Direct_Node_Selection("Circle"),
        Direct_Node_Selection("Ellipse"),
        Direct_Node_Selection("Invert"),
        Direct_Node_Selection("Undo"),
        Direct_Node_Selection("Redo"),
        Direct_Node_Selection("Clear")
        ]

    direct_pin_set = [
        Direct_Pin_Nodes("Pin"),
        Direct_Pin_Nodes("UnPin"),
        Direct_Pin_Nodes("TogglePin"),
        Direct_Pin_Nodes("Undo"),
        Direct_Pin_Nodes("Redo"),
        Direct_Pin_Nodes("Invert")
        ]
    
    page_pin_set = [
        Skeleton_PinNodes("Pin_Node_Selection"),
        Skeleton_PinNodes("UnPin_Node_Selection"),
        Skeleton_PinNodes("Pin_Internal_Boundary_Nodes"),
        Skeleton_PinNodes("Pin_Selected_Segments"),
        Skeleton_PinNodes("Pin_Selected_Elements"),
        Skeleton_PinNodes("Undo"), 
        Skeleton_PinNodes("Redo"), 
        Skeleton_PinNodes("Invert") 
        ]
    
    element_group = [
        Skeleton_Element_Group("New_Group"),
        Skeleton_Element_Group("Add_to_Group"),
        Skeleton_Element_Group("Remove_from_Group"),
        Skeleton_Element_Group("Copy_Group"),
        Skeleton_Element_Group("Delete_Group"),
        Skeleton_Element_Group("Rename_Group"),
        Skeleton_Element_Group("Clear_Group"),
        Skeleton_Element_Group("Query_Group"),
        Skeleton_Element_Group("Material_Group"),
        Skeleton_Element_Group("Auto_Group")
        ]

    segment_group = [
        Skeleton_Segment_Group("New_Group"),
        Skeleton_Segment_Group("Add_to_Group"),
        Skeleton_Segment_Group("Remove_from_Group"),
        Skeleton_Segment_Group("Copy_Group"),
        Skeleton_Segment_Group("Delete_Group"),
        Skeleton_Segment_Group("Rename_Group"),
        Skeleton_Segment_Group("Clear_Group"),
        Skeleton_Segment_Group("Query_Group"),
        Skeleton_Segment_Group("Auto_Group")
        ]

    node_group = [
        Skeleton_Node_Group("New_Group"),
        Skeleton_Node_Group("Add_to_Group"),
        Skeleton_Node_Group("Remove_from_Group"),
        Skeleton_Node_Group("Copy_Group"),
        Skeleton_Node_Group("Delete_Group"),
        Skeleton_Node_Group("Rename_Group"),
        Skeleton_Node_Group("Clear_Group"),
        Skeleton_Node_Group("Query_Group"),
        Skeleton_Node_Group("Auto_Group")        
        ]


    test_set = element_set + segment_set + node_set + \
               direct_pin_set + page_pin_set + element_group + \
               segment_group + node_group
    
    logan = unittest.TextTestRunner()
    for t in test_set:
        print >> sys.stderr,  "\n *** Running test: %s\n" % t.id() 
        res = logan.run(t)
        if not res.wasSuccessful():
            return 0
    return 1


###################################################################
# The code below this line should be common to all testing files. #
###################################################################

if __name__=="__main__":
    # If directly run, then start oof, and run the local tests, then quit.
    import sys
    try:
        import oof2
        sys.path.append(os.path.dirname(oof2.__file__))
        from ooflib.common import oof
    except ImportError:
        print "OOF is not correctly installed on this system."
        sys.exit(4)
    sys.argv.append("--text")
    sys.argv.append("--quiet")
    sys.argv.append("--seed=17")
    oof.run(no_interp=1)
    
    success = run_tests()

    OOF.File.Quit()
    
    if success:
        print "All tests passed."
    else:
        print "Test failure."
