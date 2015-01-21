// -*- C++ -*-
// $RCSfile: sparsesolve.C,v $
// $Revision: 1.1 $
// $Author: langer $
// $Date: 2007/06/14 18:17:38 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@ctcms.nist.gov. 
 */

#include <oofconfig.h>

// This is just an example of how to solve a sparse matrix equation.

#include "engine/sparselink.h"
#include "engine/matvec.h"
#include "engine/csrmatrix.h"
#include "engine/solver.h"
#include "engine/preconditioner.h"

#include <iostream>

void f() {

  // Create and fill a sparse matrix and right hand side
  int n = 10;			// size of the matrix
  SparseLinkMatrix splmat(n, n); // matrix
  VECTOR_D rhs(n);		// right-hand side vector

  for(int i=0; i<n; i++) {
    rhs(i) = something;
    for(int j=0; j<n; j++)
      splmat(i,j) = something;
  }
  // convert the matrix to a form more suitable for use by solvers
  CSRMatrix mat(new SPARSE_MATRIX_D(splmat));

  // Create a preconditioner object, from preconditioner.h.  Different
  // ones will work better in different situations.  Choosing the
  // right preconditioner is a black art.  Use Un_conditioner if you
  // want no preconditioning.
  ILU_Preconditioner preconditioner(mat);

  // Create a solver object.  Different ones are available in
  // solver.h.  Use CGSolver if the matrix is symmetric.
  int max_iterations, int krylov_dimension; // set these somehow
  double tolerance;		// this too
  GMRESSolver solver(max_iterations, krylov_dimension, tolerance, 
		     &preconditioner);

  // Vector of unknowns. Should be initialized with a good guess, if
  // available.
  VECTOR_D x(n);

  // Solve for x.
  int status = solver.solve(mat, rhs, x);  
  // status == 1 is success, 0 is failure.
  
  std::cout << solver.message() << std::endl;
}
