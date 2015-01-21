// -*- C++ -*-
// $RCSfile: quad9shapefunction.C,v $
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

// Eight node quadrilateral element

#include <oofconfig.h>
#include "engine/ooferror.h"
#include "engine/masterelement.h"
#include "quad9shapefunction.h"


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Master element for the eight node quadrilateral.
//
//                      (0, 1)
//  (-1, 1)  6------------5-----------4  (1, 1)
//           |                        |
//           |                        |
//           |                        |
//           |                        |
//  (-1, 0)  7         8(0, 0)        3  (1, 0)
//           |                        |
//           |                        |
//           |                        |
//           |                        |
//  (-1,-1)  0------------1-----------2  (1,-1)
//                      (0,-1)        

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Quad9ShapeFunction::Quad9ShapeFunction(const MasterElement &mel)
  : ShapeFunction(8, mel)
{
  precompute(mel);
}

double Quad9ShapeFunction::value(ShapeFunctionIndex i, const MasterCoord &mc)
  const
{
  if(i == 0)			// (-1, -1)
    return 0.25*mc[0]*(mc[0] - 1.)*mc[1]*(mc[1] - 1.);
  if(i == 1)			// (0, -1)
    return -0.5*(mc[0] - 1.)*(mc[0] + 1.)*mc[1]*(mc[1] - 1.);
  if(i == 2)			// (1, -1)
    return 0.25*mc[0]*(mc[0] + 1.)*mc[1]*(mc[1] - 1.);
  if(i == 3)			// (1, 0)
    return -0.5*mc[0]*(mc[0] + 1.)*(mc[1] - 1.)*(mc[1] + 1.);
  if(i == 4)			// (1, 1)
    return 0.25*mc[0]*(mc[0] + 1.)*mc[1]*(mc[1] + 1.);
  if(i == 5)			// (0, 1)
    return -0.5*(mc[0] - 1.)*(mc[0] + 1.)*mc[1]*(mc[1] + 1.);
  if(i == 6)			// (-1, 1)
    return 0.25*mc[0]*(mc[0] - 1.)*mc[1]*(mc[1] + 1.);
  if(i == 7)			// (-1, 0)
    return -0.5*mc[0]*(mc[0] - 1.)*(mc[1] - 1.)*(mc[1] + 1.);
  if(i == 8)			// (0, 0)
    return (mc[0] - 1.)*(mc[0] + 1.)*(mc[1] - 1.)*(mc[1] + 1.);
  throw ErrBadIndex(i, __FILE__, __LINE__);
}

double Quad9ShapeFunction::masterderiv(ShapeFunctionIndex i, SpaceIndex j,
				       const MasterCoord &mc) const
{
  checkSpaceIndex(j);
  if(j == 2)
    return 0;
  switch(i) {
  case 0:
    switch(j) {
    case 0:
      return 0.25*(2.*mc[0] - 1.)*mc[1]*(mc[1] - 1.);
    case 1:
      return 0.25*mc[0]*(mc[0] - 1.)*(2.*mc[1] - 1.);
    }
  case 1:
    switch(j) {
    case 0:
      return -mc[0]*mc[1]*(mc[1] - 1.);
    case 1:
      return -0.5*(mc[0]*mc[0] - 1.)*(2.*mc[1] - 1.);
    }
  case 2:
    switch(j) {
    case 0:
      return 0.25*(2.*mc[0] + 1.)*mc[1]*(mc[1] - 1.);
    case 1:
      return 0.25*mc[0]*(mc[0] + 1.)*(2.*mc[1] - 1.);
    }
  case 3:
    switch(j) {
    case 0:
      return -0.5*(2.*mc[0] + 1)*(mc[1]*mc[1] - 1.);
    case 1:
      return -mc[0]*(mc[0] + 1.)*mc[1];
    }
  case 4:
    switch(j) {
    case 0:
      return 0.25*(2.*mc[0] + 1.)*mc[1]*(mc[1] + 1.);
    case 1:
      return 0.25*mc[0]*(mc[0] + 1.)*(2.*mc[1] + 1.);
    }
  case 5:
    switch(j) {
    case 0:
      return -mc[0]*mc[1]*(mc[1] + 1.);
    case 1:
      return -0.5*(mc[0]*mc[0] - 1.)*(2.*mc[1] + 1.);
    }
  case 6:
    switch(j) {
    case 0:
      return 0.25*(2.*mc[0] - 1.)*mc[1]*(mc[1] + 1.);
    case 1:
      return 0.25*mc[0]*(mc[0] - 1.)*(2.*mc[1] + 1.);
    }
  case 7:
    switch(j) {
    case 0:
      return -0.5*(2.*mc[0] - 1)*(mc[1]*mc[1] - 1.);
    case 1:
      return -mc[0]*(mc[0] - 1.)*mc[1];
    }
  case 8:
    switch(j) {
    case 0:
      return 2.*mc[0]*(mc[1]*mc[1] - 1.);
    case 1:
      return 2.*(mc[0]*mc[0] - 1.)*mc[1];
    }
  }
  throw ErrBadIndex(i, __FILE__, __LINE__);
}
