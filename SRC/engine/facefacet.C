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

#include "common/cmicrostructure.h"
#include "common/tostring.h"
#include "common/segintersection.h"
#include "engine/cskeletonelement.h"
#include "engine/facefacet.h"
#include "engine/homogeneitytet.h"
#include "engine/pixelplanefacet.h"
#include "engine/planeintersection.h"

#include <math.h>

FaceEdgeIntersection::FaceEdgeIntersection(PlaneIntersection *crnr,
					   FaceFacetEdge *edge,
					   bool start)
  : crnr(crnr),
    edge_(edge),
    fEdge(NONE),
    segstart(start)
{}

bool FaceEdgeIntersection::operator<(const FaceEdgeIntersection &other) const {
  if(*corner() < *other.corner()) return true;
  if(*other.corner() < *corner()) return false;
  if(*edge() < *other.edge()) return true;
  return false;
}

void FaceEdgeIntersection::findFaceEdge(unsigned int face, HomogeneityTet *htet)
{
  EdgePosition tt;
  unsigned int ee = NONE;
  htet->findFaceEdge(crnr, face, ee, tt);
  setFaceEdge(ee, tt);
// #ifdef DEBUG
//   if(htet->verbosecategory) {
//     oofcerr << "FaceEdgeIntersection::findFaceEdge: face=" << face
// 	    << " fEdge=" << fEdge << " t=" << t << std::endl;
//   }
// #endif // DEBUG
}

// A marooned StrandedPoint is one that can't be matched to a
// StrandedPoint on a different face.  It must really belong on an
// edge of the face that it's on.  This routine finds the closest edge
// and puts the point there, by modifying the point's equivalence class.

void FaceEdgeIntersection::forceOntoEdge(unsigned int face,
					 HomogeneityTet *htet)
{
// #ifdef DEBUG
//   if(htet->verboseCategory()) {
//     oofcerr << "FaceEdgeIntersection::forceOntoEdge: this=" << *this
// 	    << std::endl;
//     oofcerr << "FaceEdgeIntersection::forceOntoEdge: eq class="
// 	    << *crnr->equivalence() << std::endl;
//   }
// #endif // DEBUG
  // The closest edge corresponds to the smallest barycentric
  // coordinate component other than the component for the node
  // opposite this face, which should already be zero.
  BarycentricCoord b = htet->getBarycentricCoord(crnr->location3D());
  unsigned int oppNode = CSkeletonElement::oppNode[face];
  double minB = std::numeric_limits<double>::max();
  unsigned int minN = NONE;
  for(unsigned int i=0; i<NUM_TET_NODES; i++) {
    double absb = fabs(b[i]);
    if(i != oppNode && absb < minB) {
      minB = absb;
      minN = i;
    }
  }
  // The point is on the edge that joins the faces that are opposite
  // the nodes oppNode and minN.
  unsigned int face2 = CSkeletonElement::oppFace[minN];
  unsigned int e = CSkeletonElement::faceFaceEdge[face][face2]; // tet scope
  fEdge = CSkeletonElement::tetEdge2FaceEdge[face][e]; // face scope

#ifdef DEBUG
  if(htet->verboseCategory())
    oofcerr << "FaceEdgeIntersection::forceOntoEdge: adding "
	    << *htet->getTetFacePlane(face2) << " to "
	    << *crnr->equivalence() << std::endl;
#endif	// DEBUG
  htet->getTetFacePlane(face2)->addToEquivalence(crnr->equivalence());
  htet->checkEquiv(crnr);

  t = htet->faceEdgeCoord(b, face, fEdge);
  t.normalize();
  // unsigned int node0, node1;
  // getEdgeNodes(face, fEdge, node0, node1);
  // t = b[node1]/(b[node0] + b[node1]);
  // if(t < 0)
  //   t = 0.0;
  // else if(t > 1.0)
  //   t = 1.0;

// #ifdef DEBUG
//   if(htet->verboseCategory()) {
//     oofcerr << "FaceEdgeIntersection::forceOntoEdge: forced onto edge "
// 	    << fEdge << std::endl;
//   }
// #endif // DEBUG
}

// Return the cosine of the angle between the edge and the given edge
// of the face that it's on.  Use the geometry of the planes, rather
// than the endpoints of the edge.

double FaceEdgeIntersection::declination(unsigned int face,
					 unsigned int edge,
					 HomogeneityTet *htet)
  const
{
  const HPlane *pplane = crnr->sharedPlane(remoteCorner(), face);
  // thisDir is a vector in the direction of the segment stored in this
  // FaceEdgeIntersection
  Coord3D thisDir = htet->getTetFacePlane(face)->normal() % pplane->normal();
  // We want the vector to point away from the intersection, so if the
  // end of the segment is at the intersection, reverse it.
  if(!segstart) thisDir *= -1;
  unsigned int n0, n1;
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "FaceEdgeIntersection::declination: calling getEdgeNodes,"
	    << " face=" << face << " edge=" << edge << std::endl;
#endif // DEBUG
  getEdgeNodes(face, edge, n0, n1);
  // edgeDir is in the direction of the tet edge at this FaceEdgeIntersection

#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "FaceEdgeIntersection::declination: n0=" << n0 << " "
	    << htet->nodePosition(n0) << " n1=" << n1 << " "
	    << htet->nodePosition(n1) << std::endl;
#endif // DEBUG
  
  Coord3D edgeDir = htet->nodePosition(n1) - htet->nodePosition(n0);
  // TODO: Use HomogeneityTet::edgeLengths instead of norm2(edgeDir)
  double decl = dot(edgeDir, thisDir)/sqrt(norm2(edgeDir)*norm2(thisDir));
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceEdgeIntersection::declination: " << *this << std::endl;
//     OOFcerrIndent indent(2);
//     oofcerr << "FaceEdgeIntersection::declination: pplane=" << *pplane
// 	    << " normal=" << pplane->normal() << std::endl;
//     oofcerr << "FaceEdgeIntersection::declination: faceplane="
// 	    << *htet->getTetFacePlane(face) << " normal="
// 	    << htet->getTetFacePlane(face)->normal() << std::endl;
//     oofcerr << "FaceEdgeIntersection::declination: thisDir=" << thisDir
// 	    << " norm2=" << norm2(thisDir) << std::endl;
//     oofcerr << "FaceEdgeIntersection::declination: edgeDir=" << edgeDir
// 	    << " norm2=" << norm2(edgeDir) << std::endl;
//     oofcerr << "FaceEdgeIntersection::declination: dot="
// 	    << dot(edgeDir, thisDir) << std::endl;
//     oofcerr << "FaceEdgeIntersection::declination: decl=" << decl << std::endl;
//   }
// #endif // DEBUG
  return decl;
}

