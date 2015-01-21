// -*- C++ -*-
// $RCSfile: cijkl.swg,v $
// $Revision: 1.11.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:28 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

%module cijkl

%{
#include "engine/property/elasticity/cijkl.h"
%}
%include "common/typemaps.swg"
%pragma(python) include="cijkl.spy"
%extern "engine/symmmatrix.swg"
%pragma(python) code="from ooflib.SWIG.engine.symmmatrix import SymmMatrix3Ptr"

class Cijkl {
public:
  Cijkl();
  void clear();
  %addmethods {
    double get(int i, int j, int k, int l) {
      return (*self)(i, j, k, l);
    }
    double getvoigt(int i, int j) {
      return (*self)(i, j);
    }
    void set(int i, int j, int k, int l, double val) {
      (*self)(i, j, k, l) = val;
    }
    void setvoigt(int i, int j, double val) {
      (*self)(i, j) = val;
    }
    SymmMatrix3 __mul__(SymmMatrix3 &other) {
      return (*self)*other;
    }
  }
};
