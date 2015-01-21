// -*- C++ -*-
// $RCSfile: pixelselectioncourier.C,v $
// $Revision: 1.18.8.16 $
// $Author: langer $
// $Date: 2014/08/02 03:14:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "common/ccolor.h"
#include "common/colordifference.h"
#include "common/cmicrostructure.h"
#include "common/pixelselectioncourier.h"
#include "common/printvec.h"
#include "common/IO/oofcerr.h"
#if DIM==2
#include "common/brushstyle.h"
#endif
#include <math.h>
#include <iostream>
#include <iomanip>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PixelSelectionCourier::PixelSelectionCourier(CMicrostructure *ms)
  : ms(ms),
    done_(false)
 {}

ICoord PixelSelectionCourier::pixelFromPoint(const Coord &pt) const {
  return ms->pixelFromPoint(pt);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PointlessSelection::PointlessSelection(CMicrostructure *ms) 
  : PixelSelectionCourier(ms)
{
  done_ = true;
}

ICoord PointlessSelection::currentPoint() const {
  return ICoord();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PointSelection::PointSelection(CMicrostructure *ms, const Coord *mp)
  : PixelSelectionCourier(ms),
    mousepoint(*mp)
{
   // oofcerr << "PointSelection::ctor: " << mousepoint 
   // 	   << " " << ms->pixelFromPoint(mousepoint) << std::endl;
}

ICoord PointSelection::currentPoint() const {
  return pixelFromPoint(mousepoint);
}

void PointSelection::next() {
  done_ = true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==2
BrushSelection::BrushSelection(CMicrostructure *ms, BrushStyle *brush,
			       const std::vector<Coord> *points)
  : PixelSelectionCourier(ms),
    brush(brush),
    points(*points),
    master(ms->sizeInPixels()),
    offset(0, 0) {}

void BrushSelection::start() {
  pts_iter = points.begin();  // start from the first point
  brush->getPixels(ms, *pts_iter, master, selected, offset); // get pixels
  sel_iter = selected.begin();
  if (!*sel_iter) next();
}

ICoord BrushSelection::currentPoint() const {
  return sel_iter.coord() + offset;
}

void BrushSelection::advance() {
  if(sel_iter.done()) {  // if it's at the end of pixel array
    if (pts_iter == points.end()-1 ) {  // if it's also at the end of points
      done_ = true;
    }
    else {  // to the next point
      ++pts_iter;
      brush->getPixels(ms, *pts_iter, master, selected, offset);
      sel_iter.reset();
    }
  }
  else {
    ++sel_iter;
  }
}

void BrushSelection::next() {
  advance();
  while(!*sel_iter && !done_) 
    advance();
}
#endif

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO 3.1: The Region selection methods (BoxSelection, CircleSelection,
// and EllipseSelection) could take an additional argument that
// determines whether voxels that straddle the boundary of the region
// are included. Options would be ALLCORNERS (all corners of the voxel
// must be in the region), ONECORNER (at least one corner of the voxel
// must be in the region), and CENTER (the center of the voxel must be
// in the region).  The current implementation is CENTER.

static bool nextPointInBox(const ICoord &ll, const ICoord &ur, 
			   ICoord &currentPt) 
{
  // ll and ur are lowerleft and upperright box corners.
  //* TODO OPT: Should this loop be unrolled?  Is it too slow like this?
  for(int i=0; i<DIM; i++) {
    currentPt[i]++;
    if(currentPt[i] < ur[i])
      return true;		// there is a next point
    currentPt[i] = ll[i];
  }
  return false;			// no next point
}

template <class COORD>
static bool canonicalDiagonal(COORD &point0, COORD &point1) {
  // Make sure that all components of point0 are smaller than the
  // corresponding components of point1.  Return false if any
  // components are equal.
  for(int i=0; i<DIM; i++) {
    if(point0[i] == point1[i])
      return false;
    if(point0[i] > point1[i]) {
      typename COORD::ComponentType temp = point0[i];
      point0[i] = point1[i];
      point1[i] = temp;
    }
  }
  return true;
}

///////////

BoxSelection::BoxSelection(CMicrostructure *ms,
			   const Coord *pt0, const Coord *pt1)
  : PixelSelectionCourier(ms)
{
  // ll and ur are the lowerleft and upperright pixel coordinates of
  // the set of pixels whose centers are within the box specified by
  // the physical coordinates pt0 and pt1.
  
  // Compute the pixel-space coordinates of pt0 and pt1.
  Coord pll = ms->physical2Pixel(*pt0);
  Coord pur = ms->physical2Pixel(*pt1);
  done_ = !canonicalDiagonal(pll, pur);
  // Round all components to the nearest integer.
  ll = pll.roundComponents();
  ur = pur.roundComponents();
}

void BoxSelection::start() {
  currentpt = ll;
}

ICoord BoxSelection::currentPoint() const {
  return currentpt;
}


void BoxSelection::next() {
  done_ = !nextPointInBox(ll, ur, currentpt);
}

//////////

CircleSelection::CircleSelection(CMicrostructure *ms,
				 const Coord *c, const double r)
  : PixelSelectionCourier(ms),
    center(*c),
    radius2(r*r)
{
  Coord rad = r*Coord(1., 1., 1.);
  Coord pll = ms->physical2Pixel(center - rad);
  Coord pur = ms->physical2Pixel(center + rad);
  ll = pll.roundComponents();
  ur = pur.roundComponents();
}

bool CircleSelection::interior() {
  double rr = 0.0;
  Coord pxlsz = ms->sizeOfPixels();
  for(int i=0; i<DIM; i++) {
    double d = (currentpt[i] + 0.5)*pxlsz[i] - center[i];
    rr += d*d;
  }
  return rr <= radius2;
}

void CircleSelection::start() {
  currentpt = ll;
  if(!interior())
    next();
}

ICoord CircleSelection::currentPoint() const {
  return currentpt;
}

void CircleSelection::advance() {
  done_ = !nextPointInBox(ll, ur, currentpt);
}

void CircleSelection::next() {
  // Move to the next slot
  advance();
  // Check if it's a valid point
  while (!interior() && !done())
    advance();
}

//////////

EllipseSelection::EllipseSelection(CMicrostructure *ms,
				   const Coord *pt0, const Coord *pt1)
  : PixelSelectionCourier(ms),
    // pt0(*pt0),
    // pt1(*pt1),
    center(0.5*(*pt0 + *pt1)),
    aa(DIM)
{
  done_ = !canonicalDiagonal(ll, ur);
  Coord boxsize = *pt1 - *pt0;
  for(int i=0; i<DIM; i++) {
    double d = 0.5*((*pt0)[i] - (*pt1)[i]);
    aa[i] = 1./(d*d);
  }
  Coord pll = ms->physical2Pixel(*pt0);
  Coord pur = ms->physical2Pixel(*pt1);
  done_ = !canonicalDiagonal(pll, pur);
  ll = pll.roundComponents();
  ur = pur.roundComponents();
}

bool EllipseSelection::interior() {
  double rr = 0;
  Coord pxlsz = ms->sizeOfPixels();
  for(int i=0; i<DIM; i++) {
    double d = (currentpt[i] + 0.5)*pxlsz[i] - center[i];
    rr += d*d*aa[i];
  }
  return rr <= 1.0;
}

void EllipseSelection::start() {
  currentpt = ll;
  if (!interior()) next();
}

ICoord EllipseSelection::currentPoint() const {
  return currentpt;
}

void EllipseSelection::advance() {
  done_ = !nextPointInBox(ll, ur, currentpt);
}

void EllipseSelection::next() {
  // Move to the next slot
  advance();
  // Check if it's a valid point
  while (!interior() && !done_)
    advance();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

GroupSelection::GroupSelection(CMicrostructure *ms, const PixelSet *group)
  : PixelSelectionCourier(ms),
    pgroup(group)
{
}
    
void GroupSelection::start() {
  pxl_iter = pgroup->members()->begin();
  if(pgroup->members()->empty())
    done_ = true;
}

ICoord GroupSelection::currentPoint() const {
  return *pxl_iter;
}

void GroupSelection::next() {
  if (pxl_iter == --pgroup->members()->end())
    done_ = true;
  else
    ++pxl_iter;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

IntersectSelection::IntersectSelection(CMicrostructure *ms,
				       const PixelSet *selpix,
				       PixelSelectionCourier *courier)
  : PixelSelectionCourier(ms),
    selpix(selpix),
    courpix(&ms->sizeInPixels(), ms),
    courier(courier)
{}

void IntersectSelection::start() {
  // Use the passed-in courier to create a PixelSet to loop over.  We
  // could use the courier itself, except that its members might not
  // be in order.
  //* TODO OPT: This involves a lot of extra copying, especially creating
  //* the intermediate ICoordVector.  Fix that.
  ICoordVector pxls;
  courpix.clear();
  courier->start();
  while(!courier->done()) {
    pxls.push_back(courier->currentPoint());
    courier->next();
  }
  courpix.add(&pxls);

  sel_iter = selpix->members()->begin();
  cour_iter = courpix.members()->begin();
  if(selpix->members()->empty() || courpix.members()->empty())
    done_ = true;
  else if (!(*sel_iter == *cour_iter))
    next();
}
  
ICoord IntersectSelection::currentPoint() const {
  return *sel_iter;
}

void IntersectSelection::advance() {
  if ( (sel_iter == --selpix->members()->end()) ||
       (cour_iter == --courpix.members()->end()) ) {
    done_ = true;
  }
  else {
    if (*sel_iter == *cour_iter) {
      ++sel_iter;
      ++cour_iter;
    }
    else if (*sel_iter < *cour_iter)
      ++sel_iter;
    else if (*cour_iter < *sel_iter)
      ++cour_iter;
  }
}

void IntersectSelection::next() {
  advance();
  while (!(*sel_iter == *cour_iter) && !done_) {
    advance();
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

DespeckleSelection::DespeckleSelection(CMicrostructure *ms,
				       const PixelSet *group,
				       const int neighbors)  
  : PixelSelectionCourier(ms),
    pgroup(group),
    neighbors(neighbors),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin())
{}

void DespeckleSelection::start() {
  pgroup->despeckle(neighbors, selected);  // get the pixel array
  if (!*sel_iter)
    next();
}

ICoord DespeckleSelection::currentPoint() const {
  return sel_iter.coord();
}

void DespeckleSelection::advance() {
  if(sel_iter.done()) // if it's at the end of pixel array
    done_ = true;
  else
    ++sel_iter;
}

void DespeckleSelection::next() {
  advance();
  while(!*sel_iter && !done_) 
    advance();
}

/////////

ElkcepsedSelection::ElkcepsedSelection(CMicrostructure *ms,
				       const PixelSet *group,
				       const int neighbors)  
  : PixelSelectionCourier(ms),
    pgroup(group),
    neighbors(neighbors),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin())
{}

void ElkcepsedSelection::start() {
  pgroup->elkcepsed(neighbors, selected);  // get the pixel array
  if (!*sel_iter)
    next();
}

ICoord ElkcepsedSelection::currentPoint() const {
  return sel_iter.coord();
}

void ElkcepsedSelection::advance() {
  if(sel_iter.done()) // if it's at the end of pixel array
    done_ = true;
  else
    ++sel_iter;
}

void ElkcepsedSelection::next() {
  advance();
  while(!*sel_iter && !done_) 
    advance();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ExpandSelection::ExpandSelection(CMicrostructure *ms,
				 const PixelSet *group,
				 const double radius)  
  : PixelSelectionCourier(ms),
    pgroup(group),
    radius(radius),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin()) {}

void ExpandSelection::start() {
  pgroup->expand(radius, selected);  // get the pixel array
  if (!*sel_iter) next();
}

ICoord ExpandSelection::currentPoint() const {
  return sel_iter.coord();
}

void ExpandSelection::advance() {
  if(sel_iter.done()) // if it's at the end of pixel array
    done_ = true;
  else
    ++sel_iter;
}

void ExpandSelection::next() {
  advance();
  while(!*sel_iter && !done_) 
    advance();
}

//////////

ShrinkSelection::ShrinkSelection(CMicrostructure *ms,
				 const PixelSet *group,
				 const double radius)  
  : PixelSelectionCourier(ms),
    pgroup(group),
    radius(radius),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin()) {}

void ShrinkSelection::start() {
  pgroup->shrink(radius, selected);  // get the pixel array
  if (!*sel_iter) next();
}

ICoord ShrinkSelection::currentPoint() const {
  return sel_iter.coord();
}

void ShrinkSelection::advance() {
  if(sel_iter.done()) // if it's at the end of pixel array
    done_ = true;
  else
    ++sel_iter;
}

void ShrinkSelection::next() {
  advance();
  while(!*sel_iter && !done_) 
    advance();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Output here is just for debugging, so it is sort of skeletal in spots.

std::ostream &operator<<(std::ostream &os, const PixelSelectionCourier &psc) {
  psc.print(os);
  return os;
}

void PointSelection::print(std::ostream &os) const {
  os << "PointSelection(" << mousepoint << ")";
}

void PointlessSelection::print(std::ostream &os) const {
  os << "PointlessSelection()";
}

#if DIM==2
void BrushSelection::print(std::ostream &os) const {
  os << "BrushSelection()";
}
#endif

void BoxSelection::print(std::ostream &os) const {
  os << "BoxSelection(" << ll << ", " << ur << ")";
}

void CircleSelection::print(std::ostream &os) const {
  os << "CircleSelection(" << center << ", " << sqrt(radius2) << ")";
}

void EllipseSelection::print(std::ostream &os) const {
  os << "EllipseSelection(" << ll << ", " << ur << ")";
}

void GroupSelection::print(std::ostream &os) const {
  os << "GroupSelection(" << pgroup->len() << ")";
}

void IntersectSelection::print(std::ostream &os) const {
  os << "IntersectSelection()";
}

void DespeckleSelection::print(std::ostream &os) const {
  os << "DespeckleSelection()";
}

void ElkcepsedSelection::print(std::ostream &os) const {
  os << "ElkcepsedSelection()";
}

void ExpandSelection::print(std::ostream &os) const {
  os << "ExpandSelection()";
}

void ShrinkSelection::print(std::ostream &os) const {
  os << "ShrinkSelection()";
}
