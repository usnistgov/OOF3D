// -*- C++ -*-
// $RCSfile: lock.h,v $
// $Revision: 1.18.10.6 $
// $Author: langer $
// $Date: 2014/05/08 14:38:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef LOCK_H
#define LOCK_H


#include <sys/types.h>
#include <pthread.h>
#include <string>

class LockBase {
public:
  virtual ~LockBase() {}
  virtual void acquire() = 0;
  virtual void release() = 0;
};

// SLock is the Silent lock, with no instrumentation.  It is allowed
// to run on the main thread and doesn't obey disableLocks().  It
// should only be used in Safe circumstances, where there is no chance
// that an exception will be thrown between calls to acquire() and
// release().

class SLock : public LockBase{
private:
  pthread_mutex_t lock;
#ifdef DEBUG
  bool verbose_;
  std::string name;
#endif // DEBUG
public:
  SLock();
  virtual ~SLock();
  virtual void acquire();
  virtual void release();
#ifdef DEBUG
  void verbose(bool, const char*);
#endif // DEBUG
  friend class Condition;
};

// A Lock can't be locked on the main thread.  It should be used
// instead of SLock almost always.  In unthreaded mode, where locks
// aren't useful, Locks can be disabled by calling disableLocks().

class Lock : public SLock {
public:
  Lock() {}
  virtual ~Lock() {}
  virtual void acquire();
  virtual void release();
};

// An UndebuggableLock doesn't check which thread it's on, and it also
// never prints debugging information, which makes it possible to use
// it inside debugging code.  See threadstate.C.

class UndebuggableLock : public LockBase {
private:
  pthread_mutex_t lock;
public:
  UndebuggableLock();
  virtual ~UndebuggableLock();
  virtual void acquire();
  virtual void release();
  friend class Condition;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class Condition {
protected:
  pthread_cond_t condition;
  SLock *lock;
#ifdef DEBUG
  bool verbose_;
  std::string name;
#endif // DEBUG
public:
  Condition(SLock*);
  virtual ~Condition();
  // wait() releases the lock, and blocks until signal() or
  // broadcast() is called in another thread, at which time wait()
  // reacquires the lock and returns.
  void wait();	
  // Use broadcast instead of signal if it's possible that more than
  // one thread is waiting.
  void signal();
  void broadcast();
#ifdef DEBUG
  void verbose(bool, const std::string&);
#endif // DEBUG
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Wrapper for the custom RWLock.  Having a custom class means not
// having to cope with architecture-dependent implementations, or the
// even-more-inconvenient absence thereof.
class RWLock {
protected:
  int r, w, p;			// read, write, pause
  pthread_mutex_t local_lock;
  // Condition signalled when r=w=0 becomes true.
  pthread_cond_t rw_zero;
#ifdef DEBUG
  bool verbose_;
#endif // DEBUG
public:
  RWLock();
  ~RWLock();
  void write_acquire();
  void write_release();

  void read_acquire();
  void read_release();

  void write_pause();
  void write_resume();

  int nReaders() const { return r; }
#ifdef DEBUG
  void verbose(bool);
#endif // VERBOSE
};


// // Uninstrumented RWLock -- used where RWLock protection is required,
// // but main thread access is required.  This should be quite rare.
// class SRWLock : public RWLock {
// public:
//   SRWLock() {};
//   virtual ~SRWLock() {};
//   virtual void write_acquire();
  
//   virtual void read_acquire();
// };

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The KeyHolder is a wrapper for a mutex lock.  The constructor
// acquires the lock and the destructor releases it.  Creating a
// KeyHolder object in a function allows the lock to be held
// throughout the scope of the function, that is, until just before
// the function returns.

class KeyHolder {
private:
  LockBase *lock;
  bool verbose;
public:
  KeyHolder(LockBase &other_lock, bool verbose=false);
  // KeyHolder(Lock&);
  ~KeyHolder();
};

// enableLocks and disableLocks override all instances of Lock and
// RWLock, but not SLock or SRWLock.  They're used to prevent
// deadlocks when running in unthreaded mode.

void enableLocks();
bool disableLocks();

#endif // LOCK_H
