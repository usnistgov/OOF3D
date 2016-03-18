// -*- C++ -*-
// $RCSfile: coincidences.C,v $
// $Revision: 1.1.2.5 $
// $Author: langer $
// $Date: 2015/12/04 19:06:29 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

OBSOLETE

#include <oofconfig.h>

#include "common/IO/oofcerr.h"
#include "common/tostring.h"
#include "engine/coincidences.h"

// Routines that resolve coincident vertices when computing the
// intersection of a voxel set boundary (VSB) with the polygon formed
// by the intersection of a tetrahedron and a pixel plane.  If
// intersection points are in topologically impossible configurations,
// they're assumed to be that way because of round-off error, and the
// points actually are exactly coincident.

// These routines belong in tetintersection.C, but that file was
// getting to be much too long.

typedef std::multimap<PixelBdyLoopSegment,PixelBdyIntersection*> LoopSegIsecs;
typedef std::multimap<unsigned int, PixelBdyIntersection*> PolySegIsecs;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility functions for deleting intersections from the ordered
// lists of intersections.

static void delete_isec(const PixelBdyIntersection *pbi,
			std::vector<ElEdgeMap> &eledge)
{
  int ni = pbi->segment;
  double fr = pbi->fraction;
  
  int count = eledge[ni].count(fr);
  if(count==1) {
    eledge[ni].erase(fr);
    return;
  }
  else {
    ElEdgeMap::iterator emi = eledge[ni].lower_bound(fr);
    for(int i=0; i<count; ++emi, ++i) {
      if(nearby((*emi).second->location2D, pbi->location2D) && 
	 (*emi).second->entry==pbi->entry)
	{
	  eledge[ni].erase(emi);
	  return;
	}
    }
  }
  throw ErrProgrammingError("delete_isec failed!", __FILE__, __LINE__);
}

// Clean up routine when deleting a pair of coincident intersections.

static void delete_isec_pair(const PixelBdyIntersection *pbi0,
			     const PixelBdyIntersection *pbi1,
			     std::vector<ElEdgeMap> &eledgedata,
			     BaryCoordMap &baryEquiv,
			     PixelPlaneFacet *facet)
{
  // If one of the points is on a tet edge, ignoring the infinitesimal
  // segment that joins the other point to the edge may cause problems
  // later in tetIntersectionFaceFacets(), because a sequence of
  // connected edges on the face will not end at an edge.  baryEquiv
  // indicates that the point that's not on the edge is equivalent to
  // the one that is, as far as tetIntersectionFaceFacets() is
  // concerned.
  bool onEdge0 = pbi0->baryCoord.onEdge();
  bool onEdge1 = pbi1->baryCoord.onEdge();
  if(onEdge0 && !onEdge1)
    baryEquiv[pbi1->baryCoord] = pbi0->baryCoord;
  else if(onEdge1 && !onEdge0)
    baryEquiv[pbi0->baryCoord] = pbi1->baryCoord;

  delete_isec(pbi0, eledgedata);
  delete_isec(pbi1, eledgedata);

  // TODO: This may be slow.
  facet->removeEdge(pbi0->location3D, pbi1->location3D);
}

static void delete_isec_pair_on_loop_segment(
			     const PixelBdyLoopSegment &loopseg,
			     LoopSegIsecs &loopSegIsecs,
			     std::vector<ElEdgeMap> &eledgedata,
			     std::set<PixelBdyIntersection*> &deleted,
			     BaryCoordMap &baryEquiv,
			     PixelPlaneFacet *facet)
{
  auto range = loopSegIsecs.equal_range(loopseg);
  PixelBdyIntersection *pbi0 = (*range.first).second;
  PixelBdyIntersection *pbi1 = (*++range.first).second;
  delete_isec_pair(pbi0, pbi1, eledgedata, baryEquiv, facet);
  deleted.insert(pbi0);
  deleted.insert(pbi1);
  loopSegIsecs.erase(range.first, range.second);
}

// This version is used when the PixelBdyIntersections aren't on the
// same VSB segment. 

