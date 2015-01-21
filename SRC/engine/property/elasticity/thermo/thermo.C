// -*- C++ -*-
// $RCSfile: thermo.C,v $
// $Revision: 1.22.10.2 $
// $Author: fyc $
// $Date: 2014/07/29 21:21:55 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/property/elasticity/thermo/thermo.h"
#include "engine/element.h"

// Coef's.  The idea is that the shear modulus is going to be 
// mu0 + alpha*(T-t0), i.e. varies with slope alpha relative to 
// reference temperature t0.  In principle, could be arbitrarily
// complex, of course.
ThermoElasticityProp::ThermoElasticityProp(PyObject *registry,
					   const std::string &nm, 
					   Cijkl *cijkl,
					   double t0, double alpha)
  : Elasticity(nm, registry),
    cijkl_(*cijkl),
    tzero_(t0),
    dmudt_(alpha)
{
  temperature = dynamic_cast<ScalarField*>(Field::getField("Temperature"));
}

const Cijkl ThermoElasticityProp::cijkl(const FEMesh *mesh, const Element *e, 
				    const MasterPosition &x) const {
  // Get local temperature
  //* TODO OPT: This is baroque and may be slow.  Make a specialized
  //* function for getting the value of a scalar field. temperature(e, x)?
  const OutputValue tfield = e->outputField(mesh, *temperature, x);
  const ScalarOutputVal *tval =
    dynamic_cast<const ScalarOutputVal*>(tfield.valuePtr());
  double temp = tval->value();

  Cijkl modulus;
  // Because temperature variation of modulus is defined in terms
  // of lambda and mu, we have to convert to that representation.

  double lambda = cijkl_(0,0);
  double mu = (cijkl_(0,0)-cijkl_(0,1))/2.0 + dmudt_*(temp-tzero_);

  modulus.clear();
  // Construct temperature-dependent modulus from lambda and mu.
  modulus(0,0) = modulus(1,1) = modulus(2,2) = lambda+2.0*mu;
  modulus(0,1) = modulus(0,2) = modulus(1,2) = lambda;
  modulus(3,3) = modulus(4,4) = modulus(5,5) = mu;
  // 
  return modulus;
}
