// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/pixelsetboundary.h"
#include "engine/barycentric.h"
#include "engine/cskeletonelement.h"
#include <vtkTetra.h>

// TODO: vtkTetra::BarycentricCoords() doesn't take advantage of the
// fact that the same matrix is used to find all coords for an
// element.  We need to save the LU decomposition and reuse it.  We
// should have a HomogeneityTet class that stores the LU
// decomposition, the TetPlaneIntersectionCache, the BaryCoordCache,
// and the FacetCornerList.

// NOTE on arithmetic with barycentric coordinates: barycentric
// coordinates aren't vectors.  They can't be simply added component
// by component, because the sum of the components has to add to 1.
// However, if they are added, the real space coordinate computed from
// the unnormalized result will still be correct.  The way to
// normalize an unnormalized barycentric coordinate is to add
// (component-wise) an appropriate multiple of the barycentric
// coordinate of the origin.

BarycentricCoord::BarycentricCoord(const Coord3D &pt,
				   const std::vector<Coord3D> &epts)
  : bcoord(4, 0.0)
{
  int ok = vtkTetra::BarycentricCoords(const_cast<Coord3D&>(pt).xpointer(),
				       const_cast<double*>(epts[0].xpointer()),
				       const_cast<double*>(epts[1].xpointer()),
				       const_cast<double*>(epts[2].xpointer()),
				       const_cast<double*>(epts[3].xpointer()),
				       &bcoord[0]);
  if(!ok)
    throw ErrProgrammingError("Illegal element!", __FILE__, __LINE__);
}

BarycentricCoord::BarycentricCoord(double b0, double b1, double b2, double b3)
  : bcoord(4, 0.0)
{
  bcoord[0] = b0;
  bcoord[1] = b1;
  bcoord[2] = b2;
  bcoord[3] = b3;
}

BarycentricCoord::BarycentricCoord(const BarycentricCoord &other)
  : bcoord(other.bcoord)
{}

BarycentricCoord::BarycentricCoord(BarycentricCoord &&other) {
  std::vector<double> temp = std::move(bcoord);
  bcoord = std::move(other.bcoord);
  other.bcoord = std::move(temp);
}

BarycentricCoord &BarycentricCoord::operator=(const BarycentricCoord &other) {
  bcoord = other.bcoord;
  return *this;
}

bool BarycentricCoord::interior(unsigned int onFace) const {
  // Interiority can be determined in two contexts: face interiority
  // and tet interiority.  If onFace is not NONE, we know that a point
  // is in a plane coincident with a face of a tet, and we want to
  // find out if the point is inside the face of the tet. On the other
  // hand, if onFace is NONE, we just want to know if the point is
  // inside the tet.  This distinction is only important because we
  // take points *on* the boundary to be outside, which would mean
  // that all points on face facets would be outside if we didn't
  // treat faces differently.
  if(onFace == NONE) {
    for(unsigned int i=0; i<4; i++)
      if(bcoord[i] <= 0)
	return false;
  }
  else {
    unsigned int oppNode = CSkeletonElement::oppNode[onFace];
    for(unsigned int i=0; i<4; i++) {
      if(i != oppNode)
	if(bcoord[i] <= 0)
	  return false;
    }
  }
  return true;
}

bool BarycentricCoord::interior() const {
  return interior(NONE);
}

bool BarycentricCoord::onEdge() const {
  unsigned int n = 0;
  for(unsigned int i=0; i<4; i++)
    if(bcoord[i] == 0.0)
      n++;
  return n >= 2;
}

Coord3D BarycentricCoord::position3D(const std::vector<Coord3D> &epts) const {
  Coord3D x(0.0, 0.0, 0.0);
  for(unsigned int i=0; i<4; i++)
    x += bcoord[i]*epts[i];
  return x;
}

// Fix roundoff error in a coordinate that is (somehow) known to be on
// the surface of a tet but appears to be just outside.

void BarycentricCoord::repair() {
  for(unsigned int i=0; i<4; i++) {
    if(bcoord[i] < 0)
      bcoord[i] = 0.0;
  }
}

// // Barycentric coordinates can't be simply added component-wise or
// // scaled, because the result wouldn't be normalized correctly.
// // However, the weighted average of two points is simple.

// BarycentricCoord averageBary(const BarycentricCoord &b0,
// 			     const BarycentricCoord &b1,
// 			     double weight)
// {
//   BarycentricCoord avg;
//   for(unsigned int i=0; i<4; i++)
//     avg[i] = (1-weight)*b0[i] + weight*b1[i];
//   return avg;
// }

