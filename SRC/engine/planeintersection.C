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

// TODO: Split up this file.

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

static std::string eqPrint(IsecEquivalenceClass *eqptr) {
  if(eqptr == nullptr)
    return "None";
  return to_string(eqptr->id);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PlaneIntersection::PlaneIntersection(HomogeneityTet *htet)
  : htet(htet),
    equivalence_(nullptr)
#ifdef DEBUG
  , verbose(false)
#endif // DEBUG
{
  setID(htet);
#ifdef DEBUG
  HomogeneityTet::allIntersections.insert(this);
  // oofcerr << "PlaneIntersection::ctor: " << this << std::endl;
#endif // DEBUG
}

PlaneIntersection::~PlaneIntersection() {
#ifdef DEBUG
  HomogeneityTet::allIntersections.erase(this);
  // oofcerr << "PlaneIntersection::dtor: " << this << std::endl;
#endif // DEBUG
  removeEquivalence();
}

PlaneIntersection::PlaneIntersection(const PlaneIntersection &other)
  : htet(other.htet),
    equivalence_(other.equivalence_)
#ifdef DEBUG
  , verbose(other.verbose)
#endif // DEBUG
{
  setID(htet);
  if(equivalence_ != nullptr)
    equivalence_->addIntersection(this);
}

const BarycentricCoord &PlaneIntersection::baryCoord(HomogeneityTet *htet) const
{
// #ifdef DEBUG
//   if(htet->verbosePlane()) {
//     oofcerr << "PlaneIntersection::baryCoord: this=" << *this << std::endl;
//     oofcerr << "PlaneIntersection::baryCoord: loc=" << location3D()
// 	    << std::endl;
//   }
// #endif // DEBUG
  const BarycentricCoord &b = htet->getBarycentricCoord(location3D());
// #ifdef DEBUG
//   if(htet->verbosePlane()) {
//     oofcerr << "PlaneIntersection::baryCoord: back from getBarycentricCoord"
// 	    << std::endl;
//     oofcerr << "PlaneIntersection::baryCoord: b=" << b << std::endl;
//   }
// #endif	// DEBUG
  return b;
}

void PlaneIntersection::setEquivalence(IsecEquivalenceClass *e) {
// #ifdef DEBUG
//   if(htet->verbosePlane()) {
//     oofcerr << "PlaneIntersection::setEquivalence: " << this << "  "
// 	    << *this << " e=" << e;
//     if(e)
//       oofcerr << " " << *e;
//     oofcerr << std::endl;
//   }
//   OOFcerrIndent indent(2);
// #endif // DEBUG

#ifdef DEBUG
  double dist2 = norm2(getLocation3D() - e->location3D());
  if(dist2 > 1.e-10) {
    oofcerr << "PlaneIntersection::setEquivalence: incompatible positions!"
	    << std::endl;
    OOFcerrIndent indent(2);
    oofcerr << "PlaneIntersection::setEquivalence: this=" << *this
	    << std::endl;
    oofcerr << "PlaneIntersection::setEquivalence: here=" << getLocation3D()
	    << " eqpos=" << e->location3D()
	    << " diff=" << getLocation3D()-e->location3D()
	    << " dist=" << sqrt(dist2)
	    << std::endl;
    e->dump();
    throw ErrProgrammingError("Incompatible equivalence class!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG

  // This may have been called via a RedundantIntersection's
  // setEquivalence method, in which case there's nothing to do.
  if(equivalence() == e)
    return;
  
  removeEquivalence();
  equivalence_ = e;
  if(e != nullptr) {		// TODO: is this check necessary?
    e->addIntersection(this);
    // TODO: When setEquivalence is called from
    // IsecEquivalenceClass::merge, it's not necessary to call
    // addPlanesToEquivalence().
    addPlanesToEquivalence(e);
  }
  
// #ifdef DEBUG
//   if(htet->verbosePlane()) {
//     if(e != nullptr)
//       oofcerr << "PlaneIntersection::setEquivalence: done, eqclass="
// 	      << *e
// 	      << " this=" << *this
// 	      << std::endl;
//     else
//       oofcerr << "PlaneIntersection::setEquivalence: done, e=0x0, this="
// 	      << *this << std::endl;
//   }
// #endif // DEBUG
}

bool PlaneIntersection::isEquivalent(const PlaneIntersection *other) const {
  return other->equivalence() == equivalence();
}

Coord3D PlaneIntersection::location3D() const {
  if(equivalence_ != nullptr)
    return equivalence_->location3D();
  return getLocation3D();
}

void PlaneIntersection::setEquivalenceOnly(IsecEquivalenceClass *e) {
  equivalence_ = e;
}

void PlaneIntersection::removeEquivalence() {
  // removeEquivalence is called from the PlaneIntersection
  // destructor, so it can't invoke any PlaneIntersection virtual
  // methods.
  if(equivalence_ != nullptr) {
    equivalence_->removeIntersection(this);
  }
  equivalence_ = nullptr;
}

void PlaneIntersection::setID(HomogeneityTet *htet) {
  id = htet->nextIntersectionID();
}

// sharedPlane returns any kind of plane (pixel plane or face plane)
// that's shared between this PlaneIntersection and the other one,
// excluding the face who's tet index is 'exlcude'.

const HPlane *PlaneIntersection::sharedPlane(const PlaneIntersection *other,
					     unsigned int exclude)
  const
{
  const FacePlane *excludeface = (exclude == NONE ?
				  nullptr :
				  htet->getTetFacePlane(exclude));
  const HPlane *ushared = equivalence()->sharedPlane(other->equivalence(),
						     excludeface);
  // The plane returned by IsecEquivalenceClass::sharedPlane is
  // unoriented.  Return the correct orientation as used by this
  // intersection.
  if(ushared == nullptr)
    return ushared;
  return orientedPlane(ushared);
}

  
#ifdef DEBUG

bool PlaneIntersection::verify() {
  if(equivalence_ != nullptr) {
    if(!equivalence_->contains(this))
      return false;
  }
  return true;
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// GenericIntersection is the intersection of some planes, with no
// special information about them.

GenericIntersection *GenericIntersection::clone(HomogeneityTet *htet) const {
  GenericIntersection *bozo = new GenericIntersection(*this);
  bozo->setID(htet);
  return bozo;
}

void GenericIntersection::setLocation(const Coord3D &pos) {
  loc_ = fixedLocation(pos);
}

void GenericIntersection::print(std::ostream &os) const {
  os << "GenericIntersection(" << printPlanes() << ", " << loc_ << ")";
}

std::string GenericIntersection::shortName() const {
  return "G" + IntersectionPlanes<PlaneIntersection>::shortName();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TripleFaceIntersection is the intersection of three tetrahedron
// faces.

TripleFaceIntersection::TripleFaceIntersection(unsigned int node,
					       HomogeneityTet *htet)
  : PlaneIntersection(htet),
    node_(node)
{
  for(unsigned int i=0; i<3; i++)
    faces_.insert(htet->getTetFacePlane(CSkeletonElement::nodeFaces[node][i]));
  loc_ = htet->nodePosition(node);
}

TripleFaceIntersection *TripleFaceIntersection::clone(HomogeneityTet *htet)
  const
{
  TripleFaceIntersection *tfi = new TripleFaceIntersection(*this);
  tfi->setID(htet);
  return tfi;
}

const BarycentricCoord &TripleFaceIntersection::baryCoord(HomogeneityTet *htet)
  const
{
  return nodeBCoord(node_);
}

void TripleFaceIntersection::print(std::ostream &os) const {
  os << "TripleFaceIntersection(node=" << node_ << ", " << location3D()
     << ", eq=" << eqPrint(equivalence_) << ")";
}

std::string TripleFaceIntersection::shortName() const {
  std::string str("T");
  for(const FacePlane *face : faces_)
    str += face->shortName();
  return str;
}

unsigned int TripleFaceIntersection::findFaceEdge(unsigned int face,
						  HomogeneityTet *htet)
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

void TripleFaceIntersection::copyPlanesToIntersection(
					      IntersectionPlanesBase *gi)
  const
{
  for(const FacePlane *face : faces_)
    face->addToIntersection(gi);
}

// bool TripleFaceIntersection::isEquivalent(const PlaneIntersection *pi) const
// {
//   if(equivalence() != nullptr && equivalence() == pi->equivalence())
//     return true;
//   return pi->isEquiv(this); // double dispatch
// }

// bool TripleFaceIntersection::isEquiv(const TripleFaceIntersection *tfi)
//   const
// {
//   return node_ == tfi->getNode();
// }

// bool TripleFaceIntersection::isEquiv(const IntersectionPlanesBase *ppi)
//   const
// {
//   return ppi->isEquiv(this);
// }

// bool TripleFaceIntersection::isEquiv(const RedundantIntersection *ri) const
// {
//   return ri->referent()->isEquiv(this);
// }

void TripleFaceIntersection::addPlanesToEquivalence(
					    IsecEquivalenceClass *eqclass)
{
  for(const FacePlane *face : faces_) {
    // face might be either a FacePlane or a FacePixelPlane and needs
    // to be put in the correct set in eqclass via this virtual
    // function call.
    face->addToEquivalence(eqclass);
  }
}

bool TripleFaceIntersection::belongsInEqClass(
				      const IsecEquivalenceClass *eqclass)
  const
{
  unsigned int nfaces = 0;
  for(const FacePlane *face : faces_) {
    if(face->isInEquivalence(eqclass))
      nfaces++;
  }
  return nfaces == 3;
}

const HPixelPlane *TripleFaceIntersection::sharedPixelPlane(
						   const PlaneIntersection*,
						   unsigned int)
  const
{
  return nullptr;
}

const HPixelPlane *TripleFaceIntersection::getSharedPixelPlane(
					    const TripleFaceIntersection*,
					    unsigned int)
const
{
  return nullptr;
}

const HPixelPlane *TripleFaceIntersection::getSharedPixelPlane(
					    const IntersectionPlanesBase*,
					    unsigned int)
const
{
  return nullptr;
}

const HPixelPlane *TripleFaceIntersection::getSharedPixelPlane(
					    const RedundantIntersection*,
					    unsigned int)
const
{
  return nullptr;
}

const FacePlane *TripleFaceIntersection::sharedFace(const PlaneIntersection *pi,
						    const FacePlane *exclude)
  const
{
  return pi->getSharedFace(this, exclude); // double dispatch
}

const FacePlane *TripleFaceIntersection::getSharedFace(
					    const TripleFaceIntersection *tpi,
					    const FacePlane *exclude)
  const
{
  FacePlaneSet::const_iterator i = sharedEntry(faces_, tpi->faces(), exclude);
  assert(i != faces_.end());
  return *i;
}

const FacePlane *TripleFaceIntersection::getSharedFace(
					    const IntersectionPlanesBase *ppi,
					    const FacePlane *exclude)
  const
{
  // Let IntersectionPlanesBase do the work, since it's the more
  // complicated object.
  return ppi->getSharedFace(this, exclude); 
}

const FacePlane *TripleFaceIntersection::getSharedFace(
					    const RedundantIntersection *ri,
					    const FacePlane *exclude)
  const
{
  return ri->referent()->getSharedFace(this, exclude);
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

unsigned int PixelPlaneIntersection::nSharedPolySegments(
					const PixelPlaneIntersection *fi,
					const PixelPlaneFacet *facet)
  const
{
  const FacePixelPlane *base = facet->getBaseFacePlane();
  FacePlaneSet shared = referent()->sharedFaces(fi->referent(), base);
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "PixelPlaneIntersection::nSharedPolySegments: shared faces=";
//     for(auto f : shared)
//       oofcerr << " " << *f;
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
  // If there are 0 or 1 shared faces (excluding the base plane), then
  // there are 0 or 1 shared polygon edges.
  if(shared.size() < 2)
    return shared.size();
  // If there are 2 shared faces, there may be only one shared polygon
  // edge if the shared faces are collinear with the base plane.
  if(shared.size() == 2) {
    if(facet->htet->areCollinear(facet->pixplane, *shared.begin(),
				 *shared.rbegin()))
      {
	return 1;
      }
    return 2;
  }
  // There are three shared faces.  The points are at a tet vertex
  // that lies in the pixel plane.
  return 2;
}

// onOnePolySegment returns true if two intersections share exactly
// one polygon segment.

bool PixelPlaneIntersection::onOnePolySegment(const PixelPlaneIntersection *fi,
					      const PixelPlaneFacet *facet)
  const
{
// #ifdef DEBUG
//   if(facet->verbose) {
//     oofcerr << "PixelPlaneIntersection::onOnePolySegment: this=" << *this
// 	    << std::endl;
//     oofcerr << "PixelPlaneIntersection::onOnePolySegment:   fi=" << *fi
// 	    << std::endl;
//   }
// #endif // DEBUG
  FacePlaneSet shared = referent()->sharedFaces(fi->referent(),
						facet->getBaseFacePlane());
// #ifdef DEBUG
//   if(facet->verbose) {
//     oofcerr << "PixelPlaneIntersection::onOnePolySegment: base plane="
// 	    << facet->getBaseFacePlane();
//     if(facet->getBaseFacePlane())
//       oofcerr << " " << *facet->getBaseFacePlane();
//     oofcerr << std::endl;
//     oofcerr << "PixelPlaneIntersection::onOnePolySegment: facet plane="
// 	    << *facet->pixplane << std::endl;
//     oofcerr << "PixelPlaneIntersection::onOnePolySegment: shared.size="
// 	    << shared.size() << std::endl;
//     for(const FacePlane *fp : shared) {
//       oofcerr << "PixelPlaneIntersection::onOnePolySegment:  shared plane="
// 	      << fp << " " << *fp << std::endl;
//     }
//   }
// #endif // DEBUG
  if(shared.size() == 1)
    return true;
  if(shared.size() == 2) {
    if(facet->htet->areCollinear(facet->pixplane,
				 *shared.begin(), *shared.rbegin()))
      return true;
  }
  return false;
} // end PixelPlaneIntersection::onOnePolySegment

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void PixelPlaneIntersectionNR::copyPlanes(const PixelPlaneIntersectionNR *fi0,
					  const PixelPlaneIntersectionNR *fi1)
{
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneIntersectionNR::copyPlanes" << std::endl;
// #endif // DEBUG
  pixelPlanes_.insert(fi0->pixelPlanes_.begin(), fi0->pixelPlanes_.end());
  pixelPlanes_.insert(fi1->pixelPlanes_.begin(), fi1->pixelPlanes_.end());
  faces_.insert(fi0->faces_.begin(), fi0->faces_.end());
  faces_.insert(fi1->faces_.begin(), fi1->faces_.end());
  pixelFaces_.insert(fi0->pixelFaces_.begin(), fi0->pixelFaces_.end());
  pixelFaces_.insert(fi1->pixelFaces_.begin(), fi1->pixelFaces_.end());
  
  //  TODO: This check needs to allow more than 3 planes if the
  //  intersection includes both the + and - versions of a plane.
// #ifdef DEBUG
//   if(pixelPlanes_.size() + pixelFaces_.size() > 3) {
//     oofcerr << "PixelPlaneIntersectionNR::copyPlanes: Too many pixel planes!"
// 	    << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::copyPlanes: fi0=" << *fi0
// 	    << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::copyPlanes: fi1=" << *fi1
// 	    << std::endl;
//     throw ErrProgrammingError("Too many pixel planes!", __FILE__, __LINE__);
//   }
// #endif // DEBUG
}

static void includeNonRedundantPlane(const HPlane *plane,
				     std::vector<const HPlane*> &planes)
{
  if(planes.empty())
    planes.push_back(plane);
  else {
    for(const HPlane *p : planes)
      if(p->coincident(*plane))
	return;
    planes.push_back(plane);
  }
}

void IntersectionPlanesBase::computeLocation() {
  // If an intersection was constructed by merging intersections that
  // contained oppositely oriented but coincident pixel planes, we
  // have to be sure to include three independent planes in the set
  // being used to compute the location.
  Coord3D pos;
  std::vector<const HPlane*> planes;
  for(const HPlane *pp : pixelPlanes_) {
    includeNonRedundantPlane(pp, planes);
    if(planes.size() == 3)
      break;
  }
  if(planes.size() < 3) {
    for(const HPlane *fpp : pixelFaces_) {
      includeNonRedundantPlane(fpp, planes);
      if(planes.size() == 3)
      break;
    }
  }
  if(planes.size() < 3) {
    // There aren't enough pixel planes to determine the location, so
    // use some faces too.  They can't be coincident with the pixel
    // planes, so don't bother calling includeNonRedundantPlane.
    int nToAdd = 3 - planes.size();
    for(const HPlane *face : faces_) {
      planes.push_back(face);
      if(--nToAdd == 0)
	break;
    }
    // If there are three non-collinear pixel planes, then
    // triplePlaneIntersection doesn't need to be called, because
    // setLocation will set all the components of pos to the pixel
    // plane offsets.
    pos = triplePlaneIntersection(planes[0], planes[1], planes[2]);
  }
  setLocation(pos);
  
//   int npixplanes = pixelPlanes_.size() + pixelFaces_.size();
//   if(npixplanes < 3) {
//     std::vector<const Plane*> planes;
//     planes.insert(planes.end(), pixelPlanes_.begin(), pixelPlanes_.end());
//     planes.insert(planes.end(), pixelFaces_.begin(), pixelFaces_.end());
//     int nToAdd = 3 - npixplanes;
//     if(nToAdd > 0) {
//       for(const Plane *face : faces_) {
// 	// If npixplanes==2, check that the plane being added doesn't
// 	// contain the intersection line of the pixplanes.
// 	if(npixplanes != 2 || face->nonDegenerate(planes[0], planes[1])) {
// 	  planes.push_back(face);
// 	  if(--nToAdd == 0)
// 	    break;
// 	}
//       }
//     }
// #ifdef DEBUG
//     if(planes.size() != 3) {
//       // This is called from constructors before "verbose" is set, so
//       // don't bother checking for it.
//       oofcerr << "IntersectionPlanesBase::computeLocation:"
// 	      << " wrong number of planes!" << std::endl;
//       oofcerr << "IntersectionPlanesBase::computeLocation: planes=";
//       std::cerr << derefprint(planes);
//       oofcerr << std::endl;
//       throw ErrProgrammingError(
// 			"IntersectionPlanesBase::computeLocation failed!",
// 			__FILE__, __LINE__);
//     }
// #endif // DEBUG
//     pos = triplePlaneIntersection(planes[0], planes[1], planes[2]);
//   }
//   // If there are three pixel planes, then pos is uninitialized, but
//   // the value passed to setLocation is irrelevant.
//   setLocation(pos);
}

void PixelPlaneIntersectionNR::setLocation(const Coord3D &pos) {
  loc_ = fixedLocation(pos);
}

Coord3D IntersectionPlanesBase::fixedLocation(const Coord3D &pt) const {
  // Make sure that the point is exactly on all of the pixel planes.
  Coord3D fixed = pt;
  for(const HPixelPlane *pixplane : pixelPlanes_)
    fixed[pixplane->direction()] = pixplane->normalOffset();
  for(const FacePixelPlane *fpp : pixelFaces_)
    fixed[fpp->direction()] = fpp->normalOffset();
  return fixed;
}

// template <class PlaneSet0, class PlaneSet1>
// bool PixelPlaneIntersectionNR::includeCollinearPlanes_(
// 				       const CollinearPlaneMap &coplanes,
// 				       const PlaneSet0 &planes0,
// 				       const PlaneSet1 &planes1)
// {
//   bool changed = false;
//   for(const HPlane *p0 : planes0) {
//     for(const HPlane *p1 : planes1) {
//       if(p0 != p1) {
// 	auto matches =
// 	  coplanes.equal_range(CollinearPlaneMap::key_type(p0, p1));
// 	for(auto i=matches.first; i!=matches.second; i++) {
// 	  (*i).second->addToIntersection(this);
// 	  changed = true;
// 	}
//       }
//     }
//   }
//   return changed;
// }

// void PixelPlaneIntersectionNR::includeCollinearPlanes(HomogeneityTet *htet) {
//   const CollinearPlaneMap &coplanes = htet->collinearPlanes;

//   // TODO: Keep track of whether collinear planes are up to date and
//   // don't recompute unless necessary.
//   bool mod = includeCollinearPlanes_(coplanes, pixelPlanes_, pixelPlanes_);
//   mod = includeCollinearPlanes_(coplanes, faces_, faces_) || mod;
//   mod = includeCollinearPlanes_(coplanes, pixelFaces_, pixelFaces_) || mod;
//   mod = includeCollinearPlanes_(coplanes, pixelPlanes_, faces_) || mod;
//   mod = includeCollinearPlanes_(coplanes, pixelPlanes_, pixelFaces_) || mod;
//   mod = includeCollinearPlanes_(coplanes, pixelFaces_, faces_) || mod;
//   if(mod && equivalence_ != nullptr) {
//     addPlanesToEquivalence(equivalence());
//   }
// }

template <class BASE>
void IntersectionPlanes<BASE>::copyPlanesToIntersection(
						IntersectionPlanesBase *gi)
  const
{
  // All of these could be written as pp->addToIntersection(gi), but
  // that adds an unnecessary virtual function call.
  for(const HPixelPlane *pp : pixelPlanes_)
    gi->pixelPlanes().insert(pp);
  for(const FacePlane *fp : faces_)
    gi->faces().insert(fp);
  for(const FacePixelPlane *fpp : pixelFaces_)
    gi->pixelFaces().insert(fpp);
}
							
template <class BASE>
bool IntersectionPlanes<BASE>::samePixelPlanes(const PlaneIntersection *pi)
  const
{
  return pi->samePixPlanes(this); // double dispatch
}

template <class BASE>
bool IntersectionPlanes<BASE>::samePixPlanes(
				       const IntersectionPlanesBase *other)
  const
{
  return (pixelPlanes_ == other->pixelPlanes() &&
	  pixelFaces_ == other->pixelFaces());
}

template <class BASE>
bool IntersectionPlanes<BASE>::samePixPlanes(const TripleFaceIntersection*)
  const
{
  return false;
}

template <class BASE>
bool IntersectionPlanes<BASE>::samePixPlanes(const RedundantIntersection *ri)
  const
{
  return ri->referent()->samePixPlanes(this);
}

template <class BASE>
const HPixelPlane *IntersectionPlanes<BASE>::sharedPixelPlane(
					      const PlaneIntersection *pi,
					      unsigned int face)
  const
{
  return pi->getSharedPixelPlane(this, face); // double dispatch
}

template <class BASE>
const HPixelPlane *IntersectionPlanes<BASE>::getSharedPixelPlane(
						 const TripleFaceIntersection*,
						 unsigned int)
  const
{
  return nullptr;
}

template <class BASE>
const HPixelPlane *IntersectionPlanes<BASE>::getSharedPixelPlane(
					   const IntersectionPlanesBase *ipb,
					   unsigned int face)
  const
{
  // auto iter = sharedEntry(pixelPlanes_, ipb->pixelPlanes());
  // if(iter != pixelPlanes_.end())
  //   return *iter;

  // When comparing pixel planes, consider oppositely directed planes
  // to be equivalent.  This means that we can't use the sharedEntry
  // template, because the comparison operator we're using is not the
  // one used to construct the sets of planes.

  // TODO: This loop is o(N^2), but N is small so it may not
  // matter. An o(N) algorithm can be made by using sharedEntry on a
  // set containing both the planes in ipb and their mirrors.
  for(const HPixelPlane *pp0 : pixelPlanes_) {
    for(const HPixelPlane *pp1 : ipb->pixelPlanes()) {
      if(pp0->coincident(*pp1)) {
	// Return pp1, not pp0, so that this->sharedPixelPlane(other)
	// returns the plane in this, not the plane in other.
	return pp1;
      }
    }
  }
  

  const FacePixelPlane *fpp = BASE::htet->getCoincidentPixelPlane(face);
  if(fpp == nullptr) {
    auto iter = sharedEntry(pixelFaces_, ipb->pixelFaces());
    if(iter != pixelFaces_.end())
      return *iter;
  }
  else {
    auto iter = sharedEntry(pixelFaces_, ipb->pixelFaces(), fpp);
    if(iter != pixelFaces_.end())
      return *iter;
  }
  return nullptr;
}

template <class BASE>
const HPixelPlane *IntersectionPlanes<BASE>::getSharedPixelPlane(
					     const RedundantIntersection *ri,
					     unsigned int face)
  const
{
  return ri->referent()->getSharedPixelPlane(this, face);
}

// const FacePlane *PixelPlaneIntersectionNR::sharedFace(
// 				      const PixelPlaneIntersectionNR *fi)
//   const
// {
//   const FacePlaneSet::const_iterator fp =
//     sharedEntry(faces_, fi->referent()->faces());
//   if(fp != faces_.end())
//     return *fp;
//   const FacePixelPlaneSet::const_iterator fpp =
//     sharedEntry(pixelFaces_, fi->referent()->pixelFaces());
//   if(fpp != pixelFaces_.end())
//     return *fpp;
//   return nullptr;
// }

template <class BASE>
const FacePlane *IntersectionPlanes<BASE>::sharedFace(
					      const PlaneIntersection *pi,
					      const FacePlane *exclude)
  const
{
  return pi->getSharedFace(this, exclude); // double dispatch
}

template <class BASE>
const FacePlane *IntersectionPlanes<BASE>::getSharedFace(
					      const TripleFaceIntersection *tfi,
					      const FacePlane *exclude)
  const
{
  for(const FacePlane *fp0 : BASE::equivalence_->facePlaneSets()) {
    if(fp0 != exclude) {
      for(const FacePlane *fp1 : tfi->faces()) {
	if(fp1 == fp0)
	  return fp0;
      }
    }
  }
  return nullptr;
}

template <class BASE>
const FacePlane *IntersectionPlanes<BASE>::getSharedFace(
				      const IntersectionPlanesBase *fi,
				      const FacePlane *exclude)
  const
{
  const FacePlaneSet::const_iterator fp = sharedEntry(
					      BASE::equivalence()->facePlanes,
					      fi->getEquivalence()->facePlanes,
					      exclude);
  if(fp != BASE::equivalence()->facePlanes.end()) {
    return *fp;
  }
  // We could have *another* double dispatch layer to see if "exclude"
  // is a FacePixelPlane, or we could just do this:
  const FacePixelPlane *fppNot = dynamic_cast<const FacePixelPlane*>(exclude);
  if(fppNot != nullptr) {
    const FacePixelPlaneSet::const_iterator fpp =
      sharedEntry(BASE::equivalence()->pixelFaces,
		  fi->getEquivalence()->pixelFaces, fppNot);
    if(fpp != BASE::equivalence()->pixelFaces.end()) {
      return *fpp;
      // return dynamic_cast<const FacePlane*>(*fpp);// TODO: Is cast needed?
    }
  }
  else {			// no excluded face plane
    const FacePixelPlaneSet::const_iterator fpp =
      sharedEntry(BASE::equivalence()->pixelFaces,
		  fi->getEquivalence()->pixelFaces);
    if(fpp != BASE::equivalence()->pixelFaces.end()) {
      return *fpp;
      // return dynamic_cast<const FacePlane*>(*fpp);  // TODO: Is cast needed?
    }
  }
  return nullptr;
}

template <class BASE>
const FacePlane *IntersectionPlanes<BASE>::getSharedFace(
					      const RedundantIntersection *ri,
					      const FacePlane *exclude)
  const
{
  return ri->referent()->getSharedFace(this, exclude);
}

template <class BASE>
const HPlane *IntersectionPlanes<BASE>::orientedPlane(const HPlane *plane)
  const
{
  // TODO: Use a virtual method in HPlane to get loop over the correct
  // set of planes.
  for(const HPixelPlane *pp : pixelPlanes_)
    if(pp->coincident(*plane))
      return pp;
  for(const FacePlane *fp : faces_)
    if(fp->coincident(*plane))
      return fp;
  for(const FacePixelPlane *fpp : pixelFaces_)
    if(fpp->coincident(*plane))
      return fpp;
  return nullptr;
}

FacePlaneSet PixelPlaneIntersectionNR::sharedFaces(
					   const PixelPlaneIntersection *fi,
					   const FacePlane *exclude)
  const
{
  return equivalence()->sharedFaces(fi->equivalence(), exclude);
  // FacePlaneSet shared;
  // // TODO: get faces from equivalence class.
  // std::set_intersection(faces_.begin(), faces_.end(),
  // 			fi->faces().begin(),
  // 			fi->faces().end(),
  // 			std::inserter(shared, shared.end()),
  // 			FacePlaneSet::key_compare());
  // std::set_intersection(pixelFaces_.begin(), pixelFaces_.end(),
  // 			fi->pixelFaces().begin(),
  // 			fi->pixelFaces().end(),
  // 			std::inserter(shared, shared.end()),
  // 			FacePixelPlaneSet::key_compare());
  // if(exclude)
  //   shared.erase(exclude);
  // return shared;
}

bool PixelPlaneIntersectionNR::onSameFacePlane(
				       const PixelPlaneIntersectionNR *fib,
				       const FacePixelPlane *exclude)
  const
{
  const FacePlane *shared = sharedFace(fib, exclude);
  return shared != nullptr;
}

// The PixelPlaneIntersectionNR includes a necessarily contiguous set of
// polygon edges.  Find the one that's at the upper end (ie most
// counterclockwise) of the set.

unsigned int PixelPlaneIntersectionNR::maxPolyEdge(const PixelPlaneFacet *facet)
  const
{
  // TODO: The result of this calculation could be computed and cached
  // in the equivalence class, although it might have to be updated
  // when the class changed.  Probably maxPolyEdge and minPolyEdge
  // should be cached together.
  unsigned int nn = facet->polygonSize();
  std::vector<bool> e(nn, false);
  // Find which polygon edges are used in the PixelPlaneIntersectionNR. 
  for(const FacePlane *fp : equivalence_->facePlaneSets()) {
    unsigned int edge = facet->getPolyEdge(fp);
// #ifdef DEBUG
//     if(verbose) {
//       oofcerr << "PixelPlaneIntersectionNR::maxPolyEdge: fp=" << *fp
// 	      << " edge=" << edge << std::endl;
//     }
// #endif // DEBUG
    if(edge != NONE)
      e[edge] = true;
  }
  // The last edge is the one whose successor is not in the set.
  for(unsigned int i=1; i<nn; i++)
    if(e[i-1] && !e[i])
      return i-1;
// #ifdef DEBUG
//   if(!(e[nn-1] && !e[0])) {
//     oofcerr << "PixelPlaneIntersectionNR::maxPolyEdge: this=" << *this
// 	    << std::endl;
//     oofcerr << "PixelPlaneIntersectionNR::maxPolyEdge: e=";
//     std::cerr << e;
//     oofcerr << std::endl;
//     throw ErrProgrammingError("maxPolyEdge failed!", __FILE__, __LINE__);
//   }
// #endif // DEBUG
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
  for(const FacePlane *fp : equivalence_->facePlaneSets()) {
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

// TODO: Get rid of CrossingType and setCrossingType.  Just use
// integer crossing counts.  Add bool isExit and isEntry if necessary.

void PixelPlaneIntersectionNR::setCrossingType(CrossingType ct) {
  if(ct == ENTRY)
    setCrossingCount(-1);
  else if(ct == EXIT)
    setCrossingCount(1);
}

CrossingType PixelPlaneIntersection::crossingType() const {
  int ct = crossingCount();
  if(ct < 0)
    return ENTRY;
  if(ct > 0)
    return EXIT;
  return NONCROSSING;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Which edge of the given face is this intersection on?

template <class BASE>
unsigned int IntersectionPlanes<BASE>::findFaceEdge(unsigned int f,
						    HomogeneityTet *htet)
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
//   if(BASE::verbose || htet->verboseFace()) {
//     oofcerr << "IntersectionPlanes::findFaceEdge: this=" << *this << std::endl;
//     oofcerr << "IntersectionPlanes::findFaceEdge: f=" << f << " " << *this
// 	    << std::endl;
//     oofcerr << "IntersectionPlanes::findFaceEdge: faceIDs=";
//     std::cerr << faceIDs;
//     oofcerr << std::endl;
//   }
// #endif	// DEBUG
  for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) { 
    unsigned int edge = CSkeletonElement::faceEdges[f][e]; // face -> tet scope
    unsigned int otherface = CSkeletonElement::getOtherFaceIndex(f, edge);
    if(faceIDs.find(otherface) != faceIDs.end()) {
// #ifdef DEBUG
//       if(BASE::verbose || htet->verboseFace()) {
// 	oofcerr << "IntersectionPlanes::findFaceEdge: face edge=" << e
// 		<< " tet edge=" << edge << " otherface=" << otherface
// 		<< std::endl;
// 	oofcerr << "IntersectionPlanes::findFaceEdge: returning " << e
// 		<< std::endl;
//       }
// #endif // DEBUG
      return e;
    }
  }
  return NONE;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Update the appropriate PolyEdgeIntersections object with data from
// this intersection.  Called from PixelPlaneFacet::completeLoops.

void PixelPlaneIntersectionNR::locateOnPolygonEdge(
				std::vector<PolyEdgeIntersections> &polyedges,
				const PixelPlaneFacet *facet)
  const
{
#ifdef DEBUG
  if(verbose) {
    oofcerr << "PixelPlaneIntersectionNR::locateOnPolygonEdge: " << *this
	    << std::endl;
    oofcerr << "PixelPlaneIntersectionNR::locateOnPolygonEdge: eq class="
	    << *equivalence_ << std::endl;
  }
#endif // DEBUG

  // This uses minPolyEdge instead of simply getPolyEdge, because it's
  // important that the edge used here is the same as the edge that
  // PixelPlaneFacet::addEdges uses when deciding whether it has to
  // add wrap-around edges.
  unsigned int edge = minPolyEdge(facet);
  assert(edge != NONE);
  polyedges[edge].push_back(this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// isEquiv_ is the guts of the two versions of
// PixelPlaneIntersectionNR::isEquivalent().  It determines whether
// two sets of planes (each made of pixel planes, face planes, and
// face pixel planes) have three nondegenerate planes in common.  It
// assumes that the given PixelPlaneSets only contain independent
// planes.

static bool isEquiv_(HomogeneityTet *htet,
		     const PixelPlaneSet &pp0, const FacePlaneSet &fp0,
		     const FacePixelPlaneSet &fpp0,
		     const PixelPlaneSet &pp1, const FacePlaneSet &fp1,
		     const FacePixelPlaneSet &fpp1)
{
  // TODO: Is it worth being cleverer about these searches?  All of
  // the sets are sorted, and that information isn't being used.  The
  // sets are small, but this is called often.
// #ifdef DEBUG
//   bool verbose = htet->verbosePlane() || htet->verboseFace();
// #endif	// DEBUG
  unsigned int npixplanes = 0;
  std::vector<const HPlane*> planes;
  planes.reserve(10);		// more than we'll need in all cases
  for(const HPixelPlane *thisplane : pp0) {
    for(const HPixelPlane *otherplane : pp1) {
      if(thisplane->coincident(*otherplane)) {
	++npixplanes;
	planes.push_back(thisplane->unoriented());
	break;
      }
    }
  }
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "isEquiv_: common planes=";
//     std::cerr << derefprint(planes);
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
  if(npixplanes >= 3)
    return true;

  unsigned int nfaces = 0;
  for(const FacePlane *thisplane : fp0) {
    for(const FacePlane *otherplane : fp1) {
      if(thisplane->coincident(*otherplane)) {
	++nfaces;
	planes.push_back(thisplane->unoriented());
	break;
      }
    }
  }
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "isEquiv_: common planes+faces=";
//     std::cerr << derefprint(planes);
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
  if(nfaces >= 3)
    return true;

  unsigned int npixfaces = 0;
  for(const FacePixelPlane *thisplane : fpp0) {
    for(const FacePixelPlane *otherplane : fpp1) {
      if(thisplane->coincident(*otherplane)) {
	++npixfaces;
	planes.push_back(thisplane->unoriented());
	break;
      }
    }
  }

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "isEquiv_: common planes+faces+pixelfaces=";
//     std::cerr << derefprint(planes);
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
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
  // coincide at the intersection point of the planes.  If there is no
  // nondegenerate set, then there must be other, non-shared planes
  // that distinguish the points, and the points do not coincide.
  unsigned int nPlanes = planes.size();
  for(unsigned int i=0; i<nPlanes-2; i++) {
    // This is a horrible hack but it's the quickest way to see if the
    // code will work...  TODO: Find a way not to use casts here.
    // Maybe a triple-dispatch method that uses htet->areCollinear if
    // it gets two faces and a pixel plane, and Plane::nonDegenerate
    // otherwise.
    bool iIsPixelPlane = dynamic_cast<const HPixelPlane*>(planes[i]) != nullptr;
    for(unsigned int j=i+1; j<nPlanes-1; j++) {
      bool jIsPixelPlane =
	dynamic_cast<const HPixelPlane*>(planes[j]) != nullptr;
      for(unsigned int k=j+1; k<nPlanes; k++) {
	bool kIsPixelPlane =
	  dynamic_cast<const HPixelPlane*>(planes[k]) != nullptr;

	int npixelplanes = 0;
	if(iIsPixelPlane) ++npixelplanes;
	if(jIsPixelPlane) ++npixelplanes;
	if(kIsPixelPlane) ++npixelplanes;
	// Cases with 0 or 3 pixelplanes have been dealt with already.
	assert(npixelplanes == 1 || npixelplanes == 2);
	if(npixelplanes == 2) {
	  if(planes[i]->nonDegenerate(planes[j], planes[k]))
	    return true;
	}
	else {			// npixelplanes == 1
	  // Instead of calling Plane::nonDegenerate here, which might
	  // be susceptible to round off error, use the
	  // HomogeneityTet::collinearPlanes structure.
	  // collinearPlanes only includes situations with two faces,
	  // so it's not always usable.
	  if(!htet->areCollinear(planes[i], planes[j], planes[k]))
	    return true;
	}
      }
    }
  }
  return false;
} // end static isEquiv_

// template <class BASE>
// bool IntersectionPlanes<BASE>::isEquiv(const IntersectionPlanesBase *ppi)
//   const

// {
//   return isEquiv_(BASE::htet, pixelPlanes_, faces_, pixelFaces_,
// 		  ppi->pixelPlanes(), ppi->faces(), ppi->pixelFaces());
// }

// template <class BASE>
// bool IntersectionPlanes<BASE>::isEquiv(const RedundantIntersection *ri)
//   const
// {
//   return ri->referent()->isEquiv(this);
// }

template <class BASE>
void IntersectionPlanes<BASE>::addPlanesToEquivalence(
					      IsecEquivalenceClass *eqclass)
{
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneIntersectionNR::addPlanesToEquivalence: eq="
// 	    << *eqclass << std::endl;
// #endif // DEBUG
  for(const HPixelPlane *plane : pixelPlanes_)
    eqclass->addPixelPlane(plane, true);
  for(const FacePlane *face : faces_)
    eqclass->addFacePlane(face, true);
  for(const FacePixelPlane *fpp : pixelFaces_)
    eqclass->addFacePixelPlane(fpp, true);
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "PixelPlaneIntersectionNR::addPlanesToEquivalence: done"
// 	    << std::endl;
// #endif // DEBUG
}

template <class BASE>
bool IntersectionPlanes<BASE>::belongsInEqClass(
					const IsecEquivalenceClass *eqclass)
  const
{
  PixelPlaneSet indepPlanes;
  for(const HPixelPlane *pp : pixelPlanes_) {
    bool independent = true;
    for(const HPixelPlane *ip : indepPlanes) {
      if(pp->coincident(*ip)) {
	independent = false;
	break;
      }
    }
    if(independent)
      indepPlanes.insert(pp);
  }
  return isEquiv_(BASE::htet, indepPlanes, faces_, pixelFaces_,
		  eqclass->pixelPlanes, eqclass->facePlanes,
		  eqclass->pixelFaces);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class BASE>
std::string IntersectionPlanes<BASE>::printPlanes() const {
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

template <class BASE>
std::string IntersectionPlanes<BASE>::shortName() const {
  std::string str;
  for(const HPixelPlane *pp : pixelPlanes_)
    str += pp->shortName();
  for(const FacePixelPlane *fpp : pixelFaces_)
    str += fpp->shortName();
  for(const FacePlane *f : faces_)
    str += f->shortName();
  return str;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Methods for the mix-in classes.

#ifdef DEBUG
SingleVSBbase::SingleVSBbase() {
  // oofcerr << "SingleVSBbase::ctor: " << this << std::endl;
}
#endif // DEBUG

#define IMPOSSIBLE_ALPHA -1.234e5

template <class BASE>
SingleFaceMixIn<BASE>::SingleFaceMixIn(HomogeneityTet *htet)
  : BASE(htet),
    facePlane_(nullptr),
    polyFracCache(4, IMPOSSIBLE_ALPHA)
{
  // polyFracCache stores the values computed by getPolyFrac.  It's
  // initialized with IMPOSSIBLE_ALPHA so that we can tell which
  // values have been already computed.  polyFracCache has size 4
  // although we could get by with size 3 in some cases, but then we'd
  // have to know the polygon size at this point.
  
// #ifdef DEBUG
//   oofcerr << "SingleFaceMixIn::ctor: " << this << std::endl;
// #endif // DEBUG
}

template <class BASE>
double SingleFaceMixIn<BASE>::getPolyFrac(unsigned int edgeno,
					  const PixelPlaneFacet *facet)
  const
{
  // The return value of getPolyFrac has to be cached so that once the
  // relative positions of intersections on an edge has been found, it
  // won't change.  If the endpoint of an edge is merged with another
  // intersection, then the value returned by
  // HomogeneityTet::edgeCoord can change by a small amount, which
  // could be enough to re-order coincident intersections on the edge.
  
  // Although a SingleFaceMixin knows which face plane it was created
  // on (after setFacePlane has been called) it's possible that
  // getPolyFrac will be called with an edgeno that corresponds to a
  // different face, because two of its planes may be collinear with
  // another face.  Therefore we have to (a) not use facePlane_ here,
  // and (b) cache results for more than one edgeno.

  if(polyFracCache[edgeno] != IMPOSSIBLE_ALPHA)
    return polyFracCache[edgeno];
 
  const BarycentricCoord &bary = BASE::baryCoord(facet->htet);
#ifdef DEBUG
  if(BASE::verbose) {
    oofcerr << "SingleFaceMixIn::getPolyFrac: this=" << *this
	    << " edgeno=" << edgeno << std::endl;
    oofcerr << "SingleFaceMixIn::getPolyFrac: bary=" << bary << std::endl;
  }
#endif // DEBUG
  double pos = facet->htet->edgeCoord(bary, edgeno, facet);
  assert(pos != IMPOSSIBLE_ALPHA);
  polyFracCache[edgeno] = pos;
  return pos;
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
MultiFaceMixin<BASE>::MultiFaceMixin(HomogeneityTet *htet)
  : BASE(htet)
{}

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


  // TODO: This might be wrong if getFacePlane returns a collinear
  // face that's not in this PlaneIntersection.
  
  unsigned int nn = facet->polygonSize();
  FacePlaneSet nextfaces = facet->getFacePlanes((edge+1)%nn);
// #ifdef DEBUG
//   if(facet->verbose)
//     oofcerr << "MultiFaceMixin::getPolyFrac: nn=" << nn << " nextface="
// 	    << nextface << " " << *nextface << std::endl;
// #endif	// DEBUG
  for(const FacePlane *nextface : nextfaces)
    if(BASE::equivalence()->containsFacePlane(nextface))
      return 1.0;
#ifdef DEBUG
  // In debug mode, don't just assume that one of the faces of the
  // previous edge is part of this intersection.
  FacePlaneSet prevfaces = facet->getFacePlanes((edge+nn-1)%nn);
  for(const FacePlane *prevface : prevfaces)
    if(BASE::equivalence()->containsFacePlane(prevface))
      return 0.0;
  if(facet->verbose) {
    oofcerr << "MultiFaceMixin::getPolyFrac: " << this << " " << *this
	    << std::endl;
    oofcerr << "MultiFaceMixin::getPolyFrac: nextfaces=";
    for(const FacePlane *nextface : nextfaces)
      oofcerr << " " << *nextface;
    oofcerr << std::endl;
    oofcerr << "MultiFaceMixin::getPolyFrac: prevfaces=";
    for(const FacePlane *prevface : prevfaces)
      oofcerr << " " << *prevface;
    oofcerr << std::endl;
  }
  throw ErrProgrammingError("MultiFaceMixin::getPolyFrac failed!",
			    __FILE__, __LINE__);
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

template <class BASE>
SingleVSBmixIn<BASE>::SingleVSBmixIn(HomogeneityTet *htet)
  : BASE(htet)
{
  // oofcerr << "SingleVSBmixIn::ctor: " << this << std::endl;
}

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
					     PixelBdyLoopSegment &seg1,
					     ICoord2D &corner)
  const
{
  return fi->reverseOrdering(static_cast<const SingleVSBbase*>(this),
			     seg0, seg1, corner);
}

// Utility used by SingleVSBmixIn::reverseOrdering.  Given a
// horizontal and a vertical PixelBdyLoopSegment, see if they meet in
// a T intersection (which might actually be an L).  The return value
// is either FIRST (meaning that the horizontal segment leads to the
// vertical one at the intersection), SECOND (meaning that the
// vertical one leads to the horizontal one), or NONCONTIGUOUS
// (meaning that there's no intersection, or that there's no path
// through it along the directed segments).

static ISEC_ORDER checkT(const PixelBdyLoopSegment &horizSeg,
			 const PixelBdyLoopSegment &vertSeg,
			 PixelBdyLoopSegment &seg0,
			 PixelBdyLoopSegment &seg1,
			 ICoord2D &corner
#ifdef DEBUG
			 , bool verbose
#endif // DEBUG
			 )
{
  ICoord2D horiz0 = horizSeg.firstPt();
  ICoord2D horiz1 = horizSeg.secondPt();
  ICoord2D vert0 = vertSeg.firstPt();
  ICoord2D vert1 = vertSeg.secondPt();

  // First check that the two segments don't start or end at the same
  // point.  If they do, then they don't form a corner even if they
  // seem to intersect.  Checking this here means that we don't have
  // to consider corner cases (ha) below.
  if(horiz0 == vert0 || horiz1 == vert1)
    return NONCONTIGUOUS;

  // If there is an intersection, it's here:
  corner[0] = vert0[0];	      // x component of the vertical segment
  corner[1] = horiz0[1];      // y component of the horizontal segment
  int x = corner[0];
  int y = corner[1];

// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "checkT: horiz0="<< horiz0 << " horiz1=" << horiz1
// 	    << " vert0=" << vert0 << " vert1=" << vert1
// 	    << " corner=" << corner
// 	    << std::endl;
// #endif // DEBUG
  
  bool up = vert1[1] > vert0[1]; // Does the vertical segment go up?

  if(horiz0[0] == x) {	// horizSeg starts at x position of vertSeg
    // All comparisons here can use >= or <= only because we've
    // checked for the corner case above.  Otherwise these comparisons
    // are uglier.
    if((up && y >= vert0[1] && y <= vert1[1]) ||
       (!up && y <= vert0[1] && y >= vert1[1]))
      {
	seg0 = vertSeg;
	seg1 = horizSeg;
	return SECOND; 
      }
    return NONCONTIGUOUS;
  } // end if horizSeg starts at x position of vertSeg

  if(horiz1[0] == x) {	// horizSeg ends at x position of vertSeg
    if((up && y >= vert0[1] && y <= vert1[1]) ||
       (!up && y <= vert0[1] && y >= vert1[1]))
      {
	// Horizontal segment ends on the vertical one.
	seg0 = horizSeg;
	seg1 = vertSeg;
	return FIRST;
      }
    return NONCONTIGUOUS;
  }

  bool right = horiz1[0] > horiz0[0]; // Does the horizontal segment go right?
  
  if(vert0[1] == y) {		// vertSeg starts at y position of horizSeg
    if((right && x >= horiz0[0] && x <= horiz1[0]) ||
       (!right && x <= horiz0[0] && x >= horiz1[0]))
      {
	seg0 = horizSeg;
	seg1 = vertSeg;
	return FIRST;
      }
    return NONCONTIGUOUS;
  }

  if(vert1[1] == y) {		// vertSeg ends at y position of horizSeg;
    if((right && x >= horiz0[0] && x <= horiz1[0]) ||
       (!right && x <= horiz0[0] && x >= horiz1[0]))
      {
	seg0 = vertSeg;
	seg1 = horizSeg;
	return SECOND;
      }
  }
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "checkT: No intersection!" << std::endl;
// #endif // DEBUG
  return NONCONTIGUOUS;
}

template <class BASE>
ISEC_ORDER SingleVSBmixIn<BASE>::reverseOrdering(const SingleVSBbase *other,
						 PixelBdyLoopSegment &seg0,
						 PixelBdyLoopSegment &seg1,
						 ICoord2D &corner)
  const
{
// #ifdef DEBUG
//   if(BASE::verbose) {
//       oofcerr << "SingleVSBmixIn::reverseOrdering:  this=" << *this
// 	      << std::endl;
//       oofcerr << "SingleVSBmixIn::reverseOrdering: other="
// 	      << *dynamic_cast<const PlaneIntersection*>(other) << std::endl;
//     }
// #endif // DEBUG
  if(vsbSegment.loop() == other->getLoopSeg().loop()) {
// #ifdef DEBUG
//     if(BASE::verbose) {
//       oofcerr << "SingleVSBmixIn::reverseOrdering: on same loop" << std::endl;
//       oofcerr << "SingleVSBmixIn::reverseOrdering: vsbSegment=" << vsbSegment
// 	      << std::endl;
//       oofcerr << "SingleVSBmixIn::reverseOrdering: other->getLoopSeg="
// 	      << other->getLoopSeg() << std::endl;
//       }
// #endif // DEBUG
    if(other->getLoopSeg().firstPt() == vsbSegment.secondPt()) {
      seg0 = vsbSegment;
      seg1 = other->getLoopSeg();
      corner = vsbSegment.secondPt();
      return SECOND;
    }
    if(other->getLoopSeg().secondPt() == vsbSegment.firstPt()) {
      seg1 = vsbSegment;
      seg0 = other->getLoopSeg();
      corner = vsbSegment.firstPt();
      return FIRST;
    }
    return NONCONTIGUOUS;
  }
// #ifdef DEBUG
//   if(BASE::verbose)
//       oofcerr << "SingleVSBmixIn::reverseOrdering: on different loops"
// 	      << std::endl;
// #endif // DEBUG
  // The intersections are on segments that are on different VSB
  // loops.  This can only happen if one of them is a VSB facet loop
  // and the other is a cross section.  In either case, it's possible
  // that the segments either join end to end or form a T, both of
  // which define corners.
  const PixelBdyLoopSegment &segA = vsbSegment;
  const PixelBdyLoopSegment &segB = other->getLoopSeg();
  bool segAhoriz = segA.horizontal();
  bool segBhoriz = segB.horizontal();
  if(segAhoriz && !segBhoriz) {
    ISEC_ORDER order = checkT(segA, segB, seg0, seg1, corner
#ifdef DEBUG
		  , BASE::verbose
#endif // DEBUG
		  );
    // Return the reverse order.
    if(order == FIRST) return SECOND;
    if(order == SECOND) return FIRST;
    return order;
  }
  if(segBhoriz && !segAhoriz) {
    ISEC_ORDER order = checkT(segB, segA, seg0, seg1, corner
#ifdef DEBUG
			      , BASE::verbose
#endif // DEBUG
			      );
    // segments were passed in reverse order to checkT, but we want to
    // return the reverse.
    return order;
  }

  // The segments are either both horizontal or both vertical.  The
  // position of the intersection is ambiguous.  If this situation
  // occurs, it needs to be handled in some other fashion entirely.
  
  // ----->----------
  //      -----<-------------------------
  // Here ^ or here ^ ?
  throw ErrProgrammingError("Ambiguous intersection!", __FILE__, __LINE__);
}

template <class BASE>
ISEC_ORDER SingleVSBmixIn<BASE>::reverseOrdering(const MultiVSBbase *other,
						 PixelBdyLoopSegment &seg0,
						 PixelBdyLoopSegment &seg1,
						 ICoord2D &corner)
  const
{
  const PBLSegmentMap &osegs = other->getLoopSegs();
  for(PBLSegmentMap::const_iterator oi=osegs.begin(); oi!=osegs.end(); ++oi) {
    const PixelBdyLoopSegment &oseg = (*oi).first;
      if(oseg.firstPt() == vsbSegment.secondPt()) {
	seg0 = vsbSegment;
	seg1 = oseg;
	corner = vsbSegment.secondPt();
	return SECOND;
      }
      if(oseg.secondPt() == vsbSegment.firstPt()) {
	seg1 = vsbSegment;
	seg0 = oseg;
	corner = vsbSegment.firstPt();
	return FIRST;
      }
  }
  return NONCONTIGUOUS;
}

//-------

// MultiVSBmixIn::categorizeCorner categorizes the VSB corner that's
// *at* an intersection, in contrast to classifyVSBcorner, which
// categorizes the corner *between* two intersections.

template <class BASE>
MultiVSBmixIn<BASE>::MultiVSBmixIn(HomogeneityTet *htet)
  : BASE(htet)
{}

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
					    PixelBdyLoopSegment &seg1,
					    ICoord2D &corner)
  const
{
  return fi->reverseOrdering(static_cast<const MultiVSBbase*>(this),
			     seg0, seg1, corner);
}

template <class BASE>
ISEC_ORDER MultiVSBmixIn<BASE>::reverseOrdering(const SingleVSBbase *other,
						PixelBdyLoopSegment &seg0,
						PixelBdyLoopSegment &seg1,
						ICoord2D &corner)
  const
{
  ISEC_ORDER reverse = other->reverseOrdering(this, seg0, seg1, corner);
  if(reverse == FIRST) {
    return SECOND;
  }
  if(reverse == SECOND)
    return FIRST;
  return reverse;
}

template <class BASE>
ISEC_ORDER MultiVSBmixIn<BASE>::reverseOrdering(const MultiVSBbase *other,
						PixelBdyLoopSegment &seg0,
						PixelBdyLoopSegment &seg1,
						ICoord2D &corner)
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
	    corner = seg.secondPt();
	    return SECOND;
	  }
	  if(oseg.secondPt() == seg.firstPt()) {
	    seg1 = seg;
	    seg0 = oseg;
	    corner = seg.firstPt();
	    return FIRST;
	  }
	}
    }
  return NONCONTIGUOUS;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility function used when merging intersections.  If the two given
// intersections are merged, what is the crossing type of the result?

static int combinedCrossing(const PixelPlaneIntersectionNR *fi0,
			    const PixelPlaneIntersectionNR *fi1)
{
  return fi0->crossingCount() + fi1->crossingCount();

  // // Hack to mimic old (incorrect!) behavior
  // if(fi0->crossingCount() > 0 && fi1->crossingCount() > 0)
  //   return 1;
  // if(fi0->crossingCount() < 0 && fi1->crossingCount() < 0)
  //   return -1;
  // if(fi0->crossingCount() == 0)
  //   return fi1->crossingCount();
  // if(fi1->crossingCount() == 0)
  //   return fi0->crossingCount();
  // return 0;

  // if(fi0->crossingType() == fi1->crossingType())
  //   return fi0->crossingType();
  // if(fi0->crossingType() == NONCROSSING)
  //   return fi1->crossingType();
  // if(fi1->crossingType() == NONCROSSING)
  //   return fi0->crossingType();
  // return NONCROSSING;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SimpleIntersection::SimpleIntersection(HomogeneityTet *htet,
				       const HPixelPlane *pp0,
				       const HPixelPlane *pp1,
				       const PixelBdyLoopSegment &pblseg,
				       double alpha,
				       unsigned int faceIndex,
				       CrossingType ct)
  : SingleVSBmixIn<SingleFaceMixIn<PixelPlaneIntersectionNR>>(htet)
{
  assert(ct != NONCROSSING);
  pp0->addToIntersection(this);
  pp1->addToIntersection(this);

  // The given faceIndex is the face that intersects the
  // PixelBdyLoopSegment.  It's not the face, if any, that contains
  // the pixel plane of the facet.  faceIndex can be NONE if the
  // segment lies in the plane of a face, in which case the calling
  // routine will set the location and add a transverse face.
  if(faceIndex != NONE) {
    const FacePlane *fp = htet->getTetFacePlane(faceIndex);
    fp->addToIntersection(this);
    setFacePlane(fp);
    computeLocation();
    // includeCollinearPlanes(htet);
  }
  else {
    setFacePlane(nullptr);
  }
  setLoopSeg(pblseg);
  setLoopFrac(alpha);
  assert(ct == ENTRY || ct == EXIT);
  setCrossingType(ct);
// #ifdef DEBUG
//   oofcerr << "SimpleIntersection::ctor: done" << std::endl;
// #endif // DEBUG
}

SimpleIntersection *SimpleIntersection::clone(HomogeneityTet *htet) const {
  SimpleIntersection *si = new SimpleIntersection(*this);
  si->setID(htet);
  return si;
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
					HomogeneityTet *htet,
					PixelPlaneIntersection *fi,
					const PixelPlaneFacet *facet)
{
  if(fi)	    // TODO: Why check for null fi?  Is that possible?
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
						HomogeneityTet *htet,
						SimpleIntersection *fi,
						const PixelPlaneFacet *facet)
{
#ifdef DEBUG
  if(htet->verbosePlane())
    oofcerr << "SimpleIntersection::mergeWith: this="
	    << *this << " fi=" << *fi << std::endl;
#endif // DEBUG
  PixelPlaneIntersectionNR *merged = nullptr;
  // Two antiparallel but otherwise equivalent VSB segments that
  // intersect a face should form a new SimpleIntersection there.  But
  // if the points originate on different faces or segments, they
  // should merge to form a multi-something intersection, below.
  if(isEquivalent(fi)) {
    if(onOnePolySegment(fi, facet) && onSameLoopSegment(fi)) {
      merged = clone(htet);
      merged->setCrossingCount(combinedCrossing(this, fi));
#ifdef DEBUG
    if(htet->verbosePlane()) {
      oofcerr << "SimpleIntersection::mergeWith: antiparallel, merged="
	      << merged << " " << *merged << std::endl;
      }
#endif // DEBUG
    // Don't call mergeEquiv -- clones don't need it
      return merged;
    }
  } // end if points are equivalent
#ifdef DEBUG
  if(facet->onOppositeEdges(this, fi)) {
    if(htet->verbosePlane())
      oofcerr << "SimpleIntersection::mergeWith: on opposite edges!"
	      << std::endl;
    throw ErrProgrammingError("SimpleIntersection::mergeWith failed!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  if(onSameLoopSegment(fi)) {
    merged = new MultiFaceIntersection(htet, this, fi);
  }
  else if(onOnePolySegment(fi, facet)) {
    merged = new MultiVSBIntersection(htet, facet, this, fi);
// #ifdef DEBUG
//     if(htet->verbosePlane())
//       oofcerr << "SimpleIntersection::mergeWith: result=" << *res << std::endl;
// #endif // DEBUG
  }
  else {
    merged = new MultiCornerIntersection(htet, this, fi);
  }
  if(merged != nullptr)
    htet->mergeEquiv(this, fi, merged);
  return merged;
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
						HomogeneityTet *htet,
						MultiFaceIntersection *fi,
						const PixelPlaneFacet *facet)
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  PixelPlaneIntersectionNR *merged;
  if(onSameLoopSegment(fi))
    merged = new MultiFaceIntersection(htet, this, fi);
  else
    merged = new MultiCornerIntersection(htet, this, fi);
  htet->mergeEquiv(this, fi, merged);
  return merged;
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
						HomogeneityTet *htet,
						MultiVSBIntersection *fi,
						const PixelPlaneFacet *facet)
{
  PixelPlaneIntersectionNR *merged;
  if(onOnePolySegment(fi, facet))
    merged = new MultiVSBIntersection(htet, facet, this, fi);
  else
    merged = new MultiCornerIntersection(htet, this, fi);
  htet->mergeEquiv(this, fi, merged);
  return merged;
}

PixelPlaneIntersectionNR *SimpleIntersection::mergeWith(
					HomogeneityTet *htet,
					MultiCornerIntersection *fi,
					const PixelPlaneFacet *facet)
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  PixelPlaneIntersectionNR *merged =
    new MultiCornerIntersection(htet, this, fi);
  htet->mergeEquiv(this, fi, merged);
  return merged;
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
//     oofcerr << "SimpleIntersection::isMisordered: this=" << *this <<  std::endl
// 	    << "                                :   fi=" << *fi << std::endl;
//   }
// #endif // DEBUG
  bool sameLoopSeg = onSameLoopSegment(fi);
  unsigned int nSharedPolySegs = nSharedPolySegments(fi, facet);
#ifdef DEBUG
  if(verbose) {
    oofcerr << "SimpleIntersection::isMisordered: sameLoopSeg=" << sameLoopSeg
	    << " nSharedPolySegs=" << nSharedPolySegs << std::endl;
  }
#endif // DEBUG
  assert(!(sameLoopSeg && nSharedPolySegs==1));
  if(!sameLoopSeg && nSharedPolySegs == 1) {
    return facet->vsbCornerCoincidence(this, fi);
  }
  if(sameLoopSeg && nSharedPolySegs == 0) {
    return facet->polyCornerCoincidence(this, fi);
  }
  if(!sameLoopSeg && nSharedPolySegs == 0) {
    return facet->polyVSBCornerCoincidence(this, fi);
  }
  if(nSharedPolySegs == 2)
    return true;		// points must be coincident
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
     << ", crossing=" << crossingCount();
  const FacePlane *fp = getFacePlane();
  if(fp)
    os << ", faceplane=" << *getFacePlane();
  else
    os << ", faceplane=0x0";
  os << ", eq=" << eqPrint(equivalence_) << ")";
}

PixelPlaneIntersectionNR *newIntersection(HomogeneityTet *htet,
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

MultiFaceIntersection::MultiFaceIntersection(HomogeneityTet *htet,
					     const HPixelPlane *pp0,
					     const HPixelPlane *pp1,
					     const PixelBdyLoopSegment &pblseg,
					     double alpha,
					     unsigned int faceIndex,
					     CrossingType ct)
  : SingleVSBmixIn<MultiFaceMixin<PixelPlaneIntersectionNR>>(htet)
{
  pp0->addToIntersection(this);
  pp1->addToIntersection(this);
  if(faceIndex != NONE) {
    const FacePlane *fp = htet->getTetFacePlane(faceIndex);
    fp->addToIntersection(this);
    computeLocation();
    // includeCollinearPlanes(htet);
  }
  setLoopSeg(pblseg);
  setLoopFrac(alpha);
  setCrossingType(ct);
}

MultiFaceIntersection::MultiFaceIntersection(HomogeneityTet *htet,
					     const SimpleIntersection *fi0,
					     const SimpleIntersection *fi1)
  : SingleVSBmixIn<MultiFaceMixin<PixelPlaneIntersectionNR>>(htet)
{
  assert(fi0->onSameLoopSegment(fi1));
  assert(fi0->getFacePlane() != fi1->getFacePlane());
#ifdef DEBUG
  verbose = fi0->verbose || fi1->verbose;
#endif // DEBUG
  setCrossingCount(combinedCrossing(fi0, fi1));
  setLoopSeg(fi0->getLoopSeg());
  setLoopFrac(fi0->getLoopFrac());
  copyPlanes(fi0, fi1);
  // This may not be the best way to calculate the position, but the
  // position shouldn't be used for topological calculations anyway.
  setLocation(0.5*(fi0->location3D() + fi1->location3D()));
  // includeCollinearPlanes(htet);	// TODO: Is this necessary?
}

MultiFaceIntersection::MultiFaceIntersection(HomogeneityTet *htet,
					     const SimpleIntersection *si,
					     const MultiFaceIntersection *mfi)
  : SingleVSBmixIn<MultiFaceMixin<PixelPlaneIntersectionNR>>(htet)
{
  assert(si->onSameLoopSegment(mfi));
#ifdef DEBUG
  verbose = si->verbose || mfi->verbose;
#endif // DEBUG
  setCrossingCount(combinedCrossing(si, mfi));
  setLoopSeg(si->getLoopSeg());
  setLoopFrac(si->getLoopFrac());
  copyPlanes(si, mfi);
  // This may not be the best way to calculate the position, but the
  // position shouldn't be used for topological calculations anyway.
  setLocation(0.5*(si->location3D() + mfi->location3D()));
  // includeCollinearPlanes(htet);	// TODO: Is this necessary?
}

MultiFaceIntersection::MultiFaceIntersection(HomogeneityTet *htet)
  : SingleVSBmixIn<MultiFaceMixin<PixelPlaneIntersectionNR>>(htet)
{}

MultiFaceIntersection *MultiFaceIntersection::clone(HomogeneityTet *htet) const
{
  MultiFaceIntersection *mfi = new MultiFaceIntersection(*this);
  mfi->setID(htet);
  return mfi;
}

// A MultiFaceIntersection is interior if the interior of the polygon
// at the corner is on the interior (ie left) side of the VSB segment.

Interiority MultiFaceIntersection::interiority(const PixelPlaneFacet *facet)
  const
{
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "MultiFaceIntersection::interiority: this=" << *this
// 	    << std::endl;
//   }
//   OOFcerrIndent indent(2);
// #endif // DEBUG
  assert(nPolySegments() == 2);
  ICoord2D vsb0 = segEnd(0);
  ICoord2D vsb1 = segEnd(1);
  unsigned int pseg0, pseg1;
  getPolyEdges(facet, pseg0, pseg1);
  Coord2D pprev = facet->polygonCorner(pseg0);
  Coord2D phere = facet->polygonCorner(pseg1);
  Coord2D pnext = facet->polygonCorner((pseg1+1) % facet->polygonSize());
  double cross0 = (pprev - phere) % (vsb1 - vsb0);
  double cross1 = (pnext - phere) % (vsb1 - vsb0);
// #ifdef DEBUG
//     if(verbose) {
//       OOFcerrIndent indent(2);
//       oofcerr << "MultiFaceIntersection::interiority: vsb0=" << vsb0
// 	      << " vsb1=" << vsb1 << std::endl;
//       oofcerr << "MultiFaceIntersection::interiority: pprev=" << pprev
// 	      << " phere=" << phere << " pnext=" << pnext << std::endl;
//       oofcerr << "MultiFaceIntersection::interiority: cross0=" << cross0
// 	      << " cross1=" << cross1 << std::endl;
//     }
// #endif // DEBUG
  if(cross0 < 0 && cross1 < 0)
    return INTERIOR;
  if(cross0 > 0 && cross1 > 0)
    return EXTERIOR;
  return MIXED;
}

// Same thing, but just for a single segment.
Interiority MultiFaceIntersection::interiority(unsigned int which,
					       const PixelPlaneFacet *facet)
  const
{
  assert(nPolySegments() == 2);
  assert(which == 0 || which == 1);
  ICoord2D vsb0 = segEnd(0);
  ICoord2D vsb1 = segEnd(1);
  unsigned int pseg0, pseg1;
  getPolyEdges(facet, pseg0, pseg1);
  Coord2D phere = facet->polygonCorner(pseg1);
  double cross;
  if(which == 0) {
    Coord2D pprev = facet->polygonCorner(pseg0);
    cross = (pprev - phere) % (vsb1 - vsb0);
  }
  else {
    Coord2D pnext = facet->polygonCorner((pseg1+1) % facet->polygonSize());
    cross = (pnext - phere) % (vsb1 - vsb0);
  }
  if(cross < 0) return INTERIOR;
  if(cross > 0) return EXTERIOR;
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
					   HomogeneityTet *htet,
					   PixelPlaneIntersection *fi,
					   const PixelPlaneFacet *facet)
{
  if(fi)
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
						   HomogeneityTet *htet,
						   SimpleIntersection *fi,
						   const PixelPlaneFacet *facet)
{
  // SimpleIntersection::mergeWith(MultiFaceIntersection) is equivalent
  return fi->mergeWith(htet, this, facet); 
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
					   HomogeneityTet *htet,
					   MultiFaceIntersection *fi,
					   const PixelPlaneFacet *facet)
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  PixelPlaneIntersectionNR *merged =
    new MultiCornerIntersection(htet, this, fi);
  htet->mergeEquiv(this, fi, merged);
  return merged;
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
					   HomogeneityTet *htet,
					   MultiVSBIntersection *fi,
					   const PixelPlaneFacet *facet)
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  PixelPlaneIntersectionNR *merged =
    new MultiCornerIntersection(htet, fi, this);
  htet->mergeEquiv(this, fi, merged);
  return merged;
}

PixelPlaneIntersectionNR *MultiFaceIntersection::mergeWith(
					   HomogeneityTet *htet,
					   MultiCornerIntersection *fi,
					   const PixelPlaneFacet *facet)
{
  if(fi->sharedPolySegment(this, facet) == NONE)
    return nullptr;
  PixelPlaneIntersectionNR *merged= new MultiCornerIntersection(htet, fi, this);
  htet->mergeEquiv(this, fi, merged);
  return merged;
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
     << ", crossing=" << crossingCount()
     << ", eq=" << eqPrint(equivalence_) << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MultiVSBIntersection::MultiVSBIntersection(HomogeneityTet *htet,
					   const PixelPlaneFacet *facet,
					   const SimpleIntersection *fi0,
					   const SimpleIntersection *fi1)
  : SingleFaceMixIn<MultiVSBmixIn<PixelPlaneIntersectionNR>>(htet)
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
  setCrossingCount(combinedCrossing(fi0, fi1));
  // setPolyFrac(fi0->getPolyFrac(NONE, facet));
  setFacePlane(fi0->getFacePlane() != nullptr ?
	       fi0->getFacePlane() : fi1->getFacePlane());
  // TODO: Enforce that each vsb segment fraction is either 0 or 1
  vsbSegments[fi0->getLoopSeg()] = fi0->getLoopFrac();
  vsbSegments[fi1->getLoopSeg()] = fi1->getLoopFrac();
  computeLocation();
  // includeCollinearPlanes(htet);
}

MultiVSBIntersection::MultiVSBIntersection(HomogeneityTet *htet,
#ifdef DEBUG
					   const PixelPlaneFacet *facet,
#endif // DEBUG
					   const SimpleIntersection *si,
					   const MultiVSBIntersection *mvi)
  : SingleFaceMixIn<MultiVSBmixIn<PixelPlaneIntersectionNR>>(htet)
{
  assert(si->onOnePolySegment(mvi, facet));
#ifdef DEBUG
  verbose = si->verbose || mvi->verbose;
#endif // DEBUG
  copyPlanes(si, mvi);
  setCrossingCount(combinedCrossing(si, mvi));
  // setPolyFrac(si->getPolyFrac(NONE, facet));
  setFacePlane(si->getFacePlane() != nullptr ?
	       si->getFacePlane() : mvi->getFacePlane());
  vsbSegments[si->getLoopSeg()] = si->getLoopFrac();
  vsbSegments.insert(mvi->getLoopSegs().begin(), mvi->getLoopSegs().end());
  computeLocation();
  // includeCollinearPlanes(htet);
}

MultiVSBIntersection *MultiVSBIntersection::clone(HomogeneityTet *htet) const {
  MultiVSBIntersection *mvi = new MultiVSBIntersection(*this);
  mvi->setID(htet);
  return mvi;
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  HomogeneityTet *htet,
					  PixelPlaneIntersection *fi,
					  const PixelPlaneFacet *facet)
{
  if(fi)
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
						  HomogeneityTet *htet,
						  SimpleIntersection *fi,
						  const PixelPlaneFacet *facet)
{
  // SimpleIntersection::mergeWith(MultiVSBIntersection) is equivalent
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  HomogeneityTet *htet,
					  MultiFaceIntersection *fi,
					  const PixelPlaneFacet *facet)
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  HomogeneityTet *htet,
					  MultiVSBIntersection *fi,
					  const PixelPlaneFacet *facet)
{
  // Both intersections are on a voxel corner, so they had better be
  // on the same corner. 
  if(!samePixelPlanes(fi))
    return nullptr;
  PixelPlaneIntersectionNR *merged;
  if(getFacePlane() == fi->getFacePlane()) {
    // If they share the same face, too, then they're really the same
    // corner, and the mergee is the same as the two mergers.
    merged = clone(htet);
  }
  else {
    merged = new MultiCornerIntersection(htet, this, fi);
  }
  htet->mergeEquiv(this, fi, merged);
  return merged;
}

PixelPlaneIntersectionNR *MultiVSBIntersection::mergeWith(
					  HomogeneityTet *htet,
					  MultiCornerIntersection *fi,
					  const PixelPlaneFacet *facet)
{
  // Both intersections are on a voxel corner, so they had better be
  // on the same corner.  They had also better share a tet face.
  if(!samePixelPlanes(fi) || !onSameFacePlane(fi, facet->getBaseFacePlane()))
    return nullptr;
  PixelPlaneIntersectionNR *merged =
    new MultiCornerIntersection(htet, this, fi);
  htet->mergeEquiv(this, fi, merged);
  return merged;
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
     << ", crossing=" << crossingCount()
     << ", eq=" << eqPrint(equivalence_) << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

MultiCornerIntersection::MultiCornerIntersection(
					 HomogeneityTet *htet,
					 const PixelPlaneIntersectionNR *fi0,
					 const PixelPlaneIntersectionNR *fi1)
  : MultiFaceMixin<MultiVSBmixIn<PixelPlaneIntersectionNR>>(htet)
{
  setCrossingCount(combinedCrossing(fi0, fi1));
#ifdef DEBUG
  verbose = fi0->verbose || fi1->verbose;
#endif // DEBUG
  copyPlanes(fi0, fi1);
  computeLocation();
  // TODO: In debug mode, check that the faces actually pass through
  // the intersection point as determined by the pixel planes?
#ifdef DEBUG
  if(htet->verbosePlane()) {
    oofcerr << "MultiCornerIntersection::ctor: built " << *this << std::endl;
    OOFcerrIndent indent(2);
    oofcerr << "MultiCornerIntersection::ctor: from fi0=" << *fi0 << std::endl;
    oofcerr << "MultiCornerIntersection::ctor:  and fi1=" << *fi1 << std::endl;
    oofcerr << "MultiCornerIntersection::ctor: crossing_=" << crossing_
	    << std::endl;
  }
#endif // DEBUG
  // includeCollinearPlanes(htet);
}

MultiCornerIntersection *MultiCornerIntersection::clone(HomogeneityTet *htet)
  const
{
  MultiCornerIntersection *mci = new MultiCornerIntersection(*this);
  mci->setID(htet);
  return mci;
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     HomogeneityTet *htet,
					     PixelPlaneIntersection *fi,
					     const PixelPlaneFacet *facet)
{
  if(fi)
    return fi->referent()->mergeWith(htet, this, facet); // double dispatch
  return nullptr;
}


PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     HomogeneityTet *htet,
					     SimpleIntersection *fi,
					     const PixelPlaneFacet *facet)
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     HomogeneityTet *htet,
					     MultiFaceIntersection *fi,
					     const PixelPlaneFacet *facet)
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     HomogeneityTet *htet,
					     MultiVSBIntersection *fi,
					     const PixelPlaneFacet *facet)
{
  return fi->mergeWith(htet, this, facet);
}

PixelPlaneIntersectionNR *MultiCornerIntersection::mergeWith(
					     HomogeneityTet *htet,
					     MultiCornerIntersection *fi,
					     const PixelPlaneFacet *facet)
{
  // This really can't happen unless the intersections are already at
  // the same point.  The point is determined by the voxel corner, so
  // there's no round-off error to worry about.
  if(location3D() != fi->location3D())
    return nullptr;
  PixelPlaneIntersectionNR *merged =
    new MultiCornerIntersection(htet, this, fi);
  htet->mergeEquiv(this, fi, merged);
  return merged;
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
     << ", crossing=" << crossingCount()
     << ", eq=" << eqPrint(equivalence_) << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RedundantIntersection::RedundantIntersection(PixelPlaneIntersection *ppi,
					     PixelPlaneFacet *facet)
  : PixelPlaneIntersection(facet->htet),
    referent_(ppi->referent()),
    facet_(facet)
{
  facet_->newRedundantIntersection(this);
}

RedundantIntersection::~RedundantIntersection() {
  facet_->removeRedundantIntersection(this);
}

RedundantIntersection *RedundantIntersection::clone(HomogeneityTet *htet) const
{
  RedundantIntersection *ri = new RedundantIntersection(referent_, facet_);
  // The RedundantIntersection constructor sets the id -- no need to
  // call setID here.
  return ri;
}

void RedundantIntersection::print(std::ostream &os) const {
  os << "RedundantIntersection(" << *referent_ << ")";
}

std::string RedundantIntersection::shortName() const {
  return "R" + referent_->shortName();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

TetEdgeIntersection::TetEdgeIntersection(HomogeneityTet *htet,
					 const FacePlane *f0,
					 const FacePlane *f1,
					 const HPixelPlane *pp)
  : TetIntersection(htet)
{
// #ifdef DEBUG
//   if(htet->verbosePlane()) {
//     oofcerr << "TetEdgeIntersection::ctor: f0=" << *f0 << " f1=" << *f1
// 	    << " pp=" << *pp << std::endl;
//   }
// #endif // DEBUG
  f0->addToIntersection(this);
  f1->addToIntersection(this);
  pp->addToIntersection(this);
  // faces_.insert(f0);
  // faces_.insert(f1);
  // pixelPlanes_.insert(pp);
  loc_ = triplePlaneIntersection(f0, f1, pp);
// #ifdef DEBUG
//   if(htet->verbosePlane()) {
//     oofcerr << "TetEdgeIntersection::ctor: " << *this << std::endl;
//   }
// #endif // DEBUG
  setCrossingCount(0);
// #ifdef DEBUG
//   if(htet->verbosePlane())
//     oofcerr << "TetEdgeIntersection::ctor: before includeCollinearPlanes, this="
// 	    << *this << std::endl;
// #endif // DEBUG

  // includeCollinearPlanes(htet);

  // #ifdef DEBUG
//   if(htet->verbosePlane())
//     oofcerr << "TetEdgeIntersection::ctor: after includeCollinearPlanes, this="
// 	    << *this << std::endl;
// #endif // DEBUG
}

TetEdgeIntersection *TetEdgeIntersection::clone(HomogeneityTet *htet) const {
  TetEdgeIntersection *tei = new TetEdgeIntersection(*this);
  tei->setID(htet);
  return tei;
}

void TetEdgeIntersection::print(std::ostream &os) const {
  os << "TetEdgeIntersection(" << printPlanes() << ", " << location3D()
     << ", crossing=" << crossingCount()
     << ", eq=" << eqPrint(equivalence_) << ")";
}

std::string TetEdgeIntersection::shortName() const {
  return "TE" + PixelPlaneIntersectionNR::shortName();
}

TetNodeIntersection::TetNodeIntersection(HomogeneityTet *htet,
					 const HPixelPlane *pp,
					 unsigned int node)
  : TetIntersection(htet)
{
  // TODO: One of the faces will either not create a polygon edge or
  // will be redundant with another plane.  If it's redundant, that's
  // ok -- planes are stored in sets so redundancies are eliminated.
  // Do we have to worry about faces that don't create polygon edges?
  for(unsigned int i=0; i<3; i++) {
    unsigned int f = CSkeletonElement::nodeFaces[node][i];
    const FacePlane *fp = htet->getTetFacePlane(f);
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
  // includeCollinearPlanes(htet);
}

TetNodeIntersection *TetNodeIntersection::clone(HomogeneityTet *htet) const {
  TetNodeIntersection *tni = new TetNodeIntersection(*this);
  tni->setID(htet);
  return tni;
}

void TetNodeIntersection::print(std::ostream &os) const {
  os << "TetNodeIntersection(" << printPlanes() << ", " << location3D()
     << ", crossing=" << crossingCount()
     << ", eq=" << eqPrint(equivalence_) << ")";
}

std::string TetNodeIntersection::shortName() const {
  return "TN" + PixelPlaneIntersectionNR::shortName();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

TriplePixelPlaneIntersection::TriplePixelPlaneIntersection(
						   HomogeneityTet *htet,
						   const HPixelPlane *pp0,
						   const HPixelPlane *pp1,
						   const HPixelPlane *pp2)
  : MultiVSBmixIn<PixelPlaneIntersectionNR>(htet)
{
  pp0->addToIntersection(this);
  pp1->addToIntersection(this);
  pp2->addToIntersection(this);
  setCrossingCount(0);
  computeLocation();
  // includeCollinearPlanes(htet);
}

TriplePixelPlaneIntersection *TriplePixelPlaneIntersection::clone(
						  HomogeneityTet *htet)
  const
{
  TriplePixelPlaneIntersection *tpi = new TriplePixelPlaneIntersection(*this);
  tpi->setID(htet);
  return tpi;
}

void TriplePixelPlaneIntersection::print(std::ostream &os) const {
  os << "TriplePixelPlaneIntersection(" << printPlanes() << ", "
     << location3D() << ", crossing=" << crossingCount()
     << ", eq=" << eqPrint(equivalence_) << ")";
}

std::string TriplePixelPlaneIntersection::shortName() const {
  return "TP" + PixelPlaneIntersectionNR::shortName();
}

unsigned int TriplePixelPlaneIntersection::findFaceEdge(unsigned int,
							HomogeneityTet*)
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

IsecEquivalenceClass::IsecEquivalenceClass(HomogeneityTet *htet,
					   PlaneIntersection *pi,
					   unsigned int id
#ifdef DEBUG
					   , bool verbose
#endif // DEBUG
					   )
  : htet(htet),
    loc_(pi->location3D()),
    id(id)
#ifdef DEBUG
  , verbose(verbose)
#endif // DEBUG
{
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "IsecEquivalenceClass::ctor: id=" << id << " " << this
// 	    << std::endl;
// #endif	// DEBUG
  pi->setEquivalence(this);
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "IsecEquivalenceClass::ctor: done " << this
// 	    << " " << *this << " size=" << intersections.size() << std::endl;
// #endif	// DEBUG
}

IsecEquivalenceClass::~IsecEquivalenceClass() {
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "IsecEquivalenceClass::dtor: id=" << id << " " << this
//   	    << std::endl;
// #endif // DEBUG
}

void IsecEquivalenceClass::addIntersection(PlaneIntersection *pi) {
  // This is called by the PlaneIntersection copy constructor and
  // PlaneIntersection::setEquivalence.  The copy constructor is
  // adding an incompletely built object, so don't call any virtual
  // PlaneIntersection methods here.
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "IsecEquivalenceClass::addIntersection: this=" << *this
// 	    << " intersection=" << pi
// 	    // << " " << pi->shortName()
// 	    << std::endl;
// #endif // DEBUG
  intersections.push_back(pi);
  //  pi->addPlanesToEquivalence(this);
}

void IsecEquivalenceClass::removeIntersection(PlaneIntersection *pi) {
  // This does *not* remove the planes in *pi from the sets of planes
  // that define this equivalence class.  The point is being deleted,
  // but that doesn't change the fact that its planes meet at the
  // common point for the class.

  // This is called from the PlaneIntersection destructor, so
  // PlaneIntersection derived class methods aren't accessible.  Don't
  // try to print any more than the pointer.

  auto iter = std::find(intersections.begin(), intersections.end(), pi);
  if(iter != intersections.end()) {
    intersections.erase(iter);
  }
  else {
    oofcerr << "IsecEquivalenceClass::removeIntersection:"
	    << " failed to remove intersection"<< std::endl;
    oofcerr << "IsecEquivalenceClass::removeIntersection: intersection="
	    << pi << std::endl;
    oofcerr << "IsecEquivalenceClass::removeIntersection: this=" << *this
	    << std::endl;
    oofcerr << "IsecEquivalenceClass::removeIntersection: insersections=";
    std::cerr << intersections;
    oofcerr << std::endl;
    throw ErrProgrammingError("removeIntersection failed!", __FILE__, __LINE__);
  }
  // pi->removeEquivalence();
}

bool IsecEquivalenceClass::contains(PlaneIntersection *pi) const {
  return (std::find(intersections.begin(), intersections.end(), pi)
	  != intersections.end());
}

void IsecEquivalenceClass::addPixelPlane(const HPixelPlane *pp, bool collinear)
{
  pixelPlanes.insert(pp->unoriented());
  loc_[pp->direction()] = pp->normalOffset();
  if(collinear)
    includeCollinearPlanes(pp);
}

bool IsecEquivalenceClass::containsPixelPlane(const HPixelPlane *pp) const {
  return pixelPlanes.count(pp->unoriented()) > 0;
}

void IsecEquivalenceClass::addFacePlane(const FacePlane *fp, bool collinear) {
  facePlanes.insert(fp);
  if(collinear)
    includeCollinearPlanes(fp);
}

void IsecEquivalenceClass::addFacePixelPlane(const FacePixelPlane *fpp,
					     bool collinear)
{
  pixelFaces.insert(fpp);
  loc_[fpp->direction()] = fpp->normalOffset();
  if(collinear)
    includeCollinearPlanes(fpp);
}

bool IsecEquivalenceClass::containsFacePlane(const FacePlane *fp) const {
  if(facePlanes.count(fp) > 0)
    return true;
  // TODO: This could be done without the dynamic cast if we added
  // virtual functions isInEquivalenceClass to FacePlane and
  // FacePixelPlane.
  const FacePixelPlane *fpp = dynamic_cast<const FacePixelPlane*>(fp);
  return (fpp != nullptr && pixelFaces.count(fpp) > 0);
}

void IsecEquivalenceClass::includeCollinearPlanes(const HPlane *plane) {
  includeCollinearPlaneSet(plane, pixelPlanes);
  includeCollinearPlaneSet(plane, facePlanes);
  includeCollinearPlaneSet(plane, pixelFaces);
}

template <class SET>
void IsecEquivalenceClass::includeCollinearPlaneSet(const HPlane *plane,
						    SET &planeset)
{
  for(auto *pp : planeset) {
    if(!pp->coincident(*plane)) {
      HPlaneSet coplanes = htet->getCollinearPlanes(plane, pp);
      for(const HPlane *ppp : coplanes) {
	if(ppp == ppp->unoriented())
	  ppp->addCollinearToEquivalence(this);
      }
    }
  }
}

FacePlaneSet IsecEquivalenceClass::sharedFaces(
				       const IsecEquivalenceClass *other,
				       const FacePlane *exclude)
  const
{
  FacePlaneSet shared;
  std::set_intersection(facePlanes.begin(), facePlanes.end(),
			other->facePlanes.begin(), other->facePlanes.end(),
			std::inserter(shared, shared.end()),
			FacePlaneSet::key_compare());
  std::set_intersection(pixelFaces.begin(), pixelFaces.end(),
			other->pixelFaces.begin(), other->pixelFaces.end(),
			std::inserter(shared, shared.end()),
			FacePixelPlaneSet::key_compare());
  if(exclude)
    shared.erase(exclude);
  return shared;
}

// sharedPlane returns any kind of plane (pixel plane or face plane)
// that's shared between this IsecEquivalenceClass and the other one,
// excluding the given FacePlane.

const HPlane *IsecEquivalenceClass::sharedPlane(
					const IsecEquivalenceClass *other,
					const FacePlane *exclude)
  const
{
  // TODO: Is it worth doing these loops more intelligently, or using
  // std::set_intersection?  The sets are small.
  for(const HPixelPlane *p0 : pixelPlanes)
    for(const HPixelPlane *p1 : other->pixelPlanes)
      if(p0 == p1)
	return p0;
  for(const FacePlane *fp0 : facePlanes)
    if(fp0 != exclude)
      for(const FacePlane *fp1 : other->facePlanes)
	if(fp0 == fp1)
	  return fp0;
  for(const FacePixelPlane *fpp0 : pixelFaces)
    if(dynamic_cast<const FacePlane*>(fpp0) != exclude)
      for(const FacePixelPlane *fpp1 : other->pixelFaces)
	if(fpp0 == fpp1)
	  return fpp0;
  return nullptr;
}

void IsecEquivalenceClass::merge(IsecEquivalenceClass *other) {
  assert(other != this);
  assert(other != nullptr);
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "IsecEquivalenceClass::merge: this=" << this << " " << *this
// 	    << " (size=" << size() << ")"
// 	    << " other=" << other << " " << *other
// 	    << " (size=" << other->size() << ")" << std::endl;
//     oofcerr << "IsecEquivalenceClass::merge:       intersections = {";
//     std::cerr << intersections;
//     oofcerr << "}" << std::endl;
//     oofcerr << "IsecEquivalenceClass::merge: other intersections = {";
//     std::cerr << other->intersections;
//     oofcerr << "}" << std::endl;
    
//   }
// #endif // DEBUG
#ifdef DEBUG
  double dist2 = norm2(location3D() - other->location3D());
  if(dist2 > 1.e-10) {
    oofcerr << "IsecEquivalenceClass::merge: incompatible classes!  dist="
	    << sqrt(dist2) << std::endl;
    oofcerr << "IsecEquivalenceClass::merge this="  << *this << " "
	    << location3D() << std::endl;
    oofcerr << "IsecEquivalenceClass::merge other=" << *other << " "
	    << other->location3D() << std::endl;
    throw ErrProgrammingError("Failed to merge equivalence classes!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  pixelPlanes.insert(other->pixelPlanes.begin(), other->pixelPlanes.end());
  facePlanes.insert(other->facePlanes.begin(), other->facePlanes.end());
  pixelFaces.insert(other->pixelFaces.begin(), other->pixelFaces.end());
  for(PlaneIntersection *pi : other->intersections) {
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "IsecEquivalenceClass::merge: changing equivalence_ in "
// 	      << pi << " " << *pi << std::endl;
// #endif // DEBUG
    pi->setEquivalenceOnly(this);
  }
  intersections.insert(intersections.end(),
		       other->intersections.begin(),
		       other->intersections.end());
  other->intersections.clear();
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "IsecEquivalenceClass::merge: after merge, this=" << *this
// 	    << std::endl;
//     oofcerr << "IsecEquivalenceClass::merge: intersections = {";
//     std::cerr << intersections;
//     oofcerr << "}" << std::endl;
//     OOFcerrIndent indent(2);
//     for(PlaneIntersection *pi : intersections) {
//       oofcerr << "IsecEquivalenceClass::merge: " << pi << " " << *pi
// 	      << std::endl;
//     }
//   }
// #endif // DEBUG
} // end IsecEquivalenceClass::merge

std::ostream &operator<<(std::ostream &os, const IsecEquivalenceClass &eqclass)
{
  if(eqclass.pixelPlanes.empty() && eqclass.facePlanes.empty() &&
     eqclass.pixelFaces.empty())
    {
      os << "uninitialized";
    }
  else {
    for(const HPixelPlane *pp : eqclass.pixelPlanes)
      os << pp->shortName();
    for(const FacePlane *fp : eqclass.facePlanes)
      os << fp->shortName();
    for(const FacePixelPlane *fpp : eqclass.pixelFaces)
      os << fpp->shortName();
  }
  os << "(" << eqclass.id << ")";
  return os;
}

#ifdef DEBUG

bool IsecEquivalenceClass::verify() {
  for(const PlaneIntersection *pi : intersections)
    if(pi->equivalence() != this) {
      oofcerr << "IsecEquivalenceClass::verify: isec->equivalence() != this!"
	      << std::endl;
      oofcerr << "IsecEquivalenceClass::verify: this=" << this << " " << *this
	      << std::endl;
      oofcerr << "IsecEquivalenceClass::verify: intersection=" << pi << " "
	      << *pi << std::endl;
      return false;
    }
  return true;
}

void IsecEquivalenceClass::dump() {
  oofcerr << "IsecEquivalenceClass::dump: this= " << *this
    	  << std::endl;
  OOFcerrIndent indent(2);
  for(PlaneIntersection *pi : intersections) {
    oofcerr << "IsecEquivalenceClass::dump: intersection= " << pi;
    oofcerr << " " << *pi << std::endl;
  }
}

#endif // DEBUG

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

std::ostream &operator<<(std::ostream &os, ISEC_ORDER order) {
  if(order == FIRST)
    os << "FIRST";
  else if(order == SECOND)
    os << "SECOND";
  else
    os << "NONCONTIGUOUS";
  return os;
}

std::ostream &operator<<(std::ostream &os, const Interiority &intr) {
  if(intr == INTERIOR)
    os << "INTERIOR";
  else if (intr == EXTERIOR)
    os << "EXTERIOR";
  else
    os << "MIXED";
  return os;
}
