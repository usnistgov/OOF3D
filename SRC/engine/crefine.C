// -*- C++ -*-
// $RCSfile: crefine.C,v $
// $Revision: 1.1.4.72 $
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

#include "common/coord.h"
#include "common/printvec.h"
#include "common/progress.h"
#include "common/random.h"
#include "common/tostring.h"
#include "engine/canonicalorder.h"
#include "engine/crefine.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonsegment.h"
#include "engine/ooferror.h"
#include "common/IO/oofcerr.h"

#include <algorithm>

Refine::Refine(RefinementTargets *trgts, RefinementCriterion *crtrn, double a) {
  targets = trgts;
  criterion = crtrn;
  alpha = a;
  divisions = 1;
  if(!rulesCreated)
    createRuleSets();
}

Refine::~Refine() {}

void Refine::cleanUp() {
  for(NewEdgeNodes::iterator i=newEdgeNodes.begin(); i!=newEdgeNodes.end(); ++i)
      delete (*i).second;
  newEdgeNodes.clear();
}

CSkeletonBase* Refine::apply(CSkeletonBase *skeleton) {
  CSkeleton *newSkeleton = skeleton->nodeOnlyCopy();
  return refine(skeleton, newSkeleton);
}

CSkeletonSegment *Refine::findParentSegment(CSkeletonBase *oldSkeleton,
					    CSkeletonElement *element,
					    CSkeletonSegment *segment) 
{
  const CSkeletonNodeVector *nodes = segment->getNodes();
  CSkeletonNode *p0 = (CSkeletonNode*)(*nodes)[0]->last_parent();
  CSkeletonNode *p1 = (CSkeletonNode*)(*nodes)[1]->last_parent();
  
  // If both nodes have parents, return the segment formed by them, if
  // any.  findExistingSegment returns NULL if there is no segment.
  if(p0 != NULL && p1 != NULL) 
    return oldSkeleton->findExistingSegment(p0, p1);

  // Exactly one new endpoint has a parent in the old element.  If the
  // other endpoint lies on the same old segment, then that old
  // segment is the parent of this segment.
  else if (p0 != NULL || p1 != NULL) {
    CSkeletonNode *parentnode = NULL, *freechild = NULL;
    CSkeletonElement *oldElement = (CSkeletonElement *)(element->last_parent());
    if(p0 == NULL) {
      parentnode = p1;
      freechild = (*nodes)[0];
    }
    else if(p1 == NULL) {
      parentnode = p0;
      freechild = (*nodes)[1];
    }
    for(unsigned int i=0; i<oldElement->getNumberOfSegments(); ++i) {
      CSkeletonMultiNodeKey h = oldElement->getSegmentKey(i);
      NewEdgeNodes::iterator it = newEdgeNodes.find(h);
      if(it != newEdgeNodes.end()) {
	// For snap refine, newEdgeNodes can contain empty vectors.
	if((*it).second->size()) {
	  if( (freechild == (*it).second->front() ||
	       freechild == (*it).second->back()) &&
	      (parentnode == oldElement->getSegmentNode(i,0) ||
	       parentnode == oldElement->getSegmentNode(i,1)) ) 
	    {
	      return oldSkeleton->getSegment(oldElement->getSegmentKey(i));
	    }
	}
      }
    }
  }

  // TODO 3.1: the last case is only relevant for trisection, which we
  // haven't implemented yet.
  // else if(p0 == NULL && p1 == NULL)

  return NULL;
}

CSkeletonFace *Refine::findParentFace(CSkeletonBase *oldSkeleton,
				      CSkeletonElement *element,
				      CSkeletonFace *face) 
{
  const CSkeletonNodeVector *nodes = face->getNodes();
  CSkeletonNodeVector freenodes;
  CSkeletonNodeSet parentfacenodes;
  CSkeletonElement *oldElement = (CSkeletonElement *)(element->last_parent());
  for(CSkeletonNodeIterator it = nodes->begin(); it != nodes->end(); ++it) {
    CSkeletonNode *n = (CSkeletonNode *)(*it)->last_parent();
    if(n==NULL) freenodes.push_back((*it));
    else parentfacenodes.insert(n);
  }
 
  // find the segments in the old element that the new edge nodes, if
  // any, are on and add their nodes to the parentfacenodes set.  This
  // will be skipped if all nodes had parents.
  for(unsigned int i = 0; i<freenodes.size(); ++i) {
    for(unsigned int j=0; j<oldElement->getNumberOfSegments(); ++j) {
      CSkeletonMultiNodeKey h = oldElement->getSegmentKey(j);
      NewEdgeNodes::iterator it = newEdgeNodes.find(h);
      if(it != newEdgeNodes.end()) {
	if((*it).second->size()) {
	  if(freenodes[i] == (*it).second->front() ||
	     freenodes[i] == (*it).second->back())
	    {
	      parentfacenodes.insert(oldElement->getSegmentNode(j,0));
	      parentfacenodes.insert(oldElement->getSegmentNode(j,1));
	    }
	}
      }
    }
  }
    
  if(parentfacenodes.size() == 3) {
    // getting nodes out of the set is annoying, so convert to a vector
    CSkeletonNodeVector parents;
    for(CSkeletonNodeSet::iterator it=parentfacenodes.begin();
	it!=parentfacenodes.end(); ++it) 
      {
	parents.push_back((*it));
      }
    return oldSkeleton->findExistingFace(parents[0], parents[1], parents[2]);
  }
  return NULL;
}
  

void checkTotalVolume(ProvisionalRefinement *refinement, CSkeletonElement *el) {
  double tol = 0.001;
  double total_volume=0;
  for(CSkeletonElementVector::iterator it = refinement->getElements()->begin();
      it != refinement->getElements()->end(); ++it) 
    total_volume += (*it)->volume();

  double volume = el->volume();
  if(fabs(total_volume-volume)/volume > tol && volume>tol) {
    std::cerr << "total volume is incorrect" << std::endl;
    std::cerr << el->getUid() << " " << el->suspect() << " "
	      << total_volume << " " << volume << std::endl;
    // throw ErrProgrammingError("CRefine: total volume is incorrect",
    // 			      __FILE__, __LINE__);
  }
}

// We want to avoid deadlocks, except when testing code coverage for
// the refinement rules, in which case we want to make the unlikely
// cases more likely.  The AllRules test in
// skeleton_modfication_test.py runs with avoidDeadLocks_==false even
// when not testing refinement rule coverage, so we can't just set
// avoidDeadLocks_==true when TESTCOVERAGE is not defined.

static bool avoidDeadLocks_ = true;
void avoidDeadLocks(bool val) {
  avoidDeadLocks_ = val;
}

