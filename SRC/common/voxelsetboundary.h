// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef VOXELSETBOUNDARY_H
#define VOXELSETBOUNDARY_H

#include <set>
#include <vector>

class ProtoVSBNode;
class VoxelSetBoundary;
class VSBGraph;
class VSBNode;

#include "common/coord.h"
class CMicrostructure;
class ICRectangularPrism;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class VoxelEdgeDirection {
public:
  VoxelEdgeDirection(unsigned int a, int d);
  VoxelEdgeDirection(const Coord3D&);
  unsigned int axis;		// 0, 1, or 2
  int dir;			// 1 or -1
  VoxelEdgeDirection reverse() const;
  bool operator==(const VoxelEdgeDirection &other) const {
    return axis == other.axis && dir == other.dir;
  }
};

std::ostream &operator<<(std::ostream&, const VoxelEdgeDirection&);

typedef std::vector<VoxelEdgeDirection> VoxelEdgeList;

class VoxRot {
private:
  VoxelEdgeList actualAxes;
public:
  VoxRot(VoxelEdgeDirection, VoxelEdgeDirection, VoxelEdgeDirection);
  VoxelEdgeDirection toActual(const VoxelEdgeDirection&) const;
  VoxelEdgeDirection toReference(const VoxelEdgeDirection&) const;
  friend std::ostream &operator<<(std::ostream&, const VoxRot&);
};

