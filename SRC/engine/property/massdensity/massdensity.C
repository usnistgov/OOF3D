// -*- C++ -*-
// $RCSfile: massdensity.C,v $
// $Revision: 1.28.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:58 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include "engine/property/massdensity/massdensity.h"
#include "engine/smallsystem.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"


MassDensityProp::MassDensityProp(PyObject *registration,
				 const std::string &name,
				 double rho)
  : EqnProperty(name, registration), rho_(rho)
{}

void MassDensityProp::precompute(FEMesh *mesh) {
  disp = Field::getField("Displacement");
}

void MassDensityProp::second_time_deriv_matrix(const FEMesh *mesh,
					       const Element *lmnt,
					       const Equation *eqn,
					       const ElementFuncNodeIterator &eni,
					       const MasterPosition &mpos,
					       double time,
					       SmallSystem *eqdata) const {

  // Optional -- check that the equation is the right one.
  double shapeFuncVal = eni.shapefunction(mpos);
  for(IteratorP component = eqn->iterator(); !component.end(); ++component) {
    eqdata->mass_matrix_element(component, disp, component, eni) -= rho_ * shapeFuncVal;
  }
}

int MassDensityProp::integration_order(const CSubProblem* subp,
				       const Element *lmnt) const {
  return 1;
}

