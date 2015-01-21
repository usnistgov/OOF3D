// -*- C++ -*-
// $RCSfile: linearizedsystem.C,v $
// $Revision: 1.28.2.10 $
// $Author: langer $
// $Date: 2014/11/05 16:54:25 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>
#include <iostream>
#include <fstream>
#include <string.h>		// for memcpy, memset, and memmove
#include <vector>

#include "common/lock.h"
#include "common/ooferror.h"
#include "common/printvec.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "common/vectormath.h"
#include "common/IO/oofcerr.h"
#include "engine/boundarycond.h"
#include "engine/csubproblem.h"
#include "engine/femesh.h"
#include "engine/freedom.h"
#include "engine/linearizedsystem.h"
#include "engine/meshiterator.h"
#include "engine/nodalequation.h"
#include "engine/pointdata.h"
#include "engine/node.h"
#include "engine/sparsemat.h"

// TODO OPT: Use timestamps on insertK(), etc. and recompute rhs,
// matrices only when out of date.

// Count LinearizedSystem objects so that the tests can check for
// leftovers.

static int nlinsys = 0;
static SLock countLock;

LinearizedSystem::LinearizedSystem(CSubProblem *subp, double time)
  : subproblem( subp ),
    tdDirichlet(false),
    time_(time)
{
  countLock.acquire();
  ++nlinsys;
  countLock.release();
  dofstates_.clear();
  dofstates_.resize(subproblem->ndof(), UNSET);
  resetFieldFlags();
}

LinearizedSystem::~LinearizedSystem() {
  countLock.acquire();
  --nlinsys;
  countLock.release();
}

int get_globalLinSysCount() {
  return nlinsys;
}

