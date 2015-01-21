// -*- C++ -*-
// $RCSfile: cmatrixmethods.h,v $
// $Revision: 1.2.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Swiggable C++ Wrappers for the low level IML++ matrix solver
// routines.

#include <oofconfig.h>

#ifndef CMATRIXMETHODS_H
#define CMATRIXMETHODS_H

class DoubleVec;
class SparseMat;
class PreconditionerBase;

void solveCG(const SparseMat&, const DoubleVec &rhs,
	    const PreconditionerBase&, int &maxiter, double &tolerance,
	    DoubleVec &x);

void solveBiCG(const SparseMat&, const DoubleVec &rhs,
	      const PreconditionerBase&, int &maxiter, double &tolerance,
	      DoubleVec &x);

void solveBiCGStab(const SparseMat&, const DoubleVec &rhs,
		  const PreconditionerBase&, int &maxiter, double &tolerance,
		  DoubleVec &x);

void solveGMRes(const SparseMat&, const DoubleVec &rhs,
	       const PreconditionerBase&, int &maxiter, int krylov_dim,
	       double &tolerance, DoubleVec &x);

void solveDirect(const SparseMat&, const DoubleVec &rhs, DoubleVec &x);


#endif // CMATRIXMETHODS_H
