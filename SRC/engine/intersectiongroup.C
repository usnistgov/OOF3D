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
#include <algorithm>
#include <math.h>

#include "engine/cskeletonelement.h"
#include "engine/facefacet.h"
#include "engine/homogeneitytet.h"
#include "engine/intersectiongroup.h"
#include "engine/pixelplanefacet.h"
#include "engine/planeintersection.h"

std::ostream &operator<<(std::ostream &os, const IntersectionGroup &ig) {
  EdgePosition lastT;
  unsigned int lastEdge = NONE;
  for(unsigned int i=0; i<ig.size(); i++) {
    os << "     " << *ig.isecs[i];
    if(ig.isecs[i]->faceEdge() == lastEdge) {
      os << " dt=" << ig.isecs[i]->edgePosition() - lastT;
    }
    if(i != ig.size()-1)
      os << std::endl;
    lastT = ig.isecs[i]->edgePosition();
    lastEdge = ig.isecs[i]->faceEdge();
  }
  return os;
}

void IntersectionGroup::sortByPositionAndEdge() {
  std::sort(isecs.begin(), isecs.end(), FaceEdgeIntersectionLTwrap());
}

bool IntersectionGroup::removeEquivPts(HomogeneityTet *htet,
				       unsigned int face,
				       LooseEndSet &looseEnds)
{
  unsigned int npts = size();
  if(npts < 2)
    return false;
  unsigned int nMatched = 0;
  std::vector<bool> matched(npts, false);
  for(unsigned int i=0; i<npts-1; i++) {
    if(!matched[i]) {
      FaceEdgeIntersection *feii = isecs[i];
      for(unsigned int j=i+1; j<npts; j++) {
	if(!matched[j]) {
	  FaceEdgeIntersection *feij = isecs[j];
	  if(feii->start() != feij->start()) {
	    // Points are a start and an end.
	    bool equiv = feii->corner()->isEquivalent(feij->corner());
	    if(equiv || feii->samePosition(feij)) {
	      matched[i] = true;
	      matched[j] = true;
	      nMatched += 2;
	      if(!equiv) {
		htet->mergeEquiv(feii->corner(), feij->corner());
	      }
	      break;		// go to next i
	    }
	  }
	}
      }
    }
  }
  if(nMatched > 0) {
    eraseMatched(matched, looseEnds);
    return true;
  }
  return false;
}

