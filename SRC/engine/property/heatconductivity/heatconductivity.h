// -*- C++ -*-
// $RCSfile: heatconductivity.h,v $
// $Revision: 1.35.4.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:47 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// heat conductivity property

#ifndef HEATCONDUCTIVITY_H
#define HEATCONDUCTIVITY_H


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

class HeatConductivity : public FluxProperty {
public:
  HeatConductivity(PyObject *registry, const std::string &name);
  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*,
			   const MasterPosition&,
			   double time,
			   SmallSystem *) const;
  virtual void static_flux_value(const FEMesh*, const Element*,
				 const Flux*,
				 const MasterPosition&,
				 double time,
				 SmallSystem *) const;
  virtual void cross_reference(Material*) = 0;
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return true; }
  virtual const SymmMatrix3 conductivitytensor(const FEMesh*, const Element*,
					       const MasterPosition&) const = 0;
protected:
  SymmMatrix3  conductivitytensor_;
  ScalarField *temperature;
  VectorFlux  *heat_flux;
};


class IsoHeatConductivity : public HeatConductivity {
public:
  IsoHeatConductivity(PyObject *registry,
		      const std::string &name, double kappa);
  virtual void cross_reference(Material*) {}
  virtual void precompute(FEMesh*);
  virtual const SymmMatrix3 conductivitytensor(const FEMesh*, const Element*,
					       const MasterPosition&) const;
private:
  double kappa_;
};


class AnisoHeatConductivity : public HeatConductivity {
public:
  AnisoHeatConductivity(PyObject *registry, const std::string &name, SymmMatrix3 *kappa);
  virtual void cross_reference(Material*); // finds Orientation
  virtual void precompute(FEMesh*);
  virtual const SymmMatrix3 conductivitytensor(const FEMesh*, const Element*,
					       const MasterPosition&) const;
private:
  SymmMatrix3 kappa_;
  OrientationPropBase *orientation;
};

#endif	// HEATCONDUCTIVITY_H
