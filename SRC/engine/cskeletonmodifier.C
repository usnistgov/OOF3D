// -*- C++ -*-
// $RCSfile: cskeletonmodifier.C,v $
// $Revision: 1.1.4.27 $
// $Author: langer $
// $Date: 2014/12/14 22:49:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/cdebug.h"
#include "common/coord.h"
#include "common/printvec.h"
#include "common/tostring.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonmodifier.h"

CSkeletonElementVector& AllElements::getTargets(CSkeletonBase *skeleton) {
  elements.clear();
  elements.insert(elements.begin(), skeleton->beginElements(),
		  skeleton->endElements());
  return elements;
}

// TODO OPT: would be nice if we could just get the data from the tracker.
CSkeletonElementVector &SelectedElements::getTargets(CSkeletonBase *skeleton) {
  elements.clear();
  for(CSkeletonElementIterator elit = skeleton->beginElements();
      elit != skeleton->endElements(); ++elit) {
    if((*elit)->last_parent() != NULL) {
      if((*elit)->last_parent()->isSelected()) {
	elements.push_back((*elit));
      }
    }
  }
  return elements;
}


CSkeletonElementVector &BadlyShapedElements::getTargets(
						CSkeletonBase *skeleton)
{
  elements.clear();
  int count=0;
  for(CSkeletonElementIterator elit = skeleton->beginElements();
      elit != skeleton->endElements(); ++elit, ++count) {
    if((*elit)->energyShape() > threshold)
      elements.push_back((*elit));
  }
  return elements;
}

CSkeletonElementVector& SuspectElements::getTargets(CSkeletonBase *skeleton) {
  elements.clear();
  int count=0;
  for(CSkeletonElementIterator elit = skeleton->beginElements();
      elit != skeleton->endElements(); ++elit, ++count) {
    if((*elit)->suspect())
      elements.push_back((*elit));
  }
  return elements;
}

// TODO 3.1: Fill this in, and uncomment the LimitedAverageEnergy and
// LimitedUnconditional registrations in cskeletonmodifier.spy.

bool LimitedSkelModCriterion::withinTheLimit(ProvisionalChangesBase *change,
					     CSkeletonBase *skeleton) const
{
//         homog_before = {}
//         homog_after = {}
//         shape_before = {}
//         shape_after = {}
//         for el in change.elBefore():
//             homog_before[el] = el.homogeneity(skel.MS)
//             shape_before[el] = el.energyShape()
//         change.makeNodeMove(skel)
//         for el in change.elAfter():
//             key = el.getPositionHash()
//             try:
//                 homogeneity = skel.cachedHomogeneities[key]
//                 el.setHomogeneityData(homogeneity)
//             except KeyError:
//                 homogeneity = el.getHomogeneityData()
//                 skel.cachedHomogeneities[key] = homogeneity            
//             homog_after[el] = el.homogeneity(skel.MS)
//             shape_after[el] = el.energyShape()
//         change.moveNodeBack(skel)
//         // In parallel-mode, changes from other processes also need
//         // to be considered.
//         if parallel_enable.enabled():
//             for i, h0,h1, s0,s1 in zip(range(len(change.parallelHomog0)),
//                                        change.parallelHomog0,
//                                        change.parallelHomog1,
//                                        change.parallelShape0,
//                                        change.parallelShape1):
//                 homog_before[i] = h0
//                 homog_after[i] = h1
//                 shape_before[i] = s0
//                 shape_after[i] = s1
                
//         for el in homog_after.keys():
//             if homog_after[el] < self.homogeneity:
//                 try:
//                     if homog_before[el] > homog_after[el]:
//                         self._hopeless = 1
//                         return 0
//                 except KeyError:
//                     self._hopeless = 1
//                     return 0
//             if shape_after[el] > self.shape_energy:
//                 try:
//                     if shape_before[el] < shape_after[el]:
//                         self._hopeless = 1
//                         return 0
//                 except KeyError:
//                     self._hopeless = 1
//                     return 0
//         return 1
  return true;
}

