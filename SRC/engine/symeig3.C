// -*- C++ -*-
// $RCSfile: symeig3.C,v $
// $Revision: 1.4.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// Eigenvalues and eigenvectors of a symmetric 3x3 matrix

#ifndef SYMEIG_C
#define SYMEIG_C

#include <math.h>
#include <iostream>

#include "engine/eigenvalues.h"
#include "engine/symeig3.h"

static const double thirdtwopi = 2*M_PI/3;

template <class MATRIX>
void swaprows(MATRIX &m, int i, int j) {
  for(int k=0; k<3; k++) {
    double temp = m(i,k);
    m(i,k) = m(j,k);
    m(j,k) = temp;
  }
}

template <class MATRIX>
void swapcols(MATRIX &m, int i, int j) {
  for(int k=0; k<3; k++) {
    double temp = m(k,i);
    m(k,i) = m(k,j);
    m(k,j) = temp;
  }
}

template <class MATRIX, class NEWMATRIX>
void setm(const MATRIX &mat, NEWMATRIX &m, double lambda) {
  m(0,0) = mat(0,0) - lambda;
  m(0,1) = m(1,0) = mat(0,1);
  m(0,2) = m(2,0) = mat(0,2);
  m(1,1) = mat(1,1) - lambda;
  m(1,2) = m(2,1) = mat(1,2);
  m(2,2) = mat(2,2) - lambda;
}

template <class MATRIX, class EIGENVECTOR>
void eigensystem(const MATRIX &mat,
		 EIGENVECTOR &eig1, EIGENVECTOR &eig2, EIGENVECTOR &eig3)
{
  EigenValues eig;
  eigenvalues(mat, eig);

  double x00, x01, x02;		// components of eigenvector 0
  double x10, x11, x12;		// components of eigenvector 1
  double x20, x21, x22;		// components of eigenvector 2

  // find first eigenvector

  // construct A-lambda*I
  MATRIX m(3,3);
  setm(mat, m, eig.max());
  // std::cerr << "original m" << std::endl << m << std::endl;

  // make sure that m00 is nonzero
  if(m(0,0) == 0) {
    if(m(0,1) != 0)
      swaprows(m, 0, 1);
    else if(m(0,2) != 0)
      swaprows(m, 0, 2);
    else {
      // every element in first column (and row) is zero
      x00 = 1.0;
      if(m(1,1) != 0) {
	x01 = -m(1,2)/m(1,1);
	x02 = 1.0;
      }
      else if(m(2,2) != 0) {
	x01 = 1.0;
	x02 = -m(1,2)/m(2,2);
      }
      else {			// m11 = m22 = 0
	x01 = 0.0;
	x02 = 0.0;
      }
    }
  }
  // std::cerr << "swapped m" << std::endl << m << std::endl;
  if(m(0,0) != 0.0) {		// m(0,0) == 0 has been dealt with above
    // make m(0,0) = 1
    m(0,1) /= m(0,0);
    m(0,2) /= m(0,0);
    m(0,0) = 1.0;
    for(int i=1; i<3; i++) {	// Gaussian elimination on first column
      // multiply top row by m(i,0) and subtract from i^th row
      m(i,1) -= m(i,0)*m(0,1);
      m(i,2) -= m(i,0)*m(0,2);
      m(i,0) = 0.0;
    }
    //std::cerr << "gaussian eliminated m" << std::endl << m << std::endl;
    
    // matrix is now of the form
    //     1  m01  m02
    //     0  m11  m12
    //     0  m21  m22
    // so we can get the ratio x01/x02, then use the top row to solve
    // for x00.
    //
    // The last two rows must be linearly dependent, but may be 0 0 0.
    // If one of these 0's is non-zero only because of roundoff, we'll get
    // the wrong answer. Ie:
    //    1   m01     m02
    //    0   3       2
    //    0   1.e-16  2.e-16
    // will give the wrong answer if we use the bottom row.
    
    // swap rows if necessary so that the maximum of m11, m12, m21,
    // and m22 is in the bottom row
    double max = fabs(m(1,1));
    int which = 1;		// row containing max
    if(fabs(m(1,2)) > max) max = fabs(m(1,2));
    if(fabs(m(2,1)) > max) { max = fabs(m(2,1)); which = 2; }
    if(fabs(m(2,2)) > max) which = 2;
    if(which == 1)
	swaprows(m, 1, 2);

    //std::cerr << "reswapped m" << std::endl << m << std::endl;
    
    if(m(2,2) != 0.0) {
      x01 = 1.0;
      x02 = -m(2,1)/m(2,2);
    }
    else if(m(2,1) != 0.0) {
      x02 = 1.0;
      x01 = -m(2,2)/m(2,1);
    }
    else {			// all m11, m12, m21, m22 are zero
      x01 = 0.0;		// arbitrary choice
      x02 = 1.0;
    }
    x00 = -m(0,1)*x01 - m(0,2)*x02;
  }
  // normalize
  double norm = 1./sqrt(x00*x00 + x01*x01 + x02*x02);
  x00 *= norm;
  x01 *= norm;
  x02 *= norm;

  // find second eigenvector orthogonal to the first
  setm(mat, m, eig.mid());
  // reorder columns so that x02 is the component with the largest
  // absolute value, so that we can divide by it safely.
  double max = fabs(x00);
  int swappedwith = 0;
  if(fabs(x01) > max) { max = fabs(x01); swappedwith = 1; }
  if(fabs(x02) > max) { max = fabs(x02); swappedwith = 2; }
  if(swappedwith == 1) {
      swapcols(m, 1, 2);
      double temp = x02;
      x02 = x01;
      x01 = temp;
    }
  else if(swappedwith == 0) {
    swapcols(m, 0, 2);
    double temp = x02;
    x02 = x00;
    x00 = temp;
  }

  // solve m(j,0)*x10 + m(j,1)*x11 + m(j,2)*x12 = 0,
  // with x00*x10 + x01*x11 + x02*x12 = 0
  // solve for x12 in the second eqn, plug into the first, multiply
  // through by x02, and get
  // a_j*x10 + b_j*x11 = 0
  // with a_j = m(j,0)*x02 - m(j,2)*x00
  //      b_j = m(j,1)*x02 - m(j,2)*x01
  // Choose the pair (a_j, b_j) with the largest absolute value in it,
  // for the same reasons given above.
  double a[3], b[3];
  max = 0;
  int which = 0;
  for(int k=0; k<3; k++) {
    a[k] = m(k,0)*x02 - m(k,2)*x00;
    b[k] = m(k,1)*x02 - m(k,2)*x01;
    if(fabs(a[k]) > max) { max = fabs(a[k]); which = k; }
    if(fabs(b[k]) > max) { max = fabs(b[k]); which = k; }
  }
  //  std::cerr << "a=" << a[which] << " b=" << b[which] << std::endl;
  double amax = a[which];
  double bmax = b[which];
  if(amax != 0) {
    x11 = 1.0;
    x10 = -bmax/amax;
  }
  else if(bmax != 0) {
    x10 = 1.0;
    x11 = -amax/bmax;
  }
  else {
    x10 = 1.0;			// arbitrary choice
    x11 = 0.0;
  }
  x12 = -(x00*x10 + x01*x11)/x02;
  norm = 1/sqrt(x10*x10 + x11*x11 + x12*x12);
  x10 *= norm;
  x11 *= norm;
  x12 *= norm;
  // fix order if columns of m were swapped
  if(swappedwith == 0) {
    double temp = x12;
    x12 = x10;
    x10 = temp;
    temp = x02;
    x02 = x00;
    x00 = temp;
  }
  else if(swappedwith == 1) {
    double temp = x12;
    x12 = x11;
    x11 = temp;
    temp = x02;
    x02 = x01;
    x01 = temp;
  }

  // find third eigenvector orthogonal to first two
  x20 = x01*x12 - x02*x11;
  x21 = x02*x10 - x00*x12;
  x22 = x00*x11 - x01*x10;

  eig1 = EIGENVECTOR(eig.max(), x00, x01, x02);
  eig2 = EIGENVECTOR(eig.mid(), x10, x11, x12);
  eig3 = EIGENVECTOR(eig.min(), x20, x21, x22);
}

