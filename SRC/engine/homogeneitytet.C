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
#include "common/segintersection.h"
#include "common/tostring.h"
#include "engine/cskeletonelement.h"
#include "engine/homogeneitytet.h"
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

void setVerboseFace(unsigned int face) {
  oofcerr << "setVerboseFace: " << face << std::endl;
  vfaces.insert(face);
}

void setVerboseAllFaces() {
  for(unsigned int f=0; f<4; f++)
    vfaces.insert(f);
}

bool HomogeneityTet::verboseFace_(bool vrbse, unsigned int face) const {
  return vrbse && (vfaces.empty() || vfaces.count(face) == 1);
}

#ifdef FINDFACEFACETS_OLD
void HomogeneityTet::printLooseEnds(unsigned int e, const LooseEndMap &lem)
  const
{
  if(!lem.empty()) {
    double lastpos = 0.0;
    LooseEndMap::const_iterator x = lem.begin();
    while(x != lem.end()) {
      auto range = lem.equal_range((*x).first);
      oofcerr << "HomogeneityTet::printLooseEnds: edge=" << e
	      << " t=" << (*x).first
	      << " delta=" << (*x).first - lastpos << std::endl;
      lastpos = (*x).first;
      OOFcerrIndent indent(2);
      for(LooseEndMap::const_iterator y=range.first; y!=range.second; ++y)
	oofcerr << "HomogeneityTet::printLooseEnds: " << (*y).second
		<< std::endl;
      x = range.second;
    }
  }
  else
    oofcerr << "HomogeneityTet::printLooseEnds: edge=" << e << ": (none)"
	    << std::endl;
}
#endif // FINDFACEFACETS_OLD

