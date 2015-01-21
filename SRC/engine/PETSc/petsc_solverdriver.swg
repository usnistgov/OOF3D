// -*- C++ -*-
// $RCSfile: petsc_solverdriver.swg,v $
// $Revision: 1.6.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:24 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PETSCSOLVERDRIVER_SWG
#define PETSCSOLVERDRIVER_SWG

%module petsc_solverdriver
%include "engine/typemaps.swg"

%pragma(python) include="engine/PETSc/petsc_solverdriver.spy"

%{
#include <oofconfig.h>
#include "engine/csrmatrix.h"
#include "engine/csubproblem.h"
#include "engine/matvec.h"
#include "engine/solver.h"
extern "C"
{
#include "petscksp.h"
}
#include "engine/PETSc/petsc_solverdriver.h"
#include "engine/steppingscheme.h"
%}

class PETScSolverDriverCore
{
public:
  PETScSolverDriverCore(SteppingScheme*, LinearSolver *, CSubProblem *);
  int nrows();
  int ncols();
  virtual void precompute();
  virtual int solve();
  virtual void postcompute();
  double residual();
  void clear_memory();
  virtual ~PETScSolverDriverCore();
};

void InitPETSc(CharPtrVec *argv);

#endif // PETSCSOLVERDRIVER_SWG
