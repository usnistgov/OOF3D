// -*- C++ -*-
// $RCSfile: heatsource.C,v $
// $Revision: 1.6.4.2 $
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

// Heat source class functions

#include <oofconfig.h>
#include "common/coord.h"
#include "common/tostring.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/property/heatsource/heatsource.h"
#include "engine/fieldindex.h"
#include "engine/material.h"
#include "engine/property/orientation/orientation.h"
#include "engine/smallsystem.h"
#include "engine/nodalequation.h"
#include <iostream>
#include <fstream>
#include <string>



HeatSourceProp::HeatSourceProp(PyObject *reg,
			       const std::string &name, double qd)
  : EqnProperty(name,reg),
    qdot_(qd) {
    heat_flux = dynamic_cast<VectorFlux*>(Flux::getFlux("Heat_Flux"));
}

int HeatSourceProp::integration_order(const CSubProblem*, const Element*)
  const
{
  return 0;
}


void HeatSourceProp::force_value(const FEMesh *mesh, const Element *element,
				 const Equation *eqn,
				 const MasterPosition &masterpos,
				 double time,
				 SmallSystem *eqndata) const
{
  eqndata->force_vector_element(0) -= qdot_;
}
