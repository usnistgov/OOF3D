// -*- C++ -*-
// $RCSfile: csubproblem.h,v $
// $Revision: 1.32.2.10 $
// $Author: fyc $
// $Date: 2015/01/07 15:53:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef SUBPROBLEM_H
#define SUBPROBLEM_H

#include <oofconfig.h>


// Underlying C++ base class for SubProblems.  SubProblems contain all
// of the machinery for defining Fields and solving Equations on a
// FEMesh.  The FEMesh hosts the subproblems and contains the Nodes
// and Elements.  The various derived SubProblem classes differ in how
// they chose which portions of the FEMesh to solve.

class CSubProblem;
#include "common/coord_i.h"
#include "common/identification.h"
#include "common/lock.h"
#include "engine/dofmap.h"
#include "engine/materialset.h"

#include <set>
#include <string>
#include <vector>

class CConjugatePair;
class CMicrostructure;
class CNonlinearSolver;
class CompoundField;
class DoFMap;
class DoubleVec;
class Element;
class ElementIterator;
class Equation;
class FEMesh;
class Field;
class Flux;
class FuncNode;
class FuncNodeIterator;
class LinearizedSystem;
class Lock;
class Material;
class MasterCoord;
class NodalEquation;
class Node;
class NodeIterator;
class Property;

//AMR subproblem
class NodalFluxes;
class NodalSCPatches;


// CSubProblem is derived from IdentifiedObject so that it can provide
// a simple Python __hash__ function, defined in csubproblem.swg.

class CSubProblem : public IdentifiedObject {
private:
  RWLock *rwlock;
  CSubProblem(const CSubProblem&); // prohibited
  static long globalCSubProblemCount;
  DoFMap mesh2subpDoFMap;
  DoFMap mesh2subpEqnMap;
  int nNodes_;
  std::set<int> slaveDoFs;
  
public:
  CSubProblem();
  virtual ~CSubProblem();

  // set_femesh must be called right after initialization.  It's not
  // called by the constructor because the constructor is called by a
  // RegisteredClass registration, before the mesh is known.
  void set_mesh(FEMesh *msh);
  void set_nnodes(int);
  FEMesh *mesh;
  FEMesh *get_mesh() const { return mesh; }

  Lock precomputeLock;
  bool precomputeRequired;
  bool consistency;

  CMicrostructure *get_microstructure() const;
  virtual MaterialSet *getMaterials() const;

  // redefined() must be called when the criteria for choosing nodes
  // and elements in a subproblem has changed.  For example, if
  // Material assignments have changed,
  // MaterialSubProblem::redefined() should be called.
  virtual void redefined() {}

  virtual ElementIterator element_iterator() const = 0;
  virtual NodeIterator node_iterator() const = 0;
  virtual FuncNodeIterator funcnode_iterator() const = 0;
  virtual bool contains(const Element *) const = 0;
  virtual bool containsNode(const Node *) const = 0;

  // Machinery to symmetrize the stiffness matrix
  std::vector<int> global_dof2eqn_map;

  void mapFields();
  // set_meshdofs and get_meshdofs copy all of the subproblem dofs
  // from the mesh to the given vector, or vice versa.  This includes
  // *all* dofs, both fixed and free, field and derivative.
  bool set_meshdofs(const DoubleVec*) const;
  DoubleVec *get_meshdofs() const; 


  // Given the subproblem index i of a DoF, dof2Deriv[i] is the
  // subproblem index of the time derivative of the DoF.  Note that
  // dof2Deriv is a std::map, not a vector, and it doesn't contain
  // entries for DoFs that don't have derivatives.
  DoFMap::TranslationMap dof2Deriv;
  // Get the subproblem deriv index corresponding to a subproblem
  // field index, or -1 if none.
  int getDerivIndex(int) const;

  // slaveDoFs are the DoFs involved in floating boundary conditions
  // that aren't the master DoFs.
  void set_slaveDoF(int);
  const std::set<int> &get_slaveDoFs() const { return slaveDoFs; }
  void clear_slaveDoFs();

  // Call the given callback function for all defined Fields.
  void fieldLooper(void (*)(void*, const Field&, const Field&, bool),
		   void*) const;

  void setStaticStepper(bool x);
  bool staticStepper() const { return staticStepper_; }

private:

