// -*- C++ -*-
// $RCSfile: cskeletonnode2.swg,v $
// $Revision: 1.1.2.25 $
// $Author: langer $
// $Date: 2014/12/14 01:07:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


// TODO OPT: remove functions that are not called from Python!

#ifndef CSKELETONNODE2_SWG
#define CSKELETONNODE2_SWG

%module cskeletonnode

%include "engine/typemaps.swg"
%extern "engine/cskeletonselectable.swg"
%extern "engine/cskeletonelement.swg"
%{
#include <oofconfig.h>
#include "common/tostring.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonselectable_i.h"
#include "engine/cskeletonelement.h"
%}

%pragma(python) include="engine/cskeletonnode2.spy"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CAbstractTrackerPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonelement import CSkeletonElementPtr"

// %typemap(python, out) CPinnedNodeTracker* {
//    $target = $source->pythonObject();
// }

class CSkeletonNode : public CSkeletonSelectable {
public:
  int getIndex();
  bool movable_x();
  bool movable_y();
  bool movable_z();
  bool pinned();
  void pin(CPinnedNodeTrackerVector *cvector,
	   CPinnedNodeTrackerVector *pvector);
  void unpin(CPinnedNodeTrackerVector *cvector,
	     CPinnedNodeTrackerVector *pvector);
  bool movable();
  bool moveTo(double doubleDIMArray[3]);
  void moveBack();
  bool illegal();
  CSkeletonElement *getElement(int i);
  CSkeletonElementVector *getElements();
  %name(position) Coord getPosition();

  // TODO MER: Why are these methods static?  They probably don't belong
  // here.  Move them to CSkeleton, perhaps?
  static void pinSelection(CSelectionTrackerBase *tracker, 
			   CPinnedNodeTrackerVector *cvector,
			   CPinnedNodeTrackerVector *pvector);
  static void unpinSelection(CSelectionTrackerBase *tracker, 
			     CPinnedNodeTrackerVector *cvector,
			     CPinnedNodeTrackerVector *pvector);
  static void pinSelectedSegments(CSelectionTrackerBase *tracker,
				  CPinnedNodeTrackerVector *cvector,
				  CPinnedNodeTrackerVector *pvector);
  static void pinSelectedElements(CSelectionTrackerBase *tracker,
				  CSkeletonBase *skel,
				  bool internal, bool boundary,
				  CPinnedNodeTrackerVector *cvector,
				  CPinnedNodeTrackerVector *pvector);
  static void pinInternalBoundaryNodes(CSkeletonBase *skel,
				       CPinnedNodeTrackerVector *cvector, 
				       CPinnedNodeTrackerVector *pvector);

  int dominantPixel(CMicrostructure*);

  %addmethods {
    int uiIdentifier() {
      return self->getIndex();
    }
    %new string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

class CPinnedNodeTracker : public CAbstractTracker {
 public:
  CPinnedNodeTracker(CSkeletonBase *s);
  CPinnedNodeTracker* clone();
  CSkeletonNodeSet* get();
  int size();
  CPinnedNodeTracker* sheriff();
  void write();
  void clear();
  void clearskeleton();
  void implied_pin(CPinnedNodeTracker *other);
  CSkeletonBase *getSkeleton();
};

class CDeputyPinnedNodeTracker : public CPinnedNodeTracker {
 public:
  CDeputyPinnedNodeTracker(CSkeletonBase *s);
  void implied_pin(CPinnedNodeTracker *other);
};

long get_globalNodeCount();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// In C++, CSkeletonNodeIterator is a typemap.  These methods must be
// added here so that it can be used in PySkeletonNodeIterator, which
// acts like a real Python iterator.

class CSkeletonNodeIterator {
public:
  %addmethods {
    CSkeletonNode *dereference() {
      return **self;
    }
    void increment() {
      ++*self;
    }
    bool notEqual(CSkeletonNodeIterator *other) {
      return *self != *other;
    }
  }
};

#endif // CSKELETONNODE2_SWG

