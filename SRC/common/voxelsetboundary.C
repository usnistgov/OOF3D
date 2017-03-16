// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <algorithm>
#include "common/voxelsetboundary.h"

// To create the boundaries of all voxel categories

//  Loop over all edges in the MS:
//    If the edge has voxels of at least two categories:
//      For each category:
//        In the ProtoGraph for the category, fetch or create the VSBNode
//         at each end point of the edge.
//        Make the VSBNodes neighbors of each other.
// For each category:
//   Create an empty VSBGraph.
//   For all vertices in the ProtoGraph:
//     If it has only two edges:
//       Connect its neighbors to each other & delete the vertex
//   For all vertices in the ProtoGraph (which now have three or more nbrs):
//     If the vertex has three neighbors:
//       Put them in the correct order.
//       Put the node in the VSBGraph.
//     If the vertex has more than three neighbors:
//       Identify which of the 8 neighboring voxels are inside the category.
//       Using the identification, invoke a splitting function that creates
//       three-fold VSBNodes and connects them to the neighbors.
//       Put the new VSBNodes in the VSBGraph.
//       Delete the original VSBNode.


// Can clipping be done without copying the full graph?  Have two
// clipping operations: one creates a copy as it goes, and one clips
// in place.  Use the first one when clipping at the first tet plane.

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelEdgeDirection::VoxelEdgeDirection(unsigned int ax, int d)
  : axis(ax),
    dir(d)
{
  assert(ax >=0 && ax <= 2);
  assert(d == 1 || d == -1);
}

