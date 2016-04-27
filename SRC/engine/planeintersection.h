// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PLANEINTERSECTION_H
#define PLANEINTERSECTION_H

#include <oofconfig.h>

// This file defines PlaneIntersection and its many subclasses.  A
// PlaneIntersection is a point in space defined by the intersection
// of three or more planes, which may be either PixelPlanes or
// FacePlanes.  Different kinds of PlaneIntersections arise in
// different situations and store different topological
// information.  The PlaneIntersection classes are used by
// HomogeneityTet and PixelPlaneFacet when computing a Skeleton
// element's homogeneity.

// PlaneIntersection
// | |  abstract base class
// | |  knows location in 3D and 2D (given a PixelPlane)
// | |  computes equivalence to any other PlaneIntersection by
// | |     counting shared planes
// | |
// | TripleFaceIntersection
// |     intersection of 3 tet faces (at a tet node)
// |     no pixel plane given
// |
// PixelPlaneIntersection
//  | |    intersection on a pixel plane
//  | |    used when finding the intersection of voxel set boundary loops
//  | |      and tet polygons on a pixel plane 
//  | |  
//  | RedundantIntersection
//  |   marks a point that's been merged with another PixelPlaneIntersection
//  |   used for bookkeeping because FacetEdges own their endpoints,
//  |     so endpoints can't be shared.
//  |  
//  PixelPlaneIntersectionNR
//   |  non-redundant PixelPlaneIntersections
//   | 
//   | The remaining subclasses use intermediate mix-in classes
//   +-+-+-+-+ 
//   | | | | |
//   | | | | TriplePixelPlaneIntersection
//   | | | |    intersection of three pixel planes
//   | | | |
//   | | | SimpleIntersection
//   | | |   VSB loop intersecting the tet polygon
//   | | |   two pixel planes and one tet face
//   | | |
//   | | MultiVSBIntersection
//   | |   VSB corner intersecting the tet polygon
//   | |   three pixel planes and one tet face
//   | |
//   | MultiCornerIntersection
//   |   VSB corner intersecting a tet polygon corner
//   |   three pixel planes and two or more tet faces
//   |
//   MultiFaceIntersection
//    |   tet polygon corner intersecting at most one VSB segment
//    |   two or more tet faces and one or two pixel planes    
//    |
//    TetIntersection
//     | |   A corner of the tet polygon that's not on a VSB segment
//     | |
//     | TetEdgeIntersection
//     |    a tet edge intersecting the base pixel plane
//     |    two tet faces and one pixel plane
//     |
//     TetNodeIntersection
//        a tet node that lies on the pixel plane
//        three tet faces and one pixel plane


#include "common/setutils.h"
#include "engine/barycentric.h"
#include "engine/homogeneitytet_i.h"
#include "engine/pixelplanefacet_i.h"
#include "engine/planeintersection_i.h"

// Forward declarations of classes that are only used internally in
// this file and planeintersection.C.
class MultiVSBbase;
class SingleVSBbase;

// Base class for the points defined by the intersection of planes.

class PlaneIntersection {
protected:
  mutable int equivalence_;    // -1 means it hasn't been assigned yet
public:
  PlaneIntersection()
    : equivalence_(-1)
#ifdef DEBUG
    , verbose(false)
#endif // DEBUG
  {}
  virtual ~PlaneIntersection() {}
  virtual PlaneIntersection *clone() const = 0;

  virtual Coord3D location3D() const = 0;
  virtual Coord2D location2D(const PixelPlane *pp) const {
    return pp->convert2Coord2D(location3D());
  }

  // Intersections are equivalent if they have any three distinct
  // planes in common.
  virtual bool isEquivalent(const PlaneIntersection*) const = 0;
  virtual bool isEquivalent(const TripleFaceIntersection*) const = 0;
  virtual bool isEquivalent(const PixelPlaneIntersectionNR*) const = 0;
  virtual bool isEquivalent(const RedundantIntersection*) const = 0;

  virtual bool samePixelPlanes(const PlaneIntersection*) const = 0;
  virtual bool samePixelPlanes(const TripleFaceIntersection*) const = 0;
  virtual bool samePixelPlanes(const PixelPlaneIntersectionNR*) const = 0;
  virtual bool samePixelPlanes(const RedundantIntersection*) const = 0;

  int equivalence() const { return equivalence_; }
  void setEquivalence(int i) const { equivalence_ = i; }

  // Which edge of the given tet face is this intersection on?  May
  // return NONE.
  virtual unsigned int findFaceEdge(unsigned int,
				    const HomogeneityTet*) const = 0;

  virtual BarycentricCoord baryCoord(const HomogeneityTet*) const;
  virtual void print(std::ostream&) const = 0;

#ifdef DEBUG
  mutable bool verbose;
#endif // DEBUG
};

