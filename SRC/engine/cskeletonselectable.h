// -*- C++ -*-
// $RCSfile: cskeletonselectable.h,v $
// $Revision: 1.1.4.79 $
// $Author: langer $
// $Date: 2014/12/14 22:49:17 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONSELECTABLE_H
#define CSKELETONSELECTABLE_H

#include <oofconfig.h>


#include "common/coord_i.h"
#include "common/lock.h"
#include "common/pythonexportable.h"
#include "engine/cskeletonselectable_i.h"

#include <string>
#include <vtkCell.h>
#include <vtkIdList.h>
#include <vtkSmartPointer.h>
#include <limits>

class CMicrostructure;
class CSkeleton;
class CSkeletonBase;
class LineIntersectionPoint;
class SimpleCellLayer;


// Handy struct for mapping boundaries, etc
struct SelectableMap {
  CSkeletonSelectableList source;
  CSkeletonSelectableList target;
};

SkeletonMapDir otherMapDir(SkeletonMapDir);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


class CSkeletonSelectable : public PythonExportable<CSkeletonSelectable> {

 protected:
  const uidtype uid;
  bool selected;
  bool defunct;
  CSkeletonSelectableList parents;
  CSkeletonSelectableList children;
  GroupNameSet *groups;
 public:
  CSkeletonSelectable();
  virtual ~CSkeletonSelectable();
  const uidtype getUid() const { return uid; }

  virtual bool active(const CSkeletonBase*) const = 0;

  inline bool isSelected() const { return selected; }
  inline void local_select() { selected = true; }
  inline void local_deselect() { selected = false; }
  inline void set_defunct() { defunct = true; } // so far there's no need to un-defunct something
  inline bool is_defunct() const { return defunct; }
  void select(CSelectionTrackerVector *cvector,
	      CSelectionTrackerVector *pvector);
  void selectChildren(CSelectionTrackerVector::iterator, 
		  CSelectionTrackerVector::iterator);
  void selectParents(CSelectionTrackerVector::iterator,
		CSelectionTrackerVector::iterator);
  void deselect(CSelectionTrackerVector *cvector,
		CSelectionTrackerVector *pvector);
  void deselectChildren(CSelectionTrackerVector::iterator,
		    CSelectionTrackerVector::iterator);
  void deselectParents(CSelectionTrackerVector::iterator,
		  CSelectionTrackerVector::iterator);
  
  // implied_select copies the selection data from "current" to
  // "next".  It doesn't actually set the "selected" flag in any
  // CSkeletonSelectable objects.  It's called when a new Skeleton is
  // created within a SkeletonContext.
  void implied_select(CSelectionTrackerBase *current, CSelectionTracker *next);

  // Group membership -- assignment is mechanically like selection.
  void add_to_group(const std::string &group, CGroupTrackerVector *cvector,
		    CGroupTrackerVector *pvector);
  void addDown(const std::string &group, CGroupTrackerVector::iterator,
	       CGroupTrackerVector::iterator);
  void addDown(CGroupTrackerVector::iterator, CGroupTrackerVector::iterator);
  void addUp(const std::string &group, CGroupTrackerVector::iterator,
	     CGroupTrackerVector::iterator);
  void addUp(CGroupTrackerVector::iterator, CGroupTrackerVector::iterator);
  void remove_from_group(const std::string &group, CGroupTrackerVector *cvector,
			 CGroupTrackerVector *pvector);
  void removeDown(const std::string &group, CGroupTrackerVector::iterator,
		  CGroupTrackerVector::iterator);
  void removeUp(const std::string &group, CGroupTrackerVector::iterator,
		CGroupTrackerVector::iterator);
  void add_group_to_local(const std::string &group);
  void remove_group_from_local(const std::string &group);
  bool is_in_group(const std::string &group) const;
  
  const GroupNameSet *groupNames() const { return groups; }

  virtual Coord center() const = 0;
  
  // copying and keeping track of parents and children
  virtual CSkeletonSelectable *copy_child(int idx,
					  vtkSmartPointer<vtkPoints> pts);
  virtual CSkeletonSelectable *new_child(int idx,
					 vtkSmartPointer<vtkPoints> pts) = 0;
  void add_parent(CSkeletonSelectable *);
  void add_parents(const CSkeletonSelectableList&);
  //void remove_parent();
  void add_child(CSkeletonSelectable*);
  void remove_child(CSkeletonSelectable*);
  CSkeletonSelectableList &getParents() { return parents; }
  CSkeletonSelectableList &getChildren() { return children; } 
  CSkeletonSelectableList &getRelatives(SkeletonMapDir); 
  CSkeletonSelectable *last_child() const {
    return (children.empty() ? NULL : children.back());
  }
  CSkeletonSelectable *last_parent() const {
    return (parents.empty() ? NULL : parents.back());
  }
  void makeSibling(CSkeletonSelectable *);
  //void disconnect();
  void map(SelectableMap &s);
  bool inList(const CSkeletonSelectableList &list) const;

