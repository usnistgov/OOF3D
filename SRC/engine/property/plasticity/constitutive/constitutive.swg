// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CONSTITUTIVE_SWG
#define CONSTITUTIVE_SWG

%module constitutive

%{
#include "engine/property/plasticity/constitutive/constitutive.h"
%}

%include "common/typemaps.swg"
%include "engine/typemaps.swg"


class PlasticConstitutiveRule {
}

class PowerLawConstitutiveRule : public PlasticConstitutiveRule {
public:
  PowerLawConstitutiveRule(double w1, double w2, double ss, double a,
			   double h0, double m, double g0dot,
			   double init_res);
}


class ElasticConstitutiveRule : public PlasticConstitutiveRule {
public:
  ElasticConstitutiveRule();
}
  
%pragma(python) include="constitutive.spy"

#endif // CONSTITUIVE_SWG
