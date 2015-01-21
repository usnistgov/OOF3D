// -*- C++ -*-
// $RCSfile: femesh.h,v $
// $Revision: 1.107.2.22 $
// $Author: langer $
// $Date: 2014/12/14 22:49:19 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef FEMESH_H
#define FEMESH_H

class FEMesh;

#include "common/coord_i.h"
#include "common/lock.h"
#include "engine/elementshape.h"
#include "engine/equation.h"
#include "engine/field.h"
#include "engine/fieldeqnlist.h"
#include "engine/materialset.h"
#include <map>
#include <set>
#include <string>
#include <vector>
#include <vtkIntArray.h>
#include <vtkSmartPointer.h>
#include <vtkUnstructuredGrid.h>

class CMicrostructure;
class CSkeletonBase;
class Condition;
class DegreeOfFreedom;
class DoFMap;
class DoubleVec;
class Element;
class ElementIterator;
class Equation;
class Field;
class FuncNode;
class FuncNodeIterator;
// class InterfaceElement;
class Lock;
class MasterCoord;
class MeshDataCache;
class NodalEquation;
class Node;
class NodeIterator;
class RWLock;
class SkeletonFilter;
struct DoFCompare;
struct NodalEqnCompare;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef HAVE_MPI
class CNodeShareInfo
{
public:
  CNodeShareInfo(std::vector<int>* procs,
		 std::vector<int>* indices, int index);
  ~CNodeShareInfo();
   // index inherited from the skeleton nodes sharing information
  int inheritedindex,nextindex;
  //the rank of the process
  int localprocrank,nextrank;
  // Des this process own the node? It does if the process is the
  // lowest ranked among those that share this node.
  // (This may now vary or get passed to the next process during a solve step.)
  bool owns;
  // Same as owns but this ownership flag should not change once created.
  bool _owns0;
  // Set to true if the sharenode is part of a subproblem element in the process
  // as determined during the solve step.
  bool hasElement;
  // list of processes (rank numbers) that share this node:
  std::vector<int> remoteproclist;
  // list of indices of this node corresponding to the other processes
  // listed in remoteproclist:
  std::vector<int> remoteindexlist;
  // The following four vectors should have the same length.  These
  // get filled up in set_equation_mapping.
  // list of indices of the free DoFs within this node:
  std::vector<int> localdofindexlist;
  // list of indices of the independent NodalEqns within this node:
  std::vector<int> localeqnindexlist;
  // list of indices into the (probably) symmetrized stiffness matrix
  // of the free DoFs:
  std::vector<int> symmatrixdofindexlist;
  // list of indices into the (probably) symmetrized stiffness matrix
  // of the independent NodalEqns:
  std::vector<int> symmatrixeqnindexlist;
};
// Then construct a mapping of the indices in the symmatrixdofindexlist to the
//  combined/global/"uber" linear system.
// Also need a list of the localdofsizes [dofsize0,dofsize1,...]

