// -*- C++ -*-
// $RCSfile: property.h,v $
// $Revision: 1.69.4.4 $
// $Author: langer $
// $Date: 2014/10/09 18:06:38 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef PROPERTY_H
#define PROPERTY_H

// forward declarations
class Property;

#include <Python.h>
#include "common/identification.h" // for ltidobject
#include "common/pythonexportable.h"
#include <string>
#include <vector>
#include <map>

// things defined elsewhere
class CNonlinearSolver;
class CSubProblem;
class EdgeSet;
class Element;
class ElementFuncNodeIterator;
class FEMesh;
class Field;
class Flux;
class Equation;
class LinearizedSystem;
class MasterPosition;
class Material;
class OutputVal;
class PropertyOutput;
class NewEquation;
class SmallSystem;

// Property objects are universally created from PropertyRegistration
// objects' call methods, from Python.

// Since properties must be visible in Python, they must be SWIG'd,
// and in general should also have a "python part" of the SWIG'd
// interface, conventionally placed in an ".spy" file.  The python
// part of the interface must include registration of the property,
// i.e. the creation of a PropertyRegistration object with appropriate
// data.  The registration code must run at import-time.

// The property registration object must include the name of the
// property, the property's class, module, and a numerical "ordering"
// which is relative to all other property registration objects, and
// controls the presentation of this property in the GUI.  Following
// that, the property should indicate the parameters it requires, the
// fields it uses, and the fluxes to which it contributes.  It should
// indicate what type of property it is, and any outputs to which it
// contributes.

// The property type broadly indicates the role of this property in
// the material, and should be defined such that it only makes sense
// to have one property of each type in a material.  For instance, any
// property dependent on displacement and contributing to stress could
// advertise itself as being of type "Elasticity".  The OOF solver
// will then allow at most one property of type "Elasticity" per
// material.  The types are not predefined, property writers may make
// new types without modifying the engine code -- OOF will simply
// insist that at most one property of each defined type be present in
// each material.


// The EqnProperty and FluxProperty classes are derived from the
// Property class.  The EqnProperty API contains the following
// functions:
//  - force_value
//  - force_deriv_matrix
//  - first_time_deriv_matrix
//  - second_time_deriv_matrix
//
// The FluxProperty API contains
//  - flux_value
//  - static_flux_value
//  - flux_offset
//  - flux_matrix


class Property: virtual public PythonExportable<Property> {
private:
  const std::string name_;	// name of this instance
  std::string classname_;   // For PythonExportable-ability.
  std::string modulename_;  // Ditto
  std::vector<const Field*> fields_reqd; // fields reqd to compute this property
  Property(const Property&);	// prohibited

public:
  Property(const std::string &nm, PyObject *registration);
  virtual ~Property();

  // As a RegisteredCClass, Property must host a Python "registry"
  // entry, which is a list of Python objects.  This entry is
  // created as class data in the property.spy file.

  // This particular property's registration must also be stored, and
  // be retrievable.
  PyObject *registration_;
  PyObject *registration() const;

  const std::string &name() const { return name_; }
  // The following are required for a base class of PythonExportable.
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }

  // A Property is computable if all the Fields it requires are
  // defined on a Mesh.  A property is active if it is computable and
  // contributes to an active equation or active flux.  Activity and
  // computability are computed during the precomputation steps of
  // stiffness matrix construction and output computation.
  // bool is_active(const CSubProblem*) is in python
  // void find_active(const CSubProblem*) is in python
  bool is_computable(const CSubProblem*) const;

  // List of fields required to compute this Property
  const std::vector<const Field*> &fields_required() const {
    return fields_reqd;
  }
  // This field is required to compute this Property.  The derived
  // Properties don't call this directly, since they don't necessarily
  // know about compound Fields.  Instead, the Properties call
  // Field::registerProperty(Property*), which calls
  // Property::require_field().  This is done automatically in
  // Property::bookkeeping() (in property.spy), which is called by
  // Material::cross_reference().
  void require_field(const Field&);

  // The remaining virtual functions have default null bodies, so that
  // each Property only has to define the relevant ones:

  // Properties may need to find other properties in the material
  // (using Material::fetchProperty).  This function is called to tell
  // them that it's time to do that. It should throw an exception if
  // it's unsuccessful.
  virtual void cross_reference(Material*) {}

  // compute things that don't depend on Element
  virtual void precompute(FEMesh*) {}

  virtual bool constant_in_space() const = 0;

  // These routines allow Properties to precompute and store
  // mesh-specific data.  Since Materials and Properties are shared
  // between Meshes, Properties can't store mesh-specific data
  // themselves.  set_mesh_data stores data in the Mesh, and
  // get_mesh_data retrieves it. clear_mesh_data is a callback, called
  // when the Mesh is being destroyed and the data must be deleted.
  void set_mesh_data(FEMesh*, void *) const;
  void *get_mesh_data(const FEMesh*) const;
  virtual void clear_mesh_data(FEMesh*, void*) const {}

  // these functions are called when beginning and ending the
  // computations on an Element, allowing Element-dependent
  // precomputation and caching
  virtual void begin_element(const CSubProblem*, const Element*) {}
  virtual void end_element(const CSubProblem*, const Element*) {}

  // This function is called after equilibration, to allow the
  // computation of auxiliary fields which may depend on equilibrium
  // fluxes -- the canoncal example is plasticity, where the
  // yield condition is stress-dependent.
  virtual void post_process(CSubProblem *, const Element *) const {}


  // Output function.
  virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*)
    const { return; }

  virtual bool is_symmetric_K(const CSubProblem*) const;
  virtual bool is_symmetric_C(const CSubProblem*) const;
  virtual bool is_symmetric_M(const CSubProblem*) const;

}; // end of Property class definition

