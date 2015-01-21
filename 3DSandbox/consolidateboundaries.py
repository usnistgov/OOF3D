import vtk
import sys, os
from math import *

import oof3d
sys.path.append(os.path.dirname(oof3d.__file__))
from ooflib.common import primitives

# read in image and create volume actor

reader = vtk.vtkTIFFReader()
size=19
reader.SetFilePattern("/users/vrc/OOF2/TEST3D/ms_data/5color/slice%i.tif")
#size=99
#reader.SetFilePattern("5color100/slice%i.tif")
reader.SetDataExtent(0,size,0,size,0,size)
image = reader.GetOutput()
image.Update()
#print image


# for some reason on the mac, the tiff reader gives us a four
# component image - doesn't unless we are using QuantizeRGBToIndex
extract = vtk.vtkImageExtractComponents()
extract.SetInput(image)
extract.SetComponents(0,1,2)
image = extract.GetOutput()
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
#print lookuptable


x0 = 0
y0 = 0
z0 = 0

#clip image so we can reasonably look at it
## clipper = vtk.vtkImageClip()
## clipper.SetInput(indexedImage)
## newsize = 50
## x0 = 0
## y0 = 0
## z0 = 0
## clipper.SetOutputWholeExtent(x0,x0+newsize,y0,y0+newsize,z0,z0+newsize)
## clipper.ClipDataOn()
## translator = vtk.vtkImageTranslateExtent()
## translator.SetInput(clipper.GetOutput())
## translator.SetTranslation(-x0,-y0,-z0)
## indexedImage = translator.GetOutput()
## indexedImage.Update()
## size = newsize
## print indexedImage.GetExtent()
## print indexedImage.GetNumberOfCells()


#for i in xrange(256):
#    print i,lookuptable.GetTableValue(i)


#fix annoyance with indexed image - not relevant for oof since we
#will be using the material image for this
indexlist = []
for i in xrange(size+1):
    for j in xrange(size+1):
        for k in xrange(size+1):
            value = int(indexedImage.GetScalarComponentAsFloat(i,j,k,0))
            if value not in indexlist:
                indexlist.append(value)
                #indexedImage.SetScalarComponentFromFloat(i,j,k,0,indexlist[0])

indexlist.sort()
print indexlist
#sys.exit()


# fix annoyance with image extent!
padder = vtk.vtkImageConstantPad()
padder.SetInput(indexedImage)
padder.SetOutputWholeExtent(0,size+1,0,size+1,0,size+1)
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

poly={}
faces={}
scalardata={}
vectordata={}
normaldata={}
for i in indexlist:
    poly[i] = vtk.vtkPolyData()
    faces[i] = vtk.vtkCellArray()
    scalardata[i] = vtk.vtkDoubleArray()
    vectordata[i] = vtk.vtkDoubleArray()
    normaldata[i] = vtk.vtkDoubleArray()
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
    point = primitives.iPoint(p[0]-x0,p[1]-y0,p[2]-z0)
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
                        normal[k]==-1.0
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
##                 area = triangle.TriangleArea(x[0],x[1],x[2]) + triangle.TriangleArea(x[2],x[3],x[0])
##                 scalardata[value].InsertNextTuple2(area,dot)
##                 vectordata[value].InsertNextTuple3(center[0],center[1],center[2])
##                 normaldata[value].InsertNextTuple3(normal[0],normal[1],normal[2])
                

print "found material region boundaries"

polymapper = {}
polyactor = {}
tiny=0.5
totalpolys = 0
for v in indexlist:
    poly[v].SetPolys(faces[v])
    poly[v].SetPoints(imagePoints.GetPoints())
##     poly[v].GetCellData().SetScalars(scalardata[v])
##     poly[v].GetCellData().SetNormals(normaldata[v])
##     poly[v].GetCellData().SetVectors(vectordata[v])

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
    polyactor[v].SetPosition(tiny*v,tiny*v,tiny*v)
    center = poly[v].GetCenter()
    polyactor[v].SetPosition(center[0]*tiny,center[1]*tiny,center[2]*tiny)
    print v, poly[v].GetNumberOfPolys()
    totalpolys += poly[v].GetNumberOfPolys()