// // When two nearly equal points are merged into one, preserve
// // topological information by ensuring that components that are zero
// // in either of the original points are also zero in the result.  The
// // result will not be normalized quite correctly, but if the original
// // points only differ by round-off, it won't matter.

// BarycentricCoord mergeBary(const BarycentricCoord &b0,
// 			   const BarycentricCoord &b1)
// {
//   BarycentricCoord result;
//   for(unsigned int i=0; i<4; i++) {
//     if(b0[i] == 0.0 || b1[i] == 0.0)
//       result[i] = 0.0;
//     else
//       result[i] = 0.5*(b0[i] + b1[i]);
//   }
//   return result;
// }

bool BarycentricCoord::operator<(const BarycentricCoord &other) const {
  for(unsigned int i=0; i<4; i++) {
    if(bcoord[i] < other.bcoord[i])
      return true;
    if(bcoord[i] > other.bcoord[i])
      return false;
  }
  return false;
}

bool BarycentricCoord::operator==(const BarycentricCoord &other) const {
  for(unsigned int i=0; i<4; i++)
    if(bcoord[i] != other.bcoord[i])
      return false;
  return true;
}

std::ostream &operator<<(std::ostream &os, const BarycentricCoord &bc) {
  int prec = os.precision();
  os << std::setprecision(20);
  os << "{" << bc[0] << ", " << bc[1] << ", " << bc[2] << ", " << bc[3] << "}";
  os << std::setprecision(prec);
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// // TODO: Should these be HomogeneityTet methods?  YES

// BarycentricCoord &getBarycentricCoord(
// 			     const Coord3D &pt,
// 			     const std::vector<Coord3D> &epts,
// 			     const std::vector<const PixelPlane*> &facePlanes,
// 			     BaryCoordCache &cache)
// {
//   // See if this coordinate has already been computed.
//   BaryCoordCache::iterator it=cache.find(pt);
//   if(it != cache.end()) {
//     return (*it).second;
//   }
//   // Compute a new coordinate.
//   BarycentricCoord b(pt, epts);
//   // If a face of the element is exactly on a pixel plane, and the
//   // point is on that plane, make sure that the corresponding
//   // barycentric component is exactly zero.
//   for(unsigned int f=0; f<NUM_TET_FACES; f++) {
//     if(facePlanes[f] != NULL) {
//       if(facePlanes[f]->contains(pt)) {
// 	b[CSkeletonElement::oppNode[f]] = 0.0;
//       }
//     }
//   }
//   // Insert the new barycentric coord into the cache, and return a
//   // reference to it.
//   std::pair<BaryCoordCache::iterator, bool> insert =
//     cache.insert(std::pair<Coord3D, BarycentricCoord>(pt, b));
//   return (*insert.first).second;
// }

// BarycentricCoord &getBarycentricCoord(
// 			    const ICoord3D &ipt,
// 			    const std::vector<Coord3D> &epts,
// 			    const std::vector<const PixelPlane*> &facePlanes,
// 			    BaryCoordCache &cache)
// {
//   Coord3D c(ipt[0], ipt[1], ipt[2]);
//   return getBarycentricCoord(c, epts, facePlanes, cache);
// }

// BarycentricCoord &getBarycentricCoord(
// 			     const ICoord2D &pt,
// 			     const PixelPlane &pixplane,
// 			     const std::vector<Coord3D> &epts,
// 			     const std::vector<const PixelPlane*> &facePlanes,
// 			     BaryCoordCache &cache)
// {
//   // TODO: Have a separate barycentric coord cache for ICoord3Ds?
//   ICoord3D x = pixplane.convert2Coord3D(pt);
//   Coord3D c(x[0], x[1], x[2]);
//   return getBarycentricCoord(c, epts, facePlanes, cache);
// }

// nodeBCoord returns the barycentric coordinates of a node of a tet.
const BarycentricCoord &nodeBCoord(unsigned int n) {
  static std::vector<BarycentricCoord> nodes({
      BarycentricCoord(1.,0.,0.,0.),
      BarycentricCoord(0.,1.,0.,0.),
      BarycentricCoord(0.,0.,1.,0.),
      BarycentricCoord(0.,0.,0.,1.)
	});
  assert(n < 4);
  return nodes[n];
	
  // BarycentricCoord b;		// all zeros
  // b[n] = 1.0;
  // return b;
}

