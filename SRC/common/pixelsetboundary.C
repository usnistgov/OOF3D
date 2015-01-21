// -*- C++ -*-
// $RCSfile: pixelsetboundary.C,v $
// $Revision: 1.34.10.20 $
// $Author: langer $
// $Date: 2014/12/12 19:38:52 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modifed
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/pixelsetboundary.h"
#include "common/cmicrostructure.h"
#include "common/geometry.h"
#include "common/printvec.h"
#include <map>
#include <math.h>

#include <assert.h>

#if DIM==2

bool PixelBdySegment::operator<(const PixelBdySegment &other) const {
  if (other.horizontal == horizontal)
    return (other.pixel < pixel);
  return (other.horizontal < horizontal);
// That is,
//   if (!other.horizontal && horizontal) return true;
//   if (!horizontal && other.horizontal) return false;
}


// This both assigns coordinates and directs the segment, but it still
// lives in integer-land.  It sets the mutable data members "start",
// "end" and "coordinated".
ICoord PixelBdySegment::coordinate() const {
  ICoord lowerleft = pixel;

  if (horizontal) {
    ICoord lowerright = lowerleft + ICoord(1, 0);
    if (local) {
      start = lowerleft;
      end = lowerright;
    }
    else { 
      end = lowerleft; 
      start = lowerright;
    }
  }
  else {
    ICoord upperleft = lowerleft + ICoord( 0, 1 );
    if (local) {
      start = upperleft;
      end = lowerleft;
    }
    else {
      start = lowerleft;
      end = upperleft;
    }
  }
  coordinated = true;
  return start;
}

void PixelBdySegment::extend() {
  if (horizontal) {
    if (local) 
      end += ICoord(1,0);
    else
      end -= ICoord(1,0);
  }
  else {
    if (local) 
      end -= ICoord(0,1);
    else
      end += ICoord(0,1);
  }
}


// Set the boundary points in physical space.
void PixelBdySegment::set_floats(const Coord &delta) const {
  if (horizontal) {
    fp_level = start[1]*delta[1];  // Segment has constant y
    fp_start = start[0]*delta[0];
    fp_end = end[0]*delta[0];
  }
  else {
    fp_level = start[0]*delta[0];  // Segment has constant x.
    fp_start = start[1]*delta[1];
    fp_end = end[1]*delta[1];
  }

  if (fp_start < fp_end) {
    fp_first = fp_start;
    fp_last = fp_end;
  }
  else {
    fp_first = fp_end;
    fp_last = fp_start;
  }

  floated = true;
}

// Not as stupid as it looks -- this routine helps resolve the "zero
// or two intersections" case by giving a definitive yes-or-no to the
// question of whether or not there are zero intersections between
// this pixel boundary segment and the element defined by the
// passed-in point list (pts).  The strategy is: if both endpoints of
// this pixel boundary segment are exterior to the same element
// segment, then no intersection is possible; failing that, the
// endpoints of the pixel boundary segment must terminate in different
// sectors, so if all of the element-corner coordinates are on the
// same side of the pixel boundary segment, then an intersection is
// impossible; failing *that*, an intersection (actually, two) is
// required.  The caller promises that both end-points of the pixel
// boundary segment are exterior to the passed-in element (using an
// interiority test which takes the same cross-products as this
// routine), and we assume convexity of the element.

// pts is passed as an array and a size, instead of a std::vector, for
// efficiency.

