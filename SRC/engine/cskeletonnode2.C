// -*- C++ -*-
// $RCSfile: cskeletonnode2.C,v $
// $Revision: 1.1.2.57 $
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


#include "common/IO/oofcerr.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/lock.h"
#include "common/tostring.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonsegment.h"

#include <vtkVertex.h>
#include <algorithm>

const unsigned char CSkeletonNode::xmovable_ = 1;
const unsigned char CSkeletonNode::ymovable_ = 2;
#if DIM==3
const unsigned char CSkeletonNode::zmovable_ = 4;
const unsigned char CSkeletonNode::unpinned_ = 8;
#else
const unsigned char CSkeletonNode::unpinned_ = 4;
#endif

const std::string CSkeletonNode::modulename_("ooflib.SWIG.engine.cskeletonnode2");
const std::string CSkeletonNode::classname_("CSkeletonNode");

long CSkeletonNode::globalNodeCount = 0; // used for testing
static SLock globalNodeCountLock;

CSkeletonNode::CSkeletonNode(int idx, vtkSmartPointer<vtkPoints> pts)
  : CSkeletonSelectable(),
    index(idx), 
    points(pts),
    mobility(xmovable_|ymovable_|zmovable_|unpinned_)
{
  // oofcerr << "CSkeletonNode::ctor: " << this << " index=" << index
  // 	  << " uid=" << uid
  // 	  << " position=" << getPosition()
  // 	  << std::endl;
  elements = new CSkeletonElementVector;
  globalNodeCountLock.acquire();
  ++globalNodeCount;
  globalNodeCountLock.release();
}

CSkeletonNode::~CSkeletonNode() {
  // oofcerr << "CSkeletonNode::dtor: " << this << std::endl;
  delete elements;
  globalNodeCountLock.acquire();
  --globalNodeCount;
  globalNodeCountLock.release();
}

long get_globalNodeCount() {
  return CSkeletonNode::globalNodeCount;
}

// TODO 3.1: Get rid of this.  Use position instead.
Coord CSkeletonNode::getPosition() const {
  Coord pos;
  points->GetPoint(index, pos);
  return pos;
}

Coord CSkeletonNode::position() const {
  Coord pos;
  points->GetPoint(index, pos);
  return pos;
}

CSkeletonNode *CSkeletonNode::new_child(int idx, vtkSmartPointer<vtkPoints> pts)
{
  CSkeletonNode *child = new CSkeletonNode(idx, pts);
  child->copyMobility(this);
  return child;
}

// CSkeletonNode *CSkeletonNode::copy_child(int idx,
// 					 vtkSmartPointer<vtkPoints> pts)
// {
//   CSkeletonNode *child = dynamic_cast<CSkeletonNode*>(
// 			      CSkeletonSelectable::copy_child(idx, pts));
//   child->nodemoved = nodemoved;
//   child->lastmoved = lastmoved;
//   for(int i=0; i<DIM; i++)
//     child->last_position[i] = last_position[i];
//   return child;
// }

void CSkeletonNode::setMobilityX(bool mob) {
  if(mob)
    mobility |= xmovable_;
  else
    mobility &= ~xmovable_;
}

void CSkeletonNode::setMobilityY(bool mob) {
  if(mob)
    mobility |= ymovable_;
  else
    mobility &= ~ymovable_;
}

#if DIM==3
void CSkeletonNode::setMobilityZ(bool mob) {
  if(mob)
    mobility |= zmovable_;
  else
    mobility &= ~zmovable_;
}
#endif

