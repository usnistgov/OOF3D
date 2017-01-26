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
#include <math.h>
#include <algorithm>
#include <fstream>

#include "common/cdebug.h"
#include "common/cmicrostructure.h"
#include "common/printvec.h"
#include "common/tostring.h"
#include "engine/cskeletonelement.h"
#include "engine/facefacet.h"
#include "engine/homogeneitytet.h"
#include "engine/intersectiongroup.h"
#include "engine/ooferror.h"
#include "engine/pixelplanefacet.h"
#include "engine/planeintersection.h"

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// When debugging it's convenient to turn on verbose output only for
// particular voxel categories and pixel planes.

#ifdef DEBUG

static std::set<unsigned int> vcategories;

void setVerboseCategory(unsigned int cat) {
  oofcerr << "setVerboseCategory: " << cat << std::endl;
  vcategories.insert(cat);
}

bool HomogeneityTet::verboseCategory_(bool vrbse, unsigned int category) const
{
  return vrbse && (vcategories.empty() || vcategories.count(category) == 1);
}

static std::set<HPixelPlane> vplanes;
static bool noPlanes = false;

void setVerbosePlane(unsigned int direction, int offset, int normal) {
  auto p = vplanes.emplace(direction, offset, normal);
  oofcerr << "setVerbosePlane: " << *p.first << std::endl;
}

void setNoVerbosePlanes() {
  noPlanes = true;
}

bool HomogeneityTet::verbosePlane_(bool vrbse, const HPixelPlane *pixplane)
  const
{
  return (vrbse && !noPlanes &&
	  (vplanes.empty() || vplanes.count(*pixplane) == 1));
}

static std::set<unsigned int> vfaces;
static bool noFaces = false;

void setVerboseFace(unsigned int face) {
  oofcerr << "setVerboseFace: " << face << std::endl;
  vfaces.insert(face);
}

void setVerboseAllFaces() {
  for(unsigned int f=0; f<4; f++)
    vfaces.insert(f);
}

void setNoVerboseFaces() {
  noFaces = true;
}

bool HomogeneityTet::verboseFace_(bool vrbse, unsigned int face) const {
  return (vrbse && !noFaces && (vfaces.empty() || vfaces.count(face) == 1));
}

template <class LOOSEENDCONTAINER>
void printLooseEnds(const LOOSEENDCONTAINER &le) {
  if(!le.empty()) {
    for(FaceEdgeIntersection *fei : le)
      oofcerr << "printLooseEnds: " << *fei << std::endl;
  }
  else
    oofcerr << "printLooseEnds: (none)" << std::endl;
}

std::ofstream *dumpfile = 0;

void openDumpFile(const std::string &name) {
  if(dumpfile)
    dumpfile->close();
  oofcerr << "openDumpFile: opening " << name << std::endl;
  dumpfile = new std::ofstream(name.c_str());
}

void dumpSegment(const Coord3D &a, const Coord3D &b) {
  // TODO: This ought to convert from pixel coordinates to physical
  // coordinates.
  if(dumpfile) {
    *dumpfile << a << ", " << b << std::endl;
  }
}