void Refine::getElementSignatures(CSkeletonBase *skeleton,
				  CSkeleton *newSkeleton,
				  ElementSignatureVector &elements)
{
  ElementSignatureVector nondeadlockable;
  for(int j=0; j<skeleton->nelements(); ++j) {
    RefinementSignature *sig = new RefinementSignature; 
    targets->signature(skeleton->getElement(j), sig);
    if(avoidDeadLocks_) {
      RefinementSignatureSet::iterator it = deadlockableSignatures.find(*sig);
      if(it!=deadlockableSignatures.end()) 
      elements.push_back(ElementSignature(skeleton->getElement(j),sig));
      else
	nondeadlockable.push_back(ElementSignature(skeleton->getElement(j),sig));
    }
    else
      elements.push_back(ElementSignature(skeleton->getElement(j), sig));
  }

  OOFRandomNumberGenerator r;
  oofshuffle(elements.begin(), elements.end(), r);
  if(avoidDeadLocks_) {
    oofshuffle(nondeadlockable.begin(), nondeadlockable.end(), r);
    elements.insert(elements.end(),
		    nondeadlockable.begin(), nondeadlockable.end());
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonBase* Refine::refine(CSkeletonBase *skeleton, CSkeleton *newSkeleton)
{

  DefiniteProgress *progress = 
    dynamic_cast<DefiniteProgress*>(getProgress("Refine", DEFINITE));
  try {
    //TODO MER: need additional marking for certain 2D cases
    targets->createSegmentMarks(skeleton, criterion, divisions);
    CSkeletonMultiNodeKeySet segmentSet;
    CSkeletonMultiNodeKeySet faceSet;

    // getElementSignatures creates vector of pairs of elements and
    // signatures.  It is randomized, with the deadlockable cases first.
    ElementSignatureVector elements; 
    getElementSignatures(skeleton, newSkeleton, elements);


    int count = 0;		// for progress bar
    for(ElementSignatureVector::iterator j=elements.begin(); j!=elements.end();
	++j) 
      {
	CSkeletonElement *el = j->first;
	RefinementSignature *sig = j->second;
	// oofcerr << "Refine::refinement: " << *el << " signature=[";
	// for(RefinementSignature::iterator it=sig->begin(); it!= sig->end(); ++it)
	// 	oofcerr << (*it).first << ", ";
	// oofcerr << "]" << std::endl;

	// Call the RulePointer for the given RefinementSignature.  The
	// rule set is a std::map from a RefinementSignature to a
	// RulePointer, which points to a method in the Refine class.
	// Because there's no way to rotate a 3D signature into a
	// canonical orientation (as is done in 2D), the rule set
	// contains a key for every equivalent orientation of every
	// signature.
	ProvisionalRefinement *refinement = 
	  (this->*conservativeRuleSet[*sig])(el, sig, newSkeleton);
	CSkeletonElementVector *newElements = refinement->getElements();
	// std::cerr << "Refine::refinement: refinement=" << refinement->rule
	// 		<< std::endl;
#ifdef DEBUG
	// check that the volume of the original element is the same
	// (within a small tolerance) of the total volume of the new
	// elements.
	checkTotalVolume(refinement, el);
#endif

	for(CSkeletonElementIterator new_it=newElements->begin();
	    new_it!=newElements->end(); ++new_it)
	  {
	    // if the parent's homogeneity is 1, this element's
	    // homogeneity is 1
	    if(el->homogeneity(skeleton->getMicrostructure()) == 1.0) {
	      (*new_it)->copyHomogeneity(*el);
	    }
	    // The calls to Skeleton.newElement() made by the refinement
	    // rules have created new SkeletonSegments in newSkeleton,
	    // but have not set the parentage of those segments.  We
	    // have to fix that here ...
	    for(unsigned int i=0; i<(*new_it)->getNumberOfSegments(); ++i) {
	      CSkeletonMultiNodeKey h = (*new_it)->getSegmentKey(i);
	      CSkeletonMultiNodeKeySet::iterator seg_it = segmentSet.find(h);
	      if(seg_it == segmentSet.end()) {
		segmentSet.insert(h);
		CSkeletonSegment *seg = newSkeleton->getSegment(h);
		CSkeletonSegment *parentSeg = findParentSegment(
						skeleton, (*new_it), seg); 
		if(parentSeg != NULL) {
		  parentSeg->add_child(seg);
		  seg->add_parent(parentSeg);
		}
	      }
	    }
	    // ... and we have to do the same with the faces
	    for(unsigned int i=0; i<(*new_it)->getNumberOfFaces(); ++i) {
	      CSkeletonMultiNodeKey h = (*new_it)->getFaceKey(i);
	      CSkeletonMultiNodeKeySet::iterator face_it = faceSet.find(h);
	      if(face_it == faceSet.end()) {
		faceSet.insert(h);
		CSkeletonFace *face = newSkeleton->getFace(h);
		CSkeletonFace *parentFace = findParentFace(skeleton, (*new_it),
							   face); 
		if(parentFace != NULL) {
		  parentFace->add_child(face);
		  face->add_parent(parentFace);
		}
	      }
	    }
	  }	// end loop over newElements
	progress->setFraction((count+1.0)/skeleton->nelements());
	progress->setMessage("refining skeleton: " + to_string(count+1) 
			     + "/" + to_string(skeleton->nelements()));

	delete refinement;
	delete sig;
      } // end loop over ElementSignatureVector elements.

    // Get rid of unused nodes, which may be leftover from unused
    // provisional refinements. 
    newSkeleton->dirty(); 
    newSkeleton->cleanUp();
  }
  catch(...) {
    progress->finish();
    throw;
  }
  progress->finish();
  return newSkeleton;
} // end Refine::refine

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonNodeVector *Refine::getNewEdgeNodes(CSkeletonNode *n1,
					     CSkeletonNode *n2, 
					     CSkeleton *newSkeleton) 
{
  if(divisions < 1)
    return NULL;

  CSkeletonMultiNodeKey h(n1,n2);
  NewEdgeNodes::iterator it = newEdgeNodes.find(h);

  if(it != newEdgeNodes.end()) {
    // New nodes have already been created on this edge.  Just return them.
    // TODO MER: reverse in 2d?
    return (*it).second;
  }
  CSkeletonNodeVector *nodes = new CSkeletonNodeVector; // deleted in cleanUp
  Coord p1;
  Coord p2;
  Coord delta;
  Coord x;
  p1 = n1->position();
  p2 = n2->position();
  for(int i=0; i<3; ++i)
    delta[i] = (p2[i]-p1[i])/(divisions+1);
  for(int i=0; i<divisions; ++i) {
    for(int j=0; j<3; ++j)
      x[j] = p1[j]+(i+1)*delta[j];
    nodes->push_back(newSkeleton->addNode(x.xpointer()));
  }
  // TODO 3.1: periodic cases
  newEdgeNodes.insert(NewEdgeNodeDatum(h,nodes));
  return nodes;
}

ElementEdgeNodes *Refine::getElementEdgeNodes(CSkeletonElement *element,
					      CSkeleton *newSkeleton) 
{
  ElementEdgeNodes *elementEdgeNodes = new ElementEdgeNodes;
  for(unsigned int i=0; i<element->getNumberOfSegments(); ++i) {
    elementEdgeNodes->push_back(
	getNewEdgeNodes(element->getSegmentNode(i,0),
			element->getSegmentNode(i,1), newSkeleton));
  }
  return elementEdgeNodes;
}

bool MinimumVolume::isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable)
  const
{
   if(units == "Voxel")
     return ((dynamic_cast<CSkeletonElement*> (selectable))->volumeInVoxelUnits(skeleton->getMicrostructure()) > threshold);
   else if(units == "Physical")
     return ((dynamic_cast<CSkeletonElement*> (selectable))->volume() > threshold);
   else if(units == "Fractional")
     return ((dynamic_cast<CSkeletonElement*> (selectable))->volumeInFractionalUnits(skeleton->getMicrostructure()) > threshold);
   else return false;
}

bool MinimumArea::isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable)
  const
{  
   if(units == "Voxel")
     return ((dynamic_cast<CSkeletonFace*> (selectable))->areaInVoxelUnits(skeleton->getMicrostructure()) > threshold);
   else if(units == "Physical")
     return ((dynamic_cast<CSkeletonFace*> (selectable))->area() > threshold);
   else if(units == "Fractional")
     return ((dynamic_cast<CSkeletonFace*> (selectable))->areaInFractionalUnits(skeleton->getMicrostructure()) > threshold);
   else return false;
}

bool MinimumLength::isGood(CSkeletonBase *skeleton, CSkeletonMultiNodeSelectable *selectable)
  const
{  
   if(units == "Voxel")
     return ((dynamic_cast<CSkeletonSegment*> (selectable))->lengthInVoxelUnits(skeleton->getMicrostructure()) > threshold);
   else if(units == "Physical")
     return ((dynamic_cast<CSkeletonSegment*> (selectable))->length() > threshold);
   else if(units == "Fractional")
     return ((dynamic_cast<CSkeletonSegment*> (selectable))->lengthInFractionalUnits(skeleton->getMicrostructure()) > threshold);
   else return false;
}

ProvisionalRefinement::ProvisionalRefinement(CSkeletonElementVector *els,
#ifdef TESTCOVERAGE
					     const std::string &rool
#else
					     const std::string&
#endif // TESTCOVERAGE
					     )
  : newElements(els) // els is new'd. ProvisionalRefinement takes ownership.
#ifdef TESTCOVERAGE
  , rule(rool)
#endif // TESTCOVERAGE
{
#ifdef DEBUG
  for(unsigned int i=0; i<els->size(); i++) {
    if((*els)[i]->illegal()) {
      std::cerr << "ProvisionalRefinement: Illegal Element: "
		<< i << " " << *(*els)[i] << std::endl;
      throw ErrProgrammingError("ProvisionalRefinement: Illegal Element!",
				__FILE__, __LINE__);
    }
  }
#endif // DEBUG
#if defined(TESTCOVERAGE) && defined(DEBUG)
  RuleCounter::iterator i = rulesUsed.find(rule);
  if(i == rulesUsed.end()) 
    rulesUsed[rule] = 1;
  else 
    (*i).second++;
#endif // TESTCOVERAGE
}

#ifdef TESTCOVERAGE
RuleCounter ProvisionalRefinement::rulesUsed;
RuleCounter ProvisionalRefinement::rulesAccepted;
#endif // TESTCOVERAGE

double ProvisionalRefinement::energy(CSkeleton *skeleton, double alpha) const {
  double energy = 0.0;
  for(CSkeletonElementVector::iterator it = newElements->begin();
      it != newElements->end(); ++it)
    energy += (*it)->energyTotal(skeleton->getMicrostructure(), alpha);
  return energy/newElements->size();
}

void ProvisionalRefinement::accept(CSkeleton *skeleton) const {
  for(CSkeletonElementVector::iterator it = newElements->begin();
      it != newElements->end(); ++it) 
    {
      skeleton->acceptProvisionalElement((*it));
    }
#if defined(TESTCOVERAGE) && defined(DEBUG)
  RuleCounter::iterator i = rulesAccepted.find(rule);
  if(i == rulesAccepted.end())
    rulesAccepted[rule] = 1;
  else
    (*i).second++;
#endif // TESTCOVERAGE
}

bool ProvisionalRefinement::hasElement(CSkeletonElement *el) const {
  for(CSkeletonElementVector::iterator it = newElements->begin();
      it != newElements->end(); ++it)
    if(el->getUid() == (*it)->getUid())
      return true;
  return false;
}

static void getElementChildrenNodes(CSkeletonElement *element,
				    CSkeletonNodeVector *childNodes)
{
  childNodes->clear();
  const CSkeletonNodeVector *parentNodes = element->getNodes();
  for(unsigned int i=0; i<parentNodes->size(); ++i) 
    childNodes->push_back((CSkeletonNode*)(*parentNodes)[i]->last_child());
}

#ifdef DEBUG
static bool checkIllegal(CSkeletonElement *el, CSkeletonElementVector *els,
			 RefinementSignature *sig, ElementEdgeNodes *edgeNodes) 
{
  // for debugging, check for illegal elements
  for(unsigned int i=0; i<els->size(); ++i) {
    if((*els)[i]->illegal()) {
      std::cerr << "ILLEGAL ELEMENT! " << i << " " << els->size() << " "
		<< el->illegal() << " " << el->suspect() << " " << el->volume()
		<< std::endl;
      // std::cerr << "original nodes:" << std::endl;
      // for(int j=0; j<4; ++j) {
      // 	el->getNode(j)->position(x);
      // 	std::cerr << el->getNode(j)->getUid() << " " << x[0] << " " << x[1] << " " << x[2] << std::endl;
      // }
      // el->printAngles();
      // std::cerr << "edge nodes " << std::endl;
      // for(int j=0; j<sig->size(); ++j) {
      // 	(*(*edgeNodes)[(*sig)[j].first])[0]->position(x);
      // 	std::cerr << (*(*edgeNodes)[(*sig)[j].first])[0]->getUid() << " " << x[0] << " " << x[1] << " " << x[2] << std::endl;
      // }
      // (*els)[i]->printAngles();
      return true;
    }
  }
  return false;
}
#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static ProvisionalRefinement *getBestRefinement(
				CSkeleton *skeleton,
				ProvisionalRefinementVector &refinements,
				double alpha,
				CSkeletonElementSet *xtras=0)
{
  double energy_min = 1000;
  ProvisionalRefinement *bestRefinement = 0;
// #ifdef DEBUG
//   DoubleVec energies;
// #endif // DEBUG
//   for(ProvisionalRefinementVector::const_iterator it=refinements.begin(); 
//       it!=refinements.end(); ++it)
//     {
//       std::cerr << "    " << (*it)->rule << std::endl;
//       double energy = (*it)->energy(skeleton, alpha);
// // #ifdef DEBUG
// //       energies.push_back(energy);
// // #endif // DEBUG
//       // std::cerr << "getBestRefinement: energy=" << energy << " energy_min=" << energy_min << " "
//       //  		<< energy_min-energy << std::endl;
//       std::cerr << energy - energy_min << std::endl;
//       if(energy - energy_min < 0) {
// 	energy_min = energy;
// 	bestRefinement = *it;
//       }
//     }

  for(unsigned int i=0; i<refinements.size(); i++) {
    ProvisionalRefinement *ref = refinements[i];
    // std::cerr << "   " << ref->rule << std::endl;
    double energy = ref->energy(skeleton, alpha);
    //std::cerr << "      " << energy - energy_min << std::endl;
    if(energy < energy_min) {
      energy_min = energy;
      bestRefinement = ref;
    }
  }

// #ifdef DEBUG
//   for(unsigned int i=0; i<energies.size(); i++)
//     energies[i] -= energy_min;
//   std::cerr << "getBestRefinement: margins=" << energies << std::endl;
// #endif // DEBUG

  if(bestRefinement == 0) {
    std::cerr << "num refinements " << refinements.size() << std::endl;
    throw ErrProgrammingError("CRefine: could not find a refinement",
			      __FILE__, __LINE__);
  }

  // Delete the refinements and elements not used in the best
  // refinement.  If xtras is provided, any elements in it will also
  // be deleted, if they're not used in the best refinement.  We need
  // to make sure we don't try to delete the same element twice.

  // Any added nodes should be deleted automatically when their
  // element counts go to zero.

  CSkeletonElementSet doomed;
  for(ProvisionalRefinementVector::iterator it=refinements.begin(); 
      it!=refinements.end(); ++it) 
    {
      if((*it) != bestRefinement) {
	CSkeletonElementVector *ev = (*it)->getElements();
	for(CSkeletonElementVector::iterator i=ev->begin(); i!=ev->end(); ++i) {
	  if(*i != NULL)
	    doomed.insert(*i);
	}
	delete *it;
      }
    }

  // xtras contains additional elements that the refinement rule
  // created, but might not have been used in any
  // ProvisionalRefinement.
  if(xtras)
    for(CSkeletonElementSet::iterator it=xtras->begin(); it!=xtras->end(); ++it)
      doomed.insert(*it);

  for(CSkeletonElementSet::iterator e=doomed.begin(); e!= doomed.end(); ++e) {
    if(!bestRefinement->hasElement(*e))
      delete (*e);
  }

  bestRefinement->accept(skeleton);
  return bestRefinement;
}


