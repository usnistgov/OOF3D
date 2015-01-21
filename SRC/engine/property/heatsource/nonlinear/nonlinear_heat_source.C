// -*- C++ -*-
// $RCSfile: nonlinear_heat_source.C,v $
// $Revision: 1.8.4.5 $
// $Author: fyc $
// $Date: 2014/07/29 21:22:24 $

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
#include "common/cleverptr.h"
#include "nonlinear_heat_source.h"
#include "common/tostring.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/fieldindex.h"
#include "engine/material.h"
#include "engine/property/orientation/orientation.h"
#include "engine/smallsystem.h"
#include "engine/nodalequation.h"
#include "engine/cnonlinearsolver.h"


NonlinearHeatSourceNoDeriv::NonlinearHeatSourceNoDeriv(PyObject *reg,
						       const std::string &name)
  : EqnProperty(name,reg)
{
  temperature = dynamic_cast<ScalarField*>(Field::getField("Temperature"));
  heat_flux   = dynamic_cast<VectorFlux*>(Flux::getFlux("Heat_Flux"));
}

int NonlinearHeatSourceNoDeriv::integration_order(const CSubProblem *, 
						  const Element *el) const
{
  return el->shapefun_degree();
}


void NonlinearHeatSourceNoDeriv::force_value(const FEMesh *mesh,
				      const Element *element,
				      const Equation *eqn,
				      const MasterPosition &pt,
				      double time,
				      SmallSystem *eqndata) const
{
  double fieldVal, sourceVal;
  Coord coord;

  // first compute the current value of the temperature field at the gauss point

  fieldVal = 0.0;
  for(CleverPtr<ElementFuncNodeIterator> node(element->funcnode_iterator());
      !node->end(); ++*node){
    double shapeFuncVal = node->shapefunction( pt );
    fieldVal += shapeFuncVal * (*temperature)( *node )->value( mesh );
  }


  // now use the world coord and temperature value to compute the value
  // of nonlinear weight function and the contribution to force_vector_element

  coord = element->from_master( pt );

  // TODO: MER Pass a Coord to nonlin_heat_source, instead of the separate
  // components, and get rid of the #if here.

#if DIM==2
  sourceVal = nonlin_heat_source( coord[0], coord[1], 0.0, time, fieldVal );
#elif DIM==3
  sourceVal = nonlin_heat_source( coord[0], coord[1], coord[2], time, fieldVal );
#endif

  eqndata->force_vector_element(0) = -sourceVal;

} // NonlinearHeatSourceNoDeriv::force_value


void NonlinearHeatSource::force_deriv_matrix(const FEMesh   *mesh,
					     const Element  *element,
					     const Equation *eqn,
					     const ElementFuncNodeIterator &j,
					     const MasterPosition &point,
					     double time,
					     SmallSystem *eqndata ) const
{
  double fieldVal, funcDerivVal, shapeFuncVal;
  Coord  coord;

  // first compute the current value of the temperature field at the gauss point

  fieldVal = 0.0;
  for(CleverPtr<ElementFuncNodeIterator> node(element->funcnode_iterator());
      !node->end(); ++*node){
    shapeFuncVal = node->shapefunction( point );
    fieldVal += shapeFuncVal * (*temperature)( *node )->value( mesh );
  }

  // compute the value of the deriv of the nonlinear source function
  // using the world coordinates and the value of the temperature field

  coord = element->from_master( point );

  // TODO MER: Pass a Coord to nonlin_heat_source_deriv_wrt_temperature,
  // instead of the separate components, and get rid of the #if here.

#if DIM==2
  funcDerivVal = nonlin_heat_source_deriv_wrt_temperature(
			  coord[0], coord[1], 0.0, time, fieldVal );
#elif DIM==3
  funcDerivVal = nonlin_heat_source_deriv_wrt_temperature(
			  coord[0], coord[1], coord[2], time, fieldVal );
#endif	// DIM==3

  // compute the value of the jth shape function at gauss point point
  // and add its contribution f(point)*phi_j(point) to the small
  // stiffness-like matrix

  shapeFuncVal = j.shapefunction( point );

  for (IteratorP eqncomp = eqn->iterator(); !eqncomp.end(); ++eqncomp)
    eqndata->force_deriv_matrix_element( eqncomp, temperature, j )
                -= funcDerivVal * shapeFuncVal;

} // NonlinearHeatSource::force_deriv_matrix



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


inline double SQR(double x){ return x*x; }
inline double CUBE(double x){ return x*x*x; }


double nonlin_heat_source_1(double x, double y, double z,
			    double time, double temperature)
{
  double source_value;
  double pi = M_PI, uex, f;
  double m = 2.0, n = 3.0, p = 4.0;

  uex = sin(m*pi*x) * sin(n*pi*y) * sin(p*pi*z);
  f = -(m*m + n*n + p*p)*pi*pi*uex + uex - CUBE(uex);
  source_value = -temperature + CUBE( temperature ) + f;

  return source_value;

} // end of 'nonlin_heat_source_1'


