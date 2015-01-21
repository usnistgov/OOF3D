// -*- C++ -*-
// $RCSfile: preconditioner.h,v $
// $Revision: 1.28.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:40 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PRECONDITIONER_H
#define PRECONDITIONER_H

class Preconditioner;
class PreconditionerBase;

#include "engine/sparsemat.h"
#include "common/pythonexportable.h"
#include <string>
#include <vector>

class DoubleVec;

#ifdef HAVE_PETSC
// #include "petscvec.h"
// #include "petscmat.h"
// #include "petscsles.h"
#endif //HAVE_PETSC

// PreconditionerBase is the base class for the 'Core'
// preconditioners, which are the ones that do the actual work.  They
// generally can't be constructed until the matrix that they
// precondition is constructed, so there's a separate Preconditioner
// class hierarchy, whose instances create an appropriate
// PreconditionerBase subclass once the matrix is known.  For each
// Preconditioner subclass, the method
// Preconditioner::create_preconditioner returns a new
// PreconditionerBase object of the appropriate subclass.

// PreconditionerBase is a PythonExportable subclass so that testing
// and debugging functions in the core preconditioners can be run in
// the test suites.

class PreconditionerBase : public PythonExportable<PreconditionerBase> {
public:
  virtual ~PreconditionerBase() {}
  virtual DoubleVec solve(const DoubleVec&) const = 0;
  virtual DoubleVec trans_solve(const DoubleVec&) const = 0;
#ifdef HAVE_PETSCOLD
  virtual void set(PC &precond) const = 0;
#endif //HAVE_PETSC
};

// Only the trivial PreconditionerBase subclass is defined here.  The
// others have their own files (ilupre.h, et al).

class UnconditionerCore : public PreconditionerBase {
public:
  UnconditionerCore() {}
  virtual DoubleVec solve(const DoubleVec &x) const { return x; }
  virtual DoubleVec trans_solve(const DoubleVec &x) const { return x; }
  static const std::string classname_;
  virtual const std::string &classname() const { return classname_; }
  static const std::string modulename_;
  virtual const std::string &modulename() const { return modulename_; }

#ifdef HAVE_PETSCOLD
  virtual void set(PC &precond) const {};
#endif //HAVE_PETSC
};

class Preconditioner;

#ifdef HAVE_PETSCOLD
#include "petscvec.h"
#include "petscmat.h"
#include "petscsles.h"
#include "engine/preconditioner.h"
#endif //HAVE_PETSC

class Preconditioner : public PythonExportable<Preconditioner> {
public:
  Preconditioner() {}
  virtual ~Preconditioner() {}

  virtual PreconditionerBase * create_preconditioner(const SparseMat &A)
    const = 0;
  static const std::string modulename_;
  virtual const std::string &modulename() const { return modulename_; }

#ifdef HAVE_PETSCOLD
  virtual void set(PC) const {};//sets correct preconditioner in derived class
#endif //HAVE_PETSC
};

class ILUPreconditioner : public Preconditioner { 
//wrapper for core class
public:
  ILUPreconditioner() {}
  virtual ~ILUPreconditioner(); 
  virtual PreconditionerBase * create_preconditioner(const SparseMat &A) const;
  virtual PreconditionerBase * build_preconditioner(const SparseMat &A) const;
  
  static const std::string classname_;
  virtual const std::string &classname() const { return classname_; }
};

class ICPreconditioner : public Preconditioner  { 
//wrapper for core class
public:
  ICPreconditioner() {}
  virtual ~ICPreconditioner();
  virtual PreconditionerBase * create_preconditioner(const SparseMat &A) const;
  virtual PreconditionerBase * build_preconditioner(const SparseMat &A) const;
  static const std::string classname_;
  virtual const std::string &classname() const { return classname_; }  
};
    
class UnPreconditioner  : public Preconditioner { 
//wrapper for core class
public:
  UnPreconditioner() {}
  virtual ~UnPreconditioner();
  virtual PreconditionerBase * create_preconditioner(const SparseMat &A) const;
  virtual PreconditionerBase * build_preconditioner(const SparseMat &A) const;
  static const std::string classname_;
  virtual const std::string &classname() const { return classname_; }  
}; 


class JacobiPreconditioner : public Preconditioner {
public:
  JacobiPreconditioner() {}
  virtual ~JacobiPreconditioner();
  virtual PreconditionerBase * create_preconditioner(const SparseMat &A) const;
  virtual PreconditionerBase * build_preconditioner(const SparseMat &A) const;
  static const std::string classname_;
  virtual const std::string &classname() const { return classname_; }
};

#endif // PRECONDITIONER_H