static void delete_isec_pair(const PixelBdyIntersection *pbi0,
			     const PixelBdyIntersection *pbi1,
			     const ICoord2D &corner,
			     bool interiorCorner,
			     std::vector<ElEdgeMap> &eledgedata,
			     BaryCoordMap &baryEquiv,
			     PixelPlaneFacet *facet,
			     const PixelPlane &pixplane,
			     unsigned int onFace
#ifdef DEBUG
			     , bool verbose
#endif // DEBUG
			     )
{
  //assert(!pbi0->sameLoopSegment(pbi1));
  delete_isec_pair(pbi0, pbi1, eledgedata, baryEquiv, facet);

  if(!pbi0->sameLoopSegment(pbi1)) {
    // It's also necessary to remove short edges from the
    // PixelPlaneFacet, because if the points are in the wrong order
    // the edges can make infinitesimal and incorrect negative
    // contributions to the area.  (If those happen to be the only
    // contributions to the area, then they'll lead to an incorrect
    // negative area correction, below.)
		
    // Short facet edges are only created when the VSB segments
    // intersect at a point inside the polygon.  We know that only two
    // VSB edges meet at this coincidence, so we can use the location
    // of their intersection to identify the segments of the facet
    // that should be deleted.
    if(interiorCorner) {
#ifdef DEBUG
      if(verbose) {
	oofcerr << "delete_isec_pair: calling removeEdgesAtPoint" << std::endl;
	oofcerr << "delete_isec_pair:   pbi0=" << *pbi0 << std::endl;
	oofcerr << "delete_isec_pair:   pbi1=" << *pbi1 << std::endl;
#endif // DEBUG
      }
      // TODO: This may be slow.
      facet->removeEdgesAtPoint(pixplane.convert2Coord3D(corner),
				pbi0->location3D, pbi1->location3D
#ifdef DEBUG
				, verbose
#endif // DEBUG
				);
    }
  }
}



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static bool interior(const ICoord2D &pt, const PixelPlane &pixplane,
		     const std::vector<Coord3D> &epts,
		     unsigned int onFace,
		     const std::vector<const PixelPlane*> &facePlanes,
		     BaryCoordCache &barycache)
{
  BarycentricCoord b = getBarycentricCoord(pt, pixplane, epts,
					   facePlanes, barycache);
  return b.interior(onFace);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given two PixelBdyIntersections on contiguous VSB segments, return
// the one that precedes the other when traversing the VSB in the
// positive direction.

static PixelBdyIntersection *firstIntersection(PixelBdyIntersection *pbi0,
					       PixelBdyIntersection *pbi1)
{
  assert(pbi0 != pbi1);
  // PixelBdyIntersection::loopseg is the index in PixelBdyLoop of the
  // point at the beginning of the loop segment.  The two segments can
  // be in different loops if the loops meet at a corner.
  const PixelBdyLoop *loop0 = pbi0->loop;
  const PixelBdyLoop *loop1 = pbi1->loop;
  if(loop0->next_icoord(pbi0->loopseg) == loop1->icoord(pbi1->loopseg)) {
    return pbi0;
  }
#ifdef DEBUG
  if(loop1->next_icoord(pbi1->loopseg) != loop0->icoord(pbi0->loopseg)) {
    // oofcerr << "firstIntersection: pbi0=" << *pbi0 << std::endl;
    // oofcerr << "firstIntersection: pbi1=" << *pbi1 << std::endl;
    // throw ErrProgrammingError("Loop segments are not contiguous!",
    // 			      __FILE__, __LINE__);
    return NULL;
  }
#endif // DEBUG
  return pbi1;
}

static const PixelBdyLoopSegment *firstSegment(const PixelBdyLoopSegment *seg0,
					       const PixelBdyLoopSegment *seg1)
{
  if(seg0->firstPt() == seg1->secondPt())
    return seg1;
  if(seg1->firstPt() == seg0->secondPt())
    return seg0;
  return NULL;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

enum TurnDirection {LEFT=0, RIGHT=1, STRAIGHT=2, REVERSE=3, UNDEFINED=4};

static TurnDirection turnDirection(const PixelBdyLoopSegment &seg0,
				   const PixelBdyLoopSegment &seg1)
{
  assert(firstSegment(&seg0, &seg1) == &seg0);
  ICoord2D a = seg0.secondPt() - seg0.firstPt();
  ICoord2D b = seg1.secondPt() - seg1.firstPt();
  int crossprod = cross(a, b);
  if(crossprod > 0)
    return LEFT;
  if(crossprod < 0)
    return RIGHT;
  if(dot(a, b) < 0)
    return REVERSE;
  return STRAIGHT;
}

static TurnDirection turnDirection(const PixelBdyIntersection *pbi0,
				   const PixelBdyIntersection *pbi1)
{
  return turnDirection(pbi0->getLoopSeg(), pbi1->getLoopSeg());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given two PixelBdyIntersections assumed to be on adjacent segments
// of a VSB, find out which one comes first when traversing the VSB,
// and whether they make a right or left turn.

static void classifyVSBcorner(PixelBdyIntersection *pbi0,
			      PixelBdyIntersection *pbi1,
			      PixelBdyIntersection *&entryPt,
			      PixelBdyIntersection *&exitPt,
			      PixelBdyIntersection *&firstPt,
			      PixelBdyIntersection *&secondPt,
			      ICoord2D &corner,
			      TurnDirection &turndir)
{
  assert(pbi0 != pbi1);
  assert(pbi0->entry != pbi1->entry);
  if(pbi0->entry) {
    entryPt = pbi0;
    exitPt = pbi1;
  }
  else {
    entryPt = pbi1;
    exitPt = pbi0;
  }
  firstPt = firstIntersection(entryPt, exitPt);
  if(firstPt == NULL) {
    secondPt = NULL;
    turndir = UNDEFINED;
  }
  else {
    secondPt = (firstPt == entryPt ? exitPt : entryPt);
    corner = firstPt->loop->next_icoord(firstPt->loopseg);
    turndir = turnDirection(firstPt, secondPt);
#ifdef DEBUG
    if(turndir == STRAIGHT) {
      oofcerr << "classifyVSBcorner: pbi0=" << *pbi0 << std::endl;
      oofcerr << "classifyVSBcorner: pbi1=" << *pbi1 << std::endl;
      throw ErrProgrammingError("classifyVSBcorner failed!",
				__FILE__, __LINE__);
    }
#endif // DEBUG
    assert(turndir != STRAIGHT);
  }
}

static void classifyVSBcorner(const PixelBdyLoopSegment &seg0,
			      const PixelBdyLoopSegment &seg1,
			      PixelBdyLoopSegment &firstSeg,
			      PixelBdyLoopSegment &secondSeg,
			      ICoord2D &corner,
			      TurnDirection &turndir)
{
  // oofcerr << "classifyVSBcorner:" << std::endl;
  // oofcerr << "classifyVSBcorner: seg0=" << seg0 << std::endl;
  // oofcerr << "classifyVSBcorner: seg1=" << seg1 << std::endl;
  const PixelBdyLoopSegment *first = firstSegment(&seg0, &seg1);
  // oofcerr << "classifyVSBcorner: first=" << first << std::endl;
  if(first == NULL)
    turndir = UNDEFINED;
  else {
    if(first == &seg0) {
      turndir = turnDirection(seg0, seg1);
      firstSeg = seg0;
      secondSeg = seg1;
    }
    else {
      turndir = turnDirection(seg1, seg0);
      firstSeg = seg1;
      secondSeg = seg0;
    }
    corner = first->loop()->next_icoord(first->loopseg());
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// These methods check for the illegal topology created by round-off
// error at coincident pairs of points.

// vsbCornerCoincidence checks two intersections that are on the
// same segment of the polygon.


//             / polygon segment
//            /
//         --o--------------- VSB segment
//         |/
//         o
//        /|
//       / |
//      /  |
//     /   |
//         |

static bool vsbCornerCoincidence(PixelBdyIntersection *pbi0,
				 PixelBdyIntersection *pbi1,
#ifdef DEBUG
				 bool verbose,
#endif // DEBUG
				 ICoord2D &corner)
{
  assert(pbi0 != pbi1);
  assert(pbi0->segment == pbi1->segment);
  assert(!pbi0->sameLoopSegment(pbi1));
  assert(pbi0->entry != pbi1->entry);
  PixelBdyIntersection *entryPt, *exitPt, *firstPt, *secondPt;
  TurnDirection turn;
  classifyVSBcorner(pbi0, pbi1, entryPt, exitPt, firstPt, secondPt,
		    corner, turn);
  // If the two voxel set boundary segments make a right turn, we
  // expect the entry point to be before the exit when traversing the
  // polygon boundary (no matter which way the polygon boundary goes).
  // If they make a left turn, the exit must be before the entry.
  return ((turn == LEFT && entryPt->fraction <= exitPt->fraction)
	  ||
	  (turn == RIGHT && entryPt->fraction >= exitPt->fraction)
	  ||
	  (turn == REVERSE && entryPt->fraction == exitPt->fraction)
	  );
}


// polyCornerCoincidence checks two intersections on the same VSB loop
// segment but different polygon segments.

//               
//            /\
//  ---------o--o------------ VSB segment
//          /    \
//         /      \
//        /        \ polygon segments
//       /  
//      /   
//          

static bool polyCornerCoincidence(PixelBdyIntersection *pbi0,
				  PixelBdyIntersection *pbi1
#ifdef DEBUG
				  , bool verbose
#endif // DEBUG
				  )
{
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "polyCornerCoincidence:"  << std::endl;
// #endif // DEBUG
  assert(pbi0 != pbi1);
  assert(pbi0->segment != pbi1->segment);
  assert(pbi0->sameLoopSegment(pbi1));
  assert(pbi0->entry != pbi1->entry);
  return ((pbi0->entry && pbi0->loopfrac >= pbi1->loopfrac) ||
	 (pbi1->entry && pbi1->loopfrac >= pbi0->loopfrac));
}


//  Coincident polygon corner and VSB corner.  There are three legal
//  possibilities for the polygon edge geometry, each of which can
//  exist with either direction of the VSB boundary.

//                   _/                  |
//    polygon      _/polygon       poly  |  polygon
//    exterior   _/  interior      int.  |  exterior
//             _/                        |
//          --o-------------          ---o-----------
//          |@ <- polygon             |  |
//          o     corner              | /
//         /|                         |/
//        / |                         o
//       /  |                        /|
//          |                       / |

//
//
//   @_
//   | \_
//   \_  \_                              The straight line directions available 
//     |   \_                            to the ascii artist are limited.
//     \_    \_   
//       |  ---o------------
//       \_ |    \_
//         ||      \_
//          o_ poly
//          | | int.
//          | \_
//          |
//          |

static bool polyVSBCornerCoincidence(
			     PixelBdyIntersection *pbi0,
			     PixelBdyIntersection *pbi1,
#ifdef DEBUG
			     bool verbose,
#endif // DEBUG
			     const PixelPlane &pixplane,
			     const std::vector<Coord3D> &epts,
			     const std::vector<const PixelPlane*> &facePlanes,
			     unsigned int onFace,
			     BaryCoordCache &baryCache,
			     ICoord2D &corner)
{
  // TODO: corner arg is unnecessary?  It's not used by the callers.
  assert(pbi0 != pbi1);
  assert(!pbi0->sameLoopSegment(pbi1));
  assert(pbi0->segment != pbi1->segment);
  assert(pbi0->entry != pbi1->entry);
  PixelBdyIntersection *entryPt, *exitPt, *firstPt, *secondPt;
  TurnDirection turn;
  classifyVSBcorner(pbi0, pbi1, entryPt, exitPt, firstPt, secondPt,
		    corner, turn);
  BarycentricCoord bcorner = getBarycentricCoord(corner, pixplane, epts,
						 facePlanes, baryCache);
  // If the VSB corner is interior to the polygon, the entry point
  // must precede the exit point on the VSB. If the VSB corner is
  // outside, the entry and exit must be in the opposite order.  If
  // the order is wrong, the points must coincide, and this function
  // returns true.
  bool inside = bcorner.interior(onFace);
  bool invalid = ((inside && exitPt == firstPt) ||
		  (!inside && entryPt == secondPt));
#ifdef DEBUG
  if(verbose) {
    oofcerr << "polyVSBCornerCoincidence: pbi0=" << pbi0 << " pbi1=" << pbi1
	    << " inside=" << inside << std::endl;
    oofcerr << "                        : firstPt=" << firstPt
	    << " secondPt=" << secondPt << std::endl;
    oofcerr << "                        : entryPt=" << entryPt
	    << " exitPt=" << exitPt << std::endl;
    oofcerr << "                        : returning invalid=" << invalid
	    << std::endl;
  }
#endif // DEBUG
  
  return invalid;
} // end polyVSBCornerCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void resolveTwoFoldCoincidence(
       unsigned int nEntries, unsigned int nExits,
       const std::pair<CoordIsec::iterator, CoordIsec::iterator> &range,
       const std::vector<Coord3D> &epts,
       std::vector<ElEdgeMap> &eledgedata,
       BaryCoordMap &baryEquiv,
       PixelPlaneFacet *facet,
       const PixelPlane &pixplane,
       unsigned int onFace,
       const std::vector<const PixelPlane*> &facePlanes,
       BaryCoordCache &baryCache
#ifdef DEBUG
	 , bool verbose
#endif	// DEBUG
			       )
{
  PixelBdyIntersection *pbi0 = (*range.first).second;
  CoordIsec::iterator p = range.first;
  ++p;
  PixelBdyIntersection *pbi1 = (*p).second;

  if(nEntries == 0 || nExits == 0) {
    // Intersections are redundant.  A polygon edge or corner lies at
    // the junction between two VSB loop segments, and was counted
    // twice.  This only applies if both intersections have a common
    // polygon segment or a common VSB loop segment.
    if(pbi0->segment == pbi1->segment || pbi0->sameLoopSegment(pbi1)) {
      pbi0->baryCoord = mergeBary(pbi0->baryCoord, pbi1->baryCoord);
      delete_isec(pbi1, eledgedata);
    }
  }
	
  else {			// nEntries == nExits == 1
    // A polygon corner lies close to a VSB edge, or vice versa.  One
    // boundary exits and enters again (or vice versa).

    if(pbi0->segment == pbi1->segment) {
      // Both intersections are on the same polygon segment.

      // Check that the intersections occur in the correct order.  If
      // they don't, then they've been misplaced due to round-off
      // error, and should actually coincide.  In fact, when this
      // happens we can ignore the intersections entirely: they won't
      // mark a point where an facet edge will start or end on the
      // polygon boundary.
      ICoord2D corner;
      if(vsbCornerCoincidence(pbi0, pbi1,
#ifdef DEBUG
			      verbose,
#endif // DEBUG
			      corner))
	{
	  // The intersection points appear in the wrong order.
	  // They're actually just one point.  Remove the
	  // intersections from eledgedata, since they're not needed
	  // for the pixel plane facet.
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "resolveTwoFoldCoincidence: vsbCornerCoincidence!"
		    << std::endl;
	    oofcerr << "       : pbi0=" << *pbi0 << std::endl;
	    oofcerr << "       : pbi1=" << *pbi1 << std::endl;
	  }
#endif // DEBUG
	  bool interiorCorner = interior(corner, pixplane, epts,
					 onFace, facePlanes, baryCache);
	  delete_isec_pair(pbi0, pbi1, corner, interiorCorner, eledgedata,
			   baryEquiv, facet, pixplane, onFace
#ifdef DEBUG
			   , verbose
#endif // DEBUG
			   );
	}
    } // end if both intersections share a polygon segment

    else if(pbi0->sameLoopSegment(pbi1)) {
      // Both intersections are on the same VSB loop segment.  The
      // segment must enter the polygon before it exits, because the
      // polygon is convex.  If it doesn't, then round-off error has
      // put the points in the wrong order, and they must be within
      // round-off error of each other. They can be ignored.
      if(polyCornerCoincidence(pbi0, pbi1
#ifdef DEBUG
			       , verbose
#endif // DEBUG
			       ))
	{
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "resolveTwoFoldCoincidence: polyCornerCoincidence!"
		    << std::endl;
	    oofcerr << "       : pbi0=" << *pbi0 << std::endl;
	    oofcerr << "       : pbi1=" << *pbi1 << std::endl;
	  }
#endif // DEBUG
	  delete_isec_pair(pbi0, pbi1, eledgedata, baryEquiv, facet);
	}
    } // end if both intersections share a VSB loop segment

    else {
      // Intersections are on different polygon/VSB segment pairs.
      ICoord2D corner;
      if(polyVSBCornerCoincidence(pbi0, pbi1,

#ifdef DEBUG
				  verbose,
#endif // DEBUG
				  pixplane, epts, facePlanes, onFace,
				  baryCache, corner))
	{
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "resolveTwoFoldCoincidence: polyVSBCornerCoincidence!"
		    << std::endl;
	    oofcerr << "       : pbi0=" << *pbi0 << std::endl;
	    oofcerr << "       : pbi1=" << *pbi1 << std::endl;
	  }
#endif // DEBUG
	  delete_isec_pair(pbi1, pbi0, eledgedata, baryEquiv, facet);
	}
    } // end if intersections are on different polygon/VSB segment pairs
  } // end if nEntries == nExits (ie, both == 1)

} // end resolveTwoFoldCoincidence


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// Triple coincidence.  When traversing either the polygon segments or
// the VSB segments, entries and exits must alternate in the
// intersection sequence.  This routine can assume that there are two
// entries and one exit or two exits and one entry, and that the two
// entries or exits are on different VSB segments.

//  A /\ B                B /\ A
// --o--o----          ----o--o---  VSB bdy
//  /    \  |          |  /    \
// /      \ |          | /      \ polygon bdy
//         \|          |/            
//          o C        o C         Polygon bdy is always counterclockwise.
//          |\        /|           VSB bdy can go either direction, so
//          | \      / |           these pictures apply to both R and L turns.
//

// pbi0 and pbi1 are both entries or both exits, and are on different segments.
// The one that's different from the other two, entry-wise, is pbiB.

static bool tripleCoincidence(PixelBdyIntersection *pbi0,
			      PixelBdyIntersection *pbi1,
			      PixelBdyIntersection *pbiB,
#ifdef DEBUG
			      bool verbose,
#endif // DEBUG
			      PixelBdyIntersection *&delPt0, // pt to be deleted
			      PixelBdyIntersection *&delPt1,
			      ICoord2D &corner)
{
#ifdef DEBUG
  if(verbose) {
    oofcerr << "tripleCoincidence: pbi0=" << *pbi0 << std::endl;
    oofcerr << "tripleCoincidence: pbi1=" << *pbi1 << std::endl;
    oofcerr << "tripleCoincidence: pbiB=" << *pbiB << std::endl;
  }
#endif // DEBUG
  assert(!pbi0->sameLoopSegment(pbi1));
  PixelBdyIntersection *pbiA = pbi0->sameLoopSegment(pbiB) ? pbi0 : pbi1;
  PixelBdyIntersection *pbiC = pbiA == pbi0 ? pbi1 : pbi0;
  assert(pbiA->entry == pbiC->entry && pbiA->entry != pbiB->entry);

  PixelBdyIntersection *entryPt, *exitPt, *firstPt, *secondPt; // not used here
  TurnDirection turn;
  classifyVSBcorner(pbiB, pbiC, entryPt, exitPt, firstPt, secondPt,
		    corner, turn);

#ifdef DEBUG
  OOFcerrIndent indent(2);
  if(verbose) {
    oofcerr << "tripleCoincidence: pbiA=" << *pbiA << std::endl;
    oofcerr << "tripleCoincidence: pbiC=" << *pbiC << std::endl;
    oofcerr << "tripleCoincidence: corner=" << corner
	    << " turn=" << (turn==RIGHT? "Right":"Left") << std::endl;
  }
#endif // DEBUG

  // If we're going to be deleting a pair of points, pbiB will always
  // be one of them, since we only delete an entry/exit pair.
  delPt0 = pbiB;

  // A and C are on the same loop segment.  If they're also on the
  // same polygon segment, all three points must be coincident.
  if(pbiA->segment == pbiC->segment) {
    delPt1 = pbiC;
    BarycentricCoord b = mergeBary(pbiA->baryCoord, pbiB->baryCoord);
    pbiA->baryCoord = mergeBary(b, pbiC->baryCoord);
    return true;
  }
  

  if(turn == LEFT) {
    if(pbiC->entry) {
      // Left turn && C is an entry ==>
      //    A precedes B on the VSB, B precedes C on the polygon.
      //      B /\ A
      //   ----o--o--<  
      //   |  /    \
      //   | /      \
      //   |/            
      //   o C        
      //  /|          
      // / V

      bool badAB = pbiA->loopfrac >= pbiB->loopfrac;
      bool badBC = pbiB->fraction >= pbiC->fraction;
      if(badAB && badBC) {
	delPt1 = pbiA;
	pbiC->baryCoord = mergeBary(pbiC->baryCoord, pbiA->baryCoord);
	return true;
      }
      else if(badAB) {
	delPt1 = pbiA;
	return true;
      }
      else if(badBC) {
	delPt1 = pbiC;
	return true;
      }
      
      // if(pbiA->loopfrac >= pbiB->loopfrac || pbiB->fraction >= pbiC->fraction) {
      // 	// Choose whether to delete AB or BC
      // 	if(pbiB->loopfrac - pbiA->loopfrac > pbiC->loopfrac)
      // 	  delPt1 = pbiC;
      // 	else
      // 	  delPt1 = pbiA;
      // 	// If the topological conditions aren't met, then the points
      // 	// are out of order due to round-off, and actually coincide,
      // 	// so we return *true*.
      // 	return true;
      // }
    }
    else {
      // Left turn && C is an exit ==>
      //    B precedes A on the VSB, C precedes B on the polygon
      //  A /\ B     
      // --o--o-<--  
      //  /    \  |  
      // /      \ |  
      //         \|  
      //          o C
      //          |\
      //          ^ \
      //
      bool badAB = pbiB->loopfrac >= pbiA->loopfrac;
      bool badBC = pbiC->fraction >= pbiB->fraction;
#ifdef DEBUG
      if(verbose)
	oofcerr << "tripleCoincidence: badAB=" << badAB << " badBC="
		<< badBC << std::endl;
#endif // DEBUG
      if(badAB && badBC) {
	delPt1 = pbiA;
#ifdef DEBUG
	if(verbose)
	  oofcerr << "tripleCoincidence: merging "<< pbiC->baryCoord
		  << " and " << pbiA->baryCoord << std::endl;
#endif // DEBUG
	pbiC->baryCoord = mergeBary(pbiC->baryCoord, pbiA->baryCoord);
	return true;
      }
      else if(badAB) {
	delPt1 = pbiA;
#ifdef DEBUG
	if(verbose)
	  oofcerr << "tripleCoincidence: badAB" << std::endl;
#endif // DEBUG
	return true;
      }
      else if(badBC) {
	delPt1 = pbiC;
	return true;
      }
      // if(pbiB->loopfrac >= pbiA->loopfrac || pbiC->fraction >= pbiB->fraction) {
      // 	if(pbiA->loopfrac - pbiB->loopfrac > 1-pbiC->loopfrac)
      // 	  delPt1 = pbiC;
      // 	else
      // 	  delPt1 = pbiA;
      // 	return true;
      // }
    }
  } // end if turn is left
  else {
    if(pbiC->entry) {
      // Right turn and C is an entry ==>
      //    A precedes B on the VSB, C precedes B on the polygon
      //  A /\ B     
      // --o--o->--  
      //  /    \  |  
      // /      \ |  
      //         \|  
      //          o C
      //          |\
      //          V \
      //
      bool badAB = pbiA->loopfrac >= pbiB->loopfrac;
      bool badBC = pbiC->fraction >= pbiB->fraction;
      if(badAB && badBC) {
	delPt1 = pbiA;
	pbiC->baryCoord = mergeBary(pbiC->baryCoord, pbiA->baryCoord);
	return true;
      }
      else if(badAB) {
	delPt1 = pbiA;
	return true;
      }
      else if(badBC) {
	delPt1 = pbiC;
	return true;
      }
      // if(pbiA->loopfrac >= pbiB->loopfrac || pbiC->fraction >= pbiB->fraction) {
      // 	if(pbiB->loopfrac - pbiA->loopfrac > pbiC->loopfrac)
      // 	  delPt1 = pbiC;
      // 	else
      // 	  delPt1 = pbiA;
      // 	return true;
      // }
    }
    else {
      // Right turn and C is an exit ==>
      //    B precedes A on the VSB, B precedes C on the polygon
      //      B /\ A
      //   ----o--o-->  
      //   |  /    \
      //   | /      \
      //   |/            
      //   o C        
      //  /|          
      // / ^
      bool badAB = pbiB->loopfrac >= pbiA->loopfrac;
      bool badBC = pbiB->fraction >= pbiC->fraction;
      if(badAB && badBC) {
	pbiC->baryCoord = mergeBary(pbiC->baryCoord, pbiA->baryCoord);
	delPt1 = pbiA;
	return true;
      }
      else if(badAB) {
	delPt1 = pbiA;
	return true;
      }
      else if(badBC) {
	delPt1 = pbiC;
	return true;
      }
      // if(pbiB->loopfrac >= pbiA->loopfrac || pbiB->fraction >= pbiC->fraction) {
      // 	if(pbiA->loopfrac - pbiB->loopfrac > 1-pbiC->loopfrac)
      // 	  delPt1 = pbiC;
      // 	else
      // 	  delPt1 = pbiA;
      // 	return true;
      // }
    }
  }
  return false;
}


void resolveThreeFoldCoincidence(
	 const std::pair<CoordIsec::iterator, CoordIsec::iterator> &range,
	 const std::vector<Coord3D> &epts,
	 std::vector<ElEdgeMap> &eledgedata,
	 BaryCoordMap &baryEquiv,
	 PixelPlaneFacet *facet,
	 const PixelPlane &pixplane,
	 unsigned int onFace,
	 const std::vector<const PixelPlane*> &facePlanes,
	 BaryCoordCache &baryCache
#ifdef DEBUG
	 , bool verbose
#endif
				 )
{
  std::vector<PixelBdyIntersection*> entries;
  std::vector<PixelBdyIntersection*> exits;
  entries.reserve(2);
  exits.reserve(2);
  for(auto pt=range.first; pt!=range.second; ++pt) {
    PixelBdyIntersection *pbi = (*pt).second;
    if(pbi->entry)
      entries.push_back(pbi);
    else
      exits.push_back(pbi);
  }
  if(entries.size()==2) {
    if(entries[0]->sameLoopSegment(entries[1])) {
      // Two entries on the same VSB segment

      //            /
      //           /
      //      ----8---    8 is a double intersection, where one polygon
      //      |  /        segment ends and another starts.
      //      | /
      //      |/
      //      o
      //     /|
      //    / |
#ifdef DEBUG
      if(verbose) {
	oofcerr << "resolveThreeFoldCoincidence: triple coincidence 1!"
		<< std::endl;
	oofcerr << "       : entry0=" << *entries[0] << std::endl;
	oofcerr << "       : entry1=" << *entries[1] << std::endl;
	oofcerr << "       :   exit=" << *exits[0] << std::endl;
      }
#endif // DEBUG
      // Keep the entry that's on the same polygon segment as
      // the exit.
      PixelBdyIntersection *keptEntry, *discardedEntry;
      if(entries[0]->segment == exits[0]->segment) {
	keptEntry = entries[0];
	discardedEntry = entries[1];
      }
      else {
	keptEntry = entries[1];
	discardedEntry = entries[0];
      }
      assert(keptEntry->segment == exits[0]->segment);
	    
      keptEntry->baryCoord = mergeBary(keptEntry->baryCoord,
				       discardedEntry->baryCoord);
      delete_isec(discardedEntry, eledgedata);
      // The retained intersections must pass the test used for
      // a two way coincidence on a polygon segment.
      ICoord2D corner;
      if(vsbCornerCoincidence(keptEntry, exits[0],
#ifdef DEBUG
			      verbose,
#endif // DEBUG
			      corner))
	{
	  bool interiorCorner = interior(corner, pixplane, epts, onFace,
					 facePlanes, baryCache);
	  delete_isec_pair(keptEntry, exits[0], corner, interiorCorner,
			   eledgedata, baryEquiv, facet, pixplane, onFace
#ifdef DEBUG
			   , verbose
#endif // DEBUG
			   );
	}
    } // end if two entries are on the same VSB segment
    else {
      // Two entries, but on different VSB segments
      PixelBdyIntersection *pt0, *pt1;
      ICoord2D corner;
      if(tripleCoincidence(entries[0], entries[1], exits[0],
#ifdef DEBUG
			   verbose,
#endif // DEBUG
			   pt0, pt1, corner))
	{
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "resolveThreeFoldCoincidence: triple coincidence 2!"
		    << std::endl;
	    oofcerr << "       : entry0=" << *entries[0] << std::endl;
	    oofcerr << "       : entry1=" << *entries[1] << std::endl;
	    oofcerr << "       :   exit=" << *exits[0] << std::endl;
	  }
#endif // DEBUG
	  bool interiorCorner = interior(corner, pixplane, epts,
					 onFace, facePlanes, baryCache);
	  delete_isec_pair(pt0, pt1, corner, interiorCorner, eledgedata,
			   baryEquiv, facet, pixplane, onFace
#ifdef DEBUG
			   , verbose
#endif // DEBUG
			   );
	}
    }
  }
  else if(exits.size() == 2) {
    // 2 exits, 1 entry
    if(exits[0]->sameLoopSegment(exits[1])) {
      // Two exits on the same VSB segment
#ifdef DEBUG
      if(verbose) {
	oofcerr << "resolveThreeFoldCoincidence: triple coincidence 3!"
		<< std::endl;
	oofcerr << "       : entry=" << *entries[0] << std::endl;
	oofcerr << "       : exit0=" << *exits[0] << std::endl;
	oofcerr << "       : exit1=" << *exits[1] << std::endl;
      }
#endif // DEBUG
      // Keep the exit that's on the same polygon segment as the
      // entry.
      PixelBdyIntersection *keptExit, *discardedExit;
      if(exits[0]->segment == entries[0]->segment) {
	keptExit = exits[0];
	discardedExit = exits[1];
      }
      else {
	keptExit = exits[1];
	discardedExit = exits[0];
      }
      keptExit->baryCoord = mergeBary(keptExit->baryCoord,
				      discardedExit->baryCoord);
      delete_isec(exits[1], eledgedata);
      ICoord2D corner;
      if(vsbCornerCoincidence(entries[0], keptExit,
#ifdef DEBUG
			      verbose,
#endif // DEBUG
			      corner))
	{
	  bool interiorCorner = interior(corner, pixplane, epts, onFace,
					 facePlanes, baryCache);
	  delete_isec_pair(entries[0], keptExit, corner, interiorCorner,
			   eledgedata, baryEquiv, facet, pixplane, onFace
#ifdef DEBUG
			   , verbose
#endif // DEBUG
			   );
	}
    }
    else {
      // Two exits on different VSB segments
      PixelBdyIntersection *pt0, *pt1;
      ICoord2D corner;
      if(tripleCoincidence(exits[0], exits[1], entries[0],
#ifdef DEBUG
			   verbose,
#endif // DEBUG
			   pt0, pt1, corner))
	{
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "resolveThreeFoldCoincidence: triple coincidence 4!"
		    << std::endl;
	    oofcerr << "resolveThreeFoldCoincidence: deleting pt0=" << *pt0
		    << std::endl;
	    oofcerr << "resolveThreeFoldCoincidence: deleting pt1=" << *pt1
		    << std::endl;
	  }
#endif // DEBUG
	  bool interiorCorner = interior(corner, pixplane, epts,
					 onFace, facePlanes, baryCache);
	  delete_isec_pair(pt0, pt1, corner, interiorCorner, eledgedata,
			   baryEquiv, facet, pixplane, onFace
#ifdef DEBUG
			   , verbose
#endif // DEBUG
			   );
	}
    }
  }
  else {
    assert(exits.empty() || entries.empty());
    // There are three entries or exits.  This can only happen
    // if the polygon has a high aspect ratio and the
    // intersection is at a spot where two VSB loops meet at a
    // corner.
	
    //   |    |      |
    //   |    |      |      8 is where one polygon segment
    //   |    V      |      ends and another begins on a VSB loop.
    //   |    |      |      o is where a polygon segment crosses
    //   |    |      |      a VSB loop.
    //  -o--<-+->----8--
    //   |    |      |
    //   |    |      |
    //   |    ^      |
    //   |    |      |

    // The two intersections that share a VSB segment are
    // redundant.  One should be removed.
    std::vector<PixelBdyIntersection*> &isecs
      = entries.empty() ? exits : entries;
    // Find which intersection is not on the shared VSB
    unsigned int notShared =
      isecs[0]->sameLoopSegment(isecs[1]) ? 2
      : (isecs[1]->sameLoopSegment(isecs[2]) ? 0 : 1);
    unsigned int a = (notShared + 1) % 3;
    unsigned int b = (notShared + 2) % 3;
    assert(isecs[a]->sameLoopSegment(isecs[b]));
    isecs[a]->baryCoord = mergeBary(isecs[a]->baryCoord,
				    isecs[b]->baryCoord);
    delete_isec(isecs[b], eledgedata);
	  
  } // end if there are three entries or exits

} // end resolveThreeFoldCoincidence


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// resolveMultipleCoincidence resolves (rare?) coincidences of four or
// more points.  In principle it could be used for two or three point
// coincidences as well, but it might be slower than the functions
// above.