VoxelEdgeDirection VoxelEdgeDirection::reverse() const {
  return VoxelEdgeDirection(axis, -dir);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Some helpful constants.

const VoxelEdgeDirection posX(0, 1);
const VoxelEdgeDirection negX(0, -1);
const VoxelEdgeDirection posY(1, 1);
const VoxelEdgeDirection negY(1, -1);
const VoxelEdgeDirection posZ(2, 1);
const VoxelEdgeDirection negZ(2, -1);

static VoxelRotation nullRotation(posX, posY, posZ);

// Voxel signatures for the single voxels of the 2x2x2 cube.  The
// names say whether the x, y, and z component of the voxel position
// is on the positive side (1) or negative side (0) of the cube.  See
// CMicrostructure::voxelSignature() in cmicrostructure.C for an
// explanation of the values of the signatures.  The values have to be
// consistent the the loops in that function.

// These values can be simply added together to get the signature for
// multi-voxel group.

static char voxel000 = 0x1;
static char voxel100 = 0x2;
static char voxel010 = 0x4;
static char voxel110 = 0x8;
static char voxel001 = 0x10;
static char voxel101 = 0x20;
static char voxel011 = 0x40;
static char voxel111 = 0x80;

static char voxelALL = 0xff;
static char voxelNONE = 0x0;


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A VoxelRotation says which axis in the actual configuration
// corresponds to which axis in the reference configuration.  The
// arguments to the constructor are the actual space directions that
// correspond to the +x, +y, and +z directions in the reference space.

VoxelRotation::VoxelRotation(VoxelEdgeDirection d0, VoxelEdgeDirection d1,
			     VoxelEdgeDirection d2)
  : dirs(3)
{
  dirs[0] = d0;
  dirs[1] = d1;
  dirs[2] = d2;
}

VoxelEdgeDirection VoxelRotation::map(VoxelEdgeDirection d) const {
  if(d.dir == 1)
    return dirs[d];
  return dirs[d].reverse();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void VSBNode::replaceNeighbor(VSBNode *oldNbr, VSBNode *newNbr) {
  for(unsigned int i=0; i<neighbors.size(); i++) {
    if(neighbors[i] == oldNbr) {
      neighbors[i] = newNbr;
      return;
    }
  }
  throw ErrProgrammingError("VSBNode::replaceNeighbor failed!",
			    __FILE__, __LINE__);
}

void VSBNode::replaceNeighbor(unsigned int idx, VSBNode *newNbr) {
  assert(idx < neighbors.size());
  neighbors[idx] = newNbr;
}

void VSBNode::removeNeighbor(VSBNode *nbr) {
  auto iter = std::find(neighbors.begin(), neighbors.end(), nbr);
  assert(iter != neighbors.end());
  neighbors.erase(iter);
}

// VSBNode *VSBNode::removeNeighbor(unsigned int idx) {
//   VSBNode *removed = neighbors[idx];
//   neighbors.erase(neighbors.begin() + idx);
//   return removed;
// }

void VSBNode::switchNeighbors() {
  // switching the order of any two neighbors of a three fold node
  // changes a CCW node into a CW one, and vice versa.
  assert(neighbors.size() == 3);
  VSBNode *tmp = neighbors[0];
  neighbors[0] = neighbors[1];
  neighbors[1] = tmp;
}

// VSBNode::getNeighborIndex returns the index of the neighbor in
// VSBNode::neighbors that is in the given direction.
unsigned int VSBNode::getNeighborIndex(VoxelEdgeDirection &dir) const {
  for(unsigned int i=0; i<neighbors.size(); i++) {
    // This is only used when building the original VSBGraph from the
    // Microstructure, before it's clipped, so the edges are all in
    // the positive or negative X, Y, and Z directions and are not
    // infinitesimal.

    //   d is the difference between the dir.axis components of this
    // node and its neighbor.  This difference is non-zero only for
    // the neighbor node we're looking for, or possibly the neighbor
    // in the opposite direction (which is checked by dir.dir).
    double d = neighbors[i]->position[dir.axis] - position[dir.axis];
    if((dir.dir == 1 && d > 0) || (dir.dir == -1 && d < 0))
      return i;
  }
  throw ErrProgrammingError("VSBNode::getNeighborIndex failed!",
			    __FILE__, __LINE__);
}

void VSBNode::ensureClockwise(const VSBNode *nodeA, const VSBNode *nodeB,
			      const VSBNode *nodeC)
{
  // Ensure that the nodes are in order ABC, BCA, or CAB.
  assert(neighbors.size() == 3);
  assert(std::find(neighbors.begin(), neighbors.end(), nodeA)!=neighbors.end());
  assert(std::find(neighbors.begin(), neighbors.end(), nodeB)!=neighbors.end());
  assert(std::find(neighbors.begin(), neighbors.end(), nodeC)!=neighbors.end());
  VSBNode *node0 = neighbors[0];
  VSBNode *node1 = neighbors[1];
  if(!((nodeA==node0 && nodeB==node1) ||
       (nodeB==node0 && nodeC==node1) ||
       (nodeC==node0 && nodeA==node1)))
    {
      switchNeighbors();
    }
}

// void VSBNode::ensureCounterClockwise(const VSBNode *nodeA, const VSBNode *nodeB,
// 			      const VSBNode *nodeC)
// {
//   // Ensure that the nodes are in order CBA, ACB, or BAC.
//   assert(neighbors.size() == 3);
//   assert(std::find(neighbors.begin(), neighbors.end(), nodeA)!=neighbors.end());
//   assert(std::find(neighbors.begin(), neighbors.end(), nodeB)!=neighbors.end());
//   assert(std::find(neighbors.begin(), neighbors.end(), nodeC)!=neighbors.end());
//   VSBNode *node0 = neighbors[0];
//   VSBNode *node1 = neighbors[1];
//   if(!((nodeC==node0 && nodeB==node1) ||
//        (nodeA==node0 && nodeC==node1) ||
//        (nodeB==node0 && nodeA==node1)))
//     {
//       switchNeighbors();
//     }
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VSBGraph::~VSBGraph() {
  for(VSBNode *node : vertexMap)
    delete node;
  vertexMap.clear();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// VSBNodeRectifier subclasses take nodes in the ProtoGraph and fix
// them up and put them in the actual graph.  Fixing them up entails
// making sure that the edges are ordered correctly and splitting
// nodes that have too many edges.  In that case, the rectifier
// allocates and inserts new nodes.

// See CMicrostructure::voxelSignature in cmicrostructure.C for
// details on the voxel signature.

static std::vector<VSBNodeRectifier*> nodeRectifiers(256, nullptr);

class VSBNodeRectifier {
protected:
  const VoxelRotation rotation;
public:
  VSBNodeRectifier(unsigned char signature, const VoxelRotation &rot)
    : rotation(rot)
  {
    assert(nodeRectifiers[signature] == nullptr);
    nodeRectifiers[signature] = this;
  }
  virtual void apply(VSBNode*, VSBGraph*) const = 0;
};

// // TODO: I don't think "positive permutation" is the correct term.  If
// // a, b, and c are some permutation of 0, 1, and 2, return true if
// // they're in ascending order (modulo a shift) and false if they're
// // descending.  Ie, 012, 120, 201 are true, and 210, 102, and 021 are
// // false.
// static bool positivePermutation(unsigned int a, unsigned int b, unsigned int c)
// {
//   assert(a == 0 || a == 1 || a == 2);
//   assert(b == 0 || b == 1 || b == 2);
//   assert(c == 0 || c == 1 || c == 2);
//   assert(a != b && b != c && c != a);
//   // Only one of these is comparisons is strictly needed, but then the
//   // compiler would complain about one of the args being unused when
//   // not compiled in debug mode.
//   // TODO: it may be faster to just write out the cases and skip the %.
//   return (a+1)%3 == b && (b+1)%3 == c && (c+1)%3 == a;
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The NullRectifier doesn't do anything, and is used for voxel
// configurations that don't contain a corner of the VSB.  It could be
// omitted, but for debugging purposes it's good to have all the
// configurations covered.  It should never be called, because its
// voxel configurations should never appear in the graph.

class NullRectifier : public VSBNodeRectifier {
public:
  NullRectifier(unsigned char signature)
    : VSBNodeRectifier(signature, nullRotation)
  {}
  virtual void apply(VSBNode*, VSBGraph*) const {
    throw ErrProgrammingError("NullRectifier called!", __FILE__, __LINE__);
  }
};

// The trivial cases:
NullRectifier(voxelNONE); // no voxels
NullRectifier(voxelALL); // all 8 voxels

// Two adjacent voxels sharing a face (the butterstick configurations)
// also don't define a vertex.  There are 12 possibilities:
NullRectifier(voxel000+voxel001);
NullRectifier(voxel010+voxel011);
NullRectifier(voxel100+voxel101);
NullRectifier(voxel110+voxel111);
NullRectifier(voxel000+voxel010);
NullRectifier(voxel001+voxel011);
NullRectifier(voxel100+voxel110);
NullRectifier(voxel101+voxel111);
NullRectifier(voxel000+voxel100);
NullRectifier(voxel001+voxel101);
NullRectifier(voxel010+voxel110);
NullRectifier(voxel011+voxel111);

// Ditto for the 12 inverse buttersticks.
NullRectifier(voxelALL-voxel000-voxel001);
NullRectifier(voxelALL-voxel010-voxel011);
NullRectifier(voxelALL-voxel100-voxel101);
NullRectifier(voxelALL-voxel110-voxel111);
NullRectifier(voxelALL-voxel000-voxel010);
NullRectifier(voxelALL-voxel001-voxel011);
NullRectifier(voxelALL-voxel100-voxel110);
NullRectifier(voxelALL-voxel101-voxel111);
NullRectifier(voxelALL-voxel000-voxel100);
NullRectifier(voxelALL-voxel001-voxel101);
NullRectifier(voxelALL-voxel010-voxel110);
NullRectifier(voxelALL-voxel011-voxel111);

// Four voxels in one plane don't define a vertex.  There are 6
// configurations:

NullRectifier(voxel000+voxel001+voxel010+voxel011); // x=M
NullRectifier(voxel100+voxel101+voxel110+voxel111); // x=P
NullRectifier(voxel000+voxel100+voxel001+voxel101); // y=M
NullRectifier(voxel010+voxel110+voxel011+voxel111); // y=P
NullRectifier(voxel000+voxel010+voxel100+voxel110); // z=M
NullRectifier(voxel001+voxel011+voxel101+voxel111); // z=P

//--------

// For a node at the corner of a single voxel, the reference
// configuration in the 2x2x2 cube has the voxel in the +x, +y, +z
// corner and the neighbors in the +x, +y, +z directions.

class SingleVoxel : public VSBNodeRectifier {
public:
  SingleVoxel(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) const {
    // Make sure that the neighbors are ordered CW when viewed from
    // outside the voxel.  The neighbors in the reference
    // configuration are in the +x, +y, and +z directions, in that
    // order, and "outside" is in the (-x, -y, -z) direction.  When
    // viewed from outside, they're ordered clockwise, so we have to
    // ensure that the mapping from reference configuration neighbors
    // to actual neighbors is a positive permutation of xyz.
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(posX));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(posZ));
    oldNode->ensureClockwise(nodeA, nodeB, nodeC);
    graph->addNode(oldNode);
  }
};

SingleVoxel(voxel000, VoxelRotation(negX, negY, negZ));
SingleVoxel(voxel100, VoxelRotation(posX, negZ, negY));
SingleVoxel(voxel010, VoxelRotation(negZ, posY, negX));
SingleVoxel(voxel110, VoxelRotation(posY, posX, negZ));
SingleVoxel(voxel001, VoxelRotation(negY, negX, posZ));
SingleVoxel(voxel101, VoxelRotation(negY, posX, posZ));
SingleVoxel(voxel011, VoxelRotation(posY, negZ, posZ));
SingleVoxel(voxel111, VoxelRotation(posX, posY, posZ)); // reference config

//--------

// Seven voxels are just like one, except the "outside" is on the
// other side.  The only difference between SevenVoxels and
// SingleVoxel is that we need to ensure that the order of the +xyz
// axes is CCW, so the args to ensureClockwise are in a different
// order.

class SevenVoxels : public VSBNodeRectifier {
public:
  SevenVoxels(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) const {
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(posX));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(posZ));
    oldNode->ensureClockwise(nodeB, nodeA, nodeC);
    graph->addNode(oldNode);
  }
};

