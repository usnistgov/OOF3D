// This program draws a checkerboard ala an OOF3D image display and
// clips it with two planes.  The cells at the intersection of the two
// planes aren't drawn correctly.

#include <vtkActor.h>
#include <vtkAutoInit.h>
#include <vtkCellData.h>
#include <vtkDataSetMapper.h>
#include <vtkDoubleArray.h>
#include <vtkExecutive.h>
#include <vtkImageData.h>
#include <vtkImageMapToColors.h>
#include <vtkInteractorStyleSwitch.h>
#include <vtkLookupTable.h>
#include <vtkMapper.h>
#include <vtkPlanes.h>
#include <vtkPointData.h>
#include <vtkPoints.h>
#include <vtkProperty.h>
#include <vtkRectilinearGrid.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkTableBasedClipDataSet.h>
#include <vtkRenderStepsPass.h>

#define IMAGESIZE 8		// number of checkerboard squares on a side
#define CUBESIZE 20.0		// physical linear dimension of entire system

// Color for the checkerboard image
#define IMAGE_R 0.7
#define IMAGE_G 0.7
#define IMAGE_B 0.7
#define IMAGE_A 1.0
#define DIM 0.5			// amount to dim the dark squares by

// Offsets for clipping planes with normals in the X and Y directions
#define XOFFSET 8
#define YOFFSET 8

///////////////////

// Make a rectilinear grid that shows image-like data, by creating a
// cubic cell at each point. A checkerboard pattern is used for
// simplicity.

vtkSmartPointer<vtkRectilinearGrid> makeImage(int n) {
  // This is a simplification of a program that uses actual image data
  // as a source for the rectilinear grid.  In order to recreate the
  // same vtk calls, create a dummy image here.
  vtkSmartPointer<vtkImageData> image0 = vtkSmartPointer<vtkImageData>::New();
  image0->SetDimensions(n, n, n);
  image0->AllocateScalars(VTK_UNSIGNED_CHAR, 1);
  image0->SetSpacing(CUBESIZE/n, CUBESIZE/n, CUBESIZE/n);
  for(unsigned int z=0; z<n; z++) {
    for(unsigned int y=0; y<n; y++) {
      for(unsigned int x=0; x<n; x++) {
	unsigned char *ptr = (unsigned char*) image0->GetScalarPointer(x, y, z);
	*ptr = (x+y+z)%2; // checkerboard
      }
    }
  }
  
  vtkSmartPointer<vtkLookupTable> lut = vtkSmartPointer<vtkLookupTable>::New();
  lut->SetNumberOfTableValues(2);
  lut->SetTableRange(0, 1);
  lut->SetTableValue(0, IMAGE_R, IMAGE_G, IMAGE_B, IMAGE_A);
  lut->SetTableValue(1, DIM*IMAGE_R, DIM*IMAGE_G, DIM*IMAGE_B, IMAGE_A);

  vtkSmartPointer<vtkImageMapToColors> map =
    vtkSmartPointer<vtkImageMapToColors>::New();
  map->SetLookupTable(lut);
  map->SetOutputFormatToRGBA();
  map->SetInputData(image0);
  map->GetExecutive()->Update();
  vtkImageData *image = map->GetOutput();

  // Convert the image to a rectilinear grid.  Each point in the image
  // becomes a cubic cell in the grid.
  
  vtkSmartPointer<vtkRectilinearGrid> rectgrid =
    vtkSmartPointer<vtkRectilinearGrid>::New();

  int extent[6];
  image->GetExtent(extent);
  extent[1] += 1;
  extent[3] += 1;
  extent[5] += 1;
  rectgrid->SetExtent(extent);

  vtkSmartPointer<vtkDoubleArray> xcoords =
    vtkSmartPointer<vtkDoubleArray>::New();
  vtkSmartPointer<vtkDoubleArray> ycoords =
    vtkSmartPointer<vtkDoubleArray>::New();
  vtkSmartPointer<vtkDoubleArray> zcoords =
    vtkSmartPointer<vtkDoubleArray>::New();
  xcoords->SetNumberOfValues(n+1);
  ycoords->SetNumberOfValues(n+1);
  zcoords->SetNumberOfValues(n+1);
  double spacing[3];
  image->GetSpacing(spacing);
  for(vtkIdType i=0; i<=n; i++) {
    xcoords->InsertValue(i, i*spacing[0]);
    ycoords->InsertValue(i, i*spacing[1]);
    zcoords->InsertValue(i, i*spacing[2]);
  }
  rectgrid->SetXCoordinates(xcoords);
  rectgrid->SetYCoordinates(ycoords);
  rectgrid->SetZCoordinates(zcoords);

  vtkPointData *pointData = image->GetPointData();
  vtkCellData *cellData = rectgrid->GetCellData();
  cellData->ShallowCopy(pointData);
  return rectgrid;
}

