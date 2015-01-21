// -*- C++ -*-
// $RCSfile: nonconstant_heat_source.C,v $
// $Revision: 1.10.4.4 $
// $Author: langer $
// $Date: 2014/07/28 20:23:46 $

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
#include "nonconstant_heat_source.h"
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





NonconstantHeatSource::NonconstantHeatSource(PyObject *reg,
					     const std::string &name)
  : EqnProperty(name,reg)
{
    heat_flux = dynamic_cast<VectorFlux*>(Flux::getFlux("Heat_Flux"));
}


int NonconstantHeatSource::integration_order(const CSubProblem *subp,
					     const Element *el) const
{
  return el->shapefun_degree();
}

void NonconstantHeatSource::force_value(const FEMesh *mesh,
					const Element *element,
					const Equation *eqn,
					const MasterPosition &masterpos,
					double time,
					SmallSystem *eqndata) const
{
  Coord coord = element->from_master( masterpos );

#if DIM==2
  eqndata->force_vector_element(0) -= nonconst_heat_source( coord[0], coord[1], 0.0, time );
#elif DIM==3
  eqndata->force_vector_element(0) -= nonconst_heat_source( coord[0], coord[1], coord[2], time );
#endif
}



//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


inline double SQR(double x){ return x*x; }
inline double CUBE(double x){ return x*x*x; }


double TestNonconstantHeatSource::nonconst_heat_source_1(
                                  double x, double y, double z, double time) const
{
  // Updated for 3D
  double source_value;
  double m = 2.0, n = 3.0, p = 4.0, pi = M_PI;

  source_value = -(m*m + n*n + p*p) * SQR(pi) * sin( m*pi*x ) * sin( n*pi*y ) * sin(p*pi*z);

  return source_value;

} // end of 'TestNonconstantHeatSource::nonconstant_heat_source_1'


double TestNonconstantHeatSource::nonconst_heat_source_2(
                                  double x, double y, double z, double time) const
{
  double source_value;
  double m = 2.0, n = 3.0, p = 4.0, pi = M_PI;

  source_value  = -(m*m + n*n +p*p) * SQR(pi) 
    * sin( m*pi*x ) * sin( n*pi*y ) * sin(p*pi*z);
  source_value -= SQR( m*pi* cos(m*pi*x)*sin(n*pi*y)*sin(p*pi*z) )
    * SQR(m*pi) * sin( m*pi*x ) * sin( n*pi*y ) * sin(p*pi*z);
  source_value -= pow( n*pi* sin(m*pi*x)*cos(n*pi*y)*sin(p*pi*z), 4.0 )
    * SQR(n*pi) * sin( m*pi*x ) * sin( n*pi*y ) * sin(p*pi*z) / 10.0;

  return source_value;

} // end of 'TestNonconstantHeatSource::nonconstant_heat_source_2'


double TestNonconstantHeatSource::nonconst_heat_source_3(
                                  double x, double y, double z, double time) const
{
  double source_value;
  double w = -1.5, m = 2.0, n = 3.0, pi = M_PI;

  source_value = -(w + (m*m + n*n)*pi*pi) * exp(w*time) * sin( m*pi*x ) * sin( n*pi*y );

  return source_value;

} // end of 'TestNonconstantHeatSource::nonconstant_heat_source_3'


double TestNonconstantHeatSource::nonconst_heat_source_4(
                                  double x, double y, double z, double time) const
{
  double Ux, Uy, Uz,Uxx, Uxy, Uyx, Uyy, Uzx, Uzy, source_value;
  double m = 2.0, n = 3.0, pi = M_PI;

  // nonlinear flux = -( Ux+Ux^3+Uz/20, Uy+Uy^3+Uz/20, Ux/20+Uy/20+arctan(Uz) )
  Ux =  m*pi * cos(m*pi*x) * sin(n*pi*y);
  Uy =  n*pi * sin(m*pi*x) * cos(n*pi*y);
  Uz = -tan( (Ux + Uy) / 20.0 );

  Uxx = -m*m*pi*pi * sin(m*pi*x) * sin(n*pi*y);
  Uxy =  m*n*pi*pi * cos(m*pi*x) * cos(n*pi*y);
  Uyx =  Uxy;
  Uyy = -n*n*pi*pi * sin(m*pi*x) * sin(n*pi*y);

  Uzx = -(1.0 + Uz*Uz) * (Uxx + Uyx) / 20.0;
  Uzy = -(1.0 + Uz*Uz) * (Uxy + Uyy) / 20.0;

  // source = -div(flux) = -( d(flux0)/dx + d(flux1)/dy )
  source_value  = (1.0 + 3.0*Ux*Ux)*Uxx + Uzx/20.0 +
                  (1.0 + 3.0*Uy*Uy)*Uyy + Uzy/20.0;

  return source_value;

} // end of 'TestNonconstantHeatSource::nonconstant_heat_source_4'


double TestNonconstantHeatSource::nonconst_heat_source_5(
                                  double x, double y, double z, double time)
  const
{
  double m = 2.0, n = 3.0, p = 4.0;

  double sx = sin(m*M_PI*x);
  double sy = sin(n*M_PI*y);
  double sz = sin(p*M_PI*z);

  double Ux  = m*M_PI * cos(m*M_PI*x) * sy * sz;
  double Uy  = n*M_PI * sx * cos(n*M_PI*y) * sz;
  double Uz  = p*M_PI * sx * sy * cos(p*M_PI*z);

  return -M_PI*M_PI*sx*sy*sz*(
		     m*m/(1.+Ux*Ux) + n*n/(1.+Uy*Uy) + p*p/(1.+Uz*Uz) );

} // end of 'TestNonconstantHeatSource::nonconstant_heat_source_5'

