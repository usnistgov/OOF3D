// -*- C++ -*-
// $RCSfile: sparsemat.h,v $
// $Revision: 1.17 $
// $Author: lnz5 $
// $Date: 2015/08/19 20:43:09 $

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

#include <vector>
#include <deque>

class SparseMat;
class SparseMatConstIterator;
class SparseMatIterator;
class SparseMatRowConstIterator;
class SparseMatRowIterator;

#ifndef SPARSEMAT_H
#define SPARSEMAT_H

class DoFMap;
class DoubleVec;

class SparseMat {
public:
  class Entry {
  public:
    unsigned int col;		// column
    double val;		// value
    Entry() : col(123456789), val(-123.) {}
    Entry(unsigned int col, double val) : col(col), val(val) {}
    Entry(const Entry &other) : col(other.col), val(other.val) {}
  };

  typedef std::vector<Entry> SparseMatRow;

  SparseMat();
  SparseMat(unsigned int nr, unsigned int nc);
  // Construct by extraction from an existing matrix.
  SparseMat(const SparseMat&, const DoFMap&, const DoFMap&);
  SparseMat(const SparseMat&) = default;
  SparseMat(SparseMat&&) = default; // move constructor
  SparseMat& operator=(const SparseMat&) = default;
  SparseMat& operator=(SparseMat&&) = default; // move assignment
  ~SparseMat() = default;

  SparseMat clone() const;

  // Matrix construction functions

  // nrows() and ncols() might not always do what you expect them to
  // do. The nominal size of the matrix is determined by the maxium of
  // (1) the sizes passed in to the constructor or to resize(), (2)
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

  // Matrix operations

  SparseMat transpose() const;
  
  SparseMat &operator*=(double);
  SparseMat &operator+=(const SparseMat&);
  SparseMat &add(double, const SparseMat&); // scale and add

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

  double norm() const;

