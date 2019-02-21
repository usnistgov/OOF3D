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
// (VSB).  See "USAGE", below, for the details.

// OVERVIEW

// This code was developed for OOF3D but is independent of it.  OOF3D
// needs to compute the volume of the intersection of a group of
// voxels (3D pixels) with a finite element (a convex polyhedron).
// These routines compute the shape and volume of the intersection of
// any convex polyhedron with any set of voxels.  The computation is
// robust -- small errors in the calculation of the positions of
// geometrical intersections lead only to small errors in the computed
// volume, which is not true for many simpler methods.

// Computing the intersection voxel by voxel is too slow. This method
// instead uses the boundary (B) of the voxel set (VS), hence the name
// "vsb.h".

// This documentation refers to "images", but the image need not be a
// conventional image.  It is just a three dimensional rectangular
// volume, divided into a rectangular array of identically sized
// rectangular regions (voxels), with a value (category) assigned to
// each voxel.  A voxel set consists of all voxels in the image with
// the same category.

// All classes used here are templates, so that they can work with
// existing image and coordinate classes.  (For simplicity the template
// arguments are omitted in most of the documentation.)

// The VSB is a polyhedron which need not be either convex or simply
// connected.  It's represented by a graph, where each node of the
// graph corresponds to a corner of the polyhedron, and each edge of
// the graph connects the two nodes that correspond to the endpoints
// of an edge of the polyhedron.  There is no class representing
// edges, but each node knows its neighbors, as well as its position
// in space.  Each node has exactly 3 neighbors.  Where the polyhedron
// has corners with more than three edges, the graph contains multiple
// nodes with the same position.

// Actually, the VSB is represented by a bunch of graphs.  The image
// is split into subregions and a separate graph is constructed for
// each subregion.  This allows the expensive graph clipping operation
// to be skipped for large parts of the volume when it's known that
// the voxel set only occupies a small part of the volume.  Because
// the optimal size of the subregions depends on the application, the
// regions are passed in as an argument.

// There are three main parts to the calculation.
// (1) Constructing the graph representation of the VSB.
// (2) Clipping the VSB by planes (the faces of the convex polyhedron).
// (3) Computing the volume of the clipped polyhedron.

// The graphs are VSBGraph objects, and are contained in a VoxelSetBdy
// object.  (The VoxelSetBdy contains a bit more information than the
// VSBGraphs, but pretty much passes all of its work to the graphs.)
// The graphs are constructed by the VoxelSetBdy constructor, which
// creates a 3D array, protoNodes, of ProtoVSBNode pointers at the
// corners of every voxel in each graph's subregion of the
// Microstructure.  Each point in protoNodes is the center of a 2x2x2
// cube of voxels, but only some of the 8 voxels are occupied (ie, in
// the voxel set). (The 2x2x2 cubes on the edges of the image always
// contain some unoccupied voxels.)  At the locations in the array
// where the configuration of voxels in the 2x2x2 cube defines a
// corner of the polyhedron, an instance of a ProtoVSBNode subclass is
// created.

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
// orientation in a table.  VoxelSetBdy::protoVSBNodeFactory()
// returns a pointer to a new ProtoVSBNode of the correct type.  It
// returns nullptr if the arrangement of voxels doesn't define a
// corner of the polyhedron.

// The voxel signatures of the eight single voxel configurations are
// predefined and named "vox000", "vox100", etc, up to "vox111".  The
// three digits in the names are the xyz coordinates of the voxel.
// vox000 is on the negative x, negative y, negative z side of the
// 2x2x2 cube.  vox111 is diagonally opposite.  The signature of any
// multi-voxel configuration can be constructed by the bitwise-or of
// the signatures of its individual voxels, so the configurations are
// referred to as "vox000|vox110", etc.

// When each ProtoVSBNode is created, it creates one or more VSBNodes
// in the VSBGraph, which stores pointers to them in a std::vector.
// It *doesn't* use a 3D array -- there may be more than one VSBNode
// at any point, and the geometrical organization isn't needed after
// graph construction is complete.  The number of VSBNodes per
// ProtoVSBNode depends on the voxel geometry, which is known to the
// ProtoVSBNode subclass.