double TestNonconstantHeatSource::nonconst_heat_source_6(
                                  double x, double y, double z, double time) const
{
  double Ut, Ux, Uy, Uxx, Uyy, source_value;
  double w = -1.5, m = 2.0, n = 3.0, pi = M_PI;

  Ut  = w * exp(w*time) * sin(m*pi*x) * sin(n*pi*y);
  Ux  = m*pi * exp(w*time) * cos(m*pi*x) * sin(n*pi*y);
  Uy  = n*pi * exp(w*time) * sin(m*pi*x) * cos(n*pi*y);

  Uxx = -m*m*pi*pi * exp(w*time) * sin(m*pi*x) * sin(n*pi*y);
  Uyy = -n*n*pi*pi * exp(w*time) * sin(m*pi*x) * sin(n*pi*y);

  source_value = -Ut + Uxx*(1.0 + Ux*Ux) + Uyy*(1.0 + pow(Uy,4.0)/10.0);

  return source_value;

} // end of 'TestNonconstantHeatSource::nonconstant_heat_source_6'

double TestNonconstantHeatSource::nonconst_heat_source_7(
                                  double x, double y, double z, double t) const
{
  double Ut, Ux, Uy, Uxx, Uyy, source_value;
  double w = 1.5, m = 2.0, n = 3.0, pi = M_PI;
  double k = 1;

  // U = sin(m*pi*x) * sin(n*pi*y) * sin(pi*(k*x - w*t))
  Ut  = -pi*w * sin(m*pi*x) * sin(n*pi*y) * cos(pi*(k*x-w*t));

  Ux  = m*pi * cos(m*pi*x) * sin(n*pi*y) * sin(pi*(k*x-w*t)) 
    + k*pi * sin(m*pi*x) * sin(n*pi*y) * cos(pi*(k*x - w*t));
  
  Uxx = -(m*m + k*k)*pi*pi * sin(m*pi*x) * sin(n*pi*y)* sin(n*pi*(x-w*t))
    + 2*m*k*pi*pi * cos(m*pi*x) * sin(n*pi*y) * cos(pi*(k*x - w*t));
  
  Uy  = n*pi * sin(m*pi*x) * cos(n*pi*y) * sin(pi*(k*x - w*t));
  Uyy = -n*n*pi*pi * sin(m*pi*x) * sin(n*pi*y) * sin(pi*(k*x-w*t));

  source_value = -Ut + Uxx*(1.0 + Ux*Ux) + Uyy*(1.0 + pow(Uy,4.0)/10.0);

  return source_value;

} // end of 'TestNonconstantHeatSource::nonconstant_heat_source_7'

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#define AA 3

static double f(double x, double t) {
  //  return 0.5*(x-AA*t)*(x-AA*t);
  return exp(AA*t*x);
}

static double dfdx(double x, double t) {
  // return (x-AA*t);
  return AA*t*f(x,t);
}

static double d2fdx2(double x, double t) {
  // return 1;
  return (AA*AA*t*t)*f(x,t);
}

static double dfdt(double x, double t) {
  // return -AA*(x-AA*t);
  return AA*x*f(x,t);
}

double TestNonconstantHeatSource::nonconst_heat_source_8(
				    double x, double y, double z, double t)
  const 
{
  // For T = (x^2 - x) (y^2 - y) f(x,t) and the nonlinear
  // conductivity given by
  // TestNonlinearHeatConductivity::nonlin_heat_flux1.

  double xx1 = x*x - x;
  double yy1 = y*y - y;
  double fxt = f(x,t);
  // The 100 is the heat capacity in TEST/nonlinear_K_timedep_tests.py.
  double Ut = 100*xx1 * yy1 * dfdt(x,t);
  double Ux = ((2*x-1)*fxt + xx1*dfdx(x,t)) * yy1;
  double Uxx = (2*fxt + 2*(2*x-1)*dfdx(x,t) + xx1*d2fdx2(x,t)) * yy1;
  double Uy = xx1*(2*y-1)*fxt;
  double Uyy = 2*xx1*fxt;

  return -Ut + Uxx*(1.0 + Ux*Ux) + Uyy*(1.0 + pow(Uy,4.0)/10.0);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

double TestNonconstantHeatSource::nonconst_heat_source(
			       double x, double y, double z, double time)
  const
{
  // The minus sign in all of these test functions is necessary
  // because the sign of the Qdot term in the heat equation changed
  // for version 2.1.2.
  switch (testNo) {
  case 1:
    return -nonconst_heat_source_1( x, y, z, time );
  case 2:
    return -nonconst_heat_source_2( x, y, z, time );
  case 3:
    return -nonconst_heat_source_3( x, y, z, time );
  case 4:
    return -nonconst_heat_source_4( x, y, z, time );
  case 5:
    return -nonconst_heat_source_5( x, y, z, time );
  case 6:
    return -nonconst_heat_source_6(x, y, z, time);
  case 7:
    return -nonconst_heat_source_7(x, y, z, time);
  case 8:
    return -nonconst_heat_source_8(x, y, z, time);
  default:
    return 0.0;
  }
} // end of 'TestNonconstantHeatSource::nonconst_heat_source'
