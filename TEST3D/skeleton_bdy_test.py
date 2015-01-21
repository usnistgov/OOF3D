# -*- python -*-
# $RCSfile: skeleton_bdy_test.py,v $
# $Revision: 1.1.2.11 $
# $Author: langer $
# $Date: 2014/12/03 19:09:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import unittest, os, sys
import memorycheck
import selection_utils

from UTILS import file_utils
file_utils.generate = False
reference_file = file_utils.reference_file

class Skeleton_Boundary(unittest.TestCase):
    def setUp(self):
        global skeletoncontext
        from ooflib.engine import skeletoncontext
        from ooflib.SWIG.engine import cskeletonselectable
        selection_utils.initialize()
        OOF.Settings.Random_Seed(seed=17)
        OOF.Windows.Graphics.New()
        OOF.Microstructure.Create_From_ImageFile(
            filenames=ThreeDImageDirectory(
                directory=reference_file('ms_data', 'bluegreen'),
                sort=NumericalOrder()),
            microstructure_name="skeltest",
            height=automatic, width=automatic, depth=automatic)
        OOF.Skeleton.New(
            name='skeleton',
            microstructure='skeltest',
            x_elements=2, y_elements=2, z_elements=2,
            skeleton_geometry=TetraSkeleton(arrangement='moderate'))
        self.skelctxt = skeletoncontext.skeletonContexts['skeltest:skeleton']

    def tearDown(self):
        OOF.Graphics_1.File.Close()

    def checkBoundaries(self, facedict=None, edgedict=None, nodedict=None,
                        complete=False):
        if facedict is not None:
            real_faces = self.skelctxt.faceboundaries.keys()
            if complete:
                self.assertEqual(sorted(facedict.keys()), sorted(real_faces))
            else:
                self.assert_(all(f in real_faces for f in facedict))
            for bdyname, faces in facedict.items():
                OOF.FaceSelection.Select_Named_Boundary(
                    skeleton='skeltest:skeleton',
                    boundary = bdyname)
                self.assertEqual(
                    selection_utils.selectedFaceIDs(self.skelctxt), faces)

        if edgedict is not None:
            real_edges = self.skelctxt.edgeboundaries.keys()
            if complete:
                self.assertEqual(sorted(edgedict.keys()), sorted(real_edges))
            else:
                self.assert_(all(e in real_edges for e in edgedict))
            for bdyname, edges in edgedict.items():
                OOF.SegmentSelection.Select_Named_Boundary(
                    skeleton='skeltest:skeleton',
                    boundary=bdyname)
                self.assertEqual(
                    selection_utils.selectedSegmentIDs(self.skelctxt), edges)

        if nodedict is not None:
            real_points = self.skelctxt.pointboundaries.keys()
            if complete:
                self.assertEqual(sorted(nodedict.keys()), sorted(real_points))
            else:
                self.assert_(all(n in real_points for n in nodedict))
            for bdyname, points in nodedict.items():
                OOF.NodeSelection.Select_Named_Boundary(
                    skeleton='skeltest:skeleton',
                    boundary=bdyname)
                self.assertEqual(
                    selection_utils.selectedNodeIDs(self.skelctxt), points)

    # Check the order of the nodes in an edge boundary
    def checkNodeOrder(self, bdyname, indices):
        bdy = self.skelctxt.edgeboundaries[bdyname].current_boundary()
        nodes = bdy.getNodes()
        self.assertEqual([n.getIndex() for n in nodes], indices)
        
    # Check the orientation of the faces in a face boundary.
    # facenodes is a dictionary mapping face ids to tuples of node
    # ids.  If the face is misoriented, the node ids will be in the
    # wrong order.
    def checkFaceOrientations(self, bdyname, facenodes):
        bdy = self.skelctxt.faceboundaries[bdyname].current_boundary()
        faces = bdy.getFaces()
        actualfacenodes = {}
        for oface in faces:
            face = oface.get_face() # CSkeletonFace oface is an
            # OrientedCSkeletonFace, and its getNode() takes the
            # orientation into account.  Using CyclicList ensures that
            # irrelevant cyclic permutations of the nodes in facenodes
            # don't break the test.
            actualNodes = selection_utils.CyclicList(
                [oface.getNode(i).getIndex() for i in range(3)])
            actualfacenodes[selection_utils.offsetFaceID(face)] = actualNodes
        self.assertEqual(facenodes, actualfacenodes)
            

    #=--=##=--=##=--=##=--=#

    # Select the nodes at x=0,5,10; y=5; z=10
    def selectThreeNodes(self, shift=0):
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(2.4725,5.03027,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=shift, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.98487,4.94955,21.9826)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(7.49723,5,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)

    # Select the nodes at x=0,5,10; y=10, z=10
    def selectThreeTopNodes(self, shift=0):
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(2.34052,7.63273,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=shift, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(5.01605,7.63273,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(7.67018,7.64343,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)

    # Select the nodes at x=0,5,10; y=0, z=10
    def selectThreeBottomNodes(self):
        OOF.SegmentSelection.Select_Named_Boundary(
            skeleton='skeltest:skeleton', boundary='YminZmax')
        OOF.NodeSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        OOF.SegmentSelection.Clear(skeleton='skeltest:skeleton')

    def selectThreeSegments(self):
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(3.97588,4.98991,21.9826)], 
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(4.99496,4.6065,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652), 
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.9434,2.66926,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
    
    def selectThreeFaces(self):
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(-13.118,18.4998,23.4669)],
            view=View(cameraPosition=Coord(-13.165,18.5331,23.5186), 
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.202236,0.874558,-0.440737), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-13.1157,18.5031,23.4668)],
            view=View(cameraPosition=Coord(-13.165,18.5331,23.5186),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.202236,0.874558,-0.440737), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-13.1227,18.4971,23.4643)],
            view=View(cameraPosition=Coord(-13.165,18.5331,23.5186), 
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.202236,0.874558,-0.440737), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)

    def selectOneElement(self):
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(3.58238,6.92715,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652), 
            shift=0, ctrl=0)

    def selectThreeElements(self):
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(3.58238,6.92715,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652), 
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(4.36939,6.36212,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton', 
            points=[Point(5.7416,6.24105,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)

    #=--=##=--=##=--=##=--=#

    # keys are the boundary names, values are the uids of the
    # objects that make up the boundary.
    original_faces = {
        "Xmax" :[112, 128, 138, 151, 219, 235, 251, 259],
        "Ymin" : [36, 64, 75, 95, 103, 127, 139, 154], 
        "Ymax" : [169, 181, 202, 208, 224, 233, 250, 256], 
        "Zmin" : [55, 62, 118, 126, 179, 185, 234, 238], 
        "Zmax" : [76, 86, 140, 146, 194, 204, 243, 253], 
        "Xmin" : [44, 63, 73, 89, 160, 178, 201, 212]
        }
    original_edges = {
        'XminYmax' : [174, 199],
        'XminZmin' : [60, 176],
        'XminYmin' : [59, 70],
        'XmaxYmin' : [123, 136],
        'YmaxZmax' : [197, 245], 
        'XminZmax' : [67, 196],
        'XmaxYmax' : [228, 248],
        'YmaxZmin' : [175, 231], 
        'XmaxZmin' : [122, 229],
        'YminZmax' : [69, 133], 
        'YminZmin' : [58, 124], 
        'XmaxZmax' : [132, 246]
        }
    original_nodes = {
        'XminYminZmax' : [2],
        'XmaxYminZmax' : [8],
        'XmaxYmaxZmax' : [26], 
        'XminYmaxZmin' : [18], 
        'XmaxYmaxZmin' : [24], 
        'XminYmaxZmax' : [20], 
        'XminYminZmin' : [0],
        'XmaxYminZmin' : [6]}
    
    original_edge_nodes = {
        'XminYmax' : [18, 19, 20],
        'XminZmin' : [0, 9, 18],
        'XminYmin' : [0, 1, 2],
        'XmaxYmin' : [6, 7, 8],
        'YmaxZmax' : [20, 23, 26],
        'XminZmax' : [2, 11, 20],
        'XmaxYmax' : [24, 25, 26],
        'YmaxZmin' : [18, 21, 24],
        'XmaxZmin' : [6, 15, 24],
        'YminZmax' : [2, 5, 8],
        'YminZmin' : [0, 3, 6],
        'XmaxZmax' : [8, 17, 26]}

    #=--=##=--=##=--=#

    # Check that the default boundaries exist and contain the correct
    # entities.  This is also the test for the Select_Named_Boundary
    # commands.
    @memorycheck.check("skeltest")
    def Defaults(self):
        self.checkBoundaries(self.original_faces, self.original_edges,
                             self.original_nodes, complete=True)
        for bdyname, nodes in self.original_edge_nodes.items():
            self.checkNodeOrder(bdyname, nodes)

    @memorycheck.check("skeltest")
    def ConstructPointFromNodes(self):
        self.selectThreeNodes()
        # Make a boundary
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=PointFromNodes(group=selection))
        self.checkBoundaries(nodedict={'boundary' : [11, 14, 17]})

    @memorycheck.check("skeltest")
    def ConstructPointFromNodeGroup(self):
        self.selectThreeNodes()
        OOF.NodeGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='group')
        OOF.NodeGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='group')
        OOF.NodeSelection.Clear(
            skeleton='skeltest:skeleton')
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=PointFromNodes(group='group'))
        self.checkBoundaries(nodedict={'boundary' : [11, 14, 17]})

    @memorycheck.check("skeltest")
    def ConstructPointFromSegments(self):
        self.selectThreeSegments()
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary', 
            constructor=PointFromSegments(group=selection))
        self.checkBoundaries(nodedict={'boundary' : [5, 7, 11, 14]})

    @memorycheck.check("skeltest")
    def ConstructPointFromFaces(self):
        self.selectThreeFaces()
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=PointFromFaces(group=selection))
        self.checkBoundaries(nodedict={'boundary' : [10, 11, 19, 20, 23]})

    @memorycheck.check("skeltest")
    def ConstructPointFromElements(self):
        # Select all but one corner element, by selecting the corner
        # and inverting.  This is an easy way to select a nontrivial
        # group of elements with an internal node.
        self.selectOneElement()
        OOF.ElementSelection.Invert(skeleton='skeltest:skeleton')
        # Create a point boundary from all nodes
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='all',
            constructor=PointFromElements(group=selection,coverage='All'))
        self.checkBoundaries(
            nodedict={'all' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                               14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 26]
                  })
        # Create a point boundary from the exterior nodes only
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='exterior',
            constructor=PointFromElements(group=selection,coverage='Exterior'))
        self.checkBoundaries(
            nodedict={'exterior' : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                    14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25,
                                    26]})
        # Create a point boundary from the internior nodes only
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='interior',
            constructor=PointFromElements(group=selection,coverage='Interior'))
        self.checkBoundaries(nodedict={'interior' : [13]})

    @memorycheck.check("skeltest")
    def ConstructEdgeFromSegments(self):
        self.selectThreeSegments()
        # The first and last nodes differ in x, y, and z, so we can
        # check all six directions with one set of initial segments.
        # +X to -X.
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='rl',
            constructor=EdgeFromSegments(group=selection,
                                         direction='+X to -X'))
        self.checkBoundaries(edgedict={"rl" : [78, 79, 134]})
        self.checkNodeOrder("rl", [7, 5, 14, 11])
        # -X to +X
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='lr',
            constructor=EdgeFromSegments(group=selection,
                                         direction='-X to +X'))
        self.checkBoundaries(edgedict={"lr" : [78, 79, 134]})
        self.checkNodeOrder("lr", [11, 14, 5, 7])
        # +Y to -Y
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='tb',
            constructor=EdgeFromSegments(group=selection,
                                         direction='+Y to -Y'))
        self.checkBoundaries(edgedict={"tb" : [78, 79, 134]})
        self.checkNodeOrder("tb", [11, 14, 5, 7])
        # -Y to +Y
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='bt',
            constructor=EdgeFromSegments(group=selection,
                                         direction='-Y to +Y'))
        self.checkBoundaries(edgedict={"bt" : [78, 79, 134]})
        self.checkNodeOrder("bt", [7, 5, 14, 11])
        # +Z to -Z
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='fb',
            constructor=EdgeFromSegments(group=selection,
                                         direction='+Z to -Z'))
        self.checkBoundaries(edgedict={"fb" : [78, 79, 134]})
        self.checkNodeOrder("fb", [11, 14, 5, 7])
        # -Z to +Z
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='bf',
            constructor=EdgeFromSegments(group=selection,
                                         direction='-Z to +Z'))
        self.checkBoundaries(edgedict={"bf" : [78, 79, 134]})
        self.checkNodeOrder("bf", [7, 5, 14, 11])
        
        # Counterclockwise and clockwise don't work.
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton', 
            name='dummy', 
            constructor=EdgeFromSegments(group=selection,
                                         direction='Counterclockwise-x'))
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton', 
            name='dummy', 
            constructor=EdgeFromSegments(group=selection,
                                         direction='Clockwise-y'))
    
    @memorycheck.check("skeltest")
    def ConstructEdgeLoopFromSegments(self):
        self.selectThreeSegments()
        # Select three more segments, to make a closed loop.
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton', 
            points=[Point(5.55846,2.94406,22.2326)], 
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(4.34269,2.94406,22.2326)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652), 
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(2.83039,3.46793,22.2326)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton', 
            name='ccw', 
            constructor=EdgeFromSegments(group=selection,
                                         direction='Counterclockwise-z'))
        self.checkBoundaries(edgedict={"ccw" : [30, 71, 78, 79, 100, 134]})
        self.checkNodeOrder("ccw", [1, 4, 7, 5, 14, 11])
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton', 
            name='cw', 
            constructor=EdgeFromSegments(group=selection,
                                         direction='Clockwise-z'))
        self.checkBoundaries(edgedict={"cw" : [30, 71, 78, 79, 100, 134]})
        self.checkNodeOrder("cw", [1, 11, 14, 5, 7, 4])
        ## TODO 3.0: Test other projection directions
        
    @memorycheck.check("skeltest")
    def ConstructEdgeFromNodes(self):
        self.selectThreeTopNodes()
        # -X to +X, through three colinear nodes.
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary1',
            constructor=EdgeFromNodes(group=selection,
                                      direction='-X to +X'))
        self.checkBoundaries(edgedict={'boundary1' : [197, 245]})
        self.checkNodeOrder("boundary1", [20, 23, 26])
        # The other direction
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary2',
            constructor=EdgeFromNodes(group=selection,
                                      direction='+X to -X'))
        self.checkBoundaries(edgedict={'boundary2' : [197, 245]})
        self.checkNodeOrder("boundary2", [26, 23, 20])

        # Add another node (10, 5, 10) which makes the sequence ambiguous
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(7.68089,4.9786,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary3', 
            constructor=EdgeFromNodes(group=selection,direction=
                                      '-X to +X'))
        # Add another (10, 0, 10) to to resolve the ambiguity
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(7.68089,2.33517,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary3', 
            constructor=EdgeFromNodes(group=selection,
                                      direction='-X to +X'))
        self.checkBoundaries(edgedict={'boundary3' : [132, 197, 245, 246]})
        self.checkNodeOrder("boundary3", [20, 23, 26, 17, 8])
        # Repeat bottom to top instead of left to right
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary4', 
            constructor=EdgeFromNodes(group=selection,
                                      direction='-Y to +Y'))
        self.checkBoundaries(edgedict={'boundary4' : [132, 197, 245, 246]})
        self.checkNodeOrder("boundary4", [8, 17, 26, 23, 20])
        # Add a point (0, 0, 0) that can't be connected
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(3.10037,3.10572,21.2376)], 
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary5', 
            constructor=EdgeFromNodes(group=selection,direction=
                                      '-X to +X'))

    @memorycheck.check("skeltest")
    def ConstructEdgeLoopFromNodes(self):
        # Select all the nodes on the edges of the front face
        self.selectThreeBottomNodes()
        self.selectThreeTopNodes(shift=1)
        self.selectThreeNodes(shift=1)
        # but not the middle one
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton', 
            points=[Point(5.01513,4.98991,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=1)
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton', name='boundary',
            constructor=EdgeFromNodes(group=selection,
                                      direction='Clockwise-z'))
        self.checkBoundaries(edgedict={'boundary' : 
                                       [67, 69, 132, 133, 196, 197, 245, 246]})
        self.checkNodeOrder('boundary', [2, 11, 20, 23, 26, 17, 8, 5])
        # Select the middle node of the face, making the set unsequenceable.
        OOF.Graphics_1.Toolbox.Select_Node.Single_Node(
            skeleton='skeltest:skeleton',
            points=[Point(4.98517,5,22.2326)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary', 
            constructor=EdgeFromNodes(group=selection,
                                      direction='Clockwise-z'))
        ## TODO 3.0: Test other projection directions and chiralities

    @memorycheck.check("skeltest")
    def ConstructEdgeLoopFromFaces(self):
        self.selectThreeFaces()
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=EdgeFromFaces(group=selection,
                                      direction='Counterclockwise-x'))
        self.checkBoundaries(edgedict={'boundary':
                                       [88, 157, 196, 197, 200]})
        self.checkNodeOrder('boundary', [11, 10, 19, 23, 20])
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='b2',
            constructor=EdgeFromFaces(group=selection,
                                      direction='Clockwise-x'))
        self.checkBoundaries(edgedict={'b2':
                                       [88, 157, 196, 197, 200]})
        self.checkNodeOrder('b2', [11, 20, 23, 19, 10])

    @memorycheck.check("skeltest")
    def ConstructFaceFromFaces(self):
        # Select faces that don't form a closed surface and create a
        # face boundary from them.
        self.selectThreeFaces()
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary', 
            constructor=FaceFromFaces(group=selection,
                                      direction='-X to +X'))
        self.checkBoundaries(facedict={'boundary': [201, 202, 212]})
        self.checkFaceOrientations('boundary', {201: [11, 19, 20],
                                                202: [23, 20, 19],
                                                212: [19, 11, 10]})
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='b2', 
            constructor=FaceFromFaces(group=selection,
                                      direction='+X to -X'))
        self.checkBoundaries(facedict={'b2': [201, 202, 212]})
        self.checkFaceOrientations('b2', {201: [20, 19, 11],
                                          202: [19, 20, 23],
                                          212: [10, 11, 19]})
    @memorycheck.check("skeltest")
    def ConstructFaceFromFaces2(self):
        # Select faces that form a closed surface and create a face
        # boundary from them.
        self.selectOneElement()
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='b1',
            constructor=FaceFromFaces(group=selection,direction='Outward'))
        self.checkBoundaries(facedict={'b1' : [201, 202, 203, 204]})
        self.checkFaceOrientations('b1', {201: [11, 20, 19],
                                          202: [19, 20, 23],
                                          203: [11, 19, 23],
                                          204: [11, 23, 20]})
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='b2',
            constructor=FaceFromFaces(group=selection,direction='Inward'))
        self.checkBoundaries(facedict={'b2' : [201, 202, 203, 204]})
        self.checkFaceOrientations('b2', {201: [20, 11, 19],
                                          202: [20, 19, 23],
                                          203: [19, 11, 23],
                                          204: [23, 11, 20]})
    @memorycheck.check("skeltest")
    def FailFaceFromFaces(self):
        self.selectThreeFaces()
        # Select a face that shares a node, but not an edge, with the
        # previously selected faces.
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(6.10767,5.33177,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=FaceFromFaces(
                group=selection,
                direction='-X to +X'))

        # Select the faces surrounding an element, plus one more.
        self.selectOneElement()
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(6.10767,5.33177,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583), 
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=FaceFromFaces(
                group=selection,
                direction='Inward'))

        # Select an orientable set of faces, but try to construct a
        # boundary with the wrong type of direction.  

        # Closed boundary with an open direction:
        OOF.FaceSelection.Select_from_Selected_Elements(
            skeleton='skeltest:skeleton',
            coverage='Exterior')
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=FaceFromFaces(
                group=selection,
                direction='-X to +X'))
        # Open boundary with a closed direction:
        self.selectThreeFaces()
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=FaceFromFaces(
                group=selection,
                direction='Inward'))

        # Check that none of the above tests actually created a new
        # boundary.
        self.checkBoundaries(self.original_faces, self.original_edges,
                             self.original_nodes, complete=True)

    @memorycheck.check("skeltest")
    def Moebius(self):
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-21.8765,5.55065,16.3917)],
            view=View(cameraPosition=Coord(-21.9309,5.54845,16.4225),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.00575824,0.999391,-0.0344091), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 5.0, 0]], invertClip=0,
                      size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-21.8755,5.55297,16.394)],
            view=View(cameraPosition=Coord(-21.9309,5.54845,16.4225),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.00575824,0.999391,-0.0344091), angle=30,
                      clipPlanes=[[1.0, 0.0, 0.0, 5.0, 0]], invertClip=0,
                      size_x=691, size_y=652), 
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-1.60049,26.4027,-13.715)],
            view=View(cameraPosition=Coord(-1.62947,26.4521,-13.7591),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.961381,0.273945,-0.02648), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-1.60442,26.404,-13.7122)],
            view=View(cameraPosition=Coord(-1.62947,26.4521,-13.7591),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.961381,0.273945,-0.02648), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-1.61163,26.3972,-13.7174)],
            view=View(cameraPosition=Coord(-1.62947,26.4521,-13.7591),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.961381,0.273945,-0.02648), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-1.61675,26.3969,-13.7158)],
            view=View(cameraPosition=Coord(-1.62947,26.4521,-13.7591),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.961381,0.273945,-0.02648), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-23.7214,9.41775,7.86405)],
            view=View(cameraPosition=Coord(-23.7789,9.41921,7.88042),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.135776,0.979819,-0.146694), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-23.7214,9.41421,7.86921)],
            view=View(cameraPosition=Coord(-23.7789,9.41921,7.88042),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.135776,0.979819,-0.146694), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-23.7209,9.41194,7.87735)],
            view=View(cameraPosition=Coord(-23.7789,9.41921,7.88042),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.135776,0.979819,-0.146694), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(-23.7197,9.41707,7.88126)],
            view=View(cameraPosition=Coord(-23.7789,9.41921,7.88042),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.135776,0.979819,-0.146694), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(2.82905,8.23523,22.9884)],
            view=View(cameraPosition=Coord(4.19942,7.51999,34.1386),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.112517,0.990215,-0.0825451), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(3.86972,7.38555,23.0905)],
            view=View(cameraPosition=Coord(4.19942,7.51999,34.1386),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.112517,0.990215,-0.0825451), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.07639,7.11611,23.1469)],
            view=View(cameraPosition=Coord(4.19942,7.51999,34.1386),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.112517,0.990215,-0.0825451), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(5.93782,7.89159,23.1035)],
            view=View(cameraPosition=Coord(4.19942,7.51999,34.1386),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.112517,0.990215,-0.0825451), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(24.1008,5.03397,6.28131)],
            view=View(cameraPosition=Coord(34.1342,2.3668,4.43828),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.0850631,0.979783,-0.18108), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(24.025,4.36682,5.47844)],
            view=View(cameraPosition=Coord(34.1342,2.3668,4.43828),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.0850631,0.979783,-0.18108), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(23.9671,4.01208,4.13759)],
            view=View(cameraPosition=Coord(34.1342,2.3668,4.43828),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.0850631,0.979783,-0.18108), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(24.003,4.60091,3.23981)],
            view=View(cameraPosition=Coord(34.1342,2.3668,4.43828),
                      focalPoint=Coord(5,5,5),
                      up=Coord(0.0850631,0.979783,-0.18108), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)

        OOF.FaceGroup.New_Group(
            skeleton='skeltest:skeleton',
            name='moebius')
        OOF.FaceGroup.Add_to_Group(
            skeleton='skeltest:skeleton',
            group='moebius')

        # Try to create an oriented boundary, and fail.
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=FaceFromFaces(
                group=selection,
                direction='Inward'))
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=FaceFromFaces(
                group=selection,
                direction='-X to +X'))

        # Check that the above tests didn't actually create a new
        # boundary.
        self.checkBoundaries(self.original_faces, self.original_edges,
                             self.original_nodes, complete=True)

        # checkBoundaries changed the selection.  Reselect the moebius strip.
        OOF.FaceSelection.Select_Group(
            skeleton='skeltest:skeleton',
            group='moebius')

        # Deselecting one of the faces should make the surface
        # orientable, and boundary creation should work.
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton', 
            points=[Point(5.67654,15.7085,24.6481)],
            view=View(cameraPosition=Coord(5.5354,19.6928,30.296), 
                      focalPoint=Coord(5,5,5),
                      up=Coord(-0.167783,0.853998,-0.49248), angle=30, 
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=1)
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary', 
            constructor=FaceFromFaces(
                group=selection,
                direction='-X to +X'))
        self.checkBoundaries(
            facedict={
                'boundary' : 
                [160, 170, 178, 179, 185, 186, 194, 201, 204, 212, 219, 224,
                 233, 235, 251, 253, 259]})

    @memorycheck.check("skeltest")
    def ConstructFaceFromElements(self):
        # Build a boundary from the faces of a single element in the
        # corner of the skeleton.
        self.selectOneElement()
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary',
            constructor=FaceFromElements(
                group=selection,
                direction='Outward'))
        self.checkBoundaries(facedict={'boundary' : [201, 202, 203, 204]})
        self.checkFaceOrientations('boundary', {201: [11, 20, 19],
                                                202: [19, 20, 23],
                                                203: [11, 19, 23],
                                                204: [11, 23, 20]})
        # Do it again with the opposite orientation.
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary2',
            constructor=FaceFromElements(
                group=selection,
                direction='Inward'))
        self.checkBoundaries(facedict={'boundary2' : [201, 202, 203, 204]})
        self.checkFaceOrientations('boundary2', {201: [20, 11, 19],
                                                 202: [20, 19, 23],
                                                 203: [19, 11, 23],
                                                 204: [23, 11, 20]})
        # Try to do it with an illegal orientation.
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundarynot',
            constructor=FaceFromElements(
                group=selection,
                direction='-X to +X'))

        # Select a second adjacent element.
        OOF.ElementSelection.Expand(
            skeleton='skeltest:skeleton',
            mode='Faces')

        # Create a boundary.
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary3',
            constructor=FaceFromElements(
                group=selection,
                direction='Outward'))
        self.checkBoundaries(
            facedict={'boundary3' :[192, 201, 202, 204, 207, 211]})
        self.checkFaceOrientations('boundary3', { 192: [11, 13, 23],
                                                  201: [11, 20, 19],
                                                  202: [19, 20, 23],
                                                  204: [11, 23, 20],
                                                  207: [13, 19, 23],
                                                  211: [11, 19, 13]})
        # Select a third non-adjacent element.
        OOF.Graphics_1.Toolbox.Select_Element.Single_Element(
            skeleton='skeltest:skeleton',
            points=[Point(-14.3998,-16.685,2.5804)],
            view=View(cameraPosition=Coord(-14.432,-16.7396,2.5839),
                      focalPoint=Coord(5,5,5),
                      up=Coord(-0.738119,0.634189,0.230185), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundarynot',
            constructor=FaceFromElements(
                group=selection,
                direction='Outward'))
                

    @memorycheck.check("skeltest")
    def Delete(self):
        # Delete one of each type of boundary.
        OOF.Skeleton.Boundary.Delete(
            skeleton='skeltest:skeleton', boundary='Xmax')
        OOF.Skeleton.Boundary.Delete(
            skeleton='skeltest:skeleton', boundary='XmaxYmax')
        OOF.Skeleton.Boundary.Delete(
            skeleton='skeltest:skeleton', boundary='XmaxYmaxZmin')
        # Delete them from the reference dicts.
        faces = self.original_faces.copy()
        del faces['Xmax']
        edges = self.original_edges.copy()
        del edges['XmaxYmax']
        nodes = self.original_nodes.copy()
        del nodes['XmaxYmaxZmin']
        # Compare actual boundaries to the reference lists.
        self.checkBoundaries(faces, edges, nodes, complete=True)
    
    @memorycheck.check("skeltest")
    def Rename(self):
        # Rename one boundary of each type.
        OOF.Skeleton.Boundary.Rename(
            skeleton='skeltest:skeleton',
            boundary='Xmax',
            name='write')
        OOF.Skeleton.Boundary.Rename(
            skeleton='skeltest:skeleton',
            boundary='XmaxYmax',
            name='topwrite')
        OOF.Skeleton.Boundary.Rename(
            skeleton='skeltest:skeleton',
            boundary='XmaxYminZmin',
            name='berightback')
        # Modify the reference lists.
        faces = self.original_faces.copy()
        faces['write'] = faces['Xmax']
        del faces['Xmax']
        edges = self.original_edges.copy()
        edges['topwrite'] = edges['XmaxYmax']
        del edges['XmaxYmax']
        nodes = self.original_nodes.copy()
        nodes['berightback'] = nodes['XmaxYminZmin']
        del nodes['XmaxYminZmin']
        # Compare actual boundaries with the reference lists.
        self.checkBoundaries(faces, edges, nodes, complete=True)
        # Delete a renamed boundary
        OOF.Skeleton.Boundary.Delete(
            skeleton='skeltest:skeleton',
            boundary='berightback')
        del nodes['berightback']
        self.checkBoundaries(faces, edges, nodes, complete=True)

    @memorycheck.check("skeltest")
    def RemoveSegments(self):
        # Remove a single segment from an edge boundary.
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(7.51741,6.85652,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Modify(
            skeleton='skeltest:skeleton',
            boundary='XmaxZmax',
            modifier=RemoveSegments(group=selection))
        self.checkBoundaries(edgedict={"XmaxZmax":[132]})
        self.checkNodeOrder('XmaxZmax', [8, 17])
        # Try to remove the selected segment from a boundary that it's
        # not part of.
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(7.51741,6.85652,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Modify(
            skeleton='skeltest:skeleton',
            boundary='XminZmax',
            modifier=RemoveSegments(group=selection))
        self.checkBoundaries(edgedict={'XminZmax':[67, 196]})
        self.checkNodeOrder('XminZmax', [2, 11, 20])
        # Select two segments, and remove them from a boundary that
        # contains only one of them.
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.98376,7.52245,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.9434,7.35092,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Skeleton.Boundary.Modify( 
            skeleton='skeltest:skeleton',
            boundary='YmaxZmax',
            modifier=RemoveSegments(group=selection))
        self.checkBoundaries(edgedict={'YmaxZmax':[197]})
        self.checkNodeOrder('YmaxZmax', [20, 23])

        ## TODO 3.1: This doesn't work because the commands for boundary
        ## modification don't do enough topology checking.  The GUI
        ## does, but the scriptable commands don't.  If the commands
        ## are fixed, reinstall these tests (and make them check for
        ## exceptions).
        # # Create a boundary with three segments in it, and try to
        # # remove the middle one.
        # OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
        #     skeleton='skeltest:skeleton',
        #     points=[Point(6.24609,6.77581,21.9826)],
        #     view=View(cameraPosition=Coord(5,5,34.2583),
        #               focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
        #               clipPlanes=[], invertClip=0, size_x=691, size_y=652),
        #     shift=0, ctrl=0)
        # OOF.Skeleton.Boundary.Modify( 
        #     skeleton='skeltest:skeleton',
        #     boundary='XmaxZmin',
        #     modifier=AddSegments(group=selection))
        # OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
        #     skeleton='skeltest:skeleton',
        #     points=[Point(6.79094,6.1906,21.9826)],
        #     view=View(cameraPosition=Coord(5,5,34.2583),
        #               focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
        #               clipPlanes=[], invertClip=0, size_x=691, size_y=652),
        #     shift=0, ctrl=0)
        # OOF.Skeleton.Boundary.Modify( 
        #     skeleton='skeltest:skeleton',
        #     boundary='XmaxZmin',
        #     modifier=RemoveSegments(group=selection))


    @memorycheck.check("skeltest")
    def RemoveFaces(self):
        # Select a single face and remove it from a boundary.
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(6.59923,3.15357,21.9826)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Skeleton.Boundary.Modify( 
            skeleton='skeltest:skeleton',
            boundary='Zmax', 
            modifier=RemoveFaces(group=selection))
        self.checkBoundaries(
            facedict={'Zmax': [76, 86, 146, 194, 204, 243, 253]})
        self.checkFaceOrientations('Zmax', {
            76 : [2, 5, 11],
            86 : [11, 5, 14],
            146 : [14, 5, 17],
            194 : [11, 14, 23],
            204 : [20, 11, 23],
            243 : [14, 17, 23],
            253 : [17, 26, 23]})
        # Try to remove the selected face from a boundary that it's
        # not part of.
        OOF.Skeleton.Boundary.Modify( 
            skeleton='skeltest:skeleton',
            boundary='Xmax', 
            modifier=RemoveFaces(group=selection))
        self.checkBoundaries(
            facedict={"Xmax" :[112, 128, 138, 151, 219, 235, 251, 259],})
        # Select two faces, and remove them from a boundary that
        # contains only one of them.
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(16.492,6.04252,23.962)],
            view=View(cameraPosition=Coord(20.0692,5,30.0793),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(16.9513,5.95516,23.686)],
            view=View(cameraPosition=Coord(20.0692,5,30.0793),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Skeleton.Boundary.Modify(
            skeleton='skeltest:skeleton',
            boundary='Zmax', 
            modifier=RemoveFaces(group=selection))
        self.checkBoundaries(
            facedict={'Zmax': [76, 86, 146, 194, 204, 243]})
        
    @memorycheck.check("skeltest")
    def ReverseSegments(self):
        OOF.Skeleton.Boundary.Modify(
            skeleton='skeltest:skeleton',
            boundary='XmaxZmax', 
            modifier=ReverseBoundary())
        self.checkBoundaries(
            edgedict={'XmaxZmax' : [132, 246]})
        self.checkNodeOrder('XmaxZmax', [26, 17, 8])

    @memorycheck.check("skeltest")
    def ReverseFaces(self):
        OOF.Skeleton.Boundary.Modify(
            skeleton='skeltest:skeleton',
            boundary='Zmax',
            modifier=ReverseBoundary())
        self.checkBoundaries(
            facedict={'Zmax' : [76, 86, 140, 146, 194, 204, 243, 253]})
        self.checkFaceOrientations('Zmax', {
            76 : [5, 2, 11],
            86 : [5, 11, 14],
            140 : [8, 5, 17],
            146 : [5, 14, 17],
            194 : [14, 11, 23],
            204 : [11, 20, 23],
            243 : [17, 14, 23],
            253 : [26, 17, 23]})

    # Check that the default boundaries behave correctly when the
    # Skeleton is refined.  This tests the forward propagation of
    # boundary definitions in the skeleton stack.
    @memorycheck.check("skeltest")
    def RefinedDefaults(self):
        dflt_faces = {
            "Xmax" : [
                390, 400, 410, 429, 608, 618, 628, 637, 1200, 1206, 1212,
                1226, 1423, 1429, 1439, 1453, 1480, 1486, 1492, 1505, 1864,
                1872, 1881, 1889, 1960, 1964, 1966, 1972, 2259, 2269, 2275, 2283
                ],
            "Xmin" : [
                316, 326, 346, 353, 664, 674, 692, 699, 798, 809, 815, 823,
                851, 861, 880, 887, 975, 995, 1005, 1014, 1297, 1304, 1314,
                1320, 2065, 2068, 2072, 2077, 2176, 2183, 2195, 2201],
            "Ymax" : [
                456, 466, 485, 492, 667, 677, 686, 704, 862, 872, 881, 889,
                1427, 1437, 1443, 1451, 1853, 1863, 1880, 1887, 1920, 1927,
                1932, 1940, 2029, 2036, 2039, 2045, 2100, 2103, 2108, 2118],
            "Ymin" : [
                389, 409, 419, 428, 734, 744, 754, 772, 916, 927, 935, 944,
                976, 986, 996, 1015, 1344, 1353, 1358, 1366, 1717, 1721, 1723,
                1730, 2178, 2190, 2196, 2204, 2254, 2270, 2276, 2284],
            "Zmax" : [
                854, 864, 874, 892, 1569, 1579, 1585, 1599, 1750, 1756, 1762,
                1772, 1797, 1807, 1813, 1827, 1856, 1866, 1874, 1892, 2137,
                2140, 2143, 2150, 2179, 2185, 2191, 2205, 2255, 2261, 2271,
                2285],
            "Zmin" : [398, 408, 418, 427, 675, 684, 693, 701, 984, 994, 1004,
                      1013, 1096, 1106, 1112, 1120, 1149, 1154, 1161, 1169,
                      1248, 1259, 1266, 1275, 1422, 1438, 1444, 1452, 1528,
                      1532, 1536, 1544],
            }
        dflt_edges = {
            'XminYmax' : [660, 668, 859, 878],
            'XminZmin' : [672, 690, 992, 1002],
            'XminYmin' : [969, 989, 2173, 2194],
            'XmaxYmin' : [383, 403, 2267, 2274],
            'YmaxZmax' : [856, 866, 1848, 1857],
            'XminZmax' : [846, 855, 2170, 2180],
            'XmaxYmax' : [1424, 1431, 1861, 1879],
            'YmaxZmin' : [669, 679, 1435, 1442],
            'XmaxZmin' : [392, 402, 1419, 1432],
            'YminZmax' : [2172, 2187, 2251, 2264],
            'YminZmin' : [406, 416, 978, 988],
            'XmaxZmax' : [1858, 1868, 2256, 2263]
            }
        dflt_nodes = {
            'XminYminZmax' : [2],
            'XmaxYminZmax' : [8],
            'XmaxYmaxZmax' : [26], 
            'XminYmaxZmin' : [18], 
            'XmaxYmaxZmin' : [24], 
            'XminYmaxZmax' : [20], 
            'XminYminZmin' : [0],
            'XmaxYminZmin' : [6]}

        
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckAllElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))

        self.checkBoundaries(dflt_faces, dflt_edges, dflt_nodes, complete=True)

        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        self.checkBoundaries(self.original_faces, self.original_edges,
                             self.original_nodes,
                             complete=True)

        
    # Check that a boundaries created on a modified skeleton are
    # correctly defined in the original skeleton.
    @memorycheck.check("skeltest")
    def BackPropagate(self):
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckAllElements(),
                            criterion=Unconditionally(),
                            alpha=0.3))
        # Create a new point boundary on the refined skeleton,
        # consisting of the five nodes on the top front edge.
        OOF.SegmentSelection.Select_Named_Boundary(
            skeleton='skeltest:skeleton',
            boundary='YmaxZmax')
        OOF.NodeSelection.Select_from_Selected_Segments(
            skeleton='skeltest:skeleton')
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='ptbdy',
            constructor=PointFromNodes(group=selection))
        self.checkBoundaries(nodedict={'ptbdy': [20, 23, 26, 68, 105,]})

        # Create a new edge boundary, including the equivalents of
        # some complete and some incomplete unrefined segments.
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(2.31911,4.30436,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(2.46894,5.16053,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(4.57727,7.29026,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(5.41203,7.27956,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(6.80331,5.86687,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(
            skeleton='skeltest:skeleton',
            points=[Point(7.67018,4.44349,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='edgebdy',
            constructor=EdgeFromSegments(group=selection,
                                         direction='-X to +X'))
        self.checkBoundaries(
            edgedict={'edgebdy' : [848, 867, 1799, 1809, 2180, 2256]})

        # Ditto for faces.
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(2.7579,7.20464,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=0, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(3.18599,6.80866,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(2.88633,6.11302,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(4.05286,7.18324,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(3.53916,5.74915,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(4.64148,6.68024,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Graphics_1.Toolbox.Select_Face.Single_Face(
            skeleton='skeltest:skeleton',
            points=[Point(4.33112,6.08092,21.2376)],
            view=View(cameraPosition=Coord(5,5,34.2583),
                      focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30,
                      clipPlanes=[], invertClip=0, size_x=691, size_y=652),
            shift=1, ctrl=0)
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='facebdy', 
            constructor=FaceFromFaces(
                group=selection,
                direction='-Z to +Z'))
        self.checkBoundaries(
            facedict={'facebdy' :
                      [854, 864, 874, 892, 2137, 2140, 2150]})

        # Undo
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        ## TODO 3.0: Are the undone faceboundary faces correct?  face
        ## boundaries and face selections behave differently when the
        ## refined boundary or selection corresponds to only part of
        ## the unrefined one.
        self.checkBoundaries(nodedict={'ptbdy': [20, 23, 26]},
                             edgedict={'edgebdy' : [189, 241]},
                             facedict={'facebdy': [194, 204]})

        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        self.checkBoundaries(
            nodedict={'ptbdy' : [20, 23, 26, 68, 105,]},
            edgedict={'edgebdy' : [848, 867, 1799, 1809, 2180, 2256]},
            facedict={'facebdy' : [854, 864, 874, 892, 2137, 2140, 2150]}
        )

    @memorycheck.check("skeltest")
    def SkelStackTest(self):
        # Make three skeleton modifications (that don't actually
        # change anything, but that doesn't matter), undo the last
        # modification, and check that new boundaries are propagated
        # correctly to the top and bottom of the stack.  It's
        # important to check the case where the current skeleton is a
        # deputy at the time that the new boundaries are created.
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Anneal(targets=AllNodes(),
                            criterion=AverageEnergy(alpha=0.3),
                            T=0.0,
                            delta=1.0,
                            iteration=FixedIteration(iterations=1)))
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Anneal(targets=AllNodes(),
                            criterion=AverageEnergy(alpha=0.3),
                            T=0.0, 
                            delta=1.0,
                            iteration=FixedIteration(iterations=1)))
        OOF.Skeleton.Modify(
            skeleton='skeltest:skeleton',
            modifier=Refine(targets=CheckHomogeneity(threshold=0.9),
                            criterion=Unconditionally(),
                            alpha=0.3))

        # Go back to one of the annealed skeletons
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')

        self.selectThreeNodes()
        self.selectThreeSegments()
        self.selectThreeFaces()

        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='facebdy',
            constructor=FaceFromFaces(group=selection,
                                      direction='-X to +X'))
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton', 
            name='edgebdy', 
            constructor=EdgeFromSegments(group=selection,
                                         direction='-X to +X'))
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton', 
            name='pointbdy',
            constructor=PointFromNodes(group=selection))

        # Go back to the initial skeleton
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Undo(skeleton='skeltest:skeleton')

        self.checkBoundaries(nodedict={'pointbdy' : [11, 14, 17]},
                             edgedict={'edgebdy' : [78, 79, 134]},
                             facedict={'facebdy' : [201, 202, 212]})

        # Go to the most modified skeleton.
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')
        OOF.Skeleton.Redo(skeleton='skeltest:skeleton')

        self.checkBoundaries(nodedict={'pointbdy' : [11, 14, 17]},
                             edgedict={'edgebdy' : [292, 338, 339]},
                             facedict={'facebdy' : [368, 369, 519]})    
    # TODO 3.1: 
    # all of the above, but from element/face/segment/node groups?

    # Modify -- all operations on all bdy types, w/o skeleton mods
        # check that modify works on renamed bdys
    # ForwardPropagate -- are new/modified bdys propagated to child skeletons?
    # SelectNamedBoundaries

        
test_set = [
    Skeleton_Boundary("Defaults"),
    Skeleton_Boundary("ConstructPointFromNodes"),
    Skeleton_Boundary("ConstructPointFromSegments"),
    Skeleton_Boundary("ConstructPointFromFaces"),
    Skeleton_Boundary("ConstructPointFromElements"),
    Skeleton_Boundary("ConstructPointFromNodeGroup"),
    Skeleton_Boundary("ConstructEdgeFromSegments"),
    Skeleton_Boundary("ConstructEdgeLoopFromSegments"),
    Skeleton_Boundary("ConstructEdgeFromNodes"),
    Skeleton_Boundary("ConstructEdgeLoopFromNodes"),
    Skeleton_Boundary("ConstructEdgeLoopFromFaces"),
    Skeleton_Boundary("ConstructFaceFromFaces"),
    Skeleton_Boundary("ConstructFaceFromFaces2"),
    Skeleton_Boundary("FailFaceFromFaces"),
    Skeleton_Boundary("Moebius"),
    Skeleton_Boundary("ConstructFaceFromElements"),
    Skeleton_Boundary("Delete"),
    Skeleton_Boundary("Rename"),
    Skeleton_Boundary("RemoveSegments"),
    Skeleton_Boundary("RemoveFaces"),
    Skeleton_Boundary("ReverseSegments"),
    Skeleton_Boundary("RefinedDefaults"),
    Skeleton_Boundary("BackPropagate"),
    Skeleton_Boundary("SkelStackTest"),
]

# test_set = [
#     Skeleton_Boundary("SkelStackTest"),
# ]
