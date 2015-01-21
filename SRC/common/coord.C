// -*- C++ -*-
// $RCSfile: coord.C,v $
// $Revision: 1.12.18.12 $
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

#include <oofconfig.h>
#include "common/coord.h"
#include "common/differ.h"
#include <math.h>		// for round

Coord2D &Coord2D::operator+=(const ICoord2D &ic) {
  x[0] += ic[0];
  x[1] += ic[1];
  return *this;
}

Coord2D &Coord2D::operator-=(const ICoord2D &ic) {
  x[0] -= ic[0];
  x[1] -= ic[1];
  return *this;
}

bool Coord2D::differFrom(const Coord2D &other) const {
  return (differ(x[0], other[0]) || differ(x[1], other[1]));
}

Coord2D Coord2D::operator-() const {
  return -1.0 * (*this);
}

Coord3D &Coord3D::operator+=(const ICoord3D &ic) {
  x[0] += ic[0];
  x[1] += ic[1];
  x[2] += ic[2];
  return *this;
}

Coord3D &Coord3D::operator-=(const ICoord3D &ic) {
  x[0] -= ic[0];
  x[1] -= ic[1];
  x[2] -= ic[2];
  return *this;
}

bool Coord3D::differFrom(const Coord3D &other) const {
  return (differ(x[0], other[0]) ||
	  differ(x[1], other[1]) ||
	  differ(x[2], other[2]));
}

Coord3D Coord3D::operator-() const {
  return -1.0 * (*this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


ICoord2D ICoord2D::operator-() const {
  return -1 * (*this);
}

ICoord2D Coord2D::roundComponents() const {
  return ICoord2D(round(x[0]), round(x[1]));
}

ICoord3D ICoord3D::operator-() const {
  return -1 * (*this);
}

ICoord3D Coord3D::roundComponents() const {
  return ICoord3D(round(x[0]), round(x[1]) , round(x[2]));
}

std::ostream &operator<<(std::ostream &os, const Coord2D &coord) {
  os << "(" << coord[0] << ", " << coord[1] << ")";
  return os;
}

std::ostream &operator<<(std::ostream &os, const Coord3D &coord) {
  os << "(" << coord[0] << ", " << coord[1] << ", " << coord[2] << ")";
  return os;
}

// std::istream &operator>>(std::istream &is, Coord &coord) {
//   char c;
//   is >> c;
//   if(!is || c != '(') {		// check for initial '('
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   is >> coord[0];		// read x component
//   if(!is) return is;		// check for error
//   is >> c;
//   if(!is || c != ',') {		// check for ','
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   is >> coord[1];
//   if(!is) return is;
//   is >> c;
// #if DIM == 3
//   if(!is || c != ',') {		// check for ','
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   is >> coord[2];
//   if(!is) return is;
//   is >> c;	
// #endif
//   if(!is || c != ')') {
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   return is;
// }

std::ostream &operator<<(std::ostream &os, const ICoord2D &coord) {
  os << "(" << coord[0] << ", " << coord[1] << ")";
  return os;
}

std::ostream &operator<<(std::ostream &os, const ICoord3D &coord) {
  os << "(" << coord[0] << ", " << coord[1] << ", " << coord[2] << ")";
  return os;
}

// std::istream &operator>>(std::istream &is, ICoord &coord) {
//   char c;
//   is >> c;
//   if(!is || c != '(') {		// check for initial '('
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   is >> coord[0];		// read x component
//   if(!is) return is;		// check for error
//   is >> c;
//   if(!is || c != ',') {		// check for ','
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   is >> coord[1];
//   if(!is) return is;
//   is >> c;
// #if DIM == 3
//   if(!is || c != ',') {		// check for ','
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   is >> coord[2];
//   if(!is) return is;
//   is >> c;
// #endif
//   if(!is || c != ')') {
//     is.clear(std::ios::badbit | is.rdstate());
//     return is;
//   }
//   return is;
// }

bool operator<(const ICoord2D &a, const ICoord2D &b) {
  if(a[0] < b[0]) return true;
  if(a[0] > b[0]) return false;
  if(a[1] < b[1]) return true;
 return false;
}

bool operator<(const ICoord3D &a, const ICoord3D &b) {
  if(a[0] < b[0]) return true;
  if(a[0] > b[0]) return false;
  if(a[1] < b[1]) return true;
  if(a[1] > b[1]) return false;
  if(a[2] < b[2]) return true;
 return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const ICoord2D ICoord2D::origin(0, 0);
const Coord2D Coord2D::origin(0., 0.);

const ICoord3D ICoord3D::origin(0, 0, 0);
const Coord3D Coord3D::origin(0., 0., 0.);

