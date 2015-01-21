// -*- C++ -*-
// $RCSfile: pypropertywrapper.C,v $
// $Revision: 1.40.2.4 $
// $Author: langer $
// $Date: 2013/11/08 20:44:42 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/coord.h"
#include "common/pythonlock.h"
#include "common/swiglib.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/outputval.h"
#include "engine/pypropertywrapper.h"
#include "engine/smallsystem.h"

PyPropertyMethods::PyPropertyMethods(PyObject *referent)
  : referent_(referent)
{
  PyGILState_STATE pystate = acquirePyLock();
  Py_INCREF(referent_);
  releasePyLock(pystate);
}

PyPropertyMethods::~PyPropertyMethods() {
  PyGILState_STATE pystate = acquirePyLock();
  Py_DECREF(referent_);
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyPropertyMethods::py_precompute(PyObject *referent, Property *prop,
				      FEMesh *mesh) {
  char _mesh_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "precompute")) {
      // The function isn't defined in the derived class.  Call the
      // base class method instead.
      PyErr_Clear();
      prop->Property::precompute(mesh);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent,
					      (char*) "precompute_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      PyObject *args = Py_BuildValue((char*) "(s)", _mesh_temp);
      PyObject *k_result = PyEval_CallObject(func, args);
      Py_XDECREF(func);
      Py_XDECREF(args);
      if(k_result==NULL)
	pythonErrorRelay();
      Py_XDECREF(k_result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyPropertyMethods::py_cross_reference(PyObject *referent, Property *prop,
					   Material *mat)
{
  char _material_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "cross_reference")) {
      prop->Property::cross_reference(mat);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent,
					      (char*) "cross_reference_wrap");
      SWIG_MakePtr(_material_temp, (char *)mat, (char*)"_Material_p");
      PyObject *args = Py_BuildValue((char*) "(s)",_material_temp);
      PyObject *k_result = PyEval_CallObject(func, args);
      Py_XDECREF(func);
      Py_XDECREF(args);
      if(k_result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(k_result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyPropertyMethods::py_begin_element(PyObject *referent, Property *prop,
					 const CSubProblem *m,
					 const Element *el)
{
  char _element_temp[128];
  char _mesh_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "begin_element")) {
      prop->Property::begin_element(m, el);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent,
					      (char*)"begin_element_wrap");
      SWIG_MakePtr(_mesh_temp, (char *)m, (char*)"_CSubProblem_p");
      SWIG_MakePtr(_element_temp, (char *)el, (char*)"_Element_p");
      PyObject *args = Py_BuildValue((char*) "(ss)", _mesh_temp, _element_temp);
      PyObject *k_result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(k_result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(k_result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

void PyPropertyMethods::py_end_element(PyObject *referent, Property *prop,
				       const CSubProblem *m, const Element *el)
{
  char _element_temp[128];
  char _mesh_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, "end_element")) {
      prop->Property::end_element(m, el);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent,
					      (char*) "end_element_wrap");
      SWIG_MakePtr(_mesh_temp, (char *)m, (char*)"_CSubProblem_p");
      SWIG_MakePtr(_element_temp, (char *)el, (char*)"_Element_p");
      PyObject *args = Py_BuildValue((char*) "(ss)", _mesh_temp, _element_temp);
      PyObject *k_result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(k_result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(k_result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyFluxProperty::begin_point(const FEMesh *m, const Element *el,
				 const Flux *flx, const MasterPosition &mpos) 
{
  char _element_temp[128];
  char _mesh_temp[128];
  char _flx_temp[128];
  char _mpos_temp[128];

  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, "begin_point")) {
      this->FluxProperty::begin_point(m, el, flx, mpos);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent_,
					      (char*) "begin_point_wrap");
      SWIG_MakePtr(_mesh_temp, (char *) m, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char *) el, (char*)"_Element_p");
      SWIG_MakePtr(_flx_temp, (char *)flx, (char*)"_Flux_p");
      SWIG_MakePtr(_mpos_temp, (char *)(&mpos), (char*)"_MasterPosition_P");
      PyObject *args = Py_BuildValue((char*) "(ssss)", _mesh_temp,
				     _element_temp, _flx_temp, _mpos_temp);
      PyObject *k_result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(k_result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(k_result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

void PyFluxProperty::end_point(const FEMesh *m, const Element *el,
			       const Flux *flx, const MasterPosition &mpos) 
{
  char _element_temp[128];
  char _mesh_temp[128];
  char _flx_temp[128];
  char _mpos_temp[128];

  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "end_point")) {
      this->FluxProperty::end_point(m, el, flx, mpos);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent_,
					      (char*) "end_point_wrap");
      SWIG_MakePtr(_mesh_temp, (char *) m, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char *) el, (char*)"_Element_p");
      SWIG_MakePtr(_flx_temp, (char *)flx, (char*)"_Flux_p");
      SWIG_MakePtr(_mpos_temp, (char *)(&mpos), (char*)"_MasterPosition_P");
      PyObject *args = Py_BuildValue((char*) "(ssss)", _mesh_temp,
				     _element_temp, _flx_temp, _mpos_temp);
      PyObject *k_result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(k_result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(k_result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyPropertyMethods::py_post_process(PyObject *referent,
					const Property *prop,
					CSubProblem *m, const Element *el)
  const
{
  char _subp_temp[128];
  char _element_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "post_process")) {
      prop->Property::post_process(m, el);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent,
					      (char*) "post_process_wrap");
      SWIG_MakePtr(_subp_temp, (char *)m, (char*)"_CSubProblem_p");
      SWIG_MakePtr(_element_temp, (char *)el, (char*)"_Element_p");
      PyObject *args = Py_BuildValue((char*) "(ss)", _subp_temp, _element_temp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

// The PyPropertyMethods::py_output function is a bit different than
// the others, because it uses the returned value.  The C++ and Python
// signatures are different: in C++ a pointer to an OutputVal is
// passed in and the OutputVal is changed by the derived class
// function, which returns void.  In Python, the OutputVal isn't
// passed in, but the function returns an OutputVal which is added to
// it.

void PyPropertyMethods::py_output(PyObject *referent, const Property *prop,
			       const FEMesh *mesh, const Element *el,
			       const PropertyOutput *propout,
			       const MasterPosition &pos,
			       OutputVal *oval)
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _propout_temp[128];
  char _pos_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "output")) {
      prop->Property::output(mesh, el, propout, pos, oval);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent,
					      (char*) "output_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char*) el, (char*)"_Element_p");
      SWIG_MakePtr(_propout_temp, (char*) propout, (char*)"_PropertyOutput_p");
      SWIG_MakePtr(_pos_temp, (char *) (&pos), (char*)"_MasterPosition_p");
      PyObject *args = Py_BuildValue((char*) "(ssss)", _mesh_temp,
				     _element_temp, _propout_temp, _pos_temp);
      PyObject *pyresult = PyEval_CallObject(func, args);
      Py_XDECREF(func);
      Py_XDECREF(args);

      if(pyresult == NULL)
	pythonErrorRelay();

      // Check for None.  PyProperty.output_wrap() returns None if
      // the derived class doesn't define PyProperty.output().
      if(pyresult != Py_None) {
	// Convert result to a C++ object
	OutputVal *cresult;
	if(SWIG_GetPtrObj(pyresult, (void**)&cresult, "_OutputVal_p")) {
	  throw ErrProgrammingError(
			    "Python output() does not return an OutputVal",
			    __FILE__, __LINE__);
	}
	*oval += *cresult;
      }
      Py_XDECREF(pyresult);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

bool PyPropertyMethods::py_constant_in_space(PyObject *referent,
					     const Property *prop) 
  const
{
  bool c_result;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "constant_in_space")) {
      releasePyLock(pystate);
      return prop->Property::constant_in_space();
    }
    PyObject *func = PyObject_GetAttrString(referent,
					    (char*) "constant_in_space_wrap");
    PyObject *args = Py_BuildValue((char*) "()");
    PyObject *k_result = PyEval_CallObject(func, args);
    Py_XDECREF(func);
    Py_XDECREF(args);
    if(k_result == NULL) {
      pythonErrorRelay();
    }
    c_result = PyObject_IsTrue(k_result);
    Py_XDECREF(k_result);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return c_result;
}

//=\\=//=\\=//

bool PyPropertyMethods::is_symmetric_K(PyObject *referent, const Property *prop,
				       const CSubProblem *subp)
  const
{
  bool c_result;
  char _subp_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "is_symmetric_K")) {
      releasePyLock(pystate);
      return prop->Property::is_symmetric_K(subp);
    }
    PyObject *func = PyObject_GetAttrString(referent,
					    (char*) "is_symmetric_K_wrap");
    SWIG_MakePtr(_subp_temp, (char*) subp, (char*)"_CSubProblem_p");
    PyObject *args = Py_BuildValue((char*) "(s)", _subp_temp);
    PyObject *k_result = PyEval_CallObject(func, args);
    Py_XDECREF(func);
    Py_XDECREF(args);
    if(k_result == NULL) {
      pythonErrorRelay();
    }
    c_result = PyObject_IsTrue(k_result);
    Py_XDECREF(k_result);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return c_result;
}