void printLooseEnds(const LooseEndSet &le) {
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

static void getEdgeNodes(unsigned int faceIndex, unsigned int edgeIndex,
			 unsigned int &inode0, unsigned int &inode1)
{
  assert(edgeIndex < NUM_TET_FACE_EDGES);
  assert(faceIndex < NUM_TET_FACES);
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

    // A more symmetric but more expensive expression for the area is
    // 0.5*(pt0%pt1 + pt1%pt2 + pt2%pt0).
    faceAreaVectors[f] = 0.5*((pt1 - pt0) % (pt2 - pt0));
    faceCenters[f] = (pt0 + pt1 + pt2)/3.0;

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
#ifdef DEBUG
  if(verbose)
    oofcerr << "HomogeneityTet::ctor: looking for collinear planes"
	    << std::endl;
#endif // DEBUG
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
	  if(i != j && planes[i]->unoriented() != planes[j]->unoriented())
	    {
	      for(unsigned int k=0; k<planes.size(); k++) {
		if(k != i && k != j &&
		   planes[k]->unoriented() != planes[i]->unoriented() &&
		   planes[k]->unoriented() != planes[j]->unoriented())
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

const HPixelPlane *HomogeneityTet::getPixelPlane(unsigned int dir, int offset,
						int normal)
{
  return getPixelPlane(new HPixelPlane(dir, offset, normal));
}

const HPixelPlane *HomogeneityTet::getPixelPlane(HPixelPlane *pixplane) {
  auto result = pixelPlanes_.emplace(pixplane);
  if(!result.second)
    delete pixplane;
  else
    allPlanes_.insert(*result.first);
  (*result.first)->setUnoriented(getUnorientedPixelPlane(*result.first));
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
    delete oplane;
  else
    allPlanes_.insert(*p.first);
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

  if(!verify()) {
    oofcerr << "HomogeneityTet::mergeEquiv:"
	    << " verification failed at beginning of mergeEquiv" << std::endl;
    throw ErrProgrammingError("Verification failed before mergeEquiv!",
			      __FILE__, __LINE__);
  }
  OOFcerrIndent indent(2);
#endif // DEBUG
  
  IsecEquivalenceClass *equivClass0 = point0->equivalence();
  IsecEquivalenceClass *equivClass1 = point1->equivalence();

  if(equivClass0 == nullptr) {
    if(equivClass1 == nullptr) {
      // Neither point is in an equivalence class.  Construct one.
      IsecEquivalenceClass *eqclass = new IsecEquivalenceClass(
					       merged, nextEquivalenceID()
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
      }
      else {
	// The points are in different equivalence classes.  Merge the classes.
// #ifdef DEBUG
// 	if(verboseplane) {
// 	  oofcerr << "HomogeneityTet::mergeEquiv: merging classes" << std::endl;
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
      }
    }
  }
#ifdef DEBUG
  if(!verify())
    throw ErrProgrammingError("Verification failed after mergeEquiv!",
			      __FILE__, __LINE__);
#endif // DEBUG
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
					       pt0, nextEquivalenceID()
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
#ifdef DEBUG
  if(verboseplane || verboseface) 
    oofcerr << "HomogeneityTet::checkEquiv: point=" << point << " " << *point
	    << " verboseplane=" << verboseplane
	    << " verboseface=" << verboseface << std::endl;
  OOFcerrIndent indent(2);
#endif // DEBUG

  bool foundEquiv = true;
  while(foundEquiv == true) {
    foundEquiv = false;
    for(IsecEquivalenceClass *eqclass : equivalences) {
      if(point->equivalence() != eqclass) {
	if(point->belongsInEqClass(eqclass)) {
	  foundEquiv = true;
	  IsecEquivalenceClass *oldclass = point->equivalence();
#ifdef DEBUG
	  if(verboseplane || verboseplane)
	    oofcerr << "HomogeneityTet::checkEquiv: found eqclass "
		    << *eqclass << std::endl;
#endif // DEBUG
	  if(oldclass != nullptr) {
	    // Since point is in oldclass, calling merge will call
	    // point->setEquivalence(eqclass).
#ifdef DEBUG
	    if(verboseplane || verboseface)
	      oofcerr << "HomogeneityTet::checkEquiv: merging oldclass="
		      << *oldclass << std::endl;
#endif // DEBUG
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
      }
    } // end loop over equivalence classes eqclass
  }
  if(point->equivalence() == nullptr) {
    // The point doesn't belong to any existing equivalence class.
    // Create one, so that other points can be made equivalent to it.
#ifdef DEBUG
    if(verboseplane || verboseface)
      oofcerr << "HomogeneityTet::checkEquiv: creating new class." << std::endl;
#endif // DEBUG
    IsecEquivalenceClass *eqclass = new IsecEquivalenceClass(
					     point, nextEquivalenceID()
#ifdef DEBUG
					     , verboseplane || verboseface
#endif // DEBUG
							     );
    equivalences.push_back(eqclass);
    point->setEquivalence(eqclass);
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "HomogeneityTet::checkEquiv: new class=" << *eqclass
// 	      << std::endl;
// #endif // DEBUG
  }
  return point;
} // end HomogeneityTet::checkEquiv

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

double HomogeneityTet::edgeCoord(const BarycentricCoord &bint,
				 unsigned int edgeno,
				 const PixelPlaneFacet *facet)
  const
{
// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::edgeCoord: bint=" << bint << " face=" << *face
// 	    << " facet=" << *facet << std::endl;
//   }
// #endif	// DEBUG

  // unsigned int edgeno = facet->getPolyEdge(face);

// #ifdef DEBUG
//   if(edgeno == NONE) {
//     oofcerr << "HomogeneityTet::edgeCoord: edgeno==NONE! face=" << *face
// 	    << std::endl;
//     oofcerr << "HomogeneityTet::edgeCoord: facet=" << *facet << std::endl;
//     throw ErrProgrammingError("HomogeneityTet::edgeCoord: bad edgeno!",
// 			      __FILE__, __LINE__);
//   }
// #endif // DEBUG
  
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
//     oofcerr << "HomogeneityTet::edgeCoord: b0=" << b0 << " b1=" << b1
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
  for(unsigned int i=0; i<4; i++) {
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
  // if(verboseplane)
  //   oofcerr << "HomogeneityTet::edgeCoord: best=" << best << std::endl;
#endif // DEBUG

  double alpha = (bint[best] - b0[best])/(b1[best] - b0[best]);
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::edgeCoord: alpha=" << alpha << std::endl;
// #endif // DEBUG
  return alpha;
}

// Return the fractional position of the given point along the given
// edge of the given tet face.
double HomogeneityTet::faceEdgeCoord(const BarycentricCoord &bary,
				     unsigned int face, unsigned int edge)
  const
{
  // Get the nodes at the ends of the tet edge.
  unsigned int n0, n1;
  getEdgeNodes(face, edge, n0, n1);
  // If bary is really on the edge between nodes n0 and n1, then
  // bary[n0] = 1-alpha and bary[n1] = alpha, where alpha is the
  // fractional position, so we could get alpha in two ways.  Average
  // them.
  return 0.5*(1. - bary[n0] + bary[n1]);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the points at which the edges of the tetrahedron intersect the
// given pixel plane. 

TetIntersectionPolygon&
HomogeneityTet::getTetPlaneIntersectionPoints(const HPixelPlane *pixplane) {
#ifdef DEBUG
  if(verboseCategory())
    oofcerr << "HomogeneityTet::getTetPlaneIntersectionPoints: pixplane="
	    << pixplane << " " << *pixplane << std::endl;
#endif // DEBUG
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
  throw ErrProgrammingError("nonIntegerInteriorPt failed!", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FacetMap2D HomogeneityTet::findPixelPlaneFacets(unsigned int cat,
						const VoxelSetBoundary &vsb)
{
#ifdef DEBUG
  verbosecategory = verboseCategory_(verbose, cat);
#endif // DEBUG
  FacetMap2D facets;		// typedef in pixelplanefacet.h

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
      doFindPixelPlaneFacets(cat, pixplane, loops, f, facets);
#ifdef DEBUG
      verboseplane = false;
#endif  // DEBUG
    }
  }
#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findPixelPlaneFacets: done with face planes"
	    << std::endl;
  }
#endif // DEBUG

  // TODO: coincidentPixelPlanes and coincidentFacePlanes store the
  // unoriented pixel planes, which means that if a VSB uses both
  // orientations of a plane, and one of them is coincident with a
  // face, the other one won't be used.
  //
  // For purposes of comparing intersection positions, it makes sense
  // to use the unoriented planes.  For deciding if a plane has
  // already been computed or if it's coincident with a face, use the
  // oriented planes.

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
	doFindPixelPlaneFacets(cat, pixplane, loops, /*face=*/NONE, facets);
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
  TetIntersectionPolygon &tetPts = getTetPlaneIntersectionPoints(pixplane);
  unsigned int nn = tetPts.size();

  if(nn < 3) {
#ifdef DEBUG
    if(verboseplane) 
      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: no intersection! nn="
	      << nn << " pixplane=" << *pixplane << std::endl;
#endif // DEBUG
    return;
  }
  assert(nn == 3 || nn == 4);

#ifdef DEBUG
  if(verboseplane) {
    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: pixplane=" << *pixplane
  	    << " category=" << cat << std::endl;
    if(!tetPts.empty()) {
      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: tetPts="
	      << std::endl;
      for(const TetIntersection *pt : tetPts)
	oofcerr << "HomogeneityTet::doFindPixelPlaneFacets:    " << *pt
		<< std::endl;
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
	continue;
      }
// #ifdef DEBUG
//       if(verboseplane)
//         oofcerr << "doFindPixelPlaneFacets: examining loop " << *loop
// 		<< std::endl;
// #endif // DEBUG

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
	  // pixel plane that contains the segment, and the orthogonal
	  // plane that contains the previous segment or the next one.
	  HPixelPlane *orthoPlanePrev =
	    pixplane->orthogonalPlane(pbs_prev, pbs_start);
	  HPixelPlane *orthoPlane =
	    pixplane->orthogonalPlane(pbs_start, pbs_end);
	  HPixelPlane *orthoPlaneNext =
	    pixplane->orthogonalPlane(pbs_end, pbs_next);
	  // Get the pointers to the reference versions of the planes,
	  // so that pointer comparisons can be used later.
	  // TODO: Instead of calling PixelPlane::orthogonalPlane
	  // and HomogeneityTet::getPixelPlane, combine them into
	  // HomogeneityTet::getOrthogonalPlane.
	  const HPixelPlane *prevPlanePtr = getPixelPlane(orthoPlanePrev);
	  const HPixelPlane *orthoPlanePtr = getPixelPlane(orthoPlane);
	  const HPixelPlane *nextPlanePtr = getPixelPlane(orthoPlaneNext);
	  facet->addEdge(new PixelFacetEdge(
	    checkEquiv(new TriplePixelPlaneIntersection(
				this, pixplane, prevPlanePtr, orthoPlanePtr)),
	    checkEquiv(new TriplePixelPlaneIntersection(
				this, pixplane, orthoPlanePtr, nextPlanePtr))));

	} // end if the segment is entirely inside the polygon

	else if(pbs_start_inside != pbs_end_inside) {
	  // If start and end are hetero-interior, so to speak, then
	  // there's one intersection. Find it.
	  HPixelPlane *orthoPlane =
	    pixplane->orthogonalPlane(pbs_start, pbs_end);
	  const HPixelPlane *orthoPlanePtr = getPixelPlane(orthoPlane);
	  unsigned int orthoFace = getCoincidentFaceIndex(orthoPlanePtr);
	  PixelPlaneIntersectionNR *pi = find_one_intersection(
						 pixplane,
						 orthoPlanePtr,
						 PixelBdyLoopSegment(loop, k),
						 onFace, orthoFace,
						 pbs_end_inside);
	  if(pbs_start_inside) {
	    HPixelPlane *orthoPlanePrev =
	      pixplane->orthogonalPlane(pbs_prev, pbs_start);
	    const HPixelPlane *prevPlanePtr = getPixelPlane(orthoPlanePrev);
	    facet->addEdge(new StopFaceIntersectionEdge(
		checkEquiv(new TriplePixelPlaneIntersection(
			    this, pixplane, prevPlanePtr, orthoPlanePtr)),
		checkEquiv(pi)));
	  }
	  else {
	    HPixelPlane *orthoPlaneNext = 
	      pixplane->orthogonalPlane(pbs_end, pbs_next);
	    const HPixelPlane *nextPlanePtr = getPixelPlane(orthoPlaneNext);
	    facet->addEdge(new StartFaceIntersectionEdge(
		 checkEquiv(pi),
		 checkEquiv(new TriplePixelPlaneIntersection(
			 this, pixplane, orthoPlanePtr, nextPlanePtr))));
	  }
	} // end if start and end are hetero-interior
	else {
	  // The current segment has both endpoints outside the
	  // polygon.  It must intersect zero or two times.
	  ICRectangle segbb(pbs_start, pbs_end);
	  if(segbb.intersects(tetBounds)) {
	    HPixelPlane *orthoPlane =
	      pixplane->orthogonalPlane(pbs_start, pbs_end);
	    // Since getTetPlaneIntersectionPoints looks up caches
	    // previous computations by PixelPlane pointer, get the
	    // HomogeneityTet's official version of the orthogonal
	    // plane.
	    const HPixelPlane *orthoPlanePtr = getPixelPlane(orthoPlane);
	    // There's no intersection unless the orthoPlane actually
	    // intersects the tetrahedron.  This check is important
	    // for consistency.  When a pixel plane coincides with a
	    // face, sometimes find_two_intersections will find
	    // intersections when getTetPlaneIntersectionPoints
	    // doesn't, and this can lead to unmatched facet edge
	    // endpoints.
	    TetIntersectionPolygon orthoPts =
	      getTetPlaneIntersectionPoints(orthoPlanePtr);
	    if(!orthoPts.empty()) {
	      unsigned int orthoFace = getCoincidentFaceIndex(orthoPlanePtr);
	      std::vector<PixelPlaneIntersectionNR*> isecs =
		find_two_intersections(pixplane,
				       orthoPlanePtr,
				       PixelBdyLoopSegment(loop, k),
				       onFace, orthoFace);
	      if(isecs.size() == 2) {
		facet->addEdge(new TwoFaceIntersectionEdge(
				   checkEquiv(isecs[0]), checkEquiv(isecs[1])));
	      }
	    } // end if the orthogonal plane intersects the tet
#ifdef DEBUG
	    else {
	      if(verboseplane) {
		oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
			<< "skipping find_two_intersections" << std::endl;
	      }
	    }
#endif // DEBUG

	  } // end if segment bbox intersects polygon bbox
	} // end if both segment endpoints are outside the polygon

	pbs_start_inside = pbs_end_inside;
	pbs_start_bary = pbs_end_bary;

#ifdef DEBUG
	if(!verify()) {
	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
		  << "verification failed!" << std::endl;
	  oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
		  << "facet=" << *facet << std::endl;
	  throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
	}
#endif // DEBUG
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

#ifdef DEBUG
  if(!verify()) {
    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
	    << "verification failed after completeLoops!" << std::endl;
    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: "
	    << "facet=" << *facet << std::endl;
    throw ErrProgrammingError("Verification failed after completeLoops!",
			      __FILE__, __LINE__);
  }
#endif // DEBUG

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
	// TetIntersection *t0 = tetPts[i]->clone();
	// TetIntersection *t1 = tetPts[i+1]->clone();
	// facet->addEdge(new PolygonEdge(t0, t1));
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
    else
      oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: cat=" << cat
	      << " pixel plane=" << *pixplane
	      << " final facet is empty"
	      << std::endl;
  }
  if(!verify()) {
    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: cat=" << cat
	    << " pixel plane=" << *pixplane
	    << " verification failed!" << std::endl;
    throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
  }
#endif	// DEBUG
} // end HomogeneityTet::doFindPixelPlaneFacets

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the intersection of a pixel boundary loop segment with the
// tetrahedron, given a segment that's known to have just one endpoint
// inside the tet.  The only question is which face of the tet is
// crossed by the segment.  The segment is on the intersection of
// pixplane and orthoPlane.

PixelPlaneIntersectionNR *HomogeneityTet::find_one_intersection(
					const HPixelPlane *pixplane,
					const HPixelPlane *orthoPlane,
					const PixelBdyLoopSegment &pbls,
					unsigned int onFace,
					unsigned int orthoFace,
					bool entry)
{
  // Calculate the position of the intersection in a way that's
  // independent of the direction of the segment.
  ICoord2D interiorPt = entry ? pbls.secondPt() : pbls.firstPt();
  ICoord2D exteriorPt = entry ? pbls.firstPt() : pbls.secondPt();
  // Examining the barycentric coordinates of the points tells us
  // immediately which face the segment crosses.
  BarycentricCoord b0 = getBarycentricCoord(interiorPt, pixplane);
  BarycentricCoord b1 = getBarycentricCoord(exteriorPt, pixplane);

  BarycentricCoord interiorB, exteriorB;
  if(b0.interior(onFace)) {
    interiorB = b0;
    exteriorB = b1;
  }
  else {
    interiorB = b1;
    exteriorB = b0;
  }
  // Look at each face to see which face planes the segment crosses.
  // If it crosses more than one, the one closest to the interior
  // point of the PixelBdyLoopSegment is the real intersection.
  double bestAlpha = std::numeric_limits<double>::max();
  unsigned int bestFace = NONE;
  const FacePlane *collinearFace = nullptr;
  for(unsigned int n=0; n<NUM_TET_NODES; n++) {
    unsigned int face = CSkeletonElement::oppFace[n];
    // skip this face if it lies in the pixel plane or the orthogonal
    // plane or is collinear with them.
    if(onFace != face && orthoFace != face) {
      if(!areCollinear(pixplane, orthoPlane, getTetFacePlane(face))) {
	if(interiorB[n] > 0.0 && exteriorB[n] <= 0.0) {
	  // alpha is the fractional distance from interiorPt to exteriorPt.
	  double alpha = interiorB[n]/(interiorB[n] - exteriorB[n]);
	  if(alpha < bestAlpha) {
	    bestAlpha = alpha;
	    bestFace = face;
	  }
	}
      }
      else
	collinearFace = getTetFacePlane(face);
    }
  } // end loop over nodes/faces

  if(bestFace == NONE) {
    // No face crosses the segment.  The segment must lie along a face
    // (ie, pixplane and orthoPlane are collinear with at least one
    // tet face), and roundoff error has put one end of the segment
    // inside and one outside.  The intersection point can be chosen
    // to lie at any point on the segment, unless the segment extends
    // past the rim of the tet face.  Choose interiorPt because it
    // can't be past the rim.
    bestAlpha = 0;
  }
#ifdef DEBUG
  if(verboseplane) {
    oofcerr << "HomogeneityTet::find_one_intersection: pixplane=" << *pixplane
	    << " orthoPlane=" << *orthoPlane << " face=" << bestFace
	    << std::endl;
  }
#endif // DEBUG

  // newIntersection returns either a SimpleIntersection or a
  // MultiFaceIntersection, depending on whether or not orthoPlane is
  // also a tet face.
  PixelPlaneIntersectionNR *ppi =
    newIntersection(this, pixplane, orthoPlane, pbls,
		    entry ? 1-bestAlpha : bestAlpha,
		    bestFace,
		    entry ? ENTRY : EXIT);

  if(bestFace == NONE) {
    // Do the things that the SimpleIntersection or
    // MultiFaceIntersection constructor couldn't do because it was
    // called with faceIndex==NONE.
    ICoord3D loc = pixplane->convert2Coord3D(interiorPt);
    ppi->setLocation(pixplane->convert2Coord3D(interiorPt).coord());
    // The third plane for the intersection is the pixel plane at
    // interiorPt that isn't either pixplane or orthoPlane.
    unsigned int dir = 3 - pixplane->direction() - orthoPlane->direction();
    int offset = loc[dir];
    const HPixelPlane *pp = getPixelPlane(dir, offset, 1);
    pp->addToIntersection(ppi);
    ppi->includeCollinearPlanes(this);
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
					const HPixelPlane *pixplane,
					const HPixelPlane *orthoPlane,
					const PixelBdyLoopSegment &pblseg,
					unsigned int onFace,
					unsigned int orthoFace)
{
// #ifdef DEBUG
//   if(verboseplane)
//     oofcerr << "HomogeneityTet::find_two_intersections: pblseg=" << pblseg
// 	    << " onFace=" << onFace << " orthoFace=" << orthoFace
// 	    << " pixplane=" << *pixplane << " ortho=" << *orthoPlane
// 	    << std::endl;
// #endif	// DEBUG
  // The pixplane passed to find_two_intersections is the unoriented
  // one, so it can't be used to convert the 2D coords in pblseg to 3D.
  BarycentricCoord b0 = getBarycentricCoord(pblseg.firstPt(), pixplane);
  BarycentricCoord b1 = getBarycentricCoord(pblseg.secondPt(), pixplane);
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
  for(unsigned int n=0; n<NUM_TET_NODES; n++) {
    unsigned int face = CSkeletonElement::oppFace[n];
// #ifdef DEBUG
//     if(verboseplane) {
//       oofcerr << "HomogeneityTet::find_two_intersections: n=" << n
// 	      << " face=" << face << std::endl;
//     }
//     OOFcerrIndent indent(2);
// #endif // DEBUG
    // skip this face if it lies in the pixel plane or the orthoFace
    // or is collinear with them.
    if(face != onFace && face != orthoFace &&
       !areCollinear(pixplane, orthoPlane, getTetFacePlane(face)))
      {
	double b0n = b0[n];
	double b1n = b1[n];
// #ifdef DEBUG
//       if(verboseplane) {
// 	oofcerr << "HomogeneityTet::find_two_intersections: b0n=" << b0n
// 		<< " b1n=" << b1n << " b1n-b0n=" << b1n-b0n
// 		<< std::endl;
//       }
// #endif // DEBUG
	// Skip this face if the segment is parallel to it (b0n == b1n)
	// or if it doesn't cross it (b0n and b1n have the same sign).
	if(b0n != b1n && b0n*b1n <= 0) {
	  double alpha = b0n/(b0n - b1n);
	  if(b0n < b1n) {
	    // This is an entry point
	    if(alpha > entryAlpha) {
	      entryAlpha = alpha;
	      entryFace = face;
// #ifdef DEBUG
// 	    if(verboseplane)
// 	      oofcerr << "HomogeneityTet::find_two_intersections: alpha="
// 		      << alpha << " entryAlpha=" << entryAlpha << std::endl;
// #endif // DEBUG
	    }
	  }
	  else {
	    // This is an exit point.
	    if(alpha < exitAlpha) {
	      exitAlpha = alpha;
	      exitFace = face;
// #ifdef DEBUG
// 	    if(verboseplane)
// 	      oofcerr << "HomogeneityTet::find_two_intersections: alpha="
// 		      << alpha << " exitAlpha=" << exitAlpha << std::endl;
// #endif // DEBUG
	    }
	  }
	}
      } // end if f != onFace, etc
  }   // end loop over nodes f

// #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::find_two_intersections: entry face="
// 	    << entryFace << " alpha=" << entryAlpha
// 	    << "  exit face=" << exitFace << " alpha=" << exitAlpha
// 	    << std::endl;
//   }
// #endif // DEBUG
  std::vector<PixelPlaneIntersectionNR*> isecs;
  
  if(entryFace != NONE && exitFace != NONE &&
     entryAlpha <= exitAlpha &&
     ((entryAlpha >= 0.0 && entryAlpha <= 1.0) ||
      // TODO: old version had || instead of && ^ here, because
      // sometimes one of the alphas was just epsilon out of bounds
      // and the other was in bounds and we knew that there were two
      // intersections.
      (exitAlpha >= 0.0 && exitAlpha <= 1.0)))
    {
// #ifdef DEBUG
//       if(verboseplane) {
// 	oofcerr << "HomogeneityTet::find_two_intersections: pixplane="
// 		<< *pixplane << " orthoPlane=" << *orthoPlane
// 		<< " entryFace=" << entryFace << " exitFace=" << exitFace
// 		<< std::endl;
//       }
// #endif // DEBUG
      isecs.resize(2);
      isecs[0] = newIntersection(this, pixplane, orthoPlane, pblseg,
				 entryAlpha, entryFace, ENTRY);
      isecs[1] = newIntersection(this, pixplane, orthoPlane, pblseg,
				 exitAlpha, exitFace, EXIT);
#ifdef DEBUG
      isecs[0]->verbose = verboseplane;
      isecs[1]->verbose = verboseplane;
#endif // DEBUG
    }
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

// NEW findFaceFacets

FaceFacets HomogeneityTet::findFaceFacets(unsigned int cat,
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

  // // looseEndCatalog[f][e] is a LooseEndMap for edge e of face f.  It
  // // maps parametric positions along the edge to the
  // // FaceEdgeIntersection at that point.
  // LooseEndCatalog looseEndCatalog(NUM_TET_FACES,
  // 		    std::vector<LooseEndMap>(NUM_TET_FACE_EDGES));

  LooseEndCatalog looseEndCatalog(NUM_TET_FACES);
  std::vector<StrandedPoint> strandedPoints;

  // Loop over all faces that aren't also pixel planes.
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
  if(verbosecategory)
    oofcerr << "HomogeneityTet::findFaceFacets: back from matchStrandedPoints"
	    << std::endl;
#endif	// DEBUG
  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
    if(coincidentPixelPlanes[face] == nullptr) { // face is not a pixel plane
#ifdef DEBUG
      verboseface = verboseFace_(verbosecategory, face);
      if(verboseface)
	oofcerr << "HomogeneityTet::findFaceFacets: second loop over face "
		<< face << " category " << cat << std::endl;
      OOFcerrIndent indent(2);
#endif // DEBUG
      FaceFacet &facet = faceFacets[face];
      LooseEndSet &looseEnds = looseEndCatalog[face];
      Coord3D faceNormal = faceAreaVectors[face]; // not a unit vector

      // Put any marooned points onto the closest edge.
      for(StrandedPoint &sp : marooned[face]) {
	sp.feInt->forceOntoEdge(sp.face, this);
	looseEnds.insert(sp.feInt);
      }

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
		<< " before resolveCoincidences, looseEnds="
		<< std::endl;
	OOFcerrIndent indent(2);
	printLooseEnds(looseEnds);
      }
#endif // DEBUG
      resolveCoincidences(face, looseEnds, edgeEdges);
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets:"
		<< " after resolveCoincidences, looseEnds (unsorted)="
		<< std::endl;
	OOFcerrIndent indent(2);
	printLooseEnds(looseEnds);
      }
#endif // DEBUG

      if(!looseEnds.empty()) {
	// Put all the LooseEnds in a single vector, ordered by face
	// edge and position along the edge.
	std::vector<FaceEdgeIntersection*> sortedLooseEnds(
					 looseEndCatalog[face].begin(),
					 looseEndCatalog[face].end());
	std::sort(sortedLooseEnds.begin(), sortedLooseEnds.end(),
		  FaceEdgeIntersectionLT());
	unsigned int npts = sortedLooseEnds.size();
	
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
	    double lastT = 0;
	    unsigned int lastEdge = NONE;
	    for(auto *le : sortedLooseEnds) {
	      oofcerr << "HomogeneityTet::findFaceFacets: " << *le;
	      if(le->faceEdge() == lastEdge)
		oofcerr << " dt=" << le->edgePosition() - lastT;
	      lastT = le->edgePosition();
	      lastEdge = le->faceEdge();
	      oofcerr << std::endl;
	    }
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
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: done with face "
		<< face << std::endl;
      }
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
} // end HomogeneityTet::findFaceFacets

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
    // Construct FaceEdgeIntersection objects in-place.
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
//     for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++)
//       htet->printLooseEnds(i, looseEnds[i]);
//   }
// #endif // DEBUG

} // end FaceFacet::findLooseEnds

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// If there are stranded points, pair them up.  Stranded points arise
// when the intersection line of two perpendicular pixel planes nearly
// passes through a tet edge (to within round off error).  In that
// case, there will be intersection points on the two planes but on
// different faces, and because each point is only on one face, it
// won't be assigned to a tet edge.

// If there are no other pixel planes creating segments connecting
// to those points, they will be loose ends of each face facet, but
// they're not on tet edges, so they can't be joined by adding facet
// edges on the tet edges.  When the stranded points are paired,
// each point of each pair must be on a different tet face, and
// merging the pair produces a point on a tet edge (the edge shared
// by the two faces).  The new merged point can be inserted into the
// looseEndCatalog.

StrandedPointLists HomogeneityTet::matchStrandedPoints(
			       std::vector<StrandedPoint> &strandedPoints,
			       LooseEndCatalog &looseEndCatalog)
{
// #ifdef DEBUG
//   if(verbosecategory)
//     oofcerr << "HomogeneityTet::matchStrandedPoints: size="
// 	    << strandedPoints.size() << std::endl;
// #endif // DEBUG
  
  // Stranded intersection points that can't be matched are marooned.
  // The list of marooned points is returned.  StrandedPointsLists is
  // a vector of vectors of StrandedPoints, one for each tet face.
  StrandedPointLists marooned(NUM_TET_FACES);
  if(strandedPoints.empty())
    return marooned;
  
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
// #ifdef DEBUG
// 	if(verbosecategory) {
// 	  OOFcerrIndent indent(2);
// 	  oofcerr << "HomogeneityTet::matchStrandedPoints:  pt0=" << *pt0.feInt
// 		  << std::endl;
// 	  oofcerr << "HomogeneityTet::matchStrandedPoints: best=" << *pt1.feInt
// 		  << std::endl;
// 	}
// #endif // DEBUG
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
	// The merged point isn't in a FacetEdge, so it won't be
	// automatically deleted.  Store it for later deletion.
	extraPoints.insert(merged);
      }	// end if best is not NONE
      else {
	// No match found for point i
	marooned[pt0.face].push_back(pt0);
#ifdef DEBUG
	if(verbosecategory)
	  oofcerr << "HomogeneityTet::matchStrandedPoints: marooned point! "
		  << pt0.feInt << std::endl;
#endif // DEBUG
      }
    } // end if point i hasn't been matched
  }   // end loop over stranded points i

  return marooned;
} // end HomogeneityTet::matchStrandedPoints

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO: Put IntersectionGroup in a separate file.

//enum GroupClassification {CORRECT, AMBIGUOUS, INCORRECT, UNKNOWN};
// enum IsecGroupOrdering {STARTSTART, ENDEND, STARTEND, ENDSTART, AMBIGUOUS};

#define CLOSEBY 0.3
#define CLOSEBY2 (CLOSEBY*CLOSEBY)

// IntersectionGroup is a group of FaceEdgeIntersections that are
// close to one another on the edges of a tet face.  The group may
// include intersections that are supposed to coincide exactly, but
// don't due to round off error.

class IntersectionGroup {
private:
  Coord3D location;
  // GroupClassification isectype;
  std::vector<FaceEdgeIntersection*> isecs;
  unsigned int face;
  bool tentCheck(HomogeneityTet*, unsigned int, PlaneIntersection*,
		 FaceEdgeIntersection*, FaceEdgeIntersection*) const;
  void eraseMatched(const std::vector<bool>&, LooseEndSet&);
public:
  IntersectionGroup(const Coord3D loc, FaceEdgeIntersection *fei,
		    unsigned int f)
    : location(loc),
      // isectype(CORRECT),
      face(f)
  {
    isecs.push_back(fei);
  }
  void addIntersection(FaceEdgeIntersection *fei) {
    isecs.push_back(fei);
    // isectype = UNKNOWN;
  }
  bool nearby(const Coord3D &where) const {
    return (norm2(where-location) < CLOSEBY2);
  }

  void sortByPositionAndEdge();

  void removeEquivPts(HomogeneityTet*, unsigned int, LooseEndSet&);
  void fixCrossings(HomogeneityTet*, unsigned int, LooseEndSet&);
  void fixOccupiedEdges(HomogeneityTet*, unsigned int, LooseEndSet&,
			const std::vector<FaceFacetEdgeSet>&);
  void fixTents(HomogeneityTet*, unsigned int, LooseEndSet&);
  void checkOrdering(HomogeneityTet*, unsigned int, std::vector<LooseEndMap>&);
  bool empty() const { return isecs.empty(); }
  unsigned int size() const { return isecs.size(); }
  friend class HomogeneityTet;
  friend std::ostream &operator<<(std::ostream&, const IntersectionGroup&);
};
#undef CLOSEBY2
#undef CLOSEBY

std::ostream &operator<<(std::ostream &os, const IntersectionGroup &ig) {
  double lastT = 0;
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
  std::sort(isecs.begin(), isecs.end(), FaceEdgeIntersectionLT());
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
// 		  oofcerr << "IntersectionGroup::fixTents: tentCheck returned T"
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
// 		  oofcerr << "IntersectionGroup::fixTents: tentCheck returned F"
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
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::tentCheck" << std::endl;
  OOFcerrIndent indent(2);
#endif // DEBUG
  
  // The two intersection points comprise a start and an end, are on
  // the same edge of the face, and the FaceFacetEdges that they're on
  // meet at their far ends.  This means that we know the order in
  // which the intersection points should appear on the tet face
  // perimeter.  Return true if the order is correct.
	      
  // TODO: Do this calculation for points on different tet
  // face edges too.
  Coord3D faceNormal = htet->faceAreaVector(face); // not unit vec
  const PlaneIntersection *pt0 = fei0->corner();
  const PlaneIntersection *pt1 = fei1->corner();
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::tentCheck: pt0=" << *pt0 << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: pt1=" << *pt1 << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: ptX=" << *ptX << std::endl;
  }
#endif // DEBUG
  const FacePlane *thisFacePtr = htet->getTetFacePlane(face);
  // pt0 and pt1 are on the same tet edge, so they share
  // two faces.  otherFace is the other face.
  const FacePlane *otherFacePtr = pt0->sharedFace(pt1, thisFacePtr);
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
  unsigned int n1 = vtkTetra::GetFaceArray(face)[(faceEdge+1)%3];
  // TODO: Add a table to CSkeletonElement that maps pairs of face
  // indices to pairs of node indices, and skip the previous 4 lines.

#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::tentCheck: face=" << face
	    << " otherFace=" << otherFace << " tetEdge=" << tetEdge
	    << " faceEdge=" << faceEdge
	    << " n0=" << n0 << " n1=" << n1 << std::endl;
#endif // DEBUG
  
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

  // Find the vectors in the directions of the edges from pt0 and pt1
  // to ptX.  *Don't* just use the positions of those points, since
  // that'll be susceptible to round off error in exactly the
  // situations in which this calculation is important.  Use the
  // topological information instead.  If sharedPixelPlane returns
  // nullptr, it means that the points are connected along a tet face
  // and not a pixel plane, and this check is irrelevant.
  const PixelPlane *pp0 = pt0->sharedPixelPlane(ptX, face);
  if(pp0 == nullptr)
    return true;
  const PixelPlane *pp1 = pt1->sharedPixelPlane(ptX, face);
  if(pp1 == nullptr)
    return true;
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::tentCheck: pp0=" << *pp0 << " pp1=" << *pp1
	    << std::endl;
#endif // DEBUG

  // TODO: These vectors may have the wrong sign because the
  // PixelPlanes stored in PlaneIntersections are unoriented.
  Coord3D edgeVec0 = cross(pp0->normal(), faceNormal);
  Coord3D edgeVec1 = cross(pp1->normal(), faceNormal);

  double dot0 = dot(edgeVec0, Eperp);
  double dot1 = dot(edgeVec1, Eperp);
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::tentCheck: edgeVec0=" << edgeVec0
	    << " edgeVec1=" << edgeVec1 << " Eperp=" << Eperp
	    << std::endl;
    oofcerr << "IntersectionGroup::tentCheck: dot0=" << dot0 << " dot1="
	    << dot1 << std::endl;
  }
#endif // DEBUG
  // If feiN is a start point, then the vector along the edge feiN,ptX
  // must go towards the interior of the face, and must have a
  // positive dot product with Eperp.  If it's an end point, the dot
  // product must be negative.  But if the dot product is zero,
  // postpone the decision.
  if((dot0 > 0 && !fei0->start()) || (dot0 < 0 && fei0->start()) ||
     (dot1 > 0 && !fei1->start()) || (dot1 < 0 && fei1->start()))
    {
#ifdef DEBUG
      if(htet->verboseFace())
	oofcerr << "IntersectionGroup::tentCheck: dot check failed"
		<< std::endl;
#endif // DEBUG
      return false;
    }
  

  // Normalize the edgeVecs.
  edgeVec0 /= sqrt(norm2(edgeVec0));
  edgeVec1 /= sqrt(norm2(edgeVec1));

  double dotSum = dot(edgeVec0 + edgeVec1, E);

#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::tentCheck: dotSum=" << dotSum << std::endl;
#endif // DEBUG
  if(dotSum > 0) {
    // The segment that goes from ptX to the tet edge must intersect
    // the edge after the other edge.  Return true if it does, false
    // otherwise.
    if(fei0->start()) {
      // The segment at fei0 starts on the edge and ends at ptX.  fei1
      // must be after fei0.
#ifdef DEBUG
      if(htet->verboseFace())
	oofcerr << "IntersectionGroup::tentCheck: case A: "
		<< fei0->edgePosition() << " " <<  fei1->edgePosition()
		<< std::endl;
#endif // DEBUG      
      return fei1->edgePosition() > fei0->edgePosition();
    }
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "IntersectionGroup::tentCheck: case B: "
	      << fei0->edgePosition() << " " <<  fei1->edgePosition()
	      << std::endl;
#endif // DEBUG      
    return fei1->edgePosition() < fei0->edgePosition();
  }
  else if(dotSum < 0) {
    // The segment that goes from the tet edge to ptX must intersect
    // the edge after he other edge.  Return true if it does, false
    // otherwise.
    if(fei0->start()) {
      // fei0 must be after fei1.
#ifdef DEBUG
      if(htet->verboseFace())
	oofcerr << "IntersectionGroup::tentCheck: case C: "
		<< fei0->edgePosition() << " " <<  fei1->edgePosition()
		<< std::endl;
#endif // DEBUG      
      return fei0->edgePosition() > fei1->edgePosition();
    }
#ifdef DEBUG
    if(htet->verboseFace())
      oofcerr << "IntersectionGroup::tentCheck: case D: "
	      << fei0->edgePosition() << " " <<  fei1->edgePosition()
	      << std::endl;
#endif // DEBUG      
    return fei0->edgePosition() < fei1->edgePosition();
  }
  // dotSum == 0.  The two segments from ptX are antiparallel, or both
  // are parallel to the tet edge.  If they're antiparallel, their
  // other ends must be coincident, and we should return false so that
  // they'll be merged.  If the segments are parallel to the tet edge,
  // but one end is on the edge (fei0 or fei1) and the other is
  // interior (ptX), everything is inconsistent and must be due to
  // round-off error.  Again, return false.
  return false;
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
  // are loose ends, but the order of starts and end along the edge is
  // start-start-end-end, and the points can't be paired. Note that A
  // and a need not be loose ends.  Also, b must not be joined to C
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
      double tC = xprev->edgePosition();
      double tb = x->edgePosition();
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
	    double tA =
	      htet->faceEdgeCoord(edge->startPt()->baryCoord(htet), face, e);
	    double ta =
	      htet->faceEdgeCoord(edge->endPt()->baryCoord(htet), face, e);
	    if(tA < tC && tC < ta && tA < tb && tb < ta) {
	      // Cb lies inside Aa on the edge of the tet face.
	      // Remove x and xprev (ie C and b) from the loose end
	      // set, merge their equivalence classes, and set up the
	      // next iteration.
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
#ifdef DEBUG
    if(htet->verboseFace()) {
      oofcerr << "IntersectionGroup::fixOccupiedEdges: deleting "
	      << nDeleted << " intersections" << std::endl;
    }
#endif // DEBUG
    unsigned int n = 0;
    for(unsigned int i=0; i<isecs.size(); i++) {
      if(!deleteMe[i])
	isecs[n++] = isecs[i];
    }
    isecs.resize(isecs.size() - nDeleted);
#ifdef DEBUG
    if(htet->verboseFace()) {
      oofcerr << "IntersectionGroup::fixOccupiedEdges: done deleting"
	      << std::endl;
    }
#endif // DEBUG
  }
}

// void IntersectionGroup::fixOrdering(HomogeneityTet *htet,
// 				    unsigned int face,
// 				    LooseEndSet &looseEnds)
// {
//   // Check that starts and ends alternate properly, and remove
//   // intersections if they don't.  When fixOrdering is called, the
//   // points in isecs are guaranteed not to coincide and the segments
//   // ending on the points are guaranteed not to cross each other.
  
//   if(size() <= 2)
//     return;
  
//   // misordered[i] is true if isecs[i-1] and isecs[i] are both starts
//   // or both ends.
//   std::vector<bool> misordered(isecs.size(), false);
//   unsigned int nStarts = 0;
//   unsigned int nEnds = 0;
//   int diff = nStarts - nEnds;
//   if(diff > 1 || diff < -1) {
//     oofcerr << "IntersectionGroup::fixOrdering: nStarts=" << nStarts
// 	    << " nEnds=" << nEnds << std::endl;
//     throw ErrProgrammingError("fixOrdering failed!", __FILE__, __LINE__);
//   }
//   bool ok = true;
//   for(unsigned int i=0; i<size(); i++) {
//     if(isecs[i]->start())
//       nStarts++;
//     else
//       nEnds++;
//     if(i > 0 && isecs[i]->start() != isecs[i-1]->start()) {
//       misordered[i] = true;
//       ok = false;
//     }
//   }
//   if(!ok)
//     return;
// }

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

  if(size() <= 1)
    return;

  // firstXing is the first segment in the group that crosses another
  // segment in the group.
  unsigned int firstXing = NONE;
  // tempXing is the segment that crosses firstXing.
  unsigned int tempXing = NONE;
  // Find the first segment that crosses any other
  for(unsigned int i=0; i<isecs.size()-1 && firstXing==NONE; i++) {
    for(unsigned int j=i+1; j<isecs.size(); j++) {
      if(isecs[i]->crosses(isecs[j], face, htet
#ifdef DEBUG
			   , htet->verboseFace()
#endif // DEBUG
			   ))
	{
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
  if(firstXing == NONE)
    return;

  // Find the last segment that crosses any other.  It's either
  // tempXing or later, because tempXing > firstXing and tempXing
  // crosses another segment (firstXing).
  unsigned int lastXing = NONE;
  for(unsigned int i=isecs.size()-1; i>tempXing && lastXing==NONE; i--) {
    for(unsigned int j=0; j<i; j++) {
      if(isecs[i]->crosses(isecs[j], face, htet
#ifdef DEBUG
			   , htet->verboseFace()
#endif // DEBUG
			   ))
	{
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

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::fixCrossings: lastXing=" << lastXing
	    << std::endl;
  }
#endif // DEBUG

  // Make a new GenericIntersection merging the planes of all of the
  // original intersections.
  GenericIntersection *newPt = new GenericIntersection(htet);
  htet->extraPoints.insert(newPt);
  for(unsigned int i=firstXing; i<lastXing+1; i++) {
    isecs[i]->corner()->copyPlanesToIntersection(newPt);
  }
  htet->checkEquiv(newPt);	// merges equivalence classees
  newPt->computeLocation();
  // Find out where newPt is on the face.
  double newT = -1;
  unsigned int newEdge = NONE;
  htet->findFaceEdge(newPt, face, newEdge, newT); // computes newEdge, newT

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "IntersectionGroup::fixCrossings: newPt=" << *newPt << std::endl;
  }
#endif // DEBUG

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
#ifdef DEBUG
  if(htet->verboseFace())
    oofcerr << "IntersectionGroup::fixCrossings: keepStarts=" << keepStarts
	    << " keepEnds=" << keepEnds << std::endl;
#endif // DEBUG
  unsigned int startCount = 0;	// number of start points already kept
  unsigned int endCount = 0;
  std::vector<FaceEdgeIntersection*> newIsecs;
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
  isecs = newIsecs;
} // end IntersectionGroup::fixCrossings


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// resolveCoincidences resolves topological impossibilities that can
// arise from round off error in the positions of the unmatched loose
// end points around the perimeter of a tet face.  These points have
// to be connected to complete the FaceFacets.  The points come in two
// flavors: starts, where an existing segment starts, and stops, where
// an existing segmentsstops.  Stops need to be connected to starts by
// adding new segments going counterclockwise around the perimeter of
// the face.  If stops and starts are in the wrong order, incorrect
// segments will be added.  Round-off error can make two points that
// are supposed to be coincident or nearly coincident to appear to be
// in the wrong order.

void HomogeneityTet::resolveCoincidences(
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
    oofcerr << "HomogeneityTet::resolveCoincidences: nLooseEnds="
	    << looseEnds.size() << std::endl;
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

  for(IntersectionGroup &ig : intersectionGroups) {
#ifdef DEBUG
    if(verboseface) {
      oofcerr << "HomogeneityTet::resolveCoincidences: ig=" << std::endl;
      OOFcerrIndent indent(2);
      std::cerr << ig << std::endl;
    }
#endif // DEBUG
    if(ig.size() > 1) {
      ig.sortByPositionAndEdge();
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveCoincidences: "
		<< "after sorting, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG
      ig.removeEquivPts(this, face, looseEnds);
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveCoincidences: "
		<< "after removeEquivPts, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG
      ig.fixTents(this, face, looseEnds);
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveCoincidences: "
		<< "after fixTents, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG
      ig.fixCrossings(this, face, looseEnds);
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveCoincidences: "
		<< "after fixCrossings, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG
      // fixCrossings can merge points, thereby changing equivalence
      // classes, so it's possible that positions have changed. Re-sort.
      // TODO: keep track of whether anything changed, and only re-sort
      // if necessary.
      ig.sortByPositionAndEdge();
      ig.fixOccupiedEdges(this, face, looseEnds, edgeEdges);
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::resolveCoincidences: "
		<< "after fixOccupiedEdges, ig=" << std::endl;
	OOFcerrIndent indent(2);
	std::cerr << ig << std::endl;
      }
#endif // DEBUG

      // ig.sortByPositionAndEdge();
      // ig.checkOrdering(this, face, looseEnds);
    }
#ifdef DEBUG
    if(verboseface)
      oofcerr << "HomogeneityTet::resolveCoincidences: done with ig"
	      << std::endl;
#endif // DEBUG
  }
} // end HomogeneityTet::resolveCoincidences


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
//     output << "HomogeneityTet::intersectionVolume: tetcenter=" << tetCenter
// 	   << std::endl;
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
// 	  output << "HomogeneityTet::intersectionVolume: pixel plane facet:"
// 		 << " category=" << cat
// 		 << " pixel plane=" << *facet->pixplane
// 		 << " area=" << facet->area()
// 		 << " dv=" << dv << std::endl;
// 	  output << facet->shortDescription()
// 		 << std::endl;
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
// 	output << "HomogeneityTet::intersectionVolume: face facet:"
// 	       << "category=" << cat
// 	       << " face=" << f
// 	       << " area=" << area
// 	       << " " << dot(area, facenorm)
// 	       << " dv=" << dv << std::endl;
// 	output << faceFacets[f].shortDescription()
// 	       << std::endl;
// 	// writeDebugFile(to_string(faceFacets[f]) + "\n");
//       }
// #endif	// DEBUG
      vol += dv;
    }
  }
  return vol;
}

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
  for(IsecEquivalenceClass *eqclass : equivalences) {
    eqclass->dump();
  }
}