void IntersectionGroup::eraseMatched(const std::vector<bool> &matched,
				     LooseEndSet &looseEnds)
{
  unsigned int newSize = 0;
  for(unsigned int i=0; i<isecs.size(); i++) {
    if(!matched[i]) {
      isecs[newSize] = isecs[i];
      newSize++;
    }
    else {
	looseEnds.erase(isecs[i]);
    }
  }
  isecs.resize(newSize);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// Methods used by HomogeneityTet::resolveFaceFacetCoincidences

// fixTents looks for situations in which two intersections in an
// IntersectionGrup are parts of segments that join together within
// the tet face. Because the interior point (ptX) is at the junction
// of facet edges that arise from the intersection of pixel planes and
// the tet face, we can find the directions of those edges and use
// that to compute the order of the intersection points on the face
// edge.  If that order is incorrect, then points are close enough
// that roundoff error has affected the order, and the three points X,
// A, and B must all really be equivalent.

/*
//        X
//       / \
//      /   \
//     /     \
//    /       \
// --A---------B--->-- directed tet face edge
*/
bool IntersectionGroup::fixTents(HomogeneityTet *htet,
				 unsigned int face,
				 LooseEndSet &looseEnds)
{
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::fixTents: this=" << std::endl;
    std::cerr << *this << std::endl;
  }
#endif // DEBUG
  unsigned int npts = size();
  if(npts < 2)
    return false;
  std::vector<bool> matched(npts, false);
  unsigned int nMatched = 0;
  for(unsigned int i=0; i<npts-1; i++) {
    if(!matched[i]) {
      FaceEdgeIntersection *feii = isecs[i];
      PlaneIntersection *ptX = feii->remoteCorner();
#ifdef DEBUG
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::fixTents: feii=" << *feii << std::endl;
	oofcerr << "IntersectionGroup::fixTents: ptX=" << *ptX << std::endl;
      }
      OOFcerrIndent indent(2);
#endif // DEBUG
      for(unsigned int j=i+1; j<npts; j++) {
	if(!matched[j]) {
	  FaceEdgeIntersection *feij = isecs[j];
#ifdef DEBUG
	  if(htet->verboseFace()) {
	    oofcerr << "IntersectionGroup::fixTents: feij=" << *feij
		    << std::endl;
	  }
#endif // DEBUG
	  if(feii->start() != feij->start() &&
	     feii->faceEdge() == feij->faceEdge() &&
	     feij->remoteCorner()->isEquivalent(ptX))
	    {
#ifdef DEBUG
	      if(htet->verboseFace()) {
		oofcerr << "IntersectionGroup::fixTents: calling tentCheck"
			<< std::endl;
	      }
#endif // DEBUG
	      if(!tentCheck(htet, face, ptX, feii, feij)) {
#ifdef DEBUG
		if(htet->verboseFace()) {
		  oofcerr << "IntersectionGroup::fixTents: tentCheck returned F"
			  << std::endl;
	      }
#endif // DEBUG
		matched[j] = true;
		matched[i] = true;
		htet->mergeEquiv(feii->corner(), feij->corner());
		nMatched += 2;
		break;
	      }
#ifdef DEBUG
	      else
		if(htet->verboseFace()) {
		  oofcerr << "IntersectionGroup::fixTents: tentCheck returned T"
			  << std::endl;
	      }
#endif // DEBUG
	    }
	} // end if j wasn't already matched
      }	  // end loop over intersections j
    } // end if i wasn't already matched
  }   // end loop over intersections i
  if(nMatched > 0) {
    eraseMatched(matched, looseEnds);
    return true;
  }
  return false;
}

bool IntersectionGroup::tentCheck(HomogeneityTet *htet, unsigned int face,
				  PlaneIntersection *ptX,
				  FaceEdgeIntersection *fei0,
				  FaceEdgeIntersection *fei1)
  const
{
// #ifdef DEBUG
//   if(htet->verboseFace())
//     oofcerr << "IntersectionGroup::tentCheck" << std::endl;
//   OOFcerrIndent indent(2);
// #endif // DEBUG
  
  // The two intersection points comprise a start and an end, are on
  // the same edge of the face, and the FaceFacetEdges that they're on
  // meet at their far ends.  This means that we know the order in
  // which the intersection points should appear on the tet face
  // perimeter.  Return true if the order is correct.

  // TODO: Do this calculation for points on different tet
  // face edges too.

  // Let feiA be the FaceEdgeIntersection for the facet segment that
  // starts on the tet edge and feiB be the one that ends on the tet
  // edge.
  FaceEdgeIntersection *feiA = fei0->start() ? fei0 : fei1;
  FaceEdgeIntersection *feiB = fei0->start() ? fei1 : fei0;
	      
  Coord3D faceNormal = htet->faceAreaVector(face); // not unit vec
  const PlaneIntersection *ptA = feiA->corner();
  const PlaneIntersection *ptB = feiB->corner();
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::tentCheck: ptA=" << *ptA
	    << " start=" << feiA->start() << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: ptB=" << *ptB
	    << " start=" << feiB->start() << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: ptX=" << *ptX << std::endl;
  }
#endif // DEBUG
  const FacePlane *thisFacePtr = htet->getTetFacePlane(face);
  // pt0 and pt1 are on the same tet edge, so they share two faces.
  // The calculation is being done on thisFacePtr.  otherFacePtr is
  // the other face.
  const FacePlane *otherFacePtr = ptA->sharedFace(ptB, thisFacePtr);
  assert(otherFacePtr != nullptr);
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::tentCheck: otherFacePtr=" << *otherFacePtr
	    << std::endl;
