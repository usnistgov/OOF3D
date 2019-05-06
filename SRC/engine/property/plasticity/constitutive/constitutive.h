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


// Constitutive-rule-specific stored at the gausspoints to preserve
// local state across time iterations.  Stored in the SlipData object,
// managed by the Plasticity property class.  Actually, some of the
// data in here (delta_gamma, dgamma_dtau) is needed for any
// constitutive rule, so it's not special to any particular one.  The
// argument for keeping this data here is that it reduces the number
// of data objects that a constitutive-rule author needs to worry
// about.  It's duplicative, though, so it's a bit ugly.
class PowerLawSlipData : public GptSlipData {
public:
  PowerLawSlipData(int slips, double res);
  std::vector<double> res;         // Initial slip resistance.
  std::vector<double> tau_alpha;   // Resolved shear stress.
};

class PlasticConstitutiveRule {
public:
  virtual void set_slip_systems(int n) { slip_systems = n; }
  virtual GptSlipData *getSlipData() const = 0;
  virtual void evolve(GptPlasticData *, GptSlipData*) = 0;
  virtual void complete(GptPlasticData *, GptSlipData*) = 0;
protected:
  int slip_systems;
};


// TODO: The "dt" parameter here is the time-step size, it should not
// be provided by users here, but should come from the solver
// infrastructure.
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
  virtual GptSlipData *getSlipData() const;
  virtual void evolve(GptPlasticData *, GptSlipData*);
  virtual void complete(GptPlasticData *, GptSlipData*);
private:
  double w1,w2,ss,a,h0,m,g0dot,dt,init_res;
  std::vector<double> total_res,delta_res;
  void _evolve_hardening(PowerLawSlipData*);
  void _evolve_gamma(PowerLawSlipData*);
};

// ----- ELASTIC ------

// The ElasticConstitutiveRule is a trivial constitutive rule
// whose main role is to exercise the API.  It doesn't do any
// plastic evolution, and its state object is trivial.

class ElasticLawSlipData : public GptSlipData {
public:
  ElasticLawSlipData(int slips);
};


class ElasticConstitutiveRule : public PlasticConstitutiveRule {
public:
  ElasticConstitutiveRule() {}
  virtual GptSlipData *getSlipData() const;
  virtual void evolve(GptPlasticData*, GptSlipData*);
  virtual void complete(GptPlasticData*, GptSlipData*);
};
  

#endif // CONSTITUTIVE_H

