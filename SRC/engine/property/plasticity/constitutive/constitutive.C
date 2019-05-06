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
#include "engine/property/plasticity/constitutive/constitutive.h"



PowerLawSlipData::PowerLawSlipData(int slips, double initial_r)
  : GptSlipData(slips) {
  for(int i=0;i<slips;++i) {
    res.push_back(initial_r);
    tau_alpha.push_back(0.0);
  }
}

GptSlipData *PowerLawConstitutiveRule::getSlipData() const {
  return new PowerLawSlipData(slip_systems, init_res);
}

void PowerLawConstitutiveRule::evolve(GptPlasticData *gptpd,
				      GptSlipData *gptsd) {
  // GptSlipData is not polymorphic (has no functions at all, in fact),
  // it's a data class, so static cast is right.
  PowerLawSlipData *plsd = static_cast<PowerLawSlipData*>(gptsd);

  total_res = plsd->res;
  _evolve_hardening(plsd);
  for(int alpha=0;alpha<slip_systems;++alpha) {
    total_res[alpha] += delta_res[alpha];
  }
  _evolve_gamma(plsd);
}

// Updates delta_res.
void PowerLawConstitutiveRule::_evolve_hardening(PowerLawSlipData *plsd) {
  double const_qab;
  double ratio_res;

  delta_res.resize(slip_systems);

  for(int alpha=0;alpha<slip_systems;++alpha) {
    delta_res[alpha] = 0.0;
    for(int beta=0;beta<slip_systems;++beta) {
      if (alpha==beta) {
	const_qab = w1; // Self-hardening
      }
      else {
	const_qab = w2; // Latent hardening
      }
      ratio_res = 1.0-total_res[beta]/ss;
      delta_res[alpha] += const_qab*h0*abs(plsd->delta_gamma[beta])*(pow(ratio_res,a));
    }
  }
}

void PowerLawConstitutiveRule::_evolve_gamma(PowerLawSlipData *plsd) {
  double ratio_alpha = 0.0;
  double const_sign = 0.0;
  double m_inv = 0.0;
  double res_inv = 0.0;

  for(int alpha=0;alpha<slip_systems;++alpha) {
    if (total_res[alpha] >= 1.0) {
      ratio_alpha = plsd->tau_alpha[alpha]/total_res[alpha];

      if (plsd->tau_alpha[alpha]>=0.0)
	const_sign = 1.0;
      else
	const_sign = 0.0;

      m_inv = 1.0/m;

      plsd->delta_gamma[alpha] = dt*const_sign*g0dot*(pow(abs(ratio_alpha),m_inv));

      res_inv = 1.0/total_res[alpha];

      // Derivative is reason
      plsd->dgamma_dtau[alpha] = dt*res_inv*g0dot*m_inv*(pow(abs(ratio_alpha),(m_inv-1.0)));
      
    }
    else {
      plsd->delta_gamma[alpha] = 0.0;
      plsd->dgamma_dtau[alpha] = 0.0;
    }
  }
}

void PowerLawConstitutiveRule::complete(GptPlasticData *gptpd,
					GptSlipData *gptsd) {
  PowerLawSlipData *plsd = static_cast<PowerLawSlipData*>(gptsd);

  plsd->res = total_res;
  
}
// ----- ELASTIC -----


// ElasticLawSlipData -- cumulative slip is zero. 
ElasticLawSlipData::ElasticLawSlipData(int nslips)
  : GptSlipData(nslips) {}


GptSlipData *ElasticConstitutiveRule::getSlipData() const {
  return new ElasticLawSlipData(slip_systems);
}

// ElasticConstitutiveRule -- needs to set the gptsd slip
// accumulations to zero.  Somehow.
void ElasticConstitutiveRule::evolve(GptPlasticData *gptpd,
				     GptSlipData *gptsd) {
  ElasticLawSlipData *elsd = static_cast<ElasticLawSlipData*>(gptsd);
  // Done!  The slip data is initialized to zeros, and is still zero,
  // which is the right answer for elasticity, so there's nothing to
  // do.
}

// All const. rules have to have this, ours is trivial.
void ElasticConstitutiveRule::complete(GptPlasticData *gptpd,
				       GptSlipData *gptsd) {
}

