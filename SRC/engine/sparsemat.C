// -*- C++ -*-
// $RCSfile: sparsemat.C,v $
// $Revision: 1.27 $
// $Author: lnz5 $
// $Date: 2015/08/19 20:43:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/doublevec.h"
#include "common/ooferror.h"
#include "common/printvec.h"
#include "common/progress.h"
#include "common/tostring.h"
#include "engine/dofmap.h"
#include "engine/sparsemat.h"
#include <algorithm>		// for std::sort
#include <fstream>
#include <iostream>
#include <math.h>
#include <set>
#include <unordered_map>
#include <map>

SparseMat::SparseMat()
  : nnz_(0),
    nrows_(0),
    ncols_(0),
    consolidated_(true)
{
}

SparseMat::SparseMat(unsigned int nr, unsigned int nc)
  : data(nr),
    nonempty_col(nc),
    nnz_(0), 
    nrows_(nr),
    ncols_(nc),
    consolidated_(true)
{
}

// Construct by extraction from another matrix.  rowmap[i] is the row
// of the submatrix corresponding to row i of mat.  If rowmap[i] ==
// -1, then row i should not be included in the submatrix.  If
// rowmap[i] == rowmap[j], then rows i and j of mat are added together
// in the submatrix.  Likewise for columns.

SparseMat::SparseMat(const SparseMat &source,
			     const DoFMap &rowmap,
			     const DoFMap &colmap)
  : nnz_(0),
    nrows_(rowmap.range()),
    ncols_(colmap.range()),
    consolidated_(true)	       // true, because mtx is initially empty
{
  data.resize(nrows_);
  nonempty_col.resize(ncols_, false);
  
  for(SparseMatConstIterator ij=source.begin(); ij<source.end(); ++ij) {
    assert(ij.row() < rowmap.domain()); // row is unsigned, dont check >= 0
    int i = rowmap[ij.row()];

    assert(data.size()!=0 || i==-1);
    assert(i < (int) rowmap.range());

    if(i >= 0) {
      assert(ij.col() < colmap.domain());
      int j = colmap[ij.col()];
      assert(j < (int) colmap.range() && j >= -1);
      if(j >= 0) {
	insert(i, j, *ij);	// unsets consolidated_.
      }
    }
  }
  consolidate();
}

void SparseMat::insert(unsigned int i, unsigned int j, double val) {
  resize(i + 1, j + 1);
  assert(i < nrows_ && j < ncols_);
  data[i].emplace_back(j, val);
  nonempty_col[j] = true;
  consolidated_ = false;
  ++nnz_;
}

void SparseMat::resize(unsigned int nr, unsigned int nc) {
  // resize doesn't do anything if the new size is smaller than the
  // current size.  It never deletes data.  TODO NITPICK: This
  // actually is not true, since the routine compares against nrows
  // and cols, but the sizes of the ST vectors are not constrained to
  // be equal to nrows and cols.  If the array somehow became much
  // larger, this call could shrink it.

  if (nr > nrows_) {
    assert( nr >= data.size() );
    data.resize(nr);
    nrows_ = nr;
  }

  if (nc > ncols_) {
    assert( nc >= nonempty_col.size() );
    ncols_ = nc;
    nonempty_col.resize(nc, false);
  }
}

void SparseMat::consolidate_row(unsigned int rdx) {
  // Consolidate a single row of a SparseMat.

  class EntrySort {
  public:
    bool operator()(const Entry &a, const Entry&b)
      const
    {
      return a.col < b.col;
    }
  };

  SparseMatRow& row = data[rdx];
  int startsize = row.size();
  if (startsize > 1 ) {
    std::sort(row.begin(), row.end(), EntrySort());
    // Add the values in columns with the same index, which are now
    // in consecutive entries.  Store the results in consecutive
    // entries at the *beginning* of the row, overwriting old
    // redundant entries.
    
    // Except, temporarily for debugging, don't actually do this,
    // create a whole new row and replace data[i] with the new
    // one.
    SparseMatRow::iterator src = row.begin(); // beginning of a column
    SparseMatRow newrow;
    // SparseMatRow::iterator target = row.begin(); // store result here
    while(src != row.end()) {
      unsigned int col = (*src).col; // column index
      double sum = (*src).val;
      // SparseMatRow::iterator j = src+1;
      SparseMatRow::iterator j = src;
      ++j;
      // loop over subsequent entries for this column and add values
      for( ; j<row.end() && (*j).col==col; ++j)
	sum += (*j).val;
      // (*target).col = col;
      // (*target).val = sum;
      // ++target;
      newrow.push_back(Entry(col,sum));
      src = j;
    }
    data[rdx] = std::move(newrow);
  }
  else {
    return;
  }
}

