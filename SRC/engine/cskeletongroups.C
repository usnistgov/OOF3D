// -*- C++ -*-
// $RCSfile: cskeletongroups.C,v $
// $Revision: 1.1.2.11 $
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

#include "common/IO/oofcerr.h"
#include "engine/cskeletongroups.h"
#include "engine/cskeletonselectable.h"


void CGroupTracker::add_group(const std::string &name) { 
  data[name] = new CSkeletonSelectableSet; 
}

void CGroupTracker::clear_group(const std::string &name) {
  CSkeletonSelectableSet *sss = data[name];
  for(CSkeletonSelectableSet::iterator it=sss->begin(); it!=sss->end(); ++it) {
    (*it)->remove_group_from_local(name);
  }
  sss->clear();
}

void CGroupTracker::remove_group(const std::string &name) {
  clear_group(name);
  delete data[name];
  data.erase(name);
}

void CGroupTracker::rename_group(const std::string &oldname,
				 const std::string &newname) 
{
  if(newname.compare(oldname) != 0){
    data[newname] = new CSkeletonSelectableSet;
    CSkeletonSelectableSet *sss = data[oldname];
    for(CSkeletonSelectableSet::iterator it=sss->begin(); it!=sss->end(); ++it) {
      add(newname,*(it));
    }
    delete sss;
    data.erase(oldname);
  }
}

void CGroupTracker::add(const std::string &name, CSkeletonSelectable *s) {
  data[name]->insert(s); 
}

void CGroupTracker::remove(const std::string &name, CSkeletonSelectable *s) {
  data[name]->erase(s); 
}

CSkeletonSelectableSet* CGroupTracker::get_group(const std::string &name) const
{
  // "return data[name]" doesn't work, because operator[] isn't const.
  CGroupMap::const_iterator it = data.find(name);
  return (*it).second;
}

int CGroupTracker::get_group_size(const std::string &name) const {
  // "return data[name]->size()" doesn't work because operator[] isn't const.
  CGroupMap::const_iterator it = data.find(name);
  return (*it).second->size();
}

void CGroupTracker::addDown(CSkeletonSelectable *s, const std::string &group,
			    CGroupTrackerVector::iterator begin,
			    CGroupTrackerVector::iterator end) 
{
  s->addDown(group, begin, end);
}
void CGroupTracker::addUp(CSkeletonSelectable *s, const std::string &group,
			  CGroupTrackerVector::iterator begin,
			  CGroupTrackerVector::iterator end) 
{
  s->addUp(group, begin, end);
}
void CGroupTracker::removeDown(CSkeletonSelectable *s, const std::string &group,
			       CGroupTrackerVector::iterator begin,
			       CGroupTrackerVector::iterator end) 
{
  s->removeDown(group, begin, end);
}

void CGroupTracker::removeUp(CSkeletonSelectable *s, const std::string &group,
			     CGroupTrackerVector::iterator begin,
			     CGroupTrackerVector::iterator end)
{
  s->removeUp(group, begin, end);
}

void CDeputyGroupTracker::addDown(CSkeletonSelectable *s,
				  const std::string &group,
				  CGroupTrackerVector::iterator begin,
				  CGroupTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->addDown(s, group, begin, end);
}

void CDeputyGroupTracker::addUp(CSkeletonSelectable *s,
				const std::string &group,
				CGroupTrackerVector::iterator begin,
				CGroupTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->addUp(s, group, begin, end);
}

void CDeputyGroupTracker::removeDown(CSkeletonSelectable *s,
				     const std::string &group,
				     CGroupTrackerVector::iterator begin,
				     CGroupTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->removeDown(s, group, begin, end);
}

void CDeputyGroupTracker::removeUp(CSkeletonSelectable *s,
				   const std::string &group,
				   CGroupTrackerVector::iterator begin,
				   CGroupTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->removeUp(s, group, begin, end);
}
				  
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const CGroupTracker &gt) {
  os << "CGroupTracker(" << &gt << "; ";
  for(CGroupMap::const_iterator i=gt.data.begin(); i!=gt.data.end(); ++i) {
    os << (*i).first << " [";
    const CSkeletonSelectableSet &s = *(*i).second;
    for(CSkeletonSelectableSet::const_iterator j=s.begin(); j!=s.end(); ++j)
      os << *(*j) << " ";
    os << "]";
  }
  os << ")";
  return os;
}
