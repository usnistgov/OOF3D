// -*- C++ -*-
// $RCSfile: ghostoofcanvas.swg,v $
// $Revision: 1.1.2.76 $
// $Author: fyc $
// $Date: 2014/07/22 17:55:52 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GHOSTOOFCANVAS_SWG
#define GHOSTOOFCANVAS_SWG

%module ghostoofcanvas
%include "common/typemaps.swg"
%extern "common/coord.swg"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"
%extern "common/IO/view.swg"
%pragma(python) code="from ooflib.SWIG.common.IO.view import ViewPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkCellPtrPtr"

class vtkCellPtr;
class ImageFormat;

%{
#include "common/IO/canvaslayers.h"
#include "common/IO/ghostoofcanvas.h"
#include "common/IO/view.h"
#include "common/IO/vtkutils.h"
%}

class GhostOOFCanvas {
public:
  GhostOOFCanvas();

  ICoord get_size();
  void set_size(int, int);

  void set_bgColor(const CColor);
  void set_margin(double f);
  void setAntiAlias(bool);

  void setAxisOffset(Coord *Point);
  void setAxisLength(Coord *Point);
  void showAxisLabels(bool);
  void setAxisLabelColor(const CColor*);
  void setAxisLabelFontSize(int);
  void toggleAxes(bool);

  void noContourMap();
  void showContourMap(bool);
  void setContourMapBGColor(const CColor*, float);
  void setContourMapSize(float, float);
  void setContourMapTextColor(const CColor*);
  void setContourMapPosition(float, float);

  void reset();
  void render();

  void orthogonalize_view_up();
  void recalculate_clipping();

  void track(double, double, double);
  void dolly(double);
  void dolly_fill();
  void roll(double);
  void pitch(double);
  void yaw(double);
  void azimuth(double);
  void elevation(double);
  void zoom(double);
  void zoom_fill();
  void recenter();

  // camera info
  %addmethods{    

    // TODO MER: Use the Coord typemap for all of these!

    PyObject *get_camera_position() {
      Coord x;
      x = self->get_camera_position();
      PyObject *result = PyList_New((Py_ssize_t) DIM);
      if(result == NULL) 
	return NULL;
      for(int i=0; i<DIM; ++i) 
	PyList_SET_ITEM(result, (Py_ssize_t) i, PyFloat_FromDouble(x[i]));
      return result;
    }

    PyObject *get_camera_focal_point() {
      double x[3];
      self->get_camera_focal_point(x);
      PyObject *result = PyList_New((Py_ssize_t) DIM);
      if(result == NULL) 
	return NULL;
      for(int i=0; i<DIM; ++i) 
	PyList_SET_ITEM(result, (Py_ssize_t) i, PyFloat_FromDouble(x[i]));
      return result;
    }

    PyObject *get_camera_view_up() {
      double x[3];
      self->get_camera_view_up(x);
      PyObject *result = PyList_New((Py_ssize_t) DIM);
      if(result == NULL) 
	return NULL;
      for(int i=0; i<DIM; ++i) 
	PyList_SET_ITEM(result, (Py_ssize_t) i, PyFloat_FromDouble(x[i]));
      return result;
    }

    PyObject *get_camera_direction_of_projection() {
      double x[3];
      self->get_camera_direction_of_projection(x);
      PyObject *result = PyList_New((Py_ssize_t) DIM);
      if(result == NULL) 
	return NULL;
      for(int i=0; i<DIM; ++i) 
	PyList_SET_ITEM(result, (Py_ssize_t) i, PyFloat_FromDouble(x[i]));
      return result;
    }
  }

  double get_camera_distance();
  double get_camera_view_angle();
  void set_camera_position(double, double, double);
  void set_camera_focal_point(double, double, double);

  vtkCellPtr findClickedCell(Coord *Point, View*, OOFCanvasLayer*);
  int findClickedCellID(Coord *Point, View*, OOFCanvasLayer*, Coord *outCoord);
  %new Coord *findClickedCellCenter(Coord *Point, View*, OOFCanvasLayer*);
  %new Coord *findClickedPosition(Coord *Point, View*, OOFCanvasLayer*);
  %new Coord *findClickedPoint(Coord *Point, View*, OOFCanvasLayer*);
  %new Coord *findClickedSegment(Coord *Point, View*, OOFCanvasLayer*);
  vtkIdListPtr findClickedFace(Coord *Point, View*, OOFCanvasLayer*);

  Coord display2Physical(View*, double, double);

  // Coord get_bounds();
  Coord get_visible_center();
  Coord get_visible_size();

  // views
  %new View *get_view();
  // set_view() returns the old view, which was obtained with
  // get_view(), hence %new.  If the second arg is true the clip
  // planes will also be set.
  %new View *set_view(View *v, bool);
  
// save
  void save_canvas(char *filename, ImageFormat*);

};

#endif	// GHOSTOOFCANVAS_SWG


