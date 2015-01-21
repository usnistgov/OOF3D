// -*- C++ -*-
// $RCSfile: cdebug.h,v $
// $Revision: 1.10.18.5 $
// $Author: langer $
// $Date: 2013/02/12 19:02:38 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CDEBUG_H
#define CDEBUG_H

// Routines used to catch C++ signals and dump the current Python
// stack before bailing out.

#include <string>
#include <vector>

void initDebug(PyObject*);
void installSignals_();
void restoreSignals_();

void segfault(int delay);
void throwException();
void throwPythonException();
void throwPythonCException();

#ifdef DEBUG
#define installSignals installSignals_()
#define restoreSignals restoreSignals_()
#else
#define installSignals /**/
#define restoreSignals /**/
#endif // DEBUG

void openDebugFile_(const std::string&);
void writeDebugFile_(const std::string&, const std::string&, int);
void closeDebugFile_();
#ifdef DEBUG
#define openDebugFile(name) openDebugFile_(name)
#define writeDebugFile(strng) writeDebugFile_(strng, __FILE__, __LINE__)
#define closeDebugFile() closeDebugFile_()
#else
#define openDebugFile(name) /**/
#define writeDebugFile(strng) /**/
#define closeDebugFile() /**/
#endif // DEBUG

void spinCycle(int);

#endif // CDEBUG_H
