// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

// Base class of plastic constitutive rules.  Separated out so
// it can be imported separately, needed for some applicaitons.

#ifndef CONSTITUTIVE_BASE_H
#define CONSTITUTIVE_BASE_H

class GptSlipData;
class GptPlasticData;

class PlasticConstitutiveRule {
public:
  virtual void set_slip_systems(int n) { slip_systems = n; }
  virtual GptSlipData *getSlipData() const = 0;
  virtual void evolve(GptPlasticData *, GptSlipData*,double) = 0;
  virtual void complete(GptPlasticData *, GptSlipData*) = 0;
protected:
  int slip_systems;
};

#endif // CONSITUTIVE_BASE_H
