// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/IO/oofcerr.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletongroups.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonselectable.h"
#include "engine/skeletonselectioncourier.h"

SkeletonSelectionCourier::SkeletonSelectionCourier(
				   CSkeletonBase *skel,
				   CSelectionTrackerVector *clist,
				   CSelectionTrackerVector *plist)
  : skeleton(skel),
    // Using std::move is crucial here.  The input vectors are created
    // by the CSelectionTrackerVector swig typemap and go out of scope
    // when the constructor's wrapper exits.
    clist(std::move(*clist)),
    plist(std::move(*plist)),
    done_(false)
{
}

void SkeletonSelectionCourier::select() {
  start();
  while(!done()) {
    CSkeletonSelectable *obj = currentObj();
    if(obj->active(skeleton))
      obj->select(&clist, &plist);
    next();
  }
}

void SkeletonSelectionCourier::deselect() {
  start();
  while(!done()) {
    CSkeletonSelectable *obj = currentObj();
    if(obj->active(skeleton))
      obj->deselect(&clist, &plist);
    next();
  }
}

void SkeletonSelectionCourier::toggle() {
  start();
  while(!done()) {
    CSkeletonSelectable *obj = currentObj();
    if(obj->active(skeleton)) {
      if(obj->isSelected())
	obj->deselect(&clist, &plist);
      else
	obj->select(&clist, &plist);
    }
    next();
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SkeletonGroupCourier::SkeletonGroupCourier(CSkeletonBase *skel,
					   const std::string &name,
					   const CGroupTrackerBase *tracker,
					   CSelectionTrackerVector *clist,
					   CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist),
    groupTracker(tracker),
    groupName(name)
{}

void SkeletonGroupCourier::start() {
  // group is a CSkeletonSelectableSet*, which is a std::set* of
  // CSkeletonSelectable*s.
  group = groupTracker->get_group(groupName);
  done_ = (group->size() == 0);
  iter = group->begin();
}

void SkeletonGroupCourier::next() {
  ++iter;
  done_ = (iter == group->end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// SingleObjectCourier can be used to select a single element, face,
// segment, or node.

SingleObjectCourier::SingleObjectCourier(CSkeletonBase *skeleton,
					 CSkeletonSelectable *obj,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skeleton, clist, plist),
    object(obj)
{}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// NodeSelection methods which compute and store a set of nodes in
// their constructor are derived from NodeSelectionCourier.

NodeSelectionCourier::NodeSelectionCourier(CSkeletonBase *skel,
					   CSelectionTrackerVector *clist,
					   CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist)
{}

void NodeSelectionCourier::start() {
  iter = selectedNodes.begin();
  done_ = (iter == selectedNodes.end());
}

void NodeSelectionCourier::next() {
  ++iter;
  done_ = (iter == selectedNodes.end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

NodesFromOtherCourier::NodesFromOtherCourier(
			CSkeletonBase *skel,
			const std::string *cvrage,
			const CSelectionTracker *oTracker,
			CSelectionTrackerVector *clist,
			CSelectionTrackerVector *plist)
  : NodeSelectionCourier(skel, clist, plist),
    coverage(*cvrage),
    otherTracker(oTracker)
{}

void NodesFromOtherCourier::start() {
  // coverage is a string because it comes from a Python Enum via swig.
  if(coverage == std::string("Exterior")) {
    selectedNodes = exteriorNodes();
  }
  else if(coverage == std::string("Interior")) {
    CSkeletonNodeSet allnodes = allNodes();
    CSkeletonNodeSet extnodes = exteriorNodes();
    std::set_difference(allnodes.begin(), allnodes.end(),
			extnodes.begin(), extnodes.end(),
			std::inserter(selectedNodes, selectedNodes.end()));
  }
  else {
    assert(coverage == std::string("All"));
    selectedNodes = allNodes();
  }
  NodeSelectionCourier::start();
}

CSkeletonNodeSet NodesFromOtherCourier::allNodes() const
{
  CSkeletonNodeSet allnodes;	// all nodes of selected others
  const CSkeletonSelectableSet *others = otherTracker->get(); 
  for(const CSkeletonSelectable *other : *others) {
    const CSkeletonMultiNodeSelectable *otherM =
      dynamic_cast<const CSkeletonMultiNodeSelectable*>(other);
    const CSkeletonNodeVector *elnodes = otherM->getNodes();
    allnodes.insert(elnodes->begin(), elnodes->end());
  }
  return allnodes;
}

//----------

NodesFromElementsCourier::NodesFromElementsCourier(
				   CSkeletonBase *skel,
				   const std::string *coverage,
				   const CSelectionTracker *otherTracker,
				   CSelectionTrackerVector *clist,
				   CSelectionTrackerVector *plist)
  : NodesFromOtherCourier(skel, coverage, otherTracker, clist, plist)
{}

CSkeletonNodeSet NodesFromElementsCourier::exteriorNodes() const
{
  // A node is on the exterior of the element selection if it is on
  // a boundary face of the element selection.  A boundary face is
  // one that has only one selected neighboring element.
  const CSkeletonSelectableSet *elements = otherTracker->get(); //selected els
  CSkeletonFaceSet faces;	// exterior faces
  // Loop over the selected elements, and put each face in faces if
  // it's not already there.  If it is already there, it's not a
  // boundary face, so take it out.
  for(const CSkeletonSelectable *elmnt : *elements) {
    const CSkeletonElement *el = dynamic_cast<const CSkeletonElement*>(elmnt);
    for( int i=0; i<el->getNumberOfFaces(); i++) {
      CSkeletonFace *face = skeleton->getFace(el->getFaceKey(i));
      // If a face is already in exet
      if(faces.count(face) == 0) {
	faces.insert(face);
      }
      else {
	faces.erase(face);
      }
    }
  }
  CSkeletonNodeSet extnodes;
  for(CSkeletonFace *face : faces) {
    const CSkeletonNodeVector *facenodes = face->getNodes();
    extnodes.insert(facenodes->begin(), facenodes->end());
  }
  return extnodes;
}

//-----------

NodesFromFacesCourier::NodesFromFacesCourier(
				     CSkeletonBase *skel,
				     const std::string *coverage,
				     const CSelectionTracker *otherTracker,
				     CSelectionTrackerVector *clist,
				     CSelectionTrackerVector *plist)
  : NodesFromOtherCourier(skel, coverage, otherTracker, clist, plist)
{}


CSkeletonNodeSet NodesFromFacesCourier::exteriorNodes() const {
  // Exterior nodes are the nodes that are on segments belonging to
  // only one face in the set of selected faces.  Otherwise this is
  // just like NodesFromElementsCourier::exteriorNodes().
  const CSkeletonSelectableSet *faces = otherTracker->get();
  CSkeletonSegmentSet segments; // exterior segments
  for(const CSkeletonSelectable *f : *faces) {
    const CSkeletonFace *face = dynamic_cast<const CSkeletonFace*>(f);
    int nn = face->nnodes();
    for(int i=0; i<nn; i++) {
      const CSkeletonNode *n0 = face->getNode(i);
      const CSkeletonNode *n1 = face->getNode((i+1)%nn);
      CSkeletonSegment *segment = skeleton->findExistingSegment(n0, n1);
      if(segments.count(segment) == 0)
	segments.insert(segment);
      else
	segments.erase(segment);
    }
  }
  CSkeletonNodeSet extnodes;
  for(CSkeletonSegment *segment : segments) {
    const CSkeletonNodeVector *segnodes = segment->getNodes();
    extnodes.insert(segnodes->begin(), segnodes->end());
  }
  return extnodes;
}

//------------

// NodesFromSegmentsCourier is not derived from NodesFromOtherCourier
// because there's no way to differentiate between interior and
// exterior nodes.

NodesFromSegmentsCourier::NodesFromSegmentsCourier(
				   CSkeletonBase *skel,
				   const CSelectionTracker *segmentTracker,
				   CSelectionTrackerVector *clist,
				   CSelectionTrackerVector *plist)
  : NodeSelectionCourier(skel, clist, plist)
{
  const CSkeletonSelectableSet *segments = segmentTracker->get();
  for(const CSkeletonSelectable *sg : *segments) {
    const CSkeletonSegment *segment = dynamic_cast<const CSkeletonSegment*>(sg);
    selectedNodes.insert(segment->getNode(0));
    selectedNodes.insert(segment->getNode(1));
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CategoryElementCourier::CategoryElementCourier(
					       CSkeletonBase *skel,
					       int cat,
					       CSelectionTrackerVector *clist,
					       CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist),
    category(cat)
{}

void CategoryElementCourier::skipOthers() {
  // Skip over elements that have the wrong category.
  while(iter != skeleton->endElements() &&
	(*iter)->dominantPixel(skeleton) != category) {
    ++iter;
  }
  done_ = (iter == skeleton->endElements());
}

void CategoryElementCourier::start() {
  iter = skeleton->beginElements();
  skipOthers();
}

void CategoryElementCourier::next() {
  iter++;
  skipOthers();
}
