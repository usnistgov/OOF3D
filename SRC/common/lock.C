// -*- C++ -*-
// $RCSfile: lock.C,v $
// $Revision: 1.21.2.8 $
// $Author: langer $
// $Date: 2014/05/08 14:38:52 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/oofcerr.h"
#include "common/lock.h"
#include "common/ooferror.h"
#include "common/threadstate.h"

#include <errno.h>
#include <iostream>

static bool enabled = true;

bool disableLocks() {
  bool oldval = enabled;
  enabled = false;
  return oldval;
}

void enableLocks() {
  enabled = true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

SLock::SLock() {
  // std::cerr << "SLock::ctor:";
  pthread_mutex_init(&lock, NULL);
#ifdef DEBUG
  verbose_ = false;
#endif // DEBUG
  // std::cerr << " done" << std::endl;
}

SLock::~SLock() {
  pthread_mutex_destroy(&lock);
#ifdef DEBUG
  if(verbose_)
    std::cerr << "SLock::dtor: " << this << " " << name << std::endl;
#endif // DEBUG
}

void SLock::acquire() {
#ifdef DEBUG
  if(verbose_)
    std::cerr << "SLock::acquire: " << this << " " << name 
	    << " waiting" << std::endl;
#endif // DEBUG
  pthread_mutex_lock(&lock);
#ifdef DEBUG
  if(verbose_)
    std::cerr << "SLock::acquire: " << this << " " << name
	    << " acquired" << std::endl;
#endif // DEBUG
}

void SLock::release() {
#ifdef DEBUG
  if(verbose_)
    std::cerr << "SLock::release: " << this << " " << name << " released"
	    << std::endl;
#endif // DEBUG
  pthread_mutex_unlock(&lock);
}

#ifdef DEBUG
void SLock::verbose(bool verb, const char *nm) {
  verbose_ = verb;
  name = nm;
  std::cerr << "SLock::verbose: " << this << " " << name << std::endl;
}
#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Lock::acquire() {
  if(enabled) {
    if(mainthread_query()) {
      std::cerr << "Lock::acquire called on main thread. " << this << std::endl;
      //abort();
      throw ErrProgrammingError("Lock error.", __FILE__, __LINE__);
    }
    SLock::acquire();
  }
}