#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FaceEdgeIntersection::FaceEdgeIntersection(PlaneIntersection *crnr,
					   FaceFacetEdge *edge,
					   bool start)
  : crnr(crnr),
    edge_(edge),
    t(-1.0),
    fEdge(NONE),
    segstart(start)
{}

// Given a PlaneIntersection and a tet face, compute which edge of the
// face it's on and how far along the edge.
void HomogeneityTet::findFaceEdge(PlaneIntersection *pt, unsigned int face,
				  unsigned int &faceEdge, double &t)
{
  // findFaceEdge uses topological information about intersections and
  // faces, not numerical information about positions.
  faceEdge = pt->findFaceEdge(face, this);
  if(faceEdge != NONE) {
    BarycentricCoord b = getBarycentricCoord(pt->location3D());
    t = faceEdgeCoord(b, face, faceEdge);
    if(t < 0)
      t = 0.0;
    else if(t > 1.0)
      t = 1.0;
  }
}

void FaceEdgeIntersection::findFaceEdge(unsigned int face, HomogeneityTet *htet)
{
  double tt = 0;
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

// void FaceEdgeIntersection::replacePoint(PlaneIntersection *pi,
// 					HomogeneityTet *htet)
// {
//   unsigned int oldEdge = fEdge;
//   double oldT = t;
//   crnr = pi;
//   edge_->replacePoint(pi, htet, segstart);
// }

// A marooned StrandedPoint is one that can't be matched to a
// StrandedPoint on a different face.  It must really belong on an
// edge of the face that it's on.  This routine finds the closest edge
// and puts the point there, by inserting it into the LooseEndMap for
// that edge.

void FaceEdgeIntersection::forceOntoEdge(unsigned int face,
					 HomogeneityTet *htet)
{
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

  htet->getTetFacePlane(face2)->addToEquivalence(crnr->equivalence());
  htet->checkEquiv(crnr);

  unsigned int node0, node1;
  getEdgeNodes(face, fEdge, node0, node1);
  t = b[node1]/(b[node0] + b[node1]);
  if(t < 0)
    t = 0.0;
  else if(t > 1.0)
    t = 1.0;

#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceEdgeIntersection::forceOntoEdge: this=" << *this
	    << std::endl;
    oofcerr << "FaceEdgeIntersection::forceOntoEdge: forced onto edge "
	    << fEdge << std::endl;
  }
#endif // DEBUG
}

