// -*- C++ -*-
// $RCSfile: pixelsetboundary.h,v $
// $Revision: 1.20.10.21 $
// $Author: langer $
// $Date: 2014/12/12 18:53:03 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PIXELSETBOUNDARY_H
#define PIXELSETBOUNDARY_H

// TODO 3.1: Far too many files are recompiled when this one is
// edited.  Reduce the number of places in which it and its dependents
// are included.

#include <map>
#include <vector>

#include "common/coord.h"
#include "common/geometry.h"
#include "common/IO/oofcerr.h"

class CMicrostructure;

// Special classes for keeping track of the boundaries of pixel sets.

// PixelBdySegment object is either the bottom or left-side boundary
// of the pixel located at ICoord in the mesh.  The purpose of
// identifying things this way is to avoid any possible round-off
// problems.  Note that, for pixel boundary segments on the right-hand
// edge or the top of a microstructure, the ICoord passed in will not
// correspond to an actual pixel in that microstructure -- the segment
// will be (e.g.) the left-hand boundary of a farther-than-rightmost
// pixel.

// The boolean flags provide enough data to locate and direct the
// segment, but this is not done initially due to possible round-off
// problems.  All these segments are either horizontal or vertical.
// The "local" flag is true if this segment is the bottom or left
// segment of the pixel indicated by the ICoord, and false if it is
// the top segment of the pixel below the ICoord or the right segment
// of the pixel to the left of the ICoord.

#if DIM == 2
class PixelSetBoundary;


// Special utility class for pixel boundary intersections, so we can
// keep track of "incoming" versus "outgoing" intersections.  Incoming
// and outgoing are intended to be used with respect to elements --
// entry==true means that the pixel boundary enters the element at
// this intersection, and entry==false means that it exits the element
// at this intersection.
class PixelBdyIntersection {
private:
  // The node-index and fraction values are specific to a particular
  // skeleton element, and are filled in by the cskeleton element.
  // The node index is an integer indicating which node is at the
  // start of the element boundary on which the intersection occurs,
  // and the "fraction" number is the square of the distance from the
  // start of this element boundary to the location of the
  // intersection.
  int node_index;
  double fraction; 
public:
  Coord location;
  bool entry;  // 

  PixelBdyIntersection(Coord &loc, bool ntry) 
    : node_index(0), fraction(0), location(loc), entry(ntry)
  {} 
  PixelBdyIntersection() 
    : node_index(0), fraction(0), entry(false) 
  {}
  void set_element_data(int ni, double f) {
    node_index = ni;
    fraction = f;
  }
  int get_element_node_index() const { return node_index; }
  double get_element_fraction() const { return fraction; }
};

typedef std::pair<Coord, Coord> CoordPair;

class PixelBdySegment {
  // Represents a collinear and contiguous set of pixel edges.
private:
  ICoord pixel;
  bool horizontal;
  bool local;
  mutable bool coordinated; // Indicates if start, end have been set.
  mutable ICoord start, end;

  // For speed, geometric data is represented several ways.  fp_level
  // is the "level" (x-value of vertical, y-value of horizontal) of
  // this segment.  fp_start and fp_end are the start and end points
  // on the x-axis for horizontal, and y-axis for vertical, segments.
  // fp_first and fp_last are a second representation of the start and
  // end coordinates, used in intersection checking, and guaranteed to
  // have the property that fp_first < fp_last.  This saves continual
  // checking of the "local" flag.
  mutable double fp_level, fp_start, fp_end, fp_first, fp_last;
  mutable bool floated; // Indicates if the above have been set.
public:
  PixelBdySegment(const ICoord &pxl, bool horiz, bool lcl) :
    pixel(pxl), horizontal(horiz), local(lcl), 
    coordinated(false), floated(false) {}
  bool operator<(const PixelBdySegment &other) const;
  ICoord coordinate() const;
  void extend();
  void set_floats(const Coord&) const;

  // Intersection-related support functions for the skeleton elements'
  // categoryAreas computation.
  bool find_no_intersection(const Coord* const, int, const Coord&) const;

  int find_one_intersection(const Coord* const, int,
			    PixelBdyIntersection&, bool) const;

//   bool find_intersection(const Coord &p1, const Coord &p2, 
// 			 const Coord &dp,
// 			 PixelBdyIntersection &) const;

  inline Coord start_pt() const {
    if (horizontal)
      return Coord(fp_start, fp_level);
    return Coord(fp_level, fp_start);
  };

  inline Coord end_pt() const {
    if (horizontal) 
      return Coord(fp_end, fp_level);
    return Coord(fp_level, fp_end);
  };

  friend class PixelSetBoundary;
  friend class PixelBdyLoop;
  friend std::ostream& operator<<(std::ostream &, const PixelBdySegment&);
};

std::ostream& operator<<(std::ostream &, const PixelBdySegment&);

class PixelBdyLoop {
private:
  std::vector<PixelBdySegment> loop;
  CRectangle *bounds;		// computed by set_floats
public:
  PixelBdyLoop() : bounds(0) {}
  ~PixelBdyLoop();
  void add_segment(const PixelBdySegment&);
  void clean();
  void set_floats(const Coord&);
  const CRectangle &bbox() const { return *bounds; }
  const std::vector<PixelBdySegment> &segments() const { return loop; }
  friend std::ostream& operator<<(std::ostream&, const PixelBdyLoop&);
  friend class PixelSetBoundary; // for debugging
};

std::ostream& operator<<(std::ostream&, const PixelBdyLoop&);

