// -*- C++ -*-
// $RCSfile: smallmatrix3.C,v $
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

#include <string.h>
#include <math.h>
#include "common/smallmatrix.h"
#include "common/vectormath.h"
#include "common/ooferror.h"
#include "common/tostring.h"
#include "common/vectormath.h"
#include "engine/smallmatrix3.h"

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
// requires the matrix to be symmetric, and is not specialized
// to the 3x3 case. 
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


double SmallMatrix3::determinant() const {
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

double SmallMatrix3::trace() const {
  return data[0]+data[4]+data[8];
}

// Useful macro for the below. Non-bounds-checked
// compile-time element retrieval.
#define DATA(r,c) data[c*3+r]

double SmallMatrix3::secondInvariant() const {
  // Match sign with the SymmMatrix3 one.  Same as Wikipedia,
  // opposite of Wolfram.
  return DATA(0,0)*DATA(1,1) + DATA(1,1)*DATA(2,2) + DATA(0,0)*DATA(2,2) \
    - DATA(0,1)*DATA(1,0) - DATA(1,2)*DATA(2,1) - DATA(0,2)*DATA(2,0);
}

std::pair<SmallMatrix3,SmallMatrix3> SmallMatrix3::ch_sqrt() const {
// Cayley-Hamilton matrix square root algorithm.
// Compile-time element retrieval wtih no bounds checking.
  
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

std::string SmallMatrix3::classname_("SmallMatrix3");
std::string SmallMatrix3::modulename_("ooflib.SWIG.engine.smallmatrix3");
  
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


/////////////////////////////////////////
// OutputVal functionality below here. //
/////////////////////////////////////////

OutputVal *SmallMatrix3::clone() const {
  return new SmallMatrix3(*this);
}

OutputVal *SmallMatrix3::zero() const {
  // TODO Opt: 
  SmallMatrix3 *res = new SmallMatrix3();
  res->clear();
  return res;
}

OutputVal *SmallMatrix3::one() const {
  // TODO: Really?  Not the identity?
  // NB SymmMatrix3 does the same thing.
  SmallMatrix3 *res = new SmallMatrix3();
  for(unsigned int i=0;i<9;++i) {
    res->data[i]=1.0;
  }
  return res;
}


OutputVal &SmallMatrix3::operator+=(const OutputVal &a) {
  const SmallMatrix3 &reala = dynamic_cast<const SmallMatrix3&>(a);
  return dynamic_cast<OutputVal&>(SmallMatrix::operator+=(reala));
}

OutputVal &SmallMatrix3::operator-=(const OutputVal &a) {
  const SmallMatrix3 &reala = dynamic_cast<const SmallMatrix3&>(a);
  return dynamic_cast<OutputVal&>(SmallMatrix::operator-=(reala));
}


OutputVal &SmallMatrix3::operator*=(double d) {
  return dynamic_cast<OutputVal&>(SmallMatrix::operator*=(d));
}

// Doubly-overloaded, to disambiguate from OutputVal versions.
SmallMatrix3 &SmallMatrix3::operator+=(const SmallMatrix3 &s) {
  return dynamic_cast<SmallMatrix3&>(SmallMatrix::operator+=(s));
}

SmallMatrix3 &SmallMatrix3::operator-=(const SmallMatrix3 &s) {
  return dynamic_cast<SmallMatrix3&>(SmallMatrix::operator-=(s));
}

double SmallMatrix3::operator[](const IndexP& ip) const {
  return data[ip.integer()];
}

double &SmallMatrix3::operator[](const IndexP& ip) {
  return data[ip.integer()];
}

void SmallMatrix3::component_pow(int p) {
  for(DoubleVec::iterator di = data.begin(); di!=data.end(); ++di)
    (*di) = pow(*di,p);
}

void SmallMatrix3::component_square() {
  for(DoubleVec::iterator di = data.begin(); di!=data.end(); ++di)
    (*di) = (*di)*(*di);
}


void SmallMatrix3::component_sqrt() {
  for(DoubleVec::iterator di = data.begin(); di!=data.end(); ++di)
    (*di) = sqrt(*di);
}

void SmallMatrix3::component_abs() {
  for(DoubleVec::iterator di = data.begin(); di!=data.end(); ++di)
    (*di) = fabs(*di);
}

DoubleVec *SmallMatrix3::value_list() const {
  DoubleVec *res = new DoubleVec(data);
  return res;
}

double SmallMatrix3::magnitude() const {
  double sum = 0.0;
  for(DoubleVec::const_iterator di = data.begin(); di!=data.end(); ++di)
    sum += (*di)*(*di);
  return sqrt(sum);
}


IteratorP SmallMatrix3::getIterator() const {
  return IteratorP(new TensorIterator());
}

void SmallMatrix3::print(std::ostream& o) const {
  // Need to cast to use the Smallmatrix's output, and not
  // the OutputVal one.
  const SmallMatrix &sm = dynamic_cast<const SmallMatrix&>(*this);
  o << sm; 
}

IndexP SmallMatrix3::getIndex(const std::string &str) const {
  return IndexP(new TensorIndex(TensorIndex::str2voigt9(str)));
}

// Dot products use a dispatch trick.
OutputVal *SmallMatrix3::dot(const OutputVal &ov) const {
  return ov.dotSmallMatrix3(*this);
}

OutputVal *SmallMatrix3::dotScalar(const ScalarOutputVal &ov) const {
  SmallMatrix3 *result = new SmallMatrix3(*this);
  (*result) *= ov.value();
  return result;
}

OutputVal *SmallMatrix3::dotVector(const VectorOutputVal &ov) const {
  assert(ov.dim()==3);
  return new VectorOutputVal((*this)* ov.value());
}

OutputVal *SmallMatrix3::dotSymmMatrix3(const SymmMatrix3 &ov) const {
  throw ErrProgrammingError(
     "Smallmatrix3 dot SymmMatrix not yet implemented as an OutputVal",
      __FILE__, __LINE__);
}

OutputVal *SmallMatrix3::dotSmallMatrix3(const SmallMatrix3 &ov) const {
  throw ErrProgrammingError(
      "SmallMatrix3 dot SmallMatrix3 not yet implemented as an OutputVal.",
       __FILE__,__LINE__);
}

std::ostream &operator<<(std::ostream& o, const SmallMatrix3& s) {
  // Use the matrix version, not the OutputVal one.
  const SmallMatrix &sm = dynamic_cast<const SmallMatrix&>(s);
  return o << sm;
}


OutputValue *newSmallMatrix3OutputValue() {
  return new OutputValue(new SmallMatrix3());
}

