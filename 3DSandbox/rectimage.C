// -*- C++ -*-
// $RCSfile: rectimage.C,v $
// $Revision: 1.1.2.5 $
// $Author: langer $
// $Date: 2013/11/08 19:36:51 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <assert.h>

#include <vtkActor.h>
#include <vtkCellData.h>
#include <vtkDataSetMapper.h>
#include <vtkDoubleArray.h>
#include <vtkImageAppendComponents.h>
#include <vtkImageData.h>
#include <vtkImageReader2.h>
#include <vtkImageReader2Factory.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkPlane.h>
#include <vtkPointData.h>
#include <vtkProperty.h>
#include <vtkRectilinearGrid.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkStringArray.h>
#include <vtkTableBasedClipDataSet.h>
#include <vtkUnstructuredGrid.h>
#include <vtkXOpenGLRenderWindow.h>

#include "oofImageToGrid.h"
#include "oofOverlayVoxels.h"
#include "oofExcludeVoxels.h"
 
#include <dirent.h>
#include <getopt.h>
#include <iostream>
#include <stdlib.h>
#include <sys/stat.h>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

vtkSmartPointer<vtkImageData> readImage(const char *imagedir) {
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
  vtkSmartPointer<vtkImageReader2Factory> factory = 
    vtkSmartPointer<vtkImageReader2Factory>::New();
  vtkSmartPointer<vtkImageReader2> imagereader = 
    factory->CreateImageReader2(names->GetPointer(0)->c_str());
  imagereader->SetDataScalarTypeToUnsignedChar();
  // Read first file to get its xy size
  imagereader->SetFileName(names->GetPointer(0)->c_str());
  imagereader->Update();
  int extent[6];
  imagereader->GetDataExtent(extent);
  extent[4] = 0;
  extent[5] = names->GetNumberOfValues() - 1;
  imagereader->SetDataExtent(extent);
  
  imagereader->SetFileNames(names);
  imagereader->Update();
  return imagereader->GetOutput();
}


