// -*- C++ -*-


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
%extern "common/IO/vtkutils.swg"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"
%extern "common/IO/view.swg"
%pragma(python) code="from ooflib.SWIG.common.IO.view import ViewPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkCellPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkActorPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkActorCollectionPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkIdListPtrPtr"

class vtkActorCollectionPtr;
class vtkActorPtr;
class vtkCellPtr;
class ImageFormat;

%{
#include "common/IO/canvaslayers.h"
#include "common/IO/ghostoofcanvas.h"
#include "common/IO/view.h"
#include "common/IO/vtkutils.h"
typedef std::vector<OOFCanvasLayer*> CanvasLayerVec;
%}

%typemap(python, in) CanvasLayerVec *layerVec (CanvasLayerVec v) {
  // typemap(python, in) CanvasLayerVec *layerVec
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Type error in ICoordVec typemap. Python list required.");
    return NULL;
  }
  CanvasLayerVec::size_type sz = Py_SAFE_DOWNCAST(
		  PyList_Size($source), Py_ssize_t, CanvasLayerVec::size_type);
  v.resize(sz);
  for(CanvasLayerVec::size_type i=0; i<sz; i++) {
    OOFCanvasLayer *layer;
    PyObject *swigstr =
      PyObject_GetAttrString(PyList_GET_ITEM($source, (Py_ssize_t) i), "this");
    if(!swigstr)
      return 0;
    char *str = PyString_AsString(swigstr);
    SWIG_GetPtr(str, (void**)&layer, "_OOFCanvasLayer_p");
    v[i] = layer;
  }
  $target = &v;
}

%typemap(python, out) CoordAndInt* {
  // typemap(python, out) CoordAndInt*
  char _ptemp[128];
  static PyObject *coordClass = 0;
  static PyObject *pyOne = 0;
  if(!coordClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.common.coord");
    coordClass = PyObject_GetAttrString(module, "CoordPtr");
    Py_XDECREF(module);
    if(!coordClass) return 0;
    pyOne = PyInt_FromLong(1);
  }
  SWIG_MakePtr(_ptemp, (void*)(&$source->coord), "_Coord_p");
  PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
  PyObject *coord = PyObject_CallObject(coordClass, swigthis);
  Py_XDECREF(swigthis);
  PyObject_SetAttrString(coord, "thisown", pyOne);

  $target = PyTuple_Pack(2, coord, PyInt_FromLong($source->val));
}


class GhostOOFCanvas {
public:
  GhostOOFCanvas();

  ICoord get_size();
  void set_size(int, int);

  void set_bgColor(const CColor);
  void set_margin(double f);
  void setAntiAlias(bool);
  // void setFXAAOptions(double, double, double, double, int, bool);

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
    // If this is ever fixed, then get_camera_position and
    // get_camera_position_v2 (below) will do practically the same
    // thing, so all calls to get_camera_position_v2 should be changed
    // to calls to get_camera_position.  Get_camera_position_v2 is
    // only used in a few places, which can be found using the
    // terminal command 'sf get_camera_position_v2', so this shouldn't
    // be hard to do. Likewise, all calls to
    // get_camera_direction_of_projection_v2 will have to be changed
    // to calls to get_camera_direction_of_projection.

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

  // These do the same as get_camera_position and
  // get_camera_direction_of_projection, but they each return a Coord*
  // instead of Python list.
  %new Coord *get_camera_position_v2();
  Coord get_camera_direction_of_projection_v2();

  vtkRendererPtr get_renderer();
  double get_camera_distance();
  double get_camera_view_angle();
  void set_camera_position(double, double, double);
  void set_camera_focal_point(double, double, double);
  void setTumbleCenter(Coord *Point);
  void setTumbleAroundFocalPoint();

  Coord findRayThroughPoint(const Coord *Point);
  %new Coord *findClickedPositionOnActor(Coord *Point, View*, OOFCanvasLayer*);
  vtkActorPtr findClickedActor(Coord *Point, View*, OOFCanvasLayer*);
  vtkActorCollectionPtr findClickedActors(Coord *Point, View*, OOFCanvasLayer*);
  vtkCellPtr findClickedCell(Coord *Point, View*, OOFCanvasLayer*);
  int findClickedCellID(Coord *Point, View*, OOFCanvasLayer*, Coord *outCoord);
  %new Coord *findClickedCellCenter(Coord *Point, View*, OOFCanvasLayer*);
  %new Coord *findClickedPosition(Coord *Point, View*, OOFCanvasLayer*);
  %new Coord *findClickedPoint(Coord *Point, View*, OOFCanvasLayer*);
  vtkIdListPtr findClickedSegment(Coord *Point, View*, OOFCanvasLayer*);
  vtkIdListPtr findClickedFace(Coord *Point, View*, OOFCanvasLayer*);

  %new CoordAndInt *findClickedCellCenterMulti(Coord *Point, View*,
					       CanvasLayerVec *layerVec);

  Coord display2Physical(View*, double, double);

  void setFixCanvasScaleBug(bool);

  // views
  %new View *get_view();
  // set_view() returns the old view, which was obtained with
  // get_view(), hence %new.  If the second arg is true the clip
  // planes will also be set.
  %new View *set_view(View *v, bool);
  
// save
  void save_canvas(char *filename, ImageFormat*);

  void dumpProps();		// debugging

};

#endif	// GHOSTOOFCANVAS_SWG


