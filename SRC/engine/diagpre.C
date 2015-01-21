// -*- C++ -*-
// $RCSfile: diagpre.C,v $
// $Revision: 1.2.10.3 $
// $Author: langer $
// $Date: 2014/10/15 20:53:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include <stdlib.h>
#include "common/doublevec.h"
#include "engine/diagpre.h"
#include "engine/sparsemat.h"
#include "engine/ooferror.h"

const std::string JacobiPreconditioner::classname_("JacobiPreconditioner");
const std::string DiagPreconditionerCore::classname_("DiagPreconditionerCore");
const std::string DiagPreconditionerCore::modulename_(
						 "ooflib.SWIG.engine.diagpre");

DiagPreconditionerCore::DiagPreconditionerCore(const SparseMat &C)
  : diag_(C.nrows())
{
  for(unsigned int i=0; i<C.nrows(); i++) {
    for(SparseMat::const_row_iterator ij=C.begin(i); ij!=C.end(i); ++ij) {
      if(ij.col() == i) {
	if(*ij == 0.0)
	  throw ErrSetupError("Zero element in diagonal preconditioner!");
	diag_[i] = 1./(*ij);
	break;
      }
    }
  }
}

DoubleVec DiagPreconditionerCore::solve(const DoubleVec &x) const 
{
  DoubleVec y(x.size());

  for(unsigned int i = 0; i < x.size(); i++)
    y[i] = x[i] * diag_[i];
  
  return y;
}


DoubleVec DiagPreconditionerCore::trans_solve (const DoubleVec &x) const 
{
  return solve(x);
}
