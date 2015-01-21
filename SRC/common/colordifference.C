// -*- C++ -*-
// $RCSfile: colordifference.C,v $
// $Revision: 1.4.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:49 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <math.h> 

#include "common/colordifference.h"

bool DeltaRGB::contains(const CColor &c1, const CColor &c2) const {
  double rdiff = fabs(c1.getRed()-c2.getRed());
  double gdiff = fabs(c1.getGreen()-c2.getGreen());
  double bdiff = fabs(c1.getBlue()-c2.getBlue());
  
  if (rdiff <= delta_red && gdiff <= delta_green && bdiff <= delta_blue)
    return true;
  return false;
}


bool DeltaGray::contains(const CColor &c1, const CColor &c2) const {
  double grdiff = fabs(c1.getGray()-c2.getGray());
  if (grdiff <= delta_gray)
    return true;
  return false;
}


bool DeltaHSV::contains(const CColor &c1, const CColor &c2) const {
  double hdiff;
  double h1=c1.getHue();
  double h2=c2.getHue();
  // hdiff is the smallest difference between h1 and h2.
  if (h1<h2) 
    hdiff=h2-h1;
  else 
    hdiff=h1-h2;
  if (hdiff>180.0)
    hdiff=360.0-hdiff;
  double sdiff = fabs(c1.getSaturation()-c2.getSaturation());
  double vdiff = fabs(c1.getValue()-c2.getValue());
  
  if (hdiff <= delta_hue && sdiff <= delta_saturation && vdiff <= delta_value)
    return true;
  return false;
}


std::ostream &operator<<(std::ostream &os, const ColorDifference &cd) {
  cd.print(os);
  return os;
}

void DeltaRGB::print(std::ostream &os) const {
  os << "DeltaRGB(" << delta_red << ", " << delta_green
     << ", " << delta_blue << ")";
}

void DeltaGray::print(std::ostream &os) const {
  os << "DeltaGray(" << delta_gray << ")";
}
void DeltaHSV::print(std::ostream &os) const {
  os << "DeltaHSV(" << delta_hue << ", " << delta_saturation 
     << ", " << delta_value << ")";
}	
