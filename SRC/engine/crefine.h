// -*- C++ -*-
// $RCSfile: crefine.h,v $
// $Revision: 1.1.4.23 $
// $Author: langer $
// $Date: 2014/12/14 01:07:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CREFINE_H
#define CREFINE_H

#include <oofconfig.h>

class CSkeleton;
#include "engine/cskeletonselectable_i.h"
#include "engine/cskeletonmodifier.h"
#include "engine/crefinementcriterion.h"

// Define TESTCOVERAGE to include code that checks to see which
// refinement rules are used.  This is useful when developing
// regression tests.
//#define TESTCOVERAGE

#ifdef TESTCOVERAGE
typedef std::map<std::string, int> RuleCounter;
#endif // TESTCOVERAGE


/******************************************************

                    HELPER CLASS

*******************************************************/

class ProvisionalRefinement {
private:
  CSkeletonElementVector *newElements;
#ifdef TESTCOVERAGE
  static RuleCounter rulesUsed;
  static RuleCounter rulesAccepted;
#endif // TESTCOVERAGE
  // internal nodes?
public:
  ProvisionalRefinement(CSkeletonElementVector*, const std::string&);
#ifdef TESTCOVERAGE
  const std::string rule;
#endif	// TESTCOVERAGE
  ~ProvisionalRefinement() { delete newElements; }
  double energy(CSkeleton *skeleton, double alpha) const;
  void accept(CSkeleton *skeleton) const;
  CSkeletonElementVector *getElements() { return newElements; }
  bool hasElement(CSkeletonElement*) const;
  friend void printRuleUsage();
  friend void clearRuleUsage();
};

// These functions are used when looking for test cases for the
// regression tests.
void avoidDeadLocks(bool);
void printRuleUsage();
void clearRuleUsage();

typedef std::vector<ProvisionalRefinement*> ProvisionalRefinementVector;


/******************************************************

                 THE ACTUAL MODIFIER

*******************************************************/

class Refine;

typedef std::pair<CSkeletonMultiNodeKey, CSkeletonNodeVector*> NewEdgeNodeDatum;
typedef std::map<CSkeletonMultiNodeKey, CSkeletonNodeVector*> NewEdgeNodes;
typedef std::vector<CSkeletonNodeVector*> ElementEdgeNodes;
// A type that represents a pointer to a function with the prototype
// of our refinement rule functions
typedef ProvisionalRefinement *(Refine::*RulePointer)(CSkeletonElement*,
						      RefinementSignature*,
						      CSkeleton*);
// map of signatures to pointers to rule functions
typedef std::pair<RefinementSignature, RulePointer> RuleDatum;
typedef std::map<RefinementSignature, RulePointer> RuleSet;
typedef std::set<RefinementSignature> RefinementSignatureSet;
typedef std::pair<CSkeletonElement*, RefinementSignature*> ElementSignature;
typedef std::vector<ElementSignature> ElementSignatureVector;


class Refine : public CSkeletonModifier {
protected:
  RefinementTargets *targets;
  RefinementCriterion *criterion;
  //RefinementDegree *degree;
  double alpha;
  short divisions;
  NewEdgeNodes newEdgeNodes;
  static bool rulesCreated;
  static RuleSet conservativeRuleSet;
  static RefinementSignatureSet deadlockableSignatures;

public:
  Refine(RefinementTargets *trgts, RefinementCriterion *crtrn, double a);
  virtual ~Refine();
  virtual void cleanUp();
  CSkeletonBase *apply(CSkeletonBase *skeleton);
  CSkeletonBase *refine(CSkeletonBase *skeleton, CSkeleton *newSkeleton);
  virtual void getElementSignatures(CSkeletonBase *skeleton, 
				    CSkeleton *newSkeleton,
				    ElementSignatureVector &elements);
  virtual CSkeletonNodeVector *getNewEdgeNodes(CSkeletonNode *n1, 
					       CSkeletonNode *n2,
					       CSkeleton *newSkeleton);
  ElementEdgeNodes *getElementEdgeNodes(CSkeletonElement *element,
					CSkeleton *newSkeleton);
  CSkeletonSegment *findParentSegment(CSkeletonBase *oldSkeleton,
				      CSkeletonElement *element, 
				      CSkeletonSegment *segment);
  CSkeletonFace *findParentFace(CSkeletonBase *oldSkeleton,
				CSkeletonElement *element, CSkeletonFace *face);

  // rules

  ProvisionalRefinement *tetNullRule(CSkeletonElement *element,
				     RefinementSignature *sig,
				     CSkeleton *newSkeleton);
  ProvisionalRefinement *tet1Edge1Div(CSkeletonElement *element,
				      RefinementSignature *sig, 
				      CSkeleton *newSkeleton);
  ProvisionalRefinement *tet2Edges1DivAdjacent(CSkeletonElement *element,
					       RefinementSignature *sig,
					       CSkeleton *newSkeleton);
  ProvisionalRefinement *tet2Edges1DivOpposite(CSkeletonElement *element,
					       RefinementSignature *sig,
					       CSkeleton *newSkeleton);
  ProvisionalRefinement *tet3Edges1DivTriangle(CSkeletonElement *element,
					       RefinementSignature *sig,
					       CSkeleton *newSkeleton);
  ProvisionalRefinement *tet3Edges1DivZigZag(CSkeletonElement *element,
					     RefinementSignature *sig,
					     CSkeleton *newSkeleton);
  ProvisionalRefinement *tet3Edges1Div1Node(CSkeletonElement *element,
					    RefinementSignature *sig,
					    CSkeleton *newSkeleton);
  ProvisionalRefinement *tet4Edges1Div1(CSkeletonElement *element,
					RefinementSignature *sig,
					CSkeleton *newSkeleton);
  ProvisionalRefinement *tet4Edges1Div2(CSkeletonElement *element, 
					RefinementSignature *sig,
					CSkeleton *newSkeleton);
  ProvisionalRefinement *tet5Edges1Div(CSkeletonElement *element,
				       RefinementSignature *sig,
				       CSkeleton *newSkeleton);
  ProvisionalRefinement *tet6Edges1Div(CSkeletonElement *element,
				       RefinementSignature *sig,
				       CSkeleton *newSkeleton);
  static void createRuleSets();
};


#endif	// CREFINE_H

