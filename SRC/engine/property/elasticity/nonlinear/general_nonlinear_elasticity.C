// -*- C++ -*-
// $RCSfile: general_nonlinear_elasticity.C,v $
// $Revision: 1.17.4.4 $
// $Author: fyc $
// $Date: 2014/07/29 21:21:52 $

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
#include "common/threadstate.h"
#include "common/trace.h"
#include "engine/IO/propertyoutput.h"
#include "engine/cnonlinearsolver.h"
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
#include "engine/smalltensor.h"
#include "general_nonlinear_elasticity.h"


GeneralNonlinearElasticityNoDeriv::GeneralNonlinearElasticityNoDeriv(PyObject *registration, const std::string &nm)
  : FluxProperty(nm, registration)
{
#if DIM==2
  displacement = dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
#elif DIM==3
  displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
#endif
  stress_flux = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}


int GeneralNonlinearElasticityNoDeriv::integration_order(const CSubProblem *subp,
							 const Element *el) const {
#if DIM==2
  if(displacement->in_plane(subp))
    return el->dshapefun_degree();
#endif
  return el->shapefun_degree();
}


void GeneralNonlinearElasticityNoDeriv::static_flux_value(
				  const FEMesh  *mesh,
				  const Element *element,
				  const Flux    *flux,
				  const MasterPosition &pt,
				  double time,
				  SmallSystem *fluxdata) const
{
  DoubleVec dispVec(3);
  SmallMatrix dispGrad(3);
  SmallMatrix stress(3);


  // first compute the displacement and its gradient at the given point

  computeDisplacement( mesh, element, pt, dispVec );
  computeDisplacementGradient( mesh, element, pt, dispGrad );


  // compute the value of stress with the user-defined function

  Coord coord = element->from_master( pt );

  // TODO MER: Why not just pass the Coord to nonlin_stress(), instead of
  // passing the components separately?

#if DIM==2
  nonlin_stress( coord[0], coord[1], 0.0, time, dispVec, dispGrad, stress );
#elif DIM==3
  nonlin_stress( coord[0], coord[1], coord[2], time, dispVec, dispGrad, stress );
#endif


  // now we can plug in the flux element values to fluxdata

  for (SymTensorIterator ij; !ij.end(); ++ij)

    fluxdata->flux_vector_element( ij ) += stress( ij.row(), ij.col() );


} // end of 'GeneralNonlinearElasticityNoDeriv::static_flux_value'


