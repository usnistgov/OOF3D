// -*- C++ -*-
// $RCSfile: progress.swg,v $
// $Revision: 1.2.2.2 $
// $Author: langer $
// $Date: 2013/01/28 16:58:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PROGRESS_SWG
#define PROGRESS_SWG

%module progress
%include "common/typemaps.swg"

%{
#include "common/progress.h"
%}

enum ProgressType {
  DEFINITE,
  LOGDEFINITE,
  INDEFINITE
};

Progress *getProgress(char*, ProgressType);
Progress *findProgress(char*);
Progress *findProgressByID(int);

class Progress {
public:
  ~Progress();
  void setProgressBar(PyObject*);
  bool hasProgressBar();
  bool started();
  // See comments in progress.h.
  void finish();
  bool finished();
  void stop();
  bool stopped();
  void setMessage(char*);
  void setFraction(double);
  %new string *message();
  const string &name();
  int id();
  void acquireThreadLock();
  void releaseThreadLock();
  void disconnectBar(PyObject*);
  %addmethods {
    bool __eq__(Progress *other) {
      return self->id() == other->id();
    }
    int __hash__() {
      return self->id();
    }
  }
};

class DefiniteProgress : public Progress {
 public:
  double getFraction();
};

class LogDefiniteProgress : public DefiniteProgress {
public:
  void setRange(double, double);
}

class IndefiniteProgress : public Progress {
public:
  void pulse();
  unsigned long pulsecount();
};

#endif // PROGRESS_SWG
