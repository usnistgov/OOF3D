// -*- C++ -*-
// $RCSfile: coord.h,v $
// $Revision: 1.25.10.28 $
// $Author: langer $
// $Date: 2014/12/14 22:49:06 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef COORD_H
#define COORD_H

#include <oofconfig.h>

// Coord2D and Coord3D are the 2D and 3D coordinate classes.  Both are
// always defined, whatever the value of DIM.  Coord is defined to be
// Coord2D if DIM==2 and Coord3D if DIM==3.  If DIM==2, only Coord2D
// is derived from Position.

// The Coord and MasterCoord classes used to be both derived from the
// same template, so that they could share the same code but still be
// distinct classes. That doesn't work now that Coord is derived from
// Position, but MasterCoord isn't.  So now the classes have
// separate but equal definitions.

#include "engine/ooferror.h"
#include <iostream>

#include "common/coord_i.h"

// The Position base class allows simple objects like Coord and
// complex objects like GaussPoint to be passed to the same functions,
// if all they need to know is the position of the object.

class Position {
public:
  virtual ~Position () {}
  virtual Coord position() const = 0;
};

class Coord2D
#if DIM==2
  : public Position
#endif // DIM==2
{
public:
  typedef double ComponentType;
  double x[2];
  Coord2D() { x[0] = 0.0; x[1] = 0.0; }
  Coord2D(double x0, double y0) { x[0]=x0; x[1]=y0; }
  virtual ~Coord2D() {}

  inline Coord2D &operator+=(const Coord2D &c) {
    x[0]+=c[0]; x[1]+=c[1]; 
    return *this; 
  }
  inline Coord2D &operator-=(const Coord2D &c) { 
    x[0]-=c[0]; x[1]-=c[1]; 
    return *this; 
  }
  Coord2D &operator*=(double f) { x[0]*=f; x[1]*=f; return *this; }
  Coord2D &operator/=(double f) { x[0]/=f; x[1]/=f; return *this; }
  Coord2D(const Coord2D &c) {x[0] = c[0]; x[1] = c[1];}

  Coord2D &operator+=(const ICoord2D&);
  Coord2D &operator-=(const ICoord2D&);
#if DIM==2
  virtual Coord position() const { return *this; }
#endif

  Coord2D operator-() const;

  bool differFrom(const Coord2D&) const; // differ to within machine precision?
  
  double *xpointer() { return &x[0]; }
  const double *xpointer() const { return &x[0]; }
  operator double* () { return &x[0]; }
  operator const double* () const { return &x[0]; }
  
  inline double operator[](int i) const {
#ifdef DEBUG
   if(i >= 2)
     throw ErrBoundsError("Coord2D: Index too large."); 
   else if(i < 0)
     throw ErrBoundsError("Coord2D: Index too small.");
   else 
#endif // DEBUG
     return x[i];
  }
  
  inline double &operator[](int i) {
#ifdef DEBUG
   if(i >= 2)
     throw ErrBoundsError("Coord2D: Index too large."); 
   else if(i < 0)
     throw ErrBoundsError("Coord2D: Index too small.");
   else
#endif // DEBUG
     return x[i];
  }

  ICoord2D roundComponents() const;

  static const Coord2D origin;
};				       // end Coord2D

class Coord3D
#if DIM==3
  : public Position
