// -*- C++ -*-
// $RCSfile: pypropertywrapper.h,v $
// $Revision: 1.35.6.5 $
// $Author: langer $
// $Date: 2014/11/05 16:54:29 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef PYPROPERTYWRAPPER_H
#define PYPROPERTYWRAPPER_H

// Structure to wrap a pure-Python property, and make it available by
// way of the usual interface to the stiffness-matrix construction
// process.

#include <Python.h>
#include "engine/element.h"
#include "property.h"
#include "common/pythonexportable.h"

class Field;
class Flux;
class SmallSystem;
class Material;
class FEMesh;
class ElementFuncNodeIterator;
class MasterPosition;


class PyPropertyMethods {
public:
  PyPropertyMethods(PyObject*);
  virtual ~PyPropertyMethods();
  // A "py_" prefix was added to these method names to keep the clang
  // compiler from complaining about hidden overloaded virtual
  // functions.
  virtual void py_precompute(PyObject*, Property*, FEMesh*);
  virtual void py_cross_reference(PyObject*, Property*, Material*);
  virtual void py_begin_element(PyObject*, Property*, const CSubProblem*,
				const Element*);
  virtual void py_end_element(PyObject*, Property*,
			      const CSubProblem*, const Element*);
  virtual void py_post_process(PyObject*, const Property*, 
			       CSubProblem *, const Element*) const;
  virtual bool py_constant_in_space(PyObject*, const Property*) const;
  virtual void py_output(PyObject*, const Property*, const FEMesh*,
			 const Element*,
			 const PropertyOutput*,
			 const MasterPosition&, OutputVal*) const;
  bool is_symmetric_K(PyObject*, const Property*, const CSubProblem*) const;
  bool is_symmetric_C(PyObject*, const Property*, const CSubProblem*) const;
  bool is_symmetric_M(PyObject*, const Property*, const CSubProblem*) const;
protected:
  PyObject *referent_;		// pointer to the actual Python object
};

class PyPhysicalPropertyMethods {
public:
  virtual int py_integration_order(PyObject*, const PhysicalProperty*,
				const CSubProblem*, const Element*) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PyFluxProperty : public FluxProperty,
		       public PyPropertyMethods, 
		       public PyPhysicalPropertyMethods,
		       virtual public PythonNative<Property>
{
public:
  PyFluxProperty(PyObject *referent, PyObject *regstn,
			const std::string &name);
  virtual ~PyFluxProperty();
  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*) const;
  virtual void flux_value(const FEMesh*, const Element*,
			  const Flux*, const MasterPosition&,
			  double time, SmallSystem*) const;
  virtual void static_flux_value(const FEMesh*, const Element*,
				 const Flux*, const MasterPosition&,
				 double time, SmallSystem*) const;
  virtual void flux_offset(const FEMesh*, const Element*,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*) const;

