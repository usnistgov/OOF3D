// -*- C++ -*-
// $RCSfile: pythonexportable.h,v $
// $Revision: 1.37.2.3 $
// $Author: langer $
// $Date: 2013/08/22 19:50:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PYTHONEXPORTABLE_H
#define PYTHONEXPORTABLE_H

// The PythonExportable base class is used to convert base class
// pointers exported to Python via SWIG into their derived class
// Python objects.  For example, suppose you have a C++ class
// hierarchy with a base class B and derived classes D1 and D2, all of
// which are swigged.  If you have a function B* f() that returns a
// pointer to an instance of D1 or D2, the SWIG generated Python code
// won't give you access to the derived parts of D1 and D2.  The
// swigged f() will return a Python B.  This is consistent with the
// way C++ does things---using a B* only gives you access to those
// parts of D1 and D2 that are declared in the base class---but it's
// inconsistent with Python's approach, in which there's no such thing
// as a base class pointer---all components of all objects are always
// accessible, if you know they're there. (For example, you might have
// created a SWIGged derived class object in Python, stored in a C++
// list of base class objects, and then retrieved it from that list in
// Python.  You'd expect to have all of the derived class functions
// available.)  The PythonExportable class remedies this
// inconsistency, allowing C++ functions to have polymorphic Python
// return types.

// To use this class, you need to do two things:

// 1) Derive a C++ class heirarchy from the templated base class
//    PythonExportable.  The template parameter must be the name of
//    the class derived from PythonExportable.  Each derived type must
//    supply a classname() virtual function that returns the name of
//    the derived class.  If the C++ derived classes will be swigged
//    and used as base classes for Python classes, then the
//    PythonExportable must be a *virtual* base class (see PythonNative,
//    below).
//
//    For example:
//      class MyExportable : public PythonExportable<MyExportable> { ... }
//      class Oil : public MyExportable {
//      public:
//         virtual const std::string &classname() const { return "Oil"; }
//      }
//      class Cheese : public MyExportable {
//      public:
//         virtual const std::string &classname() const { return "Cheese"; }
//      }

// 2) In every swig file containing a function that returns a base
//    class pointer ("MyExportable*" in the example above), include
//    the following typemap:
//    %typemap(python, out) BASECLASS* {
//      $target = $source->pythonObject();
//    }
//    where BASECLASS is the base class of the heirarchy derived
//    from PythonExportable.  This typemap changes the return type to
//    a tuple containing the Python name of the derived class (classnamePtr)
//    and the encoded address of the C++ object.

// If the C++ class heirarchy derived from PythonExportable is
// swigged, and the swigged Python classes are extended by Python
// inheritance, then the above mechanism doesn't quite work.  The
// class which is to be used as a base class for the Python
// inheritance must be derived from PythonExportable and *also*
// PythonNative.  PythonNative is a template, and must have the same
// template parameter as PythonExportable. 

// For example, if Cheese is swigged and extended in Python,
// then it needs to have been defined like this in C++:
//    class Cheese
//       : public MyExportable, virtual public PythonNative<MyExportable>
//    { ... }
// with a constructor that passes the Python object pointer to PythonNative:
//    Cheese::Cheese(PyObject *self) : PythonNative(self) { ... }
// and a Python constructor for the derived class that also passes the pointer:
// class Cheddar(Cheese):
//    def __init__(self):
//         [cheddar specific stuff]
//         Cheese.__init__(self, self)
// The second "self" in the line above is the "PyObject *self" in the C++
// Cheese constructor.

// If you use PythonNative, then PythonExportable must be a virtual base class:
//    class MyExportable : virtual public PythonExportable<MyExportable> { ... }
// It is legal to use PythonExportable as a virtual base class even if
// you don't use PythonNative, but there may be a small performance
// penalty.

#include <Python.h>
#include <string>
#include <iostream>
#include <stdexcept>

#include "common/ooferror.h"
#include "common/pythonlock.h"
#include "common/swiglib.h"
#include "common/trace.h"

class PythonExportableBase {
public:
  virtual PyObject *pythonObject() const = 0; 
  virtual ~PythonExportableBase() {}
};

template <class TYPE>
class PythonExportable : public PythonExportableBase {
public:
  virtual ~PythonExportable() {}

  // classname() must return the name of the *derived* class. 
  virtual const std::string &classname() const = 0;
  virtual const std::string &modulename() const = 0;

