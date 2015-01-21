// -*- C++ -*-
// $RCSfile: nonlinear_heat_source.h,v $
// $Revision: 1.5.8.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:54 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef NONLINEAR_HEAT_SOURCE_H
#define NONLINEAR_HEAT_SOURCE_H


#include "common/coord.h"
#include "engine/property.h"
#include "engine/symmmatrix.h"
#include <string>

class Element;
class Material;
class FEMesh;
class OrientationPropBase;
class SmallSystem;
class ScalarField;
class VectorFlux;
class ElementNodeIterator;


class NonlinearHeatSourceNoDeriv : public EqnProperty {
public:
  NonlinearHeatSourceNoDeriv(PyObject *registry, const std::string &name);
  virtual ~NonlinearHeatSourceNoDeriv() {}
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return false; }
  virtual void force_value(const FEMesh*, const Element*,
			   const Equation*,
			   const MasterPosition&,
			   double time,
			   SmallSystem *) const;
protected:
  ScalarField *temperature;
  VectorFlux  *heat_flux;

  virtual double nonlin_heat_source(double x, double y, double z,
				    double time, double temperature) const = 0;
}; // NonlinearHeatSourceNoDeriv


class NonlinearHeatSource : public NonlinearHeatSourceNoDeriv {
public:
  NonlinearHeatSource(PyObject *registry, const std::string &name)
    : NonlinearHeatSourceNoDeriv(registry, name) {};
  virtual ~NonlinearHeatSource() {}
  virtual void force_deriv_matrix(const FEMesh *mesh,
				  const Element *el,
				  const Equation *eqn,
				  const ElementFuncNodeIterator &j,
				  const MasterPosition &pt,
				  double time,
				  SmallSystem *eqndata ) const;
protected:
  virtual double nonlin_heat_source_deriv_wrt_temperature(
                                    double x, double y, double z,
				    double time, double temperature) const = 0;
}; // NonlinearHeatSource


class TestNonlinearHeatSourceNoDeriv : public NonlinearHeatSourceNoDeriv {
public:
  TestNonlinearHeatSourceNoDeriv(PyObject *registry, const std::string &name,
				 int testno)
    : NonlinearHeatSourceNoDeriv( registry, name), testNo(testno) {};
  virtual ~TestNonlinearHeatSourceNoDeriv() {};
protected:
  int testNo;
  virtual double nonlin_heat_source(double x, double y, double z,
				    double time, double temperature) const;
}; // TestNonlinearHeatSourceNoDeriv


class TestNonlinearHeatSource : public NonlinearHeatSource {
public:
  TestNonlinearHeatSource(PyObject *registry, const std::string &name, int testno)
    : NonlinearHeatSource( registry, name ), testNo(testno) {};
  virtual ~TestNonlinearHeatSource() {};
protected:
  int testNo;
  virtual double nonlin_heat_source(double x, double y, double z,
				    double time, double temperature) const;
  virtual double nonlin_heat_source_deriv_wrt_temperature(
                                    double x, double y, double z,
				    double time, double temperature) const;

}; // TestNonlinearHeatSource

#endif
