// -*- C++ -*-
// $RCSfile: sparsemat.h,v $
// $Revision: 1.6.4.6 $
// $Author: langer $
// $Date: 2014/12/03 19:16:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <iostream>

// A reference counted sparse matrix class, loosely based on the NIST
// sparse blas.  The basic construction call is
//    SparseMat::insert(i, j, x)
// which *adds* x to the i,j component.

// Data is stored as a vector of pointers to vectors of pairs.
// There's one vector of pairs for each row.  Each pair contains a
// column index and a value.  Repeated column indices are allowed
// during matrix construction, but should be consolidated (by calling
// consolidate()) before doing any computations.

// This class intentionally does not have any way of extracting a
// single entry, since that shouldn't be necessary, and is
// inefficient.  It does have a way of extracting a submatrix, though,
// and a const iterator for looping over all values.

// TIMING (dist3d on iolanthe):
// % time python regression.py solver_test
// using std::list for SparseMatRow:
//   real 34m37.824s   user 34m0.383s   sys 0m16.208s
// using std::vector:
//   real 33m9.264s    user 32m28.683s  sys 0m16.300s
//   real 33m20.782s   user 32m47.049s  sys 0m16.189s

// % time python regression.py nonlinear_floatbc_test
// using std::list
//   real 6m33.892s    user 6m31.087s   sys 0m1.105s
// using std::vector:
//   real 6m13.280s    user 6m9.875s    sys 0m1.011s

#include <vector>
#include <list>

class SparseMat;
class SparseMatCore;
class SparseMatConstIterator;
class SparseMatIterator;
class SparseMatRowConstIterator;
class SparseMatRowIterator;

#ifndef SPARSEMAT_H
#define SPARSEMAT_H

#include "common/lock.h"

class DoFMap;
class DoubleVec;

class SparseMatCore {
public:
  class Entry {
  public:
    unsigned int col;		// column
    double val;			// value
    Entry() : col(123456789), val(-123.) {}
    Entry(unsigned int col, double val) : col(col), val(val) {}
    Entry(const Entry &other) : col(other.col), val(other.val) {}
    bool operator<(const Entry &other) const {
      return col < other.col;
    }
  };
  typedef std::vector<Entry> SparseMatRow;
private:
  SLock refcountlock_;
  // data is stored as a vector of pointers, so that resizing is quick.
  std::vector<SparseMatRow*> data;
  // nonempty_col keeps track of which columns have data in them.

  std::vector<bool> nonempty_col;

  // nnz_ is the number of entries, which is only equal to the number
  // of nonzeros after consolidate() has been called.
  unsigned int nnz_; 
  unsigned int nrows_, ncols_;
  unsigned int refcount_;
  bool consolidated_;
  // The copy constructor is prohibited. SparseMatCores should never be copied.
  SparseMatCore(const SparseMatCore&);
  // Other constructors can only be called by SparseMat.
  SparseMatCore();
  SparseMatCore(unsigned int nr, unsigned int nc);
  // Construct by extraction from an existing matrix.
  SparseMatCore(const SparseMatCore&, const DoFMap&, const DoFMap&);
  ~SparseMatCore();

  typedef SparseMatConstIterator const_iterator;
  const_iterator begin() const;
  const_iterator end() const;

  typedef SparseMatIterator iterator;
  iterator begin();
  iterator end();

  typedef SparseMatRowConstIterator const_row_iterator;
  const_row_iterator begin(unsigned int) const;
  const_row_iterator end(unsigned int) const;

  typedef SparseMatRowIterator row_iterator;
  row_iterator begin(unsigned int);
  row_iterator end(unsigned int);

  // nrows() and ncols() might not always do what you expect them to
  // do. The nominal size of the matrix is determined by the maximum
  // of (1) the sizes passed in to the constructor or to resize(), (2)
  // the DoFMaps passed into the constructor, or (3) the indices used
  // in calls to insert(i,j,x).
  unsigned int nrows() const { return nrows_; }
  unsigned int ncols() const { return ncols_; }
  unsigned int nnonzeros() const { return nnz_; }
  void resize(unsigned int, unsigned int);
  void insert(unsigned int, unsigned int, double);
  void consolidate_row(unsigned int);    // Helper for consolidate().
  void consolidate();		// call after insertion has finished
  bool consolidated() const { return consolidated_; }
  // set_consolidated() is used in a few situations when it's known
  // whether a matrix is consolidated or not, but its consolidated_
  // flag isn't set properly for some reason.
  void set_consolidated(bool cons) { consolidated_ = cons; }

