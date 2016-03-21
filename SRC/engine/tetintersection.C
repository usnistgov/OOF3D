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

#include "common/IO/oofcerr.h"
#include "common/cmicrostructure.h"
#include "common/pixelsetboundary.h"
#include "common/printvec.h"
#include "engine/coincidences.h"
#include "engine/cskeletonelement.h"
#include "engine/tetintersection.h"

#include <math.h>
#include <algorithm>

// TODO: PixelBdyIntersections need to be deleted!

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Various tolerances have to be used to account for roundoff errors.
// All tolerances are in pixel units.

// Intersection facets with areas less than AREATOL are ignored.
#define AREATOL 0.0 //1.e-8

// When barycentric coordinates are used to determine if a point is on
// an edge or face of a tet, values less than BARYTOL are equivalent
// to zero.
// #define BARYTOL 2.e-6
// #define BARYTOLFACE 1.e-12
#define BARYTOL 0.0
#define BARYTOLFACE 0.0

// // When a point is known for topological reasons to be on a tet edge,
// // the measured distance to the edge must be less than EDGETOL.
// #define EDGETOL 1.e-4 

// Also, see POINTTOL2 in common/pixelsetboundary.h.

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// When debugging it's convenient to turn on verbose output only for
// particular voxel categories and pixel planes.

#ifdef DEBUG

bool verboseCategory(bool verbose, unsigned int category) {
  return verbose
    // && (category == 1)
    ;
};

bool verbosePlane(bool verbose, const PixelPlane &pixplane) {
  // return false;
  return verbose
    // && (
    // 	(pixplane.direction() == 2 && pixplane.normalOffset() == 2
    // 	 && pixplane.normalSign() == -1)
    //   	// || (pixplane.direction() == 2 && pixplane.normalOffset() == 1
    // 	//     && pixplane.normalSign() == -1)
    // 	// // || (pixplane.direction() == 0 && pixplane.normalOffset() == 4
    // 	// //     && pixplane.normalSign() == 1)
    // 	)
    ;
}

#include <fstream>
std::ofstream *dumpfile = 0;

void openDumpFile(const std::string &name) {
  if(dumpfile)
    dumpfile->close();
  oofcerr << "openDumpFile: opening " << name << std::endl;
  dumpfile = new std::ofstream(name.c_str());
}

void dumpSegment(const Coord3D &a, const Coord3D &b) {
  // TODO: This ought to convert from pixel coordinates to physical
  // coordinates.
  if(dumpfile) {
    *dumpfile << a << ", " << b << std::endl;
  }
}