  // active_flux_map and active_equation_map cache the lists of active
  // fluxes and equations for each Material.
  typedef std::map<const Material*, std::vector<Flux*>*, MaterialCompare>
     ActiveFluxMap;
  ActiveFluxMap active_flux_map;
  typedef std::map<const Material*, std::vector<Equation*>*, MaterialCompare>
     ActiveEqnMap;
  ActiveEqnMap active_equation_map;

  // For constructing mesh2subpDoFMap, etc.  Called by mapFields().
  static void mapField(void*, const Field&, const Field&, bool);
  void mapField_(const Field&, const Field&, bool);
public:
#ifdef HAVE_MPI
  // These are arrays corresponding to the freedofmap and indepeqnmap
  // but with the shared non-owned rows and columns indicated.  At the
  // end of the day, these should map the indices of the local
  // stiffness matrix onto the combined stiffness matrix
  std::vector<int> m_precombined_freedofmap;
  std::vector<int> m_precombined_indepeqnmap;
  // These are less than or equal to m_precombined_freedofmap.size()
  // (not counting the -1)
  int m_precombined_dofsize;
  int m_precombined_eqnsize;
  void set_parallel_mapping();
  // This member stores the cumulative sum of pdofsizelist
  // (dofsize0+dofsize1+...)
  int m_combinedmatrixdim;
  // This function for displaying solution at the FuncNodes
  void NodalPositionSolution(double* temp_array);
  //
  void ResetSharesData();
  // Gather total number of unique nodes for this subproblem.
  // First get the number of nodes in this process for this
  // subproblem (if the node is shared, count it if this
  // process owns the node). When these are collected
  // from all processes and added together, it will give the total number
  // of unique nodes for this subproblem (useful for subproblem info)
  int GatherNumNodes();
#endif	// HAVE_MPI

//   void dump_dof() const;	// for debugging
//   void dump_eqn() const;

  LinearizedSystem *new_linear_system(double time);
  void make_linear_system(LinearizedSystem *linearsystem,
			  const CNonlinearSolver*) const;

  int ndof() const;
  int neqn() const;
  int nelements() const;
  int nnodes() const;
  int nfuncnodes() const;

  void activate_equation(Equation &);
  void deactivate_equation(Equation &);
  bool is_active_equation(const Equation&) const;
  int n_active_eqns() const;

  void activate_flux(const Flux&);
  void deactivate_flux(const Flux&);
  bool is_active_flux(const Flux&) const;

  // active_fluxes() and active_equations() return the lists of active
  // fluxes and equations relevant to the given material.  The lists
  // are computed by Material::precompute() and used in
  // Material::make_linear_system(), but are stored in CSubProblem
  // because they may differ from subproblem to subproblem.
  const std::vector<Flux*> &active_fluxes(const Material*) const;
  const std::vector<Equation*> &active_equations(const Material*) const;
  // The non-const versions of these routines will create the lists if
  // they don't already exist.
  std::vector<Flux*> &active_fluxes(const Material*);
  std::vector<Equation*> &active_equations(const Material*);
  // Delete cached data for the given Material.
  void clear_active_fluxes(const Material*);
  void clear_active_equations(const Material*);

  // activate, etc, for Fields have to be routed through Field virtual
  // functions, because they have to know if the Field is a
  // CompoundField or not.  The routines that do the real work are
  // SubProblem::do_activate, etc.
  void activate_field(const Field&);
  void deactivate_field(const Field&);
  void acquire_field_data(Field &field, const CSubProblem*);
  bool define_field(const Field&); // return true if field newly defined
  void undefine_field(const Field&);

#if DIM==2
  bool in_plane(const Field&) const;
#endif // DIM==2

  // active fields are being solved for
  void do_activate_field(const Field&);
  void do_deactivate_field(const Field&);
  bool is_active_field(const Field&) const;
  int n_active_fields() const;

  // defined fields have values at nodes
  void do_define_field(const Field&);
  void do_undefine_field(const Field&);
  bool is_defined_field(const Field&) const;

  // List of this subproblem's defined fields.
  std::vector<CompoundField*>* all_compound_fields() const;
  std::vector<Equation*>* all_equations() const;
  std::vector<Flux*>* all_fluxes() const;
  std::vector<Flux*> allFluxes() const;  // no need to free memory.

  // Call requirePrecompute() when Materials change or Fields are
  // defined.  The actual precompute() function is in csubproblem.spy.
  void requirePrecompute();

  // Functions for symmetrizing the stiffness matrix, if
  // possible. set_equation_mapping is called from the conjugacy code,
  // and sets up a map whose index is the position of a nodal equation
  // in the FEMesh's master list of nodal equations, and whose value
  // is the row of the master stiffness matrix to which this
  // corresponds.
  void set_equation_mapping(const std::vector<CConjugatePair*>*);
//   int check_symmetricity(const SparseMat &); //for debugging only

