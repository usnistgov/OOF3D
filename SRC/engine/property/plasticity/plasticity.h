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

// Crystal plasticity classes are richer than that, though, they also
// know the crystallography, and can construct the Schmid tensors for
// common crystal classes.

// The base class knows the Cijkl, and that there are slip systems,
// derived classes know the specific slip systems, and the plastic
// data objects which have the gausspoint-specific, per-time-step
// information about the accumulated slip on each of these systems.

// Constitutive models know how to compute the slip increment given
// the stress, and have additional per-time-step gausspoint-specific
// data about the state of various local variables, like hardening.

// At the moment, there's no top-level "generic" way of doing this,
// but there probably should be.  That's a TODO.

// TODO: We might want to use a different property sub-class
// to ensure the right kind of equation does the derivatives.


#ifndef PLASTICITY_H
#define PLASTICITY_H

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/element.h"
#include "engine/property/elasticity/cijkl.h"
#include "common/pythonexportable.h"
#include "common/smallmatrix.h"
#include "engine/smallmatrix3.h"
#include <string>
#include <map>

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
class SmallGeometricSystem;
class PlasticConstitutiveRule;
class SmallMatrix;
class SmallMatrix3;


class OrientationPropBase;

class PlasticConstitutiveRule;

class Plasticity : public FluxProperty {
public:
  Plasticity(PyObject *rg, const std::string &nm,
	     const Cijkl &c, PlasticConstitutiveRule *r, const int slips);
  virtual ~Plasticity() {}
  virtual void begin_element_matrix(const CSubProblem*, double time,
				    const Element*); 
  virtual void flux_matrix(const FEMesh *mesh,
			   const Element *element,
			   const ElementFuncNodeIterator &nu,
			   const Flux *flux,
			   const MasterPosition &x,
			   double time,
			   SmallGeometricSystem *fluxmtx) const;
  virtual void static_flux_value(const FEMesh*, const Element*,
				 const Flux*,
				 const MasterPosition&,
				 double time,
				 SmallSystem*) const;
  virtual int integration_order(const CSubProblem *, const Element*) const;
  virtual bool constant_in_space() const { return true; }
  virtual void precompute(FEMesh*);
  virtual void cross_reference(Material*);
  
  const Cijkl cijkl(const FEMesh*, const Element*,
		    const MasterPosition&);

  // Outputs -- plastic strain at gpts, total strain, elastic strain...
  virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*) const;
  
protected:
  FEMesh *mesh; // Set in precompute, used in begin_element_matrix.
  const int nslips;
  // TODO: 2D version?
  ThreeVectorField *displacement;
  SymmetricTensorFlux *stress_flux;
  SmallMatrix3 *_normalized_outer_product(double*, double*);
  SmallMatrix3 *_rotate_schmid_tensor(SmallMatrix3*, const COrientation *);

  const OrientationPropBase *orientation;
  const Cijkl xtal_cijkl_;
  Cijkl lab_cijkl_;
  std::vector<SmallMatrix3*> xtal_schmid_tensors;
  std::vector<SmallMatrix3*> lab_schmid_tensors;
  PlasticConstitutiveRule *rule;
};


class FCCPlasticity : public Plasticity {
public:
  FCCPlasticity(PyObject *rg, const std::string &nm,
		const Cijkl &c, PlasticConstitutiveRule *rule);
  virtual ~FCCPlasticity() {}
  //
};


#endif
