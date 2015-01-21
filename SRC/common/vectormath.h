// -*- C++ -*-
// $RCSfile: vectormath.h,v $
// $Revision: 1.1.4.4 $
// $Author: langer $
// $Date: 2014/09/16 00:42:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// Arithmetic operations on DoubleVec (aka std::vector<double>),
// implemented with BLAS.

#ifndef VECTORMATH_H
#define VECTORMATH_H

#include <vector>
#include <math.h>

class DoubleVec;

// In-place operations, using no temporaries

DoubleVec &axpy(double alpha, const DoubleVec &x, DoubleVec &y); // y += alpha*x
DoubleVec &operator+=(DoubleVec &x, const DoubleVec &y);
DoubleVec &operator-=(DoubleVec &x, const DoubleVec &y);
DoubleVec &scale(double alpha, DoubleVec &y);
DoubleVec &operator*=(DoubleVec&, double);
DoubleVec &operator/=(DoubleVec&, double);

// Non-in-place, which may return a temporary object.

DoubleVec operator+(const DoubleVec&, const DoubleVec&);
DoubleVec operator-(const DoubleVec&, const DoubleVec&);
DoubleVec operator*(const DoubleVec&, double);
DoubleVec operator*(double, const DoubleVec&);
DoubleVec operator/(const DoubleVec&, double);

// dot product

double dot(const DoubleVec&, const DoubleVec&);
double operator*(const DoubleVec&, const DoubleVec&);

// set all entries to 0
void zero(DoubleVec&);

#endif // VECTORMATH_H
