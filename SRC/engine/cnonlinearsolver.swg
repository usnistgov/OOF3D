// -*- C++ -*-
// $RCSfile: cnonlinearsolver.swg,v $
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

#ifndef CNONLINEARSOLVER_SWG
#define CNONLINEARSOLVER_SWG

%module cnonlinearsolver
%include "engine/typemaps.swg"

%{
#include "engine/cnonlinearsolver.h"
%}
%extern "common/timestamp.swg"
%pragma(python) code="from ooflib.SWIG.common.timestamp import TimeStampPtr"

class CNonlinearSolver {
public:
  CNonlinearSolver(bool);
  bool nonlinear(); 
  void requireJacobian(bool);
  bool needsJacobian();
  const TimeStamp &jacobianRequirementChanged();
  void requireResidual(bool);
  bool needsResidual();
  const TimeStamp &residualRequirementChanged();
};

#endif // CNONLINEARSOLVER_SWG

