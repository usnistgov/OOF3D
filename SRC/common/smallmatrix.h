/// -*- C++ -*-
// $RCSfile: smallmatrix.h,v $
// $Revision: 1.8.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:43:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <iostream>

// The "SmallMatrix" class is a general (i.e. not symmetric or
// positive-definite or anything) real-valued matrix which stores its
// data internally in column-ordered LAPACK-friendly format.  For
// maximum speed, routines which require "utility" linear-algebra
// operations should construct one of these directly.


#ifndef SMALLMATRIX_H
#define SMALLMATRIX_H

#include "common/doublevec.h"

class Cijkl;

class SmallMatrix {
protected:
  unsigned int nrows, ncols;
  DoubleVec data;
public:
  SmallMatrix(unsigned int size); // Makes a square matrix, not a vector.
  SmallMatrix(unsigned int rows, unsigned int cols);
  SmallMatrix(const SmallMatrix&);
  SmallMatrix(const Cijkl*);	// for SCPR
  virtual ~SmallMatrix();
  
  void clear();  // Sets all entries to zero, doesn't resize.
  void resize(unsigned int rows, unsigned int cols);
  
  unsigned int rows() const { return nrows; }
  unsigned int cols() const { return ncols; }

  virtual double &operator()(unsigned int row, unsigned int col);
  virtual const double &operator()(unsigned int row, unsigned int col) const;

  SmallMatrix &operator=(const SmallMatrix&);

  SmallMatrix &operator+=(const SmallMatrix&);
  SmallMatrix &operator-=(const SmallMatrix&);
  SmallMatrix &operator*=(double);

  // Functions used by the python interface.  If we write the python
  // arithmetic operators in the 'obvious' way, then swig generates
  // code that copies the matrices more than necessary.  By swigging
  // these functions, we can eliminate the extra copies.
  void scale(double x) { *this *= x; }
  void madd(const SmallMatrix &other) { *this += other; }
  void msub(const SmallMatrix &other) { *this -= other; }

  // Transpose in-place.
  void transpose();

  // The solve routine is fast, but corrupts the contents
  // of both the matrix and the passed-in rhs.  Matrix on which
  // "solve" is called must be square.  Return value is 0 on success.
  int solve(SmallMatrix&);

  // Perform a local inverse, assuming that the matrix is symmetric.
  int symmetric_invert();

  friend SmallMatrix operator*(const SmallMatrix&, const SmallMatrix &);
  friend DoubleVec operator*(const SmallMatrix&, const DoubleVec&);
  friend DoubleVec operator+(const DoubleVec&, const SmallMatrix&);
  friend DoubleVec operator+(const SmallMatrix&, const DoubleVec&);
};

SmallMatrix operator+(const SmallMatrix&, const SmallMatrix&);
SmallMatrix operator-(const SmallMatrix&, const SmallMatrix&);
SmallMatrix operator*(const SmallMatrix&, double);

std::ostream &operator<<(std::ostream&, const SmallMatrix&);

#endif	// SMALLMATRIX_H
