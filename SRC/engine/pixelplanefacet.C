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
#include <iterator>
#include <math.h>

#include "common/printvec.h"
#include "common/setutils.h"
#include "common/tostring.h"
#include "engine/cskeletonelement.h"
#include "engine/homogeneitytet.h"
#include "engine/pixelplanefacet.h"
#include "engine/planeintersection.h"

/*
  Comments containing ascii art diagrams in this file are all inside
  C-style comment blocks.  This prevents g++ from complaining about
  multi-line comments when a line in a diagram ends with a backslash.
  Suppressing the warnings with -Wno-comment at compile time was
  deemed to be dangerous.
*/

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void FacePlane::print(std::ostream &os) const {
  os << face_;
  // os << "FacePlane(" << "face=" << face_ << ", offset=" << offset_
  //    << ", normal=" << unitNormal_ << ")";
}

void FacePixelPlane::print(std::ostream &os) const {
  PixelPlane::print(os);
  os << " (face=" << face() << ")";
}

std::string HPixelPlane::shortName() const {
  return ("XYZ"[direction()] + to_string(normalOffset()) +
	  (normalSign() == 1 ? "+" : "-"));
}

std::string FacePlane::shortName() const {
  return "F" + to_string(face_);
}

std::string FacePixelPlane::shortName() const {
  return "FP" + to_string(face());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool HPixelPlane::isPartOf(const PixelPlaneIntersectionNR *fi) const {
  return fi->pixelPlanes().count(this) > 0;
}

void HPixelPlane::addToIntersection(PixelPlaneIntersectionNR *fi) const {
  fi->pixelPlanes().insert(this);
}

bool HPixelPlane::isInEquivalence(const IsecEquivalenceClass *eqclass) const {
  return eqclass->pixelPlanes.count(this) > 0;
}

void HPixelPlane::addToEquivalence(IsecEquivalenceClass *eqclass) const {
  eqclass->addPixelPlane(this);
}

bool FacePlane::isPartOf(const PixelPlaneIntersectionNR *fi) const {
  return fi->faces().count(this) > 0;
}

void FacePlane::addToIntersection(PixelPlaneIntersectionNR *fi) const {
  fi->faces().insert(this);
}

bool FacePlane::isInEquivalence(const IsecEquivalenceClass *eqclass) const {
  return eqclass->facePlanes.count(this) > 0;
}

void FacePlane::addToEquivalence(IsecEquivalenceClass *eqclass) const {
  eqclass->addFacePlane(this);
}

bool FacePixelPlane::isPartOf(const PixelPlaneIntersectionNR *fi) const {
  return fi->pixelFaces().count(this) > 0;
}

void FacePixelPlane::addToIntersection(PixelPlaneIntersectionNR *fi) const {
  fi->pixelFaces().insert(this);
}

void FacePixelPlane::addToEquivalence(IsecEquivalenceClass *eqclass) const {
  eqclass->addFacePixelPlane(this);
}

bool FacePixelPlane::isInEquivalence(const IsecEquivalenceClass *eqclass) const
{
  return eqclass->pixelFaces.count(this) > 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Functor for sorting intersections by their position along their
// shared polygon edge.  Used in PixelPlaneFacet::completeLoops and
// PixelPlaneFacet::resolveMultipleCoincidence

class LtPolyFrac {
private:
  const PixelPlaneFacet *facet;
public:
  LtPolyFrac(const PixelPlaneFacet *f) : facet(f) {}
  bool operator()(const PixelPlaneIntersection *fi0,
		  const PixelPlaneIntersection *fi1)
    const
  {
// #ifdef DEBUG
//     if(facet->verbose) {
//       // oofcerr << "LtPolyFrac::operator(): fi0=" << fi0 << " fi1=" << fi1
//       // 	      << std::endl;
//       oofcerr << "LtPolyFrac::operator(): fi0= " << *fi0 << std::endl;
//       oofcerr << "LtPolyFrac::operator(): fi1= " << *fi1 << std::endl;      
//     }
// #endif // DEBUG

    // TODO: sharedPolySegment might be too slow in this context.
    unsigned int sharedSeg = fi0->sharedPolySegment(fi1, facet);
// #ifdef DEBUG
//     if(facet->verbose)
//       oofcerr << "LtPolyFrac::operator(): sharedSeg=" << sharedSeg << std::endl;
// #endif // DEBUG
    if(sharedSeg != NONE) {
// #ifdef DEBUG
//       if(facet->verbose) {
// 	oofcerr << "LtPolyFrac:operator(): polyFrac0="
// 		<< fi0->getPolyFrac(sharedSeg, facet) << std::endl;
// 	oofcerr << "LtPolyFrac:operator(): polyFrac1="
// 		<< fi1->getPolyFrac(sharedSeg, facet) << std::endl;
//       }
// #endif // DEBUG
      return (fi0->getPolyFrac(sharedSeg, facet) <
	      fi1->getPolyFrac(sharedSeg, facet));
    }
    return false;
  }
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FacetEdge::FacetEdge(PixelPlaneIntersection *s, PixelPlaneIntersection *e)
  : start_(s), stop_(e), nullified_(false)
{
  start_->setEdge(this);
  stop_->setEdge(this);
}

FacetEdge::FacetEdge(const FacetEdge &fe)
  : start_(fe.start_->clone()),
    stop_(fe.stop_->clone())
{
  start_->setEdge(this);
  stop_->setEdge(this);
}

FacetEdge::FacetEdge(FacetEdge &&fe) {
  PixelPlaneIntersection *temp = start_;
  start_ = fe.start_;
  fe.start_ = temp;
  temp = stop_;
  stop_ = fe.stop_;
  fe.stop_ = temp;
}

FacetEdge::~FacetEdge() {
  delete start_;
  delete stop_;
}

// bool FacetEdge::operator<(const FacetEdge &other) const {
//   return (*start_ < *other.start_ ||
// 	  (*start_ == *other.start_ && *stop_ < *other.stop_));
// }

double FacetEdge::length2() const {
  return norm2(start_->location3D() - stop_->location3D());
}

void FacetEdge::replacePoint(const PixelPlaneIntersection *oldPt,
			     PixelPlaneIntersection *newPt)
{
  if(oldPt == start_) {
    start_ = newPt;
    start_->setEdge(this);
    return;
  }
  assert(oldPt == stop_);
  stop_ = newPt;
  stop_->setEdge(this);
}

// Swap the edge's start point with its referent.
void FacetEdge::swapStart() {
  PixelPlaneIntersectionNR *temp = start_->referent();
  assert(temp != start_);
  assert(temp->getEdge() != this);
  temp->getEdge()->replacePoint(temp, start_);
  start_ = temp;
  start_->setEdge(this);
}

void FacetEdge::swapStop() {
  PixelPlaneIntersectionNR *temp = stop_->referent();
  assert(temp != stop_);
  assert(temp->getEdge() != this);
  temp->getEdge()->replacePoint(temp, stop_);
  stop_ = temp;
  stop_->setEdge(this);
}

// The FacetEdge base class defines a no-op version of
// getEdgesOnFaces.  PolygonEdges are the only edges created by
// HomogeneityTet::doFindPixelPlaneFacets that are on tet faces.

void PolygonEdge::getEdgesOnFaces(HomogeneityTet *htet,
				  const HPixelPlane *pixplane,
				  FaceFacets &faceFacets)
  const
{
  start_->referent()->getEdgesOnFaces(htet, stop_->referent(), pixplane,
				      faceFacets);
}

Coord2D FacetEdge::startPos(const PixelPlane *p) const {
  return start_->location2D(p);
}

Coord2D FacetEdge::endPos(const PixelPlane *p) const {
  return stop_->location2D(p);
}

Coord3D FacetEdge::startPos3D() const {
  return start_->location3D();
}

Coord3D FacetEdge::endPos3D() const {
  return stop_->location3D();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PixelFacetEdge::PixelFacetEdge(TriplePixelPlaneIntersection *s,
			       TriplePixelPlaneIntersection *e)
  : FacetEdge(s, e)
{}

StartFaceIntersectionEdge::StartFaceIntersectionEdge(
					     PixelPlaneIntersection *s,
					     TriplePixelPlaneIntersection *e)
  : FacetEdge(s, e)
{}

StopFaceIntersectionEdge::StopFaceIntersectionEdge(
					   TriplePixelPlaneIntersection *s,
					   PixelPlaneIntersection *e)
  : FacetEdge(s, e)
{}

PolygonEdge::PolygonEdge(PixelPlaneIntersection *f0, PixelPlaneIntersection *f1)
  : FacetEdge(f0, f1)
{}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PixelPlaneFacet::PixelPlaneFacet(HomogeneityTet *htet,
				 const HPixelPlane *pixplane,
				 const TetIntersectionPolygon &tetPts,
				 bool onFace
#ifdef DEBUG
				 , bool verbose
#endif // DEBUG

				 )
  : tetPts(tetPts),
    areaComputed_(false),
    onFace(onFace),
    htet(htet),
    pixplane(pixplane)
#ifdef DEBUG
  , verbose(verbose)
#endif // DEBUG
{
  // Map FacePlanes and FacePixelPlanes to polygon edge numbers.  Edge
  // e goes from tetPts[e] to tetPts[e+1].
  for(unsigned int i=0; i<tetPts.size(); i++) {
    const FacePlane *face = getFacePlane(i);
    assert(face != nullptr);
    faceEdgeMap[face] = i;
    const FacePixelPlane *fpp = htet->getCoincidentPixelPlane(face);
    if(fpp != nullptr)
      faceEdgeMap[fpp] = i;
  }
}

PixelPlaneFacet::~PixelPlaneFacet() {
  for(FacetEdge *edge : edges)
    delete edge;
}

const FacePlane *PixelPlaneFacet::getFacePlane(unsigned int f) const {
  assert(f != NONE);
  unsigned int g = f + 1;
  if(g == tetPts.size())
    g = 0;
  std::vector<const FacePlane*> faces = tetPts[f]->sharedFaces(tetPts[g]);
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::getFacePlane: tetPts[f=" << f << "]="
// 	    << *tetPts[f] << std::endl;
//     oofcerr << "PixelPlaneFacet::getFacePlane: tetPts[g=" << g << "]="
// 	    << *tetPts[g] << std::endl;
//     oofcerr << "PixelPlaneFacet::getFacePlane: faces=";
//     std::cerr << derefprint(faces);
//     oofcerr << std::endl;	
//   }
// #endif // DEBUG
  for(const FacePlane *face : faces) {
    // Use Plane::coincident instead of operator== here because the
    // planes stored in the tetPts have arbitrary orientations.
    if(!face->coincident(*pixplane)) {
// #ifdef DEBUG
//       if(verbose) {
// 	oofcerr << "PixelPlaneFacet::getFacePlane: face=" << *face
// 		<< std::endl;
//       }
// #endif	// DEBUG
      return face;
    }
  }
  throw ErrProgrammingError("getFacePlane failed!", __FILE__, __LINE__);
}

const FacePixelPlane *PixelPlaneFacet::getBaseFacePlane() const {
  // TODO: This result should just be stored in the PixelPlaneFacet.
  // There's no need to be looking it up all the time.
  return htet->getCoincidentFacePlane(pixplane);
}

unsigned int PixelPlaneFacet::getPolyEdge(const Plane *fp) const {
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::getPolyEdge: fp=" << *fp << std::endl;
// #endif // DEBUG
  FaceEdgeMap::const_iterator e = faceEdgeMap.find(fp);
  if(e != faceEdgeMap.end())
    return (*e).second;
  return NONE;
}

void PixelPlaneFacet::clear() {
  for(FacetEdge *edge : edges)
    delete edge;
  edges.clear();
  faceEdgeMap.clear();
  area_ = 0;
  areaComputed_ = true;
}

void PixelPlaneFacet::addEdge(FacetEdge *edge) {
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::addEdge: " << *edge << std::endl;
  }
#endif // DEBUG
  edges.push_back(edge);
  areaComputed_ = false;
}

// addEdges adds edges to connect fi0 and fi1 along the perimeter of
// the polygon, going around the polygon corners if necessary.

void PixelPlaneFacet::addEdges(const PixelPlaneIntersection *fi0,
			       const PixelPlaneIntersection *fi1)
{
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::addEdges: fi0=" << *fi0 << std::endl;
//     oofcerr << "PixelPlaneFacet::addEdges: fi1=" << *fi1 << std::endl;
//   }
//   OOFcerrIndent indent(2);
// #endif // DEBUG
  unsigned int startSeg = fi0->maxPolyEdge(this);
  unsigned int endSeg = fi1->minPolyEdge(this);
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::addEdges: startSeg=" << startSeg
// 	    << " endSeg=" << endSeg << std::endl;
// #endif	// DEBUG
  assert(startSeg != NONE && endSeg != NONE);
  if(startSeg == endSeg &&
     fi0->getPolyFrac(startSeg, this) <= fi1->getPolyFrac(startSeg, this))
    {
      // The points are on the same polygon edge.
      addEdge(new PolygonEdge(fi0->clone(), fi1->clone()));
    }
  else {
    // The points are on different polygon edges, or the end is before
    // the start on the same edge.  Add the segment between the exit
    // and the first corner.
    unsigned int nn = polygonSize();
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::addEdges: adding initial " << *fi0
// 	      << " to tetPts[" << (startSeg+1)%nn << "]" << std::endl;
// #endif // DEBUG
    addEdge(new PolygonEdge(fi0->clone(), tetPts[(startSeg+1)%nn]->clone()));
    // If there is more than one intermediate corner, then there are
    // one or more intermediate segments that span an entire polygon
    // edge.
    unsigned int seg = startSeg + 1;
    if(seg == nn)
      seg = 0;
    unsigned int nextseg = seg + 1;
    if(nextseg == nn)
      nextseg = 0;
     
    while(seg != endSeg) {
// #ifdef DEBUG
//       if(verbose)
// 	oofcerr << "PixelPlaneFacet::addEdges: adding intermediate: "
// 		<< "tetPts[" << seg << "] to tetPts[" << nextseg << "]"
// 		<< std::endl;
// #endif	// DEBUG
      addEdge(new PolygonEdge(tetPts[seg]->clone(), tetPts[nextseg]->clone()));
      seg = nextseg;
      nextseg++;
      if(nextseg == nn)
	nextseg = 0;
    }
    
    // Add the segment between the last corner and the entry.
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::addEdges: adding final "
// 	      << "tetPts[" << endSeg << "] to " << *fi1 << std::endl;
// #endif // DEBUG
    addEdge(new PolygonEdge(tetPts[endSeg]->clone(), fi1->clone()));
  }
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::addEdges: done" << std::endl;
// #endif // DEBUG
}

double PixelPlaneFacet::area() const {
  if(areaComputed_) {
    return area_;
  }
  if(edges.empty())
    area_ = 0.0;
  else
    area_ = getArea();
  areaComputed_ = true;
  return area_;
}

double PixelPlaneFacet::getArea() const {
  if(edges.size() <= 2)
    return 0.0;

  // TODO: If this is too slow, try not computing the center and
  // subtracting it from the positions before taking the cross
  // product.  Subtracting the center is meant to increase accuracy by
  // preventing the subtraction of large numbers.
  Coord2D center(0.0, 0.0);
  for(const FacetEdge *edge : edges) {
    center += edge->startPos(pixplane) + edge->endPos(pixplane);
  }
  center /= 2.0*edges.size();

  double a = 0.0;
  
  // Don't include pairs of oppositely directed edges with equivalent
  // endpoints.  If these are the only edges in a facet, round-off
  // error can make the area appear to be non-zero when it should be
  // zero.
  std::vector<bool> includeEdge(edges.size(), true);
  for(unsigned int i=0; i<edges.size(); i++) {
    if(includeEdge[i]) {
      for(unsigned int j=i+1; j<edges.size() && includeEdge[i]; j++) {
	if(includeEdge[j]) {
	  if(edges[i]->startPt()->isEquivalent(edges[j]->endPt()) &&
	     edges[j]->startPt()->isEquivalent(edges[i]->endPt()))
	    {
	      includeEdge[i] = false;
	      includeEdge[j] = false;
	    }
	}
      }
    }
    if(includeEdge[i]) {
      a += ((edges[i]->startPos(pixplane) - center) %
	    (edges[i]->endPos(pixplane) - center));
    }
  }
  return 0.5*a;
}

BarycentricCoord PixelPlaneFacet::polygonCornerBary(unsigned int i) const {
  return tetPts[i]->baryCoord(htet);
}

Coord2D PixelPlaneFacet::polygonCorner(unsigned int i) const {
  return pixplane->convert2Coord2D(tetPts[i]->location3D());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utilities used by PixelPlaneFacet::completeLoops

#define CLOSEBY 0.3
#define CLOSEBY2 (CLOSEBY*CLOSEBY)

static int storeCoincidenceData(PixelPlaneIntersectionNR *isec,
				const HPixelPlane *pixplane,
				std::set<Coord2D> &coincidentLocs,
				IsecsNearCoord &coincidences)
{
  Coord2D loc = pixplane->convert2Coord2D(isec->location3D());
  for(Coord2D p : coincidentLocs) {
    if(norm2(loc-p) < CLOSEBY2) {
      coincidences.insert(IsecsNearCoord::value_type(p, isec));
      return 1;			// possible coincidence detected
    }
  }
  coincidences.insert(IsecsNearCoord::value_type(loc, isec));
  coincidentLocs.insert(loc);
  return 0;			// no coincidence detected
}

// class NullEdgePredicate {
// private:
//   const HomogeneityTet *htet;
// public:
//   NullEdgePredicate(const HomogeneityTet *htet) : htet(htet) {}
//   bool operator()(const FacetEdge *edge) const  {
//     bool result = edge->startPt()->isEquivalent(edge->endPt());
// #ifdef DEBUG
//     if(htet->verboseplane) {
//       oofcerr << "NullEdgePredicate: edge=" << *edge
// 	      << " null=" << result
// 	      << std::endl;
//     }
// #endif // DEBUG
//     return result;
//   }
// };

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


bool PixelPlaneFacet::completeLoops() {
  // When this is called by doFindPixelPlaneFacets, the facet consists
  // of an ordered vector of segments, whose endpoints are all
  // TriplePixelPlaneIntersections or SimpleIntersections.  If the endpoint
  // of one segment is not the startpoint of the next, then (a) the
  // two points must be SimpleIntersections, and (b) there are missing
  // segments along the edges of the polygon.  However, some cleanup
  // must be done first.
  //
  // (1) Look for intersection points on polygon edges that are within
  //     a fraction of a voxel length of each other.  These can only
  //     come from VSB segments that meet at a voxel corner that lies
  //     on or near one or more polygon edges, and are the only points
  //     that can be mis-ordered due to round-off error, or duplicated
  //     due to the end of one VSB segment and the start of the next
  //     both being counted.
  //
  // (2) Use topological information to fix the misordered sets of
  //     points by merging them together.  Since round-off error
  //     caused them to be misordered, it's safe to assume that they
  //     are coincident.  This converts SimpleIntersections into
  //     instances of other subclasses of PixelPlaneIntersection.
  //
  // (3) Add missing segments between the PixelPlaneIntersections.
  
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::completeLoops: initial facet=" << *this
	    << std::endl;
  }
#endif // DEBUG

  std::set<Coord2D> coincidentLocs; // locations where coincidences occur
  IsecsNearCoord coincidences; // All intersections at a point
  unsigned int totalIntersections = 0;

  for(FacetEdge *edge : edges) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::completeLoops: edge=" << edge
// 	      << " " << *edge << std::endl;
// #endif	// DEBUG

    // Calling referent() is sort of silly here, but it's possibly
    // cheaper than using a dynamic_cast to convert the
    // PixelPlaneIntersection in the FacetEdge to a
    // PixelPlaneIntersectionNR.  At this point the intersection can't
    // be a RedundantIntersection.
    if(edge->startFace())
      totalIntersections += storeCoincidenceData(edge->startFace()->referent(),
						 pixplane,
						 coincidentLocs,
						 coincidences);
    if(edge->stopFace())
      totalIntersections += storeCoincidenceData(edge->stopFace()->referent(),
						 pixplane,
						 coincidentLocs,
						 coincidences);
    
  } // end loop over edges

// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::completeLoops: done with edge loop"
// 	    << std::endl;
// #endif	// DEBUG

  // Resolve coincidences that occur when a voxel corner is on or near
  // a tet face.  In that case roundoff error can put points in the
  // wrong order on an edge.

  for(Coord2D loc : coincidentLocs) {
#ifdef DEBUG
    if(verbose)
      oofcerr << "PixelPlaneFacet::completeLoops: looking for coincidence at "
	      << loc << " " << pixplane->convert2Coord3D(loc) << std::endl;
#endif // DEBUG
    if(coincidences.count(loc) > 1) {
      auto range = coincidences.equal_range(loc);
#ifdef DEBUG
      if(verbose) {
	oofcerr << "PixelPlaneFacet::completeLoops: resolving coincidence at "
		<< loc << " " << pixplane->convert2Coord3D(loc) << std::endl;
	oofcerr << "PixelPlaneFacet::completeLoops: coincident points are:"
		<< std::endl;
	for(auto r=range.first; r!=range.second; ++r) {
	  OOFcerrIndent indent(4);
	  oofcerr << "PixelPlaneFacet::completeLoops: "
		  << *dynamic_cast<PixelPlaneIntersectionNR*>((*r).second)
		  << std::endl;
	}
      }
      OOFcerrIndent indent(2);
#endif // DEBUG
      // First, copy the intersections at this location into a set,
      // and merge ones that are at *identical* positions.
      std::set<PixelPlaneIntersectionNR*> uniqueIsecs;
      for(auto pp=range.first; pp!=range.second; ++pp) {
	PixelPlaneIntersectionNR *p = (*pp).second;
	bool replaced = false;
	for(PixelPlaneIntersectionNR *q : uniqueIsecs) {
	  if(q->isEquivalent(p)) {
#ifdef DEBUG
	    if(verbose) {
	      oofcerr << "PixelPlaneFacet::completeLoops: merging identical pts"
		      << std::endl;
	    }
#endif // DEBUG
	    PixelPlaneIntersectionNR *merged = q->mergeWith(htet, p, this);
	    if(merged) {
#ifdef DEBUG
	      if(verbose) {
		oofcerr << "PixelPlaneFacet::completeLoops: merged "
			<< *q << " and " << *p << std::endl;
		oofcerr << "PixelPlaneFacet::completeLoops:  result="
			<< *merged << std::endl;
	      }
#endif // DEBUG
	      replaceIntersection(q, merged);
	      replaceIntersection(p, new RedundantIntersection(merged, this));
	      uniqueIsecs.erase(q);
	      if(merged->crossingType() != NONCROSSING)
		uniqueIsecs.insert(merged);
	      replaced = true;
	      break;
	    }
	  }
	}
	if(!replaced) {
	  uniqueIsecs.insert(p);
	}
      }	// end loop over intersections at this coincidence location
      
      int nIntersections = uniqueIsecs.size();
#ifdef DEBUG
      if(verbose)
	oofcerr << "PixelPlaneFacet::completeLoops: resolving "
		<< nIntersections << "-fold coincidence at " << loc
		<< std::endl;
#endif // DEBUG
      if(nIntersections == 2) {
	if(!resolveTwoFoldCoincidence(uniqueIsecs)) {
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "PixelPlaneFacet::completeLoops: failed at "
		    << loc << std::endl;
	  }
#endif // DEBUG
	  return false;
	}
      }
      else if(nIntersections == 3) {
	if(!resolveThreeFoldCoincidence(uniqueIsecs)) {
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "PixelPlaneFacet::completeLoops: failed at "
		    << loc << std::endl;
	  }
#endif // DEBUG
	  return false;
	}
      }
      else if(nIntersections > 3) {
	if(!resolveMultipleCoincidence(uniqueIsecs, totalIntersections)) {
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "PixelPlaneFacet::completeLoops: failed at "
		    << loc << std::endl;
	  }
#endif // DEBUG
	  return false;
	}
      }
#ifdef DEBUG
      if(verbose) {
	oofcerr << "PixelPlaneFacet::completeLoops: resolved coincidence at "
		<< loc << std::endl;
      }
#endif // DEBUG
    } // end if there is more than one intersection near loc
  }   // end loop over locations loc of intersection positions

