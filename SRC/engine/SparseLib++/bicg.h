// -*- C++ -*-
// $RCSfile: bicg.h,v $
// $Revision: 1.19.2.2 $
// $Author: langer $
// $Date: 2014/07/22 21:02:47 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// This routine is originally from IML++ (http://math.nist.gov/iml++/)
// but has been slightly modified to work with OOF2.

#include <oofconfig.h>
#include "common/progress.h" 
#include "common/tostring.h"
#include "common/vectormath.h"
#include "common/IO/oofcerr.h"
#include "engine/ooferror.h"
#include <math.h>

//*****************************************************************
// Iterative template routine -- BiCG
//
// BiCG solves the unsymmetric linear system Ax = b 
// using the Preconditioned BiConjugate Gradient method
//
// BiCG follows the algorithm described on p. 22 of the 
// SIAM Templates book.
//
// The return value indicates convergence within max_iter (input)
// iterations (0), or no convergence within max_iter iterations (1).
//
// Upon successful return, output arguments have the following values:
//  
//        x  --  approximate solution to Ax = b
// max_iter  --  the number of iterations performed before the
//               tolerance was reached
//      tol  --  the residual after the final iteration
//  
//*****************************************************************


template < class Matrix, class Vector, class Preconditioner, class Real >
void BiCG(const Matrix &A, Vector &x, const Vector &b,
	  const Preconditioner &M, int &max_iter, Real &tol)
{

  Real resid;
  Vector rho_1(1), rho_2(1), alpha(1), beta(1);
  Vector z, ztilde, p, ptilde, q, qtilde;

  Real normb = b.norm();
  Vector r = b - A * x;
  Real normr = r.norm();
  if(!isfinite(normb) || !isfinite(normr))
    throw ErrInstabilityError("BiCG arguments are infinite.");
  Vector rtilde = r;

  if (normb == 0.0)
    normb = 1;
  
  if ((resid = normr / normb) <= tol) {
    tol = resid;
    max_iter = 0;
    return;
  }
  LogDefiniteProgress *progress =
    dynamic_cast<LogDefiniteProgress*>(getProgress("BiCG", LOGDEFINITE));
  progress->setRange(resid, tol);
  for (int i = 1; i <= max_iter; i++) {
    if(progress->stopped()) {
      progress->setMessage("BiCG Interrupted");
      progress->finish();
      throw ErrInterrupted();
    }
    z = M.solve(r);
    ztilde = M.trans_solve(rtilde);
    rho_1[0] = dot(z, rtilde);
    if (rho_1[0] == 0) { 
      tol = r.norm() / normb;
      max_iter = i;
      progress->finish(); // finished successfully (woo-hoo!)
      return; 
    }
    if (i == 1) {
      p = z;
      ptilde = ztilde;
    } else {
      beta[0] = rho_1[0] / rho_2[0];
      p = z + beta[0] * p;
      ptilde = ztilde + beta[0] * ptilde;
    }
    q = A * p;
    qtilde = A.trans_mult(ptilde);
    alpha[0] = rho_1[0] / dot(ptilde, q);
    x += alpha[0] * p;
    r -= alpha[0] * q;
    rtilde -= alpha[0] * qtilde;

    rho_2[0] = rho_1[0];
    if ((resid = r.norm() / normb) < tol) {
      progress->setMessage(to_string(resid) + "/" + to_string(tol));
      progress->finish();
      tol = resid;
      max_iter = i;
      return;
    }

    progress->setMessage(to_string(resid) + "/" + to_string(tol));
    progress->setFraction(resid);
  }

  tol = resid;
  // If thread made it to this point, it means that solver failed.
  progress->setMessage("BiCG failed"); 
  progress->finish();
  throw ErrConvergenceFailure("BiCG", max_iter);
}
  
