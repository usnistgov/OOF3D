// -*- C++ -*-
// $RCSfile: properties.swg,v $
// $Revision: 1.23.8.3 $
// $Author: langer $
// $Date: 2014/10/09 18:06:37 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PROPERTIES_SWG
#define PROPERTIES_SWG

%module property
%include "engine/typemaps.swg"

%pragma(python) include="engine/property.spy"

%typemap(python,out) PyObject * {
  $target = $source;
}

%{
#include "engine/property.h"
#include "engine/csubproblem.h"
%}


class Property {
public:
  ~Property();
  const string &name();
  const string &classname(); // Returns the name of the derived class.
  const string &modulename(); 
  bool is_computable(CSubProblem*);
  PyObject *registration();

  // Methods that are redefined in pypropertywrapper.h must be swigged
  // under different names, so that Python won't call the wrapper
  // function recursively if the method is *not* redefined in a
  // derived Python Property class.
  %name(c_cross_reference) void cross_reference(Material*);
  %name(c_precompute) void precompute(FEMesh*);
  %name(c_is_symmetric_K) bool is_symmetric_K(const CSubProblem*);
  %name(c_is_symmetric_C) bool is_symmetric_C(const CSubProblem*);
  %name(c_is_symmetric_M) bool is_symmetric_M(const CSubProblem*);
  %name(c_constant_in_space) bool constant_in_space();
  %name(c_begin_element) void begin_element(CSubProblem*, Element*);
  %name(c_end_element) void end_element(CSubProblem*, Element*);
  %name(c_post_process) void post_process(CSubProblem*, Element*);
  %name(c_output) void output(const FEMesh*, Element*, PropertyOutput*,
			      MasterPosition&, OutputVal*);

};

class PhysicalProperty : public Property {
public:
  %name(c_integration_order)
  int integration_order(CSubProblem*, Element*);
};

class FluxProperty : public PhysicalProperty {
public:
  %name(c_flux_matrix)
  void flux_matrix(FEMesh*, Element*, ElementFuncNodeIterator&, Flux*,
		   MasterPosition&, double, SmallSystem*);
  %name(c_flux_value)
  void flux_value(FEMesh*, Element*, Flux*, MasterPosition&, double,
		  SmallSystem*);
  %name(c_static_flux_value)
  void static_flux_value(FEMesh*, Element*, Flux*, MasterPosition&,
			 double, SmallSystem*);
  %name(c_flux_offset)
  void flux_offset(FEMesh*, Element*, Flux*, MasterPosition&,
		   double, SmallSystem*);
  %name(c_begin_point) void begin_point(FEMesh*, Element*, Flux*,
					MasterPosition&);
  %name(c_end_point) void end_point(FEMesh*, Element*, Flux*, MasterPosition&);
};

class EqnProperty : public PhysicalProperty {
public:
  %name(c_force_deriv_matrix)
  void force_deriv_matrix(FEMesh*, Element*, Equation*,
			  ElementFuncNodeIterator&, MasterPosition&, double,
			  SmallSystem*);
  %name(c_force_value)
  void force_value(FEMesh*, Element*, Equation*, MasterPosition&, double,
		   SmallSystem*);
  %name(c_first_time_deriv_matrix)
  void first_time_deriv_matrix(FEMesh*, Element*, Equation*, 
			       ElementFuncNodeIterator&, MasterPosition&,
			       double, SmallSystem*);
  %name(c_second_time_deriv_matrix)
  void second_time_deriv_matrix(FEMesh*, Element*, Equation*, 
			       ElementFuncNodeIterator&, MasterPosition&,
			       double, SmallSystem*);
};

double deriv_eps;

%typemap(python,out) PyObject *;

#endif // PROPERTIES_SWG
