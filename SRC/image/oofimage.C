// -*- C++ -*-
// $RCSfile: oofimage.C,v $
// $Revision: 1.77.18.3 $
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

#include "image/oofimage.h"
#ifdef HAVE_MPI
#include "common/mpitools.h"
#endif ////HAVE_MPI
#include "common/IO/bitoverlay.h"
#include "common/ooferror.h"
#include "common/boolarray.h"
#include "common/doublearray.h"
#include <math.h>
#include <set>

// get rid of this after debugging
#include <iostream>

OOFImage::OOFImage(const std::string &name, const std::string &filename)
  : name_(name)
{
  // It is apparently necessary to construct a null image first and
  // then perform a "read" operation on it, to get the data from a file.
  // The more obvious "image=Magick::Image(filename)" does not throw
  // an exception if the file cannot be found, it just returns a 
  // mangled and useless Magick::Image object. 
  image = Magick::Image();
  try {
    image.read(filename);
  }
  catch (Magick::Exception &error) {
    // Magick::Exceptions have to be converted into OOF2
    // ImageMagickErrors so that they'll be handled properly by the
    // SWIG exception typemap.
    throw ImageMagickError(error.what());
  }
  image.flip();		// real coordinates don't start at the top
  setup();
}

OOFImage::OOFImage(const std::string &name)
  : name_(name)
{
}

// Constructor for making a new blank image the same size 
// and size-in-pixels as an old one.  You can't just pass in 
// the old image, because that fuction signature is already 
// taken by the real copy constructor.
OOFImage::OOFImage(const std::string &name, const Coord &size, 
		   const Magick::Geometry &g) 
  : name_(name), image(g, Magick::Color(0,0,0)), size_(size)
{
  setup();
}

// Copy constructor that makes an explicit copy -- this bypasses a
// cache-entry-counting bug in the Magick++ API's "Image" class copy
// constructor.  This bug is to have been corrected in 5.5.7-16 and
// later. 
OOFImage::OOFImage(const OOFImage &other) 
  : name_(other.name_),
    image(other.geometry(), Magick::Color(0,0,0)),
    size_(other.size_)
{
  
  Magick::Geometry g = geometry();
  int w = g.width();
  int h = g.height();

  // Fast PixelPacket copy -- uses a lot of memory for big images.
  const Magick::PixelPacket *orig = other.image.getConstPixels(0,0,w,h);
  Magick::PixelPacket *copy = image.setPixels(0,0,w,h);
  
  for(int i=0;i<h*w;i++) {
    copy[i]=orig[i];
  } 
  image.syncPixels();

    
  // Slow pixelColor way.  Uses less memory?
  // image.modifyImage();
  // for(int r=0;r<g.height();r++)
  //   for(int c=0;c<g.width();c++) {
  //     image.pixelColor(r,c,other.image.pixelColor(r,c));
  //  }

  setup();
}

OOFImage *newImageFromData(const std::string &name, const ICoord *isize,
			   const std::vector<unsigned short> *data)
{
  return new OOFImage(name, *isize, "RGB", Magick::ShortPixel, &((*data)[0]));
}

OOFImage::OOFImage(const std::string &name, const ICoord &isize,
		   const std::string &map,
		   const Magick::StorageType storage,
		   const void *data) 
  : name_(name),
    image(isize(0), isize(1), map, storage, data)
{
  setup();
}


void OOFImage::setup() {
  try {
    Magick::Geometry sighs = image.size();
    sizeInPixels_ = ICoord(sighs.width(), sighs.height());
  }
  catch (Magick::Exception &e) {
    throw ImageMagickError(e.what());
  }
  
  // Scale factor for converting ImageMagick rgb values to floats in
  // [0,1].  Using "Magick::MaxRGB" doesn't work, so we have to use
  // "using namespace Magick" to get access to MaxRGB.
  using namespace Magick;
  scale = 1./MaxRGB;
}


OOFImage::~OOFImage() {
}

// Tolerant comparison -- returns a boolean true if the other image
// is within tolerance of this image, otherwise returns false.
bool OOFImage::compare(const OOFImage &other, double tol) const {
  if (sizeInPixels_ != other.sizeInPixels_) return false;

  for(int i=0;i<sizeInPixels_(0);i++) {
    for(int j=0;j<sizeInPixels_(1);j++) {
      CColor c0 = (*this)[ICoord(i,j)];
      CColor c1 = other[ICoord(i,j)];
      if (!c0.compare(c1, tol))
	return false;
    }
  }
  return true;
}

