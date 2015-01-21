// -*- C++ -*-
// $RCSfile: preconditioner.swg,v $
// $Revision: 1.21.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:41 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PRECONDITIONER_SWG
#define PRECONDITIONER_SWG

%module preconditioner
%include "engine/typemaps.swg"
%extern "engine/sparsemat.swg"
%extern "common/doublevec.swg"

%pragma(python) code="from ooflib.SWIG.common.doublevec import DoubleVecPtr"

%pragma(python) include="engine/preconditioner.spy"

%{
#include "engine/preconditioner.h"
#include "common/doublevec.h"
%}

%typemap(python, out) PreconditionerBase* {
  // typemap(python, out) PreconditionerBase*
  $target = $source->pythonObject();
  if(!$target)
    return 0;
  // Transfer ownership to python.
  PyObject_SetAttrString($target, "thisown", PyInt_FromLong(1));
}

class PreconditionerBase {
public:
  ~PreconditionerBase();
  DoubleVec solve(DoubleVec&);
  DoubleVec trans_solve(DoubleVec&);
};

class Preconditioner {
public:
  ~Preconditioner();
  PreconditionerBase *create_preconditioner(SparseMat&);
};

class ILUPreconditioner : public Preconditioner {
public:
  ILUPreconditioner();
  ~ILUPreconditioner();
};

class ICPreconditioner : public Preconditioner {
public:
  ICPreconditioner();
  ~ICPreconditioner();
};

class UnPreconditioner : public Preconditioner {
public:
  UnPreconditioner();
  ~UnPreconditioner();
};

class JacobiPreconditioner: public Preconditioner {
public:
  JacobiPreconditioner();
  ~JacobiPreconditioner();
};

// Most PreconditionerBase subclasses are swigged separately.
// UnPreconditioner is trivial, so it's in preconditioner.h and
// preconditioner.swg.
class UnconditionerCore : public PreconditionerBase {
public:
  UnconditionerCore();
  ~UnconditionerCore();
};

#endif // PRECONDITIONER_SWG





