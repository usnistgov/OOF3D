// -*- C++ -*-
// $RCSfile: nonlinear_heat_conductivity.C,v $
// $Revision: 1.16.4.5 $
// $Author: fyc $
// $Date: 2014/07/31 21:03:19 $

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
#include "common/smallmatrix.h"
#include "common/tostring.h"
#include "common/vectormath.h"
#include "engine/cnonlinearsolver.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/fieldindex.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/nodalequation.h"
#include "engine/property/heatconductivity/nonlinear/nonlinear_heat_conductivity.h"
#include "engine/property/orientation/orientation.h"
#include "engine/smallsystem.h"
#include <iostream>
#include <fstream>
#include <string>


NonlinearHeatConductivityNoDeriv::NonlinearHeatConductivityNoDeriv(
				     PyObject *reg, const std::string &nm)
  : FluxProperty(nm,reg)
{
  temperature = dynamic_cast<ScalarField*>(Field::getField("Temperature"));
  heat_flux = dynamic_cast<VectorFlux*>(Flux::getFlux("Heat_Flux"));
}


int NonlinearHeatConductivityNoDeriv::integration_order(const CSubProblem *subp,
							const Element *el) const
{
#if DIM==2
  if(temperature->in_plane(subp))
    return el->dshapefun_degree();
#endif
  return el->shapefun_degree();
}


void NonlinearHeatConductivityNoDeriv::static_flux_value(
						 const FEMesh  *mesh,
						 const Element *element,
						 const Flux    *flux,
						 const MasterPosition &pt,
						 double time,
						 SmallSystem *fluxdata)
  const
{
  // first evaluate the temperature field and the temperature gradient

  DoubleVec fieldGradient(3), fluxVector(3);
  double fieldValue;

  OutputValue outputVal = element->outputField( mesh, *temperature, pt );
  fieldValue = outputVal[0];

  for (SpaceIndex i=0; i<DIM; ++i){
    OutputValue outputVal = element->outputFieldDeriv(
				      mesh, *temperature, &i, pt );
    fieldGradient[i] = outputVal[0];
  }

#if DIM==2
  // if plane-flux eqn, then dT/dz is kept as a separate out_of_plane
  // field
  if ( !temperature->in_plane(mesh) ){
    OutputValue outputVal = element->outputField(
				 mesh, *temperature->out_of_plane(), pt );
    fieldGradient[2] = outputVal[0];
  }
#endif

  // evaluate the value of the flux with the given pt, time and
  // temperature field

  Coord coord = element->from_master( pt );
  
  nonlin_heat_flux(coord, time, fieldValue, fieldGradient, fluxVector);
// #if DIM==2
//   nonlin_heat_flux( coord.x, coord.y, 0.0, time,
// 		    fieldValue, fieldGradient, fluxVector );
// #elif DIM==3
//   nonlin_heat_flux( coord.x, coord.y, coord.z, time,
// 		    fieldValue, fieldGradient, fluxVector );
// #endif

  // add the heat flux contribution to the small system 'fluxdata',
  // which will later be added to the global div_flux vector
  fluxdata->fluxVector() += fluxVector;

} // end of 'NonlinearHeatConductivityNoDeriv::static_flux_value'