void SparseMat::consolidate() {
  if(!consolidated_) {
    nnz_ = 0;
    #pragma omp parallel for schedule(dynamic, 1)
    for(unsigned int r=0; r<data.size(); r++) {
      consolidate_row(r);
      nnz_ += data[r].size();
    } // end loop over rows
    consolidated_ = true;
  }
}

bool SparseMat::is_nonempty_row(unsigned int r) const {
  return r < data.size() && data[r].size() > 0;
}

bool SparseMat::is_nonempty_col(unsigned int c) const {
  return c < nonempty_col.size() && nonempty_col[c];
}

SparseMat::iterator SparseMat::begin() {
  return SparseMat::iterator(*this);
}

SparseMat::const_iterator SparseMat::begin() const {
  return SparseMat::const_iterator(*this);
}

SparseMat::row_iterator SparseMat::begin(unsigned int i) {
  return SparseMat::row_iterator(*this, i);
}

SparseMat::const_row_iterator SparseMat::begin(unsigned int i) const {
  return SparseMat::const_row_iterator(*this, i);
}

SparseMat::iterator SparseMat::end() {
  iterator iter(*this);
  iter.rowiter = data.end();
  return iter;
}

SparseMat::const_iterator SparseMat::end() const {
  const_iterator iter(*this);
  iter.rowiter = data.end();
  return iter;
}

SparseMat::row_iterator SparseMat::end(unsigned int i) {
  row_iterator iter(*this, i);
  iter.coliter = data[i].end();
  return iter;
}

SparseMat::const_row_iterator SparseMat::end(unsigned int i) const {
  const_row_iterator iter(*this, i);
  iter.coliter = data[i].end();
  return iter;
}

SparseMat &SparseMat::operator*=(double a) {
  for(SparseMatIterator ij=begin(); ij!=end(); ++ij) 
    *ij *= a;
  return *this;
}

SparseMat &SparseMat::operator+=(const SparseMat &other) {
  #pragma omp parallel shared(other)
  {
    #pragma omp for 
    for (size_t i = 0; i < data.size(); ++i) {
      const SparseMatRow& fromRow = other.data[i];
      SparseMatRow& toRow = data[i];
      toRow.reserve(toRow.size() + fromRow.size());
      toRow.insert(toRow.end(), fromRow.begin(), fromRow.end()); 
    }
    consolidated_ = false;

    #pragma omp for
    for (size_t i = 0; i < ncols_; ++i) {
      if (other.nonempty_col[i] == true)
        nonempty_col[i] = true;
    }
  }
  return *this;
}

// Add a scalar multiple of another matrix.
SparseMat &SparseMat::add(double alpha, const SparseMat &other) {
  assert(other.nrows() == nrows_ && other.ncols() == ncols_);
  if(alpha != 1.0) {
    for(const_iterator iter = other.begin(); iter<other.end(); ++iter)
      insert(iter.row(), iter.col(), alpha*iter.value());
  }
  else {			// alpha == 1.0
    for(const_iterator iter = other.begin(); iter<other.end(); ++iter)
      insert(iter.row(), iter.col(), iter.value());
  }
  // TODO OPT: Don't consolidate here -- there might be more additions
  // later.  Consolidate explicitly only.
  consolidate();
  return *this;
}

DoubleVec SparseMat::operator*(const DoubleVec &x) const {
  assert(x.size() == ncols_);
  DoubleVec result(nrows_, 0.0);
  for(unsigned int r=0; r<nrows_; r++) {
    double sum = 0.0;
    const SparseMatRow &row = data[r];
    for(SparseMatRow::const_iterator j=row.begin(); j<row.end(); ++j) {
      assert((*j).col >= 0 && (*j).col < x.size());
      sum += (*j).val * x[(*j).col];
    }
    result[r] = sum;
  }
  return result;
}

DoubleVec SparseMat::trans_mult(const DoubleVec &x) const {
  DoubleVec result(ncols_, 0.0);
  axpy_trans(1.0, x, result);
  return result;
}

SparseMat SparseMat::transpose() const {
  SparseMat result(ncols(), nrows());
  for(SparseMat::const_iterator ij=begin(); ij<end(); ++ij) {
    result.insert(ij.col(), ij.row(), *ij);
  }
  result.set_consolidated(consolidated());
  return result;
}

// Matrix-matrix multiplication, mostly for debugging.  It shouldn't
// be necessary to multiply large sparse matrices very often.  This
// routine first computes the transpose of the right multiplier,
// because it's easier to loop over rows than columns.