SevenVoxels(voxelALL-voxel000, VoxelRotation(negX, negY, negZ));
SevenVoxels(voxelALL-voxel100, VoxelRotation(posX, negZ, negY));
SevenVoxels(voxelALL-voxel010, VoxelRotation(negZ, posY, negX));
SevenVoxels(voxelALL-voxel110, VoxelRotation(posY, posX, negZ));
SevenVoxels(voxelALL-voxel001, VoxelRotation(negY, negX, posZ));
SevenVoxels(voxelALL-voxel101, VoxelRotation(negY, posX, posZ));
SevenVoxels(voxelALL-voxel011, VoxelRotation(posY, negZ, posZ));
SevenVoxels(voxelALL-voxel111, VoxelRotation(posX, posY, posZ)); 

//--------

// The nontrivial cases for two voxels are when they touch at an edge
// and when they touch at a corner.

class TwoVoxelsByEdge : public VSBNodeRectifier {
public:
  TwoVoxelsByEdge(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) const {
    // The reference configuration is voxel000 + voxel110.  There are
    // edges in the posX, negX, posY, negY, and negZ directions.
    // 
    /*
     *                    E    D         O is the old node.
     *  E  D               \   |         ABCD are in the Z plane of O.
     *   \ |                1--2---C     E is on the negZ plane.
     *	  \|               /             
     * A---O---C ==>  A---O              1 and 2 are new nodes colocated
     *     |              |              with O
     *     |              |
     *     B              B
     */
    
    VSBNode *newNode1 = new VSBNode(oldNode->position);
    VSBNode *newNode2 = new VSBNode(oldNode->position);
    
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(negX));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(negY));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(posX));
    VSBNode *nodeD = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeE = oldNode->getNeighbor(rotation.map(negZ));
    // TODO: add and remove all in one call, for efficiency?  This
    // resizes the vector too often.
    oldNode->removeNeighbor(nodeD);
    oldNode->removeNeighbor(nodeE);
    oldNode->replaceNeighbor(nodeC, newNode1);
    
    newNode1->addNeighbor(oldNode);
    newNode1->addNeighbor(nodeE);
    newNode1->addNeighbor(newNode2);
    newNode2->addNeighbor(newNode1);
    newNode2->addNeighbor(nodeD);
    newNode2->addNeighbor(nodeC);
    // Make sure that the edges are in CW order for all three nodes O,
    // 1, and 2, when viewed from outside (ie +z side).
    oldNode->ensureClockwise(nodeB, nodeA, node1);
    newNode1->ensureClockwise(oldNode, nodeE, newNode2);
    newNode2->ensureClockwise(newNode1, nodeD, nodeC);
    graph->addNode(oldNode);
    graph->addNode(newNode1);
    graph->addNode(newNode2);
  }
};

