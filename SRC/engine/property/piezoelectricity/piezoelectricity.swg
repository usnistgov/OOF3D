// -*- C++ -*-
// $RCSfile: piezoelectricity.swg,v $
// $Revision: 1.10.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:46:01 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef PIEZOELECTRICITY_SWG
#define PIEZOELECTRICITY_SWG

%module piezoelectricity

%{
#include "engine/property/piezoelectricity/piezoelectricity.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%pragma(python) code="from ooflib.SWIG.engine.symmmatrix import SymmMatrix3Ptr"
%extern "engine/symmmatrix.swg"
%pragma(python) code="from ooflib.SWIG.engine.rank3tensor import Rank3TensorPtr"
%extern "engine/rank3tensor.swg"

class IsotropicPiezoElectricity : public Property {
public:
  IsotropicPiezoElectricity(PyObject *reg, char *name, double d);
};

class AnisotropicPiezoElectricity : public Property {
public:
  AnisotropicPiezoElectricity(PyObject *registry, char *name,
			      Rank3Tensor *dijkTensor);
  Rank3Tensor dijk();
};

%pragma(python) include="piezoelectricity.spy"

#endif // PIEZOELECTRICITY_SWG