bool FaceEdgeIntersection::crossesSameEdge(const FaceEdgeIntersection *other,
					   unsigned int face,
					   const FacePlane *sharedFace,
					   HomogeneityTet *htet
#ifdef DEBUG
					   , bool verbose
#endif // DEBUG
					   ) const
{
  // Does the facet edge that meets the face edge here cross the facet
  // edge that meets the face edge at "other"?

  // The two FaceEdgeIntersections and their FacetEdges lie in the tet
  // face with index 'face'.

  // This routine assumes that both FaceEdgeIntersections are on the
  // same face edge, and that their FacetEdges are distinct and don't
  // share any endpoints.  The 'sharedFace' argument is the other tet
  // face (other than 'face') that shares the face edge containing the
  // intersections.

  // Just calling segIntersection() here is insufficient, because this
  // is likely to be called in cases in which the two edges start very
  // close to one another on the edge of a face, and round-off error
  // can give us the wrong result.  We know more topological
  // information, and have to use it.

  // Get the endpoints that are on the face edge.
  const PlaneIntersection *nearEnd = corner();
  const PlaneIntersection *otherNearEnd = other->corner();
  // Get the endpoints that aren't on the face edge.
  const PlaneIntersection *farEnd = edge_->point(!start());
  const PlaneIntersection *otherFarEnd = other->edge()->point(!other->start());

#ifdef DEBUG
  if(verbose) {
    oofcerr << "FaceEdgeIntersection::crossesSameEdge:  this=" << *this
	    << std::endl;
    oofcerr << "FaceEdgeIntersection::crossesSameEdge: other=" << *other
	    << std::endl;
    oofcerr << "FaceEdgeIntersection::crossesSameEdge: nearEnd=" << *nearEnd
	    <<  " farEnd=" << *farEnd << std::endl;
    oofcerr << "FaceEdgeIntersection::crossesSameEdge: otherNearEnd="
	    << *otherNearEnd << " otherFarEnd=" << *otherFarEnd << std::endl;
  }
#endif // DEBUG

  // Check for parallel edges.  If both edges are formed by pixel
  // planes intersecting the face, then the edges are parallel if the
  // cross product of the normals to the pixel planes is perpendicular
  // to the face normal.  This check probably catches very few cases,
  // but they're cases in which round off error can confuse the
  // declination check, below.  This case could be common when an
  // element has been constructed with faces aligned with the x, y,
  // and z axes, and then one node has been moved, pivoting a face
  // around an axis-aligned edge.  The pivoted face may clip a VSB
  // corner, creating parallel intersection lines.
  const HPixelPlane *pp0 = nearEnd->sharedPixelPlane(farEnd, face);
  const HPixelPlane *pp1 = otherNearEnd->sharedPixelPlane(otherFarEnd, face);
  if(pp0 != nullptr && pp1 != nullptr) {
    Coord3D crossprod = cross(pp0->normal(), pp1->normal());
    // Getting this dot product to be exactly zero is the reason for
    // setting components of the area vectors to zero in the
    // HomogeneityTet constructor.
    if(dot(crossprod, htet->faceAreaVector(face)) == 0.0) {
#ifdef DEBUG
      if(verbose)
	oofcerr << "FaceEdgeIntersection::crosses: edges are parallel!"
		<< std::endl;
#endif // DEBUG
      return false;
    }
  }

  // Which point precedes the other one on the tet edge?  Since one
  // point might be at a tet corner the data in the
  // FaceEdgeIntersection objects has to be interpreted carefully.
  bool firstPt = (faceEdge() == other->faceEdge() ?
		  edgePosition() < other->edgePosition()
		  :
		  (faceEdge()+1)%3 == other->faceEdge()
		  && (edgePosition().atEnd() ||
		      other->edgePosition().atStart()));

//   if(shared == nullptr) {
//     // Since the points aren't on a shared edge, we can't use the
//     // placement of the near end points on the edge to make the
//     // calculation easier. 
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "FaceEdgeIntersection::crosses: using segIntersection"
// 	      << std::endl;
// #endif// DEBUG
//     bool crs = segIntersection(
// 		       nearEnd->location3D(), farEnd->location3D(),
// 		       otherNearEnd->location3D(), otherFarEnd->location3D()
// #ifdef DEBUG
// 		       , verbose
// #endif // DEBUG
// 			   );
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "FaceEdgeIntersection::crosses: returning " << crs
// 	      << std::endl;
// #endif // DEBUG
//     return crs;
//   }

  // sharedE is the face-scope index of the tet edge that's shared by
  // this and the other FaceEdgeIntersection.  It's equal to fEdge if
  // both intersections have the same fEdge, which is true unless one
  // of them is on a corner.
  unsigned int sharedF = htet->getTetFaceIndex(sharedFace);
  unsigned int sharedEtet = CSkeletonElement::faceFaceEdge[face][sharedF];
  unsigned int sharedE = CSkeletonElement::tetEdge2FaceEdge[face][sharedEtet];

#ifdef DEBUG
  if(verbose) {
    oofcerr << "FaceEdgeIntersection::crossesSameEdge:"
	    << " this->edgePosition=" << edgePosition()
	    << " other->edgePosition=" << other->edgePosition() << std::endl;
    oofcerr << "FaceEdgeIntersection::crossesSameEdge: sharedF=" << sharedF
	    << " sharedEtet=" << sharedEtet << " sharedE=" << sharedE
	    << std::endl;
  }
#endif // DEBUG

  // Use FaceEdgeIntersection::declination() to check for
  // diverging segments, and only call segIntersection for converging
  // ones.
  double thisDecl = declination(face, sharedE, htet);
  double otherDecl = other->declination(face, sharedE, htet);
#ifdef DEBUG
  if(verbose)
    oofcerr << "FaceEdgeIntersection::crossesSameEdge: thisDecl=" << thisDecl
	    << " otherDecl=" << otherDecl
	    << " diff=" << thisDecl-otherDecl
	    << " firstPt=" << firstPt << " "
	    << (thisDecl > otherDecl ? "convergent" : "divergent")
	    << std::endl;
#endif // DEBUG
  if((firstPt && thisDecl > otherDecl) || (!firstPt && otherDecl>thisDecl))
    {
      // The segments might cross because they converge inside the tet
      // face.
      double alpha = 0.0;  // position of crossing point on this edge
      double beta = 0.0;   // position of crossing point on other edge
      bool parallel = false;
      (void) segIntersection(nearEnd->location3D(), farEnd->location3D(),
			     otherNearEnd->location3D(),
			     otherFarEnd->location3D(),
			     alpha, beta, parallel
#ifdef DEBUG
			     , verbose
#endif // DEBUG
			     );
      // Since we know that the segments both start on the tet edge
      // and head into the face, if alpha<0 or beta<0 it's just due to
      // round off error, and one of them must actually be slightly
      // positive.  This is why we discard the return value of
      // segIntersection, which doesn't know that negative alphas and
      // betas are topologically impossible here.
#ifdef DEBUG
      if(verbose)
	oofcerr << "FaceEdgeIntersection::crossesSameEdge: alpha=" << alpha
		<< " beta=" << beta << " parallel=" << parallel
		<< ", returning " << (!parallel && alpha <= 1.0 && beta <= 1.0)
		<< std::endl;
#endif // DEBUG
      return !parallel && alpha <= 1.0 && beta <= 1.0;
    }
#ifdef DEBUG
    if(verbose)
      oofcerr << "FaceEdgeIntersection::crossesSameEdge:"
	      << " divergent, not crossing" << std::endl;
#endif // DEBUG
    return false;
} // end FaceEdgeIntersection::crossesSameEdge