bool PyPropertyMethods::is_symmetric_C(PyObject *referent, const Property *prop,
				       const CSubProblem *subp)
  const
{
  bool c_result;
  char _subp_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "is_symmetric_C")) {
      releasePyLock(pystate);
      return prop->Property::is_symmetric_C(subp);
    }
    PyObject *func = PyObject_GetAttrString(referent,
					    (char*) "is_symmetric_C_wrap");
    SWIG_MakePtr(_subp_temp, (char*) subp, (char*)"_CSubProblem_p");
    PyObject *args = Py_BuildValue((char*) "(s)", _subp_temp);
    PyObject *k_result = PyEval_CallObject(func, args);
    Py_XDECREF(func);
    Py_XDECREF(args);
    if(k_result == NULL) {
      pythonErrorRelay();
    }
    c_result = PyObject_IsTrue(k_result);
    Py_XDECREF(k_result);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return c_result;
}

bool PyPropertyMethods::is_symmetric_M(PyObject *referent, const Property *prop,
				       const CSubProblem *subp)
  const
{
  bool c_result;
  char _subp_temp[128];
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "is_symmetric_M")) {
      releasePyLock(pystate);
      return prop->Property::is_symmetric_M(subp);
    }
    PyObject *func = PyObject_GetAttrString(referent,
					    (char*) "is_symmetric_M_wrap");
    SWIG_MakePtr(_subp_temp, (char*) subp, (char*)"_CSubProblem_p");
    PyObject *args = Py_BuildValue((char*) "(s)", _subp_temp);
    PyObject *k_result = PyEval_CallObject(func, args);
    Py_XDECREF(func);
    Py_XDECREF(args);
    if(k_result == NULL) {
      pythonErrorRelay();
    }
    c_result = PyObject_IsTrue(k_result);
    Py_XDECREF(k_result);
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return c_result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

