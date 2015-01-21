// -*- C++ -*-
// $RCSfile: nonlinear_force_density.C,v $
// $Revision: 1.13.4.5 $
// $Author: fyc $
// $Date: 2014/07/29 21:22:10 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */


#include <oofconfig.h>
#include "common/cleverptr.h"
#include "common/coord.h"
#include "common/ooferror.h"
#include "common/smallmatrix.h"
#include "common/trace.h"
#include "common/vectormath.h"
#include "engine/cnonlinearsolver.h"
#include "engine/cstrain.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/indextypes.h"
#include "engine/material.h"
#include "nonlinear_force_density.h"


NonlinearForceDensityNoDeriv::NonlinearForceDensityNoDeriv(PyObject *reg, const std::string &nm)
  : EqnProperty(nm,reg)
{
#if DIM==2
  displacement = dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
#elif DIM==3
  displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
#endif
  stress_flux  = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}

void NonlinearForceDensityNoDeriv::precompute(FEMesh*) {
}

int NonlinearForceDensityNoDeriv::integration_order(const CSubProblem*, const Element *el) const
{
  return el->shapefun_degree();
}


void NonlinearForceDensityNoDeriv::force_value(
                                const FEMesh *mesh, const Element *element,
				const Equation *eqn, const MasterPosition &point,
				double time, SmallSystem *eqndata) const
{
  DoubleVec fieldVal(3, 0.0);
  Coord coord;

  // first compute the current value of the displacement field at the gauss point

  for(CleverPtr<ElementFuncNodeIterator> node(element->funcnode_iterator());
      !node->end(); ++*node) {
    double shapeFuncVal = node->shapefunction( point );

    // TODO OPT: It would be nice if we could write this with no loop like so:
    //   fieldVal += shapeFuncVal * (*displacement)(node)->value(mesh);
    // That would require a Field method that returned a DoubleVec.
    // Can we use OutputValues?  Would that be slow?
    fieldVal[0] += shapeFuncVal * (*displacement)( *node, 0 )->value( mesh );
    fieldVal[1] += shapeFuncVal * (*displacement)( *node, 1 )->value( mesh );
#if DIM==3
    fieldVal[2] += shapeFuncVal * (*displacement)( *node, 2 )->value( mesh );
#endif	// DIM==3
  }

  // now compute the force density value for the current coordinate x,y,z,
  // time and displacement,
  // the nonlinear force density function returns the corresponding
  // force value in the array 'force',

  coord = element->from_master( point );

  DoubleVec force(3, 0.0);
  nonlin_force_density(coord, time, fieldVal, force);
// #if DIM==2
//   nonlin_force_density( coord.x, coord.y, 0.0, time, fieldVal, force );
// #elif DIM==3
//   nonlin_force_density( coord.x, coord.y, coord.z, time, fieldVal, force );
// #endif

  eqndata->forceVector() += force;
//   eqndata->force_vector_element(0) += force[0];
//   eqndata->force_vector_element(1) += force[1];
// #if DIM==3
//   eqndata->force_vector_element(2) += force[2];
// #endif

} // end of 'NonlinearForceDensityNoDeriv::force_value'


void NonlinearForceDensity::force_deriv_matrix(const FEMesh   *mesh,
					       const Element  *element,
					       const Equation *eqn,
					       const ElementFuncNodeIterator &j,
					       const MasterPosition &point,
					       double time,
					       SmallSystem *eqndata) const
{
  DoubleVec fieldVal(3, 0.0);
  double shapeFuncVal;
  Coord  coord;

  // first compute the current value of the displacement field at the gauss point

  for(CleverPtr<ElementFuncNodeIterator> node(element->funcnode_iterator());
      !node->end(); ++*node){
    shapeFuncVal = node->shapefunction( point );
    fieldVal[0] += shapeFuncVal * (*displacement)( *node, 0 )->value( mesh );
    fieldVal[1] += shapeFuncVal * (*displacement)( *node, 1 )->value( mesh );
#if DIM==3
    fieldVal[2] += shapeFuncVal * (*displacement)( *node, 2 )->value( mesh );
#endif
  }

  // now compute the value of the force density derivative function
  // for the current coordinate x,y,z, time and displacement,
  // the nonlinear force density derivative function returns the
  // corresponding force derivative value in the array 'forceDeriv',
  // the function definition is given in USER_CODE.C

  coord = element->from_master( point );

  SmallMatrix forceDeriv(3);
  nonlin_force_density_deriv(coord, time, fieldVal, forceDeriv);
// #if DIM==2
//   nonlin_force_density_deriv( coord.x, coord.y, 0.0,
// 			      time, fieldVal, forceDeriv );
// #elif DIM==3
//   nonlin_force_density_deriv( coord.x, coord.y, coord.z,
// 			      time, fieldVal, forceDeriv );
// #endif

  // compute the value of the jth shape function at gauss point point and add
  // its contribution Df(point,field)*phi_j(point) to the small mass-like matrix

  shapeFuncVal = j.shapefunction( point );

  for(IteratorP eqncomp = eqn->iterator(); !eqncomp.end(); ++eqncomp) {
    int eqno = eqncomp.integer();

    for (IteratorP fieldcomp = displacement->iterator(); !fieldcomp.end();
	 ++fieldcomp)
      { 
	// TODO OPT: get rid of this loop, and write component
	// contributions explicitly
	int fieldno = fieldcomp.integer();

	eqndata->force_deriv_matrix_element(eqncomp, displacement, fieldcomp, j)
	  += forceDeriv( eqno, fieldno ) * shapeFuncVal;
      }
  }

} // end of 'NonlinearForceDensity::force_deriv_matrix'


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


