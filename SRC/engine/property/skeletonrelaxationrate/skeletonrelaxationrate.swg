// -*- C++ -*-
// $RCSfile: skeletonrelaxationrate.swg,v $
// $Revision: 1.5.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:46:03 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef SKELETONRELAXATIONRATE_SWG
#define SKELETONRELAXATIONRATE_SWG

%module skeletonrelaxationrate

%{
#include "engine/property/skeletonrelaxationrate/skeletonrelaxationrate.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
// %pragma(python) code="from ooflib.SWIG.engine.symmmatrix import SymmMatrix3Ptr"
// %extern "engine/symmmatrix.swg"


class SkeletonRelaxationRate : public Property {
public:
  SkeletonRelaxationRate(PyObject *reg, char *name, double alpha, double beta);
  const double alpha();
};

%pragma(python) include="skeletonrelaxationrate.spy"

// %typemap(python,in) SymmMatrix * {}

#endif // SKELETONRELAXATIONRATE_SWG
