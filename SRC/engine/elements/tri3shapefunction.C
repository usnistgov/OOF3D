// -*- C++ -*-
// $RCSfile: tri3shapefunction.C,v $
// $Revision: 1.2.18.2 $
// $Author: langer $
// $Date: 2014/02/28 03:22:01 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "engine/ooferror.h"
#include "engine/shapefunction.h"
#include "tri3shapefunction.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Master element for the three node triangle:
//
//       1  (0,1)                                      // comments
//       |\                                            // ending in
//       | \                                           // backslashes
//       |  \                                          // generate
//       |   \                                         // spurious
//       |    \                                        // compiler
//       |     \                                       // warnings
//       2------0
//  (0,0)          (1,0)
//
// Number the nodes this way so that Cartesian coordinates (x,y)
// correspond to area coordinates (x,y,1-x-y).

Tri3ShapeFunction::Tri3ShapeFunction(const MasterElement &mel)
  : ShapeFunction(3, mel)
{
  precompute(mel);
}

double Tri3ShapeFunction::value(ShapeFunctionIndex i,
				     const MasterCoord &mc) const
{
  if(i == 0)
    return mc[0];
  if(i == 1)
    return mc[1];
  if(i == 2)
    return 1.0 - mc[0] - mc[1];
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

double Tri3ShapeFunction::masterderiv(ShapeFunctionIndex i, SpaceIndex j,
				      const MasterCoord &) const
{
  checkSpaceIndex(j);
  if(j == 2)
    return 0.0;
  if(i == 2)
    return -1.0;
  if((i==0 && j==0) || (i==1 && j==1)) 
    return 1.0;
  return 0.0;
}