#endif // DEBUG
  unsigned int otherFace = htet->getTetFaceIndex(otherFacePtr);
  // tetEdge is the index of the common edge at tet scope.
  unsigned int tetEdge =
    CSkeletonElement::faceFaceEdge[face][otherFace];
  // faceEdge is the index of the common edge at face scope.
  unsigned int faceEdge =
    CSkeletonElement::tetEdge2FaceEdge[face][tetEdge];
  // At face scope, edge n goes from node n to node (n+1)%3.
  unsigned int n0 = vtkTetra::GetFaceArray(face)[faceEdge];
  unsigned int n1 = vtkTetra::GetFaceArray(face)[(faceEdge+1)
						 % NUM_TET_FACE_EDGES];
  // TODO: Add a table to CSkeletonElement that maps pairs of face
  // indices to pairs of node indices, and skip the previous 4 lines.

  // The common edge goes from coord e0 to e1.
  Coord3D e0 = htet->nodePosition(n0);
  Coord3D e1 = htet->nodePosition(n1);
  Coord3D E = e1 - e0;
  // Eperp is a unit vector perpendicular to the edge of
  // the face that lies in the plane of the face, pointing
  // inwards (ie, to the left when traversing the edge).
  // TODO: Precompute and cache Eperp in the HomogeneityTet.
  Coord3D Eperp = cross(faceNormal, E);
  Eperp /= sqrt(norm2(Eperp));

#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::tentCheck: face=" << face
	    << " otherFace=" << otherFace << " tetEdge=" << tetEdge
	    << " faceEdge=" << faceEdge
	    << " n0=" << n0 << " n1=" << n1
	    << " e0=" << e0 << " e1=" << e1
	    << std::endl;
#endif // DEBUG
  
  // Find the vectors in the directions of the edges from ptA and ptB
  // to ptX.  *Don't* just use the positions of those points, since
  // that'll be susceptible to round off error in exactly the
  // situations in which this calculation is important.  Use the
  // topological information instead.  If sharedPixelPlane returns
  // nullptr, it means that the points are connected along a tet face
  // and not a pixel plane, and this check is irrelevant.

  const PixelPlane *ppA = ptA->sharedPixelPlane(ptX, face);
  if(ppA == nullptr) {
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "IntersectionGroup::tentCheck: ppA = nullptr!" << std::endl;
#endif // DEBUG
    return true;
  }
  const PixelPlane *ppB = ptB->sharedPixelPlane(ptX, face);
  if(ppB == nullptr) {
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "IntersectionGroup::tentCheck: ppB = nullptr!" << std::endl;
#endif // DEBUG
    return true;
  }
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::tentCheck: ppA=" << *ppA << " ppB=" << *ppB
	    << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: ppB->normal=" << ppA->normal()
	    << " ppB->normal=" << ppB->normal() << " faceNormal=" << faceNormal
	    << std::endl;
  }
#endif // DEBUG

  // edgeVecA goes in the direction of ptA to ptX, and edgeVecB goes
  // in the direction of ptX to ptB.  They are *not* the vectors from
  // ptA to ptX or ptX to ptB.  Their lengths depend on the dihedral
  // angle between the pixel planes and the face, and aren't important
  // here.
  Coord3D edgeVecA = cross(faceNormal, ppA->normal());
  Coord3D edgeVecB = cross(faceNormal, ppB->normal());

  // dotA and dotB are proportional to the components of edgeVecA and
  // edgeVecB that are perpendicular to the tet edge.  We only care
  // about their signs.
  double dotA = dot(edgeVecA, Eperp);
  double dotB = dot(edgeVecB, Eperp);
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::tentCheck: edgeVecA=" << edgeVecA
	    << " edgeVecB=" << edgeVecB << " Eperp=" << Eperp
	    << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: dotA=" << dotB << " dotB="
	    << dotB << std::endl;
  }
