// -*- C++ -*-
// $RCSfile: csnaprefine.h,v $
// $Revision: 1.1.4.6 $
// $Author: langer $
// $Date: 2014/12/14 01:07:52 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CSNAPREFINE_H
#define CSNAPREFINE_H

#include "engine/cskeleton2_i.h"
#include "engine/crefine.h"

class SnapRefine : public Refine {
protected:
  double min_distance, min_delta2;

public:
  SnapRefine(RefinementTargets *trgts, RefinementCriterion *crtrn,
	     double min, double a) 
    : Refine(trgts,crtrn,a)
  {
    min_distance = min;
  }
  ~SnapRefine() {}
  virtual void getElementSignatures(CSkeletonBase *skeleton,
				    CSkeleton *newSkeleton,
				    ElementSignatureVector &elements);
  virtual CSkeletonNodeVector *getNewEdgeNodes(CSkeletonNode*, CSkeletonNode*,
					       CSkeleton*);

};

#endif	// CSNAPREFINE_H