void resolveMultipleCoincidence(
	 const std::pair<CoordIsec::iterator, CoordIsec::iterator> &pbirange,
	 const std::vector<Coord3D> &epts,
	 unsigned int nn,	// size of polygon
	 unsigned int totalIntersections, // total # of intersections on polygon
	 std::vector<ElEdgeMap> &eledgedata,
	 BaryCoordMap &baryEquiv,
	 PixelPlaneFacet *facet,
	 const PixelPlane &pixplane,
	 unsigned int onFace,
	 const std::vector<const PixelPlane*> &facePlanes,
	 BaryCoordCache &baryCache
#ifdef DEBUG
	 , bool verbose
#endif
			       )

{
#ifdef DEBUG
  if(verbose) {
    oofcerr << "resolveMultipleCoincidence: pbirange=" << std::endl;
    OOFcerrIndent indent(2);
    for(CoordIsec::iterator i=pbirange.first; i!=pbirange.second; ++i) {
      oofcerr << (*i).first << ": " << *(*i).second << std::endl;
    }
  }
#endif // DEBUG

  // Find which VSB loop segments are involved in the given
  // PixelBdyIntersections.
  std::set<PixelBdyLoopSegment> loopsegSet;
  LoopSegIsecs loopSegIsecs;	// multimap<PixelBdyLoopSegment,
				//          PixelBdyIntersection*>

  for(auto pt=pbirange.first; pt!=pbirange.second; ++pt) {
    PixelBdyIntersection *pbi = (*pt).second;
    loopsegSet.insert(pbi->getLoopSeg());
    loopSegIsecs.insert(LoopSegIsecs::value_type(pbi->getLoopSeg(), pbi));
  }

  unsigned int npts = loopSegIsecs.size();

#ifdef DEBUG
  if(verbose) {
    oofcerr << "resolveMultipleCoincidence: npts=" << npts << std::endl;
    oofcerr << "resolveMultipleCoincidence: loopsegSet=";
    std::cerr << loopsegSet;
    oofcerr << std::endl;
  }
#endif // DEBUG

  // If all of the intersections on the polygon are within this
  // coincidence region, then when we examine pairs of adjacent points
  // we need to remember that the last point is adjacent to the first.
  bool wrapAround = (npts == totalIntersections);

  // Check first for oppositedly directed loop segments (segments that
  // share a starting or ending point).  If there are two, and both
  // have two intersections, then all four intersections are
  // coincidental and should be ignored.

  std::set<PixelBdyIntersection*> deleted;
  for(auto loopseg0 : loopsegSet) {
    ICoord2D startPt = loopseg0.firstPt();
    for(auto loopseg1 : loopsegSet) {
      if(loopseg1 < loopseg0 &&
	 (loopseg1.firstPt() == loopseg0.firstPt() ||
	  loopseg1.secondPt() == loopseg0.secondPt()))
	{
	  if(loopSegIsecs.count(loopseg0) >= 2 &&
	     loopSegIsecs.count(loopseg1) >= 2)
	    {
	      delete_isec_pair_on_loop_segment(loopseg0, loopSegIsecs,
					       eledgedata, deleted, baryEquiv,
					       facet);
	      delete_isec_pair_on_loop_segment(loopseg1, loopSegIsecs,
					       eledgedata, deleted, baryEquiv,
					       facet);
	    }
	}
    }
  }

  // Find which polygon segments are involved in the given
  // PixelBdyIntersections.
  std::set<unsigned int> polysegSet;
  PolySegIsecs polySegIsecs;

  for(auto pt=pbirange.first; pt!=pbirange.second; ++pt) {
    PixelBdyIntersection *pbi = (*pt).second;
    // Don't include a PBI if it was deleted in the last step...
    if(deleted.count(pbi) == 0) {
      polysegSet.insert(pbi->segment);
      polySegIsecs.insert(PolySegIsecs::value_type(pbi->segment, pbi));
    }
  }

#ifdef DEBUG
  if(verbose) {
    oofcerr << "resolveMultipleCoincidence: polysegSet=";
    std::cerr << polysegSet;
    oofcerr << std::endl;
  }
#endif // DEBUG

  // Put the polygon segments in order.  Since polysegSet is an
  // ordered set, that's easy.
  std::vector<unsigned int> polysegVec;
  polysegVec.insert(polysegVec.end(), polysegSet.begin(), polysegSet.end());
  // If there's a gap in the ordering, the sequence should start after
  // the gap ([0,1,3] --> [3,0,1]).  If there are two gaps, it doesn't
  // matter which segment comes first. [0, 2] and [2, 0] are
  // equivalent.
  for(unsigned int i=1; i<polysegVec.size(); i++) {
    if(polysegVec[i]-polysegVec[i-1] > 1) {
      // i is the start point
      std::vector<unsigned int> newvec;
      for(unsigned int k=i; k<polysegVec.size(); k++)
	newvec[k-i] = polysegVec[i];
      unsigned int ii = newvec.size();
      for(unsigned int k=0; k<i; k++)
	newvec[ii+k] = polysegVec[k];
      polysegVec = newvec;
      break;
    }
  }

#ifdef DEBUG
  if(verbose) {
    oofcerr << "resolveMultipleCoincidence: polysegVec=";
    std::cerr << polysegVec;
    oofcerr << std::endl;
  }
#endif // DEBUG

  // Put the PBIs in order going around the polygon.
  std::vector<PixelBdyIntersection*> orderedPBIs;
  orderedPBIs.reserve(npts);
  for(unsigned int i=0; i<polysegVec.size(); i++) { // Loop over polygon edges
    auto r = polySegIsecs.equal_range(i);	    // PBIs on this edge
    ElEdgeMap m;
    for(auto i=r.first; i!=r.second; ++i) { // Put PBIs in a map to sort them
      /// WRONG:  (*i).first is the edge number, not alpha
      m.insert(ElEdgeMap::value_type((*i).first, (*i).second));
    }
    for(auto &j : m)		// Copy sorted PBIs into orderedPBIs
      orderedPBIs.push_back(j.second);
  }

#ifdef DEBUG
  if(verbose) {
    oofcerr << "resolveMultipleCoincidence: orderedPBIs=" << std::endl;
    OOFcerrIndent indent(2);
    for(auto pbi: orderedPBIs)
      oofcerr << *pbi << std::endl;
  }
#endif // DEBUG

  // Check for doubled entries or exits.  These are points at which
  // the VSB passes through a vertex of the polygon.  Both of the
  // polygon edges at the vertex will have recorded an entry or an
  // exit.
  std::set<std::vector<PixelBdyIntersection*>::iterator> deleteMe;
  for(auto k=orderedPBIs.begin(); k!=orderedPBIs.end(); ++k) {
    auto knext = k+1;
    if(knext == orderedPBIs.end()) {
      if(wrapAround)
	knext = orderedPBIs.begin();
      else
	break;
    }
    if((*k)->entry == (*knext)->entry &&
       ((*k)->segment + 1) % nn == (*knext)->segment &&
       (*k)->sameLoopSegment(*knext))
      {
	PixelBdyIntersection *pbi0 = *k;
	PixelBdyIntersection *pbi1 = *knext;
	pbi1->baryCoord = mergeBary(pbi0->baryCoord, pbi1->baryCoord);
	deleteMe.insert(k);
      }
  }
  // Delete in reverse order so as not to invalidate iterators.
  for(auto d=deleteMe.rbegin(); d!=deleteMe.rend(); ++d) {
    delete_isec(*(*d), eledgedata);
    orderedPBIs.erase(*d);
  }

  unsigned int nfixed = 0;
  do {
    nfixed = 0;
    std::set<std::vector<PixelBdyIntersection*>::iterator> deleteMe;
    // Loop over pairs of adjacent intersections.
    for(auto k=orderedPBIs.begin(); k!=orderedPBIs.end(); ++k) {
      auto knext = k+1;
      if(knext == orderedPBIs.end())
	knext = orderedPBIs.begin(); // ONLY IF WRAPAROUND?
      PixelBdyIntersection *pbi0 = *k;
      PixelBdyIntersection *pbi1 = *knext;
      oofcerr << "resolveMultipleCoincidence: pbi0=" << *pbi0 << std::endl;
      oofcerr << "resolveMultipleCoincidence: pbi1=" << *pbi1 << std::endl;
      OOFcerrIndent indent(2);
      
      // If both intersections are entries or both are exits, but they
      // weren't fixed above, it means that one of them is out of
      // place wrt its neighbor that's not part of this pair.  Don't
      // fix it now.  It'll get fixed when that pair is examined.
      if(pbi0->entry != pbi1->entry) {
	bool sameLoopSeg = pbi0->sameLoopSegment(pbi1);
	bool samePolySeg = pbi0->segment == pbi1->segment;
	assert(!(sameLoopSeg && samePolySeg));

	if(!sameLoopSeg && samePolySeg) {
	  if(verbose)
	    oofcerr << "resolveMultipleCoincidence: checking vsbCornerCoincidence"
		    << std::endl;

	  //             / polygon segment
	  //            /
	  //         --o--------------- VSB segment
	  //         |/
	  //         o
	  //        /|
	  //       / |
	  //      /  |
	  //     /   |
	  //         |

	  ICoord2D corner;
	  if(vsbCornerCoincidence(pbi0, pbi1,
#ifdef DEBUG
				  verbose,
#endif // DEBUG
				  corner))
	    {
	      bool interiorCorner = interior(corner, pixplane, epts,
					     onFace, facePlanes, baryCache);
	      delete_isec_pair(pbi0, pbi1, corner, interiorCorner, eledgedata,
			       baryEquiv, facet, pixplane, onFace
#ifdef DEBUG
			       , verbose
#endif // DEBUG
			       );
	      // Delete from orderdPBIs too.
	      deleteMe.insert(k);
	      deleteMe.insert(knext);
	      ++nfixed;
	    }
	} // end if samePolySeg and not sameLoopSeg
	
	else if(sameLoopSeg && !samePolySeg) {
	  //               
	  //            /\
	  //  ---------o--o------------ VSB segment
	  //          /	   \
	  //         /	    \
	  //        /        \ polygon segments
	  //       /  
	  //      /   
	  //
	  if(verbose)
	    oofcerr << "resolveMultipleCoincidence: checking polyCornerCoincidence"
		    << std::endl;
	  if(polyCornerCoincidence(pbi0, pbi1
#ifdef DEBUG
				   , verbose
#endif // DEBUG
				   ))
	    {
	      delete_isec_pair(pbi0, pbi1, eledgedata, baryEquiv, facet);
	      deleteMe.insert(k);
	      deleteMe.insert(knext);
	      ++nfixed;
	    }
	} // end if sameLoopSegment and not samePolySeg

	else {			// !sameLoopSeg && !samePolySeg
	  ICoord2D corner;
	  if(verbose)
	    oofcerr << "resolveMultipleCoincidence: checking polyVSBCornerCoincidence"
		    << std::endl;
	  if(polyVSBCornerCoincidence(pbi0, pbi1,
#ifdef DEBUG
				      verbose,
#endif // DEBUG
				      pixplane, epts, facePlanes, onFace,
				      baryCache, corner))
	    {
	      delete_isec_pair(pbi0, pbi1, eledgedata, baryEquiv, facet);
	      deleteMe.insert(k);
	      deleteMe.insert(knext);
	      ++nfixed;
	    }
	} // end if !sameLoopSeg and !samePolySeg
	
      }	// end if pbi0 and pbi1 aren't both entries or both exits

    }	// end loop over adjacent pairs of intersections

    for(auto d=deleteMe.rbegin(); d!=deleteMe.rend(); ++d) {
      orderedPBIs.erase(*d);
    }

  } while(nfixed > 0);

#ifdef DEBUG
  // Check that entries and exits alternate properly in both the
  // polygon and VSB sequences.  Checking VSB sequences is hard
  // because there may be multiple loops.
#endif // DEBUG
  
} // end resolveMultipleCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// resolveFourFoldCoincidence and resolveFiveFoldCoincidence aren't
// finished and won't be needed if resolveMultipleCoincidence works.