void closeDumpFile() {
  if(dumpfile) {
    dumpfile->close();
    dumpfile = 0;
  }
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the nodes of an edge of a face, going counterclockwise around
// the face.  The faceIndex is the vtk index.  The edgeIndex is the
// index of the edge on the face, not on the tet. 

void getEdgeNodes(unsigned int faceIndex, unsigned int edgeIndex,
		  unsigned int &inode0, unsigned int &inode1)
{
#ifdef DEBUG
  if(edgeIndex >= NUM_TET_FACE_EDGES || faceIndex >= NUM_TET_FACES) {
    oofcerr << "getEdgeNodes: faceIndex=" << faceIndex << " edgeIndex="
	    << edgeIndex << std::endl;
    throw ErrProgrammingError("Bad arguments to getEdgeNodes!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  unsigned int edgeid = CSkeletonElement::faceEdges[faceIndex][edgeIndex];
  if(CSkeletonElement::faceEdgeDirs[faceIndex][edgeIndex] == 1) {
    inode0 = vtkTetra::GetEdgeArray(edgeid)[0];
    inode1 = vtkTetra::GetEdgeArray(edgeid)[1];
  }
  else {
    inode0 = vtkTetra::GetEdgeArray(edgeid)[1];
    inode1 = vtkTetra::GetEdgeArray(edgeid)[0];
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


HomogeneityTet::HomogeneityTet(const CSkeletonElement *element,
			       const CMicrostructure *ms
#ifdef DEBUG
			       , bool verbose
#endif // DEBUG
			       )
  : edgeLengths(6),
    faces(4),
    faceCenters(4),
    faceAreaVectors(4),
    testVoxels(4),
    testVoxelsFound(4, false),
    faceFacetEdgeCount(0),
    intersectionID_(0),
    equivalenceID_(0),
    coincidentPixelPlanes(4, nullptr),
    microstructure(ms)
#ifdef DEBUG
  , verbose(verbose),
    verbosecategory(false),
    verboseplane(false),
    verboseface(false)
#endif  // DEBUG
{
#ifdef DEBUG
  allIntersections.clear();
#endif // DEBUG
  // compute the node positions in pixel coordinates, store in epts.
  element->pixelCoords(ms, epts);
  bbox_ = new CRectangularPrism(epts);
#ifdef DEBUG
  if(verbose) {
    oofcerr << "HomogeneityTet::ctor: writing element.lines" << std::endl;
    std::ofstream file("element.lines");
    for(unsigned int i=0; i<3; i++)
      for(unsigned int j=i+1; j<4; j++)
	file << epts[i] << ", " << epts[j] << std::endl;
    file.close();
  }
#endif // DEBUG

  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    Coord3D pt0 = epts[CSkeletonElement::getFaceArray(f)[0]];
    Coord3D pt1 = epts[CSkeletonElement::getFaceArray(f)[1]];
    Coord3D pt2 = epts[CSkeletonElement::getFaceArray(f)[2]];

    faceCenters[f] = (pt0 + pt1 + pt2)/3.0;

    // A more symmetric but more expensive expression for the area is
    // 0.5*(pt0%pt1 + pt1%pt2 + pt2%pt0).
    faceAreaVectors[f] = 0.5*((pt1 - pt0) % (pt2 - pt0));
    // If we know that components of the normal have to be zero, make
    // them really zero.  If the coordinates of any two nodes on the
    // face have the same i and j comoponents, then the k component of
    // the normal is zero (k != i, k != j).  This is important in
    // FaceEdgeIntersection::crosses.
    for(unsigned int k=0; k<3; k++) {
      unsigned int i=(k+1)%3;
      unsigned int j=(k+2)%3;
      if((pt0[i] == pt1[i] && pt0[j] == pt1[j]) ||
	 (pt1[i] == pt2[i] && pt1[j] == pt2[j]) ||
	 (pt2[i] == pt0[i] && pt2[j] == pt0[j]))
	{
	  faceAreaVectors[f][k] = 0;
	}
    }

    // Is this face on a pixel plane?
    bool fplane = false;
    for(unsigned int c=0; c<3; c++) { // loop over directions
      double x = pt0[c];
      if(x == floor(x) && pt1[c] == x && pt2[c] == x) {
	fplane = true;
	int nrml = epts[CSkeletonElement::oppNode[f]][c] > x ? -1 : 1;
	FacePixelPlane *fpp = new FacePixelPlane(c, x, nrml, f);
	pixelPlanes_.insert(fpp);
	allPlanes_.insert(fpp);
	faces[f] = fpp;
	coincidentPixelPlanes[f] = fpp; // vector
	coincidentFacePlanes[fpp] = fpp; // map, keyed by deref'd HPixelPlane*
	// The oppositely directed pixel plane is also coincident.
	HPixelPlane *opp = fpp->flipped();
	allPlanes_.insert(opp);
	pixelPlanes_.insert(opp);
	coincidentFacePlanes[opp] = fpp;
	break;
      }
    } // end loop over directions

    if(!fplane) {
      Coord3D normal = faceAreaVectors[f];
      normal /= sqrt(norm2(normal));
      double offset = dot(faceCenters[f], normal);
      faces[f] = new FacePlane(f, normal, offset);
      allPlanes_.insert(faces[f]);
    }

  } // end loop over tet faces

// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "HomogeneityTet::ctor: faces=" << std::endl;
//     for(unsigned int f=0; f<4; f++)
//       oofcerr << "     " << f << ": " << *faces[f] << std::endl;
//     // oofcerr << "HomogeneityTet::ctor: coincidentFacePlanes=" << std::endl;
//     // for(auto p : coincidentFacePlanes)
//     //   oofcerr << "     " << *p.first << ": " << *p.second << std::endl;
//   }
// #endif // DEBUG

  for(unsigned int e=0; e<NUM_TET_EDGES; e++) {
    unsigned int n0 = CSkeletonElement::getEdgeArray(e)[0];
    unsigned int n1 = CSkeletonElement::getEdgeArray(e)[1];
    edgeLengths[e] = sqrt(norm2(epts[n0] - epts[n1]));
  }

  for(unsigned int n=0; n<NUM_TET_NODES; n++) {
    tetCenter += epts[n];
  }
  tetCenter /= NUM_TET_NODES;

  // Find the edges that coincide with pixel planes and construct the
  // multimap "collinearPlanes", which maps a pair of planes into the
  // other planes that meet on the same line.  This is only done for
  // combinations of two faces and one or more pixel planes, because
  // those are the cases that are necessary for findFaceFacets to work.
// #ifdef DEBUG
//   if(verbose)
//     oofcerr << "HomogeneityTet::ctor: looking for collinear planes"
// 	    << std::endl;
// #endif // DEBUG
  for(unsigned int e=0; e<NUM_TET_EDGES; e++) {
    unsigned int n0 = CSkeletonElement::getEdgeArray(e)[0];
    unsigned int n1 = CSkeletonElement::getEdgeArray(e)[1];
    // First, find which pixel planes the edge lies on.  There can be
    // at most two.  Don't include pixel planes that are also faces.
    std::vector<unsigned int> dirs;
    dirs.reserve(2);
    for(unsigned int c=0; c<3; c++) {
      double x = epts[n0][c];
      if(x == floor(x) && epts[n1][c] == x) {
	// The edge between n0 and n1 is on pixel plane with position[c] == x
	dirs.push_back(c);
      }
    }
    if(!dirs.empty()) {		// if the edge is on any pixel planes
      std::vector<const HPlane*> planes;
      planes.reserve(2 + 2*dirs.size());
      planes.push_back(getTetFacePlane(CSkeletonElement::edgeFaces[e][0]));
      planes.push_back(getTetFacePlane(CSkeletonElement::edgeFaces[e][1]));
      for(unsigned int c : dirs) {
	double x = epts[n0][c];
	const HPixelPlane *pp = getPixelPlane(c, x, 1);
	const HPixelPlane *opp = getPixelPlane(c, x, -1);
	if(getCoincidentFacePlane(pp) == nullptr &&
	   getCoincidentFacePlane(opp) == nullptr)
	  {
	    planes.push_back(pp);
	    planes.push_back(opp);
	  }
      }
      // Put all combinations of the planes into collinearPlanes so
      // that any plane can be located from a pair of the others.
      for(unsigned int i=0; i<planes.size(); i++) {
	for(unsigned int j=0; j<planes.size(); j++) {
	  if(i != j && !planes[i]->coincident(*planes[j]))
	    {
	      for(unsigned int k=0; k<planes.size(); k++) {
		if(k != i && k != j &&
		   !planes[k]->coincident(*planes[i]) &&
		   !planes[k]->coincident(*planes[j]))
		  {
		    collinearPlanes.insert(
			 std::make_pair(std::make_pair(planes[i], planes[j]),
					planes[k]));
		  }
	      }
	    }
	}
      }
    } // end if the tet edge is on any pixel planes
  }   // end loop over tet edges

#ifdef DEBUG
  if(verbose) {
    for(const auto &planes : collinearPlanes) {
      oofcerr << "HomogeneityTet::ctor: collinear planes: "
	      << planes.first.first->shortName() << ", "
	      << planes.first.second->shortName() << ", "
	      << planes.second->shortName()
	      // << "     "
	      // << planes.first.first << " " << planes.first.second
	      // << " -> " << planes.second
	      << std::endl;
      }
  }
#endif // DEBUG
  
} // end HomogeneityTet ctor

HomogeneityTet::~HomogeneityTet() {
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "HomogeneityTet::dtor" << std::endl;
//   }
// #endif // DEBUG
  for(TetPlaneIsecMap::iterator tpi=tetPlaneIntersections.begin();
      tpi!=tetPlaneIntersections.end(); ++tpi)
    {
      for(const TetIntersection *tetPt : (*tpi).second) {
	delete tetPt;
      }
    }
  for(const HPlane *plane : allPlanes_)
    delete plane;
  for(PlaneIntersection *pt : extraPoints)
    delete pt;

  for(IsecEquivalenceClass *eqclass : equivalences)
    delete eqclass;

  for(FaceEdgeIntersection *fei : allFaceEdgeIntersections)
    delete fei;
  
  delete bbox_;
// #ifdef DEBUG
//   if(verbose) {
//     oofcerr << "HomogeneityTet::dtor: done" << std::endl;
//   }
// #endif // DEBUG
}

// getPixelPlane returns an existing pixel plane or makes a new one,
// adding it to the set of known pixel planes.  Only planes in this
// set should be used, so that different PixelPlane objects always
// refer to different pixel planes, and we can cheaply compare
// PixelPlane*s instead of calling PixelPlane::operator==.

HPixelPlane *HomogeneityTet::getPixelPlane(unsigned int dir, int offset,
						int normal)
{
  return getPixelPlane(new HPixelPlane(dir, offset, normal));
}

HPixelPlane *HomogeneityTet::getPixelPlane(HPixelPlane *pixplane) {
  auto result = pixelPlanes_.emplace(pixplane);
  if(!result.second)
    delete pixplane;
  else
    allPlanes_.insert(*result.first);
  (*result.first)->setUnoriented(getUnorientedPixelPlane(*result.first));
  assert((*result.first)->unoriented() != nullptr);
  assert((*result.first)->unoriented()->unoriented() ==
	 (*result.first)->unoriented());
  return *result.first;
}

// getUnorientedPixelPlane is just like getPixelPlane, but the plane
// it adds and returns always(*) has a positive orientation.  When planes
// are being used to define intersection points, the orientation of
// the plane isn't important, and it's important that coincident
// planes aren't perceived to be different, so only one orientation is
// used.
// (*) If the plane coincides with a face plane, the FacePixelPlane
// for the face is used. 

const HPixelPlane *HomogeneityTet::getUnorientedPixelPlane(
						   const HPixelPlane *pp)
{
  // If either the given plane or its inverse are already in use as a
  // face plane, return that plane.
  const FacePixelPlane *fpp = getCoincidentFacePlane(pp);
  if(fpp != nullptr)
    return fpp;
  HPixelPlane inverted(pp->direction(), pp->normalOffset(), -pp->normalSign());
  fpp = getCoincidentFacePlane(&inverted);
  if(fpp != nullptr)
    return fpp;
  
  HPixelPlane *oplane = new HPixelPlane(pp->direction(), pp->normalOffset(), 1);
  auto p = pixelPlanes_.emplace(oplane);
  if(!p.second)
    delete oplane;		// plane was already in pixelPlanes_
  else {
    allPlanes_.insert(*p.first); // plane is new
    oplane->setUnoriented(oplane);
  }
  assert(*p.first != nullptr);
  return *p.first;
}

const FacePixelPlane *HomogeneityTet::getCoincidentPixelPlane(
						      const FacePlane *fp)
  const
{
  return coincidentPixelPlanes[fp->face()]; // may return nullptr
}

const FacePixelPlane *HomogeneityTet::getCoincidentPixelPlane(unsigned int face)
  const
{
  return coincidentPixelPlanes[face]; // may return nullptr
}

const FacePixelPlane *HomogeneityTet::getCoincidentFacePlane(
						     const HPixelPlane *pp)
  const
{
  auto iter = coincidentFacePlanes.find(pp);
  if(iter == coincidentFacePlanes.end())
    return nullptr;
  return (*iter).second;
}

unsigned int HomogeneityTet::getCoincidentFaceIndex(const HPixelPlane *pp)
  const
{
  const FacePixelPlane *fpp = getCoincidentFacePlane(pp);
  if(fpp == nullptr)
    return NONE;
  return fpp->face();
}

ICoord3D HomogeneityTet::testVoxel(unsigned int f) {
  if(testVoxelsFound[f])
    return testVoxels[f];
  Coord3D ctr = faceCenters[f];
  ICoord3D testvxl(ctr[0], ctr[1], ctr[2]); // convert doubles to ints

  // If the center of the face is exactly on a voxel boundary, then
  // the voxel we want is the one that's inside the tet.  Use the face
  // area vectors to determine which side inside, and adjust the test
  // voxel position if necessary.
  Coord3D nrml = faceAreaVectors[f];	    
  for(unsigned int c=0; c<3; c++) {
    if(ctr[c] == testvxl[c]) {
      if(nrml[c] > 0)
	testvxl[c] -= 1;
    }
    if(testvxl[c] == microstructure->sizeInPixels()[c]) {
      testvxl[c] -= 1;
    }
  } // end loop over directions c
  testVoxels[f] = testvxl;
  testVoxelsFound[f] = true;
  return testvxl;
}

FaceEdgeIntersection *HomogeneityTet::newFaceEdgeIntersection(
					      PlaneIntersection *pi,
					      FaceFacetEdge *edge,
					      bool start)
{
  FaceEdgeIntersection *fei = new FaceEdgeIntersection(pi, edge, start);
  allFaceEdgeIntersections.insert(fei);
  return fei;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

HPlaneSet HomogeneityTet::getCollinearPlanes(const HPlane *p0, const HPlane *p1)
  const
{
  auto range = collinearPlanes.equal_range(std::make_pair(p0, p1));
  HPlaneSet planes;
  for(auto iter=range.first; iter!=range.second; ++iter)
    planes.insert(iter->second);
  return planes;
}

FacePlaneSet HomogeneityTet::getCollinearFaces(const HPlane *p0,
					       const HPlane *p1)
  const
{
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::getCollinearFaces: " << *p0 << " " << *p1
// 	    << std::endl;
//   }
//   OOFcerrIndent indent(2);
// #endif // DEBUG
  auto range = collinearPlanes.equal_range(std::make_pair(p0, p1));
  FacePlaneSet faces;
  for(auto iter=range.first; iter!=range.second; ++iter) {
// #ifdef DEBUG
//     if(verboseplane)
//       oofcerr << "HomogeneityTet::getCollinearFaces: found " << *iter->second
// 	      << std::endl;
// #endif // DEBUG
    // TODO: This cast is dumb and may be slow.  It shouldn't be
    // necessary when we get rid of the diamond inheritance in the
    // HPlane class hierarchy.
    const FacePlane *face = dynamic_cast<const FacePlane*>(iter->second);
    if(face != nullptr)
      faces.insert(face);
  }
  return faces;
}

bool HomogeneityTet::areCollinear(const HPlane *p0, const HPlane *p1,
				  const HPlane *p2)
  const
{
  auto range = collinearPlanes.equal_range(std::make_pair(p0, p1));
  for(auto iter=range.first; iter!=range.second; ++iter) {
    if(iter->second == p2)
      return true;
  }
  return false;
}

bool HomogeneityTet::areCollinear(const FacePlaneSet &faceSet) const {
  assert(faceSet.size() == 3);
  auto iter = faceSet.begin();
  const FacePlane *f0 = *iter;
  const FacePlane *f1 = *++iter;
  const FacePlane *f2 = *++iter;
  return areCollinear(f0, f1, f2);
}

unsigned int HomogeneityTet::getTetFaceIndex(const FacePlane *fp) const {
  for(unsigned int i=0; i<NUM_TET_FACES; i++) {
    if(faces[i] == fp)
      return i;
  }
  throw ErrProgrammingError("getTetFaceIndex failed!", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// mergeEquiv is called by the various PlaneIntersection::mergeWith
// virtual methods after they merge "point0" and "point1" to form
// "merged".  It updates the equivalence classes.  The two points must
// be in the same equivalence class, and that class's plane list must
// include all of the planes in both points.

void HomogeneityTet::mergeEquiv(PlaneIntersection *point0,
				PlaneIntersection *point1,
				PlaneIntersection *merged)
{
#ifdef DEBUG
  // if(verboseplane) {
  //   oofcerr << "HomogeneityTet::mergeEquiv: point0=" << point0 << " "
  // 	    << *point0 << std::endl;
  //   oofcerr << "HomogeneityTet::mergeEquiv: point1=" << point1 << " "
  // 	    << *point1 << std::endl;
  //   oofcerr << "HomogeneityTet::mergeEquiv: merged=" << *merged
  // 	    << std::endl;
  // }

  // if(!verify()) {
  //   oofcerr << "HomogeneityTet::mergeEquiv:"
  // 	    << " verification failed at beginning of mergeEquiv" << std::endl;
  //   throw ErrProgrammingError("Verification failed before mergeEquiv!",
  // 			      __FILE__, __LINE__);
  // }
  OOFcerrIndent indent(2);
#endif // DEBUG
  
  IsecEquivalenceClass *equivClass0 = point0->equivalence();
  IsecEquivalenceClass *equivClass1 = point1->equivalence();
  IsecEquivalenceClass *modifiedClass = nullptr;

  if(equivClass0 == nullptr) {
    if(equivClass1 == nullptr) {
      // Neither point is in an equivalence class.  Construct one.
      IsecEquivalenceClass *eqclass = new IsecEquivalenceClass(
					       this, merged, nextEquivalenceID()
#ifdef DEBUG
					       , verbose
#endif // DEBUG
							       );
// #ifdef DEBUG
//       if(verboseplane) {
// 	oofcerr << "HomogeneityTet::mergeEquiv: new equivalence class "
// 		<< *eqclass << std::endl;
// 	oofcerr << "HomogeneityTet::mergeEquiv: merged=" << *merged
// 		<< std::endl;
//       }
// #endif // DEBUG
      equivalences.push_back(eqclass);
      point0->setEquivalence(eqclass);
      point1->setEquivalence(eqclass);
      modifiedClass = eqclass;
// #ifdef DEBUG
//       if(verboseplane) {
// 	oofcerr << "HomogeneityTet::mergeEquiv: after merge, point0=" << *point0
// 		<< std::endl;
// 	oofcerr << "HomogeneityTet::mergeEquiv: after merge, point1=" << *point1
// 		<< std::endl;
//       }
// #endif // DEBUG
    }
    else {
      // Point 1 is already in an equivalence class but point 0 is not.
      point0->setEquivalence(equivClass1);
      merged->setEquivalence(equivClass1);
      modifiedClass = equivClass1;
    }
  }
  else {
    // Point 0 is already in an equivalence class
    if(equivClass1 == nullptr) {
      point1->setEquivalence(equivClass0);
      merged->setEquivalence(equivClass0);
    }
    else {
      // Both points are in equivalence classes
      if(equivClass0 == equivClass1) {
	merged->setEquivalence(equivClass0);
	modifiedClass = equivClass0;
      }
      else {
	// The points are in different equivalence classes.  Merge the classes.
// #ifdef DEBUG
// 	if(verboseplane) {
// 	  oofcerr << "HomogeneityTet::mergeEquiv(3): merging classes"
// 		  << std::endl;
// 	}
// #endif // DEBUG
	equivClass0->merge(equivClass1); // Resets all pointers to equivClass1.
	merged->setEquivalence(equivClass0);
	// equivalences.erase(equivClass1);
	auto eptr = std::find(equivalences.begin(), equivalences.end(),
			      equivClass1);
	assert(eptr != equivalences.end());
	equivalences.erase(eptr);
	delete equivClass1;
	modifiedClass = equivClass0;
      }
    }
  }
  // Since modifiedClass is new or newly changed, it now may be
  // equivalent to some other class(es).  Find the other classes,
  // merge them, and delete them.
  // TODO: This may be slow.  Does it have to be done every time?
  bool foundEquiv = true;
  while(foundEquiv) {
    foundEquiv = false;
    std::set<IsecEquivalenceClass*> deleteThese;
    for(IsecEquivalenceClass *eqclass : equivalences) {
      if(eqclass != modifiedClass && modifiedClass->isEquivalent(eqclass)) {
	modifiedClass->merge(eqclass);
	deleteThese.insert(eqclass);
	foundEquiv = true;
      }
    }
    for(IsecEquivalenceClass *eqclass : deleteThese) {
      auto eptr = std::find(equivalences.begin(), equivalences.end(), eqclass);
      equivalences.erase(eptr);
      delete eqclass;
    }
  }
  
// #ifdef DEBUG
//   if(!verify())
//     throw ErrProgrammingError("Verification failed after mergeEquiv!",
// 			      __FILE__, __LINE__);
// #endif // DEBUG
}  // end HomogeneityTet::mergeEquiv (three arg version)

// This version of mergeEquiv is used when the classes are merged, but
// not the points.  In findFaceFacets, it's not necessary to create
// new merged points when coincidences are detected, but the
// equivalence classes have to be updated.

void HomogeneityTet::mergeEquiv(PlaneIntersection *pt0, PlaneIntersection *pt1)
{
  IsecEquivalenceClass *equivClass0 = pt0->equivalence();
  IsecEquivalenceClass *equivClass1 = pt1->equivalence();
  if(equivClass0 == nullptr) {
    if(equivClass1 == nullptr) {
      IsecEquivalenceClass *eqclass = new IsecEquivalenceClass(
					       this, pt0, nextEquivalenceID()
#ifdef DEBUG
					       , verbose
#endif // DEBUG
							       );
      equivalences.push_back(eqclass);
      pt0->setEquivalence(eqclass);
      pt1->setEquivalence(eqclass);
    }
    else {
      pt0->setEquivalence(equivClass1);
    }
  }
  else {
    if(equivClass1 == nullptr) {
      pt1->setEquivalence(equivClass0);
    }
    else if(equivClass0 != equivClass1) {
// #ifdef DEBUG
//       if(verboseplane)
// 	oofcerr << "HomogeneityTet::mergeEquiv(2): merging classes"
// 		<< std::endl;
// #endif // DEBUG
      equivClass0->merge(equivClass1);
      auto eptr = std::find(equivalences.begin(), equivalences.end(),
			    equivClass1);
      assert(eptr != equivalences.end());
      equivalences.erase(eptr);
      delete equivClass1;
    }
  }
} // end HomogeneityTet::mergeEquiv (two arg version)

// checkEquiv checks to see if the given intersection point belongs in
// any existing equivalence class, and puts it in it.  If the point
// already belongs to a class and is found to also belong to another,
// the classes are merged.
template <class PLANEINTERSECTION>
PLANEINTERSECTION *HomogeneityTet::checkEquiv(PLANEINTERSECTION *point) {
// #ifdef DEBUG
//   if(verboseplane || verboseface) 
//     oofcerr << "HomogeneityTet::checkEquiv: point=" << *point << std::endl;
//   OOFcerrIndent indent(2);
// #endif // DEBUG

  bool foundEquiv = true;
  while(foundEquiv == true) {
    foundEquiv = false;
    for(IsecEquivalenceClass *eqclass : equivalences) {
      if(point->equivalence() != eqclass) {
// #ifdef DEBUG
// 	if(verboseplane || verboseface)
// 	  oofcerr << "HomogeneityTet::checkEquiv: checking class " << *eqclass
// 		  << ", loc=" << eqclass->location3D() << std::endl;
// #endif // DEBUG
	if(point->belongsInEqClass(eqclass)) {
	  foundEquiv = true;
	  IsecEquivalenceClass *oldclass = point->equivalence();
// #ifdef DEBUG
// 	  if(verboseplane || verboseface)
// 	    oofcerr << "HomogeneityTet::checkEquiv: found eqclass "
// 		    << *eqclass << std::endl;
// #endif // DEBUG
	  if(oldclass != nullptr) {
	    // Since point is in oldclass, calling merge will call
	    // point->setEquivalence(eqclass).
// #ifdef DEBUG
// 	    if(verboseplane || verboseface)
// 	      oofcerr << "HomogeneityTet::checkEquiv: merging oldclass="
// 		      << *oldclass << std::endl;
// #endif // DEBUG
	    eqclass->merge(oldclass);
	    auto eptr = std::find(equivalences.begin(), equivalences.end(),
				  oldclass);
	    assert(eptr != equivalences.end());
	    equivalences.erase(eptr);
	    delete oldclass;
	  }
	  else {
	    point->setEquivalence(eqclass);
	  }
	  break;
	} // end if point belongs in another class
// #ifdef DEBUG
// 	else
// 	  if(verboseplane || verboseface)
// 	    oofcerr << "HomogeneityTet::checkEquiv: wrong class" << std::endl;
// #endif // DEBUG
      }
    } // end loop over equivalence classes eqclass
  }
  if(point->equivalence() == nullptr) {
    // The point doesn't belong to any existing equivalence class.
    // Create one, so that other points can be made equivalent to it.
    IsecEquivalenceClass *eqclass = new IsecEquivalenceClass(
					     this, point, nextEquivalenceID()
#ifdef DEBUG
					     , verboseplane || verboseface
#endif // DEBUG
							     );
// #ifdef DEBUG
//     if(verboseplane || verboseface)
//       oofcerr << "HomogeneityTet::checkEquiv: creating new class "
// 	      << eqclass->id << std::endl;
// #endif // DEBUG
    equivalences.push_back(eqclass);
    point->setEquivalence(eqclass);
// #ifdef DEBUG
//     if(verboseplane || verboseface)
//       oofcerr << "HomogeneityTet::checkEquiv: created new class=" << *eqclass
// 	      << std::endl;
// #endif // DEBUG
  }
// #ifdef DEBUG
//   if(verboseplane || verboseface)
//     oofcerr << "HomogeneityTet::checkEquiv: final point=" << *point
// 	    << std::endl;
// #endif // DEBUG
  return point;
} // end HomogeneityTet::checkEquiv

// Force template instantiation.  Most instances are generated
// automatically, but these are apparently only used elsewhere
// (facefacet.C and intersectiongroup.C) and not created unless we ask
// nicely here.

template TripleFaceIntersection*
HomogeneityTet::checkEquiv<TripleFaceIntersection>(TripleFaceIntersection*);
template GenericIntersection*
HomogeneityTet::checkEquiv<GenericIntersection>(GenericIntersection*);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

BarycentricCoord &HomogeneityTet::getBarycentricCoord(const Coord3D &pt) {
  {
    // See if this coordinate has already been computed.
    BaryCoordCache::iterator it = baryCache.find(pt);
    if(it != baryCache.end()) {
// #ifdef DEBUG
//       if(verboseplane)
// 	oofcerr << "HomogeneityTet::getBarycentricCoord: " << pt << " "
// 		<< (*it).second << " cached" << std::endl;
// #endif  // DEBUG
      return (*it).second;
    }
  }
  // Compute a new coordinate
  BarycentricCoord b(pt, epts);
  // If a face of the element is exactly on a pixel plane, and the
  // point is on that plane, make sure that the corresponding
  // barycentric coordinate is exactly zero.
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    const FacePixelPlane *pixplane = coincidentPixelPlanes[f];
    if(pixplane && pixplane->contains(pt)) {
      b[CSkeletonElement::oppNode[f]] = 0.0;
    }
  }

// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::getBarycentricCoord: " << pt << " " << b
// 	    << " computed" << std::endl;
// #endif // DEBUG

  // Insert the new barycentric coord into the cache, and return a
  // reference to it.
  std::pair<BaryCoordCache::iterator, bool> insert =
    baryCache.insert(std::pair<Coord3D, BarycentricCoord>(pt, b));
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::getBarycentricCoord: " << pt << " "
// 	    << (*insert.first).second << " new" << std::endl;
// #endif // DEBUG
  return (*insert.first).second;
}

BarycentricCoord &HomogeneityTet::getBarycentricCoord(const ICoord3D &ipt) {
  return getBarycentricCoord(ipt.coord());
}

BarycentricCoord &HomogeneityTet::getBarycentricCoord(
			      const ICoord2D &ipt, const HPixelPlane *pixplane)
{
  return getBarycentricCoord(pixplane->convert2Coord3D(ipt).coord());
}

// Given a SimpleIntersection, a polygon edge index, and the corners of
// the polygon, compute the parametric position of the intersection
// along the polygon edge.

// void HomogeneityTet::setIntersectionPolyFrac(SingleFaceBase *isec,
// 					     unsigned int edgeno,
// 					     const PixelPlaneFacet *facet)
//   const
// {
// // #ifdef DEBUG
// //   if(verboseplane) {
// //     oofcerr << "HomogeneityTet::setIntersectionPolyFrac: isec=" << *isec
// // 	    << std::endl;
// //   }
// // #endif // DEBUG  
//   unsigned int nextno = edgeno + 1;
//   if(nextno == facet->polygonSize())
//     nextno = 0;
//   BarycentricCoord b0 = facet->polygonCornerBary(edgeno);
//   BarycentricCoord b1 = facet->polygonCornerBary(nextno);
//   BarycentricCoord bint =
//     dynamic_cast<PixelPlaneIntersectionNR*>(isec)->baryCoord(this);
//   // alpha is the position of the intersection as a fractional
//   // distance from corner edgeno to edgeno+1.  It can be computed
//   // from bint = (1-alpha)*b0 + alpha*b1 where bint is the
//   // barycentric coord of the intersection and b0 and b1 are the
//   // barycentric coords of the corner points.  This holds for all
//   // components of b, but we have to use the ones in which b0 and
//   // b1 differ.

//   // Since roundoff error can make components of b0 and b1 differ when
//   // they should be the same, look at all the components and use the
//   // one with the biggest absolute difference.

//   unsigned int best = NONE;
//   double bigdiff = 0;
//   for(unsigned int i=0; i<4; i++) {
//     double bd = fabs(b0[i] - b1[i]);
//     if(bd > bigdiff) {
//       bigdiff = bd;
//       best = i;
//     }
//   }
// #ifdef DEBUG
//   if(best == NONE)
//     throw ErrProgrammingError("HomogeneityTet::setIntersectionPolyFrac failed!",
// 			      __FILE__, __LINE__);
// #endif // DEBUG
//   double alpha = (bint[best] - b0[best])/(b1[best] - b0[best]);
//   isec->setPolyFrac(alpha);
// }

// Given the barycentric coordinates of a point that is on the given
// face of the tet, find its fractional position along the polygon
// edge formed by the intersection of the face with the plane of the
// given facet.  The point is assumed to lie in both the face and the
// plane.

EdgePosition HomogeneityTet::edgeCoord(const BarycentricCoord &bint,
				       unsigned int edgeno,
				       const PixelPlaneFacet *facet)
  const
{
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::edgeCoord: bint=" << bint
// 	    << " edgeno=" << edgeno << " onFace=" << facet->onFace
// 	    << std::endl;
//   }
// #endif	// DEBUG

#ifdef DEBUG
  if(edgeno == NONE) {
    oofcerr << "HomogeneityTet::edgeCoord: edgeno==NONE! facet=" << *facet
	    << std::endl;
    throw ErrProgrammingError("HomogeneityTet::edgeCoord: bad edgeno!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG

  // If the pixelplane facet is on a tet face, then the polygon is the
  // whole tet face.  Use faceEdgeCoord to get the position, to be
  // compatible with the position computed on the adjacent face.
  if(facet->onFace != NONE) {
    return faceEdgeCoord(bint, facet->onFace, facet->getFaceEdgeIndex(edgeno));
  }
  
  unsigned int nextno = edgeno + 1;
  if(nextno == facet->polygonSize())
    nextno = 0;
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::edgeCoord: edgeno=" << edgeno
// 	    << " nextno=" << nextno << std::endl;
// #endif // DEBUG
  BarycentricCoord b0 = facet->polygonCornerBary(edgeno);
  BarycentricCoord b1 = facet->polygonCornerBary(nextno);
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::edgeCoord:"
// 	    << " b0=" << b0 << " " << *facet->getTetPoint(edgeno)->equivalence()
// 	    << " b1=" << b1 << " " << *facet->getTetPoint(nextno)->equivalence()
// 	    << std::endl;
// #endif // DEBUG
  
  // alpha is the position of the intersection as a fractional
  // distance from corner edgeno to edgeno+1.  It can be computed
  // from bint = (1-alpha)*b0 + alpha*b1 where bint is the
  // barycentric coord of the intersection and b0 and b1 are the
  // barycentric coords of the corner points.  This holds for all
  // components of b, but we have to use the ones in which b0 and
  // b1 differ.

  // Since roundoff error can make components of b0 and b1 differ when
  // they should be the same, look at all the components and use the
  // one with the biggest absolute difference.

  unsigned int best = NONE;
  double bigdiff = 0;
  for(unsigned int i=0; i<NUM_TET_NODES; i++) {
    double bd = fabs(b0[i] - b1[i]);
    if(bd > bigdiff) {
      bigdiff = bd;
      best = i;
    }
  }
#ifdef DEBUG
  if(best == NONE)
    throw ErrProgrammingError("HomogeneityTet::edgeCoord failed!",
			      __FILE__, __LINE__);
#endif // DEBUG

  double alpha = (bint[best] - b0[best])/(b1[best] - b0[best]);
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::edgeCoord: best=" << best
// 	    << " alpha=" << alpha << std::endl;
// #endif // DEBUG
  return EdgePosition(alpha, false);
}

// Return the fractional position of the given point along the given
// edge of the given tet face.
EdgePosition HomogeneityTet::faceEdgeCoord(const BarycentricCoord &bary,
					   unsigned int face, unsigned int edge)
  const
{
  // Get the nodes at the ends of the tet edge.
  unsigned int n0, n1;
// #ifdef DEBUG
//   if(verboseface || verboseplane)
//     oofcerr << "HomogeneityTet::faceEdgeCoord: calling getEdgeNodes, face="
// 	    << face << " edge=" << edge << std::endl;
// #endif // DEBUG
  getEdgeNodes(face, edge, n0, n1);
  // If bary is really on the edge between nodes n0 and n1, then
  // bary[n0] = 1-alpha and bary[n1] = alpha, where alpha is the
  // fractional position, so we could get alpha in two ways.  Average
  // them.

// #ifdef DEBUG
//   if(verboseplane || verboseface) {
//     double t0 = 0.5*(1 - bary[n0] + bary[n1]);
//     double t1 = 0.5*(1 - bary[n1] + bary[n0]);
//     if(t0 != 1-t1 || t1 != 1-t0) {
//       oofcerr << "HomogeneityTet::faceEdgeCoord: bary=" << bary
// 	      << " n0=" << n0 << " n1=" << n1 << std::endl;
//       oofcerr << "HomogeneityTet::faceEdgeCoord: t0=" << t0 << " t1=" << t1
// 	      << " 1-t0=" << (1-t0) << " 1-t1=" << (1-t1) << std::endl;
//       oofcerr << "HomogeneityTet::faceEdgeCoord: diff=" << ((1-t0) - t1)
// 	      << " " << ((1-t1) - t0) << std::endl;
//       throw ErrProgrammingError("Inconsistent HomogeneityTet::faceEdgeCoord",
// 				__FILE__, __LINE__);
//     }
//   }
// #endif // DEBUG

  // The canonical EdgePosition is calculated with n0 < n1.  If n0 >
  // n1, then compute the position for n0 < n1 and mark it as
  // reversed.  This avoids situations in which round off error can
  // reverse the apparent order of points when viewed from a different
  // face.
  if(n0 <  n1)
    return EdgePosition(0.5*(1. - bary[n0] + bary[n1]), false);
  return EdgePosition(0.5*(1. - bary[n1] + bary[n0]), true);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the points at which the edges of the tetrahedron intersect the
// given pixel plane.

TetIntersectionPolygon&
HomogeneityTet::getTetPlaneIntersectionPoints(const HPixelPlane *pixplane) {
// #ifdef DEBUG
//   if(verboseCategory())
//     oofcerr << "HomogeneityTet::getTetPlaneIntersectionPoints: pixplane="
// 	    << pixplane << " " << *pixplane << std::endl;
// #endif // DEBUG
  {
    // Return cached points if possible.
    TetPlaneIsecMap::iterator i = tetPlaneIntersections.find(pixplane);
    if(i != tetPlaneIntersections.end()) {
// #ifdef DEBUG
//       if(verboseplane)
// 	oofcerr << "HomogeneityTet::getTetPlaneIntersectionPoints: "
// 		<< "returning cached values for " << *pixplane << std::endl;
// #endif // DEBUG
      return (*i).second;
    }
  }
  
  // overnodes holds the indices of the tet nodes that are above the
  // plane, ie in the direction of the outward normal of the voxel
  // set.  undernodes are the nodes that are below the plane.  If
  // there are no undernodes, then the tet can't intersect the voxel
  // group at this plane.
  std::vector<unsigned int> overnodes;
  std::vector<unsigned int> undernodes;
  std::vector<unsigned int> inplanenodes;
  for(unsigned int k=0; k<NUM_TET_NODES; ++k) {
    double h = ((epts[k][pixplane->direction()] - pixplane->normalOffset())
		* pixplane->normalSign());
    if(h == 0) {
      inplanenodes.push_back(k);
    } 
    else if(h > 0) {
      overnodes.push_back(k);
    }
    else if(h < 0) {
      undernodes.push_back(k);
    }
  } // end loop over tet nodes k

  tetPlaneIntersections[pixplane] = TetIntersectionPolygon();
  TetIntersectionPolygon &result = tetPlaneIntersections[pixplane];

  // If undernodes.size() is 0 or 4 then there is no significant
  // intersection.
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::getTetPlaneIntersectionPoints: pixplane="
// 	    << *pixplane;
//     std::cerr << " overnodes=[" << overnodes << "] inplanenodes=["
// 	      << inplanenodes << "] undernodes=[" << undernodes << "]";
//     oofcerr << std::endl;
//   }
// #endif // DEBUG

  if(undernodes.size() == 1) {
    // One tet node is under the plane and the other three are on or
    // above it.  All three edges that meet at the node must end on or
    // intersect the plane. 
    result.reserve(3);
    unsigned int n = undernodes[0];
    for(unsigned int i=0; i<3; i++) {
      unsigned int edge = CSkeletonElement::cwNodeEdges[n][i];
      FacePlane *face0 = faces[CSkeletonElement::edgeFaces[edge][0]];
      FacePlane *face1 = faces[CSkeletonElement::edgeFaces[edge][1]];
      result.push_back(checkEquiv(new TetEdgeIntersection(
					  this, face0, face1, pixplane)));
#ifdef DEBUG
      result.back()->verbose = verboseplane;
#endif // DEBUG
    }
  }
  else if(undernodes.size() == 2) {
    // There are two nodes underneath the pixel plane.  If the other
    // two nodes are both above the plane, there are four intersection
    // points.  If both are on the plane, the intersection has no area
    // and can be ignored.  If one is on the plane and one is above
    // it, there are three intersection points.
    unsigned int underedge =
      CSkeletonElement::nodeNodeEdge[undernodes[0]][undernodes[1]];
    if(overnodes.size() == 2) {
      // Two nodes are on each side of the plane, so there are four
      // intersection points.  The correct order is given by
      // CSkeletonElement::cwNeighborEdgeOrder.  (It's cw, instead of
      // ccw, because we're looking at the plane from below.)
      result.reserve(4);
      for(unsigned int i=0; i<4; i++) {
	// "edge" is the edge between one of the undernodes and one of
	// the other nodes.
	unsigned int edge =
	  CSkeletonElement::cwNeighborEdgeOrder[underedge][i];
	FacePlane *face0 = faces[CSkeletonElement::edgeFaces[edge][0]];
	FacePlane *face1 = faces[CSkeletonElement::edgeFaces[edge][1]];	
	result.push_back(checkEquiv(new TetEdgeIntersection(
					    this, face0, face1, pixplane)));
#ifdef DEBUG
	result.back()->verbose = verboseplane;
#endif // DEBUG
      }
    } // end if overnodes.size() == 2
    else if(overnodes.size() == 1) {
      assert(inplanenodes.size() == 1);
      unsigned int inplanenode = inplanenodes[0];
      // Loop over the 4 edges that connect to underedge.
      bool didinplane = false;
      for(unsigned int i=0; i<4; i++) {
	unsigned int edge = CSkeletonElement::cwNeighborEdgeOrder[underedge][i];
	// Urgh.  vtk uses signed ints here.
	int *edgenodes = vtkTetra::GetEdgeArray(edge);
	if(edgenodes[0] == (int) inplanenode ||
	   edgenodes[1] == (int) inplanenode)
	  {
	    if(!didinplane) {
	      result.push_back(checkEquiv(new TetNodeIntersection(
					  this, pixplane, inplanenode)));
	      didinplane = true;
	    }
	  }
	else {
	  FacePlane *face0 = faces[CSkeletonElement::edgeFaces[edge][0]];
	  FacePlane *face1 = faces[CSkeletonElement::edgeFaces[edge][1]];
	  result.push_back(checkEquiv(new TetEdgeIntersection(
					      this, face0, face1, pixplane)));
#ifdef DEBUG
	  result.back()->verbose = verboseplane;
#endif // DEBUG
	}
      }	// end loop over underedge neighbor edges i
    }	// end if overnodes.size() == 1
  } // end if undernodes.size() == 2
  else if(undernodes.size() == 3) {
    // A tet with three nodes under the plane forms a meaningful
    // intersection only if the fourth point is above the plane.  If
    // it's on the plane, then the intersection is only a point and
    // can be ignored.
    if(overnodes.size() == 1) {
      result.reserve(3);
      unsigned int n = overnodes[0];
      for(unsigned int i=0; i<3; i++) {
	unsigned int edge = CSkeletonElement::ccwNodeEdges[n][i];
	FacePlane *face0 = faces[CSkeletonElement::edgeFaces[edge][0]];
	FacePlane *face1 = faces[CSkeletonElement::edgeFaces[edge][1]];
	result.push_back(checkEquiv(new TetEdgeIntersection(
					    this, face0, face1, pixplane)));
#ifdef DEBUG
	result.back()->verbose = verboseplane;
#endif // DEBUG
      }
    }
  } // end if undernodes.size() == 3

  return result;
} // HomogeneityTet::getTetPlaneIntersectionPoints

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility functions used by doFindPixelPlaneFacets

// Given the corners of a convex polygon, find an interior point whose
// coordinates are not integers.  This is used to generate input for
// PixelBdyLoop::contains(), which is more efficient if it knows that
// its input can't coincide with a corner of a loop (and all of its
// corners are at integer coordinates).

static bool isIntCoord(const Coord2D &c) {
  return (c[0] == floor(c[0]) || c[1] == floor(c[1]));
}

static Coord2D nonIntegerInteriorPt(const TetIntersectionPolygon &poly,
				    const HPixelPlane *pixplane)
{
  Coord2D trialPt;
  // Use the center of the polygon for the first trial point.
  for(const PlaneIntersection *pt : poly) {
    trialPt += pt->location2D(pixplane);
  }
  trialPt /= poly.size();
  if(!isIntCoord(trialPt))
    return trialPt;
  // We will almost never get past this point so it doesn't matter how
  // ugly the code is.  The scheme here is to construct a new trial
  // point that's on the line between the current trial point and a
  // corner.  Because the polygon is convex, that point is guaranteed
  // to also be interior.  If that fails, move towards the next
  // corner.  The fractional distance of the move is decreased on each
  // step, in case the original distances are integers.
  double fact = 1049./2048.;
  double frac = 0.51;
  for(const PlaneIntersection *pt : poly) {
    // Create another interior point near corner pt.
    trialPt = (1-frac)*pt->location2D(pixplane) + frac*trialPt;
    if(!isIntCoord(trialPt))
      return trialPt;
    // The point still has integer coordindates.  Reduce the
    // fractional distance by something unlikely to land on another
    // integer point.
    frac *= fact;
  }
  // This really can't happen unless the polygon is degenerate, in
  // which case we should never have reached this point.
  oofcerr << "nonIntegerInteriorPt: failed! pixplane=" << *pixplane << " poly=";
  std::cerr << derefprint(poly);
  oofcerr << std::endl;
  throw ErrProgrammingError("nonIntegerInteriorPt failed!", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FacetMap2D HomogeneityTet::findPixelPlaneFacets(unsigned int cat,
						const VoxelSetBoundary &vsb)
{
#ifdef DEBUG
  verbosecategory = verboseCategory_(verbose, cat);
#endif // DEBUG
  FacetMap2D facets;		// typedef in pixelplanefacet_i.h

  const PixelSetBoundaryMap &pxlSetBdys = vsb.getPixelSetBdys();

  // We have to examine each pixel plane that has loops in the VSB,
  // and also the pixel planes that contain faces of the tet, whether
  // or not they have loops in the VSB.  So first examine the faces,
  // and remember which ones have been examined, so they're not
  // examined twice.
  std::set<const HPixelPlane*> didPlane;
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    const FacePixelPlane *pixplane = coincidentPixelPlanes[f];
    if(pixplane != NULL) {
#ifdef DEBUG
      verboseplane = verbosePlane_(verbosecategory, pixplane);
#endif  // DEBUG
      didPlane.insert(pixplane);
      const std::vector<PixelBdyLoop*> &csloops = vsb.getPlaneCS(*pixplane,
								 cat
#ifdef DEBUG
							       , verboseplane
#endif // DEBUG
								 );
      std::vector<PixelBdyLoop*> loops(csloops);
      PixelSetBoundaryMap::const_iterator psbmi = pxlSetBdys.find(*pixplane);
      if(psbmi != pxlSetBdys.end()) {
	const std::vector<PixelBdyLoop*> &floops = (*psbmi).second->get_loops();
	loops.insert(loops.end(), floops.begin(), floops.end());
      }
// #ifdef DEBUG
//       if(verboseplane)
// 	oofcerr << "HomogeneityTet::findPixelPlaneFacets: "
// 		<< "calling doFindPixelPlaneFacets with CS data, f=" << f
// 		<< std::endl;
// #endif // DEBUG
      doFindPixelPlaneFacets(cat, pixplane, loops, f, facets);
// #ifdef DEBUG
// 	if(verboseplane)
// 	  oofcerr << "HomogeneityTet::findPixelPlaneFacets: back from doFindPixelPlaneFacets" << std::endl;
// #endif // DEBUG
#ifdef DEBUG
      verboseplane = false;
#endif  // DEBUG
    }
  }
// #ifdef DEBUG
//   if(verbosecategory) {
//     oofcerr << "HomogeneityTet::findPixelPlaneFacets: done with face planes"
// 	    << std::endl;
//   }
// #endif // DEBUG

  for(PixelSetBoundaryMap::const_iterator psbm=pxlSetBdys.begin();
      psbm!=pxlSetBdys.end(); ++psbm)
    {
      const PixelPlane &pp = (*psbm).first;
      // The PixelPlane that's used in the PixelSetBoundaryMap is a
      // different object than the one that the HomogeneityTet may be
      // tracking.  Get (or create) the tracked PixelPlane.  Also,
      // it's an HPixelPlane, not a PixelPlane.
      const HPixelPlane *pixplane = getPixelPlane(pp.direction(),
						  pp.normalOffset(),
						  pp.normalSign());
#ifdef DEBUG
      verboseplane = verbosePlane_(verbosecategory, pixplane);
#endif  // DEBUG
      if(didPlane.count(pixplane) == 0) {
	const PixelSetBoundary *psb = (*psbm).second;
	const std::vector<PixelBdyLoop*> loops = psb->get_loops();
// #ifdef DEBUG
// 	if(verboseplane)
// 	  oofcerr << "HomogeneityTet::findPixelPlaneFacets: "
// 		  << "calling doFindPixelPlaneFacets with facet data"
// 		  << std::endl;
// #endif // DEBUG
	doFindPixelPlaneFacets(cat, pixplane, loops, /*face=*/NONE, facets);
// #ifdef DEBUG
// 	if(verboseplane)
// 	  oofcerr << "HomogeneityTet::findPixelPlaneFacets: back from doFindPixelPlaneFacets" << std::endl;
// #endif // DEBUG
      }
#ifdef DEBUG
      verboseplane = false;
#endif // DEBUG
    } // end loop over PixelSetBoundaryMap
  return facets;
} // end HomogeneityTet::findPixelPlaneFacets


#define MIN_POLYGON_AREA 1.e-10

void HomogeneityTet::doFindPixelPlaneFacets(
				    unsigned int cat,
				    const HPixelPlane *pixplane,
				    const std::vector<PixelBdyLoop*> &loops,
				    unsigned int onFace,
				    FacetMap2D &facets)
{
  // TODO: Check bounding box for intersection before doing anything
  // else.
#ifdef DEBUG
  if(verboseplane) {
    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: cat=" << cat
	    << " pixplane=" << *pixplane << " onFace=" << onFace << std::endl;
  }
#endif // DEBUG
  
  TetIntersectionPolygon &tetPts = getTetPlaneIntersectionPoints(pixplane);
  unsigned int nn = tetPts.size();

  if(nn < 3) {
// #ifdef DEBUG
//     if(verboseplane) 
//       oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: no intersection! nn="
// 	      << nn << " pixplane=" << *pixplane << std::endl;
// #endif // DEBUG
    return;
  }
  assert(nn == 3 || nn == 4);

#ifdef DEBUG
  if(verboseplane) {
    if(!tetPts.empty()) {
      // oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
      // 	      << "initial equivalence classes:" << std::endl;
      // dumpEquivalences();
      // oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: tetPts="
      // 	      << std::endl;
      // for(const TetIntersection *pt : tetPts)
      // 	oofcerr << "HomogeneityTet::doFindPixelPlaneFacets:    " << *pt
      // 		<< std::endl;
      std::string filename = "tetpts-" + pixplane->shortName() + ".lines";
      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
	      << " writing " << filename << std::endl;
      std::ofstream tetpts(filename);
      for(unsigned int i=0; i<tetPts.size(); i++) {
	unsigned int j = (i == tetPts.size()-1 ? 0 : i+1);
	tetpts << tetPts[i]->location3D() << ", " << tetPts[j]->location3D()
	       << std::endl;
      }
      tetpts.close();
    }
  }
  OOFcerrIndent indent(2);
#endif // DEBUG

  // The tet intersects the plane.  There might be an intersection
  // with the voxel set boundary, so create a new PixelPlaneFacet
  // object to store it.
  // PixelPlaneFacets are deleted by
  // CSkeletonElement::categoryVolumes, which owns the FacetMap2D
  // object (facets).
  PixelPlaneFacet *facet = new PixelPlaneFacet(this, pixplane, tetPts, onFace
#ifdef DEBUG
					       , verboseplane
#endif // DEBUG
					       );
  facets[pixplane] = facet;

//   // Check that the area is greater than a certain minimum.
//   Coord2D polyCenter;
//   for(unsigned int i=0; i<nn; i++) {
//     polyCenter += tetPts[i]->location2D(pixplane);
//   }
//   polyCenter /= tetPts.size();
//   double polyArea = 0;		// really twice the area
//   for(unsigned int i=0; i<nn; i++) {
//     polyArea += ((tetPts[i]->location2D(pixplane) - polyCenter) %
// 		 (tetPts[(i+1)%nn]->location2D(pixplane) - polyCenter));
//   }
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: polyArea=" << polyArea
// 	    << std::endl;
// #endif	// DEBUG
//   if(polyArea < MIN_POLYGON_AREA)
//     return;

  // Find the bounding box of the tet intersection points.
  CRectangle tetBounds(tetPts[0]->location2D(pixplane),
		       tetPts[1]->location2D(pixplane));
  tetBounds.swallow(tetPts[2]->location2D(pixplane));
  if(nn == 4)
    tetBounds.swallow(tetPts[3]->location2D(pixplane));

  // For each loop in the PixelSetBoundary, find its intersection with
  // the polygon formed by tetPts.

  for(std::vector<PixelBdyLoop*>::const_iterator pbl=loops.begin();
      pbl!=loops.end(); ++pbl)
    {
      const PixelBdyLoop *loop = *pbl;
      // Skip this bdy loop if its bounding box doesn't intersect the
      // polygon's bounding box.  
      if(!tetBounds.intersects(loop->bbox())) {
// #ifdef DEBUG
// 	if(verboseplane) {
// 	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets:"
// 		  << " bounding boxes don't intersect, skipping loop"
// 		  << std::endl;
// 	  OOFcerrIndent indent(2);
// 	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: loop bbox="
// 		  << loop->bbox() << std::endl;
// 	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: tet bbox="
// 		  << tetBounds << std::endl;
// 	  if(tetBounds.xmin() > loop->bbox().xmax())
// 	    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: deltaX="
// 		    << tetBounds.xmin() - loop->bbox().xmax() << std::endl;
// 	  if(loop->bbox().xmin() > tetBounds.xmax())
// 	    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: deltaX="
// 		    << loop->bbox().xmin() - tetBounds.xmax() << std::endl;
// 	  if(tetBounds.ymin() > loop->bbox().ymax())
// 	    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: deltaY="
// 		    << tetBounds.ymin() - loop->bbox().ymax() << std::endl;
// 	  if(loop->bbox().ymin() > tetBounds.ymax())
// 	    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: deltaY="
// 		    << loop->bbox().ymin() - tetBounds.ymax() << std::endl;
// 	}
// #endif // DEBUG
	continue;
      }
#ifdef DEBUG
      if(verboseplane)
        oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: examining loop "
		<< *loop << std::endl;
#endif // DEBUG

      // Find the interiority of the start of the first pixel boundary
      // segment.  End-point interiorities are done on the fly in the
      // k loop.  Start point interiorities for every point after the
      // first are the same as the end point interiority of the
      // previous point.
      BarycentricCoord pbs_start_bary = getBarycentricCoord(loop->icoord(0),
							    pixplane);
      bool pbs_start_inside = pbs_start_bary.interior(onFace);
      unsigned int loopsize = loop->size();
      // Loop over segments of the boundary loop
      for(unsigned int k=0; k<loopsize; k++) {
	ICoord2D pbs_start = loop->icoord(k); // start of this segment
	ICoord2D pbs_end = loop->next_icoord(k); // end of this segment
	ICoord2D pbs_prev = loop->prev_icoord(k); // start of previous segment
	ICoord2D pbs_next = loop->next2_icoord(k); // end of next segment
	BarycentricCoord pbs_end_bary = getBarycentricCoord(pbs_end, pixplane);
	bool pbs_end_inside = pbs_end_bary.interior(onFace);

#ifdef DEBUG
	if(verboseplane) {
	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: examining bdy loop segment "
		  << k << " " << std::endl;
	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: start= "
		  << pbs_start << " "
		  << pixplane->convert2Coord3D(pbs_start) << " "
		  << pbs_start_bary
		  << " ("
		  << (pbs_start_inside ? "interior" : "exterior") << ")"
		  << std::endl;
	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets:   end=" 
		  << pbs_end << " "
		  << pixplane->convert2Coord3D(pbs_end) << " "
		  << pbs_end_bary
		  << " ("
		  << (pbs_end_inside ? "interior" : "exterior") << ")"
		  << std::endl;

	}
	OOFcerrIndent indnt(2);
#endif // DEBUG

	// Does the loop segment cross the polygon?
	if(pbs_start_inside && pbs_end_inside) {

	  // The pixel boundary segment is completely interior.  (We
	  // know this because the endpoints are inside and the
	  // polygon is convex.)  The endpoints are at the
	  // intersections of the current pixel plane, the orthogonal
	  // pixel plane(s) that contains the segment, and the orthogonal
	  // plane that contains the previous segment or the next one.

	  // Orthogonal plane at the start of the segment, containing
	  // the seg (or at least its start).
	  const HPixelPlane *orthoPlane0 =
	    orientedOrthogonalPlane(cat, pixplane, loop->segment(k), true);
	  // Orthogonal plane at the end of the segment, containing the seg.
	  const HPixelPlane *orthoPlane1 =
	    orientedOrthogonalPlane(cat, pixplane, loop->segment(k), false);
	  // Orthogonal plane perpendicular to the start of the segment.
	  const HPixelPlane *prevPlane =
	    orientedOrthogonalPlane(cat, pixplane, loop->segment(k).prev(),
				    false);
	  // Orthogonal plane perpendicular to the end of the segment.
	  const HPixelPlane *nextPlane =
	    orientedOrthogonalPlane(cat, pixplane, loop->segment(k).next(),
				    true);
	  facet->addEdge(new PixelFacetEdge(
	    checkEquiv(new TriplePixelPlaneIntersection(
				this, pixplane, orthoPlane0, prevPlane)),
	    checkEquiv(new TriplePixelPlaneIntersection(
				this, pixplane, orthoPlane1, nextPlane))));
	} // end if the segment is entirely inside the polygon

	else if(pbs_start_inside != pbs_end_inside) {
	  // If start and end are hetero-interior, so to speak, then
	  // there's one intersection. Find it.
	  PixelPlaneIntersectionNR *pi = find_one_intersection(
	       cat, facet, pixplane, loop->segment(k), onFace, pbs_end_inside);
	  // Find the intersection at the other end of the segment.
	  // It must be a TriplePixelPlaneIntersection.
	  if(pbs_start_inside) {
	    // The segment starts inside the tet.  The planes are
	    // pixplane, the orthogonal plane containing the given
	    // segment (at the start of the segment), and the plane
	    // containing the previous segment in the loop (at the end
	    // of the segment).  Start and end are important to get
	    // the correct orientation of the planes.
	    const HPixelPlane *orthoPlane =
	      orientedOrthogonalPlane(cat, pixplane, loop->segment(k), true);
	    const HPixelPlane *thirdPlane =
	      orientedOrthogonalPlane(cat, pixplane, loop->segment(k).prev(),
				      false);
	    //   pixplane->orthogonalPlane(pbs_prev, pbs_start);
	    // const HPixelPlane *prevPlanePtr = getPixelPlane(orthoPlanePrev);
	    facet->addEdge(new StopFaceIntersectionEdge(
		checkEquiv(new TriplePixelPlaneIntersection(
			    this, pixplane, orthoPlane, thirdPlane)),
		checkEquiv(pi)));
	  }
	  else {
	    // The segment ends inside the tet.
	    const HPixelPlane *orthoPlane =
	      orientedOrthogonalPlane(cat, pixplane, loop->segment(k), false);
	    const HPixelPlane *thirdPlane =
	      orientedOrthogonalPlane(cat, pixplane, loop->segment(k).next(),
				      true);
	    facet->addEdge(new StartFaceIntersectionEdge(
		 checkEquiv(pi),
		 checkEquiv(new TriplePixelPlaneIntersection(
			 this, pixplane, orthoPlane, thirdPlane))));
	  }
	} // end if start and end are hetero-interior
	else {
	  // The current segment has both endpoints outside the
	  // polygon.  It must intersect zero or two times.

	  // First check the bounding box in the plane.  Use
	  // intersects_open, which does not count intersections that
	  // include only boundary points, to be consistent with
	  // getTetPlaneIntersectionPoints and
	  // BarycentricCoord::interior.

	  // BUT BarycentricCoord::interior *does* include boundary
	  // points when looking at points known to be on a tet face!
	  
	  ICRectangle segbb(pbs_start, pbs_end);
	  if(segbb.intersects_open(tetBounds)) {
// #ifdef DEBUG
// 	    if(verboseplane) {
// 	      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
// 		      << " segbb=" << segbb << " tetBounds=" << tetBounds
// 		      << std::endl;
// 	      double dx0 = segbb.xmax() - tetBounds.xmin();
// 	      double dx1 = tetBounds.xmax() - segbb.xmin();
// 	      double dx = (dx0 > dx1 ? dx1 : dx0);
// 	      double dy0 = segbb.ymax() - tetBounds.ymin();
// 	      double dy1 = tetBounds.ymax() - segbb.ymin();
// 	      double dy = (dy0 > dy1 ? dy1 : dy0);
// 	      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: overlap="
// 		      << "(" << dx << ", " << dy << ")" << std::endl;
// 	    }
// #endif // DEBUG
	    const HPixelPlane *orthoPlane =
	      getPixelPlane(pixplane->orthogonalPlane(pbs_start, pbs_end));
	    // There's no intersection unless the orthoPlane actually
	    // intersects the tetrahedron.  This check is important
	    // for consistency.  When a pixel plane coincides with a
	    // face, sometimes find_two_intersections will find
	    // intersections when getTetPlaneIntersectionPoints
	    // doesn't, and this can lead to unmatched facet edge
	    // endpoints.
	    TetIntersectionPolygon orthoPts =
	      getTetPlaneIntersectionPoints(orthoPlane);
// #ifdef DEBUG
// 	    if(verboseplane) {
// 	      oofcerr << "HomogeneityTet:doFindPixelPlaneFacets: orthoPlane="
// 		      << *orthoPlane << " orthoPts=";
// 	      std::cerr << derefprint(orthoPts);
// 	      oofcerr << std::endl;
// 	    }
// #endif // DEBUG
	    if(!orthoPts.empty()) {
	      unsigned int orthoFace = getCoincidentFaceIndex(orthoPlane);
	      std::vector<PixelPlaneIntersectionNR*> isecs =
		find_two_intersections(cat, facet, pixplane, orthoPlane,
				       loop->segment(k), onFace, orthoFace);
	      if(isecs.size() == 2) {
		facet->addEdge(new TwoFaceIntersectionEdge(
				   checkEquiv(isecs[0]), checkEquiv(isecs[1])));
	      }
	    } // end if the orthogonal plane intersects the tet
// #ifdef DEBUG
// 	    else {
// 	      if(verboseplane) {
// 		oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
// 			<< "skipping find_two_intersections" << std::endl;
// 	      }
// 	    }
// #endif // DEBUG

	  } // end if segment bbox intersects polygon bbox
	} // end if both segment endpoints are outside the polygon

	pbs_start_inside = pbs_end_inside;
	pbs_start_bary = pbs_end_bary;

// #ifdef DEBUG
// 	if(!verify()) {
// 	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
// 		  << "verification failed!" << std::endl;
// 	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
// 		  << "facet=" << *facet << std::endl;
// 	  throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
// 	}
// #endif // DEBUG
      }	// end loop over boundary loop segments k

    } // end loop over PixelBdyLoops pbl

  // The facet contains a bunch of edges which may not yet form loops.
  // The loops need to be closed along the exterior of the polygon.
  if(!facet->completeLoops()) {
#ifdef DEBUG
    if(verboseplane) {
      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: completeLoops failed, ignoring facet."
	      << std::endl;
    }
#endif // DEBUG
    // The intersection points aren't sensible.  The facet must
    // be small and dominated by round-off error.  Ignore it.
    facet->clear();
    return;
  }

// #ifdef DEBUG
//   if(!verify()) {
//     oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
// 	    << "verification failed after completeLoops!" << std::endl;
//     oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
// 	    << "facet=" << *facet << std::endl;
//     throw ErrProgrammingError("Verification failed after completeLoops!",
// 			      __FILE__, __LINE__);
//   }
// #endif // DEBUG

// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: back from completeLoops"
// 	    << std::endl;
// #endif // DEBUG

  double facetarea = facet->area();
#ifdef DEBUG
  if(verboseplane) {
    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: completed loops, area="
	    << facetarea << std::endl;
    if(facetarea <= 0)
      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: non-positive area!"
	      << " facet=" << *facet << std::endl;
  }
#endif // DEBUG
  if(facetarea <= 0.0) {
    // There are no intersections.  We either need to include all of
    // the tetPts polygon, or none if it.
    //
    // If the polygon encloses a loop of the voxel set boundary, the
    // voxel boundary edges will already have been included in the
    // intersection facet, and we don't have to do anything.  The area
    // of the facet computed from the current set of edges is
    // positive.
    //
    // If the polygon is entirely inside a loop, but there are
    // holes within the polygon (ie, the boundary the voxel set
    // lying in this plane is annular and the polygon edges lie
    // within the annulus and surround the hole), then the entire
    // boundary must be included.  The area computed so far will
    // be *negative*, because it's made up of holes.
    //
    // If the polygon is entirely inside a boundary loop and there
    // are no holes in the pixel set within the polygon, the
    // polygon is homogeneous and its entire boundary is the
    // entire intersection boundary.
    //
    // A big difference between this code and the categoryAreas
    // calculation in 2D is that it's possible for the polygon
    // here to be homogeneous and lie within the voxel category
    // but *not* delimit a boundary facet of the intersection
    // volume.
    bool homogeneous = false;
    if(facetarea == 0) {
      // If any interior point of the polygon is inside the voxel
      // category, the whole polygon must be inside the loop, and is
      // homogeneous.  To determine if a point is inside the category,
      // compute the winding number of the category's loops around a
      // point that's inside the polygon.
      
      // NOTE: The polygon can be homogeneous and inside the voxel
      // category, but not be inside a facet loop.  In this case it's
      // *not* a facet of the intersection volume and should not be
      // included, unless it's also a face of the tetrahedron.  That's
      // why when a tet face is in the plane we use the loops bounding
      // the voxel set cross section, not the voxel set facets.

      // The winding number calculation is easier if the interior
      // point is known not to coincide with any loop components.  The
      // loop segments are orthogonal and lined up on integer
      // coordinates, so pick a non-integer interior point.
      Coord2D testPt = nonIntegerInteriorPt(tetPts, pixplane);
      int windingNumber = 0;
      for(PixelBdyLoop *loop : loops) {
	windingNumber += loop->windingNumber(testPt);
      }
      homogeneous = windingNumber == 1;
    }
    if(homogeneous || facetarea < 0.0) {
#ifdef DEBUG
      if(verboseplane)
	oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
		<< "adding entire perimeter, pixplane=" << *pixplane
		<< std::endl;
#endif // DEBUG
      for(unsigned int i=0; i<nn-1; i++) {
	facet->addEdge(new PolygonEdge(tetPts[i]->clone(this),
	 			       tetPts[i+1]->clone(this)));
      }
      facet->addEdge(new PolygonEdge(tetPts.back()->clone(this),
				     tetPts[0]->clone(this)));
    }
  } // end if facetarea <= 0

#ifdef DEBUG
  if(verboseplane) {
    if(!facet->empty()) {
      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: cat=" << cat
      	      << " pixel plane=" << *pixplane
      	      << " final facet= " << *facet << std::endl;
      facet->dump(cat);
    }
    // else
    //   oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: cat=" << cat
    // 	      << " pixel plane=" << *pixplane
    // 	      << " final facet is empty"
    // 	      << std::endl;
  }
  // if(!verify()) {
  //   oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: cat=" << cat
  // 	    << " pixel plane=" << *pixplane
  // 	    << " verification failed!" << std::endl;
  //   throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
  // }
#endif	// DEBUG
} // end HomogeneityTet::doFindPixelPlaneFacets

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the intersection of a pixel boundary loop segment with the
// tetrahedron, given a segment that's known to have just one endpoint
// inside the tet.  The only question is which face of the tet is
// crossed by the segment.  The segment is on the intersection of
// pixplane and orthoPlane.

PixelPlaneIntersectionNR *HomogeneityTet::find_one_intersection(
					unsigned int cat,
					const PixelPlaneFacet *facet,
					const HPixelPlane *pixplane,
					const PixelBdyLoopSegment &pbls,
					unsigned int onFace,
					bool entry)
{
  // Calculate the position of the intersection in a way that's
  // independent of the direction of the segment.
  ICoord2D interiorPt = entry ? pbls.secondPt() : pbls.firstPt();
  ICoord2D exteriorPt = entry ? pbls.firstPt() : pbls.secondPt();
  // Examining the barycentric coordinates of the points tells us
  // immediately which face the segment crosses.
  BarycentricCoord interiorB = getBarycentricCoord(interiorPt, pixplane);
  BarycentricCoord exteriorB = getBarycentricCoord(exteriorPt, pixplane);
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::find_one_intersection: interiorPt="
// 	    << interiorPt << " " << pixplane->convert2Coord3D(interiorPt)
// 	    << " " << interiorB << std::endl;
//     oofcerr << "HomogeneityTet::find_one_intersection: exteriorPt="
// 	    << exteriorPt << " " << pixplane->convert2Coord3D(exteriorPt)
// 	    << " " << exteriorB << std::endl;
//   }
// #endif // DEBUG

  // Look at each face to see which face planes the segment crosses.
  // If it crosses more than one, the one closest to the interior
  // point of the PixelBdyLoopSegment is the real intersection.
  double bestAlpha = std::numeric_limits<double>::max();
  unsigned int bestFace = NONE;
  const FacePlane *collinearFace = nullptr;
  // tempOrthoPlane is perpendicular to pixplane and contains the segment.
  // At this point it doesn't necessarily have the correct
  // orientation.
  const HPixelPlane *tempOrthoPlane = getPixelPlane(
			     pixplane->orthogonalPlane(interiorPt, exteriorPt));
  unsigned int orthoFace = getCoincidentFaceIndex(tempOrthoPlane);

  for(const FacePlane *face : facet->getBoundingFaces()) {
    // Skip this face if it lies in the orthogonal plane of the segment or is
    // collinear with it.
    if(orthoFace != face->face()) {
      if(!areCollinear(pixplane, tempOrthoPlane, face)) {
	unsigned int n = CSkeletonElement::oppNode[face->face()];
	if(interiorB[n] > 0.0 && exteriorB[n] <= 0.0) {
	  // alpha is the fractional distance from interiorPt to exteriorPt.
	  double alpha = interiorB[n]/(interiorB[n] - exteriorB[n]);
	  if(alpha < bestAlpha) {
	    bestAlpha = alpha;
	    bestFace = face->face();
	  }
	}
      }
      else {
	// If a face is collinear with the orthogonal plane, we may
	// need to use it below in case we don't find an intersecting
	// face.  There can be only one collinear face, so this is it.
	collinearFace = face;
      }
    }
  }

  if(bestFace == NONE) {
    // No face crosses the segment.  The segment must lie along a face
    // (ie, pixplane and tempOrthoPlane are collinear with at least one
    // tet face), and roundoff error has put one end of the segment
    // inside and one outside.  The intersection point can be chosen
    // to lie at any point on the segment, unless the segment extends
    // past the rim of the tet face.  Choose interiorPt because it
    // can't be past the rim.
    bestAlpha = 0;
  }
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::find_one_intersection: pixplane=" << *pixplane
// 	    << " tempOrthoPlane=" << *tempOrthoPlane << " face=" << bestFace
// 	    << std::endl;
//   }
// #endif // DEBUG

  // Now that we know the intersection point, we can find the actual
  // orientation of the orthogonal plane.  It depends on whether the
  // segment is along a ridge or valley of the surface of the category
  // volume.
  double realAlpha = entry ? 1-bestAlpha : bestAlpha;
  const HPixelPlane *orthoPlane = orientedOrthogonalPlane(cat, pixplane, pbls,
							 realAlpha);
						    
  // newIntersection returns either a SimpleIntersection or a
  // MultiFaceIntersection, depending on whether or not orthoPlane is
  // also a tet face.
  PixelPlaneIntersectionNR *ppi =
    newIntersection(this, pixplane, orthoPlane, pbls,
		    realAlpha, bestFace,
		    entry ? ENTRY : EXIT);

  if(bestFace == NONE) {
    // Do the things that the SimpleIntersection or
    // MultiFaceIntersection constructor couldn't do because it was
    // called with faceIndex==NONE.
    ICoord3D loc = pixplane->convert2Coord3D(interiorPt);
    ppi->setLocation(loc.coord());
    // The third plane for the intersection is the pixel plane at
    // interiorPt that isn't either pixplane or orthoPlane.  If this
    // segment is an entry, then interiorPt is the junction between
    // this segment and the next, and the third plane is found at the
    // beginning of the next segment.
    const HPixelPlane *pp = (entry ?
			     orientedOrthogonalPlane(cat, pixplane,
						     pbls.next(), true)
			     :
			     orientedOrthogonalPlane(cat, pixplane,
						     pbls.prev(), false));
    pp->addToIntersection(ppi);
    ppi->setFacePlane(collinearFace); // no-op for MultiFaceIntersection
  }
  
#ifdef DEBUG
  // if(verboseplane) {
  //   oofcerr << "HomogeneityTet::find_one_intersection: pixplane=" << *pixplane
  // 	    << " orthoPlane=" << *orthoPlane << " face=" << bestFace
  // 	    << std::endl;
  // }
  ppi->verbose = verboseplane;
#endif // DEBUG
  return ppi;
} // end HomogeneityTet::find_one_intersection





std::vector<PixelPlaneIntersectionNR*> HomogeneityTet::find_two_intersections(
				      unsigned int cat,
				      const PixelPlaneFacet *facet,
				      const HPixelPlane *pixplane,
				      const HPixelPlane *tempOrthoPlane,
				      const PixelBdyLoopSegment &pblseg,
				      unsigned int onFace,
				      unsigned int orthoFace)
{
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::find_two_intersections: cat=" << cat
// 	    << " pblseg=" << pblseg
// 	    << " pixplane=" << *pixplane
// 	    << " tempOrthoPlane=" << *tempOrthoPlane
// 	    << " onFace=" << onFace << " orthoFace=" << orthoFace
// 	    << std::endl;
// #endif	// DEBUG
  // The pixplane passed to find_two_intersections is the unoriented
  // one, so it can't be used to convert the 2D coords in pblseg to 3D.
  BarycentricCoord b0 = getBarycentricCoord(pblseg.firstPt(), pixplane);
  BarycentricCoord b1 = getBarycentricCoord(pblseg.secondPt(), pixplane);
  ICoord3D segvec = (pixplane->convert2Coord3D(pblseg.secondPt()) -
		     pixplane->convert2Coord3D(pblseg.firstPt()));
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::find_two_intersections: b0=" << b0
// 	    << " b1=" << b1 << std::endl;
// #endif	// DEBUG
  // If the segment enters or exits through a polygon corner, there
  // can appear to be multiple entries or exits at that point, since
  // the segment will intersect two polygon edges.  Keep track of
  // entries and exits separately, to ensure that we don't
  // accidentally return two entries or two exits.

  // Alpha is the fractional position of the intersection along the
  // segment.  alpha=0 puts the intersection at pblseg.firstPt() and
  // alpha=1 puts it at pblseg.secondPt().  Keep the entry with the
  // largest alpha and the exit with the smallest alpha.
  double entryAlpha = -std::numeric_limits<double>::max();
  double exitAlpha = std::numeric_limits<double>::max();
  unsigned int entryFace = NONE;
  unsigned int exitFace = NONE;
  for(const FacePlane *face : facet->getBoundingFaces()) {
    unsigned int n = CSkeletonElement::oppNode[face->face()];
// #ifdef DEBUG
//     if(verboseplane) {
//       oofcerr << "HomogeneityTet::find_two_intersections: n=" << n
// 	      << " face=" << *face << std::endl;
//     }
//     OOFcerrIndent indent(2);
// #endif // DEBUG
    // Skip this face if it lies in the pixel plane or the orthoFace
    // or is collinear with them.
    if(face->face() != onFace && face->face() != orthoFace &&
       !areCollinear(pixplane, tempOrthoPlane, face))
      {
	double b0n = b0[n];
	double b1n = b1[n];
// #ifdef DEBUG
// 	if(verboseplane) {
// 	  oofcerr << "HomogeneityTet::find_two_intersections: b0n=" << b0n
// 		  << " b1n=" << b1n << " b1n-b0n=" << b1n-b0n
// 		  << std::endl;
// 	}
// #endif // DEBUG
	// Skip this face if the segment is parallel to it (b0n ==
	// b1n) (We used to check that the segment crossed the face
	// here with b0n*b1n<0, but that's susceptible to round off
	// error.
	if(b0n != b1n) {
	  double alpha = b0n/(b0n - b1n);
	  // facedot is used to check that the face is oriented
	  // correctly to be an entry or exit.
	  double facedot = dot(faceAreaVector(face->face()), segvec);
	  if(b0n < b1n && facedot < 0 && alpha > entryAlpha) {
	    // This is the best entry point so far.
	    entryAlpha = alpha;
	    entryFace = face->face();
// #ifdef DEBUG
// 	    if(verboseplane)
// 	      oofcerr << "HomogeneityTet::find_two_intersections: alpha="
// 		      << alpha << " entryAlpha=" << entryAlpha << std::endl;
// #endif // DEBUG
	  }
	  else if(b0n > b1n && facedot > 0 && alpha < exitAlpha) {
	    // This is the best exit point so far.
	    exitAlpha = alpha;
	    exitFace = face->face();
// #ifdef DEBUG
// 	    if(verboseplane)
// 	      oofcerr << "HomogeneityTet::find_two_intersections: alpha="
// 		      << alpha << " exitAlpha=" << exitAlpha << std::endl;
// #endif // DEBUG
	  }
	}
      } // end if f != onFace, etc
  }   // end loop over nodes n, faces f

// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::find_two_intersections: entry face="
// 	    << entryFace << " alpha=" << entryAlpha
// 	    << "  exit face=" << exitFace << " alpha=" << exitAlpha
// 	    << std::endl;
//   }
// #endif // DEBUG
  std::vector<PixelPlaneIntersectionNR*> isecs;

  // If we didn't find an entry or exit, or if the entry comes after
  // the exit on the VSB segment, then the segment doesn't intersect
  // the polygon.
  if(entryFace == NONE || exitFace == NONE || entryFace == exitFace ||
     entryAlpha > exitAlpha)
    {
      return isecs;		// empty vec, no intersections
    }

  // Check that the intersection point is actually on the VSB segment.
  // This can happen if the continuation of the segment would
  // intersect the polygon, but the segment itself doesn't.
  if((entryAlpha < 0.0 || entryAlpha > 1.0) ||
     (exitAlpha < 0.0 || exitAlpha > 1.0))
    {
      return isecs;
    }

  BarycentricCoord bentry = averageBary(b0, b1, entryAlpha);
  BarycentricCoord bexit = averageBary(b0, b1, exitAlpha);

  const HPixelPlane *orthoPlane0 = orientedOrthogonalPlane(
					   cat, pixplane, pblseg, entryAlpha);
  const HPixelPlane *orthoPlane1 = orientedOrthogonalPlane(
					   cat, pixplane, pblseg, exitAlpha);
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::find_two_intersections:"
// 	    << " entryFace=" << entryFace << " entryAlpha=" << entryAlpha
// 	    << " " << bentry << " " << bentry.position3D(epts)
// 	    << " orthoplane=" << *orthoPlane0 << std::endl;
//     oofcerr << "HomogeneityTet::find_two_intersections:"
// 	    << " exitFace=" << exitFace << " exitAlpha=" << exitAlpha
// 	    << " " << bexit << " " << bexit.position3D(epts)
// 	    << " orthoplane=" << *orthoPlane1 << std::endl;
//   }
// #endif // DEBUG
  isecs.resize(2);
  isecs[0] = newIntersection(this, pixplane, orthoPlane0, pblseg,
			     entryAlpha, entryFace, ENTRY);
  isecs[1] = newIntersection(this, pixplane, orthoPlane1, pblseg,
			     exitAlpha, exitFace, EXIT);
#ifdef DEBUG
  isecs[0]->verbose = verboseplane;
  isecs[1]->verbose = verboseplane;
#endif // DEBUG

// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::find_two_intersections: isecs=";
//     std::cerr << derefprint(isecs);
//     oofcerr << std::endl;
//   }
// #endif // DEBUG
  return isecs;
} // end HomogeneityTet::find_two_intersections

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given a voxel category, a pixel plane that contains a boundary
// facet for the category, pixel boundary loop segment that is part of
// the boundary, and a position along the segment, return the pixel
// plane that also bounds the category but is perpendicular to the
// given pixel plane at the given point on the segment.
const HPixelPlane *HomogeneityTet::orientedOrthogonalPlane(
					     unsigned int cat,
					     const HPixelPlane *pixplane,
					     const PixelBdyLoopSegment &pbls,
					     double alpha)
{
  // orthoPlane (set below) goes through the segment and has a
  // normal that points toward the outside of the boundary loop.  This
  // may not be the correct normal.
  
  // If the voxel just outside orthoPlane and just below pixplane is
  // outside the voxel category, then the outward normal is correct.
  // This condition needs to be evaluated at the given point on the
  // segment, because the result can be different at different points.
  // The condition is the same as asking if the VSB forms a ridge or
  // valley fold (as in origami).  A ridge fold means that normal of
  // the perpendicular plane points away from the loop.  A valley fold
  // means that it points into the loop.


  // This is a cross section through four voxels at the point in
  // question:
  //           |?????????   
  //           |?????????   
  //           |?????????
  //           |?????????
  // ----------O----------  <-- pixplane, seen edge on
  // ..........|\????????
  // ..........|?\???????
  // ..........|??X<----------- test point
  // ..........|?????????

  // The horizontal dashed line is the pixplane, and the vertical one
  // is the orthogonal plane that we wish to find.  The point O is
  // where the pixel boundary loop segment enters the screen.  The
  // voxel marked with dots is in the voxel category, and unmarked
  // voxel is not.
  
  // If the test point X is also in the voxel category, then the
  // correct normal for the orthogonal plane is inward:
  //           |.........   
  //           |.........                                   |
  //     <=====|.........        This configuration -->     |
  //           |.........        is impossible              |
  // ----------O----------       because it doesn't --------O-------- 
  // ..........|\........        have a facet edge  ........|........
  // ..........|.\.......        in pixplane at     ........|........
  // ..........|..X......        point O.           ........|........
  // ..........|.........


  // If the test point is outside the category, the normal is outward:
  //           |?????????   
  //           |????????? <-- It doesn't matter if this voxel is inside
  //           |?????????     or outside the category.
  //           |?????????
  // ----------O---------- 
  // ..........|        
  // ..........|=====>        
  // ..........|        
  // ..........|         


  ICoord2D pt0 = pbls.firstPt();
  ICoord2D pt1 = pbls.secondPt();
  HPixelPlane *orthoPlane = pixplane->orthogonalPlane(pt0, pt1);
  const FacePixelPlane *fpp = getCoincidentFacePlane(orthoPlane);
  if(fpp)
    return fpp;
  ICoord3D baseNormal = pixplane->normalVector();
  ICoord3D loopNormal = orthoPlane->normalVector(); // lies in pixplane

// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::orientedOrthogonalPlane: cat=" << cat
// 	    << " pixplane=" << *pixplane
// 	    << " pt0=" << pt0 << " pt1=" << pt1 << " alpha=" << alpha
// 	    << std::endl;
//   }
//   OOFcerrIndent indent(2);
// #endif // DEBUG
  
  // X is the real space position of the point.  Computing the
  // position this way (ie, in real space, not just topologically) is
  // necessary in order to examine the category of the neighboring
  // voxel.
  Coord3D X = pixplane->convert2Coord3D((1-alpha)*pt0 + alpha*pt1);
  Coord3D testPt = X + 0.5*(loopNormal - baseNormal); // in pixel units

  return orientedOrthogonalPlane_(cat, pixplane, orthoPlane, testPt);
}

// This version of orientedOrthogonalPlane returns the orthogonal
// plane at the start or end of the given boundary loop segment.

const HPixelPlane *HomogeneityTet::orientedOrthogonalPlane(
					     unsigned int cat,
					     const HPixelPlane *pixplane,
					     const PixelBdyLoopSegment &pbls,
					     bool start)
{
  ICoord2D pt0 = pbls.firstPt();
  ICoord2D pt1 = pbls.secondPt();
  HPixelPlane *orthoPlane = pixplane->orthogonalPlane(pt0, pt1);
  const FacePixelPlane *fpp = getCoincidentFacePlane(orthoPlane);
  if(fpp)
    return fpp;
  ICoord3D baseNormal = pixplane->normalVector();
  ICoord3D loopNormal = orthoPlane->normalVector();
  // Don't actually compute at the end of the segment.  Avoid
  // ambiguity by moving half a voxel in.
  Coord2D fudge = (pbls.horizontal() ?
		    (pt0[0] < pt1[0] ? Coord2D(0.5, 0) : Coord2D(-0.5, 0)) :
		    (pt0[1] < pt1[1] ? Coord2D(0, 0.5) : Coord2D(0, -0.5)));
  Coord3D X = pixplane->convert2Coord3D(start? pt0 + fudge : pt1 - fudge);
  Coord3D testPt = X + 0.5*(loopNormal - baseNormal);
  return orientedOrthogonalPlane_(cat, pixplane, orthoPlane, testPt);
}

// Utility function used by the two versions of orientedOrthogonalPlane.
const HPixelPlane *HomogeneityTet::orientedOrthogonalPlane_(
					    unsigned int cat,
					    const HPixelPlane *pixplane,
					    HPixelPlane *orthoPlane,
					    const Coord3D &testPt)
{
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::orientedOrthogonalPlane_: testPt=" << testPt
// 	    << " pixplane=" << pixplane << " " << *pixplane
// 	    << " orthoPlane=" << orthoPlane << " " << *orthoPlane
// 	    << std::endl;
//   }
// #endif // DEBUG
  if(!microstructure->containsPixelCoord(testPt)) {
    // At the edge of the microstructure there are no valleys.
// #ifdef DEBUG
//     if(verboseplane)
//       oofcerr << "HomogeneityTet::orientedOrthogonalPlane_: not in MS"
// 	      << std::endl;
// #endif // DEBUG
    return getPixelPlane(orthoPlane);
  }
  unsigned int testCat = microstructure->category(
				    microstructure->pixel2Physical(testPt));
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::orientedOrthogonalPlane_: testCat=" << testCat
// 	    << std::endl;
// #endif // DEBUG
  if(testCat == cat) {
    HPixelPlane *flipped = orthoPlane->flipped();
// #ifdef DEBUG
//     if(verboseplane)
//       oofcerr << "HomogeneityTet::orientedOrthogonalPlane_: flipped="
// 	      << *flipped << std::endl;
// #endif // DEBUG
    delete orthoPlane;
    return getPixelPlane(flipped);
  }
// #ifdef DEBUG
//     if(verboseplane)
//       oofcerr << "HomogeneityTet::orientedOrthogonalPlane_: unflipped="
// 	      << *orthoPlane << std::endl;
// #endif // DEBUG
  return getPixelPlane(orthoPlane);
} // end HomogeneityTet::orientedOrthogonalPlane

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// #ifdef CLEAN_UP_LOOSE_ENDS
// // cleanUpLooseEnds removes a loose start or end from the given sets
// // of FaceEdgeIntersections, when it's known that there's at least one
// // extra one.  It looks at all pairs of adjacent points on each edge,
// // and removes one member of the pair with the smallest separation.
// // It only looks at points which are either starts or stops, according
// // to the "start" argument.

// static bool cleanUpLooseEnds(std::vector<LooseEndMap> &looseEnds, bool start) {
//   double smallestDist = std::numeric_limits<double>::max();
//   unsigned int edge = NONE;
//   LooseEndMap::iterator deleteMe;

//   for(unsigned int e=0; e<looseEnds.size(); e++) {
//     LooseEndMap &lem = looseEnds[e];
//     LooseEndMap::iterator i = lem.begin();
//     if(i != lem.end()) {
//       LooseEndMap::iterator prev = i;
//       i++;
//       for( ; i!=lem.end(); ++i) {
// 	if((*i).second.start() == start && (*prev).second.start() == start &&
// 	   (*i).first - (*prev).first < smallestDist)
// 	  {
// 	    smallestDist = (*i).first - (*prev).first;
// 	    deleteMe = i;
// 	    edge = e;
// 	  }
// 	prev = i;
//       }
//     }
//   }
//   if(edge != NONE) {
//     looseEnds[edge].erase(deleteMe);
//     return true;
//   }
//   return false;
// }
// #endif // CLEAN_UP_LOOSE_ENDS

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FaceFacets HomogeneityTet::findFaceFacets(unsigned int cat,
					  const FacetMap2D &planeFacets)
{
#ifdef DEBUG
  verbosecategory = verboseCategory_(verbose, cat);
  if(verbosecategory)
    oofcerr << "HomogeneityTet::findFaceFacets: cat=" << cat << std::endl;
  OOFcerrIndent indent(2);
  int loopcount = 0;
#endif // DEBUG
  FaceFacets faceFacets;
  faceFacets.reserve(NUM_TET_FACES);
  for(unsigned int f=0; f<NUM_TET_FACES; f++)
    faceFacets.emplace_back(f, this);

  // looseEndCatalog[f] is a LooseEndSet for face f.  A LooseEndSet is
  // a set of FaceEdgeIntersection*s. 
  LooseEndCatalog looseEndCatalog(NUM_TET_FACES);
  std::vector<StrandedPoint> strandedPoints;

  // Some operations merge points, which means that a point that
  // wasn't known to be on a tet edge may become known to be on a tet
  // edge.  This change in topology means that the calculation of
  // which pixel plane facet edges are on which faces may have to be
  // repeated.
  bool pointsHaveChanged = false;
  
  // Loop until no points have changed.
  do {
#ifdef DEBUG
    if(verbosecategory) {
      oofcerr << "HomogeneityTet::findFaceFacets: loopcount=" << ++loopcount
	      << std::endl;
    }
    if(loopcount > 10) {
      throw ErrProgrammingError("Loopcount too big!", __FILE__, __LINE__);
    }
#endif // DEBUG
    // Get a clean start.
    pointsHaveChanged = false;
    for(FaceFacet &ff : faceFacets)
      ff.clear();
    for(LooseEndSet &looseEnds : looseEndCatalog)
      looseEnds.clear();
    strandedPoints.clear();

    // Loop over pixel plane facets, copying the edges that lie in tet
    // faces into the empty face facet strutures.
    for(FacetMap2D::const_iterator fm=planeFacets.begin();
	fm!=planeFacets.end(); ++fm)
      {
	PixelPlaneFacet *planeFacet = (*fm).second;
	planeFacet->getEdgesOnFaces(faceFacets);
      }
#ifdef DEBUG
    if(verbosecategory) {
      oofcerr << "HomogeneityTet::findFaceFacets:"
	      << " edges from pixel plane facets:" << std::endl;
      OOFcerrIndent indent(2);
      for(unsigned int f=0; f<NUM_TET_FACES; f++) {
	verboseface = verboseFace_(verbosecategory, f);
	if(verboseface) {
	  if(coincidentPixelPlanes[f] == nullptr) {
	    oofcerr << "HomogeneityTet::findFaceFacets: facet=" << faceFacets[f]
		    << std::endl;
	    faceFacets[f].dump("facefacet_orig", cat);
	  }
	}
      }
      verboseface = false;
    }
#endif	// DEBUG

    // Loop over all faces that aren't also pixel planes, finding the
    // loose ends of the edges of the incomplete face facets.
#ifdef DEBUG
    if(verbosecategory) {
      oofcerr << "HomogeneityTet::findFaceFacets: starting findLooseEnds loop"
	      << std::endl;
      }
#endif // DEBUG
    for(unsigned int face=0; face<NUM_TET_FACES; face++) {
      if(coincidentPixelPlanes[face] == nullptr) {
#ifdef DEBUG
	verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
	FaceFacet &facet = faceFacets[face];
	// Make sure equivalence classes are up to date.
	// TODO: If checkEquiv is run for each new PlaneIntersection, is
	// this loop necessary?
	for(auto seg=facet.edges().begin(); seg!=facet.edges().end(); ++seg) {
	  checkEquiv((*seg)->startPt());
	  checkEquiv((*seg)->endPt());
	}
	// findLooseEnds creates FaceEdgeIntersection objects for each
	// endpoint of each segment on the facet and stores the
	// unpaired ones either in looseEndCatalog (if they're on an
	// edge of a face) or in strandedPoints (if they're not).
	facet.findLooseEnds(looseEndCatalog[face], strandedPoints);
#ifdef DEBUG
	verboseface = false;
#endif // DEBUG
      }	// end if face isn't coincident with a pixel plane
    } // end loop over faces, face
#ifdef DEBUG
    if(verbosecategory) {
      oofcerr << "HomogeneityTet::findFaceFacets: finished findLooseEnds loop"
	      << std::endl;
    }
#endif // DEBUG
#ifdef DEBUG
  if(verbosecategory) {
    if(strandedPoints.empty())
      oofcerr << "HomogeneityTet::findFaceFacets: no strandedPoints"
	      << std::endl;
    else {
      oofcerr << "HomogeneityTet::findFaceFacets: strandedPoints=" << std::endl;
      OOFcerrIndent indent(2);
      for(const StrandedPoint &pt : strandedPoints)
	oofcerr << "HomogeneityTet::findFaceFacets: face=" << pt.face
		<<  " " << *pt.feInt << std::endl;
    }
  }
#endif // DEBUG

    // Try to pair up the stranded points (loose ends that aren't on a
    // tet edge).  This is outside the loop over faces, because it may
    // merge points on different faces.
    std::vector<StrandedPoint> marooned = matchStrandedPoints(
		      strandedPoints, looseEndCatalog, pointsHaveChanged);

#ifdef DEBUG
    if(verbosecategory) {
      oofcerr << "HomogeneityTet::findFaceFacets: back from matchStrandedPoints"
	      << std::endl;
      oofcerr << "HomogeneityTet::findFaceFacets: marooned points="
	      << std::endl;
      OOFcerrIndent indent(4);
      for(const StrandedPoint &pt : marooned)
	oofcerr << "HomogeneityTet::findFaceFacets: face=" << pt.face
		<< " " << *pt.feInt << std::endl;
    }
#endif	// DEBUG
    
    // Force the unmatched stranded points onto the nearest tet edge.
    pointsHaveChanged = pointsHaveChanged || !marooned.empty();
    for(StrandedPoint &sp : marooned) {
      sp.feInt->forceOntoEdge(sp.face, this);
      // There's no point in adding the intersection to the
      // looseEndCatalog, because the catalog will be rebuilt before
      // it's used, since pointsHaveChanged==true.
      // looseEndCatalog[sp.face].insert(sp.feInt);
    }

    // If points have been merged, start over, rebuilding the face
    // facet edges from the modified pixel plane facets.
    if(pointsHaveChanged) {
#ifdef DEBUG
      if(verbosecategory) {
	oofcerr << "HomogeneityTet::findFaceFacets: restarting"
		<< std::endl;
      }
#endif // DEBUG
      continue;
    }

    // Loop over tet faces, again, looking for topological
    // inconsistencies that indicate that distinct points must
    // actually coincide.
    for(unsigned int face=0; face<NUM_TET_FACES; face++) {
      if(coincidentPixelPlanes[face] == nullptr) {
#ifdef DEBUG
	verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
	FaceFacet &facet = faceFacets[face];

	// First find the existing face facet edges that lie on tet edges.
	// (TODO: Can this be done more efficiently earlier, perhaps
	// during the getEdgesOnFaces stage? Possibly not, because the
	// resolution of stranded and marooned points moves some points
	// onto edges.)
	std::vector<FaceFacetEdgeSet> edgeEdges(NUM_TET_FACE_EDGES);
	for(FaceFacetEdge *edge : facet.edges()) {
	  unsigned int faceEdge = edge->findFaceEdge(face, this);
	  if(faceEdge != NONE) {
	    edgeEdges[faceEdge].insert(edge);
	  }
	}

	// Detect and merge coincident intersection points on the tet
	// edges.
	bool merged = resolveFaceFacetCoincidences(face, looseEndCatalog[face],
						    edgeEdges);
	pointsHaveChanged = pointsHaveChanged || merged;
	
#ifdef DEBUG
	verboseface = false;
#endif // DEBUG
      }	// end if face isn't coincident with a pixel plane (2)
    } // end loop over tet faces (2)
#ifdef DEBUG
    if(verbosecategory)
      oofcerr << "HomogeneityTet::findFaceFacets: end of while loop,"
	      << " pointsHaveChanged=" << pointsHaveChanged << std::endl;
#endif // DEBUG
  } while(pointsHaveChanged);

#ifdef DEBUG
    if(verbosecategory)
      oofcerr << "HomogeneityTet::findFaceFacets: exited while loop"
	      << std::endl;
#endif // DEBUG
    
  // At this stage all operations that can merge points have
  // completed.  The loose ends on each face facet can be linked by
  // new face facet edges.

  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
    if(coincidentPixelPlanes[face] == nullptr) {
#ifdef DEBUG
      verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
      FaceFacet &facet = faceFacets[face];
      LooseEndSet &looseEnds = looseEndCatalog[face];
      if(!looseEnds.empty()) {
	// Put all the LooseEnds in a single vector, ordered by face
	// edge and position along the edge.
	std::vector<FaceEdgeIntersection*> sortedLooseEnds(looseEnds.begin(),
							   looseEnds.end());
	std::sort(sortedLooseEnds.begin(), sortedLooseEnds.end(),
		  FaceEdgeIntersectionLT());
	unsigned int npts = sortedLooseEnds.size();

	// The missing segments that close the loops start at a loose
	// end and end at a loose start.  Find the first loose end.
	unsigned int i0 = 0;
	bool found = false;
	for(; i0<npts; i0++) {
	  if(!sortedLooseEnds[i0]->start()) {
	    found = true;
	    break;
	  }
	}
	if(!found) {
	  oofcerr << "HomogeneityTet::findFaceFacets: failed! cat="
		  << cat << " face=" << face << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: sortedLooseEnds="
		  << std::endl;
	  OOFcerrIndent indent(2);
	  for(unsigned int i=0; i<sortedLooseEnds.size(); i++)
	    oofcerr << "HomogeneityTet::findFaceFacets: " << *sortedLooseEnds[i]
		    << std::endl;
	  throw ErrProgrammingError("findFaceFacets failed to find first end!",
				    __FILE__, __LINE__);
	}
	// Loop over pairs (i, j) of adjacent loose ends, starting at
	// i0.  i is an end, and j is a start.
	for(unsigned int ii=0; ii<npts; ii+=2) {
	  unsigned int i= ii + i0;
	  if(i >= npts)
	    i -= npts;
	  unsigned int j = i + 1;
	  if(j >= npts)
	    j -= npts;
	  facet.addFaceEdges(sortedLooseEnds[i], sortedLooseEnds[j], this);
	} // end loop over ii
	
      }	// end if there are loose ends on the face

      // Remove pairs of equal and opposite segments
      facet.removeOpposingEdges();
      // Fix situations that can cause the area to be zero or negative.
      facet.fixNonPositiveArea(this, cat);

#ifdef DEBUG
      verboseface = false;
#endif // DEBUG
    } // end if face isn't coincident with a pixel plane (3)
  } // end loop over tet faces (3)
#ifdef DEBUG
  verbosecategory = false;
#endif // DEBUG
  return faceFacets;
} // end HomogeneityTet::findFaceFacets


#ifdef OLDFINDFACEFACETS
FaceFacets HomogeneityTet::findFaceFacetsOLD(unsigned int cat,
					  const FacetMap2D &planeFacets)
{
#ifdef DEBUG
  verbosecategory = verboseCategory_(verbose, cat);
  if(verbosecategory)
    oofcerr << "HomogeneityTet::findFaceFacets: cat=" << cat << std::endl;
  OOFcerrIndent indent(2);
#endif // DEBUG
  FaceFacets faceFacets;
  faceFacets.reserve(NUM_TET_FACES);
  for(unsigned int f=0; f<NUM_TET_FACES; f++)
    faceFacets.emplace_back(f, this);

  // Loop over pixel plane facets, sorting the edges that lie in tet
  // faces.

  for(FacetMap2D::const_iterator fm=planeFacets.begin(); fm!=planeFacets.end();
      ++fm)
    {
      PixelPlaneFacet *planeFacet = (*fm).second;
      // getEdgesOnFaces asks each PolygonEdge to store a reversed
      // copy of itself in faceFacets.  A new FaceFacetEdge is created
      // in faceFacets for each edge of the PixelPlaneFacet that lies
      // in a tet face.
// #ifdef DEBUG
//       if(verbosecategory)
// 	oofcerr << "HomogeneityTet::findFaceFacets: calling getEdgesOnFaces for"
// 		<< " " << *planeFacet->pixplane << std::endl;
//       OOFcerrIndent indent(2);
// #endif	// DEBUG
      planeFacet->getEdgesOnFaces(faceFacets);
    }
#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: edges from pixel plane facets:"
    	    << std::endl;
    OOFcerrIndent indent(2);
    for(unsigned int f=0; f<NUM_TET_FACES; f++) {
      verboseface = verboseFace_(verbosecategory, f);
      if(verboseface) {
    	if(coincidentPixelPlanes[f] == nullptr) {
    	  oofcerr << "HomogeneityTet::findFaceFacets: facet=" << faceFacets[f]
    		  << std::endl;
    	  faceFacets[f].dump("facefacet_orig", cat);
    	}
      }
    }
    verboseface = false;
  }
#endif	// DEBUG

  // looseEndCatalog[f] is a LooseEndSet for face f.  A LooseEndSet is
  // a set of FaceEdgeIntersections.

  LooseEndCatalog looseEndCatalog(NUM_TET_FACES);
  std::vector<StrandedPoint> strandedPoints;

  // Loop over all faces that aren't also pixel planes.
#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: starting findLooseEnds loop"
	    << std::endl;
  }
#endif // DEBUG
  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
    if(coincidentPixelPlanes[face] == nullptr) {
#ifdef DEBUG
      verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
      FaceFacet &facet = faceFacets[face];

      // Make sure equivalence classes are up to date.
      // TODO: If checkEquiv is run for each new PlaneIntersection, is
      // this loop necessary?
      for(auto seg=facet.edges().begin(); seg!=facet.edges().end(); ++seg) {
	checkEquiv((*seg)->startPt());
	checkEquiv((*seg)->endPt());
      }

      facet.findLooseEnds(looseEndCatalog[face], strandedPoints);

#ifdef DEBUG
      verboseface = false;
#endif // DEBUG
    } // end if face is not on a pixel plane
  } // end loop over faces, face
#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: finished findLooseEnds loop"
	    << std::endl;
  }
#endif // DEBUG
 
#ifdef DEBUG
  if(verbosecategory) {
    if(strandedPoints.empty())
      oofcerr << "HomogeneityTet::findFaceFacets: no strandedPoints"
	      << std::endl;
    else {
      oofcerr << "HomogeneityTet::findFaceFacets: strandedPoints=" << std::endl;
      OOFcerrIndent indent(2);
      for(const StrandedPoint &pt : strandedPoints)
	oofcerr << "HomogeneityTet::findFaceFacets: face=" << pt.face
		<<  " " << *pt.feInt << std::endl;
    }
  }
#endif // DEBUG

  StrandedPointLists marooned = matchStrandedPoints(strandedPoints,
						    looseEndCatalog);
#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: back from matchStrandedPoints"
	    << std::endl;
    oofcerr << "HomogeneityTet::findFaceFacets: marooned points=" << std::endl;
    OOFcerrIndent indent(4);
    for(unsigned int f=0; f<NUM_TET_FACES; f++) {
      verboseface = verboseFace_(verbosecategory, f);
      for(StrandedPoint &sp : marooned[f])
	oofcerr << "HomogeneityTet::findFaceFacets: f=" << f << " "
		<< *sp.feInt << std::endl;
    }
  }
#endif	// DEBUG
  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
    if(coincidentPixelPlanes[face] == nullptr) { // face is not a pixel plane
#ifdef DEBUG
      verboseface = verboseFace_(verbosecategory, face);
      // if(verboseface)
      // 	oofcerr << "HomogeneityTet::findFaceFacets: second loop over face "
      // 		<< face << " category " << cat << std::endl;
      OOFcerrIndent indent(2);
#endif // DEBUG
      FaceFacet &facet = faceFacets[face];
      LooseEndSet &looseEnds = looseEndCatalog[face];
      // Coord3D faceNormal = faceAreaVectors[face]; // not a unit vector

#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets:"
		<< " before handling marooned points, cat=" << cat
		<< " face=" << face << " looseEnds=" << std::endl;
	printLooseEnds(looseEnds);
      }
#endif // DEBUG
      // Put any marooned points onto the closest edge.
      for(StrandedPoint &sp : marooned[face]) {
	sp.feInt->forceOntoEdge(sp.face, this);
	looseEnds.insert(sp.feInt);
      }
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets:"
		<< " after handling marooned points, cat=" << cat
		<< " face=" << face << " looseEnds=" << std::endl;
	printLooseEnds(looseEnds);
      }
#endif // DEBUG

      // Find the existing facet edges that lie on the tet edges.
      // (TODO: Can this be done more efficiently earlier, perhaps
      // during the getEdgesOnFaces stage? Possibly not, because the
      // resolution of stranded and marooned points moves some points
      // onto edges.)
      std::vector<FaceFacetEdgeSet> edgeEdges(NUM_TET_FACE_EDGES);
      for(FaceFacetEdge *edge : facet.edges()) {
	unsigned int faceEdge = edge->findFaceEdge(face, this);
	if(faceEdge != NONE) {
	  edgeEdges[faceEdge].insert(edge);
	}
      }
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets:"
		<< " before resolveFaceFacetCoincidences, cat=" << cat
		<< " face=" << face << " looseEnds=" << std::endl;
	printLooseEnds(looseEnds);
      }
#endif // DEBUG

      // Detect and merge coincident intersection points on the tet
      // edges.
      resolveFaceFacetCoincidences(face, looseEnds, edgeEdges);
// #ifdef DEBUG
//       if(verboseface) {
// 	oofcerr << "HomogeneityTet::findFaceFacets:"
// 		<< " after resolveFaceFacetCoincidences, looseEnds (unsorted)="
// 		<< std::endl;
// 	OOFcerrIndent indent(2);
// 	printLooseEnds(looseEnds);
//       }
// #endif // DEBUG

      if(!looseEnds.empty()) {
	// Put all the LooseEnds in a single vector, ordered by face
	// edge and position along the edge.
	std::vector<FaceEdgeIntersection*> sortedLooseEnds(
					 looseEndCatalog[face].begin(),
					 looseEndCatalog[face].end());
	std::sort(sortedLooseEnds.begin(), sortedLooseEnds.end(),
		  FaceEdgeIntersectionLT());
	unsigned int npts = sortedLooseEnds.size();

#ifdef DEBUG
	if(verboseface) {
	  oofcerr << "HomogeneityTet::findFaceFacets:"
		  << " after sorting, looseEnds =" << std::endl;
	  OOFcerrIndent indent(2);
	  printLooseEnds(sortedLooseEnds);
	}
#endif // DEBUG
	
	// The missing segments that close the loops start at a loose
	// end and end at a loose start. Find the first loose end.
	unsigned int i0 = 0;
	bool found = false;
	for(; i0<npts; i0++) {
	  if(!sortedLooseEnds[i0]->start()) {
	    found = true;
	    break;
	  }
	}
	if(!found) {
	  oofcerr << "HomogeneityTet::findFaceFacets: failed! cat="
		  << cat << " face=" << face << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: sortedLooseEnds="
		  << std::endl;
	  OOFcerrIndent indent(2);
	  for(unsigned int i=0; i<sortedLooseEnds.size(); i++)
	    oofcerr << "HomogeneityTet::findFaceFacets: " << *sortedLooseEnds[i]
		    << std::endl;
	  throw ErrProgrammingError("findFaceFacets failed to find first end!",
				    __FILE__, __LINE__);
	}
	// Loop over pairs (i, j) of adjacent loose ends, starting at
	// i0.  i is an end, and j is a start.
	for(unsigned int ii=0; ii<npts; ii += 2) {
	  unsigned int i = ii+i0;
	  if(i >= npts)
	    i -= npts;
	  unsigned int j = i + 1;
	  if(j >= npts)
	    j -= npts;
#ifdef DEBUG
	  if(sortedLooseEnds[i]->start() || !sortedLooseEnds[j]->start()) {
	    oofcerr << "HomogeneityTet::findFaceFacets: loose end mismatch! i="
		    << i << " j=" << j << " i0=" << i0
		    << " face=" << face << " cat=" << cat
		    << std::endl;
	    OOFcerrIndent indent(2);
	    EdgePosition lastT;
	    unsigned int lastEdge = NONE;
	    for(auto *le : sortedLooseEnds) {
	      oofcerr << "HomogeneityTet::findFaceFacets: " << *le;
	      if(le->faceEdge() == lastEdge && !lastT.unset())
		oofcerr << " dt=" << le->edgePosition() - lastT;
	      lastT = le->edgePosition();
	      lastEdge = le->faceEdge();
	      oofcerr << std::endl;
	    }
	    // dumpEquivalences();
	    throw ErrProgrammingError("Loose ends don't pair up!",
				      __FILE__, __LINE__);
	  }
#endif // DEBUG
	  facet.addFaceEdges(sortedLooseEnds[i], sortedLooseEnds[j], this);
	}
      }	// end if there are loose ends

      // Remove pairs of equal and opposite segments.
      facet.removeOpposingEdges();
      // Fix situations that can cause the area to be zero or negative.
      facet.fixNonPositiveArea(this, cat);
      
#ifdef DEBUG
      // if(verboseface) {
      //  	oofcerr << "HomogeneityTet::findFaceFacets: done with face "
      //  		<< face << std::endl;
      // }
      verboseface = false;
      // for(unsigned int f=0; f<NUM_TET_FACES; f++) {
      // 	if(verboseFace_(verbosecategory, f)) {
      // 	  oofcerr << "HomogeneityTet::findFaceFacets: " << faceFacets[f]
      // 		  << std::endl;
      // 	}
      // }
#endif // DEBUG
    }  // end if face is not on a pixel plane
  }    // end second loop over faces, face

#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: returning.  Face facets are:"
	    << std::endl;
    OOFcerrIndent indent(2);
    for(unsigned int face=0; face<NUM_TET_FACES; face++) {
      if(verboseFace_(verbosecategory, face)) {
	if(coincidentPixelPlanes[face] == nullptr) {
	  FaceFacet &facet = faceFacets[face];
	  oofcerr << "HomogeneityTet::findFaceFacets: " << facet << std::endl;
	  facet.dump("facefacet", cat);
	}
      }
    }
  }