std::ostream &operator<<(std::ostream&, const PlaneIntersection&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TripleFaceIntersection is the intersection of three tetrahedron
// faces.  No pixel planes are involved.

class TripleFaceIntersection : public PlaneIntersection {
private:
  FacePlaneSet faces_;
  unsigned int node_;
  Coord3D loc_;
public:
  TripleFaceIntersection(unsigned int node, const HomogeneityTet*);
  virtual TripleFaceIntersection *clone() const;
  const FacePlaneSet &faces() const { return faces_; }
  virtual Coord3D location3D() const { return loc_; }
  unsigned int getNode() const { return node_; }
  virtual unsigned int findFaceEdge(unsigned int, const HomogeneityTet*) const;
  virtual BarycentricCoord baryCoord(const HomogeneityTet*) const;
  virtual void print(std::ostream&) const;
  
  virtual bool isEquivalent(const PlaneIntersection*) const;
  virtual bool isEquivalent(const TripleFaceIntersection*) const;
  virtual bool isEquivalent(const PixelPlaneIntersectionNR*) const;
  virtual bool isEquivalent(const RedundantIntersection*) const;

  virtual bool samePixelPlanes(const PlaneIntersection*) const {
    return false;
  }
  virtual bool samePixelPlanes(const TripleFaceIntersection*) const {
    return false;
      };
  virtual bool samePixelPlanes(const PixelPlaneIntersectionNR*) const {
    return false;
  }
  virtual bool samePixelPlanes(const RedundantIntersection*) const {
    return false;
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// PixelPlaneIntersection is the base class for intersection points on
// a pixel plane.  It's used when computing PixelPlaneFacets.  The
// intersections will be intersections of segments of a voxel set
// boundary perimeter with other voxel set boundary segments in the
// pixel plane or with tet faces, or the intersection of two or more
// tet faces with the pixel plane.

// PixelPlaneIntersection is actually a pure virtual class.  Most
// subclasses of it are derived from PixelPlaneIntersectionNR.  NR
// stands for Not Redundant, because RedundantIntersection is also
// derived from PixelPlaneIntersection.  RedundantIntersections refer
// to a PixelPlaneIntersectionNR, for which they rely on for all of
// their data.  They're used when it's determined that two FacetEdges
// meet at a point -- each FacetEdge owns the PixelPlaneIntersections
// at its endpoints, so the PixelPlaneIntersection objects can't be
// shared between FacetEdges.  When the endpoints coincide, one of
// them is a RedundantIntersection, and uses the data from the other
// one.

class PixelPlaneIntersection : public PlaneIntersection {
private:
  // edge_ is the edge of the facet that this intersection point was
  // constructed on.  If it's at a corner, it may actually be on more
  // than one edge, but for computational reasons it's associated with
  // just one.
  FacetEdge *edge_;
public:
  PixelPlaneIntersection()
    : edge_(nullptr)
  {}
  
  // Despite the fact that clone() has already been declared in the
  // PlaneIntersection base class and is not actually defined here in
  // PixelPlaneIntersection, it's necessary to declare it here so that
  // cloned PixelPlaneIntersections aren't returned as
  // PlaneIntersections.
  virtual PixelPlaneIntersection *clone() const = 0;
  
  virtual PixelPlaneIntersectionNR *referent() = 0;
  virtual const PixelPlaneIntersectionNR *referent() const = 0;

  virtual CrossingType crossingType() const = 0;
  
  // This intersection point is an end point of the given facet edge.
  // The edge owns the intersection point and will delete it when the
  // edge is destroyed.  If two edges meet at a point, one of the
  // endpoints will be a RedundantIntersection.  The edges will not
  // share PixelPlaneIntersection instances.
  void setEdge(FacetEdge *edge) { edge_ = edge; }
  FacetEdge *getEdge() const { return edge_; }

  // locateOnPolygonEdge stores the point in the PolyEdgeIntersections
  // vectors after coincidence checking has been done.
  // RedundantIntersections and intersections that aren't on polygon
  // edges don't store themselves.
  virtual void locateOnPolygonEdge(std::vector<PolyEdgeIntersections>&,
				   const PixelPlaneFacet*) const = 0;
  virtual unsigned int minPolyEdge(const PixelPlaneFacet*) const = 0;
  virtual unsigned int maxPolyEdge(const PixelPlaneFacet*) const = 0;
  bool onOnePolySegment(const PixelPlaneIntersection*, const PixelPlaneFacet*)
    const;
  unsigned int sharedPolySegment(const PixelPlaneIntersection*,
				 const PixelPlaneFacet*) const;

  // getPolyEdge returns the index of the intersection's polygon edge,
  // if there's only one. Otherwise, it returns NONE.
  virtual unsigned int getPolyEdge(const PixelPlaneFacet*) const = 0;
  // getPolyFrac returns the intersection's parametric position along
  // the given polygon edge.
  virtual double getPolyFrac(unsigned int, const PixelPlaneFacet*) const = 0;

  virtual double getLoopFrac(const PixelBdyLoopSegment &seg) const = 0;
  
  // Double dispatch methods for comparison and merging with various
  // types of PixelPlaneIntersection.
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
					      const PixelPlaneIntersection*,
					      const PixelPlaneFacet*) const = 0;
  virtual bool isMisordered(const PixelPlaneIntersection*,
			    const PixelPlaneFacet*) const = 0;

}; // class PixelPlaneIntersection

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

enum ISEC_ORDER {FIRST, SECOND, NONCONTIGUOUS};

class PixelPlaneIntersectionNR : public PixelPlaneIntersection {
protected:
  // These are the planes that define the intersection point.  There
  // may be more than three of them, but the extras must all be
  // FacePlanes, not HPixelPlanes or FacePixelPlanes.
  PixelPlaneSet pixelPlanes_;	// pixel planes that don't coincide with faces
  FacePlaneSet faces_;		// faces that don't coincide with pixel planes
  FacePixelPlaneSet pixelFaces_; // faces that do coincide with pixel planes

  Coord3D loc_;

  // void addPixelPlane(const HomogeneityTet*, const HPixelPlane*);
  // void addFacePlane(const HomogeneityTet*, unsigned int);

  CrossingType crossing_;	// may be ENTRY, EXIT, or NONCROSSING

  // Either computeLocation or setLocation should be called by the
  // subclass's constructor.
  void computeLocation();	// use planes to compute loc_
  void setLocation(const Coord3D&); // set loc_ directly

  // Copy the planes from two other PixelPlaneIntersections.
  void copyPlanes(const PixelPlaneIntersectionNR*,
		  const PixelPlaneIntersectionNR*);

#ifdef DEBUG
  std::string printPlanes() const;
#endif // DEBUG
  
public:
  // PixelPlaneIntersectionNR and the mix-in classes below must only
  // have constructors that take no arguments.  This is because we've
  // been lazy and haven't bothered to implement the mix-in classes in
  // a way that makes it possible to pass constructor arguments to
  // them.  Parameters that would be set with constructor arguments
  // are instead set with setXXXX methods called by the derived class
  // constructors.  This is ok because we're not expecting these
  // classes to be extended or used elsewhere.  (We're using mix-in
  // classes instead of regular multiple inheritance because some of
  // the mix-in methods need access to data in the
  // PixelPlaneIntersectionNR base class.)
  
  // RedundantIntersections refer to the PixelPlaneIntersection with
  // which they're redundant through these methods.  Non-redundant
  // intersections refer to themselves.
  virtual PixelPlaneIntersectionNR *referent() { return this; }
  virtual const PixelPlaneIntersectionNR *referent() const { return this; }

  const PixelPlaneSet &pixelPlanes() const { return pixelPlanes_; }
  PixelPlaneSet &pixelPlanes() { return pixelPlanes_; }
  const FacePlaneSet &faces() const { return faces_; }
  FacePlaneSet &faces() { return faces_; }
  // TODO: Come up with a better name than pixelFaces.
  const FacePixelPlaneSet &pixelFaces() const { return pixelFaces_; }
  FacePixelPlaneSet &pixelFaces() { return pixelFaces_; }

  virtual bool onSameLoopSegment(const PixelPlaneIntersectionNR*) const = 0;
  virtual bool sameLoopSegment(const SingleVSBbase*) const = 0;
  virtual bool sameLoopSegment(const MultiVSBbase*) const = 0;
  virtual const PixelBdyLoopSegment *sharedLoopSegment(
					 const PixelPlaneIntersectionNR*)
    const = 0;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const SingleVSBbase*)
    const = 0;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const MultiVSBbase*)
    const = 0;

  // If the second arg to onSameFacePlane is non-null, that plane will
  // be excluded from the calculation.  This is so that the plane of a
  // PixelPlaneFacet won't appear to be a common face of its facet
  // corners.
  bool onSameFacePlane(const PixelPlaneIntersectionNR*,
		       const FacePixelPlane*) const;
  const FacePlane *sharedFace(const PixelPlaneIntersectionNR*) const;
  // This version excludes a face, as in onSameFacePlane, above.
  const FacePlane *sharedFace(const PixelPlaneIntersectionNR*,
			      const FacePixelPlane*) const;
  const std::vector<const FacePlane*> sharedFaces(
				  const PixelPlaneIntersectionNR*) const;

  // bool samePixelPlanes(const PixelPlaneIntersectionNR*) const;

  virtual Coord3D location3D() const { return loc_; }

  // pixelPlaneSets() and facePlaneSets() return iterators that can be
  // used in a range-based for loop to iterate over all PixelPlanes or
  // all FacePlanes (including those in pixelFaces_).
  typedef TwoSetIterator<const HPixelPlane, PixelPlaneSet, FacePixelPlaneSet> PixelPlaneSets;
  PixelPlaneSets pixelPlaneSets() const {
    return PixelPlaneSets(pixelPlanes_, pixelFaces_);
  }
  typedef TwoSetIterator<const FacePlane, FacePlaneSet, FacePixelPlaneSet> FacePlaneSets;
  FacePlaneSets facePlaneSets() const {
    return FacePlaneSets(faces_, pixelFaces_);
  }

  // Does the VBS segment enter or leave the tet polygon at this point?
  virtual CrossingType crossingType() const { return crossing_; }
  void setCrossingType(CrossingType t) { crossing_ = t; }

  // getOrdering computes whether two intersection points (this and
  // the given arg) are on consecutive VSB segments, and which comes
  // first when traversing the VSB.  It also returns the VSB segments,
  // in order. 
  virtual ISEC_ORDER getOrdering(const PixelPlaneIntersectionNR*,
				 PixelBdyLoopSegment&,
				 PixelBdyLoopSegment&,
				 ICoord2D&) const = 0;
  virtual ISEC_ORDER ordering(const SingleVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const = 0;
  virtual ISEC_ORDER ordering(const MultiVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const = 0;

  // TODO: Fix the function names.  Polygon edges are sometimes called
  // edges and sometimes called segments.
  // unsigned int nVSBSegments() const {
  //   return pixelPlanes_.size() + pixelFaces_.size()- 1;
  // }
  virtual unsigned int nVSBSegments() const = 0;
  unsigned int nPolySegments() const { return faces_.size(); }

  // Find the beginning or end of the set of contiguous polygon edges
  // at the intersection.
  virtual unsigned int minPolyEdge(const PixelPlaneFacet*) const;
  virtual unsigned int maxPolyEdge(const PixelPlaneFacet*) const;


  void getEdgesOnFaces(const HomogeneityTet*,
		       const PixelPlaneIntersectionNR*, const HPixelPlane*,
		       FaceFacets&) const;
  virtual unsigned int findFaceEdge(unsigned int, const HomogeneityTet*) const;

  virtual void locateOnPolygonEdge(std::vector<PolyEdgeIntersections>&,
				   const PixelPlaneFacet*) const;

  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
					      const PixelPlaneIntersection*,
					      const PixelPlaneFacet*) const = 0;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const SimpleIntersection*,
				      const PixelPlaneFacet*) const = 0;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiFaceIntersection*,
				      const PixelPlaneFacet*) const = 0;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiVSBIntersection*,
				      const PixelPlaneFacet*) const = 0;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiCornerIntersection*,
				      const PixelPlaneFacet*) const = 0;

  virtual bool isMisordered(const PixelPlaneIntersection*,
			    const PixelPlaneFacet*) const = 0;
  virtual bool isMisordered(const SimpleIntersection*,
			    const PixelPlaneFacet*) const = 0;
  virtual bool isMisordered(const MultiFaceIntersection*,
			    const PixelPlaneFacet*) const = 0;
  virtual bool isMisordered(const MultiVSBIntersection*,
			    const PixelPlaneFacet*) const = 0;
  virtual bool isMisordered(const MultiCornerIntersection*,
			    const PixelPlaneFacet*) const = 0;

  virtual bool isEquivalent(const PlaneIntersection*) const;
  virtual bool isEquivalent(const TripleFaceIntersection*) const;
  virtual bool isEquivalent(const PixelPlaneIntersectionNR*) const;
  virtual bool isEquivalent(const RedundantIntersection*) const;

  virtual bool samePixelPlanes(const PlaneIntersection*) const;
  virtual bool samePixelPlanes(const TripleFaceIntersection*) const;
  virtual bool samePixelPlanes(const PixelPlaneIntersectionNR*) const;
  virtual bool samePixelPlanes(const RedundantIntersection*) const;

}; // end class PixelPlaneIntersectionNR

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Mix-in classes for subclasses of PixelPlaneIntersectionNR.  They're
// used as base classes, where the base class of the mix-in itself is
// given as the template parameter.  For example,

