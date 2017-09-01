// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

// Classes for finding, storing, and clipping a voxel set boundary
// (VSB).  A voxel set is the group of voxels in a single category for
// Skeleton construction purposes.  The Skeleton needs to be able to
// quickly determine the volume of the intersection of a voxel set
// with an element.  Checking voxel by voxel is too slow, so we need a
// method that uses only the boundary (B) of the voxel set (VS).

// The VSB is a polyhedron which need not be either convex or simply
// connected.  It's represented by a graph, where each node of the
// graph corresponds to a corner of the polyhedron, and each edge of
// the graph connects the two nodes that correspond to the endpoints
// of an edge of the polyhedron.  There is no class representing
// edges, but each node knows its neighbors, as well as its position
// in space.  Each node has exactly 3 neighbors.  Where the polyhedron
// has corners with more than three edges, the graph contains multiple
// nodes with the same position.

// Actually, the VSB is represented by a bunch of graphs.  The
// Microstructure is split into subregions and a graph is constructed
// for each subregion.  This allows the expensive graph clipping
// operation to be skipped for large parts of the Microstructure when
// computing an Element's homogeneiety.

// There are three main parts to the calculation.
// (1) Constructing the graph representation of the VSB.
// (2) Clipping the VSB by planes (the faces of a Skeleton element).
// (3) Computing the volume of the clipped polyhedron.

// The graphs are VSBGraph objects, and are contained in a
// VoxelSetBoundary object.  (The VoxelSetBoundary contains a bit more
// information than the VSBGraphs, but pretty much passes all of its
// work to the graphs.)  The graphs are constructed by
// CMicrostructure::categorize(), which creates a 3D array,
// protoNodes, of ProtoVSBNode pointers at the corners of every voxel
// in each graph's subregion of the Microstructure.  Each point in
// protoNodes is the center of a 2x2x2 cube of voxels, but only some
// of the 8 voxels are occupied (ie, in the voxel set). (The 2x2x2
// cubes on the edges of the Microstructure always contain some
// unoccupied voxels.)  At the locations in the array where the
// configuration of voxels in the 2x2x2 cube defines a corner of the
// polyhedron, an instance of a ProtoVSBNode subclass is created.

// ProtoVSBNodes are different from VSBNodes.  There is never more
// than one ProtoVSBNode at a point, and ProtoVSBNodes may have up to
// six ProtoVSBNode neighbors.  VSBNodes always have three neighbors,
// but there may be more than one (up to seven!) VSBNodes at a point.
// There is only one type of VSBNode, but there are many different
// subclasses of ProtoNode.

// There are different subclasses of ProtoVSBNode for different
// configurations of voxels in the local 2x2x2 cube.  To avoid having
// to code all 256 possibilities, voxel arrangements that can be
// rotated into one another are in the same subclass, and each
// ProtoVSBNode instance contains a rotation (VoxRot instance) that
// maps its reference space axes (VoxelEdgeDirection instances) to the
// real space axes.  The occupied/unoccupied status of the voxels in
// the cube is encoded in the bits of an unsigned char (called a voxel
// signature), which is used to look up the ProtoVSBNode type and
// orientation in a table.  VoxelSetBoundary::protoVSBNodeFactory()
// returns a pointer to a new ProtoVSBNode of the correct type.  It
// returns nullptr if the arrangement of voxels doesn't define a
// corner of the polyhedron.

// The voxel signatures of the eight single voxel configurations are
// predefined and named "vox000", "vox100", etc, up to "vox111".  The
// three digits are the xyz coordinates of the voxel.  vox000 is on
// the negative x, negative y, negative z side of the 2x2x2 cube.
// vox111 is diagonally opposite.  The signature of any multi-voxel
// configuration can be constructed by the bitwise-or of the
// signatures of its individual voxels, so the configurations are
// referred to as "vox000|vox110", etc.

// When each ProtoVSBNode is created, it creates one or more VSBNodes
// in the VSBGraph, which stores pointers to them in a std::vector.
// It *doesn't* use a 3D array -- there may be more than one VSBNode
// at any point, and the geometrical organization isn't needed after
// construction is complete.  The number of VSBNodes per ProtoVSBNode
// depends on the voxel geometry, which is known to the ProtoVSBNode
// subclass.

// After creating the ProtoVSBNodes, CMicrostructure::categorize()
// calls ProtoVSBNode::connect() to set the nodes' neighbor pointers.
// If a ProtoVSBNode needs a neighbor in the +x, +y, or +z direction
// (in real space), categorize() finds the next ProtoVSBNode in that
// direction and calls connect().  Each ProtoVSBNode subtype knows in
// which directions its neighbors lie, and how to arrange them so that
// they're ordered correctly for the clipping and volume calculations.
// (See below.)  The rule is that the neighbors (edges) of a VSBNode
// must be ordered clockwise when viewed from the outside of the
// polyhedron.

// In the simplest situations (ProtoVSBNode subclasses SingleVoxel,
// SevenVoxels, etc), ProtoVSBNode::connect() works by passing its
// VSBNode* to the other ProtoVSBNode's connectBack() method, which
// returns the other ProtoVSBNode's VSBNode*.  The two ProtoVSBNodes
// can thereby insert the neighboring VSBNode pointers in their local
// VSBNodes' neighbor lists.

// One subtlety in connecting neighbors occurs when two occupied
// voxels in the 2x2x2 cube share an edge.  For example, the two
// voxels in configuration "vox000|vox110" share the edge in the
// negative z direction.  In these cases (TwoVoxelsByEdge,
// SixVoxelsByEdge, etc), there will be at least two VSBNodes at the
// center of the cube, and at least two VSBNodes in the next
// ProtoVSBNode in the direction of the shared edge.  It's important
// to connect the correct VSBNodes to each other at either end of the
// edge, or else the graph won't correctly represent the polyhedron,
// and the clipping and volume routines will fail.  For this,
// ProtoVSBNode::connect calls the neighboring ProtoVSBNode's
// connectDoubleBack method, passing in two VSBNode*s and getting two
// in return.  connect() and connectDoubleBack() use
// ProtoVSBNode::voxelOrder() to ensure that the neighbors are paired
// correctly.  voxelOrder() takes two single-voxel signatures in the
// ProtoVSBNode's reference space, rotates them into real space, and
// returns true if the first voxel's location in the 2x2x2 cube is
// greater than the second one's.  The voxels defining the doubled
// edge must have the same relative real space positions in both
// ProtoVSBNodes, so voxelOrder()s return value indicates if the
// arguments or return values of connectDoubleBack need to be swapped.

// The second subtlety in connecting neighbors concerns how multiple
// VSBNodes are arranged in a single ProtoNode.  The simplest
// non-trivial situation is when two voxels touch at a corner
// (TwoVoxelsByCorner, signature vox000|vox111 and equivalents).  In
// this case, there are two completely independent VSBNodes.  One
// connects to the +x, +y, and +z neighbors and one to the -x, -y, and
// -z neighbors.  The case vox000|vox110 (TwoVoxelsByEdge) also has
// two independent VSBNodes, but they share a doubled edge in the -z
// direction.  In more complicated cases, two VSBNodes may actually
// need to be neighbors of each other.  For example,
// vox000|vox100|vox010|vox011 (ChiralR) has four outgoing edges, so
// it needs two VSBNodes that are connected to each other.  There are
// configurations (Pyramid, FiveVoxByEdges) with six outgoing edges,
// which require six VSBNodes arranged in an infinitesimal hexagon, each
// connected to two co-located VSBNodes.

// Finally, there is one set of configurations (ThreeTwoOne,
// vox000|vox110|vox111) which is most conveniently resolved by
// creating a VSBNode with only two neighbors, and removing that node
// later.  This is because this configuration consists of one edge
// that passes straight through the 2x2x2 cube (-z and +z) and another
// edge that coincides with the first edge in the -z direction but
// joins the -x and -y edges instead of passing through.  All such
// VSBNodes with only two neighbors are stored in the VoxelSetBoundary
// when they're created and are cleaned up after all connections are
// made.

// After all the VSBNodes are connected, the ProtoVSBNodes are
// deleted.

// The second main part of the computation is using the VSBGraph to
// compute the graph of a clipped polyhedron, This is more or less a
// straight implementation of Powell and Abel's r3d algorithm.  See
// git@github.com:devonmpowell/r3d.git.  The differences are:

// * We're using C++ instead of C.
// * We don't have a fixed maximum size for the graph, but use dynamic
//   allocation.
// * Instead of manipulating vectors of integer indices, we use
//   vectors of pointers to VSBNodes, mostly.
// * We want to be able to clip the same graph multiple times because
//   each VSB intersects many Skeleton elements, so instead of just
//   clipping in place, we have two methods, VSBGraph::copyAndClip()
//   and VSBGraph::clipInPlace().  copyAndClip() is used to clip to
//   the first element face, and clipInPlace() is used for the rest.
// * For the same reason, we don't store the distances from the nodes
//   to the clipping plane in the VSBNodes.

// The clipping algorithm is

// * Compute signed distances from all VSBNodes to the clipping plane.
//   Nodes with distance < 0 are to be kept.
// * For each edge with one node on each side of the plane (distance <
//   0 for one and distance >= 0 for the other) create a new node on
//   the plane by interpolating the positions of two endpoints.
//   Connect the new node to the one being kept, and discard the other
//   one.
// * Discard all other nodes with distance >= 0.
// * The new nodes now have only one neighbor.  They're at the
//   perimeter of one or more "holes" where a bunch of nodes have been
//   clipped out of the graph.  Because the neighbors stored in each
//   VSBNode are ordered (going CW around the node as viewed from
//   outside the polyhedron), it's possible to start at one new node
//   and trace through the graph to find the next new node (ie, the
//   next node with fewer than 3 neighbors) on the perimeter of the
//   same hole, by always leaving a node on the edge that's CCW from
//   the incoming edge.  Connect each new node with the next one.

// The actual clipping routines, copyAndClip() and clipInPlace() are a
// bit more complex because they have to some bookkeeping that's not
// described here.

// If the initial unclipped polyhedron is not convex, then clipped
// polyhedron can include incorrect edges.  However, these edges will
// be part of oppositely oriented coplanar faces, so they have no
// effect on the computed volume.

// Finding the volume of a polyhedron relies on the same CW neighbor
// ordering that's used by the clipping routines.

// * Pick an unused node and edge of the polyhedron.

// * By choosing an exit edge that's CCW from the entrance edge, move
//   from node to node until you get back to where you started.  This
//   traces out a facet of the polyhedron.  Mark all the (node, exit
//   edge) pairs as "used".
// * Compute the area vector of the facet by taking cross products of
//   edges.
// * Compute the facet's contribution to the volume from the dot
//   product of the area vector with the a vector from the center of
//   the polyhedron to the facet.

// There are also two debugging routines:

// * checkEdges() just checks that each node has three neighbors, and
//   that if A is a neighbor of B, then B is a neighbor of A.

// * checkConnectivity() checks that the graph has three-vertex
//   connectivity, which means that removing two vertices from the
//   graph doesn't divide it into two disconnected parts.  Because the
//   graph is allowed to have disconnected portions, this test applies
//   to each disconnected subgraph individually.  Three-vertex
//   connectivity is necessary for a well formed graph for a CONVEX
//   polygon.  I don't know if it's sufficient.  checkConnectivity()
//   is very slow (o(N^3)) and should only be run for small graphs, or
//   if you have a lot of free time.

#include "common/IO/canvaslayers.h"
#include "common/IO/oofcerr.h"
#include "common/geometry.h"
#include "common/voxelsetboundary.h"
#include "common/cmicrostructure.h"
#include "common/printvec.h"
#include <limits>

#define swap(x, y) { auto temp = (x); x = (y); y = temp; }

#ifdef DEBUG
static bool verbose = false;
void setVerboseVSB(bool f) { verbose = f; }
bool verboseVSB() { return verbose; }
#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelEdgeDirection::VoxelEdgeDirection(unsigned int ax, int d)
  : axis(ax),
    dir(d)
{
  assert(axis >=0 && axis <= 2);
  assert(dir == 1 || dir == -1);
}

