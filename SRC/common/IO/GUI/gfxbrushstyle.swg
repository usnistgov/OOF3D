// -*- C++ -*-
// $RCSfile: gfxbrushstyle.swg,v $
// $Revision: 1.6.18.1 $
// $Author: langer $
// $Date: 2014/09/27 22:34:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GFXBRUSHSTYLE_SWG
#define GFXBRUSHSTYLE_SWG

%module gfxbrushstyle
%include "common/typemaps.swg"
%{
#include "common/IO/GUI/gfxbrushstyle.h"
%}

%extern "common/brushstyle.swg"
%pragma(python) include="gfxbrushstyle.spy"
%pragma(python) code="from ooflib.SWIG.common.brushstyle import CircleBrushPtr"
%pragma(python) code="from ooflib.SWIG.common.brushstyle import SquareBrushPtr"

class GfxBrushStyle {
public:
  ~GfxBrushStyle();
};

class GfxCircleBrush : public GfxBrushStyle, public CircleBrush {
public:
  GfxCircleBrush(double);
};

class GfxSquareBrush : public GfxBrushStyle, public SquareBrush {
public:
  GfxSquareBrush(double);
};

#endif // GFXBRUSHSTYLE_SWG
