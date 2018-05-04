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
#include "common/cmicrostructure.h"
#include "common/pixelgroup.h"
#include "common/random.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletongroups.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonselectable.h"
#include "engine/material.h"
#include "engine/skeletonselectioncourier.h"


// Some utility functions.

static
CSkeletonFaceSet internalBoundaryFaces(const CSkeletonBase *skel) {
  CSkeletonFaceSet faces;
  for(CSkeletonFaceIterator f=skel->beginFaces(); f!=skel->endFaces(); ++f) {
    CSkeletonFace *face = (*f).second;
    if(face->nElements() == 2 &&
       (face->getElement(skel, 0)->dominantPixel(skel) !=
	face->getElement(skel, 1)->dominantPixel(skel)))
      faces.insert(face);
  }
  return faces;
}

static
CSkeletonFaceSet exteriorFacesOfElements(const CSkeletonBase *skeleton,
					 const CSkeletonSelectableSet *els)
{
  // An exterior face of an element set is a face that's only part of
  // one element.
  CSkeletonFaceSet faces;
  for(const CSkeletonSelectable *ell : *els) {
    const CSkeletonElement *el = dynamic_cast<const CSkeletonElement*>(ell);
    for(int i=0; i<4; i++) {
      const CSkeletonMultiNodeKey fkey = el->getFaceKey(i);
      CSkeletonFace *face = skeleton->getFace(fkey);
      // Faces can't be part of more than two elements, so if this
      // face is already in the set, it's not exterior and we can
      // remove it.  We won't encounter it again and re-add it by
      // mistake.
      if(faces.count(face) == 0)
	faces.insert(face);
      else
	faces.erase(face);
    }
  }
  return faces;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


SkeletonSelectionCourier::SkeletonSelectionCourier(
				   const CSkeletonBase *skel,
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

// SkeletonGroupCourier works on a group of elements, faces, segments,
// or nodes.

SkeletonGroupCourier::SkeletonGroupCourier(const CSkeletonBase *skel,
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

SingleObjectCourier::SingleObjectCourier(const CSkeletonBase *skeleton,
					 CSkeletonSelectable *obj,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skeleton, clist, plist),
    object(obj)
{}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// IntersectionCourier loops over the intersection of the current
// selection (give as a CSelectionTracker) and the objects defined by
// the given courier.

IntersectionCourier::IntersectionCourier(CSelectionTracker *selection,
					 SkeletonSelectionCourier *courier)
  : SkeletonSelectionCourier(courier->skeleton, &courier->clist,
			     &courier->plist),
    oldSelection(*selection->get()) // copy!
{
  courier->start();
  while(!courier->done()) {
    courierObjs.insert(courier->currentObj());
    courier->next();
  }
}

bool IntersectionCourier::done() const {
  return (oldSelIter == oldSelection.end() || courierIter == courierObjs.end());
}

void IntersectionCourier::start() {
  oldSelIter = oldSelection.begin();
  courierIter = courierObjs.begin();
  advance();
}

void IntersectionCourier::next() {
  ++oldSelIter;
  ++courierIter;
  advance();
}

void IntersectionCourier::advance() {
  auto key_comp = oldSelection.key_comp();
  while(!done()) {
    if(key_comp(*oldSelIter, *courierIter)) {
      ++oldSelIter;
    }
    else if(key_comp(*courierIter, *oldSelIter)) {
      ++courierIter;
    }
    else {
      return;
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// StupidCourier copies a list of objects from Python to C++.  It's
// stupid because the whole point of the couriers is to avoid doing
// just that. It's useful for testing, and in hypothetical situations
// in which the source of the selected objects can't be easily
// accessed from C++.

StupidCourier::StupidCourier(const CSkeletonBase *skeleton,
			     CSkeletonSelectableVector *objs,
			     CSelectionTrackerVector *clist,
			     CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonSelectableVector>(skeleton, clist, plist)
{
  selectedObjects = std::move(*objs);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//            Node Selection Couriers
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

AllNodesCourier::AllNodesCourier(const CSkeletonBase *skel,
				 CSelectionTrackerVector *clist,
				 CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist)
{}

void AllNodesCourier::start() {
  iter = skeleton->beginNodes();
  done_ = (iter == skeleton->endNodes());
}

void AllNodesCourier::next() {
  ++iter;
  done_ = (iter == skeleton->endNodes());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

NodesFromOtherCourier::NodesFromOtherCourier(
			const CSkeletonBase *skel,
			const std::string *cvrage,
			const CSelectionTracker *oTracker,
			CSelectionTrackerVector *clist,
			CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonNodeSet>(skel, clist, plist),
    coverage(*cvrage),
    otherTracker(oTracker)
{}

void NodesFromOtherCourier::start() {
  // coverage is a string because it comes from a Python Enum via swig.
  if(coverage == std::string("Exterior")) {
    selectedObjects = exteriorNodes();
  }
  else if(coverage == std::string("Interior")) {
    CSkeletonNodeSet allnodes = allNodes();
    CSkeletonNodeSet extnodes = exteriorNodes();
    std::set_difference(allnodes.begin(), allnodes.end(),
			extnodes.begin(), extnodes.end(),
			std::inserter(selectedObjects, selectedObjects.end()));
  }
  else {
    assert(coverage == std::string("All"));
    selectedObjects = allNodes();
  }
  BulkSkelSelCourier<CSkeletonNodeSet>::start();
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
				   const CSkeletonBase *skel,
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
				     const CSkeletonBase *skel,
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
      CSkeletonSegment *segment = face->getSegment(skeleton, i);
      // const CSkeletonNode *n0 = face->getNode(i);
      // const CSkeletonNode *n1 = face->getNode((i+1)%nn);
      // CSkeletonSegment *segment = skeleton->findExistingSegment(n0, n1);
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
				   const CSkeletonBase *skel,
				   const CSelectionTracker *segmentTracker,
				   CSelectionTrackerVector *clist,
				   CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonNodeSet>(skel, clist, plist)
{
  const CSkeletonSelectableSet *segments = segmentTracker->get();
  for(const CSkeletonSelectable *sg : *segments) {
    const CSkeletonSegment *segment = dynamic_cast<const CSkeletonSegment*>(sg);
    selectedObjects.insert(segment->getNode(0));
    selectedObjects.insert(segment->getNode(1));
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ExpandNodeSelectionCourier::ExpandNodeSelectionCourier(
				       const CSkeletonBase *skel,
				       const CSelectionTracker *nodesel,
				       CSelectionTrackerVector *clist,
				       CSelectionTrackerVector *plist)
  : BulkSkelSelCourier(skel, clist, plist)
{
  const CSkeletonSelectableSet *nodes = nodesel->get(); // currently selected
  for(const CSkeletonSelectable *selectable : *nodes) {
    const CSkeletonNode *node = dynamic_cast<const CSkeletonNode*>(selectable);
    selectedObjects.insert(const_cast<CSkeletonNode*>(node));
    CSkeletonSegmentSet segs;
    skeleton->getNodeSegments(node, segs);
    for(CSkeletonSegment *segment : segs) {
      CSkeletonNode *otherNode = segment->get_other_node(node);
      selectedObjects.insert(otherNode);
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PointBoundaryCourier::PointBoundaryCourier(const CSkeletonBase *skel,
					   const CSkeletonPointBoundary *bdy,
					   CSelectionTrackerVector *clist,
					   CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist),
    nodes(bdy->getNodes())
{}

void PointBoundaryCourier::start() {
  iter = nodes->begin();
  done_ = (iter == nodes->end());
}

void PointBoundaryCourier::next() {
  ++iter;
  done_ = (iter == nodes->end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

InternalBoundaryNodesCourier::InternalBoundaryNodesCourier(
					   const CSkeletonBase *skel,
					   CSelectionTrackerVector *clist,
					   CSelectionTrackerVector *plist)
  : BulkSkelSelCourier(skel, clist, plist)
{
  for(CSkeletonNodeIterator node=skel->beginNodes(); node!=skel->endNodes();
      ++node)
    {
      // A node is on an internal boundary if not all of its Elements
      // have the same category.
      CSkeletonElementVector *elements = (*node)->getElements();
      int cat = (*elements)[0]->dominantPixel(skel);
      for(CSkeletonElement *element : *elements) {
	if(element->dominantPixel(skel) != cat) {
	  selectedObjects.insert(*node);
	  break;
	}
      }	// end loop over elements at a node
    } // end loop over nodes
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//        Segment Selection Couriers
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

AllSegmentsCourier::AllSegmentsCourier(const CSkeletonBase *skel,
				       CSelectionTrackerVector *clist,
				       CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist)
{}

void AllSegmentsCourier::start() {
  iter = skeleton->beginSegments();
  done_ = (iter == skeleton->endSegments());
}

void AllSegmentsCourier::next() {
  ++iter;
  done_ = (iter == skeleton->endSegments());
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SegmentsFromOtherCourier::SegmentsFromOtherCourier(
					 const CSkeletonBase *skel,
					 const std::string *cvrage,
					 const CSelectionTracker *oTracker,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonSegmentSet>(skel, clist, plist),
  coverage(*cvrage),
  otherTracker(oTracker)
{}

void SegmentsFromOtherCourier::start() {
  if(coverage == std::string("Exterior")) {
    selectedObjects = exteriorSegments();
  }
  else if(coverage == std::string("Interior")) {
    CSkeletonSegmentSet allsegs = allSegments();
    CSkeletonSegmentSet extsegs = exteriorSegments();
    std::set_difference(allsegs.begin(), allsegs.end(),
			extsegs.begin(), extsegs.end(),
			std::inserter(selectedObjects, selectedObjects.end()));
  }
  else {
    selectedObjects = allSegments();
  }
  BulkSkelSelCourier<CSkeletonSegmentSet>::start();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SegmentsFromElementsCourier::SegmentsFromElementsCourier(
					 const CSkeletonBase *skel,
					 const std::string *coverage,
					 const CSelectionTracker *otherTracker,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : SegmentsFromOtherCourier(skel, coverage, otherTracker, clist, plist)
{}

CSkeletonSegmentSet SegmentsFromElementsCourier::allSegments() const {
  CSkeletonSegmentSet segments;				       
  const CSkeletonSelectableSet *others = otherTracker->get(); // selected els
  for(const CSkeletonSelectable *other : *others) {
    const CSkeletonElement *el = dynamic_cast<const CSkeletonElement*>(other);
    for(int i=0; i<6; i++) {
      CSkeletonMultiNodeKey segkey = el->getSegmentKey(i);
      CSkeletonSegment *segment = skeleton->getSegment(segkey);
      segments.insert(segment);
    }
  }
  return segments;
}

CSkeletonSegmentSet SegmentsFromElementsCourier::exteriorSegments() const {
  // A segment is on the exterior of the element set if it's an edge
  // of an exterior face.
  const CSkeletonSelectableSet *elements = otherTracker->get();
  CSkeletonFaceSet exteriorFaces = exteriorFacesOfElements(skeleton, elements);
  CSkeletonSegmentSet segments;
  for(CSkeletonFace *face : exteriorFaces) {
    int nn = face->nnodes();
    for(int i=0; i<nn; i++) { 	// loop over segments
      segments.insert(face->getSegment(skeleton, i));
      // const CSkeletonNode *n0 = face->getNode(i);
      // const CSkeletonNode *n1 = face->getNode((i+1)%nn);
      // CSkeletonSegment *segment = skeleton->findExistingSegment(n0, n1);
      // segments.insert(segment);
    }
  }
  return segments;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SegmentsFromFacesCourier::SegmentsFromFacesCourier(
					 const CSkeletonBase *skel,
					 const std::string *coverage,
					 const CSelectionTracker *otherTracker,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : SegmentsFromOtherCourier(skel, coverage, otherTracker, clist, plist)
{}

CSkeletonSegmentSet SegmentsFromFacesCourier::allSegments() const {
  CSkeletonSegmentSet segments;
  const CSkeletonSelectableSet *others = otherTracker->get(); // selected faces
  for(const CSkeletonSelectable *other : *others) {
    const CSkeletonFace *face = dynamic_cast<const CSkeletonFace*>(other);
    for(int i=0; i<face->nnodes(); i++)
      segments.insert(face->getSegment(skeleton, i));
  }
  return segments;
}

CSkeletonSegmentSet SegmentsFromFacesCourier::exteriorSegments() const {
  // A segment is on an exterior boundary of a set of faces if only
  // one of the segment's faces is in the set.
  const CSkeletonSelectableSet *faces = otherTracker->get();
  std::multiset<CSkeletonSegment*> segcounts;
  for(const CSkeletonSelectable *f : *faces) {
    const CSkeletonFace *face = dynamic_cast<const CSkeletonFace*>(f);
    for(int i=0; i<face->nnodes(); i++) {
      segcounts.insert(face->getSegment(skeleton, i));
    }
  }
  CSkeletonSegmentSet segments;
  for(CSkeletonSegment *seg : segcounts)
    if(segcounts.count(seg) == 1)
      segments.insert(seg);
  return segments;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SegmentsFromNodesCourier::SegmentsFromNodesCourier(
				   const CSkeletonBase *skel,
				   bool oneNode, bool twoNodes,
				   const CSelectionTracker *otherTracker,
				   CSelectionTrackerVector *clist,
				   CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonSegmentSet>(skel, clist, plist)
{
  if(oneNode || twoNodes) {
    // Find all segments of the selected nodes
    CSkeletonSegmentSet allSegs;
    const CSkeletonSelectableSet *others = otherTracker->get();
    for(const CSkeletonSelectable *other : *others) {
      const CSkeletonNode *node = dynamic_cast<const CSkeletonNode*>(other);
      CSkeletonSegmentSet nodesegs;
      skeleton->getNodeSegments(node, nodesegs);
      allSegs.insert(nodesegs.begin(), nodesegs.end());
    }
    // Pick out the segments with the desired number of selected
    // nodes.  They all have either one or two.
    for(CSkeletonSegment *segment : allSegs) {
      int nsel = 0;
      if(segment->getNode(0)->isSelected()) nsel = 1;
      if(segment->getNode(1)->isSelected()) nsel += 1;
      if((nsel == 1 && oneNode) || (nsel == 2 && twoNodes))
	selectedObjects.insert(segment);
    }
  }
  else {
    // Select segments with zero selected nodes.  otherTracker is
    // useless.  Just look at all segments in the Skeleton.
    for(CSkeletonSegmentIterator s=skeleton->beginSegments();
	s!=skeleton->endSegments(); ++s)
      {
	CSkeletonSegment *segment = (*s).second;
	if(!segment->getNode(0)->isSelected() &&
	   !segment->getNode(1)->isSelected())
	  selectedObjects.insert(segment);
      }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

InternalBoundarySegmentsCourier::InternalBoundarySegmentsCourier(
						 const CSkeletonBase *skel,
						 CSelectionTrackerVector *clist,
						 CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonSegmentSet>(skel, clist, plist)
{
  // Internal boundary segments are the segments of the internal
  // boundary faces, which are faces whose elements have different
  // categories.
  CSkeletonFaceSet faces = internalBoundaryFaces(skeleton);
  for(CSkeletonFace *face : faces) {
    for(int i=0; i<face->nnodes(); i++)
      selectedObjects.insert(face->getSegment(skeleton, i));
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

EdgeBoundaryCourier::EdgeBoundaryCourier(const CSkeletonBase *skel,
					 const CSkeletonEdgeBoundary *bdy,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist),
    segments(bdy->getUnorientedSegments())
{}

EdgeBoundaryCourier::~EdgeBoundaryCourier() {
  // getUnorientedSegments returns a new vector.
  delete segments;
}

void EdgeBoundaryCourier::start() {
  iter = segments->begin();
  done_ = (iter == segments->end());
}

void EdgeBoundaryCourier::next() {
  ++iter;
  done_ = (iter == segments->end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

InhomogeneousSegmentCourier::InhomogeneousSegmentCourier(
					     const CSkeletonBase *skel,
					     double threshold,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonSegmentSet>(skel, clist, plist)
{
  for(CSkeletonSegmentIterator s=skeleton->beginSegments();
      s!=skeleton->endSegments(); ++s)
    {
      CSkeletonSegment *segment = (*s).second;
      if(segment->homogeneity(skeleton) < threshold)
	selectedObjects.insert(segment);
    }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RandomSegmentCourier::RandomSegmentCourier(const CSkeletonBase *skel,
					   double prob,
					   CSelectionTrackerVector *clist,
					   CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist),
    probability(prob)
{}

void RandomSegmentCourier::start() {
  iter = skeleton->beginSegments();
  advance();
}

void RandomSegmentCourier::advance() {
  while(iter != skeleton->endSegments() && rndm() >= probability)
    ++iter;
  done_ = (iter == skeleton->endSegments());
}

void RandomSegmentCourier::next() {
  iter++;
  advance();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//        Face Selection Couriers
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

AllFacesCourier::AllFacesCourier(const CSkeletonBase *skel,
				 CSelectionTrackerVector *clist,
				 CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist)
{}

void AllFacesCourier::start() {
  iter = skeleton->beginFaces();
  done_ = (iter == skeleton->endFaces());
}

void AllFacesCourier::next() {
  ++iter;
  done_ = (iter == skeleton->endFaces());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FacesFromElementsCourier::FacesFromElementsCourier(
				   const CSkeletonBase *skel,
				   const std::string *coverage,
				   const CSelectionTracker *elemTracker,
				   CSelectionTrackerVector *clist,
				   CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonFaceSet>(skel, clist, plist)
{
  if(*coverage == std::string("Exterior"))
    selectedObjects = exteriorFaces(elemTracker);
  else if(*coverage == std::string("All"))
    selectedObjects = allFaces(elemTracker);
  else {
    CSkeletonFaceSet allfaces = allFaces(elemTracker);
    CSkeletonFaceSet extfaces = exteriorFaces(elemTracker);
    std::set_difference(allfaces.begin(), allfaces.end(),
			extfaces.begin(), extfaces.end(),
			std::inserter(selectedObjects, selectedObjects.end()));
  }
}

CSkeletonFaceSet FacesFromElementsCourier::exteriorFaces(
				 const CSelectionTracker *tracker)
  const
{
  return exteriorFacesOfElements(skeleton, tracker->get());
}

CSkeletonFaceSet FacesFromElementsCourier::allFaces(
					    const CSelectionTracker *tracker)
  const
{
  CSkeletonFaceSet faces;
  const CSkeletonSelectableSet *elements = tracker->get();
  for(const CSkeletonSelectable *e : *elements) {
    const CSkeletonElement *el = dynamic_cast<const CSkeletonElement*>(e);
    for(int i=0; i<4; i++) {
      const CSkeletonMultiNodeKey fkey = el->getFaceKey(i);
      CSkeletonFace *face = skeleton->getFace(fkey);
      faces.insert(face);
    }
  }
  return faces;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FacesFromNodesCourier::FacesFromNodesCourier(
				     const CSkeletonBase *skel,
				     int min_nodes,
				     const CSelectionTracker *nodeTracker,
				     CSelectionTrackerVector *clist,
				     CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonFaceSet>(skel, clist, plist)
{
  const CSkeletonSelectableSet *nodes = nodeTracker->get();
  if(min_nodes == 1) {
    for(const CSkeletonSelectable *n : *nodes) {
      const CSkeletonNode *node = dynamic_cast<const CSkeletonNode*>(n);
      CSkeletonFaceSet faces;
      skeleton->getNodeFaces(node, faces);
      selectedObjects.insert(faces.begin(), faces.end());
    }
  } // end if min_nodes == 1
  else {			// min_nodes == 2 or 3
    // Loop over the selected nodes and examine each face at the nodes
    // to see if they have at least min_nodes selected nodes.  Each
    // face could be examined up to three times, so keep track of
    // which ones have already been seen and don't repeat them.
    CSkeletonFaceSet examinedAlready;
    for(const CSkeletonSelectable *n : *nodes) { // loop over selected nodes
      const CSkeletonNode *node = dynamic_cast<const CSkeletonNode*>(n);
      // Examine each face of each selected node, and count how many
      // selected nodes it has.
      CSkeletonFaceSet faces;
      skeleton->getNodeFaces(node, faces);
      for(CSkeletonFace *face : faces) {
	if(examinedAlready.count(face) == 0) {
	  examinedAlready.insert(face);
	  int nselected = 0;
	  // Count how many nodes of this face are selected.
	  for(CSkeletonNode *nn : *face->getNodes()) {
	    if(nn->isSelected())
	      ++nselected;
	  } // end loop over nodes of this face
	  if(nselected >= min_nodes)
	    selectedObjects.insert(face);
	}
      }	// end loop over faces of a selected node
    } // end loop over selected nodes
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FacesFromSegmentsCourier::FacesFromSegmentsCourier(
				   const CSkeletonBase *skel,
				   int min_segments,
				   const CSelectionTracker *segTracker,
				   CSelectionTrackerVector *clist,
				   CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonFaceSet>(skel, clist, plist)
{
  // This is conceptually identical to FacesFromNodesCourier
  const CSkeletonSelectableSet *segments = segTracker->get();
  if(min_segments == 1) {
    for(const CSkeletonSelectable *s : *segments) {
      const CSkeletonSegment *seg = dynamic_cast<const CSkeletonSegment*>(s);
      CSkeletonFaceVector faces;
      skeleton->getSegmentFaces(seg, faces);
      selectedObjects.insert(faces.begin(), faces.end());
    }
  }
  else {
    CSkeletonFaceSet examinedAlready;
    for(const CSkeletonSelectable *s : *segments) {
      const CSkeletonSegment *seg = dynamic_cast<const CSkeletonSegment*>(s);
      CSkeletonFaceVector faces;
      skeleton->getSegmentFaces(seg, faces);
      for(CSkeletonFace *face : faces) {
	if(examinedAlready.count(face) == 0) {
	  examinedAlready.insert(face);
	  CSkeletonSegmentSet fsegs;
	  skeleton->getFaceSegments(face, fsegs);
	  int nselected = 0;
	  for(CSkeletonSegment *fseg : fsegs) {
	    if(fseg->isSelected())
	      ++nselected;
	  }
	  if(nselected >= min_segments)
	    selectedObjects.insert(face);
	} // end if this face hasn't been examined already
      }	  // end loop over faces of this segment
    }	  // end loop over selected segments
  }	  // end if min_segments > 1
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FaceBoundaryCourier::FaceBoundaryCourier(const CSkeletonBase *skel,
					 const CSkeletonFaceBoundary *bdy,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist),
    faces(bdy->getUnorientedFaces())
{}

FaceBoundaryCourier::~FaceBoundaryCourier() {
  delete faces;
}

void FaceBoundaryCourier::start() {
  iter = faces->begin();
  done_ = (iter == faces->end());
}

void FaceBoundaryCourier::next() {
  ++iter;
  done_ = (iter == faces->end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

InternalBoundaryFacesCourier::InternalBoundaryFacesCourier(
					   const CSkeletonBase *skel,
					   CSelectionTrackerVector *clist,
					   CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonFaceSet>(skel, clist, plist)
{
  selectedObjects = internalBoundaryFaces(skel);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//        element Selection Couriers
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


AllElementsCourier::AllElementsCourier(const CSkeletonBase *skel,
				       CSelectionTrackerVector *clist,
				       CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist)
{}

void AllElementsCourier::start() {
  iter = skeleton->beginElements();
  done_ = (iter == skeleton->endElements());
}

void AllElementsCourier::next() {
  ++iter;
  done_ = (iter == skeleton->endElements());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ConditionalElementCourier::ConditionalElementCourier(
					     const CSkeletonBase *skel,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : SkeletonSelectionCourier(skel, clist, plist)
{}

void ConditionalElementCourier::start() {
  iter = skeleton->beginElements();
  done_ = false;
  advance();
}

void ConditionalElementCourier::next() {
  iter++;
  advance();
}

void ConditionalElementCourier::advance() {
  while(iter != skeleton->endElements()) {
    if(includeElement(*iter))
      return;
    ++iter;
  }
  done_ = true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MaterialElementCourier::MaterialElementCourier(const CSkeletonBase *skel,
					       const Material *mat,
					       CSelectionTrackerVector *clist,
					       CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist),
    material(mat)
{}

bool MaterialElementCourier::includeElement(const CSkeletonElement *el) const {
  return el->material(skeleton) == material;
}

AnyMaterialElementCourier::AnyMaterialElementCourier(
					     const CSkeletonBase *skel,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist)
{}

bool AnyMaterialElementCourier::includeElement(const CSkeletonElement *el)
  const
{
  return el->material(skeleton) != 0;
}

NoMaterialElementCourier::NoMaterialElementCourier(
					     const CSkeletonBase *skel,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist)
{}

bool NoMaterialElementCourier::includeElement(const CSkeletonElement *el)
  const
{
  return el->material(skeleton) == 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CategoryElementCourier::CategoryElementCourier(const CSkeletonBase *skel,
					       int cat,
					       CSelectionTrackerVector *clist,
					       CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist),
    category(cat)
{}

bool CategoryElementCourier::includeElement(const CSkeletonElement *el) const {
  return el->dominantPixel(skeleton) == category;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementHomogeneityCourier::ElementHomogeneityCourier(
					     const CSkeletonBase *skel,
					     double min_homog,
					     double max_homog,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist),
    min_homogeneity(min_homog),
    max_homogeneity(max_homog)
{}

bool ElementHomogeneityCourier::includeElement(const CSkeletonElement *el) const
{
  double homog = el->homogeneity(skeleton);
  return homog >= min_homogeneity && homog <= max_homogeneity;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementShapeEnergyCourier::ElementShapeEnergyCourier(
					     const CSkeletonBase *skel,
					     double min_energy,
					     double max_energy,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist),
    min_energy(min_energy),
    max_energy(max_energy)
{}

bool ElementShapeEnergyCourier::includeElement(const CSkeletonElement *el) const
{
  double energy = el->energyShape();
  return energy >= min_energy && energy <= max_energy;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

IllegalElementCourier::IllegalElementCourier(const CSkeletonBase *skel,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist)
{}

bool IllegalElementCourier::includeElement(const CSkeletonElement *el) const
{
  return el->illegal();
}

SuspectElementCourier::SuspectElementCourier(const CSkeletonBase *skel,
					     CSelectionTrackerVector *clist,
					     CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist)
{}

bool SuspectElementCourier::includeElement(const CSkeletonElement *el) const
{
  return el->suspect();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementsFromNodesCourier::ElementsFromNodesCourier(
					 const CSkeletonBase *skel,
					 int min_nodes,
					 const CSelectionTracker *nodeTracker,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonElementSet>(skel, clist, plist)
{
  // See comments in FacesFromNodesCourier.  This is exactly like that.
  const CSkeletonSelectableSet *nodes = nodeTracker->get();
  if(min_nodes == 1) {
    for(const CSkeletonSelectable *n : *nodes) {
      const CSkeletonNode *node = dynamic_cast<const CSkeletonNode*>(n);
      CSkeletonElementVector *elements = node->getElements();
      selectedObjects.insert(elements->begin(), elements->end());
    }
  }
  else {
    CSkeletonElementSet examinedAlready;
    for(const CSkeletonSelectable *n : *nodes) {
      const CSkeletonNode *node = dynamic_cast<const CSkeletonNode*>(n);
      CSkeletonElementVector *elements = node->getElements();
      for(CSkeletonElement *element : *elements) {
	if(examinedAlready.count(element) == 0) {
	  examinedAlready.insert(element);
	  int nSelected = 0;
	  for(CSkeletonNode *eNode : *element->getNodes()) {
	    if(eNode->isSelected())
	      ++nSelected;
	  }
	  if(nSelected >= min_nodes)
	    selectedObjects.insert(element);
	}
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementsFromSegmentsCourier::ElementsFromSegmentsCourier(
					 const CSkeletonBase *skel,
					 int min_segments,
					 const CSelectionTracker *segTracker,
					 CSelectionTrackerVector *clist,
					 CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonElementSet>(skel, clist, plist)
{
  const CSkeletonSelectableSet *segments = segTracker->get();
  if(min_segments == 1) {
    for(const CSkeletonSelectable *s : *segments) {
      const CSkeletonSegment *seg = dynamic_cast<const CSkeletonSegment*>(s);
      CSkeletonElementVector elements = skeleton->getSegmentElements(seg);
      selectedObjects.insert(elements.begin(), elements.end());
    }
  }
  else {
    CSkeletonElementSet examinedAlready;
    for(const CSkeletonSelectable *s : *segments) {
      const CSkeletonSegment *seg = dynamic_cast<const CSkeletonSegment*>(s);
      CSkeletonElementVector elements = skeleton->getSegmentElements(seg);
      for(CSkeletonElement *element : elements) {
	if(examinedAlready.count(element) == 0) {
	  examinedAlready.insert(element);
	  int nSelected = 0;
	  for(int i=0; i<6; i++) {
	    CSkeletonMultiNodeKey segkey = element->getSegmentKey(i);
	    CSkeletonSegment *segment = skeleton->getSegment(segkey);
	    if(segment->isSelected())
	      ++nSelected;
	  }
	  if(nSelected >= min_segments)
	    selectedObjects.insert(element);
	}
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementsFromFacesCourier::ElementsFromFacesCourier(
					   const CSkeletonBase *skel,
					   int min_faces,
					   const CSelectionTracker *faceTracker,
					   CSelectionTrackerVector *clist,
					   CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonElementSet>(skel, clist, plist)
{
  const CSkeletonSelectableSet *faces = faceTracker->get();
  if(min_faces == 1) {
    for(const CSkeletonSelectable *f : *faces) {
      const CSkeletonFace *face = dynamic_cast<const CSkeletonFace*>(f);
      CSkeletonElementVector elements;
      skeleton->getFaceElements(face, elements);
      selectedObjects.insert(elements.begin(), elements.end());
    }
  }
  else {
    CSkeletonElementSet examinedAlready;
    for(const CSkeletonSelectable *f : *faces) {
      const CSkeletonFace *face = dynamic_cast<const CSkeletonFace*>(f);
      CSkeletonElementVector elements;
      skeleton->getFaceElements(face, elements);
      for(CSkeletonElement *element : elements) {
	if(examinedAlready.count(element) == 0) {
	  examinedAlready.insert(element);
	  int nSelected = 0;
	  for(int i=0; i<4; i++) {
	    CSkeletonMultiNodeKey facekey = element->getFaceKey(i);
	    CSkeletonFace *face = skeleton->getFace(facekey);
	    if(face->isSelected())
	      ++nSelected;
	  }
	  if(nSelected >= min_faces)
	    selectedObjects.insert(element);
	}
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ExpandElementSelectionCourier::ExpandElementSelectionCourier(
				     const CSkeletonBase *skel,
				     std::string *mode,
				     const CSelectionTracker *oldSelection,
				     CSelectionTrackerVector *clist,
				     CSelectionTrackerVector *plist)
  : BulkSkelSelCourier<CSkeletonElementSet>(skel, clist, plist)
{
  const CSkeletonSelectableSet *oldElements = oldSelection->get();
  for(const CSkeletonSelectable *e : *oldElements) {
    const CSkeletonElement *element = dynamic_cast<const CSkeletonElement*>(e);

    if(*mode == std::string("Nodes")) {
      const CSkeletonNodeVector *nodes = element->getNodes();
      for(CSkeletonNode *node : *nodes) {
	CSkeletonElementVector *elements = node->getElements();
	selectedObjects.insert(elements->begin(), elements->end());
      }
    }
    else if(*mode == std::string("Segments")) {
      for(int i=0; i<6; i++) {
	CSkeletonMultiNodeKey segkey = element->getSegmentKey(i);
	CSkeletonSegment *seg = skeleton->getSegment(segkey);
	CSkeletonElementVector elements = skeleton->getSegmentElements(seg);
	selectedObjects.insert(elements.begin(), elements.end());
      }
    }
    else {
      assert(*mode == std::string("Faces"));
      // Would it be better to use exteriorFacesOfElements here?
      for(int i=0; i<4; i++) {
	CSkeletonMultiNodeKey fkey = element->getFaceKey(i);
	CSkeletonFace *face = skeleton->getFace(fkey);
	CSkeletonElementVector elements;
	skeleton->getFaceElements(face, elements);
	selectedObjects.insert(elements.begin(), elements.end());
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PixelGroupCourier::PixelGroupCourier(const CSkeletonBase *skel,
				     const PixelGroup *grp,
				     CSelectionTrackerVector *clist,
				     CSelectionTrackerVector *plist)
  : ConditionalElementCourier(skel, clist, plist),
    group(grp)
{}

bool PixelGroupCourier::includeElement(const CSkeletonElement *element) const
{
  int cat = element->dominantPixel(skeleton);
  return pixelGroupQueryCategory(*skeleton->getMicrostructure(), cat, group);
}
