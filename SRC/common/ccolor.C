// -*- C++ -*-
// $RCSfile: ccolor.C,v $
// $Revision: 1.22.10.4 $
// $Author: langer $
// $Date: 2014/09/27 22:33:48 $


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
#include <math.h>

Triple rgb_to_hsv(double r, double g, double b) {
  double maxval = (r > g ? r : g);
  maxval = (maxval > b ? maxval : b);

  double minval = (r < g ? r : g);
  minval = (minval < b ? minval : b);

  double delta = maxval-minval;
  
  double h, s, v;
  
  if (maxval==0.0) {  // It's black, s=0, h and v irrelevant.
    h=0.0; s=0.0; v=0.0; 
  }
  else if (delta==0.0) { // It's gray, h and s are 0, value is nontrivial.
    h=0.0; s=0.0; v=maxval;
  }
  else {   // Find which sextant.
    s = delta/maxval;
    v = maxval;
    if (r==maxval)
      h = (g-b)/delta;
    else if (g==maxval)
      h = 2.0+(b-r)/delta;
    else 
      h = 4.0+(r-g)/delta;
    h *= 60.0; // Original h is between 0 and 6.
    if (h<0.0)
      h+=360.0;
  }
  return Triple(h, s, v);
}

// Algorithm taken from http://www.cs.rit.edu/~ncs/color/t_convert.html
Triple hsv_to_rgb(double h, double s, double v) {
  double r=0.0, g=0.0, b=0.0;
  if (s==0.0) {
    r=v; g=v; b=v;
  }
  else {
    double hue=h/60.0;
    int sextant = (int)floor(hue);
    double fract = hue-sextant; // Fractional part.
    double p = v*(1.0-s);
    double q = v*(1.0-s*fract);
    double t = v*(1.0-s*(1.0-fract));
    
    switch(sextant) {
    case 0:
    case 6: 
      r=v; g=t; b=p;
      break;
    case 1:
      r=q; g=v; b=p;
      break;
    case 2:
      r=p; g=v; b=t;
      break;
    case 3:
      r=p; g=q; b=v;
      break;
    case 4:
      r=t; g=p; b=v;
      break;
    case 5:
      r=v; g=p; b=q;
    }
  }
  return Triple(r, g, b);
}
  
CColor::~CColor() {}

void CColor::fade(double factor) {
  red_ = 1.0 - (1.0 - red_)*(1.0-factor);
  green_ = 1.0 - (1.0 - green_)*(1.0-factor);
  blue_ = 1.0 - (1.0 - blue_)*(1.0-factor);
  hsv.ok=false;
}

void CColor::dim(double factor) {
  red_ *= factor;
  blue_ *= factor;
  green_ *= factor;
  if(factor > 1.0) {
    if(red_ > 1.0) red_ = 1.0;
    if(green_ > 1.0) green_ = 1.0;
    if(blue_ > 1.0) blue_ = 1.0;
  }
  hsv.ok=false;
}

bool CColor::operator<(const CColor &other) const {
  if ( other.red_ < red_ ) return true;
  if ( other.red_ > red_ ) return false;
  if ( other.green_ < green_ ) return true;
  if ( other.green_ > green_ ) return false;
  if ( other.blue_ < blue_ ) return true;
  return false; 
}

void CColor::operator=(const CColor &other) {
	this->red_ = other.red_;
	this->green_ = other.green_;
	this->blue_ = other.blue_;
}


void CColor::setRed(double r) {
  red_ = r;
  hsv.ok=false;
}

void CColor::setGreen(double g) {
  green_ = g;
  hsv.ok=false;
}

void CColor::setBlue(double b) {
  blue_ = b;
  hsv.ok=false;
}

void CColor::setAlpha(double a) {
  alpha_ = a;
}

void CGrayColor::setGray(double gr) {
  red_ = gr;
  green_ = gr;
  blue_ = gr;
  hsv.ok=false;
}

CHSVColor::CHSVColor(double h, double s, double v) {
  Triple rgb = hsv_to_rgb(h, s, v);
  red_ = rgb.x;
  green_ = rgb.y;
  blue_ = rgb.z;
  hsv = Triple(h, s, v);
}

