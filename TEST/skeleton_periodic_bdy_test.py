# -*- python -*-
# $RCSfile: skeleton_periodic_bdy_test.py,v $
# $Revision: 1.7 $
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
            skeleton_geometry=TriSkeleton(arrangement="middling",
                                          left_right_periodicity=True,
                                          top_bottom_periodicity=True))

        # Need a graphics window so we can do the direct selection.
        OOF.Windows.Graphics.New()
        graphics_name = gfxmanager.gfxManager.windows[-1].name
        self.g_window_menu = OOF.__getattr__(graphics_name)
        self.sk_context = skeletoncontext.skeletonContexts[
            "skeltest:bdytest"]

    def tearDown(self):
##        # restore default values for later tests
##        QuadSkeleton(left_right_periodicity=False,top_bottom_periodicity=False)
        self.g_window_menu.File.Close()

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
        self.g_window_menu.Toolbox.Select_Element.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(11,3), Point(19,-.5)],
            shift=0, ctrl=0)
        self.g_window_menu.Toolbox.Select_Element.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(11,17), Point(19,20.5)],
            shift=0, ctrl=1)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromElements(group=selection,
                                         direction="Clockwise"))
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)

    @memorycheck.check("skeltest")
    def Construct_Edge_from_Segments(self):
        self.g_window_menu.Toolbox.Select_Segment.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(11,3), Point(19,-.5)],
            shift=0, ctrl=0)
        self.g_window_menu.Toolbox.Select_Segment.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(11,17), Point(19,20.5)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(13.5,20)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(16.5,20)],
            shift=0, ctrl=1) 
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(13.5,0)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(16.5,0)],
            shift=0, ctrl=1) 
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(15,19)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(15,1)],
            shift=0, ctrl=1)      
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(16.25,1.25)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(13.75,1.25)],
            shift=0, ctrl=1)      
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(16.25,18.75)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(13.75,18.75)],
            shift=0, ctrl=1)       
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromSegments(group=selection,
                                         direction="Clockwise"))
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)

    @memorycheck.check("skeltest")
    def Construct_Edge_from_Nodes(self):
        self.g_window_menu.Toolbox.Select_Node.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(11,3), Point(19,-.5)],
            shift=0, ctrl=0)
        self.g_window_menu.Toolbox.Select_Node.Rectangle(
            skeleton="skeltest:bdytest",
            points=[Point(11,17), Point(19,20.5)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Node.Single_Node(
            skeleton="skeltest:bdytest",
            points=[Point(15,0)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Node.Single_Node(
            skeleton="skeltest:bdytest",
            points=[Point(15,20)],
            shift=0, ctrl=1)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromNodes(group=selection,
                                      direction="Clockwise"))
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)


    @memorycheck.check("skeltest")
    def Winding_Test(self):
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(1.25,8.75)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(3.75,6.25)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(6.25,3.75)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(8.75,1.25)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(11.25,18.75)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(13.75,16.25)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(16.25,13.75)],
            shift=0, ctrl=1)
        self.g_window_menu.Toolbox.Select_Segment.Single_Segment(
            skeleton="skeltest:bdytest",
            points=[Point(18.75,11.25)],
            shift=0, ctrl=1)
        OOF.Skeleton.Boundary.Construct(
            skeleton="skeltest:bdytest", name="test",
            constructor=EdgeFromSegments(group=selection,
                                      direction="Left to right"))
        self.assert_("test" in self.sk_context.edgeboundaries.keys())
        test_bdy = self.sk_context.edgeboundaries["test"]
        self.assertEqual(test_bdy.current_size(), 8)

        
def run_tests():

    test_set = [
        Skeleton_Boundary("Defaults"),
        Skeleton_Boundary("Construct_Edge_from_Elements"),
        Skeleton_Boundary("Construct_Edge_from_Segments"),
        Skeleton_Boundary("Construct_Edge_from_Nodes"),
        Skeleton_Boundary("Winding_Test")
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