// After creating the ProtoVSBNodes, the VoxelSetBdy constructor calls
// ProtoVSBNode::connect() to set the nodes' neighbor pointers.  If a
// ProtoVSBNode needs a neighbor in the +x, +y, or +z direction (in
// real space), the constructor finds the next ProtoVSBNode in that
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
// voxels in the 2x2x2 cube share an edge but not a face.  For
// example, the two voxels in configuration "vox000|vox110" share the
// edge in the negative z direction.  In these cases (TwoVoxelsByEdge,
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
// VSBNodes with only two neighbors are stored in the VoxelSetBdy
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
// * We want to be able to clip the same graph multiple times to
//   compute its intersection with many polyhedra, so instead of just
//   clipping in place, we have two methods, VSBGraph::copyAndClip()
//   and VSBGraph::clipInPlace().  copyAndClip() is used to clip at
//   the first polyhedron face, and clipInPlace() is used for the rest.
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


// USAGE

// To construct the boundary of a voxel set, create an object of the
// VoxelSetBdy class.  For example:
//  auto *vsb = new VoxelSetBdy<COORD, ICOORD, IMAGE, IMAGEVAL>(
//               image, imageVal, voxelVolume, subregions);
//
// The arguments are:
//     const IMAGE &image -- a 3D array of voxels
//     const IMAGEVAL &imageVal -- the value of the voxels in the voxel set
//     double voxelVolume -- the volume of a voxel
//     const std::vector<ICRectPrism<ICOORD>> &subregions --
//            a set of 3D regions of the image.  A separate graph will
//            be build in each region. (ICRectPrism is defined in cprism.h.)
//
// The template arguments are:
//   COORD: A coordinate or vector in 3 dimensional space with
//     floating point compenents.  The following member and non-member
//     functions must supported: 
//       COORD(double x, double y, double z)       -- constructor
//       double COORD::operator[](int) const       -- read component
//       double &COORD::operator[](int)            -- read/write component
//       COORD &COORD::operator+=(const COORD&)    -- addition in place
//       double dot(const COORD&, const COORD&)    -- dot product
//       COORD cross(const COORD&, const COORD&)   -- cross product
//       COORD operator+(const COORD&, const COORD&) -- vector addition
//       COORD operator*(const COORD&, double)     -- scalar multiplication
//       COORD operator/(const COORD&, double)     -- scalar division
//
//   ICOORD: Just like COORD, but with integer components.  Used to
//     identify voxels.  The following member and non-member
//     functions must be supported:
//       ICOORD(int, int, int)                     -- constructor
//       int ICOORD::operator[](int) const         -- read component
//       int & ICOORD::operator[](int)             -- read/write a component
//       bool operator==(const ICOORD&, const ICOORD&)  -- equality
//       bool operator!=(const ICOORD&, const ICOORD&)  -- inequality
//       ICOORD operator+(const ICOORD&, const ICOORD&) -- vector addition
//       ICOORD operator-(const ICOORD&, const ICOORD&) -- vector subtraction
//
//   IMAGE: A 3D array of voxels.  It must allow a voxel value to be
//   extracted, given the voxel coordinate as an ICOORD:
//       const IMAGEVAL &IMAGE::operator[](const ICOORD&) const
//
//   IMAGEVAL: The value of a voxel in the image.  It needs an == operator.
//       bool operator==(const IMAGEVAL&, const IMAGEVAL&)
//
//
// Once the VoxelSetBdy has been constructed, the following methods
// are available:
//
// * double VoxelSetBdy::volume()  -- the volume of the voxel set.
//
// * double VoxelSetBdy::clippedVolume(
//      const CRectPrism<COORD> &bbox,
//      const std::vector<VoxelSetBdy::Plane> &planes)
//   Returns the volume of the polyhedron formed by clipping the voxel
//   set with all of the given planes. bbox is the bounding box of the
//   region defined by the planes.  Only subregions that intersect the
//   bounding box will be considered.  If bbox is too large, the
//   routine will work but may be slow.

// There are also some debugging routines:

// * bool checkEdges()
//   just checks that each node has three neighbors, and that if A is
//   a neighbor of B, then B is a neighbor of A.  It returns true if
//   test passes.

// * bool checkConnectivity()
//   checks that the graph has three-vertex connectivity, which means
//   that removing two vertices from the graph doesn't divide it into
//   two disconnected parts.  Because the graph is allowed to have
//   disconnected portions, this test applies to each disconnected
//   subgraph individually.  Three-vertex connectivity is necessary
//   for a well formed graph for a CONVEX polygon.  I don't know if
//   it's sufficient.  checkConnectivity() is very slow (o(N^3)) and
//   should only be run for small graphs, or if you have a lot of free
//   time.  checkConnectivity() returns true if the test passes.

// * void dump(std::ostream&)
//   writes raw data to the given output stream. 

