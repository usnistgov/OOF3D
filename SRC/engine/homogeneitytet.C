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

#include "common/cdebug.h"
#include "common/cmicrostructure.h"
#include "common/printvec.h"
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

bool HomogeneityTet::verboseCategory_(bool verbose, unsigned int category) const
{
  return verbose && (vcategories.empty() || vcategories.count(category) == 1);
}

static std::set<HPixelPlane> vplanes;

void setVerbosePlane(unsigned int direction, int offset, int normal) {
  auto p = vplanes.emplace(direction, offset, normal);
  oofcerr << "setVerbosePlane: " << *p.first << std::endl;
}

bool HomogeneityTet::verbosePlane_(bool verbose, const HPixelPlane *pixplane)
  const
{
  return verbose && (vplanes.empty() || vplanes.count(*pixplane) == 1);
}

static std::set<unsigned int> vfaces;

void setVerboseFace(unsigned int face) {
  oofcerr << "setVerboseFace: " << face << std::endl;
  vfaces.insert(face);
}

bool HomogeneityTet::verboseFace_(bool verbose, unsigned int face) const {
  return verbose && (vfaces.empty() || vfaces.count(face) == 1);
}

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
    oofcerr << "HomogeneityTet::printLooseEnds: (none)" << std::endl;
}

#include <fstream>
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
    verboseplane(false)
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
      planes.reserve(2 + dirs.size());
      planes.push_back(getTetFacePlane(CSkeletonElement::edgeFaces[e][0]));
      planes.push_back(getTetFacePlane(CSkeletonElement::edgeFaces[e][1]));
      for(unsigned int c : dirs) {
	double x = epts[n0][c];
	const HPixelPlane *pp = getUnorientedPixelPlane(getPixelPlane(c, x, 1));
	if(getCoincidentFacePlane(pp) == nullptr)
	  planes.push_back(pp);
      }
      // Put all combinations of the planes into collinearPlanes so
      // that any plane can be located from a pair of the others.
      for(unsigned int i=0; i<planes.size(); i++) {
	for(unsigned int j=0; j<planes.size(); j++) {
	  if(i != j) {
	    for(unsigned int k=0; k<planes.size(); k++) {
	      if(k != i && k != j) {
		collinearPlanes.insert(
		       std::make_pair(std::make_pair(planes[i], planes[j]),
				      planes[k]));
	      }
	    }
	  }
	}
      }
    } // end if the edge is on any pixel planes
  }   // end loop over edges

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
  for(HPlane *plane : allPlanes_)
    delete plane;
  for(PixelPlaneIntersectionNR *pt : extraPoints)
    delete pt;

  for(IsecEquivalenceClass *eqclass : equivalences)
    delete eqclass;
  
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
  HPixelPlane *pixplane = new HPixelPlane(dir, offset, normal);
  auto result = pixelPlanes_.emplace(pixplane);
  if(!result.second)
    delete pixplane;
  else
    allPlanes_.insert(*result.first);
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
}

