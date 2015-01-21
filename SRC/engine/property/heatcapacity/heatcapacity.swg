// -*- C++ -*-
// $RCSfile: heatcapacity.swg,v $
// $Revision: 1.7.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:46 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef HEATCAPACITY_SWG
#define HEATCAPACITY_SWG

%module heatcapacity

%{
#include "engine/property/heatcapacity/heatcapacity.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"

class HeatCapacityProp : public Property {
public:
  HeatCapacityProp(PyObject *self, char *, double);
};

%pragma(python) include="heatcapacity.spy"

#endif // HEATCAPACITY_SWG