void NonlinearHeatConductivity::flux_matrix(const FEMesh  *mesh,
					    const Element *element,
					    const ElementFuncNodeIterator &j,
					    const Flux    *flux,
					    const MasterPosition &pt,
					    double time,
					    SmallSystem *fluxdata)
  const
{
  // check for unexpected flux, should be heat flux

  if (*flux != *heat_flux) {
    throw ErrProgrammingError("Unexpected flux", __FILE__, __LINE__);
  }

  // first evaluate the temperature field and the temperature gradient

  DoubleVec fieldGradient(3), fluxDerivVec(3);
  double fieldValue;
  SmallMatrix fluxDerivMtx(3);

  OutputValue outputVal = element->outputField( mesh, *temperature, pt );
  fieldValue = outputVal[0];

  for (SpaceIndex i=0; i<DIM; ++i){
    OutputValue outputVal = element->outputFieldDeriv(mesh, *temperature,
						      &i, pt);
    fieldGradient[i] = outputVal[0];
  }

#if DIM==2
  // if plane-flux eqn, then dT/dz is kept as a separate out_of_plane
  // field
  if(!temperature->in_plane(mesh)) {
    OutputValue outputVal = element->outputField(
				 mesh, *temperature->out_of_plane(), pt );
    fieldGradient[2] = outputVal[0];
  }
#endif

  // evaluate the value of the flux derivatives with the given pt,
  // time, temperature etc

  Coord coord = element->from_master( pt );

  // the derivative of the heat flux mapping w.r.t. temperature
  nonlin_heat_flux_deriv_wrt_temperature(coord, time, fieldValue, fieldGradient,
					 fluxDerivVec);
// #if DIM==2
//   nonlin_heat_flux_deriv_wrt_temperature( coord.x, coord.y, 0.0, time,
// 				  fieldValue, fieldGradient, fluxDerivVec );
// #elif DIM==3
//   nonlin_heat_flux_deriv_wrt_temperature( coord.x, coord.y, coord.z, time,
// 				  fieldValue, fieldGradient, fluxDerivVec );
// #endif

  // the derivative of the heat flux mapping w.r.t. temperature gradient
  nonlin_heat_flux_deriv_wrt_temperature_gradient(coord, time, fieldValue,
						  fieldGradient, fluxDerivMtx);
// #if DIM==2
//   nonlin_heat_flux_deriv_wrt_temperature_gradient( coord.x, coord.y, 0.0, time,
// 				   fieldValue, fieldGradient, fluxDerivMtx );
// #elif DIM==3
//   nonlin_heat_flux_deriv_wrt_temperature_gradient(
// 				  coord.x, coord.y, coord.z, time,
// 				  fieldValue, fieldGradient, fluxDerivMtx );
// #endif

  // evaluate the shape function and its gradient of given node j at given pt

  double shapeFuncVal, shapeFuncGrad[3];
  shapeFuncVal     = j.shapefunction( pt );
  shapeFuncGrad[0] = j.dshapefunction( 0, pt );
  shapeFuncGrad[1] = j.dshapefunction( 1, pt );
#if DIM==3
  shapeFuncGrad[2] = j.dshapefunction( 2, pt );
#endif


  // Loop over flux components.  Loop over all components, even if
  // the flux is in-plane, because the out-of-plane components of
  // the flux matrix are used to construct the constraint equation.

  // This iterator by default has a dimension of 3.
  for (VectorFieldIterator i; !i.end(); ++i)
  {
#if DIM==2
    // in-plane temperature gradient contributions
    fluxdata->stiffness_matrix_element( i, temperature, j )

               += fluxDerivVec[ i.integer() ] * shapeFuncVal +
                  fluxDerivMtx( i.integer(), 0 ) * shapeFuncGrad[0] +
                  fluxDerivMtx( i.integer(), 1 ) * shapeFuncGrad[1];

    if ( !temperature->in_plane( mesh ) )
      fluxdata->stiffness_matrix_element( i, temperature->out_of_plane(), j )
	+= fluxDerivMtx( i.integer(), 2 ) * shapeFuncVal;

#elif DIM==3
    fluxdata->stiffness_matrix_element( i, temperature, j )

               += fluxDerivVec[ i.integer() ] * shapeFuncVal +
                  fluxDerivMtx( i.integer(), 0 ) * shapeFuncGrad[0] +
                  fluxDerivMtx( i.integer(), 1 ) * shapeFuncGrad[1] +
                  fluxDerivMtx( i.integer(), 2 ) * shapeFuncGrad[2];
#endif
  }

} // end of 'NonlinearHeatConductivity::flux_matrix'



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

inline double SQR(double x){ return x*x; }
inline double CUBE(double x){ return x*x*x; }


void nonlin_heat_flux_1(double x, double y, double z,
			double time, double temperature,
			const DoubleVec &temperature_gradient,
			DoubleVec &heat_flux)
{
  heat_flux[0] = -temperature_gradient[0] - CUBE(temperature_gradient[0]) / 3.0;
  heat_flux[1] = -temperature_gradient[1] -
    pow(temperature_gradient[1], 5.0)/50.0;
  heat_flux[2] =  0.0;

} // end of 'nonlin_heat_flux_1'


void nonlin_heat_flux_deriv_wrt_temperature_1(
                                       double x, double y, double z,
				       double time, double temperature,
				       const DoubleVec &temperature_gradient,
				       DoubleVec &heat_flux_deriv)
{
  heat_flux_deriv[0] = 0.0;
  heat_flux_deriv[1] = 0.0;
  heat_flux_deriv[2] = 0.0;

} // end of 'nonlin_heat_flux_deriv_wrt_temperature_1'