ProvisionalChangesBase* AverageEnergy::getBestChange(
					     ProvisionalChangesVector *changes,
					     CSkeletonBase *skeleton)
{
  double bestE = 0.0;
  ProvisionalChangesBase *bestchange = NULL;
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit)
    {
      if(*pcvit && !(*pcvit)->illegal()) {
	double diff = (*pcvit)->deltaE(alpha);
	if(diff <= bestE) {
	  bestchange = *pcvit;
	  bestE = diff;
	}
      }
    }
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit) 
    {
      if(*pcvit && *pcvit != bestchange) 
	(*pcvit)->removeAddedNodes();
      // There's no need to clean up faces and segments here, since
      // CSkeleton::cleanUp will do that.  Is it even necessary to
      // clean up the nodes here?
    }
  return bestchange;
}

bool AverageEnergy::isChangeGood(ProvisionalChangesBase *change,
				 CSkeletonBase *skeleton) const 
{
  return change && !change->illegal() && change->deltaE(alpha) <= 0.0;
}

ProvisionalChangesBase* Unconditional::getBestChange(
					     ProvisionalChangesVector *changes,
					     CSkeletonBase *skeleton)
{
  double bestE = 0.0;
  ProvisionalChangesBase *bestchange = NULL;  
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit) 
    {
      if(*pcvit && !(*pcvit)->illegal()) {
	double diff = (*pcvit)->deltaE(alpha);
	if(!bestchange || diff <= bestE) {
	  bestchange = *pcvit;
	  bestE = diff;
	}
      }
    }
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit) 
    {
      if((*pcvit) != NULL && (*pcvit) != bestchange) 
	(*pcvit)->removeAddedNodes();
    }
  return bestchange;
}


bool Unconditional::isChangeGood(ProvisionalChangesBase *change,
				 CSkeletonBase *skeleton) 
  const
{
  return change && !change->illegal();
}

ProvisionalChangesBase* LimitedAverageEnergy::getBestChange(
					    ProvisionalChangesVector *changes, 
					    CSkeletonBase *skeleton)
{
  double bestE = 0.0;
  ProvisionalChangesBase *bestchange = 0;
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit) 
    {
      if(*pcvit && !(*pcvit)->illegal() && withinTheLimit(*pcvit, skeleton)) {
	double diff = (*pcvit)->deltaE(alpha);
	if(diff<=bestE) {
	  bestchange = (*pcvit);
	  bestE = diff;
	}
      }
    }
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit) 
    {
      if(*pcvit && *pcvit != bestchange) 
	(*pcvit)->removeAddedNodes();
    }
  return bestchange;
}

bool LimitedAverageEnergy::isChangeGood(ProvisionalChangesBase *change,
					CSkeletonBase *skeleton) const 
{
  return (change &&
	  !change->illegal() &&
	  withinTheLimit(change, skeleton) &&
	  change->deltaE(alpha) <= 0.0);
}

ProvisionalChangesBase* LimitedUnconditional::getBestChange(
					    ProvisionalChangesVector *changes, 
					    CSkeletonBase *skeleton)
{
  double bestE = 0.0;
  ProvisionalChangesBase *bestchange = 0;  
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit) 
    {
      if(*pcvit && !(*pcvit)->illegal() && withinTheLimit(*pcvit, skeleton)) {
	double diff = (*pcvit)->deltaE(alpha);
	if(!bestchange || diff <= bestE) {
	  bestchange = *pcvit;
	  bestE = diff;
	}
      }
    }
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit != changes->end(); ++pcvit) 
    {
      if(*pcvit && *pcvit != bestchange) 
	(*pcvit)->removeAddedNodes();
    }
  return bestchange;
}


bool LimitedUnconditional::isChangeGood(ProvisionalChangesBase *change,
					CSkeletonBase *skeleton)
  const
{
  return change && !change->illegal() && withinTheLimit(change, skeleton);
}
