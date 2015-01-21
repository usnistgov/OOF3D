// -*- C++ -*-
// $RCSfile: cskeletonmodifier.h,v $
// $Revision: 1.1.4.14 $
// $Author: langer $
// $Date: 2014/12/14 01:07:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CSKELETONMODIFIER_H
#define CSKELETONMODIFIER_H

#include "engine/cskeleton2_i.h"
#include "engine/cskeletonselectable_i.h"

/******************************************************

                     TARGETS

*******************************************************/

class CSkelModTargets {
protected:
  CSkeletonElementVector elements;
public:
  CSkelModTargets() {}
  virtual ~CSkelModTargets() {}
  virtual CSkeletonElementVector &getTargets(CSkeletonBase *skeleton) = 0;
};

class AllElements : public CSkelModTargets {
public:
  AllElements() {}
  virtual ~AllElements() {}
  virtual CSkeletonElementVector &getTargets(CSkeletonBase *skeleton);
};

class SelectedElements : public CSkelModTargets {
public:
  SelectedElements() {}
  virtual ~SelectedElements() {}
  virtual CSkeletonElementVector &getTargets(CSkeletonBase *skeleton);
};

// class HeterogenousElements : public CSkelModTargets {
// private:
//   double threshold;
// public:
//   HeterogenousElements(double th = 0.9) {threshold = th;};
//   virtual ~HeterogenousElements() {};
//   const CSkeletonElementVector *getTargets(CSkeletonBase *skeleton);
// };

class BadlyShapedElements : public CSkelModTargets {
private:
  double threshold;
public:
  BadlyShapedElements(double th = 0.4) : threshold(th) {}
  virtual ~BadlyShapedElements() {}
  virtual CSkeletonElementVector &getTargets(CSkeletonBase *skeleton);
};

class SuspectElements : public CSkelModTargets {
public:
  SuspectElements() {}
  virtual ~SuspectElements() {}
  virtual CSkeletonElementVector &getTargets(CSkeletonBase *skeleton);
};

// class ElementsInGroup : public CSkelModTargets {
// private:
//   CSkeletonGroup *group;
// public:
//   ElementsInGroup(CSkeletonGroup *grp) {group = grp;};
//   virtual ~ElementsInGroup() {};
//   const CSkeletonElementVector *getTargets(CSkeletonBase *skeleton);
// };

/******************************************************

                     CRITERIA

*******************************************************/

class CSkelModCriterion {
protected:
  double alpha;
public:
  CSkelModCriterion(double a) : alpha(a) {}
  virtual ~CSkelModCriterion() {}
  virtual ProvisionalChangesBase* getBestChange(ProvisionalChangesVector*,
						CSkeletonBase*) = 0;
  virtual bool isChangeGood(ProvisionalChangesBase*, CSkeletonBase*) const = 0;
  bool hopeless() { return false; }
  double getAlpha() { return alpha; }
};

class LimitedSkelModCriterion : public CSkelModCriterion {
protected:
  bool hopeless_;
  double homogeneity;
  double shape_energy;
public:
  LimitedSkelModCriterion(double a, double h, double s)
    : CSkelModCriterion(a),
      hopeless_(false),
      homogeneity(h),
      shape_energy(s)
  {}
  bool withinTheLimit(ProvisionalChangesBase*, CSkeletonBase*) const;
  bool hopeless() { return hopeless_; }
};

class AverageEnergy : public CSkelModCriterion {
public:
  AverageEnergy(double a) : CSkelModCriterion(a) {}
  virtual ProvisionalChangesBase* getBestChange(ProvisionalChangesVector*,
						CSkeletonBase*);
  virtual bool isChangeGood(ProvisionalChangesBase*, CSkeletonBase*) const;
};

class Unconditional : public CSkelModCriterion {
public:
  Unconditional(double a) : CSkelModCriterion(a) {}
  virtual ProvisionalChangesBase* getBestChange(ProvisionalChangesVector*,
						CSkeletonBase*);
  virtual bool isChangeGood(ProvisionalChangesBase*, CSkeletonBase*) const;
};

class LimitedAverageEnergy : public LimitedSkelModCriterion {
public:
  LimitedAverageEnergy(double a, double h, double s) 
    : LimitedSkelModCriterion(a, h, s)
  {}
  virtual ProvisionalChangesBase* getBestChange(ProvisionalChangesVector*,
						CSkeletonBase*);
  virtual bool isChangeGood(ProvisionalChangesBase*, CSkeletonBase*) const;
};

class LimitedUnconditional : public LimitedSkelModCriterion {
public:
  LimitedUnconditional(double a, double h, double s) 
    : LimitedSkelModCriterion(a, h, s)
  {}
  virtual ProvisionalChangesBase* getBestChange(ProvisionalChangesVector*,
						CSkeletonBase*);
  virtual bool isChangeGood(ProvisionalChangesBase*, CSkeletonBase*) const;
}; 

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Skeleton modifiers written in C++ should be derived from
// CSkeletonModifier and must redefine apply().  CSkeletonModifierBase
// is swigged and CRegistered.  It *doesn't* have a pure virtual C++
// apply() method, so it can be used as a base for a Python derived
// class (which must define apply() in Python).  NOTE that because
// CSkeletonModifierBase is the base class, it's the one that should
// be specified in the Registrations of the derived classes.

class CSkeletonModifierBase {
public:
  CSkeletonModifierBase() {}
  virtual ~CSkeletonModifierBase() {}
  virtual const char *get_progressbar_type() { return "continuous"; }
  virtual void postProcess(PyObject*) {}
  // cleanUp should be redefined if the modifier has allocated memory
  // and needs to free it when it's done.  It's not sufficient to
  // release the memory in the destructor, because the modifier may be
  // being stored in the GUI's historian, and not destroyed until much
  // later.
  virtual void cleanUp() {}
};

class CSkeletonModifier : public CSkeletonModifierBase {
public:
  virtual CSkeletonBase *apply(CSkeletonBase *skeleton) = 0;
};

				
#endif
