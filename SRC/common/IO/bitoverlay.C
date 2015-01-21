// -*- C++ -*-
// $RCSfile: bitoverlay.C,v $
// $Revision: 1.23.10.10 $
// $Author: langer $
// $Date: 2014/12/14 22:49:09 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/bitoverlay.h"
#include "common/trace.h"
#include "common/tostring.h"

BitmapOverlay::BitmapOverlay(const Coord *size, const ICoord *isize)
  : fg(CColor(1., 1., 1.)),
    bg(CColor(0., 0., 0.)),
    data(*isize)
{
  resize(size, isize);
  tintAlpha = 1.0;
  voxelAlpha = 1.0;
}

BitmapOverlay::~BitmapOverlay() {}

void BitmapOverlay::resize(const Coord *size, const ICoord *isize) {
  size_ = *size;
  sizeInPixels_ = *isize;
  clear();
}

void BitmapOverlay::clear() {
  data.resize(sizeInPixels_);
  data.clear(false);
  // ++timestamp;
}

void BitmapOverlay::invert() {
  data.invert();
}

void BitmapOverlay::set(const ICoord *pixel) {
  data.set(pixel);
  // ++timestamp;
}

void BitmapOverlay::set(const ICoordVector *pixels) {
  for(ICoordVector::const_iterator i=pixels->begin();i!=pixels->end();++i)
    if(data.contains(*i))
      data.set(&*i);
  // ++timestamp;
}

void BitmapOverlay::reset(const ICoordVector *pixels) {
  for(ICoordVector::const_iterator i=pixels->begin();i!=pixels->end();++i)
    if(data.contains(*i))
      data.reset(&*i);
  // ++timestamp;
}

void BitmapOverlay::reset(const ICoord *pixel) {
  data.reset(pixel);
  // ++timestamp;
}

void BitmapOverlay::toggle(const ICoord *pixel) {
  data.toggle(pixel);
  // ++timestamp;
}

void BitmapOverlay::toggle(const ICoordVector *pixels) {
  for(ICoordVector::const_iterator i=pixels->begin();i!=pixels->end();++i)
    if(data.contains(*i))
      data.toggle(&*i);
  // ++timestamp;
}

bool BitmapOverlay::get(const ICoord *pixel) const {
  if(data.contains(*pixel))
    return data.get(*pixel);
  return false;
}

void BitmapOverlay::copy(const BitmapOverlay *other) {
  data = other->data.clone();
  // avoid taking address of temporary
  const CColor x(other->fg);
  setColor(&x);
  tintAlpha = other->getTintAlpha();
  voxelAlpha = other->getVoxelAlpha();
}

void BitmapOverlay::setColor(const CColor *color) {
  fg = *color;
  if(fg.getRed() == 0.0) {
    bg.setRed(1.0);
    bg.setGreen(1.0);
    bg.setBlue(1.0);
  }
  else {
    bg.setRed(0.0); 
    bg.setBlue(0.0);
    bg.setGreen(0.0);
  }
}

// CColor BitmapOverlay::getBG() const {
//   return bg;
// }

// CColor BitmapOverlay::getFG() const {
//   return fg;
// }