// There are 12 orientations.  The comment on each line says which
// plane the two voxels share.  There are two configurations for each
// plane.
TwoVoxelsByEdge(voxel000+voxel110, VoxelRotation(posX, posY, posZ)); // Z=N
TwoVoxelsByEdge(voxel010+voxel100, VoxelRotation(posY, negX, posZ)); // Z=N
TwoVoxelsByEdge(voxel001+voxel111, VoxelRotation(posZ, posY, negX)); // Z=P
TwoVoxelsByEdge(voxel011+voxel101, VoxelRotation(posY, posX, negZ)); // Z=P
TwoVoxelsByEdge(voxel000+voxel011, VoxelRotation(negZ, posY, posX)); // X=N
TwoVoxelsByEdge(voxel001+voxel010, VoxelRotation(posZ, negY, posX)); // X=N
TwoVoxelsByEdge(voxel100+voxel111, VoxelRotation(posZ, posY, negX)); // X=P
TwoVoxelsByEdge(voxel110+voxel101, VoxelRotation(negY, posZ, negX)); // X=P
TwoVoxelsByEdge(voxel000+voxel101, VoxelRotation(negZ, negX, posY)); // Y=N
TwoVoxelsByEdge(voxel100+voxel001, VoxelRotation(negX, posZ, posY)); // Y=N
TwoVoxelsByEdge(voxel010+voxel111, VoxelRotation(posX, posZ, negY)); // Y=P
TwoVoxelsByEdge(voxel110+voxel011, VoxelRotation(posZ, negX, negY)); // Y=P

