// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// General 3-matrix class, has virtual methods for the
// invariants, and is a subclass of OutputVal.  Has sub-classes
// SymmMatrix3 and SmallMatrix3.  The purpose of this class
// is so that the code in invariant.C can be agnostic about
// what kind of matrix it's getting, it can just dynamic-cast
// to *this* class and call the invariant method.  Subclasses
// still have to implement it.

#ifndef MATRIX3_H
#define MATRIX3_H

#include <iostream>
#include "engine/eigenvalues.h"
#include "engine/outputval.h"

class Matrix3 : public OutputVal {
private:
  mutable EigenValues eigenvalues;  // cache.
  mutable bool dirtyeigs_;
  void findEigenvalues() const;
  static std::string classname_;  // PythonExportables need this.
  static std::string modulename_;
public:
  Matrix3() : dirtyeigs_(true) {}
  virtual OutputVal *clone() const = 0;
  virtual OutputVal *zero() const = 0;
  virtual OutputVal *one() const = 0;

  virtual double trace() const = 0;
  virtual double determinant() const = 0;
  virtual double secondInvariant() const = 0;
  // Deviator is not in this set, only symmetric matrices can do that.

  virtual double maxEigenvalue() const = 0;
  virtual double midEigenvalue() const = 0;
  virtual double minEigenvalue() const = 0;
  
};

#endif //MATRIX3_H
