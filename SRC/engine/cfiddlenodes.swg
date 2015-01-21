// -*- C++ -*-
// $RCSfile: cfiddlenodes.swg,v $
// $Revision: 1.1.4.10 $
// $Author: langer $
// $Date: 2011/10/20 20:50:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CFIDDLENODES_SWG
#define CFIDDLENODES_SWG

%module cfiddlenodes

%include "common/typemaps.swg"
%include "engine/typemaps.swg"
%extern "engine/cskeletonmodifier.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/cfiddlenodes.h"
#include "engine/cskeletonmodifier.h"
#include "engine/cskeleton2.h"
%}

%pragma(python) include="engine/cfiddlenodes.spy"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkeletonModifierPtr, CSkeletonModifierBasePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonmodifier import CSkelModCriterionPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeleton2 import CDeputySkeletonPtr"

class FiddleNodesTargets {
public:
  void cleanUp();
};

class AllNodes : public FiddleNodesTargets {
public:
  AllNodes();
};

class SelectedNodes : public FiddleNodesTargets {
public:
  SelectedNodes();
};

class NodesInGroup : public FiddleNodesTargets {
public:
  NodesInGroup(char*);
};

class FiddleSelectedElements : public FiddleNodesTargets {
public:
  FiddleSelectedElements();
};

class FiddleHeterogeneousElements : public FiddleNodesTargets {
public:
  FiddleHeterogeneousElements(double);
};

class FiddleElementsInGroup : public FiddleNodesTargets {
public:
  FiddleElementsInGroup(char*);
};

//class FiddleNodesMovePosition {};

// class AnnealMovePosition : public FiddleNodesMovePosition {
// public:
//   AnnealMovePosition(double d);
// };

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FiddleNodes : public CSkeletonModifier {
public:
  int getNok();
  int getNbad();
  double getDeltaE();
  double getTotalE();
  void coreProcess(CDeputySkeleton *skeleton);
  CSkelModCriterion *getCriterion();
  FiddleNodesTargets *getTargets();
};

class Anneal : public FiddleNodes {
public:
  Anneal(FiddleNodesTargets *trgts, CSkelModCriterion *crtrn, double t,
	 double d);
};

class Smooth : public FiddleNodes {
public:
  Smooth(FiddleNodesTargets *trgts, CSkelModCriterion *crtrn, double t);
};

class SurfaceSmooth : public FiddleNodes {
public:
  SurfaceSmooth(CSkelModCriterion *crtrn, double t, double g);
};

#endif