  virtual double homogeneity(const CMicrostructure*) const = 0;

  virtual VTKCellType getCellType() const = 0;
  virtual vtkSmartPointer<vtkCell> getVtkCell() const = 0;
  virtual vtkSmartPointer<vtkIdList> getPointIds() const = 0;

  // These methods are defined in all CSkeletonSelectable subclasses.
  // Some classes have similar methods that aren't generic, and
  // therefore can't be called by CSkeletonSelectable base classes.
  virtual void getElements(const CSkeletonBase*, ConstCSkeletonElementVector&)
    const = 0;
  virtual void getElements(const CSkeletonBase*, CSkeletonElementVector&) = 0;
  virtual int nElements() const = 0;

  LineIntersectionPoint *nextIntersection(const CSkeletonBase*, 
					  const ConstCSkeletonElementSet&,
					  const Coord&, const Coord&) const;

  // function used by sorting algorithm for containers of pointers
  static inline bool ltUid(const CSkeletonSelectable *s1,
			   const CSkeletonSelectable *s2)
  {
    return s1->uid < s2->uid; 
  }

  friend inline bool operator==(const CSkeletonSelectable &s1,
				const CSkeletonSelectable &s2)
  {
    return s1.uid == s2.uid;
  }
  
  friend inline bool operator!=(const CSkeletonSelectable &s1,
				const CSkeletonSelectable &s2)
  {
    return s1.uid != s2.uid;
  }
  
  // Sort by uid for deterministic behavior.
  friend inline bool operator<(const CSkeletonSelectable &s1,
			       const CSkeletonSelectable &s2)
  {
    return s1.uid < s2.uid;
  }
  friend inline bool operator>(const CSkeletonSelectable &s1,
			       const CSkeletonSelectable &s2) 
  {
    return s1.uid > s2.uid;
  }
  virtual void print(std::ostream&) const = 0;
};				// CSkeletonSelectable

std::ostream &operator<<(std::ostream &, const CSkeletonSelectable&);


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


class CSkeletonMultiNodeSelectable : public CSkeletonSelectable {
protected:
  // nodes is a pointer because the vector of nodes is sometimes
  // created externally and passed to the constructor.
  CSkeletonNodeVector *nodes;
public:
  CSkeletonMultiNodeSelectable();
  CSkeletonMultiNodeSelectable(CSkeletonNodeVector *ns); //takes ownership of ns
  virtual ~CSkeletonMultiNodeSelectable() { delete nodes; }
  unsigned int nnodes() const { return nodes->size(); }
  const CSkeletonNodeVector *getNodes() const { return nodes; }
  CSkeletonNode *getNode(int i) const { return (*nodes)[i]; }
  int getNodeOrder(const CSkeletonNode*, const CSkeletonNode*) const;
  int getNodeIndexIntoList(const CSkeletonNode *) const;
  virtual bool active(const CSkeletonBase*) const;
  virtual vtkSmartPointer<vtkIdList> getPointIds() const;
  virtual void getPointIds(vtkIdType *) const;
  void getNodeIndices(std::vector<unsigned int>&) const;
  virtual vtkSmartPointer<vtkCell> getVtkCell() const;
  virtual vtkSmartPointer<vtkCell> getEmptyVtkCell() const = 0;
  CSkeletonNodeVector *get_node_children();
  virtual Coord center() const;
  void printNodes(ostream&) const;
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CAbstractTracker {
public:
  virtual ~CAbstractTracker() {}
  virtual CSkeletonSelectableSet *get() = 0;
  virtual const CSkeletonSelectableSet *get() const = 0;
};

class CSelectionTrackerBase : public CAbstractTracker {
private:
  static SLock trackerLock;
  static long trackerCount;
  friend long getTrackerCount();
public:
  CSelectionTrackerBase();
  virtual ~CSelectionTrackerBase();

