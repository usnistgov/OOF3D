OOF.Windows.Graphics.New()
OOF.Microstructure.Create_From_ImageFile(filenames=ThreeDImageDirectory(directory='/Users/langer/FE/OOF3D/TEST3D/ms_data/bluegreen',sort=NumericalOrder()), microstructure_name='skeltest', height=automatic, width=automatic, depth=automatic)
OOF.Skeleton.New(name='skeleton', microstructure='skeltest', x_elements=2, y_elements=2, z_elements=2, skeleton_geometry=TetraSkeleton(arrangement='moderate'))
OOF.Graphics_1.Layer.Hide(n=0)
OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(skeleton='skeltest:skeleton', points=[Point(3.97588,4.98991,21.9826)], view=View(cameraPosition=Coord(5,5,34.2583), focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, clipPlanes=[], invertClip=0, size_x=691, size_y=652), shift=0, ctrl=0)
OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(skeleton='skeltest:skeleton', points=[Point(4.99496,4.6065,21.9826)], view=View(cameraPosition=Coord(5,5,34.2583), focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, clipPlanes=[], invertClip=0, size_x=691, size_y=652), shift=1, ctrl=0)
OOF.Graphics_1.Toolbox.Select_Segment.Single_Segment(skeleton='skeltest:skeleton', points=[Point(5.9434,2.66926,21.9826)], view=View(cameraPosition=Coord(5,5,34.2583), focalPoint=Coord(5,5,5), up=Coord(0,1,0), angle=30, clipPlanes=[], invertClip=0, size_x=691, size_y=652), shift=1, ctrl=0)
OOF.Skeleton.Boundary.Construct(skeleton='skeltest:skeleton', name='boundary', constructor=PointFromSegments(group=selection))

