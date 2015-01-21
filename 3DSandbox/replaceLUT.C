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
#include <vtkLookupTable.h>
#include <vtkCellData.h>
#include <vtkCommand.h>
#include <vtkCallbackCommand.h>

#include <vtkTableBasedClipDataSet.h>
#include <vtkClipDataSet.h>

std::vector<vtkSmartPointer<vtkLookupTable> > luts;

vtkSmartPointer<vtkDataSetMapper> mapper;
vtkSmartPointer<vtkDataSetMapper> cutMapper;

void callback(vtkObject *obj, unsigned long eid, void *clientdata,
	      void *calldata)
{
  static int n = 0;
  ++n;
  if(n >= luts.size())
    n = 0;
  mapper->SetLookupTable(luts[n]);
  cutMapper->SetLookupTable(luts[n]);
}

void addTet(vtkSmartPointer<vtkUnstructuredGrid> grid,
	    vtkSmartPointer<vtkDoubleArray> data,
	    vtkIdType p0, vtkIdType p1, vtkIdType p2, vtkIdType p3)
{
  vtkIdType pts[4];
  pts[0] = p0;
  pts[1] = p1;
  pts[2] = p2;
  pts[3] = p3;
  vtkIdType i = grid->InsertNextCell(VTK_TETRA, 4, pts);
  std::cerr << "addTet: " << i << std::endl;
  static double v = 0.0;
  data->InsertNextValue(v);
  //v += 0.25;
  v += 1;
}

vtkSmartPointer<vtkLookupTable> getLUT_red() {
  vtkSmartPointer<vtkLookupTable> lut = vtkSmartPointer<vtkLookupTable>::New();
  int ncolors = 5;
  lut->SetNumberOfColors(ncolors);
  for(int i=0; i<ncolors; i++) {
    double d = i/(ncolors - 1.);
    lut->SetTableValue(i, d, 1.-d, 1.-d, 1.);
  }
  return lut;
}

vtkSmartPointer<vtkLookupTable> getLUT_grn() {
  vtkSmartPointer<vtkLookupTable> lut = vtkSmartPointer<vtkLookupTable>::New();
  int ncolors = 5;
  lut->SetNumberOfColors(ncolors);
  for(int i=0; i<ncolors; i++)
    lut->SetTableValue(i, 0., i/(ncolors-1.), 0., 1.);
  return lut;
}

vtkSmartPointer<vtkLookupTable> getLUT_gry() {
  vtkSmartPointer<vtkLookupTable> lut = vtkSmartPointer<vtkLookupTable>::New();
  int ncolors = 19;
  lut->SetNumberOfColors(ncolors);
  for(vtkIdType i=0; i<ncolors; i++)
    lut->SetTableValue(i, i/(ncolors-1.), i/(ncolors-1.), i/(ncolors-1.), 1.);
  return lut;
}

int main(int, char**) {
  vtkSmartPointer<vtkOpenGLRenderer> renderer =
    vtkSmartPointer<vtkOpenGLRenderer>::New();
  renderer->SetBackground(1, 1, 0);

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
  actor->GetProperty()->SetRepresentationToSurface();
  //actor->GetProperty()->SetRepresentationToWireframe();
  mapper = vtkSmartPointer<vtkDataSetMapper>::New();
  actor->SetMapper(mapper);
  mapper->SetScalarRange(0., 4.);

  vtkSmartPointer<vtkUnstructuredGrid> grid =
    vtkSmartPointer<vtkUnstructuredGrid>::New();
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  grid->SetPoints(points);
  vtkSmartPointer<vtkDoubleArray> data = vtkSmartPointer<vtkDoubleArray>::New();
  grid->GetCellData()->SetScalars(data);

  // Create corner points of a cube
  double x[3];
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


  // Create five tetrahedra in a cube
  addTet(grid, data, 0, 6, 5, 4);
  addTet(grid, data, 5, 3, 0, 1);
  addTet(grid, data, 0, 6, 2, 3);
  addTet(grid, data, 5, 3, 7, 6);
  addTet(grid, data, 0, 5, 6, 3);	// central tet

  std::cerr << "Data:" << std::endl;
  for(vtkIdType i=0; i<data->GetNumberOfTuples(); i++) {
    std::cerr << i << ": " << data->GetValue(i) << std::endl;
  }
  
  luts.push_back(getLUT_gry());
  luts.push_back(getLUT_red());
  luts.push_back(getLUT_grn());
  
  mapper->SetLookupTable(luts[0]);
  mapper->SetScalarModeToUseCellData();
  mapper->SetScalarRange(0, 4);

  bool clipping = true;
  bool cutting = true;
  vtkSmartPointer<vtkPlanes> planes = vtkSmartPointer<vtkPlanes>::New();

  if(clipping || cutting) {
    vtkSmartPointer<vtkPoints> clippoints = vtkSmartPointer<vtkPoints>::New();
    vtkSmartPointer<vtkDoubleArray> normals = 
      vtkSmartPointer<vtkDoubleArray>::New();
    normals->SetNumberOfComponents(3);
    double nrml[] = {0.0, 0.0, -1.0};
    normals->InsertNextTuple(nrml);
    double pt[] = {0.0, 0.0, 0.5};
    clippoints->InsertNextPoint(pt);
    planes->SetPoints(clippoints);
    planes->SetNormals(normals);
  }
  
  if(!clipping) {
    mapper->SetInputConnection(grid->GetProducerPort());
  }
  else {
    vtkSmartPointer<vtkClipDataSet> clipper =
      vtkSmartPointer<vtkClipDataSet>::New();
    clipper->SetClipFunction(planes);
    clipper->SetInputConnection(grid->GetProducerPort());
    mapper->SetInput(clipper->GetOutput());
  }

  cutMapper = vtkSmartPointer<vtkDataSetMapper>::New();
  if(cutting) {
    vtkSmartPointer<vtkActor> cutActor = vtkSmartPointer<vtkActor>::New();
    cutMapper->SetLookupTable(luts[0]);
    cutMapper->SetScalarModeToUseCellData();
    cutMapper->SetScalarRange(0, 4);
  
    cutActor->SetMapper(cutMapper);
    renderer->AddActor(cutActor);
    // cutActor->GetProperty()->SetRepresentationToWireframe();
    cutActor->GetProperty()->SetRepresentationToSurface();
    //cutActor->GetProperty()->SetColor(1, 0, 0);
    cutActor->GetProperty()->SetLineWidth(2);
    vtkSmartPointer<vtkCutter> cutter = vtkSmartPointer<vtkCutter>::New();
    cutter->SetInputConnection(grid->GetProducerPort());
    cutter->SetCutFunction(planes);
    cutMapper->SetInput(cutter->GetOutput());
  }

  renderer->ResetCamera();
  window->Render();

  interactor->Initialize();

  vtkSmartPointer<vtkCallbackCommand> callbackcmd =
    vtkSmartPointer<vtkCallbackCommand>::New();
  callbackcmd->SetCallback(callback);
  
  interactor->AddObserver(vtkCommand::LeftButtonPressEvent, callbackcmd);
  
  interactor->Start();

  return 0;
}
