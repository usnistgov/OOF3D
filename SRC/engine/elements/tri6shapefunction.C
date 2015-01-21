// -*- C++ -*-
// $RCSfile: tri6shapefunction.C,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/01/18 04:42:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Shape function definition for a six-node triangular
// element, using a particular node-ordering convetion where the
// corner nodes precede the edge nodes. 

#include <oofconfig.h>
#include "engine/ooferror.h"
#include "tri6shapefunction.h"

// This is the ordering scheme in the master space:
//
// Master element for the six node triangle.
// See comment in subparametric.h for node numbering convention.
//
//       2  (0,1)
//       |\ 				// backslash
//       | \				// terminated
//       |  \				// comments
//       3   1				// generate
//       |    \				// unnecessary
//       |     \			// compiler
//       |      \			// warnings
//       4---5---0
//  (0,0)           (1,0)
//
// Number the nodes this way so that Cartesian coordinates (x,y)
// correspond to area coordinates (x,y,1-x-y).

// Definition follows, using the above node-ordering.
//
Tri6ShapeFunction::Tri6ShapeFunction(const MasterElement &mel)
  : ShapeFunction(6, mel)
{
  precompute(mel);
}

double Tri6ShapeFunction::value(ShapeFunctionIndex i, const MasterCoord &mc)
  const
{
  if(i == 0) 
    return mc[0]*(2.0*mc[0] - 1.0);
  if(i == 2)
    return mc[1]*(2.0*mc[1] - 1.0);
  if(i == 4) {
    double mc2 = 1.0 - mc[0] - mc[1];
    return mc2*(2.0*mc2 - 1);
  }
  if(i == 1)
    return 4.0*mc[0]*mc[1];
  if(i == 3)
    return 4.0*mc[1]*(1.0 - mc[0] - mc[1]);
  if(i == 5)
    return 4.0*mc[0]*(1.0 - mc[0] - mc[1]);
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

double Tri6ShapeFunction::masterderiv(ShapeFunctionIndex i, SpaceIndex j,
				      const MasterCoord &mc) const
{
  checkSpaceIndex(j);
  if(j == 2)
    return 0;
  switch(i) {
  case 0:
    switch(j) {
    case 0:
      return 4.*mc[0] - 1.0;
    case 1:
      return 0.0;
    }
  case 2:
    switch(j) {
    case 0:
      return 0.0;
    case 1:
      return 4.*mc[1] - 1.0;
    }
  case 4: 
    {	// local variable needs well defined scope, which case doesn't provide.
      double mc2 = 1.0 - mc[0] - mc[1];
      return -4.*mc2 + 1.0;
    }
  case 1:
    switch(j) {
    case 0:
      return 4.0*mc[1];
    case 1:
      return 4.0*mc[0];
    }
  case 3:
    switch(j) {
    case 0:
      return -4.0*mc[1];
    case 1:
      return 4.0*(1.0 - mc[0] - 2.0*mc[1]);
    }
  case 5:
    switch(j) {
    case 0:
      return 4.0*(1.0 - 2.0*mc[0] - mc[1]);
    case 1:
      return -4.0*mc[0];
    }
  }
  throw ErrBadIndex(i, __FILE__, __LINE__);
}
