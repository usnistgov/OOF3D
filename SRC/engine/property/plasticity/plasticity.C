// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include "engine/property/elasticity/cijkl.h"
#include "common/coord.h"
#include "common/threadstate.h"
#include "common/trace.h"
#include "common/smallmatrix.h"
#include "engine/property/plasticity/plasticity.h"
#include "engine/property/plasticity/constitutive/constitutive.h"
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
#include "engine/property/orientation/orientation.h"


Plasticity::Plasticity(PyObject *reg, const std::string &name,
		       const Cijkl &c, PlasticConstitutiveRule *r)
  : FluxProperty(name, reg), orientation(0), xtal_cijkl_(c), rule(r)
{
  displacement = dynamic_cast<ThreeVectorField*>(Field::getField("Displacement"));
  stress_flux = dynamic_cast<SymmetricTensorFlux*>(Flux::getFlux("Stress"));
  //

}


void Plasticity::cross_reference(Material *mtl) {
  try {
    orientation = 
      dynamic_cast<OrientationPropBase*>(mtl->fetchProperty("Orientation"));
  }
  catch (ErrNoSuchProperty&) {
    // If fetchProperty failed, we have to ensure that an old pointer
    // value isn't still being stored.
    orientation = 0;
    throw;
  }
}

void Plasticity::precompute(FEMesh*) {
  // Do the orientation thing.
  if(orientation && orientation->constant_in_space()) {
    lab_cijkl_ = xtal_cijkl_.transform(orientation->orientation());
    // Also do the slip systems.

    unsigned int sz = lab_schmid_tensors.size();
    lab_schmid_tensors.resize(sz);
    for(unsigned int i=0; i<sz; ++i)
      xtal_schmid_tensors[i]=_rotate_schmid_tensor(xtal_schmid_tensors[i],
						   orientation->orientation());
	  
  }
}

void Plasticity::begin_element(const CSubProblem *c, const Element *e) {}

int Plasticity::integration_order(const CSubProblem *sp,
				  const Element *el) const {
  return el->shapefun_degree();
}

// Utility function, takes a normal and a slip direction, normalizes
// them, and computes their outer product -- this is how one makes
// Schmid tensors.  TODO: Might be handier if it could take
// initializers as arguments, which I think is a C++11 thing.
SmallMatrix *Plasticity::_normalized_outer_product(double *norm, double *slip) {
  double nmag = sqrt(norm[0]*norm[0]+norm[1]*norm[1]+norm[2]*norm[2]);
  double smag = sqrt(slip[0]*slip[0]+slip[1]*slip[1]+slip[2]*slip[2]);
  double norm_norm[3] = {norm[0]/nmag, norm[1]/nmag, norm[2]/nmag};
  double norm_slip[3] = {slip[0]/smag, slip[1]/smag, slip[2]/smag};
  
  SmallMatrix *res = new SmallMatrix(3);
  for(unsigned int i=0;i<3;++i)
    for(unsigned int j=0;j<3;++j)
      (*res)(i,j) = 0.5*(norm_norm[i]*norm_slip[j]+norm_norm[j]*norm_slip[i]);
  return res;

}

SmallMatrix *Plasticity::_rotate_schmid_tensor(SmallMatrix *m,
					       const COrientation *o) {
  SmallMatrix rtmtx = o->rotation();
  SmallMatrix *res = new SmallMatrix(3);
  
  for(unsigned int i=0; i<3; i++)
    for(unsigned int j=0; j<3; j++) {
      double &v = (*res)(i,j);
      for(unsigned int ii=0; ii<3; ii++)
	for(unsigned int jj=0; jj<3; jj++)
	  v += rtmtx(i,ii)*rtmtx(j,jj)*(*m)(ii,jj);
    }
  return res;
}

// Evaluates itself.  "Static" unclear in the context of
// an intrinsically quasistatic property.
void Plasticity::static_flux_value(const FEMesh *mesh,
				   const Element *element,
				   const Flux *flux,
				   const MasterPosition &mpt,
				   double time, SmallSystem *fluxdata)
  const
{
}


// Evaluates elasto-plastic derivatives of the stress flux wrt the
// displacement dofs.
void Plasticity::flux_matrix(const FEMesh *mesh,
			     const Element *element,
			     const ElementFuncNodeIterator&,
			     const Flux *flux,
			     const MasterPosition &mpt,
			     double time,
			     SmallSystem *fluxmtx)
  const
{
}


FCCPlasticity::FCCPlasticity(PyObject *reg, const std::string &nm,
			     const Cijkl &c, PlasticConstitutiveRule *r)
  : Plasticity(reg,nm,c,r) {

  std::cerr << xtal_cijkl_ << std::endl;
  //
  // Populate the schmid_tensor data member.
  xtal_schmid_tensors.resize(12); // 12 slip systems in FCC.
  //
  double n[3];
  double s[3];
  //
  // 1 1 1 planes.
  n[0]=1.0; n[1]=1.0; n[2]=1.0;
  //
  s[0]=-1.0; s[1]=0.0; s[2]=1.0;
  xtal_schmid_tensors[0]=_normalized_outer_product(n,s);
  //
  s[0]=0.0; s[1]=-1.0; s[2]=1.0;
  xtal_schmid_tensors[1]=_normalized_outer_product(n,s);
  //
  s[0]=-1.0; s[1]=1.0; s[2]=0.0;
  xtal_schmid_tensors[2]=_normalized_outer_product(n,s);
  //
  // 1 -1 1 planes
  n[0]=1.0; n[1]=-1.0; n[2]=1.0;
  //
  s[0]=-1.0; s[1]=0.0; s[2]=1.0;
  xtal_schmid_tensors[3]=_normalized_outer_product(n,s);
  //
  s[0]=0.0; s[1]=1.0; s[2]=1.0;
  xtal_schmid_tensors[4]=_normalized_outer_product(n,s);
  //
  s[0]=1.0; s[1]=1.0; s[2]=0.0;
  xtal_schmid_tensors[5]=_normalized_outer_product(n,s);
  //
  // -1 1 1 planes
  n[0]=-1.0; n[1]=1.0; n[2]=1.0;
  //
  s[0]=1.0; s[1]=0.0; s[2]=1.0;
  xtal_schmid_tensors[6]=_normalized_outer_product(n,s);
  //
  s[0]=0.0; s[1]=-1.0; s[2]=1.0;
  xtal_schmid_tensors[7]=_normalized_outer_product(n,s);
  //
  s[0]=1.0; s[1]=1.0; s[2]=0.0;
  xtal_schmid_tensors[8]=_normalized_outer_product(n,s);
  //
  // 1 1 -1 planes
  n[0]=1.0; n[1]=1.0; n[2]=-1.0;
  //
  s[0]=1.0; s[1]=0.0; s[2]=1.0;
  xtal_schmid_tensors[9]=_normalized_outer_product(n,s);
  //
  s[0]=0.0; s[1]=1.0; s[2]=1.0;
  xtal_schmid_tensors[10]=_normalized_outer_product(n,s);
  //
  s[0]=-1.0; s[1]=1.0; s[2]=0.0;
  xtal_schmid_tensors[11]=_normalized_outer_product(n,s);

}