SparseMat SparseMat::operator*(const SparseMat &right) const {
  if(!consolidated() || !right.consolidated())
    throw ErrProgrammingError("Attempt to multiply unconsolidated SparseMats!",
			      __FILE__, __LINE__);
  SparseMat result(nrows(), right.ncols());
  const SparseMat rightt = right.transpose();
  for(unsigned int i=0; i<nrows(); i++) {
    for(unsigned int j=0; j<rightt.nrows(); j++) {
      const_row_iterator ai = begin(i);
      const_row_iterator bj = rightt.begin(j);
      while(ai < end(i) && bj < rightt.end(j)) {
	if(ai.col() == bj.col()) {
	  result.insert(i, j, (*ai)*(*bj));
	  ++ai;
	  ++bj;
	}
	else if(ai.col() < bj.col())
	  ++ai;
	else
	  ++bj;
      }
    }
    result.consolidate_row(i);
  }
  // result.consolidate();
  result.consolidated_ = true;
  return result;
}

// Add alpha*this*x to y.

void SparseMat::axpy(double alpha, const DoubleVec &x, DoubleVec &y) const
{
  if(ncols() != x.size() || nrows() != y.size()) {
    std::string msg = "Incompatible sizes in SparseMat::axpy! [" 
      + to_string(nrows()) + "x" + to_string(ncols()) + "] * [" 
      + to_string(x.size()) + "] + [" + to_string(y.size()) + "]";
    throw ErrProgrammingError(msg, __FILE__, __LINE__);
  }
  if(alpha != 1.0) {
    for(unsigned int r=0; r<nrows_; r++) {
      const SparseMatRow &row = data[r];
      double sum = 0.0;
      for(SparseMatRow::const_iterator j=row.begin(); j<row.end(); ++j)
	sum += (*j).val * x[(*j).col];
      y[r] += alpha*sum;
    }
  }
  else {			// alpha == 1.0
    for(unsigned int r=0; r<nrows_; r++) {
      const SparseMatRow &row = data[r];
      double sum = 0.0;
      for(SparseMatRow::const_iterator j=row.begin(); j<row.end(); ++j)
	sum += (*j).val * x[(*j).col];
      y[r] += sum;
    }
  }
}

void SparseMat::axpy_trans(double alpha, const DoubleVec &x, DoubleVec &y)
  const
{
  if(alpha != 1.0) {
    for(unsigned int r=0; r<nrows_; r++) {
      const SparseMatRow &row = data[r];
      for(SparseMatRow::const_iterator j=row.begin(); j<row.end(); ++j)
	y[(*j).col] += alpha * x[r] * (*j).val;
    }
  }
  else {			// alpha == 1.0
    for(unsigned int r=0; r<nrows_; r++) {
      const SparseMatRow &row = data[r];
      for(SparseMatRow::const_iterator j=row.begin(); j<row.end(); ++j)
	y[(*j).col] += x[r] * (*j).val;
    }
  }
}

double SparseMat::norm() const {
  assert(consolidated());
  double sum = 0.0;
  for(SparseMat::const_iterator ij=begin(); ij<end(); ++ij)
    sum += (*ij)*(*ij);
  return sqrt(sum);
}

void SparseMat::solve_lower_triangle_unitd(const DoubleVec &rhs,
					       DoubleVec &x)
  const
{
  // Solve a lower triangular matrix assuming that the diagonal
  // elements are 1.0.  rhs and x can be the same vector.
  assert(is_lower_triangular(false)); // diags aren't stored explicitly
  // x_n = rhs_n - \sum{i=0}^{n-1} L_ni x_i
  for(unsigned int rowno=0; rowno<rhs.size(); rowno++) {
    double sum = 0.0;
    for(const_row_iterator ij=begin(rowno); ij<end(rowno); ++ij)
      sum += (*ij)*x[ij.col()];
    x[rowno] = rhs[rowno] - sum;
  }
}

void SparseMat::solve_lower_triangle(const DoubleVec &rhs, DoubleVec &x)
  const
{
  // Solve a lower triangular matrix. rhs and x can be the same
  // vector.
  assert(is_lower_triangular(true)); // diag elements are stored explicitly
  // x_n = (1/L_nn) (rhs_n - \sum{i=0}^{n-1} L_ni x_i)
  for(unsigned int rowno=0; rowno<rhs.size(); rowno++) {
    double sum = 0.0;
    const_row_iterator ij=--end(rowno);
    double diag = *ij;
    if(diag == 0.0)
      throw ErrSetupError("Zero divisor in solve_lower_triangle");
    for(--ij; ij>=begin(rowno); --ij)
      sum += (*ij)*x[ij.col()];
    x[rowno] = (rhs[rowno] - sum)/diag;
  }
}

