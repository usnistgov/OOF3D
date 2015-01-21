// -*- C++ -*-
// $RCSfile: bitmask.h,v $
// $Revision: 1.6.18.1 $
// $Author: langer $
// $Date: 2012/12/26 01:33:19 $

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

// The BitMask class is a wrapper for BoolArray with a few
// enhancements convenient for using it as a mask.  The constructor
// takes an ICoord 'center' argument, as well as an ICoord size.  The
// coordinates used by operator[] are relative to the given center.
// The iterator and const_iterator iterate over only the non-zero (ie
// true) pixels in the mask, and their coord() functions return
// ICoords relative to the mask's 'center'.  If it's necessary to
// iterate over all of the pixels, not just the 1's, you have to get
// an iterator with BitMask::raw_begin() and increment it with
// BitMaskIterator::raw_incr(), instead of operator++.

class BitMask;
class BitMaskIterator;
class ConstBitMaskIterator;

class BitMask {
private:
  ICoord center;
  BoolArray data;
public:
  BitMask(const ICoord &size, const ICoord &center, bool val=false);

  bool &operator[](const BitMaskIterator&);
  bool operator[](const ConstBitMaskIterator&) const;
  bool &operator[](const ICoord&);
  bool operator[](const ICoord&) const;

  typedef BitMaskIterator iterator;
  typedef ConstBitMaskIterator const_iterator;

  iterator begin();		// first true pixel
  const_iterator begin() const;
  iterator raw_begin();		// first pixel, independent of value
  const_iterator raw_begin() const;
  iterator end();
  const_iterator end() const;

  friend class BitMaskIterator;
  friend class ConstBitMaskIterator;
};

// Iterators could be derived from ArrayIterator<bool>, but since
// these will be used a lot it's probably best to avoid virtual
// function calls.

class BitMaskIterator {
private:
  ICoord location;	    // (0, 0, [0]) -> (width, height, [depth])
  BitMask &bitmask;
public:
  BitMaskIterator(BitMask &mask) : bitmask(mask) {}
  void operator++();		// increment to next true pixel
  void raw_incr();		// increment without checking value
  bool &operator*() { return bitmask[*this]; }
  const ICoord coord() const { return location - bitmask.center; }
  friend bool operator==(const BitMaskIterator&, const BitMaskIterator&);
  friend bool operator!=(const BitMaskIterator&, const BitMaskIterator&);
  friend class BitMask;
};

class ConstBitMaskIterator {
private:
  ICoord location;
  const BitMask &bitmask;
public:
  ConstBitMaskIterator(const BitMask &mask) : bitmask(mask) {}
  void operator++();
  void raw_incr();
  bool operator*() const { return bitmask[*this]; }
  const ICoord coord() const { return location - bitmask.center; }
  friend bool operator==(const ConstBitMaskIterator&,
			 const ConstBitMaskIterator&);
  friend bool operator!=(const ConstBitMaskIterator&,
			 const ConstBitMaskIterator&);
  friend class BitMask;
};

