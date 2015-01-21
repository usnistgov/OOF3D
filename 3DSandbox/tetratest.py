import vtk
import sys, os
from math import *

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
meshGrid = makeTetraGrid(1,1)

print "made mesh"
print meshGrid.GetBounds()
numCells = meshGrid.GetNumberOfCells()
wholemeshactor = vtk.vtkActor()
wholemeshmapper = vtk.vtkDataSetMapper()
wholemeshmapper.SetInput(meshGrid)
wholemeshactor.SetMapper(wholemeshmapper)
wholemeshactor.GetProperty().SetRepresentationToWireframe()
wholemeshactor.GetProperty().SetColor(0,0,0)
wholemeshactor.GetProperty().SetLineWidth(3)


for i in [4]: #xrange(numcells):

    # visualize the one cell
    oneboxmesh = vtk.vtkUnstructuredGrid()
    oneboxmesh.Allocate(1,1)
    oneboxmesh.SetPoints(meshGrid.GetPoints())
    oneboxmesh.InsertNextCell(meshGrid.GetCell(i).GetCellType(),meshGrid.GetCell(i).GetPointIds())
    meshactor = vtk.vtkActor()
    meshmapper = vtk.vtkDataSetMapper()
    meshmapper.SetInput(oneboxmesh)
    meshactor.SetMapper(meshmapper)
    #meshactor.GetProperty().SetRepresentationToWireframe()
    meshactor.GetProperty().SetColor(0,0,1)
    meshactor.GetProperty().SetLineWidth(3)

    # find centers and normals of faces for glyphing
    polygon = vtk.vtkPolygon()
    n = [0,0,0]
    glyphpoly = vtk.vtkPolyData()
    glyphpoly.Allocate(1000,1000)
    points = vtk.vtkPoints()
    glyphpoly.SetPoints(points)
    normalarray = vtk.vtkDoubleArray()
    normalarray.SetNumberOfComponents(3)
    glyphpoly.GetPointData().SetNormals(normalarray)
    cell = meshGrid.GetCell(i)

    # glyph the normals of the faces
    for j in xrange(cell.GetNumberOfFaces()):
        face = cell.GetFace(j)
        p1 = [0,0,0]
        numPoints = face.GetPoints().GetNumberOfPoints()
        for k in xrange(numPoints):
            p2=face.GetPoints().GetPoint(k)
            p1[0]+=p2[0]/numPoints
            p1[1]+=p2[1]/numPoints
            p1[2]+=p2[2]/numPoints
        glyphpoly.GetPoints().InsertNextPoint(p1)
        polygon.ComputeNormal(face.GetPoints(), n)
        glyphpoly.GetPointData().GetNormals().InsertNextTuple3(n[0],n[1],n[2])

arrow = vtk.vtkArrowSource()
elementglyph = vtk.vtkGlyph3D()
elementglyph.SetInput(glyphpoly)
elementglyph.SetSource(arrow.GetOutput())
elementglyph.SetVectorModeToUseNormal()
glyphmapper = vtk.vtkPolyDataMapper()
glyphmapper.SetInput(elementglyph.GetOutput())
glyphactor = vtk.vtkActor()
glyphactor.SetMapper(glyphmapper)

# display

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(.5, .5, .5)

## ren.AddVolume(volume)
ren.AddActor(glyphactor)
#ren.AddActor(wholemeshactor)
ren.AddActor(meshactor)

ren.ResetCamera()
ren.ResetCameraClippingRange()


# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()












