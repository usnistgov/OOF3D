// -*- C++ -*-
// $RCSfile: orientationimage.C,v $
// $Revision: 1.4.10.3 $
// $Author: langer $
// $Date: 2014/08/01 19:53:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "common/array.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "engine/angle2color.h"
#include "engine/material.h"
#include "engine/ooferror.h"
#include "engine/orientationimage.h"
#include "engine/property/orientation/orientation.h"

OrientationImage::OrientationImage(CMicrostructure *microstructure,
				   const Angle2Color *colorscheme,
				   const CColor *noMaterial,
				   const CColor *noOrientation)
  : microstructure(microstructure),
    noMaterial(*noMaterial),
    noOrientation(*noOrientation),
    colorscheme(colorscheme->clone())
{}

OrientationImage::~OrientationImage() {
  delete colorscheme;
}

const Coord &OrientationImage::size()  const {
  std::cerr << "OrientationImage::size: size=" << microstructure->size() << std::endl;
  return microstructure->size();
}

const ICoord &OrientationImage::sizeInPixels() const {
  return microstructure->sizeInPixels();
}