// void resolveFourFoldCoincidence(
// 	 const std::pair<CoordIsec::iterator, CoordIsec::iterator> &range,
// 	 const std::vector<Coord3D> &epts,
// 	 std::vector<ElEdgeMap> &eledgedata,
// 	 BaryCoordMap &baryEquiv,
// 	 PixelPlaneFacet *facet,
// 	 const PixelPlane &pixplane,
// 	 unsigned int onFace,
// 	 const std::vector<const PixelPlane*> &facePlanes,
// 	 BaryCoordCache &baryCache
// #ifdef DEBUG
// 	 , bool verbose
// #endif
// 				 )
// {
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "resolveFourFoldCoincidence:" << std::endl;
//   }
// #endif // DEBUG
//   // Four way coincidences are classified by how many VSB
//   // segments and how many polygon segments are involved.
//   std::set<PixelBdyLoopSegment> loopsegs;
//   std::set<unsigned int> polysegs;

//   LoopSegIsecs loopSegIsecs;
//   PolySegIsecs polySegIsecs;
//   std::vector<PixelBdyIntersection*> isecs;
//   isecs.reserve(4);
  
//   for(auto pt=range.first; pt!=range.second; ++pt) {
//     PixelBdyIntersection *pbi = (*pt).second;
//     isecs.push_back(pbi);
//     loopsegs.insert(pbi->getLoopSeg());
//     polysegs.insert(pbi->segment);
//     loopSegIsecs.insert(LoopSegIsecs::value_type(pbi->getLoopSeg(), pbi));
//     polySegIsecs.insert(PolySegIsecs::value_type(pbi->segment, pbi));
//   }

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "resolveFourFoldCoincidence: got segments.  #loopsegs="
// 	    << loopsegs.size() << " #polysegs=" << polysegs.size() << std::endl;
//   }
// #endif // DEBUG
  
