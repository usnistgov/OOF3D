// -*- C++ -*-
// $RCSfile: cskeletonface.C,v $
// $Revision: 1.1.2.48 $
// $Author: langer $
// $Date: 2014/12/14 22:49:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/differ.h"
#include "common/geometry.h"
#include "common/printvec.h"
#include "common/IO/oofcerr.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonsegment.h"
#include <vtkTriangle.h>

const std::string CSkeletonFace::modulename_(
				     "ooflib.SWIG.engine.cskeletonface");
const std::string CSkeletonFace::classname_("CSkeletonFace");

long CSkeletonFace::globalFaceCount = 0;
static SLock globalFaceCountLock;

CSkeletonFace::CSkeletonFace(CSkeletonNodeVector *ns) 
  : CSkeletonMultiNodeSelectable(ns)
{
  // std::cerr << "CSkeletonFace::ctor: uid=" << uid << " nodes=";
  // for(int i=0; i<3; i++)
  //   std::cerr << " " << (*nodes)[i]->getUid();
  // std::cerr << std::endl;
  nelements=0;
  defunct=true;			// because there are no elements yet.
  globalFaceCountLock.acquire();
  ++globalFaceCount;
  globalFaceCountLock.release();
}

CSkeletonFace::~CSkeletonFace() {
  globalFaceCountLock.acquire();
  --globalFaceCount;
  globalFaceCountLock.release();
}

long get_globalFaceCount() {
  return CSkeletonFace::globalFaceCount;
}


CSkeletonFace* CSkeletonFace::new_child(int idx, 
					vtkSmartPointer<vtkPoints> pts = NULL)
{
  CSkeletonNodeVector *node_children = get_node_children();
  CSkeletonFace *child  = new CSkeletonFace(node_children);
  return child;
}
  
vtkSmartPointer<vtkCell> CSkeletonFace::getEmptyVtkCell() const {
  return vtkSmartPointer<vtkTriangle>::New();
}

double CSkeletonFace::area() const {
  const Coord &x1 = (*nodes)[0]->position();
  const Coord &x2 = (*nodes)[1]->position();
  const Coord &x3 = (*nodes)[2]->position();
  // triangleArea is always non-negative!
  double a = triangleArea(x1, x2, x3);
  return a;
}

double CSkeletonFace::areaInVoxelUnits(const CMicrostructure *MS) const  {
  Coord fpts[3];
  Coord delta = MS->sizeOfPixels();
  for(int i=0; i<3; ++i) {
    fpts[i] = (*nodes)[i]->position()/delta;
  }
  double a = triangleArea(fpts[0], fpts[1], fpts[2]);
  return a;
}

double CSkeletonFace::areaInFractionalUnits(const CMicrostructure *MS) const  {
  Coord fpts[3];
  Coord delta = MS->size();
  for(int i=0; i<3; ++i) {
    fpts[i] = (*nodes)[i]->position()/delta;
  }
  double a = triangleArea(fpts[0], fpts[1], fpts[2]);
  return a;
}

double CSkeletonFace::homogeneity(const CMicrostructure*) const {
  // TODO 3.1: Write this!  And then use it to choose faces to refine,
  // maybe.
  return 1.0;
}



void CSkeletonFace::increment_nelements() {
  ++nelements;
  defunct=false;
}

void CSkeletonFace::decrement_nelements() {
  --nelements;
  defunct = (nelements == 0);
}

void CSkeletonFace::getElements(const CSkeletonBase *skel,
				ConstCSkeletonElementVector &result)
  const
{
  skel->getFaceElements(this, result);
}

void CSkeletonFace::getElements(const CSkeletonBase *skel,
				CSkeletonElementVector &result)
{
  skel->getFaceElements(this, result);
}

const CSkeletonElement *CSkeletonFace::getElement(const CSkeletonBase *skel,
						  int which)
  const
{
  ConstCSkeletonElementVector elements;
  skel->getFaceElements(this, elements);
  return elements[which];
}

Coord CSkeletonFace::normal() const {
  Coord x[3];
  Coord n;
  for(int i=0; i<3; ++i) {
    x[i] = (*nodes)[i]->position();
  }
  vtkTriangle::ComputeNormal(x[0].xpointer(), x[1].xpointer(), x[2].xpointer(),
			     n.xpointer());
  return n;
}