int PyPhysicalPropertyMethods::py_integration_order(
					    PyObject *referent,
					    const PhysicalProperty *prop,
					    const CSubProblem *subp, 
					    const Element *el)
  const
{
  char _element_temp[128];
  char _subp_temp[128];
  int c_result;
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent, (char*) "integration_order")) {
	throw ErrUserError("integration_order method is missing from Property " 
			   + prop->name());
    }
    PyObject *func = PyObject_GetAttrString(referent,
					    (char*) "integration_order_wrap");
    SWIG_MakePtr(_subp_temp, (char*) subp, (char*)"_CSubProblem_p");
    SWIG_MakePtr(_element_temp, (char*) el, (char*)"_Element_p");
    PyObject *args = Py_BuildValue((char*) "(ss)", _subp_temp, _element_temp);
    PyObject *k_result = PyEval_CallObject(func, args);
    Py_XDECREF(func);
    Py_XDECREF(args);
    if(k_result==NULL) {
      pythonErrorRelay();
    }

    c_result = PyInt_AsLong(k_result);
    Py_XDECREF(k_result);
  }
  catch (...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
  return c_result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Note that "regstn" is the registration entry of the property to 
// which the wrapper refers, not that of the wrapper itself.

// The "PythonNative" parent object holds a pointer to the referent
// Python object, and uses it to answer questions about the type of 
// object and so forth.  Because of this, we probably don't have to 
// do indirection on the repr's.

PyFluxProperty::PyFluxProperty(PyObject *referent, PyObject *regstn,
			       const std::string &name)
  : PythonNative<Property>(referent),
    FluxProperty(name, regstn),
    PyPropertyMethods(referent)
{}

PyFluxProperty::~PyFluxProperty() {}

//=\\=//=\\=//

void PyFluxProperty::flux_matrix(const FEMesh *mesh,
				 const Element *el,
				 const ElementFuncNodeIterator &efi,
				 const Flux *flux,
				 const MasterPosition &gpt,
				 double time,
				 SmallSystem *fluxdata)
  const
{
  char _mesh_temp[128];  // SWIG uses 128-byte arrays, also.
  char _element_temp[128];
  char _efni_temp[128];
  char _flux_temp[128];
  char _fluxdata_temp[128];
  char _mp_temp[128];
    
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "flux_matrix")) {
      this->FluxProperty::flux_matrix(mesh, el, efi, flux, gpt, time, fluxdata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent_,
					      (char*) "flux_matrix_wrap");
      SWIG_MakePtr(_mesh_temp, (char *)mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char *)el, (char*)"_Element_p");
      SWIG_MakePtr(_efni_temp, (char *)(&efi), 
		   (char*)"_ElementFuncNodeIterator_p");
      SWIG_MakePtr(_flux_temp, (char *)flux, (char*)"_Flux_p");
      SWIG_MakePtr(_fluxdata_temp, (char *)fluxdata, (char*)"_SmallSystem_p");
      SWIG_MakePtr(_mp_temp, (char *)(&gpt), (char*)"_MasterPosition_p");
      PyObject *args = Py_BuildValue((char*) "(sssssds)",
				     _mesh_temp, _element_temp,
				     _efni_temp, _flux_temp, _mp_temp, 
				     time,
				     _fluxdata_temp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyFluxProperty::flux_value(const FEMesh *mesh,
				const Element *element,
				const Flux *flux, 
				const MasterPosition &pt,
				double time, 
				SmallSystem *fluxdata)
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _flux_temp[128];
  char _mp_temp[128];
  char _fluxdata_temp[128];

  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "flux_value")) {
      this->FluxProperty::flux_value(mesh, element, flux, pt, time, fluxdata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent_,
					      (char*) "flux_value_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char *) element, (char*)"_Element_p");
      SWIG_MakePtr(_flux_temp, (char *) flux, (char*)"_Flux_p");
      SWIG_MakePtr(_mp_temp, (char *)(&pt), (char*)"_MasterPosition_p");
      SWIG_MakePtr(_fluxdata_temp, (char *) fluxdata, (char*)"_SmallSystem_p");
      PyObject *args = Py_BuildValue((char*) "(ssssds)",
				     _mesh_temp, _element_temp, _flux_temp,
				     _mp_temp, time, _fluxdata_temp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result == NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyFluxProperty::static_flux_value(const FEMesh *mesh,
				       const Element *element,
				       const Flux *flux, 
				       const MasterPosition &pt,
				       double time, 
				       SmallSystem *fluxdata)
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _flux_temp[128];
  char _mp_temp[128];
  char _fluxdata_temp[128];

  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "static_flux_value")) {
      this->FluxProperty::static_flux_value(mesh, element, flux, pt, time,
					fluxdata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent_,
					      (char*) "static_flux_value_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char *) element, (char*)"_Element_p");
      SWIG_MakePtr(_flux_temp, (char *) flux, (char*)"_Flux_p");
      SWIG_MakePtr(_mp_temp, (char *)(&pt), (char*)"_MasterPosition_p");
      SWIG_MakePtr(_fluxdata_temp, (char *) fluxdata, (char*)"_SmallSystem_p");
      PyObject *args = Py_BuildValue((char*) "(ssssds)",
				     _mesh_temp, _element_temp, _flux_temp,
				     _mp_temp, time, _fluxdata_temp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result == NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyFluxProperty::flux_offset(const FEMesh *mesh, const Element *el,
				 const Flux *flux, 
				 const MasterPosition &gpt,
				 double time,
				 SmallSystem *fluxdata) 
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _flux_temp[128];
  char _fluxdata_temp[128];
  char _mp_temp[128];
  
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "flux_offset")) {
      this->FluxProperty::flux_offset(mesh, el, flux, gpt, time, fluxdata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent_,
					      (char*) "flux_offset_wrap");
      SWIG_MakePtr(_mesh_temp, (char *)mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char *)el, (char*)"_Element_p");
      SWIG_MakePtr(_flux_temp, (char *)flux, (char*)"_Flux_p");
      SWIG_MakePtr(_fluxdata_temp, (char *)fluxdata, (char*)"_SmallSystem_p");
      SWIG_MakePtr(_mp_temp, (char *)(&gpt), (char*)"_MasterPosition_p");
      PyObject *args = Py_BuildValue((char*) "(ssssds)",
				     _mesh_temp, _element_temp,
				     _flux_temp, _mp_temp, time, 
				     _fluxdata_temp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result==NULL) {
	pythonErrorRelay();
      }
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

PyEqnProperty::PyEqnProperty(PyObject *referent, PyObject *regstn,
			     const std::string &name)
  : PythonNative<Property>(referent),
    EqnProperty(name, regstn),
    PyPropertyMethods(referent)
{}

PyEqnProperty::~PyEqnProperty() {}

//=\\=//=\\=//

void PyEqnProperty::force_deriv_matrix(const FEMesh *mesh,
				       const Element *element,
				       const Equation *eqn,
				       const ElementFuncNodeIterator &efi,
				       const MasterPosition &pt,
				       double time,
				       SmallSystem *eqndata)
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _eqn_temp[128];
  char _efni_temp[128];
  char _mp_temp[128];
  char _eqndata_tmp[128];
  
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "force_deriv_matrix")) {
      this->EqnProperty::force_deriv_matrix(mesh, element, eqn, efi, pt, time,
					    eqndata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(
			      referent_, (char*) "force_deriv_matrix_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char*) element, (char*)"_Element_p");
      SWIG_MakePtr(_eqn_temp, (char*) eqn, (char*)"_Equation_p");
      SWIG_MakePtr(_efni_temp, (char*)(&efi),
		   (char*)"_ElementFuncNodeIterator_p");
      SWIG_MakePtr(_mp_temp, (char*)(&pt), (char*)"_MasterPosition_p");
      SWIG_MakePtr(_eqndata_tmp, (char*) eqndata, "(char*)_SmallSystem_p");
      PyObject *args = Py_BuildValue((char*) "(sssssds)",
				     _mesh_temp,
				     _element_temp,
				     _eqn_temp,
				     _efni_temp,
				     _mp_temp,
				     time,
				     _eqndata_tmp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result == NULL)
	pythonErrorRelay();
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyEqnProperty::force_value(const FEMesh *mesh,
				const Element *element,
				const Equation *eqn,
				const MasterPosition &pt,
				double time,
				SmallSystem *eqndata)
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _eqn_temp[128];
  char _mp_temp[128];
  char _eqndata_tmp[128];
  
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "force_value")) {
      this->EqnProperty::force_value(mesh, element, eqn, pt, time, eqndata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(referent_,
					      (char*) "force_value_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char*) element, (char*)"_Element_p");
      SWIG_MakePtr(_eqn_temp, (char*) eqn, (char*)"_Equation_p");
      SWIG_MakePtr(_mp_temp, (char*)(&pt), (char*)"_MasterPosition_p");
      SWIG_MakePtr(_eqndata_tmp, (char*) eqndata, (char*)"_SmallSystem_p");
      PyObject *args = Py_BuildValue((char*) "(ssssds)",
				     _mesh_temp,
				     _element_temp,
				     _eqn_temp,
				     _mp_temp,
				     time,
				     _eqndata_tmp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result == NULL)
	pythonErrorRelay();
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyEqnProperty::first_time_deriv_matrix(const FEMesh *mesh,
					    const Element *element,
					    const Equation *eqn,
					    const ElementFuncNodeIterator &efi,
					    const MasterPosition &pt,
					    double time, SmallSystem *eqndata)
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _eqn_temp[128];
  char _efni_temp[128];
  char _mp_temp[128];
  char _eqndata_tmp[128];
  
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "first_time_deriv_matrix")) {
      this->EqnProperty::first_time_deriv_matrix(mesh, element, eqn, efi, pt,
						 time, eqndata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(
		      referent_, (char*) "first_time_deriv_matrix_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char*) element, (char*)"_Element_p");
      SWIG_MakePtr(_eqn_temp, (char*) eqn, (char*)"_Equation_p");
      SWIG_MakePtr(_efni_temp, (char*)(&efi), 
		   (char*)"_ElementFuncNodeIterator_p");
      SWIG_MakePtr(_mp_temp, (char*)(&pt), (char*)"_MasterPosition_p");
      SWIG_MakePtr(_eqndata_tmp, (char*)(&eqndata), (char*)"_SmallSystem_p");
      PyObject *args = Py_BuildValue((char*) "(sssssds)",
				     _mesh_temp,
				     _element_temp,
				     _eqn_temp,
				     _efni_temp,
				     _mp_temp,
				     time,
				     _eqndata_tmp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result == NULL)
	pythonErrorRelay();
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//

void PyEqnProperty::second_time_deriv_matrix(const FEMesh *mesh,
					     const Element *element,
					     const Equation *eqn,
				     const ElementFuncNodeIterator &efi,
					     const MasterPosition &pt,
					     double time,
					     SmallSystem *eqndata)
  const
{
  char _mesh_temp[128];
  char _element_temp[128];
  char _eqn_temp[128];
  char _efni_temp[128];
  char _mp_temp[128];
  char _eqndata_tmp[128];
  
  PyGILState_STATE pystate = acquirePyLock();
  try {
    if(!PyObject_HasAttrString(referent_, (char*) "second_time_deriv_matrix")) {
      this->EqnProperty::second_time_deriv_matrix(mesh, element, eqn, efi, pt,
						  time, eqndata);
    }
    else {
      PyObject *func = PyObject_GetAttrString(
		      referent_, (char*) "second_time_deriv_matrix_wrap");
      SWIG_MakePtr(_mesh_temp, (char*) mesh, (char*)"_FEMesh_p");
      SWIG_MakePtr(_element_temp, (char*) element, (char*)"_Element_p");
      SWIG_MakePtr(_eqn_temp, (char*) eqn, (char*)"_Equation_p");
      SWIG_MakePtr(_efni_temp, (char*)(&efi),
		   (char*)"_ElementFuncNodeIterator_p");
      SWIG_MakePtr(_mp_temp, (char*)(&pt), (char*)"_MasterPosition_p");
      SWIG_MakePtr(_eqndata_tmp, (char*)(&eqndata), (char*)"_SmallSystem_p");
      PyObject *args = Py_BuildValue((char*) "(sssssds)",
				     _mesh_temp,
				     _element_temp,
				     _eqn_temp,
				     _efni_temp,
				     _mp_temp,
				     time,
				     _eqndata_tmp);
      PyObject *result = PyEval_CallObject(func, args);
      Py_XDECREF(args);
      Py_XDECREF(func);
      if(result == NULL)
	pythonErrorRelay();
      Py_XDECREF(result);
    }
  }
  catch(...) {
    releasePyLock(pystate);
    throw;
  }
  releasePyLock(pystate);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::string PyPropertyElementData::classname_("PyPropertyElementData");
std::string PyPropertyElementData::modulename_(
				       "ooflib.SWIG.engine.pypropertywrapper");

PyPropertyElementData::PyPropertyElementData(const std::string & name,
					     PyObject *dat) 
  : ElementData(name), _data(dat) 
{
  PyGILState_STATE pystate = acquirePyLock();
  Py_INCREF(_data);
  releasePyLock(pystate);
}

// For the particular case of PyObject *'s, simple member 
// retrieval through SWIG doesn't appear to work -- you have to 
// override SWIG's conversion-to-pointer-string to get the actual
// Python object out.  This function has the appropriate typemap
// defined in pypropertywrapper.swg.
PyObject *PyPropertyElementData::data() {
  // Hacky extra incref.
  PyGILState_STATE pystate = acquirePyLock();
  Py_INCREF(_data);
  releasePyLock(pystate);
  return _data;
}

PyPropertyElementData::~PyPropertyElementData() {
  // It's an error if this refcount is already zero -- avoid XDECREF.
  PyGILState_STATE pystate = acquirePyLock();
  Py_DECREF(_data);
  releasePyLock(pystate);
}
// PyPropertyElementData-handling functions.  Simple wrappers, mostly.
// These are here partially because Element doesn't have a convenient
// SWIG file, and partially because of the need to do the dynamic
// cast.  More direct Python access to the element functions
// is not out of the question.

// int PyProperty::appendElementData(Element *el, 
// 					 PyPropertyElementData *data)
// {
//   return el->appendData(data);
// }

// PyPropertyElementData *PyProperty::getElementData(Element *el, int i)
// {
//   return dynamic_cast<PyPropertyElementData*>(el->getData(i));
// }

// int PyProperty::getElementDataIndex(Element *el, std::string name)
// {
//   std::cerr << "getElementDataIndex" << std::endl;
//   return el->getIndexByName(name);
// }