bool FaceEdgeIntersection::crosses(const FaceEdgeIntersection *other,
				   unsigned int face,
				   HomogeneityTet *htet
#ifdef DEBUG
				   , bool verbose
#endif // DEBUG
				   ) const
{
  // Does the facet edge that meets the face edge here cross the facet
  // edge that meets the face edge at "other"?

  assert(start() != other->start());
  // Either this point precedes the other on the same face edge, or
  // this point is on the edge preceding the other point's edge.
  // TODO: In a very small face, is it possible that the edge order is
  // reversed?
  assert((faceEdge()==other->faceEdge() &&
	  edgePosition()<=other->edgePosition() )
	 ||
	 ((faceEdge()+1) % NUM_TET_FACE_EDGES == other->faceEdge()));
  
  // The edges don't cross if their endpoints meet.
#ifdef DEBUG
  if(verbose) {
    oofcerr << "FaceEdgeIntersection::crosses:  this=" << *this << std::endl;
    oofcerr << "FaceEdgeIntersection::crosses: other=" << *other << std::endl;
  }
  OOFcerrIndent indent(2);
#endif // DEBUG

  // Check endpoints that are on the face edge.
  const PlaneIntersection *nearEnd = corner();
  const PlaneIntersection *otherNearEnd = other->corner();
  if(nearEnd->isEquivalent(otherNearEnd)) {
#ifdef DEBUG
    if(verbose)
      oofcerr << "FaceEdgeIntersection::crosses: near ends equivalent"
	      << std::endl;
#endif // DEBUG
    return false;
  }
  // Get the endpoints that aren't on the face edge.
  const PlaneIntersection *farEnd = edge_->point(!start());
  const PlaneIntersection *otherFarEnd = other->edge()->point(!other->start());
  if(farEnd->isEquivalent(otherFarEnd)) {
#ifdef DEBUG
    if(verbose)
      oofcerr << "FaceEdgeIntersection::crosses: far ends equivalent"
	      << std::endl;
#endif // DEBUG
    return false;
  }

  // See if the segments actually intersect.
  Coord3D a0 = nearEnd->location3D();
  Coord3D a1 = farEnd->location3D();
  Coord3D b0 = otherNearEnd->location3D();
  Coord3D b1 = otherFarEnd->location3D();
  Coord3D faceNormal = htet->faceAreaVector(face);
  // We know that b0 lies to the right of (a0,a1) and that a0 lies to
  // the left of (b0,b1).  If the segments cross, then b1 must lie to
  // the left of (a0,a1) and a1 to the right of (b0,b1), which is what
  // these cross products check:
  return (dot(cross(a1-a0, b1-a0), faceNormal) >= 0.0 ||
	  dot(cross(b1-b0, a1-b0), faceNormal) <= 0.0);
  
//   return segIntersection(nearEnd->location3D(), farEnd->location3D(),
// 			 otherNearEnd->location3D(), otherFarEnd->location3D()
// #ifdef DEBUG

// 			 , verbose
// #endif // DEBUG
// 			 );
} // end FaceEdgeIntersection::crosses

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

