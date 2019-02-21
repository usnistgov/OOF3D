// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GEOMETRY_SWG
#define GEOMETRY_SWG

%module geometry

%{
#include <oofconfig.h>
#include "common/geometry.h"
#include "common/cprism_i.h"
typedef class CPolygon<double, Coord> CPolygonCoord;
%}
%pragma(python) include="geometry.spy"
%include "common/typemaps.swg"

   // TODO: Why do we need this typemap?  Does it predate our
   // knowledge of %new?  It would seem to make an unnecessary copy of
   // its input.
%typemap(python, argout) CRectangularPrism *outPrism {
  // typemap(python, argout) CRectangularPrism *outPrism
  char _ptemp[128];
  static PyObject *prismClass = 0;
  static PyObject *pyOne = 0;
  if(!prismClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.common.geometry");
    prismClass = PyObject_GetAttrString(module, "CRectangularPrismPtr");
    Py_XDECREF(module);
    if(!prismClass) return 0;
    pyOne = PyInt_FromLong(1);
  }
  SWIG_MakePtr(_ptemp, (void*) $source, "_CRectangularPrism_p");
  PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
  PyObject *prism = PyObject_CallObject(prismClass, swigthis);
  Py_XDECREF(swigthis);
  PyObject_SetAttrString(prism, "thisown", pyOne);

  if(!PyList_Check($target)) {
    PyObject *retval = $target;
    $target = PyList_New((Py_ssize_t) 0);
    PyList_Append($target, retval);
    Py_XDECREF(retval);
  }
  PyList_Append($target, prism);
}

%typemap(python, ignore) CRectangularPrism *outPrism {
  // typemap(python, ignore) CRectangularPrism *outPrism
  $target = new CRectangularPrism();
}
   

class CPolygonCoord {};

class CRectangularPrism : public CPolygonCoord {
public:
  CRectangularPrism(Coord *Point, Coord *Point);
  double xmin();
  double xmax();
  double ymin();
  double ymax();
  double zmin();
  double zmax();
  double height();
  double width();
  double depth();
  void expand(double factor);
  Coord center();
  Coord lowerleftback();
  Coord upperrightfront();
  void swallowPrism(CRectangularPrism&);
};

class COrientedPlane {
public:
  COrientedPlane(Coord *Point, double);
  COrientedPlane reversed();
  %addmethods {
    double getOffset() { return self->offset; }
    Coord getNormal() { return self->normal; }
  }
};

// class CQuadrilateral : public CPolygonCoord {
// public:
//   CQuadrilateral(Coord *Point, Coord *Point, Coord *Point, Coord *Point);
//   bool contains(Coord *Point);
//   double area();
// };

// class CTriangle : public CPolygonCoord {
// public:
//   CTriangle(Coord *Point, Coord *Point, Coord *Point);
//   bool contains(Coord *Point);
//   double area();
// };

//double triangleArea(Coord *Point, Coord *Point, Coord *Point);

//double pixelIntersection(CPolygonCoord, ICoord *iPoint, double, double);

#endif // GEOMETRY_SWG
