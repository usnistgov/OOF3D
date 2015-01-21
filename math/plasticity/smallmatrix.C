// -*- C++ -*-
// $RCSfile: smallmatrix.C,v $
// $Revision: 1.1 $
// $Author: reida $
// $Date: 2006/12/07 14:02:35 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@ctcms.nist.gov. 
 */

#include "smallmatrix.h"


// How stupid is this?
std::string intstring(int i) {
  std::ostringstream os;
  os << i;
  return os.str();
}

std::ostream &operator<<(std::ostream &os, ErrProgrammingError &epe)
{
  os << "ErrProgrammingError(" << epe.msg << ", " << epe.lineno 
     << ", " << epe.filename << ")";
  return os;
}

SmallMatrix::SmallMatrix(int rows, int cols) :
  length(rows*cols), nrows(rows), ncols(cols) {
  data = new double[length];
}

SmallMatrix::SmallMatrix(int size) : 
  length(size*size), nrows(size), ncols(size) {
  data = new double[length];
}

SmallMatrix::SmallMatrix(const SmallMatrix& s) :
  length(s.length), nrows(s.nrows), ncols(s.ncols) {
  data = new double[length];
  for(int i=0;i<length;i++) 
    data[i]=s.data[i];
}

SmallMatrix::~SmallMatrix() {
  delete[] data;
}


void SmallMatrix::clear() {
  for(int i=0;i<length;i++) 
    data[i]=0.0;
}

// The FORTRAN ordering happens here.
// Should maybe do bounds-checking?
double &SmallMatrix::operator()(int row, int col) {
  return data[col*nrows+row];
}

double SmallMatrix::operator()(int row, int col) const {
  return data[col*nrows+row];
}


// Arithmetic, including assignment.
SmallMatrix &SmallMatrix::operator=(const SmallMatrix &s) {
  if ((s.nrows==nrows)&&(s.ncols==ncols)) {
    for(int i=0;i<length;i++) 
      data[i]=s.data[i];
  }
  else {
    throw ErrProgrammingError("Incorrect size for SmallMatrix assignment.",
			      __FILE__, __LINE__);
  }
  return *this;
}

SmallMatrix &SmallMatrix::operator+=(const SmallMatrix &s) {
  if ((s.nrows==nrows)&&(s.ncols==ncols)) {
    for(int i=0; i<length; i++) 
      data[i]+=s.data[i];
  }
  else {
    throw ErrProgrammingError("Incorrect size for SmallMatrix addition.",
			      __FILE__, __LINE__);
  }
  return *this;
}


SmallMatrix &SmallMatrix::operator-=(const SmallMatrix &s) {
  if ((s.nrows==nrows)&&(s.ncols==ncols)) {
    for(int i=0; i<length; i++) 
      data[i]-=s.data[i];
  }
  else {
    throw ErrProgrammingError("Incorrect size for SmallMatrix addition.",
			      __FILE__, __LINE__);
  }
  return *this;
}



SmallMatrix &SmallMatrix::operator*=(double x) {
  for(int i=0; i<length; i++) 
    data[i]*=x;
  return *this;
}


// In-place transposition.  Only works for square matrices.  Used by
// the block preconditioner in the Sparse++ directory.
void SmallMatrix::transpose() {
  if(nrows==ncols) {
    for(int i=0;i<nrows;i++)
      for(int j=0;j<i;j++) {
	double tmp = data[i*nrows+j];
	data[i*nrows+j]=data[j*nrows+i];
	data[j*nrows+i]=tmp;
      }
  }
  else
    throw ErrProgrammingError("Cannot transpose non-square SmallMatrix.",
			      __FILE__, __LINE__);
}


// This routine modifies the contents both of the "host" matrix
// and the passed-in rhs.  
int SmallMatrix::solve(SmallMatrix &rhs) {
  int info;
  if(nrows==ncols) {
    if(nrows==rhs.nrows) {
      int *ipiv = new int[nrows];
      dgesv_(&nrows, &rhs.ncols, data, &nrows, 
	     ipiv, rhs.data, &rhs.nrows, &info);
      delete[] ipiv;
      return info;  // Result is encoded in the rhs.
    } 
    else {
      throw ErrProgrammingError("Cannot solve SmallMatrix, matrix is " + 
				intstring(nrows) + "x" + intstring(ncols) + 
				", RHS is of size " + 
				intstring(rhs.nrows) + ".", 
				__FILE__, __LINE__);
    }
  } 
  else {
    throw ErrProgrammingError("Cannot solve non-square " + 
			      intstring(nrows) + " by " + 
			      intstring(ncols) + " SmallMatrix.",
			      __FILE__, __LINE__);
  }
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

// Matrix multiplication, accessing result matrix in column order.                                     
SmallMatrix operator*(const SmallMatrix &a, const SmallMatrix &b) {
  if(a.ncols == b.nrows) {
    SmallMatrix res = SmallMatrix(a.nrows, b.ncols);
    res.clear();
    for(int i=0;i<b.ncols;i++) 
      for(int j=0;j<a.nrows;j++) 
	for(int k=0;k<a.ncols;k++) 
	  res(j,i)+=a(j,k)*b(k,i);
    return res;
  } else {
    throw ErrProgrammingError("Incorrect size for SmallMatrix multiplicaiton.",
			      __FILE__, __LINE__);
  }
}