bool PixelBdySegment::find_no_intersection(const Coord* const pts,
					   int npts,
					   const Coord &perturb) const
{
  
  const Coord start = start_pt();
  const Coord end = end_pt();
    
  // loop over sides of the element 
  for(int i1=0; i1<npts; ++i1) {
    int i2 = (i1+1)%npts;
    // This is the same arithmetic as the CSkeletonElement::interior
    // function -- this is important for avoiding roundoff-related
    // screwups.
    const Coord eside = pts[i2] - pts[i1];
    double start_cross = eside % (start-pts[i1]);
    double end_cross = eside % (end-pts[i1]);

    // Easy case -- if they're both negative for this segment, then
    // there are no intersections, we're done.
    if ( (start_cross < 0) && (end_cross < 0) ) 
      return true;

    // In the boundary case, check against perturbations.
    double delta = perturb % eside;
    bool start_ok = (start_cross < 0) || ( (start_cross==0) && (delta < 0) );
    bool end_ok = (end_cross < 0) || ( (end_cross==0) && (delta < 0) );
    if (start_ok && end_ok) return true;
  } // end loop over sides of the element

  // If we made it this far, then the endpoints must be exterior in
  // different "sectors".  In this case, we can still rule out
  // intersections if all of the element nodes are on the same side of
  // the pixel boundary segment.  Find out which side the first one is
  // on.  If any of the others are on a different side, return false,
  // indicating that intersections are required.

  double initial_res = (pts[0]-start)%(end-start);
  double delta = perturb%(end-start);
  if (initial_res==0)
    initial_res = delta;

  for(int i1=1; i1<npts; ++i1) {
    double new_res = (pts[i1]-start)%(end-start);
    if ( initial_res*new_res < 0) return false; // Intersection required.
    if ( (new_res==0) && (initial_res*delta < 0) ) return false;
  }
  // If we didn't succeed in the first block, or fail in the second
  // block, then there are no intersections.

  return true;
}
				      




// Quick intersection-finding routine, used when you have topological
// information about what's going on.  Specifically, you know that
// it's geometrically required that the pixel boundary segment must
// intersect the passed-in set of coordinates exactly once, you know
// whether it enters or exits, and the only real question is where
// this occurs.  First argument is a vector of points, making up a
// closed convex polygon (convexity is assumed, the caller should
// ensure this), and the second argument is a PixelBdyIntersection
// structure which will be filled in by this routine.  The third
// argument is the classification (entry or exit) of the searched-for
// intersection.  Currently this is just put in the pbi, but it could
// be checked for consistency.  The return value is an integer
// indicating on which element segment the intersection occurred.
int 
PixelBdySegment::find_one_intersection(const Coord * const pts, int npts,
				       PixelBdyIntersection &pbi,
				       bool entry) const {
  // Alpha is the fractional distance along an element segment, and
  // beta is the fractional distance along this segment from fp_first
  // to fp_last.  The "t_" prefix counterparts are intermediate trial
  // versions of these quantities.  "Error" is a postive-definite
  // measure of how far out of bounds the trial quantities are.
  int segment = -1;
  double alpha, beta, t_beta=0.0, error=0.0;

  // Transfer the passed-in classification info.
  pbi.entry = entry;

  if (horizontal) {
    for(int i1=0;i1<npts;++i1) {
      int i2 = (i1+1)%npts;
      // Ignore the parallel case.
      if (pts[i1][1]==pts[i2][1]) continue;
      // Also skip segments which are oriented incorrectly for the
      // type of intersection we want.
      bool seg_entry = !( (local && (pts[i2][1]>pts[i1][1])) || 
			  (!local && (pts[i2][1]<pts[i1][1])) );
      if (seg_entry != entry) continue;
      
      alpha=(fp_level-pts[i1][1]) / (pts[i2][1]-pts[i1][1]);
      beta =((fp_first-pts[i1][0])-(pts[i2][0]-pts[i1][0])*alpha)/
	(fp_first-fp_last);
      // If the trial alpha/beta is in-bounds, we're done.
      if (( alpha > 0) && (alpha <1) && (beta > 0) && (beta <1)) {
	pbi.location = Coord(fp_first+beta*(fp_last-fp_first),fp_level);
	return i1;
      }
      // Compute how far out of bounds we ended up.
      double new_error=0.0;
      
      if (alpha>1) new_error = (alpha-1.0)*(alpha-1.0);
      if (alpha<0) new_error = alpha*alpha;
      if (beta>1) new_error += (beta-1.0)*(beta-1.0);
      if (beta<0) new_error += beta*beta;
      
      // If this is the first iteration, or if the new error is
      // smaller than the already-stored error, save the results.
      if ((segment==-1) || ( new_error < error)) {
	segment = i1;
	t_beta = beta;
	error = new_error;
      }

    } // End of the for-loop.
    // If we made it out of the loop, that means none of the element
    // segments were in-bounds.  But the caller insists there must be
    // an intersection, so we'll return our best guess.
    pbi.location = Coord(fp_first+t_beta*(fp_last-fp_first), fp_level);
    assert(segment!=-1);
    return segment;
  }
  else { // Vertical
    for(int i1=0;i1<npts;++i1) {
      int i2 = (i1+1)%npts;
      // Again, ignore the parallel case.
      if (pts[i1][0]==pts[i2][0]) continue;
      // And again, ignore wrongly oriented segments.
      bool seg_entry = !( ( local && (pts[i2][0]>pts[i1][0]) ) ||
			  ( !local && (pts[i2][0]<pts[i1][0])) );
      if (seg_entry != entry) continue;

      alpha = (fp_level-pts[i1][0])/(pts[i2][0]-pts[i1][0]);
      beta = ((fp_first-pts[i1][1])-(pts[i2][1]-pts[i1][1])*alpha)/
	(fp_first-fp_last);
      
      // If we're in-bounds, we're done.
      if (( alpha>0) && (alpha<1) && (beta>0) && (beta<1)) {
	pbi.location = Coord(fp_level, fp_first+beta*(fp_last-fp_first));
	return i1;
      }
      double new_error=0.0;
      
      if (alpha>1) new_error = (alpha-1.0)*(alpha-1.0);
      if (alpha<0) new_error = alpha*alpha;
      if (beta>1) new_error += (beta-1.0)*(beta-1.0);
      if (beta<0) new_error += beta*beta;
      
      if ((segment==-1) || (new_error < error)) {
	segment = i1;
	t_beta = beta;
	error = new_error;
      }
    }
    // If we made it this far, we were never in-bounds.  Return best-guess.
    pbi.location = Coord(fp_level, fp_first+t_beta*(fp_last-fp_first));
    assert(segment!=-1);
    return segment;
  }
}
    
					    

