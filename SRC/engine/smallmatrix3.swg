// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SMALLMATRIX3_SWG
#define SMALLMATRIX3_SWG

%module smallmatrix3
%include "engine/typemaps.swg"

%{
#include "engine/smallmatrix3.h"
%}

%extern "engine/fieldindex.swg"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IteratorPPtr"

class SmallMatrix3 : public Matrix3, public SmallMatrix {
public:
  SmallMatrix3();
  ~SmallMatrix3();
  IteratorP getIterator();
};

// HERE:
// Swig additional stuff following the example from SymmMatrix3?

%new OutputValue *newSmallMatrix3OutputValue();

#endif // SMALLMATRIX3_SWG
