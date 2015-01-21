// -*- C++ -*-
// $RCSfile: ghostoofcanvas.C,v $
// $Revision: 1.1.2.171 $
// $Author: langer $
// $Date: 2014/11/24 21:44:49 $

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
#include "common/IO/imageformat.h"
#include "common/IO/oofcerr.h"
#include "common/IO/view.h"
#include "common/coord.h"
#include "common/ooferror.h"
#include "common/printvec.h"
#include "common/threadstate.h"

#include <iostream>
#include <limits>
#include <math.h>

#include <vtkAreaPicker.h>
#include <vtkCamera.h>
#include <vtkCaptionActor2D.h>
#include <vtkCellPicker.h>
#include <vtkDataSet.h>
#include <vtkDataSetMapper.h>
#include <vtkExtractSelectedFrustum.h>
#include <vtkPointPicker.h>
#include <vtkProp3D.h>
#include <vtkProp3DCollection.h>
#include <vtkProperty.h>
#include <vtkProperty2D.h>
#include <vtkTextActor.h>
#include <vtkTextProperty.h>
#include <vtkTransform.h>
#include <vtkVolume.h>
#include <vtkVolumeCollection.h>
#include <vtkVolumeProperty.h>

#include <vtkPropCollection.h>
#include <vtkAssemblyPath.h>

// "initialized" is used by the OOFCanvas and OOFCanvas3D
// constructors.
bool GhostOOFCanvas::initialized = 0;

GhostOOFCanvas::GhostOOFCanvas() 
  : created(false),
    exposed(false),
    rendered(false),
    axes_showing(false),
    render_window(vtkSmartPointer<vtkXOpenGLRenderWindow>::New()),
    renderer(vtkSmartPointer<vtkRenderer>::New()),
    axes(vtkSmartPointer<vtkAxesActor>::New()),
    contourMapActor(vtkSmartPointer<vtkScalarBarActor>::New()),
    contourmap_requested(true),
    contourmap_showing(false),
    contour_layer(0),
    clipInverted(false),
    clipSuppressed(false),
    vClipPlanes(vtkSmartPointer<vtkPlanes>::New()),
    margin(.10)
{
  assert(mainthread_query());
  render_window->AddRenderer(renderer);
  // Choose an arbitrary size for the render window.  This will be
  // reset when the window is actually displayed, but if we're in text
  // mode the window won't ever be displayed.  The size must be set or
  // findClickedCell_, et al, will seg fault.
  render_window->SetSize(1000, 1000);

  // Some of these initial settings will be overwritten by
  // GfxWindow3D.postinitialize().
#if VTK_MAJOR_VERSION == 5 && VTK_MINOR_VERSION > 8
  contourMapActor->DrawBackgroundOn();
  contourMapActor->DrawFrameOn();
  vtkProperty2D *prop = contourMapActor->GetBackgroundProperty();
  prop->SetColor(0.5, 0.5, 0.5);
  prop->SetOpacity(0.5);
  prop = contourMapActor->GetFrameProperty();
  prop->SetColor(0, 0, 0);
# endif
  vtkTextProperty *tprop = contourMapActor->GetLabelTextProperty();
  tprop->ItalicOff();
  tprop->SetColor(0, 0, 0);
  tprop->ShadowOff();
  
  axes->GetXAxisCaptionActor2D()->GetCaptionTextProperty()->ShadowOff();
  axes->GetYAxisCaptionActor2D()->GetCaptionTextProperty()->ShadowOff();
  axes->GetZAxisCaptionActor2D()->GetCaptionTextProperty()->ShadowOff();

  axes->GetXAxisCaptionActor2D()->GetProperty()->
    SetDisplayLocationToBackground();
  axes->GetYAxisCaptionActor2D()->GetProperty()->
    SetDisplayLocationToBackground();
  axes->GetZAxisCaptionActor2D()->GetProperty()->
    SetDisplayLocationToBackground();
}

GhostOOFCanvas::~GhostOOFCanvas() {
  //layers.clear();
}

void GhostOOFCanvas::toggleAxes(bool show) {
  assert(mainthread_query());
  if(show && !axes_showing) {
    setAxisProperties();
    renderer->AddActor(axes);
    axes_showing = true;
  }
  else if(!show and axes_showing) {
    renderer->RemoveActor(axes);
    axes_showing = false;
  }
}

// This should only be called from python and only with mainthread.run

void GhostOOFCanvas::render() {
  // TODO OPT: Why is this called so often, for example, after Skeleton
  // refinement?  Does it matter? 
  assert(mainthread_query());
  if(exposed) {
    if(contourmap_requested && contour_layer!=0 && !contourmap_showing) {
      renderer->AddViewProp(contourMapActor);
      contourmap_showing = true;
    }
    else if(!(contourmap_requested && contour_layer!=0) && contourmap_showing) {
      renderer->RemoveViewProp(contourMapActor);
      contourmap_showing = false;
    }
    
    renderLock.acquire();
    try {
      // oofcerr << "GhostOOFCanvas::render: " << this << std::endl;
      render_window->Render(); 
    }
    catch(...) {
      renderLock.release();
      throw;
    }
    renderLock.release();
  }
}

void GhostOOFCanvas::newLayer(OOFCanvasLayerBase *layer) {
  layers.push_back(layer);
}

