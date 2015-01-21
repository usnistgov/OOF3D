// -*- C++ -*-
// $RCSfile: nonconstant_force_density.C,v $
// $Revision: 1.8.10.3 $
// $Author: langer $
// $Date: 2014/07/17 19:44:03 $

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
#include "common/ooferror.h"
#include "common/trace.h"
#include "common/vectormath.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/indextypes.h"
#include "engine/material.h"
#include "nonconstant_force_density.h"


NonconstantForceDensity::NonconstantForceDensity(PyObject *reg,
						 const std::string &nm)
  : EqnProperty(nm,reg)
{
#if DIM==2
  displacement = dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
#elif DIM==3
  displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
#endif	// DIM==3
  stress_flux  = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}

void NonconstantForceDensity::precompute(FEMesh*) {
}

int NonconstantForceDensity::integration_order(const CSubProblem*, const Element *el) const
{
  return el->shapefun_degree();
}

void NonconstantForceDensity::force_value(const FEMesh *mesh,
					  const Element *element,
					  const Equation *eqn,
					  const MasterPosition &masterpos,
					  double time,
					  SmallSystem *eqndata) const
{
  Coord  coord = element->from_master( masterpos );
  DoubleVec force(3);

  nonconst_force_density(coord, time, force);
// #if DIM==2
//   nonconst_force_density( coord.x, coord.y, 0.0, time, force );
// #elif DIM==3
//   nonconst_force_density( coord.x, coord.y, coord.z, time, force );
// #endif

  eqndata->forceVector() += force;
//   eqndata->force_vector_element(0) += force[0];
//   eqndata->force_vector_element(1) += force[1];
// #if DIM==3
//   eqndata->force_vector_element(2) += force[2];
// #endif
}



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


inline double SQR(double x){ return x*x; }
inline double CUBE(double x){ return x*x*x; }


void TestNonconstantForceDensity::nonconst_force_density_1(
                                     double x, double y, double z, double time,
				     DoubleVec &result) const
{
  double m0 = 2.0, n0 = 3.0, p0 = 4.0;
  double m1 = 1.0, n1 = 2.0, p1 = 3.0;
  double m2 = 3.0, n2 = 2.0, p2 = 1.0;
  double pi = M_PI;
  double pi2 = M_PI*M_PI;

  result[0] = (m0*m0 + n0*n0 + p0*p0) * pi2 * sin(m0*pi*x) * sin(n0*pi*y) * sin(p0*pi*z);
  result[1] = (m1*m1 + n1*n1 + p1*p1) * pi2*  sin(m1*pi*x) * sin(n1*pi*y) * sin(p1*pi*z);
  result[2] = (m2*m2 + n2*n2 + p2*p2) * pi2*  sin(m2*pi*x) * sin(n2*pi*y) * sin(p2*pi*z);

} // end of 'TestNonconstantForceDensity::nonconst_force_density_1'


void TestNonconstantForceDensity::nonconst_force_density_2(
                                     double x, double y, double z, double time,
				     DoubleVec &result) const
{
  double pi = M_PI;
  double soln0, c0 = -0.5, m0 = 2.0, n0 = 3.0;
  double soln1, c1 = -1.5, m1 = 1.0, n1 = 2.0;

  soln0 = exp( c0*time ) * sin( m0*pi*x ) * sin( n0*pi*y );
  soln1 = exp( c1*time ) * sin( m1*pi*x ) * sin( n1*pi*y );

  result[0] = (c0*c0 + (m0*m0 + n0*n0)*pi*pi) * soln0;
  result[1] = (c1*c1 + (m1*m1 + n1*n1)*pi*pi) * soln1;

} // end of 'TestNonconstantForceDensity::nonconst_force_density_2'


void TestNonconstantForceDensity::nonconst_force_density_3(
                                     double x, double y, double z, double time,
				     DoubleVec &result) const
{
  double m = 2.0, n = 3.0, pi = M_PI;
  double Ux, Uxx, Uyy, Uyx, Vy, Vxx, Vyy, Vxy;

  // U(x,y) = sin(m*pi*x) * sin(n*pi*y)
  Ux  =  m*pi * cos(m*pi*x) * sin(n*pi*y);
  Uxx = -SQR(m*pi) * sin(m*pi*x) * sin(n*pi*y);
  Uyy = -SQR(n*pi) * sin(m*pi*x) * sin(n*pi*y);
  Uyx =  m*pi*n*pi * cos(m*pi*x) * cos(n*pi*y);

  // V(x,y) = x^2 + y^2
  Vy  =  2.0*y;
  Vxx =  2.0;
  Vyy =  2.0;
  Vxy =  0.0;

  result[0] = - ( (1.0 + 3.0*Ux*Ux)*Uxx + Uyy + Vxy );
  result[1] = - ( Vxx + (1.0 + 3.0*Vy*Vy)*Vyy + Uyx );

} // end of 'TestNonconstantForceDensity::nonconst_force_density_3'


