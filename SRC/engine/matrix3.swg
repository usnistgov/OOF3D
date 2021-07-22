// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


// This can be super-basic, it just needs to exist so that
// Python instances of the base classes have the right
// class structure.   This might change if we decide we
// need to call invariant methods from Python.

#ifndef MATRIX3_SWG

%module matrix3

%include "engine/typemaps.swg"

%{
#include "engine/matrix3.h"
%}

%pragma(python) code="from ooflib.SWIG.engine.outputval import OutputValPtr"
%extern "engine/outputval.swg"
  
class Matrix3 : public OutputVal {
}

// Constructor makes no sense, it has virtual fns.

#endif // MATRIX3_SWG