#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::completeLoops: after resolving coincidences,"
	    << " facet=" << *this << std::endl;
  }
#endif	// DEBUG

  // Remove edges that join equivalent intersection points.
  removeNullEdges();

#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::completeLoops: after removing null edges,"
	    << " facet=" << *this << std::endl;
  }
#endif	// DEBUG

  // Construct the lists of intersections on each edge, now including
  // only the topologically distinct intersections
  // (RedundantIntersection::locateOnPolygonEdge() is a no-op).

  // PolyEdgeIntersections is vector of PixelPlaneIntersection*s.
  std::vector<PolyEdgeIntersections> polyEdgeIntersections(tetPts.size());

  for(FacetEdge *edge : edges) {
    edge->startPt()->locateOnPolygonEdge(polyEdgeIntersections, this);
    edge->endPt()->locateOnPolygonEdge(polyEdgeIntersections, this);
  }

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::completeLoops: done with locateOnPolygonEdge"
// 	    << std::endl;
//     OOFcerrIndent indent(2);
//     for(unsigned int e=0; e<polyEdgeIntersections.size(); e++) {
//       if(!polyEdgeIntersections[e].empty()) {
// 	oofcerr << "PixelPlaneFacet::completeLoops: polyEdgeIntersections[" << e
// 		<< "]=" << std::endl;
// 	OOFcerrIndent indnt(2);
// 	for(const PixelPlaneIntersection *fib : polyEdgeIntersections[e]) {
// 	  oofcerr << "PixelPlaneFacet::completeLoops:   " << *fib << std::endl;
// 	}
//       }
//     }
//   }
// #endif // DEBUG

  // Sort the polyEdgeIntersections by polyFrac (position along the
  // edge).  TODO: This is inefficient, since LtPolyFrac computes the
  // shared polygon edge for each pair of points that it compares.  In
  // this case we already know the polygon edge.
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::completeLoops: sorting" << std::endl;
// #endif  // DEBUG
  for(PolyEdgeIntersections &polyedge : polyEdgeIntersections) {
    std::sort(polyedge.begin(), polyedge.end(), LtPolyFrac(this));
// #ifdef DEBUG
//     if(verbose) {
//       if(!polyedge.empty()) {
// 	oofcerr << "PixelPlaneFacet::completeLoops: sorted polyedge="
// 		<< std::endl;
// 	for(auto fib : polyedge) {
// 	  OOFcerrIndent indent(2);
// 	  oofcerr << "PixelPlaneFacet::completeLoops:  " << *fib << std::endl;
// 	}
//       }
//     }
// #endif // DEBUG
  }

  // At this point, polyEdgeIntersections contains edge intersections
  // that are free from topological irregularities due to round-off
  // error.  Traverse the edges, adding segments along the polygon
  // between each VSB exit and entry.

  /*           /
  //  outside / inside polygon
  //     ----o----<---
  //     |  / exit   ^
  //     | / < < < < ^< < < < This polygon segment has to be added
  //     |/          ^
  //     o entry     ^
  //    /|           ^
  //   / |< < < < These VSB segments are already accounted for
  //  /  |
  */

  // Look for an exit.  If the first intersection found is an entry,
  // it's stored in firstEntry.
  const PixelPlaneIntersection *firstEntry = nullptr;
  // Similarly for non-crossing intersections, but there may be more
  // than one.  "First" means "before an exit was found".
  std::vector<const PixelPlaneIntersection*> firstNoncrossing;
  // currentExit is non-null if we've found an exit and are looking
  // for a matching entry.
  const PixelPlaneIntersection *currentExit = nullptr;
  bool started = false;