void SparseMat::solve_upper_triangle(const DoubleVec &rhs, DoubleVec &x)
  const
{
  // Solve an upper triangular matrix with explicit diagonal elements.
  // rhs and x can be the same vector.
  assert(is_upper_triangular(true));
  
  // x_i = (1/U_ii) (rhs_i - \sum_{n=i+1}^M U_in x_n )
  // rowno must be an int, not an unsigned int, or else rowno>=0 will
  // always be true.
  for(int rowno=int(rhs.size())-1; rowno>=0; rowno--) {
    const_row_iterator ij=begin(rowno);
    double diagterm = *ij;
    if(ij.row() != ij.col() || diagterm == 0.0)
      throw ErrSetupError("Zero divisor in solve_upper_triangle!");
    double sum = rhs[rowno];
    for(++ij; ij<end(rowno); ++ij)
      sum -= (*ij)*x[ij.col()];
    x[rowno] = sum/diagterm;
  }
}

void SparseMat::solve_upper_triangle_trans(const DoubleVec &rhs,
					       DoubleVec &x) const
{
  // Solve the transpose of an upper triangular matrix with explicit
  // diagonal elements.  rhs and x can be the same vector.
  assert(is_upper_triangular(true));

  // x_i = (1/U_ii) (rhs_i - \sum_{j=0}^{i-1} U_ji x_j)

  // Copy rhs into x. This does all of the rhs_i terms.
  if(&x[0] != &rhs[0])
    x = rhs;
  for(unsigned int i=0; i<x.size(); i++) {
    const_row_iterator ji=begin(i); // loop over i^th col of the transpose
    // We're already done with the sums for x_i.
    if(ji.row() != ji.col() || *ji == 0.0)
      throw ErrSetupError("Zero divisor in solve_upper_triangle_trans!");
    x[i] /= *ji; 		// divide by the diagonal
    // Accumulate contributions to later x[i]'s.
    for(++ji; ji<end(i); ++ji)
      x[ji.col()] -= (*ji) * x[i];
  }
}

void SparseMat::solve_lower_triangle_trans(const DoubleVec &rhs,
					       DoubleVec &x) const
{
  // Solve the transpose of a lower triangular matrix with explicitly
  // stored diagonal elements.  rhs and x can be the same vector.
  
  // x_i = (1/L_ii) (rhs_i - \sum_{j=i+1}^M L_ji x_j)
  assert(is_lower_triangular(true));
  assert(rhs.size() == nrows_);
  assert(x.size() == nrows_);
  assert(nrows_ == ncols_);
  
  // Copy rhs into x.  This does all of the rhs_i terms.
  if(&x[0] != &rhs[0])
    x = rhs;
  for(int j=int(x.size()-1); j>=0; j--) {
    const_row_iterator ji = --end(j);
    if(ji.row() != ji.col() || *ji == 0.0)
      throw ErrSetupError("Zero divisor in solve_lower_triangle_trans!");
    // We're done with the sums for x[j].
    x[j] /= *ji; 
    for(--ji; ji>=begin(j); --ji)
	x[ji.col()] -= (*ji) * x[j];
  }
}

void
SparseMat::solve_lower_triangle_trans_unitd(const DoubleVec &rhs,
						DoubleVec &x) const
{
  // Solve the transpose of a lower triangular matrix with implicit
  // ones on the diagonal.  rhs and x can be the same vector.

  // x_i = rhs_i - \sum_{j=i+1}^M L_ji x_j

  assert(is_lower_triangular(false));
  if(&x[0] != &rhs[0])
    x = rhs;
  for(int j=int(x.size()-1); j>=0; j--) {
    if(is_nonempty_row(j)) {
      for(const_row_iterator ji=begin(j); ji<end(j); ++ji) {
        x[ji.col()] -= (*ji) * x[j];
      }
    }
  }
}

SparseMat SparseMat::clone() const {
  return *this;
}

void SparseMat::tile(unsigned int i, unsigned int j,
		     const SparseMat &other)
{
  // Add other to this, offset by i rows and j columns.
  assert(i + other.nrows() <= nrows());
  assert(j + other.ncols() <= ncols());
  for(SparseMat::const_iterator kl = other.begin(); kl<other.end(); ++kl) {
    unsigned int ii = kl.row() + i;
    unsigned int jj = kl.col() + j;
    assert(0 <= ii && ii < nrows_);
    assert(0 <= jj && jj < ncols_);
    insert(ii, jj, *kl);
  }
}

