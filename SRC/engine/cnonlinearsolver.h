// -*- C++ -*-
// $RCSfile: cnonlinearsolver.h,v $
// $Revision: 1.3.8.2 $
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

#ifndef CNONLINEARSOLVER_H
#define CNONLINEARSOLVER_H


// Base class for Python NonlinearSolver classes, so that
// CSubproblem::make_linear_system can find out what quantities the
// solver wants it to compute.

#include "common/timestamp.h"

class CNonlinearSolver {
private:
  bool nonlinear_;
  bool need_Jacobian_;
  bool need_Residual_;
  TimeStamp jacReqChanged_;
  TimeStamp resReqChanged_;
 public:
  CNonlinearSolver(bool nonlinear);

  bool nonlinear() const { return nonlinear_; }

  void requireJacobian(bool val);
  bool needsJacobian() const { return need_Jacobian_; }
  const TimeStamp &jacobianRequirementChanged() const { return jacReqChanged_; }

  void requireResidual(bool val);
  bool needsResidual() const { return need_Residual_; }
  const TimeStamp &residualRequirementChanged() const { return resReqChanged_; }
};

#endif
