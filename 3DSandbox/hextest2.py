import vtk
import sys, os
from math import *


# test to get ordering of hexahedron point right, such that the normal
# of each face points out.


# display the box
hexpoints = vtk.vtkPoints()
hexpoints.SetNumberOfPoints(8)

hexpoints.InsertPoint(0, 0, 0, 0)
hexpoints.InsertPoint(1, 1, 0, 0)
hexpoints.InsertPoint(2, 1, 1, 0)
hexpoints.InsertPoint(3, 0, 1, 0)
hexpoints.InsertPoint(4, 0, 0, 1)
hexpoints.InsertPoint(5, 1, 0, 1)
hexpoints.InsertPoint(6, 1, 1, 1)
hexpoints.InsertPoint(7, 0, 1, 1)

## hexpoints.InsertPoint(0,bounds[0],bounds[2],bounds[4])
## hexpoints.InsertPoint(1,bounds[1],bounds[2],bounds[4])
## hexpoints.InsertPoint(2,bounds[0],bounds[3],bounds[4])
## hexpoints.InsertPoint(3,bounds[1],bounds[3],bounds[4])
## hexpoints.InsertPoint(4,bounds[0],bounds[2],bounds[5])
## hexpoints.InsertPoint(5,bounds[1],bounds[2],bounds[5])
## hexpoints.InsertPoint(6,bounds[0],bounds[3],bounds[5])
## hexpoints.InsertPoint(7,bounds[1],bounds[3],bounds[5])


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


# This example poses some challenges.  Points (1,1,0), (2,1,0),
# (3,1,0) return -1 for evaluate position.
## hexpoints.InsertPoint(0, 1.5, 1, 1.25)
## hexpoints.InsertPoint(1, 1.5, 2, 1)
## hexpoints.InsertPoint(2, 2.5, 2, .75)
## hexpoints.InsertPoint(3, 2.5, 1, 1)
## hexpoints.InsertPoint(4, 1,   1, 2)
## hexpoints.InsertPoint(5, 1,   2, 2)
## hexpoints.InsertPoint(6, 2,   2, 2)
## hexpoints.InsertPoint(7, 2,   1, 2)

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
for i in xrange(6):
    print "FACE ",i
    face=hexa.GetFace(i)
    points=vtk.vtkPoints()
    for j in xrange(3):
        print face.GetPoints().GetPoint(j)
        points.InsertPoint(j,face.GetPoints().GetPoint(j))
    poly.ComputeNormal(points,normal)
    print normal



# display

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(.5, .5, .5)

ren.AddActor(hexactor)

ren.ResetCamera()
ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()