inline double SQR(double x){ return x*x; }
inline double CUBE(double x){ return x*x*x; }


void nonlin_force_density_1(double x, double y, double z, double time,
			    DoubleVec &displacement,
			    DoubleVec &result)
{
  double pi = M_PI;
  double m0 = 2.0, n0 = 3.0, p0 = 4.0;
  double m1 = 1.0, n1 = 2.0, p1 = 3.0;
  double m2 = 3.0, n2 = 2.0, p2 = 1.0;

  double uex0 = sin(m0*pi*x) * sin(n0*pi*y) * sin(p0*pi*z);
  double uex1 = sin(m1*pi*x) * sin(n1*pi*y) * sin(p1*pi*z);
  double uex2 = sin(m2*pi*x) * sin(n2*pi*y) * sin(p2*pi*z);

  double f0 = (m0*m0 + n0*n0 + p0*p0)*pi*pi * uex0 - uex0 + CUBE( uex0 );
  double f1 = (m1*m1 + n1*n1 + p1*p1)*pi*pi * uex1 - uex1 + CUBE( uex1 );
  double f2 = (m2*m2 + n2*n2 + p2*p2)*pi*pi * uex2 - uex2 + CUBE( uex2 );

  result[0] = displacement[0] - CUBE( displacement[0] ) + f0;
  result[1] = displacement[1] - CUBE( displacement[1] ) + f1;
  result[2] = displacement[2] - CUBE( displacement[2] ) + f2;

} // end of 'nonlin_force_density_1'

void nonlin_force_density_deriv_1(double x, double y, double z, double time,
				  DoubleVec &displacement,
				  SmallMatrix &result)
{
  result(0,0) = 1.0 - 3.0 * SQR( displacement[0] );
  result(0,1) = 0.0;
  result(0,2) = 0.0;

  result(1,0) = 0.0;
  result(1,1) = 1.0 - 3.0 * SQR( displacement[1] );
  result(1,2) = 0.0;

  result(2,0) = 0.0;
  result(2,1) = 0.0;
  result(2,2) = 1.0 - 3.0 * SQR( displacement[2] );

} // end of 'nonlin_force_density_deriv_1'


void nonlin_force_density_2(double x, double y, double z, double time,
			    DoubleVec &displacement,
			    DoubleVec &result)
{
  double pi = M_PI;
  double a0 =  2.0, b0 = 3.0, m0 = 2.0, n0 = 3.0, p0 = 1.0;
  double a1 = -4.0, b1 = 5.0, m1 = 1.0, n1 = 2.0, p1 = 1.0;
  double a2 = -4.0, b2 = 3.0, m2 = 1.0, n2 = 1.0, p2 = 2.0;

  // Exact solution
  double uex0 = (a0*time + b0) * sin(m0*pi*x) * sin(n0*pi*y) * sin(p0*pi*z);
  double uex1 = (a1*time + b1) * sin(m1*pi*x) * sin(n1*pi*y) * sin(p1*pi*z);
  double uex2 = (a2*time + b2) * sin(m2*pi*x) * sin(n2*pi*y) * sin(p2*pi*z);

  double f0 = (m0*m0 + n0*n0 + p0*p0)*pi*pi * uex0 - uex0 + CUBE( uex0 );
  double f1 = (m1*m1 + n1*n1 + p1*p1)*pi*pi * uex1 - uex1 + CUBE( uex1 );
  double f2 = (m2*m2 + n2*n2 + p2*p2)*pi*pi * uex2 - uex2 + CUBE( uex2 );

  result[0] = displacement[0] - CUBE( displacement[0] ) + f0;
  result[1] = displacement[1] - CUBE( displacement[1] ) + f1;
  result[2] = displacement[2] - CUBE( displacement[2] ) + f2;

} // end of 'nonlin_force_density_2'

