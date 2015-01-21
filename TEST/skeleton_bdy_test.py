# -*- python -*-
# $RCSfile: skeleton_bdy_test.py,v $
# $Revision: 1.12 $
# $Author: langer $
# $Date: 2008/09/08 18:30:07 $

# Test suite for skeleton boundary construction, modification, and
# deletion.  Currently only creates boundaries from selections, not
# groups.  This test should follow the more basic skeleton_test tests.

import unittest, os
import memorycheck

class Skeleton_Boundary(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        global cskeleton
        from ooflib.SWIG.engine import cskeleton
        global cmicrostructure
        from ooflib.SWIG.common import cmicrostructure
        OOF.Microstructure.Create_From_ImageFile(
            filename=os.path.join("ms_data","small.ppm"),
            microstructure_name="skeltest",
            height=20.0, width=20.0)
        OOF.Image.AutoGroup(image="skeltest:small.ppm")
        global gfxmanager
        from ooflib.common.IO import gfxmanager
        OOF.Skeleton.New(
            name="bdytest",
            microstructure="skeltest", 
            x_elements=8, y_elements=8,
            skeleton_geometry=QuadSkeleton(top_bottom_periodicity=False,
                                           left_right_periodicity=False))

        # Need a graphics window so we can do the direct selection.
        OOF.Windows.Graphics.New()
        self.sk_context = skeletoncontext.skeletonContexts[
            "skeltest:bdytest"]

    def tearDown(self):
        OOF.Graphics_1.File.Close()

    # Check that the default boundaries exist and are the right size.
    # As with most tests, this could do more, i.e. ensure edges are
    # exterior, check that indices are as expected, etc.
    @memorycheck.check("skeltest")
    def Defaults(self):
        edge_bdy_names = self.sk_context.edgeboundaries.keys()
        default_edges = ["top", "bottom", "left", "right"]
        self.assertEqual(len(edge_bdy_names), 4)
        for e in edge_bdy_names:
            self.assert_(e in default_edges)
            default_edges.remove(e)
            
        point_bdy_names = self.sk_context.pointboundaries.keys()
        default_points = ["topleft", "topright", "bottomleft", "bottomright"]
        self.assertEqual(len(point_bdy_names), 4)
        for p in point_bdy_names:
            self.assert_(p in default_points)
            default_points.remove(p)

        for e in self.sk_context.edgeboundaries.values():
            self.assertEqual(e.current_size(), 8)

        for p in self.sk_context.pointboundaries.values():
            self.assertEqual(p.current_size(), 1)


    @memorycheck.check("skeltest")
    def Construct_Edge_from_Elements(self):
        # Create bdy from selected elements
        OOF.Graphics_1.Toolbox.Select_Element.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(4.5,8.5), Point(14.0,4.0)],
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromElements(group=selection,
                                         direction="Clockwise"))
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)
        # Create bdy from element group
        OOF.ElementGroup.New_Group(skeleton='skeltest:bdytest',name='egroup')
        OOF.ElementGroup.Add_to_Group(skeleton='skeltest:bdytest',
                                      group='egroup')
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:bdytest', name='test2',
            constructor=EdgeFromElements(group='egroup',
                                         direction='Clockwise'))
        self.assert_("test2" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test2"]
        self.assertEqual(test_bdy.current_size(), 8)

    @memorycheck.check("skeltest")
    def Construct_Edge_from_Segments(self):
        # Create bdy from selected segments
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(4.5,8.5), Point(14.0,4.0)],
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(7.5,6.25)],
            shift=0, ctrl=1)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(10.0,6.25)],
            shift=0, ctrl=1)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromSegments(group=selection,
                                         direction="Clockwise"))
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)
        # Create bdy from segment group
        OOF.SegmentGroup.New_Group(skeleton='skeltest:bdytest', name="sgroup")
        OOF.SegmentGroup.Add_to_Group(skeleton='skeltest:bdytest',
                                      group='sgroup')
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test2",
            constructor=EdgeFromSegments(group='sgroup',
                                         direction="Clockwise"))
        self.assert_("test2" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test2"]
        self.assertEqual(test_bdy.current_size(), 8)

    @memorycheck.check("skeltest")
    def Construct_Edge_from_Nodes(self):
        OOF.Graphics_1.Toolbox.Select_Node.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(3.75,3.75), Point(11.25,11.25)],
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton="skeltest:bdytest",
            points=[Point(7.5,7.5)],
            shift=0, ctrl=1)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromNodes(group=selection,
                                      direction="Clockwise"))
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)
        OOF.NodeGroup.New_Group(skeleton='skeltest:bdytest', name='ngroup')
        OOF.NodeGroup.Add_to_Group(skeleton='skeltest:bdytest', group='ngroup')
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:bdytest', name='test2',
            constructor=EdgeFromNodes(group='ngroup', direction="Clockwise"))
        self.assert_("test2" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test2"]
        self.assertEqual(test_bdy.current_size(), 8)

    @memorycheck.check("skeltest")
    def Construct_Point_from_Elements(self):
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton="skeltest:bdytest",
            points=[Point(3.75,3.75)],
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=PointFromElements(group=selection))
        self.assert_("test" in self.sk_context.pointboundaries.keys())
        test_bdy = self.sk_context.pointboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 4)
        OOF.ElementGroup.New_Group(skeleton='skeltest:bdytest', name='egroup')
        OOF.ElementGroup.Add_to_Group(skeleton='skeltest:bdytest',
                                      group='egroup')
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test2",
            constructor=PointFromElements(group='egroup'))
        self.assert_("test2" in self.sk_context.pointboundaries.keys())
        test_bdy = self.sk_context.pointboundaries["test2"]
        self.assertEqual(test_bdy.current_size(), 4)


    @memorycheck.check("skeltest")
    def Construct_Point_from_Segments(self):
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(4.5,8.5), Point(14.0,4.0)],
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=PointFromSegments(group=selection))
        self.assert_("test" in self.sk_context.pointboundaries.keys())
        test_bdy = self.sk_context.pointboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)
        OOF.SegmentGroup.New_Group(skeleton='skeltest:bdytest', name='sgroup')
        OOF.SegmentGroup.Add_to_Group(skeleton='skeltest:bdytest',
                                      group='sgroup')
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test2",
            constructor=PointFromSegments(group='sgroup'))
        self.assert_("test2" in self.sk_context.pointboundaries.keys())
        test_bdy = self.sk_context.pointboundaries["test2"]
        self.assertEqual(test_bdy.current_size(), 8)
        
        
    @memorycheck.check("skeltest")
    def Construct_Point_from_Nodes(self):
        OOF.Graphics_1.Toolbox.Select_Node.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(3.75,3.75), Point(11.25,11.25)],
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=PointFromNodes(group=selection))
        self.assert_("test" in self.sk_context.pointboundaries.keys())
        test_bdy = self.sk_context.pointboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 9)
        OOF.NodeGroup.New_Group(skeleton='skeltest:bdytest', name='ngroup')
        OOF.NodeGroup.Add_to_Group(skeleton='skeltest:bdytest', group='ngroup')
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test2",
            constructor=PointFromNodes(group='ngroup'))
        self.assert_("test2" in self.sk_context.pointboundaries.keys())
        test_bdy = self.sk_context.pointboundaries["test2"]
        self.assertEqual(test_bdy.current_size(), 9)

    # For deletion, do two, one for edge and one for point.
    @memorycheck.check("skeltest")
    def Delete(self):
        OOF.Skeleton.Boundary.Delete(skeleton="skeltest:bdytest",
                                     boundary="top")
        self.assertEqual(len(self.sk_context.edgeboundaries), 3)
        self.assert_(not "top" in self.sk_context.edgeboundaries.keys())
        OOF.Skeleton.Boundary.Delete(skeleton="skeltest:bdytest",
                                     boundary="topright")
        self.assertEqual(len(self.sk_context.pointboundaries), 3)
        self.assert_(not "topright" in self.sk_context.pointboundaries.keys())

    @memorycheck.check("skeltest")
    def Rename(self):
        bdy0 = self.sk_context.edgeboundaries["top"]
        OOF.Skeleton.Boundary.Rename(skeleton="skeltest:bdytest",
                                     boundary="top", name="test")
        self.assertEqual(len(self.sk_context.edgeboundaries), 4)
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        bdy1 = self.sk_context.edgeboundaries["test"]
        self.assertEqual(id(bdy0),id(bdy1))
        
    # "Modify" does not (yet) test direction reversal for edge boundaries.
    @memorycheck.check("skeltest")
    def Modify(self):
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(3.75,3.75), Point(11.25,6.25)],
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromSegments(group=selection,
                                         direction="Left to right"))
        bdy0 = self.sk_context.edgeboundaries["test"]
        OOF.Graphics_1.Toolbox.Select_Segment.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(8.75,3.75), Point(18.75,6.25)],
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Modify(
            skeleton="skeltest:bdytest", boundary="test",
            modifier=AddSegments(group=selection))
        bdy1 = self.sk_context.edgeboundaries["test"]
        self.assertEqual(id(bdy1), id(bdy0))
        self.assertEqual(bdy1.current_size(), 5)
        OOF.Graphics_1.Toolbox.Select_Segment.Undo(
            skeleton="skeltest:bdytest")
        OOF.Skeleton.Boundary.Modify(
            skeleton="skeltest:bdytest", boundary="test",
            modifier=RemoveSegments(group=selection))
        bdy2 = self.sk_context.edgeboundaries["test"]
        self.assertEqual(id(bdy2), id(bdy0))
        self.assertEqual(bdy2.current_size(), 3)
        
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton="skeltest:bdytest",
            points=[Point(5.25,5.25)], shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test2",
            constructor=PointFromNodes(group=selection))
        bdy0 = self.sk_context.pointboundaries["test2"]
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton="skeltest:bdytest",
            points=[Point(7.25,7.25)], shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Modify(
            skeleton="skeltest:bdytest", boundary="test2",
            modifier=AddNodes(group=selection))
        bdy1 = self.sk_context.pointboundaries["test2"]
        self.assertEqual(id(bdy1),id(bdy0))
        self.assertEqual(bdy1.current_size(), 2)
        OOF.Graphics_1.Toolbox.Select_Node.Undo(
            skeleton="skeltest:bdytest")
        OOF.Skeleton.Boundary.Modify(
            skeleton="skeltest:bdytest", boundary="test2",
            modifier=RemoveNodes(group=selection))
        bdy2 = self.sk_context.pointboundaries["test2"]
        self.assertEqual(id(bdy2),id(bdy0))
        self.assertEqual(bdy2.current_size(), 1)
        
def run_tests():

    test_set = [
        Skeleton_Boundary("Defaults"),
        Skeleton_Boundary("Construct_Edge_from_Elements"),
        Skeleton_Boundary("Construct_Edge_from_Segments"),
        Skeleton_Boundary("Construct_Edge_from_Nodes"),
        Skeleton_Boundary("Construct_Point_from_Elements"),
        Skeleton_Boundary("Construct_Point_from_Segments"),
        Skeleton_Boundary("Construct_Point_from_Nodes"),
        Skeleton_Boundary("Delete"),
        Skeleton_Boundary("Rename"),
        Skeleton_Boundary("Modify")
        ]
    

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
