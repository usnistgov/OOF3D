// -*- C++ -*-
// $RCSfile: imageformat.swg,v $
// $Revision: 1.1.2.4 $
// $Author: langer $
// $Date: 2014/05/20 13:43:35 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef IMAGEFORMAT_SWG
#define IMAGEFORMAT_SWG

%module imageformat
%include "common/typemaps.swg"

%{
#include "common/IO/imageformat.h"
%}
%pragma(python) include="common/IO/imageformat.spy"

class ImageFormat {
public:
  ~ImageFormat();
  const string &suffix();
};

class BitmapImageFormat : public ImageFormat {
};

class JPEGImageFormat : public BitmapImageFormat {
public:
  JPEGImageFormat(int);
};

class TIFFImageFormat : public BitmapImageFormat {
public:
  TIFFImageFormat();
};

class PNGImageFormat : public BitmapImageFormat {
public:
  PNGImageFormat();
};

class EPSImageFormat : public BitmapImageFormat {
public:
  EPSImageFormat();
};

class PNMImageFormat : public BitmapImageFormat {
public:
  PNMImageFormat();
};

class BMPImageFormat : public BitmapImageFormat {
public:
  BMPImageFormat();
};

// class PDFImageFormat : public ImageFormat {
// public:
//   PDFImageFormat();
// };

#endif // IMAGEFORMAT_SWG
