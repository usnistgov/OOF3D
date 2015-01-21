import sys, os, types, string, random, code
#import gtk
import vtk
#from canvas3d import Canvas3D



# simplified script for messing with vtkImageData types

# this defines our image file location and size
prefix = 'mini/checkerboard6.pgm'
extent = (0,5,0,5,0,5)
## prefix = 'pgm/slice.pgm'
## extent = (0,99,0,99,0,99)

# make image reader and get image
reader = vtk.vtkPNMReader()      
reader.SetDataExtent(extent)
reader.SetFilePrefix(prefix)
reader.SetDataSpacing(1,1,1)
image = reader.GetOutput()
image.Update()
image.UpdateInformation()


# Before realizing that the FixedPointRayCastMapper (needed to render
# volumetric images with more than one component) centers pixels
# differently and cuts off one whole voxel off of 3 sides instead of a
# fraction of a voxel off of 6 sides it seemed necessary to add a
# component to the image for the alpha values.  The following code is
# one way (probably not the best) to add a constant component to an
# image.

# prepare to pad the image - copy and add component

## colorfunction = vtk.vtkLookupTable()
## colorfunction.SetTableRange(0,255)
## colorfunction.SetSaturationRange(0,0)
## colorfunction.SetHueRange(0,0)
## colorfunction.SetValueRange(1,1)
## colorfunction.Build()

## colormapper = vtk.vtkImageMapToColors()
## colormapper.SetInputConnection(image.GetProducerPort())
## colormapper.SetLookupTable(colorfunction)
## # need this so output has one component
## colormapper.SetOutputFormatToLuminance()

## alphacomponent = colormapper.GetOutput()
## alphacomponent.Update()

## # now append the new image to the original image as another component
## appender = vtk.vtkImageAppendComponents()
## appender.AddInputConnection(image.GetProducerPort())
## appender.AddInputConnection(alphacomponent.GetProducerPort())
## imagewalpha = appender.GetOutput()
## imagewalpha.Update()

## # check that all the data is the same
## for i in xrange(216):
##     v1 = imagewalpha.GetPointData().GetScalars().GetComponent(i,0)
##     v2 = image.GetPointData().GetScalars().GetComponent(i,0)
##     v3 = imagewalpha.GetPointData().GetScalars().GetComponent(i,1)
##     if v1 != v2:
##         print "NOT EQUAL"
##     if v3 != 255:
##         print "NOT OPAQUE"


# try padding the image
padder = vtk.vtkImageConstantPad()
padder.SetInput(image)
padder.SetOutputWholeExtent(0,6,0,6,0,6) # pad one voxel layer to 3 of the sides?
padder.SetConstant(255) # arbitrary
imagepadded = padder.GetOutput()
imagepadded.Update()

# FixedPointVolumeRayCastMapper can handle more than one component but
# also elimnates the need for a second component in this case.
mapper = vtk.vtkFixedPointVolumeRayCastMapper()
# must alter sample distance to be a fraction of a pixel for this
# small volume, otherwise rendering is garbled when not viewing volume
# head on.
mapper.SetSampleDistance(.05)
mapper.SetInteractiveSampleDistance(.2)
mapper.SetInput(imagepadded)

# set up color functions and property object
color =  vtk.vtkPiecewiseFunction()
color.AddSegment(0,0,255,1)

opacity = vtk.vtkPiecewiseFunction()
opacity.AddSegment(0,.5,255,1)

volproperty =  vtk.vtkVolumeProperty()
volproperty.SetColor(color)
volproperty.SetScalarOpacity(1,opacity)

# make volume actor, pass in mapper and property
volume =  vtk.vtkVolume()
volume.SetMapper(mapper)
volume.SetProperty(volproperty)
print volume

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