  // Run post-solver processing routines in those materials/properties
  // that have them.  This should eventually depend upon which
  // auxiliary fields are contributed to by the material.
  void post_process();

  // API for setting/referring to the read-write lock.  Set_rwlock
  // should be called exactly once when the SubProblem is inserted
  // into a SubProblemContext object.
  void set_rwlock(RWLock *rw) { rwlock = rw; };
  RWLock *get_rwlock() { return rwlock;};

  void cache_active_prop(const Property*, bool);
  bool currently_active_prop(const Property*) const; // returns cached value
  // void find_computable_prop(const Property*);
  // bool currently_computable_prop(const Property*) const;
  void cache_nonlinearity_prop(const Property*, bool);
  bool currently_nonlinear_prop(const Property*) const;
private:

  // Is a Flux active?  Stored as an int, because a Flux can be
  // activated more than once.
  std::vector<int> active_flux;


  // This is data that can't live in the Field class, because there is
  // only one instance of each Field, but it might have different
  // properties on each SubProblem, and there might be more than one
  // SubProblem.  Planarity data isn't stored here, because it's
  // determined at the FEMesh level.
  class FieldData {
  public:
    FieldData();
  private:
    bool active;		// is this field being solved for?
    bool defined;		// have DoF's been assigned?
    friend class CSubProblem;
  };
  std::vector<FieldData> fielddata;

  // This is data that can't live in the Equation class, for the same
  // reason that the FieldData can't live in the Field class.
  class EquationData {
  public:
    EquationData();
  private:
    bool active;
    friend class CSubProblem;
  };
  std::vector<EquationData> eqndata;

  int n_active_eqn;		// number of explicitly activated eqns
  int n_active_field;		// number of explicitly activated fields

  bool staticStepper_;

  friend class SubProblemElementIterator;
  friend class SubProblemFuncNodeIterator;
  friend class SubProblemNodeIterator;
  friend long get_globalCSubProblemCount();

  // Various flags that used to be stored in a SubProblem-keyed map in
  // Property, which is a bad idea because Properties generally
  // outlive SubProblems.
  typedef std::map<const Property*, bool> PropertyFlagCache;
  PropertyFlagCache propActivity;
  // PropertyFlagCache propComputability;
  PropertyFlagCache propNonlinearity;


  //Adaptive Mesh Refinement stuff translocated from femesh.h
public:
  // TODO 3.1: encapsulate all of the ZZ error estimation stuff, so that
  // we can switch estimators.

  // create & add a new CSCPatch pointer
  void init_scpatches(const std::vector<int>*);
  void add_scpatch(const int, const Material*,
		   const int,
		   const std::vector<int>*,
		   const std::vector<int>*,
		   const int);
  // getting elements & nodes from the patch
  std::vector<int> *get_elements_from_patch(const int, const Material*);
  std::vector<int> *get_nodes_from_patch(const int, const Material*);
  // recovering flux(es)
  void init_nodalfluxes();
  void recover_fluxes();
  // adding recovered flux
  void add_this_flux(const Material*, const Flux*,
		     const Node*, DoubleVec*);
  // recovered flux at a given point
  DoubleVec *get_recovered_flux(const Flux*, const Element*,
					  const MasterCoord&);
  // reporting recovered fluxes at a given point -- debug purpose
  void report_recovered_fluxes(const Element*, const Coord*);
  // estimating error
  double zz_L2_estimate(const Element*, const Flux*);
  void zz_L2_estimate_sub(const Element*, const Flux*,
			  const int&, double&, double&,
			  const MasterCoord&, const double&);
  DoubleVec *zz_L2_weights(const Flux*,
				     const double&, const double&);
  void zz_L2_weights_sub(const Element*, const Flux*,
			  const int&, double&,
			  const MasterCoord&, const double&);

private:
  // Storage for CSCPatch's (keyed an assembly node)
  // NodalSCPatches contains as many CSCPatches as no. of Materials
  // at the assembly node.
  std::map<const int, NodalSCPatches*> scpatches;
  // Storage for SCpatch Recovered Fluxes
  std::map<const int, NodalFluxes*> recovered_fluxes;


  friend class LinearizedSystem;
};				// class CSubProblem

long get_globalCSubProblemCount();

#endif // SUBPROBLEM_H
