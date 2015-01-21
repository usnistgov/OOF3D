// -*- C++ -*-
// $RCSfile: cfiddlenodes.C,v $
// $Revision: 1.1.4.35 $
// $Author: langer $
// $Date: 2014/12/14 22:49:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/random.h"
#include "common/progress.h"
#include "common/tostring.h"
#include "engine/cfiddlenodes.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include <algorithm>

// ----------------------- Targets ------------------------

CSkeletonNodeVector* AllNodes::getNodes(CSkeletonBase *skeleton) {
  if(nodes==NULL) {
    nodes = new CSkeletonNodeVector;
    for(CSkeletonNodeIterator nodeit = skeleton->beginNodes();
	nodeit != skeleton->endNodes(); ++nodeit)
      {
	if((*nodeit)->active(skeleton) && (*nodeit)->movable())
	  nodes->push_back((*nodeit));
      }
  }
  return nodes;
}

CSkeletonNodeVector* SelectedNodes::getNodes(CSkeletonBase *skeleton) {
  if(nodes==NULL) {
    nodes = new CSkeletonNodeVector;
    for(CSkeletonNodeIterator nodeit = skeleton->beginNodes();
	nodeit != skeleton->endNodes(); ++nodeit)
      {
	if((*nodeit)->active(skeleton) &&
	   (*nodeit)->movable() && (*nodeit)->isSelected())
	  {
	    nodes->push_back((*nodeit));
	  }
      }
  }
  return nodes;
}

CSkeletonNodeVector* NodesInGroup::getNodes(CSkeletonBase *skeleton) {
  if(nodes==NULL) {
    nodes = new CSkeletonNodeVector;
    for(CSkeletonNodeIterator nodeit = skeleton->beginNodes();
	nodeit != skeleton->endNodes(); ++nodeit)
      {
	if((*nodeit)->active(skeleton) &&
	   (*nodeit)->movable() && (*nodeit)->is_in_group(group))
	  {
	    nodes->push_back((*nodeit));
	  }
      }
  }
  return nodes;
}

CSkeletonNodeVector* InternalBoundaryNodes::getNodes(CSkeletonBase *skeleton) {
  if(nodes==NULL) 
    nodes = new CSkeletonNodeVector;
  nodes->clear();
  skeleton->getInternalBoundaryNodes(nodeSet);
  nodes->insert(nodes->begin(), nodeSet.begin(), nodeSet.end());
  return nodes;
}

CSkeletonNodeVector* FiddleSelectedElements::getNodes(CSkeletonBase *skeleton) {
  if(nodes==NULL) {
    nodes = new CSkeletonNodeVector;
    // use a set to make sure the nodes are unique
    CSkeletonNodeSet nodeSet;
    for(CSkeletonElementIterator elit = skeleton->beginElements();
	elit != skeleton->endElements(); ++elit) {
      if((*elit)->active(skeleton) && (*elit)->isSelected()) {
	for(CSkeletonNodeIterator nodeit = (*elit)->getNodes()->begin();
	    nodeit != (*elit)->getNodes()->end(); ++nodeit) 
	  {
	    if((*nodeit)->movable()) nodeSet.insert((*nodeit));
	  }
      }
    }
    // copy the set into the vector
    for(CSkeletonNodeSet::iterator nodeit = nodeSet.begin(); 
	nodeit != nodeSet.end(); ++nodeit) 
      {
	nodes->push_back((*nodeit));
      }
  }
  return nodes;
}

CSkeletonNodeVector* FiddleHeterogeneousElements::getNodes(
						   CSkeletonBase *skeleton) 
{
  if(nodes==NULL) {
    nodes = new CSkeletonNodeVector;
    // use a set to make sure the nodes are unique
    CSkeletonNodeSet nodeSet;
    for(CSkeletonElementIterator elit = skeleton->beginElements();
	elit != skeleton->endElements(); ++elit) {
      if((*elit)->active(skeleton) &&
	 (*elit)->homogeneity(skeleton->getMicrostructure()) < threshold)
	{
	  for(CSkeletonNodeIterator nodeit = (*elit)->getNodes()->begin();
	      nodeit != (*elit)->getNodes()->end(); ++nodeit)
	    {
	      if((*nodeit)->movable()) nodeSet.insert((*nodeit));
	    }
	}
    }
    // copy the set into the vector
    for(CSkeletonNodeSet::iterator nodeit = nodeSet.begin(); 
	nodeit != nodeSet.end(); ++nodeit)
      { 
	nodes->push_back((*nodeit));
      }
  }
  return nodes;
}


