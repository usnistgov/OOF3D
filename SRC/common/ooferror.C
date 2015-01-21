// -*- C++ -*-
// $RCSfile: ooferror.C,v $
// $Revision: 1.23.2.2 $
// $Author: langer $
// $Date: 2012/03/13 15:01:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <iostream>
#include "common/ooferror.h"
#include "common/pythonlock.h"
#include "common/swiglib.h"
#include "common/tostring.h"


// Some trivial constructors are here instead of in ooferror.h so that
// debugging lines can be added without recompiling everything else.

ErrProgrammingError::ErrProgrammingError(const std::string &f, int l)
  : ErrProgrammingErrorBase<ErrProgrammingError>(f, l)
{}

ErrProgrammingError::ErrProgrammingError(const std::string &m,
					 const std::string &f, int l)
  : ErrProgrammingErrorBase<ErrProgrammingError>(m, f, l)
{}

const std::string *ErrBadIndex::summary() const {
  const std::string *sum = ErrProgrammingErrorBase<ErrBadIndex>::summary();
  const std::string *equiv = new std::string(*sum  + " Bad Index: "
					     + to_string(badindex));
  delete sum;
  return equiv;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Python equivalents 

// Makes the most general assumption about the structure.
const std::string ErrProgrammingError::pythonequiv() const {
  return "ErrProgrammingError('" +
    escapostrophe(msg) + "', '" + file + "', " +
    to_string(line) + ")";
}

const std::string ErrResourceShortage::pythonequiv() const {
  return "ErrResourceShortage('" + escapostrophe(msg) + "')";
}


const std::string ErrBoundsError::pythonequiv() const {
  return "ErrBoundsError('" + escapostrophe(msg) + "')";
}


const std::string ErrBadIndex::pythonequiv() const {
  const std::string *sum = ErrProgrammingErrorBase<ErrBadIndex>::summary();
  const std::string equiv = "ErrBadIndex('" + *sum + "')";
  delete sum;
  return equiv;
}

const std::string ErrUserError::pythonequiv() const {
  return "ErrUserError('" + escapostrophe(msg) + "')";
}

const std::string ErrSetupError::pythonequiv() const {
  return "ErrSetupError('" + escapostrophe(msg) + "')";
}

const std::string ErrInterrupted::pythonequiv() const {
  return "ErrInterrupted()";
}


// Use basic_string functionality, to be all properly C++y, and
// hopefully ensure that the functionality is robustly retained when
// we switch over to Unicode.
std::basic_string<char> escapostrophe(const std::string &in) {
  // Make sure to work on a copy.
  std::basic_string<char> out(in);

  std::basic_string<char>::size_type p = out.find("'",0);
  while(p!=std::basic_string<char>::npos) {
    out.replace(p,1,"\\'");
    p = out.find("'",p+2);
  }
  return out;
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Function to convert a Python exception into a C++ exception.  This
// in effect is the inverse of the swig exception typemap.  The two of
// them together allow an exception to be batted back and forth
// between C++ and Python until somebody decides to catch it.

// pythonErrorRelay() should be called whenever C++ detects that a
// Python exception has been raised in a Python API call.  It converts
// the Python exception to a C++ exception if possible (ie, when the
// Python exception is really a swigged C++ ErrError subclass).
// Otherwise it just throws PythonError, which is caught by the swig
// exception typemap.

void pythonErrorRelay() {
  PyGILState_STATE pystate = acquirePyLock();
  try {
    PyObject *ptype;
    PyObject *pvalue;
    PyObject *ptraceback;
    // PyErr_Fetch returns new references to its arguments.  It also
    // clears the Python error state.
    PyErr_Fetch(&ptype, &pvalue, &ptraceback);
    if(ptype) {
      // Get the swigged ErrError class, so that we can compare error
      // types on the Python side.
      static PyObject *pyErrError = 0;
      if(!pyErrError) {
	PyObject *module = PyImport_ImportModule((char*) 
						 "ooflib.SWIG.common.ooferror");
	pyErrError = PyObject_GetAttrString(module, (char*) "ErrErrorPtr");
	Py_XDECREF(module);
      }
      if(PyErr_GivenExceptionMatches(ptype, pyErrError)) {
	// The Python exception is a swigged ErrError -- ie, it's one of
	// ours.  Extract the C++ object and raise it as a new
	// exception.
	const ErrError *ee;
	SWIG_GetPtrObj(pvalue, (void**) &ee, "_ErrError_p");
	Py_XDECREF(ptraceback);
	Py_XDECREF(ptype);
	// Don't decref pvalue! It will destroy *ee.
	ee->throw_self();
      }
      else {
	// The error is a native Python exception.  Since PyErr_Fetch
	// cleared the error state, we have to call PyErr_Restore.
	// The error will be caught again when C++ returns to Python,
	// at which point the swig exception typemap will handle it.
	// PyErr_Restore steals references to its arguments, so we
	// don't have to decref here.

	// Mysterious crashes are sometimes due to python errors that
	// don't propagate properly, perhaps because they're occuring
	// within the thread handling machinery.  Uncommenting these
	// lines can help to debug them:
	// std::cerr << "pythonErrorRelay: " <<
	//   PyString_AsString(PyObject_Repr(ptype)) << std::endl;
	// std::cerr << "pythonErrorRelay: " <<
	//   PyString_AsString(PyObject_Repr(pvalue)) << std::endl;

	PyErr_Restore(ptype, pvalue, ptraceback);

	throw PythonError();
      }
    } // end if ptype
  }
  catch (...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// This isn't the real initialization for pyconverter, this is just
// here to make the linker happy.  The real initialization happens in
// the function below at import time.
PyObject *ErrError::pyconverter(0);

// Initializes the static pyconverter member of the ErrError base
// class -- called from the SWIG'd Python file at ooferror import
// time.  Errors which occur prior to this import will not be handled
// correctly.
void pyErrorInit(PyObject *converter) {
  Py_XINCREF(converter);
  ErrError::pyconverter = converter;
}


