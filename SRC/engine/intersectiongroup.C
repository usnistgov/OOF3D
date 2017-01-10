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

void IntersectionGroup::removeEquivPts(HomogeneityTet *htet,
				       unsigned int face,
				       LooseEndSet &looseEnds)
{
  unsigned int npts = size();
  if(npts <= 1)
    return;
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
  if(nMatched > 0)
    eraseMatched(matched, looseEnds);
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

// Methods used by HomogeneityTet::resolveCoincidences

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
void IntersectionGroup::fixTents(HomogeneityTet *htet,
				 unsigned int face,
				 LooseEndSet &looseEnds)
{
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "IntersectionGroup::fixTents: this=" << std::endl;
//     std::cerr << *this << std::endl;
//   }
// #endif // DEBUG
  unsigned int npts = size();
  if(npts <= 1)
    return;
  std::vector<bool> matched(npts, false);
  unsigned int nMatched = 0;
  for(unsigned int i=0; i<npts-1; i++) {
    if(!matched[i]) {
      FaceEdgeIntersection *feii = isecs[i];
      PlaneIntersection *ptX = feii->remoteCorner();
// #ifdef DEBUG
//       if(htet->verboseFace()) {
// 	oofcerr << "IntersectionGroup::fixTents: feii=" << *feii << std::endl;
// 	oofcerr << "IntersectionGroup::fixTents: ptX=" << *ptX << std::endl;
//       }
//       OOFcerrIndent indent(2);
// #endif // DEBUG
      for(unsigned int j=i+1; j<npts; j++) {
	if(!matched[j]) {
	  FaceEdgeIntersection *feij = isecs[j];
// #ifdef DEBUG
// 	  if(htet->verboseFace()) {
// 	    oofcerr << "IntersectionGroup::fixTents: feij=" << *feij
// 		    << std::endl;
// 	  }
// #endif // DEBUG
	  if(feii->start() != feij->start() &&
	     feii->faceEdge() == feij->faceEdge() &&
	     feii->remoteCorner()->isEquivalent(ptX))
	    {
// #ifdef DEBUG
// 	      if(htet->verboseFace()) {
// 		oofcerr << "IntersectionGroup::fixTents: calling tentCheck"
// 			<< std::endl;
// 	      }
// #endif // DEBUG
	      if(!tentCheck(htet, face, ptX, feii, feij)) {
// #ifdef DEBUG
// 		if(htet->verboseFace()) {
// 		  oofcerr << "IntersectionGroup::fixTents: tentCheck returned F"
// 			  << std::endl;
// 	      }
// #endif // DEBUG
		matched[j] = true;
		matched[i] = true;
		htet->mergeEquiv(feii->corner(), feij->corner());
		nMatched += 2;
		break;
	      }
// #ifdef DEBUG
// 	      else
// 		if(htet->verboseFace()) {
// 		  oofcerr << "IntersectionGroup::fixTents: tentCheck returned T"
// 			  << std::endl;
// 	      }
// #endif // DEBUG
	    }
	} // end if j wasn't already matched
      }	  // end loop over intersections j
    } // end if i wasn't already matched
  }   // end loop over intersections i
  if(nMatched > 0)
    eraseMatched(matched, looseEnds);
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
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "IntersectionGroup::tentCheck: ptA=" << *ptA
// 	    << " start=" << feiA->start() << std::endl;
//     oofcerr << "IntersectionGroup::tentCheck: ptB=" << *ptB
// 	    << " start=" << feiB->start() << std::endl;
//     oofcerr << "IntersectionGroup::tentCheck: ptX=" << *ptX << std::endl;
//   }
// #endif // DEBUG
  const FacePlane *thisFacePtr = htet->getTetFacePlane(face);
  // pt0 and pt1 are on the same tet edge, so they share two faces.
  // The calculation is being done on thisFacePtr.  otherFacePtr is
  // the other face.
  const FacePlane *otherFacePtr = ptA->sharedFace(ptB, thisFacePtr);
  assert(otherFacePtr != nullptr);
// #ifdef DEBUG
//   if(htet->verboseFace())
//     oofcerr << "IntersectionGroup::tentCheck: otherFacePtr=" << *otherFacePtr
// 	    << std::endl;
// #endif // DEBUG
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

// #ifdef DEBUG
//   if(htet->verboseFace())
//     oofcerr << "IntersectionGroup::tentCheck: face=" << face
// 	    << " otherFace=" << otherFace << " tetEdge=" << tetEdge
// 	    << " faceEdge=" << faceEdge
// 	    << " n0=" << n0 << " n1=" << n1
// 	    << " e0=" << e0 << " e1=" << e1
// 	    << std::endl;
// #endif // DEBUG
  
  // Find the vectors in the directions of the edges from ptA and ptB
  // to ptX.  *Don't* just use the positions of those points, since
  // that'll be susceptible to round off error in exactly the
  // situations in which this calculation is important.  Use the
  // topological information instead.  If sharedPixelPlane returns
  // nullptr, it means that the points are connected along a tet face
  // and not a pixel plane, and this check is irrelevant.

  const PixelPlane *ppA = ptA->sharedPixelPlane(ptX, face);
  if(ppA == nullptr) {
// #ifdef DEBUG
//     if(htet->verboseFace())
//       oofcerr << "IntersectionGroup::tentCheck: ppA = nullptr!" << std::endl;
// #endif // DEBUG
    return true;
  }
  const PixelPlane *ppB = ptB->sharedPixelPlane(ptX, face);
  if(ppB == nullptr) {
// #ifdef DEBUG
//     if(htet->verboseFace())
//       oofcerr << "IntersectionGroup::tentCheck: ppB = nullptr!" << std::endl;
// #endif // DEBUG
    return true;
  }
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "IntersectionGroup::tentCheck: ppA=" << *ppA << " ppB=" << *ppB
// 	    << std::endl;
//     oofcerr << "IntersectionGroup::tentCheck: ppB->normal=" << ppA->normal()
// 	    << " ppB->normal=" << ppB->normal() << " faceNormal=" << faceNormal
// 	    << std::endl;
//   }
// #endif // DEBUG

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
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "IntersectionGroup::tentCheck: edgeVecA=" << edgeVecA
// 	    << " edgeVecB=" << edgeVecB << " Eperp=" << Eperp
// 	    << std::endl;
//     oofcerr << "IntersectionGroup::tentCheck: dotA=" << dotB << " dotB="
// 	    << dotB << std::endl;
//   }
// #endif // DEBUG
  // Check that edgeVecA points towards the interior and edgeVecB
  // points towards the exterior.
  if(dotA < 0 || dotB > 0) {
// #ifdef DEBUG
//     if(htet->verboseFace())
//       oofcerr << "IntersectionGroup::tentCheck: dot check failed"
// 	      << std::endl;
// #endif // DEBUG
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
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "IntersectionGroup::tentCheck: normalized edgeVecA=" << edgeVecA
// 	    << " edgeVecA dot E= " << dot(edgeVecA, E) << std::endl;
//     oofcerr << "IntersectionGroup::tentCheck: normalized edgeVecB=" << edgeVecB
// 	    << " edgeVecB dot E= " << dot(edgeVecB, E) << std::endl;
//     oofcerr << "IntersectionGroup::tentCheck: dotSum=" << dotSum << std::endl;
//     oofcerr << "IntersectionGroup::tentCheck: tA=" << feiA->edgePosition()
// 	    << " tB=" << feiB->edgePosition()
// 	    << " tA-tB=" << (feiA->edgePosition() - feiB->edgePosition())
// 	    << std::endl;
//   }
// #endif // DEBUG
  if((dotSum > 0 && feiA->edgePosition() > feiB->edgePosition()) ||
     (dotSum < 0 && feiA->edgePosition() < feiB->edgePosition()))
    {
// #ifdef DEBUG
//       if(htet->verboseFace())
// 	oofcerr << "IntersectionGroup::tentCheck: dotSum check failed"
// 		<< std::endl;
// #endif // DEBUG
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
// #ifdef DEBUG
//       if(htet->verboseFace()) {
// 	oofcerr << "IntersectionGroup::tentCheck: area test failed: area="
// 		<< area << std::endl;
//       }
// #endif // DEBUG
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

void IntersectionGroup::fixOccupiedEdges(
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
    return;
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
  }
} // end IntersectionGroup::fixOccupiedEdges

#define OLDFIXXING
#ifdef OLDFIXXING
void IntersectionGroup::fixCrossings(HomogeneityTet *htet, unsigned int face,
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

  // TODO: If the face is small there's a chance that all
  // intersections on all three edges of the face are in a single
  // IntersectionGroup.  In that case the method used here won't work.

  // This fix only handles crossing segments that have endpoints on
  // the same tet edge. 

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::fixCrossings: this=" << std::endl;
    std::cerr << *this << std::endl;
  }
  OOFcerrIndent indent(2);
#endif // DEBUG

  // This process rewrites the isecs vector.  The new vector is built
  // in newIsecs, which replaces isecs at the end.
  std::vector<FaceEdgeIntersection*> newIsecs;

  // beginIsec and endIsec delimit a range of FaceEdgeIntersections in
  // isecs that are on the same tet edge.
  unsigned int beginIsec = 0;
  while(beginIsec < size()) {
    unsigned int edgeno = isecs[beginIsec]->faceEdge();
    unsigned int endIsec = beginIsec;
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "IntersectionGroup::fixCrossings: beginIsec=" << beginIsec
	      << " edgeno=" << edgeno << std::endl;
    OOFcerrIndent indnt(2);
#endif // DEBUG
    do {
      endIsec++;
      // TODO: Don't compare faceEdge().  Use
      // PlaneIntersection::sharedFace(), as in
      // FaceEdgeIntersection::crosses().
    } while(endIsec < size() && isecs[endIsec]->faceEdge() == edgeno);

#ifdef DEBUG
    if(htet->verboseFace()) {
      oofcerr << "IntersectionGroup::fixCrossings: beginIsec=" << beginIsec
	      << " endIsec=" << endIsec << std::endl;
    }
#endif // DEBUG

    if(endIsec > beginIsec+1) {
      // There are two or more FaceEdgeIntersections on the same tet edge.
      
      // firstXing is the first segment in the group that crosses
      // another segment in the group.
      unsigned int firstXing = NONE;
      // tempXing is the segment that crosses firstXing.
      unsigned int tempXing = NONE;
      // Find the first segment that crosses any other
      for(unsigned int i=beginIsec; i<endIsec-1 && firstXing==NONE; i++) {
	for(unsigned int j=i+1; j<endIsec; j++) {
	  if(isecs[i]->crosses(isecs[j], face, htet
#ifdef DEBUG
			       , htet->verboseFace()
#endif // DEBUG
			       ))
	    {
#ifdef DEBUG
	      if(htet->verboseFace()) {
		oofcerr << "IntersectionGroup::fixCrossings:"
 			<< " found first crossing:" << std::endl;
		oofcerr << "IntersectionGroup::fixCrossings:   " << *isecs[i]
			<< std::endl;
		oofcerr << "IntersectionGroup::fixCrossings:   " << *isecs[j]
			<< std::endl;
	      }
#endif // DEBUG
	      firstXing = i;
	      tempXing = j;
	      break;
	    }
	}
      }
#ifdef DEBUG
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::fixCrossings: firstXing=" << firstXing
		<< " tempXing=" << tempXing << std::endl;
      }
#endif // DEBUG
      
      if(firstXing == NONE) {
	// There are no crossing segments in this segment range.  Copy
	// the range into newIsecs (which will replace isecs after
	// we're done here).
	for(unsigned int i=beginIsec; i<endIsec; i++)
	  newIsecs.push_back(isecs[i]);
	beginIsec = endIsec;
	continue;	// next iteration of while(beginIsec < size())
      }

      // Find the last segment that crosses any other.  It's either
      // tempXing or later, because tempXing > firstXing and tempXing
      // crosses another segment (firstXing).
      unsigned int lastXing = NONE;
      for(unsigned int i=endIsec-1; i>tempXing && lastXing==NONE; i--) {
	for(unsigned int j=beginIsec; j<i; j++) {
	  if(isecs[i]->crosses(isecs[j], face, htet
#ifdef DEBUG
			       , htet->verboseFace()
#endif // DEBUG
			       ))
	    {
#ifdef DEBUG
	      if(htet->verboseFace()) {
		oofcerr << "IntersectionGroup::fixCrossings:"
			<< " found last crossing:" << std::endl;
		oofcerr << "IntersectionGroup::fixCrossings:   " << *isecs[i]
			<< std::endl;
		oofcerr << "IntersectionGroup::fixCrossings:   " << *isecs[j]
			<< std::endl;
	      }
#endif // DEBUG
	      lastXing = i;
	      break;
	    }
	}
      }
      // The previous loop didn't check tempXing, because it's a known
      // crossing.  If the loop didn't find another crossing, tempXing is
      // the last one.
      if(lastXing == NONE)
	lastXing = tempXing;
      
      // #ifdef DEBUG
      //   if(htet->verboseFace()) {
      //     oofcerr << "IntersectionGroup::fixCrossings: lastXing=" << lastXing
      // 	    << std::endl;
      //   }
      // #endif // DEBUG

      // Make a new GenericIntersection merging the planes of all of the
      // original intersections.
      GenericIntersection *newPt = new GenericIntersection(htet);
      htet->extraPoints.insert(newPt);
      for(unsigned int i=firstXing; i<lastXing+1; i++) {
	isecs[i]->corner()->copyPlanesToIntersection(newPt);
      }
#ifdef DEBUG
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::fixCrossings: new GenericIntersection! "
		<< *newPt << std::endl;
      }
#endif // DEBUG
      newPt->computeLocation();
#ifdef DEBUG
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::fixCrossings:                         "
		<< " location3D=" << newPt->location3D()
		<< " getLocation3D=" << newPt->getLocation3D() << std::endl;
      }
#endif // DEBUG
      htet->checkEquiv(newPt);	// merges equivalence classees
#ifdef DEBUG
      if(htet->verboseFace()) {
	oofcerr << "IntersectionGroup::fixCrossings:                         "
		<< " back from checkEquiv" << std::endl;
      }
#endif // DEBUG
  // Find out where newPt is on the face.
      EdgePosition newT;
      unsigned int newEdge = NONE;
      htet->findFaceEdge(newPt, face, newEdge, newT); // computes newEdge, newT
      
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "IntersectionGroup::fixCrossings: newPt=" << *newPt << std::endl;
//   }
// #endif // DEBUG

      unsigned int nStarts = 0;
      unsigned int nEnds = 0;
      for(unsigned int i=firstXing; i<=lastXing; i++) {
	if(isecs[i]->start())
	  nStarts++;
	else
	  nEnds++;
      }

      // Replace entries in the LooseEndSet with new ones using newPt, or
      // discard them if they're part of a start/end pair.  keepStarts is
      // the number of start points to keep.  Since all the points will
      // end up at the same place, it doesn't matter which ones we keep as
      // long as we end up with the right number of starts and ends.
      unsigned int keepStarts = nStarts > nEnds ? nStarts-nEnds : 0;
      unsigned int keepEnds   = nEnds > nStarts ? nEnds-nStarts : 0;
// #ifdef DEBUG
//   if(htet->verboseFace())
//     oofcerr << "IntersectionGroup::fixCrossings: keepStarts=" << keepStarts
// 	    << " keepEnds=" << keepEnds << std::endl;
// #endif // DEBUG
      unsigned int startCount = 0;	// number of start points already kept
      unsigned int endCount = 0;
      newIsecs.insert(newIsecs.end(), isecs.begin(), isecs.begin()+firstXing);
      if(keepStarts > 0 || keepEnds > 0) {
	for(unsigned int i=firstXing; i<=lastXing; i++) {
	  FaceEdgeIntersection *oldfei = isecs[i];
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
	}
      }
      else {
	// Don't keep any of the endpoints of crossing segments.
	for(unsigned int i=firstXing; i<=lastXing; i++)
	  looseEnds.erase(isecs[i]);
      }
      newIsecs.insert(newIsecs.end(), isecs.begin()+lastXing+1, isecs.end());
    } // end if there is more than one intersection on the edge

    else {
      // There's only one FaceEdgeIntersection on the edge.  Copy it
      // to newIsecs.
      newIsecs.push_back(isecs[beginIsec]);
    }
    
    beginIsec = endIsec;
  } // end while beginIsec < isecs.size()
  isecs = std::move(newIsecs);

#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::fixCrossings: done" << std::endl;
#endif // DEBUG
} // end IntersectionGroup::fixCrossings
#endif // OLDFIXXING

//#define NEWFIXXING
#ifdef NEWFIXXING
void IntersectionGroup::fixCrossings(HomogeneityTet *htet, unsigned int face,
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

  // This process rewrites the isecs vector.  The new vector is built
  // in newIsecs, which replaces isecs at the end.
  std::vector<FaceEdgeIntersection*> newIsecs;

  // Look for an incoming segment that crosses an outgoing segment,
  // and the incoming intersection point on the face perimeter is
  // *after* the the outgoing segment.
  
  unsigned int i = 0;	// loop over segments in the IntersectionGroup
  while(i+1 < isecs.size()) {
    if(!isecs[i]->start()) {
      // Look for a segment that crosses isecs[i]
      bool found = false;
      for(unsigned int j=i+1; j<isecs.size() && !found; j++) {
	if(isecs[j]->start()) {
	  if(isecs[i]->crosses(isecs[j], face, htet)) {
	    
	  } // end if isecs cross
	} // end if j is a start
      } // end loop over segments j
    } // end if i is not a start
  } // end loop over segments i
  
}
#endif // NEWFIXXING
