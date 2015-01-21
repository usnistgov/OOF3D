import sys, os, types, string, random, code
#import gtk
import vtk
#from canvas3d import Canvas3D



# this defines our image file location and size
size = 99
#pattern = 'mini/colorchecker.jpg.%i'
pattern = 'jpeg/slice.jpg.%i'
extent = (0,size,0,size,0,size)

# make image reader and get image
reader = vtk.vtkJPEGReader()      
reader.SetDataExtent(extent)
reader.SetFilePattern(pattern)
reader.SetDataSpacing(1,1,1)
image = reader.GetOutput()
image.Update()

# add a component
extractor = vtk.vtkImageExtractComponents()
extractor.SetInput(image)
extractor.SetComponents(0)

ellipsoid = vtk.vtkImageEllipsoidSource()
ellipsoid.SetCenter(size/2,size/2,size/2)
ellipsoid.SetWholeExtent(0,size+1,0,size+1,0,size+1)
ellipsoid.SetOutputScalarTypeToUnsignedChar()
ellipsoid.SetRadius(20,30,40)
# remember that this is opacity per length, so the same value for the
# ellipsoid will seem much more transclucent than that for the outer
# portion of the cube.  What's weird is that with the inner cube set
# to 0 (totally opaque) and the outer cube set to something like 220,
# we get the expected effect.  But with the inner cube set to slightly
# translucent, about 10, the outer cube disappears.  When the values
# are too close, everything disappears.

# This is because we cannot have intermixing translucent
# geometries.  If one portion is translucent, the other portion must
# be either fully transparent or fully opaque.

# A side effect of this feature seems to be that if the fourth
# component is a constant, the mapper decides the whole thing is
# translucent.  Our trick around this is to set the padding voxels to
# have a value of 255 in the alpha channel, representing total
# transparency while the rest of the fourth channel is set to be
# totally opaque, until we decide to mess with it.
ellipsoid.SetInValue(100)
ellipsoid.SetOutValue(255)

# Testing if a smoothly varying translucency works.  Seems to, to an extent.
smoother = vtk.vtkImageGaussianSmooth()
smoother.SetInput(ellipsoid.GetOutput())
smoother.SetRadiusFactors(50,50,50)
smoother.SetStandardDeviation(5,5,5)
smoother.SetDimensionality(3)

appender = vtk.vtkImageAppendComponents()
appender.AddInput(image)
#appender.AddInput(extractor.GetOutput())
#appender.AddInput(ellipsoid.GetOutput())
appender.AddInput(smoother.GetOutput())
image4comp = appender.GetOutput()
image4comp.Update()
#image4comp = imagepadded

# when we fill the fourth component "IndependentComponentsOff"
# rendering no longer works. On the other hand, we can't get opacity
# to work at all with "IndependentComponentsOn"
image4comp.GetPointData().GetScalars().FillComponent(3,0)

print image4comp.GetScalarComponentAsFloat(50,50,50,3)
print image4comp.GetScalarComponentAsFloat(5,5,5,3)


# try padding the image
padder = vtk.vtkImageConstantPad()
padder.SetInput(image4comp)
padder.SetOutputWholeExtent(0,size+1,0,size+1,0,size+1) # pad one voxel layer to 3 of the sides?
padder.SetConstant(255) 
# arbitrary except we want it to be different from the value in the
# alpha component that represents total opacity
imagepadded = padder.GetOutput()
imagepadded.Update()



mapper = vtk.vtkFixedPointVolumeRayCastMapper()
mapper.SetSampleDistance(.2)
mapper.SetInteractiveSampleDistance(4)
mapper.SetInput(imagepadded)


red = vtk.vtkColorTransferFunction()
red.AddRGBSegment(0,0,0,0,255,1,0,0)
green = vtk.vtkColorTransferFunction()
green.AddRGBSegment(0,0,0,0,255,0,1,0)
blue = vtk.vtkColorTransferFunction()
blue.AddRGBSegment(0,0,0,0,255,0,0,1)
opacity = vtk.vtkPiecewiseFunction()
# it seems to work better when we reverse the direction of the opacity
opacity.AddSegment(0,1,255,0)
#gradientopacity = vtk.vtkPiecewiseFunction()
#gradientopacity.AddSegment(0,1,255,1)


volproperty =  vtk.vtkVolumeProperty()
# volproperty.SetColor(0,red)
# volproperty.SetColor(1,green)
# volproperty.SetColor(2,blue)
volproperty.SetScalarOpacity(opacity)
volproperty.IndependentComponentsOff()

# none of the stuff we do with gradient opacity seems to make a
# difference
#volproperty.SetGradientOpacity(3,gradientopacity)
#volproperty.SetScalarOpacityUnitDistance(0,10)
#volproperty.SetScalarOpacityUnitDistance(1,10)
#volproperty.SetScalarOpacityUnitDistance(2,10)
#volproperty.SetScalarOpacityUnitDistance(3,10)
#volproperty.DisableGradientOpacityOn()
#volproperty.DisableGradientOpacityOn(1)
#volproperty.DisableGradientOpacityOn(2)
#volproperty.DisableGradientOpacityOn(3)

for i in xrange(4):
    print i, volproperty.GetColorChannels(i)
    print volproperty.GetScalarOpacityUnitDistance(i)
    print volproperty.GetDisableGradientOpacity(i)
    
print mapper.GetGradientOpacityRequired()

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