void Lock::release() {
  if(enabled)
    SLock::release();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

UndebuggableLock::UndebuggableLock() {
  pthread_mutex_init(&lock, NULL);
}

UndebuggableLock::~UndebuggableLock() {
  pthread_mutex_destroy(&lock);
}

void UndebuggableLock::acquire() {
  pthread_mutex_lock(&lock);
}

void UndebuggableLock::release() {
  pthread_mutex_unlock(&lock);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// See
// https://computing.llnl.gov/tutorials/pthreads/#ConditionVariables
// for a good discussion of condition variables.  In particular:
// Proper locking and unlocking of the associated mutex variable is
// essential when using these routines. For example:
//  * Failing to lock the mutex before calling pthread_cond_wait() may
//    cause it NOT to block.
//  * Failing to unlock the mutex after calling pthread_cond_signal()
//    may not allow a matching pthread_cond_wait() routine to complete
//    (it will remain blocked).


Condition::Condition(SLock *lock)
  : lock(lock)
{
  if(enabled) {
    pthread_cond_init(&condition, NULL);
  }
#ifdef DEBUG
  verbose_ = false;
#endif // DEBUG
}

Condition::~Condition() {
  if(enabled)
    pthread_cond_destroy(&condition);
#ifdef DEBUG
  if(verbose_)
    std::cerr << "Condition::dtor: " << this << std::endl;
#endif // DEBUG
}

// Condition::wait() releases the lock and blocks the current thread
// until Condition::broadcast is called in some other thread.  Then it
// reacquires the lock and unblocks.

void Condition::wait() {
  if(enabled) {
#ifdef DEBUG
    if(verbose_)
      std::cerr << "Condition::wait: " << this << " waiting" << std::endl;
#endif // DEBUG
    pthread_cond_wait(&condition, &lock->lock);
#ifdef DEBUG
    if(verbose_)
      std::cerr << "Condition::wait: " << this << " done waiting" << std::endl;
#endif // DEBUG
  }
}

void Condition::broadcast() {
  if(enabled) {
#ifdef DEBUG
    if(verbose_)
      std::cerr << "Condition::broadcast: " << this << std::endl;
#endif // DEBUG
    pthread_cond_broadcast(&condition);
  }
}

void Condition::signal() {
  if(enabled) {
#ifdef DEBUG
    if(verbose_)
      std::cerr << "Condition::signal: " << this << std::endl;
#endif	// DEBUG
    pthread_cond_signal(&condition);
  }
}

#ifdef DEBUG
void Condition::verbose(bool verb, const std::string &nm) {
  std::cerr << "Condition::verbose: " << this << std::endl;
  verbose_ = verb;
  name = nm;
}
#endif // DEBUG

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

RWLock::RWLock()
  : r(0), w(0), p(0)
{
  if(enabled) {
    pthread_mutex_init(&local_lock, NULL);
    pthread_cond_init(&rw_zero, NULL);
  }
#ifdef DEBUG
  verbose_ = false;
#endif // DEBUG
}

RWLock::~RWLock() {
  if(enabled) {
    pthread_mutex_destroy(&local_lock);
    pthread_cond_destroy(&rw_zero);
  }
#ifdef DEBUG
  if(verbose_)
    std::cerr << "RWLock::dtor: " << this << std::endl;
#endif // DEBUG
}

#ifdef DEBUG
void RWLock::verbose(bool verb) {
  std::cerr << "RWLock::verbose: " << this << std::endl;
  verbose_ = verb;
}
#endif // DEBUG

// Before you can write, you have to wait until there are no 
// readers or writers.  
void RWLock::write_acquire() {
  if(enabled) {
    if(mainthread_query()) {
      std::cerr << "RWLock::write_acquire called on main thread." << std::endl;
      throw ErrProgrammingError("RWLock write error.", __FILE__, __LINE__);
    }
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::write_acquire: " << this << " waiting for local"
	      << std::endl;
#endif // DEBUG
    pthread_mutex_lock(&local_lock);
    while (r>0 || w>0 || p>0) {
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::write_acquire: " << this << " waiting on condition "
	      << "r=" << r << " w=" << w << " p=" << p << std::endl;
#endif // DEBUG
    pthread_cond_wait(&rw_zero, &local_lock);
    }
    w=1;
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::write_acquire: " << this << " releasing local"
	      << std::endl;
#endif // DEBUG
    pthread_mutex_unlock(&local_lock);
  }
}


void RWLock::write_release() {
  if(enabled) {
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::write_release: " << this << " waiting for local"
	      << std::endl;
#endif // DEBUG
    pthread_mutex_lock(&local_lock);
    w = 0;
    p = 0;
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::write_release: " << this << "broadcasting" 
	      << std::endl;
#endif // DEBUG
    pthread_cond_broadcast(&rw_zero);  // r==0 at this point.
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::write_acquire: " << this << " releasing local"
	      << std::endl;
#endif // DEBUG
    pthread_mutex_unlock(&local_lock);
  }
}


// You cannot read if anybody is writing.  Other readers are OK.
void RWLock::read_acquire() {
  if(enabled) {
    if(mainthread_query()) {
      std::cerr << "RWLock::read_acquire called on main thread." << std::endl;
      throw ErrProgrammingError("RWLock read error.", __FILE__, __LINE__);
    }
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::read_acquire: " << this << " waiting for local"
	      << std::endl;
#endif // DEBUG
    pthread_mutex_lock(&local_lock);
    while (w>0) {
#ifdef DEBUG
      if(verbose_)
	std::cerr << "RWLock::read_acquire: " << this << " waiting on condition "
		<< "w=" << w << std::endl;
#endif // DEBUG
      pthread_cond_wait(&rw_zero, &local_lock);
    }
    r++;
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::read_acquire: releasing local, r=" << r << std::endl;
#endif // DEBUG
    pthread_mutex_unlock(&local_lock);
  }
}

void RWLock::read_release() {
  if(enabled) {
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::read_release: " << this << " waiting for local"
	      << std::endl;
#endif // DEBUG
    pthread_mutex_lock(&local_lock);
    r--;
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::read_release: " << this << " r=" << r << std::endl;
#endif // DEBUG
    if (r==0) { // w==0 is already true here.
      assert(w == 0);
#ifdef DEBUG
      if(verbose_)
	std::cerr << "RWLock::read_release: " << this << " broadcasting"
		<< std::endl;
#endif // DEBUG
      pthread_cond_broadcast(&rw_zero);
    }
#ifdef DEBUG
    if(verbose_)
      std::cerr << "RWLock::read_release: " << this << " releasing local"
	      << std::endl;
#endif	// DEBUG
    pthread_mutex_unlock(&local_lock);
  }
}

void RWLock::write_pause() {
  if(enabled) {
    bool ok = true;
    pthread_mutex_lock(&local_lock);
    // It's an error to call write_pause when not writing, but an
    // exception can't be thrown until after local_lock has been
    // released, so the state is stored in 'ok'.
    ok = (w != 0);
    p = 1;
    w = 0;
    pthread_cond_broadcast(&rw_zero);
    pthread_mutex_unlock(&local_lock);
    if(!ok) {
      // throwing ErrProgrammingError here seems to be unreliable, so
      // we're using an assert statement as well.
      assert(ok);
      throw ErrProgrammingError("Called RWLock::write_pause() when not writing",
				__FILE__, __LINE__);
    }
  }
}

void RWLock::write_resume() {
  if(enabled) {
    pthread_mutex_lock(&local_lock);
    while (r>0) {
      // std::cerr << "***** Waiting in RWLock::write_resume" << std::endl;
      pthread_cond_wait(&rw_zero, &local_lock);
    }
    p = 0;
    w = 1;
    pthread_mutex_unlock(&local_lock);
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// // SRWLock functions -- same as RWLock except for error-checking.


// // Before you can write, you have to wait until there are no 
// // readers or writers.  
// void SRWLock::write_acquire() {
//   if(enabled) {
//     pthread_mutex_lock(&local_lock);
//     while (r>0 || w>0 || p>0) {
//       pthread_cond_wait(&rw_zero, &local_lock);
//     }
//     w=1;
//     pthread_mutex_unlock(&local_lock);
//   }
// }


// // You cannot read if anybody is writing.  Other readers are OK.
// void SRWLock::read_acquire() {
//   if(enabled) {
//     pthread_mutex_lock(&local_lock);
//     while (w>0) {
//       pthread_cond_wait(&rw_zero, &local_lock);
//     }
//     r++;
//     pthread_mutex_unlock(&local_lock);
//   }
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

KeyHolder::KeyHolder(LockBase &some_lock, bool verbose)
  : lock(&some_lock), verbose(verbose)
{
  // static long debugcount = 0;
  // if(verbose)
  //   std::cerr << "KeyHolder::ctor: waiting " << lock << " " << debugcount++ 
  // 	    << std::endl;
  lock->acquire();
  // if(verbose)
  //   std::cerr << "KeyHolder::ctor: released " << lock << std::endl;
}


KeyHolder::~KeyHolder() {
  lock->release();
  if(verbose)
    std::cerr << "KeyHolder::~KeyHolder: released " << lock << std::endl;
  
}
