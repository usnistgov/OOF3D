import vtk
import sys, os
from math import *

import oof3d
sys.path.append(os.path.dirname(oof3d.__file__))

from ooflib.SWIG.engine import clipimage3d
from ooflib.SWIG.engine import cskeleton
from ooflib.common import primitives

#def neighbors(

def tetVolume(p0,p1,p2,p3):
    # (1.0/6.0) *  fabs( dot( (v3-v0) , ((v3-v1)%(v3-v2)) ) );
    return (1.0/6.0) * abs( (p3-p0) * ( (p3-p1).cross(p3-p2) ) )

def tetCellVolume(cell):
    points=[]
    for i in xrange(4):
        points.append(cell.GetPoints().GetPoint(i))
    ps = primitives.pontify(points)
    return tetVolume(ps[0],ps[1],ps[2],ps[3])

# read in image and create volume actor

reader = vtk.vtkTIFFReader()
reader.SetDataExtent(0,19,0,19,0,19)
reader.SetFilePattern("/users/vrc/OOF2/TEST3D/ms_data/5color/slice%i.tif")
image = reader.GetOutput()
image.Update()

mapper = vtk.vtkFixedPointVolumeRayCastMapper()
volproperty = vtk.vtkVolumeProperty()
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

# fix annoyance with indexed image - not relevant for oof since we
# will be using the material image for this
for i in xrange(20):
    for j in xrange(20):
        for k in xrange(20):
            value = indexedImage.GetScalarComponentAsFloat(i,j,k,0)
            if value % 2 == 0:
                indexedImage.SetScalarComponentFromFloat(i,j,k,0,0)

# fix annoyance with image extent!
padder = vtk.vtkImageConstantPad()
padder.SetInput(indexedImage)
padder.SetOutputWholeExtent(0,20,0,20,0,20)
padder.SetConstant(100)
indexedImage = padder.GetOutput()
indexedImage.Update()

mapper.SetInput(indexedImage)
color = vtk.vtkColorTransferFunction()
num=lookuptable.GetNumberOfColors()
for i in (0,1,3,5,7):
    rgb = lookuptable.GetTableValue(i)
    color.AddRGBPoint(i,rgb[0],rgb[1],rgb[2])
                
volproperty.SetColor(color)
print "made indexed image"

imageBounds = indexedImage.GetExtent()
dirs=(iPoint(-1,0,0),iPoint(1,0,0),iPoint(0,-1,0),iPoint(0,1,0),iPoint(0,0,-1),iPoint(0,0,1))

poly = {0:vtk.vtkPolyData(),
        1:vtk.vtkPolyData(),
        3:vtk.vtkPolyData(),
        5:vtk.vtkPolyData(),
        7:vtk.vtkPolyData()}

faces = {0:vtk.vtkCellArray(),
         1:vtk.vtkCellArray(),
         3:vtk.vtkCellArray(),
         5:vtk.vtkCellArray(),
         7:vtk.vtkCellArray()}

scalardata = {0:vtk.vtkDoubleArray(),
              1:vtk.vtkDoubleArray(),
              3:vtk.vtkDoubleArray(),
              5:vtk.vtkDoubleArray(),
              7:vtk.vtkDoubleArray()}

vectordata = {0:vtk.vtkDoubleArray(),
              1:vtk.vtkDoubleArray(),
              3:vtk.vtkDoubleArray(),
              5:vtk.vtkDoubleArray(),
              7:vtk.vtkDoubleArray()}

normaldata = {0:vtk.vtkDoubleArray(),
              1:vtk.vtkDoubleArray(),
              3:vtk.vtkDoubleArray(),
              5:vtk.vtkDoubleArray(),
              7:vtk.vtkDoubleArray()}

for i in [0,1,3,5,7]:
    # one for the dot product, one for the area
    scalardata[i].SetNumberOfComponents(2)
    # these have 3 components for cartesian coordinates
    vectordata[i].SetNumberOfComponents(3)
    normaldata[i].SetNumberOfComponents(3)

imageGeoFilter = vtk.vtkImageDataGeometryFilter()
imageGeoFilter.SetInput(indexedImage)
imageGeoFilter.SetExtent(imageBounds)
imagePoints = imageGeoFilter.GetOutput()
imagePoints.Update()

