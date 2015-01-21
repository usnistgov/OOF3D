// -*- C++ -*-
// $RCSfile: heatsource.swg,v $
// $Revision: 1.2.16.3 $
// $Author: langer $
// $Date: 2014/09/27 22:34:32 $

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
#include "engine/property/heatsource/heatsource.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%extern "engine/symmmatrix.swg"

%pragma(python) include="heatsource.spy"

class HeatSourceProp : public Property {
public:
  HeatSourceProp(PyObject *reg, char *name, double qdot);
};
