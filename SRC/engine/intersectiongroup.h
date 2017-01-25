// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef INTERSECTIONGROUP_H
#define INTERSECTIONGROUP_H

#include <oofconfig.h>
#include "engine/homogeneitytet_i.h"

// IntersectionGroup is a group of FaceEdgeIntersections that are
// close to one another on the edges of a tet face.  The group may
// include intersections that are supposed to coincide exactly, but
// don't due to round off error.

class IntersectionGroup {
private:
  Coord3D location;
  std::vector<FaceEdgeIntersection*> isecs;
  unsigned int face;
  bool tentCheck(HomogeneityTet*, unsigned int, PlaneIntersection*,
		 FaceEdgeIntersection*, FaceEdgeIntersection*) const;
  void eraseMatched(const std::vector<bool>&, LooseEndSet&);
public:
  IntersectionGroup(const Coord3D loc, FaceEdgeIntersection *fei,
		    unsigned int f)
    : location(loc),
      // isectype(CORRECT),
      face(f)
  {
    isecs.push_back(fei);
  }
  void addIntersection(FaceEdgeIntersection *fei) {
    isecs.push_back(fei);
    // isectype = UNKNOWN;
  }
  bool nearby(const Coord3D &where) const {
    return (norm2(where-location) < CLOSEBY2);
  }

  void sortByPositionAndEdge();

  // These four methods are the operations that detect and fix
  // topologically impossible configurations.  They return true if
  // they're successful.
  bool removeEquivPts(HomogeneityTet*, unsigned int, LooseEndSet&);
  bool fixCrossings(HomogeneityTet*, unsigned int, LooseEndSet&);
  bool fixOccupiedEdges(HomogeneityTet*, unsigned int, LooseEndSet&,
			const std::vector<FaceFacetEdgeSet>&);
  bool fixTents(HomogeneityTet*, unsigned int, LooseEndSet&);
  
  void checkOrdering(HomogeneityTet*, unsigned int, std::vector<LooseEndMap>&);
  bool empty() const { return isecs.empty(); }
  unsigned int size() const { return isecs.size(); }
  friend class HomogeneityTet;
  friend std::ostream &operator<<(std::ostream&, const IntersectionGroup&);
};

#endif // INTERSECTIONGROUP_H
