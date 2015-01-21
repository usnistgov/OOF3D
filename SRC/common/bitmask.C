// -*- C++ -*-
// $RCSfile: bitmask.C,v $
// $Revision: 1.4.18.5 $
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

#include "bitmask.h"
#include "common/coord.h"

BitMask::BitMask(const ICoord &size, const ICoord &center, bool val)
  : center(center),
    data(size, val)
{
}

bool &BitMask::operator[](const BitMaskIterator &iter) {
  return data[iter.location];
}

bool BitMask::operator[](const ConstBitMaskIterator &iter) const {
  return data[iter.location];
}

bool &BitMask::operator[](const ICoord &where) {
  return data[center + where];
}

bool BitMask::operator[](const ICoord &where) const {
  return data[center + where];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

BitMask::iterator BitMask::raw_begin() {
  return BitMaskIterator(*this);
}

BitMask::iterator BitMask::begin() {
  iterator start = BitMaskIterator(*this);
  while(start.location[DIM-1] < data.lastdim() && !*start)
    start.raw_incr();
  return start;
}

BitMask::const_iterator BitMask::raw_begin() const {
  return ConstBitMaskIterator(*this);
}

BitMask::const_iterator BitMask::begin() const {
  const_iterator start = ConstBitMaskIterator(*this);
  while(start.location[DIM-1] < data.lastdim() && !*start)
    start.raw_incr();
  return start;
}

BitMask::iterator BitMask::end() {
  iterator finis(*this);
#if DIM==2
  finis.location = ICoord(0, data.height());
#else // DIM==3
  finis.location = ICoord(0, 0, data.depth());
#endif
  return finis;
}

BitMask::const_iterator BitMask::end() const {
  const_iterator finis(*this);
#if DIM==2
  finis.location = ICoord(0, data.height());
#else // DIM==3
  finis.location = ICoord(0, 0, data.depth());
#endif
  return finis;
}

void BitMaskIterator::raw_incr() {
  const ICoord &size = bitmask.data.size();
  for(int i=0; i<DIM; i++) {
    location[i]++;
    if(location[i] < size[i])
      return;
    location[i] = 0;
  }
  location[DIM-1] = size[DIM-1]; // done
  }

void BitMaskIterator::operator++() {
  do
    raw_incr();
  while (location[DIM-1] < bitmask.data.lastdim() && !*(*this));
}

void ConstBitMaskIterator::raw_incr() {
  const ICoord &size = bitmask.data.size();
  for(int i=0; i<DIM; i++) {
    location[i]++;
    if(location[i] < size[i])
      return;
    location[i] = 0;
  }
  location[DIM-1] = size[DIM-1]; // done
}

void ConstBitMaskIterator::operator++() {
  do
    raw_incr();
  while(location[DIM-1] < bitmask.data.lastdim() && !*(*this));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool operator==(const BitMaskIterator &a, const BitMaskIterator &b) {
  return a.location == b.location;
}

bool operator!=(const BitMaskIterator &a, const BitMaskIterator &b) {
  return a.location != b.location;
}

bool operator==(const ConstBitMaskIterator &a, const ConstBitMaskIterator &b) {
  return a.location == b.location;
}

bool operator!=(const ConstBitMaskIterator &a, const ConstBitMaskIterator &b) {
  return a.location != b.location;
}
