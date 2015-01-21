import vtk
import sys, os
from math import *

import oof3d
sys.path.append(os.path.dirname(oof3d.__file__))

from ooflib.SWIG.engine import clipimage3d
from ooflib.common import primitives

# this script is to test whether the vtkCutter preserves the normals
# (sense of in and out).

# moral of the story: the vtkCutter orients the edges in a way that is
# consistent and convenient for our purposes.  The edges are always
# counterclockwise around the material in question, relative to the
# normal vector of the cutting plane.  This is good.


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

imageGeoFilter = vtk.vtkImageDataGeometryFilter()
imageGeoFilter.SetInput(indexedImage)
imageGeoFilter.SetExtent(imageBounds)
imagePoints = imageGeoFilter.GetOutput()
imagePoints.Update()

# loop over voxels and add faces that border different pixel groups to polydata
for i in xrange(indexedImage.GetNumberOfCells()):
    voxel = indexedImage.GetCell(i)
    p = voxel.GetPoints().GetPoint(0)
    point = primitives.iPoint(p[0],p[1],p[2])
    value = indexedImage.GetScalarComponentAsFloat(point[0],point[1],point[2],0)
    for j in xrange(6):
        face=voxel.GetFace(j)
        # We have to explicity make the quad because, very annoyingly,
        # the order of points in the voxels and pixels returned by
        # vtkImageData are not compatible with the quads used for
        # polydata.
        quad=vtk.vtkQuad()
        quad.GetPointIds().SetId(0,face.GetPointIds().GetId(0))
        quad.GetPointIds().SetId(1,face.GetPointIds().GetId(1))
        quad.GetPointIds().SetId(2,face.GetPointIds().GetId(3))
        quad.GetPointIds().SetId(3,face.GetPointIds().GetId(2))
        point2 = point+dirs[j] 
        if point2[0] >= imageBounds[0] and point2[0] <= imageBounds[1] and point2[1] >= imageBounds[2] and point2[1] <= imageBounds[3] and point2[2] >= imageBounds[4] and point2[2] <= imageBounds[5]:
            value2 = indexedImage.GetScalarComponentAsFloat(point2[0],point2[1],point2[2],0)
            if value2 != value:
                # only add face for the given value, so that we don't
                # get double faces and so that the normal points
                # outward.
                faces[value].InsertNextCell(quad)

print "found material region boundaries"

polymapper = {}
polyactor = {}
tiny=0.5
for v in [0,1,3,5,7]:
    poly[v].SetPolys(faces[v])
    poly[v].SetPoints(imagePoints.GetPoints())

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


# cut the polys by a plane
plane = vtk.vtkPlane()
plane.SetNormal(0,1,0)
plane.SetOrigin(0,5,0)
cutpoly = {}
cutpolymapper = {}
cutpolyactor = {}
for v in [0,1,3,5,7]:
    cutter = vtk.vtkCutter()
    cutter.SetInput(poly[v])
    cutter.SetCutFunction(plane)
    cutpoly[v] = cutter.GetOutput()
    
    cutpolymapper[v]=vtk.vtkPolyDataMapper()
    cutpolymapper[v].SetInput(cutpoly[v])
    cutpolyactor[v] = vtk.vtkActor()
    cutpolyactor[v].SetMapper(cutpolymapper[v])
    cutpolyactor[v].GetProperty().SetRepresentationToWireframe()
    color=lookuptable.GetTableValue(v)
    cutpolyactor[v].GetProperty().SetColor(color[0],color[1],color[2])
    cutpolyactor[v].GetProperty().SetLineWidth(1)
    cutpolyactor[v].GetProperty().SetAmbient(1)
    cutpolyactor[v].GetProperty().SetDiffuse(0)
    cutpolyactor[v].GetProperty().SetSpecular(1)


# find centers and directions of edges for glyphing
polygon = vtk.vtkPolygon()
d = [0,0,0]
p1 = [0,0,0]
p2 = [0,0,0]
c = [0,0,0]
glyphpoly={}
glyphmapper = {}
glyphactor = {}
for v in [0,1,3,5,7]:
    glyphpoly[v] = vtk.vtkPolyData()
    glyphpoly[v].Allocate(1000,1000)
    points = vtk.vtkPoints()
    glyphpoly[v].SetPoints(points)
    normalarray = vtk.vtkDoubleArray()
    normalarray.SetNumberOfComponents(3)
    glyphpoly[v].GetPointData().SetVectors(normalarray)
    cutpoly[v].Update()
    numEdges = cutpoly[v].GetNumberOfCells()
    for j in xrange(numEdges):
        edge = cutpoly[v].GetCell(j)
        p1 = edge.GetPoints().GetPoint(0)
        p2 = edge.GetPoints().GetPoint(1)
        d = [p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]
        c = [(p2[0]+p1[0])/2,(p2[1]+p1[1])/2,(p2[2]+p1[2])/2]
        glyphpoly[v].GetPoints().InsertNextPoint(p1)
        glyphpoly[v].GetPointData().GetVectors().InsertNextTuple3(d[0],d[1],d[2])

    #glyph it to visualize normals
    glyphpoly[v].Update()
    arrow = vtk.vtkArrowSource()
    elementglyph = vtk.vtkGlyph3D()
    elementglyph.SetInput(glyphpoly[v])
    elementglyph.SetSource(arrow.GetOutput())
    elementglyph.SetVectorModeToUseVector()
    glyphmapper[v] = vtk.vtkPolyDataMapper()
    glyphmapper[v].SetInput(elementglyph.GetOutput())
    glyphactor[v] = vtk.vtkActor()
    glyphactor[v].SetMapper(glyphmapper[v])

    color=lookuptable.GetTableValue(v)
    glyphactor[v].GetProperty().SetColor(color[0],color[1],color[2])
    glyphactor[v].GetProperty().SetLineWidth(2)
    glyphactor[v].GetProperty().SetAmbient(1)
    glyphactor[v].GetProperty().SetDiffuse(0)
    glyphactor[v].GetProperty().SetSpecular(1)


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

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
#ren.SetBackground(.5, .5, .5)

#ren.AddVolume(volume)
ren.AddActor(axes)
#for v in [0,1,3,5,7]:
for v in [0,1,3,7]:
    ren.AddActor(glyphactor[v])
##     #ren.AddActor(polyactor[v])
    ren.AddActor(cutpolyactor[v])

ren.ResetCamera()
ren.ResetCameraClippingRange()
#ren.GetActiveCamera().SetFocalPoint((bounds[0]+bounds[1])/2,(bounds[2]+bounds[3])/2,(bounds[4]+bounds[5])/2)

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()
