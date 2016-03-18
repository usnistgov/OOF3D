// -*- C++ -*-
// $RCSfile: tetintersection.h,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2015/01/22 20:35:15 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef TETINTERSECTION_H
#define TETINTERSECTION_H

#include <oofconfig.h>

#include "common/coord.h"
#include "common/pixelsetboundary.h"

#include <vector>
#include <set>

// Special utility class for pixel boundary intersections, so we can
// keep track of "incoming" versus "outgoing" intersections.  Incoming
// and outgoing are intended to be used with respect to elements (or
// element cross sections in 3D).  entry==true means that the pixel
// boundary enters the element at this intersection, and entry==false
// means that it exits the element at this intersection.

class PixelBdyIntersection {
public:
  const Coord2D location2D;
  const Coord3D location3D;
  const unsigned int node_index; // TODO: Bad name!  Change to seg_index?
  const unsigned int face;
  const double fraction; 
  const bool entry;

  PixelBdyIntersection(const Coord2D &loc2D, const Coord3D &loc3D,
		       unsigned int node, unsigned int face,
		       double frac, bool entry)
    : location2D(loc2D),
      location3D(loc3D),
      node_index(node),
      face(face),
      fraction(frac),
      entry(entry) 
  {}
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// TetPlaneIntersectionPoint stores the 2D intersection point of a tet
// edge and a plane, and the 3D coords of the endpoints of the edge,
// and the indices (in the local tetrahedron's list of nodes) of the
// nodes at the endpoints of the edge.

class TetPlaneIntersectionPoint : public Coord2D {
private:
  double t_;		    // interection = (1-t)*node0 + t*node1
  unsigned int edge_;	    // tet edge number, in vtk ordering scheme
public:
  TetPlaneIntersectionPoint(const Coord2D &pt, double t, unsigned int edge)
    : Coord2D(pt),
      t_(t),
      edge_(edge)
  {}
  double t() const { return t_; }
  unsigned int edge() const { return edge_; }
  int node0() const;
  int node1() const;
  unsigned int sharedFace(const TetPlaneIntersectionPoint&) const;
  bool operator<(const TetPlaneIntersectionPoint&) const;
};

std::ostream &operator<<(std::ostream&, const TetPlaneIntersectionPoint&);

std::vector<TetPlaneIntersectionPoint> findTetPlaneIntersectionPoints(
			      const std::vector<Coord>&, unsigned int, int);

unsigned int faceIndex(const TetPlaneIntersectionPoint&,
		       const TetPlaneIntersectionPoint&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void findPixelPlaneFacets(const VoxelSetBoundary&,
			  const std::vector<Coord>&,
			  FacetMap2D&);

double tetIntersectionVolume(const VoxelSetBoundary&,
			     const std::vector<Coord3D> &epts,
			     const FacetMap2D &facets,
			     unsigned int category);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Facet corner where a face of the tetrahedron intersects a plane of
// voxels.

class FaceFacetCorner : public PixelPlaneFacetCorner {
public:
  FaceFacetCorner(const Coord3D &loc, unsigned int f, const PixelPlane &pp)
    : PixelPlaneFacetCorner(pp),
      location(loc), face(f)
  {}
  const Coord3D location;
  const unsigned int face;
  virtual Coord2D position2D() const;
  virtual Coord3D position3D() const { return location; }
};

// Facet corner where an edge of the tetrahedron intersects a plane of
// voxels.  It also stores a reference to the
// TetPlaneIntersectionPoint that gave rise to the corner. Usually,
// multiple EdgeFacetCorners are created for each
// TetPlaneIntersectionPoint, one for each face that that shares the
// edge.  EdgeFacetCorner should *not* redefine position2D to return
// its TetPlaneIntersectionPoint's location, because position2D() may
// be called for a different PixelPlane.

class EdgeFacetCorner : public FaceFacetCorner {
private:
  const TetPlaneIntersectionPoint &tpip;
public:
  // TODO: Since loc can be computed from tpip and pp, it doesn't need
  // to be an explicit argument to the constructor.
  EdgeFacetCorner(const Coord3D &loc, unsigned int face,
		  const TetPlaneIntersectionPoint &tpip,
		  const PixelPlane &pp)
    : FaceFacetCorner(loc, face, pp),
      tpip(tpip)
  {}
  unsigned int edge() const { return tpip.edge(); }
  double edgePosition() const { return tpip.t(); }
};


#endif // TETINTERSECTION_H
