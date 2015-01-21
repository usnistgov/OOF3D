// -*- C++ -*-
// $RCSfile: nonlinear_heat_source.swg,v $
// $Revision: 1.3.8.3 $
// $Author: langer $
// $Date: 2014/09/27 22:34:33 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

%module heatsource

%{
#include "engine/property/heatsource/nonlinear/nonlinear_heat_source.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%extern "engine/symmmatrix.swg"

%pragma(python) include="nonlinear_heat_source.spy"

class NonlinearHeatSourceNoDeriv : public Property {
};

class NonlinearHeatSource : public NonlinearHeatSourceNoDeriv {
};

class TestNonlinearHeatSourceNoDeriv : public NonlinearHeatSourceNoDeriv {
public:
  TestNonlinearHeatSourceNoDeriv(PyObject *reg, char *name, int testno);
};

class TestNonlinearHeatSource : public NonlinearHeatSource {
public:
  TestNonlinearHeatSource(PyObject *reg, char *name, int testno);
};
