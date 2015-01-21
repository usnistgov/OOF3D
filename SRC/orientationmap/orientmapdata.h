// -*- C++ -*-
// $RCSfile: orientmapdata.h,v $
// $Revision: 1.3.24.4 $
// $Author: langer $
// $Date: 2013/11/08 20:46:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef ORIENTMAPDATA_H
#define ORIENTMAPDATA_H

class OrientMap;
class OrientMapReader;

#include "common/imagebase.h"
#include "common/array.h"
#include "common/corientation.h"
#if DIM == 2
#include "image/oofimage.h"
#elif DIM == 3
#include "image/oofimage3d.h"
#endif
#include <string>
#include <vector>

class Angle2Color;
class StringImage;

// Python has dict of OrientMapReaderRegistrations keyed by file format.  It
// creates an OrientMapReader subclass and passes it to an OrientMap
// constructor.  OrientMapReader subclasses need to provide a read()
// function in Python which creates and returns an OrientMap object.

class OrientMapReader {
public:
  virtual ~OrientMapReader() {}
  void set_angle(OrientMap &data, const ICoord*, const COrientation*) const;
  friend class OrientMap;
};

class OrientMap {
private:
  Array<COrientABG> angles;
  Coord size_;
  std::string name;
public:
  OrientMap(const ICoord*, const Coord*);
  OrientMap(const OrientMap&);
  ~OrientMap();
  const ICoord &sizeInPixels() const { return angles.size(); }
  const Coord &size() const { return size_; }
  ICoord pixelFromPoint(const Coord *point) const;
  bool pixelInBounds(const ICoord *pxl) const;
  const COrientABG &angle(const ICoord *pt) const { return angles[*pt]; }
  const COrientABG &angle(const ICoord pt) const { return angles[pt]; }
  Array<COrientABG>::const_iterator begin() const {return angles.begin();};
  Array<COrientABG>::const_iterator end() const {return angles.end();};
#if DIM == 2
  OOFImage *createImage(const std::string&, const Angle2Color&) const;
#endif
  friend class OrientMapReader;
  friend void registerOrientMap(const std::string&, OrientMap*);
};

void registerOrientMap(const std::string&, OrientMap*);
void removeOrientMap(const std::string&);
OrientMap *getOrientMap(const std::string&);

// OrientMapImage is used when displaying an OrientaionMap object in
// the graphics window.

class OrientMapImage : public ImageBase {
private:
  const OrientMap *orientmap;
  const Angle2Color *colorscheme;
public:
  OrientMapImage(const OrientMap*, const Angle2Color*);
  virtual ~OrientMapImage();
  virtual const Coord &size() const;
  virtual const ICoord &sizeInPixels() const;
};

#endif // ORIENTMAPDATA_H
