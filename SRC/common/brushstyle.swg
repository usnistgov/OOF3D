// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BRUSHSTYLE_SWG
#define BRUSHSTYLE_SWG

%module brushstyle

%include "common/typemaps.swg"
%{
#include "common/brushstyle.h"
%}

%pragma(python) include="brushstyle.spy"

class BrushStyle {};

class CircleBrush: public BrushStyle {
public:
  CircleBrush(double);
  ~CircleBrush();
};

class SquareBrush: public BrushStyle {
public:
  SquareBrush(double);
  ~SquareBrush();
};

#endif // BRUSHSTYLE_SWG
