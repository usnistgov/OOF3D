// -*- C++ -*-
// $RCSfile: entiremeshsubproblem.swg,v $
// $Revision: 1.4.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ENTIREMESHSUBPROBLEM_SWG
#define ENTIREMESHSUBPROBLEM_SWG

%module entiremeshsubproblem

%include "engine/typemaps.swg"
%extern "engine/csubproblem.swg"
%pragma(python) code="from ooflib.SWIG.engine.csubproblem import CSubProblemPtr"
%pragma(python) code="from ooflib.SWIG.common.lock import LockPtr"
%pragma(python) include="engine/entiremeshsubproblem.spy"


%{
#include "engine/entiremeshsubproblem.h"
%}

class CEntireMeshSubProblem : public CSubProblem {
public:
  CEntireMeshSubProblem();
  ~CEntireMeshSubProblem();
};

#endif // ENTIREMESHSUBPROBLEM_SWG