# needed to calulate normal and area
polygon = vtk.vtkPolygon()
triangle = vtk.vtkTriangle()
normal = [0.0,0.0,0.0]
pt=[0.0,0.0,0.0]

# loop over voxels and add faces that border different pixel groups to polydata
for i in xrange(indexedImage.GetNumberOfCells()):
    voxel = indexedImage.GetCell(i)
    p = voxel.GetPoints().GetPoint(0)
    point = primitives.iPoint(p[0],p[1],p[2])
    value = indexedImage.GetScalarComponentAsFloat(point[0],point[1],point[2],0)
    for j in xrange(6):
        point2 = point+dirs[j]
        if point2[0] >= imageBounds[0] and point2[0] <= imageBounds[1]-1 and point2[1] >= imageBounds[2] and point2[1] <= imageBounds[3]-1 and point2[2] >= imageBounds[4] and point2[2] <= imageBounds[5]-1:
            value2 = indexedImage.GetScalarComponentAsFloat(point2[0],point2[1],point2[2],0)
            if value2 != value:
                # only add face for the given value, so that we don't
                # get double faces and so that the normal points
                # outward.
                face=voxel.GetFace(j)
                quadpoints = vtk.vtkPoints()
                # We have to explicity make the quad because, very annoyingly,
                # the order of points in the voxels and pixels returned by
                # vtkImageData are not compatible with the quads used for
                # polydata.
                quad=vtk.vtkQuad()
                quad.GetPointIds().SetId(0,face.GetPointIds().GetId(0))
                quad.GetPointIds().SetId(1,face.GetPointIds().GetId(1))
                quad.GetPointIds().SetId(2,face.GetPointIds().GetId(3))
                quad.GetPointIds().SetId(3,face.GetPointIds().GetId(2))
                faces[value].InsertNextCell(quad)
                for k in [0,1,3,2]:
                    face.GetPoints().GetPoint(k,pt)
                    quadpoints.InsertNextPoint(pt[0],pt[1],pt[2])
                # calculate normal
                polygon.ComputeNormal(quadpoints,normal)
                # handle roundoff!
                for k in xrange(3):
                    if(normal[k]<1e-10):
                        normal[k]==0.0
                    elif(normal[k]>(1-1e-10)):
                        normal[k]==1.0
                    elif(normal[k]<(-1+1e-10)):
                        normal[k]==1.0
                # calculate center
                center = [0.0,0.0,0.0]
                x = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
                dot = 0
                for k in xrange(4):
                    quadpoints.GetPoint(k,x[k])
                    for l in xrange(3):
                        center[l]+=x[k][l]/4
                for l in xrange(3): 
                    dot+=center[l]*normal[l]
                area = triangle.TriangleArea(x[0],x[1],x[2]) + triangle.TriangleArea(x[2],x[3],x[0])
                scalardata[value].InsertNextTuple2(area,dot)
                vectordata[value].InsertNextTuple3(center[0],center[1],center[2])
                normaldata[value].InsertNextTuple3(normal[0],normal[1],normal[2])
                

print "found material region boundaries"

polymapper = {}
polyactor = {}
tiny=0.5
for v in [0,1,3,5,7]:
    poly[v].SetPolys(faces[v])
    poly[v].SetPoints(imagePoints.GetPoints())
    poly[v].GetCellData().SetScalars(scalardata[v])
    poly[v].GetCellData().SetNormals(normaldata[v])
    poly[v].GetCellData().SetVectors(vectordata[v])

    polymapper[v]=vtk.vtkPolyDataMapper()
    polymapper[v].SetInput(poly[v])
    polyactor[v] = vtk.vtkActor()
    polyactor[v].SetMapper(polymapper[v])
    polyactor[v].GetProperty().SetRepresentationToWireframe()
    color=lookuptable.GetTableValue(v)
    polyactor[v].GetProperty().SetColor(color[0],color[1],color[2])
    polyactor[v].GetProperty().SetLineWidth(2)
    polyactor[v].GetProperty().SetAmbient(1)
    polyactor[v].GetProperty().SetDiffuse(0)
    polyactor[v].GetProperty().SetSpecular(1)
    # for boundary visualization, need to offset based on distance from origin...
    #polyactor[v].SetPosition(tiny[0]*v,tiny[1]*v,tiny[2]*v)
