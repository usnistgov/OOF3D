// -*- C++ -*-
// $RCSfile: threadstate.C,v $
// $Revision: 1.5.2.10 $
// $Author: fyc $
// $Date: 2014/07/22 15:39:37 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <Python.h>

#include "common/lock.h"
#include "common/ooferror.h"
#include "common/oofomp.h"
#include "common/printvec.h"
#include "common/threadstate.h"
#include "common/IO/oofcerr.h"
#include <iostream>
#include <pthread.h>
#include <string>
#include <vector>

bool text_mode = false;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Because findThreadNumber() is used by debugging output, the lock
// which is used by findThreadNumber() can't be instrumented with
// debugging output of its own.  We have to use an UndebuggableLock
// here, which will never be instrumented.
UndebuggableLock lockListOfStates;

static std::vector<ThreadState*> &listOfStates() {
  static std::vector<ThreadState*> list;
  return list;
}

ThreadState *findThreadState() {
  const ThreadID currentThread;
  std::vector<ThreadState*> &list = listOfStates();
  KeyHolder hldr(lockListOfStates); 

  for(std::vector<ThreadState*>::size_type i=0; i<list.size(); i++) {
    ThreadState *ts = list[i];
    if(ts->get_thread_ID() == currentThread) {
      return ts;
    }
  }
  return 0;
}

int findThreadNumber() {
  ThreadState *ts = findThreadState();
  if(!ts)
    // If this function has been called too early in the thread
    // creation process, the call to findThreadState() can fail.  The
    // only good reason that this function would be called that early
    // is if it's being used to identify the source of debugging
    // output, so raising an exception isn't necessary.  Just return
    // an otherwise impossible number.
    return -1;
    // throw ErrProgrammingError(
    // 	   "findThreadNumber called on a thread with no ThreadState!",
    // 	   __FILE__, __LINE__);
  return ts->id();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ThreadID::ThreadID() {
  _ID = pthread_self();
}

bool operator==(const ThreadID &t1, const ThreadID &t2) {
  return pthread_equal(t1.get_ID(), t2.get_ID());
}

bool operator!=(const ThreadID &t1, const ThreadID &t2) {
  return not pthread_equal(t1.get_ID(), t2.get_ID());
}

std::ostream &operator<<(std::ostream &os, const ThreadID &tid) {
  return os << tid.get_ID();
}

static int uniqueThreadSafeID() {
  static int counter = 0;
  static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
  pthread_mutex_lock(&lock);
  int id = counter++;
  pthread_mutex_unlock(&lock);
  return id;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ThreadIDcompare {
private:
  const ThreadID _ID;
public:
  ThreadIDcompare(const ThreadState *ts) : _ID(ts->get_thread_ID()) {}
  bool operator()(const ThreadState *ts) const {
    return ts->get_thread_ID() == _ID;
  }
};


ThreadState::ThreadState()
  : _id(uniqueThreadSafeID())
{
  // oofcerr << "ThreadState::ctor: " << this << " " << id() << std::endl;
  KeyHolder hldr(lockListOfStates);
  // If there is another ThreadState with the same ThreadID, it must
  // correspond to a thread that's finished (because the system won't
  // reuse a pthread_t from a live thread) but for some reason the
  // ThreadState hasn't been destroyed. 

  std::vector<ThreadState*> &los = listOfStates();
  bool replaced = false;
  for(std::vector<ThreadState*>::iterator i=los.begin(); i<los.end(); ++i) {
    if((*i)->get_thread_ID() == get_thread_ID()) {
      *i = this;
      replaced = true;
      break;
    }
  }
  if(!replaced)
    los.push_back(this);

  int old_cancel_state;
  pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, &old_cancel_state);
  int old_cancel_type;
  // pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, &old_cancel_type);
  pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS, &old_cancel_type);
}

ThreadState::~ThreadState() {
  // oofcerr << "ThreadState::dtor: " << this << " " << id() << std::endl;
  progressLock.acquire();
  for(ProgressList::iterator i=progressList.begin(); i<progressList.end(); ++i)
    {
      delete *i;
    }
  progressList.clear();
  progressLock.release();
  KeyHolder hldr(lockListOfStates);
  std::vector<ThreadState*> &list = listOfStates();
  // It's possible that the ThreadState has already been removed from
  // the list, if another ThreadState with the same pthread ID has
  // already been created.
  for(std::vector<ThreadState*>::iterator i=list.begin(); i<list.end(); ++i) {
    if((*i) == this) {
      list.erase(i);
      break;
    }
  }
}

int nThreadStates() {
  KeyHolder hldr(lockListOfStates);
  return listOfStates().size();
}

std::ostream &operator<<(std::ostream &os, const ThreadState &ts) {
  return os << "ThreadState(id=" << ts.id() << ", ID=" << ts.get_thread_ID()
	    << ")";
}

