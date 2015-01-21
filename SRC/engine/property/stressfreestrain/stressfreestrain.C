// -*- C++ -*-
// $RCSfile: stressfreestrain.C,v $
// $Revision: 1.11.10.3 $
// $Author: langer $
// $Date: 2013/11/08 20:46:04 $

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
#include "engine/cstrain.h"
#include "engine/element.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/ooferror.h"
#include "engine/property/elasticity/cijkl.h"
#include "engine/property/elasticity/elasticity.h"
#include "engine/property/orientation/orientation.h"
#include "engine/property/stressfreestrain/stressfreestrain.h"
#include "engine/smallsystem.h"

StressFreeStrain::StressFreeStrain(PyObject *reg,
			 const std::string &nm)
  : FluxProperty(nm, reg)
{
  stress_flux = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}

int StressFreeStrain::integration_order(const CSubProblem*, const Element*el) const {
  return el->shapefun_degree();
}

void StressFreeStrain::flux_offset(const FEMesh *mesh, const Element *element,
				   const Flux *flux,
				   const MasterPosition &x,
				   double time,
				   SmallSystem *fluxdata)
  const
{
  if(*flux != *stress_flux) {
    throw ErrProgrammingError("Unexpected flux.", __FILE__, __LINE__);
  }
  const Cijkl modulus = elasticity->cijkl(mesh, element, x);
  SymmMatrix3 sfs = stressfreestrain(mesh, element, x);
  for(SymTensorIterator ij; !ij.end(); ++ij) {
    double &offset_el = fluxdata->offset_vector_element(ij);
    for(SymTensorIterator kl; !kl.end(); ++kl) {
      if(kl.diagonal()) {
	offset_el -= modulus(ij, kl)*sfs[kl];
      }
      else {
	offset_el -= 2.0*modulus(ij, kl)*sfs[kl];
      }
    }
  }
}

IsotropicStressFreeStrain::IsotropicStressFreeStrain(PyObject *registry,
						     const std::string &name,
						     double e)
  : StressFreeStrain(registry, name),
    e_(e)
{}

void IsotropicStressFreeStrain::cross_reference(Material *mat) {
  try {
    elasticity = dynamic_cast<Elasticity*>(mat->fetchProperty("Elasticity"));
  }
  catch (ErrNoSuchProperty&) {
    elasticity = 0;
    throw;
  }
}

void IsotropicStressFreeStrain::precompute(FEMesh *mesh) {
  StressFreeStrain::precompute(mesh);
  stressfreestrain_(0,0) = stressfreestrain_(1,1) = stressfreestrain_(2,2) = e_;
}

AnisotropicStressFreeStrain::AnisotropicStressFreeStrain(PyObject *registry,
					       const std::string &name,
					       SymmMatrix3 *e)
  : StressFreeStrain(registry, name),
    e_(*e),
    orientation(0)
{}

void AnisotropicStressFreeStrain::cross_reference(Material *mat) {
  try {
    elasticity = dynamic_cast<Elasticity*>(mat->fetchProperty("Elasticity"));
    orientation = dynamic_cast<OrientationPropBase*>
      (mat->fetchProperty("Orientation"));
  }
  catch (ErrNoSuchProperty&) {
    elasticity = 0;
    orientation = 0;
    throw;
  }
}

void AnisotropicStressFreeStrain::precompute(FEMesh*) {
  if(orientation && orientation->constant_in_space())
    stressfreestrain_ = e_.transform(orientation->orientation());
}

const SymmMatrix3
AnisotropicStressFreeStrain::stressfreestrain(const FEMesh *mesh,
					      const Element *elem,
					      const MasterPosition &pos)
  const
{
  if(orientation->constant_in_space())
    return stressfreestrain_;
  return e_.transform(orientation->orientation(mesh, elem, pos));
}

void StressFreeStrain::output(const FEMesh *mesh,
			      const Element *element,
			      const PropertyOutput *output,
			      const MasterPosition &pos,
			      OutputVal *data)
  const
{
  // Mostly copied from ThermalExpansion::output
  const std::string &outputname = output->name();
  if(outputname == "Strain") {
    const std::string *stype = output->getRegisteredParamName("type");
    SymmMatrix3 *sdata = dynamic_cast<SymmMatrix3*>(data);
    if(*stype == "Elastic")
      *sdata -= stressfreestrain(mesh, element, pos);
    delete stype;
  }
  if(outputname == "Energy") {
    // Energy looks strange, because we're doing two of the three
    // terms in a product of differences.  The full answer is
    // (1/2)Cijkl(e_ij-e0_ij)(e_kl-e0_kl), with e_ij the strain, and
    // e0_ij the stress-free strain.  But the elasticity property
    // independently contributes (1/2)Cijkl.e_ij.e_kl.  The remaining
    // terms are - Cijkl.e_ij.e0_kl + Cijkl.e0_ij.e0_kl.  In the code
    // below, "stress" refers to the product Cijkl.e0_ij.
    const std::string *etype = output->getEnumParam((char*) "etype");
    if(*etype == "Total" || *etype == "Elastic") {
      ScalarOutputVal *edata = dynamic_cast<ScalarOutputVal*>(data);
      const Cijkl modulus = elasticity->cijkl(mesh, element, pos);
      SymmMatrix3 strain;
      SymmMatrix3 sfs = stressfreestrain(mesh, element, pos);
      elasticity->geometricStrain(mesh, element, pos, &strain);
      SymmMatrix3 stress(modulus*sfs);
      double e = 0;
      for(int i=0; i<3; i++) {
	e += stress(i,i)*(-strain(i,i)+0.5*sfs(i,i));
	int j=(i+1)%3;
	e += 2*stress(i,j)*(-strain(i,j)+0.5*sfs(i,j));
      }
      *edata += e;
    }
    delete etype;
  }
}
