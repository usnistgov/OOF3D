// -*- C++ -*-
// $RCSfile: tetintersection.C,v $
// $Revision: 1.1.2.1 $
// $Author: langer $
// $Date: 2015/01/22 20:35:14 $

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
#include "engine/cskeletonelement.h"
#include "engine/tetintersection.h"

// Given two points p0 and p1 and a triangle t0, t1, t2, find
// the intersection of the segment with the triangle.  Do it in a way
// that's symmetric under reorderings of the points to ensure that the
// roundoff error is reproducible if the segment or triangle is
// defined differently.

// The intersection point X is at
//    X = p0 + alpha0*(p1 - p0), then
//    alpha0 = ((C-p0) dot N)/((p1-p0) dot N)
// where C could be any point in the plane of the triangle, but we use
// the center to make it symmetric to reordering of t.
// We can switch the indices of p0 and p1 to get an equivalent
// expression,
//    X = p1 + alpha1*(p0 - p1)
//    alpha1 = ((C-p1) dot N)/((p0-p1) dot N)
//and then average the two to get a symmetric version:
//    X = 0.5 [p0 + p1 + (alpha0 - alpha1)*(p1 - p0)]
//      = 0.5 [p0 + p1 + (p1-p0)*((2C - (p0 + p1)) dot N)/((p1-p0) dot N)

