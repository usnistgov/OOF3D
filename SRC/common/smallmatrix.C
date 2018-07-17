// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/coord.h"
#include "common/smallmatrix.h"

#include <string.h>

SmallMatrix::SmallMatrix(int size) : data(size, size) {
  data.setZero(size, size);
}

SmallMatrix::SmallMatrix(int rows, int cols) : data(rows, cols) {
  data.setZero(rows, cols);
}

void SmallMatrix::resize(int rows, int cols) {
  data.resize(rows, cols);
  data.setZero(rows, cols);
}

double& SmallMatrix::operator()(int row, int col) {
  assert(row >= 0 && col >= 0 && row < data.rows() && col < data.cols());
  return data.coeffRef(row, col);
}

const double &SmallMatrix::operator()(int row, int col) const 
{
  assert(row >= 0 && col >= 0 && row < data.rows() && col < data.cols());
  return data.coeffRef(row, col);
}

SmallMatrix& SmallMatrix::operator+=(const SmallMatrix &other) {
  data += other.data;
  return *this;
}

SmallMatrix& SmallMatrix::operator-=(const SmallMatrix &other) {
  data -= other.data;
  return *this;
}

SmallMatrix& SmallMatrix::operator*=(double x) {
  data *= x;
  return *this;
}

SmallMatrix SmallMatrix::operator+(const SmallMatrix &other) const {
  SmallMatrix tmp;
  tmp.data = data + other.data;
  return tmp;
}

SmallMatrix SmallMatrix::operator-(const SmallMatrix &other) const {
  SmallMatrix tmp;
  tmp.data = data - other.data;
  return tmp;
}

// Matrix * scalar
SmallMatrix SmallMatrix::operator*(double x) const {
  SmallMatrix tmp;
  tmp.data = data * x;
  return tmp;
}

// Matrix * Matrix
SmallMatrix SmallMatrix::operator*(const SmallMatrix& other) const {
  SmallMatrix tmp;
  tmp.data = data * other.data;
  return tmp;
}

// Matrix * vector
DoubleVec SmallMatrix::operator*(const DoubleVec& other) const {
  DoubleVec tmp;
  tmp.data = data * other.data;
  return tmp;
}

// Matrix * Coord3D
Coord3D SmallMatrix::operator*(const Coord3D &other) const {
  assert(rows() == 3 && cols() == 3);
  // TODO: Does this do more copying than necessary?  Can Eigen be
  // made to work with a Coord3D directly?
  Eigen::VectorXd othr;
  othr << other[0], other[1], other[2]; // Eigen overloads the comma operator.
  Eigen::MatrixXd result = data*othr;
  return Coord3D(result(0,0), result(1,0), result(2,0));
}

// In-place transposition. Only works for square matrices.
void SmallMatrix::transpose() {
  data.transposeInPlace();
}

int SmallMatrix::solve(SmallMatrix &rhs) const {
  // This routine modifies the contents both of the "host" matrix
  // and the passed-in rhs.  
  rhs.data = data.fullPivLu().solve(rhs.data);

  //TODO(lizhong): remove return value
  return 0;
}

int SmallMatrix::symmetric_invert() {
  data = data.inverse();

  //TODO(lizhong): remove return value
  return 0;
}


//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//

std::ostream& operator<<(std::ostream &os, const SmallMatrix& mat) {
  for(int i=0; i<mat.rows(); i++) {
    for(int j=0; j<mat.cols(); j++) 
      os << " " << mat(i,j);
    os << std::endl;
  }
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#include "common/sincos.h"

SmallMatrix rotateAboutAxis(double angle, const Coord3D &axis) {
  SmallMatrix R(3);
  double cosA, sinA;
  sincos(angle, sinA, cosA);
  double omcosA = 1.0 - cosA;
  // This formula was copied from https://en.wikipedia.org/wiki/Rotation_matrix
  R(0,0) = cosA + axis[0]*axis[0]*omcosA;
  R(0,1) = axis[0]*axis[1]*omcosA - axis[2]*sinA;
  R(0,2) = axis[0]*axis[2]*omcosA + axis[1]*sinA;
  R(1,0) = axis[1]*axis[0]*omcosA + axis[2]*sinA;
  R(1,1) = cosA + axis[1]*axis[1]*omcosA;
  R(1,2) = axis[1]*axis[2]*omcosA - axis[0]*sinA;
  R(2,0) = axis[2]*axis[0]*omcosA - axis[1]*sinA;
  R(2,1) = axis[2]*axis[1]*omcosA + axis[0]*sinA;
  R(2,2) = cosA + axis[2]*axis[2]*omcosA;
  return R;
}