//    class D : public MixInA<PixelPlaneIntersectionNR> {}
// is derived from MixInA and PixelPlaneIntersectionNR.
//    class D : public MixInA<MixinB<PixelPlaneIntersectionNR>> {}
// is derived from MixInA, MixInB, and PixelPlaneIntersectionNR.

// Because I've been lazy, none of the constructors for the mix-ins
// and PixelPlaneIntersectionNR can take arguments.  Passing the correct
// arguments to mix-in constructors is difficult, especially when the
// order of multiple mix-ins isn't predetermined.


// SingleFaceMixIn is a base class for an intersection on a
// single polygon segment (ie single tetrahedron face).  That is, the
// intersection is not on a polygon corner or tetrahedron edge.

class SingleFaceBase {
public:
  virtual ~SingleFaceBase() {}
  virtual const FacePlane *getFacePlane() const = 0;
};

template <class BASE>
class SingleFaceMixIn : public BASE, public SingleFaceBase {
protected:
  mutable double polyFrac;  // relative position along polygon segment

  // In an intersection with one face plane, that plane plays a
  // special topological role, since it is used to identify a polygon
  // edge.  We can't just store it in the base class's faces set,
  // because if the plane is coincident with a pixel plane it has to
  // be stored in the pixelplane set.  So to preserve the toplogical
  // info, we have to store it again, here:
  const FacePlane *facePlane_;
public:
  SingleFaceMixIn();
  virtual const FacePlane *getFacePlane() const { return facePlane_; }