void CHSVColor::setHue(double h) {
  hsv = rgb_to_hsv(red_, green_, blue_);
  hsv.x = h; hsv.ok=true;
  Triple rgb = hsv_to_rgb(hsv.x, hsv.y, hsv.z);
  red_ = rgb.x; green_=rgb.y; blue_=rgb.z;
}

void CHSVColor::setSaturation(double s) {
  hsv = rgb_to_hsv(red_, green_, blue_);
  hsv.y = s; hsv.ok=true;
  Triple rgb = hsv_to_rgb(hsv.x, hsv.y, hsv.z);
  red_ = rgb.x; green_=rgb.y; blue_=rgb.z;
}

void CHSVColor::setValue(double v) {
  hsv = rgb_to_hsv(red_, green_, blue_);
  hsv.z = v; hsv.ok=true;
  Triple rgb = hsv_to_rgb(hsv.x, hsv.y, hsv.z);
  red_ = rgb.x; green_=rgb.y; blue_=rgb.z;
}

// Nontrivial conversion routines.  All gray conversions are trivial.

double CColor::getHue() const {
  if (!hsv.ok) {
    hsv = rgb_to_hsv(red_, green_, blue_);
  }
  return hsv.x;
}

double CColor::getSaturation() const {
  if (!hsv.ok) {
    hsv = rgb_to_hsv(red_, green_, blue_);
  }
  return hsv.y;
}

double CColor::getValue() const {
  if (!hsv.ok) {
    hsv = rgb_to_hsv(red_, green_, blue_);
  }
  return hsv.z;
}

// Returns true if all of the attributes are within tol.
bool CColor::compare(const CColor &c1, double tol) const {
  if ((fabs(red_-c1.red_)>tol) ||
      (fabs(green_-c1.green_)>tol) ||
      (fabs(blue_-c1.blue_)>tol))
    return false;
  return true;
}

bool CColor::operator!=(const CColor &other) const {
  return (red_ != other.red_ ||
	  green_ != other.green_ ||
	  blue_ != other.blue_ ||
	  alpha_ != other.alpha_);
}


// L1dist and L2dist2 operate in RGB-space.

double L1dist(const CColor &c1, const CColor &c2) {
  return ((fabs(c1.getRed() - c2.getRed()) +
	   fabs(c1.getGreen() - c2.getGreen()) +
	   fabs(c1.getBlue() - c2.getBlue()))/3.0);
}

double L2dist2(const CColor &c1, const CColor &c2) {
  double dr = c1.getRed() - c2.getRed();
  double dg = c1.getGreen() - c2.getGreen();
  double db = c1.getBlue() - c2.getBlue();
  return dr*dr + dg*dg + db*db;
}

std::ostream &operator<<(std::ostream &os, const CColor &c) {
  c.print(os);
  return os;
}

void CColor::print(std::ostream &os) const {
  os << "CColor(" << getRed() << ", " << getGreen() << ", " << getBlue()
     << ", " << getAlpha() << ")";
}

void CGrayColor::print(std::ostream &os) const {
  os << "CGrayColor(" << getGray() << ")";
}

void CHSVColor::print(std::ostream &os) const {
  os << "CHSVColor(" << getHue() << ", " << getSaturation() 
     << ", " << getValue() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


std::string CColor::name() const {
  int r = red_*256;
  if(r == 256) r = 255;
  int g = green_*256;
  if(g == 256) g = 255;
  int b = blue_*256;
  if(b == 256) b = 255;
  char buffer[8];
  sprintf(buffer, "#%02x%02x%02x", r, g, b);
  return std::string(buffer);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// bool ltCColor::operator()(const CColor &color1, const CColor &color2) const {
//   double c1 = color1.getRed();
//   double c2 = color2.getRed();
//   if(c1 < c2) return true;
//   if(c1 > c2) return false;
//   c1 = color1.getGreen();
//   c2 = color2.getGreen();
//   if(c1 < c2) return true;
//   if(c1 > c2) return false;
//   if(color1.getBlue() < color2.getBlue()) return true;
//   return false;
// }
