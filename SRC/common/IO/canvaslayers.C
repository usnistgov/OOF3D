// -*- C++ -*-
// $RCSfile: canvaslayers.C,v $
// $Revision: 1.1.2.77 $
// $Author: langer $
// $Date: 2014/12/14 22:49:09 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/canvaslayers.h"
#include "common/IO/ghostoofcanvas.h"
#include "common/IO/oofExcludeVoxels.h"
#include "common/IO/oofImageToGrid.h"
#include "common/IO/oofOverlayVoxels.h"
#include "common/IO/oofcerr.h"
#include "common/IO/view.h"
#include "common/coord.h"
#include "common/imagebase.h"
#include "common/threadstate.h"
#include "common/voxelfilter.h"

#include <vtkAlgorithmOutput.h>
#include <vtkPointData.h>	// required implicitly by GetPointData
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkVoxel.h>

// TODO 3.1: Give each layer a flag indicating whether or not it should be
// clipped, and make the flag settable in the gfx window's layer list.

// TODO 3.1: When multiple intersecting clipping planes are used, the
// Skeleton isn't clipped correctly.  See clipbug2.log in TEST3D.

const std::string &OOFCanvasLayerBase::modulename() const {
  static const std::string modname("ooflib.SWIG.common.IO.canvaslayer");
  return modname;
}

OOFCanvasLayerBase::OOFCanvasLayerBase(GhostOOFCanvas *c, const std::string &nm)
  : canvas(c),
    name_(nm),
    clipState(CLIP_UNKNOWN)
{
  c->newLayer(this);
  // oofcerr << "OOFCanvasLayerBase::ctor: " << this << " " << name() 
  // 	  << std::endl;
}

OOFCanvasLayerBase::~OOFCanvasLayerBase() {
  canvas->removeLayer(this);
}

void OOFCanvasLayerBase::set_clipping(bool clip, bool inverted) {
  if(clip && clipState != CLIP_ON) {
    start_clipping();
    clipState = CLIP_ON;
  }
  else if(!clip && clipState != CLIP_OFF) {
    stop_clipping();
    clipState = CLIP_OFF;
  }
  if(clipState == CLIP_ON)
    set_clip_parity(inverted);
}

std::ostream &operator<<(std::ostream &os, const OOFCanvasLayerBase &layer) {
  return os << layer.name();
}

OOFCanvasLayer::OOFCanvasLayer(GhostOOFCanvas *c, const std::string &nm)
  : OOFCanvasLayerBase(c, nm),
    showing_(false)
{}

OOFCanvasLayer::~OOFCanvasLayer() {
}

void OOFCanvasLayer::addProp(vtkSmartPointer<vtkProp> prop) {
  props.push_back(prop);
  canvas->renderer->AddViewProp(prop);
}

void OOFCanvasLayer::removeProp(vtkSmartPointer<vtkProp> prop) {
  for(PropVec::iterator i=props.begin(); i<props.end(); ++i) {
    if(*i == prop) {
      props.erase(i);
      if(canvas->renderer->HasViewProp(prop)) {
	canvas->renderer->RemoveViewProp(prop);
      }
      return;
    }
  }
  assert(0);			// This shouldn't happen.
}

void OOFCanvasLayer::removeAllProps() {
  for(PropVec::iterator i=props.begin(); i<props.end(); ++i) {
    if(canvas->renderer->HasViewProp(*i)) {
      canvas->renderer->RemoveViewProp(*i);
    }
  }
  props.resize(0);
}

// void OOFCanvasLayer::raise_layer(int h) {
//   canvas->raise_layer(this, h);
// }

// void GhostOOFCanvas::raise_layer(OOFCanvasLayer *layer, int h) {
//   for(DisplayLayerList::iterator it=layers.begin(); it!=layers.end(); ++it) {
//     if(*it == layer) {
//       layers.erase(it);
//       layers.insert(it+h, layer);
//       return;
//     }
//   }
// }

// void OOFCanvasLayer::raise_to_top() {
//   canvas->raise_layer_to_top(this);
//   // if(rendered_) 
//   //   remove_from_renderer);
//   if(showing)
//     add_to_renderer();
// }

