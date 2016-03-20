def selectInteriorWhitePoint(shift=0, ctrl=0):
    # This selects a white voxel completely surrounded by white
    # voxels.
    OOF.Graphics_1.Toolbox.Pixel_Select.Point(
        source='5color:5color', 
        points=[Point(-39.9938,12.3018,40.071)], 
        view=View(cameraPosition=Coord(-40.1038,12.3068,40.1412),
                  focalPoint=Coord(10,10,10),
                  up=Coord(0.0376411,0.999195,-0.0139001), angle=30,
                  clipPlanes=[[1.0, 0.0, 0.0, 10.5]], invertClip=0),
        shift=shift, ctrl=ctrl)

def selectInteriorYellowPoint(shift=0, ctrl=0):
    # This selects a yellow voxel on the yellow/white boundary.
    # It has 12 yellow neighbors.
    OOF.Graphics_1.Toolbox.Pixel_Select.Point(
        source='5color:5color',
        points=[Point(-39.9903,12.3024,40.0768)],
        view=View(cameraPosition=Coord(-40.1038,12.3068,40.1412),
                  focalPoint=Coord(10,10,10),
                  up=Coord(0.0376411,0.999195,-0.0139001), angle=30,
                  clipPlanes=[[1.0, 0.0, 0.0, 10.5]],
                  invertClip=0),
        shift=shift, ctrl=ctrl)

selectInteriorYellowPoint()
selectInteriorWhitePoint(shift=1)

