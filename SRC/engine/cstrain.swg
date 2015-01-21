// -*- C++ -*-
// $RCSfile: cstrain.swg,v $
// $Revision: 1.6.18.2 $
// $Author: langer $
// $Date: 2014/06/24 20:17:48 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSTRAIN_SWG
#define CSTRAIN_SWG

%module cstrain
%include "engine/typemaps.swg"
%{
#include "engine/cstrain.h"
#include "engine/IO/propertyoutput.h"
%}

%extern "engine/IO/propertyoutput.swg"
%pragma(python) code="from ooflib.SWIG.engine.IO.propertyoutput import PropertyOutputInitPtr"

%pragma(python) include="cstrain.spy"

class POInitGeometricStrain : public PropertyOutputInit {
public:
  POInitGeometricStrain();
};

%typemap(python,ignore) SymmMatrix3 *OUT (SymmMatrix3 *tmp) {
  // typemap(python, ignore) SymmMatrix3 *OUT
    tmp = new SymmMatrix3();
    $target = tmp;
}

%typemap(python,argout) SymmMatrix3 *OUT {
  // typemap(python, argout) SymmMatrix3 *OUT
  static PyObject *symmMatrix3Class = 0;
  static PyObject *pyOne;
  if(!symmMatrix3Class) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.symmmatrix");
    symmMatrix3Class = PyObject_GetAttrString(module, "SymmMatrix3Ptr");
    Py_XDECREF(module);
    if(!symmMatrix3Class) return 0;
    pyOne = PyInt_FromLong(1);
  }
  char _stemp[128];
  SWIG_MakePtr(_stemp, (char*)($source), "_SymmMatrix3_p");
  PyObject *swigthis = Py_BuildValue("(s)", _stemp);
  PyObject *mtx = PyObject_CallObject(symmMatrix3Class, swigthis);
  Py_XDECREF(swigthis);
  PyObject_SetAttrString(mtx, "thisown", pyOne);
  $target = mtx;
}

void findGeometricStrain(FEMesh*, Element*, MasterPosition&, SymmMatrix3 *OUT,
			 bool);

%typemap(python,argout) SymmMatrix3 *OUT {}
%typemap(python,ignore) SymmMatrix3 *OUT {}

#endif // CSTRAIN_SWG
