// -*- C++ -*-
// $RCSfile: thermo.h,v $
// $Revision: 1.13.18.2 $
// $Author: fyc $
// $Date: 2014/07/29 21:21:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef THERMOELASTICITY_H
#define THERMOELASTICITY_H

#include "engine/property/elasticity/elasticity.h"
#include "engine/property/elasticity/cijkl.h"
#include <string>

class ScalarField;

// TODO 3.1: Add symmetries.  This isn't a real property anyway.

class ThermoElasticityProp : public Elasticity {
private:
  Cijkl cijkl_;
  double tzero_;   // Temperature at which mu is unchanged.
  double dmudt_;   // Change in mu per unit change in T.
public:
  ThermoElasticityProp(PyObject *registry, const std::string &name, 
		       Cijkl *c, double tzero, double dmudt);
  virtual ~ThermoElasticityProp() {}
  const Cijkl cijkl(const FEMesh*, const Element*, const MasterPosition&) const;

protected:
  ScalarField *temperature;
};

#endif	// THERMOELASTICITY_H
