// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/oofcerr.h"
#include "engine/sparsemat.h"
#include "engine/dofmap.h"
#include "eigen/unsupported/Eigen/SparseExtra"
#include <iostream>
#include <fstream>
#ifndef HAVE_SSTREAM
#include <strstream.h
#else
#include <sstream>
#endif // HAVE_SSTREAM

SparseMat::SparseMat() {
  // oofcerr << "SparseMat::ctor 0: " << this << std::endl;
}

SparseMat::SparseMat(unsigned int nr, unsigned int nc)
  : data(nr, nc)
{
  // oofcerr << "SparseMat::ctor 1: " << this << std::endl;
}

// Construct by extraction from an existing matrix.
SparseMat::SparseMat(const SparseMat& source,
                     const DoFMap& rowmap,
                     const DoFMap& colmap) 
  : data(rowmap.range(), colmap.range())
{
  // oofcerr << "SparseMat::ctor 2: this=" << this << std::endl;

  // rowmap[i] is the row of the submatrix corresponding to row i of
  // mat. If rowmap[i] == -1, then row i should not be included in the
  // submatrix. If rowmap[i] == rowmap[j], then rows i and j of mat are
  // added together in the submatrix. Likewise for columns.

  auto from = source.data; 
  for (int k = 0; k < from.outerSize(); ++k) {
    for (InnerIter it(from, k); it; ++it) {
      assert(it.row() < rowmap.domain());
      assert(it.col() < colmap.domain());
      int i = rowmap[it.row()];
      assert(i < (int) rowmap.range());
      if (i >= 0) {
        int j = colmap[it.col()];
        assert(j < (int) colmap.range() && j >= -1);
        if (j >= 0)
          insert(i, j, it.value());
      }
    }
  }
  make_compressed();
}

SparseMat::SparseMat(const SparseMat &x)
  : data(x.data)
{
  // oofcerr << "SparseMat::copy ctor: " << &x << " --> " << this << std::endl;
}

SparseMat::SparseMat(SparseMat &&x)
  : data(std::move(x.data))
{
  // oofcerr << "SparseMat::move ctor: " << &x << " --> " << this << std::endl;
}

SparseMat::~SparseMat() {
  // oofcerr << "SparseMat::dtor: this=" << this << std::endl;
}

void SparseMat::set_from_triplets(std::vector<Triplet>& tris) {
  // Initialize this sparse matrix from treiplets like (row, col,
  // value). For triplets having the same row# and col#, add them
  // together.
  data.setFromTriplets(tris.begin(), tris.end(),
    [] (const double& a, const double& b) { return a+b; });
}

bool SparseMat::is_nonempty_row(int i) const {
  assert(i >=0 && i <= nrows());
  Eigen::SparseVector<double> row = data.row(i);
  return row.nonZeros() != 0 ? true : false;
}

bool SparseMat::is_nonempty_col(int i) const {
  assert(i >= 0 && i <= ncols());
  Eigen::SparseVector<double> col = data.col(i);
  return col.nonZeros() != 0 ? true : false;
}

SparseMat SparseMat::lower() const {
  SparseMat tmp;
  tmp.data = data.triangularView<Eigen::Lower>();
  return tmp;
}

SparseMat SparseMat::unit_lower() const {
  SparseMat tmp;
  tmp.data = data.triangularView<Eigen::UnitLower>();
  return tmp;
}

SparseMat SparseMat::upper() const {
  SparseMat tmp;
  tmp.data = data.triangularView<Eigen::Upper>();
  return tmp;
}

SparseMat SparseMat::unit_upper() const {
  SparseMat tmp;
  tmp.data = data.triangularView<Eigen::UnitUpper>();
  return tmp;
}

SparseMat SparseMat::transpose() const {
  SparseMat tmp;
  tmp.data = data.transpose();
  return tmp;
}

SparseMat& SparseMat::operator*=(double scalar) {
  data *= scalar;
  return *this;
}

SparseMat& SparseMat::operator/=(double scalar) {
  data /= scalar;
  return *this;
}

SparseMat& SparseMat::operator+=(const SparseMat& other) {
  data += other.data;
  return *this;
}

SparseMat& SparseMat::operator-=(const SparseMat& other) {
  data -= other.data;
  return *this;
}

SparseMat SparseMat::operator*(double scalar) const {
  SparseMat tmp;
  tmp.data = data * scalar;
  return tmp;
}

SparseMat SparseMat::operator*(const SparseMat& other) const {
  SparseMat tmp;
  tmp.data = data * other.data;
  return tmp;
}