#endif // DEBUG
  
#ifdef DEBUG
  verbosecategory = false;
#endif // DEBUG
  return faceFacets;
} // end HomogeneityTet::findFaceFacetsOLD
#endif // OLDFINDFACEFACETS

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// matchStrandedPoints pairs up the stranded points left over by
// findLooseEnds..  Stranded points arise when the intersection line
// of two perpendicular pixel planes nearly passes through a tet edge
// (to within round off error).  In that case, there will be
// intersection points on the two planes but on different faces, and
// because each point is only on one face, it won't be assigned to a
// tet edge.

// If there are no other pixel planes creating segments connecting
// to those points, they will be loose ends of each face facet, but
// they're not on tet edges, so they can't be joined by adding facet
// edges on the tet edges.  When the stranded points are paired,
// each point of each pair must be on a different tet face, and
// merging the pair produces a point on a tet edge (the edge shared
// by the two faces).  The new merged point can be inserted into the
// looseEndCatalog.

std::vector<StrandedPoint> HomogeneityTet::matchStrandedPoints(
			       std::vector<StrandedPoint> &strandedPoints,
			       LooseEndCatalog &looseEndCatalog,
			       bool &pointsHaveChanged)
{
#ifdef DEBUG
  if(verbosecategory)
    oofcerr << "HomogeneityTet::matchStrandedPoints: size="
	    << strandedPoints.size() << std::endl;
#endif // DEBUG
  
  // Stranded intersection points that can't be matched are marooned.
  // The list of marooned points is returned.  
  std::vector<StrandedPoint> marooned;

  if(strandedPoints.empty())
    return marooned;

  //#define EXPERIMENTAL
#ifdef EXPERIMENTAL
  // Trying to just force stranded points onto edges, without matching
  // them with other stranded points first.
  // TODO: If this hack works, then change findFaceFacets so that
  // matchStrandedPoints isn't even called.
  for(StrandedPoint &pt0 : strandedPoints)
    marooned.push_back(pt0);
  return marooned;

#else // EXPERIMENTAL

  
  std::vector<bool> matched(strandedPoints.size(), false);

  for(unsigned int i=0; i<strandedPoints.size(); i++) {
    // The i loop goes up to strandedPoints.size(), not size-1,
    // because if there's only one strandedPoint it has to be put in
    // the marooned list.
    if(!matched[i]) {
      const StrandedPoint &pt0 = strandedPoints[i];
// #ifdef DEBUG
//       if(verbosecategory) {
// 	oofcerr << "HomogeneityTet::matchStrandedPoints: i=" << i
// 		<< " pt0=" << *pt0.feInt << std::endl;
//       }
// #endif // DEBUG
      unsigned int best = NONE;
      double mindist2 = std::numeric_limits<double>::max();
      for(unsigned int j=i+1; j<strandedPoints.size(); j++) {
// #ifdef DEBUG
// 	OOFcerrIndent ind(2);
// 	if(verbosecategory) {
// 	  oofcerr << "HomogeneityTet::matchStrandedPoints: j=" << j
// 		  << std::endl;
// 	}
// #endif // DEBUG
	const StrandedPoint &pt1 = strandedPoints[j];
// #ifdef DEBUG
// 	if(verbosecategory) {
// 	  oofcerr << "HomogeneityTet::matchStrandedPoints: pt1=" << *pt1.feInt
// 		  << std::endl;
// 	}
// #endif // DEBUG
	if(pt0.face != pt1.face &&
	   pt0.feInt->corner()->samePixelPlanes(pt1.feInt->corner()))
	  {
	    double dist2 = norm2(pt0.feInt->corner()->location3D() -
				 pt1.feInt->corner()->location3D());
// #ifdef DEBUG
// 	    if(verbosecategory)
// 	      oofcerr << "HomogeneityTet::matchStrandedPoints: dist2="
// 		      << dist2 << std::endl;
// #endif // DEBUG
	    if(dist2 < mindist2) {
	      mindist2 = dist2;
	      best = j;
	    }
	  }
// #ifdef DEBUG
// 	else {
// 	  if(verbosecategory)
// 	    oofcerr << "HomogeneityTet::matchStrandedPoints: not comparing"
// 		    << std::endl;
// 	}
// #endif // DEBUG
      }	// end loop over possible matches j
// #ifdef DEBUG
//       if(verbosecategory) 
// 	oofcerr << "HomogeneityTet::matchStrandedPoints: done with j loop,"
// 		<< " best=" << best << std::endl;
// #endif // DEBUG
      if(best != NONE) {
	matched[best] = true;
	matched[i] = true;
	const StrandedPoint &pt1 = strandedPoints[best];
#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "HomogeneityTet::matchStrandedPoints: merging:"
		  << std::endl;
	  OOFcerrIndent indent(2);
	  oofcerr << "HomogeneityTet::matchStrandedPoints: pt0=" << *pt0.feInt
		  << std::endl;
	  oofcerr << "HomogeneityTet::matchStrandedPoints: pt1=" << *pt1.feInt
		  << std::endl;
	}
#endif // DEBUG
	// The PixelPlaneIntersections are stored in
	// FaceEdgeIntersection as generic PlaneIntersections, but in
	// this case we know that they're PixelPlaneIntersections.
	// TODO: Can we do this without the dynamic_casts?
	PixelPlaneIntersection *ppi0 =
	  dynamic_cast<PixelPlaneIntersection*>(pt0.feInt->corner());
	PixelPlaneIntersection *ppi1 =
	  dynamic_cast<PixelPlaneIntersection*>(pt1.feInt->corner());
	assert(ppi0 != nullptr && ppi1 != nullptr);
	PixelPlaneIntersectionNR *merged =
	  new MultiCornerIntersection(this, ppi0->referent(), ppi1->referent());
	mergeEquiv(ppi0->referent(), ppi1->referent(), merged);
	// FaceFacetEdge::replacePoint clones its argument and returns
	// the clone, which is the object actually stored in the edge.
	PlaneIntersection *newpt0 =
	  pt0.feInt->edge()->replacePoint(merged, this, pt0.feInt->start());
	PlaneIntersection *newpt1 =
	  pt1.feInt->edge()->replacePoint(merged, this, pt1.feInt->start());
	FaceEdgeIntersection *fei0 = newFaceEdgeIntersection(
			   newpt0, pt0.feInt->edge(), pt0.feInt->start());
	FaceEdgeIntersection *fei1 = newFaceEdgeIntersection(
			   newpt1, pt1.feInt->edge(), pt1.feInt->start());
	fei0->findFaceEdge(pt0.face, this);
	fei1->findFaceEdge(pt1.face, this);
	looseEndCatalog[pt0.face].insert(fei0);
	looseEndCatalog[pt1.face].insert(fei1);
#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "HomogeneityTet::matchStrandedPoints: after merging,"
		  << std::endl;
	  oofcerr << "HomogeneityTet::matchStrandedPoints: fei0=" << *fei0
		  << std::endl;
	  oofcerr << "HomogeneityTet::matchStrandedPoints: fei1=" << *fei1
		  << std::endl;
	}
#endif // DEBUG
	// The merged point isn't in a FacetEdge, so it won't be
	// automatically deleted.  Store it for later deletion.
	extraPoints.insert(merged);
	pointsHaveChanged = true;
      }	// end if best is not NONE
      else {
	// No match found for point i
	marooned.push_back(pt0);
// #ifdef DEBUG
// 	if(verbosecategory)
// 	  oofcerr << "HomogeneityTet::matchStrandedPoints: marooned point! "
// 		  << *pt0.feInt << std::endl;
// #endif // DEBUG
      }
    } // end if point i hasn't been matched
  }   // end loop over stranded points i

  return marooned;