  void setPolyFrac(double a) { polyFrac = a; }
  void setFacePlane(const FacePlane *fp) { facePlane_ = fp; }
  virtual double getPolyFrac(unsigned int, const PixelPlaneFacet*) const;
  virtual unsigned int getPolyEdge(const PixelPlaneFacet *facet) const;
  virtual unsigned int maxPolyEdge(const PixelPlaneFacet *facet) const;
  virtual unsigned int minPolyEdge(const PixelPlaneFacet *facet) const;
};

// MultiFaceMixin is for a intersections that occur on multiple tet
// faces (aka polygon edges).

template <class BASE>
class MultiFaceMixin : public BASE
{
public:
  bool inside(const Coord3D &pt) const;
  virtual double getPolyFrac(unsigned int, const PixelPlaneFacet*) const;
  virtual unsigned int getPolyEdge(const PixelPlaneFacet*) const;
  unsigned int getOtherFaceIndex(unsigned int, const PixelPlaneFacet*) const;
};

// SingleVSBmixIn is a templated base class for an intersection that
// is on a single VSB loop segment.  That is, the intersection is not
// on a VSB loop corner.

// SingleVSBbase is a non-templated base class for SingleVSBmixIn that
// makes double dispatch possible without using templated virtual
// functions.

class SingleVSBbase {
public:
#ifdef DEBUG
  SingleVSBbase();
#endif // DEBUG
  virtual ~SingleVSBbase() {}
  virtual const PixelBdyLoopSegment &getLoopSeg() const = 0;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const SingleVSBbase*)
    const = 0;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const MultiVSBbase*)
    const = 0;
  virtual ISEC_ORDER ordering(const SingleVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const = 0;
  virtual ISEC_ORDER ordering(const MultiVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const = 0;
};

template <class BASE> class SingleVSBmixIn : public BASE, public SingleVSBbase {
protected:
  PixelBdyLoopSegment vsbSegment;
  double loopFrac;
public:
#ifdef DEBUG
  SingleVSBmixIn();
#endif // DEBUG
  void setLoopSeg(const PixelBdyLoopSegment &seg) { vsbSegment = seg; }
  void setLoopFrac(double f) { loopFrac = f; }
  virtual const PixelBdyLoopSegment &getLoopSeg() const { return vsbSegment; }
  double getLoopFrac() const { return loopFrac; } // position along VSB segment
  virtual double getLoopFrac(const PixelBdyLoopSegment&) const;
  ICoord2D segEnd(unsigned int i) const {
    return i==0 ? vsbSegment.firstPt() : vsbSegment.secondPt();
  }
  virtual bool onSameLoopSegment(const PixelPlaneIntersectionNR*) const;
  virtual bool sameLoopSegment(const SingleVSBbase*) const;
  virtual bool sameLoopSegment(const MultiVSBbase*) const;
  virtual const PixelBdyLoopSegment *sharedLoopSegment(
					 const PixelPlaneIntersectionNR*) const;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const SingleVSBbase*) const;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const MultiVSBbase*) const;

  virtual ISEC_ORDER getOrdering(const PixelPlaneIntersectionNR*,
				 PixelBdyLoopSegment&,
				 PixelBdyLoopSegment&,
				 ICoord2D&) const;
  virtual ISEC_ORDER ordering(const SingleVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const;
  virtual ISEC_ORDER ordering(const MultiVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const;

  virtual unsigned int nVSBSegments() const { return 1; }
};

// MultiVSBmixIn is for intersections that occur on multiple VSB loop
// edges.  They are therefore on voxel corners.

typedef std::map<PixelBdyLoopSegment, double> PBLSegmentMap;

class MultiVSBbase {
public:
  virtual ~MultiVSBbase() {}
  virtual const PBLSegmentMap &getLoopSegs() const = 0;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const SingleVSBbase*)
    const = 0;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const MultiVSBbase*)
    const = 0;
  virtual ISEC_ORDER ordering(const SingleVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const = 0;
  virtual ISEC_ORDER ordering(const MultiVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&,
			      ICoord2D&) const = 0;
  // MultiVSBmixIn<BASE>::categorizeCorner isn't instantiated unless
  // it's declared virtual here.  I don't understand this.  It
  // shouldn't need to be virtual or declared in MultiVSBbase.
  virtual TurnDirection categorizeCorner(PixelBdyLoopSegment&,
					 PixelBdyLoopSegment&) const = 0;
};