// checkEquiv checks to see if the given intersection point belongs in
// any existing equivalence class, and puts it in it.  If the point
// already belongs to a class and is found to also belong to another,
// the classes are merged.
PlaneIntersection *HomogeneityTet::checkEquiv(PlaneIntersection *point) {
// #ifdef DEBUG
//   if(verbose) 
//     oofcerr << "HomogeneityTet::checkEquiv: point=" << point << " " << *point
// 	    << std::endl;
//   OOFcerrIndent indent(2);
// #endif // DEBUG

  bool foundEquiv = true;
  while(foundEquiv == true) {
    foundEquiv = false;
    for(IsecEquivalenceClass *eqclass : equivalences) {
      if(point->equivalence() != eqclass) {
	if(point->isEquivalent(eqclass)) {
	  foundEquiv = true;
	  IsecEquivalenceClass *oldclass = point->equivalence();
// #ifdef DEBUG
// 	  if(verbose)
// 	    oofcerr << "HomogeneityTet::checkEquiv: found eqclass "
// 		    << *eqclass << std::endl;
// #endif // DEBUG
	  if(oldclass != nullptr) {
	    // Since point is in oldclass, calling merge will call
	    // point->setEquivalence(eqclass).
// #ifdef DEBUG
// 	    if(verbose)
// 	      oofcerr << "HomogeneityTet::checkEquiv: merging oldclass="
// 		      << *oldclass << std::endl;
// #endif // DEBUG
	    eqclass->merge(oldclass);
	    // equivalences.erase(oldclass);
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
	}	// end if point belongs in another class
      }
    } // end loop over equivalence classes eqclass
  }
  if(point->equivalence() == nullptr) {
    // The point doesn't belong to any existing equivalence class.
    // Create one, so that other points can be made equivalent to it.
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "HomogeneityTet::checkEquiv: creating new class." << std::endl;
// #endif // DEBUG
    IsecEquivalenceClass *eqclass = new IsecEquivalenceClass(
					     point, nextEquivalenceID()
#ifdef DEBUG
					     , verbose
#endif // DEBUG
							     );
    // equivalences.insert(eqclass);
    equivalences.push_back(eqclass);
    point->setEquivalence(eqclass);
// #ifdef DEBUG
//     if(verbose)
//       oofcerr << "HomogeneityTet::checkEquiv: new class=" << *eqclass
// 	      << std::endl;
// #endif // DEBUG
  }
  return point;
}

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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Find the points at which the edges of the tetrahedron intersect the
// given pixel plane.  The first argument is the oriented PixelPlane.
// The second is the unoriented one used for creating the intersection
// points.  If we just used the unoriented one, the order of the
// points would be wrong half the time.  If we just use the oriented
// one, points that should be at the same location but are on
// different orientations of the same plane would appear to be
// different.

TetIntersectionPolygon&
HomogeneityTet::getTetPlaneIntersectionPoints(const HPixelPlane *pixplane,
					      const HPixelPlane *upixplane)
{
// #ifdef DEBUG
//   oofcerr << "HomogeneityTet::getTetPlaneIntersectionPoints: pixplane="
// 	  << pixplane << " " << *pixplane << std::endl;
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
      result.push_back(new TetEdgeIntersection(this, face0, face1, upixplane));
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
	result.push_back(new TetEdgeIntersection(this, face0, face1,
						 upixplane));
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
	      result.push_back(
		       new TetNodeIntersection(this, pixplane, inplanenode));
	      didinplane = true;
	    }
	  }
	else {
	  FacePlane *face0 = faces[CSkeletonElement::edgeFaces[edge][0]];
	  FacePlane *face1 = faces[CSkeletonElement::edgeFaces[edge][1]];
	  result.push_back(new TetEdgeIntersection(this, face0, face1,
						   upixplane));
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
	result.push_back(new TetEdgeIntersection(this, face0, face1,
						 upixplane));
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
// #ifdef DEBUG
//   if(verbosecategory) {
//     oofcerr << "HomogeneityTet::findPixelPlaneFacets: done with face planes"
// 	    << std::endl;
//   }
// #endif // DEBUG

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
  const HPixelPlane *upixplane = getUnorientedPixelPlane(pixplane);
  TetIntersectionPolygon &tetPts = getTetPlaneIntersectionPoints(pixplane,
								 upixplane);
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

  // #ifdef DEBUG
//   if(verboseplane) {
//     oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: upixplane="
// 	    << *upixplane << std::endl;
//     const FacePixelPlane *ufpp = dynamic_cast<const FacePixelPlane*>(upixplane);
//     oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: as FacePixelPlane, upixplane=" << ufpp;
//     if(ufpp != nullptr)
//       oofcerr << " " << *ufpp;
//     oofcerr << std::endl;
//   }
// #endif	// DEBUG


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
	  HPixelPlane orthoPlanePrev =
	    pixplane->orthogonalPlane(pbs_prev, pbs_start);
	  HPixelPlane orthoPlane =
	    pixplane->orthogonalPlane(pbs_start, pbs_end);
	  HPixelPlane orthoPlaneNext =
	    pixplane->orthogonalPlane(pbs_end, pbs_next);
	  // Get the pointers to the reference versions of the planes,
	  // so that pointer comparisons can be used later.
	  const HPixelPlane *prevPlanePtr =
	    getUnorientedPixelPlane(&orthoPlanePrev);
	  const HPixelPlane *orthoPlanePtr =
	    getUnorientedPixelPlane(&orthoPlane);
	  const HPixelPlane *nextPlanePtr =
	    getUnorientedPixelPlane(&orthoPlaneNext);
	  facet->addEdge(new PixelFacetEdge(
			    new TriplePixelPlaneIntersection(this,
				 upixplane, prevPlanePtr, orthoPlanePtr),
			    new TriplePixelPlaneIntersection(this,
				 upixplane, orthoPlanePtr, nextPlanePtr)));

	} // end if the segment is entirely inside the polygon

	else if(pbs_start_inside != pbs_end_inside) {
	  // If start and end are hetero-interior, so to speak, then
	  // there's one intersection. Find it.
	  HPixelPlane orthoPlane =
	    pixplane->orthogonalPlane(pbs_start, pbs_end);
	  const HPixelPlane *orthoPlanePtr =
	    getUnorientedPixelPlane(&orthoPlane);
	  unsigned int orthoFace = getCoincidentFaceIndex(orthoPlanePtr);
	  PixelPlaneIntersectionNR *pi = find_one_intersection(
						 pixplane,
						 upixplane,
						 orthoPlanePtr,
						 PixelBdyLoopSegment(loop, k),
						 onFace, orthoFace,
						 pbs_end_inside);
	  if(pbs_start_inside) {
	    HPixelPlane orthoPlanePrev =
	      pixplane->orthogonalPlane(pbs_prev, pbs_start);
	    const HPixelPlane *prevPlanePtr =
	      getUnorientedPixelPlane(&orthoPlanePrev);
	    facet->addEdge(new StopFaceIntersectionEdge(
				new TriplePixelPlaneIntersection(this,
				       upixplane, prevPlanePtr, orthoPlanePtr),
			    pi));
	  }
	  else {
	    HPixelPlane orthoPlaneNext = 
	      pixplane->orthogonalPlane(pbs_end, pbs_next);
	    const HPixelPlane *nextPlanePtr =
	      getUnorientedPixelPlane(&orthoPlaneNext);
	    facet->addEdge(new StartFaceIntersectionEdge(
			     pi,
			     new TriplePixelPlaneIntersection(this,
				      upixplane, orthoPlanePtr, nextPlanePtr)));
	  }
	} // end if start and end are hetero-interior
	else {
	  // The current segment has both endpoints outside the
	  // polygon.  It must intersect zero or two times.
	  ICRectangle segbb(pbs_start, pbs_end);
	  if(segbb.intersects(tetBounds)) {
	    HPixelPlane orthoPlane =
	      pixplane->orthogonalPlane(pbs_start, pbs_end);
	    // Since getTetPlaneIntersectionPoints looks up caches
	    // previous computations by PixelPlane pointer, get the
	    // HomogeneityTet's official version of the orthogonal
	    // plane.
	    // TODO: Instead of calling PixelPlane::orthogonalPlane
	    // and HomogeneityTet::getPixelPlane, combine them into
	    // HomogeneityTet::getOrthogonalPlane.
	    const HPixelPlane *orthoPlanePtr = getPixelPlane(
						    orthoPlane.direction(),
						    orthoPlane.normalOffset(),
						    orthoPlane.normalSign());
	    const HPixelPlane *uOrthoPlanePtr =
	      getUnorientedPixelPlane(&orthoPlane);
	    // There's no intersection unless the orthoPlane actually
	    // intersects the tetrahedron.  This check is important
	    // for consistency.  When a pixel plane coincides with a
	    // face, sometimes find_two_intersections will find
	    // intersections when getTetPlaneIntersectionPoints
	    // doesn't, and this can lead to unmatched facet edge
	    // endpoints.
	    TetIntersectionPolygon orthoPts =
	      getTetPlaneIntersectionPoints(orthoPlanePtr, uOrthoPlanePtr);
	    if(!orthoPts.empty()) {
	      unsigned int orthoFace = getCoincidentFaceIndex(orthoPlanePtr);
	      std::vector<PixelPlaneIntersectionNR*> isecs =
		find_two_intersections(pixplane, upixplane,
				       uOrthoPlanePtr,
				       PixelBdyLoopSegment(loop, k),
				       onFace, orthoFace);
	      if(isecs.size() == 2) {
		facet->addEdge(new TwoFaceIntersectionEdge(isecs[0], isecs[1]));
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
    oofcerr << "HomogeneityTet::doFindPixelPlaneFacets: facet=" << *facet
	    << std::endl;
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
					const HPixelPlane *upixplane,
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
  // immediately which face the segment crosses.  Do *not* use
  // upixplane here.
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
      if(!areCollinear(upixplane, orthoPlane, getTetFacePlane(face))) {
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
    newIntersection(this, upixplane, orthoPlane, pbls,
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
    const HPixelPlane *upp = getUnorientedPixelPlane(pp);
    upp->addToIntersection(ppi);
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
					const HPixelPlane *upixplane,
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
       !areCollinear(upixplane, orthoPlane, getTetFacePlane(face)))
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
      isecs[0] = newIntersection(this, upixplane, orthoPlane, pblseg,
				 entryAlpha, entryFace, ENTRY);
      isecs[1] = newIntersection(this, upixplane, orthoPlane, pblseg,
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

// cleanUpLooseEnds removes a loose start or end from the given sets
// of FaceEdgeIntersections, when it's known that there's at least one
// extra one.  It looks at all pairs of adjacent points on each edge,
// and removes one member of the pair with the smallest separation.
// It only looks at points which are either starts or stops, according
// to the "start" argument.

static bool cleanUpLooseEnds(std::vector<LooseEndMap> &looseEnds, bool start) {
  double smallestDist = std::numeric_limits<double>::max();
  unsigned int edge = NONE;
  LooseEndMap::iterator deleteMe;

  for(unsigned int e=0; e<looseEnds.size(); e++) {
    LooseEndMap &lem = looseEnds[e];
    LooseEndMap::iterator i = lem.begin();
    if(i != lem.end()) {
      LooseEndMap::iterator prev = i;
      i++;
      for( ; i!=lem.end(); ++i) {
	if((*i).second.start() == start && (*prev).second.start() == start &&
	   (*i).first - (*prev).first < smallestDist)
	  {
	    smallestDist = (*i).first - (*prev).first;
	    deleteMe = i;
	    edge = e;
	  }
	prev = i;
      }
    }
  }
  if(edge != NONE) {
    looseEnds[edge].erase(deleteMe);
    return true;
  }
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// A StrandedPoint is an unpaired end in a set of segments on a tet
// face.

class StrandedPoint {
public:
  FaceEdgeIntersection feInt;
  unsigned int face;
  StrandedPoint(const FaceEdgeIntersection &fei, unsigned int f)
    : feInt(fei), face(f)
  {}
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


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

  // Loop over pixel plane facets, sorting the edges that cross tet
  // faces.

  for(FacetMap2D::const_iterator fm=planeFacets.begin(); fm!=planeFacets.end();
      ++fm)
    {
      PixelPlaneFacet *planeFacet = (*fm).second;
      // getEdgesOnFaces asks each PolygonEdge to store a reversed
      // copy of itself in faceFacets.  A new FaceFacetEdge is created
      // in faceFacets for each edge of the PixelPlaneFacet that lies
      // in a tet face.
#ifdef DEBUG
      if(verbosecategory)
	oofcerr << "HomogeneityTet::findFaceFacets: calling getEdgesOnFaces for"
		<< " " << *planeFacet->pixplane << std::endl;
      OOFcerrIndent indent(2);
#endif	// DEBUG
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
  }
#endif	// DEBUG

  // The segments on each face facet must (eventually) join together
  // end to end to form a closed polygon.  They don't necessarily do
  // so yet, because the polygon may need to be closed by adding
  // segments along the perimeter of the face.  Also, if a VSB
  // boundary passed through a tet edge, it may have resulted in an
  // ENTRY/EXIT pair of points neither of which will be considered to
  // be on the edge, because each is composed of two pixel planes and
  // one tet face.  This will result in two unpaired endpoints on two
  // different faces in virtually the same location.  We need to
  // detect and merge these points so that they're on the tet edge.
  
  // This only needs to be done for faces that aren't coincident with
  // pixel planes, because the facets on the pixel planes have already
  // been found.

  // looseEndCatalog[f][e] is a LooseEndMap for edge e of face f.  It
  // maps parametric positions along the edge to the
  // FaceEdgeIntersection at that point.
  std::vector<std::vector<LooseEndMap>>
    looseEndCatalog(NUM_TET_FACES,
		    std::vector<LooseEndMap>(NUM_TET_FACE_EDGES));

  std::vector<StrandedPoint> strandedPoints;

  // Loop over all faces that aren't also pixel planes.
  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
    if(coincidentPixelPlanes[face] == nullptr) {

#ifdef DEBUG
    verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
    
      FaceFacet &facet = faceFacets[face];
      std::vector<LooseEndMap> &looseEnds = looseEndCatalog[face];
	    
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: looking for loose ends"
		<< " on face " << face << std::endl;
      }
      OOFcerrIndent indent(2);
#endif	// DEBUG
      unsigned int nsegs = facet.size();
      std::vector<FaceEdgeIntersection> startPoints;
      std::vector<FaceEdgeIntersection> endPoints;
      startPoints.reserve(nsegs);
      endPoints.reserve(nsegs);
      // Loop over segments in the face facet, storing their start and
      // end points.  *seg is a FaceFacetEdge*.
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: starting checkEquiv loop"
		<< std::endl;
	if(!verify())
	  throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      }
#endif // DEBUG

      
      // Make sure equivalence classes are up to date.
      // for(auto seg=facet.begin(); seg!=facet.end(); ++seg) {
      // 	(*seg)->startPt()->includeCollinearPlanes(collinearPlanes);
      // 	(*seg)->endPt()->includeCollinearPlanes(collinearPlanes);
      // }
      for(auto seg=facet.begin(); seg!=facet.end(); ++seg) {
      	checkEquiv((*seg)->startPt());
      	checkEquiv((*seg)->endPt());
      }

      for(auto seg=facet.begin(); seg!=facet.end(); ++seg) {
	// Construct FaceEdgeIntersection objects in-place.
	startPoints.emplace_back((*seg)->startPt(), *seg, true);
	endPoints.emplace_back((*seg)->endPt(), *seg, false);
      }
#ifdef DEBUG
      if(verboseface) {
	// At this point, fEdge hasn't been set in the
	// FaceEdgeIntersection objects, so don't be surprised by the
	// printed value.
	oofcerr << "HomogeneityTet::findFaceFacets: startPoints="
		<< std::endl;
	for(const auto &p: startPoints) {
	  OOFcerrIndent indent(2);
	  oofcerr << "HomogeneityTet::findFaceFacets: " << p << std::endl;
	}
	oofcerr << "HomogeneityTet::findFaceFacets: endPoints="
		<< std::endl;
	for(const auto &p: endPoints) {
	  OOFcerrIndent indent(2);
	  oofcerr << "HomogeneityTet::findFaceFacets: " << p << std::endl;
	}
      }
      if(!verify())
      	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
#endif // DEBUG
      // matchedStarts and matchedEnds indicate which segment start
      // and end points have been paired up.  The loose ones that
      // haven't been paired will be used to construct the missing
      // segments.
      std::vector<bool> matchedStarts(nsegs, false);
      std::vector<bool> matchedEnds(nsegs, false);
      for(unsigned int s=0; s<nsegs; s++) {
	for(unsigned int e=0; e<nsegs; e++) {
	  if(// s!=e &&
	     !matchedEnds[e] &&
	     startPoints[s].corner()->isEquivalent(endPoints[e].corner()))
	    {
	      matchedStarts[s] = true;
	      matchedEnds[e] = true;
#ifdef DEBUG
	      if(verboseface) {
		oofcerr << "HomogeneityTet::findFaceFacets: matched s="
			<< s << " e=" << e << " "
			<< *startPoints[s].corner() << " to "
			<< *endPoints[e].corner() << std::endl;
	      }
#endif // DEBUG
	      break;		// don't match this s with another e
	    }
	} // end loop over end points e
      }   // end loop over start points s
#ifdef DEBUG
      // if(!verify())
      // 	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      if(verboseface) {
	// oofcerr << "HomogeneityTet::findFaceFacets: got matches" << std::endl;
	oofcerr << "HomogeneityTet::findFaceFacets: matchedStarts=";
	std::cerr << matchedStarts;
	oofcerr << std::endl;
	oofcerr << "HomogeneityTet::findFaceFacets:   matchedEnds=";
	std::cerr << matchedEnds;
	oofcerr << std::endl;
      }
#endif // DEBUG
      
      // All of the truly unmatched points must be on tet edges.  Sort
      // them by the edge and intersection position along the edge.
      // The ones that don't appear to be on edges now are "stranded",
      // but must be very close to edges and will be paired up later
      // to stranded points on other faces.

      for(unsigned int i=0; i<nsegs; i++) {
	if(!matchedStarts[i]) {
	  startPoints[i].findFaceEdge(face, this);
	  unsigned int edge = startPoints[i].faceEdge();
	  if(edge != NONE) {
	    looseEnds[edge].emplace(startPoints[i].edgePosition(),
				    startPoints[i]);
	  }
	  else {
	    strandedPoints.emplace_back(startPoints[i], face);
	  }
	}
	if(!matchedEnds[i]) {
	  endPoints[i].findFaceEdge(face, this);
	  unsigned int edge = endPoints[i].faceEdge();
	  if(edge != NONE)
	    looseEnds[edge].emplace(endPoints[i].edgePosition(),
				    endPoints[i]);
	  else {
	    strandedPoints.emplace_back(endPoints[i], face);
	  }
	}
      }
#ifdef DEBUG
      // if(!verify())
      // 	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: loose ends, face="
		<< face << ":" << std::endl;
	for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++) {
	  OOFcerrIndent indent(2);
	  if(!looseEnds[i].empty())
	    for(auto l=looseEnds[i].begin(); l!=looseEnds[i].end(); ++l) {
	      oofcerr << "HomogeneityTet::findFaceFacets: edge=" << i
		      << " pos=" << (*l).first
		      << ": " << (*l).second << std::endl;
	    }
	  else
	    oofcerr << "HomogeneityTet::findFaceFacets: edge=" << i
		    << " (none)" << std::endl;
	}
      }
#endif // DEBUG
    }  // end if tet face is not a pixel plane
  } // end loop over faces

#ifdef DEBUG
  if(verbosecategory) {
    oofcerr << "HomogeneityTet::findFaceFacets: strandedPoints="
	    << std::endl;
    OOFcerrIndent indent(2);
    for(const StrandedPoint &pt : strandedPoints)
      oofcerr << "HomogeneityTet::findFaceFacets: face=" << pt.face
	      << " " << pt.feInt << std::endl;
  }
#endif // DEBUG

  // if(!verify())
  //   throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
  
  // If there are stranded points, pair them up.  Stranded points come
  // from situations where a VSB segment passes nearly through a
  // polygon vertex in one pixel plane, leading to an entry/exit pair
  // that should be on a tet edge but isn't.  They can also arise when
  // the intersection line of two perpendicular pixel planes passes
  // through a tet edge.  In that case, there will be points on the
  // two planes but on different faces, and because each point is only
  // on one face, it won't be assigned to a tet edge.  TODO: This
  // comment is confusing.  The second case encompasses the first,
  // doesn't it?

  // If there are no other pixel planes creating segments connecting
  // to those points, they will be loose ends of the face facet, but
  // they're not on tet edges, so they can't be joined by adding facet
  // edges on the tet edges.  When the stranded points are paired,
  // each point of each pair must be on a different tet face, and
  // merging the pair produces a point on a tet edge (the edge shared
  // by the two faces).  The new merged point can be inserted into the
  // looseEndCatalog.

  // Stranded points that can't be matched, sorted by face
  std::vector<std::vector<StrandedPoint>> marooned(NUM_TET_FACES);
  
  std::vector<bool> matched(strandedPoints.size(), false);
  for(unsigned int i=0; i<strandedPoints.size(); i++) {
    if(!matched[i]) {
      const StrandedPoint &pt0 = strandedPoints[i];
      unsigned int best = NONE;
      double mindist2 = std::numeric_limits<double>::max();
      for(unsigned int j=i+1; j<strandedPoints.size(); j++) {
	const StrandedPoint &pt1 = strandedPoints[j];
	if(pt0.face != pt1.face &&
	   pt0.feInt.corner()->samePixelPlanes(pt1.feInt.corner()))
	  {
	    double dist2 = norm2(pt0.feInt.corner()->location3D() -
				 pt1.feInt.corner()->location3D());
	    if(dist2 < mindist2) {
	      mindist2 = dist2;
	      best = j;
	    }
	  }
      }	// end loop over possible matches j
      if(best != NONE) {
	matched[best] = true;
	matched[i] = true;
	const StrandedPoint &pt1 = strandedPoints[best];
	// The pixel plane intersections are stored in
	// FaceEdgeIntersection as generic PlaneIntersections, but in
	// this case we know that they're PixelPlaneIntersections.
	PixelPlaneIntersection *ppi0 =
	  dynamic_cast<PixelPlaneIntersection*>(pt0.feInt.corner());
	PixelPlaneIntersection *ppi1 =
	  dynamic_cast<PixelPlaneIntersection*>(pt1.feInt.corner());
	assert(ppi0 != nullptr && ppi1 != nullptr);
	PixelPlaneIntersectionNR *merged =
	  new MultiCornerIntersection(this, ppi0->referent(), ppi1->referent());
	PlaneIntersection *newpt0 =
	  pt0.feInt.edge()->replacePoint(merged, this, pt0.feInt.start());
	PlaneIntersection *newpt1 =
	  pt1.feInt.edge()->replacePoint(merged, this, pt1.feInt.start());
	FaceEdgeIntersection fei0(newpt0, pt0.feInt.edge(), pt0.feInt.start());
	FaceEdgeIntersection fei1(newpt1, pt1.feInt.edge(), pt1.feInt.start());
	fei0.findFaceEdge(pt0.face, this);
	fei1.findFaceEdge(pt1.face, this);
	looseEndCatalog[pt0.face][fei0.faceEdge()].emplace(
						   fei0.edgePosition(), fei0);
	looseEndCatalog[pt1.face][fei1.faceEdge()].emplace(
						   fei1.edgePosition(), fei1);
	
	// The merged point isn't in a FacetEdge, so it won't be
	// automatically deleted.  Store it for later deletion.
	extraPoints.insert(merged);
#ifdef DEBUG
	if(verbosecategory) {
	  oofcerr << "HomogeneityTet::findFaceFacets: matched stranded points:"
		  << std::endl;
	  OOFcerrIndent indent(2);
	  oofcerr << "HomogeneityTet::findFaceFacets: ppi0=" << *ppi0
		  << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: ppi1=" << *ppi1
		  << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: --> " << *merged
		  << std::endl;
	}
#endif // DEBUG
      }	// end if best is not NONE
      else {
	marooned[pt0.face].push_back(pt0);
#ifdef DEBUG
	if(verbosecategory)
	  oofcerr << "HomogeneityTet::findFaceFacets: marooned point! "
		  << pt0.feInt << std::endl;
#endif // DEBUG
      }
    }	// end if point i hasn't been matched
  }	// end loop over stranded points i

  // Join the unmatched points in each FaceFacet.  This only needs to
  // be done for faces that aren't coincident with pixel planes,
  // because the facets on the pixel planes have already been found.

  // if(!verify())
  //   throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);

  for(unsigned int face=0; face<NUM_TET_FACES; face++) {
#ifdef DEBUG
    verboseface = verboseFace_(verbosecategory, face);
#endif // DEBUG
    FaceFacet &facet = faceFacets[face];
    if(coincidentPixelPlanes[face] == nullptr) { // face is not a pixel plane
      std::vector<LooseEndMap> &looseEnds = looseEndCatalog[face];
      Coord3D faceNormal = faceAreaVectors[face]; // not unit vector

      // Put any marooned points onto the closest edge.
      for(StrandedPoint &sp : marooned[face]) {
	sp.feInt.forceOntoEdge(sp.face, this);
	unsigned int edge = sp.feInt.faceEdge();
	looseEnds[edge].emplace(sp.feInt.edgePosition(), sp.feInt);
      }

#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: before coincidence check, "
		<< "loose ends, face=" << face << ":" << std::endl;
	for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++) {
	  OOFcerrIndent indent(2);
	  printLooseEnds(i, looseEnds[i]);
	}
      }
#endif // DEBUG

      // Look for near coincidences.  These are a problem if round-off
      // error has perturbed the edge positions, and a loose end
      // that's supposed to coincide with a loose start has an
      // edgePosition that's slightly after the start.  But first,
      // remove exact coincidences to simplify the near coincidence
      // check.
      
      for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
#ifdef DEBUG
	if(verboseface)
	  oofcerr
	    << "HomogeneityTet::findFaceFacets: looking for coincidences, cat "
	    << cat << " face " << face << " edge " << e << std::endl;
	OOFcerrIndent indent(2);
#endif // DEBUG
	if(looseEnds[e].size() > 1) {
	  // Coincidence check part 1.  If more than one segment
	  // intersects at *exactly* the same point on the edge of a
	  // face, throw out as many stop/start pairs as possible.
	  LooseEndMap &lem = looseEnds[e];
	  LooseEndMap::iterator x = lem.begin();
	  while(x != lem.end()) {
	    double t = (*x).first;	   // parametric coord of intersection
	    unsigned int n = lem.count(t); // no. of intersections at t
	    if(n > 1) {
	      auto range = lem.equal_range(t);
	      int nstartdiff = 0; // # of starts minus # of stops at this t
	      for(LooseEndMap::iterator y=range.first; y!=range.second; ++y) {
		if((*y).second.start())
		  nstartdiff++;
		else
		  nstartdiff--;
	      }
	      if(nstartdiff == 0) {
		// There are as many starts as stops.  They're all irrelevant.
		lem.erase(range.first, range.second);
	      }
	      else {
		// nstartdiff != 0
		std::vector<LooseEndMap::iterator> deleteThese;
		if(nstartdiff > 0) {
		  // Delete all but nstartdiff starts.
		  int kept = 0;
		  for(LooseEndMap::iterator y=range.first; y!=range.second; ++y)
		    {
		      if(kept >= nstartdiff || !(*y).second.start())
			deleteThese.push_back(y);
		      else
			kept++;
		    }
		}
		else if(nstartdiff < 0) {
		  // Delete all but -nstartdiff stops.
		  unsigned int kept = 0;
		  for(LooseEndMap::iterator y=range.first; y!=range.second; ++y)
		    {
		      if(kept >= -nstartdiff || (*y).second.start())
			deleteThese.push_back(y);
		      else
			kept++;
		    }
		}
		for(auto y=deleteThese.rbegin(); y!=deleteThese.rend(); ++y)
		  lem.erase(*y);
	      }	// end if nstartdiff != 0
	      x = range.second;
	    } // end if there is more than one intersection at point t
	    else {
	      ++x;
	    }
	  }
	}
#ifdef DEBUG
	if(verboseface) {
	  oofcerr << "HomogeneityTet::findFaceFacets: "
		  << " after 1st coincidence check: " << std::endl;
	  OOFcerrIndent indent(2);
	}
#endif // DEBUG
	
	// Coincidence check part 2.  Look for intersection points on
	// the face edges that are close to each other but not exactly
	// equivalent, and make sure that the facet segments that meet
	// the face edges there don't cross.  If they do, the
	// intersection points must be misordered by roundoff, and
	// should actually be identical.
	if(looseEnds[e].size() > 1) {
	  // Loop over loose ends on the edge.  The loop isn't simple
	  // because loose ends are removed by pairs, so the iterator
	  // has to increase by 2 and the stop criterion is that
	  // either the iterator (x) or its successor (xnext) points
	  // to the end of the array.
	  LooseEndMap::iterator x = looseEnds[e].begin();
	  LooseEndMap::iterator xnext = x;
	  xnext++;
	  unsigned int tetEdge = CSkeletonElement::faceEdges[face][e];
	  bool done = false;
	  while(!done) {
	    double dt = ((*xnext).second.edgePosition() -
			 (*x).second.edgePosition()) * edgeLengths[tetEdge];
#ifdef DEBUG
	    if(verboseface) {
	      oofcerr << "HomogeneityTet::findFaceFacets: x=" << (*x).second
		      << " xnext=" << (*xnext).second
		      << " dt=" << dt << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets: alphas x="
		      << (*x).first << " xnext=" << (*xnext).first
		      << " diff=" << (*xnext).first - (*x).first
		      << std::endl;
	    }
#endif // DEBUG
	    bool equiv =
	      (*x).second.corner()->isEquivalent((*xnext).second.corner());
	    if(!equiv && dt < 0.5) {
	      // The two points are within a half a pixel of each
	      // other and can potentially coincide.
	      if((*x).second.start() != (*xnext).second.start()) {
#ifdef DEBUG
		if(verboseface) {
		  oofcerr << "HomogeneityTet::findFaceFacets: checking... "
			  << std::endl;
		}
		OOFcerrIndent indnt(2);
#endif // DEBUG
		// x is the start (end) of a facet segment that lies
		// in the face and has an endpoint on an edge of the
		// face, and xnext is the end (start) of another such
		// facet segment. xnext's endpoint is just past x's on
		// the facet edge (because xnext is after x in the
		// LooseEndMap).

		// If round-off error has put the edge intersections
		// in the wrong order, then the segments will
		// intersect.  Since facet segments can't cross, we
		// can tell if the ordering is incorrect.

		// a0 and b0 are the endpoints of x and xnext that lie
		// on the facet edge, irrespective of the directions
		// of the segments.  a1 and b1 are the other endpoints
		// of the segments.
		Coord3D a0, a1, b0, b1;
		const FaceFacetEdge *edgeA = (*x).second.edge();
		const FaceFacetEdge *edgeB = (*xnext).second.edge();
#ifdef DEBUG
		if(verboseface) {
		  oofcerr << "HomogeneityTet::findFaceFacets: edgeA="
			  << *edgeA << std::endl;
		  oofcerr << "HomogeneityTet::findFaceFacets: edgeB="
			  << *edgeB << std::endl;
		}
#endif // DEBUG
		if((*x).second.start()) {
		  a0 = edgeA->startPt()->location3D();
		  b0 = edgeB->endPt()->location3D();
		  a1 = edgeA->endPt()->location3D();
		  b1 = edgeB->startPt()->location3D();
		}
		else {
		  a1 = edgeA->startPt()->location3D();
		  b1 = edgeB->endPt()->location3D();
		  a0 = edgeA->endPt()->location3D();
		  b0 = edgeB->startPt()->location3D();
		}
#ifdef DEBUG
		if(verboseface) {
		  oofcerr << "HomogeneityTet::findFaceFacets: normal="
			  << faceNormal << std::endl;
		  oofcerr << "HomogeneityTet::findFaceFacets: a0=" << a0
			  << " a1=" << a1 << " b0=" << b0 << " b1=" << b1
			  << std::endl;
		  oofcerr << "HomogeneityTet::findFaceFacets: a1-a0=" << a1-a0
			  << " b1-a0=" << b1-a0
			  << " cross=" << cross(a1-a0, b1-a0)
			  << std::endl;
		  oofcerr << "HomogeneityTet::findFaceFacets: b1-b0=" << b1-b0
			  << " a1-b0=" << a1-b0
			  << " cross=" << cross(b1-b0, a1-b0)
			  << std::endl;
		  oofcerr << "HomogeneityTet::findFaceFacets: dotA="
			  << dot(cross(a1-a0, b1-a0), faceNormal)
			  << " dotB=" << dot(cross(b1-b0, a1-b0), faceNormal)
			  << std::endl;
		}
#endif // DEBUG
		// We know that b0 lies to the right of (a0,a1) and
		// that a0 lies to the left of (b0,b1).  If the
		// segments cross, then b1 must lie to the left of
		// (a0,a1) and a1 to the right of (b0,b1), which is
		// what these cross products check:
		equiv = (dot(cross(a1-a0, b1-a0), faceNormal) >= 0.0 ||
			 dot(cross(b1-b0, a1-b0), faceNormal) <= 0.0);
	      } // end if x is start and xnext is an end, or vice versa
	    }	// end if the points are within a pixel of each other
	    if(equiv) {
	      // The points are either identical, or are in the wrong
	      // order, so they must actually coincide but differ by
	      // roundoff error.  They're not really loose ends.
	      // Remove them from the list.
#ifdef DEBUG
	      if(verboseface) {
		oofcerr << "HomogeneityTet::findFaceFacets:"
			<< " removing coincidence" << std::endl;
	      }
#endif // DEBUG
	      LooseEndMap::iterator xtemp = xnext;
	      ++xtemp;
	      looseEnds[e].erase(x);
	      looseEnds[e].erase(xnext);
	      x = xtemp;
	      if(xtemp == looseEnds[e].end()) 
		done = true;
	      else {
		xnext = x;
		xnext++;
		done = (xnext == looseEnds[e].end());
	      }
	    }
	    else {
	      x = xnext;
	      xnext++;
	      done = (xnext == looseEnds[e].end());
	    }
	  } // end loop over loose ends x
	} // end if there is more than one loose end on the edge
      }   // end loop over face edges e
// #ifdef DEBUG
//       if(verbosecategory)
// 	oofcerr << "HomogeneityTet::findFaceFacets: coincidence check done "
// 		<< std::endl;
// #endif	// DEBUG

#ifdef DEBUG
      // if(!verify())
      // 	throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: after coincidence check, "
		<< "loose ends, face=" << face << ":" << std::endl;
	for(unsigned int i=0; i<NUM_TET_FACE_EDGES; i++) {
	  OOFcerrIndent indent(2);
	  printLooseEnds(i, looseEnds[i]);
	}
      }
