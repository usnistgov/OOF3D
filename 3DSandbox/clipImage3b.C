// This program draws a checkerboard ala an OOF3D image display and
// clips it with two planes.  The cells at the intersection of the two
// planes aren't drawn correctly.

// As modified by Bill Lorenson at kitware
// SAL added tet mesh

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
#include <vtkTetra.h>
#include <vtkUnstructuredGrid.h>

#define IMAGESIZE 64		// number of checkerboard squares on a side
#define MESHSIZE 5		// number of blocks of tets on a side
#define CUBESIZE 20.0		// physical linear dimension of entire system

// Color for the checkerboard image
#define IMAGE_R 0.7
#define IMAGE_G 0.7
#define IMAGE_B 0.7
#define IMAGE_A 1.0
#define DIM 0.5			// amount to dim the dark squares by

#define MESH_R 0.5
#define MESH_G 0.2
#define MESH_B 0.2
#define MESH_A 0.5

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
  int checkerSize = n / 8;
  for(unsigned int z=0; z<n; z++) {
    for(unsigned int y=0; y<n; y++) {
      for(unsigned int x=0; x<n; x++) {
	unsigned char *ptr = (unsigned char*) image0->GetScalarPointer(x, y, z);
	*ptr = (x/checkerSize+y/checkerSize+z/checkerSize)%2; // checkerboard
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

// Make a grid by dividing the cube into subcubes and each subcube
// into 5 tetrahedra.  n is the number of subcubes on a side.

vtkSmartPointer<vtkUnstructuredGrid> makeMesh(unsigned int n) {
  int total = 5*n*n*n;		// total number of tets
  double delta = CUBESIZE/n;

  vtkSmartPointer<vtkUnstructuredGrid> mesh =
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  mesh->Allocate(total, total);
  mesh->SetPoints(points);
  
  // Create points.  Order of loops is weird, but historical.
  for(int i=0; i<=n; i++) {			 // y dimension
    double y = (i == n? CUBESIZE : i*delta);
    for(int j=0; j<=n; j++) {			 // x dimension
      double x = (j == n? CUBESIZE: j*delta);
      for(int k=0; k<=n; k++) {			 // z dimension
	double z = (k == n? CUBESIZE : k*delta);
	points->InsertNextPoint(x,y,z);
      }
    }
  }

  for(int i=0; i<n; i++) {			 // y dimension
    for(int j=0; j<n; j++) {			 // x dimension
      for(int k=0; k<n; k++) {			 // z dimension

	// Indices of points at the corners of this subcube.
	int ulf = (i+1)*(n+1)*(n+1)+j*(n+1)+k+1;      // upper left front
	int urf = (i+1)*(n+1)*(n+1)+(j+1)*(n+1)+k+1;  // upper right front
	int lrf = i*(n+1)*(n+1)+(j+1)*(n+1)+k+1;      // lower right front
	int llf = i*(n+1)*(n+1)+j*(n+1)+k+1;          // lower left front 
	int ulb = (i+1)*(n+1)*(n+1)+j*(n+1)+k;        // upper left back
	int urb = (i+1)*(n+1)*(n+1)+(j+1)*(n+1)+k;    // upper right back 
	int lrb = i*(n+1)*(n+1)+(j+1)*(n+1)+k;        // lower right back
	int llb = i*(n+1)*(n+1)+j*(n+1)+k;            // lower left back

	// There are two possible arrangements of the 5 tets in the
	// subcube.  Adjacent subcubes must have alternating
	// arrangements.
	if((i+j+k)%2 == 0) {
	  vtkIdType ids1[4] = {llf, urf, lrf, lrb}; // tet in lrf corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids1);
	  vtkIdType ids2[4] = {llf, ulf, urf, ulb}; // tet in ulf corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids2);
	  vtkIdType ids3[4] = {lrb, urf, urb, ulb}; // tet in urb corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids3);
	  vtkIdType ids4[4] = {llf, lrb, llb, ulb}; // tet in llb corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids4);
	  vtkIdType ids5[4] = {llf, ulb, urf, lrb}; // tet in middle
	  mesh->InsertNextCell(VTK_TETRA, 4, ids5);
	}
	else {
	  vtkIdType ids1[4] = {llf, ulf, lrf, llb}; // tet in llf corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids1);
	  vtkIdType ids2[4] = {ulf, urf, lrf, urb}; // tet in urf corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids2);
	  vtkIdType ids3[4] = {ulf, ulb, urb, llb}; // tet in ulb corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids3);
	  vtkIdType ids4[4] = {lrf, urb, lrb, llb}; // tet in lrb corner
	  mesh->InsertNextCell(VTK_TETRA, 4, ids4);
	  vtkIdType ids5[4] = {ulf, urb, lrf, llb}; // tet in middle
	  mesh->InsertNextCell(VTK_TETRA, 4, ids5);
	}
      }
    }
  }
  return mesh;
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

  vtkSmartPointer<vtkDataSetMapper> imageMapper =
    vtkSmartPointer<vtkDataSetMapper>::New();
  vtkSmartPointer<vtkActor> imageActor = vtkSmartPointer<vtkActor>::New();
  imageActor->SetMapper(imageMapper);
  renderer->AddViewProp(imageActor);
  imageMapper->SetInputConnection(clipper->GetOutputPort());

  vtkSmartPointer<vtkUnstructuredGrid> mesh = makeMesh(MESHSIZE);
  vtkSmartPointer<vtkDataSetMapper> meshMapper =
    vtkSmartPointer<vtkDataSetMapper>::New();
  vtkSmartPointer<vtkActor> meshActor = vtkSmartPointer<vtkActor>::New();
  meshActor->GetProperty()->SetRepresentationToWireframe();
  meshActor->GetProperty()->SetRepresentationToSurface();
  meshActor->GetProperty()->SetColor(MESH_R, MESH_G, MESH_B);
  meshActor->GetProperty()->SetOpacity(MESH_A);
  meshActor->SetMapper(meshMapper);
  vtkSmartPointer<vtkTableBasedClipDataSet> meshClipper =
    vtkSmartPointer<vtkTableBasedClipDataSet>::New();
  meshClipper->SetClipFunction(clipPlanes);
  meshClipper->SetInputData(mesh);
  meshMapper->SetInputConnection(meshClipper->GetOutputPort());
  renderer->AddViewProp(meshActor);

  renderer->ResetCamera();
  renderWindow->Render();
  
  interactor->Start();
  return 0;
}
