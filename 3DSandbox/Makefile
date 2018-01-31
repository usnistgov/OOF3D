CXX = clang++
#CXX = g++

#VTKDIR = /Users/langer
VTKDIR = /usr/local
VTK = 9.0

CFLAGS = -I$(VTKDIR)/include/vtk-$(VTK) -g -I/opt/local/include -std=c++11 -Wno-inconsistent-missing-override

VTKLIBS= -L$(VTKDIR)/lib -lvtkCommonCore-$(VTK) -lvtkCommonDataModel-$(VTK) -lvtkCommonExecutionModel-$(VTK) -lvtkCommonMisc-$(VTK) -lvtkCommonTransforms-$(VTK) -lvtkFiltersCore-$(VTK) -lvtkFiltersExtraction-$(VTK) -lvtkFiltersGeneral-$(VTK) -lvtkFiltersModeling-$(VTK) -lvtkFiltersSources-$(VTK) -lvtkIOImage-$(VTK) -lvtkIOXML-$(VTK) -lvtkImagingColor-$(VTK) -lvtkImagingCore-$(VTK) -lvtkImagingGeneral-$(VTK) -lvtkRenderingAnnotation-$(VTK) -lvtkRenderingContextOpenGL2-$(VTK) -lvtkRenderingCore-$(VTK) -lvtkRenderingFreeType-$(VTK) -lvtkRenderingOpenGL2-$(VTK) -lvtkRenderingVolumeOpenGL2-$(VTK) -lvtkInteractionStyle-$(VTK)

#VTKLIBS = -L$(VTKDIR)/lib/ -lvtkCommonCore-$(VTK) -lvtkIO -lvtkFiltering -lvtkRendering -lvtkVolumeRendering -lvtkGraphics -lvtkRendering -lvtkHybrid -lvtkImaging -lvtkWidgets

.C.o:
	$(CXX) $(CFLAGS) -c $<

tetsandcubes: tetsandcubes.o
	$(CXX) -o tetsandcubes tetsandcubes.o $(VTKLIBS)


readppm: readppm.o
	$(CXX) -o readppm readppm.o $(VTKLIBS)

polyimage: polyimage.o
	$(CXX) -o polyimage polyimage.o $(VTKLIBS)

rectgrid: rectgrid.o
	$(CXX) -o rectgrid rectgrid.o $(VTKLIBS)

contours3: contours3.o
	$(CXX) -o contours3 contours3.o $(VTKLIBS)

contours2: contours2.o
	$(CXX) -o contours2 contours2.o $(VTKLIBS)

contours: contours.o
	$(CXX) -o contours contours.o $(VTKLIBS)

RFILES = replaceimage.o oofImageTogrid.o oofOverlayVoxels.o
replaceimage: $(RFILES)
	$(CXX) -o replaceimage $(RFILES) $(VTKLIBS)

replaceimage3: replaceimage3.o oofImageTogrid.o
	$(CXX) -o replaceimage3 replaceimage3.o oofImageTogrid.o $(VTKLIBS)

OFILES = rectimage.o oofImageToGrid.o oofOverlayVoxels.o oofExcludeVoxels.o
rectimage: $(OFILES)
	$(CXX) -o rectimage $(OFILES) $(VTKLIBS)

cliptet: cliptet.o
	$(CXX) -o cliptet cliptet.o $(VTKLIBS)

replaceLUT: replaceLUT.o
	$(CXX) -o replaceLUT replaceLUT.o $(VTKLIBS)

fillcell: fillcell.o
	$(CXX) -o fillcell fillcell.o $(VTKLIBS)

renderTranslucent: renderTranslucent.o
	$(CXX) -o renderTranslucent renderTranslucent.o $(VTKLIBS)

clipImage: clipImage.o
	$(CXX) -o clipImage clipImage.o $(VTKLIBS)
clipImage2: clipImage2.o
	$(CXX) -o clipImage2 clipImage2.o $(VTKLIBS)

CorrectlyRenderTranslucentGeometry: CorrectlyRenderTranslucentGeometry.o
	$(CXX) -o CorrectlyRenderTranslucentGeometry CorrectlyRenderTranslucentGeometry.o $(VTKLIBS)

Rendering_Testing_Cxx_TestAreaSelections: Rendering_Testing_Cxx_TestAreaSelections.o
	$(CXX) -o Rendering_Testing_Cxx_TestAreaSelections Rendering_Testing_Cxx_TestAreaSelections.o $(VTKLIBS)

depend:
	makedepend $(CFLAGS) *.C

# DO NOT DELETE THIS LINE -- make depend depends on it.
