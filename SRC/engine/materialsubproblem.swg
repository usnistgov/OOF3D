// -*- C++ -*-
// $RCSfile: materialsubproblem.swg,v $
// $Revision: 1.5.2.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:31 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MATERIALSUBPROBLEM_SWG
#define MATERIALSUBPROBLEM_SWG

%module materialsubproblem

%include "engine/typemaps.swg"
%extern "engine/csubproblem.swg"
%extern "engine/material.swg"
%pragma(python) include="engine/materialsubproblem.spy"
%pragma(python) code="from ooflib.SWIG.engine.csubproblem import CSubProblemPtr"
%pragma(python) code="from ooflib.SWIG.common.lock import LockPtr"

%{
#include "engine/material.h"
#include "engine/materialsubproblem.h"
%}

class CMaterialSubProblem : public CSubProblem {
public:
  CMaterialSubProblem(Material*);
};

#endif // MATERIALSUBPROBLEM_SWG
