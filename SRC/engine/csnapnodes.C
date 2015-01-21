// -*- C++ -*-
// $RCSfile: csnapnodes.C,v $
// $Revision: 1.1.4.32 $
// $Author: langer $
// $Date: 2014/12/14 22:49:17 $

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
#include "common/progress.h"
#include "common/random.h"
#include "common/tostring.h"
#include "engine/canonicalorder.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/csnapnodes.h"

#include <algorithm>

// TODO: Try a Segment-based method instead of an Element-based
// method.  That is, loop over Segments instead of Elements.  For both
// Nodes in a Segment, find the possible transition points on *all*
// Segments that contain each Node (picking the closest one if there
// are multiple transition points on a Segment).  Then examine all
// possible pair-wise moves of the two nodes, as well as the single
// node moves.

// The proposed method can do something that the current algorithm
// can't, namely aligning a Segment that crosses a material boundary
// to the boundary in one step.  The current algorithm can only align
// such as segment in two steps, because the transition points are in
// different elements.  If the intermediate configuration has a high
// energy, the alignment won't occur.

CSkeletonElementVector* SnapAll::getElements(CSkeletonBase *skeleton) {
  if(elements==NULL) {
    elements = new CSkeletonElementVector;
    for(CSkeletonElementIterator elit = skeleton->beginElements();
	elit != skeleton->endElements(); ++elit) {
      elements->push_back(*elit);
    }
  }
  return elements;
}

CSkeletonElementVector* SnapSelected::getElements(CSkeletonBase *skeleton) {
  if(elements==NULL) {
    elements = new CSkeletonElementVector;
  }
  elements->clear();
  for(CSkeletonElementIterator elit = skeleton->beginElements();
      elit != skeleton->endElements(); ++elit) {
    if((*elit)->isSelected())
      elements->push_back(*elit);
  }
  return elements;
}

CSkeletonElementVector* SnapHeterogenous::getElements(CSkeletonBase *skeleton) {
  if(elements==NULL) {
    elements = new CSkeletonElementVector;
  }
  elements->clear();
  for(CSkeletonElementIterator elit = skeleton->beginElements();
      elit != skeleton->endElements(); ++elit) {
    if((*elit)->homogeneity(skeleton->getMicrostructure()) < threshold)
      elements->push_back(*elit);
  }
  return elements;
}

SnapNodes::SnapNodes(SnapNodeTargets *trgts, CSkelModCriterion *crtrn) {
  targets = trgts;
  criterion = crtrn;
  if(!snapperMapperCreated)
    createSnapperMapper();
}

SnapSignature getSignature(TransitionPointVector *transitionPoints) {
  SnapSignature sig;
  for(unsigned int i=0; i<transitionPoints->size(); ++i) 
    if((*transitionPoints)[i].first) sig.push_back(i);
  return sig;
}


NodeSnapperBase *SnapNodes::getNodeSnapper(CSkeletonElement *el, 
					   TransitionPointVector *tps) 
{
  SnapSignature sig = getSignature(tps);
  SnapperMapper::iterator it = snapperMapper.find(sig);
  if(it == snapperMapper.end()) {
    //     if(!sig.empty()) {
    //       oofcerr << "no snapper for signature ";
    //       for(unsigned int i=0; i<sig.size(); ++i) oofcerr << sig[i] << " ";
    //       oofcerr << std::endl;
    //     }
    return NULL;
  }
  NodeSnapperBase *snapper = snapperMapper[sig](el, sig, tps);
  return snapper;
}

