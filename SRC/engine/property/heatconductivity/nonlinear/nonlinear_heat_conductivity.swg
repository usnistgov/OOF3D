// -*- C++ -*-
// $RCSfile: nonlinear_heat_conductivity.swg,v $
// $Revision: 1.4.8.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:50 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

%module heatconductivity

%{
#include "engine/property/heatconductivity/nonlinear/nonlinear_heat_conductivity.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%extern "engine/symmmatrix.swg"

%pragma(python) include="nonlinear_heat_conductivity.spy"

class NonlinearHeatConductivityNoDeriv : public Property {
};

class NonlinearHeatConductivity : public NonlinearHeatConductivityNoDeriv {
};

class TestNonlinearHeatConductivityNoDeriv : public NonlinearHeatConductivityNoDeriv {
public:
  TestNonlinearHeatConductivityNoDeriv(PyObject *reg, char *name, int testno);
};

class TestNonlinearHeatConductivity : public NonlinearHeatConductivity {
public:
  TestNonlinearHeatConductivity(PyObject *reg, char *name, int testno);
};
