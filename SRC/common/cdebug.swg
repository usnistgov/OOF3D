// -*- C++ -*-

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
#ifdef PROFILER
#include <gperftools/profiler.h>
#endif // PROFILER
%}
%pragma(python) include="cdebug.spy"

void setDebugMode(bool);

void initDebug(PyObject*);
void segfault(int);
void throwException();
void throwPythonException();
void throwPythonCException();

void openDebugFile(char*);
void writeDebugFile_(char*, char*, int);
void closeDebugFile();

void spinCycle(int);

#ifdef PROFILER
void ProfilerStart(char*);
void ProfilerStop();
#endif // PROFILER

#endif // CDEBUG_SWG
