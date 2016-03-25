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

#include "common/tostring.h"
#include "engine/cskeletonelement.h"
#include "engine/homogeneitytet.h"
#include "engine/pixelplanefacet.h"
#include "engine/planeintersection.h"

#include <algorithm>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

BarycentricCoord PlaneIntersection::baryCoord(const HomogeneityTet *htet) const
{
  return htet->getBarycentricCoord(location3D());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TripleFaceIntersection is the intersection of three tetrahedron
// faces.

TripleFaceIntersection::TripleFaceIntersection(unsigned int node,
					       const HomogeneityTet *htet)
  : node_(node)
{
  for(unsigned int i=0; i<3; i++)
    faces_.insert(htet->getFacePlane(CSkeletonElement::nodeFaces[node][i]));
  loc_ = htet->nodePosition(node);
}

TripleFaceIntersection *TripleFaceIntersection::clone() const {
  return new TripleFaceIntersection(*this);
}

BarycentricCoord TripleFaceIntersection::baryCoord(const HomogeneityTet *htet)
  const
{
  return nodeBCoord(node_);
}

void TripleFaceIntersection::print(std::ostream &os) const {
  os << "TripleFaceIntersection(node=" << node_ << ", " << location3D() << ")";
}

unsigned int TripleFaceIntersection::findFaceEdge(unsigned int face,
						  const HomogeneityTet *htet)
  const
{
  // Which edge of the given face is this point on?  The answer is
  // ambiguous, since the point is on a corner of the face, but it
  // doesn't matter which edge we choose.
  for(const FacePlane *otherface : faces_) {
    unsigned int oface = otherface->face();
    if(oface != face) {
      // Return the edge of "face" that is shared with oface.
      unsigned int edge = CSkeletonElement::faceFaceEdge[face][oface];
      assert(edge != NONE);
      return CSkeletonElement::tetEdge2FaceEdge[face][edge];
    }
  }
  throw ErrProgrammingError("TripleFaceIntersection::findFaceEdge failed!",
			    __FILE__, __LINE__);
}

bool TripleFaceIntersection::isEquivalent(const PlaneIntersection *pi) const
{
  return pi->isEquivalent(this); // double dispatch
}

bool TripleFaceIntersection::isEquivalent(const TripleFaceIntersection *tfi)
  const
{
  return node_ == tfi->getNode();
}

bool TripleFaceIntersection::isEquivalent(const PixelPlaneIntersectionNR *ppi)
  const
{
  return ppi->isEquivalent(this);
}

bool TripleFaceIntersection::isEquivalent(const RedundantIntersection *ri) const
{
  return ri->referent()->isEquivalent(this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: sharedPolySegment and onOnePolySegment can be written more
// efficiently for some subclasses of PixelPlaneIntersection. See the
// way onSameLoopSegment is done.

unsigned int PixelPlaneIntersection::sharedPolySegment(
					     const PixelPlaneIntersection *fi,
					     const PixelPlaneFacet *facet)
  const
{
  const FacePlane *fp = referent()->sharedFace(fi->referent(),
					       facet->getBaseFacePlane());
  if(fp == nullptr)
    return NONE;
  return facet->getPolyEdge(fp);
}

// onOnePolySegment returns true if two intersections share exactly
// one polygon segment.

bool PixelPlaneIntersection::onOnePolySegment(const PixelPlaneIntersection *fi,
					       const PixelPlaneFacet *facet)
  const
{
#ifdef DEBUG
  if(facet->verbose) {
    oofcerr << "PixelPlaneIntersection::onOnePolySegment: this=" << *this
	    << std::endl;
    oofcerr << "PixelPlaneIntersection::onOnePolySegment:   fi=" << *fi
	    << std::endl;
  }
#endif // DEBUG
  const std::vector<const FacePlane*> shared =
    referent()->sharedFaces(fi->referent());
#ifdef DEBUG
  if(facet->verbose) {
    oofcerr << "PixelPlaneIntersection::onOnePolySegment: base plane="
	    << facet->getBaseFacePlane();
    if(facet->getBaseFacePlane())
      oofcerr << " " << *facet->getBaseFacePlane();
    oofcerr << std::endl;
    oofcerr << "PixelPlaneIntersection::onOnePolySegment: shared.size="
	    << shared.size() << std::endl;
    for(const FacePlane *fp : shared) {
      oofcerr << "PixelPlaneIntersection::onOnePolySegment:  shared plane="
	      << fp << " " << *fp << std::endl;
    }
  }
#endif // DEBUG
  if(shared.size() == 1 && facet->getBaseFacePlane() != shared[0])
    return true;
  if(shared.size() == 2) {
    const FacePlane *base = facet->getBaseFacePlane();
    if(base == shared[0] || base == shared[1])
      return true;
  }
  return false;

  // // Old version that checks if there is at least one shared segment,
  // // not exactly one.
  // const FacePlane *fp = referent()->sharedFace(fi->referent(),
  // 					       facet->getBaseFacePlane());
  // return fp != nullptr;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void PixelPlaneIntersectionNR::copyPlanes(const PixelPlaneIntersectionNR *fi0,
					  const PixelPlaneIntersectionNR *fi1)
{
  pixelPlanes_.insert(fi0->pixelPlanes_.begin(), fi0->pixelPlanes_.end());
  pixelPlanes_.insert(fi1->pixelPlanes_.begin(), fi1->pixelPlanes_.end());
  faces_.insert(fi0->faces_.begin(), fi0->faces_.end());
  faces_.insert(fi1->faces_.begin(), fi1->faces_.end());
  pixelFaces_.insert(fi0->pixelFaces_.begin(), fi0->pixelFaces_.end());
  pixelFaces_.insert(fi1->pixelFaces_.begin(), fi1->pixelFaces_.end());
  
#ifdef DEBUG
  if(pixelPlanes_.size() + pixelFaces_.size() > 3) {
    if(verbose) {
      oofcerr << "PixelPlaneIntersectionNR::copyPlanes: Too many pixel planes!"
	      << std::endl;
      oofcerr << "PixelPlaneIntersectionNR::copyPlanes: fi0=" << *fi0
	      << std::endl;
      oofcerr << "PixelPlaneIntersectionNR::copyPlanes: fi1=" << *fi1
	      << std::endl;
    }
    throw ErrProgrammingError("Too many pixel planes!", __FILE__, __LINE__);
  }
#endif // DEBUG
}

void PixelPlaneIntersectionNR::computeLocation() {
  Coord3D pos;
  int npixplanes = pixelPlanes_.size() + pixelFaces_.size();
  if(npixplanes < 3) {
    std::vector<const Plane*> planes;
    planes.insert(planes.end(), pixelPlanes_.begin(), pixelPlanes_.end());
    planes.insert(planes.end(), pixelFaces_.begin(), pixelFaces_.end());
    int nToAdd = 3 - npixplanes;
    for(const Plane *face : faces_) {
      // TODO: If npixplanes==2, check that the plane being added
      // doesn't contain the intersection line of the pixplanes.
      if(npixplanes != 2 ||face->nonDegenerate(planes[0], planes[1])) {
	planes.push_back(face);
	if(--nToAdd == 0)
	  break;
      }
    }
#ifdef DEBUG
    if(planes.size() != 3) {
      // This is called from constructors before "verbose" is set, so
      // don't bother checking for it.
      oofcerr << "PixelPlaneIntersectionNR::computeLocation: wrong number of planes!: "
	      << *this << std::endl;
      throw ErrProgrammingError(
			"PixelPlaneIntersectionNR::computeLocation failed!",
			__FILE__, __LINE__);
    }
#endif // DEBUG
    pos = triplePlaneIntersection(planes[0], planes[1], planes[2]);
  }
  // If there are three pixel planes, then pos is uninitialized, but
  // the value passed to setLocation is irrelevant.
  setLocation(pos);
}

void PixelPlaneIntersectionNR::setLocation(const Coord3D &pos) {
  loc_ = pos;
  // Make sure that the point is exactly on all of the pixel planes.
  for(const HPixelPlane *pixplane : pixelPlaneSets())
    loc_[pixplane->direction()] = pixplane->normalOffset();
}

bool PixelPlaneIntersectionNR::samePixelPlanes(const PlaneIntersection *pi)
  const
{
  return pi->samePixelPlanes(this); // double dispatch
}

bool PixelPlaneIntersectionNR::samePixelPlanes(
				       const PixelPlaneIntersectionNR *other)
  const
{
  return (pixelPlanes_ == other->pixelPlanes_ &&
	  pixelFaces_ == other->pixelFaces_);
}

bool PixelPlaneIntersectionNR::samePixelPlanes(const TripleFaceIntersection*)
  const
{
  return false;
}

bool PixelPlaneIntersectionNR::samePixelPlanes(const RedundantIntersection *ri)
  const
{
  return ri->referent()->samePixelPlanes(this);
}

const FacePlane *PixelPlaneIntersectionNR::sharedFace(
				      const PixelPlaneIntersectionNR *fi)
  const
{
  const FacePlaneSet::const_iterator fp =
    sharedEntry(faces_, fi->referent()->faces());
  if(fp != faces_.end())
    return *fp;
  const FacePixelPlaneSet::const_iterator fpp =
    sharedEntry(pixelFaces_, fi->referent()->pixelFaces());
  if(fpp != pixelFaces_.end())
    return *fpp;
  return nullptr;
}

const FacePlane *PixelPlaneIntersectionNR::sharedFace(
				      const PixelPlaneIntersectionNR *fi,
				      const FacePixelPlane *exclude)
  const
{
  const FacePlaneSet::const_iterator fp =
    sharedEntry(faces_, fi->referent()->faces());
  if(fp != faces_.end())
    return *fp;
  const FacePixelPlaneSet::const_iterator fpp =
    sharedEntry(pixelFaces_, fi->referent()->pixelFaces(), exclude);
  if(fpp != pixelFaces_.end())
    return *fpp;
  return nullptr;
}

const std::vector<const FacePlane*> PixelPlaneIntersectionNR::sharedFaces(
				       const PixelPlaneIntersectionNR *fi)
  const
{
  std::vector<const FacePlane*> shared;
  std::set_intersection(faces_.begin(), faces_.end(),
			fi->faces().begin(),
			fi->faces().end(),
			std::inserter(shared, shared.end()),
			FacePlaneSet::key_compare());
  std::set_intersection(pixelFaces_.begin(), pixelFaces_.end(),
			fi->pixelFaces().begin(),
			fi->pixelFaces().end(),
			std::inserter(shared, shared.end()),
			FacePixelPlaneSet::key_compare());
  return shared;
}

bool PixelPlaneIntersectionNR::onSameFacePlane(
				       const PixelPlaneIntersectionNR *fib,
				       const FacePixelPlane *exclude)
  const
{
  if(exclude != nullptr)
    return sharedFace(fib, exclude) != nullptr;
  else
    return sharedFace(fib) != nullptr;
}


// The PixelPlaneIntersectionNR includes a necessarily contiguous set of
// polygon edges.  Find the one that's at the upper end (ie most
// counterclockwise) of the set.

unsigned int PixelPlaneIntersectionNR::maxPolyEdge(const PixelPlaneFacet *facet)
  const
{
  // TODO: The result of this calculation could be computed just once
  // and stored in the PixelPlaneIntersectionNR.  Probably maxPolyEdge
  // and minPolyEdge should be cached together.
  unsigned int nn = facet->polygonSize();
  std::vector<bool> e(nn, false);
  // Find which polygon edges are used in the PixelPlaneIntersectionNR. 
  for(const FacePlane *fp : facePlaneSets()) {
    unsigned int edge = facet->getPolyEdge(fp);
#ifdef DEBUG
    if(verbose) {
      oofcerr << "PixelPlaneIntersectionNR::maxPolyEdge: fp=" << *fp
	      << " edge=" << edge << std::endl;
    }
#endif // DEBUG
    if(edge != NONE)
      e[edge] = true;
  }
  // The last edge is the one whose successor is not in the set.
  for(unsigned int i=1; i<nn; i++)
    if(e[i-1] && !e[i])
      return i-1;
#ifdef DEBUG
  if(!(e[nn-1] && !e[0])) {
    oofcerr << "PixelPlaneIntersectionNR::maxPolyEdge: this=" << *this
	    << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::maxPolyEdge: e=";
    std::cerr << e;
    oofcerr << std::endl;
    throw ErrProgrammingError("maxPolyEdge failed!", __FILE__, __LINE__);
  }
#endif // DEBUG
  return nn-1;
}

// minPolyEdge is just like maxPolyEdge but it finds the first polygon
// edge in the intersection.

unsigned int PixelPlaneIntersectionNR::minPolyEdge(const PixelPlaneFacet *facet)
  const
{
  unsigned int nn = facet->polygonSize();
  // TODO: The vector e could be computed just once and stored in the
  // PixelPlaneIntersectionNR.
  std::vector<bool> e(nn, false);
  for(const FacePlane *fp : facePlaneSets()) {
    unsigned int edge = facet->getPolyEdge(fp);
    if(edge != NONE)
      e[edge] = true;
  }
  for(unsigned int i=1; i<nn; i++)
    if(!e[i-1] && e[i])
      return i;
  assert(!e[nn-1] && e[0]);
  return 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

struct GEOFdata {		// Get Edges On Faces data
  const HomogeneityTet *htet;
  FaceFacets &faceFacets;
  const PixelPlaneIntersectionNR *thisIntersection;
  const PixelPlaneIntersectionNR *otherIntersection;
  const HPixelPlane *pixplane;
#ifdef DEBUG
  bool verbose;
#endif // DEBUG
};

template <class TYPE>
bool GEOFcallback(const TYPE &faceplane, void *data) {
  GEOFdata *gdata = (GEOFdata*) data;
#ifdef DEBUG
  if(gdata->verbose)
    oofcerr << "GEOFcallback: face=" << *faceplane << " isecs= "
	    << *gdata->otherIntersection << " "
	    << *gdata->thisIntersection << std::endl;
#endif // DEBUG
  // This PixelPlaneIntersectionNR is the start of an existing facet
  // edge on a pixel plane, so the face facet edges that are created
  // here begin at "other" and go to "this".
  // The FaceFacetEdge constructor clones its intersection args.
  gdata->faceFacets[faceplane->face()].addEdge(
		       new FaceFacetEdge(gdata->htet, gdata->otherIntersection,
					 gdata->thisIntersection,
					 gdata->pixplane));
  return false;
}

void PixelPlaneIntersectionNR::getEdgesOnFaces(
				       const HomogeneityTet *htet,
				       const PixelPlaneIntersectionNR *other,
				       const HPixelPlane *pixplane,
				       FaceFacets &faceFacets)
  const
{
  // For each face that this PixelPlaneIntersectionNR shares with the
  // other PixelPlaneIntersectionNR, add an edge joining this to the
  // other in FaceFacets.  FaceFacets is a std::vector of FaceFacet
  // objects, which contain sets of FacetEdges.

  GEOFdata data({htet, faceFacets, this, other, pixplane
#ifdef DEBUG
	, verbose
#endif // DEBUG
	});
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneIntersectionNR::getEdgesOnFaces:  this=" << *this
	    << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::getEdgesOnFaces: other=" << *other
	    << std::endl;
  }
  OOFcerrIndent indent(2);
#endif // DEBUG
  // foreachShared calls GEOFcallback for each face that's in both of
  // the given sets (faces_ and other->faces()).  If a face is on a
  // pixel plane, it's not used.
  foreachShared(faces_, other->faces(), GEOFcallback<const FacePlane*>, &data);
  foreachShared(pixelFaces_, other->pixelFaces(),
		GEOFcallback<const FacePixelPlane*>, &data);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Which edge of the given face is this intersection on?

unsigned int PixelPlaneIntersectionNR::findFaceEdge(unsigned int f,
						    const HomogeneityTet *htet)
  const
{
  // faceIDs contains the face indices of the tet faces that this
  // intersection is on.
  std::set<unsigned int> faceIDs;
  // TODO: See if f is a FacePixelPlane and loop over either faces_ or
  // pixelFaces_.  No need to use facePlaneSets.
  for(const FacePlane *face : facePlaneSets())
    faceIDs.insert(face->face());
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneIntersectionNR::findFaceEdge: f=" << f << " " << *this
// 	    << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::findFaceEdge: faceIDs=";
//     std::cerr << faceIDs;
//     oofcerr << std::endl;
//   }
// #endif	// DEBUG
  for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) { 
    unsigned int edge = CSkeletonElement::faceEdges[f][e]; // face -> tet scope
    unsigned int otherface = CSkeletonElement::getOtherFaceIndex(f, edge);
    if(faceIDs.find(otherface) != faceIDs.end())
      return e;
  }
  return NONE;
  
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Update the appropriate PolyEdgeIntersections object with data from
// this intersection.

void PixelPlaneIntersectionNR::locateOnPolygonEdge(
				std::vector<PolyEdgeIntersections> &polyedges,
				const PixelPlaneFacet *facet)
  const
{
  // If there are multiple faces, this makes an arbitrary choice.  Any
  // of them will do, except for the plane of the facet.
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneIntersectionNR::locateOnPolygonEdge: " << *this
// 	    << std::endl;
// #endif // DEBUG
  if(!faces_.empty()) {
    unsigned int edge = facet->getPolyEdge(*faces_.begin());
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "PixelPlaneIntersectionNR::locateOnPolygonEdge: polyEdge="
// 	      << edge << " using faces_" << std::endl;
// #endif // DEBUG
    assert(edge != NONE);
    polyedges[edge].push_back(this);
    return;
  }
  else {
    assert(!pixelFaces_.empty());
    for(const FacePixelPlane *fpp : pixelFaces_) {
      if(fpp != facet->pixplane) {
	unsigned int edge = facet->getPolyEdge(fpp);
// #ifdef DEBUG
// 	if(verbose) {
// 	  oofcerr << "PixelPlaneIntersectionNR::locateOnPolygonEdge: polyEdge="
// 		  << edge << " using pixelFaces_ "
// 		  << *fpp << std::endl;
//     }
// #endif // DEBUG
	assert(edge != NONE);
	polyedges[edge].push_back(this);
	return;
      }
    }
  }
  throw ErrProgrammingError(
		    "PixelPlaneIntersectionNR::locateOnPolygonEdge failed!",
		    __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool PixelPlaneIntersectionNR::isEquivalent(const PlaneIntersection *pi) const
{
  return pi->isEquivalent(this); // double dispatch
}

bool PixelPlaneIntersectionNR::isEquivalent(const TripleFaceIntersection *tfi)
  const
{
  // Each face in the TripleFaceIntersection must be in the
  // PixelPlaneIntersectionNR.

  // TODO: Is it worth being cleverer about this search?  Both
  // tfiFaces is sorted, and facePlaneSets is too, sort of.
  unsigned int nmatch = 0;
  const FacePlaneSet &tfiFaces = tfi->faces();
  for(const FacePlane *face : facePlaneSets()) {
    if(tfiFaces.find(face) != tfiFaces.end())
      ++nmatch;
  }
  return nmatch == 3;
}

bool PixelPlaneIntersectionNR::isEquivalent(const PixelPlaneIntersectionNR *ppi)
  const
{
  // TODO: Is it worth being cleverer about these searches?  All of
  // the sets are sorted, and that information isn't being used.  The
  // sets are also small.
  unsigned int npixplanes = 0;
  std::vector<const Plane*> planes;
  planes.reserve(10);	   // more than we'll need in almost all cases
  for(const HPixelPlane *thisplane : pixelPlanes_) {
    for(const HPixelPlane *otherplane : ppi->pixelPlanes()) {
      if(thisplane == otherplane) {
	++npixplanes;
	planes.push_back(thisplane);
	break;
      }
    }
  }
  if(npixplanes >= 3)
    return true;

  unsigned int nfaces = 0;
  for(const FacePlane *thisplane : faces_) {
    for(const FacePlane *otherplane : ppi->faces()) {
      if(thisplane == otherplane) {
	++nfaces;
	planes.push_back(thisplane);
	break;
      }
    }
  }
  if(nfaces >= 3)
    return true;

  unsigned int npixfaces = 0;
  for(const FacePixelPlane *thisplane : pixelFaces_) {
    for(const FacePixelPlane *otherplane : ppi->pixelFaces()) {
      if(thisplane == otherplane) {
	++npixfaces;
	planes.push_back(thisplane);
	break;
      }
    }
  }

  if(planes.size() < 3)
    return false;

  if(npixfaces + nfaces >= 3 || npixfaces + npixplanes >= 3)
    return true;

  // The tricky cases are:
  // (A) two faces (including pixelfaces) and one pixelplane
  // (B) two pixelplanes (including pixelfaces) and one face

  // In these cases the three planes might all intersect on a line, so
  // all points on the line share 3 planes.  Sharing three planes
  // isn't enough to say that two points are equivalent.

  // Look at all sets of 3 shared planes and check to see if they're
  // degenerate.  If there is a nondegenerate set, then the points
  // coincide at that point.  If there is no nondegenerate point, then
  // there must be other, non-shared planes that distinguish the
  // points, and the points do not coincide.
  unsigned int nPlanes = planes.size();
  for(unsigned int i=0; i<nPlanes; i++) {
    for(unsigned int j=i+1; j<nPlanes; j++) {
      for(unsigned int k=j+1; k<nPlanes; k++) {
	if(planes[i]->nonDegenerate(planes[j], planes[k]))
	  return true;
      }
    }
  }
  return false;
  
  // for(const HPixelPlane *thisplane : pixelPlanes_)
  //   for(const HPixelPlane *otherplane : ppi->pixelPlanes()) {
  //     if(thisplane == otherplane) {
  // 	++nmatch;
  // 	break;
  //     }
  //   }
  // if(nmatch >= 3)
  //   return true;
  // for(const FacePlane *thisplane : faces_)
  //   for(const FacePlane *otherplane : ppi->faces()) {
  //     if(thisplane == otherplane) {
  // 	++nmatch;
  // 	break;
  //     }
  //   }
  // if(nmatch >= 3)
  //   return true;
  // for(const FacePixelPlane *thisplane : pixelFaces_)
  //   for(const FacePixelPlane *otherplane : ppi->pixelFaces()) {
  //     if(thisplane == otherplane) {
  // 	++nmatch;
  // 	break;
  //     }
  //   }
  // return nmatch >= 3;
}

bool PixelPlaneIntersectionNR::isEquivalent(const RedundantIntersection *ri)
  const
{
  return ri->referent()->isEquivalent(this);
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::string PixelPlaneIntersectionNR::printPlanes() const {
  std::string str;
  bool printedSome = false;
  if(!pixelPlanes_.empty()) {
    str += "pixelPlanes=[";
    bool first = true;
    for(const PixelPlane *pp : pixelPlanes_) {
      if(!first)
	str += ", ";
      first = false;
      str += to_string(*pp);
    }
    str += "]";
    printedSome = true;
  }
  if(!pixelFaces_.empty()) {
    if(printedSome)
      str += ", ";
    bool first = true;
    str += "pixelFaces=[";
    for(const FacePixelPlane *fpp : pixelFaces_) {
      if(!first)
	str += ", ";
      first = false;
      str += to_string(*fpp);
    }
    str += "]";
    printedSome = true;
  }
  if(!faces_.empty()) {
    if(printedSome)
      str += ", ";
    str += "faces=[";
    bool first = true;
    for(const FacePlane *f : faces_) {
      if(!first)
	str += ", ";
      first = false;
      str += to_string(*f);
    }
    str += "]";
  }
  return str;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Methods for the mix-in classes.

#ifdef DEBUG
SingleVSBbase::SingleVSBbase() {
  // oofcerr << "SingleVSBbase::ctor: " << this << std::endl;
}
#endif // DEBUG

template <class BASE>
SingleFaceMixIn<BASE>::SingleFaceMixIn()
  : polyFrac(-12345.),		// will be reset
    facePlane_(nullptr)
{
// #ifdef DEBUG
//   oofcerr << "SingleFaceMixIn::ctor: " << this << std::endl;
// #endif // DEBUG
}

template <class BASE>
double SingleFaceMixIn<BASE>::getPolyFrac(unsigned int,
					  const PixelPlaneFacet *facet)
  const
{
  //  assert(edgeno == facet->getPolyEdge(facePlane_));
  if(polyFrac >= 0) return polyFrac; // cached value
  BarycentricCoord bary = BASE::baryCoord(facet->htet);
  polyFrac = facet->htet->edgeCoord(bary, facePlane_, facet);
  return polyFrac;
}

template <class BASE>
unsigned int SingleFaceMixIn<BASE>::getPolyEdge(const PixelPlaneFacet *facet)
  const
{
  return facet->getPolyEdge(facePlane_);
}

template <class BASE>
unsigned int SingleFaceMixIn<BASE>::maxPolyEdge(const PixelPlaneFacet *facet)
  const
{
  return facet->getPolyEdge(facePlane_);
}

template <class BASE>
unsigned int SingleFaceMixIn<BASE>::minPolyEdge(const PixelPlaneFacet *facet)
  const
{
  return facet->getPolyEdge(facePlane_);
}

// template <class BASE1> template <class BASE2>
// bool SingleFaceMixIn<BASE1>::onOnePolySegment(
// 				     const SingleFaceMixIn<BASE2> *other)
//   const
// {
//   return facePlane_ == other->getFacePlane();
// }

//-------

template <class BASE>
unsigned int MultiFaceMixin<BASE>::getPolyEdge(const PixelPlaneFacet*) const {
  return NONE;
}

// Is the given point on the non-positive side of all of the faces?
// TODO: Is it better to use barycentric coords for this?

template <class BASE>
bool MultiFaceMixin<BASE>::inside(const Coord3D &pt) const {
  for(const FacePlane *face : BASE::faces_) {
    if(face->outside(pt))
      return false;
  }
  return true;
}

// Given a polygon edge index, return the fractional position of this
// intersection on the edge.

template <class BASE>
double MultiFaceMixin<BASE>::getPolyFrac(unsigned int edge,
					 const PixelPlaneFacet *facet)
  const
{
  // An intersection that's on more than one face must be at a corner
  // of the polygon, so its fractional position along a polygon edge
  // is either 0 or 1.
// #ifdef DEBUG
//   if(facet->verbose)
//     oofcerr << "MultiFaceMixin::getPolyFrac: " << this << " " << *this
// 	    << std::endl;
// #endif // DEBUG
  unsigned int nn = facet->polygonSize();
  const FacePlane *nextface = facet->getFacePlane((edge+1)%nn);
// #ifdef DEBUG
//   if(facet->verbose)
//     oofcerr << "MultiFaceMixin::getPolyFrac: nn=" << nn << " nextface="
// 	    << nextface << " " << *nextface << std::endl;
// #endif	// DEBUG
  if(nextface->isPartOf(this))
    return 1.0;
#ifdef DEBUG
  const FacePlane *prevface = facet->getFacePlane((edge+nn-1)%nn);
  // if(facet->verbose)
  //   oofcerr << "MultiFaceMixin::getPolyFrac: prevface="
  // 	    << prevface << " " << *prevface << std::endl;
  assert(prevface->isPartOf(this));
#endif // DEBUG
  return 0.0;
}

template <class BASE>
unsigned int MultiFaceMixin<BASE>::getOtherFaceIndex(
					     unsigned int f,
					     const PixelPlaneFacet *facet)
  const
{
  assert(BASE::faces_.size() + BASE::pixelFaces_.size() == 2);
  for(const FacePlane *fp : BASE::facePlaneSets()) {
    unsigned int idx = facet->getPolyEdge(fp);
    if(idx != f)
      return idx;
  }
  throw ErrProgrammingError("getOtherFaceIndex failed!", __FILE__, __LINE__);
  // auto iter = BASE::faces_.begin();
  // unsigned int idx = facet->getPolyEdge(*iter);
  // if(idx != f)
  //   return idx;
  // idx = facet->getPolyEdge(*++iter);
  // assert(idx != f);
  // return idx;
}

//-------

#ifdef DEBUG
template <class BASE>
SingleVSBmixIn<BASE>::SingleVSBmixIn() {
  // oofcerr << "SingleVSBmixIn::ctor: " << this << std::endl;
}
#endif // DEBUG

template <class BASE>
double SingleVSBmixIn<BASE>::getLoopFrac(const PixelBdyLoopSegment &seg) const
{
  assert(seg == vsbSegment);
  return loopFrac;
}

// The onSameLoopSegment stuff is complicated because it does double
// dispatch within the template zoo.  This would be easier if virtual
// member functions with template arguments were allowed.

template <class BASE>
bool SingleVSBmixIn<BASE>::onSameLoopSegment(
				     const PixelPlaneIntersectionNR *fib)
  const
{
  // double dispatch
  return fib->sameLoopSegment(static_cast<const SingleVSBbase*>(this));
}

template <class BASE> 
bool SingleVSBmixIn<BASE>::sameLoopSegment(const SingleVSBbase *other)
  const
{
  // onSameLoopSegment is more restrictive than samePixelPlanes.
// #ifdef DEBUG
//   if(BASE::verbose) {
//     OOFcerrIndent indent(2);
//     oofcerr << "SingleVSBmixIn::sameLoopSegment: this->vsbSegment="
// 	    << vsbSegment
// 	    << " other=" << other->getLoopSeg() << std::endl;
//   }
// #endif // DEBUG
  return vsbSegment == other->getLoopSeg();
}

template <class BASE> 
bool SingleVSBmixIn<BASE>::sameLoopSegment(const MultiVSBbase *other)
  const
{
  return other->getLoopSegs().count(vsbSegment) > 0;
}

template <class BASE>
const PixelBdyLoopSegment *SingleVSBmixIn<BASE>::sharedLoopSegment(
					     const PixelPlaneIntersectionNR *fi)
  const
{
  // double dispatch
  return fi->sharedLoopSeg(static_cast<const SingleVSBbase*>(this));
}

template <class BASE>
const PixelBdyLoopSegment *SingleVSBmixIn<BASE>::sharedLoopSeg(
						const SingleVSBbase *other)
  const
{
  const PixelBdyLoopSegment &seg = other->getLoopSeg();
  if(seg == vsbSegment)
    return &vsbSegment;
  return nullptr;
}

template <class BASE>
const PixelBdyLoopSegment *SingleVSBmixIn<BASE>::sharedLoopSeg(
						 const MultiVSBbase *other)
  const
{
  if(other->getLoopSegs().count(vsbSegment) > 0)
    return &vsbSegment;
  return nullptr;
}

template <class BASE>
ISEC_ORDER SingleVSBmixIn<BASE>::getOrdering(const PixelPlaneIntersectionNR *fi,
					     PixelBdyLoopSegment &seg0,
					     PixelBdyLoopSegment &seg1)
  const
{
  return fi->ordering(static_cast<const SingleVSBbase*>(this), seg0, seg1);
}

template <class BASE>
ISEC_ORDER SingleVSBmixIn<BASE>::ordering(const SingleVSBbase *other,
					  PixelBdyLoopSegment &seg0,
					  PixelBdyLoopSegment &seg1)
  const
{
  if(other->getLoopSeg().firstPt() == vsbSegment.secondPt()) {
    seg0 = vsbSegment;
    seg1 = other->getLoopSeg();
    return FIRST;
  }
  if(other->getLoopSeg().secondPt() == vsbSegment.firstPt()) {
    seg1 = vsbSegment;
    seg0 = other->getLoopSeg();
    return SECOND;
  }
  return NONCONTIGUOUS;
}

template <class BASE>
ISEC_ORDER SingleVSBmixIn<BASE>::ordering(const MultiVSBbase *other,
					  PixelBdyLoopSegment &seg0,
					  PixelBdyLoopSegment &seg1)
  const
{
  const PBLSegmentMap &osegs = other->getLoopSegs();
  for(PBLSegmentMap::const_iterator oi=osegs.begin(); oi!=osegs.end(); ++oi) {
    const PixelBdyLoopSegment &oseg = (*oi).first;
    if(oseg.firstPt() == vsbSegment.secondPt()) {
      seg0 = vsbSegment;
      seg1 = oseg;
      return FIRST;
    }
    if(oseg.secondPt() == vsbSegment.firstPt()) {
      seg1 = vsbSegment;
      seg0 = oseg;
      return SECOND;
    }
  }
  return NONCONTIGUOUS;
}

//-------

// MultiVSBmixIn::categorizeCorner categorizes the VSB corner that's
// *at* an intersection, in contrast to classifyVSBcorner, which
// categorizes the corner *between* two intersections.

template <class BASE>
TurnDirection MultiVSBmixIn<BASE>::categorizeCorner(
						PixelBdyLoopSegment &loopSeg0,
						PixelBdyLoopSegment &loopSeg1)
  const
{
  assert(vsbSegments.size() == 2);
  auto iter = vsbSegments.begin();
  const PixelBdyLoopSegment &seg0 = (*iter).first;
  ++iter;
  const PixelBdyLoopSegment &seg1 = (*iter).first;
  if(seg0.firstPt() == seg1.secondPt()) {
    loopSeg0 = seg1;
    loopSeg1 = seg0;
  }
  else {
    assert(seg1.firstPt() == seg0.secondPt());
    loopSeg0 = seg0;
    loopSeg1 = seg1;
  }
  return turnDirection(loopSeg0.firstPt(), loopSeg0.secondPt(),
		       loopSeg1.secondPt());
}

template <class BASE>
double MultiVSBmixIn<BASE>::getLoopFrac(const PixelBdyLoopSegment &seg) const {
  PBLSegmentMap::const_iterator it = vsbSegments.find(seg);
#ifdef DEBUG
  if(it == vsbSegments.end())
    throw ErrProgrammingError("VSB segment not found!", __FILE__, __LINE__);
#endif // DEBUG
  return (*it).second;
}

template <class BASE>
bool MultiVSBmixIn<BASE>::onSameLoopSegment(const PixelPlaneIntersectionNR *fib)
  const
{
  // double dispatch
  return fib->sameLoopSegment(static_cast<const MultiVSBbase*>(this));
}

template <class BASE>
bool MultiVSBmixIn<BASE>::sameLoopSegment(const SingleVSBbase *other)
  const
{
  return vsbSegments.find(other->getLoopSeg()) != vsbSegments.end();
}

template <class BASE>
bool MultiVSBmixIn<BASE>::sameLoopSegment(const MultiVSBbase *other)
  const
{
  const PBLSegmentMap &osegs = other->getLoopSegs();
  if(vsbSegments.empty() || osegs.empty())
    return false;
  return sharedMapEntry(vsbSegments, osegs) != vsbSegments.end();
}

template <class BASE>
const PixelBdyLoopSegment *MultiVSBmixIn<BASE>::sharedLoopSegment(
				      const PixelPlaneIntersectionNR *fi)
  const
{
  return fi->sharedLoopSeg(static_cast<const MultiVSBbase*>(this));
}

template <class BASE>
const PixelBdyLoopSegment *MultiVSBmixIn<BASE>::sharedLoopSeg(
						const SingleVSBbase *other)
  const
{
  return other->sharedLoopSeg(this);
}

template <class BASE>
const PixelBdyLoopSegment *MultiVSBmixIn<BASE>::sharedLoopSeg(
						const MultiVSBbase *other)
  const
{
  const PBLSegmentMap &osegs = other->getLoopSegs();
  PBLSegmentMap::const_iterator seg = sharedMapEntry(vsbSegments, osegs);
  if(seg != vsbSegments.end())
    return &(*seg).first;
  return nullptr;
}

template <class BASE>
ISEC_ORDER MultiVSBmixIn<BASE>::getOrdering(const PixelPlaneIntersectionNR *fi,
					    PixelBdyLoopSegment &seg0,
					    PixelBdyLoopSegment &seg1)
  const
{
  return fi->ordering(static_cast<const MultiVSBbase*>(this), seg0, seg1);
}

template <class BASE>
ISEC_ORDER MultiVSBmixIn<BASE>::ordering(const SingleVSBbase *other,
					 PixelBdyLoopSegment &seg0,
					 PixelBdyLoopSegment &seg1)
  const
{
  ISEC_ORDER reverse = other->ordering(this, seg0, seg1);
  if(reverse == FIRST) {
    return SECOND;
  }
  if(reverse == SECOND)
    return FIRST;
  return NONCONTIGUOUS;
}

template <class BASE>
ISEC_ORDER MultiVSBmixIn<BASE>::ordering(const MultiVSBbase *other,
					 PixelBdyLoopSegment &seg0,
					 PixelBdyLoopSegment &seg1)
  const
{
  const PBLSegmentMap &osegs = other->getLoopSegs();
  for(PBLSegmentMap::const_iterator iseg=vsbSegments.begin();
      iseg!=vsbSegments.end(); ++iseg)
    {
      const PixelBdyLoopSegment &seg = (*iseg).first;
      for(PBLSegmentMap::const_iterator ioseg=osegs.begin(); ioseg!=osegs.end();
	  ++ioseg)
	{
	  const PixelBdyLoopSegment &oseg = (*ioseg).first;
	  if(oseg.firstPt() == seg.secondPt()) {
	    seg0 = seg;
	    seg1 = oseg;
	    return FIRST;
	  }
	  if(oseg.secondPt() == seg.firstPt()) {
	    seg1 = seg;
	    seg0 = oseg;
	    return SECOND;
	  }
	}
    }
  return NONCONTIGUOUS;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility function used when merging intersections.  If the two given
// intersections are merged, what is the crossing type of the result?

static CrossingType combinedCrossing(const PixelPlaneIntersectionNR *fi0,
				     const PixelPlaneIntersectionNR *fi1)
{
  if(fi0->crossingType() == fi1->crossingType())
    return fi0->crossingType();
  if(fi0->crossingType() == NONCROSSING)
    return fi1->crossingType();
  if(fi1->crossingType() == NONCROSSING)
    return fi0->crossingType();
  return NONCROSSING;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SimpleIntersection::SimpleIntersection(const HomogeneityTet *htet,
				       const HPixelPlane *pp0,
				       const HPixelPlane *pp1,
				       const PixelBdyLoopSegment &pblseg,
				       double alpha,
				       unsigned int faceIndex,
				       CrossingType ct)
{
#ifdef DEBUG
  if(pp0 != htet->getUnorientedPixelPlane(pp0)) {
    oofcerr << "SimpleIntersection::ctor: pp0=" << pp0 << " " << *pp0
	    << " unoriented=" << htet->getUnorientedPixelPlane(pp0)
	    << " " << dynamic_cast<const HPixelPlane*>(htet->getUnorientedPixelPlane(pp0))
	    << " " << *htet->getUnorientedPixelPlane(pp0)
	    << std::endl;
    throw ErrProgrammingError(
      "SimpleIntersection constructor: received misoriented pixel plane!",
      __FILE__, __LINE__);
  }
#endif // DEBUG
  assert(ct != NONCROSSING);
  assert(pp0 == htet->getUnorientedPixelPlane(pp0));
  assert(pp1 == htet->getUnorientedPixelPlane(pp1));
  pp0->addToIntersection(this);
  pp1->addToIntersection(this);

  // The given faceindex is the face that intersects the
  // PixelBdyLoopSegment.  It's not the face, if any, that contains the
  // pixel plane of the facet.
  const FacePlane *fp = htet->getFacePlane(faceIndex);
  fp->addToIntersection(this);
  setFacePlane(fp);
  setLoopSeg(pblseg);
  setLoopFrac(alpha);
  setCrossingType(ct);
  // try {
    computeLocation();
  // }
  // catch (...) {
  //   oofcerr << "SimpleIntersection::ctor: pp0=" << *pp0 << " pp1=" << *pp1
  // 	    << " pblseg=" << pblseg << " faceIndex=" << faceIndex
  // 	    << std::endl;
  //   throw;
  // }

    // #ifdef DEBUG
//   oofcerr << "SimpleIntersection::ctor: done" << std::endl;
// #endif // DEBUG
}

SimpleIntersection *SimpleIntersection::clone() const {
  return new SimpleIntersection(*this);
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
					const HomogeneityTet *htet,
					const PixelPlaneIntersection *fi,
					const PixelPlaneFacet *facet)
  const
{
  if(fi)
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
						const HomogeneityTet *htet,
						const SimpleIntersection *fi,
						const PixelPlaneFacet *facet)
  const
{
#ifdef DEBUG
  if(htet->verbosePlane())
    oofcerr << "SimpleIntersection::mergeWith: this="
	    << *this << " fi=" << *fi << std::endl;
#endif // DEBUG
  // Two antiparallel but otherwise equivalent VSB segments that
  // intersect a face should form a new SimpleIntersection there.
  if(isEquivalent(fi)) {
    SimpleIntersection *result = clone();
    result->setCrossingType(combinedCrossing(this, fi));
    return result;
  }
  if(facet->onOppositeEdges(this, fi))
    return nullptr;
  if(onSameLoopSegment(fi))
    return new MultiFaceIntersection(htet, this, fi);

  if(onOnePolySegment(fi, facet)) {
    PixelPlaneIntersectionNR *res =
      new MultiVSBIntersection(htet, facet, this, fi);
#ifdef DEBUG
    if(htet->verbosePlane())
      oofcerr << "SimpleIntersection::mergeWith: result=" << *res << std::endl;
#endif // DEBUG
    return res;
  }
  return new MultiCornerIntersection(htet, this, fi);
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
						const HomogeneityTet *htet,
						const MultiFaceIntersection *fi,
						const PixelPlaneFacet *facet)
  const
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  if(onSameLoopSegment(fi))
    return new MultiFaceIntersection(htet, this, fi);
  return new MultiCornerIntersection(htet, this, fi);
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
						const HomogeneityTet *htet,
						const MultiVSBIntersection *fi,
						const PixelPlaneFacet *facet)
  const
{
  if(onOnePolySegment(fi, facet))
    return new MultiVSBIntersection(htet, facet, this, fi);
  return new MultiCornerIntersection(htet, this, fi);
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
					const HomogeneityTet *htet,
					const MultiCornerIntersection *fi,
					const PixelPlaneFacet *facet)
const
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  return new MultiCornerIntersection(htet, this, fi);
}

bool SimpleIntersection::isMisordered(const PixelPlaneIntersection *fi,
				      const PixelPlaneFacet *facet)
  const
{
  return fi->referent()->isMisordered(this, facet); // double dispatch
}

bool SimpleIntersection::isMisordered(const SimpleIntersection *fi,
				      const PixelPlaneFacet *facet)
  const
{
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "SimpleIntersection::isMisordered: this=" << *this
// 	    << " crossing=" << crossingType() << std::endl
// 	    << "                                :   fi=" << *fi
// 	    << " crossing=" << fi->crossingType() << std::endl;
//   }
// #endif // DEBUG
  bool sameLoopSeg = onSameLoopSegment(fi);
  bool samePolySeg = onOnePolySegment(fi, facet);
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "SimpleIntersection::isMisordered: sameLoopSeg=" << sameLoopSeg
// 	    << " samePolySeg=" << samePolySeg << std::endl;
// #endif // DEBUG
  assert(!(sameLoopSeg && samePolySeg));
  if(!sameLoopSeg && samePolySeg) {
    return facet->vsbCornerCoincidence(this, fi);
  }
  if(sameLoopSeg && !samePolySeg) {
    return facet->polyCornerCoincidence(this, fi);
  }
  if(!sameLoopSeg && !samePolySeg) {
    return facet->polyVSBCornerCoincidence(this, fi);
  }
  return false;
}

bool SimpleIntersection::isMisordered(const MultiFaceIntersection *fi,
				      const PixelPlaneFacet *facet)
  const
{
  if(onSameLoopSegment(fi)) {
    /*           /
    //          /
    //   ------o----o-----
    //   |    /    / \      It's hard to see how this can happen even with
    //   |   /    /   \     round-off error.  Maybe the middle polygon
    //   |  /    /     \    segment is actually horizontal.  
    //                      Merge the intersections.
    */
    return true;
  }
  /* We've got something like this:
  //
  //   ----m-----
  //   |  / \      m = MultiFaceIntersection
  //   | /   \     s = SimpleIntersection
  //   |/     \                                                   
  //   s       \   The ordering constraints are the same as they'd be if
  //  /|        \  the MultiFaceIntersection were a SimpleIntersection.
  */

  return facet->badTopology(this, fi);
}

bool SimpleIntersection::isMisordered(const MultiVSBIntersection *fi,
				      const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(this, fi);
}

bool SimpleIntersection::isMisordered(const MultiCornerIntersection *fi,
				      const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(this, fi);
}

void SimpleIntersection::print(std::ostream &os) const {
  os << "SimpleIntersection(" << printPlanes() << ", " << location3D()
     << ", " << crossingType() << ", faceplane=" << *getFacePlane() << ")";
}

PixelPlaneIntersectionNR *newIntersection(const HomogeneityTet *htet,
					  const HPixelPlane *basePlane,
					  const HPixelPlane *orthoPlane,
					  const PixelBdyLoopSegment &pblSeg,
					  double alpha,
					  unsigned int faceIndex,
					  CrossingType ct)
{
  const FacePixelPlane *fpp = htet->getCoincidentFacePlane(orthoPlane);
  if(fpp == nullptr) {
    return new SimpleIntersection(htet, basePlane, orthoPlane, pblSeg, alpha,
				  faceIndex, ct);
  }
  return new MultiFaceIntersection(htet, basePlane, orthoPlane, pblSeg, alpha,
				   faceIndex, ct);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MultiFaceIntersection::MultiFaceIntersection(const HomogeneityTet *htet,
					     const HPixelPlane *pp0,
					     const HPixelPlane *pp1,
					     const PixelBdyLoopSegment &pblseg,
					     double alpha,
					     unsigned int faceIndex,
					     CrossingType ct)
{
  pp0->addToIntersection(this);
  pp1->addToIntersection(this);
  const FacePlane *fp = htet->getFacePlane(faceIndex);
  fp->addToIntersection(this);
  setLoopSeg(pblseg);
  setLoopFrac(alpha);
  setCrossingType(ct);
  computeLocation();
}

MultiFaceIntersection::MultiFaceIntersection(const HomogeneityTet *htet,
					     const SimpleIntersection *fi0,
					     const SimpleIntersection *fi1)
{
  assert(fi0->onSameLoopSegment(fi1));
  assert(fi0->getFacePlane() != fi1->getFacePlane());
#ifdef DEBUG
  verbose = fi0->verbose || fi1->verbose;
#endif // DEBUG
  setCrossingType(combinedCrossing(fi0, fi1));
  setLoopSeg(fi0->getLoopSeg());
  setLoopFrac(fi0->getLoopFrac());
  copyPlanes(fi0, fi1);
  // This may not be the best way to calculate the position, but the
  // position shouldn't be used for topological calculations anyway.
  setLocation(0.5*(fi0->location3D() + fi1->location3D()));
}

MultiFaceIntersection::MultiFaceIntersection(const HomogeneityTet *htet,
					     const SimpleIntersection *si,
					     const MultiFaceIntersection *mfi)
{
  assert(si->onSameLoopSegment(mfi));
#ifdef DEBUG
  verbose = si->verbose || mfi->verbose;
#endif // DEBUG
  setCrossingType(combinedCrossing(si, mfi));
  setLoopSeg(si->getLoopSeg());
  setLoopFrac(si->getLoopFrac());
  copyPlanes(si, mfi);
  // This may not be the best way to calculate the position, but the
  // position shouldn't be used for topological calculations anyway.
  setLocation(0.5*(si->location3D() + mfi->location3D()));
}

MultiFaceIntersection *MultiFaceIntersection::clone() const {
  return new MultiFaceIntersection(*this);
}

// A MultiFaceIntersection is interior if the interior of the polygon
// at the corner is on the interior (ie left) side of the VSB segment.

Interiority MultiFaceIntersection::interiority(const PixelPlaneFacet *facet)
  const
{
  assert(faces_.size() == 2);
  ICoord2D vsb0 = segEnd(0);
  ICoord2D vsb1 = segEnd(1);
  std::vector<bool> interior;
  interior.reserve(2);
  for(const FacePlane *face : facePlaneSets()) {
    unsigned int polyseg = facet->getPolyEdge(face);
    Coord2D p0 = facet->polygonCorner(polyseg);
    Coord2D p1 = facet->polygonCorner((polyseg+1) % facet->polygonSize());
    // TODO: Worry about round-off error here, or explain why it's not
    // important.
    interior.push_back(cross(vsb1-vsb0, p1-p0) > 0.0);
  }
  if(interior[0] && interior[1])
    return INTERIOR;
  if(!interior[0] && !interior[1])
    return EXTERIOR;
  return MIXED;
}

const FacePlane *MultiFaceIntersection::firstFacePlane(
					       const PixelPlaneFacet *facet)
  const
{
  const FacePlane *face0 = nullptr;
  const FacePlane *face1 = nullptr;
  assert(faces_.size() + pixelFaces_.size() == 2);
  for(const FacePlane *face : facePlaneSets()) {
    if(!face0)
      face0 = face;
    else
      face1 = face;
  }
  if((facet->getPolyEdge(face0)+1)%facet->polygonSize() ==
     facet->getPolyEdge(face1))
    return face0;
  return face1;
}

// TODO: Should this return std::pair<unsigned int, unsigned int> ?

void MultiFaceIntersection::getPolyEdges(const PixelPlaneFacet *facet,
					 unsigned int &seg0,
					 unsigned int &seg1)
  const
{
  const FacePlane *face0 = firstFacePlane(facet);
  seg0 = facet->getPolyEdge(face0);
  seg1 = (seg0 + 1) % facet->polygonSize();
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
					   const HomogeneityTet *htet,
					   const PixelPlaneIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  if(fi)
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
						   const HomogeneityTet *htet,
						   const SimpleIntersection *fi,
						   const PixelPlaneFacet *facet)
  const
{
  // SimpleIntersection::mergeWith(MultiFaceIntersection) is equivalent
  return fi->mergeWith(htet, this, facet); 
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
					   const HomogeneityTet *htet,
					   const MultiFaceIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  return new MultiCornerIntersection(htet, this, fi);
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
					   const HomogeneityTet *htet,
					   const MultiVSBIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  return new MultiCornerIntersection(htet, fi, this);
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
					   const HomogeneityTet *htet,
					   const MultiCornerIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  return new MultiCornerIntersection(htet, fi, this);
}

bool MultiFaceIntersection::isMisordered(const PixelPlaneIntersection *fi,
					 const PixelPlaneFacet *facet)
  const
{
  return fi->referent()->isMisordered(this, facet); // double dispatch
}

bool MultiFaceIntersection::isMisordered(const SimpleIntersection *fi,
					 const PixelPlaneFacet *facet)
  const
{
  return fi->isMisordered(this, facet);
}

bool MultiFaceIntersection::isMisordered(const MultiFaceIntersection *fi,
					 const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(this, fi);
}

bool MultiFaceIntersection::isMisordered(const MultiVSBIntersection *fi,
					 const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(this, fi);
}

bool MultiFaceIntersection::isMisordered(const MultiCornerIntersection *fi,
					 const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(this, fi);
}

void MultiFaceIntersection::print(std::ostream &os) const {
  os << "MultiFaceIntersection(" << printPlanes() << ", " << location3D()
     << ", " << crossingType() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MultiVSBIntersection::MultiVSBIntersection(const HomogeneityTet *htet,
					   const PixelPlaneFacet *facet,
					   const SimpleIntersection *fi0,
					   const SimpleIntersection *fi1)
{
// #ifdef DEBUG
//   if(fi0->getFacePlane() != fi1->getFacePlane()) {
//     oofcerr << "MultiVSBIntersection::ctor: fi0=" << *fi0 << std::endl;
//     oofcerr << "MultiVSBIntersection::ctor: fi1=" << *fi1 << std::endl;
//     oofcerr << "MultiVSBIntersection::ctor: fi0->faceplane="
// 	    << fi0->getFacePlane() << " " << *fi0->getFacePlane() << std::endl;
//     oofcerr << "MultiVSBIntersection::ctor: fi1->faceplane="
// 	    << fi1->getFacePlane() << " " << *fi1->getFacePlane() <<  std::endl;
//     throw ErrProgrammingError("Face planes don't match!", __FILE__, __LINE__);
//   }
// #endif // DEBUG
  assert(fi0->onOnePolySegment(fi1, facet));
  assert(!fi0->onSameLoopSegment(fi1));
#ifdef DEBUG
  verbose = fi0->verbose || fi1->verbose;
#endif // DEBUG
  copyPlanes(fi0, fi1);
  setCrossingType(combinedCrossing(fi0, fi1));
  setPolyFrac(fi0->getPolyFrac(NONE, facet));
  setFacePlane(fi0->getFacePlane());
  // TODO: Enforce that each vsb segment fraction is either 0 or 1
  vsbSegments[fi0->getLoopSeg()] = fi0->getLoopFrac();
  vsbSegments[fi1->getLoopSeg()] = fi1->getLoopFrac();
  computeLocation();
}

MultiVSBIntersection::MultiVSBIntersection(const HomogeneityTet *htet,
#ifdef DEBUG
					   const PixelPlaneFacet *facet,
#endif // DEBUG
					   const SimpleIntersection *si,
					   const MultiVSBIntersection *mvi)
{
  assert(si->onOnePolySegment(mvi, facet));
#ifdef DEBUG
  verbose = si->verbose || mvi->verbose;
#endif // DEBUG
  copyPlanes(si, mvi);
  setCrossingType(combinedCrossing(si, mvi));
  setPolyFrac(si->getPolyFrac(NONE, facet));
  setFacePlane(si->getFacePlane());
  vsbSegments[si->getLoopSeg()] = si->getLoopFrac();
  vsbSegments.insert(mvi->getLoopSegs().begin(), mvi->getLoopSegs().end());
  computeLocation();
}

MultiVSBIntersection *MultiVSBIntersection::clone() const {
  return new MultiVSBIntersection(*this);
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  const HomogeneityTet *htet,
					  const PixelPlaneIntersection *fi,
					  const PixelPlaneFacet *facet)
  const
{
  if(fi)
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
						  const HomogeneityTet *htet,
						  const SimpleIntersection *fi,
						  const PixelPlaneFacet *facet)
  const
{
  // SimpleIntersection::mergeWith(MultiVSBIntersection) is equivalent
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  const HomogeneityTet *htet,
					  const MultiFaceIntersection *fi,
					  const PixelPlaneFacet *facet)
  const
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  const HomogeneityTet *htet,
					  const MultiVSBIntersection *fi,
					  const PixelPlaneFacet *facet)
  const
{
  // Both intersections are on a voxel corner, so they had better be
  // on the same corner. 
  if(!samePixelPlanes(fi))
    return nullptr;
  // If they share the same face, too, then they're really the same
  // corner, and the mergee is the same as the two mergers.
  if(getFacePlane() == fi->getFacePlane())
    return clone();
  return new MultiCornerIntersection(htet, this, fi);
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  const HomogeneityTet *htet,
					  const MultiCornerIntersection *fi,
					  const PixelPlaneFacet *facet)
  const
{
  // Both intersections are on a voxel corner, so they had better be
  // on the same corner.  They had also better share a tet face.
  if(!samePixelPlanes(fi) || !onSameFacePlane(fi, facet->getBaseFacePlane()))
    return nullptr;
  return new MultiCornerIntersection(htet, this, fi);
}

bool MultiVSBIntersection::isMisordered(const PixelPlaneIntersection *fi,
					const PixelPlaneFacet *facet)
  const
{
  return fi->referent()->isMisordered(this, facet); // double dispatch
}

bool MultiVSBIntersection::isMisordered(const SimpleIntersection *fi,
					const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(fi, this);
}

bool MultiVSBIntersection::isMisordered(const MultiFaceIntersection *fi,
					const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(fi, this);
}

bool MultiVSBIntersection::isMisordered(const MultiVSBIntersection *fi,
					const PixelPlaneFacet *facet)
  const
{
  // Two MultiVSBIntersections at the same VSB corner (they have to be
  // at the same corner if they're close enough to be examined here)
  // are always coincidental.

  /* This can only happen if the same polygon corner is considered to
  // intersect two voxel corners in a checkerboard layout:
  //
  //             |..........
  //             |..........
  //             |..........    It doesn't matter how the polygon 
  //             |..........    segments are arranged as long as
  //    ---------o----------    they meet at the VSB corner.
  //    ......../|\  
  //    ......./.| \  
  //    ....../..|  \  
  //    ...../...|   \  
  */
  
  return true;
}

bool MultiVSBIntersection::isMisordered(const MultiCornerIntersection *fi,
					const PixelPlaneFacet *facet)
  const
{
  // This is just like two MultiVSBIntersections, only more so.
  return true;
}

void MultiVSBIntersection::print(std::ostream &os) const {
  os << "MultiVSBIntersection(" << printPlanes() << ", " << location3D()
     << ", " << crossingType() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MultiCornerIntersection::MultiCornerIntersection(
					 const HomogeneityTet *htet,
					 const PixelPlaneIntersectionNR *fi0,
					 const PixelPlaneIntersectionNR *fi1)
{
  setCrossingType(combinedCrossing(fi0, fi1));
#ifdef DEBUG
  verbose = fi0->verbose || fi1->verbose;
#endif // DEBUG
  copyPlanes(fi0, fi1);
  computeLocation();
  // TODO: In debug mode, check that the faces actually pass through
  // the intersection point as determined by the pixel planes?
// #ifdef DEBUG
//   oofcerr << "MultiCornerIntersection::ctor: built " << *this << std::endl;
//   OOFcerrIndent indent(2);
//   oofcerr << "MultiCornerIntersection::ctor: from fi0=" << *fi0 << std::endl;
//   oofcerr << "MultiCornerIntersection::ctor:  and fi1=" << *fi1 << std::endl;
// #endif // DEBUG
}

MultiCornerIntersection *MultiCornerIntersection::clone() const {
  return new MultiCornerIntersection(*this);
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     const HomogeneityTet *htet,
					     const PixelPlaneIntersection *fi,
					     const PixelPlaneFacet *facet)
  const
{
  if(fi)
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}


PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     const HomogeneityTet *htet,
					     const SimpleIntersection *fi,
					     const PixelPlaneFacet *facet)
  const
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     const HomogeneityTet *htet,
					     const MultiFaceIntersection *fi,
					     const PixelPlaneFacet *facet)
const
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     const HomogeneityTet *htet,
					     const MultiVSBIntersection *fi,
					     const PixelPlaneFacet *facet)
const
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     const HomogeneityTet *htet,
					     const MultiCornerIntersection *fi,
					     const PixelPlaneFacet *facet)
  const
{
  // This really can't happen unless the intersections are already at
  // the same point.  The point is determined by the voxel corner, so
  // there's no round-off error to worry about.
  if(location3D() != fi->location3D())
    return nullptr;
  return new MultiCornerIntersection(htet, this, fi);
}

bool MultiCornerIntersection::isMisordered(const PixelPlaneIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  return fi->referent()->isMisordered(this, facet); // double dispatch
}
  

bool MultiCornerIntersection::isMisordered(const SimpleIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(fi, this);
}

bool MultiCornerIntersection::isMisordered(const MultiFaceIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  return facet->badTopology(fi, this);
}

bool MultiCornerIntersection::isMisordered(const MultiVSBIntersection *fi,
					   const PixelPlaneFacet *facet)
  const
{
  // See comment in MultiVSBIntersection::isMisordered(MultiVSBIntersection)
  return true;
}

bool MultiCornerIntersection::isMisordered(const MultiCornerIntersection*,
					   const PixelPlaneFacet*)
  const
{
  return true;
}

void MultiCornerIntersection::print(std::ostream &os) const {
  os << "MultiCornerIntersection(" << printPlanes() << ", " << location3D()
     << ", " << crossingType() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RedundantIntersection::RedundantIntersection(PixelPlaneIntersection *ppi,
					     PixelPlaneFacet *facet)
  : referent_(ppi->referent()), facet_(facet)
{
  facet_->newRedundantIntersection(this);
}

RedundantIntersection::~RedundantIntersection() {
  facet_->removeRedundantIntersection(this);
}

RedundantIntersection *RedundantIntersection::clone() const {
  return new RedundantIntersection(referent_, facet_);
}

void RedundantIntersection::print(std::ostream &os) const {
  os << "RedundantIntersection(" << *referent_ << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

TetEdgeIntersection::TetEdgeIntersection(const FacePlane *f0,
					 const FacePlane *f1,
					 const HPixelPlane *pp)
{
  f0->addToIntersection(this);
  f1->addToIntersection(this);
  pp->addToIntersection(this);
  // faces_.insert(f0);
  // faces_.insert(f1);
  // pixelPlanes_.insert(pp);
  loc_ = triplePlaneIntersection(f0, f1, pp);
  setCrossingType(NONCROSSING);
}

TetEdgeIntersection *TetEdgeIntersection::clone() const {
  return new TetEdgeIntersection(*this);
}

void TetEdgeIntersection::print(std::ostream &os) const {
  os << "TetEdgeIntersection(" << printPlanes() << ", " << location3D()
     << ", " << crossingType() <<  ")";
}


TetNodeIntersection::TetNodeIntersection(const HomogeneityTet *htet,
					 const HPixelPlane *pp,
					 unsigned int node)
{
  // TODO: One of the faces will either not create a polygon edge or
  // will be redundant with another plane.  If it's redundant, that's
  // ok -- planes are stored in sets so redundancies are eliminated.
  // Do we have to worry about faces that don't create polygon edges?
  for(unsigned int i=0; i<3; i++) {
    unsigned int f = CSkeletonElement::nodeFaces[node][i];
    const FacePlane *fp = htet->getFacePlane(f);
    fp->addToIntersection(this);
  }
  pp->addToIntersection(this);
  // // TODO: One of the faces will either not create a polygon edge or
  // // will be redundant with another plane.  Don't include it in the
  // // set of faces.
  // for(unsigned int i=0; i<3; i++) {
  //   unsigned int f = CSkeletonElement::nodeFaces[node][i];
  //   const FacePixelPlane *fpp = htet->getCoincidentPixelPlane(f);
  //   if(fpp != nullptr)
  //     pixelFaces_.insert(fpp);
  //   else
  //     faces_.insert(htet->getFacePlane(f));
  // }
  // const FacePixelPlane *fpp = htet->getCoincidentFacePlane(pp);
  // if(fpp != nullptr)
  //   pixelFaces_.insert(fpp);
  // else
  //     pixelPlanes_.insert(pp);
  loc_ = htet->nodePosition(node);
}

TetNodeIntersection *TetNodeIntersection::clone() const {
  return new TetNodeIntersection(*this);
}

void TetNodeIntersection::print(std::ostream &os) const {
  os << "TetNodeIntersection(" << printPlanes() << ", " << location3D()
     << ", " << crossingType() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

TriplePixelPlaneIntersection::TriplePixelPlaneIntersection(
						   const HPixelPlane *pp0,
						   const HPixelPlane *pp1,
						   const HPixelPlane *pp2)
{
  // assert(pp0 == htet->getUnorientedPixelPlane(pp0));
  // assert(pp1 == htet->getUnorientedPixelPlane(pp1));
  // assert(pp2 == htet->getUnorientedPixelPlane(pp2));
  pp0->addToIntersection(this);
  pp1->addToIntersection(this);
  pp2->addToIntersection(this);
  // addPixelPlane(htet, pp0);
  // addPixelPlane(htet, pp1);
  // addPixelPlane(htet, pp2);
  setCrossingType(NONCROSSING);
  computeLocation();
}

TriplePixelPlaneIntersection *TriplePixelPlaneIntersection::clone() const {
  return new TriplePixelPlaneIntersection(*this);
}

void TriplePixelPlaneIntersection::print(std::ostream &os) const {
  os << "TriplePixelPlaneIntersection(" << printPlanes() << ", "
     << location3D() << ", " << crossingType() << ")";
}

unsigned int TriplePixelPlaneIntersection::findFaceEdge(unsigned int,
							const HomogeneityTet*)
  const
{
  return NONE;
}

unsigned int TriplePixelPlaneIntersection::getPolyEdge(const PixelPlaneFacet*)
  const
{
  return NONE;
}

unsigned int TriplePixelPlaneIntersection::minPolyEdge(const PixelPlaneFacet*)
  const
{
  return NONE;
}

unsigned int TriplePixelPlaneIntersection::maxPolyEdge(const PixelPlaneFacet*)
  const
{
  return NONE;
}

double TriplePixelPlaneIntersection::getPolyFrac(unsigned int,
						 const PixelPlaneFacet*)
  const
{
  throw ErrProgrammingError("This should not be called.", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


std::ostream &operator<<(std::ostream &os, const PlaneIntersection &pi) {
  pi.print(os);
  return os;
}

std::ostream &operator<<(std::ostream &os, const CrossingType ct) {
  if(ct == ENTRY)
    os << "ENTRY";
  else if(ct == EXIT)
    os << "EXIT";
  else
    os << "NONCROSSING";
  return os;
}
