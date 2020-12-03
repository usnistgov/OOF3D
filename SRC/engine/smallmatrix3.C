// -*- C++ -*-
// $RCSfile: smallmatrix.C,v $
// $Revision: 1.9.4.4 $
// $Author: langer $
// $Date: 2014/10/15 20:53:44 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/smallmatrix.h"
#include "common/vectormath.h"
#include "common/ooferror.h"
#include "common/tostring.h"
#include "common/vectormath.h"
#include "engine/smallmatrix3.h"
#include <string.h>		// for memset


void SmallMatrix3::resize(unsigned int r, unsigned int c) {
  throw ErrProgrammingError("Attempt to resize SmallMatrix3.",
			    __FILE__,__LINE__);
}

// Inverts SmallMatrix3 "manually".
// Now a method of the SmallMatrix3 subclass.
// TODO:
// Should it use the use dgetrf/dgetri, to avoid the determinant?
// Our determinants are near unity, so we are probably OK.
// SmallMatrix has a "symmetric_invert" routine already, but that
// requires the matrix to be symmetric.
// 
// Method cribbed from:
// http://www.mathcentre.ac.uk/resources/uploaded/sigma-matrices11-2009-1.pdf
SmallMatrix3 SmallMatrix3::invert() const {
  SmallMatrix3 res;
  // Cofactors.
  // Data array index is col*3+row, due to Fortran ordering.
  // res(0,0) = x(1,1)*x(2,2)-x(1,2)*x(2,1);
  res(0,0) = data[4]*data[8]-data[7]*data[5];
  // res(0,1) = -(x(1,0)*x(2,2)-x(1,2)*x(2,0));
  res(0,1) = -data[1]*data[8]+data[7]*data[2];
  // res(0,2) = x(1,0)*x(2,1)-x(1,1)*x(2,0);
  res(0,2) = data[1]*data[5]-data[4]*data[2];
  //
  // res(1,0) = -(x(0,1)*x(2,2)-x(0,2)*x(2,1));
  res(1,0) = -data[3]*data[8]+data[6]*data[5];
  // res(1,1) = x(0,0)*x(2,2)-x(0,2)*x(2,0);
  res(1,1) = data[0]*data[8]-data[6]*data[2];
  // res(1,2) = -(x(0,0)*x(2,1)-x(0,1)*x(2,0));
  res(1,2) = -data[0]*data[5]+data[3]*data[2];
  //
  // res(2,0) = x(0,1)*x(1,2)-x(0,2)*x(1,1);
  res(2,0) = data[3]*data[7]-data[6]*data[4];
  // res(2,1) = -(x(0,0)*x(1,2)-x(0,2)*x(1,0));
  res(2,1) = -data[0]*data[7]+data[6]*data[1];
  // res(2,2) = x(0,0)*x(1,1)-x(0,1)*x(1,0);
  res(2,2) = data[0]*data[4]-data[3]*data[1];
  //
  double dtmt = data[0]*res(0,0)+data[3]*res(0,1)+data[6]*res(0,2);
  //
  // Inverse is adjoint divided by determinant.
  res.transpose();
  //
  return res*(1.0/dtmt);
}


double SmallMatrix3::det() const {
  SmallMatrix3 res;
  // Cofactors.  Data array index is col*3+row, due to Fortran ordering.
  // res(0,0) = x(1,1)*x(2,2)-x(1,2)*x(2,1);
  res(0,0) = data[4]*data[8]-data[7]*data[5];
  // res(0,1) = -(x(1,0)*x(2,2)-x(1,2)*x(2,0));
  res(0,1) = -data[1]*data[8]+data[7]*data[2];
  // res(0,2) = x(1,0)*x(2,1)-x(1,1)*x(2,0);
  res(0,2) = data[1]*data[5]-data[4]*data[2];
  //
  // res(1,0) = -(x(0,1)*x(2,2)-x(0,2)*x(2,1));
  res(1,0) = -data[3]*data[8]+data[6]*data[5];
  // res(1,1) = x(0,0)*x(2,2)-x(0,2)*x(2,0);
  res(1,1) = data[0]*data[8]-data[6]*data[2];
  // res(1,2) = -(x(0,0)*x(2,1)-x(0,1)*x(2,0));
  res(1,2) = -data[0]*data[5]+data[3]*data[2];
  //
  // res(2,0) = x(0,1)*x(1,2)-x(0,2)*x(1,1);
  res(2,0) = data[3]*data[7]-data[6]*data[4];
  // res(2,1) = -(x(0,0)*x(1,2)-x(0,2)*x(1,0));
  res(2,1) = -data[0]*data[7]+data[6]*data[1];
  // res(2,2) = x(0,0)*x(1,1)-x(0,1)*x(1,0);
  res(2,2) = data[0]*data[4]-data[3]*data[1];
  //
  return  data[0]*res(0,0)+data[3]*res(0,1)+data[6]*res(0,2);
}


