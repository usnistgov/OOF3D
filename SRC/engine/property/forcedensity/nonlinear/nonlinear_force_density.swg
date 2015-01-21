// -*- C++ -*-
// $RCSfile: nonlinear_force_density.swg,v $
// $Revision: 1.4.8.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:44 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

%module forcedensity

%{
#include "engine/property/forcedensity/nonlinear/nonlinear_force_density.h"
%}
%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"

%pragma(python) include="nonlinear_force_density.spy"

class NonlinearForceDensityNoDeriv : public Property {
};

class NonlinearForceDensity : public NonlinearForceDensityNoDeriv {
};

class TestNonlinearForceDensityNoDeriv : public NonlinearForceDensityNoDeriv {
public:
  TestNonlinearForceDensityNoDeriv(PyObject *reg, char *name, int testno);
};

class TestNonlinearForceDensity : public NonlinearForceDensity {
public:
  TestNonlinearForceDensity(PyObject *reg, char *name, int testno);
};