bool FaceEdgeIntersection::crossesDiffEdge(const FaceEdgeIntersection *other
#ifdef DEBUG
					   , bool verbose
#endif // DEBUG
					   )
  const
{
  double alpha = 0.0;
  double beta = 0.0;
  bool parallel = false;
  (void) segIntersection(corner()->location3D(), remoteCorner()->location3D(),
			 other->corner()->location3D(),
			 other->remoteCorner()->location3D(),
			 alpha, beta, parallel
#ifdef DEBUG
			 , verbose
#endif // DEBUG
			 );
  return (!parallel && alpha >= 0.0 && alpha <= 1.0 &&
	  beta >= 0.0 && beta <= 1.0);
}

PlaneIntersection *FaceEdgeIntersection::remoteCorner() const {
  return edge_->point(!segstart);
}

bool FaceEdgeIntersection::samePosition(const FaceEdgeIntersection *other) const
{
  return (faceEdge() == other->faceEdge() &&
	  edgePosition() == other->edgePosition());
}

bool FaceEdgeIntersectionLT::operator()(const FaceEdgeIntersection *a,
					const FaceEdgeIntersection *b)
  const
{
  if(a->faceEdge() < b->faceEdge())
    return true;
  if(a->faceEdge() > b->faceEdge())
    return false;
  return a->edgePosition() < b->edgePosition();
}

bool FaceEdgeIntersectionLTwrap::operator()(const FaceEdgeIntersection *a,
					    const FaceEdgeIntersection *b)
  const
{
  if(a->faceEdge() == b->faceEdge())
    return a->edgePosition() < b->edgePosition();
  if((a->faceEdge()+1) % NUM_TET_FACE_EDGES == b->faceEdge())
    return true;
  assert((b->faceEdge()+1) % NUM_TET_FACE_EDGES == a->faceEdge());
  return false;
}