void closeDumpFile() {
  if(dumpfile) {
    dumpfile->close();
    dumpfile = 0;
  }
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// // Given two 3D points p0 and p1 and a triangle t0, t1, t2, find the
// // intersection of the segment with the triangle.  Do it in a way
// // that's symmetric under reorderings of the points to ensure that the
// // roundoff error is reproducible if the segment or triangle is
// // defined differently.

// // The intersection point X is at
// //    X = p0 + alpha0*(p1 - p0), then
// //    alpha0 = ((C-p0) dot N)/((p1-p0) dot N)
// // where C could be any point in the plane of the triangle, but we use
// // the center to make it symmetric to reordering of t.
// // We can switch the indices of p0 and p1 to get an equivalent
// // expression,
// //    X = p1 + alpha1*(p0 - p1)
// //    alpha1 = ((C-p1) dot N)/((p0-p1) dot N)
// //and then average the two to get a symmetric version:
// //    X = 0.5 [p0 + p1 + (alpha0 - alpha1)*(p1 - p0)]
// //      = 0.5 [p0 + p1 + (p1-p0)*((2C - (p0 + p1)) dot N)/((p1-p0) dot N)

// static Coord3D segmentFaceIntersection(const ICoord3D &p0, const ICoord3D &p1,
// 				       const std::vector<Coord3D> &t
// #ifdef DEBUG
// 				       , bool verbose=false
// #endif // DEBUG
// 				       )
// {
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "segmentFaceIntersection: p0=" << p0 << " p1=" << p1
//   	    << std::endl;
//     // oofcerr << "segmentFaceIntersection: t=";
//     // std::cerr << t;
//     // oofcerr << std::endl;
//   }
// #endif // DEBUG
//   Coord3D N = t[0]%t[1] + t[1]%t[2] + t[2]%t[0]; // triangle normal
//   Coord3D C = (t[0] + t[1] + t[2])/3.0;	       // triangle center
//   ICoord3D psum = p0 + p1;
//   ICoord3D pdiff = p1 - p0;
// #ifdef DEBUG
//   if(dot(pdiff, N) == 0.0) {
//     if(verbose)
//       oofcerr << "segmentFaceIntersection: dot product is zero! pdiff=" << pdiff
// 	      << " N=" << N << std::endl;
//     throw ErrProgrammingError("segmentFaceIntersection failed!",
// 			      __FILE__, __LINE__);
//   }
// #endif // DEBUG
//   return 0.5 * (psum + pdiff*dot(2*C - psum, N)/dot(pdiff, N));
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given a point x that lies on the line joining p0 and p1, return the
// fractional distance of x from p0 towards p1.  That is, return 0 if
// x is at p0, 1 if x is at p1, and something between 0 and 1 if x is
// in the middle.  The result is negative or greater than 1 if x does
// not lie on the segment (p0, p1).

// static double fractionalDistance(const Coord2D &x, const Coord2D &p0,
// 				 const Coord2D &p1)
// {
//   assert(p0 != p1);
//   Coord2D dp = p1 - p0;
//   return dot((x-p0), dp)/dot(dp, dp);
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: faceNormal and faceOffset should be computed and stored by
// the HomogeneityTet constructor for all faces.

// Compute the unnormalized outward normal vector of the given face.

static Coord3D faceNormal(int faceIndex, const std::vector<Coord3D> &epts) {
  Coord3D pt0 = epts[vtkTetra::GetFaceArray(faceIndex)[0]];
  Coord3D pt1 = epts[vtkTetra::GetFaceArray(faceIndex)[1]];
  Coord3D pt2 = epts[vtkTetra::GetFaceArray(faceIndex)[2]];
  // This is *not* the symmetric expression for the normal, so it
  // might not be appropriate in all circumstances.  The symmetric but
  // more expensive form is pt0%pt1 + pt1%pt2 + pt2%pt0
  return (pt1 - pt0) % (pt2 - pt0);
}

// Compute the distance from the origin to the plane of the given face.

static double faceOffset(int faceIndex, const std::vector<Coord3D> &epts) {
  Coord3D pt0 = epts[vtkTetra::GetFaceArray(faceIndex)[0]];
  Coord3D pt1 = epts[vtkTetra::GetFaceArray(faceIndex)[1]];
  Coord3D pt2 = epts[vtkTetra::GetFaceArray(faceIndex)[2]];
  Coord3D normvec = faceNormal(faceIndex, epts);
  // TODO: can the offset be found without using a sqrt?
  normvec /= sqrt(norm2(normvec));
  return dot((pt0 + pt1 + pt2)/3., normvec);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: FacePlanes should be constructed by the HomogeneityTet
// constructor, which should notice if a face is in a pixel plane and
// avoid the arithmetic in faceNormal and faceOffset if it can.

FacePlane::FacePlane(unsigned int f, const std::vector<Coord3D> &epts)
  : Plane(faceNormal(f, epts), faceOffset(f, epts), true),
    face(f)
{}

void FacePlane::print(std::ostream &os) const {
  os << "FacePlane(face=" << face << ", offset=" << offset_
     << ", normal=" << unitNormal_ << ")";
}
	  

PixelBdyIntersection::PixelBdyIntersection(
	   const PixelPlane &pixplane,
	   unsigned int face, // index of tet face containing polyogn segment
	   unsigned int segment, // polygon segment
	   double frac,	  // fractional distance along polygon segment
	   bool entry,
	   const PixelBdyLoop *loop,
	   unsigned int loopseg,
	   double loopfrac,
	   const std::vector<Coord3D> &epts,
	   const std::vector<const PixelPlane*> &facePlanes,
	   BaryCoordCache &baryCache)
  : segment(segment),
    face(face),
    fraction(frac),
    entry(entry),
    loop(loop),
    loopseg(loopseg),
    loopfrac(loopfrac)
{
  // The intersection point is where the PixelPlane, the FacePlane,
  // and the plane of the loop segment meet.

  // TODO: Just set ptr to existing FacePlane in HomogeneityTet
  FacePlane *fp = new FacePlane(face, epts);
  
  // Find which direction the PixelBdyLoop segment runs
  PixelBdyLoopSegment pbls(loop, loopseg);
  ICoord3D pbs0 = pixplane.convert2Coord3D(pbls.firstPt());
  ICoord3D pbs1 = pixplane.convert2Coord3D(pbls.secondPt());
  unsigned int segdir = NONE;
  for(unsigned int i=0; i<3; i++) {
    if(pbs0[i] != pbs1[i]) {
      segdir = i;
      break;
    }
  }
  assert(segdir != NONE);

  // The normal direction of the plane containing the segment is the
  // direction that isn't either segdir or the pixelplane direction.
  int segnorm = 3 - segdir - pixplane.direction();
  int segoffset = pbs0[segnorm];
  OOFcerrIndent indent(2);
  oofcerr << "PixelBdyIntersection: pixplane=" << pixplane << std::endl;
  oofcerr << "PixelBdyIntersection::ctor: loopseg=" << loopseg << std::endl;
  oofcerr << "PixelBdyIntersection::ctor: pbls=" << pbls
	  << " segdir=" << segdir << std::endl;
  // TODO: HomogeneityTet should own the PixelPlanes.  This is a memory leak.
  PixelPlane *pixplane2 = new PixelPlane(segnorm, segoffset, 1);
  planes = new TriplePlaneIntersection(fp, &pixplane, pixplane2);

  location3D = planes->point();
  location2D = pixplane.convert2Coord2D(location3D);

  baryCoord = getBarycentricCoord(location3D, epts, facePlanes, baryCache);
}

PixelBdyIntersection::~PixelBdyIntersection() {
  delete planes;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


static double fractionalDistance(const BarycentricCoord &b0,
				 const BarycentricCoord &b1,
				 const BarycentricCoord &pt)
{
  unsigned int kbest = NONE;
  double dbest = -std::numeric_limits<double>::max();
  for(unsigned int k=0; k<4; k++) {
    double d = fabs(b0[k] - b1[k]);
    if(d > dbest) {
      dbest = d;
      kbest = k;
    }
  }
  assert(b1[kbest] != b0[kbest]);
  return (pt[kbest] - b0[kbest])/(b1[kbest] - b0[kbest]);
}

// pinUnitRange removes roundoff error on quantities that are known to
// be between 0 and 1, inclusive.

static double pinUnitRange(double x
#ifdef DEBUG
			   , bool verbose
#endif
			   )
{
#ifdef DEBUG
  if(verbose) {
    if(x < 0.0)
      oofcerr << "pinUnitRange: correcting " << x << " to 0.0" << std::endl;
    else if(x > 1.0)
      oofcerr << "pinUnitRange: correcting 1+" << x-1 << " to 1.0" << std::endl;
  }
#endif // DEBUG
  if(x < 0.0)
    return 0.0;
  if(x > 1.0)
    return 1.0;
  return x;
}
 
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static std::vector<Coord3D> faceNodes(unsigned int faceIndex,
				      const std::vector<Coord3D> &epts)
{
  assert(faceIndex < 4);
  std::vector<Coord3D> nodes;
  nodes.reserve(3);
  for(unsigned int i=0; i<3; i++)
    nodes.push_back(epts[vtkTetra::GetFaceArray(faceIndex)[i]]);
  return nodes;
}

// Find the nodes of an edge of a face, going counterclockwise around
// the face.  The faceIndex is the vtk index.  The edgeIndex is the
// index of the edge on the face, not on the tet.  Different versions
// return the coordinates of the nodes, their indices, or both.

static void edgeNodes(unsigned int faceIndex, unsigned int edgeIndex,
		      unsigned int &inode0, unsigned int &inode1)
{
  assert(edgeIndex < NUM_TET_FACE_EDGES);
  assert(faceIndex < NUM_TET_FACES);
  unsigned int edgeid = CSkeletonElement::faceEdges[faceIndex][edgeIndex];
  if(CSkeletonElement::faceEdgeDirs[faceIndex][edgeIndex] == 1) {
    inode0 = vtkTetra::GetEdgeArray(edgeid)[0];
    inode1 = vtkTetra::GetEdgeArray(edgeid)[1];
  }
  else {
    inode0 = vtkTetra::GetEdgeArray(edgeid)[1];
    inode1 = vtkTetra::GetEdgeArray(edgeid)[0];
  }
}

// static void edgeNodes(unsigned int faceIndex, unsigned int edgeIndex,
// 		      const std::vector<Coord3D> &epts,
// 		      Coord3D &node0, Coord3D &node1)
// {
//   unsigned int inode0, inode1;
//   edgeNodes(faceIndex, edgeIndex, inode0, inode1);
//   node0 = epts[inode0];
//   node1 = epts[inode1];
// }

static void edgeNodes(unsigned int faceIndex, unsigned int edgeIndex,
		      const std::vector<Coord3D> &epts,
		      Coord3D &node0, Coord3D &node1,
		      unsigned int &inode0, unsigned int &inode1)
{
  edgeNodes(faceIndex, edgeIndex, inode0, inode1);
  node0 = epts[inode0];
  node1 = epts[inode1];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Figure out if the given face of the tet lies on a plane between two
// layers of voxels (or is on an external boundary).  That is, is one
// of the components of the node positions the same for all three
// nodes, and an integer?

static bool faceIsOnVoxelPlane(unsigned int faceIndex,
			       const std::vector<Coord3D> &epts,
			       PixelPlane &pixplane)
{
  std::vector<Coord3D> nodes(faceNodes(faceIndex, epts));
  for(int c=0; c<3; c++) {	// loop over directions
    double x = nodes[0][c];
    // TODO: Is x==floor(x) robust?  If nodes are moved to a voxel
    // boundary in snapnodes, for example, they're moved to a point
    // given in physical units.  That point is converted to voxel
    // units by dividing by the voxel dimensions.  Is the value in
    // voxel units guaranteed to be an integer?  Do positions that
    // arise from snapping need to be saved as (integer,dx) so that
    // the integer can be extracted robustly?
    if(x == floor(x) && nodes[1][c] == x && nodes[2][c] == x) {
      // If the c-component of the position of the node that's not on
      // this face is greater than the offset, then the normal is
      // negative.
      int normal = (epts[CSkeletonElement::oppNode[faceIndex]][c] > x ?
		    -1 : 1);
      pixplane = PixelPlane(c, x, normal);
      return true;
    }
  }
  return false;
}

// // Find out if the two given points are on the same face of the given
// // tetrahedron.  If they're on different faces, or both on the same
// // edge, return false.  Otherwise, return true and set 'face' to the
// // index of the shared face.

// static bool findCrossedFace(const BarycentricCoord &bcoords0,
// 			    const BarycentricCoord &bcoords1,
// #ifdef DEBUG
// 			    bool verbose,
// #endif // DEBUG
// 			    unsigned int &face)
// {
//   // The barycentric coordinates of a point in a tet are a linear
//   // combination of the corners of the tet.  If a point is on a face,
//   // then the barycentric coord corresponding to the node opposite
//   // that face must be zero.

//   unsigned int nboth = 0; // no. of bcoords which are zero for both points
//   for(unsigned int f=0; f<NUM_TET_FACES && nboth < 2; f++) {
//     unsigned int i = CSkeletonElement::oppNode[f];
//     bool zero0 = fabs(bcoords0[i]) <= BARYTOL;
//     bool zero1 = fabs(bcoords1[i]) <= BARYTOL;
//     if(zero0 && zero1) {
//       nboth++;
//       face = f;
//     }
//   }
// // #ifdef DEBUG
// //   if(verbose) {
// //     oofcerr << "findCrossedFace: bcoords0=" << bcoords0
// // 	    << " bcoords1=" << bcoords1
// // 	    << " face=" << face << " nboth=" << nboth
// // 	    << std::endl;
// //   }
// // #endif // DEBUG

//   // If nboth >= 2, then the points are on the same edge and don't
//   // cross a face.
//   return nboth == 1;
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class EdgePoint {
public:
  const unsigned int edge;
  const double t;
  EdgePoint(unsigned int e, double t)
    : edge(e), t(t)
  {}
};

// // Find the edge of a face that's closest to the given point, and the
// // parametric position along the edge of the projection of the point
// // onto the edge. The parametric coordinate increases counterclockwise
// // around the face.  It is not necessarily the same direction used by
// // TetPlaneIntersectionPoint.

// static EdgePoint findClosestEdge(const Coord3D &pt, unsigned int faceIndex,
// 				 const std::vector<Coord3D> &epts)
// {
//   double min_dist2 = std::numeric_limits<double>::max();
//   // min_t is the parametric position along the closest edge seen so far.
//   double min_t = 0;		// two mints in one
//   unsigned int min_e = 0;	// index of the closest edge
//   for(unsigned int edge=0; edge<3; edge++) { // face index of the edge
//     Coord3D node0, node1;
//     edgeNodes(faceIndex, edge, epts, node0, node1);
//     // TODO: Precompute lengths of the tet sides.
//     double invlen2 = 1./norm2(node1 - node0);
//     double dist2 = norm2((node1 - node0) % (pt - node0))*invlen2;
//     if(dist2 < min_dist2) {
//       min_dist2 = dist2;
//       min_e = edge;
//       min_t = dot(node1-node0, pt-node0)*invlen2;
//     }
//   }
//   if(min_t < 0.0)
//     min_t = 0.0;
//   if(min_t > 1.0)
//     min_t = 1.0;
// #ifdef DEBUG
//   if(min_dist2 >= EDGETOL) {
//     oofcerr << "findClosestEdge: point " << pt << " is not on an edge of face "
// 	    << faceIndex << std::endl;
//     oofcerr << "findClosestEdge:    min_dist2=" << min_dist2 << std::endl;
//     oofcerr << "findClosestEdge:    epts=";
//     std::cerr << epts;
//     oofcerr << std::endl;
//     double bcoords[4];
//     int ok = vtkTetra::BarycentricCoords(
// 				 const_cast<Coord3D&>(pt).xpointer(),
// 				 const_cast<double*>(epts[0].xpointer()),
// 				 const_cast<double*>(epts[1].xpointer()),
// 				 const_cast<double*>(epts[2].xpointer()),
// 				 const_cast<double*>(epts[3].xpointer()),
// 				 bcoords);
//     if(!ok)
//       oofcerr << "findClosestEdge: element is degenerate" << std::endl;
//     else {
//       oofcerr << "findClosestEdge: bcoords:";
//       for(unsigned int i=0; i<4; i++)
// 	oofcerr << " " << bcoords[i];
//       oofcerr << std::endl;
//     }
//     throw ErrProgrammingError("findClosestEdge failed!", __FILE__, __LINE__);
//   }
// #endif // DEBUG
//   // assert(min_dist2 < EDGETOL);	// pretty small, in pixel units
//   return EdgePoint(min_e, min_t);
// }


// Given a barycentric coordinate b, find out which edge of face f
// it's on, and its parametric position along the edge.

static bool find_edge(const BarycentricCoord &b, unsigned int f,
#ifdef DEBUG
			  bool verbose,
#endif // DEBUG
			  double &t, unsigned int &fEdge
			  )		  
{
  unsigned int oppNode = CSkeletonElement::oppNode[f];
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "find_edge: b=" << b << " f=" << f << " oppNode=" << oppNode
// 	    << std::endl;
//   }
//   // if(b[oppNode] != 0)
//   //   oofcerr << "find_edge: b=" << b << " f=" << f << std::endl;
// #endif // DEBUG
  assert(b[oppNode] <= BARYTOL);

  // Since b is on an edge, two of its components must be zero.  We
  // know one of them is oppNode.  Find the other one.

  // TODO: Just look for 0 components.  Don't bother with looking for
  // the smallest.
  unsigned int k = NONE;
  double smallest = std::numeric_limits<double>::max();
  for(unsigned int i=0; i<4; i++) {
    if(i != oppNode) {
      double bi = fabs(b[i]);
      if(bi < smallest) {
	smallest = bi;
	k = i;
      }
    }
  }
  if(smallest > BARYTOL) {
#ifdef DEBUG
  if(verbose) {
    oofcerr << "find_edge: point is not not on an edge!  b=" << b
	    << " f=" << f << std::endl;
    // throw ErrProgrammingError("find_edge failed!", __FILE__, __LINE__);
  }
#endif // DEBUG
    return false;
  }
  
  // The edge we're looking for is the tet edge that doesn't include
  // the nodes oppNode and k.
  unsigned int notthisedge = CSkeletonElement::nodeNodeEdge[oppNode][k];
  // 'edge' is the tet index of the edge we're after.
  unsigned int edge = CSkeletonElement::oppEdge[notthisedge];
  // 'fEdge' is the face index of the edge.
   fEdge = CSkeletonElement::tetEdge2FaceEdge[f][edge];
  // 'node0' and 'node1' are the indices of the nodes on the edge.
  unsigned int node0, node1;
  edgeNodes(f, fEdge, node0, node1);
  t = b[node1]/(b[node0] + b[node1]);
  if(t < 0)
    t = 0.0;
  if(t > 1.0)
    t = 1.0;
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "find_edge: edge=" << edge << " fEdge=" << fEdge
// 	    << " node0=" << node0 << " node1=" << node1 << " t=" << t
// 	    << std::endl;
//   }
// #endif	// DEBUG
  return true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given the corners of a convex polygon, find an interior point whose
// coordinates are not integers.  This is used to generate input for
// PixelBdyLoop::contains(), which is more efficient if it knows that
// its input can't coincide with a corner of a loop (and all of its
// corners are at integer coordinates).

static bool isIntCoord(const Coord2D &c) {
  return (c[0] == floor(c[0]) || c[1] == floor(c[1]));
}

Coord2D nonIntegerInteriorPt(const std::vector<Coord2D> &corners) {
  Coord2D trialPt;
  // Use the center of the polygon for the first trial point.
  for(std::vector<Coord2D>::const_iterator c=corners.begin(); c!=corners.end();
      ++c)
    trialPt += *c;
  trialPt /= corners.size();
  if(!isIntCoord(trialPt)) {
    return trialPt;
  }
  // We will almost never get past this point so it doesn't matter how
  // ugly the code is.  The scheme here is to construct a new trial
  // point that's on the line between the current trial point and a
  // corner.  Because the polygon is convex, that point is guaranteed
  // to also be interior.  If that fails, move towards the next
  // corner.  The fractional distance of the move is decreased on each
  // step, in case the original distances are integers.
  double fact = 1049./2048.;
  double frac = 0.51;
  for(std::vector<Coord2D>::const_iterator c=corners.begin(); c!=corners.end();
      ++c)
    {
      // Create another interior point near corner c;
      trialPt = (1-frac)*(*c) + frac*trialPt;
      if(!isIntCoord(trialPt)) {
	return trialPt;
      }
      // The point still has integer coordinates.  Reduce the
      // fractional distance by something unlikely to land on another
      // integer point.
      frac *= fact;
    }
  // This really can't happen unless the polygon is degenerate.
  oofcerr << "nonIntegerInteriorPt: corners=";
  std::cerr << corners;
  oofcerr << std::endl;
  throw ErrProgrammingError("nonIntegerInteriorPt failed!", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const PixelBdyIntersection &pbi) {
  int prec = os.precision();
  os << std::setprecision(20);
  os << "PixelBdyIntersection(" << pbi.location2D
     << ", " << pbi.location3D
     << ", " << pbi.baryCoord
     << ", segment=" << pbi.segment
     << ", fraction=" << pbi.fraction
     << ", loop=" << pbi.loop
     << ", loopseg=" << pbi.loopseg
     << " (" << pbi.loop->icoord(pbi.loopseg)
     << ", " << pbi.loop->next_icoord(pbi.loopseg)
     << "), loopfrac=" << pbi.loopfrac << ", "
     << (pbi.entry? "entry" : "exit") << ")";
  os << std::setprecision(prec);
  return os;
}

// template <class OSTREAM>
// OSTREAM &operator<<(OSTREAM &os, const ElEdgeMap &eem) {
//   bool firstone = true;
//   OOFcerrIndent indent(2);
//   for(ElEdgeMap::const_iterator i=eem.begin(); i!=eem.end(); ++i) {
//     if(!firstone) {
//       os << std::endl;
//     }
//     os << (*i).first << ": " << *(*i).second;
//     firstone = false;
//   }
//   return os;
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the points at which the edges of a tet intersect a voxel
// plane, specified by a normal direction c and an integer offset.

// This constructs points that are correct only for PixelPlanes
// with normal==1.  The Coord2Ds have to be transposed when they're
// used on planes with normal==-1.

// TODO OPT: Would it be more efficient to compute the
// TetPlaneIntersectionPoints for all offsets at once?

void findTetPlaneIntersectionPoints(
			      const std::vector<Coord> &epts,
			      const PixelPlane &pixplane,
#ifdef DEBUG
			      bool verbose,
#endif // DEBUG
			      std::vector<TetPlaneIntersectionPoint> &result,
			      unsigned int &excludeFace)
{
  result.clear();
  result.reserve(4);
  excludeFace = NONE;
  std::vector<unsigned int> overnodes;	// tet nodes above the plane
  std::vector<unsigned int> undernodes;	// tet nodes below the plane
  std::vector<int> altitude(4, 2); // is node above (1), on (0) or below (-1)?
  int c = pixplane.direction();
  double offset = pixplane.normalOffset();
  PixelPlane pp(c, offset, 1);
  for(unsigned int k=0; k<NUM_TET_NODES; ++k) {
    double h = epts[k][c];
    if(h == offset) {
      altitude[k] = 0;
      // The tet node is on the plane.  Choose an edge that's not in
      // the plane, and whose other end is in the opposite direction
      // as the pixelplane normal, and put the
      // TetPlaneIntersectionPoint at the end of the edge.  If there
      // is no such edge, then the tet must just graze the voxel
      // category but doesn't really intersect it.
      Coord2D pt(pp.convert2Coord2D(epts[k]));
      bool done = false;
      for(unsigned int kk=0; kk<NUM_TET_NODES && !done; ++kk) {
	if((pixplane.normalSign() == 1 && epts[kk][c] < offset) ||
	   (pixplane.normalSign() == -1 && epts[kk][c] > offset))
	  {
	    unsigned int edgeId = CSkeletonElement::nodeNodeEdge[k][kk];
	    int *segnodes = vtkTetra::GetEdgeArray(edgeId);
	    if(k == segnodes[0] && kk == segnodes[1]) {
	      result.push_back(TetPlaneIntersectionPoint(
						 pt, nodeBCoord(k), 0, edgeId));
	    }
	    else if(k == segnodes[1] && kk == segnodes[0]) {
	      result.push_back(TetPlaneIntersectionPoint(
						 pt, nodeBCoord(k), 1, edgeId));
	    }
	    else
	      throw ErrProgrammingError("Unexpected node/edge indices! (1)",
					__FILE__, __LINE__);
	    done = true;
	  }
      }	// end search for a suitable edge
      if(!done) {
	// There is a node (or two) in the plane, but the tet doesn't
	// otherwise intersect it, or it lies entirely on the wrong
	// side.  Just return an empty result vector.
	return;
      }
    }
    else if(h < offset) {
      altitude[k] = -1;
      undernodes.push_back(k);
    }
    else if(h > offset) {
      altitude[k] = 1;
      overnodes.push_back(k);
    }
  } // end loop over nodes tet nodes k
  
  if(!(undernodes.empty() && overnodes.empty())) {
    for(unsigned int i=0; i<undernodes.size(); i++) {
      unsigned int ii = undernodes[i];
      for(unsigned int j=0; j<overnodes.size(); j++) {
	unsigned int jj = overnodes[j];
	if(jj == ii)
	  continue;
	Coord2D p0(pp.convert2Coord2D(epts[ii]));
	Coord2D p1(pp.convert2Coord2D(epts[jj]));
	double c0 = epts[ii][c];
 	double c1 = epts[jj][c];
	double cfactor = 1./(c1 - c0);
	// This formula for the intersection is symmetric in the order
	// of the points, so round-off error won't make identical
	// points appear to be different when the order of the tet
	// points is changed.
	Coord2D isec = 0.5*(p0 + p1 + (p1-p0)*(2*offset-(c0+c1))*cfactor);
	// t is the parametric position of the intersection point
	// along the tet edge.  
	double t = (offset - c0)*cfactor;
	// TODO: Do we need to correct for roundoff error?
	// if(t > 1.0)
	//   t = 1.0;
	// else if(t < 0)
	//   t = 0.0;
	BarycentricCoord b = averageBary(nodeBCoord(ii), nodeBCoord(jj), t);

	unsigned int edgeId = CSkeletonElement::nodeNodeEdge[ii][jj];
	// Decide if the order of the nodes is canonical, according to
	// the vtk scheme, and create the TetPlaneIntersectionPoint object.
	int *segnodes = vtkTetra::GetEdgeArray(edgeId);
	if(ii == segnodes[0] && jj == segnodes[1]) 
	  result.push_back(TetPlaneIntersectionPoint(isec, b, t, edgeId));
	else if(ii == segnodes[1] && jj == segnodes[0])
	  result.push_back(TetPlaneIntersectionPoint(isec, b, 1-t, edgeId));
	else
	  throw ErrProgrammingError("Unexpected node/edge indices! (2)",
				    __FILE__, __LINE__);
      }
    }
  } // end if undernodes && overnodes are not both empty

  // A face that does not have nodes in both undernodes and overnodes
  // doesn't contribute any segments to the polygon.  There can be at
  // most one such face if the polygon exists.  Set excludeFace to its
  // index.
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "findTetPlaneIntersectionPoints: pixplane=" << pixplane
// 	    << std::endl;
//     for(unsigned int i=0; i<NUM_TET_NODES; i++)
//       oofcerr << "findTetPlaneIntersectionPoints: node=" << epts[i]
// 	      << " altitude=" << altitude[i] << std::endl;
//   }
// #endif // DEBUG
  
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    int nup = 0;		// number of nodes of face f above the plane
    int ndn = 0;		// number of nodes below the plane
    int n0 = 0;			// number of nodes in the plane
    for(unsigned int n=0; n<NUM_TET_FACE_EDGES; n++) {
      int node = CSkeletonElement::getFaceArray(f)[n];
      int alt = altitude[node];
      if(alt == 1)
	nup++;
      else if(alt == -1)
	ndn++;
      else
	n0++;
    }
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "findTetPlaneIntersectionPoints: face=" << f
// 	      << " nodes=" << CSkeletonElement::getFaceArray(f)[0]
// 	      << " " << CSkeletonElement::getFaceArray(f)[1]
// 	      << " " << CSkeletonElement::getFaceArray(f)[2]
// 	      << "  nup=" << nup << " ndn=" << ndn << " n0=" << n0
// 	      << std::endl;
//     }
// #endif // DEBUG
    if(nup == 3 || ndn == 3 || n0 == 3|| (n0 == 1 && (nup == 2 || ndn == 2))) {
      excludeFace = f;
      break;
    }
  }
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "findTetPlaneIntersectionPoints: excludeFace=" << excludeFace
// 	    << std::endl;
// #endif // DEBUG
} // end findTetPlaneIntersectionPoints

// TODO: Instead of having separate tetPts, tetCoords, and excludeFace
// args, just use the TetPlaneIntData object.

static void getTetPlaneIntersectionPoints(
		   const PixelPlane &pixplane,
		   const std::vector<Coord3D> &epts,
#ifdef DEBUG
		   bool verbose,
#endif // DEBUG
		   TetPlaneIntersectionCache &cache,
		   std::vector<TetPlaneIntersectionPoint> **tetPts,
		   std::vector<Coord2D> **tetCoords,
		   unsigned int &excludeFace)
{
  // if(verbose) {
  //   oofcerr << "getTetPlaneIntersectionPoints: pixplane=" << pixplane
  // 	    << std::endl;
  //   oofcerr << "getTetPlaneIntersectionPoints: epts=";
  //   std::cerr << epts;
  //   oofcerr << std::endl;
  // }
  // See if the intersection polygon has already been found.
  TetPlaneIntersectionCache::iterator tpi = cache.find(pixplane);
  if(tpi == cache.end()) {
    // Storage for new intersection points
    TetPlaneIntData &data = cache[pixplane] = TetPlaneIntData();
    *tetPts = &data.tetPts;
    *tetCoords = &data.tetCoords;
    data.tetCoords.clear();
    // Compute new intersection points
    findTetPlaneIntersectionPoints(epts, pixplane,
#ifdef DEBUG
				   verbose,
#endif // DEBUG
				   data.tetPts, data.excludeFace);
    excludeFace = data.excludeFace;
    unsigned int nn = data.tetPts.size();
    if(nn >= 3) {
      data.tetCoords.reserve(nn);
      for(unsigned int i=0; i<nn; i++)
	data.tetCoords.push_back(data.tetPts[i].location2D(pixplane));
      // Order the intersections so that they form a convex polygon with
      // positive area.
      std::vector<unsigned int> reordering;
      polygonize(data.tetCoords, reordering);
      reorderVector(data.tetPts, reordering);
    }
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "getTetPlaneIntersectionPoints: computed new points: ";
//       std::cerr << data.tetPts;
//       oofcerr << std::endl;
//       oofcerr << "getTetPlaneIntersectionPoints:                      ";
//       std::cerr << data.tetCoords;
//       oofcerr << std::endl;
//     }
// #endif // DEBUG
  }
  else {
    // Retrieve previously computed intersection points.
    *tetPts = &(*tpi).second.tetPts;
    *tetCoords = &(*tpi).second.tetCoords;
    excludeFace = (*tpi).second.excludeFace;
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "getTetPlaneIntersectionPoints: reusing old points: ";
//       std::cerr << (*tpi).second.tetPts;
//       oofcerr << std::endl;
//       oofcerr << "getTetPlaneIntersectionPoints:                     ";
//       std::cerr << (*tpi).second.tetCoords;
//       oofcerr << std::endl;
//     }
// #endif // DEBUG
  }
} // end getTetPlaneIntersectionPoints
									     
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool TetPlaneIntersectionPoint::operator<(const TetPlaneIntersectionPoint &xy)
  const
{
  return (edge_ < xy.edge() || (edge_ == xy.edge() && t() < xy.t()));
}

int TetPlaneIntersectionPoint::node0() const {
  return vtkTetra::GetEdgeArray(edge_)[0];
}

int TetPlaneIntersectionPoint::node1() const {
  return vtkTetra::GetEdgeArray(edge_)[1];
}

Coord2D TetPlaneIntersectionPoint::location2D(const PixelPlane &pixplane) const
{
  if(pixplane.normalSign() == 1)
    return location;
  return Coord2D(location[1], location[0]);
}

Coord3D TetPlaneIntersectionPoint::location3D(const PixelPlane &pixplane) const
{
  return pixplane.convert2Coord3D(location2D(pixplane));
}

std::ostream &operator<<(std::ostream &os, const TetPlaneIntersectionPoint &t)
{
  return os << "TetPlaneIntersectionPoint(("
	    << t.location[0] << ", " << t.location[1]
	    << "), t=" << t.t() << ", e=" << t.edge() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FacetCorner::FacetCorner(const BarycentricCoord &b, FacetCornerList &allCorners)
  : bcoord_(b)
{
  // oofcerr << "FacetCorner::ctor: " << b << std::endl;
  allCorners.push_back(this);
}

FacetCorner::~FacetCorner() {
}

// FacetCorner *FaceFacetCorner::clone(const Coord3D &loc,
// 				    FacetCornerList &allCorners)
//   const
// {
//   return new FaceFacetCorner(loc, bcoord_, pixelplane, allCorners);
// }

void FaceFacetCorner::print(std::ostream &os) const {
  os << "FaceFacetCorner(" << position3D() << ")";
}

// FacetCorner *EdgeFacetCorner::clone(const Coord3D &loc,
// 				    FacetCornerList &allCorners)
//   const
// {
//   return new EdgeFacetCorner(loc, tpip, pixelplane, allCorners);
// }

void EdgeFacetCorner::print(std::ostream &os) const {
  os << "EdgeFacetCorner(" << position3D()
     // << ", edge=" << edge() << ", t=" << edgePosition()
     << ")";
}

Coord3D PixelFacetCorner::position3D() const {
  return pixelplane.convert2Coord3D(location).coord();
}

std::ostream &operator<<(std::ostream &os, const FacetCorner &corner) {
  corner.print(os);
  return os;
}

void PixelFacetCorner::print(std::ostream &os) const {
  os << "PixelFacetCorner(" << position3D() << ")";
}

void SimpleFacetCorner::print(std::ostream &os) const {
  os << "SimpleFacetCorner(" << position3D() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// FacetEdge::operator< uses barycentric coords rather than Coord3Ds
// because when a point that's epsilon away from a tet edge is joined
// to that edge in doFindPixelPlaneFacets, the joining segment might
// have length zero.  The barycentric coords of the endpoints will
// differ, but its 3D coords might not. The std::set of FacetEdges
// used by tetintersectionfacefacets needs to distinguish between the
// connecting edges created by different pixel planes, and using the
// barycentric coords here allows that.

bool FacetEdge::operator<(const FacetEdge &other) const {
  if(start->bcoord() < other.start->bcoord())
    return true;
  if(other.start->bcoord() < start->bcoord())
    return false;
  return end->bcoord() < other.end->bcoord();
  // if(start->position3D() < other.start->position3D())
  //   return true;
  // if(other.start->position3D() < start->position3D())
  //   return false;
  // return end->position3D() < other.end->position3D();
}

bool FacetEdge::nearlyEqual(const FacetEdge &other) const {
  return (norm2(start->position3D() - other.start->position3D()) < 1.e-10 &&
	  norm2(end->position3D() - other.end->position3D()) < 1.e-10);
}

double FacetEdge::length2() const {
  return norm2(start->position3D() - end->position3D());
}

std::ostream &operator<<(std::ostream &os, const FacetEdge &edge) {
  return os << "[" << *edge.start << ", " << *edge.end << ", "
	    << edge.start->bcoord() << ", " << edge.end->bcoord()
#ifdef DEBUG
	    << ", '" << edge.note << "'"
#endif // DEBUG
	    << ", length=" << sqrt(edge.length2()) << "]";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void cleanUpFacetMap(FacetMap2D &facets, FacetCornerList &corners) {
  for(FacetMap2D::iterator fm=facets.begin(); fm!=facets.end(); ++fm) {
    delete (*fm).second;
  }
  for(FacetCornerList::iterator c=corners.begin(); c!=corners.end(); ++c) {
    delete *c;
  }
  corners.clear();
}

void cleanUpFacetMaps(std::vector<FacetMap2D> &planeFacets,
		      FacetCornerList &corners)
{
  for(unsigned int cat=0; cat<planeFacets.size(); cat++) {
    cleanUpFacetMap(planeFacets[cat], corners);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void PixelPlaneFacet::addEdge(const FacetCorner *c0, const FacetCorner *c1
#ifdef DEBUG
			      , const std::string &note, bool verbose
#endif // DEBUG
			      )
{
  areaComputed_ = false;
  edges.insert(FacetEdge(c0, c1
#ifdef DEBUG
			    , note
#endif // DEBUG
			    ));
#ifdef DEBUG
  if(verbose)
    oofcerr << "PixelPlaneFacet::addEdge: " << *c0 << " " << *c1
	    << " " << c0->bcoord() << " " << c1->bcoord()
  	    << " '" << note << "'" << std::endl;
#endif // DEBUG
}

void PixelPlaneFacet::removeEdgesAtPoint(const ICoord3D &pt,
					 const Coord3D &ptA,
					 const Coord3D &ptB
#ifdef DEBUG
					 , bool verbose
#endif // DEBUG
					 )
{
  // Delete edges (pt, ptA) and (pt, ptB) if they exist.
  std::vector<std::set<FacetEdge>::iterator> doomed;
  doomed.reserve(edges.size());
  for(std::set<FacetEdge>::iterator e=edges.begin(); e!=edges.end(); ++e) {
    if((*e).start->position3D() == pt) {
      const Coord3D &other = (*e).end->position3D();
      if(other == ptA || other == ptB)
	doomed.push_back(e);
    }
    else if((*e).end->position3D() == pt) {
      const Coord3D &other = (*e).start->position3D();
      if(other == ptA || other == ptB)
	doomed.push_back(e);
    }
  }
  for(auto &d : doomed)
    edges.erase(d);
}

void PixelPlaneFacet::removeEdge(const Coord3D &ptA, const Coord3D &ptB) {
  for(std::set<FacetEdge>::iterator e=edges.begin(); e!=edges.end(); ++e) {
    Coord3D e0 = (*e).start->position3D();
    Coord3D e1 = (*e).end->position3D();
    if((e0 == ptA && e1 == ptB) || (e1 == ptA && e0 == ptB)) {
      edges.erase(e);
      return;
    }
  }
}

// TODO: Remove verbose arg from area() and getArea()
double PixelPlaneFacet::area(bool verbose) const {
  if(areaComputed_) {
    if(verbose)
      oofcerr << "PixelPlaneFacet::area: precomputed " << area_ << std::endl;
    return area_;
  }
  if(edges.empty())
    area_ = 0.0;
  else
    area_= getArea(verbose);
  areaComputed_ = true;
  return area_;
};

typedef std::pair<Coord2D, Coord2D> Coord2DPair;

double PixelPlaneFacet::getArea(bool verbose) const {
  std::vector<Coord2DPair> endpts;
  endpts.reserve(edges.size());
  Coord2D center(0.0, 0.0);
  for(std::set<FacetEdge>::const_iterator edge=edges.begin();
      edge!=edges.end(); ++edge)
    {
      Coord2D s =
	dynamic_cast<const PixelPlaneFacetCorner*>((*edge).start)->position2D();
      Coord2D e =
	dynamic_cast<const PixelPlaneFacetCorner*>((*edge).end)->position2D();
      endpts.push_back(Coord2DPair(s,e));
      center += s + e;
      if(verbose)
	oofcerr << "PixelPlaneFacet::getArea: " << *edge << std::endl;
    }
  center /= 2.0*edges.size();
  if(verbose)
    oofcerr << "PixelPlaneFacet::getArea: center=" << center << std::endl;
  
  double a = 0;
  for(std::vector<Coord2DPair>::const_iterator seg=endpts.begin();
      seg!=endpts.end(); ++seg)
    {
      // TODO: subtracting center may not be necessary.  It's slower,
      // but it might improve numerical stability.  Without it, the
      // cross products can involve differences of large numbers.
      a += ((*seg).first - center) % ((*seg).second - center);
    }
  return 0.5*a;
}

Coord3D PixelPlaneFacet::areaVector() const {
  assert(!edges.empty());
  Coord3D a;
  Coord3D c = center();
  for(std::set<FacetEdge>::const_iterator e=edges.begin(); e!=edges.end(); ++e)
    {
      a += ((*e).start->position3D()-c) % ((*e).end->position3D()-c);
    }
  return 0.5*a;
}

Coord3D PixelPlaneFacet::center() const {
  assert(!edges.empty());
  Coord3D c;
  for(std::set<FacetEdge>::const_iterator e=edges.begin(); e!=edges.end(); ++e)
    {
      c += (*e).start->position3D() + (*e).end->position3D();
    }
  return c/(2.*edges.size());
}

std::ostream &operator<<(std::ostream &os, const PixelPlaneFacet &ppf) {
  os << "PixelPlaneFacet(";
  bool first = true;
  for(std::set<FacetEdge>::const_iterator e=ppf.begin(); e!=ppf.end(); ++e) {
    if(!first)
      os << ", ";
    first = false;
    os << *e;
  }
  os << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef CLEANUP

// Support for PixelPlaneFacet::cleanUp().

typedef std::map<const Coord3D, const FacetCorner*> CornerMap;
typedef std::multimap<Coord3D, FacetEdge> FacetEdgeMap;
typedef std::pair<Coord3D, FacetEdge> FacetEdgeMapDatum;

const FacetCorner *findReplacement(const FacetCorner *corner,
				   const CornerMap &cornerMap)
{
  CornerMap::const_iterator which = cornerMap.find(corner->position3D());
  if(which == cornerMap.end())
    return corner;
  return (*which).second;
}

// Predicate class for std::find_if.

class PointNearlyEqual {
private:
  const Coord3D ptA;
public:
  PointNearlyEqual(const Coord3D ptA) : ptA(ptA) {}
  bool operator()(const FacetEdgeMapDatum &femd) const {
    return nearby(ptA, femd.first);
  }
};

// Do two consecutive edges make a hairpin turn?

static bool isHairPin(const FacetEdge &edge0, const FacetEdge &edge1) {
  // Does this segment go in exactly the opposite direction as the
  // next one?  This can only happen if the segments are lined up
  // on pixel boundaries, so roundoff shouldn't be a problem.
  Coord3D ptA = edge0.start->position3D();
  Coord3D ptB = edge0.end->position3D();
  Coord3D ptC = edge1.end->position3D();
  Coord3D segAB = ptB - ptA;
  Coord3D segBC = ptC - ptB;
  double d = dot(segAB, segBC);
  return d < 0 && norm2(cross(segAB, segBC)) <= POINTTOL2*(-d);
}

    
// PixelPlaneFacet::cleanUp is called at the end of
// findPixelPlaneFacets.  It removes edges with squared length less
// than POINTTOL2, and hairpin turns.

// TODO: cleanUp needs to be a HomogeneityTet method, so that it has
// access to epts and barycentric coords.  For now, epts and baryCache
// are passed in as arguments.

void PixelPlaneFacet::cleanUp(const PixelPlane &pixplane,
			      FacetCornerList &allCorners,
			      const std::vector<Coord3D> &epts,
			      BaryCoordCache &baryCache
#ifdef DEBUG
			      , bool verbose
#endif // DEBUG
			      )
{
  // Get rid of short edges, with lengths much less than a voxel size
  // (as determined by POINTTOL2, which is the cutoff length,
  // squared).  These edges often result from roundoff errors, and
  // even if they don't, removing them has little effect on the end
  // result.  Leaving them in can confuse later topological
  // operations.

  if(empty())
    return;

#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::cleanUp: original edges=" << std::endl;
    OOFcerrIndent indent(2);
    for(std::vector<FacetEdge>::const_iterator e=edges.begin();
	e!=edges.end(); ++e)
      {
	oofcerr << *e << std::endl;
      }
  }
#endif  // DEBUG

  CornerMap cornerMap;
  std::set<FacetEdge> goodEdges; // edges that aren't short
  for(std::vector<FacetEdge>::iterator edge=edges.begin(); edge!=edges.end();
      ++edge)
    {
      double length2 = (*edge).length2();
      if(length2 <= POINTTOL2) {
	// Two points that are close together get replaced with a
	// single point.  The replacement position is chosen so that
	// any barycentric coord component of either point that's zero
	// in the original remains zero in the replacement.  This
	// preserves topological information. (Points on edges stay on
	// edges, etc.)

	// TODO: What if there are two consecutive short edges?  Do we
	// need to check that neither endpoint is already in cornerMap
	// before creating a new one?  Can this even happen?
	
	BarycentricCoord bnew = mergeBary((*edge).start->bcoord(),
					  (*edge).end->bcoord());
	Coord3D newPos = bnew.position3D(epts);
	const FaceFacetCorner *newCorner = new FaceFacetCorner(
					   newPos, bnew, pixplane, allCorners);
	cornerMap[(*edge).start->position3D()] = newCorner;
	cornerMap[(*edge).end->position3D()] = newCorner;

// 	// TODO: Using dynamic_cast here is ugly.  Would using virtual
// 	// functions be slow?
// 	const PixelFacetCorner *pc0 =
// 	  dynamic_cast<const PixelFacetCorner*>((*edge).start);
// 	const PixelFacetCorner *pc1 =
// 	  dynamic_cast<const PixelFacetCorner*>((*edge).end);
// 	if(pc0 && !pc1) {
// 	  // start is a PixelFacetCorner but end isn't.
// 	  Coord3D pos0 = pc0->position3D();
// 	  Coord3D pos1 = (*edge).end->position3D();
// 	  CornerMap::iterator which = cornerMap.find(pos0);
// 	  const FacetCorner *newCorner =
// 	    (which == cornerMap.end() ?
// 	     (*edge).end->clone(pos0, allCorners) : (*which).second);
// 	  cornerMap[pos0] = newCorner;
// 	  cornerMap[pos1] = newCorner;
// // #ifdef DEBUG
// // 	  if(verbose) {
// // 	    oofcerr << "PixelPlaneFacet::cleanUp: removing edge "
// // 		    << pos0 << " " << pos1
// // 		    << " newCorner=" << newCorner->position3D()
// // 		    << std::endl;
// // 	  }
// // #endif // DEBUG
// 	}
// 	else if(pc1 && !pc0) {
// 	  Coord3D pos0 = (*edge).start->position3D();
// 	  Coord3D pos1 = pc1->position3D();
// 	  CornerMap::iterator which = cornerMap.find(pos1);
// 	  const FacetCorner *newCorner =
// 	    (which == cornerMap.end() ?
// 	     (*edge).start->clone(pos1, allCorners) : (*which).second);
// 	  cornerMap[pos0] = newCorner;
// 	  cornerMap[pos1] = newCorner;
// // #ifdef DEBUG
// // 	  if(verbose) {
// // 	    oofcerr << "PixelPlaneFacet::cleanUp: removing edge "
// // 		    << pos0 << " " << pos1
// // 		    << " newCorner=" << newCorner->position3D()
// // 		    << std::endl;
// // 	  }
// // #endif // DEBUG
// 	}
// 	if(!(pc0 || pc1)) {
// 	  // Neither corner is a PixelFacetCorner.  
// 	  if(length2 > 0) {	// TODO: Always true.  Is this test vestigial?
// 	    cornerMap[(*edge).start->position3D()] = (*edge).end;
// // #ifdef DEBUG
// // 	    if(verbose) {
// // 	      oofcerr << "PixelPlaneFacet::cleanUp: removing edge by moving "
// // 		      << (*edge).start->position3D() << " to "
// // 		      << (*edge).end->position3D()
// // 		      << std::endl;
// // 		}
// // #endif // DEBUG
// 	  }
// 	  // goodEdges.insert(*edge);
// 	}
      }	// end if length is small
      else {
	// edge isn't too short
	goodEdges.insert(*edge);
      }
    } // end loop over edges

  // If there aren't enough good edges, then the facet is degenerate
  // and can be ignored.  It probably arose from a corner of a voxel
  // that lies within roundoff of a tet face or edge.
  if(goodEdges.size() < 3) {
    edges.clear();
    area_ = 0;
    areaComputed_ = true;
#ifdef DEBUG
    if(verbose)
      oofcerr << "PixelPlaneFacet::cleanUp: facet is degenerate." << std::endl;
#endif // DEBUG
    return;
  }
  
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::cleanUp: goodEdges=" << std::endl;
    for(std::set<FacetEdge>::const_iterator g=goodEdges.begin(); g!=goodEdges.end(); ++g)
      {
	OOFcerrIndent indent(2);
	oofcerr << *g << std::endl;
      }
    oofcerr << "PixelPlaneFacet::cleanUp: cornerMap=" << std::endl;
    int prec = std::cerr.precision();
    std::cerr << std::setprecision(20);
    for(CornerMap::const_iterator i=cornerMap.begin(); i!=cornerMap.end(); ++i)
      {
	OOFcerrIndent indent(2);
	oofcerr << " " << (*i).first << "-->" << *(*i).second << " "
		<< (*i).second->bcoord() << std::endl;
      }
    std::cerr << std::setprecision(prec);
  }
#endif // DEBUG
  
  // Now use cornerMap to replace the endpoints in the good edges.
  // std::set<FacetEdge> cleanedEdges;
  edges.clear();
  for(std::set<FacetEdge>::const_iterator edge=goodEdges.begin();
      edge!=goodEdges.end(); ++edge)
    {
      // Because findReplacement will return the same corner for
      // different inputs, after this there will be edges that will
      // share corner objects.  That's ok.
      const FacetCorner *newp0 = findReplacement((*edge).start, cornerMap);
      const FacetCorner *newp1 = findReplacement((*edge).end, cornerMap);
      bool replaced = newp0 != (*edge).start || newp1 != (*edge).end;
      edges.push_back(FacetEdge(newp0, newp1
#ifdef DEBUG
				, (replaced? "replacement " : " ")
				+ (*edge).note
#endif // DEBUG
		      ));
    }

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::cleanUp: cleanedEdges=" << std::endl;
//     OOFcerrIndent indent(2);
//     for(std::vector<FacetEdge>::const_iterator edge=edges.begin();
// 	edge!=edges.end(); ++edge)
//       oofcerr << *edge << std::endl;
//   }
// #endif // DEBUG

  // Get rid of hairpin turns, where the facet boundary doubles back
  // on itself.  These can occur when a pixel set boundary takes a jog
  // along a polygon edge.  That is, when a pixel boundary approaches
  // an edge at point A, turns right to pointB (on the same edge), and
  // turns left to exit the polygon at point B' (nearly at the same
  // point as B).  A and B are inside the polygon, but B' is outside.
  // The boundary will then go along the polygon edge, past A, to C.
  // The part from A to B to B' and back to A is redundant and needs
  // to be removed.

  // By the time we get to this point, B and B' will have been merged
  // already.
  /*
                               |pixel set bdy
                               |
                               |
   C-------------------<-------B'              polygon exterior
   =========================================== polygon bdy
               A------->-------B               polygon interior
    interior   |
    of pixel   ^   exterior
    set        |   of pixel set
               |
   */

  // First, find out how the edges are connected to one another by
  // ordering the list.  They may form more than one loop, so keep
  // track of the sizes of each loop.

  // TODO: This information could possibly be gathered when the edges
  // are originally found, which would save time.
  FacetEdgeMap startPts;
  for(std::vector<FacetEdge>::iterator e=edges.begin(); e!=edges.end(); ++e) {
    startPts.insert(FacetEdgeMapDatum((*e).start->position3D(), *e));
  }
  
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::cleanUp: looking for hairpins" << std::endl;
//     // oofcerr << "PixelPlaneFacet::cleanUp: startPts=" << std::endl;
//     // OOFcerrIndent indent(2);
//     // for(FacetEdgeMap::const_iterator d=startPts.begin(); d!=startPts.end();
//     // 	++d)
//     //   oofcerr << (*d).first << ": " << (*d).second << std::endl;
//   }
// #endif // DEBUG

  // Find loops
  std::vector<unsigned int> loopSizes;
  std::vector<unsigned int> loopStarts;
  unsigned int sizeSum = 0;
  std::vector<FacetEdge> tempEdges;
  tempEdges.reserve(edges.size());
  edges.clear();
  while(!startPts.empty()) {
    // Find a starting point.
    OOFcerrIndent indent(2);
    FacetEdgeMap::iterator edgeIter = startPts.begin();
    FacetEdge startEdge = (*edgeIter).second;
    startPts.erase(edgeIter);
    tempEdges.push_back(startEdge);
    Coord3D startPt = startEdge.start->position3D();
    Coord3D currentPt = startEdge.end->position3D();
    int nedges = 1;
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "PixelPlaneFacet::cleanUp: startPt=" << startPt << std::endl;
//       oofcerr << "PixelPlaneFacet::cleanUp: added edge " << tempEdges.back()
// 	      << std::endl;
//       oofcerr << "PixelPlaneFacet::cleanUp: currentPt=" << currentPt
// 	      << std::endl;
//     }
// #endif // DEBUG
    while(!nearby(currentPt, startPt)) {
// #ifdef DEBUG
//       OOFcerrIndent indent(2);
//       if(verbose)
//       	oofcerr << "PixelPlaneFacet::cleanUp: looking for " << currentPt
//       		<< std::endl;
// #endif // DEBUG

      // TODO: Do we still need to use PointNearlyEqual here?
      // edgeIter = startPts.find(currentPt);
      edgeIter = std::find_if(startPts.begin(), startPts.end(),
			      PointNearlyEqual(currentPt));
      
// #ifdef DEBUG
//       if(verbose && edgeIter == startPts.end()) {
// 	oofcerr << "PixelPlaneFacet::cleanUp: Can't find " << currentPt
// 		<< "!" << std::endl;
// 	OOFcerrIndent indent(2);
// 	for(FacetEdgeMap::const_iterator e=startPts.begin(); e!=startPts.end();
// 	    ++e)
// 	  oofcerr << "PixelPlaneFacet::cleanUp: " << (*e).first << " = "
// 		  << currentPt << " + " << (*e).first - currentPt << std::endl;
	      
//       }
// #endif // DEBUG
      assert(edgeIter != startPts.end());
      tempEdges.push_back((*edgeIter).second);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "PixelPlaneFacet::cleanUp: added edge " << tempEdges.back()
//       		<< std::endl;
// #endif // DEBUG
      currentPt = (*edgeIter).second.end->position3D();
      startPts.erase(edgeIter);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "PixelPlaneFacet::cleanUp: currentPt=" << currentPt
//       		<< std::endl;
// #endif // DEBUG
      ++nedges;
    } // end while not nearby (ie, we're now back where we started)
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::cleanUp: finished a loop of size " << nedges
//     	      << " startPts.size= " << startPts.size() << std::endl;
// #endif // DEBUG
    loopSizes.push_back(nedges);
    loopStarts.push_back(sizeSum);
    sizeSum += nedges;
  }		       // end while startPts is not empty

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::cleanUp: edges sorted into loops:"
// 	    << std::endl;
//     {
//       OOFcerrIndent indent(2);
//       for(unsigned int k=0; k<tempEdges.size(); k++)
// 	oofcerr << "PixelPlaneFacet::cleanUp: " << tempEdges[k] << std::endl;
//     }
//     oofcerr << "PixelPlaneFacet::cleanUp: loopSizes=";
//     std::cerr << loopSizes;
//     oofcerr << std::endl;
//   }
// #endif // DEBUG

  // Look for hairpins
  for(unsigned int loop=0; loop<loopSizes.size(); loop++) {
    // firstSeg is the position in tempEdges of the start of current loop
    unsigned int firstSeg = loopStarts[loop];
    unsigned int loopSize = loopSizes[loop]; // size before removing hairpins
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "PixelPlaneFacet::cleanUp: examining loop " << loop
//     	      << " for hairpin turns" << std::endl;
//       for(unsigned int l=firstSeg; l<firstSeg+loopSize; l++) {
// 	OOFcerrIndent indent(2);
// 	oofcerr << "PixelPlaneFacet::cleanUp: " << tempEdges[l] << std::endl;
//       }
//     }
//     OOFcerrIndent indent(2);
// #endif // DEBUG
    if(loopSize <= 2) {
      if(verbose)
	oofcerr << "PixelPlaneFacet::cleanUp: skipping short loop" << std::endl;
      continue;
    }
    unsigned int loopStart = edges.size(); // start position in final edge list
    unsigned int lastSeg = firstSeg + loopSize;
    bool started = false; // Are we processing a sequence of hairpins?
    unsigned int hairpinStart = 0; // Where the sequence started.
    for(unsigned int thisSeg=firstSeg; thisSeg<lastSeg; thisSeg++) {
      unsigned int nextSeg = thisSeg + 1;
      if(nextSeg == lastSeg)
	nextSeg = firstSeg;
      if(!started) {
	if(!isHairPin(tempEdges[thisSeg], tempEdges[nextSeg])) {
	  edges.push_back(tempEdges[thisSeg]);
	}
	else {
	  // Start of a new sequence of hairpin turns.
	  started = true;
	  hairpinStart = thisSeg;
	}
      }
      else {
	// We're in the middle of processing a sequence of hairpin
	// turns.  Unless the sequence ends here, there's nothing to
	// do.
	if(!isHairPin(tempEdges[thisSeg], tempEdges[nextSeg])) {
	  started = false;
	  addEdge(tempEdges[hairpinStart].start, tempEdges[thisSeg].end,
#ifdef DEBUG
		  "hairpin shortcut",
#endif // DEBUG
		  verbose);
	}
      }
    } // end loop over thisSeg
    // If we finished examining segments while in the middle of a
    // hairpin sequence, the final hairpins connect to the first
    // segment.
    if(started) {
      edges[loopStart] = FacetEdge(tempEdges[hairpinStart].start,
				   edges[loopStart].end
#ifdef DEBUG
				   , "wraparound hairpin shortcut"
#endif // DEBUG
				   );
    }

#ifdef DEBUG
    if(verbose) {
      oofcerr << "PixelPlaneFacet::cleanUp: after hairpin removal:"
	       << std::endl;
      for(unsigned int l=loopStart; l<edges.size(); l++) {
	OOFcerrIndent indent(2);
	oofcerr << "PixelPlaneFacet::cleanUp: " << edges[l] << std::endl;
      }
    }
#endif	// DEBUG
  } // end loop over loops
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::cleanUp: done" << std::endl;
// #endif // DEBUG
} // PixelPlaneFacet::cleanUp

#endif // CLEANUP


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void polygonize(std::vector<Coord2D> &ipts, std::vector<unsigned int> &order) {
  // Given a list of 3 or 4 points in a plane, reorder the points so
  // that they form a polygon with positive area.  This is always
  // possible and has a unique solution (up to trivial renumbering)
  // because the points came from the intersection of a tet with a
  // plane. This code is the C++ version of the polygonize() routine
  // in primitives.py.
  assert(ipts.size() == 3 || ipts.size() == 4);

  order.resize(ipts.size());
  for(unsigned int i=0; i<ipts.size(); i++)
    order[i] = i;

  Coord2D center;
  for(int i=0; i<ipts.size(); i++)
    center += ipts[i];
  center /= ipts.size();
  if(ipts.size() == 3) {
    // Three points in a triangle are oriented correctly if
    // their area, computed by cross products, is positive.
    double area = 0;
    for(int i=0; i<3; i++) {
      area += cross(ipts[i] - center, ipts[(i+1)%3] - center);
    }
    if(area < 0) {
      Coord2D temp = ipts[2];
      ipts[2] = ipts[1];
      ipts[1] = temp;
      order[2] = 1;
      order[1] = 2;
    }
    return;
  }
  else if(ipts.size() == 4) {
    static unsigned int ordering[6][4] = {
      {0,1,2,3}, {0,1,3,2}, {0,2,1,3}, {0,2,3,1}, {0,3,1,2}, {0,3,2,1}};
    std::set<unsigned int> positiveOrderings;
    for(unsigned int ord=0; ord<6; ord++) {
      double area = 0;
      for(unsigned int i=0; i<4; i++) {
	area += cross(ipts[ordering[ord][i]] - center,
		      ipts[ordering[ord][(i+1)%4]] - center);
      }
      if(area > 0)
	positiveOrderings.insert(ord);
    }
    assert(!positiveOrderings.empty());
    if(positiveOrderings.size() == 1) {
      unsigned int ord = *positiveOrderings.begin();
      if(ord != 0) {// skip the trivial case
	reorderVector(ipts, ordering[ord]);
	// compute the ordering that can be applied to other vectors
	reorderVector(order, ordering[ord]);
      }
      return;
    }
    else {
      // There's more than one ordering with positive area.  Check
      // that opposite edges don't cross.  Because the legal polygon
      // must be convex, it's sufficient to check that the end points
      // of one edge are both on the same side of the linear extension
      // of the other edge.
      for(std::set<unsigned int>::const_iterator o=positiveOrderings.begin();
	  o!=positiveOrderings.end(); ++o)
	{
	  unsigned int *ord = ordering[*o];
	  bool edgesCross = false;
	  // Loop over the pairs of opposite edges
	  for(unsigned int i=0; i<2 && !edgesCross; i++) {
	    Coord2D pt0 = ipts[ord[i]];
	    Coord2D seg0 = ipts[ord[i+1]] - pt0;
	    Coord2D ptA = ipts[ord[i+2]] - pt0;
	    Coord2D ptB = ipts[ord[(i+3)%4]] - pt0;
	    double crossA = cross(seg0, ptA);
	    double crossB = cross(seg0, ptB);
	    if(crossA*crossB < 0)
	      edgesCross = true;
	  }
	  if(!edgesCross) {
	    reorderVector(ipts, ord);
	    reorderVector(order, ord);
	    return;
	  }
	} // end loop over positiveOrderings
    }	// end else if positiveOrderings.size() > 1
  }	// end if ipts.size() == 4
  throw ErrProgrammingError("Failed to find a well formed polygon.",
			    __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given a polygon of TetPlaneIntersectionPoints, find which of its
// segments is on the tet face opposite node oppNode.

unsigned int getPolygonSegmentOnFace(
			   unsigned int oppNode,
			   const std::vector<TetPlaneIntersectionPoint> &pts)
{
  // Two barycentric coords are on the same face if they share a
  // zero.  In this case, we know that the zero is in position
  // oppNode.
  for(unsigned int i=0; i<pts.size(); i++) {
    if(pts[i].bcoord()[oppNode] == 0.0 &&
       pts[(i+1)%pts.size()].bcoord()[oppNode] == 0.0)
      return i;
  }
#ifdef DEBUG
  oofcerr << "getPolygonSegmentOnFace: failed to find a segment opposite node "
	  << oppNode << std::endl;
  oofcerr << "getPolygonSegmentOnFace: polygon points are:";
  for(std::vector<TetPlaneIntersectionPoint>::const_iterator p=pts.begin();
      p!=pts.end(); ++p)
    oofcerr << " " << (*p).bcoord();
  oofcerr << std::endl;
#endif // DEBUG
  throw ErrProgrammingError("getPolygonSegmentOnFace failed!",
			    __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// FaceIntersection packages the information returned by
// find_face_intersection, which computes the intersection of a
// segment (pt0, pt1) with a given face of a tetrahedron.

class FaceIntersection {
public:
  unsigned int oppNode;	   // index of node opposite intersected face
  Coord3D position;
  BarycentricCoord intersect;
  // alpha is the fractional distance along the segment (pt0, pt1)
  // at the intersection point.
  double alpha;
  // Error is how far outside the face the intersection is.
  double error;
  // Entry is true if the segment is entering the tet.
  bool entry;
};

std::ostream &operator<<(std::ostream &os, const FaceIntersection &fi) {
  return os << "FaceIntersection(" << fi.position << ", " << fi.intersect
	    << ", oppNode=" << fi.oppNode << " alpha=" << fi.alpha
	    << ", error=" << fi.error
	    << ", " << (fi.entry? "entry" : "exit") << ")";
}

// Given the barycentric coords of two points relative to a
// tetrahedron, find the point where the segment joining them
// intersects the given face of the tetrahedron.  (The face is
// specified by giving the index of the opposite node.)

static FaceIntersection *do_find_face_intersection(
		   const ICoord3D &pt0, const ICoord3D &pt1,
		   const BarycentricCoord &b0, const BarycentricCoord &b1,
		   const std::vector<Coord3D> &epts,
		   const ICRectangularPrism &iBounds,
		   unsigned int oppNode
#ifdef DEBUG
		   , bool verbose,
		   const std::vector<const PixelPlane*> &facePlanes,
		   BaryCoordCache &baryCache
#endif // DEBUG
						   )
{
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "do_find_face_intersection: pt0=" << pt0 << " b0=" << b0
// 	    << std::endl
// 	    << "                         : pt1=" << pt1 << " b1=" << b1
// 	    << "    " << "oppNode=" << oppNode << std::endl;
//   }
//   OOFcerrIndent indent(2);
// #endif // DEBUG

  // All points on the face have b[oppNode]==0, so if the segment
  // intersects the face, b[oppNode] at the two endpoints of the
  // segments must have opposite signs.  If just one is zero, we
  // should continue, but if both are zero we shouldn't.
  if(b0[oppNode]*b1[oppNode] > 0.0 || b0[oppNode] == b1[oppNode]) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "do_find_face_intersection: no intersection" << std::endl;
// #endif // DEBUG
    return NULL;
  }

  // Find the direction c of the segment
  unsigned int c = NONE;
  for(unsigned int i=0; i<3; i++) {
    if(pt0[i] != pt1[i]) {
      c = i;
      break;
    }
  }
  assert(c != NONE);

  // The barycentric coordinates of the actual intersection point are
  // computed by first projecting the endpoints of the segment onto
  // the bounding box of the element.  This ensures that all colinear
  // segments intersect the face at exactly the same point, with
  // identical round off errors.
  ICoord3D bpt0 = pt0;
  ICoord3D bpt1 = pt1;
  if(bpt0[c] > bpt1[c]) {
    bpt0[c] = iBounds.max(c);
    bpt1[c] = iBounds.min(c);
  }
  else {
    bpt1[c] = iBounds.max(c);
    bpt0[c] = iBounds.min(c);
  }
  BarycentricCoord bb0 = getBarycentricCoord(bpt0, epts, facePlanes,
					     baryCache);
  BarycentricCoord bb1 = getBarycentricCoord(bpt1, epts, facePlanes,
					     baryCache);
  double balpha = bb0[oppNode]/(bb0[oppNode] - bb1[oppNode]);
  // Even though b0 and b1 may be on opposite sides of the face, if
  // they're only off by epsilon it's possible that bb0 and bb1 may be
  // both exactly on the face.  In this case, balpha can be NaN, but
  // we can just take it to be 0.5.
  if(isnan(balpha))
    balpha = 0.5;
  // If the segment is parallel to the face, within round-off error,
  // balpha can be nearly 0 or 1.  Since the bounding box extends at
  // least one voxel beyond the element, such intersections are an
  // indication that this face should not have been considered.
  int boxsize = iBounds.max(c) - iBounds.min(c);
  double padding = 0.5/boxsize;
  if(balpha <= padding || balpha >= 1.0-padding) {
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "do_find_face_intersection: rejecting balpha="
// 	      << balpha << " padding=" << padding << std::endl;
//     }
// #endif // DEBUG
    return NULL;
  }
  
  // If we got here, we have a real intersection.
  
  FaceIntersection *fint = new FaceIntersection;
  fint->oppNode = oppNode;
  // alpha is the fractional distance from pt0 to pt1 at the intersection.
  fint->alpha = pinUnitRange(b0[oppNode]/(b0[oppNode] - b1[oppNode])
#ifdef DEBUG
			     , verbose
#endif // DEBUG
			     );
//  #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "do_find_face_intersection: b0[oppNode]=" << b0[oppNode]
// 	    << " b1[oppNode]=" << b1[oppNode]
// 	    << " prod=" << b0[oppNode]*b1[oppNode]
// 	    << " eq=" << (b0[oppNode] == b1[oppNode])
// 	    << " zero=" << (b0[oppNode]==0) << " " << (b1[oppNode]==0)
// 	    << " raw alpha=" << (b0[oppNode]/(b0[oppNode]-b1[oppNode]))
// 	    << std::endl;
//     oofcerr << "do_find_face_intersection: alpha=" << fint->alpha << std::endl;
//   }
// #endif // DEBUG

  // Use the bounding box endpoints and alpha to compute the actual
  // intersection point.
  fint->intersect = averageBary(bb0, bb1, balpha);
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "do_find_face_intersection: c=" << c << std::endl;
//     oofcerr << "do_find_face_intersection: bb0=" << bpt0 << " " << bb0
// 	    << std::endl;
//     oofcerr << "do_find_face_intersection: bb1=" << bpt1 << " " << bb1
// 	    << std::endl;
//     oofcerr << "do_find_face_intersection: balpha=" << balpha << std::endl;
//   }
// #endif // DEBUG


  // Avoid roundoff errors.  We know that the intersection is on the
  // oppNode face of the tet, so that barycentric coord must be zero.
  fint->intersect[oppNode] = 0.0;
  
  // Is the intersection an entry or an exit?  "Entry" means that the
  // segment is entering the tetrahedron, which means that b0 is
  // outside the intersected face, which means that its oppNode
  // component is negative.  If that component is zero, but b1 is on
  // the interior side (ie, has a positive barymetric component), that
  // also counts as an entry.
  fint->entry = b0[oppNode] < 0.0 || (b0[oppNode] == 0.0 && b1[oppNode] > 0.0);

// #ifdef DEBUG
//   const BarycentricCoord boriginal = fint->intersect;
//   const Coord3D poriginal = boriginal.position3D(epts);
//   // bool corrected = false;
// #endif // DEBUG

  
  // If the intersection is on a tet edge, another barycentric
  // component should be zero, but may not be exactly zero due to
  // roundoff.  If the edge and the intersecting segment lie on a
  // pixel plane, it's important to ensure that the intersection is
  // exactly on the plane.
  bool done = false;
  for(unsigned int i=1; i<4 && !done; i++) {
    // ii and jj are the node indices of an edge of the intersected
    // face.  First set ii to a node that's not oppNode.
    unsigned int ii = (oppNode + i) % NUM_TET_NODES;
    // jj is another node that's not ii and is not oppNode.  When the
    // loop is done, all legal ii,jj pairs will have been checked.
    unsigned int jj = ii + 1;
    if(jj == oppNode) {
      jj = (oppNode == 3 ? 0 : oppNode+1);
    }
    else if(jj == 4) {
      jj = oppNode == 0 ? 1 : 0;
    }
    
    // Is this edge in the same plane as segment (pt0, pt1)?  We know
    // that the segment lies in planes in both of the non-c directions.
    for(unsigned int k=1; k<3; k++) { // loop over non-c directions
      unsigned int kk = (c + k) % 3;
      if(epts[ii][kk] == epts[jj][kk] && pt0[kk] == epts[ii][kk]) {
	// The intersection point is on the edge joining nodes ii and
	// jj.  That means that its barycentric coordinate components
	// are zero for the nodes that aren't ii or jj.  One of those
	// nodes is oppNode, and the other is 6-ii-jj-oppNode.
// #ifdef DEBUG
// 	corrected = true;
// 	if(verbose) {
// 	  oofcerr << "do_find_face_intersection: zeroing intersect["
// 		  << 6-ii-jj-oppNode << "]" << std::endl;
// 	}
// #endif // DEBUG
	fint->intersect[6 - ii - jj - oppNode] = 0.0;
// #ifdef DEBUG
// 	if(verbose) {
// 	  oofcerr << "do_find_face_intersection: made edge correction: c="
// 		  << c << " ii=" << ii << " jj=" << jj << " kk=" << kk
// 		  << " intersect=" << fint->intersect << std::endl;
// 	}
// #endif	// DEBUG
	done = true;
	break;
      }
    } // end loop over non-c directions kk
  }   // end loop over nodes ii that aren't oppNode
// #ifdef DEBUG
//   if(verbose && corrected)
//     oofcerr << "do_find_face_intersection: after corrections, intersect="
// 	    << fint->intersect << std::endl;
// #endif // DEBUG

  // Get the 3D position of the intersection, making sure that it is
  // exactly on the line joining pt0 and pt1, since pt0 and pt1 are on
  // a pixel boundary.
  fint->position = fint->intersect.position3D(epts);
  for(unsigned int i=0; i<3; i++)
    if(i != c)
      fint->position[i] = pt0[i];
// #ifdef DEBUG
//   // The distance that the intersection moves because of the
//   // correction should be very small, so checking it here is a
//   // reasonable diagnostic.
  
//   if(norm2(poriginal - fint->position) > 1.e-10) {
//     oofcerr << "do_find_face_intersection: original=" << poriginal
// 	    << " corrected=" << fint->position << std::endl;
//     throw ErrProgrammingError("Intersection correction is too large!",
// 			      __FILE__, __LINE__);
//   }
// #endif // DEBUG

  // See if the intersection is actually within the face, by checking
  // that other barycentric components are between 0 and 1.  It's
  // possible that roundoff error may put a point slightly outside the
  // face, so keep track of largest error.
  fint->error = 0.0;
  for(unsigned int j=0; j<4; j++) {
    if(j != oppNode) {
      double baryj = fint->intersect[j];
      if(baryj < 0.0) {
	if(-baryj > fint->error)
	  fint->error = -baryj;
      }
      // We don't really need to check for baryj > 1.  If any
      // component is greater than 1, some other component must be
      // less than zero.  But we'll get a different value of the error
      // if we skip the >1 test.
      else if(baryj > 1.0) {
	if(baryj - 1.0 > fint->error)
	  fint->error = baryj - 1.0;
      }
    }
  } // end loop over j
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "do_find_face_intersection: final intersect=" << fint->intersect
// 	    << " " << fint->position
      
// 	    << " alpha=" << fint->alpha << " entry=" << fint->entry
// 	    << " error=" << fint->error << std::endl;
// #endif // DEBUG
  return fint;
}

// find_face_intersection just calls do_find_face_intersection, after
// ensuring that the coords b0 and b1 are in the same canonical order,
// to ensure that the intersection point is the same even if the
// intersecting segment goes in the other direction.

static FaceIntersection *find_face_intersection(
		const ICoord3D &pt0, const ICoord3D &pt1,
		const BarycentricCoord &b0, const BarycentricCoord &b1,
		const std::vector<Coord3D> &epts,
		const ICRectangularPrism &iBounds,
		unsigned int oppNode
#ifdef DEBUG
		, bool verbose,
		const std::vector<const PixelPlane*> &facePlanes,
		BaryCoordCache &baryCache
#endif // DEBUG
						)
{
  if(b0 < b1)
    return do_find_face_intersection(pt0, pt1, b0, b1, epts, iBounds, oppNode
#ifdef DEBUG
				     , verbose, facePlanes, baryCache
#endif // DEBUG
				     );
  FaceIntersection *result = do_find_face_intersection(pt1, pt0, b1, b0,
						       epts, iBounds, oppNode
#ifdef DEBUG
						       , verbose,
						       facePlanes, baryCache
#endif // DEBUG
						       );
  if(result) {
    result->alpha = 1.-result->alpha;
    result->entry = !result->entry;
  }
  return result;
}
				   

static PixelBdyIntersection *find_one_intersection(
			   const PixelBdyLoop &loop,
			   unsigned int loopseg,
			   const PixelPlane &pixplane,
			   unsigned int onFace,
			   const std::vector<Coord3D> &epts,
			   const ICRectangularPrism &iBounds,
			   const std::vector<const PixelPlane*> &facePlanes,
			   const std::vector<TetPlaneIntersectionPoint> &pts,
			   unsigned int excludeFace,
			   bool entry,
#ifdef DEBUG
			   bool verbose,
#endif // DEBUG
			   BaryCoordCache &baryCache)
{
  const ICoord2D &pt0 = loop.icoord(loopseg);
  const ICoord2D &pt1 = loop.next_icoord(loopseg);
  BarycentricCoord b0 = getBarycentricCoord(pt0, pixplane, epts, facePlanes,
					    baryCache);
  BarycentricCoord b1 = getBarycentricCoord(pt1, pixplane, epts, facePlanes,
					    baryCache);
  if(onFace != NONE) {
    // Correct for round off error.
    
    // TODO: This calculation should be done by the HomogeneityTet.
    // Change find_two_intersections as well.

    // TODO: If we know that one component of the barycentric coord is
    // zero, we can solve a 3x3 matrix to find the other components,
    // instead of solving the generic 4x4 matrix.  If we know that two
    // components are zero, we can find the other two trivially.  This
    // will prevent zeros from turning into epsilons.
   
    unsigned int n = CSkeletonElement::oppNode[onFace];

    // TODO: This check has been commented out while testing to see
    // what breaks if BARYTOLFACE is set to 0.0.
// #ifdef DEBUG
//     if(fabs(b0[n]) > BARYTOLFACE || fabs(b1[n]) > BARYTOLFACE) {
//       oofcerr << "find_one_intersection: barycentric components aren't zero!"
// 	      << std::endl;
//       oofcerr << "find_one_intersection: b0=" << b0 << " b1=" << b1
// 	      << " n=" << n << std::endl;
//       throw ErrProgrammingError("Barycentric coordinates on face are not zero",
// 				__FILE__, __LINE__);
//     }
// #endif // DEBUG
    b0[n] = 0.0;
    b1[n] = 0.0;
  }
  BarycentricCoord bint;	// intersection
  Coord3D bpos;			// position of intersection
  unsigned int oppNode = NONE;
  bool found = false;
  double error = std::numeric_limits<double>::max();
  double alpha = -1;
  for(unsigned int n=0; n<4 && !found; n++) {
    unsigned int face = CSkeletonElement::oppFace[n];
    if(face != excludeFace) {
      // Does the segment (b0, b1) intersect the face opposite node n?
      FaceIntersection *fint = find_face_intersection(
					      pixplane.convert2Coord3D(pt0),
					      pixplane.convert2Coord3D(pt1),
					      b0, b1, epts, iBounds, n
#ifdef DEBUG
					      , verbose, facePlanes, baryCache
#endif // DEBUG
						      );
      if(fint) {
	if(fint->entry == entry && fint->error < error) {
	  oppNode = fint->oppNode;
	  error = fint->error;
	  bint = fint->intersect;
	  bpos = fint->position;
	  alpha = fint-> alpha;
	}
	// If we've found an intersection that's definitely inside,
	// don't look any further.
	found = (error == 0.0);
	delete fint;
      }
    }
  } // end loop over nodes n
#ifdef DEBUG
  // if(verbose || oppNode == NONE || error > BARYTOLFACE) {
  //   oofcerr << "find_one_intersection: pt0=" << pt0 << " " << b0 << std::endl;
  //   oofcerr << "find_one_intersection: pt1=" << pt1 << " " << b1 << std::endl;
  //   oofcerr << "find_one_intersection: pts=";
  //   for(unsigned int i=0; i<pts.size(); i++)
  //     oofcerr << " " << pts[i].bcoord();
  //   oofcerr << std::endl;
  //   oofcerr << "find_one_intersection: bint=" << bint << std::endl;
  //   oofcerr << "find_one_intersection: oppNode=" << oppNode << std::endl;
  //   oofcerr << "find_one_intersection: error=" << error << std::endl;
  // }
  if(oppNode == NONE/* || error > 0.0*/) {
    throw ErrProgrammingError("Failed to find an intersection!",
			      __FILE__, __LINE__);
  }

#endif // DEBUG

  // At this point, bint contains the barycentric coords of the
  // intersection point or the best near miss and bpos is the 3D
  // position of the point.  oppNode is the index of the node opposite
  // the intersected face.
  Coord2D loc2D = pixplane.convert2Coord2D(bpos);
  unsigned int face = CSkeletonElement::oppFace[oppNode];

  // Which segment of the polygon is the intersection on?  If
  // TetPlaneIntersectionPoints i and i+1 are on the same face as
  // bint, then bint is on segment i.
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "find_one_intersection: calling getPolygonSegmentOnFace"
// 	    << std::endl;
// #endif // DEBUG
  unsigned int seg = getPolygonSegmentOnFace(oppNode, pts);
  const TetPlaneIntersectionPoint &segpt0 = pts[seg];
  const TetPlaneIntersectionPoint &segpt1 = pts[(seg+1)%pts.size()];

  // Where is the intersection on the polygon segment?
  double frac = fractionalDistance(segpt0.bcoord(), segpt1.bcoord(), bint);
#ifdef DEBUG
  if(!isfinite(frac)) {
    oofcerr << "find_one_intersection: endpts are " << segpt0.bcoord()
	    << " " << segpt1.bcoord() << std::endl;
    oofcerr << "find_one_intersection: intersection is " << bint
	    << std::endl;
    oofcerr << "find_one_intersection: frac=" << frac << std::endl;
    throw ErrProgrammingError("Fractional distance is NaN", __FILE__, __LINE__);
  }
#endif // DEBUG
  
  return new PixelBdyIntersection(pixplane, face, seg, frac, entry,
				  &loop, loopseg, alpha,
				  epts, facePlanes, baryCache);
} // end find_one_intersection()


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// Look for two intersections of the segment (pt0, pt1) with the
// polygon defined by pts.  Both endpoints are known to be outside the
// polygon.  The polygon is convex, so there must be either zero or
// two intersections.

static bool find_two_intersections(
			   const PixelBdyLoop &loop,
			   unsigned int loopseg,
			   const PixelPlane &pixplane,
			   unsigned int onFace,
			   const std::vector<Coord3D> &epts,
			   const ICRectangularPrism &iBounds,
			   const std::vector<const PixelPlane*> facePlanes,
			   const std::vector<TetPlaneIntersectionPoint> &pts,
			   unsigned int excludeFace,
#ifdef DEBUG
			   bool verbose,
#endif // DEBUG
			   BaryCoordCache &baryCache,
			   std::vector<PixelBdyIntersection*> &isecs)

{
  const ICoord2D &pt0 = loop.icoord(loopseg);
  const ICoord2D &pt1 = loop.next_icoord(loopseg);
#ifdef DEBUG
  if(verbose)
    oofcerr << "find_two_intersections: pt0=" << pt0 << " pt1=" << pt1
	    << " onFace=" << onFace
	    << " excludeFace=" << excludeFace << std::endl;
  OOFcerrIndent indent(2);
#endif	// DEBUG
  BarycentricCoord b0 = getBarycentricCoord(pt0, pixplane, epts, facePlanes,
					    baryCache);
  BarycentricCoord b1 = getBarycentricCoord(pt1, pixplane, epts, facePlanes,
					    baryCache);
  if(onFace != NONE) {
    unsigned int n = CSkeletonElement::oppNode[onFace];
    b0[n] = 0.0;
    b1[n] = 0.0;
  }

  // If the segment enters or exits through a polygon corner, there
  // can appear to be multiple entries or exits at that point, since
  // the segment will intersect two polygon edges.  Keep track of
  // entries and exits separately, to ensure that we don't
  // accidentally return two entries or two exits.

  // Keep only the entry with the largest alpha and the exit with the
  // smallest alpha. 

  double entryAlpha = -std::numeric_limits<double>::max();
  double exitAlpha = std::numeric_limits<double>::max();
  FaceIntersection *entryPt = NULL;
  FaceIntersection *exitPt = NULL;
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    if(f != excludeFace) {
      FaceIntersection *fi =
	find_face_intersection(pixplane.convert2Coord3D(pt0),
			       pixplane.convert2Coord3D(pt1),
			       b0, b1, epts, iBounds,
			       CSkeletonElement::oppNode[f]
#ifdef DEBUG
			       , verbose, facePlanes, baryCache
#endif // DEBUG
			       );
      if(fi) {

	// When two pixel planes look for intersections on oppositely
	// directed versions of the same segment, they should get the
	// same answers, except that entries for one pixel plane will
	// be exits for the other.  If two faces (two different f
	// values in this loop) intersect at the same alpha, the first
	// f will be chosen for one pixel plane and the second f for
	// the other unless we use > for the alpha comparisons for
	// entries and >= for exits (or vice versa).
	
	if(fi->entry && fi->alpha >= entryAlpha) {
	  if(entryPt != NULL) {
#ifdef DEBUG
	    if(verbose) {
	      oofcerr << "find_two_intersections: replacing entryPt"
		      << std::endl;
	    }
#endif // DEBUG
	    delete entryPt;
	  }
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "find_two_intersections: found entryPt " << *fi
		    << std::endl;
	  }
#endif // DEBUG
	  entryPt = fi;
	  entryAlpha = fi->alpha;
	}
	else if(!fi->entry && fi->alpha < exitAlpha) {
	  if(exitPt != NULL) {
#ifdef DEBUG
	    if(verbose) {
	      oofcerr << "find_two_intersections: replacing exitPt"
		      << std::endl;
	    }
#endif // DEBUG
	    delete exitPt;
	  }
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "find_two_intersections: found exitPt " << *fi
		    << std::endl;
	  }
#endif // DEBUG
	  exitPt = fi;
	  exitAlpha = fi->alpha;
	}
	else
	  delete fi;
      }
    }
  } // end loop over faces f

  // If the best intersections have the alphas in the wrong order, or
  // if *both* the entry and exit are outside the tet (ie, error > 0),
  // then there isn't any intersection.  (If either the entry or exit
  // is inside the tet, then the other must be too.)

  // Use > instead of >= when comparing alphas.  If points are
  // coincident, the coincidence detector will handle them better,
  // because it has more information.  There may be other conincident
  // points that we don't know about here.
  
  if(entryPt == NULL || exitPt == NULL || entryAlpha > exitAlpha
     || (entryPt->error > 0.0 && exitPt->error > 0.0))
    {
#ifdef DEBUG
      if(verbose) {
	oofcerr << "find_two_intersections: no intersection! ";
	if(!entryPt || !exitPt)
	  oofcerr << "entryPt=" << entryPt << " exitPt=" << exitPt;
	else if(entryAlpha >= exitAlpha)
	  oofcerr << "entryAlpha= " << entryAlpha
		  << " exitAlpha=" << exitAlpha;
	else
	  oofcerr << "entry error=" << entryPt->error << " exit error="
		  << exitPt->error;
	oofcerr << std::endl;
      }
#endif // DEBUG
      delete entryPt;
      delete exitPt;
      return false;
    }

#ifdef DEBUG
  if(verbose) {
    oofcerr << "find_two_intersections: entryPt=" << *entryPt << std::endl;
    oofcerr << "find_two_intersections:  exitPt=" << *exitPt << std::endl;
    if(entryPt->error > 0 || exitPt->error > 0) {
      oofcerr << "find_two_intersections:  *** error is positive!" << std::endl;
    }
  }
#endif // DEBUG

  // // If one of the intersection points is inside the tet but the other
  // // is outside, it must be from roundoff error.  Fix it.  We already
  // // know that one of the intersections is inside.
  // if(entryPt->error > 0) {
  //   entryPt->intersect.repair();
  // }
  // if(exitPt->error > 0) {
  //   exitPt->intersect.repair();
  // }
  
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "find_two_intersections: found best intersections at alpha="
// 	    << entryPt->alpha << " and " << exitPt->alpha
// 	    << "; delta=" << exitPt->alpha - entryPt->alpha << std::endl;
//     oofcerr << "find_two_intersections: entry is "
// 	    << entryPt->intersect << " "
// 	    << entryPt->intersect.position3D(epts)
// 	    << " error=" << entryPt->error << std::endl;
//     oofcerr << "find_two_intersections:  exit is "
// 	    << exitPt->intersect << " "
// 	    << exitPt->intersect.position3D(epts)
// 	    << " error=" << exitPt->error << std::endl;
//   }
// #endif // DEBUG

  // Compute the location of the intersection points along the polygon
  // edges.
  unsigned int seg0 = getPolygonSegmentOnFace(entryPt->oppNode, pts);
  double frac0 = fractionalDistance(pts[seg0].bcoord(),
				    pts[(seg0+1)%pts.size()].bcoord(),
				    entryPt->intersect);
  unsigned int seg1 = getPolygonSegmentOnFace(exitPt->oppNode, pts);
  double frac1 = fractionalDistance(pts[seg1].bcoord(),
				    pts[(seg1+1)%pts.size()].bcoord(),
				    exitPt->intersect);
  // It's safe to require frac[01] to be between 0 and 1 here, because
  // the error check above has already ensured that the intersection
  // points are not outside the polygon.
  frac0 = pinUnitRange(frac0, verbose);
  frac1 = pinUnitRange(frac1, verbose);
//   // If the intersections are outside the polygon, the intersection is
//   // spurious. 
//   if(frac0 < 0.0 || frac0 > 1.0 || frac1 < 0.0 || frac1 > 1.0) {
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "find_two_intersections: bad intersection! frac0="
// 	      << frac0 << " frac1-1=" << frac1-1 << std::endl;
//     }
// #endif // DEBUG
//     delete entryPt;
//     delete exitPt;
//     return false;
//   }

  // Coord3D loc3D = entryPt->position;
  // Coord2D loc2D = pixplane.convert2Coord2D(loc3D);
  unsigned int face = CSkeletonElement::oppFace[entryPt->oppNode];
  isecs[0] = new PixelBdyIntersection(pixplane, face, 
				      seg0, frac0, entryPt->entry,
				      &loop, loopseg, entryPt->alpha,
				      epts, facePlanes, baryCache);
#ifdef DEBUG
  if(verbose)
    oofcerr << "find_two_intersections: isecs[0]=" << *isecs[0] << std::endl;
#endif // DEBUG
  // loc3D = exitPt->position;
  // loc2D = pixplane.convert2Coord2D(loc3D);
  face = CSkeletonElement::oppFace[exitPt->oppNode];
  isecs[1] = new PixelBdyIntersection(pixplane, face,
				      seg1, frac1, exitPt->entry,
				      &loop, loopseg, exitPt->alpha,
				      epts, facePlanes, baryCache);
#ifdef DEBUG
  if(verbose)
    oofcerr << "find_two_intersections: isecs[1]=" << *isecs[1] << std::endl;
#endif // DEBUG
  delete entryPt;
  delete exitPt;
  return true;
} // end find_two_intersections()


// // Quick intersection-finding routine, used when you have topological
// // information about what's going on.  Specifically, you know that
// // it's geometrically required that the pixel boundary segment must
// // intersect the passed-in polygon edges exactly once, you know
// // whether it enters or exits, and the only real question is where
// // this occurs.

// // Since the polygon comes from the intersection of a tet with a
// // plane, and we need to match edges that come from different planes,
// // we need to compute intersection points using tet face data instead
// // of polygon edge data.  If two voxel boundary planes intersect each
// // other and a tet face, we want both voxel boundary planes to compute
// // the same intersection point even though they'll be working with
// // different polygon edges.

// static PixelBdyIntersection *find_one_intersection(
//     const PixelBdyLoop &loop,
//     const std::vector<Coord3D> &epts,
//     const PixelPlane &pixplane,
//     unsigned int seg, // index of the starting point of the bdy segment
//     const std::vector<TetPlaneIntersectionPoint> &pts, //  polygon corners
//     bool entry,		       // is the segment entering the polygon?
// #ifdef DEBUG
//     bool verbose,
// #endif // DEBUG
//     BaryCoordCache &baryCoordCache)
// {
// // #ifdef DEBUG
// //   OOFcerrIndent indent(2);
// //   if(verbose) {
// //     oofcerr << "find_one_intersection:" << std::endl;
// //     OOFcerrIndent indent(2);
// //     oofcerr << "find_one_intersection: loop=" << loop << std::endl;
// //     oofcerr << "find_one_intersection: seg=" << seg << " entry=" << entry
// //   	    << std::endl;
// //     oofcerr << "find_one_intersection: pixplane=" << pixplane << std::endl;
// //     oofcerr << "find_one_intersection:   pts=";
// //     std::cerr << pts;
// //     oofcerr << std::endl;
// //     oofcerr << "find_one_intersection: epts=";
// //     std::cerr << epts;
// //     oofcerr << std::endl;
// //   }
// // #endif // DEBUG
//   int npts = pts.size();
//   // Alpha is the fractional distance along an polygon segment, and
//   // beta is the fractional distance along the boundary segment.
//   // Round-off error can make it seem as if the intersection is just
//   // past the endpoint of one of the segments.  Unless we've found an
//   // intersection that clearly is in bounds, we use the one that's
//   // least out of bounds.
//   int t_segment = -1;		// segment number of the best intersection
//   Coord3D t_pos; 		// position of best intersection found so far
//   double t_alpha; 		// alpha for best intersection so far
//   unsigned int t_face;		// face index of ...
//   double error = std::numeric_limits<double>::max();
//   const ICoord2D segstart = loop.icoord(seg);
//   const ICoord2D segend = loop.next_icoord(seg);
//   bool decrseg = loop.decreasing(seg);
  
//   if (loop.horizontal(seg)) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "find_one_intersection: horizontal" << std::endl;
// #endif // DEBUG
//     OOFcerrIndent indent(2);
//     // int fp_level = segstart[1];
//     for(int i1=0; i1<npts; ++i1) { // loop over polygon edges
//       int i2 = (i1 + 1)%npts;
//       const Coord2D p1 = pts[i1].location2D(pixplane);
//       const Coord2D p2 = pts[i2].location2D(pixplane);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: examining polygon edge " << i1
//       		<< " " << p1 << " " << p2 << std::endl;
// #endif // DEBUG
      
//       // Ignore the parallel case.
//       if (p1[1] == p2[1]) {
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "find_one_intersection: ignoring parallel edge"
// 		  << std::endl;
// #endif // DEBUG
// 	continue;
//       }

//       // Also skip segments which are oriented incorrectly for the
//       // type of intersection we want.  A horizontal category edge is
//       // entering the polygon if the category edge is L->R (!decrseg)
//       // and the polygon edge is is going down (!goingup), or if the
//       // category edge is R->L (decrseg) and the polygon edge is going
//       // up.
//       bool goingup = p2[1] > p1[1]; // polygon edge is going up
//       bool seg_entry = (goingup == decrseg);
//       if (seg_entry != entry) {
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "find_one_intersection: ignoring wrongly directed edge"
// 		  << std::endl;
// #endif	// DEBUG
// 	continue;
//       }

//       // Compute the intersection of the boundary segment with the
//       // face of the tetrahedron that the polygon segment was formed
//       // from.  Computing it in this way ensures that the round-off
//       // error in the result is independent of pixplane.
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: looking for intersection of segment ("
//       		<< pixplane.convert2Coord3D(segstart) << ", "
//       		<< pixplane.convert2Coord3D(segend) << ")" << std::endl
//       		<< "                       with polygon edge ("
//       		<< pixplane.convert2Coord3D(p1) << ", "
//       		<< pixplane.convert2Coord3D(p2) << ")" << std::endl;
// #endif // DEBUG
//       unsigned int face_index = sharedFace(pts[i1], pts[i2]);
//       Coord3D intersect3D = segmentFaceIntersection(
// 				       pixplane.convert2Coord3D(segstart),
// 				       pixplane.convert2Coord3D(segend),
// 				       faceNodes(face_index, epts)
// #ifdef DEBUG
// 				       , verbose
// #endif // DEBUG
// 						    );
//       // Find the location of the intersection on the pixel plane. 
//       Coord2D intersect2D = pixplane.convert2Coord2D(intersect3D);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: segmentFaceIntersection = "
//       		<< intersect3D << " " << intersect2D
// 		<< " face=" << face_index << std::endl;
// #endif // DEBUG
//       // Is the 2D intersection point between the endpoints of the boundary
//       // segment and the polygon segment?
//       double alpha = fractionalDistance(intersect2D, p1, p2);
//       double beta = (intersect2D[0] - segstart[0])/(segend[0] - segstart[0]);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: alpha=" << alpha << " beta=" << beta
//       		<< std::endl;
// #endif // DEBUG
//       // If the trial alpha/beta is in-bounds, we're done.
//       // TODO: Should these checks use <= and >= ?
//       if ((alpha > 0) && (alpha < 1) && (beta > 0) && (beta < 1)) {
// 	intersect2D[1] = segstart[1]; // correct possible roundoff error
// 	PixelBdyIntersection *pbi =
// 	  new PixelBdyIntersection(intersect2D, intersect3D,
// 				   i1, face_index, alpha, entry);
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "find_one_intersection: found " << *pbi << std::endl;
// #endif // DEBUG
// 	return pbi;
//       }
//       // Compute how far out of bounds we ended up.
//       double new_error = 0.0;
//       if (alpha > 1)
// 	new_error = (alpha-1.0)*(alpha-1.0);
//       else if (alpha < 0)
// 	new_error = alpha*alpha;
//       if (beta > 1)
// 	new_error += (beta-1.0)*(beta-1.0);
//       else if (beta < 0)
// 	new_error += beta*beta;
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: error=" << new_error << std::endl;
// #endif // DEBUG
      
//       // If this is the first iteration, or if the new error is
//       // smaller than the already-stored error, save the results.
//       if (new_error < error) {
// 	error = new_error;
// 	t_segment = i1;
// 	t_pos = intersect3D;
// 	t_alpha = alpha > 1.0? 1.0 : (alpha < 0.0 ? 0 : alpha);
// 	t_face = face_index;
//       }
//     } // end loop over polygon edges
    
//     // If we made it out of the loop, that means none of the element
//     // segments were in-bounds.  But the caller insists there must be
//     // an intersection, so we'll return our best guess.
//     assert(t_segment != -1);
//     PixelBdyIntersection *pbi =
//       new PixelBdyIntersection(pixplane.convert2Coord2D(t_pos), t_pos,
// 			       t_segment, t_face, t_alpha, entry);
// #ifdef DEBUG    
//     if(verbose)
//       oofcerr << "find_one_intersection: returning best guess "
//     	      << *pbi << std::endl;
// #endif // DEBUG
//     return pbi;
//   } // end if horizontal
  
//   else {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "find_one_intersection: vertical" << std::endl;
// #endif // DEBUG
//     // Pixel boundary segment is vertical
//     // int fp_level = segstart[0];
//     for(int i1=0; i1 <npts; ++i1) { // loop over polygon edges
//       int i2 = (i1 + 1)%npts;
//       const Coord2D p1 = pts[i1].location2D(pixplane);
//       const Coord2D p2 = pts[i2].location2D(pixplane);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: examining polygon edge " << i1
//       		<< " " << p1 << " " << p2 << std::endl;
// #endif // DEBUG
//       // Again, ignore the parallel case.
//       if (p1[0] == p2[0]) {
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "find_one_intersection:  ignoring parallel edge"
// 		  << std::endl;
// #endif	// DEBUG
// 	continue;
//       }
//       // And again, ignore wrongly oriented segments.
//       bool goingright = p2[0] > p1[0]; // polygon edge is going right
//       bool seg_entry = (goingright != decrseg);
//       if (seg_entry != entry) {
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "find_one_intersection:  ignoring wrongly directed edge"
// 		  << std::endl;
// #endif	// DEBUG
// 	continue;
//       }
// #ifdef DEBUG
//       if(verbose) {
//       	oofcerr << "find_one_intersection: looking for intersection of segment ("
//       		<< pixplane.convert2Coord3D(segstart) << ", "
//       		<< pixplane.convert2Coord3D(segend) << ")" << std::endl
//       		<< "                       with polygon edge ("
//       		<< pixplane.convert2Coord3D(p1) << ", "
//       		<< pixplane.convert2Coord3D(p2) << ")" << std::endl;
//       }
// #endif // DEBUG
//       unsigned int face_index = sharedFace(pts[i1], pts[i2]);
//       Coord3D intersect3D = segmentFaceIntersection(
// 				       pixplane.convert2Coord3D(segstart),
// 				       pixplane.convert2Coord3D(segend),
// 				       faceNodes(face_index, epts)
// #ifdef DEBUG
// 				       , verbose
// #endif // DEBUG
// 						    );
//       Coord2D intersect2D = pixplane.convert2Coord2D(intersect3D);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: segmentFaceIntersection = "
//       		<< intersect3D << " " << intersect2D
// 		<< " face=" << face_index << std::endl;
// #endif // DEBUG
//       double alpha = fractionalDistance(intersect2D, p1, p2);
//       double beta = (intersect2D[1] - segstart[1])/(segend[1] - segstart[1]);
// #ifdef DEBUG
//       if(verbose)
//       	oofcerr << "find_one_intersection: alpha=" << alpha << " beta=" << beta
//       		<< std::endl;
// #endif // DEBUG
//       // If we're in-bounds, we're done.
//       if ((alpha > 0) && (alpha < 1) && (beta > 0) && (beta < 1)) {
// 	intersect2D[0] = segstart[0]; // correct possible roundoff error
// 	PixelBdyIntersection *pbi=
// 	  new PixelBdyIntersection(intersect2D, intersect3D,
// 				   i1, face_index, alpha, entry);
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "find_one_intersection: found " << *pbi << std::endl;
// #endif // DEBUG
// 	return pbi;
//       }
//       double new_error=0.0;
//       if (alpha > 1)
// 	new_error = (alpha-1.0)*(alpha-1.0);
//       if (alpha < 0)
// 	new_error = alpha*alpha;
//       if (beta > 1)
// 	new_error += (beta-1.0)*(beta-1.0);
//       if (beta < 0)
// 	new_error += beta*beta;
      
//       if (new_error < error) {
// 	error = new_error;
// 	t_segment = i1;
// 	t_pos = intersect3D;
// 	t_alpha = alpha > 1.0? 1.0 : (alpha < 0.0 ? 0.0 : alpha);
// 	t_face = face_index;
//       }
//     }
//     // If we made it this far, we were never in-bounds.  Return best-guess.
//     assert(t_segment != -1);
//     PixelBdyIntersection *pbi =
//       new PixelBdyIntersection(pixplane.convert2Coord2D(t_pos), t_pos,
// 			       t_segment, t_face, t_alpha, entry);
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "find_one_intersection: returning best guess "
//     	      << *pbi << std::endl;
// #endif // DEBUG
//     return pbi;
							    
//   } // end if !horizontal
// }
// end PixelBdyLoop::find_one_intersection

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// findPixelPlaneFacets finds the facets in the x, y, and z planes of
// the intersection of a tet with the voxel set boundarys.  It works
// in pixel coordinates (in-plane voxel coordinates).  It works in
// more or less the same way as the 2D CSkeletonElement::categoryAreas
// routine (but has been modified so much that comparison to 2D is
// probably not practical).

// Actually, the work of findPixelPlaneFacets is done by
// doFindPixelPlaneFacets, which is called by findPixelPlaneFacets
// after findPixelPlaneFacets figures out whether it's using facet
// loops or cross section loops.

// "onFace" indicates whether the pixel plane coincides with a tet
// face. It's equal to either the face index or NONE.

// If the area of the tet's intersection with the plane is less than
// MIN_PLANE_AREA, in pixel units, it's assumed not to intersect at
// all.
// TODO: Is this still necessary?

#define MIN_PLANE_AREA 0.0 //1.e-5

static void doFindPixelPlaneFacets(
			   const PixelPlane &pixplane,
			   const std::vector<PixelBdyLoop*> &loops,
			   const std::vector<Coord3D> &epts,
			   const ICRectangularPrism &iBounds,
			   unsigned int onFace,
			   const std::vector<const PixelPlane*> &facePlanes,
			   unsigned int category,
#ifdef DEBUG
			   bool verbose,
#endif // DEBUG
			   FacetMap2D &facets,
			   BaryCoordMap &baryEquiv,
			   FacetCornerList &allCorners,
			   TetPlaneIntersectionCache &tetPlaneIntCache,
			   BaryCoordCache &baryCache
				   )
{
#ifdef DEBUG
  bool verbosecategory = verboseCategory(verbose, category);
  bool verboseplane = verbosePlane(verbosecategory, pixplane);
#endif // DEBUG
  OOFcerrIndent indent(2);

  
  // Find the polygon formed by the intersection of the edges of the
  // tet with the c-plane.  TODO: We could save some work by treating
  // both normals together here, instead of computing tetPts twice.

  // tetPts and tetCoords are allocated in
  // getTetPlaneIntersectionPoints and live in tetPlaneIntCache.
  // They're deleted when the cache is destroyed.
  std::vector<TetPlaneIntersectionPoint> *tetPts = 0;
  std::vector<Coord2D> *tetCoords;
  unsigned int excludeFace = NONE;
  getTetPlaneIntersectionPoints(pixplane, epts,
#ifdef DEBUG
				verboseplane,
#endif // DEBUG
				tetPlaneIntCache, &tetPts, &tetCoords,
				excludeFace);

  unsigned int nn = tetPts->size();
  
  // If there's no intersection, go on to the next plane.
  if(nn < 3) {
// #ifdef DEBUG
//     if(verboseplane)
//       oofcerr << "doFindPixelPlaneFacets: no intersection! nn=" << nn
// 	      << std::endl;
// #endif // DEBUG
    return;
  }

#ifdef DEBUG
  if(verboseplane)
    oofcerr << "doFindPixelPlaneFacets: pixplane=" << pixplane
  	    << " category=" << category
  	    << std::endl;
#endif // DEBUG

  // The tet intersects the plane.  There might be an intersection
  // with the voxel set boundary, so create a new PixelPlaneFacet
  // object to store it.  It will be deleted by cleanUpFacetMaps()
  // when CSkeletonElement::categoryVolumes() finishes.
  PixelPlaneFacet *facet = new PixelPlaneFacet();
  facets[pixplane] = facet;

  // Check that the area of the polygon isn't too small.  If it is,
  // there really isn't any intersection.
  // TODO: Do we really need to check this?  Defining MIN_PLANE_AREA
  // is ugly.
  double polyarea = tetCoords->back() % tetCoords->front();
  for(unsigned int i=1; i<tetCoords->size(); i++)
    polyarea += (*tetCoords)[i-1] % (*tetCoords)[i];
#ifdef DEBUG
  if(verboseplane)
    oofcerr << "doFindPixelPlaneFacets: polyarea=" << 0.5*polyarea << std::endl;
#endif // DEBUG
  if(polyarea < 2*MIN_PLANE_AREA) {
#ifdef DEBUG
    if(verboseplane)
      oofcerr << "doFindPixelPlaneFacets: ignoring tiny intersection polygon"
	      << std::endl;
#endif // DEBUG
    return;
  }
  
#ifdef DEBUG
  if(verboseplane) {
    oofcerr << "doFindPixelPlaneFacets: tetPts=";
    std::cerr << *tetPts;
    oofcerr << std::endl;
    oofcerr << "                        Coords=";
    std::cerr << *tetCoords;
    oofcerr << std::endl;
    oofcerr << "                            ";
    for(unsigned int kk=0; kk<nn; kk++)
      oofcerr << " " << (*tetPts)[kk].location3D(pixplane);
    oofcerr << std::endl;
    oofcerr << "                            ";
    for(unsigned int kk=0; kk<nn; kk++)
      oofcerr << " " << (*tetPts)[kk].bcoord();
    oofcerr << std::endl;
  }
#endif // DEBUG
      
  // Find the bounding box of the tet points.  There are either 3
  // or 4 of them.
  assert(nn == 3 || nn == 4);
  CRectangle tetBounds((*tetCoords)[0], (*tetCoords)[1]);
  tetBounds.swallow((*tetCoords)[2]);
  if(nn == 4)
    tetBounds.swallow((*tetCoords)[3]);
      
  // Store intersection data -- used to figure out what sections of
  // the polygon boundaries contribute to the area.  Stored a couple
  // of ways -- firstly by element edge, so it can be easily
  // traversed, and secondly indexed by coordinate, so duplicates can
  // be removed.
  std::vector<ElEdgeMap> eledgedata(nn); 
  CoordIsec coordisecs;	 // multimap<Coord2D, PixelBdyIntersection>

  // For each loop in the PixelSetBoundary, find its intersection
  // with the polygon formed by tetPts.  This block is copied more
  // or less from the 2D CSkeletonElement::categoryAreas() method.
  // It's not copied verbatim because that code works in physical
  // coordinates, but here we're using pixel coordinates.

#ifdef DEBUG
  if(verboseplane)
  	oofcerr << "doFindPixelPlaneFacets: getting loops for category "
  		<< category << std::endl;
#endif // DEBUG
	
  for(std::vector<PixelBdyLoop*>::const_iterator pbl=loops.begin();
      pbl!=loops.end(); ++pbl)
    {
      // Intersection data for this loop
      std::vector<ElEdgeMap> eledgedata_loop(nn);
      CoordIsec coordisecs_loop;
      
      OOFcerrIndent indent(2);
      const PixelBdyLoop &loop = *(*pbl);
      // Skip this bdy loop if its bounding box doesn't intersect
      // the polygon's bounding box.
      if(!tetBounds.intersects(loop.bbox())) {
	continue;
      }
#ifdef DEBUG
      if(verboseplane)
        oofcerr << "doFindPixelPlaneFacets: examining loop " << loop
		<< std::endl;
#endif // DEBUG
      
      // Find the interiority of the start of the first pixel boundary
      // segment.  End-point interiorities are done on the fly in the
      // k loop.  Start point interiorities for every point after the
      // first are the same as the end point interiority of the
      // previous point.
      BarycentricCoord pbs_start_bary = getBarycentricCoord(
				    loop.icoord(0), pixplane, epts,
				    facePlanes, baryCache);
      bool pbs_start_inside =  pbs_start_bary.interior(onFace);
      //  interior(loop.icoord(0), pixplane, epts, onFace, baryCache);
	  
      unsigned int loopsize = loop.size();
      // Loop over segments of the boundary loop
      for(unsigned int k=0; k<loopsize; ++k) {
	OOFcerrIndent indent2(2);
	ICoord2D pbs_start = loop.icoord(k);
	ICoord2D pbs_end = loop.next_icoord(k);
	BarycentricCoord pbs_end_bary = getBarycentricCoord(
					    pbs_end, pixplane, epts,
					    facePlanes, baryCache);
	bool pbs_end_inside = pbs_end_bary.interior(onFace);
	  // interior(pbs_end, pixplane, epts, onFace, baryCache);
#ifdef DEBUG
	if(verboseplane)
	  oofcerr << "doFindPixelPlaneFacets: examining bdy loop segment "
		  << k << " "
		  << pbs_start << " "
		  << pixplane.convert2Coord3D(pbs_start) << " "
		  << getBarycentricCoord(pbs_start, pixplane, epts,
					 facePlanes, baryCache)
		  << " ("
		  << (pbs_start_inside ? "interior" : "exterior") << ") --> "
		  << pbs_end << " "
		  << pixplane.convert2Coord3D(pbs_end) << " "
		  << getBarycentricCoord(pbs_end, pixplane, epts, facePlanes,
					 baryCache)
		  << " ("
		  << (pbs_end_inside ? "interior" : "exterior") << ")"
		  << std::endl;
	OOFcerrIndent indent3(2);
#endif	// DEBUG
	if(pbs_start_inside && pbs_end_inside) {
	  // Pixel boundary segment is wholly interior. (We know this
	  // because the endpoints are inside and the polygon is
	  // guaranteed to be convex).
#ifdef DEBUG
	  if(verboseplane)
	  	oofcerr << "doFindPixelPlaneFacets: segment is interior"
	  		<< std::endl;
#endif // DEBUG
	  facet->addEdge(new PixelFacetCorner(pbs_start, pbs_start_bary,
					      pixplane, allCorners),
			 new PixelFacetCorner(pbs_end, pbs_end_bary,
					      pixplane, allCorners)
#ifdef DEBUG
			 , "interior pixels " + to_string(pixplane),
			 verboseplane
#endif // DEBUG
			 );
	}
	    
	else if(pbs_start_inside != pbs_end_inside) {
	  // If start and end are hetero-interior, so to speak,
	  // then there's an intersection.  Find it.
	  PixelBdyIntersection *pbi = 
	    find_one_intersection(loop, k, 
				  pixplane, onFace, epts, iBounds, facePlanes,
				  *tetPts,
				  excludeFace,
				  pbs_end_inside,
#ifdef DEBUG
				  verboseplane,
#endif // DEBUG
				  baryCache);
#ifdef DEBUG
	  if(verboseplane) {
	    oofcerr << "doFindPixelPlaneFacets: found one intersection"
		    << std::endl;
	    oofcerr << "     " << *pbi << std::endl;
	  }
#endif // DEBUG
	  eledgedata_loop[pbi->segment].insert(
				  ElEdgeMap::value_type(pbi->fraction,pbi));
	  coordisecs_loop.insert(CoordIsec::value_type(pbi->location2D, pbi));
	  if(pbs_start_inside) {
	    facet->addEdge(new PixelFacetCorner(pbs_start, pbs_start_bary,
						pixplane, allCorners),
			   new FaceFacetCorner(pbi, pixplane, allCorners)
#ifdef DEBUG
			   , ("exit, seg=[" +
			      to_string(pixplane.convert2Coord3D(pbs_start))
			      + "," +
			      to_string(pixplane.convert2Coord3D(pbs_end))
			      + "] " + to_string(pixplane)),
			   verboseplane
#endif // DEBUG
			   );
	  }
	  else {
	    facet->addEdge(new FaceFacetCorner(pbi, pixplane, allCorners),
			   new PixelFacetCorner(pbs_end, pbs_end_bary,
						pixplane, allCorners)
#ifdef DEBUG
			   ,
			   ("entrance, seg=[" +
			    to_string(pixplane.convert2Coord3D(pbs_start))
			    + "," +
			    to_string(pixplane.convert2Coord3D(pbs_end))
			    +"] " + to_string(pixplane)),
			   verboseplane
#endif // DEBUG
			   );
	  }
	}	// end if bdy segment has exactly one endpoint inside

	else {
	  assert(!pbs_start_inside && !pbs_end_inside);
	  // The current segment has both endpoints outside the
	  // polygon.  It must intersect zero or two times.


#ifdef DEBUG
	  // if(verboseplane)
	  //   oofcerr << "doFindPixelPlaneFacets: calling find_two_intersections"
	  // 	      << std::endl;
	  // OOFcerrIndent indent(2);
#endif // DEBUG
	  
	  // There are either zero or two intersections, although
	  // they could be degenerate.
	  
	  std::vector<PixelBdyIntersection*> isecs(2);
	  
	  // TODO: Do some bounding box checks before calling
	  // find_two_intersections.  Lots of voxel boundary set
	  // segments will be completely outside the polygon.
	  if(find_two_intersections(loop, k,
				    pixplane, onFace, epts, iBounds,
				    facePlanes, *tetPts,
				    excludeFace,
#ifdef DEBUG
				    verboseplane,
#endif // DEBUG
				    baryCache,
				    isecs))
	    {
#ifdef DEBUG
	      if(verboseplane) {
		oofcerr << "doFindPixelPlaneFacets: found two intersections"
			<< std::endl;
		oofcerr << "     " << *isecs[0] << std::endl;
		oofcerr << "     " << *isecs[1] << std::endl;
	      }
#endif // DEBUG
	      for(unsigned int ii=0; ii<2; ii++) {
		eledgedata_loop[isecs[ii]->segment].insert(
		      ElEdgeMap::value_type(isecs[ii]->fraction, isecs[ii]));
		coordisecs_loop.insert(
			       CoordIsec::value_type(isecs[ii]->location2D,
						     isecs[ii]));
	      }
	      facet->addEdge(
		     new FaceFacetCorner(isecs[0], pixplane, allCorners),
		     new FaceFacetCorner(isecs[1], pixplane, allCorners)
#ifdef DEBUG
		     ,
		     ("double intersection, seg=" +
		      to_string(pixplane.convert2Coord3D(pbs_start))
		      + "," +
		      to_string(pixplane.convert2Coord3D(pbs_end))
		      + " " + to_string(pixplane)),
		     verboseplane
#endif // DEBUG
			     );
	    } // end if two intersections were found
// #ifdef DEBUG
// 	    else {
// 	      if(verboseplane)
// 		oofcerr << "doFindPixelPlaneFacets: find_two_intersections returned false" << std::endl;
// 	    }
// #endif // DEBUG
	}   // end if both endpoints are exterior
	    
	// Hand off status info in preparation for next pixel bdy segment
	pbs_start_inside = pbs_end_inside;
	pbs_start_bary = pbs_end_bary;
	    
      } // end loop over segments k
// #ifdef DEBUG
//       if(verboseplane)
//       	oofcerr << "doFindPixelPlaneFacets: done looping over bdy loop segments"
//       		<< std::endl;
// #endif // DEBUG


      // Do coincidence checking for this VSB loop.

      // oofcerr << "doFindPixelPlaneFacets: checking for coincidences"
      // 	      << std::endl;

      unsigned int totalIntersections = coordisecs_loop.size();
      std::set<Coord2D> coincidentLocs;
      CoordIsec coincidences;
      for(auto x=coordisecs_loop.begin(); x!=coordisecs_loop.end(); ++x) {
	Coord2D loc = (*x).first;
	bool found = false;
	for(Coord2D p : coincidentLocs) {
#define CLOSEBY 0.3
#define CLOSEBY2 (CLOSEBY*CLOSEBY)
	  if(norm2(loc-p) < CLOSEBY2) {
	    coincidences.insert(CoordIsec::value_type(p, (*x).second));
	    found = true;
	  }
	}
	if(!found) {
	  coincidences.insert(CoordIsec::value_type(loc, (*x).second));
	  coincidentLocs.insert(loc);
	}
      }
      for(Coord2D loc : coincidentLocs) {
	if(coincidences.count(loc) > 1) {
	  unsigned int nEntries = 0;
	  unsigned int nExits = 0;
	  auto range = coincidences.equal_range(loc);
	  for(auto pt=range.first; pt!=range.second; ++pt) {
	    PixelBdyIntersection *pbi = (*pt).second;
	    if(pbi->entry)
	      nEntries++;
	    else
	      nExits++;
	  }
	  unsigned int nIntersections = nEntries + nExits;

	  if(nIntersections == 2) {
	    resolveTwoFoldCoincidence(nEntries, nExits, range, epts,
				      eledgedata_loop, baryEquiv, facet,
				      pixplane, onFace, facePlanes, baryCache
#ifdef DEBUG
				      , verboseplane
#endif // DEBUG
				      );
	  }
	  else if(nIntersections == 3) {
	    resolveThreeFoldCoincidence(range, epts, eledgedata_loop,
					baryEquiv, facet, pixplane, onFace,
					facePlanes, baryCache
#ifdef DEBUG
				      , verboseplane
#endif // DEBUG
					);
	  }
	  else {
	    resolveMultipleCoincidence(range, epts, nn, totalIntersections,
				       eledgedata_loop, baryEquiv, facet,
				       pixplane, onFace, facePlanes, baryCache
#ifdef DEBUG
				       , verboseplane
#endif // DEBUG
				       );
	  }
	}
      }
      // oofcerr << "doFindPixelPlaneFacets: finished coincidence check"
      // 	      << std::endl;

      // Merge cleaned intersection data from the loop-specific
      // version of eledgedata into the global one.
      for(unsigned int i=0; i<nn; i++) {
	eledgedata[i].insert(eledgedata_loop[i].begin(),
			     eledgedata_loop[i].end());
      }
      // oofcerr << "doFindPixelPlaneFacets: merged eledgedata" << std::endl;
      
    }   // end loop over pixel boundary loops

#ifdef DEBUG
  if(verboseplane) {
    oofcerr << "doFindPixelPlaneFacets: done looping over bdy loops"
  	    << std::endl;
    oofcerr << "doFindPixelPlaneFacets: before coincidence check:" << std::endl;
    OOFcerrIndent indent(2);
    oofcerr << "doFindPixelPlaneFacets: facet= " << std::endl;
    for(std::set<FacetEdge>::const_iterator e=facet->begin();
	e!=facet->end(); ++e)
      {
	OOFcerrIndent indent(2);
	oofcerr << *e << std::endl;
      }
    for(unsigned int i=0; i<nn; i++) {
      if(!eledgedata[i].empty()) {
	oofcerr << "doFindPixelPlaneFacets: polygon edge="
		<< (*tetPts)[i].location3D(pixplane) << " "
		<< (*tetPts)[(i+1)%nn].location3D(pixplane) 
		<< " eledgedata[" << i <<"]="
		<< std::endl;
	std::cerr << eledgedata[i] << std::endl;
      }
    }
  }
#endif // DEBUG
      
  // At this point, we have found all the facet edges which are
  // boundaries of the 2D pixel set and are interior to the current
  // polygon. It remains to traverse the polygon exterior and find the
  // portions of it which are between an exit intersection and an
  // entry intersection.

  
// THIS BLOCK OF COINCIDENCE CHECKING HAS BEEN MOVED INSIDE THE LOOP
// OVER VSB FACET LOOPS.. COPY THE COMMENTS OUT OF HERE BEFORE
// DELETING
//   // But first.. Check for multiple coincident intersections.  These
//   // arise when a corner of a polygon coincides with an edge of the
//   // pixel set boundary, or a corner of the pixel set boundary
//   // coincides with an edge of the polygon, or a corner of one
//   // coincides with a corner of the other.  Coincident intersections
//   // may be incorrectly ordered, and so are confusing to the traversal
//   // code, so we rationalize them here.

//   unsigned int totalIntersections = coordisecs.size();

//   std::set<Coord2D> coincidentLocs;
//   CoordIsec coincidences;
//   for(auto x=coordisecs.begin(); x!=coordisecs.end(); ++x) {
//     // coordisecs and coincidences are both
//     // std::multimap<Coord2D,PixelBdyIntersection*>s.  The difference
//     // between them is that the key in coordisecs is the actual
//     // position of the PixelBdyIntersection, whereas in coincidences
//     // it may be the position of a nearby PixelBdyIntersection.
    
//     // TODO: We could construct coincidences instead of coordisecs
//     // initially.  Do we really need coordisecs?

//     Coord2D loc = (*x).first;	// position of this intersection

//     // Have we already found a nearby intersection?
//     bool found = false;
//     for(Coord2D p : coincidentLocs) {
//       // The definition of "closeby" here is somewhat arbitrary.  The
//       // exact value shouldn't matter as long as it's less than a
//       // pixel size and significantly greater than the expected round
//       // off error.  There should be no way that a set of mutually
//       // close points includes more than one voxel corner.
// #define CLOSEBY 0.3
// #define CLOSEBY2 (CLOSEBY*CLOSEBY)
//       if(norm2(loc-p) < CLOSEBY2) {
// 	coincidences.insert(CoordIsec::value_type(p, (*x).second));
// 	found = true;
//       }
//     }
//     if(!found) {
//       coincidences.insert(CoordIsec::value_type(loc, (*x).second));
//       coincidentLocs.insert(loc);
//     }
//   }
// // #ifdef DEBUG
// //   if(verboseplane) {
// //     oofcerr << "doFindPixelPlaneFacets: coincidentLocs=";
// //     std::cerr << coincidentLocs;
// //     oofcerr << std::endl;
// //     oofcerr << "doFindPixelPlaneFacets: intersections grouped for coincidence detection" << std::endl;
// //     for(auto coinkydink : coincidences) {
// //       oofcerr <<  "     " << coinkydink.first << ": " << *coinkydink.second
// // 	      << std::endl;
// //     }
// //   }
// // #endif // DEBUG
  
//   // Examine each set of coincident points.
//   for(Coord2D loc : coincidentLocs) { // loop over possible coincidence spots
//     if(coincidences.count(loc) > 1) { // is there a coincidence here
//       unsigned int nEntries = 0;
//       unsigned int nExits = 0;
//       auto range = coincidences.equal_range(loc);
//       for(auto pt=range.first; pt!=range.second; ++pt) {
// 	PixelBdyIntersection *pbi = (*pt).second;
// 	if(pbi->entry)
// 	  nEntries++;
// 	else
// 	  nExits++;
//       }
//       // Number of intersections near loc.
//       unsigned int nIntersections = nEntries + nExits;

//       // The types of possible coincidences can be enumerated easily
//       // because the polygon is convex and the corners of the VSB loop
//       // are at least one pixel size away from each other.

//       if(nIntersections == 2) {
// #ifdef DEBUG
// 	if(verboseplane)
// 	  oofcerr << "doFindPixelPlaneFacets: two fold coincidence at "
// 		  << loc << std::endl;
// #endif // DEBUG
// 	resolveTwoFoldCoincidence(nEntries, nExits, range, epts, eledgedata,
// 				  baryEquiv, facet, pixplane, onFace,
// 				  facePlanes, baryCache
// #ifdef DEBUG
// 				  , verboseplane
// #endif // DEBUG
// 				  );
//       }	

//       else if(nIntersections == 3) {
// #ifdef DEBUG
// 	if(verboseplane)
// 	  oofcerr << "doFindPixelPlaneFacets: three fold coincidence at "
// 		  << loc << std::endl;
// #endif // DEBUG
// 	resolveThreeFoldCoincidence(range, epts, eledgedata, baryEquiv, facet,
// 				    pixplane, onFace, facePlanes, baryCache
// #ifdef DEBUG
// 				    , verboseplane
// #endif // DEBUG
// 				    );
//       }
//       else {
// 	#ifdef DEBUG
// 	if(verboseplane)
// 	  oofcerr << "doFindPixelPlaneFacets: multiple fold coincidence at "
// 		  << loc << " nIntersections=" << nIntersections
// 		  << std::endl;
// #endif // DEBUG

// 	resolveMultipleCoincidence(range, epts, nn, totalIntersections,
// 				   eledgedata, baryEquiv, facet, pixplane,
// 				   onFace, facePlanes, baryCache
// #ifdef DEBUG
// 				   , verboseplane
// #endif // DEBUG
// 				   );
//       }
//     } // end if there is a coincidence
//   }   // end loop over coincidence locations loc

// #ifdef TWO_STAGE_COINCIDENCE_DETECTION
//   // CoordIsec is std::multimap<Coord2D, PixelBdyIntersection*>
//   CoordIsec::iterator x = coordisecs.begin();
//   while(x != coordisecs.end()) {
//     const Coord2D key = (*x).first;
//     int ct = coordisecs.count(key);
// #ifdef DEBUG
//     if(verboseplane) {
//       oofcerr << "doFindPixelPlaneFacets: coordisecs key=" << key
// 	      << " ct=" << ct << std::endl;
//     }
// #endif // DEBUG
//     if(ct > 1) {
//       CoordIsec::iterator w = x;
//       // Set x to the start of the next key, for the next iteration of
//       // the outer loop.
//       x = coordisecs.upper_bound(key);
//       // Determine the sign of the resultant intersection.  It may be
//       // entry, exit, or zero, if everything cancels out.
//       int entries = 0;
//       int exits = 0;
//       for(CoordIsec::iterator t=w; t!=x; ++t) {
// 	if((*t).second->entry)
// 	  entries++;
// 	else
// 	  exits++;
//       }
// #ifdef DEBUG
//       if(abs(entries-exits) > 1) {
// 	oofcerr << "doFindPixelPlaneFacets: entries=" << entries
// 		<< " exits=" << exits << " at " << key << std::endl;
// 	throw ErrProgrammingError("Unexpected entry count at coincident point!",
// 				  __FILE__, __LINE__);
//       }
// #endif // DEBUG
//       if(entries > exits) {
// 	// Keep the first entry in the set of coincident points, and
// 	// delete the rest.
// 	bool got_entry = false;
// 	for(CoordIsec::iterator t2=w; t2!=x; ++t2) {
// 	  if((*t2).second->entry && !got_entry) {
// #ifdef DEBUG
// 	    if(verboseplane) {
// 	      oofcerr << "doFindPixelPlaneFacets: keeping coincidence (1) "
// 		      << *(*t2).second << std::endl;
// 	    }
// #endif // DEBUG
// 	    got_entry = true;
// 	  }
// 	  else {
// #ifdef DEBUG
// 	    if(verboseplane) {
// 	      oofcerr << "doFindPixelPlaneFacets: deleting coincidence (1) "
// 		      << *(*t2).second << std::endl;
// 	    }
// #endif // DEBUG
// 	    delete_isec((*t2).second, eledgedata);
// 	  }
// 	}
//       }
//       else if(entries < exits) {
// 	bool got_exit = false;
// 	for(CoordIsec::iterator t2=w; t2!=x; ++t2) {
// 	  if(!(*t2).second->entry && !got_exit) {
// #ifdef DEBUG
// 	    if(verboseplane) {
// 	      oofcerr << "doFindPixelPlaneFacets: keeping coincidence (2) "
// 		      << *(*t2).second << std::endl;
// 	    }
// #endif // DEBUG
// 	    got_exit = true;
// 	  }
// 	  else {
// #ifdef DEBUG
// 	    if(verboseplane) {
// 	      oofcerr << "doFindPixelPlaneFacets: deleting coincidence (2) "
// 		      << *(*t2).second << std::endl;
// 	    }
// #endif // DEBUG
// 	    delete_isec((*t2).second, eledgedata);
// 	  }
// 	}
//       }
//       else {
// 	for(CoordIsec::iterator t2=w; t2!=x; ++t2) {
// #ifdef DEBUG
// 	  if(verboseplane) {
// 	    oofcerr << "doFindPixelPlaneFacets: deleting coincidence (3) "
// 		    << *(*t2).second << std::endl;
// 	  }
// #endif // DEBUG
// 	  delete_isec((*t2).second, eledgedata);
// 	}
//       }
//     } // end if ct > 1
//     else {
//       // Key only occurs once, move on.
//       ++x;
//     }
//   } // end search for multiple coincident intersections at polygon corners

//   // Check for pairs of intersections on a single polygon edge that
//   // are within one voxel side length of one another.  The only way
//   // that this can happen is if the two vsb segments connect to each
//   // other.  If one intersection is an entry and the other is an exit,
//   // check that the parametric positions are in the right order along
//   // the edge.  (Misordered intersections can lead to the entire
//   // perimeter being added to the facet.)  Misordering can only be due
//   // to roundoff error, and the positions of the points should have
//   // been the same.  If both intersections are exits or entries, then
//   // one is superfluous and should be removed.  In either case, the
//   // positions of the intersections in the FacetEdges need to be
//   // adjusted so that FacetEdges join exactly and
//   // tetIntersectionFaceFacets works correctly.

//   for(unsigned int ni=0; ni<nn; ni++) { // loop over polygon edges
//     ElEdgeMap::iterator ii = eledgedata[ni].begin();
//     while(ii != eledgedata[ni].end()) {
//       // (*ii).second is a PixelBdyIntersection*
//       const Coord2D &pos0 = (*ii).second->location2D;
//       std::vector<ElEdgeMap::iterator> entries;
//       std::vector<ElEdgeMap::iterator> exits;
//       if((*ii).second->entry)
// 	entries.push_back(ii);
//       else
// 	exits.push_back(ii);
//       ElEdgeMap::iterator jj = ii;
//       ++jj;
//       bool done = false;
//       unsigned int nIntersects = 1;
//       while(jj != eledgedata[ni].end() && !done) {
// 	const Coord2D diff = pos0 - (*jj).second->location2D;
// 	if(fabs(diff[0]) < 1.0 && fabs(diff[1]) < 1.0) {
// 	  // The two points are within a pixel of each other.  They
// 	  // must be on contiguous VSB segments.
// 	  ++nIntersects;
// 	  if((*jj).second->entry)
// 	    entries.push_back(jj);
// 	  else
// 	    exits.push_back(jj);
// 	  ++jj;
// 	}
// 	else {
// 	  // The points are distinct.
// 	  done = true;
// 	}
//       }
//       ii = jj;			// ready for next intersection on this edge

//       if(nIntersects > 1) {
// #ifdef DEBUG
// 	if(verboseplane) {
// 	  oofcerr << "doFindPixelPlaneFacets: found coincidence.  entries="
// 		  << std::endl;
// 	  for(auto k=entries.begin(); k!=entries.end(); k++) {
// 	    OOFcerrIndent indent(2);
// 	    oofcerr << " " << *(*(*k)).second << std::endl;
// 	  }
// 	  oofcerr << "doFindPixelPlaneFacets:                       exits="
// 		  << std::endl;
// 	  for(auto k=exits.begin(); k!=exits.end(); k++) {
// 	    OOFcerrIndent indent(2);
// 	    oofcerr << " " << *(*(*k)).second << std::endl;
// 	  }
// 	}
// 	if(nIntersects != 2 && nIntersects != 4) {
// 	  throw ErrProgrammingError("Bad coincidence number! " +
// 				    to_string(nIntersects),
// 				    __FILE__, __LINE__);
// 	}
// #endif // DEBUG
// 	if(entries.size() == 1 && exits.size() == 1) {
// 	  // Check that the intersections occur in the correct order.
// 	  // If they don't, then they've been misplaced due to
// 	  // round-off error, and should actually coincide.  In fact,
// 	  // when this happens we can ignore the intersections
// 	  // entirely: they won't mark a point where an facet edge
// 	  // will start or end on the polygon boundary.

// 	  // If the two voxel set boundary segments make a right turn,
// 	  // we expect the entry point to be before the exit when
// 	  // traversing the polygon boundary (no matter which way the
// 	  // polygon boundary goes).  If they make a left turn, the
// 	  // exit must be before the entry.

// 	  PixelBdyIntersection *entryPt = (*entries.front()).second;
// 	  PixelBdyIntersection *exitPt = (*exits.front()).second;

// 	  // First find how the VSB segments that form the
// 	  // intersections are connected.  We need to know which one
// 	  // comes first when traversing the boundary.
// 	  const PixelBdyIntersection *firstPt =
// 	    firstIntersection(entryPt, exitPt);
// 	  const PixelBdyIntersection *secondPt =
// 	    (firstPt == entryPt ? exitPt : entryPt);
// 	  TurnDirection turn = turnDirection(firstPt, secondPt);
// 	  // TurnDirection turn = firstPt->loop.turnDirection(firstPt->loopseg);
// 	  assert(turn != STRAIGHT);
// #ifdef DEBUG
// 	  if(verboseplane) {
// 	    oofcerr << "doFindPixelPlaneFacets: firstPt=" << *firstPt
// 		    << " turn="
// 		    << (turn == LEFT ? "LEFT" : "RIGHT")
// 		    << " delta=" << entryPt->fraction - exitPt->fraction
// 		    << std::endl;
// 	  }
// #endif // DEBUG
// 	  if((turn == LEFT
// 	     && entryPt->fraction <= exitPt->fraction)
// 	     ||
// 	     (turn == RIGHT
// 	      && entryPt->fraction >= exitPt->fraction))
// 	    {
// 	      // The intersection points appear in the wrong order.
// 	      // They're actually just one point.  Remove the
// 	      // intersections from eledgedata, since they're not
// 	      // needed for the pixel plane facet.
// #ifdef DEBUG
// 	      if(verboseplane){
// 		oofcerr << "doFindPixelPlaneFacets: deleting coincidence (4) "
// 			<< entryPt->baryCoord << " " << exitPt->baryCoord
// 			<< std::endl;
// 	      }
// #endif // DEBUG
// 	      // If one of the points is on a tet edge, ignoring the
// 	      // infinitesimal segment that joins the other point to
// 	      // the edge may cause problems later in
// 	      // tetIntersectionFaceFacets(), because a sequence of
// 	      // connected edges on the face will not end at an edge.
// 	      // baryEquiv indicates that the point that's not on the
// 	      // edge is equivalent to the one that is, as far as
// 	      // tetIntersectionFaceFacets() is concerned.
// 	      bool onEdgeEntry = entryPt->baryCoord.onEdge();
// 	      bool onEdgeExit = exitPt->baryCoord.onEdge();
// 	      if(onEdgeEntry && !onEdgeExit)
// 		baryEquiv[exitPt->baryCoord] = entryPt->baryCoord;
// 	      else if(onEdgeExit && !onEdgeEntry)
// 		baryEquiv[entryPt->baryCoord] = exitPt->baryCoord;
	      
// 	      eledgedata[ni].erase(entries.front());
// 	      eledgedata[ni].erase(exits.front());

// 	      // It's also necessary to remove short edges from the
// 	      // PixelPlaneFacet, because if the points are in the
// 	      // wrong order the edges can make infinitesimal and
// 	      // incorrect negative contributions to the area.  (If
// 	      // those happen to be the only contributions to the
// 	      // area, then they'll lead to an incorrect negative area
// 	      // correction, below.)

// 	      // Short facet edges are only created when the VSB
// 	      // segments intersect at a point inside the polygon.  We
// 	      // know that only two VSB edges meet at this
// 	      // coincidence, so we can use the location of their
// 	      // intersection to identify the segments of the facet
// 	      // that should be deleted.
// 	      if(firstPt == entryPt) {
// 		ICoord2D meetingPt =
// 		  firstPt->loop.next_icoord(firstPt->loopseg);
// 		facet->removeEdgesAtPoint(pixplane.convert2Coord3D(meetingPt)
// // #ifdef DEBUG
// // 					  , verboseplane
// // #endif // DEBUG
// 					  );
// 	      }
// 	    }
// #ifdef DEBUG
// 	  else {
// 	    if(verboseplane)
// 	      oofcerr << "doFindPixelPlaneFacets: not removing coincidence"
// 		      << std::endl;
// 	  }
// #endif // DEBUG
// 	} // end if there is one entry and one exit

// 	else if(entries.size() == 2 && exits.size() == 2) {
// 	  // If there are two entries and two exits, the polygon edge
// 	  // must pass exactly through a point where two pixels are
// 	  // joined at a corner.  That point isn't the beginning or
// 	  // end of a polygon facet segment and can be ignored for the
// 	  // purposes of finding the facets in this pixel plane.  It
// 	  // also can't be an endpoint of a facet edge on a tet face.
// 	  for(auto p=entries.begin(); p!=entries.end(); ++p)
// 	    eledgedata[ni].erase(*p);
// 	  for(auto p=exits.begin(); p!=exits.end(); ++p)
// 	    eledgedata[ni].erase(*p);
// 	}

// 	else if(entries.size() == 2 && exits.empty()) {
// 	  // The end of one VSB segment and the start of the next
// 	  // both lie on the polygon edge.  One of the points is
// 	  // superfluous.  It doesn't matter which.
// 	  eledgedata[ni].erase(entries.back());
// #ifdef DEBUG
// 	  if(verboseplane)
// 	    oofcerr << "doFindPixelPlaneFacets: 2 entries" << std::endl;
// #endif // DEBUG
// 	}
// 	else if(exits.size() == 2 && entries.empty()) {
// 	  eledgedata[ni].erase(exits.front());
// #ifdef DEBUG
// 	  if(verboseplane)
// 	    oofcerr << "doFindPixelPlaneFacets: 2 exits" << std::endl;
// #endif // DEBUG
// 	}
	
//       }	// end if there are coincidences
//     }	// end loop over intersections on polygon edge
//   }	// end loop over polygon edges ni

// #endif // TWO_STAGE_COINCIDENCE_DETECTION

  // Done with coincidence checks
      
  
//  // commented out coincidence checker using sloppy comparison.
  
//   // Make a copy of coordisecs.  It contains the intersections that we
//   // have yet to examine for coincidences.  We're done when it's
//   // empty.
//   CoordIsec isecCopy(coordisecs);

//   // TODO: Since we're not looking up intersections by location in the
//   // map (because we're using sloppy comparison) we don't really need
//   // the CoordIsec structure at all.  Just a std::set of
//   // PixlBdyIntersection*s would suffice.  (Using sloppy Coord2D
//   // comparison as the Compare type in std::multimap doesn't work
//   // here.)  Do we still need sloppy comparisons?  Does the new
//   // find_two_intersections eliminate the need for them?  Do we still
//   // need to check for coincidences? 

//   // TODO: This is an o(n^2) process, where n is the number of
//   // intersections being checked.  Some creative hashing could make it
//   // faster, but n is pretty small, so maybe it's not necessary.


//   while(isecCopy.size() > 1) {
//     // coincidences is a vector of iterators that point to data in
//     // isecCopy.  Because isecCopy is a std::multimap, deleting an
//     // element does not invalidate other iterators, so we can use the
//     // iterators in coincidences to remove multiple objects from
//     // isecCopy.
//     std::vector<CoordIsec::iterator> coincidences;
//     coincidences.reserve(10);	// more than we'll need

//     // Pick an intersection point.
//     CoordIsec::iterator firstintersect = isecCopy.begin();
//     Coord2D firstpos = (*isecCopy.begin()).first;

//     // Look for other intersection points at nearly the same location,
//     // and keep track of how many are entrances and how many are
//     // exits.
//     int entries = 0;
//     int exits = 0;
//     for(CoordIsec::iterator nextintersect=isecCopy.begin();
// 	nextintersect!=isecCopy.end(); ++nextintersect)
//       {
// 	// This conditional is always true on the first pass through
// 	// the loop.
// 	if(nearby(firstpos, (*nextintersect).first)) {
// 	  coincidences.push_back(nextintersect);
// 	  if((*nextintersect).second->entry)
// 	    entries++;
// 	  else
// 	    exits++;
// 	}
//       } // end nextintersect loop

//     // Delete the extraneous intersections from coordisecs.
//     if(coincidences.size() > 1) {	// there are coincidences
// #ifdef DEBUG
//       int diff = entries - exits;
//       assert(diff == -1 || diff == 0 || diff == 1);
// #endif // DEBUG
//       if(entries > exits) {
// 	bool got_entry = false;
// 	for(std::vector<CoordIsec::iterator>::iterator i=coincidences.begin();
// 	    i!=coincidences.end(); ++i)
// 	  {
// 	    // Keep the first entry, and delete all the other
// 	    // coincident points from coordisecs and eledgedata.
// 	    if((**i).second->entry && !got_entry)
// 	      got_entry = true;
// 	    else
// 	      delete_isec((**i).second, eledgedata);
// 	    // Delete all of the coincident points, even the first
// 	    // entry, from isecCopy, so that we don't look at them
// 	    // again.
// 	    isecCopy.erase(*i);
// 	  }
//       }
//       else if(entries < exits) {
// 	bool got_exit = false;
// 	for(std::vector<CoordIsec::iterator>::iterator i=coincidences.begin();
// 	    i!=coincidences.end(); ++i)
// 	  {
// 	    if(!(**i).second->entry && !got_exit)
// 	      got_exit = true;
// 	    else
// 	      delete_isec((**i).second, eledgedata);
// 	    isecCopy.erase(*i);
// 	  }
//       }
//       else {
// 	// entries == exits, all cancel
// 	for(std::vector<CoordIsec::iterator>::iterator i=coincidences.begin();
// 	    i!=coincidences.end(); ++i)
// 	  {
// 	    delete_isec((**i).second, eledgedata);
// 	    isecCopy.erase(*i);
// 	  }

//       }
//     } // end if there are coincidences
//     else {
//       isecCopy.erase(firstintersect);
//     }
//   } // end while isecCopy is not empty

// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "doFindPixelPlaneFacets: done with coincidence detection"
//   	    << std::endl;
// #endif // DEBUG  

#ifdef DEBUG
  if(verboseplane) {
    oofcerr << "doFindPixelPlaneFacets: after coincidence check"
	    << std::endl;
    OOFcerrIndent indent(2);
    oofcerr << "doFindPixelPlaneFacets: facet= " << std::endl;
    for(std::set<FacetEdge>::const_iterator e=facet->begin();
	e!=facet->end(); ++e)
      {
	OOFcerrIndent indent(2);
	oofcerr << *e << std::endl;
      }
    for(unsigned int i=0; i<nn; i++) {
      if(!eledgedata[i].empty()) {
	oofcerr << "doFindPixelPlaneFacets: eledgedata[" << i <<"]="
		<< std::endl;
	std::cerr << eledgedata[i] << std::endl;
      }
    }
  }
#endif // DEBUG
  
  // Now traverse the boundary of the polygon, recording the
  // segments that are between an exit and an entry.  "exit" means
  // that the pixel set boundary segment is exiting the polygon.
  // (When the pixel set boundary is outside the polygon, the
  // boundary of the intersection follows the polygon.)

  int icount = 0;		     // number of intersections
  for(unsigned int n=0; n<nn; n++) { // loop over polygon edges
    icount += eledgedata[n].size();
  }

  if(icount > 0) {
#ifdef DEBUG
    if(verboseplane) {
      oofcerr << "doFindPixelPlaneFacets: finding missing polygon segments in "
	      << pixplane << std::endl;
    }
    OOFcerrIndent indent(2);
#endif	// DEBUG
    bool started = false;	// has the inner loop been started?
    for(unsigned int startedgeno=0;
	startedgeno<eledgedata.size() && !started; ++startedgeno)
      {
	const ElEdgeMap &edgemap = eledgedata[startedgeno];
	for(ElEdgeMap::const_iterator edgedatum=edgemap.begin();
	    edgedatum!=edgemap.end() && !started; ++edgedatum)
	  {
	    const PixelBdyIntersection *pbi = (*edgedatum).second;
	    if(!pbi->entry) {
	      // Exit point discovered.  Start traversing the polygon.
	      // This looks like a doubly nested loop, but it's
	      // not. The outer loops will exit after this inner loop
	      // is executed. 
	      started = true;
	      // bool done = false;
	      unsigned int edgeno = startedgeno;
	      Coord3D starting_point = pbi->location3D;
	      FacetCorner *exitpt =
		new FaceFacetCorner(pbi, pixplane, allCorners);
	      ElEdgeMap::const_iterator here = edgedatum;
	      ++here;
	      // eledgedata[edgeno].erase(edgedatum);
	      unsigned int handled = 1; // # of intersections dealt with
#ifdef DEBUG
	      if(verboseplane) {
		oofcerr << "doFindPixelPlaneFacets: initial corner= "
			<< *exitpt
			<< " starting edge=" << startedgeno
			<< std::endl;
	      }
#endif // DEBUG
	      while(handled < icount) {
#ifdef DEBUG
		if(verboseplane) {
		  oofcerr << "doFindPixelPlaneFacets: handled=" << handled
			  << " edgeno=" << edgeno
			  << " exitpt=";
		  if(exitpt)
		    oofcerr << *exitpt;
		  else
		    oofcerr << "None";
		  oofcerr << std::endl;
		}
#endif // DEBUG
		if(exitpt) {
		  // We've found a point, "exitpt", where the VSB
		  // boundary loop exits the polygon.  "here" points
		  // to the next intersection in the ElEdgeMap for the
		  // polygon edge containing exitpt.
		  if(here == eledgedata[edgeno].end()) {
		    // intersection bdy segment ends at polygon corner
#ifdef DEBUG
		    if(verboseplane) {
		      oofcerr << "doFindPixelPlaneFacets: going to next edge"
			      << std::endl;
		    }
#endif // DEBUG
		    edgeno = (edgeno + 1) % nn;
		    Coord3D cornerpt = (*tetPts)[edgeno].location3D(pixplane);
		    EdgeFacetCorner *crnr =
		      new EdgeFacetCorner((*tetPts)[edgeno], pixplane,
					  allCorners);
#ifdef DEBUG
		    std::string idstr =
		      "polygon edge to corner " + to_string(pixplane);
#endif // DEBUG
		    facet->addEdge(exitpt, crnr
#ifdef DEBUG
				   , idstr, verboseplane
#endif // DEBUG
				   );
		    // Go to next polygon edge/tet face
		    here = eledgedata[edgeno].begin();
		    // We already know the beginning of the next segment:
		    exitpt = new EdgeFacetCorner((*tetPts)[edgeno], pixplane,
						 allCorners);
		  }
		  else {	// not at the end of the edge
		    // Intersection bdy segment ends at entry on same edge
#ifdef DEBUG
		    if(verboseplane) {
		      oofcerr << "doFindPixelPlaneFacets: not at end of edge"
			      << std::endl;
		    }
#endif // DEBUG
		    // There may be more than one point here, from
		    // different VSB loops.
		    // TODO OPT: Is it worth handling the case when
		    // there's just a single intersection point
		    // separately?
		    double fraction = (*here).second->fraction;
		    if(verboseplane)
		      oofcerr << "doFindPixelPlaneFacets: fraction=" << fraction << std::endl;
		    int entryDiff = 0;
		    auto range = eledgedata[edgeno].equal_range(fraction);
		    int multiplicity = eledgedata[edgeno].count(fraction);
		    if(verboseplane)
		      oofcerr << "doFindPixelPlaneFacets: multiplicity="
			      << multiplicity << std::endl;
		    for(auto i=range.first; i!=range.second; i++) {
		      entryDiff += (*i).second->entry ? 1 : -1;
		    }
		    if(verboseplane)
		      oofcerr << "doFindPixelPlaneFacets: entryDiff="
			      << entryDiff << std::endl;
		    if(entryDiff == 0) {
		      // There are as many entries as exits.  Close
		      // the current segment and start the next.
		      FaceFacetCorner *crnr =
			new FaceFacetCorner((*here).second, pixplane,
					    allCorners);
#ifdef DEBUG
		      std::string idstr =
			"polygon edge to multiple entry " +
			to_string(pixplane);
#endif // DEBUG
		      facet->addEdge(exitpt, crnr
#ifdef DEBUG
				     , idstr, verboseplane
#endif // DEBUG
				     );
		      exitpt = crnr;
		    }	// end if entryDiff == 0
		    else if(entryDiff == 1) {
		      // There's one more entry than exits.  The
		      // current segment ends and no new one begins.
		      FaceFacetCorner *crnr =
			new FaceFacetCorner((*here).second, pixplane,
					    allCorners);
#ifdef DEBUG
		      std::string idstr = (multiplicity == 1 ?
					   "polygon edge to entry ":
					   ("polygon edge to multiple(" +
					    to_string(multiplicity) +
					    ") entry "))
			+ to_string(pixplane);
#endif // DEBUG
		      facet->addEdge(exitpt, crnr
#ifdef DEBUG
				     , idstr, verboseplane
#endif // DEBUG
				     );
		      exitpt = 0;
		    }
		    else {
		      throw ErrProgrammingError("Incorrect entry/exit count!",
						__FILE__, __LINE__);
		    }
		    here = range.second;
		    handled += multiplicity;
		    // eledgedata[edgeno].erase(range.first, range.second);
		    
		  }   // end if not at the end of the edge
		} // end if exitpt (ie, we're looking for the next entry)
		else {
		  // exitpt == 0.  Look for the next exit point.
		  if(here == eledgedata[edgeno].end()) {
		    // go to the next polygon edge/tet face
		    edgeno = (edgeno + 1) % nn;
		    here = eledgedata[edgeno].begin();
		  }
		  else {	// not at the end of the edge
		    double fraction = (*here).second->fraction;
		    int entryDiff = 0;
		    auto range = eledgedata[edgeno].equal_range(fraction);
		    int multiplicity = eledgedata[edgeno].count(fraction);
		    for(auto i=range.first; i!=range.second; ++i) {
		      entryDiff += (*i).second->entry ? 1 : -1;
		    }
		    if(entryDiff == -1) {
		      // There's one more exit than entry.  A new
		      // segment starts here.
		      exitpt = new FaceFacetCorner((*here).second,
						   pixplane, allCorners);
		      // eledgedata[edgeno].erase(range.first, range.second);
		      here = range.second;
		      handled += multiplicity;
		    }
		    else {
		      throw ErrProgrammingError("Incorrect entry/exit count!",
						__FILE__, __LINE__);
		    }
		  }
		} // end if exitpt else
	      }	  // end while handled < icount
	    }	  // end if found initial exit point
	  }	  // end search over edge for initial exit point
      } // end search over edges startedgeno for initial exit point
    
    // If started is still false, no initial exit point was found,
    // although we know there are intersections.
    if(!started)
      throw ErrProgrammingError("No exit.", __FILE__, __LINE__);
    
  }   // end if icount > 0 (ie, there are intersections)

//   // Although coincident points have been eliminated, there can still
//   // be leftover short edges in the PixelPlaneFacet.  Remove them.
//   // Also remove hairpin turns.  THIS RELIES ON TOLERANCES AND
//   // SHOULDN'T BE NEEDED.

// #ifdef CLEANUP
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "doFindPixelPlaneFacets: calling cleanUp for "
//   	    << pixplane << " category=" << category << std::endl;
// #endif // DEBUG
//   facet->cleanUp(pixplane, allCorners, epts, baryCache
//  #ifdef DEBUG
// 		 , verboseplane
// #endif // DEBUG
// 		 );
// #endif // CLEANUP
  
  if(icount == 0) {

    // If there are no intersections, we either need to include all of
    // the tetPts polygon, or none of it.
    //
    // If the polygon encloses a loop of the set boundary, the
    // boundary edges will already have been included in the
    // intersection facet, and we don't have to do anything.  The
    // area of the facet computed from the current set of edges is
    // positive.
    //
    // If the polygon is entirely inside a loop, but there are
    // holes within the polygon (ie, the boundary the voxel set
    // lying in this plane is annular and the polygon edges lie
    // within the annulus and surround the hole), then the entire
    // boundary must be included.  The area computed so far will
    // be *negative*, because it's made up of holes.
    //
    // If the polygon is entirely inside a boundary loop and there
    // are no holes in the pixel set within the polygon, the
    // polygon is homogeneous and its entire boundary is the
    // entire intersection boundary.
    //
    // A big difference between this code and the categoryAreas
    // calculation in 2D is that it's possible for the polygon
    // here to be homogeneous and lie within the voxel category
    // but *not* delimit a boundary facet of the intersection
    // volume.

    double area = facet->area(verboseplane);
// #ifdef DEBUG
//     if(verboseplane)
//       oofcerr << "doFindPixelPlaneFacets: area=" << area
//     	  << " category=" << category
//     	  << " pixplane=" << pixplane << std::endl;
// #endif  // DEBUG
    bool homogeneous = false;
    if(area == 0.) {
      // If any interior point of the polygon is inside the voxel
      // category, the whole polygon must be inside the loop, and is
      // homogeneous.  To determine if a point is inside the category,
      // compute the winding number of the category's loops around a
      // point thats inside the polygon.
      
      // NOTE: The polygon can be homogeneous and inside the voxel
      // category, but not be inside a facet loop.  In this case it's
      // *not* a facet of the intersection volume and should not be
      // included, unless it's also a face of the tetrahedron.  That's
      // why when a tet face is in the plane we use the loops bounding
      // the voxel set cross section, not the voxel set facets.

      // The winding number calculation is easier if the interior
      // point is known not to coincide with any loop components.  The
      // loop segments are orthogonal and lined up on integer
      // coordinates, so pick a non-integer interior point.
      Coord2D testpt = nonIntegerInteriorPt(*tetCoords);
      int windingNumber = 0;
      for(std::vector<PixelBdyLoop*>::const_iterator pbl=loops.begin();
	  pbl!=loops.end(); ++pbl)
	{
	  windingNumber += (*pbl)->windingNumber(testpt);
	}
      homogeneous = windingNumber == 1;
    } // end if area == 0
#ifdef DEBUG
    if(verboseplane)
      oofcerr << "doFindPixelPlaneFacets: homogeneous=" << homogeneous
	      << " area=" << area << std::endl;
#endif // DEBUG
    if(homogeneous || area < 0.0) {
#ifdef DEBUG
      std::string msg = (area < 0.0 ? "negative area correction "
			 : "homogeneous pixplane ");
#endif // DEBUG
      for(unsigned int i=0; i<nn-1; i++) {
	facet->addEdge(new EdgeFacetCorner((*tetPts)[i], pixplane, allCorners),
		       new EdgeFacetCorner((*tetPts)[i+1], pixplane, allCorners)
#ifdef DEBUG
		       , msg + to_string(pixplane),
		       verboseplane
#endif // DEBUG
		       );
      }
      facet->addEdge(new EdgeFacetCorner(tetPts->back(), pixplane, allCorners),
		     new EdgeFacetCorner((*tetPts)[0], pixplane, allCorners)
#ifdef DEBUG
		     , msg + to_string(pixplane),
		     verboseplane
#endif // DEBUG
		     );
    } // end if homogeneous or facet area < 0
  }   // end if there are no intersections
}     // end doFindPixelPlaneFacets()

//=\\=//=\\=//

void findPixelPlaneFacets(const CMicrostructure *ms,
			  const VoxelSetBoundary &vsb,
			  const std::vector<Coord3D> &epts,
			  const ICRectangularPrism &iBounds,
			  unsigned int category,
#ifdef DEBUG
			  bool verbose,
#endif	// DEBUG
			  FacetMap2D &facets,
			  BaryCoordMap &baryEquiv,
			  FacetCornerList &allCorners,
			  std::vector<bool> &didFace,
			  TetPlaneIntersectionCache &tetPlaneIntCache,
			  BaryCoordCache &baryCache
			  )
{
#ifdef DEBUG
  bool verbosecategory = verboseCategory(verbose, category);
  if(verbose) {
    openDumpFile("epts");
    for(unsigned int i=0; i<3; i++)
      for(unsigned int j=i+1; j<4; j++)
    	dumpSegment(epts[i], epts[j]);
    closeDumpFile();
  }
#endif // DEBUG

  // Determine which faces of the tet lie on pixel planes.
  // TODO: These vecs should be stored in HomogeneityTet.
  std::vector<const PixelPlane*> facePlaneVec(4, NULL);
  std::set<PixelPlane> facePlaneSet;
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    PixelPlane pixplane;
    if(faceIsOnVoxelPlane(f, epts, pixplane)) {
      std::pair<std::set<PixelPlane>::iterator, bool> ii = facePlaneSet.insert(pixplane);
      facePlaneVec[f] = &(*ii.first);
    }
  }

  // Loop over planes of voxels (pixel planes)

  // Find the pixel planes to loop over, and the PixelBdyLoops in each
  // plane.  The planes are the planes of the VoxelSetBoundary loops,
  // plus the planes of the faces of the tet, if those faces lie on
  // pixel planes, whether or not those pixel planes contain
  // VoxelSetBoundary loops.

  const PixelSetBoundaryMap &pxlSetBdys = vsb.getPixelSetBdys();

  // Do the tet planes first.
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    if(facePlaneVec[f] != NULL) {
      const PixelPlane &pixplane = *facePlaneVec[f];
      // When the pixel plane coincides with an element face, use the
      // entire perimeter of the set of pixels in the pixel plane, not
      // just the ones that are on external facets of the voxel set.
#ifdef DEBUG
      bool verboseplane = verbosePlane(verbosecategory, pixplane);
#endif // DEBUG
      const std::vector<PixelBdyLoop*> &csloops = vsb.getPlaneCS(pixplane,
								 category
#ifdef DEBUG
							       , verboseplane
#endif // DEBUG
								 );
      std::vector<PixelBdyLoop*> loops(csloops);
      // Add the vsb facet loops to the cross section.
      PixelSetBoundaryMap::const_iterator psbmi = pxlSetBdys.find(pixplane);
      if(psbmi != pxlSetBdys.end()) {
	const std::vector<PixelBdyLoop*> &floops = (*psbmi).second->get_loops();
	loops.insert(loops.end(), floops.begin(), floops.end());
      }
#ifdef DEBUG
      if(verboseplane) {
      	oofcerr << "findPixelPlaneFacets: using cross section loops for "
      		<< pixplane << std::endl;
	oofcerr << "findPixelPlaneFacets: found " << loops.size() << " loop"
		<< (loops.size()==1?"":"s") << std::endl;
	for(unsigned int i=0; i<loops.size(); ++i) {
	  oofcerr << "findPixelPlaneFacets: loop[" << i << "]="
		  << *loops[i] << std::endl;
	}
      }
#endif // DEBUG
      doFindPixelPlaneFacets(pixplane, loops, epts, iBounds, f,
			     facePlaneVec, category,
#ifdef DEBUG
			     verboseplane,
#endif // DEBUG
			     facets, baryEquiv, allCorners,
			     tetPlaneIntCache, baryCache);
      // facePlaneSet.insert(pixplane);
      didFace[f] = true;
    }
  } // end loop over faces f

  // Look at the pixel planes that don't coincide with tet faces.
  
  for(PixelSetBoundaryMap::const_iterator psbm=pxlSetBdys.begin();
      psbm!=pxlSetBdys.end(); ++psbm)
    {
      const PixelPlane &pixplane = (*psbm).first;
      if(facePlaneSet.count(pixplane) == 0) {
	const PixelSetBoundary *psb = (*psbm).second;
	doFindPixelPlaneFacets(pixplane, psb->get_loops(), epts, iBounds,
			       NONE, facePlaneVec, category,
#ifdef DEBUG
			       verbose,
#endif // DEBUG
			       facets, baryEquiv, allCorners,
			       tetPlaneIntCache, baryCache);
      }
    } // end loop over pixel set boundarys

#ifdef DEBUG
  if(verbosecategory) {
    openDumpFile("pixelplanefacets" + to_string(category));
    oofcerr << "findPixelPlaneFacets: final pixel plane facets for category "
	    << category << std::endl;
    OOFcerrIndent indent(2);
    for(FacetMap2D::const_iterator fmi=facets.begin(); fmi!=facets.end(); ++fmi)
      {
	if(!(*fmi).second->empty()) {
	  oofcerr << (*fmi).first << std::endl;
	  OOFcerrIndent indent(2);
	  for(std::set<FacetEdge>::const_iterator e=(*fmi).second->begin();
	      e!=(*fmi).second->end(); ++e)
	    {
	      oofcerr << *e << std::endl;
	      // oofcerr << "      " << (*e).start->bcoord() << " "
	      // 	      << (*e).end->bcoord() << std::endl;
	      dumpSegment((*e).start->position3D(), (*e).end->position3D());
	    }
	}
      }
    closeDumpFile();
  }
#endif // DEBUG
}     // end findPixelPlaneFacets()


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Class that represents the intersection of a facet edge with the
// edge of a tet face (ie, a facet corner that lies on the edge of a
// tet face).

class FaceEdgeIntersection {
private:
  const FacetCorner *crnr;
  unsigned int fEdge;		// face index of intersected tet edge
  double t;			// parametric position along tet edge
public:
  const std::set<FacetEdge>::const_iterator edge;
  const bool start;		// is this the start of a segment?
  FaceEdgeIntersection(const FacetCorner *crnr,
		       const std::set<FacetEdge>::const_iterator edge,
		       bool start)
    : crnr(crnr),
      fEdge(NONE),
      edge(edge),
      start(start)
  {}
  // position3D() can't return a reference because some versions of
  // FacetCorner::position3D() return an object, not a reference.
  const Coord3D position3D() const { return crnr->position3D(); }
  const BarycentricCoord &bcoord() const { return crnr->bcoord(); }
  const FacetCorner *corner() const { return crnr; }
  unsigned int faceEdge() const { return fEdge; }
  double edgePosition() const { return t; }

  // findEdge finds which edge the intersection is on and its position
  // along the edge. 
  void findEdge(unsigned int f, const BaryCoordMap &baryEquiv
#ifdef DEBUG
		, bool verbose
#endif // DEBUG
		)
  {
    if(!find_edge(crnr->bcoord(), f,
#ifdef DEBUG
		  verbose,
#endif // DEBUG
		  t, fEdge))
      {
	BaryCoordMap::const_iterator bcmi = baryEquiv.find(crnr->bcoord());
	if(bcmi != baryEquiv.end()) {
	  if(!find_edge((*bcmi).second, f,
#ifdef DEBUG
			verbose,
#endif // DEBUG
			t, fEdge))
	    {
#ifdef DEBUG
	      if(verbose) {
		oofcerr << "FaceEdgeIntersection::findEdge: baryEquiv replacement failed: "
			<< crnr->bcoord() << " --> " << (*bcmi).second
			<< std::endl;
	      }
#endif
	      fEdge = NONE;
	    }
#ifdef DEBUG
	  else if(verbose) {
	    oofcerr << "FaceEdgeIntersection::findEdge: successfully used baryEquiv: "
		    << crnr->bcoord() << " --> " << (*bcmi).second
		    << " fEdge=" << fEdge << std::endl;

	  }
#endif // DEBUG
	}
	else {
	  fEdge = NONE;
	  // throw ErrProgrammingError("FaceEdgeIntersection::findEdge failed!",
	  // 			  __FILE__, __LINE__);
	}
      }
  }
};

typedef std::multimap<double, FaceEdgeIntersection> LooseEndMap;

std::ostream &operator<<(std::ostream &os, const FaceEdgeIntersection &fei) {
  os << "FaceEdgeIntersection(" << *fei.corner()
     << ", t=" << fei.edgePosition()
     << ", edge=" << *fei.edge
     << ", start=" << fei.start
     << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// mergeLooseEnds removes a loose start or end from the given sets of
// FaceEdgeIntersections, when it's known that there's at least one
// extra one.

static bool mergeLooseEnds(std::vector<LooseEndMap> &looseEnds, bool start) {
  double smallestDist = std::numeric_limits<double>::max();
  unsigned int edge = NONE;
  LooseEndMap::iterator deleteMe;
  
  for(unsigned int e=0; e<looseEnds.size(); e++) {
    LooseEndMap &lem = looseEnds[e];
    LooseEndMap::iterator i = lem.begin();
    if(i != lem.end()) {
      LooseEndMap::iterator prev = i;
      i++;
      for( ; i!=lem.end(); ++i) {
	if((*i).second.start == start && (*prev).second.start == start &&
	   (*i).first - (*prev).first < smallestDist)
	  {
	    smallestDist = (*i).first - (*prev).first;
	    deleteMe = i;
	    edge = e;
	  }
	prev = i;
      }
    }
  }
  if(edge != NONE) {
    looseEnds[edge].erase(deleteMe);
    return true;
  }
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Compute the facets of the intersection volume of a tetrahedral
// element and a voxel category.  This computes only the facets that
// lie on facees of the tetrahedron.  The facets that lie on pixel
// planes (planes aligned with the voxel axes at the boundary between
// two planes of voxels) have already been computed and are provided
// by the "facets" arg.  The "didFace" arg indicates whether or not a
// face of the tet has already been computed (ie, if it lies in a
// pixel plane).

void tetIntersectionFaceFacets(
		       const VoxelSetBoundary &vsb, 
		       const std::vector<Coord3D> &epts,
		       const ICRectangularPrism &iBounds,
		       const FacetMap2D &facets,
		       const BaryCoordMap &baryEquiv,
		       FacetCornerList &allCorners,
		       BaryCoordCache &baryCache,
		       const std::vector<bool> &didFace,
		       unsigned int category,
#ifdef DEBUG
		       bool verbose,
#endif // DEBUG
		       std::vector< std::set<FacetEdge> > &faceFacetEdges)
{
  try {
#ifdef DEBUG
    bool verbosecategory = verboseCategory(verbose, category);
    if(verbosecategory) {
      oofcerr << "tetIntersectionFaceFacets: category=" << category
	      << std::endl;
      oofcerr << "tetIntersectionFaceFacets: baryEquiv=[";
      std::cerr << baryEquiv;
      oofcerr << "]" << std::endl;
    }
#endif // DEBUG

    faceFacetEdges.clear();

    // Loop over pixel plane facets, sorting the edges that cross tet
    // faces by face.
    for(FacetMap2D::const_iterator fm=facets.begin(); fm!=facets.end(); ++fm) {
      const PixelPlaneFacet *facet = (*fm).second;
      #ifdef DEBUG
      if(verbosecategory && !facet->empty())
	oofcerr << "tetIntersectionFaceFacets: sorting segments from facet "
		<< (*fm).first << std::endl;
      #endif // DEBUG
      // edge is a std::set<FacetEdge>::const_iterator
      for(auto edge=facet->begin(); edge!=facet->end(); ++edge) {
	OOFcerrIndent indent(2);
	// Find which faces the edge is on.
	BarycentricCoord bStart = (*edge).start->bcoord();
	BarycentricCoord bEnd = (*edge).end->bcoord();
	for(unsigned int ff=0; ff<NUM_TET_FACES; ++ff) {
	  if(!didFace[ff]) {
	    unsigned int n = CSkeletonElement::oppNode[ff];
	    if(bStart[n] == 0.0 && bEnd[n] == 0.0) {
#ifdef DEBUG
	      if(verbosecategory) {
		oofcerr << "tetIntersectionFaceFacets: adding "
			<< (*edge).reversed() << " to face " << ff
			<< std::endl;
	      }
	      if(faceFacetEdges[ff].count((*edge).reversed()) != 0) {
		oofcerr << "tetIntersectionFaceFacets: duplicate edge!"
			<< std::endl;
		oofcerr << "                             new edge: "
			<< (*edge).reversed() << std::endl;
		oofcerr << "                             old edge: "
			<< *faceFacetEdges[ff].find((*edge).reversed())
			<< std::endl;
		throw ErrProgrammingError("Duplicate edge!",
					  __FILE__, __LINE__);
	      }
#endif // DEBUG
	      faceFacetEdges[ff].insert((*edge).reversed());
	    }
	  }
	}
      }	// end loop over facet edges

      // This version only includes segments that cross a face.  The
      // version above also includes segments that lie on edges of a
      // face, and it puts them on both faces.
      
// 	unsigned int ff = NONE;
// 	if(findCrossedFace((*edge).start->bcoord(), (*edge).end->bcoord(),
// #ifdef DEBUG
// 			   verbosecategory,
// #endif // DEBUG
// 			   ff))
// 	  {
// 	    if(!didFace[ff]) {
// #ifdef DEBUG
// 	      if(verbosecategory) {
// 		oofcerr << "tetIntersectionFaceFacets: adding "
// 			<< (*edge).reversed() << " to face " << ff
// 			<< std::endl;
// 	      }
// 	      if(faceFacetEdges[ff].count((*edge).reversed()) != 0) {
// 		oofcerr << "tetIntersectionFaceFacets: duplicate edge!"
// 			<< std::endl;
// 		oofcerr << "                             new edge: "
// 			<< (*edge).reversed() << std::endl;
// 		oofcerr << "                             old edge: "
// 			<< *faceFacetEdges[ff].find((*edge).reversed())
// 			<< std::endl;
// 		throw ErrProgrammingError("Duplicate edge!",
// 					  __FILE__, __LINE__);
// 	      }
// #endif // DEBUG
// 	      faceFacetEdges[ff].insert((*edge).reversed());
// 	    }
// 	  }
// #ifdef DEBUG
// 	else {
// 	  if(verbosecategory) {
// 	    oofcerr << "tetIntersectionFaceFacets: edge " << *edge
// 		    << " is not on a face" << std::endl;
// 	  }
// 	}
// #endif // DEBUG
//       }	// end loop over facet edges
    } // end loop over facets

#ifdef DEBUG
    if(verbosecategory) {
      oofcerr << "tetIntersectionFaceFacets: didFace=";
      std::cerr << didFace;
      oofcerr << std::endl;
  
      oofcerr << "tetIntersectionFaceFacets: sorted faceFacetEdges before looking for missing segments: "
	      << std::endl;
      for(unsigned int f=0; f<NUM_TET_FACES; f++) {
	if(!faceFacetEdges[f].empty()) {
	  oofcerr << "     face " << f << ": " << std::endl;
	  for(const auto &k : faceFacetEdges[f])
	    oofcerr << "          " << k << std::endl;
	}
      }
    }
#endif // DEBUG

    // Loop over tet faces, constructing a polygon on the face from the
    // unmatched edges found above.  There may be missing segments, but
    // only along the edges of the original tet.  Add those segments if
    // necessary. 

    for(unsigned int f=0; f<NUM_TET_FACES; f++) {
      std::set<FacetEdge> &facetEdges = faceFacetEdges[f];

      if(!didFace[f]) {
#ifdef DEBUG
	if(verbosecategory)
	  oofcerr << "tetIntersectionFaceFacets: finding face facets, face=" << f
		  << " category=" << category << std::endl;
	OOFcerrIndent indent(2);
	if(verbosecategory) {
	  oofcerr << "tetIntersectionFaceFacets: faceNodes=";
	  std::cerr << faceNodes(f, epts);
	  oofcerr<< std::endl;
	}
#endif // DEBUG

	// TODO: facenormal should be precomputed in tet class
	Coord3D facenormal = faceNormal(f, epts);

	// Look for loose ends (and starts).

	std::vector<FaceEdgeIntersection> startPoints;
	std::vector<FaceEdgeIntersection> endPoints;
	unsigned int nsegs = facetEdges.size();
	startPoints.reserve(nsegs);
	endPoints.reserve(nsegs);
	for(std::set<FacetEdge>::const_iterator seg=facetEdges.begin();
	    seg!=facetEdges.end(); ++seg)
	  {
	    startPoints.push_back(
				FaceEdgeIntersection((*seg).start, seg, true));
	    endPoints.push_back(
				FaceEdgeIntersection((*seg).end, seg, false));
	  }
	// matchedStarts and matchedEnds indicate which segment start
	// and end points have been paired up.  The loose ones that
	// haven't been paired will be used to construct the missing
	// segments.
	std::vector<bool> matchedStarts(nsegs, false);
	std::vector<bool> matchedEnds(nsegs, false);
	for(unsigned int s=0; s<nsegs; s++) {
	  const Coord3D &sp = startPoints[s].position3D();
	  const BarycentricCoord &sb = startPoints[s].bcoord();
	  for(unsigned int e=0; e<nsegs; e++) {
	    // Compare both barycentric coords and cartesian coords to
	    // avoid round off errors.
	    if(e!=s && !matchedEnds[e] &&
	       (sb==endPoints[e].bcoord() || sp==endPoints[e].position3D()))
	      {
		matchedEnds[e] = true;
		matchedStarts[s] = true;
		break;
	      }
	  } // end loop over end points e
	}   // end loop over start points s
#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "tetIntersectionFaceFacets: found matches" << std::endl;
	  // oofcerr << "tetIntersectionFaceFacets: startPoints=" << std::endl;
	  // for(auto &pt : startPoints) {
	  //   OOFcerrIndent  indent(2);
	  //   oofcerr << pt << std::endl;
	  // }
	  // oofcerr << "tetIntersectionFaceFacets: endPoints=" << std::endl;
	  // for(auto &pt : endPoints) {
	  //   OOFcerrIndent  indent(2);
	  //   oofcerr << pt << std::endl;
	  // }
	  // oofcerr << "tetIntersectionFaceFacets: matchedStarts= ";
	  // std::cerr << matchedStarts;
	  // oofcerr << std::endl;
	  // oofcerr << "tetIntersectionFaceFacets:   matchedEnds= ";
	  // std::cerr << matchedEnds;
	  // oofcerr << std::endl;
	}
#endif // DEBUG
	// All of the unmatched points must be on tet edges.  Sort
	// them by edge and intersection position along the edge.
	std::vector<LooseEndMap> looseEnds(NUM_TET_FACE_EDGES);
	for(unsigned int i=0; i<nsegs; i++) {
	  if(!matchedStarts[i]) {
	    startPoints[i].findEdge(f, baryEquiv
#ifdef DEBUG
				    , verbose
#endif // DEBUG
				    );
	    unsigned int e = startPoints[i].faceEdge();
	    if(e != NONE)
	      looseEnds[e].insert(
			  LooseEndMap::value_type(startPoints[i].edgePosition(),
						  startPoints[i]));
	  }
	  if(!matchedEnds[i]) {
	    endPoints[i].findEdge(f, baryEquiv
#ifdef DEBUG
				  , verbose
#endif // DEBUG
				  );
	    unsigned int e = endPoints[i].faceEdge();
	    if(e != NONE)
	      looseEnds[e].insert(
			  LooseEndMap::value_type(endPoints[i].edgePosition(),
						  endPoints[i]));
	  }
	}
#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "tetIntersectionFaceFacets: sorted loose ends"
		  << std::endl;
	  for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	    oofcerr << "tetIntersectionFaceFacets: edge=" << e << std::endl;
	    OOFcerrIndent indent(2);
	    for(LooseEndMap::iterator le=looseEnds[e].begin();
		le!=looseEnds[e].end(); ++le)
	      {
		oofcerr << "   " << (*le).first
			<< " (x" << looseEnds[e].count((*le).first) << ") "
			<< ": "
			<< (*le).second << std::endl;
	      }
	      
	  }
	}
#endif // DEBUG

// 	// Because the baryEquiv mapping may have created zero length
// 	// edges, there may be multiple starts and ends at a single
// 	// point.  Remove them, as long as they're sensible.
// 	for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
// 	  LooseEndMap &lem = looseEnds[e];
// 	  LooseEndMap::iterator x = lem.begin();
// 	  while(x != lem.end()) {
// 	    double t = (*x).first; // parametric position along the edge
// 	    unsigned int count = lem.count(t);
// 	    if(count > 1) {
// 	      std::pair<LooseEndMap::iterator, LooseEndMap::iterator> range =
// 		lem.equal_range(t);
// 	      // stopsign is the number of starting points minus the
// 	      // number of stopping points at this t.
// 	      int stopsign = 0;
// 	      for(auto k=range.first; k!=range.second; ++k) {
// 		stopsign += (*k).second.start ? 1 : -1;
// 	      }
// 	      if(stopsign == 0) {
// 		x = range.second;
// 		lem.erase(range.first, range.second);
// 	      }
// 	      else {
// 		// There are different numbers of starts and stops.
// 		// In most cases, there will be one more of one than
// 		// the other, but if round-off error has caused two
// 		// PixelPlaneFacets to intersect by a tiny amount,
// 		// there can be two starts or two stops and none of
// 		// the other.  In this case, the correct thing to do
// 		// is to ignore all but one.
// #ifdef DEBUG
// 		if(stopsign > 2 || stopsign < -2) {
// 		  throw ErrProgrammingError(
// 			    "Invalid value: stopsign=" + to_string(stopsign),
// 			    __FILE__, __LINE__);
// 		}
// #endif // DEBUG
// 		bool keepstart = stopsign > 0;
// 		bool found_one = false;
// 		for(auto k=range.first; k!=range.second; ++k) {
// 		  if((*k).second.start == keepstart && !found_one) {
// 		    found_one = true;
// 		  }
// 		  else {
// 		    lem.erase(k);
// 		  }
// 		}
// 		x = range.second;
// 	      }	// end if stopsign != 0
// 	    }
// 	    else {		// count == 1
// 	      ++x;
// 	    }
// 	  }
// 	} // end loop over edges, removing multiple starts and ends
	
	// Look for near coincidences due to round-off error.  These
	// are a problem if a loose end that's supposed to coincide
	// with a loose start has an edgePosition that's slightly
	// after the start.
	for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	  // oofcerr << "tetIntersectionFaceFacets: e=" << e
	  // 	  << " looseEnds[e].size()=" << looseEnds[e].size()
	  // 	  << std::endl;
	  LooseEndMap::iterator x = looseEnds[e].begin();
	  while(x != looseEnds[e].end()) {
	    LooseEndMap::iterator xnext = x;
	    xnext++;
	    bool didit = false;
	    if(xnext != looseEnds[e].end()) {
// #ifdef DEBUG
// 	      if(verbosecategory) {
// 		oofcerr << "tetIntersectionFaceFacets: checking coincidence at "
// 			<< std::endl
// 			<< "tetIntersectionFaceFacets:   " 
// 			<< (*x).first << ":" << (*x).second << std::endl
// 			<< "tetIntersectionFaceFacets:   "
// 			<< (*xnext).first << ":" << (*xnext).second << std::endl
// 			<< "tetIntersectionFaceFacets: delta="
// 			<< (*xnext).first - (*x).first << std::endl;
// 	      }
// #endif // DEBUG
	      if((*xnext).second.edgePosition() -
		 (*x).second.edgePosition() < 0.5)
		// THIS ISN'T THE RIGHT COMPARISON. edgePosition is
		// relative to edge length.
		{
		  // Two points are within a pixel size of each other
		  // and can potentially coincide.
		  if((*x).second.start != (*xnext).second.start) {
		    // x is the start (end) of a facet segment that
		    // lies in the face and has an endpoint on an edge
		    // of the face, and xnext is the end (start) of
		    // another such facet segment.  xnext's endpoint
		    // is just past x's on the facet edge.

		    // If round-off error has put the edge
		    // intersections in the wrong order, then segments
		    // will intersect.  Since facet segments can't
		    // cross, we can tell if the ordering is
		    // incorrect.

		    // a0 and b0 are the endpoints of x and xnext that
		    // lie on the facet edge.  
		    Coord3D a0, a1, b0, b1;
		    const FacetEdge &edgeA = *(*x).second.edge;
		    const FacetEdge &edgeB = *(*xnext).second.edge;
		    if((*x).second.start) {
		      a0 = edgeA.start->position3D();
		      b0 = edgeB.end->position3D();
		      a1 = edgeA.end->position3D();
		      b1 = edgeB.start->position3D();
		    }
		    else {
		      a1 = edgeA.start->position3D();
		      b1 = edgeB.end->position3D();
		      a0 = edgeA.end->position3D();
		      b0 = edgeB.start->position3D();
		    }
		    // We know that b0 lies to the right of (a0,a1)
		    // and that a0 lies to the left of (b0, b1).  If
		    // the segments cross, then b1 must lie to the
		    // left of (a0,a1) and a1 to the right of (b0,b1),
		    // which is what these cross products check:
		    if(dot(cross(a1-a0, b1-a0), facenormal) > 0.0 &&
		       dot(cross(b1-b0, a1-b0), facenormal) < 0.0)
		      {
			LooseEndMap::iterator xtemp = xnext;
			++xtemp;
// #ifdef DEBUG
// 			if(verbosecategory) {
// 			  oofcerr << "tetIntersectionFaceFacets: erasing loose end at " << *x << std::endl;
// 			  oofcerr << "tetIntersectionFaceFacets: erasing loose end at " << *xnext << std::endl;
// 			}
// #endif // DEBUG
			looseEnds[e].erase(x);
			looseEnds[e].erase(xnext);
			x = xtemp;
			didit = true;
		      }
		  } // end if x is a segment start and xnext is an end
		}   // end if points are within a pixel of each other
	    }	    // end if xnext is not off the end of the list
	    if(!didit)
	      x = xnext;
	  } // end loop over looseEnds on edge e
	}   // end loop over edges e

#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "tetIntersectionFaceFacets: loose ends after removing coincidences"
		  << std::endl;
	  for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	    oofcerr << "tetIntersectionFaceFacets: edge=" << e << std::endl;
	    OOFcerrIndent indent(2);
	    for(LooseEndMap::iterator le=looseEnds[e].begin();
		le!=looseEnds[e].end(); ++le)
	      {
		oofcerr << "   " << (*le).first << ": "
			<< (*le).second << std::endl;
	      }
	      
	  }
	}
#endif // DEBUG

	// Check that the number of loose starts and ends match
	int nStarts = 0;
	int nEnds = 0;
	for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	  LooseEndMap &lem = looseEnds[e];
	  for(LooseEndMap::const_iterator i=lem.begin(); i!=lem.end(); ++i) {
	    if((*i).second.start)
	      nStarts++;
	    else
	      nEnds++;
	  }
	}
	if(nStarts != nEnds) {
	  // This can happen if a coincidence was resolved on one
	  // pixel plane but not on another.  In that case there can
	  // be two starts (or ends) at nearly identical positions,
	  // one of which should be removed.
#ifdef DEBUG
	  if(verbosecategory) {
	    oofcerr << "tetIntersectionFaceFacets: loose ends don't match!"
		    << " nStarts=" << nStarts << " nEnds=" << nEnds
		    << std::endl;
	  }
#endif // DEBUG
	  if(nStarts > nEnds) {
	    while(nStarts > nEnds) {
	      if(mergeLooseEnds(looseEnds, true))
		--nStarts;
	      else {
		oofcerr << "tetIntersectionFaceFacets: failed to resolve loose end mismatch" << std::endl;
		throw ErrProgrammingError("mergeLooseEnds failed! start=true",
					  __FILE__, __LINE__);
	      }
	    }
	  }
	  else {
	    while(nEnds > nStarts) {
	      if(mergeLooseEnds(looseEnds, false))
		--nEnds;
	      else {
		oofcerr << "tetIntersectionFaceFacets: failed to resolve loose end mismatch" << std::endl;
		throw ErrProgrammingError("mergeLooseEnds failed! start=false",
					  __FILE__, __LINE__);
	      }
	    }
	  }
#ifdef DEBUG
	  if(verbosecategory) {
	    oofcerr << "tetIntersectionFaceFacets: evened up the loose ends"
		    << std::endl;
	  }
#endif // DEBUG
	} // end if nStarts != nEnds

#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "tetIntersectionFaceFacets: loose ends before adding missing segs:"
		  << std::endl;
	  for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	    oofcerr << "tetIntersectionFaceFacets: edge=" << e << std::endl;
	    OOFcerrIndent indent(2);
	    for(LooseEndMap::iterator le=looseEnds[e].begin();
		le!=looseEnds[e].end(); ++le)
	      {
		oofcerr << "   " << (*le).first << ": "
			<< (*le).second << std::endl;
	      }
	      
	  }
	}
#endif // DEBUG
	
	// Create the missing segments.  Missing segments start at a
	// loose end and end at a loose start.  Begin by finding a
	// loose end.
	unsigned int e0 = 0; // starting edge for missing seg construction
	LooseEndMap::iterator le; // starting intersection
	bool found = false;
	for(unsigned int e=0 ; e<NUM_TET_FACE_EDGES && !found; e++) {
	  LooseEndMap &lem = looseEnds[e];
	  for(le=lem.begin(); le!=lem.end(); ++le) {
	    if(!(*le).second.start) {
	      found = true;
	      e0 = e;
	      break;
	    }
	  } // end loop over intersections on edge e0 looking for loose start
	} // end loop looking for edge with a loose start.

#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "tetIntersectionFaceFacets: looked for loose end: found="
		  << found << std::endl;
	}
#endif // DEBUG
	
	// If an initial loose end wasn't found, there are no
	// unmatched intersections on the edges of the face, and no
	// missing segments.
	
	if(found) {
	  bool wrapped = false;
	  bool done = false;
	  unsigned int edge = e0;
	  // startPt is the start of the missing segment
	  const FacetCorner *startPt = (*le).second.corner();
	  if(verbosecategory)
	    oofcerr << "tetIntersectionFaceFacets: startPt=" << *startPt
		    << std::endl;
	  LooseEndMap::iterator deleteMe = le;
	  le++;
	  // oofcerr << "tetIntersectionFaceFacets: deleting FaceEdgeIntersection "
	  // 	  << (*deleteMe).first << ": " << (*deleteMe).second
	  // 	  << " e0=" << e0 << std::endl;
	  looseEnds[e0].erase(deleteMe);
	  // oofcerr << "tetIntersectionFaceFacets: deleted first point"
	  // 	  << std::endl;
	  Coord3D node0, node1;	// nodes at ends of current edge
	  unsigned int inode0, inode1; // indices of the nodes
	  edgeNodes(f, edge, epts, node0, node1, inode0, inode1);
	  if(verbosecategory)
	    oofcerr << "tetIntersectionFaceFacets: initial nodes: "
		    << node0 << " " << node1 << " " << inode0 << " " << inode1
		    << std::endl;
	  while(!done) {
	    // oofcerr << "tetIntersectionFaceFacets: top of connection loop"
	    // 	    << std::endl;
	    if(startPt != NULL) {
	      // oofcerr << "tetIntersectionFaceFacets: looking for end"
	      // 	      << std::endl;
	      // Look for the next point at which a missing segment
	      // ends.  This is either the next intersection point on
	      // this edge (which must be the start of an existing
	      // segment), or the end of the edge.
	      if(le == looseEnds[edge].end()) {
		// Missing segment ends at the end of the edge
		if(verbosecategory)
		  oofcerr << "tetIntersectionFaceFacets: ending at corner"
			  << std::endl;
		FacetCorner *endPt = new SimpleFacetCorner(
				   node1, nodeBCoord(inode1), allCorners);
		facetEdges.insert(FacetEdge(
		   new SimpleFacetCorner(startPt->position3D(),
					 startPt->bcoord(), allCorners),
		   endPt
#ifdef DEBUG
		   , "missing 1"
#endif // DEBUG
					   ));
		if(verbosecategory)
		  oofcerr << "tetIntersectionFaceFacets: added edge "
			  << startPt->position3D() << " "
			  << endPt->position3D() << std::endl;
		edge += 1;
		if(edge == NUM_TET_FACE_EDGES)
		  edge = 0;
		// oofcerr << "tetIntersectionFaceFacets: going to next edge "
		// 	<< edge << std::endl;
		le = looseEnds[edge].begin();
		wrapped = (edge == e0);
		edgeNodes(f, edge, epts, node0, node1, inode0, inode1);
		startPt = endPt;
	      }	// end if at the end of the edge
	      else {
		// end point of missing segment is on this edge
#ifdef DEBUG
		// oofcerr << "tetIntersectionFaceFacets: looking for end pt on this edge" << std::endl;
		// The end pt of the missing segment should be the
		// start pt of an existing segment.
		if(!(*le).second.start) {
		  throw ErrProgrammingError(
			    "Misordered segments on face " + to_string(f)
			    + " category " + to_string(category)
			    + "! (1)",
			    __FILE__, __LINE__);
		}
#endif // DEBUG
		const FacetCorner *endPt = (*le).second.corner();
		// oofcerr << "tetIntersectionFaceFacets: endPt=" << *endPt
		// 	<< std::endl;
		facetEdges.insert(FacetEdge(
		   new SimpleFacetCorner(startPt->position3D(),
					 startPt->bcoord(), allCorners),
		   new SimpleFacetCorner(endPt->position3D(),
					 endPt->bcoord(), allCorners)
#ifdef DEBUG
					   , "missing 2"
#endif // DEBUG
					   ));
		deleteMe = le;
		le++;
		looseEnds[edge].erase(deleteMe);
		startPt = NULL;
	      }	// end if endpoint of missing segment is on this edge
	    }	// end if startPt is not null
	    else {
	      // Look for the next point at which a missing segment
	      // starts.  This will be the end point of an existing
	      // segment.
	      if(le == looseEnds[edge].end()) {
		// There's no remaining starting point on this edge.
		if(wrapped) {
		  // oofcerr << "tetIntersectionFaceFacets: wrapped" << std::endl;
		  done = true;
		}
		else {
		  edge += 1;
		  if(edge == NUM_TET_FACE_EDGES)
		    edge = 0;
		  // oofcerr << "tetIntersectionFaceFacets: going to next edge "
		  // 	  << edge << std::endl;
		  edgeNodes(f, edge, epts, node0, node1, inode0, inode1);
		  wrapped = (edge == e0);
		  le = looseEnds[edge].begin();
		} // end if not wrapped
	      }	  // end if at end of edge
	      else {
#ifdef DEBUG
		// oofcerr << "tetIntersectionFaceFacets: looking for start pt on this edge." << std::endl;
		if((*le).second.start) {
		  oofcerr << "tetIntersectionFaceFacets: "
			  << "Misordered segments on face " << f << "! (2)"
			  << std::endl;
		  throw ErrProgrammingError(
			    "Misordered segments on face " + to_string(f)
			    + " category " + to_string(category)
			    + "! (2)",
			    __FILE__, __LINE__);
		}
#endif // DEBUG
		startPt = (*le).second.corner();
		// oofcerr << "tetIntersectionFaceFacets: startPt=" << *startPt
		// 	<< std::endl;
		deleteMe = le;
		le++;
		looseEnds[edge].erase(deleteMe);
	      }
	    }
	  }	// end while not done
// #ifdef DEBUG
// 	  if(verbosecategory) {
// 	    oofcerr << "tetIntersectionFaceFacets: constructed missing edges"
// 		    << std::endl;
// 	  }
// #endif // DEBUG
	} // end if loose ends were found
       

// 	std::vector<const FaceEdgeIntersection> looseStarts;
// 	std::vector<const FaceEdgeIntersection> looseEnds;
// 	looseStarts.reserve(nsegs);
// 	looseEnds.reserve(nsegs);
// 	for(unsigned int i=0; i<nsegs; i++) {
// 	  if(!matchedStarts[i]) {
// 	    startPoints[i].findEdge(f);
// 	    looseStarts.push_back(startPoints[i]);
// 	  }
// 	  if(!matchedEnds[i]) {
// 	    endPoints[i].findEdge(f);
// 	    looseEnds.push_back(endPoints[i]);
// 	  }
// 	}
// #ifdef DEBUG
// 	if(verbosecategory) {
// 	  oofcerr << "tetIntersectionFaceFacets: found loose ends" << std::endl;
// 	  oofcerr << "tetIntersectionFaceFacets: looseStarts=";
// 	  std::cerr << derefprint(looseStarts);
// 	  oofcerr << std::endl;
// 	  oofcerr << "tetIntersectionFaceFacets: looseEnds=";
// 	  std::cerr << derefprint(looseEnds);
// 	  oofcerr << std::endl;
// 	  OOFcerrIndent indent(2);
// 	  for(auto &s : looseStarts) {
// 	    for(auto &e : looseEnds) {
// 	      oofcerr << "diff: " << *s << " - " << *e << " = "
// 		      << (s->position3D() - e->position3D())
// 		      << " " << s->bcoord() << " " << e->bcoord()
// 		      << std::endl;
// 	    }
// 	  }
// 	}
// #endif // DEBUG
// 	assert(looseStarts.size() == looseEnds.size());

// 	if(!looseStarts.empty()) {
// 	  // Loop over the loose ends at which a missing segment must
// 	  // start.  These are the end points of existing segments.
// 	  // Project the point onto the closest tet edge, and store its
// 	  // parametric position along the edge.
// 	  std::vector< std::multiset<double> > startMap(NUM_TET_FACE_EDGES);
// 	  for(std::vector<const FacetCorner*>::iterator c=looseEnds.begin();
// 	      c!=looseEnds.end(); ++c)
// 	    {
// 	      // #ifdef DEBUG
// 	      // 	    if(verbosecategory)
// 	      // 	      oofcerr << "tetIntersectionFaceFacets: finding closest edge, pt="
// 	      // 	    	      << *c << std::endl;
// 	      // #endif // DEBUG
// 	      unsigned int fEdge = NONE; // face index of edge
// 	      double t;			 // position along edge
// 	      if(find_edge((*c)->bcoord(), f,
// #ifdef DEBUG
// 			  verbosecategory,
// #endif // DEBUG
// 			  t, fEdge))
// 		{
// 		  // #ifdef DEBUG
// 		  // 	    if(verbosecategory)
// 		  // 	      oofcerr << "tetIntersectionFaceFacets: missing start pt "
// 		  // 	    	      << *c << " is on edge " << closest.edge
// 		  // 	    	      << " at t=" << closest.t << std::endl;
// 		  // #endif // DEBUG
// 		  startMap[fEdge].insert(t);
// 		}
// 	    }
// 	  // Do the same for the points at which a missing segment must
// 	  // end.
// 	  std::vector< std::multiset<double> > endMap(NUM_TET_FACE_EDGES);
// 	  for(std::vector<const FacetCorner*>::iterator c=looseStarts.begin();
// 	      c!=looseStarts.end(); ++c)
// 	    {
// 	      unsigned int fEdge = NONE;
// 	      double t;
// 	      if(find_edge((*c)->bcoord(), f,
// #ifdef DEBUG
// 			  verbosecategory,
// #endif // DEBUG
// 			  t, fEdge))
// 		{
// 		  // #ifdef DEBUG
// 		  // 	    if(verbosecategory)
// 		  // 	      oofcerr << "tetIntersectionFaceFacets: missing end pt "
// 		  // 		      << *c << " is on edge " << closest.edge
// 		  // 		      << " at t=" << closest.t << std::endl;
// 		  // #endif // DEBUG
// 		  endMap[fEdge].insert(t);
// 		}
// 	    }
// #ifdef DEBUG
// 	  if(verbosecategory) {
// 	    for(int i=0; i<NUM_TET_FACE_EDGES; i++)
// 	      std::cerr << "tetIntersectionFaceFacets: startMap[" << i << "] = "
// 			<< startMap[i] << std::endl;
// 	    for(int i=0; i<NUM_TET_FACE_EDGES; i++)
// 	      std::cerr << "tetIntersectionFaceFacets: endMap[" << i << "] = "
// 			<< endMap[i] << std::endl;
// 	  }
// #endif // DEBUG

// 	  // Go around the face and add edges joining the loose ends.
// 	  // First, find an edge with a start point.
// 	  bool done = false;
// 	  // #ifdef DEBUG
// 	  // 	if(verbosecategory)
// 	  // 	  oofcerr << "tetIntersectionFaceFacets: looking for loose start point"
// 	  // 		  << std::endl;
// 	  // #endif // DEBUG
// 	  for(unsigned int e0=0; e0<NUM_TET_FACE_EDGES && !done; e0++) {
// 	    // OOFcerrIndent indent(2);
// 	    if(!startMap[e0].empty()) {
// 	      // e0 is the first face edge with a starting point on it.
// 	      unsigned int edge = e0;
// 	      bool wraparound = false;
// 	      // s is fractional distance along edge to the start point
// 	      double s = *startMap[edge].begin();
// 	      // #ifdef DEBUG
// 	      // 	    if(verbosecategory)
// 	      // 	      oofcerr << "tetIntersectionFaceFacets: initial start point e0="
// 	      // 	    	      << e0
// 	      // 	    	      << " s=" << s << std::endl;
// 	      // #endif // DEBUG
// 	      // Now loop over the start and end points, pairing them
// 	      // up.  If an end point doesn't exist for a start point,
// 	      // use the end of the edge (ie, the node).
// 	      while(!done) {
// 		unsigned int inode0, inode1; // tet indices of nodes
// 		Coord3D node0, node1;
// 		// edgeNodes finds the nodes of edge 'edge' of face 'f'.
// 		edgeNodes(f, edge, epts, node0, node1, inode0, inode1);
// 		// #ifdef DEBUG
// 		// 	      OOFcerrIndent indent(2);
// 		// 	      if(verbosecategory) {
// 		// 	      	oofcerr << "tetIntersectionFaceFacets: node0=" << node0
// 		// 	      		<< " node1=" << " " << node1 << std::endl;
// 		// 	      	oofcerr << "tetIntersectionFaceFacets: looking for end for s="
// 		// 	      		<< s << " edge=" << edge << std::endl;
// 		// 	      }
// 		// #endif // DEBUG
// 		startMap[edge].erase(s);
	      
// 		// Find the end point for this startpoint.
// 		bool endfound = false;
// 		// Look for an end on this edge.  No need to loop --
// 		// the end must be the first or second entry in
// 		// endMap[edge], if it exists.  It can be the second
// 		// entry only if this is the very first pass and the
// 		// initial start point on e0 come after the first end
// 		// point on e0.
// 		std::multiset<double> &ends = endMap[edge];
// 		std::multiset<double>::iterator endit = ends.begin();
// 		if(!ends.empty() && *endit >=s) {
// 		  endfound = true;
// 		}
// 		else if(ends.size() >=2) {
// 		  endit++;
// 		  if(*endit >= s)
// 		    endfound = true;
// 		}
// 		if(endfound) {
// 		  // e is the fractional position along the edge to the end pt
// 		  double e = *endit;
// 		  endMap[edge].erase(endit);
// 		  // TODO: Use position3D of FacetCorner instead of
// 		  // recomputing from s and e?
// 		  // #ifdef DEBUG
// 		  // 		if(verbosecategory) 
// 		  // 		  oofcerr << "tetIntersectionFaceFacets: found end e=" << e
// 		  // 			  << ", adding segment "
// 		  // 			  << (1-s)*node0 + s*node1 << " "
// 		  // 			  << (1-e)*node0 + e*node1 << std::endl;
// 		  // #endif // DEBUG

// 		  BarycentricCoord b0 = nodeBCoord(inode0);
// 		  BarycentricCoord b1 = nodeBCoord(inode1);
// 		  facetEdges.insert(FacetEdge(
// 			      new SimpleFacetCorner((1-s)*node0 + s*node1,
// 						    averageBary(b0, b1, s),
// 						    allCorners),
// 			      new SimpleFacetCorner((1-e)*node0 + e*node1,
// 						    averageBary(b0, b1, e),
// 						    allCorners)
// #ifdef DEBUG
// 					      , "missing"
// #endif // DEBUG
// 					      ));
// 		  // #ifdef DEBUG
// 		  // 		if(verbosecategory)
// 		  // 		  oofcerr << "tetIntersectionFaceFacets: looking for next start"
// 		  // 			  << std::endl;
// 		  // #endif // DEBUG
// 		  // Look for the next start point.
// 		  if(!startMap[edge].empty()) {
// 		    // #ifdef DEBUG
// 		    // 		  if(verbosecategory)
// 		    // 		    oofcerr << "tetIntersectionFaceFacets: got start on same edge"
// 		    // 		  	    << std::endl;
// 		    // #endif // DEBUG
// 		    s = *startMap[edge].begin();
// 		  } // end if startMap[edge] is not empty
// 		  else {
// 		    bool startfound = false;
// 		    // #ifdef DEBUG
// 		    // 		  if(verbosecategory)
// 		    // 		    oofcerr << "tetIntersectionFaceFacets: looking for start on new edge"
// 		    // 		   	    << std::endl;
// 		    // #endif // DEBUG
// 		    while(!startfound && !done) {
// 		      edge = (edge + 1) % NUM_TET_FACE_EDGES;
// 		      // #ifdef DEBUG
// 		      // 		    if(verbosecategory) {
// 		      // 		      oofcerr << "tetIntersectionFaceFacets: moving to edge "
// 		      // 		    	      << edge << std::endl;
// 		      // 		      std::cerr << "tetIntersectionFaceFacets: startMap["
// 		      // 		    		<< edge << "]=" << startMap[edge] << std::endl;
// 		      // 		    }
// 		      // #endif // DEBUG
// 		      if(edge == e0) {
// 			// #ifdef DEBUG
// 			// 		      if(verbosecategory)
// 			// 		      	oofcerr << "tetIntersectionFaceFacets: wrapped around"
// 			// 		      		<< std::endl;
// 			// #endif // DEBUG
// 			done = true;
// 		      }
// 		      else if(!startMap[edge].empty()) {
// 			// #ifdef DEBUG
// 			// 		      if(verbosecategory)
// 			// 		       	oofcerr << "tetIntersectionFaceFacets: found new start on edge " << edge << std::endl;
// 			// #endif // DEBUG
// 			s = *startMap[edge].begin();
// 			// #ifdef DEBUG
// 			// 		      if(verbosecategory)
// 			// 		      	oofcerr << "tetIntersectionFaceFacets: s=" << s
// 			// 		      		<< std::endl;
// 			// #endif // DEBUG
// 			startfound = true;
// 		      }
// 		    }	// end while !startfound && !done
// 		  }	// end if/else startMap[edge] is empty
// 		}	// end if endfound
// 		else {
// 		  // There's no end point on this tet edge.  Use the
// 		  // node at the end of the edge, and go to the next
// 		  // edge.  There had better not be another start point
// 		  // on this edge.
// #ifdef DEBUG
// 		  if(!startMap[edge].empty()) {
// 		    if(verbosecategory) {
// 		      oofcerr << "tetIntersectionFaceFacets: no end found on this edge"
// 			      << std::endl;
// 		      oofcerr << "tetIntersectionFaceFacets: startMap not empty!"
// 			      << std::endl;
// 		      std::cerr << "tetIntersectionFaceFacets:  startMap[" << edge
// 				<< "] = " << startMap[edge] << std::endl;
// 		    }
// 		    // oofcerr << "tetIntersectionFaceFacets: adding segment to end "
// 		    // 	  << (1-s)*node0 + s*node1 << " " << node1 << std::endl;
// 		    throw ErrProgrammingError("startMap not empty!",
// 					      __FILE__, __LINE__);
// 		  }
// #endif // DEBUG

		  
// 		  BarycentricCoord b0 = nodeBCoord(inode0);
// 		  BarycentricCoord b1 = nodeBCoord(inode1);
		  
		  
// 		  facetEdges.insert(FacetEdge(
// 			      new SimpleFacetCorner((1-s)*node0 + s*node1,
// 						    averageBary(b0, b1, s),
// 						    allCorners),
// 			      new SimpleFacetCorner(node1, b1, allCorners)
// #ifdef DEBUG
// 			      , "missing to end"
// #endif // DEBUG
// 					      ));
// 		  s = 0;		// next start point is at the node
// 		  edge = (edge + 1) % NUM_TET_FACE_EDGES;
// 		  if(wraparound) {
// 		    throw ErrProgrammingError(
// 	      "tetIntersectionFaceFacets: endpoint search wrapped around.",
// 	      __FILE__, __LINE__);
// 		  }
// 		  wraparound = edge == e0;
// 		  startMap[edge].insert(0.0);
// 		}	// end if end not found
//  	      } // end while !done
	    
	      
// 	      // What if round off error has put a start point after its
// 	      // end point?
	    
// 	    } // end if !startMap[e0].empty()
// 	  } // end loop over edges e0 looking for the first loose starting point

// 	} // end if there are any loose ends (!looseStarts.empty())

#ifdef DEBUG
	if(verbosecategory)
	  oofcerr << "tetIntersectionFaceFacets: done with loose ends"
		  << std::endl;
#endif // DEBUG

	// If, after all of this, there are no facet edges on the face,
	// it's either because the face is in the wrong category or
	// because *all* of the face is in the right category.  This can
	// also happen if there are one or more pairs of oppositely
	// directed but otherwise equal edges on a face, if it grazes
	// one or more voxel edges. In either case, we have to add edges
	// for the entire perimeter if the whole face is in the
	// category.

	// If the computed area is *negative*, then we also have to add
	// edges for the entire perimeter.  The area can be negative
	// only if the entire perimeter of the face is in the target
	// category, but there are islands of another category inside
	// the face.

	// It's important to use AREATOL correctly here.  A rather
	// common corner case is when a tet face grazes a voxel edge.
	// In that case, there will be a facet with two (ideally) equal
	// and opposite edges.  Each edge arises from the intersection
	// of a different pixel plane with the tet face, so in practice
	// the end points of the two edges might not precisely agree.
	// We detect such a case by looking for facets that have zero
	// area.  Because we're deciding whether or not to include the
	// entire perimeter of the tet face in the face, the
	// consequences of choosing wrong are significant.  So, when
	// looking for zero area, we include areas from -AREATOL to
	// +AREATOL.  If a truly positive area is treated as 0, the
	// whole perimeter still won't be included because it will fail
	// the testxvl condition (TODO: will it?).  A truly negative
	// area treated as zero will include the whole perimeter, as it
	// should, because it will pass the testvxl condition.

	// TODO: We can re-use the area computed here in
	// tetIntersectionVolume.

	std::vector<Coord3D> nodes = faceNodes(f, epts);
	Coord3D ctr = (nodes[0] + nodes[1] + nodes[2])/3.0;
	Coord3D areavec;		// vector!
	for(std::set<FacetEdge>::const_iterator s=facetEdges.begin();
	    s!=facetEdges.end(); ++s)
	  {
	    areavec += (((*s).start->position3D() - ctr) %
			((*s).end->position3D()- ctr));
	  
	  }
	bool homog_face = false;
	double raw_area = 0.5*dot(areavec, faceNormal(f, epts));
#ifdef DEBUG
	if(verbosecategory)
	  oofcerr << "tetIntersectionFaceFacets: raw_area for face "
		  << f << " is " << raw_area << std::endl;
#endif // DEBUG

	if(fabs(raw_area) <= AREATOL) {	
	  // Check for a homogeneous face.  Look at the voxel at the center.
	  ICoord testvxl(ctr[0], ctr[1], ctr[2]);
	  // The point at the center may be on a voxel boundary, and we
	  // have to choose the voxel that is inside the element.

	  // TODO: The calculation of testvxl is independent of the
	  // category, so it should be cached and re-used here.

	  // TODO: Is this the correct way to find testvxl?  What if an
	  // edge or a corner of a voxel lies in the tet face?  Is it
	  // possible that the wrong voxel could be chosen?
	
	  Coord3D nrml;
	  bool nrmlfound = false;
	  for(unsigned int c=0; c<3; c++) {
	    // See comment in faceIsOnVoxelPlane about whether or not
	    // this is a robust way of determining if a point is on a
	    // voxel edge.
	    if(ctr[c] == testvxl[c]) {
	      if(!nrmlfound) {
		nrml = nodes[0]%nodes[1]; // outward normal
		nrmlfound = true;
	      }
	      if(nrml[c] > 0) {
		testvxl[c] -= 1;
	      }
	    }
	    if(testvxl[c] == vsb.microstructure->sizeInPixels()[c]) {
	      testvxl[c] -= 1;
	    }
	  } // end loop over directions c to adjust the test voxel position
	  homog_face = vsb.microstructure->category(testvxl) == category;
	}
	// Include the entire perimeter if the face is entirely in the
	// category or has holes in it.
	if(raw_area < -AREATOL || homog_face) {
#ifdef DEBUG
	  if(verbosecategory) {
	    oofcerr << "tetIntersectionFaceFacets: including full perimeter"
		    << std::endl;
	  }
#endif // DEBUG
	  std::vector<BarycentricCoord> bcoords;
	  bcoords.reserve(3);
	  for(unsigned int i=0; i<3; i++) {
	    bcoords.push_back(nodeBCoord(vtkTetra::GetFaceArray(f)[i]));
	  }
	  facetEdges.insert(FacetEdge(
			      new SimpleFacetCorner(nodes[0], bcoords[0],
						    allCorners),
			      new SimpleFacetCorner(nodes[1], bcoords[1],
						    allCorners)
#ifdef DEBUG
			      , "homogeneous face"
#endif // DEBUG
				      ));
	  facetEdges.insert(FacetEdge(
			      new SimpleFacetCorner(nodes[1], bcoords[1],
						    allCorners),
			      new SimpleFacetCorner(nodes[2], bcoords[2],
						    allCorners)
#ifdef DEBUG
			      , "homogeneous face"
#endif // DEBUG
				      ));
	  facetEdges.insert(FacetEdge(
			      new SimpleFacetCorner(nodes[2], bcoords[2],
						    allCorners),
			      new SimpleFacetCorner(nodes[0], bcoords[0],
						    allCorners)
#ifdef DEBUG
			      , "homogeneous face"
#endif // DEBUG
				      ));
	}
	
#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "tetIntersectionFaceFacets: final facetEdges for face "
		  << f << " category " << category << std::endl;
	  OOFcerrIndent indent(4);
	  for(std::set<FacetEdge>::const_iterator i=facetEdges.begin();
	      i!=facetEdges.end(); ++i)
	    oofcerr << *i << std::endl;
	}
	if(verbose) {
	  openDumpFile("finalfacets_cat" + to_string(category)
		       + "_face" + to_string(f));
	  for(std::set<FacetEdge>::const_iterator i=facetEdges.begin();
	      i!=facetEdges.end(); ++i)
	    dumpSegment((*i).start->position3D(), (*i).end->position3D());
	  closeDumpFile();
	}
#endif // DEBUG

      }	  // end if face not done already
    }	  // end loop over faces f
  }
  catch (...) {
    oofcerr << "Error in tetIntersectionFaceFacets: category=" << category
	    << std::endl;
    throw;
  }
} // end tetIntersectionFaceFacets


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Compute the volume, in voxel units, of the intersection of the
// voxel set with the tetrahedron with the given corners.  The facets
// of the intersection that lie on pixel planes are also given.