void OOFImage::save(const std::string &filename) {
  Magick::Image copy = image;
  try {
    copy.flip();			// undo flip in constructor
    copy.write(filename);
  }
  catch (Magick::Exception &e) {
    throw ImageMagickError(e.what());
   }
}

void OOFImage::setSize(const Coord *sighs) {
  size_ = *sighs;
}

ICoord OOFImage::pixelFromPoint(const Coord *point) const {
  double xx = (*point)(0)/size_(0)*sizeInPixels_(0);
  double yy = (*point)(1)/size_(1)*sizeInPixels_(1);
  if (xx == sizeInPixels_(0))
    xx = sizeInPixels_(0) - 1.0;
  if (yy == sizeInPixels_(1))
    yy = sizeInPixels_(1) - 1.0;

  return ICoord((int) floor(xx), (int) floor(yy));
}

bool OOFImage::pixelInBounds(const ICoord *pxl) const {
  int xx = (*pxl)(0);
  int yy = (*pxl)(1);
  if ( (xx<0) || (xx>=sizeInPixels_(0)) || (yy<0) || (yy>=sizeInPixels_(1)) )
    return false;
  return true;
}

OOFImage *OOFImage::clone(const std::string &nm) const {
  OOFImage *copy = new OOFImage(nm);
  try {
    copy->image = Magick::Image(image); // Magick::Image copy constructor
  }
  catch (Magick::Exception &e) {
    throw ImageMagickError(e.what());
  }
  copy->setup();
  copy->size_ = size_;
  copy->setMicrostructure(microstructure);
  return copy;
}

OOFImage makeNewImage(const std::string &name, const ICoord *size)
{
  return OOFImage(name,Coord(0,0),Magick::Geometry((*size)(0),(*size)(1)));
}

std::string OOFImage::comment() const {
  return image.comment();
}

void OOFImage::imageChanged() {
  ++timestamp;			// marks image as changed
}

// void OOFImage::fillstringimage(StringImage *stringimage) const {
//   // Convert image into a string suitable for constructing a gdk pixbuf.
//   for(int j=0; j<sizeInPixels_(1); j++) {
//     for(int i=0; i<sizeInPixels_(0); i++) {
//       ICoord where(i,j);
//       CColor color = (*this)[where];
//       stringimage->set(&where, &color);
//     }
//   }
// }

