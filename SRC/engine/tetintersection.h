// -*- C++ -*-
// $RCSfile: tetintersection.h,v $
// $Revision: 1.1.2.1.2.24 $
// $Author: langer $
// $Date: 2015/12/04 19:06:34 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

OBSOLETE

#ifndef TETINTERSECTION_H
#define TETINTERSECTION_H

#include <oofconfig.h>

class FacetCorner;

#include "common/coord.h"
#include "common/pixelsetboundary.h"
#include "engine/barycentric.h"

class CMicrostructure;

#include <vector>
#include <set>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FacePlane: public virtual Plane {
protected:
  const unsigned int face;
public:
  FacePlane(unsigned int face, const std::vector<Coord3D> &epts);
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Class for the intersection points where a voxel set boundary
// segment in a pixel plane crosses the polygon formed by the
// intersection of a tet with the pixel plane.  The intersection is
// stored in different coordinate systems to reduce round off errors
// (a point exactly on a tet face will have one barycentric coord
// equal to zero, or a point lying on a pixel boundary will have an
// integer 3D coord, for example).  The class also keeps track of
// whether or not the voxel set boundary is entering or exiting the
// polygon.

class PixelBdyIntersection {
public:
  TriplePlaneIntersection *planes;
  
  Coord2D location2D;
  Coord3D location3D;
  BarycentricCoord baryCoord;
  const unsigned int segment;
  const unsigned int face;
  const double fraction;
  const bool entry;
  // TODO: Store a PixelBdyLoopSegment instead of separate loop & loopseg.
  const PixelBdyLoop *loop;
  const unsigned int loopseg;
  const double loopfrac;

  PixelBdyIntersection(const PixelPlane &pixplane,
		       unsigned int face,
		       unsigned int segment,
		       double frac,
		       bool entry,
		       const PixelBdyLoop *loop,
		       unsigned int loopseg,
		       double loopfrac,
		       const std::vector<Coord3D> &epts,
		       const std::vector<const PixelPlane*> &facePlanes,
		       BaryCoordCache &baryCache);

  // PixelBdyIntersection(const Coord2D &loc2D, const Coord3D &loc3D,
  // 		       const BarycentricCoord &bary,
  // 		       unsigned int seg, unsigned int face,
  // 		       double frac, bool entry,
  // 		       const PixelBdyLoop *loop,
  // 		       unsigned int loopseg,  double loopfrac)
  //   : location2D(loc2D),	// 2D coord of intersection point in pixel plane
  //     location3D(loc3D),	// 3D coord of intersection point
  //     baryCoord(bary),		// barycentric coord relative to the tet
  //     segment(seg),		// polygon segment index
  //     face(face),		// tet face index corresponding to polygon seg
  //     fraction(frac),		// fractional distance along polygon segment
  //     entry(entry), 		// true if voxel set bdy enters the polygon
  //     loop(loop),
  //     loopseg(loopseg),
  //     loopfrac(loopfrac)
  // {}
  ~PixelBdyIntersection();
  PixelBdyLoopSegment getLoopSeg() const {
    return PixelBdyLoopSegment(loop, loopseg);
  }
  bool sameLoopSegment(const PixelBdyIntersection *other) const {
    return loop == other->loop && loopseg == other->loopseg;
  }
  bool sameLoopSegment(const PixelBdyLoopSegment *other) const {
    return loop == other->loop() && loopseg == other->loopseg();
  }
};

