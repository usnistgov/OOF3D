// -*- C++ -*-
// $RCSfile: cskeletongroups.h,v $
// $Revision: 1.1.2.8 $
// $Author: langer $
// $Date: 2014/12/14 01:07:49 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSKELETONGROUPS_H
#define CSKELETONGROUPS_H

class CDeputyGroupTracker;
class CGroupTracker;
class CGroupTrackerBase;

#include "engine/cskeletonselectable_i.h"

#include <string>

typedef std::map<std::string, CSkeletonSelectableSet*> CGroupMap;

class CGroupTrackerBase {
public:
  virtual ~CGroupTrackerBase() {}
  virtual CGroupTracker *sheriff() = 0;
  virtual CSkeletonSelectableSet* get_group(const std::string&) const = 0;
  virtual void addDown(CSkeletonSelectable*, const std::string&,
		       CGroupTrackerVector::iterator,
		       CGroupTrackerVector::iterator) = 0;
  virtual void addUp(CSkeletonSelectable*, const std::string&,
		     CGroupTrackerVector::iterator,
		     CGroupTrackerVector::iterator) = 0;
  virtual void removeDown(CSkeletonSelectable*, const std::string&,
			  CGroupTrackerVector::iterator,
			  CGroupTrackerVector::iterator) = 0;
  virtual void removeUp(CSkeletonSelectable*, const std::string&,
			CGroupTrackerVector::iterator,
			CGroupTrackerVector::iterator) = 0;
};

class CGroupTracker : public CGroupTrackerBase { 
protected:
  CGroupMap data;
public:
  CGroupTracker() {};
  virtual ~CGroupTracker() {};
  void add_group(const std::string&);
  void clear_group(const std::string&);
  void remove_group(const std::string&);
  void rename_group(const std::string &oldname, const std::string &newname);
  void add(const std::string&, CSkeletonSelectable *s);
  void remove(const std::string&, CSkeletonSelectable *s);
  virtual CSkeletonSelectableSet* get_group(const std::string&) const;
  int get_group_size(const std::string&) const;

  virtual CGroupTracker* sheriff() { return this; }

  virtual void addDown(CSkeletonSelectable *s, const std::string &group,
		       CGroupTrackerVector::iterator,
		       CGroupTrackerVector::iterator);
   virtual void addUp(CSkeletonSelectable *s, const std::string &group,
		     CGroupTrackerVector::iterator,
		     CGroupTrackerVector::iterator);
  virtual void removeDown(CSkeletonSelectable *s, const std::string &group,
			  CGroupTrackerVector::iterator,
			  CGroupTrackerVector::iterator);
  virtual void removeUp(CSkeletonSelectable *s, const std::string &group,
			CGroupTrackerVector::iterator,
			CGroupTrackerVector::iterator);

  friend class CSkeletonSelectable;
  friend std::ostream &operator<<(std::ostream&, const CGroupTracker&);
};

class CDeputyGroupTracker : public CGroupTrackerBase {
protected:
  CGroupTracker *tracker;
public:
  CDeputyGroupTracker(CGroupTrackerBase* t) : tracker(t->sheriff()) {}
  virtual CGroupTracker* sheriff() { return tracker; }
  virtual CSkeletonSelectableSet* get_group(const std::string& g) const {
    return tracker->get_group(g);
  }
  virtual void addDown(CSkeletonSelectable *s, const std::string &group,
		       CGroupTrackerVector::iterator,
		       CGroupTrackerVector::iterator);
   virtual void addUp(CSkeletonSelectable *s, const std::string &group,
		     CGroupTrackerVector::iterator,
		     CGroupTrackerVector::iterator);
  virtual void removeDown(CSkeletonSelectable *s, const std::string &group,
			  CGroupTrackerVector::iterator,
			  CGroupTrackerVector::iterator);
  virtual void removeUp(CSkeletonSelectable *s, const std::string &group,
			CGroupTrackerVector::iterator,
			CGroupTrackerVector::iterator);
};


#endif	// CSKELETONGROUPS_H
