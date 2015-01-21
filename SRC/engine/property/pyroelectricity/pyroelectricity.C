// -*- C++ -*-
// $RCSfile: pyroelectricity.C,v $
// $Revision: 1.13.10.5 $
// $Author: langer $
// $Date: 2013/11/08 20:46:01 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#include "common/coord.h"
#include "engine/ooferror.h"
#include "engine/fieldindex.h"
#include "engine/symmmatrix.h"
#include "engine/rank3tensor.h"
#include "engine/IO/propertyoutput.h"
#include "engine/celectricfield.h"
#include "engine/cstrain.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/equation.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/property/thermalexpansion/thermalexpansion.h"
#include "engine/property/elasticity/cijkl.h"
#include "engine/property/elasticity/elasticity.h"
#include "engine/property/orientation/orientation.h"
#include "engine/property/piezoelectricity/piezoelectricity.h"
#include "engine/property/pyroelectricity/pyroelectricity.h"
#include "engine/smallsystem.h"

PyroElectricity::PyroElectricity(PyObject *reg,
				 const std::string &nm,
				 double px, double py, double pz,
				 double t0,
				 std::string *ctype)
  : FluxProperty(nm,reg), elasticity(0), piezoelectricity(0),
    thermalexpansion(0), orientation(0), modulus(3),
    lab_modulus(3), tzero(t0), coefficient_type(*ctype),
    effective_modulus(0), modulus_ok(false)
{
  modulus[0] = px;
  modulus[1] = py;
  modulus[2] = pz;
  temperature=dynamic_cast<ScalarField*>(Field::getField("Temperature"));
  total_polarization =
    dynamic_cast<VectorFlux*>(Flux::getFlux("Total_Polarization"));
}


void PyroElectricity::cross_reference(Material *mat) {
  //  All of the cross-referencing properties that we require are
  //  actually optional, so if they're not found, we have to be
  //  careful to catch the NoSuchProperty exception, and not allow it
  //  to propagate to our caller.  Otherwise, the caller will
  //  invalidate the material.
  try {
    orientation = dynamic_cast<OrientationPropBase*>
      (mat->fetchProperty("Orientation"));
  }
  catch(ErrNoSuchProperty&) {
    orientation=0;
  }

  try {
    elasticity = dynamic_cast<Elasticity*>(mat->fetchProperty("Elasticity"));
    piezoelectricity = dynamic_cast<PiezoElectricity*>
      (mat->fetchProperty("PiezoElectricity"));
    thermalexpansion = dynamic_cast<ThermalExpansion*>
      (mat->fetchProperty("ThermalExpansion"));

  }
  catch(ErrNoSuchProperty&) {
    elasticity=0;
    piezoelectricity=0;
    thermalexpansion=0;
  }
}

void PyroElectricity::precompute(FEMesh*) {
  modulus_ok = false;
  if(orientation!=0) {
    if(orientation->constant_in_space())
      lab_modulus = orientation->orientation()->rotation()*modulus;
  }
  else				// no orientation specified
    lab_modulus = modulus;
}

int PyroElectricity::integration_order(const CSubProblem *subproblem,
					const Element *el) const {
  return el->shapefun_degree();
}


