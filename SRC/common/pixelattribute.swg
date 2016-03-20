// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PIXELATTRIBUTE_SWG
#define PIXELATTRIBUTE_SWG

%module pixelattribute
%include "common/typemaps.swg"
%{
#include "common/pixelattribute.h"
%}
%pragma(python) include="pixelattribute.spy"

class PxlAttributeRegistration {
public:
  const string &name();
};

%typemap(python, out) PxlAttributeRegistration* {
  $target = $source->pythonObject();
}

int nAttributes();
PxlAttributeRegistration *getRegistration(int);

#endif // PIXELATTRIBUTE_SWG
