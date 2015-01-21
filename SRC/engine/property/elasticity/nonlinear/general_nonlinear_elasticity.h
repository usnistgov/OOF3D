// -*- C++ -*-
// $RCSfile: general_nonlinear_elasticity.h,v $
// $Revision: 1.11.8.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:35 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef GENERAL_NONLINEAR_ELASTICITY_H
#define GENERAL_NONLINEAR_ELASTICITY_H

#include <oofconfig.h>

#include "engine/property.h"

#include <Python.h>
#include <string>

class CSubProblem;
class DoubleVec;
class Element;
class ElementNodeIterator;
class FEMesh;
class Flux;
class Material;
class OutputVal;
class Position;
class PropertyOutput;
class SmallMatrix;
class SmallTensor3;
class SmallTensor4;
class SmallSystem;
class SymmetricTensorFlux;
class ThreeVectorField;
class TwoVectorField;



class GeneralNonlinearElasticityNoDeriv : public FluxProperty {
public:
  GeneralNonlinearElasticityNoDeriv(PyObject *registry, const std::string &name);
  virtual ~GeneralNonlinearElasticityNoDeriv() {}
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return false; }
  virtual void static_flux_value(const FEMesh*, const Element*,
				 const Flux*,
				 const MasterPosition&,
				 double time,
				 SmallSystem *) const;
protected:
#if DIM==2
  TwoVectorField *displacement;
#elif DIM==3
  ThreeVectorField *displacement;
#endif
  SymmetricTensorFlux *stress_flux;

  virtual void nonlin_stress(double x, double y, double z,
			     double time, DoubleVec &displacement,
			     SmallMatrix &dispGrad,
			     SmallMatrix &stress) const = 0;

}; // GeneralNonlinearElasticityNoDeriv


class GeneralNonlinearElasticity : public GeneralNonlinearElasticityNoDeriv {
public:
  GeneralNonlinearElasticity(PyObject *registry, const std::string &name)
    : GeneralNonlinearElasticityNoDeriv( registry, name ) {};
  virtual ~GeneralNonlinearElasticity() {}
  virtual void flux_matrix(const FEMesh *mesh,
			   const Element *element,
			   const ElementFuncNodeIterator &nu,
			   const Flux *flux,
			   const MasterPosition &x,
			   double time,
			   SmallSystem *fluxmtx) const;
protected:
  virtual void nonlin_stress_deriv_wrt_displacement(
                             double x, double y, double z,
			     double time, DoubleVec &displacement,
			     SmallMatrix &dispGrad,
			     SmallTensor3 &stress_deriv) const = 0;

  virtual void nonlin_stress_deriv_wrt_displacement_gradient(
                             double x, double y, double z,
			     double time, DoubleVec &displacement,
			     SmallMatrix &dispGrad,
			     SmallTensor4 &stress_deriv) const = 0;

}; // GeneralNonlinearElasticity

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


class TestGeneralNonlinearElasticityNoDeriv : public GeneralNonlinearElasticityNoDeriv {

public:
  TestGeneralNonlinearElasticityNoDeriv(PyObject *registry,
					const std::string &name, int testno)
    : GeneralNonlinearElasticityNoDeriv( registry, name ), testNo(testno) {};
  virtual ~TestGeneralNonlinearElasticityNoDeriv() {}

protected:
  int testNo;
  virtual void nonlin_stress(double x, double y, double z, double time,
			     DoubleVec &displacement,
			     SmallMatrix &dispGrad,
			     SmallMatrix &stress) const;
}; // TestGeneralNonlinearElasticityNoDeriv


class TestGeneralNonlinearElasticity : public GeneralNonlinearElasticity{

public:
  TestGeneralNonlinearElasticity(PyObject *registry,
				 const std::string &name, int testno)
    : GeneralNonlinearElasticity(registry, name), testNo(testno) {};
  virtual ~TestGeneralNonlinearElasticity() {};

protected:
  int testNo;
  virtual void nonlin_stress(double x, double y, double z, double time,
			     DoubleVec &displacement,
			     SmallMatrix &dispGrad,
			     SmallMatrix &stress) const;
  virtual void nonlin_stress_deriv_wrt_displacement(
                             double x, double y, double z, double time,
			     DoubleVec &displacement,
			     SmallMatrix &dispGrad,
			     SmallTensor3 &stress_deriv) const;
  virtual void nonlin_stress_deriv_wrt_displacement_gradient(
                             double x, double y, double z, double time,
			     DoubleVec &displacement,
			     SmallMatrix &dispGrad,
			     SmallTensor4 &stress_deriv) const;

}; // TestGeneralNonlinearElasticity

#endif
