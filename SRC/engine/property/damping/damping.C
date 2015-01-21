// -*- C++ -*-
// $RCSfile: damping.C,v $
// $Revision: 1.3.10.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:25 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/property/damping/damping.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/smallsystem.h"

IsotropicDampingProp::IsotropicDampingProp(PyObject *registration,
					   const std::string &name,
					   double coeff)
  : EqnProperty(name, registration),
    coeff(coeff)
{}

void IsotropicDampingProp::precompute(FEMesh *mesh) {
  displacement = Field::getField("Displacement");
}

void IsotropicDampingProp::first_time_deriv_matrix(
			 const FEMesh *mesh,
			 const Element *lmnt,
			 const Equation *eqn,
			 const ElementFuncNodeIterator &eni,
			 const MasterPosition &mpos,
			 double time,
			 SmallSystem *eqndata)
  const
{
  double shapeFuncVal = eni.shapefunction(mpos);
  for(IteratorP ell = displacement->iterator(ALL_INDICES); !ell.end(); ++ell) {
    for(IteratorP eqncomp = eqn->iterator(); !eqncomp.end(); ++eqncomp) {
      eqndata->damping_matrix_element(eqncomp, displacement, ell, eni)
	-= coeff * shapeFuncVal;
    }
  }
}

int IsotropicDampingProp::integration_order(const CSubProblem*, const Element*) 
  const 
{
  return 1;
}
