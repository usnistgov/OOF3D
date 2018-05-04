// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// Plasticity property, v0.1.  This implements quasi-static crystal
// plasticity, and requires a fixed-step non-adaptive time-stepper
// and a large-deformation equation.

// Operationally speaking it works like a nonlinear elasticity, the
// way in which it contributes to the stiffness matrix is through the
// stress flux, but the stress derivatives are the elasto-plastic ones
// that take into account the additional yield that would occur if you
// incremented the displacements.  The plastic constitutive rule is a
// parameter to this object, not yet written.

// TODO: We might want to use a different property sub-class
// to ensure the right kind of equation does the derivatives.

#ifndef PLASTICITY_H
#define PLASTICITY_H

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/property/elasticity/cijkl.h"
#include <string>

// TODO: cijkl is in a different hierarchy, needs to be higher?
// Or, plasticity should be a sub-type of elasticity, logically
// speaking?

class CSubProblem;
class Element;
class ElementFuncNodeIterator;
class FEMesh;
class Flux;
class Material;
class OutputVal;
class Position;
class PropertyOutput;
class SymmetricTensorFlux;
class TwoVectorField;
class ThreeVectorField;
class SmallSystem;

class Plasticity : public FluxProperty {
public:
  Plasticity(PyObject *rg, const std::string &nm,
	     const Cijkl &c);
  virtual ~Plasticity() {}
  virtual void begin_element(const CSubProblem*, const Element*); 
  virtual void flux_matrix(const FEMesh *mesh,
			   const Element *element,
			   const ElementFuncNodeIterator &nu,
			   const Flux *flux,
			   const MasterPosition &x,
			   double time,
			   SmallSystem *fluxmtx) const;
  virtual void static_flux_value(const FEMesh*, const Element*,
				 const Flux*,
				 const MasterPosition&,
				 double time,
				 SmallSystem*) const;
  virtual int integration_order(const CSubProblem *, const Element*) const;
  virtual bool constant_in_space() const { return true; }
  virtual void precompute(FEMesh*);
  
  // Option: Crystallographic subclasses, later.
  const Cijkl cijkl(const FEMesh*, const Element*,
		    const MasterPosition&);

  
  // Outputs -- plastic strain at gpts, total strain, elastic strain...
  
protected:
  // TODO: 2D version?
  ThreeVectorField *displacement;
  SymmetricTensorFlux *stress_flux;
private:
  const Cijkl xtal_cijkl_;
  const Cijkl lab_cijkl_;
};

#endif // PLASTICITY_H