void GeneralNonlinearElasticity::flux_matrix(const FEMesh *mesh,
					     const Element *element,
					     const ElementFuncNodeIterator &node,
					     const Flux *flux,
					     const MasterPosition &pt,
					     double time,
					     SmallSystem *fluxmtx)
  const
{
  DoubleVec dispVec(3, 0.0);
  SmallMatrix dispGrad(3);
  SmallTensor3 stressDeriv1;
  SmallTensor4 stressDeriv2;


  // check for unexpected flux, should be stress flux

  if (*flux != *stress_flux) {
    throw ErrProgrammingError("Unexpected flux", __FILE__, __LINE__);
  }


  // first compute the displacement and its gradient at the given point

  computeDisplacement( mesh, element, pt, dispVec );
  computeDisplacementGradient( mesh, element, pt, dispGrad );


  // evaluate the value of flux derivatives with the given pt, time,
  // displacement etc

  Coord coord = element->from_master( pt );

  // the derivative of the stress flux mapping w.r.t. displacement field
#if DIM==2
  // TODO MER: Why not just pass the Coord to nonlin_stress_etc(), instead of
  // passing the components separately?

  nonlin_stress_deriv_wrt_displacement( coord[0], coord[1], 0.0, time,
					dispVec, dispGrad, stressDeriv1 );
#elif DIM==3
  nonlin_stress_deriv_wrt_displacement( coord[0], coord[1], coord[2], time,
					dispVec, dispGrad, stressDeriv1 );
#endif
  // the derivative of the stress flux mapping w.r.t. displacement gradient
#if DIM==2
  nonlin_stress_deriv_wrt_displacement_gradient(coord[0], coord[1], 0.0, time,
						dispVec, dispGrad, stressDeriv2);
#elif DIM==3
  nonlin_stress_deriv_wrt_displacement_gradient(coord[0], coord[1], coord[2],
						time,
						dispVec, dispGrad, stressDeriv2);
#endif


  // evaluate the shape function and its gradient at the given node j

  double shapeFuncVal     = node.shapefunction( pt );
  double shapeFuncGrad0 = node.dshapefunction( 0, pt );
  double shapeFuncGrad1 = node.dshapefunction( 1, pt );
#if DIM==3
  double shapeFuncGrad2 = node.dshapefunction( 2, pt );
#endif


  // finally add the contributions to the stiffness matrix element

  IteratorP kay = displacement->iterator(); // to iterate over components of disp.

  for (SymTensorIterator ij; !ij.end(); ++ij) {

    int i = ij.row(), j = ij.col();

#if DIM==2

    for( ; !kay.end(); ++kay) { // loop over kth component of displacement

      int k = kay.integer();

      fluxmtx->stiffness_matrix_element( ij, displacement, kay, node ) +=
	stressDeriv1(i,j,k) * shapeFuncVal +
	stressDeriv2(i,j,k,0) * shapeFuncGrad0 +
	stressDeriv2(i,j,k,1) * shapeFuncGrad1;
    } // End of kay loop.

    if ( !displacement->in_plane( mesh ) ){
      Field *disp_z_deriv = displacement->out_of_plane();
      for(IteratorP kayo = disp_z_deriv->iterator( ALL_INDICES );
	  !kayo.end(); ++kayo) {
	int ko = kayo.integer();

	fluxmtx->stiffness_matrix_element( ij, disp_z_deriv, kayo, node ) +=
	  stressDeriv2(i,j,ko,2) * shapeFuncVal;
      }
    }

#elif DIM==3

    // This loop is repeated here because if you start it once and
    // terminate it twice in different branches of the ifdef, the
    // editor gets all confused and can't match up the brackets, and
    // the indenting all breaks.

    for( ; !kay.end(); ++kay) { // loop over kth component of displacement
      int k = kay.integer();

      fluxmtx->stiffness_matrix_element( ij, displacement, kay, node ) +=
    	             stressDeriv1(i,j,k) * shapeFuncVal +
   	             stressDeriv2(i,j,k,0) * shapeFuncGrad0 +
	             stressDeriv2(i,j,k,1) * shapeFuncGrad1 +
	             stressDeriv2(i,j,k,2) * shapeFuncGrad2;
    } // End of kay loop.

#endif

    kay.reset();

  } // end of loop over ij

} // end of 'GeneralNonlinearElasticity::flux_matrix'


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


inline double SQR(double x){ return x*x; }
inline double CUBE(double x){ return x*x*x; }


void nonlin_stress_1(double x, double y, double z, double time,
		     DoubleVec &displacement,
		     SmallMatrix &dispGrad,
		     SmallMatrix &stress)
{
  stress(0,0) = dispGrad(0,0) + CUBE( dispGrad(0,0) );
  stress(0,1) = dispGrad(0,1) + dispGrad(1,0);
  stress(0,2) = dispGrad(0,2) + dispGrad(2,0);

  stress(1,0) = dispGrad(0,1) + dispGrad(1,0);
  stress(1,1) = dispGrad(1,1) + CUBE( dispGrad(1,1) );
  stress(1,2) = dispGrad(1,2) + dispGrad(2,1);

  stress(2,0) = dispGrad(0,2) + dispGrad(2,0);
  stress(2,1) = dispGrad(1,2) + dispGrad(2,1);
  stress(2,2) = dispGrad(2,2) + CUBE( dispGrad(2,2) );

} // end of 'nonlin_stress_1'


void nonlin_stress_deriv_wrt_displacement_1(double x, double y, double z,
					    double time,
					    DoubleVec &displacement,
					    SmallMatrix &dispGrad,
					    SmallTensor3 &stress_deriv)
{
  for (int i = 0; i < 3; i++) {
    stress_deriv(i,0,0) = stress_deriv(i,0,1) = stress_deriv(i,0,2) = 0.0;
    stress_deriv(i,1,0) = stress_deriv(i,1,1) = stress_deriv(i,1,2) = 0.0;
    stress_deriv(i,2,0) = stress_deriv(i,2,1) = stress_deriv(i,2,2) = 0.0;
  }

} // end of 'nonlin_stress_deriv_wrt_displacement_1'


