// -*- C++ -*-
// $RCSfile: cpixelselection.h,v $
// $Revision: 1.12.18.10 $
// $Author: langer $
// $Date: 2014/07/10 18:54:06 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CPIXELSELECTION_H
#define CPIXELSELECTION_H

// Base class for python PixelSelection and related objects.  

#include "common/pixelgroup.h"
#include "common/pixelselectioncourier.h"
#include "common/IO/bitoverlay.h"

class ActiveArea;

class CPixelSelection {
protected:
  // These can be used by the ActiveArea subclass.
  PixelSet pixset;
  BitmapOverlay bitmap;
private:
  // TimeStamp timestamp;
  const ICoord isize_;
  const Coord size_;
  const ActiveArea *getActiveArea() const; // gets aa from Microstructure
  const ICoordVector *getActivePixels() const;
public:
  CPixelSelection(const ICoord *pxlsize, const Coord *size, CMicrostructure*);
  CPixelSelection(const CPixelSelection&);
  CPixelSelection *clone() const { return new CPixelSelection(*this); }
  virtual ~CPixelSelection() {}

  CMicrostructure *getMicrostructure() const;

  const Coord &size() const { return size_; }
  const ICoord &sizeInPixels() const { return isize_; }
  bool checkpixel(const ICoord *pixel) const;

  void clear();
  void clearWithoutCheck();
  void invert();
  void invertWithoutCheck();
  
  void select(PixelSelectionCourier*);
  void unselect(PixelSelectionCourier*);
  void toggle(PixelSelectionCourier*);
  void selectSelected(PixelSelectionCourier*);

  void selectWithoutCheck(PixelSelectionCourier*);
  void unselectWithoutCheck(PixelSelectionCourier*);
  void toggleWithoutCheck(PixelSelectionCourier*);

  bool isSelected(const ICoord*) const;
  const ICoordVector *members() const;
  const PixelSet *getPixelGroup() const { return &pixset; }
  const BitmapOverlay *getBitmap() const { return &bitmap; }
  void setFromGroup(const PixelSet*);
  int len() const;
  bool empty() const;
  void getBounds(ICoord&, ICoord&) const;
};


#endif // CPIXELSELECTION_H
