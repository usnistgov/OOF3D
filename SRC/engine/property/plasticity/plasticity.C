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
#include "engine/property/elasticity/cijkl.h"
#include "common/coord.h"
#include "common/threadstate.h"
#include "common/trace.h"
#include "engine/property/plasticity/plasticity.h"
#include "engine/IO/propertyoutput.h"
#include "engine/cstrain.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/indextypes.h"
#include "engine/material.h"
#include "engine/ooferror.h"
#include "engine/smallsystem.h"
#include "engine/property/orientation/orientation.h"


Plasticity::Plasticity(PyObject *reg, const std::string &name,
		       const Cijkl &c)
  : FluxProperty(name, reg), xtal_cijkl_(c), orientation(0)
{
  displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
  stress_flux = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}


void Plasticity::cross_reference(Material *mtl) {
  try {
    orientation = 
      dynamic_cast<OrientationPropBase*>(mtl->fetchProperty("Orientation"));
  }
  catch (ErrNoSuchProperty&) {
    // If fetchProperty failed, we have to ensure that an old pointer
    // value isn't still being stored.
    orientation = 0;
    throw;
  }
}

void Plasticity::precompute(FEMesh*) {
  // Do the orientation thing.
  // if(orientation && orientation->constant_in_space()) {
  //    lab_cijkl_ = xtal_cijkl_.transform(orientation->orientation());
  //    // Also do the constitutive rule.
  // }
}

void Plasticity::begin_element(const CSubProblem *c, const Element *e) {}

int Plasticity::integration_order(const CSubProblem *sp,
				  const Element *el) const {
  return el->shapefun_degree();
}


// Evaluates itself.  "Static" unclear in the context of
// an intrinsically quasistatic property.
void Plasticity::static_flux_value(const FEMesh *mesh,
				   const Element *element,
				   const Flux *flux,
				   const MasterPosition &mpt,
				   double time, SmallSystem *fluxdata)
  const
{
}


// Evaluates elasto-plastic derivatives of the stress flux wrt the
// displacement dofs.
void Plasticity::flux_matrix(const FEMesh *mesh,
			     const Element *element,
			     const ElementFuncNodeIterator&,
			     const Flux *flux,
			     const MasterPosition &mpt,
			     double time,
			     SmallSystem *fluxmtx)
  const
{
}
