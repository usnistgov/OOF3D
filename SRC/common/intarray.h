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

#ifndef INTARRAY_H
#define INTARRAY_H

#include "common/array.h"

class IntArray : public Array<int> {
public:
  IntArray(int w, int h) : Array<int>(w,h) {}
  IntArray(const ICoord &size, int x=0.0) : Array<int>(size, x) {}
//  IntArray(const ICoord *size, int x=0.0) : Array<int>(*size, x) {}
  IntArray(const ICoord &size, ArrayData<int> *dptr)
    : Array<int>(size, dptr)
  {}
  IntArray(const Array<int> &other) : Array<int>(other) {}
  virtual ~IntArray() {}
};

IntArray makeIntArray(ICoord *,int);

#endif // INTARRAY_H