template <class BASE> class MultiVSBmixIn : public BASE, public MultiVSBbase {
protected:
  PBLSegmentMap vsbSegments;
public:
  virtual TurnDirection categorizeCorner(PixelBdyLoopSegment&,
					 PixelBdyLoopSegment&) const;
  virtual const PBLSegmentMap &getLoopSegs() const { return vsbSegments; }
  virtual double getLoopFrac(const PixelBdyLoopSegment &seg) const;
  virtual bool onSameLoopSegment(const PixelPlaneIntersectionNR*) const;
  virtual bool sameLoopSegment(const SingleVSBbase*) const;
  virtual bool sameLoopSegment(const MultiVSBbase*) const;
  virtual const PixelBdyLoopSegment *sharedLoopSegment(
					 const PixelPlaneIntersectionNR*) const;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const SingleVSBbase*) const;
  virtual const PixelBdyLoopSegment *sharedLoopSeg(const MultiVSBbase*) const;

  virtual ISEC_ORDER getOrdering(const PixelPlaneIntersectionNR*,
				 PixelBdyLoopSegment&,
				 PixelBdyLoopSegment&, ICoord2D&) const;
  virtual ISEC_ORDER ordering(const SingleVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&, ICoord2D&) const;
  virtual ISEC_ORDER ordering(const MultiVSBbase*,
			      PixelBdyLoopSegment&,
			      PixelBdyLoopSegment&, ICoord2D&) const;

  virtual unsigned int nVSBSegments() const { return vsbSegments.size(); }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// SimpleIntersection is the intersection of a single polygon segment
