// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

OBSOLETE

#ifndef FACEFACET_H
#define FACEFACET_H

#include <oofconfig.h>

#include "common/coord.h"
#include "engine/facefacet_i.h"
#include "engine/homogeneitytet_i.h"
#include "engine/planeintersection_i.h"

// EdgePosition is the relative position of a point along a directed
// edge.  "reversed" is true if the position was calculated for an
// edge with the opposite orientation.  "position" is a number between
// 0 and 1 inclusive.

// To guarantee consistency when the relative position of a point on
// an edge is computed both for the edge and its mirror image, the
// position is always calculated for some canonical orientation of the
// edge (for example, if the edge is a tet edge, the canonical
// orientation is the one that goes from the lower node number to the
// higher number).  The intention is to guarantee that the computed
// order of two points on a edge is the reverse of their computed
// order on the reversed edge, even if the points differ only by round
// off error.  It's not possible to compute the position on the
// reversed edge by subracting from 1, since this can lose precision.

class EdgePosition {
private:
  double position;
  bool reversed;
  bool unset_;
public:
  EdgePosition(double t, bool rev)
    : position(t), reversed(rev), unset_(false)
  {}
  EdgePosition()
    : position(-12345), reversed(false), unset_(true)
  {}
  bool operator<(const EdgePosition&) const;
  bool operator>(const EdgePosition&) const;
  bool operator<=(const EdgePosition&) const;
  bool operator>=(const EdgePosition&) const;
  bool operator==(const EdgePosition&) const;
  double operator-(const EdgePosition&) const;
  bool atStart() const;
  bool atEnd() const;
  void normalize();
  void forceToEnd();
  bool unset() const { return unset_; }
  friend std::ostream &operator<<(std::ostream&, const EdgePosition&);
};

std::ostream &operator<<(std::ostream&, const EdgePosition&);

class FaceEdgeIntersection {
private:
  PlaneIntersection *crnr;   // This object does not own this pointer.
  FaceFacetEdge *edge_;	     // The edge that ends at crnr.
  EdgePosition t;	// Parametric position of crnr along tet edge.
  unsigned int fEdge;	// Index on tet face of intersected tet edge.
  bool segstart;	// Is this the start of a segment?
public:
  FaceEdgeIntersection(PlaneIntersection*, FaceFacetEdge*, bool);
  FaceFacetEdge *edge() const { return edge_; }
  unsigned int faceEdge() const { return fEdge; }
  bool start() const { return segstart; }
  EdgePosition edgePosition() const { return t; }
  PlaneIntersection *corner() const { return crnr; }
  PlaneIntersection *remoteCorner() const;

  // findFaceEdge sets fEdge and t.  It uses topology to find fEdge.
  void findFaceEdge(unsigned int face, HomogeneityTet*);

  // Sometimes we know fEdge and t already and don't have to compute it.
  void setFaceEdge(unsigned int fe, EdgePosition pos) { fEdge = fe; t = pos; }
  // forceOntoEdge also sets fEdge and t.  It uses arithmetic to find fEdge.
  void forceOntoEdge(unsigned int face, HomogeneityTet*);
  bool crossesSameEdge(const FaceEdgeIntersection*, unsigned int,
		       const FacePlane*, HomogeneityTet*
#ifdef DEBUG
	       , bool
#endif // DEBUG
	       ) const;
  bool crossesDiffEdge(const FaceEdgeIntersection*
#ifdef DEBUG
	       , bool
#endif // DEBUG
	       ) const;

  // Are two points on the same edge and same edge coordinate?
  bool samePosition(const FaceEdgeIntersection*) const;
  // declination is the cosine of the angle between the edge on the
  // face and the edge of the face.
  double declination(unsigned int f, unsigned int e, HomogeneityTet*) const;

  bool operator<(const FaceEdgeIntersection &) const;
};				// end class FaceEdgeIntersection

struct FaceEdgeIntersectionLT {
public:
  bool operator()(const FaceEdgeIntersection*, const FaceEdgeIntersection*)
    const;
};

struct FaceEdgeIntersectionLTwrap {
public:
  bool operator()(const FaceEdgeIntersection*, const FaceEdgeIntersection*)
    const;
};

