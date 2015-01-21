// -*- C++ -*-
// $RCSfile: petsc_preconditioner.h,v $
// $Revision: 1.14.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PETSCPRECONDITIONER_H
#define PETSCPRECONDITIONER_H

// Headers, where art thou?
// The required headers should preceed this file when included in the implementation (.C) file

// *****************************************
// PETScII
// *****************************************

class PETScPreconditionerWrap
{
public:
  PETScPreconditionerWrap()
  {
  }
  virtual ~PETScPreconditionerWrap()
  {
  }
  virtual void SetPCtype(PC &)=0;
};

// Use macro and token pasting, since the classes for all methods look the same
// (assume the default options for each preconditioner are used)
#define PETSCPRECONDITIONER(method)					\
  class PETSc##method##Preconditioner : public PETScPreconditionerWrap	\
  {									\
  public:								\
    PETSc##method##Preconditioner()					\
    {									\
    }									\
    virtual ~PETSc##method##Preconditioner()				\
    {									\
    }									\
    virtual void SetPCtype(PC& pchandle)				\
    {									\
      PCSetType(pchandle,PC##method);					\
    }									\
  };									\
  // end #define

PETSCPRECONDITIONER(JACOBI)
PETSCPRECONDITIONER(BJACOBI)
PETSCPRECONDITIONER(SOR)
PETSCPRECONDITIONER(EISENSTAT)
PETSCPRECONDITIONER(ICC)
PETSCPRECONDITIONER(ILU)
PETSCPRECONDITIONER(ASM)
PETSCPRECONDITIONER(KSP)
//PETSCPRECONDITIONER(COMPOSITE)
PETSCPRECONDITIONER(LU)
PETSCPRECONDITIONER(CHOLESKY)
PETSCPRECONDITIONER(NONE)
//PETSCPRECONDITIONER(SHELL)

#endif // PETSCPRECONDITIONER_H
