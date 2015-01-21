// -*- C++ -*-
// $RCSfile: heatsource.h,v $
// $Revision: 1.4.10.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// Heat source property classes

#ifndef HEATSOURCE_H
#define HEATSOURCE_H


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


// Constant heat source

class HeatSourceProp : public EqnProperty {
private:
  double qdot_; // external heat dumped in per unit area per unit time.
protected:
  VectorFlux *heat_flux;
public:
  HeatSourceProp(PyObject *registry, const std::string &name, double qd);
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual void force_value(const FEMesh*, const Element*,
			   const Equation*,
			   const MasterPosition&,
			   double time,
			   SmallSystem *) const;
  virtual bool constant_in_space() const { return true; }
};

#endif