std::ostream &operator<<(std::ostream &os, const FaceEdgeIntersection &fei) {
  os << "FaceEdgeIntersection(" << *fei.corner()
     << ", " << *fei.remoteCorner()
     << ", fedge=" << fei.faceEdge()
     << ", t=" << fei.edgePosition()
     << ", start=" << fei.start() << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FaceFacetEdge::FaceFacetEdge(HomogeneityTet *htet,
			     const PlaneIntersection *s,
			     const PlaneIntersection *e,
			     const HPixelPlane *pp)
  : start_(s->clone(htet)),
    stop_(e->clone(htet)),
    pixplane_(pp),
    id(htet->nextFaceFacetEdgeID())
{
// #ifdef DEBUG
//   oofcerr << "FaceFacetEdge::ctor 1: " << *this << std::endl;
// #endif // DEBUG
}

FaceFacetEdge::FaceFacetEdge(HomogeneityTet *htet,
			     const PlaneIntersection *s,
			     const PlaneIntersection *e)
  : start_(s->clone(htet)),
    stop_(e->clone(htet)),
    pixplane_(nullptr),
    id(htet->nextFaceFacetEdgeID())
{
// #ifdef DEBUG
//   oofcerr << "FaceFacetEdge::ctor 2: " << *this << std::endl;
// #endif // DEBUG
}

FaceFacetEdge::~FaceFacetEdge() {
// #ifdef DEBUG
//   oofcerr << "FaceFacetEdge::dtor: " << this << std::endl;
// #endif // DEBUG
  delete start_;
  delete stop_;
}

FaceFacetEdge::FaceFacetEdge(FaceFacetEdge &&ffe) {
  PlaneIntersection *temp = start_;
  start_ = ffe.start_;
  ffe.start_ = temp;
  temp = stop_;
  stop_ = ffe.stop_;
  ffe.stop_ = temp;
  ffe.id = id;
}

Coord3D FaceFacetEdge::startPos3D() const {
  return start_->location3D();
}

Coord3D FaceFacetEdge::endPos3D() const {
  return stop_->location3D();
}

PlaneIntersection *FaceFacetEdge::replacePoint(PlaneIntersection *pt,
					       HomogeneityTet *htet,
					       bool start)
{
  PlaneIntersection *bozo = pt->clone(htet);
  if(start) {
// #ifdef DEBUG
//     oofcerr << "FacetEdge::replacePoint: replacing " << *start_ << " with "
// 	    << *pt << std::endl;
//     oofcerr << "FacetEdge::replacePoint: edge is now " << *this << std::endl;
// #endif // DEBUG
    start_ = bozo;
  }
  else {
// #ifdef DEBUG
//     oofcerr << "FacetEdge::replacePoint: replacing " << *stop_ << " with "
// 	    << *pt << std::endl;
//     oofcerr << "FacetEdge::replacePoint: edge is now " << *this << std::endl;
// #endif // DEBUG
    stop_ = bozo;
  }
  return bozo;
}

bool FaceFacetEdge::operator<(const FaceFacetEdge &other) const {
  return id < other.id;
}

std::ostream &operator<<(std::ostream &os, const FaceFacetEdge &edge) {
  os << "[" << *edge.startPt() << ", " << *edge.endPt() << " pixplane=";
  if(edge.pixelPlane() != nullptr)
    os << *edge.pixelPlane();
  else
    os << "null";
  os << ", length=" << sqrt(norm2(edge.startPt()->location3D() -
				  edge.endPt()->location3D()))
     << "]";
  return os;
}

bool FaceFacetEdge::isNull() const {
  return start_->isEquivalent(stop_);
}

// Does this edge lie along an edge of the given tet face?
unsigned int FaceFacetEdge::findFaceEdge(unsigned int face,
					 HomogeneityTet *htet)
  const
{
  // It lies on an edge of the face if the start and end points share
  // a face that's not the given face.
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacetEdge::findFaceEdge: this=" << *this << std::endl;
//     oofcerr << "FaceFacetEdge::findFaceEdge: face=" << face << " "
// 	    << htet->getTetFacePlane(face) << " "
// 	    << *htet->getTetFacePlane(face) << std::endl;
//   }
// #endif // DEBUG
  const FacePlane *fp = start_->sharedFace(stop_, htet->getTetFacePlane(face));
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacetEdge::findFaceEdge: fp=" << fp;
//     if(fp)
//       oofcerr << " " << *fp;
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
  if(fp == nullptr)
    return NONE;
  unsigned int otherFace = htet->getTetFaceIndex(fp);
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacetEdge::findFaceEdge: otherFace=" << otherFace
// 	    << std::endl;
//   }
// #endif // DEBUG
  assert(face != otherFace);
  unsigned int edge = CSkeletonElement::faceFaceEdge[face][otherFace];
  return CSkeletonElement::tetEdge2FaceEdge[face][edge];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FaceFacet::~FaceFacet() {
  for(FaceFacetEdge *edge : edges_)
    delete edge;
}

void FaceFacet::clear() {
  for(FaceFacetEdge *edge : edges_)
    delete edge;
  edges_.clear();
  areaComputed = false;
  closedOnPerimeter = false;
}

void FaceFacet::addEdge(FaceFacetEdge *edge) {
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::addEdge: face=" << face << " adding " << *edge;
    if(edge->isNull())
      oofcerr << " ** null edge! **";
    oofcerr << std::endl;
  }
#endif // DEBUG
  if(edge->isNull())
    return;
  areaComputed = false;
  edges_.insert(edge);
}

// addFaceEdges joins the two given intersections by adding edges
// around the perimeter of the face.

void FaceFacet::addFaceEdges(const FaceEdgeIntersection *fei0,
			     const FaceEdgeIntersection *fei1,
			     HomogeneityTet *htet)
{
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::addFaceEdges: fei0=" << *fei0 << std::endl;
    oofcerr << "FaceFacet::addFaceEdges: fei1=" << *fei1 << std::endl;
  }
#endif // DEBUG
  
  unsigned int startEdge = fei0->faceEdge();
  unsigned int endEdge = fei1->faceEdge();
  
  if(startEdge == endEdge && fei0->edgePosition() < fei1->edgePosition()) {
    // The intersection points are on the same tet edge and in the
    // right order to be joined by a single segment.
    addEdge(new FaceFacetEdge(
	      htet,
	      fei0->corner()->clone(htet),
	      fei1->corner()->clone(htet)));
  }
  else {
    // The intersection points are on different tet edges, or
    // backwards on the same edge.  nwrap is the number of corners we
    // go around to get from fei0 to fei1.

    // TODO: There are duplicate calls to checkEquiv here.  Call it
    // once, and then clone the intersection.
    
    int nwrap = (NUM_TET_FACE_EDGES + endEdge - startEdge) % NUM_TET_FACE_EDGES;
    if(nwrap == 1) {
      // e0 is the tet-scope index of this edge
      unsigned int e0 = CSkeletonElement::faceEdges[face][startEdge];
      // e1 is the tet-scope index of the next edge on the face
      unsigned int e1 = CSkeletonElement::faceEdges[face][endEdge];
      // node is the index of the node at the junction of e0 and e1
      unsigned int node = CSkeletonElement::edgeEdgeNode[e0][e1];
      addEdge(new FaceFacetEdge(
		htet,
		fei0->corner()->clone(htet),
		htet->checkEquiv(new TripleFaceIntersection(node, htet))));
      addEdge(new FaceFacetEdge(
		htet,
		htet->checkEquiv(new TripleFaceIntersection(node, htet)),
		fei1->corner()->clone(htet)));
    }
    else if(nwrap == 2) {	// There are two corners to go around.
      unsigned int e0 = CSkeletonElement::faceEdges[face][startEdge];
      unsigned int e1 = CSkeletonElement::faceEdges[face][(startEdge+1)%3];
      unsigned int e2 = CSkeletonElement::faceEdges[face][endEdge];
      unsigned int node01 = CSkeletonElement::edgeEdgeNode[e0][e1];
      unsigned int node12 = CSkeletonElement::edgeEdgeNode[e1][e2];
      addEdge(new FaceFacetEdge(
		htet,
		fei0->corner()->clone(htet),
		htet->checkEquiv(new TripleFaceIntersection(node01, htet))));
      addEdge(new FaceFacetEdge(
		htet,
		htet->checkEquiv(new TripleFaceIntersection(node01, htet)),
		htet->checkEquiv(new TripleFaceIntersection(node12, htet))));
      addEdge(new FaceFacetEdge(
		htet,
		htet->checkEquiv(new TripleFaceIntersection(node12, htet)),
		fei1->corner()->clone(htet)));
	      
    }
    else if(nwrap == 0) {
      // There are three corners to go around.  nwrap==0 instead of 3
      // because it was computed mod 3.
#ifdef DEBUG
      if(nwrap != 0) {
	oofcerr << "FaceFacet::addFaceEdges: expected nwrap= 0, 1 or 2, got "
		<< nwrap << std::endl;
	oofcerr << "FaceFacet::addFaceEdges: fei0=" << *fei0 << std::endl;
	oofcerr << "FaceFacet::addFaceEdges: fei1=" << *fei1 << std::endl;
	throw ErrProgrammingError("addFaceEdges failed!", __FILE__, __LINE__);
      }
#endif // DEBUG
      unsigned int e0 = CSkeletonElement::faceEdges[face][startEdge];
      unsigned int e1 = CSkeletonElement::faceEdges[face][(startEdge+1)%3];
      unsigned int e2 = CSkeletonElement::faceEdges[face][(startEdge+2)%3];
      unsigned int node01 = CSkeletonElement::edgeEdgeNode[e0][e1];
      unsigned int node12 = CSkeletonElement::edgeEdgeNode[e1][e2];
      unsigned int node20 = CSkeletonElement::edgeEdgeNode[e2][e0];
      addEdge(new FaceFacetEdge(
		htet,
		fei0->corner()->clone(htet),
		htet->checkEquiv(new TripleFaceIntersection(node01, htet))));
      addEdge(new FaceFacetEdge(
		htet,
		htet->checkEquiv(new TripleFaceIntersection(node01, htet)),
		htet->checkEquiv(new TripleFaceIntersection(node12, htet))));
      addEdge(new FaceFacetEdge(
		htet,
		htet->checkEquiv(new TripleFaceIntersection(node12, htet)),
		htet->checkEquiv(new TripleFaceIntersection(node20, htet))));
      addEdge(new FaceFacetEdge(
		htet,
		htet->checkEquiv(new TripleFaceIntersection(node20, htet)),
		fei1->corner()->clone(htet)));
    }
  }
  closedOnPerimeter = true;
} // end FaceFacet::addFaceEdges