std::pair<SmallMatrix3,SmallMatrix3> SmallMatrix3::sqrt() const {

// Compile-time element retrieval wtih no bounds checking.
#define DATA(r,c) data[c*3+r]
  
  SmallMatrix3 u_res,r_res;
  SmallMatrix3 ident;
  ident.clear();
  ident(0,0)=1.0; ident(1,1)=1.0; ident(2,2)=1.0;

  // TODO: Unroll this and use the DATA macro? Probable speedup.
  SmallMatrix3 c2 = (*this)*(*this);
  double o3 = 1.0/3.0;
  double root3 = pow(3.0,0.5);
        
  double c1212 = DATA(0,1)*DATA(0,1);
  double c1313 = DATA(0,2)*DATA(0,2);
  double c2323 = DATA(1,2)*DATA(1,2);
  double c2313 = DATA(1,2)*DATA(0,2);
  double c1223 = DATA(0,1)*DATA(1,2);
  double s11 = DATA(1,1)*DATA(2,2)-c2323;
  double ui1 = o3*(DATA(0,0)+DATA(1,1)+DATA(2,2));
  double ui2 = s11+DATA(0,0)*DATA(1,1)+DATA(2,2)*DATA(0,0)-c1212-c1313;
  double ui3 = DATA(0,0)*s11+DATA(0,1)*(c2313-DATA(0,1)*DATA(2,2))+DATA(0,2)*(c1223-DATA(1,1)*DATA(0,2));
  double ui1s = ui1*ui1;
  double q = pow(-fmin((o3*ui2-ui1s),0.0),0.5);
  double r = 0.5*(ui3-ui1*ui2)+ui1*ui1s;
  double xmod = q*q*q;

  double sign;
  if (xmod-1.0e30 > 0.0)  // TODO: Double-check the magic number here.
    sign = 1.0;
  else
    sign = -1.0;
  
  double scl1 = 0.5 + 0.5*sign;
  
  if (xmod-std::abs(r) > 0.0)
    sign = 1.0;
  else
    sign = -1.0;
  
  double scl2 = 0.5 + 0.5*sign;
  double scl0 = fmin(scl1,scl2);
  scl1 = 1.0 - scl0;

  double xmodscl1;
  if(scl1 == 0)
    xmodscl1 = xmod;
  else
    xmodscl1=xmod+scl1;
  
  double sdetm = acos(r/(xmodscl1))*o3;
  
  q = scl0*q;
  double ct3=q*cos(sdetm);
  double st3=q*root3*sin(sdetm);
  sdetm = scl1*pow(fmax(0.0,r),0.5);
  double aa = 2.0*(ct3+sdetm)+ui1;
  double bb = -ct3+st3-sdetm+ui1;
  double cc = -ct3-st3-sdetm+ui1;
  double lamda1 = pow(fmax(aa,0.0),0.5);
  double lamda2 = pow(fmax(bb,0.0),0.5);
  double lamda3 = pow(fmax(cc,0.0),0.5);
  
  double Iu = lamda1 + lamda2 + lamda3;
  double IIu = lamda1*lamda2 + lamda1*lamda3 + lamda2*lamda3;
  double IIIu = lamda1*lamda2*lamda3;
  
  for (int i = 0 ; i < 3 ; i++){
    for (int j = 0 ; j < 3 ; j++){
      u_res(i,j) = Iu*IIIu*ident(i,j)+(pow(Iu,2)-IIu)*DATA(i,j)-c2(i,j);
      u_res(i,j) = u_res(i,j)/(Iu*IIu-IIIu);
    }
  }
  
  for (int i = 0 ; i < 3 ; i++){
    for (int j = 0 ; j < 3 ; j++){
      r_res(i,j) = (IIu*ident(i,j)-Iu*u_res(i,j)+DATA(i,j))/IIIu;
    }
  }

  return std::pair<SmallMatrix3,SmallMatrix3>(u_res,r_res);

// Scope control.
#undef DATA 
}

  

//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//

SmallMatrix3::SmallMatrix3() : SmallMatrix(3) {}

SmallMatrix3::SmallMatrix3(const SmallMatrix3 &sm3) : SmallMatrix(sm3) {}

SmallMatrix3::SmallMatrix3(const SmallMatrix &sm) : SmallMatrix(sm) {
  if ((nrows!=3) || (ncols!=3)) {
    throw ErrProgrammingError(
      "Attempt to construct Symmatrix3 from non-3x3 SmallMatrix.",
      __FILE__,__LINE__);
  }
  // Otherwise there's nothing to do.
}
