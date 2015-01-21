// -*- C++ -*-
// $RCSfile: aniso.swg,v $
// $Revision: 1.17.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:30 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ANISO_SWG
#define ANISO_SWG

%module aniso

%{
#include "engine/property/elasticity/aniso/aniso.h"
#include "engine/property/elasticity/cijkl.h"
%}

%include "engine/typemaps.swg"
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.elasticity import ElasticityPtr"
%extern "engine/property/elasticity/elasticity.swg"

// The following fixes the return-type for the SWIG'd crystal_cijkl()
// routine, and allows the anisoelasticity's repr functions to work.
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.cijkl import CijklPtr"
%extern "engine/property/elasticity/cijkl.swg"


class CAnisoElasticity : public Elasticity
{
public:
  CAnisoElasticity(PyObject *registry, PyObject *self, char *name, Cijkl &c);
  ~CAnisoElasticity();
  const Cijkl crystal_cijkl();
};

%pragma(python) include="aniso.spy"

#endif // ANISO_SWG