DoubleVec SparseMat::operator*(const DoubleVec& vec) const {
  DoubleVec tmp;
  tmp.data = data * vec.data;
  return tmp;
}

SparseMat& SparseMat::add(double scalar, const SparseMat& other) {
  // TODO(lizhong): inplace operation
  data += other.data * scalar;
  return *this;
}

DoubleVec SparseMat::trans_mult(const DoubleVec& x) const {
  DoubleVec result = DoubleVec(data.cols(), 0.0);
  axpy_trans(1.0, x, result);
  return result;
}

void SparseMat::axpy(double alpha, const DoubleVec &x, DoubleVec &y) const {
  // TODO(lizhong): inplace operation
  // adds alpha*M*x to y.
  y.data = data * x.data * alpha + y.data;
}

void SparseMat::axpy_trans(double alpha, const DoubleVec &x, DoubleVec &y) const {
  // TODO(lizhong): inplace operation
  // adds alpha*transpose(M)*x to y.
  y.data = data.transpose() * x.data * alpha + y.data;
}

void SparseMat::solve_lower_triangle(const DoubleVec& rhs, DoubleVec& x) const {
  // Solve a lower triangular matrix. rhs and x can be the same
  // vector.
  assert(is_lower_triangular(true));
  x.data = data.triangularView<Eigen::Lower>().solve(rhs.data);
}

void SparseMat::solve_lower_triangle_unitd(const DoubleVec& rhs, DoubleVec& x) const {
  // Solve a lower triangular matrix assuming that the diagonal
  // elements are 1.0.  rhs and x can be the same vector.
  assert(is_lower_triangular(false)); // false ==> no diagonal elements allowed
  x.data = data.triangularView<Eigen::UnitLower>().solve(rhs.data);
}

void SparseMat::solve_lower_triangle_trans(const DoubleVec& rhs, DoubleVec& x) const {
  // Solve the transpose of a lower triangular matrix with explicitly
  // stored diagonal elements.  rhs and x can be the same vector.
  assert(is_lower_triangular(true));
  x.data = data.triangularView<Eigen::Lower>().transpose().solve(rhs.data);
}

void SparseMat::solve_lower_triangle_trans_unitd(const DoubleVec& rhs, DoubleVec& x) const {
  // Solve a lower triangular matrix assuming that the diagonal
  // elements are 1.0.  rhs and x can be the same vector.
  assert(is_lower_triangular(false)); // false ==> no diagonal elements allowed
  x.data = data.triangularView<Eigen::UnitLower>().transpose().solve(rhs.data);
}

void SparseMat::solve_upper_triangle(const DoubleVec& rhs, DoubleVec& x) const {
  // Solve an upper triangular matrix with explicit diagonal elements.
  // rhs and x can be the same vector.
  assert(is_upper_triangular(true));
  x.data = data.triangularView<Eigen::Upper>().solve(rhs.data);
}

void SparseMat::solve_upper_triangle_trans(const DoubleVec& rhs, DoubleVec& x) const {
  // Solve the transpose of an upper triangular matrix with explicit
  // diagonal elements.  rhs and x can be the same vector.
  assert(is_upper_triangular(true));
  x.data = data.triangularView<Eigen::Upper>().transpose().solve(rhs.data);
}

void SparseMat::tile(int i, int j, const SparseMat &other) {
  // TODO(lizhong): improve the performance
  // Add other to this, offset by i rows and j columns.
  assert(i + other.nrows() <= nrows());
  assert(j + other.ncols() <= ncols());
  
  auto from = other.data;
  for (int k = 0; k < from.outerSize(); ++k) {
    for (InnerIter it(from, k); it; ++it) {
      int ii = it.row() + i;
      int jj = it.col() + j;
      data.coeffRef(ii, jj) +=  it.value();
    }
  }
}

SparseMat::iterator SparseMat::begin() {
  return iterator(*this);
}

SparseMat::iterator SparseMat::end() {
  iterator it(*this);
  it.to_end();
  return it;
}

SparseMat::const_iterator SparseMat::begin() const {
  return const_iterator(*this);
}

SparseMat::const_iterator SparseMat::end() const {
  const_iterator it(*this);
  it.to_end();
  return it;
}

bool SparseMat::is_lower_triangular(bool diag) const {
  if (diag) { // diagonal elements allowed
    for (int k = 0; k < data.outerSize(); ++k) {
      for (InnerIter it(data, k); it; ++it) 
        if (it.row() < it.col())
          return false;
    }
  }
  else { // no diagonal elements allowed
    for (int k = 0; k < data.outerSize(); ++k) {
      for (InnerIter it(data, k); it; ++it) 
        if (it.row() <= it.col()) {
          return false;
	}
    }
  }
  return true;
}