Coord3D FaceFacet::area(HomogeneityTet *htet) const {
  if(!areaComputed) {
    areaVec_ = getArea(htet);
    areaComputed = true;
  }
  return areaVec_;
}

void FaceFacet::removeOpposingEdges() {
  // Equal but opposite segments, have a net zero contribution to the
  // area, but if they're the only segments and they're included in
  // the area calculation, roundoff error might make the area
  // negative, which will cause the entire perimeter to be included
  // erroneously.
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacet::removeOpposingEdges: initial facet=" << std::endl;
//     std::cerr << *this << std::endl;
//   }
// #endif // DEBUG
  auto edge0 = edges_.begin();
  while(edge0 != edges_.end()) {
    auto edge1 = edge0;
    ++edge1;
    bool matched = false;
    for( ; edge1 != edges_.end(); ++edge1) {
      if((*edge0)->startPt()->isEquivalent((*edge1)->endPt()) &&
	 (*edge1)->startPt()->isEquivalent((*edge0)->endPt()))
	{
	  // Save an iterator to the next edge before erasing edge0
	  // and edge1.
	  auto nextedge = edge0;
	  ++nextedge;
	  if(nextedge == edge1)
	    ++nextedge;
	  delete *edge0;
	  delete *edge1;
	  edges_.erase(edge0);
	  edges_.erase(edge1);
	  edge0 = nextedge;
	  matched = true;
	  break;
	}
    }
    if(!matched)
      ++edge0;
  }
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacet::removeOpposingEdges: final facet=" << std::endl;
//     std::cerr << *this << std::endl;
//   }
// #endif // DEBUG
}

Coord3D FaceFacet::getArea(HomogeneityTet *htet) const {
  Coord3D a;
  Coord3D fcenter = htet->faceCenter(face);
  for(const FaceFacetEdge *edge : edges_) {
    if(!edge->isNull()) {
      a += (edge->startPos3D() - fcenter) % (edge->endPos3D() - fcenter);
    }
// #ifdef DEBUG
//     else {
//       oofcerr << "FaceFacet::getArea: this=" << *this << std::endl;
//       oofcerr << "FaceFacet::getArea: ignoring edge: " << *edge << std::endl;
//     }
// #endif // DEBUG
  }
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     Coord3D tetfacearea = htet->faceAreaVector(face);
//     Coord3D norm = tetfacearea/sqrt(norm2(tetfacearea));
//     oofcerr << "FaceFacet::getArea(): " << *htet->getTetFacePlane(face)
// 	    << " A=" << 0.5*a << " (" << dot(0.5*a, norm) << ")" << std::endl;
//   }
// #endif // DEBUG
  return 0.5*a;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void FaceFacet::findLooseEnds(LooseEndSet &looseEnds,
			      std::vector<StrandedPoint> &strandedPoints)
  const
{
  unsigned int nsegs = edges_.size();

  // Construct lists of start and end points of the existing segments.
  std::vector<FaceEdgeIntersection*> startPoints;
  std::vector<FaceEdgeIntersection*> endPoints;
  startPoints.reserve(nsegs);
  endPoints.reserve(nsegs);
  for(auto seg=edges_.begin(); seg!=edges_.end(); ++seg) {
    startPoints.push_back(
		htet->newFaceEdgeIntersection((*seg)->startPt(), *seg, true));
    endPoints.push_back(
		htet->newFaceEdgeIntersection((*seg)->endPt(), *seg, false));
  }
#ifdef DEBUG
  if(htet->verboseFace()) {
    // At this point, fEdge hasn't been set in the
    // FaceEdgeIntersection objects, so don't be surprised by the
    // printed value.
    oofcerr << "FaceFacet::findLooseEnds: face=" << face << std::endl;
    oofcerr << "FaceFacet::findLooseEnds: startPoints="
	    << std::endl;
    for(const auto p: startPoints) {
      OOFcerrIndent indent(2);
      oofcerr << "FaceFacet::findLooseEnds: " << *p << std::endl;
    }
    oofcerr << "FaceFacet::findLooseEnds: endPoints="
	    << std::endl;
    for(const auto p: endPoints) {
      OOFcerrIndent indent(2);
      oofcerr << "FaceFacet::findLooseEnds: " << *p << std::endl;
    }
  }
  if(!htet->verify())
    throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
#endif // DEBUG

  // Match up existing start and end points.
  std::vector<bool> matchedStarts(nsegs, false);
  std::vector<bool> matchedEnds(nsegs, false);
  for(unsigned int s=0; s<nsegs; s++) {
    for(unsigned int e=0; e<nsegs; e++) {
      if(!matchedEnds[e] &&
	 startPoints[s]->corner()->isEquivalent(endPoints[e]->corner()))
	{
	  matchedStarts[s] = true;
	  matchedEnds[e] = true;
	  break;		// don't match this s with another e
	}
    } // end loop over end points e
  } // end loop over start points s

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::findLooseEnds: matchedStarts=";
    std::cerr << matchedStarts;
    oofcerr << std::endl;
    oofcerr << "FaceFacet::findLooseEnds:   matchedEnds=";
    std::cerr << matchedEnds;
    oofcerr << std::endl;
  }
#endif // DEBUG

  // All of the truly unmatched points must be on tet edges.  Sort
  // them by edge and intersection position along the edge by
  // inserting them into the LooseEndMaps.  The unmatched points that
  // don't appear to be on an edge are "stranded".
  for(unsigned int i=0; i<nsegs; i++) {
    if(!matchedStarts[i]) {
      startPoints[i]->findFaceEdge(face, htet);
      unsigned int edge = startPoints[i]->faceEdge();
      if(edge != NONE) {
	looseEnds.insert(startPoints[i]);
      }
      else
	strandedPoints.emplace_back(startPoints[i], face);
    }
    if(!matchedEnds[i]) {
      endPoints[i]->findFaceEdge(face, htet);
      unsigned int edge = endPoints[i]->faceEdge();
      if(edge != NONE) {
	looseEnds.insert(endPoints[i]);
      }
      else {
	strandedPoints.emplace_back(endPoints[i], face);
      }
    }
  }
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacet::findLooseEnds: loose ends, face=" << face
// 	    << std::endl;
//     OOFcerrIndent indent(2);
//     for(auto leptr : looseEnds)
//       oofcerr << "FaceFacet::findLooseEnds: " << *leptr << std::endl;
//   }
// #endif // DEBUG

} // end FaceFacet::findLooseEnds


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// getAreaCarefully looks for sets of three linked facet edges that
// form a triangle with very small area, either positive or negative.
// The expected sign of the area can be found by examining the three
// pixel planes (they must be pixel planes) that form the triangle. If
// the computed area has the wrong sign, it's set to zero.