int operator==(const ThreadState &t1, const ThreadState &t2) {
  return t1.id() == t2.id();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void ThreadState::acquireProgressLock() {
  // oofcerr << "ThreadState::acquireProgressLock: " << this << " " << id()
  // 	  << std::endl;
  progressLock.acquire();
}

void ThreadState::releaseProgressLock() {
  // oofcerr << "ThreadState::releaseProgressLock: " << this << " " << id() 
  // 	  << std::endl;
  progressLock.release();
}

// getProgress retrieves an existing Progress object with the given
// name in the calling thread.  It creates a new one if there isn't an
// existing Progress object with that name.

Progress *ThreadState::getProgress(const std::string &name, ProgressType ptype)
{
  // oofcerr << "ThreadState::getProgress: " << this << " " << id()
  // 	  << std::endl;
  ProgressList::iterator iter;
  try {
    iter = findProgressIterator(name);
  }
  catch (ErrNoProgress &exc) {
    // Create a new Progress object.  The old one wasn't found.
    Progress *progress;
    if(ptype == DEFINITE) {
      progress = new DefiniteProgress(name, this);
    }
    else if(ptype == LOGDEFINITE) {
      progress = new LogDefiniteProgress(name, this);
    }
    else if(ptype == INDEFINITE) {
      progress = new IndefiniteProgress(name, this);
    }
    else {
      throw ErrProgrammingError("Unknown Progress type", __FILE__, __LINE__);
    }
    progressLock.acquire();
    progressList.push_back(progress);
    progressLock.release();
    return progress;
  }
  
  // An old Progress object was found.  Move it to the end of the
  // list, and return it.  It gets moved to the end of the list
  // because since it's nominally just been created, it's subsidiary
  // to any other Progress objects in the thread.
  progressLock.acquire();
  Progress *progress = *iter;
  // oofcerr << "ThreadState::getProgress: reusing old Progress object "
  // 	  << progress << " " << name <<  std::endl;
  progressList.erase(iter);
  progressList.push_back(progress);
  
  progressLock.release();
  return progress;
}

// findProgress retrieves an existing Progress object with the given
// name in the calling thread.  It throws ErrNoProgress if the
// Progress object doesn't exist.

Progress *ThreadState::findProgress(const std::string &name) {
  return *findProgressIterator(name);
}

ThreadState::ProgressList::iterator
ThreadState::findProgressIterator(const std::string &name)
{
  // This linear search shouldn't be too slow, because there should
  // never be hundreds of Progress objects in a single thread.  If we
  // use a std::map instead of a std::vector to store the Progress
  // objects, then information about the order in which they were
  // created would be lost, and we'd have to store extra information
  // to ensure that the bars are displayed in the correct order.

  for(ProgressList::iterator i=progressList.begin(); i<progressList.end();
      ++i)
    {
      if((*i)->name() == name)
	return i;
    }
  throw ErrNoProgress();
}

void ThreadState::impedeProgress() {
  KeyHolder key(progressLock);
  for(ProgressList::iterator i=progressList.begin(); i<progressList.end(); ++i)
    (*i)->stop1();
}

std::vector<std::string> *ThreadState::getProgressNames() const {
  std::vector<std::string> *pnames(new std::vector<std::string>());
  // When this is called by ActivityViewer.__init__ or
  // TextThreadedWorker._drawProgressBars, progressLock has already
  // been acquired.
  pnames->reserve(progressList.size());
  for(ProgressList::const_iterator i=progressList.begin(); i<progressList.end();
      ++i)
    {
      pnames->push_back((*i)->name());
    }
  return pnames;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


static ThreadState *mainthreadstate = 0;

void initThreadState() {
#ifdef _OPENMP
#pragma omp parallel
  {
#pragma omp single
    {
      oofcerr << "Using OpenMP with " << omp_get_num_threads() 
	      << " threads." << std::endl;
    }
  }
#endif // _OPENMP
  // Create a ThreadState object for the main thread.  This is created
  // when the oof module is loaded by Python.
  mainthreadstate = new ThreadState();
}

// // Reassign the mainthreadstate variable -- used to set a new main
// // thread.  This probably should never be used.
// ThreadState *make_thread_main() {
//   ThreadState *ts = findThreadState();
//   if (*ts == *mainthreadstate) 
//     return mainthreadstate; // Calling thread is already main, do nothing.
//   ThreadState *oldmain = mainthreadstate;
//   mainthreadstate = ts;
//   return oldmain;
// }
// // Undo the effect of make_thread_main().
// void restore_main_thread(ThreadState *ts) {
//   mainthreadstate = ts;
// }


// TODO OPT: To clarify the situations in which mainthread_query should
// return true even when not on the main thread, the name of the
// function should be changed.  There should be *two* functions,
// mainthread_safe() and subthread_safe(), which say whether or not
// it's allowable to call functions that have to be called on the
// mainthread or on a subthread in GUI mode.  Both will return true in
// text mode.  Then the tests in Lock::acquire() [and
// mainthreadGUI.runBlock_gui()?] can use subthread_safe() and all
// other mainthread_query() calls can be changed to mainthread_safe().
// Perhaps we should have a third call that actually indicates whether
// or not we're really on the main thread, independent of text mode.

bool mainthread_query() {
  // Are we on the main thread? 
  if(text_mode) {
    // In text mode, all threads are main, because everything is
    // serial.  
    return true;
  }
  ThreadState *ts = findThreadState();
  // The main thread always has a ThreadState object=, so if
  // findThreadState fails, we're not on the main thread.
  return ts && *ts == *mainthreadstate;
}

void mainthread_delete() {
  delete mainthreadstate;
  mainthreadstate = 0;
}

void cancelThread(ThreadState &tobecancelled) {
  // TODO OPT: Why isn't this a ThreadState member function?
  if(tobecancelled == *mainthreadstate) {
    // make sure that the main thread is NOT stopped by this function
    return; 
  }
  else {
    ThreadID id = tobecancelled.get_thread_ID();
    pthread_cancel(id.get_ID());
  }
}

void testcancel() {
  pthread_testcancel();
}

void textMode() {
  text_mode = true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// threading_enabled is used by the swig "except" directive (defined
// in typemaps.swg).  It controls whether
// PyEval_SaveThread/PyEval_RestoreThread pairs surround swigged C++
// function calls.  For reasons that aren't completely understood, if
// those functions are used in unthreaded mode, we get seg faults from
// gtk.

bool threading_enabled=true;

