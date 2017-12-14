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

#ifndef GHOSTOOFCANVAS_H
#define GHOSTOOFCANVAS_H

// Uncomment this line to display the subset of the grid being
// considered for selections.
// #define DEBUGSELECTIONS

class GhostOOFCanvas;

#include "common/ccolor.h"
#include "common/clip.h"
#include "common/coord_i.h"
#include "common/direction.h"
#include "common/geometry.h"
#include "common/lock.h"
#include "common/IO/canvaslayers.h"

#include <vtkActor.h>
#include <vtkAxesActor.h>
#include <vtkCell.h>
#include <vtkPlanes.h>
#include <vtkRenderer.h>
#include <vtkScalarBarActor.h>
#include <vtkScalarsToColors.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

// #include <vtkXOpenGLRenderWindow.h>
#ifdef OOF_USE_COCOA
#include <vtkCocoaRenderWindow.h>
#else
#include <vtkRenderWindow.h>
#endif // OOF_USE_COCOA

class View;
class ImageFormat;
class OOFCanvasLayer;
class OOFCanvasLayerBase;

class GhostOOFCanvas {
protected:
  static bool initialized;	// has pygtk been initialized?
  bool created;			// used by OOFCanvas3D::realize
  bool exposed;
  bool axes_showing;		// axes are actually drawn
  bool antialiasing;		// has antialiasing been turned on?
  // TODO: Use vtkNew instead of vtkSmartPointer here, and remove the
  // lines that initialize the vtkSmartPointers in the GhostOOFCanvas
  // constructor.  Doing this requires vtk8, though.
#ifdef OOF_USE_COCOA
  vtkSmartPointer<vtkCocoaRenderWindow> render_window;
#else
  vtkSmartPointer<vtkRenderWindow> render_window;
#endif // OOF_USE_COCOA
  vtkSmartPointer<vtkRenderer> renderer;
  vtkSmartPointer<vtkAxesActor> axes;
  vtkSmartPointer<vtkScalarBarActor> contourMapActor;
  bool contourmap_requested;
  bool contourmap_showing;
  OOFCanvasLayer *contour_layer;
  virtual void repositionRenderWindow() {}

  ClippingPlaneList clipPlanes;	// typedef in common/clip.h
  bool clipInverted;
  bool clipSuppressed;
  vtkSmartPointer<vtkPlanes> vClipPlanes;
  CanvasLayerList layers;
  SLock viewLock;

  Coord3D tumbleCenter;
  bool tumbleAroundFocalPoint;

  double margin;
  void makeAllUnpickable() const;
  void fixScreenCoord(const Coord*, double &x, double &y) const;
  void findClickedCell_(const Coord*, const View*, OOFCanvasLayer*,
			vtkSmartPointer<vtkCell>&, Coord&, vtkIdType&, int&);
  vtkSmartPointer<vtkUnstructuredGrid> getFrustumSubgrid(
		 double x, double y, const View*, OOFCanvasLayer*);

#ifdef DEBUGSELECTIONS
  vtkSmartPointer<vtkActor> tempActor;
#endif // DEBUGSELECTIONS

public:
  GhostOOFCanvas();
  virtual ~GhostOOFCanvas();

  // newLayer() and removeLayer() are called by the OOFCanvasLayerBase
  // constructor and destructor.
  void newLayer(OOFCanvasLayerBase*);
  void removeLayer(OOFCanvasLayerBase*);

  void reset();

  // This should only be called from python and only with mainthread.run
  void render();

  void set_bgColor(const CColor);
  void set_margin(double f) { margin = f; }
  
  void setAntiAlias(bool);
  //void setFXAAOptions(double, double, double, double, int, bool);

  void setAxisOffset(const Coord*);
  void setAxisLength(const Coord*);
  void setAxisProperties();
  void showAxisLabels(bool);
  void setAxisLabelColor(const CColor*);
  void setAxisLabelFontSize(int);
  void toggleAxes(bool);