class TwoVoxelsByCorner : public VSBNodeRectifier {
public:
  TwoVoxelsByCorner(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) const {
    // The reference configuration is voxel000 + voxel111
    // There are edges in all 6 directions.
    /*
     *     A     F             A        F
     *      \   /               \      /
     *       \ /                 \    /
     *   B----O---- E  -->  B ----O  1---- E
     *       / \                 /    \
     *      /   \               /      \
     *     C     D             C        D
     */

    VSBNode *newNode = new VSBNode(oldNode->position);
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(negZ));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(negX));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(negY));
    VSBNode *nodeD = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeE = oldNode->getNeighbor(rotation.map(posZ));
    VSBNode *nodeF = oldNode->getNeighbor(rotation.map(posX));
    oldNode->removeNeighbor(nodeD);
    oldNode->removeNeighbor(nodeE);
    oldNode->removeNeighbor(nodeF);
    oldNode->ensureClockwise(nodeA, nodeC, nodeB);
    // Adding nodes to newNode in the correct order means we don't
    // have to call ensureClockwise for it.
    newNode->addNeighbor(nodeD);
    newNode->addNeighbor(nodeE);
    newNode->addNeighbor(nodeF);
    graph->addNode(oldNode);
    graph->addNode(newNode);
  }
};

// There are 4 orientations
TwoVoxelsByCorner(voxel000+voxel111, VoxelRotation(posX, posY, posZ));
TwoVoxelsByCorner(voxel100+voxel011, VoxelRotation(posY, negX, posZ));
TwoVoxelsByCorner(voxel110+voxel001, VoxelRotation(negX, negY, posZ));
TwoVoxelsByCorner(voxel010+voxel101, VoxelRotation(negY, posX, posZ));

//--------

// SixVoxelsByEdge is the inverse of TwoVoxelsByEdge

class SixVoxelsByEdge : public VSBNodeRectifier {
public:
  SixVoxelsByEdge(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) const {
    VSBNode *newNode1 = new VSBNode(oldNode->position);
    VSBNode *newNode2 = new VSBNode(oldNode->position);
    
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(negX));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(negY));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(posX));
    VSBNode *nodeD = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeE = oldNode->getNeighbor(rotation.map(negZ));
    // TODO: add and remove all in one call, for efficiency?  This
    // resizes the vector too often.
    oldNode->removeNeighbor(nodeD);
    oldNode->removeNeighbor(nodeE);
    oldNode->replaceNeighbor(nodeC, newNode1);
    
    newNode1->addNeighbor(oldNode);
    newNode1->addNeighbor(nodeE);
    newNode1->addNeighbor(newNode2);
    newNode2->addNeighbor(newNode1);
    newNode2->addNeighbor(nodeD);
    newNode2->addNeighbor(nodeC);

    // The difference between SixVoxelsByEdge and TwoVoxelsByEdge is
    //  in the next three lines, where the order of the neighbors is
    //  reversed, because inside and outside are reversed.
    oldNode->ensureClockwise(nodeA, nodeB, node1);
    newNode1->ensureClockwise(nodeE, oldNode, newNode2);
    newNode2->ensureClockwise(nodeD, newNode1, nodeC);

    graph->addNode(oldNode);
    graph->addNode(newNode1);
    graph->addNode(newNode2);
  }
};

SixVoxelsByEdge(voxelALL-voxel000-voxel110,
		VoxelRotation(posX, posY, posZ)); // Z=N
SixVoxelsByEdge(voxelALL-voxel010-voxel100,
		VoxelRotation(posY, negX, posZ)); // Z=N
SixVoxelsByEdge(voxelALL-voxel001-voxel111,
		VoxelRotation(posZ, posY, negX)); // Z=P
SixVoxelsByEdge(voxelALL-voxel011-voxel101,
		VoxelRotation(posY, posX, negZ)); // Z=P