bool SparseMat::is_upper_triangular(bool diag) const {
  if (diag) { // diagonal elements allowed
    for (int k = 0; k < data.outerSize(); ++k) {
      for (InnerIter it(data, k); it; ++it)
        if (it.row() > it.col())
          return false;
    }
  }
  else { // no diagonal elements allowed
    for (int k = 0; k < data.outerSize(); ++k) {
      for (InnerIter it(data, k); it; ++it)
        if (it.row() >= it.col())
          return false;
    }
  }
  return true;
}

bool SparseMat::is_symmetric(double tolerance) const {
  if (data.rows() != data.cols())
    return false;

  for (int k = 0; k < data.outerSize(); ++k) {
    for (InnerIter it(data, k); it; ++it) {
      double e1 = it.value();    
      double e2 = data.coeff(it.col(), it.row());
      if (fabs(e1-e2) > 0.5*tolerance*(fabs(e1)+fabs(e2)) 
        && fabs(e1-e2) > tolerance) {
        // not symetric
        //std::cerr << "Matrix is not symmetric:"
      	//    << " (" << it.row() << "," << it.col() << ")=" << e1 
      	//    << " (" << it.col() << "," << it.row() << ")=" << e2
      	//    << " difference=" << e1 - e2
      	//    << std::endl;
        return false;
      }
    }
  }
  return true;
}

bool SparseMat::is_positive_definite() const {
  // The LL' decomposition (Cholesky decomposition) fails if the
  // matrix is not positive definite, and Eigen will detect that.
  // This is probably a time consuming test.
  Eigen::SimplicialLLT<ESMat> llt(data);
  return llt.info() != Eigen::NumericalIssue;
}

const std::string SparseMat::str() const {
  std::ostringstream os;
  os << *this;
  return os.str();
}

SparseMat identityMatrix(int size) {
  // make an identity matrix
  SparseMat mat(size, size);
  mat.reserve(size);
  for (int i = 0; i < size; ++i)
    mat.insert(i, i, 1);
  return mat;
}

std::ostream& operator<<(std::ostream& os, const SparseMat& smat) {
  auto mat = smat.data;
  os << mat.rows() << " " << mat.cols() << " " << mat.nonZeros() << std::endl;
  for (int k = 0; k < mat.outerSize(); ++k) {
    for (SparseMat::InnerIter it(mat, k); it; ++it)
      os << it.row() << " " << it.col() << " "
         << it.value() << std::endl;
  }
  return os;
}

bool save_market_mat(const SparseMat& mat, const std::string& filename, int sym) {
  return Eigen::saveMarket(mat.data, filename, sym);
}

bool load_market_mat(SparseMat& mat, const std::string& filename) {
  return Eigen::loadMarket(mat.data, filename);
}

bool save_mat(const SparseMat& mat, const std::string& filename, int precision, int sym) {
  //TODO(lizhong): support symmetric matrix

  // Note: matrix needs to be compressed

  std::ofstream fs(filename);

  // floatfield set to scientific
  fs.setf(std::ios::scientific, std::ios::floatfield);
  fs.precision(precision);

  // save matrix row by row 

  fs << mat.nrows() << " " << mat.ncols() << " "
     << mat.nnonzeros() << std::endl;
     
  auto& m = const_cast<SparseMat&>(mat);
  if (ESMat::IsRowMajor) {
    // TODO(lizhong): use a const iterator here
    for (auto it = m.begin(); it != m.end(); ++it) {
      fs << it.row() << " " << it.col() << " "
         << it.value() << std::endl;
    }
  } else {
    typedef std::tuple<int, int, double> Tri;
    std::vector<Tri> coeffs;
    coeffs.reserve(m.nnonzeros());
    for (auto it = m.begin(); it != m.end(); ++it)
      coeffs.emplace_back(it.row(), it.col(), it.value());

    std::sort(coeffs.begin(), coeffs.end(),
      [](const Tri& a, const Tri& b) -> bool {
        if (std::get<0>(a) < std::get<0>(b))
          return true;
        else if (std::get<0>(a) == std::get<0>(b) &&
          std::get<1>(a) < std::get<1>(b))
          return true;
        return false;
      });

    for (auto& tri : coeffs) {
      fs << std::get<0>(tri) << " " << std::get<1>(tri) << " "
         << std::get<2>(tri) << std::endl;
    }
  }
  return true;
}