void nonlin_heat_flux_deriv_wrt_temperature_gradient_1(
                                       double x, double y, double z,
				       double time, double temperature,
				       const DoubleVec &temperature_gradient,
				       SmallMatrix &heat_flux_deriv)
{
  heat_flux_deriv(0,0) = -1.0 - SQR( temperature_gradient[0] );
  heat_flux_deriv(0,1) =  0.0;
  heat_flux_deriv(0,2) =  0.0;

  heat_flux_deriv(1,0) =  0.0;
  heat_flux_deriv(1,1) = -1.0 - pow( temperature_gradient[1], 4.0 ) / 10.0;
  heat_flux_deriv(1,2) =  0.0;

  heat_flux_deriv(2,0) =  0.0;
  heat_flux_deriv(2,1) =  0.0;
  heat_flux_deriv(2,2) =  0.0;

} // end of 'nonlin_heat_flux_deriv_wrt_temperature_gradient_1'


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


void nonlin_heat_flux_2(double x, double y, double z,
			double time, double temperature,
			const DoubleVec &temperature_gradient,
			DoubleVec &heat_flux)
{
  heat_flux[0] = -temperature_gradient[0] - CUBE( temperature_gradient[0] )
                 -temperature_gradient[2] / 20.0;
  heat_flux[1] = -temperature_gradient[1] - CUBE( temperature_gradient[1] )
                 -temperature_gradient[2] / 20.0;
  heat_flux[2] = -temperature_gradient[0] /20.0 - temperature_gradient[1] /20.0
                 -atan( temperature_gradient[2] );

} // end of 'nonlin_heat_flux_1'


void nonlin_heat_flux_deriv_wrt_temperature_2(
                                       double x, double y, double z,
				       double time, double temperature,
				       const DoubleVec &temperature_gradient,
				       DoubleVec &heat_flux_deriv)
{
  heat_flux_deriv[0] = 0.0;
  heat_flux_deriv[1] = 0.0;
  heat_flux_deriv[2] = 0.0;

} // end of 'nonlin_heat_flux_deriv_wrt_temperature_2'


void nonlin_heat_flux_deriv_wrt_temperature_gradient_2(
                                       double x, double y, double z,
				       double time, double temperature,
				       const DoubleVec &temperature_gradient,
				       SmallMatrix &heat_flux_deriv)
{
  heat_flux_deriv(0,0) = -1.0 - 3.0 * SQR( temperature_gradient[0] );
  heat_flux_deriv(0,1) =  0.0;
  heat_flux_deriv(0,2) = -1.0 / 20.0;

  heat_flux_deriv(1,0) =  0.0;
  heat_flux_deriv(1,1) = -1.0 - 3.0 * SQR( temperature_gradient[1] );
  heat_flux_deriv(1,2) = -1.0 / 20.0;

  heat_flux_deriv(2,0) = -1.0 / 20.0;
  heat_flux_deriv(2,1) = -1.0 / 20.0;
  heat_flux_deriv(2,2) = -1.0 / (1.0 + SQR( temperature_gradient[2] ));

} // end of 'nonlin_heat_flux_deriv_wrt_temperature_gradient_2'


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


void nonlin_heat_flux_3(double x, double y, double z,
			double time, double temperature,
			const DoubleVec &temperature_gradient,
			DoubleVec &heat_flux)
{
  heat_flux[0] = -atan( temperature_gradient[0] );
  heat_flux[1] = -atan( temperature_gradient[1] );
  heat_flux[2] = -atan( temperature_gradient[2] );

} // end of 'nonlin_heat_flux_3'


void nonlin_heat_flux_deriv_wrt_temperature_3(double x, double y, double z,
					      double time, double temperature,
					      const DoubleVec &temperature_gradient,
					      DoubleVec &heat_flux_deriv)
{
  heat_flux_deriv[0] = 0.0;
  heat_flux_deriv[1] = 0.0;
  heat_flux_deriv[2] = 0.0;

} // end of 'nonlin_heat_flux_deriv_wrt_temperature_3'


void nonlin_heat_flux_deriv_wrt_temperature_gradient_3(
                                       double x, double y, double z,
				       double time, double temperature,
				       const DoubleVec &temperature_gradient,
				       SmallMatrix &heat_flux_deriv)
{
  heat_flux_deriv(0,0) = -1.0 / (1.0 + SQR( temperature_gradient[0] ));
  heat_flux_deriv(0,1) =  0.0;
  heat_flux_deriv(0,2) =  0.0;

  heat_flux_deriv(1,0) =  0.0;
  heat_flux_deriv(1,1) = -1.0 / (1.0 + SQR( temperature_gradient[1] ));
  heat_flux_deriv(1,2) =  0.0;

  heat_flux_deriv(2,0) =  0.0;
  heat_flux_deriv(2,1) =  0.0;
  heat_flux_deriv(2,2) = -1.0 / ( 1.0 + SQR( temperature_gradient[2] ));

} // end of 'nonlin_heat_flux_deriv_wrt_temperature_gradient_3'


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


