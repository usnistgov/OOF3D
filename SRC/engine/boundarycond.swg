// -*- C++ -*-
// $RCSfile: boundarycond.swg,v $
// $Revision: 1.35.6.3 $
// $Author: langer $
// $Date: 2014/02/24 22:33:36 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BOUNDARYCOND_SWG
#define BOUNDARYCOND_SWG

%module boundarycond
%include "engine/typemaps.swg"

%{
#include "engine/boundarycond.h"
#include "engine/flux.h"
#include "engine/fluxnormal.h"
#include "common/tostring.h"
#include "common/coord.h"
%}

class FloatBCApp {
public:
  FloatBCApp();
  ~FloatBCApp();
  void editmap(LinearizedSystem*, double, FuncNode *, 
	       Field *, int,
	       Equation *, int, int, int, int, double);
};

class NeumannBCApp {
public:
  ~NeumannBCApp();
#ifndef DIM_3
  NeumannBCApp(CSubProblem *m, LinearizedSystem*, Flux *f, EdgeSet *b);
  void integrate(PyObject *pythonCallable, PyObject *pythonCallable,
		 bool normal, double time);
#else // DIM==3
  NeumannBCApp(CSubProblem *m, LinearizedSystem*, Flux *f, FaceSet *b);
  void integrate(PyObject *pythonCallable, PyObject *pythonCallable,
		 double time);
#endif // DIM==3
};

/* ForceBC differs from NeumannBC in that it applies point forces
   directly at nodes. */
void applyForceBC(CSubProblem*, LinearizedSystem*, Equation*, FuncNode*,
		  int, double);

#endif // BOUNDARYCOND_SWG
