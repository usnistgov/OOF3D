// -*- C++ -*-
// $RCSfile: petsc_solver.C,v $
// $Revision: 1.38.12.1 $
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
#include "petsc_preconditioner.h"
#include "petsc_solver.h"
#include "petsc_solverdriver.h"

// ****************************************************************************
// PETScII
// ****************************************************************************

void PETScLinearSolver::set_blocking(const std::vector<int> rb, 
			  const std::vector<int> cb)
{
  rowblocks = rb;
  colblocks = cb;
}

void PETScLinearSolver::set_blocking(const CSubProblem * subp)
{
  rowblocks = subp->A_rowblocks();
  colblocks = subp->A_colblocks();
}

#define MYCHKERRQ(x) CHKERRQ((x))

//As of 11/13/07, the petsc version in mr-french is 2.3.2
#define PETSCVERSION2p3p1
// Written for PETSc version 2.2.0 (March 10, 2004), installed in sancho
bool PETScLinearSolver::solve(const CSRmatrix &A, const VECTOR_D &rhs, VECTOR_D &x)
{
  PetscPrintf(PETSC_COMM_WORLD,"Entering PETSc solver\n");

  Mat Apetsc;
#ifdef PETSCVERSION2p3p1
  PetscInt Istart,Iend,I,J;
  PetscInt Adim=x.size();
  PetscErrorCode ierr;
  ierr=MatCreate(PETSC_COMM_WORLD,&Apetsc);MYCHKERRQ(ierr);
  ierr=MatSetSizes(Apetsc,PETSC_DECIDE,PETSC_DECIDE,Adim*Adim,Adim*Adim);MYCHKERRQ(ierr);
#else
  int Istart,Iend,I,J;
  int Adim=x.size();
  int ierr;
  ierr=MatCreate(PETSC_COMM_WORLD,PETSC_DECIDE,PETSC_DECIDE,Adim,Adim,&Apetsc);MYCHKERRQ(ierr);
#endif
  //Not optional
  ierr=MatSetFromOptions(Apetsc);MYCHKERRQ(ierr);

  PetscScalar S;
  ierr=MatGetOwnershipRange(Apetsc,&Istart,&Iend);MYCHKERRQ(ierr);
  for(I=Istart;I<Iend;I++)
    for(J=0;J<Adim;J++)
      {
        S=A(I,J);
        ierr=MatSetValues(Apetsc,1,&I,1,&J,&S,INSERT_VALUES);MYCHKERRQ(ierr);
      }
  ierr=MatAssemblyBegin(Apetsc,MAT_FINAL_ASSEMBLY);MYCHKERRQ(ierr);
  //Anything you want to do in the mean time? Put it here.
  ierr=MatAssemblyEnd(Apetsc,MAT_FINAL_ASSEMBLY);MYCHKERRQ(ierr);

  // Take just a little peek before continuing
  //MatView(Apetsc,PETSC_VIEWER_STDOUT_WORLD);

  Vec xpetsc,rhspetsc;
  ierr=VecCreate(PETSC_COMM_WORLD,&xpetsc);MYCHKERRQ(ierr);
  //PetscObjectSetName((PetscObject) xpetsc, "Solution");//optional?
  ierr=VecSetSizes(xpetsc,PETSC_DECIDE,Adim);MYCHKERRQ(ierr);
  ierr=VecSetFromOptions(xpetsc);MYCHKERRQ(ierr);
  ierr=VecDuplicate(xpetsc,&rhspetsc);MYCHKERRQ(ierr);
  for(I=0; I<Adim; I++)
    {
      S=rhs(I);
      ierr=VecSetValues(rhspetsc,1,&I,&S,INSERT_VALUES);MYCHKERRQ(ierr);
    }
  ierr=VecAssemblyBegin(rhspetsc);MYCHKERRQ(ierr);
  //Anything you want to do in the mean time? Put it here.
  ierr=VecAssemblyEnd(rhspetsc);MYCHKERRQ(ierr);

  // Take a peek
  //VecView(rhspetsc,PETSC_VIEWER_STDOUT_WORLD);

  KSP ksp;
  ierr=KSPCreate(PETSC_COMM_WORLD,&ksp);MYCHKERRQ(ierr);
  ierr=KSPSetOperators(ksp,Apetsc,Apetsc,DIFFERENT_NONZERO_PATTERN);MYCHKERRQ(ierr);
  //ierr=KSPSetTolerances(ksp,1.e-2/((Adim+1)*(Adim+1)),PETSC_DEFAULT,PETSC_DEFAULT,PETSC_DEFAULT);MYCHKERRQ(ierr);
  ierr=KSPSetTolerances(ksp,this->relative_tolerance,this->absolute_tolerance,this->dtolerance,this->max_iterations);MYCHKERRQ(ierr);

  // The following class method (not a KSP method) calls KSPSetType()
  this->SetKSPtype(ksp);

  // The following lines eventually call PCSetType(pchandle)
  PC pchandle;
  ierr=KSPGetPC(ksp,&pchandle);MYCHKERRQ(ierr);
  this->pc->SetPCtype(pchandle);

  //ierr=KSPSetFromOptions(ksp);MYCHKERRQ(ierr);

#ifdef PETSCVERSION2p3p1
  ierr=KSPSolve(ksp,rhspetsc,xpetsc);MYCHKERRQ(ierr);
#else
  ierr=KSPSetRhs(ksp,rhspetsc);MYCHKERRQ(ierr);
  ierr=KSPSetSolution(ksp,xpetsc);MYCHKERRQ(ierr);
  ierr=KSPSolve(ksp);MYCHKERRQ(ierr);
#endif

  KSPView(ksp,PETSC_VIEWER_STDOUT_WORLD);

  //Possible codes for converged reason in petscksp.h
  //typedef enum {/* converged */
  //            KSP_CONVERGED_RTOL               =  2,
  //            KSP_CONVERGED_ATOL               =  3,
  //            KSP_CONVERGED_ITS                =  4,
  //            KSP_CONVERGED_QCG_NEG_CURVE      =  5,
  //            KSP_CONVERGED_QCG_CONSTRAINED    =  6,
  //            KSP_CONVERGED_STEP_LENGTH        =  7,
  //            /* diverged */
  //            KSP_DIVERGED_ITS                 = -3,
  //            KSP_DIVERGED_DTOL                = -4,
  //            KSP_DIVERGED_BREAKDOWN           = -5,
  //            KSP_DIVERGED_BREAKDOWN_BICG      = -6,
  //            KSP_DIVERGED_NONSYMMETRIC        = -7,
  //            KSP_DIVERGED_INDEFINITE_PC       = -8,
  //            KSP_CONVERGED_ITERATING          =  0} KSPConvergedReason;
  KSPConvergedReason reason;
  ierr=KSPGetConvergedReason(ksp,&reason);MYCHKERRQ(ierr);
  if(int(reason)<0)
    {
      status_=1; // failed to converge
      _message+="failed to converge!\n";
    }
  else
    {
      status_=0;
      _message+="converged.\n";
    }
  ierr=KSPGetIterationNumber(ksp,&this->num_iterations);MYCHKERRQ(ierr);
  ierr=KSPGetResidualNorm(ksp,&this->residual_norm);MYCHKERRQ(ierr);
  this->_message+="KSPConvergedReason code = " + to_string(reason) +
    ", residualnorm = " + to_string(this->residual_norm) +
    ", iteration number = " + to_string(this->num_iterations);

  PetscScalar* temp_array;
  VecGetArray(xpetsc, &temp_array);
  for(I = 0; I<Adim; I++)
    {
      x(I)=double(temp_array[I]);
    }
  VecRestoreArray(xpetsc,&temp_array);

  ierr=KSPDestroy(ksp);MYCHKERRQ(ierr);
  ierr=VecDestroy(rhspetsc);MYCHKERRQ(ierr);
  ierr=VecDestroy(xpetsc);MYCHKERRQ(ierr);
  ierr=MatDestroy(Apetsc);MYCHKERRQ(ierr);

  PetscPrintf(PETSC_COMM_WORLD,"Leaving PETSc solver\n");
  return !status_;
}