// (ie tet face) and a single VSB segment (defined by the intersection
// of two pixel planes, one of which is the base plane of the facet.

class SimpleIntersection :
  public SingleVSBmixIn<SingleFaceMixIn<PixelPlaneIntersectionNR>>
{
public:
  SimpleIntersection(const HomogeneityTet*,
		     const HPixelPlane*, const HPixelPlane*,
		     const PixelBdyLoopSegment&, double,
		     unsigned int, CrossingType);
  virtual SimpleIntersection *clone() const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const PixelPlaneIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const SimpleIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiFaceIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiVSBIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiCornerIntersection*,
				      const PixelPlaneFacet*) const;

  virtual bool isMisordered(const PixelPlaneIntersection*, 
			    const PixelPlaneFacet*) const; 
  virtual bool isMisordered(const SimpleIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiFaceIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiVSBIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiCornerIntersection*, 
			    const PixelPlaneFacet*) const;

  virtual void print(std::ostream&) const;
};

// MultiFaceIntersection is the intersection of a single VSB segment
// with multiple (ie two) tet faces.

class MultiFaceIntersection :
  public SingleVSBmixIn<MultiFaceMixin<PixelPlaneIntersectionNR>>
{
public:
  MultiFaceIntersection(const HomogeneityTet*,
			const HPixelPlane*, const HPixelPlane*,
			const PixelBdyLoopSegment&, double,
			unsigned int, CrossingType);
  MultiFaceIntersection(const HomogeneityTet*, const SimpleIntersection*,
			const SimpleIntersection*);
  MultiFaceIntersection(const HomogeneityTet*, const SimpleIntersection*,
			const MultiFaceIntersection*);
  MultiFaceIntersection() {}
  virtual MultiFaceIntersection *clone() const;
  // Are both polygon segments interior to the voxel?
  Interiority interiority(const PixelPlaneFacet*) const;
  const FacePlane *firstFacePlane(const PixelPlaneFacet*) const;
  void getPolyEdges(const PixelPlaneFacet*, unsigned int&, unsigned int&) const;

  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const PixelPlaneIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const SimpleIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiFaceIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiVSBIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiCornerIntersection*,
				      const PixelPlaneFacet*) const;
  virtual bool isMisordered(const PixelPlaneIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const SimpleIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiFaceIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiVSBIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiCornerIntersection*, 
			    const PixelPlaneFacet*) const;

  virtual void print(std::ostream&) const;
  friend class SimpleIntersection;
};

// MultiVSBIntersection is the intersection of multiple VSB segments
// and a single polygon segment (aka tet face).

class MultiVSBIntersection :
  public SingleFaceMixIn<MultiVSBmixIn<PixelPlaneIntersectionNR>> 
{
public:
  MultiVSBIntersection(const HomogeneityTet*, const PixelPlaneFacet*,
		       const SimpleIntersection*, const SimpleIntersection*);
  MultiVSBIntersection(const HomogeneityTet*, const PixelPlaneFacet*,
		       const SimpleIntersection*, const MultiVSBIntersection*);
  virtual MultiVSBIntersection *clone() const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const PixelPlaneIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const SimpleIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiFaceIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiVSBIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiCornerIntersection*,
				      const PixelPlaneFacet*) const;
  virtual bool isMisordered(const PixelPlaneIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const SimpleIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiFaceIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiVSBIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiCornerIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual void print(std::ostream&) const;
};

