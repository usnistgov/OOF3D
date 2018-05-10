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

#include <oofconfig.h>


class PlasticConstitutiveRule {
public:
  virtual void set_slip_systems(int n) { slip_systems = n; }
protected:
  int slip_systems;

};

class PowerLawConstitutiveRule : public PlasticConstitutiveRule {
public:
  PowerLawConstitutiveRule(double exp) : exponent(exp) {}
private:
  double exponent;
  
};


#endif // CONSTITUTIVE_H

