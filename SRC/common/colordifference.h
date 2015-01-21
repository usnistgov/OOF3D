// -*- C++ -*-
// $RCSfile: colordifference.h,v $
// $Revision: 1.6.18.1 $
// $Author: langer $
// $Date: 2014/09/19 03:24:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/ccolor.h"

#ifndef COLORDIFFERENCE_H
#define COLORDIFFERENCE_H

// Base class for all color differences. 
class ColorDifference {
public:
  virtual ~ColorDifference() {}
  virtual bool contains(const CColor &c1, const CColor &c2) const = 0;
  virtual ColorDifference *clone() const = 0;
  virtual void print(std::ostream&) const = 0;
};


class DeltaRGB: public ColorDifference {
private:
  double delta_red, delta_green, delta_blue;
public:
  DeltaRGB(double dr, double dg, double db) : 
    delta_red(dr), delta_green(dg), delta_blue(db) {}
  virtual ~DeltaRGB() {}
  virtual bool contains(const CColor &c1, const CColor &c2) const;
  virtual ColorDifference *clone() const {
    return new DeltaRGB(delta_red, delta_green, delta_blue);
  }
  virtual void print(std::ostream&) const;
};


class DeltaGray: public ColorDifference {
private:
  double delta_gray;
public:
  DeltaGray(double dg) : delta_gray(dg) {}
  virtual ~DeltaGray() {}
  virtual bool contains(const CColor &c1, const CColor &c2) const;
  virtual ColorDifference *clone() const {
    return new DeltaGray(delta_gray);
  }
  virtual void print(std::ostream&) const;
};

class DeltaHSV: public ColorDifference {
private:
  double delta_hue;
  double delta_saturation;
  double delta_value;
public:
  DeltaHSV(double dh, double ds, double dv) :
    delta_hue(dh), delta_saturation(ds), delta_value(dv) {}
  virtual ~DeltaHSV() {}
  virtual bool contains(const CColor &c1, const CColor &c2) const;
  virtual ColorDifference *clone() const {
    return new DeltaHSV(delta_hue, delta_saturation, delta_value);
  }
  virtual void print(std::ostream&) const;
};

std::ostream &operator<<(std::ostream &, const ColorDifference&);

#endif // COLORDIFFERENCE_H
