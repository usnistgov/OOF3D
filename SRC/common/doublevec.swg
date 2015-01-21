// -*- C++ -*-
// $RCSfile: doublevec.swg,v $
// $Revision: 1.1.4.6 $
// $Author: langer $
// $Date: 2014/10/15 20:53:44 $

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

%include "common/typemaps.swg"

%{
#include <string.h>		// for memcpy & memset
#include <fstream>
#include <iostream>
#include <string>
#include <algorithm>
#include "common/doublevec.h"
#include "common/printvec.h"
#include "common/tostring.h"
#include "common/vectormath.h"
#include "common/IO/oofcerr.h"
%}

%pragma(python) include="doublevec.spy"

// DoubleVec is *not* typemapped into a list of doubles, so it's a
// lightweight Python object.

class DoubleVec {
public:
  DoubleVec(int);
  ~DoubleVec();
  int size();
  void resize(int);
  double norm();
  void clear();
};

%addmethods DoubleVec {

  %new const string *__repr__() {
#ifdef DEBUG
     return new std::string("DoubleVec(" + to_string(self->size())
			    + ", " + self->addr() + ")");
#else
     return new std::string("DoubleVec(" + to_string(self->size()) + ")");
     // return new std::string(to_string(*self));
#endif // DEBUG
  }

  // axpy() and scale() operate in place and *don't* return the result
  // because doing so makes SWIG create a copy.
  void axpy(double a, DoubleVec *x) {
    axpy(a, *x, *self);
  }

  void scale(double a) {
    scale(a, *self);
  }

  double dot(DoubleVec *x) {
    return (*self) * (*x);
  }

  void copy_inplace(DoubleVec *x) { // Copy values of x to self.
    self->resize(x->size());
    memcpy(&(*self)[0], &(*x)[0], x->size()*sizeof(double));
  }

  %new DoubleVec *clone() {
    return new DoubleVec(*self);
  }

  // Increment the entry at index i by the amount v. Don't use this
  // too much.
  void increment(int i, double v) {
    (*self)[i] += v;
  }

  // save(), load(), and unit() are provided mainly for testing.
  void save(const char *filename) {
    std::ofstream fs(filename);
    fs << *self << std::endl;
    fs.close();
  }

  void load(const char *filename) {
    std::ifstream fs(filename);
    while(fs) {
      double v;
      fs >> v;
      if(fs)
	self->push_back(v);
    }
  }
  
  // Make a unit vector in the n direction.
  void unit(int n) {
    memset(&(*self)[0], 0, self->size()*sizeof(double));
    (*self)[n] = 1.0;
  }

  void zero() {
    memset(&(*self)[0], 0, self->size()*sizeof(double));
  }

  %new DoubleVec *sorted() {	// for debugging
    DoubleVec *r = new DoubleVec(*self);
    std::sort(r->begin(), r->end());
    return r;
  }
 };


#ifdef DEBUG
void printVecSizes(char*);
%inline %{
  int getVecSizes() { return DoubleVec::total; }
%}
#endif // DEBUG

#endif // DOUBLEVEC_SWG