/************************************************************

                          RULES
 
*************************************************************/

// TODO 3.1: These rules don't include methods for refining faces like
// this:
//
//        /|\                                /\           //
//       / | \                              /  \          // (g++ doesn't
//      /  |  \                            /    \         // like comments
//     /\  |  /\        They only use     /______\        // that end with
//    /  \ | /  \                this:   / \    / \       // a backslash)
//   /    \|/    \                      /   \  /   \      //
//  -------X-------                    /_____\/_____\     //
//      "frond"                      "central triangle"
// Refinements including the frond pattern could and possibly should
// be included, but they add a lot of complication, because all of
// different orientations of the pattern have to be considered for
// the 6, 5, and some of the 4 edge refinements.  Mixtures of the
// frond and central triangle patterns would have to be considered
// too.


ProvisionalRefinement *Refine::tetNullRule(CSkeletonElement *element,
					   RefinementSignature *sig,
					   CSkeleton *newSkeleton)
{
  // std::cerr << "tetNullRule " << element->getUid() << std::endl;
  std::string name = "tetNullRule";
  CSkeletonNodeVector *baseNodes = new CSkeletonNodeVector;
  getElementChildrenNodes(element, baseNodes);
  CSkeletonElementVector *els = new CSkeletonElementVector;
  els->push_back(new CSkeletonElement(baseNodes, element, name));
  ProvisionalRefinement *pr = new ProvisionalRefinement(els, name);
  pr->accept(newSkeleton);
  return pr;
}

// --------

// Refine a single edge.

ProvisionalRefinement *Refine::tet1Edge1Div(CSkeletonElement *element,
					    RefinementSignature *sig,
					    CSkeleton *newSkeleton)
{
  std::string name = "tet1Edge1Div";
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  CSkeletonElementVector *els = new CSkeletonElementVector(2);
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  int *idxs = CSkeletonElement::getEdgeArray((*sig)[0].first);

  CSkeletonNodeVector *newnodes0 = new CSkeletonNodeVector(baseNodes);
  (*newnodes0)[idxs[0]] = (*(*edgeNodes)[(*sig)[0].first])[0];
  (*els)[0] = new CSkeletonElement(newnodes0, element, name);
  CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
  (*newnodes1)[idxs[1]] = (*(*edgeNodes)[(*sig)[0].first])[0];
  (*els)[1] = new CSkeletonElement(newnodes1, element, name);

  delete edgeNodes;

  ProvisionalRefinement *pr = new ProvisionalRefinement(els, name);
  pr->accept(newSkeleton);
  return pr;
} // end tet1Edge1Div

// --------

// Refine two adjacent edges.  See TwoEdgeAdjacentRefine-0.png and
// TwoEdgeAdjacentRefine-1.png.

ProvisionalRefinement *Refine::tet2Edges1DivAdjacent(CSkeletonElement *element,
						     RefinementSignature *sig,
						     CSkeleton *newSkeleton)
{
  // if(element->getUid() == 78531)
  //   std::cerr << "tet2Edges1DivAdjacent " << *sig << " " 
  // 	      << element->getUid() << std::endl;
  std::string name = "tet2Edges1DivAdjacent";
  ProvisionalRefinementVector refinements;
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);

  // (*sig)[i].first for i=0,1 are the indices of the segments being
  // refined.

  // (*edgeNodes)[j] is a pointer to a vector of new nodes on segment
  // j.

  // n0 is the node being added to the first segment listed in the
  // RefinementSignature.  n1 is being added to the second one.
  CSkeletonNode *n0 = (*(*edgeNodes)[(*sig)[0].first])[0];
  CSkeletonNode *n1 = (*(*edgeNodes)[(*sig)[1].first])[0];

  IndexVec idxs = CanonicalOrderMapper::getNodes(*sig);

  // Look for existing segments from the refinement of adjacent
  // elements.  They may restrict the possible refinements of this
  // element.

  // In the face defined by the two segments being refined, seg1 and
  // seg2 go from the new nodes, n0, and n1, to the opposite corner of
  // the face.
  CSkeletonSegment *seg1 = newSkeleton->findExistingSegment(
						    n0,baseNodes[idxs[2]]);
  CSkeletonSegment *seg2 = newSkeleton->findExistingSegment(
						    baseNodes[idxs[0]], n1);
  if(seg1 != NULL && seg2 != NULL)
    throw ErrProgrammingError("CRefine: inconsistent refinement on tet face",
			      __FILE__, __LINE__);

  // One tet is in both possible refinements.
  // The CSkeletonElement constructor requires a new'd vector of
  // nodes.  It assumes ownership.
  CSkeletonNodeVector *newnodes0 = new CSkeletonNodeVector(baseNodes);
  (*newnodes0)[idxs[0]] = n0;
  (*newnodes0)[idxs[2]] = n1;
  CSkeletonElement *tet0 = new CSkeletonElement(newnodes0, element, name);

  // Don't create a possible refinement if a conflicting segment
  // already exists.  It's not possible for both segments to exist,
  // because they would cross.
  if(seg2 == NULL) {
    CSkeletonElementVector *els = new CSkeletonElementVector;
    els->push_back(tet0);
    CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
    (*newnodes1)[idxs[1]] = n0;
    els->push_back(new CSkeletonElement(newnodes1, element, name));
    CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
    (*newnodes2)[idxs[0]] = n0;
    (*newnodes2)[idxs[1]] = n1;
    els->push_back(new CSkeletonElement(newnodes2, element, name));
#ifdef DEBUG
    checkIllegal(element, els, sig, edgeNodes);
#endif
    refinements.push_back(new ProvisionalRefinement(els, 
						    "tet2Edges1DivAdjacent_1"));
  }
  if(seg1 == NULL) {
    CSkeletonElementVector *els = new CSkeletonElementVector;
    els->push_back(tet0);
    CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
    (*newnodes1)[idxs[1]] = n1;
    els->push_back(new CSkeletonElement(newnodes1, element, name));
    CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
    (*newnodes2)[idxs[1]] = n0;
    (*newnodes2)[idxs[2]] = n1;
    els->push_back(new CSkeletonElement(newnodes2, element, name));
#ifdef DEBUG
    checkIllegal(element, els, sig, edgeNodes);
#endif
    refinements.push_back(new ProvisionalRefinement(els, 
						    "tet2Edges1DivAdjacent_2"));
  }

  delete edgeNodes;

  return getBestRefinement(newSkeleton, refinements, alpha);
} // end tet2Edges1DivAdjacent

// --------

// Refine a pair of non-adjacent edges.

ProvisionalRefinement *Refine::tet2Edges1DivOpposite(CSkeletonElement *element,
						     RefinementSignature *sig,
						     CSkeleton *newSkeleton)
{
  // std::cerr << "tet2EdgesDivOpposite " << element->getUid() << std::endl;
  std::string name = "tet2EdgesDivOpposite";
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  CSkeletonElementVector *els = new CSkeletonElementVector(4);
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  CSkeletonNode *n0 = (*(*edgeNodes)[(*sig)[0].first])[0];
  CSkeletonNode *n1 = (*(*edgeNodes)[(*sig)[1].first])[0];
  int *idxs0 = CSkeletonElement::getEdgeArray((*sig)[0].first);
  int *idxs1 = CSkeletonElement::getEdgeArray((*sig)[1].first);

  CSkeletonNodeVector *newnodes0 = new CSkeletonNodeVector(baseNodes);
  (*newnodes0)[idxs0[0]] = n0;
  (*newnodes0)[idxs1[0]] = n1;
  (*els)[0] = new CSkeletonElement(newnodes0, element, name);
  CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
  (*newnodes1)[idxs0[0]] = n0;
  (*newnodes1)[idxs1[1]] = n1;
  (*els)[1] = new CSkeletonElement(newnodes1, element, name);
  CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
  (*newnodes2)[idxs0[1]] = n0;
  (*newnodes2)[idxs1[0]] = n1;
  (*els)[2] = new CSkeletonElement(newnodes2, element, name);
  CSkeletonNodeVector *newnodes3 = new CSkeletonNodeVector(baseNodes);
  (*newnodes3)[idxs0[1]] = n0;
  (*newnodes3)[idxs1[1]] = n1;
  (*els)[3] = new CSkeletonElement(newnodes3, element, name);

  delete edgeNodes;

  ProvisionalRefinement *pr = new ProvisionalRefinement(els, name);
  pr->accept(newSkeleton);
  return pr;
} // end tet2Edges1DivOpposite

// --------

// Refine three edges that form a triangle.

