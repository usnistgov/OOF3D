// -*- C++ -*-
// $RCSfile: quad9shapefunction.h,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:18 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef QUAD9SHAPEFUNCTION_H
#define QUAD9SHAPEFUNCTION_H

#include "engine/shapefunction.h"

class Quad9ShapeFunction : public ShapeFunction {
public:
  Quad9ShapeFunction(const MasterElement&);
  virtual double value(ShapeFunctionIndex, const MasterCoord&) const;
  virtual double masterderiv(ShapeFunctionIndex, SpaceIndex, const MasterCoord&)
    const;
  // see comment in quad4shapefunction.h
  virtual int degree() const { return 2; }
  virtual int deriv_degree() const { return 2; }
};

#endif