void SparseMat::merge(const std::vector<SparseMat> &ms) {
  #pragma omp parallel for schedule(dynamic, 1)
  for (size_t i = 0; i < data.size(); ++i) {
    size_t rsv = ms[0].data[i].size() * 2; 
    SparseMatRow& row = data[i];
    row.reserve(rsv);
    std::unordered_map<int, int> colM; 
    colM.reserve(rsv);

    for (size_t j = 0; j < ms.size(); ++j) {
      const SparseMatRow& from = ms[j].data[i];
      for (size_t k = 0; k < from.size(); ++k) {
        const Entry& entry = from[k];
        auto it = colM.find(entry.col);
        if (it != colM.end()) {
            row[it->second].val += entry.val;
        }
        else {
           row.push_back(entry);
           colM[entry.col] = row.size() - 1;
        }
      }
    }
  }
  consolidated_ = false;
}

DoubleVec SparseMat::inefficient_get_column(unsigned int i) const {
  DoubleVec clmn(nrows(), 0.0);
  for(SparseMatConstIterator ij=begin(); ij<end(); ++ij)
    if(ij.col() == i)
      clmn[ij.row()] += *ij;
  return clmn;
}

bool SparseMat::is_lower_triangular(bool diag) const {
  if(diag) {			// diagonal elements allowed
    for(const_iterator ij=begin(); ij<end(); ++ij)
      if(ij.col() > ij.row())
	return false;
  }
  else {			// no diagonal elements allowed
    for(const_iterator ij=begin(); ij<end(); ++ij)
      if(ij.col() >= ij.row())
	return false;
  }
  return true;
}

bool SparseMat::is_upper_triangular(bool diag) const {
  if(diag) {			// diagonal elements allowed
    for(const_iterator ij=begin(); ij<end(); ++ij)
      if(ij.col() < ij.row())
	return false;
  }
  else {			// no diagonal elements allowed
    for(const_iterator ij=begin(); ij<end(); ++ij)
      if(ij.col() <= ij.row())
	return false;
  }
  return true;
}

bool SparseMat::unique_indices() const {
  // This must have had some debugging purpose at some point...
  for(unsigned int i=0; i<data.size(); i++) {
    std::set<int> indices;
    for(SparseMatRow::const_iterator j=data[i].begin(); j<data[i].end(); ++j) 
      {
	int col = (*j).col;
	if(indices.find(col) == indices.end())
	  indices.insert(col);
	else {
	  std::cerr << "SparseMat::unique_indices: duplicate ("
		    << i << "," << col << ")" << std::endl;
	  return false;
	}
      }
  }
  return true;
}

