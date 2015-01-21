// -*- C++ -*-
// $RCSfile: sparsemat.swg,v $
// $Revision: 1.5.2.5 $
// $Author: langer $
// $Date: 2014/12/03 19:16:40 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SPARSEMAT_SWG
#define SPARSEMAT_SWG

%module sparsemat

%include "engine/typemaps.swg"
%extern "common/doublevec.swg"
%pragma(python) code="from ooflib.SWIG.common.doublevec import DoubleVecPtr"
%pragma(python) include="engine/sparsemat.spy"

%{
#include "common/tostring.h"
#include "engine/dofmap.h"
#include "common/doublevec.h"
#include "engine/sparsemat.h"
#include <iostream>
#include <vector>
%}

class SparseMatIterator;
class SparseMatRowIterator;

class SparseMat {
public:
  SparseMat(int, int);
  ~SparseMat();
  int nrows();
  int ncols();
  int nnonzeros();
  void insert(int, int, double);
  void consolidate();
  bool consolidated();
  bool empty();

  // The C++ code generated for the clone() function does an additional
  // copy of the result. This is ok, because of the reference
  // counting.  The extra copy only copies the wrapper.
  SparseMat clone();
  SparseMat &add(double, SparseMat&);
//   DoubleVec trans_mult(DoubleVec&); // not needed? See __rmul__ in sparsemat.spy
  void axpy(double a, DoubleVec &x, DoubleVec &y); // y += a*self*x
  void axpy_trans(double, DoubleVec&, DoubleVec&);

  void solve_lower_triangle(DoubleVec&, DoubleVec&);
  void solve_lower_triangle_unitd(DoubleVec&, DoubleVec&);
  void solve_lower_triangle_trans(DoubleVec&, DoubleVec&);
  void solve_lower_triangle_trans_unitd(DoubleVec&, DoubleVec&);
  void solve_upper_triangle(DoubleVec&, DoubleVec&);
  void solve_upper_triangle_trans(DoubleVec&, DoubleVec&);

  double norm();

  DoubleVec inefficient_get_column(int);
  bool unique_indices();
  bool is_symmetric(double tolerance); // uses inefficient_get_column!
  // void sanityCheck();

  SparseMat transpose();

  %addmethods {
    void scale(double a) { *self *= a; }
    SparseMat matrixmultiply(SparseMat &m) { return (*self)*m; }
    SparseMatRowIterator row(int i) { 
//       std::cerr << "SparseMat::row(" << i << "): core=" << self->core
// 		<< std::endl;
      return self->begin(i); }
    SparseMatIterator __iter__() { return self->begin(); }
    %new const string *__repr__() { return new std::string(to_string(*self)); }
    SparseMat submatrix(const DoFMap &rows, const DoFMap &cols) {
      return SparseMat(*self, rows, cols);
    }
  }
};

class SparseMatIterator {
public:
  ~SparseMatIterator();
  int row();
  int col();
  double value();
  bool done();
  %addmethods {
    // SparseMatIterator *__iter__() { return self; }
    void increment() { ++*self; }
  }
};

class SparseMatRowIterator {
public:
  ~SparseMatRowIterator();
  int row();
  int col();
  double value();
  bool done();
  %addmethods {
    //SparseMatRowIterator *__iter__() { return self; }
    void increment() { ++*self; }
  }
};

void mmadump(char *filename, char *mtxname, SparseMat); // mathematica format

long nSparseMatCores();

#endif // SPARSEMAT_SWG
