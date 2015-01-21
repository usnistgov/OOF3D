// -*- C++ -*-
// $RCSfile: timestamp.C,v $
// $Revision: 1.17.2.4 $
// $Author: langer $
// $Date: 2014/12/02 21:52:37 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */
#include <oofconfig.h>

#include <iostream>
#include "timestamp.h"
#include <limits>
#include "common/lock.h"
unsigned long TimeStamp::globaltime(0);
unsigned long TimeStamp::globalepoch(0);

static const unsigned long MAXTIME = std::numeric_limits<unsigned long>::max();

SLock TimeStampLock;


TimeStamp::TimeStamp() {
  TimeStampLock.acquire();
  localtime = globaltime;
  localepoch = globalepoch;
  TimeStampLock.release();
}

void TimeStamp::operator++() {
  TimeStampLock.acquire();
  globaltime++;
  if(globaltime == MAXTIME) {
    globaltime = 0;
    globalepoch++;
  }
  localtime = globaltime;
  localepoch = globalepoch;
  TimeStampLock.release();
}

int operator<(const TimeStamp &t1, const TimeStamp &t2) {
  TimeStampLock.acquire();
  bool lt;
  if(t1.localepoch == t2.localepoch)
    lt = t1.localtime < t2.localtime;
  else
    lt = t1.localepoch < t2.localepoch;
  TimeStampLock.release();
  return lt;
}

int operator>(const TimeStamp &t1, const TimeStamp &t2) {
  TimeStampLock.acquire();
  bool gt;
  if(t1.localepoch == t2.localepoch)
    gt= t1.localtime > t2.localtime;
  else
    gt = t1.localepoch > t2.localepoch;
  TimeStampLock.release();
  return gt;
}

TimeStamp TimeStamp::clone() const {
  return TimeStamp(*this);
}

TimeStamp TimeStamp::cloneAndIncrement() {
  TimeStamp ts = clone();
  operator++();
  return ts;
}

std::ostream &operator<<(std::ostream &os, const TimeStamp &ts) {
  return os << "TimeStamp(" << ts.localepoch << "," << ts.localtime << ")";
}

TimeStamp timeZero;

const TimeStamp currentTime() {
  return TimeStamp();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#include <sys/time.h>
#include <sys/resource.h>

double cputime() {
  struct rusage rusage;
  if(getrusage(RUSAGE_SELF, &rusage) == -1)
    return 0.0;
  return rusage.ru_utime.tv_sec + 1.e-6*rusage.ru_utime.tv_usec;
}
