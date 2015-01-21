// -*- C++ -*-
// $RCSfile: linearizedsystem.swg,v $
// $Revision: 1.13.2.3 $
// $Author: langer $
// $Date: 2014/03/21 00:01:35 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef LINEARIZEDSYSTEM_SWG
#define LINEARIZEDSYSTEM_SWG

%module linearizedsystem
%include "engine/typemaps.swg"
%extern "engine/sparsemat.swg"
%extern "common/doublevec.swg"

%{
#include "common/doublevec.h"
#include "engine/linearizedsystem.h"
#include "engine/sparsemat.h"
%}

%pragma(python) code="from ooflib.SWIG.engine.sparsemat import SparseMatPtr"
%pragma(python) code="from ooflib.SWIG.common.doublevec import DoubleVecPtr"

%pragma(python) include="linearizedsystem.spy"

class LinearizedSystem {
public:
  ~LinearizedSystem();

  %addmethods {
    %new LinearizedSystem *clone_() {
      return new LinearizedSystem(*self);
    }
  }
  
  double time();
  void set_time(double);
  void clearResidual();
  void clearForceBndyRhs();
  void clearBodyRhs();
  void clearMatrices();
  void clearJacobian();
  void cleanmaps();
  void resetFieldFlags();
  int getSubproblemDoFIndex(FuncNode*, Field*, int);
  int getSubproblemEqnIndex(FuncNode*, Equation*, int);
  void profile_rhs(FloatBCApp&);
  void applyFloatBC(int, int, int, int, int, int);
  
  void build_submatrix_maps();
  void build_MCK_maps();

  void fixdof(DegreeOfFreedom*);
  void fixeqn(NodalEquation*);
  bool is_fixed(DegreeOfFreedom*);
  void find_fix_bndy_rhs(DoubleVec*);

  %new DoubleVec* get_unknowns_MCK(DoubleVec*);
  %new DoubleVec* get_unknowns_MCKa(DoubleVec*);
  %new DoubleVec* get_unknowns_MCKd(DoubleVec*);
  
  %new DoubleVec* set_unknowns_MCK(DoubleVec*, DoubleVec*);
  %new DoubleVec* set_unknowns_MCKa(DoubleVec*, DoubleVec*);
  %new DoubleVec* set_unknowns_MCKd(DoubleVec*, DoubleVec*);

  %new DoubleVec* get_unknowns_part(char, DoubleVec*);
  void set_unknowns_part(char, DoubleVec*, DoubleVec*);

  %new DoubleVec* get_fields_MCKd(DoubleVec*);
  void set_fields_MCKd(DoubleVec*, DoubleVec*);

  %new DoubleVec* get_derivs_MCKd(DoubleVec*);
  void set_derivs_MCKd(DoubleVec*, DoubleVec*);

  %new DoubleVec* get_derivs_part_MCKa(char, DoubleVec*);
  %new DoubleVec* get_derivs_part_MCKd(char, DoubleVec*);
  void set_derivs_part_MCKa(char, DoubleVec*, DoubleVec*);
  void set_derivs_part_MCKd(char, DoubleVec*, DoubleVec*);

  %new DoubleVec* extract_MCa_dofs(DoubleVec*);
  void inject_MCa_dofs(DoubleVec*, DoubleVec*);
  void expand_MCa_dofs(DoubleVec*);

  %new DoubleVec* error_estimation_dofs_MCKd(DoubleVec*);

  unsigned int n_unknowns_MCK();
  unsigned int n_unknowns_MCKa();
  unsigned int n_unknowns_MCKd();
  unsigned int n_unknowns_part(char);

  SparseMat K_submatrix(char, char);
  SparseMat C_submatrix(char, char);
  SparseMat M_submatrix(char, char);
  SparseMat J_submatrix(char, char);

  bool C21_nonempty();

  SparseMat K_MCK();
  SparseMat C_MCK();
  SparseMat M_MCK();
  SparseMat J_MCK();

  SparseMat K_MCKa();
  SparseMat C_MCKa();
  SparseMat J_MCKa();

  SparseMat K_MCa();
  SparseMat C_MCa();

  %new DoubleVec *rhs_MCa();
  %new DoubleVec *rhs_MCK();
  %new DoubleVec *rhs_MCKa();
  %new DoubleVec *rhs_ind_part(char);

  %new DoubleVec *static_residual_MCK();
  %new DoubleVec *static_residual_MCKa(DoubleVec*);
  %new DoubleVec *static_residual_MCa(DoubleVec*);
  %new DoubleVec *static_residual_ind_part(char);

  const DoubleVec &raw_static_residual();

  
  void initDirichletDerivatives();
  void setDirichletDerivatives(FuncNode*, Field*, int, double, double);

  void dumpMaps(char*);		      // debugging
  void dumpAll(char*, double, char*); // debugging
};

int get_globalLinSysCount();

#endif // LINEARIZEDSYSTEM_SWG