bool load_mat(SparseMat& mat, const std::string& filename) {
  
  std::ifstream fs(filename);
  std::string line;
  
  // Ignore the comments at the begining of file
  while (!fs.eof()) {
    std::getline(fs, line);
    // '#' is the comment flag
    if (line[0] != '#')
      break;
  }
  // extract matrix size info
  int nr, nc, nnz;
  std::stringstream ss;
  ss << line;
  ss >> nr >> nc >> nnz;

  mat.resize(nr, nc);

  // read matrix elements
  std::vector<Triplet> trips;
  trips.reserve(nnz);
  int r, c;
  double val;
  for (int i = 0; i < nnz; i++) {
    fs >> r >> c >> val;
    trips.emplace_back(r, c, val);
  }

  mat.set_from_triplets(trips);
  return true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template<typename MT, typename VT>
SparseMatIterator<MT, VT>::SparseMatIterator(MT& spmat)
  : mat(spmat), in_idx(0), out_idx(0) {
  val_ptr = mat.data.valuePtr();
  in_ptr  = (int*)mat.data.innerIndexPtr();
  out_ptr = (int*)mat.data.outerIndexPtr();

  if (mat.data.nonZeros() > 0) {
    // move oud_idx to the first non-epmty row/column
    while (out_ptr[out_idx] == out_ptr[out_idx+1])
        out_idx += 1;
  }
}

template<typename MT, typename VT>
int SparseMatIterator<MT, VT>::row() const {
  assert(!done());
  return ESMat::IsRowMajor ? out_idx : in_ptr[in_idx];  
}

template<typename MT, typename VT>
int SparseMatIterator<MT, VT>::col() const {
  assert(!done());
  return ESMat::IsRowMajor ? in_ptr[in_idx] : out_idx;  
}

template<typename MT, typename VT>
VT& SparseMatIterator<MT, VT>::value() const {
  assert(!done());
  return val_ptr[in_idx];
}

template<typename MT, typename VT>
bool SparseMatIterator<MT, VT>::done() const {
  if (in_idx < mat.data.nonZeros()) {
    return false;   
  }
  return true;
}

template<typename MT, typename VT>
SparseMatIterator<MT, VT>& SparseMatIterator<MT, VT>::operator++() {
  // TODO: Can we use Eigen::InnerIterator here?
  int last = mat.data.nonZeros()-1;
  if (in_idx <= last) {
    in_idx += 1;
    if (in_idx == out_ptr[out_idx + 1]) {
      // reached the end of a row or a column,
      // move to next non-empty row/column.
      do {
        out_idx += 1;
      } while (out_ptr[out_idx] == out_ptr[out_idx+1]);
    }
  }
  return *this;
}

// template<typename MT, typename VT>
// SparseMatIterator<MT, VT>& SparseMatIterator<MT, VT>::operator--() {
//   if(in_idx > 0) {
//     in_idx -= 1;
//     if(in_idx == 0) {
//       // reached the beginning of a row or a column.  Move to previous
//       // non-empty row/column.
//       do {
// 	out_idx -= 1;
//       } while(
//     }
//   }
  
// }

template<typename MT, typename VT>
VT& SparseMatIterator<MT, VT>::operator*() const {
  return value();
}

template<typename MT, typename VT>
bool SparseMatIterator<MT, VT>::operator==(const SparseMatIterator& other) const {
  return (&mat==&other.mat && in_idx==other.in_idx) ? true : false;
}

template<typename MT, typename VT> 
bool SparseMatIterator<MT, VT>::operator!=(const SparseMatIterator& other) const {
  return (&mat==&other.mat && in_idx!=other.in_idx) ? true : false;
}

template<typename MT, typename VT> 
bool SparseMatIterator<MT, VT>::operator<(const SparseMatIterator& other) const {
  return (&mat==&other.mat && in_idx<other.in_idx) ? true : false;
}

template<typename MT, typename VT>
void SparseMatIterator<MT, VT>::to_end() {
  // move this iterator to the end.
  in_idx = mat.data.nonZeros();
}

template<typename MT, typename VT>
void SparseMatIterator<MT, VT>::print_indices() const {
  // print compressed matrix' internal arrays for debug purpose
  for (int i = 0; i <= mat.data.nonZeros(); i++) {
      std::cout << val_ptr[i] << ", ";
  }
  std::cout << std::endl;
  for (int i = 0; i <= mat.data.nonZeros(); i++) {
      std::cout << in_ptr[i] << ", ";
  }
  std::cout << std::endl;
  for (int i = 0; i <= mat.data.outerSize(); i++) {
      std::cout << out_ptr[i] << ", ";
  }
  std::cout << std::endl;
}

// Instantiate the SparseMatIterator template
template class SparseMatIterator<SparseMat, double>;
template class SparseMatIterator<const SparseMat, const double>;


