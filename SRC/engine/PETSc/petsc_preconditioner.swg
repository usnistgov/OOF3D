// -*- C++ -*-
// $RCSfile: petsc_preconditioner.swg,v $
// $Revision: 1.10.18.1 $
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

#ifndef PETSCPRECONDITIONER_SWG
#define PETSCPRECONDITIONER_SWG

%module petsc_preconditioner
%include "common/typemaps.swg"

%pragma(python) include="engine/PETSc/petsc_preconditioner.spy"

%{
extern "C"
{
#include "petscksp.h"
}
#include "engine/PETSc/petsc_preconditioner.h"
%}

class PETScPreconditionerWrap
{
};

class PETScJACOBIPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScJACOBIPreconditioner();
  virtual ~PETScJACOBIPreconditioner();
};

class PETScBJACOBIPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScBJACOBIPreconditioner();
  virtual ~PETScBJACOBIPreconditioner();
};

class PETScSORPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScSORPreconditioner();
  virtual ~PETScSORPreconditioner();
};

class PETScEISENSTATPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScEISENSTATPreconditioner();
  virtual ~PETScEISENSTATPreconditioner();
};

class PETScICCPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScICCPreconditioner();
  virtual ~PETScICCPreconditioner();
};

class PETScILUPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScILUPreconditioner();
  virtual ~PETScILUPreconditioner();
};

class PETScASMPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScASMPreconditioner();
  virtual ~PETScASMPreconditioner();
};

class PETScKSPPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScKSPPreconditioner();
  virtual ~PETScKSPPreconditioner();
};

class PETScLUPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScLUPreconditioner();
  virtual ~PETScLUPreconditioner();
};

class PETScCHOLESKYPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScCHOLESKYPreconditioner();
  virtual ~PETScCHOLESKYPreconditioner();
};

class PETScNONEPreconditioner : public PETScPreconditionerWrap
{
public:
  PETScNONEPreconditioner();
  virtual ~PETScNONEPreconditioner();
};

#endif // PETSCPRECONDITIONER_SWG
