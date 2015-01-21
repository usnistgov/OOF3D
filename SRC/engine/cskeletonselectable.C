// -*- C++ -*-
// $RCSfile: cskeletonselectable.C,v $
// $Revision: 1.1.4.66 $
// $Author: fyc $
// $Date: 2015/01/07 15:53:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/lock.h"
#include "common/printvec.h"
#include "common/IO/canvaslayers.h"
#include "common/IO/oofcerr.h"
#include "common/coord.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonselectable.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletongroups.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static uidtype uidbase = 0;
static SLock uidlock;

// Generate a unique ID for a SkeletonSelectable object.
uidtype safeNewUID() {
  KeyHolder kh(uidlock);
  return uidbase++;
}

// Fetch the next UID that will be created.  Used in testing.
uidtype peekUID() {
  KeyHolder kh(uidlock);
  return uidbase;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


CSkeletonSelectable::CSkeletonSelectable()
  : uid(safeNewUID())
{ 
  selected = false;
  defunct = false;

  // TODO MER: CSkeletonSelectables should share GroupNameSet objects.
  groups = new GroupNameSet;
};

CSkeletonSelectable::~CSkeletonSelectable() {
  // Remove this from its parents' list of children and its children's
  // list of parents.
  for(CSkeletonSelectableList::iterator it=children.begin(); 
      it!=children.end(); ++it) 
    {
      (*it)->parents.remove(this);
    }
  for(CSkeletonSelectableList::iterator it=parents.begin(); 
      it!=parents.end(); ++it) 
    {
      (*it)->children.remove(this);
    }
  delete groups;
}

typedef void (CSelectionTrackerBase::*SelectUpDownFunction)(
					CSkeletonSelectable*,
					CSelectionTrackerVector::iterator,
					CSelectionTrackerVector::iterator);

static void selecthelper(CSelectionTrackerVector::iterator begin,
			 CSelectionTrackerVector::iterator end,
			 CSkeletonSelectableList &relatives,
			 SelectUpDownFunction f)
{
  CSelectionTrackerVector::iterator next = begin+1;
  if(next != end) {
    for(CSkeletonSelectableList::iterator it=relatives.begin();
	it!=relatives.end(); ++it)
      {
	((*next)->*f)((*it), next, end);
      }
  }
}

void CSkeletonSelectable::select(CSelectionTrackerVector *cvector,
				 CSelectionTrackerVector *pvector) 
{
  selected = true;
  // Selection.trackerlist has adjusted the CSelectionTrackerVectors
  // to ensure that (*cvector)[0] isn't a deputy tracker.
  CSelectionTracker *tracker = dynamic_cast<CSelectionTracker*>((*cvector)[0]);
  assert(tracker != 0);
  tracker->add(this);
  // On selection, recursively select_down all your children, then
  // select_up your parents.  The reason for the two selection paths
  // is to prevent having to process spurious selections from
  // children.
  selecthelper(cvector->begin(), cvector->end(), children,
	       &CSelectionTrackerBase::selectChildren);
  selecthelper(pvector->begin(), pvector->end(), parents,
	       &CSelectionTrackerBase::selectParents);
}

void CSkeletonSelectable::selectChildren(
				 CSelectionTrackerVector::iterator begin,
				 CSelectionTrackerVector::iterator end)
{
  // Select an object only if all of its parents are selected.
  for(CSkeletonSelectableList::iterator it=parents.begin(); it!=parents.end();
      ++it) 
    {
      if(!(*it)->selected)
	return;
    }
  selected = true;
  CSelectionTracker *tracker = dynamic_cast<CSelectionTracker*>(*begin);
  assert(tracker != 0);
  tracker->add(this);
  selecthelper(begin, end, children, &CSelectionTrackerBase::selectChildren);
}

void CSkeletonSelectable::selectParents(CSelectionTrackerVector::iterator begin,
				   CSelectionTrackerVector::iterator end)
{
  // Select an object only if all of its children are selected.
  for(CSkeletonSelectableList::iterator it=children.begin();
      it!=children.end(); ++it) 
    {
      if(!(*it)->selected)
	return;
    }
  selected = true;
  CSelectionTracker *tracker = dynamic_cast<CSelectionTracker*>(*begin);
  assert(tracker != 0);
  tracker->add(this);
  selecthelper(begin, end, parents, &CSelectionTrackerBase::selectParents);
}

void CSkeletonSelectable::deselect(CSelectionTrackerVector *cvector,
				   CSelectionTrackerVector *pvector) 
{
  selected = false;
  CSelectionTracker *tracker = dynamic_cast<CSelectionTracker*>((*cvector)[0]);
  assert(tracker != 0);
  tracker->remove(this);
  selecthelper(cvector->begin(), cvector->end(),  children,
	       &CSelectionTrackerBase::deselectChildren);
  selecthelper(pvector->begin(), pvector->end(), parents,
	       &CSelectionTrackerBase::deselectParents);
}

void CSkeletonSelectable::deselectChildren(
				   CSelectionTrackerVector::iterator begin,
				   CSelectionTrackerVector::iterator end)
{
  // Deselect an object only if none of its parents are selected.
  for(CSkeletonSelectableList::iterator it=parents.begin();
      it!=parents.end(); ++it) 
    {
      if((*it)->selected)
	return;
    }
  selected = false;
  CSelectionTracker *tracker = dynamic_cast<CSelectionTracker*>(*begin);
  assert(tracker != 0);
  tracker->remove(this);
  selecthelper(begin, end, children, &CSelectionTrackerBase::deselectChildren);
}

void CSkeletonSelectable::deselectParents(
				  CSelectionTrackerVector::iterator begin,
				  CSelectionTrackerVector::iterator end)
{
  // Deselect an object only if none of its children are selected.
  for(CSkeletonSelectableList::iterator it=children.begin();
      it!=children.end(); ++it) 
    {
      if((*it)->selected)
	return;
    }
  selected = false;
  CSelectionTracker *tracker = dynamic_cast<CSelectionTracker*>(*begin);
  assert(tracker != 0);
  tracker->remove(this);
  selecthelper(begin, end, parents, &CSelectionTrackerBase::deselectParents);
}

void CSelectionTracker::selectChildren(CSkeletonSelectable *s,
				   CSelectionTrackerVector::iterator begin,
				   CSelectionTrackerVector::iterator end)
{
  s->selectChildren(begin, end);
}

void CSelectionTracker::selectParents(CSkeletonSelectable *s,
				 CSelectionTrackerVector::iterator begin,
				 CSelectionTrackerVector::iterator end)
{
  s->selectParents(begin, end);
}

void CSelectionTracker::deselectChildren(CSkeletonSelectable *s,
				     CSelectionTrackerVector::iterator begin,
				     CSelectionTrackerVector::iterator end)
{
  s->deselectChildren(begin, end);
}

void CSelectionTracker::deselectParents(CSkeletonSelectable *s,
				   CSelectionTrackerVector::iterator begin,
				   CSelectionTrackerVector::iterator end)
{
  s->deselectParents(begin, end);
}

// Deputy trackers don't do anything except pass the task on to the
// next tracker.

void CDeputySelectionTracker::selectChildren(
				 CSkeletonSelectable *s,
				 CSelectionTrackerVector::iterator begin,
				 CSelectionTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->selectChildren(s, begin, end);
}

void CDeputySelectionTracker::selectParents(
				 CSkeletonSelectable *s,
				 CSelectionTrackerVector::iterator begin,
				 CSelectionTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->selectParents(s, begin, end);
}

void CDeputySelectionTracker::deselectChildren(
				 CSkeletonSelectable *s,
				 CSelectionTrackerVector::iterator begin,
				 CSelectionTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->deselectChildren(s, begin, end);
}

void CDeputySelectionTracker::deselectParents(
				 CSkeletonSelectable *s,
				 CSelectionTrackerVector::iterator begin,
				 CSelectionTrackerVector::iterator end)
{
  ++begin;
  if(begin == end)
    return;
  (*begin)->deselectParents(s, begin, end);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonSelectable::implied_select(CSelectionTrackerBase *current,
					 CSelectionTracker *next) 
{
  // Called when a new Skeleton is pushed onto the SkeletonContext's
  // undo buffer.  Selects objects in the new Skeleton if *any* of their
  // parent objects are selected in the parent Skeleton. 
  bool anyselected = false;
  CSelectionTracker *base = current->sheriff();
  for(CSkeletonSelectableList::iterator cit=children.begin();
      cit!=children.end(); ++cit)
    {
      for(CSkeletonSelectableList::iterator pit=(*cit)->parents.begin();
	  pit!=(*cit)->parents.end() && !anyselected; ++pit)
	{
	  if(base->data.find(*pit) != base->data.end()) {
	    anyselected = true;
	    break;
	  }
	}
      if(anyselected) {
	next->data.insert(*cit);
      }
    }
}

CSkeletonSelectableList &CSkeletonSelectable::getRelatives(SkeletonMapDir dir) {
  if(dir == MAP_DOWN)
    return children;
  return parents;		// dir == MAP_UP
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

typedef void (CGroupTrackerBase::*GroupUpDownFunction)(
					   CSkeletonSelectable*,
					   const std::string&,
					   CGroupTrackerVector::iterator,
					   CGroupTrackerVector::iterator);

static void grouphelper(const std::string &group,
			CGroupTrackerVector::iterator begin,
			CGroupTrackerVector::iterator end,
			CSkeletonSelectableList &relatives,
			GroupUpDownFunction f) 
{
  CGroupTrackerVector::iterator next = begin+1;
  if(next != end) {
    for(CSkeletonSelectableList::iterator it=relatives.begin();
	it!=relatives.end(); ++it)
      {
	((*next)->*f)(*it, group, next, end);
      }
  }
}

void CSkeletonSelectable::add_to_group(const std::string &group,
				       CGroupTrackerVector *cvector,
				       CGroupTrackerVector *pvector)
{
  groups->insert(group);
  CGroupTracker *tracker = dynamic_cast<CGroupTracker*>((*cvector)[0]);
  assert(tracker != 0);		// (*cvector)[0] can't be a deputy
  tracker->add(group, this);
  grouphelper(group, cvector->begin(), cvector->end(), children,
	      &CGroupTrackerBase::addDown);
  grouphelper(group, pvector->begin(), pvector->end(), parents,
	      &CGroupTrackerBase::addUp);
}

void CSkeletonSelectable::addDown(const std::string &group,
				  CGroupTrackerVector::iterator begin,
				  CGroupTrackerVector::iterator end)
{
  // Add *this to the given group, if all of its parents are in the
  // group.
  for(CSkeletonSelectableList::iterator it=parents.begin(); 
      it!=parents.end(); ++it) 
    {
      // groups is a pointer to a std::set of group names
      if((*it)->groups->count(group) == 0) {
	return;
      }
    }
  groups->insert(group);
  CGroupTracker *tracker = dynamic_cast<CGroupTracker*>(*begin);
  assert(tracker != 0);		// *begin can't be a deputy
  tracker->add(group, this);
  grouphelper(group, begin, end, children, &CGroupTrackerBase::addDown);
}

void CSkeletonSelectable::addDown(CGroupTrackerVector::iterator begin,
				  CGroupTrackerVector::iterator end)
{
  // Add *this to all groups to which all of its parents belong.
  if(!parents.empty()) {
    const CSkeletonSelectable *parent = *(parents.begin());
    for(GroupNameSet::const_iterator git=parent->groups->begin();
	git!=parent->groups->end(); ++git)
      {
	addDown(*git, begin, end);
      }
  }
}

void CSkeletonSelectable::addUp(const std::string &group,
				CGroupTrackerVector::iterator begin,
				CGroupTrackerVector::iterator end)
{
  // Add *this to the given group, if all of its children are in the
  // group.
  for(CSkeletonSelectableList::iterator it=children.begin();
      it!=children.end(); ++it) 
    {
      if((*it)->groups->count(group) == 0)
	return;
    }
  groups->insert(group);
  CGroupTracker *tracker = dynamic_cast<CGroupTracker*>(*begin);
  assert(tracker != 0);		// *begin can't be a deputy
  tracker->add(group, this);
  grouphelper(group, begin, end, parents, &CGroupTrackerBase::addUp);
}

void CSkeletonSelectable::addUp(CGroupTrackerVector::iterator begin,
				CGroupTrackerVector::iterator end)
{
  // Add *this to all groups to which all of its children belong.
  if(!children.empty()) {
    const CSkeletonSelectable *child = (*children.begin());
    for(GroupNameSet::const_iterator git=child->groups->begin();
	git!=child->groups->end(); ++git)
      {
	addUp(*git, begin, end);
      }
  }
}


void CSkeletonSelectable::remove_from_group(const std::string &group,
					    CGroupTrackerVector *cvector,
					    CGroupTrackerVector *pvector) 
{
  groups->erase(group);
  CGroupTracker *tracker = dynamic_cast<CGroupTracker*>((*cvector)[0]);
  assert(tracker != 0);		// (*cvector)[0] can't be a deputy
  tracker->remove(group, this);
  grouphelper(group, cvector->begin(), cvector->end(), children,
	      &CGroupTrackerBase::removeDown);
  grouphelper(group, pvector->begin(), pvector->end(), parents,
	      &CGroupTrackerBase::removeUp);
}

void CSkeletonSelectable::removeDown(const std::string &group,
				     CGroupTrackerVector::iterator begin,
				     CGroupTrackerVector::iterator end)
{
  // TODO 3.1: Why is this done unconditionally?  Shouldn't it check that
  // none of the parents are in the group, ala deselectChildren?
  //
  //I think it is fine here. Because you don't need to check that the parents
  //are in the group or not because you are removing down.
  for(CSkeletonSelectableList::iterator it=parents.begin();
      it!=parents.end(); ++it) 
    {
      if((*it)->groups->count(group) != 0)
  return;
    }
  groups->erase(group);
  CGroupTracker *tracker = dynamic_cast<CGroupTracker*>(*begin);
  assert(tracker != 0);		// *begin can't be a deputy
  tracker->remove(group, this);
  grouphelper(group, begin, end, children, &CGroupTrackerBase::removeDown);
}

void CSkeletonSelectable::removeUp(const std::string &group,
				   CGroupTrackerVector::iterator begin,
				   CGroupTrackerVector::iterator end)
{
  for(CSkeletonSelectableList::iterator it=children.begin();
      it!=children.end(); ++it) 
    {
      if((*it)->groups->count(group) != 0)
	return;
    }
  groups->erase(group);
  CGroupTracker *tracker = dynamic_cast<CGroupTracker*>(*begin);
  assert(tracker != 0);		// *begin can't be a deputy
  tracker->remove(group, this);
  grouphelper(group, begin, end, parents, &CGroupTrackerBase::removeUp);
}



CSkeletonSelectable *CSkeletonSelectable::copy_child(
				     int idx, vtkSmartPointer<vtkPoints> pts) 
{
  CSkeletonSelectable *child = new_child(idx, pts);
  child->add_parent(this);
  add_child(child);
  return child;
}

void add_unique_to_list(CSkeletonSelectableList &list,
			CSkeletonSelectable *item) 
{
  for(CSkeletonSelectableList::iterator it=list.begin(); it!=list.end(); ++it) {
    if((*it)->getUid() == item->getUid()) {
      return;
    }
  }
  list.push_back(item);
}

void CSkeletonSelectable::add_parent(CSkeletonSelectable *newparent) {
#ifdef DEBUG
  // you cannot be your own parent!
  if(uid == newparent->uid) {
    throw ErrProgrammingError(
		      "CSkeletonSelectable: trying to add self as parent",
		      __FILE__, __LINE__);
  }
#endif
  // TODO OPT: If parents were a std::set instead of a std::list,
  // add_unique_to_list wouldn't be necessary.
  add_unique_to_list(parents, newparent);
}

void CSkeletonSelectable::add_parents(const CSkeletonSelectableList &newparents)
{
  for(CSkeletonSelectableList::const_iterator p=newparents.begin();
      p!=newparents.end(); ++p) 
    {
      add_unique_to_list(parents, *p);
    }
}

void CSkeletonSelectable::add_child(CSkeletonSelectable *newchild) {
  add_unique_to_list(children, newchild);
}

void CSkeletonSelectable::remove_child(CSkeletonSelectable *child) {
  children.remove(child);
}

void CSkeletonSelectable::makeSibling(CSkeletonSelectable *other) {
  for(CSkeletonSelectableList::iterator it = parents.begin(); 
      it != parents.end(); ++it) 
    {
      (*it)->add_child(other);
      other->add_parent((*it));
    }
}

void CSkeletonSelectable::add_group_to_local(const std::string &group) {
  groups->insert(group);
}

void CSkeletonSelectable::remove_group_from_local(const std::string &group) {
  groups->erase(group);
}

bool CSkeletonSelectable::is_in_group(const std::string &group) const {
  return groups->count(group); 
}

// Utility function for identifying a "map" from an initial
// selectable.  A "map" is two sets of selectables, s1 and s2, related
// both topologically and familially.  All the selectables in s2 are
// children of at least one selectable in s1, and all the selectables
// in s1 are parents of at least one selectable in s2.  Maps should
// preserve connectivity, i.e. if nodes n1 and n2 are connected in the
// parent set, then c(n1) and c(n2), if they exist, should be
// connected in the child set.  There is also a completeness
// requirement -- all the children of every selectable in s1 should be
// present in s2, and all the parents of the selectables in s2 should
// be present in s1.  It should also be minimal, i.e. it should be the
// smallest set of selectables that has the completeness property.

// TODO MER: Change the name of SelectableMap to RelationshipMap, and
// change the name of CSkeletonSelectable::map to getRelationshipMap.
// "map" is too generic.  The "source" and "target" data in
// RelationshipMap can be renamed to "parents" and "children".  Should
// they be std::sets instead of std::lists?

void CSkeletonSelectable::map(SelectableMap &s) {
  // pass the map in by reference to avoid a bunch of copying.
  s.source.clear();
  s.target.clear();

  bool simple = true;
  s.source.push_back(this);
  s.target.insert(s.target.begin(), children.begin(), children.end());
  for(CSkeletonSelectableList::iterator it=s.target.begin(); it!=s.target.end();
      ++it)
    {
      if((*it)->getParents().size() != 1) 
	simple = false;
    }
  if(simple) {
    return;
  }
  // it's complicated

  int old_c = 0;
  int old_p = 0;
  int new_c = s.target.size();
  int new_p = s.source.size();
  while(old_c != new_c || old_p != new_p) {
    old_c = new_c;
    old_p = new_p;
    for(CSkeletonSelectableList::iterator c=s.target.begin(); c!=s.target.end();
	++c)
      {
	// oofcerr << "num parents " << (*c)->getParents()->size() << std::endl;
	for(CSkeletonSelectableList::iterator p = (*c)->getParents().begin();
	    p != (*c)->getParents().end(); ++p)
	  {
	    // oofcerr << "parent uid " << (*p)->getUid() << std::endl;
	    if(!(*p)->inList(s.source))
	      s.source.push_back(*p);
	  }
      }
    for(CSkeletonSelectableList::iterator p=s.source.begin(); p!=s.source.end();
	++p)
      {
	for(CSkeletonSelectableList::iterator c=(*p)->getChildren().begin();
	    c!=(*p)->getChildren().end(); ++c)
	  {
	    // oofcerr << "child uid " << (*c)->getUid() << std::endl;
	    if(!(*p)->inList(s.source))
	      s.target.push_back(*c);
	  }
      }
    new_c = s.target.size();
    new_p = s.source.size();
  }
} // end CSkeletonSelectable::map


bool CSkeletonSelectable::inList(const CSkeletonSelectableList &list) const {
  // oofcerr << "CSkeletonSelectable::inList" << std::endl;
  return std::find_if(list.begin(), list.end(), FindUid(uid)) != list.end();
  // for(CSkeletonSelectableList::const_iterator it=list.begin(); it!=list.end();
  //     ++it) 
  //   {
  //     if(uid == (*it)->getUid())
  // 	return true;
  //   }
  // return false;
}

CSkeletonMultiNodeSelectable::CSkeletonMultiNodeSelectable() 
  : CSkeletonSelectable(),
    nodes(new CSkeletonNodeVector)
{}

CSkeletonMultiNodeSelectable::CSkeletonMultiNodeSelectable(
						   CSkeletonNodeVector *ns) 
  : CSkeletonSelectable(),
    nodes(ns)
{}


int CSkeletonMultiNodeSelectable::getNodeIndexIntoList(const CSkeletonNode *n)
const 
{
  int i=0;
  for(CSkeletonNodeIterator it=nodes->begin(); it!=nodes->end(); ++it, ++i) 
    if(**it == *n) 
      return i;
  return -1;
}

// If node0 and node1 occur in that order in the node list, return 1.
// If they're in the opposite order, return -1.  If they're not
// adjacent, return 0.

int CSkeletonMultiNodeSelectable::getNodeOrder(const CSkeletonNode *node0,
					       const CSkeletonNode *node1)
  const
{
  for(unsigned int i=0; i<nnodes(); i++) {
    if(node0 == (*nodes)[i]) {
      if(node1 == (*nodes)[(i+1) % nnodes()])
	return 1;
      if(node1 == (*nodes)[(i+nnodes()-1) % nnodes()])
	return -1;
    }
  }
  return 0;
}

bool CSkeletonMultiNodeSelectable::active(const CSkeletonBase *skeleton) const {
  for(unsigned int i=0; i<nodes->size(); ++i)
    if((*nodes)[i]->active(skeleton))
      return true;
  return false;
}

CSkeletonNodeVector *CSkeletonMultiNodeSelectable::get_node_children() {
  // TODO 3.1: should this method be const?
  CSkeletonNodeVector *children = new CSkeletonNodeVector;
  for(unsigned int i=0; i<nodes->size(); ++i)
    children->push_back(
	dynamic_cast<CSkeletonNode*>((*nodes)[i]->getChildren().back()));
  return children;
}

Coord CSkeletonMultiNodeSelectable::center() const {
  Coord x;
  for(unsigned int i=0; i<nodes->size(); ++i) {
    x += (*nodes)[i]->position();
  }
  x /= nodes->size();
  return x;
}

vtkSmartPointer<vtkIdList> CSkeletonMultiNodeSelectable::getPointIds() const {
  vtkSmartPointer<vtkIdList> list = vtkSmartPointer<vtkIdList>::New();
  list->SetNumberOfIds(nodes->size());
  for(unsigned int i=0; i<nodes->size(); ++i) 
    list->SetId(i,(*nodes)[i]->getIndex());
  return list;
}

void CSkeletonMultiNodeSelectable::getPointIds(vtkIdType *ids) const {
  for(unsigned int i=0; i<nodes->size(); ++i) 
    ids[i] = (*nodes)[i]->getIndex();
}

void CSkeletonMultiNodeSelectable::getNodeIndices(
				  std::vector<unsigned int> &nidxs)
  const 
{
  for(unsigned int i=0; i<nodes->size(); ++i) 
    nidxs.push_back((*nodes)[i]->getIndex());
}

vtkSmartPointer<vtkCell> CSkeletonMultiNodeSelectable::getVtkCell() const {
  Coord x;
  vtkSmartPointer<vtkCell> cell = getEmptyVtkCell();
  for(unsigned int i=0; i<nodes->size(); ++i) {
    cell->GetPointIds()->SetId(i,i); //(*nodes)[i]->getIndex());
    x = (*nodes)[i]->position();
    cell->GetPoints()->SetPoint(i,x.xpointer());
  }
  return cell;
}

void CSkeletonMultiNodeSelectable::printNodes(ostream &os) const {
  os << "[";
  for(unsigned int i=0; i<nodes->size(); ++i) {
    Coord x = (*nodes)[i]->position();
    os << (*nodes)[i]->getUid() << " " << x;
    if(i < nodes->size()-1)
      os << ", ";
  }
  os << "]";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SLock CSelectionTrackerBase::trackerLock;
long CSelectionTrackerBase::trackerCount = 0;

CSelectionTrackerBase::CSelectionTrackerBase() {
  trackerLock.acquire();
  ++trackerCount;		// for debugging, decremented by destructor
  trackerLock.release();
}

CSelectionTrackerBase::~CSelectionTrackerBase() {
  trackerLock.acquire();
  --trackerCount;		// for testing
  trackerLock.release();
}

long getTrackerCount() {
  return CSelectionTrackerBase::trackerCount; 
}

CSelectionTracker* CSelectionTracker::clone() const {
  CSelectionTracker* shakes = new CSelectionTracker();
  shakes->data.insert(data.begin(), data.end());
  return shakes;
}

void CSelectionTracker::clear() {
  for(CSkeletonSelectableSet::iterator it=data.begin(); it!=data.end(); ++it) 
    (*it)->local_deselect();
  data.clear();
}

void CSelectionTracker::clearskeleton() const {
  for(CSkeletonSelectableSet::const_iterator it=data.begin(); it!=data.end();
      ++it) 
    {
      (*it)->local_deselect();
    }
}

void CSelectionTracker::write() const {
  for(CSkeletonSelectableSet::const_iterator it=data.begin(); it!=data.end();
      ++it) 
    {
      (*it)->local_select();
    }
}

void CSelectionTracker::implied_select(CSelectionTrackerBase *other) {
  for(CSkeletonSelectableSet::iterator it = other->get()->begin(); 
      it != other->get()->end(); ++it) 
    (*it)->implied_select(other, this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const CSkeletonSelectable &css) {
  css.print(os);
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SkeletonMapDir otherMapDir(SkeletonMapDir dir) {
  if(dir == MAP_DOWN)
    return MAP_UP;
  else
    return MAP_DOWN;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

LineIntersectionPoint *CSkeletonSelectable::nextIntersection(
				   const CSkeletonBase *skel,
				   const ConstCSkeletonElementSet &traversed,
				   const Coord &xstart, const Coord &xend)
  const
{
  ConstCSkeletonElementVector elements;
  getElements(skel, elements);
  double maxAlpha = -std::numeric_limits<double>::max();
  LineIntersectionPoint *next = 0;
  // oofcerr << "CSkeletonSelectable::nextIntersection: this=" << *this << std::endl;
  // Loop over neighboring elements...
  for(ConstCSkeletonElementVector::const_iterator nbr=elements.begin();
      nbr!=elements.end(); ++nbr)
    {
      // ... but only if they haven't already been used in this cross section
      ConstCSkeletonElementSet::const_iterator i=traversed.find(*nbr);
      if(i == traversed.end()) {
	if((*nbr)->interior(&xend)) {
	  return new LineIntersectionEndPoint(*nbr, xstart, xend);
	}
	// oofcerr << "CSkeletonSelectable::nextIntersection: examining " << **nbr
	// 	<< std::endl;
	LineIntersectionPoint *entrancePt = 0;
	LineIntersectionPoint *exitPt = 0;
	(*nbr)->lineIntersections(skel, xstart, xend, &entrancePt, &exitPt);
	if(exitPt && exitPt->getAlpha() > maxAlpha) {
	  // double oldmax = maxAlpha;	// debugging
	  maxAlpha = exitPt->getAlpha();
	  // oofcerr << "CSkeletonSelectable::nextIntersection: maxAlpha="
	  // 	  << maxAlpha << " (" << maxAlpha-oldmax << ")" << std::endl;
	  delete next;
	  next = exitPt;
	}
	else {
	  // if(!exitPt)
	  //   oofcerr << "CSkeletonSelectable::nextIntersection: no exit point"
	  // 	    << std::endl;
	  // else
	  //   oofcerr << "CSkeletonSelectable::nextIntersection: alpha too small "
	  // 	    << exitPt->getAlpha() << " (" << maxAlpha-exitPt->getAlpha()
	  // 	    << ")" << std::endl;
	  delete exitPt;
	}
	delete entrancePt;
      }	// end if (i != traversed.end())
    }	// end loop over elements
  // if(next)
  //   oofcerr << "CSkeletonSelectable::nextIntersection: returning " << *next
  // 	    << std::endl;
  // else
  //   oofcerr << "CSkeletonSelectable::nextIntersection: returning nothing"
  // 	    << std::endl;
  return next;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool CSkeletonSelectableLTUid::operator()(const CSkeletonSelectable *s1,
					  const CSkeletonSelectable *s2)
  const
{
  return *s1 < *s2;
}

bool CSkeletonSelectablePairLTUid::operator()(const CSkeletonSelectablePair &a,
					      const CSkeletonSelectablePair &b)
  const
{
    if(*a.first == *b.first)
      return *a.second < *b.second;
    return *a.first < *b.first;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void rebuildLayerCells(const CSkeletonBase *skel, 
		       SimpleCellLayer *canvaslayer,
		       const CAbstractTracker *tracker)
{
  const CSkeletonSelectableSet *s = tracker->get();
  canvaslayer->newGrid(skel->getPoints(), s->size());
  for(CSkeletonSelectableSet::const_iterator i=s->begin(); i!=s->end(); ++i) {
    canvaslayer->addCell((*i)->getCellType(), (*i)->getPointIds());
  }
}