//   if(loopsegs.size() == 2) {
//     std::set<PixelBdyLoopSegment>::iterator it = loopsegs.begin();
//     PixelBdyLoopSegment s0 = *it;
//     ++it;
//     PixelBdyLoopSegment s1 = *it;
//     PixelBdyLoopSegment seg0, seg1;
//     ICoord2D corner;
//     TurnDirection turn;
//     // s0 and s1 are the VSB segments.  seg0 and seg1 are the same
//     // segments, but reordered so that seg0 precedes seg1 on the VSB.
//     classifyVSBcorner(s0, s1, seg0, seg1, corner, turn);
// // #ifdef DEBUG
// //     oofcerr << "resolveFourFoldCoincidence: classified corner" << std::endl;
// // #endif // DEBUG
    
//     if(turn == UNDEFINED) {
//       // The two VSB loop segments connect head to head or tail to
//       // tail (at a point where two pixels touch corners).  There's no
//       // way that we can have 4 intersections involving two polygon
//       // segments on these two VSB segments, unless the polygon
//       // segments meet at the meeting point of the VSB segments.  All
//       // of the intersections are degenerate.  Find the pairs that
//       // share VSB segments and remove them from the facet.
//       for(auto vsbseg : loopsegs) {
// 	assert(loopSegIsecs.count(vsbseg) == 2);
// 	delete_isec_pair_on_loop_segment(vsbseg, loopSegIsecs, eledgedata,
// 					 baryEquiv, facet);
// 	// auto rng = loopSegIsecs.equal_range(vsbseg);
// 	// const PixelBdyIntersection *pbi0 = (*rng.first).second;
// 	// const PixelBdyIntersection *pbi1 = (*++rng.first).second;
// 	// delete_isec_pair(pbi0, pbi1, eledgedata, baryEquiv, facet);
//       }
//       return;
//     } // end if VSB loop segments don't connect

