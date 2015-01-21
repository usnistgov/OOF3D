// -*- C++ -*-
// $RCSfile: heatconductivity.C,v $
// $Revision: 1.59.2.6 $
// $Author: langer $
// $Date: 2014/10/09 01:48:58 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// heat conductivity

#include <oofconfig.h>
#include "common/coord.h"
#include "common/tostring.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/fieldindex.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/nodalequation.h"
#include "engine/ooferror.h"
#include "engine/outputval.h"
#include "engine/property/heatconductivity/heatconductivity.h"
#include "engine/property/orientation/orientation.h"
#include "engine/smallsystem.h"
#include <iostream>
#include <fstream>
#include <string>

HeatConductivity::HeatConductivity(PyObject *reg, const std::string &nm)
  : FluxProperty(nm,reg)
{
  temperature = dynamic_cast<ScalarField*>(Field::getField("Temperature"));
  heat_flux = dynamic_cast<VectorFlux*>(Flux::getFlux("Heat_Flux"));
}

int HeatConductivity::integration_order(const CSubProblem *subp,
					const Element *el) const
{
#if DIM==2
  if(temperature->in_plane(subp))
    return el->dshapefun_degree();
#endif
  return el->shapefun_degree();
}


void HeatConductivity::static_flux_value(const FEMesh  *mesh,
					 const Element *element,
					 const Flux    *flux,
					 const MasterPosition &pt,
					 double time,
					 SmallSystem *fluxdata) const
{
  // first evaluate the temperature gradient

  DoubleVec fieldGradient(3);

  for (SpaceIndex i=0; i<DIM; ++i){
    OutputValue outputVal = 
      element->outputFieldDeriv( mesh, *temperature, &i, pt );
    fieldGradient[i] = outputVal[0];
  }

#if DIM==2
  // if plane-flux eqn, then dT/dz is kept as a separate out_of_plane field
  if ( !temperature->in_plane(mesh) ){
    OutputValue outputVal = 
      element->outputField( mesh, *temperature->out_of_plane(), pt );
    fieldGradient[2] = outputVal[0];
  }
#endif

  // now compute the flux elements by the following summation
  //    flux_i = cond(i,j) * dT_j
  // where 'cond' is the conductivity tensor and dT_j is
  // jth component of the gradient of the temperature field

  const SymmMatrix3 cond( conductivitytensor( mesh, element, pt ) );

  for(VectorFieldIterator i; !i.end(); ++i)
    fluxdata->flux_vector_element( i ) -= 
      cond( i.integer(), 0 ) * fieldGradient[0] +
      cond( i.integer(), 1 ) * fieldGradient[1] +
      cond( i.integer(), 2 ) * fieldGradient[2];

} // end of 'HeatConductivity::static_flux_value'

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void HeatConductivity::flux_matrix(const FEMesh  *mesh,
				   const Element *el,
				   const ElementFuncNodeIterator &j,
				   const Flux    *flux,
				   const MasterPosition &pt,
				   double time,
				   SmallSystem *fluxdata) const
{
  // The heat flux matrix M_{ij} multiplies the vector of nodal
  // temperatures to give the vector heat current J at point pt.
  // M_{ij} = -kappa_{ik} grad_k N_j
  // J_i = -M_{ij} T_j
  // where N_j is the shapefunction at node j.

  if (*flux != *heat_flux) {
    throw ErrProgrammingError("Unexpected flux", __FILE__, __LINE__);
  }

#if DIM==2
  double sf   = j.shapefunction( pt );
#endif // DIM==2
  double dsf0 = j.dshapefunction( 0, pt );
  double dsf1 = j.dshapefunction( 1, pt );
#if DIM==3
  double dsf2 = j.dshapefunction( 2, pt );
#endif	// DIM==3

  const SymmMatrix3 cond( conductivitytensor( mesh, el, pt ) );

  // Loop over flux components.  Loop over all components, even if
  // the flux is in-plane, because the out-of-plane components of
  // the flux matrix are used to construct the constraint equation.

  for(VectorFieldIterator i; !i.end(); ++i){
#if DIM==2
    // in-plane temperature gradient contributions
    fluxdata->stiffness_matrix_element( i, temperature, j ) -=
                  cond(i.integer(), 0) * dsf0 + cond(i.integer(), 1) * dsf1;

    // out-of-plane temperature gradient contribution
    if(!temperature->in_plane(mesh))
      fluxdata->stiffness_matrix_element(i, temperature->out_of_plane(), j)
                                          -= cond(i.integer(), 2) * sf;

#elif DIM==3
    fluxdata->stiffness_matrix_element( i, temperature, j ) -=
                              cond( i.integer(), 0 ) * dsf0 +
                              cond( i.integer(), 1 ) * dsf1 +
                              cond( i.integer(), 2 ) * dsf2;
#endif	// DIM==3

  }
} // end of 'HeatConductivity::flux_matrix'


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

IsoHeatConductivity::IsoHeatConductivity(PyObject *reg,
					 const std::string &nm,
					 double kppa)
  : HeatConductivity(reg, nm),
    kappa_(kppa)
{
}

void IsoHeatConductivity::precompute(FEMesh *mesh) {
  HeatConductivity::precompute(mesh);
  conductivitytensor_(0,0) = conductivitytensor_(1,1)
    = conductivitytensor_(2,2) = kappa_;
}

const SymmMatrix3
IsoHeatConductivity::conductivitytensor(const FEMesh*,
					const Element*,
					const MasterPosition&)
  const
{
  return conductivitytensor_;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

AnisoHeatConductivity::AnisoHeatConductivity(PyObject *reg,
					     const std::string &nm,
					     SymmMatrix3 *k)
  : HeatConductivity(reg,nm),
    kappa_(*k),
    orientation(0)
{}

void AnisoHeatConductivity::cross_reference(Material *mat) {
  try {
    orientation =
      dynamic_cast<OrientationPropBase*>(mat->fetchProperty("Orientation"));
  }
  catch (ErrNoSuchProperty&) {
    orientation = 0;
    throw;
  }
}

void AnisoHeatConductivity::precompute(FEMesh *mesh) {
  HeatConductivity::precompute(mesh);
  if(orientation && orientation->constant_in_space())
    conductivitytensor_ = kappa_.transform(orientation->orientation());
}

const SymmMatrix3
AnisoHeatConductivity::conductivitytensor(const FEMesh *mesh,
					  const Element *el,
					  const MasterPosition &mpos)
  const
{
  if(orientation->constant_in_space())
    return conductivitytensor_;
  return kappa_.transform(orientation->orientation(mesh, el, mpos));
}