std::vector<unsigned short> *OOFImage::getPixels() {
  // Magick::Image::write isn't const, so this function isn't const either.
  int n = 3*sizeInPixels_(0)*sizeInPixels_(1);
  std::vector<unsigned short> *pxls = new std::vector<unsigned short>(n);
  image.write(0, 0, sizeInPixels_(0), sizeInPixels_(1),
	      "RGB", Magick::ShortPixel, &(*pxls)[0]);
  return pxls;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Access to individual pixels.

const CColor OOFImage::operator[](const ICoord &c) const {
  try {
    Magick::Color color = image.pixelColor(c(0), c(1));
    return CColor(color.redQuantum()*scale,
		  color.greenQuantum()*scale,
		  color.blueQuantum()*scale);
  }
  catch (Magick::Exception &e) {
    throw ImageMagickError(e.what());
  }
}

// TODO 3.1: It may be useful to have "block-set" routines which use
// the ImageMagick PixelPacket routine to set many pixels together.
// This is alleged to be much faster.  See the OOFImage copy
// constructor definition for an example.
void OOFImage::set(const ICoord &c, const CColor &color) {
  try {
    Magick::ColorRGB culler(color.getRed(), color.getGreen(), color.getBlue());
    image.pixelColor(c(0), c(1), culler);
  }
  catch (Magick::Exception &e) {
    throw ImageMagickError(e.what());
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Conversion to and from arrays of double, int, or bool.  This is not
// an efficient way of getting or setting just a few pixels.  These
// routines all take as an argument a function f which converts from
// CColor to the appropriate type (double, int, or bool) or vice
// versa.

// TODO 3.1: Is it better to make these functions use
// OOFImage::image::write, like OOFImage::getPixels does?  Doing so
// would require allocating another array, so it's not obviously more
// efficient.

Array<double> OOFImage::convert(double (*f)(const CColor&)) const {
  Array<double> arr(sizeInPixels_(0), sizeInPixels_(1));
  for(Array<double>::iterator i=arr.begin(); i!=arr.end(); ++i) {
    arr[i] = (*f)((*this)[i.coord()]);
  }
  return arr;
}

Array<int> OOFImage::convert(int (*f)(const CColor&)) const {
  Array<int> arr(sizeInPixels_(0), sizeInPixels_(1));
  for(Array<int>::iterator i=arr.begin(); i!=arr.end(); ++i) {
    arr[i] = (*f)((*this)[i.coord()]);
  }
  return arr;
}

Array<bool> OOFImage::convert(bool (*f)(const CColor&)) const {
  Array<bool> arr(sizeInPixels_(0), sizeInPixels_(1));
  for(Array<bool>::iterator i=arr.begin(); i!=arr.end(); ++i) {
    arr[i] = (*f)((*this)[i.coord()]);
  }
  return arr;
}

void OOFImage::set(const Array<double> &array, CColor (*f)(double)) {
  for(Array<double>::const_iterator i=array.begin(); i!=array.end(); ++i) 
    set(i.coord(), (*f)(array[i]));
	imageChanged();
}

void OOFImage::set(const Array<int> &array, CColor (*f)(int)) {
  for(Array<int>::const_iterator i=array.begin(); i!=array.end(); ++i)
    set(i.coord(), (*f)(array[i]));
  imageChanged();
}

void OOFImage::set(const Array<bool> &array, CColor (*f)(bool)) {
  for(Array<bool>::const_iterator i=array.begin(); i!=array.end(); ++i)
    set(i.coord(), (*f)(array[i]));
  imageChanged();
}
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// std::vector<ICoord>* OOFImage::getColorPoints(const CColor &ref, 
// 					      const ColorDifference &diff)
// const
// {
//   std::vector<ICoord>* icoordlist = new std::vector<ICoord>(0);
//   // Be greedy, reserve enough space for all the pixels.
//   icoordlist->reserve(sizeInPixels_(0)*sizeInPixels_(1));
//   for(ConstOOFImageIterator i=this->begin(); i!=this->end(); ++i) {
//     if ( diff.contains(ref, *i) )
//       icoordlist->push_back(i.coord());
//   }
//   return icoordlist;  // memory leak
// }

void OOFImage::getColorPoints(const CColor &ref, 
			      const ColorDifference &diff,
			      BoolArray &selected)
const
{
  for(ConstOOFImageIterator i=this->begin(); i!=this->end(); ++i)
    if (diff.contains(ref, *i)) selected[i.coord()] = true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

OOFImage::iterator OOFImage::begin() {
  return OOFImageIterator(*this, 0);
}

OOFImage::const_iterator OOFImage::begin() const {
  return ConstOOFImageIterator(*this, 0);
}

OOFImage::iterator OOFImage::end() {
  return OOFImageIterator(*this, sizeInPixels_(0)*sizeInPixels_(1));
}

OOFImage::const_iterator OOFImage::end() const {
  return ConstOOFImageIterator(*this, sizeInPixels_(0)*sizeInPixels_(1));
}


ICoord OOFImageIterator::coord() const {
  int width = image.sizeInPixels()(0);
  int y = pos/width;
  int x = pos - width*y;
  return ICoord(x, y);
}

ICoord ConstOOFImageIterator::coord() const {
  int width = image.sizeInPixels()(0);
  int y = pos/width;
  int x = pos - width*y;
  return ICoord(x, y);
}

bool operator==(const OOFImageIterator &a, const OOFImageIterator &b) {
  return a.pos == b.pos;
}

bool operator!=(const OOFImageIterator &a, const OOFImageIterator &b) {
  return a.pos != b.pos;
}


bool operator==(const ConstOOFImageIterator &a, const ConstOOFImageIterator &b){
  return a.pos == b.pos;
}

bool operator!=(const ConstOOFImageIterator &a, const ConstOOFImageIterator &b){
  return a.pos != b.pos;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Examples of image modification routines.

void OOFImage::flip(const std::string &axis) {
  if(axis == "x")
    image.flop();		// ImageMagick function call
  else if(axis == "y")
    image.flip();
  else if(axis == "xy") {
    image.flip();
    image.flop();
  }
  imageChanged(); // call this after using ImageMagick modification routines
}

void OOFImage::dim(double factor) {
  for(OOFImage::iterator i=begin(); i!=end(); ++i) {
    CColor c = *i;
    c.dim(factor);
    set(i.coord(), c);
  }
  imageChanged();		// call this after setting pixels directly
}

double color2gray(const CColor &color) {
  return color.getGray();
}

CColor gray2color(double x) {
  return CColor(x, x, x);
}

CColor bool2color(bool x) {
  if(x)
    return CColor(1,1,1);
  else
    return CColor(0,0,0);
}

CColor int2color(int x) {
  return CColor(x, x, x);
}

void OOFImage::gray() {
  // simple example using OOFImage::convert()
  Array<double> arr = convert(color2gray);
  set(arr, gray2color);		// calls imageChanged() itself
}

void OOFImage::fade(double factor) {
  for(OOFImage::iterator i=begin(); i!=end(); ++i) {
    CColor c = *i;
    c.fade(factor);
    set(i.coord(), c);
  }
  imageChanged();
}

void OOFImage::blur(double radius, double sigma) {
  image.blur(radius, sigma);
  imageChanged();
}

void OOFImage::contrast(bool sharpen) {
  image.contrast(sharpen);
  imageChanged();
}

void OOFImage::despeckle() {
  image.despeckle();
  imageChanged();
}

void OOFImage::edge(double radius) {
  image.edge(radius);
  imageChanged();
}

void OOFImage::enhance() {
  image.enhance();
  imageChanged();
}

void OOFImage::equalize() {
  image.equalize();
  imageChanged();
}

void OOFImage::medianFilter(double radius) {
  image.medianFilter(radius);
  imageChanged();
}

void OOFImage::negate(bool grayscale) {
  image.negate(grayscale);
  imageChanged();
}

void OOFImage::normalize() {
  image.normalize();
  imageChanged();
}

void OOFImage::reduceNoise(double radius) {
  image.reduceNoise(radius);
  imageChanged();
}

void OOFImage::sharpen(double radius, double sigma) {
  image.sharpen(radius, sigma);
  imageChanged();
}

BoolArray threshold(const DoubleArray& image1, double tolerance)
{
// This function converts a grayscale image to binary (black/white).
// Any value above the tolerance value (passed in) is changed to white
// and any value under the tolerance is change to black.

  bool color;  // The color of the current pixel
  int w = image1.width();  // Image width
  int h = image1.height();  // Image height
  BoolArray newimage(w, h);  // Copies the image from the passed in (image1) to the function's image (image)
  for (DoubleArray::const_iterator i = image1.begin(); i != image1.end(); ++i) {  // For width
    if (image1[i]<=tolerance) // If cell is under tolerance,
      color = false;  // Make low pixels black
    else
      color = true; // Make high pixels white
    newimage[i.coord()] = color;  // Cell takes new color as set above	
  }

  return newimage;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO 3.1: On Linux, ImageMagickErrors all have trailing backslashes.
// They've got to be coming from here. 
ImageMagickError::ImageMagickError(const std::string &messg) {
  // Make sure that all quotation marks in messg are escaped.
  for(std::string::size_type i=0; i<messg.size(); ++i) {
    char c = messg[i];
    if(c == '"' || c == '\'')
      msg += '\\';
    msg += c;
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Utility functions moved from imageops.C.

DoubleArray grayify(const OOFImage& image) {
//Creates a gray image from a color image.
  return image.convert(color2gray);
}


void setFromBool(OOFImage& colorImage, const BoolArray& image) {
  colorImage.set(image,bool2color);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Parallel image send/recv
#ifdef HAVE_MPI
void _Send_Image(OOFImage *image, std::vector<int> *destinations, int tag)
{
  std::string name = image->name();
  _Isend_Int(name.size(), destinations, tag);  // size of the name
  _Isend_String(name, destinations, tag);  // name itself
  _Isend_Double(image->size()(0), destinations, tag);  // physical size X
  _Isend_Double(image->size()(1), destinations, tag);  // physical size Y
  _Isend_Int(image->sizeInPixels()(0), destinations, tag);  // size in pixels X
  _Isend_Int(image->sizeInPixels()(1), destinations, tag);  // size in pixels Y

  std::vector<unsigned short> * pixels = image->getPixels();
  _Isend_Int(pixels->size(), destinations, tag);  // size of pixels vector
  _Isend_UnsignedShortVec(pixels, destinations, tag);
  delete pixels;
}

OOFImage *_Recv_Image(int origin, int tag)
{
  int name_size = _Recv_Int(origin, tag);  // size of the name
  std::string name = _Recv_String(origin, name_size, tag);  // name itself
  double px = _Recv_Double(origin, tag);  // physical size X
  double py = _Recv_Double(origin, tag);  // physical size Y
  int ix = _Recv_Int(origin, tag);  // size in pixels X
  int iy = _Recv_Int(origin, tag);  // size in pixels Y
  int size_pixels = _Recv_Int(origin, tag);  // size of pixels vector
  std::vector<unsigned short> *pixels = _Recv_UnsignedShortVec(origin,
							       size_pixels,
							       tag);
  Coord *psize = new Coord(px, py);
  ICoord *isize = new ICoord(ix, iy);
  
  OOFImage *image = newImageFromData(name, isize, pixels);
  image->setSize(psize);

  delete psize;
  delete isize;
  delete pixels;

  return image;
}
#endif //HAVE_MPI
