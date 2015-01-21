import vtk
import sys, os
from math import *
from random import *

# finding the right order for adding points in a tetra, so that the
# normals point out


# make a mesh
def makeVoxelGrid(nCubes):
    max_x=nCubes+1
    max_y=nCubes+1
    max_z=nCubes+1
    scale=5./nCubes #*(19./20)
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
                # This is the order we need such that the normals point out.
                cell.GetPointIds().SetId(0, (i+1)*(max_y)*(max_z)+j*(max_z)+k)       # upper left front
                cell.GetPointIds().SetId(1, (i+1)*(max_y)*(max_z)+(j+1)*(max_z)+k)   # upper right front
                cell.GetPointIds().SetId(2, i*(max_y)*(max_z)+(j+1)*(max_z)+k)       # lower right front
                cell.GetPointIds().SetId(3, i*(max_y)*(max_z)+j*(max_z)+k)           # lower left front node index
                cell.GetPointIds().SetId(4, (i+1)*(max_y)*(max_z)+j*(max_z)+k+1)     # upper left back
                cell.GetPointIds().SetId(5, (i+1)*(max_y)*(max_z)+(j+1)*(max_z)+k+1) # upper right back
                cell.GetPointIds().SetId(6, i*(max_y)*(max_z)+(j+1)*(max_z)+k+1)     # lower right back
                cell.GetPointIds().SetId(7, i*(max_y)*(max_z)+j*(max_z)+k+1)         # lower left back
                meshGrid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

    return meshGrid

def makeTetraGrid(nCubes, flip=0):
    max_x=nCubes+1
    max_y=nCubes+1
    max_z=nCubes+1
    scale=5./nCubes #*(19./20)
    meshPoints = vtk.vtkPoints()
    meshPoints.SetNumberOfPoints(max_x*max_y*max_z)
    #i*(max_y)*(max_z)+j*(max_z)+k
    for i in xrange(max_x):
        for j in xrange(max_y):
            for k in xrange(max_z):
                meshPoints.InsertPoint(i*(max_y)*(max_z)+j*(max_z)+k,scale*i,scale*j,scale*k)

    nelements = 5*(max_x-1)*(max_y-1)*(max_z-1)
    meshGrid = vtk.vtkUnstructuredGrid()
    meshGrid.Allocate(nelements, nelements)
    meshGrid.SetPoints(meshPoints)

    for i in range(max_x-1):                  
        for j in range(max_y-1):              
            for k in range(max_z-1):
                ulf = (i+1)*(max_y)*(max_z)+j*(max_z)+k        # upper left front
                urf = (i+1)*(max_y)*(max_z)+(j+1)*(max_z)+k    # upper right front
                lrf = i*(max_y)*(max_z)+(j+1)*(max_z)+k        # lower right front
                llf = i*(max_y)*(max_z)+j*(max_z)+k            # lower left front 
                ulb = (i+1)*(max_y)*(max_z)+j*(max_z)+k+1      # upper left back
                urb = (i+1)*(max_y)*(max_z)+(j+1)*(max_z)+k+1  # upper right back 
                lrb = i*(max_y)*(max_z)+(j+1)*(max_z)+k+1      # lower right back
                llb = i*(max_y)*(max_z)+j*(max_z)+k+1          # lower left back
                
                point_order = [  # not flip
                    [[llf,urf,lrf,lrb],
                     [llf,ulf,urf,ulb],
                     [lrb,urf,urb,ulb],
                     [llf,lrb,llb,ulb],
                     [llf,ulb,urf,lrb]],
                    # flip
                    [[llf,ulf,lrf,llb],
                     [ulf,urf,lrf,urb],
                     [ulf,ulb,urb,llb],
                     [lrf,urb,lrb,llb],
                     [ulf,urb,lrf,llb]
                     ]]
                
                for o in point_order[flip]:
                    cell = vtk.vtkTetra()
                    id=0
                    for p in o:
                        cell.GetPointIds().SetId(id,p)
                        id+=1
                    meshGrid.InsertNextCell(cell.GetCellType(),cell.GetPointIds())

    return meshGrid
   

#meshGrid = makeVoxelGrid(1)
meshGrid = makeTetraGrid(3,1)
numCells = meshGrid.GetNumberOfCells()
data = vtk.vtkIntArray()
data.Allocate(numCells, numCells)
meshGrid.GetCellData().SetScalars(data)
for i in xrange(numCells):
    data.InsertNextTuple1(randint(0,4))
    

print "made mesh"
print meshGrid.GetBounds()
numCells = meshGrid.GetNumberOfCells()
wholemeshactor = vtk.vtkActor()
wholemeshmapper = vtk.vtkDataSetMapper()
wholemeshmapper.SetInput(meshGrid)
wholemeshmapper.SetScalarModeToUseCellData()
wholemeshmapper.SetScalarRange(0,4)
wholemeshactor.SetMapper(wholemeshmapper)
#wholemeshactor.GetProperty().SetRepresentationToWireframe()
#wholemeshactor.GetProperty().SetColor(0,0,0)
wholemeshactor.GetProperty().SetLineWidth(3)
#color = vtk.vtkColorTransferFunction()
#color.AddRGBPoint(0,1,1,1)
#color.AddRGBPoint(1,.8,.2,.2)
#color.AddRGBPoint(2,.2,.8,.2)
#color.AddRGBPoint(3,.2,.2,.8)
#color.AddRGBPoint(4,.8,.8,.2)
color = vtk.vtkLookupTable()
#color.SetHueRange(0,.66667)
color.SetNumberOfColors(5)
color.SetTableValue(0,1,1,1,1)
color.SetTableValue(1,.8,.2,.2,1)
color.SetTableValue(2,.2,.8,.2,1)
color.SetTableValue(3,.2,.2,.8,1)
color.SetTableValue(4,.8,.8,.2,0)
color.Build()
for i in xrange(5):
    print color.GetTableValue(i)
wholemeshmapper.SetLookupTable(color)



# display

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(.5, .5, .5)

## ren.AddVolume(volume)
ren.AddActor(wholemeshactor)

ren.ResetCamera()
ren.ResetCameraClippingRange()


# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()












