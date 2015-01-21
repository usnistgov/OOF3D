// -*- C++ -*-
// $RCSfile: ooferror.h,v $
// $Revision: 1.16.2.4 $
// $Author: langer $
// $Date: 2013/08/22 19:50:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef OOFERROR_H
#define OOFERROR_H

#include <iostream>
#include <string>
#include <Python.h>

// Error namespace causes too many problems for SWIG.  Instead,
// use a customizing prefix for error names.

// Base class so that all OOF errors can be caught by the one catch
// statement typemap in oof.swg.  Also holds the One True Pythonizer
// for error classes.

class ErrError {
public:
  static PyObject *pyconverter;
  virtual ~ErrError() {}
  // These functions all return pointers to new string objects.  They
  // do this so that the strings may be handed off to Python via swig
  // without additional copying or memory leaks.
  virtual const std::string *summary() const = 0;
  virtual const std::string *details() const { return new std::string(""); }

  virtual const std::string pythonequiv() const = 0;
  virtual void throw_self() const = 0;
};


// Utility function to escape single-quotes (i.e. apostrophes) in a
// string.  Used to santize message strings in the various subclassses
// pythonequiv() methods, so that these don't generate syntax errors
// when the strings are eval'd by Python.
std::basic_string<char> escapostrophe(const std::string &in);

// ErrErrorBase exists just so that a base class pointer can re-throw
// itself.  It's used in pythonErrorRelay, when throwing a C++
// exception that was originally raised in Python.  The template
// trickery is necessary because it's not possible to throw an object
// of an abstract class (such as ErrError).  The template parameter
// must be the derived class.

template <class E>
class ErrErrorBase : public ErrError {
public:
  virtual void throw_self() const {
    const E *self = dynamic_cast<const E*>(this);
    throw *self;
  }
};

void pyErrorInit(PyObject*);


// Programming errors are fatal (to the program...)

template <class E>
class ErrProgrammingErrorBase : public ErrErrorBase<E> {
protected:
  const std::string file;
  const int line;
  const std::string msg;
public:
  ErrProgrammingErrorBase(const std::string &f, int l)
    : file(f), line(l), msg("")
  {}
  ErrProgrammingErrorBase(const std::string &m, const std::string &f, int l)
    : file(f), line(l), msg(m)
  {}
  virtual ~ErrProgrammingErrorBase() {}
  virtual const std::string *summary() const { return new std::string(msg); }
  // filename and lineno are for reading from Python
  const std::string &filename() const { return file; }
  int lineno() const { return line; }  
};

class ErrProgrammingError
  : public ErrProgrammingErrorBase<ErrProgrammingError>
{
public:
  ErrProgrammingError(const std::string &f, int l);
  ErrProgrammingError(const std::string &m, const std::string &f, int l);
  virtual const std::string pythonequiv() const;
};


// Resource shortages are probably fatal.

class ErrResourceShortage : public ErrErrorBase<ErrResourceShortage> {
private:
  const std::string msg;
public:
  ErrResourceShortage(const std::string &m) 
    : msg(m) 
  {}
  virtual ~ErrResourceShortage() {}
  virtual const std::string *summary() const { return new std::string(msg); }
  virtual const std::string pythonequiv() const;
};


class ErrBoundsError : public ErrErrorBase<ErrBoundsError> {
private:
  const std::string msg;
public:
  ErrBoundsError(const std::string &m) 
    : msg(m) 
  {}
  virtual ~ErrBoundsError() {}
  virtual const std::string *summary() const { return new std::string(msg); }
  virtual const std::string pythonequiv() const;
};


class ErrBadIndex : public ErrProgrammingErrorBase<ErrBadIndex> {
private:
  int badindex;
public:
  ErrBadIndex(int i, const std::string &f, int l)
    : ErrProgrammingErrorBase<ErrBadIndex>(f, l),
      badindex(i)
  {}
  virtual const std::string *summary() const;
  virtual const std::string pythonequiv() const;
};


// User errors shouldn't be fatal.

template <class E>
class ErrUserErrorBase : public ErrErrorBase<E> {
public:
  const std::string msg;
  ErrUserErrorBase(const std::string &m) : msg(m) {}
  virtual ~ErrUserErrorBase() {}
  virtual const std::string *summary() const { return new std::string(msg); }
  // pythonequiv must be defined in derived classes.
};

// Generic user error
class ErrUserError : public ErrUserErrorBase<ErrUserError> {
public:
  ErrUserError(const std::string &m) : ErrUserErrorBase<ErrUserError>(m) {}
  virtual const std::string pythonequiv() const;
};

class ErrSetupError : public ErrUserErrorBase<ErrSetupError> {
public:
  ErrSetupError(const std::string &m) : ErrUserErrorBase<ErrSetupError>(m) {}
  virtual const std::string pythonequiv() const;
};

class ErrInterrupted : public ErrUserErrorBase<ErrInterrupted> {
public:
  ErrInterrupted() : ErrUserErrorBase<ErrInterrupted>("Interrupted!") {}
  virtual const std::string pythonequiv() const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ErrNoProgress is used when building Progress objects.

class ErrNoProgress : public ErrErrorBase<ErrNoProgress> {
public:
  virtual const std::string pythonequiv() const { 
    return "ErrNoProgress()"; 
  }
  virtual const std::string *summary() const { return new std::string(""); }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ErrClickError : public ErrErrorBase<ErrClickError> {
public:
  virtual const std::string pythonequiv() const {
    return "ErrClickError()";
  }
  virtual const std::string *summary() const { return new std::string(""); }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Separate "stub" class for passing Python errors out through C++.
// This happens when a callback sets the Python error state, but 
// doesn't return to the Python environment.  The C++ caller should
// detect the error (by NULL return), and throw this exception,
// which will be caught in the exception typemap.

class PythonError {};

// pythonErrorRelay() should be called when C++ detects that a Python
// exception has been raised in a Python API call, if there's any
// chance that the exception might want to be handled in C++.  It
// converts the Python exception to a C++ exception (ie, an ErrError
// subclass) if possible.  Otherwise it just throws PythonError.

void pythonErrorRelay();

#endif	// OOFERROR_H
