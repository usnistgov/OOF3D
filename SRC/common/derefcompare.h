// -*- C++ -*-
// $RCSfile: derefcompare.h,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2016/03/18 19:24:37 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef DEREFCOMPARE_H
#define DEREFCOMPARE_H

// Comparator object for sorting sets and maps of pointers by the
// value pointed to, not by the pointers themselves.  This is useful
// to ensure that the values aren't duplicated in a set, or (for
// debugging) that the order of the objects is reproducible.

// Examples:
// class A;
// typedef std::set<A*, DerefCompare<A>> SetA;
// typedef std::map<A*, int, DerefCompare<A>> MapAint;

template <class TYPE>
struct DerefCompare {
  bool operator()(const TYPE *a, const TYPE *b) const {
    return *a < *b;
  }
};

#endif // DEREFCOMPARE_H