vtkSmartPointer<vtkUnstructuredGrid> clipGrid(
			      vtkSmartPointer<vtkDataSet> rectgrid,
			      double clipfactor)
{
  double bounds[6];
  rectgrid->Update();	       
  rectgrid->ComputeBounds();
  rectgrid->GetBounds(bounds);
  double xmid = (bounds[1] - bounds[0])*clipfactor;
  double ymid = (bounds[3] - bounds[2])*clipfactor;
  double zmid = (bounds[5] - bounds[4])*clipfactor;
  vtkSmartPointer<vtkPlane> plane = vtkSmartPointer<vtkPlane>::New();
  plane->SetNormal(1,1,1);
  plane->SetOrigin(xmid, ymid, zmid);
  vtkSmartPointer<vtkTableBasedClipDataSet> clipper =
    vtkSmartPointer<vtkTableBasedClipDataSet>::New();
  clipper->SetClipFunction(plane);
  clipper->SetInputConnection(rectgrid->GetProducerPort());
  return clipper->GetOutput();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool excludefn(const ICoord &ijk) {
  //  return !(ijk(0) == ijk(1) && ijk(1) == ijk(2)) && ijk(0) != 0;
  return (ijk(0) + ijk(1) + ijk(2)) % 2;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int main(int argc, char *argv[]) {
  double opacity = 1.0;
  char *imagedir = 0;
  char *image2dir = 0;
  double clipfactor = 0;
  bool clip = false;
  bool exclude = false;

  extern char *optarg;
  int ch, which;
  static struct option longopts[] = {
    {"image", required_argument, 0, 'i'},
    {"image2", required_argument, 0, '2'},
    {"opacity", required_argument, 0, 'o'},
    {"clip", required_argument, 0, 'c'},
    {"exclude", no_argument, 0, 'e'}
  };
  while((ch = getopt_long(argc, argv, "i:o:c:e2:", longopts, &which)) != -1) {
    if(ch == -1)
      break;
    switch(ch) {
    case 'i':
      imagedir = optarg;
      break;
    case 'o':
      opacity = atof(optarg);
      break;
    case 'c':
      clipfactor = atof(optarg);
      clip = true;
      break;
    case 'e':
      exclude = true;
      break;
    case '2':
      image2dir = optarg;
      break;
    }
  }

  vtkSmartPointer<vtkRenderer> renderer =
    vtkSmartPointer<vtkRenderer>::New();
  vtkSmartPointer<vtkRenderWindow> renderWindow =
    vtkSmartPointer<vtkXOpenGLRenderWindow>::New();
  renderWindow->AddRenderer(renderer);
  renderer->SetBackground(1, 1, 1);
  renderWindow->SetSize(600, 400);
  vtkSmartPointer<vtkRenderWindowInteractor> renderWindowInteractor =
    vtkSmartPointer<vtkRenderWindowInteractor>::New();
  renderWindowInteractor->SetRenderWindow(renderWindow);
  vtkSmartPointer<vtkInteractorStyleTrackballCamera> tball =
    vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New();
  renderWindowInteractor->SetInteractorStyle(tball);


  vtkSmartPointer<vtkImageData> image = readImage(imagedir);

  vtkSmartPointer<oofImageToGrid> image2Grid =
    vtkSmartPointer<oofImageToGrid>::New();
  image2Grid->SetInputConnection(image->GetProducerPort());
  vtkSmartPointer<vtkRectilinearGrid> rGrid = image2Grid->GetOutput();


  PixelSet voxels;
  ICoord voxel(0, 1, 2);
  voxels.add(voxel);
  voxel = ICoord(0, 4, 4);
  voxels.add(voxel);
  for(int i=0; i<5; i++) {
    ICoord voxel(i, i, i);
    voxels.add(voxel);
  }
  double color[] = {0.3, 0.3, 0.3};
  vtkSmartPointer<oofOverlayVoxels> overlay =
    vtkSmartPointer<oofOverlayVoxels>::New();
  overlay->DebugOn();
  overlay->SetPixelSet(&voxels);
  overlay->SetColor(color);
  overlay->SetOpacity(0.9);
  overlay->SetInputConnection(rGrid->GetProducerPort());
  rGrid = overlay->GetOutput();

  vtkSmartPointer<vtkUnstructuredGrid> uGrid;

  if(exclude) {
    vtkSmartPointer<oofExcludeVoxels> excluder = 
      vtkSmartPointer<oofExcludeVoxels>::New();
    excluder->SetExclude(excludefn);
    excluder->SetInputConnection(rGrid->GetProducerPort());
    uGrid = excluder->GetOutput();
  }

  if(clip) {
    if(exclude)
      uGrid = clipGrid(uGrid, clipfactor);
    else
      uGrid = clipGrid(rGrid, clipfactor);
  }

  vtkSmartPointer<vtkDataSetMapper> mapper
    = vtkSmartPointer<vtkDataSetMapper>::New();
  mapper->SelectColorArray(0);
  vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();
  actor->SetMapper(mapper);
  if(opacity != 1.0)
    actor->GetProperty()->SetOpacity(opacity);
  renderer->AddActor(actor);

  mapper->SetScalarModeToUseCellFieldData();
  if(uGrid.GetPointer() != 0)
    mapper->SetInputConnection(uGrid->GetProducerPort());
  else
    mapper->SetInputConnection(rGrid->GetProducerPort());

  std::cerr << "*** Rendering ***" << std::endl;
  renderWindow->Render();

  if(image2dir) {
    // replace image with another one
    std::cerr << "*** Loading second image ***" << std::endl;
    vtkSmartPointer<vtkImageData> image2 = readImage(image2dir);
    image2Grid->RemoveAllInputs();
    image2Grid->SetInputConnection(image2->GetProducerPort());
    std::cerr << "*** Rendering again ***" << std::endl;
    renderWindow->Render();
  }

  renderWindowInteractor->Start();
  return 0;
}


std::ostream &operator<<(std::ostream &os, const ICoord &ic) {
  return os << "ICoord(" << ic(0) << ", " << ic(1) << ", " << ic(2) << ")";
}
