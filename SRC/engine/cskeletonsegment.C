// -*- C++ -*-
// $RCSfile: cskeletonsegment.C,v $
// $Revision: 1.1.2.44 $
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

#include "common/IO/oofcerr.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/printvec.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonsegment.h"
#include <vtkMath.h>
#include <vtkLine.h>
#include <algorithm> 		// for std::reverse

const std::string CSkeletonSegment::modulename_(
				"ooflib.SWIG.engine.cskeletonsegment");
const std::string CSkeletonSegment::classname_("CSkeletonSegment");

CSkeletonSegment::~CSkeletonSegment() {}

CSkeletonSegment::CSkeletonSegment(CSkeletonNodeVector *ns)
  : CSkeletonMultiNodeSelectable(ns),
    nelements(0)
{
  // std::cerr << "CSkeletonSegment::ctor: uid=" << uid << " nodes=";
  // for(int i=0; i<2; i++)
  //   std::cerr << " " << (*nodes)[i]->getUid();
  // std::cerr << std::endl;
  defunct=true;	     // segments are defunct until elements are added.
}

CSkeletonSegment* CSkeletonSegment::new_child(int idx,
					      vtkSmartPointer<vtkPoints> pts)
{
  CSkeletonNodeVector *node_children = get_node_children();
  CSkeletonSegment *child  = new CSkeletonSegment(node_children);
  return child;
}
  

double CSkeletonSegment::length() const {
  return sqrt(norm2((*nodes)[0]->position() - (*nodes)[1]->position()));
}

double CSkeletonSegment::lengthInVoxelUnits(const CMicrostructure *MS) const {
  Coord spts[2];
  Coord delta = MS->sizeOfPixels();
  for(int i=0; i<2; ++i) {
    spts[i] = (*nodes)[i]->position()/delta;
  }
  return sqrt(norm2(spts[0] - spts[1]));
}

double CSkeletonSegment::lengthInFractionalUnits(const CMicrostructure *MS) const {
  Coord spts[2];
  Coord delta = MS->size();
  for(int i=0; i<2; ++i) {
    spts[i] = (*nodes)[i]->position()/delta;
  }
  return sqrt(norm2(spts[0] - spts[1]));
}

double CSkeletonSegment::homogeneity(const CMicrostructure *MS) const {
  return MS->edgeHomogeneity((*nodes)[0]->position(), (*nodes)[1]->position());
}

int CSkeletonSegment::dominantPixel(const CMicrostructure *ms) const {
  int cat;
  ms->edgeHomogeneityCat((*nodes)[0]->position(), (*nodes)[1]->position(), &cat);
  return cat;
}

vtkSmartPointer<vtkCell> CSkeletonSegment::getEmptyVtkCell() const {
  return vtkSmartPointer<vtkLine>::New();
}

void CSkeletonSegment::increment_nelements() {
  ++nelements;
  defunct=false;
}

void CSkeletonSegment::decrement_nelements() {
  --nelements;
  defunct = (nelements == 0);
}

void CSkeletonSegment::getElements(const CSkeletonBase *skel,
				   ConstCSkeletonElementVector &result)
  const
{
  skel->getConstSegmentElements(this, result);
}

void CSkeletonSegment::getElements(const CSkeletonBase *skel,
				   CSkeletonElementVector &result)
{
  skel->getSegmentElements(this, result);
}

const CSkeletonElement *CSkeletonSegment::getElement(const CSkeletonBase *skel,
						     int which)
  const
{
  ConstCSkeletonElementVector elements;
  skel->getConstSegmentElements(this, elements);
  return elements[which];
}


void CSkeletonSegment::print(std::ostream &os) const {
  os << "Segment(" << uid << ", ";
  printNodes(os);
  os << ")";
}

void OrientedCSkeletonSegment::set_direction(const CSkeletonNode *n0,
					     const CSkeletonNode *n1) 
{
  // TODO OPT: Do we really need this method?  The single-node version of
  // set_direction should be sufficient.
  if(*segment->getNode(0) == *n0 && *segment->getNode(1) == *n1)
    direction = 1;
  else if(*segment->getNode(1) == *n0 && *segment->getNode(0) == *n1)
    direction = -1;
  else
    throw ErrProgrammingError("Incorrect node set in OrientedCSkeletonEdge",
			      __FILE__, __LINE__);
}

// Set the direction so that the given node is the segment's first
// node.
void OrientedCSkeletonSegment::set_direction(const CSkeletonNode *firstnode) {
  if(*segment->getNode(0) == *firstnode)
    direction = 1;
  else
    direction = -1;
}

