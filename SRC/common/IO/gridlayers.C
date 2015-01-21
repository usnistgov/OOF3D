// -*- C++ -*-
// $RCSfile: gridlayers.C,v $
// $Revision: 1.1.2.11 $
// $Author: langer $
// $Date: 2014/11/25 19:20:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/ghostoofcanvas.h"
#include "common/IO/gridlayers.h"
#include "common/IO/gridsourcebase.h"
#include "common/IO/oofcerr.h"
#include "common/threadstate.h"

#include <vtkActor.h>
#include <vtkCellData.h>
#include <vtkPointData.h>
#include <vtkProperty.h>
#include <vtkLookupTable.h>

WireGridCanvasLayer::WireGridCanvasLayer(GhostOOFCanvas *c,
					 const std::string &nm,
					 vtkSmartPointer<GridSource> gridsrc)
  : OOFCanvasLayer(c, nm),
    gridsource(gridsrc),
    edgeActor(vtkSmartPointer<vtkActor>::New()),
    faceActor(vtkSmartPointer<vtkActor>::New()),
    edgeMapper(vtkSmartPointer<vtkDataSetMapper>::New()),
    faceMapper(vtkSmartPointer<vtkDataSetMapper>::New()),
    locator(vtkSmartPointer<oofCellLocator>::New()),
    edgeExtractor(vtkSmartPointer<vtkExtractEdges>::New())
{
  // Since the grid is a grid of tets, the internal edges won't be
  // drawn if we simply use "mapper->SetInput(grid)".  We have to
  // extract the edges first.  However, if just the edges are drawn,
  // the vtkCellPicker won't ever select the tets, so we draw both.
  addProp(edgeActor);
  addProp(faceActor);

  // TODO OPT: Check that edge extraction isn't being repeated when
  // trivial changes are being made to the layer (eg, nodes have
  // moved, or display parameters have changed).
  ///edgeMapper->SetInput(edgeExtractor->GetOutput());
  edgeActor->SetMapper(edgeMapper);
  edgeActor->GetProperty()->SetRepresentationToWireframe();
  // edgeActor->GetProperty()->SetAmbient(1.0);

  faceActor->SetMapper(faceMapper);
  faceActor->GetProperty()->SetRepresentationToSurface();
  // Draw the displayed tets almost invisibly, since they haven't
  // actually been requested by the user.
  faceActor->GetProperty()->SetColor(0.99, 0.99, 0.99);
  faceActor->GetProperty()->SetOpacity(0.01);

  vtkSmartPointer<vtkUnstructuredGrid> grid = gridsource->GetOutput();

  locator->LazyEvaluationOn();
  locator->SetDataSet(grid);

  // vtkExtractEdges has to operate on the original grid, not the
  // clipped grid, because clipping introduces new internal edges when
  // it tetrahedralizes the clipped cells.  We need to extract the
  // edges because the wireframe rendering of the original grid omits
  // all internal edges.
  edgeExtractor->SetInputConnection(grid->GetProducerPort());

  // set_clipping finishes building the pipeline.
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

WireGridCanvasLayer::~WireGridCanvasLayer() {}

const std::string &WireGridCanvasLayer::classname() const {
  static const std::string nm("WireGridCanvasLayer");
  return nm;
}

void WireGridCanvasLayer::setModified() {
  gridsource->Modified();
}

void WireGridCanvasLayer::set_color(const CColor &lineColor) {
  edgeActor->GetProperty()->SetColor(lineColor.getRed(),
				     lineColor.getGreen(),
				     lineColor.getBlue());
}

void WireGridCanvasLayer::set_lineWidth(int lineWidth) {
  edgeActor->GetProperty()->SetLineWidth(lineWidth);
}

void WireGridCanvasLayer::start_clipping() {
  // To draw the intersections of the faces with the clipping planes,
  // we have to draw the wireframe representation of the clipped
  // original grid.  This doesn't include internal edges, but that's
  // ok.  The clipped wireframe representation of the extracted edges
  // doesn't draw anything on the clipping planes.  We can't use a
  // vtkCutter here, because it introduces extra internal edges (eg,
  // the quad produced by cutting a tet will be drawn as two
  // triangles).

  //* TODO OPT: This scheme draws all unclipped external edges twice.
  //* Using vtkExtractGeometry on the clipped grid might allow us to
  //* draw them only once, and to give different properties to the
  //* intersections drawn on the clipping planes.

  vtkSmartPointer<vtkPolyData> edges = edgeExtractor->GetOutput();
  cutActor = vtkSmartPointer<vtkActor>::New();
  cutActor->SetProperty(edgeActor->GetProperty());
  cutMapper = vtkSmartPointer<vtkDataSetMapper>::New();
  cutActor->SetMapper(cutMapper);
  addProp(cutActor);
  faceClipper = getClipper(this);
  faceClipper->SetInputConnection(gridsource->GetOutputPort());
  cutMapper->SetInputConnection(faceClipper->GetOutputPort());
  faceMapper->SetInputConnection(faceClipper->GetOutputPort());
  edgeClipper = getClipper(this);
  edgeClipper->SetInputConnection(edgeExtractor->GetOutputPort());
  edgeMapper->SetInputConnection(edgeClipper->GetOutputPort());
}

void WireGridCanvasLayer::stop_clipping() {
  if(clipState == CLIP_ON) {
    removeProp(cutActor);
    faceClipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
    edgeClipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
  }
  cutActor = vtkSmartPointer<vtkActor>();
  cutMapper = vtkSmartPointer<vtkDataSetMapper>();
  faceMapper->SetInput(gridsource->GetOutput());
  edgeMapper->SetInput(edgeExtractor->GetOutput());
}

void WireGridCanvasLayer::set_clip_parity(bool inverted) {
  faceClipper->SetInsideOut(inverted);
  edgeClipper->SetInsideOut(inverted);
}

vtkSmartPointer<vtkProp3D> WireGridCanvasLayer::get_pickable_prop3d() {
  return faceActor;
}

vtkSmartPointer<vtkDataSet> WireGridCanvasLayer::get_pickable_dataset() {
  return gridsource->GetOutput();
}

vtkSmartPointer<vtkPoints> WireGridCanvasLayer::get_pickable_points() {
  return vtkSmartPointer<vtkPoints>(gridsource->GetOutput()->GetPoints());
}

vtkSmartPointer<vtkAbstractCellLocator> WireGridCanvasLayer::get_locator() {
  // If the locator isn't reinitialized here, clicks on a refined
  // Skeleton aren't interpreted correctly.  Apparently the locator
  // doesn't forget the old dataset when a new one is assigned.
  //* TODO OPT: Don't initialize on every mouse click, only after the
  //* skeleton or mesh has been modified or the layer has been edited.
  locator->Initialize();
  locator->SetDataSet(gridsource->GetOutput());
  return locator;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FilledGridCanvasLayer::FilledGridCanvasLayer(GhostOOFCanvas *canvas,
					     const std::string &nm,
					     vtkSmartPointer<GridSource> gs)
  : OOFCanvasLayer(canvas, nm),
    gridsource(gs),
    actor(vtkSmartPointer<vtkActor>::New()),
    mapper(vtkSmartPointer<vtkDataSetMapper>::New()),
    locator(vtkSmartPointer<vtkCellLocator>::New())
{
  addProp(actor);
  actor->SetMapper(mapper);
  actor->GetProperty()->SetRepresentationToSurface();
  //actor->GetProperty()->SetAmbient(1.0);
  locator->SetDataSet(gridsource->GetOutput());
  locator->LazyEvaluationOn();

  // set_clipping can't be called here, because it calls
  // start/stop_clipping, which is pure virutal in
  // FilledGridCanvasLayer.  The derived classes have to call it.
  //set_clipping(canvas->clipping(), canvas->invertedClipping());
}

FilledGridCanvasLayer::~FilledGridCanvasLayer() {}

const std::string &FilledGridCanvasLayer::classname() const {
  static const std::string nm("FilledGridCanvasLayer");
  return nm;
}


void FilledGridCanvasLayer::setModified() {
  gridsource->Modified();
}

void FilledGridCanvasLayer::set_clip_parity(bool inverted) {
  clipper->SetInsideOut(inverted);
}

void FilledGridCanvasLayer::set_lookupTable(vtkSmartPointer<vtkLookupTable> lut,
					    double dmin, double dmax)
{
  assert(mainthread_query());
  // oofcerr << "FilledGridCanvasLayer::set_lookupTable: min=" << dmin
  // 	  << " max=" << dmax << std::endl;
  vmin = dmin;
  vmax = dmax;
  mapper->SetScalarRange(dmin, dmax);
  lut->SetRange(dmin, dmax);
  mapper->SetLookupTable(lut);
  canvas->updateContourMap(this, lut);
}

vtkScalarsToColors *FilledGridCanvasLayer::get_lookupTable() {
  return mapper->GetLookupTable();
}

vtkSmartPointer<vtkProp3D> FilledGridCanvasLayer::get_pickable_prop3d() {
  return actor;
}

vtkSmartPointer<vtkDataSet> FilledGridCanvasLayer::get_pickable_dataset() {
  return gridsource->GetOutput();
}

vtkSmartPointer<vtkPoints> FilledGridCanvasLayer::get_pickable_points() {
  return vtkSmartPointer<vtkPoints>(gridsource->GetOutput()->GetPoints());
}

vtkSmartPointer<vtkAbstractCellLocator> FilledGridCanvasLayer::get_locator() {
  // If the locator isn't reinitialized here, clicks on a refined
  // Skeleton aren't interpreted correctly.  The locator apparently
  // doesn't forget its old dataset when a new one is assigned.
  //* TODO OPT: Don't initialize on every mouse click, only after the
  //* skeleton or mesh has been modified or the layer has been edited.
  locator->Initialize();
  locator->SetDataSet(gridsource->GetOutput());
  return locator;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SolidFilledGridCanvasLayer::SolidFilledGridCanvasLayer(
			       GhostOOFCanvas *canvas, const std::string &nm,
			       vtkSmartPointer<GridSource> gs)
  : FilledGridCanvasLayer(canvas, nm, gs)
{
  mapper->SetScalarModeToUseCellData();
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

const std::string &SolidFilledGridCanvasLayer::classname() const {
  static const std::string nm("SolidFilledGridCanvasLayer");
  return nm;
}

void SolidFilledGridCanvasLayer::start_clipping() {
  clipper = getClipper(this);
  clipper->SetInputConnection(gridsource->GetOutputPort());
  mapper->SetInputConnection(clipper->GetOutputPort());
}

void SolidFilledGridCanvasLayer::stop_clipping() {
  mapper->SetInputConnection(gridsource->GetOutputPort());
  clipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
}

void SolidFilledGridCanvasLayer::set_CellData(
				      vtkSmartPointer<vtkDataArray> data)
{
  gridsource->SetCellData(data);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The pipeline is 
// MeshGridSource --> Clipper --> GeometryFilter --> BandedPolyDataContourFilter
//  --> Mapper
// The Clipper is optional.  The data to be contoured is an argument
// to MeshGridSource.

// TODO OPT: The right way to do the contouring is to compute the data
// *after* running GeometryFilter, so that it's computed only on the
// visible surface.  This will require calling the python
// Output.evaluate routine from C++, or moving the Output classes to
// C++.

ContourGridCanvasLayer::ContourGridCanvasLayer(GhostOOFCanvas *canvas,
					       const std::string &nm,
					       vtkSmartPointer<GridSource> gs)
  : OOFCanvasLayer(canvas, nm),
    gridsource(gs),
    actor(vtkSmartPointer<vtkActor>::New()),
    mapper(vtkSmartPointer<vtkPolyDataMapper>::New()),
    geometryfilter(vtkSmartPointer<vtkGeometryFilter>::New()),
    contourfilter(vtkSmartPointer<vtkBandedPolyDataContourFilter>::New()),
    locator(vtkSmartPointer<vtkCellLocator>::New())
{
  addProp(actor);
  actor->SetMapper(mapper);
  actor->GetProperty()->SetInterpolationToFlat();

  // TODO 3.1: These three lines turn off shading, so the displayed
  // colors don't depend on the surface normal.  Shading should be a
  // global option applied to all layers.
  // actor->GetProperty()->SetAmbient(1.0);
  // actor->GetProperty()->SetSpecular(0.0);
  // actor->GetProperty()->SetDiffuse(0.0);

  locator->SetDataSet(gridsource->GetOutput());
  locator->LazyEvaluationOn();
  contourfilter->SetInputConnection(geometryfilter->GetOutputPort());
  contourfilter->SetScalarModeToValue();
  mapper->SetScalarModeToUseCellData();
  mapper->SetInputConnection(contourfilter->GetOutputPort());
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

const std::string &ContourGridCanvasLayer::classname() const {
  static const std::string nm("ContourGridCanvasLayer");
  return nm;
}

void ContourGridCanvasLayer::set_pointData(vtkSmartPointer<vtkDoubleArray> data)
{
  // This sets the PointData member in the MeshGridSource object.  It
  // doesn't directly affect the data in the vtkUnstructuredGrid,
  // which might not exist yet.
  gridsource->SetPointData(data);
}

void ContourGridCanvasLayer::start_clipping() {
  clipper = getClipper(this);
  clipper->SetInputConnection(gridsource->GetOutputPort());
  geometryfilter->SetInputConnection(clipper->GetOutputPort());
}

void ContourGridCanvasLayer::stop_clipping() {
  clipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
  geometryfilter->SetInputConnection(gridsource->GetOutputPort());
}

void ContourGridCanvasLayer::set_nContours(int n, double vmin, double vmax) {
  contourfilter->GenerateValues(n, vmin, vmax);
  mapper->SetScalarRange(vmin, vmax);
}

void ContourGridCanvasLayer::set_lookupTable(
				     vtkSmartPointer<vtkLookupTable> lut)
{
  assert(mainthread_query());
  mapper->SetLookupTable(lut);
  canvas->updateContourMap(this, lut);
}

vtkScalarsToColors *ContourGridCanvasLayer::get_lookupTable() {
  return mapper->GetLookupTable();
}

void ContourGridCanvasLayer::set_clip_parity(bool inverted) {
  clipper->SetInsideOut(inverted);
}

void ContourGridCanvasLayer::setModified() {
  gridsource->Modified();
}

#include <vtkXMLPolyDataWriter.h>

void ContourGridCanvasLayer::writeVTK(const std::string &filename) {
  // For debugging
  vtkSmartPointer<vtkXMLPolyDataWriter> writer =
    vtkSmartPointer<vtkXMLPolyDataWriter>::New();
  writer->SetInputConnection(contourfilter->GetOutputPort());
  writer->SetFileName(filename.c_str());
  writer->SetDataModeToAscii();
  writer->Write();
}
