// -*- C++ -*-
// $RCSfile: edgeset.C,v $
// $Revision: 1.22.4.7 $
// $Author: langer $
// $Date: 2014/11/05 16:54:24 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/cleverptr.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/edge.h"
#include "engine/edgeset.h"
#include "engine/node.h"
#include "engine/ooferror.h"
#include <algorithm>		// for std::reverse

SubDimensionalSet::SubDimensionalSet(FEMesh *m) : mesh(m) {}

void SubDimensionalSet::add(Element *el, bool reversed) {
  parts.push_back(el);
  directions.push_back(reversed);
  // We used to require that EdgeSets contained only contiguous edges,
  // which was enforced by the code below.  The interface branch
  // relaxed that constraint, but that may be a bad idea.  If the
  // edges don't have to be contiguous and simply connected, the
  // lengths computed by EdgeSetIterator don't make sense, so the
  // class structure must be incorrect.  TODO 3.1: Fix this.  Fixing may
  // require that add() become a virtual function with different
  // definitions in FaceSet and EdgeSet.

  // if(edgelist.empty()) {
  //   edgelist.push_back(ed_in);  // Add to back.
  // }
  // else {
  //   BoundaryEdge *lastedge = edgelist[edgelist.size()-1];
  //   if ( *(lastedge->endnode()) == *(ed_in->startnode()) ) {
  //     edgelist.push_back(ed_in);
  //   }
  //   else {
  //     throw ErrProgrammingError("Non-contiguous edges passed to edgeset.",
  // 				__FILE__, __LINE__);
  //   }
  // }
}

SubDimensionalIterator::SubDimensionalIterator(const SubDimensionalSet *b)
  : bdy(b),
    index_(0)
{}

// Build a big list of node pointers, and pass it out.  Let
// the caller (presumed to be a Python routine) iterate over it.
// This is where we fulfill the promise of uniqueness.
// ndlist() is called by _EdgeSet_build_caches_ in edgeset.spy.

std::vector<const EdgeNodeDistance*> *EdgeSet::ndlist() {
  // This object gets deleted by the copy-out typemap in edgeset.swg
  std::vector<const EdgeNodeDistance*> *elist = 
    new std::vector<const EdgeNodeDistance*>;

  //  Trace("EdgeSet::ndlist");
  EdgeSetIterator i = EdgeSetIterator(this);
  double bdy_length = i.total_length();
  int index = 0;
  for(; !i.end(); ++i) {	// loop over edges
    // Loop over nodes in the edge.  We might be going in reverse, so
    // first get a list of nodes.
    std::vector<FuncNode*> nodes;
    nodes.reserve(i.edge()->nfuncnodes());
    for(CleverPtr<ElementFuncNodeIterator> n(i.edge()->funcnode_iterator()); 
	!n->end(); ++*n) 
      {
	nodes.push_back(n->funcnode());
      }
    // Reverse the nodes if necessary.
    if(i.reversed()) 
      std::reverse(nodes.begin(), nodes.end());
    for(std::vector<FuncNode*>::iterator n=nodes.begin(); n!=nodes.end(); ++n) {
      int listsize = elist->size();
      if((listsize == 0) || (*elist)[listsize-1]->node != *n) {
	// Distance to this node from the beginning of the undistorted
	// boundary.
	double distance = i.traversed_length() + 
	  sqrt(norm2((*n)->position() - nodes[0]->position()));
	double fraction = distance/bdy_length;
	elist->push_back(new EdgeNodeDistance(*n, index, distance, fraction));
	index++;
      }
    } // end loop over nodes in the edge in boundary order
  }   // end loop over edges
  return elist;
}

//--\\||//--\\||//--\\||//--\\||//--\\||//--\\||//--\\||//--\\||

SubDimensionalIterator *EdgeSet::iterator() const {
  return new EdgeSetIterator(this);
}

// EdgeSetIterators.  We assume that, during the lifetime of the
// EdgeSetIterator, the nodes do not move, so we can reasonably
// compute the proper (lab-space) length of individual edges, and the
// cumulative length of the set.

EdgeSetIterator::EdgeSetIterator(const EdgeSet *b)
  : SubDimensionalIterator(b),
    length(0.0)
{
  cumulength_.reserve(bdy->size());

  // Loop over all the edges in the EdgeSet, and total up their
  // lengths.  At the end, cumulength[i] is the length of all the
  // previous edges up to but not including the edge indexed by i.
  const EdgeSet *eset = dynamic_cast<const EdgeSet*>(bdy);
  for (std::vector<Element*>::const_iterator i=eset->parts.begin();
       i!=eset->parts.end(); ++i) 
    {
      cumulength_.push_back(length);
      length += (*i)->span();
    }
}

std::ostream &operator<<(std::ostream &os, const EdgeSetIterator &esi) {
  return os << "EdgeSetIterator(" << esi.traversed_length() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==3

std::set<Node*> *FaceSet::getNodes() const {
  std::set<Node*> *nodeset = new std::set<Node*>;
  for(std::vector<Element*>::const_iterator f=parts.begin(); 
      f!=parts.end(); ++f)
    {
      for(CleverPtr<ElementFuncNodeIterator> n((*f)->funcnode_iterator());
	  !n->end(); ++*n)
	{
	  nodeset->insert(n->funcnode());
	}
    }
  return nodeset;
}

SubDimensionalIterator *FaceSet::iterator() const {
  return new FaceSetIterator(this);
}

#endif // DIM==3
