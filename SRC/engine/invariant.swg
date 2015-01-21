// -*- C++ -*-
// $RCSfile: invariant.swg,v $
// $Revision: 1.6.18.2 $
// $Author: langer $
// $Date: 2014/06/27 20:30:33 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef INVARIANT_SWG
#define INVARIANT_SWG

%module invariant

%include "engine/typemaps.swg"
%{
#include "engine/invariant.h"
#include "common/ooferror.h"
%}
%pragma(python) include="engine/invariant.spy"

class Invariant {
public:
  %addmethods{
    double __call__(OutputVal &ov) {
      return (*self)(ov);
    }
  }
};

class Magnitude : public Invariant {
public:
  Magnitude();
};

class MatrixTrace : public Invariant {
public:
  MatrixTrace();
};

class SecondInvariant : public Invariant {
public:
  SecondInvariant();
};

class Determinant : public Invariant {
public:
  Determinant();
};

class Deviator : public Invariant {
public:
  Deviator();
}

%typemap(python, in) EigenValueRank* (EigenValueRank rank) {
  // $source is a Python EigenValueRank, which is a subclass of
  // enum.Enum and defined in invariant.spy.  We're converting it to a
  // C++ EigenValueRank, which is just an enum defined in invariant.h.
  // This routine relies on the order in which the Python
  // EigenValueRank values were listed in the class definition.
  
  int indx = PyInt_AsLong(PyObject_CallMethod($source, (char *) "index", NULL));
  switch(indx) {
  case 0:
    rank = MAX_EIGENVALUE;
    break;
  case 1:
    rank = MID_EIGENVALUE;
    break;
  case 2:
    rank = MIN_EIGENVALUE;
    break;
  default:
    throw ErrProgrammingError("Bad EigenValueRank!", __FILE__, __LINE__);
  }
  $target = &rank;
}

class Eigenvalue : public Invariant {
public:
  Eigenvalue(EigenValueRank*);
};

#endif // INVARIANT_SWG