std::ostream &operator<<(std::ostream&, const PixelBdyIntersection&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TetPlaneIntersectionPoint stores the 2D intersection point of a tet
// edge and a plane, and the 3D coords of the endpoints of the edge,
// and the indices (in the local tetrahedron's list of nodes) of the
// nodes at the endpoints of the edge.

// TetPlaneIntersectionPoints are computed (by
// findTetPlaneIntersectionPoints) on a given PixelPlane with
// normal==1, and it is illegal to use them on a different plane
// except for the one with the opposite normal. 

class TetPlaneIntersectionPoint {
private:
  Coord2D location;	    // computed on a PixelPlane with normal==1
  BarycentricCoord bcoord_;
  double t_;		    // intersection = (1-t)*node0 + t*node1
  unsigned int edge_;	    // tet edge number, in vtk ordering scheme
public:
  TetPlaneIntersectionPoint(const Coord2D &pt, const BarycentricCoord &b,
			    double t, unsigned int edge)
    : location(pt),
      bcoord_(b),
      t_(t),
      edge_(edge)
  {}
  TetPlaneIntersectionPoint(const TetPlaneIntersectionPoint &tp)
    : location(tp.location),
      bcoord_(tp.bcoord_),
      t_(tp.t_),
      edge_(tp.edge_)
  {}
  TetPlaneIntersectionPoint &operator=(const TetPlaneIntersectionPoint &tp) {
    location = tp.location;
    bcoord_ = tp.bcoord_;
    t_ = tp.t_;
    edge_ = tp.edge_;
    return *this;
  }
  double t() const { return t_; }
  unsigned int edge() const { return edge_; }
  int node0() const;
  int node1() const;
  const BarycentricCoord &bcoord() const { return bcoord_; }
  bool operator<(const TetPlaneIntersectionPoint&) const;
  Coord2D location2D(const PixelPlane&) const;
  Coord3D location3D(const PixelPlane&) const;
  friend std::ostream &operator<<(std::ostream&,
				  const TetPlaneIntersectionPoint&);
};

std::ostream &operator<<(std::ostream&, const TetPlaneIntersectionPoint&);

class TetPlaneIntData {
public:
  std::vector<TetPlaneIntersectionPoint> tetPts;
  std::vector<Coord2D> tetCoords;
  unsigned int excludeFace;
  TetPlaneIntData() { tetPts.clear(); tetCoords.clear(); }
};

typedef std::map<PixelPlane, TetPlaneIntData> TetPlaneIntersectionCache;

void findTetPlaneIntersectionPoints(const std::vector<Coord3D>&,
				    const PixelPlane&,
#ifdef DEBUG
				    bool verbose,
#endif // DEBUG
				    std::vector<TetPlaneIntersectionPoint>&,
				    unsigned int&);

unsigned int faceIndex(const TetPlaneIntersectionPoint&,
		       const TetPlaneIntersectionPoint&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// polygonize reorders the given vector of Coord2Ds so that the points
// form a counterclockwise convex polygon.  The length of the vector
// must be 3 or 4.  The second argument is filled with a set of ints
// that can be passed to reorderVector to perform the same reordering
// on a different vector. 

void polygonize(std::vector<Coord2D>&, std::vector<unsigned int>&);

template <class TYPE, class IPTR>
void reorderVector(std::vector<TYPE> &vec, const IPTR &ordering) {
  std::vector<TYPE> old(vec);
  for(unsigned int i=0; i<vec.size(); i++)
    vec[i] = old[ordering[i]];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A Facet is a side of the volume formed by the intersection of a
// group of voxels and a tetrahedral element.  The voxel region is
// represented by a set of planar PixelBdyLoops.  Facets are
// constructed from the intersection of the loops with the cross
// section of the tetrahedron in the plane of the loop.

// The PixelBdyLoop is a completely 2D object.  After it's been
// interesected by a tet, it's a sort of hybrid.  Some of its corners
// are exactly at the corners of the PixelBdyLoop and can be
// represented by Coord2Ds. Others are at the intersections of the
// loop with the tet faces, and their 3D positions (robustly computed
// by segmentFaceIntersection) need to be retained so that they'll
// match corners on other facets.  Different kinds of corners are
// represented by different subclasses of FacetCorner (defined in
// engine/tetintersection.h).

typedef std::vector<FacetCorner*> FacetCornerList;

class FacetCorner {
protected:
  // TODO: Storing the BarycentricCoord here is silly since
  // FaceFacetCorner stores it in its PixelBdyIntersection.
  BarycentricCoord bcoord_;
public:
  FacetCorner(const BarycentricCoord &b, FacetCornerList &fcl);
  virtual ~FacetCorner();
  virtual Coord3D position3D() const = 0;
  virtual const BarycentricCoord &bcoord() const { return bcoord_; }
  virtual void print(std::ostream&) const = 0; // for debugging
  // virtual FacetCorner *clone(const Coord3D&, FacetCornerList&) const = 0;
};

std::ostream &operator<<(std::ostream&, const FacetCorner&);

// Base class for facet corners that lie on a plane of voxels

class PixelPlaneFacetCorner : public FacetCorner {
protected:
  const PixelPlane pixelplane;
public:
  PixelPlaneFacetCorner(const BarycentricCoord &b, const PixelPlane &pp,
			FacetCornerList &fcl)
    : FacetCorner(b, fcl),
      pixelplane(pp)
  {}
  virtual Coord2D position2D() const = 0;
};

// Facet corner formed by voxels alone.

class PixelFacetCorner : public PixelPlaneFacetCorner {
private:
  const ICoord2D location;
public:
  PixelFacetCorner(const ICoord2D &loc,
		   const BarycentricCoord &b,
		   const PixelPlane &pp,
		   FacetCornerList &fcl)
    : PixelPlaneFacetCorner(b, pp, fcl),
      location(loc)
  {}
  virtual Coord2D position2D() const { return location.coord(); }
  virtual Coord3D position3D() const;
  // virtual FacetCorner *clone(const Coord3D&, FacetCornerList&) const {
  //   return NULL;
  // }
  virtual void print(std::ostream&) const;
};

class SimpleFacetCorner : public FacetCorner {
private:
  const Coord3D location;
public:
  SimpleFacetCorner(const Coord3D &loc, const BarycentricCoord &b,
		    FacetCornerList &fcl)
    : FacetCorner(b, fcl),
      location(loc)
  {}
  virtual Coord3D position3D() const { return location; }
  // virtual FacetCorner *clone(const Coord3D &loc, FacetCornerList &fcl) const {
  //   return new SimpleFacetCorner(loc, bcoord(), fcl);
  // }
  virtual void print(std::ostream&) const;
};

// Facet corner where a face of the tetrahedron intersects a plane of
// voxels.

class FaceFacetCorner : public PixelPlaneFacetCorner {
protected:
  const PixelBdyIntersection *pbi;
public:
  // FaceFacetCorner(const Coord3D &loc, const BarycentricCoord &b,
  // 		  const PixelPlane &pp,
  // 		  FacetCornerList &fcl)
  //   : PixelPlaneFacetCorner(b, pp, fcl),
  //     location(loc)
  // {}
  // const Coord3D location;

  FaceFacetCorner(const PixelBdyIntersection *pbi,
		  const PixelPlane &pp, FacetCornerList &fcl)
    : PixelPlaneFacetCorner(pbi->baryCoord, pp, fcl),
      pbi(pbi)
  {}
  
  virtual const BarycentricCoord &bcoord() const { return pbi->baryCoord; }
  virtual Coord2D position2D() const { return pbi->location2D; }
  virtual Coord3D position3D() const { return pbi->location3D; }
  // virtual FacetCorner *clone(const Coord3D &pos, FacetCornerList&) const;
  virtual void print(std::ostream&) const;
};

// Facet corner where an edge of the tetrahedron intersects a plane of
// voxels.  It also stores a copy of the TetPlaneIntersectionPoint
// that gave rise to the corner.

class EdgeFacetCorner : public PixelPlaneFacetCorner {
private:
  const TetPlaneIntersectionPoint tpip;
public:
  // TODO: Since loc can be computed from tpip and pp, it doesn't need
  // to be an explicit argument to the constructor.
  // TODO: Is tpip used outside of the print method?  We may not need
  // to store it.
  EdgeFacetCorner(const TetPlaneIntersectionPoint &tpip,
		  const PixelPlane &pp,
		  FacetCornerList &fcl)
    : PixelPlaneFacetCorner(tpip.bcoord(), pp, fcl),
      tpip(tpip)
  {}
  virtual const BarycentricCoord &bcoord() const { return tpip.bcoord(); }
  virtual Coord2D position2D() const { return tpip.location2D(pixelplane); }
  virtual Coord3D position3D() const {
    return pixelplane.convert2Coord3D(position2D());
  }
  // unsigned int edge() const { return tpip.edge(); }
  // double edgePosition() const { return tpip.t(); } // only used in debugging
  // FacetCorner *clone(const Coord3D &pos, FacetCornerList&) const;
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FacetEdge {
public:
  const FacetCorner *start;
  const FacetCorner *end;
#ifdef DEBUG
  std::string note;   // Can't be const for copy ctor
#endif // DEBUG
  FacetEdge(const FacetCorner *s, const FacetCorner *e
#ifdef DEBUG
	    , const std::string &note
#endif // DEBUG
	    )
    : start(s), end(e)
#ifdef DEBUG
    , note(note)
#endif // DEBUG
  {}
  FacetEdge reversed() const {
    return FacetEdge(end, start
#ifdef DEBUG
		     , "reversed: "+note
#endif // DEBUG
		     );
  }
  bool operator<(const FacetEdge&) const;
  bool nearlyEqual(const FacetEdge&) const;
  double length2() const;	// length squared
};

std::ostream &operator<<(std::ostream&, const FacetEdge&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

typedef std::map<BarycentricCoord, BarycentricCoord> BaryCoordMap;

typedef std::multimap<double, PixelBdyIntersection*> ElEdgeMap;

typedef std::multimap<Coord2D, PixelBdyIntersection*> CoordIsec;


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PixelPlaneFacet {
private:
  std::set<FacetEdge> edges;
  mutable double area_;
  mutable bool areaComputed_;
  double getArea(bool) const;
public:
  PixelPlaneFacet() : areaComputed_(false) {}
  double area(bool) const;
  Coord3D center() const;
  Coord3D areaVector() const;
  void addEdge(const FacetCorner*, const FacetCorner*
#ifdef DEBUG
	       , const std::string&, bool
#endif // DEBUG
	       );
  void removeEdgesAtPoint(const ICoord3D&, const Coord3D&, const Coord3D&
#ifdef DEBUG
			  , bool
#endif // DEBUG
			  );
  void removeEdge(const Coord3D&, const Coord3D&);
#ifdef CLEANUP
  void cleanUp(const PixelPlane&, FacetCornerList&,
	       const std::vector<Coord3D>&, BaryCoordCache&
#ifdef DEBUG
	       , bool
#endif // DEBUG
	       );
#endif // CLEANUP
  
  std::set<FacetEdge>::const_iterator begin() const {return edges.begin();}
  std::set<FacetEdge>::const_iterator end() const { return edges.end(); }
  bool empty() const { return edges.empty(); }
};

std::ostream &operator<<(std::ostream&, const PixelPlaneFacet&);
  
typedef std::map<PixelPlane, PixelPlaneFacet*> FacetMap2D;


void cleanUpFacetMaps(std::vector<FacetMap2D>&, FacetCornerList&);
void cleanUpFacetMap(FacetMap2D&, FacetCornerList&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void findPixelPlaneFacets(const CMicrostructure*,
			  const VoxelSetBoundary&,
			  const std::vector<Coord3D>&,
			  const ICRectangularPrism&,
			  unsigned int,
#ifdef DEBUG
			  bool,	// verbose, for debugging
#endif // DEBUG
			  FacetMap2D&,
			  BaryCoordMap&,
			  FacetCornerList&,
			  std::vector<bool>&,
			  TetPlaneIntersectionCache&,
			  BaryCoordCache&);

double tetIntersectionVolume(const VoxelSetBoundary&,
			     const std::vector<Coord3D>&,
			     const ICRectangularPrism&,
			     const FacetMap2D&,
			     const BaryCoordMap&,
			     FacetCornerList&,
			     BaryCoordCache&,
			     const std::vector<bool>&,
			     unsigned int category
#ifdef DEBUG
			     , bool /* verbose */
#endif // DEBUG
			     );

void tetIntersectionFaceFacets(const VoxelSetBoundary&,
			       const std::vector<Coord3D>&,
			       const ICRectangularPrism&,
			       const FacetMap2D&,
			       const BaryCoordMap&,
			       FacetCornerList&,
			       BaryCoordCache&,
			       const std::vector<bool>&,
			       unsigned int,
#ifdef DEBUG
			       bool, // verbose, for debugging
#endif // DEBUG			       
			       std::vector< std::set<FacetEdge> >&);

#endif // TETINTERSECTION_H
