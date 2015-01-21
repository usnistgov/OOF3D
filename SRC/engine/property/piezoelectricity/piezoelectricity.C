// -*- C++ -*-
// $RCSfile: piezoelectricity.C,v $
// $Revision: 1.45.10.3 $
// $Author: langer $
// $Date: 2013/11/08 20:46:00 $

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
#include "common/doublevec.h"
#include "common/printvec.h"
#include "common/trace.h"
#include "engine/IO/propertyoutput.h"
#include "engine/celectricfield.h"
#include "engine/cstrain.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/equation.h"
#include "engine/flux.h"
#include "engine/indextypes.h"
#include "engine/material.h"
#include "engine/ooferror.h"
#include "engine/property/elasticity/cijkl.h"
#include "engine/property/elasticity/elasticity.h"
#include "engine/property/orientation/orientation.h"
#include "engine/property/piezoelectricity/piezoelectricity.h"
#include "engine/rank3tensor.h"
#include "engine/smallsystem.h"

PiezoElectricity::PiezoElectricity(PyObject *reg,
				   const std::string &nm)
  : FluxProperty(nm,reg)
{

  stress_flux=dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
  voltage=dynamic_cast<ScalarField*>(Field::getField("Voltage"));
  total_polarization = 
    dynamic_cast<VectorFlux*>(Flux::getFlux("Total_Polarization"));

#if DIM==2
  displacement = 
    dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
#elif DIM==3
  displacement = 
    dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
#endif	// DIM==3
}


void PiezoElectricity::precompute(FEMesh*) {}

int PiezoElectricity::integration_order(const CSubProblem *subproblem,
					const Element *el) const {
#if DIM==2
  if(displacement->in_plane(subproblem))
    return el->dshapefun_degree();
#endif	// DIM==2
  return el->shapefun_degree();
}

void PiezoElectricity::flux_matrix(const FEMesh *mesh,
				   const Element *element,
				   const ElementFuncNodeIterator &nu,
				   const Flux *flux,
				   const MasterPosition &pos,
				   double time,
				   SmallSystem *fluxdata) const
{
  const Rank3Tensor eijk =
    elasticity->cijkl(mesh, element, pos) * dijk(mesh, element, pos);

  //shape functions and their derivatives
#if DIM==2
  double sf = nu.shapefunction(pos);
#endif	// DIM==2
  double dsf0 = nu.dshapefunction(0, pos);
  double dsf1 = nu.dshapefunction(1, pos);
#if DIM==3
  double dsf2 = nu.dshapefunction(2, pos);
#endif	// DIM==3

  if(*flux == *stress_flux) {
    for(SymTensorIterator ij; !ij.end(); ++ij) { // stress component ij
#if DIM==2
      fluxdata->stiffness_matrix_element(ij, voltage, nu)
	+= eijk(0,ij)*dsf0 + eijk(1,ij)*dsf1;
#elif DIM==3
      fluxdata->stiffness_matrix_element(ij, voltage, nu)
	+= eijk(0,ij)*dsf0 + eijk(1,ij)*dsf1 + eijk(2,ij)*dsf2;
#endif // DIM==3
    }
#if DIM==2
    if(!voltage->in_plane(mesh)) {
      Field *voop = voltage->out_of_plane();
      for(SymTensorIterator ij; !ij.end(); ++ij) {
	fluxdata->stiffness_matrix_element(ij, voop, nu) += eijk(2,ij)*sf;
      }
    }
#endif // DIM==2
  }

  if(*flux == *total_polarization) {
    for(VectorFieldIterator i; !i.end(); ++i) { // polarization components
      // in-plane displacement gradient contributions
      int ii = i.integer();
      for(IteratorP ell = displacement->iterator(); !ell.end(); ++ell) {
	SymTensorIndex ell0(0, ell.integer());
	SymTensorIndex ell1(1, ell.integer());
	
#if DIM==2
	fluxdata->stiffness_matrix_element(i, displacement, ell, nu) +=
	  eijk(ii, ell0)*dsf0 + eijk(ii, ell1)*dsf1;
#elif DIM==3
	SymTensorIndex ell2(2, ell.integer());
	fluxdata->stiffness_matrix_element(i, displacement, ell, nu) +=
	  eijk(ii, ell0)*dsf0 + eijk(ii, ell1)*dsf1 + eijk(ii, ell2)*dsf2;
#endif	// DIM==3
      }

#if DIM==2
      if(!displacement->in_plane(mesh)) {
	Field *oop = displacement->out_of_plane();
	for(IteratorP kay=oop->iterator(ALL_INDICES); !kay.end(); ++kay) {
	  fluxdata->stiffness_matrix_element(i, oop, kay, nu) +=
	    sf * eijk(ii, SymTensorIndex(2, kay.integer()));
	}
      }
#endif // DIM==2

    }  // end loop over polarization components
  } 
}


