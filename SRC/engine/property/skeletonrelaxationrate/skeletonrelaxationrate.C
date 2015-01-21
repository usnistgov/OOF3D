// -*- C++ -*-
// $RCSfile: skeletonrelaxationrate.C,v $
// $Revision: 1.15.10.4 $
// $Author: langer $
// $Date: 2014/12/14 01:07:54 $

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
#include "engine/IO/propertyoutput.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonelement.h"
#include "engine/csubproblem.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/flux.h"
#include "engine/material.h"
#include "engine/ooferror.h"
#include "engine/property/elasticity/cijkl.h"
#include "engine/property/elasticity/elasticity.h"
#include "engine/property/skeletonrelaxationrate/skeletonrelaxationrate.h"
#include "engine/smallsystem.h"



SkeletonRelaxationRate::SkeletonRelaxationRate(PyObject *reg,
			     const std::string &nm,
			     double gamma,
			     double alpha)
  : FluxProperty(nm,reg),
    gamma_(gamma),
    alpha_(alpha)
{
  stress_flux=dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
}

void SkeletonRelaxationRate::cross_reference(Material *mat) {
  // find out which property is the elasticity
  try {
    elasticity = dynamic_cast<Elasticity*>(mat->fetchProperty("Elasticity"));
  }
  catch (ErrNoSuchProperty&) {
    elasticity= 0;
    throw;
  }
}

void SkeletonRelaxationRate::precompute(FEMesh*) {
};

int SkeletonRelaxationRate::integration_order(const CSubProblem *mesh,
					      const Element *el) const
{
  return 0;
}


void SkeletonRelaxationRate::flux_offset(const FEMesh *mesh,
					 const Element *element,
					 const Flux *flux,
					 const MasterPosition &x,
					 double time,
					 SmallSystem *fluxdata) const {
  if(*flux!=*stress_flux) {
    throw ErrProgrammingError("Unexpected flux." __FILE__, __LINE__);
  }
  const Cijkl modulus = elasticity->cijkl(mesh, element, x);
  const CSkeletonElement * skelel = element->get_skeleton_element();

  // HomogeneityEnergy is a function of the homogeneity, which we
  // don't know, but we can ask the element, and then pass the result
  // through.
  double energyH = skelel->energyHomogeneity(mesh->get_microstructure());
  // TODO OPT: compute S in-line.
  const SymmMatrix3 S = shapetensor(element);
  for(SymTensorIterator ij; !ij.end(); ++ij) {
    double &offset_el = fluxdata->offset_vector_element(ij); // reference!
    for(SymTensorIterator kl; !kl.end(); ++kl) {
      if(kl.diagonal()) {
	offset_el += alpha_*modulus(ij,kl)*gamma_*(1.0+energyH)*energyH;
	offset_el += (1.0-alpha_)*modulus(ij,kl)*gamma_*S(kl.row(),kl.col());
      }
      else {
	offset_el += (2.0*(1.0-alpha_)*modulus(ij,kl)*gamma_
		      *S(kl.row(),kl.col()));
      }
    }
  }
}

SymmMatrix3 SkeletonRelaxationRate::shapetensor(const Element *element) const {
  SymmMatrix3 etensor;
  Coord r_c;
  const std::vector<Node*> & nl = element->get_nodelist();
  double inv_nnodes = 1./double(element->nnodes());
  for (int i = 0; i<element->nnodes(); i++)
    {
      Node * ni = nl[i];
      r_c += ni->position();
    }
  r_c *= inv_nnodes;

  Coord x;
  double xx = 0;
  double yy = 0;
  double xy = 0;
#if DIM==3
  double zz = 0;
  double xz = 0;
  double yz = 0;
#endif
  for (int i = 0; i<element->nnodes(); i++)
    {
      Node * ni = nl[i];
      x = ni->position() - r_c;
      xx += x[0]*x[0];
      yy += x[1]*x[1];
      xy += x[0]*x[1];
#if DIM==3
      zz += x[2]*x[2];
      xz += x[0]*x[2];
      yz += x[1]*x[2];
#endif	// DIM==3
    }
#if DIM==2
  double traceI = xx + yy;
#elif DIM==3
  double traceI = 2 * (xx + yy + zz); 
#endif	// DIM==3
  if (traceI == 0)
    traceI = 1.0;
  etensor(0,1) = xy/traceI;
#if DIM==2
  etensor(0,0) = (xx - yy)/(2.0*traceI);
  etensor(1,1) = -etensor(0,0);
#elif DIM==3
  double onethird = 1.0/3.0;
  double twothirds = 2.0/3.0;
  etensor(0,0) = (twothirds * xx - onethird * (yy + zz)) / traceI;
  etensor(1,1) = (twothirds * yy - onethird * (xx + zz)) / traceI;
  etensor(2,2) = (twothirds * zz - onethird * (xx + yy)) / traceI;
  etensor(0,2) = xz/traceI;
  etensor(1,2) = yz/traceI;
#endif	// DIM==3
  return etensor;
}