def GetFacesInPlane(poly, coord, value):
    numcells = poly.GetNumberOfPolys()
    newPoints = vtk.vtkPoints()
    newPoints.DeepCopy(poly.GetPoints())
    polysInPlane = vtk.vtkPolyData()
    polysInPlane.Allocate(1000,1000)
    polysInPlane.SetPoints(newPoints)
    x=[0,0,0]
    for i in xrange(numcells):
        cell = poly.GetCell(i)
        inPlane = True
        for j in range(4):
            cell.GetPoints().GetPoint(j,x)
            inPlane &= ( x[coord] == value )
        if inPlane:
            polysInPlane.InsertNextCell(cell.GetCellType(),cell.GetPointIds())

    cleaner = vtk.vtkCleanPolyData()
    cleaner.SetInput(polysInPlane)
    polysInPlane = cleaner.GetOutput()
    polysInPlane.Squeeze()
    polysInPlane.Update()
    return polysInPlane
            

def SimpleFindStrips(poly, coord):
    # Just do the cells in their given order
    # This method reduces the number of polys in the 20x20x20 by a factor of 3.623
    # reduces the number of polys in the 100x100x100 by 2.216
    #dirs=[0,1,2]
    #dirs.remove(coord)
    bounds = poly.GetBounds()
    numCells = poly.GetNumberOfCells()
    current = vtk.vtkGenericCell()
    newcell = vtk.vtkGenericCell()
    poly.GetCell(0, current)
    sharedpts = vtk.vtkIdList()
    sharedpts.DeepCopy(current.GetPointIds())
    newPoints = vtk.vtkPoints()
    newPoints.DeepCopy(poly.GetPoints())
    consolidatedpoly = vtk.vtkPolyData()
    consolidatedpoly.Allocate(1000,1000)
    consolidatedpoly.SetPoints(newPoints)
    x = [0,0,0]
    for i in xrange(1,numCells):
        poly.GetCell(i, newcell)
        # check if this cell shares an edge
        sharedpts.IntersectWith(newcell.GetPointIds())
        # if they share an edge, the current cell becomes the union of the 2 cells
        if sharedpts.GetNumberOfIds() == 2:
            quad = vtk.vtkQuad()
            ptIds = []
            for j in xrange(4):
                if sharedpts.IsId(current.GetPointIds().GetId(j)) == -1:
                    ptIds.append(j)
            if ptIds == [0,3]: ptIds.reverse()
            current.GetPoints().GetPoint(ptIds[0],x)
            quad.GetPointIds().InsertId(0,current.GetPointIds().GetId(ptIds[0]))
            quad.GetPoints().InsertPoint(0,x)
            current.GetPoints().GetPoint(ptIds[1],x)
            quad.GetPointIds().InsertId(1,current.GetPointIds().GetId(ptIds[1]))
            quad.GetPoints().InsertPoint(1,x)

            ptIds = []
            for j in xrange(4):
                if sharedpts.IsId(newcell.GetPointIds().GetId(j)) == -1:
                    ptIds.append(j)
            if ptIds == [0,3]: ptIds.reverse()
            newcell.GetPoints().GetPoint(ptIds[0],x)
            quad.GetPointIds().InsertId(2,newcell.GetPointIds().GetId(ptIds[0]))
            quad.GetPoints().InsertPoint(2,x)
            newcell.GetPoints().GetPoint(ptIds[1],x)
            quad.GetPointIds().InsertId(3,newcell.GetPointIds().GetId(ptIds[1]))
            quad.GetPoints().InsertPoint(3,x)

            current.DeepCopy(quad)
            #consolidatedpoly.InsertNextCell(current.GetCellType(),current.GetPointIds())
        else:
            consolidatedpoly.InsertNextCell(current.GetCellType(),current.GetPointIds())
            current.DeepCopy(newcell)
        sharedpts.DeepCopy(current.GetPointIds())

    consolidatedpoly.InsertNextCell(current.GetCellType(),current.GetPointIds())
    cleaner = vtk.vtkCleanPolyData()
    cleaner.SetInput(consolidatedpoly)
    consolidatedpoly = cleaner.GetOutput()
    consolidatedpoly.Squeeze()
    consolidatedpoly.Update()
    return consolidatedpoly