VoxelEdgeDirection::VoxelEdgeDirection(const Coord3D &vec) {
  // This constructor uses Coord3D instead of ICoord3D because its
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

VoxelEdgeDirection VoxelEdgeDirection::reverse() const {
  return VoxelEdgeDirection(axis, -dir);
}

// Which of the two given ICoord3Ds has the larger component in this
// direction?  Return 1 if i0 is greater, -1 if i1 is greater, and 0
// if they're the same.

int VoxelEdgeDirection::compare(const ICoord3D &i0, const ICoord3D &i1) const {
  int d = (i0[axis] - i1[axis]) * dir;
  return d == 0 ? 0 : (d > 0 ? 1 : -1);
}

static const VoxelEdgeDirection posX(0, 1);
static const VoxelEdgeDirection negX(0, -1);
static const VoxelEdgeDirection posY(1, 1);
static const VoxelEdgeDirection negY(1, -1);
static const VoxelEdgeDirection posZ(2, 1);
static const VoxelEdgeDirection negZ(2, -1);

static VoxelEdgeList allDirs({posX, negX, posY, negY, posZ, negZ});

std::ostream &operator<<(std::ostream &os, const VoxelEdgeDirection &dir) {
  if(dir == posX)
    os << "posX";
  else if(dir == posY)
    os << "posY";
  else if(dir == posZ)
    os << "posZ";
  else if(dir == negX)
    os << "negX";
  else if(dir == negY)
    os << "negY";
  else if(dir == negZ)
    os << "negZ";
  else
    os << "VoxelEdgeDirection(" << dir.axis << "," << dir.dir << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A voxel signature indicates which voxels in the 2x2x2 cube
// surrounding a point are in the voxel category of interest.  It's
// stored in a char, with one bit for each of the eight voxels.  The
// order of the bits in the char is determined by the loops in
// CMicrostructure::voxelSignature.  The innermost loop is over x and
// the outermost is over z.

// Voxel signatures for the single voxels of the 2x2x2 cube are named
// here.  The names say whether the x, y, and z component of the voxel
// position is on the positive side (1) or negative side (0) of the
// cube.  These values can be simply added together to get the
// signature for a multi-voxel group.

// These aren't static because they're swigged and used in the test
// suite.
unsigned char vox000 = 0x01;
unsigned char vox100 = 0x02;
unsigned char vox010 = 0x04;
unsigned char vox110 = 0x08;
unsigned char vox001 = 0x10;
unsigned char vox101 = 0x20;
unsigned char vox011 = 0x40;
unsigned char vox111 = 0x80;

static unsigned char voxelALL = 0xff;
static unsigned char voxelNONE = 0x00;

static ICoord3D singleVoxelOffset(unsigned char voxel) {
  // There must be a more elegant way of doing this, but this is
  // probably more efficient.
  if(voxel == vox000)
    return ICoord3D(-1, -1, -1);
  if(voxel == vox100)
    return ICoord3D(1, -1, -1);
  if(voxel == vox010)
    return ICoord3D(-1, 1, -1);
  if(voxel == vox110)
    return ICoord3D(1, 1, -1);
  if(voxel == vox001)
    return ICoord3D(-1, -1, 1);
  if(voxel == vox101)
    return ICoord3D(1, -1, 1);
  if(voxel == vox011)
    return ICoord3D(-1, 1, 1);
  if(voxel == vox111)
    return ICoord3D(1, 1, 1);
  throw ErrProgrammingError("Unexpected argument to singleVoxelOffset!",
			    __FILE__, __LINE__);
}

std::string &printSig(unsigned char sig) {
  // Store a copy of each signature string, and return a reference to
  // it, because swig does strange things with bare std::string return
  // types.  We need to return a reference to a permanent object.
  static std::map<unsigned char, std::string> sigdict;
  auto s = sigdict.find(sig);
  if(s != sigdict.end())
    return s->second;
  std::vector<std::string> voxels;
  if(sig & vox000) voxels.push_back("vox000");
  if(sig & vox100) voxels.push_back("vox100");
  if(sig & vox010) voxels.push_back("vox010");
  if(sig & vox110) voxels.push_back("vox110");
  if(sig & vox001) voxels.push_back("vox001");
  if(sig & vox101) voxels.push_back("vox101");
  if(sig & vox011) voxels.push_back("vox011");
  if(sig & vox111) voxels.push_back("vox111");
  if(voxels.empty())
    sigdict[sig] = "voxelNONE";
  else if(voxels.size() == 8)
    sigdict[sig] = "voxelALL";
  else if(voxels.size() == 1)
    sigdict[sig] = voxels[0];
  else {
    for(unsigned int i=1; i<voxels.size(); i++)
      voxels[0] += "|" + voxels[i];
    sigdict[sig] = voxels[0];
  }
  return sigdict[sig];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A VoxRot (VoxelRotation) maps axes in the actual configuration to
// axes in the reference configuration and vice versa.  The arguments
// to the constructor are the actual space directions that correspond
// to the +x, +y, and +z directions in the reference space.

VoxRot::VoxRot(VoxelEdgeDirection d0, VoxelEdgeDirection d1,
	       VoxelEdgeDirection d2)
  : actualAxes({d0, d1, d2})
{
#ifdef DEBUG
  if(d0.axis == d1.axis || d1.axis == d2.axis || d2.axis == d0.axis) {
    oofcerr << "VoxRot::VoxRot: d0=" << d0 << " d1=" << d1 << " d2=" << d2
	    << std::endl;
    throw ErrProgrammingError("Badly specified voxel rotation!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
}

VoxelEdgeDirection VoxRot::toActual(const VoxelEdgeDirection &d) const
{
  if(d.dir == 1)
    return actualAxes[d.axis];
  return actualAxes[d.axis].reverse();
}

VoxelEdgeDirection VoxRot::toReference(const VoxelEdgeDirection &d) const
{
  // d is a direction in the actual space.  Find which of the
  // actualAxes is in the same direction (up to a sign).  TODO: This
  // could be done with a table lookup, but then the VoxRot
  // object would need a lot more data.  Or we could precompute the 24
  // possible rotations and re-use the objects.
  for(int c=0; c<3; c++) {
    if(actualAxes[c].axis == d.axis) {
      // actualAxes[c] is the actual-space direction corresponding to
      // the positive orientation of reference space vector c.  If the
      // actual space direction d is in oppositely oriented, return
      // the negative oriention of the reference space vector.
      return VoxelEdgeDirection(c, d.dir*actualAxes[c].dir);
    }
  }
  throw ErrProgrammingError("VoxRot::toReference failed!",
			    __FILE__, __LINE__);
}

static const VoxRot noRotation(posX, posY, posZ);

std::ostream &operator<<(std::ostream &os, const VoxRot &rotation) {
  os << "[" << rotation.actualAxes[0] << "," << rotation.actualAxes[1]
     << "," << rotation.actualAxes[2] << "]";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ProtoVSBNode::ProtoVSBNode(const VoxRot &rot)
  : rotation(rot)
{}

VoxelEdgeDirection ProtoVSBNode::getReferenceDir(const ProtoVSBNode *that)
  const
{
  // Return the direction from this node to that node
  return rotation.toReference(
		      VoxelEdgeDirection(that->position() - position()));
}

// Given two voxels, decide if they're in canonical order or not. The
// answer is arbitrary, but must be the same for the other
// ProtoVSBNode that shares the two voxels.  The voxels are specified
// by the single voxel signatures, which define where they are
// relative to the center of the current ProtoVSBNode in its reference
// orientation.  The comparison is made using the *actual*
// orientation, so that it can be compared to a different
// ProtoVSBNode's view of the same two voxels.

bool ProtoVSBNode::voxelOrder(unsigned char sig0, unsigned char sig1) const {
  // Get the positions of the voxels relative to the center of the
  // 2x2x2 cube.
  assert(sig0 != sig1);
  ICoord3D v0 = singleVoxelOffset(sig0);
  ICoord3D v1 = singleVoxelOffset(sig1);
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
}

#ifdef DEBUG
void ProtoVSBNode::checkDir(const VoxelEdgeDirection &dir) const {
  for(VoxelEdgeDirection allowed : connectDirs()) {
    if(allowed == dir)
      return;
  }
  oofcerr << "ProtoVSBNode::checkDir: this=" << *this
	  << " dir=" << dir << std::endl;
  oofcerr << "ProtoVSBNode::checkDir: connectDirs=";
  std::cerr << connectDirs();
  oofcerr << std::endl;
  throw ErrProgrammingError("ProtoVSBNode::checkDir failed!",
			    __FILE__, __LINE__);
}

std::ostream &operator<<(std::ostream &os, const ProtoVSBNode &pnode) {
  pnode.print(os);
  return os;
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void SingleNode::makeVSBNodes(VSBGraph *graph, const ICoord3D &here)
{
  vsbNode = new VSBNode(here);
  graph->addNode(vsbNode);
}

const Coord3D &SingleNode::position() const {
  assert(vsbNode != nullptr);
  return vsbNode->position;
}

void ProtoVSBNode::connectDoubleBack(const ProtoVSBNode*, VSBNode*, VSBNode*,
				     VSBNode*&, VSBNode*&)
{
  throw ErrProgrammingError("connectDoubleBack called illegally!",
			    __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const Coord3D &DoubleNode::position() const {
  assert(vsbNode0 != nullptr);
  return vsbNode0->position;
}

const Coord3D &TripleNode::position() const {
  assert(vsbNode0 != nullptr);
  return vsbNode0->position;
}

const Coord3D &MultiNode::position() const {
  assert(vsbNodes[0] != nullptr);
  return vsbNodes[0]->position;
}

void DoubleNode::makeVSBNodes(VSBGraph *graph, const ICoord3D &here) {
  vsbNode0 = new VSBNode(here);
  vsbNode1 = new VSBNode(here);
  graph->addNode(vsbNode0);
  graph->addNode(vsbNode1);
}

void TripleNode::makeVSBNodes(VSBGraph *graph, const ICoord3D  &here) {
  vsbNode0 = new VSBNode(here);
  vsbNode1 = new VSBNode(here);
  vsbNode2 = new VSBNode(here);
  graph->addNode(vsbNode0);
  graph->addNode(vsbNode1);
  graph->addNode(vsbNode2);
}

void MultiNode::makeVSBNodes(VSBGraph *graph, const ICoord3D  &here) {
  for(unsigned int i=0; i<vsbNodes.size(); i++) {
    vsbNodes[i] = new VSBNode(here);
    graph->addNode(vsbNodes[i]);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// For a node at the corner of a single voxel, the reference
// configuration in the 2x2x2 cube has the voxel in the +x, +y, +z
// corner (vox111) and the neighbors in the +x, +y, +z directions.

class SingleVoxel : public SingleNode {
public:
  SingleVoxel(const VoxRot &rot)
    : SingleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new SingleVoxel(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    // The neighbors are in the +x, +y, and +z directions, so
    // inserting them in the neighbor list in that order puts them
    // CW when viewed from outside (from the -x, -y, -z side).
    vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SingleVoxel(" << printSig(signature) << ", " << rotation
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

class SevenVoxels : public SingleNode {
public:
  SevenVoxels(const VoxRot &rot)
    : SingleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new SevenVoxels(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    // The neighbors are in the +x, +y, and +z directions, but
    // inserting them in the neighbor list in otherproto order would puts
    // them CCW when viewed from outside (from the +x, +y, +z side).
    // They're supposed to be CW, so switch 0 and 2.
    vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(2-dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SevenVoxels(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG

};

//--------

// Two voxels that share an edge.

class TwoVoxelsByEdge : public DoubleNode {
public:
  TwoVoxelsByEdge(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new TwoVoxelsByEdge(rotation); }

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

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // The edges of vox000 connect to vsbNode0 and the edges of
    // vox110 to vsbNode1.  vox000's edges are negY, negX, negZ, in
    // that order (CW as viewed from outside (from +x+y+z).
    // Similarly, vox110's edges are posY, posX, negZ.
    if(dir == negX || dir == negY) {
      // Connect to vox000's edges, using vsbNode0.
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      // Since dir.axis is 0 or 1, 1-dir.axis gives us the order we want.
      vsbNode0->setNeighbor(1-dir.axis, othernode); 
    }
    else if(dir == posX || dir == posY) {
      // Connect to vox110's edges, using vsbNode1.
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(1-dir.axis, othernode);
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
      bool ordered = voxelOrder(vox000, vox110);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX || dir == negY) {
      vsbNode0->setNeighbor(1-dir.axis, othernode);
      return vsbNode0;
    }
    if(dir == posX || dir == posY) {
      vsbNode1->setNeighbor(1-dir.axis, othernode);
      return vsbNode1;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in TwoVoxelsByEdge::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox000, vox110);
    node0 = ordered ? vsbNode0 : vsbNode1;
    node1 = ordered ? vsbNode1 : vsbNode0;
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByEdge(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};  // end class TwoVoxelsByEdge

//-------------

// Two voxels that touch at a corner.

class TwoVoxelsByCorner : public DoubleNode {
public:
  TwoVoxelsByCorner(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new TwoVoxelsByCorner(rotation);}

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }
  
  virtual void connect(ProtoVSBNode *otherproto) {
    // TwoVoxelsByCorner is easier than TwoVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 connect to vsbNode0, and
    // the edges on vox111 connect to vsbNode1.  There's no
    // consistency to maintain at the other end of a doubled edge.
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      // The edges around vox000 in CW order when viewed from +x+y+z
      // are negZ, negY, negX. 
      vsbNode0->setNeighbor(2-dir.axis, othernode);
    }
    else {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      // The edges around vox111 in CW order when viewed from -x-y-z
      // are posX, posY, pozY.
      vsbNode1->setNeighbor(dir.axis, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {
      vsbNode0->setNeighbor(2-dir.axis, othernode);
      return vsbNode0;
    }
    vsbNode1->setNeighbor(dir.axis, othernode);
    return vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "TwoVoxelsByCorner(" << printSig(signature) << ", " << rotation
       << ")";
  }
#endif // DEBUG
};	// end class TwoVoxelsByCorner
  
//--------

// SixVoxelsByEdge is the inverse of TwoVoxelsByEdge

class SixVoxelsByEdge : public DoubleNode {
public:
  SixVoxelsByEdge(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new SixVoxelsByEdge(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    // The reference configuration all voxels *except* vox000 and
    // vox110.  There are edges in the posX, negX, posY, negY, and
    // negZ directions.
    static const VoxelEdgeList v({posX, negX, posY, negY, negZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // The edges on vox100 connect to vsbNode0 and the edges on vox010
    // connect to vsbNode1.  Edges on vox100 are posX, negY, negZ.
    // Edges on vox010 are negX, posY, negZ.
    if(dir == posX || dir == negY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(dir.axis, othernode); 
    }
    else if(dir == negX || dir == posY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(dir.axis, othernode);
    }
    else {
      assert(dir == negZ);
      bool ordered = voxelOrder(vox100, vox010);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered? vsbNode1 : vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == posX || dir == negY) {
      vsbNode0->setNeighbor(dir.axis, othernode);
      return vsbNode0;
    }
    else if(dir == negX || dir == posY) {
      vsbNode1->setNeighbor(dir.axis, othernode);
      return vsbNode1;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in SixVoxelsByEdge::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox100, vox010);
    node0 = ordered ? vsbNode0 : vsbNode1;
    node1 = ordered ? vsbNode1 : vsbNode0;
    node0->setNeighbor(2, othernode0);
    node1->setNeighbor(2, othernode1);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByEdge(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};  // end class SixVoxelsByEdge

//--------

// SixVoxelsByCorner is the inverse of TwoVoxelsByCorner

class SixVoxelsByCorner : public DoubleNode {
public:
  SixVoxelsByCorner(const VoxRot &rot)
    : DoubleNode(rot)
  {}
  virtual ProtoVSBNode *clone() const { return new SixVoxelsByCorner(rotation);}

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    // SixVoxelsByCorner is easier than SixVoxelsByEdge, because there
    // aren't two connections going out in the same direction.  We can
    // simply say that the edges on vox000 (which is a hole) connect
    // to vsbNode0, and the edges on vox111 (also a hole) connect to
    // vsbNode1.  There's no consistency to maintain at the other end
    // of a doubled edge.
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {		// negX, negY, or negZ
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      // The edges around vox000 in CW order when viewed from -x-y-z
      // are negX, negY, negZ. 
      vsbNode0->setNeighbor(dir.axis, othernode);
    }
    else {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      // The edges around vox111 in CW order when viewed from +x+y+z
      // are posZ, posY, pozX.
      vsbNode1->setNeighbor(2-dir.axis, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir.dir == -1) {
      vsbNode0->setNeighbor(dir.axis, othernode);
      return vsbNode0;
    }
    vsbNode1->setNeighbor(2-dir.axis, othernode);
    return vsbNode1;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "SixVoxelsByCorner(" << printSig(signature) << ", " << rotation
       << ")";
  }
#endif // DEBUG
};
  
//----------

// Three voxels in an L configuration.  The node does not need to be
// split.  The reference configuration is vox000, vox100,
// vox010, with edges posX, posY, negZ in that order.

class ThreeVoxL : public SingleNode {
public:
  ThreeVoxL(const VoxRot &rot)
    : SingleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new ThreeVoxL(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    vsbNode->setNeighbor(dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxL(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

// ----------

// FiveVoxL is the inverse of ThreeVoxL.  The connections are
// the same, but the order is reversed.

class FiveVoxL : public SingleNode {
public:
  FiveVoxL(const VoxRot &rot)
    : SingleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new FiveVoxL(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negZ, posX, posY});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNode);
    vsbNode->setNeighbor(2-dir.axis, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    vsbNode->setNeighbor(2-dir.axis, othernode);
    return vsbNode;
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxL(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//---------

// ThreeTwoOne is three voxels, two stacked face to face and a third
// connected to one of the other two along an edge.  There are 24
// orientations.  The reference configuration contains voxels 000,
// 111, and 110.

class ThreeTwoOne : public DoubleNode {
public:
  ThreeTwoOne(const VoxRot &rot)
    : DoubleNode(rot)
  {}
  
  virtual ProtoVSBNode *clone() const { return new ThreeTwoOne(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(VSBGraph *graph, const ICoord3D &here) {
    vsbNode0 = new VSBNode(here);
    vsbNode1 = new VSBNode(here);
    graph->addNode(vsbNode0);
    graph->twoFoldNode(vsbNode1);
    // Don't add vsbNode1 to the graph! It's not a real node.
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // See comments in TwoVoxelsByEdge.  This is similar, but the
    // edges on vox110 are different, and its VSBNode will only be
    // connected to two edges, so we have to tell the VSB about it.
    // VSBNode0 is the 3-fold node, with edges on vox000 in the negX,
    // negY, and negZ directions.  VSBNode1 is the 2-fold node, on
    // vox110 and vox111, with edges negZ and posZ.
    
    if(dir == negX || dir == negY) {
      // Connecting to the edges on vox000
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(1-dir.axis, othernode);
    }
    else if(dir==posZ) {
      // Connecting to the edges on vox110
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.  To ensure compatibility
      // with the other ends of edge, use voxelOrder to determine the
      // order of the input and output args to connectDoubleBack.
      assert(dir == negZ);
      bool ordered = voxelOrder(vox000, vox110);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX || dir == negY) {
      vsbNode0->setNeighbor(1-dir.axis, othernode);
      return vsbNode0;
    }
    if(dir == posZ) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in ThreeTwoOne::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox000, vox110);
    if(ordered) {
      node0 = vsbNode0;
      node1 = vsbNode1;
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
    else {
      node0 = vsbNode1;
      node1 = vsbNode0;
      vsbNode0->setNeighbor(2, othernode1);
      vsbNode1->setNeighbor(1, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeTwoOne(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class ThreeTwoOne

//---------

// FiveTwoOne is the inverse of ThreeTwoOne.  The reference
// configuration contains all voxels except vox000, vox111, and
// vox110.  That means that vox100 and vox010 touch along an edge.
// The case is treated completely differently from ThreeTwoOne,
// because it's not possible to resolve the doubled edge in a unique
// way.  So here we add an extra (third) node and avoid a doubled
// edge.  It's not possible to resolve ThreeTwoOne in this way because
// it would lead to an insufficiently connected graph.

class FiveTwoOne : public TripleNode {
public:
  FiveTwoOne(const VoxRot &rot)
    : TripleNode(rot)
  {
  }
  
  virtual ProtoVSBNode *clone() const { return new FiveTwoOne(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({negY, negX, negZ, posZ});
    return v;
  }

  void makeVSBNodes(VSBGraph *graph, const ICoord3D &here) {
    TripleNode::makeVSBNodes(graph, here);
    vsbNode0->setNeighbor(2, vsbNode2);
    vsbNode1->setNeighbor(1, vsbNode2);
    vsbNode2->setNeighbor(2, vsbNode0);
    vsbNode2->setNeighbor(1, vsbNode1);
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // vsbNode0 connects the negY, negZ edges of vox100 and vsbNode1
    // connects the negX, negZ edges of vox010.  Both also connect to
    // vsbNode2, which connects the posZ edge as well.
    
    if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir==posZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode2);
      vsbNode2->setNeighbor(0, othernode);
    }
    else {
      // The double edge coming in on negZ.
      assert(dir == negZ);
      bool ordered = voxelOrder(vox100, vox010);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNode0->setNeighbor(1, othernode0);
      vsbNode1->setNeighbor(2, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    if(dir == negY) {
      vsbNode0->setNeighbor(0, othernode);
      return vsbNode0;
    }
    if(dir == posZ) {
      vsbNode2->setNeighbor(0, othernode);
      return vsbNode2;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in FiveTwoOne::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
#ifdef DEBUG
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    assert(dir == negZ);
#endif // DEBUG
    bool ordered = voxelOrder(vox100, vox010);
    if(ordered) {
      node0 = vsbNode0;
      node1 = vsbNode1;
      vsbNode0->setNeighbor(1, othernode0);
      vsbNode1->setNeighbor(2, othernode1);
    }
    else {
      node0 = vsbNode1;
      node1 = vsbNode0;
      vsbNode0->setNeighbor(1, othernode1);
      vsbNode1->setNeighbor(2, othernode0);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveTwoOne(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class FiveTwoOne

//--------

// Three voxels that each share an edge with both of the others.  

class ThreeVoxByEdges : public TripleNode {
public:
  ThreeVoxByEdges(const VoxRot &rot)
    : TripleNode(rot)
  {}

  virtual ProtoVSBNode *clone() const { return new ThreeVoxByEdges(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // The reference configuration is vox110 + vox011 + vox101.
    // There are doubled edges in the +x, +y, and +z directions and
    // single edges in the -x, -y, and -z directions.  We use vsbNode0
    // for the edges of vox110, vsbNode1 for 101, and vsbNode2 for
    // 011.
    if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode2);
      vsbNode2->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox110 (VSBNode0) and vox101 (VSBNode1)
      bool ordered = voxelOrder(vox110, vox101);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // The edges on vsbNode0 (vox110) are (negZ, posY, posX),
      // CW.  This is posX, so it goes in slot 2.
      vsbNode0->setNeighbor(2, othernode0);
      // The edges on vsbNode1 (vox101) are (negY, posX, posZ),
      // CW.  This is posX, so it goes in slot 1.
      vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox110 (VSBNode0) and vox011 (VSBNode2)
      bool ordered = voxelOrder(vox110, vox011);
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode2;
      VSBNode *node1 = ordered ? vsbNode2 : vsbNode0;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negZ, posY, posX).
      vsbNode0->setNeighbor(1, othernode0);
      // Edges are (negX, posZ, posY)
      vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox101 (VSBNode1) and vox011 (VSBNode2)
      bool ordered = voxelOrder(vox101, vox011);
      VSBNode *node0 = ordered ? vsbNode1 : vsbNode2;
      VSBNode *node1 = ordered ? vsbNode2 : vsbNode1;
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      // Edges are (negY, posX, posZ)
      vsbNode1->setNeighbor(2, othernode0);
      // Edges are (negX, posZ, posY)
      vsbNode2->setNeighbor(1, othernode1);
    }
  } // end connect()

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX) {
      vsbNode2->setNeighbor(0, othernode);
      return vsbNode2;
    }
    if(dir == negY) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(0, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in ThreeVoxByEdges::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = voxelOrder(vox110, vox101);
      node0 = vsbNode0;
      node1 = vsbNode1;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode0->setNeighbor(2, othernode0);
      vsbNode1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox110, vox011);
      node0 = vsbNode0;
      node1 = vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode0->setNeighbor(1, othernode0);
      vsbNode2->setNeighbor(2, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = voxelOrder(vox101, vox011);
      node0 = vsbNode1;
      node1 = vsbNode2;
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNode1->setNeighbor(2, othernode0);
      vsbNode2->setNeighbor(1, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ThreeVoxByEdges(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class ThreeVoxByEdges

//-----------

// FiveVoxByEdges is the inverse of ThreeVoxByEdges, but has to be
// treated more like Pyramid with an extra voxel.  The reference
// configuration is all voxels except vox110, vox011, and vox101.

class FiveVoxByEdges : public MultiNode {
public:
  FiveVoxByEdges(const VoxRot &rot)
    : MultiNode(7, rot)
  {}

  virtual ProtoVSBNode *clone() const { return new FiveVoxByEdges(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void makeVSBNodes(VSBGraph *graph, const ICoord3D &here) {
    MultiNode::makeVSBNodes(graph, here);
    for(unsigned int i=0; i<6; i++) {
      // Same as Pyramid::makeVSBNodes()
      vsbNodes[i]->setNeighbor(2, vsbNodes[(i+5)%6]);
      vsbNodes[i]->setNeighbor(1, vsbNodes[(i+1)%6]);
    }
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // The reference configuration is ~(vox110|vox011|vox101).  There
    // are doubled edges in the +x, +y, and +z directions and single
    // edges in the -x, -y, and -z directions.  Nodes vsbNodes[0]
    // through vsbNodes[5] form an infinitesimal hexagon at the
    // junction of voxels 100, 001, and 010.  vsbNodes[6] links the
    // edges of vox111, which are coincident the the +x, +y, and +z
    // edges of the other voxels.
    if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNodes[3]);
      vsbNodes[3]->setNeighbor(0, othernode);
    }
    else if(dir == negY) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNodes[1]);
      vsbNodes[1]->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNodes[5]);
      vsbNodes[5]->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      // Two edges between vox100 and vox111
      bool ordered = voxelOrder(vox100, vox111);
      VSBNode *node0 = ordered ? vsbNodes[0] : vsbNodes[6];
      VSBNode *node1 = ordered ? vsbNodes[6] : vsbNodes[0];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[0]->setNeighbor(0, othernode0);
      vsbNodes[6]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      // Two edges between vox010 and vox111
      bool ordered = voxelOrder(vox010, vox111);
      VSBNode *node0 = ordered ? vsbNodes[4] : vsbNodes[6];
      VSBNode *node1 = ordered ? vsbNodes[6] : vsbNodes[4];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[4]->setNeighbor(0, othernode0);
      vsbNodes[6]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // Two edges between vox001 and vox111
      bool ordered = voxelOrder(vox001, vox111);
      VSBNode *node0 = ordered ? vsbNodes[2] : vsbNodes[6];
      VSBNode *node1 = ordered ? vsbNodes[6] : vsbNodes[2];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[2]->setNeighbor(0, othernode0);
      vsbNodes[6]->setNeighbor(2, othernode1);
    }
  } // end connect()

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == negX) {
      vsbNodes[3]->setNeighbor(0, othernode);
      return vsbNodes[3];
    }
    if(dir == negY) {
      vsbNodes[1]->setNeighbor(0, othernode);
      return vsbNodes[1];
    }
    if(dir == negZ) {
      vsbNodes[5]->setNeighbor(0, othernode);
      return vsbNodes[5];
    }
    throw ErrProgrammingError(
		      "Unexpected direction in FiveVoxByEdges::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = voxelOrder(vox100, vox111);
      node0 = vsbNodes[0];
      node1 = vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[0]->setNeighbor(0, othernode0);
      vsbNodes[6]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox010, vox111);
      node0 = vsbNodes[4];
      node1 = vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[4]->setNeighbor(0, othernode0);
      vsbNodes[6]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = voxelOrder(vox001, vox111);
      node0 = vsbNodes[2];
      node1 = vsbNodes[6];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[2]->setNeighbor(0, othernode0);
      vsbNodes[6]->setNeighbor(2, othernode1);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FiveVoxByEdges(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end FiveVoxByEdges

//--------------

// Four voxels in the shape of two perpendicular stacks of two voxels.
// This configuration is chiral and requires an additional node to be
// created, although there are no multiply connected edges.

class ChiralR : public DoubleNode {
public:
  ChiralR(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new ChiralR(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(VSBGraph *graph, const ICoord3D &here) {
    DoubleNode::makeVSBNodes(graph, here);
    vsbNode0->setNeighbor(0, vsbNode1);
    vsbNode1->setNeighbor(0, vsbNode0);
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // Connect posX and negZ to VSBNode0, and negX and posZ to VSBNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // VSBNode0's CW edges are [dummy], negZ, posX.
    // VSBNode1's CW edges are [dummy], negX, posZ.
    // The order of the edges is the reverse of the order in ChiralL.
    if(dir == posX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(2, othernode);
    }
    else if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == posZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(1, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == posX) {
      vsbNode0->setNeighbor(2, othernode);
      return vsbNode0;
    }
    if(dir == negX) {
      vsbNode1->setNeighbor(1, othernode);
      return vsbNode1;
    }
    if(dir == posZ) {
      vsbNode1->setNeighbor(2, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(1, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError("Unexpected direction in ChiralR::connectBack!",
			      __FILE__, __LINE__);
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralR(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//--------------

// The mirror image of ChiralR is ChiralL

class ChiralL : public DoubleNode {
public:
  ChiralL(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new ChiralL(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, negX, posZ, negZ});
    return v;
  }

  virtual void makeVSBNodes(VSBGraph *graph, const ICoord3D &here) {
    DoubleNode::makeVSBNodes(graph, here);
    vsbNode0->setNeighbor(0, vsbNode1);
    vsbNode1->setNeighbor(0, vsbNode0);
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    // Connect posX and negZ to VSBNode0, and negX and posZ to VSBNode1.
    // The two VSBNodes are already connected by a dummy edge, in makeVSBNodes.
    // VSBNode0's CW edges are [dummy], posX, negZ.
    // VSBNode1's CW edges are [dummy], posZ, negX.
    // The order of the edges is the reverse of the order in ChiralR.
    if(dir == posX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(1, othernode);
    }
    else if(dir == negX) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(2, othernode);
    }
    else if(dir == posZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(1, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(2, othernode);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == posX) {
      vsbNode0->setNeighbor(1, othernode);
      return vsbNode0;
    }
    if(dir == negX) {
      vsbNode1->setNeighbor(2, othernode);
      return vsbNode1;
    }
    if(dir == posZ) {
      vsbNode1->setNeighbor(1, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(2, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError("Unexpected direction in ChiralL::connectBack!",
			      __FILE__, __LINE__);
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "ChiralL(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//------------

// The Pyramid is 4 voxels stacked in a sort of skewed pyramid.  It
// contains one central voxel and the voxels on each of its faces.  An
// infinitesimal hexagonal face is inserted in the corner to convert
// the 6-fold vertex into 6 3-fold vertices.

class Pyramid : public MultiNode {
public:
  Pyramid(const VoxRot &rot)
    : MultiNode(6, rot)
  {}

  virtual ProtoVSBNode *clone() const { return new Pyramid(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void makeVSBNodes(VSBGraph *graph, const ICoord3D &here) {
    MultiNode::makeVSBNodes(graph, here);
    for(unsigned int i=0; i<6; i++) {
      // Neighbor 1 is the previous node in the hexagonal face.
      vsbNodes[i]->setNeighbor(1, vsbNodes[(i+5)%6]);
      // Neighbor 2 is the next node in the hexagonal face.
      vsbNodes[i]->setNeighbor(2, vsbNodes[(i+1)%6]);
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

  virtual void connect(ProtoVSBNode *otherproto) {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    VSBNode *othernode = otherproto->connectBack(this, vsbNodes[i]);
    vsbNodes[i]->setNeighbor(0, othernode);
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    unsigned int i = hexDirIndex(dir);
    vsbNodes[i]->setNeighbor(0, othernode);
    return vsbNodes[i];
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "Pyramid(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};

//----------

// Four voxels arranged in a checkerboard pattern, each sharing an
// edge with all of the others.  Each edge becomes a split edge, and
// there's one VSBNode for the inside corner of each voxel.

class CheckerBoard : public MultiNode {
public:
  CheckerBoard(const VoxRot &rot)
    : MultiNode(4, rot)
  {}

  ProtoVSBNode *clone() const { return new CheckerBoard(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    return allDirs;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    // The reference configuration is vox100 + vox010 + vox001 +
    // vox111.  Use VSBnodes[0] for vox100, 1 for vox010, 2 for
    // vox001, and 3 for vox111.  The assignment of neighbor indices
    // for the VSBNodes is arbitrary but consistent (and gets them all
    // CW, hopefully!)
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posX) {
      // The posX edge is between voxels 100 and 111, so it connects
      // to vsbNodes 0 and 3.
      bool ordered = voxelOrder(vox100, vox111);
      VSBNode *node0 = ordered ? vsbNodes[0] : vsbNodes[3];
      VSBNode *node1 = ordered ? vsbNodes[3] : vsbNodes[0];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[0]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      // negX is between voxels 001 and 010, connecting to vsbNodes 2
      // and 1.
      bool ordered = voxelOrder(vox001, vox010);
      VSBNode *node0 = ordered ? vsbNodes[2] : vsbNodes[1];
      VSBNode *node1 = ordered ? vsbNodes[1] : vsbNodes[2];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[2]->setNeighbor(1, othernode0);
      vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      // posY is between voxels 010 and 111, connecting to vsbNodes 1
      // and 3.
      bool ordered = voxelOrder(vox010, vox111);
      VSBNode *node0 = ordered ? vsbNodes[1] : vsbNodes[3];
      VSBNode *node1 = ordered ? vsbNodes[3] : vsbNodes[1];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[1]->setNeighbor(1, othernode0);
      vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      // negY is between voxels 001 and 100, connecting to vsbNodes 2
      // and 0.
      bool ordered = voxelOrder(vox001, vox100);
      VSBNode *node0 = ordered ? vsbNodes[2] : vsbNodes[0];
      VSBNode *node1 = ordered ? vsbNodes[0] : vsbNodes[2];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[2]->setNeighbor(2, othernode0);
      vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      // posZ is between voxels 001 and 111, connecting to vsbNodes 2
      // and 3.
      bool ordered = voxelOrder(vox001, vox111);
      VSBNode *node0 = ordered ? vsbNodes[2] : vsbNodes[3];
      VSBNode *node1 = ordered ? vsbNodes[3] : vsbNodes[2];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[2]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      // negZ is between voxels 100 and 010, connecting to vsbNodes 0
      // and 1.
      bool ordered = voxelOrder(vox100, vox010);
      VSBNode *node0 = ordered ? vsbNodes[0] : vsbNodes[1];
      VSBNode *node1 = ordered ? vsbNodes[1] : vsbNodes[0];
      VSBNode *othernode0, *othernode1;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      if(!ordered)
	swap(othernode0, othernode1);
      vsbNodes[0]->setNeighbor(2, othernode0);
      vsbNodes[1]->setNeighbor(2, othernode1);
    }
  } // end CheckerBoard::connect

  virtual VSBNode *connectBack(const ProtoVSBNode*, VSBNode*) {
    throw ErrProgrammingError("CheckerBoard::connectBack should not be called!",
			      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    // See comments in CheckerBoard::connect.
    if(dir == posX) {
      bool ordered = voxelOrder(vox100, vox111);
      node0 = vsbNodes[0];
      node1 = vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[0]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(2, othernode1);
    }
    else if(dir == negX) {
      bool ordered = voxelOrder(vox001, vox010);
      node0 = vsbNodes[2];
      node1 = vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[2]->setNeighbor(1, othernode0);
      vsbNodes[1]->setNeighbor(0, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox010, vox111);
      node0 = vsbNodes[1];
      node1 = vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[1]->setNeighbor(1, othernode0);
      vsbNodes[3]->setNeighbor(0, othernode1);
    }
    else if(dir == negY) {
      bool ordered = voxelOrder(vox001, vox100);
      node0 = vsbNodes[2];
      node1 = vsbNodes[0];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[2]->setNeighbor(2, othernode0);
      vsbNodes[0]->setNeighbor(1, othernode1);
    }
    else if(dir == posZ) {
      bool ordered = voxelOrder(vox001, vox111);
      node0 = vsbNodes[2];
      node1 = vsbNodes[3];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[2]->setNeighbor(0, othernode0);
      vsbNodes[3]->setNeighbor(1, othernode1);
    }
    else if(dir == negZ) {
      bool ordered = voxelOrder(vox100, vox010);
      node0 = vsbNodes[0];
      node1 = vsbNodes[1];
      if(!ordered) {
	swap(othernode0, othernode1);
	swap(node0, node1);
      }
      vsbNodes[0]->setNeighbor(2, othernode0);
      vsbNodes[1]->setNeighbor(2, othernode1);
    }
  }
#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "CheckerBoard(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};				// end class CheckerBoard

//-------------

// FourThreeOne is three voxels in an L with one more voxel out of the
// plane of the L and over the gap.

class FourThreeOne : public DoubleNode {
public:
  FourThreeOne(const VoxRot &rot)
    : DoubleNode(rot)
  {}

  ProtoVSBNode *clone() const { return new FourThreeOne(rotation); }

  virtual const VoxelEdgeList &connectDirs() const {
    static const VoxelEdgeList v({posX, posY, posZ, negZ});
    return v;
  }

  virtual void connect(ProtoVSBNode *otherproto) {
    // The reference configuration is three voxels in the Z=0 plane,
    // vox000, vox100 and vox010, just like ThreeVoxL, plus one voxel
    // at vox111.  The three in the L are connected to vsbNode0 and
    // the single voxel is connected to vsbNode1.  The edges in the
    // posX and posY directions are doubled.

    // Neighbor indexing for the edges of the single voxel at vox111
    // is posZ, posX, posY.  For the inside corner of the L it's negZ,
    // posX, posY.
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    checkDir(dir);
    if(dir == posZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode1);
      vsbNode1->setNeighbor(0, othernode);
    }
    else if(dir == negZ) {
      VSBNode *othernode = otherproto->connectBack(this, vsbNode0);
      vsbNode0->setNeighbor(0, othernode);
    }
    else if(dir == posX) {
      bool ordered = voxelOrder(vox100, vox111);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      // Conveniently the posX and posY neighbor indexing is the same
      // for both nodes.
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else {
      assert(dir == posY);
      bool ordered = voxelOrder(vox010, vox111);
      VSBNode *othernode0, *othernode1;
      VSBNode *node0 = ordered ? vsbNode0 : vsbNode1;
      VSBNode *node1 = ordered ? vsbNode1 : vsbNode0;
      otherproto->connectDoubleBack(this, node0, node1, othernode0, othernode1);
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
  }

  virtual VSBNode *connectBack(const ProtoVSBNode *otherproto,
			       VSBNode *othernode)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posZ) {
      vsbNode1->setNeighbor(0, othernode);
      return vsbNode1;
    }
    if(dir == negZ) {
      vsbNode0->setNeighbor(0, othernode);
      return vsbNode0;
    }
    throw ErrProgrammingError(
		      "Unexpected direction in FourThreeOne::connectBack!",
		      __FILE__, __LINE__);
  }

  virtual void connectDoubleBack(const ProtoVSBNode *otherproto,
				 VSBNode *othernode0, VSBNode *othernode1,
				 VSBNode *&node0, VSBNode *&node1)
  {
    VoxelEdgeDirection dir = getReferenceDir(otherproto);
    if(dir == posX) {
      bool ordered = voxelOrder(vox100, vox111);
      node0 = ordered ? vsbNode0 : vsbNode1;
      node1 = ordered ? vsbNode1 : vsbNode0;
      node0->setNeighbor(1, othernode0);
      node1->setNeighbor(1, othernode1);
    }
    else if(dir == posY) {
      bool ordered = voxelOrder(vox010, vox111);
      node0 = ordered ? vsbNode0 : vsbNode1;
      node1 = ordered ? vsbNode1 : vsbNode0;
      node0->setNeighbor(2, othernode0);
      node1->setNeighbor(2, othernode1);
    }
    else {
      oofcerr << "FourThreeOne::connectDoubleBack: position="
	      << position() << " other position=" << otherproto->position()
	      << " rotation=" << rotation
	      << " dir=" << dir << std::endl;
      throw ErrProgrammingError(
	      "Unexpected direction in FourThreeOne::connectDoubleBack!",
	      __FILE__, __LINE__);
    }
  }

#ifdef DEBUG
  virtual void print(std::ostream &os) const {
    os << "FourThreeOne(" << printSig(signature) << ", " << rotation << ")";
  }
#endif // DEBUG
};	// end class FourThreeOne

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static std::vector<const ProtoVSBNode*> protoNodeTable(256, nullptr);

static void pn(unsigned char signature, const ProtoVSBNode *protoNode) {
#ifdef DEBUG
  if(protoNode != nullptr)
    protoNode->setSignature(signature);
  if(protoNodeTable[signature] != nullptr) {
    oofcerr << "Duplicate signature! " << signature << " "
	    << printSig(signature) << std::endl;
    throw ErrProgrammingError("Duplicate ProtoVSBNode signature!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  protoNodeTable[signature] = protoNode;
}

void initializeProtoNodes() {
  // Create an instance of each ProtoVSBNode class in each orientation
  // and store it in a table indexed by the voxel signature for that
  // configuration.  The table is used to create the ProtoVSBNodes
  // when a CMicrostructure is computing voxel set boundaries.

  // First, the configurations that *don't* define a vertex.
  // Including these explicitly just helps us to be sure that we
  // covered all the cases.
  
  // The trivial cases:
  pn(voxelNONE, nullptr); // no voxels
  pn(voxelALL, nullptr); // all 8 voxels

  // Two adjacent voxels sharing a face (the butterstick
  // configurations) don't define a vertex.  There are 12
  // possibilities:
  pn(vox000|vox001, nullptr);
  pn(vox010|vox011, nullptr);
  pn(vox100|vox101, nullptr);
  pn(vox110|vox111, nullptr);
  pn(vox000|vox010, nullptr);
  pn(vox001|vox011, nullptr);
  pn(vox100|vox110, nullptr);
  pn(vox101|vox111, nullptr);
  pn(vox000|vox100, nullptr);
  pn(vox001|vox101, nullptr);
  pn(vox010|vox110, nullptr);
  pn(vox011|vox111, nullptr);
  // Ditto for the 12 inverse buttersticks (two holes sharing a face).
  pn(~(vox000|vox001), nullptr);
  pn(~(vox010|vox011), nullptr);
  pn(~(vox100|vox101), nullptr);
  pn(~(vox110|vox111), nullptr);
  pn(~(vox000|vox010), nullptr);
  pn(~(vox001|vox011), nullptr);
  pn(~(vox100|vox110), nullptr);
  pn(~(vox101|vox111), nullptr);
  pn(~(vox000|vox100), nullptr);
  pn(~(vox001|vox101), nullptr);
  pn(~(vox010|vox110), nullptr);
  pn(~(vox011|vox111), nullptr);

  // Four voxels in one plane don't define a vertex.  There are 6
  // configurations:
  pn(vox000|vox001|vox010|vox011, nullptr); // x=0
  pn(vox100|vox101|vox110|vox111, nullptr); // x=1
  pn(vox000|vox100|vox001|vox101, nullptr); // y=0
  pn(vox010|vox110|vox011|vox111, nullptr); // y=1
  pn(vox000|vox010|vox100|vox110, nullptr); // z=0
  pn(vox001|vox011|vox101|vox111, nullptr); // z=1
  
  // Two parallel offset stacks of two voxels don't define a vertex.
  pn(vox000|vox001|vox110|vox111, nullptr);
  pn(vox100|vox101|vox010|vox011, nullptr);
  pn(vox000|vox100|vox011|vox111, nullptr);
  pn(vox001|vox101|vox010|vox110, nullptr);
  pn(vox001|vox011|vox100|vox110, nullptr);
  pn(vox000|vox010|vox101|vox111, nullptr);

  // Now the real cases:
  pn(vox111, new SingleVoxel(VoxRot(posX, posY, posZ)));
  pn(vox101, new SingleVoxel(VoxRot(negY, posX, posZ)));
  pn(vox001, new SingleVoxel(VoxRot(negX, negY, posZ)));
  pn(vox011, new SingleVoxel(VoxRot(posY, negX, posZ)));
  pn(vox000, new SingleVoxel(VoxRot(negY, negX, negZ)));
  pn(vox010, new SingleVoxel(VoxRot(negX, posY, negZ)));
  pn(vox110, new SingleVoxel(VoxRot(posY, posX, negZ)));
  pn(vox100, new SingleVoxel(VoxRot(posX, negY, negZ)));

  pn(~vox111, new SevenVoxels(VoxRot(posX, posY, posZ)));
  pn(~vox101, new SevenVoxels(VoxRot(negY, posX, posZ)));
  pn(~vox001, new SevenVoxels(VoxRot(negX, negY, posZ)));
  pn(~vox011, new SevenVoxels(VoxRot(posY, negX, posZ)));
  pn(~vox000, new SevenVoxels(VoxRot(negY, negX, negZ)));
  pn(~vox010, new SevenVoxels(VoxRot(negX, posY, negZ)));
  pn(~vox110, new SevenVoxels(VoxRot(posY, posX, negZ)));
  pn(~vox100, new SevenVoxels(VoxRot(posX, negY, negZ)));

  pn(vox000|vox110, new TwoVoxelsByEdge(VoxRot(posX, posY, posZ)));
  pn(vox010|vox100, new TwoVoxelsByEdge(VoxRot(posY, negX, posZ)));
  pn(vox001|vox111, new TwoVoxelsByEdge(VoxRot(negY, negX, negZ)));
  pn(vox101|vox011, new TwoVoxelsByEdge(VoxRot(posX, negY, negZ)));
  pn(vox100|vox111, new TwoVoxelsByEdge(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110, new TwoVoxelsByEdge(VoxRot(posY, negZ, negX)));
  pn(vox000|vox011, new TwoVoxelsByEdge(VoxRot(negY, negZ, posX)));
  pn(vox001|vox010, new TwoVoxelsByEdge(VoxRot(negZ, posY, posX)));
  pn(vox010|vox111, new TwoVoxelsByEdge(VoxRot(posX, posZ, negY)));
  pn(vox110|vox011, new TwoVoxelsByEdge(VoxRot(negZ, posX, negY)));
  pn(vox000|vox101, new TwoVoxelsByEdge(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100, new TwoVoxelsByEdge(VoxRot(negX, posZ, posY)));

  pn(~(vox000|vox110), new SixVoxelsByEdge(VoxRot(posX, posY, posZ)));
  pn(~(vox010|vox100), new SixVoxelsByEdge(VoxRot(posY, negX, posZ)));
  pn(~(vox001|vox111), new SixVoxelsByEdge(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox011), new SixVoxelsByEdge(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox111), new SixVoxelsByEdge(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110), new SixVoxelsByEdge(VoxRot(posY, negZ, negX)));
  pn(~(vox000|vox011), new SixVoxelsByEdge(VoxRot(negY, negZ, posX)));
  pn(~(vox001|vox010), new SixVoxelsByEdge(VoxRot(negZ, posY, posX)));
  pn(~(vox010|vox111), new SixVoxelsByEdge(VoxRot(posX, posZ, negY)));
  pn(~(vox110|vox011), new SixVoxelsByEdge(VoxRot(negZ, posX, negY)));
  pn(~(vox000|vox101), new SixVoxelsByEdge(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100), new SixVoxelsByEdge(VoxRot(negX, posZ, posY)));

  pn(vox000|vox111, new TwoVoxelsByCorner(VoxRot(posX, posY, posZ)));
  pn(vox100|vox011, new TwoVoxelsByCorner(VoxRot(posY, negX, posZ)));
  pn(vox110|vox001, new TwoVoxelsByCorner(VoxRot(negX, negY, posZ)));
  pn(vox010|vox101, new TwoVoxelsByCorner(VoxRot(negY, posX, posZ)));

  pn(~(vox000|vox111), new SixVoxelsByCorner(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox011), new SixVoxelsByCorner(VoxRot(posY, negX, posZ)));
  pn(~(vox110|vox001), new SixVoxelsByCorner(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox101), new SixVoxelsByCorner(VoxRot(negY, posX, posZ)));

  // Three voxels in the Z=0 plane
  pn(vox000|vox100|vox010, new ThreeVoxL(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110, new ThreeVoxL(VoxRot(posY, negX, posZ)));
  pn(vox100|vox110|vox010, new ThreeVoxL(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110, new ThreeVoxL(VoxRot(negY, posX, posZ)));
  // Three voxels in the Z=1 plane
  pn(vox001|vox101|vox011, new ThreeVoxL(VoxRot(posY, posX, negZ)));
  pn(vox111|vox011|vox001, new ThreeVoxL(VoxRot(posX, negY, negZ)));
  pn(vox101|vox111|vox011, new ThreeVoxL(VoxRot(negY, negX, negZ)));
  pn(vox101|vox111|vox001, new ThreeVoxL(VoxRot(negX, posY, negZ)));
  // Three voxels in the X=0 plane
  pn(vox000|vox010|vox001, new ThreeVoxL(VoxRot(posY, posZ, posX)));
  pn(vox000|vox001|vox011, new ThreeVoxL(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox010, new ThreeVoxL(VoxRot(negY, negZ, posX)));
  pn(vox000|vox010|vox011, new ThreeVoxL(VoxRot(posZ, negY, posX)));
  // Three voxels in the X=1 plane
  pn(vox100|vox101|vox110, new ThreeVoxL(VoxRot(posZ, posY, negX)));
  pn(vox111|vox101|vox100, new ThreeVoxL(VoxRot(posY, negZ, negX)));
  pn(vox101|vox111|vox110, new ThreeVoxL(VoxRot(negZ, negY, negX)));
  pn(vox111|vox110|vox100, new ThreeVoxL(VoxRot(negY, posZ, negX)));
  // Three voxels in the Y=0 plane
  pn(vox000|vox100|vox001, new ThreeVoxL(VoxRot(posZ, posX, posY)));
  pn(vox000|vox001|vox101, new ThreeVoxL(VoxRot(posX, negZ, posY)));
  pn(vox001|vox101|vox100, new ThreeVoxL(VoxRot(negZ, negX, posY)));
  pn(vox000|vox100|vox101, new ThreeVoxL(VoxRot(negX, posZ, posY)));
  // Three voxels in the Y=1 plane
  pn(vox110|vox010|vox011, new ThreeVoxL(VoxRot(posX, posZ, negY)));
  pn(vox111|vox011|vox010, new ThreeVoxL(VoxRot(negZ, posX, negY)));
  pn(vox111|vox011|vox110, new ThreeVoxL(VoxRot(negX, negZ, negY)));
  pn(vox110|vox010|vox111, new ThreeVoxL(VoxRot(posZ, negX, negY)));

  pn(~(vox100|vox101|vox110), new FiveVoxL(VoxRot(posZ, posY, negX)));
  pn(~(vox111|vox101|vox100), new FiveVoxL(VoxRot(posY, negZ, negX)));
  pn(~(vox101|vox111|vox110), new FiveVoxL(VoxRot(negZ, negY, negX)));
  pn(~(vox111|vox110|vox100), new FiveVoxL(VoxRot(negY, posZ, negX)));
  pn(~(vox000|vox010|vox001), new FiveVoxL(VoxRot(posY, posZ, posX)));
  pn(~(vox000|vox001|vox011), new FiveVoxL(VoxRot(negZ, posY, posX)));
  pn(~(vox001|vox011|vox010), new FiveVoxL(VoxRot(negY, negZ, posX)));
  pn(~(vox000|vox010|vox011), new FiveVoxL(VoxRot(posZ, negY, posX)));
  pn(~(vox110|vox010|vox011), new FiveVoxL(VoxRot(posX, posZ, negY)));
  pn(~(vox111|vox011|vox010), new FiveVoxL(VoxRot(negZ, posX, negY)));
  pn(~(vox111|vox011|vox110), new FiveVoxL(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox010|vox111), new FiveVoxL(VoxRot(posZ, negX, negY)));
  pn(~(vox000|vox100|vox001), new FiveVoxL(VoxRot(posZ, posX, posY)));
  pn(~(vox000|vox001|vox101), new FiveVoxL(VoxRot(posX, negZ, posY)));
  pn(~(vox001|vox101|vox100), new FiveVoxL(VoxRot(negZ, negX, posY)));
  pn(~(vox000|vox100|vox101), new FiveVoxL(VoxRot(negX, posZ, posY)));
  pn(~(vox001|vox101|vox011), new FiveVoxL(VoxRot(posY, posX, negZ)));
  pn(~(vox111|vox011|vox001), new FiveVoxL(VoxRot(posX, negY, negZ)));
  pn(~(vox101|vox111|vox011), new FiveVoxL(VoxRot(negY, negX, negZ)));
  pn(~(vox101|vox111|vox001), new FiveVoxL(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox100|vox010), new FiveVoxL(VoxRot(posX, posY, posZ)));
  pn(~(vox000|vox100|vox110), new FiveVoxL(VoxRot(posY, negX, posZ)));
  pn(~(vox100|vox110|vox010), new FiveVoxL(VoxRot(negX, negY, posZ)));
  pn(~(vox000|vox010|vox110), new FiveVoxL(VoxRot(negY, posX, posZ)));

  // Double stack in the z direction, single voxel in the z=0 plane
  pn(vox000|vox110|vox111, new ThreeTwoOne(VoxRot(posX, posY, posZ)));
  pn(vox100|vox010|vox011, new ThreeTwoOne(VoxRot(posY, negX, posZ)));
  pn(vox000|vox110|vox001, new ThreeTwoOne(VoxRot(negX, negY, posZ)));
  pn(vox100|vox010|vox101, new ThreeTwoOne(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single voxel in the z=1 plane
  pn(vox001|vox110|vox111, new ThreeTwoOne(VoxRot(posY, posX, negZ)));
  pn(vox010|vox011|vox101, new ThreeTwoOne(VoxRot(negX, posY, negZ)));
  pn(vox000|vox001|vox111, new ThreeTwoOne(VoxRot(negY, negX, negZ)));
  pn(vox100|vox101|vox011, new ThreeTwoOne(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single voxel in the x=1 plane
  pn(vox000|vox100|vox111, new ThreeTwoOne(VoxRot(negZ, negY, negX)));
  pn(vox001|vox110|vox101, new ThreeTwoOne(VoxRot(negY, posZ, negX)));
  pn(vox100|vox011|vox111, new ThreeTwoOne(VoxRot(posZ, posY, negX)));
  pn(vox101|vox110|vox010, new ThreeTwoOne(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single voxel in the x=0 plane
  pn(vox000|vox100|vox011, new ThreeTwoOne(VoxRot(negY, negZ, posX)));
  pn(vox010|vox001|vox101, new ThreeTwoOne(VoxRot(posZ, negY, posX)));
  pn(vox000|vox011|vox111, new ThreeTwoOne(VoxRot(posY, posZ, posX)));
  pn(vox001|vox010|vox110, new ThreeTwoOne(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single voxel in the x=0 plane
  pn(vox000|vox010|vox101, new ThreeTwoOne(VoxRot(negZ, negX, posY)));
  pn(vox001|vox100|vox110, new ThreeTwoOne(VoxRot(posX, negZ, posY)));
  pn(vox000|vox101|vox111, new ThreeTwoOne(VoxRot(posZ, posX, posY)));
  pn(vox100|vox001|vox011, new ThreeTwoOne(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single voxel in the x=1 plane
  pn(vox000|vox010|vox111, new ThreeTwoOne(VoxRot(negX, negZ, negY)));
  pn(vox110|vox001|vox011, new ThreeTwoOne(VoxRot(posZ, negX, negY)));
  pn(vox010|vox101|vox111, new ThreeTwoOne(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox011, new ThreeTwoOne(VoxRot(negZ, posX, negY)));

  // Double stack in the z direction, single hole in the z=0 plane
  pn(~(vox000|vox110|vox111), new FiveTwoOne(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox010|vox011), new FiveTwoOne(VoxRot(posY, negX, posZ)));
  pn(~(vox000|vox110|vox001), new FiveTwoOne(VoxRot(negX, negY, posZ)));
  pn(~(vox100|vox010|vox101), new FiveTwoOne(VoxRot(negY, posX, posZ)));
  // Double stack in the z direction, single hole in the z=1 plane
  pn(~(vox001|vox110|vox111), new FiveTwoOne(VoxRot(posY, posX, negZ)));
  pn(~(vox010|vox011|vox101), new FiveTwoOne(VoxRot(negX, posY, negZ)));
  pn(~(vox000|vox001|vox111), new FiveTwoOne(VoxRot(negY, negX, negZ)));
  pn(~(vox100|vox101|vox011), new FiveTwoOne(VoxRot(posX, negY, negZ)));
  // Double stack in the x direction, single hole in the x=1 plane
  pn(~(vox000|vox100|vox111), new FiveTwoOne(VoxRot(negZ, negY, negX)));
  pn(~(vox001|vox110|vox101), new FiveTwoOne(VoxRot(negY, posZ, negX)));
  pn(~(vox100|vox011|vox111), new FiveTwoOne(VoxRot(posZ, posY, negX)));
  pn(~(vox101|vox110|vox010), new FiveTwoOne(VoxRot(posY, negZ, negX)));
  // Double stack in the x direction, single hole in the x=0 plane
  pn(~(vox000|vox100|vox011), new FiveTwoOne(VoxRot(negY, negZ, posX)));
  pn(~(vox010|vox001|vox101), new FiveTwoOne(VoxRot(posZ, negY, posX)));
  pn(~(vox000|vox011|vox111), new FiveTwoOne(VoxRot(posY, posZ, posX)));
  pn(~(vox001|vox010|vox110), new FiveTwoOne(VoxRot(negZ, posY, posX)));
  // Double stack in the y direction, single hole in the x=0 plane
  pn(~(vox000|vox010|vox101), new FiveTwoOne(VoxRot(negZ, negX, posY)));
  pn(~(vox001|vox100|vox110), new FiveTwoOne(VoxRot(posX, negZ, posY)));
  pn(~(vox000|vox101|vox111), new FiveTwoOne(VoxRot(posZ, posX, posY)));
  pn(~(vox100|vox001|vox011), new FiveTwoOne(VoxRot(negX, posZ, posY)));
  // Double stack in the y direction, single hole in the x=1 plane
  pn(~(vox000|vox010|vox111), new FiveTwoOne(VoxRot(negX, negZ, negY)));
  pn(~(vox110|vox001|vox011), new FiveTwoOne(VoxRot(posZ, negX, negY)));
  pn(~(vox010|vox101|vox111), new FiveTwoOne(VoxRot(posX, posZ, negY)));
  pn(~(vox100|vox110|vox011), new FiveTwoOne(VoxRot(negZ, posX, negY)));

  pn(vox110|vox011|vox101, new ThreeVoxByEdges(VoxRot(posX, posY, posZ)));
  pn(vox100|vox001|vox111, new ThreeVoxByEdges(VoxRot(negY, posX, posZ)));
  pn(vox000|vox101|vox011, new ThreeVoxByEdges(VoxRot(negX, negY, posZ)));
  pn(vox010|vox001|vox111, new ThreeVoxByEdges(VoxRot(posY, negX, posZ)));

  pn(vox111|vox100|vox010, new ThreeVoxByEdges(VoxRot(posY, posX, negZ)));
  pn(vox000|vox110|vox101, new ThreeVoxByEdges(VoxRot(posX, negY, negZ)));
  pn(vox100|vox010|vox001, new ThreeVoxByEdges(VoxRot(negY, negX, negZ)));
  pn(vox000|vox011|vox110, new ThreeVoxByEdges(VoxRot(negX, posY, negZ)));

  pn(~(vox110|vox011|vox101), new FiveVoxByEdges(VoxRot(posX, posY, posZ)));
  pn(~(vox100|vox001|vox111), new FiveVoxByEdges(VoxRot(negY, posX, posZ)));
  pn(~(vox000|vox101|vox011), new FiveVoxByEdges(VoxRot(negX, negY, posZ)));
  pn(~(vox010|vox001|vox111), new FiveVoxByEdges(VoxRot(posY, negX, posZ)));

  pn(~(vox111|vox100|vox010), new FiveVoxByEdges(VoxRot(posY, posX, negZ)));
  pn(~(vox000|vox110|vox101), new FiveVoxByEdges(VoxRot(posX, negY, negZ)));
  pn(~(vox100|vox010|vox001), new FiveVoxByEdges(VoxRot(negY, negX, negZ)));
  pn(~(vox000|vox011|vox110), new FiveVoxByEdges(VoxRot(negX, posY, negZ)));

  pn(vox000|vox100|vox010|vox011, new ChiralR(VoxRot(posX, posY, posZ)));
  pn(vox000|vox010|vox110|vox111, new ChiralR(VoxRot(negY, posX, posZ)));
  pn(vox100|vox010|vox110|vox101, new ChiralR(VoxRot(negX, negY, posZ)));
  pn(vox000|vox001|vox100|vox110, new ChiralR(VoxRot(posY, negX, posZ)));

  pn(vox000|vox001|vox011|vox111, new ChiralR(VoxRot(negZ, posY, posX)));
  pn(vox101|vox111|vox011|vox010, new ChiralR(VoxRot(negZ, posX, negY)));
  pn(vox001|vox101|vox111|vox110, new ChiralR(VoxRot(negZ, negY, negX)));
  pn(vox001|vox011|vox100|vox101, new ChiralR(VoxRot(negZ, negX, posY)));

  pn(vox000|vox010|vox001|vox101, new ChiralR(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox110, new ChiralR(VoxRot(negY, negZ, posX)));
  pn(vox100|vox110|vox111|vox011, new ChiralR(VoxRot(negX, negZ, negY)));
  pn(vox000|vox100|vox101|vox111, new ChiralR(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox110, new ChiralL(VoxRot(posX, posY, posZ)));
  pn(vox100|vox110|vox010|vox011, new ChiralL(VoxRot(negY, posX, posZ)));
  pn(vox000|vox100|vox110|vox111, new ChiralL(VoxRot(negX, negY, posZ)));
  pn(vox000|vox100|vox101|vox010, new ChiralL(VoxRot(posY, negX, posZ)));

  pn(vox101|vox001|vox011|vox010, new ChiralL(VoxRot(negZ, posY, posX)));
  pn(vox001|vox011|vox111|vox110, new ChiralL(VoxRot(negZ, posX, negY)));
  pn(vox100|vox101|vox111|vox011, new ChiralL(VoxRot(negZ, negY, negX)));
  pn(vox000|vox001|vox101|vox111, new ChiralL(VoxRot(negZ, negX, posY)));

  pn(vox000|vox100|vox001|vox011, new ChiralL(VoxRot(posX, negZ, posY)));
  pn(vox000|vox010|vox011|vox111, new ChiralL(VoxRot(negY, negZ, posX)));
  pn(vox101|vox111|vox110|vox010, new ChiralL(VoxRot(negX, negZ, negY)));
  pn(vox001|vox101|vox100|vox110, new ChiralL(VoxRot(posY, negZ, negX)));

  pn(vox000|vox001|vox010|vox100, new Pyramid(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox101|vox110, new Pyramid(VoxRot(posY, negX, posZ)));
  pn(vox111|vox110|vox010|vox100, new Pyramid(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox011, new Pyramid(VoxRot(negY, posX, posZ)));

  pn(vox111|vox110|vox101|vox011, new Pyramid(VoxRot(negY, negX, negZ)));
  pn(vox001|vox011|vox111|vox010, new Pyramid(VoxRot(posX, negY, negZ)));
  pn(vox000|vox001|vox011|vox101, new Pyramid(VoxRot(posY, posX, negZ)));
  pn(vox001|vox101|vox111|vox100, new Pyramid(VoxRot(negX, posY, negZ)));

  pn(vox100|vox010|vox001|vox111, new CheckerBoard(VoxRot(posX, posY, posZ)));
  pn(vox000|vox110|vox101|vox011, new CheckerBoard(VoxRot(posY, negX, posZ)));

  pn(vox000|vox010|vox100|vox111, new FourThreeOne(VoxRot(posX, posY, posZ)));
  pn(vox000|vox100|vox110|vox011, new FourThreeOne(VoxRot(posY, negX, posZ)));
  pn(vox100|vox010|vox110|vox001, new FourThreeOne(VoxRot(negX, negY, posZ)));
  pn(vox000|vox010|vox110|vox101, new FourThreeOne(VoxRot(negY, posX, posZ)));

  pn(vox000|vox001|vox011|vox110, new FourThreeOne(VoxRot(negZ, posY, posX)));
  pn(vox100|vox010|vox011|vox111, new FourThreeOne(VoxRot(negZ, posX, negY)));
  pn(vox000|vox110|vox111|vox101, new FourThreeOne(VoxRot(negZ, negY, negX)));
  pn(vox100|vox101|vox001|vox010, new FourThreeOne(VoxRot(negZ, negX, posY)));

  pn(vox010|vox011|vox101|vox110, new FourThreeOne(VoxRot(posX, posZ, negY)));
  pn(vox100|vox110|vox111|vox001, new FourThreeOne(VoxRot(negY, posZ, negX)));
  pn(vox000|vox100|vox101|vox011, new FourThreeOne(VoxRot(negX, posZ, posY)));
  pn(vox000|vox010|vox001|vox111, new FourThreeOne(VoxRot(posY, posZ, posX)));

  pn(vox000|vox001|vox101|vox110, new FourThreeOne(VoxRot(posX, negZ, posY)));
  pn(vox001|vox011|vox010|vox100, new FourThreeOne(VoxRot(negY, negZ, posX)));
  pn(vox000|vox011|vox111|vox110, new FourThreeOne(VoxRot(negX, negZ, negY)));
  pn(vox010|vox100|vox101|vox111, new FourThreeOne(VoxRot(posY, negZ, negX)));

  pn(vox100|vox110|vox101|vox011, new FourThreeOne(VoxRot(posZ, posY, negX)));
  pn(vox000|vox001|vox100|vox111, new FourThreeOne(VoxRot(posZ, posX, posY)));
  pn(vox000|vox010|vox011|vox101, new FourThreeOne(VoxRot(posZ, negY, posX)));
  pn(vox001|vox111|vox110|vox010, new FourThreeOne(VoxRot(posZ, negX, negY)));

  pn(vox001|vox011|vox111|vox100, new FourThreeOne(VoxRot(posX, negY, negZ)));
  pn(vox000|vox101|vox011|vox111, new FourThreeOne(VoxRot(negY, negX, negZ)));
  pn(vox010|vox001|vox101|vox111, new FourThreeOne(VoxRot(negX, posY, negZ)));
  pn(vox110|vox001|vox101|vox011, new FourThreeOne(VoxRot(posY, posX, negZ)));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VSBNode::VSBNode(const Coord3D &p)
    : neighbors(3, nullptr), position(p)
{}

VSBNode::VSBNode(const ICoord3D &p)
  : neighbors(3, nullptr), position(p.coord())
{}

VSBNode::~VSBNode() {}

void VSBNode::setNeighbor(unsigned int i, VSBNode *nbr) {
  assert(neighbors[i] == nullptr);
  neighbors[i] = nbr;
}

void VSBNode::replaceNeighbor(VSBNode *oldnode, VSBNode *newnode) {
  for(unsigned int i=0; i<3; i++) {
    if(neighbors[i] == oldnode) {
      neighbors[i] = newnode;
      return;
    }
  }
  throw ErrProgrammingError("VSBNode::replaceNeighbor failed!",
			    __FILE__, __LINE__);
}

unsigned int VSBNode::neighborIndex(const VSBNode *nbr) const {
  for(unsigned int i=0; i<3; i++)
    if(neighbors[i] == nbr)
      return i;
  throw ErrProgrammingError("VSBNode::neighborIndex failed!",
			    __FILE__, __LINE__);
}

// nextCWNeighbor returns the neighbor of this node that follows the
// given node CW in the neighbor list.  This is where the CW storage
// ordering of the neighbors is important.  If the initial graph is
// insufficiently connected, it's possible that a clipped graph has
// nodes with duplicate neighbors.  In that case, nextCWNeighbor
// should always return the neighbor that's *not* the argument.

// TODO: Can the result of nextCWNeighbor be computed at graph
// construction time and cached?

const VSBNode *VSBNode::nextCWNeighbor(const VSBNode *nbr) const {
  if(neighbors[0] == nbr) {
    // if(neighbors[1] == nbr)
    //   return neighbors[2];
    return neighbors[1];
  }
  if(neighbors[1] == nbr) {
    // if(neighbors[2] == nbr)
    //   return neighbors[0];
    return neighbors[2];
  }
  assert(neighbors[2] == nbr);
  // if(neighbors[0] == nbr)
  //   return neighbors[1];
  return neighbors[0];
}

VSBNode *VSBNode::nextCWNeighbor(const VSBNode *nbr) {
  if(neighbors[0] == nbr) {
    // if(neighbors[1] == nbr)
    //   return neighbors[2];
    return neighbors[1];
  }
  if(neighbors[1] == nbr) {
    // if(neighbors[2] == nbr)
    //   return neighbors[0];
    return neighbors[2];
  }
  assert(neighbors[2] == nbr);
  // if(neighbors[0] == nbr)
  //   return neighbors[1];
  return neighbors[0];
}

bool VSBNode::degenerateNeighbor(const VSBNode *other) const {
  return (other->neighbors[1] == this && other->neighbors[2] == this &&
	  neighbors[1] == other && neighbors[2] == other);
}

std::ostream &operator<<(std::ostream &os, const VSBNode &node) {
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

VSBGraph::VSBGraph(const ICRectangularPrism &domain)
  : bounds(Coord3D(0,0,0), Coord3D(0,0,0)),
    domain(domain)
{}

VSBGraph::~VSBGraph() {
  for(VSBNode *node : vertices)
    delete node;
  vertices.clear();
}

void VSBGraph::addNode(VSBNode *node) {
  if(vertices.empty())
    bounds = CRectangularPrism(node->position, node->position);
  else
    bounds.swallow(node->position);
  node->index = vertices.size();
  vertices.push_back(node);
}

void VSBGraph::addNodes(const std::vector<VSBNode*> &newNodes) {
  assert(!newNodes.empty());
  unsigned int n = vertices.size();
  if(n == 0) {
    bounds = CRectangularPrism(newNodes[0]->position, newNodes[0]->position);
  }
  for(VSBNode *node : newNodes) {
    node->index = n++;
    bounds.swallow(node->position);
  }
  vertices.insert(vertices.end(), newNodes.begin(), newNodes.end());
}

VSBGraph::VSBGraph(const VSBGraph &other)
  : bounds(other.bounds)
{
  vertices.reserve(other.size());
  for(const VSBNode *overtex : other.vertices) {
    addNode(new VSBNode(overtex->position));
  }
  for(VSBNode *vertex : vertices) {
    const VSBNode *oldNode = other.getNode(vertex->getIndex());
    for(unsigned int i=0; i<3; i++) {
      vertex->setNeighbor(i, vertices[oldNode->getNeighbor(i)->getIndex()]);
    }
  }
}

Coord3D VSBGraph::center() const {
  Coord ctr;
  for(VSBNode *vertex : vertices)
    ctr += vertex->position;
  return ctr/vertices.size();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

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
// plane?  Is it faster than COrientedPlane::distance?  (Powell & Abel
// suggest splitting volume across longest direction, instead of
// dividing in 8.  They also say it's not worth the effort unless
// there are a lot of voxels.)


std::vector<double> VSBGraph::getDistances(const COrientedPlane &plane,
					   double &dmin, double &dmax)
  const
{
  std::vector<double> dists;
  dists.reserve(size());
  dmin = std::numeric_limits<double>::max();
  dmax = -std::numeric_limits<double>::max();
  for(const VSBNode *vertex : vertices) {
    double d = plane.distance(vertex->position);
    dists.push_back(d);
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "getDistances: vertex=" << vertex->index << " "
// 	      << vertex->position << " " << "d=" << d << std::endl;
// #endif // DEBUG
    if(d > dmax)
      dmax = d;
    if(d < dmin)
      dmin = d;
  }
  return dists;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VSBGraph *VSBGraph::copyAndClip(const COrientedPlane &plane) const {
  // Based loosely on r3d_clip in r3d.c.
  double dmin, dmax;
  std::vector<double> distance = getDistances(plane, dmin, dmax);
  if(dmax < 0) {
    // entire graph is within the clipping region
    return new VSBGraph(*this);
  }
  if(dmin > 0) {
    // entire graph is outside the clipping region
    return new VSBGraph(domain); // empty graph
  }

  // Copy the nodes that are to be kept, and create new nodes at the
  // clipping plane.
  VSBGraph *newGraph = new VSBGraph(domain);
  // copies[i] is the node in the new graph that is a copy of the node
  // with index i in the old graph.
  std::vector<VSBNode*> copies(vertices.size(), nullptr);
  unsigned int nCopied = 0;
  std::vector<VSBNode*> danglingNodes;
  // v0 loops through the nodes in the old graph, finding ones that
  // need to be copied.
  for(unsigned int v0=0; v0<vertices.size(); v0++) {
    if(copies[v0]==nullptr && distance[v0] < 0) {
      // Old node v0 needs to be copied to the new graph.  Copy it and
      // its neighbors.  stack stores all the nodes that need to be
      // copied.
      std::vector<const VSBNode*> stack;
      stack.reserve(vertices.size() - nCopied);
      stack.push_back(vertices[v0]);
      while(!stack.empty()) {
	const VSBNode *oldNode = stack.back();
	stack.pop_back();

	// Nodes might be put on the stack multiple times.  Just
	// ignore the repeats.
	if(copies[oldNode->getIndex()] != nullptr)
	  continue;

	double d0 = distance[oldNode->getIndex()]; // negative!
	VSBNode *newNode = new VSBNode(oldNode->position);
	copies[oldNode->getIndex()] = newNode;
	++nCopied;
	newGraph->addNode(newNode);
	for(unsigned int n=0; n<3; n++) { // loop over nbrs of old node
	  // If the neighbor has already been copied, set the neighbor
	  // pointers in the new node and the copy of its neighbor.
	  const VSBNode *oldNbr = oldNode->getNeighbor(n);
	  VSBNode *nbrCopy = copies[oldNbr->getIndex()];
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
	      Coord3D p = ((oldNode->position*nbrDistance - oldNbr->position*d0)
			   / (nbrDistance - d0));
	      VSBNode *newNbr = new VSBNode(p);
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
  std::vector<VSBNode*> keptNodes =
    newGraph->removeDegenerateFaces(danglingNodes);
  if(!keptNodes.empty())
    newGraph->addNodes(keptNodes);
 
  return newGraph;
} // end VSBGraph::copyAndClip

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void VSBGraph::clipInPlace(const COrientedPlane &plane) {
  // Modeled after r3d_clip, more or less. This is more like it than
  // copyAndClip is.
  // oofcerr << "VSBGraph::clipInPlace" << std::endl;
  double dmin, dmax;
  std::vector<double> distance = getDistances(plane, dmin, dmax);
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "VSBGraph::clipInPlace: dmin=" << dmin << " dmax=" << dmax
// 	    << std::endl;
// #endif // DEBUG
  if(dmax < 0) {
    // Entire graph is within the clipping region.  There's nothing to do.
    return;
  }
  if(dmin > 0) {
    // The entire graph is outside the clipping region.  Delete all
    // nodes.
    for(VSBNode *node : vertices)
      delete node;
    vertices.clear();
    return;
  }

  std::vector<VSBNode*> newNodes;
  for(unsigned int v0=0; v0<vertices.size(); v0++) {
    if(distance[v0] < 0) {	// keep this vertex
      VSBNode *thisvert = vertices[v0];
      double d0 = distance[v0];		// negative!
      for(unsigned int n=0; n<3; n++) { // loop over neighbors
	const VSBNode *nbr = thisvert->getNeighbor(n);
	double d1 = distance[nbr->getIndex()];
	if(d1 >= 0) {
	  // The neighbor needs to be clipped.
	  Coord3D p = (thisvert->position*d1 - nbr->position*d0)/(d1 - d0);
// #ifdef DEBUG
// 	  if(verbose) {
// 	    oofcerr << "VSBGraph::clipInPlace: clipping! thisvert=" << *thisvert
// 		    << " nbr=" << *nbr << std::endl;
// 	  }
// #endif // DEBUG
	  VSBNode *newNode = new VSBNode(p);
	  newNodes.push_back(newNode);
	  thisvert->replaceNeighbor(n, newNode);
	  newNode->setNeighbor(0, thisvert);
// #ifdef DEBUG
// 	  if(verbose) {
// 	    oofcerr << "VSBGraph::clipInPlace: newNode=" << *newNode
// 		    << std::endl;
// 	    oofcerr << "VSBGraph::clipInPlace: after clipping, thisvert="
// 		    << *thisvert << std::endl;
// 	  }
// #endif // DEBUG
	}
      }	// end loop over neighbors n of v0
    } // end if v0 is being kept
  } // end loop over vertices v0

  // oofcerr << "VSBGraph::clipInPlace: clipped" << std::endl;
  // Connect the new nodes to one another.
  connectClippedNodes(newNodes);
  // oofcerr << "VSBGraph::clipInPlace: connected" << std::endl;
  std::vector<VSBNode*> realNewNodes = removeDegenerateFaces(newNodes);
  // oofcerr << "VSBGraph::clipInPlace: removed degenerate" << std::endl;

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
  // oofcerr << "VSBGraph::clipInPlace: removed" << std::endl;
  // Fix VSBNode::index for the retained nodes.
  for(unsigned int i=0; i<vertices.size(); i++) {
    vertices[i]->index = i;
  }
  // Add the new nodes to the graph.
  if(!realNewNodes.empty())
    addNodes(realNewNodes);
}

void VSBGraph::connectClippedNodes(const std::vector<VSBNode*> &newNodes)
  const
{
  // Each node in newNodes has exactly one neighbor, in slot 0.
  // Starting from that neighbor, go from node to node
  // counterclockwise around the hole in the graph to find the next
  // new node, and connect to it.  We know when we've found the next
  // new node because it won't have a neighbor in slot 1.
  for(VSBNode *newNode : newNodes) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "VSBGraph::connectClippedNodes: newNode=" << *newNode
// 	      << std::endl;
//     OOFcerrIndent indent(2);
// #endif // DEBUG
    VSBNode *vcur = newNode;
    VSBNode *vnext = newNode->getNeighbor(0);
    do {
      // To make a counterclockwise turn from one graph edge to
      // another, pick the outgoing edge that's the *clockwise*
      // neighbor of the incoming edge.
      VSBNode *vtemp = vnext->nextCWNeighbor(vcur);
      vcur = vnext;
      vnext = vtemp;
// #ifdef DEBUG
//       if(verbose)
// 	oofcerr << "VSBGraph::connectClippedNodes: vcur=" << *vcur << std::endl;
// #endif // DEBUG
    } while(vcur->getNeighbor(1) != nullptr);
    vcur->setNeighbor(1, newNode);
    newNode->setNeighbor(2, vcur);
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "VSBGraph::connectClippedNodes: connected "
// 	      << *vcur << " " << *newNode << std::endl;
// #endif // DEBUG
  }
}

std::vector<VSBNode*> VSBGraph::removeDegenerateFaces(
					      std::vector<VSBNode*> &newNodes)
  const
{
  // oofcerr << "VSBGraph::removeDegenerateFaces: nNew=" << newNodes.size()
  // 	  << std::endl;
  if(newNodes.empty())
    return newNodes;
  // If the graph isn't 3-vertex connected, clipping can produce a
  // degenerate new face, in which two nodes have two connections to
  // each other, both of which have to be neighbor slots 1 and 2.
  // There can be no change of direction at such nodes, so we can
  // remove the two nodes and connect their other neighbors directly
  // to each other.
  std::vector<bool> removed(newNodes.size(), false); // has a node been removed?
  unsigned int nremoved = 0;
  // Loop over pairs of new nodes that haven't yet been removed from newNodes
  for(unsigned int i=0; i<newNodes.size()-1; i++) {
    if(!removed[i]) {
      for(unsigned int j=i+1; j<newNodes.size(); j++) {
	if(!removed[j]) {
	  if(newNodes[i]->degenerateNeighbor(newNodes[j])) {
	    // The two nodes are multiply connected.  Remove them.
	    VSBNode *oldnbr0 = newNodes[i]->getNeighbor(0);
	    VSBNode *oldnbr1 = newNodes[j]->getNeighbor(0);
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
  // oofcerr << "VSBGraph::removeDegenerateFaces: nremoved=" << nremoved
  // 	  << std::endl;
  if(nremoved == 0)
    return newNodes;
  std::vector<VSBNode*> retained;
  retained.reserve(newNodes.size() - nremoved);
  for(unsigned int k=0; k<newNodes.size(); k++) {
    if(!removed[k])
      retained.push_back(newNodes[k]);
    else
      delete newNodes[k];
  }
  return retained;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double VSBGraph::volume() const {
  // Based on r3d_reduce.  Compute the volume of the polyhedron by
  // splitting each face into triangles, and computing the volume of
  // the each tet formed by a triangle and the center of the
  // polyhedron.
 
  if(empty())
    return 0.0;
  Coord3D cntr = center();
  double vol = 0.0;
  // emarks[node][nbr] indicates which edges have been used.
  std::vector<std::vector<bool>> emarks(vertices.size(), {false, false, false});
  // Find an unused edge.
  for(unsigned int vstart=0; vstart<vertices.size(); vstart++) {
    for(unsigned int pstart=0; pstart<3; pstart++) {
      if(!emarks[vstart][pstart]) {
	// Found an unused edge.  Follow the sequence of neighbors
	// around a facet, using the starting point and a segment of
	// the perimeter to define a triangular portion of the facet.
	const VSBNode *startNode = vertices[vstart];
	Coord3D startPt = startNode->position;
	// cur and prev are the endpoints of a segment of the
	// perimeter.  Their initial values *don't* contribute to the
	// area, because prev==startPt.
	const VSBNode *prev = startNode;
	const VSBNode *cur = startNode->getNeighbor(pstart);
	emarks[vstart][pstart] = true;
	bool done = false;
	do {
	  // Go to next pair
	  const VSBNode *next = cur->nextCWNeighbor(prev);
	  prev = cur;
	  cur = next;
	  // If the graph includes doubly connected edges (which can
	  // happen when a non-3-vertex connected graph is clipped)
	  // then it's unclear which of the two edges we are
	  // traversing, and emarks may already be set.

	  
	  
// #ifdef DEBUG
// 	  if(emarks[prev->index][prev->neighborIndex(cur)]) {
// 	    oofcerr << "VSBGraph::volume: attempt to reuse an edge!"
// 		    << std::endl;
// 	    oofcerr << "VSBGraph::volume: startNode=" << *startNode
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
} // end VSBGraph::volume

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool VSBGraph::checkEdges() const {
  bool result = true;
  for(const VSBNode *vertex : vertices) {
    for(unsigned int n=0; n<3; n++) {
      const VSBNode *nbr = vertex->getNeighbor(n);
      if(nbr == nullptr) {
	oofcerr << "VSBGraph::checkEdges: missing neighbor " << n
		<< " for vertex " << vertex->index << " " << vertex->position
		<< std::endl;
	result = false;
      }
    }
    for(unsigned int n=0; n<3; n++) {
      const VSBNode *nbr = vertex->getNeighbor(n);
      if(nbr == vertex->getNeighbor((n+1)%3)) {
	result = false;
	oofcerr << "VSBGraph::checkEdges: node "
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
	oofcerr << "VSBGraph::checkEdges: node "
		<< nbr->index << " " << nbr->position
		<< " is a neighbor of node " << vertex->index
		<< " " << vertex->position << " but not vice versa."
		<< std::endl;
      }
    }
  }
  // oofcerr << "VSBGraph::checkEdges: ok!" << std::endl;
  return result;
} // end VSBGraph::checkEdges

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// checkConnectivity divides the graph into disjoint regions and
// checks that each region is three-vertex connected.  A "region" is a
// set of nodes that are connected to each other (maybe indirectly)
// and not connected to any nodes outside the region.  A three-fold
// connected region is one that can't be divided into two regions by
// removing two nodes.  This test is at least o(N^2) and is based on
// the C routine r3d_is_good() in r3d.c

// Return false if three-node connectivity is not present.  If
// nRegions is positive and not equal to the number of regions, also
// return false.

// ** checkConnectivity only applies to convex polygons. **

bool VSBGraph::checkConnectivity() const
{
  // First find the regions.  region[i] is nullptr if the node hasn't
  // yet been assigned to a region.
  bool ok = true;
  typedef std::set<const VSBNode*> Region;
  std::set<Region*> regions;
  std::vector<Region*> region(vertices.size(), nullptr);
  for(const VSBNode *start : vertices) {
    if(region[start->index] == nullptr) {
      // This vertex isn't in a region.  Start a new region.
      Region *reg = new Region();
      regions.insert(reg);
      std::vector<const VSBNode*> stack;
      stack.reserve(vertices.size());
      stack.push_back(start);
      while(!stack.empty()) {
	const VSBNode *v = stack.back();
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
	oofcerr << "VSBGraph::checkConnectivity: region is too small! size="
		<< reg->size() << std::endl;
	return false;
      }
    } // end if vertex "start" isn't in a region.
  }   // end loop over vertices "start"
  // Loop over pairs of vertices in the same region, and check that
  // removing them doesn't divide the region into two.
  for(Region *reg : regions) {
    bool okreg = true;		// region is ok
    for(Region::iterator ia=reg->begin(); ia!=reg->end() && okreg; ++ia) {
      const VSBNode *nodeA = *ia;
      Region::iterator ib=ia;
      ib++;
      for(; ib!=reg->end() && okreg; ++ib) {
	const VSBNode *nodeB = *ib;
	// Find a point nodeC that's not nodeA or nodeB, and check
	// that all nodes in the region can be reached from it. We
	// know that the region size is greater than 2, so nodeC must
	// exist.
	Region::iterator ic = reg->begin(); // pointer to nodeC
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
	std::vector<const VSBNode*> stack;
	stack.reserve(vertices.size());
	stack.push_back(*ic);
	while(!stack.empty()) {
	  const VSBNode *v = stack.back();
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
	  oofcerr << "VSBGraph::checkConnectivity:"
		  << " region is insufficiently connected!" << std::endl;
	  oofcerr << "VSBGraph::checkConnectivity: nodeA=" << *nodeA
		  << " nodeB=" << *nodeB << std::endl;
	  // for(const VSBNode *node : *reg) {
	  //   oofcerr << "VSBGraph::checkConnectivity: index=" << node->index
	  // 	    << " position=" << node->position
	  // 	    << " nbrs=[" << node->getNeighbor(0)->index << ", "
	  // 	    << node->getNeighbor(1)->index << ", "
	  // 	    << node->getNeighbor(2)->index << "]";
	  //   if(node == nodeA)
	  //     oofcerr << " A";
	  //   else if(node == nodeB)
	  //     oofcerr << " B";
	  //   oofcerr << std::endl;
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Write out the graph structure
void VSBGraph::dump(std::ostream &os) const {
  // for(const VSBNode *vertex: vertices)
  //   os << "Vertex " << vertex << " " << vertex->index << std::endl;
  for(const VSBNode *vertex : vertices) {
    os << "Vertex " << vertex->index << " " << vertex->position;
    os << "   nbrs=";
    for(VSBNode *nbr : vertex->neighbors) {
      if(nbr)
      	os << nbr->index << " ";
      else
      	os << "(0x0)  ";
    }
    os << std::endl;
  }
}

// Write out the edges in a plottable form
void VSBGraph::dumpLines(std::ostream &os, const CMicrostructure *ms) const {
  for(const VSBNode *vertex : vertices) {
    for(VSBNode *nbr : vertex->neighbors) {
      if(nbr && vertex->index < nbr->index)
	os << ms->pixel2Physical(vertex->position) << ", "
	   << ms->pixel2Physical(nbr->position) << " # "
	   << vertex->index << " " << nbr->index << std::endl;
    }
  }
}

void VSBGraph::draw(LineSegmentLayer *layer, const CMicrostructure *ms) const {
  unsigned int nsegs = (3*size())/2;
  layer->set_nSegs(nsegs);
  for(const VSBNode *node : vertices) {
    for(VSBNode *nbr : node->neighbors) {
      if(nbr && node->index < nbr->index) {
	Coord3D pt0 = ms->pixel2Physical(node->position);
	Coord3D pt1 = ms->pixel2Physical(nbr->position);
	layer->addSegment(&pt0, &pt1);
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VSBEdgeIterator::VSBEdgeIterator(const VoxelSetBoundary *vsb)
  : vsb(vsb),
    igraph(0),
    ihere(0),
    inbr(0),
    finished(false)
{
  if(vsb->graphs.empty())
    finished = true;
}

const VSBNode *VSBEdgeIterator::node0() const {
  return vsb->graphs[igraph].getNode(ihere);
}

const VSBNode *VSBEdgeIterator::node1() const {
  return vsb->graphs[igraph].getNode(ihere)->getNeighbor(inbr);
}

void VSBEdgeIterator::next() {
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// pixsize is the maximum size, in pixels of a block of pixels to
// include in a single VSBGraph.  If the microstructure is bigger than
// pixsize in any dimension, it will be broken up into more than one
// VSBGraph.  This allows many elements to skip the clipping step if
// they're outside of a graph's bounding box.  Making pixsize too
// large will make the clipping step slow (it will spend a lot of time
// clipping voxels that are no where near the element).  Making it too
// small will make it run too often.

// slopsize is the amount by which a block of pixels is allowed to
// exceed pixsize if doing so would fill the Microstructure without
// adding a new block.

VoxelSetBoundary::VoxelSetBoundary(
			   const CMicrostructure *ms,
			   const std::vector<ICRectangularPrism> &subregions,
			   unsigned int cat)
  : category(cat),
    microstructure(ms),
    bbox_(nullptr)
{
  graphs.reserve(subregions.size());
  for(unsigned int s=0; s<subregions.size(); s++)
    graphs.emplace_back(subregions[s]);
}

// protoVSBNodeFactory converts a signature (2x2x2 set of bools stored
// as a char) to a type of ProtoVSBNode and a VoxRot.  To do
// that, it clones the ProtoVSBNode that's in the protoNodeTable for
// that signature.

ProtoVSBNode *VoxelSetBoundary::protoVSBNodeFactory(unsigned int subregionNo,
						    unsigned char signature,
						    const ICoord3D &here)
{
  
  const ProtoVSBNode *prototype = protoNodeTable[signature];
  if(prototype == nullptr)
    return nullptr;
  ProtoVSBNode *protoNode = prototype->clone();
#ifdef DEBUG
  protoNode->setSignature(signature);
#endif // DEBUG
  protoNode->makeVSBNodes(&graphs[subregionNo], here);
  return protoNode;
}

void VSBGraph::twoFoldNode(VSBNode *node) {
  twoFoldNodes.insert(node);
}

void VSBGraph::fixTwoFoldNodes() {
  for(VSBNode *node : twoFoldNodes) {
    VSBNode *n0 = node->neighbors[0];
    VSBNode *n1 = node->neighbors[1];
    n0->replaceNeighbor(node, n1);
    n1->replaceNeighbor(node, n0);
    delete node;
  }
  twoFoldNodes.clear();
}

double VoxelSetBoundary::volume() const {
  double vol = 0.0;
  for(const VSBGraph &graph : graphs)
    vol += graph.volume();
  return vol * microstructure->volumeOfVoxels();    
}

bool VoxelSetBoundary::checkEdges() const {
  bool ok = true;
  for(const VSBGraph &graph : graphs)
    ok &= graph.checkEdges();
  return ok;
}

bool VoxelSetBoundary::checkConnectivity() const {
  bool ok = true;
  for(const VSBGraph &graph : graphs) {
    bool regionOk = graph.checkConnectivity();
    ok &= regionOk;
  }
  return ok;
}

static int nRegionsUsed = 0;	// For figuring out optimal subregions...
static int nHomogCalcs = 0;

void printHomogRegionStats() {
  oofcerr << "printHomogRegionStats: nRegionsUsed=" << nRegionsUsed
	  << " nHomogCalcs=" << nHomogCalcs
	  << " average regions/calc =" << nRegionsUsed/(double)nHomogCalcs
	  << std::endl;
  nRegionsUsed = 0;
  nHomogCalcs = 0;
}

// VoxelSetBoundary::clippedVolume is the core of the element
// homogeneity calculation.  It's called by
// CSkeletonElement::categoryVolumes().

double VoxelSetBoundary::clippedVolume(
			       const std::vector<ICRectangularPrism> &bins,
			       const CRectangularPrism &ebbox,
			       const std::vector<COrientedPlane> &planes)
  const
{
  assert(!planes.empty());
  double vol = 0.0;
  // TODO: Instead of looping over all bins, compute which bvins to
  // use, since we know their sizes.  Or perhaps use an octree
  // structure for the bins so that we can find the bins containing
  // the corners of the element bounding box quickly, and then examine
  // only the bins between the corners.
  for(unsigned int s=0; s<bins.size(); s++) { // loop over bins
    if(!graphs[s].empty() && bins[s].intersects(ebbox)) {
      ++nRegionsUsed;
      VSBGraph *clippedGraph = graphs[s].copyAndClip(planes[0]);
      for(unsigned i=1; i<planes.size(); i++) {
	clippedGraph->clipInPlace(planes[i]);
      }
      vol += clippedGraph->volume();
      delete clippedGraph;
    } // end if graph intersects elements
  }   // end loop over bins s
  ++nHomogCalcs;
  return vol;
} // end VoxelSetBoundary::clippedVolume

void VoxelSetBoundary::findBBox() {
  for(unsigned int i=0; i<graphs.size(); i++) {
    if(!graphs[i].empty()) {
      bbox_ = new CRectangularPrism(graphs[i].bbox());
      for(unsigned int j=i+1; j<graphs.size(); j++)
	if(!graphs[j].empty())
	  bbox_->swallowPrism(graphs[j].bbox());
      return;
    }
  }
}

unsigned int VoxelSetBoundary::size() const {
  unsigned int sz = 0;
  for(unsigned int i=0; i<graphs.size(); i++)
    sz += graphs[i].size();
  return sz;
}
  
void VoxelSetBoundary::saveClippedVSB(const std::vector<COrientedPlane> &planes,
				      const std::string &filenamebase)
  const
{
  std::ofstream f(filenamebase+".dat");
    std::ofstream f2(filenamebase+".lines");
    for(const VSBGraph &graph : graphs) {
    VSBGraph *clippedGraph = graph.copyAndClip(planes[0]);
    for(unsigned i=1; i<planes.size(); i++) {
      clippedGraph->clipInPlace(planes[i]);
    }
    clippedGraph->dump(f);
    clippedGraph->dumpLines(f2, microstructure);
    delete clippedGraph;
  }
  f.close();
  f2.close();
}

void VoxelSetBoundary::drawClippedVSB(const std::vector<COrientedPlane> &planes,
				      LineSegmentLayer *layer)
  const
{
  for(const VSBGraph &graph : graphs) {
    VSBGraph *clippedGraph = graph.copyAndClip(planes[0]);
    for(unsigned i=1; i<planes.size(); i++) {
      clippedGraph->clipInPlace(planes[i]);
    }
    clippedGraph->draw(layer, microstructure);
    delete clippedGraph;
  }
}

void VoxelSetBoundary::dump(std::ostream &os,
			    const std::vector<ICRectangularPrism> &bins)
  const
{
  for(unsigned int s=0; s<graphs.size(); s++) {
    os << "Subregion " << s << " " << bins[s] << std::endl;
    graphs[s].dump(os);
  }
}

void VoxelSetBoundary::dumpLines(const std::string &filename) const {
  for(unsigned int s=0; s<graphs.size(); s++) {
    std::string fname = filename + '_' + to_string(s);
    oofcerr << "# Writing subregion " << s << " to file " << fname
	    << std::endl;
    std::ofstream os(fname);
    graphs[s].dumpLines(os, microstructure);
    os.close();
  }
}
