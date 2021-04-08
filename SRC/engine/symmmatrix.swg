// -*- C++ -*-
// $RCSfile: symmmatrix.swg,v $
// $Revision: 1.30.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SYMMMATRIX_SWG
#define SYMMMATRIX_SWG

%module symmmatrix
%include "engine/typemaps.swg"

%{
#include "engine/symmmatrix.h"
%}

%pragma(python) include="engine/symmmatrix.spy"
%extern "engine/outputval.swg"
%pragma(python) code="from ooflib.SWIG.engine.outputval import OutputValPtr"
%pragma(python) code="from ooflib.SWIG.engine.outputval import OutputValuePtr"
%extern "engine/fieldindex.swg"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IteratorPPtr"

class SymmMatrix {
public:
  SymmMatrix(int);
  ~SymmMatrix();
  int size();
  %addmethods {
    double get(int i, int j) {
      double v =  (*self)(i,j);
      return v;
    }
    void set(int i, int j, double val) {
      (*self)(i,j)=val;
    }
    // *= defined in Python only for scalars.
    SymmMatrix __imul__(double x) {
      return (*self).operator*=(x);
    }
    bool __eq__(SymmMatrix *other) {
      return other && *self == *other;
    }
    bool __ne__(SymmMatrix *other) {
      return !(other && *self == *other);
    }
  } 
};

#endif // SYMMMATRIX_SWG
