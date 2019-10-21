// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#ifndef VISCOELASTICITY_H
#define VISCOELASTICITY_H

#include <oofconfig.h>
#include "engine/property/elasticity/cijkl.h"
#include "engine/property.h"
#include <string>

class CSubProblem;
class Element;
class ElementFuncNodeIterator;
class Flux;
class FEMesh;
class MasterPosition;
class SmallSystem;
class TwoVectorField;
class ThreeVectorField;
class SymmetricTensorFlux;

// TODO 3.1: Add all symmetries. Probably to be done later on.

class ViscoElasticityProp : public FluxProperty {
private:
  Cijkl g_ijkl;
#if DIM==2
  TwoVectorField *displacement;
#elif DIM==3
  ThreeVectorField *displacement;
#endif	// DIM==3
  SymmetricTensorFlux *stress_flux;
public:
  ViscoElasticityProp(PyObject *registry, const std::string &name, Cijkl* g);
  virtual ~ViscoElasticityProp() {}
  virtual void flux_matrix(const FEMesh *mesh,
			   const Element *element,
			   const ElementFuncNodeIterator &nu,
			   const Flux *flux,
			   const MasterPosition &x,
			   double time,
			   SmallSystem *fluxmtx) const;
  virtual int integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return true; }
  virtual void output(FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*);
};

#endif	// VISCOELASTICITY_H
