// -*- C++ -*-
// $RCSfile: cskeletonboundary.C,v $
// $Revision: 1.1.2.47 $
// $Author: langer $
// $Date: 2014/12/14 22:49:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/oofcerr.h"
#include "common/coord.h"
#include "common/printvec.h"
#include "engine/cskeletonboundary.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/ooferror.h"

#include <vtkMath.h>
#include <algorithm> 

// Names needed for PythonExportable base class
const std::string CSkeletonBoundary::modulename_(
				 "ooflib.SWIG.engine.cskeletonboundary");
const std::string CSkeletonPointBoundary::classname_(
					     "CSkeletonPointBoundary");
const std::string ExteriorCSkeletonPointBoundary::classname_(
					     "ExteriorCSkeletonPointBoundary");
const std::string CSkeletonEdgeBoundary::classname_("CSkeletonEdgeBoundary");
const std::string ExteriorCSkeletonEdgeBoundary::classname_(
					    "ExteriorCSkeletonEdgeBoundary");
const std::string CSkeletonFaceBoundary::classname_("CSkeletonFaceBoundary");
const std::string ExteriorCSkeletonFaceBoundary::classname_(
					    "ExteriorCSkeletonFaceBoundary");

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonBoundary::CSkeletonBoundary(const std::string &name)
  : name_(name)
{
}

