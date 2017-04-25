// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CFIDDLENODES_H
#define CFIDDLENODES_H

#include "common/coord_i.h"
#include "engine/cskeletonselectable_i.h"
#include "engine/cskeletonmodifier.h"

/******************************************************

                     TARGETS

*******************************************************/

class FiddleNodesTargets {
protected:
  // nodes is set by getNodes().  It's a pointer so that we can
  // distinguish betwen an empty list and a list that hasn't been set
  // yet.
  CSkeletonNodeVector *nodes;
public:
  FiddleNodesTargets() : nodes(0) {}
  virtual ~FiddleNodesTargets() {};
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton) = 0;
  void cleanUp() { delete nodes; nodes = 0; }
};

class AllNodes : public FiddleNodesTargets {
public:
  AllNodes() : FiddleNodesTargets() {}
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton);
};

class SelectedNodes : public FiddleNodesTargets {
public:
  SelectedNodes() : FiddleNodesTargets() {}
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton);
};

class NodesInGroup : public FiddleNodesTargets {
private:
  const std::string group;
public:
  NodesInGroup(const std::string &g) : group(g) {}
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton);
};

class InternalBoundaryNodes : public FiddleNodesTargets {
private:
  CSkeletonNodeSet nodeSet;
public:
  InternalBoundaryNodes() {}
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton);
};

class FiddleSelectedElements : public FiddleNodesTargets {
public:
  FiddleSelectedElements() : FiddleNodesTargets() {}
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton);
};

class FiddleHeterogeneousElements : public FiddleNodesTargets {
private:
  double threshold;
public:
  FiddleHeterogeneousElements(double t) : FiddleNodesTargets(), threshold(t) {}
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton);
};

class FiddleElementsInGroup : public FiddleNodesTargets {
private:
  const std::string group;
public:
  FiddleElementsInGroup(const std::string &g) : group(g) {}
  virtual CSkeletonNodeVector *getNodes(CSkeletonBase *skeleton);
};


/******************************************************

                     MODIFIERS

*******************************************************/

class FiddleNodes : public CSkeletonModifier {
protected:
  FiddleNodesTargets *targets;
  CSkelModCriterion *criterion;
  double T;
  int nok;
  int nbad;
  double deltaE;
  double totalE;
public:
  FiddleNodes(FiddleNodesTargets*, CSkelModCriterion*, double t);
  virtual ~FiddleNodes();
  int getNok() { return nok; }
  int getNbad() { return nbad; }
  double getDeltaE() { return deltaE; }
  double getTotalE() { return totalE; }
  CSkeletonBase *apply(CSkeletonBase *skeleton);
  void coreProcess(CDeputySkeleton *skeleton);
  CSkelModCriterion *getCriterion() { return criterion; }
  FiddleNodesTargets *getTargets() { return targets; }

  // The subclasses of FiddleNodes differ only in how getPosition
  // computes the candidate new positions of the nodes.
  virtual Coord getPosition(const CDeputySkeleton*, const CSkeletonNode*) 
    const = 0;
};

class Anneal : public FiddleNodes {
private:
  double delta;
public:
  Anneal(FiddleNodesTargets *trgts, CSkelModCriterion *crtrn, double t,
	 double d);
  virtual Coord getPosition(const CDeputySkeleton*, const CSkeletonNode*) const;
};

class Smooth : public FiddleNodes {
public:
  Smooth(FiddleNodesTargets *trgts, CSkelModCriterion *crtrn, double t);
  virtual Coord getPosition(const CDeputySkeleton*, const CSkeletonNode*) const;
};

class SurfaceSmooth : public FiddleNodes {
private:
  double gamma;
public:
  SurfaceSmooth(CSkelModCriterion *crtrn, double t, double g);
  virtual Coord getPosition(const CDeputySkeleton*, const CSkeletonNode*) const;
};

#endif	// CFIDDLENODES_H
