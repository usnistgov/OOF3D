// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PLASTICITY_SWG
#define PLASTICITY_SWG

%module plasticity

%{
#include "engine/property/plasticity/plasticity.h"
#include "engine/property/elasticity/cijkl.h"
%}

%include "common/typemaps.swg"
%include "engine/propertyhdr.swg"
%extern "engine/property/elasticity/cijkl.swg"
%pragma(python) code="from ooflib.SWIG.engine.property.elasticity.cijkl import CijklPtr"

class Plasticity : public Property {
public:
  Cijkl cijkl(const FEMesh*, const Element*, const MasterPosition&);
}

class CPlasticity : public Plasticity {
public:
  CPlasticity(PyObject *reg, PyObject *self, char *name, Cijkl &c);
  ~CPlasticity();
};

%pragma(python) include="plasticity.spy"
   
# endif // PLASTICITY_SWG