SixVoxelsByEdge(voxelALL-voxel000-voxel011,
		VoxelRotation(negZ, posY, posX)); // X=N
SixVoxelsByEdge(voxelALL-voxel001-voxel010,
		VoxelRotation(posZ, negY, posX)); // X=N
SixVoxelsByEdge(voxelALL-voxel100-voxel111,
		VoxelRotation(posZ, posY, negX)); // X=P
SixVoxelsByEdge(voxelALL-voxel110-voxel101,
		VoxelRotation(negY, posZ, negX)); // X=P
SixVoxelsByEdge(voxelALL-voxel000-voxel101,
		VoxelRotation(negZ, negX, posY)); // Y=N
SixVoxelsByEdge(voxelALL-voxel100-voxel001,
		VoxelRotation(negX, posZ, posY)); // Y=N
SixVoxelsByEdge(voxelALL-voxel010-voxel111,
		VoxelRotation(posX, posZ, negY)); // Y=P
SixVoxelsByEdge(voxelALL-voxel110-voxel011,
		VoxelRotation(posZ, negX, negY)); // Y=P

//--------

// SixVoxelsByCorner is the inverse of TwoVoxelsByCorner

class SixVoxelsByCorner : public VSBNodeRectifier {
public:
  SixVoxelsByCorner(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) const {
    VSBNode *newNode = new VSBNode(oldNode->position);
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(negZ));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(negX));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(negY));
    VSBNode *nodeD = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeE = oldNode->getNeighbor(rotation.map(posZ));
    VSBNode *nodeF = oldNode->getNeighbor(rotation.map(posX));
    oldNode->removeNeighbor(nodeD);
    oldNode->removeNeighbor(nodeE);
    oldNode->removeNeighbor(nodeF);
    oldNode->ensureClockwise(nodeC, nodeA, nodeB);
    newNode->addNeighbor(nodeE);
    newNode->addNeighbor(nodeD);
    newNode->addNeighbor(nodeF);
    graph->addNode(oldNode);
    graph->addNode(newNode);
  }
};

SixVoxelsByCorner(voxelALL-voxel000-voxel111, VoxelRotation(posX, posY, posZ));
SixVoxelsByCorner(voxelALL-voxel100-voxel011, VoxelRotation(posY, negX, posZ));
SixVoxelsByCorner(voxelALL-voxel110-voxel001, VoxelRotation(negX, negY, posZ));
SixVoxelsByCorner(voxelALL-voxel010-voxel101, VoxelRotation(negY, posX, posZ));

//----------

// Three voxels in an L configuration.  The node does not need to be
// split.

class ThreeVoxelsL : public VSBNodeRectifier {
public:
  ThreeVoxelsL(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) {
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(posX));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(negZ));
    oldNode->ensureClockwise(nodeA, nodeB, nodeC);
    graph->addNode(oldNode);
  }
};

// There are 24 orientations.

// Three voxels in the X=P plane
ThreeVoxelsL(voxel100+voxel101+voxel110, VoxelRotation(posZ, posY, negX));
ThreeVoxelsL(voxel111+voxel101+voxel100, VoxelRotation(posY, negZ, negX));
ThreeVoxelsL(voxel101+voxel111+voxel110, VoxelRotation(negZ, negY, negX));
ThreeVoxelsL(voxel111+voxel110+voxel100, VoxelRotation(negY, posZ, negX));
// Three voxels in the X=N plane
ThreeVoxelsL(voxel000+voxel010+voxel001, VoxelRotation(posY, posZ, posX));
ThreeVoxelsL(voxel000+voxel001+voxel011, VoxelRotation(negZ, posY, posX));
ThreeVoxelsL(voxel001+voxel011+voxel010, VoxelRotation(negY, negZ, posX));
ThreeVoxelsL(voxel000+voxel010+voxel011, VoxelRotation(posZ, negY, posX));
// Three voxels in the Y=P plane
ThreeVoxelsL(voxel110+voxel010+voxel011, VoxelRotation(posX, posZ, negY));
ThreeVoxelsL(voxel111+voxel011+voxel010, VoxelRotation(negZ, posX, negY));
ThreeVoxelsL(voxel111+voxel011+voxel110, VoxelRotation(negX, negZ, negY));
ThreeVoxelsL(voxel110+voxel010+voxel111, VoxelRotation(posZ, negX, negY));
// Three voxels in the Y=N plane
ThreeVoxelsL(voxel000+voxel100+voxel001, VoxelRotation(posZ, posX, posY));
ThreeVoxelsL(voxel000+voxel001+voxel101, VoxelRotation(posX, negZ, posY));
ThreeVoxelsL(voxel001+voxel101+voxel100, VoxelRotation(negZ, negX, posY));
ThreeVoxelsL(voxel000+voxel100+voxel101, VoxelRotation(negX, posZ, posY));
// Three voxels in the Z=P plane
ThreeVoxelsL(voxel001+voxel101+voxel011, VoxelRotation(posY, posX, negZ));
ThreeVoxelsL(voxel111+voxel011+voxel001, VoxelRotation(posX, negY, negZ));
ThreeVoxelsL(voxel101+voxel111+voxel011, VoxelRotation(negY, negX, negZ));
ThreeVoxelsL(voxel101+voxel111+voxel001, VoxelRotation(negX, posY, negZ));
// Three voxels in the Z=N plane
ThreeVoxelsL(voxel000+voxel100+voxel010, VoxelRotation(posX, posY, posZ));
ThreeVoxelsL(voxel000+voxel100+voxel110, VoxelRotation(posY, negX, posZ));
ThreeVoxelsL(voxel100+voxel110+voxel010, VoxelRotation(negX, negY, posZ));
ThreeVoxelsL(voxel000+voxel010+voxel110, VoxelRotation(negY, posX, posZ));

