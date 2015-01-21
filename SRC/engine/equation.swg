// -*- C++ -*-
// $RCSfile: equation.swg,v $
// $Revision: 1.51.4.2 $
// $Author: langer $
// $Date: 2013/11/08 20:44:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef EQUATION_SWG
#define EQUATION_SWG

%module equation
%include "engine/typemaps.swg"
%extern "engine/nodalequation.swg"
%extern "engine/planarity.swg"
%extern "engine/flux.swg"
%extern "engine/csubproblem.swg"

%{
#include "engine/equation.h"
%}

%pragma(python) include="equation.spy"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IteratorPPtr"
%pragma(python) code="from ooflib.SWIG.engine.fieldindex import IndexPPtr"

%pragma(python) code="from ooflib.SWIG.engine.flux import FluxPtr"

%typemap(python, out) Equation* {
   // typemap(python, out) Equation*
   $target = $source->pythonObject();
   if(!$target)
     return 0;
}

class Equation {
public:
  const string &name();
  int objectid();
  int dim();
  int ndof();			// same as dim()
  // string fluxname();
  // Flux *flux();
  NodalEquation *nodaleqn(const FuncNode&, int);
  IteratorP iterator();
  %addmethods{
    // iterator_all is used in situations in which it's not known if
    // we're iterating over a Field, Flux, or Equation.
    // Field::iterator and Flux::iterator take an argument, but
    // iterator_all doesn't.
    IteratorP iterator_all() {
      return self->iterator();
    }
  }
  IndexP componenttype();
  IndexP getIndex(char*);
  int is_active(const CSubProblem*);
  bool allow_boundary_conditions();
};

class FluxEquation : public Equation {
public:
  const string &fluxname();
  Flux *flux();
};

// Natural equations don't require a flux.
class NaturalEquation : public Equation {
public:
  NaturalEquation(char *name, int dim);
};

class DivergenceEquation : public FluxEquation {
public:
  DivergenceEquation(char *name, Flux &flux, int dim);
};

class PlaneFluxEquation : public FluxEquation {
public:
  PlaneFluxEquation(char *name, Flux &flux, int dim);
};

int countEquations();
Equation *getEquationByIndex(int);
Equation *getEquationByName(char *);

%{
  Equation *getEquationByName(const std::string &name) {
    return Equation::getEquation(name);
  }
%}

#endif // EQUATION_SWG
