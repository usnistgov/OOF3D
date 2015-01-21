// -*- C++ -*-
// $RCSfile: differ.h,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2012/06/05 19:05:02 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <limits>

// A function that computes whether or not two values are different to
// within machine epsilon.

template <class TYPE>
bool differ(const TYPE &x, const TYPE &y) {
  TYPE diff = fabs(x - y);
  TYPE ax = fabs(x);
  TYPE ay = fabs(y);
  TYPE max = ax > ay ? ax : ay;
  return diff > std::numeric_limits<TYPE>::epsilon() * max;
}

