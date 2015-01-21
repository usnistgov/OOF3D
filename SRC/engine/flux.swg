// -*- C++ -*-
// $RCSfile: flux.swg,v $
// $Revision: 1.30.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:25 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef FLUX_SWG
#define FLUX_SWG

%module flux

%include "engine/typemaps.swg"
%{
#include "engine/flux.h"
%}

%pragma(python) include="engine/flux.spy"
%extern "engine/fieldindex.swg"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IteratorPPtr"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IndexPPtr"
%extern "engine/outputval.swg"
%pragma(python) code="from ooflib.SWIG.engine.outputval import OutputValuePtr"



class Flux {
public:
  int ndof();
  int divergence_dim();
  const string &name();
  int objectid();

  IteratorP iterator(Planarity p);
  IteratorP divergence_iterator();
  %addmethods {
    // iterator_all is used in situations in which it's not known if
    // we're iterating over a Field, Flux, or Equation.
    // Equation::iterator doesn't take an argument.
    IteratorP iterator_all() {
      return self->iterator(ALL_INDICES);
    }
  }
  IndexP componenttype();
  OutputValue newOutputValue();
};
  
class VectorFlux : public Flux {
public:
  VectorFlux(char *name);
};

class SymmetricTensorFlux : public Flux {
public:
  SymmetricTensorFlux(char *name);
};

Flux *getFluxByIndex(int);
int countFluxes();

#endif // FLUX_SWG
