// -*- C++ -*-
// $RCSfile: sincos.C,v $
// $Revision: 1.1.26.2 $
// $Author: langer $
// $Date: 2014/09/27 22:33:55 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/sincos.h"

// Efficient calculation of sin and cos together.  Algorithm borrowed
// from Numerical Recipes.

// TODO OPT: Test to see if this is really faster than calling sin() and
// cos().

void sincos(const double angle, double &sine, double &cosine) {
  double tn = tan(0.5*angle);
  if(!finite(tn)) {
    sine = sin(angle);
    cosine = cos(angle);
    return;
  }
  double tntn = 1./(1 + tn*tn);
  cosine = (1 - tn*tn)*tntn;
  sine = 2*tn*tntn;
}