std::ostream &operator<<(std::ostream &os, const FaceEdgeIntersection &fei) {
  os << "FaceEdgeIntersection(" << *fei.corner()
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

// FaceFacetEdge::FaceFacetEdge(const FaceFacetEdge &ffe)
//   :start_(ffe.start_->clone()),
//    stop_(ffe.stop_->clone())
// {
// #ifdef DEBUG
//   oofcerr << "FaceFacetEdge::copy ctor: " << this << std::endl;
// #endif // DEBUG
// }

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
  os << "[" << *edge.startPt() << ", " << *edge.endPt()
     << ", length=" << sqrt(norm2(edge.startPt()->location3D() -
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
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::removeOpposingEdges: initial facet=" << std::endl;
    std::cerr << *this << std::endl;
  }
#endif // DEBUG
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
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::removeOpposingEdges: final facet=" << std::endl;
    std::cerr << *this << std::endl;
  }
#endif // DEBUG
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
  return 0.5*a;
}

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

void FaceFacet::fixNonPositiveArea(HomogeneityTet *htet, unsigned int cat)
{
  Coord3D facetArea = area(htet); // vector!
  Coord3D faceArea = htet->faceAreaVector(face);
  // raw_area is not really the area, but the sign is correct.  It
  // would be the area if we divided by norm(faceArea).
  double raw_area = dot(facetArea, faceArea);
  bool homog_face = false;

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
#ifdef DEBUG
    if(htet->verboseFace()) {
      oofcerr << "FaceFacet::fixNonPositiveArea: testVxl=" << testVxl
	      << " cat=" << htet->microstructure->category(testVxl)
	      << " homog_face=" << homog_face << std::endl;
    }
#endif	// DEBUG
  }
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::fixNonPositiveArea: input facet=" << *this
     	    << std::endl;
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
#ifdef DEBUG
  if(htet->verboseFace()) {
    oofcerr << "FaceFacet::fixNonPositiveArea: final facet=" << *this
     	    << std::endl;
  }
#endif // DEBUG
}

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
    file << edge->startPos3D() << ", " << edge->endPos3D() << std::endl;
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
