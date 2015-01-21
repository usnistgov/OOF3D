// -*- C++ -*-
// $RCSfile: pixelselectioncourieri.h,v $
// $Revision: 1.3.18.2 $
// $Author: langer $
// $Date: 2014/09/27 22:34:38 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PIXELSELECTIONCOURIERI_H
#define PIXELSELECTIONCOURIERI_H

#include "common/pixelselectioncourier.h"
#if DIM==2
class OOFImage;
#elif DIM==3
class OOFImage3D;
#endif
class CColor;
class ColorDifference;
class BasicBurner;

// Color Difference 
class ColorSelection : public PixelSelectionCourier {
private:
#if DIM==2
  OOFImage *image;
#elif DIM==3
	OOFImage3D *image;
#endif
  const CColor *color;
  const ColorDifference *diff;
  BoolArray selected;
  BoolArray::iterator sel_iter;
  void advance();
public:
#if DIM==2
  ColorSelection(CMicrostructure *ms, OOFImage *immidge,
		 const CColor *color, const ColorDifference *diff);
#elif DIM==3
  ColorSelection(CMicrostructure *ms, OOFImage3D *immidge,
		 const CColor *color, const ColorDifference *diff);
#endif
  virtual ~ColorSelection();
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Burn
class BurnSelection : public PixelSelectionCourier {
private:
  BasicBurner *burner;
#if DIM==2
  OOFImage *image;
#elif DIM==3
	OOFImage3D *image;
#endif
  const ICoord spark;
  BoolArray selected;
  BoolArray::iterator sel_iter;
  void advance();
public:
#if DIM==2
  BurnSelection(CMicrostructure *ms,
		BasicBurner *burner, OOFImage *immidge, const ICoord *pt);
#elif DIM==3
  BurnSelection(CMicrostructure *ms,
		BasicBurner *burner, OOFImage3D *immidge, const ICoord *pt);
#endif
  virtual ~BurnSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

#endif // PIXELSELECTIONCOURIERI_H