CSkeletonNodeVector* FiddleElementsInGroup::getNodes(CSkeletonBase *skeleton) {
  if(nodes==NULL) {
    nodes = new CSkeletonNodeVector;
    // use a set to make sure the nodes are unique
    CSkeletonNodeSet nodeSet;
    for(CSkeletonElementIterator elit = skeleton->beginElements();
	elit != skeleton->endElements(); ++elit)
      {
	if((*elit)->active(skeleton) && (*elit)->is_in_group(group)) {
	  for(CSkeletonNodeIterator nodeit = (*elit)->getNodes()->begin();
	      nodeit != (*elit)->getNodes()->end(); ++nodeit) 
	    {
	      if((*nodeit)->movable()) nodeSet.insert((*nodeit));
	    }
	}
      }
    // copy the set into the vector
    for(CSkeletonNodeSet::iterator nodeit = nodeSet.begin(); 
	nodeit != nodeSet.end(); ++nodeit) 
      {
	nodes->push_back((*nodeit));
      }
  }
  return nodes;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FiddleNodes::FiddleNodes(FiddleNodesTargets *trgts, CSkelModCriterion *crtrn,
			 double t)
  : targets(trgts),
    criterion(crtrn),
    T(t),
    nok(0), nbad(0),
    deltaE(0.0),
    totalE(0.0)
{}

FiddleNodes::~FiddleNodes() {}

CSkeletonBase* FiddleNodes::apply(CSkeletonBase *skeleton) {
  CSkeletonBase *copy = skeleton->deputyCopy();
  return copy;
}


void FiddleNodes::coreProcess(CDeputySkeleton *skeleton) {
  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("Moving nodes", DEFINITE));
  totalE = skeleton->energyTotal(criterion->getAlpha());
  nok = 0;
  nbad = 0;
  deltaE = 0.0;
  CSkeletonNodeVector *activenodes = targets->getNodes(skeleton);
  OOFRandomNumberGenerator r;
  oofshuffle(activenodes->begin(), activenodes->end(), r);

  for(unsigned int i = 0; i<activenodes->size() && !progress->stopped(); ++i) {
    DeputyProvisionalChanges change(skeleton, "fiddlenodes");
    Coord x = getPosition(skeleton, (*activenodes)[i]);
    change.moveNode((*activenodes)[i], x);
    if(criterion->isChangeGood(&change, skeleton)) {
      ++nok;
      deltaE += change.deltaE(criterion->getAlpha());
      change.accept();
    }
    else if(T>0.0 && !change.illegal() && !criterion->hopeless()) {
      double diffE = change.deltaE(criterion->getAlpha());
      if(exp(-diffE/T) > rndm()) {
	++nok;
	deltaE += diffE;
	change.accept();
      }
      else ++nbad;
    }
    else ++nbad;   
    progress->setFraction(float(i)/activenodes->size());
    progress->setMessage(to_string(i) + "/" + to_string(activenodes->size()));
  }
  progress->finish();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Anneal::Anneal(FiddleNodesTargets *trgts, CSkelModCriterion *crtrn, double t,
	       double d) 
  : FiddleNodes(trgts, crtrn, t),
    delta(d)
{}

Coord Anneal::getPosition(const CDeputySkeleton *skeleton,
			  const CSkeletonNode *node) 
  const
{
  Coord x = node->position();
  Coord pxlsize = skeleton->getMicrostructure()->sizeOfPixels();
  x[0] += delta*pxlsize[0]*gasdev();
  x[1] += delta*pxlsize[1]*gasdev();
  x[2] += delta*pxlsize[2]*gasdev();
  return x;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Smooth::Smooth(FiddleNodesTargets *trgts, CSkelModCriterion *crtrn, double t)
  : FiddleNodes(trgts, crtrn, t)
{}

Coord Smooth::getPosition(const CDeputySkeleton *skeleton,
			  const CSkeletonNode *node)
  const
{
  return skeleton->averageNeighborPosition(node);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SurfaceSmooth::SurfaceSmooth(CSkelModCriterion *crtrn, double t, double g)
  : FiddleNodes(new InternalBoundaryNodes, crtrn, t),
    gamma(g)
{}

Coord SurfaceSmooth::getPosition(const CDeputySkeleton *skeleton, 
				 const CSkeletonNode *node)
  const
{
  // Get the set of neighboring nodes for which the segment joining
  // the target node and the neighbor lies along an internal skeleton
  // boundary, meaning that the segment contains elements of more than
  // one dominant pixel type.
  CSkeletonNodeSet neighborNodes;
  CSkeletonSegmentSet segs;
  skeleton->getNodeSegments(node, segs);
  for(CSkeletonSegmentSet::iterator s=segs.begin(); s!=segs.end(); ++s) {
    CSkeletonElementVector els;
    skeleton->getSegmentElements(*s, els);
    if(!els.empty()) {
      int cat1 = els[0]->dominantPixel(skeleton->getMicrostructure());
      for(unsigned int i=1; i<els.size(); ++i) {
	int cat2 = els[i]->dominantPixel(skeleton->getMicrostructure());
	if(cat1!=cat2 && cat1!=UNKNOWN_CATEGORY && cat2!=UNKNOWN_CATEGORY) {
	  neighborNodes.insert((*s)->get_other_node(node));
	  break;
	}
      }
    }
  }
  
  // If neighborNodes is empty, averageNeighborPosition just returns
  // the position of node.
  Coord z = skeleton->averageNeighborPosition(node, neighborNodes);
  Coord y = node->position();
  return y + gamma*(z - y);
}