double nonlin_heat_source_deriv_wrt_temperature_1(
                                  double x, double y, double z,
				  double time, double temperature)
{
  double source_deriv_value = -1.0 + 3.0 * SQR( temperature );

  return source_deriv_value;

} // end of 'nonlin_heat_source_wrt_temperature_1'


double nonlin_heat_source_2(double x, double y, double z,
			    double time, double temperature)
{
  double source_value;
  double pi = M_PI, uex, f;
  double w = 1.5, m = 2.0, n = 3.0, p=2.0;

  uex = exp(-w*time) * sin(m*pi*x) * sin(n*pi*y) * sin(p*pi*z);
  f = (w -(m*m + n*n + p*p)*pi*pi)*uex + uex - CUBE(uex);
  source_value = -temperature + CUBE( temperature ) + f;

  return source_value;

} // end of 'nonlin_heat_source_2'


double nonlin_heat_source_deriv_wrt_temperature_2(
                                  double x, double y, double z,
				  double time, double temperature)
{
  double source_deriv_value = -1.0 + 3.0 * SQR( temperature );

  return source_deriv_value;

} // end of 'nonlin_heat_source_wrt_temperature_2'


double nonlin_heat_source_3(double x, double y, double z,
			    double time, double temperature)
{
  double source_value = 4.0 * exp( temperature );

  return source_value;

} // end of 'nonlin_heat_source_3'


double nonlin_heat_source_deriv_wrt_temperature_3(
                                  double x, double y, double z,
				  double time, double temperature)
{
  double source_deriv_value = 4.0 * exp( temperature );

  return source_deriv_value;

} // end of 'nonlin_heat_source_wrt_temperature_3'


double nonlin_heat_source_4(double x, double y, double z,
			    double time, double temperature)
{
  double source_value = 2.0 * CUBE( temperature );

  return source_value;

} // end of 'nonlin_heat_source_4'


double nonlin_heat_source_deriv_wrt_temperature_4(
                                  double x, double y, double z,
				  double time, double temperature)
{
  double source_deriv_value = 6.0 * SQR( temperature );

  return source_deriv_value;

} // end of 'nonlin_heat_source_wrt_temperature_4'


double nonlin_heat_source_5(double x, double y, double z,
			    double time, double temperature)
{
  double source_value = -2.0 + 8.0 * exp( 2.0 * temperature );

  return source_value;

} // end of 'nonlin_heat_source_5'


double nonlin_heat_source_deriv_wrt_temperature_5(
                                  double x, double y, double z,
				  double time, double temperature)
{
  double source_deriv_value = 16.0 * exp( 2.0 * temperature );

  return source_deriv_value;

} // end of 'nonlin_heat_source_wrt_temperature_5'


double TestNonlinearHeatSourceNoDeriv::nonlin_heat_source(
                                  double x, double y, double z,
				  double time, double temperature) const
{
  switch (testNo)
  {
    case 1:
      return -nonlin_heat_source_1( x, y, z, time, temperature );
    case 2:
      return -nonlin_heat_source_2( x, y, z, time, temperature );
    case 3:
      return -nonlin_heat_source_3( x, y, z, time, temperature );
    case 4:
      return -nonlin_heat_source_4( x, y, z, time, temperature );
    case 5:
      return -nonlin_heat_source_5( x, y, z, time, temperature );
    default:
      return 0.0;
  }

} // end of 'TestNonlinearHeatSourceNoDeriv::nonlin_heat_source'


double TestNonlinearHeatSource::nonlin_heat_source(
                                  double x, double y, double z,
				  double time, double temperature) const
{
  switch (testNo)
  {
    case 1:
      return -nonlin_heat_source_1( x, y, z, time, temperature );
    case 2:
      return -nonlin_heat_source_2( x, y, z, time, temperature );
    case 3:
      return -nonlin_heat_source_3( x, y, z, time, temperature );
    case 4:
      return -nonlin_heat_source_4( x, y, z, time, temperature );
    case 5:
      return -nonlin_heat_source_5( x, y, z, time, temperature );
    default:
      return 0.0;
  }

} // end of 'TestNonlinearHeatSource::nonlin_heat_source'


double TestNonlinearHeatSource::nonlin_heat_source_deriv_wrt_temperature(
                                  double x, double y, double z,
				  double time, double temperature) const
{
  switch (testNo)
  {
    case 1:
      return -nonlin_heat_source_deriv_wrt_temperature_1( x, y, z, time, temperature );
    case 2:
      return -nonlin_heat_source_deriv_wrt_temperature_2( x, y, z, time, temperature );
    case 3:
      return -nonlin_heat_source_deriv_wrt_temperature_3( x, y, z, time, temperature );
    case 4:
      return -nonlin_heat_source_deriv_wrt_temperature_4( x, y, z, time, temperature );
    case 5:
      return -nonlin_heat_source_deriv_wrt_temperature_5( x, y, z, time, temperature );
    default:
      return 0.0;
  }

} // end of 'TestNonlinearHeatSource::nonlin_heat_source_wrt_temperature'
