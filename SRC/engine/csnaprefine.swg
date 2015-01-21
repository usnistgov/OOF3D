// -*- C++ -*-
// $RCSfile: csnaprefine.swg,v $
// $Revision: 1.1.4.8 $
// $Author: fyc $
// $Date: 2014/02/18 16:38:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSNAPREFINE_SWG
#define CSNAPREFINE_SWG

%module csnaprefine

%include "engine/typemaps.swg"
%extern "engine/crefine.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/csnaprefine.h"
#include "engine/crefine.h"
#include "engine/cskeleton2.h"
%}

%pragma(python) include="engine/csnaprefine.spy"

%pragma(python) code="from ooflib.SWIG.engine.crefine import RefinePtr"
%pragma(python) code="from ooflib.SWIG.engine.crefinementcriterion import RefinementTargets"
%pragma(python) code="from ooflib.SWIG.engine.crefinementcriterion import RefinementCriterion"

class SnapRefine : public Refine {
public:
  SnapRefine(RefinementTargets *trgts, RefinementCriterion *crtrn, 
	     double min, double a);
};


#endif
