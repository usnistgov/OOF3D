# -*- python -*-

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
                OOF.FaceSelection.Select(
                    skeleton='skeltest:skeleton',
                    method=SelectNamedBoundaryFaces(boundary=bdyname,
                                                    operator=Select()))
                self.assertEqual(
                    selection_utils.selectedFaceIDs(self.skelctxt), faces)

        if edgedict is not None:
            real_edges = self.skelctxt.edgeboundaries.keys()
            if complete:
                self.assertEqual(sorted(edgedict.keys()), sorted(real_edges))
            else:
                self.assert_(all(e in real_edges for e in edgedict))
            for bdyname, edges in edgedict.items():
                OOF.SegmentSelection.Select(
                    skeleton='skeltest:skeleton',
                    method=SelectNamedBoundarySegments(boundary=bdyname,
                                                       operator=Select()))
                self.assertEqual(
                    selection_utils.selectedSegmentIDs(self.skelctxt), edges)

        if nodedict is not None:
            real_points = self.skelctxt.pointboundaries.keys()
            if complete:
                self.assertEqual(sorted(nodedict.keys()), sorted(real_points))
            else:
                self.assert_(all(n in real_points for n in nodedict))
            for bdyname, points in nodedict.items():
                OOF.NodeSelection.Select(
                    skeleton='skeltest:skeleton',
                    method=SelectNamedBoundaryNodes(boundary=bdyname,
                                                    operator=Select()))
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
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(
                point=Coord(0,5,10),
                operator=(AddSelection() if shift else Select())))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,5,10),
                                    operator=AddSelection()))

    # Select the nodes at x=0,5,10; y=10, z=10
    def selectThreeTopNodes(self, shift=0):
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(
                point=Coord(0,10,10),
                operator=(AddSelection() if shift else Select())))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,10,10),
                                    operator=AddSelection()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,10,10),
                                    operator=AddSelection()))

    # Select the nodes at x=0,5,10; y=0, z=10
    def selectThreeBottomNodes(self):
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SelectNamedBoundarySegments(boundary='YminZmax',
                                               operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedSegments(operator=Select()))

    def selectThreeSegments(self):
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[11, 14],
                                       operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[5, 14],
                                       operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[5, 7],
                                       operator=AddSelection()))
    
    def selectThreeFaces(self):
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[10, 11, 19],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 20, 19],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[20, 23, 19],
                                    operator=AddSelection()))

    def selectOneElement(self):
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=26,operator=Select()))

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
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[11, 1],
                                       operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[4, 1],
                                       operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[7, 4],
                                       operator=AddSelection()))

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
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,5,10),
                                    operator=AddSelection()))
        self.assertRaises(
            ooferror.ErrUserError,
            OOF.Skeleton.Boundary.Construct,
            skeleton='skeltest:skeleton',
            name='boundary3', 
            constructor=EdgeFromNodes(group=selection,direction=
                                      '-X to +X'))
        # Add another (10, 0, 10) to to resolve the ambiguity
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(10,0,10),
                                    operator=AddSelection()))
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
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(0,0,0),
                                    operator=AddSelection()))
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
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=Toggle()))
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton', name='boundary',
            constructor=EdgeFromNodes(group=selection,
                                      direction='Clockwise-z'))
        self.checkBoundaries(edgedict={'boundary' : 
                                       [67, 69, 132, 133, 196, 197, 245, 246]})
        self.checkNodeOrder('boundary', [2, 11, 20, 23, 26, 17, 8, 5])
        # Select the middle node of the face, making the set unsequenceable.
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleNodeSelect(point=Coord(5,5,10),
                                    operator=AddSelection()))
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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Exterior',
                                            operator=Select()))
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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[1, 10, 9],
                                    operator=AddSelection()))
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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Exterior',
                                            operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],
                                    operator=AddSelection()))
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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceFromSelectedElements(coverage='Exterior',
                                            operator=Select()))
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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[23, 14, 13],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[13, 22, 23],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 23, 20],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[23, 26, 25],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[23, 25, 22],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 20, 19],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[10, 11, 19],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[10, 19, 9],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[19, 18, 9],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[18, 21, 9],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[21, 12, 9],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 12, 21],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[24, 15, 21],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[15, 24, 25],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[25, 16, 15],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[17, 16, 25],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[26, 17, 25],
                                    operator=AddSelection()))

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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=FaceSelectGroup(group='moebius',operator=Select()))

        # Deselecting one of the faces should make the surface
        # orientable, and boundary creation should work.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 14, 23],
                                    operator=Unselect()))
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='boundary', 
            constructor=FaceFromFaces(
                group=selection,
                direction='-X to +X'))
        self.checkBoundaries(
            facedict={
                'boundary' : [160, 178, 179, 185, 193, 201, 204, 209, 212,
                              219, 234, 235, 238, 250, 251, 256, 259]})

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
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=ExpandElementSelection(mode='Faces'))

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
        OOF.ElementSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleElementSelect(element=32,
                                       operator=AddSelection()))
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
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[26, 17],
                                       operator=Select()))
        OOF.Skeleton.Boundary.Modify(
            skeleton='skeltest:skeleton',
            boundary='XmaxZmax',
            modifier=RemoveSegments(group=selection))
        self.checkBoundaries(edgedict={"XmaxZmax":[132]})
        self.checkNodeOrder('XmaxZmax', [8, 17])
        # Try to remove the selected segment from a boundary that it's
        # not part of.
        OOF.Skeleton.Boundary.Modify(
            skeleton='skeltest:skeleton',
            boundary='XminZmax',
            modifier=RemoveSegments(group=selection))
        self.checkBoundaries(edgedict={'XminZmax':[67, 196]})
        self.checkNodeOrder('XminZmax', [2, 11, 20])
        # Select two segments, and remove them from a boundary that
        # contains only one of them.
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 26],
                                       operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[26, 17],
                                       operator=AddSelection()))
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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[5, 8, 17],
                                    operator=Select()))
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
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[5, 8, 17],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[23, 17, 26],
                                    operator=AddSelection()))
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
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SelectNamedBoundarySegments(boundary='YmaxZmax',
                                               operator=Select()))
        OOF.NodeSelection.Select(
            skeleton='skeltest:skeleton',
            method=NodeFromSelectedSegments(operator=Select()))
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='ptbdy',
            constructor=PointFromNodes(group=selection))
        self.checkBoundaries(nodedict={'ptbdy': [20, 23, 26, 68, 105,]})

        # Create a new edge boundary, including the equivalents of
        # some complete and some incomplete unrefined segments.
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[111, 11],
                                       operator=Select()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[69, 11],
                                       operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[23, 69],
                                       operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[103, 23],
                                       operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[103, 17],
                                       operator=AddSelection()))
        OOF.SegmentSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleSegmentSelect(nodes=[17, 114],
                                       operator=AddSelection()))
        OOF.Skeleton.Boundary.Construct(
            skeleton='skeltest:skeleton',
            name='edgebdy',
            constructor=EdgeFromSegments(group=selection,
                                         direction='-X to +X'))
        self.checkBoundaries(
            edgedict={'edgebdy' : [848, 867, 1799, 1809, 2180, 2256]})

        # Ditto for faces.
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[69, 97, 102],
                                    operator=Select()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 97, 69],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[11, 69, 67],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[67, 69, 68],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[67, 68, 20],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[69, 23, 68],
                                    operator=AddSelection()))
        OOF.FaceSelection.Select(
            skeleton='skeltest:skeleton',
            method=SingleFaceSelect(nodes=[69, 102, 23],
                                    operator=AddSelection()))
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
