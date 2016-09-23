// -*- C++ -*-


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Special classes for keeping track of the boundaries of voxel and
// pixel sets.  2D pixel set boundaries are stored as a set of loops
// encircling the pixels.  3D voxel set boundaries are stored by
// storing their cross sections as 2D pixel set boundaries in each of
// the three xyz directions.  This allows us to use the 2D
// pixel/polygon intersection code to compute the intersection of
// voxel sets with tetrahedra.

#include <oofconfig.h>

#ifndef PIXELSETBOUNDARY_H
#define PIXELSETBOUNDARY_H

#include <map>
#include <set>
#include <vector>

class Plane;
class PixelPlane;
class PixelBdyLoop;
class PixelBdyLoopSegment;
class PixelSetBoundaryBase;
class PixelSetBoundary;
class PixelSetCrossSection;
class VoxelSetBoundary;

#include "common/coord.h"
#include "common/geometry.h"
#include "common/IO/oofcerr.h"

class CMicrostructure;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: Move Plane class to geometry.[Ch]?

class Plane {
protected:
  Coord3D unitNormal_;
  double offset_;		// distance from origin in direction
				// of unitNormal_.  May be negative.
public:
  Plane(const Coord3D &normal, double offset, bool normalize=false);
  Plane() {}
  virtual ~Plane() {}
  const Coord3D &normal() const { return unitNormal_; }
  double offset() const { return offset_; }
  virtual void print(std::ostream &) const;
  bool operator<(const Plane &other) const {
    // Compare normals before offsets, and use > for normals, so that
    // pixel planes are sorted in XYZ order.
    return (unitNormal_ > other.unitNormal_ ||
	    (unitNormal_ == other.unitNormal_ && offset_ < other.offset_));
  }
  bool operator==(const Plane &other) const {
    return offset_ == other.offset_ && unitNormal_ == other.unitNormal_;
  }
  bool operator!=(const Plane &other) const {
    return offset_ != other.offset_ || unitNormal_ != other.unitNormal_;
  }
  // Planes are "opposed" if they occupy the same points in space but
  // have opposing normals.
  bool opposed(const Plane &other) const {
    return unitNormal_ == -1*other.normal() && offset_ == -other.offset();
  }
  // Planes are "coincident" if they occupy the same points in space.
  bool coincident(const Plane &other) const {
    return *this == other || opposed(other);
  }
  // Is the given point on the same side as the normal?
  bool outside(const Coord3D &pt) const;

  // Do this plane and the two given planes define a point?
  bool nonDegenerate(const Plane*, const Plane*) const;
};

// The PixelPlane class provides the link between the 2D pixel
// calculations and the 3D voxel calculations.

class PixelPlane : public virtual Plane {
protected:
  static const unsigned int proj_dirs[6][2];
  unsigned int proj_index; // index into proj_dirs
  unsigned int direction_;
public:
  PixelPlane(unsigned int dir, int offst, int nrml);
  // The null constructor is provided only so that we can create
  // vectors of PixelPlanes.  The elements of the vector should
  // reinitialized with real PixelPlane data.
  PixelPlane() : proj_index(0), direction_(0) {}
  unsigned int direction() const { return direction_; }	// x, y, or z (0, 1, 2)

  // normalOffset is the distance from the origin to the plane,
  // independent of the orientation of the plane.
  int normalOffset() const { return unitNormal_[direction_]*offset_; }
  int normalSign() const { return unitNormal_[direction_] > 0 ? 1 : -1; }
  
  int getCategoryFromPoint(const CMicrostructure*, const Coord2D&) const;
  bool contains(const Coord3D&) const;
  
  // The arguments and return values for these conversion routines are
  // all in pixel and voxel units, not physical units.
  Coord2D convert2Coord2D(const Coord3D&) const;
  Coord3D convert2Coord3D(const Coord2D&) const;
  ICoord2D convert2Coord2D(const ICoord3D&) const;
  ICoord3D convert2Coord3D(const ICoord2D&) const;
  // When converting to a voxel, not just a 3D position, the voxel on
  // the correct side of the plane must be returned.  This subtracts 1
  // if the normal is positive.
  ICoord3D convert2Voxel3D(const ICoord2D&) const;
  ICoord3D normalVector() const;

  virtual void print(std::ostream&) const;
};

Coord3D triplePlaneIntersection(const Plane*, const Plane*, const Plane*);
Coord3D triplePlaneIntersection(const PixelPlane*, const PixelPlane*,
				const PixelPlane*);

