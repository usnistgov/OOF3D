// -*- C++ -*-
// $RCSfile: threadstate.swg,v $
// $Revision: 1.4.2.4 $
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

#ifndef THREADSTATE_SWG
#define THREADSTATE_SWG

%module threadstate
%include "common/typemaps.swg"
%extern "common/progress.swg"
%pragma(python) include="common/threadstate.spy"

%{
#include "common/threadstate.h"
#include "common/progress.h"
#include "common/tostring.h"
%}

class ThreadID {
public:
  ThreadID();
  %addmethods {
    bool __eq__(ThreadID &right) {
      return operator==(*self,right);
    }
    %new const string *__repr__() {
      return new std::string(to_string(self->get_ID()));
    }
  }
};

class ThreadState {
 public:
  ThreadState();
  ~ThreadState();
  const ThreadID & get_thread_ID();
  int id();
  %new StringVec *getProgressNames();
  Progress *getProgress(char*, ProgressType);
  Progress *findProgress(char*);
  void impedeProgress();
  void acquireProgressLock();
  void releaseProgressLock();
  %addmethods {
    int __eq__(ThreadState &right) {
      return operator==(*self,right);
    }
  }
};

void initThreadState();
int findThreadNumber();
ThreadState *findThreadState();
bool mainthread_query();
void mainthread_delete();
int nThreadStates();

void textMode();

bool threading_enabled;


void cancelThread(ThreadState &tobecancelled); 
/*
  Handle with care!! cancelThread WILL stop a thread without any regard to 
  any cleanup that must be done.
*/

void testcancel();

Progress *getProgress(char *name, ProgressType);


#endif // THREADSTATE_SWG

  
