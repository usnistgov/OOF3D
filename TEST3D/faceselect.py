OOF.Windows.Graphics.New()
OOF.Microstructure.Create_From_ImageFile(filenames=ThreeDImageDirectory(directory='/Users/langer/FE/OOF3D/TEST3D/ms_data/bluegreen',sort=NumericalOrder()), microstructure_name='skeltest', height=automatic, width=automatic, depth=automatic)
OOF.Skeleton.New(name='skeleton', microstructure='skeltest', x_elements=2, y_elements=2, z_elements=2, skeleton_geometry=TetraSkeleton(arrangement='moderate'))
OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='skeltest:skeleton', points=[Point(-13.118,18.4998,23.4669)], view=View(cameraPosition=Coord(-13.165,18.5331,23.5186), focalPoint=Coord(5,5,5), up=Coord(0.202236,0.874558,-0.440737), angle=30, clipPlanes=[], invertClip=0, size_x=691, size_y=652), shift=0, ctrl=0)
OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='skeltest:skeleton', points=[Point(-13.1157,18.5031,23.4668)], view=View(cameraPosition=Coord(-13.165,18.5331,23.5186), focalPoint=Coord(5,5,5), up=Coord(0.202236,0.874558,-0.440737), angle=30, clipPlanes=[], invertClip=0, size_x=691, size_y=652), shift=1, ctrl=0)
OOF.Graphics_1.Toolbox.Select_Face.Single_Face(skeleton='skeltest:skeleton', points=[Point(-13.1227,18.4971,23.4643)], view=View(cameraPosition=Coord(-13.165,18.5331,23.5186), focalPoint=Coord(5,5,5), up=Coord(0.202236,0.874558,-0.440737), angle=30, clipPlanes=[], invertClip=0, size_x=691, size_y=652), shift=1, ctrl=0)

