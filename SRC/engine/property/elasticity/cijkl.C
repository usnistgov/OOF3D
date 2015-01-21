// -*- C++ -*-
// $RCSfile: cijkl.C,v $
// $Revision: 1.13.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:27 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>


#include "cijkl.h"
#include "common/corientation.h"
#include "common/doublevec.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "engine/fieldindex.h"
#include "engine/ooferror.h"
#include <iostream>

// ----------------------------------------------------------- //

double &Cijkl::operator()(int i, int j, int k, int l) {
  return c(SymTensorIndex(i, j).integer(), SymTensorIndex(k, l).integer());
}

double Cijkl::operator()(int i, int j, int k, int l) const {
  return c(SymTensorIndex(i, j).integer(), SymTensorIndex(k, l).integer());
}

double &Cijkl::operator()(const SymTensorIndex &a, const SymTensorIndex &b) {
  return c(a.integer(), b.integer());
}

double Cijkl::operator()(const SymTensorIndex &a, const SymTensorIndex &b) const
{
  return c(a.integer(), b.integer());
}

double &Cijkl::operator()(int ij, int kl) {
  return c(ij, kl);
}

double Cijkl::operator()(int ij, int kl) const {
  return c(ij, kl);
}

// ----------------------------------------------------------- //

// A is a rotation matrix which, when right-multiplied by 
// a crystal-coordinate vector, gives a lab-coordinate vector.
Cijkl Cijkl::transform(const COrientation *orient) const {
  SmallMatrix A = orient->rotation();
  Cijkl B;
  /* should use partial sums to speed this up */
  for(int i=0; i<3; i++)
    for(int j=0; j<=i; j++)
      for(int k=0; k<3; k++)  /* k<=i ? */
 	for(int l=0; l<=k; l++) {
 	  double &b = B(i, j, k, l);
 	  b = 0.0;
 	  for(int ii=0; ii<3; ii++)
 	    for(int jj=0; jj<3; jj++)
 	      for(int kk=0; kk<3; kk++)
 		for(int ll=0; ll<3; ll++)
 		  b += A(i, ii)*A(j, jj)*A(k, kk)*A(l, ll)*
		    (*this)(ii, jj, kk, ll);
 	}
  return B;
}

// This version doesn't work because at the first iteration
// B1(ijkl) != B1(ijlk), so it can't be stored in a Cijkl. The symmetry
// should be taken advantage of...

// Cijkl Cijkl::transform(const MV_ColMat_double &A) const {
//   Cijkl B, B1;
//   int i, ii, j, jj, k, kk, l, ll;
  
//   for(i=0; i<3; i++)
//     for(j=0; j<3; j++)
//       for(k=0; k<3; k++)
// 	for(ll=0; ll<3; ll++) {
// 	  double &b = B1(i, j, k, ll);
// 	  for(l=0; l<3; l++)
// 	    b += A(l, ll)*(*this)(i, j, k, l);
// 	}

//   for(i=0; i<3; i++)
//     for(j=0; j<3; j++)
//       for(kk=0; kk<3; kk++)
// 	for(ll=0; ll<3; ll++) {
// 	  double &b = B(i, j, kk, ll);
// 	  for(k=0; k<3; k++)
// 	    b += A(k, kk)*B1(i, j, k, ll);
// 	}

//   for(i=0; i<3; i++)
//     for(jj=0; jj<3; jj++)
//       for(kk=0; kk<3; kk++)
// 	for(ll=0; ll<3; ll++) {
// 	  double &b = B1(i, jj, kk, ll);
// 	  for(j=0; j<3; j++)
// 	    b += A(j, jj)*B(i, j, kk, ll);
// 	}

//   for(ii=0; ii<3; ii++)
//     for(jj=0; jj<3; jj++)
//       for(kk=0; kk<3; kk++)
// 	for(ll=0; ll<3; ll++) {
// 	  double &b = B(ii, jj, kk, ll);
// 	  for(i=0; i<3; i++)
// 	    b += A(i, ii)*B1(i, jj, kk, ll);
// 	}
//   return B;
// }


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const Cijkl &cijkl) {
  return os << cijkl.c;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Tensor multiplication C_ijkl * M_kl

SymmMatrix3 operator*(const Cijkl &cijkl, const SymmMatrix3 &m) {
  if(m.size() != 3) {
    throw ErrProgrammingError("Incompatible matrix size", __FILE__, __LINE__);
  }
  DoubleVec mv(6);
  mv[0] = m(0,0);
  mv[1] = m(1,1);
  mv[2] = m(2,2);
  mv[3] = 2*m(1,2);
  mv[4] = 2*m(0,2);
  mv[5] = 2*m(0,1);
  DoubleVec rv(cijkl.c * mv);
  SymmMatrix3 product;
  product(0,0) = rv[0];
  product(1,1) = rv[1];
  product(2,2) = rv[2];
  product(1,2) = rv[3];
  product(0,2) = rv[4];
  product(0,1) = rv[5];
  return product;
}