std::ostream& operator<<(std::ostream &o, const PixelBdySegment &pbs) {
  if (pbs.floated) {
    if (pbs.horizontal) {
      o << "(" << pbs.fp_start << ", " << pbs.fp_level << 
	") -> (" << pbs.fp_end << ", " << pbs.fp_level << ")";
    }
    else {
      o << "( " << pbs.fp_level << ", " << pbs.fp_start << 
	") -> (" << pbs.fp_level << ", " << pbs.fp_end << ")";
    }
  }
  else if (pbs.coordinated) {
    o << "[" << pbs.start << ", " << pbs.end << "]";
  }
  else {
    o << (pbs.horizontal ? " Horizontal " : " Vertical ") << 
      (pbs.local ? " Local " : " Nonlocal ") << pbs.pixel;
  }
  return o;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PixelSetBoundary::PixelSetBoundary(const CMicrostructure* ms)
  : segments(), microstructure(ms), loopset(0)
{
  ms_delta = microstructure->sizeOfPixels();
}

PixelSetBoundary::~PixelSetBoundary() {
  for(std::vector<PixelBdyLoop*>::iterator i=loopset.begin(); i<loopset.end();
      ++i)
    delete *i;
}

// Create the boundary segments for this pixel, and add them to the
// map of all pixel segments.  PixelBdySegment constructor args are
// pixel ICoord, horizontality, and locality.
void PixelSetBoundary::add_pixel(const ICoord &px) {
  segments[PixelBdySegment(px, true, true)] += 1;
  segments[PixelBdySegment(px, false, true)] += 1;

  ICoord neighbor = px + ICoord(0,1);
  segments[PixelBdySegment(neighbor, true, false)] += 1;
  
  neighbor = px + ICoord(1,0);
  segments[PixelBdySegment(neighbor, false, false)] += 1;
}


typedef std::pair<ICoord, PixelBdySegment> SegByCoord;

void PixelSetBoundary::find_boundary() {
  CoordMap coordmap;		// Coord-keyed map of segments.

  // Remove the segments which occur twice -- they are interior.
  SegMap::iterator i = segments.begin();
  while(i!=segments.end()) {
    if ((*i).second == 2) {
      SegMap::iterator j = i;
      ++i;
      segments.erase(j);
    }
    else {
      ++i;
    }
  }

  // At this point, the keys in the "segments" map all have value "1",
  // and are grouped, but not in a useful way.  The geometry of the
  // pixel array guarantees that we have at least four segments.
  // Put them in a new multimap, indexed by their start coords.
  // Avoid making a copy of the PixelBdySegment.
  for(SegMap::iterator s=segments.begin(); s!=segments.end(); ++s) {
    const PixelBdySegment &pbs = (*s).first;
    ICoord segment_start = pbs.coordinate();
    coordmap.insert( SegByCoord(segment_start, pbs ) );
  } 
  segments.clear();

  // Now we have a Coord-indexed multimap of segment objects, and
  // furthermore, all of the indices are the start of a coordinated
  // segment.  Now, construct the loops, merrily erasing as we go.
  
  while (!coordmap.empty()) {
    loopset.push_back(find_loop(coordmap));
  }

  for(std::vector<PixelBdyLoop*>::iterator ell = loopset.begin();
      ell!=loopset.end(); ++ell)
    {
      // Optimization: Clean up redundant segments from the loops.
      (*ell)->clean();
      // set_floats in all the segments (which also computes bbox).
      (*ell)->set_floats(ms_delta);
   }
}


typedef std::pair<CoordMap::iterator, CoordMap::iterator> CoordMapRange;
 
// Finds a loop in the passed-in coordinate map, and returns it.
// Removes the relevant segments from the cm, also, which is why it's
// a reference and not const.
PixelBdyLoop *PixelSetBoundary::find_loop(CoordMap &cm) {
  PixelBdyLoop *result = new PixelBdyLoop;
  assert(!cm.empty());
  CoordMap::iterator current = cm.begin();
  
  bool done = false;
  while (!done) {
    PixelBdySegment current_seg = (*current).second;
    result->add_segment(current_seg);
    ICoord next = current_seg.end;
    cm.erase(current);

    int n = cm.count(next);
    
    if (n==0)
      done=true;
    else if (n==1) {
      current = cm.lower_bound(next);
    }
    else {
      // There is more than one choice of outgoing segment from the
      // current point.  This can only happen if two pixels in the set
      // touch at a corner, and the other two pixels at the corner are
      // not in the set, checkerboard style. Because the pixels in the
      // set are always on the left of the boundary, we know that
      // there are only two possible situations:  
      // A: The pixels are in the NE and SW corners. The incoming
      //    segments are vertical, and the outgoing segments are
      //    horizontal.  If we come in from the S we go out to the W
      //    and both segments are local.  If we come in from the N
      //    we go out to the E and both segments are nonlocal.
      // B: The pixels are in the NW and SE corners.  The incoming
      //    segments are horizontal and the outgoing segments are
      //    vertical.  If we come in from the E we go out to the S,
      //    and the incoming segment is nonlocal while the outgoing
      //    segment is local.  If we come in from the W we go out to
      //    the N, and the incoming segment is local while the
      //    outgoing segment is nonlocal.

      // Examine the outgoing segments and set "current" to the
      // correct one, using the "local" information.
      CoordMapRange range = cm.equal_range(next); // possible outgoing segments
      for (CoordMap::iterator i = range.first; i!=range.second; ++i) {
	if((current_seg.horizontal && (current_seg.local!=(*i).second.local))
	   ||
	   (!current_seg.horizontal && (current_seg.local==(*i).second.local)))
	  {
	    current = i;
	    break; 
	  }
      }	// loop over outgoing segments
    } // more than one outgoing segment
  } // while(!done)
  return result;
}

//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//\\//
							 
void PixelBdyLoop::add_segment(const PixelBdySegment &pbs) {
  loop.push_back(pbs);
}

// Cleans up the loop in-place, by extending segments for which the
// adjacent segment is just a continuation of the current segment.
void PixelBdyLoop::clean() {
  std::vector<PixelBdySegment>::iterator current = loop.begin();
  std::vector<PixelBdySegment>::iterator i = current;
  i++;
  // STL semantics are such that iterators preceding the erasure point
  // remain valid after an erasure, but those afterwards do not, so
  // current < i is important.
  while(i!=loop.end()) {
    if ((*i).horizontal == (*current).horizontal) {
      (*current).extend();
      loop.erase(i);
      i = current;
      i++;
    }
    else {
      current = i;
      i++;
    }
  }
}

void PixelBdyLoop::set_floats(const Coord &delta) {
  assert(!loop.empty());
  bool first = true;
  for(std::vector<PixelBdySegment>::iterator x=loop.begin(); x!=loop.end(); ++x)
    {
      (*x).set_floats(delta);
      if(first) {
	bounds = new CRectangle((*(loop.begin())).start_pt(),
				(*(loop.begin())).end_pt());
	first = false;
      }
      else {
	bounds->swallow((*x).start_pt());
	bounds->swallow((*x).end_pt());
      }
    }
}

PixelBdyLoop::~PixelBdyLoop() {
  delete bounds; 
}

std::ostream &operator<<(std::ostream &os, const PixelBdyLoop &pbl) {
  return os << "PixelBdyLoop(" << pbl.loop << ")";
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


#elif DIM==3

// proj_dirs[i] contains the in-plane indices of coords in a plane
// whose normal is in the i direction.  TODO: Check that it's faster
// to look up values in proj_dirs than it is to calculate (i+j+1)%3.
const short VoxelSetBoundary::proj_dirs[3][2] = 
  {{1,2},
   {2,0},
   {0,1}};

const ICoord VoxelSetBoundary::dirs[6] =
  {ICoord(-1,0,0),
   ICoord(0,-1,0),
   ICoord(0,0,-1),
   ICoord(1,0,0),
   ICoord(0,1,0),
   ICoord(0,0,1)};

// faces[i][j] is the position of the jth corner of the ith face of a
// unit voxel.  Only the faces containing (0,0,0) are included.  The
// corners are numbered counterclockwise around the *inward* normal.
const ICoord VoxelSetBoundary::faces[3][4] = {
  {ICoord(0,0,0),ICoord(0,1,0),ICoord(0,1,1),ICoord(0,0,1)}, // left, x=0
  {ICoord(0,0,0),ICoord(0,0,1),ICoord(1,0,1),ICoord(1,0,0)}, // bottom, y=0
  {ICoord(0,0,0),ICoord(1,0,0),ICoord(1,1,0),ICoord(0,1,0)}}; // back, z=0

VoxelSetBoundary::~VoxelSetBoundary() 
{
  for(int i=0; i<3; ++i) {
    for(PlanesOfQuads::iterator pq=quads[i].begin(); pq!=quads[i].end(); ++pq) {
      for(QuadVector::iterator q=(*pq).second->begin(); q!=(*pq).second->end();
	  ++q)
	{
	  delete *q;
	}
      delete (*pq).second;
    }
  }
}


void VoxelSetBoundary::add_face(const ICoord &where, int c, int norm) {
  Quad *q = new Quad;
  for(int k=0; k<4; ++k) {
    ICoord facepoint = where + faces[c][k];
    // When calculating the homogeneity, we always want the coords in
    // a counterclockwise order.  The direction of the normal is
    // stored explicitly.
    q->coords[k][0] = facepoint[proj_dirs[c][0]];
    q->coords[k][1] = facepoint[proj_dirs[c][1]];
  }
  q->norm = norm;
  q->area = 1;
  q->height = where[c];
  q->norm_dir = c;
  PlanesOfQuads::iterator pq = quads[c].find(q->height);
  if(pq == quads[c].end()) {
    // This is the first Quad found in direction c at height where[c].
    quads[c][q->height] = new QuadVector;
    quads[c][q->height]->push_back(q);
  }
  else {
    // We already have a list of Quads at this height.  Can the new
    // one be merged with an old one?
    bool joinedcell = false;
    QuadVector *qv = (*pq).second; // Previous Quads found at this height
    // Loop over the quads in reverse.  We can take
    // advantage of our convention for ordering the points
    // in the quad to check whether two quads should be
    // joined.  
    for(QuadVector::reverse_iterator rqi=qv->rbegin(); rqi<qv->rend(); ++rqi) {
      Quad *oq = *rqi;
      // TODO OPT: some of these probably aren't necessary
      if(oq->norm == q->norm) {
	if(oq->coords[1][0] == q->coords[0][0] &&
	   oq->coords[1][1] == q->coords[0][1] &&
	   oq->coords[2][0] == q->coords[3][0] &&
	   oq->coords[2][1] == q->coords[3][1])
	  {
	    // oofcerr << "VoxelSetBoundary::add_face: merging " << *oq
	    // 	    << std::endl
	    // 	    << "                                and " << *q
	    // 	    << std::endl;
	    oq->coords[1][0] = q->coords[1][0];
	    //oq->coords[1][1] = q->coords[1][1];
	    oq->coords[2][0] = q->coords[2][0];
	    //oq->coords[2][1] = q->coords[2][1];
	    oq->area += 1;
	    // oofcerr << "                            to form " << *oq
	    // 	    << std::endl;
	    joinedcell = true;
	    break;
	  }
	else if(oq->coords[0][0] == q->coords[1][0] &&
		oq->coords[0][1] == q->coords[1][1] &&
		oq->coords[3][0] == q->coords[2][0] &&
		oq->coords[3][1] == q->coords[2][1])
	  {
	    oq->coords[0][0] = q->coords[0][0];
	    //oq->coords[0][1] = q->coords[0][1];
	    oq->coords[3][0] = q->coords[3][0];
	    //oq->coords[3][1] = q->coords[3][1];
	    oq->area += 1;
	    joinedcell = true;
	    break;
	  }
	else if(oq->coords[0][0] == q->coords[3][0] &&
		oq->coords[0][1] == q->coords[3][1] &&
		oq->coords[1][0] == q->coords[2][0] &&
		oq->coords[1][1] == q->coords[2][1])
	  {
	    //oq->coords[0][0] = q->coords[0][0];
	    oq->coords[0][1] = q->coords[0][1];
	    //oq->coords[1][0] = q->coords[1][0];
	    oq->coords[1][1] = q->coords[1][1];
	    oq->area += 1;
	    joinedcell = true;
	    break;
	  }
	else if(oq->coords[3][0] == q->coords[0][0] &&
		oq->coords[3][1] == q->coords[0][1] &&
		oq->coords[2][0] == q->coords[1][0] &&
		oq->coords[2][1] == q->coords[1][1])
	  {
	    //oq->coords[3][0] = q->coords[3][0];
	    oq->coords[3][1] = q->coords[3][1];
	    //oq->coords[2][0] = q->coords[2][0];
	    oq->coords[2][1] = q->coords[2][1];
	    oq->area += 1;
	    joinedcell = true;
	    break;
	  }
      }	// end if normal directions are equal
    } // end loop over previously found Quads
    if(!joinedcell)
      quads[c][q->height]->push_back(q);
    else
      delete q;
  } // end if not empty quads
}   // end VoxelSetBoundary::add_face

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Quad::Quad() {
// #ifdef DEBUG
//   allQuads.insert(this);
// #endif // DEBUG
}

Quad::~Quad() {
// #ifdef DEBUG
//   allQuads.erase(this);
// #endif
}

std::ostream &operator<<(std::ostream &os, const Quad &q) {
  os << "Quad([";
  for(int i=0; i<4; i++) {
    os << "(" << q.coords[i][0] << "," << q.coords[i][1] << ")";
    if(i<3)
      os << ",";
    else
      os << "],";
  }
  os << " h=" << q.height << ", norm_dir=" << q.norm_dir << ")";
  return os;
}

// #ifdef DEBUG

// std::set<const Quad*> Quad::allQuads;

// bool Quad::validQuad(const Quad *q) {
//   return allQuads.find(q) != allQuads.end();
// }

// #endif // DEBUG

#endif	// DIM==3
