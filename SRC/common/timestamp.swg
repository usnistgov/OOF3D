// -*- C++ -*-
// $RCSfile: timestamp.swg,v $
// $Revision: 1.12.10.2 $
// $Author: langer $
// $Date: 2011/10/25 20:46:56 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef TIMESTAMP_SWG
#define TIMESTAMP_SWG

%module timestamp
%include "common/typemaps.swg"

%{
#include "common/timestamp.h"
#include "common/tostring.h"
%}
%pragma(python) include="timestamp.spy"

class TimeStamp {
public:
  TimeStamp();
  ~TimeStamp();
  void backdate();
  unsigned long time();		// for debugging
  unsigned long epoch();	// for debugging
  TimeStamp clone();
  TimeStamp cloneAndIncrement();
  %addmethods {
    void increment() {
      ++(*self);
    }
    int __cmp__(TimeStamp &other) {
      if (*self < other) return -1;
      if (*self > other) return 1;
      return 0;
    }
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

//double cputime();

%readonly
TimeStamp timeZero;
TimeStamp currentTime();

#endif // TIMESTAMP_SWG