CSkeletonBoundary::~CSkeletonBoundary() {
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonPointBoundary* CSkeletonPointBoundary::map(CSkeleton *new_skeleton,
						    SkeletonMapDir direction,
						    bool exterior)
{
  CSkeletonPointBoundary *new_bdy =
    new_skeleton->makePointBoundary(name_, NULL, exterior);
  
  CSkeletonNodeVector target_list;
  for(CSkeletonNodeSet::iterator it = nodes.begin(); it != nodes.end(); ++it) {
    CSkeletonSelectableList &src = (*it)->getRelatives(direction);
    for(CSkeletonSelectableList::iterator c=src.begin(); c!=src.end(); ++c) {
      CSkeletonNode *n = dynamic_cast<CSkeletonNode*>(*c);
      // TODO MER: if a separate 2D version is needed, this should be
      // encapsulated in a function:
      if( !exterior or (n->movable_x() == (*it)->movable_x() && 
			n->movable_y() == (*it)->movable_z() && 
			n->movable_y() == (*it)->movable_z())) 
	target_list.push_back(n);
    }  
  }

  CSkeletonNodeVector new_node_list;
  for(CSkeletonNodeVector::iterator it=target_list.begin();
      it!=target_list.end(); ++it)
    {
      CSkeletonSelectableList &src = (*it)->getRelatives(direction);
      bool valid = true;
      for(CSkeletonSelectableList::iterator c=src.begin(); c!=src.end(); ++c)
	{
	  CSkeletonNode *n = dynamic_cast<CSkeletonNode*>(*c);
	  if(!hasNode(n)) {
	    valid = false;
	    break;
	  }
	}
      if(valid)
	new_node_list.push_back(*it);
    }
  
  new_bdy->appendNodes(&new_node_list);
  return new_bdy;
}

void CSkeletonPointBoundary::appendNodes(const CSkeletonNodeVector *ns) {
  nodes.insert(ns->begin(), ns->end()); 
}

void CSkeletonPointBoundary::removeNodes(const CSkeletonNodeVector *ns) {
  for(CSkeletonNodeVector::const_iterator i=ns->begin(); i!=ns->end(); ++i) {
    nodes.erase(*i);
  }
}

bool CSkeletonPointBoundary::hasNode(const CSkeletonNode *node) const {
  return nodes.find(const_cast<CSkeletonNode*>(node)) != nodes.end();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonEdgeBoundary::~CSkeletonEdgeBoundary() {
  for(OrientedCSkeletonSegmentVector::iterator it = oriented_segments.begin(); 
      it != oriented_segments.end(); ++it) 
    {
      delete (*it);
    }
};

bool CSkeletonEdgeBoundary::try_appendSegs(const CSkeletonSegmentVector *segs)
  const
{
  CSkeletonSegmentVector *allSegs = getUnorientedSegments();
  allSegs->insert(allSegs->end(), segs->begin(), segs->end());
  SegmentSequence *segSeq = sequenceSegments(allSegs, (CSkeletonNode*) 0);
  bool status = (segSeq != 0);
  delete segSeq;
  delete allSegs;
  return status;
}

// There are two versions of appendSegs(), one for unoriented segments
// and one for oriented segments.  The one for unoriented segments has
// to orient them.

void CSkeletonEdgeBoundary::appendSegs(
			       const OrientedCSkeletonSegmentVector &segs) 
{
  oriented_segments.insert(oriented_segments.end(), segs.begin(), segs.end());
}

void CSkeletonEdgeBoundary::appendSegs(const CSkeletonSegmentVector *segs) {
  // This is similar to sequenceSegments() in cskeletonsegment.C.
  // It's not the same, because here we already know the direction of
  // the pre-existing segments in the boundary and we don't want to
  // lose that information.
  assert(!empty());
  CSkeletonNode *head = oriented_segments.front()->getNode(0);
  CSkeletonNode *tail = oriented_segments.back()->getNode(1);
  AdjacencyMap adjacency = findAdjacency(segs);

  // Construct the sequence of segments to add to the head of the
  // existing sequence.
  OrientedCSkeletonSegmentVector prepended;
  AdjacencyMap::iterator ami = adjacency.find(head);
  while(ami != adjacency.end() && !(*ami).second.empty()) {
    // Find the segment adjacent to the current head ...
    CSkeletonSegment *newseg = (*ami).second.front();
    // ... remove the segment from the adjacency list for the head node
    (*ami).second.pop_front();
    // Remove the list of segments for the head node.  The list should
    // be empty, since the head node can have only one new segment
    // added to it.
    assert((*ami).second.empty());
    adjacency.erase(ami);

    CSkeletonNode *newnode = newseg->get_other_node(head);
    int direction = (newnode == newseg->getNode(1) ? -1 : 1);
    prepended.push_back(new OrientedCSkeletonSegment(newseg, direction));
    // Look for the next segment.
    head = newnode;
    ami = adjacency.find(head);
    // Remove the segment from the adjacency list for the new head
    // (because this segment has already been used).
    (*ami).second.remove(newseg);
  }

  // Construct the sequence of segments to add to the tail of the
  // existing sequence.
  OrientedCSkeletonSegmentVector appended;
  ami = adjacency.find(tail);
  while(ami != adjacency.end() && !(*ami).second.empty()) {
    CSkeletonSegment *newseg = (*ami).second.front();
    (*ami).second.pop_front();
    assert((*ami).second.empty());
    adjacency.erase(ami);
    CSkeletonNode *newnode = newseg->get_other_node(tail);
    int direction = (newnode == newseg->getNode(0) ? -1 : 1);
    appended.push_back(new OrientedCSkeletonSegment(newseg, direction));
    tail = newnode;
    ami = adjacency.find(tail);
    (*ami).second.remove(newseg);
  }

  // Add the new segments to the boundary.
  oriented_segments.insert(oriented_segments.begin(),
			   prepended.rbegin(), prepended.rend());
  oriented_segments.insert(oriented_segments.end(),
			   appended.begin(), appended.end());
}

bool CSkeletonEdgeBoundary::try_removeSegs(const CSkeletonSegmentVector *segs)
  const
{
  CSkeletonSegmentVector *oldSegs = getUnorientedSegments();
  for(CSkeletonSegmentVector::const_iterator i=segs->begin(); i!=segs->end();
      ++i)
    {
      for(CSkeletonSegmentVector::iterator j=oldSegs->begin(); 
	  j!=oldSegs->end(); ++j)
	{
	  if(*j == *i) {
	    oldSegs->erase(j);
	    break;
	  }
	}
      // If a segment in segs isn't in oldSegs, that's ok.  Ignore it.
    }
  SegmentSequence *segSeq = sequenceSegments(oldSegs, (CSkeletonNode*) 0);
  bool status = (segSeq != 0);
  delete segSeq;
  delete oldSegs;
  return status;
}

void CSkeletonEdgeBoundary::removeSegs(const CSkeletonSegmentVector *segs) {
  for(CSkeletonSegmentVector::const_iterator i=segs->begin(); i!=segs->end();
      ++i) 
    {
      for(OrientedCSkeletonSegmentVector::iterator j=oriented_segments.begin();
	  j!=oriented_segments.end(); ++j) 
	{
	  if((*j)->get_segment() == *i) {
	    oriented_segments.erase(j);
	    break;
	  }
	}
    }
}

const OrientedCSkeletonSegmentVector *CSkeletonEdgeBoundary::getSegments() const
{
  return &oriented_segments;
}

const OrientedCSkeletonSegmentVector *
CSkeletonEdgeBoundary::getOrientedSegments()
  const
{
  return &oriented_segments;
}

CSkeletonSegmentVector *CSkeletonEdgeBoundary::getUnorientedSegments() const {
  CSkeletonSegmentVector *segs = new CSkeletonSegmentVector();
  for(OrientedCSkeletonSegmentVector::const_iterator
	i=oriented_segments.begin();
      i!=oriented_segments.end(); ++i)
    {
      segs->push_back((*i)->get_segment());
    }
  return segs;
}

bool CSkeletonEdgeBoundary::hasSegment(const CSkeletonSegment *seg) const {
  for(OrientedCSkeletonSegmentVector::const_iterator
	i=oriented_segments.begin(); i!=oriented_segments.end(); ++i)
    {
      if((*i)->get_segment() == seg)
	return true;
    }
  return false;
}

// Propagate a boundary up to its parent or down to its child.  Caller
// must ensure that the skeleton passed through as "new_skeleton" in
// fact contains the appropriately-related segments (parents for
// MAP_UP, children for MAP_DOWN) with respect to first skeleton.
// Caller is also responsible for issuing the "new_boundaries" signal.

CSkeletonEdgeBoundary *CSkeletonEdgeBoundary::map(
	  CSkeleton *new_skeleton, SkeletonMapDir direction, bool exterior)
{
  CSkeletonEdgeBoundary *new_bdy = new_skeleton->makeEdgeBoundary(
					  name_, NULL, NULL, exterior);

  // oofcerr << "CSkeletonEdgeBoundary::map: " << get_name() << " -------- " 
  // 	  << std::endl;
  // Convert oriented_segments to a list so we can pop items off the
  // front and remove from the middle efficiently, without modifying
  // the original vector.
  std::list<OrientedCSkeletonSegment*> copy;
  copy.insert(copy.begin(), oriented_segments.begin(), oriented_segments.end());
  // oofcerr << "CSkeletonEdgeBoundary::map: oldbdy=" << derefprint(copy)
  // 	  << std::endl;

  while(!copy.empty()) {
    OrientedCSkeletonSegment *e = copy.front();
    SelectableMap m;
    CSkeletonSelectableList *map_start, *map_end;
    // oofcerr << "CSkeletonEdgeBoundary::map: e=" << *e << std::endl;
    
    if(direction == MAP_DOWN) {
      e->get_segment()->map(m); // computes SelectableMap m
      map_start = &m.source;
      map_end = &m.target;
    }
    else {			// direction == MAP_UP
      if(e->get_segment()->getParents().empty()) {
	copy.pop_front();
	continue;
      }
      e->get_segment()->getParents().front()->map(m);
      map_start = &m.target;
      map_end = &m.source;
    }

    // oofcerr << "CSkeletonEdgeBoundary::map: map_start="
    // 	    << derefprint(*map_start) << std::endl;
    // oofcerr << "CSkeletonEdgeBoundary::map: map_end="
    // 	    << derefprint(*map_end) << std::endl;

    OrientedCSkeletonSegmentVector new_oriented_segs;
    if(map_start->size() == 1) {
      // oofcerr << "CSkeletonEdgeBoundary::map: one to many" << std::endl;
      // One-to-many case -- Sequence and create oriented segments
      if(!getOrientedSegs(e, map_end, direction, new_oriented_segs)) {
	throw ErrProgrammingError("Unable to get Oriented Segments",
				  __FILE__, __LINE__);
      }
      // oofcerr << "CSkeletonEdgeBoundary::map: new_oriented_segs="
      // 	      << derefprint(new_oriented_segs) << std::endl;
      new_bdy->appendSegs(new_oriented_segs);
      copy.pop_front();
    } // end if map_start->size() == 1

    else {
      // oofcerr << "CSkeletonEdgeBoundary::map: many to some" << std::endl;
      // Many-to-one or many-to-many case.  First, find all the edges
      // of this bdy in the parent part.
      OrientedCSkeletonSegmentSet source_set;
      source_set.insert(e);
      for(std::list<OrientedCSkeletonSegment*>::iterator os=copy.begin();
      	  os!=copy.end(); ++os) 
	{
	  for(CSkeletonSelectableList::iterator seg=map_start->begin(); 
	      seg!=map_start->end(); ++seg) 
	    {
	      // TODO OPT: Is is ok to compare pointers here and skip a
	      // level of dereferencing?
	      if(*(*os)->get_segment() == *(*seg)) {
		source_set.insert(*os);
		break;
	      }
	    }
	}
      // oofcerr << "CSkeletonEdgeBoundary::map: source_set="
      // 	      << derefprint(source_set) << std::endl;


      // Remove these edges from copy and rebuild map_start to
      // correspond to source_set.
      map_start->clear();      
      for(OrientedCSkeletonSegmentSet::iterator os=source_set.begin(); 
      	  os!=source_set.end(); ++os) 
	{
	  std::list<OrientedCSkeletonSegment*>::iterator it =
	    std::find(copy.begin(), copy.end(), *os);
	  if(it != copy.end()) {
	    copy.erase(it);
	    map_start->push_back((*os)->get_segment());
	  }
	}
      // oofcerr << "CSkeletonEdgeBoundary::map: rebuilt map_start="
      // 	      << derefprint(*map_start) << std::endl;

      // Sequence the source segments -- this is the path the original
      // boundary takes through the source part of the map.
      //* TODO OPT: Is this necessary?
      CSkeletonSegmentVector sequenced_segs;
      CSkeletonNodeVector sequenced_nodes;
      if(!OrientedCSkeletonSegment::segSequence(map_start, e->getNode(0),
						sequenced_segs,
						sequenced_nodes))
	{
	  // oofcerr << "CSkeletonEdgeBoundary::map: no sequence" << std::endl;
	  continue; 
	}      

      // TODO 3.1: This is a simplified translation of the python
      // code. Update if necessary.

      // Direct the resulting edge-sequence correctly. (necessary?)

      // Rebuild the target set to correspond to the rebuilt source.

      // TODO MER: The comment on this section in oof2 was: "Extract
      // the subset of the target that has some relation to the
      // boundary part of the parent."  The rebuilt target is not
      // necessarily a subset!
      CSkeletonSelectableList rebuilt_target;
      for(CSkeletonSegmentVector::iterator s=sequenced_segs.begin();
	  s!=sequenced_segs.end(); ++s)
	{
	  CSkeletonSelectableList &kin = (direction==MAP_DOWN ? 
					  (*s)->getChildren() :
					  (*s)->getParents());
	  for(CSkeletonSelectableList::iterator c=kin.begin(); c!=kin.end();
	      ++c)
	    {
	      if(std::find(rebuilt_target.begin(), rebuilt_target.end(), *c)
		 == rebuilt_target.end())
		{
		  rebuilt_target.push_back(*c);
		}
	    }
	}
      // oofcerr << "CSkeletonEdgeBoundary::map: rebuilt_target="
      // 	      << derefprint(rebuilt_target) << std::endl;

      // Find the counterparts of the endpoints of the original path,
      // if they exist and are unique, otherwise fail.
      CSkeletonSelectableList &start_shadow =
	sequenced_nodes.front()->getRelatives(direction);
      CSkeletonSelectableList &end_shadow =
	sequenced_nodes.back()->getRelatives(direction);
      CSkeletonNode *target_start, *target_end;
      // oofcerr << "CSkeletonEdgeBoundary::map: start_shadow=" 
      // 	      << derefprint(start_shadow) << std::endl;
      // oofcerr << "CSkeletonEdgeBoundary::map: end_shadow="
      // 	      << derefprint(end_shadow) << std::endl;
      if(start_shadow.size() == 1) {
	target_start = dynamic_cast<CSkeletonNode*>(start_shadow.front());
	// oofcerr << "CSkeletonEdgeBoundary::map: target_start="
	// 	<< *target_start << std::endl;
      }
      else {
	continue;
      }
      if(end_shadow.size()==1) {
	target_end = dynamic_cast<CSkeletonNode*>(end_shadow.front());
	// oofcerr << "CSkeletonEdgeBoundary::map: target_end="
	// 	<< *target_end << std::endl;
	}
      else {
	continue;
      }
      if(*target_start == *target_end) {
	// oofcerr << "CSkeletonEdgeBoundary::map: target_start==target_end"
	// 	<< std::endl;
	continue;
      }
      // oofcerr << "CSkeletonEdgeBoundary::map: shadows ok" << std::endl;
	
      // Find the paths in the target segment set. Using segSequence for now.
      sequenced_segs.clear();
      sequenced_nodes.clear();
      if(!OrientedCSkeletonSegment::segSequence(&rebuilt_target, target_start,
						sequenced_segs,
						sequenced_nodes)) 
	{
	  // oofcerr << "CSkeletonEdgeBoundary::map: sequencing failed"
	  // 	  << std::endl;
	  continue; 
	}      
      // oofcerr << "CSkeletonEdgeBoundary::map: sequenced_segs="
      // 	      << derefprint(sequenced_segs) << std::endl;
      // oofcerr << "CSkeletonEdgeBoundary::map: sequenced_nodes="
      // 	      << derefprint(sequenced_nodes) << std::endl;
      // Now create edges from the sequenced set of target segments
      // and add them to the boundary.
      for(unsigned int i=0; i<sequenced_segs.size(); ++i) {
	if(sequenced_segs[i]->getNode(0) == sequenced_nodes[i])
	  new_oriented_segs.push_back(
		      new OrientedCSkeletonSegment(sequenced_segs[i], 1));
	else
	  new_oriented_segs.push_back(
		      new OrientedCSkeletonSegment(sequenced_segs[i], -1));
      }
      // oofcerr << "CSkeletonEdgeBoundary::map: new_oriented_segs="
      // 	      << derefprint(new_oriented_segs) << std::endl;
      new_bdy->appendSegs(new_oriented_segs);

    } // end map_start->size() > 1

  } // end while !copy.empty()

#ifdef DEBUG
  CSkeletonSegmentVector sequenced_segs;
  CSkeletonNodeVector sequenced_nodes;
  CSkeletonSelectableList new_bdy_segs;
  for(OrientedCSkeletonSegmentVector::const_iterator
	i=new_bdy->getOrientedSegments()->begin(); 
      i!=new_bdy->getOrientedSegments()->end(); ++i)
    {
      new_bdy_segs.push_back((*i)->get_segment());
    }
  if(!OrientedCSkeletonSegment::segSequence(&new_bdy_segs, NULL,
					    sequenced_segs, sequenced_nodes))
    {
      oofcerr << "CSkeletonEdgeBoundary::map: unsequencable mapped boundary!"
	      << std::endl;
      for(CSkeletonSelectableList::const_iterator i=new_bdy_segs.begin();
	  i!=new_bdy_segs.end(); ++i)
	{
	  oofcerr << "CSkeletonEdgeBoundary::map: seg=" << *(*i) << std::endl;
	}
      throw ErrProgrammingError(
			"Mapped boundary " + name_ + " is not sequenceable",
			__FILE__, __LINE__);
    }
#endif	// DEBUG

  // oofcerr << "CSkeletonEdgeBoundary::map: done" << std::endl;
  return new_bdy;
} // end CSkeletonEdgeBoundary::map


// getOrientedSegs() returns a list of edges with the properties that:
//   - The target list edges trace a path from the edge's start node
//                       to the edge's stop node.
//   - The target edge's segments are related (parents if
//                       direction is up, children if direction
//                       is down) to the edge's segment.
//   - The new edges are directed correctly from start to finish.
// getOrientedSegs() is a static method in CSkeletonEdgeBoundary.
bool CSkeletonEdgeBoundary::getOrientedSegs(
			    OrientedCSkeletonSegment *s,
			    CSkeletonSelectableList *target_segs, 
			    SkeletonMapDir direction,
			    OrientedCSkeletonSegmentVector &result)
{
  // oofcerr << "getOrientedSegs: s= " << *s << std::endl;
  // oofcerr << "getOrientedSegs: target_segs= "
  // 	  << derefprint(*target_segs) << std::endl;
  // oofcerr << "getOrientedSegs: direction=" << direction << std::endl;


  result.clear();

  if(target_segs->empty())
    return true;

  CSkeletonSegmentVector sequenced_segs;
  CSkeletonNodeVector sequenced_nodes;
  if(!OrientedCSkeletonSegment::segSequence(target_segs, NULL, sequenced_segs,
					    sequenced_nodes)) 
    {
      return false;
    }
  // oofcerr << "getOrientedSegs: sequenced_segs="
  // 	  << derefprint(sequenced_segs) << std::endl;
  // oofcerr << "getOrientedSegs: sequenced_nodes="
  // 	  << derefprint(sequenced_nodes) << std::endl;

  CSkeletonSelectableList &target_start=s->getNode(0)->getRelatives(direction);
  if(target_start.size() == 0) {
    throw ErrProgrammingError(
	      "Can't find related nodes for " + to_string(*s->getNode(0)),
	      __FILE__, __LINE__);
  }
  if(sequenced_nodes.back()->inList(target_start)) {
    // oofcerr << "getOrientedSegs: reversing" << std::endl;
    std::reverse(sequenced_segs.begin(), sequenced_segs.end());
    std::reverse(sequenced_nodes.begin(), sequenced_nodes.end());
  }
  else {
    // In cases of boundaries that are loops, when no starting node is
    // passed in, segSequence makes an arbitrary choice for the
    // starting node that can be incorrect, but otherwise sequences
    // the boundary correctly.  In this case, we must re-sequence the
    // list.  The alternative is to pass in a target start to
    // segSequence and then handle the case where the target start is
    // not in the node list in there, but that seems more complicated.

    // calculate overlap between node_list and target_start.
    // TODO 3.1: consider creating general intersection function for
    // containers of selectables
    CSkeletonNodeVector overlap;
    for(CSkeletonNodeIterator n=sequenced_nodes.begin();
	n!=sequenced_nodes.end(); ++n)
      {
      if((*n)->inList(target_start))
	overlap.push_back(*n);
      }
    if(!overlap.empty()) {
      if(!OrientedCSkeletonSegment::segSequence(target_segs, NULL,
						sequenced_segs,
						sequenced_nodes))
	return false;
    }
    else
      throw ErrProgrammingError(
		"Malformed segment sequence -- node counterpart not found.",
		__FILE__, __LINE__); 
  }

  for(unsigned int i=0; i<sequenced_segs.size(); ++i) {
    if(sequenced_segs[i]->getNode(0) == sequenced_nodes[i])
      result.push_back(new OrientedCSkeletonSegment(sequenced_segs[i], 1));
    else
      result.push_back(new OrientedCSkeletonSegment(sequenced_segs[i], -1));
  }
  return true;

} // end CSkeletonEdgeBoundary::getOrientedSegs

void CSkeletonEdgeBoundary::reverse() {
  std::reverse(oriented_segments.begin(), oriented_segments.end());
  for(OrientedCSkeletonSegmentVector::iterator i=oriented_segments.begin();
      i!=oriented_segments.end(); ++i)
    {
      (*i)->reverse();
    }
}

CSkeletonNodeVector *CSkeletonEdgeBoundary::getNodes() const {
  CSkeletonNodeVector *nodes = new CSkeletonNodeVector();
  for(OrientedCSkeletonSegmentVector::const_iterator i=oriented_segments.begin();
      i!=oriented_segments.end(); ++i)
    {
      nodes->push_back((*i)->getNode(0));
    }
  if(oriented_segments.back()->getNode(1) != (*nodes)[0]) {
    nodes->push_back(oriented_segments.back()->getNode(1));
  }
  return nodes;
}

double CSkeletonEdgeBoundary::length() const {
  double ell = 0;
  for(OrientedCSkeletonSegmentVector::const_iterator i=oriented_segments.begin();
      i!=oriented_segments.end(); ++i)
    {
      ell += (*i)->get_segment()->length();
    }
  return ell;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonFaceBoundary::CSkeletonFaceBoundary(const std::string &n)
  : CSkeletonBoundary(n)
{}

CSkeletonFaceBoundary::~CSkeletonFaceBoundary() {
  delete oriented_faces;
};

int CSkeletonFaceBoundary::size() const {
  return oriented_faces->size();
}

bool CSkeletonFaceBoundary::empty() const {
  return oriented_faces->empty();
}

void CSkeletonFaceBoundary::addOrientedFace(OrientedCSkeletonFace *s) {
  oriented_faces->insert(s);
}

void CSkeletonFaceBoundary::remove() {
  oriented_faces->clear();
}

void CSkeletonFaceBoundary::setSurface(OrientedSurface *surf) {
  // Only called by CSkeleton::getFaceBoundary().  Takes ownership of
  // the given OrientedSurface.
  oriented_faces = surf;
}

CSkeletonFaceVector *CSkeletonFaceBoundary::getUnorientedFaces() const {
  CSkeletonFaceVector *faces = new CSkeletonFaceVector();
  for(OrientedCSkeletonFaceSet::const_iterator i=oriented_faces->begin();
      i!=oriented_faces->end(); ++i)
    {
      faces->push_back((*i)->get_face());
    }
  return faces;
}

bool CSkeletonFaceBoundary::try_appendFaces(const CSkeletonBase *skel,
					    const CSkeletonFaceVector *faces)
  const
{
  // TODO OPT: This may be too slow.  It doesn't use the orientation
  // information that's been computed for the existing faces in the
  // boundary.
  CSkeletonFaceVector *allFaces = getUnorientedFaces();
  allFaces->insert(allFaces->end(), faces->begin(), faces->end());
  OrientedSurface *surface = orientFaces(skel, allFaces, 
					 (OrientedCSkeletonFace*) 0);
  bool status = (surface != 0);
  delete surface;
  delete allFaces;
  return status;
}

void CSkeletonFaceBoundary::appendFaces(const OrientedCSkeletonFaceSet &faces) {
  oriented_faces->insert(faces.begin(), faces.end());
}

void CSkeletonFaceBoundary::appendFaces(const CSkeletonBase *skel,
					const CSkeletonFaceVector *faces) 
{
  // Similar to orientFaces in cskeletonface.C, except that we already
  // know the orientation of the pre-existing faces.
  assert(!empty());
  // Make a map from segments to faces for the new faces.
  SegFaceListMap facemap;
  for(CSkeletonFaceVector::const_iterator f=faces->begin(); f!=faces->end();
      ++f)
    {
      CSkeletonFace *face = *f;
      // Loop over the segments of the face.
      CSkeletonSegmentSet segs;
      skel->getFaceSegments(face, segs);
      for(CSkeletonSegmentSet::const_iterator s=segs.begin(); s!=segs.end();
	  ++s)
	{
	  CSkeletonSegment *seg = *s;
	  // Look for the list of faces for the current segment
	  SegFaceListMap::iterator fl = facemap.find(*s);
	  if(fl != facemap.end()) {
	    // Put the current face in the list.
	    (*fl).second.push_back(face);
	  }
	  else {
	    // Make a new list and put the face in it.
	    facemap[seg] = CSkeletonFaceList(1, face);
	  }
	} // end loop over segments s
    } // end loop over faces f

  // Check (a) that no segments have more than two faces and (b) that
  // some faces have just one segment.  Otherwise the new faces can't
  // be added to the old ones, or won't form a surface if they are.
  bool closed = true;
  for(SegFaceListMap::iterator sf=facemap.begin(); sf!=facemap.end(); ++sf) {
    int nsegs = (*sf).second.size();
    if(nsegs > 2)
      throw ErrUserError("Too many faces per segment!");
    if(nsegs == 1)
      closed = false;
  }
  if(closed)
    throw ErrUserError("Additional faces form a closed surface.");

  // Compute the initial "active" perimeter, to which new faces can be
  // added, by looping over the preexisting faces and finding the
  // segments with only one face.
  SegFaceMap activeFaces;
  // Loop over existing faces
  for(OrientedCSkeletonFaceSet::const_iterator f=oriented_faces->begin();
      f!=oriented_faces->end(); ++f)
    {
      OrientedCSkeletonFace *oface = *f;
      CSkeletonSegmentSet segs;
      skel->getFaceSegments(oface->get_face(), segs);
      // Loop over segments of a face
      for(CSkeletonSegmentSet::const_iterator s=segs.begin(); s!=segs.end();
	  ++s)
	{
	  // If this segment has been seen before, remove it from the
	  // SegFaceMap.  It's not a perimeter segment.  If it hasn't
	  // been seen before, it might be a perimeter segment, so put
	  // in in the map.
	  SegFaceMap::iterator sfmi = activeFaces.find(*s);
	  if(sfmi == activeFaces.end())
	    activeFaces[*s] = oface;
	  else
	    activeFaces.erase(sfmi);
	}
    } // end loop over faces
  
  // If there is nothing left in activeFaces, then the existing
  // boundary is closed, and we can't add anything to it.
  if(activeFaces.empty())
    throw ErrUserError("It's not possible to add faces to a closed boundary");

  // Construct the perimeter.
  CSkeletonSegmentSet activePerimeter;
  for(SegFaceMap::iterator i=activeFaces.begin(); i!=activeFaces.end(); ++i) {
    CSkeletonSegment *seg = (*i).first;
    CSkeletonFace *face = (*i).second->get_face();
    activePerimeter.insert(seg);
    // facemap needs to include all (segment, face) pairs that might
    // be used, including the ones on the old perimeter.
    SegFaceListMap::iterator sfmi = facemap.find(seg);
    if(sfmi == facemap.end())
      facemap[seg] = CSkeletonFaceList(1, face);
    else
      (*sfmi).second.push_back(face);
  }

  if(!augmentSurface(skel, activePerimeter, activeFaces, facemap,
		     oriented_faces))
    {
      throw ErrUserError("The surface is not orientable.");
    }
} // end CSkeletonFaceBoundary::appendFaces

bool CSkeletonFaceBoundary::try_removeFaces(const CSkeletonBase *skel,
					    const CSkeletonFaceVector *faces)
  const
{
  CSkeletonFaceVector *oldFaces = getUnorientedFaces();
  for(CSkeletonFaceVector::const_iterator i=faces->begin(); i!=faces->end();
      ++i)
    {
      for(CSkeletonFaceVector::iterator j=oldFaces->begin(); j!=oldFaces->end();
	  ++j)
	{
	  if(*i == *j) {
	    oldFaces->erase(j);
	    break;
	  }
	}
      // If a face in faces isn't in oldFaces, that's ok.  Ignore it.
    }
  OrientedSurface *surface = orientFaces(skel, oldFaces, 
					 (OrientedCSkeletonFace*) 0);
  bool status = (surface != 0);
  delete surface;
  delete oldFaces;
  return status;
}

void CSkeletonFaceBoundary::removeFaces(const CSkeletonBase *skel,
					const CSkeletonFaceVector *faces)
{
  for(CSkeletonFaceVector::const_iterator i=faces->begin(); i!=faces->end();
      ++i)
    {
      oriented_faces->remove(*i);
    }
}

const OrientedCSkeletonFaceSet *CSkeletonFaceBoundary::getFaces() const {
  // oofcerr << "CSkeletonFaceBoundary::getFaces: " << &oriented_faces->faces
  // 	  << " size=" << oriented_faces->faces.size();
  // for(OrientedCSkeletonFaceSet::const_iterator i=oriented_faces->faces.begin();
  //     i!=oriented_faces->faces.end(); ++i)
  //   oofcerr << " " << *i;
  // oofcerr << std::endl;
  return &oriented_faces->faces;
}

CSkeletonFaceBoundary* CSkeletonFaceBoundary::map(CSkeleton *new_skeleton, 
						  SkeletonMapDir direction,
						  bool exterior) 
{
  typedef std::map<CSkeletonFace*, OrientedCSkeletonFaceSet> SourceMap;
  SourceMap srcmap;
  // Keep track of the unoriented faces in the old boundary. Here
  // "old" refers to the boundary which was already defined, and "new"
  // is the boundary which we're defining now.  Depending on the given
  // mapping direction, either one may be the parent or child of the
  // other.
  CSkeletonFaceSet oldfaces;
  // Loop over this boundary's oriented faces
  for(OrientedCSkeletonFaceSet::iterator it=oriented_faces->begin();
      it!=oriented_faces->end(); ++it)
    {
      CSkeletonFace *oldface = (*it)->get_face();
      oldfaces.insert(oldface);
      // Get the faces in the new boundary corresponding to the
      // current face in the old boundary.
      CSkeletonSelectableList &nfl = oldface->getRelatives(direction);
      // For each face in the new boundary, create an entry in srcmap
      // that lists the corresponding OrientedCSkeletonFace(s) in the
      // old boundary.
      for(CSkeletonSelectableList::const_iterator nf=nfl.begin(); nf!=nfl.end();
	  ++nf)
	{
	  CSkeletonFace *newface = dynamic_cast<CSkeletonFace*>(*nf);
	  // oofcerr << "CSkeletonFaceBoundary::map:"
	  // 	  << " defunct=" << newface->is_defunct()
	  // 	  << " newface=" << *newface
	  // 	  << std::endl;
	  SourceMap::iterator smi = srcmap.find(newface);
	  if(smi == srcmap.end()) {
	    srcmap[newface] = OrientedCSkeletonFaceSet();
	    srcmap[newface].insert(*it);
	  }
	  else
	    (*smi).second.insert(*it);
	}
    }

  // Create a vector containing the faces in the new boundary.  We have
  // to find the orientation for one of them so that the orientation
  // of the new boundary can be the same as the orientation of the old
  // one.
  CSkeletonFaceVector newFaces;
  double maxdot = -2;
  CSkeletonFace *startFace = 0;
  int startDir = 0;
  for(SourceMap::iterator smi=srcmap.begin(); smi!=srcmap.end(); ++smi) {
    CSkeletonFace *newface = (*smi).first;
    CSkeletonSelectableList &rels = newface->getRelatives(
						  otherMapDir(direction));

    // This works differently than propagating selections, in which a
    // new object is selected only if all of its parents are selected.
    // That is the wrong thing to do for boundaries.  If a boundary
    // face has two parents, only one of which is part of the
    // boundary, leaving it out might create a hole in the boundary.
    // For predefined boundaries (top, bottom, etc) this would be bad.
    bool ok = false;
    for(CSkeletonSelectableList::iterator r=rels.begin(); r!=rels.end() && !ok;
	++r)
      {
	CSkeletonFace *relative = dynamic_cast<CSkeletonFace*>(*r);
	CSkeletonFaceSet::iterator i=oldfaces.find(relative);
	if(i!=oldfaces.end()) {
	  ok = true;
	  break;
	}
      }
    if(ok) {
      newFaces.push_back(newface);
      // Loop over the old oriented faces that correspond to the new
      // face and check their alignment.  The face with the best
      // alignment will be the one that sets the orientation for the
      // entire new surface.
      Coord normal(newface->normal());
      OrientedCSkeletonFaceSet &oldofaces = (*smi).second;
      for(OrientedCSkeletonFaceSet::iterator j=oldofaces.begin();
	  j!=oldofaces.end(); ++j)
	{
	  Coord olddir = (*j)->get_direction_vector();
	  double dotp = dot(normal, olddir);
	  if(fabs(dotp) > maxdot) {
	    maxdot = fabs(dotp);
	    startFace = newface;
	    startDir = dotp > 0 ? 1 : -1;
	  }
	}
    }
  }
  assert(!newFaces.empty());
  assert(startFace != 0);
  assert(startDir != 0);

  OrientedCSkeletonFace *startOFace = 
    new OrientedCSkeletonFace(startFace, startDir);
  // orientFaces returns a new'd OrientedSurface instance.
  OrientedSurface *surface = orientFaces(new_skeleton, &newFaces, startOFace);

  return new_skeleton->makeFaceBoundary(name_, surface, exterior);
} // end CSkeletonFaceBoundary::map


double CSkeletonFaceBoundary::area() const {
  double a = 0;
  for(OrientedCSkeletonFaceSet::iterator it=oriented_faces->begin();
      it!=oriented_faces->end(); ++it) 
    {
      a += (*it)->get_face()->area();
    }
  return a;
}

void CSkeletonFaceBoundary::reverse() {
  for(OrientedCSkeletonFaceSet::iterator it=oriented_faces->begin();
      it!=oriented_faces->end(); ++it)
    {
      (*it)->reverse();
    }
}

bool CSkeletonFaceBoundary::hasFace(const CSkeletonFace *face) const {
  // TODO OPT: Looping over a std::set to look for an entry is silly, but
  // the set is a set of oriented faces, and we are given an
  // unoriented one.  If the set's comparator function used the
  // unoriented face, could we use fast set lookup for this?  Does it
  // matter? This isn't going to be used in critical parts of the
  // code.
  // TODO 3.1: Use std::find_if instead of an explicit loop.
  for(OrientedCSkeletonFaceSet::iterator it=oriented_faces->begin();
      it!=oriented_faces->end(); ++it)
    {
      if(face == (*it)->get_face())
	return true;
    }
  return false;
}