void PiezoElectricity::output(const FEMesh *mesh,
			      const Element *element,
			      const PropertyOutput *output,
			      const MasterPosition &pos,
			      OutputVal *data)
  const
{
  const std::string &outputname = output->name();
  if(outputname == "Strain") {
    const std::string *stype = output->getRegisteredParamName((char*) "type");
    if(*stype == "Piezoelectric" || *stype == "Elastic") {
      SymmMatrix3 *sdata = dynamic_cast<SymmMatrix3*>(data);
      DoubleVec E_field(3,0);
      findElectricField(mesh, element, pos, E_field);
      if(*stype == "Piezoelectric")
	// Piezoelectric strain is d*E = -d*(grad V)
	*sdata += dijk(mesh, element, pos)*E_field;
      else			// stype == "Elastic"
	*sdata -= dijk(mesh, element, pos)*E_field;
    }
    delete stype;
  }

  if(outputname == "Energy") {
    const std::string *etype = output->getEnumParam((char*) "etype");
    //Energies
    if(*etype == "Total" || *etype == "Elastic" || *etype == "Electric") {
      ScalarOutputVal *edata =
	dynamic_cast<ScalarOutputVal*>(data);
      SymmMatrix piezoelectricStrain(3);
      const Cijkl modulus = elasticity->cijkl(mesh, element, pos);

      DoubleVec E_field(3,0.0);
      findElectricField(mesh, element, pos, E_field);
      piezoelectricStrain = dijk(mesh, element, pos)*E_field;
      SymmMatrix electricstress(modulus*piezoelectricStrain);
      SymmMatrix3 strain;
      elasticity->geometricStrain(mesh, element, pos, &strain);
      double e = 0;
      for(int i=0; i<3; i++) {
	e += electricstress(i,i)*strain(i,i);
	int j = (i+1)%3;
	e += 2*electricstress(i,j)*strain(i,j);
      }
      if(*etype == "Total")
	*edata += -e;
      else if (*etype == "Elastic" || *etype == "Electric")
	*edata += -0.5*e;
    } 
    delete etype;
  }
}

IsotropicPiezoElectricity::IsotropicPiezoElectricity(PyObject *registry,
						     const std::string &name,
						     double d)
  : PiezoElectricity(registry, name),
    _dijkValue(d)
{

}


void IsotropicPiezoElectricity::cross_reference(Material *mat) {
  // find out which property is the elasticity
  try {
    elasticity = dynamic_cast<Elasticity*>(mat->fetchProperty("Elasticity"));
  }
  catch (ErrNoSuchProperty&) {
    elasticity = 0;
    throw;
  }
}

void IsotropicPiezoElectricity::precompute(FEMesh *mesh) {
  PiezoElectricity::precompute(mesh);
  _dijkLab(0,0,0) = _dijkLab(1,1,1)
    = _dijkLab(2,2,2) = _dijkValue;
}

AnisotropicPiezoElectricity::AnisotropicPiezoElectricity(PyObject *registry,
							 const std::string &nm,
							 Rank3Tensor *dijkTensor)
  : PiezoElectricity(registry, nm),
    _dijkValue(*dijkTensor),
    orientation(0)
{

}
void AnisotropicPiezoElectricity::cross_reference(Material *mat) {
  // find out which property is the elasticity
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

void AnisotropicPiezoElectricity::precompute(FEMesh*) {
  if(orientation && orientation->constant_in_space())
    _dijkLab = _dijkValue.transform(orientation->orientation());
}

const Rank3Tensor
AnisotropicPiezoElectricity::dijk(const FEMesh *mesh, const Element *el,
				  const MasterPosition &pos) const
{
  if(orientation->constant_in_space())
    return _dijkLab;
  return _dijkValue.transform(orientation->orientation(mesh, el, pos));
}
