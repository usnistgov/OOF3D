// -*- C++ -*-
// $RCSfile: cmatrixmethods.C,v $
// $Revision: 1.8.2.3 $
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
#include <iostream>
#include <string.h>		// for memcpy

#include "common/doublevec.h"
#include "common/printvec.h"	// for debugging
#include "common/smallmatrix.h"
#include "common/vectormath.h"	// needed when templates are expanded
#include "engine/SparseLib++/bicg.h"
#include "engine/SparseLib++/bicgstab.h"
#include "engine/SparseLib++/cg.h"
#include "engine/SparseLib++/gmres.h"
#include "engine/cmatrixmethods.h"
#include "engine/ooferror.h"
#include "engine/preconditioner.h"
#include "engine/sparsemat.h"

// CG, BiCG, BiCGStab and GMRES are just wrappers for the IML++
// template routines.  The wrappers are necessary because we can't
// swig the templates.

// On exit, these routines set maxiter and tolerance to the actual
// number of iterations and the residual.  The swigged versions then
// return those values as a tuple to Python, so that solution
// statistics can be accumulated by SolverStats.

void solveCG(const SparseMat &A, const DoubleVec &rhs,
	    const PreconditionerBase &pc, int &maxiter, double &tolerance,
	    DoubleVec &x)
{
  CG(A, x, rhs, pc, maxiter, tolerance);
}

void solveBiCG(const SparseMat &A, const DoubleVec &rhs,
	      const PreconditionerBase &pc, int &maxiter, double &tolerance,
	      DoubleVec &x)
{
  BiCG(A, x, rhs, pc, maxiter, tolerance);
}

void solveBiCGStab(const SparseMat &A, const DoubleVec &rhs,
		  const PreconditionerBase &pc, int &maxiter, double &tolerance,
		  DoubleVec &x)
{
  BiCGSTAB(A, x, rhs, pc, maxiter, tolerance);
}

void solveGMRes(const SparseMat &A, const DoubleVec &rhs,
	       const PreconditionerBase &pc, int &maxiter, int krylov_dim,
	       double &tolerance, DoubleVec &x)
{
  SmallMatrix H(krylov_dim+1, krylov_dim+1);
  GMRES(A, x, rhs, pc, H, krylov_dim, maxiter, tolerance);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void solveDirect(const SparseMat &A, const DoubleVec &rhs, DoubleVec &x) {
//   std::cerr << "solveDirect: " << A.nrows() << "x" << A.ncols()
// 	    << " rhs " << rhs.size() << " x " << x.size() << std::endl;
//   std::cerr << "solveDirect: rhs=" << rhs << std::endl;
//   std::cerr << "solveDirect: A=" << A << std::endl;

  // Copy sparse matrix into dense matrix.
  SmallMatrix small_m(A.nrows(), A.ncols());
  for(SparseMat::const_iterator ij=A.begin(); ij!=A.end(); ++ij)
    small_m(ij.row(), ij.col()) = *ij;

//   std::cerr << "solveDirect: small_m=" << small_m << std::endl;

  // Copy vector rhs into 'matrix' rhs
  SmallMatrix small_r(rhs.size(), 1);
  (void) memcpy(&small_r(0, 0), &rhs[0], rhs.size()*sizeof(double));

  // Solve.  SmallMatrix::solve will raise an exception if A is not
  // square or rhs is the wrong size.
  int rcode = small_m.solve(small_r);

  (void) memcpy(&x[0], &small_r(0, 0), rhs.size()*sizeof(double));

  // double r = 0.0;
  if(rcode == 0) {		// success
    // // compute residual
    // DoubleVec resid(rhs);
    // A.axpy(-1.0, x, resid);	// resid = -A*x + rhs
    // r = resid*resid;
  }
  else				// failure
    throw ErrUserError(
	     "Direct matrix solver failed. The matrix is probably singular.");
}