template <class MATRIX>
void getEigenvalues(const MATRIX &mat, EigenValues &eig) {
  double a00 = mat(0,0);
  double a01 = mat(0,1);
  double a02 = mat(0,2);
  double a11 = mat(1,1);
  double a12 = mat(1,2);
  double a22 = mat(2,2);

  // coeffiecients of the characteristic equation
  // lambda^3 + a*lambda^2 + b*lambda + c = 0
  double a = -(a00 + a11 + a22);
  double b = -(a01*a01 + a02*a02 + a12*a12 - a00*a11 - a00*a22 - a11*a22);
  double c = -(a00*(a11*a22 - a12*a12) +
	       a01*(a02*a12 - a22*a01) +
	       a02*(a01*a12 - a11*a02));

  double asq = a*a;
  double Q = (asq - 3*b)/9;
  if(Q <= 0.0) {		// could be negative only via roundoff error
    eig = EigenValues(-a/3, -a/3, -a/3);
    return;
  }
  double sqrtQ = sqrt(Q);
  double R = (2*asq*a - 9*a*b + 27*c)/54;
  double RQ = R/(sqrtQ*sqrtQ*sqrtQ);
  if(RQ > 1.0) RQ = 1.0;	// check for roundoff errors
  if(RQ < -1.0) RQ = -1.0;
  double theta = acos(RQ);
  
  double thirda = a/3;
  double thirdtheta = theta/3;
  eig = EigenValues(-2*sqrtQ*cos(thirdtheta) - thirda,
		    -2*sqrtQ*cos(thirdtheta + thirdtwopi) - thirda,
		    -2*sqrtQ*cos(thirdtheta - thirdtwopi) - thirda);
}


#endif // SYMEIG_C
