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


// Utility function -- inverts a 3x3 SmallMatrix "manually".
// TODO: Make this a sub-class of SmallMatrix class, which should
// use dgetri function, to avoid the determinant?  Our determinants
// are near unity, so we are probably OK.
//
// Method cribbed from:
// http://www.mathcentre.ac.uk/resources/uploaded/sigma-matrices11-2009-1.pdf
SmallMatrix sm_invert3(SmallMatrix x) {
  if ((x.rows()!=3) || (x.cols()!=3)) {
      throw ErrProgrammingError("sm_invert3 called with non-3x3 SmallMatrix.",
				__FILE__,__LINE__);
    }
  else {
    SmallMatrix res(3);
    // Cofactors
    res(0,0) = x(1,1)*x(2,2)-x(1,2)*x(2,1);
    res(0,1) = -(x(1,0)*x(2,2)-x(1,2)*x(2,0));
    res(0,2) = x(1,0)*x(2,1)-x(1,1)*x(2,0);
    //
    res(1,0) = -(x(0,1)*x(2,2)-x(0,2)*x(2,1));
    res(1,1) = x(0,0)*x(2,2)-x(0,2)*x(2,0);
    res(1,2) = -(x(0,0)*x(2,1)-x(0,1)*x(2,0));
    //
    res(2,0) = x(0,1)*x(1,2)-x(0,2)*x(1,1);
    res(2,1) = -(x(0,0)*x(1,2)-x(1,2)*x(1,0));
    res(2,2) = x(0,0)*x(1,1)-x(0,1)*x(1,0);
    //
    double dtmt = x(0,0)*res(0,0)+x(0,1)*res(0,1)+x(0,2)*res(0,2);
    //
    // Inverse is adjoint divided by determinant.
    res.transpose();
    //
    return res*(1.0/dtmt);
  }
}


