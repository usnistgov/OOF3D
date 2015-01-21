// -*- C++ -*-
// $RCSfile: mastercoord.C,v $
// $Revision: 1.8.10.4 $
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

#include <oofconfig.h>
#include "common/coord.h"
#include "engine/mastercoord.h"
#include "engine/shapefunction.h"

#if DIM==3
MasterCoord::MasterCoord(const Coord &c) {
  x[0] = c[0]; x[1] = c[1]; x[2] = c[2];
}
#endif // DIM==3

// double-dispatch functions for shape function evaluation

// value of shapefunction
double MasterCoord::shapefunction(const ShapeFunction &sf, ShapeFunctionIndex n)
  const
{
  return sf.value(n, *this);
}

// derivative of shapefunction wrt master coordinates
double MasterCoord::mdshapefunction(const ShapeFunction &sf,
				   ShapeFunctionIndex n,
				   SpaceIndex i)
  const
{
  return sf.masterderiv(n, i, *this);
}

// derivative of shapefunction wrt real coordinates
double MasterCoord::dshapefunction(const ElementBase *el,
				   const ShapeFunction &sf,
				   ShapeFunctionIndex n, SpaceIndex i)
  const
{
  return sf.realderiv(el, n, i, *this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const MasterPosition &mpos) {
  return mpos.print(os);
}

std::ostream &MasterCoord::print(std::ostream &os) const {
  os << "MasterCoord" << *this;
  return os;
}

std::ostream &operator<<(std::ostream &os, const MasterCoord &coord) {
#if DIM == 2
  os << "(" << coord[0] << ", " << coord[1] << ")";
#elif DIM == 3
  os << "(" << coord[0] << ", " << coord[1] << ", " << coord[2] << ")";
#endif
  return os;
}

std::istream &operator>>(std::istream &is, MasterCoord &coord) {
  char c;
  is >> c;
  if(!is || c != '(') {		// check for initial '('
    is.clear(std::ios::badbit | is.rdstate());
    return is;
  }
  is >> coord[0];		// read x component
  if(!is) return is;		// check for error
  is >> c;
  if(!is || c != ',') {		// check for ','
    is.clear(std::ios::badbit | is.rdstate());
    return is;
  }
  is >> coord[1];
  if(!is) return is;
  is >> c;
  if(!is || c != ')') {
    is.clear(std::ios::badbit | is.rdstate());
    return is;
  }
  return is;
}

#if DIM == 2
std::ostream &operator<<(std::ostream &os, const MasterEndPoint &mep) {
  os << "MasterEndPoint" << *mep.mc;
  return os;
}
#endif
