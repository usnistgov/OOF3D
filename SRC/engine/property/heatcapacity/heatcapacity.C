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
#include "engine/IO/propertyoutput.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/property/heatcapacity/heatcapacity.h"
#include "engine/smallsystem.h"


HeatCapacityProp::HeatCapacityProp(PyObject *registration,
				   const std::string &name,
				   double cv)
  : EqnProperty(name, registration), cv_(cv)
{}

void HeatCapacityProp::precompute(FEMesh *mesh) {
  temperature = Field::getField("Temperature");
}

void HeatCapacityProp::first_time_deriv_matrix(const FEMesh *mesh,
					       const Element *lmnt,
					       const Equation *eqn,
					       const ElementFuncNodeIterator &eni,
					       const MasterPosition &mpos,
					       double time,
					       SmallSystem *eqdata) const {

  // Optional -- check that the equation is the right one.
  double shapeFuncVal = eni.shapefunction( mpos );
  for(IteratorP eqncomp = eqn->iterator(); !eqncomp.end(); ++eqncomp) {
    eqdata->damping_matrix_element(eqncomp, temperature, eqncomp, eni) += \
      cv_ * shapeFuncVal;
  }
}

int HeatCapacityProp::integration_order(const CSubProblem* subp,
				       const Element *lmnt) const {
  return 1;
}

void HeatCapacityProp::output(FEMesh *mesh,
			      const Element *element,
			      const PropertyOutput *output,
			      const MasterPosition &pos,
			      OutputVal *data)
{
  const std::string &outputname = output->name();
  if(outputname == "Material Constants:Thermal:Heat Capacity") {
    ScalarOutputVal *sdata = dynamic_cast<ScalarOutputVal*>(data);
    *sdata = cv_;
  }
}
