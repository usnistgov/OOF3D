// -*- C++ -*-
// $RCSfile: femesh.swg,v $
// $Revision: 1.83.2.18 $
// $Author: langer $
// $Date: 2014/09/22 21:01:04 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef FEMESH_SWG
#define FEMESH_SWG

%module femesh

%include "engine/typemaps.swg"
%extern "common/IO/vtkutils.swg"
%extern "common/cmicrostructure.swg"
%extern "common/doublevec.swg"
%extern "common/lock.swg"
%extern "common/timestamp.swg"
%extern "engine/cskeleton2.swg"
%extern "engine/element.swg"
%extern "engine/field.swg"
%extern "engine/meshiterator.swg"
%extern "engine/node.swg"

%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkIntArrayPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkUnstructuredGridPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.lock import LockPtr"
%pragma(python) code="from ooflib.SWIG.common.lock import RWLockPtr"
%pragma(python) code="from ooflib.SWIG.engine.element import ElementPtr"
%pragma(python) code="from ooflib.SWIG.engine.field import FieldPtr"
%pragma(python) code="from ooflib.SWIG.engine.meshiterator import ElementIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.meshiterator import FuncNodeIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.meshiterator import NodeIteratorPtr"

%typemap(python, out) ElementShapeCountMap* {
   // typemap(python, out) ElementShapeCountMap
   FEMesh::ElementShapeCountMap::size_type sz = $source->size();
   assert((int)sz >= PY_SSIZE_T_MIN && (int) sz <= PY_SSIZE_T_MAX);
   $target = PyDict_New();
   for(FEMesh::ElementShapeCountMap::const_iterator i=$source->begin();
       i!=$source->end(); ++i)
     {
       const std::string &shapename = (*i).first->name();
       int count = (*i).second;
       PyDict_SetItemString($target, shapename.c_str(), PyInt_FromLong(count));
     }
}

%{
#include "common/IO/vtkutils.h"
#include "engine/csubproblem.h"
#include "engine/femesh.h"
#include "engine/node.h"
#include "engine/field.h"
#include "engine/nodalequation.h"
#include "engine/meshiterator.h"
typedef FEMesh::ElementShapeCountMap ElementShapeCountMap;
%}

%pragma(python) include="femesh.spy"



class FEMesh {
public:
  FEMesh(CMicrostructure*);
  ~FEMesh();


  void refreshMaterials(CSkeletonBase*);
  void addMaterial(Material*);
  void removeMaterial(Material*);
  %new MaterialSet *getAllMaterials();

  Node *newMapNode(Coord&);
  FuncNode *newFuncNode(Coord&);
#ifdef HAVE_MPI
  FuncNode *newFuncNode_shares(Coord&,IntVec*,IntVec*,int);
#endif
  Node *getNode(int i);
  FuncNode *getFuncNode(int);
  Node *closestNode(Coord*, double);

  void reserveFuncNodes(int);
  void reserveMapNodes(int);

  void addElement(Element*);
  Element *getElement(int i);
  void reserveElements(int);

  int nelements();
  int nnodes();
  %new ElementShapeCountMap *getElementShapeCounts();

  void addInterfaceElement(Element*);
  int nedgements();
  ElementIterator edgement_iterator();
  // void renameInterfaceElements(char* oldname, char* newname);

#ifndef DIM_3
  bool in_plane(Field&);
  void set_in_plane(Field&, bool);
#endif // !DIM_3

  ElementIterator element_iterator();
  NodeIterator node_iterator();
  FuncNodeIterator funcnode_iterator();

  void set_rwlock(RWLock *rw);
  RWLock * get_rwlock();

  void setCurrentTime(double);
  double getCurrentTime();

  void setCurrentSubProblem(CSubProblem*);
  void clearCurrentSubProblem();

  double get_dofvalue(int);
  void dumpDoFs(char*);		// for debugging

  %new StringVec *getFieldSetByID(int);

  void getGrid(double, CSkeletonBase*, SkeletonFilter*, vtkUnstructuredGridPtr);
  vtkIntArrayPtr getMaterialCellData(CSkeletonBase*, SkeletonFilter*);

  void setDataCache(MeshDataCache*);
  void replaceDataCache(MeshDataCache*);
  void clearDataCache();
  void cacheCurrentData();
  void restoreCachedData(double);
  void restoreLatestData();
  void releaseCachedData();
  DoubleList *cachedTimes();
  double latestTime();
  double earliestTime();
  bool atEarliest();
  bool atLatest();
  bool isEmptyCache();
  int dataCacheSize();
};				// class FEMesh

long get_globalFEMeshCount();

#endif // FEMESH_SWG
