// -*- C++ -*-
// $RCSfile: boundarycond.h,v $
// $Revision: 1.19.6.3 $
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

#include <oofconfig.h>

#ifndef BOUNDARYCOND_H
#define BOUNDARYCOND_H

#include <vector>
#include <map>
#include "common/tostring.h"

class CompoundField;
class Field;
class Flux;
class Equation;
class FuncNode;
class CSubProblem;
class LinearizedSystem;

// FloatBCApp is the "applicator" for the floating boundary
// condition class, which is in Python.  The calling semantics
// are that, when you get to this level, you should have
// a DOF and a nodalequation in-hand, along with the
// mapping lists. 

class FloatBCApp {
public:
  FloatBCApp() {}
  ~FloatBCApp() {}
  void editmap(LinearizedSystem*,
	       double, FuncNode *, Field *, int,
	       Equation *, int, int, int, int, double);
  typedef std::map<int, double> ProfileData;
  ProfileData profile_data;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// "Applicator" for the flux boundary condition, NeumannBC. 

#if DIM==2

class EdgeSet;

class NeumannBCApp {
private:
  CSubProblem *subproblem;
  LinearizedSystem *linearsystem;
  Flux *flux;
  EdgeSet *bdy;
public:
  NeumannBCApp(CSubProblem *m, LinearizedSystem *ls, Flux *f, EdgeSet *b)
    : subproblem(m), linearsystem(ls), flux(f), bdy(b)
  {}
  ~NeumannBCApp() {}
  void integrate(PyObject *, PyObject *, bool, double time);
};

#else // DIM==3

class FaceSet;

class NeumannBCApp {
private:
  CSubProblem *subproblem;
  LinearizedSystem *linearsystem;
  Flux *flux;
  FaceSet *bdy;
public:
  NeumannBCApp(CSubProblem *m, LinearizedSystem *ls, Flux *f, FaceSet *b)
    : subproblem(m), linearsystem(ls), flux(f), bdy(b)
  {}
  ~NeumannBCApp() {}
  void integrate(PyObject*, PyObject*, double);
};
#endif // DIM==3

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ForceBC is the node-based twin of NeumannBC.  Fluxes make sense to
// integrate, forces are associated with equations and make sense for
// direct application at nodes.

void applyForceBC(CSubProblem*, LinearizedSystem*,
		  Equation*, FuncNode*, int eqnindex, double value);
  
#endif