void TestNonconstantForceDensity::nonconst_force_density_4(
                                     double x, double y, double z, double time,
				     DoubleVec &result) const
{
  double m = 2.0, n = 3.0, pi = M_PI;
  double Ux, Uy, ddU, Vx, Vy, ddV, c1=0.05, c2=0.05;

  // U(x,y) = c1 * sin(m*pi*x) * sin(n*pi*y)
  Ux  =  c1 * m*pi * cos(m*pi*x) * sin(n*pi*y);
  Uy  =  c1 * n*pi * sin(m*pi*x) * cos(n*pi*y);
  ddU = -c1 * (m*m + n*n)*pi*pi * sin(m*pi*x) * sin(n*pi*y);

  // V(x,y) = c2 * (x^2 + y^2)
  Vx  = c2 * 2.0*x;
  Vy  = c2 * 2.0*y;
  ddV = c2 * 4.0;

  result[0] = -( (1.0 + Ux)*ddU + Vx*ddV );
  result[1] = -( Uy*ddU + (1.0 + Vy)*ddV );

} // end of 'TestNonconstantForceDensity::nonconst_force_density_4'


void TestNonconstantForceDensity::nonconst_force_density_5(
                                     double x, double y, double z, double time,
				     DoubleVec &result) const
{
  double m = 2.0, n = 3.0, pi = M_PI;
  double U0x, U0xx, U0xy, U0yx, U0yy, U1y, U1xx, U1xy, U1yx, U1yy;
  double V0x, V1y, V2x, V2y;

  // U0(x,y) = sin(m*pi*x) * sin(n*pi*y),  U1(x,y) = x^2 + y^2, // displacement field
  U0x  =  m*pi * cos(m*pi*x) * sin(n*pi*y);
  U0xx = -m*pi*m*pi * sin(m*pi*x) * sin(n*pi*y);
  U0xy =  m*pi*n*pi * cos(m*pi*x) * cos(n*pi*y);
  U0yx =  n*pi*m*pi * cos(m*pi*x) * cos(n*pi*y);
  U0yy = -n*pi*n*pi * sin(m*pi*x) * sin(n*pi*y);
  U1y  =  m*pi * sin(n*pi*x) * cos(m*pi*y);
  U1xx = -n*pi*n*pi * sin(n*pi*x) * sin(m*pi*y);
  U1xy =  n*pi*m*pi * cos(n*pi*x) * cos(m*pi*y);
  U1yx =  m*pi*n*pi * cos(n*pi*x) * cos(m*pi*y);
  U1yy = -m*pi*m*pi * sin(n*pi*x) * sin(m*pi*y);
//   U1y  =  2.0*y;
//   U1xx =  U1yy = 2.0;
//   U1xy =  U1yx = 0.0;

  // V0 = -tan(dU0/dx/20),  V1 = -tan(dU1/dy / 20),
  // V2 = -tan((dU0/dx + dU1/dy) / 20),  // z-derivs of displacement
  V0x = -(1.0 + SQR( tan(U0x/20.0) )) * U0xx / 20.0;
  V1y = -(1.0 + SQR( tan(U1y/20.0) )) * U1yy / 20.0;
  V2x = -(1.0 + SQR( tan((U0x+U1y)/20.0) )) * (U0xx + U1yx) / 20.0;
  V2y = -(1.0 + SQR( tan((U0x+U1y)/20.0) )) * (U0xy + U1yy) / 20.0;
//   V0x = -U0xx / 20.0;
//   V1y = -U1yy / 20.0;
//   V2x = -(U0xx + U1yx) / 20.0;
//   V2y = -(U0xy + U1yy) / 20.0;

  result[0] = -( (1.0 + 3.0*U0x*U0x)*U0xx + (V0x + V2x)/20.0 + U0yy );
  result[1] = -( U1xx + (1.0 + 3.0*U1y*U1y)*U1yy + (V1y + V2y)/20.0 );
  result[2] = 0.0;

} // end of 'TestNonconstantForceDensity::nonconst_force_density_5'


void TestNonconstantForceDensity::nonconst_force_density(
                                     const Coord &coord, double time,
				     DoubleVec &result) const
{
  double x = coord[0];
  double y = coord[1];
#if DIM==3
  double z = coord[2];
#else  // DIM==2
  double z = 0;
#endif
  switch (testNo)
  {
    case 1:
      nonconst_force_density_1( x, y, z, time, result );
      return;
    case 2:
      nonconst_force_density_2( x, y, z, time, result );
      return;
    case 3:
      nonconst_force_density_3( x, y, z, time, result );
      return;
    case 4:
      nonconst_force_density_4( x, y, z, time, result );
      return;
    case 5:
      nonconst_force_density_5( x, y, z, time, result );
      return;
    default:
      result[0] = result[1] = result[2] = 0.0;
  }

} // end of 'TestNonconstantForceDensity::nonconst_force_density'