##     center = poly[v].GetCenter()
##     print center
##     polyactor[v].SetPosition(center[0]*tiny,center[1]*tiny,center[2]*tiny)
    #print poly[v].GetNumberOfPolys()

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

def makeTetraGrid(nCubes, flip=0):
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

                flip = not flip

            if (max_z-1)%2==0:
                flip = not flip
        if (max_y-1)%2==0:
            flip = not flip

    return meshGrid

#meshGrid = makeVoxelGrid(4)
meshGrid = makeTetraGrid(4)

# tetrahedralize the mesh
## delaunay3D = vtk.vtkDelaunay3D()
## delaunay3D.SetInput(meshGrid)
## meshGrid = delaunay3D.GetOutput()
## meshGrid.Update()
#print meshGrid
#print meshGrid.GetCell(0)



print "made mesh"
print meshGrid.GetBounds()
#numCells = meshGrid.GetNumberOfCells()
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
#[61, 140, 144, 221, 224, 300]
for i in [2]: #xrange(0,numcells):
    print "\n\n\nCELL",i
    volumes={}
    cell=meshGrid.GetCell(i)
    print "bounds = ", cell.GetBounds()
    numEdges=cell.GetNumberOfEdges()
    bounds=cell.GetBounds()

##     print "POINTS" 
##     numPts = cell.GetPoints().GetNumberOfPoints()
##     for j in xrange(numPts):
##         x = cell.GetPoints().GetPoint(j)
##         print x

    clippedpoly = {}
    clippedpolymapper = {}
    clippedpolyactor = {}
    outputgrid = {}
    outputgridmapper = {}
    outputgridactor = {}
    box = vtk.vtkBox()
    newbounds=[0,0,0,0,0,0]
    for j in xrange(len(bounds)):
        if j%2==0:
            newbounds[j]=bounds[j]-1
        else:
            newbounds[j]=bounds[j]+1
    box.SetBounds(newbounds)
    #box.SetBounds(bounds)

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
##     for j in xrange(4):
##         face = cell.GetFace(j)
##         p1 = [0,0,0]
##         for k in xrange(3):
##             p2=face.GetPoints().GetPoint(k)
##             p1[0]+=p2[0]/3
##             p1[1]+=p2[1]/3
##             p1[2]+=p2[2]/3
##         glyphpoly.GetPoints().InsertNextPoint(p1)
##         polygon.ComputeNormal(face.GetPoints(), n)
##         glyphpoly.GetPointData().GetNormals().InsertNextTuple3(n[0],n[1],n[2])


    # glyph directions of edges of a particular face
##     facenum=1
##     numEdges = cell.GetFace(facenum).GetNumberOfEdges()
##     for j in xrange(numEdges):
##         c = [0,0,0]
##         d = [0,0,0]
##         p1 = cell.GetFace(facenum).GetEdge(j).GetPoints().GetPoint(0)
##         p2 = cell.GetFace(facenum).GetEdge(j).GetPoints().GetPoint(1)
##         for k in xrange(3):
##             c[k] = (p1[k]+p2[k])/2
##             d[k] = (p2[k]-p1[k])/3
##         glyphpoly.GetPoints().InsertNextPoint(c)
##         glyphpoly.GetPointData().GetNormals().InsertNextTuple3(d[0],d[1],d[2])



    #cellVolume=(bounds[1]-bounds[0])*(bounds[3]-bounds[2])*(bounds[5]-bounds[4])
    cellVolume = tetCellVolume(cell)
    totalVolume=0
    maxVolume=0
    for j in (0,1,3,5,7):
