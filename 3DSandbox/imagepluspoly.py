import vtk
import sys, os

#load image data
reader = vtk.vtkPNMReader()
reader.SetFilePattern("mini/checkerboard%i.pgm")
size = 5

reader.SetDataExtent(0,size,0,size,0,size)
reader.SetDataSpacing(1,1,1)
reader.SetDataScalarTypeToUnsignedChar()
image = reader.GetOutput()
image.Update()

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

#add a polydate object
cone = vtk.vtkConeSource()
cone.SetResolution(80)
cone.SetRadius(2)
cone.SetHeight(2)
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInput(cone.GetOutput())
coneActor = vtk.vtkActor()
coneActor.SetMapper(coneMapper)    
coneActor.GetProperty().SetColor(0.5, 0.5, 1.0)
ren.AddActor(coneActor)

ren.ResetCamera()
ren.ResetCameraClippingRange()

# Render the scene and start interaction.
iren.Initialize()
renWin.Render()
iren.Start()

print renWin
