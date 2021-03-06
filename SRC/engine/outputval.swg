// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef OUTPUTVAL_SWG
#define OUTPUTVAL_SWG


%module outputval
%include "engine/typemaps.swg"
%extern "engine/fieldindex.swg"

%pragma(python) include="outputval.spy"

%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IndexPPtr"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IteratorPPtr"

%{
#include "engine/outputval.h"
#include "common/tostring.h"
typedef OutputVal NewOutputVal;
%}

%typemap(python, out) OutputVal* {
  // typemap(python, out) OutputVal*
  $target = $source->pythonObject();
}

// For transferring ownership to Python.  %new is supposed to add
// thisown=1 to the wrapper, but it doesn't seem to work if there's
// also an "out" typemap.  See comments in outputval.C.

%typemap(python, out) NewOutputVal* {
  // typemap(python, out) NewOutputVal*
  $target = $source->pythonObject();
  if($target) {
    static PyObject *pyOne = 0;
    if(!pyOne)
      pyOne = PyInt_FromLong(1);
    PyObject_SetAttrString($target, "thisown", pyOne);
  }
}

class OutputVal {
public:
  ~OutputVal();
  IndexP getIndex(char *);
  IteratorP getIterator();
  int dim();
  NewOutputVal *clone();
  NewOutputVal *zero();
  %new DoubleList *value_list();
};

class NonArithmeticOutputVal : public OutputVal {
public:
};

class ArithmeticOutputVal : public OutputVal {
public:
  NewOutputVal *one();
  NewOutputVal *dot(ArithmeticOutputVal&);
  void component_pow(int);
  void component_square();
  void component_sqrt();
  void component_abs();
  %addmethods {
    double __getitem__(const IndexP &i) const {
      return (*self)[i];
    }
  }
};

class ScalarOutputVal : public ArithmeticOutputVal {
public:
  ScalarOutputVal(double);
  double value();
  // Arithmetic operations -- it's convenient to have
  // Python-accessible wrapped versions of the addto/subtractfrom
  // operations, which don't mess up the ownership.  These are not
  // substitutes for __add__, __sub__, etc. -- they're called by
  // them.
  %addmethods {
    %new const string *__repr__() const {
      return new std::string(to_string( self->value() ));
    }
    void _add(const ScalarOutputVal &other) {
      (*self) += other;
    }
    void _sub(const ScalarOutputVal &other) {
      (*self) -= other;
    }
    void _mul(double other) {
      (*self) *= other;
    }
    double __float__() const {
      return self->value(); 
    }
  }
};

class VectorOutputVal : public ArithmeticOutputVal {
public:
  int size();
  VectorOutputVal(int);
  %addmethods {
    %new const string *__repr__() const {
      std::string *res = new std::string("[");
      *res += to_string( (*self)[0] );
      for(unsigned int i=1; i<self->size(); i++)
	*res += ", " + to_string( (*self)[i] );
      *res += "]";
      return res;
    }

    // Arithmetic operations -- see comment in ScalarOutputVal, above.
    void _add(const VectorOutputVal &other) {
      (*self) += other;
    }
    void _sub(const VectorOutputVal &other) {
      (*self) -= other;
    }
    void _mul(double other) {
      (*self) *= other;
    }
  }
  %addmethods {
    double __getitem__(const IndexP &i) const {
      return (*self)[i];
    }
    void __setitem__(const IndexP &i, double x) {
      (*self)[i] = x;
    }
    double getItemInt(int i) const {
      return (*self)[i];
    }
  }
};

class ListOutputVal : public NonArithmeticOutputVal {
public:
  ListOutputVal(StringVec*);
  int size();
  %addmethods {
    double __getitem__(const IndexP &i) const {
      return (*self)[i];
    }
    void __setitem__(const IndexP &i, double x) {
      (*self)[i] = x;
    }
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class OutputValue {
public:
  ~OutputValue();
  OutputVal *valuePtr();	// Do NOT transfer ownership!
  OutputValue(const OutputValue&);
  int dim();
  NewOutputVal *valueClone();
};

class NonArithmeticOutputValue : public OutputValue {
};

class ArithmeticOutputValue : public OutputValue {
public:
  %addmethods {
     double __getitem__(const IndexP &i) const {
       return (*self)[i];
     }
     void _add(const ArithmeticOutputValue &other) {
       (*self) += other;
     }
     void _mul(double other) {
       (*self) *= other;
     }
  }
};

int get_globalOutputValueCount();
int get_globalOutputValCount();
void init_globalOutputValCount();

#endif // OUTPUTVAL_SWG