bool SparseMat::is_symmetric(double tol) const {
  bool rval = true;
  int count = 0;
  assert(consolidated());
  for(unsigned int r=0; r<nrows(); r++) {
    DoubleVec col = inefficient_get_column(r);
    for(const_row_iterator rij=begin(r); rij<end(r); ++rij) {
      count++;
      // *Don't* try to cut out extra tests by checking for
      // rij.col()<r here.  Since rij doesn't hit every column, that
      // could miss some non-symmetric entries.
      double one = *rij;
      double other = col[rij.col()];
      if(fabs(one-other) > 0.5*tol*(fabs(one) + fabs(other)) && 
        fabs(one-other) > tol)
      {
        std::cerr << "Matrix is not symmetric:"
      	    << " (" << r << "," << rij.col() << ")=" << one // *rij
      	    << " (" << rij.col() << "," << r << ")=" << other // col[rij.col()]
      	    << " difference=" << one-other
      	    << std::endl;
        rval=false;
        return false;  
      }
    }
  }
  return rval;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// void SparseMat::sanityCheck() const {
//   assert(data.size() == nrows_);
//   for(unsigned int i=0; i<nrows_; i++) {
//     for(unsigned int j=0; j<data[i].size(); j++) {
//       unsigned int col = data[i][j].col;
//       assert(col >= 0);
//       assert(col < ncols_);
//       double x = data[i][j].val;
//       assert( x >= 0. || x <= 0);
//     }
//   }
// }

std::ostream &operator<<(std::ostream &os, const SparseMat &m) {
  if(m.nnonzeros() == 0)
    os << "<empty " << m.nrows() << "x" << m.ncols() << " SparseMat>";
  else {
    os << m.nrows() << "x" << m.ncols() << " SparseMat" << std::endl;
    for(SparseMat::const_iterator ij=m.begin(); ij<m.end(); ++ij)
      os << "     " << ij.row() << " " << ij.col() << " " << *ij << std::endl;
  }
  return os;
}

void mmadump(const std::string &filename, const std::string &mtxname, 
	     const SparseMat &m)
{
  std::ofstream os(filename.c_str());
  os << mtxname << " = Table[Table[0, {i, 1, " <<  m.ncols() << "}], {j, 1, "
     << m.nrows() << "}]" << std::endl;
  for(SparseMat::const_iterator ij=m.begin(); ij<m.end(); ++ij) {
    std::string val(to_string(*ij));
    int epos = val.find("e");
    if(epos >= 0)
      val.replace(epos, 1, "*^");
    os << mtxname << "[[" << ij.row()+1 << "," << ij.col()+1 << "]] = " << val
       << std::endl;
  }
  os.close();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// non-const iterator

SparseMatIterator::SparseMatIterator(SparseMat& mat)
  : mat(mat)
{
  rowiter = mat.data.begin();
  if(!mat.data.empty()) {
    coliter = rowiter->begin();
    if(coliter == rowiter->end())
      operator++();
  }
}

SparseMatIterator::~SparseMatIterator() {

}

SparseMatIterator &SparseMatIterator::operator++() {
  std::vector<SparseMat::SparseMatRow>::iterator dataend =
    mat.data.end();
  if(rowiter < dataend) {
    if(coliter < rowiter->end())
      ++coliter;
    // Find next non-empty row, if we're at the end of the row.
    while(rowiter < dataend && coliter == rowiter->end()) {
      ++rowiter;
      if(rowiter < dataend)
        coliter = rowiter->begin();
    }
  }
  return *this;
}

bool SparseMatIterator::done() const {
  return rowiter == mat.data.end();
}

unsigned int SparseMatIterator::row() const {
  assert(*this >= mat.begin() && *this < mat.end());
  return rowiter - mat.data.begin();
}

unsigned int SparseMatIterator::col() const {
  assert(*this >= mat.begin() && *this < mat.end());
  return (*coliter).col;
}

double &SparseMatIterator::value() const {
  assert(*this >= mat.begin() && *this < mat.end());
  return (*coliter).val;
}

bool SparseMatIterator::operator==(const SparseMatIterator &o) const {
  return rowiter == o.rowiter &&
    (rowiter == mat.data.end() || coliter == o.coliter);
}

bool SparseMatIterator::operator==(const SparseMatConstIterator &o) const {
  return rowiter == o.rowiter &&
    (rowiter == mat.data.end() || coliter == o.coliter);
}

bool SparseMatIterator::operator!=(const SparseMatIterator &o) const {
  return rowiter != o.rowiter ||
    (rowiter != mat.data.end() && coliter != o.coliter);
}

bool SparseMatIterator::operator!=(const SparseMatConstIterator &o) const {
  return rowiter != o.rowiter ||
    (rowiter != mat.data.end() && coliter != o.coliter);
}

bool SparseMatIterator::operator<(const SparseMatIterator &o) const {
  return rowiter < mat.data.end() &&
    (rowiter < o.rowiter || (rowiter == o.rowiter && coliter < o.coliter));
}

bool SparseMatIterator::operator<(const SparseMatConstIterator &o) const {
  return rowiter < mat.data.end() && 
    (rowiter < o.rowiter || (rowiter == o.rowiter && coliter < o.coliter));
}

bool SparseMatIterator::operator>=(const SparseMatIterator &o) const {
  return ! (*this < o);
}

bool SparseMatIterator::operator>=(const SparseMatConstIterator &o) const {
  return ! (*this < o);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// const iterator

SparseMatConstIterator::SparseMatConstIterator(const SparseMat& mat)
  : mat(mat)
{
  rowiter = mat.data.begin();
  if(!mat.data.empty()) {
    coliter = rowiter->begin();
    if(coliter == rowiter->end())
      operator++();
  }
}

SparseMatConstIterator::~SparseMatConstIterator() {
}

SparseMatConstIterator &SparseMatConstIterator::operator++() {
  std::vector<SparseMat::SparseMatRow>::const_iterator dataend =
    mat.data.end();
  // std::cerr << "SparseMatConstIterator::operator++: dataend-rowiter="
  // 	    << dataend-rowiter << std::endl;
  if(rowiter < dataend) {
    // std::cerr << "SparseMatConstIterator::operator++: rowend-coliter="
    // 	      << rowiter->end() - coliter << std::endl;
    if(coliter < rowiter->end()) {
      ++coliter;
      // std::cerr << "SparseMatConstIterator::operator++: rowend-coliter="
      // 		<< rowiter->end() - coliter << " after incrementing"
      // 		<< std::endl;
    }
    // Find next non-empty row, if we're at the end of the row.
    while(rowiter < dataend && coliter == rowiter->end()) {
      ++rowiter;
      // std::cerr << "SparseMatConstIterator::operator++: incremented rowiter"
      // 		<< std::endl;
      if(rowiter < dataend)
	coliter = rowiter->begin();
    }
  }
  return *this;
}

unsigned int SparseMatConstIterator::row() const {
  assert(*this >= mat.begin() && *this < mat.end());
  return rowiter - mat.data.begin();
}

unsigned int SparseMatConstIterator::col() const {
  assert(*this >= mat.begin() && *this < mat.end());
  return (*coliter).col;
}

double SparseMatConstIterator::value() const {
  assert(*this >= mat.begin() && *this < mat.end());
  return (*coliter).val;
}

bool SparseMatConstIterator::operator==(const SparseMatConstIterator &o) const {
  return rowiter == o.rowiter &&
    (rowiter == mat.data.end() || coliter == o.coliter);
}

bool SparseMatConstIterator::operator==(const SparseMatIterator &o) const {
  return rowiter == o.rowiter &&
    (rowiter == mat.data.end() || coliter == o.coliter);
}

bool SparseMatConstIterator::operator!=(const SparseMatConstIterator &o) const {
  return rowiter != o.rowiter ||
    (rowiter != mat.data.end() && coliter != o.coliter);
}

bool SparseMatConstIterator::operator!=(const SparseMatIterator &o) const {
  return rowiter != o.rowiter ||
    (rowiter != mat.data.end() && coliter != o.coliter);
}

bool SparseMatConstIterator::operator<(const SparseMatConstIterator &o) const {
  return rowiter < mat.data.end() && 
    (rowiter < o.rowiter || (rowiter==o.rowiter && coliter<o.coliter));
}

bool SparseMatConstIterator::operator<(const SparseMatIterator &o) const {
  return rowiter < mat.data.end() && 
    (rowiter < o.rowiter || (rowiter==o.rowiter && coliter<o.coliter));
}

bool SparseMatConstIterator::operator>=(const SparseMatConstIterator &o) const {
  return ! (*this < o);
}

bool SparseMatConstIterator::operator>=(const SparseMatIterator &o) const {
  return ! (*this < o);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

/* SparseMatConstRowIterator */

SparseMatRowConstIterator::SparseMatRowConstIterator(const SparseMat& mat,
						     unsigned int row)
  :mat(mat),
   row_(row)
{
  if(row >= mat.nrows())
    throw ErrProgrammingError(
			  "SparseMatRowConstIterator row index out of range",
			  __FILE__, __LINE__);
  coliter = mat.data[row].begin(); // iterates over the row
}

SparseMatRowConstIterator::SparseMatRowConstIterator(
				       const SparseMatConstIterator &smi)
  : mat(smi.mat),
    row_(smi.row()),
    coliter(smi.coliter)
{
}

SparseMatRowConstIterator::~SparseMatRowConstIterator() {}

SparseMatRowConstIterator &SparseMatRowConstIterator::operator++() {
  ++coliter;
  return *this;
}

SparseMatRowConstIterator &SparseMatRowConstIterator::operator--() {
  --coliter;
  return *this;
}

unsigned int SparseMatRowConstIterator::col() const {
  assert(*this >= mat.begin(row_) && *this < mat.end(row_));
  return (*coliter).col;
}

double SparseMatRowConstIterator::value() const {
  assert(*this >= mat.begin(row_) && *this < mat.end(row_));
  return (*coliter).val;
}

bool SparseMatRowConstIterator::operator==(const SparseMatRowConstIterator &o)
  const
{
  return row_ == o.row_ && coliter == o.coliter;
}

bool SparseMatRowConstIterator::operator!=(const SparseMatRowConstIterator &o)
  const
{
  return row_ != o.row_ || coliter != o.coliter;
}

bool SparseMatRowConstIterator::operator<(const SparseMatRowConstIterator &o) 
  const
{
  return row_ < o.row_ || (row_ == o.row_ && coliter < o.coliter);
}

bool SparseMatRowConstIterator::operator>=(const SparseMatRowConstIterator &o)
  const
{
  return ! (*this < o);
}

bool SparseMatRowConstIterator::operator==(const SparseMatRowIterator &o) const 
{
  return row_ == o.row_ && coliter == o.coliter;
}

bool SparseMatRowConstIterator::operator!=(const SparseMatRowIterator &o) const 
{
  return row_ != o.row_ || coliter != o.coliter;
}

bool SparseMatRowConstIterator::operator<(const SparseMatRowIterator &o) const {
  return row_ < o.row_ || (row_ == o.row_  && coliter < o.coliter);
}

bool SparseMatRowConstIterator::operator>=(const SparseMatRowIterator &o) const 
{
  return ! (*this < o);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

/* SparseMatRowIterator */

SparseMatRowIterator::SparseMatRowIterator(SparseMat& mat, unsigned int row)
  : mat(mat),
    row_(row)
{
  if(row >= mat.nrows())
    throw ErrProgrammingError("SparseMatRowIterator row index out of range",
			      __FILE__, __LINE__);
  coliter = mat.data[row].begin(); // iterates over the row
}

SparseMatRowIterator::SparseMatRowIterator(SparseMatIterator &smi)
  : mat(smi.mat),
    row_(smi.row()),
    coliter(smi.coliter)
{
}

SparseMatRowIterator::~SparseMatRowIterator() {}

SparseMatRowIterator &SparseMatRowIterator::operator++() {
  ++coliter;
  return *this;
}

SparseMatRowIterator &SparseMatRowIterator::operator--() {
  --coliter;
  return *this;
}

unsigned int SparseMatRowIterator::col() const {
  assert(*this >= mat.begin(row_) && *this < mat.end(row_));
  return (*coliter).col;
}

double &SparseMatRowIterator::value() {
  assert(*this >= mat.begin(row_) && *this < mat.end(row_));
  return (*coliter).val;
}

bool SparseMatRowIterator::done() const {
  return *this == mat.end(row_);
}

bool SparseMatRowIterator::operator==(const SparseMatRowIterator &o) const {
  return row_ == o.row_ && coliter == o.coliter;
}

bool SparseMatRowIterator::operator==(const SparseMatRowConstIterator &o) const {
  return row_ == o.row_ && coliter == o.coliter;
}

bool SparseMatRowIterator::operator!=(const SparseMatRowIterator &o) const {
  return row_ != o.row_ || coliter != o.coliter;
}

bool SparseMatRowIterator::operator!=(const SparseMatRowConstIterator &o) const {
  return row_ != o.row_ || coliter != o.coliter;
}

bool SparseMatRowIterator::operator<(const SparseMatRowIterator &o) const {
  return row_ < o.row_ || (row_ == o.row_ && coliter < o.coliter);
}

bool SparseMatRowIterator::operator<(const SparseMatRowConstIterator &o) const {
  return row_ < o.row_ || (row_ == o.row_ && coliter < o.coliter);
}

bool SparseMatRowIterator::operator>=(const SparseMatRowIterator &o) const {
  return ! (*this < o);
}

bool SparseMatRowIterator::operator>=(const SparseMatRowConstIterator &o) const {
  return ! (*this < o);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SparseMat identityMatrix(unsigned int n) {
  SparseMat result(n, n);
  for(unsigned int i=0; i<n; i++)
    result.insert(i, i, 1.0);
  return result;
}

SparseMat mistakenIdentityMatrix(unsigned int n) {
  SparseMat result(n, n);
  for(unsigned int i=0; i<n; i++)
    result.insert(i, i, -1.0);
  return result;
}

SparseMat operator*(double a, const SparseMat &m) {
  SparseMat prod(m.clone());
  prod *= a;
  return prod;
}

SparseMat operator*(const SparseMat &m, double a) {
  SparseMat prod(m.clone());
  prod *= a;
  return prod;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream& operator<<(std::ostream &os, const SparseMatIterator &it) {
  if(it.done())
    return os << "SparseMatIterator(<done>)";
  int row = it.rowiter - it.mat.data.begin();
  int col = (*it.coliter).col;
  return os << "SparseMatIterator(" << row << "," << col << ")";
}

std::ostream& operator<<(std::ostream &os, const SparseMatConstIterator &it) {
  int row = it.rowiter - it.mat.data.begin();
  int col = (*it.coliter).col;
  os << "SparseMatConstIterator(" << row << "," << col << ")";
  if(it.done())
    os << " [done]";
  return os;
}

std::ostream& operator<<(std::ostream &os, const SparseMatRowIterator &it) {
  if(it.done()) {
    return os << "SparseMatRowIterator(<done>)";
  }
  int row = it.row();
  int col = (*it.coliter).col;
  return os << "SparseMatRowIterator(" << row << "," << col << ")";
}

std::ostream& operator<<(std::ostream &os, const SparseMatRowConstIterator &it) 
{
  if(it.done())
    return os << "SparseMatRowConstIterator(<done>)";
  int row = it.row();
  int col = (*it.coliter).col;
  return os << "SparseMatRowConstIterator(" << row << "," << col << ")";
}

std::ostream &operator<<(std::ostream &os, const SparseMat::Entry &e) {
  return os << "(" << e.col << "," << e.val << ")";
}
