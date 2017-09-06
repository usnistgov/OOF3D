
/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CSNAPNODES_H
#define CSNAPNODES_H

#include "common/coord_i.h"
#include "engine/cskeleton2_i.h"
#include "engine/cskeletonmodifier.h"
#include <queue>

typedef std::pair<bool, Coord*> TransitionPointDatum;
typedef std::map<CSkeletonMultiNodeKey, TransitionPointDatum>
  TransitionPointMap;
typedef std::vector<TransitionPointDatum> TransitionPointVector;
typedef std::vector<short> SnapSignature;

/******************************************************

                     TARGETS

*******************************************************/

class SnapNodeTargets {
protected:
  CSkeletonElementVector *elements;
public:
  SnapNodeTargets() {elements = NULL;};
  virtual CSkeletonElementVector* getElements(CSkeletonBase *skeleton) = 0;
  virtual ~SnapNodeTargets() {delete elements;};
};

class SnapAll : public SnapNodeTargets {
public:
  SnapAll() {};
  virtual CSkeletonElementVector* getElements(CSkeletonBase *skeleton);
  virtual ~SnapAll() {};
};

class SnapSelected : public SnapNodeTargets {
public:
  SnapSelected() {};
  virtual CSkeletonElementVector* getElements(CSkeletonBase *skeleton);
  virtual ~SnapSelected() {};
};

class SnapHeterogenous : public SnapNodeTargets {
private:
  double threshold;
public:
  SnapHeterogenous(double th) {threshold = th;};
  virtual CSkeletonElementVector* getElements(CSkeletonBase *skeleton);
  virtual ~SnapHeterogenous() {};
};

// SnapSelectedNodes
// class SnapSelectedNodes : public SnapNodeTargets {
// public:
//   SnapSelectedNodes() {};
//   virtual CSkeletonElementVector* getElements(CSkeletonBase *skeleton);
//   virtual ~SnapSelectedNodes() {};
// };


/******************************************************

                     SNAPPERS

*******************************************************/

typedef std::pair<CSkeletonNode*, Coord*> SnapMoveDatum;

class SnapMove {
private:
  std::vector<SnapMoveDatum> snaps;
public:
  SnapMove(CSkeletonNode*, Coord*); 
  SnapMove(CSkeletonNode*, Coord*, CSkeletonNode*, Coord*);
  SnapMove(CSkeletonNode*, Coord*, CSkeletonNode*, Coord*,
	   CSkeletonNode*, Coord*);
  SnapMove(CSkeletonNode*, Coord*, CSkeletonNode*, Coord*, 
	   CSkeletonNode*, Coord*, CSkeletonNode*, Coord*);
  ~SnapMove() {}
  bool isLegal() const;
  DeputyProvisionalChanges *getProvisionalChange(CDeputySkeleton*);
};

typedef std::vector<SnapMove> SnapMoveVector;
typedef std::set<int> IndexSet;

class NodeSnapperBase {
public:
  NodeSnapperBase() {};
  virtual ~NodeSnapperBase() {};
  void apply(CDeputySkeleton *skeleton, CSkelModCriterion *criterion,
	     IndexSet *movedNodes, IndexSet *curMoveNodesAffected);
  virtual SnapMoveVector *get_movelist(IndexSet *movedNodes) = 0;
  virtual short get_priority() = 0;
  virtual CSkeletonElement* getElement() = 0;
};

template <class X>
class NodeSnapper : public NodeSnapperBase {
 protected:
  CSkeletonElement *element;
  SnapSignature signature;
  TransitionPointVector *transitionPoints;
  // keep track of other snap points calculated by the snapper so that
  // the memory can be deallocated
  std::vector<Coord*> otherPoints; 

 public:
  NodeSnapper(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : element(el), signature(sig), transitionPoints(tps) {};
  virtual ~NodeSnapper();
  static NodeSnapperBase* factory(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps);
  CSkeletonElement* getElement() {return element;}
};


class Tet1EdgeSnapper : public NodeSnapper<Tet1EdgeSnapper> {
 public:
  Tet1EdgeSnapper(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet1EdgeSnapper>(el, sig, tps) {};
  virtual ~Tet1EdgeSnapper() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 5;};
  
};


class Tet2EdgesAdjacentSnapper : public NodeSnapper<Tet2EdgesAdjacentSnapper> {
 public:
  Tet2EdgesAdjacentSnapper(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet2EdgesAdjacentSnapper>(el, sig, tps) {};
  virtual ~Tet2EdgesAdjacentSnapper() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 4;};
  
};


class Tet2EdgesOppositeSnapper : public NodeSnapper<Tet2EdgesOppositeSnapper> {
 public:
  Tet2EdgesOppositeSnapper(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet2EdgesOppositeSnapper>(el, sig, tps) {};
  virtual ~Tet2EdgesOppositeSnapper() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 5;};
  
};

class Tet3EdgesTriangle : public NodeSnapper<Tet3EdgesTriangle> {
 public:
  Tet3EdgesTriangle(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet3EdgesTriangle>(el, sig, tps) {};
  virtual ~Tet3EdgesTriangle() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 3;};
  
};

class Tet3EdgesZigZag : public NodeSnapper<Tet3EdgesZigZag> {
 public:
  Tet3EdgesZigZag(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet3EdgesZigZag>(el, sig, tps) {};
  virtual ~Tet3EdgesZigZag() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 3;};
  
};

class Tet3Edges1Node : public NodeSnapper<Tet3Edges1Node> {
 public:
  Tet3Edges1Node(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet3Edges1Node>(el, sig, tps) {};
  virtual ~Tet3Edges1Node() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 1;};
  
};

class Tet4Edges1 : public NodeSnapper<Tet4Edges1> {
 public:
  Tet4Edges1(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet4Edges1>(el, sig, tps) {};
  virtual ~Tet4Edges1() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 2;};
  
};

class Tet4Edges2 : public NodeSnapper<Tet4Edges2> {
 public:
  Tet4Edges2(CSkeletonElement *el, SnapSignature sig, TransitionPointVector *tps)
    : NodeSnapper<Tet4Edges2>(el, sig, tps) {};
  virtual ~Tet4Edges2() {};
  virtual SnapMoveVector *get_movelist(IndexSet* movedNodes);
  virtual short get_priority() {return 3;};
  
};

typedef NodeSnapperBase* (*FactoryPointer)(CSkeletonElement *, SnapSignature, TransitionPointVector*);
typedef std::pair<SnapSignature, FactoryPointer> SnapperMapperPair;
typedef std::map<SnapSignature, FactoryPointer> SnapperMapper;
typedef std::vector<NodeSnapperBase*> SnapperVector;
typedef std::pair<short, SnapperVector*> PrioritySnapperPair;
typedef std::map<short, SnapperVector*> PrioritizedSnappers;
typedef std::vector<NodeSnapperBase*> AllMovesVector;
typedef std::queue<NodeSnapperBase*> NextMovesQueue;

/******************************************************

                 THE ACTUAL MODIFIER

*******************************************************/

class SnapNodes : public CSkeletonModifier {

protected:
  SnapNodeTargets *targets;
  CSkelModCriterion *criterion;
  static bool snapperMapperCreated;
  static SnapperMapper snapperMapper;
  int numSnapped;

public:
  SnapNodes(SnapNodeTargets*, CSkelModCriterion*); 
  ~SnapNodes() {};
  CSkeletonBase *apply(CSkeletonBase*);
  NodeSnapperBase *getNodeSnapper(CSkeletonElement*, TransitionPointVector*);
  static void createSnapperMapper();
  int getNumSnapped() { return numSnapped; }
};


#endif