//     assert(turn == RIGHT || turn == LEFT);

//     if(polysegs.size() == 2) {

//       //             //  polygon edges meet up here somewhere, maybe via
//       //         2  / /  an intermediate segment
//       //        ---o-o--------
//       //        | / / 1
//       //        |/ /
//       //      3 o /   (0 & 2 could be switched if 1 & 3 are also)
//       //       /|/
//       //      / o 0
//       //     / /|
//       //      <----- actually they could meet down here instead

//       // The order of the entries and exits, when following the
//       // polygon segments and starting from an end of one segment,
//       // depends only on whether the VSB segments turn left or right.
//       // It doesn't depend on which polygon segment comes first, which
//       // is a good thing because the polygon segments don't have to be
//       // adjacent sides of the polygon, so we can't determine which
//       // comes first.

//       std::vector<PixelBdyIntersection*> orderedPBIs;
//       orderedPBIs.reserve(4);
//       for(unsigned int pseg : polysegs) {
// 	auto prange = polySegIsecs.equal_range(pseg);
// 	PixelBdyIntersection *pbi0 = (*prange.first).second;
// 	PixelBdyIntersection *pbi1 = (*++prange.first).second;
// 	if(pbi0->fraction < pbi1->fraction) {
// 	  orderedPBIs.push_back(pbi0);
// 	  orderedPBIs.push_back(pbi1);
// 	}
// 	else {
// 	  orderedPBIs.push_back(pbi1);
// 	  orderedPBIs.push_back(pbi0);
// 	}
//       }

