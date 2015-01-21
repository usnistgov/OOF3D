// -*- C++ -*-
// $RCSfile: pixelselectioncourieri.C,v $
// $Revision: 1.3.18.2 $
// $Author: langer $
// $Date: 2012/12/21 22:55:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/cmicrostructure.h"
#include "common/IO/oofcerr.h"
#include "image/pixelselectioncourieri.h"
#if DIM==2
#include "image/oofimage.h"
#elif DIM==3
#include "image/oofimage3d.h"
#endif
#include "image/burn.h"

#if DIM==2
ColorSelection::ColorSelection(CMicrostructure *ms, OOFImage *immidge,
			       const CColor *color,
			       const ColorDifference *diff)
  : PixelSelectionCourier(ms),
    image(immidge),
    color(color->clone()),
    diff(diff->clone()),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin()) {}
#elif DIM==3
ColorSelection::ColorSelection(CMicrostructure *ms, OOFImage3D *immidge,
			       const CColor *color,
			       const ColorDifference *diff)
  : PixelSelectionCourier(ms),
    image(immidge),
    color(color->clone()),
    diff(diff->clone()),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin()) {}
#endif


ColorSelection::~ColorSelection() {
  delete color;
  delete diff;
}

void ColorSelection::start() {
  image->getColorPoints(*color, *diff, selected);  // get the pixel array
  if (!*sel_iter) next();
}

ICoord ColorSelection::currentPoint() const {
  return sel_iter.coord();
}

void ColorSelection::advance() {
  if(sel_iter.done()) // if it's at the end of pixel array
    done_ = true;
  else
    ++sel_iter;
}

void ColorSelection::next() {
  advance();
  while(!*sel_iter && !done_) 
    advance();
}

void ColorSelection::print(std::ostream &os) const {
  os << "ColorSelection()";
}

//////////

#if DIM==2
BurnSelection::BurnSelection(CMicrostructure *ms,
			     BasicBurner *burner, OOFImage *immidge,
			     const ICoord *pt)
  : PixelSelectionCourier(ms),
    burner(burner),
    image(immidge),
    spark(*pt),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin()) {}
#elif DIM==3
BurnSelection::BurnSelection(CMicrostructure *ms,
			     BasicBurner *burner, OOFImage3D *immidge,
			     const ICoord *pt)
  : PixelSelectionCourier(ms),
    burner(burner),
    image(immidge),
    spark(*pt),
    selected(ms->sizeInPixels(), false),
    sel_iter(selected.begin()) {}
#endif

void BurnSelection::start() {
  burner->burn(*image, &spark, selected);  // get the pixel array
  if (!*sel_iter) next();
}

ICoord BurnSelection::currentPoint() const {
  return sel_iter.coord();
}

void BurnSelection::advance() {
  if(sel_iter.done()) // if it's at the end of pixel array
    done_ = true;
  else
    ++sel_iter;
}

void BurnSelection::next() {
  advance();
  while(!*sel_iter && !done_) 
    advance();
}

void BurnSelection::print(std::ostream &os) const {
  os << "BurnSelection()";
}

