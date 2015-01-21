// -*- C++ -*-
// $RCSfile: iso.swg,v $
// $Revision: 1.17.2.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:31 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ISO_SWG
#define ISO_SWG

%module iso

%{
#include "engine/property/elasticity/iso/iso.h"
%}

%include "engine/typemaps.swg"
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.elasticity import ElasticityPtr"
%extern "engine/property/elasticity/elasticity.swg"

%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.cijkl import CijklPtr"
%extern "engine/property/elasticity/cijkl.swg"


class CIsoElasticityProp : public Elasticity {
public:
  CIsoElasticityProp(PyObject*, PyObject*, char*, Cijkl&);
  ~CIsoElasticityProp();
};

%pragma(python) include="iso.spy"

#endif // ISO_SWG