void TestNonlinearHeatConductivityNoDeriv::nonlin_heat_flux(
				    const Coord &coord,
				    double time, double temperature,
				    const DoubleVec &temperature_gradient,
				    DoubleVec &heat_flux) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else
  double z = 0.0;
#endif
  switch(testNo)
  {
    case 1:
      nonlin_heat_flux_1( x, y, z, time,
			  temperature, temperature_gradient, heat_flux );
      return;
    case 2:
      nonlin_heat_flux_2( x, y, z, time,
			  temperature, temperature_gradient, heat_flux );
      return;
    case 3:
      nonlin_heat_flux_3( x, y, z, time,
			  temperature, temperature_gradient, heat_flux );
      return;
    default:
      heat_flux[0] = heat_flux[1] = heat_flux[2] = 0.0;
  }
} // end of TestNonlinearHeatConductivityNoDeriv::nonlin_heat_flux_deriv_wrt_temperature_gradient


void TestNonlinearHeatConductivity::nonlin_heat_flux(
				     const Coord &coord,
				     double time, double temperature,
				     const DoubleVec &temperature_gradient,
				     DoubleVec &heat_flux) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else
  double z = 0.0;
#endif
  switch(testNo)
  {
    case 1:
      nonlin_heat_flux_1( x, y, z, time,
			  temperature, temperature_gradient, heat_flux );
      return;
    case 2:
      nonlin_heat_flux_2( x, y, z, time,
			  temperature, temperature_gradient, heat_flux );
      return;
    case 3:
      nonlin_heat_flux_3( x, y, z, time,
			  temperature, temperature_gradient, heat_flux );
      return;
    default:
      heat_flux[0] = heat_flux[1] = heat_flux[2] = 0.0;
  }
} // end of TestNonlinearHeatConductivity::nonlin_heat_flux_deriv_wrt_temperature_gradient


void TestNonlinearHeatConductivity::nonlin_heat_flux_deriv_wrt_temperature(
				   const Coord &coord,
				   double time, double temperature,
				   const DoubleVec &temperature_gradient,
				   DoubleVec &heat_flux_deriv) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else
  double z = 0.0;
#endif
  switch(testNo)
  {
    case 1:
      nonlin_heat_flux_deriv_wrt_temperature_1( x, y, z, time, temperature,
					temperature_gradient, heat_flux_deriv);
      return;

    case 2:
      nonlin_heat_flux_deriv_wrt_temperature_2( x, y, z, time, temperature,
					temperature_gradient, heat_flux_deriv);
      return;

    case 3:
      nonlin_heat_flux_deriv_wrt_temperature_3( x, y, z, time, temperature,
					temperature_gradient, heat_flux_deriv);
      return;

    default:
      heat_flux_deriv[0] = heat_flux_deriv[1] = heat_flux_deriv[2] = 0.0;
  }
} // end of TestNonlinearHeatConductivity::nonlin_heat_flux_deriv_wrt_temperature_gradient


void
TestNonlinearHeatConductivity::nonlin_heat_flux_deriv_wrt_temperature_gradient(
				    const Coord &coord,
				    double time, double temperature,
				    const DoubleVec &temperature_gradient,
				    SmallMatrix &heat_flux_deriv) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else
  double z = 0.0;
#endif
  switch(testNo)
  {
    case 1:
      nonlin_heat_flux_deriv_wrt_temperature_gradient_1( x, y, z, time,
							 temperature,
							 temperature_gradient,
							 heat_flux_deriv );
      return;

    case 2:
      nonlin_heat_flux_deriv_wrt_temperature_gradient_2( x, y, z, time,
							 temperature,
							 temperature_gradient,
							 heat_flux_deriv );
      return;

    case 3:
      nonlin_heat_flux_deriv_wrt_temperature_gradient_3( x, y, z, time,
							 temperature,
							 temperature_gradient,
							 heat_flux_deriv );
      return;

    default:
      for (int i=0; i<3; i++)
	heat_flux_deriv(i,0) = heat_flux_deriv(i,1) =
	  heat_flux_deriv(i,2) = 0.0;
  }
} // end of TestNonlinearHeatConductivity::nonlin_heat_flux_deriv_wrt_temperature_gradient