#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::completeLoops: filling gaps"
	    << std::endl;
    unsigned int n=0;
    for(auto const &edge : polyEdgeIntersections)
	n += edge.size();
    if(n > 0) {
      oofcerr << "PixelPlaneFacet::completeLoops: intersections are:"
	      << std::endl;
      OOFcerrIndent indent(2);
      for(unsigned int e=0; e<tetPts.size(); e++) {
	oofcerr << "PixelPlaneFacet::completeLoops: e=" << e << std::endl;
	OOFcerrIndent ind(2);
	if(!polyEdgeIntersections[e].empty())
	  for(const PixelPlaneIntersection *fi : polyEdgeIntersections[e]) {
	    oofcerr << "PixelPlaneFacet::completeLoops: " << *fi
		    << std::endl;
	  }
	else
	  oofcerr << "PixelPlaneFacet::completeLoops: (empty)" << std::endl;
      }
    }
  }
#endif // DEBUG
  for(unsigned int e=0; e<tetPts.size(); e++) { // Loop over polygon edges
    OOFcerrIndent indent(2);
    for(const PixelPlaneIntersection *fi : polyEdgeIntersections[e]) {
      // Loop over isecs on edge
      CrossingType crossing = fi->referent()->crossingType();
#ifdef DEBUG
      if(verbose)
	oofcerr << "PixelPlaneFacet::completeLoops: current point="
		<< *fi->referent() << std::endl;
#endif // DEBUG
	
      if(crossing == EXIT) {
#ifdef DEBUG
	if(currentExit != nullptr) {
	  oofcerr << "PixelPlaneFacet::completeLoops: ------- aborting -------"
		  << std::endl;
	  oofcerr << "PixelPlaneFacet::completeLoops: facet=" << *this
		  << std::endl;
	  oofcerr << "PixelPlaneFacet::completeLoops: currentExit="
		  << *currentExit << std::endl;
	  oofcerr << "PixelPlaneFacet::completeLoops: fi=" << *fi
		  << std::endl;
	  throw ErrProgrammingError(
	    "Intersection matching failed!  Found two consecutive exits.",
	    __FILE__, __LINE__);
	}
#endif // DEBUG
	if(!started && firstEntry==nullptr) {
	  // If the first crossing found is an exit, then any
	  // non-crossings already found must be outside of an
	  // exit->entry pair, and should be discarded.
	  firstNoncrossing.clear();
	}
	started = true;
	currentExit = fi;
#ifdef DEBUG
	if(verbose)
	  oofcerr << "PixelPlaneFacet::completeLoops: found an exit: "
		  << *currentExit << std::endl;
#endif // DEBUG
      } // end if intersection is an exit
	
      else if(crossing == ENTRY) {
	if(currentExit == nullptr) {
	  if(firstEntry == nullptr) {
	    // We've only just begun, and the first intersection
	    // found was an entry.  Save it for later.
	    firstEntry = fi;
#ifdef DEBUG
	    if(verbose)
	      oofcerr << "PixelPlaneFacet::completeLoops: saving an entry: "
		      << *firstEntry << std::endl;
#endif // DEBUG
	  }
	  else {
#ifdef DEBUG
	    if(verbose)
	      oofcerr << "PixelPlaneFacet::completeLoops: extra entry: "
		      << *fi << std::endl;
#endif // DEBUG
	    throw ErrProgrammingError(
	      "Intersection matching failed! Found two consecutive entries.",
	      __FILE__, __LINE__);
	  }
	} // end if currentExit is null
	else {
	  // currentExit is not null.  Join currentExit to the
	  // current entry.
#ifdef DEBUG
	  if(verbose)
	    oofcerr << "PixelPlaneFacet::completeLoops: joining exit to entry"
		    << std::endl;
	  OOFcerrIndent indent(2);
#endif // DEBUG
	  addEdges(currentExit, fi);
	  currentExit = nullptr;
	} // end if currentExit is not null
      } // end if intersection is an entry

      else {
	// crossing == NONCROSSING.  Noncrossing intersections
	// insert breaks into existing perimeter segments but don't
	// do anything if they don't occur between an exit and an
	// entry.  There can be multiple noncrossing intersections
	// within a single exit/entry pair.
	if(!started) {
	  // If we've already found an entry but haven't found an
	  // exit, then this non-crossing intersection lies outside of
	  // an exit->entry pair and can be ignored.
	  if(!firstEntry) {
#ifdef DEBUG
	    if(verbose)
	      oofcerr << "PixelPlaneFacet::completeLoops: saving noncrossing: "
		      << *fi << std::endl;
#endif // DEBUG
	    firstNoncrossing.push_back(fi);
	  }
	} // end if !started
	else if(currentExit != nullptr) {
#ifdef DEBUG
	  if(verbose)
	    oofcerr << "PixelPlaneFacet::completeLoops: joining to noncrossing:"
		    << std::endl;
	    OOFcerrIndent indent(2);
#endif // DEBUG
	  addEdges(currentExit, fi);
	  currentExit = fi;
	}
      }	// end if crossing==NONCROSSING
	
    }	// end loop over PixelPlaneIntersections fi on edge e
  } // end loop over tet edges e


  // If we get here with a non-null currentExit, we must have started
  // in the middle of a segment, and firstEntry must also be non-null.
  // Add the segment(s) connecting currentExit and firstEntry.
  if(currentExit != nullptr) {
#ifdef DEBUG
    if(verbose) {
      oofcerr << "PixelPlaneFacet::completeLoops: not done after main loop finished" << std::endl;
      oofcerr << "PixelPlaneFacet::completeLoops: firstEntry=" << *firstEntry
	      << std::endl;
      oofcerr << "PixelPlaneFacet::completeLoops: currentExit=" << *currentExit
	      << std::endl;
      oofcerr << "PixelPlaneFacet::completeLoops: firstNoncrossing.size="
	      << firstNoncrossing.size() << std::endl;
    }
#endif // DEBUG
    assert(firstEntry != nullptr);
    if(firstNoncrossing.empty())
      addEdges(currentExit, firstEntry);
    else {
      addEdges(currentExit, firstNoncrossing[0]);
      for(unsigned int i=0; i<firstNoncrossing.size()-1; i++)
	addEdges(firstNoncrossing[i], firstNoncrossing[i+1]);
      addEdges(firstNoncrossing.back(), firstEntry);
    }
  }
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::completeLoops: done, facet=" << *this
// 	    << std::endl;
//   }
// #endif // DEBUG
  
  return true;
} // end PixelPlaneFacet::completeLoops

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// replaceIntersection replaces an intersection in the FacetEdges and
// updates references in the RedundantIntersections.  Since the
// FacetEdges own the intersections, this operation deletes the old
// intersection.

void PixelPlaneFacet::replaceIntersection(PixelPlaneIntersection *oldPt,
					  PixelPlaneIntersection *newPt)
  const
{
  // When an intersection is replaced, any RedundantIntersections that
  // refer to the old intersection have to be updated to refer to the
  // new one.  There aren't going to be a lot of such intersections,
  // so there's no need for a sophisticated search here, probably.
  for(RedundantIntersection *ri : redundantIntersections) {
    if(ri->referent() == oldPt)
      ri->update(newPt);
  }
  
  oldPt->getEdge()->replacePoint(oldPt, newPt);
  // htet->removeEquivalence(oldPt);
  delete oldPt;
}

void PixelPlaneFacet::newRedundantIntersection(RedundantIntersection *ri) {
  redundantIntersections.insert(ri);
}

