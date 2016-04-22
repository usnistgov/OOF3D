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

#ifndef HOMOGENEITYTET_H
#define HOMOGENEITYTET_H

#include "engine/homogeneitytet_i.h"

#include "common/coord.h"
#include "common/geometry.h"
#include "engine/barycentric.h"
#include "engine/pixelplanefacet_i.h"
#include "engine/planeintersection_i.h"

#include <vector>

// TODO: There are too many mutable data members here.  Maybe there
// are too many const methods.

class CMicrostructure;
class CSkeletonElement;
class VoxelSetBoundary;
class PixelBdyLoop;
class PixelBdyLoopSegment;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FaceEdgeIntersection {
private:
  const PlaneIntersection *crnr; // this object does not own this pointer
  // fEdge and t are set when findFaceEdge() is called.
  double t;			// parametric position along tet edge
  unsigned int fEdge;		// index on tet face of intersected tet edge
  bool segstart;		// is this the start of a segment?
  FaceFacetEdge *edge_;
public:

  FaceEdgeIntersection(const PlaneIntersection*,
		       FaceFacetEdge*,
		       // const std::set<FaceFacetEdge*>::const_iterator&,
		       bool);

  FaceFacetEdge *edge() const { return edge_; }
  unsigned int faceEdge() const { return fEdge; }
  bool start() const { return segstart; }
  double edgePosition() const { return t; }
  const PlaneIntersection *corner() const { return crnr; }

  // findFaceEdge sets fEdge and t.
  void findFaceEdge(unsigned int face, const HomogeneityTet *htet);
};