#endif // DIM==3
{
public:
  typedef double ComponentType;
  double x[3];
  Coord3D() { x[0] = 0.0; x[1] = 0.0; x[2] = 0.0 ;}
  Coord3D(double x0, double y0, double z0) { x[0] = x0; x[1] = y0; x[2] = z0; }
  Coord3D(double *p) { x[0] = p[0]; x[1] = p[1]; x[2] = p[2]; }
  Coord3D(const Coord3D &c) { x[0] = c[0]; x[1] = c[1]; x[2] = c[2]; }
  virtual ~Coord3D() {}
  
  inline Coord3D &operator+=(const Coord3D &c) {
    x[0]+=c[0]; x[1]+=c[1]; x[2]+=c[2];
    return *this; 
  }
  inline Coord3D &operator-=(const Coord3D &c) {
    x[0]-=c[0]; x[1]-=c[1]; x[2]-=c[2];
    return *this; 
  }
  Coord3D &operator*=(double f) {
    x[0]*=f; x[1]*=f; x[2]*=f; 
    return *this; 
  }
  Coord3D &operator/=(double f) {
    x[0]/=f; x[1]/=f; x[2]/=f;
    return *this; 
  }

  Coord3D &operator+=(const ICoord3D&);
  Coord3D &operator-=(const ICoord3D&);

 #if DIM==3
  virtual Coord position() const { return *this; }
 #endif

  Coord3D operator-() const;

  bool differFrom(const Coord3D&) const; // differ to within machine precision?
  
  double *xpointer() { return &x[0]; }
  const double *xpointer() const { return &x[0]; }
  operator double* () { return &x[0]; }
  operator const double* () const { return &x[0]; }
  
  inline double operator[](int i) const {
#ifdef DEBUG
   if(i >= 3)
     throw ErrBoundsError("Coord3D: Index too large."); 
   else if(i < 0)
     throw ErrBoundsError("Coord3D: Index too small.");
   else 
#endif // DEBUG
     return x[i];
  }
  
  inline double &operator[](int i) {
#ifdef DEBUG
   if(i >= 3)
     throw ErrBoundsError("Coord3D: Index too large."); 
   else if(i < 0)
     throw ErrBoundsError("Coord3D: Index too small.");
   else
#endif // DEBUG
     return x[i];
  }

  ICoord3D roundComponents() const;

  static const Coord3D origin;
};				       // end Coord3D

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Coord2D operators

inline bool operator<(const Coord2D &a, const Coord2D &b) {
  if(a[0] < b[0]) return true;
  if(a[0] > b[0]) return false;
  if(a[1] < b[1]) return true;
  return false;
}

std::ostream &operator<<(std::ostream&, const Coord2D&);
// std::istream &operator>>(std::istream&, Coord2D&);

inline Coord2D operator+(const Coord2D &a, const Coord2D &b) {
  Coord2D result(a);
  result += b;
  return result;
}

inline Coord2D operator-(const Coord2D &a, const Coord2D &b) {
  Coord2D result(a);
  result -= b;
  return result;
}

inline Coord2D operator*(const Coord2D &a, double x) {
  Coord2D b(a);
  b *= x;
  return b;
}

inline Coord2D operator*(double x, const Coord2D &a) {
  Coord2D b(a);
  b *= x;
  return b;
}

inline Coord2D operator/(const Coord2D &a, double x) {
  Coord2D b(a);
  b /= x;
  return b;
}

inline Coord2D operator/(const Coord2D &a, const Coord2D &b) {
  Coord2D c(a);
  for(int i=0;i<DIM;i++) c[i] /= b[i];
  return c;
}

inline double cross(const Coord2D &c1, const Coord2D &c2)
{
  return c1[0]*c2[1] - c1[1]*c2[0];
}

inline bool operator==(const Coord2D &a, const Coord2D &b) {
  return a[0] == b[0] && a[1] == b[1];
}

inline bool operator!=(const Coord2D &a, const Coord2D &b) {
  return a[0] != b[0] || a[1] != b[1];
}

inline double dot(const Coord2D &c1, const Coord2D &c2) {
  return c1[0]*c2[0] + c1[1]*c2[1];
}

inline double operator%(const Coord2D &c1, const Coord2D &c2)
{
  return(cross(c1,c2));
}

inline double norm2(const Coord2D &c) {
  return dot(c, c);
}


// Coord3D operators

inline bool operator<(const Coord3D &a, const Coord3D &b) {
  if(a[0] < b[0]) return true;
  if(a[0] > b[0]) return false;
  if(a[1] < b[1]) return true;
  if(a[1] > b[1]) return false;
  if(a[2] < b[2]) return true;
  return false;
}