typedef std::map<PixelBdySegment, int> SegMap;
typedef std::multimap<ICoord, PixelBdySegment> CoordMap;

// Pixel set boundary knows its microstructure.  The way this works
// is, you create it with a microstructure, then put in all the pixels
// in the pixel set for which you want this to be the boundary, then
// call the "find_boundary" method, which finds all the loops and
// assigns them to the "loopset" member.
class PixelSetBoundary {
private:
  SegMap segments;
  const CMicrostructure* microstructure;
  Coord ms_delta;
  std::vector<PixelBdyLoop*> loopset;
  PixelBdyLoop *find_loop(CoordMap&);
public:
  PixelSetBoundary(const CMicrostructure*);
  ~PixelSetBoundary();
  void add_pixel(const ICoord&);
  void find_boundary();
  const std::vector<PixelBdyLoop*> &get_loops() const { return loopset; }
  friend std::ostream& operator<<(std::ostream &, const PixelSetBoundary&);
};


// For debugging....
std::ostream& operator<<(std::ostream &, const PixelSetBoundary &);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#else //  DIM==3

// Quad is a quadrilateral piece of a VoxelSet boundary.  It must lie
// in a coordinate plane, so we keep track of which plane (norm_dir),
// the offset of that plane (height) and the 2d coordinates of the
// corners in that plane (coords). Everything is described in voxel
// units, so the components are all integers.

// TODO 3.1: Quad is a bad name.  Call it VoxelBdyQuad, or something.

class Quad {
private:
// #ifdef DEBUG
//   static std::set<const Quad*> allQuads;
// public:
//   static bool validQuad(const Quad*);
// #endif // DEBUG
public:
  Quad();
  ~Quad();
  int coords[4][2];
  // norm_dir is the index of the coordinate of the direction of the
  // normal.  Ie, norm_dir=2 means this Quad lies in an xy plane.
  int norm_dir;
  int norm;	// just gives the sign of the normal
  int area;
  int height; // gives the value of norm_dir coordinate;
};

std::ostream &operator<<(std::ostream&, const Quad&);

typedef std::vector<Quad*> QuadVector;

// PlanesOfQuads maps an offset (height) to a list of Quads at that
// height.  A VoxelSetBoundary has a PlanesOfQuads for each direction.
// The Quads in each PlanesOfQuads have normals in that direction.
typedef std::map<int, QuadVector*> PlanesOfQuads;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class VoxelSetBoundary {
private:
  PlanesOfQuads quads[3];	// one for each direction
  // for convenience in finding the faces of voxels
  static const ICoord dirs[6];
  static const ICoord faces[3][4];

public:
  VoxelSetBoundary() {}
  ~VoxelSetBoundary();
  const PlanesOfQuads& getQuads(int i) const { return quads[i]; }
  void add_face(const ICoord&, int, int);

  // this gives the indices for quads stored in 2D
  static const short proj_dirs[3][2];
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

enum IntersectionCategory {
  UNCATEGORIZED_INTERSECTION=0,
  // mnemonic: one enters before one exits
  ENTRANCE_INTERSECTION=1,
  EXIT_INTERSECTION=2,
  GRAZE_INTERSECTION=3 // graze = exit + entrance
};

class IntersectionType {
public:
  IntersectionType() : entrances(0), exits(0) {}
  unsigned short entrances;
  unsigned short exits;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// just a container class so we can put the location and the type in a map
class VoxelBdyIntersection {
private:
  //std::map<unsigned short, IntersectionType> types;
  IntersectionType types[4];

public:
  Coord location;

  // TODO: Why not use Coord instead of double x, y, z?

  VoxelBdyIntersection(double x, double y, double z, unsigned short f0, 
		       unsigned short f1) 
  {
    location = Coord(x,y,z);
    IntersectionType temp;
    assert(0 <= f0 && f0 < 4);
    assert(0 <= f1 && f1 < 4);
    types[f0] = types[f1] = temp;
  }  
  VoxelBdyIntersection(double x, double y, double z, unsigned short f0,
		       unsigned short f1, unsigned short f2) 
  {
    assert(0 <= f0 && f0 < 4);
    assert(0 <= f1 && f1 < 4);
    assert(0 <= f2 && f2 < 4);
    location = Coord(x,y,z);
    IntersectionType temp;
    types[f0] = types[f1] = types[f2] = temp;
  }
  IntersectionCategory getType(unsigned short face) { 
    unsigned short x = (types[face].entrances*ENTRANCE_INTERSECTION +
	    types[face].exits*EXIT_INTERSECTION) % GRAZE_INTERSECTION;
    return (IntersectionCategory) x;
  }  
  void addEntrance(unsigned short face) {
    ++types[face].entrances;
  }
  void addExit(unsigned short face) {
    ++types[face].exits;
  }
  void addType(unsigned short face, IntersectionCategory type) {
    if(type == ENTRANCE_INTERSECTION)
      addEntrance(face);
    if(type == EXIT_INTERSECTION)
      addExit(face);
  }
  // void setType(unsigned short face, IntersectionCategory type) { 
  //   IntersectionType temp;
  //   types[face] = temp;
  //   addType(face, type);
  // }
  void combine(unsigned short face, VoxelBdyIntersection &other) {
    types[face].entrances += other.types[face].entrances;
    types[face].exits += other.types[face].exits;
    other.types[face].entrances = 0;
    other.types[face].exits = 0;
  }
};				// end VoxelBdyIntersection



#endif	// DIM==3


#endif // PIXELSETBOUNDARY_H
