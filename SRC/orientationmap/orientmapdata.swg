// -*- C++ -*-
// $RCSfile: orientmapdata.swg,v $
// $Revision: 1.5.6.4 $
// $Author: langer $
// $Date: 2014/09/27 22:34:41 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ORIENTMAPDATA_SWG
#define ORIENTMAPDATA_SWG

%module orientmapdata
%include "common/typemaps.swg"
%{
#include "orientationmap/orientmapdata.h"
%}

%pragma(python) include="orientmapdata.spy"
%extern "common/imagebase.swg"
%extern "common/coord.swg"
   //%extern "common/IO/stringimage.swg"
%extern "engine/angle2color.swg"
%extern "common/corientation.swg"
#ifndef DIM_3
%extern "image/oofimage.swg"
#endif
%pragma(python) code="from ooflib.SWIG.common.imagebase import ImageBasePtr"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"
%pragma(python) code="from ooflib.SWIG.common.coord import ICoordPtr"
%pragma(python) code="from ooflib.SWIG.common.corientation import COrientABGPtr"
#ifndef DIM_3
%pragma(python) code="from ooflib.SWIG.image.oofimage import OOFImagePtr"
#endif

class OrientMap {
public:
  OrientMap(ICoord *iPoint, Coord *Point);
  ~OrientMap();
  const COrientABG &angle(const ICoord *iPoint);
  const ICoord sizeInPixels();
  const Coord size();
  ICoord pixelFromPoint(Coord *Point);
  bool pixelInBounds(ICoord *iPoint);
#ifndef DIM_3
  OOFImage *createImage(char *, Angle2Color&);
#endif
};

class OrientMapReader {
public:
  OrientMapReader();
  void set_angle(OrientMap &data, const ICoord *iPoint, const COrientation*);
};

class OrientMapImage : public ImageBase {
public:
  OrientMapImage(OrientMap*, Angle2Color*);
  ~OrientMapImage();
};

void registerOrientMap(char*, OrientMap*);
void removeOrientMap(char*);

#endif // ORIENTMAPDATA_SWG
