// -*- C++ -*-
// $RCSfile: pyroelectricity.h,v $
// $Revision: 1.10.10.3 $
// $Author: langer $
// $Date: 2013/11/08 20:46:01 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef PYROELECTRICITY_H
#define PYROELECTRICITY_H

// Base class for PiezoElectricity Properties

#include "common/doublevec.h"
#include "engine/property.h"

#include <string>

class Elasticity;
class PiezoElectricity;
class ThermalExpansion;
class Element;
class Flux;
class Material;
class Position;
class OrientationPropBase;
class OutputVal;
class PropertyOutput;
class ScalarField;
class SmallSystem;
class SymmetricTensorFlux;
class VectorFlux;

// Pyroelectricity is dependent on temperature, and contributes to the
// polarization flux.  The coefficient is the constant-strain modulus,
// and is a three-vector, and works in the obvious way.  Users may
// specify the constant-stress modulus.  In this case, the
// constant-strain modulus can be deduced from the constant-stress
// modulus by subtracting the product of the piezoelectric d tensor,
// the isothermal elastic constants, and the strain thermal expansion
// coefficient.  If any of these are zero, then the constant stress
// and constant strain pyroelectric moduli are equal.

class PyroElectricity : public FluxProperty {
protected:
  // Physical parameters.
  Elasticity *elasticity;	// pointer to this Material's Elasticity
  PiezoElectricity *piezoelectricity;
  ThermalExpansion *thermalexpansion;
  ScalarField *temperature;
  VectorFlux *total_polarization;
  OrientationPropBase *orientation;
  DoubleVec modulus;
  DoubleVec lab_modulus;  // Constant-stress modulus.
  double tzero;
  std::string coefficient_type;
  void set_effective_modulus(const FEMesh*, const Element*,
			     const MasterPosition&) const;
private:
  mutable DoubleVec effective_modulus;
  mutable bool modulus_ok;
public:
  PyroElectricity(PyObject *registry,
		  const std::string &nm,
		  double px, double py, double pz, double t0,
		  std::string *ctype);
  virtual ~PyroElectricity() {}
  virtual void cross_reference(Material*);
  virtual void precompute(FEMesh*);

  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*) const;


  virtual void flux_offset(const FEMesh*, const Element*,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem *) const;

  virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*) const;

  virtual bool constant_in_space() const { return true; }
  virtual int integration_order(const CSubProblem*, const Element*) const;

  virtual bool is_symmetric_K(const CSubProblem*) const;

};

#endif	// PYROELECTRICITY_H
