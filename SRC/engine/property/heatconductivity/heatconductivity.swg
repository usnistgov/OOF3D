// -*- C++ -*-
// $RCSfile: heatconductivity.swg,v $
// $Revision: 1.22.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:47 $

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
#include "engine/property/heatconductivity/heatconductivity.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%extern "engine/symmmatrix.swg"

%pragma(python) include="heatconductivity.spy"

class IsoHeatConductivity : public Property {
public:
  IsoHeatConductivity(PyObject *reg, char *name, double kappa);
};

class AnisoHeatConductivity : public Property {
public:
  AnisoHeatConductivity(PyObject *reg, char *name, SymmMatrix3 *k);
};
