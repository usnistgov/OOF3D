// -*- C++ -*-
// $RCSfile: brushstyle.C,v $
// $Revision: 1.16.18.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */
#include <oofconfig.h>

#include "common/brushstyle.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/geometry.h"
#include <math.h>
#include "printvec.h"

void CircleBrush::getPixels(const CMicrostructure *ms,
			    const Coord &c, BoolArray &master,
			    BoolArray &selected, ICoord &offset) {
  // If r is smaller than max(psize(0)/2, psize(1)/2),
  //it returns a pixel position of the given mouse point.
  if (2.0*r<=ms->sizeOfPixels()(0) || 2.0*r<=ms->sizeOfPixels()(1)) {
    offset = ms->pixelFromPoint(c);
//     offset.setCoord(ms->pixelFromPoint(c)(0), ms->pixelFromPoint(c)(1));
    selected.resize(ICoord(1,1));
    if (!master.get(offset)) {
      selected[ICoord(0,0)] = true;
      master[offset] = true;
    }
    return;
  }
  // If r is specified appropriately, it return a list of pixel
  // positions enclosed in the circle.
  const double cx = c(0);
  const double cy = c(1);
  const double rr = r*r;
  Coord ll = ms->physical2Pixel(Coord(cx-r, cy-r));
  Coord ur = ms->physical2Pixel(Coord(cx+r, cy+r));
  const int Xmin = int(ll(0)) - 1;
  const int Xmax = int(ur(0)) + 1;
  const int Ymin = int(ll(1)) - 1;
  const int Ymax = int(ur(1)) + 1;
  selected.resize(ICoord(Xmax-Xmin+1, Ymax-Ymin+1));
  selected.clear(false);
  offset = ICoord(Xmin, Ymin);
  //   offset.setCoord(Xmin, Ymin);
  for (int i=Xmin; i<=Xmax; i++) {
    for (int j=Ymin; j<=Ymax; j++) {
      double dx = (i+0.5)*ms->sizeOfPixels()(0) - cx;
      double dy = (j+0.5)*ms->sizeOfPixels()(1) - cy;
      if (dx*dx + dy*dy <= rr) {
	if (ms->contains(ICoord(i,j)))
	  if (!master.get(ICoord(i,j))) { 
	    selected[ICoord(i-Xmin, j-Ymin)] = true;
	    master[ICoord(i,j)] = true;
	  }
      }
    }
  }
  return;
}

void SquareBrush::getPixels(const CMicrostructure *ms,
			    const Coord &c, BoolArray &master,
			    BoolArray &selected, ICoord &offset) {
  // If a radius is not a positive number, it returns a pixel position of
  // the given mouse point.
  if (2.0*size<=ms->sizeOfPixels()(0) || 2.0*size<=ms->sizeOfPixels()(1)) {
    offset = ms->pixelFromPoint(c);
//     offset.setCoord(ms->pixelFromPoint(c)(0), ms->pixelFromPoint(c)(1));
    selected.resize(ICoord(1,1));
    if (!master.get(offset)) {
      selected[ICoord(0,0)] = true;
      master[offset] = true;
    }
    return;
  }
  // If a r is specified appropriately, it return a list of pixel
  // positions enclosed in the square.
  double cx = c(0);
  double cy = c(1);
  Coord ll = ms->physical2Pixel(Coord(cx-size, cy-size));
  Coord ur = ms->physical2Pixel(Coord(cx+size, cy+size));
  CRectangle rect = CRectangle(ll, ur);
  int Xmin = int(ll(0))-1;
  int Xmax = int(ur(0))+1;
  int Ymin = int(ll(1))-1;
  int Ymax = int(ur(1))+1;
  selected.resize(ICoord(Xmax-Xmin+1, Ymax-Ymin+1));
  selected.clear(false);
//   offset.setCoord(Xmin, Ymin);
  offset = ICoord(Xmin, Ymin);
  for (int i=Xmin; i<=Xmax; i++) {
    for (int j=Ymin; j<=Ymax; j++) {
      double dx = (i+0.5)*ms->sizeOfPixels()(0);
      double dy = (j+0.5)*ms->sizeOfPixels()(1);
      if (rect.contains(Coord(dx, dy)))
	if (ms->contains(ICoord(i,j)))
	  if (!master.get(ICoord(i,j))) {
	    selected[ICoord(i-Xmin, j-Ymin)] = true;
	    master[ICoord(i,j)] = true;
	  }
    }
  }
  return;
}

