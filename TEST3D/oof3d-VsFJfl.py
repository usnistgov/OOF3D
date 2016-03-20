OOF.Microstructure.Create_From_ImageFile(filenames=ThreeDImageDirectory(directory='../examples/bone',sort=NumericalOrder()), microstructure_name='bone', height=automatic, width=automatic, depth=automatic)
OOF.Image.AutoGroup(image='bone:bone', name_template='%c')
OOF.Skeleton.New(name='skeleton', microstructure='bone', x_elements=4, y_elements=4, z_elements=4, skeleton_geometry=TetraSkeleton(arrangement='moderate'))