#endif // HAVE_MPI

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class FEMesh {    // : public PythonExportable<FEMesh> {
  // FEMesh used to be derived from PythonExportable so that it could
  // be used as an argument in switchboard messages.
private:
  CMicrostructure * microstructure;
  RWLock *rwlock;
  static long globalFEMeshCount;
  DoubleVec *dofvalues;
  double time;		       // max time attained by all subproblems
  CSubProblem *currentSubProblem_;

  // Cache for timestep data
  MeshDataCache *dataCache;
  // It's necessary to use an SLock instead of a Lock here because the
  // data cache must be accessed on the main thread when vtk is
  // drawing.  See MeshGridSource::GetGrid() in
  // engine/IO/gridsource.C.
  SLock masterCacheLock;
  // pthreads condition variable that indicates when the cache isn't
  // being read.
  Condition noCacheReadersCond;
  int nCacheReaders;		// number of cache readers

public:
  FEMesh(CMicrostructure *);
  virtual ~FEMesh();
  CMicrostructure *get_microstructure() const { return microstructure; }
  virtual const std::string &classname() const;
  virtual const std::string &modulename() const;

  ElementIterator element_iterator() const;
  NodeIterator node_iterator() const;
  FuncNodeIterator funcnode_iterator() const;

  typedef std::map<const ElementShape*, int> ElementShapeCountMap;
  ElementShapeCountMap *getElementShapeCounts() const;

  Node *newMapNode(const Coord&); // the only way to make a Node
  FuncNode *newFuncNode(const Coord&); // the only way to make a FuncNode

#ifdef HAVE_MPI
  // These carry the extra sharing information derived from the
  // parallel skeleton construction of Haan
  FuncNode *newFuncNode_shares(const Coord&,std::vector<int> * procs,
			       std::vector<int> * remoteindices, int index);
  // Map of inherited index to shared FuncNodes
  std::map<int,FuncNode*> m_indexnodemap;
  // It felt natural to associate CNodeShareInfo directly with a FuncNode
  //* TODO 3.1: Give NodeShareMap an explicit comparison operator, so that
  //* its storage order is reproducible.
  typedef std::map<FuncNode*,CNodeShareInfo*> NodeShareMap;
  NodeShareMap m_nodesharemap;
  // These maps are keyed by DoFs and NodalEqns.
  // These link to the sharing information stored in the FuncNode
  // and in the two maps above. The intention is to add to the map only
  // those DoFs and NodalEqns that are associated
  // with a node that is shared between two or more processes.
  // In principle, one can search the doflist or eqnlist of the FuncNode's
  // to get the right FuncNode, but this is slower. (This may be temporary)
  typedef std::map<DegreeOfFreedom*, FuncNode*, DoFCompare> DoFNodeMap;
  DoFNodeMap m_dofnodemap;
  typedef std::map<NodalEquation*, FuncNode*, NodalEqnCompare> EqnNodeMap;
  EqnNodeMap m_eqnnodemap;
#endif	// HAVE_MPI

  void reserveFuncNodes(int n);	// reserve space for n func nodes
  void reserveMapNodes(int n);	// reserve space for n map nodes
  void addElement(Element*);
  void reserveElements(int n);
  void reserveMoreDoFs(int n);

  void addInterfaceElement(Element*);
  int nedgements() const;
  ElementIterator edgement_iterator() const;
  // // Tell interface elements that a boundary name has changed.
  // void renameInterfaceElements(const std::string &oldname,
  // 			       const std::string &newname);

  // Caution: NodeIterator::index is not necessarily the same as
  // node.index().  The argument to FEMesh::getNode() is the
  // NodeIterator::index.
  Node *getNode(int) const;
  FuncNode *getFuncNode(int) const;

  // Temporary function for finding the closest node.
  Node *closestNode(const Coord*, double) const;

  DegreeOfFreedom *createDoF(double x=0); // only way to make a DoF
  void removeDoF(DegreeOfFreedom*);
  int ndof() const { return dof.size(); }

  // NodalEquations represent one component of one Equation at a Node.
  // They are to the rows of the stiffness matrix what the
  // DegreeOfFreedoms are to the columns.
  NodalEquation *createNodalEqn();
  void removeNodalEqn(NodalEquation*);
  int neqn() const { return nodaleqn.size(); }

  Element *getElement(int i) const;

  void refreshMaterials(CSkeletonBase*);
  // Keep track of how many Elements use each Material.
  void addMaterial(const Material*);
  void removeMaterial(const Material*);
  //  void makeMaterialLists();
  MaterialSet *getAllMaterials() const; // creates new set

  int nnodes() const;
  int nelements() const;

#if DIM==2
  // Is a field in-plane on this mesh?
  bool in_plane(const Field &field) const;
  void set_in_plane(const Field &field, bool);
#endif // DIM==2

  std::vector<std::string> *getFieldSetByID(int) const;	// returns new obj

  // API for setting/referring to the read-write lock.  Set_rwlock
  // should be called exactly once when the femesh is inserted into a
  // mesh context object.
  void set_rwlock(RWLock *rw) { rwlock = rw; };
  inline RWLock *get_rwlock() { return rwlock;};

  // For visualization
  void getGrid(double, const CSkeletonBase*, SkeletonFilter*,
	       vtkUnstructuredGrid*) const;
  vtkSmartPointer<vtkIntArray> getMaterialCellData(const CSkeletonBase*,
						   const SkeletonFilter*) const;
  
private:
  // These lists can be accessed through the MeshIterators.
  std::vector<FuncNode*> funcnode; // nodes at which dofs are defined
  std::vector<Node*> mapnode;	// nodes only used for geometry mapping
  std::vector<Element*> element;
  std::vector<Element*> edgement;
  int ncount;			// node counter, for assigning ids

  // Master lists of degrees of freedom and nodal equations
  std::vector<DegreeOfFreedom*> dof;

  std::vector<NodalEquation*> nodaleqn;
  void housekeeping();		     // do garbage collection on the lists
  bool dof_list_needs_cleaning;
  bool nodaleqn_list_needs_cleaning; // do the lists need to be cleaned up?

  // Dictionary of wrappers for Field and Equation lists stored at
  // Nodes.  See fieldeqnlist.h.
  FEWrapper<Field>::AllWrappers fieldwrappers;
  FEWrapper<Equation>::AllWrappers equationwrappers;

#if DIM==2
  std::vector<bool> in_plane_field;
#endif // DIM==2

  void clean_nodaleqn();
  void clean_doflist();

  // All materials used by the Mesh
  typedef std::map<const Material*, int, MaterialCompare> MaterialCountMap;
  MaterialCountMap materialCounts;

  struct PropCmp {
    bool operator()(const Property *a, const Property *b) const {
      return a < b;
    }
  };
  typedef std::map<const Property*, void*, PropCmp> PropertyDataMap;
  PropertyDataMap propertyDataMap;

public:
  // Routines for copying DoF values 
  void get_dofvalues(DoubleVec &x, const DoFMap&) const; // mesh -> x
  bool set_dofvalues(const DoubleVec &x, const DoFMap&,
		     const std::set<int>&); // x -> mesh

  // Retrieve the value of a single DoF. Used by FloatBC, sparingly.
  double get_dofvalue(int) const;
  void dumpDoFs(const std::string&) const; // for debugging

  // Routines for storing and retrieving Mesh specific data used by
  // Properties. 
  void set_property_data(const Property*, void*);
  void *get_property_data(const Property*) const;

  void setCurrentTime(double t);
  double getCurrentTime() const;
  CSubProblem *getCurrentSubProblem() const { return currentSubProblem_; }
  void setCurrentSubProblem(CSubProblem *subp) { currentSubProblem_ = subp; }
  void clearCurrentSubProblem() { currentSubProblem_ = 0; }

  void setDataCache(MeshDataCache*);
  void replaceDataCache(MeshDataCache*);
  void clearDataCache();
  void cacheCurrentData();
  void restoreCachedData(double);
  void restoreLatestData();
  void releaseCachedData();
  const std::vector<double> *cachedTimes() const;
  double latestTime() const;
  double earliestTime() const;
  bool atEarliest() const;
  bool atLatest() const;
  bool isEmptyCache() const;
  int dataCacheSize() const;

private:
  friend class Equation::FindAllEquationWrappers;
  friend class Field::FindAllFieldWrappers;
  friend class MeshElementIterator;
  friend class MeshFuncNodeIterator;
  friend class MeshInterfaceElementIterator;
  friend class MeshNodeIterator;
  friend class Node;
  friend class CSubProblem;
  friend class LinearizedSystem;
  friend long get_globalFEMeshCount();
  friend class DegreeOfFreedom;
  friend class MeshDataCache;
  friend class MemoryDataCache;
  friend class DiskDataCache;

  //AMR, moved to csubproblem
// Adaptive Mesh Refinement stuff.
//public:
//   // TODO 3.1: encapsulate all of the ZZ error estimation stuff, so that
//   // we can switch estimators.

//   // create & add a new CSCPatch pointer
//   void init_scpatches(const std::vector<int>*);
//   void add_scpatch(const int, const Material*, 
// 		   const int,
// 		   const std::vector<int>*,
// 		   const std::vector<int>*,
// 		   const int);
//   // getting elements & nodes from the patch
//   std::vector<int> *get_elements_from_patch(const int, const Material*);
//   std::vector<int> *get_nodes_from_patch(const int, const Material*);
//   // recovering flux(es)
//   void init_nodalfluxes();
//   void recover_fluxes();
//   // adding recovered flux
//   void add_this_flux(const Material*, const Flux*,
// 		     const Node*, VECTOR_D*);
//   // recovered flux at a given point
//   VECTOR_D *get_recovered_flux(const Flux*, const Element*,
// 			       const MasterCoord&);
//   // reporting recovered fluxes at a given point -- debug purpose
//   void report_recovered_fluxes(const Element*, const Coord*);
//   // estimating error
//   double zz_L2_estimate(const Element*, const Flux*);
//   void zz_L2_estimate_sub(const Element*, const Flux*,
// 			  const int&, double&, double&,
// 			  const MasterCoord&, const double&);
//   DoubleVec *zz_L2_weights(const Flux*,
// 				     const double&, const double&);
//   void zz_L2_weights_sub(const Element*, const Flux*,
// 			  const int&, double&,
// 			  const MasterCoord&, const double&);
//   void setDefaultSubProblem(CSubProblem*);
//private:
//   // Storage for CSCPatch's (keyed an assembly node)
//   // NodalSCPatches contains as many CSCPatches as no. of Materials
//   // at the assembly node.
//   std::map<const int, NodalSCPatches*> scpatches;
//   // Storage for SCpatch Recovered Fluxes
//   std::map<const int, NodalFluxes*> recovered_fluxes;
  // The default subproblem is passed in so that the above routines
  // can use it.  This is a temporary hack, only to be used while AMR
  // is being done in the FEMesh instead of the CSubProblem.
//   CSubProblem *defaultSubProblem;

};				// FEMesh

long get_globalFEMeshCount();

#endif // FEMESH_H
