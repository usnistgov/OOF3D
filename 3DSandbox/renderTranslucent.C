
// This file started out as a copy of the vtk example program
// CorrectlyRenderTranslucentGeometry.C, which draws translucent
// spheres using Depth Peeling, if available.  It's not available on
// OS X (or at least on my Mac) so the part of the code that decides
// how to render the translucent bits has been removed.


#include <vtkActor.h>
#include <vtkAlgorithm.h>
#include <vtkAlgorithmOutput.h>
#include <vtkAppendPolyData.h>
#include <vtkAxesActor.h>
#include <vtkCamera.h>
#include <vtkDataSetMapper.h>
#include <vtkFixedPointVolumeRayCastMapper.h>
#include <vtkImageAppendComponents.h>
#include <vtkImageChangeInformation.h>
#include <vtkImageConstantPad.h>
#include <vtkImageData.h>
#include <vtkImageExtractComponents.h>
#include <vtkImageReader2.h>
#include <vtkImageReader2Factory.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkOpenGLRenderer.h>
#include <vtkPiecewiseFunction.h>
#include <vtkPointData.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkSphereSource.h>
#include <vtkStringArray.h>
#include <vtkTimerLog.h>
#include <vtkTransform.h>
#include <vtkUnstructuredGrid.h>
#include <vtkVolume.h>
#include <vtkVolumeProperty.h>
#include <vtkXOpenGLRenderWindow.h>

#include <vtkCaptionActor2d.h>
#include <vtkAnnotatedCubeActor.h>
#include <vtkTextProperty.h>
#include <vtkOrientationMarkerWidget.h>

#include <vtkExtractEdges.h>

#include <assert.h>
#include <dirent.h>
#include <getopt.h>
#include <iostream>
#include <stdlib.h>
#include <sys/stat.h>
#include <math.h>

double imageSize = 2.0;

/**
 * Generate a bunch of overlapping spheres within one poly data set:
 * one big sphere evenly surrounded by four small spheres that intersect the
 * centered sphere.
 * @param theta sphere sampling resolution (THETA)
 * @param phi sphere sampling resolution (PHI)
 * @return the set of spheres within one logical poly data set
 **/
vtkSmartPointer<vtkAppendPolyData> GenerateOverlappingBunchOfSpheres(int theta,
                                                                     int phi)
{
  vtkSmartPointer<vtkAppendPolyData> appendData =
    vtkSmartPointer<vtkAppendPolyData>::New();
 
  double r = imageSize;
  for (int i = 0; i < 5; i++)
    {
    vtkSmartPointer<vtkSphereSource> sphereSource =
      vtkSmartPointer<vtkSphereSource>::New();
    sphereSource->SetThetaResolution(theta);
    sphereSource->SetPhiResolution(phi);
    // all spheres except the center one have radius = 0.5*imageSize
    sphereSource->SetRadius(0.5*r); 
    
    switch (i)
      {
      case 0:
        sphereSource->SetRadius(r);
        sphereSource->SetCenter(0, 0, 0); break;
      case 1:
        sphereSource->SetCenter(r, 0, 0); break;
      case 2:
        sphereSource->SetCenter(-r, 0, 0); break;
      case 3:
        sphereSource->SetCenter(0, r, 0); break;
      case 4:
        sphereSource->SetCenter(0, -r, 0); break;
      }
    sphereSource->Update();
    appendData->AddInputConnection(sphereSource->GetOutputPort());
    }
 
  return appendData;
}

void addSpheres(int theta, int phi, vtkSmartPointer<vtkRenderer> renderer) {
  // Generate a translucent sphere poly data set that partially overlaps:
  vtkSmartPointer<vtkAlgorithm> translucentGeometry =
    GenerateOverlappingBunchOfSpheres(theta, phi);
 
  // generate a basic Mapper and Actor
  vtkSmartPointer<vtkPolyDataMapper> mapper = 
    vtkSmartPointer<vtkPolyDataMapper>::New();
  mapper->SetInputConnection(translucentGeometry->GetOutputPort());
 
  vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();
  actor->SetMapper(mapper);
  actor->GetProperty()->SetOpacity(0.5); // translucent !!!
  actor->GetProperty()->SetColor(1, 0, 0);
  // actor->RotateX(-72); 
  renderer->AddActor(actor);

}
 
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

vtkSmartPointer<vtkActor> lineactor;
vtkSmartPointer<vtkActor> lineactor2;