  SparseMat transpose() const;
  
  SparseMatCore &operator*=(double);
  SparseMatCore &operator+=(const SparseMatCore&);
  SparseMatCore &add(double, const SparseMatCore&); // scale and add

  // Matrix-vector multiplication.  These return a new object, which
  // may not be desirable in some situations.
  DoubleVec operator*(const DoubleVec&) const;
  DoubleVec trans_mult(const DoubleVec&) const;
  // In-place matrix vector multiplication, ala blas.  This adds
  // alpha*M*x to y.
  void axpy(double alpha, const DoubleVec &x, DoubleVec &y) const;
  // This adds alpha*transpose(M)*x to y.
  void axpy_trans(double alpha, const DoubleVec &x, DoubleVec &y) const;

  // Matrix-matrix multiplication.
  SparseMat operator*(const SparseMat&) const;

  // Triangular solvers.
  void solve_lower_triangle(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_unitd(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_trans(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_trans_unitd(const DoubleVec&, DoubleVec&) const;
  void solve_upper_triangle(const DoubleVec&, DoubleVec&) const;
  void solve_upper_triangle_trans(const DoubleVec&, DoubleVec&) const;

  double norm() const;

  bool is_nonempty_row(unsigned int) const;
  bool is_nonempty_col(unsigned int) const;

  // Extracting a column is inefficient and should only be used for
  // testing.
  DoubleVec inefficient_get_column(unsigned int) const;

  // Debugging routines.  
  // diag==true means the diagonal is present.
  bool is_lower_triangular(bool diag) const;
  bool is_upper_triangular(bool diag) const;
  bool unique_indices() const;
  bool is_symmetric(double tolerance) const;
  // void sanityCheck() const;

  friend class SparseMat;
  friend class SparseMatConstIterator;
  friend class SparseMatIterator;
  friend class SparseMatRowConstIterator;
  friend class SparseMatRowIterator;
  friend std::ostream &operator<<(std::ostream&, const SparseMatCore&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatIterator&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatConstIterator&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatRowIterator&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatRowConstIterator&);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// SparseMat is a reference counting wrapper for SparseMatCore.

class SparseMat {
public: // DEBUGGING private: 
  SparseMatCore *core;
public:
  SparseMat();
  SparseMat(unsigned int nr, unsigned int nc);
  SparseMat(SparseMatCore&);	// rewrap
  SparseMat(const SparseMat&);
  SparseMat(const SparseMat&, const DoFMap&, const DoFMap&);
  SparseMat &operator=(const SparseMat&);
  ~SparseMat();

  SparseMat clone() const;	// creates independent copy

  typedef SparseMatIterator iterator;
  iterator begin();
  iterator end();

  typedef SparseMatConstIterator const_iterator;
  const_iterator begin() const;
  const_iterator end() const;

  typedef SparseMatRowConstIterator const_row_iterator;
  const_row_iterator begin(unsigned int r) const;
  const_row_iterator end(unsigned int r) const;

  typedef SparseMatRowIterator row_iterator;
  row_iterator begin(unsigned int r);
  row_iterator end(unsigned int r);

  unsigned int nrows() const { return core->nrows(); }
  unsigned int ncols() const { return core->ncols(); }
  void resize(unsigned int i, unsigned int j) { core->resize(i, j); }
  int nnonzeros() const { return core->nnonzeros(); }
  bool is_nonempty_row(int i) const { return core->is_nonempty_row(i); }
  bool is_nonempty_col(int j) const { return core->is_nonempty_col(j); }
  bool empty() const { return core->nnonzeros() == 0; }

  void insert(unsigned int i, unsigned int j, double x) {
    core->insert(i, j, x); 
  }
  void tile(unsigned int i, unsigned int j, const SparseMat&);

  void consolidate() { core->consolidate(); }
  bool consolidated() const { return core->consolidated(); }
  // set_consolidated() is used after copying a matrix whose
  // consolidation status is known.
  void set_consolidated(bool cons) { core->set_consolidated(cons); }

  SparseMat transpose() const { return core->transpose(); }

  SparseMat &operator*=(double a) {
    (*core) *= a;
    return *this;
  }
  SparseMat &operator+=(const SparseMat &m) {
    *core += *m.core;
    return *this; 
  }
  SparseMat &add(double a, const SparseMat &m) { 
    core->add(a, *m.core); 
    return *this;
  }

  SparseMat operator*(const SparseMat &m) const { return (*core)*m; }

  DoubleVec operator*(const DoubleVec &v) const { return (*core)*v; }
  DoubleVec trans_mult(const DoubleVec &v) const { return core->trans_mult(v); }
  void axpy(double alpha, const DoubleVec &x, DoubleVec &y)
    const
  {
    core->axpy(alpha, x, y);
  }
  void axpy_trans(double alpha, const DoubleVec &x, DoubleVec &y) const {
    core->axpy_trans(alpha, x, y);
  }

  double norm() const { return core->norm(); }

  void solve_lower_triangle(const DoubleVec &rhs, DoubleVec &x) const {
    core->solve_lower_triangle(rhs, x);
  }
  void solve_lower_triangle_unitd(const DoubleVec &rhs, DoubleVec &x) const {
    core->solve_lower_triangle_unitd(rhs, x);
  }
  void solve_lower_triangle_trans(const DoubleVec &rhs, DoubleVec &x) const {
    core->solve_lower_triangle_trans(rhs, x);
  }
  void solve_lower_triangle_trans_unitd(const DoubleVec &rhs, DoubleVec &x) const
  {
    core->solve_lower_triangle_trans_unitd(rhs, x);
  }
  void solve_upper_triangle(const DoubleVec &rhs, DoubleVec &x) const {
    core->solve_upper_triangle(rhs, x);
  }
  void solve_upper_triangle_trans(const DoubleVec &rhs, DoubleVec &x) const {
    core->solve_upper_triangle_trans(rhs, x);
  }

  friend class SparseMatConstIterator;
  friend class SparseMatIterator;
  friend class SparseMatRowConstIterator;
  friend class SparseMatRowIterator;
  friend class SparseMatCore;

  
  // Debugging routines.  
  DoubleVec inefficient_get_column(int i) const {
    // Extracting a column is inefficient and should only be used for
    // testing.
    return core->inefficient_get_column(i); 
  }
  bool is_lower_triangular(bool diag) const {
    // diag==true means the diagonal may be present.
    return core->is_lower_triangular(diag);
  }
  bool is_upper_triangular(bool diag) const {
    // diag==true means the diagonal may be present.
    return core->is_upper_triangular(diag);
  }
  bool unique_indices() const { return core->unique_indices(); }
  bool is_symmetric(double tolerance) const {
    return core->is_symmetric(tolerance); 
  }
  // void sanityCheck() const { core->sanityCheck(); }

  friend std::ostream &operator<<(std::ostream&, const SparseMat&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatIterator&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatConstIterator&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatRowIterator&);
  friend std::ostream &operator<<(std::ostream&, const SparseMatRowConstIterator&);
};

SparseMat operator*(const SparseMat&, double);
SparseMat operator*(double, const SparseMat&);

void mmadump(const std::string &filename, const std::string &mtxname, 
	     const SparseMat&);	// for debugging

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Iterator classes

// TODO MER: SparseMatIterator and SparseMatConstIterator share a lot of
// mostly trivial code.  Is it worth giving them a common base class?
// Same for SparseMatRowIterator and SparseMatRowConstIterator.

class SparseMatIterator {
private:
  SparseMat mat;
  std::vector<SparseMatCore::SparseMatRow*>::iterator rowiter;
  SparseMatCore::SparseMatRow::iterator coliter;
public:
  SparseMatIterator(SparseMat);
  ~SparseMatIterator();
  SparseMatIterator &operator++();
  unsigned int row() const;
  unsigned int col() const;
  double &value() const;
  bool done() const;
  double &operator*() const { return value(); }
  bool operator==(const SparseMatIterator&) const;
  bool operator!=(const SparseMatIterator&) const;
  bool operator==(const SparseMatConstIterator&) const;
  bool operator!=(const SparseMatConstIterator&) const;
  friend class SparseMat;
  friend class SparseMatCore;
  friend class SparseMatRowIterator;
  friend class SparseMatConstIterator;
  friend std::ostream& operator<<(std::ostream&, const SparseMatIterator&);
};

class SparseMatConstIterator {
private:
  const SparseMat mat;
  std::vector<SparseMatCore::SparseMatRow*>::const_iterator rowiter;
  SparseMatCore::SparseMatRow::const_iterator coliter;
public:
  SparseMatConstIterator(const SparseMat);
  ~SparseMatConstIterator();
  SparseMatConstIterator &operator++();
  unsigned int row() const;
  unsigned int col() const;
  double value() const;
  bool done() const { return *this == mat.end(); }
  double operator*() const { return value(); }
  bool operator==(const SparseMatConstIterator&) const;
  bool operator!=(const SparseMatConstIterator&) const;
  bool operator==(const SparseMatIterator&) const;
  bool operator!=(const SparseMatIterator&) const;
  friend class SparseMat;
  friend class SparseMatCore;
  friend class SparseMatRowConstIterator;
  friend class SparseMatIterator;
  friend std::ostream& operator<<(std::ostream&, const SparseMatConstIterator&);
};

class SparseMatRowIterator {
private:
  SparseMat mat;
  unsigned int row_;
  SparseMatCore::SparseMatRow::iterator coliter;
public:
  SparseMatRowIterator(SparseMat mat, unsigned int r);
  // When initialized with a SparseMatIterator, the row iterator
  // starts at the given iterator's position and goes to the end of
  // the row.
  SparseMatRowIterator(SparseMatIterator&);
  ~SparseMatRowIterator();
  SparseMatRowIterator &operator++();
  SparseMatRowIterator &operator--();
  unsigned int row() const { return row_; }
  unsigned int col() const;
  double &value();
  bool done() const;
  double &operator*() { return value(); }
  bool operator==(const SparseMatRowIterator&) const;
  bool operator!=(const SparseMatRowIterator&) const;
  bool operator==(const SparseMatRowConstIterator&) const;
  bool operator!=(const SparseMatRowConstIterator&) const;
  friend class SparseMat;
  friend class SparseMatCore;
  friend class SparseMatRowConstIterator;
  friend std::ostream& operator<<(std::ostream&, const SparseMatRowIterator&);
};

class SparseMatRowConstIterator {
private:
  const SparseMat mat;
  unsigned int row_;
  SparseMatCore::SparseMatRow::const_iterator coliter;
public:
  SparseMatRowConstIterator(const SparseMat mat, unsigned int r);
  // When initialized with a SparseMatIterator, the row iterator
  // starts at the given iterator's position and goes to the end of
  // the row.
  SparseMatRowConstIterator(const SparseMatConstIterator&);
  ~SparseMatRowConstIterator();
  SparseMatRowConstIterator &operator++();
  SparseMatRowConstIterator &operator--();
  unsigned int row() const { return row_; }
  unsigned int col() const;
  double value() const;
  bool done() const { return *this == mat.end(row_); }
  double operator*() const { return value(); }
  bool operator==(const SparseMatRowConstIterator&) const;
  bool operator!=(const SparseMatRowConstIterator&) const;
  bool operator==(const SparseMatRowIterator&) const;
  bool operator!=(const SparseMatRowIterator&) const;
  friend class SparseMat;
  friend class SparseMatCore;
  friend class SparseMatRowIterator;
  friend std::ostream& operator<<(std::ostream&,
				  const SparseMatRowConstIterator&);
};

std::ostream& operator<<(std::ostream&, const SparseMatIterator&);
std::ostream& operator<<(std::ostream&, const SparseMatConstIterator&);
std::ostream& operator<<(std::ostream&, const SparseMatRowIterator&);
std::ostream& operator<<(std::ostream&, const SparseMatRowConstIterator&);
std::ostream& operator<<(std::ostream&, const SparseMatCore::Entry&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SparseMat identityMatrix(unsigned int);
SparseMat mistakenIdentityMatrix(unsigned int);

long nSparseMatCores();

#endif // SPARSEMAT_H