#endif // EXPERIMENTAL
  
} // end HomogeneityTet::matchStrandedPoints

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// resolveFaceFacetCoincidences resolves topological impossibilities
// that can arise from round off error in the positions of the
// unmatched loose end points around the perimeter of a tet face.
// These points have to be connected to complete the FaceFacets.  The
// points come in two flavors: starts, where an existing segment
// starts, and stops, where an existing segments stops.  Stops need to
// be connected to starts by adding new segments going
// counterclockwise around the perimeter of the face.  If stops and
// starts are in the wrong order, incorrect segments will be added.
// Round-off error can make two points that are supposed to be
// coincident or nearly coincident to appear to be in the wrong order.

bool HomogeneityTet::resolveFaceFacetCoincidences(
				 unsigned int face,
				 LooseEndSet &looseEnds,
				 const std::vector<FaceFacetEdgeSet> &edgeEdges)
{
  // Divide start and end points in the LooseEndMaps into groups,
  // where the maximum distance between points in a group is less than
  // a voxel side length.  We don't expect coincidences to affect
  // points more than a fraction of a pixel apart.

#ifdef DEBUG
  if(verboseface) {
    oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: face=" << face
	    << " nLooseEnds=" << looseEnds.size() << std::endl;
  }
  OOFcerrIndent indent(2);
#endif // DEBUG

  // IntersectionGroups are created in order moving around the face.
  // Store them in a vector to preserve that order.
  std::vector<IntersectionGroup> intersectionGroups;
  intersectionGroups.reserve(looseEnds.size());
  for(FaceEdgeIntersection *fei : looseEnds) {
    const Coord3D loc = fei->corner()->location3D();
    bool found = false;
    for(IntersectionGroup &grp : intersectionGroups) {
      if(grp.nearby(loc)) {
	grp.addIntersection(fei);
	found = true;
	break;
      }
    }
    if(!found) {
      // Create a new IntersectionGroup at loc
      intersectionGroups.emplace_back(loc, fei, face);
    }
  } // end loop over loose ends

  bool didSomething = false;
  
  for(IntersectionGroup &ig : intersectionGroups) {
#ifdef DEBUG
    if(verboseface) {
      oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: ig="
	      << std::endl;
      OOFcerrIndent indent(2);
      std::cerr << ig << std::endl;
    }
#endif // DEBUG
    if(ig.size() > 1) {
      ig.sortByPositionAndEdge();
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences:"
		<< " calling removeEquivPts" << std::endl;
      }
#endif // DEBUG
      if(ig.removeEquivPts(this, face, looseEnds)) {
	// The modifiers can merge points, thereby changing equivalence
	// classes, so it's possible that positions have changed. Re-sort.
	ig.sortByPositionAndEdge();
	didSomething = true;
      }
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: "
		<< "after removeEquivPts, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG
      if(ig.size() <= 1)
	continue;
// #ifdef DEBUG
//       if(verboseface)
// 	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: calling fixTents"
// 		<< std::endl;
// #endif // DEBUG
      if(ig.fixTents(this, face, looseEnds)) {
	ig.sortByPositionAndEdge();
	if(ig.removeEquivPts(this, face, looseEnds))
	  ig.sortByPositionAndEdge();
	didSomething = true;
      }
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: "
		<< "after fixTents, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG
      if(ig.size() <= 1)
	continue;
#ifdef DEBUG
      if(verboseface)
	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: "
		<< "calling fixCrossings" << std::endl;
#endif // DEBUG
      if(ig.fixCrossings(this, face, looseEnds)) {
	ig.sortByPositionAndEdge();
	if(ig.removeEquivPts(this, face, looseEnds))
	  ig.sortByPositionAndEdge();
	didSomething = true;
      }
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: "
		<< "after fixCrossings, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG
      if(ig.size() <= 1)
	continue;

#ifdef DEBUG
      if(verboseface)
	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: "
		<< "calling fixOccupiedEdges" << std::endl;
#endif // DEBUG
      if(ig.fixOccupiedEdges(this, face, looseEnds, edgeEdges)) {
	didSomething = true;
      }

								 
// #ifdef DEBUG
//       if(verboseface) {
// 	oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: "
// 		<< "after fixOccupiedEdges, ig=" << std::endl;
// 	OOFcerrIndent indent(2);
// 	std::cerr << ig << std::endl;
//       }
// #endif // DEBUG

      // ig.sortByPositionAndEdge();
      // ig.checkOrdering(this, face, looseEnds);

    } // end if ig.size() > 1
    
// #ifdef DEBUG
//     if(verboseface)
//       oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: done with ig"
// 	      << std::endl;
// #endif // DEBUG
  }
