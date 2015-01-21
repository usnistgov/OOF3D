import vtk
import sys, os
from math import *

# just a simple script to load and display an image

#reader = vtk.vtkTIFFReader()
#reader.SetFilePattern("5color100/slice%i.tif")

#reader = vtk.vtkJPEGReader()
#reader.SetFilePattern("jpeg/slice.jpg.%i")
#size=99

reader = vtk.vtkPNMReader()
reader.SetFilePattern("mini/checkerboard%i.pgm")
size = 5

reader.SetDataExtent(0,size,0,size,0,size)
reader.SetDataSpacing(1,1,1)
reader.SetDataScalarTypeToUnsignedChar()
image = reader.GetOutput()
image.Update()
print image.GetNumberOfScalarComponents()
print image.GetScalarTypeAsString()

# add a channel
# extractor = vtk.vtkImageExtractComponents()
# extractor.SetInput(image)
# extractor.SetComponents(2)
# appender = vtk.vtkImageAppendComponents()
# appender.AddInput(image)
# appender.AddInput(extractor.GetOutput())
# image = appender.GetOutput()
# image.Update()
# image.GetPointData().GetScalars().FillComponent(3,255)
# image.Update()
# print image.GetNumberOfScalarComponents()

mapper = vtk.vtkFixedPointVolumeRayCastMapper()
mapper.SetInput(image)
if size < 20:
    mapper.SetSampleDistance(float(size)/1000)
    mapper.SetInteractiveSampleDistance(float(size)/500)
volproperty = vtk.vtkVolumeProperty()
color = vtk.vtkPiecewiseFunction()
color.AddSegment(0,0,255,1)
volproperty.SetColor(0,color)
volume = vtk.vtkVolume()
volume.SetMapper(mapper)
volume.SetProperty(volproperty)


ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(600, 600)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
ren.SetBackground(.5, .5, .5)

ren.AddActor(volume)

ren.ResetCamera()
ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()