std::ostream &operator<<(std::ostream&, const Coord3D&);
// std::istream &operator>>(std::istream&, Coord3D&);

inline Coord3D operator+(const Coord3D &a, const Coord3D &b) {
  Coord3D result(a);
  result += b;
  return result;
}

inline Coord3D operator-(const Coord3D &a, const Coord3D &b) {
  Coord3D result(a);
  result -= b;
  return result;
}

inline Coord3D operator*(const Coord3D &a, double x) {
  Coord3D b(a);
  b *= x;
  return b;
}

inline Coord3D operator*(double x, const Coord3D &a) {
  Coord3D b(a);
  b *= x;
  return b;
}

inline Coord3D operator/(const Coord3D &a, double x) {
  Coord3D b(a);
  b /= x;
  return b;
}

inline Coord3D operator/(const Coord3D &a, const Coord3D &b) {
  Coord3D c(a);
  for(int i=0;i<DIM;i++) c[i] /= b[i];
  return c;
}

inline double dot(const Coord3D &c1, const Coord3D &c2) {
  return c1[0]*c2[0] + c1[1]*c2[1] + c1[2]*c2[2];
}

inline Coord3D cross(const Coord3D &c1, const Coord3D &c2) {
  Coord3D temp((c1[1]*c2[2]-c1[2]*c2[1]),
	     (c1[2]*c2[0]-c1[0]*c2[2]),
	     (c1[0]*c2[1]-c1[1]*c2[0]));
  return temp;
}

inline bool operator==(const Coord3D &a, const Coord3D &b) {
  return a[0] == b[0] && a[1] == b[1] && a[2] == b[2];
}

inline bool operator!=(const Coord3D &a, const Coord3D &b) {
  return a[0] != b[0] || a[1] != b[1] || a[2] != b[2];
}

inline Coord3D operator%(const Coord3D &c1, const Coord3D &c2) {
  return(cross(c1,c2));
}

