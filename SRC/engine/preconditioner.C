// -*- C++ -*-
// $RCSfile: preconditioner.C,v $
// $Revision: 1.15.10.1 $
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

#include "common/doublevec.h"
#include "engine/preconditioner.h"
#include "engine/ilupre.h"
#include "engine/icpre.h"
#include "engine/diagpre.h"

ILUPreconditioner::~ILUPreconditioner() {}

PreconditionerBase* 
ILUPreconditioner::build_preconditioner(const SparseMat &A) const {
  return new ILUPreconditionerCore(A);
}

PreconditionerBase* 
ILUPreconditioner::create_preconditioner(const SparseMat &A) const
{
  return build_preconditioner(A);
}

ICPreconditioner::~ICPreconditioner() {}


PreconditionerBase* 
ICPreconditioner::build_preconditioner(const SparseMat &A) const {
  return new ICPreconditionerCore(A);
}

PreconditionerBase * 
ICPreconditioner::create_preconditioner(const SparseMat &A) const
{
  return build_preconditioner(A);
}


UnPreconditioner::~UnPreconditioner() {}

PreconditionerBase* 
UnPreconditioner::build_preconditioner(const SparseMat &A) const {
  return new UnconditionerCore();
}

PreconditionerBase *
UnPreconditioner::create_preconditioner(const SparseMat &A) const
{
  return build_preconditioner(A);
}


JacobiPreconditioner::~JacobiPreconditioner() {}

PreconditionerBase*
JacobiPreconditioner::build_preconditioner(const SparseMat &A) const {
  return new DiagPreconditionerCore(A);
}

PreconditionerBase*
JacobiPreconditioner::create_preconditioner(const SparseMat &A) const
{
  return build_preconditioner(A);
}

const std::string Preconditioner::modulename_(
				      "ooflib.SWIG.engine.preconditioner");
const std::string UnPreconditioner::classname_("UnPreconditioner");

const std::string UnconditionerCore::modulename_(
					 "ooflib.SWIG.engine.preconditioner");
const std::string UnconditionerCore::classname_("UnconditionerCore");
