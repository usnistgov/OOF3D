// -*- C++ -*-
// $RCSfile: thermalexpansion.swg,v $
// $Revision: 1.22.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:46:05 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

%module thermalexpansion

%{
#include "engine/property/thermalexpansion/thermalexpansion.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%pragma(python) code="from ooflib.SWIG.engine.symmmatrix import SymmMatrix3Ptr"
%extern "engine/symmmatrix.swg"




class IsotropicThermalExpansion : public Property {
public:
  IsotropicThermalExpansion(PyObject *reg, char *name, double alpha, double t0);
};


class AnisotropicThermalExpansion : public Property {
public:
  AnisotropicThermalExpansion(PyObject *registry, char *name, SymmMatrix3 *alpha, double t0);
};

%pragma(python) include="thermalexpansion.spy"

%typemap(python,in) SymmMatrix * {}

