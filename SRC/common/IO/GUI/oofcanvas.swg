// -*- C++ -*-
// $RCSfile: oofcanvas.swg,v $
// $Revision: 1.68.18.2 $
// $Author: langer $
// $Date: 2014/09/27 22:34:12 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef OOFCANVAS_SWG
#define OOFCANVAS_SWG

%module oofcanvas

%include "common/typemaps.swg"
%{
#include "common/IO/GUI/oofcanvas.h"
#include "common/ooferror.h"
#include "common/IO/GUI/rubberband.h"
typedef std::vector<GnomeCanvasPoints*> GtkPointVec;
typedef std::vector<gushort> ColorVec;
%}

%extern "common/geometry.swg"
%extern "common/coord.swg"
%pragma(python) code="from ooflib.SWIG.common.geometry import CRectanglePtr"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"

class OOFCanvasLayer;
class GnomeCanvasGroup;
class StringImage;
class AlphaStringImage;


// Typemap to convert from a Python Color object to a Gtk guint32
// packed rgba color.  Assumes that the Python Color has functions
// getRed(), getGreen(), and getBlue(), which return Floats between 0
// and 1.

%typemap(python,in) guint32 *color (guint32 tmp) {
  PyObject *redobj = PyObject_CallMethod($source, (char *) "getRed", NULL);
  PyObject *grnobj = PyObject_CallMethod($source, (char *) "getGreen", NULL);
  PyObject *bluobj = PyObject_CallMethod($source, (char *) "getBlue", NULL);
  if(!(redobj && grnobj && bluobj)) {
    PyErr_SetString(PyExc_TypeError, "guint32* typemap: Failed to evaluate Color.");
    return NULL;
  }
  unsigned char red = (unsigned char)(255*PyFloat_AsDouble(redobj));
  unsigned char grn = (unsigned char)(255*PyFloat_AsDouble(grnobj));
  unsigned char blu = (unsigned char)(255*PyFloat_AsDouble(bluobj));
 
  tmp = GNOME_CANVAS_COLOR_A(red, grn, blu, 255); // 255=opaque
  $target = &tmp;
  Py_XDECREF(redobj);
  Py_XDECREF(grnobj);
  Py_XDECREF(bluobj);
}

%typemap(python, in) ColorVec* (ColorVec tmp) {
  PyObject *redobj = PyObject_CallMethod($source, (char *) "getRed", NULL);
  PyObject *grnobj = PyObject_CallMethod($source, (char *) "getGreen", NULL);
  PyObject *bluobj = PyObject_CallMethod($source, (char *) "getBlue", NULL);
  if(!(redobj && grnobj && bluobj)) {
    PyErr_SetString(PyExc_TypeError, "ColorVec* typemap: Failed to evaluate Color.");
    return NULL;
  }
  tmp.resize(3);
  tmp[0] = gushort(65535*PyFloat_AsDouble(redobj));
  tmp[1] = gushort(65535*PyFloat_AsDouble(grnobj));
  tmp[2] = gushort(65535*PyFloat_AsDouble(bluobj));
  $target = &tmp;
  Py_XDECREF(redobj);
  Py_XDECREF(grnobj);
  Py_XDECREF(bluobj);
}

// Typemaps to convert from Segments, Curves, and Polygons (all
// defined in primitives.py) to a GnomeCanvasPoints struct.
 
