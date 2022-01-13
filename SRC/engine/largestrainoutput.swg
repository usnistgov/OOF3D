// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


#ifndef LARGESTRAINOUTPUT_SWG
#define LARGESTRAINOUTPUT_SWG

%module largestrainoutput
%include "engine/typemaps.swg"
%{
#include "engine/largestrainoutput.h"
#include "engine/IO/propertyoutput.h"
%}

%extern "engine/IO/propertyoutput.swg"
%pragma(python) code="from ooflib.SWIG.engine.IO.propertyoutput import PropertyOutputInitPtr"

%pragma(python) include="largestrainoutput.spy"

class POInitLargeStrain : public PropertyOutputInit {
public:
  POInitLargeStrain();
};

#endif // LARGESTRAINOUTPUT_SWG
