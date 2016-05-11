// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PIXELPLANEFACET_H
#define PIXELPLANEFACET_H

#include <oofconfig.h>

#include "engine/pixelplanefacet_i.h"

#include "common/coord.h"
#include "common/pixelsetboundary.h"
#include "common/setutils.h"
#include "engine/homogeneitytet_i.h"
#include "engine/planeintersection_i.h"

#include <vector>
#include <map>

typedef std::multimap<const Coord2D, PixelPlaneIntersectionNR*> IsecsNearCoord;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Planes used in the homogeneity calculation are all derived from
// HPlane, which just lets us add virtual functions whose arguments
// are classes in the engine module, and which aren't allowed in the
// base Plane class in the common module.

class HPlane : public virtual Plane {
public:
  virtual bool isPartOf(const PixelPlaneIntersectionNR*) const = 0;
  virtual void addToIntersection(PixelPlaneIntersectionNR*) const = 0;
  virtual void addToEquivalence(IsecEquivalenceClass*) const = 0;
  virtual std::string shortName() const = 0;
};

class HPixelPlane : public virtual HPlane, public virtual PixelPlane {
public:
  HPixelPlane(unsigned int dir, int offst, int nrml)
    : Plane(axisVector(dir)*nrml, offst*nrml, false),
      PixelPlane(dir, offst, nrml)
  {}
  HPixelPlane(const PixelPlane &pp)
    : Plane(pp),
      PixelPlane(pp)
  {}
  HPixelPlane() {}
  virtual bool isPartOf(const PixelPlaneIntersectionNR*) const;
  virtual void addToIntersection(PixelPlaneIntersectionNR*) const;
  virtual void addToEquivalence(IsecEquivalenceClass*) const;
  virtual std::string shortName() const;
};

class FacePlane : public virtual HPlane {
private:
  // Planes are compared by pointer, so we don't want them to be copied.
  FacePlane(const FacePlane&) = delete;
  FacePlane(FacePlane&&) = delete;
protected:
  const unsigned int face_;
public:
  FacePlane(unsigned int face, const Coord3D &normal, double offset)
    : Plane(normal, offset),
      face_(face)
  {}
  FacePlane(unsigned int face)
    : face_(face)
  {}
  virtual bool isPartOf(const PixelPlaneIntersectionNR*) const;
  virtual void addToIntersection(PixelPlaneIntersectionNR*) const;  
  virtual void addToEquivalence(IsecEquivalenceClass*) const;
  virtual void print(std::ostream&) const;
  unsigned int face() const { return face_; }
  virtual std::string shortName() const;
};

