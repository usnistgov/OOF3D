// -*- C++ -*-
// $RCSfile: oofimage.swg,v $
// $Revision: 1.45.12.2 $
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

#ifndef OOFIMAGE_SWG
#define OOFIMAGE_SWG
%module oofimage
%include "common/typemaps.swg"
%{
#include "image/oofimage.h"
#include "common/ooferror.h"
#include <oofconfig.h>
#include "common/doublearray.h"
#include "common/boolarray.h"
//typedef Array<bool> arraybool;
// typedef Array<double> arraydouble;
%}

%pragma(python) include="oofimage.spy"
%extern "common/IO/bitoverlay.swg"
%extern "common/ccolor.swg"
%extern "common/timestamp.swg"
%extern "common/ooferror.swg"
%extern "common/abstractimage.swg"
%extern "common/IO/stringimage.swg"

%extern "common/doublearray.swg"
%pragma(python) code="from ooflib.SWIG.common.doublearray import DoubleArrayPtr"
%extern "common/boolarray.swg"
%pragma(python) code="from ooflib.SWIG.common.boolarray import BoolArrayPtr"
%pragma(python) code="from ooflib.SWIG.common.boolarray import BoolArrayPtr"
%pragma(python) code="from ooflib.SWIG.common.ccolor import CColorPtr"
%pragma(python) code="from ooflib.SWIG.common.timestamp import TimeStampPtr"
%pragma(python) code="from ooflib.SWIG.common.ooferror import ErrErrorPtr"
%pragma(python) code="from ooflib.SWIG.common.abstractimage import AbstractImagePtr"

class OOFImage : public AbstractImage {
public:
  OOFImage(char *name, char *filename);
  ~OOFImage();
  void save(char *filename);
  const string &name();
  void rename(char *);
  string comment();
  void setSize(Coord *Point);
  
  Coord size();
  ICoord sizeInPixels();
  ICoord pixelFromPoint(Coord *Point);
  bool pixelInBounds(ICoord *iPoint);
  OOFImage *clone(char *name);

  void setMicrostructure(CMicrostructure*);
  CMicrostructure *getCMicrostructure();
  void removeMicrostructure();

  %new ShortVec *getPixels();
  void flip(char *axis);
  void fade(double);
  void dim(double);
  void blur(double, double);
  void contrast(bool);
  void despeckle();
  void edge(double);
  void enhance();
  void equalize();
  void medianFilter(double);
  void negate(bool);
  void normalize();
  void reduceNoise(double);
  void sharpen(double, double);
  void gray();
  void evenly_illuminate(int);
  
  bool compare(OOFImage&, double);
  // virtual void fillstringimage(StringImage*) const; 

  // getTimeStamp is redefined in oofimage.spy so that it can have optional args
  %name(_getTimeStamp) TimeStamp *getTimeStamp();
  %addmethods {
    CColor __getitem__(ICoord *iPoint) {
      return (*self)[iPoint];
    }
  }
};

%new OOFImage makeNewImage(char *name,ICoord *iPoint);

%new OOFImage *newImageFromData(char *name, ICoord *iPoint, ShortVec*);

// Parallel image send/recv
#ifdef HAVE_MPI
void _Send_Image(OOFImage*, IntVec*, int);
%new OOFImage *_Recv_Image(int, int);
#endif //HAVE_MPI

BoolArray threshold(DoubleArray,double);

class ImageMagickError : public ErrError {
public:
  ImageMagickError(char *m);
  ~ImageMagickError();
  %addmethods {
    string __repr__() {
      return self->message();
    }
  }
};

DoubleArray grayify(const OOFImage& image);
void setFromBool(OOFImage&, const BoolArray&);


#endif // OOFIMAGE_SWG
