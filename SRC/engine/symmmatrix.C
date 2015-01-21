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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::string SymmMatrix3::classname_("SymmMatrix3");
std::string SymmMatrix3::modulename_("ooflib.SWIG.engine.symmmatrix");

SymmMatrix3::SymmMatrix3(double v00, double v11, double v22,
			 double v12, double v02, double v01)
  : SymmMatrix(3), dirtyeigs_(true)
{
  operator()(0,0) = v00;
  operator()(1,1) = v11;
  operator()(2,2) = v22;
  operator()(1,2) = v12;
  operator()(0,2) = v02;
  operator()(0,1) = v01;
}

OutputVal *SymmMatrix3::clone() const {
  return new SymmMatrix3(*this);
}

OutputVal *SymmMatrix3::zero() const {
  return new SymmMatrix3();
}

OutputVal *SymmMatrix3::one() const {
  return new SymmMatrix3(1.0, 1.0, 1.0, 1.0, 1.0, 1.0);
}

SymmMatrix3::SymmMatrix3(const SymmMatrix3 &mat)
  : SymmMatrix(3), dirtyeigs_(mat.dirtyeigs_)
{
  copy(mat.m);
  eigenvalues = mat.eigenvalues;
}

SymmMatrix3::SymmMatrix3(const SymmMatrix &mat)
  : SymmMatrix(3), dirtyeigs_(true)
{
  if(mat.size() != 3)
    throw ErrProgrammingError("Illegal SymmMatrix3 initialization", 
			      __FILE__, __LINE__);
  copy(mat.m);
}

std::ostream &operator<<(std::ostream &os, const SymmMatrix3 &a) {
  a.print(os);		// The OutputVal way of doing it.
  return os;
}

// SymmMatrix3::~SymmMatrix3() {
//   std::cerr << "SymmMatrix3::~SymmMatrix3: " << this << std::endl;
// }

SymmMatrix3 operator+(const SymmMatrix3 &a, const SymmMatrix3 &b) {
  SymmMatrix3 result(a);
  result += b;
  return result;
}

SymmMatrix3 operator-(const SymmMatrix3 &a, const SymmMatrix3 &b) {
  SymmMatrix3 result(a);
  result -= b;
  return result;
}

SymmMatrix3 operator*(const SymmMatrix3 &a, double b) {
  SymmMatrix3 result(a);
  result *= b;
  return result;
}

SymmMatrix3 operator*(double b, const SymmMatrix3 &a) {
  SymmMatrix3 result(a);
  result *= b;
  return result;
}

SymmMatrix3 operator/(const SymmMatrix3 &a, double b) {
  SymmMatrix3 result(a);
  result *= (1./b);
  return result;
}

OutputVal *SymmMatrix3::dot(const OutputVal &ov) const {
  return ov.dotSymmMatrix3(*this);
}

OutputVal *SymmMatrix3::dotScalar(const ScalarOutputVal &ov) const {
  SymmMatrix3 *result = new SymmMatrix3(*this);
  *result *= ov.value();
  return result;
}

OutputVal *SymmMatrix3::dotVector(const VectorOutputVal &ov) const {
  assert(ov.dim() == 3);
  return new VectorOutputVal((*this) * ov.value());
}

OutputVal *SymmMatrix3::dotSymmMatrix3(const SymmMatrix3 &ov) const {
  // This doesn't work because the product of two SymmMatrices is a
  // SmallMatrix (not necessarily symmetric), and SmallMatrix isn't an
  // OutputVal class.
  throw ErrProgrammingError(
	    "SymmMatrix dot SymmMatrix not yet implemented as an OutputVal",
	    __FILE__, __LINE__);
}

#if DIM==3
Coord operator*(const SymmMatrix3 &a, const Coord &x) {
  Coord result;
  for(int i=0; i<3; i++) {
    double &r = result[i];
    for(int j=0; j<3; j++)
      r += a(i,j)*x[j];
  }
  return result;
}

Coord operator*(const Coord &x, const SymmMatrix3 &a) {
  return a*x;
}
#endif // DIM==3

double SymmMatrix3::trace() const {
  return operator()(0,0) + operator()(1,1) + operator()(2,2);
}

double SymmMatrix3::determinant() const {
  double v00 = operator()(0,0);
  double v11 = operator()(1,1);
  double v22 = operator()(2,2);
  double v12 = operator()(1,2);
  double v02 = operator()(0,2);
  double v01 = operator()(0,1);
  return v00*(v11*v22 - v12*v12) - v01*(v01*v22 - v12*v02) 
    + v02*(v01*v12 - v11*v02);
}

