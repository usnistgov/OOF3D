// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SKELETONSELECTIONCOURIER_H
#define SKELETONSELECTIONCOURIER_H

#include <oofconfig.h>
#include "engine/cskeletonselectable_i.h"

class CSkeletonBase;
class CGroupTrackerBase;
class PixelGroup;
class Material;

class SkeletonSelectionCourier {
protected:
  const CSkeletonBase *skeleton;
  CSelectionTrackerVector clist, plist; // Trackers for the selection
  bool done_;
public:
  SkeletonSelectionCourier(const CSkeletonBase*, CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
  virtual ~SkeletonSelectionCourier() {}

  // The PixelSelectionCouriers don't provide select, unselect, etc.
  // But the Skeleton selections are stored in a more distributed way
  // with trackers and all, so it's easier if the selection methods
  // are actually provided by the couriers.
  void select();
  void deselect();
  void toggle();

protected:
  virtual void start() = 0;
  virtual CSkeletonSelectable *currentObj() const = 0;
  virtual void next() = 0;
  virtual bool done() const { return done_; }

  friend class IntersectionCourier;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Generic couriers that work with any type of selectable skeleton
// component.

class SingleObjectCourier : public SkeletonSelectionCourier {
private:
  CSkeletonSelectable *object;
public:
  SingleObjectCourier(const CSkeletonBase*,
		      CSkeletonSelectable*,
		      CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual void start() { done_ = false; }
  virtual CSkeletonSelectable *currentObj() const { return object; }
  virtual void next() { done_ = true; }
};

// BulkSkelSelCourier is a base class for any courier that can
// compute and store all of the objects that it will iterate over in
// its constructor.  TYPE should be CSkeletonSelectableSet,
// CSkeletonNodeVector, or some such.

template <class TYPE>
class BulkSkelSelCourier : public SkeletonSelectionCourier {
protected:
  TYPE selectedObjects;
  typename TYPE::iterator iter;
public:
  BulkSkelSelCourier(const CSkeletonBase *skel, CSelectionTrackerVector *clist,
		      CSelectionTrackerVector *plist)
    : SkeletonSelectionCourier(skel, clist, plist)
  {}
  virtual void start() {
    iter = selectedObjects.begin();
    done_ = (iter == selectedObjects.end()); 
  }
  virtual CSkeletonSelectable *currentObj() const {
    return *iter;
  }
  virtual void next() {
    ++iter;
    done_ = (iter == selectedObjects.end());
  }
  
};

// StupidCourier just carries in a list of objects.  It's stupid
// because transmitting a list of objects from Python to C++ is what
// the courier classes are meant to avoid.

class StupidCourier : public BulkSkelSelCourier<CSkeletonSelectableVector> {
public:
  StupidCourier(const CSkeletonBase*,
		CSkeletonSelectableVector*,
		CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class SkeletonGroupCourier : public SkeletonSelectionCourier {
private:
  const CGroupTrackerBase *groupTracker;
  const std::string groupName;
  CSkeletonSelectableSet *group;
  CSkeletonSelectableSet::iterator iter;
protected:
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
public:
  SkeletonGroupCourier(const CSkeletonBase*,
		       const std::string&,
		       const CGroupTrackerBase*,
		       CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class IntersectionCourier : public SkeletonSelectionCourier {
private:
  void advance();
  CSkeletonSelectableSet oldSelection;
  CSkeletonSelectableSet courierObjs;
  CSkeletonSelectableSet::iterator oldSelIter;
  CSkeletonSelectableSet::iterator courierIter;
public:
  IntersectionCourier(CSelectionTracker*, SkeletonSelectionCourier*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *courierIter; }
  virtual void next();
  virtual bool done() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Node selection couriers

class AllNodesCourier : public SkeletonSelectionCourier {
private:
  CSkeletonNodeIterator iter;
public:
  AllNodesCourier(const CSkeletonBase*,
		  CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
};


// Intermediate base class for selecting Nodes from other kinds of
// selections.

class NodesFromOtherCourier : public BulkSkelSelCourier<CSkeletonNodeSet> {
protected:
  virtual CSkeletonNodeSet exteriorNodes() const = 0;
  CSkeletonNodeSet allNodes() const;
  std::string coverage;
  const CSelectionTracker *otherTracker;
public:
  NodesFromOtherCourier(const CSkeletonBase*,
			const std::string*, // coverage
			const CSelectionTracker*,
			CSelectionTrackerVector*,
			CSelectionTrackerVector*);
  virtual void start();
  ~NodesFromOtherCourier() {}
};

class NodesFromElementsCourier : public NodesFromOtherCourier {
private:
  virtual CSkeletonNodeSet exteriorNodes() const;
public:
  NodesFromElementsCourier(const CSkeletonBase*,
			   const std::string*,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};

class NodesFromFacesCourier : public NodesFromOtherCourier {
private:
  virtual CSkeletonNodeSet exteriorNodes() const;
public:
  NodesFromFacesCourier(const CSkeletonBase*,
			const std::string*,
			const CSelectionTracker*,
			CSelectionTrackerVector*,
			CSelectionTrackerVector*);
};

class NodesFromSegmentsCourier : public BulkSkelSelCourier<CSkeletonNodeSet> {
public:
  NodesFromSegmentsCourier(const CSkeletonBase*,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};


class InternalBoundaryNodesCourier
  : public BulkSkelSelCourier<CSkeletonNodeSet> {
public:
  InternalBoundaryNodesCourier(const CSkeletonBase*,
			       CSelectionTrackerVector*,
			       CSelectionTrackerVector*);
};

class PointBoundaryCourier : public SkeletonSelectionCourier {
private:
  const CSkeletonNodeSet *nodes;
  CSkeletonNodeSet::iterator iter;
public:
  PointBoundaryCourier(const CSkeletonBase*,
		       const CSkeletonPointBoundary*,
		       CSelectionTrackerVector*,
		       CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
};

class ExpandNodeSelectionCourier : BulkSkelSelCourier<CSkeletonNodeSet> {
public:
  ExpandNodeSelectionCourier(const CSkeletonBase*,
			     const CSelectionTracker*,
			     CSelectionTrackerVector*,
			     CSelectionTrackerVector*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Segment selection couriers

class AllSegmentsCourier : public SkeletonSelectionCourier {
private:
  CSkeletonSegmentIterator iter;
public:
  AllSegmentsCourier(const CSkeletonBase*,
		     CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return (*iter).second; }
  virtual void next();
};

class SegmentsFromOtherCourier
  : public BulkSkelSelCourier<CSkeletonSegmentSet>
{
protected:
  virtual CSkeletonSegmentSet exteriorSegments() const = 0;
  virtual CSkeletonSegmentSet allSegments() const = 0;
  std::string coverage;
  const CSelectionTracker *otherTracker;
public:
  SegmentsFromOtherCourier(const CSkeletonBase*,
			   const std::string*, // coverage
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
  virtual void start();
  ~SegmentsFromOtherCourier() {}
};

class SegmentsFromElementsCourier : public SegmentsFromOtherCourier {
private:
  virtual CSkeletonSegmentSet exteriorSegments() const;
  virtual CSkeletonSegmentSet allSegments() const;
public:
  SegmentsFromElementsCourier(const CSkeletonBase*,
			      const std::string*, // coverage
			      const CSelectionTracker*,
			      CSelectionTrackerVector*,
			      CSelectionTrackerVector*);
};

class SegmentsFromFacesCourier : public SegmentsFromOtherCourier {
private:
  virtual CSkeletonSegmentSet exteriorSegments() const;
  virtual CSkeletonSegmentSet allSegments() const;
public:
  SegmentsFromFacesCourier(const CSkeletonBase*,
			   const std::string*, // coverage
			   const CSelectionTracker*, // selected faces
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};

class SegmentsFromNodesCourier : public BulkSkelSelCourier<CSkeletonSegmentSet>
{
public:
  SegmentsFromNodesCourier(const CSkeletonBase*,
			   bool, bool,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};

class InternalBoundarySegmentsCourier
  : public BulkSkelSelCourier<CSkeletonSegmentSet>
{
public:
  InternalBoundarySegmentsCourier(const CSkeletonBase*,
				  CSelectionTrackerVector*,
				  CSelectionTrackerVector*);
};

class EdgeBoundaryCourier : public SkeletonSelectionCourier {
private:
  const CSkeletonSegmentVector *segments;
  CSkeletonSegmentVector::const_iterator iter;
public:
  EdgeBoundaryCourier(const CSkeletonBase*,
		      const CSkeletonEdgeBoundary*,
		      CSelectionTrackerVector*,
		      CSelectionTrackerVector*);
  ~EdgeBoundaryCourier();
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
};

class SegmentHomogeneityCourier
  : public BulkSkelSelCourier<CSkeletonSegmentSet>
{
public:
  SegmentHomogeneityCourier(const CSkeletonBase*, double, double,
			    CSelectionTrackerVector*,
			    CSelectionTrackerVector*);
};

class RandomSegmentCourier : public SkeletonSelectionCourier {
private:
  CSkeletonSegmentIterator iter;
  const double probability;
  void advance();
public:
  RandomSegmentCourier(const CSkeletonBase*, double,
		       CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return (*iter).second; }
  virtual void next();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Face selection couriers

class AllFacesCourier : public SkeletonSelectionCourier {
private:
  CSkeletonFaceIterator iter;
public:
  AllFacesCourier(const CSkeletonBase*,
		  CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return (*iter).second; }
  virtual void next();
};

class FacesFromElementsCourier : public BulkSkelSelCourier<CSkeletonFaceSet> {
protected:
  CSkeletonFaceSet allFaces(const CSelectionTracker*) const;
  CSkeletonFaceSet exteriorFaces(const CSelectionTracker*) const;
public:
  FacesFromElementsCourier(const CSkeletonBase*,
			   const std::string*,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};

class FacesFromNodesCourier : public BulkSkelSelCourier<CSkeletonFaceSet> {
public:
  FacesFromNodesCourier(const CSkeletonBase*,
			int,
			const CSelectionTracker*,
			CSelectionTrackerVector*,
			CSelectionTrackerVector*);
};

class FacesFromSegmentsCourier : public BulkSkelSelCourier<CSkeletonFaceSet> {
public:
  FacesFromSegmentsCourier(const CSkeletonBase*,
			   int,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};

class FaceBoundaryCourier : public SkeletonSelectionCourier {
private:
  const CSkeletonFaceVector *faces;
  CSkeletonFaceVector::const_iterator iter;
public:
  FaceBoundaryCourier(const CSkeletonBase*,
		      const CSkeletonFaceBoundary*,
		      CSelectionTrackerVector*,
		      CSelectionTrackerVector*);
  ~FaceBoundaryCourier();
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
};

class InternalBoundaryFacesCourier : public BulkSkelSelCourier<CSkeletonFaceSet>
{
public:
  InternalBoundaryFacesCourier(const CSkeletonBase*,
			       CSelectionTrackerVector*,
			       CSelectionTrackerVector*);
};
  
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Element selection couriers

class AllElementsCourier : public SkeletonSelectionCourier {
private:
  CSkeletonElementIterator iter;
public:
  AllElementsCourier(const CSkeletonBase*,
		  CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
};

// ConditionalElementCourier is an intermediate base class for looping
// over elements that meet a simply stated criterion.

class ConditionalElementCourier : public SkeletonSelectionCourier {
private:
  CSkeletonElementIterator iter;
  void advance();
protected:
  virtual bool includeElement(const CSkeletonElement*) const = 0;
public:
  ConditionalElementCourier(const CSkeletonBase*,
			    CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
};

// CategoryElementCourier selects all elements of a given category.

class CategoryElementCourier : public ConditionalElementCourier {
private:
  int category;
public:
  CategoryElementCourier(const CSkeletonBase*, int,
			 CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class MaterialElementCourier : public ConditionalElementCourier {
private:
  const Material *material;
public:
  MaterialElementCourier(const CSkeletonBase*, const Material*,
			 CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class NoMaterialElementCourier : public ConditionalElementCourier {
public:
  NoMaterialElementCourier(const CSkeletonBase*,
			   CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class AnyMaterialElementCourier : public ConditionalElementCourier {
public:
  AnyMaterialElementCourier(const CSkeletonBase*,
			    CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class ElementHomogeneityCourier : public ConditionalElementCourier {
private:
  double min_homogeneity, max_homogeneity;
public:
  ElementHomogeneityCourier(const CSkeletonBase*, double, double,
			    CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class ElementShapeEnergyCourier : public ConditionalElementCourier {
private:
  double min_energy, max_energy;
public:
  ElementShapeEnergyCourier(const CSkeletonBase*, double, double,
			    CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class IllegalElementCourier : public ConditionalElementCourier {
public:
  IllegalElementCourier(const CSkeletonBase*,
			CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class SuspectElementCourier : public ConditionalElementCourier {
public:
  SuspectElementCourier(const CSkeletonBase*,
			CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

class ElementsFromNodesCourier
  : public BulkSkelSelCourier<CSkeletonElementSet>
{
public:
  ElementsFromNodesCourier(const CSkeletonBase*, int,
			  const CSelectionTracker*,
			  CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class ElementsFromSegmentsCourier
  : public BulkSkelSelCourier<CSkeletonElementSet>
{
public:
  ElementsFromSegmentsCourier(const CSkeletonBase*, int,
			  const CSelectionTracker*,
			  CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class ElementsFromFacesCourier
  : public BulkSkelSelCourier<CSkeletonElementSet>
{
public:
  ElementsFromFacesCourier(const CSkeletonBase*, int,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*, CSelectionTrackerVector*);
};

class ExpandElementSelectionCourier
  : public BulkSkelSelCourier<CSkeletonElementSet>
{
public:
  ExpandElementSelectionCourier(const CSkeletonBase*,
				std::string*,
				const CSelectionTracker*,
				CSelectionTrackerVector*,
				CSelectionTrackerVector*);
};

class PixelGroupCourier : public ConditionalElementCourier {
private:
  const PixelGroup *group;
public:
  PixelGroupCourier(const CSkeletonBase*, const PixelGroup*,
		    CSelectionTrackerVector*, CSelectionTrackerVector*);
  virtual bool includeElement(const CSkeletonElement*) const;
};

#endif // SKELETONSELECTIONCOURIER_H