class FaceFacetLoop {
public:
  FaceFacetLoop(const FaceFacetEdge *e);
  std::set<const FaceFacetEdge*> edges;
  void addEdge(const FaceFacetEdge *e) { edges.insert(e); }
  void merge(const FaceFacetLoop*);
  Coord3D area(const FaceFacet*, HomogeneityTet*) const;
};

std::ostream &operator<<(std::ostream &os, const FaceFacetLoop &loop) {
  os << "FaceFacetLoop(" << std::endl;
  for(const FaceFacetEdge *edge : loop.edges)
    os << "      " << *edge << std::endl;
  os << ")";
  return os;
}

FaceFacetLoop::FaceFacetLoop(const FaceFacetEdge *e) {
  edges.insert(e);
}

void FaceFacetLoop::merge(const FaceFacetLoop *other) {
  for(const FaceFacetEdge *edge : other->edges)
    addEdge(edge);
}

Coord3D FaceFacetLoop::area(const FaceFacet *ffacet, HomogeneityTet *htet)
  const
{
  if(edges.size() < 3)
    return Coord3D(0.0, 0.0, 0.0);
  // Compute the area of the loop.  This is the same calculation used
  // in FaceFacet::getArea.
  Coord3D a;
  Coord3D fcenter = htet->faceCenter(ffacet->face);
  for(const FaceFacetEdge *edge : edges) {
    if(!edge->isNull())
      a += (edge->startPos3D() - fcenter) % (edge->endPos3D() - fcenter);
  }
  a *= 0.5;
  if(edges.size() > 3) {
    // TODO: Is it possible that the infinitesimally protruding VSB
    // corner is clipped by a different tet face (or two) so the loop
    // has 4 (or five) edges?  Or have all of those cases been caught
    // by the closedOnPerimeter check in fixNonPositiveArea?
    return a;
  }

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacetLoop::area: edges=" << std::endl;
    OOFcerrIndent indent(2);
    for(const FaceFacetEdge *edge : edges)
      oofcerr << "FaceFacetLoop::area: " << *edge << std::endl;
  }
#endif // DEBUG

  // There are exactly three edges.  The loop may be due to a VSB
  // corner formed by three pixel planes protruding infinitesimally
  // through the face, and round off error may lead to an area with
  // the incorrect sign.  Use only topological information to get the
  // expected sign of the area.

  // The three *oriented* pixel planes can meet to form either a
  // convex or concave corner.  If it's convex (all normals pointing
  // outward), then the facet loop should have a positive area, and if
  // it's concave, the loop should have a negative area.  (We don't
  // need to consider cases in which the normals don't all point
  // either outward or inward, because they won't lead to small
  // loops.)  We don't have to compute the concavity, though.  The
  // sum, N, of the normals of the planes points towards the outside
  // of the voxel set.  If that's in the same direction as the normal
  // to the face, F, then the area is positive if the intersection
  // point is outside the tet and negative if it's inside.  If N is
  // oppositely directed to F, the relationship is reversed.

  // We don't expect N dot F to be near zero, because why? I dunno.

  // Find the point at which the three pixel planes intersect.
  std::vector<const HPixelPlane*> pplanes;
  pplanes.reserve(3);
  for(const FaceFacetEdge* edge : edges) {
    const HPixelPlane *pixplane = edge->pixelPlane();
    if(pixplane == nullptr) {
      // If one of the bounding planes is a tet face, then this
      // triangle has already been checked by the coincidence checking
      // routines (fixTents, probably).
      return a;
    }
    pplanes.push_back(edge->pixelPlane());
  }
  // The three planes can fail to be in different directions if the
  // VSB just grazes a corner of the tet.
  if(pplanes[0]->direction() == pplanes[1]->direction() ||
     pplanes[1]->direction() == pplanes[2]->direction() ||
     pplanes[2]->direction() == pplanes[0]->direction())
    {
      return Coord3D(0.0, 0.0, 0.0);
    }
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "FaceFacetLoop::area: calling triplePlaneIntersection"
	    << std::endl;
#endif // DEBUG
  Coord3D vertex = triplePlaneIntersection(pplanes[0], pplanes[1], pplanes[2]);
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "FaceFacetLoop::area: back from triplePlaneIntersection, vertex="
	    << vertex << std::endl;
#endif // DEBUG
  BarycentricCoord bvertex = htet->getBarycentricCoord(vertex);
  // Is the intersection point of the pixel planes inside the tet?
  bool interior = bvertex.interior();

  // Find the direction of the VSB corner. This is a vector that at
  // the intersection point points from the interior of the voxel
  // category towards the exterior.
  Coord3D N;
  for(const HPixelPlane *plane : pplanes)
    N += plane->normal();

  double NdotF = dot(N, htet->faceAreaVector(ffacet->face));
  // a is a vector too... we really want the sign of its normal component.
  double adotF = dot(a, htet->faceAreaVector(ffacet->face));
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacetLoop::area: vertex=" << vertex << " " << bvertex
	    << " " << (interior? "interior" : "exterior") << std::endl;
    oofcerr << "FaceFacetLoop::area: N=" << N << " NdotF=" << NdotF
	    << std::endl;
    oofcerr << "FaceFacetLoop::area: a=" << a << " adotF=" << adotF
	    << std::endl;
  }
#endif // DEBUG
  if(NdotF > 0) {
    if((interior && adotF < 0) || (!interior && adotF > 0))
      return a;
  }
  if(NdotF < 0) {
    if((interior && adotF > 0) || (!interior && adotF < 0))
      return a;
  }
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "FaceFacetLoop::area: detected bad topology, returning 0"
	    << std::endl;
#endif // DEBUG
  return Coord3D(0.0, 0.0, 0.0);
}

