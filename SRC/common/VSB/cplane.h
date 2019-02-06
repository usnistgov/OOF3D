// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef VSBPLANE_H
#define VSBPLANE_H

template <class COORD>
class VSBPlane {
public:
  const COORD normal; // unit normal
  const double offset;		    // distance from origin to plane
				    // in normal direction
  VSBPlane(const COORD &norm, double d)
    : normal(norm), offset(d)
  {}
  VSBPlane(const COORD *norm, double d)
    : normal(*norm), offset(d)
  {}
  // Distance from arg to the plane. It's positive if the point is in
  // the +normal direction.
  double distance(const COORD &x) const {
    return dot(x, normal) - offset;
  }
  VSBPlane<COORD> reversed() const {
    return VSBPlane<COORD>(-normal, -offset);
  }
};

template <class COORD>
std::ostream &operator<<(std::ostream &os, const VSBPlane<COORD> &plane) {
  return os << "VSBPlane(" << plane.normal << ", " << plane.offset
	    << ")";
}

#endif // VSBPLANE_H