static Coord3D segmentFaceIntersection(const ICoord3D &p0, const ICoord3D &p1,
				       const std::vector<Coord3D> &t)
{
  Coord3D N = t[0]%t[1] + t[1]%t[2] + t[2]%t[0]; // triangle normal
  Coord3D C = (t[0] + t[1] + t[2])/3.0;	       // triangle center
  ICoord3D psum = p0 + p1;
  ICoord3D pdiff = p1 - p0;
  assert(dot(pdiff, N) != 0.0);
  return 0.5 * (psum + pdiff*dot(2*C - psum, N)/dot(pdiff, N));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given a point x that lies on the line joining p0 and p1, return the
// fractional distance of x from p0 towards p1.  That is, return 0 if
// x is at p0, 1 if x is at p1, and something between 0 and 1 if x is
// in the middle.  The result is negative or greater than 1 if x does
// not lie on the segment (p0, p1).

static double fractionalDistance(const Coord2D &x, const Coord2D &p0,
				 const Coord2D &p1)
{
  Coord2D dp = p1 - p0;
  assert(dp != Coord2D(0, 0));
  return dot((x-p0), dp)/dot(dp, dp);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static std::vector<Coord3D> faceNodes(unsigned int faceIndex,
				      const std::vector<Coord3D> &epts)
{
  std::vector<Coord3D> nodes;
  nodes.reserve(3);
  for(unsigned int i=0; i<3; i++)
    nodes.push_back(epts[vtkTetra::GetFaceArray(faceIndex)[i]]);
  return nodes;
}

// Figure out if the given face of the tet lies on a plane between two
// layers of voxels (or is on an external boundary).  That is, is one
// of the components of the node positions the same for all three
// nodes, and an integer?

static bool faceIsOnVoxelPlane(unsigned int faceIndex,
			       const std::vector<Coord3D> &epts)
{
  std::vector<Coord3D> nodes(faceNodes(faceIndex, epts));
  for(int c=0; c<3; c++) {	// loop over directions
    double x = nodes[0][c];
    // TODO: Is x==int(x) robust?  If nodes are moved to a voxel
    // boundary in snapnodes, for example, they're moved to a point
    // given in physical units.  That point is converted to voxel
    // units by dividing by the voxel dimensions.  Is the value in
    // voxel units guaranteed to be an integer?  Do positions that
    // arise from snapping need to be saved as (integer,dx) so that
    // the integer can be extracted robustly?
    if(x == int(x) && nodes[1][c] == x && nodes[2][c] == x) {
      return true;
    }
  }
  return false;
}

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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

typedef std::multimap<double, PixelBdyIntersection*> ElEdgeMap;
typedef std::vector<ElEdgeMap> ElEdge;
typedef std::pair<double, PixelBdyIntersection*> ElEdgeDatum;


typedef std::multimap<Coord2D, PixelBdyIntersection*> CoordIsec;
typedef std::pair<Coord2D, PixelBdyIntersection*> CoordIsecDatum;

// Utility function for deleting an intersection from one of the
// ordered lists of intersections.  Intersections have sufficient data
// to locate themselves in these lists.

static void delete_isec(const PixelBdyIntersection *pbi, ElEdge &eledge) {
  int ni = pbi->node_index;
  double fr = pbi->fraction;
  
  int count = eledge[ni].count(fr);
  if (count==1) {
    eledge[ni].erase(fr);
  }
  else {
    ElEdgeMap::iterator emi = eledge[ni].lower_bound(fr);
    for(int i=0; i<count; ++emi, ++i) {
      if (((*emi).second->location2D==pbi->location2D) && 
	  ((*emi).second->entry==pbi->entry) ) {
	eledge[ni].erase(emi);
	break;
      }
    }
  }
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Set of perturbation directions for moving polygon corners.  This is
// a set of nonhorizontal, nonvertical unit vectors which are
// candidate directions for perturbing corners when searching for
// intersections with pixel-boundary segments.  The exclusion of the
// i=0 case is deliberate.  Corners are perturbed so that they won't lie
// directly on top of pixel boundaries, which complicates the
// intersection finding code.

// This should be prime, and greater than one more than the number of
// sides of the most-sided possible polygon.
#define PERTURB_DIRECTIONS 7

static const std::vector<Coord2D> *perturbations() {
  static std::vector<Coord2D> *perturbation_list = 0;
  if(!perturbation_list) {
    // This shows up as a memory leak in valgrind.  It's not, really.
    perturbation_list = new std::vector<Coord2D>(PERTURB_DIRECTIONS-1);
    double delta = 2.0*M_PI/PERTURB_DIRECTIONS;
    for(int i=1; i<PERTURB_DIRECTIONS; i++) {
      double angle = i*delta;
      (*perturbation_list)[i-1] = Coord2D(cos(angle), sin(angle));
    }
  }
  return perturbation_list;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Copied from CSkeletonElement::interior in 2D.  In 3D we need to
// know whether a point is inside a polygon, which is a 2D cross
// section of an element, so we can't use the CSkeletonElement method.

static bool interior(const std::vector<TetPlaneIntersectionPoint> &pos,
		     const ICoord2D &pt, const Coord2D &perturb)
{
  int nn = pos.size();
  if(nn == 3) {
    // Loops unrolled
    Coord2D edge = pos[1] - pos[0];
    double cross = edge % (pt - pos[0]);
    if(cross < 0.0)
      return false;
    if(cross == 0) {
      if(perturb % edge < 0.0)
	return false;
    }
    edge = pos[2] - pos[1];
    cross = edge % (pt - pos[1]);
    if(cross < 0.0)
      return false;
    if(cross == 0) {
      if(perturb % edge < 0.0)
	return false;
    }
    edge = pos[0] - pos[2];
    cross = edge % (pt - pos[2]);
    if(cross < 0.0)
      return false;
    if(cross == 0) {
      if(perturb % edge < 0.0)
	return false;
    }
    return true;
  }

  else if(nn == 4) {
    Coord2D edge = pos[1] - pos[0];
    double cross = edge % (pt - pos[0]);
    if(cross < 0.0)
      return false;
    if(cross == 0) {
      if(perturb % edge < 0.0)
	return false;
    }
    edge = pos[2] - pos[1];
    cross = edge % (pt - pos[1]);
    if(cross < 0.0)
      return false;
    if(cross == 0) {
      if(perturb % edge < 0.0)
	return false;
    }
    edge = pos[3] - pos[2];
    cross = edge % (pt - pos[2]);
    if(cross < 0.0)
      return false;
    if(cross == 0) {
      if(perturb % edge < 0.0)
	return false;
    }
    edge = pos[0] - pos[3];
    cross = edge % (pt - pos[3]);
    if(cross < 0.0)
      return false;
    if(cross == 0) {
      if(perturb % edge < 0.0)
	return false;
    }
    return true;
  }

  else {
    // This is the generic case, for nn!=3 and nn!=4, which will
    // probably never occur.  
    for(int ni=0; ni<nn; ++ni) {
      const Coord2D &posni = pos[ni];
      Coord2D edge = pos[(ni+1)%nn] - posni;
      double cross = edge % (pt-posni);
      if (cross < 0) {
	return false;
      }
      else if (cross==0) {
	if (perturb % edge < 0) {
	  return false;
	}
#ifdef DEBUG
	if (perturb % edge == 0) {
	  std::cerr << "Ambiguous interiority after perturbation!" 
		    << std::endl;
	}
#endif // DEBUG
      }
    }
    return true;
  } // end generic case
  return false;
} // end interior()

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO OPT: TetPlaneIntersectionPoints are sort of large objects.  Is
// it better to use a vector of pointers, and/or not copy the vector?

// TODO OPT: Would it be more efficient to compute the
// TetPlaneIntersectionPoints for all offsets at once?

std::vector<TetPlaneIntersectionPoint> findTetPlaneIntersectionPoints(
					   const std::vector<Coord> &epts,
					   unsigned int c, int offset)
{
  // std::cerr << "findTetPlaneIntersectionPoints: epts=" << epts
  // 	    << ", c=" << c << ", offset=" << offset << std::endl;
  std::vector<TetPlaneIntersectionPoint> result;
  std::vector<unsigned int> overnodes;	// tet nodes above the plane
  std::vector<unsigned int> undernodes;	// tet nodes below the plane
  PixelPlane pp(c, offset, 1);
  for(unsigned int k=0; k<NUM_TET_NODES; ++k) {
    double h = epts[k][c];
    if(h == offset) {
      // The tet node is on the plane.  Choose an edge that's not in
      // the plane, and put the TetPlaneIntersectionPoint at the end
      // of the edge.
      Coord2D pt(pp.convert2Coord2D(epts[k]));
      bool done = false;
      for(unsigned int kk=0; kk<NUM_TET_NODES && !done; ++kk) {
	if(epts[kk][c] != offset) {
	  unsigned int edgeId = CSkeletonElement::nodeNodeEdge[k][kk];
	  int *segnodes = vtkTetra::GetEdgeArray(edgeId);
	  if(k == segnodes[0] && kk == segnodes[1])
	    result.push_back(TetPlaneIntersectionPoint(pt, 0, edgeId));
	  else if(k == segnodes[1] && kk == segnodes[0]) 
	    result.push_back(TetPlaneIntersectionPoint(pt, 1, edgeId));
	  else
	    throw ErrProgrammingError("Unexpected node/edge indices! (1)",
				      __FILE__, __LINE__);
	  done = true;
	}
      }
      if(!done)			// all of the nodes are in the plane
	throw ErrProgrammingError(
		  "findTetPlaneIntersectionPoints found an illegal element.",
		  __FILE__, __LINE__);
    }
    else if(h < offset) {
      undernodes.push_back(k);
    }
    else if(h > offset) {
      overnodes.push_back(k);
    }
  } // end loop over nodes tet nodes k
  if(!(undernodes.empty() && overnodes.empty())) {
    result.reserve(undernodes.size()*overnodes.size());
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
	Coord2D intersect = 0.5*(p0 + p1 + (p1-p0)*(2*offset-(c0+c1))*cfactor);
	// t is the parametric position of the intersection point
	// along the tet edge.  
	double t = (offset - c0)*cfactor;
	// TODO: Do we need to correct for roundoff error?
	// if(t > 1.0)
	//   t = 1.0;
	// else if(t < 0)
	//   t = 0.0;

	unsigned int edgeId = CSkeletonElement::nodeNodeEdge[ii][jj];
	// Decide if the order of the nodes is canonical, according to
	// the vtk scheme, and create the TetPlaneIntersectionPoint object.
	int *segnodes = vtkTetra::GetEdgeArray(edgeId);
	if(ii == segnodes[0] && jj == segnodes[1])
	  result.push_back(TetPlaneIntersectionPoint(intersect, t, edgeId));
	else if(ii == segnodes[1] && jj == segnodes[0])
	  result.push_back(TetPlaneIntersectionPoint(intersect, 1-t, edgeId));
	else
	  throw ErrProgrammingError("Unexpected node/edge indices! (2)",
				    __FILE__, __LINE__);
      }
    }
  }
  return result;
} // end findTetPlaneIntersectionPoints

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

unsigned int TetPlaneIntersectionPoint::sharedFace(
				   const TetPlaneIntersectionPoint &other)
  const
{
  return CSkeletonElement::edgeEdgeFace[edge_][other.edge()];
}

std::ostream &operator<<(std::ostream &os, const TetPlaneIntersectionPoint &t)
{
  return os << "TetPlaneIntersectionPoint((" << t[0] << ", " << t[1]
	    << "), t=" << t.t() << ", e=" << t.edge() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Coord2D FaceFacetCorner::position2D() const {
  return pixelplane.convert2Coord2D(location);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class TYPE>
static void reorderVector(std::vector<TYPE> &vec, int *ordering) {
  std::vector<TYPE> old(vec);
  for(unsigned int i=0; i<vec.size(); i++)
    vec[i] = old[ordering[i]];
}
					 
static void polygonize(std::vector<TetPlaneIntersectionPoint> &ipts) {
  // Given a list of 3 or 4 points in a plane, reorder the points so
  // that they form a polygon with positive area.  This is always
  // possible and has a unique solution (up to trivial renumbering)
  // because the points came from the intersection of a tet with a
  // plane. This code is the C++ version of the polygonize() routine
  // in primitives.py.
  assert(ipts.size() == 3 || ipts.size() == 4);
  Coord2D center;
  for(int i=0; i<ipts.size(); i++)
    center += ipts[i];
  center /= ipts.size();
  if(ipts.size() == 3) {
    // Three points in a triangle are oriented correctly if
    // their area, computed by cross products, is positive.
    double area = 0;
    for(int i=0; i<3; i++) {
      area += cross(ipts[i]-center, ipts[(i+1)%3]-center);
    }
    if(area < 0) {
      TetPlaneIntersectionPoint temp = ipts[2];
      ipts[2] = ipts[1];
      ipts[1] = temp;
    }
    return;
  }
  else if(ipts.size() == 4) {
    static int ordering[6][4] = {{0,1,2,3},{0,1,3,2},{0,2,1,3},{0,2,3,1},
				 {0,3,1,2},{0,3,2,1}};
    std::set<int> positiveOrderings;
    for(int ord=0; ord<6; ord++) {
      double area = 0;
      for(int i=0; i<4; i++) {
	area += cross(ipts[ordering[ord][i]] - center,
		      ipts[ordering[ord][(i+1)%4]] - center);
      }
      if(area > 0)
	positiveOrderings.insert(ord);
    }
    assert(!positiveOrderings.empty());
    if(positiveOrderings.size() == 1) {
      int ord = *positiveOrderings.begin();
      if(ord != 0) // skip the trivial case
	reorderVector(ipts, ordering[ord]);
      return;
    }
    else {
      // There's more than one ordering with positive area.  Check
      // that opposite edges don't cross.  Because the legal polygon
      // must be convex, it's sufficient to check that the end points
      // of one edge are both on the same side of the linear extension
      // of the other edge.
      for(std::set<int>::const_iterator o=positiveOrderings.begin();
	  o!=positiveOrderings.end(); ++o)
	{
	  int *ord = ordering[*o];
	  bool edgesCross = false;
	  // Loop over the pairs of opposite edges
	  for(int i=0; i<2 && !edgesCross; i++) {
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
	    return;
	  }
	} // end loop over positiveOrderings
    }	// end else if positiveOrderings.size() > 1
  }	// end if ipts.size() == 4
  throw ErrProgrammingError("Failed to find a well formed polygon.",
			    __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Not as stupid as it looks -- this routine helps resolve the "zero
// or two intersections" case by giving a definitive yes-or-no to the
// question of whether or not there are zero intersections between
// this pixel boundary segment and the polygon defined by the
// passed-in point list (pts).  The strategy is: if both endpoints of
// this pixel boundary segment are exterior to the same polygon
// segment, then no intersection is possible; failing that, the
// endpoints of the pixel boundary segment must terminate in different
// sectors, so if all of the polygon-corner coordinates are on the
// same side of the pixel boundary segment, then an intersection is
// impossible; failing *that*, an intersection (actually, two) is
// required.  The caller promises that both end-points of the pixel
// boundary segment are exterior to the passed-in polygon (using an
// interiority test which takes the same cross-products as this
// routine), and we assume convexity of the element.

static bool find_no_intersection(
			 const PixelBdyLoop &loop,
			 unsigned int seg,
			 const std::vector<TetPlaneIntersectionPoint> &pts,
			 const Coord2D &perturb)
{
  int npts = pts.size();
  const ICoord2D start = loop.icoord(seg);
  const ICoord2D end = loop.next_icoord(seg);
    
  // loop over sides of the element 
  for(int i1=0; i1<npts; ++i1) {
    int i2 = (i1+1)%npts;
    // This is the same arithmetic as the interior function -- this is
    // important for avoiding roundoff-related screwups.
    const Coord2D eside = pts[i2] - pts[i1];
    double start_cross = eside % (start-pts[i1]);
    double end_cross = eside % (end-pts[i1]);

    // Easy case -- if they're both negative for this segment, then
    // there are no intersections, we're done.
    if ( (start_cross < 0) && (end_cross < 0) ) 
      return true;

    // In the boundary case, check against perturbations.
    double delta = perturb % eside;
    bool start_ok = (start_cross < 0) || ( (start_cross==0) && (delta < 0) );
    bool end_ok = (end_cross < 0) || ( (end_cross==0) && (delta < 0) );
    if (start_ok && end_ok) return true;
  } // end loop over sides of the element

  // If we made it this far, then the endpoints must be exterior in
  // different "sectors".  In this case, we can still rule out
  // intersections if all of the element nodes are on the same side of
  // the pixel boundary segment.  Find out which side the first one is
  // on.  If any of the others are on a different side, return false,
  // indicating that intersections are required.

  double initial_res = (pts[0] - start) % (end - start);
  double delta = perturb%(end-start);
  if (initial_res == 0)
    initial_res = delta;

  for(int i1=1; i1<npts; ++i1) {
    double new_res = (pts[i1] - start) % (end - start);
    if ( initial_res*new_res < 0)
      return false; // Intersection required.
    if ( (new_res==0) && (initial_res*delta < 0) )
      return false;
  }
  // If we didn't succeed in the first block, or fail in the second
  // block, then there are no intersections.

  return true;
} // end find_no_intersection()

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Quick intersection-finding routine, used when you have topological
// information about what's going on.  Specifically, you know that
// it's geometrically required that the pixel boundary segment must
// intersect the passed-in polygon edges exactly once, you know
// whether it enters or exits, and the only real question is where
// this occurs.  The return value is an integer indicating on which
// polygon segment the intersection occurred.

// Since the polygon comes from the intersection of a tet with a
// plane, and we need to match edges that come from different planes,
// we need to compute intersection points using tet face data instead
// of polygon edge data.  If two voxel boundary planes intersect each
// other and a tet face, we want both voxel boundary planes to compute
// the same intersection point even though they'll be working with
// different polygon edges.

static PixelBdyIntersection *find_one_intersection(
    const PixelBdyLoop &loop,
    const std::vector<Coord3D> &epts,
    const PixelPlane &pixplane,
    unsigned int seg, // index of the starting point of the bdy segment
    const std::vector<TetPlaneIntersectionPoint> &pts, //  polygon corners
    bool entry)		       // is the segment entering the polygon?
{
  int npts = pts.size();
  // Alpha is the fractional distance along an polygon segment, and
  // beta is the fractional distance along the boundary segment.
  // Round-off error can make it seem as if the intersection is just
  // past the endpoint of one of the segments.  Unless we've found an
  // intersection that clearly is in bounds, we use the one that's
  // least out of bounds.
  int t_segment = -1;		// segment number of the best intersection
  Coord3D t_pos; 		// position of best intersection found so far
  double t_alpha; 		// alpha for best intersection so far
  unsigned int t_face;		// face index of ...
  double error = std::numeric_limits<double>::max();
  // std::cerr << "find_one_intersection: looking for "
  // 	    << (entry ? "entry" : "exit") << std::endl;
  const ICoord2D segstart = loop.icoord(seg);
  const ICoord2D segend = loop.next_icoord(seg);
  // std::cerr << "find_one_intersection: seg=" << seg
  // 	    << " segstart=" << segstart
  // 	    << " segend=" << segend << std::endl;
  bool decrseg = loop.decreasing(seg);
  // std::cerr << "find_one_intersection: decreasing=" << decrseg
  // 	    << " horizontal=" << horizontal(seg) << std::endl;
  
  if (loop.horizontal(seg)) {
    // int fp_level = segstart[1];
    for(int i1=0; i1<npts; ++i1) { // loop over polygon edges
      int i2 = (i1 + 1)%npts;

      // Ignore the parallel case.
      if (pts[i1][1] == pts[i2][1])
	continue;

      // Also skip segments which are oriented incorrectly for the
      // type of intersection we want.  A horizontal category edge is
      // entering the polygon if the category edge is L->R (!decrseg)
      // and the polygon edge is is going down (!goingup), or if the
      // category edge is R->L (decrseg) and the polygon edge is going
      // up.
      bool goingup = pts[i2][1] > pts[i1][1]; // polygon edge is going up
      bool seg_entry = (goingup == decrseg);
      if (seg_entry != entry)
	continue;

      // Compute the intersection of the boundary segment with the
      // face of the tetrahedron that the polygon segment was formed
      // from.  Computing it in this way ensures that the round-off
      // error in the result is independent of pixplane.
      unsigned int face_index = pts[i1].sharedFace(pts[i2]);
      Coord3D intersect3D = segmentFaceIntersection(
				       pixplane.convert2Coord3D(segstart),
				       pixplane.convert2Coord3D(segend),
				       faceNodes(face_index, epts)
				       // faceNodes(pts[i1], pts[i2])
						    );
      // Find the location of the intersection on the pixel plane. 
      Coord2D intersect2D = pixplane.convert2Coord2D(intersect3D);
      // Is the 2D intersection point between the endpoints of the boundary
      // segment and the polygon segment?
      double alpha = fractionalDistance(intersect2D, pts[i1], pts[i2]);
      double beta = (intersect2D[0] - segstart[0])/(segend[0] - segstart[0]);

      // double alpha = (fp_level - pts[i1][1]) / (pts[i2][1] - pts[i1][1]);
      // double x = (1 - alpha)*pts[i1][0] + alpha*pts[i2][0];
      // double beta = (x - segstart[0])/(segend[0] - segstart[0]);

      // If the trial alpha/beta is in-bounds, we're done.
      // TODO: Should these checks use <= and >= ?
      if ((alpha > 0) && (alpha < 1) && (beta > 0) && (beta < 1)) {
	intersect2D[1] = segstart[1]; // correct possible roundoff error
	return new PixelBdyIntersection(intersect2D, intersect3D,
					i1, face_index, alpha, entry);
      }
      // Compute how far out of bounds we ended up.
      double new_error = 0.0;
      if (alpha > 1)
	new_error = (alpha-1.0)*(alpha-1.0);
      else if (alpha < 0)
	new_error = alpha*alpha;
      if (beta > 1)
	new_error += (beta-1.0)*(beta-1.0);
      else if (beta < 0)
	new_error += beta*beta;
      
      // If this is the first iteration, or if the new error is
      // smaller than the already-stored error, save the results.
      if (new_error < error) {
	error = new_error;
	t_segment = i1;
	t_pos = intersect3D;
	t_alpha = alpha > 1.0? 1.0 : 0.0;
	t_face = face_index;
      }
    } // end loop over polygon edges
    
    // If we made it out of the loop, that means none of the element
    // segments were in-bounds.  But the caller insists there must be
    // an intersection, so we'll return our best guess.
    assert(t_segment != -1);
    return new PixelBdyIntersection(pixplane.convert2Coord2D(t_pos),
				    t_pos, t_segment, t_face, t_alpha, entry);
  } // end if horizontal
  
  else {
    // Pixel boundary segment is vertical
    // int fp_level = segstart[0];
    for(int i1=0; i1 <npts; ++i1) { // loop over polygon edges
      int i2 = (i1 + 1)%npts;
      // Again, ignore the parallel case.
      if (pts[i1][0] == pts[i2][0])
	continue;
      // And again, ignore wrongly oriented segments.
      bool goingright = pts[i2][0] > pts[i1][0]; // polygon edge is going right
      bool seg_entry = (goingright != decrseg);
      if (seg_entry != entry)
	continue;
      unsigned int face_index = pts[i1].sharedFace(pts[i2]);
      Coord3D intersect3D = segmentFaceIntersection(
				       pixplane.convert2Coord3D(segstart),
				       pixplane.convert2Coord3D(segend),
				       faceNodes(face_index, epts)
				       // faceNodes(pts[i1], pts[i2])
						    );
      Coord2D intersect2D = pixplane.convert2Coord2D(intersect3D);
      double alpha = fractionalDistance(intersect2D, pts[i1], pts[i2]);
      double beta = (intersect2D[1] - segstart[1])/(segend[1] - segstart[1]);

      // double alpha = (fp_level - pts[i1][0])/(pts[i2][0] - pts[i1][0]);
      // double y = (1 - alpha)*pts[i1][1] + alpha*pts[i2][1];
      // double beta = (y - segstart[1])/(segend[1] - segstart[1]);
      
      // If we're in-bounds, we're done.
      if ((alpha > 0) && (alpha < 1) && (beta > 0) && (beta < 1)) {
	intersect2D[0] = segstart[0]; // correct possible roundoff error
	return new PixelBdyIntersection(intersect2D, intersect3D,
					i1, face_index, alpha, entry);
      }
      double new_error=0.0;
      if (alpha > 1)
	new_error = (alpha-1.0)*(alpha-1.0);
      if (alpha < 0)
	new_error = alpha*alpha;
      if (beta > 1)
	new_error += (beta-1.0)*(beta-1.0);
      if (beta < 0)
	new_error += beta*beta;
      
      if (new_error < error) {
	error = new_error;
	t_segment = i1;
	t_pos = intersect3D;
	t_alpha = alpha > 1.0? 1.0 : 0.0;
	t_face = face_index;
      }
    }
    // If we made it this far, we were never in-bounds.  Return best-guess.
    assert(t_segment != -1);
    return new PixelBdyIntersection(pixplane.convert2Coord2D(t_pos),
				    t_pos, t_segment, t_face, t_alpha, entry);
							    
  } // end if !horizontal
} // end PixelBdyLoop::find_one_intersection

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// findPixelPlaneFacets finds the facets of the intersection of
// a tet with the voxel set boundary that lie in the x, y, and z
// planes.  It works in pixel coordinates (in-plane voxel coordinates).
  
void findPixelPlaneFacets(const VoxelSetBoundary &vsb,
			  const std::vector<Coord> &epts,
			  FacetMap2D &facets)
{
  int nn = epts.size();

  // First find the faces of the intersection that are inside the tet
  // and are therefore made up of faces of the voxel set boundary.
  // These are found by using the 2D code for intersecting 2D pixel
  // set boundary loops with polygons, which is the core of the
  // categoryAreas code.

  // Loop over planes of voxels (pixel planes)
  const PixelSetBoundaryMap &pxlSetBdys = vsb.getPixelSetBdys();
  for(PixelSetBoundaryMap::const_iterator psbm=pxlSetBdys.begin();
	psbm!=pxlSetBdys.end(); ++psbm)
    {
      const PixelPlane &pixplane = (*psbm).first;
      int offset = pixplane.offset;
      int c = pixplane.direction;
      const PixelSetBoundary *psb = (*psbm).second;
      
      // Find the polygon formed by the intersection of the edges of
      // the tet with the c-plane.
      // TODO: We could save a little bit of work by treating both
      // normals together here, instead of computing tetpts twice.
      // But the savings might be small, and the bookkeeping would be
      // more complicated.
      std::vector<TetPlaneIntersectionPoint> tetpts =
	findTetPlaneIntersectionPoints(epts, c, offset);
      int polysize = tetpts.size();
      
      // If there's no intersection, go on to the next plane.
      if(polysize < 3) {
	continue;
      }

      // There might be an intersection, so create a new PixelPlaneFacet
      // object to store it.  It will be deleted by cleanUpFacetMaps() when
      // CSkeletonElement::categoryVolumes() finishes.
      PixelPlaneFacet *facet = new PixelPlaneFacet();
      facets[pixplane] = facet;

      // Make sure that the points are arranged to form a
      // counterclockwise polygon.
      polygonize(tetpts);

      // Find the bounding box of the tet points.  There are either 3
      // or 4 of them.
      assert(polysize == 3 || polysize == 4);
      CRectangle tetBounds(tetpts[0], tetpts[1]);
      tetBounds.swallow(tetpts[2]);
      if(polysize == 4)
	tetBounds.swallow(tetpts[3]);
      
      // Find a perturbation direction, used to resolve ambiguous
      // interiority questions.  The direction can not be parallel to
      // any edge of the tetpts polygon.
      Coord2D perturb;
      const std::vector<Coord2D> * const ptbs = perturbations();
      for(int pt=0; pt<PERTURB_DIRECTIONS; pt++) {
	bool parallel = false;
	for(int el=0; el<nn && !parallel; el++) {
	  Coord2D v = tetpts[(el+1)%nn] - tetpts[el];
	  if((*ptbs)[pt] % v == 0) {
	    parallel = true;
	  }
	}
	if(!parallel) {
	  perturb = (*ptbs)[pt];
	  break; // no need to look at other perturbation directions
	}
      }	// end loop over potential perturbation directions
      assert(perturb != Coord2D(0, 0));

      // Store intersection data -- used to figure out what sections
      // of the polygon boundaries contribute to the area.  Stored a
      // couple of ways -- firstly by element edge, so it can be
      // easily traversed, and secondly indexed by coordinate, so
      // duplicates can be removed.
      ElEdge eledgedata(nn);  // vector of multimap<double,PixelBdyIntersection>
      CoordIsec coordisecs;   // multimap<Coord2D, PixelBdyIntersection>

      // For each loop in the PixelSetBoundary, find its intersection
      // with the polygon formed by tetpts.  This block is copied more
      // or less from the 2D CSkeletonElement::categoryAreas() method.
      // It's not copied verbatim because that code works in physical
      // coordinates, but here we're using pixel coordinates.
      const std::vector<PixelBdyLoop*> loops = psb->get_loops();
	
      for(std::vector<PixelBdyLoop*>::const_iterator pbl=loops.begin();
	  pbl!=loops.end(); ++pbl)
	{
	  const PixelBdyLoop &loop = *(*pbl);
	  // Skip this bdy loop if its bounding box doesn't intersect
	  // the polygon's bounding box.
	  if(!tetBounds.intersects(loop.bbox())) {
	    continue;
	  }

	  // Find the interiority of the start of the first pixel
	  // boundary segment.  End-point interiorities are done on
	  // the fly in the k loop.  Start point interiorities for
	  // every point after the first are the same as the end
	  // point interiority of the previous point.
	  bool pbs_start_inside = interior(tetpts, loop.icoord(0), perturb);
	  
	  int loopsize = loop.size();
	  // Loop over segments of the boundary loop
	  for(unsigned int k=0; k<loopsize; ++k) {
	    const ICoord2D pbs_start = loop.icoord(k);
	    const ICoord2D pbs_end = loop.next_icoord(k);
	    bool pbs_end_inside = interior(tetpts, pbs_end, perturb);

	    if(pbs_start_inside && pbs_end_inside) {
	      // Pixel boundary segment is wholly interior (the
	      // polygon is guaranteed to be convex).
	      facet->addEdge(new PixelFacetCorner(pbs_start, pixplane),
			     new PixelFacetCorner(pbs_end, pixplane));
	    }
	    // If start and end are hetero-interior, so to speak,
	    // then there's an intersection.  Find it.
	    else if(pbs_start_inside != pbs_end_inside) {
	      PixelBdyIntersection *pbi = 
		find_one_intersection(loop, epts, pixplane, k, tetpts,
				      pbs_end_inside);
	      eledgedata[pbi->node_index].insert(
					 ElEdgeDatum(pbi->fraction,pbi));
	      coordisecs.insert(CoordIsecDatum(pbi->location2D, pbi));
	      if(pbs_start_inside) {
		facet->addEdge(new PixelFacetCorner(pbs_start, pixplane),
			       new FaceFacetCorner(pbi->location3D, pbi->face,
						   pixplane));
	      }
	      else {
		facet->addEdge(new FaceFacetCorner(pbi->location3D, pbi->face,
						   pixplane),
			       new PixelFacetCorner(pbs_end, pixplane));
	      }
	    }	// end if bdy segment has exactly one endpoint inside
	    else {
	      assert(!pbs_start_inside && !pbs_end_inside);
	      // The current segment has both endpoints outside the
	      // polygon.  It must intersect zero or two times.
	      // Find out.
	      bool no_isecs = find_no_intersection(loop, k, tetpts, perturb);
	      if(!no_isecs) {
		// We know there have to be two intersections.  Find them.
		// Entry first.
		PixelBdyIntersection *isec0 =
		  find_one_intersection(loop, epts, pixplane, k, tetpts, true);
		eledgedata[isec0->node_index].insert(
				     ElEdgeDatum(isec0->fraction, isec0));
		// Then find the exit.
		PixelBdyIntersection *isec1 =
		  find_one_intersection(loop, epts, pixplane, k, tetpts, false);
		eledgedata[isec1->node_index].insert(
				     ElEdgeDatum(isec1->fraction, isec1));
		// Measure distance along the segment, for
		// coincidence-checking and sorting.
		double d0 = norm2(isec0->location2D - pbs_start);
		double d1 = norm2(isec1->location2D - pbs_start);
		// If two intersections coincide, they should annihilate.
		if(d0 == d1) {
		  if(isec0->entry != isec1->entry) {
		    delete_isec(isec0, eledgedata);
		    delete_isec(isec1, eledgedata);
		  }
		  else {
		    throw ErrProgrammingError(
	      "tetIntersection: Coincident intersections do not annihilate!",
	      __FILE__, __LINE__);
		  }
		}
		// The intersections are not coincident.
		else {
		  // Order the intersections.  Topologically, the
		  // first one has to be an entry, but if they're very
		  // close together, they could come out in the wrong
		  // order by roundoff.  If this happens, they're
		  // within roundoff of each other, and the area is
		  // zero. Delete them.
		  PixelBdyIntersection *one = (d0 < d1 ? isec0 : isec1);
		  PixelBdyIntersection *two = (d0 < d1 ? isec1 : isec0);
		  // Expected case, first intersection is an entry.
		  // Add them to the coordisecs structure and save
		  // the segment.
		  if(one->entry) {
		    coordisecs.insert(CoordIsecDatum(one->location2D, one));
		    coordisecs.insert(CoordIsecDatum(two->location2D, two));
		    facet->addEdge(new FaceFacetCorner(one->location3D,
						       one->face, pixplane),
				   new FaceFacetCorner(two->location3D,
						       two->face, pixplane));
		  }
		  // Pathological case
		  else {
		    delete_isec(one, eledgedata);
		    delete_isec(two, eledgedata);
		  }
		} // end non-coincident, two-intersection case
		
	      } // end if !no_isecs
	    }	// end  both endpoints exterior block
	    
	    // Hand off status info in preparation for next pixel bdy segment
	    pbs_start_inside = pbs_end_inside;
	    
	  } // end loop over segments k
	}   // end loop over pixel boundary loops
      
      // At this point, we have found all the facet edges which are
      // boundaries of the 2D pixel set and are interior to the
      // current polygon. It remains to traverse the polygon exterior
      // and find the portions of it which are between an exit
      // intersection and an entry intersection.

      // But first.. Check for multiple coincident intersections.
      // These can arise when the corner of a polygon and the corner of
      // a pixel boundary coincide, and the perturbation resolution is
      // such that the corner point of the pixel boundary set is
      // inside the polygon, but only by epsilon.  Because each
      // intersection is on a different
      // polygon-segment/pixel-boundary-segment pair, they don't get
      // picked up earlier.  Coincident intersections cannot be
      // ordered, and so are confusing to the traversal code, so we
      // rationalize them here.

      CoordIsec::iterator x = coordisecs.begin();
      while(x != coordisecs.end()) {
	const Coord2D key = (*x).first;
	int ct = coordisecs.count(key);
	if(ct > 1) {
	  CoordIsec::iterator w = x;
	  // Set x to the start of the next key, for the next
	  // iteration of the outer loop.
	  x = coordisecs.upper_bound(key);
	  // Determine the sign of the resultant intersection.  It
	  // may be entry, exit, or zero, if everything cancels out.
	  int entries = 0;
	  int exits = 0;
	  for(CoordIsec::iterator t=w; t!=x; ++t) {
	    if((*t).second->entry)
	      entries++;
	    else
	      exits++;
	  }
	  if(entries > exits) {
	    // Keep the first entry in the set of coincident points,
	    // and delete the rest.
	    bool got_entry = false;
	    for(CoordIsec::iterator t2=w; t2!=x; ++t2) {
	      if((*t2).second->entry && !got_entry)
		got_entry = true;
	      else
		delete_isec((*t2).second, eledgedata);
	    }
	  }
	  else if(entries < exits) {
	    bool got_exit = false;
	    for(CoordIsec::iterator t2=w; t2!=x; ++t2) {
	      if(!(*t2).second->entry && !got_exit)
		got_exit = true;
	      else
		delete_isec((*t2).second, eledgedata);
	    }
	  }
	  else {
	    for(CoordIsec::iterator t2=w; t2!=x; ++t2)
	      delete_isec((*t2).second, eledgedata);
	  }
	} // end if ct > 1
	else {		// Key only occurs once, move on.
	  ++x;
	}
      } // end search for multiple coincident intersections
      
      // Also check for multiple intersections where more than one
      // pixel boundary segment intersects a polygon edge at the same
      // spot.  These ought to cancel each other.  If they're left
      // in, the loop below might see them in the wrong order, and
      // get confused about the sequence of entries and exits.
      for(int ni=0; ni<nn; ni++) { // loop over edges
	ElEdgeMap::iterator ii = eledgedata[ni].begin();
	while(ii != eledgedata[ni].end()) {
	  double frac = (*ii).first; // parametric position of intersection
	  int ninter = eledgedata[ni].count(frac);
	  if(ninter > 1) {
	    // coincidences detected
	    std::pair<ElEdgeMap::iterator, ElEdgeMap::iterator> range =
	      eledgedata[ni].equal_range(frac);
	    int entries = 0;
	    int exits = 0;
	    for(ElEdgeMap::iterator k=range.first; k!=range.second; ++k) {
	      if((*k).second->entry)
		entries++;
	      else
		exits++;
	    }
	    if(entries != exits) {
	      // entries-exits can never be something other than -1,
	      // 0, or 1, because the directions and number of pixel
	      // boundary segments at a point are limited.  This
	      // code is actually more general than it needs to be.
	      bool keep_entry = entries > exits;
	      bool found_one = false;
	      for(ElEdgeMap::iterator j=range.first; j!=range.second; ++j) {
		if((*j).second->entry == keep_entry && !found_one)
		  found_one = true;
		else
		  eledgedata[ni].erase(j);
	      }
	    }
	    else {	   // entries == exits
	      eledgedata[ni].erase(range.first, range.second);
	    }
	    ii = range.second; // go on to next frac
	  } // end if ninter > 1
	  else { // only one intersection at this frac
	    ++ii;
	  }
	} // end loop over intersections on this edge
      } // end loop over edges ni
	// Done with coincidence check
      
      // Now traverse the boundary of the polygon, recording the
      // segments that are between an exit and an entry.  "exit" means
      // that the pixel set boundary segment is exiting the polygon.
      // (When the pixel set boundary is outside the polygon, the
      // boundary of the intersection follows the polygon.)

      int icount = 0;		// number of intersections
      for(int n=0; n<nn; n++) { // loop over polygon edges
	icount += eledgedata[n].size();
      }
      if(icount > 0) {
	// First, find a point where the pixel boundary exits the polygon.
	bool started = false;	// has the inner loop been started?
	// for(ElEdge::const_iterator startedgep=eledgedata.begin();
	//     startedgep!=eledgedata.end() && !started; ++startedgep)
	for(unsigned int startedgeno=0;
	    startedgeno<eledgedata.size() && !started; ++startedgeno)
	  {
	    const ElEdgeMap &edgemap = eledgedata[startedgeno];
	    for(ElEdgeMap::const_iterator edgedatum=edgemap.begin();
		edgedatum!=edgemap.end() && !started; ++edgedatum)
	      {
		const PixelBdyIntersection *pbi = (*edgedatum).second;
		if(!pbi->entry) {
		  // Exit point discovered.  Start traversing the
		  // polygon.  This looks like a doubly nested loop,
		  // but it's not. The outer loops will exit after
		  // this inner loop is executed.
		  started = true;
		  bool done = false;
		  unsigned int edgeno = startedgeno;
		  Coord3D starting_point = pbi->location3D;
		  unsigned int face = tetpts[edgeno].sharedFace(
							tetpts[(edgeno+1)%nn]);
		  FacetCorner *exitpt =
		    new FaceFacetCorner(starting_point, face, pixplane);
		  ElEdgeMap::const_iterator here = edgedatum;
		  ++here;
		  while(!done) {
		    if(exitpt) {
		      // here is the start of a segment of the
		      // intersection boundary that follows the polygon
		      // boundary.  It ends at the next entry
		      // intersection or corner of the polygon.
		      if(here == eledgedata[edgeno].end()) {
			// intersection bdy segment ends at polygon corner
			edgeno = (edgeno + 1) % nn;
			Coord3D cornerpt =
			  pixplane.convert2Coord3D(tetpts[edgeno]);
			facet->addEdge(exitpt,
				       new EdgeFacetCorner(cornerpt, face,
							   tetpts[edgeno],
							   pixplane));
			// Go to next polygon edge/tet face
			face = tetpts[edgeno].sharedFace(tetpts[(edgeno+1)%nn]);
			here = eledgedata[edgeno].begin();
			// We already know the beginning of the next segment:
			exitpt = new EdgeFacetCorner(cornerpt, face,
						     tetpts[edgeno],
						     pixplane);
		      }
		      else {	// not at the end of the edge
			// intersection bdy segment ends at entry on same edge
			assert((*here).second->entry);
			facet->addEdge(
			      exitpt,
			      new FaceFacetCorner((*here).second->location3D,
						  face, pixplane));
			exitpt = 0;
			++here;
		      }
		    } // end if exitpt (ie, we're looking for the next entry)
		    else {
		      // exitpt == 0.  Look for the next exit point.
		      if(here == eledgedata[edgeno].end()) {
			// go to the next polygon edge/tet face
			edgeno = (edgeno + 1) % nn;
			face = tetpts[edgeno].sharedFace(tetpts[(edgeno+1)%nn]);
			here = eledgedata[edgeno].begin();
		      }
		      else {	// not at the end of the edge
			assert(!(*here).second->entry);
			Coord3D pt = (*here).second->location3D;
			if(pt == starting_point) {
			  done = true;
			}
			else {
			  exitpt = new FaceFacetCorner(pt, face, pixplane);
			  ++here;
			}
		      }
		    } // end if exitpt else
		  } // end while !done
		}   // end if found initial exit point
	      }	// end search over edge for initial exit point
	  } // end search over edges startedgep for initial exit point

	// If started is still false, no initial exit point was found,
	// although we know there are intersections.
	if(!started)
	  throw ErrProgrammingError("No exit.", __FILE__, __LINE__);
      }   // end if icount > 0 (ie, there are intersections)
      
      else {
	// If there are no intersections, we either need to include
	// all of the tetpts polygon, or none of it.
	//
	// If the polygon encloses the pixel set boundary, the
	// boundary edges will already have been included in
	// intersection facet, and we don't have to do anything.  The
	// area of the facet computed from the current set of edges is
	// positive.
	//
	// If the polygon is entirely inside the pixel set and there
	// are no holes in the pixel set within the polygon, the
	// polygon is homogeneous and its entire boundary is the
	// entire intersection boundary.  This situation is detected
	// in CSkeletonElement::categoryVolumes when all categories
	// have zero area.  It's hard to detect this here.
	//
	// If the polygon is entirely inside the pixel set, but there
	// are holes within the polygon (ie, the pixel set is annular
	// and the polygon edges lie within the annulus and surround
	// the hole), then the entire boundary must be included.  The
	// area computed so far will be *negative*, because it's made
	// up of holes.  This is the only case that has to be handled
	// here.
	if(facet->area() < 0.0) {
	  for(int i=0; i<polysize-1; i++) {
	    unsigned int face = tetpts[i].sharedFace(tetpts[i+1]);
	    facet->addEdge(
		   new EdgeFacetCorner(pixplane.convert2Coord3D(tetpts[i]),
				       face, tetpts[i], pixplane),
		   new EdgeFacetCorner(pixplane.convert2Coord3D(tetpts[i+1]),
				       face, tetpts[i+1], pixplane));
	  }
	  unsigned int face = tetpts[polysize-1].sharedFace(tetpts[0]);
	  facet->addEdge(new EdgeFacetCorner(
			     pixplane.convert2Coord3D(tetpts[polysize-1]),
			     face, tetpts[polysize-1], pixplane),
			 new EdgeFacetCorner(
			     pixplane.convert2Coord3D(tetpts[0]),
			     face, tetpts[0], pixplane));
	} // end if facet area < 0
      }
    } // end loop over planes in the c direction
}     // end findPixelPlaneFacets()


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// Compute the volume, in voxel units, of the intersection of the
// voxel set with the tetrahedron with the given corners.  The facets
// of the intersection that lie on pixel planes are also given.

double tetIntersectionVolume(const VoxelSetBoundary &vsb, 
			     const std::vector<Coord3D> &epts,
			     const FacetMap2D &facets,
			     unsigned int category)
{
  double vol = 0;
  Coord3D center = 0.25*(epts[0] + epts[1] + epts[2] + epts[3]);

  std::set<FacetEdge> unmatchedEdges;

  // Loop over pixel plane facets
  for(FacetMap2D::const_iterator fm=facets.begin(); fm!=facets.end(); ++fm) {
    const PixelPlane &pixplane = (*fm).first;
    const PixelPlaneFacet *facet = (*fm).second;

    // Make the facet's contribution to the volume
    vol += (facet->area() * pixplane.normal *
	    (pixplane.offset - center[pixplane.direction]))/3.0;

    // Find the edges of the facet, keeping only those that don't
    // match opposite direction edges from other facets.  The
    // *reversed* edges are stored in unmatchedEdges, so that they can
    // later be used directly as edges for new facets.
    for(std::vector<FacetEdge>::const_iterator edge=facet->begin();
	edge!=facet->end(); ++edge)
      {
	std::set<FacetEdge>::iterator match = unmatchedEdges.find(*edge);
	if(match == unmatchedEdges.end()) {
	  FacetEdge reversed = (*edge).reversed();
	  unmatchedEdges.insert(reversed);
	}
	else {
	  unmatchedEdges.erase(match);
	}
      }	// end loop over edges of the facet
  } // end loop over pixel plane facets

  // The edges in unmatchedEdges must be the boundaries of
  // intersection facets on the tet faces. There may be mising
  // segments, which must be along the edges of the tet, and which we
  // will have to find.

  // Sort the unmatched edges by tet face. 
  std::vector< std::set<FacetEdge> > faceFacetEdges(NUM_TET_FACES);
  for(std::set<FacetEdge>::const_iterator edge=unmatchedEdges.begin();
      edge!=unmatchedEdges.end(); ++edge)
    {
      const FaceFacetCorner *c0 =
	dynamic_cast<const FaceFacetCorner*>((*edge).start);
      const FaceFacetCorner *c1 =
	dynamic_cast<const FaceFacetCorner*>((*edge).end);

#ifdef DEBUG
      if(c0 == NULL || c1 == NULL)
	throw ErrProgrammingError(
		  "Unmatched polyhedron edge is not on an element face.",
		  __FILE__, __LINE__);
      if(c0->face != c1->face)
	throw ErrProgrammingError(
		  "Endpoints of unmatched polyhedron edge are on different element faces.",
		  __FILE__, __LINE__);
#endif	// DEBUG
      faceFacetEdges[c0->face].insert(*edge);
    }
  
  // Loop over tet faces, constructing a polygon on the face from the
  // unmatched edges found above.  There may be missing segments, but
  // only along the edges of the original tet.  Add those segments if
  // necessary. 
 
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    // Find the unmatched endpoints of the FacetEdges on this face.
    // Sort them by the tet edges that they're on.  Loop over the
    // endpoints on each tet edge.  If the midpoint of the segment
    // between one point and the next is in the category, then add the
    // segment between those points to the facet boundary.  Include
    // the endpoints of the tet edge in the set of points being
    // considered.  (This will work even if there are no intersections
    // on an edge, so it's not necessary to consider the blank faces
    // first!  Adding edges to neighboring faces may save time, but is
    // not necessary.)  When computing whether the midpoint is in the
    // category, it may benecessary to perturb it off of a voxel
    // boundary.  Be sure to perturb it towards the center of the tet.

    // We don't have to check that a segment along a tet edge isn't
    // already present.  This can happen only if the tet face lies in
    // a voxel plane at a boundary between voxels.  But if the face
    // lies in a plane like that, then the tet edges for the facet in
    // that plane are the same as the TetIntersectionPoint polygon,
    // and have been included.  Therefore we don't have to do anything
    // here, except to ignore the facet.

    if(!faceIsOnVoxelPlane(f, epts)) {

      // For each edge e of this face, edgePos[e] is a set containing
      // the parametric position (along the edge) of a possible start
      // or end of a boundary segment. 
      std::vector<std::set<double> > edgePos(NUM_TET_FACE_EDGES);
      
      for(std::set<FacetEdge>::const_iterator s=faceFacetEdges[f].begin();
	  s!=faceFacetEdges[f].end(); ++s)
	{
	  const EdgeFacetCorner *corner0 =
	    dynamic_cast<const EdgeFacetCorner*>((*s).start);
	  if(corner0 != 0) {
	    edgePos[corner0->edge()].insert(corner0->edgePosition());
	  }
	  const EdgeFacetCorner *corner1 =
	    dynamic_cast<const EdgeFacetCorner*>((*s).end);
	  if(corner1 != 0) {
	    edgePos[corner1->edge()].insert(corner1->edgePosition());
	  }
	}

      bool normalComputed = false; // we might not need it.
      Coord3D normal;
      
      for(unsigned int edge=0; edge<3; edge++) {
	// "edge" is the face index of the edge, not the tet index of
	// the edge.  "edgeid" is the tet index.  "edge" runs from
	// 0-2, but edgeid runs from 0-5.
	unsigned int edgeid = CSkeletonElement::faceEdges[f][edge]; 

	// edgePos[e] needs to include the end points of the edge.
	edgePos[edge].insert(0.0);
	edgePos[edge].insert(1.0);

	Coord3D node0 = epts[vtkTetra::GetEdgeArray(edgeid)[0]];
	Coord3D node1 = epts[vtkTetra::GetEdgeArray(edgeid)[1]];
					       
	// The parametric position t of an edge intersection is assigned
	// in findTetPlaneIntersectionPoints assuming that the edge
	// direction is given by the order of the points in
	// vtkTetra::GetEdgeArray.  That's not necessarily the direction
	// that makes the edges go around the face counterclockwise
	// (with an outward normal).  Fix that.  faceEdgeDirs is -1 if
	// the edge has a different direction when viewed as a face edge
	// than as a tet edge.
	bool reversed = CSkeletonElement::faceEdgeDirs[f][edge] == -1;

	// Look at pairs of adjacent intersections on the edge, and
	// decide if the segment between them should be included.
	// std::set is a sorted container, so iterating over it
	// returns the elements in increasing order.
	std::set<double>::const_iterator segstart = edgePos[edge].begin();
	std::set<double>::const_iterator segend = segstart;
	++segend;
	while(segend != edgePos[edge].end()) {
	  double tmid = 0.5*(*segend + *segstart);
	  Coord3D midpt = (1-tmid)*node1 + tmid*node1;
	  // midpt is a Coord3D, but it's already in voxel units.  If
	  // it's on a voxel edge, choose the voxel toward the
	  // interior of the element.
	  ICoord vxl(midpt[0], midpt[1], midpt[2]); // truncates 
	  for(unsigned int c=0; c<3; c++) {
	    // See comment in faceIsOnVoxelPlane about whether or not
	    // this is a robust way of determining if the midpoint is
	    // on a voxel edge.
	    if(midpt[c] == vxl[c]) {
	      if(!normalComputed) {
		normal = faceNormal(f, epts); // outward normal
		normalComputed = true;
	      }
	      if(normal[c] > 0) {
		// The outward normal is in the +c direction, so the
		// interior pixel we're interested in is behind us.
		vxl[c] -= 1;
	      }
	    }
	  
	    if(vxl[c] == vsb.microstructure->sizeInPixels()[c])
	      vxl[c] -= 1;
	  } // end loop over directions c to adjust the midpoint
	
	  if(vsb.microstructure->category(vxl) == category) {
	    Coord3D s0 = (1-*segstart)*node0 + (*segstart)*node1;
	    Coord3D s1 = (1-*segend)*node0 + (*segend)*node1;
	    if(!reversed)
	      faceFacetEdges[f].insert(FacetEdge(new SimpleFacetCorner(s0),
						 new SimpleFacetCorner(s1)));
	    else
	      faceFacetEdges[f].insert(FacetEdge(new SimpleFacetCorner(s1),
						 new SimpleFacetCorner(s0)));
	  }
	
	  segstart = segend;
	  ++segend;
	} // end loop over segments (segstart, segend) along edge 
      }	  // end loop over edges, edge
    }	  // end if face is not on a voxel plane
  }	  // end loop over faces f

  // Now that all polygons are complete, compute their areas and their
  // contributions to the volume. 

  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    Coord3D facecenter;
    const std::set<FacetEdge> &edges = faceFacetEdges[f];
    if(!edges.empty()) {
      for(std::set<FacetEdge>::const_iterator s=edges.begin(); s!=edges.end();
	  ++s)
	{
	  facecenter += (*s).start->position3D();
	  facecenter += (*s).end->position3D();
	}
      facecenter /= 2.0 * edges.size();
      Coord3D area;
      for(std::set<FacetEdge>::const_iterator s=edges.begin(); s!=edges.end();
	  ++s)
	{
	  area += (((*s).start->position3D() - facecenter) %
		   ((*s).end->position3D() - facecenter));
	}
      // factor of 1/2 for area, 1/3 for volume of pyramid
      vol += dot(area, facecenter - center)/6.0;
      
    } // end if !edges.empty()
  } // end loop over faces, accumulating areas and volumes

  // If the volume is negative, then there must be a hole in the
  // middle of the tet and no intersections with any tet edges.  Add
  // the volume of the entire tet.
  if(vol < 0.0)
    // WTF doesn't vtk use const correctly?
    vol += vtkTetra::ComputeVolume(const_cast<double*>(epts[0].xpointer()),
				   const_cast<double*>(epts[1].xpointer()),
				   const_cast<double*>(epts[2].xpointer()),
				   const_cast<double*>(epts[3].xpointer()));
  
  return vol;
} // end tetIntersectionVolume


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


std::ostream &operator<<(std::ostream &os, const PixelBdyIntersection &pbi) {
  int prec = os.precision();
  os << std::setprecision(20);
  os << "PixelBdyIntersection(" << pbi.location2D
     << ", " << pbi.location3D
     << ", fraction=" << pbi.fraction << ", "
     << (pbi.entry? "entry" : "exit") << ")";
  os << std::setprecision(prec);
  return os;
}