#endif // DEBUG
  // Check that edgeVecA points towards the interior and edgeVecB
  // points towards the exterior.
  if(dotA < 0 || dotB > 0) {
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "IntersectionGroup::tentCheck: dot check failed"
	      << std::endl;
#endif // DEBUG
    return false;
  }

  // The perpendicular components of the edgeVecs have the correct
  // signs.  Check the transverse components.

  // Normalize the edgeVecs.
  edgeVecA /= sqrt(norm2(edgeVecA));
  edgeVecB /= sqrt(norm2(edgeVecB));

  // The normalized vectors edgeVecB and -edgeVecA point from ptX
  // torwards the intersection points on the tet edge.  ptB is past
  // ptA if dot(edgeVecB, E) > dot(-edgeVecA, E), so the order just
  // depends on the sign of the dot product of the sum of the
  // edgeVecs.

  double dotSum = dot(edgeVecA + edgeVecB, E);
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::tentCheck: normalized edgeVecA=" << edgeVecA
	    << " edgeVecA dot E= " << dot(edgeVecA, E) << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: normalized edgeVecB=" << edgeVecB
	    << " edgeVecB dot E= " << dot(edgeVecB, E) << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: dotSum=" << dotSum << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: tA=" << feiA->edgePosition()
	    << " tB=" << feiB->edgePosition()
	    << " tA-tB=" << (feiA->edgePosition() - feiB->edgePosition())
	    << std::endl;
  }
#endif // DEBUG
  if((dotSum > 0 && feiA->edgePosition() > feiB->edgePosition()) ||
     (dotSum < 0 && feiA->edgePosition() < feiB->edgePosition()))
    {
#ifdef DEBUG
      if(htet->verboseFace())
	oofcerr << "IntersectionGroup::tentCheck: dotSum check failed"
		<< std::endl;
#endif // DEBUG
      return false;
    }


  // Check that the area of the triangle (ptA,ptX,ptB) has the
  // expected sign. TODO: Perhaps this is the only check required.  Do
  // it first?
  Coord3D fcenter = htet->faceCenter(face);
  // Calculate the area in the same way as it's done in
  // FaceFacet::fixNonPositiveArea (which uses FaceFacet::getArea) so
  // the round-off error should be the same.  It's hard to use exactly
  // the same code because that calculation uses very different data
  // structures.
  Coord3D avec = ((ptA->location3D()-fcenter) % (ptX->location3D()-fcenter) +
		  (ptX->location3D()-fcenter) % (ptB->location3D()-fcenter) +
		  (ptB->location3D()-fcenter) % (ptA->location3D()-fcenter));
  double area = dot(htet->faceAreaVector(face), avec);
  if((area > 0 && feiB->edgePosition() > feiA->edgePosition()) ||
     (area < 0 && feiA->edgePosition() > feiB->edgePosition()))
    {
#ifdef DEBUG
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::tentCheck: area test failed: area="
		<< area << std::endl;
      }
#endif // DEBUG
      return false;
    }
  // If dotSum == 0, the two segments from ptX are antiparallel, or both
  // are parallel to the tet edge.  If they're antiparallel, their
  // other ends must be coincident, and we should return false so that
  // they'll be merged.  If the segments are parallel to the tet edge,
  // but one end is on the edge (ptA or ptB) and the other is
  // interior (ptX), everything is inconsistent and must be due to
  // round-off error.  Again, return false.
  if(dotSum == 0)
    return false;

  return true;			//  all is ok
} // end IntersectionGroup::tentCheck


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


