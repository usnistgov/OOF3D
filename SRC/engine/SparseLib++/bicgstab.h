// -*- C++ -*-
// $RCSfile: bicgstab.h,v $
// $Revision: 1.18.2.2 $
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

#include <oofconfig.h>
#include "common/progress.h" 
#include "common/tostring.h"
#include "engine/ooferror.h"
#include <math.h>

//*****************************************************************
// Iterative template routine -- BiCGSTAB
//
// BiCGSTAB solves the unsymmetric linear system Ax = b 
// using the Preconditioned BiConjugate Gradient Stabilized method
//
// BiCGSTAB follows the algorithm described on p. 27 of the 
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
void BiCGSTAB(const Matrix &A, Vector &x, const Vector &b,
	      const Preconditioner &M, int &max_iter, Real &tol)
{
  Real resid;
  Vector rho_1(1), rho_2(1), alpha(1), beta(1), omega(1);
  Vector p, phat, s, shat, t, v;

  Real normb = b.norm();
  Vector r = b - A * x;
  Real normr = r.norm();
  if(!isfinite(normb) || !isfinite(normr))
    throw ErrInstabilityError("BiCGStab arguments are infinite.");
  Vector rtilde = r;

  if (normb == 0.0)
    normb = 1;
  
  if ((resid = normr / normb) <= tol) {
    tol = resid;
    max_iter = 0;
    return;
  }
  LogDefiniteProgress *progress = 
    dynamic_cast<LogDefiniteProgress*>(getProgress("BiCGSTAB", LOGDEFINITE));
  progress->setRange(resid, tol);
  for (int i = 1; i <= max_iter; i++) {

    if(progress->stopped()) {
      progress->setMessage("BiCGSTAB Interrupted");
      progress->finish();
      throw ErrInterrupted();
    }

    rho_1[0] = dot(rtilde, r);
    if (rho_1[0] == 0) {
      tol = r.norm() / normb;
      progress->finish();
      return;
    }
    if (i == 1)
      p = r;
    else {
      beta[0] = (rho_1[0]/rho_2[0]) * (alpha[0]/omega[0]);
      p = r + beta[0] * (p - omega[0] * v);
    }
    phat = M.solve(p);
    v = A * phat;
    alpha[0] = rho_1[0] / dot(rtilde, v);
    s = r - alpha[0] * v;
    if ((resid = s.norm()/normb) < tol) {
      x += alpha[0] * phat;
      progress->setMessage(to_string(resid) + "/" + to_string(tol));
      progress->finish();
      tol = resid;
      return;
    }
    shat = M.solve(s);
    t = A * shat;
    omega[0] = dot(t,s) / dot(t,t);
    x += alpha[0] * phat + omega[0] * shat;
    r = s - omega[0] * t;

    rho_2[0] = rho_1[0];
    if ((resid = r.norm() / normb) < tol) {
      progress->setMessage(to_string(resid) + "/" + to_string(tol));
      tol = resid;
      max_iter = i;
      progress->finish();
      return;
    }
    if (omega[0] == 0) {
      tol = r.norm() / normb;
      progress->setMessage("BiCGSTAB failed");
      progress->finish();
      throw ErrConvergenceFailure("BiCGSTAB", i);
    }

    progress->setMessage(to_string(resid) + "/" + to_string(tol));
    progress->setFraction(resid); 
  }

  tol = resid;

  progress->setMessage("BiCGSTAB failed");
  progress->finish();
  throw ErrConvergenceFailure("BiCGSTAB", max_iter);
}
