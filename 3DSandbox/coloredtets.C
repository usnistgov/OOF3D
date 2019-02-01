
#include <vtkActor.h>
#include <vtkAutoInit.h>
#include <vtkDataSetMapper.h>
#include <vtkInteractorStyleSwitch.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkTetra.h>
#include <vtkUnstructuredGrid.h>


int main(int, char*[]) {

  VTK_MODULE_INIT(vtkRenderingOpenGL2);
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

  // Corners of a simple right tetrahedron
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  points->InsertNextPoint(0., 0., 0.);
  points->InsertNextPoint(1., 0., 0.);
  points->InsertNextPoint(0., 1., 0.);
  points->InsertNextPoint(0., 0., 1.);

  // Make a trivial grid with one tetrahedral cell.
  vtkSmartPointer<vtkUnstructuredGrid> gridA =
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  gridA->SetPoints(points);
  vtkIdType idsA[4] = {0, 1, 2, 3};
  gridA->InsertNextCell(VTK_TETRA, 4, idsA);

  // Make a second identical grid.
  vtkSmartPointer<vtkUnstructuredGrid> gridB =
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  gridB->SetPoints(points);
  gridB->InsertNextCell(VTK_TETRA, 4, idsA); // same points as gridA

  // Render the two grids.  gridA is red and gridB is green.  gridA
  // should hide gridB because of its relative coincident topology settings. 
  vtkSmartPointer<vtkDataSetMapper> mapperA =
    vtkSmartPointer<vtkDataSetMapper>::New();
  mapperA->SetInputData(gridA);
  mapperA->SetRelativeCoincidentTopologyPolygonOffsetParameters(-3, -3);
  vtkSmartPointer<vtkActor> actorA = vtkSmartPointer<vtkActor>::New();
  actorA->GetProperty()->SetRepresentationToSurface();
  actorA->GetProperty()->SetColor(1.0, 0.0, 0.0);
  actorA->SetMapper(mapperA);
  renderer->AddViewProp(actorA);

  vtkSmartPointer<vtkDataSetMapper> mapperB =
    vtkSmartPointer<vtkDataSetMapper>::New();
  mapperB->SetInputData(gridB);
  vtkSmartPointer<vtkActor> actorB = vtkSmartPointer<vtkActor>::New();
  actorB->GetProperty()->SetRepresentationToSurface();
  actorB->GetProperty()->SetColor(0.0, 1.0, 0.0);
  actorB->SetMapper(mapperB);
  renderer->AddViewProp(actorB);

  renderer->ResetCamera();
  renderWindow->Render();
  interactor->Start();
  return 0;
}