// #ifdef OLDPIXELPLANE
// class PixelPlane {
// private:
//   static const unsigned int proj_dirs[6][2];
//   unsigned int proj_index; // index into proj_dirs
//   unsigned int direction_;
//   int offset_;
//   int normal_;
// public:
//   PixelPlane(unsigned int dir, int offset, int normal);
//   // The null constructor is provided only so that we can create
//   // vectors of PixelPlanes.  The elements of the vector should
//   // reinitialized with real PixelPlane data.
//   PixelPlane() : proj_index(0), direction_(0), offset_(-1), normal_(0) {}
//   unsigned int direction() const { return direction_; }	// x, y, or z (0, 1, 2)
//   int offset() const { return offset_; } // distance from plane to the origin
//   int normal() const { return normal_; } // +1 or -1
//   bool operator<(const PixelPlane &other) const {
//     return (direction_ < other.direction_ ||
// 	    (direction_ == other.direction_ &&
// 	     (offset_ < other.offset_ ||
// 	      (offset_ == other.offset_ && normal_ < other.normal_))));
//   }
//   int getCategoryFromPoint(const CMicrostructure*, const Coord2D&) const;
//   bool contains(const Coord3D&) const;
//   PixelPlane inverted() const {
//     return PixelPlane(direction_, offset_, -normal_);
//   }

//   // The arguments and return values for these conversion routines are
//   // all in pixel and voxel units, not physical units.
//   Coord2D convert2Coord2D(const Coord3D&) const;
//   Coord3D convert2Coord3D(const Coord2D&) const;
//   ICoord2D convert2Coord2D(const ICoord3D&) const;
//   ICoord3D convert2Coord3D(const ICoord2D&) const;
//   // When converting to a voxel, not just a 3D position, the voxel on
//   // the correct side of the plane must be returned.  This subtracts 1
//   // if the normal is positive.
//   ICoord3D convert2Voxel3D(const ICoord2D&) const;

//   ICoord3D normalVector() const;
// };
// #endif // OLDPIXELPLANE

