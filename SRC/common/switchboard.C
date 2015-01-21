// -*- C++ -*-
// $RCSfile: switchboard.C,v $
// $Revision: 1.23.2.1 $
// $Author: vrc $
// $Date: 2011/04/08 23:02:55 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <string>

#include "switchboard.h"
#include "ooferror.h"
#include "trace.h"
#include "common/pythonlock.h"

static PyObject *notifier = 0;

void init_switchboard_api(PyObject *pyNotify) {
  // Called just once, passing switchboard.cnotify.
  PyGILState_STATE pystate = acquirePyLock();
  Py_XINCREF(pyNotify);
  releasePyLock(pystate);
  notifier = pyNotify;
}

void switchboard_notify(const std::string &msg) {
  if(notifier != 0) {
    PyGILState_STATE pystate = acquirePyLock();
    PyObject *arg = Py_BuildValue((char*) "(s)", msg.c_str());
    PyObject *result = PyObject_CallObject(notifier, arg);
    if(!result) {
      releasePyLock(pystate);
      pythonErrorRelay();
    }
    Py_XDECREF(arg);
    Py_XDECREF(result);
    releasePyLock(pystate);
    /*
      READ THIS: There is a risk that Acquire/Release locks the main
      thread if this switchboard_notify attempts to execute a callback
      in this child thread (the calling thread), if the callback takes
      a significant amount of time.
    */
    // I think that the above comment is misleading.  The GUI can
    // appear to be stalled while some switchboard callback is
    // executing.  This isn't the same thing as being
    // deadlocked. --SAL
  }
}

void switchboard_notify(const OOFMessage &msg) {
  if(notifier != 0) {
    PyObject *pmsg = msg.pythonObject();
    PyGILState_STATE pystate = acquirePyLock();
    PyObject *result = PyObject_CallFunction(notifier, (char*) "O", pmsg);
    if(!result) {
      releasePyLock(pystate);
      pythonErrorRelay();
    }
    Py_XDECREF(pmsg);
    Py_XDECREF(result);
    releasePyLock(pystate);
  
    /*
      READ ABOVE.
    */
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string OOFMessage::classname_("OOFMessage");
const std::string OOFMessage::modulename_("ooflib.SWIG.common.switchboard");

OOFMessage::OOFMessage(const std::string &msgname)
  : msgname(msgname)
{
}

const std::string &OOFMessage::name() const { return msgname; }

void OOFMessage::addarg(const PythonExportableBase &arggh) {
  args.push_back(arggh.pythonObject());
}

void OOFMessage::addarg(const std::string &strng) {
  args.push_back(PyString_FromString(strng.c_str()));
}

void OOFMessage::addarg(int val) {
  args.push_back(PyLong_FromLong(val));
}

int OOFMessage::nargs() const {
  return args.size();
}

PyObject *OOFMessage::getarg(int i) const {
  return args[i];
}
