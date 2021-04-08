// -*- C++ -*-
// $RCSfile: symmmatrix.C,v $
// $Revision: 1.37.10.3 $
// $Author: langer $
// $Date: 2014/04/15 19:35:02 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */
#include <oofconfig.h>

#include "common/coord.h"
#include "common/corientation.h"
#include "common/doublevec.h"
#include "common/ooferror.h"
#include "engine/fieldindex.h"
#include "engine/ooferror.h"
#include "engine/symeig3.h"
#include "engine/symmmatrix.h"
#include <iomanip>
#include <iostream>

// construct an n by n matrix

SymmMatrix::SymmMatrix(int n) : m(0), nrows(n) {
  allocate();
}

// copy constructor

SymmMatrix::SymmMatrix(const SymmMatrix& sm) : m(0), nrows(sm.nrows) {
  allocate();
  copy(sm.m);
}
    
SymmMatrix::~SymmMatrix() {
//   std::cerr << "SymmMatrix::~SymmMatrix" << this << std::endl;
  free();    
}

// assignment

SymmMatrix& SymmMatrix::operator=(const SymmMatrix& sm) {
  if(&sm != this) {
    if(nrows != sm.nrows) {
      free();
      nrows = sm.nrows;
      allocate();
    }
    copy(sm.m);
  }
  return *this;
}

// Equality.

bool SymmMatrix::operator==(const SymmMatrix& that) {
  // If our counterpart is us, we're equal.
  if (this==&that)
    return true;
  
  // Distinct SymmMatrices of different sizes are always unequal.
  if (nrows != that.nrows) 
    return false;

  unsigned int sz = nrows*(nrows+1)/2;
  double *here = *m;
  double *there = *that.m;
  
  for(unsigned int i=0;i<sz;i++) 
    if (here[i]!=there[i])
      return false;
  return true;
}

// access

double SymmMatrix::operator()(int i, int j) const {
#ifdef DEBUG
  if(i >= int(nrows) || j >= int(nrows) || i<0 || j<0) {
    std::cerr << "SymmMatrix error: i=" << i << " j=" << j
	      << " nrows=" << nrows << std::endl;
    abort();
  }
#endif
//   std::cerr << "SymmMatrix::operator()(" << i << ", " << j << ") const " << this << std::endl;
  if(i > j) return m[i][j];	// as stored
  return m[j][i];		// transpose
}

double &SymmMatrix::operator()(int i, int j) {
#ifdef DEBUG
  if(i >= int(nrows) || j >= int(nrows) || i<0 || j<0) {
    std::cerr << "SymmMatrix error: i=" << i << " j=" << j
	      << " nrows=" << nrows<< std::endl;
    abort();
  }
#endif
//   std::cerr << "SymmMatrix::operator()(" << i << ", " << j << ") " << this << std::endl;
  if(i > j) return m[i][j];	// as stored
  return m[j][i];		// transpose
}

SmallMatrix operator*(const SymmMatrix &a, const SymmMatrix &b) {
  if(a.nrows != b.nrows) abort();
  unsigned int nrows = a.nrows;
  SmallMatrix result(nrows, nrows);
  for(unsigned int i=0; i<nrows; i++) {
    for(unsigned int j=0; j<nrows; j++) {
      double &r = result(i, j);
      for(unsigned int k=0; k<nrows; k++)
	r += a(i, k) * b(k, j);
    }
  }
  return result;
}

SymmMatrix &SymmMatrix::operator+=(const SymmMatrix &a) {
  unsigned int sz = nrows*(nrows+1)/2;
  double *here = *m;
  double *there = *a.m;
  for(unsigned int i=0; i<sz; i++)
    here[i] += there[i];
  return *this;
}

SymmMatrix &SymmMatrix::operator-=(const SymmMatrix &a) {
  unsigned int sz = nrows*(nrows+1)/2;
  double *here = *m;
  double *there = *a.m;
  for(unsigned int i=0; i<sz; i++)
    here[i] -= there[i];
  return *this;
}

