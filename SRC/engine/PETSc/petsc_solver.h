// -*- C++ -*-
// $RCSfile: petsc_solver.h,v $
// $Revision: 1.26.18.1 $
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

#ifndef PETSCSOLVER_H
#define PETSCSOLVER_H

// Headers, where art thou?
// The required headers should preceed this file when included in the implementation (.C) file

// *****************************************
// PETScII
// *****************************************

class PETScLinearSolver: public LinearSolver
{
public:
  bool status_;
  int max_iterations;
  double relative_tolerance;//corresponds to PETSc's rtol...
  double absolute_tolerance;// ...atol...
  double dtolerance;//...dtol...
  int num_iterations;
  double residual_norm;
  PETScPreconditionerWrap *pc; //wrapper to the actual preconditioner
  int krylov_dimension; //Not used by PETSc?
//   std::string _message; // already defined in LinearSolver
//   std::vector<int> rowblocks, colblocks;

  PETScLinearSolver()
  {
  }
  PETScLinearSolver(int max_iterations, double relative_tolerance, double absolute_tolerance, double dtolerance, PETScPreconditionerWrap* pc)
  :status_(0),
  max_iterations(max_iterations),
  relative_tolerance(relative_tolerance),
  absolute_tolerance(absolute_tolerance), 
  dtolerance(dtolerance), 
  num_iterations(0),
  residual_norm(0),
  pc(pc), 
  krylov_dimension(100) // Not used by PETSc?
  {
  }

  virtual ~PETScLinearSolver()
  {
  }

  virtual void SetKSPtype(KSP &)=0;

  virtual std::string message() const
  {
    return "PETSc generic solver" + _message;
  }

  virtual bool status() const
  { 
    return status_;
  }

  virtual double get_residual()
  {
    return residual_norm;
  }

  virtual void set_blocking(const std::vector<int> rblocks,
  		    const std::vector<int> cblocks);
  virtual void set_blocking(const CSubProblem *);

  virtual void precompute(const CSRmatrix &A)
  {
  }

  virtual void postcompute()
  {
  }

  // This method (was) used when the solver is passed to SolverDriverCore
  virtual bool solve(const CSRmatrix &A, const VECTOR_D &rhs, VECTOR_D &x);
  // This method used when the solver is passed to PETScSolverDriverCore
  virtual bool solve(const Mat &A, const Vec &rhs, Vec &x);
};

// Use macro and token pasting, since the classes for all methods look the same
#define PETSCKSPSOLVER(method)						\
  class PETScKSP##method##Solver : public PETScLinearSolver		\
  {									\
  public:								\
    PETScKSP##method##Solver(int max_iterations, double relative_tolerance, double absolute_tolerance, double dtolerance, PETScPreconditionerWrap* pc) \
      :PETScLinearSolver::PETScLinearSolver(max_iterations,relative_tolerance,absolute_tolerance,dtolerance,pc) \
    {									\
    }									\
    virtual ~PETScKSP##method##Solver()					\
    {									\
    }									\
    virtual void SetKSPtype(KSP& ksp)					\
    {									\
      KSPSetType(ksp, KSP##method );					\
    }									\
    virtual std::string message() const					\
    {									\
      return "PETSc KSP " #method " solver " + _message;		\
    }									\
    virtual bool status() const						\
    {									\
      return status_;							\
    }									\
  };									\
  //end #define

PETSCKSPSOLVER(RICHARDSON)
PETSCKSPSOLVER(CHEBYCHEV)
PETSCKSPSOLVER(CG)
PETSCKSPSOLVER(BICG)
PETSCKSPSOLVER(GMRES)
PETSCKSPSOLVER(BCGS)
PETSCKSPSOLVER(CGS)
PETSCKSPSOLVER(TFQMR)
PETSCKSPSOLVER(TCQMR)
PETSCKSPSOLVER(CR)
PETSCKSPSOLVER(LSQR)
PETSCKSPSOLVER(PREONLY)

#endif // PETSCSOLVER_H
