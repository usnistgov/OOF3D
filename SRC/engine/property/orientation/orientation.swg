// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef ORIENTATION_SWG
#define ORIENTATION_SWG

%module orientation
%include "common/typemaps.swg"
%{
#include "common/swiglib.h"
#include "engine/corientation.h"
#include "engine/property/orientation/orientation.h"
%}
%include "engine/propertyhdr.swg"
%extern "engine/corientation.swg"


%pragma(python) include="engine/property/orientation/orientation.spy"
%pragma(python) code="from ooflib.SWIG.engine.corientation import COrientationPtr"


// Typemap for converting a convertible registered Orientation gizmo
// from orientationmatrix.py into a COrientation.  The COrientation is
// already a C++ object, and a pointer to it is stored in the
// Orientation object.

%typemap(python,in) COrientation * {
  PyObject *py_orient = PyObject_GetAttrString($source,"corient");
  SWIG_GetPtrObj(py_orient, (void **)(&$target), "_COrientation");
}

class OrientationProp : public Property {
public:
  OrientationProp(PyObject *registry, char *name, COrientation *orient);
  const COrientation *orientation();
};

%typemap(python,in) COrientation * {}

#endif // ORIENTATION_SWG