void nonlin_stress_deriv_wrt_displacement_gradient_1(
                                        double x, double y, double z, double time,
					DoubleVec &displacement,
					SmallMatrix &dispGrad,
					SmallTensor4 &stress_deriv)
{
  for (int i = 0; i < 3; i++)
    for (int j = 0; j < 3; j++) {
      stress_deriv(i,j,0,0) = stress_deriv(i,j,0,1) = stress_deriv(i,j,0,2) = 0.0;
      stress_deriv(i,j,1,0) = stress_deriv(i,j,1,1) = stress_deriv(i,j,1,2) = 0.0;
      stress_deriv(i,j,2,0) = stress_deriv(i,j,2,1) = stress_deriv(i,j,2,2) = 0.0;
    }

  stress_deriv(0,0,0,0) = 1.0 + 3.0 * SQR( dispGrad(0,0) );
  stress_deriv(0,1,0,1) = 1.0;
  stress_deriv(0,1,1,0) = 1.0;
  stress_deriv(1,1,1,1) = 1.0 + 3.0 * SQR( dispGrad(1,1) );
  stress_deriv(1,0,0,1) = 1.0;
  stress_deriv(1,0,1,0) = 1.0;

} // end of 'nonlin_stress_deriv_wrt_displacement_gradient_1'


void nonlin_stress_2(double x, double y, double z, double time,
		     DoubleVec &displacement,
		     SmallMatrix &dispGrad,
		     SmallMatrix &stress)
{
  stress(0,0) = dispGrad(0,0) + CUBE( dispGrad(0,0) ) +
                 ( dispGrad(0,2) + dispGrad(2,0) + dispGrad(2,2) )/20.0;
  stress(0,1) = dispGrad(0,1);
  stress(0,2) = dispGrad(0,0)/20.0 + atan( dispGrad(0,2) + dispGrad(2,0) );

  stress(1,0) = dispGrad(1,0);
  stress(1,1) = dispGrad(1,1) + CUBE( dispGrad(1,1) ) +
 	         ( dispGrad(1,2) + dispGrad(2,1) + dispGrad(2,2) )/20.0;
  stress(1,2) = dispGrad(1,1)/20.0 + atan( dispGrad(1,2) + dispGrad(2,1) );

  stress(2,0) = dispGrad(0,0)/20.0 + atan( dispGrad(0,2) + dispGrad(2,0) );
  stress(2,1) = dispGrad(1,1)/20.0 + atan( dispGrad(1,2) + dispGrad(2,1) );
  stress(2,2) = ( dispGrad(0,0) + dispGrad(1,1) )/20.0 + atan( dispGrad(2,2) );

} // end of 'nonlin_stress_2'


void nonlin_stress_deriv_wrt_displacement_2(double x, double y, double z,
					    double time,
					    DoubleVec &displacement,
					    SmallMatrix &dispGrad,
					    SmallTensor3 &stress_deriv)
{
  for (int i = 0; i < 3; i++) {
    stress_deriv(i,0,0) = stress_deriv(i,0,1) = stress_deriv(i,0,2) = 0.0;
    stress_deriv(i,1,0) = stress_deriv(i,1,1) = stress_deriv(i,1,2) = 0.0;
    stress_deriv(i,2,0) = stress_deriv(i,2,1) = stress_deriv(i,2,2) = 0.0;
  }

} // end of 'nonlin_stress_deriv_wrt_displacement_2'


void nonlin_stress_deriv_wrt_displacement_gradient_2(
                                        double x, double y, double z, double time,
					DoubleVec &u,
					SmallMatrix &du,
					SmallTensor4 &s)
{
  for (int i = 0; i < 3; i++)
    for (int j = 0; j < 3; j++) {
      s(i,j,0,0) = s(i,j,0,1) = s(i,j,0,2) = 0.0;
      s(i,j,1,0) = s(i,j,1,1) = s(i,j,1,2) = 0.0;
      s(i,j,2,0) = s(i,j,2,1) = s(i,j,2,2) = 0.0;
    }

  s(0,0,0,0) = 1.0 + 3.0 * SQR( du(0,0) );
  s(1,1,1,1) = 1.0 + 3.0 * SQR( du(1,1) );
  s(2,2,2,2) = 1.0 / (1.0 + SQR( du(2,2) ));

  s(0,1,0,1) = s(1,0,1,0) = 1.0;

  s(0,2,0,2) = s(0,2,2,0) = s(2,0,0,2) = s(2,0,2,0)
                = 1.0 / (1.0 + SQR( du(0,2) + du(2,0) ));

  s(1,2,1,2) = s(1,2,2,1) = s(2,1,1,2) = s(2,1,2,1)
                = 1.0 / (1.0 + SQR( du(1,2) + du(2,1) ));

  s(0,0,0,2) = s(0,0,2,0) = s(0,0,2,2) = s(0,2,0,0)
             = s(1,1,1,2) = s(1,1,2,1) = s(1,1,2,2)
             = s(1,2,1,1) = s(2,0,0,0) = s(2,1,1,1)
             = s(2,2,0,0) = s(2,2,1,1) = 1.0/20.0;

} // end of 'nonlin_stress_deriv_wrt_displacement_gradient_2'