// void GhostOOFCanvas::raise_layer_to_top(OOFCanvasLayer *layer) {
//   for(DisplayLayerList::iterator it=layers.begin(); it!=layers.end(); ++it) {
//     if(*it == layer) {
//       layers.erase(it);
//       layers.push_back(layer);
//       return;
//     }
//   }
// }

// void OOFCanvasLayer::lower_layer(int h) {
//   canvas->lower_layer(this, h);
// }

// void GhostOOFCanvas::lower_layer(OOFCanvasLayer *layer, int h) {
//   for(DisplayLayerList::iterator it=layers.begin(); it!=layers.end(); ++it) {
//     if(*it == layer) {
//       layers.erase(it);
//       layers.insert(it-h, layer);
//       return;
//     }
//   }
// }

void OOFCanvasLayer::show(bool forced) {
  if(!showing_ || forced) {
    for(unsigned int i=0; i<props.size(); i++)
      props[i]->VisibilityOn();
    showing_ = true;
  }
}

void OOFCanvasLayer::hide(bool forced) {
  if(showing_ || forced) {
    for(unsigned int i=0; i<props.size(); i++)
      props[i]->VisibilityOff();
    showing_ = false;
  }
}

void OOFCanvasLayer::destroy() {
  removeAllProps();
}

void OOFCanvasLayer::installContourMap() {
  vtkScalarsToColors *lut = get_lookupTable();
  assert(lut != 0);
  canvas->setContourMap(this, lut);
}

void OOFCanvasLayer::updateContourMap() {
  vtkScalarsToColors *lut = get_lookupTable();
  if(lut != 0)
    canvas->updateContourMap(this, lut);
}

vtkScalarsToColors *OOFCanvasLayer::get_lookupTable() {
  return 0;
}

vtkSmartPointer<vtkProp3D> OOFCanvasLayer::get_pickable_prop3d() {
  return vtkSmartPointer<vtkProp3D>();
}

vtkSmartPointer<vtkDataSet> OOFCanvasLayer::get_pickable_dataset() {
  return vtkSmartPointer<vtkDataSet>();
}

vtkSmartPointer<vtkPoints> OOFCanvasLayer::get_pickable_points() {
  return vtkSmartPointer<vtkPoints>();
}

vtkSmartPointer<vtkAbstractCellLocator> OOFCanvasLayer::get_locator() {
  return vtkSmartPointer<vtkAbstractCellLocator>();
}

