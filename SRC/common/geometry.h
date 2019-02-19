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

// Simple geometrical objects defined in terms of Coords.

#ifndef GEOMETRY_H
#define GEOMETRY_H

// The geometrical objects defined here are stored in C++, unlike
// those defined in IO/primitives.py, which are stored in Python.  Use
// whichever is more efficient in any given context.

#include "common/coord.h"
#include "common/ooferror.h"
#include <iostream>
#include <limits>
#include <vector>
#include <math.h>

#define min_(a,b) ((a) < (b)? (a) : (b))
#define max_(a,b) ((a) > (b)? (a) : (b))

// CTYPE is the type of the corner (Coord, ICoord, etc)
// VTYPE is the type of a coordinate component (double, int, etc)

template <class VTYPE, class CTYPE>
class CPolygon {
public:
  virtual ~CPolygon() {}
  virtual bool contains(const CTYPE&) const = 0;
  virtual int ncorners() const = 0;
  virtual CTYPE operator[](int) const = 0; // returns a corner
  virtual VTYPE area() const = 0;
};

template <class VTYPE, class CTYPE>
std::ostream &operator<<(std::ostream &os, const CPolygon<VTYPE, CTYPE> &poly) {
  os << "CPolygon:";
  for(int i=0; i<poly.ncorners(); i++)
    os << " " << poly[i];
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO MER: In 3D, do we really need separate CRectangle_ and
// CRectangularPrism_ classes?  Should everything that's a CRectangle_
// in 2D become a CRectangularPrism_ in 3D?  Then we could have just
// one class with "#if DIM"s in it and eliminate some "#if DIM"s
// elsewhere.

template <class VTYPE, class CTYPE>
class CRectangle_ : public CPolygon<VTYPE, CTYPE> {
protected:
  CTYPE upright;
  CTYPE lowleft;
  CTYPE size_;
public:
  CRectangle_() {}
  CRectangle_(const CTYPE &a, const CTYPE &b);
  virtual ~CRectangle_() {}
  inline const CTYPE &lowerleft() const { return lowleft; }
  inline const CTYPE &upperright() const { return upright; }
  void swallow(const CTYPE &pt) {
    if(upright[0] < pt[0]) upright[0] = pt[0];
    if(upright[1] < pt[1]) upright[1] = pt[1];
    if(lowleft[0] > pt[0]) lowleft[0] = pt[0];
    if(lowleft[1] > pt[1]) lowleft[1] = pt[1];
    size_ = upright - lowleft;
  }
  void swallow(const CRectangle_<VTYPE, CTYPE> &r) {
    swallow(r.upright);
    swallow(r.lowleft);
  }
  inline VTYPE xmin() const { return lowleft[0]; }
  inline VTYPE xmax() const { return upright[0]; }
  inline VTYPE ymin() const { return lowleft[1]; }
  inline VTYPE ymax() const { return upright[1]; }
  inline VTYPE height() const { return upright[1] - lowleft[1]; }
  inline VTYPE width() const { return upright[0] - lowleft[0]; }
  inline virtual VTYPE area() const { return width()*height(); }
  inline const CTYPE &size() const { return size_; }
  bool contains(const CTYPE &point) const {
    if(point[0] < xmin() || point[0] >= xmax()) return false;
    if(point[1] < ymin() || point[1] >= ymax()) return false;
    return true;
  }
  bool containsInclusive(const CTYPE &point) const {
    if(point[0] < xmin() || point[0] > xmax()) return false;
    if(point[1] < ymin() || point[1] > ymax()) return false;
    return true;
  }
  template <class VTYPE2, class CTYPE2>
  bool intersects(const CRectangle_<VTYPE2, CTYPE2> &other) const {
    if(upright[0] < other.lowleft[0]) return false;
    if(upright[1] < other.lowleft[1]) return false;
    if(lowleft[0] > other.upright[0]) return false;
    if(lowleft[1] > other.upright[1]) return false;
    return true;
  }
  template <class VTYPE2, class CTYPE2>
  bool intersects_fuzzy(const CRectangle_<VTYPE2, CTYPE2> &other, double fuzz)
    const
  {
    if(upright[0] < other.lowleft[0] - fuzz) return false;
    if(upright[1] < other.lowleft[1] - fuzz) return false;
    if(lowleft[0] > other.upright[0] + fuzz) return false;
    if(lowleft[1] > other.upright[1] + fuzz) return false;
    return true;
  }
  template <class VTYPE2, class CTYPE2>
  bool intersects_open(const CRectangle_<VTYPE2, CTYPE2> &other) const {
    if(upright[0] <= other.lowleft[0]) return false;
    if(upright[1] <= other.lowleft[1]) return false;
    if(lowleft[0] >= other.upright[0]) return false;
    if(lowleft[1] >= other.upright[1]) return false;
    return true;
  }
  virtual int ncorners() const { return 4; }
  virtual CTYPE operator[](int i) const {
    switch(i) {
    case 0:
      return lowleft;
    case 1:
      return CTYPE(upright[0], lowleft[1]);
    case 2:
      return upright;
    case 3:
      return CTYPE(lowleft[0], upright[1]);
    };
    throw ErrBadIndex(i, __FILE__, __LINE__);
  }
  // 
  void restrict(const CRectangle_<VTYPE, CTYPE> &limits) {
    if(limits.xmin() > lowleft[0])
      lowleft[0] = min_(upright[0], limits.xmin());
    if(limits.xmax() < upright[0])
      upright[0] = max_(lowleft[0], limits.xmax());
    if(limits.ymin() > lowleft[1])
      lowleft[1] = min_(upright[1], limits.ymin());
    if(limits.ymax() < upright[1])
      upright[1] = max_(lowleft[1], limits.ymax());
    size_ = upright - lowleft;
  }

  virtual std::ostream &print(std::ostream&) const = 0;

  // To allow intersections to be computed with other types of
  // rectangles, make all rectangles friends.
  template <class VTYPE2, class CTYPE2> friend class CRectangle_;
};				// end CRectangle_

template <class VTYPE, class CTYPE>
CRectangle_<VTYPE, CTYPE>::CRectangle_(const CTYPE &a, const CTYPE &b) {
  if(a[0] < b[0]) {
    upright[0] = b[0];
    lowleft[0] = a[0];
  }
  else {
    upright[0] = a[0];
    lowleft[0] = b[0];
  }
  if(a[1] < b[1]) {
    upright[1] = b[1];
    lowleft[1] = a[1];
  }
  else {
    upright[1] = a[1];
    lowleft[1] = b[1];
  }
  size_ = upright - lowleft;
}

class CRectangle: public CRectangle_<double, Coord2D> {
public:
  CRectangle(const Coord2D &a, const Coord2D &b)
    : CRectangle_<double, Coord2D>(a,b)
  {}
  friend std::ostream& operator<<(std::ostream&, const CRectangle&);
  virtual std::ostream &print(std::ostream &os) const {
    return os << *this;
  }
  void expand(double howmuch);
};

std::ostream& operator<<(std::ostream&, const CRectangle&);

class ICRectangle : public CRectangle_<int, ICoord2D> {
public:
  ICRectangle() {}
  ICRectangle(const ICoord2D &a, const ICoord2D &b)
    : CRectangle_<int, ICoord2D>(a,b)
  {}
  friend std::ostream& operator<<(std::ostream&, const ICRectangle&);
  virtual std::ostream &print(std::ostream &os) const {
    return os << *this;
  }    
};

std::ostream& operator<<(std::ostream&, const ICRectangle&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double triangleArea(const Coord&, const Coord&, const Coord&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// To make the VSB code distributable independently from the rest of
// OOF3D, it needed its own oriented plane class.  So COrientedPlane,
// which used to be defined here, was turned into a template, renamed
// to VSBPlane, and moved to VSB/cplane.h.  Here we just create an
// instance of the template and call it COrientedPlane.

#include "common/VSB/cplane.h"
typedef VSBPlane<Coord3D> COrientedPlane;

std::ostream &operator<<(std::ostream&, const COrientedPlane&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#undef min_
#undef max_

#endif	// GEOMETRY_H