void TestGeneralNonlinearElasticityNoDeriv::nonlin_stress(
                                        double x, double y, double z, double time,
					DoubleVec &displacement,
					SmallMatrix &dispGrad,
					SmallMatrix &stress) const
{
  switch (testNo)
  {
    case 1:
      nonlin_stress_1( x, y, z, time, displacement, dispGrad, stress );
      return;

    case 2:
      nonlin_stress_2( x, y, z, time, displacement, dispGrad, stress );
      return;

    default:
      for (int i=0; i<3; i++)
	stress(i,0) = stress(i,1) = stress(i,2) = 0.0;
  }

} // end of 'TestGeneralNonlinearElasticityNoDeriv::nonlin_stress'


void TestGeneralNonlinearElasticity::nonlin_stress(
                                        double x, double y, double z, double time,
					DoubleVec &displacement,
					SmallMatrix &dispGrad,
					SmallMatrix &stress) const
{
  switch (testNo)
  {
    case 1:
      nonlin_stress_1( x, y, z, time, displacement, dispGrad, stress );
      return;

    case 2:
      nonlin_stress_2( x, y, z, time, displacement, dispGrad, stress );
      return;

    default:
      for (int i=0; i<3; i++)
	stress(i,0) = stress(i,1) = stress(i,2) = 0.0;
  }

} // end of 'TestGeneralNonlinearElasticity::nonlin_stress'


void TestGeneralNonlinearElasticity::nonlin_stress_deriv_wrt_displacement(
                                        double x, double y, double z, double time,
					DoubleVec &displacement,
					SmallMatrix &dispGrad,
					SmallTensor3 &stress_deriv) const
{
  switch (testNo)
  {
    case 1:
      nonlin_stress_deriv_wrt_displacement_1( x, y, z, time,
					      displacement, dispGrad, stress_deriv );
      return;

    case 2:
      nonlin_stress_deriv_wrt_displacement_2( x, y, z, time,
					      displacement, dispGrad, stress_deriv );
      return;

    default:
      for (int i = 0; i < 3; i++) {
	stress_deriv(i,0,0) = stress_deriv(i,0,1) = stress_deriv(i,0,2) = 0.0;
	stress_deriv(i,1,0) = stress_deriv(i,1,1) = stress_deriv(i,1,2) = 0.0;
	stress_deriv(i,2,0) = stress_deriv(i,2,1) = stress_deriv(i,2,2) = 0.0;
      }
  }

} // end of 'TestGeneralNonlinearElasticity::nonlin_stress_deriv_wrt_displacement'


void TestGeneralNonlinearElasticity::nonlin_stress_deriv_wrt_displacement_gradient(
                                        double x, double y, double z, double time,
					DoubleVec &displacement,
					SmallMatrix &dispGrad,
					SmallTensor4 &stress_deriv) const
{
  switch (testNo)
  {
    case 1:
      nonlin_stress_deriv_wrt_displacement_gradient_1( x, y, z, time,
						       displacement, dispGrad,
						       stress_deriv );
      return;

    case 2:
      nonlin_stress_deriv_wrt_displacement_gradient_2( x, y, z, time,
						       displacement, dispGrad,
						       stress_deriv );
      return;

    default:
      for (int i = 0; i < 3; i++)
	for (int j = 0; j < 3; j++) {
	  stress_deriv(i,j,0,0) = stress_deriv(i,j,0,1) = stress_deriv(i,j,0,2) = 0.0;
	  stress_deriv(i,j,1,0) = stress_deriv(i,j,1,1) = stress_deriv(i,j,1,2) = 0.0;
	  stress_deriv(i,j,2,0) = stress_deriv(i,j,2,1) = stress_deriv(i,j,2,2) = 0.0;
	}
  }

} // end of 'TestGeneralNonlinearElasticity::nonlin_stress_deriv_wrt_displacement_gradient'
