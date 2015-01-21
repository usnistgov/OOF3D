// -*- C++ -*-
// $RCSfile: voxelfilter.swg,v $
// $Revision: 1.1.2.4 $
// $Author: langer $
// $Date: 2012/12/26 01:33:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef VOXELFILTER_SWG
#define VOXELFILTER_SWG

%module voxelexcluder

%include "common/typemaps.swg"

%pragma(python) include="common/voxelfilter.spy"

%{
#include "common/voxelfilter.h"
typedef std::vector<VoxelFilter*> VoxelFilterVec;
%}

%typemap(python, out) VoxelFilterVec* {
  // typemap(python, out) VoxelFilterVec*
  VoxelFilterVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int) sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(VoxelFilterVec::size_type i=0; i<sz; i++) {
    PyList_SET_ITEM($target, (Py_ssize_t) i, (*$source)[i]->pythonObject());
  }
}
   
VoxelFilterVec *getVoxelFilters();

class VoxelFilter {
protected:
  OOFCanvasLayerBase *canvaslayer;
public:
  ~VoxelFilter();
  void setMicrostructure(CMicrostructure*);
  void setCanvasLayer(OOFCanvasLayerBase*);
  void setModified();
};

class AllVoxels : public VoxelFilter {
public:
  AllVoxels();
};

class ActiveVoxels : public VoxelFilter {
public:
  ActiveVoxels();
};

class SelectedVoxels : public VoxelFilter {
public:
  SelectedVoxels();
};

class VoxelIntersection : public VoxelFilter {
public:
  VoxelIntersection(VoxelFilter*, VoxelFilter*);
};

class VoxelUnion : public VoxelFilter {
public:
  VoxelUnion(VoxelFilter*, VoxelFilter*);
};

class VoxelXor : public VoxelFilter {
public:
  VoxelXor(VoxelFilter*, VoxelFilter*);
};

class VoxelNot : public VoxelFilter {
public:
  VoxelNot(VoxelFilter*);
};

class VoxelGroupFilter : public VoxelFilter {
public:
  VoxelGroupFilter(char*);
};

#endif // VOXELFILTER_SWG
