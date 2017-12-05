// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

//  Objects and functions for storing and retrieving thread
//  information.  There is exactly one OOFThreadState object per thread.
//  There can be more than one OOFThreadID object for one thread, but
//  they are all equal.  The OOFThreadID is used by findThreadState to
//  retrieve the thread's OOFThreadState.

#ifndef THREADSTATE
#define THREADSTATE

#include "common/lock.h"
#include "common/progress.h"

#include <pthread.h>
#include <vector>

class OOFThreadID {
private:
  pthread_t _ID;
public:
  OOFThreadID();
  const pthread_t & get_ID() const { return _ID; }
};

std::ostream &operator<<(std::ostream&, const OOFThreadID&);
bool operator==(const OOFThreadID&, const OOFThreadID&);
bool operator!=(const OOFThreadID&, const OOFThreadID&);

class OOFThreadState {
private:
  OOFThreadID _ID;	// May be re-used. Depends on pthread implementation.
  int _id;	// Unique among all threads for all time.

  typedef std::vector<Progress*> ProgressList;
  ProgressList progressList;
  ProgressList::iterator findProgressIterator(const std::string&);
  mutable SLock progressLock;
public:
  OOFThreadState();
  ~OOFThreadState();
  int id() const { return _id; }
  const OOFThreadID & get_thread_ID() const { return _ID; }
  
  // getProgress returns an existing Progress object with the given
  // name, or creates a new one with the given type if there isn't an
  // existing object.
  Progress *getProgress(const std::string &name, ProgressType ptype);
  // findProgress returns an existing Progress object with the given
  // name, or raises an exception.
  Progress *findProgress(const std::string &name);
  void impedeProgress();	// set the 'stopped' flag on all Progress objs.
  std::vector<std::string> *getProgressNames() const;
  void acquireProgressLock();
  void releaseProgressLock();
private:
  OOFThreadState(const OOFThreadState&); // prohibited
};

int operator==(const OOFThreadState&, const OOFThreadState&);
std::ostream &operator<<(std::ostream&, const OOFThreadState&);

//void make_thread_main(); // Make the calling thread the new "main" thread.

void initThreadState();

int findThreadNumber();
OOFThreadState *findThreadState();
int nThreadStates();

bool mainthread_query();	// returns true on main thread, false on others.
void mainthread_delete();

// void cleanThreadList();

void cancelThread(OOFThreadState &tobecancelled);
void testcancel();

void textMode();

// OOFThreadState *make_thread_main(); 
// void restore_main_thread(OOFThreadState*);

extern bool threading_enabled;


#endif // THREADSTATE