#endif // DEBUG
      
      // Check that the number of loose starts and ends match
      int nStarts = 0;
      int nEnds = 0;
      for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	LooseEndMap &lem = looseEnds[e];
	for(LooseEndMap::const_iterator i=lem.begin(); i!=lem.end(); ++i) {
	  if((*i).second.start())
	    nStarts++;
	  else
	    nEnds++;
	}
      }
      if(nStarts != nEnds) {
	// This can happen if a coincidence was resolved on one pixel
	// plane but not on another. In that case there can be two
	// starts (or ends) at nearly identical positions, one of
	// which should be removed.
#ifdef DEBUG
	if(verboseface) {
	  oofcerr << "HomogeneityTet::findFaceFacets: resolving loose end mismatch"
		 << std::endl;
	  oofcerr << "HomogeneityTet::findFaceFacets: looseEnds=" << std::endl;
	  OOFcerrIndent indent(2);
	  for(unsigned int e=0; e<looseEnds.size(); e++) {
	    for(auto lem=looseEnds[e].begin(); lem!=looseEnds[e].end(); ++lem) {
	      oofcerr << "HomogeneityTet:findFaceFacets: e=" << e
		      << " d=" << (*lem).first
		      << " " << (*lem).second << std::endl;
	    }
	  }
	}
#endif // DEBUG
	if(nStarts > nEnds) {
	  while(nStarts > nEnds) {
	    if(cleanUpLooseEnds(looseEnds, true))
	      --nStarts;
	    else {
	      oofcerr << "HomogeneityTet::findFaceFacets: "
		      << "failed to resolve loose end mismatch, cat=" << cat
		      << " face=" << face << std::endl;
	      throw ErrProgrammingError("HomogeneityTet::findFaceFacets: cleanUpLooseEnds failed! start=true",
					__FILE__, __LINE__);
	    }
	  } // end while nStarts > nEnds
	}   // end if nStarts > nEnds
	else  {
	  // nStarts < nEnds
	  while(nEnds > nStarts) {
	    if(cleanUpLooseEnds(looseEnds, false))
	      --nEnds;
	    else {
	      oofcerr << "HomogeneityTet::findFaceFacets: "
		      << "failed to resolve loose end mismatch, cat=" << cat
		      << " face=" << face << std::endl;
	      throw ErrProgrammingError("HomogeneityTet::findFaceFacets: cleanUpLooseEnds failed! start=false",
					__FILE__, __LINE__);
	    }
	  } // end while nEnds > nStarts
	} // end if nStarts < nEnds
      }	// end if nStarts != nEnds

	// Create the missing segments. Missing segments start at a
	// loose end and end at a loose start.
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: creating missing segments"
		<< " on face " << face << std::endl;
	for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	  oofcerr << "HomogeneityTet::findFaceFacets: loose ends on edge "
		  << e << std::endl;
	  OOFcerrIndent indent(2);
	  const LooseEndMap &lem = looseEnds[e];
	  for(LooseEndMap::const_iterator le=lem.begin(); le!=lem.end(); ++le) {
	    oofcerr << "HomogeneityTet::findFaceFacets: " << le->first
		    << ": " << le->second << std::endl;
	  }
	}
      }