Coord3D FaceFacet::getAreaCarefully(HomogeneityTet *htet) const {
  // First find sets of connected edges and compute their area.  These
  // maps map the equivalence classes of the loose starts and end to
  // the FaceFacetLoops that they belong to.

  // The data structures constructed here are somewhat redundant with
  // those used in HomogeneityTet::findFaceFacets, et al.  They could
  // be constructed earlier, but since they're not necessary in most
  // situtations, it is probably cheaper to reconstruct them here
  // rather than to build them earlier and save them.
  std::map<const IsecEquivalenceClass*, FaceFacetLoop*> starts;
  std::map<const IsecEquivalenceClass*, FaceFacetLoop*> ends;
  std::set<FaceFacetLoop*> loops;
  for(const FaceFacetEdge *edge : edges_) {
    if(!edge->isNull()) {
      auto findEnd = ends.find(edge->startPt()->equivalence());
      auto findStart = starts.find(edge->endPt()->equivalence());
      if(findEnd == ends.end() && findStart == starts.end()) {
	// This edge doesn't match any loose ends.  Start a new loop.
	FaceFacetLoop *newLoop = new FaceFacetLoop(edge);
	loops.insert(newLoop);
	starts[edge->startPt()->equivalence()] = newLoop;
	ends[edge->endPt()->equivalence()] = newLoop;
      }
      else if(findEnd == ends.end()) {
	// The end point of this edge matches an existing loop start.
	findStart->second->addEdge(edge);
	starts[edge->startPt()->equivalence()] = findStart->second;
	starts.erase(findStart);
      }
      else if(findStart == starts.end()) {
	// The start point of this edge matches an existing loop end.
	findEnd->second->addEdge(edge);
	ends[edge->endPt()->equivalence()] = findEnd->second;
	ends.erase(findEnd);
      }
      else {
	// Both the start and end points of this edge match existing
	// loop endpoints.
	if(findEnd->second == findStart->second) {
	  // This edge closes the loop!
	  findEnd->second->addEdge(edge);
	}
	else {
	  // This edge joins two loops.
	  findEnd->second->addEdge(edge);
	  findEnd->second->merge(findStart->second);
	  loops.erase(findStart->second);
	}
	starts.erase(findStart);
	ends.erase(findEnd);
      }
    } // end if edge is not null (both ends equivalent
  } // end loop over edges of the facet

#ifdef DEBUG
  if(!starts.empty() || !ends.empty()) {
    oofcerr << "FaceFacet::getAreaCarefully: starts or ends don't match!"
	    << std::endl;
    oofcerr << "FaceFacet::getAreaCarefully: this=" << *this << std::endl;
    oofcerr << "FaceFacet::getAreaCarefully: starts=" << std::endl;
    for(auto x : starts)
      oofcerr << "                  " << *x.first << ": " << *x.second
	      << std::endl;
    oofcerr << "FaceFacet::getAreaCarefully: ends=" << std::endl;
    for(auto x : ends)
      oofcerr << "                  " << *x.first << ": " << *x.second
	      << std::endl;
  }
#endif // DEBUG
  assert(starts.empty());
  assert(ends.empty());

  Coord3D carefulArea;
  
  // Get area (carefully) from each loop.
  for(FaceFacetLoop *loop : loops) {
    carefulArea += loop->area(this, htet);
    delete loop;
  }

  return carefulArea;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// FaceFacet::fixNonPositiveArea is called after all the pixel facet
// edges on the face have been located and joined.  If the facet area
// is zero and there are no facet edges on the face, it's either
// because the face is in the wrong category or because *all* of the
// face is in the right category.  The area can also be zero if there
// are one or more pairs of oppositely directed but otherwise equal
// edges on a face, which happens if the face grazes one or more voxel
// edges. In either case, we have to add edges for the entire
// perimeter if the whole face is in the category.

// We also have to add edges for the entire perimeter if the computed
// area is *negative*.  The area can be negative only if the entire
// perimeter of the face is in the target category, but there are
// islands of another category inside the face.

// It's also necessary to check for roundoff error that can make a
// very small negative area appear to be positive, or vice versa.
// MIN_AREA_TOL (in units of a pixel area) is the threshold at which
// this test is applied.  Making it too small may cause errors.
// Making it too large will cause extra work.  It should be a (small)
// fraction of a pixel area.
#define MIN_AREA_TOL 0.01
#define MIN_AREA_TOL2 (MIN_AREA_TOL * MIN_AREA_TOL)

void FaceFacet::fixNonPositiveArea(HomogeneityTet *htet, unsigned int cat)
{
  Coord3D facetArea = area(htet); // vector!
  Coord3D faceArea = htet->faceAreaVector(face);
  // raw_area is not really the area, but the sign is correct.  It
  // would be the area if we divided by norm(faceArea).
  double raw_area = dot(facetArea, faceArea);
  bool homog_face = false;

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::fixNonPositiveArea: face=" << face << " cat="
	    << cat << std::endl;
    oofcerr << "FaceFacet::fixNonPositiveArea: input facet=" << *this
     	    << std::endl;
    oofcerr << "FaceFacet::fixNonPositiveArea: raw_area=" << raw_area
	    << " homog_face=" << homog_face << std::endl;
  }
#endif // DEBUG
  // Negative areas at this point indicate that the edges detected so
  // far are the edges of a "hole" in the middle of the facet, and the
  // entire perimeter of the tet face has to be included.  However, if
  // edges have already been added along the perimeter by
  // addFaceEdges, then parts of the face's perimeter have been
  // included, and the computed area *must* be positive already.  If
  // it's not, it's because of round off error, and it should really
  // be zero.
  if(closedOnPerimeter && raw_area < 0) {
    raw_area = 0.0;
  }
  else if(raw_area*raw_area < MIN_AREA_TOL2 * norm2(faceArea)) {
    raw_area = dot(getAreaCarefully(htet), faceArea);
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "FaceFacet::fixNonPositiveArea: after careful calculation,"
	      << " raw_area=" << raw_area << std::endl;
#endif // DEBUG
  }
  if(raw_area == 0.0) {
    // There are no edges on the facet (or there are only mutually
    // counteroriented pairs of edges).  The face is homogeneous.
    // Look at the voxel in the center to see if the whole face is in
    // our category and therefore needs to be included.
    ICoord3D testVxl = htet->testVoxel(face);
    // TODO: Some compilers complain about comparison between signed
    // and unsigned ints here.  See the TODO in cmicrostructure.h
    // about using unsigned ints for voxel categories.
    homog_face = htet->microstructure->category(testVxl) == cat;
// #ifdef DEBUG
//     if(htet->verboseFace()) {
//       oofcerr << "FaceFacet::fixNonPositiveArea: testVxl=" << testVxl
// 	      << " cat=" << htet->microstructure->category(testVxl)
// 	      << " homog_face=" << homog_face << std::endl;
//     }
// #endif	// DEBUG
  }
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::fixNonPositiveArea: raw_area=" << raw_area
	    << " homog_face=" << homog_face << std::endl;
  }
#endif // DEBUG
  if(raw_area < 0.0 || homog_face) {
    unsigned int n0 = CSkeletonElement::getFaceArray(face)[0];
    unsigned int n1 = CSkeletonElement::getFaceArray(face)[1];
    unsigned int n2 = CSkeletonElement::getFaceArray(face)[2];
    addEdge(new FaceFacetEdge(
		      htet,
		      htet->checkEquiv(new TripleFaceIntersection(n0, htet)),
		      htet->checkEquiv(new TripleFaceIntersection(n1, htet))));
    addEdge(new FaceFacetEdge(
		      htet,
		      htet->checkEquiv(new TripleFaceIntersection(n1, htet)),
		      htet->checkEquiv(new TripleFaceIntersection(n2, htet))));
    addEdge(new FaceFacetEdge(
		      htet,
		      htet->checkEquiv(new TripleFaceIntersection(n2, htet)),
		      htet->checkEquiv(new TripleFaceIntersection(n0, htet))));
  }
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacet::fixNonPositiveArea: final facet=" << *this
//      	    << std::endl;
//   }
// #endif // DEBUG
} // FaceFacet::fixNonPositiveArea