%{

  // Convert a Segment of Coords or Points into a GnomeCanvasPoints struct.
  static GnomeCanvasPoints *segment2gtk(PyObject *segment) {
    GnomeCanvasPoints *pts = gnome_canvas_points_new(2); // must be freed elsewhere
    PyObject *start = PyObject_CallMethod(segment, (char *) "start", NULL);
    PyObject *endpt = PyObject_CallMethod(segment, (char *) "end", NULL);
    if(PyObject_HasAttrString(start, "this")) {
      // The Segment is made of swigged objects, which must be Coords
      Coord *cstart=0, *cend=0;
      PyObject *sobj = PyObject_GetAttrString(start, "this");
      char *str = PyString_AsString(sobj);
      Py_XDECREF(sobj);
      if(SWIG_GetPtr(str, (void**) &cstart, "_Coord_p")) {
	PyErr_SetString(PyExc_TypeError,
			"Type error in segment2gtk.  Expected _Coord_p");
	return NULL;
      }
      sobj = PyObject_GetAttrString(endpt, "this");
      str = PyString_AsString(sobj);
      Py_XDECREF(sobj);
      if(SWIG_GetPtr(str, (void**) &cend, "_Coord_p")) {
	PyErr_SetString(PyExc_TypeError,
			"Type error in segment2gtk.  Expected _Coord_p");
	return NULL;
      }
      pts->coords[0] = (*cstart)(0);
      pts->coords[1] = (*cstart)(1);
      pts->coords[2] = (*cend)(0);
      pts->coords[3] = (*cend)(1);
    }	
    else {
      PyObject *x0 = PyObject_GetAttrString(start, "x");
      PyObject *y0 = PyObject_GetAttrString(start, "y");
      PyObject *x1 = PyObject_GetAttrString(endpt, "x");
      PyObject *y1 = PyObject_GetAttrString(endpt, "y");
      if(!(x0 && y0 && x1 && y1)) {
	PyErr_SetString(PyExc_AttributeError,
			"Segment component doesn't have x and y attributes.");
	return NULL;
      }
      pts->coords[0] = PyFloat_AsDouble(x0);
      pts->coords[1] = PyFloat_AsDouble(y0);
      pts->coords[2] = PyFloat_AsDouble(x1);
      pts->coords[3] = PyFloat_AsDouble(y1);
      Py_XDECREF(x0);
      Py_XDECREF(y0);
      Py_XDECREF(x1);
      Py_XDECREF(y1);
    }
    Py_XDECREF(start);
    Py_XDECREF(endpt);
    return pts;
  }
%}

%typemap(python, in) GnomeCanvasPoints *segment (GnomeCanvasPoints *pts) {
  pts =  segment2gtk($source);
  $target = pts;
}

// Convert a List of Segments to a std::vector of GnomeCanvasPoints*.

%typemap(python, in) GtkPointVec* (GtkPointVec ptvec) {
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		  "Type error in GtkPointVec* typemap. Python list required.");
    return NULL;
  }
  GtkPointVec::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source), Py_ssize_t,
					       GtkPointVec::size_type);
  ptvec.resize(sz);
  for(GtkPointVec::size_type i=0; i<sz; i++)
    ptvec[i] = segment2gtk(PyList_GET_ITEM($source, (Py_ssize_t) i));
  $target = &ptvec;
}

%typemap(python,freearg) GtkPointVec* {
  for(std::vector<GnomeCanvasPoints*>::size_type i=0; i<ptvec.size(); i++)
    gnome_canvas_points_unref(ptvec[i]);
}

// Convert a Curve or Polygon of Points or Coords into a
// GnomeCanvasPoints struct.

