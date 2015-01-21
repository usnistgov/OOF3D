import vtk
import sys, os
from math import *

import oof3d
sys.path.append(os.path.dirname(oof3d.__file__))

from ooflib.SWIG.engine import clipimage3d
from ooflib.common import primitives

def tetVolume(p0,p1,p2,p3):
    # (1.0/6.0) *  fabs( dot( (v3-v0) , ((v3-v1)%(v3-v2)) ) );
    return (1.0/6.0) * abs( (p3-p0) * ( (p3-p1).cross(p3-p2) ) )

def hexVolume(hexahedron):
    tets=((0,1,2,5),(2,5,6,7),(0,2,3,7),(0,2,5,7),(0,4,5,7))

    points = []
    for i in xrange(8):
        points.append(hexahedron.GetPoints().GetPoint(i))
    ps = primitives.pontify(points)
    volume=0
    for tet in tets:
        volume += tetVolume(ps[tet[0]],ps[tet[1]],ps[tet[2]],ps[tet[3]])
    return volume
    

def makeVoxelGrid(cubesize, scale):
    max_x=cubesize
    max_y=cubesize
    max_z=cubesize
    meshPoints = vtk.vtkPoints()
    meshPoints.SetNumberOfPoints(max_x*max_y*max_z)
    #i*(max_y)*(max_z)+j*(max_z)+k
    for i in xrange(max_x):
        for j in xrange(max_y):
            for k in xrange(max_z):
                meshPoints.InsertPoint(i*(max_y)*(max_z)+j*(max_z)+k,scale*i,scale*j,scale*k)

    nelements = (max_x-1)*(max_y-1)*(max_z-1)
    meshGrid = vtk.vtkUnstructuredGrid()
    meshGrid.Allocate(nelements, nelements)
    meshGrid.SetPoints(meshPoints)

    for i in range(max_x-1):                  
        for j in range(max_y-1):              
            for k in range(max_z-1):          
                cell = vtk.vtkHexahedron()
                cell.GetPointIds().SetId(0, i*(max_y)*(max_z)+j*(max_z)+k)           # lower left front node index
                cell.GetPointIds().SetId(1, i*(max_y)*(max_z)+(j+1)*(max_z)+k)       # lower right front
                cell.GetPointIds().SetId(2, (i+1)*(max_y)*(max_z)+(j+1)*(max_z)+k)   # upper right front
                cell.GetPointIds().SetId(3, (i+1)*(max_y)*(max_z)+j*(max_z)+k)       # upper left front
                cell.GetPointIds().SetId(4, i*(max_y)*(max_z)+j*(max_z)+k+1)         # lower left back
                cell.GetPointIds().SetId(5, i*(max_y)*(max_z)+(j+1)*(max_z)+k+1)     # lower right back
                cell.GetPointIds().SetId(6, (i+1)*(max_y)*(max_z)+(j+1)*(max_z)+k+1) # upper right back
                cell.GetPointIds().SetId(7, (i+1)*(max_y)*(max_z)+j*(max_z)+k+1)     # upper left back
                meshGrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

    return meshGrid




# read in image and create volume actor

reader = vtk.vtkTIFFReader()
reader.SetDataExtent(0,19,0,19,0,19)
reader.SetFilePattern("/users/vrc/OOF2/TEST3D/ms_data/5color/slice%i.tif")
image = reader.GetOutput()
image.Update()

mapper = vtk.vtkFixedPointVolumeRayCastMapper()
mapper.SetInput(image)
volproperty = vtk.vtkVolumeProperty()
volproperty.IndependentComponentsOff()
volume = vtk.vtkVolume()
volume.SetMapper(mapper)
volume.SetProperty(volproperty)


# we want an indexed image

indexer = vtk.vtkImageQuantizeRGBToIndex()
indexer.SetInput(image)
#indexer.SetNumberOfColors(5) # causes errors!
indexedImage = indexer.GetOutput()
indexedImage.Update()
lookuptable = indexer.GetLookupTable()

# create skeleton

meshGrid = makeVoxelGrid(5,5)

meshMapper = vtk.vtkDataSetMapper()
meshMapper.SetInput(meshGrid)
meshActor = vtk.vtkActor()
meshActor.SetMapper(meshMapper)
meshActor.GetProperty().SetRepresentationToWireframe()
meshActor.GetProperty().SetColor(0,0,0)
meshActor.GetProperty().SetLineWidth(5)


# cut image grid by skeleton cell

# for now, try with arbitrary box
box = vtk.vtkBox()
#box.SetBounds(1.5,4.5,1.5,4.5,1.5,4.5)
box.SetBounds(1.5, 3.5, 5.5, 7.5, 0, 2.5)
#box.SetBounds(1,2,1,2,1,2) #causes empty output!
#box.SetBounds(0,5,0,5,0,5)
bounds=[0,0,0,0,0,0]
box.GetBounds(bounds)


# display the box
hexpoints = vtk.vtkPoints()
hexpoints.SetNumberOfPoints(8)

## hexpoints.InsertPoint(0,bounds[0],bounds[2],bounds[4])
## hexpoints.InsertPoint(1,bounds[0],bounds[3],bounds[4])
## hexpoints.InsertPoint(2,bounds[1],bounds[3],bounds[4])
## hexpoints.InsertPoint(3,bounds[1],bounds[2],bounds[4])
## hexpoints.InsertPoint(4,bounds[0],bounds[2],bounds[5])
## hexpoints.InsertPoint(5,bounds[0],bounds[3],bounds[5])
## hexpoints.InsertPoint(6,bounds[1],bounds[3],bounds[5])
## hexpoints.InsertPoint(7,bounds[1],bounds[2],bounds[5])

