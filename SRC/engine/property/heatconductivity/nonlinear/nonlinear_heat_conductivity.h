// -*- C++ -*-
// $RCSfile: nonlinear_heat_conductivity.h,v $
// $Revision: 1.13.8.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:49 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef NONLINEAR_HEAT_CONDUCTIVITY_H
#define NONLINEAR_HEAT_CONDUCTIVITY_H


#include "common/coord.h"
#include "engine/property.h"
#include "engine/symmmatrix.h"
#include <string>

class DoubleVec;
class Element;
class Material;
class FEMesh;
class OrientationPropBase;
class SmallSystem;
class ScalarField;
class VectorFlux;
class ElementNodeIterator;

// There's an extra layer in the class hierarchy here so that test
// properties that don't provide a flux_matrix method can be defined.
// These are used in the regression tests.  Users deriving their own
// nonlinear heat conductivity properties using the examples in
// OOFEXTENSIONS should ignore NonlinearHeatConductivityBase and
// TestNonlinearHeatConductivity, and just use
// NonlinearHeatConductivity.

class NonlinearHeatConductivityNoDeriv : public FluxProperty {
public:
  NonlinearHeatConductivityNoDeriv(PyObject *registry, const std::string &name);
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return false; }
  // virtual bool is_symmetric_K(const CSubProblem*) const { return false; }
  virtual void static_flux_value(const FEMesh*, const Element*,
				 const Flux*,
				 const MasterPosition&,
				 double time,
				 SmallSystem *) const;
protected:
  ScalarField *temperature;
  VectorFlux  *heat_flux;

  virtual void nonlin_heat_flux(const Coord &,
				double time, double temperature,
				const DoubleVec &temperature_gradient,
				DoubleVec &heat_flux) const = 0;
}; // NonlinearHeatConductivityNoDeriv


class NonlinearHeatConductivity : public NonlinearHeatConductivityNoDeriv {
public:
  NonlinearHeatConductivity(PyObject *registry, const std::string &name)
    : NonlinearHeatConductivityNoDeriv(registry, name) {};
  virtual ~NonlinearHeatConductivity() {};
  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*,
			   const MasterPosition&,
			   double time,
			   SmallSystem*) const;

protected:
  virtual void nonlin_heat_flux_deriv_wrt_temperature(
			      const Coord&,
			      double time, double temperature,
			      const DoubleVec &temperature_gradient,
			      DoubleVec &heat_flux_deriv) const = 0;

  virtual void nonlin_heat_flux_deriv_wrt_temperature_gradient(
			       const Coord&,
			       double time, double temperature,
			       const DoubleVec &temperature_gradient,
			       SmallMatrix &heat_flux_deriv) const = 0;
}; // NonlinearHeatConductivity

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


class TestNonlinearHeatConductivityNoDeriv : public NonlinearHeatConductivityNoDeriv {

public:
  TestNonlinearHeatConductivityNoDeriv(PyObject *registry,
				       const std::string &name, int testno)
    : NonlinearHeatConductivityNoDeriv( registry, name ), testNo(testno) {};
  virtual ~TestNonlinearHeatConductivityNoDeriv() {};

protected:
  int testNo;
  virtual void nonlin_heat_flux(const Coord&,
				double time, double temperature,
				const DoubleVec &temperature_gradient,
				DoubleVec &heat_flux) const;
}; // TestNonlinearHeatConductivityNoDeriv


class TestNonlinearHeatConductivity : public NonlinearHeatConductivity {

public:
  TestNonlinearHeatConductivity(PyObject *registry,
				const std::string &name, int testno)
    : NonlinearHeatConductivity( registry, name ), testNo(testno) {};
  virtual ~TestNonlinearHeatConductivity() {};

protected:
  int testNo;
  virtual void nonlin_heat_flux(const Coord&,
				double time, double temperature,
				const DoubleVec &temperature_gradient,
				DoubleVec &heat_flux) const;
  virtual void nonlin_heat_flux_deriv_wrt_temperature(
			      const Coord&,
			      double time, double temperature,
			      const DoubleVec &temperature_gradient,
			      DoubleVec &heat_flux_deriv) const;
  virtual void nonlin_heat_flux_deriv_wrt_temperature_gradient(
			       const Coord&,
			       double time, double temperature,
			       const DoubleVec &temperature_gradient,
			       SmallMatrix &heat_flux_deriv) const;
}; // TestNonlinearHeatConductivity

#endif