std::ostream &operator<<(std::ostream&, const VoxRot&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ProtoVSBNode {
protected:
  // Given two voxels, decide if they're in canonical order or
  // not. The answer is arbitrary, but must be the same for the other
  // ProtoVSBNode that shares the two voxels.  The voxels are
  // specified by the single voxel signatures, which define where they
  // are relative to the center of the current ProtoVSBNode in the
  // node's orientation.
  bool voxelOrder(unsigned char sig0, unsigned char sig1) const;
public:
  const VoxRot rotation;
  ProtoVSBNode(const VoxRot &rot);
  virtual ~ProtoVSBNode() {}

  // Pure virtual methods in this class are defined in subclasses
  // defined in voxelsetboundary.C.

  // makeVSBNodes constructs the VSBnodes and puts them in the graph,
  // but doesn't connect them.
  virtual void makeVSBNodes(VoxelSetBoundary*, const ICoord3D&) = 0;
  // connect connects nodes by creating links between VSBNodes in the
  // graph.  
  virtual void connect(ProtoVSBNode*) = 0;
  // connectBack tells the node that another node wants to connect.
  // It makes the connection and returns the VSBNode that the other
  // node should connect to.
  virtual VSBNode *connectBack(const ProtoVSBNode*, VSBNode*) = 0;

  // connectDoubleBack connects two nodes in the same direction, in
  // cases in which a split node connects along two coincident edges
  // to another split node. It's only used in some (but not all)
  // DoubleNode and TripleNode subclasses.  The base class method here
  // just raises an exception, because it should never be called.
  // It's defined here so that it doesn't have to be defined
  // separately in all of the DoubleNode and TripleNode classes that
  // *don't* need it.
  virtual void connectDoubleBack(const ProtoVSBNode*, VSBNode*, VSBNode*,
				 VSBNode*&, VSBNode*&);

  // connectDirs returns the reference space directions in which
  // neighbors need to be found.
  virtual const VoxelEdgeList &connectDirs() const = 0;
#ifdef DEBUG
  void checkDir(const VoxelEdgeDirection&) const;
#endif // DEBUG

  virtual ProtoVSBNode *clone() const = 0;

  // position() can only be used after the VSBNode(s) have been created.
  virtual const Coord3D &position() const = 0;
  // Return the direction from this node to the argument, in the
  // reference orientation for this node's signature.
  VoxelEdgeDirection getReferenceDir(const ProtoVSBNode*) const;

  virtual void print(std::ostream&) const = 0;
};

std::ostream &operator<<(std::ostream&, const ProtoVSBNode&);

#ifndef DEBUG
#define checkDir(x) /* */
#endif // DEBUG

// Intermediate ProtoVSBNode classes.  SingleNode is a ProtoVSBNode
// that isn't split into multiple VSBNodes.  DoubleNode is split into
// two VSBNodes.  TripleNode is split into three.

class SingleNode : public ProtoVSBNode {
protected:
  VSBNode *vsbNode;
public:
  SingleNode(const VoxRot &rot)
    : ProtoVSBNode(rot),
      vsbNode(nullptr)
  {}
  virtual void makeVSBNodes(VoxelSetBoundary*, const ICoord3D &here);
  virtual const Coord3D &position() const;
};

class DoubleNode : public ProtoVSBNode {
protected:
  VSBNode *vsbNode0, *vsbNode1;
public:
  DoubleNode(const VoxRot &rot)
    : ProtoVSBNode(rot),
      vsbNode0(nullptr), vsbNode1(nullptr)
  {}
  virtual void makeVSBNodes(VoxelSetBoundary*, const ICoord3D &here);
  virtual const Coord3D &position() const;
};

class TripleNode : public ProtoVSBNode {
protected:
  VSBNode *vsbNode0, *vsbNode1, *vsbNode2;
public:
  TripleNode(const VoxRot &rot)
    : ProtoVSBNode(rot),
      vsbNode0(nullptr), vsbNode1(nullptr), vsbNode2(nullptr)
  {}
  virtual void makeVSBNodes(VoxelSetBoundary*, const ICoord3D &here);
  virtual const Coord3D &position() const;
};

class MultiNode : public ProtoVSBNode {
  // For more than three, give up on writing them out explicitly;
protected:
  std::vector<VSBNode*> vsbNodes;
public:
  MultiNode(unsigned int n, const VoxRot &rot)
    : ProtoVSBNode(rot),
      vsbNodes(n, nullptr)
  {}
  virtual void makeVSBNodes(VoxelSetBoundary*, const ICoord3D &here);
  virtual const Coord3D &position() const;
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class VSBNode {
 private:
  double distance;		// distance to clipping plane
  bool trimmed;
  std::vector<VSBNode*> neighbors;
 public:
  const Coord3D position;
  VSBNode(const Coord3D &p)
    : trimmed(false), neighbors(3, nullptr), position(p)
  {}
  VSBNode(const ICoord3D &p)
    : trimmed(false), neighbors(3, nullptr), position(p.coord())
  {}
  void setNeighbor(unsigned int i, VSBNode *nbr);
  VSBNode *getNeighbor(unsigned int i) const { return neighbors[i]; }
  void replaceNeighbor(VSBNode*, VSBNode*);
  bool checkNeighborCount() const;
  friend class VoxelSetBoundary;
};


class VSBGraph {
 private:
  std::vector<VSBNode*> vertices; // maybe a std::set instead?
 public:
  VSBGraph() {}
  ~VSBGraph();
  // Copying a graph is difficult because the nodes' neighbor pointers
  // would all need to be rebuilt.  We shouldn't ever need to a copy a
  // graph, though.  Just forbid it.
  VSBGraph(const VSBGraph&) = delete;
  // TODO: Do we need a move constructor?
  VSBGraph(const VSBGraph&&) = delete;

  unsigned int size() const { return vertices.size(); }
  
  void addNode(VSBNode *node) { vertices.push_back(node); }
  const VSBNode *getNode(unsigned int i) const { return vertices[i]; }
  // VSBGraph *copyAndClip(const Plane*) const;
  // void clipInPlace(const Plane*);

  double volume() const;
  bool verify() const;
};

class VSBEdgeIterator {
private:
  const VSBGraph *graph;
  unsigned int ihere;
  unsigned int inbr;
  bool finished;
public:
  VSBEdgeIterator(const VSBGraph *g);
  bool done() const { return finished; }
  const VSBNode *node0() const;
  const VSBNode *node1() const;
  void next();
};


class VoxelSetBoundary {
private:
  const unsigned int category;
  ICRectangularPrism *bounds;
  const CMicrostructure *microstructure;
  VSBGraph graph;
  // Some two fold nodes are created during the graph building process
  // and need to be fixed later.  They're stored here:
  std::set<VSBNode*> twoFoldNodes;
public:
  VoxelSetBoundary(const CMicrostructure *ms, unsigned int cat)
    : category(cat),
      bounds(nullptr),
      microstructure(ms)
  {}
  ~VoxelSetBoundary();
  ProtoVSBNode *protoVSBNodeFactory(unsigned char, const ICoord3D&);
  void addNode(VSBNode *node) { graph.addNode(node); }
  void addEdge(const ICoord3D&, const ICoord3D&);
  // void find_boundaries();
  void twoFoldNode(VSBNode*);
  void fixTwoFoldNodes();

  unsigned int size() const { return graph.size(); }

  VSBEdgeIterator iterator() const { return VSBEdgeIterator(&graph); }

  bool verify() const { return graph.verify(); }
  
  // friend class SingleNode;
  // friend class DoubleNode;
  // friend class TripleNode;
  // friend class MultiNode;
  // friend class ThreeTwoOne;
  // friend class FiveTwoOne;
};

void initializeProtoNodes();

#endif // VOXELSETBOUNDARY_H