// This one for PETScSolverDriverCore
bool PETScLinearSolver::solve(const Mat &Apetsc, const Vec &rhspetsc, Vec &xpetsc)
{
  PetscPrintf(PETSC_COMM_WORLD,"Entering PETSc solver\n");

  int ierr;
  KSP ksp;
  ierr=KSPCreate(PETSC_COMM_WORLD,&ksp);MYCHKERRQ(ierr);
  ierr=KSPSetOperators(ksp,Apetsc,Apetsc,DIFFERENT_NONZERO_PATTERN);MYCHKERRQ(ierr);
  //ierr=KSPSetTolerances(ksp,1.e-2/((Adim+1)*(Adim+1)),PETSC_DEFAULT,PETSC_DEFAULT,PETSC_DEFAULT);MYCHKERRQ(ierr);
  ierr=KSPSetTolerances(ksp,this->relative_tolerance,this->absolute_tolerance,this->dtolerance,this->max_iterations);MYCHKERRQ(ierr);

  // The following class method (not a KSP method) calls KSPSetType()
  this->SetKSPtype(ksp);

  // The following lines eventually call PCSetType(pchandle)
  PC pchandle;
  ierr=KSPGetPC(ksp,&pchandle);MYCHKERRQ(ierr);
  this->pc->SetPCtype(pchandle);

  //ierr=KSPSetFromOptions(ksp);MYCHKERRQ(ierr);

#ifdef PETSCVERSION2p3p1
  ierr=KSPSolve(ksp,rhspetsc,xpetsc);MYCHKERRQ(ierr);
#else
  ierr=KSPSetRhs(ksp,rhspetsc);MYCHKERRQ(ierr);
  ierr=KSPSetSolution(ksp,xpetsc);MYCHKERRQ(ierr);
  ierr=KSPSolve(ksp);MYCHKERRQ(ierr);
#endif

  KSPView(ksp,PETSC_VIEWER_STDOUT_WORLD);

  //Possible codes for converged reason in petscksp.h
  //typedef enum {/* converged */
  //            KSP_CONVERGED_RTOL               =  2,
  //            KSP_CONVERGED_ATOL               =  3,
  //            KSP_CONVERGED_ITS                =  4,
  //            KSP_CONVERGED_QCG_NEG_CURVE      =  5,
  //            KSP_CONVERGED_QCG_CONSTRAINED    =  6,
  //            KSP_CONVERGED_STEP_LENGTH        =  7,
  //            /* diverged */
  //            KSP_DIVERGED_ITS                 = -3,
  //            KSP_DIVERGED_DTOL                = -4,
  //            KSP_DIVERGED_BREAKDOWN           = -5,
  //            KSP_DIVERGED_BREAKDOWN_BICG      = -6,
  //            KSP_DIVERGED_NONSYMMETRIC        = -7,
  //            KSP_DIVERGED_INDEFINITE_PC       = -8,
  //            KSP_CONVERGED_ITERATING          =  0} KSPConvergedReason;
  KSPConvergedReason reason;
  ierr=KSPGetConvergedReason(ksp,&reason);MYCHKERRQ(ierr);
  if(int(reason)<0)
    {
      status_=1; // failed to converge
      _message+="failed to converge!\n";
    }
  else
    {
      status_=0;
      _message+="converged.\n";
    }
  ierr=KSPGetIterationNumber(ksp,&this->num_iterations);MYCHKERRQ(ierr);
  ierr=KSPGetResidualNorm(ksp,&this->residual_norm);MYCHKERRQ(ierr);
  this->_message+="KSPConvergedReason code = " + to_string(reason) +
    ", residualnorm = " + to_string(this->residual_norm) +
    ", iteration number = " + to_string(this->num_iterations);

#if 0
  PetscScalar* temp_array;
  VecGetArray(xpetsc, &temp_array);
  for(I = 0; I<Adim; I++)
    {
      x(I)=double(temp_array[I]);
    }
  VecRestoreArray(xpetsc,&temp_array);
#endif

  ierr=KSPDestroy(ksp);MYCHKERRQ(ierr);
  //ierr=VecDestroy(rhspetsc);MYCHKERRQ(ierr);
  //ierr=VecDestroy(xpetsc);MYCHKERRQ(ierr);
  //ierr=MatDestroy(Apetsc);MYCHKERRQ(ierr);

  PetscPrintf(PETSC_COMM_WORLD,"Leaving PETSc solver\n");
  return !status_;
}