double SymmMatrix3::secondInvariant() const {
  double v00 = operator()(0,0);
  double v11 = operator()(1,1);
  double v22 = operator()(2,2);
  double v12 = operator()(1,2);
  double v02 = operator()(0,2);
  double v01 = operator()(0,1);
  // http://mathworld.wolfram.com/CharacteristicPolynomial.html gives
  // the opposite sign for the second invariant, but the wikipedia
  // page doesn't.  There may be multiple conventions.
  return v00*v22 + v00*v11 + v11*v22 - v01*v01 - v02*v02 - v12*v12;
}

// "Deviator" is the square root of the sum of the squares of the
// traceless part of the matrix.
double SymmMatrix3::deviator() const {
  double v00 = operator()(0,0);
  double v11 = operator()(1,1);
  double v22 = operator()(2,2);
  double v12 = operator()(1,2);
  double v02 = operator()(0,2);
  double v01 = operator()(0,1);
  double trace = v00+v11+v22;
  return sqrt(v00*v00+v11*v11+v22*v22 + 2*(v01*v01+v02*v02+v12*v12) - 
	      (1.0/3.0)*trace*trace);
}

// "Magnitude" is the square root of the sum of the squares of the
// elements.  It actually is an invariant.
double SymmMatrix3::magnitude() const {
  double v00 = operator()(0,0);
  double v11 = operator()(1,1);
  double v22 = operator()(2,2);
  double v12 = operator()(1,2);
  double v02 = operator()(0,2);
  double v01 = operator()(0,1);
  return sqrt(v00*v00+v11*v11+v22*v22 + 2*(v01*v01+v02*v02+v12*v12));
}

double SymmMatrix3::contract(const SymmMatrix3 &other) const {
  return (operator()(0,0)*other(0,0) +
	  operator()(1,1)*other(1,1) +
	  operator()(2,2)*other(2,2) +
	  2.0*(operator()(0,1)*other(0,1) +
	       operator()(1,2)*other(1,2) +
	       operator()(2,0)*other(2,0)));
}


void SymmMatrix3::findEigenvalues() const {
  if(!dirtyeigs_) return;
  dirtyeigs_ = false;
  getEigenvalues(*this, eigenvalues);
}

double SymmMatrix3::maxEigenvalue() const {
  findEigenvalues();
  return eigenvalues.max();
}

double SymmMatrix3::midEigenvalue() const {
  findEigenvalues();
  return eigenvalues.mid();
}

double SymmMatrix3::minEigenvalue() const {
  findEigenvalues();
  return eigenvalues.min();
}

double &SymmMatrix3::operator[](const IndexP &p) {
  const FieldIndex &fi(p);
  const SymTensorIndex &sti = dynamic_cast<const SymTensorIndex&>(fi);
  dirtyeigs_ = true;
  return (*this)(sti.row(), sti.col());
}

double SymmMatrix3::operator[](const IndexP &p) const {
  // const FieldIndex &fi(p);
  const SymTensorIndex &sti = dynamic_cast<const SymTensorIndex&>(p);
  return (*this)(sti.row(), sti.col());
}

double &SymmMatrix3::operator[](const SymTensorIndex &ij) {
  dirtyeigs_ = true;
  return (*this)(ij.row(), ij.col());
}

double SymmMatrix3::operator[](const SymTensorIndex &ij) const {
  return (*this)(ij.row(), ij.col());
}

void SymmMatrix3::print(std::ostream &os) const {
  const SymmMatrix &sm = dynamic_cast<const SymmMatrix&>(*this);
  os << sm;
}

IndexP SymmMatrix3::getIndex(const std::string &str) const {
  // str must be "xx", "yy", "zz", "yz", "xz", or "xy", or permutations
  return IndexP(new SymTensorIndex(SymTensorIndex::str2voigt(str)));
}

IteratorP SymmMatrix3::getIterator() const {
  return IteratorP(new SymTensorIterator());
}

OutputValue *newSymTensorOutputValue() {
  return new OutputValue(new SymmMatrix3());
}

DoubleVec *SymmMatrix3::value_list() const {
  DoubleVec *res = new DoubleVec(0);
  res->reserve(6);
  res->push_back(m[0][0]);  // Voigt order. 
  res->push_back(m[1][1]);
  res->push_back(m[2][2]);
  res->push_back(m[2][1]);
  res->push_back(m[2][0]);
  res->push_back(m[1][0]);
  return res;
}
