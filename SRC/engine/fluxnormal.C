// -*- C++ -*-
// $RCSfile: fluxnormal.C,v $
// $Revision: 1.4.18.5 $
// $Author: fyc $
// $Date: 2014/07/24 21:36:25 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Support routines for the generic access method for the FluxNormal
// derived classes.  These are so that you can still query the 
// values even if you're not sure which type you've gotten.

#include "engine/fluxnormal.h"
#include "engine/ooferror.h"


double VectorFluxNormal::operator[](int n) const {
  if(n==0) 
    return val_;
  else
    throw ErrProgrammingError("Bad index for VectorFluxNormal", 
			      __FILE__, __LINE__);
}

#if DIM==2
// n is the boundary frame's x-axis, given in lab-frame coordinates.
// Use this to transform the given x and y, given in boundary-frame
// coordinates, into lab coordinates.

// This isn't defined in 3D because the coordinate system that's
// normal to the surface isn't well defined.  In 3D Neumann boundary
// conditions have to be defined in the lab coordinates.  TODO MER: This
// restriction could be relaxed as long as there are no tangential
// components to the boundary forces.

void SymTensorFluxNormal::transform(const Coord &n) {
  // TODO MER: Update for 3D.
  double normal_frame_x = x;
  double normal_frame_y = y;
  x = n[0]*normal_frame_x - n[1]*normal_frame_y;
  y = n[0]*normal_frame_y + n[1]*normal_frame_x;
}
#endif // DIM==2


std::ostream &operator<<(std::ostream &os, const FluxNormal &flxnrm) {
  flxnrm.print(os);
  return os;
}

void VectorFluxNormal::print(std::ostream  &os) const {
  os << "VectorFluxNormal(" << val_ << ")";
}

void SymTensorFluxNormal::print(std::ostream &os) const {
  os << "SymTensorFluxNormal" << val;
}
