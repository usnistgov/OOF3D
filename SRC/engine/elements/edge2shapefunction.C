// -*- C++ -*-
// $RCSfile: edge2shapefunction.C,v $
// $Revision: 1.1.54.1 $
// $Author: langer $
// $Date: 2014/01/18 04:41:59 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/IO/oofcerr.h"
#include "engine/ooferror.h"
#include "edge2shapefunction.h"

// Master element for the 2-noded edge element:
//
//     0----------------------1
//  (-1,0)                  (1,0)
// Here, the y-component of master-coord is totally trivial.


Edge2ShapeFunction::Edge2ShapeFunction(const MasterElement &mel)
  : ShapeFunction(2, mel)
{
  precompute(mel);
}

double Edge2ShapeFunction::value(ShapeFunctionIndex i,
				 const MasterCoord &mc) const
{
  switch(i) {
  case 0:
    return 0.5*(1. - mc[0]);
  case 1:
    return 0.5*(1. + mc[0]);
  case 2:
    return 0.0;
  }
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

double Edge2ShapeFunction::masterderiv(ShapeFunctionIndex i, SpaceIndex j,
				       const MasterCoord &mc) const
{
  checkSpaceIndex(j);
  if(j == 1 || j == 2)
    return 0;
  switch(i) {
  case 0:
    return -0.5;
  case 1:
    return  0.5;
  }
  throw ErrBadIndex(i, __FILE__, __LINE__);
}
