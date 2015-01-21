// -*- C++ -*-
// $RCSfile: fruitproperty.h,v $
// $Revision: 1.8.8.1 $
// $Author: langer $
// $Date: 2014/09/27 22:35:14 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

// This file, along with fruitproperty.C, fruitproperty.swg, and
// strawberry.py, demonstrates how to add a new material property to
// OOF2.  The property being added is not meant to be used for serious
// scientific work.

#ifndef FRUITPROPERTY_H
#define FRUITPROPERTY_H

#include "engine/property.h"
#include "engine/symmmatrix.h"
#include <string>

class Element;
class ElementFuncNodeIterator;
class FEMesh;
class Flux;
class FluxData;
class MasterPosition;
class Material;
class OrientationProp;
class OutputVal;
class PropertyOutput;
class ScalarField;
class VectorFlux;

class FruitProperty : public Property {
private:
  SymmMatrix3 modulus;		// 3x3 symmetric matrix
  SymmMatrix3 lab_modulus;	// should this be a MATRIX_D?
  double coupling;
  ScalarField *strawberryField;
  VectorFlux *jamFlux;
  OrientationProp *orientation;
public:

  // Constructor.  The first two arguments must be PyObject* and const
  // std::string&.  The remaining arguments correspond to the "params"
  // list in the PropertyRegistration (see strawberry.py).  The C++
  // class underlying a TrigonalRank2Tensor is a SymmMatrix3.
  FruitProperty(PyObject *registration, const std::string &name,
		const SymmMatrix3 &modulus, double coupling);

  // The following virtual functions all have default no-op
  // definitions in property.h, so they can be omitted from Property
  // subclasses that don't need them.  This Property doesn't define
  // all of the available functions.  See the manual for a full
  // discussion of all of the functions.

  // cross_reference is called after the Property is added to a
  // Material.  It allows a Property to locate other Properties within
  // the same Material, with which it might need to share information.  
  virtual void cross_reference(Material*);

  // integration_order returns the polynomial degree of the Property's
  // contribution to the flux matrix and/or right hand side.
  virtual int integration_order(const FEMesh*, const Element*) const;

  // precompute is called before beginning the construction of the
  // finite element stiffness matrix or right hand side vector.  It
  // gives the Property a chance to compute and store
  // element-independent quantities.
  virtual void precompute(FEMesh*);

  // is_symmetric indicates whether stiffness matrices formed by this
  // Property can be symmetrized.  See the conjugatePair
  // documentation.  The default is_symmetric function returns false
  // because symmetrizing an asymmetric matrix will lead to wrong
  // answers, whereas not symmetrizing a potentially symmetric one
  // will only lead to inefficiencies.
  virtual bool is_symmetric(const FEMesh*) const { return true; }

  // constant_in_space indicates whether the property depends
  // explicitly on the position at which it is evaluated.
  virtual bool constant_in_space() const { return true; }

  // The fluxmatrix function computes this Property's contribution to
  // fluxes when the finite element stiffness matrix is being built.
  virtual void fluxmatrix(const FEMesh*, const Element*,
			  const ElementFuncNodeIterator&,
			  const Flux*, FluxData*,
			  const MasterPosition&) const;


//   // output computes the quantities listed in the
//   // PropertyRegistration's "outputs" list.
//   virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
// 		      const MasterPosition&, OutputVal*) const;
};



#endif // FRUITPROPERTY_H
