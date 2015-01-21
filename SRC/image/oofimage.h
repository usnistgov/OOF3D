// -*- C++ -*-
// $RCSfile: oofimage.h,v $
// $Revision: 1.50.18.2 $
// $Author: langer $
// $Date: 2014/08/01 19:53:08 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef OOFIMAGE_H
#define OOFIMAGE_H

#include "common/abstractimage.h"
#include "common/array.h"
#include "common/ccolor.h"
#include "common/colordifference.h"
#include "common/coord.h"
#include "common/ooferror.h"
#include "common/timestamp.h"
#include <string>
#include <vector>
#include <Magick++.h>

class BitmapOverlay;
class BoolArray;
class DoubleArray;
class CMicrostructure;
class StringImage;
class OOFImageIterator;
class ConstOOFImageIterator;

/*----------*/

class OOFImage : public AbstractImage {
protected:
  std::string name_;
  Magick::Image image;
  Coord size_; 
  ICoord sizeInPixels_;		// width, height.
  double scale;			// converts from int rgb to doubles in [0,1]
  void setup();
  TimeStamp timestamp;
  CMicrostructure *microstructure;
public:
  OOFImage(const std::string &nm);
  OOFImage(const std::string &nm, const Coord &sz, const Magick::Geometry &g);
  OOFImage(const std::string &nm, const std::string &filename);
  OOFImage(const std::string &nm, const ICoord&,
	   const std::string &colortype, const Magick::StorageType,
	   const void*);
  OOFImage(const OOFImage&);
  virtual ~OOFImage();
  void save(const std::string &filename);\
  const Magick::Geometry geometry() const { return image.size(); }
  const std::string &name() const { return name_; }
  void rename(const std::string &nm) { name_ = nm; }
  void setSize(const Coord*);

  virtual const Coord &size() const { return size_; }
  virtual const ICoord &sizeInPixels() const { return sizeInPixels_; }
  ICoord pixelFromPoint(const Coord*) const;
  bool pixelInBounds(const ICoord*) const;
  std::string comment() const;

  void setMicrostructure(CMicrostructure *ms) { microstructure = ms; }
  CMicrostructure *getCMicrostructure() const { return microstructure; }
  void removeMicrostructure() { microstructure = 0; }

  typedef OOFImageIterator iterator;
  typedef ConstOOFImageIterator const_iterator;

  iterator begin();
  const_iterator begin() const;
  iterator end();
  const_iterator end() const;

  const CColor operator[](const ICoord &c) const;
  // Version taking ICoord* arg is provided for use in SWIG typemaps.
  const CColor operator[](const ICoord *c) const { return operator[](*c); }
  // Since OOFImage isn't actually made up of CColors, it's hard to
  // use operator[] to set values.  Use this instead:
  void set(const ICoord&, const CColor&);
  void imageChanged();		// call this when done setting pixels.

  // Convert to an Array of doubles.  f is a function that takes a
  // CColor and returns a double.
  Array<double> convert(double (*f)(const CColor&)) const;
  // Same for ints and bools.
  Array<int> convert(int (*f)(const CColor&)) const;
  Array<bool> convert(bool (*f)(const CColor&)) const;
  // Set pixels in the image to values from an array.  These call imageChanged()
  void set(const Array<double> &array, CColor (*f)(double));
  void set(const Array<int> &array, CColor (*f)(int));
  void set(const Array<bool> &array, CColor (*f)(bool));

  // virtual void fillstringimage(StringImage*) const; 

  OOFImage *clone(const std::string &name) const;

  void getColorPoints(const CColor &reference,
		      const ColorDifference &diff,
		      BoolArray &selected) const;

  bool compare(const OOFImage&, double) const;

  std::vector<unsigned short> *getPixels();

  void flip(const std::string &axis);
  void fade(double);
  void dim(double);

  TimeStamp *getTimeStamp() { return &timestamp; }

  // ImageMagick effects
  void blur(double radius, double sigma);
  void contrast(bool sharpen);
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
  void evenly_illuminate(int windowsize);
};

OOFImage *newImageFromData(const std::string &name,
			   const ICoord *isize,
			   const std::vector<unsigned short> *data);

// Parallel image send/recv
#ifdef HAVE_MPI
void _Send_Image(OOFImage*, std::vector<int>*, int);
OOFImage *_Recv_Image(int, int);
#endif //HAVE_MPI

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ImageMagickError : public ErrErrorBase<ImageMagickError> {
  std::string msg;
public:
  ImageMagickError(const std::string&);
  virtual std::string pythonequiv() const {
    return "ImageMagickError('" + msg + "')";
  }
  std::string message() const { return msg; }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class OOFImageIterator {
private:
  OOFImageIterator(OOFImage &image, int pos)
    : pos(pos), image(image)
  {}
  int pos;
  OOFImage &image;
public:
  void operator++() { pos++; }
  CColor operator*() const { return image[coord()]; }
  ICoord coord() const;
  friend class OOFImage;
  friend bool operator==(const OOFImageIterator&, const OOFImageIterator&);
  friend bool operator!=(const OOFImageIterator&, const OOFImageIterator&);
};

class ConstOOFImageIterator {
private:
  ConstOOFImageIterator(const OOFImage &image, int pos)
    : pos(pos), image(image)
  {}
  int pos;
  const OOFImage &image;
public:
  void operator++() { pos++; }
  const CColor operator*() const { return image[coord()]; }
  ICoord coord() const;
  friend class OOFImage;
  friend bool operator==(const ConstOOFImageIterator&,
			 const ConstOOFImageIterator&);
  friend bool operator!=(const ConstOOFImageIterator&,
			 const ConstOOFImageIterator&);
};

OOFImage makeNewImage(const std::string &name,const ICoord*); /////////////////
double color2gray(const CColor&);
CColor gray2color(double);
CColor bool2color(bool);
CColor int2color(int);

DoubleArray grayify(const OOFImage& image);
void setFromBool(OOFImage&, const BoolArray&);


BoolArray threshold(const DoubleArray&, double);
#endif // OOFIMAGE_H