CSkeletonBase* SnapNodes::apply(CSkeletonBase *skeleton) {

  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("SnapNodes", DEFINITE));
  
  try {
    CDeputySkeleton *newSkeleton = skeleton->deputyCopy();
    newSkeleton->activate();
    CSkeletonElementVector *elements = targets->getElements(newSkeleton);
    Coord x0;
    Coord x1;
    unsigned int i;
    //int h;
    CSkeletonMultiNodeKey h;
    TransitionPointMap stored_tps;
    PrioritizedSnappers prioritizedSnappers;
    PrioritizedSnappers::iterator psi;

    // Loop over the elements to create a multimap of snapper objects
    // keyed by priority
    for(CSkeletonElementIterator it = elements->begin(); it != elements->end();
	++it)
      {
	// oofcerr << "considering element " << (*it)->getIndex() << std::endl;
    
	if( (*it)->homogeneity(skeleton->getMicrostructure()) == 1.0)
	  continue;
	// Loop over the segments to find the transition points, if
	// any. tpoints gets deleted by the snapper destructors.
	TransitionPointVector *tpoints = new TransitionPointVector(6);
	for(i = 0; i<(*it)->getNumberOfSegments(); ++i) {
	  h = CSkeletonMultiNodeKey((*it)->getSegmentNode(i,0), 
				    (*it)->getSegmentNode(i,1));
	  TransitionPointMap::iterator mapit = stored_tps.find(h);
	  if(mapit!=stored_tps.end()) {
	    // oofcerr << "found hashed version" << std::endl;
	    (*tpoints)[i] = stored_tps[h];
	  }
	  else {
	    x0 = (*it)->getSegmentNode(i,0)->position();
	    x1 = (*it)->getSegmentNode(i,1)->position();
	    Coord c0(x0);
	    Coord c1(x1);
	    Coord *point = new Coord();
	    bool istp = skeleton->getMicrostructure()->transitionPoint(
						       c0,c1, point, false);
	    if(istp) {
	      // oofcerr << "transition point " << c0 << " " << c1 << " "
	      // 	    << *point << std::endl;
	      if( point->x[0] < 0 ||
		  point->x[0] > skeleton->getMicrostructure()->size()[0] || 
		  point->x[1] < 0 ||
		  point->x[1] > skeleton->getMicrostructure()->size()[1] ||
		  point->x[2] < 0 ||
		  point->x[2] > skeleton->getMicrostructure()->size()[2])
		throw ErrProgrammingError(
		  "CSnapNodes: invalid transition point", __FILE__, __LINE__);
	    }
	    (*tpoints)[i] = TransitionPointDatum(istp,point);
	    stored_tps[h] = (*tpoints)[i];
	  }
	} // end loop over segments
	// store the snappers in a map of vectors keyed by priority
	NodeSnapperBase *snapper = getNodeSnapper(*it, tpoints);
	if(snapper != NULL) {
	  // oofcerr << "snapper priority " << snapper->get_priority() << std::endl;
	  psi = prioritizedSnappers.find(snapper->get_priority());
	  if(psi == prioritizedSnappers.end()) {
	    SnapperVector *svector = new SnapperVector;
	    svector->push_back(snapper);
	    prioritizedSnappers.insert(PrioritySnapperPair(
					   snapper->get_priority(), svector));
	  }
	  else
	    prioritizedSnappers[snapper->get_priority()]->push_back(snapper);
	}
	else
	  delete tpoints;
	progress->setFraction(float((*it)->getIndex()+1)/skeleton->nelements());
	progress->setMessage("examining elements: " +
			     to_string((*it)->getIndex()+1) + "/" +
			     to_string(skeleton->nelements()));

      }
  
    // loop over the snappers in the order of priority

    // TODO 3.1: After snapping a node, snap its neighbors if they're
    // scheduled to be snapped, recursively, before going back to the
    // list.
    IndexSet *movedNodes = new IndexSet;
    OOFRandomNumberGenerator r;
    for(psi=prioritizedSnappers.begin(); psi!=prioritizedSnappers.end(); ++psi)
      {
	oofshuffle((*psi).second->begin(), (*psi).second->end(), r);
	i = 0;
	for(SnapperVector::iterator svit = (*psi).second->begin();
	    svit != (*psi).second->end(); ++svit, ++i) 
	  {
	    (*svit)->apply(newSkeleton, criterion, movedNodes);
	    progress->setFraction(1.0*(i+1)/(*psi).second->size());
	    progress->setMessage("SnapNode Type " + to_string((*psi).first) +
				 ": " + to_string(i+1) + "/" +
				 to_string((*psi).second->size()));
	  }
      }
    numSnapped = movedNodes->size();
    
    // delete the coords that were created above after they have all been used.
    for(TransitionPointMap::iterator tpit = stored_tps.begin();
	tpit != stored_tps.end(); ++tpit)
      delete (*tpit).second.second;

    // delete the snapper vectors and snappers
    for(psi=prioritizedSnappers.begin(); psi!=prioritizedSnappers.end(); ++psi)
      {
	for(SnapperVector::iterator svit = (*psi).second->begin();
	    svit != (*psi).second->end(); ++svit) 
	  delete (*svit);
	delete (*psi).second;
      }
    delete movedNodes;
    progress->finish();
    return newSkeleton;
  }
  catch (...) {
    progress->finish();
    throw;
  }
} // SnapNodes::apply