bool OOFCanvasLayer::pickable() {
  return get_pickable_prop3d().GetPointer() != 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

vtkSmartPointer<vtkTableBasedClipDataSet> getClipper(
					     const OOFCanvasLayer *layer)

{
  // This used to return the input grid if getVTKClipPlanes returned a
  // null pointer, which it did if there were no clipping planes.  Now
  // it doesn't give special treatment to that case, other than
  // calling InsideOutOn, which makes the no-clipping-plane case do no
  // clipping.  Using a clipper when there's no actual clipping to be
  // done should be rare.
  const GhostOOFCanvas *canvas = layer->getCanvas();
  vtkSmartPointer<vtkPlanes> vplanes = canvas->getVTKClipPlanes();
  vtkSmartPointer<vtkTableBasedClipDataSet> clipper =
    vtkSmartPointer<vtkTableBasedClipDataSet>::New();
  clipper->SetClipFunction(vplanes);
  if(canvas->invertedClipping() || vplanes->GetNumberOfPlanes() == 0) {
    clipper->InsideOutOn();
  }
  return clipper;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SimpleCellLayer::SimpleCellLayer(GhostOOFCanvas *canvas, const std::string &nm)
  : OOFCanvasLayer(canvas, nm),
    grid(vtkSmartPointer<vtkUnstructuredGrid>::New()),
    actor(vtkSmartPointer<vtkActor>::New()),
    mapper(vtkSmartPointer<vtkDataSetMapper>::New())
{
  actor->SetMapper(mapper);
  addProp(actor);
}

SimpleCellLayer::~SimpleCellLayer() {}

void SimpleCellLayer::setModified() { 
  grid->Modified();
}

void SimpleCellLayer::clear() {
  grid->Initialize();
  number_cells = 0;
}

void SimpleCellLayer::newGrid(vtkSmartPointer<vtkPoints> pts, int ncells) {
  grid->Initialize();
  number_cells = ncells;
  if(ncells > 0)
    grid->Allocate(ncells, ncells);
  grid->SetPoints(pts);
}

void SimpleCellLayer::start_clipping() {
  clipper = getClipper(this);
  clipper->SetInputConnection(grid->GetProducerPort());
  mapper->SetInputConnection(clipper->GetOutputPort());
}

void SimpleCellLayer::stop_clipping() {
  if(clipState == CLIP_ON) {
    clipper->RemoveAllInputs();
    clipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
  }
  mapper->SetInputConnection(grid->GetProducerPort());
}

void SimpleCellLayer::set_clip_parity(bool inverted) {
  clipper->SetInsideOut(inverted);
}

void SimpleCellLayer::addCell(VTKCellType type,
			      vtkSmartPointer<vtkIdList> ptIds) 
{
  grid->InsertNextCell(type, ptIds);
}

void SimpleCellLayer::set_size(double size) {
  actor->GetProperty()->SetLineWidth(size);
  actor->GetProperty()->SetPointSize(size);
}

void SimpleCellLayer::set_color(const CColor &color) {
  actor->GetProperty()->SetColor(color.getRed(), color.getGreen(),
				 color.getBlue());
}

void SimpleCellLayer::set_opacity(double opacity) {
  actor->GetProperty()->SetOpacity(opacity);
}

int SimpleCellLayer::get_gridsize() const {
  return number_cells;
}

//=\\=//=\\=//=\\=//=\\=//

SimpleFilledCellLayer::SimpleFilledCellLayer(GhostOOFCanvas *canvas,
					     const std::string &nm)
  : SimpleCellLayer(canvas, nm)
{
  actor->GetProperty()->SetRepresentationToSurface();
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

const std::string &SimpleFilledCellLayer::classname() const {
  static const std::string nm("SimpleFilledCellLayer");
  return nm;
}


//=\\=//=\\=//=\\=//=\\=//

PickableFilledCellLayer::PickableFilledCellLayer(
			     GhostOOFCanvas *canvas, const std::string &nm)
  : SimpleFilledCellLayer(canvas, nm),
    locator(vtkSmartPointer<oofCellLocator>::New())
{
  locator->LazyEvaluationOn();
}

const std::string &PickableFilledCellLayer::classname() const {
  static const std::string nm("PickableFilledCellLayer");
  return nm;
}

vtkSmartPointer<vtkProp3D> PickableFilledCellLayer::get_pickable_prop3d() {
  return actor;
}

vtkSmartPointer<vtkDataSet> PickableFilledCellLayer::get_pickable_dataset() {
  return grid;
}

vtkSmartPointer<vtkPoints> PickableFilledCellLayer::get_pickable_points() {
  return grid->GetPoints();
}

vtkSmartPointer<vtkAbstractCellLocator> PickableFilledCellLayer::get_locator() {
  locator->Initialize();
  locator->SetDataSet(grid);
  return locator;
}

//=\\=//=\\=//=\\=//=\\=//

SimpleWireframeCellLayer::SimpleWireframeCellLayer(GhostOOFCanvas *canvas,
						   bool extract,
						   const std::string &nm)
  : SimpleCellLayer(canvas, nm),
    extract(extract)
{
  // 'extract' is true if edges should be extracted from the grid
  // before plotting.  It should be false if the grid is already a
  // grid of segments.  It's never changed after construction time.
  setup();
}

SimpleWireframeCellLayer::SimpleWireframeCellLayer(GhostOOFCanvas *canvas,
						   const std::string &nm)
  : SimpleCellLayer(canvas, nm),
    extract(true)
{
  setup();
}

void SimpleWireframeCellLayer::setup() {
  actor->GetProperty()->SetRepresentationToWireframe();
  if(extract) {
    edgeExtractor = vtkSmartPointer<vtkExtractEdges>::New();
    edgeExtractor->SetInputConnection(grid->GetProducerPort());
    mapper->SetInputConnection(edgeExtractor->GetOutputPort());
  }
  else {
    mapper->SetInputConnection(grid->GetProducerPort());
  }
  // set_clipping() completes the pipeline
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

void SimpleWireframeCellLayer::start_clipping() {
  // TODO 3.1: Add a vtkCutter
  clipper = getClipper(this);
  if(extract)
    clipper->SetInputConnection(edgeExtractor->GetOutputPort());
  else
    clipper->SetInputConnection(grid->GetProducerPort());
  mapper->SetInputConnection(clipper->GetOutputPort());
}

void SimpleWireframeCellLayer::stop_clipping() {
  // turn clipping off
  if(clipState == CLIP_ON) {
    clipper->RemoveAllInputs();
    clipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
  }
  if(extract)
    mapper->SetInputConnection(edgeExtractor->GetOutputPort());
  else
    mapper->SetInputConnection(grid->GetProducerPort());
}

void SimpleWireframeCellLayer::set_clip_parity(bool inverted) {
  clipper->SetInsideOut(inverted);
}

const std::string &SimpleWireframeCellLayer::classname() const {
  static const std::string nm("SimpleWireframeCellLayer");
  return nm;
}

void SimpleWireframeCellLayer::set_lineWidth(double w) {
  actor->GetProperty()->SetLineWidth(w);
}

//=\\=//=\\=//=\\=//=\\=//

SimplePointCellLayer::SimplePointCellLayer(GhostOOFCanvas *canvas,
					   const std::string &nm)
  : SimpleCellLayer(canvas, nm)
{
  actor->GetProperty()->SetRepresentationToPoints();
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

const std::string &SimplePointCellLayer::classname() const {
  static const std::string nm("SimplePointCellLayer");
  return nm;
}

void SimplePointCellLayer::set_pointSize(double p) {
  actor->GetProperty()->SetPointSize(p);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

GlyphedLayer::GlyphedLayer(GhostOOFCanvas *canvas, const std::string &name) 
  : SimpleCellLayer(canvas, name),
    glyphCenters(vtkSmartPointer<vtkPolyData>::New()),
    glyphDirections(vtkSmartPointer<vtkDoubleArray>::New()),
    glyphActor(vtkSmartPointer<vtkActor>::New()),
    glyph(vtkSmartPointer<vtkGlyph3D>::New()),
    centerFinder(vtkSmartPointer<vtkCellCenters>::New())
{
  glyphCenters = centerFinder->GetOutput();
  glyph->SetInput(glyphCenters);
  glyphDirections->SetNumberOfComponents(3);
  // addProp(glyphActor) is not called here because the input to
  // centerFinder can't be set until newGrid is called.

  // The mapper is not built here.  It's created by start_clipping()
  // or stop_clipping(), because the clipping state determines what
  // kind of vtkMapper must be used.
}

void GlyphedLayer::set_glyphColor(const CColor *color) {
  glyphActor->GetProperty()->SetColor(color->getRed(), color->getGreen(),
				      color->getBlue());
}

void GlyphedLayer::newGrid(vtkSmartPointer<vtkPoints> pts, int n) {
  SimpleCellLayer::newGrid(pts, n);
  glyphDirections->Reset();	// resize to empty, without freeing memory
  centerFinder->SetInputConnection(grid->GetProducerPort());
  glyphCenters->GetPointData()->SetNormals(glyphDirections);
  addProp(glyphActor);
}

void GlyphedLayer::setModified() {
  SimpleCellLayer::setModified();
  recomputeDirections();
}

void GlyphedLayer::addDirectedCell(VTKCellType type, vtkIdList *ptIds,
				   double direction[3]) 
{
  SimpleCellLayer::addCell(type, ptIds);
  glyphDirections->InsertNextTupleValue(direction);
}

void GlyphedLayer::start_clipping() {
  SimpleCellLayer::start_clipping();
  if(clipState == CLIP_OFF) {
    glyphMapper->RemoveAllInputs();
  }
  glyphClipper = getClipper(this);
  glyphClipper->SetInputConnection(glyph->GetOutputPort());
  glyphMapper = vtkSmartPointer<vtkDataSetMapper>::New();
  glyphMapper->SetInputConnection(glyphClipper->GetOutputPort());
  glyphActor->SetMapper(glyphMapper);
}

void GlyphedLayer::stop_clipping() {
  SimpleCellLayer::stop_clipping();
  if(clipState == CLIP_ON) {
    glyphClipper->RemoveAllInputs();
    glyphClipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
    glyphMapper->RemoveAllInputs();
  }
  glyphMapper = vtkSmartPointer<vtkPolyDataMapper>::New();
  glyphMapper->SetInputConnection(glyph->GetOutputPort());
  glyphActor->SetMapper(glyphMapper);
}

void GlyphedLayer::set_clip_parity(bool inverted) {
  SimpleCellLayer::set_clip_parity(inverted);
  glyphClipper->SetInsideOut(inverted);
}

//=\\=//=\\=//=\\=//=\\=//

ConeGlyphLayer::ConeGlyphLayer(GhostOOFCanvas *canvas, const std::string &name)
  : GlyphedLayer(canvas, name),
    coneSource(vtkSmartPointer<vtkConeSource>::New())
{
  glyph->SetSource(coneSource->GetOutput());
}

void ConeGlyphLayer::set_coneGeometry(double len, int resolution) {
  coneSource->SetRadius(0.5*len);
  coneSource->SetHeight(len);
  coneSource->SetResolution(resolution);
}

void ConeGlyphLayer::start_clipping() {
  GlyphedLayer::start_clipping();
  recomputeDirections();
}

void ConeGlyphLayer::stop_clipping() {
  GlyphedLayer::stop_clipping();
  recomputeDirections();
}
    
void ConeGlyphLayer::recomputeDirections() {
  if(glyphDirections->GetSize() > 0) {
    glyphCenters->Update();
    glyphCenters->GetPointData()->SetNormals(glyphDirections);
  }
}

//=\\=//=\\=//=\\=//=\\=//

FaceGlyphLayer::FaceGlyphLayer(GhostOOFCanvas *canvas, const std::string &name)
  : ConeGlyphLayer(canvas, name)
{
  actor->GetProperty()->SetRepresentationToSurface();
  glyph->OrientOn();
  glyph->SetVectorModeToUseNormal();
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

const std::string &FaceGlyphLayer::classname() const {
  static const std::string nm("FaceGlyphLayer");
  return nm;
}

//=\\=//=\\=//=\\=//=\\=//

EdgeGlyphLayer::EdgeGlyphLayer(GhostOOFCanvas *canvas, const std::string &name)
  : ConeGlyphLayer(canvas, name)
{
  actor->GetProperty()->SetRepresentationToWireframe();
  // actor->GetProperty()->SetRepresentationToSurface();
  glyph->OrientOn();
  glyph->SetVectorModeToUseNormal(); // glyph->SetVectorModeToUseVector() ?
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

const std::string &EdgeGlyphLayer::classname() const {
  static const std::string nm("EdgeGlyphLayer");
  return nm;
}

void EdgeGlyphLayer::set_lineWidth(double w) {
  actor->GetProperty()->SetLineWidth(w);
}

//=\\=//=\\=//=\\=//=\\=//

PointGlyphLayer::PointGlyphLayer(GhostOOFCanvas *canvas,
				 const std::string &name)
  : GlyphedLayer(canvas, name),
    sphereSource(vtkSmartPointer<vtkSphereSource>::New())
{
  glyph->ScalingOn();
  glyph->SetScaleFactor(1);
  glyph->OrientOff();
  glyph->SetSource(sphereSource->GetOutput());
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

const std::string &PointGlyphLayer::classname() const {
  static const std::string nm("PointGlyphLayer");
  return nm;
}

void PointGlyphLayer::set_sphereGeometry(double size, int resolution) {
  sphereSource->SetRadius(0.5*size);
  sphereSource->SetThetaResolution(resolution); // azimuth (!?)
  sphereSource->SetPhiResolution(resolution > 4? resolution/2 : 2); 
 }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SingleVoxelLayer::SingleVoxelLayer(GhostOOFCanvas *canvas,
				   const std::string &nm)
  : SimpleWireframeCellLayer(canvas, true, nm)
{}

// TODO 3.1: Add a vtkCutter to draw the intersections of the voxel faces
// with the clipping planes?

const std::string &SingleVoxelLayer::classname() const {
  static const std::string nm("SingleVoxelLayer");
  return nm;
}

void SingleVoxelLayer::set_voxel(const ICoord *where, const Coord *size) {
  // It should be possible to use the vtkPoints from the Image and get
  // the vtkCell corresponding to a voxel, instead of creating new
  // vtkPoints and a new vtkUnstructuredGrid to display the queried
  // voxel.  But with the current Microstructure it's not completely
  // trivial to access the vtkPoints.  Plus, doing it this way is
  // easy.
  grid->Initialize();
  grid->Allocate(1,1);
  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
  grid->SetPoints(points);
  points->Allocate(8, 8);
  double x0 = (*where)[0]*(*size)[0];
  double y0 = (*where)[1]*(*size)[1];
  double z0 = (*where)[2]*(*size)[2];
  double x1 = ((*where)[0] + 1)*(*size)[0];
  double y1 = ((*where)[1] + 1)*(*size)[1];
  double z1 = ((*where)[2] + 1)*(*size)[2];
  // See p 334 in the VTK User's Guide for the point ordering for VTK_VOXEL.
  points->InsertNextPoint(x0, y0, z0);
  points->InsertNextPoint(x1, y0, z0);
  points->InsertNextPoint(x0, y1, z0);
  points->InsertNextPoint(x1, y1, z0);
  points->InsertNextPoint(x0, y0, z1);
  points->InsertNextPoint(x1, y0, z1);
  points->InsertNextPoint(x0, y1, z1);
  points->InsertNextPoint(x1, y1, z1);

  vtkSmartPointer<vtkVoxel> voxel = vtkSmartPointer<vtkVoxel>::New();
  for(int i=0; i<8; ++i)
    voxel->GetPointIds()->SetId(i,i);
  grid->InsertNextCell(VTK_VOXEL, voxel->GetPointIds());
}
    
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The pipeline is:
// Image -> oofImageToGrid -> 
//    overlayers -> oofExcludeVoxels -> Clipper -> Mapper
// Overlayers, oofExcludeVoxels, and Clipper are all optional but must
// occur in that order if they're used.  There may be more than one
// instance of oofOverlayVoxels, or other similar operations, in the
// overlayers list.

// oofImageToGrid and oofOverlayVoxels are vtkRectilinearGridAlgorithms.
// oofExcludeVoxels and Clipper are vtkUnstructuredGridAlgorithms.
// vtkAlgorithm is a base class for Mapper, too.

// It might be tempting to use vtkImageDataGeometryFilter instead of
// oofImageToGrid, but it turns out to be no easier.
// vtkImageDataGeometryFilter creates a vtkPolyData object consisting
// of just vertex cells, and has the same off-by-one error that the
// original images do.  Modifying vtkImageDataGeometryFilter to make
// it work for us would gain nothing over using oofImageToGrid.

ImageCanvasLayer::ImageCanvasLayer(
			   GhostOOFCanvas *c,
			   const std::string &name)
  : OOFCanvasLayer(c, name),
    image(0),
    gridifier(vtkSmartPointer<oofImageToGrid>::New()),
    locator(vtkSmartPointer<vtkCellLocator>::New()),
    mapper(vtkSmartPointer<vtkDataSetMapper>::New()),
    actor(vtkSmartPointer<vtkActor>::New()),
    filter(0),
    bottomOverlayer(0),
    topOverlayer(0)
{
  addProp(actor);
  actor->SetMapper(mapper);
  locator->LazyEvaluationOn();
  
  // Build the initial pipeline, with no image and no excluded voxels.
  pipelineLock.acquire();
  downstreamSocket()->SetInputConnection(gridifier->GetOutputPort());
  pipelineLock.release();
  set_clipping(canvas->clipping(), canvas->invertedClipping());
}

ImageCanvasLayer::~ImageCanvasLayer() {}

const std::string &ImageCanvasLayer::classname() const {
  static const std::string nm("ImageCanvasLayer");
  return nm;
}

void ImageCanvasLayer::destroy() {
  OOFCanvasLayer::destroy();
}

void ImageCanvasLayer::setModified() {
  gridifier->Modified();
}

void ImageCanvasLayer::set_image(const ImageBase *img, const Coord *location,
				 const Coord *size)
{
  if(image != img) {
    pipelineLock.acquire();
    image = img;
    image->getVTKImageData()->Update();
    gridifier->SetInputConnection(image->getVTKImageData()->GetProducerPort());
    pipelineLock.release();
  }
}

void ImageCanvasLayer::noOverlayers() {
  // There are no overlayers.  Connect the grid directly to the
  // downstream pipeline socket.
  if(topOverlayer) {
    topOverlayer = 0;
    downstreamSocket()->SetInputConnection(gridifier->GetOutputPort());
  }
}

void ImageCanvasLayer::connectBottomOverlayer(ImageCanvasOverlayer *overlayer) {
  vtkSmartPointer<vtkAlgorithmOutput> gridOut = gridifier->GetOutputPort();
  if(overlayer != bottomOverlayer || bottomOverlayer->input != gridOut) {
    if(bottomOverlayer) {
      bottomOverlayer->disconnect();
    }
    bottomOverlayer = overlayer;
    overlayer->connectToAlgorithm(gridOut);
  }
}

void ImageCanvasLayer::connectTopOverlayer(ImageCanvasOverlayer *overlayer) {
  if(overlayer != topOverlayer) {
    topOverlayer = overlayer;
    downstreamSocket()->SetInputConnection(overlayer->output());
  }
}

vtkSmartPointer<vtkAlgorithm> ImageCanvasLayer::downstreamSocket() const {
  // Return the object that the downstream end of the overlayer
  // pipeline should be plugged into.
  if(excluder.GetPointer() != 0)
    return excluder;
  if(clipper.GetPointer() != 0)
    return clipper;
  return mapper;
}

vtkSmartPointer<vtkAlgorithmOutput> ImageCanvasLayer::overlayerOutput() {
  if(topOverlayer)
    return topOverlayer->output();
  return gridifier->GetOutputPort();
}

vtkSmartPointer<vtkAlgorithmOutput> ImageCanvasLayer::clipperInput() {
  if(excluder.GetPointer() != 0)
    return excluder->GetOutputPort();
  return overlayerOutput();
}

void ImageCanvasLayer::set_filter(VoxelFilter *condition) {
  // Voxel exclusion needs to be applied downstream from the
  // overlayers, because it creates a unstructured grid, but the
  // overlayers work on a rectilinear grid.
  pipelineLock.acquire();

  vtkSmartPointer<vtkAlgorithm> socket; // what the excluder connects to
  if(clipper.GetPointer() != 0)
    socket = clipper;
  else
    socket = mapper;

  if(condition != 0 && !condition->trivial()) {
    if(excluder.GetPointer() == 0) {
      // Create and connect a new excluder.
      excluder = vtkSmartPointer<oofExcludeVoxels>::New();
      // connect last overlay or grid to excluder input
      excluder->SetInputConnection(overlayerOutput());
      // connect excluder output to clipper or mapper
      socket->SetInputConnection(excluder->GetOutputPort());
    } 
    filter = condition;
    filter->setCanvasLayer(this);
    excluder->SetFilter(filter);
  }
  else {			// condition == 0, so no exclusion
    if(excluder.GetPointer() != 0) {
      // Remove existing excluder
      filter = 0;
      excluder = vtkSmartPointer<oofExcludeVoxels>();
      // connect last overlay or grid to clipper or mapper
      socket->SetInputConnection(overlayerOutput());
    }
  }
  pipelineLock.release();
}

void ImageCanvasLayer::start_clipping() {
  // TODO 3.1: Move pipelineLock to the base class?
  pipelineLock.acquire();
  // Create and connect a new clipper.
  assert(clipper.GetPointer() == 0);
  clipper = getClipper(this);
  clipper->SetInputConnection(clipperInput());
  mapper->SetInputConnection(clipper->GetOutputPort());
  pipelineLock.release();
}

void ImageCanvasLayer::stop_clipping() {
  // Disconnect and discard the existing clipper.
  pipelineLock.acquire();
  if(clipState == CLIP_ON) {
    assert(clipper.GetPointer() != 0);
    clipper->RemoveAllInputs();
    clipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
  }
  mapper->SetInputConnection(clipperInput());
  pipelineLock.release();
}

void ImageCanvasLayer::set_clip_parity(bool inverted) {
  pipelineLock.acquire();
  clipper->SetInsideOut(inverted);
  pipelineLock.release();
}

vtkSmartPointer<vtkProp3D> ImageCanvasLayer::get_pickable_prop3d() {
  return actor;
}

vtkSmartPointer<vtkAbstractCellLocator> ImageCanvasLayer::get_locator() {
  // If the locator isn't reinitialized here, voxel picks that are
  // made after the layer is edited (eg, clipped or filtered) can fail
  // or crash.  
  //* TODO OPT: It shouldn't be necessary to reinitialize every time.
  //* Rebuilding the locator might be slow for large images.  Should it
  //* be done only after the layer has been edited?  What if the pixel
  //* group for a filter has changed?
  locator->Initialize();
  locator->LazyEvaluationOn();
  locator->SetDataSet(get_pickable_dataset());
  return locator;
}

vtkSmartPointer<vtkDataSet> ImageCanvasLayer::get_pickable_dataset() {
  // mapper->Update();
  return mapper->GetInput();
}
    
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ImageCanvasOverlayer::ImageCanvasOverlayer(
	   GhostOOFCanvas *canvas, const std::string &nm,
	   vtkSmartPointer<vtkRectilinearGridAlgorithm> alg)
  : OOFCanvasLayerBase(canvas, nm),
    algorithm(alg),
    input(vtkSmartPointer<vtkAlgorithmOutput>())
{
  // oofcerr << "ImageCanvasOverlayer::ctor: " << this << " " << name()
  // 	  << std::endl;
}

ImageCanvasOverlayer::~ImageCanvasOverlayer() {}

void ImageCanvasOverlayer::setModified() {
  algorithm->Modified();
}

void ImageCanvasOverlayer::disconnect() {
  if(input.GetPointer() != 0) {
    algorithm->RemoveAllInputs();
    input = vtkSmartPointer<vtkAlgorithmOutput>();
  }
}

void ImageCanvasOverlayer::connectToAlgorithm(
			      vtkSmartPointer<vtkAlgorithmOutput> inp)
{
  if(inp != input) {
    disconnect();
    algorithm->SetInputConnection(inp);
    input = inp;
  }
}

void ImageCanvasOverlayer::connectToOverlayer(ImageCanvasOverlayer *other) {
  connectToAlgorithm(other->output());
}

vtkSmartPointer<vtkAlgorithmOutput> ImageCanvasOverlayer::output() {
  return algorithm->GetOutputPort();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

OverlayVoxels::OverlayVoxels(GhostOOFCanvas *canvas, const std::string &name)
  : ImageCanvasOverlayer(canvas, name, vtkSmartPointer<oofOverlayVoxels>::New())
{}

const std::string &OverlayVoxels::classname() const {
  static const std::string nm("OverlayVoxels");
  return nm;
}

void OverlayVoxels::setTintOpacity(double opacity) {
  oofOverlayVoxels::SafeDownCast(algorithm)->SetOpacity(opacity);
}

void OverlayVoxels::setColor(const CColor *color) {
  double r = color->getRed();
  double g = color->getGreen();
  double b = color->getBlue();
  double x[] = {r, g, b};
  oofOverlayVoxels::SafeDownCast(algorithm)->SetColor(x);
}

void OverlayVoxels::setPixelSet(PixelSet *pixset) {
  oofOverlayVoxels::SafeDownCast(algorithm)->SetPixelSet(pixset);
}

void OverlayVoxels::clearPixelSet() {
  oofOverlayVoxels::SafeDownCast(algorithm)->SetPixelSet(0);
}