void addLines(vtkSmartPointer<vtkRenderer> renderer) {
  int npts = 6;
  lineactor = vtkSmartPointer<vtkActor>::New();
  lineactor->GetProperty()->SetRepresentationToWireframe();
  lineactor->GetProperty()->SetColor(0, 0, 0);
  // lineactor->GetProperty()->SetOpacity(1.0);
  lineactor->GetProperty()->SetLineWidth(4.);
  vtkSmartPointer<vtkDataSetMapper> mapper =
    vtkSmartPointer<vtkDataSetMapper>::New();
  lineactor->SetMapper(mapper);

  lineactor2 = vtkSmartPointer<vtkActor>::New();
  lineactor2->GetProperty()->SetRepresentationToWireframe();
  lineactor2->GetProperty()->SetColor(1, 0, 0);
  lineactor2->GetProperty()->SetLineWidth(6.);
  lineactor2->SetMapper(mapper);

  vtkSmartPointer<vtkUnstructuredGrid> grid = 
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  grid->SetPoints(points);
  points->Allocate(npts);
  vtkIdType pts[npts];
  double x[3];
  double size = imageSize;
  x[0] = size;
  x[1] = 0.0;
  x[2] = 0.0;
  pts[0] = points->InsertNextPoint(x);
  x[0] = 0.0;
  x[1] = size;
  pts[1] = points->InsertNextPoint(x);
  x[0] = -size;
  x[1] = 0.0;
  pts[2] = points->InsertNextPoint(x);
  x[0] = 0.0;
  x[1] = -size;
  pts[3] = points->InsertNextPoint(x);
  x[0] = 0.0;
  x[1] = 0.0;
  x[2] = size;
  pts[4] = points->InsertNextPoint(x);
  x[2] = -size;
  pts[5] = points->InsertNextPoint(x);
  for(int i=0; i<npts; i++) {
    for(int j=0; j<i; j++) {
      vtkIdType ids[2];
      ids[0] = pts[i];
      ids[1] = pts[j];
      grid->InsertNextCell(VTK_LINE, 2, ids);
    }
  }

  // lineactor->RotateX(-72);
  // lineactor2->RotateX(-72);

  // vtkSmartPointer<vtkExtractEdges> extractor = 
  //   vtkSmartPointer<vtkExtractEdges>::New();
  // extractor->SetInputConnection(grid->GetProducerPort());
  // mapper->SetInput(extractor->GetOutput());
  mapper->SetInput(grid);

  renderer->AddActor(lineactor);
  renderer->AddActor(lineactor2);

  std::cerr << "Added lines" << std::endl;
}


