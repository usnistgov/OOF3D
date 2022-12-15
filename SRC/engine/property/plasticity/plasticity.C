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
#include "engine/property/plasticity/plasticity_data.h"
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
#include "engine/smallmatrix3.h"
#include "engine/property/orientation/orientation.h"

// TODO: Should be settable in the solver somewhere.
#define TOLERANCE 0.00001
#define ITER_MAX 20
#define OLD_S_STAR_SIZE_LIMIT 0.001

// Conversion of 3x3 matrix to 6-vector, forward and reverse.

//#################  Reduce 2nd order 3*3 tensor to 1st 6 vector ########
SmallMatrix sm_6vec(SmallMatrix3 x) {

  SmallMatrix res(6,1);
  
  for(int i = 0 ; i < 3 ; i++)
    res(i,0) = x(i,i);
    
  res(3,0) = 0.5*(x(0,1)+x(1,0));
  res(4,0) = 0.5*(x(1,2)+x(2,1));
  res(5,0) = 0.5*(x(0,2)+x(2,0));
  
  return res;
  
}


//######### Inflate 1st 6 vector to 2nd 3*3 tensor ################
SmallMatrix3 sm_6tensor(SmallMatrix x) {

  SmallMatrix3 res;
  
  for(int i = 0 ; i < 3 ; i++)
    res(i,i) = x(i,0);
  
  res(0,1) = x(3,0);
  res(1,2) = x(4,0);
  res(0,2) = x(5,0);
  
  res(1,0) = x(3,0);
  res(2,1) = x(4,0);
  res(2,0) = x(5,0);
  
  return res;
    
}


Plasticity::Plasticity(PyObject *reg, const std::string &name,
		       const Cijkl &c, PlasticConstitutiveRule *r,
		       const int slips)
  : FluxProperty(name, reg), nslips(slips), orientation(0),
    xtal_cijkl_(c), rule(r)
{
  r->set_slip_systems(nslips);
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
      lab_schmid_tensors[i]=_rotate_schmid_tensor(xtal_schmid_tensors[i],
						  orientation->orientation());
	  
  }
}