#for j in [5]:
        #print "material",j
        thispoly = poly[j]
        clipImage = clipimage3d.ClipImage3D()
        clipImage.SetInputConnection(thispoly.GetProducerPort())
        clipImage.SetClipCell(meshGrid,i)
        clipImage.SetValue(j)
        clipImage.SetIndexedImage(indexedImage)
        outputgrid[j] = clipImage.GetOutput()
        outputgrid[j].Update()
        tmpvolume=clipImage.getVolume()
        volumes[j]=tmpvolume
        totalVolume+=tmpvolume
        if tmpvolume>maxVolume:
            maxVolume=tmpvolume


        color=lookuptable.GetTableValue(j)

        # make clipped polys for visualization
        clipper=vtk.vtkClipPolyData()
        clipper.SetClipFunction(box)
        clipper.SetInput(poly[j])
        clipper.InsideOutOn()
        clippedpoly[j]=clipper.GetOutput()
        clippedpoly[j].Update()

        clippedpolymapper[j]=vtk.vtkPolyDataMapper()
        clippedpolymapper[j].SetInput(clippedpoly[j])
        clippedpolyactor[j] = vtk.vtkActor()
        clippedpolyactor[j].SetMapper(clippedpolymapper[j])
        clippedpolyactor[j].GetProperty().SetRepresentationToWireframe()
        clippedpolyactor[j].GetProperty().SetColor(color[0],color[1],color[2])
        clippedpolyactor[j].GetProperty().SetLineWidth(2)
        clippedpolyactor[j].GetProperty().SetAmbient(1)
        clippedpolyactor[j].GetProperty().SetDiffuse(0)
        clippedpolyactor[j].GetProperty().SetSpecular(1)

        #del clipImage

    ##     for k in xrange(clippedpoly[j].GetNumberOfPolys()):
    ##         face = clippedpoly[j].GetCell(k)
    ##         p1 = [0,0,0]
    ##         num = face.GetPoints().GetNumberOfPoints()
    ##         for l in xrange(num):  
    ##             p2=face.GetPoints().GetPoint(l)
    ##             p1[0]+=p2[0]/num
    ##             p1[1]+=p2[1]/num
    ##             p1[2]+=p2[2]/num
    ##         glyphpoly.GetPoints().InsertNextPoint(p1)
    ##         polygon.ComputeNormal(face.GetPoints(), n)
    ##         print glyphpoly.GetPointData().GetNormals()
    ##         glyphpoly.GetPointData().GetNormals().InsertNextTuple3(n[0],n[1],n[2])


        # visualize output    
##         outputgridmapper[j]=vtk.vtkDataSetMapper()
##         outputgridmapper[j].SetInput(outputgrid[j])
##         outputgridactor[j] = vtk.vtkActor()
##         outputgridactor[j].SetMapper(outputgridmapper[j])
##         #outputgridactor[j].GetProperty().SetRepresentationToWireframe()
##         #print color
##         outputgridactor[j].GetProperty().SetColor(color[0],color[1],color[2])
##         #outputgridactor[j].GetProperty().SetLineWidth(2)
##         #outputgridactor[j].GetProperty().SetAmbient(1)
##         outputgridactor[j].GetProperty().SetOpacity(0.5)
##         #outputgridactor[j].GetProperty().SetDiffuse(0)
##         #outputgridactor[j].GetProperty().SetSpecular(1)


    homogeneity += maxVolume
    print i, volumes
    print totalVolume
    print cellVolume
    if(abs(totalVolume-cellVolume)/cellVolume > 1e-3 or volumes[0]<0 or
       volumes[1]<0 or volumes[3]<0 or volumes[5]<0 or volumes[7]<0):
        cellswithissues.append(i)
        print "CELLS with issues", cellswithissues

    

    
homogeneity/=microstructureVolume
print homogeneity
print cellswithissues


#glyph it to visualize normals
arrow = vtk.vtkArrowSource()
elementglyph = vtk.vtkGlyph3D()
elementglyph.SetInput(glyphpoly)
elementglyph.SetSource(arrow.GetOutput())
elementglyph.SetVectorModeToUseNormal()
glyphmapper = vtk.vtkPolyDataMapper()
glyphmapper.SetInput(elementglyph.GetOutput())
glyphactor = vtk.vtkActor()
glyphactor.SetMapper(glyphmapper)


# axes actor
axes = vtk.vtkAxesActor()
axes.SetTotalLength(2,2,2)

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

## ren.AddVolume(volume)
#ren.AddActor(wholemeshactor)
ren.AddActor(meshactor)
ren.AddActor(axes)
#ren.AddActor(glyphactor)
for v in [0,1,3,5,7]:
#for v in [5]:
    #ren.AddActor(polyactor[v])
    ren.AddActor(clippedpolyactor[v])
    #ren.AddActor(outputgridactor[v])

ren.ResetCamera()
ren.ResetCameraClippingRange()
ren.GetActiveCamera().SetFocalPoint((bounds[0]+bounds[1])/2,(bounds[2]+bounds[3])/2,(bounds[4]+bounds[5])/2)

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()