  virtual PyObject *pythonObject() const  {
    // For a class named "TYPE", SWIG creates a Python object by
    // passing the string "_TYPE_p" to SWIG_MakePtr, to create a
    // string representation of the pointer to the object.  Then it
    // passes that string to the Python function TYPEPtr, to create an
    // instance of the Ptr version of the Python shadow class.  Here,
    // we do the same thing, but we use the virtual C++ classname()
    // function to get the name of the derived class, and use that
    // instead.

    PyGILState_STATE pystate = acquirePyLock();
    try {
      // SWIG's string representation of pointer to object
      char swigaddr[128];
      std::string clsnm = std::string("_") + classname() + std::string("_p");
      char *cls = const_cast<char*>(clsnm.c_str());

      // Because C++ classes use PythonExportable as a *virtual* base
      // class, the value of "this" in this function is not necessarily
      // the same as the address of the TYPE object.  Swig needs to know
      // the derived class's address, so here we cast "this" to a
      // pointer to the derived type.
      const TYPE *derived_addr = dynamic_cast<const TYPE*>(this);

      if (derived_addr==0) {
	// The dynamic cast can fail, and when it does, a coherent
	// exception is hard to throw -- this code is inside a
	// typemap, and outside the usual SWIG exception-handling
	// code.  So, since this is expected to be rare, we 
	// print out a message, and abort with a standard C++ exception.
	// This will be uncaught, and the program will exit.
	throw std::runtime_error("Dynamic cast failed in PythonExportable.");
      }

      // Construct the string encoding the address. The SWIGged Python
      // object stores this string in its "this" data.
      SWIG_MakePtr(swigaddr, (char*) derived_addr, cls);
      // Construct a Python tuple containing the encoded address.
      PyObject *swigthis = Py_BuildValue((char*) "(s)", swigaddr);

      // Get the module containing the SWIGged Python class.  It's
      // likely that this function will be called repeatedly with the
      // same module, so the result is cached.  (It's ok to use a static
      // cached value here, because we're inside the Python interpreter
      // lock.)
      static std::string lastmodule;
      static PyObject *module = 0;
      if(modulename() != lastmodule) {
	if(module) {
	  Py_XDECREF(module);
	}
	lastmodule = modulename();
	//       char *modulenm = const_cast<char*>(lastmodule.c_str());
	module = PyImport_ImportModule(const_cast<char*>(lastmodule.c_str()));
	// Because pythonObject() is often used within swig typemaps, it
	// shouldn't call pythonErrorRelay() when an exception occurs.
	// The calling function should check the return value and if
	// it's zero, should either return 0 to Python (if within a
	// typemap) or call pythonErrorRelay (if within C++ code that
	// doesn't return immediately to Python).
	if(!module) {
	  std::cerr << "pythonexportable: Failed to import module "
		    << lastmodule << std::endl;
	  releasePyLock(pystate);
	  return 0;
	}
      }
      // Get the SWIGged Python class from the module.
      static std::string lastclass;
      static PyObject *klass = 0;
      if(lastclass != classname()) {
	if(klass) {
	  Py_XDECREF(klass);
	}
	lastclass = classname();
	std::string classnm = lastclass + "Ptr";
	klass =PyObject_GetAttrString(module, const_cast<char*>(classnm.c_str()));
	if(!klass) {
	  std::cerr << "pythonexportable: Failed to import class " << classnm 
		    << " from module " << lastmodule << std::endl;
	  releasePyLock(pystate);
	  return 0;
	}
      }

      // Construct the Python object by calling the class, passing the
      // SWIG encoded address as the argument.
      PyObject *result = PyObject_CallObject(klass, swigthis);
      Py_XDECREF(swigthis);
      if(!result) {
	std::cerr << "pythonexportable: Failed to instantiate python object"
		  << std::endl;
	  releasePyLock(pystate);
	  return 0;
      }

      releasePyLock(pystate);
      return result;
    }
    catch (...) {
      releasePyLock(pystate);
      throw;
    }
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// If a C++ class derived from PythonExportable is to be used as a
// base class for other Python classes (via SWIG), then the C++
// derived class must also include PythonNative as a virtual base
// class.

template <class TYPE>
class PythonNative : virtual public PythonExportable<TYPE> {
private:
  PyObject * const self;
public:
  PythonNative(PyObject *slf)
    : self(slf)
  {
    PyGILState_STATE pystate = acquirePyLock();
    Py_XINCREF(self);
    releasePyLock(pystate);
  }
  virtual ~PythonNative() {
    PyGILState_STATE pystate = acquirePyLock();
    Py_XDECREF(self);
    releasePyLock(pystate);
  }
  virtual PyObject *pythonObject() const {
    PyGILState_STATE pystate = acquirePyLock();
    Py_XINCREF(self);
    releasePyLock(pystate);
    return self;
  }
};

#endif // PYTHONEXPORTABLE_H