#ifdef DEBUG
  if(verboseface)
    oofcerr << "HomogeneityTet::resolveFaceFacetCoincidences: "
	    << "done, didSomething =" << didSomething << std::endl;
#endif // DEBUG

  return didSomething;
} // end HomogeneityTet::resolveFaceFacetCoincidences


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double HomogeneityTet::intersectionVolume(const FacetMap2D &planeFacets,
					  const FaceFacets &faceFacets
// #ifdef DEBUG
// 					  , unsigned int cat,
// 					  std::ostream &output
// #endif // DEBUG
					  )
{
// #ifdef DEBUG
//   if(verbosecategory)
//     oofcerr << "HomogeneityTet::intersectionVolume: tetcenter=" << tetCenter
// 	    << std::endl;
// #endif // DEBUG
  double vol = 0.0;
  // Get volume contribution from pixel plane facets.
  for(FacetMap2D::const_iterator fm=planeFacets.begin(); fm!=planeFacets.end();
      ++fm)
    {
      const HPixelPlane *pixplane = (*fm).first;
      const PixelPlaneFacet *facet = (*fm).second;
      if(!facet->empty()) {
	double dv = (1./3.)*(facet->area() * pixplane->normalSign() *
		     (pixplane->normalOffset() -
		      tetCenter[pixplane->direction()]));
// #ifdef DEBUG
// 	if(verbose) {
// 	  oofcerr << "HomogeneityTet::intersectionVolume: pixel plane facet:"
// 		  // << " category=" << cat
// 		  << " pixel plane=" << *facet->pixplane
// 		  << " area=" << facet->area()
// 		  << " dv=" << dv << std::endl;
// 	  // writeDebugFile(to_string(*facet) + "\n");
// 	}
// #endif	// DEBUG
	vol += dv;
      }
    }

  // Get volume contribution from tet face facets.
  for(unsigned int f=0; f<NUM_TET_FACES; f++) {
    if(coincidentPixelPlanes[f] == nullptr && !faceFacets[f].empty()) {
      Coord3D area = faceFacets[f].area(this);
      double dv = dot(area, faceCenters[f]-tetCenter)/3.0;
// #ifdef DEBUG
//       if(verbose) {
// 	Coord3D facenorm = faceAreaVectors[f]/sqrt(norm2(faceAreaVectors[f]));
// 	oofcerr << "HomogeneityTet::intersectionVolume: face facet:"
// 		// << "category=" << cat
// 		<< " face=" << f
// 		<< " area=" << area
// 		<< " " << dot(area, facenorm)
// 		<< " dv=" << dv << std::endl;
// 	// writeDebugFile(to_string(faceFacets[f]) + "\n");
//       }
// #endif	// DEBUG
      vol += dv;
    }
  }
  return vol;
} // end HomogeneityTet::intersectionVolume

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Debugging routines for intersection equivalence classes.

