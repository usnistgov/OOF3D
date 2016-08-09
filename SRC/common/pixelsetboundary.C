// -*- C++ -*-


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/cmicrostructure.h"
#include "common/geometry.h"
#include "common/pixelsetboundary.h"
#include "common/printvec.h"
#include "common/smallmatrix.h"
#include <assert.h>
#include <algorithm>
#include <limits>
#include <map>
#include <math.h>
#include <stdlib.h>


static const ICoord2D iRight(1, 0);
static const ICoord2D iUp(0, 1);
static const ICoord2D iLeft(-1, 0);
static const ICoord2D iDown(0, -1);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PixelSetBoundaryBase::PixelSetBoundaryBase(const CMicrostructure* ms)
  : microstructure(ms), bounds(0)
{}

PixelSetBoundaryBase::~PixelSetBoundaryBase() {
  for(std::vector<PixelBdyLoop*>::iterator i=loopset.begin(); i<loopset.end();
      ++i)
    delete *i;
  delete bounds;
}

// Add the boundary segments for this pixel to the map of all pixel
// segments.
void PixelSetBoundary::add_pixel(const ICoord2D &px) {
// #ifdef DEBUG
//   if(npixels == 0)
//     oofcerr << "PixelSetBoundary::add_pixel: first pixel! " << px << " this="
// 	    << this << std::endl;
//   else
//     oofcerr << "PixelSetBoundary::add_pixel: px=" << px << " this=" << this
// 	    << std::endl;
//   npixels++;
// #endif // DEBUG
  // Pixel boundary segments are actually just stored as ICoords,
  // which are the left or bottom endpoint of the segment.  The
  // direction of the segment is implied by which SegSet2D it's in.

  // Insert the L->R segment along the bottom of the pixel unless the
  // R->L one is already present.
  SegSet2D::iterator old = segmentsRL.find(px);
  if(old == segmentsRL.end())
    segmentsLR.insert(px);
  else
    segmentsRL.erase(old);

  // Insert the R->L segment along the top of the pixel unless the
  // L->R is already present.
  ICoord2D rl = px + iUp;
  old = segmentsLR.find(rl);
  if(old == segmentsLR.end())
    segmentsRL.insert(rl);
  else
    segmentsLR.erase(old);

  // Insert the U->D segment along the left edge unless the D->U is
  // already present.
  old = segmentsDU.find(px);
  if(old == segmentsDU.end())
    segmentsUD.insert(px);
  else
    segmentsDU.erase(old);

  // Insert the D->U segment along the right edge ...
  ICoord2D ud = px + iRight;
  old = segmentsUD.find(ud);
  if(old == segmentsUD.end())
    segmentsDU.insert(ud);
  else
    segmentsUD.erase(old);
}

typedef std::pair<ICoord2D, ICoord2D> DirectedSeg; // start point, direction

void PixelSetBoundary::find_boundary() {
  DirectedSegMap cm;
  delete bounds;
  // The remaining segments are all boundary segments.  Put them in a
  // more convenient map for making connections.  The map key is the
  // starting point of the segment, and the stored value is a pair
  // (DirectedSeg) containing the segment's direction and the pointer
  // to the segment itself.
  for(SegSet2D::iterator i=segmentsLR.begin(); i!=segmentsLR.end(); ++i)
    cm.insert(DirectedSeg(*i, iRight));
  for(SegSet2D::iterator i=segmentsDU.begin(); i!=segmentsDU.end(); ++i)
    cm.insert(DirectedSeg(*i, iUp));
  for(SegSet2D::iterator i=segmentsRL.begin(); i!=segmentsRL.end(); ++i)
    cm.insert(DirectedSeg(*i+iRight, iLeft));
  for(SegSet2D::iterator i=segmentsUD.begin(); i!=segmentsUD.end(); ++i)
    cm.insert(DirectedSeg(*i+iUp, iDown));

  // oofcerr << "PixelSetBoundary::find_boundary: cm=";
  // std::cerr << cm;
  // oofcerr << std::endl;

  // There must be at least one segment in each direction.  Find
  // loops, removing segments from the sets, until the sets are empty.
  while(!cm.empty()) {
    loopset.push_back(find_loop(cm));
  }
  assert(cm.empty());

  // Clean up.  Combine colinear contiguous segments and compute
  // bounding boxes. 
  for(std::vector<PixelBdyLoop*>::iterator loop=loopset.begin();
      loop!=loopset.end(); ++loop)
    {
      (*loop)->clean();		// removes extra points and computes bbox
      if(bounds == 0)
	bounds = new ICRectangle((*loop)->bbox());
      else
	bounds->swallow((*loop)->bbox());
    }
  segmentsLR.clear();
  segmentsRL.clear();
  segmentsUD.clear();
  segmentsDU.clear();
}


