// -*- C++ -*-
// $RCSfile: elasticity.h,v $
// $Revision: 1.25.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:28 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef ELASTICITY_H
#define ELASTICITY_H

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/property/elasticity/cijkl.h"
#include <string>

class CSubProblem;
class Element;
class ElementNodeIterator;
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


class Elasticity : public FluxProperty {
public:
  Elasticity(const std::string &name, PyObject *registry);
  virtual ~Elasticity() {}
  virtual void precompute(FEMesh*);
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
				 SmallSystem *) const;
  virtual int integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return true; }

  // elastic modulus to be defined in subclasses
  virtual const Cijkl cijkl(const FEMesh*, const Element*,
			    const MasterPosition&) const = 0;

  virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*) const;

  virtual void geometricStrain(const FEMesh*, const Element*,
			       const MasterPosition&, SymmMatrix3*) const;
protected:
#if DIM==2
  TwoVectorField *displacement;
#elif DIM==3
  ThreeVectorField *displacement;
#endif
  SymmetricTensorFlux *stress_flux;
};


#endif	// ELASTICITY_H