std::ostream &operator<<(std::ostream &os, const FaceFacet &facet) {
  os << "FaceFacet(face=" << facet.face;
  if(facet.empty())
    os << ")";
  else {
    os << "," << std::endl;
    for(auto edge=facet.edges().begin(); edge!=facet.edges().end(); ++edge) {
      os << "   " << **edge << std::endl;
    }
    os << "    )";
  }
  return os;
}

#ifdef DEBUG

void FaceFacet::dump(std::string basename, unsigned int cat) const {
  std::string filename = (basename + to_string(face) +
			  "cat" + to_string(cat) + ".lines");
 
  oofcerr << "FaceFacet::dump: writing " << filename << std::endl;
  std::ofstream file(filename);
  for(const FaceFacetEdge *edge : edges_) {
    file << edge->startPos3D() << ", " << edge->endPos3D()
	 << " # " << edge->startPt()->shortName() << " --> "
	 << edge->endPt()->shortName() << std::endl;
  }
  file.close();
}

std::string FaceFacet::shortDescription() const {
  std::string result;
  std::string spaces = "   ";
  for(const FaceFacetEdge *edge : edges_)
    result += (spaces + to_string(edge->startPos3D()) + ", " +
	       to_string(edge->endPos3D()) + '\n');
  return result;
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The naive way to compare two EdgePositions would be to compare
// EdgePosition::position for the non-reversed EdgePositions to
// 1-EdgePosition::position for the reversed EdgePositions.  This is a
// bad idea because if the two points are actually very close (eg,
// computed from two different intersection plane representations of a
// single point and only differing by round-off error) subtracting
// from 1 can change the round-off, and the order of the points might
// change.  It's important to avoid the subtraction when possible.

// The two EdgePositions being compared will usually be on the same
// edge and computed by SingleFaceMixIn::getPolyFrac, so their
// "reversed" flags will be the same.  The only situations in which
// the "reversed" flags will differ is when one of the EdgePositions
// was computed by MultiFaceMixin::getPolyFrac, in which case its
// position is either 0 or 1, which we can safely subtract from 1
// without roundoff error.

bool EdgePosition::operator<(const EdgePosition &other) const {
  if(reversed == other.reversed) {
    if(reversed)
      return position > other.position;
    return position < other.position;
  }
  // reversed != other.reversed
  if(position == 0.0 || position == 1.0) {
    if(reversed)
      return 1-position < other.position;
    return 1-position > other.position;
  }
  else if(other.position == 0.0 || other.position == 1.0) {
    if(reversed)
      return position > 1-other.position;
    return position < 1-other.position;
  }
  // reversed != other.reversed and neither position is 0 or 1
  if(reversed)
    return position > (other.reversed ? other.position : (1-other.position));
  return position < (other.reversed ? (1-other.position) : other.position);
}

bool EdgePosition::operator<=(const EdgePosition &other) const {
  if(reversed == other.reversed) {
    if(reversed)
      return position >= other.position;
    return position <= other.position;
  }
  // reversed != other.reversed
  if(position == 0.0 || position == 1.0) {
    if(reversed)
      return 1-position <= other.position;
    return 1-position >= other.position;
  }
  else if(other.position == 0.0 || other.position == 1.0) {
    if(reversed)
      return position >= 1-other.position;
    return position <= 1-other.position;
  }
  // reversed != other.reversed and neither position is 0 or 1
  if(reversed)
    return position >= (other.reversed ? other.position : (1-other.position));
  return position <= (other.reversed ? (1-other.position) : other.position);
}

bool EdgePosition::operator>(const EdgePosition &other) const {
  if(reversed == other.reversed) {
    if(reversed)
      return position < other.position;
    return position > other.position;
  }
  // reversed != other.reversed
  if(position == 0.0 || position == 1.0) {
    if(reversed)
      return 1-position > other.position;
    return 1-position < other.position;
  }
  else if(other.position == 0.0 || other.position == 1.0) {
    if(reversed)
      return position < 1-other.position;
    return position > 1-other.position;
  }
  // reversed != other.reversed and neither position is 0 or 1
  if(reversed)
    return position < (other.reversed ? other.position : (1-other.position));
  return position > (other.reversed ? (1-other.position) : other.position);
}

bool EdgePosition::operator>=(const EdgePosition &other) const {
  if(reversed == other.reversed) {
    if(reversed)
      return position <= other.position;
    return position >= other.position;
  }
  // reversed != other.reversed
  if(position == 0.0 || position == 1.0) {
    if(reversed)
      return 1-position >= other.position;
    return 1-position <= other.position;
  }
  else if(other.position == 0.0 || other.position == 1.0) {
    if(reversed)
      return position <= 1-other.position;
    return position >= 1-other.position;
  }
  // reversed != other.reversed and neither position is 0 or 1
  if(reversed)
    return position <= (other.reversed ? other.position : (1-other.position));
  return position >= (other.reversed ? (1-other.position) : other.position);
}

bool EdgePosition::operator==(const EdgePosition &other) const {
  if(reversed == other.reversed)
    return position == other.position;
  if(position == 0.0 || position == 1.0)
    return 1-position == other.position;
  return position == 1-other.position;
}

double EdgePosition::operator-(const EdgePosition &other) const {
  if(reversed == other.reversed) {
    double diff = position - other.position;
    if(reversed)
      return -diff;
    return diff;
  }
  if(reversed)
    return (1-position) - other.position;
  return position - (1-other.position);
}

bool EdgePosition::atStart() const {
  return reversed ? position == 1.0 : position == 0.0;
}

bool EdgePosition::atEnd() const {
  return reversed ? position == 0.0 : position == 1.0;
}

void EdgePosition::normalize() {
  if(position < 0.0)
    position = 0.0;
  else if(position > 1.0)
    position = 1.0;
}

void EdgePosition::forceToEnd() {
  // This should never be called unless position is already close to 0
  // or 1.
  assert(position < 0.1 || position > 0.9);
  if(position < 0.5)
    position = 0.0;
  else
    position = 1.0;
}

std::ostream &operator<<(std::ostream &os, const EdgePosition &ep) {
  if(ep.reversed)
    os << "1-" << ep.position;
  else
    os << ep.position;
  if(ep.atStart())
    os << "(start)";
  if(ep.atEnd())
    os << "(end)";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