std::ostream &operator<<(std::ostream&, const FaceEdgeIntersection&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A FaceFacetEdge is an edge added to a facet on a tet face.  It's
// like FacetEdge, except that the endpoints of the edge are general
// PlaneIntersections, not PixelPlaneIntersections.

class FaceFacetEdge {
private:
  // The FaceFacetEdge object owns the PlaneIntersections pointed to
  // here.
  PlaneIntersection *start_;
  PlaneIntersection *stop_;
  const HPixelPlane *pixplane_;	// The PixelPlane that this edge came
				// from, if any.
  unsigned int id;
public:
  FaceFacetEdge(HomogeneityTet*,
		const PlaneIntersection*, const PlaneIntersection*,
		const HPixelPlane*);
  FaceFacetEdge(HomogeneityTet*,
		const PlaneIntersection*, const PlaneIntersection*);
  ~FaceFacetEdge();
  FaceFacetEdge(const FaceFacetEdge&) = delete; // do we need this?
  FaceFacetEdge(FaceFacetEdge&&);
  PlaneIntersection *startPt() const { return start_; }
  PlaneIntersection *endPt() const { return stop_; }
  PlaneIntersection *point(bool start) const {
    return start ? start_ : stop_;
  }
  Coord3D startPos3D() const;
  Coord3D endPos3D() const;
  const HPixelPlane *pixelPlane() const { return pixplane_; }
  PlaneIntersection *replacePoint(PlaneIntersection *pt, HomogeneityTet*, bool);
  bool isNull() const;
  // Does this edge lie along an edge of the given tet face?  Returns
  // the edge number or NONE.
  unsigned int findFaceEdge(unsigned int, HomogeneityTet*) const;
  bool operator<(const FaceFacetEdge&) const; // object identity, not value
}; // end class FaceFacetEdge

std::ostream &operator<<(std::ostream&, const FaceFacetEdge&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A StrandedPoint is an unpaired end in a set of segments on a tet
// face.

class StrandedPoint {
public:
  FaceEdgeIntersection *feInt;
  unsigned int face;
  StrandedPoint(FaceEdgeIntersection *fei, unsigned int f)
    : feInt(fei), face(f)
  {}
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FaceFacet {
public:
  const unsigned int face;
private:
  FaceFacetEdgeSet edges_;
  HomogeneityTet *htet;
  mutable Coord3D areaVec_;
  mutable bool areaComputed;
  bool closedOnPerimeter;
  Coord3D getArea(HomogeneityTet*) const;
  Coord3D getAreaCarefully(HomogeneityTet*) const;
public:
  FaceFacet(unsigned int f, HomogeneityTet *h)
    : face(f), htet(h), areaComputed(false), closedOnPerimeter(false)
  {}
  // Don't allow FaceFacets to be copied. The FaceFacet owns the
  // FaceFacetEdges that it points to.  A correct copy constructor
  // would have to clone the FaceFacetEdges.
  FaceFacet(const FaceFacet&) = delete;
  // Deleting the copy constructor and not providing the move
  // constructor is an error.
  FaceFacet(FaceFacet&&) = default;
  ~FaceFacet();

  Coord3D area(HomogeneityTet*) const;
  unsigned int size() const { return edges_.size(); }
  bool empty() const { return edges_.empty(); }

  void clear();

  void addEdge(FaceFacetEdge*); // takes ownership of argument
  void addFaceEdges(const FaceEdgeIntersection*, const FaceEdgeIntersection*,
		    HomogeneityTet*);

  void findLooseEnds(LooseEndSet&, std::vector<StrandedPoint>&) const;
  void removePerimeterEdges(LooseEndSet&);

  const std::set<FaceFacetEdge*, DerefCompare<FaceFacetEdge>> &edges() const {
    return edges_;
  }

  void removeOpposingEdges();
  void fixNonPositiveArea(HomogeneityTet*, unsigned int cat);
#ifdef DEBUG
  void dump(std::string, unsigned int, unsigned int=NONE) const;
  std::string shortDescription() const;
  friend class CSkeletonElement;
#endif // DEBUG
  friend std::ostream &operator<<(std::ostream&, const FaceFacet&);
};				// end class FaceFacet

std::ostream &operator<<(std::ostream&, const FaceFacet&);



#endif // FACEFACET_H
