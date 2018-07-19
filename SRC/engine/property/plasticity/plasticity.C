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
#include "common/cleverptr.h"
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
#include "engine/outputval.h"
#include "engine/planarity.h"
#include "engine/smallsystem.h"
#include "engine/property/orientation/orientation.h"


Plasticity::Plasticity(PyObject *reg, const std::string &name,
		       const Cijkl &c, PlasticConstitutiveRule *r,
		       const int slips)
  : FluxProperty(name, reg), nslips(slips), orientation(0),
    xtal_cijkl_(c), rule(r)
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

void Plasticity::precompute(FEMesh* f) {

  mesh = f; // Presumed to be re-set if another mesh is run.
  
  // Do the orientation thing.
  if(orientation && orientation->constant_in_space()) {
    lab_cijkl_ = xtal_cijkl_.transform(orientation->orientation());
    // Also do the slip systems.

    lab_schmid_tensors.resize(nslips);
    for(unsigned int i=0; i<(unsigned)nslips; ++i)
      xtal_schmid_tensors[i]=_rotate_schmid_tensor(xtal_schmid_tensors[i],
						   orientation->orientation());
	  
  }
}

void Plasticity::begin_element(const CSubProblem *c, const Element *e) {

  ElementData *ed = e->getDataByName("plastic_data");
  ElementData *eds = e->getDataByName("slip_data");

  // # of slips is available in local data "nslips".
  // Integration order is a function, integration_order(c,e).

  PlasticData *pd;
  SlipData *sd;

  int ig_order = integration_order(c,e);
  
  if (ed==0) {
    pd = new PlasticData(ig_order,e);
    e->setDataByName(pd);  // Element extracts the name.
  }
  else {
    pd = dynamic_cast<PlasticData*>(ed);

    for (unsigned int ig=0;ig<pd->gptdata.size();++ig) {
      pd->gptdata[ig].ft = pd->gptdata[ig].f_tau;
      pd->gptdata[ig].fpt = pd->gptdata[ig].fp_tau;
    }
  }
    
  if (eds==0) {
    sd = new SlipData(ig_order,rule,e);
    e->setDataByName(sd);
  }
  else {
    sd = dynamic_cast<SlipData*>(eds);
  }

  // At this point, pd and sd are set to the relevant PlasticData and
  // SlipData objects, respectively, and we're ready to do some physics.

  // Prototype code does:
  // Constructs XYZ, which is reference location of all nodes.
  // Constructs xyz, which is current location of all nodes.
  // (I think we don't need these?  We have access through
  // the node iterators.
  //
  // Allocate space for 3x3 A matrix, 3x3 B and C matrices
  // 
  // For each gausspoint:
  //   Retrieve the local plastic data and slip data
  //   Compute F(tau) from current u field..
  //   Compute S_trial.
  //   Compute the A matrix from F(tau) and Fp(t)
  //   Compute the B and C matrix sets.
  //
  //   Set S(tau) = S_trial
  //   Iterate:
  //     Call the constitutive rule with S(tau) and the slip data,
  //        get back delta-gamma for each slip system, and
  //        derivatives of delta-gamma wrt 2nd PK stress..
  //     Do NR until S converges.
  //   Update Fp(tau) from the Asaro equation.
  //   Compute local elasto-plastic tangent, store it in the plastic data.
  //   
  //   (Update the plasticdata and slipdata objects?  Or not until final
  //      outer loop convergence?)

  SmallMatrix f_tau(3);
  
  int gptdx = 0;
  for (GaussPointIterator gpt = e->integrator(ig_order);
       !gpt.end(); ++gptdx,++gpt) {
    const GaussPoint agpt = gpt.gausspoint(); // Actual gausspoint.

    f_tau.clear();

    // CleverPtr for scope management.  The control sequence here
    // resembles Element::outputFieldDeriv, which we should maybe use
    // directly?  Not doing this because I think I need to own the
    // node loop, but this might not be true.
    for (CleverPtr<ElementFuncNodeIterator> efi(e->funcnode_iterator());
	 !(efi->end()); ++(*efi)) {
      OutputValue dval = displacement->newOutputValue();
      // Reference-state derivatives.
      double dshapedx = efi->dshapefunction(0,agpt);
      double dshapedy = efi->dshapefunction(1,agpt);
      double dshapedz = efi->dshapefunction(2,agpt);

      // Vector value of the displacement at the node.
      dval += displacement->output(mesh, *efi);

      for (IteratorP ip = displacement->iterator(ALL_INDICES);
	   !ip.end(); ++ip) {
	f_tau(ip.integer(),0) += dval[ip]*dshapedx;
	f_tau(ip.integer(),1) += dval[ip]*dshapedy;
	f_tau(ip.integer(),2) += dval[ip]*dshapedz;
	f_tau(ip.integer(), ip.integer()) += 1.0;
      }
    }
    // f_tau is now populated.
    
  }
}

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


// The magic 12 is the number of slip systems in FCC.
FCCPlasticity::FCCPlasticity(PyObject *reg, const std::string &nm,
			     const Cijkl &c, PlasticConstitutiveRule *r)
  : Plasticity(reg,nm,c,r, 12) {

  std::cerr << xtal_cijkl_ << std::endl;
  //
  // Populate the schmid_tensor data member.
  xtal_schmid_tensors.resize(nslips); // Base class knows nslips at this point.
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


//--------------------------------------------------------------------//


GptPlasticData::GptPlasticData() :
  ft(3),fpt(3),f_tau(3),fp_tau(3),fe_tau(3),cauchy(3),s_star(3),d_ep(3)
{
  ft(0,0) = ft(1,1) = ft(2,2) = 1.0;
  fpt(0,0) = fpt(1,1) = fpt(2,2) = 1.0;
  f_tau(0,0) = f_tau(1,1) = f_tau(2,2) = 1.0;
}

// The order selects which gpt array to iterate over.  It's passed in,
// but it's very important that this be done consistently.
PlasticData::PlasticData(int ord, const Element *el) :
  ElementData("plastic_data"), order(ord) {
  for (GaussPointIterator gpt = el->integrator(order);
       !gpt.end(); ++gpt) {
    GptPlasticData gppd = GptPlasticData();
    fp.push_back(gppd);
    gptdata.push_back(gppd);
  }
}


SlipData::SlipData(int ord, const PlasticConstitutiveRule *r,
		   const Element *e) : ElementData("slip_data"), order(ord)
{
  for (GaussPointIterator gpti = e->integrator(order);
       !gpti.end(); ++gpti) {
    GptSlipData *gpslip = r->getSlipData();
    gptslipdata.push_back(gpslip);
  }
}

// We own the pointed-to GptSlipData objects -- clean them up when we die.
SlipData::~SlipData() {
  for (std::vector<GptSlipData*>::iterator i = gptslipdata.begin();
       i!=gptslipdata.end(); ++i) {
    delete (*i);
  }
}
