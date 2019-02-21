#include <vtkActor.h>
#include <vtkAutoInit.h>
#include <vtkCellData.h>
#include <vtkDataSetMapper.h>
#include <vtkDoubleArray.h>
#include <vtkInteractorStyleSwitch.h>
#include <vtkMapper.h>
#include <vtkPlanes.h>
#include <vtkPoints.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkTableBasedClipDataSet.h>
#include <vtkClipDataSet.h>
#include <vtkTetra.h>
#include <vtkUnstructuredGrid.h>

#define MESHSIZE 5		// number of blocks of tets on a side
#define CUBESIZE 20.0		// physical linear dimension of entire system

#define MESH_R 1.0
#define MESH_G 0.0
#define MESH_B 0.0
#define MESH_A 1.0

// Offsets for clipping planes with normals in the X and Y directions
#define XOFFSET 8.5
#define YOFFSET 8.5

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

  vtkSmartPointer<vtkUnstructuredGrid> mesh = makeMesh(MESHSIZE);
  vtkSmartPointer<vtkDataSetMapper> meshMapper =
    vtkSmartPointer<vtkDataSetMapper>::New();
  vtkSmartPointer<vtkActor> meshActor = vtkSmartPointer<vtkActor>::New();
  //meshActor->GetProperty()->SetRepresentationToWireframe();
  meshActor->GetProperty()->SetRepresentationToSurface();
  meshActor->GetProperty()->SetColor(MESH_R, MESH_G, MESH_B);
  meshActor->GetProperty()->SetOpacity(MESH_A);
  meshActor->SetMapper(meshMapper);
  clipper->SetInputData(mesh);
  meshMapper->SetInputConnection(clipper->GetOutputPort());
  renderer->AddViewProp(meshActor);

  renderer->ResetCamera();
  renderWindow->Render();
  
  interactor->Start();
  return 0;
}