bool IntersectionGroup::fixOccupiedEdges(
			 HomogeneityTet *htet,
			 unsigned int face,
			 LooseEndSet &looseEnds,
			 const std::vector<FaceFacetEdgeSet> &edgeEdges
					 )
{
  // Remove pairs of points on an edge that is already occupied by
  // another segment.  This can happen in situations like this:
  /*
    ....c          B
    .....\        /...
    ......\      /.....    Points marked by capital letters are
    .......\    /......    starts and lower case are stops.
    ........\  /........
    A--------Cb----------a 
  */
  // C and b should be identical and should be on the edge A-a, but
  // roundoff error may make C come before b.  In that case, C and b
  // are loose ends, but the order of starts and ends along the edge
  // is start-start-end-end, and the points can't be paired. Note that
  // A and a need not be loose ends.  Also, b must not be joined to C
  // counterclockwise, the way ends and starts are normally joined.
  // (If roundoff has put Cb in the other order (bC), then
  // fixCrossings will have already removed them.)

// #ifdef DEBUG
//   if(htet->verboseFace())
//     oofcerr << "IntersectionGroup::fixOccupiedEdges" << std::endl;
// #endif // DEBUG

  if(size() < 2 || edgeEdges.empty()) {
// #ifdef DEBUG
//     if(htet->verboseFace())
//       oofcerr << "IntersectionGroup::fixOccupiedEdges: nothing to do"
// 	      << std::endl;
// #endif // DEBUG
    return false;
  }

  // Rather than do complicated bookkeeping during the loop, keep
  // track of the intersections to be deleted and delete them all at
  // the end.
  std::vector<bool> deleteMe(size(), false);
  // Look for start-end pairs in isecs that are on the same face edge.
  // i is the *second* intersection in the pair.
  unsigned int nDeleted = 0;
  unsigned int i = 1;
  while(i < size()) {
// #ifdef DEBUG
//     if(htet->verboseFace())
//       oofcerr << "IntersectionGroup::fixOccupiedEdges: i=" << i << std::endl;
// #endif // DEBUG
    FaceEdgeIntersection *x = isecs[i];
    FaceEdgeIntersection *xprev = isecs[i-1];
    if(xprev->start() && !x->start() && xprev->faceEdge() == x->faceEdge()) {
      // Found start-end pair on the same face edge.
// #ifdef DEBUG
//       if(htet->verboseFace()) {
// 	oofcerr << "IntersectionGroup::fixOccupiedEdges: found start-end pair:"
// 		<< std::endl;
// 	oofcerr << "IntersectionGroup::fixOccupiedEdges: start=" << *xprev
// 		<< std::endl;
// 	oofcerr << "IntersectionGroup::fixOccupiedEdges:   end=" << *x
// 		<< std::endl;
//       }
// #endif // DEBUG
      EdgePosition tC = xprev->edgePosition();
      EdgePosition tb = x->edgePosition();
      // Look for an existing facet edge on the same face edge.
      unsigned int e = x->faceEdge();
      bool foundEdge = false;
      for(FaceFacetEdge *edge : edgeEdges[e]) {
	// If x and xprev are the endpoints of the edge, it doesn't count.
	if(!edge->startPt()->isEquivalent(xprev->corner()) &&
	   !edge->endPt()->isEquivalent(x->corner()))
	  {
// #ifdef DEBUG
// 	    if(htet->verboseFace()) {
// 	      oofcerr << "IntersectionGroup::fixOccupiedEdges: checking edge "
// 		      << *edge << std::endl;
// 	    }
// #endif // DEBUG
	    // TODO: Should tA and ta be cached?
	    EdgePosition tA =
	      htet->faceEdgeCoord(edge->startPt()->baryCoord(htet), face, e);
	    EdgePosition ta =
	      htet->faceEdgeCoord(edge->endPt()->baryCoord(htet), face, e);
	    if(tA < tC && tC < ta && tA < tb && tb < ta) {
	      // Cb lies inside Aa on the edge of the tet face.
	      // Remove x and xprev (ie C and b) from the loose end
	      // set, merge their equivalence classes, and set up the
	      // next iteration.
// #ifdef DEBUG
// 	      if(htet->verboseFace())
// 		oofcerr << "IntersectionGroup::fixOccupiedEdges: "
// 			<< "merging classes" << std::endl;
// #endif // DEBUG
	      x->corner()->equivalence()->merge(xprev->corner()->equivalence());
	      looseEnds.erase(x);
	      looseEnds.erase(xprev);
	      deleteMe[i] = true;
	      deleteMe[i-1] = true;
	      i += 2;
	      foundEdge = true;
	      nDeleted += 2;
	      break;		// break out of loop over edgeEdges
	    }
	  }
      }	// end loop over edgeEdges
      if(!foundEdge)
	i++;
    } // end if xprev and x are a start-end pair on the same edge
    else
      i++;
  } // end while i < size()

  // Delete entries from isecs
  if(nDeleted > 0) {
// #ifdef DEBUG
//     if(htet->verboseFace()) {
//       oofcerr << "IntersectionGroup::fixOccupiedEdges: deleting "
// 	      << nDeleted << " intersections" << std::endl;
//     }
// #endif // DEBUG
    unsigned int n = 0;
    for(unsigned int i=0; i<isecs.size(); i++) {
      if(!deleteMe[i])
	isecs[n++] = isecs[i];
    }
    isecs.resize(isecs.size() - nDeleted);
// #ifdef DEBUG
//     if(htet->verboseFace()) {
//       oofcerr << "IntersectionGroup::fixOccupiedEdges: done deleting"
// 	      << std::endl;
//     }
// #endif // DEBUG
    return true;
  }
  return false;
} // end IntersectionGroup::fixOccupiedEdges


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