// convenience function for creating the snapper mapper
static SnapSignature array2Signature(short a[],int size) {
  SnapSignature sig;
  for(int i=0; i<size; ++i) 
    sig.push_back(a[i]);
  return sig;
}

bool SnapNodes::snapperMapperCreated = false;
SnapperMapper SnapNodes::snapperMapper = SnapperMapper();

void SnapNodes::createSnapperMapper() {
  int i;
  
  short r1[6][1] = { {0}, {1}, {2}, {3}, {4}, {5} };
  for(i=0; i<6; ++i)
    snapperMapper.insert( SnapperMapperPair(
		     array2Signature(r1[i],1),
		     Tet1EdgeSnapper::factory) );

  short r2_1[12][2] = { {0,1},{0,2},{0,3},{0,4},{1,2},{1,4},
			{1,5},{2,3},{2,5},{3,4},{3,5},{4,5} };
  for(i=0; i<12; ++i)
    snapperMapper.insert( SnapperMapperPair(
		    array2Signature(r2_1[i],2),
		    Tet2EdgesAdjacentSnapper::factory) );

  short r2_2[3][2] = { {0,5}, {1,3}, {2,4} };
  for(i=0; i<3; ++i) 
    snapperMapper.insert( SnapperMapperPair(
		    array2Signature(r2_2[i],2),
		    Tet2EdgesOppositeSnapper::factory) );

  short r3_1[4][3] = { {0,3,4}, {0,1,2}, {2,3,5}, {1,4,5} };
  for(i=0; i<4; ++i)
    snapperMapper.insert( SnapperMapperPair(
		    array2Signature(r3_1[i],3),
		    Tet3EdgesTriangle::factory) );

  short r3_2[12][3] = { {0,2,4}, {0,1,5}, {0,1,3}, {1,2,4}, {0,2,5}, {1,2,3}, 
			{1,3,5}, {2,3,4}, {0,4,5}, {1,3,4}, {0,3,5}, {2,4,5} };
  for(i=0; i<12; ++i) 
    snapperMapper.insert( SnapperMapperPair(
		    array2Signature(r3_2[i], 3),
		    Tet3EdgesZigZag::factory) ); 

  short r3_3[4][3] = { {3,4,5}, {0,1,4}, {0,2,3}, {1,2,5} };
  for(i=0; i<4; ++i)
    snapperMapper.insert( SnapperMapperPair( 
		    array2Signature(r3_3[i],3),
		    Tet3Edges1Node::factory) );

  short r4_1[12][4] = { {0,1,3,4}, {0,2,3,4}, {0,3,4,5}, {0,1,4,5},
			{1,2,4,5}, {1,3,4,5}, {0,2,3,5}, {1,2,3,5}, 
			{2,3,4,5}, {0,1,2,3}, {0,1,2,4}, {0,1,2,5} };
  for(i=0; i<12; ++i)
    snapperMapper.insert( SnapperMapperPair(
		    array2Signature(r4_1[i], 4),
		    Tet4Edges1::factory) ); 

  short r4_2[3][4] = { {1,2,3,4}, {0,2,4,5}, {0,1,3,5} };
  for(i=0; i<3; ++i)
    snapperMapper.insert( SnapperMapperPair(
		    array2Signature(r4_2[i], 4),
		    Tet4Edges2::factory) ); 

  snapperMapperCreated = true;
}