## hexpoints.InsertPoint(0,1,1,1)
## hexpoints.InsertPoint(1,1,2,1)
## hexpoints.InsertPoint(2,2,2,1)
## hexpoints.InsertPoint(3,2,1,1)
## hexpoints.InsertPoint(4,1,1,2)
## hexpoints.InsertPoint(5,1,2,2)
## hexpoints.InsertPoint(6,2,2,2)
## hexpoints.InsertPoint(7,2,1,2)


# This example poses some challenges. 
hexpoints.InsertPoint(0, 1.5, 1, 1)
hexpoints.InsertPoint(1, 1.5, 2.7, 1.)
hexpoints.InsertPoint(2, 2.5, 2.7, 1.)
hexpoints.InsertPoint(3, 2.5, 1, 1.)
hexpoints.InsertPoint(4, 1,   1, 2)
hexpoints.InsertPoint(5, 1,   2, 2)
hexpoints.InsertPoint(6, 2,   2, 2)
hexpoints.InsertPoint(7, 2,   1, 2)

hexahedron = vtk.vtkHexahedron()
hexahedron.GetPointIds().SetId(0,0)
hexahedron.GetPointIds().SetId(1,1)
hexahedron.GetPointIds().SetId(2,2)
hexahedron.GetPointIds().SetId(3,3)
hexahedron.GetPointIds().SetId(4,4)
hexahedron.GetPointIds().SetId(5,5)
hexahedron.GetPointIds().SetId(6,6)
hexahedron.GetPointIds().SetId(7,7)
hexgrid = vtk.vtkUnstructuredGrid()
hexgrid.Allocate(1,1)
hexgrid.SetPoints(hexpoints)
hexgrid.InsertNextCell(hexahedron.GetCellType(), hexahedron.GetPointIds())
hexmapper = vtk.vtkDataSetMapper()
hexmapper.SetInput(hexgrid)
hexactor = vtk.vtkActor()
hexactor.SetMapper(hexmapper)
hexactor.GetProperty().SetRepresentationToWireframe()
hexactor.GetProperty().SetColor(0,0,0)
hexactor.GetProperty().SetLineWidth(5)


#check that the hexahedron is legal
hexa=hexgrid.GetCell(0)
normal=[0,0,0]
poly=vtk.vtkPolygon()
plane=vtk.vtkPlane()
for i in xrange(6):
    #print "FACE ",i
    face=hexa.GetFace(i)
    points=vtk.vtkPoints()
    for j in xrange(3):
        #print face.GetPoints().GetPoint(j)
        points.InsertPoint(j,face.GetPoints().GetPoint(j))
    poly.ComputeNormal(points,normal)
    #print normal
    dist = plane.DistanceToPlane(face.GetPoints().GetPoint(3), normal, face.GetPoints().GetPoint(0))
    #print dist
    if abs(dist)>1e-15:
        print "FOUR POINTS NOT IN SAME PLANE FOR FACE",i, dist
        for j in xrange(4):
            print face.GetPoints().GetPoint(j)


# try with our modified clipped volume

clipImage = clipimage3d.ClipImage3D()
clipImage.SetInputConnection(indexedImage.GetProducerPort())
#clipImage.InsideOutOn()
#clipImage.Mixed3DCellGenerationOff() 
#clipImage.SetClipFunction(box)
clipImage.SetClipCell(hexgrid, 0)
clippedImage2 = clipImage.GetOutput()
clippedImage2.Update()

clippedImageMapper = vtk.vtkDataSetMapper()
clippedImageMapper.SetInput(clippedImage2)
#clippedImageMapper.SetLookupTable(lookuptable)
clippedImageActor = vtk.vtkActor()
clippedImageActor.SetMapper(clippedImageMapper)
#clippedImageActor.GetProperty().SetRepresentationToWireframe()
clippedImageActor.GetProperty().SetColor(0,0,1)
clippedImageActor.GetProperty().SetLineWidth(3)


volumes = clipImage.getVolumes()
print volumes
total = 0
maxvol = 0
dominant = -1
for v in volumes:
    total += v
    if v > maxvol:
        maxvol = v
        dominant = volumes.index(v)
print "total volume =",total
boxvolume=hexVolume(hexgrid.GetCell(0))
if (abs(total-boxvolume)/boxvolume > 1e-5): print "BOX VOLUME DOES NOT EQUAL TOTAL VOLUME"
print "box volume =",boxvolume
if total>0:
    print "homogeneity =",maxvol/total
print "dominant category =",dominant

# examine tetrahedralization
numCells = clippedImage2.GetNumberOfCells()
for i in xrange(numCells):
    bounds = clippedImage2.GetCell(i).GetBounds()
    if bounds[1]-bounds[0]>1 or bounds[3]-bounds[2]>1 or bounds[5]-bounds[4]>1:
        print "TET SPANS MORE THAN ONE VOXEL"
        print clippedImage2.GetCell(i)

    


#print clipImage.GetLocator()



# for a voxel, point 0 is the point that defines the voxels value in the image
## points = indexedImage.GetCell(5).GetPoints()
## for i in xrange(8):
##     print points.GetPoint(i)

# display

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(.5, .5, .5)

#ren.AddVolume(volume)
#ren.AddVolume(indexedvolume)
#ren.AddActor(meshActor)
#ren.AddActor(imageGridActor)
ren.AddActor(clippedImageActor)
ren.AddActor(hexactor)

ren.ResetCamera()
ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()