#ifdef DEBUG
std::set<PlaneIntersection*> HomogeneityTet::allIntersections;

bool HomogeneityTet::verify() {
  for(IsecEquivalenceClass *eqclass : equivalences) {
    // if(verbose)
    //   oofcerr << "HomogeneityTet::verify: checking class " << eqclass
    // 	      << std::endl;
    if(!eqclass->verify())
      return false;
  }
  for(PlaneIntersection* pi : allIntersections) {
    // if(verbose)
    //   oofcerr << "HomogeneityTet::verify: checking point " << *pi
    // 	      << std::endl;
    if(!pi->verify())
      return false;
  }
  // if(verbose)
  //   oofcerr << "HomogeneityTet::verify: done!" << std::endl;
  return true;
}

void HomogeneityTet::dumpEquivalences() {
  if(equivalences.empty())
    oofcerr << "HomogeneityTet::dumpEquivalences: (none)" << std::endl;
  else
    for(IsecEquivalenceClass *eqclass : equivalences) {
      eqclass->dump();
    }
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Given a PlaneIntersection and a tet face, compute which edge of the
// face it's on and how far along the edge.
void HomogeneityTet::findFaceEdge(PlaneIntersection *pt, unsigned int face,
				  unsigned int &faceEdge, EdgePosition &t)
{
  // findFaceEdge uses topological information about intersections and
  // faces, not numerical information about positions.
  faceEdge = pt->findFaceEdge(face, this);
  if(faceEdge != NONE) {
    BarycentricCoord b = getBarycentricCoord(pt->location3D());
    t = faceEdgeCoord(b, face, faceEdge);
    t.normalize();
  }
}

