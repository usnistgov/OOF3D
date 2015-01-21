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

// This particular inheritance is a problem for indexing -- both
// SymmMatrix and OutputVal have __getitem__ overrides, and the order
// in which the classes appear here dictates which one gets found by
// Python.  This is a problem because they take different arguments --
// the OutputVal wants an IndexP, and the SymmMatrix wants a tuple of
// integers.  Currently, the OutputVal __getitem__ is privileged, and
// SymmMatrix users must use the .get method, which takes the two
// integers that would be in the tuple.  It would be nicer if the
// __getitem__ were homogenous.
class SymmMatrix3 : public OutputVal, public SymmMatrix {
public:
  SymmMatrix3(double, double, double, double, double, double);
  ~SymmMatrix3();
  double trace();
  double determinant();
  double secondInvariant();
  double deviator();
  double maxEigenvalue();
  double midEigenvalue();
  double minEigenvalue();
  double contract(SymmMatrix3&);
  IteratorP getIterator();
  
  // Because of maintenance-of-ownership requirements for OutputVal
  // subclasses, these routines should operate in-place on the object
  // and not return anything.  This prevents SWIG from automatically
  // making new "Ptr" objects of dubious provenance.
  %addmethods {
    void _add(const SymmMatrix3 &other) {
      (*self) += other;
    }
    void _sub(const SymmMatrix3 &other) {
      (*self) -= other;
    }
    void _mul(double other) {
      (*self) *= other;
    }
  }
};

%new OutputValue *newSymTensorOutputValue();

#endif // SYMMMATRIX_SWG