bool IntersectionGroup::fixCrossings(HomogeneityTet *htet, unsigned int face,
				     LooseEndSet &looseEnds)
{
  // Merge points at the endpoints of crossing segments.

  // isecs is a list of FaceEdgeIntersections, each of which contains
  // pointers to an intersection point (PlaneIntersection) on the edge
  // of a face and the segment (FaceFacetEdge) that leads to it.  When
  // we talk about points or segments in the intersection group, those
  // are what we're talking about.

  // If one segment in the intersection group crosses another, the two
  // must actually meet, and their intersection points should be
  // merged.  There can be more than one crossing, but there can't be
  // more than one independent crossing -- if multiple segments cross,
  // they must all merge into the same point.

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::fixCrossings: this=" << std::endl;
    std::cerr << *this << std::endl;
  }
  OOFcerrIndent indent(2);
#endif // DEBUG

  const FacePlane *facePlane = htet->getTetFacePlane(face);

  // This process rewrites the isecs vector.  The new vector is built
  // in newIsecs, which replaces isecs at the end.
  std::vector<FaceEdgeIntersection*> newIsecs;

  // Since we want to find the segments that cross, and one segment
  // can be in more than one FaceEdgeIntersection, first make a list
  // of unique segments.  Since there aren't going to be a lot of
  // segments in an IntersectionGroup, we use simple data structures
  // ane linear search.
  std::vector<FaceFacetEdge*> segments;
  segments.reserve(isecs.size());
  for(FaceEdgeIntersection *isec : isecs) {
    bool found = false;
    for(unsigned int i=0; i<segments.size() && !found; i++)
      if(isec->edge() == segments[i])
	found = true;
    if(!found)
      segments.push_back(isec->edge());
  }

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::fixCrossings: segments=" << std::endl;
    OOFcerrIndent indent(2);
    for(FaceFacetEdge *seg : segments)
      oofcerr << "IntersectionGroup::fixCrossings: " << *seg << std::endl;
  }
