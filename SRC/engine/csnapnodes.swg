// -*- C++ -*-
// $RCSfile: csnapnodes.swg,v $
// $Revision: 1.1.4.6 $
// $Author: langer $
// $Date: 2011/10/20 20:50:28 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CSNAPNODES_SWG
#define CSNAPNODES_SWG

%module csnapnodes

%include "common/typemaps.swg"
%include "engine/typemaps.swg"
%extern "engine/cskeletonmodifier.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/csnapnodes.h"
#include "engine/cskeletonmodifier.h"
#include "engine/cskeleton2.h"
%}

%pragma(python) include="engine/csnapnodes.spy"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierPtr, CSkeletonModifierBasePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeleton2 import CDeputySkeletonPtr"

class SnapNodeTargets {

};

class SnapAll : public SnapNodeTargets {
public:
  SnapAll();
};

class SnapSelected : public SnapNodeTargets {
public:
  SnapSelected();
};

class SnapHeterogenous : public SnapNodeTargets {
public:
  SnapHeterogenous(double);
};

class SnapNodes : public CSkeletonModifier {
public:
  SnapNodes(SnapNodeTargets *trgts, CSkelModCriterion *crtrn);
  int getNumSnapped();
};

#endif
