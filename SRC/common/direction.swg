// -*- C++ -*-
// $RCSfile: direction.swg,v $
// $Revision: 1.2.2.6 $
// $Author: langer $
// $Date: 2014/07/29 20:26:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DIRECTION_SWG
#define DIRECTION_SWG

%module direction
%include "common/typemaps.swg"
%{
#include "common/direction.h"
%}

%pragma(python) include="direction.spy"

%extern "common/coord.swg"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"

class CDirection {
public:
  ~CDirection();
  double theta();
  double phi();
  double dot(Coord *Point);
  CUnitVectorDirection unitVector();
  %new Coord *coord();
  %new string *identifier();
};

class CUnitVectorDirection : public CDirection {
public:
  CUnitVectorDirection(double, double, double);
  double x();
  double y();
  double z();
};

class CAngleDirection : public CDirection {
public:
  CAngleDirection(double, double);
};

class CDirectionX : public CDirection {
public:
  CDirectionX();
};

class CDirectionY : public CDirection {
public:
  CDirectionY();
};

class CDirectionZ : public CDirection {
public:
  CDirectionZ();
};

#endif // DIRECTION_SWG