void NodeSnapperBase::apply(CDeputySkeleton *skeleton,
			    CSkelModCriterion *criterion, IndexSet *movedNodes)
{
  SnapMoveVector *moves = get_movelist(movedNodes);
  ProvisionalChangesVector *changes = new ProvisionalChangesVector;
  // oofcerr << "considering " << moves->size() << " moves" << std::endl;
  for(SnapMoveVector::iterator it = moves->begin(); it != moves->end(); ++it) {
    if((*it).isLegal()) {
      DeputyProvisionalChanges *change = (*it).getProvisionalChange(skeleton);
      changes->push_back(change);
    }
  }
  ProvisionalChangesBase *bestChange = criterion->getBestChange(changes,
								skeleton);
  if(bestChange != NULL) {
    bestChange->accept();
    for(MoveNodeVector::const_iterator nodeit=bestChange->getMovedNodesBegin(); 
	nodeit != bestChange->getMovedNodesEnd(); ++nodeit) 
      {
	// oofcerr << "moving node " << (*nodeit).node->getIndex() << " to ";
	// oofcerr << (*nodeit).position[0] << " " << (*nodeit).position[1]
	// 	<< " " << (*nodeit).position[2] << std::endl;
	movedNodes->insert((*nodeit).node->getIndex());
      }
  }
  for(ProvisionalChangesVector::iterator pcvit=changes->begin();
      pcvit!=changes->end(); ++pcvit)
    {
      delete *pcvit;
    }
  delete changes;
  delete moves;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SnapMove::SnapMove(CSkeletonNode *n, Coord *c) {
  snaps.push_back(SnapMoveDatum(n,c));
}

SnapMove::SnapMove(CSkeletonNode *n0, Coord *c0, CSkeletonNode *n1, Coord *c1) 
{
  snaps.push_back(SnapMoveDatum(n0,c0));
  snaps.push_back(SnapMoveDatum(n1,c1));
}

SnapMove::SnapMove(CSkeletonNode *n0, Coord *c0,
		   CSkeletonNode *n1, Coord *c1, 
		   CSkeletonNode *n2, Coord *c2)
{
  snaps.push_back(SnapMoveDatum(n0,c0));
  snaps.push_back(SnapMoveDatum(n1,c1));
  snaps.push_back(SnapMoveDatum(n2,c2));
}

SnapMove::SnapMove(CSkeletonNode *n0, Coord *c0, 
		   CSkeletonNode *n1, Coord *c1, 
		   CSkeletonNode *n2, Coord *c2,
		   CSkeletonNode *n3, Coord *c3)
{
  snaps.push_back(SnapMoveDatum(n0,c0));
  snaps.push_back(SnapMoveDatum(n1,c1));
  snaps.push_back(SnapMoveDatum(n2,c2));
  snaps.push_back(SnapMoveDatum(n3,c3));
}

bool SnapMove::isLegal() const {
  for(std::vector<SnapMoveDatum>::const_iterator it=snaps.begin(); 
      it!=snaps.end(); ++it) 
    {
      if(!(*it).first->canMoveTo((*it).second->xpointer()))
	return false;
    }
  return true;
}

DeputyProvisionalChanges *SnapMove::getProvisionalChange(
						 CDeputySkeleton *skeleton)
{
  DeputyProvisionalChanges *change = new DeputyProvisionalChanges(skeleton,
								  "snapmove"); 
  for(std::vector<SnapMoveDatum>::iterator it=snaps.begin(); it!=snaps.end();
      ++it)
    {
      change->moveNode((*it).first, *((*it).second));
    }
  return change;
}


/**********************************************************

                        SNAPPERS


***********************************************************/
template <class X>
NodeSnapperBase* NodeSnapper<X>::factory(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps) {
  X *bozo = new X(el,sig,tps);
  return bozo;
}

template <class X>
NodeSnapper<X>::~NodeSnapper() {
  for(std::vector<Coord*>::iterator it = otherPoints.begin(); 
      it != otherPoints.end(); ++it)
    delete (*it);
  delete transitionPoints;
}

SnapMoveVector *Tet1EdgeSnapper::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet1EdgeSnapper" << std::endl;
  CSkeletonNode *n0 = element->getSegmentNode(signature[0],0);
  CSkeletonNode *n1 = element->getSegmentNode(signature[0],1);
  Coord *c = (*transitionPoints)[signature[0]].second;
  if(movedNodes->count(n0->getIndex())==0) 
    moves->push_back(SnapMove(n0,c));
  if(movedNodes->count(n1->getIndex())==0)
    moves->push_back(SnapMove(n1,c));
  return moves;
}


SnapMoveVector *Tet2EdgesAdjacentSnapper::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet2EdgesAdjacentSnapper" << std::endl;
  CSkeletonNodeVector nodes(3);
  IndexVec idxs = CanonicalOrderMapper::getNodes(signature);
  for(int i=0; i<3; ++i) nodes[i] = element->getNode(idxs[i]);
  Coord *c0 = (*transitionPoints)[signature[0]].second;
  Coord *c1 = (*transitionPoints)[signature[1]].second;
  IndexSet::iterator it0, it1;
  if(movedNodes->count(nodes[0]->getIndex())==0) {
    moves->push_back(SnapMove(nodes[0],c0));
    if(movedNodes->count(nodes[2]->getIndex())==0) 
      moves->push_back(SnapMove(nodes[0], c0, nodes[2], c1));
  }
  if(movedNodes->count(nodes[1]->getIndex())==0) {
    Coord *avg = new Coord((*c0+*c1)*0.5);
    otherPoints.push_back(avg);
    moves->push_back(SnapMove(nodes[1],avg));
    moves->push_back(SnapMove(nodes[1], c0));
    moves->push_back(SnapMove(nodes[1], c1));
  }
  if(movedNodes->count(nodes[2]->getIndex())==0)
    moves->push_back(SnapMove(nodes[2], c1));
  return moves;
}


