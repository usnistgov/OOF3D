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
#include <map>

class VSBGraph;
class VSBNode;

#include "common/coord.h"

class VoxelEdgeDirection {
public:
  VoxelEdgeDirection(unsigned int a, int d);
  unsigned int axis;		// 0, 1, or 2
  int dir;			// 1 or -1
  VoxelEdgeDirection reverse() const;
};

extern const VoxelEdgeDirection posX, negX, posY, negY, posZ, negZ;

class VoxelRotation {
private:
  std::vector<VoxelEdgeDirection> dirs;
public:
  VoxelRotation(VoxelEdgeDirection, VoxelEdgeDirection, VoxelEdgeDirection);
  VoxelEdgeDirection map(VoxelEdgeDirection &d) const;
};

class VSBNode {
 private:
  double distance;		// distance to clipping plane
  bool trimmed;
  std::vector<VSBNode*> neighbors;
 public:
  const Coord3D position;
  VSBNode(const Coord3D &p)
    : trimmed(false),
      position(p)
  {}
  void addNeighbor(VSBNode *n) { neighbors.push_back(n); }
  VSBNode *getNeighbor(int i) const { return neighbors[i]; }
  VSBNode *getNeighbor(VoxelEdgeDirection) const;
  unsigned int getNeighborIndex(VoxelEdgeDirection) const;
  void replaceNeighbor(VSBNode*, VSBNode*);
  void replaceNeighbor(unsigned int, VSBNode*);
  void removeNeighbor(VSBNode*);
  // VSBNode *removeNeighbor(unsigned int);
  void switchNeighbors();
  int nNeighbors() const { return neighbors->size(); }
  void ensureClockwise(const VSBNode*, const VSBNode*, const VSBNode*);
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
  
  void addNode(VSBNode *node) { vertices.push_back(node); }
  VSBGraph *copyAndClip(const Plane*) const;
  void clipInPlace(const Plane*);

  double volume() const;
};

typedef std::map<ICoord3D, VSBNode*> ProtoGraph;

class VoxelSetBoundary {
private:
  const unsigne int category;
  ICRectangularPrism *bounds;
  const CMicrostructure *microstructure;
  ProtoGraph protoGraph;	// used when constructing the graph
  VSBGraph *graph;
public:
  VoxelSetBoundary(const CMicrostructure *ms, unsigned int cat)
    : category(cat),
      bounds(nullptr),
      microstructure(ms)
  {}
  ~VoxelSetBoundary();
  void addEdge(const ICoord3D&, const ICoord3D&);
  void find_boundaries();
};

#endif // VOXELSETBOUNDARY_H
