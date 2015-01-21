// -*- C++ -*-
// $RCSfile: csubproblem.swg,v $
// $Revision: 1.22.2.8 $
// $Author: fyc $
// $Date: 2015/01/07 15:53:12 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef SUBPROBLEM_SWG
#define SUBPROBLEM_SWG

%module subproblem

%include "engine/typemaps.swg"
%extern "common/cmicrostructure.swg"
%extern "common/doublevec.swg"
%extern "common/lock.swg"
%extern "engine/element.swg"
%extern "engine/equation.swg"
%extern "engine/femesh.swg"
%extern "engine/field.swg"
%extern "engine/linearizedsystem.swg"
%extern "engine/meshiterator.swg"
%extern "engine/node.swg"

%pragma(python) code="from ooflib.SWIG.common.lock import LockPtr"
%pragma(python) code="from ooflib.SWIG.common.lock import RWLockPtr"
%pragma(python) code="from ooflib.SWIG.common.doublevec import DoubleVecPtr"
%pragma(python) code="from ooflib.SWIG.engine.equation import EquationPtr"
%pragma(python) code="from ooflib.SWIG.engine.femesh import FEMeshPtr"
%pragma(python) code="from ooflib.SWIG.engine.field import FieldPtr"
%pragma(python) code="from ooflib.SWIG.engine.linearizedsystem import LinearizedSystemPtr"
%pragma(python) code="from ooflib.SWIG.engine.meshiterator import ElementIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.meshiterator import FuncNodeIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.meshiterator import NodeIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.nodalequation import NodalEquationPtr"

%pragma(python) include="csubproblem.spy"

%{
#include "common/doublevec.h"
#include "engine/cconjugate.h"
#include "engine/csubproblem.h"
#include "engine/femesh.h"
#include "engine/material.h"
#include "engine/meshiterator.h"
#include "engine/sparsemat.h"
#include <vector>
typedef std::vector<CConjugatePair*> CConjugateVec;
%}

%typemap(python, in) CConjugateVec * (CConjugateVec cv) {
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		 "Type Error in CConjugateVec typemap.  Python list required.");
    return NULL;
  }
  CConjugateVec::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
						 Py_ssize_t,
						 CConjugateVec::size_type);
  cv.resize(sz);
  for(CConjugateVec::size_type i=0; i<sz; i++) {
    CConjugatePair *pair;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**) &pair, "_CConjugatePair_p");
    cv[i] = pair;
  }
  $target = &cv;
}


class CSubProblem {
public:
//   CSubProblem(FEMesh*);	// only derived classes can be constructed
  ~CSubProblem();

  void set_rwlock(RWLock *rw);
  RWLock * get_rwlock();
  void set_mesh(FEMesh*);
  // A comment in femesh.spy says that FEMesh objects are never
  // returned from C++ to python. get_mesh() was only used in 2D.
  FEMesh *get_mesh();
  void set_nnodes(int);

  int ndof();
  int neqn();

  int nelements();
  int nnodes();
  int nfuncnodes();

  bool containsNode(Node*);

  Lock precomputeLock;
  bool consistency;
  
//%readwrite
  bool precomputeRequired;
  void requirePrecompute();
  void redefined();

  // These iterator methods should not be used directly in Python.
  // Real iteratable objects (that use these methods) are returned by
  // CSubProblem.elements(), CSubProblem.nodes(), and
  // CSubProblem.funcnodes().
  ElementIterator element_iterator();
  NodeIterator node_iterator();
  FuncNodeIterator funcnode_iterator();

  %new LinearizedSystem *new_linear_system(double);
  void make_linear_system(LinearizedSystem *, CNonlinearSolver*);

  %new CompoundFieldVec *all_compound_fields();
  %new EquationVec *all_equations();
  %new FluxVec *all_fluxes();

  %new MaterialSet *getMaterials();
  void cache_active_prop(Property*, bool);
  bool currently_active_prop(Property*);
  void cache_nonlinearity_prop(Property*, bool);
  bool currently_nonlinear_prop(Property*);
 
  bool define_field(Field&);
  void undefine_field(Field&);
  bool is_defined_field(Field&);
  void activate_field(Field&);
  void deactivate_field(Field&);
  bool is_active_field(Field&);
  int n_active_fields();
  void acquire_field_data(Field &field, const CSubProblem*);

  bool is_active_flux(Flux&);

  void activate_equation(Equation&);
  void deactivate_equation(Equation&);
  bool is_active_equation(Equation&);
  int n_active_eqns();

  void setStaticStepper(bool);
  bool staticStepper();

  void mapFields();
  bool set_meshdofs(DoubleVec*);
  %new DoubleVec *get_meshdofs();

  void set_slaveDoF(int);
  void clear_slaveDoFs();

  void post_process();

  // for symmetrizing the stiffness matrix, if at all possible
//   void set_trivial_equation_mapping();
  void set_equation_mapping(CConjugateVec*);

#ifdef HAVE_MPI
  int GatherNumNodes();
  void set_parallel_mapping();
#endif

  //AMR subproblem
  // SCPatch stuff, which should be encapsulated elsewhere eventually
  void init_scpatches(IntVec*);
  void add_scpatch(int, Material*, int, IntVec*, IntVec*, int);
  %new IntVec *get_elements_from_patch(int, Material*);
  %new IntVec *get_nodes_from_patch(int, Material*);
  void init_nodalfluxes();
  void recover_fluxes();
  void report_recovered_fluxes(Element*, Coord *Point);
  double zz_L2_estimate(Element*, Flux*);
  %new DoubleList *zz_L2_weights(Flux*, double, double);
  bool contains(Element*);

  %addmethods {
    int __hash__() {
      return self->objectid();
    }
  }

};				// class CSubProblem

long get_globalCSubProblemCount();


#endif // SUBPROBLEM_SWG