class FacePixelPlane : public virtual HPixelPlane, public virtual FacePlane {
private:
  FacePixelPlane(const FacePixelPlane&) = delete;
  FacePixelPlane(FacePixelPlane&&) = delete;
public:
  FacePixelPlane(unsigned int dir, int offst, int nrml, unsigned int face)
    : Plane(axisVector(dir)*nrml, offst*nrml, false),
      PixelPlane(dir, offst, nrml),
      FacePlane(face)
  {}
  FacePixelPlane(const PixelPlane *pixplane, unsigned int face)
    : Plane(*pixplane),
      PixelPlane(*pixplane),
      FacePlane(face)
  {}
  virtual bool isPartOf(const PixelPlaneIntersectionNR*) const;
  virtual void addToIntersection(PixelPlaneIntersectionNR*) const;
  virtual void addToEquivalence(IsecEquivalenceClass*) const;
  virtual void print(std::ostream&) const;
  virtual std::string shortName() const;  
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FacetEdge {
protected:
  // FacetEdges own the PlaneIntersections that they store.  The copy
  // constructor clones them and the destructor deletes them.
  PixelPlaneIntersection *start_;
  PixelPlaneIntersection *stop_;
  bool nullified_;
public:
  FacetEdge(PixelPlaneIntersection *s, PixelPlaneIntersection *e);
  virtual ~FacetEdge();
  FacetEdge(const FacetEdge&);
  FacetEdge(FacetEdge&&);
  double length2() const; 	// length squared

  virtual PixelPlaneIntersection *startFace() { return nullptr; }
  virtual PixelPlaneIntersection *stopFace() { return nullptr; }

  void nullify() { nullified_ = true; }
  bool nullified() const { return nullified_; }
  
  void replacePoint(const PixelPlaneIntersection *oldPt,
		    PixelPlaneIntersection *newPt);
  Coord2D startPos(const PixelPlane *p) const;
  Coord2D endPos(const PixelPlane *p) const;
  Coord3D startPos3D() const;
  Coord3D endPos3D() const;
  virtual void getEdgesOnFaces(HomogeneityTet*, const HPixelPlane*,
			       FaceFacets&) const
  {}

  PixelPlaneIntersection *startPt() { return start_; }
  PixelPlaneIntersection *endPt() { return stop_; }
  const PixelPlaneIntersection *startPt() const { return start_; }
  const PixelPlaneIntersection *endPt() const { return stop_; }

  // Switch the start or stop points with their referents.
  void swapStart();
  void swapStop();
};

std::ostream &operator<<(std::ostream&, const FacetEdge&);

// TODO: Do we really need subclasses of FacetEdge?

// A PixelFacetEdge is one that follows a pixel boundary and doesn't
// intersect any face of the tetrahedron.

class PixelFacetEdge : public FacetEdge {
public:
  PixelFacetEdge(TriplePixelPlaneIntersection *s,
		 TriplePixelPlaneIntersection *e);
  // virtual FacetEdge *reversed() const;
};

// A StartFaceIntersectionEdge is one that follows a pixel boundary but
// starts at a tet face and ends on a pixel corner.

class StartFaceIntersectionEdge : public FacetEdge {
public:
  StartFaceIntersectionEdge(PixelPlaneIntersection *s,
			    TriplePixelPlaneIntersection *e);
  virtual PixelPlaneIntersection *startFace() { return start_; }
};

class StopFaceIntersectionEdge : public FacetEdge {
public:
  StopFaceIntersectionEdge(TriplePixelPlaneIntersection *s,
			   PixelPlaneIntersection *e);
  virtual PixelPlaneIntersection *stopFace() { return stop_; }
};

class PolygonEdge : public FacetEdge {
public:
  PolygonEdge(PixelPlaneIntersection *f0, PixelPlaneIntersection *f1);
  virtual void getEdgesOnFaces(HomogeneityTet*, const HPixelPlane*,
			       FaceFacets&) const;
  // virtual FacetEdge *reversed() const;
};

// A TwoFaceIntersectionEdge is one that crosses from one tet face to
// another.

class TwoFaceIntersectionEdge : public FacetEdge {
public:
  TwoFaceIntersectionEdge(PixelPlaneIntersection *s, PixelPlaneIntersection *e)
    : FacetEdge(s, e)
  {}
  virtual PixelPlaneIntersection *startFace() { return start_; }
  virtual PixelPlaneIntersection *stopFace() { return stop_; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PixelPlaneFacet {
private:
  std::vector<FacetEdge*> edges;
  double getArea() const;
  const std::vector<const TetIntersection*> &tetPts;
  mutable double area_;
  mutable bool areaComputed_;
  const bool onFace;
  FaceEdgeMap faceEdgeMap;  // maps Planes to polygon edge numbers
  std::set<RedundantIntersection*> redundantIntersections;

public:
  HomogeneityTet * const htet;
  const HPixelPlane * const pixplane;

private:
  // The resolveXXXCoincidence methods return true if they were
  // successful.  If they
  bool resolveTwoFoldCoincidence(const std::set<PixelPlaneIntersectionNR*>&);
  bool resolveThreeFoldCoincidence(const std::set<PixelPlaneIntersectionNR*>&);
  bool resolveMultipleCoincidence(const std::set<PixelPlaneIntersectionNR*>&,
				  unsigned int);
  void replaceIntersection(PixelPlaneIntersection*, PixelPlaneIntersection*)
    const;

  bool badTopology_(const MultiFaceIntersection*, const MultiFaceIntersection*,
		    unsigned int) const;
  
  std::vector<PixelPlaneIntersectionNR*> tripleCoincidence(
					   PixelPlaneIntersectionNR*,
					   PixelPlaneIntersectionNR*,
					   PixelPlaneIntersectionNR*) const;
  
  void addEdges(const PixelPlaneIntersection*, const PixelPlaneIntersection*);

  void removeNullEdges();

public:
  PixelPlaneFacet(HomogeneityTet*, const HPixelPlane*,
		  const TetIntersectionPolygon&, bool
#ifdef DEBUG
		  , bool verbose
#endif // DEBUG
		  );
  ~PixelPlaneFacet();
  void addEdge(FacetEdge*);
  bool completeLoops();

  double area() const;
  Coord3D center() const;
  Coord3D areaVector() const;
  bool empty() const { return edges.empty(); }
  unsigned int size() const { return edges.size(); }
  unsigned int polygonSize() const { return tetPts.size(); }
  BarycentricCoord polygonCornerBary(unsigned int) const;
  Coord2D polygonCorner(unsigned int i) const;
  unsigned int getPolyEdge(const Plane *fp) const;
  const FacePlane *getFacePlane(unsigned int) const;
  const FacePixelPlane *getBaseFacePlane() const;

  bool onOppositeEdges(const SimpleIntersection*, const SimpleIntersection*)
    const;
  
  
  bool vsbCornerCoincidence(const PixelPlaneIntersectionNR*,
			    const PixelPlaneIntersectionNR*) const;
  bool polyCornerCoincidence(const PixelPlaneIntersectionNR*,
			     const PixelPlaneIntersectionNR*) const;
  bool polyVSBCornerCoincidence(const PixelPlaneIntersectionNR*,
				const PixelPlaneIntersectionNR*) const;

  bool badTopology(const SimpleIntersection*,
		   const MultiFaceIntersection*) const;
  bool badTopology(const SimpleIntersection*,
		   const MultiVSBIntersection*) const;
  bool badTopology(const SimpleIntersection*,
		   const MultiCornerIntersection*) const;
  bool badTopology(const MultiFaceIntersection*,
		   const MultiFaceIntersection*) const;
  bool badTopology(const MultiFaceIntersection*,
		   const MultiVSBIntersection*) const;
  bool badTopology(const MultiFaceIntersection*,
		   const MultiCornerIntersection*) const;

  void clear();

  void getEdgesOnFaces(FaceFacets&) const;

  void newRedundantIntersection(RedundantIntersection*);
  void removeRedundantIntersection(RedundantIntersection*);

#ifdef DEBUG
  bool verbose;
  void dump() const;
  void getEndPoints(unsigned int i, Coord3D &startPt, Coord3D &endPt) const {
    startPt = edges[i]->startPos3D();
    endPt = edges[i]->endPos3D();
  }
#endif // DEBUG

  friend std::ostream &operator<<(std::ostream&, const PixelPlaneFacet&);
}; // end class PixelPlaneFacet

std::ostream &operator<<(std::ostream&, const PixelPlaneFacet&);

#endif // PIXELPLANEFACET_H
