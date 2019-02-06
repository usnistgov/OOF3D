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
// computing an Element's homogeneity.  Because the size of the
// subregions is determined by the size of the Elements, the VSBs are
// constructed by a Skeleton method, CSkeletonBase::buildVSBs(), not
// by a Microstructure method.

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

// After creating the ProtoVSBNodes, CSkeletonBase::buildVSBs()
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
#include "common/VSB/vsb.h"
#include <limits>

#ifdef DEBUG
static bool verbose = false;
void setVerboseVSB(bool f) { verbose = f; }
bool verboseVSB() { return verbose; }
#endif // DEBUG

void initializeVSB() {
  initializeProtoNodes<Coord3D, ICoord3d>();
}








  











//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


void VSBGraph::dumpLines(std::ostream &os, const CMicrostructure *ms) const {
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


void printHomogRegionStats() {
  oofcerr << "printHomogRegionStats: nRegionsUsed=" << nRegionsUsed
	  << " nHomogCalcs=" << nHomogCalcs
	  << " average regions/calc =" << nRegionsUsed/(double)nHomogCalcs
	  << std::endl;
  nRegionsUsed = 0;
  nHomogCalcs = 0;
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
