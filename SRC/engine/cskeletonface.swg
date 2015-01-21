// -*- C++ -*-
// $RCSfile: cskeletonface.swg,v $
// $Revision: 1.1.2.21 $
// $Author: langer $
// $Date: 2014/11/07 04:14:17 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONFACE_SWG
#define CSKELETONFACE_SWG

%module cskeletonface

%include "common/typemaps.swg"
%extern "engine/cskeletonselectable.swg"
%extern "common/cmicrostructure.swg"
%extern "engine/cskeletonnode2.swg"
%{
#include <oofconfig.h>
#include "common/tostring.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonselectable.h"
#include "common/IO/vtkutils.h"
%}

%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonMultiNodeSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonnode2 import CSkeletonNodePtr"
%pragma(python) code="from ooflib.SWIG.common.cmicrostructure import CMicrostructurePtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkIdListPtrPtr"

class CSkeletonFace : public CSkeletonMultiNodeSelectable {
public:
  double area();
  double areaInVoxelUnits(CMicrostructure *MS);
  double areaInFractionalUnits(CMicrostructure *MS);
  %addmethods {
    int uiIdentifier() {
      return self->getUid();
    }
  }
};

class OrientedCSkeletonFace {
public:
  VTKCellType getCellType();
  vtkIdListPtr getPointIds();
  CSkeletonFace *get_face();
  %addmethods {
    
    PyObject* get_direction_vector() {
      PyObject *tuple = PyTuple_New((Py_ssize_t) DIM);
      Coord v;
      v = self->get_direction_vector();
      for(int i=0; i<DIM; ++i)
	PyTuple_SET_ITEM(tuple, (Py_ssize_t) i, PyFloat_FromDouble(v[i]));
      return tuple;
    }

    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
  CSkeletonNode *getNode(int i);
  int nnodes();
};

long get_globalFaceCount();
long get_globalOrientedFaceCount();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// In C++, CSkeletonFaceIterator is a typemap.  These methods must be
// added here so that it can be used in PySkeletonFaceIterator, which
// acts like a real Python iterator.

class CSkeletonFaceIterator {
public:
  %addmethods {
    CSkeletonFace *dereference() {
      return (**self).second;
    }
    void increment() {
      ++*self;
    }
    bool notEqual(CSkeletonFaceIterator *other) {
      // swig 1.1 can't handle operator!=
      return *self != *other;
    }
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class OrientedSurface {
public:
  ~OrientedSurface();
  int size();
  void reverse();
  bool closed();
  double volume();
  Coord normal();
};

// orientFaces constructs a new OrientedSurface object.  Some, but not
// all, OrientedSurfaces are passed back in to C++ and stored in a
// face boundary.  The ones that aren't stored in C++ need to be
// deleted by Python, so orientFaces is declared with %new here, which
// sets thisown=1.  The ones that are passed back into C++ to be
// stored in a boundary need to *not* be deleted by Python, so the
// takeOwnership typemap sets thisown=0.

%new OrientedSurface *orientFaces(CSkeletonBase*, CSkeletonFaceVector*,
				  OrientedCSkeletonFace*);

%typemap(python, in) OrientedSurface *takeOwnership {
  // typemap(python, in) OrientedSurface *takeOwnership
  if($source) {
    if($source == Py_None) {
      $target = NULL;
    }
    else {
      PyObject *pyZero = PyInt_FromLong(0);
      if(SWIG_GetPtrObj($source, (void**) &$target, "_OrientedSurface_p")) {
	PyErr_SetString(PyExc_TypeError,
			"Type error.  Expected _OrientedSurface_p.");
	return NULL;
      }
      PyObject_SetAttrString($source, "thisown", pyZero);
    }
  }
}

#endif	// CSKELETONFACE_SWG
