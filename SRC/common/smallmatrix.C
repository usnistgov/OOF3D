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
#include <string.h>		// for memset

SmallMatrix::SmallMatrix(unsigned int rows, unsigned int cols)
  : nrows(rows),
    ncols(cols)
{
  data = DoubleVec(rows*cols, 0.0);
}

SmallMatrix::SmallMatrix(unsigned int size)
  : nrows(size),
    ncols(size)
{
  data = DoubleVec(size*size, 0.0);
}

SmallMatrix::SmallMatrix(const SmallMatrix& s)
  : nrows(s.nrows), 
    ncols(s.ncols)
{
  data = s.data;
}

void SmallMatrix::resize(unsigned int r, unsigned int c) {
  nrows = r;
  ncols = c;
  data.resize(r*c);
}

SmallMatrix::~SmallMatrix() {}

void SmallMatrix::clear() {
  data.clear(); // Erases all the elements, doesn't set them to zero.
  data.resize(nrows*ncols, 0.0);
}

// The FORTRAN ordering happens here.
double &SmallMatrix::operator()(unsigned int row, unsigned int col) {
  assert(row >= 0 && col >= 0 && row < nrows && col < ncols);
  return data[col*nrows+row];
}

// Dot product. 
double dot(const SmallMatrix &s1,const SmallMatrix &s2) {
  return dot(s1.data,s2.data);
}

// This has to have a return type of const double&, and not just
// double, so that expressions like &m(0,0) work correctly, as in the
// blas calls below.
const double &SmallMatrix::operator()(unsigned int row, unsigned int col) const 
{
  assert(row >= 0 && col >= 0 && row < nrows && col < ncols);
  return data[col*nrows+row];
}


// Arithmetic, including assignment.
SmallMatrix &SmallMatrix::operator=(const SmallMatrix &s) {
  assert(s.nrows==nrows && s.ncols==ncols);
  data = s.data;
  return *this;
}

SmallMatrix &SmallMatrix::operator+=(const SmallMatrix &s) {
  assert(s.nrows==nrows && s.ncols==ncols);
  data += s.data;
  return *this;
}


SmallMatrix &SmallMatrix::operator-=(const SmallMatrix &s) {
  assert(s.nrows==nrows && s.ncols==ncols);
  data -= s.data;
  return *this;
}



SmallMatrix &SmallMatrix::operator*=(double x) {
  data *= x;
  return *this;
}


// In-place transposition.  Only works for square matrices.
void SmallMatrix::transpose() {
  assert(nrows==ncols);
  for(unsigned int i=0;i<nrows;i++) {
    for(unsigned int j=0;j<i;j++) {
      double tmp = data[i*nrows+j];
      data[i*nrows+j]=data[j*nrows+i];
      data[j*nrows+i]=tmp;
    }
  }
}

extern "C" {
  // Arguments: N, # of columns of A.
  //            NRHS, # of right-hand-sides to solve for.
  //            A, the matrix
  //            LDA, leading dimension of the array (# of rows)
  //            IPIV -- pivot-index array, one pivot per row.
  //            B, matrix of right-hand-sides.
  //            LDB, leading dimension of B.
  //            INFO, error-return variable.
  void dgesv_(unsigned int*n, unsigned int*nrhs, double*a, unsigned int*lda,
	      int*ipiv, double*b, unsigned int*ldb, int*info);

  
  // Arguments: UL, character saying which triangle to refer to.
  //            N, the order of the matrix.
  //            A, the matrix.
  //            LDA, the leading dimension of the matrix.
  //            IPIV, an N-sized integer array for pivot indices.
  //            WORK, a work-space array, size affects performance.
  //            LWORK, integer size of the work array.
  //            INFO, single integer output. 0=success.
  void dsytrf_(char*ul, int*n, double*a, int*lda, int*ipiv,
	       double*work, int *lwork, int*info);

  
  // Arguments: UL, character saying which triangle to use.
  //            N, the order of A.
  //            A, the matrix.
  //            LDA, the leading dimension of A.
  //            IPIV, N-sized integer array of pivots from dsytrf.
  //            WORK, N-sized work-space array.
  //            INFO, single integer output, 0=success.
  void dsytri_(char *ul, int*n, double*a, int*lda, int*ipiv, 
	       double*work, int*info);

  // y <- alpha Ax + beta y
  // Arguments:
  //    trans: 'n' or 't', for 'no transpose' or 'transpose'
  //    m: # of rows of A
  //    n: # of cols of A
  //    alpha: scale factor
  //    a: the matrix A
  //    lda: leading dimension of A
  //    x: vector
  //    incx: stride for x
  //    beta: scale factor
  //    y: input/output vector
  void dgemv_(const char *trans, const unsigned int *m, const unsigned int *n,
	      const double *alpha, const double *a, const unsigned int *lda,
	      const double *x, const int *incx,
	      const double *beta,
	      double *y, const int *incy);
  // C <- alpha A B + beta C
  void dgemm_(const char *transa, const char *transb,
	      const unsigned int *m, const unsigned int *n,
	      const unsigned int *k, 
	      const double *alpha,
	      const double *a, const unsigned int *lda,
	      const double *b, const unsigned int *ldb,
	      const double *beta,
	      double *c, const unsigned int *ldc);
}


