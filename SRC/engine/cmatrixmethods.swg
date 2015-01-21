// -*- C++ -*-
// $RCSfile: cmatrixmethods.swg,v $
// $Revision: 1.2.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CMATRIXMETHODS_SWG
#define CMATRIXMETHODS_SWG

%module cmatrixmethods
%include "engine/typemaps.swg"

%{
#include "engine/cmatrixmethods.h"
#include "common/doublevec.h"
%}

%typemap(python, argout) int INOUT {
  // typemap(python, argout) int INOUT
  if(!$target || $target == Py_None) {
    $target = PyList_New(0);
  }
  PyList_Append($target, PyInt_FromLong($source));
 }

%typemap(python, argout) double INOUT {
  // typemap(python, argout) double INOUT
  if(!$target || $target == Py_None) {
    $target = PyList_New(0);
  }
  PyList_Append($target, PyFloat_FromDouble($source));
 }

void solveCG(const SparseMat&, const DoubleVec&,
	    const PreconditionerBase&, int INOUT, double INOUT, DoubleVec&);

void solveBiCG(const SparseMat&, const DoubleVec&,
	      const PreconditionerBase&, int INOUT, double INOUT, DoubleVec&);

void solveBiCGStab(const SparseMat&, const DoubleVec&,
		  const PreconditionerBase&, int INOUT, double INOUT,
		   DoubleVec&);

void solveGMRes(const SparseMat&, const DoubleVec&,
	       const PreconditionerBase&, int INOUT, int, double INOUT,
		DoubleVec&);

void solveDirect(const SparseMat&, const DoubleVec &rhs, DoubleVec &x);

%typemap(python, argout) int INOUT {}
%typemap(python, argout) double INOUT {}

#endif
