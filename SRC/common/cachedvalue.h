// -*- C++ -*-
// $RCSfile: cachedvalue.h,v $
// $Revision: 1.2.18.2 $
// $Author: langer $
// $Date: 2011/11/02 17:40:30 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CACHEDVALUE_H
#define CACHEDVALUE_H

#include "common/timestamp.h"

template <class TYPE>
class CachedValue {
private:
  TYPE val;
  TYPE savedValue;
  TimeStamp timestamp_;
  TimeStamp savedtime;
  bool set_;
public:
  CachedValue() {
    timestamp_.backdate();	// out of date!
    savedtime.backdate();
  }
  CachedValue(TYPE x) {
    set_value(x);
    savedtime.backdate();
  }
  const TYPE &value() const {
    return val; 
  }
  void set_value(const TYPE &x) {
    savedValue = val;
    savedtime = timestamp_.cloneAndIncrement();
    val = x;
    ++timestamp_;
  }
  const TimeStamp &timestamp() const { return timestamp_; }
  void revert() {
    if(savedtime > timeZero) {
      val = savedValue;
      timestamp_ = savedtime;
    }
  }
  void copy(const CachedValue<TYPE> &other) {
    val = other.value();
    timestamp_ = other.timestamp().clone();
  }
};

#endif // CACHEDVALUE_H