ProvisionalRefinement *Refine::tet3Edges1DivTriangle(CSkeletonElement *element,
						     RefinementSignature *sig,
						     CSkeleton *newSkeleton)
{
  // std::cerr << "tet3Edges1DivTriangle " << element->getUid() << std::endl;
  std::string name = "tet3Edges1DivTriangle";
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  CSkeletonElementVector *els = new CSkeletonElementVector(4);
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  CSkeletonNode *n0 = (*(*edgeNodes)[(*sig)[0].first])[0];
  CSkeletonNode *n1 = (*(*edgeNodes)[(*sig)[1].first])[0];
  CSkeletonNode *n2 = (*(*edgeNodes)[(*sig)[2].first])[0];
  IndexVec idxs = CanonicalOrderMapper::getNodes(*sig);
  CSkeletonNodeVector *newnodes0 = new CSkeletonNodeVector(baseNodes);
  (*newnodes0)[idxs[1]] = n0;
  (*newnodes0)[idxs[2]] = n2;
  (*els)[0] = new CSkeletonElement(newnodes0, element, name);
  CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
  (*newnodes1)[idxs[0]] = n0;
  (*newnodes1)[idxs[2]] = n1;
  (*els)[1] = new CSkeletonElement(newnodes1, element, name);
  CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
  (*newnodes2)[idxs[0]] = n2;
  (*newnodes2)[idxs[1]] = n0;
  (*newnodes2)[idxs[2]] = n1;
  (*els)[2] = new CSkeletonElement(newnodes2, element, name);
  CSkeletonNodeVector *newnodes3 = new CSkeletonNodeVector(baseNodes);
  (*newnodes3)[idxs[0]] = n2;
  (*newnodes3)[idxs[1]] = n1;
  (*els)[3] = new CSkeletonElement(newnodes3, element, name);

  delete edgeNodes;

  ProvisionalRefinement *pr = new ProvisionalRefinement(els, name);
  pr->accept(newSkeleton);
  return pr;
} // end tet3Edges1DivTriangle

// --------

// Refine three sequentially connected edges that don't form a
// triangle.  See NOTES/tetrahedra/tet3edges1divzigzag.pdf

ProvisionalRefinement *Refine::tet3Edges1DivZigZag(CSkeletonElement *element,
						   RefinementSignature *sig,
						   CSkeleton *newSkeleton)
{
  // std::cerr << "tet3Edges1DivZigZag " << element->getUid() << std::endl;
  std::string name = "tet3Edges1DivZigZag";
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(*sig);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(*sig);
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  // n0, n1, and n2 are the new edge nodes.
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  CSkeletonNode *n0 = (*(*edgeNodes)[seg_idxs[0]])[0];
  CSkeletonNode *n1 = (*(*edgeNodes)[seg_idxs[1]])[0];
  CSkeletonNode *n2 = (*(*edgeNodes)[seg_idxs[2]])[0];

  // The seg*s are potential new segments on the faces of the parent
  // element.  seg0 and seg1 intersect, so only one of them can be
  // used and at most one can already exist (from the refinement of a
  // neighbor).  If one exists, it must be used.  Ditto for seg2 and
  // seg3.
  CSkeletonSegment *seg0 =
    newSkeleton->findExistingSegment(n1, baseNodes[node_idxs[3]]);
  CSkeletonSegment *seg1 =
    newSkeleton->findExistingSegment(n2, baseNodes[node_idxs[1]]);
  CSkeletonSegment *seg2 =
    newSkeleton->findExistingSegment(n1, baseNodes[node_idxs[0]]);
  CSkeletonSegment *seg3 =
    newSkeleton->findExistingSegment(n0, baseNodes[node_idxs[2]]);
#ifdef DEBUG
  if((seg0 != NULL && seg1 != NULL) || (seg2 != NULL && seg3 != NULL))
    throw ErrProgrammingError("CRefine: inconsistent refinement on tet face",
			      __FILE__, __LINE__);
#endif	// DEBUG

  ProvisionalRefinementVector refinements;
  // The tet formed by the line joining n0 and n2 and the original tet
  // edge from basenode0 to basenode3 is in all the refinements.
  CSkeletonNodeVector *newnodes0 = new CSkeletonNodeVector(baseNodes);
  (*newnodes0)[node_idxs[1]] = n0;
  (*newnodes0)[node_idxs[2]] = n2;
  CSkeletonElement *tet0 = new CSkeletonElement(newnodes0, element, name);

  // elset0 and elset1 store elements that are used in more than one
  // refinement below.
  CSkeletonElementVector elset0(3), elset1(3);
  CSkeletonElementSet maybe;	// new elements that might not be used
  if(seg0 == NULL) {
    elset0[0] = tet0;
    // n0, basenode1, n2, basenode3
    CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
    (*newnodes1)[node_idxs[0]] = n0;
    (*newnodes1)[node_idxs[2]] = n2;
    elset0[1] = new CSkeletonElement(newnodes1, element, name);
    maybe.insert(elset0[1]);
    CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
    (*newnodes2)[node_idxs[0]] = n0;
    (*newnodes2)[node_idxs[2]] = n1;
    (*newnodes2)[node_idxs[3]] = n2;
    elset0[2] = new CSkeletonElement(newnodes2, element, name);
    maybe.insert(elset0[2]);
  }
  if(seg1 == NULL) {
    elset1[0] = tet0;
    CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
    (*newnodes1)[node_idxs[0]] = n0;
    (*newnodes1)[node_idxs[2]] = n1;
    elset1[1] = new CSkeletonElement(newnodes1, element, name);
    maybe.insert(elset1[1]);
    CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
    (*newnodes2)[node_idxs[0]] = n0;
    (*newnodes2)[node_idxs[1]] = n1;
    (*newnodes2)[node_idxs[2]] = n2;
    elset1[2] = new CSkeletonElement(newnodes2, element, name);
    maybe.insert(elset1[2]);
  }
  // Create the refinements.  There may be up to four, depending on
  // the pre-existence of segs 0-3.
  if(seg2 == NULL) {
    CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
    (*newnodes1)[node_idxs[0]] = n0;
    (*newnodes1)[node_idxs[1]] = n1;
    (*newnodes1)[node_idxs[3]] = n2;
    CSkeletonElement *tet1 = new CSkeletonElement(newnodes1, element, name);
    CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
    (*newnodes2)[node_idxs[1]] = n0;
    (*newnodes2)[node_idxs[3]] = n2;
    CSkeletonElement *tet2 = new CSkeletonElement(newnodes2, element, name);
    if(seg0 == NULL) {
      CSkeletonElementVector *els2 = new CSkeletonElementVector(elset0);
      els2->push_back(tet1);
      els2->push_back(tet2);
      refinements.push_back(new ProvisionalRefinement(els2,
						      "tet3Edges1DivZigZag_1"));
    }
    if(seg1 == NULL) {
      CSkeletonElementVector *els2 = new CSkeletonElementVector(elset1);
      els2->push_back(tet1);
      els2->push_back(tet2);
      refinements.push_back(new ProvisionalRefinement(els2,
						      "tet3Edges1DivZigZag_2"));
    }
  }
  if(seg3 == NULL) {
    CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
    (*newnodes1)[node_idxs[1]] = n0;
    (*newnodes1)[node_idxs[2]] = n1;
    (*newnodes1)[node_idxs[3]] = n2;
    CSkeletonElement *tet1 = new CSkeletonElement(newnodes1, element, name);
    CSkeletonNodeVector *newnodes2 = new CSkeletonNodeVector(baseNodes);
    (*newnodes2)[node_idxs[1]] = n1;
    (*newnodes2)[node_idxs[3]] = n2;
    CSkeletonElement *tet2 = new CSkeletonElement(newnodes2, element, name);
    if(seg0 == NULL) {
      CSkeletonElementVector *els2 = new CSkeletonElementVector(elset0);
      els2->push_back(tet1);
      els2->push_back(tet2);
      refinements.push_back(new ProvisionalRefinement(els2, 
						      "tet3Edges1DivZigZag_3"));
    }
    if(seg1 == NULL) {
      CSkeletonElementVector *els2 = new CSkeletonElementVector(elset1);
      els2->push_back(tet1);
      els2->push_back(tet2);
      refinements.push_back(new ProvisionalRefinement(els2, 
						      "tet3Edges1DivZigZag_4"));
    }
  }

  delete edgeNodes;

  return getBestRefinement(newSkeleton, refinements, alpha, &maybe);
} // end tet3Edges1DivZigZag

// --------

// Refine three edges that all connect to one node.