// Is a point assumed to be in the plane of the face actually within
// the face?  Points on the edge of the face are *not* interior.

bool CSkeletonFace::contains(const Coord &pt) const {
  // radius[i] is the vector from pt to the i^th corner
  Coord radius[3];
  for(int i=0; i<3; i++)
    radius[i] = getNode(i)->position() - pt;

  // The point is inside if the normal components of the cross product
  // of all pairs of radii all are nonzero and have the same sign.
  int sign = 0;
  Coord norm = normal();
  for(int i=0; i<3; i++) {
    double crs = dot(cross(radius[i], radius[(i+1)%3]), norm);
    if(crs == 0.0) 
      return false;
    if(sign == 0)
      sign = crs > 0? 1 : -1;
    if((sign > 0 && crs < 0) || (sign < 0 && crs > 0))
      return false;
  }
  return true;
}

void CSkeletonFace::print(std::ostream &os) const {
  os << "Face(" << uid << ", ";
  printNodes(os);
  os << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

CSkeletonNode *CSkeletonFace::get_other_node(const CSkeletonSegment *s) const {
  for(unsigned int i=0; i<nnodes(); ++i) {
    CSkeletonNode *node = (*nodes)[i];
    if(*node != *s->getNode(0) && *node != *s->getNode(1))
      return node;
  }
  throw ErrProgrammingError("Couldn't find other node", __FILE__, __LINE__);
  return NULL;
}

const CSkeletonElement *CSkeletonFace::get_other_element(
						 const CSkeletonBase *skel,
						 const CSkeletonElement *el)
  const 
{
  ConstCSkeletonElementVector elems;
  skel->getFaceElements(this, elems);
  for(unsigned int i=0; i<elems.size(); i++)
    if(elems[i] != el)
      return elems[i];
  return NULL;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

long OrientedCSkeletonFace::globalOrientedFaceCount = 0;
static SLock globalOrientedFaceCountLock;

OrientedCSkeletonFace::OrientedCSkeletonFace(CSkeletonFace *f, int d)
  : face(f), direction(d)
{
  globalOrientedFaceCountLock.acquire();
  globalOrientedFaceCount++;
  globalOrientedFaceCountLock.release();
}

OrientedCSkeletonFace::~OrientedCSkeletonFace() {
  globalOrientedFaceCountLock.acquire();
  globalOrientedFaceCount--;
  globalOrientedFaceCountLock.release();
}

long get_globalOrientedFaceCount() {
  return OrientedCSkeletonFace::globalOrientedFaceCount;
}

void OrientedCSkeletonFace::set_direction(const CSkeletonNode *n0, 
					  const CSkeletonNode *n1,
					  const CSkeletonNode *n2) 
{
  const CSkeletonNode *fn[3] = {face->getNode(0), face->getNode(1),
				face->getNode(2)};
  for(int i=0; i<3; i++) {
    if(n0 == fn[i] && n1 == fn[(i+1)%3] && n2 == fn[(i+2)%3]) {
      direction = 1;
      return;
    }
  }
  for(int i=0; i<3; i++) {
    if(n0 == fn[i] && n1 == fn[(i+2)%3] && n2 == fn[(i+1)%3]) {
      direction = -1;
      return;
    }
  }
  throw ErrProgrammingError("Incorrect node set in OrientedCSkeletonFace",
			    __FILE__, __LINE__);
}
  
Coord OrientedCSkeletonFace::get_direction_vector() const {
  return face->normal() * direction;
}

double OrientedCSkeletonFace::get_offset() const {
  // Find the distance from the origin to the plane of the face in the
  // direction of the normal.
  return dot(face->center(), get_direction_vector());
}

CSkeletonNode *OrientedCSkeletonFace::getNode(int i) const {
  if(direction == 1)
    return face->getNode(i);
  else
    return face->getNode(2-i);
}

vtkSmartPointer<vtkIdList> OrientedCSkeletonFace::getPointIds() const {
  return get_face()->getPointIds();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

OrientedSurface::OrientedSurface()
  : closed_(false)
{}

OrientedSurface::~OrientedSurface() {
  clear();
}

void OrientedSurface::clear() {
  for(OrientedCSkeletonFaceSet::iterator it=faces.begin(); it!=faces.end(); 
      ++it)
    {
      delete (*it);
    }
  faces.clear();
}

OrientedCSkeletonFaceSet::const_iterator OrientedSurface::begin() const {
  return faces.begin();
}

OrientedCSkeletonFaceSet::const_iterator OrientedSurface::end() const {
  return faces.end();
}

// normal() is the area-weighted average of the normals to each face
// in the surface.

Coord OrientedSurface::normal() const {
  Coord nrml;
  double area = 0;
  for(OrientedCSkeletonFaceSet::const_iterator i=begin(); i!=end(); ++i) {
    OrientedCSkeletonFace *face = *i;
    double a = face->get_face()->area();
    area += a;
    Coord n = face->get_direction_vector();
    nrml += a * n;
  }
  return nrml/area;
}

// Compute the signed volume enclosed by a closed oriented surface.
// If the normals all point outwards, the volume is positive.

double OrientedSurface::volume() const {
  if(!closed())
    return 0.0;
  // Each face's contribution to the volume is 1/3 of its area times
  // the distance between the plane of the face and some arbitrarily
  // chosen center (which is the same for all faces).  That distance
  // is the normal dotted into the vector from any one of the corners
  // of the face to the center.
  double vol = 0;
  
  // Compute the center point.  We could be lazy and just use the
  // origin since the center is arbitrary, but if we're computing the
  // volume of a small surface far from the origin we could have
  // trouble with roundoff errors.  So here we compute the mean
  // position of the nodes and use that instead.
  Coord center;
  int count = 0;
  for(OrientedCSkeletonFaceSet::const_iterator i=begin(); i!=end(); ++i) {
    const CSkeletonFace *face = (*i)->get_face();
    for(unsigned int n=0; n<face->nnodes(); ++n) {
      center += face->getNode(n)->getPosition();
    }
    count += face->nnodes();
  }
  center /= (double) count;

  for(OrientedCSkeletonFaceSet::const_iterator i=begin(); i!=end(); ++i) {
    OrientedCSkeletonFace *face = *i;
    Coord n = face->get_direction_vector(); // normal to the face
    CSkeletonNode *node = face->get_face()->getNode(0);
    vol += (face->get_face()->area() * 
	    dot(n, (node->getPosition()-center)));
  }
  return vol/3.;
}

void OrientedSurface::remove(CSkeletonFace *face) {
  for(OrientedCSkeletonFaceSet::iterator i=faces.begin(); i!=faces.end(); i++) {
    if((*i)->get_face() == face) {
      faces.erase(i);
      closed_ = false;
      delete *i;
      return;
    }
  }
}


void OrientedSurface::reverse() {
  for(OrientedCSkeletonFaceSet::iterator i=faces.begin(); i!=faces.end(); ++i) {
    (*i)->reverse();
  }
}

bool operator==(const OrientedCSkeletonFace &f1,
		const OrientedCSkeletonFace &f2)
{
  return (f1.getNode(0)->getIndex() == f2.getNode(0)->getIndex() && 
	  f1.getNode(1)->getIndex() == f2.getNode(1)->getIndex() && 
	  f1.getNode(2)->getIndex() == f2.getNode(2)->getIndex());
}  

bool operator!=(const OrientedCSkeletonFace &f1,
		const OrientedCSkeletonFace &f2)
{
  return !(f1.getNode(0)->getIndex() == f2.getNode(0)->getIndex() && 
	   f1.getNode(1)->getIndex() == f2.getNode(1)->getIndex() && 
	   f1.getNode(2)->getIndex() == f2.getNode(2)->getIndex());
}

bool operator<(const OrientedCSkeletonFace &f1,
	       const OrientedCSkeletonFace &f2)
{
  return *f1.get_face() < *f2.get_face();
}

bool OrientedCSkeletonFace::ltKey(const OrientedCSkeletonFace *f1,
				  const OrientedCSkeletonFace *f2)
{
  CSkeletonMultiNodeKey k1(f1->get_face());
  CSkeletonMultiNodeKey k2(f2->get_face());
  return k1 < k2;
}

std::ostream &operator<<(std::ostream &os, const OrientedCSkeletonFace &oface)
{
  os << "OrientedCSkeletonFace(face=" << *oface.get_face() << ", dir="
     << oface.get_direction() << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// orientFaces() takes a vector of CSkeletonFaces and returns a new
// OrientedSurface* if the faces can be arranged into an oriented
// surface, or 0.  If a startFace is given, its orientation determines
// the orientation of the whole surface. Otherwise the surface
// orientation is arbitrary.  The new surface takes over ownership of
// startFace.

OrientedSurface *orientFaces(const CSkeletonBase *skel,
			     const CSkeletonFaceVector *faces,
			     OrientedCSkeletonFace *startFace) 
{
  if(faces->empty())
    return NULL;

  // Make a map from segments to faces.
  SegFaceListMap facemap;
  for(CSkeletonFaceVector::const_iterator f=faces->begin(); f!=faces->end();
      ++f)
    {
      CSkeletonFace *face = *f;
      // Loop over the segments of the face.
      CSkeletonSegmentSet segs;
      skel->getFaceSegments(face, segs);
      for(CSkeletonSegmentSet::const_iterator s=segs.begin(); s!=segs.end();
	  ++s)
	{
	  CSkeletonSegment *seg = *s;
	  // Look for the list of faces for the current segment.
	  SegFaceListMap::iterator fl = facemap.find(*s);
	  if(fl != facemap.end()) {
	    // Put the current face in the list.
	    (*fl).second.push_back(face);
	  }
	  else {
	    // Make a new list and put the face in it.
	    facemap[seg] = CSkeletonFaceList(1, face);
	  }
	} // end loop over segs
    } // end loop over faces
  
  // Check that no segment has more than two faces.
  for(SegFaceListMap::iterator sf=facemap.begin(); sf!=facemap.end(); ++sf) {
    int nsegs = (*sf).second.size();
    if(nsegs > 2) {
#ifdef DEBUG
      oofcerr << "orientFaces: too many faces per segment!" << std::endl;
#endif // DEBUG
      return NULL;
    }
  }

  OrientedSurface *surface = new OrientedSurface();

  // Choose the initial face.  Use startFace if it's been provided.
  CSkeletonFace *face;
  OrientedCSkeletonFace *oface;
  int direction;
  if(startFace) {
    face = startFace->get_face();
    oface = startFace;
    direction = startFace->get_direction();
  }
  else {
    // Make an arbitrary choice of initial face and direction.
    face = (*faces)[0];
    direction = 1;
    oface = new OrientedCSkeletonFace(face, direction);
  }

  // Insert the initial face into the surface.
  surface->insert(oface);
  // Keep track of the "active" perimeter segments of the surface.
  // Active segments are ones to which another face might connect.
  // Initially, all segments of the starting face are active.
  CSkeletonSegmentSet activePerimeter;
  // Also keep track of the face responsible for adding a segment to
  // the active perimeter list.
  SegFaceMap activeFaces;
  for(int i=0; i<3; i++) {
    CSkeletonSegment *seg = skel->getFaceSegment(face, i);
    activePerimeter.insert(seg);
    activeFaces[seg] = oface;
  }
  
  if(!augmentSurface(skel, activePerimeter, activeFaces, facemap, surface)) {
#ifdef DEBUG
    oofcerr << "augmentSurface: unorientable surface detected!"
	    << std::endl;
#endif // DEBUG
    delete surface;
    return NULL;
  }
  
  // If not all the faces are in the surface, there must be faces that
  // don't connect to the original one.
  if(surface->size() != faces->size()) {
#ifdef DEBUG
    oofcerr << "orientFaces: discontiguous faces!" << std::endl;
#endif	// DEBUG
    delete surface;
    return NULL;
  }
  return surface;
} // end orientFaces

// augmentSurface does the hard work of putting new faces onto an
// oriented surface.  It's used by orientFaces, above, and
// CSkeletonFaceBoundary::appendFaces.  It returns true if it
// successfully attaches all of the new faces to the surface.

bool augmentSurface(const CSkeletonBase *skel,
		    CSkeletonSegmentSet &activePerimeter,
		    SegFaceMap &activeFaces, 
		    SegFaceListMap &facemap,
		    OrientedSurface *surface) 
{
  if(activePerimeter.empty()) {
#ifdef DEBUG
    oofcerr << "augmentSurface: Nothing to add!" << std::endl;
#endif	// DEBUG
    return false;
  }
  if(surface->closed()) {
#ifdef DEBUG
    oofcerr << "augmentSurface: Attempt to add faces to a closed surface."
	    << std::endl;
#endif	// DEBUG
    return false;
  }
  // Assume that the new faces will close the surface.  If an
  // unmatchable segment is found, this assumption will be corrected.
  surface->setClosed(true);
  // While there are segments on the activePerimeter, pick one and try
  // to attach a face to it. 
  while(!activePerimeter.empty()) {
    // Pick an active segment.
    CSkeletonSegment *activeSeg = *activePerimeter.begin();
    // Remove the active segment from the active list.
    activePerimeter.erase(activePerimeter.begin());
    // Look for a face that abuts the active segment.
    SegFaceListMap::iterator sfmi = facemap.find(activeSeg);
    assert(sfmi != facemap.end());
    CSkeletonFaceList &facelist = (*sfmi).second;
    // One of the faces adjoining the active segment is already in the
    // surface.  If there's another face, it should be added to the
    // surface and its other segments added to the active perimeter.
    if(facelist.size() == 2) {
      OrientedCSkeletonFace *oldOFace = activeFaces[activeSeg];
      CSkeletonFace *newFace = facelist.front();
      if(newFace == oldOFace->get_face())
	newFace = facelist.back();

      // If the nodes shared by the new and old faces come in the
      // *opposite* order in the two faces, then the direction of the
      // two faces is the same.  Otherwise the new face has the
      // opposite direction of the old face.
      CSkeletonNode *node0 = activeSeg->getNode(0);
      CSkeletonNode *node1 = activeSeg->getNode(1);
      int oldOrder = oldOFace->get_face()->getNodeOrder(node0, node1);
      int newOrder = newFace->getNodeOrder(node0, node1);
      int dir = (newOrder == oldOrder ? -1 : 1) * oldOFace->get_direction();

      OrientedCSkeletonFace *newOrientedFace =
	new OrientedCSkeletonFace(newFace, dir);
      surface->insert(newOrientedFace);
      // Put the other two segments in the active set, unless they're
      // already there, in which case the face being added connects to
      // them too.  In that case, they should be removed.
      for(int i=0; i<3; i++) {	// Loop over segments of the new face
	CSkeletonSegment *seg = skel->getFaceSegment(newFace, i);
	if(seg != activeSeg) {
	  // This is not a segment of the old face.  Is it already in
	  // the active perimeter?
	  CSkeletonSegmentSet::iterator s = activePerimeter.find(seg);
	  if(s == activePerimeter.end()) {
	    // The segment is not in the active perimeter.
	    activePerimeter.insert(seg);
	    activeFaces[seg] = newOrientedFace;
	  }
	  else {
	    // The segment is already in the active perimeter, so the
	    // newly added face matches it too.  It's no longer
	    // active.
	    activePerimeter.erase(s);
	    // Check that the orientation matches!  Moebius strips are
	    // not permitted.
	    OrientedCSkeletonFace *oldOFace = activeFaces[seg];
	    CSkeletonNode *n0 = seg->getNode(0);
	    CSkeletonNode *n1 = seg->getNode(1);
	    int oldOrdr = oldOFace->get_face()->getNodeOrder(n0, n1);
	    int newOrdr = newFace->getNodeOrder(n0, n1);
	    if(oldOrdr*oldOFace->get_direction() != -newOrdr*dir) {
	      return false;
	    }
	  }
	}
      }	// end loop over segments of the newly added face
    }	// end if facelist.size == 2
    else {
      // facelist.size == 1.  This segment has only one face, so the
      // surface is not closed.
      assert(facelist.size() == 1);
      surface->setClosed(false);
    }

  } // end while activePerimeter.size > 0
  return true;
} // end augmentSurface
