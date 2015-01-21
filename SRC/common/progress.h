// -*- C++ -*-
// $RCSfile: progress.h,v $
// $Revision: 1.2.2.4 $
// $Author: langer $
// $Date: 2013/02/07 20:03:15 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PROGRESS_H
#define PROGRESS_H

// Progress objects keep track of a task's progress toward its goal
// (DefiniteProgress subclass) or just that it's still active
// (IndefiniteProgress subclass).  They're created by
// ThreadState.getProgress() and deleted when the ThreadState is
// destroyed.  Progress objects are lightweight so that running
// processes don't have to do much work to maintain them, even inside
// inner loops.  UI elements that display progress (ProgressBars) can
// do more work because they're not called frequently.

#include "common/pythonexportable.h"
#include "common/lock.h"

class ThreadState;

#include <string>
#include <vector>

class Progress : public PythonExportable<Progress> {
 private:
  const std::string name_;
  std::string message_; 
  bool stopped_;
  bool finished_;
  ThreadState *threadstate;
  static const std::string modulename_;
  PyObject *progressbar;
  // Progress objects need to have __eq__ and __hash__ methods in
  // Python that will work on ProgressPtrs.  Since swig returns a
  // different ProgressPtr each time, __eq__ and __hash__ use a unique
  // id() instead.  id_ is not const, because it must be set in the
  // body of the constructor, after idlock is acquired.
  int id_;
  static int idcounter;
  static SLock idlock;
protected:
  // started_ indicates that the progress object is actually being
  // used.  It's set to true when the message is changed or progress
  // has been recorded.
  bool started_;
  // The lock is mutable so that const functions can acquire it to
  // ensure they're computing their output safely.
  mutable SLock msglock;   // lock for reading or writing message_.
  SLock flaglock;	   // separate lock for started_ and stopped_.
  // start() is called once something interesting starts to happen.
  // It sends the "new progress" signal that causes progress bars to
  // be built in the GUI.
  void start();
public:
  Progress(const std::string&, ThreadState*);
  virtual ~Progress();
  int id() const { return id_; }

  bool started() const { return started_; }
  // The difference between stop() and finish() is that finish() is
  // called by the thread whose progress is being monitored to
  // indicate that its task is complete, and stop() is called by an
  // external thread to indicate that the thread should stop work on
  // the task prematurely.
  void finish();
  void stop();	// stops this and other Progress objects on the thread
  void stop1();			// stops just this Progress object
  // stopped() and finished() indicate whether stop() or finish() has
  // been called.  stopped() should be used within the thread to
  // decide whether or not to abort, and finished() should be called
  // from outside the thread to find out if the task is still running.
  // Note that determining if the *thread* is still running should be
  // done by querying the Worker or ThreadState, not the Progress
  // object(s)!
  bool stopped() const { return stopped_; } 
  bool finished() const { return finished_; }
  void setMessage(const std::string&);
  virtual void setFraction(double) = 0;
  const std::string &name() const { return name_; }
  const std::string *message() const;
  virtual const std::string &modulename() const { return modulename_; }
  void setProgressBar(PyObject*);
  bool hasProgressBar() const;

  void acquireThreadLock();
  void releaseThreadLock();

  // Hook for disconnecting a GUI progress bar.  If the GUI isn't
  // loaded, the function pointer is null.
  static void (*disconnect_hook)(PyObject*);

  // disconnectBar is public so that it can be swigged.  It's used by
  // progressbarGUI.py.
  void disconnectBar(PyObject*);
};

enum ProgressType {
  DEFINITE,			// degree of completion is measurable
  LOGDEFINITE,			// completion measured logarithmically
  INDEFINITE			// completion can not be computed ahead of time
};

class DefiniteProgress : public Progress {
private:
  static const std::string classname_;
protected:
  double fraction_;
public:
  DefiniteProgress(const std::string&, ThreadState*);
  virtual ~DefiniteProgress();
  virtual const std::string &classname() const { return classname_; }
  virtual void setFraction(double x);
  double getFraction() const; 
};

// LogDefiniteProgress is used, for example, when a residual is
// converging towards a tolerance.  It requires two parameters to be
// set by the setRange function: the initial value of the residual and
// the target value.  The initial value must be greater than the
// target.  The bar size is 0.0 when the residual is at the initial
// value or above, and 1.0 when it's at the target or below.  The
// logarithm magnifies the intervals near the target.

class LogDefiniteProgress : public DefiniteProgress {
private:
  double initialValue;
  double targetValue;
  double log_init_over_targ;
  static const std::string classname_;
public:
  LogDefiniteProgress(const std::string &, ThreadState*);
  virtual const std::string &classname() const { return classname_; }
  void setRange(double initial, double target);
  virtual void setFraction(double);
};

class IndefiniteProgress : public Progress {
private:
  unsigned long count_;
  static const std::string classname_;
public:
  IndefiniteProgress(const std::string&, ThreadState*);
  virtual ~IndefiniteProgress();
  virtual const std::string &classname() const { return classname_; }
  // The backend should call pulse() to indicate that it's still alive
  // and kicking.
  void pulse();
  // Sometimes the backend doesn't know if the progress bar is
  // Definite or Indefinite.  In that case it should call
  // setFraction().  If the bar is Indefinite, the fraction is
  // ignored.
  virtual void setFraction(double) { pulse(); }
  // The frontend knows that the backend is still alive if two calls
  // to pulsecount() return different answers.
  unsigned long pulsecount() const;
};

Progress *getProgress(const std::string &name, ProgressType);
Progress *findProgress(const std::string &name);
Progress *findProgressByID(int);

#endif // PROGRESS_H