LinearizedSystem::LinearizedSystem(const LinearizedSystem &other)
  : subproblem(other.subproblem),

    subp2freeFieldMap(other.subp2freeFieldMap),
    subp2fixedFieldMap(other.subp2fixedFieldMap),
    subp2freeDerivMap(other.subp2freeDerivMap),
    subp2indepEqnMap(other.subp2indepEqnMap),
    freeField2subpMap(other.freeField2subpMap),
    freeDeriv2subpMap(other.freeDeriv2subpMap),

    nonEmptyMRowMap(other.nonEmptyMRowMap),
    nonEmptyMColMap(other.nonEmptyMColMap),
    nonEmptyCRowMap(other.nonEmptyCRowMap),
    nonEmptyCColMap(other.nonEmptyCColMap),
    nonEmptyKRowMap(other.nonEmptyKRowMap),
    nonEmptyKColMap(other.nonEmptyKColMap),

    mesh2fixedFieldMap(other.mesh2fixedFieldMap),
    subp2nonEmptyMColMap(other.subp2nonEmptyMColMap),
    subp2nonEmptyCColMap(other.subp2nonEmptyCColMap),
    subp2nonEmptyKColMap(other.subp2nonEmptyKColMap),
    subp2nonEmptyMRowMap(other.subp2nonEmptyMRowMap),
    subp2nonEmptyCRowMap(other.subp2nonEmptyCRowMap),
    subp2nonEmptyKRowMap(other.subp2nonEmptyKRowMap),
    subp2nonEmptyMDerivMap(other.subp2nonEmptyMDerivMap),

    subp2MCKFieldMap(other.subp2MCKFieldMap),
    subp2MCKEqnMap(other.subp2MCKEqnMap),
    subp2MCKDerivMap(other.subp2MCKDerivMap),

    subp2freeFieldMasterMap(other.subp2freeFieldMasterMap),
    subp2freeDerivMasterMap(other.subp2freeDerivMasterMap),
    subp2MCKFieldMasterMap(other.subp2MCKFieldMasterMap),
    subp2nonEmptyMDerivMasterMap(other.subp2nonEmptyMDerivMasterMap),
    subp2MCKDerivMasterMap(other.subp2MCKDerivMasterMap),

    body_rhs(other.body_rhs),
    fix_bndy_rhs(other.fix_bndy_rhs),
    force_bndy_rhs(other.force_bndy_rhs),
    residual(other.residual),

    dirichlet1(other.dirichlet1),
    dirichlet2(other.dirichlet2),
    tdDirichlet(other.tdDirichlet),

    time_(other.time_),

    dofstates_(other.dofstates_),
    dependenteqns_(other.dependenteqns_)
{
  countLock.acquire();
  ++nlinsys;
  countLock.release();

  // TODO OPT: TDEP The cost of the LinearizedSystem clone can be
  // reduced if SparseMats have copy-on-write semantics.  Then the
  // matrices here don't have to be cloned.  Be careful!  There may be
  // situations in which copy-on-write is incorrect.  If that's the
  // case, we'll need to somehow indicate which clones should use
  // copy-on-write and which shouldn't.
  K_ = other.K_.clone();
  C_ = other.C_.clone();
  M_ = other.M_.clone();
  J_ = other.J_.clone();
  K_indfree_ = other.K_indfree_.clone();
  C_indfree_ = other.C_indfree_.clone();
  M_indfree_ = other.M_indfree_.clone();
  J_indfree_ = other.J_indfree_.clone();
  K_indfixed_ = other.K_indfixed_.clone();
  C_indfixed_ = other.C_indfixed_.clone();
  M_indfixed_ = other.M_indfixed_.clone();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void LinearizedSystem::set_time(double t) {
  time_ = t;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// fieldLooper() applies the given function to all Fields defined on
// the Subproblem. 

void LinearizedSystem::fieldLooper(
	   void (LinearizedSystem::*fn)(const Field&, const Field&, bool))
{
  // Loop over CompoundFields
  const std::vector<CompoundField*> *fields = subproblem->all_compound_fields();
  for(unsigned int f=0; f<fields->size(); ++f) {
    CompoundField *field = (*fields)[f];
    Field *tdfield = field->time_derivative();
    bool tddefined = subproblem->is_defined_field(*tdfield);
    if(subproblem->is_defined_field(*field)) {
      (this->*fn)(*field, *tdfield, tddefined);
#if DIM==2
      Field *zfield = field->out_of_plane();
      Field *tdzfield = field->out_of_plane_time_derivative();
      (this->*fn)(*zfield, *tdzfield, tddefined);
#endif // DIM==2
    }
  }
  delete fields;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// resetFieldFlags resets the dofstates_ array.  It's called when a
// LinearizedSystem is constructed, and before the fixed bcs are
// invoked.

void LinearizedSystem::resetFieldFlags() {
  dofstates_.clear();
  dofstates_.resize(subproblem->ndof(), UNSET);
  subproblem->fieldLooper(&LinearizedSystem::resetFFlagsWrap, this);
  dependenteqns_.clear();
  dependenteqns_.resize(subproblem->mesh2subpEqnMap.range(), false);
}

void LinearizedSystem::resetFFlagsWrap(void *data, const Field &field,
				   const Field &tdfield,
				   bool tddefined) 
{
  ((LinearizedSystem*)data)->resetFFlags(field, tdfield, tddefined);
}

void LinearizedSystem::resetFFlags(const Field &field, const Field &tdfield,
				   bool tddefined)
{
  // Inactive Fields are marked as fixed here.  Active ones may be
  // fixed later at particular nodes by boundary conditions.
  bool active = subproblem->is_active_field(field);
  DoFState fieldstate = active? FREEFIELD : FIXEDFIELD;
  DoFState derivstate = active? FREEDERIV : FIXEDDERIV;
  for(FuncNodeIterator nd=subproblem->funcnode_iterator(); !nd.end(); ++nd) {
    FuncNode *node = nd.node();
    for(int i=0; i<field.ndof(); i++) {
      int dofindex = subproblem->mesh2subpDoFMap[field(node,i)->dofindex()];
      dofstates_[dofindex] = fieldstate;
      if(tddefined) {
	dofstates_[subproblem->dof2Deriv[dofindex]] = derivstate;
      }
    }
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void LinearizedSystem::clearForceBndyRhs() {
  force_bndy_rhs.clear();
  force_bndy_rhs.resize(subproblem->mesh2subpEqnMap.range(), 0.0);
}

void LinearizedSystem::clearBodyRhs() {
  body_rhs.clear();
  body_rhs.resize(subproblem->mesh2subpEqnMap.range(), 0.0);
}

void LinearizedSystem::clearResidual() {
  residual.clear();
  residual.resize(subproblem->mesh2subpEqnMap.range(), 0.0);
}

void LinearizedSystem::clearMatrices() {
  K_ = SparseMat();
  C_ = SparseMat();
  M_ = SparseMat();
}

void LinearizedSystem::clearJacobian() {
  J_ = SparseMat();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Routines for constructing the matrices and rhs.

// insert[KCMJ] inserts a value into a subproblem-scope matrix, given
// the global indices of the row (equation) and column (dof).  It
// *adds* to existing matrix elements.

// TODO OPT: Mark empty*Maps as out-of-date.

void LinearizedSystem::insertK(int row, int col, double x) {
  int i = subproblem->mesh2subpEqnMap[row];
  int j = subproblem->mesh2subpDoFMap[col];
  assert(i > -1 && j > -1);
  K_.insert(i, j, x);
}

void LinearizedSystem::insertC(int row, int col, double x) {
  int i = subproblem->mesh2subpEqnMap[row];
  int j = subproblem->mesh2subpDoFMap[col];
  assert(i > -1 && j > -1);
  C_.insert(i, j, x);
}

void LinearizedSystem::insertM(int row, int col, double x) {
  int i = subproblem->mesh2subpEqnMap[row];
  int j = subproblem->mesh2subpDoFMap[col];
  assert(i > -1 && j > -1);
  M_.insert(i, j, x);
}

void LinearizedSystem::insertJ(int row, int col, double x) {
  J_.insert(subproblem->mesh2subpEqnMap[row], subproblem->mesh2subpDoFMap[col], x);
}

void LinearizedSystem::consolidate() {
  // Called by CSubproblem::make_linear_system after matrices are
  // built.
  M_.consolidate();
  C_.consolidate();
  J_.consolidate();
  K_.consolidate();
}

void LinearizedSystem::insert_force_bndy_rhs(int row, double val) {
  assert(subproblem->mesh2subpEqnMap[row] != -1);
  force_bndy_rhs[subproblem->mesh2subpEqnMap[row]] += val;
}

void LinearizedSystem::insert_body_rhs(int row, double val) {
  assert(subproblem->mesh2subpEqnMap[row] != -1);
  body_rhs[subproblem->mesh2subpEqnMap[row]] += val;
}

void LinearizedSystem::insert_static_residual(int row, double val) {
  assert(subproblem->mesh2subpEqnMap[row] != -1);
  residual[subproblem->mesh2subpEqnMap[row]] += val;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void LinearizedSystem::fixdof(const DegreeOfFreedom *dof) {
  // TODO OPT: Mark maps as out-of-date.
  int fldindex = subproblem->mesh2subpDoFMap[dof->dofindex()];
  dofstates_[fldindex] = FIXEDFIELD;
  int derivindex = subproblem->getDerivIndex(fldindex);
  if(derivindex > -1)
    dofstates_[derivindex] = FIXEDDERIV;
}

bool LinearizedSystem::is_fixed(const DegreeOfFreedom *dof) const {
  int fldindex = subproblem->mesh2subpDoFMap[dof->dofindex()];
  return dofstates_[fldindex] == FIXEDFIELD;
}

void LinearizedSystem::fixeqn(const NodalEquation *eqn) {
  // TODO OPT: Mark maps as out-of-date.
  dependenteqns_[subproblem->mesh2subpEqnMap[eqn->ndq_index()]] = true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// See linearizedsystem.h for explanation of map levels.
// build_submatrix_maps() is called only *after* the main matrices
// have been built and Dirichlet boundary conditions have been
// applied.  It builds the maps that will be modified by FloatBCs.
// Maps that depend on the modified maps are built later by
// build_MCK_maps().

void LinearizedSystem::build_submatrix_maps() {
  int ndof = subproblem->mesh2subpDoFMap.range();
  int neqn = subproblem->mesh2subpEqnMap.range();

  subp2freeFieldMap.reset(ndof);
  subp2fixedFieldMap.reset(ndof);
  subp2freeDerivMap.reset(ndof);
  subp2indepEqnMap.reset(neqn);

  subp2freeFieldMasterMap.reset(ndof);
  subp2freeDerivMasterMap.reset(ndof);

  for(int i=0; i<ndof; i++) {
    DoFState s = dofstates_[i];
    if(s == FREEFIELD) {     // dof i is a free field (not derivative)
      subp2freeFieldMap.add(i);
    }
    else if(s == FIXEDFIELD) {	// dof i is a fixed field
      subp2fixedFieldMap.add(i);
    }
    else if(s == FREEDERIV) {	// dof i is a free derivative
      subp2freeDerivMap.add(i);
    }
  }
  for(int i=0; i<neqn; i++) {
    if(!dependenteqns_[i]) {	// eqn i is independent
      subp2indepEqnMap.add(i);
    }
  }

  // freeField2subpMap and freeDeriv2subpMap are used when applying
  // FloatBCs.
  freeField2subpMap = subp2freeFieldMap.inverse();
  freeDeriv2subpMap = subp2freeDerivMap.inverse();
}

void LinearizedSystem::build_MCK_maps() {
  mesh2fixedFieldMap = compose(subproblem->mesh2subpDoFMap, subp2fixedFieldMap);

  // Construct the actual matrices so that we can build the level 3
  // maps which extract submatrices of [KCM]_indfree.

  // TODO OPT: These should be SparseSubMats.

  // TODO OPT: We wouldn't need these matrices to be constructed
  // explicitly if we had a way of computing the empty[MCK]Maps
  // directly from the other maps and K_, C_, and M_.  (Is this
  // comment out of date?  We have nonEmpty maps, not empty maps.)
  K_indfree_ = SparseMat(K_, subp2indepEqnMap, subp2freeFieldMap);
  C_indfree_ = SparseMat(C_, subp2indepEqnMap, subp2freeFieldMap);
  M_indfree_ = SparseMat(M_, subp2indepEqnMap, subp2freeFieldMap);
  J_indfree_ = SparseMat(J_, subp2indepEqnMap, subp2freeFieldMap);

  K_indfixed_ = SparseMat(K_, subp2indepEqnMap, subp2fixedFieldMap);
  C_indfixed_ = SparseMat(C_, subp2indepEqnMap, subp2fixedFieldMap);
  M_indfixed_ = SparseMat(M_, subp2indepEqnMap, subp2fixedFieldMap);

  // These maps extract subsets of the independent eqns and free DoFs,
  // corresponding to the empty and nonempty rows of M, C, and K.
  nonEmptyMRowMap.reset(subp2indepEqnMap.range());
  nonEmptyCRowMap.reset(subp2indepEqnMap.range());
  nonEmptyKRowMap.reset(subp2indepEqnMap.range());
  nonEmptyMColMap.reset(subp2freeFieldMap.range());
  nonEmptyCColMap.reset(subp2freeFieldMap.range());
  nonEmptyKColMap.reset(subp2freeFieldMap.range());

  for(unsigned int i=0; i<subp2freeFieldMap.range(); i++) {
    if(M_indfree_.is_nonempty_col(i)) {
      nonEmptyMColMap.add(i);	// M col is nonempty
    }
    else {
      if(C_indfree_.is_nonempty_col(i))
	nonEmptyCColMap.add(i);	// M col is empty, C col is nonempty
      else {
	if(K_indfree_.is_nonempty_col(i))
	  nonEmptyKColMap.add(i); // M and C cols are empty, K col is nonempty
      }
    }
  }

  for(unsigned int i=0; i<subp2indepEqnMap.range(); i++) {
    if(M_indfree_.is_nonempty_row(i)) {
      nonEmptyMRowMap.add(i);
    }
    else {			// M row is empty
      if(C_indfree_.is_nonempty_row(i))
	nonEmptyCRowMap.add(i);
      else {			// C row is empty
	if(K_indfree_.is_nonempty_row(i))
	  nonEmptyKRowMap.add(i);
      }	// end C row is empty
    }	// end M row is empty
  }	// end loop over independent equations

  subp2nonEmptyMColMap = compose(subp2freeFieldMap, nonEmptyMColMap);
  subp2nonEmptyCColMap = compose(subp2freeFieldMap, nonEmptyCColMap);
  subp2nonEmptyKColMap = compose(subp2freeFieldMap, nonEmptyKColMap);

  subp2nonEmptyMRowMap = compose(subp2indepEqnMap, nonEmptyMRowMap);
  subp2nonEmptyCRowMap = compose(subp2indepEqnMap, nonEmptyCRowMap);
  subp2nonEmptyKRowMap = compose(subp2indepEqnMap, nonEmptyKRowMap);

  subp2MCKFieldMap = concat(subp2nonEmptyMColMap,
			  concat(subp2nonEmptyCColMap, subp2nonEmptyKColMap));
  subp2MCKEqnMap = concat(subp2nonEmptyMRowMap,
			  concat(subp2nonEmptyCRowMap, subp2nonEmptyKRowMap));

  DoFMap tempM = compose(subp2freeFieldMasterMap, nonEmptyMColMap);
  DoFMap tempC = compose(subp2freeFieldMasterMap, nonEmptyCColMap);
  DoFMap tempK = compose(subp2freeFieldMasterMap, nonEmptyKColMap);
  subp2MCKFieldMasterMap = concat(tempM, concat(tempC, tempK));

  if(!subproblem->dof2Deriv.empty()) {
    subp2nonEmptyMDerivMap = subp2nonEmptyMColMap.translateDomain(
			subp2freeFieldMap.domain(), subproblem->dof2Deriv);
    subp2nonEmptyMDerivMasterMap = tempM.translateDomain(
			subp2freeFieldMap.domain(), subproblem->dof2Deriv);
    subp2MCKDerivMap = subp2MCKFieldMap.translateDomain(
			subp2freeFieldMap.domain(), subproblem->dof2Deriv);
    subp2MCKDerivMasterMap = subp2MCKFieldMasterMap.translateDomain(
			subp2freeFieldMap.domain(), subproblem->dof2Deriv);
  }

  // static bool once = false;
  // if(not once) {
  //   once = true;
  //   dumpMaps();
  // }
} // end build_MCK_maps

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void LinearizedSystem::dumpMaps(const std::string &filename) const {
  if(filename.size() > 0) {
    ofstream os(filename.c_str());
    do_dumpMaps(os);
    os.close();
  }
  else
    do_dumpMaps(std::cerr);
}

void LinearizedSystem::do_dumpMaps(ostream &os) const {
  os << "LinearizedSystem::dumpMaps -----------" << std::endl;
  os << "      mesh2subpDoFMap=" << subproblem->mesh2subpDoFMap << std::endl;
  os << "      mesh2subpEqnMap=" << subproblem->mesh2subpEqnMap << std::endl;
  os << std::endl;
  os << "   subp2freeFieldMap=" << subp2freeFieldMap << std::endl;
  os << "  subp2fixedFieldMap=" << subp2fixedFieldMap << std::endl;
  os << "    subp2indepEqnMap=" << subp2indepEqnMap << std::endl;
  os << "  mesh2fixedFieldMap=" << mesh2fixedFieldMap << std::endl;
  os << std::endl;
  os << "  nonEmptyMRowMap=" << nonEmptyMRowMap << std::endl;
  os << "  nonEmptyCRowMap=" << nonEmptyCRowMap << std::endl;
  os << "  nonEmptyKRowMap=" << nonEmptyKRowMap << std::endl;
  os << "  nonEmptyMColMap=" << nonEmptyMColMap << std::endl;
  os << "  nonEmptyCColMap=" << nonEmptyCColMap << std::endl;
  os << "  nonEmptyKColMap=" << nonEmptyKColMap << std::endl;
  os << std::endl;
  os << "  subp2nonEmptyMRowMap=" << subp2nonEmptyMRowMap << std::endl;
  os << "  subp2nonEmptyCRowMap=" << subp2nonEmptyCRowMap << std::endl;
  os << "  subp2nonEmptyKRowMap=" << subp2nonEmptyKRowMap << std::endl;
  os << "  subp2nonEmptyMColMap=" << subp2nonEmptyMColMap << std::endl;
  os << "  subp2nonEmptyCColMap=" << subp2nonEmptyCColMap << std::endl;
  os << "  subp2nonEmptyKColMap=" << subp2nonEmptyKColMap << std::endl;
  os << "      subp2MCKFieldMap=" << subp2MCKFieldMap << std::endl;
  os << "        subp2MCKEqnMap=" << subp2MCKEqnMap << std::endl;
  os << std::endl;
  os << "  subp2nonEmptyMDerivMap=" << subp2nonEmptyMDerivMap<<std::endl;
  os << "        subp2MCKDerivMap=" << subp2MCKDerivMap << std::endl;

  os << "      subp2freeFieldMasterMap=" << subp2freeFieldMasterMap
	    << std::endl;
  os << "      subp2freeDerivMasterMap=" << subp2freeDerivMasterMap
	    << std::endl;
  os << "       subp2MCKFieldMasterMap=" << subp2MCKFieldMasterMap
	    << std::endl;
  os << " subp2nonEmptyMDerivMasterMap=" << subp2nonEmptyMDerivMasterMap
	    << std::endl;
  os << "       subp2MCKDerivMasterMap=" << subp2MCKDerivMasterMap
	    << std::endl;
  os << "LinearizedSystem::dumpMaps: done -----" << std::endl;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// get_unknowns_MCK() and set_unknowns_MCK() are called by steppers to
// get the current values of the unknowns and to set the solved
// values.  The *MCKa versions include auxiliary variables and are
// used by first order steppers when solving second order equations.
// The MCKd versions include all first derivative fields and are used
// by second order steppers.

DoubleVec *LinearizedSystem::get_unknowns_MCK(const DoubleVec *source) const {
  DoubleVec *unknowns = subp2MCKFieldMap.extract(*source);
  subp2MCKFieldMasterMap.extract(*source, *unknowns, 0);
  return unknowns;
}

DoubleVec *LinearizedSystem::get_unknowns_MCKa(const DoubleVec *source) const {
  int n2 = subp2nonEmptyMDerivMap.range();
  int n = subp2MCKFieldMap.range();
  DoubleVec *unknowns = new DoubleVec(n+n2);
  subp2MCKFieldMap.extract(*source, *unknowns, 0);
  subp2MCKFieldMasterMap.extract(*source, *unknowns, 0);
  subp2nonEmptyMDerivMap.extract(*source, *unknowns, n);
  subp2nonEmptyMDerivMasterMap.extract(*source, *unknowns, n);
  return unknowns;
}

DoubleVec *LinearizedSystem::get_unknowns_MCKd(const DoubleVec *source) const {
  int n = subp2MCKFieldMap.range();
  DoubleVec *unknowns = new DoubleVec(2*n);
  subp2MCKFieldMap.extract(*source, *unknowns, 0);
  subp2MCKFieldMasterMap.extract(*source, *unknowns, 0);
  subp2MCKDerivMap.extract(*source, *unknowns, n);
  subp2MCKDerivMasterMap.extract(*source, *unknowns, n);
  return unknowns;
}

DoubleVec *LinearizedSystem::error_estimation_dofs_MCKd(
						const DoubleVec *unknowns)
  const
{
  // Second order fields use field and deriv value for error
  // estimation.  Zero and first order fields use just the field
  // value, even if the stepper is second order.
  unsigned int n2 = nonEmptyMColMap.range();
  unsigned int n1 = nonEmptyCColMap.range();
  unsigned int n0 = nonEmptyKColMap.range();
  unsigned int n = n2+n1+n0;
  DoubleVec *dofs = new DoubleVec(2*n2 + n1 + n0);
  (void) memcpy(&(*dofs)[0], &(*unknowns)[0], n*sizeof(double));
  (void) memcpy(&(*dofs)[n], &(*unknowns)[n], n2*sizeof(double));
  return dofs;
}

// These routines set_unknowns_MCK*() copy values from src into a copy
// of dest, which they return.

DoubleVec *LinearizedSystem::set_unknowns_MCK(const DoubleVec *src,
					      const DoubleVec *dest)
  const
{
  DoubleVec *result = new DoubleVec(*dest);
  subp2MCKFieldMap.inject(*src, *result);
  return result;
}

DoubleVec *LinearizedSystem::set_unknowns_MCKa(const DoubleVec *src,
					       const DoubleVec *dest)
  const
{
  int n = subp2MCKFieldMap.range();
  DoubleVec *result = new DoubleVec(*dest);
  subp2MCKFieldMap.inject(*src, 0, *result);
  subp2nonEmptyMDerivMap.inject(*src, n, *result);
  return result;
}

DoubleVec *LinearizedSystem::set_unknowns_MCKd(const DoubleVec *src,
					       const DoubleVec *dest)
  const
{
  int n = subp2MCKFieldMap.range();
  DoubleVec *result = new DoubleVec(*dest);
  subp2MCKFieldMap.inject(*src, 0, *result);
  subp2MCKDerivMap.inject(*src, n, *result);
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// get_unknowns_part and set_unknowns_part extract and set the M, C,
// or K parts of the unknowns vector (such as returned by
// get_unknowns_XXX).  Since get_unknowns_XXX returns values in MCK
// order, these functions just operate on contiguous subsets of their
// inputs, and don't need to use maps, except to find out how large
// the M, C, and K blocks are.  *** This assumes that all of the
// schemes for creating the unknowns vector (get_unknowns_MCK(), etc.)
// store the M, C, and K parts in the same way. ***

DoubleVec *LinearizedSystem::get_unknowns_part(
			     char which, const DoubleVec *src) const
{
  if(which == 'M') {
    unsigned int n2 = n_unknowns_part('M');
    return new DoubleVec(src->begin(), src->begin()+n2);
  }
  else if(which == 'C') {
    unsigned int n2 = n_unknowns_part('M');
    unsigned int n1 = n_unknowns_part('C');
    return new DoubleVec(src->begin()+n2, src->begin()+n2+n1);
  }
  else if(which == 'K') {
    unsigned int n2 = n_unknowns_part('M');
    unsigned int n1 = n_unknowns_part('C');
    unsigned int n0 = n_unknowns_part('K');
    return new DoubleVec(src->begin()+n2+n1, src->begin()+n2+n1+n0);
  }
  throw ErrProgrammingError("Bad map requested in get_unknowns_part",
			    __FILE__, __LINE__);
}

void LinearizedSystem::set_unknowns_part(
			 char which, const DoubleVec *vals, DoubleVec *dest)
  const
{
  if(which == 'M') {
    unsigned int n2 = n_unknowns_part('M');
    assert(vals->size() == n2);
    assert(dest->size() >= n2);
    memcpy(&(*dest)[0], &(*vals)[0], n2*sizeof(double));
  }
  else if(which == 'C') {
    unsigned int n2 = n_unknowns_part('M');
    unsigned int n1 = n_unknowns_part('C');
    assert(vals->size() == n1);
    assert(dest->size() >= n1+n2);
    memcpy(&(*dest)[n2], &(*vals)[0], n1*sizeof(double));
  }
  else if(which == 'K') {
    unsigned int n2 = n_unknowns_part('M');
    unsigned int n1 = n_unknowns_part('C');
    unsigned int n0 = n_unknowns_part('K');
    assert(vals->size() == n0);
    assert(dest->size() >= n2+n1+n0);
    memcpy(&(*dest)[n2+n1], &(*vals)[0], n0*sizeof(double));
  }
  else
    throw ErrProgrammingError("Bad map requested in set_unknowns_part",
			      __FILE__, __LINE__);
}

unsigned int LinearizedSystem::n_unknowns_part(char which) const {
  return subp2nonEmptyColMap(which).range();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


DoubleVec *LinearizedSystem::get_derivs_MCKd(const DoubleVec *src) const {
  unsigned int n = subp2MCKFieldMap.range();
  return new DoubleVec(src->begin()+n, src->end());
}

DoubleVec *LinearizedSystem::get_fields_MCKd(const DoubleVec *src) const {
  unsigned int n = subp2MCKFieldMap.range();
  return new DoubleVec(src->begin(), src->begin()+n);
}

void LinearizedSystem::set_fields_MCKd(const DoubleVec *src, DoubleVec *dest)
  const
{
  unsigned int n = subp2MCKFieldMap.range();
  assert(dest->size() >= n);
  assert(src->size() >= n);
  (void) memcpy(&(*dest)[0], &(*src)[0], n*sizeof(double));
}

void LinearizedSystem::set_derivs_MCKd(const DoubleVec *src, DoubleVec *dest)
  const
{
  unsigned int n = subp2MCKFieldMap.range();
  assert(dest->size()>=2*n);
  assert(src->size()>=n);
  (void) memcpy(&(*dest)[n], &(*src)[0], n*sizeof(double));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

DoubleVec *LinearizedSystem::get_derivs_part_MCKa(char which,
						  const DoubleVec *src)
  const
{
  assert(which == 'M');
  unsigned int n2 = n_unknowns_part('M');
  unsigned int n1 = n_unknowns_part('C');
  unsigned int n0 = n_unknowns_part('K');
  return new DoubleVec(src->begin()+n2+n1+n0, src->end());
}

DoubleVec *LinearizedSystem::get_derivs_part_MCKd(char which,
						  const DoubleVec *src) const
{
  unsigned int n2 = n_unknowns_part('M');
  unsigned int n1 = n_unknowns_part('C');
  unsigned int n0 = n_unknowns_part('K');
  if(which == 'M')
    return new DoubleVec(src->begin()+n2+n1+n0, src->begin()+2*n2+n1+n0);
  else if(which == 'C')
    return new DoubleVec(src->begin()+2*n2+n1+n0, src->begin()+2*n2+2*n1+n0);
  else if(which == 'K')
    return new DoubleVec(src->begin()+2*n2+2*n1+n0, src->end());
  throw ErrProgrammingError("Bad map requested in get_derivs_part_MCKd",
			    __FILE__, __LINE__);
}

void LinearizedSystem::set_derivs_part_MCKa(char which, const DoubleVec *src,
					    DoubleVec *dest)
  const
{
  assert(which == 'M');
  unsigned int n2 = n_unknowns_part('M');
  unsigned int n1 = n_unknowns_part('C');
  unsigned int n0 = n_unknowns_part('K');
  assert(dest->size() >= 2*n2+n1+n0);
  assert(src->size() >= n2);
  (void) memcpy(&(*dest)[n2+n1+n0], &(*src)[0], n2*sizeof(double));
}

void LinearizedSystem::set_derivs_part_MCKd(char which, const DoubleVec *src,
					    DoubleVec *dest)
  const
{
  unsigned int n2 = n_unknowns_part('M');
  unsigned int n1 = n_unknowns_part('C');
  unsigned int n0 = n_unknowns_part('K');
  if(which == 'M') {
    assert(dest->size() >= 2*n2+n1+n0);
    assert(src->size() >= n2);
    (void) memcpy(&(*dest)[n2+n1+n0], &(*src)[0], n2*sizeof(double));
  }
  else if(which == 'C') {
    assert(dest->size() >= 2*n2+2*n1+n0);
    assert(src->size() >= n1);
    (void) memcpy(&(*dest)[2*n2+n1+n0], &(*src)[0], n1*sizeof(double));
  }
  else if(which == 'K') {
    assert(dest->size() >= 2*(n2+n1+n0));
    assert(src->size() >= n0);
    (void) memcpy(&(*dest)[2*n2+2*n1+n0], &(*src)[0], n0*sizeof(double));
  }
  else
    throw ErrProgrammingError("Bad map requested in set_derivs_part_MCKd",
			      __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

unsigned int LinearizedSystem::n_unknowns_MCK() const {
  return subp2MCKFieldMap.range();
}

unsigned int LinearizedSystem::n_unknowns_MCKa() const {
  return subp2MCKFieldMap.range() + nonEmptyMColMap.range();
}

unsigned int LinearizedSystem::n_unknowns_MCKd() const {
  return 2*subp2MCKFieldMap.range();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Routines for handling DoF vectors in ForwardEuler and RK, which
// have to handle the static equations and DoFs separately.

// Given a vector of DoFs in MCKa order, extract the MCa parts.

// TODO OPT: If ForwardEuler and RK used MCaK order instead of MCKa
// order, using just the MCa part would be simpler, and we could
// probably avoid some copies, especially if we had a DoubleSubVec
// class that provided a view into an existing DoubleVec.

DoubleVec *LinearizedSystem::extract_MCa_dofs(const DoubleVec *v) const {
  // v is already in MCKa order, but we want just the MCa part of it.
  unsigned int n2 = nonEmptyMColMap.range();
  unsigned int n1 = nonEmptyCColMap.range();
  unsigned int n0 = nonEmptyKColMap.range();
  assert(v->size() == 2*n2+n1+n0);
  DoubleVec *mca = new DoubleVec(2*n2 + n1);

  assert(mca->size() >= n2+n1);
  assert(v->size() >= n2+n1);
  (void) memcpy(&(*mca)[0], &(*v)[0], (n2+n1)*sizeof(double)); // M and C parts

  assert(mca->size() >= 2*n2+n1);
  assert(v->size() >= 2*n2+n1+n0);
  (void) memcpy(&(*mca)[n2+n1], &(*v)[n2+n1+n0], n2*sizeof(double)); // a part
  return mca;
}

// Copy values from an MCa vector into an MCKa vector.

void LinearizedSystem::inject_MCa_dofs(const DoubleVec *src, DoubleVec *dest)
  const
{
  // Copy the contents of src, which has MCa indexing, to dest with
  // MCKa indexing..
  unsigned int n2 = nonEmptyMColMap.range();
  unsigned int n1 = nonEmptyCColMap.range();
  unsigned int n0 = nonEmptyKColMap.range();
  assert(src->size() == 2*n2+n1);
  assert(dest->size() == 2*n2+n1+n0);
  (void) memcpy(&(*dest)[0], &(*src)[0], (n2+n1)*sizeof(double)); // M & C parts
  assert(dest->size() >= 2*n2+n1+n0);
  assert(src->size() >= 2*n2+n1);
  (void) memcpy(&(*dest)[n2+n1+n0], &(*src)[n2+n1], n2*sizeof(double));
}

// Convert an MCa vector to an MCKa vector by inserting 0s for the K part.

void LinearizedSystem::expand_MCa_dofs(DoubleVec *dofs) const {
  // Take a vector of dof values with MCa indexing and convert it to
  // one with MCKa indexing by inserting zeros for the K part.
  unsigned int n2 = nonEmptyMColMap.range();
  unsigned int n1 = nonEmptyCColMap.range();
  unsigned int n0 = nonEmptyKColMap.range();
  assert(dofs->size() == 2*n2+n1);
  if(n0 > 0) {
    dofs->resize(2*n2 + n1 + n0, 0.0);
    // Move the aux dof values to the end.
    assert( dofs->size() >= 2*n2+n1+n0);  // Duh, we just resized it...
    (void) memmove(&(*dofs)[n2+n1+n0], &(*dofs)[n2+n1], n2*sizeof(double));

    // Insert zeros.
    assert(dofs->size() >= n2+n1+n0);
    (void) memset(&(*dofs)[n2+n1], 0, n0*sizeof(double));
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO OPT: These should return SparseSubMats.

SparseMat LinearizedSystem::K_submatrix(char whicheqn, char whichdof)
  const
{
  return SparseMat(K_,
		   subp2nonEmptyRowMap(whicheqn),
		   subp2nonEmptyColMap(whichdof));
}

SparseMat LinearizedSystem::C_submatrix(char whicheqn, char whichdof)
  const
{
  return SparseMat(C_,
		   subp2nonEmptyRowMap(whicheqn),
		   subp2nonEmptyColMap(whichdof));
}

SparseMat LinearizedSystem::M_submatrix(char whicheqn, char whichdof)
  const
{
  return SparseMat(M_,
		   subp2nonEmptyRowMap(whicheqn),
		   subp2nonEmptyColMap(whichdof));
}

SparseMat LinearizedSystem::J_submatrix(char whicheqn, char whichdof)
  const
{
  return SparseMat(J_,
		   subp2nonEmptyRowMap(whicheqn),
		   subp2nonEmptyColMap(whichdof));
}

bool LinearizedSystem::C21_nonempty() const {
  return (subp2nonEmptyRowMap('C').range() > 0 &&
	  subp2nonEmptyRowMap('M').range() > 0 &&
	  !C_.empty());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// K_MCK reorders K_indfree

SparseMat LinearizedSystem::K_MCK() const {
  return SparseMat(K_, subp2MCKEqnMap, subp2MCKFieldMap);
}

SparseMat LinearizedSystem::C_MCK() const {
  return SparseMat(C_, subp2MCKEqnMap, subp2MCKFieldMap);
}

SparseMat LinearizedSystem::M_MCK() const {
  return SparseMat(M_, subp2MCKEqnMap, subp2MCKFieldMap);
}

SparseMat LinearizedSystem::J_MCK() const {
  return SparseMat(J_, subp2MCKEqnMap, subp2MCKFieldMap);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// C_MCKa() and K_MCKa() return effective matrices for solving second
// order equations with a first order stepper.  If the equations are
// actually first order, then C_eff() and K_eff() just return C and K
// with reordered rows and columns to match the ordering used by
// get_unknowns().

// The DoFs are arranged as follows:
//
//   u2 = dofs that have second order time derivatives.
//   u1 = dofs that have first but not second order time derivatives.
//   u0 = dofs that have no time derivatives.
//   v  = first time derivative of u2
//
// The second derivatives are included by adding the auxiliary
// variables, v, and the auxiliary equation
//
//   (d/dt) u2 = v
//
// Then the full set of equations can be written
//
//   U = (u2, u1, u0, v)
//   C_eff*dU/dt + K_eff*U + f_eff = 0
//
// where
//
//          1   0   0   0             0   0   0  -1             0
// C_eff =  0 C11   0   0   K_eff = K12 K11 K10 C12    f_eff = f1
//          0   0   0   0           K02 K01 K00   0            f0
//          0 C21   0 M22           K22 K21 K20 C22            f2
//
// Note that the equation ordering is strange, in order to make C_eff
// sort of symmetric. If C11 and M22 are symmetric and C21 is 0, then
// C_eff is really symmetric.  The equation (and rhs) ordering for
// MCKa really should be called aCKM.
//
// If M is empty, then u2 is empty and so are C2x, Cx2, K2x, and Kx2,
// and the identity submatrices are 0x0.  C_eff is the same as
// C_indfree, except for possible trivial reordering.

SparseMat LinearizedSystem::C_MCKa() const {
  int n2 = subp2nonEmptyMColMap.range();
  int n1 = subp2nonEmptyCColMap.range();
  int n0 = subp2nonEmptyKColMap.range();
  int n = n0 + n1 + 2*n2;

  SparseMat Cf(n, n);

  // TODO OPT: If SparseMat::tile took map args, then the intermediate
  // Cxx, Kxx, and Mxx matrices wouldn't be necessary.

  SparseMat C11 = C_submatrix('C', 'C');
  SparseMat C21 = C_submatrix('M', 'C');
  SparseMat M22 = M_submatrix('M', 'M');

  Cf.tile(0, 0, identityMatrix(n2));
  Cf.tile(n2, n2, C11);
  Cf.tile(n2+n1+n0, n2, C21);
  Cf.tile(n2+n1+n0, n2+n1+n0, M22);

  Cf.consolidate();
  return Cf;
}


SparseMat LinearizedSystem::K_MCKa() const {
  int n2 = subp2nonEmptyMColMap.range();
  int n1 = subp2nonEmptyCColMap.range();
  int n0 = subp2nonEmptyKColMap.range();
  int n = n0 + n1 + 2*n2;

  SparseMat Kf(n, n);

  SparseMat K22 = K_submatrix('M', 'M');
  SparseMat K11 = K_submatrix('C', 'C');
  SparseMat K21 = K_submatrix('M', 'C');
  SparseMat K12 = K_submatrix('C', 'M');
  SparseMat K20 = K_submatrix('M', 'K');
  SparseMat K02 = K_submatrix('K', 'M');
  SparseMat K10 = K_submatrix('C', 'K');
  SparseMat K01 = K_submatrix('K', 'C');
  SparseMat K00 = K_submatrix('K', 'K');
  SparseMat C12 = C_submatrix('C', 'M');
  SparseMat C22 = C_submatrix('M', 'M');

  Kf.tile(0, n2+n1+n0, -1*identityMatrix(n2));
  Kf.tile(n2, 0, K12);
  Kf.tile(n2, n2, K11);
  Kf.tile(n2, n2+n1, K10);
  Kf.tile(n2, n2+n1+n0, C12);
  Kf.tile(n2+n1, 0, K02);
  Kf.tile(n2+n1, n2, K01);
  Kf.tile(n2+n1, n2+n1, K00);
  Kf.tile(n2+n1+n0, 0, K22);
  Kf.tile(n2+n1+n0, n2, K21);
  Kf.tile(n2+n1+n0, n2+n1, K20);
  Kf.tile(n2+n1+n0, n2+n1+n0, C22);

  Kf.consolidate();
  return Kf;
}

SparseMat LinearizedSystem::J_MCKa() const {
  // Almost the same as K_MCKa, but with J.
  // More explanation about J_MCKa can be found at static_residual_MCKa()
  int n2 = subp2nonEmptyMColMap.range();
  int n1 = subp2nonEmptyCColMap.range();
  int n0 = subp2nonEmptyKColMap.range();
  int n = n0 + n1 + 2*n2;

  SparseMat Jf(n, n);

  SparseMat J22 = J_submatrix('M', 'M');
  SparseMat J11 = J_submatrix('C', 'C');
  SparseMat J21 = J_submatrix('M', 'C');
  SparseMat J12 = J_submatrix('C', 'M');
  SparseMat J20 = J_submatrix('M', 'K');
  SparseMat J02 = J_submatrix('K', 'M');
  SparseMat J10 = J_submatrix('C', 'K');
  SparseMat J01 = J_submatrix('K', 'C');
  SparseMat J00 = J_submatrix('K', 'K');
  SparseMat C12 = C_submatrix('C', 'M');
  SparseMat C22 = C_submatrix('M', 'M');

  Jf.tile(0, n2+n1+n0, -1*identityMatrix(n2));
  Jf.tile(n2, 0, J12);
  Jf.tile(n2, n2, J11);
  Jf.tile(n2, n2+n1, J10);
  Jf.tile(n2, n2+n1+n0, C12);
  Jf.tile(n2+n1, 0, J02);
  Jf.tile(n2+n1, n2, J01);
  Jf.tile(n2+n1, n2+n1, J00);
  Jf.tile(n2+n1+n0, 0, J22);
  Jf.tile(n2+n1+n0, n2, J21);
  Jf.tile(n2+n1+n0, n2+n1, J20);
  Jf.tile(n2+n1+n0, n2+n1+n0, C22);

  Jf.consolidate();
  return Jf;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ForwardEuler and RK need to ensure that C_eff is not singular, so
// these versions don't include the K0x and Kx0 rows and columns.
// Actually, the static dofs may make non-zero contributions to the
// nonstatic equations via K10 and K20, so K_eff isn't square.
//
//          1   0   0             0   0   0  -1           0
// C_eff =  0 C11   0   K_eff = K12 K11 K10 C12  f_eff = f1
//          0 C21 M22           K22 K21 K20 C22          f2

SparseMat LinearizedSystem::C_MCa() const {
  int n2 = subp2nonEmptyMColMap.range();
  int n1 = subp2nonEmptyCColMap.range();

  SparseMat Cf(2*n2+n1, 2*n2+n1);

  Cf.tile(0, 0, identityMatrix(n2));
  {
    SparseMat C11 = C_submatrix('C', 'C');
    Cf.tile(n2, n2, C11);
  }
  {
    SparseMat C21 = C_submatrix('M', 'C');
    Cf.tile(n2+n1, n2, C21);
  }
  {
    SparseMat M22 = M_submatrix('M', 'M');
    Cf.tile(n2+n1, n2+n1, M22);
  }
  Cf.consolidate();
  return Cf;
}

SparseMat LinearizedSystem::K_MCa() const {

  unsigned int n2 = subp2nonEmptyMColMap.range();
  unsigned int n1 = subp2nonEmptyCColMap.range();
  unsigned int n0 = subp2nonEmptyKColMap.range();

  SparseMat Kf(2*n2+n1, 2*n2+n1+n0);

  Kf.tile(0, n2+n1+n0, -1.0*identityMatrix(n2));
  {
    SparseMat K12 = K_submatrix('C', 'M');
    Kf.tile(n2, 0, K12);
  }
  {
    SparseMat K11 = K_submatrix('C', 'C');
    Kf.tile(n2, n2, K11);
  }
  {
    SparseMat K10 = K_submatrix('C', 'K');
    Kf.tile(n2, n2+n1, K10);
  }
  {
    SparseMat C12 = C_submatrix('C', 'M');
    Kf.tile(n2, n2+n1+n0, C12);
  }
  {
    SparseMat K20 = K_submatrix('M', 'K');
    Kf.tile(n2+n1, n2+n1, K20);
  }
  {
    SparseMat K22 = K_submatrix('M', 'M');
    Kf.tile(n2+n1, 0, K22);
  }
  {
    SparseMat K21 = K_submatrix('M', 'C');
    Kf.tile(n2+n1, n2, K21);
  }
  {
    SparseMat C22 = C_submatrix('M', 'M');
    Kf.tile(n2+n1, n2+n1+n0, C22);
  }
  Kf.consolidate();
  return Kf;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Return the rhs vector for the independent equations (ie, the
// independent equation components of the rhs vector).  This combines
// the boundary and body rhs contributions from the Properties with
// the contributions from the fixed degrees of freedom.

DoubleVec *LinearizedSystem::rhs_ind() const {
  // rhs = f_body - f_bdy - C_indfix*udot_fix - K_indfix*u_fix

  // DoFMap::extract returns a new'd vector.
  DoubleVec *r = subp2indepEqnMap.extract(body_rhs-force_bndy_rhs);
  *r -= fix_bndy_rhs;
  return r;
}

void LinearizedSystem::find_fix_bndy_rhs(const DoubleVec *dofvalues) {
  // TODO OPT: Check timestamps and only recompute if necessary.

  // profile_rhs() is only called *after* find_fix_bndy_rhs(), so
  // clearing fix_bndy_rhs here is ok.  profile_rhs() adds to
  // fix_bndy_rhs but doesn't clear it.
  fix_bndy_rhs.clear();
  fix_bndy_rhs.resize(subp2indepEqnMap.range(), 0.0);

  // K times vector of fixed field values.
  DoubleVec *u = subp2fixedFieldMap.extract(*dofvalues);
  K_indfixed_.axpy(1.0, *u, fix_bndy_rhs);
  delete u;

  // For time-dependent boundary conditions, add C times vector of
  // fixed deriv values and M times vector of fixed acceleration
  // values.
  if(tdDirichlet) {
    if(C_.nnonzeros() > 0) {
      C_indfixed_.axpy(1.0, dirichlet1, fix_bndy_rhs);
    }
    if(M_.nnonzeros() > 0) {
      M_indfixed_.axpy(1.0, dirichlet2, fix_bndy_rhs);
    }
  }
}

// Extract subvectors of the rhs.  These use nonEmptyXRowMaps innstead
// of subp2nonEmptyXRowMaps because rhs_ind is indexed by independent
// equation number, not by subproblem equation number.

DoubleVec *LinearizedSystem::rhs_MCK() const {

  DoubleVec *rhsi = rhs_ind();

  int m2 = nonEmptyMRowMap.range();
  int m1 = nonEmptyCRowMap.range();
  int m0 = nonEmptyKRowMap.range();

  DoubleVec *rhs = new DoubleVec(m2 + m1 + m0);
  nonEmptyMRowMap.extract(*rhsi, *rhs, 0);
  nonEmptyCRowMap.extract(*rhsi, *rhs, m2);
  nonEmptyKRowMap.extract(*rhsi, *rhs, m2+m1);

  delete rhsi;
  return rhs;
}

DoubleVec *LinearizedSystem::rhs_MCKa() const {
  // rhs for the effective equations used by first order steppers when
  // solving second order problems.  Ordering of rows is really aCKM.
  // See comments before C_MCKa.
  DoubleVec *rhsi = rhs_ind();

  int m2 = nonEmptyMRowMap.range();
  int m1 = nonEmptyCRowMap.range();
  int m0 = nonEmptyKRowMap.range();

  DoubleVec *rhs = new DoubleVec(2*m2 + m1 + m0);
  nonEmptyCRowMap.extract(*rhsi, *rhs, m2);
  nonEmptyKRowMap.extract(*rhsi, *rhs, m2+m1);
  nonEmptyMRowMap.extract(*rhsi, *rhs, m2+m1+m0);

  delete rhsi;
  return rhs;
}

DoubleVec *LinearizedSystem::rhs_MCa() const {
  // Just like rhs_MCKa, but doesn't include the K part.  Used by
  // ForwardEuler and RK.  See comment at C_MCa.
  DoubleVec *rhsi = rhs_ind();

  int m2 = nonEmptyMRowMap.range();
  int m1 = nonEmptyCRowMap.range();

  DoubleVec *rhs = new DoubleVec(2*m2 + m1);
  nonEmptyCRowMap.extract(*rhsi, *rhs, m2);
  nonEmptyMRowMap.extract(*rhsi, *rhs, m2+m1);
  delete rhsi;
  return rhs;
}

DoubleVec *LinearizedSystem::rhs_ind_part(char which) const {
  DoubleVec *fullrhs = rhs_ind();
  DoubleVec *r = indepEqn2nonEmptyRowMap(which).extract(*fullrhs);
  delete fullrhs;
  return r;
}

DoubleVec *LinearizedSystem::static_residual_MCK() const {
  return subp2MCKEqnMap.extract(force_bndy_rhs + residual);
}


// The 2nd order time-dependent nonlinear problem is given by
//
//    M22 u2" + C22 u2' + C21 u1' + F2(u2,u1,u0) = 0
//              C12 u2' + C11 u1' + F1(u2,u1,u0) = 0
//                                  F0(u2,u1,u0) = 0
//
// where u2'=(d/dt)u2, u2"=(d^2/dt^2)u2.
//
// To solve the 2nd order problem, we convert it into a 1st order problem
// by introducing an auxiliary variable v=u2'. The new 1st order system is:
//
//        C21 u1' + M22 v' + C22 v + F2(u2,u1,u0) = 0
//        C11 u1'          + C12 v + F1(u2,u1,u0) = 0
//                                   F0(u2,u1,u0) = 0
//    u2'                    -   v    = 0
//
// We reorder the equations
//
//    u2'                    -   v    = 0
//        C21 u1' + M22 v' + C22 v + F2(u2,u1,u0) = 0
//        C11 u1'          + C12 v + F1(u2,u1,u0) = 0
//                                   F0(u2,u1,u0) = 0
//
// and write in matrix form
//
//     / 1  0  0  0 \  / u2'\   /    -v     \    / 0 \  [ending a comment line
//    |  0 C11 0  0  | | u1'| + | F1 + C12*v | = | 0 |   with \ is bad practice]
//    |  0  0  0  0  | | u0'|   |     F0     |   | 0 |
//     \ 0 C21 0 M22/  \  v'/   \ F2 + C22*v /   \ 0 /
//
//    \______  _____/  \_  _/   \______  ____/
//           \/          \/            \/
//           C_eff       w'            F_eff (=static residual)
//
// The new 1st order eqn can be concisely written as
//
//       C_eff dw/dt + F_eff(w) = 0      ( w=(u2,u1,u0,v) )
//
// Backward Euler method applied to this equation would need to solve
// the following equation for z (=w_{n+1}) at each time step
//
//       C_eff (z - w_n) + dt F_eff(z) = 0
//
// The nonlinear solver would need the residual and possibly the Jacobian
// or the linear coefficient matrix:
//
//    r(z) = C_eff z + dt F_eff(z) - C_eff w_n  (F_eff = static_residual_MCKa)
//    J(z) = C_eff + dt DF_eff(z)   (DF_eff = J_MCKa)
//    K    = C_eff + dt K_eff       (K_eff = K_MCKa)


DoubleVec *LinearizedSystem::static_residual_MCKa(const DoubleVec *unknowns)
  const
{
  int m2 = subp2nonEmptyMRowMap.range();
  int m1 = subp2nonEmptyCRowMap.range();
  int m0 = subp2nonEmptyKRowMap.range();

  // See comments above C_MCKa explaining the odd (aCKM) ordering.
  DoubleVec fullresidual = force_bndy_rhs + residual;
  DoubleVec *resid = new DoubleVec(2*m2 + m1 + m0);
  subp2nonEmptyCRowMap.extract(fullresidual, *resid, m2);
  subp2nonEmptyKRowMap.extract(fullresidual, *resid, m2+m1);
  subp2nonEmptyMRowMap.extract(fullresidual, *resid, m2+m1+m0);

  if(m2 > 0) {
    SparseMat CC(2*m2 + m1 + m0, m2);
    DoubleVec *derivs = get_derivs_part_MCKa('M', unknowns);
    SparseMat C22 = C_submatrix('M', 'M');
    SparseMat C12 = C_submatrix('C', 'M');
    CC.tile(0, 0, -1.0*identityMatrix(m2));
    CC.tile(m2, 0, C12);
    CC.tile(m2+m1+m0, 0, C22);
    CC.axpy(1.0, *derivs, *resid);
    delete derivs;
  }
  return resid;

  //*// This version can be used for testing the nonlinear solvers on
  //*// linear problems.
  // DoubleVec *rhs = rhs_MCKa();
  // SparseMat K = K_MCKa();
  // DoubleVec *resid = new DoubleVec(K*(*unknowns)-*rhs);
  // delete rhs;
  // return resid;
}

DoubleVec *LinearizedSystem::static_residual_MCa(const DoubleVec *unknowns)
  const
{
  int m2 = subp2nonEmptyMRowMap.range();
  int m1 = subp2nonEmptyCRowMap.range();

  DoubleVec fullresidual = force_bndy_rhs + residual;
  DoubleVec *resid = new DoubleVec(2*m2 + m1);
  subp2nonEmptyCRowMap.extract(fullresidual, *resid, m2);
  subp2nonEmptyMRowMap.extract(fullresidual, *resid, m2+m1);

  if(m2 > 0) {
    SparseMat CC(2*m2 + m1, m2);
    DoubleVec *derivs = get_derivs_part_MCKa('M', unknowns);
    SparseMat C22 = C_submatrix('M', 'M');
    SparseMat C12 = C_submatrix('C', 'M');
    CC.tile(0, 0, -1.0*identityMatrix(m2));
    CC.tile(m2, 0, C12);
    CC.tile(m2+m1, 0, C22);
    CC.axpy(1.0, *derivs, *resid);
    delete derivs;
  }
  return resid;
}

DoubleVec *LinearizedSystem::static_residual_ind_part(char which) const {
  return subp2nonEmptyRowMap(which).extract(force_bndy_rhs + residual);
}

const DoubleVec &LinearizedSystem::raw_static_residual() const {
  return residual;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const DoFMap &LinearizedSystem::subp2nonEmptyColMap(char which) const {
  if(which == 'M')
    return subp2nonEmptyMColMap;
  if(which == 'C')
    return subp2nonEmptyCColMap;
  if(which == 'K')
    return subp2nonEmptyKColMap;
  throw ErrProgrammingError("Bad map requested", __FILE__, __LINE__);
}

const DoFMap &LinearizedSystem::subp2nonEmptyRowMap(char which) const {
  if(which == 'M')
    return subp2nonEmptyMRowMap;
  if(which == 'C')
    return subp2nonEmptyCRowMap;
  if(which == 'K')
    return subp2nonEmptyKRowMap;
  throw ErrProgrammingError("Bad map requested", __FILE__, __LINE__);
}

const DoFMap &LinearizedSystem::indepEqn2nonEmptyRowMap(char which) const {
  if(which == 'M')
    return nonEmptyMRowMap;
  if(which == 'C')
    return nonEmptyCRowMap;
  if(which == 'K')
    return nonEmptyKRowMap;
  throw ErrProgrammingError("Bad map requested", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// FloatBC support

void LinearizedSystem::applyFloatBC(int olddofindex, int newdofindex,
				    int oldeqnindex, int neweqnindex,
				    int oldderivindex, int newderivindex)
{
  // Both old and new indices are subproblem indices.  Old indices are
  // for dofs, derivs, and eqns that are being mapped to others (being
  // made subservient to them by FloatBCs).  "New" means the new
  // values of the old indices, ie, the indices of the master dofs,
  // derivs, and eqns.

  // The new indices are given as subproblem indices, but we're
  // changing the way they're mapped to matrix indices, so first
  // translate the new indices.
  int newfreefieldindex = subp2freeFieldMap[newdofindex];
  int newfixedfieldindex = subp2fixedFieldMap[newdofindex];
  int newindepeqnindex = subp2indepEqnMap[neweqnindex];
  int newfreederivindex = -1;
  if(newderivindex != -1)
    newfreederivindex = subp2freeDerivMap[newderivindex];

  // This makes the subproblem --> indepEqn/freeDoF maps many-to-one,
  // so the inverse maps aren't well defined.  We don't touch the
  // inverse maps here.
  //
  // This doesn't have to modify dof2Deriv, because it already
  // contains the newdofindex, newderivindex pair.

  subp2freeFieldMap.reassign(olddofindex, newfreefieldindex);
  subp2fixedFieldMap.reassign(olddofindex, newfixedfieldindex);
  subp2freeDerivMap.reassign(oldderivindex, newfreederivindex);
  subp2indepEqnMap.reassign(oldeqnindex, newindepeqnindex);

  subproblem->set_slaveDoF(olddofindex);

  // TODO OPT: Mark maps as out-of-date.

  // subp2freeFieldMasterMap and subp2freeDerivMasterMap contain just
  // the fields and derivs that are the master DoFs for FloatBCs.
  // That is, they are the DoFs that are actually solved for.  When
  // extracting the unknown values from the SubProblem, it's important
  // to use the value of the reference DoF, but when there are
  // FloatBCs, the subp2freeFieldMap maps many DoFs to the same
  // target, so it doesn't necessarily get the right one.  Here we
  // find out which DoF was the reference by using the unedited
  // inverse map, and keep track of it so that the correct DoF values
  // can be extracted simply by applying subp2freeFieldMasterMap after
  // subp2freeFieldMap.

  if(newfreefieldindex != -1) {
    int masterfield = freeField2subpMap[newfreefieldindex];
    subp2freeFieldMasterMap.reassign(masterfield, newfreefieldindex);
  }
  if(newfreederivindex != -1) {
    int masterderiv = freeDeriv2subpMap[newfreederivindex];
    subp2freeDerivMasterMap.reassign(masterderiv, newfreederivindex);
  }
}

// The cleanmaps operation restores maps to consistency after the
// application of a FloatBC.  The FloatBC's cause several dofs or
// equations to be mapped to a single row or column.  As a result, the
// range of the maps can develop holes -- cleanmaps() closes those
// holes, ensuring that the range of the map is a contiguous group of
// integers from 0 to the appropriate N.

void LinearizedSystem::cleanmaps() {
  std::vector<int> *subtractors = subp2freeFieldMap.clean();
  subp2freeFieldMasterMap.do_clean(subtractors);
  subp2freeFieldMasterMap.coerce_range(subp2freeFieldMap.range());
  delete subtractors;

  subtractors = subp2freeDerivMap.clean();
  subp2freeDerivMasterMap.do_clean(subtractors);
  subp2freeDerivMasterMap.coerce_range(subp2freeDerivMap.range());
  delete subtractors;

  subtractors = subp2indepEqnMap.clean();
  delete subtractors;
}

// profile_rhs() is called by FloatBC.contrib_rhs() to make the
// boundary condition's contributions to the rhs vector.  These
// contributions are K times the profile offset.  The values are used
// only if the solver is linear.

void LinearizedSystem::profile_rhs(const FloatBCApp &fbcapp) {
  const FloatBCApp::ProfileData &pfd = fbcapp.profile_data;
  // TODO OPT: Aggregate data from all FloatBCs and make just one call
  // to this function, so that the loop over K doesn't have to be
  // repeated.  This can be done easily by storing ProfileData in the
  // LinearizedSystem instead of in the FloatBCApp.
  for(SparseMat::iterator kij=K_.begin(); kij!=K_.end(); ++kij) {
    FloatBCApp::ProfileData::const_iterator x = pfd.find(kij.col());
    if(x != pfd.end()) {
      int row = subp2indepEqnMap[kij.row()];
      if(row != -1) {
	fix_bndy_rhs[row] += (*kij) * (*x).second;
      }
    }
  }
}

int LinearizedSystem::getSubproblemDoFIndex(const FuncNode *node,
					    const Field *field, int fcomp)
  const
{
  return subproblem->mesh2subpDoFMap[(*field)(*node, fcomp)->dofindex()];
}

int LinearizedSystem::getSubproblemEqnIndex(const FuncNode *node,
					    const Equation *eqn, int ecomp)
  const
{
  return subproblem->mesh2subpEqnMap[eqn->nodaleqn(*node, ecomp)->ndq_index()];
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void LinearizedSystem::initDirichletDerivatives() {
  int nfixed = subp2fixedFieldMap.range();
  tdDirichlet = false;
  dirichlet1.clear();
  dirichlet1.resize(nfixed, 0.0);
  dirichlet2.clear();
  dirichlet2.resize(nfixed, 0.0);
}

void LinearizedSystem::setDirichletDerivatives(
         const FuncNode *node, const Field *field, int comp,
	 double udot, double udotdot)
{
  int indx = mesh2fixedFieldMap[(*field)(node, comp)->dofindex()];
  if(indx != -1) {
    dirichlet1[indx] = udot;
    dirichlet2[indx] = udotdot;
    tdDirichlet = true;
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void LinearizedSystem::dumpAll(const std::string &filename, double time, 
			       const std::string &comment)
  const
{
  std::ofstream os((filename+"_matrices").c_str()); 
  os << "---------------------" << std::endl;
  os << "---------------------" << std::endl;
  os << comment << " " << time << std::endl;
  os << "K_:" << std::endl << K_ << std::endl;
  os << "C_:" << std::endl << C_ << std::endl;
  os << "M_:" << std::endl << M_ << std::endl;
  os << "K_indfree_:" << std::endl << K_indfree_ << std::endl;
  os << "C_indfree_:" << std::endl << C_indfree_ << std::endl;
  os << "M_indfree_:" << std::endl << M_indfree_ << std::endl;
  os << "J_indfree_:" << std::endl << J_indfree_ << std::endl;
  os << "K_indfixed_:" << std::endl << K_indfixed_ << std::endl;
  os << "C_indfixed_:" << std::endl << C_indfixed_ << std::endl;
  os << "M_indfixed_:" << std::endl << M_indfixed_ << std::endl;
  os.close();

  std::ofstream os2((filename+"_maps").c_str());
  os2 << "subp2freeFieldMap: " << subp2freeFieldMap << std::endl;
  os2 << "subp2fixedFieldMap: " << subp2fixedFieldMap << std::endl;
  os2 << "subp2freeDerivMap: " << subp2freeDerivMap << std::endl;
  os2 << "subp2indepEqnMap: " << subp2indepEqnMap << std::endl;
  os2 << "freeField2subpMap: " << freeField2subpMap << std::endl;
  os2 << "freeDeriv2subpMap: " << freeDeriv2subpMap << std::endl;
  os2 << "nonEmptyMRowMap: " << nonEmptyMRowMap << std::endl;   
  os2 << "nonEmptyMColMap: " << nonEmptyMColMap << std::endl;   
  os2 << "nonEmptyCRowMap: " << nonEmptyCRowMap << std::endl;   
  os2 << "nonEmptyCColMap: " << nonEmptyCColMap << std::endl;   
  os2 << "nonEmptyKRowMap: " << nonEmptyKRowMap << std::endl;   
  os2 << "nonEmptyKColMap: " << nonEmptyKColMap << std::endl;   
  os2 << "mesh2fixedFieldMap: " << mesh2fixedFieldMap << std::endl; 
  os2 << "subp2nonEmptyMColMap: " << subp2nonEmptyMColMap << std::endl;
  os2 << "subp2nonEmptyCColMap: " << subp2nonEmptyCColMap << std::endl;
  os2 << "subp2nonEmptyKColMap: " << subp2nonEmptyKColMap << std::endl;
  os2 << "subp2nonEmptyMRowMap: " << subp2nonEmptyMRowMap << std::endl;
  os2 << "subp2nonEmptyCRowMap: " << subp2nonEmptyCRowMap << std::endl;
  os2 << "subp2nonEmptyKRowMap: " << subp2nonEmptyKRowMap << std::endl;
  os2 << "subp2nonEmptyMDerivMap: " << subp2nonEmptyMDerivMap << std::endl;
  os2 << "subp2MCKFieldMap: " << subp2MCKFieldMap << std::endl;
  os2 << "subp2MCKEqnMap: " << subp2MCKEqnMap << std::endl;
  os2 << "subp2MCKDerivMap: " << subp2MCKDerivMap << std::endl;
  os2 << "subp2freeFieldMasterMap: " << subp2freeFieldMasterMap << std::endl;
  os2 << "subp2freeDerivMasterMap: " << subp2freeDerivMasterMap << std::endl;
  os2 << "subp2MCKFieldMasterMap: " << subp2MCKFieldMasterMap << std::endl; 
  os2 << "subp2nonEmptyMDerivMasterMap: " << subp2nonEmptyMDerivMasterMap
     << std::endl;
  os2 << "subp2MCKDerivMasterMap: " << subp2MCKDerivMasterMap << std::endl;
  os2.close();

  std::ofstream os3((filename+"_vectors").c_str());
  os3 << "residual: " << residual << std::endl;
  os3 << "dirichlet1: " << dirichlet1 << std::endl;
  os3 << "dirichlet2: " << dirichlet2 << std::endl;
  os3 << "tdDirichlet: " << tdDirichlet << std::endl;
  os3 << "time_: " << time_ << std::endl;
  os3 << "dofstates_: " << dofstates_ << std::endl;
  os3 << "dependenteqns_: " << dependenteqns_ << std::endl;
  os3 << "body_rhs:" << body_rhs << std::endl;
  os3 << "fix_bndy_rhs:" << fix_bndy_rhs << std::endl;
  os3 << "force_bndy_rhs:" << force_bndy_rhs << std::endl;
  os3.close();
}
