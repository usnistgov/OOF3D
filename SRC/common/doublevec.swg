// # -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DOUBLEVEC_SWG
#define DOUBLEVEC_SWG

%module doublevec

%{
#include <cstring>
#include "common/doublevec.h"
%}

%pragma(python) include="doublevec.spy"

class DoubleVec {
public:
  DoubleVec(int size, double val=0);
  ~DoubleVec();
  
  int size() const;
  void resize(int size, double val=0);
  void zero();
  void ones();

  double norm() const;

  void axpy(double alpha, const DoubleVec& x);
  void scale(double alpha);
  double dot(const DoubleVec&);
  void eval();
  const std::string str() const;
};

%addmethods DoubleVec {
  const char* __repr__() {
    return (*self).str().c_str();
  }

  void copy_inplace(DoubleVec *x) {
    *self = *x;
  }

  %new DoubleVec *clone() {
    return new DoubleVec(*self);
  }

  // Increment the entry at index i by the amount v.
  // Do not use this too much.
  void increment(int i, double v) {
    (*self)[i] += v;
  }

  void save(const char *filename) {
    save_vec(*self, std::string(filename));
  }

  void load(const char *filename) {
    load_vec(*self, std::string(filename));
  }
}

#endif // DOUBLEVEC_SWG