void CSkeletonNode::copyMobility(CSkeletonNode *source) {
  this->mobility = source->mobility;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CPinnedNodeTracker::CPinnedNodeTracker(CSkeletonBase *s)
  : skeleton(s)
{
  // oofcerr << "CPinnedNodeTracker::ctor: this=" << this << std::endl;
}

CDeputyPinnedNodeTracker::CDeputyPinnedNodeTracker(CSkeletonBase *s)
  : CPinnedNodeTracker(s)
{
  // oofcerr << "CDeputyPinnedNodeTracker::ctor: this=" << this << std::endl;
}

const std::string &CPinnedNodeTracker::classname() const {
  static const std::string nm("CPinnedNodeTracker");
  return nm;
}

const std::string &CDeputyPinnedNodeTracker::classname() const {
  static const std::string nm("CDeputyPinnedNodeTracker");
  return nm;
}

const std::string &CPinnedNodeTracker::modulename() const {
  static const std::string m("ooflib.SWIG.engine.cskeletonnode2");
  return m;
}

std::ostream &operator<<(std::ostream &os, const CPinnedNodeTracker &cpnt) {
  return os << cpnt.printself();
}

std::string CPinnedNodeTracker::printself() const {
  return std::string("CPinnedNodeTracker(" + to_string(this) + ")");
}

std::string CDeputyPinnedNodeTracker::printself() const { 
  return std::string("CDeputyPinnedNodeTracker(" + to_string(this) + ")");
}

CPinnedNodeTracker* CPinnedNodeTracker::clone() const {
  CPinnedNodeTracker* shakes = new CPinnedNodeTracker(skeleton);
  shakes->data.insert(data.begin(), data.end());
  return shakes;
}

CPinnedNodeTracker* CDeputyPinnedNodeTracker::clone() const {
  CPinnedNodeTracker* shakes = new CDeputyPinnedNodeTracker(skeleton);
  shakes->get()->insert(data.begin(), data.end());
  return shakes;
}

void CPinnedNodeTracker::clear() {
  for(CSkeletonSelectableSet::iterator it=data.begin(); it!=data.end(); ++it) 
    dynamic_cast<CSkeletonNode*>(*it)->setPinned(false);
  data.clear();
}

void CPinnedNodeTracker::clearskeleton() {
  for(CSkeletonSelectableSet::iterator it=data.begin(); it!=data.end(); ++it) 
    dynamic_cast<CSkeletonNode*>(*it)->setPinned(false);
}

void CPinnedNodeTracker::write() {
  for(CSkeletonSelectableSet::iterator it=data.begin(); it!=data.end(); ++it) 
    dynamic_cast<CSkeletonNode*>(*it)->setPinned(true);
}

Coord CPinnedNodeTracker::nodePosition(CSkeletonNode *n) {
  // CSkeleton::nodePositionForSkeleton() returns the position of the
  // node in the skeleton even if the skeleton has an active deputy.
  return skeleton->nodePositionForSkeleton(n);
}
                    
void CPinnedNodeTracker::implied_pin(CPinnedNodeTracker *other) {
  // "this" is the tracker for a new CSkeleton.  "other" is the
  // tracker for the parent CSkeleton.  Nodes in the new CSkeleton are
  // pinned only if they have a pinned parent in the old CSkeleton,
  // and the parent and child are at the same location.
  for(CSkeletonSelectableSet::iterator it = other->get()->begin(); 
      it != other->get()->end(); ++it)
    {
      Coord x = nodePosition(dynamic_cast<CSkeletonNode*>(*it));
      for(CSkeletonSelectableList::iterator cit = (*it)->getChildren().begin();
	  cit != (*it)->getChildren().end(); ++cit)
	{
	  if(x == nodePosition(dynamic_cast<CSkeletonNode*>(*it)))
	    add(dynamic_cast<CSkeletonNode*>(*cit));
	}
    }
}

void CDeputyPinnedNodeTracker::implied_pin(CPinnedNodeTracker *other) {
  for(CSkeletonSelectableSet::iterator it = other->get()->begin(); 
      it != other->get()->end(); ++it)
    {
      Coord y = other->nodePosition(dynamic_cast<CSkeletonNode*>(*it));
      Coord x = nodePosition(dynamic_cast<CSkeletonNode*>(*it));
      if(x == y)
	add(dynamic_cast<CSkeletonNode*>(*it));
    }
}

void CSkeletonNode::setPinned(bool pin) {
  if(pin)
    mobility &= ~unpinned_;
  else
    mobility |= unpinned_;
}

//  pin and unpin are analogous to select and deselect in the
//  SkeletonSelectable class.  They pin and unpin this node and its
//  children and parents.  The cvector and pvector args are lists of
//  trackers corresponding to the children and parents in the
//  SkeletonContext's stack of skeletons.  Some of those Skeletons may
//  be DeputySkeletons, which share nodes instead of having
//  parent/child nodes.  For those Skeletons the tracker is a
//  DeputyPinnedNodeTracker instead of a PinnedNodeTracker.

// Pinning is sufficiently different from selecting that the two
// operations don't share any code.  The differences are in how the
// pinning state propagates from a CSkeleton to its parent or
// children.  A change in pinned state propagates from a node in one
// CSkeleton to a node in another only if the two nodes are at the
// same position.  Because nodes in deputy skeletons can be at
// different positions, the pinned state is non-trivial for deputies,
// in contrast to the selection state, which is always the same in a
// deputy and its sheriff.

void CPinnedNodeTracker::add(CSkeletonNode *n) {
  data.insert(n);
}

void CPinnedNodeTracker::remove(CSkeletonNode *n) {
  data.erase(n);
}

void CSkeletonNode::pin(CPinnedNodeTrackerVector *cvector,
			CPinnedNodeTrackerVector *pvector)
{
  setPinned(true);
  Coord x = position();
  pinChildren(cvector->begin(), cvector->end(), x);
  pinParents(pvector->begin(), pvector->end(), x);
}

//=\\=//=\\=//

void CSkeletonNode::pinChildren(CPinnedNodeTrackerVector::iterator begin,
				CPinnedNodeTrackerVector::iterator end,
				const Coord &x) 
{
  // Checking that the actual node position is x is done by the
  // tracker, not here, because the position depends on the skeleton.
  (*begin)->add(this);
  CPinnedNodeTrackerVector::iterator nexttracker = begin + 1;
  if(nexttracker != end)
    (*nexttracker)->pinChildren(this, nexttracker, end, x);
}

void CPinnedNodeTracker::pinChildren(CSkeletonNode *node,
				     CPinnedNodeTrackerVector::iterator begin,
				     CPinnedNodeTrackerVector::iterator end,
				     const Coord &x)
{
  // "node" is from the previous (parent) tracker.  Its children are
  // pinned by this tracker.  The loop over children is done by this
  // tracker and not the previous one, because if this tracker were a
  // deputy it would just reuse the node and not pin the children.
  for(CSkeletonSelectableList::iterator i=node->getChildren().begin();
      i!=node->getChildren().end(); ++i)
    {
      CSkeletonNode *nextnode = dynamic_cast<CSkeletonNode*>(*i);
      // Only continue to pin if the position of the node in this
      // tracker's skeleton is the same as the position in the
      // skeleton where the pinning originally occurred.
      if(nodePosition(nextnode) == x) {
	nextnode->pinChildren(begin, end, x);
      }
    }
}

void CDeputyPinnedNodeTracker::pinChildren(
				   CSkeletonNode *node,
				   CPinnedNodeTrackerVector::iterator begin,
				   CPinnedNodeTrackerVector::iterator end,
				   const Coord &x)
{
  // "node" is from the previous (parent) tracker, but because this
  // tracker is a deputy, the same node should be pinned in this
  // tracker.
  if(nodePosition(node) == x)
    node->pinChildren(begin, end, x);
}

//=\\=//=\\=//

// The asymmetry between the pinParents and pinChildren routines is because
// deputies are always children of their sheriffs.

void CSkeletonNode::pinParents(CPinnedNodeTrackerVector::iterator begin,
			       CPinnedNodeTrackerVector::iterator end,
			       const Coord &x) 
{
  if(begin == end || (*begin)->nodePosition(this) != x)
    return;
  (*begin)->add(this); 
  (*begin)->pinParents(this, begin, end, x);
}

void CPinnedNodeTracker::pinParents(CSkeletonNode *node,
				    CPinnedNodeTrackerVector::iterator begin,
				    CPinnedNodeTrackerVector::iterator end,
				    const Coord &x)
{
  for(CSkeletonSelectableList::iterator i=node->getParents().begin();
      i!=node->getParents().end(); ++i)
    {
      CSkeletonNode *nextnode = dynamic_cast<CSkeletonNode*>(*i);
      nextnode->pinParents(begin+1, end, x);
    }
}

void CDeputyPinnedNodeTracker::pinParents(
				  CSkeletonNode *node,
				  CPinnedNodeTrackerVector::iterator begin,
				  CPinnedNodeTrackerVector::iterator end,
				  const Coord &x)
{
  if(nodePosition(node) == x)
    node->pinParents(begin+1, end, x);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonNode::unpin(CPinnedNodeTrackerVector *cvector,
			CPinnedNodeTrackerVector *pvector)
{
  setPinned(false);
  Coord x = position();
  unpinChildren(cvector->begin(), cvector->end(), x);
  unpinParents(pvector->begin(), pvector->end(), x);
}

//=\\=//=\\=//

void CSkeletonNode::unpinChildren(CPinnedNodeTrackerVector::iterator begin,
				  CPinnedNodeTrackerVector::iterator end,
				  const Coord &x)
{
  (*begin)->remove(this);
  CPinnedNodeTrackerVector::iterator nexttracker = begin + 1;
  if(nexttracker != end)
    (*nexttracker)->unpinChildren(this, begin, end, x);
}

void CPinnedNodeTracker::unpinChildren(CSkeletonNode *node,
				       CPinnedNodeTrackerVector::iterator begin,
				       CPinnedNodeTrackerVector::iterator end,
				       const Coord &x)
{
  for(CSkeletonSelectableList::iterator i=node->getChildren().begin();
      i!=node->getChildren().end(); ++i)
    {
      CSkeletonNode *nextnode = dynamic_cast<CSkeletonNode*>(*i);
      if(nodePosition(nextnode) == x) {
	nextnode->unpinChildren(begin, end, x);
      }
    }
}

void CDeputyPinnedNodeTracker::unpinChildren(
				     CSkeletonNode *node,
				     CPinnedNodeTrackerVector::iterator begin,
				     CPinnedNodeTrackerVector::iterator end,
				     const Coord &x)
{
  if(nodePosition(node) == x)
    node->unpinChildren(begin, end, x);
}

//=\\=//=\\=//

void CSkeletonNode::unpinParents(CPinnedNodeTrackerVector::iterator begin,
				 CPinnedNodeTrackerVector::iterator end,
				 const Coord &x) 
{
  if(begin == end || (*begin)->nodePosition(this) != x)
    return;
  (*begin)->remove(this); 
  (*begin)->unpinParents(this, begin, end, x);
}

void CPinnedNodeTracker::unpinParents(
			      CSkeletonNode *node,
			      CPinnedNodeTrackerVector::iterator begin,
			      CPinnedNodeTrackerVector::iterator end,
			      const Coord &x)
{
  for(CSkeletonSelectableList::iterator i=node->getParents().begin();
      i!=node->getParents().end(); ++i)
    {
      CSkeletonNode *nextnode = dynamic_cast<CSkeletonNode*>(*i);
      nextnode->unpinParents(begin+1, end, x);
    }
}

void CDeputyPinnedNodeTracker::unpinParents(
				    CSkeletonNode *node,
				    CPinnedNodeTrackerVector::iterator begin,
				    CPinnedNodeTrackerVector::iterator end,
				    const Coord &x)
{
  if(nodePosition(node) == x)
    node->unpinParents(begin+1, end, x);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility functions used when pinning nodes of a set of elements.
// TODO MER: These functions are duplicates of ones in SkeletonContext:
// exteriorNodesOfElementSet, etc.  Do we need both?

static void getAllElementNodes(const CSkeletonSelectableSet *els,
			       CSkeletonNodeSet &nodes) 
{
  CSkeletonElement *el;
  for(CSkeletonSelectableSet::iterator it=els->begin(); it!=els->end(); ++it) {
    el = (dynamic_cast<CSkeletonElement*>(*it));
    for(unsigned int i=0; i<el->nnodes(); ++i)
      nodes.insert(el->getNode(i));
  }
}

static void getBoundaryNodes(const CSkeletonBase *skel,
			     const CSkeletonSelectableSet *els,
			     CSkeletonNodeSet &nodes)
{
  // The boundary nodes are on exterior faces.  Exterior faces are
  // faces that have only one element in the given set.

  // First, count the faces by looping over elements.
  typedef std::map<CSkeletonFace*, int> FaceCounts;
  FaceCounts facecounts;
  for(CSkeletonSelectableSet::iterator e=els->begin(); e!=els->end(); ++e) {
    CSkeletonElement *el = dynamic_cast<CSkeletonElement*>(*e);
    for(unsigned int f=0; f<el->getNumberOfFaces(); ++f) {
      CSkeletonFace *face = skel->getElementFace(el, f);
      FaceCounts::iterator fi = facecounts.find(face);
      if(fi == facecounts.end())
	facecounts[face] = 1;
      else
	(*fi).second += 1;
    }
  }
  // Loop over the faces that are only on one element and put their
  // nodes in the node set.
  for(FaceCounts::iterator fi = facecounts.begin(); fi!=facecounts.end(); ++fi)
    {
      if((*fi).second == 1) {	// face is external
	CSkeletonFace *face = (*fi).first;
	for(unsigned int n=0; n<face->nnodes(); n++) {
	  nodes.insert(face->getNode(n));
	}
      }
    }
}

static void getInternalNodes(const CSkeletonBase *skel,
			     const CSkeletonSelectableSet *els,
			     CSkeletonNodeSet &nodes)
{
  CSkeletonNodeSet all, boundary;
  getAllElementNodes(els, all);
  getBoundaryNodes(skel, els, boundary);
  std::set_difference(all.begin(), all.end(), boundary.begin(), boundary.end(),
   		      std::inserter(nodes, nodes.end()),
		      CSkeletonNodeSet::key_compare());
}


void CSkeletonNode::pinSet(CSkeletonNodeSet *nset,
			   CPinnedNodeTrackerVector *cvector,
			   CPinnedNodeTrackerVector *pvector)
{
  for(CSkeletonNodeSet::iterator it=nset->begin(); it!=nset->end(); ++it) {
    (*it)->pin(cvector, pvector);
    //            for partner in n.getPartners():
    //                 partner.pin(clist, plist)
  }
}

void CSkeletonNode::pinSet(CSkeletonSelectableSet *sset,
			   CPinnedNodeTrackerVector *cvector, 
			   CPinnedNodeTrackerVector *pvector)
{
  for(CSkeletonSelectableSet::iterator it = sset->begin(); it != sset->end();
      ++it)
    {
      (dynamic_cast<CSkeletonNode*>(*it))->pin(cvector, pvector);
      //            for partner in n.getPartners():
      //                 partner.pin(clist, plist)
    }
}

// static
void CSkeletonNode::pinSelection(CSelectionTrackerBase *tracker, 
				 CPinnedNodeTrackerVector *cvector,
				 CPinnedNodeTrackerVector *pvector) 
{
  pinSet(tracker->get(), cvector, pvector);
}


void CSkeletonNode::unpinSet(CSkeletonNodeSet *nset,
			     CPinnedNodeTrackerVector *cvector,
			     CPinnedNodeTrackerVector *pvector) 
{
  for(CSkeletonNodeSet::iterator it = nset->begin(); it != nset->end(); ++it) {
    (*it)->unpin(cvector, pvector);
    //            for partner in n.getPartners():
    //                 partner.unpin(clist, plist)
  }
}

void CSkeletonNode::unpinSet(CSkeletonSelectableSet *sset,
			     CPinnedNodeTrackerVector *cvector,
			     CPinnedNodeTrackerVector *pvector) 
{
  for(CSkeletonSelectableSet::iterator it=sset->begin(); it!=sset->end(); ++it)
    {
      (dynamic_cast<CSkeletonNode*>(*it))->unpin(cvector, pvector);
      //            for partner in n.getPartners():
      //                 partner.unpin(clist, plist)
    }
}

// static
void CSkeletonNode::unpinSelection(CSelectionTrackerBase *tracker, 
				   CPinnedNodeTrackerVector *cvector,
				   CPinnedNodeTrackerVector *pvector) 
{
  unpinSet(tracker->get(), cvector, pvector);
}

// static
void CSkeletonNode::pinSelectedSegments(CSelectionTrackerBase *tracker, 
					CPinnedNodeTrackerVector *cvector,
					CPinnedNodeTrackerVector *pvector) 
{
  CSkeletonSegment *seg;
  CSkeletonNodeSet nodes;
  for(CSkeletonSelectableSet::iterator it=tracker->get()->begin();
      it!=tracker->get()->end(); ++it) 
    {
      seg = (dynamic_cast<CSkeletonSegment*>(*it));
      nodes.insert(seg->getNode(0));
      nodes.insert(seg->getNode(1));
    }
  pinSet(&nodes, cvector, pvector);
}

// static
void CSkeletonNode::pinSelectedElements(CSelectionTrackerBase *tracker, 
					CSkeletonBase *skel,
					bool internal, bool boundary,
					CPinnedNodeTrackerVector *cvector,
					CPinnedNodeTrackerVector *pvector) 
{
  CSkeletonNodeSet nodes;
  if(internal and boundary)
    getAllElementNodes(tracker->get(), nodes);
  else if(not internal and boundary)
    getBoundaryNodes(skel, tracker->get(), nodes);
  else if(internal and not boundary)
    getInternalNodes(skel, tracker->get(), nodes);
  pinSet(&nodes, cvector, pvector);
}


// TODO OPT: use skeleton function
// static
void CSkeletonNode::pinInternalBoundaryNodes(CSkeletonBase *skel,
					     CPinnedNodeTrackerVector *cvector, 
					     CPinnedNodeTrackerVector *pvector) 
{
  CSkeletonNodeSet nodes;
  skel->getInternalBoundaryNodes(nodes);
  // oofcerr << "number in set of internal nodes " << nodes.size() << endl;
  pinSet(&nodes, cvector, pvector);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

 bool CSkeletonNode::active(const CSkeletonBase *skeleton)  const {
   return skeleton->getMicrostructure()->isActive(position());
 }

 //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonNode::unconstrainedMoveTo(const Coord &pos) {
  lastmoved = nodemoved;
  points->GetPoint(index, last_position);
   // points->SetPoint(index, pos[0], pos[1], pos[2]);
   points->SetPoint(index, pos);
   ++nodemoved;
 }

 bool CSkeletonNode::moveTo(const Coord &pos) {
   double x,y,z;
   lastmoved = nodemoved;
   points->GetPoint(index,last_position);
   if(movable_x())
     x = pos[0];
   else 
     x = last_position[0];
   if(movable_y())
     y = pos[1];
   else
     y = last_position[1];
   if(movable_z()) 
     z = pos[2];
   else
     z = last_position[2];
   points->SetPoint(index, x, y, z);
   if( !(x==last_position[0] && y==last_position[1] && z==last_position[2]) ) {
     ++nodemoved;
     return true;
   }  
   return false;
 }

 bool CSkeletonNode::moveBy(const Coord &disp) {
   double x,y,z;
   lastmoved = nodemoved;
   points->GetPoint(index,last_position);
   if(movable_x())
     x = last_position[0] + disp[0];
   else
     x = last_position[0];
   if(movable_y())
     y = last_position[1] + disp[1];
   else
     y = last_position[1];
   if(movable_z()) 
     z = last_position[2] + disp[2];
   else 
     z = last_position[2];
   points->SetPoint(index, x, y, z);
   if( !(x==last_position[0] && y==last_position[1] && z==last_position[2]) ) {
     ++nodemoved;
     return true;
   }  
   return false;
 }

 bool CSkeletonNode::canMoveTo(const Coord &pos) const {
 // #if DIM==2
 //   return ((movable_x() || position_.x == pos->x) &&
 // 	  (movable_y() || position_.y == pos->y));
 // #elif DIM==3
   Coord currentpos = position();
   return ((movable_x() || currentpos[0] == pos[0]) &&
	   (movable_y() || currentpos[1] == pos[1]) &&
	   (movable_z() || currentpos[2] == pos[2]));
   //#endif
 }

 void CSkeletonNode::moveBack() {
   nodemoved = lastmoved;
   points->SetPoint(index,last_position);
   for(CSkeletonElementIterator it=elements->begin(); it!=elements->end(); ++it)
     (*it)->revertHomogeneity();
 }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Can this node be moved to and merge with another node?
bool CSkeletonNode::canMergeWith(const CSkeletonNode *other) const {
#if DIM==2
  bool xmovable = movable_x();
  bool ymovable = movable_y();
  if(!xmovable && !ymovable)
    return false;
  else if(!xmovable && ymovable)
    return position_.x == other->position_.x;
  else if(xmovable && !ymovable)
    return position_.y == other->position_.y;
  return true;
#elif DIM==3
  bool movables[3] = {movable_x(), movable_y(), movable_z()};
  bool canmerge = 1;
  Coord pos;
  Coord otherpos;
  points->GetPoint(index, pos);
  points->GetPoint(other->index, otherpos);
  for(int i=0; i<DIM; i++) 
    canmerge &= ( movables[i] || pos[i] == otherpos[i]); 
  return canmerge;
#endif
}

// A node is illegal if any of its elements are illegal.  This
// is used when testing possible node motions, so it's assumed
// that the node being tested is the one causing the elements
// to be illegal.
bool CSkeletonNode::illegal() const {
  for(CSkeletonElementIterator it = elements->begin(); it != elements->end(); ++it)
    if((*it)->illegal())
      return true;
  return false;
}

vtkSmartPointer<vtkCell> CSkeletonNode::getVtkCell() const {
  vtkSmartPointer<vtkCell> cell = vtkSmartPointer<vtkVertex>::New();
  Coord x;
  cell->GetPointIds()->SetId(0,0); //index);
  x = position();
  cell->GetPoints()->SetPoint(0,x.xpointer());
  return cell;
}

VTKCellType CSkeletonNode::getCellType() const { return VTK_VERTEX; }

vtkSmartPointer<vtkIdList> CSkeletonNode::getPointIds() const {
  vtkSmartPointer<vtkIdList> list = vtkSmartPointer<vtkIdList>::New();
  list->SetNumberOfIds(1);
  list->SetId(0,index);
  return list;
}

// the hashes use the uids so that the maps stay valid as the indices
// change when nodes are removed.
// The python tuple hash according to: http://effbot.org/zone/python-hash.htm
// TODO OPT: look out for possible collisions, especially in 64-bit.
// int hash2(const CSkeletonNode *n1, const CSkeletonNode *n2) {
//   int corned_beef = 0x345678; // 0x345678
//   corned_beef *= 1000003;
//   corned_beef ^= n1->getUid();
//   corned_beef *= 1000003;
//   corned_beef ^= n2->getUid();
//   return corned_beef;
// }

// int CSkeletonNode::hash(const CSkeletonNode *n1, const CSkeletonNode *n2) {
//   int corned_beef = 0;
//   if(*n1<*n2)
//     corned_beef = hash2(n1,n2);
//   else
//     corned_beef = hash2(n2,n1);
//   corned_beef ^= 2;
//   return corned_beef;
// }

// int CSkeletonNode::hash(const CSkeletonNode *n1, const CSkeletonNode *n2, const CSkeletonNode *n3) {
//   int corned_beef = 0;
//   if(*n3>*n1 && *n3>*n2) {
//     if(*n1<*n2)
//       corned_beef = hash2(n1,n2);
//     else
//       corned_beef = hash2(n2,n1);
//     corned_beef *= 1000003;
//     corned_beef ^= n3->getUid();
//   }
//   else if(*n2>*n1 && *n2>*n3) {
//     if(*n1<*n3)
//       corned_beef = hash2(n1,n3);
//     else
//       corned_beef = hash2(n3,n1);
//     corned_beef *= 1000003;
//     corned_beef ^= n2->getUid();
//   }
//   else if(*n1>*n2 && *n1>*n3) {
//     if(*n2<*n3)
//       corned_beef = hash2(n2,n3);
//     else
//       corned_beef = hash2(n3,n2);
//     corned_beef *= 1000003;
//     corned_beef ^= n1->getUid();
//   }
//   corned_beef ^= 3;
//   return corned_beef;
// }

void CSkeletonNode::removeElement(CSkeletonElement *el, CSkeleton *skel) {
  for(CSkeletonElementVector::iterator it=elements->begin();
      it!=elements->end(); ++it)
    {
      if( (*it)->getUid() == el->getUid() ) {
	elements->erase(it);
	break;
      }
    } 
  if(elements->empty())
    skel->removeNode(this);
}

void CSkeletonNode::addElement(CSkeletonElement* el) {
  assert(!defunct);
  elements->push_back(el);
}

bool CSkeletonNode::hasElement(CSkeletonElement* el) {
  return std::find_if(elements->begin(), elements->end(), FindUid(el->getUid()))
    != elements->end();
}

void CSkeletonNode::getElements(const CSkeletonBase*,
				ConstCSkeletonElementVector &result)
  const
{
  result.resize(elements->size());
  for(unsigned int i=0; i<elements->size(); ++i)
    result[i] = (*elements)[i];
}

void CSkeletonNode::getElements(const CSkeletonBase*,
				CSkeletonElementVector &result)
{
  result.resize(elements->size());
  for(unsigned int i=0; i<elements->size(); ++i)
    result[i] = (*elements)[i];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void CSkeletonNode::print(std::ostream &os) const {
  os << "Node " << position()<< " " << uid << " " << index;
}


int CSkeletonNode::dominantPixel(const CMicrostructure *ms) const {
  return ms->category(getPosition());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const CSkeletonMultiNodeKey &key) {
  os << "CSkeletonMultiNodeKey(";
  for(UidVector::const_iterator i=key.uids.begin(); i<key.uids.end(); ++i) {
    if(i != key.uids.begin())
      os << ", ";
    os << *i;
  }
  os << ")";
  return os;
}
