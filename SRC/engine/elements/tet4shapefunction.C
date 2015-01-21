// -*- C++ -*-
// $RCSfile: tet4shapefunction.C,v $
// $Revision: 1.2.10.3 $
// $Author: langer $
// $Date: 2014/09/27 22:34:28 $

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
#include "tet4shapefunction.h"

//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Tet4ShapeFunction::Tet4ShapeFunction(const MasterElement &mel)
  : ShapeFunction(4, mel)
{
  precompute(mel);
}

double Tet4ShapeFunction::value(ShapeFunctionIndex i,
				      const MasterCoord &mc) const
{
  if(i == 0)
    return 1.0 - mc[0] - mc[1] - mc[2];
  if(i == 1)
    return mc[1];
  if(i == 3)
    return mc[0];
  if(i == 2)
    return mc[2];
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

double Tet4ShapeFunction::masterderiv(ShapeFunctionIndex i, SpaceIndex j,
				       const MasterCoord &mc) const
{
  if(i==0)
    return -1.0;
  if((i==1 && j==1) || (i==3 && j==0) || (i==2 && j==2))
    return 1.0;
  return 0.0;
}

