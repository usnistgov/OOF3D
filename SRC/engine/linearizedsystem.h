// -*- C++ -*-
// $RCSfile: linearizedsystem.h,v $
// $Revision: 1.16.2.2 $
// $Author: langer $
// $Date: 2014/03/21 00:01:34 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#ifndef LINEARIZED_SYSTEM_H
#define LINEARIZED_SYSTEM_H

class CSubProblem;
class DegreeOfFreedom;
class Equation;
class Field;
class FloatBCApp;
class FuncNode;
class NodalEquation;

#include "common/doublevec.h"
#include "engine/dofmap.h"
#include "engine/sparsemat.h"
#include <vector>
#include <iostream>


// Data object to hold the matrices and vectors, which may make up the
// general linear or nonlinear time-dependent FE problem.
//
// The matrices are "K", "C", "M" and "J".
// The vectors are "residual", "body_rhs", "fix_bndy_rhs", and 
// "force_bndy_rhs".  They are defined as follows:
//
//  * The K (stiffness) matrix multiplies the degrees of
//    freedom directly.
//
//  * The C (damping) matrix is the matrix which multiplies
//    the first time derivatives of the degrees of freedom.
//
//  * The M (mass) matrix multiplies the second time derivatives.
//
//  * The J (Jacobian) matrix is used by the Newton solver to solve
//    nonlinear eqns, it is the derivative of static part w.r.t. field.
//
//  * The vector residual is the residual of the static part of the eqn.
//
//  * The vectors body_rhs, force_bndy_rhs, and fix_bndy_rhs contain
//    various contributions to the rhs.  See below for details.

class LinearizedSystem {
public:
  CSubProblem *subproblem;
private:
  // There are a bunch of indexing schemes for matrices and vectors,
  // and maps for translating between them.  The indexing schemes are:

  // mesh indexing: index of a DoF or nodal eqn in the FEMesh's dof
  // and nodaleqn vectors.

  // subproblem indexing: index of a DoF in the SubProblemContext's
  // startValues or endValues vectors.  All DoFs contained in the
  // subproblem are indexed, even if they're not solved for.  Nodal
  // eqns are indexed too, even though they're not stored explicitly
  // (because they don't have values to store), but the indices are
  // used as matrix row indices.

  // submatrix indexing: index of rows and columns in submatrices of
  // the full K, C, M, and J matrices.  Submatrices correspond to free
  // or fixed DoFs and independent or dependent nodal equations.
  

  // 1. mesh --> subproblem indices
  //       Extracts active dofs & eqns, enforces conjugacy
  // 2. subproblem --> submatrices
  //       Separates fixed and free dofs, independent equations. 
  //       Enforces FloatBCs.
  // 3. submatrix --> MCK[ad]
  //       Separates active DoFs by derivative degree
  //         M = DoFs that have second derivatives
  //         C = DoFs that couple to C, have first but not second derivatives
  //         K = DoFs that only couple to K, have no time derivatives
  //         a = Auxiliary time derivative DoFs added by some solvers
  //         d = time derivatives of all fields, in MCK order
  //       Equations are sorted similarly, by their highest time derivative.

  // Matrices stored in subproblem index order.
  SparseMat K_, C_, M_, J_;
  // The free and independent parts of the matrices.  These are
  // TODO MAP OPT: these should be SparseSubMats
  SparseMat K_indfree_, C_indfree_, M_indfree_, J_indfree_;
  SparseMat K_indfixed_, M_indfixed_, C_indfixed_;


  // Each map level operates on the output from the previous level.
  // The domain of level x is the range of level x-1.

  // Level 1 maps  *** Now stored in CSubProblem ***
  // DoFMap mesh2subpDoFMap;      // mesh dof index --> subprob dof index
  // DoFMap mesh2subpEqnMap;      // mesh eqn index --> subprob eqn index

  // Level 2 maps
  DoFMap subp2freeFieldMap;
  DoFMap subp2fixedFieldMap;
  DoFMap subp2freeDerivMap;
  DoFMap subp2indepEqnMap;
  DoFMap freeField2subpMap;
  DoFMap freeDeriv2subpMap;

  // Level 3 maps.
  // Extract submatrices for fixed DoFs and independent equations,
  // corresponding to empty and nonempty rows and columns of C and M.
  DoFMap nonEmptyMRowMap;      // nonempty row in M (meaning M_indfree!)
  DoFMap nonEmptyMColMap;      // nonempty col in M
  DoFMap nonEmptyCRowMap;      // nonempty row in C, empty in M
  DoFMap nonEmptyCColMap;      // nonempty col in C, empty in M
  DoFMap nonEmptyKRowMap;      // nonempty row in K, empty in M and C
  DoFMap nonEmptyKColMap;      // nonempty col in K, empty in M and C

