// -*- C++ -*-
// $RCSfile: thermalexpansion.h,v $
// $Revision: 1.32.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:46:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef THERMALEXPANSION_H
#define THERMALEXPANSION_H

// Base class for Thermal Expansion Properties

#include "engine/property.h"
#include "engine/property.h"
#include "engine/symmmatrix.h"
#include <string>

class Elasticity;
class Element;
class FEMesh;
class Flux;
class Material;
class Position;
class OrientationPropBase;
class OutputVal;
class PropertyOutput;
class ScalarField;
class SmallSystem;
class SymmetricTensorFlux;

class ThermalExpansion : public FluxProperty {
protected:
  // Physical parameters.
  double tzero_;
  Elasticity *elasticity;	// pointer to this Material's Elasticity
  ScalarField *temperature;
  SymmetricTensorFlux *stress_flux;
  SymmMatrix3 expansiontensor_; //lab reference system tensor
public:
  ThermalExpansion(PyObject *registry,
		   const std::string &nm,
		   double t0);
  virtual ~ThermalExpansion() {}
  virtual void cross_reference(Material*) = 0;
  virtual void precompute(FEMesh*);
  virtual bool constant_in_space() const { return true; }

  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*) const;
  virtual void flux_offset(const FEMesh*, const Element*,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*) const;
  virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*) const;

  virtual int integration_order(const CSubProblem*, const Element*) const;

  virtual bool is_symmetric_K(const CSubProblem*) const;

  // Returns the lab-frame modulus.
  virtual const SymmMatrix3 expansiontensor(const FEMesh*, const Element*,
				    const MasterPosition&) const = 0;
};

class IsotropicThermalExpansion: public ThermalExpansion {
public:
  IsotropicThermalExpansion(PyObject *registry,
			    const std::string &name,
			    double alpha,
			    double t0);
  virtual void cross_reference(Material*);
  virtual void precompute(FEMesh*);
  virtual const SymmMatrix3 expansiontensor(const FEMesh*, const Element*,
					     const MasterPosition&) const;
private:
  double alpha_;
};

class AnisotropicThermalExpansion: public ThermalExpansion {
public:
  AnisotropicThermalExpansion(PyObject *registry,
			      const std::string &nm,
			      SymmMatrix3 *alpha, double t0);
  virtual void cross_reference(Material*); // finds Orientation
  virtual void precompute(FEMesh*);
  virtual const SymmMatrix3 expansiontensor(const FEMesh*, const Element*,
					     const MasterPosition&) const;
private:
  SymmMatrix3 alpha_;
  OrientationPropBase *orientation;
};

#endif	// THERMALEXPANSION_H
