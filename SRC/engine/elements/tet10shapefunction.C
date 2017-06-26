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
#include "engine/ooferror.h"
#include "tet10shapefunction.h"


Tet10ShapeFunction::Tet10ShapeFunction(const MasterElement &mel)
  : ShapeFunction(10, mel)
{
  precompute(mel);
}

double Tet10ShapeFunction::value(ShapeFunctionIndex i, const MasterCoord &mc)
  const
{
  // If we define (x, y, z) = mc and t = 1-x-y-z, then the symmetry of
  // these expressions is more apparent, but we don't get any
  // numerical advantage from rewriting them.  (t, x, y, z) are the
  // barycentric coordinates of mc.
  if(i == 0)			// 2*t*(t-0.5)
    return 2.0 * (0.5 - mc[0] - mc[1] - mc[2]) * (1.0 - mc[0] - mc[1] - mc[2]);
  if(i == 1)			
    return 2.0 * (mc[1] - 0.5) * mc[1];	// 2*y*(y-0.5)
  if(i == 2)			
    return 2.0 * (mc[2] - 0.5) * mc[2];	// 2*z*(z-0.5)
  if(i == 3)
    return 2.0 * (mc[0] - 0.5) * mc[0];	// 2*x*(x-0.5)
  if(i == 4)
    return 4.0 * (1.0 - mc[0] - mc[1] - mc[2]) * mc[1]; // 4*t*y;
  if(i == 5)
    return 4.0 * mc[1] * mc[2];	// 4*y*z
  if(i == 6)
    return 4.0 * (1.0 - mc[0] - mc[1] - mc[2]) * mc[2]; // 4*t*z
  if(i == 7)
    return 4.0 * (1.0 - mc[0] - mc[1] - mc[2]) * mc[0]; // 4*t*x
  if(i == 8)
    return 4.0 * mc[0] * mc[1];	// 4*x*y
  if(i == 9)
    return 4.0 * mc[0] * mc[2];	// 4*x*z
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

double Tet10ShapeFunction::masterderiv(ShapeFunctionIndex i, SpaceIndex j,
				       const MasterCoord &mc)
  const
{
  // d phi_i/d x_j
  
  if(i == 0) {				    // sf0 = 2*t*(t-1/2)
    double t = 1.0 - mc[0] - mc[1] - mc[2];
    return 1.0 - 4.0*t;		// dt/x_j = -1
  }
  if(i == 1) {			// sf1 = 2*y*(y-1/2)
    if(j == 1)
      return 4.0*mc[1] - 1.0;
    return 0.0;
  }
  if(i == 2) {			// sf2 = 2*z*(z-1/2)
    if(j == 2)
      return 4.0*mc[2] - 1.0;
    return 0.0;
  }
  if(i == 3) {			// sf3 = 2*x*(x-1/2)
    if(j == 0)
      return 4.0*mc[0] - 1.0;
    return 0.0;
  }
  if(i == 4) {			// sf4 = 4*t*y
    if(j == 1)
      return 4.0 * (1 - mc[0] - 2*mc[1] - mc[2]);
    else
      return -4.0 * mc[1];
  }
  if(i == 5) {			// sf5 = 4*y*z
    if(j == 0)
      return 0.0;
    if(j == 1)
      return 4.0 * mc[2];
    if(j == 2)
      return 4.0 * mc[1];
  }
  if(i == 6) {			// sf6 = 4*t*z
    if(j == 2)
      return 4.0 * (1 - mc[0] - mc[1] - 2*mc[2]);
    else
      return -4.0 * mc[2];
  }
  if(i == 7) {			// sf7 = 4*t*x
    if(j == 0)
      return 4.0 * (1 - 2*mc[0] - mc[1] - mc[2]);
    else
      return -4.0 * mc[0];
  }
  if(i == 8) {			// sf8 = 4*x*y
    if(j == 0)
      return 4.0 * mc[1];
    if(j == 1)
      return 4.0 * mc[0];
    if(j == 2)
      return 0.0;
  }
  if(i == 9) {			// sf9 = 4*x*z
    if(j == 0)
      return 4.0 * mc[2];
    if(j == 1)
      return 0.0;
    if(j == 2)
      return 4.0 * mc[0];
  }
  throw ErrBadIndex(i, __FILE__, __LINE__);
}