SnapMoveVector *Tet2EdgesOppositeSnapper::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet2EdgesOppositeSnapper" << std::endl;
  CSkeletonNode *n0 = element->getSegmentNode(signature[0],0);
  CSkeletonNode *n1 = element->getSegmentNode(signature[0],1);
  CSkeletonNode *n2 = element->getSegmentNode(signature[1],0);
  CSkeletonNode *n3 = element->getSegmentNode(signature[1],1);
  Coord *c0 = (*transitionPoints)[signature[0]].second;
  Coord *c1 = (*transitionPoints)[signature[1]].second;
  IndexSet::iterator it0, it1;
  if(movedNodes->count(n0->getIndex())==0) {
    moves->push_back(SnapMove(n0,c0));
    if(movedNodes->count(n2->getIndex())==0) 
      moves->push_back(SnapMove(n0,c0,n2,c1));
    if(movedNodes->count(n3->getIndex())==0) 
      moves->push_back(SnapMove(n0,c0,n3,c1));
  }
  if(movedNodes->count(n1->getIndex())==0) { 
    moves->push_back(SnapMove(n1,c0));
    if(movedNodes->count(n2->getIndex())==0) 
      moves->push_back(SnapMove(n1,c0,n2,c1));
    if(movedNodes->count(n3->getIndex())==0) 
      moves->push_back(SnapMove(n1,c0,n3,c1));
  }
  return moves;
}


SnapMoveVector *Tet3EdgesTriangle::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet3EdgesTriangle" << std::endl;
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(signature);
  CSkeletonNode *nodes[3]; 
  for(int i=0; i<3; ++i)
    nodes[i] = element->getNode(node_idxs[i]);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(signature);
  Coord *c[3];
  for(int i=0; i<3; ++i)
    c[i] = (*transitionPoints)[seg_idxs[i]].second;

  int count[3];
  for(int i=0; i<3; ++i) 
    count[i] = movedNodes->count(nodes[i]->getIndex());
  if(count[0] == 0) {
    moves->push_back(SnapMove(nodes[0], c[0]));
    moves->push_back(SnapMove(nodes[0], c[2]));
    if(count[1] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1]));
      moves->push_back(SnapMove(nodes[0], c[2], nodes[1], c[0]));
      moves->push_back(SnapMove(nodes[0], c[2], nodes[1], c[1]));
      if(count[2] == 0) {
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[2], c[2]));
	moves->push_back(SnapMove(nodes[0], c[2], nodes[1], c[0], 
				  nodes[2], c[1]));
      }
    }
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[2]));
      moves->push_back(SnapMove(nodes[0], c[2], nodes[2], c[1]));
    }
  }
  if(count[1] == 0) {
    moves->push_back(SnapMove(nodes[1], c[0]));
    moves->push_back(SnapMove(nodes[1], c[1]));
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[2]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[2], c[2]));
    }
  }
  if(count[2] == 0) {
    moves->push_back(SnapMove(nodes[2], c[1]));
    moves->push_back(SnapMove(nodes[2], c[2]));
  }

  return moves;
}



