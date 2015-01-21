// -*- C++ -*-
// $RCSfile: fixillegal.C,v $
// $Revision: 1.1.2.11 $
// $Author: fyc $
// $Date: 2015/01/07 15:53:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "engine/fixillegal.h"
#include "engine/cfiddlenodes.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonnode2.h"

#include <algorithm>

CSkeletonBase* FixIllegal::apply(CSkeletonBase *skeleton) {

  CDeputySkeleton *newSkeleton = skeleton->deputyCopy();
  newSkeleton->activate();

  CSkeletonElementVector baddies;
  newSkeleton->getIllegalElements(baddies);
  CSkeletonElementSet bad_set;
  bad_set.insert(baddies.begin(), baddies.end());
  oofshuffle(baddies.begin(), baddies.end(), rand);

  // arbitrary number just to keep us out of an infinite loop
  int max = 222; 
  int count = 0;
  nguilty = baddies.size();

  while(bad_set.size() and count<max) {
    ++count;
    smoothIllegalElements(newSkeleton, bad_set, baddies);
  }
  ndone = nguilty - bad_set.size();

  // TODO 3.1: There are cases in which this doesn't work, that could be
  // solved by moving a node *towards* the average position of its
  // neighbors, but not all the way.  Try moving problem nodes until
  // their elements become barely legal.
  // We will hold on to this untill we find a use case with which we think
  // it is necessary
 
  newSkeleton->cleanUp();
  newSkeleton->checkIllegality();
  
  return newSkeleton;

}

void FixIllegal::smoothIllegalElements(CDeputySkeleton *newSkeleton, 
				       CSkeletonElementSet &bad_set, 
				       CSkeletonElementVector &baddies)
{
  std::vector<int> node_indices;
  for(CSkeletonElementIterator it=baddies.begin(); it!=baddies.end(); ++it) {
    node_indices.clear();
    for(unsigned int i=0; i<(*it)->getNumberOfNodes(); ++i)
      node_indices.push_back(i);
    oofshuffle(node_indices.begin(), node_indices.end(), rand);
    for(unsigned int i=0; i<node_indices.size(); ++i)
      smoothTheNode(newSkeleton, (*it)->getNode(node_indices[i]),
		    bad_set, baddies);
  }
}

void FixIllegal::smoothTheNode(CDeputySkeleton *newSkeleton,
			       CSkeletonNode *node,
			       CSkeletonElementSet &bad_set, 
			       CSkeletonElementVector &baddies)
{
  int n_local_guilty = 0;
  CSkeletonElementVector *neighborElements = node->getElements();
  for(CSkeletonElementIterator it=neighborElements->begin();
      it!=neighborElements->end(); ++it)
    {
      if(bad_set.count((*it)))
	++n_local_guilty;
    }

  // Move node to its average position WRT its neighbor nodes
  // The TODO 3.1 idea is to setup a coefficient alpha that will be reduced to the
  // maximum by moving the node slowly from its position to the average one when
  // the average position is not suitable (1-alpha) AveragePosition + CurrentPosition
  newSkeleton->moveNodeTo(node, newSkeleton->averageNeighborPosition(node));

  int n_still_guilty = 0;
  for(CSkeletonElementIterator it=neighborElements->begin();
      it!=neighborElements->end(); ++it)
    {
      if((*it)->illegal())
	++n_still_guilty;
    }

  if(n_local_guilty <= n_still_guilty)
    newSkeleton->moveNodeBack(node);
  else {
    for(CSkeletonElementIterator it=neighborElements->begin();
	it!=neighborElements->end(); ++it) 
      {
	bool estillguilty = (*it)->illegal();
	bool ewasguilty = bad_set.count((*it));
	if(ewasguilty and !estillguilty)
	  bad_set.erase(*it);
	else if(estillguilty and !ewasguilty) {
	  baddies.push_back(*it);
	  bad_set.insert(*it);
	}
      }
  }
}
