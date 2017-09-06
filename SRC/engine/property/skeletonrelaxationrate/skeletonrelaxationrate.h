// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef SKELETONRELAXATIONRATE_H
#define SKELETONRELAXATIONRATE_H


#include "engine/property.h"
#include "engine/symmmatrix.h"
#include <string>

class Elasticity;
class Element;
class FEMesh;
class Flux;
class Material;
class Position;
class OutputVal;
class PropertyOutput;
class ScalarField;
class SymmetricTensorFlux;
class SmallSystem;

// Property analogous to plasticity.
// Its purpose is to expand/contract the skeleton
// element node positions, based on the quality of the mesh
// energy shape/homogeneity.

class SkeletonRelaxationRate : public FluxProperty {
  private:
  // Physical parameters.
  double gamma_;
  double alpha_;
  Elasticity *elasticity;	// pointer to this Material's Elasticity
  SymmetricTensorFlux *stress_flux;
  SymmMatrix3 shapetensor(const Element*) const;
public:
  SkeletonRelaxationRate(PyObject *registry, const std::string &nm,
		       double gamma, double alpha);
  virtual ~SkeletonRelaxationRate() {}
  virtual void cross_reference(Material*);
  virtual void precompute(FEMesh*);

  virtual void flux_offset(const FEMesh*, const Element*,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*) const;

  virtual int integration_order(const CSubProblem*, const Element*) const;

  double alpha() const { return alpha_; }
  double gamma() const {return gamma_;}
  virtual bool constant_in_space() const { return true; }
};

#endif	// SKELETONRELAXATIONRATE_H
