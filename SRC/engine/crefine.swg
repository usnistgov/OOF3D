// -*- C++ -*-
// $RCSfile: crefine.swg,v $
// $Revision: 1.1.4.15 $
// $Author: langer $
// $Date: 2014/12/14 01:07:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CREFINE_SWG
#define CREFINE_SWG

%module crefine

%include "common/typemaps.swg"
%extern "engine/cskeletonmodifier.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/crefine.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonmodifier.h"
%}

%pragma(python) include="engine/crefine.spy"
%pragma(python) code="from ooflib.SWIG.engine.crefinementcriterion import RefinementTargets"
%pragma(python) code="from ooflib.SWIG.engine.crefinementcriterion import RefinementCriterion"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierPtr, CSkeletonModifierBasePtr"

class Refine : public CSkeletonModifier {
public:
  Refine(RefinementTargets *trgts, RefinementCriterion *crtrn, double a);
};

void printRuleUsage();
void clearRuleUsage();
void avoidDeadLocks(bool);

#endif	// CREFINE_SWG
