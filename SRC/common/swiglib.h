// -*- C++ -*-
// $RCSfile: swiglib.h,v $
// $Revision: 1.4.18.3 $
// $Author: langer $
// $Date: 2014/09/27 22:33:56 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


// We define our own copies of the SWIG library functions to work
// around differences between SWIG versions.

#include <oofconfig.h>

#include <Python.h>

extern "C" {
  extern void SWIG_MakePtr(char *, void *, const char *);
  extern void SWIG_RegisterMapping(const char *, const char *,
				   void *(*)(void *));
  extern const char *SWIG_GetPtr(const char *, void **, const char *);
  extern const char *SWIG_GetPtrObj(PyObject *, void **, const char *);
  extern void SWIG_addvarlink(PyObject *, const char *, PyObject *(*)(void),
			      int (*)(PyObject *));
  extern PyObject *SWIG_newvarlink(void);
}