def GetWholeConnectedRegions(poly, coord):
    # for each of the connected regions, make a (likely non-convex)
    # whole polygon, divided at the self intersections.
    # for small image, reduces by 4.975
    # big image improves by 3.918
    numCells = poly.GetNumberOfCells()
    #print "numcells before", numCells
    connectivity = vtk.vtkPolyDataConnectivityFilter()
    connectivity.SetInput(poly)
    connectivity.SetExtractionModeToAllRegions()
    connectivity.Update()
    numRegions = connectivity.GetNumberOfExtractedRegions()
    connectivity.SetExtractionModeToSpecifiedRegions()
    featureEdges = vtk.vtkFeatureEdges()
    featureEdges.BoundaryEdgesOn()

    numResult = 0
    for r in range(numRegions):
        numResult += 1
        connectivity.InitializeSpecifiedRegionList()
        connectivity.AddSpecifiedRegion(r)
        region = connectivity.GetOutput()
        region.Update()
        #print "region has ", region.GetNumberOfCells(), " cells"
        featureEdges.SetInput(region)
        edges = featureEdges.GetOutput()
        edges.Update()
        edges.BuildLinks(0)
        #print "edges has", edges.GetNumberOfCells(), " cells"
        numCells = edges.GetNumberOfCells()
        # for i in xrange(numCells):
        #     print edges.GetCell(i).GetPoints().GetPoint(0), edges.GetCell(i).GetPoints().GetPoint(1)
        # edges not given in order, we need to traverse
        # first look for self intersections
        points = edges.GetPoints()
        selfIntersections = []
        cellIds = vtk.vtkIdList()
        for p in range(points.GetNumberOfPoints()):
            edges.GetPointCells(p,cellIds)
            if cellIds.GetNumberOfIds() == 4:
                selfIntersections.append(p)
                numResult += 1
        #print selfIntersections
##         if not selfIntersections:
##             selfIntersections.append(edges.GetCell(0).GetPointIds().GetId(0))
        
        # for now just return number of cells in result
    return numResult

##     newPoints = vtk.vtkPoints()
##     newPoints.DeepCopy(poly.GetPoints())
##     consolidatedpoly = vtk.vtkPolyData()
##     consolidatedpoly.Allocate(1000,1000)
##     consolidatedpoly.SetPoints(newPoints)

##     cleaner = vtk.vtkCleanPolyData()
##     cleaner.SetInput(consolidatedpoly)
##     consolidatedpoly = cleaner.GetOutput()
##     consolidatedpoly.Squeeze()
##     consolidatedpoly.Update()
##     return consolidatedpoly
        

# now try to consolidate
norms = [[1,0,0],[0,1,0],[0,0,1]]

newpoly = {}
newpolymapper = {}
newpolyactor = {}
totalpolys2 = 0

for v in indexlist:
    #print "consolidating",v
    appender = vtk.vtkAppendPolyData()
    
    for coord in range(3):
        #print "coord",coord
        for p in xrange(1,size+1):
            #print "plane",p
##             cutter = vtk.vtkCutter()
##             plane = vtk.vtkPlane()
##             plane.SetNormal(norms[coord])
##             origin = [norms[coord][0]*p,norms[coord][1]*p,norms[coord][2]*p]
##             plane.SetOrigin(origin)


##             # the cutter is not actually what we want.  It finds the
##             # intersection of the polydata with the plane, but this
##             # can return something even if there are no whole faces in
##             # that plane.  We want the whole faces so that we can
##             # group them into larger rectangles.
##             cutter.SetInput(poly[v])
##             cutter.SetCutFunction(plane)
##             cutpoly = cutter.GetOutput()
##             cutpoly.Update()

            cutpoly = GetFacesInPlane(poly[v],coord,p)
            #print cutpoly
