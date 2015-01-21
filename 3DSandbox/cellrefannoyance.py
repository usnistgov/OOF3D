import vtk
import sys, os
from math import *


poly = vtk.vtkPolyData()
poly.Allocate(1000,1000)
points = vtk.vtkPoints()
points.Allocate(1000,1000)
poly.SetPoints(points)


for i in xrange(6):
    points.InsertNextPoint(i,0,0)
    points.InsertNextPoint(i,1,0)


for i in xrange(5):
    quad = vtk.vtkQuad()
    quad.GetPointIds().SetId(0,2*i)
    quad.GetPointIds().SetId(1,2*i+1)
    quad.GetPointIds().SetId(2,2*i+3)
    quad.GetPointIds().SetId(3,2*i+2)
    poly.InsertNextCell(quad.GetCellType(),quad.GetPointIds())


# now that we have a simple polydata set up, test the reference
# annoyance
quad1 = poly.GetCell(0)
print "quad1", quad1.GetBounds()
quad2 = poly.GetCell(1)
print "quad2", quad2.GetBounds()
print "quad1", quad1.GetBounds()
# this gives this output, the reference to quad 1 is overwritten!
## quad1 (0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
## quad2 (1.0, 2.0, 0.0, 1.0, 0.0, 0.0)
## quad1 (1.0, 2.0, 0.0, 1.0, 0.0, 0.0)

# try using another version of GetCell
quad1 = vtk.vtkGenericCell()
quad2 = vtk.vtkGenericCell()
poly.GetCell(0,quad1)
print "quad1", quad1.GetBounds()
poly.GetCell(1,quad2)
print "quad2", quad2.GetBounds()
print "quad1", quad1.GetBounds()
# this fixes the problem!
## quad1 (0.0, 1.0, 0.0, 1.0, 0.0, 0.0)
## quad2 (1.0, 2.0, 0.0, 1.0, 0.0, 0.0)
## quad1 (0.0, 1.0, 0.0, 1.0, 0.0, 0.0)





poly.Update()
polymapper = vtk.vtkDataSetMapper()
polymapper.SetInput(poly)
polyactor = vtk.vtkActor()
polyactor.SetMapper(polymapper)
polyactor.GetProperty().SetRepresentationToWireframe()

    

# display

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(.5, .5, .5)

ren.AddActor(polyactor)

ren.ResetCamera()
ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()




















