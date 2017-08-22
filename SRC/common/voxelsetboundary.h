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
#include "common/geometry.h"
class CMicrostructure;
class COrientedPlane;
class LineSegmentLayer;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Predefined voxel signatures for the 8 individual voxels.
extern unsigned char vox000, vox100, vox010, vox110,
  vox001, vox101, vox011, vox111;

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
  // Compare the positions of two points in this direction.  Return 1
  // if the first point is past the second point, -1 if it's the other
  // way around, and 0 if they're at the same position.
  int compare(const ICoord3D&, const ICoord3D&) const;
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
#ifdef DEBUG
  mutable unsigned char signature;
#endif // DEBUG
public:
  const VoxRot rotation;
  ProtoVSBNode(const VoxRot &rot);
  virtual ~ProtoVSBNode() {}
#ifdef DEBUG
  void setSignature(unsigned char sig) const { signature = sig;}
#endif // DEBUG
  
  // Pure virtual methods in this class are defined in subclasses
  // defined in voxelsetboundary.C.

  // makeVSBNodes constructs the VSBnodes and puts them in the graph,
  // but doesn't connect them.
  virtual void makeVSBNodes(VSBGraph*, const ICoord3D&) = 0;
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

#ifdef DEBUG
  virtual void print(std::ostream&) const = 0;
#endif // DEBUG
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
  virtual void makeVSBNodes(VSBGraph*, const ICoord3D&);
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
  virtual void makeVSBNodes(VSBGraph*, const ICoord3D&);
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
  virtual void makeVSBNodes(VSBGraph*, const ICoord3D&);
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
  virtual void makeVSBNodes(VSBGraph*, const ICoord3D&);
  virtual const Coord3D &position() const;
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class VSBNode {
 private:
  unsigned int index;		// set by VSBGraph::addNode
  // TODONT: Changing this to VSBNode *neighbors[3] provided no
  // noticable speed up, although profiling indicates that a lot of
  // time is spent in the VSBNode constructor.
  std::vector<VSBNode*> neighbors;
 public:
  const Coord3D position;
  VSBNode(const Coord3D &p);
  VSBNode(const ICoord3D &p);
  ~VSBNode();
  VSBNode(const VSBNode&) = delete;
  VSBNode(const VSBNode&&) = delete;
  void setNeighbor(unsigned int i, VSBNode *nbr);
  VSBNode *getNeighbor(unsigned int i) { return neighbors[i]; }
  const VSBNode *getNeighbor(unsigned int i) const { return neighbors[i]; }
  void replaceNeighbor(VSBNode*, VSBNode*);
  void replaceNeighbor(unsigned int i, VSBNode *nbr) { neighbors[i] = nbr; }
  
  VSBNode *nextCWNeighbor(const VSBNode*);
  const VSBNode *nextCWNeighbor(const VSBNode*) const;
  unsigned int neighborIndex(const VSBNode*) const;
  unsigned int getIndex() const { return index; }

  bool degenerateNeighbor(const VSBNode*) const;
  
  friend class VoxelSetBoundary;
  friend class VSBGraph;
};

std::ostream &operator<<(std::ostream&, const VSBNode&);


class VSBGraph {
 private:
  std::vector<VSBNode*> vertices;
  void connectClippedNodes(const std::vector<VSBNode*>&) const;
  std::vector<double> getDistances(const COrientedPlane&, double&, double&)
    const;
  // bounds is the actual extent of the graph.  domain is the region
  // of Microstructure that the graph was built from.  It may be
  // bigger than the actual extent.
  CRectangularPrism bounds;
  ICRectangularPrism domain;
  // Some two fold nodes are created during the graph building process
  // and need to be fixed later.  They're stored here:
  std::set<VSBNode*> twoFoldNodes;
 public:
  VSBGraph(const ICRectangularPrism &subregion);
  ~VSBGraph();
  VSBGraph(const VSBGraph&);
  // TODO: Do we need a move constructor?
  VSBGraph(const VSBGraph&&) = delete;

  unsigned int size() const { return vertices.size(); }
  bool empty() const { return vertices.empty(); }
  
  void addNode(VSBNode *node);
  void addNodes(const std::vector<VSBNode*>&);
  const VSBNode *getNode(unsigned int i) const { return vertices[i]; }
  void twoFoldNode(VSBNode*);
  void fixTwoFoldNodes();
  std::vector<VSBNode*> removeDegenerateFaces(std::vector<VSBNode*>&) const;

  VSBGraph *copyAndClip(const COrientedPlane&) const;
  void clipInPlace(const COrientedPlane&);

  double volume() const;
  Coord3D center() const;
  const CRectangularPrism &bbox() const { return bounds; }
  
  bool checkEdges() const;
  bool checkConnectivity(unsigned int nRegions, const ICRectangularPrism&)
    const;
  void dump(std::ostream &) const;
  void dumpLines(std::ostream&, const CMicrostructure*) const;
  void draw(LineSegmentLayer*, const CMicrostructure*) const;
};

class VSBEdgeIterator {
private:
  const VoxelSetBoundary *vsb;
  unsigned int igraph;
  unsigned int ihere;
  unsigned int inbr;
  bool finished;
public:
  VSBEdgeIterator(const VoxelSetBoundary*);
  bool done() const { return finished; }
  const VSBNode *node0() const;
  const VSBNode *node1() const;
  void next();
};


class VoxelSetBoundary {
private:
  const unsigned int category;
  const CMicrostructure *microstructure;
  // There's one VSBGraph for each subregion in the CMicrostructure. 
  std::vector<VSBGraph> graphs;
  CRectangularPrism *bbox_;
public:
  VoxelSetBoundary(const CMicrostructure *ms, unsigned int cat);
  ProtoVSBNode *protoVSBNodeFactory(unsigned int, unsigned char,
				    const ICoord3D&);
  void addEdge(const ICoord3D&, const ICoord3D&);
  void fixTwoFoldNodes(unsigned int s) { graphs[s].fixTwoFoldNodes(); }
  // void find_boundaries();

  unsigned int size() const;
  double volume() const;
  void findBBox();
  const CRectangularPrism &bounds() const { return *bbox_; }

  double clippedVolume(const CRectangularPrism&,
		       const std::vector<COrientedPlane>&,
		       bool checkTopology) const;

  VSBEdgeIterator iterator() const { return VSBEdgeIterator(this); }

  bool checkEdges() const;
  bool checkConnectivity(unsigned int) const;
  void dump(std::ostream &os) const;
  void dumpLines(const std::string&) const;
  void saveClippedVSB(const std::vector<COrientedPlane>&,
		      const std::string&) const;
  void drawClippedVSB(const std::vector<COrientedPlane>&,
		      LineSegmentLayer*) const;

  friend class VSBEdgeIterator;
};

void initializeProtoNodes();

void printHomogRegionStats();
std::string &printSig(unsigned char);

#ifdef DEBUG
void setVerboseVSB(bool);
#endif // DEBUG

#endif // VOXELSETBOUNDARY_H