// ----------

// FiveVoxelsL is the inverse of ThreeVoxelsL.  The connections are
// the same, but the order is reversed.

class ThreeVoxelsL : public VSBNodeRectifier {
public:
  FiveVoxelsL(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) {
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(posX));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(posY));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(negZ));
    oldNode->ensureClockwise(nodeB, nodeA, nodeC);
    graph->addNode(oldNode);
  }
};

FiveVoxelsL(voxelALL-voxel100-voxel101-voxel110,
	    VoxelRotation(posZ, posY, negX));
FiveVoxelsL(voxelALL-voxel111-voxel101-voxel100,
	    VoxelRotation(posY, negZ, negX));
FiveVoxelsL(voxelALL-voxel101-voxel111-voxel110,
	    VoxelRotation(negZ, negY, negX));
FiveVoxelsL(voxelALL-voxel111-voxel110-voxel100,
	    VoxelRotation(negY, posZ, negX));
FiveVoxelsL(voxelALL-voxel000-voxel010-voxel001,
	    VoxelRotation(posY, posZ, posX));
FiveVoxelsL(voxelALL-voxel000-voxel001-voxel011,
	    VoxelRotation(negZ, posY, posX));
FiveVoxelsL(voxelALL-voxel001-voxel011-voxel010,
	    VoxelRotation(negY, negZ, posX));
FiveVoxelsL(voxelALL-voxel000-voxel010-voxel011,
	    VoxelRotation(posZ, negY, posX));
FiveVoxelsL(voxelALL-voxel110-voxel010-voxel011,
	    VoxelRotation(posX, posZ, negY));
FiveVoxelsL(voxelALL-voxel111-voxel011-voxel010,
	    VoxelRotation(negZ, posX, negY));
FiveVoxelsL(voxelALL-voxel111-voxel011-voxel110,
	    VoxelRotation(negX, negZ, negY));
FiveVoxelsL(voxelALL-voxel110-voxel010-voxel111,
	    VoxelRotation(posZ, negX, negY));
FiveVoxelsL(voxelALL-voxel000-voxel100-voxel001,
	    VoxelRotation(posZ, posX, posY));
FiveVoxelsL(voxelALL-voxel000-voxel001-voxel101,
	    VoxelRotation(posX, negZ, posY));
FiveVoxelsL(voxelALL-voxel001-voxel101-voxel100,
	    VoxelRotation(negZ, negX, posY));
FiveVoxelsL(voxelALL-voxel000-voxel100-voxel101,
	    VoxelRotation(negX, posZ, posY));
FiveVoxelsL(voxelALL-voxel001-voxel101-voxel011,
	    VoxelRotation(posY, posX, negZ));
FiveVoxelsL(voxelALL-voxel111-voxel011-voxel001,
	    VoxelRotation(posX, negY, negZ));
FiveVoxelsL(voxelALL-voxel101-voxel111-voxel011,
	    VoxelRotation(negY, negX, negZ));
FiveVoxelsL(voxelALL-voxel101-voxel111-voxel001,
	    VoxelRotation(negX, posY, negZ));
FiveVoxelsL(voxelALL-voxel000-voxel100-voxel010,
	    VoxelRotation(posX, posY, posZ));