  void noContourMap();
  void setContourMap(OOFCanvasLayer*, vtkScalarsToColors*);
  void updateContourMap(OOFCanvasLayer*, vtkScalarsToColors*);
  void showContourMap(bool);
  void setContourMapBGColor(const CColor*, float);
  void setContourMapSize(float, float);
  void setContourMapTextColor(const CColor*);
  void setContourMapPosition(float, float);

  void orthogonalize_view_up();
  void recalculate_clipping();

  // movements
  void track(double x, double y, double z);
  void dolly(double factor);
  void dolly_fill();
  void roll(double a); 
  void pitch(double a);
  void yaw(double a);
  void azimuth(double a);
  void elevation(double a);
  void zoom(double a);
  void zoom_fill();
  void recenter();
  void setTumbleCenter(Coord3D*);
  void setTumbleAroundFocalPoint();

  // TODO: These should all be const, but it might not be possible.
  // They have to call set_view.
  Coord findRayThroughPoint(const Coord*) const;
  Coord *findClickedPositionOnActor(const Coord*, const View*, 
				    OOFCanvasLayer*);
  vtkSmartPointer<vtkActor> findClickedActor(const Coord*, const View*,
					     OOFCanvasLayer*);
  vtkSmartPointer<vtkActorCollection> findClickedActors(const Coord*,
							const View*,
							OOFCanvasLayer*);
  vtkSmartPointer<vtkCell> findClickedCell(const Coord*, const View*,
					   OOFCanvasLayer*);
  Coord *findClickedPosition(const Coord*, const View*,
			     OOFCanvasLayer*);
  vtkIdType findClickedCellID(const Coord*, const View*, OOFCanvasLayer*,
			      Coord*);
  Coord *findClickedCellCenter(const Coord*, const View*, OOFCanvasLayer*);
  Coord *findClickedPoint(const Coord*, const View*, OOFCanvasLayer*);
  Coord *findClickedSegment(const Coord*, const View*, OOFCanvasLayer*);
  vtkSmartPointer<vtkIdList> findClickedFace(const Coord*, const View*,
   					     OOFCanvasLayer*);

  // camera info
  Coord *get_camera_position_v2() const;
  Coord get_camera_direction_of_projection_v2() const;

  Coord get_camera_position() const;
  void set_camera_position(double x, double y, double z) const;
  void get_camera_focal_point(double *p) const;
  void set_camera_focal_point(double x, double y, double z) const;
  void get_camera_view_up(double *p) const;
  void get_camera_direction_of_projection(double *p) const;
  double get_camera_distance() const;
  double get_camera_view_angle() const;
  const ClippingPlaneList &getClipPlanes() const { return clipPlanes; }
  vtkSmartPointer<vtkRenderer> get_renderer() { return renderer; }
  
  bool clipping() const;
  vtkSmartPointer<vtkPlanes> getVTKClipPlanes() const { return vClipPlanes; }
  bool invertedClipping() const { return clipInverted; }
  bool suppressedClipping() const { return clipSuppressed; }

  // 2D <-> 3D coordinate transformations
  Coord display2Physical(const View*, double, double);
  void physical2Display(const Coord&, double&, double&) const;
  

  // Views
  View *get_view() const;
  // set_view acquires viewLock, calls set_view_nolock, and releases
  // viewLock.  It returns the old view.  If it's necessary to restore
  // the old view before releasing the lock, acquire the lock
  // explicitly and use set_view_nolock.  See findClickedCell_ et al.
  View *set_view(const View*, bool);
  View *set_view_nolock(const View*, bool);
  void restore_view(const View*, bool);

  ICoord get_size() const;
  void set_size(int, int);

  SLock renderLock;

  void save_canvas(const std::string &filename, const ImageFormat*) const;

  void dumpProps();		// debugging

  friend class OOFCanvasLayer;
};				// end GhostOOFCanvas

bool findSegLineDistance(const Coord&, const Coord&, const Coord&, const Coord&,
			 double &, double&);

#endif // GHOSTOOFCANVAS_H



