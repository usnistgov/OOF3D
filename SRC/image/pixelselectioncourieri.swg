// -*- C++ -*-
// $RCSfile: pixelselectioncourieri.swg,v $
// $Revision: 1.4.18.1 $
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

#ifndef PIXELSELECTIONCOURIERI_SWG
#define PIXELSELECTIONCOURIERI_SWG

%module pixelselectioncourieri

%include "common/typemaps.swg"
%extern "common/pixelselectioncourier.swg"
%extern "common/ccolor.swg"
%extern "common/colordifference.swg"

%pragma(python) code="from ooflib.SWIG.common.pixelselectioncourier import PixelSelectionCourierPtr"

%{
#include "image/pixelselectioncourieri.h"
#include "common/ccolor.h"
#include "common/colordifference.h"
%}

class ColorSelection : public PixelSelectionCourier {
public:
#ifndef DIM_3
  ColorSelection(CMicrostructure*, OOFImage*, CColor*, ColorDifference*);
#else
  ColorSelection(CMicrostructure*, OOFImage3D*, CColor*, ColorDifference*);
#endif
  ~ColorSelection();
};

class BurnSelection : public PixelSelectionCourier {
public:
#ifndef DIM_3
  BurnSelection(CMicrostructure*, BasicBurner*, OOFImage*, ICoord *iPoint);
#else
  BurnSelection(CMicrostructure*, BasicBurner*, OOFImage3D*, ICoord *iPoint);
#endif
  ~BurnSelection();
};

#endif // PIXELSELECTIONCOURIERI_SWG