##            for i in xrange(cutpoly.GetNumberOfPolys()):
##                print cutpoly.GetCell(i).GetBounds()
            
            cutpolymapper = vtk.vtkPolyDataMapper()
            cutpolymapper.SetInput(cutpoly)
            cutpolyactor = vtk.vtkActor()
            cutpolyactor.SetMapper(cutpolymapper)
            cutpolyactor.GetProperty().SetRepresentationToWireframe()
            cutpolyactor.GetProperty().SetLineWidth(2)
            cutpolyactor.GetProperty().SetAmbient(1)
            cutpolyactor.GetProperty().SetDiffuse(0)
            cutpolyactor.GetProperty().SetSpecular(1)
            color=lookuptable.GetTableValue(v)
            cutpolyactor.GetProperty().SetColor(color[0],color[1],color[2])

            consolidatedpoly = SimpleFindStrips(cutpoly, coord)
            # totalpolys2 +=  GetWholeConnectedRegions(cutpoly, coord)
            # consolidatedpoly = GetWholeConnectedRegions(cutpoly, coord)
            consolidatedpolymapper = vtk.vtkPolyDataMapper()
            consolidatedpolymapper.SetInput(consolidatedpoly)
            consolidatedpolyactor = vtk.vtkActor()
            consolidatedpolyactor.SetMapper(consolidatedpolymapper)
            consolidatedpolyactor.GetProperty().SetRepresentationToWireframe()
            consolidatedpolyactor.GetProperty().SetLineWidth(2)
            consolidatedpolyactor.GetProperty().SetAmbient(1)
            consolidatedpolyactor.GetProperty().SetDiffuse(0)
            consolidatedpolyactor.GetProperty().SetSpecular(1)
            color=lookuptable.GetTableValue(v)
            consolidatedpolyactor.GetProperty().SetColor(color[0],color[1],color[2])

            appender.AddInput(consolidatedpoly)
            #print coord, p, cutpoly.GetNumberOfPolys(), consolidatedpoly.GetNumberOfPolys()

    #print "numpolys", v, totalpolys2
    newpoly[v] = appender.GetOutput()
    newpoly[v].Update()
    print "appendedpoly", v, newpoly[v].GetNumberOfPolys()
    totalpolys2 += newpoly[v].GetNumberOfPolys()
    
    newpolymapper[v]=vtk.vtkPolyDataMapper()
    newpolymapper[v].SetInput(newpoly[v])
    newpolyactor[v] = vtk.vtkActor()
    newpolyactor[v].SetMapper(newpolymapper[v])
    newpolyactor[v].GetProperty().SetRepresentationToWireframe()
    color=lookuptable.GetTableValue(v)
    newpolyactor[v].GetProperty().SetColor(color[0],color[1],color[2])
    newpolyactor[v].GetProperty().SetLineWidth(2)
    newpolyactor[v].GetProperty().SetAmbient(1)
    newpolyactor[v].GetProperty().SetDiffuse(0)
    newpolyactor[v].GetProperty().SetSpecular(1)
    # for boundary visualization, need to offset based on distance from origin...
    newpolyactor[v].SetPosition(tiny*v,tiny*v,tiny*v)
    center = newpoly[v].GetCenter()
    newpolyactor[v].SetPosition(center[0]*tiny,center[1]*tiny,center[2]*tiny)

if totalpolys2:
    print "POLYS REDUCED BY FACTOR OF", float(totalpolys)/totalpolys2
    

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

#ren.AddActor(cutpolyactor)
ren.AddActor(consolidatedpolyactor)
ren.AddActor(axes)

##for v in [5]: #indexlist:
####      #ren.AddActor(polyactor[v])
##    ren.AddActor(newpolyactor[v])

ren.ResetCamera()
ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()











