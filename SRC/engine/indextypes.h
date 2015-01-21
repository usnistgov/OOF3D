// -*- C++ -*-
// $RCSfile: indextypes.h,v $
// $Revision: 1.13.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef INDEXTYPES_H
#define INDEXTYPES_H

#include <iostream>

template <int N>
class IndexType {
private:
  int index;
public:
  IndexType() : index(0) {}
  IndexType(int i) : index(i) {}
  IndexType(const IndexType &other) : index(int(other)) {}
  operator int() const { return index; }
  IndexType &operator=(const IndexType &that) {
    index = that.index;
    return *this;
  }
  IndexType &operator=(int i) { index = i; return *this; }
  IndexType &operator++() { ++index; return *this; }
  friend bool operator==(const IndexType<N> &a, const IndexType<N> &b) {
    return a.index == b.index;
  }
  friend bool operator!=(const IndexType<N> &a, const IndexType<N> &b) {
    return a.index != b.index;
  }
  // the compiler might complain about ambiguous overloaded operators
  // unless these are defined explicitly:
  friend bool operator==(const IndexType<N> &a, int b) {return a.index == b;}
  friend bool operator==(int b, const IndexType<N> &a) {return a.index == b;}
  friend bool operator!=(const IndexType<N> &a, int b) {return a.index != b;}
  friend bool operator!=(int b, const IndexType<N> &a) {return a.index != b;}
};

template <int N>
std::ostream &operator<<(std::ostream &os, const IndexType<N> &i) {
  return os << int(i);
}

// typedef IndexType<0> NodeIndex;
typedef IndexType<1> SpaceIndex;
typedef IndexType<2> ShapeFunctionIndex;

#endif // INDEXTYPES_H