// * void dumpLines(const std::string &filename, CONVERTER &conv)
//   writes the edges of the VSB to the given file in a format that
//   the author found useful for plotting:
//     (x0, y0, z0), (x0, y0, z0) # index0 index1
//   CONVERTER is a template argument, and must be a callable type
//   that converts a COORD in voxel units to whatever format you'd
//   like in the output.

// * void saveClippedVSB(const std::vector<Plane> &planes,
//                       CONVERTER &converter,
//                       const std::string &filenamebase)
//   clips the VSB with the given planes, and writes the lines of the
//   clipped graphs to two files, filenamebase.dat and
//   filenamebase.lines.  The first file is the same as the file
//   produced by dump(), and the second the same as dumpLines().

// * void drawClippedVSB(const std::vector<Plane> &planes,
//                       PLOTTER &plotter)
//   clips the VSB with the given planes and then passes each graph to
//   the given plotter object.  PLOTTER must be callable, with an
//   operator() taking a single argument which is a pointer to a
//       VoxelSetBdy<COORD, ICOORD, int>::Graph.


#ifndef VSB_H
#define VSB_H

#include <assert.h>
#include <fstream>
#include <set>
#include <vector>

#include "array3d.h"
#include "cprism.h"
#include "cplane.h"

#define swap(x, y) { auto temp = (x); x = (y); y = temp; }

template <class COORD, class ICOORD> class ProtoVSBNode;
template <class VOXELSETBOUNDARY> class VSBEdgeIterator;
template <class COORD, class ICOORD> class VSBGraph;
template <class COORD, class ICOORD> class VSBNode;

template <class COORD, class ICOORD, class IMAGE, class IMAGEVAL>
class VoxelSetBdy;

template<class COORD, class ICOORD>
  ProtoVSBNode<COORD, ICOORD> *fetchProtoNode(unsigned char);

// A lot of classes here all need to define the same typedefs.
// typedefs in a template class's base class aren't visible
// to the derived class, so these get repeated often.
#define TEMPLATE_TYPEDEFS \
  typedef VSBNode<COORD, ICOORD> Node; \
  typedef ProtoVSBNode<COORD, ICOORD> ProtoNode; \
  typedef VSBGraph<COORD, ICOORD> Graph;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Predefined voxel signatures for the 8 individual voxels, for all 8
// together, and none of them.
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

