// -*- C++ -*-
// $RCSfile: oofimage3d.swg,v $
// $Revision: 1.3.10.18 $
// $Author: langer $
// $Date: 2013/02/13 22:33:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef OOFIMAGE3D_SWG
#define OOFIMAGE3D_SWG
%module oofimage3d
%include "common/typemaps.swg"
%{
#include <oofconfig.h>
#include "common/boolarray.h"
#include "common/cmicrostructure.h"
#include "common/doublearray.h"
#include "common/ooferror.h"
#include "image/oofimage3d.h"
%}

%pragma(python) include="oofimage3d.spy"
%extern "common/IO/bitoverlay.swg"
%extern "common/ccolor.swg"
%extern "common/timestamp.swg"
%extern "common/ooferror.swg"
%extern "common/imagebase.swg"

%extern "common/doublearray.swg"
%pragma(python) code="from ooflib.SWIG.common.doublearray import DoubleArrayPtr"
%extern "common/boolarray.swg"
%pragma(python) code="from ooflib.SWIG.common.boolarray import BoolArrayPtr"
%pragma(python) code="from ooflib.SWIG.common.ccolor import CColorPtr"
%pragma(python) code="from ooflib.SWIG.common.timestamp import TimeStampPtr"
%pragma(python) code="from ooflib.SWIG.common.ooferror import ErrErrorPtr"
%pragma(python) code="from ooflib.SWIG.common.imagebase import ImageBasePtr"

class OOFImage3D : public ImageBase {
public:
  OOFImage3D(char *name, StringVec *files, Coord *Point);
  ~OOFImage3D();

  const string &name();
  void rename(char *);

  ICoord pixelFromPoint(Coord *Point);
  bool pixelInBounds(ICoord *iPoint);

  void setMicrostructure(CMicrostructure*);
  CMicrostructure *getMicrostructure();
  void removeMicrostructure();

  bool compare(OOFImage3D&, double);

  void save(char *filepattern, char *format);

  %new OOFImage3D *clone(char *name);

  // getTimeStamp is redefined in oofimage.spy so that it can have optional args
  %name(_getTimeStamp) TimeStamp *getTimeStamp();
  %addmethods {
    CColor __getitem__(ICoord *iPoint) {
      return (*self)[iPoint];
    }
  }

  %new UCharVec *getPixels();

  void gray();
  void threshold(double T);
  void blur(double radius, double sigma);
  void dim(double factor);
  void fade(double factor);
  void negate(double dummy);
  void medianFilter(int radius);
  void normalize();
  void contrast(double);
  void flip(char *axis);
  void permuteAxes(char*);
};


%new OOFImage3D *newImageFromData(char *name, Coord *Point, ICoord *iPoint,
				  UCharVec*);

#endif // OOFIMAGE3D_SWG
