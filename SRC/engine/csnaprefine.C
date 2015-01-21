// -*- C++ -*-
// $RCSfile: csnaprefine.C,v $
// $Revision: 1.1.4.25 $
// $Author: langer $
// $Date: 2014/12/14 22:49:18 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/IO/oofcerr.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/random.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonnode2.h"
#include "engine/csnaprefine.h"
#include <vtkMath.h>

#include <algorithm>

void SnapRefine::getElementSignatures(CSkeletonBase *skeleton,
				      CSkeleton *newSkeleton,
				      ElementSignatureVector &elements) 
{
  ElementSignatureVector nondeadlockable;
  Coord size = newSkeleton->getMicrostructure()->sizeOfPixels();
  min_delta2 = min_distance*std::max(std::max(size[0],size[1]),size[2]);
  min_delta2 *= min_delta2;

  for(int j=0; j<skeleton->nelements(); ++j) {
    RefinementSignature sig0;
    RefinementSignature *sig1 = new RefinementSignature;
    targets->signature(skeleton->getElement(j),&sig0);
    for(RefinementSignature::size_type i=0; i<sig0.size(); ++i) {
      CSkeletonNodeVector *newEdgeNodes = getNewEdgeNodes(
		skeleton->getElement(j)->getSegmentNode(sig0[i].first,0), 
		skeleton->getElement(j)->getSegmentNode(sig0[i].first,1),
		newSkeleton);
      if(!newEdgeNodes->empty())
	sig1->push_back(sig0[i]);
    }
    RefinementSignatureSet::iterator it = deadlockableSignatures.find(*sig1);
    if(it!=deadlockableSignatures.end()) 
      elements.push_back(ElementSignature(skeleton->getElement(j),sig1));
    else
      nondeadlockable.push_back(ElementSignature(skeleton->getElement(j),sig1));
  }
  OOFRandomNumberGenerator r;
  oofshuffle(elements.begin(), elements.end(), r);
  oofshuffle(nondeadlockable.begin(), nondeadlockable.end(), r);
  for(ElementSignatureVector::size_type j=0; j<nondeadlockable.size(); ++j) 
    elements.push_back(nondeadlockable[j]);
}

CSkeletonNodeVector *SnapRefine::getNewEdgeNodes(CSkeletonNode *n1,
						 CSkeletonNode *n2,
						 CSkeleton *newSkeleton)
{
  bool verbose = false; // n1->getUid() == 577 && n2->getUid() == 373;
  if(verbose)
    oofcerr << "SnapRefine::getNewEdgeNodes: n1=" << n1->getUid()
	    << " n2=" << n2->getUid() << std::endl;

  CSkeletonNodeVector *nodes;
  CSkeletonMultiNodeKey h(n1,n2);
  NewEdgeNodes::iterator it = newEdgeNodes.find(h);
  if(it != newEdgeNodes.end()) {
    // TODO MER: reverse in 2d?
    return (*it).second;
  }
  else {
    nodes = new CSkeletonNodeVector;
    double dist12;
    double dist22;
    Coord p1 = n1->position();
    Coord p2 = n2->position();
    Coord c0(p1);
    Coord c1(p2);
    Coord *point = new Coord();
    // TODO 3.1: old snapnodes did some dance with finding various
    // possible transitions points. We might want to incorporate that
    // idea here too.
    bool istp = newSkeleton->getMicrostructure()->transitionPoint(c0,c1,point,
								  verbose);
    if(istp) {      
      dist12 = norm2(*point - p1);
      dist22 = norm2(*point - p2);
      if(dist12 > min_delta2 && dist22 > min_delta2) {
	nodes->push_back(newSkeleton->addNode(point->xpointer()));
      }
    }
    delete point;
    // TODO 3.1: periodic cases
    newEdgeNodes.insert(NewEdgeNodeDatum(h,nodes));
  }
  return nodes;
}
