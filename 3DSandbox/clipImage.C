
// This file started out as a copy of the vtk example program
// CorrectlyRenderTranslucentGeometry.C, which draws translucent
// spheres using Depth Peeling, if available.  It's not available on
// OS X (or at least on my Mac) so the part of the code that decides
// how to render the translucent bits has been removed.


#include <vtkActor.h>
#include <vtkAlgorithm.h>
#include <vtkAlgorithmOutput.h>
#include <vtkAppendPolyData.h>
#include <vtkCamera.h>
#include <vtkClipVolume.h>
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
#include <vtkPlane.h>
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
#include <vtkUnstructuredGridVolumeRayCastMapper.h>
#include <vtkVolume.h>
#include <vtkVolumeProperty.h>
#include <vtkXOpenGLRenderWindow.h>

#include <vtkProjectedTetrahedraMapper.h>

#include <assert.h>
#include <dirent.h>
#include <getopt.h>
#include <iostream>
#include <stdlib.h>
#include <sys/stat.h>
#include <math.h>

double imageSize = 2.0;
bool clipping = false;
bool padding = false;


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
  padder->SetConstant(255);
  padder->ReleaseDataFlagOn();
  padder->Update();
  return padder->GetOutput();
}


void addImage(const char *imagedir, int opacity,
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
  //image = padImage(image);


  // The vtkVolume gets a different kind of mapper if it's being
  // clipped.
  if(!clipping) {
    if(padding)
      image = padImage(image);
    vtkSmartPointer<vtkVolume> volume = vtkSmartPointer<vtkVolume>::New();
    vtkSmartPointer<vtkVolumeProperty> volprop =
      vtkSmartPointer<vtkVolumeProperty>::New();
    volprop->IndependentComponentsOff(); // RGBA data, no lookup table
    vtkSmartPointer<vtkPiecewiseFunction> opacityfunc =
      vtkSmartPointer<vtkPiecewiseFunction>::New();
    double op = opacity/255.;
    setAlpha(image, 255);
    opacityfunc->AddSegment(0, 0, 255, op);
    volprop->SetScalarOpacity(opacityfunc);
    volume->SetProperty(volprop);
    renderer->AddVolume(volume);

    vtkSmartPointer<vtkFixedPointVolumeRayCastMapper> mapper =
      vtkSmartPointer<vtkFixedPointVolumeRayCastMapper>::New();
    mapper->IntermixIntersectingGeometryOn();
    volume->SetMapper(mapper);
    mapper->SetInputConnection(image->GetProducerPort());
  }
  else {			// clipping
    // Single clipping plane
    if(padding)
      image = padImage(image);
    vtkSmartPointer<vtkPlane> plane = vtkSmartPointer<vtkPlane>::New();
    plane->SetOrigin(0, 0, 0);
    plane->SetNormal(-1, -1, -1);
    //plane->SetNormal(1, 0, 0);
    vtkSmartPointer<vtkClipVolume> clipper =
      vtkSmartPointer<vtkClipVolume>::New();
    clipper->SetClipFunction(plane);
    clipper->Mixed3DCellGenerationOn();
    clipper->SetInputConnection(image->GetProducerPort());
    vtkSmartPointer<vtkUnstructuredGrid> ug = clipper->GetOutput();


    // // vtkSmartPointer<vtkUnstructuredGridVolumeRayCastMapper> mapper =
    // //   vtkSmartPointer<vtkUnstructuredGridVolumeRayCastMapper>::New();
    // // mapper->IntermixIntersectingGeometryOn();
    // vtkSmartPointer<vtkProjectedTetrahedraMapper> mapper =
    //   vtkSmartPointer<vtkProjectedTetrahedraMapper>::New();    
    // volume->SetMapper(mapper);
    // mapper->SetInputConnection(ug->GetProducerPort());

    vtkSmartPointer<vtkDataSetMapper> mapper = 
      vtkSmartPointer<vtkDataSetMapper>::New();
    mapper->SetInput(ug);
    mapper->InterpolateScalarsBeforeMappingOff();
    //mapper->SetScalarModeToUseCellData();
    vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();
    renderer->AddActor(actor);
    actor->SetMapper(mapper);

    // vtkSmartPointer<vtkActor> actor2 = vtkSmartPointer<vtkActor>::New();
    // vtkSmartPointer<vtkDataSetMapper> map2 = 
    //   vtkSmartPointer<vtkDataSetMapper>::New();
    // actor2->SetMapper(map2);
    // map2->SetInput(ug);
    // renderer->AddActor(actor2);
    // actor2->GetProperty()->SetRepresentationToWireframe();
  }
  //mapper->DebugOn();
  //std::cerr << "mapper=" << *mapper << std::endl;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void addSeg(vtkSmartPointer<vtkUnstructuredGrid> grid, vtkIdType a, vtkIdType b)
{
  vtkIdType ids[2];
  ids[0] = a;
  ids[1] = b;
  grid->InsertNextCell(VTK_LINE, 2, ids);
}

void addLines(vtkSmartPointer<vtkRenderer> renderer) {
  int npts = 8;
  vtkSmartPointer<vtkActor> lineactor;
  lineactor = vtkSmartPointer<vtkActor>::New();
  lineactor->GetProperty()->SetRepresentationToWireframe();
  lineactor->GetProperty()->SetColor(0, 0, 0);
  // lineactor->GetProperty()->SetOpacity(1.0);
  lineactor->GetProperty()->SetLineWidth(4.);
  vtkSmartPointer<vtkDataSetMapper> mapper =
    vtkSmartPointer<vtkDataSetMapper>::New();
  lineactor->SetMapper(mapper);

  vtkSmartPointer<vtkUnstructuredGrid> grid = 
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  grid->SetPoints(points);
  points->Allocate(npts);
  vtkIdType pts[npts];
  #define FUDGE 1.0
  double size = FUDGE*imageSize; // add a little extra space
  int n=0;
  for(int i=0; i<2; i++)
    for(int j=0; j<2; j++)
      for(int k=0; k<2; k++) {
	double xyz[3] = {size*(i-0.5),
			 size*(j-0.5),
			 size*(k-0.5)};
	pts[n] = points->InsertNextPoint(xyz);
	n++;
      }
  addSeg(grid, pts[0], pts[1]);
  addSeg(grid, pts[1], pts[3]);
  addSeg(grid, pts[3], pts[2]);
  addSeg(grid, pts[2], pts[0]);
  addSeg(grid, pts[4], pts[5]);
  addSeg(grid, pts[5], pts[7]);
  addSeg(grid, pts[7], pts[6]);
  addSeg(grid, pts[6], pts[4]);
  addSeg(grid, pts[1], pts[5]);
  addSeg(grid, pts[0], pts[4]);
  addSeg(grid, pts[2], pts[6]);
  addSeg(grid, pts[3], pts[7]);

  mapper->SetInput(grid);
  renderer->AddActor(lineactor);

  std::cerr << "Added lines" << std::endl;
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
  vtkVolumeCollection *volumes = renderer->GetVolumes();
  volumes->InitTraversal();
  vtkVolume *vol = volumes->GetNextVolume();
  while(vol != 0) {
    if(!clipping) {
      vtkFixedPointVolumeRayCastMapper *map =
	vtkFixedPointVolumeRayCastMapper::SafeDownCast(vol->GetMapper());
      map->SetSampleDistance(sample_distance);
      map->SetInteractiveSampleDistance(sample_distance);
      //map->AutoAdjustSampleDistancesOn();
    }
    else {
      vtkAbstractVolumeMapper *map = vol->GetMapper();
      if(map->IsA("vtkUnstructuredGridVolumeRayCastMapper")) {
	vtkUnstructuredGridVolumeRayCastMapper *mp =
	  vtkUnstructuredGridVolumeRayCastMapper::SafeDownCast(mp);
	mp->SetImageSampleDistance(sample_distance);
	// mp->AutoAdjustSampleDistancesOn();
      }
    }
    vol = volumes->GetNextVolume();
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int main (int argc, char *argv[])
{
  extern char *optarg;
  
  char *imagedir = 0;
  bool lines=true;
  int opacity = 255;

  int ch, which;
  static struct option longopts[] = {
    {"image", required_argument, 0, 'i'},
    {"nolines", no_argument, 0, 'l'},
    {"opacity", required_argument, 0, 'o'},
    {"size", required_argument, 0, 's'},
    {"clip", no_argument, 0, 'c'},
    {"pad", no_argument, 0, 'p'},
    {0, 0, 0, 0}
  };
  while((ch = getopt_long(argc, argv, "o:i:ls:cp", longopts, &which)) != -1)
    {
      if(ch == -1)
	break;
      switch(ch) {
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
      case 'c':
	clipping = true;
	break;
      case 'p':
	padding = true;
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
  renderer->SetBackground(0.9, 0.9, 0.9);
  renderWindow->SetSize(600, 400);

  addImage(imagedir, opacity, renderer);

  if(lines) 
    addLines(renderer);

  // Setup view geometry
  renderer->ResetCamera();
  set_sample_distances(renderer, renderWindow);

  //  renderer->GetActiveCamera()->Zoom(2.); 

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

  // vtkSmartPointer<vtkCamera> camera = renderer->GetActiveCamera();
  // double camPos[3]; // camera position
  // // Start test
  // clock->StartTimer();
  // for (int i = 0; i < endCount; i++)
  //   {
  //   camera->GetPosition(camPos);
  //   transform->TransformPoint(camPos, camPos);
  //   camera->SetPosition(camPos);
  //   renderWindow->Render();
  //   }
  // std::cerr << "Done rendering" << std::endl;
  // clock->StopTimer();
  // double frameRate = (double)endCount / clock->GetElapsedTime();
  // std::cout << "AVERAGE FRAME RATE: " << frameRate << " fps" << std::endl;

  renderWindow->Render();

  renderWindowInteractor->Start();
  return 0;
}

