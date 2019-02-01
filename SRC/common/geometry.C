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
#include "common/coord.h"
#include "common/geometry.h"
#include "common/cprism_i.h"

void CRectangle::expand(double howmuch) {
  double mid = 0.5*(lowleft[0] + upright[0]);
  double size = 0.5*(upright[0] - lowleft[0])*(1 + howmuch);
  lowleft[0] = mid - size;
  upright[0] = mid + size;
  mid = 0.5*(lowleft[1] + upright[1]);
  size = 0.5*(upright[1] - lowleft[1])*(1 + howmuch);
  lowleft[1] = mid - size;
  upright[1] = mid + size;
  size_ = upright - lowleft;
}

std::ostream& operator<<(std::ostream &os, const CRectangle &rect) {
  os << "CRectangle(" << rect.lowleft << ", " << rect.upright << ")";
  return os;
}

std::ostream& operator<<(std::ostream &os, const ICRectangle &rect) {
  os << "ICRectangle(" << rect.lowleft << ", " << rect.upright << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double triangleArea(const Coord &p1, const Coord &p2, const Coord &p3) {
  // Copied from vtkTriangle::TriangleArea, with added consts, and
  // using Coord instead of double[3].
  double a = norm2(p1 - p2);
  double b = norm2(p2 - p3);
  double c = norm2(p3 - p1);
  return (0.25 * sqrt(fabs(4.*a*c - (a-b+c)*(a-b+c))));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

COrientedPlane COrientedPlane::reversed() const {
  return COrientedPlane(-normal, -offset);
}

double COrientedPlane::distance(const Coord3D &x) const {
  return dot(x, normal) - offset;
}

std::ostream &operator<<(std::ostream &os, const COrientedPlane &plane) {
  return os << "COrientedPlane(" << plane.normal << ", " << plane.offset
	    << ")";
}
