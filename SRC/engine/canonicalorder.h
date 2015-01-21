// -*- C++ -*-
// $RCSfile: canonicalorder.h,v $
// $Revision: 1.1.4.4 $
// $Author: fyc $
// $Date: 2014/07/22 21:07:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


#include <oofconfig.h>

#ifndef CANONICALORDER_H
#define CANONICALORDER_H

#include <vector>
#include <utility>
#include <map>

// For tetrahedra, the signatures that give edges marked for
// refinement or snapping are found in numerical order.  But our
// routines need them in a topologically consistent order.  In 3D,
// there is no simple way of rotating the list of edges.  We can find
// the canonical orders with code, but that gets very messy for
// signatures with 4 or 5 edges marked.  It's faster and easier to
// just hard code all of the canonical orderings of segments and nodes
// for each of the signatures that need it.  This class provides
// static methods for retrieving those orderings.

typedef std::vector<short> IndexVec;
typedef std::vector< std::pair<short,short> > IndexPairVec;
// TODO MER: IndexPairVec is the same as RefinementSignature. Why have both?

struct CanonicalOrder {
  IndexVec nodes;
  IndexVec segs;
  CanonicalOrder() {}
  CanonicalOrder(IndexVec n, IndexVec s) {
    nodes = n;
    segs = s;
  }
};

//typedef std::pair<IndexVec, CanonicalOrder> COPair;
typedef std::map<IndexVec, CanonicalOrder> CanonicalOrderMap;

class CanonicalOrderMapper {

private:
  static CanonicalOrderMap canonicalOrderMap;
  static bool canonicalOrderMapCreated;

public:
  static void createCanonicalOrderMap();
  static const IndexVec& getNodes(const IndexVec&);
  static const IndexVec& getSegs(const IndexVec&);
  // The IndexPairVec forms of these methods are called by the
  // refinement rules in crefine.C.
  static const IndexVec& getNodes(const IndexPairVec&);
  static const IndexVec& getSegs(const IndexPairVec&);
};


#endif
