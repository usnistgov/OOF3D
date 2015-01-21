// -*- C++ -*-
// $RCSfile: largestrain.swg,v $
// $Revision: 1.1.18.3 $
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

#ifndef LARGESTRAIN_SWG
#define LARGESTRAIN_SWG

%module largestrain

%{
#include "engine/property/elasticity/largestrain/largestrain.h"
%}

%include "engine/typemaps.swg"
%include "engine/propertyhdr.swg"
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.cijkl import CijklPtr"
%extern "engine/property/elasticity/cijkl.swg"


%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.elasticity import ElasticityPtr"
%extern "engine/property/elasticity/elasticity.swg"

class CIsoLargeStrainElasticity : public Elasticity {
public:
  CIsoLargeStrainElasticity(PyObject*, PyObject*, char*, Cijkl&);
  ~CIsoLargeStrainElasticity();
};

class CAnisoLargeStrainElasticity : public Elasticity {
public:
  CAnisoLargeStrainElasticity(PyObject*, PyObject*, char*, Cijkl&);
  ~CAnisoLargeStrainElasticity();
};


%pragma(python) include="largestrain.spy"

#endif // LARGESTRAIN_SWG
