// -*- C++ -*-
// $RCSfile: ooferror.swg,v $
// $Revision: 1.21.2.3 $
// $Author: langer $
// $Date: 2014/09/27 22:33:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef OOFERROR_SWG
#define OOFERROR_SWG

%module ooferror

%include "common/typemaps.swg"

%{
#include "common/ooferror.h"
%}

%pragma(python) include="ooferror.spy"

void pyErrorInit(PyObject *pythonCallable);

/* Swigged for automatic synchronization with C++ classes.
   The error-handling scheme involves error objects being created
   in the C++ code, then re-created from Python via the 
   string returned by the pythonequiv method, which must be a 
   call to the constructor in string form, with literal arguments,
   e.g. if the constructor takes a string and two integers, the
   pythonequiv string might look like: "MyError('Doom.', 13, 666)" */
/* NB the pythonequiv method only needs to be visible from C++. */
 

class ErrError {
public:
  %new string *summary();
  %new string *details();
};

// NOTE: inheritance layout here is different than ooferror.h. 

// Subclasses require individual __repr__s.  If you provide one in the
// base class but don't provide them in the subclasses, SWIG will
// construct default uninformative __repr__s for the subclasses.

/* Args are: Message, filename, line-number. */
class ErrProgrammingError : public ErrError {
public:
  const string &filename();
  int lineno();
  ErrProgrammingError(char *, char *, int);
  ~ErrProgrammingError();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};


class ErrResourceShortage : public ErrError {
public:
  ErrResourceShortage(char *m);
  ~ErrResourceShortage();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrBoundsError : public ErrError {
public:
  ErrBoundsError(char *m);
  ~ErrBoundsError();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};


class ErrBadIndex : public ErrError {
public:
  ErrBadIndex(int, char *, int);
  ~ErrBadIndex();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};


class ErrUserError : public ErrError {
public:
  ErrUserError(char *);
  ~ErrUserError();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrSetupError : public ErrError {
public:
  ErrSetupError(char * m);
  ~ErrSetupError();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrInterrupted : public ErrError {
public:
  ErrInterrupted();
  ~ErrInterrupted();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

class ErrNoProgress : public ErrError {
public:
  ErrNoProgress();
  ~ErrNoProgress();
  %addmethods {
    const string *__repr__() {
      static const std::string s("Progress object not found");
      return &s;
    }
  }
};

class ErrClickError : public ErrError {
public:
  ErrClickError();
  ~ErrClickError();
  %addmethods {
    %new const string *__repr__() {
      return self->summary();
    }
  }
};

#endif // OOFERROR_SWG