// This routine modifies the contents both of the "host" matrix
// and the passed-in rhs.  
int SmallMatrix::solve(SmallMatrix &rhs) {
  int info;
  assert(nrows==ncols && nrows==rhs.nrows);
  int *ipiv = new int[nrows];
  dgesv_(&nrows, &rhs.ncols, &data[0], &nrows, 
	 ipiv, &rhs.data[0], &rhs.nrows, &info);
  delete[] ipiv;
  // Numerical result is stored in the RHS.  Return value is a status
  // code.  Zero is successful exit, a negative integer n indicates
  // that the nth argument had an illegal value for dgesv, and a
  // positive integer indicates that the nth divisor was exactly zero,
  // the matrix is singular, the factorization is complete, but the
  // solution could not be computed.
  return info; 
}

int SmallMatrix::symmetric_invert() {
  // This method assumes that the matrix is symmetric, and only
  // examines the upper triangle in order to compute the inverse.  You
  // should only use it when you know for sure that your matrix is in
  // fact symmetric, otherwise you will get wrong answers.

  assert(nrows==ncols) ;
  char uplo='U';
  int n=nrows;
  int lda=nrows;
  int ipiv[nrows];
  int lwork=nrows;
  double work[lwork];
  int info=0;
  
  // Factor.
  dsytrf_(&uplo, &n, &data[0], &lda, ipiv, work, &lwork, &info);
  if (info==0) {
    // Actually invert.
    dsytri_(&uplo, &n, &data[0], &lda, ipiv, work, &info);
    if (info==0) {
      // TODO MER: The dsytrf+dsytri combo only looks at and fills in one
      // triangle of the matrix (the upper triangle, because we used
      // uplo='U').  Here, we hack acround this by filling in the
      // lower triangle.  The Really Right answer is to make a
      // symmetric matrix class that uses LAPACK-style packed storage
      // for its data, and then put this routine in that class.  It
      // would make sense for this class (SymDenseMatrix?) to also
      // replace the SymmMatrix class, and for it to inherit from both
      // the OutputValue and the SmallMatrix classes.  Also,
      // SmallMatrix should be renamed to "DenseMatrix" to be more
      // descriptive.  An alternative is to just implement a more
      // general (but probably slower) inversion scheme here.
      for(unsigned int ltr=1;ltr<nrows;ltr++) 
	for(unsigned int ltc=0;ltc<ltr;ltc++)   
	  data[ltc*nrows+ltr]=data[ltr*nrows+ltc]; 
    }
    return info;
  }
  else {
    throw ErrProgrammingError("Return code " + to_string(info) + 
			      " attempting to factor " +
			      to_string(nrows) + " by " + 
			      to_string(ncols) + " SmallMatrix.",
			      __FILE__, __LINE__);
  }

}


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
  if (xmod-1.0e30 > 0.0)
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


SmallMatrix operator+(const SmallMatrix &a, const SmallMatrix &b) {
  SmallMatrix res = a;
  res+=b;
  return res;
}

SmallMatrix operator-(const SmallMatrix &a, const SmallMatrix &b) {
  SmallMatrix res = a;
  res-=b;
  return res;
}

SmallMatrix operator*(const SmallMatrix &a, double x) {
  SmallMatrix res = a;
  res*=x;
  return res;
}

SmallMatrix operator*(double x, const SmallMatrix &a) {
  // Doesn't just call the other one to avoid function-call overhead.
  SmallMatrix res = a;
  res*=x;
  return res;
}

// Matrix multiplication, accessing result matrix in column order. 

DoubleVec operator*(const SmallMatrix &m, const DoubleVec &v) {
  const int one = 1;
  const double One = 1.0;
  const char enn = 'n';		// indicates no transpose
  assert(v.size() == m.ncols);
  const double zero = 0.0;
  DoubleVec result(m.nrows, 0.0);
  dgemv_(&enn, &m.nrows, &m.ncols, &One, &m(0,0), &m.nrows, &v[0], &one, &zero,
	 &result[0], &one);
  return result;
}

// Matrix multiplication, accessing result matrix in column order.                                     
SmallMatrix operator*(const SmallMatrix &a, const SmallMatrix &b) {
  assert(a.ncols == b.nrows);
  SmallMatrix result(a.nrows, b.ncols);
  const char enn = 'n';
  const double one = 1.0;
  const double zero = 0.0;
  dgemm_(&enn, &enn, &a.nrows, &b.ncols, &a.ncols, &one, &a(0,0), &a.nrows,
	 &b(0,0), &b.nrows, &zero, &result(0,0), &a.nrows);
  return result;
}

DoubleVec operator+(const DoubleVec &v, const SmallMatrix &ss) {
  DoubleVec result = DoubleVec(ss.data);
  result += v;
  return result;
}

DoubleVec operator+(const SmallMatrix &ss, const DoubleVec &v) {
  DoubleVec result = DoubleVec(ss.data);
  result += v;
  return result;
}

///////////////////////

std::ostream &operator<<(std::ostream &os, const SmallMatrix &mat) {
  for(unsigned int i=0; i<mat.rows(); i++) {
    os << std::endl;
    for(unsigned int j=0; j<mat.cols(); j++) 
      os << " " << mat(i,j);
  }
  return os;
}


///////////////////////

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