ProvisionalRefinement *Refine::tet3Edges1Div1Node(CSkeletonElement *element,
						  RefinementSignature *sig,
						  CSkeleton *newSkeleton)
{
  // std::cerr << "tet3Edges1Div1Node "  << element->getUid() << std::endl;
  std::string name = "tet3Edges1Div1Node";
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(*sig);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(*sig);

  CSkeletonNodeVector baseNodes1;
  getElementChildrenNodes(element, &baseNodes1);
  CSkeletonNodeVector baseNodes;
  for(int i=0; i<4; ++i)
    baseNodes.push_back(baseNodes1[node_idxs[i]]);
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  CSkeletonNodeVector ns;
  for(int i=0; i<3; ++i)
    ns.push_back((*(*edgeNodes)[seg_idxs[i]])[0]);

  CSkeletonSegmentVector segA(3);
  CSkeletonSegmentVector segB(3);
  for(int i=0; i<3; ++i) {
    segA[i] = newSkeleton->findExistingSegment(ns[i], baseNodes[(i+1)%3]);
    segB[i] = newSkeleton->findExistingSegment(ns[(i+1)%3], baseNodes[i]);
  }
  
  // One tet is in all possible refinements
  CSkeletonElement *kingtet = new CSkeletonElement(ns[0], ns[1], ns[2],
						   baseNodes[3],
						   element, name);
  
  ProvisionalRefinementVector refinements;
  // there are two basic cases - all existing segments can tilt the
  // same way (all in segA are not NULL or all in B are not NULL)
  // which means we need an internal node, or one of the three is
  // different or at least one does not exist yet.

  // the case where one is different or at least one is non existent
  for(int i=0; i<3; ++i) {
    if( segA[(i+2)%3] == NULL && segB[i] == NULL ) {
      CSkeletonElement *tet1 =
	new CSkeletonElement(baseNodes[0], baseNodes[1], baseNodes[2], ns[i],
			     element, name);
      if( segB[(i+1)%3] == NULL) {
	CSkeletonElementVector *els = new CSkeletonElementVector;
	els->push_back(kingtet);
	els->push_back(tet1);
	CSkeletonNodeVector *newnodes0 = new CSkeletonNodeVector(baseNodes);
	(*newnodes0)[i] = ns[i];
	(*newnodes0)[3] = ns[(i+1)%3];
	els->push_back(new CSkeletonElement(newnodes0, element, name));
	CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
	(*newnodes1)[i] = ns[i];
	(*newnodes1)[(i+1)%3] = ns[(i+1)%3];
	(*newnodes1)[3] = ns[(i+2)%3];
	els->push_back(new CSkeletonElement(newnodes1, element, name));
	refinements.push_back(
		      new ProvisionalRefinement(els, "tet3Edges1Div1Node_1"));
      }
      if( segA[(i+1)%3] == NULL) {
	CSkeletonElementVector *els = new CSkeletonElementVector;
	els->push_back(kingtet);
	els->push_back(tet1);
	CSkeletonNodeVector *newnodes0 = new CSkeletonNodeVector(baseNodes);
	(*newnodes0)[i] = ns[i];
	(*newnodes0)[3] = ns[(i+2)%3];
	els->push_back(new CSkeletonElement(newnodes0, element, name));
	CSkeletonNodeVector *newnodes1 = new CSkeletonNodeVector(baseNodes);
	(*newnodes1)[i] = ns[i];
	(*newnodes1)[(i+2)%3] = ns[(i+2)%3];
	(*newnodes1)[3] = ns[(i+1)%3];
	els->push_back(new CSkeletonElement(newnodes1, element, name));
	refinements.push_back(
		      new ProvisionalRefinement(els, "tet3Edges1Div1Node_2"));
      }
    }
  }

  // this is the "deadlocking" case
  if(refinements.empty()) {
    // Add a new node at the average position of the new nodes and the
    // nodes at the base of the original tet (the nodes of the face
    // opposite the node where the subdivided edges meet).
    Coord y;
    for(int i=0; i<3; ++i) {
      Coord x;
      x = baseNodes[i]->position();
      y += x;
      x = ns[i]->position();
      y += x;
    }
    y /= 6.0;
    CSkeletonNode *centernode = newSkeleton->addNode(y.xpointer());
    CSkeletonElementVector *els = new CSkeletonElementVector;
    els->push_back(kingtet);
    els->push_back(new CSkeletonElement(
	baseNodes[0], baseNodes[1], baseNodes[2], centernode,
	element, name));
    els->push_back(new CSkeletonElement(
	ns[2], ns[1], ns[0], centernode, element, name));
    if(segA[0]!=NULL && segA[1]!=NULL && segA[2]!=NULL) {
      els->push_back(new CSkeletonElement(
	  baseNodes[0], ns[0], baseNodes[1], centernode, element, name));
      els->push_back(new CSkeletonElement(
	  ns[0], ns[1], baseNodes[1], centernode, element, name));
      els->push_back(new CSkeletonElement(
	  baseNodes[1], ns[1], baseNodes[2], centernode, element, name));
      els->push_back(new CSkeletonElement(
	  baseNodes[2], ns[1], ns[2], centernode, element, name));
      els->push_back(new CSkeletonElement(
	  baseNodes[2], ns[2], baseNodes[0], centernode, element, name));
      els->push_back(new CSkeletonElement(
	  ns[2], ns[0], baseNodes[0], centernode, element, name));
    }
    else if(segB[0]!=NULL && segB[1]!=NULL && segB[2]!=NULL) {
      els->push_back(new CSkeletonElement(
		  ns[0], ns[1], baseNodes[0], centernode, element, name));
      els->push_back(new CSkeletonElement(
		  baseNodes[0], ns[1], baseNodes[1], centernode,
		  element, name));
      els->push_back(new CSkeletonElement(
		  baseNodes[1], ns[1], ns[2], centernode, element, name));
      els->push_back(new CSkeletonElement(
		  baseNodes[1], ns[2], baseNodes[2], centernode,
		  element, name));
      els->push_back(new CSkeletonElement(
		  baseNodes[2], ns[2], ns[0], centernode, element, name));
      els->push_back(new CSkeletonElement(
		  ns[0], baseNodes[0], baseNodes[2], centernode,
		  element, name));
    }
    refinements.push_back(
	   new ProvisionalRefinement(els, "tet3Edges1Div1Node_deadlock"));
  }

  delete edgeNodes;
  return getBestRefinement(newSkeleton, refinements, alpha);
} // end tet3Edges1Div1Node

// --------

// Refine all but two adjacent edges.  See
// NOTES/tetrahedra/tet4edges1div1.pdf and tet4edges1div1A.pdf.

ProvisionalRefinement *Refine::tet4Edges1Div1(CSkeletonElement *element,
					      RefinementSignature *sig,
					      CSkeleton *newSkeleton)
{
  // std::cerr << "tet4Edges1Div1 " << element->getUid() << std::endl;
  std::string name = "tet4Edges1Div1";
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(*sig);
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(*sig);

  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  CSkeletonNodeVector ns;
  for(int i=0; i<4; ++i)
    ns.push_back((*(*edgeNodes)[seg_idxs[i]])[0]);
  CSkeletonElementSet maybe;

  CSkeletonSegment *seg0 = 
    newSkeleton->findExistingSegment(ns[0], baseNodes[node_idxs[2]]);
  CSkeletonSegment *seg1 =
    newSkeleton->findExistingSegment(ns[1], baseNodes[node_idxs[0]]);
  CSkeletonSegment *seg2 =
    newSkeleton->findExistingSegment(ns[0], baseNodes[node_idxs[3]]);
  CSkeletonSegment *seg3 =
    newSkeleton->findExistingSegment(ns[3], baseNodes[node_idxs[0]]);

  // this tet is in every refinement
  CSkeletonElement *tet0 = new CSkeletonElement(baseNodes[node_idxs[1]],
						ns[1], ns[3], ns[0],
						element, name);
  // this tet is in almost all refinements (tet4edges1div1.pdf)
  CSkeletonElement *tet1 = new CSkeletonElement(ns[1], ns[2], ns[3], ns[0],
						element, name); 
  maybe.insert(tet1);

  // tet0 and tet1 leave two quadrilateral-based pyramids to be
  // filled.  The apex of both pyramids is ns[2].  The base of both
  // can be subdivided into a triangle in two ways, using seg0 or seg1
  // for one pyramid, and seg2 or seg3 for the other.  However, if
  // seg1 and seg3 are being used, then there's a simpler refinement
  // that doesn't use tet1.

  ProvisionalRefinementVector refinements;

  CSkeletonElementVector els0(4);
  CSkeletonElementVector els1(4);
  
  // els0 and els1 represent the ways of dividing one of the pyramids,
  // the one whose base contains nodes basenode0, basenode2, ns[0],
  // and ns[1]. 
  if(seg0 == NULL) {
    els0[0] = tet0;
    els0[1] = tet1;
    // These elements use seg1.
    els0[2] = new CSkeletonElement(baseNodes[node_idxs[0]], ns[1], ns[0], ns[2],
				   element, name);
    els0[3] = new CSkeletonElement(
			   baseNodes[node_idxs[0]], baseNodes[node_idxs[2]],
			   ns[1], ns[2], element, name);
    maybe.insert(els0[2]);
    maybe.insert(els0[3]);
  }
  if(seg1 == NULL) {
    els1[0] = tet0;
    els1[1] = tet1;
    // These elements use seg0.
    els1[2] = new CSkeletonElement(baseNodes[node_idxs[2]], ns[1], ns[0], ns[2],
				   element, name);
    els1[3] = new CSkeletonElement(
			   baseNodes[node_idxs[0]], baseNodes[node_idxs[2]],
			   ns[0], ns[2], element, name);
    maybe.insert(els1[2]);
    maybe.insert(els1[3]);
  }
  if(seg2 == NULL) {
    CSkeletonElement *tet2 = new CSkeletonElement(
	  ns[3], baseNodes[node_idxs[3]], baseNodes[node_idxs[0]], ns[2],
	  element, name);
    if(seg0 == NULL) {
      // seg0 and seg2 aren't present, so we're free to create seg1
      // and seg3. This is the special case that doesn't require tet1.
      // See NOTES/tetrahedra/tet4edges1div1A.pdf.
      CSkeletonElementVector *els = new CSkeletonElementVector();
      els->push_back(tet0);
      els->push_back(tet2);
      els->push_back(new CSkeletonElement(
	  baseNodes[node_idxs[0]], ns[1], ns[2], baseNodes[node_idxs[2]],
	  element, name));
      els->push_back(new CSkeletonElement(
	  baseNodes[node_idxs[0]], ns[2], ns[1], ns[3], element, name));
      els->push_back(new CSkeletonElement(
	  baseNodes[node_idxs[0]], ns[1], ns[0], ns[3], element, name));
      refinements.push_back(new ProvisionalRefinement(els, "tet4Edges1Div1_0"));
    }
    if(seg1 == NULL) {
      CSkeletonElementVector *els = new CSkeletonElementVector(els1);
      CSkeletonElement *tet3 = new CSkeletonElement(
		    ns[0],ns[3],baseNodes[node_idxs[0]],ns[2], element, name);
      els->push_back(tet2);
      els->push_back(tet3);
      refinements.push_back(new ProvisionalRefinement(els, "tet4Edges1Div1_1"));
    }
  }
  if(seg3 == NULL) {
    CSkeletonElement *tet2 = new CSkeletonElement(
	  ns[0], baseNodes[node_idxs[3]], baseNodes[node_idxs[0]], ns[2],
	  element, name);
    CSkeletonElement *tet3 = new CSkeletonElement(
	  ns[3], baseNodes[node_idxs[3]], ns[0], ns[2], element, name);
    if(seg0 == NULL) {
      CSkeletonElementVector *els = new CSkeletonElementVector(els0);
      els->push_back(tet2);
      els->push_back(tet3);
      refinements.push_back(new ProvisionalRefinement(els, "tet4Edges1Div1_2"));
    }
    if(seg1 == NULL) {
      CSkeletonElementVector *els = new CSkeletonElementVector(els1);
      els->push_back(tet2);
      els->push_back(tet3);
      refinements.push_back(new ProvisionalRefinement(els, "tet4Edges1Div1_3"));
    }
  }
  delete edgeNodes;

  return getBestRefinement(newSkeleton, refinements, alpha, &maybe);
} // end tet4Edges1Div1

// --------

// Refine all but two non-adjacent edges.  See
// NOTES/tetrahedra/tet4edges1div2.pdf.

