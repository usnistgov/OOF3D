/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SMALLMATRIX_H
#define SMALLMATRIX_H

#include <oofconfig.h>
#include <iostream>

#include "common/doublevec.h"
#include "eigen/Eigen/Dense"

class Coord3D;

// The "SmallMatrix" class is a general (i.e. not symmetric or
// positive-definite or anything) real-valued dense matrix.

class SmallMatrix {
protected:
  Eigen::MatrixXd data;
public:
  SmallMatrix() : data(0, 0) {}
  SmallMatrix(int size);
  SmallMatrix(int rows, int cols); 
  SmallMatrix(const SmallMatrix& other) : data(other.data) {}
  virtual ~SmallMatrix() {}

  /* Matrix property methods */

  void resize(int rows, int cols);
  int rows() const { return data.rows(); }
  int cols() const { return data.cols(); }
  void clear() { data.setZero(data.rows(), data.cols()); }
  virtual double& operator()(int row, int col);
  virtual const double& operator()(int row, int col) const;

  /* Arithmetic operations */

  SmallMatrix& operator+=(const SmallMatrix&);
  SmallMatrix& operator-=(const SmallMatrix&);
  SmallMatrix& operator*=(double);
  SmallMatrix operator+(const SmallMatrix&) const;
  SmallMatrix operator-(const SmallMatrix&) const;
  SmallMatrix operator*(double) const;
  SmallMatrix operator*(const SmallMatrix&) const;
  DoubleVec operator*(const DoubleVec&) const;
  Coord3D operator*(const Coord3D&) const;

  void transpose();  // Transpose in-place.
  double norm() { return data.norm(); }

  // The solve routine is fast, but corrupts the contents
  // of both the matrix and the passed-in rhs.  Matrix on which
  // "solve" is called must be square.  Return value is 0 on success.
  int solve(SmallMatrix&) const;

  // Perform a local inverse, assuming that the matrix is symmetric.
  int symmetric_invert();

  // Functions used by the python interface.  If we write the python
  // arithmetic operators in the 'obvious' way, then swig generates
  // code that copies the matrices more than necessary.  By swigging
  // these functions, we can eliminate the extra copies.
  void scale(double x) { data *= x; }
  void madd(const SmallMatrix& other) { data += other.data; }
  void msub(const SmallMatrix& other) { data -= other.data; }
};

std::ostream &operator<<(std::ostream&, const SmallMatrix&);

// Generate a 3x3 rotation matrix.
SmallMatrix rotateAboutAxis(double, const Coord3D&);

#endif	// SMALLMATRIX_H
