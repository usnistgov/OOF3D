// -*- C++ -*-
// $RCSfile: cdebug.C,v $
// $Revision: 1.21.2.6 $
// $Author: langer $
// $Date: 2013/02/12 19:02:37 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// Routines used to catch C++ signals and dump the current Python
// stack before bailing out.

#include "common/IO/oofcerr.h"
#include "common/cdebug.h"
#include "common/ooferror.h"
#include "common/pythonlock.h"

#include <fstream>
#include <iostream>
#include <pthread.h>
#include <signal.h>
#include <string>
#include <unistd.h>

static PyObject *python_dumper;

static void handler(int sig) {
  std::string msg;
  if(sig == SIGBUS)
    msg = "Bus Error";
  else if(sig == SIGSEGV)
    msg = "Segmentation Fault";
  else if(sig == SIGINT)
    msg = "Interrupted";
  
  PyGILState_STATE pystate = acquirePyLock();
  PyObject *args = Py_BuildValue("(s)", msg.c_str());
  PyObject *result = PyEval_CallObject(python_dumper, args);
  Py_DECREF(args);
  Py_DECREF(result);
  releasePyLock(pystate);
  oofcerr << "cdebug.C: " << msg << ": aborting" << std::endl;
  abort();
}

void initDebug(PyObject *pydump) {
  python_dumper = pydump;
  Py_XINCREF(python_dumper);
}

// installSignals and restoreSignals are called by the 'except'
// directive in typemaps.swg.

typedef void (*sighandler)(int);

// Signal handlers called due to internal segfaults (i.e. actual
// pointer-dereference problems, as opposed to "kill -11" from the
// command line) appear to be run on the segfaulting thread, resulting
// in the stack dump being correct.

// Experiments with test programs imply that successive "signal" calls
// override the main handler.  Since we actually only have one
// handler, and we want it to be in place whenever any thread is in
// C++ code, the right thing to do is to count up the handlers in a
// thread-safe way, and not restore until you're all the way out.

sighandler bushandler;
sighandler inthandler;
sighandler segvhandler;

static pthread_mutex_t signal_handler_count_lock=PTHREAD_MUTEX_INITIALIZER;
static int signal_handler_count=0;

void installSignals_() {
  pthread_mutex_lock(&signal_handler_count_lock);
  if (signal_handler_count==0) {
    bushandler = signal(SIGBUS, handler);
    inthandler = signal(SIGINT, handler);
    segvhandler = signal(SIGSEGV, handler);
  }
  signal_handler_count++;
  pthread_mutex_unlock(&signal_handler_count_lock);
}

void restoreSignals_() {
  pthread_mutex_lock(&signal_handler_count_lock);
  signal_handler_count--;
  if (signal_handler_count==0) {
    signal(SIGBUS, bushandler);
    signal(SIGINT, inthandler);
    signal(SIGSEGV, segvhandler);
  }
  pthread_mutex_unlock(&signal_handler_count_lock);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// The following functions are for testing the error handling
// facilities.  

void segfault(int delay) {
  // raise(SIGSEGV);
  sleep(delay);
  void (*f)() = 0;
  f();
}

void throwException() {
  throw ErrProgrammingError("Somebody made a mistake!", __FILE__, __LINE__);
}

// A C++ function that can be called from Python, and which calls a
// Python "function" that raises a Python exception.

void throwPythonException() {
  PyGILState_STATE pystate = acquirePyLock();
  try {
    PyObject *result = PyObject_GetAttrString(Py_None, "say what?");
    if(!result)
      pythonErrorRelay();
    Py_XDECREF(result);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

// A C++ function that can be called from Python, and which calls a
// Python function that throws a C++ exception.

void throwPythonCException() {
  PyGILState_STATE pystate = acquirePyLock();
  try {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.common.cdebug");
    PyObject *func = PyObject_GetAttrString(module, "throwException");
    Py_XDECREF(module);
    PyObject *args = Py_BuildValue("()");
    PyObject *result = PyEval_CallObject(func, args);
    Py_XDECREF(args);
    if(!result)
      pythonErrorRelay();
    Py_XDECREF(result);
  }
  catch (...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#include "common/lock.h"
#include <iostream>

static std::ofstream *debugfile = 0;
static SLock debugfilelock;
static bool lastNL;		// did the last line end with a new line?

void openDebugFile_(const std::string &filename) {
  debugfilelock.acquire();
  if(debugfile)
    debugfile->close();
  debugfile = new std::ofstream(filename.c_str());
  std::cerr << "************ Opening debug file " << filename << " ************"
	    << std::endl;
  lastNL = true;
  debugfilelock.release();
}

void writeDebugFile_(const std::string &message, const std::string &filename,
		     int lineno)
{
  debugfilelock.acquire();
  if(debugfile) {
    if(lastNL)
      *debugfile << filename << "(" << lineno << "):\t ";
    *debugfile << message;
    debugfile->flush();
    lastNL = (message[message.size()-1] == '\n');
  }
  debugfilelock.release();
}

void closeDebugFile_() {
  debugfilelock.acquire();
  if(debugfile) {
    debugfile->close();
    debugfile = 0;
  }
  debugfilelock.release();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// For testing progress bars

#include <math.h>
#include "common/tostring.h"
#include "common/progress.h"

void spinCycle(int nCycles) {
  DefiniteProgress *progress = dynamic_cast<DefiniteProgress*>(
				       getProgress("SpinCycle", DEFINITE));

  double x;
  for(int i=0; i<nCycles && !progress->stopped(); i++) {
    x = cos(x);
    progress->setMessage(to_string(i) + "/" + to_string(nCycles));
    progress->setFraction((float) i/nCycles);
  }
  progress->finish();
}
