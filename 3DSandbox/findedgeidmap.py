import vtk
import sys, os
from math import *


# script to find map between edge id within whole tet (ranging from
# 0-5) and within each face (ranging fro 0-2)

def tetVolume(p0,p1,p2,p3):
    # (1.0/6.0) *  fabs( dot( (v3-v0) , ((v3-v1)%(v3-v2)) ) );
    return (1.0/6.0) * abs( (p3-p0) * ( (p3-p1).cross(p3-p2) ) )

def tetCellVolume(cell):
    points=[]
    for i in xrange(4):
        points.append(cell.GetPoints().GetPoint(i))
    ps = primitives.pontify(points)
    return tetVolume(ps[0],ps[1],ps[2],ps[3])



# make a mesh
def makeVoxelGrid(nCubes):
    max_x=nCubes+1
    max_y=nCubes+1
    max_z=nCubes+1
    scale=20./nCubes #*(19./20)
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

meshGrid = makeVoxelGrid(1)

# tetrahedralize the mesh
delaunay3D = vtk.vtkDelaunay3D()
delaunay3D.SetInput(meshGrid)
meshGrid = delaunay3D.GetOutput()
meshGrid.Update()
#print meshGrid
#print meshGrid.GetCell(0)



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

def inBounds(point,bounds):
    if point[0]>=bounds[0] and point[0]<=bounds[1] and point[1]>=bounds[2] and point[1]<=bounds[3] and point[2]>=bounds[4] and point[2]<=bounds[5]:
        return True
    return False

numcells = meshGrid.GetNumberOfCells()
print "numcells = ", numcells

cellswithissues = []
homogeneity = 0
microstructureVolume = 20**3
p1 = [0,0,0]
p2 = [0,0,0]
edgedict = {}
facedict = {}
for i in xrange(numcells): #xrange(0,25):0
    print "\n\n\nCELL",i
    volumes={}
    cell=meshGrid.GetCell(i)
    print "bounds = ", cell.GetBounds()
    numEdges=cell.GetNumberOfEdges()
    bounds=cell.GetBounds()

    print "POINTS" 
    numPts = cell.GetPoints().GetNumberOfPoints()
    for j in xrange(numPts):
        id = cell.GetPointIds().GetId(j)
        x = cell.GetPoints().GetPoint(j)
        print id, x


    for j in xrange(cell.GetNumberOfEdges()):
        edgedict[j] = [cell.GetEdge(j).GetPointId(0), cell.GetEdge(j).GetPointId(1)]
    print edgedict

    for j in xrange(cell.GetNumberOfFaces()):
        print "FACE ",j
        facedict[j]=[]
        for k in xrange(cell.GetFace(j).GetNumberOfEdges()):
            id1 = cell.GetFace(j).GetEdge(k).GetPointId(0)
            id2 = cell.GetFace(j).GetEdge(k).GetPointId(1)
            for edgeId in edgedict.keys():
                if (edgedict[edgeId][0]==id1 and edgedict[edgeId][1]==id2):
                    facedict[j].append( (edgeId, 1) )
                elif (edgedict[edgeId][1]==id1 and edgedict[edgeId][0]==id2):
                    facedict[j].append( (edgeId, -1) )
        print facedict[j]


        

    clippedpoly = {}
    clippedpolymapper = {}
    clippedpolyactor = {}
    outputgrid = {}
    outputgridmapper = {}
    outputgridactor = {}


    # visualize the one cell
    oneboxmesh = vtk.vtkUnstructuredGrid()
    oneboxmesh.Allocate(1,1)
    oneboxmesh.SetPoints(meshGrid.GetPoints())
    oneboxmesh.InsertNextCell(meshGrid.GetCell(i).GetCellType(),meshGrid.GetCell(i).GetPointIds())
    meshactor = vtk.vtkActor()
    meshmapper = vtk.vtkDataSetMapper()
    meshmapper.SetInput(oneboxmesh)
    meshactor.SetMapper(meshmapper)
    meshactor.GetProperty().SetRepresentationToWireframe()
    meshactor.GetProperty().SetColor(0,0,0)
    meshactor.GetProperty().SetLineWidth(3)



    




# axes actor
axes = vtk.vtkAxesActor()
axes.SetTotalLength(5,5,5)

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

## ren = vtk.vtkRenderer()
## renWin = vtk.vtkRenderWindow()
## renWin.AddRenderer(ren)
## renWin.SetSize(600, 600)
## iren = vtk.vtkRenderWindowInteractor()
## iren.SetRenderWindow(renWin)
## ren.SetBackground(.5, .5, .5)

## ## ren.AddVolume(volume)
## ## ren.AddActor(wholemeshactor)
## ren.AddActor(meshactor)
## ren.AddActor(axes)


## ren.ResetCamera()
## ren.ResetCameraClippingRange()
## ren.GetActiveCamera().SetFocalPoint((bounds[0]+bounds[1])/2,(bounds[2]+bounds[3])/2,(bounds[4]+bounds[5])/2)

## # Render the scene and start interaction.
## iren.Initialize()
## renWin.Render()
## iren.Start()
