// -*- C++ -*-
// $RCSfile: bitoverlay.swg,v $
// $Revision: 1.21.10.6 $
// $Author: langer $
// $Date: 2014/09/27 22:34:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BITOVERLAY_SWG
#define BITOVERLAY_SWG

%module bitoverlay
%include "common/typemaps.swg"

%{
#include "common/IO/bitoverlay.h"
%}
%extern "common/coord.swg"
// %extern "common/timestamp.swg"
%extern "common/ccolor.swg"

// %pragma(python) code="from ooflib.SWIG.common.timestamp import TimeStampPtr"
%pragma(python) code="from ooflib.SWIG.common.ccolor import CColorPtr"
%pragma(python) include="bitoverlay.spy"

class BitmapOverlay { 
public:
  BitmapOverlay(Coord *Point, ICoord *iPoint);
  ~BitmapOverlay();
  void resize(Coord *Point, ICoord *iPoint);
  void clear();
  void invert();
  void set(ICoord *iPoint);
  void reset(ICoord *iPoint);
  void toggle(ICoord *iPoint);
  bool get(ICoord *iPoint);
  void copy(BitmapOverlay*);
  bool contains(ICoord *iPoint);
  void setColor(CColor*);
  void setVoxelAlpha(double alpha);
  void setTintAlpha(double alpha);
  // CColor getBG();
  // CColor getFG();
  double getVoxelAlpha();
  double getTintAlpha();
  Coord size();
  ICoord sizeInPixels();
  bool empty();
  // TimeStamp &getTimeStamp();
};

#endif // BITOVERLAY_SWG