std::ostream &operator<<(std::ostream &, const Property&);


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


// class InterfaceProperty: public Property
// {
// public:
//   InterfaceProperty(const std::string &nm, PyObject *registration):
//     Property(nm, registration)
//   {}
//   virtual ~InterfaceProperty() {}
// };


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class AuxiliaryProperty: public Property {
public:
  AuxiliaryProperty(const std::string &nm, PyObject *registration)
    : Property(nm, registration)
  {}
  virtual bool constant_in_space() const { return true; }
};

class PhysicalProperty: public Property {
public:
  PhysicalProperty(const std::string &nm, PyObject *registration)
    : Property(nm, registration)
  {}
  // this function returns the polynomial order (in x and y) of the
  // quantity computed by fluxmatrix.
  virtual int integration_order(const CSubProblem*, const Element*) const = 0;
};


class FluxProperty: public PhysicalProperty {
private:
  // 'recurse' is used to prevent the default versions of flux_matrix
  // and static_flux_value from both being used at once, since they
  // call each other.  recurse must be mutable because flux_matrix and
  // static_flux_value are const functions.
  mutable bool recurse;

public:
  FluxProperty(const std::string &nm, PyObject *registration)
    : PhysicalProperty(nm,registration)
  {}

  // The flux is currently considered to have one of the following forms
  //
  //  (1)  flux = sigma(x,u,Du) + C Du^dot
  //
  //  (2)  flux = K(x,u,Du) Du + sigma_0(x,u,Du) + C Du^dot
  //
  // where u is the field and Du is its gradient,
  //       Du^dot is the time derivative of Du.
  //
  // In (1), sigma(x,u,Du) is the possibly nonlinear static part
  // of the flux, depending on x, u, Du.
  //
  // In (2), K(x,u,Du) is the linearization/derivative of the flux
  // with respect to Du and is typically only x-dependent for linear
  // problems. sigma_0(x,u,Du) is the flux offset that captures
  // remaining dependences on u & Du. The following is true by definition
  //
  //    sigma(x,u,Du) = K(x,u,Du) Du + sigma_0(x,u,Du)
  //

  void make_flux_contributions(const FEMesh*, const Element*,
			       const Flux*,
			       const MasterPosition&, double time,
			       const CNonlinearSolver*, SmallSystem*)
    const;

  // Redefining each of the following functions is optional in derived
  // classes, but at least one of them must be redefined.

  // Linearization/derivative of the flux with respect to field and
  // field derivatives.
  // Used to assemble the stiffness matrix and the Jacobian matrix.
  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*)
    const;

  // The actual value of the flux at the given element and given point.
  virtual void flux_value(const FEMesh *mesh, const Element *element,
			  const Flux *flux, const MasterPosition &pt,
			  double time, SmallSystem *fluxdata) const;

  // The static portion of the flux vector/tensor, equal to flux_value
  // for most cases, but not for viscoelasticity.
  virtual void static_flux_value(const FEMesh *mesh, const Element *element,
				 const Flux *flux, const MasterPosition &pt,
				 double time, SmallSystem *fluxdata) const;

  // Flux offset as described above.
  virtual void flux_offset(const FEMesh*, const Element*, const Flux*,
			   const MasterPosition&, double time, SmallSystem* )
    const { return; }

  // These functions are called from material.C before and after the
  // flux contributions are requested.  If properties have
  // per-evaluation-point expensive operations they want to perform,
  // they should do them in these functions.

  virtual void begin_point(const FEMesh*, const Element*,
			   const Flux*, const MasterPosition&) {}
  virtual void end_point(const FEMesh*, const Element*,
			 const Flux*, const MasterPosition&) {}

}; // end of FluxProperty class definition


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


class EqnProperty: public PhysicalProperty {

public:
  EqnProperty(const std::string &nm, PyObject *registration)
    : PhysicalProperty(nm,registration)
  {};

  void make_equation_contributions(const FEMesh*, const Element*,
				   const Equation*,
				   const MasterPosition&, double time,
				   const CNonlinearSolver*,
				   SmallSystem*)
    const;

  // A derived class can optionally redefine any of these functions.
  // It must redefine at least one of them.

  // The linearization/derivative of force with respect to field.
  virtual void force_deriv_matrix(const FEMesh*, const Element*,
				  const Equation*,
				  const ElementFuncNodeIterator&,
				  const MasterPosition&,
				  double time, SmallSystem* )
    const;

  // The value of the force at a given element and given point.
  virtual void force_value(const FEMesh*, const Element*,
			   const Equation*, const MasterPosition&,
			   double time, SmallSystem* )
    const { return; }

  // Contributions to the coefficient of the 1st time-deriv of the field.
  // An example of this is heat capacity.
  virtual void first_time_deriv_matrix(const FEMesh*, const Element*,
				       const Equation*,
				       const ElementFuncNodeIterator&,
				       const MasterPosition&,
				       double time, SmallSystem* )
    const { return; }

  // Contributions to the coefficient of the 2nd time-deriv of the field.
  // An example of this is mass density.
  virtual void second_time_deriv_matrix(const FEMesh*, const Element*,
					const Equation*,
					const ElementFuncNodeIterator&,
					const MasterPosition&,
					double time, SmallSystem* )
    const { return; }

}; // end of EqnProperty class definition

extern double deriv_eps;

#endif