typedef std::pair<DirectedSegMap::iterator, DirectedSegMap::iterator> DirectedSegMapRange;

// Finds a loop in the passed-in coordinate map, and returns it.
// Removes the relevant segments from the cm, also, which is why cm is
// a reference and not const.

PixelBdyLoop *PixelSetBoundary::find_loop(DirectedSegMap &cm) {
  PixelBdyLoop *loop = new PixelBdyLoop();
  assert(!cm.empty());
  DirectedSegMap::iterator current = cm.begin();
  // oofcerr << "PixelSetBoundary::find_loop:" << std::endl;
  // OOFcerrIndent indent(2);

  bool done = false;
  while(!done) {
    ICoord2D here = (*current).first;
    ICoord2D direction = (*current).second;
    loop->add_point(here);
    ICoord2D next = here + direction; // endpoint of the current segment
    // oofcerr << "PixelSetBoundary::find_loop: here=" << here
    // 	    << " direction=" << direction << " next=" << next
    // 	    << std::endl;

    cm.erase(current);

    // Look for a segment starting at the end point of this one.
    int n = cm.count(next);
    if(n == 0)
      done = true;
    else if(n == 1) {
      current = cm.lower_bound(next);
    }
    else {
      // There is more than one choice of outgoing segment from the
      // current point.  This can happen only if two pixels in the set
      // touch at a corner, and the other two pixels at the corner are
      // not in the set, checkerboard style. Because the pixels in the
      // set are always on the left of the boundary, we know that
      // there are only two possible situations:  
      // A: The pixels are in the NE and SW corners. The incoming
      //    segments are vertical, and the outgoing segments are
      //    horizontal.  If we come in from the S we go out to the W.
      //    If we come in from the N we go out to the E.
      // B: The pixels are in the NW and SE corners.  The incoming
      //    segments are horizontal and the outgoing segments are
      //    vertical.  If we come in from the E we go out to the S.
      //    If we come in from the W we go out to the N.

      DirectedSegMapRange range = cm.equal_range(next); // poss. outgoing segs
      ICoord2D outgoing = (direction == iUp ? iLeft : // desired outgoing dir
			   (direction == iDown ? iRight :
			    (direction == iRight ? iUp :
			     iDown)));
      for(DirectedSegMap::iterator i=range.first; i!=range.second; ++i) {
	if((*i).second == outgoing) {
	  current = i;
	  break;
	}
      }	// loop over outgoing segments
    } // more than one outgoing segment
  } // while !done
#ifdef DEBUG
  if(loop->size() < 4 || !loop->closed()) {
    oofcerr << "PixelSetBoundary::find_loop: diff = "
	    << loop->loop.front() - loop->loop.back() << std::endl;
    throw ErrProgrammingError("Bad loop! size=" + to_string(loop->size()) +
			      " closed=" + to_string(loop->closed()),
			      __FILE__, __LINE__);
  }
#endif // DEBUG
  return loop;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PixelBdyLoop::PixelBdyLoop(const PixelBdyLoop &other)
  : loop(other.loop),		// vector copy
    bounds(0)
{
  if(other.bounds)
    bounds = new ICRectangle(*other.bounds);
}
							 
PixelBdyLoop::~PixelBdyLoop() {
  delete bounds; 
}

void PixelBdyLoop::add_point(const ICoord2D &pbs) {
  loop.push_back(pbs);
}

ICoord2D PixelBdyLoop::icoord(unsigned  int k) const {
  assert(k < loop.size());
  return loop[k];
}

ICoord2D PixelBdyLoop::next_icoord(unsigned int k) const {
  assert(k < loop.size());
  unsigned int kk = k + 1;
  if(kk == loop.size())
    return loop[0];
  return loop[kk];
}

bool PixelBdyLoop::left_turn(unsigned int k) const {
  unsigned int kprev = (k == 0 ? loop.size()-1 : k-1);
  unsigned int knext = (k == loop.size()-1 ? 0 : k+1);
  ICoord2D segA = loop[k] - loop[kprev];
  ICoord2D segB = loop[knext] - loop[k];
  return cross(segA, segB) > 0;
}

bool PixelBdyLoop::right_turn(unsigned int k) const {
  unsigned int kprev = (k == 0 ? loop.size()-1 : k-1);
  unsigned int knext = (k == loop.size()-1 ? 0 : k+1);
  ICoord2D segA = loop[k] - loop[kprev];
  ICoord2D segB = loop[knext] - loop[k];
  return cross(segA, segB) < 0;
}

ICoord2D PixelBdyLoop::next2_icoord(unsigned int k) const {
  assert(k < loop.size());
  unsigned int kk = k + 2;
  if(kk >= loop.size())
    return loop[kk - loop.size()];
  return loop[kk];
}

ICoord2D PixelBdyLoop::prev_icoord(unsigned int k) const {
  assert(k < loop.size());
  int kk = k - 1;
  if(kk < 0)
    return loop.back();
  return loop[kk];
}

bool PixelBdyLoop::horizontal(unsigned int k) const {
  assert(k >= 0 && k < loop.size());
  return icoord(k)[1] == next_icoord(k)[1];
}

bool PixelBdyLoop::decreasing(unsigned int k) const {
  // A decreasing segment is a horizontal segment that goes right to
  // left or a vertical segment that goes top to bottom.
  assert(k >= 0 && k < loop.size());
  ICoord2D here(icoord(k));
  ICoord2D next(next_icoord(k));
  return (here[0] == next[0] && here[1] > next[1]) || (here[0] > next[0]);
}

int PixelBdyLoop::windingNumber(const Coord2D &pt) const {
  // How many times does the loop wrap around the given point?  I.e,
  // how many times does a line drawn from the point to an arbitrary
  // exterior point cross the loop, counting counterclockwise
  // crossings as +1 and clockwise crossings as -1.

  // Requiring the point not to have integer coordinates eliminates
  // the need to worry about if it's on the boundary.  The outside
  // point doesn't actually have to be constructed.
  assert(floor(pt[0]) != pt[0] && floor(pt[1]) != pt[1]); 
  const double x = pt[0];
  const double y = pt[1];
  int ncross = 0;
  for(unsigned int k=0; k<loop.size(); k++) {
    // Only check vertical segments
    if(!horizontal(k)) {
      // Only check segments to the right of pt
      if(icoord(k)[0] > x) {
	int y0 = icoord(k)[1];
	int y1 = next_icoord(k)[1];
	if(y0 < y && y1 > y)
	  ncross += 1;
	else if(y1 < y && y0 > y)
	  ncross -= 1;
      }
    }
  }
  return ncross;
}

// Clean up the loop in-place, by extending segments for which the
// adjacent segment is just a continuation of the current segment.
// Also compute the bounding box.
void PixelBdyLoop::clean() {
  std::vector<ICoord2D>::iterator segend = loop.begin(); // end of current seg
  ++segend;
  ICoord2D segdir = *segend - loop.front(); // direction of current seg
  if(!bounds)
    delete bounds;
  bounds = new ICRectangle(*loop.begin(), *segend);
  std::vector<ICoord2D>::iterator next = segend; // next point to examine
  ++next;
  while(next != loop.end()) {
    // segend points to the end point of the current segment.  If the
    // next point extends the segment, just update *segend to be the
    // next point.  If the next point is in a different direction, the
    // old segend is the beginning of a new segment, and segend is
    // incremented to point to the new end point.
    ICoord2D nextdir = *next - *segend;
    if(nextdir != segdir) {	// Heading off in a new direction
      bounds->swallow(*next);
      ++segend;
      segdir = nextdir;
    }
    *segend = *next;
    ++next;
  }
  // The last retained entry in loop might be redundant if the
  // starting point is in line with it.  If it is redundant, delete it
  // and everything after it.  If it's not redundant, just delete
  // everything after it.
  if(*segend + segdir != loop.front())
    ++segend;
  loop.erase(segend, loop.end());
}

void PixelBdyLoop::find_bounds() {
  assert(!loop.empty());
  if(!bounds)
    delete bounds;
  std::vector<ICoord2D>::const_iterator pt = loop.begin();
  bounds = new ICRectangle(*pt, *pt);
  ++pt;
  for(; pt!=loop.end(); ++pt) {
    bounds->swallow(*pt);
  }
}

bool PixelBdyLoop::closed() const {
  // This is used to check consistency *before* clean() is called.  It
  // won't work afterwards.
  ICoord2D diff = loop.front() - loop.back();
  return (diff == iUp || diff == iDown || diff == iLeft || diff == iRight);
}

int PixelBdyLoop::area() const {
  int a = 0;
  for(unsigned int k=0; k<size(); k++) {
    ICoord2D x0 = icoord(k);
    ICoord2D x1 = next_icoord(k);
    a += cross(x0, x1);
  }
  return a/2;
}

bool PixelBdyLoop::contains(const ICoord2D &pt, unsigned int &k) const {
  for(unsigned int j=0; j<loop.size(); ++j) {
    if(loop[j] == pt) {
      k = j;
      return true;
    }
  }
  return false;
}

std::ostream &operator<<(std::ostream &os, const PixelBdyLoop &pbl) {
  return os << "PixelBdyLoop(" << pbl.loop << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool PixelBdyLoopSegment::operator<(const PixelBdyLoopSegment &other) const {
  if(firstPt() < other.firstPt())
    return true;
  else if(other.firstPt() < firstPt())
    return false;
  return secondPt() < other.secondPt();
}

bool PixelBdyLoopSegment::operator==(const PixelBdyLoopSegment &other) const {
  return (loop_ == other.loop_ && loopseg_ == other.loopseg_);
}

PixelBdyLoopSegment &PixelBdyLoopSegment::operator=(
					    const PixelBdyLoopSegment &other)
{
  loop_ = other.loop_;
  loopseg_ = other.loopseg_;
  return *this;
}

int PixelBdyLoopSegment::length() const {
  ICoord2D delta = secondPt() - firstPt();
  if(delta[0] == 0)
    return abs(delta[1]);
  return abs(delta[0]);
}

bool PixelBdyLoopSegment::onRight(const Coord2D &pt) const {
  ICoord2D a = firstPt();
  ICoord2D b = secondPt();
  return cross(pt - a, b - a) > 0.0;
}

std::ostream &operator<<(std::ostream &os, const PixelBdyLoopSegment &pbls) {
  os << "PixelBdyLoopSegment(" << pbls.firstPt() << ", " << pbls.secondPt()
     << ")";
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void PixelSetCrossSection::add_loop(PixelBdyLoop *loop) {
  loopset.push_back(loop);
  if(bounds == 0)
    bounds = new ICRectangle(loop->bbox());
  else
    bounds->swallow(loop->bbox());
}

// // PixelSetCrossSection::find_boundary assembles the segments located
// // by getPlaneCS into loops.  It's slightly different from
// // PixelSetBoundary::find_boundary because the segments aren't unit
// // segments and consecutive segments are guaranteed not to be
// // colinear.

// void PixelSetCrossSection::find_boundary(bool verbose) {
//   if(verbose) {
//     oofcerr << "PixelSetCrossSection::find_boundary: segmap=";
//     std::cerr << segmap;
//     oofcerr << std::endl;
//   }
//   while(!segmap.empty()) {
//     PixelBdyLoop *loop = new PixelBdyLoop();
//     SegMap::iterator current = segmap.begin();
//     ICoord2D start = (*current).first;
//     ICoord2D here = start;
//     ICoord2D prev = start;
//     loop->add_point(here);
//     ICoord2D next = (*current).second;
//     loop->add_point(next);
//     segmap.erase(current);
//     bool done = false;
//     while(!done) {
//       prev = here;
//       here = next;
//       // See how many end points are accessible from the previous end point
//       int n = segmap.count(here);
//       if(n == 1) {
// 	current = segmap.find(here);
// 	next = (*current).second;
// 	segmap.erase(current);
// 	if(next == start) {
// 	  done = true;
// 	}
// 	else {
// 	  loop->add_point(next);
// 	}
//       }	// end if n == 1
//       else if(n == 2) {
// 	// There are two segments going out from 'here'.  One must go
// 	// left and one right, since consecutive colinear segments are
// 	// impossible.  Choose the one that makes a left turn.
// 	SegMapRange range = segmap.equal_range(here);
// 	bool ok = false;
// 	SegMap::iterator deleteMe;
// 	for(SegMap::iterator smi=range.first; smi!=range.second && !ok; ++smi) {
// 	  next = (*smi).second;
// 	  if(cross(here-prev, next-here) > 0) { // found the left turn
// 	    ok = true;
// 	    deleteMe = smi;
// 	    if(next == start) {
// 	      done = true;
// 	    }
// 	    else {
// 	      loop->add_point(next);
// 	    }
// 	  } // end if found the left turn
// 	}   // end loop over possible outgoing segments smi
// 	assert(ok);
// 	// Deletion is done outside the loop, because range.second is
// 	// an invalid iterator after the point is deleted.
// 	segmap.erase(deleteMe);
//       }	    // end if n == 2
//       else {
// 	oofcerr << "PixelSetCrossSection::find_boundary: n=" << n << std::endl;
// 	oofcerr << "PixelSetCrossSection::find_boundary: segmap=" << std::endl;
// 	OOFcerrIndent indent(2);
// 	SegMapRange range = segmap.equal_range(here);
// 	for(SegMap::iterator i=range.first; i!=range.second; ++i)
// 	  oofcerr << "  " << (*i).first << " " << (*i).second << std::endl;
// 	throw ErrProgrammingError("PixelSetCrossSection::find_boundary failed!",
// 				  __FILE__, __LINE__);
//       }
//     } // end while not done (with the current loop)
//     assert(loop->size() >= 4);
//     loop->find_bounds();
//     loopset.push_back(loop);
//   } // end while segmap not empty
//   for(std::vector<PixelBdyLoop*>::iterator loop=loopset.begin();
//       loop!=loopset.end(); ++loop)
//     {
//       if(bounds == 0)
// 	bounds = new ICRectangle((*loop)->bbox());
//       else
// 	bounds->swallow((*loop)->bbox());
//     }
// }   // PixelSetCrossSection::find_boundary

std::ostream &operator<<(std::ostream &os, const VoxelSetBoundary &vsb) {
  os << "VoxelSetBoundary:  bounds=" << vsb.bbox() << std::endl;
  const PixelSetBoundaryMap &psbm(vsb.getPixelSetBdys());
  for(PixelSetBoundaryMap::const_iterator p=psbm.begin(); p!=psbm.end(); ++p) {
    os << "   PixelSetBoundary: " << (*p).second
       << " plane=" << (*p).first << std::endl;
    os << "       loops=";
    const std::vector<PixelBdyLoop*> &loops = (*p).second->get_loops();
    for(std::vector<PixelBdyLoop*>::const_iterator l=loops.begin();
	l!=loops.end(); ++l)
      os << "  " << **l;
    os << std::endl;
  }
  return os;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Plane::Plane(const Coord3D &normal, double offset, bool normalize)
  : unitNormal_(normal), offset_(offset)
{
  if(normalize)
    unitNormal_ /= sqrt(norm2(unitNormal_));
}

bool Plane::outside(const Coord3D &pt) const {
  return dot(unitNormal_, pt) > offset_;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// When we're doing 2D calculations on a plane of pixels, the plane is
// described by a PixelPlane object.  The PixelPlane takes care of
// converting from 3D coordinates to 2D coordinates.  PixelPlanes know
// what their positive normal direction is.

// PixelPlane::proj_dirs is a table that maps the 2D coordinates to
// the 3D coordinates, given the normal information.  The mapping is
// different for positive and negative normals so that a
// counterclockwise loop on a 2D plane will be mapped to a
// counterclockwise loop on the 3D plane that it's mapped to, whether
// or not the 3D plane's normal is positive or negative.

// proj_dirs[c] contains the indices of coords in a plane whose normal
// is in the c direction.  That is, proj_dirs[c][0] and
// proj_dirs[c][1] are the 3D axes that are mapped to the x and y axes
// in the plane.  proj_dirs[c+3] contains the of coords in a plane
// whose normal is in the -c direction.

const unsigned int PixelPlane::proj_dirs[6][2] =
  {{1,2},	    // c=0, normal=1
   {2,0},	    // c=1, normal=1
   {0,1},	    // c=2, norma1=1
   {2,1},	    // c=0, normal=-1
   {0,2},	    // c=1, normal=-1
   {1,0}};	    // c=2, normal=-1

PixelPlane::PixelPlane(unsigned int dir, int offst, int nrml)
  : Plane(axisVector(dir)*nrml, offst*nrml, false),
    proj_index(nrml==1 ? dir : dir+3),
    direction_(dir)
{
  assert(nrml == 1 || nrml == -1);
  assert(direction_ < 3);
}

// PixelPlane PixelPlane::inverted() const {
//   return PixelPlane(direction_, normalOffset(), offset_ > 0? -1 : 1);
// }

bool PixelPlane::contains(const Coord3D &pt) const {
  return pt[direction_] == unitNormal_[direction_]*offset_;
}

Coord2D PixelPlane::convert2Coord2D(const Coord3D &x) const {
  return Coord2D(x[proj_dirs[proj_index][0]], x[proj_dirs[proj_index][1]]);
}

ICoord2D PixelPlane::convert2Coord2D(const ICoord3D &x) const {
  return ICoord2D(x[proj_dirs[proj_index][0]], x[proj_dirs[proj_index][1]]);
}

Coord3D PixelPlane::convert2Coord3D(const Coord2D &x) const {
  Coord3D xxx;
  xxx[direction_] = unitNormal_[direction_]*offset_;
  xxx[proj_dirs[proj_index][0]] = x[0];
  xxx[proj_dirs[proj_index][1]] = x[1];
  return xxx;
}

ICoord3D PixelPlane::convert2Coord3D(const ICoord2D &x) const {
  ICoord3D xxx;
  xxx[direction_] = unitNormal_[direction_]*offset_;
  xxx[proj_dirs[proj_index][0]] = x[0];
  xxx[proj_dirs[proj_index][1]] = x[1];
  return xxx;
}

ICoord3D PixelPlane::convert2Voxel3D(const ICoord2D &x) const {
  ICoord3D xxx;
  if(unitNormal_[direction_] == 1.0)
    xxx[direction_] = offset_-1;
  else
    xxx[direction_] = offset_;
  xxx[proj_dirs[proj_index][0]] = x[0];
  xxx[proj_dirs[proj_index][1]] = x[1];
  return xxx;
}

int PixelPlane::getCategoryFromPoint(const CMicrostructure *ms,
				     const Coord2D &pt)
  const
{
  // pt is a Coord2D in *pixel* units.  Convert it to an ICoord2D by
  // truncation.
  ICoord2D ipt2(pt[0], pt[1]);
  // Convert the ICoord2D to an ICoord3D.
  ICoord3D x(convert2Voxel3D(ipt2));
  // oofcerr << "PixelPlane::getCategoryFromPoint: pt=" << pt
  // 	  << " ipt2=" << ipt2 << " x=" << x << std::endl;
  ICoord3D mssize = ms->sizeInPixels();
  for(unsigned int i=0; i<3; i++)
    if(x[i] == mssize[i])
      x[i] -= 1;
  // Get the voxel category.
  // oofcerr << "PixelPlane::getCategoryFromPoint: x=" << x << std::endl;
  return ms->category(x);
}

ICoord3D PixelPlane::normalVector() const {
  return ICoord3D(unitNormal_[0], unitNormal_[1], unitNormal_[2]);
  // ICoord3D nrml(0, 0, 0);
  // nrml[direction_] = normal_;	// +1 or -1
  // return nrml;
}

std::ostream &operator<<(std::ostream &os, const Plane &plane) {
  plane.print(os);
  return os;
}

void Plane::print(std::ostream &os) const {
  os << "Plane(" << this << ", offset=" << offset_
     << ", normal=" << unitNormal_ << ")";
}

void PixelPlane::print(std::ostream &os) const {
  os << "XYZ"[direction_] << "=" << normalOffset()
     << (normalSign() == 1 ? "+" : "-")
     // << " (" << this << ")"
    ;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelSetBoundary::~VoxelSetBoundary() {
  for(PixelSetBoundaryMap::iterator psb=pxlSetBdys.begin();
      psb!=pxlSetBdys.end(); ++psb)
    delete (*psb).second;
  for(PixelSetBoundaryMap::iterator psb=pxlSetCSs.begin();
      psb!=pxlSetCSs.end(); ++psb)
    delete (*psb).second;
  delete bounds;
}

void VoxelSetBoundary::addFace(const ICoord3D &where, unsigned int c, int norm)
{
  PixelPlane pp(c, where[c], norm);
  // TODO: Have PixelSetBoundaryMap store PixelSetBoundary objects,
  // not pointers, and use emplace here?
  PixelSetBoundaryMap::iterator psb = pxlSetBdys.find(pp);
  if(psb == pxlSetBdys.end()) {
// #ifdef DEBUG
//     oofcerr << "VoxelSetBoundary::addFace: new PixelPlane " << pp << std::endl;
// #endif // DEBUG
    PixelSetBoundary *b = new PixelSetBoundary(microstructure);
    pxlSetBdys[pp] = b;
    b->add_pixel(pp.convert2Coord2D(where));
  }
  else {
    (*psb).second->add_pixel(pp.convert2Coord2D(where));
  }
// #ifdef DEBUG
//   oofcerr << "VoxelSetBoundary::addFace: added " << where
// 	  << " " << pp.convert2Coord2D(where)
// 	  << " to " << pp
// 	  << std::endl;
// #endif // DEBUG
}   // end VoxelSetBoundary::addFace

void VoxelSetBoundary::find_boundaries() {
  delete bounds;
  bounds = 0;
  for(PixelSetBoundaryMap::iterator i=pxlSetBdys.begin(); i!=pxlSetBdys.end();
      ++i)
    {
      PixelSetBoundary *psb = (*i).second;
      const PixelPlane &pixelplane = (*i).first;
// #ifdef DEBUG
//       oofcerr << "VoxelSetBoundary::find_boundaries: calling find_boundary for pixelplane="
// 	      << pixelplane << std::endl;
//       OOFcerrIndent indent(2);
// #endif // DEBUG
      psb->find_boundary();
      ICoord3D c0 = pixelplane.convert2Coord3D(psb->bbox().upperright());
      ICoord3D c1 = pixelplane.convert2Coord3D(psb->bbox().lowerleft());
      if(!bounds)
	bounds = new ICRectangularPrism(c0, c1);
      else {
	bounds->swallow(c0);
	bounds->swallow(c1);
      }
    }
}



// getPlaneCS finds the perimeter of the intersection of a PixelPlane,
// pixplane, and the VoxelSetBoundary.  It does this by examining the
// PixelSetBoundary planes of the VoxelSetBoundary that intersect the
// given PixelPlane.  Those planes must be orthogonal to pixplane.

// getPlaneCS is called by findPixelPlaneFacets (in tetintersection.C)
// when looking for facets on a pixel plane that coincides with a tet
// face.

//#define DEBUG_PLANECS

const std::vector<PixelBdyLoop*> &VoxelSetBoundary::getPlaneCS(
					       const PixelPlane &pixplane,
					       unsigned int category
#ifdef DEBUG
					       , bool verbose
#endif // DEBUG
							       )
  const
{
#ifdef DEBUG_PLANECS
  if(verbose)
    oofcerr << "VoxelSetBoundary::getPlaneCS: pixplane=" << pixplane
  	    << std::endl;
  OOFcerrIndent indent(2);
#endif // DEBUG_PLANECS
  // See if the cross section has already been computed.
  PixelSetBoundaryMap::const_iterator psbmi = pxlSetCSs.find(pixplane);
  if(psbmi != pxlSetCSs.end())
    return (*psbmi).second->get_loops();

  // Create new cross section.
  PixelSetBoundary *pscs = new PixelSetBoundary(microstructure);
  pxlSetCSs[pixplane] = pscs;

  // TODO: See if the cross section on the inverted pixel plane has
  // already been computed.  Copy it, reverse the direction of its
  // segments, and flip the coordinates.

  ICoord2D planesize = pixplane.convert2Coord2D(microstructure->sizeInPixels());
  int offset = pixplane.normalOffset();
  if(offset != 0 &&
     offset != microstructure->sizeInPixels()[pixplane.direction()])
    {
      for(unsigned int i=0; i<planesize[0]; i++) {
	for(unsigned int j=0; j<planesize[1]; j++) {
	  ICoord2D pxl(i, j);
	  ICoord3D vxl0 = pixplane.convert2Coord3D(pxl);
	  ICoord3D vxl1 = vxl0;
	  vxl1[pixplane.direction()] -= 1;
	  if(microstructure->category(vxl0) == category &&
	     microstructure->category(vxl1) == category)
	    {
	      pscs->add_pixel(pxl);
	    }
	} // end loop over j
      } // end loop over i
    }
  pscs->find_boundary();
  return pscs->get_loops();
} // VoxelSetBoundary::getPlaneCS

// #ifdef DEBUG
// void VoxelSetBoundary::dumpPSBs() const {
//   for(PixelSetBoundaryMap::const_iterator psb=pxlSetBdys.begin();
//       psb!=pxlSetBdys.end(); ++psb)
//     {
//       oofcerr << "VoxelSetBoundary::dumpPSBs: pixel plane="
// 	      << (*psb).first << std::endl;
//       OOFcerrIndent indent(2);
//       (*psb).second->dump();
//     }
// }

// void PixelSetBoundary::dump() const {
//   oofcerr << "PixelSetBoundary::dump: LR=";
//   std::cerr << segmentsLR;
//   oofcerr << std::endl;
//   oofcerr << "PixelSetBoundary::dump: RL=";
//   std::cerr << segmentsRL;
//   oofcerr << std::endl;
//   oofcerr << "PixelSetBoundary::dump: UD=";
//   std::cerr << segmentsUD;
//   oofcerr << std::endl;
//   oofcerr << "PixelSetBoundary::dump: DU=";
//   std::cerr << segmentsDU;
//   oofcerr << std::endl;
// }
// #endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Coord3D triplePlaneIntersection(const Plane *plane0, const Plane *plane1,
				const Plane *plane2)
{
  // Compute the intersection point of the planes.
  SmallMatrix normals(3, 3);
  SmallMatrix offsets(3, 1);
  for(unsigned int i=0; i<3; i++) {
    normals(0, i) = plane0->normal()[i];
    normals(1, i) = plane1->normal()[i];
    normals(2, i) = plane2->normal()[i];
  }
  offsets(0, 0) = plane0->offset();
  offsets(1, 0) = plane1->offset();
  offsets(2, 0) = plane2->offset();
  if(normals.solve(offsets) != 0) {
    oofcerr << "triplePlaneIntersection::point: plane0=" << *plane0 <<std::endl;
    oofcerr << "triplePlaneIntersection::point: plane1=" << *plane1 <<std::endl;
    oofcerr << "triplePlaneIntersection::point: plane2=" << *plane2 <<std::endl;
    throw ErrProgrammingError("triplePlaneIntersection could not be found",
			      __FILE__, __LINE__);
  }
  Coord3D isec(offsets(0, 0), offsets(1, 0), offsets(2, 0));
  // oofcerr << "triplePlaneIntersection: " << *plane0 << " " << *plane1 << " "
  // 	  << *plane2 << " --> " << isec << std::endl;
  return isec;
}

Coord3D triplePlaneIntersection(const PixelPlane *p0, const PixelPlane *p1,
				const PixelPlane *p2)
{
  assert(p0->direction() != p1->direction() &&
	 p1->direction() != p2->direction() &&
	 p2->direction() != p0->direction());
  Coord3D pt;
  pt[p0->direction()] = p0->normalOffset();
  pt[p1->direction()] = p1->normalOffset();
  pt[p2->direction()] = p2->normalOffset();
  return pt;
}


bool Plane::nonDegenerate(const Plane *planeA, const Plane *planeB) const {
  // TODO: Do we need a tolerance here?  Hopefully not.
  return dot(normal(), cross(planeA->normal(), planeB->normal())) != 0;
}
