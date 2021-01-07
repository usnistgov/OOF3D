// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DEFORMATION_SWG
#define DEFORMATION_SWG

%module deformation
%include "engine/typemaps.swg"
%{
#include "engine/deformation.h"
#include "engine/IO/propertyoutput.h"
%}

%extern "engine/IO/propertyoutput.swg"
%pragma(python) code="from ooflib.SWIG.engine.IO.propertyoutput import PropertyOutputInitPtr"

%pragma(python) include="deformation.spy"

class POInitDeformation : public PropertyOutputInit {
public:
  POInitDeformation();
};

#endif // DEFORMATION_SWG
