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

// Magic for converting a parameter argument to a Cijkl.
%typemap(python,in) Cijkl * (Cijkl *c) {
   PyObject *wrapped_cijkl = PyObject_CallMethod($source,
 						 (char *)"tensorForm", NULL);
   if(!wrapped_cijkl) {
     restoreSignals;
     return 0;
   }
   PyObject *cijkl_str = PyObject_GetAttrString(wrapped_cijkl,"this");
   if(!cijkl_str) { return NULL; }
   char *_str = PyString_AsString(cijkl_str);
   SWIG_GetPtr(_str, (void **)&c, "_Cijkl_p");
   $target = c;
   // TODO: Ownership?
}




   
class Plasticity : public Property {
public:
  const Cijkl cijkl(const FEMesh*, const Element*, const MasterPosition&);
}

class FCCPlasticity : public Plasticity {
public:
  FCCPlasticity(PyObject *, char *, Cijkl &);
  virtual ~FCCPlasticity();
}

%pragma(python) include="plasticity.spy"
   
# endif // PLASTICITY_SWG
