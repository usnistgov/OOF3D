// -*- C++ -*-
// $RCSfile: petsc_solver.swg,v $
// $Revision: 1.21.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:23 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PETSCSOLVER_SWG
#define PETSCSOLVER_SWG

%module petsc_solver
%include "common/typemaps.swg"

%typemap(python, out) PETScPreconditionerWrap*
{
  $target = $source->pythonObject();
}

%pragma(python) include="engine/PETSc/petsc_solver.spy"
%{
#include <oofconfig.h>
#include "engine/csubproblem.h"
#include "engine/solver.h"
#include "engine/csrmatrix.h"
#include "engine/matvec.h"
#include <string>
extern "C"
{
#include "petscksp.h"
}
#include "engine/PETSc/petsc_preconditioner.h"
#include "engine/PETSc/petsc_solver.h"
%}

// *************************************
// PETScII
// *************************************

// We want PETScDefaultSolver to be derived from PETScLinearSolver so that it is a
// separate item in the driver list of the Solver page. We also have to derive it
// from LinearSolver because SolverDriverCore expects a LinearSolver.
class LinearSolver
{
};

class PETScLinearSolver : public LinearSolver
{
};

class PETScKSPRICHARDSONSolver : public PETScLinearSolver
{
public:
  PETScKSPRICHARDSONSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPRICHARDSONSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPCHEBYCHEVSolver : public PETScLinearSolver
{
public:
  PETScKSPCHEBYCHEVSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPCHEBYCHEVSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPCGSolver : public PETScLinearSolver
{
public:
  PETScKSPCGSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPCGSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPBICGSolver : public PETScLinearSolver
{
public:
  PETScKSPBICGSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPBICGSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPGMRESSolver : public PETScLinearSolver
{
public:
  PETScKSPGMRESSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPGMRESSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPBCGSSolver : public PETScLinearSolver
{
public:
  PETScKSPBCGSSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPBCGSSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPCGSSolver : public PETScLinearSolver
{
public:
  PETScKSPCGSSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPCGSSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPTFQMRSolver : public PETScLinearSolver
{
public:
  PETScKSPTFQMRSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPTFQMRSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPTCQMRSolver : public PETScLinearSolver
{
public:
  PETScKSPTCQMRSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPTCQMRSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPCRSolver : public PETScLinearSolver
{
public:
  PETScKSPCRSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPCRSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPLSQRSolver : public PETScLinearSolver
{
public:
  PETScKSPLSQRSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPLSQRSolver();
  virtual string message() const;
  virtual bool status() const;
};

class PETScKSPPREONLYSolver : public PETScLinearSolver
{
public:
  PETScKSPPREONLYSolver(int, double, double, double, PETScPreconditionerWrap *);
  virtual ~PETScKSPPREONLYSolver();
  virtual string message() const;
  virtual bool status() const;
};

#endif // PETSCSOLVER_SWG
