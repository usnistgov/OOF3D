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



PowerLawSlipData::PowerLawSlipData(int slips, double initial_r) {
  for(int i=0;i<slips;++i) {
    res.push_back(initial_r);
    dgam.push_back(0.0);
    dgam_dta.push_back(0.0);
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
}

// TASK 1:
// Write the "evolve" function that takes the Cauchy stress from
// the outer loop and returns the plastic strain increments
// and their derivatives wrt the strain.
