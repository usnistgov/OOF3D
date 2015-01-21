// -*- C++ -*-
// $RCSfile: stressfreestrain.swg,v $
// $Revision: 1.2.18.1 $
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

#ifndef STRESSFREESTRAIN_SWG
#define STRESSFREESTRAIN_SWG

%module stressfreestrain

%{
#include "engine/property/stressfreestrain/stressfreestrain.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%pragma(python) code="from ooflib.SWIG.engine.symmmatrix import SymmMatrix3Ptr"
%extern "engine/symmmatrix.swg"


class IsotropicStressFreeStrain : public Property {
public:
  IsotropicStressFreeStrain(PyObject *reg, char *name, double e);
};

class AnisotropicStressFreeStrain : public Property {
public:
  AnisotropicStressFreeStrain(PyObject *reg, char *naem, SymmMatrix3 *e);
};

%pragma(python) include="stressfreestrain.spy"

%typemap(python, in) SymmMatrix * {}

#endif	// STRESSFREESTRAIN_SWG
