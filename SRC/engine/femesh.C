// -*- C++ -*-
// $RCSfile: femesh.C,v $
// $Revision: 1.192.2.32 $
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
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <vector>
#include <map>
#include <algorithm>
#include <limits>

#include "common/cleverptr.h"
#include "common/coord.h"
#include "common/doublevec.h"
#include "common/printvec.h"
#include "common/smallmatrix.h"
#include "common/tostring.h"
#include "common/trace.h"
#include "common/IO/oofcerr.h"
#include "engine/cscpatch.h"
#include "engine/cskeletonelement.h"
#include "engine/csubproblem.h"
#include "engine/dofmap.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/equation.h"
#include "engine/femesh.h"
#include "engine/field.h"
#include "engine/flux.h"
#include "engine/gausspoint.h"
#include "engine/masterelement.h"
#include "engine/material.h"
#include "engine/meshdatacache.h"
#include "engine/meshiterator.h"
#include "engine/nodalequation.h"
#include "engine/node.h"
#include "engine/ooferror.h"
#include "engine/outputval.h"
#include "engine/preconditioner.h"
#include "engine/property.h"
#include "engine/skeletonfilter.h"

#include <vtkTetra.h>
#include <vtkUnstructuredGrid.h>
#include <vtkIntArray.h>
#include <vtkPointData.h>

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

long FEMesh::globalFEMeshCount = 0; // used for code testing
static SLock globalFEMeshCountLock;

FEMesh::FEMesh(CMicrostructure * mc)
  : microstructure(mc),
    rwlock(0),
    dofvalues(new DoubleVec),
    time(0.0),
    currentSubProblem_(0),
    dataCache(0),
    noCacheReadersCond(&masterCacheLock),
    nCacheReaders(0),
    ncount(0),			// used as a Node ID only
    dof_list_needs_cleaning(false),
    nodaleqn_list_needs_cleaning(false)
{
  globalFEMeshCountLock.acquire();
  ++globalFEMeshCount;
  globalFEMeshCountLock.release();
}

FEMesh::~FEMesh() {
  for(std::vector<NodalEquation*>::size_type i=0; i<nodaleqn.size(); i++)
    delete nodaleqn[i];
  
  for(std::vector<DegreeOfFreedom*>::size_type i=0; i<dof.size(); i++)
    delete dof[i];
  for(std::vector<FuncNode*>::size_type i=0; i<funcnode.size(); ++i)
    delete funcnode[i];
  for(std::vector<Node*>::size_type i=0; i<mapnode.size(); ++i)
    delete mapnode[i];
  for(std::vector<Element*>::size_type i=0; i<element.size(); ++i)
    delete element[i];
  for(std::vector<Element*>::size_type i=0; i<edgement.size(); ++i)
    delete edgement[i];
  delete dofvalues;

  // We do not own rwlock, so don't delete it.

  // Clear mesh-specific property data, if any
  for(PropertyDataMap::iterator i=propertyDataMap.begin();
      i!=propertyDataMap.end(); ++i)
    {
      (*i).first->clear_mesh_data(this, (*i).second);
    }

#ifdef HAVE_MPI
  for(NodeShareMap::iterator it=m_nodesharemap.begin();
      it!=m_nodesharemap.end();it++)
    {
      delete it->second;
    }
  m_nodesharemap.clear();
#endif
  globalFEMeshCountLock.acquire();
  --globalFEMeshCount;
  globalFEMeshCountLock.release();
  // data cache is owned by Python.  Don't delete it here.
}

const std::string &FEMesh::classname() const {
  static const std::string _name = "FEMesh";
  return _name;
}

const std::string &FEMesh::modulename() const {
  static const std::string _name = "ooflib.SWIG.engine.femesh";
  return _name;
}