Coord OrientedCSkeletonSegment::get_direction_vector() {
  return direction * (segment->getNode(1)->position() - 
		      segment->getNode(0)->position());
}

vtkSmartPointer<vtkIdList> OrientedCSkeletonSegment::getPointIds() const {
  return get_segment()->getPointIds();
}


// OLD VERSION of segSequence.  It's not clear why this was a static
// OrientedCSkeletonSegment method, and not just a function.  It's
// also not clear why the seglist arg is a CSkeletonSelectableList,
// instead of a CSkeletonSegmentVector.  In any case, it is being
// replaced by sequenceSegments().
bool OrientedCSkeletonSegment::segSequence(
			   const CSkeletonSelectableList *seglist,
			   CSkeletonNode *caller_start_node, 
			   CSkeletonSegmentVector &seg_sequence,
			   CSkeletonNodeVector &node_sequence) 
{
  // TODO 3.1: update for periodic skeletons, or eliminate entirely in
  // favor of sequenceSegments(), which probably needs to be updated
  // too.

  seg_sequence.clear();
  node_sequence.clear();

  if(seglist->empty())
    return true;

  std::map<CSkeletonNode*, CSkeletonSegmentList> adjacency;
  std::map<CSkeletonNode*, CSkeletonSegmentList>::iterator ami; // adjacency map iterator
  for(CSkeletonSelectableList::const_iterator it = seglist->begin();
      it != seglist->end(); ++it)
    {
      CSkeletonSegment *s = dynamic_cast<CSkeletonSegment*>(*it);
      const CSkeletonNodeVector *nodes = s->getNodes();

//     double x[3];
//     (*nodes)[0]->position(x);
//     cout << "segment " << s->getUid() << " " << x[0] << " " << x[1] << " " << x[2];
//     (*nodes)[1]->position(x);
//     cout << " to " << x[0] << " " << x[1] << " " << x[2] << endl;
//     cout << "node uids: " << (*nodes)[0]->getUid() << " " << (*nodes)[1]->getUid() << endl;
    

      for(int i=0; i<2; ++i) {
	ami = adjacency.find((*nodes)[i]);
	if(ami == adjacency.end()) 
	  adjacency[(*nodes)[i]] = CSkeletonSegmentList(1, s);
	else
	  adjacency[(*nodes)[i]].push_back(s);
      
      //         for p in n[0].getPartners():
      //             try:
      //                 adjacency[p].append(s)
      //             except KeyError:
      //                 adjacency[p] = [s]
    }
  } // end loop over seglist
 
//     # remove any grazed corners (nodes added to adjacency dictionary
//     # because of partnerships, that are not directly connected to
//     # segments in the boundary) before doing the topology check
//     for (n,l) in adjacency.items():
//         grazedCorner = True
//         for seg in l:
//             if n in seg.get_nodes():
//                 grazedCorner = False
//         if grazedCorner:
//             del adjacency[n]  

  // Basic topology check -- if any node occurs in 3 or more segments,
  // there's a self-intersection, and we can't sequence.  This loop
  // would also detect zero-length segment lists, but since the nodes
  // used are deduced from the passed-in segments, that can't happen.
  CSkeletonNodeVector endpoints;
  for(ami = adjacency.begin(); ami != adjacency.end(); ++ami) {
    if((*ami).second.size() == 1)
      endpoints.push_back((*ami).first);
    else if((*ami).second.size() != 2) {
      oofcerr << "OrientedCSkeletonSegment::segSequence: self intersection"
	      << endl;
      return false;
    }
  }

  // Find the callers's start node, or pick our own.
  CSkeletonNode *start_node;
  if(endpoints.size() == 2) { // Line case.
    if(caller_start_node != NULL) {
      if(caller_start_node == endpoints[0] || caller_start_node == endpoints[1])
	start_node = caller_start_node;
      else {
	oofcerr << "OrientedCSkeletonSegment::segSequence: start node in middle"
		<< endl;
	return false;
      }
    }
    else
      start_node = endpoints[0]; // arbitrary
  }
  else if(endpoints.empty()) { // Loop case.
    if(caller_start_node != NULL) {
      ami = adjacency.find(caller_start_node);
      if(ami != adjacency.end()) 
	start_node = caller_start_node;
      else {
	oofcerr << "OrientedCSkeletonSegment::segSequence: loop case with start node not in loop" << endl;
	return false;
      }
    }
    start_node = (*adjacency.begin()).first; // arbitrary
  }
  // We reach this point if the number of nodes with only one
  // corresponding segment in the passed-in set is not 0 or 2 (ie, the
  // number of endpoints is something other than 0 or 2).  This could
  // happen for disjoint segments that don't link up properly.
  else {
    oofcerr << "OrientedCSkeletonSegment::segSequence: disjoint segs "
	    << endpoints.size() << endl;
//     double x[3];
//     for(CSkeletonNodeVector::iterator epit = endpoints.begin(); epit != endpoints.end(); ++epit) {
//       (*epit)->position(x);
//       cout << "endpoint: " << x[0] << " " << x[1] << " " << x[2] << endl;
//     }
    return false;
  }

  // Build the correctly-sequenced vector now.
  node_sequence.push_back(start_node);

//     # The case where we begin with a node that is on a periodic
//     # boundary but the first segment is across the boundary is
//     # confusing, so we simply reverse the list of segments in the
//     # adjacency dict for the starting node
//     for partner in begin_node.getPartners():
//         if partner in adjacency.keys():
//             seg = adjacency[begin_node][0]
//             if begin_node not in seg.get_nodes():
//                 adjacency[begin_node].reverse()

  while(!adjacency[node_sequence.back()].empty()) {
    CSkeletonSegment *seg = adjacency[node_sequence.back()].front();
    seg_sequence.push_back(seg);
    adjacency[node_sequence.back()].remove(seg);
//         # in case we've just crossed a periodic boundary, we must
//         # remove the seg from the partner on the other side  
//         for partner in node_sequence[-1].getPartners():
//             if partner in adjacency.keys():
//                 adjacency[partner].remove(seg)
    node_sequence.push_back(seg->get_other_node(node_sequence.back()));
    adjacency[node_sequence.back()].remove(seg);

//         # cross the periodic boundary.
//         for partner in node_sequence[-1].getPartners():
//             if partner in adjacency.keys():
//                 setWindingVector(node_sequence51[-1], partner, winding_vector)
//                 node_sequence.append(partner)
//                 adjacency[partner].remove(seg)
  }

  for(ami = adjacency.begin(); ami != adjacency.end(); ++ami) {
    if(!(*ami).second.empty()) {
      oofcerr << "OrientedCSkeletonSegment::segSequence: failed adjacency check" << endl;
      return false;
    }
  }

  return true;
} // end OrientedCSkeletonSegment::segSequence

