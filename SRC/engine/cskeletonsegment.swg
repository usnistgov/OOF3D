// -*- C++ -*-
// $RCSfile: cskeletonsegment.swg,v $
// $Revision: 1.1.2.23 $
// $Author: langer $
// $Date: 2013/12/06 20:05:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONSEGMENT_SWG
#define CSKELETONSEGMENT_SWG

%module cskeletonsegment

%include "engine/typemaps.swg"
%extern "engine/cskeletonselectable.swg"
%extern "common/cmicrostructure.swg"
%extern "engine/cskeletonnode2.swg"
%{
#include <oofconfig.h>
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonsegment.h"
#include "engine/cskeletonselectable.h"
#include "common/tostring.h"
#include "common/IO/vtkutils.h"
%}

%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonMultiNodeSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonnode2 import CSkeletonNodePtr"
%pragma(python) code="from ooflib.SWIG.common.cmicrostructure import CMicrostructurePtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkIdListPtrPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonelement import CSkeletonElementPtr"

class CSkeletonSegment : public CSkeletonMultiNodeSelectable {
public:
  double length();
  double lengthInVoxelUnits(CMicrostructure *MS);
  double lengthInFractionalUnits(CMicrostructure *MS);
  double homogeneity(CMicrostructure*);
  int dominantPixel(CMicrostructure*);
  %addmethods {
    int uiIdentifier() { 
      return self->getUid();
    }
    %new string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
  CSkeletonNode *get_other_node(CSkeletonNode*);
  const CSkeletonElement *getElement(CSkeletonBase*, int);
};

class OrientedCSkeletonSegment {
public:
  VTKCellType getCellType();
  vtkIdListPtr getPointIds();

  %addmethods {
    
    PyObject* get_direction_vector() {
      PyObject *tuple = PyTuple_New((Py_ssize_t) DIM);
      Coord v;
      v = self->get_direction_vector();
      for(int i=0; i<DIM; ++i)
	PyTuple_SET_ITEM(tuple, (Py_ssize_t) i, PyFloat_FromDouble(v[i]));
      return tuple;
    }
  }
  CSkeletonSegment *get_segment();
  CSkeletonNode *getNode(int i);
  // %addmethods {
  //   static bool segSequence(CSkeletonSelectableList *seglist) {
  //     CSkeletonSegmentVector segs;
  //     CSkeletonNodeVector nodes;
  //     return OrientedCSkeletonSegment::segSequence(seglist, NULL, segs, nodes);
  //   }
  // }
};

class SegmentSequence {
public:
  bool closed();
  void reverse();
  Coord span();
  double projectedArea(char*);
};

// %typemap(python, ignore) CSkeletonNode *ignore {
//   // typemap(python, ignore) CSkeletonNode *ignore
//   $target = 0;
// }

%new SegmentSequence *sequenceSegments(CSkeletonSegmentVector*,
				       CSkeletonNode*);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// In C++, CSkeletonSegmentIterator is a typemap.  These methods must
// be added here so that it can be used in PySkeletonSegmentIterator,
// which acts like a real Python iterator.

class CSkeletonSegmentIterator {
public:
  %addmethods {
    CSkeletonSegment *dereference() {
      return (**self).second;
    }
    void increment() {
      ++*self;
    }
    bool notEqual(CSkeletonSegmentIterator *other) {
      // swig 1.1 can't handle operator!=
      return *self != *other;
    }
  }
};

#endif	// CSKELETONSEGMENT_SWG