inline double norm2(const Coord3D &c) {
  return dot(c, c);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Integer coordinates

class ICoord2D {
protected:
  int x[2];
public:
  typedef int ComponentType;

  virtual ~ICoord2D() {}

  ICoord2D() { x[0] = 0; x[1] = 0; }
  ICoord2D(int x0, int x1) { x[0] = x0; x[1] = x1; } 

  int *xpointer() { return &x[0]; }
  const int *xpointer() const { return &x[0]; }
  operator int* () { return &x[0]; }
  operator const int* () const { return &x[0]; }

  ICoord2D operator-() const;
  
  ICoord2D &operator+=(const ICoord2D &c) {
    for(int i=0; i<2; i++)
      x[i] += c[i];
    return *this;
  }
  ICoord2D &operator-=(const ICoord2D &c) {
    for(int i=0; i<2; i++)	
      x[i] -= c[i];
    return *this;
  }
  ICoord2D &operator*=(int y) {
    for(int i=0; i<2; i++)	
      x[i] *= y;
    return *this;
  }
  
  inline int operator[](int i) const {
#ifdef DEBUG
   if(i >= 2)
     throw ErrBoundsError("ICoord2D: Index too large."); 
   else if(i < 0)
     abort(); //throw ErrBoundsError("ICoord2D: Index too small.");
   else
#endif // DEBUG
     return x[i];
  }
  
  inline int &operator[](int i) {
#ifdef DEBUG
   if(i >= 2)
     throw ErrBoundsError("ICoord2D: Index too large."); 
   else if(i < 0)
     abort(); //throw ErrBoundsError("ICoord2D: Index too small.");
   else
#endif // DEBUG
     return x[i];
  }
  
  friend Coord2D operator*(const ICoord2D &a, double x);
  friend bool operator==(const ICoord2D&, const ICoord2D&);
  friend bool operator!=(const ICoord2D&, const ICoord2D&);
  friend bool operator!=(const ICoord2D &a, const Coord2D &b);
  friend int dot(const ICoord2D &c1, const ICoord2D &c2);
  friend double dot(const Coord2D &c1, const ICoord2D &c2);
  friend bool operator<(const ICoord2D &a, const ICoord2D &b);
  static const ICoord2D origin;
};				// end ICoord2D

class ICoord3D {
protected:
  int x[3];
public:
  typedef int ComponentType;

  virtual ~ICoord3D() {}

  ICoord3D() { x[0] = 0; x[1] = 0; x[2] = 0; }
  ICoord3D(int x0, int x1, int x2) { x[0] = x0; x[1] = x1; x[2] = x2; }

  int *xpointer() { return &x[0]; }
  const int *xpointer() const { return &x[0]; }
  operator int* () { return &x[0]; }
  operator const int* () const { return &x[0]; }

  ICoord3D operator-() const;
  
  ICoord3D &operator+=(const ICoord3D &c) {
    for(int i=0; i<3; i++)
      x[i] += c[i];
    return *this;
  }
  ICoord3D &operator-=(const ICoord3D &c) {
    for(int i=0; i<3; i++)	
      x[i] -= c[i];
    return *this;
  }
  ICoord3D &operator*=(int y) {
    for(int i=0; i<3; i++)	
      x[i] *= y;
    return *this;
  }
  
  inline int operator[](int i) const {
#ifdef DEBUG
   if(i >= 3)
     throw ErrBoundsError("ICoord3D: Index too large."); 
   else if(i < 0)
     abort(); //throw ErrBoundsError("ICoord3D: Index too small.");
   else
#endif // DEBUG
     return x[i];
  }
  
  inline int &operator[](int i) {
#ifdef DEBUG
   if(i >= 3)
     throw ErrBoundsError("ICoord3D: Index too large."); 
   else if(i < 0)
     abort(); //throw ErrBoundsError("ICoord3D: Index too small.");
   else
#endif // DEBUG
     return x[i];
  }
  
  friend Coord3D operator*(const ICoord3D &a, double x);
  friend bool operator==(const ICoord3D&, const ICoord3D&);
  friend bool operator!=(const ICoord3D&, const ICoord3D&);
  friend bool operator!=(const ICoord3D &a, const Coord3D &b);
  friend int dot(const ICoord3D &c1, const ICoord3D &c2);
  friend double dot(const Coord3D &c1, const ICoord3D &c2);
  friend bool operator<(const ICoord3D &a, const ICoord3D &b);
  static const ICoord3D origin;
};				// end ICoord3D

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ICoord2D operators

std::ostream &operator<<(std::ostream&, const ICoord2D&);
// std::istream &operator>>(std::istream&, ICoord2D&);

inline ICoord2D operator+(const ICoord2D &a, const ICoord2D &b) {
  ICoord2D result(a);
  result += b;
  return result;
}

inline ICoord2D operator-(const ICoord2D &a, const ICoord2D &b) {
  ICoord2D result(a);
  result -= b;
  return result;
}

inline Coord2D operator+(const Coord2D &a, const ICoord2D &b) {
  Coord2D result(a);
  result += b;
  return result;
}

inline Coord2D operator-(const Coord2D &a, const ICoord2D &b) {
  Coord2D result(a);
  result -= b;
  return result;
}

inline Coord2D operator+(const ICoord2D &b, const Coord2D &a) {
  Coord2D result(a);
  result += b;
  return result;
}

inline Coord2D operator-(const ICoord2D &b, const Coord2D &a) {
  Coord2D result(a);
  result -= b;
  return result;
}

inline ICoord2D operator*(const ICoord2D &a, int x) {
  ICoord2D b(a);
  b *= x;
  return b;
}

inline ICoord2D operator*(int x, const ICoord2D &a) {
  ICoord2D b(a);
  b *= x;
  return b;
}

inline Coord2D operator*(const ICoord2D &a, double x) {
  Coord2D b(a[0], a[1]);
  b *= x;
  return b;
}

inline bool operator==(const ICoord2D &a, const ICoord2D &b) {
  return a[0] == b[0] && a[1] == b[1];
}

inline bool operator!=(const ICoord2D &a, const ICoord2D &b) {
  return a[0] != b[0] || a[1] != b[1];
}

inline bool operator!=(const ICoord2D &a, const Coord2D &b) {
  return a[0] != b[0] || a[1] != b[1];
}

inline int dot(const ICoord2D &c1, const ICoord2D &c2) {
  int dotproduct = 0;
  for(int i=0; i<2; i++)	
    dotproduct += c1[i]*c2[i];
  return dotproduct;
}

inline double dot(const Coord2D &c1, const ICoord2D &c2) {
  double dotproduct = 0;
  for(int i=0; i<3; i++)	
    dotproduct += c1[i]*(double)c2[i];
  return dotproduct;
}

inline int norm2(const ICoord2D &c) {
  return dot(c, c);
}

bool operator<(const ICoord2D &a, const ICoord2D &b);


// ICoord3D operators

std::ostream &operator<<(std::ostream&, const ICoord3D&);
// std::istream &operator>>(std::istream&, ICoord3D&);

inline ICoord3D operator+(const ICoord3D &a, const ICoord3D &b) {
  ICoord3D result(a);
  result += b;
  return result;
}

inline ICoord3D operator-(const ICoord3D &a, const ICoord3D &b) {
  ICoord3D result(a);
  result -= b;
  return result;
}

inline Coord3D operator+(const Coord3D &a, const ICoord3D &b) {
  Coord3D result(a);
  result += b;
  return result;
}

inline Coord3D operator-(const Coord3D &a, const ICoord3D &b) {
  Coord3D result(a);
  result -= b;
  return result;
}

inline Coord3D operator+(const ICoord3D &b, const Coord3D &a) {
  Coord3D result(a);
  result += b;
  return result;
}

inline Coord3D operator-(const ICoord3D &b, const Coord3D &a) {
  Coord3D result(a);
  result -= b;
  return result;
}

inline ICoord3D operator*(const ICoord3D &a, int x) {
  ICoord3D b(a);
  b *= x;
  return b;
}

inline ICoord3D operator*(int x, const ICoord3D &a) {
  ICoord3D b(a);
  b *= x;
  return b;
}

inline Coord3D operator*(const ICoord3D &a, double x) {
  Coord3D b(a[0], a[1], a[2]);
  b *= x;
  return b;
}

inline bool operator==(const ICoord3D &a, const ICoord3D &b) {
  return a[0] == b[0] && a[1] == b[1] && a[2] == b[2];
}

inline bool operator!=(const ICoord3D &a, const ICoord3D &b) {
  return a[0] != b[0] || a[1] != b[1] || a[2] != b[2];
}

inline bool operator!=(const ICoord3D &a, const Coord3D &b) {
  return a[0] != b[0] || a[1] != b[1] || a[2] != b[2];
}

inline int dot(const ICoord3D &c1, const ICoord3D &c2) {
  int dotproduct = 0;
  for(int i=0; i<DIM; i++)	
    dotproduct += c1[i]*c2[i];
  return dotproduct;
}

inline double dot(const Coord3D &c1, const ICoord3D &c2) {
  double dotproduct = 0;
  for(int i=0; i<DIM; i++)	
    dotproduct += c1[i]*(double)c2[i];
  return dotproduct;
}

inline int norm2(const ICoord3D &c) {
  return dot(c, c);
}

bool operator<(const ICoord3D &a, const ICoord3D &b);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==2
typedef Coord2D Coord;
typedef ICoord2D ICoord;
#else
typedef Coord3D Coord;
typedef ICoord3D ICoord;
#endif

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


#endif // COORD_H
