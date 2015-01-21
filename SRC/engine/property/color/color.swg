// -*- C++ -*-
// $RCSfile: color.swg,v $
// $Revision: 1.15.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:23 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

%module colorproperty

%{
#include "engine/property/color/color.h"
#include "common/ccolor.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%pragma(python) code="from ooflib.SWIG.common.ccolor import CColorPtr"
%extern "common/ccolor.swg"

class ColorProp : public Property {
public:
  ColorProp(PyObject *self, char *name, CColor *cv);
  CColor color();
};

%pragma(python) include="engine/property/color/color.spy"
