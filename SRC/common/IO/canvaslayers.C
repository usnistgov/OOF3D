// -*- C++ -*-

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
#include <vtkCellType.h>
#include <vtkPointData.h>	// required implicitly by GetPointData
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkType.h>
#include <vtkVoxel.h>

#include <math.h>

// TODO 3.1: Give each layer a flag indicating whether or not it should be
// clipped, and make the flag settable in the gfx window's layer list.

// TODO 3.1: When multiple intersecting clipping planes are used, the
// Skeleton isn't clipped correctly.  See clipbug2.log in TEST3D.

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Compute the bounding box of the part of the data that's within the
// frustum.  The frustum is the volume that's visible to the camera.
// This is used to find the center of the visible objects on the
// canvas, which is used by OOFCanvas3D::mouse_tumble.  mouse_tumble
// would use vtkRenderer::ComputeVisiblePropBounds instead, except
// that ComputeVisiblePropBounds includes all the points in a grid,
// not just the ones that are in the drawn cells.  As a result, all
// tumbles are centered on the center of the Microstructure, making it
// impossible to rotate a small cluster of elements.

bool getVisibleBoundingBox(vtkDataSet *data,
			   vtkSmartPointer<vtkRenderer> renderer,
			   CRectangularPrism *bbox)
{
  vtkIdType ncells = data->GetNumberOfCells();
  if(ncells == 0)
    return false;
  CRectangularPrism layerbbox;	// "uninitialized", with max < min
  int foundSomething = false;
  for(vtkIdType c=0; c<ncells; c++) {
    vtkCell *cell = data->GetCell(c); // not thread safe! Should be ok if locked
    vtkIdType npts = cell->GetNumberOfPoints();
    for(vtkIdType i=0; i<npts; i++) {
      // Is this point visible?  Rather than compute the frustum
      // planes and check that the point is on the correct side of all
      // of them, it's easier to covert the point to ViewPort
      // coordinates.  The visible part of the ViewPort is defined by
      // -1<x<1, -1<y<1, and z between the clipping planes. But I
      // can't seem to get sensible values for the clipping planes
      // from vtkCamera::GetClippingRange, so we're ignoring z values
      // here.
      Coord3D pt(data->GetPoint(cell->GetPointId(i)));
      double x = pt[0];
      double y = pt[1];
      double z = pt[2];
      renderer->WorldToView(x, y, z); // converts values in place
      // I don't understand the values returned by GetClippingRange,
      // so we're just ignoring them.
      if(x >= -1 && x <= 1 && y >= -1 && y <= 1
	 //	 && z >= zmin && z <= zmax
	 )
	{
	  layerbbox.swallow(pt);
	  foundSomething = true;
	}
    } // end loop over points i in cell
  } // end loop over cells c
  if(foundSomething) {
    *bbox = layerbbox;
  }
  return foundSomething;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &OOFCanvasLayerBase::modulename() const {
  static const std::string modname("ooflib.SWIG.common.IO.canvaslayer");
  return modname;
}

OOFCanvasLayerBase::OOFCanvasLayerBase(GhostOOFCanvas *c, const std::string &nm)
  : canvas(c),
    name_(nm),
    clipState(CLIP_UNKNOWN)
{
  // oofcerr << "OOFCanvasLayerBase::ctor: " << this << " " << name() 
  // 	  << std::endl;
}

OOFCanvasLayerBase::~OOFCanvasLayerBase() {
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

bool OOFCanvasLayerBase::visibleBoundingBox(vtkSmartPointer<vtkRenderer>,
					    CRectangularPrism*)
  const
{
  return false;
}

std::ostream &operator<<(std::ostream &os, const OOFCanvasLayerBase &layer) {
  return os << layer.name();
}

OOFCanvasLayer::OOFCanvasLayer(GhostOOFCanvas *c, const std::string &nm)
  : OOFCanvasLayerBase(c, nm),
    showing_(false),
    empty_(true)
{
  c->newLayer(this);
}

OOFCanvasLayer::~OOFCanvasLayer() {
  canvas->removeLayer(this);
}

void OOFCanvasLayer::addProp(vtkSmartPointer<vtkProp> prop) {
  props.push_back(prop);
  canvas->renderer->AddViewProp(prop);
}

void OOFCanvasLayer::setEmpty(bool empty) {
  // This is a hack to avoid a peculiarity in vtk (in versions 7.1.1
  // and 8.0.1, at least).  vtkDataSetMapper::Render creates a
  // vtkDataSetSurfaceFilter when the mapper's input type isn't
  // VTK_POLY_DATA, and this filter raises a warning when its input
  // contains no cells, although the empty input actually causes no
  // errors.  We often have input data with no cells, such as the
  // selection layers when nothing is selected.  To avoid filling the
  // screen with ignorable warnings, those layers should call
  // setEmpty(true) when they become empty.

  // setEmpty(true) does *not* mean that there are no vtkProps.  It
  // means that the props won't result in anything being drawn.

  // Layers that don't use a vtkDataSetMapper or always pass
  // VTK_POLY_DATA to it can probably get away with just calling
  // setEmpty(false) in newLayer() and ignoring it thereafter.

  if(empty != empty_) {
    empty_ = empty;
    if(empty_)
      setPropVisibility(false);
    else
      setPropVisibility(showing_);
  }
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
  empty_ = true;
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
//   //   remove_from_renderer();
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

// setPropVisibility toggles the vtkProp's visibilities, without
// touching the OOFCanvasLayer flags that say whether or not the layer
// *should* be visible.

void OOFCanvasLayer::setPropVisibility(bool visible) {
  if(empty_)
    visible = false;
  for(unsigned int i=0; i<props.size(); i++) {
    // If the new value is the same as the old one, don't call
    // SetVisibility because it'll update the vtk modification time
    // unnecessarily.
    if((bool) props[i]->GetVisibility() != visible)
      props[i]->SetVisibility(visible);
  }
}

// TODO: Do we need the 'forced' arg for show and hide?  It seems to
// always be false.

void OOFCanvasLayer::show(bool forced) {
  if(!showing_ || forced) {
    setPropVisibility(true);
    showing_ = true;
    // setModified();
  }
}

void OOFCanvasLayer::hide(bool forced) {
  if(showing_ || forced) {
    setPropVisibility(false);
    showing_ = false;
    // setModified();
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

vtkSmartPointer<vtkActorCollection> OOFCanvasLayer::get_pickable_actors() {
  return vtkSmartPointer<vtkActorCollection>();
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

  // From the man page for vtkTableBasedClipDataSet:::SetInsideOut():

  // Set/Get the InsideOut flag. With this flag off, a vertex is
  // considered inside (the implicit function or the isosurface) if
  // the (function or scalar) value is greater than IVAR Value. With
  // this flag on, a vertex is considered inside (the implicit
  // function or the isosurface) if the (function or scalar) value is
  // less than or equal to IVAR Value. This flag is off by default.

  // From the man page for vtkPlanes:

  // The function value is the closest first order distance of a point
  // to the convex region defined by the planes. ... Note that the
  // normals must point outside of the convex region. Thus, a negative
  // function value means that a point is inside the convex region.

  // The natural definition for OOF is that the *inside* of the convex
  // region should be displayed, and not clipped away.  Therefore all
  // calls to SetInsideOut need to have an extra "!".

  clipper->SetInsideOut(!(canvas->invertedClipping() ||
			  (vplanes->GetNumberOfPlanes() == 0)));
  return clipper;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The PlaneAndArrowLayer is used when interactively editing clipping
// planes, and possibly other sorts of planes too.  It's probably
// redundant with the vtkImplicitPlaneWidget, but in order to use VTK
// widgets we probably would have to use VTK's interactor event loop
// instead of the gtk2 event loop.  That would be possible, and maybe
// should be considered.

PlaneAndArrowLayer::PlaneAndArrowLayer(GhostOOFCanvas *canvas,
				       const std::string &nm,
				       bool inverted)
  : OOFCanvasLayer(canvas, nm),
    planeSource(vtkSmartPointer<vtkCubeSource>::New()),
    arrowSource(vtkSmartPointer<vtkArrowSource>::New()),
    scaling(vtkSmartPointer<vtkTransform>::New()),
    arrowScaling(vtkSmartPointer<vtkTransform>::New()),
    rotation(vtkSmartPointer<vtkTransform>::New()),
    translation(vtkSmartPointer<vtkTransform>::New()),
    planeTransform(vtkSmartPointer<vtkTransform>::New()),
    arrowTransform(vtkSmartPointer<vtkTransform>::New()),
    planeFilter(vtkSmartPointer<vtkTransformPolyDataFilter>::New()),
    arrowFilter(vtkSmartPointer<vtkTransformPolyDataFilter>::New()),
    planeMapper(vtkSmartPointer<vtkPolyDataMapper>::New()),
    arrowMapper(vtkSmartPointer<vtkPolyDataMapper>::New()),
    planeActor(vtkSmartPointer<vtkActor>::New()),
    arrowActor(vtkSmartPointer<vtkActor>::New()),
    arrowParity(inverted? -1 : 1)
{
  // Constructor for the PlaneAndArrowLayer class.  Creates
  // and joins together the pre-render portions of the vtk pipeline
  // that are need in order to display a plane, along with an arrow
  // that represents the normal vector of that plane.

  // TODO: The plane isn't drawn in the correct color when inverted is
  // false.  

  // If planeSource were a vtkPlaneSource and not a vtkCubeSource:
  // planeSource->SetNormal(1, 0, 0);
  // planeSource->Push(-0.001);

  planeSource->SetCenter(arrowParity*0.001, 0, 0);
  //planeSource->SetCenter(0, 0, 0);  
  planeSource->SetXLength(0.001);
  planeSource->SetYLength(1.0);
  planeSource->SetZLength(1.0);
  planeSource->Update();

  // The arrow tip is a cone, and its shaft is a cylinder.  The
  // following lines of code set the cone and cylinder to be
  // approximated by a dodecagonal pyramid and a dodecagonal prism,
  // respectively.
  arrowSource->SetTipResolution(12);
  arrowSource->SetShaftResolution(12);
  arrowSource->Update();

  scaling->Identity();
  rotation->Identity();
  translation->Identity();
  planeTransform->Identity();
  planeTransform->Concatenate(translation);
  planeTransform->Concatenate(rotation);
  planeTransform->Concatenate(scaling);

  // Scales the arrow by one half the sidelength of the plane.
  // arrowParity is set by the "inverted" constructor arg, which
  // should be chosen so that the arrow is visible.  When using this
  // widget to define a clipping plane, for example, the arrow should
  // be on the clipped (hidden) side of the plane.
  arrowScaling->Identity();
  double s = arrowParity*0.5;
  arrowScaling->Scale(s, s, s);

  arrowTransform->Identity();
  arrowTransform->Concatenate(planeTransform);
  arrowTransform->Concatenate(arrowScaling);

  planeFilter->SetInputConnection(planeSource->GetOutputPort());
  planeFilter->SetTransform(planeTransform);

  arrowFilter->SetInputConnection(arrowSource->GetOutputPort());
  arrowFilter->SetTransform(arrowTransform);

  planeMapper->SetInputConnection(planeFilter->GetOutputPort());
  arrowMapper->SetInputConnection(arrowFilter->GetOutputPort());

  planeActor->SetMapper(planeMapper);
  planeActor->GetProperty()->BackfaceCullingOn();
  arrowActor->SetMapper(arrowMapper);

  addProp(planeActor);
  addProp(arrowActor);
}

PlaneAndArrowLayer::~PlaneAndArrowLayer() {}

const std::string &PlaneAndArrowLayer::classname() const {
  static const std::string nm("PlaneAndArrowLayer");
  return nm;
}

// The following four functions are inherited from OOFCanvasLayer and
// need to be defined, but aren't used by this particular subclass.
void PlaneAndArrowLayer::start_clipping() { }

void PlaneAndArrowLayer::stop_clipping() { }

void PlaneAndArrowLayer::set_clip_parity(bool b) { }

void PlaneAndArrowLayer::setModified() {
  planeSource->Modified();
  arrowSource->Modified();
}

vtkSmartPointer<vtkActor> PlaneAndArrowLayer::get_planeActor() {
  return planeActor;
}

vtkSmartPointer<vtkActor> PlaneAndArrowLayer::get_arrowActor() {
  return arrowActor;
}

vtkSmartPointer<vtkActorCollection> PlaneAndArrowLayer::get_pickable_actors() {
  vtkSmartPointer<vtkActorCollection> actors = 
    vtkSmartPointer<vtkActorCollection>::New();
  
  actors->AddItem(planeActor);   
  actors->AddItem(arrowActor);
 
  return actors;
}

// void PlaneAndArrowLayer::set_visibility(bool visible) {
//   // Sets whether or not the vtk plane and arrow are to be visible
//   // once the renderer is called.
//   planeActor->SetVisibility(int(visible));
//   arrowActor->SetVisibility(int(visible));
//   setModified();
// }

void PlaneAndArrowLayer::set_arrowShaftRadius(double radius) {
  arrowSource->SetShaftRadius(radius);
}

void PlaneAndArrowLayer::set_arrowTipRadius(double radius) {
  arrowSource->SetTipRadius(radius);
}

void PlaneAndArrowLayer::set_arrowLength(double length) {
  // Sets the arrow's length to (length * (the sidelength of the
  // plane)), with the (+) sign causing the arrow to point in the
  // direction we want it to--that is, into to the otherwise empty
  // region of the OOF3D canvas which has been clipped away by the
  // clipping plane being edited. Otherwise the arrow could become
  // hidden in the unclipped parts of 3D objects which are still
  // visible in the unclipped region of the OOF3D canvas.
  arrowScaling->Identity();
  double s = arrowParity*length;
  arrowScaling->Scale(s, s, s);
}

void PlaneAndArrowLayer::set_arrowColor(const CColor& color) {
  arrowActor->GetProperty()->SetColor(color.getRed(), color.getGreen(), 
				      color.getBlue());
}

void PlaneAndArrowLayer::set_planeColor(const CColor& color) {
  planeActor->GetProperty()->SetColor(color.getRed(), color.getGreen(), 
				      color.getBlue());
}

// TODO: Change set_planeOpacity to set_opacity.
void PlaneAndArrowLayer::set_planeOpacity(double opacity) {
  planeActor->GetProperty()->SetOpacity(opacity);
  arrowActor->GetProperty()->SetOpacity(opacity/2.); // it has two sides
 }

void PlaneAndArrowLayer::rotate(const Coord3D *axisOfRotation,
				double angleOfRotation)
{
  vtkSmartPointer<vtkTransform> new_rotation =
    vtkSmartPointer<vtkTransform>::New();
  new_rotation->RotateWXYZ(-angleOfRotation, (*axisOfRotation)[0],
			   (*axisOfRotation)[1], (*axisOfRotation)[2]);

  // Concatenate the new rotation after the current rotation. 
  rotation->PostMultiply();
  rotation->Concatenate(new_rotation);
  rotation->PreMultiply();
} 

void PlaneAndArrowLayer::translate(const Coord3D *translationVector) {
  // Shifts the plane and arrow by the specified displacement vector.

  double translationX = (*translationVector)[0];
  double translationY = (*translationVector)[1];
  double translationZ = (*translationVector)[2];

  // Concatenate the new translation onto the current
  // translation.
  translation->Translate(translationX, translationY, translationZ);
  setModified();
}

void PlaneAndArrowLayer::offset(double offset) {
  // Offsets the plane and arrow by the specified amount along the
  // plane's normal.

  double unitX[3] = {1, 0, 0};
  double normal_double[3];

  rotation->TransformPoint(unitX, normal_double);

  Coord3D normal(normal_double);
  
  // We multiply the normal vector by the offset in order to get the
  // vector representing the plane's displacement from the
  // origin. This will be the coordinates of our translation.
  normal *= offset;

  // Concatenate the new offsetting translation onto the current
  // translation.
  translation->Translate(normal[0], normal[1], normal[2]);
  setModified();
}

void PlaneAndArrowLayer::scale(double scale) {
  // Scales the plane and arrow by the specified amount.

  vtkSmartPointer<vtkTransform> new_scaling =
    vtkSmartPointer<vtkTransform>::New();
  new_scaling->Scale(scale, scale, scale);

  // Concatenate the new scaling onto the current scaling.
  scaling->Concatenate(new_scaling);
  setModified();
}

Coord3D *PlaneAndArrowLayer::get_center() {
  // Returns the world coordinates of the arrow base, which are the
  // same coordinates as the center of the plane.
  double center_double[3];
  translation->GetPosition(center_double);
  Coord3D *center =
    new Coord3D(center_double[0], center_double[1], center_double[2]);
  return center;
}

Coord3D *PlaneAndArrowLayer::get_normal_Coord3D() {
  // Returns the normal vector as a Coord3D*.
  double unitX[3] = {1, 0, 0};
  double normal_double[3];

  rotation->TransformPoint(unitX, normal_double);

  Coord3D *normal = new Coord3D(normal_double);
  return normal;
}

CUnitVectorDirection *PlaneAndArrowLayer::get_normal() {
  // Returns the normal vector as a CUnitVectorDirection*.
  double unitX[3] = {1, 0, 0};
  double normal_double[3];

  rotation->TransformPoint(unitX, normal_double);

  CUnitVectorDirection *normal = 
    new CUnitVectorDirection(normal_double[0], normal_double[1],
			     normal_double[2]);

  return normal;
}

double PlaneAndArrowLayer::get_offset() {
  Coord3D center;
  translation->GetPosition(center.xpointer());

  double unitX[3] = {1, 0, 0};
  double normal_double[3];

  rotation->TransformPoint(unitX, normal_double);

  Coord3D normal(normal_double);

  return dot(center, normal);
}

void PlaneAndArrowLayer::set_scale(double scale) {
  // Sets the length of the plane's edges to the specified scale,
  // while keeping the plane and arrow centered at their current
  // position and facing in their current direction.  The arrow is
  // scaled relative to the specified scale by means of the
  // arrowScaling transform, which is changed by the function
  // set_arrowScale(double).
  scaling->Identity();
  double s = arrowParity*scale;
  scaling->Scale(s, s, s);
  setModified();
}

void PlaneAndArrowLayer::set_normal(const CDirection *direction) {
  // Sets the direction of the plane's normal vector (which is
  // opposite the direction which should be pointed to by the arrow)
  // to the specified direction, while keeping the plane and arrow
  // centered at their current position and sized at their current
  // scale.
  Coord3D *normalVector = direction->coord();
  Coord3D xVector = Coord3D(1, 0, 0);

  // We calculate the angle to rotate the plane's normal vector away
  // from the x-axis as the angle between the unit vector in the
  // x-direction (xVector) and the desired normal vector
  // (normalVector).  We further find the axis to perform this
  // rotation about by taking the cross product of the the two
  // vectors.
  double angleOfRotation = (180 / M_PI) * acos(dot(*normalVector, xVector));
  Coord3D axisOfRotation = cross(xVector, *normalVector); 

  // Reset the transform controling the rotation of the plane and the
  // direction of the arrow.
  rotation->Identity();
  rotation->RotateWXYZ(angleOfRotation,
		       axisOfRotation[0], axisOfRotation[1], axisOfRotation[2]);

  setModified();

  // Free allocated memory.
  delete(normalVector);
}

void PlaneAndArrowLayer::set_center(const Coord3D *position) {
  // Sets the center of the plane and the base of the arrow to the
  // specified position, while while keeping the plane and arrow
  // facing in their current direction and sized at their current
  // scale.
  double position0 = (*position)[0];
  double position1 = (*position)[1];
  double position2 = (*position)[2];

  translation->Identity();
  translation->Translate(position0, position1, position2);
  setModified();
}

void PlaneAndArrowLayer::setCoincidentTopologyParams(double factor,
						     double units)
{
  planeMapper->SetRelativeCoincidentTopologyPolygonOffsetParameters(factor,
								    units);
  arrowMapper->SetRelativeCoincidentTopologyPolygonOffsetParameters(factor,
								    units);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// BoxWidgetLayer could be replaced by vtkBoxWidget if we were using
// the VTK event loop.

BoxWidgetLayer::BoxWidgetLayer(GhostOOFCanvas *canvas, const std::string &nm)
  : OOFCanvasLayer(canvas, nm),
    grid(vtkSmartPointer<vtkUnstructuredGrid>::New()),
    points(vtkSmartPointer<vtkPoints>::New()),
    boxMapper(vtkSmartPointer<vtkDataSetMapper>::New()),
    boxActor(vtkSmartPointer<vtkActor>::New()),
    locator(vtkSmartPointer<oofCellLocator>::New())
{
  points->Initialize();
  points->SetNumberOfPoints(8);

  for (int i = 0; i < 8; i++) {
    points->SetPoint(i, double(i % 2),
		     double((i / 2) % 2),
		     double((i / 4) % 2));
  }

  grid->Initialize();
  grid->Allocate(26, 26);
  grid->SetPoints(points);

  for (int i = 0; i < 8; i++) {
    // Store the 8 vertices of the box.
    vtkIdType ptID;
    ptID = i;
    grid->InsertNextCell(VTK_VERTEX, 1, &ptID);
  }

  // Store the 12 edges of the box.
  vtkIdType edge_ptIDs[12][2];
  edge_ptIDs[0][0] = 0;
  edge_ptIDs[0][1] = 1;
  edge_ptIDs[1][0] = 0;
  edge_ptIDs[1][1] = 2;
  edge_ptIDs[2][0] = 0;
  edge_ptIDs[2][1] = 4;
  edge_ptIDs[3][0] = 1;
  edge_ptIDs[3][1] = 3;
  edge_ptIDs[4][0] = 1;
  edge_ptIDs[4][1] = 5;
  edge_ptIDs[5][0] = 2;
  edge_ptIDs[5][1] = 3;
  edge_ptIDs[6][0] = 2;
  edge_ptIDs[6][1] = 6;
  edge_ptIDs[7][0] = 3;
  edge_ptIDs[7][1] = 7;
  edge_ptIDs[8][0] = 4;
  edge_ptIDs[8][1] = 5;
  edge_ptIDs[9][0] = 4;
  edge_ptIDs[9][1] = 6;
  edge_ptIDs[10][0] = 5;
  edge_ptIDs[10][1] = 7;
  edge_ptIDs[11][0] = 6;
  edge_ptIDs[11][1] = 7;
  for (int i = 0; i < 12; i++) {
    grid->InsertNextCell(VTK_LINE, 2, edge_ptIDs[i]);
  }

  // Store the 6 faces of the box.
  vtkIdType face_ptIDs[6][4];
  face_ptIDs[0][0] = 0;
  face_ptIDs[0][1] = 1;
  face_ptIDs[0][2] = 5;
  face_ptIDs[0][3] = 4;
  //
  face_ptIDs[1][0] = 0;
  face_ptIDs[1][1] = 4;
  face_ptIDs[1][2] = 6;
  face_ptIDs[1][3] = 2;
  //
  face_ptIDs[2][0] = 0;
  face_ptIDs[2][1] = 2;
  face_ptIDs[2][2] = 3;
  face_ptIDs[2][3] = 1;
  //
  face_ptIDs[3][0] = 1;
  face_ptIDs[3][1] = 3;
  face_ptIDs[3][2] = 7;
  face_ptIDs[3][3] = 5;
  //
  face_ptIDs[4][0] = 2;
  face_ptIDs[4][1] = 6;
  face_ptIDs[4][2] = 7;
  face_ptIDs[4][3] = 3;
  //
  face_ptIDs[5][0] = 4;
  face_ptIDs[5][1] = 5;
  face_ptIDs[5][2] = 7;
  face_ptIDs[5][3] = 6;
  for (int i = 0; i < 6; i++) {
    grid->InsertNextCell(VTK_QUAD, 4, face_ptIDs[i]);
  }
  
  boxMapper->SetInputData(grid);

  boxActor->SetMapper(boxMapper);
  boxActor->GetProperty()->SetEdgeVisibility(true);

  hide(false);

  addProp(boxActor);
  locator->LazyEvaluationOn();
}

BoxWidgetLayer::~BoxWidgetLayer() {}

const std::string &BoxWidgetLayer::classname() const {
  static const std::string nm("BoxWidgetLayer");
  return nm;
}

void BoxWidgetLayer::start_clipping() { }

void BoxWidgetLayer::stop_clipping() { }

void BoxWidgetLayer::set_clip_parity(bool b) { }

void BoxWidgetLayer::setModified() {
  grid->Modified();
}

vtkSmartPointer<vtkDataSet> BoxWidgetLayer::get_pickable_dataset() {
  return grid;
}

vtkSmartPointer<vtkProp3D> BoxWidgetLayer::get_pickable_prop3d() {
  return boxActor;
}

vtkSmartPointer<vtkPoints> BoxWidgetLayer::get_pickable_points() {
  return points;
}

vtkSmartPointer<vtkAbstractCellLocator> BoxWidgetLayer::get_locator() {
  locator->Initialize();
  locator->SetDataSet(grid);
  return locator;
}

// TODO: Define this to work for cell types other than VTK_QUAD.
Coord3D *BoxWidgetLayer::get_cellCenter(vtkIdType cellID) {
  int cellType = grid->GetCellType(cellID);
  if (cellType == VTK_QUAD) {
    vtkIdType *pointIDs;
    vtkIdType npts;
    grid->GetCellPoints(cellID, npts, pointIDs);
    Coord3D corners[4];
    Coord3D *center = new Coord3D(0, 0, 0);
    for (int i = 0; i < 4; i++) {
      double temp[3]; 
      points->GetPoint(pointIDs[i], temp);
      corners[i] = Coord3D(temp);
      *center += corners[i];
    }
    *center /= 4;
    return center;
  }
  return NULL;
}

// TODO: Define this to work for cell types other than VTK_QUAD.
Coord3D *BoxWidgetLayer::get_cellNormal_Coord3D(vtkIdType cellID) {
  // Returns the "normal" vector to the cell. If the cell is a
  // VTK_QUAD (a box face), this is straightforward, since the normal
  // vector is just the normal vector of [the plane in which [the face
  // in question] lies]. But, if the cell is a VTK_LINE (an edge of
  // the box), the "normal" should be the vector from [the center of
  // the opposite edge] to [the center of the edge in
  // question]. Further, if the cell is a VTK_VERTEX (a corner of the
  // box), the normal vector should be the box's diagonal from [the
  // opposite corner] to [the corner in question].
  int cellType = grid->GetCellType(cellID);
  if (cellType == VTK_QUAD) {
    vtkIdType *pointIDs;
    vtkIdType npts;
    grid->GetCellPoints(cellID, npts, pointIDs);
    Coord3D corners[4];
    for (int i = 0; i < 4; i++) {
      double temp[3];
      points->GetPoint(pointIDs[i], temp);
      corners[i] = Coord3D(temp);
    }
    Coord3D vectors[2];
    vectors[0] = corners[1] - corners[0];
    vectors[1] = corners[2] - corners[1];
    Coord3D *normal = new Coord3D();
    *normal = cross(vectors[0], vectors[1]);
    double norm = sqrt(norm2(*normal));
    if (norm == 0) {
      delete normal;
      return NULL; 
    }
    *normal /= norm;
    return normal;
  } 
  return NULL;
}

void BoxWidgetLayer::set_box(const Coord3D *point) {
  // Resets the box to a rectangular prism with one corner at (0, 0,
  // 0) and the opposite corner at the position specified by point.
  double dimensions[3];
  dimensions[0] = (*point)[0];
  dimensions[1] = (*point)[1];
  dimensions[2] = (*point)[2];
  for (int i = 0; i < 8; i++) {
    points->SetPoint(i, dimensions[0] * double(i % 2),
		     dimensions[1] * double((i / 2) % 2),
		     dimensions[2] * double((i / 4) % 2));
  }
}

// void BoxWidgetLayer::set_visibility(bool visible) {
//   // Sets whether or not the box is visible.
//   oofcerr << "BoxWidgetLayer::set_visibility: " << int(visible) << std::endl;
//   boxActor->SetVisibility(int(visible));
// }

void BoxWidgetLayer::set_pointSize(float size) {
  boxActor->GetProperty()->SetPointSize(size);
}

void BoxWidgetLayer::set_lineWidth(float width) {
  boxActor->GetProperty()->SetLineWidth(width);
}

void BoxWidgetLayer::set_lineColor(const CColor &color) {
  boxActor->GetProperty()->SetEdgeColor(
			color.getRed(), color.getGreen(), color.getBlue());
}

void BoxWidgetLayer::set_faceColor(const CColor &color) {
  boxActor->GetProperty()->SetColor(
		    color.getRed(), color.getGreen(), color.getBlue());
}

void BoxWidgetLayer::set_opacity(double opacity) {
  boxActor->GetProperty()->SetOpacity(opacity);
}

void BoxWidgetLayer::set_position(const Coord3D *point) {
  // Sets the position of the 0th point of the box to the specified
  // location.

  // Compute the vector (as a double*) to translate each point by.
  double temp[3];
  points->GetPoint(0, temp);
  double translation[3];

  // Translate point 0.
  for (int j = 0; j < 3; j++) {
    translation[j] = (*point)[j] - temp[j];
    temp[j] = (*point)[j];
  }
  points->SetPoint(0, temp);

  // Translate points 1-7.
  for (int i = 1; i < 8; i++) {
    points->GetPoint(i, temp);
    for (int j = 0; j < 3; j++) {
      temp[j] += translation[j];
    }
    points->SetPoint(i, temp);
  }
}

// TODO: Define this to work for cell types other than VTK_QUAD.
void BoxWidgetLayer::offset_cell(vtkIdType cellID, double offset) {
  // Offsets the cell by the given amount in the direction of its
  // "normal".
  int cellType = grid->GetCellType(cellID);
  if (cellType == VTK_QUAD) {
    vtkIdType *pointIDs;
    vtkIdType npts;
    grid->GetCellPoints(cellID, npts, pointIDs);
    Coord3D corners[4];
    for (int i = 0; i < 4; i++) {
      double temp[3]; 
      points->GetPoint(pointIDs[i], temp);
      corners[i] = Coord3D(temp);
    }
    Coord3D vectors[2];
    vectors[0] = corners[1] - corners[0];
    vectors[1] = corners[2] - corners[1];
    Coord3D *normal = new Coord3D(); // TODO: Why use a pointer?
    // TODO: Use vtk methods to get the normal
    *normal = cross(vectors[0], vectors[1]);
    double norm = sqrt(norm2(*normal));
    if (norm == 0) {
      delete normal;
      return; 
    }
    *normal /= norm;
    *normal *= offset;
    for (int i = 0; i < 4; i++) {
      corners[i] += *normal;
      points->SetPoint(pointIDs[i],
		       corners[i][0], corners[i][1], corners[i][2]);
    }
    delete normal;
  } 
}

void BoxWidgetLayer::setCoincidentTopologyParams(double factor, double units)
{
  boxMapper->SetRelativeCoincidentTopologyPolygonOffsetParameters(factor,
								  units);
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
}

void SimpleCellLayer::newGrid(vtkSmartPointer<vtkPoints> pts, int ncells) {
  grid->Initialize();
  if(ncells > 0)
    grid->Allocate(ncells, ncells);
  grid->SetPoints(pts);
}

void SimpleCellLayer::start_clipping() {
  clipper = getClipper(this);
  clipper->SetInputData(grid);
  mapper->SetInputConnection(clipper->GetOutputPort());
}

void SimpleCellLayer::stop_clipping() {
  if(clipState == CLIP_ON) {
    clipper->RemoveAllInputs();
    clipper = vtkSmartPointer<vtkTableBasedClipDataSet>();
  }

  // When not clipping and connecting the grid directly to the mapper,
  // if there are no cells being drawn vtk7 (and vtk8) prints:
  
  // Warning: In ... Filters/Geometry/vtkDataSetSurfaceFilter.cxx, line 166
  // vtkDataSetSurfaceFilter: Number of cells is zero, no data to process.

  // The vtkDataSetSurfaceFilter is the GeometryExtractor of the
  // vtkDataSetMapper, and is used when the input data isn't
  // VTK_POLY_DATA.

  // If the grid is clipped, the vtkDataSetSurfaceFilter, isn't used,
  // and whatever is used doesn't complain about getting no data.

  mapper->SetInputData(grid);
}

void SimpleCellLayer::set_clip_parity(bool inverted) {
  clipper->SetInsideOut(!inverted);
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

bool SimpleCellLayer::visibleBoundingBox(vtkSmartPointer<vtkRenderer> renderer,
					 CRectangularPrism *bbox) const
{
  return getVisibleBoundingBox(grid, renderer, bbox);
}

void SimpleCellLayer::setCoincidentTopologyParams(double factor, double units) {
  mapper->SetRelativeCoincidentTopologyPolygonOffsetParameters(factor, units);
  mapper->SetRelativeCoincidentTopologyLineOffsetParameters(factor, units);
  mapper->SetRelativeCoincidentTopologyPointOffsetParameter(units);
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
    edgeExtractor->SetInputData(grid);
    mapper->SetInputConnection(edgeExtractor->GetOutputPort());
  }
  else {
    mapper->SetInputData(grid);
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
    clipper->SetInputData(grid);
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
    mapper->SetInputData(grid);
}

void SimpleWireframeCellLayer::set_clip_parity(bool inverted) {
  clipper->SetInsideOut(!inverted);
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
  glyph->SetInputData(glyphCenters);
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
  centerFinder->SetInputData(grid);
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
  glyphDirections->InsertNextTuple(direction);
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
  glyphClipper->SetInsideOut(!inverted);
}

//=\\=//=\\=//=\\=//=\\=//

ConeGlyphLayer::ConeGlyphLayer(GhostOOFCanvas *canvas, const std::string &name)
  : GlyphedLayer(canvas, name),
    coneSource(vtkSmartPointer<vtkConeSource>::New())
{
  glyph->SetSourceConnection(coneSource->GetOutputPort());
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
    // glyphCenters->Update();
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
  glyph->SetSourceConnection(sphereSource->GetOutputPort());
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
  grid->Initialize();		// TODO: Is this necessary?
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

LineSegmentLayer::LineSegmentLayer(GhostOOFCanvas *canvas,
				   const std::string &nm)
  : SimpleWireframeCellLayer(canvas, false, nm)
{}

const std::string &LineSegmentLayer::classname() const {
  static const std::string nm("LineSegmentLayer");
  return nm;
}

void LineSegmentLayer::set_nSegs(int nseg) {
  grid->Initialize();
  if(nseg > 0)
    grid->Allocate(nseg, nseg);
  grid->SetPoints(vtkSmartPointer<vtkPoints>::New());
}

void LineSegmentLayer::addSegment(const Coord *a, const Coord *b) {
  vtkIdType ids[2];
  vtkSmartPointer<vtkPoints> points = grid->GetPoints();
  ids[0] = points->InsertNextPoint((*a)[0], (*a)[1], (*a)[2]);
  ids[1] = points->InsertNextPoint((*b)[0], (*b)[1], (*b)[2]);
  grid->InsertNextCell(VTK_LINE, 2, ids);
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

void ImageCanvasLayer::filterModified() {
  excluder->Modified();
}

void ImageCanvasLayer::set_image(const ImageBase *img, const Coord *location,
				 const Coord *size)
{
  if(image != img) {
    pipelineLock.acquire();
    image = img;
    gridifier->SetInputData(image->getVTKImageData());
    pipelineLock.release();
  }
}

// TODO: Does opacity work?
void ImageCanvasLayer::set_opacity(double opacity) {
  actor->GetProperty()->SetOpacity(opacity);
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
  clipper->SetInsideOut(!inverted);
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

bool ImageCanvasLayer::visibleBoundingBox(vtkSmartPointer<vtkRenderer> renderer,
					  CRectangularPrism *bbox)
  const
{
  return getVisibleBoundingBox(mapper->GetInput(), renderer, bbox);
}

void ImageCanvasLayer::setCoincidentTopologyParams(double factor, double units)
{
  mapper->SetRelativeCoincidentTopologyPolygonOffsetParameters(factor, units);
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
