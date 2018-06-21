// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// Constitutive rules for plasticity. Base class knows that there are
// Schmid tensors, can add and remove plastic data from the elements.
// The specifics of what the plastic data actually contains and what
// it means, dynamically speaking, is up to the subclasses.

// Every constitutive rule has some number of slip systems, set by the
// containing plasticity property, which knows the crystallography.

#ifndef CONSTITUTIVE_H
#define CONSTITUTIVE_H

#include "engine/property/plasticity/plasticity.h"
#include <oofconfig.h>


class PowerLawSlipData : public GptSlipData {
public:
  PowerLawSlipData(int slips, double res);
  std::vector<double> res;
  std::vector<double> dgam;
  std::vector<double> dgam_dta;
  std::vector<double> tau_alpha;
};

class PlasticConstitutiveRule {
public:
  virtual void set_slip_systems(int n) { slip_systems = n; }
  virtual GptSlipData *getSlipData() = 0;
protected:
  int slip_systems;

};

class PowerLawConstitutiveRule : public PlasticConstitutiveRule {
public:
  PowerLawConstitutiveRule(double w1,
			   double w2,
			   double ss,
			   double a,
			   double h0,
			   double m,
			   double g0dot,
			   double dt,
			   double init_res) :
    w1(w1),w2(w2),ss(ss),a(a),h0(h0),m(m),g0dot(g0dot),dt(dt),init_res(init_res)
  {}
  virtual GptSlipData *getSlipData();
private:
  double w1,w2,ss,a,h0,m,g0dot,dt,init_res;
  
};


#endif // CONSTITUTIVE_H

