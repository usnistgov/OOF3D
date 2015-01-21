// -*- C++ -*-
// $RCSfile: doublearray.h,v $
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

#ifndef DOUBLEARRAY_H
#define DOUBLEARRAY_H

#include "common/array.h"

class DoubleArray : public Array<double> {
public:
//  DoubleArray() {}
#if DIM == 2
  DoubleArray(int w, int h) : Array<double>(w,h) {}
#elif DIM == 3
  DoubleArray(int w, int h, int d) : Array<double>(w,h,d) {}
#endif
  DoubleArray(const ICoord &size, double x=0.0) : Array<double>(size, x) {}
  DoubleArray(const ICoord &size, ArrayData<double> *dptr)
    : Array<double>(size, dptr)
  {}
  DoubleArray(const Array<double> &other) : Array<double>(other) {}
  virtual ~DoubleArray() {}
};

#endif // DOUBLEARRAY_H
