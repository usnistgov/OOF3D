// -*- C++ -*-
// $RCSfile: canonicalorder.C,v $
// $Revision: 1.1.4.6 $
// $Author: langer $
// $Date: 2011/10/05 20:59:32 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "engine/canonicalorder.h"

// CanonicalOrderMapper::getNodes(sig)[i] is an element node index
// that refers to a node with the same role for every
// RefinementSignature in a set of equivalent signatures.  For
// example, for all of the signatures that mark two adjacent edges,
// CanonicalOrderMapper::getNodes(sig)[1] is node shared by the two
// edges.  CanonicalOrderMapper::getSegs() works the same way, for
// element edges.

// CanonicalOrderMapper::createCanonicalOrderMap defines the mapping.
// Each line in createCanonicalOrderMap is of the form:
///   canonicalOrderMap[signature] = CanonicalOrder(nodes, segs)
// where signature is a RefinementSignature or a vector of indices.
// There must be a line for every possible refinement signature
// (unless the refinement rule is so simple that it doesn't require a
// map).  'nodes' is a vector of node indices, where nodes[i] is the
// element index of the node that plays the role i for an element with
// the given signature.  If a refinement rule doesn't use all of the
// nodes, the 'nodes' list doesn't have to be complete.

static IndexVec getIV(short a, short b) {
  IndexVec iv;
  iv.push_back(a);
  iv.push_back(b);
  return iv;
};

static IndexVec getIV(short a, short b, short c) {
  IndexVec iv;
  iv.push_back(a);
  iv.push_back(b);
  iv.push_back(c);
  return iv;
}; 

static IndexVec getIV(short a, short b, short c, short d) {
  IndexVec iv;
  iv.push_back(a);
  iv.push_back(b);
  iv.push_back(c);
  iv.push_back(d);
  return iv;
};

static IndexVec getIV(short a, short b, short c, short d, short e) {
  IndexVec iv;
  iv.push_back(a);
  iv.push_back(b);
  iv.push_back(c);
  iv.push_back(d);
  iv.push_back(e);
  return iv;
};

static IndexVec getIV(const IndexPairVec &sig) {
  IndexVec iv;
  for(unsigned int i=0; i<sig.size(); ++i) 
    iv.push_back(sig[i].first);
  return iv;
}


bool CanonicalOrderMapper::canonicalOrderMapCreated = false;
CanonicalOrderMap CanonicalOrderMapper::canonicalOrderMap;

const IndexVec& CanonicalOrderMapper::getNodes(const IndexVec &sig) {
  if(!canonicalOrderMapCreated) 
    CanonicalOrderMapper::createCanonicalOrderMap();
  return canonicalOrderMap[sig].nodes;
}

const IndexVec& CanonicalOrderMapper::getNodes(const IndexPairVec &sig) {
  return getNodes(getIV(sig));
}

const IndexVec& CanonicalOrderMapper::getSegs(const IndexVec &sig) {
  if(!canonicalOrderMapCreated)
    CanonicalOrderMapper::createCanonicalOrderMap();
  return canonicalOrderMap[sig].segs;
}

const IndexVec& CanonicalOrderMapper::getSegs(const IndexPairVec &sig) {
  return getSegs(getIV(sig));
}