long get_globalFEMeshCount() {
  return FEMesh::globalFEMeshCount;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// All Degrees of Freedom are created and deleted with these functions

DegreeOfFreedom *FEMesh::createDoF(double x) {
  int index = dof.size();
  DegreeOfFreedom *newdof = new DegreeOfFreedom(index);
  dof.push_back(newdof);
  dofvalues->push_back(x);
  return newdof;
}

void FEMesh::removeDoF(DegreeOfFreedom *deaddof) {
//   Trace("FEMesh::removeDoF");
  int index = deaddof->dofindex();
  delete deaddof;
  // Don't shift the rest of the vector entries to fill the hole
  // caused by deleting this dof.  The hole can be filled more
  // efficiently by garbage collection later.  Just make sure to check
  // for null pointers when using the dof list!
  dof[index] = 0;
  dof_list_needs_cleaning = true;
}

void FEMesh::clean_doflist() {
  if(dof_list_needs_cleaning) {
    std::vector<DegreeOfFreedom*>::size_type j=0;
    for(std::vector<DegreeOfFreedom*>::size_type i=0; i<dof.size(); i++) {
      if (dof[i] != 0) {
	if(i != j) {
	  dof[j] = dof[i];
	  (*dofvalues)[j] = (*dofvalues)[i];
	  dof[j]->index_ = j;
	}
	j++;
      }
    }
    if(j != dof.size())
      dof.resize(j);
    dof_list_needs_cleaning=false;
  }
}

void FEMesh::reserveMoreDoFs(int n) {
  dofvalues->reserve(dofvalues->size() + n);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// All NodalEquations are created and deleted with these functions

NodalEquation *FEMesh::createNodalEqn() {
//   Trace("FEMesh::createNodalEqn");
  int index = nodaleqn.size();
  NodalEquation *neweqn = new NodalEquation(index);
  nodaleqn.push_back(neweqn);
  return neweqn;
}

void FEMesh::removeNodalEqn(NodalEquation *eqn) {
//   Trace("FEMesh::removeNodalEqn");
  int index = eqn->ndq_index();
  delete eqn;
  // Don't shift the rest of the vector entries to fill the hole
  // caused by deleting this eqn.  The hole can be filled more
  // efficiently by garbage collection later.  Just make sure to check
  // for null pointers when using the nodaleqn list!
  nodaleqn[index] = 0;
  nodaleqn_list_needs_cleaning=true;
}

void FEMesh::clean_nodaleqn() {
  if(nodaleqn_list_needs_cleaning) {
    std::vector<NodalEquation*>::size_type j = 0;
    for(std::vector<NodalEquation*>::size_type i=0; i<nodaleqn.size(); i++) {
      if(nodaleqn[i] != 0) {
	if(i != j) {
	  nodaleqn[j] = nodaleqn[i];
	  nodaleqn[j]->index_ = j;
	}
	j++;
      }
    }
    if(j != nodaleqn.size())
      nodaleqn.resize(j);
    nodaleqn_list_needs_cleaning = false;
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Make sure that all dofs and nodalequations have the right indices

void FEMesh::housekeeping() {
  clean_doflist();
  clean_nodaleqn();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

Node *FEMesh::newMapNode(const Coord &pos) {
  Node *node = new Node(ncount++, pos);
  mapnode.push_back(node);
  return node;
}

FuncNode *FEMesh::newFuncNode(const Coord &pos) {
  FuncNode *node = new FuncNode(this, ncount++, pos);
  funcnode.push_back(node);
  return node;
}

#ifdef HAVE_MPI

#include "common/mpitools.h"

//procs is (pointer to) an array of process numbers that share the node.
//indices is an array of (remote) indices of the node relative to other processes.
//procs and indices are 1-1 and must have the same length.
FuncNode *FEMesh::newFuncNode_shares(const Coord &pos, std::vector<int>* procs,
				     std::vector<int>* indices, int index)
{
  FuncNode *node = new FuncNode(this, ncount++, pos);
  funcnode.push_back(node);

  if(!procs->empty() && procs->size()==indices->size())
    {
      CNodeShareInfo* cn=new CNodeShareInfo(procs, indices, index);
      node->setShared();
      m_nodesharemap[node]=cn;
      m_indexnodemap[index]=node;
    }

  return node;
}

CNodeShareInfo::CNodeShareInfo(std::vector<int>* procs,
		 std::vector<int>* indices, int index)
{
  inheritedindex=index;
  localprocrank=Rank();//from mpitools.h
//   int minrank=localprocrank;
  for(std::vector<int>::size_type i=0;i<procs->size();i++)
    {
      int pi=(*procs)[i];
      remoteproclist.push_back(pi);
//       if(localprocrank>pi)
// 	minrank=pi;
      remoteindexlist.push_back((*indices)[i]);
    }

  //bubble sort remoteproclist (make corresponding change to remoteindexlist)
  int tmp,rsize=remoteproclist.size();
  for(std::vector<int>::size_type i=0;i<rsize;i++)
    {
      for(std::vector<int>::size_type j=i+1;j<rsize;j++)
	{
	  if(remoteproclist[i]>remoteproclist[j])
	    {
	      tmp=remoteproclist[i];
	      remoteproclist[i]=remoteproclist[j];
	      remoteproclist[j]=tmp;
	      tmp=remoteindexlist[i];
	      remoteindexlist[i]=remoteindexlist[j];
	      remoteindexlist[j]=tmp;
	    }
	}
    }
  // Find next higher rank
  nextrank=-1;
  nextindex=-1;
  for(std::vector<int>::size_type i=0;i<remoteproclist.size();i++)
    {
      if(localprocrank<remoteproclist[i])
	{
	  nextrank=remoteproclist[i];
	  nextindex=remoteindexlist[i];
	  break;
	}
    }

  if(localprocrank<=remoteproclist[0])
    {
      _owns0=true;
    }
  else
    {
      _owns0=false;
    }
  owns=_owns0;
};

CNodeShareInfo::~CNodeShareInfo()
{
  //Not necessary
  remoteproclist.clear();
  remoteindexlist.clear();
  localdofindexlist.clear();
  localeqnindexlist.clear();
  symmatrixdofindexlist.clear();
  symmatrixeqnindexlist.clear();
};

#endif

void FEMesh::reserveFuncNodes(int n) {
  funcnode.reserve(n);
}

void FEMesh::reserveMapNodes(int n) {
  mapnode.reserve(n);
}

void FEMesh::reserveElements(int n) {
  element.reserve(n);
}

int FEMesh::nnodes() const {
  // don't just return ncount here, since the node index is just an
  // identifier.  When nodes are deleted, ncount won't be decreased.
  return funcnode.size() + mapnode.size();
}

void FEMesh::addElement(Element *el) {
  element.push_back(el);
  el->set_index(element.size()-1);
  if(el->material())
    addMaterial(el->material());
}

Element *FEMesh::getElement(int i) const {
  return element[i];
}

int FEMesh::nelements() const {
  return element.size();
}

FEMesh::ElementShapeCountMap *FEMesh::getElementShapeCounts() const {
  // TODO 3.1: Maybe these counts should be done when elements are added
  // or the Mesh is modified.
  FEMesh::ElementShapeCountMap *counts = new FEMesh::ElementShapeCountMap();
  std::vector<std::string> *names = shapeNames();
  // Initialize count for each shape
  for(unsigned int i=0; i<names->size(); ++i) {
    ElementShape *shape = getShape((*names)[i]);
    (*counts)[shape] = 0;
  }
  // Count elements.
  for(ElementIterator ei=element_iterator(); !ei.end(); ++ei) {
    ++(*counts)[ei.element()->masterelement().shape()];
  }
  // Count interface elements.
  for(ElementIterator ei=edgement_iterator(); !ei.end(); ++ei) {
    ++(*counts)[ei.element()->masterelement().shape()];
  }
  return counts;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void FEMesh::refreshMaterials(CSkeletonBase *skeleton) {
  for(ElementIterator ei=element_iterator(); !ei.end(); ++ei) {
    Element *el = ei.element();
    const Material *oldmat = el->material();
    el->refreshMaterial(skeleton);
    const Material *newmat = el->material();
    if(newmat != oldmat) {
      if(oldmat)
	removeMaterial(oldmat);
      if(newmat)
	addMaterial(newmat);
    }
  }
  for(ElementIterator ei=edgement_iterator(); !ei.end(); ++ei) {
    Element *el = ei.element();
    const Material *oldmat = el->material();
    el->refreshMaterial(skeleton);
    const Material *newmat = el->material();
    if (newmat != oldmat) {
      if (oldmat) 
	removeMaterial(oldmat);
      if (newmat)
	addMaterial(newmat);
    }
  }
}

void FEMesh::addMaterial(const Material *matl) {
  assert(matl != 0);
  MaterialCountMap::iterator i = materialCounts.find(matl);
  if(i == materialCounts.end())
    materialCounts[matl] = 1;
  else
    (*i).second++;
}

void FEMesh::removeMaterial(const Material *matl) {
  MaterialCountMap::iterator i = materialCounts.find(matl);
  assert(i != materialCounts.end());
  (*i).second--;
  if((*i).second == 0)
    materialCounts.erase(i);
}

MaterialSet *FEMesh::getAllMaterials() const {
  MaterialSet *matls = new MaterialSet;
  for(MaterialCountMap::const_iterator i=materialCounts.begin();
      i!=materialCounts.end(); ++i) {
    matls->insert((*i).first);
  }
  return matls;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementIterator FEMesh::element_iterator() const {
  return ElementIterator(new MeshElementIterator(this));
}

NodeIterator FEMesh::node_iterator() const {
  return NodeIterator(new MeshNodeIterator(this));
}

FuncNodeIterator FEMesh::funcnode_iterator() const {
  return FuncNodeIterator(new MeshFuncNodeIterator(this));
}

// operator[] is deprecated...
// FuncNode *FEMesh::operator[](const FuncNodeIterator &ni) const {
//   return funcnode[ni.index];
// }

// Node *FEMesh::operator[](const NodeIterator &ni) const {
//   return getNode(ni.index);
// }

// Caution: NodeIterator::index is not necessarily the same as
// node.index().  The argument to FEMesh::getNode is the
// NodeIterator::index.

Node *FEMesh::getNode(int i) const {
//   if(i >= int(funcnode.size() + mapnode.size())) {
//     std::cerr << "FEMesh::getNode: i=" << i << " fn=" << funcnode.size() 
// 	      << " mn=" << mapnode.size() << std::endl;
//   }
  assert(i < int(funcnode.size() + mapnode.size()));
  if(i < int(funcnode.size()))
    return funcnode[i];
  return mapnode[i - funcnode.size()];
}

FuncNode *FEMesh::getFuncNode(int i) const {
  return funcnode[i];
}

// Find the closest node to the mouse point.  Used in MeshInfo.
// TODO OPT: use hash table lookup here, instead of looping over all
// nodes.  Can use a vtk point locator object once the storage is set
// up, maybe.  It's not trivial because the vtkPoints object for an
// FEMesh contains duplicate Nodes.  Each one occurs once *per
// element*, so that discontinuous functions can be plotted.

Node *FEMesh::closestNode(const Coord *pos, double enhancement) const {
  // 'enhancement' is the factor that multiplies the displacement in
  // the currently plotted Mesh.
  double min=std::numeric_limits<double>::max();
  Node *closest = 0;
  for(NodeIterator ni=node_iterator(); !ni.end(); ++ni) {
    Coord nodepos = ni.node()->displaced_position(this, enhancement);
    double dist2 = norm2(nodepos - *pos);
    if(dist2 < min) {
      closest = ni.node();
      min = dist2;
    }
  }
  return closest;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// get_dofvalues() and set_dofvalues() copy values to and from a
// SubProblem's list of dofvalues.  They can't use DoFMap.extract()
// and DoFMap.inject() because the data isn't stored in a vector on
// the FEMesh side.  TODO OPT: Yes it is.  Can this be done more
// efficiently?

// Copy values from the mesh into the given vector x.  Only called by
// CSubProblem::get_meshdofs().

void FEMesh::get_dofvalues(DoubleVec &x, const DoFMap &mesh2subpDoFMap) const {
  for(unsigned int i=0; i<mesh2subpDoFMap.domain(); i++) {
    int j = mesh2subpDoFMap[i];
    if(j != -1) {
      x[j] = dof[i]->value(this);
    }
  }
}

// Copy values from the given vector x back into the mesh.  This
// function *must* use the mesh-to-subproblem map, rather than the
// inverse, because the mesh-to-subproblem map is many-to-one if there
// are floating boundary conditions, and we need all dofs in a FloatBC
// to be updated.

// Only called by CSubProblem::set_meshdofs().

bool FEMesh::set_dofvalues(const DoubleVec &x, const DoFMap &mesh2subpmap,
			   const std::set<int> &exclusions)
{
  bool changed = false;
  for(DoubleVec::size_type i=0; i<mesh2subpmap.domain(); i++) {
    int j = mesh2subpmap[i];
    if(j != -1 && exclusions.find(j)==exclusions.end()) {
      double &val = dof[i]->value(this);
      changed |= (val != x[j]);
      val = x[j];
    }
  }
  return changed;
}

double FEMesh::get_dofvalue(int idx) const {
  return dof[idx]->value(this);
}

void FEMesh::dumpDoFs(const std::string &filename) const {
  std::ofstream os(filename.c_str(), std::ios::app);
  os << "FEMesh::dumpDoFs: " << *dofvalues << std::endl;
  os.close();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void FEMesh::setCurrentTime(double t) {
  time = t;
}

double FEMesh::getCurrentTime() const {
  return time; 
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void FEMesh::setDataCache(MeshDataCache *cache) {
  dataCache = cache;
  dataCache->setMesh(this);
}

void FEMesh::replaceDataCache(MeshDataCache *newcache) {
  newcache->setMesh(this);
  newcache->transfer(dataCache);
  dataCache = newcache;
}

void FEMesh::clearDataCache() {
  masterCacheLock.acquire();
  try {
    dataCache->clear();
  }
  catch (...) {
    masterCacheLock.release();
    throw;
  }
  masterCacheLock.release();
}

void FEMesh::cacheCurrentData() {
  masterCacheLock.acquire();
  try {
    dataCache->record();
  }
  catch (...) {
    masterCacheLock.release();
    throw;
  }
  masterCacheLock.release();
}

void FEMesh::restoreCachedData(double restoretime) {
  masterCacheLock.acquire();
  try {
    if(restoretime == getCurrentTime() and not dataCache->atLatest()) {
      nCacheReaders += 1;
    }
    else {
      // Release masterCacheLock, Wait until there are no cache
      // readers, and reacquire masterCacheLock.
      while(nCacheReaders > 0) {
	noCacheReadersCond.wait();
      }
      dataCache->interpolate(restoretime); // sets FEMesh::time
      nCacheReaders = 1;
    }
  }
  catch (...) {
    masterCacheLock.release();
    throw;
  }
  masterCacheLock.release();
}

void FEMesh::restoreLatestData() {
  masterCacheLock.acquire();
  try {
    if(atLatest())
      nCacheReaders += 1;
    else {
      while(nCacheReaders > 0) {
	noCacheReadersCond.wait();
      }
      // restoreLatest() is a no-op, if nothing has been cached yet.
      // Otherwise it sets FEMesh::time and FEMesh::dofvalues.
      dataCache->restoreLatest();
      nCacheReaders = 1;
    }
  }
  catch (...) {
    masterCacheLock.release();
    throw;
  }
  masterCacheLock.release();
}

void FEMesh::releaseCachedData() {
  masterCacheLock.acquire();
  try {
    nCacheReaders -= 1;
    if(nCacheReaders == 0) {
      noCacheReadersCond.broadcast();
    }
  }
  catch (...) {
    masterCacheLock.release();
    throw;
  }
  masterCacheLock.release();
}

const std::vector<double> *FEMesh::cachedTimes() const {
  if(dataCache)
    return dataCache->times();
  return 0;
}

double FEMesh::latestTime() const {
  if(!dataCache)
    return 0.0;
  return dataCache->latestTime();
}

double FEMesh::earliestTime() const {
  if(!dataCache)
    return 0.0;
  return dataCache->earliestTime();
}

bool FEMesh::atEarliest() const {
  if(!dataCache)
    return true;
  return dataCache->atEarliest();
}

bool FEMesh::atLatest() const {
  if(!dataCache)
    return true;
  return dataCache->atLatest();
}

bool FEMesh::isEmptyCache() const {
  if(!dataCache)
    return true;
  return dataCache->empty();
}

int FEMesh::dataCacheSize() const {
  if(!dataCache)
    return 0;
  return dataCache->size();
}


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#if DIM==2

void FEMesh::set_in_plane(const Field &field, bool planarity) {
  if(field.index() >= in_plane_field.size())
    in_plane_field.resize(field.index()+1);
  in_plane_field[field.index()] = planarity;
}

bool FEMesh::in_plane(const Field &field) const {
  return (field.index() < in_plane_field.size()
	  && in_plane_field[field.index()]);
}
#endif // DIM==2

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Return a list of Field names, in the order in which they were
// defined, for the FieldSet with the given id.

std::vector<std::string> *FEMesh::getFieldSetByID(int id) const {
  // Loop over all FEWrappers to find the one with this id. 
  for(FEWrapper<Field>::AllWrappers::const_iterator i=fieldwrappers.begin();
      i!=fieldwrappers.end(); ++i)
    {
      if((*i).second->id() == id) {
	FEWrapper<Field> &wrapper = *(*i).second;
	FEWrapper<Field>::FEvector &datalist = (*i).second->datalist;
	std::vector<std::string> *fieldnames = 
	  new std::vector<std::string>(wrapper.size);
	for(FEWrapper<Field>::FEvector::size_type f=0; f<datalist.size(); f++) {
	  if(datalist[f].order >= 0) {
	    (*fieldnames)[datalist[f].order] = getFieldByIndex(f)->name();
	  }
	}
	return fieldnames;
      }
    }
  throw ErrProgrammingError("Couldn't find FieldSet", __FILE__, __LINE__);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Routines for storing and retrieving data on behalf of the
// Properties.  Since Properties are shared between Meshes (although
// not between Materials) there must be a generic way for them to
// store precomputed mesh-dependent properties.

void FEMesh::set_property_data(const Property *property, void *data) {
  PropertyDataMap::iterator i = propertyDataMap.find(property);
  if(i != propertyDataMap.end()) {
    property->clear_mesh_data(this, (*i).second);
    propertyDataMap.erase(i);
  }
  propertyDataMap[property] = data;
}

void *FEMesh::get_property_data(const Property *property) const {
  PropertyDataMap::const_iterator i = propertyDataMap.find(property);
  if(i != propertyDataMap.end())
    return (*i).second;
  return 0;
}

//////////////////////////////////////////////

void FEMesh::addInterfaceElement(Element *ed) {
  edgement.push_back(ed);
  // Caution! This assumes that bulk elements get added before
  // interface elements.
  ed->set_index(element.size()+edgement.size()-1);
  if(ed->material()) 
    addMaterial(ed->material());
}

int FEMesh::nedgements() const
{
  return edgement.size();
}

ElementIterator FEMesh::edgement_iterator() const
{
  return ElementIterator(new MeshInterfaceElementIterator(this));
}

// void FEMesh::renameInterfaceElements(const std::string &oldname,
// 				     const std::string &newname)
// {
//   for(ElementIterator ei=edgement_iterator(); !ei.end(); ++ei)
//     ((InterfaceElement*)(ei.element()))->rename(oldname,newname);
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO OPT: getGrid and getMaterialCellData need to loop over the
// elements in the same order using element_iterator and the given
// filter.  They should share code.  Possibly the iterator should take
// the filter as an argument.

// TODO 3.1: Does this handle split nodes correctly?

void FEMesh::getGrid(
	     double factor, const CSkeletonBase *skel, 
	     SkeletonFilter *filter,
	     vtkUnstructuredGrid *grid)
  const 
{
  // 'factor' multiplies the displacement field, if it's defined.

  // 'filter' is *not* a const argument, because this routine modifies
  // the map between vtk and element indices, which is stored in the
  // filter.

  // TODO OPT: Allow higher order elements.  This version assumes linear
  // tets.

  grid->Initialize();
  filter->resetMap();

  vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();

  points->Allocate(element.size()*4, element.size()*4);
  grid->Allocate(element.size(), element.size());
  grid->SetPoints(points);

  for(ElementIterator ei=element_iterator(); !ei.end(); ++ei) {
    Element *el = ei.element();
    CSkeletonElement *skelel = el->get_skeleton_element();
    if(filter->acceptable(skelel, skel)) {
      vtkIdType ids[4];
      int j = 0;
      for(CleverPtr<ElementFuncNodeIterator> node(el->funcnode_iterator());
	  !node->end(); ++*node)
	{
	  // TODO OPT: This inserts each node once per element, which uses
	  // a lot more memory than necessary.  Is this bad?  If the
	  // grid is being used for contour plots, it has to be done
	  // this way because that's the way that the Output classes
	  // work.  It is also required if nodes are split or plotted
	  // data is discontinuous.
	  int nidx = points->InsertNextPoint(
	     node->funcnode()->displaced_position(this, factor).xpointer());
	  ids[j++] = nidx;
	}
      vtkIdType cellID = grid->InsertNextCell(VTK_TETRA, 4, ids);
      // Keep track of the correspondence between element indices and
      // vtk cell IDs.  This information is used by
      // findClickedCellID() in ghostgfxwindow.py.
      filter->mapCellIndex(cellID, el->get_index());
    }
  }
  // oofcerr << "FEMesh::getGrid: " << points->GetNumberOfPoints()
  // 	  << " nodes" << std::endl;
}

vtkSmartPointer<vtkIntArray> FEMesh::getMaterialCellData(
		 const CSkeletonBase *skel, const SkeletonFilter *filter)
  const 
{
  vtkSmartPointer<vtkIntArray> array = vtkSmartPointer<vtkIntArray>::New();
  for(ElementIterator ei=element_iterator(); !ei.end(); ++ei) {
    Element *el = ei.element();
    CSkeletonElement *skelel = el->get_skeleton_element();
    if(filter->acceptable(skelel, skel)) {
      int cat = skelel->dominantPixel(get_microstructure());
      array->InsertNextValue(cat);
    }
  }
  return array;
}