void GhostOOFCanvas::removeLayer(OOFCanvasLayerBase *layer) {
  for(CanvasLayerList::iterator i=layers.begin(); i<layers.end(); ++i) {
    if(*i == layer) {
      layers.erase(i);
      return;
    }
  }
  throw ErrProgrammingError("Layer not found!", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Settable axis parameters are set by postinitialize in
// gfxwindow3d.py.

void GhostOOFCanvas::setAxisOffset(const Coord *offset) {
  assert(mainthread_query());
  vtkSmartPointer<vtkTransform> transf = vtkSmartPointer<vtkTransform>::New();
  transf->Translate((*offset)[0], (*offset)[1], (*offset)[2]);
  axes->SetUserTransform(transf);
}

void GhostOOFCanvas::setAxisLength(const Coord *lengths) {
  assert(mainthread_query());
  axes->SetTotalLength((*lengths)[0], (*lengths)[1], (*lengths)[2]);
  // double avgL = ((*lengths)(0) + (*lengths)(1) + (*lengths)(2))/3.;
  // axes->SetConeRadius(avgL/50.);
  setAxisProperties();
}

void GhostOOFCanvas::showAxisLabels(bool show) {
  assert(mainthread_query());
  axes->SetAxisLabels(show);
}

void GhostOOFCanvas::setAxisLabelColor(const CColor *color) {
  assert(mainthread_query());
  double r = color->getRed();
  double g = color->getGreen();
  double b = color->getBlue();
  axes->GetXAxisCaptionActor2D()->GetCaptionTextProperty()->SetColor(r, g, b);
  axes->GetYAxisCaptionActor2D()->GetCaptionTextProperty()->SetColor(r, g, b);
  axes->GetZAxisCaptionActor2D()->GetCaptionTextProperty()->SetColor(r, g, b);
}

void GhostOOFCanvas::setAxisLabelFontSize(int size) {
  assert(mainthread_query());
  axes->GetXAxisCaptionActor2D()->GetTextActor()->SetTextScaleModeToNone();
  axes->GetYAxisCaptionActor2D()->GetTextActor()->SetTextScaleModeToNone();
  axes->GetZAxisCaptionActor2D()->GetTextActor()->SetTextScaleModeToNone();
  axes->GetXAxisCaptionActor2D()->GetCaptionTextProperty()->SetFontSize(size);
  axes->GetYAxisCaptionActor2D()->GetCaptionTextProperty()->SetFontSize(size);
  axes->GetZAxisCaptionActor2D()->GetCaptionTextProperty()->SetFontSize(size);
}

void GhostOOFCanvas::setAxisProperties() {
  assert(mainthread_query());
  // Set properties that depend on other user-settable properties.
  double *lengths = axes->GetTotalLength();
  // refLength is the length that the arrow size is proportional to.
  // Using the average length of the axes seems like a reasonable
  // thing, although it might make more sense to use the minimum if
  // the microstructure has an extreme aspect ratio.
  double refLength = (lengths[0] + lengths[1] + lengths[2])/3.;
  Coord relativeTipSizes;
  Coord relativeShaftLengths;
  double actualTipLength = 0.05*refLength;
  for(int i=0; i<3; i++) {
    relativeTipSizes[i] = actualTipLength/lengths[i]; // relative size
    relativeShaftLengths[i] = 1 - relativeTipSizes[i];
  }
  axes->SetNormalizedTipLength(relativeTipSizes);
  axes->SetNormalizedShaftLength(relativeShaftLengths);
  // The cone radius is relative to the cone length.  The default
  // value is 0.4, which is good enough.  We could tweak it like this
  // if we wanted to:
  // axes->SetConeRadius(0.1);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void GhostOOFCanvas::noContourMap() {
  // Called by GhostGfxWindow.newLayerMembers to indicate that no
  // layer can be contoured.
  contour_layer = 0;
}

void GhostOOFCanvas::setContourMap(OOFCanvasLayer *layer, 
				   vtkScalarsToColors *lut)
{
  // Called by OOFCanvasLayer::installContourMap to define the lookup
  // table for the contour map for the topmost contourable layer.
  assert(mainthread_query());
  contour_layer = layer;
  contourMapActor->SetLookupTable(lut);
}

void GhostOOFCanvas::updateContourMap(OOFCanvasLayer *layer,
				      vtkScalarsToColors *lut)
{
  // Called by OOFCanvasLayer subclasses when their contour map has
  // changed.
  assert(mainthread_query());
  if(layer == contour_layer)
    contourMapActor->SetLookupTable(lut);
}

void GhostOOFCanvas::showContourMap(bool show) {
  // Called by the menus.  Indicates whether or not the user wants the
  // contour map to be displayed.
  contourmap_requested = show;
}

void GhostOOFCanvas::setContourMapBGColor(const CColor *color, float opacity) {
  assert(mainthread_query());
#if VTK_MAJOR_VERSION == 5 && VTK_MINOR_VERSION > 8
  vtkProperty2D *prop = contourMapActor->GetBackgroundProperty();
  prop->SetColor(color->getRed(), color->getGreen(), color->getBlue());
  prop->SetOpacity(opacity);
#endif
}

void GhostOOFCanvas::setContourMapTextColor( const CColor *color) {
  // Text size is not settable in vtkScalarBarActor.  The largest font
  // that fits is used automatically.
  assert(mainthread_query());
  vtkTextProperty *prop = contourMapActor->GetLabelTextProperty();
  prop->SetColor(color->getRed(), color->getGreen(), color->getBlue());
}

void GhostOOFCanvas::setContourMapPosition(float x, float y) {
  assert(mainthread_query());
  contourMapActor->SetPosition(x, y);
}

void GhostOOFCanvas::setContourMapSize(float w, float h) {
  assert(mainthread_query());
  contourMapActor->SetWidth(w);
  contourMapActor->SetHeight(h);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void GhostOOFCanvas::setAntiAlias(bool antialias) {
  assert(mainthread_query());
  if(antialias)
    render_window->SetAAFrames(6);
  else
    render_window->SetAAFrames(0);
}

void GhostOOFCanvas::set_bgColor(CColor color) {
  assert(mainthread_query());
  renderer->SetBackground(color.getRed(), color.getGreen(), color.getBlue());
}

void GhostOOFCanvas::orthogonalize_view_up() {
  assert(mainthread_query());
  renderer->GetActiveCamera()->OrthogonalizeViewUp();
}

Coord GhostOOFCanvas::get_visible_center() const {
  assert(mainthread_query());
  double *bounds = renderer->ComputeVisiblePropBounds();
  return 0.5*Coord(bounds[0] + bounds[1],
		   bounds[2] + bounds[3],
		   bounds[4] + bounds[5]);
}

Coord GhostOOFCanvas::get_visible_size() const {
  double *bounds = renderer->ComputeVisiblePropBounds();
  return Coord(bounds[1] - bounds[0],
	       bounds[3] - bounds[2],
	       bounds[5] - bounds[4]);
}

// get_size() shouldn't really return an ICoord, since the return
// value only has two dimensions even in oof3D. However, using an
// ICoord is convenient, we don't have another structure handy, and
// the routine is only use by GfxWindow3D.getCanvasSize(), which is
// only used in the gui logger.  TODO LATER: If get_size() is used
// more widely, it would make sense for it to return a two dimensional
// ICoord equivalent.

ICoord GhostOOFCanvas::get_size() const {
  assert(mainthread_query());
  int *vtksz = render_window->GetSize();
  return ICoord(vtksz[0], vtksz[1], 0);
}

void GhostOOFCanvas::set_size(int width, int height) {
  assert(mainthread_query());
  render_window->SetSize(width, height);
}

void GhostOOFCanvas::recalculate_clipping() {
  assert(mainthread_query());
  renderer->ResetCameraClippingRange();
}

bool GhostOOFCanvas::clipping() const {
  if(clipSuppressed) 
    return false;
  for(ClippingPlaneList::const_iterator i=clipPlanes.begin(); 
      i<clipPlanes.end(); ++i) 
    {
      if((*i).enabled())
	return true;
    }
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Camera controls

void GhostOOFCanvas::reset() {
  assert(mainthread_query());
  if(axes_showing)
    renderer->RemoveActor(axes);
  renderer->ResetCamera();
  if(axes_showing)
    renderer->AddActor(axes);
}

void GhostOOFCanvas::track(double x, double y, double z) {
  assert(mainthread_query());
  Coord pPoint;
  Coord fPoint;
  renderer->GetActiveCamera()->GetPosition(pPoint);
  renderer->GetActiveCamera()->GetFocalPoint(fPoint);
  renderer->GetActiveCamera()->SetPosition(x + pPoint[0], y + pPoint[1],
					   z + pPoint[2]);
  renderer->GetActiveCamera()->SetFocalPoint(x + fPoint[0], y + fPoint[1],
					     z + fPoint[2]);
}

void GhostOOFCanvas::dolly(double factor) {
  assert(mainthread_query());
  renderer->GetActiveCamera()->Dolly(factor);
}

void GhostOOFCanvas::recenter() {
  // Move the focal point to the center of the visible region.  Move
  // the camera the same amount, so that its orientation and distance
  // from the focal point aren't changed.
  assert(mainthread_query());
  double d = renderer->GetActiveCamera()->GetDistance();
  Coord dop;
  renderer->GetActiveCamera()->GetDirectionOfProjection(dop);
  const double *bounds = renderer->ComputeVisiblePropBounds();
  Coord fp = Coord(bounds[1]/2.0, bounds[3]/2.0, bounds[5]/2.0);
  renderer->GetActiveCamera()->SetFocalPoint(fp);
  renderer->GetActiveCamera()->SetPosition(fp[0]-d*dop[0], fp[1]-d*dop[1],
					   fp[2]-d*dop[2]);
}

void GhostOOFCanvas::dolly_fill() {
  // From the documentation for ResetCamera: "Automatically set up the
  // camera based on the visible actors. The camera will reposition
  // itself to view the center point of the actors, and move along its
  // initial view plane normal (i.e., vector defined from camera
  // position to focal point) so that all of the actors can be seen."
  // Since the AxesActor is invisibly symmetric about its origin,
  // filling will leave too much space on the negative side when axes
  // are being drawn.  Temporarily remove them if necessary.  (It
  // doesn't appear to be necessary to remove the contour map.)
  
  assert(mainthread_query());
  if(axes_showing)
    renderer->RemoveActor(axes);

  const double *bounds = renderer->ComputeVisiblePropBounds();
  double newbounds[6];
  for(int i=0; i<3; i++) {
    double c = 0.5*(bounds[2*i+1] + bounds[2*i]);
    double r = 0.5*(bounds[2*i+1] - bounds[2*i]) * (1 + margin);
    newbounds[2*i] = c - r;
    newbounds[2*i + 1] = c + r;
  }
  renderer->ResetCamera(newbounds);
  if(axes_showing)
    renderer->AddActor(axes);
}

void GhostOOFCanvas::zoom(double a) {
  assert(mainthread_query());
  renderer->GetActiveCamera()->Zoom(a); 
}

void GhostOOFCanvas::zoom_fill() {
  assert(mainthread_query());
  recenter();
  // Compute the maximum absolute value of the view coordinates of all
  // displayed objects.  View coordinates are in the [-1,1]x[-1,1]
  // square.
  
  // See comment in dolly_fill about axes. 
  // TODO OPT: Does this have to remove the contour map too?
  if(axes_showing)
    renderer->RemoveActor(axes);
  const double *bounds = renderer->ComputeVisiblePropBounds();
  if(axes_showing)
    renderer->AddActor(axes);
  double maxviewcoord = 0;
  for(int i=0; i<2; i++)
    for(int j=2; j<4; j++)
      for(int k=4; k<6; k++) {
	// (bounds[i], bounds[j], bounds[k]) is a corner of the bounding box
	renderer->SetWorldPoint(bounds[i], bounds[j], bounds[k], 1.0);
	renderer->WorldToView();
	double *view = renderer->GetViewPoint();
	double absx = fabs(view[0]);
	double absy = fabs(view[1]);
	if(absx > maxviewcoord) maxviewcoord = absx;
	if(absy > maxviewcoord) maxviewcoord = absy;
      }
  // Scale the tangent of the camera view angle so that the maximum
  // coord is 1-margin instead of maxviewcoord.
  double oldangle = M_PI/180*renderer->GetActiveCamera()->GetViewAngle();
  double newangle = atan(maxviewcoord/(1-margin)*tan(oldangle));
  renderer->GetActiveCamera()->SetViewAngle(180/M_PI*newangle);
}

void GhostOOFCanvas::roll(double a) {
  assert(mainthread_query());
  renderer->GetActiveCamera()->Roll(a); 
}

void GhostOOFCanvas::pitch(double a) {
  assert(mainthread_query());
  renderer->GetActiveCamera()->Pitch(a); 
}
void GhostOOFCanvas::yaw(double a) {
  assert(mainthread_query());
  renderer->GetActiveCamera()->Yaw(a); 
}

void GhostOOFCanvas::azimuth(double a) { 
  assert(mainthread_query());
  renderer->GetActiveCamera()->Azimuth(a); 
}

void GhostOOFCanvas::elevation(double a) {
  assert(mainthread_query());
  renderer->GetActiveCamera()->Elevation(a); 
}

Coord GhostOOFCanvas::get_camera_position() const {
  Coord p;
  assert(mainthread_query());
  renderer->GetActiveCamera()->GetPosition(p.xpointer());
  return p;
}

void GhostOOFCanvas::set_camera_position(double x, double y, double z) const {
  assert(mainthread_query());
  renderer->GetActiveCamera()->SetPosition(x,y,z);
}

void GhostOOFCanvas::get_camera_focal_point(double *p) const {
  assert(mainthread_query());
  renderer->GetActiveCamera()->GetFocalPoint(p);
}

void GhostOOFCanvas::set_camera_focal_point(double x, double y, double z) const
{
  assert(mainthread_query());
  renderer->GetActiveCamera()->SetFocalPoint(x,y,z);
}

void GhostOOFCanvas::get_camera_view_up(double *p) const {
  assert(mainthread_query());
  renderer->GetActiveCamera()->GetViewUp(p);
}

void GhostOOFCanvas::get_camera_direction_of_projection(double *p) const {
  assert(mainthread_query());
  renderer->GetActiveCamera()->GetDirectionOfProjection(p);
}

double GhostOOFCanvas::get_camera_distance() const {
  assert(mainthread_query());
  return renderer->GetActiveCamera()->GetDistance();
}

double GhostOOFCanvas::get_camera_view_angle() const {
  assert(mainthread_query());
  return renderer->GetActiveCamera()->GetViewAngle();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Routines for handling mouse clicks.  The way in which the 2D
// coordinates of a click are translated into a 3D position depend on
// what's being clicked on, so there are multiple ways of doing it.

Coord GhostOOFCanvas::findRayThroughPoint(const Coord &point) 
  const
{
  // Given a point in world coordinates, compute the line passing
  // through that point and the camera, and return a unit vector along
  // the line.
  vtkCamera *camera = renderer->GetActiveCamera();
  Coord cameraPos(camera->GetPosition());
  Coord ray = point - cameraPos;
  ray /= sqrt(norm2(ray));		// normalized
  return ray;
}

void GhostOOFCanvas::findClickedCell_(const Coord *click, const View *view,
				      OOFCanvasLayer *layer,
				      vtkSmartPointer<vtkCell> &cell, 
				      Coord &pos, vtkIdType &cellId,
				      int &subId) 
{
  // oofcerr << "GhostOOFCanvas::findClickedCell_: click=" << *click
  // 	  << std::endl;
  
  // TODO MERGE: click is a Coord although it really should be an ICoord.
  // This is because in *2D* the conversion from screen to physical
  // coords is done by the canvas before invoking any mouse callbacks.
  // 2D and 3D share some of the mouse callback machinery (see
  // genericselecttoolbox.py), so the 3D arguments are the same type
  // as the 2D arguments.  The 3D points are raw screen coords (and
  // therefore should be ICoords) because the conversion from screen
  // to physical coordinates can't be done generically in 3D; it
  // depends on what's being clicked on.  The reason for converting
  // the points early in 2D is so that the physical coords appear in
  // the log file, and log files can therefore be replayed even if the
  // graphics window changes size or other view parameters change.  In
  // 3D, log file portability is achieved by passing the View as a
  // menu arg.  There's no need to add this extra complexity to 2D.

  assert(mainthread_query());

  vtkSmartPointer<vtkProp3D> prop = layer->get_pickable_prop3d();
  assert(prop.GetPointer() != 0);
  // oofcerr << "GhostOOFCanvas::findClickedCell_: prop=" << prop.GetPointer()
  // 	  << std::endl;

  // Sometimes the selecting is done on an object that's not actually
  // displayed.  To be clickable, the vtkProp3D has to be added to the
  // vtkRenderer, but it doesn't have to actually be rendered, so here
  // we add it if necessary, and remove it at the end.
  bool propIsRendered = renderer->HasViewProp(prop);
  if(!propIsRendered) {
    renderer->AddViewProp(prop);
  }

  makeAllUnpickable();
  
  viewLock.acquire();
  View *oldView = set_view_nolock(view, true);

  bool clickOk = false;

  try {
    // The locator and dataset must be obtained *after* the view is
    // set.
    vtkSmartPointer<vtkDataSet> dataset = layer->get_pickable_dataset();
    dataset->Update();
    vtkSmartPointer<vtkAbstractCellLocator> locator = layer->get_locator();
    assert(locator.GetPointer() != 0);
    vtkSmartPointer<vtkCellPicker> picker = 
      vtkSmartPointer<vtkCellPicker>::New();
    picker->AddLocator(locator);	// requires vtk >= 5.6

    prop->PickableOn();

    // Compute the display coordinates of the click.
    double x, y;
    physical2Display(*click, x, y);
    // oofcerr << "GhostOOFCanvas::findClickedCell_: x=" << x << " y=" << y 
    // 	    << std::endl;

    // Try to pick something.
    if(picker->Pick(x, y, 0.0, renderer)) {
      vtkSmartPointer<vtkProp3DCollection> props = picker->GetProp3Ds();
      int nprops = props->GetNumberOfItems();
      // When a click command is loaded from a file and the clipping
      // state in the command is different from the current state,
      // more than one Prop3D can be picked, somehow. (Is that still
      // true?) But it seems that the picked positions are all the
      // same, so it doesn't matter, since we only use the position
      // and not the Prop3D.  This code used to throw an exception if
      // nprops>1.
      if(nprops > 0) {
	vtkSmartPointer<vtkPoints> points = picker->GetPickedPositions();
	// if(nprops > 1) {
	//   for(int i=0; i<nprops; i++) 
	//     oofcerr << "GhostOOFCanvas::findClickedCell_: position="
	// 	    << Coord(points->GetPoint(i)) << std::endl;
	// }
	Coord pickedPoint;
	points->GetPoint(0, pickedPoint);
	// oofcerr << "GhostOOFCanvas::findClickedCell_: nPoints=" 
	// 	<< points->GetNumberOfPoints() << " pickedPoint="
	// 	<< Coord(pickedPoint) << std::endl;

	// TODO OPT: If we only want the position and not the cell, is it
	// possible to skip FindClosestPoint?
	Coord closestPt;
	double distance;
	locator->FindClosestPoint(pickedPoint, closestPt, cellId, subId,
				  distance);
	pos = Coord(closestPt);
	cell = vtkSmartPointer<vtkCell>(dataset->GetCell(cellId));

 	// vtkSmartPointer<vtkPoints> pts = cell->GetPoints();
	// oofcerr << "GhostOOFCanvas::findClickedCell_: cell info "
	// 	<< pts->GetNumberOfPoints()
	// 	<< " points=" << std::endl;
	// for(int i=0; i<cell->GetNumberOfPoints(); i++) {
	//   vtkIdType p = cell->GetPointId(i);
	//   oofcerr << "   " << p << " " << Coord(pts->GetPoint(i))
	// 	  << std::endl;
	// }
	
	clickOk = true;
      }	// end if nprops > 0
    } // end if(picker->Pick(...))
    // else {			// picker->Pick returned 0
    //   oofcerr << "GhostOOFCanvas::findClickedCell_: Pick failed!"
    // 	      << std::endl;
    // }
  }
  catch(...) {
    if(!propIsRendered) {
      renderer->RemoveViewProp(prop);
    }
    restore_view(oldView, true);
    delete oldView;
    viewLock.release();
    throw;
  }
  if(!propIsRendered) {
    renderer->RemoveViewProp(prop);
    // Calling render() here is not necessary.
  }
  restore_view(oldView, true);
  delete oldView;
  viewLock.release();
  if(!clickOk) {
    throw ErrClickError();
  }
} // GhostOOFCanvas::findClickedCell_


vtkSmartPointer<vtkCell> GhostOOFCanvas::findClickedCell(
		 const Coord *click, const View *view, OOFCanvasLayer *layer)
{
  assert(mainthread_query());
  vtkSmartPointer<vtkCell> cell;
  Coord pos;
  vtkIdType cellId;
  int subId;
  findClickedCell_(click, view, layer, cell, pos, cellId, subId);
  return cell;
}

vtkIdType GhostOOFCanvas::findClickedCellID(
    const Coord *click, const View *view, OOFCanvasLayer *layer, Coord *pos)
{
  assert(mainthread_query());
  vtkSmartPointer<vtkCell> cell;
  vtkIdType cellId;
  int subId;
  findClickedCell_(click, view, layer, cell, *pos, cellId, subId);
  return cellId;
}

Coord *GhostOOFCanvas::findClickedCellCenter(
		    const Coord *click, const View *view, OOFCanvasLayer *layer)
{
  assert(mainthread_query());
  vtkSmartPointer<vtkCell> cell;
  Coord pos;
  vtkIdType cellId;
  int subId;
  findClickedCell_(click, view, layer, cell, pos, cellId, subId);
  
  Coord pcenter;		// parametric center
  cell->GetParametricCenter(pcenter);
  Coord center;
  double weights[cell->GetNumberOfPoints()];
  cell->EvaluateLocation(subId, pcenter, center, weights);
  return new Coord(center);
} // GhostOOFCanvas::findClickedCellCenter

// findClickedPosition returns the coordinates of a click on any kind
// of vtkCell.  The returned position is not necessarily a grid point
// for the layer.  Compare to findClickedPoint, which chooses a vertex
// cell from a set of points.

// If the line from the camera to the clicked position intersects the
// cell in more than one spot, it's not clear whether the returned
// position is guaranteed to be the intersection closest to the
// camera.  It appears to work that way (when using oofCellLocator
// instead of vtkCellLocator), but I don't see where it's guaranteed.

Coord *GhostOOFCanvas::findClickedPosition(
		   const Coord *click, const View *view, OOFCanvasLayer *layer)
{
  assert(mainthread_query());
  vtkSmartPointer<vtkCell> cell;
  vtkIdType cellId;
  int subId;
  Coord *pos = new Coord();
  findClickedCell_(click, view, layer, cell, *pos, cellId, subId);
  return pos;
} // GhostOOFCanvas::findClickedPosition

vtkSmartPointer<vtkIdList> GhostOOFCanvas::findClickedFace(
	      const Coord *click, const View *view, OOFCanvasLayer *layer)
{
  assert(mainthread_query());
  vtkSmartPointer<vtkCell> cell;
  vtkIdType cellId;
  int subId;
  Coord pos;
  findClickedCell_(click, view, layer, cell, pos, cellId, subId);
  int nFaces = cell->GetNumberOfFaces();
  if(nFaces == 0)
    return vtkSmartPointer<vtkIdList>();
  if(nFaces == 1)
    return cell->GetPointIds();

  // Construct a new pickable layer whose cells are the faces of the
  // previously picked cell.
  PickableFilledCellLayer tetlayer(this, "FaceSelector");
  vtkSmartPointer<vtkPoints> points = layer->get_pickable_points();
  tetlayer.newGrid(points, nFaces);
  for(int i=0; i<nFaces; i++) {
    vtkSmartPointer<vtkCell> face = cell->GetFace(i);
    vtkSmartPointer<vtkIdList> ptids = face->GetPointIds();
    tetlayer.addCell(VTK_TRIANGLE, ptids);
  } // end loop over faces
  // Pick one of the faces...
  try {
    findClickedCell_(click, view, &tetlayer, cell, pos, cellId, subId);
  }
  catch (...) {			// in case findClickedCell_ fails
    tetlayer.destroy();
    throw;
  }
  tetlayer.destroy();
  return cell->GetPointIds();
} // GhostOOFCanvas::findClickedFace

vtkSmartPointer<vtkUnstructuredGrid> GhostOOFCanvas::getFrustumSubgrid(
	       double x, double y, const View *view, OOFCanvasLayer *layer)
{
  // Use a vtkAreaPicker to get the frustum for the chosen pixel.
  // Input values x and y are display coordinates.
  //* TODO OPT: It's probably faster to compute the frustum by hand, using
  //* the camera parameters.  vtkAreaPicker is probably doing a lot of
  //* extra work. Is there a better vtk method to do this?  On the
  //* other hand, this isn't called often.

  assert(mainthread_query());
  vtkSmartPointer<vtkUnstructuredGrid> subgrid;
  makeAllUnpickable();
  vtkSmartPointer<vtkAreaPicker> picker = 
    vtkSmartPointer<vtkAreaPicker>::New();
  picker->AreaPick(x, y, x+1, y+1, renderer);
  // Extract a vtkUnstructuredGrid that contains just the cells that
  // intersect the frustum.  This will include only vtkCells that are
  // visible in the render window.
  vtkSmartPointer<vtkExtractSelectedFrustum> extractor =
    vtkSmartPointer<vtkExtractSelectedFrustum>::New();
  extractor->SetFrustum(picker->GetFrustum());
  extractor->PreserveTopologyOff();
  vtkSmartPointer<vtkDataSet> dataset = layer->get_pickable_dataset();
  extractor->SetInputConnection(0, dataset->GetProducerPort());
  extractor->Update();
  subgrid = vtkUnstructuredGrid::SafeDownCast(extractor->GetOutput());
  return subgrid;
} // GhostOOFCanvas::getFrustumSubgrid

// findClickedPoint finds the clicked-upon point from a data set of
// points, and returns its position.  The set of points is the
// vtkPoints belonging to the layer being displayed. Compare to
// findClickedPosition, which returns the coordinates of a click on
// any kind of vtkCell.
//
// It's tempting to create a version of findClickedPoint that returns
// the point's id, so that it can be translated into a Node without
// any searching.  That doesn't work because findClickedPoint finds
// the point in a subgrid, and it doesn't know the point's index in
// the full grid's points array.

Coord *GhostOOFCanvas::findClickedPoint(const Coord *click, const View *view,
					OOFCanvasLayer *layer)
{
  assert(mainthread_query());
  viewLock.acquire();
  const View *oldView = set_view_nolock(view, true);
  try {
    double x, y;		// display coordinates
    physical2Display(*click, x, y);
    vtkSmartPointer<vtkUnstructuredGrid> subgrid = 
      getFrustumSubgrid(x, y, view, layer);

    // Add the points for the subgrid to the render window.  Because
    // only visible cells were included in the subgrid, we won't
    // accidentally pick invisible nodes when selecting from the subgrid
    // (which is a problem when using vtkPointPicker on the original
    // vtkPoints from the full grid).
    vtkSmartPointer<vtkPoints> points = subgrid->GetPoints();
    vtkSmartPointer<vtkDataSetMapper> mapper = 
      vtkSmartPointer<vtkDataSetMapper>::New();

#ifdef DEBUGSELECTIONS
    if(tempActor.GetPointer() != 0)
      renderer->RemoveActor(tempActor);
    // If DEBUGSELECTIONS is defined, tempActor is a GhostOOFCanvas
    // data member.
    tempActor = vtkSmartPointer<vtkActor>::New();
#else
    vtkSmartPointer<vtkActor> tempActor = vtkSmartPointer<vtkActor>::New();
#endif // DEBUGSELECTIONS
    tempActor->SetMapper(mapper);
    tempActor->PickableOn();
    mapper->SetInput(subgrid);
    tempActor->GetProperty()->SetRepresentationToPoints();
#ifdef DEBUGSELECTIONS
    tempActor->GetProperty()->SetRepresentationToWireframe();
    // tempActor->GetProperty()->SetPointSize(8.);
    tempActor->GetProperty()->SetLineWidth(4);
    tempActor->GetProperty()->SetColor(0.9, 0.1, 0.1);
#endif // DEBUGSELECTIONS
    renderer->AddActor(tempActor);
    subgrid->Update();

    // Use a vtkPointPicker to select the appropriate point.
    vtkSmartPointer<vtkPointPicker> pointpicker =
      vtkSmartPointer<vtkPointPicker>::New();
    pointpicker->SetTolerance(0.005); // tol is fraction of window diagonal size
    if(pointpicker->Pick(x, y, 0.0, renderer)) {
      vtkIdType ptId = pointpicker->GetPointId();
      if(ptId >= 0) {
	Coord *coord = new Coord();
	points->GetPoint(ptId, *coord);
#ifndef DEBUGSELECTIONS
	renderer->RemoveActor(tempActor);
	mapper->RemoveAllInputs();
#endif // DEBUGSELECTIONS
	restore_view(oldView, true);
	delete oldView;
	viewLock.release();
	return coord;
      }
    } // pointpicker didn't find anything
#ifndef DEBUGSELECTIONS
    renderer->RemoveActor(tempActor);
    mapper->RemoveAllInputs();
#endif // DEBUGSELECTIONS
  }
  catch(...) {
    restore_view(oldView, true);
    delete oldView;
    viewLock.release();
    throw;
  }
  restore_view(oldView, true);
  delete oldView;
  viewLock.release();
  // There is no point.  (The heat death of the universe is unavoidable.)
  throw ErrClickError();
} // GhostOOFCanvas::findClickedPoint


// findClickedSegment doesn't really find a segment.  It converts a
// click in 2D screen coordinates to a 3D Coord that's on or near a
// segment in the given layer's vtkCells.  

Coord *GhostOOFCanvas::findClickedSegment(const Coord *click, const View *view,
					  OOFCanvasLayer *layer)
{
  assert(mainthread_query());
  vtkSmartPointer<vtkDataSet> edges;
  Coord clickPosition;
  Coord ray;

  viewLock.acquire();
  View *oldView = set_view_nolock(view, true);
  try  {
    double x, y;		// display coordinates
    physical2Display(*click, x, y);
    
    vtkSmartPointer<vtkUnstructuredGrid> subgrid = 
      getFrustumSubgrid(x, y, view, layer);
    vtkSmartPointer<vtkExtractEdges> exEdges = 
      vtkSmartPointer<vtkExtractEdges>::New();
    exEdges->SetInput(subgrid);
    edges = exEdges->GetOutput();
    exEdges->Update();
  
    // Compute the ray that goes through the clicked point on the
    // focal plane.  Start by getting the camera focal point, which
    // determines the z coordinate of the click.
    double cameraFP[4];
    renderer->GetActiveCamera()->GetFocalPoint(cameraFP);
    cameraFP[3] = 1.0;
    renderer->SetWorldPoint(cameraFP);
    renderer->WorldToDisplay();
    double *displayCoords = renderer->GetDisplayPoint();
    double z = displayCoords[2];
    // x, y, z are now the coords of the clicked point on the focal
    // plane in display coordinates.  Convert them to world coordinates.
    renderer->SetDisplayPoint(x, y, z);
    renderer->DisplayToWorld();
    double *worldCoords = renderer->GetWorldPoint(); // homogeneous coords
    Coord clickPos;
    // convert homogeneous to actual coords.
    for(int i=0; i<3; i++)
      clickPos[i] = worldCoords[i]/worldCoords[3];
    clickPosition = clickPos; // convert to Coord for convenience
    ray = findRayThroughPoint(clickPosition);
  }
  catch(...) {
    restore_view(oldView, true);
    delete oldView;
    viewLock.release();
    throw;
  }
  restore_view(oldView, true);
  delete oldView;
  viewLock.release();

#ifdef DEBUGSELECTIONS
  if(tempActor.GetPointer() != 0)
    renderer->RemoveActor(tempActor);
  tempActor = vtkSmartPointer<vtkActor>::New();
  vtkSmartPointer<vtkDataSetMapper> mapper =
    vtkSmartPointer<vtkDataSetMapper>::New();
  tempActor->SetMapper(mapper);
  mapper->SetInput(edges);
  tempActor->GetProperty()->SetRepresentationToWireframe();
  tempActor->GetProperty()->SetColor(0.9, 0.9, 0.1);
  tempActor->GetProperty()->SetLineWidth(3);
  renderer->AddActor(tempActor);
#endif // DEBUGSELECTIONS

  // Loop over all segments of the subgrid, looking for the one that's
  // closest to the ray.  If there are ties, use the one that's closer
  // to the camera (dot product of nearest point with ray is smallest).
  double smallestDistance2 = std::numeric_limits<double>::max();
  Coord closestPoint;
  bool found = false;
  vtkIdType nCells = edges->GetNumberOfCells();
  // oofcerr << "GhostOOFCanvas::findClickedSegment: nCells=" << nCells
  // 	  << std::endl;
  for(vtkIdType i=0; i<nCells; i++) {
    vtkSmartPointer<vtkCell> cell = edges->GetCell(i);
    vtkSmartPointer<vtkPoints> points = cell->GetPoints();
    assert(points->GetNumberOfPoints() == 2);
    Coord ptA;
    points->GetPoint(0, ptA);
    Coord ptB;
    points->GetPoint(1, ptB);
    // Find the squared distance d2 between the segment defined by ptA
    // and ptB and the line defined by clickPosition and ray.  alpha
    // is the fractional distance along (ptA, ptB) where the closest
    // point lies.
    double d2, alpha;
    if(findSegLineDistance(ptA, ptB, clickPosition, ray, d2, alpha)) {
      if(d2 < smallestDistance2) {
	// oofcerr << "GhostOOFCanvas::findClickedSegment: ptA=" << ptA
	// 	<< " ptB=" << ptB << " d2=" << d2 << std::endl;
	smallestDistance2 = d2;
	closestPoint = (1-alpha)*ptA + alpha*ptB;
	found = true;
      }
      else if(found && d2 == smallestDistance2) {
	// New intersection is as close as the previous best intersection.
	Coord candidate = (1-alpha)*ptA + alpha*ptB;
	if(dot(candidate, ray) < dot(closestPoint, ray)) {
	  smallestDistance2 = d2;
	  closestPoint = candidate;
	}
      }
    } // end if findSegLineDistance(...)
  }
  if(found)
    return new Coord(closestPoint);
  throw ErrClickError();
} // GhostOOFCanvas::findClickedSegment

void GhostOOFCanvas::makeAllUnpickable() const {
  // Make all Actors and Volumes unpickable.
  assert(mainthread_query());
  vtkSmartPointer<vtkActorCollection> actors = renderer->GetActors();
  actors->InitTraversal();
  vtkActor *actor;
  while((actor=actors->GetNextActor()) != 0)
    actor->PickableOff();
  vtkSmartPointer<vtkVolumeCollection> volumes = renderer->GetVolumes();
  volumes->InitTraversal();
  vtkVolume *volume;
  while((volume=volumes->GetNextVolume()) != 0)
    volume->PickableOff();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Conversion from 2D screen coords to 3D world coords.

// display2Physical() can't be const because it has to temporarily
// change the View.

Coord GhostOOFCanvas::display2Physical(const View *view, double x, double y) {
  assert(mainthread_query());
  double winHeight = render_window->GetSize()[1];
  y = winHeight - y - 1;

  // display2Physical is called by mouse handlers (eg,
  // GenericSelectToolboxGUI.up) so it can't assume that the gfxlock
  // has been acquired.  That's why there's a separate viewLock.
  viewLock.acquire();
  View *oldView = set_view_nolock(view, true);
  try {
    renderer->SetDisplayPoint(x, y, 0);
    renderer->DisplayToWorld();
    double worldpoint[4];
    renderer->GetWorldPoint(worldpoint);

    for(int i=0; i<3; i++)	// convert from homogeneous coords
      worldpoint[i] /= worldpoint[3];
    restore_view(oldView, true);
    delete oldView;
    viewLock.release();
    return Coord(worldpoint);
  }
  catch(...) {
    restore_view(oldView, true);
    delete oldView;
    viewLock.release();
    throw;
  }
}

void GhostOOFCanvas::physical2Display(const Coord &pt, double &x, double &y)
  const
{
  // This should only be called when the View has been set
  // appropriately and viewLock has been acquired.  The results of
  // this computation depend on the current camera parameters.
  renderer->SetWorldPoint(pt.x[0], pt.x[1], pt.x[2], 1.0);
  renderer->WorldToDisplay();
  double *dpt = renderer->GetDisplayPoint();
  x = dpt[0];
  y = dpt[1];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Views

View *GhostOOFCanvas::get_view() const {
  Coord pos;
  Coord focal;
  Coord up;
  assert(mainthread_query());
  vtkSmartPointer<vtkCamera> camera = renderer->GetActiveCamera();
  camera->GetPosition(pos);
  camera->GetFocalPoint(focal);
  camera->GetViewUp(up);
  double angle = camera->GetViewAngle();
  int *size = render_window->GetSize();
  View *vue = new View(pos, focal, up, angle,
		       size[0], size[1]);
  for(ClippingPlaneList::const_iterator i=clipPlanes.begin();
      i<clipPlanes.end(); ++i)
    {
       vue->addClipPlaneWithoutRebuilding(*i);
    }
  vue->rebuildVtkPlanes();
  if(clipInverted)
    vue->invertClipOn();
  if(clipSuppressed)
    vue->suppressClipOn();
  return vue;
}

typedef std::set<ClippingPlane> ClippingPlaneSet;

View *GhostOOFCanvas::set_view(const View *view, bool clip) {
  View *oldView = 0;
  assert(mainthread_query());
  viewLock.acquire();
  try {
    oldView = set_view_nolock(view, clip);
  }
  catch(...) {
    viewLock.release();
    throw;
  }
  viewLock.release();
  return oldView;
}

View *GhostOOFCanvas::set_view_nolock(const View *view, bool clip) {
  assert(mainthread_query());
  assert(view != 0); // maybe running an old script with no view parameter?
  View *oldView = get_view();
  if(*view == *oldView) {
    delete oldView;
    return 0;
  }
  restore_view(view, clip);
  return oldView;
}

void GhostOOFCanvas::restore_view(const View *view, bool clip) {
  // restore_view is called either by set_view_nolock, or in a
  // set_view/restore_view pair (as in findClickedCell_, et. al.)  In
  // the first case, we know that view!=0.  In the second case, if
  // view==0 it means that set_view didn't have to do anything, so
  // there's nothing to do here either.
  if(!view) {
    return;
  }
  // size_x and size_y can be zero if the View is being loaded from a
  // script written before the sizes were provided as part of the View
  // data.  In that case we just assume that the window size hasn't
  // changed, which seems to work for the relevant test scripts.
  if(view->size_x > 0 && view->size_y > 0) {
    render_window->SetSize(view->size_x, view->size_y);
  }
  view->setCamera(renderer->GetActiveCamera()); // change active camera settings
  if(clip) {
    clipInverted = view->invertedClip();
    clipSuppressed = view->suppressedClip();

    clipPlanes = view->clipPlanes; // vector copy
    // Set the canvas's vtkPlanes object by copying the contents of
    // the View's vtkPlanes object.  Don't simply change the canvas's
    // pointer, since the layers are pointing to the canvas's
    // vClipPlanes object.  They get the pointer to it by calling
    // GhostOOFCanvas::getVTKClipPlanes().
    vClipPlanes->SetNormals(view->vtkplanes->GetNormals());
    vClipPlanes->SetPoints(view->vtkplanes->GetPoints());

    // Update the clipping status for all base layers in the
    // layerlist. 
    bool cl = clipping();
    for(CanvasLayerList::iterator i=layers.begin(); i<layers.end(); ++i) {
      (*i)->set_clipping(cl, clipInverted);
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void GhostOOFCanvas::save_canvas(const std::string &filename,
				 const ImageFormat *format) const
{
  format->saveCanvas(render_window, filename);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the minimum distance squared ('distance2') between the segment
// AB and the line defined by the position C and the unit vector
// 'ray'.  'alpha' is the fractional position along AB of the closest
// point.  The return value indicates whether or not the closest point
// lies within the line segment.
  
bool findSegLineDistance(const Coord &A, const Coord &B,
			 const Coord &C, const Coord &ray,
			 double &distance2, double &alpha)
{
  // The segment AB is given by x = (1-alpha)*A + alpha*B where 0 < alpha < 1.
  //
  // The line is given by X = C + beta*ray for any beta.
  //
  // If alpha and beta are chosen to give the points of closest
  // approach, then the segment joining the points is perpendicular to
  // both AB and ray:
  //    (x(alpha) - X(beta)) dot (A-B) = 0
  //    (x(alpha) - X(beta)) dot ray = 0
  // This gives two linear equations in alpha and beta. 
  double a00 = -norm2(B-A);
  double a01 = dot(B-A, ray);
  double a10 = -a01;
  double a11 = 1.0; // norm2(ray);
  double det = a00*a11 - a01*a10;
  if(det == 0) {		// line and ray are parallel
    alpha = 0.0;		// arbitrary
    distance2 = norm2(cross(B-C, ray)); // assumes ray is a unit vector
    return true;
  }
  // Line and ray aren't parallel.
  double b0 = dot(A-C, B-A);
  double b1 = dot(A-C, ray);
  alpha = (a11*b0 - a01*b1)/det;
  double beta = (a00*b1 - a10*b0)/det;
  Coord link = (1-alpha)*A + alpha*B - C - beta*ray;
  distance2 = norm2(link);
  return alpha >= 0.0 && alpha <= 1.0;
}
