
import vtk
import sys, os
from math import *

trianglePoints = vtk.vtkPoints()
trianglePoints.SetNumberOfPoints(3)
trianglePoints.InsertPoint(0, 0, 0, 0)
trianglePoints.InsertPoint(1, 2, 0, 0)
trianglePoints.InsertPoint(2, 1, 2.0, 0)
triangleTCoords = vtk.vtkFloatArray()
triangleTCoords.SetNumberOfComponents(3)
triangleTCoords.SetNumberOfTuples(3)
triangleTCoords.InsertTuple3(0, 1, 1, 1)
triangleTCoords.InsertTuple3(1, 2, 2, 2)
triangleTCoords.InsertTuple3(2, 3, 3, 3)
aTriangle = vtk.vtkTriangle()
aTriangle.GetPointIds().SetId(0, 0)
aTriangle.GetPointIds().SetId(1, 1)
aTriangle.GetPointIds().SetId(2, 2)
aTriangleGrid = vtk.vtkUnstructuredGrid()
aTriangleGrid.Allocate(1, 1)
aTriangleGrid.InsertNextCell(aTriangle.GetCellType(),
                             aTriangle.GetPointIds())
aTriangleGrid.SetPoints(trianglePoints)
aTriangleGrid.GetPointData().SetTCoords(triangleTCoords)
aTriangleMapper = vtk.vtkDataSetMapper()
aTriangleMapper.SetInput(aTriangleGrid)
aTriangleActor = vtk.vtkActor()
aTriangleActor.SetMapper(aTriangleMapper)
aTriangleActor.AddPosition(.25, .25, 0)
aTriangleActor.GetProperty().SetDiffuseColor(0,0,0)
aTriangleActor.GetProperty().SetRepresentationToWireframe()
aTriangleActor.GetProperty().SetLineWidth(3)


# try out evaluate position
cell = aTriangleGrid.GetCell(0)
points=[[0,0,0],[2,0,0],[1,2,0]]
for point in points:
    print "point = ",point
    pcoords = cell.GetParametricCoords(point)
    



# axes actor
axes = vtk.vtkAxesActor()
axes.SetTotalLength(.25,.25,.25)

# more non-intuitive vtk stuff.  SetFontSize changes boldness because
# letters are always scaled to fill width and height defined by the
# actor.
axes.GetXAxisCaptionActor2D().SetWidth(.125)
axes.GetXAxisCaptionActor2D().SetHeight(.05)
axes.GetYAxisCaptionActor2D().SetWidth(.125)
axes.GetYAxisCaptionActor2D().SetHeight(.05)
axes.GetZAxisCaptionActor2D().SetWidth(.125)
axes.GetZAxisCaptionActor2D().SetHeight(.05)



# display

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(.5, .5, .5)

ren.AddActor(aTriangleActor)
ren.AddActor(axes)

## ren.ResetCamera()
## ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()
