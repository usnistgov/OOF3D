// -*- C++ -*-

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

%{
#define SWIG_FILE_WITH_INIT
#include "engine/sparsemat.h"
#include "engine/dofmap.h"
#include <string>
#include <cstring>
%} 

%pragma(python) include="engine/sparsemat.spy"

class SparseMat {
public:
  SparseMat(int nr, int nc);
  ~SparseMat();
  SparseMat clone() const;

  // TODO(lizhong): inline possible methods

  /* Matrix property methods */

  int nrows() const;
  int ncols() const;
  int nnonzeros() const;
  void resize(int nr, int nc);
  void reserve(int size);
  void insert(int ir, int ic, double val);
  bool empty() const;
  bool is_nonempty_row(unsigned int) const;
  bool is_nonempty_col(unsigned int) const;
  SparseMat lower() const;
  SparseMat unit_lower() const;
  SparseMat upper() const;
  SparseMat unit_upper() const;

  /* Arithmetic operations */

  double norm() const;
  SparseMat transpose() const;

  SparseMat &add(double, const SparseMat&); // scale and add
  DoubleVec trans_mult(const DoubleVec&) const;

  // In-place matrix vector multiplication, ala blas.
  void axpy(double alpha, const DoubleVec &x, DoubleVec &y) const;
  void axpy_trans(double alpha, const DoubleVec &x, DoubleVec &y) const;

  // Triangular solvers.
  void solve_lower_triangle(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_unitd(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_trans(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_trans_unitd(const DoubleVec&, DoubleVec&) const;
  void solve_upper_triangle(const DoubleVec&, DoubleVec&) const;
  void solve_upper_triangle_trans(const DoubleVec&, DoubleVec&) const;

  /* Debugging routines. */

  bool is_lower_triangular(bool diag) const;
  bool is_upper_triangular(bool diag) const;
  bool is_symmetric(double tolerance) const;

  const std::string str() const;

  %addmethods {
    void scale(double a) { *self *= a; }
    SparseMat matrixmultiply(SparseMat &m) { return (*self)*m; }

    const char* __repr__() {
      return (*self).str().c_str();
    }

    bool save(const char *filename) {
      return save_mat(*self, std::string(filename));
    }
 
    bool load(const char *filename) {
      return load_mat(*self, std::string(filename));
    }
  }
};

#endif // SPARSEMAT_SWG