std::ostream &operator<<(std::ostream&, const Plane&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

typedef std::multimap<ICoord2D, ICoord2D> DirectedSegMap; // start pt, direction

// TODO: Should PixelBdyLoops be stored in terms of
// PixelPlaneIntersections instead of ICoord2Ds?  That would use more
// memory, but it's the PixelPlaneIntersections that are used in
// HomogeneityTet::doFindPixelPlaneFacets.

class PixelBdyLoop {
private:
  std::vector<ICoord2D> loop;
  ICRectangle *bounds;		// computed by clean
public:
  PixelBdyLoop()
    : bounds(0)
  {}
  PixelBdyLoop(const PixelBdyLoop&);
  ~PixelBdyLoop();
  void add_point(const ICoord2D&);
  // clean is called after all points are added.  It combines colinear
  // consecutive segments and computes the bounding box while doing so.
  void clean();
  // find_bounds just computes the bounding box, for loops constructed
  // in a way that doesn't require them to be cleaned.
  void find_bounds();
  bool closed() const;
  unsigned int size() const { return loop.size(); }
  const ICRectangle &bbox() const { return *bounds; } // in physical coords
  const std::vector<ICoord2D> &segments() const { return loop; }

  // The following methods return information about a given segment in
  // the loop.  Their values could be cached when the loop is cleaned,
  // if recomputing them is too slow.  They're used a lot in the
  // homogeneity calculation.
  ICoord2D icoord(unsigned int) const;
  ICoord2D prev_icoord(unsigned int) const;
  ICoord2D next_icoord(unsigned int) const;
  ICoord2D next2_icoord(unsigned int) const;

  PixelBdyLoopSegment segment(unsigned int) const;
  PixelBdyLoopSegment prev_segment(unsigned int) const;
  PixelBdyLoopSegment next_segment(unsigned int) const;
  
  bool left_turn(unsigned int) const;
  bool right_turn(unsigned int) const;
  bool horizontal(unsigned int) const;
  bool decreasing(unsigned int) const;
  int windingNumber(const Coord2D&) const;
  int area() const;		// for debugging

  bool contains(const ICoord2D&, unsigned int&) const;
  
  friend std::ostream& operator<<(std::ostream&, const PixelBdyLoop&);
  friend class PixelSetBoundary; // for debugging
};

class PixelBdyLoopSegment {
private:
  const PixelBdyLoop *loop_;
  unsigned int loopseg_;
public:
  PixelBdyLoopSegment(const PixelBdyLoop *l, unsigned int s)
    : loop_(l), loopseg_(s)
  {}
  PixelBdyLoopSegment() : loop_(NULL), loopseg_(0) {}
  const PixelBdyLoop *loop() const { return loop_; }
  unsigned int loopseg() const { return loopseg_; }
  // TODO: Should firstPt and secondPt return references?
  ICoord2D firstPt() const { return loop_->icoord(loopseg_); }
  ICoord2D secondPt() const { return loop_->next_icoord(loopseg_); }
  bool follows(const PixelBdyLoopSegment &other) const {
    return other.secondPt() == firstPt();
  }
  bool horizontal() const { return loop_->horizontal(loopseg_); }
  int length() const;
  bool operator<(const PixelBdyLoopSegment&) const; // for std::set
  bool operator==(const PixelBdyLoopSegment&) const;
  bool operator!=(const PixelBdyLoopSegment&) const;
  PixelBdyLoopSegment &operator=(const PixelBdyLoopSegment &other);

  // Is a point to the right of the segment?
  bool onRight(const Coord2D&) const;

  PixelBdyLoopSegment next() const;
  PixelBdyLoopSegment prev() const;
};

std::ostream& operator<<(std::ostream&, const PixelBdyLoop&);
std::ostream& operator<<(std::ostream&, const PixelBdyLoopSegment&);

typedef std::set<ICoord2D> SegSet2D;


// Base class for PixelSetBoundary and PixelSetCrossSection.

// TODO: Remove PixelSetCrossSection class and merge
// PixelSetBoundaryBase with PixelSetBoundary.

class PixelSetBoundaryBase {
protected:
  const CMicrostructure *microstructure;
  ICRectangle *bounds;		// in 2D pixel coords
  std::vector<PixelBdyLoop*> loopset;
public:
  PixelSetBoundaryBase(const CMicrostructure*);
  virtual ~PixelSetBoundaryBase();
  const std::vector<PixelBdyLoop*> &get_loops() const { return loopset; }
  const ICRectangle &bbox() const { return *bounds; } // in pixel coords
};

// PixelSetBoundary stores the 2D loops that define the exterior
// facets of a voxel set.  The way this works is, you create it with a
// microstructure, then put in all the pixels in the pixel set for
// which you want this to be the boundary, then call the
// "find_boundary" method, which finds all the loops and assigns them
// to the "loopset" member.

class PixelSetBoundary : public PixelSetBoundaryBase {
private:
  SegSet2D segmentsLR;		// segments going from left to right
  SegSet2D segmentsRL;		// ... right to left
  SegSet2D segmentsUD;		// ... up to down
  SegSet2D segmentsDU;		// ... down to up

  PixelBdyLoop *find_loop(DirectedSegMap&);
// #ifdef DEBUG
//   int npixels;
// #endif // DEBUG
public:
  PixelSetBoundary(const CMicrostructure *ms)
    : PixelSetBoundaryBase(ms)
// #ifdef DEBUG
//     , npixels(0)
// #endif // DEBUG
  {}
  void add_pixel(const ICoord2D&);
  void find_boundary();
  // friend std::ostream& operator<<(std::ostream &, const PixelSetBoundary&);
  friend class PixelBdyLoop;

// #ifdef DEBUG
//   void dump() const;
// #endif
};

// // For debugging....
// std::ostream& operator<<(std::ostream &, const PixelSetBoundary &);

// PixelSetCrossSection stores the loops that define the cross section
// of a pixel plane and a voxel set.  Geometrically it's more like the
// 2D PixelSetBoundary than the 3D PixelSetBoundary is, but it's
// constructed differently than 2D PixelSetBoundary.
// PixelSetCrossSection is constructed from existing 3D
// PixelSetBoundarys.

class PixelSetCrossSection : public PixelSetBoundaryBase {
public:
  PixelSetCrossSection(const CMicrostructure *ms)
    : PixelSetBoundaryBase(ms)
  {}
  void add_loop(PixelBdyLoop*);
};

typedef std::map<PixelPlane, PixelSetBoundary*> PixelSetBoundaryMap;
typedef std::map<PixelPlane, PixelSetCrossSection*> PixelSetCrossSectionMap;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// TODO: When categories change in the MS, keep track of which ones
// have changed and recompute VoxelSetBoundarys only for them.

class VoxelSetBoundary {
private:
  // For each c-coordinate (x, y, or z) store a PixelSetBoundaryMap
  // for the voxel faces (ie, pixels) on the +c side of the voxel set
  // and on the -c side.  Storing the +c and -c sets separately means
  // that we don't have to store normal information with the pixels.
  PixelSetBoundaryMap pxlSetBdys;
  // The difference between pxlSetBdys and pxlSetCSs is that
  // pxlSetBdys[p] contains the boundaries on PixelPlane p of the
  // exterior facets of the voxel set, while pxlSetCSs[p] contains the
  // boundaries of the cross section of the voxel set with the
  // PixelPlane.  Cross sections are computed and cached on demand.
  // They're needed in categoryVolumes only when a tet face coincides
  // with a pixel plane.
  mutable PixelSetBoundaryMap pxlSetCSs;
  ICRectangularPrism *bounds;
public:
  const CMicrostructure *microstructure;

  VoxelSetBoundary(const CMicrostructure *ms)
    : bounds(0),
      microstructure(ms)
  {}
  ~VoxelSetBoundary();
  void addFace(const ICoord&, unsigned int, int);
  void find_boundaries();
  const ICRectangularPrism &bbox() const { return *bounds; }

  const PixelSetBoundaryMap &getPixelSetBdys() const { return pxlSetBdys; }
  const std::vector<PixelBdyLoop*> &getPlaneCS(const PixelPlane&,
					       unsigned int
#ifdef DEBUG
					       , bool
#endif // DEBUG
					       ) const;

// #ifdef DEBUG
//   void dumpPSBs() const;
// #endif // DEBUG
};

std::ostream &operator<<(std::ostream&, const VoxelSetBoundary&);


#endif // PIXELSETBOUNDARY_H