#endif // DEBUG

  if(segments.size() < 2)
    return false;

  std::vector<FaceEdgeIntersection*> mergers;
  mergers.reserve(isecs.size());

  // Loop over pairs of segments looking for crossings
  for(unsigned int iseg0=0; iseg0<segments.size()-1; iseg0++) {
    FaceFacetEdge *seg0 = segments[iseg0];
    for(unsigned int iseg1=iseg0+1; iseg1<segments.size(); iseg1++) {
      FaceFacetEdge *seg1 = segments[iseg1];

      // See if the segments actually meet.  If they do, then they
      // don't cross.
      if(seg0->startPt()->isEquivalent(seg1->startPt()) ||
	 seg0->startPt()->isEquivalent(seg1->endPt()) ||
	 seg0->endPt()->isEquivalent(seg1->startPt()) ||
	 seg0->endPt()->isEquivalent(seg1->endPt()))
	{
	  continue;		// go to next pair of segments
	}

#ifdef DEBUG
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::fixCrossings: examining segments"
		<< std::endl;
	oofcerr << "IntersectionGroup::fixCrossings:    seg0=" << *seg0
		<< std::endl;
	oofcerr << "IntersectionGroup::fixCrossings:    seg1=" << *seg1
		<< std::endl;
      }
#endif // DEBUG
      // Find two end points of seg0 and seg1 that are in the
      // intersection group and on different segments.  If there are
      // more than two, pick the ones that are closest to one another.
      std::vector<FaceEdgeIntersection*> fei0vec; // candidate ends of seg0
      std::vector<FaceEdgeIntersection*> fei1vec; // candidate ends of seg1
      fei0vec.reserve(2);
      fei1vec.reserve(2);
      for(FaceEdgeIntersection *isec : isecs) {
	if(isec->edge() == seg0)
	  fei0vec.push_back(isec);
	if(isec->edge() == seg1)
	  fei1vec.push_back(isec);
      }
      FaceEdgeIntersection *fei0 = nullptr; // chosen end of seg0
      FaceEdgeIntersection *fei1 = nullptr; // chosen end of seg1
      if(fei0vec.size() == 1)
	fei0 = fei0vec[0];
      if(fei1vec.size() == 1)
	fei1 = fei1vec[0];
      if(fei0 && !fei1) {
	// Pick closest end of seg1
	assert(fei1vec.size() == 2);
	Coord3D p0 = fei0->corner()->location3D();
	if(norm2(p0 - fei1vec[0]->corner()->location3D()) <
	   norm2(p0 - fei1vec[1]->corner()->location3D()))
	    fei1 = fei1vec[0];
	else
	  fei1 = fei1vec[1];
      }
      else if(fei1 && !fei0) {
	// Pick closest end of seg0
	assert(fei0vec.size() == 2);
	Coord3D p1 = fei1->corner()->location3D();
	if(norm2(p1 - fei0vec[0]->corner()->location3D()) <
	   norm2(p1 - fei0vec[1]->corner()->location3D()))
	  fei0 = fei0vec[0];
	else
	  fei0 = fei0vec[1];
      }
      else if(!fei0 && !fei1) {
	// Pick closest pair from both segments
	assert(fei0vec.size() == 2);
	assert(fei1vec.size() == 2);
	double bestDist = std::numeric_limits<double>::max();
	for(unsigned int e0=0; e0<2; e0++) {
	  for(unsigned int e1=0; e1<2; e1++) {
	    double dist= norm2(fei0vec[e0]->corner()->location3D() -
			       fei1vec[e1]->corner()->location3D());
	    if(dist < bestDist) {
	      bestDist = dist;
	      fei0 = fei0vec[e0];
	      fei1 = fei1vec[e1];
	    }
	  }
	}
      }
      assert(fei0 != nullptr && fei1 != nullptr);

#ifdef DEBUG
      if(fei0 == nullptr || fei1 == nullptr) {
	throw ErrProgrammingError("Couldn't find fei0 or fei1!",
				  __FILE__, __LINE__);
      }
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::fixCrossings: fei0=" << *fei0
		<< std::endl;
	oofcerr << "IntersectionGroup::fixCrossings: fei1=" << *fei1
		<< std::endl;
      }
#endif // DEBUG
      PlaneIntersection *pt0 = fei0->corner();
      PlaneIntersection *pt1 = fei1->corner();

      // If the far ends of the two chosen segments are closer than
      // the near ends, then they must be in a different
      // IntersectionGroup, and that group is the one that needs to be
      // checked.  If the segments cross, we need to merge the closest
      // pair of ends.
      double d2 = norm2(pt0->location3D() - pt1->location3D());
      double dfar2 = norm2(fei0->remoteCorner()->location3D() -
			   fei1->remoteCorner()->location3D());
      if(d2 <= dfar2) {
	// The near ends of fei0 and fei1 are closer than the far ends.
	const FacePlane *fp = pt0->sharedFace(pt1, facePlane);
#ifdef DEBUG
	if(htet->verboseFace()) {
	  if(fp != nullptr)
	    oofcerr << "IntersectionGroup::fixCrossings: fp=" << *fp
		    << std::endl;
	  else
	    oofcerr << "IntersectionGroup::fixCrossings: fp=nullptr"
		    << std::endl;
	}
#endif // DEBUG
	if((fp && fei0->crossesSameEdge(fei1, face, fp, htet
#ifdef DEBUG
					, htet->verboseFace()
#endif // DEBUG
					))
	   ||
	   (!fp && fei0->crossesDiffEdge(fei1
#ifdef DEBUG
					 , htet->verboseFace()
#endif // DEBUG
					 )))
	  {
#ifdef DEBUG
	    if(htet->verboseFace())
	      oofcerr << "IntersectionGroup::fixCrossings: crossing detected!"
		      << std::endl;
#endif // DEBUG
	    mergers.push_back(fei0);
	    mergers.push_back(fei1);
	  }
#ifdef DEBUG
	else {
	  if(htet->verboseFace())
	    oofcerr << "IntersectionGroup::fixCrossings: no crossing"
		    << std::endl;
	}
      }	// end if near ends are closer to each other than the far ends are.=
