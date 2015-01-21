// -*- C++ -*-
// $RCSfile: icpre.C,v $
// $Revision: 1.2.10.2 $
// $Author: langer $
// $Date: 2014/10/15 20:53:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// Cholesky decomposition: Any symmetric positive definite matrix can
// be decomposed into LU, where L is lower triangular and U =
// transpose(L).

#include <stdlib.h>
#include <math.h>
#include "common/doublevec.h"
#include "common/tostring.h"
#include "engine/icpre.h"
#include "engine/ooferror.h"
#include "engine/sparsemat.h"

const std::string ICPreconditionerCore::modulename_("ooflib.SWIG.engine.icpre");
const std::string ICPreconditioner::classname_("ICPreconditioner");
const std::string ICPreconditionerCore::classname_("ICPreconditionerCore");

#ifdef DEBUG
// Machinery to check that no L values are used before they're
// computed.  Copied and pasted from ilupre.C.
#include <set>
#include <utility>
#include "common/tostring.h"

class DonePairs {
private:
  typedef std::pair<int, int> IntPair;
  std::set<IntPair> done;
  const std::string label;
public:
  DonePairs(const std::string &label) : label(label) {}
  void computed(const SparseMat::row_iterator &ij) {
    done.insert(IntPair(ij.row(), ij.col()));
  }
  void check_computed(const SparseMat::row_iterator &ij) const {
    if(done.find(IntPair(ij.row(), ij.col())) == done.end()) {
      throw ErrProgrammingError("IC misordering(" + label + "): i="
				+ to_string(ij.row())
				+ " j=" + to_string(ij.col()),
				__FILE__, __LINE__);
    }
  }
  void check_uncomputed(const SparseMat::row_iterator &ij) const {
    if(done.find(IntPair(ij.row(), ij.col())) != done.end())
      throw ErrProgrammingError("IC misordering(" + label + "): i="
				+ to_string(ij.row())
				+ " j=" + to_string(ij.col())
				+ "computed too soon",
				__FILE__, __LINE__);
  }
};
#endif // DEBUG

ICPreconditionerCore::ICPreconditionerCore(const SparseMat &A)
  : L(A.nrows(), A.ncols())
{
  // Copy just the lower triangular part (including the diagonal).
  for(SparseMat::const_iterator ij=A.begin(); ij!=A.end(); ++ij)
    if(ij.col() <= ij.row())
      L.insert(ij.row(), ij.col(), *ij);
  if(A.consolidated())
    L.set_consolidated(true);
  else
    L.consolidate();

#ifdef DEBUG
  DonePairs lprs("L");
#endif

  // Loop over rows of the matrix.
  for(unsigned int j=0; j<L.nrows(); j++) {
    SparseMat::row_iterator lastj = --L.end(j); // last entry in row j
    if(lastj.row() != lastj.col())
      throw ErrSetupError("IC Preconditioner: diagonal not found!");

    // Loop over all entries ji in row j, except the last (diagonal) one.
    for(SparseMat::row_iterator lji=L.begin(j); lji!=lastj; ++lji) {
      unsigned int i = lji.col();
      SparseMat::row_iterator lasti = --L.end(i); // last entry in row i
      assert(lasti.row() == lasti.col());
#ifdef DEBUG
      lprs.check_computed(lasti);
      lprs.check_uncomputed(lji);
#endif // DEBUG

      // L_ji = (1/L_ii) (A_ji - \sum_{k=0}^{i-i} L_ik L_jk)
      double sum = *lji;
      SparseMat::row_iterator lik = L.begin(i);
      SparseMat::row_iterator ljk = L.begin(j);
      while(lik.col() < i && ljk.col() < i) {
	if(lik.col() == ljk.col()) {
#ifdef DEBUG
	  lprs.check_computed(lik);
	  lprs.check_computed(ljk);
#endif // DEBUG
	  sum -= (*lik) * (*ljk);
	  ++lik;
	  ++ljk;
	}
	else if(lik.col() < ljk.col())
	  ++lik;
	else
	  ++ljk;
      }
      *lji = sum/(*lasti);
#ifdef DEBUG
      lprs.computed(lji);
#endif // DEBUG
    } // end loop over entries in row j

    // L_jj = sqrt(A_jj - \sum_{k=0}^{j-1} (L_jk)^2)
    double sum = *lastj;
#ifdef DEBUG
    lprs.check_uncomputed(lastj);
#endif // DEBUG
    for(SparseMat::row_iterator ljk=L.begin(j); ljk!=lastj; ++ljk) {
#ifdef DEBUG
      lprs.check_computed(ljk);
#endif // DEBUG
      sum -= (*ljk)*(*ljk);
    }
    if(sum <= 0.0) {
      std::cerr << "ICPreconditionerCore::ctor: error in row=" << j
		<< "/" << A.nrows() << std::endl;
      throw ErrSetupError("IC Preconditioner: Matrix is not positive definite");

    }
    *lastj = sqrt(sum);
#ifdef DEBUG
    lprs.computed(lastj);
#endif // DEBUG
  } // end loop over rows
}


DoubleVec ICPreconditionerCore::solve(const DoubleVec &x) const {
  DoubleVec y(x.size(), 0.0);
  // Solve L*y = x, where L is lower triangular.
  L.solve_lower_triangle(x, y);
  // Solve L^T*z = y, storing result in y.
  L.solve_lower_triangle_trans(y, y);
  return y;
}


DoubleVec ICPreconditionerCore::trans_solve(const DoubleVec &x) const {
  return solve(x);
}

SparseMat ICPreconditionerCore::unfactored() const {
  return L*L.transpose();
};