template <class IMAGE, class IMAGEVALUE, class ICOORD, class IPRISM>
unsigned char voxelSignature(const IMAGE image, ICOORD &pos, IMAGEVALUE val,
			     const IPRISM &region)
{
  // The voxelSignature indicates which of the eight voxels
  // surrounding a voxel corner in a given subregion of an image
  // have the given value.
  // The inputs are:
  //  image: The image containing the voxels.  
  //  pos: The position of the corner, in voxel units.
  //  val: The value of the voxels that we're interested in.
  //  pt0 and pt1: Two opposite corners of the subregion of the image.
  //  
  // pos is the lower-left-back corner of a voxel, so the components
  // of the coordinates of the other voxels at pos are one less.

  // A bit of the signature is 1 if the voxel corresponding to the bit
  // is in the category, cat.  The correspondence is
  // Bit          Position relative to pos
  // (0 is LSB)   
  // 0  0x1       (-1, -1, -1)
  // 1  0x2       (0, -1, -1)
  // 2  0x4       (-1, 0, -1)
  // 3  0x8       (0, 0, -1)
  // 4  0x10      (-1, -1, 0)
  // 5  0x20      (0, -1, 0)
  // 6  0x40      (-1, 0, 0)
  // 7  0x80      (0, 0, 0)
  unsigned char sig = 0;
  unsigned char b = 1;
  for(int k=0; k<2; k++) {
    for(int j=0; j<2; j++) {
      for(int i=0; i<2; i++) {
	ICOORD offset = pos + ICOORD(i-1, j-1, k-1);
	if(region.contains(offset) && image[offset] == val)
	  sig |= b;
	b <<= 1;
      }
    }
  }
  return sig;
}

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

  void connectClippedNodes(const std::vector<Node*> &newNodes)
    const
  {
    // Each node in newNodes has exactly one neighbor, in slot 0.
    // Starting from that neighbor, go from node to node
    // counterclockwise around the hole in the graph to find the next
    // new node, and connect to it.  We know when we've found the next
    // new node because it won't have a neighbor in slot 1.
    for(Node *newNode : newNodes) {
      Node *vcur = newNode;
      Node *vnext = newNode->getNeighbor(0);
      do {
	// To make a counterclockwise turn from one graph edge to
	// another, pick the outgoing edge that's the *clockwise*
	// neighbor of the incoming edge.
	Node *vtemp = vnext->nextCWNeighbor(vcur);
	vcur = vnext;
	vnext = vtemp;
      } while(vcur->getNeighbor(1) != nullptr);
      vcur->setNeighbor(1, newNode);
      newNode->setNeighbor(2, vcur);
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

  const ICRectPrism<ICOORD> &subregion() const {
    return domain;
  }

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
	    Node *newNode = new Node(p);
	    newNodes.push_back(newNode);
	    thisvert->replaceNeighbor(n, newNode);
	    newNode->setNeighbor(0, thisvert);
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

  // Write out the edges in a plottable form. 
  // CONVERTER is a callable object that takes a COORD and returns a
  // different COORD, in case you want output that's not in voxel
  // units.
  template <typename CONVERTER>
  void dumpLines(std::ostream &os, CONVERTER converter) const {
    for(const Node *vertex : vertices) {
      for(Node *nbr : vertex->neighbors) {
	if(nbr && vertex->index < nbr->index)
	  os << converter(vertex->position) << ", "
	     << converter(nbr->position) << " # "
	     << vertex->index << " " << nbr->index << std::endl;
      }
    }
  }
  // void draw(LineSegmentLayer*, const CMicrostructure*) const;

};				// end template class VSBGraph


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// VSBEdgeIterator can be used to loop over the edges of a clipped
// voxel set boundary, for debugging and graphics.  Its template
// argument is the VoxelSetBdy class that it's iterating over.  Use
// the EdgeIterator typedef in VoxelSetBdy instead of writing it all
// out.
// Use the iterator like this:
//    VoxelSetBdy<COORD,ICOORD,IMAGEVAL>::EdgeIterator iter = vsb->iterator();
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

template <class COORD, class ICOORD, class IMAGE, class IMAGEVAL>
class VoxelSetBdy {
public:
  typedef ProtoVSBNode<COORD, ICOORD> ProtoNode;
  typedef VSBNode<COORD, ICOORD> Node;
  typedef VSBGraph<COORD, ICOORD> Graph;
  typedef VSBPlane<COORD> Plane;
  typedef IMAGEVAL ImageVal;
  typedef VSBEdgeIterator<VoxelSetBdy<COORD, ICOORD, IMAGE, IMAGEVAL>> EdgeIterator;
private:
  // const IMAGEVAL category;
  //  const CMicrostructure *microstructure;
  const double voxelVolume;	// volume of a single voxel
  // There's one VSBGraph for each subregion in the image. 
  std::vector<Graph> graphs;
  CRectPrism<COORD> *bbox_;
public:
  VoxelSetBdy(const IMAGE &image,
	      const IMAGEVAL &imageVal,
	      double voxVol,
	      const std::vector<ICRectPrism<ICOORD>> &subregions
	      )
    : voxelVolume(voxVol),
      bbox_(nullptr)
  {
    // Create and populate a graph for each subregion of the image.
    graphs.reserve(subregions.size());
    for(unsigned int s=0; s<subregions.size(); s++) {
      const ICRectPrism<ICOORD> &bin = subregions[s];
      graphs.emplace_back(bin);
      // Create an array of ProtoVSBNodes in the bin.  A ProtoVSBNode is
      // the precursor to the actual VSBNodes.  There's a ProtoVSBNode
      // at each corner of each voxel, but neighboring voxels share
      // ProtoVSBNodes.  The array of protonodes is one larger in each
      // dimension than the array of voxels.
      ICRectPrism<ICOORD>
	expanded(bin.lowerleftback(), bin.upperrightfront()+ICOORD(1,1,1));
      Array3D<ProtoNode*, ICOORD, ICRectPrism<ICOORD>>
	protoNodes(expanded, nullptr);
      for(auto i=protoNodes.begin(); i!=protoNodes.end(); ++i) {
	// The type of ProtoVSBNode depends on which of the 8 voxels
	// surrounding the corner point are in the current category.
	// The bits in the signature indicate which voxels are in the
	// category.
	char signature = voxelSignature(image, i.coord(), imageVal, bin);
	// protoVSBNodeFactory returns a ProtoNode and also creates the
	// VSBNodes in the graph, but it doesn't connect them.  That can
	// be done only after all the ProtoNodes are constructed.
	*i = protoVSBNodeFactory(s, signature, i.coord());
      }
      // Loop over protonodes, connecting each one to the next protoNode
      // in the x, y, and z directions.
      for(auto i=protoNodes.begin(); i!=protoNodes.end(); ++i) {
	ICOORD here = i.coord();
	ProtoNode *pnode = protoNodes[here];
	if(pnode != nullptr) {
	  // Get the reference space directions in which this ProtoNode
	  // needs to find neighbors.
	  const std::vector<VoxelEdgeDirection> &dirs(pnode->connectDirs());
	  for(const VoxelEdgeDirection &dir : dirs) {
	    // Convert the reference space directions to real space.
	    VoxelEdgeDirection actualDir = pnode->rotation.toActual(dir);
	    // It's only necessary to look in the positive directions
	    // because the connections in the negative directions are
	    // checked when examining the other node of the edge.
	    if(actualDir.dir == 1) {
	      unsigned int c = actualDir.axis;
	      // Look for the next protoNode in this direction
#ifndef NDEBUG
	      bool found = false;
#endif // NDEBUG
	      for(int k=here[c]+1; k<=bin.upperrightfront()[c]; k++) {
		ICOORD there = here;
		there[c] = k;
		if(protoNodes[there] != nullptr) { // found the next node
#ifndef NDEBUG
		  found = true;
#endif // NDEBUG
		  protoNodes[here]->connect(protoNodes[there]);
		  break;		// done with this direction at this point
		}
	      } // end sesarch for protoNode in direction c
#ifndef NDEBUG
	      if(!found) {
		std::cerr << "buildVSB: failed to find next node!" << std::endl;
		std::cerr << "buildVSB: here=" << here << "c=" << c
			  << " val=" << imageVal << std::endl;
		assert(false);
	      }
#endif // NDEBUG
	    } // end if actualDir is positive

	  } // end loop over connection directions
	}	  // end if pnode != nullptr
      }	  // end loop over array of protoNodes

      // Remove the 2-fold connected nodes
      fixTwoFoldNodes(s);

      // Delete the protoNodes.
      for(auto i=protoNodes.begin(); i!=protoNodes.end(); ++i)
	delete *i;

    } // end loop over subregions

    findBBox();
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

  // VoxelSetBdy::clippedVolume computes the volume of the voxels that
  // is inside the volume defined by the given planes.
  //  * ebbox is the bounding box of the region delimited by the planes.
  //  * planes is the set of clipping planes.

  double clippedVolume(const CRectPrism<COORD> &ebbox,
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

    for(const Graph &graph : graphs) {
      if(graph.subregion().intersects(ebbox)) {
	++nRegionsUsed;
	Graph *clippedGraph = graph.copyAndClip(planes[0]);
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

  VSBEdgeIterator<VoxelSetBdy<COORD, ICOORD, IMAGE, IMAGEVAL>> iterator()
    const
  {
    return VSBEdgeIterator<VoxelSetBdy<COORD, ICOORD, IMAGE, IMAGEVAL>>(this);
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
  
  void dump(std::ostream &os) const {
    for(unsigned int s=0; s<graphs.size(); s++) {
      const Graph &graph = graphs[s];
      os << "Subregion " << s << " " << graph.subregion() << std::endl;
      graph.dump(os);
    }
  }

  // CONVERTER is a callable object that takes a COORD and returns a
  // different COORD, in case you want output that's not in voxel
  // units.
  template <class CONVERTER>
  void dumpLines(const std::string &filename, CONVERTER &converter) const {
    for(unsigned int s=0; s<graphs.size(); s++) {
      std::string fname = filename + '_' + std::to_string(s);
      std::cerr << "# Writing subregion " << s << " to file " << fname
		<< std::endl;
      std::ofstream os(fname);
      graphs[s].dumpLines(os, converter);
      os.close();
    }
  }

  template <class CONVERTER>
  void saveClippedVSB(const std::vector<Plane> &planes,
		      CONVERTER &converter,
		      const std::string &filenamebase)
    const
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

  template <class PLOTTER>
  void drawClippedVSB(const std::vector<Plane> &planes,
		      PLOTTER &plotter)
    const
  {
    for(const Graph &graph : graphs) {
      Graph *clippedGraph = graph.copyAndClip(planes[0]);
      for(unsigned int i=1; i<planes.size(); i++)
	clippedGraph->clipInPlace(planes[i]);
      plotter(clippedGraph);
      delete clippedGraph;
    }
  }
  
  friend class VSBEdgeIterator<VoxelSetBdy>;
};				// end template class VoxelSetBdy

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// protonodes.h defines the specific ProtoVSBNode subclasses and
// initializers.

#include "protonodes.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#undef swap
#endif // VSB_H