void CanonicalOrderMapper::createCanonicalOrderMap() {
  // Tet2EdgesAdjacent: two adjacent edges on the tet are marked.  The
  // segments can be in numerical order, we want the first node to be
  // the unshared node on the first edge, the second node to be the
  // shared node, and the last node to be the remaining node on the
  // second edge.
  canonicalOrderMap[getIV(0,1)] = CanonicalOrder(getIV(0,1,2), getIV(0,1));
  canonicalOrderMap[getIV(0,2)] = CanonicalOrder(getIV(1,0,2), getIV(0,2));
  canonicalOrderMap[getIV(0,3)] = CanonicalOrder(getIV(1,0,3), getIV(0,3));
  canonicalOrderMap[getIV(0,4)] = CanonicalOrder(getIV(0,1,3), getIV(0,4));
  canonicalOrderMap[getIV(1,2)] = CanonicalOrder(getIV(1,2,0), getIV(1,2));
  canonicalOrderMap[getIV(1,4)] = CanonicalOrder(getIV(2,1,3), getIV(1,4));
  canonicalOrderMap[getIV(1,5)] = CanonicalOrder(getIV(1,2,3), getIV(1,5));
  canonicalOrderMap[getIV(2,3)] = CanonicalOrder(getIV(2,0,3), getIV(2,3));
  canonicalOrderMap[getIV(2,5)] = CanonicalOrder(getIV(0,2,3), getIV(2,5));
  canonicalOrderMap[getIV(3,4)] = CanonicalOrder(getIV(0,3,1), getIV(3,4));
  canonicalOrderMap[getIV(3,5)] = CanonicalOrder(getIV(0,3,2), getIV(3,5));
  canonicalOrderMap[getIV(4,5)] = CanonicalOrder(getIV(1,3,2), getIV(4,5));

  // Tet3EdgesTriangle: The three marked edges are all on one face.
  // We want the three nodes traversing the face in the same order
  canonicalOrderMap[getIV(0,3,4)] = CanonicalOrder(getIV(1,0,3), getIV(0,3,4));
  canonicalOrderMap[getIV(0,1,2)] = CanonicalOrder(getIV(0,1,2), getIV(0,1,2));
  canonicalOrderMap[getIV(2,3,5)] = CanonicalOrder(getIV(2,0,3), getIV(2,3,5));
  canonicalOrderMap[getIV(1,4,5)] = CanonicalOrder(getIV(2,1,3), getIV(1,4,5));

  // Tet3EdgesZigZag: The three marked edges span all four faces and
  // all four nodes, with two of the nodes being on only one marked
  // edge.  We want the segs in an order such as the seg that is
  // connected to the other two is second.  We want the nodes in the
  // corresponding order.
  canonicalOrderMap[getIV(0,2,4)] = CanonicalOrder(getIV(2,0,1,3),getIV(2,0,4));
  canonicalOrderMap[getIV(0,1,5)] = CanonicalOrder(getIV(0,1,2,3),getIV(0,1,5));
  canonicalOrderMap[getIV(0,1,3)] = CanonicalOrder(getIV(3,0,1,2),getIV(3,0,1));
  canonicalOrderMap[getIV(1,2,4)] = CanonicalOrder(getIV(3,1,2,0),getIV(4,1,2));
  canonicalOrderMap[getIV(0,2,5)] = CanonicalOrder(getIV(3,2,0,1),getIV(5,2,0));
  canonicalOrderMap[getIV(1,2,3)] = CanonicalOrder(getIV(1,2,0,3),getIV(1,2,3));
  canonicalOrderMap[getIV(1,3,5)] = CanonicalOrder(getIV(1,2,3,0),getIV(1,5,3));
  canonicalOrderMap[getIV(2,3,4)] = CanonicalOrder(getIV(2,0,3,1),getIV(2,3,4));
  canonicalOrderMap[getIV(0,4,5)] = CanonicalOrder(getIV(0,1,3,2),getIV(0,4,5));
  canonicalOrderMap[getIV(1,3,4)] = CanonicalOrder(getIV(2,1,3,0),getIV(1,4,3));
  canonicalOrderMap[getIV(0,3,5)] = CanonicalOrder(getIV(1,0,3,2),getIV(0,3,5));
  canonicalOrderMap[getIV(2,4,5)] = CanonicalOrder(getIV(0,2,3,1),getIV(2,5,4));

  // Tet3Edges1Node: The first three nodes are on the segments
  // given by the signature.  These must be in an order
  // which defines a normal pointing towards the fourth node.
  canonicalOrderMap[getIV(3,4,5)] = CanonicalOrder(getIV(1,2,0,3),getIV(4,5,3));
  canonicalOrderMap[getIV(0,1,4)] = CanonicalOrder(getIV(3,0,2,1),getIV(4,0,1));
  canonicalOrderMap[getIV(0,2,3)] = CanonicalOrder(getIV(3,2,1,0),getIV(3,2,0));
  canonicalOrderMap[getIV(1,2,5)] = CanonicalOrder(getIV(3,1,0,2),getIV(5,1,2));

  // Tet4Edges1: Three segments on a face, plus one more.  The segment
  // that's not on the face with the other three must be first and the
  // three that form a face must in an order such that they define a
  // normal that points in the direction of the fourth point.
  canonicalOrderMap[getIV(0,1,3,4)] = CanonicalOrder(getIV(2,1,0,3),
						     getIV(1,0,3,4));
  canonicalOrderMap[getIV(0,2,3,4)] = CanonicalOrder(getIV(2,0,3,1),
						     getIV(2,3,4,0));
  canonicalOrderMap[getIV(0,3,4,5)] = CanonicalOrder(getIV(2,3,1,0),
						     getIV(5,4,0,3));
  canonicalOrderMap[getIV(1,2,4,5)] = CanonicalOrder(getIV(0,2,1,3),
						     getIV(2,1,4,5));
  canonicalOrderMap[getIV(1,3,4,5)] = CanonicalOrder(getIV(0,3,2,1),
						     getIV(3,5,1,4));
  canonicalOrderMap[getIV(0,2,3,5)] = CanonicalOrder(getIV(1,0,2,3),
						     getIV(0,2,5,3));
  canonicalOrderMap[getIV(1,2,3,5)] = CanonicalOrder(getIV(1,2,3,0),
						     getIV(1,5,3,2));
  canonicalOrderMap[getIV(2,3,4,5)] = CanonicalOrder(getIV(1,3,0,2),
						     getIV(4,3,2,5));
  canonicalOrderMap[getIV(0,1,2,3)] = CanonicalOrder(getIV(3,0,1,2),
						     getIV(3,0,1,2));
  canonicalOrderMap[getIV(0,1,2,4)] = CanonicalOrder(getIV(3,1,2,0),
						     getIV(4,1,2,0));
  canonicalOrderMap[getIV(0,1,4,5)] = CanonicalOrder(getIV(0,1,3,2),
						     getIV(0,4,5,1));
  canonicalOrderMap[getIV(0,1,2,5)] = CanonicalOrder(getIV(3,2,0,1),
						     getIV(5,2,0,1));

  // Tet4Edges2: The four edges are connected in a ring.
  canonicalOrderMap[getIV(0,2,4,5)] = CanonicalOrder(getIV(1,2,3,0),
						     getIV(0,4,5,2));
  canonicalOrderMap[getIV(0,1,3,5)] = CanonicalOrder(getIV(1,3,0,2),
						     getIV(1,0,3,5));
  canonicalOrderMap[getIV(1,2,3,4)] = CanonicalOrder(getIV(0,1,3,2),
						     getIV(2,3,4,1));

  // Tet5Edges: The five edge markings can be thought of as the
  // fourEdges2 case plus one edge.  We put the edges which form the
  // fourEdges2 formation first, in an order such that the form a
  // clockwise loop as viewed from the unmarked edge.
  canonicalOrderMap[getIV(1,2,3,4,5)] = CanonicalOrder(getIV(0,1,3,2),
						       getIV(2,3,4,1,5));
  canonicalOrderMap[getIV(0,2,3,4,5)] = CanonicalOrder(getIV(1,2,3,0),
						       getIV(0,4,5,2,3));
  canonicalOrderMap[getIV(0,1,3,4,5)] = CanonicalOrder(getIV(0,2,1,3),
						       getIV(3,0,1,5,4));
  canonicalOrderMap[getIV(0,1,2,4,5)] = CanonicalOrder(getIV(3,0,1,2),
						       getIV(5,4,0,2,1));
  canonicalOrderMap[getIV(0,1,2,3,5)] = CanonicalOrder(getIV(1,3,0,2),
						       getIV(1,0,3,5,2));
  canonicalOrderMap[getIV(0,1,2,3,4)] = CanonicalOrder(getIV(3,2,0,1),
						       getIV(4,3,2,1,0));

  canonicalOrderMapCreated = true;
}
