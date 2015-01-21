// -*- C++ -*-
// $RCSfile: quad4shapefunction.C,v $
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

#include <oofconfig.h>
#include "engine/ooferror.h"
#include "quad4shapefunction.h"

//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//-\\-//

// Master element for the four node quadrilateral:
//
//  (-1,1)   3--------------------2  (1,1)
//           |                    | 
//           |                    |
//           |                    |
//           |                    |
//           |                    |
//           |                    |
//           |                    |
//  (-1,-1)  0--------------------1  (1,-1)


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Quad4ShapeFunction::Quad4ShapeFunction(const MasterElement &mel)
  : ShapeFunction(4, mel)
{
  precompute(mel);
}

double Quad4ShapeFunction::value(ShapeFunctionIndex i,
				      const MasterCoord &mc) const
{
  if(i == 0)
    return 0.25*(1. - mc[0])*(1. - mc[1]);
  if(i == 1)
    return 0.25*(1. + mc[0])*(1. - mc[1]);
  if(i == 2)
    return 0.25*(1. + mc[0])*(1. + mc[1]);
  if(i == 3)
    return 0.25*(1. - mc[0])*(1. + mc[1]);
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

double Quad4ShapeFunction::masterderiv(ShapeFunctionIndex i, SpaceIndex j,
				       const MasterCoord &mc) const
{
  checkSpaceIndex(j);
  if(j == 2)
    return 0;
  switch(i) {
  case 0:
    switch(j) {
    case 0:
      return -0.25*(1. - mc[1]);
    case 1:
      return -0.25*(1. - mc[0]);
    }
  case 1:
    switch(j) {
    case 0:
      return  0.25*(1. - mc[1]);
    case 1:
      return -0.25*(1. + mc[0]);
    }
  case 2:
    switch(j) {
    case 0:
      return  0.25*(1. + mc[1]);
    case 1:
      return  0.25*(1. + mc[0]);
    }
  case 3:
    switch(j) {
    case 0:
      return -0.25*(1. + mc[1]);
    case 1:
      return  0.25*(1. - mc[0]);
    }
  }
  throw ErrBadIndex(i, __FILE__, __LINE__);
}


