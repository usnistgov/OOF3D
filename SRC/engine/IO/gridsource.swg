// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GRIDSOURCE_SWG
#define GRIDSOURCE_SWG

%module gridsource

%include "engine/typemaps.swg"

%extern "common/IO/gridsourcebase.swg"
%pragma(python) code="from ooflib.SWIG.common.IO.gridsourcebase import GridSourcePtrPtr"

%{
#include "engine/cskeleton2.h"
#include "engine/femesh.h"
#include "engine/IO/gridsource.h"
#include <vtkSmartPointer.h>
%}

// This is a bit of a hack.  SkeletonGridSourcePtr is not derived from
// GridSourcePtr in C++, but swig doesn't need to know that.  The
// XXXPtr objects swigged here are typedef'd vtkSmartPointers, defined
// in gridsource.h.

// Inconsistent capitalization is due to bad interaction of vtk and
// oof naming conventions.


class SkeletonGridSourcePtr : public GridSourcePtr {
public:
  ~SkeletonGridSourcePtr();
  // See comment in gridsource.h about why filter isn't in the base
  // class.
  %addmethods {
    void setSkeleton(CSkeletonBase *skel) {
      (*self)->Setskeleton(skel);
    }
    void setFilter(SkeletonFilter *f) {
      (*self)->SetFilter(f);
    }
  }
};

class MeshGridSourcePtr : public GridSourcePtr {
public:
  ~MeshGridSourcePtr();
  %addmethods {
    void setSkeleton(CSkeletonBase *skel) {
      (*self)->Setskeleton(skel);
    }
    void setMesh(FEMesh *f) {
      (*self)->Setmesh(f);
    }
    void setEnhancement(double e) {
      (*self)->SetEnhancement(e);
    }
    void setFilter(SkeletonFilter *f) {
      (*self)->SetFilter(f);
    }
    void setTime(double t) {
      (*self)->Settime(t);
    }
  }
};

SkeletonGridSourcePtr newSkeletonGridSource();
MeshGridSourcePtr newMeshGridSource();

#ifdef DEBUG

class SkeletonSegmentGridSourcePtr : public GridSourcePtr {
public:
  ~SkeletonSegmentGridSourcePtr();
  %addmethods {
    void setSkeleton(CSkeletonBase *skel) {
      (*self)->Setskeleton(skel);
    }
    void setFilter(SkeletonFilter *f) {
      (*self)->SetFilter(f);
    }
  }
};
  
SkeletonSegmentGridSourcePtr newSkeletonSegmentGridSource();

class SkeletonEdgeDiffGridSourcePtr : public GridSourcePtr {
public:
  ~SkeletonEdgeDiffGridSourcePtr();
  %addmethods {
    void setSkeleton(CSkeletonBase *skel) {
      (*self)->Setskeleton(skel);
    }
    void setOther(CSkeletonBase *other) {
      (*self)->Setother(other);
    }
    void setFilter(SkeletonFilter*f) {
      // This is a hack
    }
  }
};

SkeletonEdgeDiffGridSourcePtr newSkeletonEdgeDiffGridSource();

#endif // DEBUG

#endif // GRIDSOURCE_SWG