  virtual void precompute(FEMesh *m) {
    PyPropertyMethods::py_precompute(referent_, this, m);
  }
  virtual void cross_reference(Material *m) { 
    PyPropertyMethods::py_cross_reference(referent_, this, m);
  }
  virtual void begin_element(const CSubProblem *sb, const Element *e) {
    PyPropertyMethods::py_begin_element(referent_, this, sb, e);
  }
  virtual void end_element(const CSubProblem *sb, const Element *e) {
    PyPropertyMethods::py_end_element(referent_, this, sb, e);
  }
  virtual void begin_point(const FEMesh *m, const Element *e,
			   const Flux *f, const MasterPosition &p);
  virtual void end_point(const FEMesh *m, const Element *e,
			 const Flux *f, const MasterPosition &p);
  virtual void post_process(CSubProblem *sb, const Element *e) const {
    PyPropertyMethods::py_post_process(referent_, this, sb, e);
  }
  virtual bool constant_in_space() const {
    return PyPropertyMethods::py_constant_in_space(referent_, this);
  }
  virtual void output(const FEMesh *m, const Element *e, 
		      const PropertyOutput *po,
		      const MasterPosition &p, OutputVal *ov) const {
    PyPropertyMethods::py_output(referent_, this, m, e, po, p, ov);
  }
  virtual int integration_order(const CSubProblem *sb, const Element *e) const {
    return PyPhysicalPropertyMethods::py_integration_order(referent_, this,
							   sb, e);
  }
  bool is_symmetric_K(const CSubProblem *sb) const {
    return PyPropertyMethods::is_symmetric_K(referent_, this, sb);
  }
  bool is_symmetric_C(const CSubProblem *sb) const  {
    return PyPropertyMethods::is_symmetric_C(referent_, this, sb);
  }
  bool is_symmetric_M(const CSubProblem *sb) const {
    return PyPropertyMethods::is_symmetric_M(referent_, this, sb);
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class PyEqnProperty : public EqnProperty,
		      public PyPropertyMethods,
		      public PyPhysicalPropertyMethods,
		      virtual public PythonNative<Property>
{
public:
  PyEqnProperty(PyObject *referent, PyObject *regstn,
		       const std::string &name);
  virtual ~PyEqnProperty();
  virtual void force_deriv_matrix(const FEMesh*, const Element*,
				  const Equation*,
				  const ElementFuncNodeIterator&,
				  const MasterPosition&,
				  double time, SmallSystem*) const;
  virtual void force_value(const FEMesh*, const Element*,
			   const Equation*, const MasterPosition&,
			   double time, SmallSystem*) const;
  virtual void first_time_deriv_matrix(const FEMesh*, const Element*,
				       const Equation*,
				       const ElementFuncNodeIterator&,
				       const MasterPosition&,
				       double time, SmallSystem*) const;
  virtual void second_time_deriv_matrix(const FEMesh*, const Element*,
				       const Equation*,
				       const ElementFuncNodeIterator&,
				       const MasterPosition&,
					double time, SmallSystem*) const;
  virtual void precompute(FEMesh *m) {
    PyPropertyMethods::py_precompute(referent_, this, m);
  }
  virtual void cross_reference(Material *m) { 
    PyPropertyMethods::py_cross_reference(referent_, this, m);
  }
  virtual void begin_element(const CSubProblem *sb, const Element *e) {
    PyPropertyMethods::py_begin_element(referent_, this, sb, e);
  }
  virtual void end_element(const CSubProblem *sb, const Element *e) {
    PyPropertyMethods::py_end_element(referent_, this, sb, e);
  }
  virtual void post_process(CSubProblem *sb, const Element *e) const {
    PyPropertyMethods::py_post_process(referent_, this, sb, e);
  }
  virtual bool constant_in_space() const {
    return PyPropertyMethods::py_constant_in_space(referent_, this);
  }
  virtual void output(const FEMesh *m, const Element *e, 
		      const PropertyOutput *po,
		      const MasterPosition &p, OutputVal *ov) const {
    PyPropertyMethods::py_output(referent_, this, m, e, po, p, ov);
  }
  virtual int integration_order(const CSubProblem *sb, const Element *e) const {
    return PyPhysicalPropertyMethods::py_integration_order(referent_, this,
							   sb, e);
  }
  bool is_symmetric_K(const CSubProblem *sb) const {
    return PyPropertyMethods::is_symmetric_K(referent_, this, sb);
  }
  bool is_symmetric_C(const CSubProblem *sb) const  {
    return PyPropertyMethods::is_symmetric_C(referent_, this, sb);
  }
  bool is_symmetric_M(const CSubProblem *sb) const {
    return PyPropertyMethods::is_symmetric_M(referent_, this, sb);
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Data storage class for objects descended from PyFluxProperty or
// PyEqnProperty.

class PyPropertyElementData : public ElementData {
private:
  PyObject *_data;
  static std::string classname_;
  static std::string modulename_;
public:
  PyPropertyElementData(const std::string &name, PyObject *dat);
  virtual ~PyPropertyElementData();
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }
  PyObject *data();
};


#endif // PYPROPERTYWRAPPER_H
