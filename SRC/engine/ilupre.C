// -*- C++ -*-
// $RCSfile: ilupre.C,v $
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

// Preconditioning via incomplete LU factorization.

#include <stdlib.h>
#include "common/doublevec.h"
#include "engine/ilupre.h"
#include "engine/ooferror.h"
#include "engine/sparsemat.h"

const std::string ILUPreconditionerCore::modulename_(
					     "ooflib.SWIG.engine.ilupre");
const std::string ILUPreconditioner::classname_("ILUPreconditioner");
const std::string ILUPreconditionerCore::classname_("ILUPreconditionerCore");

#ifdef DEBUG
// Machinery to check that no L or UT values are used before they're
// computed.
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
      throw ErrProgrammingError("ILU misordering(" + label + "): i=" + to_string(ij.row())
				+ " j=" + to_string(ij.col()),
				__FILE__, __LINE__);
    }
  }
};
#endif // DEBUG

ILUPreconditionerCore::ILUPreconditionerCore(const SparseMat &A)
  : UT(A.nrows(), A.ncols()),
    L(A.nrows(), A.ncols())
{
  // Copy A into L and UT
  for(SparseMat::const_iterator ij=A.begin(); ij!=A.end(); ++ij)
    if(ij.col() < ij.row())
      L.insert(ij.row(), ij.col(), *ij);
    else
      UT.insert(ij.col(), ij.row(), *ij); // transpose!

  if(A.consolidated()) {
    L.set_consolidated(true);
    UT.set_consolidated(true);
  }
  else {
    L.consolidate();
    UT.consolidate();
  }
#ifdef DEBUG
  DonePairs uprs("U");
  DonePairs lprs("L");
#endif // DEBUG

  // This implements Crout's algorithm, but not in the order described
  // in Numerical Recipes.  That order doesn't work well for us
  // because we can only loop over rows of matrices, not columns.

  for(unsigned int r=0; r<A.nrows(); r++) {
    for(SparseMat::row_iterator lij=L.begin(r); lij!=L.end(r); ++lij) {
      // Compute the ij entry of L.
      // L_ij = (1/U_jj) (A_ij - \sum_{k=0}^{j-1} L_ik U_kj
      unsigned int c = lij.col();
      if(lij.row() == c) {
	continue; // diagonal not stored in L
      }

      double sum = 0.0;
      SparseMat::row_iterator ll = L.begin(r);
      SparseMat::row_iterator uu = UT.begin(c);
      while(ll != L.end(r) && uu != UT.end(c) && ll.col() < c && uu.col() < c) {
	if(ll.col() == uu.col()) {
#ifdef DEBUG
	  lprs.check_computed(ll);
	  uprs.check_computed(uu);
#endif // DEBUG
	  sum += (*ll) * (*uu);
	  ++ll;
	  ++uu;
	}
	else if(ll.col() < uu.col())
	  ++ll;
	else
	  ++uu;
      } // end uu & ll loop
      *lij -= sum;
      SparseMat::row_iterator endd = UT.end(c);
      if(endd == UT.begin(c)) {
	throw ErrSetupError("Empty row in ILU preconditioner");
      }
      SparseMat::row_iterator diag = --endd;
      if(diag.row() != diag.col() || *diag == 0.0)
	throw ErrSetupError("Zero divisor in ILU preconditioner");
      *lij /= *diag;
#ifdef DEBUG
      lprs.computed(lij);
#endif // DEBUG
    } // end lij loop

    for(SparseMat::row_iterator uji=UT.begin(r); uji!=UT.end(r); ++uji) {
      // Compute the ij entry of U (ie, the ji entry of UT).
      // U_ij = A_ij - \sum_{k=0}^{i-1} L_ik U_kj  for i<j
      unsigned int c = uji.col();// *row* number of U, *col* number of UT
      double sum = 0.0;
      SparseMat::row_iterator uu = UT.begin(r); // loop over column of U
      SparseMat::row_iterator ll = L.begin(c);	// and row of L
      while(ll != L.end(c) && uu != UT.end(r) && uu.col() < c) {
	if(ll.col() == uu.col()) {
#ifdef DEBUG
	  uprs.check_computed(uu);
	  lprs.check_computed(ll);
#endif // DEBUG
	  sum += (*ll) * (*uu);
	  ++ll;
	  ++uu;
	}
	else if(ll.col() < uu.col())
	  ++ll;
	else
	  ++uu;
      } // end uu & ll loop
      *uji -= sum;
#ifdef DEBUG
      uprs.computed(uji);
#endif // DEBUG
    } // end uji loop
  } // end r loop
  L.consolidate();
  UT.consolidate();
  assert(L.is_lower_triangular(false));
  assert(UT.is_lower_triangular(true));
}

ILUPreconditionerCore::~ILUPreconditionerCore() {}

DoubleVec ILUPreconditionerCore::solve(const DoubleVec &x) const {
  DoubleVec y(x.size());
  // Solve L*y = x for y.  Remember that the diagonal entries of L are
  // 1, and aren't stored explicitly.
  L.solve_lower_triangle_unitd(x, y);
  // Solve U*z = y.
  UT.solve_lower_triangle_trans(y, y);
  return y;
} 


DoubleVec ILUPreconditionerCore::trans_solve(const DoubleVec &x) const {
  DoubleVec y(x.size());
  // Solve (U^T)*y = x for y.  U^T is lower triangular, with explicit
  // entries on the diagonal.
  UT.solve_lower_triangle(x, y);
  // Solve (L^T)* z = y for z. L^T is upper triangular, with implicit
  // ones on the diagonal.
  L.solve_lower_triangle_trans_unitd(y, y);
  return y;
} 

// Multiply the factors together, for debugging and testing.

SparseMat ILUPreconditionerCore::unfactored() const {
  SparseMat L2 = L.clone();
  // Since L doesn't store its diagonal, its value of nrows might be
  // wrong.  Use UT.nrows() instead.
  for(unsigned int i=0; i<UT.nrows(); i++)
    L2.insert(i, i, 1.0);
  L2.consolidate();
  return L2*UT.transpose();
}