  // Level-skipping maps are combinations of the above.
  DoFMap mesh2fixedFieldMap;	// used in setDirichletDerivatives
  DoFMap subp2nonEmptyMColMap;
  DoFMap subp2nonEmptyCColMap;
  DoFMap subp2nonEmptyKColMap;
  DoFMap subp2nonEmptyMRowMap;
  DoFMap subp2nonEmptyCRowMap;
  DoFMap subp2nonEmptyKRowMap;
  DoFMap subp2nonEmptyMDerivMap;
  // Level skipping and aggregating maps.
  DoFMap subp2MCKFieldMap;
  DoFMap subp2MCKEqnMap;
  DoFMap subp2MCKDerivMap;

  // Maps that only include FloatBC master dofs, used to ensure that
  // the correct dof is used when the extraction maps are many-to-one.
  DoFMap subp2freeFieldMasterMap; // level 2
  DoFMap subp2freeDerivMasterMap; // level 2
  DoFMap subp2MCKFieldMasterMap;       // level 2-3
  DoFMap subp2nonEmptyMDerivMasterMap; // level 2-3
  DoFMap subp2MCKDerivMasterMap;       // level 2-3


  // subp2nonEmptyColMap(which) returns the nonEmpty[MCK]ColMap for
  // the dofs whose maximum order derivative is which.  which must be
  // 'M', 'C', or 'K'.
  const DoFMap& subp2nonEmptyColMap(char) const;
  // Same, for nonEmpty[MCK]RowMap;
  const DoFMap &subp2nonEmptyRowMap(char) const;
  const DoFMap &indepEqn2nonEmptyRowMap(char) const;

  // Utility function used by constructor.
  // static void mapField(void *, const Field&, const Field&, bool);
  // void mapField_(const Field&, const Field&, bool);
  static void resetFFlagsWrap(void*, const Field&, const Field&, bool);
  void resetFFlags(const Field&, const Field&, bool);

  void fieldLooper(
	   void (LinearizedSystem::*)(const Field&, const Field&, bool));

  // Contributions to the rhs vector are stored in three separate
  // vectors to minimize recomputation when the properties or boundary
  // conditions change.  
  //
  //* body_rhs contains contributions from material properties (such
  //  as thermal expansion and force density (gravity)) and does not
  //  depend on boundary conditions.  The index is a subproblem eqn
  //  index.
  //
  //* force_bndy_rhs contains contributions from force and flux
  //  boundary conditions.  These don't depend on the K,C, and M
  //  matrices.  The index is a subproblem eqn index.
  //
  //* fix_bndy_rhs contains contributions from direct and floating
  //  boundary conditions.  These *do* depend on the matrices.  The
  //  index is an indpendent eqn index.
  mutable DoubleVec body_rhs, fix_bndy_rhs, force_bndy_rhs;

  // rhs_ind() returns a new'd vector in subproblem independent eqn
  // order.
  DoubleVec *rhs_ind() const;	


  // The index of the residual vector is a subproblem eqn index.
  DoubleVec residual;

  // First and second derivatives of Dirichlet boundary conditions.
  DoubleVec dirichlet1, dirichlet2;
  bool tdDirichlet;    // are there any time-dep Dirichlet conditions?

  double time_;		     // time at which everything was evaluated

  // Keep track of which dofs are fixed and which eqns are dependent.
  enum DoFState {UNSET, FREEFIELD, FIXEDFIELD, FREEDERIV, FIXEDDERIV};
  std::vector<DoFState> dofstates_;
  std::vector<bool> dependenteqns_;

public:
  LinearizedSystem(CSubProblem*, double);
  LinearizedSystem(const LinearizedSystem&);
  ~LinearizedSystem();

  double time() const { return time_; }
  void set_time(double);

  void build_submatrix_maps();
  void build_MCK_maps();
  void find_fix_bndy_rhs(const DoubleVec*);

  void clearResidual();
  void clearForceBndyRhs();
  void clearBodyRhs();
  void clearMatrices();		// K, C, M only
  void clearJacobian();

  void resetFieldFlags();
  void fixdof(const DegreeOfFreedom*);
  void fixeqn(const NodalEquation*);
  bool is_fixed(const DegreeOfFreedom*) const;
  
  // get_unknowns_xxx() returns a new'd vector containing the current
  // values of the unknowns, copied out of the argument, which is a
  // list of dof values in subproblem index order.  MCK returns just
  // the Field values, in MCK order.  MCKa returns the field values
  // and the auxiliary variables.  MCKd returns the field values
  // followed by the time derivative values, all in MCK order.  These
  // methods are called via dispatch methods in the timesteppers,
  // which determine the desired dof order.
  DoubleVec *get_unknowns_MCK(const DoubleVec*) const;
  DoubleVec *get_unknowns_MCKa(const DoubleVec*) const;
  DoubleVec *get_unknowns_MCKd(const DoubleVec*) const;
  // Set the current values of the unknowns by mapping the first arg
  // into a new'd copy of the second and returning the result.  The
  // second must be a dof list in subproblem index order.
  // TODO MAP OPT: Can we get rid of the copy?  Just copy into the
  // given vector, with no return value?
  DoubleVec *set_unknowns_MCK(const DoubleVec*, const DoubleVec*) const;
  DoubleVec *set_unknowns_MCKa(const DoubleVec*, const DoubleVec*) const;
  DoubleVec *set_unknowns_MCKd(const DoubleVec*, const DoubleVec*) const;
  
