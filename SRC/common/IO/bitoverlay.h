// -*- C++ -*-
// $RCSfile: bitoverlay.h,v $
// $Revision: 1.23.10.11 $
// $Author: langer $
// $Date: 2014/10/17 21:47:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef BITOVERLAY_H
#define BITOVERLAY_H

#include "common/boolarray.h"
#include "common/coord.h"
#include "common/ccolor.h"
#include <string>
#include <set>

// TODO OPT: Should this use vtkStructuredGrid instead of BoolArray?

class BitmapOverlay { 
private:
  ICoord sizeInPixels_;
  Coord size_;
  CColor fg, bg;
  // voxelAlpha is only used in 3D
  double voxelAlpha, tintAlpha;
  // // The timestamp is used externally to determine if the image needs
  // // to be redrawn.
  // TimeStamp timestamp;
public:
  BitmapOverlay(const Coord *size, const ICoord *isize);
  virtual ~BitmapOverlay();
  BoolArray data;
  void clear();
  void invert();
  void resize(const Coord*, const ICoord*);
  void set(const ICoord*);
  void set(const ICoordVector*);
  void reset(const ICoord*);
  void reset(const ICoordVector*);
  void toggle(const ICoord*);
  void toggle(const ICoordVector*);
  bool get(const ICoord*) const;
  void copy(const BitmapOverlay*);
  bool contains(const ICoord *pt) const { return data.contains(*pt); }
  void setColor(const CColor*);
  void setVoxelAlpha(double alpha) { voxelAlpha=alpha; }
  void setTintAlpha(double alpha) { tintAlpha=alpha; }
  double getVoxelAlpha() const { return voxelAlpha; }
  double getTintAlpha() const { return tintAlpha; }
  virtual const Coord &size() const { return size_; }
  virtual const ICoord &sizeInPixels() const { return sizeInPixels_; }
  ICoordVector *pixels(int i) const { return data.pixels(i); }
  ICoordVector *getPixels(bool v) const { return data.pixels(v); }
  bool empty() const { return data.empty(); }
};


#endif
