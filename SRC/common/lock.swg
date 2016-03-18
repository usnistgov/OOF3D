// -*- C++ -*-
// $RCSfile: lock.swg,v $
// $Revision: 1.16.10.4 $
// $Author: rdw1 $
// $Date: 2015/07/09 14:59:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef LOCK_SWG
#define LOCK_SWG

%module lock
%include "common/typemaps.swg"
%{
#include "common/lock.h"
%}
%pragma(python) include="lock.spy"

class SLock {
public:
  SLock();
  ~SLock();
  void acquire();
  void release();
  //#ifdef DEBUG
  //void verbose(bool, char*);
  //#endif // DEBUG
};

class Lock : public SLock {
public:
  Lock();
  ~Lock();
  void acquire();
  void release();
};

class Condition {
public:
  Condition(SLock*);
  ~Condition();
  void wait();
  void signal();
  void broadcast();
};

class EventLogSLock {
public:
  EventLogSLock();
  ~EventLogSLock();
  void logNewEvent_acquire();
  void logNewEvent_release();
  void handleNewEvents_acquire();
  void handleNewEvents_release();
};

class RWLock {
public:
  RWLock();
  ~RWLock();
  void read_acquire();
  void read_release();

  void write_acquire();
  void write_release();

  void write_pause();
  void write_resume();
  int nReaders();		// for debugging
};

void enableLocks();
bool disableLocks();

#endif // LOCK_SWG
