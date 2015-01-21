// -*- C++ -*-
// $RCSfile: boolarray.h,v $
// $Revision: 1.11.12.5 $
// $Author: langer $
// $Date: 2014/05/29 13:47:28 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BOOLARRAY_H
#define BOOLARRAY_H

#include <oofconfig.h>
#include "common/array.h"
#include <set>
#include <iostream>

class BoolArray : public Array<bool> {
public:
#if DIM == 2
  BoolArray(int w, int h) : Array<bool>(w, h) {}
#elif DIM == 3
  BoolArray(int w, int h, int d): Array<bool>(w, h, d) {}
#endif
  BoolArray(const ICoord &size, bool x=false) : Array<bool>(size, x) {}
  BoolArray(const ICoord &size, ArrayData<bool> *dptr)
    : Array<bool>(size, dptr)
  {}
  BoolArray(const Array<bool> &other) : Array<bool>(other) {}

  virtual ~BoolArray() {}
  BoolArray clone() const;
  BoolArray subarray(const ICoord &crnr0, const ICoord &crnr1);
  const BoolArray subarray(const ICoord &crnr0, const ICoord &crnr1) const;
  virtual void clear(const bool&);
  void set(const ICoord &pxl) { (*this)[pxl] = true; }
  void reset(const ICoord &pxl) { (*this)[pxl] = false; }
  bool get(const ICoord &pxl) const { return (*this)[pxl]; }
  void toggle(const ICoord &pxl) { (*this)[pxl] ^= 1; }
  // pointer versions to keep SWIG happy
  void set(const ICoord *pxl) { (*this)[*pxl] = true; }
  void reset(const ICoord *pxl) { (*this)[*pxl] = false; }
  bool get(const ICoord *pxl) { return (*this)[*pxl]; }
  void toggle(const ICoord *pxl) { (*this)[*pxl] ^= 1; }
  void invert();
  int nset() const;
  bool empty() const;
  ICoordVector *pixels(bool) const; // returns new'd set
};


#endif // BOOLARRAY_H
