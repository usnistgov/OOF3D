// -*- C++ -*-
// $RCSfile: gmres.h,v $
// $Revision: 1.24.2.3 $
// $Author: langer $
// $Date: 2014/07/22 21:02:48 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// GMRES template from http://math.nist.gov/iml++/

#include <oofconfig.h>
#include "common/progress.h" 
#include "common/tostring.h"
#include "common/vectormath.h"
#include "engine/ooferror.h"
#include <math.h>

//*****************************************************************
// Iterative template routine -- GMRES
//
// GMRES solves the unsymmetric linear system Ax = b using the 
// Generalized Minimum Residual method
//
// GMRES follows the algorithm described on p. 20 of the 
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

#include <math.h> 


template<class Real> 
void GeneratePlaneRotation(Real &dx, Real &dy, Real &cs, Real &sn)
{
  if (dy == 0.0) {
    cs = 1.0;
    sn = 0.0;
  } else if (abs(dy) > abs(dx)) {
    Real temp = dx / dy;
    sn = 1.0 / sqrt( 1.0 + temp*temp );
    cs = temp * sn;
  } else {
    Real temp = dy / dx;
    cs = 1.0 / sqrt( 1.0 + temp*temp );
    sn = temp * cs;
  }
}


template<class Real> 
void ApplyPlaneRotation(Real &dx, Real &dy, Real &cs, Real &sn)
{
  Real temp  =  cs * dx + sn * dy;
  dy = -sn * dx + cs * dy;
  dx = temp;
}



template < class Matrix, class Vector >
void 
Update(Vector &x, int k, Matrix &h, Vector &s, Vector v[])
{
  Vector y(s);

  // Backsolve:  
  for (int i = k; i >= 0; i--) {
    y[i] /= h(i,i);
    for (int j = i - 1; j >= 0; j--)
      y[j] -= h(j,i) * y[i];
  }

  for (int j = 0; j <= k; j++)
    x += v[j] * y[j];
}


template < class Real >
Real 
abs(Real x)
{
  return (x > 0 ? x : -x);
}


template < class Operator, class Vector, class Preconditioner,
           class Matrix, class Real >
void GMRES(const Operator &A, Vector &x, const Vector &b,
	   const Preconditioner &M, Matrix &H, int &m, int &max_iter,
	   Real &tol)
{
  Real resid;
  int i, j = 1, k;
  Vector s(m+1), cs(m+1), sn(m+1), w;
  
  // Check for already-solvedness in regular space first.
  // This is special new added code to deal with singularities
  // arising for small test systems.
  Real normb = b.norm();
  Vector r = b - A*x;
  Real normr = r.norm();
  if(!isfinite(normb) || !isfinite(normr))
    throw ErrInstabilityError("GMRES arguments are infinite.");

  if (normb == 0.0) 
    normb = 1;
  
  if ((resid = normr / normb) <= tol) {
    tol = resid;
    max_iter = 0;
    return;
  }

  
  // Then check for already-solvedness in preconditioner space.
  // End of added code.

  normb = M.solve(b).norm();
  // std::cerr << "M.solve(b)=" << M.solve(b) << std::endl;
  r = M.solve(b - A * x);
  Real beta = r.norm();
  
  if (normb == 0.0)
    normb = 1;
  
  if ((resid = r.norm() / normb) <= tol) {
    tol = resid;
    max_iter = 0;
    return;
  }

  LogDefiniteProgress *progress = 
    dynamic_cast<LogDefiniteProgress*>(getProgress("GMRES", LOGDEFINITE));
  progress->setRange(resid, tol);

  Vector *v = new Vector[m+1];
  while (j <= max_iter) {

    if(progress->stopped()) {
      progress->setMessage("GMRES Interrupted");
      progress->finish();
      throw ErrInterrupted();
    }

    v[0] = r * (1.0 / beta);    // ??? r / beta
//     s = 0.0;
    for(typename Vector::iterator ii=s.begin(); ii<s.end(); ++ii)
      *ii = 0;
    s[0] = beta;
    
    for (i = 0; i < m && j <= max_iter && !progress->stopped(); i++, j++) {
      w = M.solve(A * v[i]);
      for (k = 0; k <= i; k++) {
        H(k, i) = dot(w, v[k]);
        w -= H(k, i) * v[k];
      }
      H(i+1, i) = w.norm();
      v[i+1] = w * (1.0 / H(i+1, i)); // ??? w / H(i+1, i)

      for (k = 0; k < i; k++)
        ApplyPlaneRotation(H(k,i), H(k+1,i), cs[k], sn[k]);
      
      GeneratePlaneRotation(H(i,i), H(i+1,i), cs[i], sn[i]);
      ApplyPlaneRotation(H(i,i), H(i+1,i), cs[i], sn[i]);
      ApplyPlaneRotation(s[i], s[i+1], cs[i], sn[i]);
      
      if ((resid = abs(s[i+1]) / normb) < tol) {
        Update(x, i, H, s, v);
	progress->setMessage(to_string(resid) + "/" + to_string(tol));
	progress->finish();
        tol = resid;
        max_iter = j;
        delete [] v;
        return;
      }
      progress->setMessage(to_string(resid) + "/" + to_string(tol));
      progress->setFraction(resid); 
    }
    Update(x, i - 1, H, s, v);
    r = M.solve(b - A * x);
    beta = r.norm();
    if ((resid = beta / normb) < tol) {
      //Thread control starts here
      progress->setMessage(to_string(resid) + "/" + to_string(tol));
      progress->finish();
      tol = resid;
      max_iter = j;
      delete [] v;
      return;
    }
  }
  
  tol = resid;
  delete [] v;
  
  progress->setMessage("GMRES failed");
  progress->finish();
  throw ErrConvergenceFailure("GMRES", max_iter);
}


