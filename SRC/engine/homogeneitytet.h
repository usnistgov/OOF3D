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
#include "engine/facefacet_i.h"

#include <vector>
#include <map>

class CMicrostructure;
class CSkeletonElement;
class VoxelSetBoundary;
class PixelBdyLoop;
class PixelBdyLoopSegment;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Intersection points within CLOSEBY of each other (measured in units
// of the voxel size) are considered to be close enough to merit
// special treatment as a group.

#define CLOSEBY 0.3
#define CLOSEBY2 (CLOSEBY*CLOSEBY)

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: Move FaceEdgeIntersection, FaceFacetEdge, and FaceFacet to a
// separate file.

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// LooseEndCatalog is a LooseEndSet for each tet face.
typedef std::vector<LooseEndSet> LooseEndCatalog;

typedef std::vector<std::vector<StrandedPoint>> StrandedPointLists;

class HomogeneityTet {
private:
  // epts contains the positions of tet corners in voxel coords,
  // indexed by node number
  std::vector<Coord3D> epts;
  std::vector<double> edgeLengths;
  std::vector<FacePlane*> faces;
  std::vector<Coord3D> faceCenters;
  std::vector<Coord3D> faceAreaVectors; // not unit normals!
  std::vector<ICoord3D> testVoxels;
  std::vector<bool> testVoxelsFound;
  Coord3D tetCenter;
  unsigned int faceFacetEdgeCount;
  std::set<FaceEdgeIntersection*> allFaceEdgeIntersections;

  // intersectionID_ gives PlaneIntersections a unique identifier
  unsigned int intersectionID_;
  // Same for IsecEquivalenceClasses
  unsigned int equivalenceID_;

  // Keep track of which planes are collinear: three or more planes
  // that intersect on a line.
  CollinearPlaneMap collinearPlanes;

  // Keep track of which PlaneIntersections are equivalent to others.
  // This is a set of pointers to IsecEquivalenceClasses instead of a
  // set of IsecEquivalenceClasses because intersections store
  // pointers to their equivalence classes.  The addresses of objects
  // in a set might change.  TODO: This was changed to a vector to
  // make the access order predictable when debugging.  Check to see
  // if there's a significant performance difference.
  std::vector<IsecEquivalenceClass*> equivalences;
  // std::set<IsecEquivalenceClass*> equivalences;

  // If face f lies in a pixel plane, then coincidentPixelPlanes[f] is
  // that plane.  Otherwise it's a null pointer.
  std::vector<const FacePixelPlane*> coincidentPixelPlanes;
  // coincidentPixelPlanes is the inverse of coincidentFacePlanes
  std::map<const HPixelPlane*, const FacePixelPlane*, DerefCompare<HPixelPlane>>
    coincidentFacePlanes;

  CRectangularPrism *bbox_;
  BaryCoordCache baryCache;

  // pixelPlanes_ contains pointers to the unique HPixelPlanes used by
  // the HomogeneityTet.  Since the planes are unique, pointer
  // comparison is sufficient to distinguish the planes *elsewhere*.
  // This does *not* use PixelPlaneSet, defined in
  // planeintersection_i.h, because that typedef might be redefined in
  // non-debug mode so that it doesn't use DerefCompare.
  // The stored planes are not const, because it makes it hard to
  // compute the unoriented plans in getPixelPlane().
  std::set<HPixelPlane*, DerefCompare<HPixelPlane>> pixelPlanes_;

  // Because pointers to some planes are in both pixelPlanes_ and
  // faces, we can't just delete all of those pointers in the
  // destructor.  So all pointers to planes are also stored in
  // allPlanes_, and those are deleted.
  std::set<HPlane*> allPlanes_;

  TetPlaneIsecMap tetPlaneIntersections;

  void doFindPixelPlaneFacets(unsigned int cat, const HPixelPlane*,
			      const std::vector<PixelBdyLoop*>&,
			      unsigned int face,
			      FacetMap2D&);
  PixelPlaneIntersectionNR *find_one_intersection(
				  unsigned int,
				  const PixelPlaneFacet*,
				  const HPixelPlane*,
				  const PixelBdyLoopSegment&,
				  unsigned int, bool);
  std::vector<PixelPlaneIntersectionNR*> find_two_intersections(
				unsigned int,
				const PixelPlaneFacet*,
				const HPixelPlane*,
				const HPixelPlane*,
				const PixelBdyLoopSegment&,
				unsigned int, unsigned int);

  const HPixelPlane *orientedOrthogonalPlane(unsigned int,
					     const HPixelPlane*,
					     const PixelBdyLoopSegment&,
					     double);
  const HPixelPlane *orientedOrthogonalPlane(unsigned int,
					     const HPixelPlane*,
					     const PixelBdyLoopSegment&,
					     bool);
  const HPixelPlane *orientedOrthogonalPlane_(unsigned int,
					      const HPixelPlane*,
					      HPixelPlane*,
					      const Coord3D&);

  StrandedPointLists matchStrandedPoints(std::vector<StrandedPoint>&,
					 LooseEndCatalog&);
  void resolveFaceFacetCoincidences(unsigned int, LooseEndSet&,
				    const std::vector<FaceFacetEdgeSet>&);
public:
  HomogeneityTet(const CSkeletonElement*, const CMicrostructure*
#ifdef DEBUG
		 , bool verbose
#endif	 // DEBUG
		 );
  ~HomogeneityTet();
  HomogeneityTet(const HomogeneityTet&) = delete;
  HomogeneityTet(HomogeneityTet&&) = delete;

  const CMicrostructure * const microstructure;

  const CRectangularPrism &bounds() const { return *bbox_; }

  HPixelPlane *getPixelPlane(unsigned int dir, int offset, int normal);
  HPixelPlane *getPixelPlane(HPixelPlane*);
  const HPixelPlane *getUnorientedPixelPlane(const HPixelPlane*);
  const FacePlane *getTetFacePlane(unsigned int i) const { return faces[i]; }
  unsigned int getTetFaceIndex(const FacePlane*) const;
  const FacePixelPlane *getCoincidentPixelPlane(const FacePlane*) const;
  const FacePixelPlane *getCoincidentPixelPlane(unsigned int) const;
  const FacePixelPlane *getCoincidentFacePlane(const HPixelPlane*) const;
  unsigned int getCoincidentFaceIndex(const HPixelPlane*) const;

  HPlaneSet getCollinearPlanes(const HPlane*, const HPlane*) const;
  FacePlaneSet getCollinearFaces(const HPlane*, const HPlane*) const;
  bool areCollinear(const HPlane*, const HPlane*, const HPlane*) const;
  bool areCollinear(const FacePlaneSet&) const;

  TetIntersectionPolygon &getTetPlaneIntersectionPoints(const HPixelPlane*);

  // Check to see if a point should be in an existing equivalence
  // class, and put it in if it's necessary.  Return the argument.
  template <class PLANEINTERSECTION>
  PLANEINTERSECTION *checkEquiv(PLANEINTERSECTION*);
  // Two points are merging to form a third.  Combine the equivalence
  // classes of the first two, and add the third.
  void mergeEquiv(PlaneIntersection*, PlaneIntersection*, PlaneIntersection*);
  void mergeEquiv(PlaneIntersection*, PlaneIntersection*);

  double edgeLength(unsigned int e) const;
  double edgeLength(unsigned int f, unsigned int e) const;

  BarycentricCoord &getBarycentricCoord(const Coord3D&);
  BarycentricCoord &getBarycentricCoord(const ICoord3D&);
  BarycentricCoord &getBarycentricCoord(const ICoord2D&, const HPixelPlane*);

  unsigned int nextFaceFacetEdgeID() { return faceFacetEdgeCount++; }
				       
  FacetMap2D findPixelPlaneFacets(unsigned int cat,
				  const VoxelSetBoundary &vsb);

  FaceFacets findFaceFacets(unsigned int cat, const FacetMap2D&);
  double intersectionVolume(const FacetMap2D&, const FaceFacets&
// #ifdef DEBUG
// 			    , unsigned int, std::ostream&
// #endif // DEBUG
			    );


  // void setIntersectionPolyFrac(SingleFaceBase*, unsigned int,
  // 			       const PixelPlaneFacet*) const;

  // Return the fractional position of the given point (given in
  // barycentric coords) along the polygon edge of the given facet.
  EdgePosition edgeCoord(const BarycentricCoord&, unsigned int,
			 const PixelPlaneFacet*) const;

  // Return the fractional position of the given point along the given
  // edge of the given face.
  EdgePosition faceEdgeCoord(const BarycentricCoord&, unsigned int f,
			     unsigned int e) const;
  // findFaceEdge is similar, but also computes the edge.
  void findFaceEdge(PlaneIntersection*, unsigned int f, unsigned int &e,
		    EdgePosition &t);

  Coord3D nodePosition(unsigned int n) const { return epts[n]; }
  Coord3D faceCenter(unsigned int f) const { return faceCenters[f]; }
  Coord3D faceAreaVector(unsigned int f) const { return faceAreaVectors[f]; }
  ICoord3D testVoxel(unsigned int f);

  unsigned int nextIntersectionID() { return intersectionID_++; }
  unsigned int nextEquivalenceID() { return equivalenceID_++; }

  FaceEdgeIntersection *newFaceEdgeIntersection(PlaneIntersection*,
						FaceFacetEdge*, bool);

  // Pixel plane intersection points generated by findFaceFacets
  // aren't part of FacetEdges and will need to be deleted explicitly.
  std::set<PlaneIntersection*> extraPoints;

  friend class PixelPlaneIntersectionNR;
  
#ifdef DEBUG
private:
  bool verbose;
  bool verbosecategory;
  bool verboseplane;
  bool verboseface;
public:
  // Redefine these methods to change which categories and planes are verbose.
  bool verboseCategory_(bool, unsigned int) const;
  bool verbosePlane_(bool, const HPixelPlane*) const;
  bool verboseFace_(bool, unsigned int) const;

  bool verboseCategory() const { return verbosecategory; }
  bool verbosePlane() const { return verboseplane; }
  bool verboseFace() const { return verboseface; }

  static std::set<PlaneIntersection*> allIntersections;
  bool verify();
  void dumpEquivalences();
#endif	// DEBUG
};  // end class HomogeneityTet

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the nodes of an edge of a face, going counterclockwise around
// the face.  The faceIndex is the vtk index.  The edgeIndex is the
// index of the edge on the face, not on the tet. 

void getEdgeNodes(unsigned int faceIndex, unsigned int edgeIndex,
		  unsigned int &inode0, unsigned int &inode1);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef DEBUG
void setVerboseFace(unsigned int);
void setVerboseAllFaces();
void setNoVerboseFaces();
void setVerbosePlane(unsigned int, int, int);
void setNoVerbosePlanes();
void setVerboseCategory(unsigned int);
#endif // DEBUG

#endif // HOMOGENEITYTET_H
