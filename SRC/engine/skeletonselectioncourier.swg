// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SKELETONSELECTIONCOURIER_SWG
#define SKELETONSELECTIONCOURIER_SWG

%module skeletonselectioncourier

%include "engine/typemaps.swg"

%{
  #include <oofconfig.h>
  #include "engine/cskeletongroups.h"
  #include "engine/skeletonselectioncourier.h"
%}

class SkeletonSelectionCourier {
public:
  ~SkeletonSelectionCourier();
  void select();
  void deselect();
  void toggle();
};

class SingleObjectCourier : public SkeletonSelectionCourier {
public:
  SingleObjectCourier(CSkeletonBase*, CSkeletonSelectable*,
		      CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class StupidCourier : public SkeletonSelectionCourier {
public:
  StupidCourier(CSkeletonBase*, CSkeletonSelectableVector*,
		CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class SkeletonGroupCourier : public SkeletonSelectionCourier {
public:
  SkeletonGroupCourier(CSkeletonBase*, char*, CGroupTrackerBase*,
		       CSelectionTrackerVector*, CSelectionTrackerVector*);
};

//---------

class AllNodesCourier : public SkeletonSelectionCourier {
public:
  AllNodesCourier(CSkeletonBase*, CSelectionTrackerVector*,
		  CSelectionTrackerVector*);
};

class AllSegmentsCourier : public SkeletonSelectionCourier {
public:
  AllSegmentsCourier(CSkeletonBase*, CSelectionTrackerVector*,
		     CSelectionTrackerVector*);
};

class AllFacesCourier : public SkeletonSelectionCourier {
public:
  AllFacesCourier(CSkeletonBase*, CSelectionTrackerVector*,
		  CSelectionTrackerVector*);
};

class AllElementsCourier : public SkeletonSelectionCourier {
public:
  AllElementsCourier(CSkeletonBase*, CSelectionTrackerVector*,
		  CSelectionTrackerVector*);
};

//-----------

class NodesFromElementsCourier : public SkeletonSelectionCourier {
public:
  NodesFromElementsCourier(CSkeletonBase*,
			   std::string *enum2string,
			   CSelectionTracker*,
			   CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class NodesFromFacesCourier : public SkeletonSelectionCourier {
public:
  NodesFromFacesCourier(CSkeletonBase*,
			std::string *enum2string,
			CSelectionTracker*,
			CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class NodesFromSegmentsCourier : public SkeletonSelectionCourier {
public:
  NodesFromSegmentsCourier(CSkeletonBase*,
			   CSelectionTracker*,
			   CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class PointBoundaryCourier : public SkeletonSelectionCourier {
public:
  PointBoundaryCourier(CSkeletonBase*, CSkeletonPointBoundary*,
		       CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class InternalBoundaryNodesCourier : public SkeletonSelectionCourier {
public:
  InternalBoundaryNodesCourier(CSkeletonBase*,
			       CSelectionTrackerVector*,
			       CSelectionTrackerVector*);
};

class ExpandNodeSelectionCourier : public SkeletonSelectionCourier {
public:
  ExpandNodeSelectionCourier(
		     CSkeletonBase*, CSelectionTracker*,
		     CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class SegmentsFromElementsCourier : public SkeletonSelectionCourier {
public:
  SegmentsFromElementsCourier(
		      CSkeletonBase*, std::string *enum2string,
		      CSelectionTracker*,
		      CSelectionTrackerVector*, CSelectionTrackerVector*);
};
  
class SegmentsFromFacesCourier : public SkeletonSelectionCourier {
public:
  SegmentsFromFacesCourier(
		      CSkeletonBase*, std::string *enum2string,
		      CSelectionTracker*,
		      CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class SegmentsFromNodesCourier : public SkeletonSelectionCourier {
public:
  SegmentsFromNodesCourier(
		   CSkeletonBase*, bool, bool,
		   CSelectionTracker*,
		   CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class EdgeBoundaryCourier : public SkeletonSelectionCourier {
public:
  EdgeBoundaryCourier(CSkeletonBase*, CSkeletonEdgeBoundary*,
		      CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class InternalBoundarySegmentsCourier : public SkeletonSelectionCourier {
public:
  InternalBoundarySegmentsCourier(
			  CSkeletonBase*,
			  CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class InhomogeneousSegmentCourier : public SkeletonSelectionCourier {
public:
  InhomogeneousSegmentCourier(CSkeletonBase*, double,
			    CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class RandomSegmentCourier : public SkeletonSelectionCourier {
public:
  RandomSegmentCourier(CSkeletonBase*, double,
		       CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class CategoryElementCourier : public SkeletonSelectionCourier {
public:
  CategoryElementCourier(CSkeletonBase*, int,
			 CSelectionTrackerVector*, CSelectionTrackerVector*);
};

#endif // SKELETONSELECTIONCOURIER_SWG