FiveVoxelsL(voxelALL-voxel000-voxel100-voxel110,
	    VoxelRotation(posY, negX, posZ));
FiveVoxelsL(voxelALL-voxel100-voxel110-voxel010,
	    VoxelRotation(negX, negY, posZ));
FiveVoxelsL(voxelALL-voxel000-voxel010-voxel110,
	    VoxelRotation(negY, posX, posZ));

//---------

// ThreeTwoOne is three voxels, two stacked face to face and a third
// connected to one of the other two along an edge.  There are 24
// orientations.  The reference configuration contains voxels 000,
// 111, and 110.

class ThreeTwoOne : public VSBNodeRectifier {
public:
  ThreeTwoOne(unsigned char signature, const VoxelRotation &rot)
    : VSBNodeRectifier(signature, rot)
  {}
  virtual void apply(VSBNode *oldNode, VSBGraph *graph) const {
    VSBNode *newNode = new VSBNode(oldNode->position);
    VSBNode *nodeA = oldNode->getNeighbor(rotation.map(negX));
    VSBNode *nodeB = oldNode->getNeighbor(rotation.map(negY));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(posZ));
    VSBNode *nodeC = oldNode->getNeighbor(rotation.map(negZ));
    oldNode->removeNeighbor(nodeC);
    oldNode->removeNeighbor(nodeD);
    oldNode->addNeighbor(newNode);
    newNode->addNeighbor(nodeC);
    newNode->addNeighbor(nodeD);
    newNode->addNeighbor(newNode);
    oldNode->ensureClockwise(nodeB, nodeA, nodeD);
    // Because newNode is collinear with two of its neighbors and
    // coincident with the third, the order of its neighbors doesn't
    // matter.
    graph->addNode(oldNode);
    graph->addNode(newNode);
    
      
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelSetBoundary::~VoxelSetBoundary() {
  delete bounds;
}

void VoxelSetBoundary::addEdge(const ICoord3D &pt0, const ICoord3D &pt1) {
  // Create an edge connecting pt0 and pt1 in the ProtoGraph.  The
  // ProtoGraph doesn't worry about having exactly three edges at a
  // node.
  VSBNode *node0, *node1;
  ProtoGraph::iterator n0 = protoGraph.find(pt0);
  if(n0 == protoGraph.end()) {
    node0 = new VSBNode(pt0);
    protoGraph[pt0] = node0;
  }
  else
    node0 = n0->second;
  protoGraph::iterator n1 = protoGraph.find(pt1);
  if(n1 == protoGraph.end()) {
    node1 = new VSBNode(pt1);
    protoGraph[pt1] = node1;
  }
  else
    node1 = n1->second;
  node1->addNeighbor(node0);
  node0->addNeighbor(node1);
}

// find_boundaries consolidates the edges added by addEdges and
// constructs proper 3-fold VSBNodes by splitting the protonodes if
// necessary.  It also puts the edges of each node in the correct
// order.

void VoxelSetBoundary::find_boundaries() {
  // First eliminate nodes with only 2 edges in the ProtoGraph.  Also
  // compute the bounding box.
  delete bounds;
  bounds = nullptr;
  std::vector<ProtoGraph::iterator> deleteThese;
  for(ProtoGraph::iterator i=protoGraph.begin(); i!=protoGraph.end(); ++i) {
    VSBNode *node = i->second;
    if(!bounds)
      bounds = new ICRectangularPrism(node->position, node->position);
    else
      bounds->swallow(node->position);
    assert(node->nNeighbors() >= 2);
    if(node->nNeighbors() == 2) {
      deleteThese.push_back(i);
      node->getNeighbor(0)->replaceNeighbor(node, node->getNeighbor(1));
      node->getNeighbor(1)->replaceNeighbor(node, node->getNeighbor(0));
      delete node;
    }
  }
  for(ProtoGraph::iterator i : deleteThese)
    protoGraph.erase(i);

  // Loop over the nodes in the protoGraph and create 3-fold vertices
  // in the actual graph for each.
  for(ProtoGraph::iterator i=protoGraph.begin(); i!=protoGraph.end(); ++i) {
    ICoord3D nodePos = i->first;
    VSBNode *protoNode = i->second;
    assert(protoNode->nNeighbors() >= 3);
    char sig = microstructure->voxelSignature(nodePos, category);
    // Not quite right here...  The function to call is determined by
    // the signature.  It should put the real nodes in the graph and
    // update neighbors.
    nodeRectifiers[sig]->apply(protoNode, graph);
  }

}
