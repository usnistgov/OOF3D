// -*- C++ -*-
// $RCSfile: colordifference.swg,v $
// $Revision: 1.7.10.1 $
// $Author: langer $
// $Date: 2014/09/27 22:33:49 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef COLORDIFFERENCE_SWG
#define COLORDIFFERENCE_SWG

%module colordifference
%include "common/typemaps.swg"
%{
#include "common/colordifference.h"
%}

%pragma(python) include="colordifference.spy"

class ColorDifference {}

class DeltaRGB: public ColorDifference {
public:
  DeltaRGB(double dr, double dg, double db);
  ~DeltaRGB();
  bool contains(const CColor &c1, const CColor &c2) const;
};
 
class DeltaGray: public ColorDifference {
public:
  DeltaGray(double dg);
  ~DeltaGray();
  bool contains(const CColor &c1, const CColor &c2) const;
};

class DeltaHSV: public ColorDifference {
public:
  DeltaHSV(double dh, double ds, double dv);
  ~DeltaHSV();
  bool contains(const CColor &c1, const CColor &c2) const;
};

#endif // COLORDIFFERENCE_SWG
