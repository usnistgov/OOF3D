// -*- C++ -*-
// $RCSfile: propertyoutput.C,v $
// $Revision: 1.26.2.4 $
// $Author: fyc $
// $Date: 2014/07/28 22:17:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/printvec.h"	// for debugging
#include "common/pythonlock.h"
#include "engine/IO/propertyoutput.h"
#include "engine/element.h"
#include "engine/femesh.h"
#include "engine/material.h"
#include "engine/outputval.h"
#include "engine/property.h"
#include "engine/symmmatrix.h"

// TODO 3.1: PropertyOutputs should NOT be computed by the
// Properties directly.  That is, there should not be a
// Property::output function.  This is because a user may want to add
// a PropertyOutput to an existing Property without modifying the
// Property itself.  Instead, PropertyOutputRegistrations should have
// a mechanism for being told which Properties contribute to them, and
// to specify a callback function for each Property.  The callback
// does the actual computation, instead of Property::output. This may
// be harder than it looks...  Presumably the registration of the
// Property and callback should be done from Python, but the callback
// itself must be C++.  Should there be a swigged
// PropertyOutputContribution class?  Each subclass will have to have
// a singleton instance which will be swigged.

std::vector<PropertyOutputRegistration*> &
PropertyOutputRegistration::allPropertyOutputRegs()
{
  static std::vector<PropertyOutputRegistration*> vec;
  return vec;
}

PropertyOutputRegistration::PropertyOutputRegistration(
			    const std::string &name,
			    const PropertyOutputInit *init) 
  : name_(name),
    index_(allPropertyOutputRegs().size()),
    initializer_(init)
{
  allPropertyOutputRegs().push_back(this);
}

// Count existing PropertyOutputRegistrations.

int nPropertyOutputRegistrations() {
  return PropertyOutputRegistration::allPropertyOutputRegs().size();
}

// Retrieve a PropertyOutputRegistration by name.

PropertyOutputRegistration *getPropertyOutputReg(const std::string &name) {
  std::vector<PropertyOutputRegistration*> &apor =
    PropertyOutputRegistration::allPropertyOutputRegs();
  for(std::vector<PropertyOutputRegistration*>::iterator i=apor.begin();
      i<apor.end(); ++i)
    {
      if(name == (*i)->name())
	return *i;
    }
  return 0;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PropertyOutput::PropertyOutput(const std::string &name, PyObject *params)
  : name_(name),
    params_(params),
    index_(getPropertyOutputReg(name)->index())
{
  PyGILState_STATE pystate = acquirePyLock();
  Py_XINCREF(params_);
  releasePyLock(pystate);
}

PropertyOutput::~PropertyOutput() {
  PyGILState_STATE pystate = acquirePyLock();
  Py_XDECREF(params_);
  releasePyLock(pystate);
}

std::vector<OutputValue> *
PropertyOutput::evaluate(FEMesh *mesh, Element *element,
			 const PropertyOutputInit *init, 
			 const std::vector<MasterCoord*> *mc)
{
  std::vector<OutputValue> *results = new std::vector<OutputValue>;
  results->reserve(mc->size());
  const Material *material = element->material();
  if(material) {
    const std::vector<Property*> &props = material->outputProperties(this);
//     material->begin_element(mesh, element);
    // Loop over points within the element.
    for(std::vector<MasterCoord*>::const_iterator i=mc->begin(); i!=mc->end();
	++i)
      {
	OutputVal *data((*init)(this, mesh, element, **i));
	// Loop over properties that contribute to this output.
	for(std::vector<Property*>::size_type p=0; p<props.size(); p++) {
	  // *Don't* check for active properties here; just loop over
	  // all of them.  Properties are active or inactive on
	  // SubProblems, not FEMeshes, and we don't have a SubProblem
	  // here.
	  props[p]->output(mesh, element, this, **i, data); // adds to data
	}	// end loop over Properties
	results->push_back(OutputValue(data));
      
      } // end loop over points
//     material->end_element(mesh, element);
  }
  else {			// no material!
    for(std::vector<MasterCoord*>::const_iterator i=mc->begin(); i!=mc->end();
	++i)
      results->push_back(OutputValue((*init)(this, mesh, element, **i)));
  }
  return results;
}

double PropertyOutput::getFloatParam(const char *name) const {
  double x;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    // params_ is a dictionary
    PyObject *obj = PyMapping_GetItemString(params_, (char*) name);
    if(!obj)
      pythonErrorRelay();
    x = PyFloat_AsDouble(obj);
    Py_XDECREF(obj);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return x;
}

int PropertyOutput::getIntParam(const char *name) const {
  int x;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    // params_ is a dictionary
    PyObject *obj = PyMapping_GetItemString(params_, (char*) name);
    if(!obj)
      pythonErrorRelay();
    x = PyInt_AsLong(obj);
    Py_XDECREF(obj);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return x;
}

const std::string *PropertyOutput::getStringParam(const char *name) const {
  std::string *x = new std::string;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    // params_ is a dictionary
    PyObject *obj = PyMapping_GetItemString(params_, (char*) name);
    if(!obj)
      pythonErrorRelay();
    *x = PyString_AsString(obj);
    Py_XDECREF(obj);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return x;
}

const std::string *PropertyOutput::getEnumParam(const char *name) const {
  std::string *x = new std::string;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    // params_ is a dictionary
    PyObject *obj = PyMapping_GetItemString(params_, (char*) name);
    if(!obj) {
      pythonErrorRelay();
    }
    PyObject *str = PyObject_GetAttrString(obj, (char*) "name");
    if(!str) {
      Py_XDECREF(obj);
      pythonErrorRelay();
    }
    *x = PyString_AsString(str);
    Py_XDECREF(str);
    Py_XDECREF(obj);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return x;
}

const std::string *PropertyOutput::getRegisteredParamName(const char *name)
  const
{
  std::string *x = new std::string;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    // Get the parameter out of the dictionary
    PyObject *obj = PyMapping_GetItemString(params_, (char*) name);
    if(!obj)
      pythonErrorRelay();
    // Call the parameter's "name" function"
    PyObject *str = PyObject_CallMethod(obj, (char*) "name", 0);
    if(!str) {
      Py_XDECREF(obj);
      pythonErrorRelay();
    }
    *x = PyString_AsString(str);
    Py_XDECREF(str);
    Py_XDECREF(obj);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return x;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Initializers for PropertyOutputs of various types.  These
// initialize the output to zero, which is usually what's wanted.
// Other initializer classes can compute other property-independent
// quantities. 

OutputVal *ScalarPropertyOutputInit::operator()(const PropertyOutput*,
						const FEMesh*,
						const Element*,
						const MasterCoord&) const
{
  return new ScalarOutputVal(0.0);

}

OutputVal *TwoVectorPropertyOutputInit::operator()(const PropertyOutput*,
						   const FEMesh*,
						   const Element*,
						   const MasterCoord&) const
{
  return new VectorOutputVal(2);
}

OutputVal *ThreeVectorPropertyOutputInit::operator()(const PropertyOutput*,
						     const FEMesh*,
						     const Element*,
						     const MasterCoord&) const
{
  return new VectorOutputVal(3);
}

OutputVal *SymmMatrix3PropertyOutputInit::operator()(const PropertyOutput*,
						     const FEMesh*,
						     const Element*,
						     const MasterCoord&) const
{
  return new SymmMatrix3();
}