  // Triangular solvers.
  void solve_lower_triangle(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_unitd(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_trans(const DoubleVec&, DoubleVec&) const;
  void solve_lower_triangle_trans_unitd(const DoubleVec&, DoubleVec&) const;
  void solve_upper_triangle(const DoubleVec&, DoubleVec&) const;
  void solve_upper_triangle_trans(const DoubleVec&, DoubleVec&) const;

  // Merge multiple matrices at once, which is more efficient
  // than adding them together one by one.
  // Assuming the matrix merging to is empty (no entries).
  void merge(const std::vector<SparseMat>& ms);

  void tile(unsigned int i, unsigned int j, const SparseMat &other);

  // It's assumed that the callers of is_nonempty_row and
  // is_nonempty_col know the nominal size of the matrix they're working
  // with, so if an index is out of range we just assume that it's an
  // empty row or column that the matrix doesn't know about.
  bool is_nonempty_row(unsigned int) const;
  bool is_nonempty_col(unsigned int) const;
  bool empty() const { return nnonzeros() == 0; }

  // Iterators

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

  // Debugging routines.  

  // diag==true means the diagonal is present.
  bool is_lower_triangular(bool diag) const;
  bool is_upper_triangular(bool diag) const;
  bool unique_indices() const;
  bool is_symmetric(double tolerance) const;
  DoubleVec inefficient_get_column(unsigned int) const;
  // void sanityCheck() const;

private:
  // data is stored as a vector of rows.
  std::vector<SparseMatRow> data;
  // nonempty_col keeps track of which columns have data in them.
  std::vector<bool> nonempty_col;

  // nnz_ is the number of entries, which is only equal to the number
  // of nonzeros after consolidate() has been called.
  unsigned int nnz_; 
  unsigned int nrows_, ncols_;
  bool consolidated_;

  friend class SparseMatConstIterator;
  friend class SparseMatIterator;
  friend class SparseMatRowConstIterator;
  friend class SparseMatRowIterator;
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

// TODO: SparseMatIterator and SparseMatConstIterator share a lot of
// mostly trivial code.  Is it worth giving them a common base class?
// Same for SparseMatRowIterator and SparseMatRowConstIterator.

class SparseMatIterator {
private:
  SparseMat& mat;
  std::vector<SparseMat::SparseMatRow>::iterator rowiter;
  SparseMat::SparseMatRow::iterator coliter;
public:
  SparseMatIterator(SparseMat&);
  ~SparseMatIterator();
  SparseMatIterator &operator++();
  unsigned int row() const;
  unsigned int col() const;
  double &value() const;
  bool done() const;
  double &operator*() const { return value(); }
  bool operator==(const SparseMatIterator&) const;
  bool operator!=(const SparseMatIterator&) const;
  bool operator<(const SparseMatIterator&) const;
  bool operator>=(const SparseMatIterator&) const;
  bool operator==(const SparseMatConstIterator&) const;
  bool operator!=(const SparseMatConstIterator&) const;
  bool operator<(const SparseMatConstIterator&) const;
  bool operator>=(const SparseMatConstIterator&) const;
  friend class SparseMat;
  friend class SparseMatRowIterator;
  friend class SparseMatConstIterator;
  friend std::ostream& operator<<(std::ostream&, const SparseMatIterator&);
};

class SparseMatConstIterator {
private:
  const SparseMat& mat;
  std::vector<SparseMat::SparseMatRow>::const_iterator rowiter;
  SparseMat::SparseMatRow::const_iterator coliter;
public:
  SparseMatConstIterator(const SparseMat&);
  ~SparseMatConstIterator();
  SparseMatConstIterator &operator++();
  unsigned int row() const;
  unsigned int col() const;
  double value() const;
  bool done() const { return *this == mat.end(); }
  double operator*() const { return value(); }
  bool operator==(const SparseMatConstIterator&) const;
  bool operator!=(const SparseMatConstIterator&) const;
  bool operator<(const SparseMatConstIterator&) const;
  bool operator>=(const SparseMatConstIterator&) const;
  bool operator==(const SparseMatIterator&) const;
  bool operator!=(const SparseMatIterator&) const;
  bool operator<(const SparseMatIterator&) const;
  bool operator>=(const SparseMatIterator&) const;
  friend class SparseMat;
  friend class SparseMatRowConstIterator;
  friend class SparseMatIterator;
  friend std::ostream& operator<<(std::ostream&, const SparseMatConstIterator&);
};

class SparseMatRowIterator {
private:
  SparseMat& mat;
  unsigned int row_;
  SparseMat::SparseMatRow::iterator coliter;
public:
  SparseMatRowIterator(SparseMat& mat, unsigned int r);
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
  bool operator<(const SparseMatRowIterator&) const;
  bool operator>=(const SparseMatRowIterator&) const;
  bool operator==(const SparseMatRowConstIterator&) const;
  bool operator!=(const SparseMatRowConstIterator&) const;
  bool operator<(const SparseMatRowConstIterator&) const;
  bool operator>=(const SparseMatRowConstIterator&) const;
  friend class SparseMat;
  friend class SparseMatRowConstIterator;
  friend std::ostream& operator<<(std::ostream&, const SparseMatRowIterator&);
};

class SparseMatRowConstIterator {
private:
  const SparseMat& mat;
  unsigned int row_;
  SparseMat::SparseMatRow::const_iterator coliter;
public:
  SparseMatRowConstIterator(const SparseMat& mat, unsigned int r);
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
  bool operator<(const SparseMatRowConstIterator&) const;
  bool operator>=(const SparseMatRowConstIterator&) const;
  bool operator==(const SparseMatRowIterator&) const;
  bool operator!=(const SparseMatRowIterator&) const;
  bool operator<(const SparseMatRowIterator&) const;
  bool operator>=(const SparseMatRowIterator&) const;
  friend class SparseMat;
  friend class SparseMatRowIterator;
  friend std::ostream& operator<<(std::ostream&,
				  const SparseMatRowConstIterator&);
};

std::ostream& operator<<(std::ostream&, const SparseMatIterator&);
std::ostream& operator<<(std::ostream&, const SparseMatConstIterator&);
std::ostream& operator<<(std::ostream&, const SparseMatRowIterator&);
std::ostream& operator<<(std::ostream&, const SparseMatRowConstIterator&);
std::ostream& operator<<(std::ostream&, const SparseMat::Entry&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SparseMat identityMatrix(unsigned int);
SparseMat mistakenIdentityMatrix(unsigned int);

#endif // SPARSEMAT_H