#endif // DEBUG
	
      // If the first intersection found is a start, it's stored in
      // firstStart.
      const FaceEdgeIntersection *firstStart = nullptr;
      // currentEnd is non-null if we've found an end are looking
      // for a start.
      const FaceEdgeIntersection *currentEnd = nullptr;
	
      for(unsigned int e=0; e<NUM_TET_FACE_EDGES; e++) {
	const LooseEndMap &lem = looseEnds[e];
	for(LooseEndMap::const_iterator le=lem.begin(); le!=lem.end(); ++le) {
	  if(!(*le).second.start()) {
	    // This point is a loose end, so it's the start of a new
	    // segment.
	    if(currentEnd != nullptr) {
	      oofcerr << "HomogeneityTet::findFaceFacets: "
		      << "two consecutive ends on face " << face 
		      << " category=" << cat << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets: currentEnd="
		      << *currentEnd << std::endl;
	      oofcerr << "HomogeneityTet::findFaceFacets: new point="
		      << (*le).second << std::endl;
	      throw ErrProgrammingError(
		"Loose end matching failed!  Found two consecutive ends.",
		__FILE__, __LINE__);
	    }
	    currentEnd = &(*le).second;
	  } // end if this is a loose end
	  else {
	    // This point is a loose start, so it's the end of a new segment.
	    if(currentEnd == nullptr) {
	      // We haven't seen the end for this start. Save it for later.
	      if(firstStart == nullptr)
		firstStart = &(*le).second;
	      else {
		oofcerr << "HomogeneityTet::findFaceFacets: "
			<< "two consecutive starts on face " << face 
			<< " category=" << cat << std::endl;
		oofcerr << "HomogeneityTet::findFaceFacets: firstStart="
			<< *firstStart << std::endl;
		oofcerr << "HomogeneityTet::findFaceFacets: new point="
			<< (*le).second << std::endl;
		throw ErrProgrammingError(
		  "Loose end matching failed!  Found two consecutive starts.",
		  __FILE__, __LINE__);
	      }
	    } // end if currentEnd is null
	    else {
	      facet.addFaceEdges(currentEnd, &(*le).second, this);
	      currentEnd = nullptr;
	    } // end if currentEnd is not null
	  }   // end if this point is a loose start

	} // end loop over loose ends on edge
      }   // end loop over edges e of the face

      // If we get here with a non-null currentEnd, we must have
      // started in the middle of a segment, and firstStart must also
      // be non-null.
      if(currentEnd != nullptr) {
	if(firstStart == nullptr)
	  throw ErrProgrammingError("Missing start!", __FILE__, __LINE__);
	facet.addFaceEdges(currentEnd, firstStart, this);
      }

      // Remove pairs of equal and opposite segments.
      facet.removeOpposingEdges();

