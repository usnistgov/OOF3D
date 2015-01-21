// -*- C++ -*-
// $RCSfile: intarray.C,v $
// $Revision: 1.2.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:51 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/intarray.h"

IntArray makeIntArray(ICoord *size, int x) {
  return IntArray(*size,x);
}
