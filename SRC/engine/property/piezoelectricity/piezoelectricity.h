// -*- C++ -*-
// $RCSfile: piezoelectricity.h,v $
// $Revision: 1.25.4.1 $
// $Author: langer $
// $Date: 2013/11/08 20:46:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef PIEZOELECTRICITY_H
#define PIEZOELECTRICITY_H

// Base class for PiezoElectricity Properties

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/property.h"
#include "engine/symmmatrix.h"
#include "engine/rank3tensor.h"
#include <string>

class Elasticity;
class Element;
class Flux;
class Material;
class Position;
class TwoVectorField;
class ThreeVectorField;
class OrientationPropBase;
class OutputVal;
class PropertyOutput;
class ScalarField;
class SmallSystem;
class SymmetricTensorFlux;
class VectorFlux;

class PiezoElectricity : public FluxProperty {
protected:
  // Physical parameters.
  Elasticity *elasticity;	// pointer to this Material's Elasticity
#if DIM==2
  TwoVectorField *displacement;
#elif DIM==3
  ThreeVectorField *displacement;
#endif	// DIM==3
  SymmetricTensorFlux *stress_flux;
  ScalarField *voltage;
  VectorFlux *total_polarization;
  Rank3Tensor _dijkLab; //lab reference system piezoelectric tensor
public:
  PiezoElectricity(PyObject *registry,
		   const std::string &nm);
  virtual ~PiezoElectricity() {}
  virtual void cross_reference(Material*) = 0;
  virtual void precompute(FEMesh*);

  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem*) const;


  virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*) const;

  virtual bool constant_in_space() const { return true; }
  virtual int integration_order(const CSubProblem*, const Element*) const;

  virtual const Rank3Tensor dijk(const FEMesh*, const Element*,
				 const MasterPosition&) const=0;

};

/*
  Strictly speaking, all piezoelectrics are anisotropic;
  however, IsotropicPiezoelectricity was added in case
  a user/developer requires it.
*/

class IsotropicPiezoElectricity: public PiezoElectricity {
public:
  IsotropicPiezoElectricity(PyObject *registry,
			    const std::string &name,
			    double d);
  virtual void cross_reference(Material*);
  virtual void precompute(FEMesh*);
  virtual const Rank3Tensor dijk(const FEMesh*, const Element*,
				 const MasterPosition&) const
  {
    return _dijkLab;
  }

private:
  double _dijkValue;
};

class AnisotropicPiezoElectricity: public PiezoElectricity {
public:
  AnisotropicPiezoElectricity(PyObject *registry,
			      const std::string &nm,
			      Rank3Tensor *piezoTensor);
  virtual void cross_reference(Material*); // finds Orientation
  virtual void precompute(FEMesh*);
  virtual const Rank3Tensor dijk(const FEMesh*, const Element*,
				 const MasterPosition&) const;
  // Argument-free retrieval function for the modulus -- used by the
  // testing code.  It is the responsibility of the caller to ensure
  // that precompute has already been called before retrieving this
  // object.
  const Rank3Tensor dijk() const {
    return _dijkLab;
  }
private:
  Rank3Tensor _dijkValue;
  OrientationPropBase *orientation;
};

#endif	// PIEZOELECTRICITY_H