double tetIntersectionVolume(const VoxelSetBoundary &vsb,
			     const std::vector<Coord3D> &epts,
			     const ICRectangularPrism &iBounds,
			     const FacetMap2D &facets,
			     const BaryCoordMap &baryEquiv,
			     FacetCornerList &allCorners,
			     BaryCoordCache &baryCache,
			     const std::vector<bool> &didFace,
			     unsigned int category
#ifdef DEBUG
			     , bool verbose
#endif // DEBUG
			     )
{
  // Get volume contribution from pixel plane facets.

#ifdef DEBUG
  bool verbosecategory = verboseCategory(verbose, category);
  // if(verbosecategory) {
  //   oofcerr << "tetIntersectionVolume: category=" << category << std::endl;
  //   oofcerr << "tetIntersectionVolume: pixel plane facets:" << std::endl;
  // }
  // OOFcerrIndent indent(2);
#endif // DEBUG
  double vol = 0.0;
  Coord3D center = 0.25*(epts[0] + epts[1] + epts[2] + epts[3]);
  for(FacetMap2D::const_iterator fm=facets.begin(); fm!=facets.end(); ++fm) {
    const PixelPlane &pixplane = (*fm).first;
    const PixelPlaneFacet *facet = (*fm).second;
    if(!facet->empty()) {
      // Make the facet's contribution to the volume
      double dv = (facet->area(false) * pixplane.normalSign() *
		   (pixplane.normalOffset()-center[pixplane.direction()]))/3.0;
// #ifdef DEBUG
//       if(verbosecategory) {
//       	oofcerr << "tetIntersectionVolume: plane=" << pixplane << std::endl;
//       	// oofcerr << "tetIntersectionVolume: facet=" << *facet << std::endl;
//       	oofcerr << "tetIntersectionVolume:    area=" << facet->area()
//       		<< " dV=" << dv << std::endl;
//       }
// #endif // DEBUG
      vol += dv;
    }
  }

  std::vector< std::set<FacetEdge> > faceFacetEdges(NUM_TET_FACES);
  tetIntersectionFaceFacets(vsb, epts, iBounds, facets, baryEquiv, allCorners,
			    baryCache,
			    didFace, category,
#ifdef DEBUG
			    verbose,
#endif // DEBUG
			    faceFacetEdges);

  // Get volume contribution from tet face facets
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    std::set<FacetEdge> &facetEdges = faceFacetEdges[f];
// #ifdef DEBUG
//     if(verbosecategory) {
//       oofcerr << "tetIntersectionVolume: f=" << f;
//       std::cerr << " facetEdges=" << facetEdges;
//       oofcerr << std::endl;
//     }
// #endif // DEBUG

    // didFace[f]==true means that the face was included in the
    // pixelplane step.
    if(!facetEdges.empty() && !didFace[f]) {
      Coord3D facetcenter;
      for(const auto &s : facetEdges) {
	facetcenter += s.start->position3D();
	facetcenter += s.end->position3D();
      }
      facetcenter /= 2.0 * facetEdges.size();
      Coord3D area;		// vector!
      for(const auto &s : facetEdges) {
	area += ((s.start->position3D() - facetcenter) %
		 (s.end->position3D() - facetcenter));
      }

      // factor of 1/2 for area, 1/3 for volume of pyramid
      double dv = dot(area, facetcenter-center) / 6.0;
      vol += dv;
// #ifdef DEBUG
//       if(verbosecategory)
//       	oofcerr << "tetIntersectionVolume: face=" << f << " area=" << area
//       		<< " dV=" << dv << std::endl;
// #endif // DEBUG
    } // end if face not empty or not done already
  }   // end loop over faces

#ifdef DEBUG
  if(verbosecategory)
    oofcerr << "tetIntersectionVolume: category=" << category
	    << " vol=" << vol << std::endl;
#endif // DEBUG
  return vol;
} // end tetIntersectionVolume

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