void PyroElectricity::set_effective_modulus(const FEMesh *mesh,
					    const Element *el,
					    const MasterPosition&pos) const {

  if(orientation && !orientation->constant_in_space()) {
    effective_modulus =
      orientation->orientation(mesh, el, pos)->rotation()*modulus;
  }
  else
    effective_modulus = lab_modulus;
  // In the constant-stress case, we have to convert the effective
  // modulus to the constant-strain case, which is what OOF actually
  // uses.  The string literal is not arbitrary, it must match the
  // constant-stress enum entry in pyroelectricity.spy.

  if(coefficient_type=="Constant stress") {

    // Convert the lab_modulus, constant-stress version, into the
    // constant-strain version that we want.
    if((elasticity!=0)&&(piezoelectricity!=0)&&(thermalexpansion!=0)) {
      const Cijkl& cijkl = elasticity->cijkl(mesh, el, pos);
      const SymmMatrix3 alpha = thermalexpansion->expansiontensor(mesh,el,pos);
      const Rank3Tensor &dijk = piezoelectricity->dijk(mesh, el, pos);

      for(unsigned int i=0;i<3;++i) {
	for(SymTensorIterator jk; !jk.end(); ++jk) {
	  for(SymTensorIterator lm; !lm.end(); ++lm) {
	    double diagfact = 1.0;
	    if(!jk.diagonal())
	      diagfact *= 2.0;
	    if(!lm.diagonal())
	      diagfact *= 2.0;

	    effective_modulus[i] -= diagfact*dijk(i,jk)*cijkl(jk,lm)*alpha[lm];
	  }
	}
      }
      // If the partner property moduli are homogeneous, then set a flag
      // so that we don't have to redo this computation.
      if (elasticity->constant_in_space() &&
	  piezoelectricity->constant_in_space() &&
	  thermalexpansion->constant_in_space())
	modulus_ok = true;
    }
    else {
      // If one or more of the partner properties failed to exist,
      // then the effective modulus has not been modified, and the
      // modulus is OK, unless the orientation is non-constant.
      modulus_ok = orientation==0 or not orientation->constant_in_space();
    }
  }
  // If the modulus was the constant-strain modulus in the first
  // place, then of course it was and remains OK, unless the
  // orientation is non-constant.
  else
    modulus_ok = orientation==0 or not orientation->constant_in_space();

}

void PyroElectricity::flux_matrix(const FEMesh *mesh,
				  const Element *element,
				  const ElementFuncNodeIterator &nu,
				  const Flux *flux,
				  const MasterPosition &pos,
				  double time,
				  SmallSystem *fluxdata) const
{

  if(!modulus_ok)
    set_effective_modulus(mesh, element, pos);

  double sf = nu.shapefunction(pos);
  if(*flux==*total_polarization)
    for(VectorFieldIterator i; !i.end(); ++i) {
      fluxdata->stiffness_matrix_element(i,temperature,nu) +=
	effective_modulus[i.integer()]*sf;
    }
  else
    throw ErrProgrammingError("Unexpected flux.", __FILE__, __LINE__);

}

void PyroElectricity::flux_offset(const FEMesh *mesh,
				  const Element *element,
				  const Flux *flux,
				  const MasterPosition &pos,
				  double time,
				  SmallSystem *fluxdata) const {

  if(!modulus_ok)
    set_effective_modulus(mesh, element, pos);

  if(*flux==*total_polarization)
    for(VectorFieldIterator i; !i.end(); ++i) {
      // It's T-T0, so minus.  
      fluxdata->offset_vector_element(i) -=
	effective_modulus[i.integer()]*tzero;
    }
  else
    throw ErrProgrammingError("Unexpected flux.", __FILE__, __LINE__);
}



void PyroElectricity::output(const FEMesh *mesh,
			     const Element *element,
			     const PropertyOutput *output,
			     const MasterPosition &pos,
			     OutputVal *data)
  const
// Compute our contribution to the energy.
{
  if((output->name())=="Energy") {
    const std::string *etype = output->getEnumParam((char*) "etype");
    if(*etype=="Total") {
      ScalarOutputVal *edata = dynamic_cast<ScalarOutputVal*>(data);
      if(!modulus_ok)
	set_effective_modulus(mesh, element, pos);
      const OutputValue tfield = element->outputField(mesh, *temperature, pos);
      const ScalarOutputVal *tval =
	dynamic_cast<const ScalarOutputVal*>(tfield.valuePtr());
      DoubleVec efield(3,0.0);
      findElectricField(mesh, element, pos, efield);
      for(int i=0;i<3;++i) {
	*edata += effective_modulus[i]*efield[i]*(tval->value()-tzero);
      }
    }
    delete etype;
  }
}


//-----------------------------------

bool PyroElectricity::is_symmetric_K(const CSubProblem *sp) const {
  Equation *coulomb = Equation::getEquation("Coulomb_Eqn");
  // If the coulmb equation is active, and temperature is active, then
  // this property makes the stiffness matrix unsymmetric, but not
  // otherwise.
  return !(coulomb->is_active(sp) &&
	   temperature->is_defined(sp) &&
	   temperature->is_active(sp));
}