/////////////////////
////////////////////

int main(int argc, char *argv[]) {

  VTK_MODULE_INIT(vtkRenderingOpenGL2);
  VTK_MODULE_INIT(vtkRenderingContextOpenGL2);
  VTK_MODULE_INIT(vtkRenderingVolumeOpenGL2);
  VTK_MODULE_INIT(vtkRenderingFreeType);
  VTK_MODULE_INIT(vtkInteractionStyle);

  vtkMapper::SetResolveCoincidentTopologyToPolygonOffset();
  
  vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();
  renderer->SetBackground(1.0, 1.0, 1.0);

  vtkSmartPointer<vtkRenderWindow> renderWindow =
    vtkSmartPointer<vtkRenderWindow>::New();
  renderWindow->AddRenderer(renderer);
  vtkSmartPointer<vtkRenderWindowInteractor> interactor =
    vtkSmartPointer<vtkRenderWindowInteractor>::New();
  vtkSmartPointer<vtkInteractorStyleSwitch> style =
    vtkSmartPointer<vtkInteractorStyleSwitch>::New();
  interactor->SetInteractorStyle(style);
  interactor->SetRenderWindow(renderWindow);

  vtkSmartPointer<vtkRectilinearGrid> image = makeImage(IMAGESIZE);

  // Clipping planes in the X and Y direction.
  vtkSmartPointer<vtkDoubleArray> normals
    = vtkSmartPointer<vtkDoubleArray>::New();
  vtkSmartPointer<vtkPoints> clipPts = vtkSmartPointer<vtkPoints>::New();
  normals->SetNumberOfComponents(3);
  double xnorm[3] = {-1., 0., 0.};
  double ynorm[3] = {0., -1., 0.};
  double xpt[3] = {XOFFSET, 0., 0.};
  double ypt[3] = {0., YOFFSET, 0.};
  normals->InsertNextTuple(xnorm);
  normals->InsertNextTuple(ynorm);
  clipPts->InsertNextPoint(xpt);
  clipPts->InsertNextPoint(ypt);
  vtkSmartPointer<vtkPlanes> clipPlanes = vtkSmartPointer<vtkPlanes>::New();
  clipPlanes->SetNormals(normals);
  clipPlanes->SetPoints(clipPts);

  vtkSmartPointer<vtkTableBasedClipDataSet> clipper =
    vtkSmartPointer<vtkTableBasedClipDataSet>::New();
  clipper->SetClipFunction(clipPlanes);
  clipper->SetInputData(image);
  // clipper->SetInsideOut(1);

  vtkSmartPointer<vtkDataSetMapper> imageMapper =
    vtkSmartPointer<vtkDataSetMapper>::New();
  vtkSmartPointer<vtkActor> imageActor = vtkSmartPointer<vtkActor>::New();
  imageActor->SetMapper(imageMapper);
  renderer->AddViewProp(imageActor);
  imageMapper->SetInputConnection(clipper->GetOutputPort());

  renderer->ResetCamera();
  renderWindow->Render();
  
  interactor->Start();
  return 0;
}
