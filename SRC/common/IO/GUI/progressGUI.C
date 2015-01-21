// -*- C++ -*-
// $RCSfile: progressGUI.C,v $
// $Revision: 1.8.2.2 $
// $Author: langer $
// $Date: 2013/01/28 16:58:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/lock.h"
#include "common/ooferror.h"
#include "common/progress.h"
#include "common/pythonlock.h"
#include "common/threadstate.h"

#include <glib.h>
#include <gdk/gdk.h>

// The code in this file allows a C++ Progress object to disconnect
// from its Python/gtk GUIProgressBar safely.  This is done when a
// subthread calls Progress.finish().  Progress.finish() is
// necessarily called on a subthread, but the gtk calls in
// GUIProgressBar.disconnect() have to be performed on the main
// thread.  The old way of doing this was for Progress.finish() to
// call a Python function (A) which called another Python function (B)
// on the main thread.  The trouble with that was that after B
// finished, the GUIProgressBar had no references, and was garbage
// collected in A.  Since the GUIProgressBar has gtk components and A
// was running on the subthread, gtk calls were made on the subthread
// during garbage collection, leading to X11 synchronization errors.
// The code here provides a way for the C++ Progress object on the
// subthread to call B on the main thread directly, without an
// intervening subthread Python function.  That ensures (?) that the
// destruction of the GUIProgressBar's gtk widgets doesn't occur on
// the subthread.

// Because the Progress object is in common, it can't make any gtk
// calls directly.  Instead, the Progress class has a callback hook
// which is set by the initialize() function in this file (which is
// called by the GUI initialization code).  The callback function
// (disconnectPBar(), below) installs idleCallback() as an idle
// callback in the gtk main loop, then blocks and waits for
// pyDisconnect() to finish.

static void pyDisconnect(PyObject *progressbar) {
  PyGILState_STATE gilstate = acquirePyLock();
  try {
    PyObject *result = PyObject_CallMethod(progressbar, (char*)"disconnect", 0);
    if(!result) {
      pythonErrorRelay();
    }
    // This Py_XDECREF matches the Py_XINCREF in
    // Progress::setProgressBar().
    Py_XDECREF(progressbar);
  }
  catch (...) {
    releasePyLock(gilstate);
    throw;
  }
  releasePyLock(gilstate);
}


// PBarData wraps a GUIProgressBar and a mutex so that they can be
// passed to the gtk idle callback together.
class PBarData {
public:
  PyObject *progressbar;
  // We have to use a condition instead of a simple mutex because the
  // mutex would have to be acquired on one thread and released on
  // another, which is illegal.
  SLock lock;
  Condition condition; 
  PBarData(PyObject *p)
    : progressbar(p),
      condition(&lock)
  {
    lock.acquire();
  }
  ~PBarData() {
    lock.release();
  }
};

static gboolean idleCallback(void *data) {
  PBarData *pbd = (PBarData*) data;
  gdk_threads_enter();
  pbd->lock.acquire();
  try {
    pyDisconnect(pbd->progressbar);
  }
  catch (...) {
    gdk_threads_leave();
    pbd->condition.signal();
    pbd->lock.release();
    throw;
  }
  gdk_threads_leave();
  pbd->condition.signal();	// unblock the calling thread
  pbd->lock.release();
  return false;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// disconnectPBar is the disconnect_hook function called by
// Progress::disconnectBar().

static void disconnectPBar(PyObject *progressbar) {
  // If we're on the main thread already, just call the Python
  // disconnect function directly.  We can't use the idle callback
  // mechanism because it will deadlock.
  assert(progressbar != 0);
  if(mainthread_query()) {
    pyDisconnect(progressbar);
  }
  else {
    // Install a gtk idle callback for progressbar.disconnect.
    PBarData pbd(progressbar);
    g_idle_add(idleCallback, (void*) &pbd);
    // Block and wait for pyDisconnect to finish.
    pbd.condition.wait();
  }
}

void initialize() {
  Progress::disconnect_hook = disconnectPBar;
}
