// -*- C++ -*-
// $RCSfile: vectormath.C,v $
// $Revision: 1.1.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:43:01 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/printvec.h"
#include "common/doublevec.h"
#include "common/vectormath.h"

extern "C" {
  void daxpy_(const int *n, const double *alpha,
	      const double *x, const int *incx,
	      double *y, const int *incy);
  void dscal_(const int *n, const double *alpha, double *x, const int *incx);
  double ddot_(const int *n, const double *x, const int *incx,
	       const double *y, const int *incy);
};

// y += alpha*x

DoubleVec &axpy(double alpha, const DoubleVec &x, DoubleVec &y) {
#ifdef DEBUG
  if(x.size() != y.size())
    std::cerr << "axpy: size(x)=" << x.size() << " size(y)=" << y.size()
	      << std::endl;
#endif // DEBUG
  assert(x.size() == y.size());
  int one = 1;
  int n = x.size();
  daxpy_(&n, &alpha, &x[0], &one, &y[0], &one);
  return y;
}

// x + y

DoubleVec operator+(const DoubleVec &x, const DoubleVec &y) {
  DoubleVec result(x);
  return axpy(1.0, y, result);
}

// x += y

DoubleVec &operator+=(DoubleVec &x, const DoubleVec &y) {
  return axpy(1.0, y, x);
}

// x -= y

DoubleVec &operator-=(DoubleVec &x, const DoubleVec &y) {
  return axpy(-1.0, y, x);
}

// x - y

DoubleVec operator-(const DoubleVec &x, const DoubleVec &y) {
  DoubleVec result(x);
  return axpy(-1.0, y, result);
}

// y *= alpha

DoubleVec &scale(double alpha, DoubleVec &y) {
  int one = 1;
  int n =  y.size();
  dscal_(&n, &alpha, &y[0], &one);
  return y;
}

DoubleVec &operator*=(DoubleVec &y, double alpha) {
  return scale(alpha, y);
}

// y*alpha

DoubleVec operator*(const DoubleVec &y, double alpha) {
  DoubleVec result(y);
  return scale(alpha, result);
}

// alpha*y

DoubleVec operator*(double alpha, const DoubleVec &y) {
  DoubleVec result(y);
  return scale(alpha, result);
}

// y /= alpha

DoubleVec &operator/=(DoubleVec &y, double alpha) {
  return scale(1/alpha, y);
}

// y/alpha

DoubleVec operator/(const DoubleVec &y, double alpha) {
  DoubleVec result(y);
  return result /= alpha;
}

// dot product

double dot(const DoubleVec &x, const DoubleVec &y) {
  assert(x.size() == y.size());
  int one = 1;
  int n = x.size();
  return ddot_(&n, &x[0], &one, &y[0], &one);
}

double operator*(const DoubleVec &x, const DoubleVec &y) {
  return dot(x, y);
}

#include <string.h>

void zero(DoubleVec &x) {
  memset(&x[0], 0, x.size()*sizeof(double));
}