//       // coincXY is true if intersections X and Y are misordered, and
//       // therefore are a coincidence.
//       bool coinc01 = false;
//       bool coinc12 = false;
//       bool coinc23 = false;
//       bool coinc30 = false;

//       // Check for coincidences by applying the criteria used in
//       // vsbCornerCoincidence and polyCornerCoincidence.  We don't use
//       // those routines directly because here we know more information
//       // than they assume.
//       if(turn == RIGHT) {
// 	coinc01 = !orderedPBIs[0]->entry || orderedPBIs[1]->entry;
// 	coinc12 = orderedPBIs[2]->loopfrac >= orderedPBIs[1]->loopfrac;
// 	coinc23 = !orderedPBIs[2]->entry || orderedPBIs[3]->entry;
// 	coinc30 = orderedPBIs[0]->loopfrac >= orderedPBIs[3]->loopfrac;
//       }
//       else {			// turn == LEFT
// 	coinc01 = orderedPBIs[0]->entry || !orderedPBIs[1]->entry;
// 	coinc12 = orderedPBIs[2]->loopfrac <= orderedPBIs[1]->loopfrac;
// 	coinc23 = orderedPBIs[2]->entry || !orderedPBIs[3]->entry;
// 	coinc30 = orderedPBIs[0]->loopfrac <= orderedPBIs[3]->loopfrac;
//       }

//       // If there's a misordering in only one pair of intersections,
//       // remove just that one intersection.
//       if(coinc01 && !coinc12 && !coinc23 & !coinc30) {
// 	// Points 0 & 1 coincide, but no others.
// 	delete_isec_pair(orderedPBIs[0], orderedPBIs[1], corner, false,
// 			 eledgedata, baryEquiv, facet, pixplane, onFace
// #ifdef DEBUG
// 			 , verbose
// #endif // DEBUG
// 			 );
//       }
//       else if(!coinc01 && coinc12 && !coinc23 && !coinc30) {
// 	delete_isec_pair(orderedPBIs[1], orderedPBIs[2], eledgedata, baryEquiv,
// 			 facet);
// 	return;
//       }
//       else if(!coinc01 && !coinc12 && coinc23 && !coinc30) {
// 	// Points 2 and 3 coincide, but no others.
// 	delete_isec_pair(orderedPBIs[2], orderedPBIs[3], corner, false,
// 			 eledgedata, baryEquiv, facet, pixplane, onFace
// #ifdef DEBUG
// 			 , verbose
// #endif // DEBUG
// 			 );
//       }
//       else if(!coinc01 && !coinc12 && !coinc23 && coinc30) {
// 	// Points 3 and 0 coincide, but no others.
// 	delete_isec_pair(orderedPBIs[3], orderedPBIs[0], eledgedata, baryEquiv,
// 			 facet);
//       }
//       else {
// 	// There are either 0 or more than four misorderings. If there
// 	// is more than one misordered pair, the polygon corner and
// 	// the VSB must coincide, and all four intersections are
// 	// really right at the corner.
// 	if(coinc01 || coinc12 || coinc23 || coinc30) {
// 	  BarycentricCoord bcorner = getBarycentricCoord(corner, pixplane, epts,
// 						       facePlanes, baryCache);

// 	  facet->removeEdge(orderedPBIs[3]->location3D,
// 			    orderedPBIs[0]->location3D);
// 	  facet->removeEdge(orderedPBIs[1]->location3D,
// 			    orderedPBIs[2]->location3D);
// 	  for(unsigned int i=0; i<4; i++) {
// 	    baryEquiv[orderedPBIs[i]->baryCoord] = bcorner;
// 	    delete_isec(orderedPBIs[i], eledgedata);
// 	  }
// 	}
//       }
//       return;
//     } // end if polysegs.size() == 2

