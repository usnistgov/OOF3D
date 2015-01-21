// -*- C++ -*-
// $RCSfile: quad4shapefunction.h,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:17 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef QUAD4SHAPEFUNCTION_H
#define QUAD4SHAPEFUNCTION_H

#include "engine/shapefunction.h"

class Quad4ShapeFunction : public ShapeFunction {
public:
  Quad4ShapeFunction(const MasterElement&);
  virtual double value(ShapeFunctionIndex, const MasterCoord&) const;
  virtual double masterderiv(ShapeFunctionIndex, SpaceIndex, const MasterCoord&)
    const;
  // For quads, the value returned by degree() is actually one less
  // than the actual polynomial degree of the shape functions.
  // degree() is used to determine the number of gauss points required
  // to do an integral.  A Q4_4 shape function, such as (1-x)(1-y)/4,
  // can be integrated with two *linear* integrals, so degree()
  // returns 1, even though the polynomial degree is 2.  If the shape
  // function had an x^2 term in it, then degree() would have to
  // return 2, but then the element wouldn't be "linear".
  virtual int degree() const { return 1; }
  virtual int deriv_degree() const { return 1; }
};


#endif