#ifdef DEBUG
      if(verboseface)
	oofcerr << "HomogeneityTet::findFaceFacets: face=" << face
		<< " before fixNonPositiveArea, facet=" << facet << std::endl;
#endif // DEBUG
      
      // Fix situations that can cause the area to be zero or negative.
      facet.fixNonPositiveArea(this, cat);
      
#ifdef DEBUG
      if(verboseface) {
	oofcerr << "HomogeneityTet::findFaceFacets: face=" << face
		<< " after fixNonPositiveArea, facet=" << facet << std::endl;
      }
#endif	// DEBUG
      
    } // end if face is not coincident with a pixel plane
    // if(!verify())
    //   throw ErrProgrammingError("Verification failed!", __FILE__, __LINE__);
    
    // #ifdef DEBUG
    //       else {
    // 	if(verbosecategory)
    // 	  oofcerr << "HomogeneityTet::findFaceFacets: skipping face on pixel plane"
    // 		  << std::endl;
    //       }
    // #endif // DEBUG

  }   // end loop over faces

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
#endif	// DEBUG
  return faceFacets;
} // HomogeneityTet::findFaceFacets

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#include <fstream>

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

FaceEdgeIntersection::FaceEdgeIntersection(
		   PlaneIntersection *crnr,
		   FaceFacetEdge *edge,
		   // const std::set<FaceFacetEdge*>::const_iterator &edge,
		   bool start)
  : crnr(crnr),
    t(-1.0),
    fEdge(NONE),
    segstart(start),
    edge_(edge)
{}

