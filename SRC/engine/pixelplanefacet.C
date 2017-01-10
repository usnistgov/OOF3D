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
#include "engine/facefacet.h"
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
  return "f" + to_string(face_);
}

std::string FacePixelPlane::shortName() const {
  return "F" + to_string(face());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the plane perpendicular to this plane that contains the
// segment (pt0, pt1) in this plane.  The new plane's normal points to
// the right when traversing the segment from pt0 to pt1 in this plane.

HPixelPlane *HPixelPlane::orthogonalPlane(const ICoord2D &pt0,
					  const ICoord2D &pt1)
  const
{
  // t is the direction along the segment, in this plane's coordinates.
  unsigned int t = (pt0[0] == pt1[0] ? 1 : 0);
  unsigned int n = (t == 0 ? 1 : 0);
  assert(pt0[t] != pt1[t] && pt0[n] == pt1[n]);
  int offst = pt0[n];
  unsigned int dir = proj_dirs[proj_index][n];
  int norm = (pt0[t] < pt1[t] ? -1 : 1);
  if(t == 1) norm *= -1;
  return new HPixelPlane(dir, offst, norm);
}

HPixelPlane *HPixelPlane::flipped() const {
  return new HPixelPlane(direction(), normalOffset(), -normalSign());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool HPixelPlane::isPartOf(const PixelPlaneIntersectionNR *fi) const {
  return fi->pixelPlanes().count(this) > 0;
}

void HPixelPlane::addToIntersection(IntersectionPlanesBase *fi) const {
  fi->pixelPlanes().insert(this);
}

bool HPixelPlane::isInEquivalence(const IsecEquivalenceClass *eqclass) const {
  return eqclass->containsPixelPlane(this);
  // return eqclass->pixelPlanes.count(unoriented_) > 0;
}

void HPixelPlane::addToEquivalence(IsecEquivalenceClass *eqclass) const {
  eqclass->addPixelPlane(this, true);
}

void HPixelPlane::addCollinearToEquivalence(IsecEquivalenceClass *eqclass)
  const
{
  eqclass->addPixelPlane(this, false);
}

bool FacePlane::isPartOf(const PixelPlaneIntersectionNR *fi) const {
  return fi->faces().count(this) > 0;
}

void FacePlane::addToIntersection(IntersectionPlanesBase *fi) const {
  fi->faces().insert(this);
}

bool FacePlane::isInEquivalence(const IsecEquivalenceClass *eqclass) const {
  return eqclass->facePlanes.count(this) > 0;
}

void FacePlane::addToEquivalence(IsecEquivalenceClass *eqclass) const {
  eqclass->addFacePlane(this, true);
}

void FacePlane::addCollinearToEquivalence(IsecEquivalenceClass *eqclass) const {
  eqclass->addFacePlane(this, false);
}

bool FacePixelPlane::isPartOf(const PixelPlaneIntersectionNR *fi) const {
  return fi->pixelFaces().count(this) > 0;
}

void FacePixelPlane::addToIntersection(IntersectionPlanesBase *fi) const {
  fi->pixelFaces().insert(this);
}

void FacePixelPlane::addToEquivalence(IsecEquivalenceClass *eqclass) const {
  eqclass->addFacePixelPlane(this, true);
}

void FacePixelPlane::addCollinearToEquivalence(IsecEquivalenceClass *eqclass)
  const
{
  eqclass->addFacePixelPlane(this, false);
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
//       oofcerr << "LtPolyFrac::operator(): fi0= " << fi0 << " " << *fi0
// 	      << std::endl;
//       oofcerr << "LtPolyFrac::operator(): fi1= " << fi1 << " " << *fi1
// 	      << std::endl;      
//     }
// #endif // DEBUG

    // TODO: sharedPolySegment might be too slow in this context.
    unsigned int sharedSeg = fi0->sharedPolySegment(fi1, facet);
// #ifdef DEBUG
//     if(facet->verbose)
//       oofcerr << "LtPolyFrac::operator(): sharedSeg=" << sharedSeg << std::endl;
// #endif // DEBUG
    if(sharedSeg != NONE) {
      EdgePosition t0 = fi0->getPolyFrac(sharedSeg, facet);
      EdgePosition t1 = fi1->getPolyFrac(sharedSeg, facet);
// #ifdef DEBUG
//       if(facet->verbose) {
// 	oofcerr << "LtPolyFrac::operator(): polyFrac0=" << t0 << std::endl;
// 	oofcerr << "LtPolyFrac::operator(): polyFrac1=" << t1 << std::endl;
// 	oofcerr << "LtPolyFrac::operator():     t1-t0=" << t1-t0 << std::endl;
//       }
// #endif // DEBUG

      return t0 < t1;

      // return (fi0->getPolyFrac(sharedSeg, facet) <
      // 	      fi1->getPolyFrac(sharedSeg, facet));
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

// FacetEdge::FacetEdge(const FacetEdge &fe)
//   : start_(fe.start_->clone()),
//     stop_(fe.stop_->clone())
// {
//   start_->setEdge(this);
//   stop_->setEdge(this);
// }

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
				 unsigned int onFace
#ifdef DEBUG
				 , bool verbose
#endif // DEBUG

				 )
  : tetPts(tetPts),
    areaComputed_(false),
    edgeFaceMap(tetPts.size(), NONE),
    closedOnPerimeter(false),
    onFace(onFace),
    htet(htet),
    pixplane(pixplane)
#ifdef DEBUG
  , verbose(verbose)
#endif // DEBUG
{
  // Map FacePlanes and FacePixelPlanes to polygon edge numbers.  Edge
  // i goes from tetPts[i] to tetPts[i+1].
  for(unsigned int i=0; i<tetPts.size(); i++) {
    FacePlaneSet faces = getFacePlanes(i);
    for(const FacePlane *face : faces) {
      assert(face != nullptr);
      faceEdgeMap[face] = i;
      // If this facet is on a tet face, then when
      // HomogeneityTet::edgeCoord is used to compute relative
      // positions along polygon edges, it's really doing it along tet
      // edges, and needs to know the relationship between polygon
      // edge indices and tet face edge indices.
      // TODO: edgeFaceMap is only used here and in edgeCoord().
      // Should there be a subclass of PixelPlaneFacet for facets on
      // tet faces?
      if(onFace != NONE) {
	unsigned int faceno = htet->getTetFaceIndex(face);
	if(faceno != onFace) {
	  // edgeFaceMap[i] is the index of the edge at face scope,
	  // for the face that coincides with this facet.
	  unsigned int tetedge = CSkeletonElement::faceFaceEdge[faceno][onFace];
	  edgeFaceMap[i] = CSkeletonElement::tetEdge2FaceEdge[onFace][tetedge];
	}
      }
      boundingFaces.insert(face);
      const FacePixelPlane *fpp = htet->getCoincidentPixelPlane(face);
      if(fpp != nullptr)
	faceEdgeMap[fpp] = i;
    }
  }
// #ifdef DEBUG
//   if(verbose) {
//     for(auto i=faceEdgeMap.begin(); i!=faceEdgeMap.end(); ++i)
//       oofcerr << "PixelPlaneFacet::ctor: faceEdgeMap[" << *i->first << "] = "
// 	      << i->second << std::endl;
//   }
// #endif // DEBUG
}

PixelPlaneFacet::~PixelPlaneFacet() {
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::dtor" << std::endl;
// #endif // DEBUG
  for(FacetEdge *edge : edges)
    delete edge;
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::dtor" << std::endl;
// #endif // DEBUG
}

// Find the tet faces that this edge lies on, excluding the face that
// lies in the pixel plane (if any).  These are the faces that define
// the edges of the tet-pixel plane intersection polygon.

// TODO: getFacePlanes is expensive. It's called from the
// PixelPlaneFacet constructor and also in
// MultiFaceMixin::getPolyFrac.  Its return values should be cached.

FacePlaneSet PixelPlaneFacet::getFacePlanes(unsigned int f) const {
  assert(f != NONE);
  unsigned int g = f + 1;
  if(g == tetPts.size())
    g = 0;
  auto faces = tetPts[f]->sharedFaces(tetPts[g], getBaseFacePlane());

// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::getFacePlanes: f=" << f << std::endl;
//   OOFcerrIndent indent(2);
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::getFacePlanes: tetPts[f=" << f << "]="
// 	    << *tetPts[f] << std::endl;
//     oofcerr << "PixelPlaneFacet::getFacePlanes: tetPts[g=" << g << "]="
// 	    << *tetPts[g] << std::endl;
//     oofcerr << "PixelPlaneFacet::getFacePlanes: faces=";
//     std::cerr << derefprint(faces);
//     oofcerr << std::endl;	
//   }
// #endif // DEBUG

  // For each face in faces, include the faces collinear with it and
  // the pixelplane.
  const HPixelPlane *upixplane = htet->getUnorientedPixelPlane(pixplane);
  FacePlaneSet morefaces;
  for(const FacePlane *face : faces) {
    FacePlaneSet cofaces = htet->getCollinearFaces(face, upixplane);
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "PixelPlaneFacet::getFacePlanes: cofaces(" << *face << ")=";
//       std::cerr << derefprint(cofaces);
//       oofcerr << std::endl;
//     }
// #endif // DEBUG
    morefaces.insert(cofaces.begin(), cofaces.end());
  }
  faces.insert(morefaces.begin(), morefaces.end());

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::getFacePlane: after adding collinear, faces=";
//     std::cerr << derefprint(faces);
//     oofcerr << std::endl;	
//   }
// #endif // DEBUG

  for(auto i=faces.begin(); i!=faces.end(); ++i) {
    // Use Plane::coincident instead of operator== here because the
    // planes stored in the tetPts have arbitrary orientations.
    if((*i)->coincident(*pixplane)) {
      faces.erase(i);
      break;			// there can be only one coincident face
    }
  }
#ifdef DEBUG
  if(faces.empty())
    throw ErrProgrammingError("getFacePlanes failed!", __FILE__, __LINE__);
#endif // DEBUG
  return faces;
  
//   for(const FacePlane *face : faces) {
//     if(!face->coincident(*pixplane)) {
// // #ifdef DEBUG
// //       if(verbose) {
// // 	oofcerr << "PixelPlaneFacet::getFacePlane: face=" << *face
// // 		<< std::endl;
// //       }
// // #endif	// DEBUG
//       return face;
//     }
//   }
  // throw ErrProgrammingError("getFacePlane failed!", __FILE__, __LINE__);
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
//     oofcerr << "PixelPlaneFacet::addEdges: fi0=" << fi0 << " " << *fi0
// 	    << std::endl;
//     oofcerr << "PixelPlaneFacet::addEdges: fi1=" << fi1 << " " << *fi1
// 	    << std::endl;
//   }
//   OOFcerrIndent indent(2);
// #endif // DEBUG

  // See comment in PixelPlaneIntersectionNR::locateOnPolygonEdge.
  // It's important that that routine and this use the same method for
  // finding edge numbers.
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
      addEdge(new PolygonEdge(fi0->clone(htet), fi1->clone(htet)));
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
    addEdge(new PolygonEdge(fi0->clone(htet),
			    tetPts[(startSeg+1)%nn]->clone(htet)));
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
      addEdge(new PolygonEdge(tetPts[seg]->clone(htet),
			      tetPts[nextseg]->clone(htet)));
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
    addEdge(new PolygonEdge(tetPts[endSeg]->clone(htet), fi1->clone(htet)));
  }
  closedOnPerimeter = true;
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::addEdges: done" << std::endl;
// #endif // DEBUG
} // PixelPlaneFacet::addEdges

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
  
  // Don't include edges that join equivalent points, or pairs of
  // oppositely directed edges with equivalent endpoints.  If these
  // are the only edges in a facet, round-off error can make the area
  // appear to be non-zero when it should be zero.
  std::vector<bool> includeEdge(edges.size(), true);
  for(unsigned int i=0; i<edges.size(); i++) {
    if(edges[i]->startPt()->isEquivalent(edges[i]->endPt()))
      includeEdge[i] = false;
    if(includeEdge[i]) {
      for(unsigned int j=i+1; j<edges.size(); j++) {
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
  // Negative areas at this point indicate that the edges detected so
  // far are the edges of a "hole" in the middle of the facet, and the
  // entire perimeter of the tet polygon has to be included.  However,
  // if edges have already been added along the perimeter by addEdges,
  // then parts of the polygon perimeter have been included, and the
  // computed area *must* be positive already.  If it's not, it's
  // because of round off error, and it should really be zero.
  if(closedOnPerimeter && a < 0.0) {
// #ifdef DEBUG
//     oofcerr << "PixelPlaneFacet::getArea: ignoring negative area: " << a
// 	    << std::endl;
// #endif // DEBUG
    a = 0.0;
  }
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::getArea: " << *pixplane << " a=" << 0.5*a
// 	    << std::endl;
//   }
// #endif // DEBUG
  return 0.5*a;
} // PixelPlaneFacet::getArea

BarycentricCoord PixelPlaneFacet::polygonCornerBary(unsigned int i) const {
#ifdef DEBUG
  if(i >= tetPts.size()) {
    oofcerr << "PixelPlaneFacet::polygonCornerBary: i=" << i << std::endl;
    throw ErrProgrammingError("Error in polygonCornerBary", __FILE__, __LINE__);
  }
#endif // DEBUG
  return tetPts[i]->baryCoord(htet);
}

Coord2D PixelPlaneFacet::polygonCorner(unsigned int i) const {
  return pixplane->convert2Coord2D(tetPts[i]->location3D());
}

// Find the distance from pt0 to pt1 going around the perimeter of the
// tet intersection polygon, given the positions of the points and
// which polygon edges they're on.

double PixelPlaneFacet::polygonPerimeterDistance(
					 const PixelPlaneIntersectionNR *pt0,
					 const PixelPlaneIntersectionNR *pt1)
  const
{
  unsigned int edge0 = pt0->getPolyEdge(this);
  unsigned int edge1 = pt1->getPolyEdge(this);
  EdgePosition frac0 = pt0->getPolyFrac(edge0, this);
  EdgePosition frac1 = pt1->getPolyFrac(edge1, this);
  if(edge0 == edge1) {
    double d = sqrt(norm2(pt1->location2D(pixplane) -
			  pt0->location2D(pixplane)));
    if(frac1 >= frac0) {
      return d;
    }
    // pt0 occurs after pt1 on the polygon edge.  Go all the way
    // around the polygon.
    double totalPerim = 0;
    for(unsigned int i=0; i<tetPts.size(); i++) {
      unsigned int j = i+1;
      if(j == tetPts.size()) j = 0;
      // TODO: Cache polygon edge lengths in PixelPlaneFacet?
      totalPerim += sqrt(norm2(tetPts[i]->location2D(pixplane) -
			       tetPts[j]->location2D(pixplane)));
    }
    return totalPerim - d;
  }
  // The points aren't on the same polygon edge.
  unsigned int np = tetPts.size();
  // Distance from pt0 to the end of its polygon segment.
  double d = sqrt(norm2(tetPts[(edge0+1)%np]->location2D(pixplane) -
			pt0->location2D(pixplane)));
  // Distance to pt1 from the beginning of its polygon segment.
  d += sqrt(norm2(pt1->location2D(pixplane) -
		  tetPts[edge1]->location2D(pixplane)));
  // Add the lengths of any intermediate edges.
  unsigned int e = (edge0 + 1) % np;
  while(e != edge1) {
    unsigned int enext = (e + 1) % np;
    d += sqrt(norm2(tetPts[enext]->location2D(pixplane) -
		    tetPts[e]->location2D(pixplane)));
    e = enext;
  }
  return d;
}
						 

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utilities used by PixelPlaneFacet::completeLoops

static void storeCoincidenceData(PixelPlaneIntersectionNR *isec,
				 const HPixelPlane *pixplane,
				 std::set<Coord2D> &coincidentLocs,
				 IsecsNearCoord &coincidences)
{
  Coord2D loc = pixplane->convert2Coord2D(isec->location3D());
  for(Coord2D p : coincidentLocs) {
    if(norm2(loc-p) < CLOSEBY2) {
      coincidences.insert(IsecsNearCoord::value_type(p, isec));
      return;
    }
  }
  coincidences.insert(IsecsNearCoord::value_type(loc, isec));
  coincidentLocs.insert(loc);
  return;
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

static void incrementIsec(
		  unsigned int &edgeNo, unsigned int &isecNo,
		  std::vector<PolyEdgeIntersections> &polyEdgeIntersections)
{
  isecNo++;
  if(isecNo >= polyEdgeIntersections[edgeNo].size()) {
    isecNo = 0;
    do {
      edgeNo++;
      if(edgeNo == polyEdgeIntersections.size())
	edgeNo = 0;
    } while(polyEdgeIntersections[edgeNo].empty());
  }
}

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
  
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::completeLoops: initial facet=" << *this
// 	    << std::endl;
//   }
// #endif // DEBUG

  std::set<Coord2D> coincidentLocs; // locations where coincidences occur
  IsecsNearCoord coincidences; // All intersections at a point
  unsigned int totalIntersections = 0;

  for(FacetEdge *edge : edges) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::completeLoops: edge=" << edge
// 	      << " " << *edge << std::endl;
// #endif	// DEBUG

    if(edge->startFace()) {
      // Calling referent() is sort of silly here, but it's possibly
      // cheaper than using a dynamic_cast to convert the
      // PixelPlaneIntersection in the FacetEdge to a
      // PixelPlaneIntersectionNR.  At this point the intersection
      // can't be a RedundantIntersection.
      PixelPlaneIntersectionNR *ppi = edge->startFace()->referent();
      // htet->checkEquiv(ppi);
      storeCoincidenceData(ppi, pixplane, coincidentLocs, coincidences);
      totalIntersections++;
    }
    if(edge->stopFace()) {
      PixelPlaneIntersectionNR *ppi = edge->stopFace()->referent();
      // htet->checkEquiv(ppi);
      storeCoincidenceData(ppi, pixplane, coincidentLocs, coincidences);
      totalIntersections++;
    }
    
  } // end loop over edges

#ifdef DEBUG
  if(verbose) {
    // oofcerr << "PixelPlaneFacet::completeLoops: after checkEquiv, facet="
    // 	    << *this << std::endl;
    // // oofcerr << "PixelPlaneFacet::completeLoops: after checkEquiv, eq classes="
    // // 	    << std::endl;
    // // OOFcerrIndent indent(2);
    // // htet->dumpEquivalences();
    // oofcerr << "PixelPlaneFacet::completeLoops: coincidences=" << std::endl;
    // OOFcerrIndent indent(2);
    // for(Coord2D pt : coincidentLocs) {
    //   auto range = coincidences.equal_range(pt);
    //   for(auto c=range.first; c!=range.second; ++c) {
    // 	oofcerr << "PixelPlaneFacet::completeLoops: " << c->first << ": "
    // 		<< *c->second << std::endl;
    //   }
    // }
  }

  // if(!htet->verify()) {
  //   oofcerr << "PixelPlaneFacet::completeLoops: verify failed after edge loop"
  // 	    << std::endl;
  //   throw ErrProgrammingError("Verification failed after edge loop",
  // 			      __FILE__, __LINE__);
  //   }
#endif	// DEBUG

  // Resolve coincidences that occur when a voxel corner is on or near
  // a tet face.  In that case roundoff error can put points in the
  // wrong order on an edge.

  for(Coord2D loc : coincidentLocs) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::completeLoops: looking for coincidence at "
// 	      << loc << " " << pixplane->convert2Coord3D(loc) << std::endl;
// #endif // DEBUG
    if(coincidences.count(loc) > 1) {
      auto range = coincidences.equal_range(loc);
// #ifdef DEBUG
//       if(verbose) {
// 	oofcerr << "PixelPlaneFacet::completeLoops: resolving coincidence at "
// 		<< loc << " " << pixplane->convert2Coord3D(loc) << std::endl;
// 	oofcerr << "PixelPlaneFacet::completeLoops: coincident points are:"
// 		<< std::endl;
// 	for(auto r=range.first; r!=range.second; ++r) {
// 	  OOFcerrIndent indent(4);
// 	  oofcerr << "PixelPlaneFacet::completeLoops: "
// 		  << *dynamic_cast<PixelPlaneIntersectionNR*>((*r).second)
// 		  << std::endl;
// 	}
//       }
//       OOFcerrIndent indent(2);
// #endif // DEBUG
      // First, copy the intersections at this location into a set,
      // and merge ones that are at *identical* positions.
      PPIntersectionNRSet uniqueIsecs;
      for(auto pp =range.first; pp!=range.second; ++pp) {
	PixelPlaneIntersectionNR *p = (*pp).second;
	bool replaced = false;
	for(PixelPlaneIntersectionNR *q : uniqueIsecs) {
	  if(q->isEquivalent(p)) {
// #ifdef DEBUG
// 	    if(verbose) {
// 	      oofcerr << "PixelPlaneFacet::completeLoops: merging identical pts"
// 		      << std::endl;
// 	    }
// #endif // DEBUG
	    PixelPlaneIntersectionNR *merged = q->mergeWith(htet, p, this);
	    if(merged) {
// #ifdef DEBUG
// 	      if(verbose) {
// 		oofcerr << "PixelPlaneFacet::completeLoops: merged "
// 			<< *q << " and " << *p << std::endl;
// 		oofcerr << "PixelPlaneFacet::completeLoops: result="
// 			<< *merged << std::endl;
// 	      }
// #endif // DEBUG
	      uniqueIsecs.erase(q);
	      // replaceIntersection deletes p and q.
	      replaceIntersection(q, merged);
	      replaceIntersection(p, new RedundantIntersection(merged, this));
	      uniqueIsecs.insert(merged);
	      replaced = true;
	      break;		// break from loop over uniqueIsecs
	    }
	  }
	} // end loop over uniqueIsecs q
	if(!replaced) {
	  uniqueIsecs.insert(p);
	}
      }	// end loop over intersections p at this coincidence location

// #ifdef DEBUG
//       if(verbose) {
// 	oofcerr << "PixelPlaneFacet::completeLoops: uniqueIsecs=" << std::endl;
// 	OOFcerrIndent indent(2);
// 	for(PixelPlaneIntersectionNR *isec : uniqueIsecs)
// 	  oofcerr << "PixelPlaneFacet::completeLoops: " << *isec << std::endl;
//       }
// #endif // DEBUG

      // From the set of intersections, choose the ones that are
      // actually crossings.  These are the points where segments
      // along the polygon perimeter can start or end.  NOTE: It's not
      // possible to combine this loop with the previous step, since
      // when three or more points are merged, the apparent crossing
      // type can change from crossing to non-crossing and back again.

      // The previous merge can create intersections with
      // crossingCount > 1 or < -1, which indicates that some further
      // merging is required.
      PPIntersectionNRSet uniqueCrossings;
      for(PixelPlaneIntersectionNR *p : uniqueIsecs)
	if(p->crossingType() != NONCROSSING)
	  uniqueCrossings.insert(p);
     
      int nIntersections = uniqueCrossings.size();
#ifdef DEBUG
      if(verbose) {
	oofcerr << "PixelPlaneFacet::completeLoops: resolving "
		<< nIntersections << "-fold coincidence at " << loc
		<< std::endl;
      }
#endif // DEBUG
      if(nIntersections == 2) {
	if(!resolveTwoFoldCoincidence(uniqueCrossings)) {
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "PixelPlaneFacet::completeLoops: "
		    << "resolveTwoFoldCoincidence failed at " << loc
		    << std::endl;
	  }
#endif // DEBUG
	  return false;
	}
      }
      else if(nIntersections == 3) {
	if(!resolveThreeFoldCoincidence(uniqueCrossings)) {
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "PixelPlaneFacet::completeLoops: "
		    << "resolveThreeFoldCoincidence failed at " << loc
		    << std::endl;
	  }
#endif // DEBUG
	  return false;
	}
      }
      else if(nIntersections > 3) {
	if(!resolveMultipleCoincidence(uniqueCrossings, totalIntersections)) {
#ifdef DEBUG
	  if(verbose) {
	    oofcerr << "PixelPlaneFacet::completeLoops: "
		    << "resolveMultipleCoincidence failed at " << loc
		    << std::endl;
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
  // if(verbose) {
  //   oofcerr << "PixelPlaneFacet::completeLoops: after resolving coincidences,"
  // 	    << " facet=" << *this << std::endl;
  // }
  // if(!htet->verify()) {
  //   throw ErrProgrammingError("Verification failed", __FILE__, __LINE__);
  // }
#endif	// DEBUG

  // TODO: Should removeNullEdges be used?
//   // Remove edges that join equivalent intersection points.
//   removeNullEdges();

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::completeLoops: after removing null edges,"
// 	    << " facet=" << *this << std::endl;
//   }
//   if(!htet->verify()) {
//     throw ErrProgrammingError("Verification failed", __FILE__, __LINE__);
//   }
// #endif	// DEBUG

  // Construct the lists of intersections on each edge, now including
  // only the topologically distinct intersections
  // (RedundantIntersection::locateOnPolygonEdge() is a no-op).

  // PolyEdgeIntersections is vector of PixelPlaneIntersection*s.
  std::vector<PolyEdgeIntersections> polyEdgeIntersections(tetPts.size());

// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::completeLoops: beginning locateOnPolygonEdge loop" << std::endl;
// #endif // DEBUG

  for(FacetEdge *edge : edges) {
// #ifdef DEBUG
//     try {
// #endif // DEBUG
    edge->startPt()->locateOnPolygonEdge(polyEdgeIntersections, this);
    edge->endPt()->locateOnPolygonEdge(polyEdgeIntersections, this);
// #ifdef DEBUG
//     }
//     catch (...) {
//       oofcerr << "PixelPlaneFacet::completeLoops: edge=" << *edge << std::endl;
//       oofcerr << "PixelPlaneFacet::completeLoops: pixplane=" << *pixplane
// 	      << std::endl;
//       throw;
//     }
// #endif // DEBUG
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
// 	  EdgePosition t = fib->getPolyFrac(e, this);
// 	  oofcerr << "PixelPlaneFacet::completeLoops:   " << *fib
// 		  << " t=" << t << std::endl;
// 	}
//       }
//     }
//   }
// #endif // DEBUG

  // Sort the polyEdgeIntersections by polyFrac (position along the
  // edge).  TODO: This is inefficient, since LtPolyFrac computes the
  // shared polygon edge for each pair of points that it compares.  In
  // this case we already know the polygon edge.
#ifdef DEBUG
  if(verbose)
    oofcerr << "PixelPlaneFacet::completeLoops: sorting" << std::endl;
#endif  // DEBUG
  for(PolyEdgeIntersections &polyedge : polyEdgeIntersections) {
    std::sort(polyedge.begin(), polyedge.end(), LtPolyFrac(this));
// #ifdef DEBUG
//     if(verbose) {
//       if(!polyedge.empty()) {
// 	oofcerr << "PixelPlaneFacet::completeLoops: sorted polyedge="
// 		<< std::endl;
// 	for(auto fib : polyedge) {
// 	  OOFcerrIndent indent(2);
// 	  oofcerr << "PixelPlaneFacet::completeLoops:  " << *fib
// 		  << std::endl;
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

  // This routine does *not* assume that the entries and exits
  // alternate along the polygon boundary.  It's possible to have, for
  // example, a VSB cross section that grazes the polygon exterior
  // (inserting a clockwise facet segment) and a non-cross section
  // facet that grazes the interior (inserting nothing on the boundary
  // except for exit and entry points).  The entry and exit points may
  // lie within the clockwise segment.
  unsigned int nEntries = 0;
  unsigned int nExits = 0;
  for(unsigned int e=0; e<tetPts.size(); e++)
    for(const PixelPlaneIntersection *fi : polyEdgeIntersections[e])
      if(fi->crossingType() == ENTRY)
	++nEntries;
      else if(fi->crossingType() == EXIT)
	++nExits;
#ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::completeLoops: nEntries=" << nEntries
// 	    << " nExits=" << nExits << std::endl;
//   }
  if(nEntries != nExits) {
    throw ErrProgrammingError("Mismatched entries and exits!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  if(nEntries > 0) {
    // Keep track of which intersections have been used already.  This
    // is ugly and may be slow, but that can be fixed later.  TODO:
    // Fix that.
    std::set<const PixelPlaneIntersection*> used;
    
    unsigned int nEntriesUsed = 0;
    unsigned int curEdge = 0;	// It doesn't really matter where we start
    unsigned int curIsec = 0;
    // exitEdge and exitIsec identify the current unpaired exit
    // intersection, if there is one.
    unsigned int exitEdge = NONE;
    unsigned int exitIsec = NONE;
    // Initialize the loop.
    if(polyEdgeIntersections[curEdge].size() > curIsec &&
       polyEdgeIntersections[curEdge][curIsec]->crossingType() == EXIT)
      {
	exitEdge = curEdge;
	exitIsec = curIsec;
      }
    // Loop over the intersections, looking for an exit if there is no
    // current exit, or for a non-exit to pair with the current exit.
    while(nEntriesUsed < nEntries) {
// #ifdef DEBUG
//       if(verbose)
// 	oofcerr << "PixelPlaneFacet::completeLoops: top of loop, curEdge="
// 		<< curEdge << " curIsec=" << curIsec
// 		<< " exitEdge=" << exitEdge << " exitIsec=" << exitIsec
// 		<< std::endl;
// #endif // DEBUG
      if(exitEdge == NONE) {
	// Find an exit.
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "PixelPlaneFacet::completeLoops: looking for exit"
// 		  << std::endl;
// #endif // DEBUG
	unsigned int lastEdge = curEdge; // prevent infinite loop in case
	unsigned int lastIsec = curIsec; // of error
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "PixelPlaneFacet::completeLoops: lastEdge=" << lastEdge
// 		  << " lastIsec=" << lastIsec << std::endl;
// #endif // DEBUG
	do {
	  incrementIsec(curEdge, curIsec, polyEdgeIntersections);
// #ifdef DEBUG
// 	  if(verbose)
// 	    oofcerr << "PixelPlaneFacet::completeLoops: curEdge=" << curEdge
// 		    << " curIsec=" << curIsec << " crossing="
// 		    << polyEdgeIntersections[curEdge][curIsec]->crossingType()
// 		    << " used="
// 		    << used.count(polyEdgeIntersections[curEdge][curIsec])
// 		    << std::endl;
// #endif // DEBUG
	  if(curEdge == lastEdge && curIsec == lastIsec) {
	    throw ErrProgrammingError("Wraparound while looking for exit!",
				      __FILE__, __LINE__);
	  }
	} while(polyEdgeIntersections[curEdge][curIsec]->crossingType() != EXIT
		|| used.count(polyEdgeIntersections[curEdge][curIsec])>0);

	exitEdge = curEdge;
	exitIsec = curIsec;
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "PixelPlaneFacet::completeLoops: exitEdge=" << exitEdge
// 		  << " exitIsec=" << exitIsec << std::endl;
// #endif // DEBUG
      }
      else {
	// exitEdge is not NONE.  Find the next entry or non-crossing
	// point to join to it.
// #ifdef DEBUG
// 	if(verbose)
// 	  oofcerr << "PixelPlaneFacet::completeLoops: looking for non-exit"
// 		  << std::endl;
// #endif // DEBUG
	unsigned int lastEdge = curEdge;
	unsigned int lastIsec = curIsec;
	do {
	  incrementIsec(curEdge, curIsec, polyEdgeIntersections);
	  if(curEdge == lastEdge && curIsec == lastIsec) {
	    throw ErrProgrammingError("Wraparound while looking for non-exit!",
				      __FILE__, __LINE__);
	  }
	} while(polyEdgeIntersections[curEdge][curIsec]->crossingType() == EXIT
		|| used.count(polyEdgeIntersections[curEdge][curIsec])>0);
// #ifdef DEBUG
// 	if(verbose) {
// 	  oofcerr << "PixelPlaneFacet::completeLoops: found non-exit. "
// 		  << " Connecting edge,isec " << exitEdge << "," << exitIsec
// 		  << " to " << curEdge << "," << curIsec
// 		  << std::endl;
// 	}
// #endif // DEBUG
	// Connect the exit and entry (or non-crossing intersection)
	addEdges(polyEdgeIntersections[exitEdge][exitIsec],
		 polyEdgeIntersections[curEdge][curIsec]);
	used.insert(polyEdgeIntersections[exitEdge][exitIsec]);
	used.insert(polyEdgeIntersections[curEdge][curIsec]);

	// Set up for next iteration.  If the current point is an
	// non-crossing point, we need to continue adding segments
	// from it, so pretend that it was actually an exit and
	// continue.  If it was an entry, start a new search for an
	// exit.
	if(polyEdgeIntersections[curEdge][curIsec]->crossingType() == ENTRY) {
	  ++nEntriesUsed;
	  exitEdge = NONE;
	  exitIsec = NONE;
	}
	else {
	  exitEdge = curEdge;
	  exitIsec = curIsec;
	}
      }	// end if exitEdge != NONE
    } // end while there are entries left 
  } // end if there are exits and entries
  
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::completeLoops: done, facet=" << *this
	    << std::endl;
  }
#endif // DEBUG
  
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
  newedges.reserve(edges.size() - nNullEdges);
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
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::getEdgesOnFaces: pixplane=" << *pixplane
// 	    << std::endl;
//   OOFcerrIndent indent(2);
// #endif // DEBUG
  const FacePixelPlane *baseFace = htet->getCoincidentFacePlane(pixplane);
  for(const FacetEdge *edge : edges) {
    FacePlaneSet faces = edge->startPt()->sharedFaces(edge->endPt(), baseFace);
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "PixelPlaneFacet::getEdgesOnFaces: edge=" << *edge
// 	      << std::endl;
//       oofcerr << "PixelPlaneFacet::getEdgesOnFaces: faces=";
//       for(const FacePlane *fp : faces)
// 	oofcerr << " " << *fp << std::endl;
//       }
// #endif // DEBUG
    for(const FacePlane *fp : faces) {
      // Construct an edge in the reverse order on the face facet.
      faceFacets[fp->face()].addEdge(
			     new FaceFacetEdge(htet,
					       edge->endPt()->referent(),
					       edge->startPt()->referent(),
					       pixplane));
    }
  }
//   for(FacetEdge *edge : edges) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneFacet::getEdgesOnFaces: facet="
// 	      << *pixplane << " edge=" << *edge << std::endl;
//     OOFcerrIndent indent(2);
// #endif // DEBUG
//     edge->getEdgesOnFaces(htet, pixplane, faceFacets);
//   }
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
  if(order == NONCONTIGUOUS) {
    // The points are on nonadjacent segments.
    firstPt = nullptr;
    secondPt = nullptr;
    turn = UNDEFINED;
  }
  else {
    if(order == FIRST) {
      firstPt = fi0;		// fi0 is first along the VSB
      secondPt = fi1;		// fi1 is second along the VSB
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

bool PixelPlaneFacet::resolveTwoFoldCoincidence(const PPIntersectionNRSet &isecs)
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
#ifdef DEBUG
      if(verbose)
	oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: trivial merge"
		<< std::endl;
#endif // DEBUG
      replaceIntersection(fi1, new RedundantIntersection(fi0, this));
    }
  } // end if crossing types are the same
  else {
    // There's one entry and one exit.
    bool multiCrossing = fi0->multipleCrossing() || fi1->multipleCrossing();
#ifdef DEBUG
    if(verbose)
      oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: multiCrossing="
	      << multiCrossing << std::endl;
#endif // DEBUG
    bool equiv = !multiCrossing && fi0->isEquivalent(fi1);
    bool misordered = !equiv && fi0->isMisordered(fi1, this);
    if(multiCrossing || equiv || misordered) {
#ifdef DEBUG
      if(verbose) {
	oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence:"
		<< " isEquivalent=" << equiv
		<< " isMisordered=" << misordered
		<< std::endl;
	oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: "
		<< "trying to merge equivalent entry and exit" << std::endl;
      }
#endif // DEBUG
      PixelPlaneIntersectionNR *merged = fi0->mergeWith(htet, fi1, this);
      if(merged) {
#ifdef DEBUG
	if(verbose) {
	  oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: merged="
		  << *merged << std::endl;
	}
	// if(!htet->verify()) {
	//   throw ErrProgrammingError("Verification failed!",
	//           __FILE__, __LINE__);
	// }
#endif // DEBUG
	replaceIntersection(fi0, merged);
	replaceIntersection(fi1, new RedundantIntersection(merged, this));
// #ifdef DEBUG
// 	  if(!htet->verify()) {
// 	    throw ErrProgrammingError("Verification failed!",
// 				      __FILE__, __LINE__);
// 	  }
// #endif // DEBUG
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
    }	// end if repairs were needed
#ifdef DEBUG
    else {
      if(verbose)
	oofcerr << "PixelPlaneFacet::resolveTwoFoldCoincidence: "
		<< "no repairs needed" << std::endl;
    }
#endif // DEBUG
  }
  return true;	     // coincidence handled
} // end PixelPlaneFacet::resolveTwoFoldCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool PixelPlaneFacet::resolveThreeFoldCoincidence(
			  const PPIntersectionNRSet &isecs)
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
      if(mergers.size() == 3) {
	PixelPlaneIntersectionNR *newfi = mergers[0]->mergeWith(
				htet,
				mergers[1]->mergeWith(htet, mergers[2], this),
				this);
	if(newfi) {
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

// IntersectionPair contains a pair of intersections and can be sorted
// by the distance between them.  It's used to decide which pair of
// intersections should be examined first in
// resolveMultipleCoincidence.  It's not a facet edge of any sort,
// since it's used to resolve round-off error induce topological
// problems before the edges are constructed.

class IntersectionPair {
public:
  // Using a typedef here because I'm not sure what the final type
  // will be and want to be able to change it easily.
  typedef PixelPlaneIntersectionNR IsecType;
  IsecType *pt0;
  IsecType *pt1;
  double length2;		// distance squared between points
  bool verified;
  IntersectionPair(const HPixelPlane *pixplane, IsecType *pt0, IsecType *pt1)
    : pt0(pt0), pt1(pt1)
  {
    initialize(pixplane);
  }
  void initialize(const HPixelPlane *pixplane) {
    length2 = norm2(pt0->location2D(pixplane) - pt1->location2D(pixplane));
    verified = false;
  }
  void replacePoint0(const HPixelPlane *pixplane, IsecType *pt) {
    pt0 = pt;
    initialize(pixplane);
  }
  void replacePoint1(const HPixelPlane *pixplane, IsecType *pt) {
    pt1 = pt;
    initialize(pixplane);
  }
  
  // IntersectionPair(const IntersectionPair &other)
  //   : pt0(other.pt0), pt1(other.pt1), length2(other.length2),
  //     verified(other.verified)
  // {}
  // const IntersectionPair &operator=(const IntersectionPair &other) {
  //   pt0 = other.pt0;
  //   pt1 = other.pt1;
  //   length2 = other.length2;
  //   verified = other.verified;
  //   return *this;
  // }
  bool operator<(const IntersectionPair &other) const {
    return length2 < other.length2;
  }
};

typedef std::vector<IntersectionPair> IsecPairList;

// Utility function to update the list of intersection pairs after the
// intersections in a pair have been replaced with a single new
// intersection.  i is the index of the pair, and newIsec is the
// replacement.
static void updatePairList(IsecPairList &pairs,
			   unsigned int i,
			   IntersectionPair::IsecType *newIsec,
			   const HPixelPlane *pixplane
#ifdef DEBUG
			   , bool verbose
#endif // DEBUG
			   )
{
  IntersectionPair::IsecType *pt0 = pairs[i].pt0;
  IntersectionPair::IsecType *pt1 = pairs[i].pt1;
  // Find the other pairs that use pt0 and pt1.  They have to be
  // replaced.  The list is sorted by length, not position of the
  // intersections, so the whole list has to be searched.  It's not
  // long, though.
  unsigned int j0 = NONE;
  unsigned int j1 = NONE;
  for(unsigned int k=0; k<pairs.size(); k++)
    if(k != i && pairs[k].pt1 == pt0) {
      j0 = k;
      break;
    }
  for(unsigned int k=0; k<pairs.size(); k++)
    if(k != i && pairs[k].pt0 == pt1) {
      j1 = k;
      break;
    }
#ifdef DEBUG
  if(pairs.size() > 1 && j0 == NONE && j1 == NONE) {
    oofcerr << "updatePairList: couldn't find j0 or j1! i=" << i << std::endl;
    oofcerr << "updatePairList: newIsec=" << *newIsec << std::endl;
    oofcerr << "updatePairList: j0=" << j0 << " j1=" << j1
	    << " nPairs=" << pairs.size() << std::endl;
    // oofcerr << "updatePairList: pairs=" << std::endl;
    // for(unsigned int k=0; k<pairs.size(); k++) {
    //   OOFcerrIndent indent(2);
    //   oofcerr << "updatePairList: " << k  << ": "
    // 	      << *pairs[k].pt0  << " " << *pairs[k].pt1 << std::endl;
    // }
    throw ErrProgrammingError("updatePairList failed!", __FILE__, __LINE__);
  }
#endif // DEBUG
  if(j0 != NONE)
    pairs[j0].replacePoint1(pixplane, newIsec);
  if(j1 != NONE)
    pairs[j1].replacePoint0(pixplane, newIsec);
  pairs.erase(pairs.begin()+i);	// remove the defunct pair
  // TODO: Since the list was sorted when we started and we know which
  // pairs have changed, std::sort might not be the most efficient way
  // to re-sort it.
  std::sort(pairs.begin(), pairs.end());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// resolveMultipleCoincidence resolves (rare?) coincidences of four or
// more PixelPlaneIntersection points.  In principle it could be used
// for two or three point coincidences as well, but it might be slower
// than the functions above.

// resolveMultipleCoincidence looks at pairs of adjacent
// intersections, starting with the closest two, and applies the
// two-fold coincidence checker to them.

// First create a list of intersections, in sequence going around the
// perimeter of the polygon.  Then create a list of pairs of adjacent
// intersections from the first list.  (Include a pair that joins the
// first and last intersections in the list if appropriate.)  Sort the
// pairs by length, so that the closest pair is first.  Loop through
// the pairs, looking for the first one that (a) hasn't been checked,
// and (b) has invalid toplogy.  Merge the points in that pair, remove
// it from the list, and update the neighboring pairs, which now must
// contain the newly formed merged intersection.  Re-sort the list of
// pairs, and repeat until there's nothing left to fix.

// Fixing the shortest pair first resolves situations like this, where
// if we examined the pairs in order on the perimeter the first pair
// examined would be illegal and unfixable:

//       -------------B-C--------------
//      /              X              /
//     /              / \            /
//    /              /   \          /
//   /______________/_____\________/  polygon  
//                 A       D

// AC and BD are the voxel set boundary edges.  Points B and C are
// supposed to coincide on the polygon boundary, but they don't and
// are misordered.  If the pairs are ordered along the perimeter, DC
// may be evaluated first.  The segments cross but D and C are both
// entries and can't be merged.  If BC is merged first then there is
// no conflict.

bool PixelPlaneFacet::resolveMultipleCoincidence(
			 const PPIntersectionNRSet &isecs,
			 unsigned int totalIsecs)
{
  unsigned int npts = isecs.size();
  unsigned int np = tetPts.size();

#ifdef DEBUG
  if(verbose)
    oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence, totalIsecs="
	    << totalIsecs << std::endl;
  OOFcerrIndent indent(2);
#endif // DEBUG

  // Create an ordered list of the intersections, going around the
  // polygon.  Assuming that the intersections are clumped (which will
  // be the case unless the polygon is very small) the ordered list
  // should start at the beginning of the clump.  If they're not
  // clumped, it doesn't matter where the list starts, so pretend that
  // they're clumped.
  
  // polyIsecs[e] is a vector of intersections on edge e.
  std::vector<std::vector<PixelPlaneIntersectionNR*>> polyIsecs(np);
  for(unsigned e=0; e<np; e++) {
    polyIsecs[e].reserve(isecs.size());
  }

  // Put the intersections in the lists for their edges.
  for(PixelPlaneIntersectionNR *isec: isecs) {
    // At this point the points must be either SimpleIntersections or
    // MultiVSBIntersections, which are subclasses of SingleFaceBase.
    const SingleFaceBase *sfb = dynamic_cast<const SingleFaceBase*>(isec);
    assert(sfb != nullptr);
    unsigned int polyseg = faceEdgeMap[sfb->getFacePlane()];
    polyIsecs[polyseg].push_back(isec);
#ifdef DEBUG
    if(verbose) {
      oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: isec="
	      << *isec << " polyseg=" << polyseg << std::endl;
    }
#endif // DEBUG
  }

  // Sort the intersections on each edge
  for(auto &isecvec : polyIsecs)
    if(isecvec.size() > 1) 
      std::sort(isecvec.begin(), isecvec.end(), LtPolyFrac(this));

#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: done sorting"
	    << std::endl;
    for(unsigned int i=0; i<np; i++) {
      oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: edge "
	      << i << std::endl;
      OOFcerrIndent indent(2);
      if(polyIsecs[i].empty())
	oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: empty"
		<< std::endl;
      else {
	for(const PixelPlaneIntersectionNR *ppi : polyIsecs[i])
	  oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: "
		  << *ppi << std::endl;
      }
    }
  }
#endif // DEBUG


  // Make a list of all pairs of adjacent intersections, sorted by
  // the distance between them.

  IsecPairList pairs;

  // Construct each pair with the current point and the previous
  // point, so we have to find the first previous point.  The first
  // current point is the first point on the first non-empty edge.
  // The first previous point is the last point on the last non-empty
  // edge.
  unsigned int prevEdge = np - 1; // Last non-empty edge
  while(polyIsecs[prevEdge].empty())
    prevEdge--;
  for(unsigned int edge=0; edge<np; edge++) {
    if(!polyIsecs[edge].empty()) {
      // The first point on the edge is paired with the last one on
      // the previous edge.
      pairs.emplace_back(pixplane,
			 polyIsecs[prevEdge].back(), polyIsecs[edge].front());
      for(unsigned int i=1; i<polyIsecs[edge].size(); i++) {
	pairs.emplace_back(pixplane, polyIsecs[edge][i-1], polyIsecs[edge][i]);
      }
      prevEdge = edge;
    }	// end if edge is not empty
  }	// end loop over edges

  // Sort the list of pairs from shortest to longest.
  std::sort(pairs.begin(), pairs.end());

  // If the given set of intersections wraps around the entire
  // polygon, then we will need to include the pair that joins the
  // last intersection to the first.  If the set doesn't wrap around,
  // the distance between the last intersection and the first will be
  // longer than any other distance between adjacent intersections in
  // the set, because the set is a clump of nearby intersections.
  double longestPairSize2 = pairs.back().length2;
  if(!(npts==totalIsecs && longestPairSize2 > CLOSEBY2)) {
    // We're not wrapping around.  Remove the longest pair.
    pairs.pop_back();
  }

  // Until there's nothing more to fix, search the intersection pairs
  // from shortest to longest and fix them if necessary. 
  bool fixedSomething = true;
  while(fixedSomething) {
    fixedSomething = false;
    for(unsigned int i=0; i<pairs.size(); i++) {
#ifdef DEBUG
      if(verbose) {
	oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: i=" << i
		<< std::endl;
	oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: current pairs="
		<< std::endl;
	for(unsigned int ii=0; ii<pairs.size(); ii++)
	  oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: "
		  << ii << " "
		  << pairs[ii].pt0 << " " << *pairs[ii].pt0 << " "
		  << pairs[ii].pt1 << " " << *pairs[ii].pt1 << " "
		  << sqrt(pairs[ii].length2) << std::endl;
      }
#endif // DEBUG
      if(!pairs[i].verified) {	// don't check pairs twice
	IntersectionPair::IsecType *i0 = pairs[i].pt0;
	IntersectionPair::IsecType *i1 = pairs[i].pt1;
	// Check for doubled entries and exits.  These are points at
	// which the VSB passes through a vertex of the polygon. Both
	// of the polygon edges at the vertex will have recorded an
	// entry or an exit.
	if(i0->crossingType() == i1->crossingType() &&
	   (i0->getPolyEdge(this)+1)%np == i1->getPolyEdge(this) &&
	   i0->onSameLoopSegment(i1))
	  {
	    updatePairList(pairs, i, i1, pixplane
#ifdef DEBUG
			   , verbose
#endif // DEBUG
			   );
	    replaceIntersection(i0, new RedundantIntersection(i1, this));
	    // After updating the pair list, there may be a new
	    // shortest pair, so start the loop over.
	    fixedSomething = true;
	    break;
	  }
	bool equiv = i0->isEquivalent(i1);
	bool wrongParity =
	  (i0->crossingType() == ENTRY && i1->crossingType() == ENTRY) ||
	  (i0->crossingType() == EXIT && i1->crossingType() == EXIT);
	// Don't call isMisordered if we already know that the pair
	// needs to be merged.
	bool misordered = !equiv && !wrongParity && i0->isMisordered(i1, this);
	if(equiv || wrongParity || misordered) {
#ifdef DEBUG
	  if(verbose)
	    oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: "
		    << "equiv=" << equiv << " wrongParity=" << wrongParity
		    << " misordered=" << misordered << std::endl;
#endif // DEBUG
	  PixelPlaneIntersectionNR *inew = i0->mergeWith(htet, i1, this);
	  if(inew) {
	    updatePairList(pairs, i, inew, pixplane
#ifdef DEBUG
			   , verbose
#endif // DEBUG
			   );
	    replaceIntersection(i0, inew);
	    replaceIntersection(i1, new RedundantIntersection(inew, this));
	    fixedSomething = true;
	    break;
	  }
	  throw ErrProgrammingError("Failed to merge intersections!",
				    __FILE__, __LINE__);
	}
#ifdef DEBUG
	if(verbose)
	  oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: ok"
		  << std::endl;
#endif // DEBUG
	pairs[i].verified = true;
      }	// end if pair hasn't been checked
    } // end loop over intersection pairs i
  } // end while(fixedSomething)

#ifdef DEBUG
  if(verbose)
    oofcerr << "PixelPlaneFacet::resolveMultipleCoincidence: done" << std::endl;
#endif // DEBUG
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
#ifdef DEBUG
  if(fi0->crossingType() == fi1->crossingType()) {
    oofcerr << "PixelPlaneFacet::vsbCornerCoincidence: crossing types match!"
	    << std::endl;
    oofcerr << "PixelPlaneFacet::vsbCornerCoincidence: fi0=" << *fi0<< std::endl;
    oofcerr << "PixelPlaneFacet::vsbCornerCoincidence: fi1=" << *fi1<< std::endl;
    throw ErrProgrammingError("Bad arguments to vsbCornerCoincidence",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
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
  EdgePosition entryPolyFrac = entryPt->getPolyFrac(polyseg, this);
  EdgePosition exitPolyFrac = exitPt->getPolyFrac(polyseg, this);
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::vsbCornerCoincidence: entryPt=" << *entryPt
	    << " exitPt=" << *exitPt <<  std::endl
	    << "                                     : polyseg=" << polyseg
	    << std::endl
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
#ifdef DEBUG
  if(fi0->onSameFacePlane(fi1, getBaseFacePlane())) {
    oofcerr << "PixelPlaneFacet::polyCornerCoincidence: fi0=" << *fi0
    	    << std::endl;
    oofcerr << "PixelPlaneFacet::polyCornerCoincidence: fi1=" << *fi1
    	    << std::endl;
    oofcerr << "PixelPlaneFacet::polyCornerCoincidence: baseplane="
	    << getBaseFacePlane();
    oofcerr << " " << *getBaseFacePlane() << std::endl;
    throw ErrProgrammingError("Points are on the same polygon segment!",
			      __FILE__, __LINE__);
   
  }
#endif // DEBUG
  assert(fi0->onSameLoopSegment(fi1)); // same VSB segment
  assert(fi0->crossingType() != fi1->crossingType());
  const PixelBdyLoopSegment *seg = fi0->sharedLoopSegment(fi1);
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneFacet::polyCornerCoincidence: seg=" << *seg
// 	    << std::endl;
//     oofcerr << "PixelPlaneFacet::polyCornerCoincidence: crossingType0="
// 	    << fi0->crossingType() << " crossingType1="
// 	    << fi1->crossingType() << std::endl;
//     oofcerr << "PixelPlaneFacet::polyCornerCoincidence: loopfrac0="
// 	    << fi0->getLoopFrac(*seg) << " loopfrac1="
// 	    << fi1->getLoopFrac(*seg) << std::endl;
//     oofcerr << "PixelPlaneFacet::polyCornerCoincidence: polyedge0="
// 	    << fi0->getPolyEdge(this) << " polyedge1="
// 	    << fi1->getPolyEdge(this) << std::endl;
//   }
// #endif // DEBUG
  // Return true if points are out of order.
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
  assert(fi0->nSharedPolySegments(fi1, this) == 0);
#ifdef DEBUG
  OOFcerrIndent indent(2);
  // if(fi0->samePixelPlanes(fi1)) {
  //   oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: same pixel planes!"
  // 	      << std::endl;
  //   oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: fi0=" << *fi0
  // 	      << std::endl;
  //   oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: fi1=" << *fi1
  // 	      << std::endl;
  // }
  if(fi0->onSameFacePlane(fi1, getBaseFacePlane())) {
    oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence:"
	    << " points are on same tet face!"
	    << std::endl;
    oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: fi0=" << *fi0
	    << std::endl;
    oofcerr << "PixelPlaneFacet::polyVSBCornerCoincidence: fi1=" << *fi1
	    << std::endl;
    throw ErrProgrammingError("Points are on same face!", __FILE__, __LINE__);
  }
#endif // DEBUG
  // assert(!fi0->onSameFacePlane(fi1, getBaseFacePlane()));
  assert(!fi0->samePixelPlanes(fi1));
  assert(fi0->crossingType() != fi1->crossingType());
  const PixelPlaneIntersectionNR *entryPt, *exitPt;
  // firstPt and secondPt refer to positions along the VSB segments
  const PixelPlaneIntersectionNR *firstPt, *secondPt;
  ICoord2D corner;
  TurnDirection turn;
  classifyVSBcorner(fi0, fi1, entryPt, exitPt, firstPt, secondPt, corner, turn
#ifdef DEBUG
		    , verbose
#endif // DEBUG
		    );
  BarycentricCoord bcorner = htet->getBarycentricCoord(corner, pixplane);

  // Is the VSB corner on hte interior side of the tet faces that form
  // the polygon sides occupied by fi0 and fi1? 
  bool inside = true;
  for(const FacePlane *face : fi0->facePlaneSets()) {
    if(!inside) break;
    unsigned int f = face->face();
    if(f != onFace)
      inside &= bcorner.interiorToFace(f);
  }
  for(const FacePlane *face : fi1->facePlaneSets()) {
    if(!inside) break;
    unsigned int f = face->face();
    if(f != onFace)
      inside &= bcorner.interiorToFace(f);
  }
  
  // If the VSB corner is interior to the polygon, the entry point
  // must precede the exit point on the VSB. If the VSB corner is
  // outside, the entry and exit must be in the opposite order.  If
  // the order is wrong, the points must coincide, and this function
  // returns true. 
  bool valid = ((inside && entryPt == firstPt) ||
		(!inside && exitPt == firstPt));

#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
	    << "fi0=" << *fi0 << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
	    << "fi1=" << *fi1 << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
	    << " corner=" << corner << " " << bcorner << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
	    << "  firstPt=" << *firstPt << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
	    << " secondPt=" << *secondPt << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
	    << " entryPt=" << *entryPt << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: "
	    << "  exitPt=" << *exitPt << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::polyVSBCornerCoincidence: inside="
	    << inside << " onFace=" << onFace
	    << " invalid=" << !valid << std::endl;
  }
#endif // DEBUG
  return !valid;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// tripleCoincidence is called by resolveThreeFoldCoincidence to find
// which intersections (if any) need to be merged.  There are two
// classes of triple coincidence, involving either two or three VSB
// segments.

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
  // sharedSeg is a loop segment that's shared by the nodes.  It's not
  // guaranteed to be the only shared segment (if the intersections
  // are at a corner).
  const PixelBdyLoopSegment *sharedSeg = fi0->sharedLoopSegment(fiB);
  if(sharedSeg != nullptr) {
    fiA = fi0;
    fiC = fi1;
  }
  else {
    sharedSeg = fi1->sharedLoopSegment(fiB);
    if(sharedSeg != nullptr) {
      fiA = fi1;
      fiC = fi0;
    }
  }
  if(sharedSeg != nullptr) {
    // There are two VSB segments.

    // When traversing either the polygon segments or the VSB
    // segments, entries and exits must alternate in the intersection
    // sequence.  This routine can assume that there are two entries
    // and one exit or two exits and one entry, and that the two
    // entries or exits are on different VSB segments.

    /*   A /\ B                B /\ A
    //  --o--o----          ----o--o---  VSB bdy
    //   /    \  |          |  /    \
    //  /      \ |          | /      \ polygon bdy
    //          \|          |/            
    //           o C        o C      The polygon bdy is always counterclockwise.
    //           |\        /|        The VSB bdy can go either direction, so
    //           | \      / |        these pictures apply to both R and L turns.
    */
    
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
    EdgePosition polyFracB = fiB->getPolyFrac(edgeBC, this);
    EdgePosition polyFracC = fiC->getPolyFrac(edgeBC, this);
  
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
  } // end if sharedseg != nullptr

  else {
    // All three intersections are on different VSB segments.  We
    // already know that fi0 and fi1 are both entries or both exits,
    // so they must be the right and left points in the diagrams
    // below.
    /*
    // ....... /\.|        ......| /\          
    // ......./..\|        ......|/  \         
    // ....../....o        ......o    \        The polygon segments go
    // ...../.....|\       ...../|     \       counterclockwise, but don't
    // ..../......| \      ..../.|      \      actually have to meet; there
    // ---o--->---+--o---  ---o--+----<--o---  could be intermediate segments.
    //   /        |...\..    /   |........\..  
    //  /         |....\.   /    |.........\.  

    //         /\ |......      (B)./\........  
    //        /  \|......        |/..\.......  
    //       /    o......        o....\......  
    //      /     |\.....       /|.....\.....  
    //     /      |.\....  (C) / |......\ ...  
    // ---o---<---+--o---  -<-o--+--->---o---(A)
    // ../........|   \    ../...|        \    
    // ./.........|    \   ./....|         \   
    */

    // First, find the three VSB segments.  They must meet at a point.
    // Label them A, B, C going counter-clockwise around that point,
    // with the non-intersected VSB segment coming between C and A.
    const SingleVSBbase *si0 = dynamic_cast<const SingleVSBbase*>(fi0);
    const SingleVSBbase *si1 = dynamic_cast<const SingleVSBbase*>(fi1);
#ifdef DEBUG
    if(si0 == nullptr || si1 == nullptr) {
      oofcerr << "PixelPlaneFacet::tripleCoincidence:"
	      << " cast to SingleVSBbase failed!"
	      << std::endl;
      oofcerr << "PixelPlaneFacet::tripleCoincidence: si0=" << si0
	      << " si1=" << si1 << std::endl;
      throw ErrProgrammingError("Error in PixelPlaneFacet::tripleCoincidence",
				__FILE__, __LINE__);
    }
#endif // DEBUG

    // If fiB is *not* a SingleVSBbase, then B must be right at the
    // point between the pixels.  All of the points must coincide,
    // because the polygon must be convex.
    const SingleVSBbase *siB = dynamic_cast<const SingleVSBbase*>(fiB);
    if(siB == nullptr) {
#ifdef DEBUG
      if(verbose)
	oofcerr << "PixelPlaneFacet::tripleCoincidence: all points coincide"
		<< std::endl;
#endif // DEBUG
      coincidentPoints.push_back(fi0);
      coincidentPoints.push_back(fi1);
      coincidentPoints.push_back(fiB);
      return coincidentPoints;
    }
    const PixelBdyLoopSegment &seg0 = si0->getLoopSeg();
    const PixelBdyLoopSegment &seg1 = si1->getLoopSeg();
    const PixelBdyLoopSegment &segB = siB->getLoopSeg();
    PixelBdyLoopSegment segA, segC;
    // seg0 and seg1 must start or end on a common point
    ICoord2D centerPt, farPt0, farPtB, farPt1;
    if(seg0.firstPt() == seg1.firstPt()) {
      centerPt = seg0.firstPt();
      farPt0 = seg0.secondPt();
      farPt1 = seg1.secondPt();
      farPtB = segB.firstPt();
      assert(segB.secondPt() == centerPt);
    }
    else if(seg0.secondPt() == seg1.secondPt()) {
      centerPt = seg0.secondPt();
      farPt0 = seg0.firstPt();
      farPt1 = seg1.firstPt();
      farPtB = segB.secondPt();
      assert(segB.firstPt() == centerPt);
    }
    else {
      throw ErrProgrammingError("Incompatible segments in tripleCoincidence()",
				__FILE__, __LINE__);
    }
    ICoord2D r0 = farPt0 - centerPt;
    ICoord2D r1 = farPt1 - centerPt;
    ICoord2D rB = farPtB - centerPt;
    if(r0 % rB > 0 && rB % r1 > 0) {
      segA = seg0;
      segC = seg1;
      fiA = fi0;
      fiC = fi1;
    }
    else if(r1 % rB > 0 && rB % r0 > 0) {
      segA = seg1;
      segC = seg0;
      fiA = fi1;
      fiC = fi0;
    }
    else {
      // Unexpected ordering.  B is either first or last.  Merge it
      // with the one in the middle.
      coincidentPoints.push_back(fiB);
      if((rB % r0 > 0 && r0 % r1 > 0) || (r1 % r0 > 0 && r0 % rB > 0)) {
	coincidentPoints.push_back(fi0);
      }
      else {
	assert((rB % r1 > 0 && r1 % r0 > 0) || (r0 % r1 > 0 && r1 % rB > 0));
	coincidentPoints.push_back(fi1);
      }
      return coincidentPoints;
    }
    // If A and C are on the same polygon segment all three points
    // must coincide (again).
    const FacePlane *faceAC = fiA->sharedFace(fiC, getBaseFacePlane());
    if(faceAC != nullptr) {
      coincidentPoints.push_back(fi0);
      coincidentPoints.push_back(fi1);
      coincidentPoints.push_back(fiB);
      return coincidentPoints;
    }
    // If two intersections are on the same polygon segment, check
    // that they're in the right order.
    const FacePlane *faceAB = fiA->sharedFace(fiB, getBaseFacePlane());
    if(faceAB != nullptr) {
      unsigned int edgeAB = getPolyEdge(faceAB);
      EdgePosition polyFracA = fiA->getPolyFrac(edgeAB, this);
      EdgePosition polyFracB = fiB->getPolyFrac(edgeAB, this);
      if(polyFracA >= polyFracB) {
	coincidentPoints.push_back(fiA);
	coincidentPoints.push_back(fiB);
	return coincidentPoints;
      }
    }
    const FacePlane *faceBC = fiB->sharedFace(fiC, getBaseFacePlane());
    if(faceBC != nullptr) {
      unsigned int edgeBC = getPolyEdge(faceBC);
      EdgePosition polyFracB = fiB->getPolyFrac(edgeBC, this);
      EdgePosition polyFracC = fiC->getPolyFrac(edgeBC, this);
      if(polyFracB >= polyFracC) {
	coincidentPoints.push_back(fiB);
	coincidentPoints.push_back(fiC);
	return coincidentPoints;
      }
    }
  }
  return coincidentPoints;
} // end PixelPlaneFacet::tripleCoincidence

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// PixelPlaneFacet::badTopology for a SimpleIntersection and a
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
#ifdef DEBUG
  if(!(mfiIsEntry ^ siIsEntry)) {
    oofcerr << "PixelPlaneFacet::badTopology: incompatible intersections!"
	    << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology:  si=" << *si << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology: mfi=" << *mfi << std::endl;
    throw ErrProgrammingError("badTopology failed!", __FILE__, __LINE__);
  }
#endif // DEBUG
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

#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneFacet::badTopology: si=" << *si << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology: mvi=" << *mvi << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology: siFirstOnPoly=" << siFirstOnPoly
	    << " mviFirstOnPoly=" << mviFirstOnPoly
	    << " extraPolySegment=" << extraPolySegment << std::endl;
  }
#endif // DEBUG
	     

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
      // E0. The polygon corner is on the right side of the first VSB segment
      // E1. The polygon corner is on the right side of the second VSB segment

      // (Different edge configurations can have the same sets of values
      // for A-D.  That's ok.)

      static std::set<std::vector<bool>> legalCombos = {
	// A      B      C      D     E0     E1
	{false, true,  true,  false, false, true},  // L0
	{true,  false, false, false, true,  false}, // L1
	{false, true,  true,  false, true,  true},  // L2	
	{true,  false, false, false, true,  true},  // L3
	{false, true,  false, false, false, false}, // L4
	{true,  false, true,  false, false, false}, // L5
	{true,  false, true,  true,  false, true},  // R0	
	{false, true,  false, true,  true,  false}, // R1
	{true,  false, true,  true,  false, false}, // R2
	{false, true,  false, true,  false, false}, // R3
	{true,  false, false, true,  true,  true},  // R4
	{false, true,  true,  true,  true,  true}   // R5
      };
  
      bool conditionA = si->crossingType() == ENTRY;
      bool conditionB = si->getLoopSeg() == loopSeg1;
      bool conditionC = mviFirstOnPoly;
      bool conditionD = turn == RIGHT;

      // index of the polygon corner
      unsigned int polyVertexIndex = mviFirstOnPoly ? siPolySeg : mviPolySeg;
      // position of the polygon corner
      Coord2D polyVertex = polygonCorner(polyVertexIndex);
      bool conditionE0 = loopSeg0.onRight(polyVertex);
      bool conditionE1 = loopSeg1.onRight(polyVertex);
    
#ifdef DEBUG
      if(verbose) {
	oofcerr << "PixelPlaneFacet::badTopology: loopSeg0=" << loopSeg0
		<< " loopSeg1=" << loopSeg1 << " polyVertex=" << polyVertex
		<< std::endl;
	oofcerr << "PixelPlaneFacet::badTopology: loopSeg0.onRight="
		<< loopSeg0.onRight(polyVertex)
		<< " loopSeg1.onRight=" << loopSeg1.onRight(polyVertex)
		<< std::endl;
	oofcerr << "PixelPlaneFacet::badTopology: conditionA=" << conditionA
		<< " conditionB=" << conditionB
		<< " conditionC=" << conditionC
		<< " conditionD=" << conditionD
		<< " conditionE0=" << conditionE0
		<< " conditionE1=" << conditionE1 << std::endl;
      }
#endif // DEBUG

      std::vector<bool> combo = {conditionA, conditionB, conditionC, conditionD,
				 conditionE0, conditionE1};
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
#ifdef DEBUG
  if(mfi0->nPolySegments() != 2 || mfi1->nPolySegments() != 2) {
    oofcerr << "PixelPlaneFacet::badTopology: mfi0=" << *mfi0 << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology: mfi1=" << *mfi1 << std::endl;
    throw ErrProgrammingError("Wrong number of polygon segments!",
			      __FILE__, __LINE__);
  }
  if(verbose) {
    oofcerr << "PixelPlaneFacet::badTopology: mfi0=" << *mfi0 << std::endl;
    oofcerr << "PixelPlaneFacet::badTopology: mfi1=" << *mfi1 << std::endl;
  }
  OOFcerrIndent indent(2);
#endif // DEBUG
  const PixelBdyLoopSegment &loopSeg0 = mfi0->getLoopSeg();
  const PixelBdyLoopSegment &loopSeg1 = mfi1->getLoopSeg();
#ifdef DEBUG
  if(verbose)
    oofcerr << "PixelPlaneFacet::badTopology: loopSeg0=" << loopSeg0
	    << " loopSeg1=" << loopSeg1 << std::endl;
#endif // DEBUG
  
  if(loopSeg0 != loopSeg1) {
    bool mfi0FirstOnVSB = loopSeg1.follows(loopSeg0);
#ifdef DEBUG
    bool mfi1FirstOnVSB = loopSeg0.follows(loopSeg1);
    assert(mfi0FirstOnVSB ^ mfi1FirstOnVSB);
#endif	// DEBUG

    unsigned int sharedPolySeg = mfi0->sharedPolySegment(mfi1, this);
#ifdef DEBUG
    if(verbose) {
      oofcerr << "PixelPlaneFacet::badTopology: mfi0FirstOnVSB="
	      << mfi0FirstOnVSB << " sharedPolySeg=" << sharedPolySeg
	      << std::endl;
    }
#endif // DEBUG
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
  } // end if loopSeg0 != loopSeg1

  /* If both MultiFaceIntersections are on the same VSB loop segment,
  // there are two additional configurations:
  //                             /       / 
  //      B        A            /       /   
  //  --<-o========o---     -<-o=======o----
  //    ...\........\..     ...B.......A....
  //    ....\........\.     ................
  //       case 1             case 2
  //
  //  The === lines show where the VSB (---) and the polygon edges
  //  coincide.  We can check that the ordering of the points on the
  //  VSB is consistent with the ordering on the polygon.
  */

  unsigned int sharedPolySeg = mfi0->sharedPolySegment(mfi1, this);
  if(sharedPolySeg == NONE)
    return true;
  const MultiFaceIntersection *mfiA = nullptr;
  const MultiFaceIntersection *mfiB = nullptr;
  if(mfi0->crossingType() == ENTRY ||
     (mfi0->crossingType() != ENTRY && mfi1->crossingType() == EXIT)) {
    mfiA= mfi0;
    mfiB = mfi1;
  }
  else {
    mfiA = mfi1;
    mfiB = mfi0;
  }

  // Compare positions along the VSB.
  double loopFracA = mfiA->getLoopFrac();
  double loopFracB = mfiB->getLoopFrac();
  if(loopFracB <= loopFracA)
    return true;
  // Compare positions along the polygon and the implied interiority
  // of the polygon segments.
  EdgePosition polyFracA = mfiA->getPolyFrac(sharedPolySeg, this);
  EdgePosition polyFracB = mfiB->getPolyFrac(sharedPolySeg, this);
  if(polyFracB < polyFracA) {	// case 1
    return (mfiA->interiority(0, this) == EXTERIOR ||
	    mfiB->interiority(1, this) == EXTERIOR);
  }
  else if(polyFracB > polyFracA) { // case 2
    return (mfiA->interiority(1, this) == INTERIOR ||
	    mfiB->interiority(0, this) == INTERIOR);
  }
  // If the points are at the same position on the polygon segment
  // (which is impossible, because they must be at opposite ends of a
  // segment, they're also misordered.
  return true;
} //PixelPlaneFacet::badTopology(MultiFaceIntersection*, MultiFaceIntersection*)

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
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::badTopology_: turn=" << turn << std::endl;
// #endif // DEBUG
  if(turn != LEFT && turn != RIGHT)
    return true;
  Interiority interiority0 = mfi0->interiority(this);
  Interiority interiority1 = mfi1->interiority(this);
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::badTopology_: interiority0=" << interiority0
// 	    << " interiority1=" << interiority1 << std::endl;
// #endif // DEBUG
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
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneFacet::badTopology_: sameDirection=" << sameDirection
// 	    << std::endl;
// #endif // DEBUG

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
    os << "                faceEdgeMap= {";
    bool strt = true;
    for(auto i=facet.faceEdgeMap.begin(); i!=facet.faceEdgeMap.end(); ++i) {
      if(!strt) 
	os << ", ";
      strt = false;
      os << *(*i).first << ":" << (*i).second;
    }
    os << "}" << std::endl;
  }
  os << ")";
  return os;
}

std::string PixelPlaneFacet::shortDescription() const {
  std::string spaces = "    ";
  std::string result;
  for(const FacetEdge *edge : edges) {
    result += (spaces + to_string(edge->startPos3D()) + ", " +
	       to_string(edge->endPos3D())) + '\n';
      
  }
  return result;
}

#ifdef DEBUG
std::ostream &operator<<(std::ostream &os, const FacetEdge &edge) {
  os << edge.edgeType() << "(" << *edge.startPt() << ", " << *edge.endPt();
  if(edge.nullified())
    os << ", nullified";
  os << ", length=" << sqrt(edge.length2()) << ")";
  return os;
}
#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void PixelPlaneFacet::dump(unsigned int cat) const {
  std::string filename = ("pixelplane" + pixplane->shortName()
			  + "cat" + to_string(cat)
			  + ".lines");
  std::cerr << "PixelPlaneFacet::dump: writing " << filename << std::endl;
  std::ofstream file(filename);
  for(const FacetEdge *edge : edges) {
    // std::cerr << edge->startPos3D() << ", " << edge->endPos3D() << std::endl;
    file << edge->startPos3D() << ", " << edge->endPos3D() << std::endl;
  }
  file.close();
}
