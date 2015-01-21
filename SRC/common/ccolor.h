// -*- C++ -*-
// $RCSfile: ccolor.h,v $
// $Revision: 1.19.10.5 $
// $Author: langer $
// $Date: 2014/07/29 18:40:26 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CCOLOR_H
#define CCOLOR_H

#include <iostream>

// Utility class for holding cached conversion values, including a
// cache marker.  This is set to true automatically by the nontrivial
// constructor, and to false by the default constructor, but must be
// manually set to false if the cached value becomes stale.
class Triple {
public:
  double x, y, z; // Hue/Red, Saturation/Green, Value/Blue.
  bool ok;
  Triple(double x_in, double y_in, double z_in): 
    x(x_in), y(y_in), z(z_in), ok(true) {}
  Triple(): ok(false) {}
};


// Base class for different color objects.  Is constructible, and 
// contains RGB data.  The RGB color representation is privileged,
// since routine color operations must occur in *some* space, this
// is the usual one, and it simplifies the calling interfaces.

// TODO 3.1: Get rid of alpha?  We don't allow transparent colors to be
// assigned to materials, selections, etc, although we do allow layer
// transparency to be set independently.

class CColor {
protected:
  double red_, green_, blue_, alpha_;
  mutable Triple hsv;
public:
  CColor() : red_(0.0), green_(0.0), blue_(0.0), alpha_(1.0)  {}
  CColor(double r, double g, double b):
    red_(r), green_(g), blue_(b), alpha_(1.0)  {}
  CColor(double r, double g, double b, double a):
    red_(r), green_(g), blue_(b), alpha_(a)  {}

  virtual ~CColor();

  virtual double getRed() const { return red_; }
  virtual double getGreen() const { return green_; }
  virtual double getBlue() const { return blue_; }
  virtual double getAlpha() const { return alpha_; }

  void setRed(double r);
  void setGreen(double g);
  void setBlue(double b);
  void setAlpha(double a);

  virtual double getGray() const { return (red_ + green_ + blue_)/3.0; }

  virtual double getHue() const; 
  virtual double getSaturation() const;
  virtual double getValue() const;

  virtual void fade(double factor);
  virtual void dim(double factor);

  virtual bool operator<(const CColor &) const;

	virtual void operator=(const CColor &);

  virtual void print(std::ostream&) const;
  virtual CColor *clone() const {
    return new CColor(red_, green_, blue_, alpha_);
  }
  // Tolerant comparison.
  bool compare(const CColor&, double) const;
  // Intolerant comparison
  bool operator!=(const CColor&) const;

  std::string name() const;
};



// less-than operator used when making std::maps and std::sets of
// colors, which require the colors to be sortable.
// struct ltCColor {
//   bool operator()(const CColor&, const CColor&) const;
// };


class CGrayColor: public CColor {
public:
  CGrayColor() : CColor(0,0,0) {}
  CGrayColor(double gr): CColor(gr, gr, gr) {}
  virtual ~CGrayColor() {}

  void setGray(double gr);
  virtual void print(std::ostream&) const;
  virtual CColor *clone() const {
    return new CGrayColor(red_);
  }
};

class CHSVColor: public CColor {
public:
  CHSVColor() : CColor(0,0,0) {}
  CHSVColor(double h, double s, double v);
  virtual ~CHSVColor() {}

  // These become fairly expensive operations.
  void setHue(double);
  void setSaturation(double);
  void setValue(double);
  virtual void print(std::ostream&) const;
  virtual CColor *clone() const {
    return new CHSVColor(red_, green_, blue_);
  }
};

double L1dist(const CColor&, const CColor&);
double L2dist2(const CColor&, const CColor&);

std::ostream &operator<<(std::ostream&, const CColor&);

#endif
