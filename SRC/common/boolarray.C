// -*- C++ -*-
// $RCSfile: boolarray.C,v $
// $Revision: 1.15.18.5 $
// $Author: langer $
// $Date: 2014/12/14 22:49:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/boolarray.h"
#include "common/coord.h"
#include <string.h>		// for memset()

BoolArray BoolArray::clone() const {
  BoolArray bozo(bounds_.upperright());
  bozo.dataptr->copy(*dataptr);
  return bozo;
}

BoolArray BoolArray::subarray(const ICoord &crnr0, const ICoord &crnr1) {
  BoolArray newarray(dataptr->size, dataptr);
  ++dataptr->refcount;
#if DIM == 2
  newarray.bounds_ = ICRectangle(crnr0, crnr1);
#elif DIM == 3
  newarray.bounds_ = ICRectangularPrism(crnr0, crnr1);
#endif
  newarray.bounds_.restrict(bounds());
  newarray.findfin();
  return newarray;
}

const BoolArray BoolArray::subarray(const ICoord &crnr0, const ICoord &crnr1)
  const
{
  BoolArray newarray(dataptr->size, dataptr);
  ++dataptr->refcount;
#if DIM == 2
  newarray.bounds_ = ICRectangle(crnr0, crnr1);
#elif DIM == 3
  newarray.bounds_ = ICRectangularPrism(crnr0, crnr1);
#endif
  newarray.bounds_.restrict(bounds());
  newarray.findfin();
  return newarray;
}

void BoolArray::clear(const bool &v) {
  int x = bounds_.xmin();
  int w = width();
#if DIM == 2
  for(int j=bounds_.ymin(); j<bounds_.ymax(); j++) {
     memset(&(*this)[ICoord(x, j)], v, w*sizeof(bool));
  }
#elif DIM == 3
	for(int k=bounds_.zmin(); k<bounds_.zmax(); ++k) {
		for(int j=bounds_.ymin(); j<bounds_.ymax(); j++) {
			memset(&(*this)[ICoord(x, j, k)], v, w*sizeof(bool));
		}
  }
#endif
}

ICoordVector *BoolArray::pixels(bool v) const {
  ICoordVector *pxls = new ICoordVector;
  for(const_iterator i=begin(); i!=end(); ++i) {
    if(*i == v)
      pxls->push_back(i.coord());
  }
  return pxls;
}

int BoolArray::nset() const {
  // TODO 3.1: Keep track of number of set bits, and don't loop
  // here!  This is actually quite difficult to do with the current
  // Array architecture.  One problem is that in order to maintain an
  // always up-to-date count of the set bits, operator[](ICoord) has
  // to be disabled, preventing direct access to bits.  This requires
  // that BoolArray no longer be a subclass of Array<bool>, and
  // instead contains an Array<bool>.  The code for subarrays and
  // clones becomes messy but not impossible.  The second more serious
  // problem is keeping the count up-to-date in subarrays, which share
  // data with the main array.
  int n = 0;
  for(const_iterator i=begin(); i!=end(); ++i)
    if(*i)
      ++n;
  return n;
}

bool BoolArray::empty() const {
  // TODO 3.1: Keep track of number of set bits, and don't loop here!  See
  // comment above.
  for(const_iterator i=begin(); i!=end(); ++i)
    if(*i)
      return false;
  return true;
}

void BoolArray::invert() {
  for(iterator i=begin(); i!=end(); ++i)
    *i ^= 1;
}
