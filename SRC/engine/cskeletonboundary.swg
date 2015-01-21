// -*- C++ -*-
// $RCSfile: cskeletonboundary.swg,v $
// $Revision: 1.1.2.22 $
// $Author: langer $
// $Date: 2014/01/18 04:41:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


#ifndef CSKELETONBOUNDARY_SWG
#define CSKELETONBOUNDARY_SWG

%module cskeletonboundary

%include "common/typemaps.swg"
%include "engine/typemaps.swg"
%{
#include <oofconfig.h>
#include "engine/cskeletonboundary.h"
%}
%extern "engine/cskeletonselectable.swg"

%pragma(python) include="engine/cskeletonboundary.spy"

// %typemap(python, out) CSkeletonBoundary* {
//    $target = $source->pythonObject();
//    PyObject_SetAttrString($target, "thisown",  PyInt_FromLong(1));
// }

class CSkeletonBoundary {
public:
  const string &get_name();
  int size();
  void remove();
}; 

class CSkeletonPointBoundary : public CSkeletonBoundary {
public:
  CSkeletonPointBoundary(char *name);
  CSkeletonNodeSet *getNodes();
  void addNode(CSkeletonNode *n);
  void appendNodes(CSkeletonNodeVector*);
  void removeNodes(CSkeletonNodeVector*);
  bool hasNode(CSkeletonNode*);
  CSkeletonPointBoundary *map(CSkeleton *new_skeleton, SkeletonMapDir direction,
			      bool exterior);
};

class ExteriorCSkeletonPointBoundary : public CSkeletonPointBoundary {
public:
  ExteriorCSkeletonPointBoundary(char *name);
};


class CSkeletonEdgeBoundary : public CSkeletonBoundary {
public:
  CSkeletonEdgeBoundary(char *name);
  OrientedCSkeletonSegmentVector *getSegments();
  OrientedCSkeletonSegmentVector *getOrientedSegments();
  CSkeletonSegmentVector *getUnorientedSegments();
  bool try_appendSegs(CSkeletonSegmentVector*);
  bool try_removeSegs(CSkeletonSegmentVector*);
  void appendSegs(CSkeletonSegmentVector*);
  void removeSegs(CSkeletonSegmentVector*);
  void reverse();
  double length();
  //void append(CSkeletonNodeVector *ns);
  CSkeletonEdgeBoundary *map(CSkeleton *new_skeleton, SkeletonMapDir direction,
			     bool exterior);
  bool hasSegment(CSkeletonSegment*);
  %new CSkeletonNodeVector *getNodes();
};

class ExteriorCSkeletonEdgeBoundary : public CSkeletonEdgeBoundary {
public:
  ExteriorCSkeletonEdgeBoundary(char *name);
};


class CSkeletonFaceBoundary : public CSkeletonBoundary {
public:
  CSkeletonFaceBoundary(char *name);
  OrientedCSkeletonFaceSet *getFaces();
  bool try_appendFaces(CSkeletonBase*, CSkeletonFaceVector*);
  bool try_removeFaces(CSkeletonBase*, CSkeletonFaceVector*);
  void appendFaces(CSkeletonBase*, CSkeletonFaceVector*);
  void removeFaces(CSkeletonBase*, CSkeletonFaceVector*);
  CSkeletonFaceBoundary *map(CSkeleton *new_skeleton, SkeletonMapDir direction,
			     bool exterior);
  void reverse();
  double area();
  bool hasFace(CSkeletonFace*);
};

class ExteriorCSkeletonFaceBoundary : public CSkeletonFaceBoundary {
public:
  ExteriorCSkeletonFaceBoundary(char *name);
};

#endif