std::ostream &operator<<(std::ostream &os,
			 const OrientedCSkeletonSegment &oseg)
{
  os << "OrientedCSkeletonSegment("
     << oseg.getNode(0)->position() << ", "
     << oseg.getNode(1)->position() << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

AdjacencyMap findAdjacency(const CSkeletonSegmentVector *segs) {
  AdjacencyMap adjacency;
  for(CSkeletonSegmentVector::const_iterator it=segs->begin(); it!=segs->end();
      ++it)
    {
      CSkeletonSegment *seg = *it;
      const CSkeletonNodeVector *nodes = seg->getNodes();
      for(int i=0; i<2; i++) {
	CSkeletonNode *node = (*nodes)[i];
	AdjacencyMap::iterator ami = adjacency.find(node);
	if(ami == adjacency.end())
	  adjacency[node] = CSkeletonSegmentList(1, seg);
	else
	  (*ami).second.push_back(seg);
      }
    }
  return adjacency;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SegmentSequence *sequenceSegments(const CSkeletonSegmentVector *segments,
				  CSkeletonNode *startNode)
{
  // startNode can be a null pointer, in which case an arbitrary
  // starting node will be picked.

  // TODO 3.1: startNode should be const.  Changing it to const looks like
  // it'll trigger a cascade of changes of unknown extent.

  // If this routine returns a null pointer, it has failed to find a
  // sequence.
  if(segments->empty())
    return 0;

  // Construct a map of which segments connect to which nodes.
  AdjacencyMap adjacency = findAdjacency(segments);

  // Find the endpoints, and perform a basic topology check: if any
  // node occurs in 3 or more segments, there's a self intersection or
  // branch and the segments can't be sequenced.
  CSkeletonNodeVector endpoints;
  for(AdjacencyMap::const_iterator i=adjacency.begin(); i!=adjacency.end(); ++i)
    {
      if((*i).second.size() == 1)
	endpoints.push_back((*i).first);
      else if((*i).second.size() > 2) {
#ifdef DEBUG
	oofcerr << "sequenceSegments: incompatible topology!"
		<< std::endl;
#endif // DEBUG
	return 0;
      }
    }
  // Second topology check: there must be a single loop with zero
  // endpoints, or a line with two endpoints.  Anything else can't be
  // sequenced.
  if(!(endpoints.empty() || endpoints.size() == 2)) {
#ifdef DEBUG
    oofcerr << "sequenceSegments: wrong number of endpoints! ("
	    << endpoints.size() << ")" << std::endl;
#endif // DEBUG
    return 0;
  }
  
  // Check the start node, or pick one if none was provided.

  // TODO 3.1 NOTE: because adjacency is a std::map, the order of the
  // iteration used to find the endpoints isn't guaranteed, and the
  // points stored in endpoints are therefore in an arbitrary order.
  // This means that if the start node isn't provided, the choice made
  // here is really arbitrary.

  CSkeletonNode *start = 0;
  if(endpoints.size() == 2) {
    // There are two endpoints.  The start node must be one of them.
    if(startNode) {
      if(startNode != endpoints[0] && startNode != endpoints[1]) {
#ifdef DEBUG
	oofcerr << "sequenceSegments: start node is in the middle!"
		<< std::endl;
#endif // DEBUG
	return 0;
      }
      start = startNode;
    }
    else {		
      // startNode not provided.  Make an arbitrary choice.  Which
      // node is chosen doesn't matter, because the sequence will be
      // reversed if necessary when its direction is set, so this is
      // ok, even though endpoints was derived from adjacency, which
      // is not deterministic.  Compare to the situation for loops,
      // below.
      start = endpoints[0];
    }
  } // end if 2 endpoints
  else if(endpoints.empty()) {
    if(startNode) {
      AdjacencyMap::iterator ami = adjacency.find(startNode);
      if(ami == adjacency.end()) {
#ifdef DEBUG
	oofcerr << "sequenceSegments: start node is not in loop" << std::endl;
#endif // DEBUG
	return 0;
      }
      start = startNode;
    }
    else {
      // startNode was not provided.  Make an arbitrary choice.
      // *Don't* use adjacency to make the choice.  The order of the
      // items in a std::map isn't reproducible, and for testing
      // purposes startNode must be reproducible.
      start = segments->front()->getNode(0);
    }
  } // end if 0 endpoints

  // Build the sequence. 
  SegmentSequence *result = new SegmentSequence();
  CSkeletonNode *current = start;
  while(!adjacency[current].empty()) {
    // Get the first segment in the adjacency list for the current node.
    CSkeletonSegment *seg = adjacency[current].front();
    OrientedCSkeletonSegment *oseg = new OrientedCSkeletonSegment(seg);
    oseg->set_direction(current);
    adjacency[current].remove(seg);
    result->segments.push_back(oseg);
    current = seg->get_other_node(current);
    adjacency[current].remove(seg);
  }
  
  // Check that nothing's left over
  for(AdjacencyMap::const_iterator ami=adjacency.begin(); ami!=adjacency.end();
      ++ami)
    {
      if(!(*ami).second.empty()) {
#ifdef DEBUG
	oofcerr << "sequenceSegments: adjacency check failed!" << std::endl;
#endif // DEBUG
	delete result;
	return 0;
      }
    }
  
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SegmentSequence::~SegmentSequence() {
  for(OrientedCSkeletonSegmentVector::iterator i=segments.begin();
      i<segments.end(); ++i)
    {
      delete *i;
    }
}

bool SegmentSequence::closed() const {
  return segments.front()->getNode(0) == segments.back()->getNode(1);
}

void SegmentSequence::reverse() {
  std::reverse(segments.begin(), segments.end());
  for(OrientedCSkeletonSegmentVector::iterator i=segments.begin();
      i!=segments.end(); ++i)
    {
      (*i)->reverse();
    }
};

Coord SegmentSequence::span() const {
  return (segments.back()->getNode(1)->getPosition() -
	  segments.front()->getNode(0)->getPosition());
}

OrientedCSkeletonSegmentVector::const_iterator SegmentSequence::begin() const {
  return segments.begin(); 
}

OrientedCSkeletonSegmentVector::const_iterator SegmentSequence::end() const {
  return segments.end(); 
}

double SegmentSequence::projectedArea(const std::string &plane) const {
  if(!closed())
    return 0;
  int proj = plane[0]-'x';   // which component is being projected out
  int j = (proj + 1) % 3;
  int k = (proj + 2) % 3;
  double area = 0;
  for(OrientedCSkeletonSegmentVector::const_iterator i=begin(); i!=end(); ++i) {
    Coord p0 = (*i)->getNode(0)->getPosition();
    Coord p1 = (*i)->getNode(1)->getPosition();
    double dA = p0[j]*p1[k] - p0[k]*p1[j]; 
    area += dA;
  }
  return 0.5*area;
}
