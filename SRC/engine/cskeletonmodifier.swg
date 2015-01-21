// -*- C++ -*-
// $RCSfile: cskeletonmodifier.swg,v $
// $Revision: 1.1.4.10 $
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

#ifndef CSKELETONMODIFIER_SWG
#define CSKELETONMODIFIER_SWG

%module cskeletonmodifier

%include "common/typemaps.swg"
%include "engine/typemaps.swg"
%extern "engine/cskeleton2.swg"
%{
#include <oofconfig.h>
#include "engine/cskeletonmodifier.h"
#include "engine/cskeleton2.h"
%}

%pragma(python) include="engine/cskeletonmodifier.spy"
%pragma(python) code="from ooflib.SWIG.engine.cskeleton2 import CSkeletonBasePtr"

class CSkelModTargets {
  
};

class AllElements : public CSkelModTargets {
public:
  AllElements();
};

class SelectedElements : public CSkelModTargets {
public:
  SelectedElements();
};

class BadlyShapedElements : public CSkelModTargets {
public:
  BadlyShapedElements(double th);
};

class SuspectElements : public CSkelModTargets {
public:
  SuspectElements();
};

class CSkelModCriterion {
public:
  double getAlpha();

};

class AverageEnergy : public CSkelModCriterion {
public:
  AverageEnergy(double a);
};

class Unconditional : public CSkelModCriterion {
public:
  Unconditional(double a);
};

class LimitedAverageEnergy : public CSkelModCriterion {
public:
  LimitedAverageEnergy(double a, double h, double s);
};

class LimitedUnconditional : public CSkelModCriterion {
public:
  LimitedUnconditional(double a, double h, double s);
};

// Skeleton modifiers defined in Python should be derived from
// CSkeletonModifierBase, and must provide an apply() method in
// Python.

class CSkeletonModifierBase {
public:
  CSkeletonModifierBase();
  ~CSkeletonModifierBase();
  char *get_progressbar_type();
  void postProcess(PyObject*);
  void cleanUp();
};

// Skeleton modifiers defined in C++ are derived from
// CSkeletonModifier.  Its constructor is *not* swigged, because
// CSkeletonModifier::apply is a pure virtual function.

class CSkeletonModifier : public CSkeletonModifierBase {
public:
  CSkeletonBase *apply(CSkeletonBase*);
};



#endif