void Plasticity::begin_element_matrix(const CSubProblem *c,
				      double time, const Element *e,
				      int debug_level) {

  for(int idx=0;idx<debug_level;++idx) std::cerr << "*";
  std::cerr << " Plasticity::begin_element_matrix starting." << std::endl;
  std::cerr << "Element is " << e->get_index() << "." << std::endl;
  std::cerr << "Time is " << time << std::endl;
  // LINSYS STEP 3, plastic version -- called from
  // Material::begin_element_matrix, we are in element scope, and need to run
  // our own gausspoint loop.  This class (or its subclasses) are
  // responsible for managing the per-gausspoint data objects.

  ElementData *ed = e->getDataByName("plastic_data");
  ElementData *eds = e->getDataByName("slip_data");

  // std::cerr << "Got the ElementData objects." << std::endl;
  
  // # of slips is available in local data "nslips".
  // Integration order is a function, integration_order(c,e).

  PlasticData *pd;
  SlipData *sd;

  // TODO: For time-stepping, the PlasticData object should have
  // time-step-specific info, and here, we should notice if we
  // are being asked to evaluate at a new time, and if so,
  // create a new time data in the PlasticData object, and
  // do the increment.  If not, re-do the old increment.

  // Q: Is this right?  The prior algorithm computes new iterations
  // from the result of the last iteration; the new scheme would
  // do it from the prior time-step.  This is probably more work,
  // and maybe wrong.
  int ig_order = integration_order(c,e);
  
  if (ed==0) {
    pd = new PlasticData(ig_order,e);
    e->setDataByName(pd);  // Element extracts the name.
  }
  else {
    pd = dynamic_cast<PlasticData*>(ed);
    int gptdx = 0;
    pd->set_time(time); // Sets dt internally.
    for (GaussPointIterator gpt = e->integrator(ig_order);
	 !gpt.end(); ++gptdx,++gpt) {
      // Transfer the previous "new" data to be the current "old" data.
      // TODO: Second layer is pointers?  Seems weird.
      pd->gptdata[gptdx]->ft = pd->gptdata[gptdx]->f_tau;
      pd->gptdata[gptdx]->fpt = pd->gptdata[gptdx]->fp_tau;
      // std::cerr << "Updated gptdata." << std::endl;
      // std::cerr << *(pd->gptdata[gptdx]) << std::endl;
    }
  }
  
  // HACK for testing the plasticity rule.
  // pd->set_time(0.0001);
  // end of HACK.
  
  // This is used in the calls to the constitutive evolve() method.
  double delta_t = pd->dt;
  // HACK: Diagnosing convergence issues, override dt.
  // double delta_t = 1.0;
  // end of HACK.
  std::cerr << "Retrieved delta_t, it's " << delta_t << std::endl;
  std::cerr << "Initialized the pd object." << std::endl;
  
  if (eds==0) {
    sd = new SlipData(ig_order,rule,e);
    e->setDataByName(sd);
  }
  else {
    sd = dynamic_cast<SlipData*>(eds);
  }

  std::cerr << "Initialized the sd object." << std::endl;
  
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

  
  
  SmallMatrix3 f_attau;
  SmallMatrix3 a_mtx;
  SmallMatrix3 s_trial;

  // TODO: Some kind of smart container, for memory management?

  // Gtmtx is a utility matrix used to convert delta-gamma dervatives
  // wrt to resolved shear stress to delta-gamma derivatives wrt 2nd
  // PK stress.  TODO: These arrays should be arrays of SmallMatrix3
  // objects, and those objects should have a default constructor.
  std::vector<SmallMatrix3*> b_mtx(nslips),c_mtx(nslips),gtmtx(nslips);
  for (int i=0;i<nslips;++i) {
    b_mtx[i]=new SmallMatrix3();
    c_mtx[i]=new SmallMatrix3();
    gtmtx[i]=new SmallMatrix3();
  }
  
  
  int gptdx = 0;
  for (GaussPointIterator gpt = e->integrator(ig_order);
       !gpt.end(); ++gptdx,++gpt) {
    
    std::cerr << "Start of the gausspoint loop." << std::endl;

    const GaussPoint agpt = gpt.gausspoint(); // Actual gausspoint.

    // HACK: Overwrite prior time-step F matrix.
    // pd->gptdata[gptdx]->ft.clear();
    // pd->gptdata[gptdx]->ft(0,0) = 1.0036;
    // pd->gptdata[gptdx]->ft(1,1) = 0.9985547565;
    // pd->gptdata[gptdx]->ft(2,2) = 0.9985547565;
    // End of HACK.

    std::cerr << "Input to the constitutive process:  Ft:" << std::endl;
    std::cerr << (pd->gptdata[gptdx]->ft) << std::endl;
    
    SmallMatrix3 f_att = pd->gptdata[gptdx]->ft;  // Save prior time-step's F.

    // Build the current time-step's version.
    f_attau.clear();

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
	// std::cerr << "Displacement component " << ip << " is " << dval[ip] << std::endl;
	f_attau(idx,0) += dval[ip]*dshapedx;
	f_attau(idx,1) += dval[ip]*dshapedy;
	f_attau(idx,2) += dval[ip]*dshapedz;
      }
    }
    // Diagonal part, outside the node loop.
    f_attau(0,0) += 1.0; f_attau(1,1) += 1.0; f_attau(2,2) += 1.0;

    // HACK: Overwrite f_attau with known values, for debugging.
    // f_attau.clear();
    // f_attau(0,0)=1.0037;
    // f_attau(1,1)=0.998513888;
    // f_attau(2,2)=0.998513888;
    // End of HACK.
    
    std::cerr << "Built the initial F matrix at time tau:" << std::endl;
    std::cerr << f_attau << std::endl;
    
    // f_attau is now populated for the current gausspoint.

    // Store it in the plastic-data object.
    // TODO: Do we need this?
    pd->gptdata[gptdx]->f_tau = f_attau;

    // HACK: Overwrite plastic data values.
    // pd->gptdata[gptdx]->fpt.clear();
    // pd->gptdata[gptdx]->fpt(0,0)=1.0000197;
    // pd->gptdata[gptdx]->fpt(1,1)=0.999990128;
    // pd->gptdata[gptdx]->fpt(2,2)=0.999990128;
    // End of HACK.

    
    // Plastic fp is in pd->gptdata[gptdx]->fpt
    SmallMatrix3 fp_att = pd->gptdata[gptdx]->fpt;
    SmallMatrix3 fp_att_i = fp_att.invert();
    SmallMatrix3 f_attau_t = f_attau; f_attau_t.transpose();
    SmallMatrix3 fp_att_i_t = fp_att_i; fp_att_i_t.transpose();

    std::cerr << "Other input: Fp at t:" << std::endl;
    std::cerr << fp_att << std::endl;
    
    // Handy place to construct the elastic deformation at prior time t.
    SmallMatrix3 fe_att = f_att*fp_att_i;
    SmallMatrix3 fe_att_t = fe_att; fe_att_t.transpose();

    std::cerr << "Elastic deformation at t:" << std::endl;
    std::cerr << fe_att << std::endl;
    
    a_mtx = ((fp_att_i_t*f_attau_t)*f_attau)*fp_att_i;

    SmallMatrix3 elastic_estimate = a_mtx;
    for (int i=0;i<3;++i) { elastic_estimate(i,i) -= 1.0; }

    s_trial.clear();
    for (int i=0;i<3;++i)
      for (int j=0;j<3;++j)
	for (int k=0;k<3;++k)
	  for (int l=0;l<3;++l)
	    s_trial(i,j) += 0.5*lab_cijkl_(i,j,k,l)*elastic_estimate(k,l);

    std::cerr << std::endl << "S_trial:" << std::endl;
    std::cerr << s_trial << std::endl;


    for(int idx=0;idx<debug_level;++idx) std::cerr << "*";
    std::cerr << " A matrix and trial stress." << std::endl;
    std::cerr << "Have A matrix and trial stress." << std::endl;
    // At this point we have the A matrix and trial stress for this gpt.
    // Slip systems are in lab_schmid_tensors, std::vector<SmallMatrix*>.

    // Populate b and c matrix vectors.
    std::cerr << "Constructing B and C. mn outupt inline." << std::endl;
    for(int si=0;si<nslips;++si) {
      SmallMatrix3 mn = (*lab_schmid_tensors[si]);
      // std::cerr << mn << std::endl;
      SmallMatrix3 mn_t = mn; mn_t.transpose();
      // std::cerr << mn_t << std::endl;
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
    // containing the derivative of the delta-gamma with respect
    // to the current stress.  Do NR iterations until this converges.

    // Once it's converged, make another call ("complete") to update
    // the local plastic state in slipdata. We are in charge of
    // plasticata.

    // -------------------------
    // Constitutive part is here
    // -------------------------
    // This is the "TASK 1" of the constititive rule file.
    // Possibly the GptPlasticData container is not needed?

    // Compute the resolved shear stresses for the trial stress, and
    // put them in the slipdata container for this gausspoint.
    for(int alpha=0;alpha<nslips;++alpha) {
      sd->gptslipdata[gptdx]->tau_alpha[alpha] = \
	dot(s_trial, *lab_schmid_tensors[alpha]);
      // std::cerr << "Lab schmid tensor: " << std::endl;
      // std::cerr << *lab_schmid_tensors[alpha] << std::endl;
      std::cerr << "Tau_alpha: " << std::endl;
      std::cerr << sd->gptslipdata[gptdx]->tau_alpha[alpha] << std::endl;
    }

    std::cerr << "Initial call to constitutive rule's evolve." << std::endl;
    // Initial call to evolve -- this populates the delta_gamma and
    // dgamma_dtau from s_trial..
    std::cerr << "Calling evolve, delta_t is " << delta_t << std::endl;
    rule->evolve(pd->gptdata[gptdx],sd->gptslipdata[gptdx],delta_t);

    std::cerr << "Back from evolve." << std::endl;
    
    // Compute the first correction to the s_trial in s_star.
    pd->gptdata[gptdx]->s_star = s_trial;
    for(int alpha=0;alpha<nslips;++alpha) {
      pd->gptdata[gptdx]->s_star -= (*c_mtx[alpha])*sd->gptslipdata[gptdx]->delta_gamma[alpha];
    }
    std::cerr << "First correction computed." << std::endl;
    std::cerr << pd->gptdata[gptdx]->s_star << std::endl;
    
    bool done = false;        // Set when converged or iter limit exceeded.
    unsigned int icount = 0;  // Count interations.
    while(!done) {
      for(int idx=0;idx<debug_level;++idx) std::cerr << "*";
      std::cerr << " Top of plastic convergence loop." << std::endl;
      // Compute the new resolved shear stresses from s_star.
      for(int alpha=0;alpha<nslips;++alpha) {
	sd->gptslipdata[gptdx]->tau_alpha[alpha] =	\
	  dot(pd->gptdata[gptdx]->s_star, *lab_schmid_tensors[alpha]);
	std::cerr << "Resolved shear stress and resistance:" << std::endl;
	std::cerr << sd->gptslipdata[gptdx]->tau_alpha[alpha] << std::endl;
      }

      // Call evolve, get back new delta_gamma and dgamma_dtau values.
      std::cerr << "Calling evolve in the convergence loop." << std::endl;
      std::cerr << "Iteration count is " << icount << std::endl;
      rule->evolve(pd->gptdata[gptdx],sd->gptslipdata[gptdx],delta_t);

      std::cerr << "Back from constitutive evolve method." << std::endl;
      for(int alphadx = 0; alphadx<nslips; ++alphadx) {
	std::cerr << "Delta-gamma " << alphadx << ": " << sd->gptslipdata[gptdx]->delta_gamma[alphadx] << std::endl;
	std::cerr << "Dgamma-dtau " << alphadx << ": " << sd->gptslipdata[gptdx]->dgamma_dtau[alphadx] << std::endl;
      }
      
      // TODO optimize:  Precompute gtmtx.  This transpose business is awful.
      for(int alpha=0;alpha<nslips;++alpha) {
	SmallMatrix3 lst = *lab_schmid_tensors[alpha];
	SmallMatrix3 lst_t = *lab_schmid_tensors[alpha];
	lst_t.transpose();
	// std::cerr << "Schmid tensor and transpose:" << std::endl;
	// std::cerr << lst << std::endl;
        // std::cerr << lst_t << std::endl;
	*(gtmtx[alpha]) = (lst+lst_t)*(0.5*sd->gptslipdata[gptdx]->dgamma_dtau[alpha]);
      } 

      // std::cerr << "Gtmtx:" << std::endl;
      // for(int alphadx=0;alphadx<nslips;++alphadx) {
      //   std::cerr << "Alpha: " << alphadx << std::endl;
      //   std::cerr << *(gtmtx[alphadx]) << std::endl;
      // }

      // std::cerr << "Cmtx:" << std::endl;
      // for(int alphadx=0;alphadx<nslips;++alphadx) {
      //   std::cerr << *(c_mtx[alphadx]) << std::endl;
      // }

      std::cerr << "Finished with the S loop." << std::endl;

      
      // Compute the fourth order tensor...
      Rank4_3DTensor RJ_mtx;
      for(int i=0;i<3;++i)
	for(int j=0;j<3;++j)
	  for(int k=0;k<3;++k)
	    for(int l=0;l<3;++l) {
	      for(int alpha=0;alpha<nslips;++alpha) {
		RJ_mtx(i,j,k,l) += (*c_mtx[alpha])(i,j)*(*gtmtx[alpha])(k,l);
	      }
	      if ( (i==k)&&(j==l) )
		RJ_mtx(i,j,k,l) += 0.5;
	      if ( (i==l)&&(j==k) )
		RJ_mtx(i,j,k,l) += 0.5;
	    }

      // std::cerr << "Built the RJ_mtx object." << std::endl;
      // std::cerr << RJ_mtx << std::endl;
      
      SmallMatrix3 rhs = pd->gptdata[gptdx]->s_star;
      rhs -= s_trial;
      for(int alpha=0;alpha<nslips;++alpha) {
	rhs += (*c_mtx[alpha])*(sd->gptslipdata[gptdx]->delta_gamma[alpha]);
      }

      std::cerr << "Built the rhs object." << std::endl;
      std::cerr << rhs << std::endl;
      
      // NR step involves converting the 4-index and 2-index
      // quantities to a linear system and solving it.
      SmallMatrix nr_kernel = RJ_mtx.as_6matrix();
      SmallMatrix nr_rhs = sm_6vec(rhs);
      
      std::cerr << "Matrix: " << std::endl;
      std::cerr << nr_kernel << std::endl;
      
      std::cerr << "Calling nr_kernel.solve." << std::endl;
      int res = nr_kernel.solve(nr_rhs);
      std::cerr << "Back from nr_kernel.solve." << std::endl;
      // TODO: Check the return code.
      std::cerr << "Linear algebra return code: " << res << std::endl;

      std::cerr << "Linear algebra answer:" << std::endl;
      std::cerr << nr_rhs << std::endl;
      
      SmallMatrix3 delta_s_star = sm_6tensor(nr_rhs);
      
      std::cerr << "Delta s_star:" << std::endl;
      std::cerr << delta_s_star << std::endl;
      
      SmallMatrix3 old_s_star = pd->gptdata[gptdx]->s_star;
      double old_s_star_size = sqrt(dot(old_s_star,old_s_star));

      SmallMatrix3 new_s_star = old_s_star - delta_s_star;
      double new_s_star_size = sqrt(dot(new_s_star,new_s_star));

      std::cerr << "New s_star at the bottom of the while loop:" << std::endl;
      std::cerr << new_s_star << std::endl;
      
      pd->gptdata[gptdx]->s_star = new_s_star;

      std::cerr << "Fractional tolerance check:" << std::endl;
      std::cerr << ((new_s_star_size - old_s_star_size)/old_s_star_size) << std::endl;
      if (old_s_star_size < OLD_S_STAR_SIZE_LIMIT)
	done = true;
      else 
	if ( fabs((new_s_star_size - old_s_star_size)/old_s_star_size) < TOLERANCE)
	  done = true;
      
      icount+=1;
      if (icount>ITER_MAX)
	done = true;
    } // Constitutive while loop ends here.

    for(int idx=0;idx<debug_level;++idx) std::cerr << "*";
    std::cerr << " Out of the constitutive while loop." << std::endl;
    std::cerr << "S-star: " << pd->gptdata[gptdx]->s_star << std::endl;
    
    // Compute the last set of resolved shear stresses from the last s_star.
    for(int alpha=0;alpha<nslips;++alpha) {
      sd->gptslipdata[gptdx]->tau_alpha[alpha] =			\
	dot(pd->gptdata[gptdx]->s_star, *lab_schmid_tensors[alpha]);
    }

    std::cerr << "Final call to evolve before completion." << std::endl;
    rule->evolve(pd->gptdata[gptdx],sd->gptslipdata[gptdx],delta_t);

    std::cerr << "Calling rule->complete." << std::endl;

    // It's OK to do this update inside the outermost NR loop
    // controlled by the stepper, the constitutive rule will back off
    // on the plastic contributions where appropriate within the loop.
    // Keeping the increments promotes faster convergence, which is
    // good for a process that's already slow.
    rule->complete(pd->gptdata[gptdx],sd->gptslipdata[gptdx]);

    std::cerr << "Back from rule->complete." << std::endl;
    std::cerr << "s_attau is: " << std::endl;
    std::cerr << pd->gptdata[gptdx]->s_star << std::endl;
    
    // Select data objects for the subsequent processing.
    SmallMatrix3 s_attau = pd->gptdata[gptdx]->s_star;
    std::vector<double> delta_g = sd->gptslipdata[gptdx]->delta_gamma;
    std::vector<SmallMatrix3*> dgamma_ds(nslips);

    std::cerr << "Retrieved data objects." << std::endl;
    
    // TODO optimize: Precompute the symmetrized Schmid tensor, this
    // transpose operation is very stupid.
    for (int i=0; i<nslips; ++i) {
      SmallMatrix3 lst = *lab_schmid_tensors[i];
      SmallMatrix3 lst_t = *lab_schmid_tensors[i];
      lst_t.transpose();
      // std::cerr << "Incorporating constitutive data:" << std::endl; 
      // std::cerr << lst << std::endl;
      // std::cerr << lst_t << std::endl;
      // std::cerr << sd->gptslipdata[gptdx]->dgamma_dtau[i] << std::endl;
      SmallMatrix3 dgds = (lst+lst_t)*(0.5*(sd->gptslipdata[gptdx]->dgamma_dtau[i]));
      // TODO: De-allocate this somewhere?  Use a smart pointer?
      dgamma_ds[i] = new SmallMatrix3(dgds);
    }

    std::cerr << "Dgamma_Ds[0]:" << std::endl;
    std::cerr << *(dgamma_ds[0]) << std::endl;
    
    std::cerr << "Finished stupid transpose." << std::endl;

    // This is where the constitutive rule's delta-gamma gets
    // incorporated into the accumulated plastic strain.
    SmallMatrix3 lp;
    for(int alpha=0;alpha<nslips;++alpha) {
      lp += (sd->gptslipdata[gptdx]->delta_gamma[alpha])*(*lab_schmid_tensors[alpha]);
    }

    // TODO: Ugh.  Not in the gausspoint loop, please.
    SmallMatrix3 ident;
    ident(0,0)=1.0; ident(1,1)=1.0; ident(2,2)=1.0;

    // The new fp is the old fp plus the Asaro equation result.
    // This is fp_attau;
    pd->gptdata[gptdx]->fp_tau = (pd->gptdata[gptdx]->fpt)*(ident + lp);

    std::cerr << "Incremented fp_tau." << std::endl;
    std::cerr << *(pd->gptdata[gptdx]) << std::endl;
    
    // Grab a reference to this for post-processing.
    SmallMatrix3 &fp_attau = pd->gptdata[gptdx]->fp_tau;

    // Normalize fp_tau.  
    double dtmt = fp_attau.determinant();
    fp_attau *= (1.0/pow(dtmt, 1.0/3.0));
    
    // Decompose into elastic and plastic parts.
    SmallMatrix3 fp_attau_i = fp_attau.invert();
    SmallMatrix3 fe_attau = fp_attau_i*f_attau;
    SmallMatrix3 fe_attau_i = fe_attau.invert();

    // Put it in the plastic data container.
    pd->gptdata[gptdx]->fe_tau = fe_attau;

    // std::cerr << "Got s_tau, which is the 2nd PK stress." << std::endl;
    // At this point, we have the value of s_tau, the 2nd PK stress
    // at the current time increment, as well as fp_tau, the plastic
    // strain at the current time, computed from the delta-gammas
    // and the Asaro equation.

    std::cerr << "Fe_attau: " << std::endl;
    std::cerr << fe_attau << std::endl;
    
    SmallMatrix3 fe_attau_t = fe_attau;
    fe_attau_t.transpose();

    // Compute the Cauchy stress at tau.
    std::cerr << "Cauchy stress assignment: " << std::endl;
    std::cerr <<  fe_attau*(pd->gptdata[gptdx]->s_star)*fe_attau_t << std::endl;
    
    pd->gptdata[gptdx]->cauchy = fe_attau*(pd->gptdata[gptdx]->s_star)*fe_attau_t;
    std::cerr << pd->gptdata[gptdx]->cauchy << std::endl;
    
    double fe_dtmt = fe_attau.determinant();
    pd->gptdata[gptdx]->cauchy *= (1.0/fe_dtmt);

    // Cauchy stress is now up to date.
    
    for(int idx=0;idx<debug_level;++idx) std::cerr << "*";
    std::cerr << " Cauchy stress." << std::endl;
    std::cerr << "Constitutive output: Cauchy stress: " << std::endl;
    std::cerr << pd->gptdata[gptdx]->cauchy << std::endl;

        
    for(int idx=0;idx<debug_level;++idx) std::cerr << "*";
    std::cerr << " Post-cauchy post-processing." << std::endl;
    
    // Construct the increment matrix, f_nc, and it's transpose.
    SmallMatrix3 f_att_i = f_att.invert();
    SmallMatrix3 f_inc(3);   // The increment matrix.
    SmallMatrix3 f_inc_t(3); // Its transpose.
    std::cerr << "Inputs to f_inc, f_att_i and f_attau." << std::endl;
    std::cerr << f_att_i << std::endl;
    std::cerr << f_attau << std::endl;
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j) {
	for(int k=0;k<3;++k) 
	  f_inc(i,j) += f_attau(i,k)*f_att_i(k,j);
	f_inc_t(j,i) = f_inc(i,j);
      }

    std::cerr << "Increment matrix:" << std::endl;
    std::cerr << f_inc << std::endl;
    std::cerr << f_inc_t << std::endl;
    
    std::cerr << "About to do polar decomposition." << std::endl;
    // Construct the polar decomposition of f_inc.
    // f_inc = r_inc.u_inc, where u_inc is the square root of f_inc_t.f_inc.
    SmallMatrix3 f2 = f_inc_t * f_inc;
    std::pair<SmallMatrix3,SmallMatrix3> uui = f2.ch_sqrt();
    SmallMatrix u = uui.first;
    SmallMatrix r = f_inc * uui.second;  // f-increment * u-inverse

    std::cerr << "Polar decomposition u: " << std::endl;
    std::cerr << u << std::endl;

    std::cerr << "Polar decomposition r: " << std::endl;
    std::cerr << r << std::endl;
    
    // ----------------------------------------------------
    //           Build the Q matrix, bsb_q.
    // ----------------------------------------------------

    std::cerr << "Fe_att:" << std::endl;
    std::cerr << fe_att << std::endl;
    
    // std::cerr << "Building bsb_l." << std::endl;
    // Now we have fe_att_t, fe_att, and u.  Build Balasubramian's L.
    // for(int dbi = 0; dbi<3; ++dbi)
    //   for(int dbj = 0; dbj<3; ++dbj)
    //     std::cerr << dbi << " , " << dbj << " = " << u(dbi,dbj) << std::endl;
    Rank4_3DTensor bsb_l;
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int n=0;n<3;++n)
	  for(int o=0;o<3;++o)
	    for(int idx=0;idx<3;++idx) {
	      bsb_l(i,j,n,o) += fe_att_t(i,n)*u(o,idx)*fe_att(idx,j);
	      bsb_l(i,j,n,o) += fe_att_t(i,idx)*u(idx,n)*fe_att(o,j);
	    };

    // std::cerr << "BSB L" << std::endl;
    // std::cerr << bsb_l  << std::endl;

    // For debugging, paranoia about Cijkl.
    Rank4_3DTensor check_c;
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int k=0;k<3;++k)
	  for(int l=0;l<3;++l)
	    check_c(i,j,k,l) = lab_cijkl_(i,j,k,l);
    // std::cerr << "Lab Cijkl via the tensors:" << std::endl;
    // std::cerr << check_c.as_smallmatrix() << std::endl;
    
    // std::cerr << "Lab Cijkl: " << std::endl;
    // std::cerr << lab_cijkl_ << std::endl;

    // std::cerr << "Building bsb_d." << std::endl;
    Rank4_3DTensor bsb_d;
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int n=0;n<3;++n)
	  for(int o=0;o<3;++o)
	    for(int k=0;k<3;++k)
	      for(int l=0;l<3;++l) {
		bsb_d(i,j,n,o) += 0.5*lab_cijkl_(i,j,k,l)*bsb_l(k,l,n,o);
	      }


    // std::cerr << "1100: " << bsb_d(1,1,0,0) << std::endl;
    // std::cerr << "0011: " << bsb_d(0,0,1,1) << std::endl;
    
    // std::cerr << "BSB D" << std::endl;
    // std::cerr << bsb_d.as_smallmatrix() << std::endl;
    
    // std::cerr << "Building bsb_g." << std::endl;
    std::vector<Rank4_3DTensor> bsb_g(nslips);
    for(int alpha=0;alpha<nslips;++alpha)
      for(int k=0;k<3;++k)
	for(int l=0;l<3;++l)
	  for(int m=0;m<3;++m)
	    for(int n=0;n<3;++n)
	      for(int o=0;o<3;++o) {
		bsb_g[alpha](k,l,n,o) += \
		  bsb_l(k,m,n,o)*(*(lab_schmid_tensors[alpha]))(m,l) \
		  + (*(lab_schmid_tensors[alpha]))(m,k)*bsb_l(m,l,n,o);
	      };

    // std::cerr << "BSB_G:" << std::endl;
    // std::cerr << bsb_g[0].as_smallmatrix() << std::endl;

    std::vector<Rank4_3DTensor> bsb_t(nslips);
    for(int alpha=0;alpha<nslips;++alpha)
      for(int i=0;i<3;++i)
	for(int j=0;j<3;++j)
	  for(int k=0;k<3;++k)
	    for(int l=0;l<3;++l)
	      for(int n=0;n<3;++n)
		for(int o=0;o<3;++o) {
		  bsb_t[alpha](i,j,n,o) += \
		    0.5*lab_cijkl_(i,j,k,l)*bsb_g[alpha](k,l,n,o);
		}

    // std::cerr << "BSB_T:" << std::endl;
    // std::cerr << bsb_t[0].as_smallmatrix() << std::endl;
    
    // Member objects:  lab_schmid_tensors, nslips.
    // Slip increments std::vector<double> delta_g
    // Local objects -- c_mtx is std::vector<SmallMatrix*>, by slips.
    // Slip dervatives std::vector<SmallMatrix*> dgamma_ds
    
    // TODO OPT: This uses 9x9 matrices, but can probably get away
    // with 6x6 and the magic inner product.  Also, the Rank4_3DTensor
    // class should probably have arithmetic operations that operate
    // on the linear array, for better performance, although the
    // compiler might unroll the loops.
    Rank4_3DTensor lhs;
    Rank4_3DTensor rhs = bsb_d;

    std::cerr << "Building rhs." << std::endl;
    for(int alpha=0;alpha<nslips;++alpha)
      for(int i=0;i<3;++i)
	for(int j=0;j<3;++j)
	  for(int k=0;k<3;++k)
	    for(int l=0;l<3;++l) {
	      rhs(i,j,k,l) -= delta_g[alpha]*bsb_t[alpha](i,j,k,l);
	    }

    std::cerr << "Building lhs." << std::endl;
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int m=0;m<3;++m)
	  for(int n=0;n<3;++n) {
	    // TODO: Maybe clearer to have a 4-way Kronecker delta?
	    if ((i==m) && (j==n)) 
	      lhs(i,j,m,n)=1.0;
	    
	    for(int alpha=0;alpha<nslips;++alpha) { 
	      lhs(i,j,m,n) += (*dgamma_ds[alpha])(m,n)*(*c_mtx[alpha])(i,j);
	    }
	  }

    std::cerr << "Doing the linear algebra." << std::endl;
    // The actual equation for bsb_q is
    //      lhs(i,j,m,n)*bsb_q(m,n,k,l) = rhs(i,j,k,l).
    // Do this by linear algebra with the SmallMatrix class.
    SmallMatrix lhs_sm = lhs.as_smallmatrix();
    SmallMatrix rhs_sm = rhs.as_smallmatrix();

    std::cerr << "Linear algebra components:" << std::endl;
    std::cerr << "LHS:" << std::endl;
    std::cerr << lhs_sm << std::endl;
    std::cerr << "RHS:" << std::endl;
    std::cerr << rhs_sm << std::endl;
    
    std::cerr << "Calling the Q matrix solver." << std::endl;
    int retcode = lhs_sm.solve(rhs_sm);
    std::cerr << "Back from the solver." << std::endl;
    if (retcode != 0) {
      throw ErrProgrammingError("Plasticity Q matrix computation failed",
				__FILE__,__LINE__);
    };

    std::cerr << "Assigning to bsb_q." << std::endl;
    
    // "Solve" puts the solution in the RHS matrix.
    Rank4_3DTensor bsb_q(rhs_sm);

    std::cerr << "BSB Q" << std::endl;
    std::cerr << bsb_q.as_smallmatrix() << std::endl;
    
    std::cerr << "Building the S matrix." << std::endl;
    // ----------------------------------------
    //  Now build the S matrix..
    // ----------------------------------------
    // Ingredients include the "r" matrix, fe_att,
    // std::vector<SmallMatrix*> dgamma_ds, nslips,
    Rank4_3DTensor bsb_s;
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int m=0;m<3;++m)
	  for(int n=0;n<3;++n)
	    for(int o=0;o<3;++o) {
	      double v1 = r(i,n)*fe_att(o,m);
	      if (m==j) bsb_s(i,j,n,o) += v1;
	      double v2=0.0;
	      for(int alpha=0;alpha<nslips;++alpha) {
		v2 -= delta_g[alpha]*(*lab_schmid_tensors[alpha])(m,j);
	      }
	      bsb_s(i,j,n,o) += v1*v2;
	    }

    // If some of these loops are independent, they should probably be
    // done separately, e.g. the p and q loops?
    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int k=0;k<3;++k)
	  for(int l=0;l<3;++l)
	    for(int m=0;m<3;++m)
	      for(int n=0;n<3;++n)
		for(int o=0;o<3;++o)
		  for(int p=0;p<3;++p)
		    for(int q=0;q<3;++q)
		      for(int alpha=0;alpha<nslips;++alpha) {
			bsb_s(i,j,n,o) -=		\
			  r(i,k)*u(k,l)*fe_att(l,m)*    \
			  (*dgamma_ds[alpha])(p,q)*	\
			  bsb_q(p,q,n,o)* \
			  (*lab_schmid_tensors[alpha])(m,j);
		      }

    // std::cerr << "BSB S" << std::endl;
    // std::cerr << bsb_s.as_smallmatrix() << std::endl;

    
    Rank4_3DTensor w_mat;

    double fe_attau_d = fe_attau.determinant();

    
    std::cerr << "Fe_attau" << std::endl;
    std::cerr << fe_attau << std::endl;

    std::cerr << "2nd PK stress: " << std::endl;
    std::cerr << s_attau << std::endl;
    
    SmallMatrix ess_fei(3);
    for (int k=0;k<3;++k)
      for (int l=0;l<3;++l)
	for(int p=0;p<3;++p)
	  for(int q=0;q<3;++q) {
	    ess_fei(k,l) += bsb_s(p,q,k,l)*fe_attau_i(q,p);
	  }

    for(int i=0;i<3;++i)
      for(int j=0;j<3;++j)
	for(int k=0;k<3;++k)
	  for(int l=0;l<3;++l)
	    for(int m=0;m<3;++m)
	      for(int n=0;n<3;++n) {
		double wval = bsb_s(i,m,k,l)*s_attau(m,n)*fe_attau(j,n) \
		  + fe_attau(i,m)*bsb_q(m,n,k,l)*fe_attau(j,n) \
		  + fe_attau(i,m)*s_attau(m,n)*bsb_s(j,n,k,l) \
		  - fe_attau(i,m)*s_attau(m,n)*fe_attau(j,n)*ess_fei(k,l);
		w_mat(i,j,k,l) += wval/fe_attau_d;
	      }


    // Is it sufficiently symmetric for a Cijkl object?  SK says yes.

    std::cerr << "Writing w_mat." << std::endl;
    std::cerr << w_mat << std::endl;
    std::cerr << w_mat.as_smallmatrix() << std::endl;
    pd->gptdata[gptdx]->w_mat = w_mat;
    std::cerr << "Bottom of the gausspoint loop." << std::endl;
  } // End of the gausspoint loop (!).

  std::cerr << "Exiting begin_element_matrix for element " << e->get_index() << "." << std::endl;
  // At this point, every gausspoint has a populated gptdata object
  // with the current W matrix, which is the dervative of the Cauchy
  // stress with respect to the strain.  This object is used to
  // construct the flux matrix, which wants derivatives of the
  // Cauchy stress wrt the actual DOFs.
} // End of begin_element_matrix.

