// -*- C++ -*-
// $RCSfile: nonlinear_force_density.h,v $
// $Revision: 1.9.8.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:44 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef NONLINEAR_FORCE_DENSITY_H
#define NONLINEAR_FORCE_DENSITY_H

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/smallsystem.h"
#include <string>

class CSubProblem;
class Element;
class Equation;
class Flux;
class Material;
class FEMesh;
class Position;
class TwoVectorField;
class ThreeVectorField;
class SymmetricTensorFlux;
class ElementNodeIterator;
class SmallMatrix;
class DoubleVec;


class NonlinearForceDensityNoDeriv : public EqnProperty {
public:
  NonlinearForceDensityNoDeriv(PyObject *reg, const std::string &name);
  virtual ~NonlinearForceDensityNoDeriv() {}
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return false; }
  virtual void precompute(FEMesh*);
  virtual void force_value(const FEMesh*, const Element*, const Equation*,
			   const MasterPosition&, double time, SmallSystem*) const;
protected:
#if DIM==2
  TwoVectorField *displacement;
#elif DIM==3
  ThreeVectorField *displacement;
#endif
  SymmetricTensorFlux *stress_flux;

  virtual void nonlin_force_density(const Coord &coord, double time,
				    DoubleVec &displacement,
				    DoubleVec &result) const = 0;
}; // NonlinearForceDensityNoDeriv


class NonlinearForceDensity : public NonlinearForceDensityNoDeriv {
public:
  NonlinearForceDensity(PyObject *reg, const std::string &name)
    : NonlinearForceDensityNoDeriv( reg, name ) {};
  virtual ~NonlinearForceDensity() {}
  virtual void force_deriv_matrix(const FEMesh *mesh,
				  const Element  *element,
				  const Equation *eqn,
				  const ElementFuncNodeIterator &node,
				  const MasterPosition &point,	double time,
				  SmallSystem *eqndata) const;
protected:
  virtual void nonlin_force_density_deriv(const Coord &coord, double time,
					  DoubleVec &displacement,
					  SmallMatrix &result) const = 0;
};


class TestNonlinearForceDensityNoDeriv : public NonlinearForceDensityNoDeriv {
public:
  TestNonlinearForceDensityNoDeriv(PyObject *registry, const std::string &name,
				   int testno)
    : NonlinearForceDensityNoDeriv( registry, name ), testNo(testno) {};
  virtual ~TestNonlinearForceDensityNoDeriv() {};
protected:
  int testNo;
  virtual void nonlin_force_density(const Coord &coord, double time,
				    DoubleVec &displacement,
				    DoubleVec &result) const;
}; // TestNonlinearForceDensityNoDeriv


class TestNonlinearForceDensity : public NonlinearForceDensity {
public:
  TestNonlinearForceDensity(PyObject *registry, const std::string &name,
			    int testno)
    : NonlinearForceDensity( registry, name ), testNo(testno) {};
  virtual ~TestNonlinearForceDensity() {};
protected:
  int testNo;
  virtual void nonlin_force_density(const Coord &coord, double time,
				    DoubleVec &displacement,
				    DoubleVec &result) const;
  virtual void nonlin_force_density_deriv(const Coord &coord, double time,
					  DoubleVec &displacement,
					  SmallMatrix &result) const;
}; // TestNonlinearForceDensity

#endif
