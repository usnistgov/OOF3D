// -*- C++ -*-
// $RCSfile: skeletonfilter.swg,v $
// $Revision: 1.1.2.12 $
// $Author: langer $
// $Date: 2014/11/25 22:08:31 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SKELETONFILTER_SWG
#define SKELETONFILTER_SWG

%module skeletonfilter

%include "engine/typemaps.swg"
%extern "engine/cskeletonselectable.swg"
%extern "engine/cskeleton2.swg"

%pragma(python) include="engine/skeletonfilter.spy"

%{
#include "engine/skeletonfilter.h"
#include "engine/IO/gridsource.h"
typedef std::vector<SkeletonFilter*> SkeletonFilterVec;
%}

%typemap(python, out) SkeletonFilterVec* {
  // typemap(python, out) SkeletonFilterVec*
  SkeletonFilterVec::size_type sz = $source->size();
  assert((int) sz >= PY_SSIZE_T_MIN && (int) sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(SkeletonFilterVec::size_type i=0; i<sz; i++) {
    PyList_SET_ITEM($target, (Py_ssize_t) i, (*$source)[i]->pythonObject());
  }
}

SkeletonFilterVec *getSkeletonFilters();

class SkeletonFilter {
public:
  ~SkeletonFilter();
  void precompute(CSkeleton*);
  bool acceptable(CSkeletonSelectable*, CSkeletonBase*);
  void postcompute();
  int getCellIndex(int);
  void setModified();
  void setSource(GridSourcePtr);
};

class NullFilter: public SkeletonFilter {
public:
  NullFilter();
};

// class NodeGroupFilter: public SkeletonFilter {
// public:
//   NodeGroupFilter(char *);
// };
// 
// class SegmentGroupFilter: public SkeletonFilter {
// public:
//   SegmentGroupFilter(char *);
// };

class ElementGroupFilter: public SkeletonFilter {
public:
  ElementGroupFilter(char *);
};

class SelectedElementFilter : public SkeletonFilter {
public:
  SelectedElementFilter();
};

class MaterialFilter: public SkeletonFilter {
public:
  MaterialFilter(char *);
};

class HomogeneityFilter: public SkeletonFilter {
public:
  HomogeneityFilter(double, double);
};

class ShapeEnergyFilter: public SkeletonFilter {
public:
  ShapeEnergyFilter(double, double);
};

class ElementQualityFilter: public SkeletonFilter {
public:
  ElementQualityFilter(double, double, double);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class IntersectionFilter: public SkeletonFilter {
public:
  IntersectionFilter(SkeletonFilter*, SkeletonFilter*);
};

class UnionFilter: public SkeletonFilter {
public:
  UnionFilter(SkeletonFilter*, SkeletonFilter*);
};

class XorFilter: public SkeletonFilter {
public:
  XorFilter(SkeletonFilter*, SkeletonFilter*);
};

class NotFilter: public SkeletonFilter {
public:
  NotFilter(SkeletonFilter*);
};

#endif // SKELETONFILTER_SWG
