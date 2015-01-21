// -*- C++ -*-
// $RCSfile: mastercoord.h,v $
// $Revision: 1.9.10.9 $
// $Author: langer $
// $Date: 2014/12/14 22:49:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MASTERCOORD_H		/* We also take Discoover and Viisa */
#define MASTERCOORD_H

#include <oofconfig.h>

class MasterCoord;
class MasterPosition;

#include "common/coord_i.h"
#include "engine/indextypes.h"
#include <iostream>

class ElementBase;
class ShapeFunction;

// The Coord and MasterCoord classes used to be both derived from the
// same template, so that they could share the same code but still be
// distinct classes. That doesn't work now that Coord is derived from
// Position, but MasterCoord isn't.  So now the classes have
// separate but equal definitions.


// The MasterPosition base class allows MasterCoord and GaussPoint to
// be passed to the same functions.

class MasterPosition {
public:
  virtual ~MasterPosition() {}
  virtual MasterCoord mastercoord() const = 0;
  // Shape functions and their derivatives wrt master coordinates are
  // evaluated through these double-dispatch functions.
  virtual double shapefunction(const ShapeFunction&, ShapeFunctionIndex)
    const = 0;
  virtual double mdshapefunction(const ShapeFunction&, ShapeFunctionIndex,
				SpaceIndex) const = 0;
  virtual double dshapefunction(const ElementBase*, const ShapeFunction&,
				ShapeFunctionIndex, SpaceIndex) const = 0;
  virtual std::ostream &print(std::ostream&) const = 0;
};

std::ostream &operator<<(std::ostream&, const MasterPosition&);

class MasterCoord : public MasterPosition {
protected:
  double x[DIM];
public:
#if DIM == 2
  MasterCoord() { x[0] = x[1] = 0; }
  MasterCoord(double x1, double x2) { x[0] = x1; x[1] = x2; }
  MasterCoord(const MasterCoord &c) { x[0] = c[0]; x[1] = c[1]; }
#elif DIM == 3
  MasterCoord() { x[0] = x[1] = x[2] = 0; }
  MasterCoord(double x1, double x2, double x3) {
    x[0] = x1; x[1] = x2; x[2] = x3;
  }
  MasterCoord(const MasterCoord &c) { x[0] = c[0]; x[1] = c[1]; x[2] = c[2]; }
  MasterCoord(const Coord &c);
#endif
  virtual MasterCoord mastercoord() const { return *this; }
  //double operator()(int i) const { return x[i]; }
  //double &operator()(int i) { return x[i]; }
  MasterCoord &operator+=(const MasterCoord &c) {
    x[0] += c[0];
    x[1] += c[1];
#if DIM == 3
    x[2] += c[2];
#endif	// DIM == 3
    return *this;
  }
  MasterCoord &operator*=(double y) {
    x[0] *= y;
    x[1] *= y;
#if DIM == 3
    x[2] *= y;
#endif	// DIM == 3
    return *this;
  }
  
  inline double operator[](int i) const {
#ifdef DEBUG
    if(i >= DIM)
      throw ErrBoundsError("MasterCoord: Index too large."); 
    else if(i < 0)
      throw ErrBoundsError("MasterCoord: Index too small.");
    else
#endif // DEBUG
      return x[i];
  }
  
  inline double &operator[](int i) {
#ifdef DEBUG
   if(i >= DIM)
     throw ErrBoundsError("MasterCoord: Index too large."); 
   else if(i < 0)
     throw ErrBoundsError("MasterCoord: Index too small.");
   else
#endif // DEBUG
   return x[i];
  }
  
  virtual double shapefunction(const ShapeFunction&, ShapeFunctionIndex) const;
  virtual double mdshapefunction(const ShapeFunction&, ShapeFunctionIndex,
				SpaceIndex) const;
  virtual double dshapefunction(const ElementBase*, const ShapeFunction&,
				ShapeFunctionIndex, SpaceIndex) const;
  virtual std::ostream &print(std::ostream&) const;
  friend bool operator==(const MasterCoord&, const MasterCoord&);
};

