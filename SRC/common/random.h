// -*- C++ -*-
// $RCSfile: random.h,v $
// $Revision: 1.4.18.7 $
// $Author: langer $
// $Date: 2014/11/05 16:54:16 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


#ifndef RANDOM_H
#define RANDOM_H

void rndmseed(int seed);
double rndm();
int irndm();
double gasdev();

#include <vector>


// RandomNumberGenerator Function object needed so routines such as
// std::random_shuffle use our chosen random number seed
class OOFRandomNumberGenerator
{
public:
  OOFRandomNumberGenerator() {};
  int operator() (int aRange);
};

// This implementation of std::random_shuffle was copied from
// /usr/include/c++/4.2.1/bits/stl_algo.h on OS X 10.9 and renamed.
// This version is the same as OS X 10.7 and at all Linuxes that we've
// tested.  The version provided by clang++ on OS X 10.9 (in
// /Applications/XCode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/c++/v1/algorithm)
// doesn't behave the same way, and makes our tests fail.

// On OS X 10.7, but not OS X 10.9 or Linux, this fails to compile
// unless iostream is included before algorithm.  TODO: WTF?
#include <iostream>
#include <algorithm>

template<typename _RandomAccessIterator, typename _RandomNumberGenerator>
void oofshuffle(_RandomAccessIterator __first, _RandomAccessIterator __last,
		_RandomNumberGenerator& __rand)
{
  if (__first == __last)
    return;
  for (_RandomAccessIterator __i = __first + 1; __i != __last; ++__i)
    std::iter_swap(__i, __first + __rand((__i - __first) + 1));
}

std::vector<int> *randomInts(int);

#endif	// RANDOM_H