ProvisionalRefinement *Refine::tet4Edges1Div2(CSkeletonElement *element,
					      RefinementSignature *sig,
					      CSkeleton *newSkeleton)
{
  // std::cerr << "tet4Edges1Div2 " << *sig << " " << element->getUid()
  // 	    << std::endl;
  std::string name = "tet4Edges1Div2";
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(*sig);
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(*sig);
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  // list of lists of new nodes on each edge
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  CSkeletonNodeVector ns(4);	// new nodes on edges
  for(int i=0; i<4; ++i)
    ns[i] = (*(*edgeNodes)[seg_idxs[i]])[0];
  // Nodes at the ends of the unmarked edges. oen[0] contains the
  // nodes of one unmarked edge (hereafter called the "top"
  // edge). oen[1] contains the nodes of the other.  (Valerie called
  // these "opposite edge nodes", hence the name "oen".)
  CSkeletonNodeVector oen[2];
  for(int i=0; i<2; ++i) {
    oen[0].push_back(baseNodes[node_idxs[i]]);
    oen[1].push_back(baseNodes[node_idxs[2+i]]);
  }
  
  // The refinements split the tet along the quad defined by the four
  // edge nodes (the "septum"). The four points defining the septum
  // are not necessarily in a plane.  Then we have two wedges, one
  // above and one below the septum.  The septum must be split by a
  // diagonal, and the top and bottom wedges must both use the same
  // diagonal.  The wedges can each be split into tets six possible
  // ways, 3 for each choice of septum diagonal.  Then we match up
  // pairs of wedge subdivisions which share the same diagonal for a
  // total of 18 possibilities with 6 tets each.

  // wedges[0] is a list of all the ways of subdividing the top wedge.
  // They are all compatible with the ways of subdividing the bottom
  // wedge that are stored in wedges[2] because they all divide the
  // septum along the same diagonal.  Similarly, wedges[1] is a list
  // of ways of subdividing the top that are compatible with wedges[3]
  // on the bottom, using the other septum diagonal.  Each list only
  // includes wedge subdivisions that are compatible with neighboring
  // elements.  This bookkeeping is complicated but it's better than
  // typing out all the cases individually.
  std::vector<CSkeletonElementVector*> wedges[4];

  // 'maybe' keeps track of all of the tetrahedra that have been
  // created but might not be included in a refinement, so that ones
  // that aren't used can be destroyed (by getBestRefinement).  It's
  // *not* sufficient to be careful to only create the tets that are
  // actually used in wedges, because a wedge might not be used in any
  // refinements.  In particular, neighboring elements might restrict
  // one wedge to one orientation of the septum diagonal, but not
  // restrict the other wedge.  Then elements will be generated for
  // both diagonals of the other wedge, but half of them won't be
  // used.
  CSkeletonElementSet maybe;

  for(int i=0; i<2; ++i) {	// i=0 ==> top, i==1 ==> bottom
    // The segs in segA go from an edge node to oen[i][0] and the segs
    // in segB go from edge nodes to oen[i][1].  The refinement can
    // use both segments from segA or both from segB, or one from
    // each.  Note that nodes ns 0 and 2 get swapped at the end of the
    // i loop, so that when constructing the tets for the bottom
    // wedge, the septum is effectively viewd from the other side.
    CSkeletonSegment *segA0 = newSkeleton->findExistingSegment(ns[3],oen[i][0]);
    CSkeletonSegment *segA1 = newSkeleton->findExistingSegment(ns[2],oen[i][0]);
    CSkeletonSegment *segB0 = newSkeleton->findExistingSegment(ns[0],oen[i][1]);
    CSkeletonSegment *segB1 = newSkeleton->findExistingSegment(ns[1],oen[i][1]);

#ifdef DEBUG
    if((segA0!=NULL && segB0!=NULL) || (segA1!=NULL && segB1!=NULL))
      throw ErrProgrammingError(
			"CRefine: inconsistent refinement on tet face",
			__FILE__, __LINE__);
#endif // DEBUG

    // We need to be careful that tet pointers are only allocated if
    // they are used in a ProvisionalRefinement so that they get
    // deleted. These are the pointers for tets that will be used in
    // more than one block of code below. Tets that are used in only
    // one block are declared and initialized in that block.
    CSkeletonElement *tet0 = NULL;
    CSkeletonElement *tet2 = NULL;
    CSkeletonElement *tet4 = NULL;
    CSkeletonElement *tet5 = NULL;
    CSkeletonElement *tet7 = NULL;
    CSkeletonElement *tet10 = NULL;
      
    // These wedges all have the segment ns[2] to ns[0] crossing the
    // septum.
    if(segB0==NULL and segB1==NULL) {
      CSkeletonElement *tet1 = new CSkeletonElement(ns[3], ns[2], ns[0],
						    oen[i][0], element, name);
      CSkeletonElementVector *els0 = new CSkeletonElementVector(3);
      if(!tet0)
	tet0 = new CSkeletonElement(ns[2],ns[1],ns[0],oen[i][0],
				    element, name);
      if(!tet2)
	tet2 = new CSkeletonElement(ns[2], ns[3], oen[i][1], oen[i][0],
				    element, name);
      (*els0)[0] = tet0;
      (*els0)[1] = tet1;
      (*els0)[2] = tet2;
      wedges[2*i].push_back(els0);
      maybe.insert(tet0);
      maybe.insert(tet1);
      maybe.insert(tet2);
    }
    if(segA0==NULL and segA1==NULL) {
      CSkeletonElement *tet3 = new CSkeletonElement(ns[2], ns[1], ns[0],
						    oen[i][1], element, name);
      if(!tet4)
	tet4 = new CSkeletonElement(ns[3],ns[2],ns[0],oen[i][1], element, name);
      if(!tet5)
	tet5 = new CSkeletonElement(ns[0], ns[1], oen[i][0], oen[i][1],
				  element, name);
      CSkeletonElementVector *els1 = new CSkeletonElementVector(3);
      (*els1)[0] = tet3;
      (*els1)[1] = tet4;
      (*els1)[2] = tet5;
      maybe.insert(tet3);
      maybe.insert(tet4);
      maybe.insert(tet5);
      wedges[2*i].push_back(els1);
    }
    if(segA0==NULL and segB1==NULL) {
      if(!tet0)
	tet0 = new CSkeletonElement(ns[2],ns[1],ns[0],oen[i][0], element, name);
      if(!tet4)
	tet4 = new CSkeletonElement(ns[3],ns[2],ns[0],oen[i][1], element, name);
      CSkeletonElement *tet6 = new CSkeletonElement(oen[i][0], ns[2], oen[i][1],
						    ns[0], element, name);
      CSkeletonElementVector *els2 = new CSkeletonElementVector(3);
      (*els2)[0] = tet6;
      (*els2)[1] = tet0;
      (*els2)[2] = tet4;
      maybe.insert(tet6);
      maybe.insert(tet0);
      maybe.insert(tet4);
      wedges[2*i].push_back(els2);
    }

    // These wedges cross the septum the other way: ns[1] to ns[3].
    if(segB0==NULL and segB1==NULL) {
      if(!tet2)
	tet2 = new CSkeletonElement(ns[2], ns[3], oen[i][1], oen[i][0],
				    element, name);
      if(!tet7)
	tet7 = new CSkeletonElement(ns[3],ns[1],ns[0],oen[i][0], element, name);
      CSkeletonElement *tet8 = new CSkeletonElement(ns[3], ns[2], ns[1],
						    oen[i][0], element, name);
      CSkeletonElementVector *els3 = new CSkeletonElementVector(3);
      (*els3)[0] = tet7;
      (*els3)[1] = tet8;
      (*els3)[2] = tet2;
      maybe.insert(tet7);
      maybe.insert(tet8);
      maybe.insert(tet2);
      wedges[2*i+1].push_back(els3);
    }
    if(segA0==NULL and segA1==NULL) {
      if(!tet5)
	tet5 = new CSkeletonElement(ns[0], ns[1], oen[i][0], oen[i][1],
				  element, name);
      CSkeletonElement *tet9 = new CSkeletonElement(ns[3], ns[1], ns[0],
						    oen[i][1], element, name);
      if(!tet10)
	tet10 = new CSkeletonElement(ns[3],ns[2],ns[1],oen[i][1], element,
				     name);
      CSkeletonElementVector *els4 = new CSkeletonElementVector(3);
      (*els4)[0] = tet9;
      (*els4)[1] = tet10;
      (*els4)[2] = tet5;
      maybe.insert(tet9);
      maybe.insert(tet10);
      maybe.insert(tet5);
      wedges[2*i+1].push_back(els4);
    }
    if(segB0==NULL and segA1==NULL) {
      if(!tet7)
	tet7 = new CSkeletonElement(ns[3],ns[1],ns[0],oen[i][0], element, name);
      if(!tet10)
	tet10 = new CSkeletonElement(ns[3],ns[2],ns[1],oen[i][1], element,
				     name);
      CSkeletonElement *tet11 = new CSkeletonElement(oen[i][0], ns[1],
						     oen[i][1], ns[3],
						     element, name);
      CSkeletonElementVector *els5 = new CSkeletonElementVector(3);
      (*els5)[0] = tet11;
      (*els5)[1] = tet10;
      (*els5)[2] = tet7;
      maybe.insert(tet11);
      maybe.insert(tet10);
      maybe.insert(tet7);
      wedges[2*i+1].push_back(els5);
    }
    // reorder the edge nodes so we produce legal elements on the next
    // iteration (i=1)
    CSkeletonNode *temp = ns[0];
    ns[0] = ns[2];
    ns[2] = temp;
  } // end loop over i=0,1 (top, bottom)


  ProvisionalRefinementVector refinements;
#ifdef TESTCOVERAGE
  int count = 0;
#endif
  for(int i=0; i<2; ++i) {
    for(std::vector<CSkeletonElementVector*>::iterator top = wedges[i].begin(); 
	top != wedges[i].end(); ++top)
      {
	for(std::vector<CSkeletonElementVector*>::iterator
	      bottom = wedges[2+i].begin(); bottom != wedges[2+i].end();
	    ++bottom)
	  {
	    CSkeletonElementVector *els = new CSkeletonElementVector(**top);
	    for(CSkeletonElementIterator it = (*bottom)->begin();
		it != (*bottom)->end(); ++it)
	      {
		els->push_back((*it));
	      }
#ifdef TESTCOVERAGE
	    std::string n = name + "_" + to_string(++count);
#else
	    std::string &n = name;
#endif	// TESTCOVERAGE
	    refinements.push_back(new ProvisionalRefinement(els, n)); // n 1-18
	  }
      }
  }

  // If the pre-existing segments segA* and segB* have precluded any
  // of the above refinements, it's necessary to add a node in the
  // center of the element.
  if(refinements.empty()) {
    // std::cerr << "DEADLOCKING CASE tet4Edges1Div2" << std::endl;
    Coord x;
    x = element->center();
    CSkeletonNode *centernode = newSkeleton->addNode(x.xpointer());
    CSkeletonElementVector *els = new CSkeletonElementVector;
    els->push_back(new CSkeletonElement(ns[0],ns[1],oen[0][0],centernode,
					element, name));
    els->push_back(new CSkeletonElement(ns[3],oen[0][1],ns[2],centernode,
					element, name));
    els->push_back(new CSkeletonElement(ns[2],ns[1],oen[1][0],centernode,
					element, name));
    els->push_back(new CSkeletonElement(oen[1][1],ns[0],ns[3],centernode,
					element, name));

    if(newSkeleton->findExistingSegment(ns[3],oen[0][0])!=NULL) {
      els->push_back(new CSkeletonElement(ns[0],oen[0][0],ns[3],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(ns[3],oen[0][0],oen[0][1],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(oen[0][0],ns[1],oen[0][1],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(oen[0][1],ns[1],ns[2],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(oen[1][1],oen[1][0],ns[0],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(ns[0],oen[1][0],ns[1],centernode, 
					  element, name));
      els->push_back(new CSkeletonElement(oen[1][1],ns[2],oen[1][0],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(oen[1][1],ns[3],ns[2],centernode,
					  element, name));
    }
    else if(newSkeleton->findExistingSegment(ns[0],oen[0][1])!=NULL) {
      els->push_back(new CSkeletonElement(ns[3],ns[0],oen[0][1],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(ns[0],oen[0][0],oen[0][1],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(oen[0][1],oen[0][0],ns[2],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(ns[2],oen[0][0],ns[1],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(ns[0],oen[1][1],ns[1],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(oen[1][1],oen[1][0],ns[1],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(oen[1][1],ns[3],oen[1][0],centernode,
					  element, name));
      els->push_back(new CSkeletonElement(ns[3],ns[2],oen[1][0],centernode,
					  element, name));
    }
    refinements.push_back(
		  new ProvisionalRefinement(els, "tet4Edges1Div2_deadlock"));
  }

  delete edgeNodes;

  return getBestRefinement(newSkeleton, refinements, alpha, &maybe);
} // end tet4Edges1Div2

// --------

// Refine all but one edge.  See NOTES/tetrahedra/tet5edges1div.pdf.

ProvisionalRefinement *Refine::tet5Edges1Div(CSkeletonElement *element, 
					     RefinementSignature *sig,
					     CSkeleton *newSkeleton)
{
  // There are six possible refinements, some of which may be
  // forbidden by the neighboring elements, if they've already been
  // refined.  The new nodes added to the four edges that are adjacent
  // to the unrefined edge define a quadrilateral ("septum") that
  // divides the original tet into two wedges.  Call the wedge
  // containing the unrefined edge the "bottom" wedge.  It can be
  // subdivided in six ways, each of which adds a diagonal edge across
  // the septum, just like the wedges in tet4Edges1Div2.  The top
  // wedge can be subdivided in only two ways, one for each
  // orientation of the septum diagonal.
  std::string name = "tet5Edges1Div";
  IndexVec seg_idxs = CanonicalOrderMapper::getSegs(*sig);
  IndexVec node_idxs = CanonicalOrderMapper::getNodes(*sig);
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  CSkeletonNodeVector uen, oen;
  for(int i=0; i<2; ++i) {
    uen.push_back(baseNodes[node_idxs[i]]);   // unmarked edge nodes
    oen.push_back(baseNodes[node_idxs[2+i]]); // opposite edge nodes
  }
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  CSkeletonNodeVector ns(5);
  for(int i=0; i<5; ++i) 
    ns[i] = (*(*edgeNodes)[seg_idxs[i]])[0];

  // These tets are in every possible refinement.  They're the outer
  // two corners of the top wedge.
  CSkeletonElement *tet0 =
    new CSkeletonElement(ns[1],ns[2],ns[4],oen[0], element, name);
  CSkeletonElement *tet1 =
    new CSkeletonElement(ns[0],ns[4],ns[3],oen[1], element, name);
  // We can split the remaining space in the top wedge in two
  // different ways.  We can then combine that with the "bottom wedge"
  // which can be refined as in tet4Edges1Div2.
  CSkeletonElementVector topwedges[2];
  CSkeletonElementSet maybe;	      // tets that might not be used
  for(int i=0; i<2; ++i) {
    topwedges[i].push_back(tet0);
    topwedges[i].push_back(tet1);
  }
  CSkeletonElement *tet2 =
    new CSkeletonElement(ns[0],ns[1],ns[2],ns[4], element, name);
  maybe.insert(tet2);
  topwedges[0].push_back(tet2);
  CSkeletonElement *tet3 =
    new CSkeletonElement(ns[0],ns[2],ns[3],ns[4], element, name);
  maybe.insert(tet3);
  topwedges[0].push_back(tet3);
  CSkeletonElement *tet4 =
    new CSkeletonElement(ns[0],ns[1],ns[3],ns[4], element, name);
  maybe.insert(tet4);
  topwedges[1].push_back(tet4);
  CSkeletonElement *tet5 =
    new CSkeletonElement(ns[1],ns[2],ns[3],ns[4], element, name);
  maybe.insert(tet5);
  topwedges[1].push_back(tet5);

  // Create provisional refinements for the bottom wedge only if
  // conflicting segments aren't present in the neighboring elements.

  // Look for conflicting segments.
  CSkeletonSegment *segA0 = newSkeleton->findExistingSegment(ns[3],uen[0]);
  CSkeletonSegment *segA1 = newSkeleton->findExistingSegment(ns[2],uen[0]);
  CSkeletonSegment *segB0 = newSkeleton->findExistingSegment(ns[0],uen[1]);
  CSkeletonSegment *segB1 = newSkeleton->findExistingSegment(ns[1],uen[1]);

  // These tets might be used in more than one refinement.  All of the
  // tets created from here on will definitely be used, so they don't
  // have to be inserted into the 'maybe' set.
  CSkeletonElement *tet6 = NULL;
  CSkeletonElement *tet9 = NULL;
  CSkeletonElement *tet12 = NULL;
  CSkeletonElement *tet15 = NULL;

  ProvisionalRefinementVector refinements;

  if(segB0 == NULL && segB1 == NULL) {
    if(!tet6)
      tet6 = new CSkeletonElement(ns[2],ns[1],ns[0],uen[0], element, name);
    CSkeletonElement *tet7 =
      new CSkeletonElement(ns[3],ns[2],ns[0],uen[0], element, name);
    CSkeletonElement *tet8 =
      new CSkeletonElement(ns[2],ns[3],uen[1],uen[0], element, name);
    if(!tet9)
      tet9 = new CSkeletonElement(ns[3],ns[1],ns[0],uen[0], element, name);
    CSkeletonElement *tet10 =
      new CSkeletonElement(ns[3],ns[2],ns[1],uen[0], element, name);
    CSkeletonElementVector *els0 = new CSkeletonElementVector(topwedges[0]);
    els0->push_back(tet6);
    els0->push_back(tet7);
    els0->push_back(tet8);
    refinements.push_back(new ProvisionalRefinement(els0, "tet5Edges1Div_1"));
    CSkeletonElementVector *els1 = new CSkeletonElementVector(topwedges[1]);
    els1->push_back(tet9);
    els1->push_back(tet10);
    els1->push_back(tet8);
    refinements.push_back(new ProvisionalRefinement(els1, "tet5Edges1Div_2"));
  }

  if(segA0 == NULL && segA1 == NULL) {
    CSkeletonElement *tet11 =
      new CSkeletonElement(ns[2],ns[1],ns[0],uen[1], element, name);
    if(!tet12)
      tet12 = new CSkeletonElement(ns[3],ns[2],ns[0],uen[1], element, name);
    CSkeletonElement *tet13 =
      new CSkeletonElement(ns[0],ns[1],uen[0],uen[1], element, name);
    CSkeletonElement *tet14 =
      new CSkeletonElement(ns[3],ns[1],ns[0],uen[1], element, name);
    if(!tet15)
      tet15 = new CSkeletonElement(ns[3],ns[2],ns[1],uen[1], element, name);
    CSkeletonElementVector *els0 = new CSkeletonElementVector(topwedges[0]);
    els0->push_back(tet11);
    els0->push_back(tet12);
    els0->push_back(tet13);
    refinements.push_back(new ProvisionalRefinement(els0, "tet5Edges1Div_3"));
    CSkeletonElementVector *els1 = new CSkeletonElementVector(topwedges[1]);
    els1->push_back(tet14);
    els1->push_back(tet15);
    els1->push_back(tet13);
    refinements.push_back(new ProvisionalRefinement(els1, "tet5Edges1Div_4")); 
  }

  if(segA0 == NULL && segB1 == NULL) {
    if(!tet6)
      tet6 = new CSkeletonElement(ns[2],ns[1],ns[0],uen[0], element, name);
    if(!tet12)
      tet12 = new CSkeletonElement(ns[3],ns[2],ns[0],uen[1], element, name);
    CSkeletonElement *tet16 =
      new CSkeletonElement(uen[0],ns[2],uen[1],ns[0], element, name);
    CSkeletonElementVector *els = new CSkeletonElementVector(topwedges[0]);
    els->push_back(tet16);
    els->push_back(tet6);
    els->push_back(tet12);
    refinements.push_back(new ProvisionalRefinement(els, "tet5Edges1Div_5"));
  }

  if(segA1 == NULL && segB0 == NULL) {
    if(!tet9)
      tet9 = new CSkeletonElement(ns[3],ns[1],ns[0],uen[0], element, name);
    if(!tet15)
      tet15 = new CSkeletonElement(ns[3],ns[2],ns[1],uen[1], element, name);
    CSkeletonElement *tet17 =
      new CSkeletonElement(uen[0],ns[1],uen[1],ns[3], element, name);
    CSkeletonElementVector *els = new CSkeletonElementVector(topwedges[1]);
    els->push_back(tet17);
    els->push_back(tet15);
    els->push_back(tet9);
    refinements.push_back(new ProvisionalRefinement(els, "tet5Edges1Div_6"));
  }

  delete edgeNodes;

  return getBestRefinement(newSkeleton, refinements, alpha, &maybe);
} // end tet5Edges1Div

// --------

// Refine all edges.

ProvisionalRefinement *Refine::tet6Edges1Div(CSkeletonElement *element,
					     RefinementSignature *sig,
					     CSkeleton *newSkeleton) 
{
  // std::cerr << "tet6Edges1Div " << element->getUid() << std::endl;
  std::string name = "tet6Edges1Div";
  CSkeletonNodeVector baseNodes;
  getElementChildrenNodes(element, &baseNodes);
  ProvisionalRefinementVector refinements;
  ElementEdgeNodes *edgeNodes = getElementEdgeNodes(element, newSkeleton);
  
  // create four outer corner tets -- node i is the only node not
  // replaced, the other three nodes are the adjacent edge nodes
  CSkeletonElementVector cornerTets; 
  for(int i=0; i<4; ++i) {
    CSkeletonNodeVector *newnodes = new CSkeletonNodeVector(baseNodes);
    for(int j=0; j<3; ++j) {
      int edge_idx = CSkeletonElement::getNodeEdgeIndex(i,j);
      int *edgenode_idxs = CSkeletonElement::getEdgeArray(edge_idx);
      int node_idx = (edgenode_idxs[0]==i?edgenode_idxs[1]:edgenode_idxs[0]);
      (*newnodes)[node_idx] = (*(*edgeNodes)[edge_idx])[0];
    }
    cornerTets.push_back(new CSkeletonElement(newnodes, element, name));
  }
  // now, with the six edge nodes, there are three ways to divide
  // them into four tetrahedra without adding new nodes
  static const int opposites[3][2] = {{0,5},{1,3},{2,4}};
  for(int i=0; i<3; ++i) {	// loop over refinements
    CSkeletonElementVector *newTets = new CSkeletonElementVector(cornerTets);
    for(int j=0; j<4; ++j) {	// loop over new tets
      // Each new tet has a face that connects the three edgenodes on
      // a face of the parent tet.  Find the fourth node:
      CSkeletonNode *oppnode;
      if(opposites[i][0]!=CSkeletonElement::getFaceEdgeIndex(j,0) && 
	 opposites[i][0]!=CSkeletonElement::getFaceEdgeIndex(j,1) && 
	 opposites[i][0]!=CSkeletonElement::getFaceEdgeIndex(j,2))
	{
	  oppnode = (*(*edgeNodes)[opposites[i][0]])[0];
	}
      else
	{
	  oppnode = (*(*edgeNodes)[opposites[i][1]])[0];
	}
      CSkeletonNodeVector *newnodes = new CSkeletonNodeVector;
      newnodes->push_back(
		  (*(*edgeNodes)[CSkeletonElement::getFaceEdgeIndex(j,2)])[0]);
      newnodes->push_back(
		  (*(*edgeNodes)[CSkeletonElement::getFaceEdgeIndex(j,1)])[0]);
      newnodes->push_back(
		  (*(*edgeNodes)[CSkeletonElement::getFaceEdgeIndex(j,0)])[0]);
      newnodes->push_back(oppnode);
      CSkeletonElement *newelement = new CSkeletonElement(newnodes, element,
							  name);
      newTets->push_back(newelement);
    } // end loop over new tets j
#ifdef TESTCOVERAGE
    std::string n = name + "_" + to_string(i);
#else
    std::string &n = name;
#endif // TESTCOVERAGE
    ProvisionalRefinement *pr = new ProvisionalRefinement(newTets, n); // n 1-3
    refinements.push_back(pr);
  } // end loop over refinements i
  delete edgeNodes;
  return getBestRefinement(newSkeleton, refinements, alpha);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void printRuleUsage() { 
#ifdef TESTCOVERAGE
  std::cerr << "Rules used (" << ProvisionalRefinement::rulesUsed.size()
	    << "/45):" << std::endl; // 45 is the number of rule cases
  for(RuleCounter::iterator i=ProvisionalRefinement::rulesUsed.begin();
      i!=ProvisionalRefinement::rulesUsed.end(); ++i)
    {
      std::cerr << "   " << (*i).first << " " << (*i).second << std::endl;
    }
  std::cerr << "Rules accepted (" << ProvisionalRefinement::rulesAccepted.size()
	    << "):" << std::endl;
  for(RuleCounter::iterator i=ProvisionalRefinement::rulesAccepted.begin();
      i!=ProvisionalRefinement::rulesAccepted.end(); ++i)
    {
      std::cerr << "   " << (*i).first << " " << (*i).second << std::endl;
    }
#endif	// TESTCOVERAGE
}

void clearRuleUsage() {
#ifdef TESTCOVERAGE
  ProvisionalRefinement::rulesUsed.clear();
  ProvisionalRefinement::rulesAccepted.clear();
#endif	// TESTCOVERAGE
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Convenience function for creating rule sets. 'a' is a list of
// pairs.  The first entry is an element segment index.  The second is
// the number of divisions on the segment.  When signatures are
// generated by RefinementTargets::signature(), the segments looped
// over in element segment index order, so the lists here must be in
// that order too (and no other orders need to occur in the rule set.)

static RefinementSignature array2Signature(short a[][2], int size) {
  RefinementSignature sig;
  for(int i=0; i<size; ++i) 
    sig.push_back(RefinementSignaturePair(a[i][0], a[i][1]));
  return sig;
}

bool Refine::rulesCreated = false;			// static
RuleSet Refine::conservativeRuleSet = RuleSet();	// static
RefinementSignatureSet Refine::deadlockableSignatures = // static
  RefinementSignatureSet();

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Refine::createRuleSets() {	// static method
  int i;

  RefinementSignature emptysig;
  conservativeRuleSet.insert( RuleDatum( emptysig , &Refine::tetNullRule) );

  // Refine a single edge.
  short r1[6][1][2] = { {{0,1}}, {{1,1}}, {{2,1}}, {{3,1}}, {{4,1}}, {{5,1}} };
  for(i=0; i<6; ++i) 
    conservativeRuleSet.insert( 
	       RuleDatum( array2Signature(r1[i], 1) , &Refine::tet1Edge1Div) );
 
  // Refine two adjacent edges, ie, edges sharing a node.  There are
  // twelve such pairs of edges: 12 = 6*5/2 - 3, where 3 is the number
  // of pairs of non-adjacent edges.

  short r2_1[12][2][2] = { {{0,1},{1,1}}, 
			   {{0,1},{2,1}}, 
			   {{0,1},{3,1}}, 
			   {{0,1},{4,1}}, 
			   {{1,1},{2,1}}, 
			   {{1,1},{4,1}},
			   {{1,1},{5,1}}, 
			   {{2,1},{3,1}}, 
			   {{2,1},{5,1}}, 
			   {{3,1},{4,1}}, 
			   {{3,1},{5,1}}, 
			   {{4,1},{5,1}} };
  for(i=0; i<12; ++i) 
    conservativeRuleSet.insert(
       RuleDatum( array2Signature(r2_1[i], 2) , &Refine::tet2Edges1DivAdjacent) 
			       ); 

  // Refine a pair of non-adjacent edges.
  short r2_2[3][2][2] = { {{0,1},{5,1}}, 
			  {{1,1},{3,1}}, 
			  {{2,1},{4,1}} };
  for(i=0; i<3; ++i) 
    conservativeRuleSet.insert(
       RuleDatum( array2Signature(r2_2[i], 2) , &Refine::tet2Edges1DivOpposite) 
			       ); 

  // Refine three edges that form a triangle.
  short r3_1[4][3][2] = { {{0,1},{3,1},{4,1}}, 
			  {{0,1},{1,1},{2,1}}, 
			  {{2,1},{3,1},{5,1}}, 
			  {{1,1},{4,1},{5,1}} };
  for(i=0; i<4; ++i)
    conservativeRuleSet.insert(
       RuleDatum(array2Signature(r3_1[i], 3) , &Refine::tet3Edges1DivTriangle)
			       ); 

  // Refine three sequentially connected edges that don't form a
  // triangle.
  short r3_2[12][3][2] = { {{0,1},{2,1},{4,1}}, 
			   {{0,1},{1,1},{5,1}}, 
			   {{0,1},{1,1},{3,1}}, 
			   {{1,1},{2,1},{4,1}}, 
			   {{0,1},{2,1},{5,1}}, 
			   {{1,1},{2,1},{3,1}}, 
			   {{1,1},{3,1},{5,1}}, 
			   {{2,1},{3,1},{4,1}},
			   {{0,1},{4,1},{5,1}}, 
			   {{1,1},{3,1},{4,1}}, 
			   {{0,1},{3,1},{5,1}}, 
			   {{2,1},{4,1},{5,1}} };
  for(i=0; i<12; ++i)
    conservativeRuleSet.insert(
       RuleDatum( array2Signature(r3_2[i], 3) , &Refine::tet3Edges1DivZigZag)
			       ); 

  // Refine three edges that all connect to one node.
  short r3_3[4][3][2] = { {{3,1},{4,1},{5,1}}, 
			  {{0,1},{1,1},{4,1}}, 
			  {{0,1},{2,1},{3,1}}, 
			  {{1,1},{2,1},{5,1}} };
  for(i=0; i<4; ++i)  {
    conservativeRuleSet.insert(
       RuleDatum( array2Signature(r3_3[i], 3) , &Refine::tet3Edges1Div1Node) ); 
    deadlockableSignatures.insert(array2Signature(r3_3[i], 3));
  }

  // Refine all but two adjacent edges.  I.e, refine three edges in a
  // triangle plus one more edge.
  short r4_1[12][4][2] = { {{0,1},{1,1},{3,1},{4,1}}, 
			   {{0,1},{2,1},{3,1},{4,1}}, 
			   {{0,1},{3,1},{4,1},{5,1}}, 
			   {{0,1},{1,1},{4,1},{5,1}},
			   {{1,1},{2,1},{4,1},{5,1}}, 
			   {{1,1},{3,1},{4,1},{5,1}}, 
			   {{0,1},{2,1},{3,1},{5,1}}, 
			   {{1,1},{2,1},{3,1},{5,1}}, 
			   {{2,1},{3,1},{4,1},{5,1}}, 
			   {{0,1},{1,1},{2,1},{3,1}}, 
			   {{0,1},{1,1},{2,1},{4,1}}, 
			   {{0,1},{1,1},{2,1},{5,1}} };
  for(i=0; i<12; ++i) 
    conservativeRuleSet.insert(
       RuleDatum( array2Signature(r4_1[i], 4) , &Refine::tet4Edges1Div1) ); 

  // Refine all but two non-adjacent edges.
  short r4_2[3][4][2] = { {{1,1},{2,1},{3,1},{4,1}}, 
			  {{0,1},{2,1},{4,1},{5,1}}, 
			  {{0,1},{1,1},{3,1},{5,1}} };
  for(i=0; i<3; ++i)  {
    conservativeRuleSet.insert(
       RuleDatum( array2Signature(r4_2[i], 4) , &Refine::tet4Edges1Div2) ); 
    deadlockableSignatures.insert(array2Signature(r4_2[i], 4));
  }

  // Refine all but one edge.
  short r5[6][5][2] = { {{0,1},{1,1},{2,1},{3,1},{4,1}},
			{{0,1},{1,1},{2,1},{3,1},{5,1}},
			{{0,1},{1,1},{2,1},{4,1},{5,1}},                
			{{0,1},{1,1},{3,1},{4,1},{5,1}},
			{{0,1},{2,1},{3,1},{4,1},{5,1}},
			{{1,1},{2,1},{3,1},{4,1},{5,1}} };
  for(i=0; i<6; ++i)
    conservativeRuleSet.insert(
       RuleDatum( array2Signature(r5[i], 5) , &Refine::tet5Edges1Div) );

  // Refine all edges.
  short r6[6][2] = {{0,1}, {1,1}, {2,1}, {3,1}, {4,1}, {5,1}};
  conservativeRuleSet.insert(
     RuleDatum( array2Signature(r6, 6) , &Refine::tet6Edges1Div) );

  rulesCreated = true;
}

