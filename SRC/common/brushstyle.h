// -*- C++ -*-
// $RCSfile: brushstyle.h,v $
// $Revision: 1.17.18.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BRUSHSTYLE_H
#define BRUSHSTYLE_H

#include <vector>
#include <iostream>

#include "common/coord_i.h"
class BoolArray;
class CMicrostructure;

// Brush styles for selecting objects with the brush selection tool.
// The non-gui part defined here only provides a way of getting the
// pixels.  GUI code for drawing the rubberband is in
// common/IO/GUI/gfxbrushstyle.*.

// BrushStyle is a CRegisteredClass.  Registrations for the subclassed
// defined here are in brushstyle.spy.


class BrushStyle {
public:
  virtual ~BrushStyle() {}
  // Given a microstructure and a brush position (the Coord argument),
  // getPixels sets the pixels in the BoolArray that are inside the
  // brush region.  The routine can resize the BoolArray as necessary
  // and can also set the offset, which determines position of the
  // BoolArray within the Microstructure.
  virtual void getPixels(const CMicrostructure*, const Coord&,
			 BoolArray&, BoolArray&, ICoord &offset) = 0;
};

class CircleBrush : public BrushStyle {
protected:
  double r;
public:
  CircleBrush(double r) : r(r) {}
  virtual ~CircleBrush() {}
  virtual void getPixels(const CMicrostructure*, const Coord&,
			 BoolArray&, BoolArray&, ICoord&);
};

class SquareBrush : public BrushStyle {
protected:
  double size;
public:
  SquareBrush(double hs) : size(hs) {}
  virtual ~SquareBrush() {}
  virtual void getPixels(const CMicrostructure*, const Coord&,
			 BoolArray&, BoolArray&, ICoord&);
};

#endif // BRUSHSTYLE_H