void PixelPlaneFacet::removeRedundantIntersection(RedundantIntersection *ri) {
  redundantIntersections.erase(ri);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Remove edges whose start points are identical to their end
// points.  This is nontrivial because removing an edge deletes its
// end points, but there may be RedundantIntersections that refer to
// those points.  The geometry may be like this:
//  ...-------a B-c d-----...
// Points a, B, c, and d are all equivalent, and edge B-c is going
// to be removed.  B is the only non-RedundantIntersection, and a,
// c, and d all refer to it.  After removing we want to have
//  ...-------B d-----...
// where B is (still) a non-RedundantIntersection and d refers to
// it.  a and B should be swapped:
//  ...-------B a-c d-----...
// and a-c deleted
//  ...-------B d-----...
// d referred to B before the swap, and it still does.
// It would have been ok to swap B and d, too, leading to
//  ...-------a B-----...

void PixelPlaneFacet::removeNullEdges() {
  // First, mark the edges that will be removed.
  unsigned int nNullEdges = 0;
  for(FacetEdge *edge : edges) {
    if(edge->startPt()->isEquivalent(edge->endPt())) {
      ++nNullEdges;
      edge->nullify();
    }
  }
  if(nNullEdges == 0)
    return;
  std::vector<FacetEdge*> newedges;
  newedges.reserve(edges.size()-nNullEdges);
  for(FacetEdge *edge : edges) {
    if(!edge->nullified()) {
      PixelPlaneIntersection *startPt = edge->startPt();
      if(startPt->referent()->getEdge()->nullified()) {
	edge->swapStart();
      }
      PixelPlaneIntersection *stopPt = edge->endPt();
      if(stopPt->referent()->getEdge()->nullified()) {
	edge->swapStop();
      }
      newedges.push_back(edge);
    }
    // Don't delete the nullified edges within this loop, because
    // points on other as yet unexamined edges might still refer to
    // points on them.
  }
  
  // Now that the referents are safe in the newedges list, delete the
  // null edges.
  for(FacetEdge *edge : edges)
    if(edge->nullified()) {
      delete edge;
    }
  
  edges = newedges;
} // end PixelPlaneFacet::removeNullEdges

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the FacetEdges that are on a tet face and add them to the
// given FaceFacets object.

void PixelPlaneFacet::getEdgesOnFaces(FaceFacets &faceFacets) const {
  for(FacetEdge *edge : edges) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::getEdgesOnFaces: edge=" << *edge
// 	      << std::endl;
//     OOFcerrIndent indent(2);
// #endif // DEBUG
    edge->getEdgesOnFaces(htet, pixplane, faceFacets);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// // Given two PixelPlaneIntersections that are on contiguous VSB
// // segments, return the one that precedes the other when traversing
// // the VSB in the positive direction.  The arguments should be
// // pointers to SingleVSBMixIn objects.

// // TODO: Is this only used in classifyVSBcorner? YES  If so, there's no
// // need for a template.

// template <class TYPE1, class TYPE2>
// static const PixelPlaneIntersection *firstIntersection(TYPE1 *fi0, TYPE2 *fi1)
// {
//   assert(fi0 != fi1);
//   if(fi0->segEnd(1) == fi1->segEnd(0))
//     return fi0;
//   if(fi1->segEnd(1) == fi0->segEnd(0))
//     return fi1;
//   return nullptr;
// }


// Given two intersections that might be on contiguous VSB segments,
// return information about the corner formed by those segments.  If
// the returned TurnDirection is UNDEFINED, the corner doesn't exist.

static void classifyVSBcorner(const PixelPlaneIntersectionNR * const fi0,
			      const PixelPlaneIntersectionNR * const fi1,
			      const PixelPlaneIntersectionNR *&entryPt,
			      const PixelPlaneIntersectionNR *&exitPt,
			      const PixelPlaneIntersectionNR *&firstPt,
			      const PixelPlaneIntersectionNR *&secondPt,
			      ICoord2D &corner,
			      TurnDirection &turn
#ifdef DEBUG
			      , bool verbose
#endif // DEBUG
			      )
{
  assert(fi0 != fi1);
  assert(fi0->crossingType() != fi1->crossingType());
  if(fi0->crossingType() == ENTRY) {
    entryPt = fi0;
    exitPt = fi1;
  }
  else {
    entryPt = fi1;
    exitPt = fi0;
  }
  PixelBdyLoopSegment seg0, seg1;
  // getOrdering sets seg0, seg1, and corner if it's successful.
  ISEC_ORDER order = fi0->getOrdering(fi1, seg0, seg1, corner);
#ifdef DEBUG
  if(verbose)
    oofcerr << "classifyVSBcorner: order=" << order << std::endl;
#endif // DEBUG
  if(order == NONCONTIGUOUS) {
    // The points are on nonadjacent segments.
    firstPt = nullptr;
    secondPt = nullptr;
    turn = UNDEFINED;
  }
  else {
    if(order == FIRST) {
      firstPt = fi0;
      secondPt = fi1;
    }
    else if(order == SECOND) {
      firstPt = fi1;
      secondPt = fi0;
    }
    turn = turnDirection(seg0.firstPt(), corner, seg1.secondPt());
    assert(turn != STRAIGHT);
  }
} // end classifyVSBcorner

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool PixelPlaneFacet::resolveTwoFoldCoincidence(
			const std::set<PixelPlaneIntersectionNR*> &isecs)
{
  PixelPlaneIntersectionNR *fi0 = *isecs.begin();
  PixelPlaneIntersectionNR *fi1 = *isecs.rbegin();
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: fi0=" << *fi0
	    << std::endl;
    oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: fi1=" << *fi1
	    << std::endl;
  }
  OOFcerrIndent indent(2);
#endif // DEBUG

  if(fi0->crossingType() == fi1->crossingType()) {
    // Both VSB segments enter the polygon or both leave it.  The
    // intersections are redundant.  Or a polygon edge or corner lies
    // at the junction between two VSB loop segments, and was counted
    // twice.  This only occurs if both intersections have a common
    // polygon segment (ie tet face) or a common VSB loop segment (ie
    // pixel plane pair).

    /*         / outgoing polygon segment
    //        /
    // ------o--------- VSB edge
    //        \
    //         \ incoming polygon segment
    */
    
    if(fi0->onOnePolySegment(fi1, this) || fi0->onSameLoopSegment(fi1)) {
      replaceIntersection(fi1, new RedundantIntersection(fi0, this));
    }
  } // end if crossing types are the same
  else {
    // There's one entry and one exit.
    if(fi0->isEquivalent(fi1) || fi0->isMisordered(fi1, this)) {
#ifdef DEBUG
      if(verbose) {
	// oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence:"
	// 	<< " isEquivalent=" << fi0->isEquivalent(fi1)
	// 	<< " isMisordered=" << fi0->isMisordered(fi1, this)
	// 	<< std::endl;
	oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: "
		<< "trying to merge equivalent entry and exit" << std::endl;
      }
#endif // DEBUG
      PixelPlaneIntersectionNR *merged = fi0->mergeWith(htet, fi1, this);
      if(merged) {
	replaceIntersection(fi0, merged);
	replaceIntersection(fi1, new RedundantIntersection(merged, this));
      }
      else {
// #ifdef DEBUG
// 	if(verbose) {
// 	  oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: "
// 		  << "failed to merge entry and exit" << std::endl;
// 	}
// #endif // DEBUG
	return false;
      }
    }
  }
  return true;	     // coincidence handled
} // end PixelPlaneFacet::resolveTwoFoldCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool PixelPlaneFacet::resolveThreeFoldCoincidence(
			  const std::set<PixelPlaneIntersectionNR*> &isecs)
{
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: isecs="
	    << std::endl;
    OOFcerrIndent indent(2);
    for(PixelPlaneIntersectionNR *pi : isecs) {
      oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence:   "
	      <<  *pi << std::endl;
    }
  }
#endif // DEBUG
  std::vector<PixelPlaneIntersectionNR*> entries;
  std::vector<PixelPlaneIntersectionNR*> exits;
  entries.reserve(2);
  exits.reserve(2);
  for(PixelPlaneIntersection *ipt : isecs) {
    if(ipt->crossingType() == ENTRY)
      entries.push_back(ipt->referent());
    else if(ipt->crossingType() == EXIT)
      exits.push_back(ipt->referent());
  }
