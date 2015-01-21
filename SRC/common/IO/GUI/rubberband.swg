// -*- C++ -*-
// $RCSfile: rubberband.swg,v $
// $Revision: 1.11.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef RUBBERBAND_SWG
#define RUBBERBAND_SWG

%module rubberband
%include "common/typemaps.swg"
%{
#include "common/IO/GUI/rubberband.h"
%}
%extern "gfxbrushstyle.swg"

class RubberBand {};

class NoRubberBand : public RubberBand {
public:
  NoRubberBand();
};

class RectangleRubberBand : public RubberBand {
public:
  RectangleRubberBand();
  ~RectangleRubberBand();
};

class CircleRubberBand : public RubberBand {
public:
  CircleRubberBand();
  ~CircleRubberBand();
};

class EllipseRubberBand : public RubberBand {
public:
  EllipseRubberBand();
  ~EllipseRubberBand();
};

class SpiderRubberBand : public RubberBand {
public:
  SpiderRubberBand(PointVec *PointList);
  ~SpiderRubberBand();
};

class BrushRubberBand : public RubberBand {
public:
  BrushRubberBand(GfxBrushStyle *brush);
  ~BrushRubberBand();
};

class LineRubberBand : public RubberBand {
public:
  LineRubberBand();
  ~LineRubberBand();
};

#endif // RUBBERBAND_SWG
