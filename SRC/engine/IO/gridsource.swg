// -*- C++ -*-
// $RCSfile: gridsource.swg,v $
// $Revision: 1.1.2.7 $
// $Author: langer $
// $Date: 2014/03/14 21:14:43 $

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
// GridSourcePtr in C++, but swig doesn't need to know that.

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

#endif // GRIDSOURCE_SWG