  virtual CSelectionTracker* sheriff() = 0;
  virtual CSkeletonSelectableSet *get() = 0;
  virtual const CSkeletonSelectableSet *get() const = 0;
  virtual bool empty() const = 0;
  virtual int size() const = 0;
  virtual void clear() = 0;
  virtual void clearskeleton() const = 0;
  virtual void write() const = 0;

  virtual void selectChildren(CSkeletonSelectable*,
			      CSelectionTrackerVector::iterator,
			      CSelectionTrackerVector::iterator) = 0;
  virtual void selectParents(CSkeletonSelectable*,
			     CSelectionTrackerVector::iterator,
			     CSelectionTrackerVector::iterator) = 0;
  virtual void deselectChildren(CSkeletonSelectable*,
				CSelectionTrackerVector::iterator,
				CSelectionTrackerVector::iterator) = 0;
  virtual void deselectParents(CSkeletonSelectable*,
			       CSelectionTrackerVector::iterator,
			       CSelectionTrackerVector::iterator) = 0;
};

long getTrackerCount();

class CSelectionTracker : public CSelectionTrackerBase {
protected:
  CSkeletonSelectableSet data;
public:
  CSelectionTracker() {}
  virtual ~CSelectionTracker() {}
  virtual CSelectionTracker* clone() const;

  virtual CSelectionTracker* sheriff() { return this; }
  virtual CSkeletonSelectableSet* get() { return &data; }
  virtual const CSkeletonSelectableSet* get() const { return &data; }
  virtual bool empty() const { return data.empty(); }
  virtual int size() const { return data.size(); }
  virtual void clear();
  virtual void clearskeleton() const;
  virtual void write() const;

  //void copy(SelectionTrackerBase &other); 
  // CSelectionTracker* promote() { return this; }
  void implied_select(CSelectionTrackerBase *s);

  void add(CSkeletonSelectable *s) { data.insert(s); }
  void remove(CSkeletonSelectable *s) { data.erase(s); }
  virtual void selectChildren(CSkeletonSelectable *s,
			      CSelectionTrackerVector::iterator begin,
			      CSelectionTrackerVector::iterator end);
  virtual void selectParents(CSkeletonSelectable *s,
			     CSelectionTrackerVector::iterator begin,
			     CSelectionTrackerVector::iterator end);
  virtual void deselectChildren(CSkeletonSelectable *s,
				CSelectionTrackerVector::iterator begin,
				CSelectionTrackerVector::iterator end);
  virtual void deselectParents(CSkeletonSelectable *s,
			       CSelectionTrackerVector::iterator begin,
			       CSelectionTrackerVector::iterator end);
  //redeputize, output

  friend class CSkeletonSelectable;
};

class CDeputySelectionTracker : public CSelectionTrackerBase {
protected:
  CSelectionTracker *tracker;
public:
  CDeputySelectionTracker(CSelectionTrackerBase *t) : tracker(t->sheriff()) {}

  virtual CSelectionTracker *sheriff() { return tracker; }
  virtual CSkeletonSelectableSet* get() { return tracker->get(); }
  virtual const CSkeletonSelectableSet* get() const { return tracker->get(); }
  virtual bool empty() const { return tracker->empty(); }
  virtual int size() const { return tracker->size(); }
  virtual void clear() { tracker->clear(); }
  virtual void clearskeleton() const { tracker->clearskeleton(); }
  virtual void write() const { tracker->write(); }

  virtual void selectChildren(CSkeletonSelectable *s,
			      CSelectionTrackerVector::iterator begin,
			      CSelectionTrackerVector::iterator end);
  virtual void selectParents(CSkeletonSelectable *s,
			     CSelectionTrackerVector::iterator begin,
			     CSelectionTrackerVector::iterator end);
  virtual void deselectChildren(CSkeletonSelectable *s,
				CSelectionTrackerVector::iterator begin,
				CSelectionTrackerVector::iterator end);
  virtual void deselectParents(CSkeletonSelectable *s,
			       CSelectionTrackerVector::iterator begin,
			       CSelectionTrackerVector::iterator end);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

uidtype peekUID();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void rebuildLayerCells(const CSkeletonBase*, SimpleCellLayer*,
		       const CAbstractTracker*);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// FindUid is used as an argument to std::find_if when searching for
// matching CSkeletonSelectables.

class FindUid {
public:
  uidtype uid;
  FindUid(uidtype u) : uid(u) {}
  bool operator()(CSkeletonSelectable *sel) {
    return sel->getUid() == uid;
  }
};

#endif	// CSKELETONSELECTABLE_H