#ifdef DEBUG
  if(verbose)
    oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: #entries="
	    << entries.size() << " #exits=" << exits.size() << std::endl;
  if(entries.size() + exits.size() != 3) {
    throw ErrProgrammingError("Unexpected input to resolveThreeFoldCoincidence",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  if(entries.size() == 2) {
    if(entries[0]->onSameLoopSegment(entries[1])) {
      /* Two entries on the same VSB segment.
      //        \
      //         \
      //      ----8---    8 is a double intersection, where one polygon
      //      |  /        segment ends and another starts.
      //      | /
      //      |/
      //      o
      //     /|
      //    / |
      */

      // Keep the entry that's on the same polygon segment as the
      // exit.
      PixelPlaneIntersectionNR *keptEntry, *discardedEntry;
      if(entries[0]->onSameLoopSegment(exits[0])) {
	keptEntry = entries[0];
	discardedEntry = entries[1];
      }
      else {
	keptEntry = entries[1];
	discardedEntry = entries[0];
      }
      assert(keptEntry->onSameLoopSegment(exits[0]));
      assert(keptEntry->onSameFacePlane(exits[0], getBaseFacePlane()));
      replaceIntersection(discardedEntry, new RedundantIntersection(keptEntry,
								    this));
      // The retained intersections must past the test used for a
      // two-way coincidence on a polygon segment.
      if(vsbCornerCoincidence(keptEntry, exits[0])) {
	PixelPlaneIntersectionNR *newfi = keptEntry->mergeWith(
						       htet, exits[0], this);
	if(newfi) {
	  replaceIntersection(keptEntry, newfi);
	  replaceIntersection(exits[0], new RedundantIntersection(newfi, this));
	}
	else
	  return false;
      }
    } // end if both entries are on the same VSB segment
    else {
      // Two entries, but on different VSB segments.
      std::vector<PixelPlaneIntersectionNR*> mergers =
	tripleCoincidence(entries[0], entries[1], exits[0]);
      if(mergers.size() == 3) {
	/* Something like the configuration the left is changing to
	// something like the configuration on the right.
	//
	//    /\            pxl edge     
	// --o--o----      ---------o    
	//  /    \  |              /|\
	// /      \ |             / | \
	//         \|   ==>      /  |  \
	//          o           /   |   \
	//          |\         /    |    \
	//          | \             |     \ polygon edge
	*/
	PixelPlaneIntersectionNR *newfi = mergers[0]->mergeWith(
				htet,
				mergers[1]->mergeWith(htet, mergers[2], this),
				this);
	if(newfi) {
	  newfi->setCrossingType(ENTRY);
	  replaceIntersection(mergers[0], newfi);
	  replaceIntersection(mergers[1], new RedundantIntersection(newfi,
								    this));
	  replaceIntersection(mergers[2], new RedundantIntersection(newfi,
								    this));
	}
	else
	  return false;
      }
      else if(mergers.size() == 2) {
	/* One of two things is happening:
	//
	//    /\                  /\
	// --o--o----      ------o--o    	 -----o----  
	//  /    \  |           /   |\   	     / \  |  
	// /      \ |          /    | \  	    /   \ |  
	//         \|   ==>         |  \    or	         \|  
	//          o               |   \	          o  
	//          |\              |    \	          |\
	//          | \                   \	          |
	*/

	PixelPlaneIntersectionNR *newfi = mergers[0]->mergeWith(
							htet, mergers[1], this);
	if(newfi) {
	  replaceIntersection(mergers[0], newfi);
	  replaceIntersection(mergers[1], new RedundantIntersection(newfi,
								    this));
	}
	else
	  return false;
	
	// if(mergers[0]->facePlane() == mergers[1]->facePlane()) {
	//   // Case A
	//   if(vsbCornerCoincidence(mergers[0], mergers[1])) {
	//     swapIntersections(mergers[0], mergers[1]);
	//   }
	// }
	// else if(mergers[0]->onSameLoopSegment(mergers[1])) {
	//   // Case B
	//   if(polyCornerCoincidence(mergers[0], mergers[1])) {
	//     MultiFaceIntersection *mfi = mergers[0]->mergeWith(mergers[1]);
	//     replaceIntersection(mergers[0], mfi);
	//     replaceIntersection(mergers[1], new RedundantIntersection(mfii));
	//   }
	// }
	// else {
	//   throw ErrProgrammingError("Unresolvable triple coincidence!",
	// 			    __FILE__, __LINE__);
	// }

      }	// end if two points are merging
      else if(mergers.size() != 0) {
	throw ErrProgrammingError(
	  "Wrong number of intersections in resolveThreeFoldCoincidence!",
	  __FILE__, __LINE__);
      }
    } // end if there are two entries on different VSB segments
  } // end if entries.size == 2

  else if(exits.size() == 2) {
    // See above for comments. This is just like the entries.size()==2
    // block, but for exits.
    if(exits[0]->onSameLoopSegment(exits[1])) {
      PixelPlaneIntersectionNR *keptExit, *discardedExit;
      if(exits[0]->onSameLoopSegment(entries[0])) {
	keptExit = exits[0];
	discardedExit = exits[1];
      }
      else {
	keptExit = exits[1];
	discardedExit = exits[0];
      }
      assert(keptExit->onSameLoopSegment(exits[0]));
      assert(keptExit->onSameFacePlane(entries[0], getBaseFacePlane()));
      replaceIntersection(discardedExit, new RedundantIntersection(keptExit,
								   this));
      if(vsbCornerCoincidence(keptExit, entries[0])) {
	PixelPlaneIntersectionNR *newfi = keptExit->mergeWith(
						      htet, entries[0], this);
	if(newfi) {
	  replaceIntersection(keptExit, newfi);
	  replaceIntersection(entries[0], new RedundantIntersection(newfi,
								    this));
	}
	else
	  return false;
      }
    } // end if both exits are on the same VSB segment
    else {
      // Two exits, but on different VSB segments
// #ifdef DEBUG
//       if(verbose) {
// 	oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: 2 exits on different VSB segs" << std::endl;
//       }
// #endif // DEBUG
      std::vector<PixelPlaneIntersectionNR*> mergers =
	tripleCoincidence(exits[0], exits[1], entries[0]);
// #ifdef DEBUG
//       if(verbose) {
// 	oofcerr << "PixelPlaneFacet:resolveThreeFoldCoincidence: mergers.size="
// 		<< mergers.size() << std::endl;
// 	OOFcerrIndent indent(2);
// 	for(PixelPlaneIntersectionNR *ppi : mergers) {
// 	  oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: " << *ppi
// 		  << std::endl;
// 	}
//       }
// #endif // DEBUG
      if(mergers.size() == 3) {
	PixelPlaneIntersectionNR *mfi0 = mergers[1]->mergeWith(
						       htet, mergers[2], this);
// #ifdef DEBUG
// 	if(verbose) {
// 	  if(!mfi0)
// 	    oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: failed to merge 1 & 2!" << std::endl;
// 	else
// 	  oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: merged 1 & 2 "
// 		  << *mfi0 << std::endl;
// 	}
// #endif // DEBUG
	PixelPlaneIntersectionNR *mfi = mergers[0]->mergeWith(htet, mfi0, this);
// #ifdef DEBUG
// 	if(verbose) {
// 	  if(!mfi)
// 	    oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: failed to merge 0 & (1&2)!" << std::endl;
// 	  else
// 	    oofcerr << "PixelPlaneFacet::resolveThreeFoldCoincidence: merged 0 &(1&2) "
// 		    << *mfi << std::endl;
// 	}
// #endif // DEBUG
	if(mfi) {
	  mfi->setCrossingType(EXIT);
	  replaceIntersection(mergers[0], mfi);
	  replaceIntersection(mergers[1], new RedundantIntersection(mfi,
								    this));
	  replaceIntersection(mergers[2], new RedundantIntersection(mfi,
								    this));
	}
	else
	  return false;
      }
      else if(mergers.size() == 2) {
	PixelPlaneIntersectionNR *newfi = mergers[0]->mergeWith(
							htet, mergers[1], this);
	if(newfi) {
	  replaceIntersection(mergers[0], newfi);
	  replaceIntersection(mergers[1], new RedundantIntersection(newfi,
								    this));
	}
	else
	  return false;
      }	// end if two points are merging
      else if(mergers.size() != 0) {
	throw ErrProgrammingError(
	  "Wrong number of intersections in resolveThreeFoldCoincidence!",
	  __FILE__, __LINE__);
      }
    } // end if two exits are on different VSB segments
  } // end if there are two exits

  else {
    assert(exits.empty() || entries.empty());
    // There are three entries or exits.  This can only happen
    // if the polygon has a high aspect ratio and the
    // intersection is at a spot where two VSB loops meet at a
    // corner.
	
    /*   |    |      |
    //   |    |      |      8 is where one polygon segment
    //   |    V      |      ends and another begins on a VSB loop.
    //   |    |      |      o is where a polygon segment crosses
    //   |    |      |      a VSB loop.
    //  -o--<-+->----8--
    //   |    |      |
    //   |    |      |
    //   |    ^      |
    //   |    |      |
    */

    // The two intersections that share a VSB segment are
    // redundant.  One should be removed.

    std::vector<PixelPlaneIntersectionNR*> &isecs =
      entries.empty() ? exits : entries;
    unsigned int notShared =
      isecs[0]->onSameLoopSegment(isecs[1]) ? 2
      : (isecs[1]->onSameLoopSegment(isecs[2]) ? 0 : 1);
    unsigned int a = (notShared + 1) % 3;
    unsigned int b = (notShared + 2) % 3;
    assert(isecs[a]->onSameLoopSegment(isecs[b]));
    replaceIntersection(isecs[b], new RedundantIntersection(isecs[a], this));
  }
  return true;	   // success!
} // end PixelPlaneFacet::resolveThreeFoldCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// resolveMultipleCoincidence resolves (rare?) coincidences of four or
// more PixelPlaneIntersection points.  In principle it could be used
// for two or three point coincidences as well, but it might be slower
// than the functions above.

bool PixelPlaneFacet::resolveMultipleCoincidence(
			 const std::set<PixelPlaneIntersectionNR*> &isecs,
			 unsigned int totalInts)
{
  // Find which VSB loop segments and polygon segments are involved in
  // the given PixelPlaneIntersections.
  typedef std::set<unsigned int> PolySegSet;
  PolySegSet polySegSet;
  typedef std::multimap<unsigned int, PixelPlaneIntersectionNR*> PolySegIsecs;
  PolySegIsecs polySegIsecs;
  unsigned int npts = 0;

  for(PixelPlaneIntersectionNR *isec: isecs) {
    // At this point the points must be either SimpleIntersections or
    // MultiVSBIntersections.
    const SingleFaceBase *sfb = dynamic_cast<const SingleFaceBase*>(isec);
    assert(sfb != nullptr);
    unsigned int polyseg = faceEdgeMap[sfb->getFacePlane()];
    polySegSet.insert(polyseg);
    polySegIsecs.insert(PolySegIsecs::value_type(polyseg, isec));
    npts++;
  }
  
  // // Loop over the given intersection points.
  // for(auto ptiter=range.first; ptiter!=range.second; ++ptiter) {
  //   // The points haven't yet been modified by the coindidence detector,
  //   // so they're all SimpleIntersections.
  //   // ptiter is a IsecsNearCoord::iterator
  //   // *ptiter is a std::pair<Coord2D, SimpleIntersection*>
  //   SimpleIntersection *fi = (*ptiter).second;
  //   assert(fi != nullptr);
  //   unsigned int polyseg = faceEdgeMap[fi->getFacePlane()];
  //   polySegSet.insert(polyseg);
  //   polySegIsecs.insert(PolySegIsecs::value_type(polyseg, fi));
  //   npts++;
  // }

  // Create an ordered list of the polygon segments, possibly
  // wrapping.  If there's a gap in the ordering, start the sequence
  // after the gap.  That is, use [3,0,1] instead of [0,1,3].  If
  // there are two gaps, it doesn't matter which comes first.  [0,2]
  // and [2,0] are equivalent.
  std::vector<unsigned int> temp(polySegSet.begin(), polySegSet.end());
  std::vector<unsigned int> polySegVec;
  polySegVec.reserve(polySegSet.size());

  // polySegSet is ordered, so this loops over the segment numbers in
  // increasing order.
  int kprev = NONE;
  for(PolySegSet::const_iterator k=polySegSet.begin(); k!=polySegSet.end(); ++k)
    {
      unsigned int kk = *k;
      if(kprev != NONE && kk-kprev > 1) {
	// k is the start point
	polySegVec.insert(polySegVec.end(), k, polySegSet.end());
	polySegVec.insert(polySegVec.end(), polySegSet.begin(), k);
	break;
      }
      kprev = kk;
    }
  // If we got here without putting anything into polySegVec, then
  // there is no gap in the polygon list (or the gap is between the
  // last element and the first), and we can just use the ordering
  // from polySegSet, which has been copied to temp.
  if(polySegVec.empty())
    polySegVec = std::move(temp);

  // If all of the intersections on the polygon are within this
  // coincidence region, then when we examine pairs of adjacent points
  // we need to remember that the last point is adjacent to the first.
  bool wrapAround = (npts == totalInts);

  // Put the FaceIntersections in order going around the polygon
  std::vector<PixelPlaneIntersectionNR*> orderedFIs;
  orderedFIs.reserve(npts);
  for(unsigned int i=0; i<polySegVec.size(); i++) { // loop over polygon edges
    auto range = polySegIsecs.equal_range(i); // intersections on this edge
    std::vector<PixelPlaneIntersectionNR*>::iterator start = orderedFIs.end();
    for(auto s=range.first; s!=range.second; ++s) {
      orderedFIs.push_back((*s).second);
    }
    std::sort(start, orderedFIs.end(), LtPolyFrac(this)); // sort on this edge
  }

  // Check for doubled entries or exits.  These are points at which
  // the VSB passes through a vertex of the polygon.  Both of the
  // polygon edges at the vertex will have recorded an entry or an
  // exit.
  std::set<std::vector<PixelPlaneIntersectionNR*>::iterator> deleteMe;
  for(auto k=orderedFIs.begin(); k!=orderedFIs.end(); ++k) {
    auto knext = k+1;
    if(knext == orderedFIs.end()) {
      if(wrapAround)
	knext = orderedFIs.begin();
      else
	break;
    }
    if((*k)->crossingType() == (*knext)->crossingType()) {
      if(((*k)->getPolyEdge(this)+1)%tetPts.size()==(*knext)->getPolyEdge(this)
	 && (*k)->onSameLoopSegment(*knext))
	{
	  replaceIntersection(*k, new RedundantIntersection(*knext, this));
	  deleteMe.insert(k);	// for deletion from orderedFIs
	}
    }
  } // end loop over orderedFIs k
  
  // Delete in reverse order so as not to invalidate iterators.
  for(auto d=deleteMe.rbegin(); d!=deleteMe.rend(); ++d) {
    orderedFIs.erase(*d);
  }

  // Apply the other two-fold coincidence fixes (ie, check
  // isMisordered() and merge points) until there's nothing left to be
  // fixed.
  unsigned int nfixed = 0;
  do {
    nfixed = 0;
    std::vector<PixelPlaneIntersectionNR*> newOrder;
    std::set<std::vector<PixelPlaneIntersectionNR*>::iterator> deleteMe;
    // Loop over pairs of adjacent intersections
    for(auto k=orderedFIs.begin(); k!=orderedFIs.end(); ++k) {
      auto knext = k+1;
      if(knext == orderedFIs.end()) {
	if(wrapAround)
	  knext = orderedFIs.begin();
	else
	  break;      // break out of loop over pairs of intersections
      }
      PixelPlaneIntersectionNR *fi0 = *k;
      PixelPlaneIntersectionNR *fi1 = *knext;

      // If both intersections are entries or both are exits, and the
      // weren't fixed above, it means that one of them is out of
      // place wrt its other neighbor.  Don't fix it now.  It'll get
      // fixed when the pair containing its other neighbor is
      // examined.
      if(fi0->crossingType() != fi1->crossingType()) {

	if(fi0->isMisordered(fi1, this)) {
	  PixelPlaneIntersectionNR *newfi = fi0->mergeWith(htet, fi1, this);
	  if(newfi) {
	    replaceIntersection(fi0, newfi);
	    replaceIntersection(fi1, new RedundantIntersection(newfi, this));
	    newOrder.push_back(newfi);
	  }
	  else
	    return false;
	  orderedFIs.erase(knext);
	  ++nfixed;
	}
	
	
      }	// end if intersections aren't both entries or both exits
      else {
	newOrder.push_back(fi0);
      }
    } // end loop over neighboring pairs of intersections
    orderedFIs = std::move(newOrder);
  } while(nfixed > 0); 

  return true;
} // end PixelPlaneFacet::resolveMultipleCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// These methods check for the illegal topology created by round-off
// error at coincident pairs of points.

// vsbCornerCoincidence checks two intersections that are on the
// same segment of the polygon.


/*             / polygon segment
//            /
//         --o--------------- VSB segment
//         |/
//         o
//        /|
//       / |
//      /  |
//     /   |
//         |
*/

// If the two voxel set boundary segments make a right turn, we expect
// the entry point to be before the exit when traversing the polygon
// boundary (no matter which way the polygon boundary goes).  If they
// make a left turn, the exit must be before the entry.

bool PixelPlaneFacet::vsbCornerCoincidence(const PixelPlaneIntersectionNR *fi0,
					   const PixelPlaneIntersectionNR *fi1)
  const
{
  assert(fi0 != fi1);
  assert(fi0->onOnePolySegment(fi1, this));
  assert(!fi0->samePixelPlanes(fi1));
  assert(fi0->crossingType() != fi1->crossingType());
  const PixelPlaneIntersectionNR *entryPt, *exitPt, *firstPt, *secondPt;
  ICoord2D corner;
  TurnDirection turn;
  classifyVSBcorner(fi0, fi1, entryPt, exitPt, firstPt, secondPt, corner, turn
#ifdef DEBUG
		    , verbose
#endif // DEBUG
		    );
  // If the two voxel set boundary segments make a right turn, we
  // expect the entry point to be before the exit when traversing the
  // polygon boundary (no matter which way the polygon boundary goes).
  // If they make a left turn, the exit must be before the entry.
  unsigned int polyseg = fi0->sharedPolySegment(fi1, this);
  double entryPolyFrac = entryPt->getPolyFrac(polyseg, this);
  double exitPolyFrac = exitPt->getPolyFrac(polyseg, this);
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::vsbCornerCoincidence: entryPt=" << *entryPt
	    << " exitPt=" << *exitPt <<  std::endl
	    << "                                     : turn=" << turn
	    << std::endl
	    << "                                     : entryPolyFrac="
	    << entryPolyFrac << " exitPolyFrac=" << exitPolyFrac
	    << " diff=" << (exitPolyFrac - entryPolyFrac)
	    << std::endl;
  }
#endif // DEBUG
  return ((turn == LEFT && entryPolyFrac <= exitPolyFrac)
	  ||
	  (turn == RIGHT && entryPolyFrac >= exitPolyFrac)
	  ||
	  (turn == UTURN && entryPolyFrac == exitPolyFrac)
	  );
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// polyCornerCoincidence checks two intersections on the same VSB loop
// segment but different polygon segments.

/*               
//            /\
//  ---------o--o------------ VSB segment
//          /    \
//         /      \
//        /        \ polygon segments
//       /  
//      /   
//
//  It could also look like this:
//          _______
//         /       \
// -------o---------o----------
//       /           \
//      /             \
*/

bool PixelPlaneFacet::polyCornerCoincidence(const PixelPlaneIntersectionNR *fi0,
					    const PixelPlaneIntersectionNR *fi1)
  const
{
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::polyCornerCoincidence: fi0=" << *fi0
// 	    << std::endl;
//     oofcerr << "PixelPlaneFacet::polyCornerCoincidence: fi1=" << *fi1
// 	    << std::endl;
//   }
// #endif // DEBUG
  assert(fi0 != fi1);
  assert(!fi0->onSameFacePlane(fi1, getBaseFacePlane())); // diff. polygon segs
  assert(fi0->onSameLoopSegment(fi1)); // same VSB segment
  assert(fi0->crossingType() != fi1->crossingType());
  const PixelBdyLoopSegment *seg = fi0->sharedLoopSegment(fi1);
  return ((fi0->crossingType() == ENTRY &&
	   fi0->getLoopFrac(*seg) >= fi1->getLoopFrac(*seg))
	  ||
	  (fi1->crossingType() == ENTRY &&
	   fi1->getLoopFrac(*seg) >= fi0->getLoopFrac(*seg)));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

//  Coincident polygon corner and VSB corner.  There are three legal
//  possibilities for the polygon edge geometry, each of which can
//  exist with either direction of the VSB boundary.

/*                   _/                  |
//    polygon      _/polygon       poly  |  polygon
//    exterior   _/  interior      int.  |  exterior
//             _/                        |
//          --o-------------          ---o-----------
//          |@ <- polygon             |  |
//          o     corner              |  @
//         /|                         | /
//        / |                         |/
//       /  |                         o
//          |                        /|
//                                  / |
//
// @_	
// \ \_
//  \  \_
//   \   \_                              The straight line directions available 
//    \    \_                            to the ascii artist are limited.
//     \     \_   
//      \   ---o------------
//       \  |    \_
//        \ |      \_
//         \|  poly
//          o   int.
//          |\
//          | \
//          |
*/

bool PixelPlaneFacet::polyVSBCornerCoincidence(
				       const PixelPlaneIntersectionNR *fi0,
				       const PixelPlaneIntersectionNR *fi1)
  const
{
  assert(fi0 != fi1);
  assert(!fi0->onSameFacePlane(fi1, getBaseFacePlane()));
// #ifdef DEBUG
//   if(verbose) {
//     if(fi0->samePixelPlanes(fi1)) {
//       oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: same pixel planes!"
// 	      << std::endl;
//       oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: fi0=" << *fi0
// 	      << std::endl;
//       oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: fi1=" << *fi1
// 	      << std::endl;
//     }
//   }
// #endif // DEBUG
  assert(!fi0->samePixelPlanes(fi1));
  assert(fi0->crossingType() != fi1->crossingType());
  const PixelPlaneIntersectionNR *entryPt, *exitPt, *firstPt, *secondPt;
  ICoord2D corner;
  TurnDirection turn;
  classifyVSBcorner(fi0, fi1, entryPt, exitPt, firstPt, secondPt, corner, turn
#ifdef DEBUG
		    , verbose
#endif // DEBUG
		    );
  BarycentricCoord bcorner = htet->getBarycentricCoord(corner, pixplane);
  // If the VSB corner is interior to the polygon, the entry point
  // must precede the exit point on the VSB. If the VSB corner is
  // outside, the entry and exit must be in the opposite order.  If
  // the order is wrong, the points must coincide, and this function
  // returns true.
  bool inside = bcorner.interior(onFace);

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
// 	    << "fi0=" << *fi0 << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
// 	    << "fi1=" << *fi1 << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
// 	    << "  firstPt=" << *firstPt << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
// 	    << " secondPt=" << *secondPt << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: inside="
// 	    << inside << std::endl;
//   }
// #endif // DEBUG
  bool invalid = ((inside && exitPt == firstPt) ||
		  (!inside && entryPt == secondPt));
  return invalid;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Triple coincidence.  When traversing either the polygon segments or
// the VSB segments, entries and exits must alternate in the
// intersection sequence.  This routine can assume that there are two
// entries and one exit or two exits and one entry, and that the two
// entries or exits are on different VSB segments.

/*   A /\ B                B /\ A
//  --o--o----          ----o--o---  VSB bdy
//   /    \  |          |  /    \
//  /      \ |          | /      \ polygon bdy
//          \|          |/            
//           o C        o C         Polygon bdy is always counterclockwise.
//           |\        /|           VSB bdy can go either direction, so
//           | \      / |           these pictures apply to both R and L turns.
*/

// fi0 and fi1 are both entries or both exits, and are on different segments.
// The one that's different from the other two, entry-wise, is fiB.

std::vector<PixelPlaneIntersectionNR*>
PixelPlaneFacet::tripleCoincidence(PixelPlaneIntersectionNR *fi0,
				   PixelPlaneIntersectionNR *fi1,
				   PixelPlaneIntersectionNR *fiB)
  const
{
  std::vector<PixelPlaneIntersectionNR*> coincidentPoints;
  
  assert(!fi0->onSameLoopSegment(fi1));
  PixelPlaneIntersectionNR *fiA, *fiC;
  const PixelBdyLoopSegment *sharedSeg = fi0->sharedLoopSegment(fiB);
  if(sharedSeg != nullptr) {
    fiA = fi0;
    fiC = fi1;
  }
  else {
    sharedSeg = fi1->sharedLoopSegment(fiB);
    assert(sharedSeg != nullptr);
    fiA = fi1;
    fiC = fi0;
  }
  assert(fiA->crossingType() == fiC->crossingType() &&
	 fiA->crossingType() != fiB->crossingType());

  // If A and C are on the same polygon segment all three points must
  // coincide.
  const FacePlane *faceAC = fiA->sharedFace(fiC, getBaseFacePlane());
  if(faceAC != nullptr) {
    coincidentPoints.push_back(fiA);
    coincidentPoints.push_back(fiB);
    coincidentPoints.push_back(fiC);
    return coincidentPoints;
  }

  // Only "turn" is used here, but classifyVSBcorner expects the rest
  // of the args.
  const PixelPlaneIntersectionNR *entryPt, *exitPt, *firstPt, *secondPt;
  ICoord2D corner;
  TurnDirection turn;
  classifyVSBcorner(fiB, fiC, entryPt, exitPt, firstPt, secondPt, corner, turn
#ifdef DEBUG
		    , verbose
#endif // DEBUG
);

  bool badAB = false;
  bool badBC = false;

  // TODO: Calling sharedFace and getPolyEdge and passing the result
  // to getPolyFrac may be inefficient.  getPolyFrac converts from
  // edge numbers back to face pointers.
  const FacePlane *faceBC = fiB->sharedFace(fiC, getBaseFacePlane());
  unsigned int edgeBC = getPolyEdge(faceBC);
  double polyFracB = fiB->getPolyFrac(edgeBC, this);
  double polyFracC = fiC->getPolyFrac(edgeBC, this);
  
  if(turn == LEFT) {
    if(fiC->crossingType() == ENTRY) {
      /*  Left turn && C is an entry ==>
      //     A precedes B on the VSB, B precedes C on the polygon.
      //       B /\ A
      //    ----o--o--<  
      //    |../....\.
      //    |./......\
      //    |/........    
      //    o C.......
      //   /|......... 
      //  / V
      */
      badAB = fiA->getLoopFrac(*sharedSeg) >= fiB->getLoopFrac(*sharedSeg);
      badBC = polyFracB >= polyFracC;
    } // end if C is an entry
    else {
      /*  Left turn && C is an exit ==>
      //     B precedes A on the VSB, C precedes B on the polygon
      //   A /\ B     
      //  --o--o-<--  
      //  ./... \..|  
      //  /......\.|  
      //  ........\|  
      //  ........ o C
      //  ........ |\
      //           ^ \
      */
      badAB = fiB->getLoopFrac(*sharedSeg) >= fiA->getLoopFrac(*sharedSeg);
      badBC = polyFracC >= polyFracB;
    } // end if C is an exit
  } // end if turn is LEFT
  else {
    // turn is RIGHT
    assert(turn == RIGHT);
    if(fiC->crossingType() == ENTRY) {
      /*  Right turn and C is an entry ==>
      //     A precedes B on the VSB, C precedes B on the polygon
      //  .A./\.B .......
      //  --o--o->--.....
      //   /    \  |.....
      //  /      \ |.....
      //          \|.....
      //           o C...
      //           |\....
      //           V.\...
      */
      badAB = fiA->getLoopFrac(*sharedSeg) >= fiB->getLoopFrac(*sharedSeg);
      badBC = polyFracC >= polyFracB;
    } // end if C is an entry
    else {
      /*  Right turn and C is an exit.
      //     B precedes A on the VSB, B precedes C on the polygon
      //  ...............
      //  .......B./\.A..
      //  ....----o--o-->  
      //  ....|  /    \
      //  ....| /      \
      //  ....|/            
      //  ....o C        
      //  .../|          
      //  ../.^
      */
      badAB = fiB->getLoopFrac(*sharedSeg) >= fiA->getLoopFrac(*sharedSeg);
      badBC = polyFracB >= polyFracC;
    }
  } // end if turn is RIGHT

  if(badAB && badBC) {
    coincidentPoints.reserve(3);
    coincidentPoints.push_back(fiA);
    coincidentPoints.push_back(fiB);
    coincidentPoints.push_back(fiC);
  }
  else if(badAB) {
    coincidentPoints.reserve(2);
    coincidentPoints.push_back(fiA);
    coincidentPoints.push_back(fiB);
  }
  else if(badBC) {
    coincidentPoints.reserve(2);
    coincidentPoints.push_back(fiB);
    coincidentPoints.push_back(fiC);
  }
  return coincidentPoints;
} // end PixelPlaneFacet::tripleCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// PixelPlaneFacet::badTopology for a SimpleIntersection and and
// MultiFaceIntersection.

bool PixelPlaneFacet::badTopology(const SimpleIntersection *si,
				  const MultiFaceIntersection *mfi)
  const
{
  assert(!si->samePixelPlanes(mfi));
  const PixelBdyLoopSegment &siloopseg = si->getLoopSeg();
  const PixelBdyLoopSegment &mfiloopseg = mfi->getLoopSeg();
  const PixelBdyLoopSegment &loopseg0 = (siloopseg.follows(mfiloopseg) ?
					 mfiloopseg : siloopseg);
  const PixelBdyLoopSegment &loopseg1 = (loopseg0 == mfiloopseg ?
					 siloopseg : mfiloopseg);
  TurnDirection turn = turnDirection(loopseg0.firstPt(), loopseg0.secondPt(),
				     loopseg1.secondPt());
  assert(turn == RIGHT || turn == LEFT);
  bool siIsEntry = si->crossingType() == ENTRY;

  if(mfi->crossingType() == NONCROSSING) {
    /* The case where the polygon edges at the MultiFaceIntersection
    // (m) don't cross the voxel set boundary are straightforward.
    //
    //                                 /....   Dots indicate the area that's
    //                         entry  /.....   interior to the polygon and 
    //         --m---->---         --s---->--- the voxel set.
    //         |/ \                |/          
    //   exit  s   \               m           
    //        /|    \              |\          Right VSB turns.
    //       /.|     \             | \         MFI is exterior and
    //      /..|      \	           |  \	       doesn't actually contribute
    //     /...|       \           |   \       to the intersection
    //
    //                                 /    
    //                                / exit 
    //         --m----<---         --m----<--- 
    //         |/.\                |/.......   
    //  entry  s...\               s........   
    //        /|....\              |\.......   Left VSB turns.
    //       / |.....\             | \......   MFI is interior 
    //      /  |......\	           |  \.....   
    //     /   |.......\           |   \....   
    */

    // If the VSB corner turns right, the MultiFaceIntersection must
    // be exterior.
    Interiority interiority = mfi->interiority(this); 
    if((interiority == INTERIOR && turn == RIGHT) ||
       (interiority == EXTERIOR && turn == LEFT))
      {
	return true;
      }
    // Check that the intersections are on the correct segments, which
    // depends on the turn direction *and* whether or not the
    // SimpleIntersection is an entry or an exit.

    // Is the SimpleIntersection on the first or second polygon
    // segment of the MultiFaceIntersection?
    bool siOnFirst = mfi->firstFacePlane(this) == si->getFacePlane();
    
    
    bool ok = ((turn == RIGHT && !(siIsEntry ^ siOnFirst)) ||
	       (turn == LEFT && (siIsEntry ^ siOnFirst)));
    return !ok;
  } // end if mfi doesn't cross the polygon 

  // The polygon edges at the MultiFaceIntersection (m) cross the
  // voxel set boundary.  There are more cases to consider here.  In
  // the diagrams the polygon boundary orientation can be inferred
  // because the polygon is convex.

  /*   \..............._/                   _/.  
  //    \............_/                   _/...  
  //     \...--->--_s-----        --->--_s-----
  //      \..|   _/   exit        |   _/  entry
  //       \.| _/                 | _/           Right turns with the MFI
  //        \|/                   |/             on the first VSB segment
  //  entry  m              exit  m           
  //         |  R00              /|      R01	   
  //         |                  /.|           
  //         |                 /..|
  //
  //
  //     ......\                          _/...       
  //     .......\  exit            entry_/.....   
  //     ....----m-->-----         ----m-->-----
  //     ....|  /                  |  /         
  //     ....| /                   | /          
  //     ....|/                    |/           Right turns with the MFI
  //     ... s  entry              s exit       on the second VSB segment
  //     .../|    R10             /|    R11	     
  //     ../ |                   /.|            
  //     ./  |                  /..|                 
  //
  //  
  //           \                          _/          
  //            \  entry                _/  exit  
  //         ----m--<-----         ----m--<-----
  //         |../                  |  / ......  
  //         |./                   | /........  
  //         |/                    |/.........  Left turns with the MFI
  //   exit  s               entry s..........  on the first VSB segment
  //        /|   L00              /|......L01.     
  //       / |                   / |.....       
  //      /  |                  /  |...              
  //
  //   \               _/                   _/   
  //    \            _/               exit_/     
  //     \   ---<--_s-----        ---<--_s-----
  //      \  |..._/   entry       |   _/......
  //       \ |../                 | _/........   Left turns with the MFI
  //        \|/                   |/..........   on the second VSB segment
  //   exit  m              entry m...........
  //         |   L10             /|.......L11.   
  //         |                  / |.....      
  //         |                 /  |...
  */

  // Consider 6 topological booleans that we can measure easily, and
  // check that the intersections form a legal combination.
  // 
  // A.  VSB turn direction == R
  // B.  Entry before exit and on different segments when traversing VSB
  // C.  Entry before exit and on different segments when traversing polygon
  // D.  MFI before SI when traversing the VSB
  // E.  MFI before SI when traversing the polygon
  // F.  MFI is entry (we already know that MFI and SI are
  //        not both exits or entries)

  static std::set<std::vector<bool>> legalCombos = {
    // A      B      C      D      E      F
    {true,  true,  true,  true,  true,  true},	// R00
    {true,  false, true,  true,  false, false},	// R01
    {true,  true,  true,  false, false, false},	// R10
    {true,  false, true,  false, true,  true},	// R11
    {false, true,  false, true,  false, true},  // L00
    {false, false, false, true,  true,  false}, // L01
    {false, true,  false, false, true,  false}, // L10
    {false, false, false, false, false, true}	// L11
  };
  

  // In theory, not all of these are independent, but round-off error
  // can lead to inconsistencies, which is what we need to detect.
  // TODO: Which of these conditions do we really need to check?


  bool mfiIsEntry = mfi->crossingType() == ENTRY;
  assert(mfiIsEntry ^ siIsEntry);
  // VSB turn direction == R
  bool conditionA = turn == RIGHT;
  // Entry before exit when traversing the VSB
  bool conditionB = ((siIsEntry && loopseg0 == siloopseg) ||
		     (mfiIsEntry && loopseg0 == mfiloopseg));
  // Entry before exit when traversing the polygon
  unsigned int polyseg0, polyseg1;
  mfi->getPolyEdges(this, polyseg0, polyseg1);
  unsigned int sipolyseg = si->getPolyEdge(this);
  bool conditionC = ((siIsEntry && polyseg0 == sipolyseg) ||
		     (mfiIsEntry && polyseg1 == sipolyseg));
  // MFI before SI when traversing the VSB
  bool conditionD = si->getLoopSeg().follows(mfi->getLoopSeg());
  // MFI before SI when traversing the polygon
  bool conditionE = si->getPolyEdge(this) == polyseg1;
  // MFI an entry
  bool conditionF = mfiIsEntry;
  
  std::vector<bool> combo = {conditionA, conditionB, conditionC,
			     conditionD, conditionE, conditionF};

  // Return true if the conditions don't match one of the legal
  // combinations, indicating that something is wrong.
  return legalCombos.find(combo) == legalCombos.end();
} // end PixelPlaneFacet::badTopology(SimpleIntersection, MultiFaceIntersection)

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// PixelPlaneFacet::badTopology for a SimpleIntersection and a
// MultiVSBIntersection.

bool PixelPlaneFacet::badTopology(const SimpleIntersection *si,
				  const MultiVSBIntersection *mvi)
  const
{
  unsigned int siPolySeg = si->getPolyEdge(this);
  unsigned int mviPolySeg = mvi->getPolyEdge(this);
  bool siFirstOnPoly = (siPolySeg + 1) % polygonSize() == mviPolySeg;
  bool mviFirstOnPoly = (mviPolySeg + 1) % polygonSize() == siPolySeg;
  // It's possible that the two polygon segments don't actually join
  // each other:
  bool extraPolySegment = !(mviFirstOnPoly || siFirstOnPoly);


  if(mvi->nVSBSegments() == 2) {
    PixelBdyLoopSegment loopSeg0, loopSeg1;
    TurnDirection turn = mvi->categorizeCorner(loopSeg0, loopSeg1);
  
    if(!extraPolySegment) {
      /* There are twelve geometries.  The voxel set boundaries can go
      // in either direction, so only six diagrams are needed.
      //                                 
      //                                 \
      //         /\               VSB     \
      //        /  \             ----------m    
      //       /    \                      |\ polygon  
      //  ----s------m                     | \
      //     /       |\                    | /    
      //    /        | \                   |/          
      //             |  \                  s           
      //     L0, R0  |   \        L1, R1  /|
      //                                 / | 
      //
      //                  _//                    _//
      //                _/ /                   _/ /
      //              _/  /         VSB       /  / polygon
      //     --------s---m         ----------m  /
      //          _/    /|                _/ | /
      //        _/     / |              _/   |/
      //      _/      /  |            _/     s
      //             /   |                  /|
      //    L2, R2  /    |        L3, R3   / |
      //
      //
      //               /     _/               /
      //              /    _/                /
      //     --------s---m/       ----------m     _/
      //            /  _/|                 /|   _/
      //           / _/  |        L5, R5  / | _/
      //          /_/    |               /  s/
      //                 |              / _/|
      //       L4, R4    |             /_/  |
      */                         

      // We measure five topological booleans:
      //
      // A. SimpleIntersection (s) is an entry
      // B. The SimpleIntersection is on the VSB segment that leaves the
      //    MultiVSBIntersection.    m----s--->---
      // C. The MultiVSBIntersection is first when traversing the polygon
      // D. VSB turns right.
      // E. The polygon corner is on the right side of the VSB segments.

      // (Different edge configurations can have the same sets of values
      // for A-D.  That's ok.)

      static std::set<std::vector<bool>> legalCombos = {
	// A      B      C      D     E
	{false, true,  true,  false, true},  // L0 & L2
	{true,  false, false, false, true},  // L1 & L3
	{true,  false, true,  true,  false}, // R0 & R2
	{false, true,  false, true,  false}, // R1 & R3
	{false, true,  false, false, false}, // L4
	{true,  false, false, true,  true},  // R4
	{true,  false, true,  false, false}, // L5
	{false, true,  true,  true,  true}   // R5
      };
  
      bool conditionA = si->crossingType() == ENTRY;
      bool conditionB = si->getLoopSeg() == loopSeg1;
      bool conditionC = mviFirstOnPoly;
      bool conditionD = turn == RIGHT;

      // index of the polygon corner
      unsigned int polyVertexIndex = mviFirstOnPoly ? siPolySeg : mviPolySeg;
      // position of the polygon corner
      Coord2D polyVertex = polygonCorner(polyVertexIndex);
      bool conditionE = (loopSeg0.onRight(polyVertex) &&
			 loopSeg1.onRight(polyVertex));
    
      std::vector<bool> combo = {conditionA, conditionB, conditionC, conditionD,
				 conditionE};
      return legalCombos.find(combo) == legalCombos.end();
    } // end if !extraPolySegment

    // The polygon edges don't share a polygon corner.  The polygon
    // must be a quadrilateral, and one of its sides must be short,
    // because the SimpleIntersection and MultiVSBIntersection are on
    // opposite edges yet are close to one another.  Conditions A, B,
    // and D still apply.
#ifdef DEBUG
    if(polygonSize() != 4) {
      oofcerr << "PixelPlaneFacet::badTopology:  si=" << *si << std::endl;
      oofcerr << "PixelPlaneFacet::badTopology: mvi=" << *mvi << std::endl;
      throw ErrProgrammingError("Unexpected geometry!", __FILE__, __LINE__);
    }
#endif // DEBUG
    
    static std::set<std::vector<bool>> legalCombos = {
      // A      B      D   
      {false, true,  false},	// L0 & L2
      {true,  false, false},	// L1 & L3
      {true,  false, true },	// R0 & R2
      {false, true,  true },	// R1 & R3
      {false, true,  false},	// L4
      {true,  false, true },	// R4
      {true,  false, false},	// L5
      {false, true,  true }	// R5
    };
      
    bool conditionA = si->crossingType() == ENTRY;
    bool conditionB = si->getLoopSeg() == loopSeg1;
    bool conditionD = turn == RIGHT;
    std::vector<bool> combo = {conditionA, conditionB, conditionD};
    return legalCombos.find(combo) == legalCombos.end();
  } // end if there are two VSB segments at the MultiVSBIntersection.

  // There are 4 VSB segments that meet at the MultiVSBIntersection.

  /*    .............|                  .............|/
  //    .............|                  .............s             
  //    .............|		        ............/|		   
  //    ........./\..|		        .......... /.|		   
  //    ......../..\.|		        ...........\.|		   
  //    ......./....\|		        ............\|		   
  //    -->---s------m----------<--     -->----------m----------<--
  //         /       |\............                  |\............
  //        /        |.\...........                  |.\...........
  //       /         |..\..........                  |..\..........
  //                 |...\.........                  |...\.........
  //                 |....\........                  |....\........
  //
  //                 |.............                  |/............
  //                 |.............                  s.............
  //                 |.............                 /|.............
  //             /\  |.............                / |.............
  //            /  \ |.............                \ |.............
  //           /    \|.............                 \|.............
  //    --<---s------m---------->--     --<----------m---------->--
  //    ...../.......|\                 .............|\
  //    ..../........| \                .............| \
  //    .../.........|  \               .............|  \
  //    ../..........|   \              .............|   \
  //    ./...........|    \             .............|    \
  //
  // In the configurations on the left, the MultiVSBIntersection comes
  // before the SimpleIntersection when traversing the polygon.  It
  // comes after the SimpleIntersection in the configurations on the
  // right.
  */
#ifdef DEBUG
  if(mvi->nVSBSegments() != 4) {
    oofcerr << "PixelPlaneFacet::badTopology: mvi->nVSBSegments()="
	    << mvi->nVSBSegments() << ". Expected 4!" << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology: pixplane=" << *pixplane
	    << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology:  si=" << *si << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology: mvi=" << *mvi << std::endl;
    throw ErrProgrammingError("PixelPlaneFacet::badTopology failed.",
			      __FILE__, __LINE__);
  }
#endif	// DEBUG
  assert(mvi->nVSBSegments() == 4);
  // polyVertex is the next polygon corner after the
  // MultiVSBIntersection.  There might be two corners before reaching
  // the SimpleIntersection.  Only the first is important here.
  unsigned int polyVertexIndex = (mviPolySeg + 1) % polygonSize();
  Coord2D polyVertex = polygonCorner(polyVertexIndex);
  Coord2D mPos = pixplane->convert2Coord2D(mvi->location3D());
  Coord2D sPos = pixplane->convert2Coord2D(si->location3D());
  // The vectors from the MultiVSBIntersection to the polygon corner
  // and to the SimpleIntersection can't be more than 90 degrees
  // from each other.
  if(dot(sPos - mPos, polyVertex - mPos) < 0) {
    return true;
  }
  // The order of the vertices in the triangle formed by the
  // intersections and the polygon corner depends on whether the
  // polygon edge goes from the MultiVSBIntersection to the corner
  // or goes the other way.
  double crs = cross(polyVertex - mPos, sPos - mPos);
  return !((mviFirstOnPoly && crs > 0) || (!mviFirstOnPoly && crs < 0));
} // PixelPlaneFacet::badTopology(SimpleIntersection, MultiVSBIntersection)

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// PixelPlaneFacet::badTopology for a SimpleIntersection and a
// MultiCornerIntersection

/*               |                             |     _//
//               |  /\                         |   _/ /
//               | /  \                        | _/  /
//               |/    \                       |/   /
// --------------m------s------    ------------m---s--------
//               |\      \                   / |  /
//               | \      \                  | | /
//               |  \                        / |/
//               |                          |  o
//               |                          / /|
//                                          |/ |
*/

// The MultiCornerIntersection (m)is already highly constrained, so
// there aren't very many ways that this combination can go wrong.
// The SimpleIntersection (s) must be on a VSB edge that lies between
// the two polygon segments that meet at the MultiCornerIntersection.

// In the second figure, the other SimpleIntersection (o) is assumed
// to be far enough away from m and s so that it's not included in the
// coincidence and/or will be examined later.

bool PixelPlaneFacet::badTopology(const SimpleIntersection *si,
				  const MultiCornerIntersection *mci)
  const
{
  unsigned int siPolySeg = si->getPolyEdge(this);
  const PixelBdyLoopSegment &siLoopSeg = si->getLoopSeg();

  for(const FacePlane *face : mci->facePlaneSets()) {
    if(getPolyEdge(face) == siPolySeg)
      return true;
  }
  // for(FacePlaneSet::const_iterator f=mci->beginFaces(); f!=mci->endFaces(); ++f)
  //   {
  //     if(getPolyEdge(*f) == siPolySeg)
  // 	return true;
  //   }

  // The far end of the VSB loop segment that joins m and s must be on
  // the inside side of both of the FacePlanes that define the polygon
  // segments that meet at m.
  
  Coord2D m = pixplane->convert2Coord2D(mci->location3D());
  ICoord2D farEndLoopSeg = (siLoopSeg.firstPt() == m ?
			    siLoopSeg.secondPt() : siLoopSeg.firstPt());
  return !mci->inside(pixplane->convert2Coord3D(farEndLoopSeg).coord());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// badTopology for a pair of MultiFaceIntersections.

/* VSB right turns, interiority = MIXED | EXTERIOR
//        ..\
//       ....\
//    \...----m--->--          ----m--->--
//     \..|  /                 |  / \
//      \.| /                  | /   \
//       \|/                   |/     \
//        m                    m
//        |                    |\
//        |                    | \
//  C
//  \\
//   \.\_
//    \..\_
//     \...\_
//      \....\_B		  
//       \.----m---->--	      ---->---_m--
//        \|    \     	      |	    _/  \
//       A m_    \	      |	  _/     \
//         | \_   \	      |	 /P       \      P marks a hard to draw
//         |   \_  \	      |	/          \     polygon corner
//         |     \_ \	      |/   
//         |       \_\        m_ 
//                   \\       | \_
//                    D           \_             
//
// VSB left turns, interiority = MIXED | INTERIOR
//	    \
//           \
//        ----m---<--          ----m---<--
//     \  |../                 |  /.\
//      \ |./                  | /...\
//       \|/                   |/.....\
//        m                    m....
//        |                    |\..
//        |                    | \
//
//  D
//  \\_                  
//   \ \_		     
//    \  \_	     
//     \   \_	     
//      \    \_A     
//       \ ----m----<--        ----<---_m--     
//        \|....\      	       |     _/..\
//       B m_....\     	       |   _/.....\
//         | \....\    	       |  /P.......\
//         |   \_..\   	       | /..........\
//         |     \_.\  	       |/........      
//         |       \_\ 	       m_.....	       
//                   \\	       | \_..	       
//		      C	           \_.....      
*/

bool PixelPlaneFacet::badTopology(const MultiFaceIntersection *mfi0,
				  const MultiFaceIntersection *mfi1)
  const
{
  assert(mfi0->nPolySegments() == 2);
  assert(mfi1->nPolySegments() == 2);
  const PixelBdyLoopSegment &loopSeg0 = mfi0->getLoopSeg();
  const PixelBdyLoopSegment &loopSeg1 = mfi1->getLoopSeg();
  if(loopSeg0 == loopSeg1)
    return true;
  bool mfi0FirstOnVSB = loopSeg1.follows(loopSeg0);
#ifdef DEBUG
  bool mfi1FirstOnVSB = loopSeg0.follows(loopSeg1);
  assert(mfi0FirstOnVSB ^ mfi1FirstOnVSB);
#endif	// DEBUG

  unsigned int sharedPolySeg = mfi0->sharedPolySegment(mfi1, this);
  if(sharedPolySeg == NONE) {
    // If the MultiFaceIntersections don't share a polygon segment,
    // they are at opposite corners of a quadrilateral.  In the
    // diagrams above, A is the first intersection on the VSB, and B
    // is the second.  C is the polygon vertex to the left of the VSB
    // and D is to the right.  If the triangles CAB and BAD have
    // negative area, then the points A and B are misordered.
    // Get the tet points that aren't the MultiFaceIntersections.

    // eindex0 and eindex1 are the indices of the polygon edges for
    // these planes.  We don't know which order they're in yet.
    unsigned int eindex0 = NONE;
    unsigned int eindex1 = NONE;
    for(const FacePlane *face :
	  (mfi0FirstOnVSB ? mfi0->facePlaneSets() : mfi1->facePlaneSets()))
      {
	if(eindex0 == NONE)
	  eindex0 = getPolyEdge(face);
	else
	  eindex1 = getPolyEdge(face);
      }
    
    // Figure out which edge comes first.  Remember that the index of
    // an edge is the index of the corner at the beginning of the
    // edge.
    unsigned int indexC = (eindex1==eindex0+1 || (eindex0==3 && eindex1==0) ?
			   eindex0 : eindex1);
    unsigned int indexA = (indexC + 1) % 4;
    unsigned int indexD = (indexA + 1) % 4;
    unsigned int indexB = (indexD + 1) % 4;
    
    Coord2D posA = pixplane->convert2Coord2D(tetPts[indexA]->location3D());
    Coord2D posB = pixplane->convert2Coord2D(tetPts[indexB]->location3D());
    Coord2D posC = pixplane->convert2Coord2D(tetPts[indexC]->location3D());
    Coord2D posD = pixplane->convert2Coord2D(tetPts[indexD]->location3D());
    // Don't use the triangleArea() function in geometry.C.  That
    // always returns a positive number.
    bool posCAB = ((posA-posC) % (posB-posC)) > 0;
    bool posBAD = ((posB-posD) % (posA-posD)) > 0;
    // symmetric form is posA%posC + posC%posB + posB%posA > 0 which
    // will be slower to compute but might be more robust.
    return !posCAB || !posBAD;
  } // end if the two MultiFaceIntersections don't share a polygon edge

  // The intersections are on the same polygon edge.
  if(mfi0FirstOnVSB)
    return badTopology_(mfi0, mfi1, sharedPolySeg);
  return badTopology_(mfi1, mfi0, sharedPolySeg);
}

// This version knows that the MultiFaceIntersections are given in the
// order in which they appear on the VSB, that they are on different
// (but connected) VSB segments, and that they share a polygon
// segment.  Because they're both MultiFaceIntersections, they must be
// at either end of the polygon segment.

bool PixelPlaneFacet::badTopology_(const MultiFaceIntersection *mfi0,
				   const MultiFaceIntersection *mfi1,
				   unsigned int polySeg)
  const
{
  const PixelBdyLoopSegment &loopSeg0 = mfi0->getLoopSeg();
  const PixelBdyLoopSegment &loopSeg1 = mfi1->getLoopSeg();
  TurnDirection turn = turnDirection(loopSeg0.firstPt(), loopSeg0.secondPt(),
				     loopSeg1.secondPt());
  if(turn != LEFT && turn != RIGHT)
    return true;
  Interiority interiority0 = mfi0->interiority(this);
  Interiority interiority1 = mfi1->interiority(this);
  if(interiority0 != interiority1)
    return true;
  
  // Is the order of the MultiFaceIntersections on the VSB the same as
  // it is on the polygon?
  unsigned int otherPolySeg0 = mfi0->getOtherFaceIndex(polySeg, this);
  // If otherPolySeg0+1 == polySeg, then otherPolySeg0 comes first, so
  // polySeg is the second polygon segment at mfi0, and mfi0 comes
  // before mfi1.  That means that the order on the polygon is the
  // same as the order on the VSB.
  bool sameDirection = (otherPolySeg0 + 1)%polygonSize() == polySeg;

  // Looking at the diagrams above...
  return !((turn == RIGHT && ((interiority0 == INTERIOR && !sameDirection) ||
			      (interiority0 == MIXED && sameDirection)))
	   ||
	   (turn == LEFT && ((interiority0==EXTERIOR && sameDirection) ||
			     (interiority0==MIXED && !sameDirection))));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Topology constraints for a MultiFaceIntersection and a
// MultiVSBIntersection

/*
//     \                      \      \
//      \ 		       \      \
//       o------------	        o------o-----	
//       |\		        |\    /		
//       | \		        | \  /		
//       |  \		        |  \/		
//       |  /		        |   		
//     \ | /	(I)	        |  	(II)	
//      \|/		        | 		
//       o		        |		
//       |                      |
//
// 
//          /\	                  /            
//         /  \	                 /			
//        o----o-------         o------------		
//       /|   /  	       /| 			
//      / |  /    	      / |  		
//     /  |    	             /  |   			
//        |   		     \  |   		
//        |  		      \ |  		
//        |   (III)	       \|/	 (IV)	
//        |		        o		
//        |		        |              
*/

bool PixelPlaneFacet::badTopology(const MultiFaceIntersection *mfi,
				  const MultiVSBIntersection *mvi)
  const
{
  // The planes at the MultiFaceIntersection must always cross a VSB
  // segment.
  if(mfi->interiority(this) != MIXED)
    return true;

  // Neither of the tet faces that meet at the MultiFaceIntersection
  // can be the face at the VSB.
  for(const FacePlane *face : mfi->facePlaneSets()) {
    if(face == mvi->getFacePlane())
      return true;
  }
  // for(auto fp=mfi->beginFaces(); fp!=mfi->endFaces(); ++fp)
  //   if(*fp == mvi->getFacePlane())
  //     return true;
  
  PixelBdyLoopSegment loopSeg0, loopSeg1;
  TurnDirection turn = mvi->categorizeCorner(loopSeg0, loopSeg1);
  // Does the MultiFaceIntersection precede the MultiVSBIntersection
  // on the VSB?
  bool mfiFirst = mfi->getLoopSeg() == loopSeg0;
  CrossingType mviCrossing = mvi->crossingType();
  CrossingType mfiCrossing = mfi->crossingType();
  if(turn == RIGHT) {
    if(mfiFirst) {		// Configurations I and IV
      return !(mfiCrossing == ENTRY && mviCrossing != ENTRY);
    }
    else {			// !mfiFirst, Configurations II & III
      return !(mfiCrossing == EXIT && mviCrossing != EXIT);
    }
  }
  // turn == LEFT
  if(mfiFirst) {		// Configurations II & III
    return !(mfiCrossing == ENTRY && mviCrossing != ENTRY);
  }
  // Configurations I && IV
  return !(mfiCrossing == EXIT && mviCrossing != EXIT);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Topology contraints for a MultiFaceIntersection and a
// MultiCornerIntersection.

/*                          /\
//                         /  \
//     o-----------       o----o--------
//    /|\                 |\  /
//   / | \                | \/
//  /  |  \               |
//  \  |  /   (I)         |     (II)
//   \ | /                |
//    \|/                 |
//     o
//     |  
*/

bool PixelPlaneFacet::badTopology(const MultiFaceIntersection *mfi,
				  const MultiCornerIntersection *mci)
  const
{
  // The MultiFaceIntersection and the MultiCornerIntersection don't
  // share any polygon edges.
  if(mfi->onSameFacePlane(mci, getBaseFacePlane()))
    return true;
  PixelBdyLoopSegment loopSeg0, loopSeg1;
  TurnDirection turn = mci->categorizeCorner(loopSeg0, loopSeg1);
  bool mfiFirst = mfi->getLoopSeg() == loopSeg0;
  if((mfiFirst && turn == RIGHT)     // Configuration I
     || (!mfiFirst && turn == LEFT)) // Configuration II
    {
      return !(mfi->crossingType() == ENTRY && mci->crossingType() == EXIT);
    }
  assert((mfiFirst && turn == LEFT)	   // Configuration I
	 || (!mfiFirst && turn == RIGHT)); // Configuration II
  return !(mfi->crossingType() == EXIT && mci->crossingType() == ENTRY);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// This used to be declared as a template that could use any kind of
// SingleFaceMixIn, but then the SingleFaceMixIn template would have
// to be exposed within planeintersection_i.h

bool PixelPlaneFacet::onOppositeEdges(const SimpleIntersection *fi0,
				      const SimpleIntersection *fi1)
  const
{
  return (polygonSize() == 4 &&
	  (fi0->getPolyEdge(this) + 2) % 4 == fi1->getPolyEdge(this));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const PixelPlaneFacet &facet) {
  os << "PixelPlaneFacet(pixplane=" << *facet.pixplane;
  if(!facet.edges.empty()) {
    os << "," << std::endl
       << "                edges=" << std::endl;
    for(const FacetEdge *edge : facet.edges)
      os << "                   " << *edge << std::endl;
  }
  os << ")";
  return os;
}

std::ostream &operator<<(std::ostream &os, const FacetEdge &edge) {
  os << "FacetEdge(" << *edge.startPt() << ", " << *edge.endPt();
  if(edge.nullified())
    os << ", nullified";
  os << ", length=" << sqrt(edge.length2()) << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void PixelPlaneFacet::dump() const {
  for(const FacetEdge *edge : edges) {
    std::cerr << edge->startPos3D() << ", " << edge->endPos3D() << std::endl;
  }
}
