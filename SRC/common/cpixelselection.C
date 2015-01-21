// -*- C++ -*-
// $RCSfile: cpixelselection.C,v $
// $Revision: 1.17.18.16 $
// $Author: langer $
// $Date: 2014/12/14 22:49:06 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <iostream>

#include "common/activearea.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/cpixelselection.h"
#include "common/pixelgroup.h"
#include "common/printvec.h"
#include "common/IO/oofcerr.h"

// TODO OPT: Do we still need to store the bitmap representation of the
// pixel selection?  The BitmapOverlayDisplayMethod no longer needs
// it.  The other thing it is useful for is to quickly compute the
// complement of the selected pixels, but that can be done quickly by
// simultaneously looping over all the pixels in the ms and a sorted
// list of selected pixels.  If the pixels were stored in a set
// instead of a list, this would be easy.  NO -- it's used by isSelected().

CPixelSelection::CPixelSelection(const ICoord *pxlsize, const Coord *size,
				 CMicrostructure *ms)
  : pixset(pxlsize, ms),
    bitmap(size, pxlsize),
    isize_(*pxlsize),
    size_(*size)
{}

CPixelSelection::CPixelSelection(const CPixelSelection &other)
  : pixset(other.pixset),
    bitmap(&other.size(), &other.sizeInPixels()),
    isize_(other.sizeInPixels()),
    size_(other.size())
{
  bitmap.copy(&other.bitmap);
}

bool CPixelSelection::checkpixel(const ICoord *pixel) const {
  return bitmap.contains(pixel);
}

const ActiveArea *CPixelSelection::getActiveArea() const {
  return getMicrostructure()->getActiveArea();
}

CMicrostructure *CPixelSelection::getMicrostructure() const {
  return pixset.getMicrostructure();
}

const ICoordVector *CPixelSelection::getActivePixels() const {
  // This returns a new'd set which must be deleted.  The active
  // pixels are the ones *not* set in the bitmap, which is why the
  // argument to getPixels is 0.
  return getActiveArea()->getBitmap()->getPixels(0);
}

void CPixelSelection::clear() {
  //cout << "in CPixelSelection::clear " << getActiveArea()->len() << endl;
  if(getActiveArea()->getOverride() || getActiveArea()->len() == 0)
    clearWithoutCheck();
  else {
    const ICoordVector *activepxls = getActivePixels();
    pixset.removeWithoutCheck(activepxls);
    bitmap.reset(activepxls);
    delete activepxls;
  }
}

void CPixelSelection::clearWithoutCheck() {
  pixset.clear();
  bitmap.clear();
}

void CPixelSelection::invert() {
  if(getActiveArea()->getOverride() || getActiveArea()->len() == 0)
    invertWithoutCheck();
  else {
    const ICoordVector *activepxls = getActivePixels();
    bitmap.toggle(activepxls);
    pixset.clear();
    pixset.setFromBitmap(bitmap);
  }
};

void CPixelSelection::invertWithoutCheck() {
  bitmap.invert();
  pixset.clear();
  pixset.setFromBitmap(bitmap);
};

void CPixelSelection::select(PixelSelectionCourier *selection) {
  const ActiveArea *activearea = getActiveArea();
  if(activearea->getOverride() || getActiveArea()->len() == 0) {
    selectWithoutCheck(selection);
  }
  else {
    ICoordVector okpix;
    selection->start();
    while(!selection->done()) {
      ICoord pixel = selection->currentPoint();
      if(checkpixel(&pixel) && activearea->isActive(&pixel)) {
	bitmap.set(&pixel);
	okpix.push_back(pixel);
      }
      selection->next();
    }
    pixset.add(&okpix);
  }
}

void CPixelSelection::selectWithoutCheck(PixelSelectionCourier *selection) {
  ICoordVector okpix;
  selection->start();
  while(!selection->done()) {
    ICoord pixel = selection->currentPoint();
    if(checkpixel(&pixel)) {
      bitmap.set(&pixel);
      okpix.push_back(pixel);
    }
    selection->next();
  }
  pixset.addWithoutCheck(&okpix);
}

void CPixelSelection::unselect(PixelSelectionCourier *selection) {
  const ActiveArea *activearea = getActiveArea();
  if(activearea->getOverride() || getActiveArea()->len() == 0)
    unselectWithoutCheck(selection);
  else {
    ICoordVector *pixels = new ICoordVector;
    selection->start();
    while(!selection->done()) {
      ICoord pixel = selection->currentPoint();
      if(checkpixel(&pixel) && activearea->isActive(&pixel)) {
	bitmap.reset(&pixel);
	pixels->push_back(pixel);
      }
      selection->next();
    }
    pixset.remove(pixels);
    delete pixels;
  }
}

void CPixelSelection::unselectWithoutCheck(PixelSelectionCourier *selection) {
  ICoordVector pixels;
  selection->start();
  while(!selection->done()) {
    ICoord pixel = selection->currentPoint();
    if(checkpixel(&pixel)) {
      bitmap.reset(&pixel);
      pixels.push_back(pixel);
    }
    selection->next();
  }
  pixset.removeWithoutCheck(&pixels);
}

void CPixelSelection::toggle(PixelSelectionCourier *selection) {
  const ActiveArea *activearea = getActiveArea();
  if(activearea->getOverride() || getActiveArea()->len() == 0)
    toggleWithoutCheck(selection);
  else {
    selection->start();
    while(!selection->done()) {
      ICoord pixel = selection->currentPoint();
      if(checkpixel(&pixel) && activearea->isActive(&pixel)) {
	bitmap.toggle(&pixel);
      }
      selection->next();
    }
    pixset.clear();
    pixset.setFromBitmap(bitmap);
  }
}

void CPixelSelection::toggleWithoutCheck(PixelSelectionCourier *selection) {
  selection->start();
  while(!selection->done()) {
    ICoord pixel = selection->currentPoint();
    if(checkpixel(&pixel)) {
      bitmap.toggle(&pixel);
    }
    selection->next();
  }
  pixset.clear();
  pixset.setFromBitmap(bitmap);
}

void CPixelSelection::selectSelected(PixelSelectionCourier *selection) {
  const ActiveArea *activearea = getActiveArea();
  pixset.clear();
  selection->start();
  while(!selection->done()) {
    ICoord pixel = selection->currentPoint();
    if(bitmap.get(&pixel) && activearea->isActive(&pixel))
      pixset.add(pixel);
    selection->next();
  }
  bitmap.clear();
  bitmap.set(pixset.members());
}

bool CPixelSelection::isSelected(const ICoord *pixel) const {
  return bitmap.get(pixel);
}

const ICoordVector *CPixelSelection::members() const {
  return pixset.members();
}

int CPixelSelection::len() const {
  return pixset.len();
}

bool CPixelSelection::empty() const {
  return pixset.empty();
}

void CPixelSelection::setFromGroup(const PixelSet *grp) {
  bitmap.set(grp->members());
  pixset.setFromBitmap(bitmap);
}

void CPixelSelection::getBounds(ICoord &min, ICoord &max) const {
  pixset.getBounds(min, max);
}
