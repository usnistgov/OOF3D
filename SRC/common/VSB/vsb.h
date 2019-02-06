// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Classes for computing the intersection of a set of voxels with a
// convex polyhedron.  Derived from the OOF3D code, but independent of
// it.

// Externally visible template arguments:
//  COORD: a class representing a 3D coordinate with float components
//  with member functions
//         COORD(double, double, double)          constructor
//         double COORD::operator[](int) const    read a component
//         double & COORD:operator[](int)         read/write a component
//         COORD &operator+=(const COORD&)        vector addition in place
//  and non-member functions
//         double dot(const COORD&, const COORD&) dot product
//         COORD cross(const COORD&, const COORD&) cross product
//         COORD operator+(const COORD&, const COORD&) vector addition
//         COORD operator*(const COORD&, double)       scalar multiplication
//         COORD operator/(const COORD&, double)       scalar division

// ICOORD: a class representing a 3D coordinate with integer components
// with member functions
//         ICOORD(int, int, int)                 constructor
//         int ICOORD::operator[](int) const     read a component
//         int & ICOORD::operator[](int)         read/write a component

#ifndef VSB_H
#define VSB_H

#include <fstream>
#include <set>
#include <vector>

#include "cprism.h"
#include "cplane.h"

#define swap(x, y) { auto temp = (x); x = (y); y = temp; }

template <class COORD, class ICOORD> class ProtoVSBNode;
template <class VOXELSETBOUNDARY> class VSBEdgeIterator;
template <class COORD, class ICOORD> class VSBGraph;
template <class COORD, class ICOORD> class VSBNode;
template <class COORD, class ICOORD, class IMAGEVAL> class VoxelSetBdy;

template<class COORD, class ICOORD>
  ProtoVSBNode<COORD, ICOORD> *fetchProtoNode(unsigned char);

// A lot of classes here all need to define the same typedefs.
// typedefs in a template class's base class don't seem to be visible
// to the derived class.
#define TEMPLATE_TYPEDEFS \
  typedef VSBNode<COORD, ICOORD> Node; \
  typedef ProtoVSBNode<COORD, ICOORD> ProtoNode; \
  typedef VSBGraph<COORD, ICOORD> Graph;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Predefined voxel signatures for the 8 individual voxels.
extern unsigned char vox000, vox100, vox010, vox110,
  vox001, vox101, vox011, vox111, voxelALL, voxelNONE;

std::string &printSig(unsigned char);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static int nRegionsUsed = 0;	// For figuring out optimal subregions...
static int nHomogCalcs = 0;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class VoxelEdgeDirection {
public:
  VoxelEdgeDirection(unsigned int a, int d);

  template <class COORD>
  VoxelEdgeDirection(const COORD &vec) {
    // This constructor uses COORD instead of ICOORD because its
    // caller gets positions out of VSBNodes, and those positions can be
    // nonintegers.  When this is used, however, we expect the values to
    // be integers.
    assert((vec[0] != 0 && vec[1] == 0 && vec[2] == 0) ||
	   (vec[0] == 0 && vec[1] != 0 && vec[2] == 0) ||
	   (vec[0] == 0 && vec[1] == 0 && vec[2] != 0));
    for(unsigned int c=0; c<3; c++) {
      if(vec[c] != 0) {
	axis = c;
	dir = (vec[c] > 0 ? 1 : -1);
	return;
      }
    }
  }

  unsigned int axis;		// 0, 1, or 2
  int dir;			// 1 or -1
  VoxelEdgeDirection reverse() const;
  bool operator==(const VoxelEdgeDirection &other) const {
    return axis == other.axis && dir == other.dir;
  }
  
  // Compare the positions of two points in this direction.  Return 1
  // if the first point is past the second point, -1 if it's the other
  // way around, and 0 if they're at the same position.
  template <class ICOORD>
  int compare(const ICOORD &i0, const ICOORD &i1) const {
    int d = (i0[axis] - i1[axis]) * dir;
    return d == 0 ? 0 : (d > 0 ? 1 : -1);
  }

};

extern const VoxelEdgeDirection posX, negX, posY, negY, posZ, negZ;

typedef std::vector<VoxelEdgeDirection> VoxelEdgeList;
extern const VoxelEdgeList allDirs;

