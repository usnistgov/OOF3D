// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SPARSEMAT_H
#define SPARSEMAT_H

#include <oofconfig.h>
#include <sstream>
#include "eigen/Eigen/SparseCore"
#include "common/doublevec.h"

class DoFMap;
template<typename MT, typename VT> class SparseMatIterator;
template<typename MT, typename VT> class SparseMatRowConstIterator;
template<typename MT, typename VT> class SparseMatRowIterator;
enum class Precond;
template<typename Derived> class IterativeSolver;
template<typename Derived> class DirectSolver;

typedef Eigen::Triplet<double> Triplet;
typedef Eigen::SparseMatrix<double, Eigen::ColMajor> ESMat;

/* SparseMat class wraps Eigen's SparseMatrix */

class SparseMat {
private:
  ESMat data;   // Eigen's sparse matrix 

public:
  typedef ESMat::InnerIterator InnerIter;

  SparseMat() = default;
  SparseMat(unsigned int nr, unsigned int nc) : data(nr, nc) {}
  SparseMat(const SparseMat&, const DoFMap&, const DoFMap&);
  SparseMat(const SparseMat&) = default;
  SparseMat(SparseMat&&) = default; // move constructor
  SparseMat& operator=(const SparseMat&) = default;
  SparseMat& operator=(SparseMat&&) = default; // move assignment
  ~SparseMat() = default;
  SparseMat clone() const { return *this; }
  void set_from_triplets(std::vector<Triplet>&);

  // TODO(lizhong): inline possible methods

  /* Matrix property methods */

  int nrows() const { return data.rows(); }
  int ncols() const { return data.cols(); }
  int nnonzeros() const { return data.nonZeros(); }
  void resize(int nr, int nc) { data.resize(nr, nc); }
  void reserve(int size) { data.reserve(size); }
  void insert(int ir, int ic, double val) { data.coeffRef(ir, ic) += val; }
  bool empty() const { return data.nonZeros() == 0; }
  double coeff(int ir, int ic) { return data.coeff(ir, ic); }
  double& coeff_ref(int ir, int ic) { return data.coeffRef(ir, ic); }
  void make_compressed() { data.makeCompressed(); }
  bool is_compressed() { return data.isCompressed(); }
  bool is_nonempty_row(int) const;
  bool is_nonempty_col(int) const;

  SparseMat lower() const;
  SparseMat unit_lower() const;
  SparseMat upper() const;
  SparseMat unit_upper() const;

  /* Arithmetic operations */

  double norm() const { return data.norm(); }
  SparseMat transpose() const;

  SparseMat& operator*=(double);
  SparseMat& operator/=(double);

  SparseMat& operator+=(const SparseMat&);
  SparseMat& operator-=(const SparseMat&);
  SparseMat operator*(double scalar) const;
  SparseMat operator*(const SparseMat&) const;
  DoubleVec operator*(const DoubleVec&) const;

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

  void tile(int, int, const SparseMat&);

  /* Iterators */

  // TODO(lizhong): Iterator only works with compressed matrix?
  friend class SparseMatIterator<SparseMat, double>;
  friend class SparseMatIterator<const SparseMat, const double>;
  typedef SparseMatIterator<SparseMat, double> iterator;
  typedef SparseMatIterator<const SparseMat, const double> const_iterator;
  iterator begin();
  iterator end();
  const_iterator begin() const;
  const_iterator end() const;

  /* Debugging routines. */

  bool is_lower_triangular(bool diag) const;
  bool is_upper_triangular(bool diag) const;
  bool is_symmetric(double tolerance) const;
  /*
  bool unique_indices() const;
  DoubleVec inefficient_get_column(unsigned int) const;

  //void merge(const std::vector<SparseMat>& ms);
  //void tile(unsigned int i, unsigned int j, const SparseMat &other);
  */

  const std::string str() const;

  template<typename Derived> friend class IterativeSolver;
  template<typename Derived> friend class DirectSolver;
  friend std::ostream& operator<<(std::ostream&, const SparseMat&);
  friend bool load_market_mat(SparseMat& mat, const std::string& filename);
  friend bool save_market_mat(const SparseMat&, const std::string&, int);
};

SparseMat identityMatrix(int);
bool save_mat(const SparseMat& mat, const std::string& filename,
              int precision=13, int sym = 0);
bool load_mat(SparseMat& mat, const std::string& filename);
bool save_market_mat(const SparseMat& mat, const std::string& filename,
		     int sym = 0);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO(lizhong): guess value type from matrix type
template<typename MT, typename VT>
class SparseMatIterator {
private:
  MT& mat;

  // This iterator is implemented based on the storage scheme of compressed
  // sparse matrices (row or column major) in Eigen.
  // The compressed sparse matrix consist of three compact arrays:
  // - Values: stores the coefficient values of the non-zeros.
  // - InnerIndices: stores the row (resp. column) indices of the non-zeros.
  // - OuterStarts: stores for each column (resp. row) the index of the
  //                first non-zero in the previous two arrays.

  // Note: Currently, in order to use this iterator, the reference
  // sparse matrix has to be compressed first.
  // TODO(lizhong): make it work with uncompressed sparse matrix.

  VT* val_ptr;     // pointer of the Values array
  int* in_ptr;     // pointer of the InnerIndices array 
  int* out_ptr;    // pointer of the OuterStarts array
  int  in_idx;     // current index in the InnerIndices
  int  out_idx;    // current index in the OuterIndeces

public:
  SparseMatIterator(MT&);

  int row() const;
  int col() const;
  VT& value() const;
  bool done() const;

  SparseMatIterator& operator++();
  // SparseMatIterator& operator--();
  VT& operator*() const;

  bool operator==(const SparseMatIterator&) const;
  bool operator!=(const SparseMatIterator&) const;
  bool operator<(const SparseMatIterator&) const;
  //bool operator>=(const SparseMatIterator&) const;

  /* Debug */

  void print_indices() const; // print the three compact array.

  friend class SparseMat;
  friend std::ostream& operator<<(std::ostream& os,
    const SparseMatIterator<MT, VT>& it) {
    os << it.row() << " " << it.col() << " " << it.value();
    return os;
  }

private:
  void to_end();
};

#endif // SPARSEMAT_H_
