// -*- C++ -*-
// $RCSfile: ccolor.swg,v $
// $Revision: 1.8.10.1 $
// $Author: langer $
// $Date: 2014/05/29 13:47:29 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CCOLOR_SWG
#define CCOLOR_SWG

%module ccolor
%include "common/typemaps.swg"

%{
#include "common/ccolor.h"
%}

class CColor {
public:
  double getRed();
  double getGreen();
  double getBlue();
  double getAlpha();
  double getGray();
  double getHue();
  double getSaturation();
  double getValue();

  void setRed(double);
  void setGreen(double);
  void setBlue(double);
  void setAlpha(double);
};

class CGrayColor: public CColor {
public:
  void setGray(double);
}

class CHSVColor: public CColor {
public:
  void setHue(double);
  void setSaturation(double);
  void setValue(double);
}

#endif // CCOLOR_SWG