  // get_unknowns_part() extracts the M, C, or K part of a vector of
  // unknowns, such as that returned by get_unknowns_XXX(), above. 
  DoubleVec *get_unknowns_part(char, const DoubleVec*) const;
  // set_unknowns_part() copies a given vector containing the M, C, or
  // K part of the unknowns into the right location in a given full
  // vector of unknowns.
  void set_unknowns_part(char, const DoubleVec*, DoubleVec*) const;

  // get and set the first time derivatives that may be stored in the
  // unknowns vector.  There are no derivatives stored in MCK format,
  // so there are only MCKa and MCKd variants of these functions.
  DoubleVec *get_derivs_MCKd(const DoubleVec*) const;
  DoubleVec *get_derivs_part_MCKa(char, const DoubleVec*) const;
  DoubleVec *get_derivs_part_MCKd(char, const DoubleVec*) const;
  void set_derivs_MCKd(const DoubleVec*, DoubleVec*) const;
  void set_derivs_part_MCKa(char, const DoubleVec*, DoubleVec*) const;
  void set_derivs_part_MCKd(char, const DoubleVec*, DoubleVec*) const;

  // For MCKd, we sometimes need not the full set of unknowns (which
  // includes derivatives) but just the non-derivative part.  [This
  // could be done less efficiently with three calls to
  // get_unknowns_part_MCKd().]
  DoubleVec *get_fields_MCKd(const DoubleVec*) const;
  void set_fields_MCKd(const DoubleVec*, DoubleVec*) const;

  // Routines for handling DoF vectors in ForwardEuler and RK, which
  // have to handle the static equations and DoFs separately.
  DoubleVec *extract_MCa_dofs(const DoubleVec*) const;
  void inject_MCa_dofs(const DoubleVec*, DoubleVec*) const;
  void expand_MCa_dofs(DoubleVec*) const;

  unsigned int n_unknowns_part(char) const;
  // unsigned int n_derivs_part(char) const;
  unsigned int n_unknowns_MCK() const;
  unsigned int n_unknowns_MCKa() const;
  unsigned int n_unknowns_MCKd() const;

  void consolidate();

  void insertK(int, int, double);
  void insertC(int, int, double);
  void insertM(int, int, double);
  void insertJ(int, int, double);


  // TODO MAP OPT: These should return SparseSubMats.
  // Versions of K_indfree, etc, with rows and columns in MCK order.
  SparseMat K_MCK() const;
  SparseMat C_MCK() const;
  SparseMat M_MCK() const;
  SparseMat J_MCK() const;
  // Combinations of M, C, and K used for solving 2nd order equations
  // as pairs of first order equations.
  SparseMat K_MCKa() const;
  SparseMat C_MCKa() const;
  SparseMat J_MCKa() const;
  // Verions of MCKa that don't include the K part, for use with
  // Forward Euler.
  SparseMat K_MCa() const;
  SparseMat C_MCa() const;

  // Submatrices of K_indfree, etc.  The args are the derivative
  // orders.
  SparseMat K_submatrix(char, char) const;
  SparseMat C_submatrix(char, char) const;
  SparseMat M_submatrix(char, char) const;
  SparseMat J_submatrix(char, char) const;

  bool C21_nonempty() const;

  void insert_body_rhs(int row, double val);
  void insert_force_bndy_rhs(int row, double val);
  void insert_static_residual(int row, double val);

  // Assign values to the first and second time derivatives of
  // Dirichlet boundary conditions.  
  void initDirichletDerivatives();
  void setDirichletDerivatives(const FuncNode*, const Field*, int,
			       double, double);

  // Return the rhs for the independent equations.  All of these
  // return a new vector.
  DoubleVec *rhs_MCK() const;
  DoubleVec *rhs_MCKa() const;
  DoubleVec *rhs_MCa() const;
  DoubleVec *rhs_ind_part(char) const; // just M, C, or K part

  // Return the static part of the residual vector.  All of these
  // return a new vector.
  DoubleVec *static_residual_MCK() const;
  DoubleVec *static_residual_MCKa(const DoubleVec*) const;
  DoubleVec *static_residual_MCa(const DoubleVec*) const;
  DoubleVec *static_residual_ind_part(char) const;

  DoubleVec *error_estimation_dofs_MCKd(const DoubleVec*) const;

  // FloatBC support functions.
  int getSubproblemDoFIndex(const FuncNode*, const Field*, int) const;
  int getSubproblemEqnIndex(const FuncNode*, const Equation*, int) const;
  void profile_rhs(const FloatBCApp&);
  void applyFloatBC(int, int, int, int, int, int);
  void cleanmaps();

  //=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

  // Debugging routines

public:
  const DoubleVec &raw_static_residual() const; // for debugging

  void dumpMaps(const std::string&) const;
  void dumpAll(const std::string &filename, double time,
	       const std::string &comment) const;
private:
  void do_dumpMaps(std::ostream&) const;
};

int get_globalLinSysCount();

#endif // LINEARIZED_SYSTEM_H