#endif // DEBUG
    }  // end loop over segments seg1
  } // end loop over segments seg0

  if(!mergers.empty()) {
    // Merge the FaceEdgeIntersections that lead to crossing edges.
    // All of the points merge into the same new intersection.  There
    // can't be more than one, because the crossing edges arise when a
    // corner of the VSB lies near a tet edge, and the VSB corners are
    // at least a voxel length apart (ie, larger than an
    // IntersectionGroup).

#ifdef DEBUG
    if(htet->verboseFace()) {
      oofcerr << "IntersectionGroup::fixCrossings: merging " << mergers.size()
	      << " intersections" << std::endl;
      OOFcerrIndent indent(2);
      for(FaceEdgeIntersection *mergePt : mergers)
	oofcerr << "IntersectionGroup::fixCrossings: " << *mergePt
		<< std::endl;
    }
#endif // DEBUG

    // Make a new GenericIntersection merging the planes of all of the
    // original intersections.
    GenericIntersection *newPt = new GenericIntersection(htet);
    htet->extraPoints.insert(newPt);
    // To update the loose end set, we need to know how many starts
    // and ends have been merged.
    unsigned int nStarts = 0;
    unsigned nEnds = 0;

    for(FaceEdgeIntersection *mergePt : mergers) {
      mergePt->corner()->copyPlanesToIntersection(newPt);
      if(mergePt->start())
	nStarts++;
      else
	nEnds++;
    }
    newPt->computeLocation();
    htet->checkEquiv(newPt);	// merges equivalence classes
    // Find out where newPt is on the face
    EdgePosition newT;
    unsigned int newEdge = NONE;
    htet->findFaceEdge(newPt, face, newEdge, newT); // computes newEdge, newT

    // Replace entries in the LooseEndsSet with new ones using newPt,
    // or discard them if they're part of a start/end pair.
    // keepStarts is the number of start points to keep.  Since all
    // the points will end up at the same place, it doesn't matter
    // which ones we keep as long as we end up with the right number
    // of starts and ends.
    unsigned int keepStarts = nStarts > nEnds ? nStarts-nEnds : 0;
    unsigned int keepEnds   = nEnds > nStarts ? nEnds-nStarts : 0;
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "IntersectionGroup::fixCrossings: keepStarts=" << keepStarts
	      << " keepEnds=" << keepEnds << std::endl;
#endif // DEBUG
    if(keepStarts > 0 || keepEnds > 0) {
      unsigned int startCount = 0; // number of start points already kept
      unsigned int endCount = 0;
      for(FaceEdgeIntersection *oldfei : mergers) {
	bool isStart = oldfei->start();
	if((isStart && startCount < keepStarts) ||
	   (!isStart && endCount < keepEnds))
	  {
	    FaceEdgeIntersection *newfei =
	      htet->newFaceEdgeIntersection(newPt, oldfei->edge(), isStart);
	    newfei->setFaceEdge(newEdge, newT);
	    newIsecs.push_back(newfei);
	    looseEnds.insert(newfei);
	    if(isStart)
	      startCount++;
	    else
	      endCount++;
	  }
	looseEnds.erase(oldfei);
      }	// end loop over FaceEdgeIntersections to be merged
    } // end if keepStarts > 0 || keepEnds > 0
    else {
      // Don't keep any of the endpoints of crossing segments.
      for(FaceEdgeIntersection *oldfei : mergers)
	looseEnds.erase(oldfei);
    }

    // If there are FaceEdgeIntersections that weren't merged, put
    // them in newIsecs too.
    if(mergers.size() < isecs.size()) {
      for(FaceEdgeIntersection *isec : isecs) {
	if(std::find(mergers.begin(), mergers.end(), isec) == mergers.end())
	  newIsecs.push_back(isec);
      }
    }
    isecs = std::move(newIsecs);
    return true;
  }   // end if there are FaceEdgeIntersections to be merged
  return false;
}  // end IntersectionGroup::fixCrossings