%typemap(python, in) GnomeCanvasPoints *curve (GnomeCanvasPoints *pts) {
  PyObject *ptlist = PyObject_CallMethod($source, (char *) "points", NULL);
  if(!PyList_Check(ptlist)) {
    PyErr_SetString(PyExc_TypeError, "Typemap snafu!");
    return NULL;
  }
  int sz = Py_SAFE_DOWNCAST(PyList_Size(ptlist), Py_ssize_t, int);
  pts = gnome_canvas_points_new(sz);

  // Here we have to check to see if we have a List of Points or
  // Coords.  Points are Python objects with .x and .y members.
  // Coords are C++ objects already, but we have to decipher the SWIG
  // pointer to find out where they are.

  PyObject *firstpoint = PyList_GET_ITEM(ptlist, (Py_ssize_t) 0);
  if(PyObject_HasAttrString(firstpoint, "this")) {
    // The PyObject is a swigged object.  Assume it's a Coord.
    for(int i=0; i<sz; i++) {
      PyObject *swiggedcoord = PyList_GET_ITEM(ptlist, (Py_ssize_t) i);
      Coord *coord;
      PyObject *sobj = PyObject_GetAttrString(swiggedcoord, "this");
      char *str = PyString_AsString(sobj);
      Py_XDECREF(sobj);
      if(SWIG_GetPtr(str, (void**) &coord, "_Coord_p")) {
	PyErr_SetString(PyExc_TypeError,
			"Type error in curve typemap: expected _Coord_p");
	return NULL;
      }
      pts->coords[2*i] = (*coord)(0);
      pts->coords[2*i+1] = (*coord)(1);
    }
  }
  else {
    // We have a list of pure Python objects.  Assume they're Points.
    for(int i=0; i<sz; i++) {
      PyObject *point = PyList_GET_ITEM(ptlist, (Py_ssize_t) i); // Point object
      PyObject *x = PyObject_GetAttrString(point, "x");
      PyObject *y = PyObject_GetAttrString(point, "y");
      if(!(x && y)) {
// 	std::cerr << PyString_AsString(PyObject_Repr(point)) << std::endl;
	PyErr_SetString(PyExc_AttributeError,
			"Curve component doesn't have x and y attributes.");
	return NULL;
      }
      pts->coords[2*i] = PyFloat_AsDouble(x);
      pts->coords[2*i+1] = PyFloat_AsDouble(y);
      Py_XDECREF(x);
      Py_XDECREF(y);
    }
  }
  $target = pts;
  Py_XDECREF(ptlist);
}

%typemap(python, in) guint* (guint tmp) {
  tmp = (guint) PyInt_AsLong($source);
  $target = &tmp;
}

%typemap(python,freearg) GnomeCanvasPoints * {
  gnome_canvas_points_unref(pts);
}


class OOFCanvas {
public:
  OOFCanvas(bool antialias);
  PyObject *widget();
  PyObject *rootitem();
  PyObject *get_hadjustment();
  PyObject *get_vadjustment();
  ICoord get_allocation(); // for debugging

  double get_pixels_per_unit();
  void set_pixels_per_unit(double);
  void zoom(double);
  void zoomAbout(double, Coord *Point);
  CRectangle get_scrollregion();
  ICoord get_scroll_offsets();
  void set_scroll_offsets(ICoord *iPoint);
  void set_scrollregion(CRectangle&);
  CRectangle get_bounds();
  int get_width_in_pixels();
  int get_height_in_pixels();
  Coord world_coord(int, int);
  Coord window_coord(Coord *Point);

  OOFCanvasLayer *newLayer();
  void deleteLayer(OOFCanvasLayer*);
  
  void set_mouse_callback(PyObject *pythonCallable);
  void set_configure_callback(PyObject *pythonCallable);

  void show();
  void clear();
  void underlay();

  bool is_empty();

  void set_lineWidth(unsigned int);
  void set_lineColor(guint32 *color);
  void set_fillColor(guint32 *color, unsigned char);
  void set_underlay_params(ColorVec*, double);
  void set_bgColor(ColorVec*);
  void set_margin(double);

  void draw_dot(const Coord* Point);
  void draw_triangle(const Coord* Point, double angle);
  void draw_segment(GnomeCanvasPoints *segment);
  void draw_segments(GtkPointVec*);
  void draw_curve(GnomeCanvasPoints *curve);
  void draw_polygon(GnomeCanvasPoints *curve);
  void fill_polygon(GnomeCanvasPoints *curve);
  void draw_circle(Coord&, double);
  void fill_circle(Coord&, double);
  void draw_image(AbstractImage*, Coord*, Coord *Point);
  void draw_alpha_image(AbstractImage*, Coord*, Coord *Point); //, unsigned char);
  void set_rubberband(RubberBand*);
};

class OOFCanvasLayer { //The buffered canvas layer lives in outputdevice.py 
public:
  OOFCanvasLayer(OOFCanvas*);
  ~OOFCanvasLayer();
  void raise_layer(int);
  void raise_to_top();
  void lower_layer(int);
  void show();
  void hide();
  void move(double, double);
  void clear();
  void make_current();
  void destroy();
};

#endif // OOFCANVAS_SWG
