// -*- C++ -*-
// $RCSfile: elasticity.C,v $
// $Revision: 1.54.4.4 $
// $Author: langer $
// $Date: 2014/07/16 21:07:19 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include "cijkl.h"
#include "common/coord.h"
#include "common/threadstate.h"
#include "common/trace.h"
#include "elasticity.h"
#include "engine/IO/propertyoutput.h"
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


Elasticity::Elasticity(const std::string &nm, PyObject *registration)
  : FluxProperty(nm, registration)
{
#if DIM==2
  displacement = dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
#elif DIM==3
  displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
#endif
  stress_flux = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}

void Elasticity::precompute(FEMesh*) {
}

int Elasticity::integration_order(const CSubProblem *subp,
				  const Element *el) const {
#if DIM==2
  if(displacement->in_plane(subp))
    return el->dshapefun_degree();
#endif
  return el->shapefun_degree();
}

void Elasticity::static_flux_value(const FEMesh *mesh, const Element *element,
				   const Flux *flux, const MasterPosition &pt,
				   double time, SmallSystem *fluxdata)
  const
{
  // Unexpected fluxes are bad.
  if (*flux != *stress_flux) {
    throw ErrProgrammingError("Unexpected flux", __FILE__, __LINE__);
  }

  SymmMatrix3 strain;
  geometricStrain(mesh, element, pt, &strain);
  const Cijkl modulus = cijkl( mesh, element, pt );

  for (SymTensorIterator ij; !ij.end(); ++ij) {
    // TODO OPT: Use modulus(ij,kl) where ij and kl are voigt ints.
    // Unroll the ij loop too.
    int i = ij.row();
    int j = ij.col();
    fluxdata->flux_vector_element( ij ) +=
      (modulus( i,j,0,0 ) * strain( 0,0 ) +
       modulus( i,j,1,1 ) * strain( 1,1 ) +
       modulus( i,j,2,2 ) * strain( 2,2 ) +
       2*modulus( i,j,0,1 ) * strain( 0,1 ) +
       2*modulus( i,j,0,2 ) * strain( 0,2 ) +
       2*modulus( i,j,1,2 ) * strain( 1,2 ));
  }
} // end of 'Elasticity::static_flux_value'

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Elasticity::flux_matrix(const FEMesh *mesh, const Element *element,
			     const ElementFuncNodeIterator &node,
			     const Flux *flux, const MasterPosition &x,
			     double time, SmallSystem *fluxmtx)
  const
{
  // Unexpected fluxes are bad.
  if (*flux != *stress_flux) {
    throw ErrProgrammingError("Unexpected flux", __FILE__, __LINE__);
  }

#if DIM == 2
  double shapeFuncVal     = node.shapefunction( x );
#endif // DIM == 2

  double shapeFuncGrad0 = node.dshapefunction( 0, x );
  double shapeFuncGrad1 = node.dshapefunction( 1, x );
#if DIM==3
  double shapeFuncGrad2 = node.dshapefunction( 2, x );
#endif	// DIM == 3

  const Cijkl modulus = cijkl( mesh, element, x );

  IteratorP ell = displacement->iterator(); // reuse this;

  for (SymTensorIterator ij; !ij.end(); ++ij) {

    // loop over displacement components for strain contributions
    // (just in-plane, in 2D)
    for( ; !ell.end(); ++ell) {

      // loop over k=0,1 is written out explicitly to save a tiny bit of time
      SymTensorIndex ell0( 0, ell.integer() );
      SymTensorIndex ell1( 1, ell.integer() );

#if DIM==2
      fluxmtx->stiffness_matrix_element( ij, displacement, ell, node ) +=
                                   modulus( ij, ell0 ) * shapeFuncGrad0 +
                                   modulus( ij, ell1 ) * shapeFuncGrad1;
#elif DIM==3
      SymTensorIndex ell2( 2, ell.integer() );
      fluxmtx->stiffness_matrix_element( ij, displacement, ell, node ) +=
	                           modulus( ij, ell0 ) * shapeFuncGrad0 +
                                   modulus( ij, ell1 ) * shapeFuncGrad1 +
                                   modulus( ij, ell2 ) * shapeFuncGrad2;
#endif
    } // end of loop over ell

    ell.reset();

#if DIM==2
    // loop over out-of-plane strains
    if (!displacement->in_plane(mesh))
    {
      Field *oop = displacement->out_of_plane();

      for(IteratorP kay = oop->iterator( ALL_INDICES ); !kay.end(); ++kay)
      {
	// There are no net factors of 1/2 or 2 here for the
	// off-diagonal terms, dammit.
	fluxmtx->stiffness_matrix_element( ij, oop, kay, node )
	  += shapeFuncVal * modulus( ij, SymTensorIndex( 2, kay.integer()) );
      }
    } // end if
#endif
  } // end of loop over ij

} // end of 'Elasticity::flux_matrix'

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Elasticity::geometricStrain(const FEMesh *mesh, const Element *element,
				 const MasterPosition &pos,
				 SymmMatrix3 *strain)
  const
{
  findGeometricStrain(mesh, element, pos, strain, false);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void Elasticity::output(const FEMesh *mesh,
			const Element *element,
			const PropertyOutput *output,
			const MasterPosition &pos,
			OutputVal *data)
  const
{
  const std::string &outputname = output->name();
  if(outputname == "Energy") {
    // The parameter is a Python Enum instance.  Extract its value.
    // The name of the parameter is 'etype', set in outputDefs.py when
    // the ScalarPropertyOutputRegistration for "Energy" was created.
    const std::string *etype = output->getEnumParam("etype");
    if(*etype == "Total" || *etype == "Elastic") {
      ScalarOutputVal *edata =
	dynamic_cast<ScalarOutputVal*>(data);
      SymmMatrix3 strain;
      const Cijkl modulus = cijkl(mesh, element, pos);
      geometricStrain(mesh, element, pos, &strain);
      SymmMatrix stress(modulus*strain);
      double e = 0;
      for(int i=0; i<3; i++) {
	e += stress(i,i)*strain(i,i);
	int j = (i+1)%3;
	e += 2*stress(i,j)*strain(i,j);
      }
      *edata += 0.5*e;
    }
    delete etype;
  }
} // end of 'Elasticity::output'

