// -*- C++ -*-
// $RCSfile: contourcell.C,v $
// $Revision: 1.7.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "contourcell.h"
#include "common/printvec.h"

bool operator==(const ContourCellCoord &a, const ContourCellCoord &b) {
  return a.ix == b.ix && a.iy == b.iy;
}

std::ostream &operator<<(std::ostream &os, const ContourCellCoord &c) {
  return os << "ContourCellCoord(" << c.x << ", " << c.y << ")";
}

std::ostream &operator<<(std::ostream &os, const ContourCellSkeleton &csk) {
  os << "ContourCellSkeleton(" << csk.corner[0] << ", "
     << csk.corner[1] << ", " << csk.corner[2] << ")";
  return os;
}
