import vtk
import sys, os

import oof3d
sys.path.append(os.path.dirname(oof3d.__file__))

from ooflib.SWIG.engine import clipimage3d



# read in image and create volume actor

reader = vtk.vtkTIFFReader()
reader.SetDataExtent(0,19,0,19,0,19)
reader.SetFilePattern("/users/vrc/OOF2/TEST3D/ms_data/5color/slice%i.tif")
image = reader.GetOutput()
image.Update()

mapper = vtk.vtkFixedPointVolumeRayCastMapper()
#mapper.SetInput(image)
volproperty = vtk.vtkVolumeProperty()
#volproperty.IndependentComponentsOff()
#red = vtk.vtkColorTransferFunction()
#red.Set
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

# fix annoyance with indexed image
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
    print i, rgb
    color.AddRGBPoint(i,rgb[0],rgb[1],rgb[2])
                
volproperty.SetColor(color)
#print "made indexed image"

marchingCubes = vtk.vtkMarchingCubes()
marchingCubes.SetInput(indexedImage)
#marchingCubes.SetNumberOfContours(5)
for i in (0,1,3,5,7):
    marchingCubes.SetValue(i,i)

poly = marchingCubes.GetOutput()
poly.Update()
print poly

polymapper = vtk.vtkPolyDataMapper()
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

ren.AddVolume(volume)
ren.AddActor(polyactor)

ren.ResetCamera()
ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()