//     else if(polysegs.size() == 3) {
//       // Four intersections on three polygon segments and two VSB loop
//       // segments. 

//       //           /\ poly           o marks intersections
//       //   (A)    /  \               8 marks a double intersection
//       //      ---o----8----VSB       where two polygon
//       //      | /     |              segments meet at
//       //      |/      |              a VSB segment
//       //      o      poly
//       //     /|
//       //    / |
//       //   /  |
//       //  /   |
//       //     VSB

//       //           /\ poly                    /\ poly     
//       //   (B)    /  \                (C)    /  \
//       //      ---o----o----VSB           ---o----o----VSB      
//       //      | /      \                 | /      \
//       //      |/        \                |/        \
//       //      8          \	         8          \
//       //      |\  (This is the	        /| 	               
//       //      | \  same as E)	       / |  	       
//       //      |			      /  |		       
//       //      |			         |		       
//       //     VSB		        VSB

//       //           /\                         /\
//       //  (D)     /  \                (E)    /  \
//       //      ---o----o----              ---o----o-----        
//       //      | /      \                 | /      \
//       //      |/       /                 |/        \
//       //      o       /                  o
//       //     /|      /                  /|
//       //    / |     /                   \|
//       //      |    /                     o
//       //      |   /                      |\
//       //      |  /                       | \
//       //      | /
//       //      |/
//       //      o
//       //     /|
//     }

//     else if(polysegs.size() == 4) {
//       // Four intersections on four polygon segments and two VSB loop
//       // segments.  This can happen only with a very small polygon, so
//       // that all of its points are within a fraction of a voxel
//       // length.  Since it's a quadrilateral, the polygon can't be a
//       // cross section near a tet vertex, which means that the whole
//       // tet must be small.  This is possible, but unlikely, and
//       // probably is an indication of a badly constructed Skeleton.

//     }
//   } // end if loopsegs.size() == 2

//   else if(loopsegs.size() == 3) {
//     if(polysegs.size() == 2) {
//       // Four intersections on two polygon segments and three VSB loop
//       // segments.  There is only one possible configuration:
//       //
//       //  \     |     /
//       //   \    |    /
//       // ---o---+---o---
//       //     \  |  /
//       //      \ | /
//       //       \|/
//       //        8
//       //        |

//       // Which polygon segment comes first?

// 	// This isn't finished... 
//     }

//   } // end if loopsegs.size() == 3

//   else if(loopsegs.size() == 4) {

//   } // end if loopsegs.size() == 4
  
//   // If we got here, then this particular configuration hasn't been
//   // anticipated.
  
// #ifdef DEBUG
//   if(verbose) {
//     for(auto pt=range.first; pt!=range.second; ++pt) {
//       oofcerr << "resolveFourFoldCoincidence: pbi=" << *(*pt).second
// 	      << std::endl;
//     }
//     oofcerr << "resolveFourFoldCoincidence: loopsegs=";
//     std::cerr << loopsegs;
//     oofcerr << std::endl;
//     oofcerr << "resolveFourFoldCoincidence: polysegs=";
//     std::cerr << polysegs;
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
  
//   throw ErrProgrammingError("Four point coincidence not handled yet! #loopsegs="
// 			    + to_string(loopsegs.size()) + " #polysegs="
// 			    + to_string(polysegs.size()),
// 			    __FILE__, __LINE__);
// } // end resolveFourFoldCoincidence


// //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// void resolveFiveFoldCoincidence(
// 	 const std::pair<CoordIsec::iterator, CoordIsec::iterator> &range,
// 	 const std::vector<Coord3D> &epts,
// 	 std::vector<ElEdgeMap> &eledgedata,
// 	 BaryCoordMap &baryEquiv,
// 	 PixelPlaneFacet *facet,
// 	 const PixelPlane &pixplane,
// 	 unsigned int onFace,
// 	 const std::vector<const PixelPlane*> &facePlanes,
// 	 BaryCoordCache &baryCache
// #ifdef DEBUG
// 	 , bool verbose
// #endif
// 				 )
// {
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "resolveFiveFoldCoincidence:" << std::endl;
//   }
// #endif // DEBUG
//   std::set<PixelBdyLoopSegment> loopsegs;
//   std::set<unsigned int> polysegs;

//   LoopSegIsecs loopSegIsecs;
//   PolySegIsecs polySegIsecs;
//   std::vector<PixelBdyIntersection*> isecs;
//   isecs.reserve(5);
  
//   for(auto pt=range.first; pt!=range.second; ++pt) {
//     PixelBdyIntersection *pbi = (*pt).second;
//     isecs.push_back(pbi);
//     loopsegs.insert(pbi->getLoopSeg());
//     polysegs.insert(pbi->segment);
//     loopSegIsecs.insert(LoopSegIsecs::value_type(pbi->getLoopSeg(), pbi));
//     polySegIsecs.insert(PolySegIsecs::value_type(pbi->segment, pbi));
//   }

//   // If there are just two polygon segments involved, life is simpler.
//   if(polysegs.size() == 2) {
//     if(loopsegs.size() == 3) {
//       // Two VSB loop segments have two intersections, and one has
//       // one.  Find which is which.
//       const PixelBdyLoopSegment *singleSeg = NULL;
//       const PixelBdyLoopSegment *doubleSeg0 = NULL;
//       const PixelBdyLoopSegment *doubleSeg1 = NULL;
//       for(std::set<PixelBdyLoopSegment>::iterator pbls=loopsegs.begin();
// 	  pbls!=loopsegs.end(); ++pbls)
// 	{
// 	  int count = loopSegIsecs.count(*pbls);
// 	  if(count == 1 && singleSeg == NULL) {
// 	    singleSeg = &*pbls;
// 	  }
// 	  else if(count == 2 && doubleSeg0 == NULL) {
// 	    doubleSeg0 = &*pbls;
// 	  }
// 	  else if(count == 2 && doubleSeg1 == NULL) {
// 	    doubleSeg1 = &*pbls;
// 	  }
// 	  else
// 	    throw ErrProgrammingError("Failed to sort intersections!",
// 				      __FILE__, __LINE__);
// 	}
//       PixelBdyLoopSegment dseg0, dseg1;
//       ICoord2D corner;
//       TurnDirection turn;
//       classifyVSBcorner(*doubleSeg0, *doubleSeg1, dseg0, dseg1, corner, turn);
// #ifdef DEBUG
//       if(verbose) {
// 	oofcerr << "resolveFiveFoldCoincidence: turn=" << turn << std::endl;
// 	oofcerr << "resolveFiveFoldCoincidence: singleSeg=" << *singleSeg
// 		<< std::endl;
// 	oofcerr << "resolveFiveFoldCoincidence: doubleSeg0=" << *doubleSeg0
// 		<< std::endl;
// 	oofcerr << "resolveFiveFoldCoincidence: doubleSeg1=" << *doubleSeg1
// 		<< std::endl;
//       }
// #endif // DEBUG
//       if(turn == UNDEFINED) {
// 	// The two VSB segments connect head to head or tail to tail.
// 	// The situation is the same as the four fold intersection,
// 	// except that there's an extra intersection, which should be
// 	// kept.
// 	delete_isec_pair_on_loop_segment(*doubleSeg0, loopSegIsecs, eledgedata,
// 					 baryEquiv, facet);
// 	delete_isec_pair_on_loop_segment(*doubleSeg1, loopSegIsecs, eledgedata,
// 					 baryEquiv, facet);
// 	return;
//       }
      
//     } // end if loopsegs.size == 3
    
//   } // if end polysegs.size == 2
  
// #ifdef DEBUG
//   if(verbose) {
//     for(auto pt=range.first; pt!=range.second; ++pt) {
//       oofcerr << "resolveFiveFoldCoincidence: pbi=" << *(*pt).second
// 	      << std::endl;
//     }
//     oofcerr << "resolveFiveFoldCoincidence: loopsegs=";
//     std::cerr << loopsegs;
//     oofcerr << std::endl;
//     oofcerr << "resolveFiveFoldCoincidence: polysegs=";
//     std::cerr << polysegs;
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
  
//   throw ErrProgrammingError("Five point coincidence not handled yet! #loopsegs="
// 			    + to_string(loopsegs.size()) + " #polysegs="
// 			    + to_string(polysegs.size()),
// 			    __FILE__, __LINE__);

// } // end resolveFiveFoldCoincidence