std::ostream &operator<<(std::ostream&, const VoxelEdgeDirection&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

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

template <class ICOORD>
ICOORD singleVoxelOffset(unsigned char voxel) {
  // There must be a more elegant way of doing this, but this is
  // probably more efficient.
  if(voxel == vox000)
    return ICOORD(-1, -1, -1);
  if(voxel == vox100)
    return ICOORD(1, -1, -1);
  if(voxel == vox010)
    return ICOORD(-1, 1, -1);
  if(voxel == vox110)
    return ICOORD(1, 1, -1);
  if(voxel == vox001)
    return ICOORD(-1, -1, 1);
  if(voxel == vox101)
    return ICOORD(1, -1, 1);
  if(voxel == vox011)
    return ICOORD(-1, 1, 1);
  if(voxel == vox111)
    return ICOORD(1, 1, 1);
  assert(false);		// bad argument to singleVoxelOffset
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class COORD, class ICOORD>
class ProtoVSBNode {
public:
  typedef ProtoVSBNode<COORD, ICOORD> ProtoNode;
protected:
  // Given two voxels, decide if they're in canonical order or
  // not. The answer is arbitrary, but must be the same for the other
  // ProtoVSBNode that shares the two voxels.  The voxels are
  // specified by the single voxel signatures, which define where they
  // are relative to the center of the current ProtoVSBNode in the
  // reference orientation.  The comparison is made using the *actual*
  // orientation, so that it can be compared to a different
  // ProtoVSBNode's view of the same two voxels.
  bool voxelOrder(unsigned char sig0, unsigned char sig1) const  {
    // Get the positions of the voxels relative to the center of the
    // 2x2x2 cube.
    assert(sig0 != sig1);
    ICOORD v0 = singleVoxelOffset<ICOORD>(sig0);
    ICOORD v1 = singleVoxelOffset<ICOORD>(sig1);
    // Find out which reference direction is the actual space x direction.
    VoxelEdgeDirection xdir = rotation.toReference(posX);
    int cmp = xdir.compare(v0, v1);
    if(cmp != 0)
      return cmp > 0;
  
    // The x components are the same.  Use y instead.
    VoxelEdgeDirection ydir = rotation.toReference(posY);
    cmp = ydir.compare(v0, v1);
    if(cmp != 0)
      return cmp > 0;

    // Use z.
    VoxelEdgeDirection zdir = rotation.toReference(posZ);
    cmp = zdir.compare(v0, v1);
    assert(cmp != 0);
    return cmp > 0;
  } // end ProtoVSBNode::voxelOrder
#ifdef DEBUG
  mutable unsigned char signature;
#endif // DEBUG
public:
  const VoxRot rotation;
  ProtoVSBNode(const VoxRot &rot) : rotation(rot) {}
  virtual ~ProtoVSBNode() {}
#ifdef DEBUG
  void setSignature(unsigned char sig) const { signature = sig;}
#endif // DEBUG
  
  // Pure virtual methods in this class are defined in subclasses
  // defined in voxelsetboundary.C.

  // makeVSBNodes constructs the VSBnodes and puts them in the graph,
  // but doesn't connect them.
  virtual void makeVSBNodes(VSBGraph<COORD, ICOORD>*, const ICOORD&) = 0;
  // connect connects nodes by creating links between VSBNodes in the
  // graph.  
  virtual void connect(ProtoVSBNode<COORD, ICOORD>*) = 0;
  // connectBack tells the node that another node wants to connect.
  // It makes the connection and returns the VSBNode that the other
  // node should connect to.
  virtual VSBNode<COORD, ICOORD> *connectBack(
				      const ProtoVSBNode<COORD, ICOORD>*,
				      VSBNode<COORD, ICOORD>*) = 0;

  // connectDoubleBack connects two nodes in the same direction, in
  // cases in which a split node connects along two coincident edges
  // to another split node. It's only used in some (but not all)
  // DoubleNode and TripleNode subclasses.  The base class method here
  // just raises an exception, because it should never be called.
  // It's defined here so that it doesn't have to be defined
  // separately in all of the DoubleNode and TripleNode classes that
  // *don't* need it.
  virtual void connectDoubleBack(
			 const ProtoVSBNode<COORD, ICOORD>*,
			 VSBNode<COORD, ICOORD>*, VSBNode<COORD, ICOORD>*,
			 VSBNode<COORD, ICOORD>*&, VSBNode<COORD, ICOORD>*&)
  {
    assert(false);
  }

  // connectDirs returns the reference space directions in which
  // neighbors need to be found.
  virtual const VoxelEdgeList &connectDirs() const = 0;
  
#ifdef DEBUG
  void checkDir(const VoxelEdgeDirection &dir) const {
    for(VoxelEdgeDirection allowed : connectDirs()) {
      if(allowed == dir)
	return;
    }
    std::cerr << "ProtoVSBNode::checkDir: this=" << *this
	      << " dir=" << dir << std::endl;
    std::cerr << "ProtoVSBNode::checkDir: connectDirs=" << connectDirs()
	      << std::endl;
    assert(false);
  }
#else
  void checkDir(const VoxelEdgeDirection&) const {
  }
#endif // DEBUG

  virtual ProtoVSBNode<COORD, ICOORD> *clone() const = 0;

  // position() can only be used after the VSBNode(s) have been created.
  virtual const COORD &position() const = 0;
  // Return the direction from this node to the argument, in the
  // reference orientation for this node's signature.
  VoxelEdgeDirection getReferenceDir(const ProtoVSBNode<COORD, ICOORD> *that)
    const
  {
    // Return the direction from this node to that node
    return rotation.toReference(
		VoxelEdgeDirection(that->position() - position()));
  }

#ifdef DEBUG
  virtual void print(std::ostream&) const = 0;
#endif // DEBUG
};     // end template class ProtoVSBNode

template <class COORD, class ICOORD>
std::ostream &operator<<(std::ostream &os,
			 const ProtoVSBNode<COORD, ICOORD> &pnode)
{
  pnode.print(os);
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// VSBNode is an actual node in the graph.  Unlike ProtoVSBNode,
// there's only one kind of VSBNode.  All of its topological
// information is in its connections. 

template <class COORD, class ICOORD>
class VSBNode {
 private:
  unsigned int index;		// set by VSBGraph::addNode
  // TODONT: Changing this to VSBNode *neighbors[3] provided no
  // noticable speed up, although profiling indicates that a lot of
  // time is spent in the VSBNode constructor.
  std::vector<VSBNode<COORD, ICOORD>*> neighbors;
 public:
  const COORD position;
  VSBNode(const COORD &p)
    : neighbors(3, nullptr),
      position(p)
  {}
  VSBNode(const ICOORD &p)
    : neighbors(3, nullptr),
      position(p[0], p[1], p[2])
  {}
  ~VSBNode() {}
  VSBNode(const VSBNode<COORD, ICOORD>&) = delete;
  VSBNode(const VSBNode<COORD, ICOORD>&&) = delete;
  void setNeighbor(unsigned int i, VSBNode<COORD, ICOORD> *nbr)  {
    assert(neighbors[i] == nullptr);
    neighbors[i] = nbr;
  }
  VSBNode *getNeighbor(unsigned int i) {
    return neighbors[i];
  }
  const VSBNode *getNeighbor(unsigned int i) const { return neighbors[i]; }
  void replaceNeighbor(VSBNode<COORD, ICOORD> *oldnode,
		       VSBNode<COORD, ICOORD> *newnode)
  {
    for(unsigned int i=0; i<3; i++) {
      if(neighbors[i] == oldnode) {
	neighbors[i] = newnode;
	return;
      }
    }
    assert(false);		// VSBNode::replaceNeighbor failed
  }
  void replaceNeighbor(unsigned int i, VSBNode<COORD, ICOORD> *nbr) {
    neighbors[i] = nbr;
  }

  // nextCWNeighbor returns the neighbor of this node that follows the
  // given node CW in the neighbor list.  This is where the CW storage
  // ordering of the neighbors is important.  If the initial graph is
  // insufficiently connected, it's possible that a clipped graph has
  // nodes with duplicate neighbors.  In that case, nextCWNeighbor
  // should always return the neighbor that's *not* the argument.
  
  // TODO: Can the result of nextCWNeighbor be computed at graph
  // construction time and cached?

  VSBNode *nextCWNeighbor(const VSBNode<COORD, ICOORD> *nbr) {
    if(neighbors[0] == nbr) {
      return neighbors[1];
    }
    if(neighbors[1] == nbr) {
      return neighbors[2];
    }
    assert(neighbors[2] == nbr);
    return neighbors[0];
  }
  const VSBNode *nextCWNeighbor(const VSBNode<COORD, ICOORD> *nbr) const {
    if(neighbors[0] == nbr) {
      return neighbors[1];
    }
    if(neighbors[1] == nbr) {
      return neighbors[2];
    }
    assert(neighbors[2] == nbr);
    return neighbors[0];
  }

  unsigned int neighborIndex(const VSBNode<COORD, ICOORD> *nbr) const {
    for(unsigned int i=0; i<3; i++)
      if(neighbors[i] == nbr)
	return i;
    assert(false);		// VSBNode::neighborIndex failed
  }

  unsigned int getIndex() const { return index; }

  bool degenerateNeighbor(const VSBNode<COORD, ICOORD> *other) const {
    return (other->neighbors[1] == this && other->neighbors[2] == this &&
	    neighbors[1] == other && neighbors[2] == other);
  }
  friend class VSBGraph<COORD, ICOORD>;
};				// end template class VSBNode

template <class COORD, class ICOORD>
std::ostream &operator<<(std::ostream &os, const VSBNode<COORD, ICOORD> &node) {
  os << "VSBNode(" << node.getIndex() << ", pos=" << node.position
     << ", " << "nbrs=[";
  for(unsigned int i=0; i<3; i++) {
    if(node.getNeighbor(i) == nullptr)
      os << "--";
    else
      os << node.getNeighbor(i)->getIndex();
    if(i < 2)
      os << ",";
  }
  os << "])";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class COORD, class ICOORD>
class VSBGraph {
public:
  typedef VSBNode<COORD, ICOORD> Node;
  typedef VSBPlane<COORD> Plane;
 private:
  std::vector<Node*> vertices;
  // bounds is the actual extent of the graph.  domain is the region
  // of 3D image that the graph was built from.  It may be bigger than
  // the actual extent.
  CRectPrism<COORD> bounds;
  ICRectPrism<ICOORD> domain;
  // Some two fold nodes are created during the graph building process
  // and need to be fixed later.  They're stored here:
  std::set<Node*> twoFoldNodes;

  void connectClippedNodes(const std::vector<Node**>&newNodes)
    const
  {
    // Each node in newNodes has exactly one neighbor, in slot 0.
    // Starting from that neighbor, go from node to node
    // counterclockwise around the hole in the graph to find the next
    // new node, and connect to it.  We know when we've found the next
    // new node because it won't have a neighbor in slot 1.
    for(Node *newNode : newNodes) {
      // #ifdef DEBUG
      //     if(verbose)
      //       std::cerr << "VSBGraph::connectClippedNodes: newNode=" << *newNode
      // 	      << std::endl;
      //     Std::CerrIndent indent(2);
      // #endif // DEBUG
      Node *vcur = newNode;
      Node *vnext = newNode->getNeighbor(0);
      do {
	// To make a counterclockwise turn from one graph edge to
	// another, pick the outgoing edge that's the *clockwise*
	// neighbor of the incoming edge.
	Node *vtemp = vnext->nextCWNeighbor(vcur);
	vcur = vnext;
	vnext = vtemp;
	// #ifdef DEBUG
	//       if(verbose)
	// 	std::cerr << "VSBGraph::connectClippedNodes: vcur=" << *vcur << std::endl;
	// #endif // DEBUG
      } while(vcur->getNeighbor(1) != nullptr);
      vcur->setNeighbor(1, newNode);
      newNode->setNeighbor(2, vcur);
      // #ifdef DEBUG
      //     if(verbose)
      //       std::cerr << "VSBGraph::connectClippedNodes: connected "
      // 	      << *vcur << " " << *newNode << std::endl;
      // #endif // DEBUG
    }
  } // end VSBGraph::connectClippedNodes

  // TODO: getDistances() computes a lot of distances that aren't ever
  // used, especially when clipping with the first face or two of a tet
  // when the graph is still large.  We don't really need to know the
  // distance from a point to the plane unless the point is on an edge
  // that crosses the plane.  Most of the time we just need to know
  // which side of the plane a point is one.
  //
  // (1) Does this calculation take a significant amount of time?
  //
  // (2) Can we create an octree that can quickly tell which side of the
  // plane a point is on, at least for points that are far from the
  // plane?  Is it faster than VSBPlane::distance?  (Powell & Abel
  // suggest splitting volume across longest direction, instead of
  // dividing in 8.  They also say it's not worth the effort unless
  // there are a lot of voxels.)
    
  std::vector<double> getDistances(const Plane &plane,
				   double &dmin, double &dmax)
    const
  {
    std::vector<double> dists;
    dists.reserve(size());
    dmin = std::numeric_limits<double>::max();
    dmax = -std::numeric_limits<double>::max();
    for(const Node *vertex : vertices) {
      double d = plane.distance(vertex->position);
      dists.push_back(d);
      // #ifdef DEBUG
      //     if(verbose)
      //       std::cerr << "getDistances: vertex=" << vertex->index << " "
      // 	      << vertex->position << " " << "d=" << d << std::endl;
      // #endif // DEBUG
      if(d > dmax)
	dmax = d;
      if(d < dmin)
	dmin = d;
    }
    return dists;
  } // end VSBGraph::getDistances
    
 public:
  VSBGraph(const ICRectPrism<ICOORD> &subregion)
    : bounds(COORD(0., 0., 0.), COORD(0., 0., 0.)),
      domain(subregion)
  {}

  ~VSBGraph()  {
    for(Node *node : vertices)
      delete node;
    vertices.clear();
  }

  VSBGraph(const VSBGraph<COORD, ICOORD> &other)
    : bounds(other.bounds)
  {
    vertices.reserve(other.size());
    for(const VSBNode<COORD, ICOORD> *overtex : other.vertices) {
      addNode(new VSBNode<COORD, ICOORD>(overtex->position));
    }
    for(VSBNode<COORD, ICOORD> *vertex : vertices) {
      const VSBNode<COORD, ICOORD> *oldNode
	= other.getNode(vertex->getIndex());
      for(unsigned int i=0; i<3; i++) {
	vertex->setNeighbor(i, vertices[oldNode->getNeighbor(i)->getIndex()]);
      }
    }
  }
    
  VSBGraph(const VSBGraph<COORD, ICOORD>&&) = delete;

  unsigned int size() const {
    return vertices.size();
  }

  bool empty() const {
    return vertices.empty();
  }
  
  void addNode(Node *node) {
    if(vertices.empty())
      bounds = CRectPrism<COORD>(node->position, node->position);
    else
      bounds.swallow(node->position);
    node->index = vertices.size();
    vertices.push_back(node);
  }
  
  void addNodes(const std::vector<Node*> &newNodes) {
    assert(!newNodes.empty());
    unsigned int n = vertices.size();
    if(n == 0) {
      bounds = CRectPrism<COORD>(newNodes[0]->position, newNodes[0]->position);
    }
    for(Node *node : newNodes) {
      node->index = n++;
      bounds.swallow(node->position);
    }
    vertices.insert(vertices.end(), newNodes.begin(), newNodes.end());
  }
  
  const Node *getNode(unsigned int i) const {
    return vertices[i];
  }

  void twoFoldNode(Node *node) {
    twoFoldNodes.insert(node);
  }
  
  void fixTwoFoldNodes() {
    for(Node *node : twoFoldNodes) {
      Node *n0 = node->neighbors[0];
      Node *n1 = node->neighbors[1];
      n0->replaceNeighbor(node, n1);
      n1->replaceNeighbor(node, n0);
      delete node;
    }
    twoFoldNodes.clear();
  }
  
  std::vector<Node*> removeDegenerateFaces(std::vector<Node*> &newNodes)
    const
  {
    // std::cerr << "VSBGraph::removeDegenerateFaces: nNew=" << newNodes.size()
    // 	  << std::endl;
    if(newNodes.empty())
      return newNodes;
    // If the graph isn't 3-vertex connected, clipping can produce a
    // degenerate new face, in which two nodes have two connections to
    // each other, both of which have to be neighbor slots 1 and 2.
    // There can be no change of direction at such nodes, so we can
    // remove the two nodes and connect their other neighbors directly
    // to each other.
    std::vector<bool> removed(newNodes.size(), false); // has node been removed?
    unsigned int nremoved = 0;
    // Loop over pairs of new nodes that haven't yet been removed from newNodes
    for(unsigned int i=0; i<newNodes.size()-1; i++) {
      if(!removed[i]) {
	for(unsigned int j=i+1; j<newNodes.size(); j++) {
	  if(!removed[j]) {
	    if(newNodes[i]->degenerateNeighbor(newNodes[j])) {
	      // The two nodes are multiply connected.  Remove them.
	      Node *oldnbr0 = newNodes[i]->getNeighbor(0);
	      Node *oldnbr1 = newNodes[j]->getNeighbor(0);
	      oldnbr0->replaceNeighbor(newNodes[i], oldnbr1);
	      oldnbr1->replaceNeighbor(newNodes[j], oldnbr0);
	      removed[i] = true;
	      removed[j] = true;
	      nremoved += 2;
	    }
	  }
	}
      }
    }
    // std::cerr << "VSBGraph::removeDegenerateFaces: nremoved=" << nremoved
    // 	  << std::endl;
    if(nremoved == 0)
      return newNodes;
    std::vector<Node*> retained;
    retained.reserve(newNodes.size() - nremoved);
    for(unsigned int k=0; k<newNodes.size(); k++) {
      if(!removed[k])
	retained.push_back(newNodes[k]);
      else
	delete newNodes[k];
    }
    return retained;
  }

  VSBGraph *copyAndClip(const Plane &plane) const {
    // Based loosely on r3d_clip in r3d.c.
    double dmin, dmax;
    std::vector<double> distance = getDistances(plane, dmin, dmax);
    if(dmax < 0) {
      // entire graph is within the clipping region
      return new VSBGraph<COORD, ICOORD>(*this);
    }
    if(dmin > 0) {
      // entire graph is outside the clipping region
      return new VSBGraph<COORD, ICOORD>(domain); // empty graph
    }

    // Copy the nodes that are to be kept, and create new nodes at the
    // clipping plane.
    VSBGraph<COORD, ICOORD> *newGraph = new VSBGraph<COORD, ICOORD>(domain);
    // copies[i] is the node in the new graph that is a copy of the node
    // with index i in the old graph.
    std::vector<Node*> copies(vertices.size(), nullptr);
    unsigned int nCopied = 0;
    std::vector<Node*> danglingNodes;
    // v0 loops through the nodes in the old graph, finding ones that
    // need to be copied.
    for(unsigned int v0=0; v0<vertices.size(); v0++) {
      if(copies[v0]==nullptr && distance[v0] < 0) {
	// Old node v0 needs to be copied to the new graph.  Copy it and
	// its neighbors.  stack stores all the nodes that need to be
	// copied.
	std::vector<const Node*> stack;
	stack.reserve(vertices.size() - nCopied);
	stack.push_back(vertices[v0]);
	while(!stack.empty()) {
	  const Node *oldNode = stack.back();
	  stack.pop_back();

	  // Nodes might be put on the stack multiple times.  Just
	  // ignore the repeats.
	  if(copies[oldNode->getIndex()] != nullptr)
	    continue;

	  double d0 = distance[oldNode->getIndex()]; // negative!
	  Node *newNode = new Node(oldNode->position);
	  copies[oldNode->getIndex()] = newNode;
	  ++nCopied;
	  newGraph->addNode(newNode);
	  for(unsigned int n=0; n<3; n++) { // loop over nbrs of old node
	    // If the neighbor has already been copied, set the neighbor
	    // pointers in the new node and the copy of its neighbor.
	    const Node *oldNbr = oldNode->getNeighbor(n);
	    Node *nbrCopy = copies[oldNbr->getIndex()];
	    if(nbrCopy != nullptr) {
	      newNode->setNeighbor(n, nbrCopy);
	      unsigned int nidx = oldNbr->neighborIndex(oldNode);
	      nbrCopy->setNeighbor(nidx, newNode);
	    }
	    else {
	      // The neighbor hasn't been copied. It should either be
	      // copied or clipped.
	      double nbrDistance = distance[oldNbr->getIndex()];
	      if(nbrDistance < 0) {
		// The neighbor doesn't need to be clipped.  Put it on
		// the stack to be copied.
		stack.push_back(oldNbr);
	      }
	      else {
		// The neighbor has to be clipped.  Create a new node on
		// the edge between here and there.  Remember that d0 is
		// negative when interpolating the position.
		COORD p = ((oldNode->position*nbrDistance - oldNbr->position*d0)
			   / (nbrDistance - d0));
		Node *newNbr = new Node(p);
		danglingNodes.push_back(newNbr);
		// Don't add the new node to the graph yet, since it
		// might be part of a degenerate face.
		newNode->setNeighbor(n, newNbr);
		newNbr->setNeighbor(0, newNode);
	      }
	    } // end if neighbor hasn't been copied
	  } // end loop over neighbors of node being copied
	}	// end while stack is not empty
      } // end if node v0 has to be copied
    } // end loop over node indices v0

    // At this point, newGraph contains all of the nodes from the old
    // graph that are on the correct side of the clipping plane, and a
    // bunch of dangling nodes that are on the clipping plane. Connect
    // the dangling nodes to each other.
    newGraph->connectClippedNodes(danglingNodes);
    std::vector<Node*> keptNodes =
      newGraph->removeDegenerateFaces(danglingNodes);
    if(!keptNodes.empty())
      newGraph->addNodes(keptNodes);
 
    return newGraph;
  } // end VSBGraph::copyAndClip
  
  void clipInPlace(const Plane &plane) {
    // Modeled after r3d_clip, more or less. This is more like it than
    // copyAndClip is.
    // std::cerr << "VSBGraph::clipInPlace" << std::endl;
    double dmin, dmax;
    std::vector<double> distance = getDistances(plane, dmin, dmax);
    // #ifdef DEBUG
    //   if(verbose)
    //     std::cerr << "VSBGraph::clipInPlace: dmin=" << dmin << " dmax=" << dmax
    // 	    << std::endl;
    // #endif // DEBUG
    if(dmax < 0) {
      // Entire graph is within the clipping region.  There's nothing to do.
      return;
    }
    if(dmin > 0) {
      // The entire graph is outside the clipping region.  Delete all
      // nodes.
      for(Node *node : vertices)
	delete node;
      vertices.clear();
      return;
    }

    std::vector<Node*> newNodes;
    for(unsigned int v0=0; v0<vertices.size(); v0++) {
      if(distance[v0] < 0) {	// keep this vertex
	Node *thisvert = vertices[v0];
	double d0 = distance[v0];		// negative!
	for(unsigned int n=0; n<3; n++) { // loop over neighbors
	  const Node *nbr = thisvert->getNeighbor(n);
	  double d1 = distance[nbr->getIndex()];
	  if(d1 >= 0) {
	    // The neighbor needs to be clipped.
	    COORD p = (thisvert->position*d1 - nbr->position*d0)/(d1 - d0);
	    // #ifdef DEBUG
	    // 	  if(verbose) {
	    // 	    std::cerr << "VSBGraph::clipInPlace: clipping! thisvert=" << *thisvert
	    // 		    << " nbr=" << *nbr << std::endl;
	    // 	  }
	    // #endif // DEBUG
	    Node *newNode = new Node(p);
	    newNodes.push_back(newNode);
	    thisvert->replaceNeighbor(n, newNode);
	    newNode->setNeighbor(0, thisvert);
	    // #ifdef DEBUG
	    // 	  if(verbose) {
	    // 	    std::cerr << "VSBGraph::clipInPlace: newNode=" << *newNode
	    // 		    << std::endl;
	    // 	    std::cerr << "VSBGraph::clipInPlace: after clipping, thisvert="
	    // 		    << *thisvert << std::endl;
	    // 	  }
	    // #endif // DEBUG
	  }
	}	// end loop over neighbors n of v0
      } // end if v0 is being kept
    } // end loop over vertices v0

    // std::cerr << "VSBGraph::clipInPlace: clipped" << std::endl;
    // Connect the new nodes to one another.
    connectClippedNodes(newNodes);
    // std::cerr << "VSBGraph::clipInPlace: connected" << std::endl;
    std::vector<Node*> realNewNodes = removeDegenerateFaces(newNodes);
    // std::cerr << "VSBGraph::clipInPlace: removed degenerate" << std::endl;

    // Delete the nodes that were removed.  This invalidates
    // VSBNode::index for each node.
    unsigned int nkept = 0;
    for(unsigned int v0=0; v0<vertices.size(); v0++) {
      if(distance[v0] >= 0)
	delete vertices[v0];
      else
	vertices[nkept++] = vertices[v0];
    }
    vertices.resize(nkept);
    // std::cerr << "VSBGraph::clipInPlace: removed" << std::endl;
    // Fix VSBNode::index for the retained nodes.
    for(unsigned int i=0; i<vertices.size(); i++) {
      vertices[i]->index = i;
    }
    // Add the new nodes to the graph.
    if(!realNewNodes.empty())
      addNodes(realNewNodes);
  } // end VSBGraph::clipInPlace

  double volume() const {
    // Based on r3d_reduce.  Compute the volume of the polyhedron by
    // splitting each face into triangles, and computing the volume of
    // the each tet formed by a triangle and the center of the
    // polyhedron.
 
    if(empty())
      return 0.0;
    COORD cntr = center();
    double vol = 0.0;
    // emarks[node][nbr] indicates which edges have been used.
    std::vector<std::vector<bool>> emarks(vertices.size(),
					  {false, false, false});
    // Find an unused edge.
    for(unsigned int vstart=0; vstart<vertices.size(); vstart++) {
      for(unsigned int pstart=0; pstart<3; pstart++) {
	if(!emarks[vstart][pstart]) {
	  // Found an unused edge.  Follow the sequence of neighbors
	  // around a facet, using the starting point and a segment of
	  // the perimeter to define a triangular portion of the facet.
	  const Node *startNode = vertices[vstart];
	  COORD startPt = startNode->position;
	  // cur and prev are the endpoints of a segment of the
	  // perimeter.  Their initial values *don't* contribute to the
	  // area, because prev==startPt.
	  const Node *prev = startNode;
	  const Node *cur = startNode->getNeighbor(pstart);
	  emarks[vstart][pstart] = true;
	  bool done = false;
	  do {
	    // Go to next pair
	    const Node *next = cur->nextCWNeighbor(prev);
	    prev = cur;
	    cur = next;
	    // If the graph includes doubly connected edges (which can
	    // happen when a non-3-vertex connected graph is clipped)
	    // then it's unclear which of the two edges we are
	    // traversing, and emarks may already be set.

	  
	  
	    // #ifdef DEBUG
	    // 	  if(emarks[prev->index][prev->neighborIndex(cur)]) {
	    // 	    std::cerr << "VSBGraph::volume: attempt to reuse an edge!"
	    // 		    << std::endl;
	    // 	    std::cerr << "VSBGraph::volume: startNode=" << *startNode
	    // 		    << " prev=" << *prev << " cur=" << *cur << std::endl;
	    // 	    throw ErrProgrammingError("VSBGraph::volume failed!", __FILE__,
	    // 				      __LINE__);
	    // 	  }
	    // #endif // DEBUG
	    emarks[prev->index][prev->neighborIndex(cur)] = true;
	    if(cur == startNode) {
	      done = true;
	    }
	    else {
	      double dv = dot(
			      cross(prev->position-startPt, cur->position-startPt),
			      startPt-cntr);
	      vol += dv;
	    }
	  } while(!done);
	
	}
      } // end loop over pstart
    } // end loop over vstart
    return vol/6.;       // factors of 1/2 from area and 1/3 from volume
  }		       // end VSBGraph::volume
  
  COORD center() const {
    COORD ctr;
    for(Node *vertex : vertices)
      ctr += vertex->position;
    return ctr/vertices.size();
  }
  
  const CRectPrism<COORD> &bbox() const { return bounds; }
  
  bool checkEdges() const  {
    bool result = true;
    for(const Node *vertex : vertices) {
      for(unsigned int n=0; n<3; n++) {
	const Node *nbr = vertex->getNeighbor(n);
	if(nbr == nullptr) {
	  std::cerr << "VSBGraph::checkEdges: missing neighbor " << n
		    << " for vertex " << vertex->index << " "
		    << vertex->position << std::endl;
	  result = false;
	}
      }
      for(unsigned int n=0; n<3; n++) {
	const Node *nbr = vertex->getNeighbor(n);
	if(nbr == vertex->getNeighbor((n+1)%3)) {
	  result = false;
	  std::cerr << "VSBGraph::checkEdges: node "
		    << vertex->index << " " << vertex->position
		    << " has non-unique neighbors " << nbr->index << " "
		    << nbr->position << std::endl;
	}
	bool ok = false;
	for(unsigned int i=0; i<3; i++) {
	  if(nbr->getNeighbor(i) == vertex) {
	    ok = true;
	    break;
	  }
	}
	if(!ok) {
	  result = false;
	  std::cerr << "VSBGraph::checkEdges: node "
		    << nbr->index << " " << nbr->position
		    << " is a neighbor of node " << vertex->index
		    << " " << vertex->position << " but not vice versa."
		    << std::endl;
	}
      }
    }
    // std::cerr << "VSBGraph::checkEdges: ok!" << std::endl;
    return result;
  } // end VSBGraph::checkEdges
  
  // checkConnectivity divides the graph into disjoint regions and
  // checks that each region is three-vertex connected.  A "region" is
  // a set of nodes that are connected to each other (maybe
  // indirectly) and not connected to any nodes outside the region.  A
  // three-fold connected region is one that can't be divided into two
  // regions by removing two nodes.  This test is at least o(N^2) and
  // is based on the C routine r3d_is_good() in r3d.c

  // Return false if three-node connectivity is not present.  If
  // nRegions is positive and not equal to the number of regions, also
  // return false.

  // ** checkConnectivity only applies to convex polygons. **

  bool checkConnectivity() const {
    // First find the regions.  region[i] is nullptr if node i hasn't
    // yet been assigned to a region.
    bool ok = true;
    typedef std::set<const Node*> Region;
    std::set<Region*> regions;
    std::vector<Region*> region(vertices.size(), nullptr);
    for(const Node *start : vertices) {
      if(region[start->index] == nullptr) {
	// This vertex isn't in a region.  Start a new region.
	Region *reg = new Region();
	regions.insert(reg);
	std::vector<const Node*> stack;
	stack.reserve(vertices.size());
	stack.push_back(start);
	while(!stack.empty()) {
	  const Node *v = stack.back();
	  stack.pop_back();
	  if(region[v->index] == nullptr) {
	    reg->insert(v);
	    region[v->index] = reg;
	    stack.push_back(v->getNeighbor(0));
	    stack.push_back(v->getNeighbor(1));
	    stack.push_back(v->getNeighbor(2));
	  }
	}
	if(reg->size() < 3) {
	  std::cerr << "VSBGraph::checkConnectivity: region is too small! size="
		    << reg->size() << std::endl;
	  return false;
	}
      } // end if vertex "start" isn't in a region.
    }   // end loop over vertices "start"
    // Loop over pairs of vertices in the same region, and check that
    // removing them doesn't divide the region into two.
    for(Region *reg : regions) {
      bool okreg = true;		// region is ok
      for(typename Region::iterator ia=reg->begin(); ia!=reg->end() && okreg;
	  ++ia)
	{
	  const Node *nodeA = *ia;
	  typename Region::iterator ib = ia;
	  ib++;
	  for(; ib!=reg->end() && okreg; ++ib) {
	    const Node *nodeB = *ib;
	    // Find a point nodeC that's not nodeA or nodeB, and check
	    // that all nodes in the region can be reached from it. We
	    // know that the region size is greater than 2, so nodeC must
	    // exist.
	    typename Region::iterator ic = reg->begin(); // pointer to nodeC
	    while(*ic == nodeA || *ic == nodeB)
	      ic++;
	    // Put all nodes reachable from nodeC into the visited region.
	    // Put nodeA and nodeB in the region too, so that they won't
	    // be used.
	    Region visited;
	    visited.insert(nodeA);
	    visited.insert(nodeB);
	    // Use "stack" to loop over all neighbors and neighbors of
	    // neighbors, etc.
	    std::vector<const Node*> stack;
	    stack.reserve(vertices.size());
	    stack.push_back(*ic);
	    while(!stack.empty()) {
	      const Node *v = stack.back();
	      stack.pop_back();
	      // Try to put the node in "visited".
	      auto insrt = visited.insert(v);
	      if(insrt.second) { // v was not already in "visited"
		// Put v's neighbors on the stack, to be examined later.
		stack.push_back(v->getNeighbor(0));
		stack.push_back(v->getNeighbor(1));
		stack.push_back(v->getNeighbor(2));
	      }
	    } // end while stack is not empty
	    if(visited.size() != reg->size()) {
	      std::cerr << "VSBGraph::checkConnectivity:"
			<< " region is insufficiently connected!" << std::endl;
	      std::cerr << "VSBGraph::checkConnectivity: nodeA=" << *nodeA
			<< " nodeB=" << *nodeB << std::endl;
	      // for(const VSBNode *node : *reg) {
	      //   std::cerr << "VSBGraph::checkConnectivity: index=" << node->index
	      // 	    << " position=" << node->position
	      // 	    << " nbrs=[" << node->getNeighbor(0)->index << ", "
	      // 	    << node->getNeighbor(1)->index << ", "
	      // 	    << node->getNeighbor(2)->index << "]";
	      //   if(node == nodeA)
	      //     std::cerr << " A";
	      //   else if(node == nodeB)
	      //     std::cerr << " B";
	      //   std::cerr << std::endl;
	      // }
	      okreg = false;	// go to next region
	      ok = false;
	    }
	  }	// end loop over Region, nodeB
	} // end loop over Region, nodeA
    }
  
    for(Region *reg : regions)
      delete reg;
    return ok;
  } // end VSBGraph::checkConnectivity

    
  // Write out the graph structure
  void dump(std::ostream &os) const {
    for(const Node *vertex : vertices) {
      os << "Vertex " << vertex->index << " " << vertex->position;
      os << "   nbrs=";
      for(Node *nbr : vertex->neighbors) {
	if(nbr)
	  os << nbr->index << " ";
	else
	  os << "(0x0)  ";
      }
      os << std::endl;
    }
  }

  // Write out the edges in a plottable form
  void dumpLines(std::ostream &os, COORD (*converter)(const COORD&)) const {
    for(const Node *vertex : vertices) {
      for(Node *nbr : vertex->neighbors) {
	if(nbr && vertex->index < nbr->index)
	  os << (*converter)(vertex->position) << ", "
	     << (*converter)(nbr->position) << " # "
	     << vertex->index << " " << nbr->index << std::endl;
      }
    }
  }
  // void draw(LineSegmentLayer*, const CMicrostructure*) const;

};				// end template class VSBGraph


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// VSBEdgeIterator can be used to loop over the edges of a clipped
// voxel set boundary, for debugging and graphics.
// Use it like this:
//    VSBEdgeIterator<Coord, ICoord> iter = vsb->iterator();
//    while(!iter.done()) {
//      Coord pt0 = iter.node0()->position;
//      Coord pt1 = iter.node1()->position;
//      ...
//      iter.next()
//    }

template <class VOXELSETBOUNDARY>
class VSBEdgeIterator {
private:
  const VOXELSETBOUNDARY *vsb;
  unsigned int igraph;
  unsigned int ihere;
  unsigned int inbr;
  bool finished;
public:
  VSBEdgeIterator(const VOXELSETBOUNDARY *vsb)
    : vsb(vsb),
      igraph(0),
      ihere(0),
      inbr(0),
      finished(false)
  {
    if(vsb->graphs.empty())
      finished = true;
  }
  bool done() const { return finished; }

  const typename VOXELSETBOUNDARY::Node *node0() const {
    return vsb->graphs[igraph].getNode(ihere);
  }

  const typename VOXELSETBOUNDARY::Node *node1() const {
    return vsb->graphs[igraph].getNode(ihere)->getNeighbor(inbr);
  }

  void next() {
    if(inbr < 2) {
      inbr++;
      return;
    }
    // nbr == 2
    inbr = 0;
    ihere++;
    if(ihere == vsb->graphs[igraph].size()) {
      igraph++;
      if(igraph == vsb->graphs.size()) {
	finished = true;
	return;
      }
      ihere = 0;
    }
  }
};				// end template class VSBEdgeIterator

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class COORD, class ICOORD, class IMAGEVAL>
class VoxelSetBdy {
public:
  typedef ProtoVSBNode<COORD, ICOORD> ProtoNode;
  typedef VSBNode<COORD, ICOORD> Node;
  typedef VSBGraph<COORD, ICOORD> Graph;
  typedef VSBPlane<COORD> Plane;
  typedef IMAGEVAL ImageVal;
private:
  const unsigned int category;	// for debugging only
  //  const CMicrostructure *microstructure;
  const double voxelVolume;	// volume of a single voxel
  // There's one VSBGraph for each subregion in the image. 
  std::vector<Graph> graphs;
  CRectPrism<COORD> *bbox_;
public:
  // First constructor arg is the size of a single voxel in physical
  // units.  It used to be a pointer to a CMicrostructure, which was
  // only used to get the volume of the voxel.
  VoxelSetBdy(double voxVol,
	      const std::vector<ICRectPrism<ICOORD>> &subregions,
	      const IMAGEVAL &cat)
    : category(cat),
      voxelVolume(voxVol),
      bbox_(nullptr)
  {
    graphs.reserve(subregions.size());
    for(unsigned int s=0; s<subregions.size(); s++)
      graphs.emplace_back(subregions[s]);
  }

  // protoVSBNodeFactory converts a signature (2x2x2 set of bools
  // stored as a char) to a type of ProtoVSBNode and a VoxRot.  To do
  // that, it clones the ProtoVSBNode that's in the protoNodeTable for
  // that signature.

  ProtoNode *protoVSBNodeFactory(unsigned int subregionNo,
				 unsigned char signature,
				 const ICOORD &here)
  {
    const ProtoNode *prototype = fetchProtoNode<COORD, ICOORD>(signature);
    if(prototype == nullptr)
      return nullptr;
    ProtoNode *protoNode = prototype->clone();
#ifdef DEBUG
    protoNode->setSignature(signature);
#endif // DEBUG
    protoNode->makeVSBNodes(&graphs[subregionNo], here);
    return protoNode;
  }

  void fixTwoFoldNodes(unsigned int s) {
    graphs[s].fixTwoFoldNodes();
  }

  unsigned int size() const {
    unsigned int sz = 0;
    for(unsigned int i=0; i<graphs.size(); i++)
      sz += graphs[i].size();
    return sz;
  }

  double volume() const {
    double vol = 0.0;
    for(const Graph &graph : graphs)
      vol += graph.volume();
    return vol * voxelVolume;    
  }

  void findBBox() {
    for(unsigned int i=0; i<graphs.size(); i++) {
      if(!graphs[i].empty()) {
	bbox_ = new CRectPrism<COORD>(graphs[i].bbox());
	for(unsigned int j=i+1; j<graphs.size(); j++)
	  if(!graphs[j].empty())
	    bbox_->swallowPrism(graphs[j].bbox());
	return;
      }
    }
  }
  
  const CRectPrism<COORD> &bounds() const {
    return *bbox_;
  }

  // VoxelSetBdy::clippedVolume is the core of the element
  // homogeneity calculation.  In OOF3D, it's called by
  // CSkeletonElement::categoryVolumes().
  double clippedVolume(const std::vector<ICRectPrism<ICOORD>> &bins,
		       const CRectPrism<COORD> &ebbox,
		       const std::vector<Plane> &planes)
    const
  {
    assert(!planes.empty());
    double vol = 0.0;
    // TODO: Instead of looping over all bins, compute which bins to
    // use, since we know their sizes.  Or perhaps use an octree
    // structure for the bins so that we can find the bins containing
    // the corners of the element bounding box quickly, and then examine
    // only the bins between the corners.
    for(unsigned int s=0; s<bins.size(); s++) { // loop over bins
      if(!graphs[s].empty() && bins[s].intersects(ebbox)) {
	++nRegionsUsed;
	Graph *clippedGraph = graphs[s].copyAndClip(planes[0]);
	for(unsigned i=1; i<planes.size(); i++) {
	  clippedGraph->clipInPlace(planes[i]);
	}
	vol += clippedGraph->volume();
	delete clippedGraph;
      } // end if graph intersects elements
    }   // end loop over bins s
    ++nHomogCalcs;
    return vol;
  } // end VoxelSetBdy::clippedVolume

  VSBEdgeIterator<VoxelSetBdy<COORD, ICOORD, IMAGEVAL>> iterator() const {
    return VSBEdgeIterator<VoxelSetBdy<COORD, ICOORD, IMAGEVAL>>(this);
  }

  bool checkEdges() const {
    bool ok = true;
    for(const Graph &graph : graphs)
      ok &= graph.checkEdges();
    return ok;
  }

  bool checkConnectivity() const {
    bool ok = true;
    for(const Graph &graph : graphs) {
      bool regionOk = graph.checkConnectivity();
      ok &= regionOk;
    }
    return ok;
  }
  
  void dump(std::ostream &os, const std::vector<ICRectPrism<ICOORD>>&) const;
  void dumpLines(const std::string&) const;

  void saveClippedVSB(const std::vector<Plane> &planes,
		      COORD (*converter)(const COORD&),
		      const std::string &filenamebase) const
  {
    std::ofstream f(filenamebase+".dat");
    std::ofstream f2(filenamebase+".lines");
    for(const Graph &graph : graphs) {
      Graph *clippedGraph = graph.copyAndClip(planes[0]);
      for(unsigned i=1; i<planes.size(); i++) {
	clippedGraph->clipInPlace(planes[i]);
      }
      clippedGraph->dump(f);
      clippedGraph->dumpLines(f2, converter);
      delete clippedGraph;
    }
    f.close();
    f2.close();
  }
  
  //  friend class VSBEdgeIterator<COORD, ICOORD>;
};				// end template class VoxelSetBdy

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Intermediate ProtoVSBNode classes.  SingleNode is a ProtoVSBNode
// that isn't split into multiple VSBNodes.  DoubleNode is split into
// two VSBNodes.  TripleNode is split into three.  MultiNode is split
// into more than three.

template <class COORD, class ICOORD>
class SingleNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
protected:
  Node *vsbNode;
public:
  SingleNode(const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNode(nullptr)
  {}
  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    vsbNode = new Node(here);
    graph->addNode(vsbNode);
  }
  virtual const COORD &position() const {
    assert(vsbNode != nullptr);
    return vsbNode->position;
  }
};

template <class COORD, class ICOORD>
class DoubleNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
protected:
  Node *vsbNode0, *vsbNode1;
public:
  DoubleNode(const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNode0(nullptr), vsbNode1(nullptr)
  {}
  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    vsbNode0 = new Node(here);
    vsbNode1 = new Node(here);
    graph->addNode(vsbNode0);
    graph->addNode(vsbNode1);
  }
  virtual const COORD &position() const {
    assert(vsbNode0 != nullptr);
    return vsbNode0->position;
  }
};

template <class COORD, class ICOORD>
class TripleNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
protected:
  Node *vsbNode0, *vsbNode1, *vsbNode2;
public:
  TripleNode(const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNode0(nullptr), vsbNode1(nullptr), vsbNode2(nullptr)
  {}
  virtual void makeVSBNodes(VSBGraph<COORD, ICOORD> *graph,
			    const ICOORD &here)
  {
    vsbNode0 = new Node(here);
    vsbNode1 = new Node(here);
    vsbNode2 = new Node(here);
    graph->addNode(vsbNode0);
    graph->addNode(vsbNode1);
    graph->addNode(vsbNode2);
  }
  virtual const COORD &position() const {
    assert(vsbNode0 != nullptr);
    return vsbNode0->position;
  }
};

template <class COORD, class ICOORD>
class MultiNode : public ProtoVSBNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  // For more than three, give up on writing them out explicitly;
protected:
  std::vector<Node*> vsbNodes;
public:
  MultiNode(unsigned int n, const VoxRot &rot)
    : ProtoVSBNode<COORD, ICOORD>(rot),
      vsbNodes(n, nullptr)
  {}
  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    for(unsigned int i=0; i<vsbNodes.size(); i++) {
      vsbNodes[i] = new Node(here);
      graph->addNode(vsbNodes[i]);
    }
  }
  virtual const COORD &position() const {
    assert(vsbNodes[0] != nullptr);
    return vsbNodes[0]->position;
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Concrete subclasses of ProtoVSBNode


// For a node at the corner of a single voxel, the reference
// configuration in the 2x2x2 cube has the voxel in the +x, +y, +z
// corner (vox111) and the neighbors in the +x, +y, +z directions.

template <class COORD, class ICOORD>
class SingleVoxel : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SingleVoxel(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new SingleVoxel<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    // The neighbors are in the +x, +y, and +z directions, so
    // inserting them in the neighbor list in that order puts them
    // CW when viewed from outside (from the -x, -y, -z side).
    this->vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SingleVoxel(" << printSig(this->signature) << ", " << this->rotation
       << ")";
  }
#endif // DEBUG
};
 
//--------

// Seven voxels are just like one, except the "outside" is on the
// other side.  The only difference between SevenVoxels and
// SingleVoxel is that we need to ensure that the order of the +xyz
// axes is CCW, so the args to ensureClockwise are in a different
// order.

template <class COORD, class ICOORD>
class SevenVoxels : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SevenVoxels(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new SevenVoxels<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    // The neighbors are in the +x, +y, and +z directions, but
    // inserting them in the neighbor list in otherproto order would puts
    // them CCW when viewed from outside (from the +x, +y, +z side).
    // They're supposed to be CW, so switch 0 and 2.
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SevenVoxels(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};

//--------

// Two voxels that share an edge.

template <class COORD, class ICOORD>
class TwoVoxelsByEdge : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  TwoVoxelsByEdge(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new TwoVoxelsByEdge<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    // The reference configuration is vox000 + vox110.  There are
    // edges in the posX, negX, posY, negY, and negZ directions.
    static const VoxelEdgeList v({posX, negX, posY, negY, negZ});
    return v;
  }

  /*
                 posZ  ^        ^  posY
                       |       /
                       |      /
                       |      
                            +--------+        The edges coming in to the 
                           /        /|        central vertex (X) are labeled 
                         0/        / |        with their neighbor indices.
                     1   /  1     /  |
    negX <---  ---------X--------+   +   --> posX
              /        /|        |  /
             /       0/ |2       | /
            /        /  |        |/ vox110
           +--------+   +--------+
           |        |  / 
           |        | /  
    vox000 |        |/   |
           +--------+    |
                         V negZ
                         
   */

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The edges of vox000 connect to vsbNode0 and the edges of
    // vox110 to vsbNode1.  vox000's edges are negY, negX, negZ, in
    // that order (CW as viewed from outside (from +x+y+z).
    // Similarly, vox110's edges are posY, posX, negZ.
    if(dir == negX || dir == negY) {
      // Connect to vox000's edges, using vsbNode0.
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      // Since dir.axis is 0 or 1, 1-dir.axis gives us the order we want.
      this->vsbNode0->setNeighbor(1-dir.axis, othernode); 
    }
    else if(dir == posX || dir == posY) {
      // Connect to vox110's edges, using vsbNode1.
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(1-dir.axis, othernode);
    }
    else {
      // Both vsbNode0 and vsbNode1 connect in the negZ direction
      // along a doubled edge.  We need to ensure that the two split
      // nodes at the far end of the edge are connected to the
      // corresponding split nodes here.  If we think of the split
      // nodes as being separated slightly, we need to connect two
      // nodes that are separated in the same direction.

      // voxelOrder takes two voxels (assumed to be neighbors) and
      // returns a geometrically deduced bool.  If the voxels at the
      // other end of a doubled edge have the same relative position,
      // then voxelOrder will return the same bool for them.  When
      // connecting to split nodes, passing the nodes to
      // connectDoubleBack in the order in which voxelOrder is true
      // will guarantee that the connection is done correctly.
      assert(dir == negZ);
      bool ordered = this->voxelOrder(vox000, vox110);
      Node *othernode0, *othernode1;
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX || dir == negY) {
      this->vsbNode0->setNeighbor(1-dir.axis, othernode);
      return this->vsbNode0;
    }
    if(dir == posX || dir == posY) {
      this->vsbNode1->setNeighbor(1-dir.axis, othernode);
      return this->vsbNode1;
    }
    assert(false); // "Unexpected direction in TwoVoxelsByEdge::connectBack!",
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox000, vox110);
    node0 = ordered ? this->vsbNode0 : this->vsbNode1;
    node1 = ordered ? this->vsbNode1 : this->vsbNode0;
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByEdge(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};  // end class TwoVoxelsByEdge

//-------------

// Two voxels that touch at a corner.

template <class COORD, class ICOORD>
class TwoVoxelsByCorner : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  TwoVoxelsByCorner(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new TwoVoxelsByCorner<COORD, ICOORD>(this->rotation);}

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }
  
  virtual void connect(ProtoNode *otherproto) {
    // TwoVoxelsByCorner is easier than TwoVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 connect to vsbNode0, and
    // the edges on vox111 connect to vsbNode1.  There's no
    // consistency to maintain at the other end of a doubled edge.
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      // The edges around vox000 in CW order when viewed from +x+y+z
      // are negZ, negY, negX. 
      this->vsbNode0->setNeighbor(2-dir.axis, othernode);
    }
    else {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      // The edges around vox111 in CW order when viewed from -x-y-z
      // are posX, posY, pozY.
      this->vsbNode1->setNeighbor(dir.axis, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {
      this->vsbNode0->setNeighbor(2-dir.axis, othernode);
      return this->vsbNode0;
    }
    this->vsbNode1->setNeighbor(dir.axis, othernode);
    return this->vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByCorner(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};	// end class TwoVoxelsByCorner

//--------

// SixVoxelsByEdge is the inverse of TwoVoxelsByEdge

template <class COORD, class ICOORD>
class SixVoxelsByEdge : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SixVoxelsByEdge(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new SixVoxelsByEdge<COORD, ICOORD>(this->rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    // The reference configuration all voxels *except* vox000 and
    // vox110.  There are edges in the posX, negX, posY, negY, and
    // negZ directions.
    static const VoxelEdgeList v({posX, negX, posY, negY, negZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The edges on vox100 connect to vsbNode0 and the edges on vox010
    // connect to vsbNode1.  Edges on vox100 are posX, negY, negZ.
    // Edges on vox010 are negX, posY, negZ.
    if(dir == posX || dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(dir.axis, othernode); 
    }
    else if(dir == negX || dir == posY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(dir.axis, othernode);
    }
    else {
      assert(dir == negZ);
      bool ordered = this->voxelOrder(vox100, vox010);
      Node *othernode0, *othernode1;
      Node *node0 = ordered? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posX || dir == negY) {
      this->vsbNode0->setNeighbor(dir.axis, othernode);
      return this->vsbNode0;
    }
    else if(dir == negX || dir == posY) {
      this->vsbNode1->setNeighbor(dir.axis, othernode);
      return this->vsbNode1;
    }
    assert(false); // Unexpected direction in SixVoxelsByEdge::connectBack!
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox100, vox010);
    node0 = ordered ? this->vsbNode0 : this->vsbNode1;
    node1 = ordered ? this->vsbNode1 : this->vsbNode0;
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByEdge(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};  // end class SixVoxelsByEdge

//--------

// SixVoxelsByCorner is the inverse of TwoVoxelsByCorner

template <class COORD, class ICOORD>
class SixVoxelsByCorner : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  SixVoxelsByCorner(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}
  virtual ProtoNode *clone() const {
    return new SixVoxelsByCorner<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoNode *otherproto) {
    // SixVoxelsByCorner is easier than SixVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 (which is a hole) connect
    // to vsbNode0, and the edges on vox111 (also a hole) connect to
    // vsbNode1.  There's no consistency to maintain at the other end
    // of a doubled edge.
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      // The edges around vox000 in CW order when viewed from -x-y-z
      // are negX, negY, negZ. 
      this->vsbNode0->setNeighbor(dir.axis, othernode);
    }
    else {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      // The edges around vox111 in CW order when viewed from +x+y+z
      // are posZ, posY, pozX.
      this->vsbNode1->setNeighbor(2-dir.axis, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir.dir == -1) {
      this->vsbNode0->setNeighbor(dir.axis, othernode);
      return this->vsbNode0;
    }
    this->vsbNode1->setNeighbor(2-dir.axis, othernode);
    return this->vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByCorner(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end SixVoxelsByCorner

//----------

// Three voxels in an L configuration.  The node does not need to be
// split.  The reference configuration is vox000, vox100,
// vox010, with edges posX, posY, negZ in that order.

template <class COORD, class ICOORD>
class ThreeVoxL : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ThreeVoxL(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new ThreeVoxL<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    this->vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxL(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end ThreeVoxL

// ----------

// FiveVoxL is the inverse of ThreeVoxL.  The connections are
// the same, but the order is reversed.

template <class COORD, class ICOORD>
class FiveVoxL : public SingleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FiveVoxL(const VoxRot &rot)
    : SingleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new FiveVoxL<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNode);
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    this->vsbNode->setNeighbor(2-dir.axis, othernode);
    return this->vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxL(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end FiveVoxL

//---------

// ThreeTwoOne is three voxels, two stacked face to face and a third
// connected to one of the other two along an edge.  There are 24
// orientations.  The reference configuration contains voxels 000,
// 111, and 110.

template <class COORD, class ICOORD>
class ThreeTwoOne : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ThreeTwoOne(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}
  
  virtual ProtoNode *clone() const {
    return new ThreeTwoOne<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(Graph *graph, const ICOORD &here) {
    this->vsbNode0 = new Node(here);
    this->vsbNode1 = new Node(here);
    graph->addNode(this->vsbNode0);
    graph->twoFoldNode(this->vsbNode1);
    // Don't add vsbNode1 to the graph! It's not a real node.
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // See comments in TwoVoxelsByEdge.  This is similar, but the
    // edges on vox110 are different, and its VSBNode will only be
    // connected to two edges, so we have to tell the VSB about it.
    // VSBNode0 is the 3-fold node, with edges on vox000 in the negX,
    // negY, and negZ directions.  VSBNode1 is the 2-fold node, on
    // vox110 and vox111, with edges negZ and posZ.
    
    if(dir == negX || dir == negY) {
      // Connecting to the edges on vox000
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(1-dir.axis, othernode);
    }
    else if(dir==posZ) {
      // Connecting to the edges on vox110
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.  To ensure compatibility
      // with the other ends of edge, use voxelOrder to determine the
      // order of the input and output args to connectDoubleBack.
      assert(dir == negZ);
      bool ordered = this->voxelOrder(vox000, vox110);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNode0->setNeighbor(2, othernode0);
      this->vsbNode1->setNeighbor(1, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX || dir == negY) {
      this->vsbNode0->setNeighbor(1-dir.axis, othernode);
      return this->vsbNode0;
    }
    if(dir == posZ) {
      this->vsbNode1->setNeighbor(0, othernode);
      return this->vsbNode1;
    }
    std::cerr << "Unexpected direction in ThreeTwoOne::connectBack!"
	      << std::endl;
    assert(false);
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox000, vox110);
    if(ordered) {
      node0 = this->vsbNode0;
      node1 = this->vsbNode1;
      this->vsbNode0->setNeighbor(2, othernode0);
      this->vsbNode1->setNeighbor(1, othernode1);
    }
    else {
      node0 = this->vsbNode1;
      node1 = this->vsbNode0;
      this->vsbNode0->setNeighbor(2, othernode1);
      this->vsbNode1->setNeighbor(1, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeTwoOne(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end class ThreeTwoOne

//---------

// FiveTwoOne is the inverse of ThreeTwoOne.  The reference
// configuration contains all voxels except vox000, vox111, and
// vox110.  That means that vox100 and vox010 touch along an edge.
// The case is treated completely differently from ThreeTwoOne,
// because it's not possible to resolve the doubled edge in a unique
// way.  So here we add an extra (third) node and avoid a doubled
// edge.  It's not possible to resolve ThreeTwoOne in this way because
// it would lead to an insufficiently connected graph.

template <class COORD, class ICOORD>
class FiveTwoOne : public TripleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FiveTwoOne(const VoxRot &rot)
    : TripleNode<COORD, ICOORD>(rot)
  {
  }
  
  virtual ProtoNode *clone() const {
    return new FiveTwoOne<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(Graph *graph, const ICOORD &here) {
    TripleNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    this->vsbNode0->setNeighbor(2, this->vsbNode2);
    this->vsbNode1->setNeighbor(1, this->vsbNode2);
    this->vsbNode2->setNeighbor(2, this->vsbNode0);
    this->vsbNode2->setNeighbor(1, this->vsbNode1);
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // vsbNode0 connects the negY, negZ edges of vox100 and vsbNode1
    // connects the negX, negZ edges of vox010.  Both also connect to
    // vsbNode2, which connects the posZ edge as well.
    
    if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir==posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode2);
      this->vsbNode2->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.
      assert(dir == negZ);
      bool ordered = this->voxelOrder(vox100, vox010);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNode0->setNeighbor(1, othernode0);
      this->vsbNode1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX) {
      this->vsbNode1->setNeighbor(0, othernode);
      return this->vsbNode1;
    }
    if(dir == negY) {
      this->vsbNode0->setNeighbor(0, othernode);
      return this->vsbNode0;
    }
    if(dir == posZ) {
      this->vsbNode2->setNeighbor(0, othernode);
      return this->vsbNode2;
    }
    assert(false);  // Unexpected direction in FiveTwoOne::connectBack
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = this->voxelOrder(vox100, vox010);
    if(ordered) {
      node0 = this->vsbNode0;
      node1 = this->vsbNode1;
      this->vsbNode0->setNeighbor(1, othernode0);
      this->vsbNode1->setNeighbor(2, othernode1);
    }
    else {
      node0 = this->vsbNode1;
      node1 = this->vsbNode0;
      this->vsbNode0->setNeighbor(1, othernode1);
      this->vsbNode1->setNeighbor(2, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveTwoOne(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};				// end class FiveTwoOne

//--------

// Three voxels that each share an edge with both of the others.  

template <class COORD, class ICOORD>
class ThreeVoxByEdges : public TripleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ThreeVoxByEdges(const VoxRot &rot)
    : TripleNode<COORD, ICOORD>(rot)
  {}

  virtual ProtoNode *clone() const {
    return new ThreeVoxByEdges<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The reference configuration is vox110 + vox011 + vox101.
    // There are doubled edges in the +x, +y, and +z directions and
    // single edges in the -x, -y, and -z directions.  We use vsbNode0
    // for the edges of vox110, vsbNode1 for 101, and vsbNode2 for
    // 011.
    if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode2);
      this->vsbNode2->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox110 (vsbNode0) and vox101 (vsbNode1)
      bool ordered = this->voxelOrder(vox110, vox101);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // The edges on vsbNode0 (vox110) are (negZ, posY, posX),
      // CW.  This is posX, so it goes in slot 2.
      this->vsbNode0->setNeighbor(2, othernode0);
      // The edges on vsbNode1 (vox101) are (negY, posX, posZ),
      // CW.  This is posX, so it goes in slot 1.
      this->vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox110 (vsbNode0) and vox011 (vsbNode2)
      bool ordered = this->voxelOrder(vox110, vox011);
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode2;
      Node *node1 = ordered ? this->vsbNode2 : this->vsbNode0;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negZ, posY, posX).
      this->vsbNode0->setNeighbor(1, othernode0);
      // Edges are (negX, posZ, posY)
      this->vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox101 (vsbNode1) and vox011 (vsbNode2)
      bool ordered = this->voxelOrder(vox101, vox011);
      Node *node0 = ordered ? this->vsbNode1 : this->vsbNode2;
      Node *node1 = ordered ? this->vsbNode2 : this->vsbNode1;
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negY, posX, posZ)
      this->vsbNode1->setNeighbor(2, othernode0);
      // Edges are (negX, posZ, posY)
      this->vsbNode2->setNeighbor(1, othernode1);
    }
  } // end connect()

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX) {
      this->vsbNode2->setNeighbor(0, othernode);
      return this->vsbNode2;
    }
    if(dir == negY) {
      this->vsbNode1->setNeighbor(0, othernode);
      return this->vsbNode1;
    }
    if(dir == negZ) {
      this->vsbNode0->setNeighbor(0, othernode);
      return this->vsbNode0;
    }
    std::cerr << "Unexpected direction in ThreeVoxByEdges::connectBack!"
	      << std::endl;
    assert(false);
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox110, vox101);
      node0 = this->vsbNode0;
      node1 = this->vsbNode1;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNode0->setNeighbor(2, othernode0);
      this->vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      bool ordered = this->voxelOrder(vox110, vox011);
      node0 = this->vsbNode0;
      node1 = this->vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNode0->setNeighbor(1, othernode0);
      this->vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = this->voxelOrder(vox101, vox011);
      node0 = this->vsbNode1;
      node1 = this->vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNode1->setNeighbor(2, othernode0);
      this->vsbNode2->setNeighbor(1, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxByEdges(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};				// end class ThreeVoxByEdges

//-----------

// FiveVoxByEdges is the inverse of ThreeVoxByEdges, but has to be
// treated more like Pyramid with an extra voxel.  The reference
// configuration is all voxels except vox110, vox011, and vox101.

template <class COORD, class ICOORD>
class FiveVoxByEdges : public MultiNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FiveVoxByEdges(const VoxRot &rot)
    : MultiNode<COORD, ICOORD>(7, rot)
  {}

  virtual ProtoNode *clone() const {
    return new FiveVoxByEdges<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    MultiNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    for(unsigned int i=0; i<6; i++) {
      // Same as Pyramid::makeVSBNodes()
      this->vsbNodes[i]->setNeighbor(2, this->vsbNodes[(i+5)%6]);
      this->vsbNodes[i]->setNeighbor(1, this->vsbNodes[(i+1)%6]);
    }
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // The reference configuration is ~(vox110|vox011|vox101).  There
    // are doubled edges in the +x, +y, and +z directions and single
    // edges in the -x, -y, and -z directions.  Nodes vsbNodes[0]
    // through vsbNodes[5] form an infinitesimal hexagon at the
    // junction of voxels 100, 001, and 010.  vsbNodes[6] links the
    // edges of vox111, which are coincident the the +x, +y, and +z
    // edges of the other voxels.
    if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNodes[3]);
      this->vsbNodes[3]->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      Node *othernode = otherproto->connectBack(this, this->vsbNodes[1]);
      this->vsbNodes[1]->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNodes[5]);
      this->vsbNodes[5]->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox100 and vox111
      bool ordered = this->voxelOrder(vox100, vox111);
      Node *node0 = ordered ? this->vsbNodes[0] : this->vsbNodes[6];
      Node *node1 = ordered ? this->vsbNodes[6] : this->vsbNodes[0];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox010 and vox111
      bool ordered = this->voxelOrder(vox010, vox111);
      Node *node0 = ordered ? this->vsbNodes[4] : this->vsbNodes[6];
      Node *node1 = ordered ? this->vsbNodes[6] : this->vsbNodes[4];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[4]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox001 and vox111
      bool ordered = this->voxelOrder(vox001, vox111);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[6];
      Node *node1 = ordered ? this->vsbNodes[6] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(2, othernode1);
    }
  } // end connect()

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == negX) {
      this->vsbNodes[3]->setNeighbor(0, othernode);
      return this->vsbNodes[3];
    }
    if(dir == negY) {
      this->vsbNodes[1]->setNeighbor(0, othernode);
      return this->vsbNodes[1];
    }
    if(dir == negZ) {
      this->vsbNodes[5]->setNeighbor(0, othernode);
      return this->vsbNodes[5];
    }
    std::cerr << "Unexpected direction in FiveVoxByEdges::connectBack!"
	      << std::endl;
    assert(false);
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      node0 = this->vsbNodes[0];
      node1 = this->vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      bool ordered = this->voxelOrder(vox010, vox111);
      node0 = this->vsbNodes[4];
      node1 = this->vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[4]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = this->voxelOrder(vox001, vox111);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[6]->setNeighbor(2, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxByEdges(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};				// end FiveVoxByEdges

//--------------

// Four voxels in the shape of two perpendicular stacks of two voxels.
// This configuration is chiral and requires an additional node to be
// created, although there are no multiply connected edges.

template <class COORD, class ICOORD>
class ChiralR : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ChiralR(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new ChiralR<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    DoubleNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    this->vsbNode0->setNeighbor(0, this->vsbNode1);
    this->vsbNode1->setNeighbor(0, this->vsbNode0);
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // Connect posX and negZ to vsbNode0, and negX and posZ to vsbNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // vsbNode0's CW edges are [dummy], negZ, posX.
    // vsbNode1's CW edges are [dummy], negX, posZ.
    // The order of the edges is the reverse of the order in ChiralL.
    if(dir == posX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(2, othernode);
    }
    else if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(1, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posX) {
      this->vsbNode0->setNeighbor(2, othernode);
      return this->vsbNode0;
    }
    if(dir == negX) {
      this->vsbNode1->setNeighbor(1, othernode);
      return this->vsbNode1;
    }
    if(dir == posZ) {
      this->vsbNode1->setNeighbor(2, othernode);
      return this->vsbNode1;
    }
    if(dir == negZ) {
      this->vsbNode0->setNeighbor(1, othernode);
      return this->vsbNode0;
    }
    std::cerr << "Unexpected direction in ChiralR::connectBack!" << std::endl;
    assert(false);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralR(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end ChiralR

//--------------

// The mirror image of ChiralR is ChiralL

template <class COORD, class ICOORD>
class ChiralL : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  ChiralL(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new ChiralL<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    DoubleNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    this->vsbNode0->setNeighbor(0, this->vsbNode1);
    this->vsbNode1->setNeighbor(0, this->vsbNode0);
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    // Connect posX and negZ to vsbNode0, and negX and posZ to vsbNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // vsbNode0's CW edges are [dummy], posX, negZ.
    // vsbNode1's CW edges are [dummy], posZ, negX.
    // The order of the edges is the reverse of the order in ChiralR.
    if(dir == posX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(1, othernode);
    }
    else if(dir == negX) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(2, othernode);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posX) {
      this->vsbNode0->setNeighbor(1, othernode);
      return this->vsbNode0;
    }
    if(dir == negX) {
      this->vsbNode1->setNeighbor(2, othernode);
      return this->vsbNode1;
    }
    if(dir == posZ) {
      this->vsbNode1->setNeighbor(1, othernode);
      return this->vsbNode1;
    }
    if(dir == negZ) {
      this->vsbNode0->setNeighbor(2, othernode);
      return this->vsbNode0;
    }
    assert(false);    // Unexpected direction in ChiralL::connectBack
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralL(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end ChiralL

//------------

// The Pyramid is 4 voxels stacked in a sort of skewed pyramid.  It
// contains one central voxel and the voxels on each of its faces.  An
// infinitesimal hexagonal face is inserted in the corner to convert
// the 6-fold vertex into 6 3-fold vertices.

template <class COORD, class ICOORD>
class Pyramid : public MultiNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  Pyramid(const VoxRot &rot)
    : MultiNode<COORD, ICOORD>(6, rot)
  {}

  virtual ProtoNode *clone() const {
    return new Pyramid<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void makeVSBNodes(Graph *graph, const ICOORD &here) {
    MultiNode<COORD, ICOORD>::makeVSBNodes(graph, here);
    for(unsigned int i=0; i<6; i++) {
      // Neighbor 1 is the previous node in the hexagonal face.
      this->vsbNodes[i]->setNeighbor(1, this->vsbNodes[(i+5)%6]);
      // Neighbor 2 is the next node in the hexagonal face.
      this->vsbNodes[i]->setNeighbor(2, this->vsbNodes[(i+1)%6]);
    }
  }

  // hexDirIndex maps the directions to the nodes of the hexagon.  The
  // edge in direction dir intersects the hexagon at
  // vsbNodes[hexDirIndex(dir)].
  unsigned int hexDirIndex(const VoxelEdgeDirection &dir) const {
    if(dir == posX)
      return 0;
    if(dir == negZ)
      return 1;
    if(dir == posY)
      return 2;
    if(dir == negX)
      return 3;
    if(dir == posZ)
      return 4;
    assert(dir == negY);
    return 5;
  }

  virtual void connect(ProtoNode *otherproto) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    Node *othernode = otherproto->connectBack(this, this->vsbNodes[i]);
    this->vsbNodes[i]->setNeighbor(0, othernode);
  }

  virtual Node *connectBack(const ProtoNode *otherproto, Node *othernode) {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    this->vsbNodes[i]->setNeighbor(0, othernode);
    return this->vsbNodes[i];
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "Pyramid(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end Pyramid

//----------

// Four voxels arranged in a checkerboard pattern, each sharing an
// edge with all of the others.  Each edge becomes a split edge, and
// there's one VSBNode for the inside corner of each voxel.

template <class COORD, class ICOORD>
class CheckerBoard : public MultiNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  CheckerBoard(const VoxRot &rot)
    : MultiNode<COORD, ICOORD>(4, rot)
  {}

  ProtoNode *clone() const {
    return new CheckerBoard<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoNode *otherproto) {
    // The reference configuration is vox100 + vox010 + vox001 +
    // vox111.  Use VSBnodes[0] for vox100, 1 for vox010, 2 for
    // vox001, and 3 for vox111.  The assignment of neighbor indices
    // for the VSBNodes is arbitrary but consistent (and gets them all
    // CW, hopefully!)
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      // The posX edge is between voxels 100 and 111, so it connects
      // to vsbNodes 0 and 3.
      bool ordered = this->voxelOrder(vox100, vox111);
      Node *node0 = ordered ? this->vsbNodes[0] : this->vsbNodes[3];
      Node *node1 = ordered ? this->vsbNodes[3] : this->vsbNodes[0];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      // negX is between voxels 001 and 010, connecting to vsbNodes 2
      // and 1.
      bool ordered = this->voxelOrder(vox001, vox010);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[1];
      Node *node1 = ordered ? this->vsbNodes[1] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(1, othernode0);
      this->vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      // posY is between voxels 010 and 111, connecting to vsbNodes 1
      // and 3.
      bool ordered = this->voxelOrder(vox010, vox111);
      Node *node0 = ordered ? this->vsbNodes[1] : this->vsbNodes[3];
      Node *node1 = ordered ? this->vsbNodes[3] : this->vsbNodes[1];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[1]->setNeighbor(1, othernode0);
      this->vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      // negY is between voxels 001 and 100, connecting to vsbNodes 2
      // and 0.
      bool ordered = this->voxelOrder(vox001, vox100);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[0];
      Node *node1 = ordered ? this->vsbNodes[0] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(2, othernode0);
      this->vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // posZ is between voxels 001 and 111, connecting to vsbNodes 2
      // and 3.
      bool ordered = this->voxelOrder(vox001, vox111);
      Node *node0 = ordered ? this->vsbNodes[2] : this->vsbNodes[3];
      Node *node1 = ordered ? this->vsbNodes[3] : this->vsbNodes[2];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      // negZ is between voxels 100 and 010, connecting to vsbNodes 0
      // and 1.
      bool ordered = this->voxelOrder(vox100, vox010);
      Node *node0 = ordered ? this->vsbNodes[0] : this->vsbNodes[1];
      Node *node1 = ordered ? this->vsbNodes[1] : this->vsbNodes[0];
      Node *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      this->vsbNodes[0]->setNeighbor(2, othernode0);
      this->vsbNodes[1]->setNeighbor(2, othernode1);
    }
  } // end CheckerBoard::connect

  virtual Node *connectBack(const ProtoNode*, Node*) {
    assert(false);  // CheckerBoard::connectBack should not be called!
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    // See comments in CheckerBoard::connect.
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      node0 = this->vsbNodes[0];
      node1 = this->vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[0]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      bool ordered = this->voxelOrder(vox001, vox010);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(1, othernode0);
      this->vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      bool ordered = this->voxelOrder(vox010, vox111);
      node0 = this->vsbNodes[1];
      node1 = this->vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[1]->setNeighbor(1, othernode0);
      this->vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      bool ordered = this->voxelOrder(vox001, vox100);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[0];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(2, othernode0);
      this->vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = this->voxelOrder(vox001, vox111);
      node0 = this->vsbNodes[2];
      node1 = this->vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[2]->setNeighbor(0, othernode0);
      this->vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      bool ordered = this->voxelOrder(vox100, vox010);
      node0 = this->vsbNodes[0];
      node1 = this->vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      this->vsbNodes[0]->setNeighbor(2, othernode0);
      this->vsbNodes[1]->setNeighbor(2, othernode1);
    }
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "CheckerBoard(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};     // end CheckerBoard

//-------------

// FourThreeOne is three voxels in an L with one more voxel out of the
// plane of the L and over the gap.

template <class COORD, class ICOORD>
class FourThreeOne : public DoubleNode<COORD, ICOORD> {
public:
  TEMPLATE_TYPEDEFS;
  
  FourThreeOne(const VoxRot &rot)
    : DoubleNode<COORD, ICOORD>(rot)
  {}

  ProtoNode *clone() const {
    return new FourThreeOne<COORD, ICOORD>(this->rotation);
  }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ, negZ});
    return v;
  }

  virtual void connect(ProtoNode *otherproto) {
    // The reference configuration is three voxels in the Z=0 plane,
    // vox000, vox100 and vox010, just like ThreeVoxL, plus one voxel
    // at vox111.  The three in the L are connected to vsbNode0 and
    // the single voxel is connected to vsbNode1.  The edges in the
    // posX and posY directions are doubled.

    // Neighbor indexing for the edges of the single voxel at vox111
    // is posZ, posX, posY.  For the inside corner of the L it's negZ,
    // posX, posY.
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    this->checkDir(dir);
    if(dir == posZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode1);
      this->vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      Node *othernode = otherproto->connectBack(this, this->vsbNode0);
      this->vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      Node *othernode0, *othernode1;
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      // Conveniently the posX and posY neighbor indexing is the same
      // for both nodes.
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else {
      assert(dir == posY);
      bool ordered = this->voxelOrder(vox010, vox111);
      Node *othernode0, *othernode1;
      Node *node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      Node *node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual Node *connectBack(const ProtoNode *otherproto,
			       Node *othernode)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posZ) {
      this->vsbNode1->setNeighbor(0, othernode);
      return this->vsbNode1;
    }
    if(dir == negZ) {
      this->vsbNode0->setNeighbor(0, othernode);
      return this->vsbNode0;
    }
    assert(false); // Unexpected direction in FourThreeOne::connectBack
  }

  virtual void connectDoubleBack(const ProtoNode *otherproto,
				 Node *othernode0, Node *othernode1,
				 Node *&node0, Node *&node1)
  {
    VoxelEdgeDirection dir = this->getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = this->voxelOrder(vox100, vox111);
      node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      bool ordered = this->voxelOrder(vox010, vox111);
      node0 = ordered ? this->vsbNode0 : this->vsbNode1;
      node1 = ordered ? this->vsbNode1 : this->vsbNode0;
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
    assert(false); // Unexpected direction in FourThreeOne::connectDoubleBack
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FourThreeOne(" << printSig(this->signature) << ", "
       << this->rotation << ")";
  }
#endif // DEBUG
};	// end FourThreeOne

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Build the table of ProtoNode classes

template <class COORD, class ICOORD>
std::vector<ProtoVSBNode<COORD, ICOORD>*> &getProtoNodeTable() {
  static std::vector<ProtoVSBNode<COORD, ICOORD>*> table(256, nullptr);
  return table;
}

template <class COORD, class ICOORD>
ProtoVSBNode<COORD, ICOORD> *fetchProtoNode(unsigned char signature) {
  return getProtoNodeTable<COORD, ICOORD>()[signature];
}


template <class COORD, class ICOORD>
void pn(unsigned char signature, ProtoVSBNode<COORD, ICOORD> *protoNode)
{
  assert(protoNode != nullptr);
#ifdef DEBUG
  protoNode->setSignature(signature);
  if(getProtoNodeTable<COORD, ICOORD>()[signature] != nullptr) {
    std::cerr << "Duplicate signature! " << signature << " "
	    << printSig(signature) << std::endl;
    assert(false);
  }
#endif // DEBUG
  getProtoNodeTable<COORD, ICOORD>()[signature] = protoNode;
}

// This version is for voxel configurations that don't create a
// vertex.  The template arguments have to be given explicitly when
// this is used.
template <class COORD, class ICOORD>
void pn(unsigned char signature) {
  getProtoNodeTable<COORD, ICOORD>()[signature] = nullptr;
}

// This function must be called before anything else.
template <class COORD, class ICOORD>
void initializeProtoNodes() {
  // Create an instance of each ProtoVSBNode class in each orientation
  // and store it in a table indexed by the voxel signature for that
  // configuration.  The table is used to create the ProtoVSBNodes
  // when a CMicrostructure is computing voxel set boundaries.

  static bool done = false;
  if(done)
    return;
  done = true;

  // First, the configurations that *don't* define a vertex.
  // Including these explicitly just helps us to be sure that we
  // covered all the cases.
  
  // The trivial cases:
  pn<COORD, ICOORD>(voxelNONE); // no voxels
  pn<COORD, ICOORD>(voxelALL); // all 8 voxels

  // Two adjacent voxels sharing a face (the butterstick
  // configurations) don't define a vertex.  There are 12
  // possibilities:
  pn<COORD, ICOORD>(vox000|vox001);
  pn<COORD, ICOORD>(vox010|vox011);
  pn<COORD, ICOORD>(vox100|vox101);
  pn<COORD, ICOORD>(vox110|vox111);
  pn<COORD, ICOORD>(vox000|vox010);
  pn<COORD, ICOORD>(vox001|vox011);
  pn<COORD, ICOORD>(vox100|vox110);
  pn<COORD, ICOORD>(vox101|vox111);
  pn<COORD, ICOORD>(vox000|vox100);
  pn<COORD, ICOORD>(vox001|vox101);
  pn<COORD, ICOORD>(vox010|vox110);
  pn<COORD, ICOORD>(vox011|vox111);
  // Ditto for the 12 inverse buttersticks (two holes sharing a face).
  pn<COORD, ICOORD>(~(vox000|vox001));
  pn<COORD, ICOORD>(~(vox010|vox011));
  pn<COORD, ICOORD>(~(vox100|vox101));
  pn<COORD, ICOORD>(~(vox110|vox111));
  pn<COORD, ICOORD>(~(vox000|vox010));
  pn<COORD, ICOORD>(~(vox001|vox011));
  pn<COORD, ICOORD>(~(vox100|vox110));
  pn<COORD, ICOORD>(~(vox101|vox111));
  pn<COORD, ICOORD>(~(vox000|vox100));
  pn<COORD, ICOORD>(~(vox001|vox101));
  pn<COORD, ICOORD>(~(vox010|vox110));
  pn<COORD, ICOORD>(~(vox011|vox111));

  // Four voxels in one plane don't define a vertex.  There are 6
  // configurations:
  pn<COORD, ICOORD>(vox000|vox001|vox010|vox011); // x=0
  pn<COORD, ICOORD>(vox100|vox101|vox110|vox111); // x=1
  pn<COORD, ICOORD>(vox000|vox100|vox001|vox101); // y=0
  pn<COORD, ICOORD>(vox010|vox110|vox011|vox111); // y=1
  pn<COORD, ICOORD>(vox000|vox010|vox100|vox110); // z=0
  pn<COORD, ICOORD>(vox001|vox011|vox101|vox111); // z=1
  
  // Two parallel offset stacks of two voxels don't define a vertex.
  pn<COORD, ICOORD>(vox000|vox001|vox110|vox111);
  pn<COORD, ICOORD>(vox100|vox101|vox010|vox011);
  pn<COORD, ICOORD>(vox000|vox100|vox011|vox111);
  pn<COORD, ICOORD>(vox001|vox101|vox010|vox110);
  pn<COORD, ICOORD>(vox001|vox011|vox100|vox110);
  pn<COORD, ICOORD>(vox000|vox010|vox101|vox111);

  // Now the real cases:
  pn(vox111, new SingleVoxel<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox101, new SingleVoxel<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox001, new SingleVoxel<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox011, new SingleVoxel<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox000, new SingleVoxel<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox010, new SingleVoxel<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(vox110, new SingleVoxel<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox100, new SingleVoxel<COORD, ICOORD>(VoxRot(posX, negY, negZ)));

  pn(~vox111, new SevenVoxels<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~vox101, new SevenVoxels<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(~vox001, new SevenVoxels<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~vox011, new SevenVoxels<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~vox000, new SevenVoxels<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~vox010, new SevenVoxels<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(~vox110, new SevenVoxels<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~vox100, new SevenVoxels<COORD, ICOORD>(VoxRot(posX, negY, negZ)));

  pn(vox000|vox110, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox010|vox100, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox001|vox111, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox101|vox011, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox100|vox111, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(vox000|vox011, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox001|vox010, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox010|vox111, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox110|vox011, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox000|vox101, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100, new TwoVoxelsByEdge<COORD, ICOORD>(VoxRot(negX, posZ, posY)));

  pn(~(vox000|vox110), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox010|vox100), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox001|vox111), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox011), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox111), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(~(vox000|vox011), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(~(vox001|vox010), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(~(vox010|vox111), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(~(vox110|vox011), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(~(vox000|vox101), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100), new SixVoxelsByEdge<COORD, ICOORD>(VoxRot(negX, posZ, posY)));

  pn(vox000|vox111, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox011, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox110|vox001, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox010|vox101, new TwoVoxelsByCorner<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  pn(~(vox000|vox111), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox011), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox110|vox001), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox101), new SixVoxelsByCorner<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  // Three voxels in the Z=0 plane
  pn(vox000|vox100|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox100|vox110|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  // Three voxels in the Z=1 plane
  pn(vox001|vox101|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox111|vox011|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox101|vox111|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox101|vox111|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  // Three voxels in the X=0 plane
  pn(vox000|vox010|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(vox000|vox001|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox000|vox010|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  // Three voxels in the X=1 plane
  pn(vox100|vox101|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox111|vox101|vox100, new ThreeVoxL<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(vox101|vox111|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox111|vox110|vox100, new ThreeVoxL<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  // Three voxels in the Y=0 plane
  pn(vox000|vox100|vox001, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(vox000|vox001|vox101, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox001|vox101|vox100, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(vox000|vox100|vox101, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  // Three voxels in the Y=1 plane
  pn(vox110|vox010|vox011, new ThreeVoxL<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox111|vox011|vox010, new ThreeVoxL<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox111|vox011|vox110, new ThreeVoxL<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox110|vox010|vox111, new ThreeVoxL<COORD, ICOORD>(VoxRot(posZ, negX, negY)));

  pn(~(vox100|vox101|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(~(vox111|vox101|vox100), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  pn(~(vox101|vox111|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(~(vox111|vox110|vox100), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(~(vox000|vox010|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(~(vox000|vox001|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(~(vox001|vox011|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(~(vox000|vox010|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(~(vox110|vox010|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(~(vox111|vox011|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(~(vox111|vox011|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox010|vox111), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, negX, negY)));
  pn(~(vox000|vox100|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(~(vox000|vox001|vox101), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(~(vox001|vox101|vox100), new FiveVoxL<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(~(vox000|vox100|vox101), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  pn(~(vox001|vox101|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~(vox111|vox011|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(~(vox101|vox111|vox011), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox111|vox001), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox100|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox000|vox100|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox100|vox110|vox010), new FiveVoxL<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox000|vox010|vox110), new FiveVoxL<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  // Double stack in the z direction, single voxel in the z=0 plane
  pn(vox000|vox110|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox010|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox000|vox110|vox001, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox100|vox010|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single voxel in the z=1 plane
  pn(vox001|vox110|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox010|vox011|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(vox000|vox001|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox100|vox101|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single voxel in the x=1 plane
  pn(vox000|vox100|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox001|vox110|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(vox100|vox011|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110|vox010, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single voxel in the x=0 plane
  pn(vox000|vox100|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox010|vox001|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(vox000|vox011|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(vox001|vox010|vox110, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single voxel in the x=0 plane
  pn(vox000|vox010|vox101, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100|vox110, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox000|vox101|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(vox100|vox001|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single voxel in the x=1 plane
  pn(vox000|vox010|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox110|vox001|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posZ, negX, negY)));
  pn(vox010|vox101|vox111, new ThreeTwoOne<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox011, new ThreeTwoOne<COORD, ICOORD>(VoxRot(negZ, posX, negY)));

  // Double stack in the z direction, single hole in the z=0 plane
  pn(~(vox000|vox110|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox010|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(~(vox000|vox110|vox001), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox100|vox010|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single hole in the z=1 plane
  pn(~(vox001|vox110|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~(vox010|vox011|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox001|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox100|vox101|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single hole in the x=1 plane
  pn(~(vox000|vox100|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(~(vox001|vox110|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(~(vox100|vox011|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110|vox010), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single hole in the x=0 plane
  pn(~(vox000|vox100|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(~(vox010|vox001|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(~(vox000|vox011|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posY, posZ, posX)));
  pn(~(vox001|vox010|vox110), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single hole in the x=0 plane
  pn(~(vox000|vox010|vox101), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100|vox110), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(~(vox000|vox101|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(~(vox100|vox001|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single hole in the x=1 plane
  pn(~(vox000|vox010|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox001|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(posZ, negX, negY)));
  pn(~(vox010|vox101|vox111), new FiveTwoOne<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(~(vox100|vox110|vox011), new FiveTwoOne<COORD, ICOORD>(VoxRot(negZ, posX, negY)));

  pn(vox110|vox011|vox101, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox001|vox111, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox000|vox101|vox011, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox010|vox001|vox111, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox111|vox100|vox010, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox000|vox110|vox101, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox100|vox010|vox001, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox000|vox011|vox110, new ThreeVoxByEdges<COORD, ICOORD>(VoxRot(negX, posY, negZ)));

  pn(~(vox110|vox011|vox101), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox001|vox111), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(~(vox000|vox101|vox011), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox001|vox111), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(~(vox111|vox100|vox010), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(~(vox000|vox110|vox101), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox010|vox001), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(~(vox000|vox011|vox110), new FiveVoxByEdges<COORD, ICOORD>(VoxRot(negX, posY, negZ)));

  pn(vox000|vox100|vox010|vox011, new ChiralR<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox010|vox110|vox111, new ChiralR<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox100|vox010|vox110|vox101, new ChiralR<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox001|vox100|vox110, new ChiralR<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox000|vox001|vox011|vox111, new ChiralR<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox101|vox111|vox011|vox010, new ChiralR<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox001|vox101|vox111|vox110, new ChiralR<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox001|vox011|vox100|vox101, new ChiralR<COORD, ICOORD>(VoxRot(negZ, negX, posY)));

  pn(vox000|vox010|vox001|vox101, new ChiralR<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox110, new ChiralR<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox100|vox110|vox111|vox011, new ChiralR<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox000|vox100|vox101|vox111, new ChiralR<COORD, ICOORD>(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox110, new ChiralL<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox100|vox110|vox010|vox011, new ChiralL<COORD, ICOORD>(VoxRot(negY, posX, posZ)));
  pn(vox000|vox100|vox110|vox111, new ChiralL<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox100|vox101|vox010, new ChiralL<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox101|vox001|vox011|vox010, new ChiralL<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox111|vox110, new ChiralL<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox100|vox101|vox111|vox011, new ChiralL<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox000|vox001|vox101|vox111, new ChiralL<COORD, ICOORD>(VoxRot(negZ, negX, posY)));

  pn(vox000|vox100|vox001|vox011, new ChiralL<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox000|vox010|vox011|vox111, new ChiralL<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox101|vox111|vox110|vox010, new ChiralL<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox001|vox101|vox100|vox110, new ChiralL<COORD, ICOORD>(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox100, new Pyramid<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox101|vox110, new Pyramid<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox111|vox110|vox010|vox100, new Pyramid<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox011, new Pyramid<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  pn(vox111|vox110|vox101|vox011, new Pyramid<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox001|vox011|vox111|vox010, new Pyramid<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox000|vox001|vox011|vox101, new Pyramid<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
  pn(vox001|vox101|vox111|vox100, new Pyramid<COORD, ICOORD>(VoxRot(negX, posY, negZ)));

  pn(vox100|vox010|vox001|vox111, new CheckerBoard<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox110|vox101|vox011, new CheckerBoard<COORD, ICOORD>(VoxRot(posY, negX, posZ)));

  pn(vox000|vox010|vox100|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, negX, posZ)));
  pn(vox100|vox010|vox110|vox001, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox101, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, posX, posZ)));

  pn(vox000|vox001|vox011|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, posY, posX)));
  pn(vox100|vox010|vox011|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, posX, negY)));
  pn(vox000|vox110|vox111|vox101, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, negY, negX)));
  pn(vox100|vox101|vox001|vox010, new FourThreeOne<COORD, ICOORD>(VoxRot(negZ, negX, posY)));

  pn(vox010|vox011|vox101|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox111|vox001, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, posZ, negX)));
  pn(vox000|vox100|vox101|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, posZ, posY)));
  pn(vox000|vox010|vox001|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, posZ, posX)));

  pn(vox000|vox001|vox101|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox100, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, negZ, posX)));
  pn(vox000|vox011|vox111|vox110, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, negZ, negY)));
  pn(vox010|vox100|vox101|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, negZ, negX)));

  pn(vox100|vox110|vox101|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, posY, negX)));
  pn(vox000|vox001|vox100|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, posX, posY)));
  pn(vox000|vox010|vox011|vox101, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, negY, posX)));
  pn(vox001|vox111|vox110|vox010, new FourThreeOne<COORD, ICOORD>(VoxRot(posZ, negX, negY)));

  pn(vox001|vox011|vox111|vox100, new FourThreeOne<COORD, ICOORD>(VoxRot(posX, negY, negZ)));
  pn(vox000|vox101|vox011|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(negY, negX, negZ)));
  pn(vox010|vox001|vox101|vox111, new FourThreeOne<COORD, ICOORD>(VoxRot(negX, posY, negZ)));
  pn(vox110|vox001|vox101|vox011, new FourThreeOne<COORD, ICOORD>(VoxRot(posY, posX, negZ)));
} // end initializeProtoNodes()

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


#undef swap
#endif // VSB_H