void nonlin_force_density_deriv_2(double x, double y, double z, double time,
				  DoubleVec &displacement,
				  SmallMatrix &result)
{
  result(0,0) = 1.0 - 3.0 * SQR( displacement[0] );
  result(0,1) = 0.0;
  result(0,2) = 0.0;

  result(1,0) = 0.0;
  result(1,1) = 1.0 - 3.0 * SQR( displacement[1] );
  result(1,2) = 0.0;

  result(2,0) = 0.0;
  result(2,1) = 0.0;
  result(2,2) = 1.0 - 3.0 * SQR( displacement[2] );

} // end of 'nonlin_force_density_deriv_2'


void nonlin_force_density_3(double x, double y, double z, double time,
			    DoubleVec &displacement,
			    DoubleVec &result)
{
  result[0] = -4.0 * exp( displacement[0] );
  result[1] = -5.0 * exp( 2.0*displacement[1] );
  result[2] =  0.0;

} // end of 'nonlin_force_density_3'

void nonlin_force_density_deriv_3(double x, double y, double z, double time,
				  DoubleVec &displacement,
				  SmallMatrix &result)
{
  result(0,0) = -4.0 * exp( displacement[0] );
  result(0,1) =  0.0;
  result(0,2) =  0.0;

  result(1,0) =  0.0;
  result(1,1) = -10.0 * exp( 2.0*displacement[1] );
  result(1,2) =  0.0;

  result(2,0) = result(2,1) = result(2,2) = 0.0;

} // end of 'nonlin_force_density_deriv_3'


void nonlin_force_density_4(double x, double y, double z, double time,
			    DoubleVec &displacement,
			    DoubleVec &result)
{
  result[0] = 12.0 * exp( -0.25*displacement[0] ) - 9.0 * exp( -0.5*displacement[0] );
  result[1] = -4.0 * SQR( displacement[1] ) + 8.0 * CUBE( displacement[1] );
  result[2] =  0.0;

} // end of 'nonlin_force_density_4'

void nonlin_force_density_deriv_4(double x, double y, double z, double time,
				  DoubleVec &displacement,
				  SmallMatrix &result)
{
  result(0,0) = -3.0 * exp( -0.25*displacement[0] ) + 4.5 * exp( -0.5*displacement[0] );
  result(0,1) =  0.0;
  result(0,2) =  0.0;

  result(1,0) =  0.0;
  result(1,1) = -8.0 * displacement[1] + 24.0 * SQR( displacement[1] );
  result(1,2) =  0.0;

  result(2,0) = result(2,1) = result(2,2) = 0.0;

} // end of 'nonlin_force_density_deriv_4'


void TestNonlinearForceDensity::nonlin_force_density(
                                   const Coord &coord, double time,
				   DoubleVec &displacement,
				   DoubleVec &result) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else
  double z = 0.0;
#endif
  switch (testNo)
  {
    case 1:
      nonlin_force_density_1( x, y, z, time, displacement, result );
      return;
    case 2:
      nonlin_force_density_2( x, y, z, time, displacement, result );
      return;
    case 3:
      nonlin_force_density_3( x, y, z, time, displacement, result );
      return;
    case 4:
      nonlin_force_density_4( x, y, z, time, displacement, result );
      return;
    default:
      result[0] = result[1] = result[2] = 0.0;
      return;
  }

} // end of 'TestNonlinearForceDensity::nonlin_force_density'


void TestNonlinearForceDensityNoDeriv::nonlin_force_density(
                                   const Coord &coord, double time,
				   DoubleVec &displacement,
				   DoubleVec &result) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else
  double z = 0.0;
#endif
  switch (testNo)
  {
    case 1:
      nonlin_force_density_1( x, y, z, time, displacement, result );
      return;
    case 2:
      nonlin_force_density_2( x, y, z, time, displacement, result );
      return;
    case 3:
      nonlin_force_density_3( x, y, z, time, displacement, result );
      return;
    case 4:
      nonlin_force_density_4( x, y, z, time, displacement, result );
      return;
    default:
      result[0] = result[1] = result[2] = 0.0;
      return;
  }

} // end of 'TestNonlinearForceDensity::nonlin_force_density'

void TestNonlinearForceDensity::nonlin_force_density_deriv(
                                   const Coord &coord, double time,
				   DoubleVec &displacement,
				   SmallMatrix &result) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else
  double z = 0.0;
#endif
  switch (testNo)
  {
    case 1:
      nonlin_force_density_deriv_1( x, y, z, time, displacement, result );
      return;
    case 2:
      nonlin_force_density_deriv_2( x, y, z, time, displacement, result );
      return;
    case 3:
      nonlin_force_density_deriv_3( x, y, z, time, displacement, result );
      return;
    case 4:
      nonlin_force_density_deriv_4( x, y, z, time, displacement, result );
      return;
    default:
      result(0,0) = result(0,1) = result(0,2) = 0.0;
      result(1,0) = result(1,1) = result(1,2) = 0.0;
      result(2,0) = result(2,1) = result(2,2) = 0.0;
      return;
  }

} // end of 'TestNonlinearForceDensity::nonlin_force_density_deriv'