std::ostream &operator<<(std::ostream&, const MasterCoord&);

std::istream &operator>>(std::istream&, MasterCoord&);

inline MasterCoord operator+(const MasterCoord &a, const MasterCoord &b) {
  MasterCoord result(a);
  result += b;
  return result;
}

inline MasterCoord operator-(const MasterCoord &a, const MasterCoord &b) {
#if DIM == 2
  return MasterCoord(a[0]-b[0], a[1]-b[1]);
#elif DIM == 3
  return MasterCoord(a[0]-b[0], a[1]-b[1], a[2]-b[2]);
#endif
}

inline MasterCoord operator*(const MasterCoord &a, double x) {
  MasterCoord b(a);
  b *= x;
  return b;
}

inline MasterCoord operator*(double x, const MasterCoord &a) {
  MasterCoord b(a);
  b *= x;
  return b;
}

inline MasterCoord operator/(const MasterCoord &a, double x) {
  MasterCoord b(a);
  b *= (1/x);
  return b;
}

#if DIM == 2
inline double cross(const MasterCoord &c1, const MasterCoord &c2)
{
  return c1[0]*c2[1] - c1[1]*c2[0];
}

inline double operator%(const MasterCoord &c1, const MasterCoord &c2)
{
  return(cross(c1,c2));
}
#endif	// DIM == 2

inline bool operator==(const MasterCoord &a, const MasterCoord &b) {
#if DIM == 2
  return a[0] == b[0] && a[1] == b[1];
#elif DIM == 3
  return a[0] == b[0] && a[1] == b[1] && a[2] == b[2];
#endif	// DIM == 3
}

#if DIM == 2
inline bool operator<(const MasterCoord &a, const MasterCoord &b) {
  return (a[0] < b[0]) || (a[0] == b[0] && a[1] < b[1]);
}
#endif	// DIM == 2

inline double dot(const MasterCoord &c1, const MasterCoord &c2) {
#if DIM == 2
  return c1[0]*c2[0] + c1[1]*c2[1];
#elif DIM == 3
  return c1[0]*c2[0] + c1[1]*c2[1] + c1[2]*c2[2];
#endif	// DIM == 3
}

inline double norm2(const MasterCoord &c) {
  return dot(c, c);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Factory functions for returning the right kind of MasterCoord
// independent of DIM.  These may be changed to return different
// MasterCoord subclasses at some point.  For now, they just allow the
// extra-dimensional arguments to be omitted.

inline MasterCoord masterCoord2D(double x, double y) {
#if DIM==2
  return MasterCoord(x, y);
#else
  return MasterCoord(x, y, 0.);
#endif
}

inline MasterCoord masterCoord1D(double x) {
#if DIM==2
  return MasterCoord(x, 0.);
#else
  return MasterCoord(x, 0., 0.);
#endif
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM == 2

// TODO: Eliminate MasterEndPoint.

// MasterEndPoint marks the ends of contours. 'start' indicates which
// end it is.  The default constructor is never actually used, but
// without it it's not possible to construct a
// std::vector<MasterEndPoint>.

class MasterEndPoint {
public:
  MasterEndPoint(const MasterCoord *mc, bool start) : mc(mc), start(start) {}
  MasterEndPoint() : mc[0], start(false) {}
  double operator()(int i) const { return (*mc)[i]; }
  const MasterCoord *mc;
  bool start;
};

std::ostream &operator<<(std::ostream &os, const MasterEndPoint&);

typedef bool (*MasterEndPointComparator)(const MasterEndPoint&,
					 const MasterEndPoint&);

// TODO MER: CCurve may be obsolete.  Delete it if it is.  Move this
// typedef to a better location if it's not.

#include <deque>
typedef std::deque<const MasterCoord*> CCurve;

#endif	// DIM == 2

#endif // MASTERCOORD_H
