// -*- C++ -*-
// $RCSfile: smallmatrix.h,v $
// $Revision: 1.1 $
// $Author: reida $
// $Date: 2006/12/07 14:02:35 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@ctcms.nist.gov. 
 */

#include <iostream>
#include <sstream>

// The "SmallMatrix" class is a general (i.e. not symmetric or
// positive-definite or anything) real-valued matrix which stores its
// data internally in column-ordered LAPACK-friendly format.  For
// maximum speed, routines which require "utility" linear-algebra
// operations should construct one of these directly.


#ifndef SMALLMATRIX_H
#define SMALLMATRIX_H

// This declaration will probably eventually be moved.
extern "C" {
  // Arguments: N, # of columns of A.
  //            NRHS, # of right-hand-sides to solve for.
  //            A, the matrix
  //            LDA, leading dimension of the array (# of rows)
  //            IPIV -- pivot-index array, one pivot per row.
  //            B, matrix of right-hand-sides.
  //            LDB, leading dimension of B.
  //            INFO, error-return variable.
  void dgesv_(int*n, int*nrhs, double*a, int*lda, int*ipiv,
	      double*b, int*ldb, int*info);
};

class ErrProgrammingError {
private: 
  std::string msg;
  std::string filename;
  int lineno;
public:
  ErrProgrammingError(std::string msg, std::string fn, int lno) :
    msg(msg), filename(fn), lineno(lno) {}
  friend std::ostream &operator<<(std::ostream &os, ErrProgrammingError &epe);
};

std::ostream &operator<<(std::ostream &os, ErrProgrammingError &epe);


class SmallMatrix {
private:
  int length, nrows, ncols;
  double *data;
public:
  SmallMatrix(int size);  // Makes a square one, not a vector.
  SmallMatrix(int rows, int cols);
  SmallMatrix(const SmallMatrix&);
  // SCPR purpose
  ~SmallMatrix();
  
  void clear();  // Encourage re-use of already-allocated objects.
  
  int rows() const { return nrows; }
  int cols() const { return ncols; }

  double &operator()(int row, int col);
  double operator()(int row, int col) const;

  SmallMatrix &operator=(const SmallMatrix&);

  SmallMatrix &operator+=(const SmallMatrix&);
  SmallMatrix &operator-=(const SmallMatrix&);
  SmallMatrix &operator*=(double);
  
  // Transpose in-place.
  void transpose();

  // The solve routine is fast, but corrupts the contents
  // of both the matrix and the passed-in rhs.  Matrix on which
  // "solve" is called must be square. 
  int solve(SmallMatrix&);

  friend SmallMatrix operator*(const SmallMatrix&, const SmallMatrix &);
};

SmallMatrix operator+(const SmallMatrix&, const SmallMatrix&);
SmallMatrix operator-(const SmallMatrix&, const SmallMatrix&);
SmallMatrix operator*(const SmallMatrix&, double);

#endif