DoubleVec operator*(const SymmMatrix &a, const DoubleVec &x) {
  unsigned int nrows = a.nrows;
  if(x.size() != nrows) abort();
  DoubleVec result(nrows, 0.);
  for(unsigned int i=0; i<nrows; i++) {
    double &r = result[i];
    for(unsigned int j=0; j<nrows; j++)
      r += a(i,j)*x[j];
  }
  return result;
}

// Compute A^ T (*this) A

/*
SymmMatrix SymmMatrix::transform(const MV_ColMat_double &A) const {
  if(A.size(0) != nrows) abort();
  SymmMatrix result(nrows);
  MV_ColMat_double temp(nrows, nrows, 0.0);
  int i, j, k, l;
  for(j=0; j<nrows; j++)
    for(k=0; k<nrows; k++) {
      double &t = temp(j, k);
      for(l=0; l<nrows; l++)
	t += A(j, l)*m[k][l];
    }
  for(i=0; i<nrows; i++)
    for(j=0; j<=i; j++) {
      double &r = result(i, j);
      for(k=0; k<nrows; k++)
	r += temp(j, k)*A(i, k);
    }
  return result;
}
*/

SymmMatrix SymmMatrix::transform(const COrientation *orient) const {
  SmallMatrix A = orient->rotation();
  assert(A.rows() == nrows);
  SymmMatrix result(nrows);
  for(unsigned int i=0; i<nrows; i++) {
    for(unsigned int j=0; j<=i; j++) {
      double &r = result(i,j);
      for(unsigned int k=0; k<nrows; k++)
 	for(unsigned int l=0; l<nrows; l++)
 	  r += A(i, k) * (*this)(k, l) * A(j, l);
    }
  }
  return result;
}

SymmMatrix operator*(double x, const SymmMatrix &A) {
  SymmMatrix result(A);
  result *= x;
  return result;
}

SymmMatrix operator*(const SymmMatrix &A, double x) {
  SymmMatrix result(A);
  result *= x;
  return result;
}

extern "C" {
  void dscal_(int*, double*, double*, int*);
}

SymmMatrix &SymmMatrix::operator*=(double x) {
  int n = (nrows*(nrows+1))/2;
  int one = 1;
  dscal_(&n, &x, m[0], &one);
  return *this;
}

SymmMatrix &SymmMatrix::operator/=(double x) {
  return operator*=(1./x);
}

SymmMatrix operator/(const SymmMatrix &A, double x) {
  SymmMatrix result(A);
  result *= 1./x;
  return result;
}

// allocate and free storage

void SymmMatrix::allocate() {   // assumes nrows has already been set
  if(m) {
    throw ErrProgrammingError("Reallocating SymmMatrix",
			      __FILE__, __LINE__);
  }
  m = new double*[nrows];	    // Allocate the pointers to the rows
  unsigned int sz = nrows*(nrows+1)/2;
  // Allocate all space contiguously
  double *u = m[0] = new double[sz];
  unsigned int i;
  for(i = 1; i<nrows; i++)
    m[i] = m[i-1] + i; // Sets the row pointers   	
  for(i = 0; i<sz; i++)
    u[i] = 0;
}

void SymmMatrix::free() {
  if(nrows != 0) {
    delete [] m[0];	// delete data storage
    delete [] m;	// delete pointers to rows
  }
  m = 0;
}

void SymmMatrix::copy(double **smd) {	// copy data from another data array
  unsigned int sz = nrows*(nrows+1)/2;
  (void) memcpy(&m[0][0], &smd[0][0], sz*sizeof(double));
}

void SymmMatrix::resize(unsigned int n) {
  if(n == nrows) return;
  free();
  nrows = n;
  allocate();
}

std::ostream& operator<<(std::ostream& os, const SymmMatrix &sm) {
  os.setf(std::ios::scientific, std::ios::floatfield);
  os << "[ ";
  for(unsigned int i=0; i<sm.nrows; i++) {
    for(unsigned int j=i; j<sm.nrows; j++)
      os << std::setw(13) << sm(i, j) << " ";
    if(i != sm.nrows-1)
      os << "; ";
  }
  os << "]";
  return os;
}

void SymmMatrix::clear(double x) {
  for(unsigned int i=0; i<nrows; i++)
    for(unsigned int j=0; j<=i; j++)
      m[i][j] = x;
}

