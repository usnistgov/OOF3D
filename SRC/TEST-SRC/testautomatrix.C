// -*- C++ -*-
// $RCSfile: testautomatrix.C,v $
// $Revision: 1.3.142.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

//#include <oofconfig.h>

#include "automatrix.h"
#include <iostream>
using namespace std;

class Matrix {
  int **data;
  int nrows;
  int ncols;
private:
  void allocate() {
    data = new int*[nrows];
    for(int i=0; i<nrows; i++) {
      data[i] = new int[ncols];
    }
  }
public:
  typedef int value_type;
  Matrix(int n, int m)
    : nrows(n),
      ncols(m)
  {
    allocate();
    for(int i=0; i<n; i++) {
      for(int j=0; j<m; j++)
	data[i][j] = i*j;
    }
    cerr << "new " << this << *this << endl;
  }

  Matrix(const Matrix &other)
    : nrows(other.nrows),
      ncols(other.ncols)
  {
    allocate();
    for(int i=0; i<nrows; i++)
      for(int j=0; j<ncols; j++)
	data[i][j] = other(i,j);
    cerr << "copy " << this << *this << endl;
  }

  ~Matrix() {
    cerr << "deleting " << this << *this << endl;
    for(int i=0; i<nrows; i++)
      delete data[i];
    delete data;
  }

  int &operator()(int i, int j) { return data[i][j]; }
  int operator()(int i, int j) const { return data[i][j]; }

  friend ostream &operator<<(ostream &os, const Matrix &mat) {
    os << " [";
    for(int i=0; i<mat.nrows; i++) {
      os << "[";
      for(int j=0; j<mat.ncols-1; j++)
	os << mat.data[i][j] << " ";
      os << mat.data[i][mat.ncols-1] << "]";
    }
    os << "]";
    return os;
  }
};

AutoMatrix<Matrix> f() {
  AutoMatrix<Matrix> x(2,2);
  x(1,1) = 123;
  return x;
}

AutoMatrix<Matrix> g(AutoMatrix<Matrix> m) {
  cerr << "g: " << m << endl;
  m(1,1) = 321;
  return m;
}

int main(int, char**) {
  AutoMatrix<Matrix> a(3,3);
  cerr << a << endl;
  AutoMatrix<Matrix> ba = f();
  cerr << ba << endl;
  AutoMatrix<Matrix> ca(ba);
  ba = g(a);
  cerr << "ba " << ba << endl;
  cerr << "ca " << ca << endl;
  cerr << "----" << endl;
}
