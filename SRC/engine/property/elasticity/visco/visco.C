// -*- C++ -*-
// $RCSfile: visco.C,v $
// $Revision: 1.5.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:38 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include "engine/property/elasticity/visco/visco.h"
#include "engine/flux.h"
#include "engine/field.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/smallsystem.h"


ViscoElasticityProp::ViscoElasticityProp(PyObject *registration,
				       const std::string &nm,
				       Cijkl *g)
  : FluxProperty(nm,registration),
    g_ijkl(*g)
{
#if DIM==2
  displacement = dynamic_cast<TwoVectorField*>(Field::getField("Displacement"));
#elif DIM==3
  displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
#endif
  stress_flux = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}

int ViscoElasticityProp::integration_order(const CSubProblem *subp,
					   const Element *el)
  const
{
#if DIM==2
  if(displacement->in_plane(subp))
    return el->dshapefun_degree();
#endif
  return el->shapefun_degree();
}

void ViscoElasticityProp::flux_matrix(const FEMesh *mesh,
				      const Element *element,
				      const ElementFuncNodeIterator &nu,
				      const Flux *flux,
				      const MasterPosition &x,
				      double time,
				      SmallSystem *fluxmtx) const
{
  if(*flux != *stress_flux) {
    throw ErrProgrammingError("Unexpected flux", __FILE__, __LINE__);
  }

#if DIM==2
  double sf = nu.shapefunction(x);
#endif // DIM==2
  double dsf0 = nu.dshapefunction(0, x);
  double dsf1 = nu.dshapefunction(1, x);
#if DIM==3
  double dsf2 = nu.dshapefunction(2, x);
#endif	// DIM==3

  IteratorP ell = displacement->iterator(); // reuse this;
  for(SymTensorIterator ij; !ij.end(); ++ij) {
    // loop over displacement components for in-plane strain contributions
    for( ; !ell.end(); ++ell) {
      // loop over k=0,1 is written out explicitly to save a tiny bit of time
      SymTensorIndex ell0(0, ell.integer());
      SymTensorIndex ell1(1, ell.integer());
#if DIM==2
      fluxmtx->damping_matrix_element(ij, displacement, ell, nu) +=
	g_ijkl(ij, ell0)*dsf0 + g_ijkl(ij, ell1)*dsf1;
#elif DIM==3
      SymTensorIndex ell2(2, ell.integer());
      fluxmtx->damping_matrix_element(ij, displacement, ell, nu) +=
	g_ijkl(ij, ell0)*dsf0 + g_ijkl(ij, ell1)*dsf1 + g_ijkl(ij, ell2)*dsf2;
#endif	// DIM==3
    }
    ell.reset();
    // loop over out-of-plane strains
#if DIM==2
    if(!displacement->in_plane(mesh)) {
      Field *oop = displacement->out_of_plane();
      for(IteratorP ell=oop->iterator(ALL_INDICES); !ell.end(); ++ell) {
	double diag_factor = ( ell.integer()==2 ? 1.0 : 0.5);
	fluxmtx->damping_matrix_element(ij, oop, ell, nu)
	  += g_ijkl(ij, SymTensorIndex(2, ell.integer())) * sf * diag_factor;
      }
    }
#endif
  } // end loop over ij
}