void FaceEdgeIntersection::findFaceEdge(unsigned int face, HomogeneityTet *htet)
{
  // Which edge of the face are we on?  findFaceEdge uses topological
  // information about intersections and faces, not numerical
  // information about positions.
  fEdge = crnr->findFaceEdge(face, htet);
  if(fEdge != NONE) {
    // Where on the edge?
    unsigned int node0, node1;
    getEdgeNodes(face, fEdge, node0, node1);
    BarycentricCoord b = htet->getBarycentricCoord(crnr->location3D());
    t = b[node1]/(b[node0] + b[node1]);
    if(t < 0)
      t = 0.0;
    else if(t > 1.0)
      t = 1.0;
  }
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
// and puts the point there, by inserting it into the LooseEndMap for
// that edge.

void FaceEdgeIntersection::forceOntoEdge(unsigned int face,
					 HomogeneityTet *htet)
{
  // The closest edge corresponds to the smallest barycentric
  // coordinate component other than the component for the node
  // opposite this face, which should already be zero.
  BarycentricCoord b = htet->getBarycentricCoord(crnr->location3D());
  int oppNode = CSkeletonElement::oppNode[face];
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

  unsigned int node0, node1;
  getEdgeNodes(face, fEdge, node0, node1);
  t = b[node1]/(b[node0] + b[node1]);
  if(t < 0)
    t = 0.0;
  else if(t > 1.0)
    t = 1.0;
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

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

FaceFacet::~FaceFacet() {
  for(FaceFacetEdge *edge : edges)
    delete edge;
}

void FaceFacet::addEdge(FaceFacetEdge *edge) {
  if(edge->isNull())
    return;
// #ifdef DEBUG
//   if(htet->verboseFace()) {
//     oofcerr << "FaceFacet::addEdge: face=" << face << " adding " << *edge
// 	    << std::endl;
//   }
// #endif // DEBUG
  areaComputed = false;
  edges.insert(edge);
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
  auto edge0 = edges.begin();
  while(edge0 != edges.end()) {
    auto edge1 = edge0;
    ++edge1;
    bool matched = false;
    for( ; edge1 != edges.end(); ++edge1) {
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
	  edges.erase(edge0);
	  edges.erase(edge1);
	  edge0 = nextedge;
	  matched = true;
	  break;
	}
    }
    if(!matched)
      ++edge0;
  }
}

Coord3D FaceFacet::getArea(HomogeneityTet *htet) const {
  Coord3D a;
  Coord3D fcenter = htet->faceCenter(face);
  for(const FaceFacetEdge *edge : edges) {
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
    homog_face = htet->microstructure->category(testVxl) == cat;
  }
#ifdef DEBUG
  if(htet->verboseFace()) {
    // oofcerr << "FaceFacet::fixNonPositiveArea: input facet=" << *this
    // 	    << std::endl;
    oofcerr << "FaceFacet::fixNonPositiveArea: raw_area=" << raw_area
	    << " homog_face=" << homog_face << std::endl;
  }
#endif // DEBUG
  if(raw_area < 0.0 || homog_face) {
    unsigned int n0 = CSkeletonElement::getFaceArray(face)[0];
    unsigned int n1 = CSkeletonElement::getFaceArray(face)[1];
    unsigned int n2 = CSkeletonElement::getFaceArray(face)[2];
    addEdge(new FaceFacetEdge(htet, new TripleFaceIntersection(n0, htet),
			      new TripleFaceIntersection(n1, htet)));
    addEdge(new FaceFacetEdge(htet, new TripleFaceIntersection(n1, htet),
			      new TripleFaceIntersection(n2, htet)));
    addEdge(new FaceFacetEdge(htet, new TripleFaceIntersection(n2, htet),
			      new TripleFaceIntersection(n0, htet)));
  }
}

std::ostream &operator<<(std::ostream &os, const FaceFacet &facet) {
  os << "FaceFacet(face=" << facet.face;
  if(facet.empty())
    os << ")";
  else {
    os << "," << std::endl;
    for(auto edge=facet.begin(); edge!=facet.end(); ++edge) {
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
  for(const FaceFacetEdge *edge : edges) {
    file << edge->startPos3D() << ", " << edge->endPos3D() << std::endl;
  }
  file.close();
}

std::string FaceFacet::shortDescription() const {
  std::string result;
  std::string spaces = "   ";
  for(const FaceFacetEdge *edge : edges)
    result += (spaces + to_string(edge->startPos3D()) + ", " +
	       to_string(edge->endPos3D()) + '\n');
  return result;
}

#endif // DEBUG
