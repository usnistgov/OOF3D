// -*- C++ -*-
// $RCSfile: cdebug.swg,v $
// $Revision: 1.9.18.3 $
// $Author: langer $
// $Date: 2013/02/12 19:02:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CDEBUG_SWG
#define CDEBUG_SWG

%module cdebug

%include "common/typemaps.swg"

%{
#include "common/cdebug.h"
  void segfault();
%}
%pragma(python) include="cdebug.spy"

void initDebug(PyObject*);
void segfault(int);
void throwException();
void throwPythonException();
void throwPythonCException();

void openDebugFile(char*);
void writeDebugFile_(char*, char*, int);
void closeDebugFile();

void spinCycle(int);

#endif // CDEBUG_SWG
