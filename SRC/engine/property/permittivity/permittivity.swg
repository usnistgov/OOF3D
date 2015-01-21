// -*- C++ -*-
// $RCSfile: permittivity.swg,v $
// $Revision: 1.7.18.2 $
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

%module permittivity

%{
#include "engine/property/permittivity/permittivity.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"

%pragma(python) code="from ooflib.SWIG.engine.symmmatrix import SymmMatrixPtr"
%extern "engine/symmmatrix.swg"

%pragma(python) include="permittivity.spy"

class IsoDielectricPermittivity : public Property {
public:
  IsoDielectricPermittivity(PyObject *reg, char *name, double epsilon);
};

class AnisoDielectricPermittivity : public Property {
public:
  AnisoDielectricPermittivity(PyObject *reg, char *name, SymmMatrix3 *k);
};

class ChargeDensity : public Property {
public:
  ChargeDensity(PyObject *reg, char *name, double qdot);
  double rho();
};