int Plasticity::integration_order(const CSubProblem *sp,
				  const Element *el) const {
  return el->shapefun_degree();
}

// Utility function, takes a normal and a slip direction, normalizes
// them, and computes their outer product -- this is how one makes
// Schmid tensors.  TODO: Might be handier if it could take
// initializers as arguments, which I think is a C++11 thing.
SmallMatrix3 *Plasticity::_normalized_outer_product(double *slip,
						    double *norm) {
  double nmag = sqrt(norm[0]*norm[0]+norm[1]*norm[1]+norm[2]*norm[2]);
  double smag = sqrt(slip[0]*slip[0]+slip[1]*slip[1]+slip[2]*slip[2]);
  double norm_norm[3] = {norm[0]/nmag, norm[1]/nmag, norm[2]/nmag};
  double norm_slip[3] = {slip[0]/smag, slip[1]/smag, slip[2]/smag};
  
  SmallMatrix3 *res = new SmallMatrix3();
  for(unsigned int i=0;i<3;++i)
    for(unsigned int j=0;j<3;++j)
      (*res)(i,j) = norm_slip[i]*norm_norm[j];
  return res;
}

SmallMatrix3 *Plasticity::_rotate_schmid_tensor(SmallMatrix3 *m,
						const COrientation *o) {
  // TODO: Probably this should be a SmallMatrix3 also, eventually.
  SmallMatrix rtmtx = o->rotation();
  SmallMatrix3 *res = new SmallMatrix3();
  
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
// an intrinsically quasistatic property.  Maybe we actually
// want flux_offset?  It's not NR, so maybe not.
void Plasticity::static_flux_value(const FEMesh *mesh,
				   const Element *element,
				   const Flux *flux,
				   const MasterPosition &mpt,
				   double time, SmallSystem *fluxdata)
  const
{
  // Cauchy stress is available at gausspoints, but we are given a
  // master-coord.  For now: Look it up in the custom map.  TODO
  // later: Override Property::make_flux_contributions to do this
  // differently?
  // This is used to construct the residual in the NR loop.
  PlasticData *pd = dynamic_cast<PlasticData*>
    (element->getDataByName("plastic_data"));
  int gptidx = (pd->mctogpi_map)[mpt.mastercoord()];
  const SymmMatrix3 &cchy = (pd->gptdata[gptidx])->cauchy;
  for(SymTensorIterator ij; !ij.end(); ++ij) {
    fluxdata->flux_vector_element(ij) = cchy(ij.row(),ij.col());
  }
}


// Evaluates elasto-plastic derivatives of the stress flux wrt the
// displacement dofs.
void Plasticity::flux_matrix(const FEMesh *mesh,
			     const Element *element,
			     const ElementFuncNodeIterator& node,
			     const Flux *flux,
			     const MasterPosition &mpt,
			     double time,
			     SmallSystem *fluxmtx)
  const
{
  // LINSYS STEP 4, plastic version -- called from
  // Property::make_flux_contributions, because we are a Flux
  // property, and need to populate the flux matrix.
  PlasticData *pd = dynamic_cast<PlasticData*>
    (element->getDataByName("plastic_data"));
  int gptidx = (pd->mctogpi_map)[mpt.mastercoord()];
  const Rank4_3DTensor &w = (pd->gptdata[gptidx])->w_mat;

  // TODO: Store f_tau_i in the PlasticData object.
  // Or, alternatively, store b_inverse there.
  SmallMatrix3 f_tau = (pd->gptdata[gptidx])->f_tau;
  SmallMatrix3 f_tau_i = f_tau.invert();
  SmallMatrix3 b_inverse;
  for(int k=0;k<3;++k) {
    for(int m=0;m<3;++m) {
      double res = 0.0;
      for(int n = 0; n<3; ++n) {
	res += f_tau_i(n,k)*f_tau_i(n,m);
      }
      b_inverse(k,m) = res;
    }
  }

  double displacedsfdvs[3];
  for(int idx=0; idx<3; ++idx) {
    displacedsfdvs[idx]=node.displacedsfderiv(element,idx,mpt,mesh);
  }

  SymmMatrix3 &cauchy = (pd->gptdata[gptidx])->cauchy; 
  for(SymTensorIterator ij; !ij.end(); ++ij) {
    for(IteratorP kay = displacement->iterator(); !kay.end(); ++kay) {
      for(int ell = 0; ell < 3; ++ell) {
	for(int emm = 0; emm < 3; ++emm) {
	  fluxmtx->stiffness_matrix_element( ij, displacement, kay, node) +=
	    w(ij.row(),ij.col(),ell,emm)*
	    b_inverse(kay.integer(),emm)*displacedsfdvs[ell];
	}
	// Geometric part:
	// fluxmtx->stiffness_matrix_element( ij, displacement, kay, node) -=
	//   cauchy(ij.row(),ell)*displacedsfdvs[ell];
      }
    }
  }

  // The fluxmtx object should also have a geometric part, whose
  // columns are the DOF components as for the
  // stiffness_matrix_element, but whose rows correspond to the
  // divergence of the flux, not to the flux itself. The equation can
  // then just insert this contribution directly into the master
  // stiffness matrix, assuming it does the indexing correctly.

  // Matrix is (dN_nu/dx_k)(dN_mu/dx_j)(sigma_ij) where sigma is the
  // Cauchy stress.  DOF indices are nu,k; EQN indices are mu,i, and
  // the j-index is contracted.  Cauchy stress is in
  // (pd->gptdata[gptidx])->cauchy, and is up to date when we are
  // called.

  // TODO OPT: Do this at the gauss-point loop, not inside the node loop.
  // SymmMatrix3 &cauchy = (pd->gptdata[gptidx])->cauchy; 
  //   for(SymTensorIterator ij; !ij.end(); ++ij) {
  //   for(IteratorP kay = displacement->iterator(); !kay.end(); ++kay) {
  //     fluxmtx->geometry_matrix_element( ij.row(), displacement, kay, node ) +=
  //  cauchy(ij.row(),ij.col())*displacedsfdvs[ij.col()]*(ij.diagonal() ? 2.0 : 1.0);
  //   }
  // }
 
}


// The magic 12 is the number of slip systems in FCC.
FCCPlasticity::FCCPlasticity(PyObject *reg, const std::string &nm,
			     const Cijkl &c, PlasticConstitutiveRule *r)
  : Plasticity(reg,nm,c,r, 12) {

  // std::cerr << "Crystal C_ijkl: " << std::endl;
  // std::cerr << xtal_cijkl_ << std::endl;
  // std::cerr << "Done." << std::endl;
  //
  // Populate the schmid_tensor data member.
  xtal_schmid_tensors.resize(nslips); // Base class knows nslips at this point.
  double n[3];
  double s[3];
  //
  // 1 1 1 planes.
  n[0]=1.0; n[1]=1.0; n[2]=1.0;
  //
  s[0]=0.0; s[1]=1.0; s[2]=-1.0;
  xtal_schmid_tensors[0]=_normalized_outer_product(s,n);
  //
  s[0]=-1.0; s[1]=0.0; s[2]=1.0;
  xtal_schmid_tensors[1]=_normalized_outer_product(s,n);
  //
  s[0]=1.0; s[1]=-1.0; s[2]=0.0;
  xtal_schmid_tensors[2]=_normalized_outer_product(s,n);
  //
  // 1 -1 -1 planes
  n[0]=1.0; n[1]=-1.0; n[2]=-1.0;
  //
  s[0]=0.0; s[1]=-1.0; s[2]=1.0;
  xtal_schmid_tensors[3]=_normalized_outer_product(s,n);
  //
  s[0]=-1.0; s[1]=0.0; s[2]=-1.0;
  xtal_schmid_tensors[4]=_normalized_outer_product(s,n);
  //
  s[0]=1.0; s[1]=1.0; s[2]=0.0;
  xtal_schmid_tensors[5]=_normalized_outer_product(s,n);
  //
  // -1 1 -1 planes
  n[0]=-1.0; n[1]=1.0; n[2]=-1.0;
  //
  s[0]=0.0; s[1]=1.0; s[2]=1.0;
  xtal_schmid_tensors[6]=_normalized_outer_product(s,n);
  //
  s[0]=1.0; s[1]=0.0; s[2]=-1.0;
  xtal_schmid_tensors[7]=_normalized_outer_product(s,n);
  //
  s[0]=-1.0; s[1]=-1.0; s[2]=0.0;
  xtal_schmid_tensors[8]=_normalized_outer_product(s,n);
  //
  // -1 -1 1 planes
  n[0]=-1.0; n[1]=-1.0; n[2]=1.0;
  //
  s[0]=0.0; s[1]=-1.0; s[2]=-1.0;
  xtal_schmid_tensors[9]=_normalized_outer_product(s,n);
  //
  s[0]=1.0; s[1]=0.0; s[2]=1.0;
  xtal_schmid_tensors[10]=_normalized_outer_product(s,n);
  //
  s[0]=-1.0; s[1]=1.0; s[2]=0.0;
  xtal_schmid_tensors[11]=_normalized_outer_product(s,n);

}



/////////////////////////////////////////////////
// Outputs! Coming soon!

void Plasticity::output(const FEMesh* mesh,
			const Element *e,
			const PropertyOutput *po,
			const MasterPosition &pos,
			OutputVal *v) const {
  return;
}
