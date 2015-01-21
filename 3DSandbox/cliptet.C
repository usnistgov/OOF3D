#include <vtkActor.h>
#include <vtkCellType.h>
#include <vtkCutter.h>
#include <vtkDataSetMapper.h>
#include <vtkDoubleArray.h>
#include <vtkInteractorStyleTrackballCamera.h>
#include <vtkOpenGLRenderer.h>
#include <vtkPlane.h>
#include <vtkPlanes.h>
#include <vtkPoints.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

#include <vtkTableBasedClipDataSet.h>
#include <vtkClipDataSet.h>

void addTet(vtkSmartPointer<vtkUnstructuredGrid> grid,
	    vtkIdType p0, vtkIdType p1, vtkIdType p2, vtkIdType p3)
{
  vtkIdType pts[4];
  pts[0] = p0;
  pts[1] = p1;
  pts[2] = p2;
  pts[3] = p3;
  grid->InsertNextCell(VTK_TETRA, 4, pts);
}

int main(int, char**) {
  vtkSmartPointer<vtkOpenGLRenderer> renderer =
    vtkSmartPointer<vtkOpenGLRenderer>::New();
  renderer->SetBackground(1, 1, 1);

  vtkSmartPointer<vtkRenderWindow> window = 
    vtkSmartPointer<vtkRenderWindow>::New();
  window->AddRenderer(renderer);
  window->SetSize(600, 600);

  vtkSmartPointer<vtkRenderWindowInteractor> interactor =
    vtkSmartPointer<vtkRenderWindowInteractor>::New();
  interactor->SetRenderWindow(window);
  vtkSmartPointer<vtkInteractorStyleTrackballCamera> tball =
    vtkSmartPointer<vtkInteractorStyleTrackballCamera>::New();
  interactor->SetInteractorStyle(tball);


  vtkSmartPointer<vtkActor> actor = vtkSmartPointer<vtkActor>::New();
  renderer->AddActor(actor);
  actor->GetProperty()->SetRepresentationToWireframe();
  actor->GetProperty()->SetColor(0, 0, 0);
  actor->GetProperty()->SetLineWidth(4);

  vtkSmartPointer<vtkDataSetMapper> mapper = 
    vtkSmartPointer<vtkDataSetMapper>::New();
  actor->SetMapper(mapper);

  vtkSmartPointer<vtkUnstructuredGrid> grid =
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  grid->SetPoints(points);
  vtkIdType pts[4];
  double x[3];

  // // Create a single tetrahedron
  // points->Allocate(4);
  // x[0] = 0; x[1] = 0; x[2] = 0;
  // pts[0] = points->InsertNextPoint(x);
  // x[0] = 1; x[1] = 1; x[2] = 0;
  // pts[1] = points->InsertNextPoint(x);
  // x[0] = 0; x[1] = 1; x[2] = 1;
  // pts[2] = points->InsertNextPoint(x);
  // x[0] = 1; x[1] = 0; x[2] = 1;
  // pts[3] = points->InsertNextPoint(x);
  // grid->InsertNextCell(VTK_TETRA, 4, pts);

  // Create five tetrahedra in a cube
  points->Allocate(8);
  int m = 0;
  for(int i=0; i<2; i++) {
    x[0] = i;
    for(int j=0; j<2; j++) {
      x[1] = j;
      for(int k=0; k<2; k++) {
	x[2] = k;
	points->InsertNextPoint(x);
      }
    }
  }
  addTet(grid, 0, 6, 5, 4);
  addTet(grid, 5, 3, 0, 1);
  addTet(grid, 0, 6, 2, 3);
  addTet(grid, 0, 5, 6, 3);	// central tet
  addTet(grid, 5, 3, 7, 6);

  // // No clipping
  // mapper->SetInputConnection(grid->GetProducerPort());

  // Clipping
  vtkSmartPointer<vtkClipDataSet> clipper =
    vtkSmartPointer<vtkClipDataSet>::New();
  // vtkSmartPointer<vtkPlane> plane = vtkSmartPointer<vtkPlane>::New();
  // plane->SetNormal(0, 0, 1);
  // plane->SetOrigin(0, 0, 0.5);
  // clipper->SetClipFunction(plane);

  vtkSmartPointer<vtkPlanes> planes = vtkSmartPointer<vtkPlanes>::New();
  vtkSmartPointer<vtkPoints> clippoints = vtkSmartPointer<vtkPoints>::New();
  vtkSmartPointer<vtkDoubleArray> normals = 
    vtkSmartPointer<vtkDoubleArray>::New();
  normals->SetNumberOfComponents(3);
  double nrml[] = {0.0, 0.0, 1.0};
  normals->InsertNextTuple(nrml);
  double pt[] = {0.0, 0.0, 0.5};
  clippoints->InsertNextPoint(pt);
  planes->SetPoints(clippoints);
  planes->SetNormals(normals);
  clipper->SetClipFunction(planes);

  clipper->SetInputConnection(grid->GetProducerPort());
  mapper->SetInput(clipper->GetOutput());

  // Add a Cutter too.
  vtkSmartPointer<vtkActor> cutActor = vtkSmartPointer<vtkActor>::New();
  vtkSmartPointer<vtkDataSetMapper> cutMapper = 
    vtkSmartPointer<vtkDataSetMapper>::New();
  cutActor->SetMapper(cutMapper);
  renderer->AddActor(cutActor);
  cutActor->GetProperty()->SetRepresentationToWireframe();
  cutActor->GetProperty()->SetColor(1, 0, 0);
  cutActor->GetProperty()->SetLineWidth(2);
  vtkSmartPointer<vtkCutter> cutter = vtkSmartPointer<vtkCutter>::New();
  cutter->SetInputConnection(grid->GetProducerPort());
  cutter->SetCutFunction(planes);
  cutMapper->SetInput(cutter->GetOutput());

  renderer->ResetCamera();
  interactor->Initialize();
  window->Render();
  interactor->Start();

  return 0;
}
