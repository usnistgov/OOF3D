// -*- C++ -*-
// $RCSfile: switchboard.swg,v $
// $Revision: 1.9.2.1 $
// $Author: langer $
// $Date: 2012/03/13 15:01:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef SWITCHBOARD_SWG
#define SWITCHBOARD_SWG

%module switchboard

%{
#include "common/switchboard.h"
#include "common/pythonlock.h"
%}

%pragma(python) include="switchboard.spy"

%include "common/typemaps.swg"


void init_switchboard_api(PyObject *pythonCallable); // call this once


%typemap(python, out) PyObject* {
  $target = $source;
};

class OOFMessage {
public:
  const string &name();
   %addmethods {
     int __len__() const {
       return self->nargs();
     }
     PyObject *__getitem__(int which) const {
       if(which >= self->nargs() || which < 0) {
	 PyGILState_STATE pystate = acquirePyLock();
	 PyErr_SetString(PyExc_IndexError,
 			"Not that many arguments in OOFMessage");
	 releasePyLock(pystate);
 	return 0;
       }
       return self->getarg(which);
     }
   }
};

%typemap(python, out) PyObject*;

#endif // SWITCHBOARD_SWG