SnapMoveVector *Tet3EdgesZigZag::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet3EdgesZigZag" << std::endl;
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(signature);
  CSkeletonNode *nodes[4]; 
  for(int i=0; i<4; ++i)
    nodes[i] = element->getNode(node_idxs[i]);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(signature);
  Coord *c[3];
  for(int i=0; i<3; ++i)
    c[i] = (*transitionPoints)[seg_idxs[i]].second;

  int count[4];
  for(int i=0; i<4; ++i)
    count[i] = movedNodes->count(nodes[i]->getIndex());
  if(count[0] == 0) {
    moves->push_back(SnapMove(nodes[0], c[0]));
    if(count[1] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1]));
      if(count[2] == 0)
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[2], c[2]));
      if(count[3] == 0) 
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[3], c[2]));
    }
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[2]));
      if(count[3] == 0) 
	moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1],
				  nodes[3], c[2]));
    }
    if(count[3] == 0) 
      moves->push_back(SnapMove(nodes[0], c[0], nodes[3], c[2]));
  }
  if(count[1] == 0) {
    moves->push_back(SnapMove(nodes[1], c[0]));
    moves->push_back(SnapMove(nodes[1], c[1]));
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[2]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[2], c[2]));
    }
    if(count[3] == 0) {
      moves->push_back(SnapMove(nodes[1], c[0], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[3], c[2]));
    }
  }
  if(count[2] == 0) {
    moves->push_back(SnapMove(nodes[2], c[1]));
    moves->push_back(SnapMove(nodes[2], c[2]));
    if(count[3] == 0)
      moves->push_back(SnapMove(nodes[2], c[1], nodes[3], c[2]));
  }
  if(count[3] == 0)
    moves->push_back(SnapMove(nodes[3], c[2]));
    
  return moves;
}



SnapMoveVector *Tet3Edges1Node::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet3Edges1Node" << std::endl;
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(signature);
  CSkeletonNode *nodes[4]; 
  for(int i=0; i<4; ++i)
    nodes[i] = element->getNode(node_idxs[i]);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(signature);
  Coord *c[3];
  for(int i=0; i<3; ++i)
    c[i] = (*transitionPoints)[seg_idxs[i]].second;
  if(movedNodes->count(nodes[3]->getIndex())==0) {
    Coord *avg = new Coord((*c[0]+*c[1]+*c[2])*(1.0/3.0));
    otherPoints.push_back(avg);
    moves->push_back(SnapMove(nodes[3], avg));
    moves->push_back(SnapMove(nodes[3], c[0]));
    moves->push_back(SnapMove(nodes[3], c[1]));
    moves->push_back(SnapMove(nodes[3], c[2]));
  }
  bool cando = true;
  for(int i=0; i<3; ++i) {
    cando &= (movedNodes->count(nodes[i]->getIndex())==0);
  }
  if(cando)
    moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1], nodes[2], c[2]));
  return moves;
}


SnapMoveVector *Tet4Edges1::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet4Edges1" << std::endl;
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(signature);
  CSkeletonNode *nodes[4]; 
  for(int i=0; i<4; ++i)
    nodes[i] = element->getNode(node_idxs[i]);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(signature);
  Coord *c[4];
  for(int i=0; i<4; ++i)
    c[i] = (*transitionPoints)[seg_idxs[i]].second;

  int count[4];
  for(int i=0; i<4; ++i)
    count[i] = movedNodes->count(nodes[i]->getIndex());
  if(count[0] == 0) {
    moves->push_back(SnapMove(nodes[0], c[0]));
    if(count[1] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1]));
      moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[3]));
      if(count[2] == 0) {
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[2], c[2]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[3],
				  nodes[2], c[1]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[3],
				  nodes[2], c[2]));
	if(count[3] == 0) 
	  moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				    nodes[2], c[2], nodes[3], c[3]));
      }
      if(count[3] == 0) {
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[3], c[2]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1], 
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[3],
				  nodes[3], c[2]));
      }
    }
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[2]));
      if(count[3] == 0) {
	moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1],
				  nodes[3], c[2]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[2],
				  nodes[3], c[3]));
      }
    }
    if(count[3] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[0], c[0], nodes[3], c[3]));
    }
  }
  if(count[1] == 0) {
    moves->push_back(SnapMove(nodes[1], c[0]));
    moves->push_back(SnapMove(nodes[1], c[1]));
    moves->push_back(SnapMove(nodes[1], c[3]));
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[2]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[2], c[2]));
      moves->push_back(SnapMove(nodes[1], c[3], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[1], c[3], nodes[2], c[2]));
      if(count[3] == 0) {
	moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[1],
				  nodes[3], c[2]));
	moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[1],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[2],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[1], c[1], nodes[2], c[2],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[1], c[3], nodes[2], c[1], 
				  nodes[3], c[2]));
      }
    }
    if(count[3] == 0) {
      moves->push_back(SnapMove(nodes[1], c[0], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[1], c[0], nodes[3], c[3]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[3], c[3]));
      moves->push_back(SnapMove(nodes[1], c[3], nodes[3], c[2]));
    }
  }
  if(count[2] == 0) {
    moves->push_back(SnapMove(nodes[2], c[1]));
    moves->push_back(SnapMove(nodes[2], c[2]));
    if(count[3] == 0) {
      moves->push_back(SnapMove(nodes[2], c[1], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[2], c[1], nodes[3], c[3]));
      moves->push_back(SnapMove(nodes[2], c[2], nodes[3], c[3]));
    }
  }
  if(count[3] == 0) {
    moves->push_back(SnapMove(nodes[3], c[2]));
    moves->push_back(SnapMove(nodes[3], c[3]));
  }

  return moves;
}