// Cayley-Hamilton trickery to compute the square root of a
// passed-in matrix.
// http://www.unthank.xyz/2017/03/04/
//    square-roots-of-a-matrix-from-cayley-hamilton-theorem/
SmallMatrix sm_sqrt3(SmallMatrix x) {
  if ((x.rows()!=3) || (x.cols()!=3)) {
      throw ErrProgrammingError("sm_sqrt3 called with non-3x3 SmallMatrix.",
				__FILE__,__LINE__);
    }
  else {
    SmallMatrix res(3);
    SmallMatrix ident(3);
    ident(0,0) = 1.0; ident(1,1) = 1.0; ident(2,2) = 2.0;
    
    double tol = 1.0e-16; // How to pick?  Machine precision?
    
    // Invariants.
    SmallMatrix c2 = x*x;
    double ic = x(0,0)+x(1,1)+x(2,2);
    double iic = 0.5*(ic*ic-(c2(0,0)+c2(1,1)+c2(2,2)));
    double iiic = x(0,0)*( x(1,1)*x(2,2)-x(1,2)*x(2,1))+
      x(0,1)*(-(x(1,0)*x(2,2)-x(1,2)*x(2,0)))+
      x(0,2)*(x(1,0)*x(2,1)-x(1,1)*x(2,0));
    double ik = ic*ic-3.0*iic;

    if (ik < tol) {
      double lmda = pow(ic/3.0, 0.5);
      return ident*lmda;
    }
    // else...
    double big_ev = ic*ic*(ic-4.5*iic)+13.5*iiic;
    double phi = acos(big_ev/pow(ik,1.5));
    double l2 = (1.0/3.0)*(ic+2.0*pow(ik,(1.0/3.0))*cos(phi/3.0));

    double iiiu = sqrt(iiic);
    double iu = sqrt(l2)+sqrt(-l2+ic+2*iiiu/sqrt(l2));
    double iiu = 0.5*(iu*iu-ic);

    res = (1.0/(iu*iiu-iiiu))*(ident*(iu*iiu)+x*(iu*iu-iiu)-c2);
    return res;
  }
}


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
  SmallMatrix a_mtx(3);
  SmallMatrix s_trial(3);

  // TODO: Some kind of smart container, for memory management?
  std::vector<SmallMatrix*> b_mtx(nslips),c_mtx(nslips);
  for (int i=0;i<nslips;++i) {
    b_mtx[i]=new SmallMatrix(3);
    c_mtx[i]=new SmallMatrix(3);
  }
  
  
  int gptdx = 0;
  for (GaussPointIterator gpt = e->integrator(ig_order);
       !gpt.end(); ++gptdx,++gpt) {
    const GaussPoint agpt = gpt.gausspoint(); // Actual gausspoint.

    SmallMatrix f_t = pd->gptdata[gptdx].ft;  // Save prior time-step's F.

    // Build the current time-step's version.
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
	int idx = ip.integer();
	f_tau(idx,0) += dval[ip]*dshapedx;
	f_tau(idx,1) += dval[ip]*dshapedy;
	f_tau(idx,2) += dval[ip]*dshapedz;
	f_tau(idx, idx) += 1.0;
      }
    }
    // f_tau is now populated for the current gausspoint.
    // Plastic fp is in pd->gptdata[gptdx].fpt
    SmallMatrix fp_t = pd->gptdata[gptdx].fpt;
    SmallMatrix fp_t_i = sm_invert3(fp_t);
    SmallMatrix f_tau_t = f_tau; f_tau_t.transpose();
    SmallMatrix fp_t_i_t = fp_t_i; fp_t_i_t.transpose();
    
    a_mtx = ((fp_t_i_t*f_tau_t)*f_tau)*fp_t_i;

    SmallMatrix elastic_estimate = a_mtx;
    for (int i=0;i<3;++i) { elastic_estimate(i,i) -= 1.0; }

    s_trial.clear();
    for (int i=0;i<3;++i)
      for (int j=0;j<3;++j)
	for (int k=0;k<3;++k)
	  for (int l=0;l<3;++l)
	    s_trial(i,j) += 0.5*lab_cijkl_(i,j,k,l)*elastic_estimate(k,l);
    
    // At this point we have the A matrix and trial stress for this gpt.
    // Slip systems are in lab_schmid_tensors, std::vector<SmallMatrix*>.

    // Populate b and c matrix vectors.
    for(int si=0;si<nslips;++si) {
      SmallMatrix mn = (*lab_schmid_tensors[si]);
      SmallMatrix mn_t = mn; mn_t.transpose();
      *(b_mtx[si]) = a_mtx*mn+mn_t*a_mtx;
      c_mtx[si]->clear();
      for(int i=0;i<3;++i)
	for(int j=0;j<3;++j)
	  for(int k=0;k<3;++k)
	    for(int l=0;l<3;++l)
	      (*(c_mtx[si]))(i,j) += 0.5*lab_cijkl_(i,j,k,l)*(*(b_mtx[si]))(k,l);
    }
    // A, B, and C matrix sets are built, and S_trial is populated.
    // Call the constitutive rule -- given the current S and
    // current plastic state at this gausspoint (encapsulated
    // in plasticdata and slipdata), it should return a new S,
    // a delta-gamma for each slip system, and a two-index object
    // containing the derivaggtive of the delta-gamma with respect
    // to the current stress.  Do NR iterations until this converges.

    // Once it's converged, make another call to update the
    // local plastic state in plasticdata and slipdata.

    // ********  MAGIC **********

    // Then compute the four-index W object at this gausspoint.


    // These are "stubs" for now.  The real ones come from
    // the NR loop through the constitutive rule.
    SmallMatrix s_tau(3);
    SmallMatrix fp_tau(3);
    
    // At this point, we have the value of s_tau, the 2nd PK stress
    // at the current time increment, as well as fp_tau, the plastic
    // strain at the current time, computed from the delta-gammas
    // and the Asaro equation.

    // Construct the increment matrix, f_nc.
    SmallMatrix f_t_i = sm_invert3(f_t);
    SmallMatrix f_nc(3);  // The increment matrix.
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int k=0;k<3;++k)
	  f_nc(i,j) += f_tau(i,k)*f_t_i(k,j);

    // Construct the polar decomposition of f_nc.
    // f_nc = r_nc.u_nc, where u_nc is the square root of f_nc_t.f_nc.
    
    // Construct derivative matrix s4 = dfE(tau)/dUt
    // Construct derivative matrix q4 = dS(tau)/dUt
    // Combine into four-index object w.
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
