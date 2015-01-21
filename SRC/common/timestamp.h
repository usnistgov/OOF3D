// -*- C++ -*-
// $RCSfile: timestamp.h,v $
// $Revision: 1.13.10.3 $
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

// Class to keep track of what's happened when, so that the program
// knows if something is out of date with respect to something else.
// Each TimeStamp object is associated with a certain event.  When
// that event occurs, it should call TimeStamp::operator++().  Then it
// can see whether the event preceded another event by comparing their
// timestamps with operator<() or operator>().

#ifndef TIMESTAMP_H
#define TIMESTAMP_H

#include <iostream>

class TimeStamp {
private:
  static unsigned long globaltime;
  static unsigned long globalepoch; // in case of overflow in globaltime
  unsigned long localtime;
  unsigned long localepoch;
public:
  TimeStamp();
  TimeStamp(const TimeStamp &ts)
    : localtime(ts.localtime),
      localepoch(ts.localepoch)
  {}
  void operator++();
  void backdate() { localtime = 0; localepoch = 0;}
  TimeStamp clone() const;
  // cloneAndIncrement clones *this, increments *this, then returns the clone.
  TimeStamp cloneAndIncrement();
  unsigned long time() const { return localtime; } // for debugging
  unsigned long epoch() const { return localepoch; } // for debugging
  friend int operator<(const TimeStamp&, const TimeStamp&);
  friend int operator>(const TimeStamp&, const TimeStamp&);

  friend std::ostream &operator<<(std::ostream&, const TimeStamp&);
};

double cputime();

extern TimeStamp timeZero;
const TimeStamp currentTime();

#endif
