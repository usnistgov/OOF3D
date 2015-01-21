// -*- C++ -*-
// $RCSfile: cmicrostructure.swg,v $
// $Revision: 1.35.8.14 $
// $Author: langer $
// $Date: 2014/09/27 22:33:48 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CMICROSTRUCTURE_SWG
#define CMICROSTRUCTURE_SWG

%module cmicrostructure

%{
#include <oofconfig.h>
#include "common/cmicrostructure.h"
#include "common/array.h"
typedef Array<int> ArrayInt;
%}

%pragma(python) include="cmicrostructure.spy"

%include "common/typemaps.swg"

%extern "common/pixelgroup.swg"
%pragma(python) code="from ooflib.SWIG.common.pixelgroup import PixelGroupPtr"

// %extern "common/timestamp.swg"
// %pragma(python) code="from ooflib.SWIG.common.timestamp import TimeStampPtr"


%typemap(python, out) ArrayInt* {
  int h = $source->height();
  int w = $source->width();
  assert(h >= PY_SSIZE_T_MIN && h <= PY_SSIZE_T_MAX);
  assert(w >= PY_SSIZE_T_MIN && w <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) h);
#ifndef DIM_3
  for(int j=0; j<h; j++) {
    PyObject *row = PyList_New((Py_ssize_t) w);
    PyList_SET_ITEM($target, (Py_ssize_t) j, row);
    for(int i=0; i<w; i++) {
      PyList_SET_ITEM(row, (Py_ssize_t) i,
		      PyInt_FromLong((*$source)[ICoord(i,j)]));
    }
  }
#else
  int d = $source->depth();
  assert(d >= PY_SSIZE_T_MIN && d <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) h);
  for(int k=0; k<h; k++) {
    PyObject *slice = PyList_New((Py_ssize_t) w);
    PyList_SET_ITEM($target, (Py_ssize_t) k, slice);
		for(int j=0; j<w; j++) {
			PyObject *row = PyList_New((Py_ssize_t) d);
			PyList_SET_ITEM(slice, (Py_ssize_t) j, row);
			for(int i=0; i<d; i++) {
			  PyList_SET_ITEM(row, (Py_ssize_t) i, PyInt_FromLong((*$source)[ICoord(j,k,i)]));
			}
		}
	}
#endif
}

%typemap(python,ignore) bool *newness (bool tmp) {
  $target = &tmp;
}

%typemap(python,argout) bool *newness {
  PyObject *res;
  if (*$source) 
    res = Py_True;
  else
    res = Py_False;

  if (!PyList_Check($target)) {
    PyObject *retval = $target;
    $target = PyList_New((Py_ssize_t) 0);
    PyList_Append($target,retval);
    Py_XDECREF(retval);
  }
  PyList_Append($target, res);
}

%extern "common/coord.swg"


//For SnapRefine.
%typemap(python,ignore) int *cskel_edgecat (int tmp) {
  $target = &tmp;
}

%typemap(python,argout) int *cskel_edgecat {
  PyObject *res=PyInt_FromLong(*$source);
  if (!PyList_Check($target)) {
    PyObject *retval = $target;
    $target = PyList_New((Py_ssize_t) 0);
    PyList_Append($target,retval);
    Py_XDECREF(retval);
  }
  PyList_Append($target, res);
  Py_XDECREF(res);
}

class CMicrostructure {
public:
  CMicrostructure(char *name, ICoord *Sequence, Coord *Sequence);
  ~CMicrostructure();
  void destroy(); 
  const string &name();
  void rename(char *name);
  Coord size();
  ICoord sizeInPixels();
  Coord sizeOfPixels();
#ifndef DIM_3
  double areaOfPixels();
#else
  double volumeOfPixels();
#endif
  ICoord pixelFromPoint(Coord Point);
  // TimeStamp &getTimeStamp();
  void setCurrentActiveArea(ActiveArea*);
  int nGroups();
  // getGroup is further wrapped in cmicrostructure.spy.
  PixelGroup *getGroup(char *name, 
		       bool *newness); //creates new group if necessary
  PixelGroup *findGroup(char *name); // never creates a new group
  void removeGroup(char *name);
  %new StringVec *groupNames() const;
  void setPixelSelection(CPixelSelection*);
  bool isSelected(ICoord*);
  int nCategories();
  int category(ICoord *iPoint);
  void recategorize();
  bool is_categorized();
  ArrayInt *getCategoryMap();
  %new ArrayInt *getCategoryMapRO();
  //ICoord getRepresentativePixel(int category);
//   bool transitionPointWithPoints(Coord *Point, Coord *Point,
// 				 Coord *cskel_OutPoint);
  double edgeHomogeneity(Coord Point, Coord Point);
  double edgeHomogeneityCat(Coord Point, Coord Point,
			    int* cskel_edgecat);
//   bool transitionPointWithPoints_unbiased(Coord *Point, Coord *Point,
// 				 Coord *cskel_OutPoint);

};

long get_globalMicrostructureCount();

//For SnapRefine.
%typemap(python, argout) int *cskel_edgecat {}
%typemap(python, ignore) int *cskel_edgecat {}

#endif // CMICROSTRUCTURE_SWG
