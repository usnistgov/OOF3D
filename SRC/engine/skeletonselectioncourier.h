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

class SkeletonSelectionCourier {
protected:
  CSkeletonBase *skeleton;
  CSelectionTrackerVector clist, plist; // Trackers for the selection
  bool done_;
public:
  SkeletonSelectionCourier(CSkeletonBase*, CSelectionTrackerVector*,
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
  bool done() const { return done_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

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
  SkeletonGroupCourier(CSkeletonBase*,
		       const std::string&,
		       const CGroupTrackerBase*,
		       CSelectionTrackerVector*, CSelectionTrackerVector*);
};


// NodeSelection methods which compute and store a set of nodes in
// their constructor can be derived from NodeSelectionCourier.

class NodeSelectionCourier : public SkeletonSelectionCourier {
protected:
  CSkeletonNodeSet selectedNodes;
  CSkeletonNodeSet::iterator iter;
public:
  NodeSelectionCourier(CSkeletonBase*, CSelectionTrackerVector*,
		       CSelectionTrackerVector*);
  virtual void start();
  virtual CSkeletonSelectable *currentObj() const { return *iter; }
  virtual void next();
};

// Intermediate base class for selecting Nodes from other kinds of
// selections.

class NodesFromOtherCourier : public NodeSelectionCourier {
protected:
  virtual CSkeletonNodeSet exteriorNodes() const = 0;
  CSkeletonNodeSet allNodes() const;
  std::string coverage;
  const CSelectionTracker *otherTracker;
public:
  NodesFromOtherCourier(CSkeletonBase*, const std::string*,
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
  NodesFromElementsCourier(CSkeletonBase*,
			   const std::string*,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};

class NodesFromFacesCourier : public NodesFromOtherCourier {
private:
  virtual CSkeletonNodeSet exteriorNodes() const;
public:
  NodesFromFacesCourier(CSkeletonBase*,
			const std::string*,
			const CSelectionTracker*,
			CSelectionTrackerVector*,
			CSelectionTrackerVector*);
};

class NodesFromSegmentsCourier : public NodeSelectionCourier {
public:
  NodesFromSegmentsCourier(CSkeletonBase*,
			   const CSelectionTracker*,
			   CSelectionTrackerVector*,
			   CSelectionTrackerVector*);
};

#endif // SKELETONSELECTIONCOURIER_H
