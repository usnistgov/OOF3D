// -*- C++ -*-
// $RCSfile: angle2color.swg,v $
// $Revision: 1.3.24.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ANGLE2COLOR_SWG
#define ANGLE2COLOR_SWG

%module angle2color
%include "common/typemaps.swg"
%{
#include "engine/angle2color.h"
%}
%pragma(python) include="angle2color.spy"

class Angle2Color {};

class Bunge2RGB : public Angle2Color {
public:
  Bunge2RGB();
};

class Euler2RGB : public Angle2Color {
public:
  Euler2RGB();
};

class Euler2HSV : public Angle2Color {
public:
  Euler2HSV();
};

class Axis2HSV : public Angle2Color {
public:
  Axis2HSV();
};

#endif // ANGLE2COLOR_SWG
