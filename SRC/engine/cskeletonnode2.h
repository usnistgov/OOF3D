// -*- C++ -*-
// $RCSfile: cskeletonnode2.h,v $
// $Revision: 1.1.2.55 $
// $Author: langer $
// $Date: 2014/12/14 22:49:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONNODE2_H
#define CSKELETONNODE2_H

#include <oofconfig.h>

#include "common/coord.h"
#include "common/timestamp.h"
#include "engine/cskeletonselectable.h"

#include <vtkPoints.h>
#include <vtkSmartPointer.h>
#include <algorithm>

class CPinnedNodeTracker;
class CSkeleton;

typedef std::vector<CPinnedNodeTracker*> CPinnedNodeTrackerVector;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonNode : public CSkeletonSelectable {
private:
  CSkeletonElementVector *elements;
  // this is the location in the points object and CSkeletonNodeVector
  int index;
  // TODO OPT: Does each node really need its own pointer to points?  That
  // uses a lot of memory.  A pointer to the CSkeleton could be passed
  // in as an argument each time the points are needed.
  vtkSmartPointer<vtkPoints> points; // same as the CSkeletonBase points array
  Coord last_position;
  TimeStamp nodemoved;
  TimeStamp lastmoved;
  unsigned char mobility;
  static const unsigned char unpinned_;
  static const unsigned char xmovable_;
  static const unsigned char ymovable_;
#if DIM==3
  static const unsigned char zmovable_;
#endif
  static const unsigned char freenode_;
  static const std::string modulename_;
  static const std::string classname_;

  static long globalNodeCount;

public:
  CSkeletonNode(int idx, vtkSmartPointer<vtkPoints> pts);
  virtual ~CSkeletonNode();

  virtual const std::string &modulename() const { return modulename_; }
  virtual const std::string &classname() const { return classname_; }

  // virtual CSkeletonNode *copy_child(int, vtkSmartPointer<vtkPoints>);
  virtual CSkeletonNode *new_child(int idx, vtkSmartPointer<vtkPoints> pts);
  Coord position() const;// { return points->GetPoint(index); }
  Coord getPosition() const;
  virtual Coord center() const { return position(); }
  int getIndex() const { return index; }
  void setIndex(int idx) { index = idx; }

  void setMobilityX(bool mob);
  bool movable_x() const {
    return (mobility & xmovable_) && (mobility & unpinned_);
  }
  bool movable_intrinsic_x() const {
    return mobility & xmovable_;
  }
  
  void setMobilityY(bool mob);
  bool movable_y() const {
    return (mobility & ymovable_) && (mobility & unpinned_);
  }
  bool movable_intrinsic_y() const {
    return mobility & ymovable_;
  }
#if DIM==2
  bool movable() const { return movable_x() || movable_y(); }
#elif DIM==3
  void setMobilityZ(bool mob);
  bool movable_z() const {
    return (mobility & zmovable_) && (mobility & unpinned_);
  }  
  bool movable_intrinsic_z() const {
    return mobility & zmovable_;
  }
  bool movable() const { return movable_x() || movable_y() || movable_z(); }
#endif
  void copyMobility(CSkeletonNode *);

  int dominantPixel(const CMicrostructure*) const;

  bool pinned() const { return !(mobility & unpinned_); }
  void setPinned(bool pin);  

  void pin(CPinnedNodeTrackerVector *cvector,
	   CPinnedNodeTrackerVector *pvector);
  void pinChildren(CPinnedNodeTrackerVector::iterator,
		   CPinnedNodeTrackerVector::iterator, const Coord&);
  void pinParents(CPinnedNodeTrackerVector::iterator,
		  CPinnedNodeTrackerVector::iterator, const Coord&);
  
  void unpin(CPinnedNodeTrackerVector *cvector,
	     CPinnedNodeTrackerVector *pvector);
  void unpinChildren(CPinnedNodeTrackerVector::iterator,
		     CPinnedNodeTrackerVector::iterator, const Coord&);
  void unpinParents(CPinnedNodeTrackerVector::iterator,
		    CPinnedNodeTrackerVector::iterator, const Coord&);

  bool moveTo(const Coord &pos);
  bool moveBy(const Coord &disp);
  bool canMoveTo(const Coord &pos) const;
  
  void unconstrainedMoveTo(const Coord&);
  void moveBack();
  bool canMergeWith(const CSkeletonNode *other) const;
  bool illegal() const;

  virtual bool active(const CSkeletonBase *) const ;
  virtual vtkSmartPointer<vtkCell> getVtkCell() const;
  virtual VTKCellType getCellType() const;
  virtual vtkSmartPointer<vtkIdList> getPointIds() const ;

  //static int hash(const CSkeletonNode *n1, const CSkeletonNode *n2);
  //static int hash(const CSkeletonNode *n1, const CSkeletonNode *n2, const CSkeletonNode *n3);

  void addElement(CSkeletonElement* el);
  void removeElement(CSkeletonElement* el, CSkeleton *skel);
  bool hasElement(CSkeletonElement* el);
  CSkeletonElement *getElement(int i) const { return (*elements)[i]; }
  CSkeletonElementVector *getElements() const { return elements; }
  int nElements() const { return elements->size(); }

  // Generic version used by SkeletonFilters in display methods.
  virtual void getElements(const CSkeletonBase*, ConstCSkeletonElementVector&)
    const;
  virtual void getElements(const CSkeletonBase*, CSkeletonElementVector&);

  // homogeneity() has to be defined in all CSkeletonSelectable
  // classes, although it doesn't mean much here.  It's used by
  // HomogeneityFilter.  TODO OPT: Change the filter classes so that
  // filters can specify which classes they operate on, and remove
  // this function.
  virtual double homogeneity(const CMicrostructure*) const { return 1.0; }

  // static functions for pin modifiers
  // TODO MER: These don't really belong in this class.  Move to CSkeleton?
  static void pinSet(CSkeletonNodeSet *set,
		     CPinnedNodeTrackerVector *cvector,
		     CPinnedNodeTrackerVector *pvector);
  // TODO MER: this is where a template would be nice
  // TODO 3.1: There should be an arg that provides the operation (pin,
  // unpin, toggle, etc and an arg that provides the operand (selected
  // nodes, selected elements, internal bdys, etc) and all
  // combinations should be allowed.
  static void pinSet(CSkeletonSelectableSet *set, 
		     CPinnedNodeTrackerVector *cvector,
		     CPinnedNodeTrackerVector *pvector);
  static void pinSelection(CSelectionTrackerBase *tracker, 
			   CPinnedNodeTrackerVector *cvector,
			   CPinnedNodeTrackerVector *pvector);
  static void unpinSet(CSkeletonNodeSet *set,
		       CPinnedNodeTrackerVector *cvector,
		       CPinnedNodeTrackerVector *pvector);
  static void unpinSet(CSkeletonSelectableSet *set,
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

  virtual void print(std::ostream &) const;

  friend class CSkeleton;
  friend class CSkeletonElement;
  friend class CSkeletonMultiNodeKey;
  friend long get_globalNodeCount();
};				// CSkeletonNode

long get_globalNodeCount();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonMultiNodeKey {
private:
  UidVector uids;		// sorted vector of node uids.
public:
  CSkeletonMultiNodeKey() {}
  CSkeletonMultiNodeKey(const CSkeletonNode *n1, const CSkeletonNode *n2) {
    uids.reserve(2);
    uids.push_back(n1->uid);
    uids.push_back(n2->uid);
    std::sort(uids.begin(), uids.end());
  }
  CSkeletonMultiNodeKey(uidtype i1, uidtype i2) {
    uids.reserve(2);
    uids.push_back(i1);
    uids.push_back(i2);
    std::sort(uids.begin(), uids.end());
  }
  CSkeletonMultiNodeKey(const CSkeletonNode *n1, const CSkeletonNode *n2,
			const CSkeletonNode *n3) 
  {
    uids.reserve(3);
    uids.push_back(n1->uid);
    uids.push_back(n2->uid);
    uids.push_back(n3->uid);
    std::sort(uids.begin(), uids.end());
  }
  CSkeletonMultiNodeKey(uidtype i1, uidtype i2, uidtype i3) {
    uids.reserve(3);
    uids.push_back(i1);
    uids.push_back(i2);
    uids.push_back(i3);
    std::sort(uids.begin(), uids.end());
  }
  CSkeletonMultiNodeKey(const CSkeletonNode *n1, const CSkeletonNode *n2,
			const CSkeletonNode *n3, const CSkeletonNode *n4) 
  {
    uids.reserve(4);
    uids.push_back(n1->uid);
    uids.push_back(n2->uid);
    uids.push_back(n3->uid);
    uids.push_back(n4->uid);
    std::sort(uids.begin(), uids.end());
  }
  CSkeletonMultiNodeKey(const CSkeletonMultiNodeSelectable *s) {
    uids.reserve(s->nnodes()); 
    for(unsigned int i = 0; i < s->nnodes(); ++i)
      uids.push_back(s->getNode(i)->uid);
    std::sort(uids.begin(), uids.end());
  }
  friend inline bool operator<(const CSkeletonMultiNodeKey &o1,
			       const CSkeletonMultiNodeKey &o2) 
  {
    return o1.uids < o2.uids;
  }
  friend inline bool operator==(const CSkeletonMultiNodeKey &o1,
				const CSkeletonMultiNodeKey &o2)
  {
    return o1.uids == o2.uids;
  }
  friend std::ostream &operator<<(std::ostream&, const CSkeletonMultiNodeKey&);
};

std::ostream &operator<<(std::ostream&, const CSkeletonMultiNodeKey&);

typedef std::set<CSkeletonMultiNodeKey> CSkeletonMultiNodeKeySet;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CPinnedNodeTracker
  : public CAbstractTracker, PythonExportable<CPinnedNodeTracker> 
{ 
protected:
  // data is a CSkeletonSelectableSet instead of a CSkeletonNodeSet so
  // that the return value of get() can be compatible with the other
  // CAbstractTracker subclasses.
  CSkeletonSelectableSet data;
  CSkeletonBase *skeleton;
 public:
  CPinnedNodeTracker(CSkeletonBase*);
  virtual ~CPinnedNodeTracker() {}
  virtual const std::string &classname() const;
  virtual const std::string &modulename() const;
  virtual CPinnedNodeTracker* clone() const;
  void add(CSkeletonNode*);
  void remove(CSkeletonNode*);
  virtual CSkeletonSelectableSet* get() { return &data; }
  virtual const CSkeletonSelectableSet* get() const { return &data; }
  int size() const { return data.size(); }
  //void copy(SelectionTrackerBase &other); 
  CPinnedNodeTracker* sheriff() { return this; }
  Coord nodePosition(CSkeletonNode*);
  void clear();
  virtual void write();
  void clearskeleton();
  void implied_pin(CPinnedNodeTracker*);
  virtual void pinChildren(CSkeletonNode*, CPinnedNodeTrackerVector::iterator, 
			   CPinnedNodeTrackerVector::iterator, const Coord&);
  virtual void pinParents(CSkeletonNode*, CPinnedNodeTrackerVector::iterator, 
			  CPinnedNodeTrackerVector::iterator, const Coord&);
  virtual void unpinChildren(CSkeletonNode*,
			     CPinnedNodeTrackerVector::iterator, 
			     CPinnedNodeTrackerVector::iterator, const Coord&);
  virtual void unpinParents(CSkeletonNode*, CPinnedNodeTrackerVector::iterator, 
			    CPinnedNodeTrackerVector::iterator, const Coord&);
  // output
  virtual std::string printself() const;
  // debugging
  CSkeletonBase *getSkeleton() { return skeleton; }
};

// Unlike the other deputy trackers, the DeputyPinnedNodeTracker has
// its own data and doesn't refer to another tracker.  That's because
// the same node can be pinned in a skeleton and unpinned in a deputy
// skeleton.  DeputyPinnedNodeTrackers and PinnedNodeTrackers differ
// only in how the pinned state is propagated from skeleton to
// skeleton.

class CDeputyPinnedNodeTracker : public CPinnedNodeTracker {
 public:
  CDeputyPinnedNodeTracker(CSkeletonBase*);
  virtual const std::string& classname() const;
  virtual CPinnedNodeTracker* clone() const;
  void implied_pin(CPinnedNodeTracker *s);
  virtual void pinChildren(CSkeletonNode*, CPinnedNodeTrackerVector::iterator, 
			   CPinnedNodeTrackerVector::iterator, const Coord&);
  virtual void pinParents(CSkeletonNode*, CPinnedNodeTrackerVector::iterator, 
			  CPinnedNodeTrackerVector::iterator, const Coord&);
  virtual void unpinChildren(CSkeletonNode*,
			     CPinnedNodeTrackerVector::iterator, 
			     CPinnedNodeTrackerVector::iterator, const Coord&);
  virtual void unpinParents(CSkeletonNode*, CPinnedNodeTrackerVector::iterator, 
		       CPinnedNodeTrackerVector::iterator, const Coord&);
  virtual std::string printself() const;
};

std::ostream& operator<<(std::ostream&, const CPinnedNodeTracker&);


#endif	// CSKELETONNODE2_H