void addCells(vtkSmartPointer<vtkRenderer> renderer) {
  int npts = 6;
  vtkSmartPointer<vtkActor> cellActor = vtkSmartPointer<vtkActor>::New();
  cellActor->GetProperty()->SetRepresentationToSurface();
  vtkSmartPointer<vtkDataSetMapper> mapper = 
    vtkSmartPointer<vtkDataSetMapper>::New();
  cellActor->SetMapper(mapper);
  vtkSmartPointer<vtkUnstructuredGrid> grid =
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  mapper->SetInput(grid);
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  grid->SetPoints(points);
  points->Allocate(npts);
  vtkIdType pts[npts];
  double x[3];
  double size = imageSize;
  x[0] = size;
  x[1] = 0.0;
  x[2] = 0.0;
  pts[0] = points->InsertNextPoint(x);
  x[0] = 0.0;
  x[1] = size;
  pts[1] = points->InsertNextPoint(x);
  x[0] = -size;
  x[1] = 0.0;
  pts[2] = points->InsertNextPoint(x);
  x[0] = 0.0;
  x[1] = -size;
  pts[3] = points->InsertNextPoint(x);
  x[0] = 0.0;
  x[1] = 0.0;
  x[2] = size;
  pts[4] = points->InsertNextPoint(x);
  x[2] = -size;
  pts[5] = points->InsertNextPoint(x);

  for(int i=0; i<4; i++) {
    vtkIdType ids[4];
    ids[0] = pts[i];
    ids[1] = pts[(i+1)%4];
    ids[2] = pts[4];
    ids[3] = pts[5];
    grid->InsertNextCell(VTK_TETRA, 4, ids);
  }

  

  renderer->AddActor(cellActor);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void printExtent(const std::string &tag, vtkSmartPointer<vtkImageData> image) {
  int *extent = image->GetExtent();
  double *spacing = image->GetSpacing();
  std::cerr << tag << ", extent=";
  for(int i=0; i<6; i++)
    std::cerr << " " << extent[i];
  std::cerr << "   spacing=";
  for(int i=0; i<3; i++) 
    std::cerr << " " << spacing[i];
  double *bounds = image->GetBounds();
  std::cerr << "   bounds=";
  for(int i=0; i<6; i++)
    std::cerr << " " << bounds[i];
  std::cerr << std::endl;
}

vtkSmartPointer<vtkImageData> addAlphaChannel(
				      vtkSmartPointer<vtkImageData> image) 
{
  vtkSmartPointer<vtkImageData> alpha = vtkSmartPointer<vtkImageData>::New();
  alpha->SetExtent(image->GetExtent());
  alpha->SetScalarTypeToUnsignedChar();
  alpha->SetNumberOfScalarComponents(1);
  alpha->AllocateScalars();
  
  vtkSmartPointer<vtkImageAppendComponents> appender =
    vtkSmartPointer<vtkImageAppendComponents>::New();
  appender->AddInputConnection(image->GetProducerPort());
  appender->AddInputConnection(alpha->GetProducerPort());
  appender->Update();
  return appender->GetOutput();
}

void setAlpha(vtkSmartPointer<vtkImageData> image, unsigned char opacity) {
  std::cerr << "setAlpha: opacity=" << (int) opacity << std::endl;
  image->GetPointData()->GetScalars()->FillComponent(3, opacity);
}

void setVaryingAlpha(vtkSmartPointer<vtkImageData> image, int opacity)
{
  image->Update();
  int *dims = image->GetDimensions();
  for(int z=0; z<dims[2]; z++)
    for(int y=0; y<dims[1]; y++)
      for(int x=0; x<dims[0]; x++) {
	unsigned char *ptr = (unsigned char*) image->GetScalarPointer(x,y,z);
	ptr[3] = (unsigned char)(opacity*(z+1.)/(dims[2]+1.));
      }
}

vtkSmartPointer<vtkImageData> setSize(vtkSmartPointer<vtkImageData> image,
				      double xsize, double ysize, double zsize)
{
  int *dims = image->GetDimensions();
  double spacing[3];
  spacing[0] = xsize/(dims[0]+1);
  spacing[1] = ysize/(dims[1]+1);
  spacing[2] = zsize/(dims[2]+1);
  vtkSmartPointer<vtkImageChangeInformation> changer =
    vtkSmartPointer<vtkImageChangeInformation>::New();
  changer->SetInputConnection(image->GetProducerPort());
  changer->SetOutputSpacing(spacing);
  changer->Update();
  return changer->GetOutput();
}
 
vtkSmartPointer<vtkImageData> padImage(vtkSmartPointer<vtkImageData> image) {
  int extent[6];
  image->Update();
  image->GetExtent(extent);
  extent[1] += 1;
  extent[3] += 1;
  extent[5] += 1;
  vtkSmartPointer<vtkImageConstantPad> padder =
    vtkSmartPointer<vtkImageConstantPad>::New();
  padder->SetInputConnection(image->GetProducerPort());
  padder->SetOutputWholeExtent(extent);
  padder->SetOutputNumberOfScalarComponents(4);
  padder->SetConstant(0);
  padder->ReleaseDataFlagOn();
  padder->Update();
  return padder->GetOutput();
}


vtkSmartPointer<vtkImageData> addImage(const char *imagedir, int opacity,
				       bool pointwise,
				       vtkSmartPointer<vtkRenderer> renderer)
{
  // Add an image.  Read all of the files in imagedir.
  std::cerr << "Loading image" << std::endl;
  DIR *dir = opendir(imagedir);
  if(!dir) {
    std::cerr << "Cannot open directory " << imagedir << std::endl;
    exit(1);
  }
  struct dirent *filedata;
  vtkSmartPointer<vtkStringArray> names =
    vtkSmartPointer<vtkStringArray>::New();
  while((filedata = readdir(dir)) != 0) {
    if(filedata->d_name[0] != '.') {
      struct stat statbuf;
      std::string fullname = std::string(imagedir) + "/" + filedata->d_name;
      if(!stat(fullname.c_str(), &statbuf)) {
	if(S_ISREG(statbuf.st_mode)) {
	  names->InsertNextValue(fullname);
	}
      }
    }
  }
  closedir(dir);
  std::cerr << "Reading " << names->GetNumberOfValues() << " files."
	    << std::endl;
  vtkSmartPointer<vtkImageReader2Factory> factory =
    vtkSmartPointer<vtkImageReader2Factory>::New();
  vtkSmartPointer<vtkImageReader2> imagereader =
    factory->CreateImageReader2(names->GetPointer(0)->c_str());
  imagereader->SetDataScalarTypeToUnsignedChar();

  // Read first file to get its xy size.
  imagereader->SetFileName(names->GetPointer(0)->c_str());
  // imagereader->ReleaseDataFlagOn();
  imagereader->Update();
  int extent[6];
  imagereader->GetDataExtent(extent);
  extent[4] = 0;
  extent[5] = names->GetNumberOfValues() - 1;
  imagereader->SetDataExtent(extent);

  double spacing[] = {imageSize/(extent[1]+1), 
		      imageSize/(extent[3]+1),
		      imageSize/(extent[5]+1)};
  imagereader->SetDataOrigin(-0.5*imageSize, -0.5*imageSize, -0.5*imageSize);
  imagereader->SetDataSpacing(spacing);

  // Read all files.
  imagereader->SetFileNames(names);
  imagereader->Update();

  vtkSmartPointer<vtkImageData> image = imagereader->GetOutput();

  image = addAlphaChannel(image);
  image = padImage(image);

  vtkSmartPointer<vtkFixedPointVolumeRayCastMapper> mapper =
    vtkSmartPointer<vtkFixedPointVolumeRayCastMapper>::New();

  mapper->IntermixIntersectingGeometryOn();

  vtkSmartPointer<vtkVolume> volume = vtkSmartPointer<vtkVolume>::New();
  vtkSmartPointer<vtkVolumeProperty> volprop =
    vtkSmartPointer<vtkVolumeProperty>::New();
  volprop->IndependentComponentsOff(); // RGBA data, no lookup table
  vtkSmartPointer<vtkPiecewiseFunction> opacityfunc =
    vtkSmartPointer<vtkPiecewiseFunction>::New();
  double op;
  if(pointwise) {
    op = 1.0;
    setAlpha(image, opacity);
    // setVaryingAlpha(image, opacity);
  }
  else {
    op = opacity/255.;
    setAlpha(image, 255);
  }
  opacityfunc->AddSegment(0, 0, 255, op);
  volprop->SetScalarOpacity(opacityfunc);

  volume->SetProperty(volprop);
  volume->SetMapper(mapper);
  // volume->RotateX(-72);
  mapper->SetInputConnection(image->GetProducerPort());
  renderer->AddVolume(volume);
  //mapper->DebugOn();
  //std::cerr << "mapper=" << *mapper << std::endl;
  return image;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void set_sample_distances(vtkSmartPointer<vtkRenderer> renderer,
			  vtkSmartPointer<vtkRenderWindow> window)
{
  double angle = renderer->GetActiveCamera()->GetViewAngle()*M_PI/360.;
  double height = 2*renderer->GetActiveCamera()->GetDistance()*tan(angle);
  double window_height = window->GetSize()[1];
  double sample_distance = height/window_height;
  if(sample_distance > 0.2)
    sample_distance = 0.2;
  int numvolumes = renderer->VisibleVolumeCount();
  vtkVolumeCollection *volumes = renderer->GetVolumes();
  volumes->InitTraversal();
  vtkVolume *vol = volumes->GetNextVolume();
  while(vol != 0) {
    vtkFixedPointVolumeRayCastMapper *map =
      vtkFixedPointVolumeRayCastMapper::SafeDownCast(vol->GetMapper());
    std::cerr << "set_sample_distances: " << sample_distance << std::endl;
    map->SetSampleDistance(sample_distance);
    map->SetInteractiveSampleDistance(2*sample_distance);
    vol = volumes->GetNextVolume();
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int main (int argc, char *argv[])
{
  extern char *optarg;
  
  int theta = 20;
  int phi = 20;
  bool pointwise = false;
  // double occlusionRatio = 0.1;
  char *imagedir = 0;
  bool lines=true;
  int opacity = 255;

  int ch, which;
  static struct option longopts[] = {
    {"pointwise", no_argument, 0, 'p'},
    {"image", required_argument, 0, 'i'},
    {"nolines", no_argument, 0, 'l'},
    {"opacity", required_argument, 0, 'o'},
    {"size", required_argument, 0, 's'},
    {0, 0, 0, 0}
  };
  while((ch = getopt_long(argc, argv, "o:pi:ls:", longopts, &which)) != -1)
    {
      if(ch == -1)
	break;
      switch(ch) {
      case 'p':
	pointwise = true;
	break;
      case 'o':
	opacity = atof(optarg);
	break;
      case 'i':
	imagedir = optarg;
	break;
      case 'l':
	lines = false;
	break;
      case 's':
	imageSize = atof(optarg);
	break;
      case 0:
	break;
      default:
	std::cerr << "Error in arguments! " << argv[optind] << std::endl;
      }
    }

  vtkSmartPointer<vtkRenderer> renderer =
    vtkSmartPointer<vtkRenderer>::New();
  vtkSmartPointer<vtkRenderWindow> renderWindow =
   // vtkSmartPointer<vtkRenderWindow>::New();
    vtkSmartPointer<vtkXOpenGLRenderWindow>::New();
  renderWindow->AddRenderer(renderer);

  vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
    vtkSmartPointer<vtkRenderWindowInteractor>::New();
  renderWindowInteractor->SetRenderWindow(renderWindow);
  renderer->SetBackground(1, 1, 1);
  renderWindow->SetSize(600, 400);

  // if(imagedir == 0)
  //   addSpheres(theta, phi, renderer);
  // else 
  vtkSmartPointer<vtkImageData> image = addImage(imagedir, opacity, pointwise,
						 renderer);

  if(lines) 
    addLines(renderer);

  // Setup view geometry
  renderer->ResetCamera();
  set_sample_distances(renderer, renderWindow);

  renderer->GetActiveCamera()->Zoom(2.); 

  // Initialize interaction
  renderWindowInteractor->Initialize();
 
  // Check the average frame rate when rotating the actor
  int endCount = 100;
  vtkSmartPointer<vtkTimerLog> clock = vtkSmartPointer<vtkTimerLog>::New();
  // Set a user transform for successively rotating the camera position
  vtkSmartPointer<vtkTransform> transform =
    vtkSmartPointer<vtkTransform>::New();
  transform->Identity();
  transform->RotateY(2.0); // rotate 2 degrees around Y-axis at each iteration
  renderWindow->Render();
  vtkSmartPointer<vtkInteractorStyleTrackballCamera> tball =
    vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New();
  renderWindowInteractor->SetInteractorStyle(tball);

  vtkSmartPointer<vtkAnnotatedCubeActor> axes =
    vtkSmartPointer<vtkAnnotatedCubeActor>::New();


  // vtkSmartPointer<vtkAxesActor> axes = 
  //   vtkSmartPointer<vtkAxesActor>::New();
  // renderer->AddActor(axes);
  // axes->SetTotalLength(2,2,2);
  // axes->GetXAxisCaptionActor2D()->GetCaptionTextProperty()->SetColor(0, 1, 0);
  // vtkSmartPointer<vtkTransform> atransform =
  //   vtkSmartPointer<vtkTransform>::New();
  // atransform->Translate(-1, -1, -1);
  // axes->SetUserTransform(atransform);
 
  vtkSmartPointer<vtkOrientationMarkerWidget> widget = 
    vtkSmartPointer<vtkOrientationMarkerWidget>::New();
  widget->SetOutlineColor( 0.9300, 0.5700, 0.1300 );
  widget->SetOrientationMarker( axes );
  widget->SetInteractor( renderWindowInteractor );
  widget->SetViewport( 0.0, 0.0, 0.4, 0.4 );
  widget->SetEnabled( 1 );
  widget->InteractiveOn();

  vtkSmartPointer<vtkCamera> camera = renderer->GetActiveCamera();
  double camPos[3]; // camera position
  // Start test
  clock->StartTimer();
  for (int i = 0; i < endCount; i++)
    {
    camera->GetPosition(camPos);
    transform->TransformPoint(camPos, camPos);
    camera->SetPosition(camPos);
    renderWindow->Render();
    }
  std::cerr << "Done rendering" << std::endl;
  clock->StopTimer();
  double frameRate = (double)endCount / clock->GetElapsedTime();
  std::cout << "AVERAGE FRAME RATE: " << frameRate << " fps" << std::endl;

  // Changing the opacity here makes the image disappear.
  //setVaryingAlpha(image, opacity);

  // // Change the order in which the wire frames are drawn.
  // renderer->RemoveViewProp(lineactor);
  // renderer->AddActor(lineactor);
  renderWindow->Render();

  renderWindowInteractor->Start();
  return 0;
}

