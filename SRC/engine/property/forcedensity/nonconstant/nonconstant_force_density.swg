// -*- C++ -*-
// $RCSfile: nonconstant_force_density.swg,v $
// $Revision: 1.3.14.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:42 $

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
#include "engine/property/forcedensity/nonconstant/nonconstant_force_density.h"
%}
%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"

%pragma(python) include="nonconstant_force_density.spy"

class NonconstantForceDensity : public Property {
};


class TestNonconstantForceDensity : public Property {
public:
  TestNonconstantForceDensity(PyObject *reg, char *name, int testno);
};
