// -*- C++ -*-
// $RCSfile: cnonlinearsolver.C,v $
// $Revision: 1.2.8.2 $
// $Author: langer $
// $Date: 2013/11/08 20:43:09 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/cnonlinearsolver.h"

CNonlinearSolver::CNonlinearSolver(bool nonlinear)
  : nonlinear_(nonlinear),
    need_Jacobian_(false),
    need_Residual_(false)
{
  jacReqChanged_.backdate();
  resReqChanged_.backdate();
}

void CNonlinearSolver::requireJacobian(bool val) {
  if(val && !need_Jacobian_)
    ++jacReqChanged_;
  need_Jacobian_ = val;
}

void CNonlinearSolver::requireResidual(bool val) {
  if(val && !need_Residual_)
    ++resReqChanged_;
  need_Residual_ = val;
}
