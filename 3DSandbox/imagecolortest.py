import sys, os, types, string, random, code
#import gtk
import vtk
#from canvas3d import Canvas3D



# this defines our image file location and size
prefix = 'mini/colorchecker.jpg'
extent = (0,4,0,4,0,4)

# make image reader and get image
reader = vtk.vtkJPEGReader()      
reader.SetDataExtent(extent)
reader.SetFilePrefix(prefix)
reader.SetDataSpacing(1,1,1)
image = reader.GetOutput()
image.Update()


# try padding the image
padder = vtk.vtkImageConstantPad()
padder.SetInput(image)
padder.SetOutputWholeExtent(0,5,0,5,0,5) # pad one voxel layer to 3 of the sides?
padder.SetConstant(255) # arbitrary
imagepadded = padder.GetOutput()
imagepadded.Update()
print imagepadded
print imagepadded.GetNumberOfScalarComponents()

mapper = vtk.vtkFixedPointVolumeRayCastMapper()
mapper.SetSampleDistance(.05)
mapper.SetInteractiveSampleDistance(.2)
mapper.SetInput(imagepadded)

red = vtk.vtkColorTransferFunction()
red.AddRGBSegment(0,0,0,0,255,1,0,0)
green = vtk.vtkColorTransferFunction()
green.AddRGBSegment(0,0,0,0,255,0,1,0)
blue = vtk.vtkColorTransferFunction()
blue.AddRGBSegment(0,0,0,0,255,0,0,1)

volproperty =  vtk.vtkVolumeProperty()
volproperty.SetColor(0,red)
volproperty.SetColor(1,green)
volproperty.SetColor(2,blue)

# make volume actor, pass in mapper and property
volume =  vtk.vtkVolume()
volume.SetMapper(mapper)
volume.SetProperty(volproperty)

# make renderer and render window
ren =  vtk.vtkRenderer()
ren.AddActor(volume)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(300,300)
renWin.AddRenderer(ren)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iren.Initialize()
iren.Start()