std::ostream &operator<<(std::ostream&, const FaceEdgeIntersection&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A FaceFacetEdge is an edge added to a facet on a tet face.  It's
// just like FacetEdge, except that the endpoints of the edge are
// general PlaneIntersections, not PixelPlaneIntersections.

class FaceFacetEdge {
private:
  // The FaceFacetEdge object owns the PlaneIntersections pointed to
  // here.
  const PlaneIntersection *start_;
  const PlaneIntersection *stop_;
  const HPixelPlane *pixplane_;	// The PixelPlane that this edge came
				// from, if any.
  unsigned int id;
public:
  FaceFacetEdge(const HomogeneityTet*,
		const PlaneIntersection*, const PlaneIntersection*,
		const HPixelPlane*);
  FaceFacetEdge(const HomogeneityTet*,
		const PlaneIntersection*, const PlaneIntersection*);
  ~FaceFacetEdge();
  FaceFacetEdge(const FaceFacetEdge&);
  FaceFacetEdge(FaceFacetEdge&&);
  const PlaneIntersection *startPt() const { return start_; }
  const PlaneIntersection *endPt() const { return stop_; }
  const PlaneIntersection *point(bool start) const {
    return start ? start_ : stop_;
  }
  Coord3D startPos3D() const;
  Coord3D endPos3D() const;
  const HPixelPlane *pixelPlane() const { return pixplane_; }
  const PlaneIntersection *replacePoint(const PlaneIntersection *pt, bool);
  bool isNull() const;
  bool operator<(const FaceFacetEdge&) const; // object identity, not value
};

std::ostream &operator<<(std::ostream&, const FaceFacetEdge&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FaceFacet {
private:
  const unsigned int face;
  std::set<FaceFacetEdge*, DerefCompare<FaceFacetEdge>> edges;
  const HomogeneityTet *htet;
  mutable Coord3D areaVec_;
  // mutable Coord3D center_;
  mutable bool areaComputed;
  Coord3D getArea(const HomogeneityTet*) const;
public:
  FaceFacet(unsigned int f, const HomogeneityTet *h)
    : face(f), htet(h), areaComputed(false)
  {}
  // Don't allow FaceFacets to be copied. The FaceFacet owns the
  // FaceFacetEdges that it points to.  A correct copy constructor
  // would have to clone the FaceFacetEdges.
  FaceFacet(const FaceFacet&) = delete;
  // Deleting the copy constructor and not providing the move
  // constructor is an error.
  FaceFacet(FaceFacet&&) = default;
  ~FaceFacet();
  Coord3D area(const HomogeneityTet*) const;
  // Coord3D center(const HomogeneityTet*) const;
  unsigned int size() const { return edges.size(); }
  bool empty() const { return edges.empty(); }

  void addEdge(FaceFacetEdge*); // takes ownership of argument
  void addFaceEdges(const FaceEdgeIntersection*, const FaceEdgeIntersection*,
		    const HomogeneityTet*);
  std::set<FaceFacetEdge*>::const_iterator begin() const {
    return edges.begin();
  }
  std::set<FaceFacetEdge*>::const_iterator end() const {
    return edges.end();
  }

  void removeNullEdges();
  void fixNonPositiveArea(const HomogeneityTet*, unsigned int cat);
  void dump() const;
  friend std::ostream &operator<<(std::ostream&, const FaceFacet&);
};

std::ostream &operator<<(std::ostream&, const FaceFacet&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class HomogeneityTet {
private:
  // epts contains the positions of tet corners in voxel coords,
  // indexed by node number
  std::vector<Coord3D> epts;
  std::vector<double> edgeLengths;
  std::vector<FacePlane*> faces;
  std::vector<Coord3D> faceCenters;
  std::vector<Coord3D> faceAreaVectors; // not unit normals!
  mutable std::vector<ICoord3D> testVoxels;
  mutable std::vector<bool> testVoxelsFound;
  Coord3D tetCenter;
  mutable unsigned int faceFacetEdgeCount;

  // Pixel plane intersection points generated by findFaceFacets
  // aren't part of FacetEdges and will need to be deleted explicitly.
  mutable std::set<PixelPlaneIntersectionNR*> extraPoints;

  // If face f lies in a pixel plane, then coincidentPixelPlanes[f] is
  // that plane.  Otherwise it's a null pointer.
  std::vector<const FacePixelPlane*> coincidentPixelPlanes;
  // coincidentPixelPlanes is the inverse of coincidentFacePlanes
  std::map<const HPixelPlane*, const FacePixelPlane*, DerefCompare<HPixelPlane>>
    coincidentFacePlanes;

  CRectangularPrism *bbox_;
  mutable BaryCoordCache baryCache;

  // // pixelPlanes_ is a map used by getPixelPlane and
  // // getUnorientedPixelPlane that ensures that PixelPlanes with
  // // different addresses have different values.  The map key is a
  // // PixelPlane (compared by value) and the map value is a PixelPlane
  // // pointer that points to the one official PixelPlane that is equal
  // // to the key.
  // mutable std::map<const HPixelPlane, const HPixelPlane*> pixelPlanes_;

  // pixelPlanes_ contains pointers to the unique HPixelPlanes used by
  // the HomogeneityTet.  Since the planes are unique, pointer
  // comparison is sufficient to distinguish the planes *elsewhere*.
  // This does *not* use PixelPlaneSet, defined in
  // planeintersection_i.h, because that typedef might be redefined in
  // non-debug mode so that it doesn't use DerefCompare.
  mutable std::set<HPixelPlane*, DerefCompare<HPixelPlane>> pixelPlanes_;

  // Because pointers to some planes are in both pixelPlanes_ and
  // faces, we can't just delete all of those pointers in the
  // destructor.  So all pointers to planes are also stored in
  // allPlanes_, and those are deleted.
  mutable std::set<HPlane*> allPlanes_;

  mutable int nextEquivalenceLabel;
  mutable std::map<int, std::set<const PlaneIntersection*>> equivalentPoints;

  
  TetPlaneIsecMap tetPlaneIntersections;

  void doFindPixelPlaneFacets(unsigned int cat, const HPixelPlane*,
			      const std::vector<PixelBdyLoop*>&,
			      unsigned int face,
			      FacetMap2D&);
  PixelPlaneIntersectionNR *find_one_intersection(
				  const HPixelPlane*, const HPixelPlane*,
				  const HPixelPlane*,
				  const PixelBdyLoopSegment&,
				  unsigned int, unsigned int, bool) const;
  std::vector<PixelPlaneIntersectionNR*> find_two_intersections(
				  const HPixelPlane*, const HPixelPlane*,
				  const HPixelPlane*,
				  const PixelBdyLoopSegment&,
				  unsigned int, unsigned int) const;
public:
  HomogeneityTet(const CSkeletonElement*, const CMicrostructure*
#ifdef DEBUG
		 , bool verbose
#endif	 // DEBUG
		 );
  ~HomogeneityTet();

  const CMicrostructure * const microstructure;

  const CRectangularPrism &bounds() const { return *bbox_; }

  const HPixelPlane *getPixelPlane(unsigned int dir, int offset, int normal) const;
  const HPixelPlane *getUnorientedPixelPlane(const HPixelPlane*) const;
  const FacePlane *getFacePlane(unsigned int i) const { return faces[i]; }
  const FacePixelPlane *getCoincidentPixelPlane(const FacePlane*) const;
  const FacePixelPlane *getCoincidentPixelPlane(unsigned int) const;
  const FacePixelPlane *getCoincidentFacePlane(const HPixelPlane*) const;
  unsigned int getCoincidentFaceIndex(const HPixelPlane*) const;

  TetIntersectionPolygon &getTetPlaneIntersectionPoints(const HPixelPlane*,
							const HPixelPlane*);

  // Check if two points are equivalent, and update the equivalence
  // class data if they are.
  void checkEquiv(const PlaneIntersection*, const PlaneIntersection*) const;
  // Two points are merging form a third.  Combine the equivalence
  // classes of the first two, and add the third.
  void mergeEquiv(const PlaneIntersection*, const PlaneIntersection*,
		  const PlaneIntersection*) const;

  double edgeLength(unsigned int e) const;
  double edgeLength(unsigned int f, unsigned int e) const;

  BarycentricCoord &getBarycentricCoord(const Coord3D&) const;
  BarycentricCoord &getBarycentricCoord(const ICoord3D&) const;
  BarycentricCoord &getBarycentricCoord(const ICoord2D&, const HPixelPlane*)
  const;

  unsigned int nextFaceFacetEdgeID() const { return faceFacetEdgeCount++; }
				       
  FacetMap2D findPixelPlaneFacets(unsigned int cat,
				  const VoxelSetBoundary &vsb);

  FaceFacets findFaceFacets(unsigned int cat, const FacetMap2D&) const;
  double intersectionVolume(const FacetMap2D&, const FaceFacets&) const;

  // void setIntersectionPolyFrac(SingleFaceBase*, unsigned int,
  // 			       const PixelPlaneFacet*) const;

  // Return the fractional position of the given point given in
  // barycentric coords) along the polygon edge where the given tet
  // face intersects the given pixel plane.
  double edgeCoord(const BarycentricCoord&, const FacePlane*,
		   const PixelPlaneFacet*) const;

  Coord3D nodePosition(unsigned int n) const { return epts[n]; }
  Coord3D faceCenter(unsigned int f) const { return faceCenters[f]; }
  Coord3D faceAreaVector(unsigned int f) const { return faceAreaVectors[f]; }
  ICoord3D testVoxel(unsigned int f) const;

  void resetEquivalences();
  void removeEquivalence(PlaneIntersection*) const;
  
#ifdef DEBUG
private:
  mutable bool verbose;
  mutable bool verbosecategory;
  mutable bool verboseplane;
  mutable bool verboseface;
public:
  // Redefine these methods to change which categories and planes are verbose.
  bool verboseCategory_(bool, unsigned int) const;
  bool verbosePlane_(bool, const HPixelPlane*) const;
  bool verboseFace_(bool, unsigned int) const;

  bool verboseCategory() const { return verbosecategory; }
  bool verbosePlane() const { return verboseplane; }
  bool verboseFace() const { return verboseface; }
  void printLooseEnds(unsigned int, const LooseEndMap&) const;
#endif
};

#endif // HOMOGENEITYTET_H