// MultiCornerIntersection is the intersection of multiple VSB
// segments and multiple polygon segments.  It's where a polygon
// corner and a VSB loop corner coincide.

class MultiCornerIntersection :
  public MultiFaceMixin<MultiVSBmixIn<PixelPlaneIntersectionNR>>
{
public:
  MultiCornerIntersection(const HomogeneityTet*,
			  const PixelPlaneIntersectionNR*,
			  const PixelPlaneIntersectionNR*);
  virtual MultiCornerIntersection *clone() const;
  virtual bool isMisordered(const PixelPlaneIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const SimpleIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiFaceIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiVSBIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual bool isMisordered(const MultiCornerIntersection*, 
			    const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const PixelPlaneIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const SimpleIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiFaceIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiVSBIntersection*,
				      const PixelPlaneFacet*) const;
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiCornerIntersection*,
				      const PixelPlaneFacet*) const;
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// newIntersection returns either a new SimpleIntersection or a new
// MultiFaceIntersection.

PixelPlaneIntersectionNR *newIntersection(const HomogeneityTet *htet,
					  const HPixelPlane *basePlane,
					  const HPixelPlane *orthoPlane,
					  const PixelBdyLoopSegment &pblSeg,
					  double alpha,
					  unsigned int faceIndex,
					  CrossingType ct);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A TetIntersection is the intersection of a tet edge or node with a
// pixelplane.  The only difference between a TetIntersection and
// other subclasses of PixelPlaneIntersection is that the TetIntersection is
// constructed from the PixelPlane and the tetrahedron, with no
// reference to the VSB or to other PixelPlaneIntersections, so it needs a
// different sort of constructor.  It's otherwise exactly the same as
// a MultiFaceIntersection, although some of the MultiFaceIntersection
// machinery will never be used by a TetIntersection.

class TetIntersection : public MultiFaceIntersection {
public:
  TetIntersection() {}
};

// TetEdgeIntersection is the intersection of a tet edge, defined by two
// faces, with a PixelPlane.  The corners of the polygon formed by the
// intersection of a tet with a PixelPlane are TetEdgeIntersections or
// TetNodeIntersections.

class TetEdgeIntersection : public TetIntersection {
public:
  TetEdgeIntersection(const FacePlane*, const FacePlane*, const HPixelPlane*);
  virtual TetEdgeIntersection *clone() const;
  virtual void print(std::ostream&) const;  
};

// NodeIntersection is the intersection of a tet node, defined by
// three faces, with a PixelPlane.  It is overdefined, but that's ok.
// It's only used when a tet node happens to lie on a pixel plane.
// When a tet node lies on a pixel plane, the corner of the
// intersection polygon at that node is a NodeIntersection.

class TetNodeIntersection : public TetIntersection {
public:
  TetNodeIntersection(const HomogeneityTet*, const HPixelPlane*,
		      unsigned int node);
  virtual TetNodeIntersection *clone() const;
  virtual void print(std::ostream&) const;  
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TriplePixelPlaneIntersection is the intersection of three pixel
// planes.  No tet faces are involved.

class TriplePixelPlaneIntersection
  : public MultiVSBmixIn<PixelPlaneIntersectionNR>
{
public:
  TriplePixelPlaneIntersection(const HPixelPlane*, const HPixelPlane*,
			       const HPixelPlane*);
  virtual TriplePixelPlaneIntersection *clone() const;
  virtual CrossingType crossingType() const { return NONCROSSING; }
  virtual unsigned int findFaceEdge(unsigned int, const HomogeneityTet*) const;
  virtual void locateOnPolygonEdge(std::vector<PolyEdgeIntersections>&,
				   const PixelPlaneFacet*) const
  {}


  // TODO: It should not be necessary to define getPolyEdge,
  // minPolyEdge, maxPolyEdge, and getPolyFrac in this class.  They
  // are meaningless.
  
  // onSameLoopSegment, sameLoopSegment provided by MultiVSBmixIn
  virtual unsigned int getPolyEdge(const PixelPlaneFacet*) const;
  virtual unsigned int minPolyEdge(const PixelPlaneFacet*) const;
  virtual unsigned int maxPolyEdge(const PixelPlaneFacet*) const;
  virtual double getPolyFrac(unsigned int, const PixelPlaneFacet*) const;

  // Since TriplePixelPlaneIntersections aren't on polygon edges, they
  // can't be misordered with respect to intersections on the edges,
  // and never have to merge with other intersections.

  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const PixelPlaneIntersection*,
				      const PixelPlaneFacet*) const
  { return nullptr; }
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const SimpleIntersection*,
				      const PixelPlaneFacet*) const
  { return nullptr; }
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiFaceIntersection*,
				      const PixelPlaneFacet*) const
  { return nullptr; }
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiVSBIntersection*,
				      const PixelPlaneFacet*) const
  { return nullptr; }
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet*,
				      const MultiCornerIntersection*,
				      const PixelPlaneFacet*) const
  { return nullptr; }

  virtual bool isMisordered(const PixelPlaneIntersection*,
			    const PixelPlaneFacet*) const { return false; }
  virtual bool isMisordered(const SimpleIntersection*,
			    const PixelPlaneFacet*) const { return false; }
  virtual bool isMisordered(const MultiFaceIntersection*,
			    const PixelPlaneFacet*) const { return false; }
  virtual bool isMisordered(const MultiVSBIntersection*,
			    const PixelPlaneFacet*) const { return false; }
  virtual bool isMisordered(const MultiCornerIntersection*,
			    const PixelPlaneFacet*) const { return false; }


  virtual void print(std::ostream&) const;
}; // end class TriplePixelPlaneIntersection

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class RedundantIntersection : public PixelPlaneIntersection {
private:
  PixelPlaneIntersectionNR * referent_;
  PixelPlaneFacet *facet_;
public:
  RedundantIntersection(PixelPlaneIntersection *ppi, PixelPlaneFacet*);
  ~RedundantIntersection();
  virtual RedundantIntersection *clone() const;
  virtual const PixelPlaneIntersectionNR *referent() const {
    return referent_; 
  }
  virtual PixelPlaneIntersectionNR *referent() {
    return referent_;
  }
  void update(PixelPlaneIntersection *ppi) {
    referent_ = ppi->referent();
  }
  virtual void locateOnPolygonEdge(std::vector<PolyEdgeIntersections>&,
				   const PixelPlaneFacet*) const {}
  // virtual bool onSameLoopSegment(const PixelPlaneIntersection *ppi) const {
  //   return referent_->onSameLoopSegment(ppi);
  // }
  virtual unsigned int minPolyEdge(const PixelPlaneFacet *facet) const {
    return referent_->minPolyEdge(facet);
  }
  virtual unsigned int maxPolyEdge(const PixelPlaneFacet *facet) const {
    return referent_->maxPolyEdge(facet);
  }
  virtual unsigned int getPolyEdge(const PixelPlaneFacet *facet) const {
    return referent_->getPolyEdge(facet);
  }
  virtual double getPolyFrac(unsigned int edge, const PixelPlaneFacet *facet)
    const
  {
    return referent_->getPolyFrac(edge, facet);
  }
  virtual unsigned int findFaceEdge(unsigned int f, const HomogeneityTet *htet)
    const
  {
    return referent_->findFaceEdge(f, htet);
  }

  virtual double getLoopFrac(const PixelBdyLoopSegment &seg) const {
    return referent_->getLoopFrac(seg);
  }
  
  virtual PixelPlaneIntersectionNR *mergeWith(const HomogeneityTet *htet,
					      const PixelPlaneIntersection *ppi,
					      const PixelPlaneFacet *facet)
    const
  {
    return referent_->mergeWith(htet, ppi, facet);
  }
  virtual bool isMisordered(const PixelPlaneIntersection *ppi,
			    const PixelPlaneFacet *facet)
    const
  {
    return referent_->isMisordered(ppi, facet);
  }

  virtual Coord3D location3D() const {
    return referent_->location3D();
  }
  virtual CrossingType crossingType() const {
    return referent_->crossingType();
  }

  virtual bool isEquivalent(const PlaneIntersection *pi) const {
    return referent_->isEquivalent(pi);
  }
  virtual bool isEquivalent(const TripleFaceIntersection *pi) const {
    return referent_->isEquivalent(pi);
  }
  virtual bool isEquivalent(const PixelPlaneIntersectionNR *pi) const {
    return referent_->isEquivalent(pi);
  }
  virtual bool isEquivalent(const RedundantIntersection *pi) const {
    return referent_->isEquivalent(pi);
  }

  virtual bool samePixelPlanes(const PlaneIntersection *pi) const {
    return referent_->samePixelPlanes(pi);
  }
  virtual bool samePixelPlanes(const TripleFaceIntersection *pi) const {
    return referent_->samePixelPlanes(pi);
  }
  virtual bool samePixelPlanes(const PixelPlaneIntersectionNR *pi) const {
    return referent_->samePixelPlanes(pi);
  }
  virtual bool samePixelPlanes(const RedundantIntersection *pi) const {
    return referent_->samePixelPlanes(pi);
  }

  virtual void print(std::ostream&) const;
}; // end class RedundantIntersection

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream&, const CrossingType);

#endif // PLANEINTERSECTION_H
