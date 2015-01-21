// -*- C++ -*-
// $RCSfile: contour.swg,v $
// $Revision: 1.12.10.3 $
// $Author: langer $
// $Date: 2013/11/08 20:44:57 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// OBSOLETE IN 3D

#ifndef CONTOUR_SWG
#define CONTOUR_SWG

%module contour
%include "engine/typemaps.swg"
%extern "engine/masterelement.swg"
%extern "engine/mastercoord.swg"

%pragma(python) code="from ooflib.SWIG.engine.mastercoord import MasterCoordPtr"
%pragma(python) include="contour.spy"

%{
#include "engine/IO/contour.h"
  typedef std::vector<ContourCoord*> ContourCoordVec;
  typedef std::vector<CCurve> CurveVec;
  extern int nContourStates, nCreated, nDeleted; // DEBUGGING
%}

%typemap(python, out) ContourCoordVec* {
  // Convert a vector of ContourCoord*s to a list of swigged ContourCoordPtrs.
  ContourCoordVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  char _ptemp[128];
  for(std::vector<ContourCoord*>::size_type i=0; i<sz; i++) {
    SWIG_MakePtr(_ptemp, (char*)((*$source)[i]), "_ContourCoord_p");
    PyList_SET_ITEM($target, (Py_ssize_t) i, Py_BuildValue("s", _ptemp));
  }
}

%typemap(python, out) CurveVec* {
  // Convert a vector of CCurves (which are std::deques of
  // MasterCoord*'s) to a list of lists of MasterCoords.
  char _ptemp[128];
  CurveVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
//   std::cerr << "CurveVec typemap: size=" << $source->size() << std::endl;
  for(std::vector<CCurve>::size_type i=0; i<sz; i++) {
    CCurve &curve = (*$source)[i];
    assert((int)curve.size() >= PY_SSIZE_T_MIN && 
	   (int)curve.size() <= PY_SSIZE_T_MAX);
    PyObject *coordlist = PyList_New((Py_ssize_t) curve.size());
    PyList_SET_ITEM($target, (Py_ssize_t) i, coordlist);
    for(CCurve::size_type j=0; j<curve.size(); j++) {
      SWIG_MakePtr(_ptemp, (char*)(curve[j]), "_MasterCoord_p");
      PyList_SET_ITEM(coordlist, (Py_ssize_t) j, Py_BuildValue("s", _ptemp));
    }
  }
}

class ContourCoord : public MasterCoord {
public:
  double value;
};

class CContour {
public:
  CContour(double, int);
  ~CContour();
  void compute(ContourCellSet*, MasterElement*, bool);
  CurveVec *getCurves();
  CurveVec *getLoops();
%readonly
 double value;
%readwrite
};

class ContourCellSet {
public:
  ContourCoordVec *getCorners();
  void findIntercepts(DoubleList*);
};

ContourCellSet *contourCellCache(MasterElement*, int);
void clearCache();

int nContourStates, nCreated, nDeleted;	// DEBUGGING

#endif // CONTOUR_SWG
