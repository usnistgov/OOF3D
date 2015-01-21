// -*- C++ -*-
// $RCSfile: orientationimage.h,v $
// $Revision: 1.2.26.4 $
// $Author: langer $
// $Date: 2014/12/14 22:49:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ORIENTATIONIMAGE_H
#define ORIENTATIONIMAGE_H

#include <oofconfig.h>

#include "common/ccolor.h"
#include "common/coord_i.h"

class Angle2Color;
class CMicrostructure;
class StringImage;

// Not an OrientationMap, but just a way of displaying the Orientation
// of the Materials assigned to pixels in a Microstructure.

class OrientationImage { 
  CMicrostructure *microstructure;
  const CColor noMaterial;
  const CColor noOrientation;
  const Angle2Color *colorscheme;
public:
  OrientationImage(CMicrostructure*, const Angle2Color*,
		   const CColor*, const CColor*);
  virtual ~OrientationImage();
  virtual const Coord &size() const;
  virtual const ICoord &sizeInPixels() const;
};

#endif // ORIENTATIONIMAGE_H