SnapMoveVector *Tet4Edges2::get_movelist(IndexSet *movedNodes) {
  SnapMoveVector *moves = new SnapMoveVector;
  // oofcerr << element->getIndex() << " Tet4Edges2" << std::endl;
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(signature);
  CSkeletonNode *nodes[4]; 
  for(int i=0; i<4; ++i)
    nodes[i] = element->getNode(node_idxs[i]);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(signature);
  Coord *c[4];
  for(int i=0; i<4; ++i)
    c[i] = (*transitionPoints)[seg_idxs[i]].second;

  int count[4];
  for(int i=0; i<4; ++i)
    count[i] = movedNodes->count(nodes[i]->getIndex());
  if(count[0] == 0) {
    moves->push_back(SnapMove(nodes[0], c[0]));
    moves->push_back(SnapMove(nodes[0], c[3]));
    if(count[1] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1]));
      moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[0]));
      moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[1]));
      if(count[2] == 0) {
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[2], c[2]));
	moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[0],
				  nodes[2], c[2]));
	moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[0], 
				  nodes[2], c[2]));
	moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[1],
				  nodes[2], c[2]));
	if(count[3] == 0) {
	  moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				    nodes[2], c[2], nodes[3], c[3]));
	  moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[0],
				    nodes[2], c[1], nodes[3], c[2]));
	}
      }
      if(count[3] == 0) {
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[3], c[2]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[1], c[1],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[0], 
				  nodes[3], c[2]));
	moves->push_back(SnapMove(nodes[0], c[3], nodes[1], c[1],
				  nodes[3], c[2]));
      }
    }
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[2]));
      moves->push_back(SnapMove(nodes[0], c[3], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[0], c[3], nodes[2], c[2]));
      if(count[3] == 0) {
	moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1],
				  nodes[3], c[2]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[1],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[0], c[0], nodes[2], c[2],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[0], c[3], nodes[2], c[1], 
				  nodes[3], c[2]));
      }
    }
    if(count[3] == 0) {
      moves->push_back(SnapMove(nodes[0], c[0], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[0], c[0], nodes[3], c[3]));
      moves->push_back(SnapMove(nodes[0], c[3], nodes[3], c[2]));
    }
  }
  if(count[1] == 0) {
    moves->push_back(SnapMove(nodes[1], c[0]));
    moves->push_back(SnapMove(nodes[1], c[1]));
    if(count[2] == 0) {
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[1]));
      moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[2]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[2], c[2]));
      if(count[3] == 0) {
	moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[1],
				  nodes[3], c[2]));
	moves->push_back(SnapMove(nodes[1], c[0], nodes[2], c[2],
				  nodes[3], c[3]));
	moves->push_back(SnapMove(nodes[1], c[1], nodes[2], c[2],
				  nodes[3], c[3]));
      }
    }
    if(count[3] == 0) {
      moves->push_back(SnapMove(nodes[1], c[0], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[1], c[0], nodes[3], c[3]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[1], c[1], nodes[3], c[3]));
    }
  }
  if(count[2] == 0) {
    moves->push_back(SnapMove(nodes[2], c[1]));
    moves->push_back(SnapMove(nodes[2], c[2]));
    if(count[3] == 0) {
      moves->push_back(SnapMove(nodes[2], c[1], nodes[3], c[2]));
      moves->push_back(SnapMove(nodes[2], c[1], nodes[3], c[3]));
      moves->push_back(SnapMove(nodes[2], c[2], nodes[3], c[3]));
    }
  }
  if(count[3] == 0) {
    moves->push_back(SnapMove(nodes[3], c[2]));
    moves->push_back(SnapMove(nodes[3], c[3]));
  }

  return moves;
}
