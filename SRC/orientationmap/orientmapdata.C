// -*- C++ -*-
// $RCSfile: orientmapdata.C,v $
// $Revision: 1.4.24.11 $
// $Author: fyc $
// $Date: 2014/07/29 21:24:02 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "engine/angle2color.h"
#include "common/ccolor.h"
#include "orientationmap/orientmapdata.h"
#include <iostream>
#include <map>
#include <string>

#include <vtkImageData.h>

void OrientMapReader::set_angle(OrientMap &data, const ICoord *where,
			  const COrientation *angle) const 
{
  data.angles[*where] = angle->abg();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Stuff for maintaining a list of all OrientMap objects, so that they
// can be found by the OrientationMapProps when needed.

struct ltchar {
  bool operator()(const std::string &s1, const std::string &s2) const {
    return s1 < s2;
  }
};

typedef std::map<std::string, OrientMap*, ltchar> OrientMapMap;

static OrientMapMap &all_OrientationMaps() {
  static OrientMapMap d;
  return d;
}

void registerOrientMap(const std::string &name, OrientMap *data) {
  all_OrientationMaps()[name] = data;
  data->name = name;
}

void removeOrientMap(const std::string &name) {
  OrientMapMap::iterator i = all_OrientationMaps().find(name);
  if(i != all_OrientationMaps().end())
    all_OrientationMaps().erase(i);
}

OrientMap *getOrientMap(const std::string &name) {
  OrientMapMap::iterator i = all_OrientationMaps().find(name);
  if(i != all_OrientationMaps().end())
    return (*i).second;
  return 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


OrientMap::OrientMap(const ICoord *pxlsize, const Coord *size)
  : angles(*pxlsize, COrientABG(0.0 ,0.0, 0.0)),
    size_(*size)
{}

OrientMap::~OrientMap() {
  // delete self from the list of all OrientMap objects
  OrientMapMap::iterator i = all_OrientationMaps().find(name);
  // OrientMap object may not be registered, if the construction process
  // aborted for some reason (such as the data having the wrong size).
  if(i == all_OrientationMaps().end()) {
    return;
  }
  all_OrientationMaps().erase(i);
}

ICoord OrientMap::pixelFromPoint(const Coord *point) const {
  // Copied nearly verbatim from OOFImage.  TODO MER: Perhaps there should
  // be a common base class?
  int px = sizeInPixels()[0];
  int py = sizeInPixels()[1];
  double xx = (*point)[0]/size_[0]*px;
  double yy = (*point)[1]/size_[1]*py;
  if (xx == px)
    xx = px - 1.0;
  if (yy == py)
    yy = py - 1.0;
#if DIM==2
  return ICoord((int) floor(xx), (int) floor(yy));
#elif DIM==3
  int pz = sizeInPixels()[2];
  double zz = (*point)[2]/size_[2]*pz;
  if(xx == pz)
    zz = py - 1.0;
  return ICoord((int) floor(xx), (int) floor(yy), (int) floor(zz));
#endif	// DIM==3
}

bool OrientMap::pixelInBounds(const ICoord *pxl) const {
  for(int i=0; i<DIM; i++) {
    int xx = (*pxl)[i];
    if(xx < 0 || xx >= sizeInPixels()[i])
      return false;
  }
  return true;
  // // Also copied nearly verbatim from OOFImage.  TODO MER: Perhaps there
  // // should be a common base class?
  // int xx = (*pxl)[0];
  // int yy = (*pxl)[1];
  // if ( (xx<0) || (xx>=sizeInPixels()[0]) || (yy<0) || (yy>=sizeInPixels()[1]) )
  //   return false;
  // return true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

OrientMapImage::OrientMapImage(const OrientMap *data, const Angle2Color *scheme)
  : orientmap(data),
    colorscheme(scheme->clone())
{
  image = vtkSmartPointer<vtkImageData>::New();
  image->SetDimensions(sizeInPixels()[0],sizeInPixels()[1],sizeInPixels()[2]);
  image->SetScalarTypeToUnsignedChar();
  image->SetNumberOfScalarComponents(3);
  image->AllocateScalars();

  for(Array<COrientABG>::const_iterator i=orientmap->begin();
      i!=orientmap->end(); ++i) 
    {
      const CColor color = (*scheme)(orientmap->angle(i.coord()));
      // SetScalarComponentFromFloat (or Double) is slow
      unsigned char* ptr = 
	(unsigned char*)image->GetScalarPointer(i.coord()[0], i.coord()[1],
						i.coord()[2]);
      ptr[0] = color.getRed();
      ptr[1] = color.getGreen();
      ptr[2] = color.getBlue();
  }

  // padImage(1);
  image->Update();
}

OrientMapImage::~OrientMapImage() {
  delete colorscheme;
}

const Coord &OrientMapImage::size() const {
  return orientmap->size();
}

const ICoord &OrientMapImage::sizeInPixels() const {
  return orientmap->sizeInPixels();
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Convert an Orientation Map to an OOFImage, so that it can be
// operated on by pixel selection tools, etc.  This is completely
// different from just converting the Map to a displayable
// OrientMapImage.  The OrientMapImage is just a display method, but
// createImage makes an OOFImage Who object and adds it to the
// Microstructure's list of Images.

// TODO MER: 3D version of this

#if DIM == 2
#include <Magick++.h>


OOFImage *OrientMap::createImage(const std::string &name,
				 const Angle2Color &colorscheme) const
{
  OOFImage *immidge = new OOFImage(name);
  unsigned int width = sizeInPixels()[0];
  unsigned int height = sizeInPixels()[1];
  double *pixels = new double[height*width*3*sizeof(double)];
  int count=0;
  for(Array<COrientABG>::const_iterator i=angles.begin(); i!=angles.end();
      ++i,++count)
    {
      const CColor color = colorscheme(angles[i]);
      pixels[3*count] = color.getRed();
      pixels[3*count+1] = color.getGreen();
      pixels[3*count+2] = color.getBlue();
    }
  try {
    immidge = new OOFImage(name, sizeInPixels(), "RGB", Magick::DoublePixel,
			   pixels);
  }
  catch (Magick::Exception &e) {
    delete [] pixels;
    throw ImageMagickError(e.what());
  }
  delete [] pixels;
  return immidge;
}
#endif	// DIM == 2
