// -*- C++ -*-
// $RCSfile: cskeleton2.swg,v $
// $Revision: 1.1.4.87 $
// $Author: langer $
// $Date: 2014/12/14 01:07:47 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


// TODO 3.1: remove functions that are not called from Python!

#ifndef CSKELETON2_SWG
#define CSKELETON2_SWG

%module cskeleton

%include "engine/typemaps.swg"
%extern "engine/cskeletonselectable.swg"
%extern "engine/cskeletonnode2.swg"
%extern "engine/cskeletonsegment.swg"
%extern "engine/cskeletonface.swg"
%extern "engine/cskeletonelement.swg"
%extern "engine/cskeletonboundary.swg"
%extern "engine/element.swg"
%extern "engine/femesh.swg"
%extern "common/cmicrostructure.swg"
%extern "common/timestamp.swg"
%extern "common/IO/ghostoofcanvas.swg"
%{
#include <oofconfig.h>
#include "common/IO/vtkutils.h"
#include "common/cmicrostructure.h"
#include "common/timestamp.h"
#include "common/tostring.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonboundary.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeletonselectable.h"
%}

%pragma(python) include="engine/cskeleton2.spy"

%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkDataArrayPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkPointsPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.IO.vtkutils import vtkUnstructuredGridPtrPtr"
%pragma(python) code="from ooflib.SWIG.common.cmicrostructure import CMicrostructurePtr"
%pragma(python) code="from ooflib.SWIG.common.timestamp import TimeStampPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonboundary import CSkeletonEdgeBoundaryPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonboundary import CSkeletonFaceBoundaryPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonboundary import CSkeletonPointBoundaryPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonelement import CSkeletonElementPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonelement import CSkeletonElementIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonface import CSkeletonFacePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonface import CSkeletonFaceIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonface import OrientedCSkeletonFacePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonnode2 import CSkeletonNodePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonnode2 import CSkeletonNodeIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonsegment import CSkeletonSegmentPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonsegment import CSkeletonSegmentIteratorPtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonMultiNodeSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonselectable import CSkeletonSelectablePtr"
%pragma(python) code="from ooflib.SWIG.engine.femesh import FEMeshPtr"

// Convert a C++ std::list of CDeputySkeletons to a python list.
%typemap(python,out) CDeputySkeletonList* {
  // typemap(python, out) CDeputySkeletonList*
  static PyObject *cDeputySkeletonClass = 0;
  if(!cDeputySkeletonClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.cskeleton2");
    cDeputySkeletonClass = PyObject_GetAttrString(module, "CDeputySkeletonPtr");
    Py_XDECREF(module);
    if(!cDeputySkeletonClass) return 0;
  }
  CDeputySkeletonList::size_type sz = $source->size();
  assert((int) sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  char _ptemp[128];
  int i=0;
  for(CDeputySkeletonList::iterator it=$source->begin(); it!=$source->end();
      ++it, ++i) 
    {
      SWIG_MakePtr(_ptemp, (char*)(*it), "_CDeputySkeleton_p");
      PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
      PyObject *cds = PyObject_CallObject(cDeputySkeletonClass, swigthis);
      Py_XDECREF(swigthis);
      PyList_SET_ITEM($target, (Py_ssize_t)i, cds);
    }
}

// Convert the Python Arrangement Enum (cskeleton2.spy) to a C++
// TetArrangement enum (cskeleton2.h).
%typemap(python, in) TetArrangement* (TetArrangement arr) {
  // typemap(python, in) TetArrangement*
  static PyObject *ArrangementClass = 0;
  if(!ArrangementClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.cskeleton2");
    ArrangementClass = PyObject_GetAttrString(module, "Arrangement");
    Py_XDECREF(module);
    if(!ArrangementClass) return 0;
  }
  if(PyObject_IsInstance($source, ArrangementClass)) {
    PyObject *enum_name = PyObject_GetAttrString($source, "name");
    std::string s = PyString_AsString(enum_name);
    if(s == "middling")
      arr = MIDDLING_ARRANGEMENT;
    else if(s == "moderate")
      arr = MODERATE_ARRANGEMENT;
    else {
      PyErr_SetString(PyExc_TypeError,
		      "Type error in TetArrangement* typemap.");
      return NULL;
    }
  }
  $target = &arr;
 }

typedef unsigned long uidtype;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeletonBase {
public:
  uidtype getUid();
  void activate();
  bool illegal();
  void setIllegal();
  void incrementTimestamp();
  const TimeStamp &getTimeStamp();
  // void updateGeometry();
  void cleanUp();
  void destroy();
  void needsHash();

  CMicrostructure *getMicrostructure();
  // vtkUnstructuredGridPtr getGrid();
  void getVtkCells(SkeletonFilter*, vtkUnstructuredGridPtr);
  vtkDataArrayPtr getMaterialCellData(SkeletonFilter*);
  vtkDataArrayPtr getEnergyCellData(double, SkeletonFilter*);
  vtkPointsPtr getPoints();

  const string &getElementType(int eidx);
  CSkeletonNode *getNode(int);
  bool hasNode(CSkeletonNode*);
  CSkeletonElement *getElement(int);
  bool hasElement(CSkeletonElement*);
  CSkeletonSegment *getSegmentByUid(uidtype);
  CSkeletonFace *getFaceByUid(uidtype);
  CSkeletonSegment* findExistingSegment(CSkeletonNode*, CSkeletonNode*);
  bool doesSegmentExist(CSkeletonNode*, CSkeletonNode*);
  CSkeletonFace *findExistingFace(CSkeletonNode*, CSkeletonNode*,
				  CSkeletonNode*);
  CSkeletonFace *findExistingFaceByIds(vtkIdListPtr);
  OrientedCSkeletonFace *createOrientedFace(CSkeletonNode*, CSkeletonNode*,
					    CSkeletonNode*);

  // beginXXX and endXXX are swigged so that they can be used in
  // PySkeletonXXXIterator (defined in cskeleton2.spy). 
  CSkeletonNodeIterator beginNodes();
  CSkeletonNodeIterator endNodes();
  CSkeletonSegmentIterator beginSegments();
  CSkeletonSegmentIterator endSegments();
  CSkeletonFaceIterator beginFaces();
  CSkeletonFaceIterator endFaces();
  CSkeletonElementIterator beginElements();
  CSkeletonElementIterator endElements();

  int nnodes();
  int nelements();
  int nsegments();
  int nfaces();
  double volume();

  bool getPeriodicity(int dim);
  int getIllegalCount();
  int getSuspectCount();
  void checkIllegality();

  int nDeputies();

  void nodesAddGroupsDown(CGroupTrackerVector*);
  void segmentsAddGroupsDown(CGroupTrackerVector*);
  void facesAddGroupsDown(CGroupTrackerVector*);
  void elementsAddGroupsDown(CGroupTrackerVector*);

  CSkeletonPointBoundary *makePointBoundary(
	    char *name, CSkeletonNodeVector *nodes, bool exterior=false);
  CSkeletonEdgeBoundary *makeEdgeBoundary(
	  char *name, CSkeletonSegmentVector *segs, CSkeletonNode *n,
	  bool exterior=false);
  CSkeletonEdgeBoundary *makeEdgeBoundary3D(
	    char *name, SegmentSequence*, bool exterior=false);
  CSkeletonFaceBoundary *makeFaceBoundary(
	  char *name, OrientedSurface *takeOwnership, bool exterior=false);


  double getHomogeneityIndex();
  double energyTotal(double alpha);
  // void clearElementHomogeneityCache();

  CSkeletonElement* enclosingElement(Coord *Point);
  CSkeletonElement* findElement(vtkCellPtr);
  CSkeletonNode* nearestNode(Coord *Point);
  CSkeletonSegment* nearestSegment(Coord *Point);
  CSkeletonFace* nearestFace(Coord *Point);

  %addmethods {
    // we need to return pointers here, instead of references

    // TODO OPT: Why are these defined here, instead of being actual C++
    // class members?
    %new CSkeletonElementVector *getSegmentElements(CSkeletonSegment *segment) {
      CSkeletonElementVector *els = new CSkeletonElementVector;
      self->getSegmentElements(segment, *els);
      return els;
    }
    %new CSkeletonElementVector *getFaceElements(CSkeletonFace *face) {
      CSkeletonElementVector *els = new CSkeletonElementVector;
      self->getFaceElements(face, *els);
      return els;
    }
    %new CSkeletonFaceSet *getNodeFaces(CSkeletonNode *node) {
      CSkeletonFaceSet *faces = new CSkeletonFaceSet;
      self->getNodeFaces(node, *faces);
      return faces;
    }
    %new CSkeletonFaceVector *getSegmentFaces(CSkeletonSegment *seg) {
      CSkeletonFaceVector *faces = new CSkeletonFaceVector;
      self->getSegmentFaces(seg, *faces);
      return faces;
    }
    %new CSkeletonSegmentSet *getFaceSegments(CSkeletonFace *face) {
      CSkeletonSegmentSet *segs = new CSkeletonSegmentSet;
      self->getFaceSegments(face, *segs);
      return segs;
    }
    %new CSkeletonSegmentSet *getNodeSegments(CSkeletonNode *node) {
      CSkeletonSegmentSet *segs = new CSkeletonSegmentSet;
      self->getNodeSegments(node, *segs);
      return segs;
    }
    %new CSkeletonNodeSet *getNeighborNodes(CSkeletonNode *node) {
      CSkeletonNodeSet *nodes = new CSkeletonNodeSet;
      self->getNeighborNodes(node, *nodes);
      return nodes;
    }
    %new CSkeletonElementVector *getIllegalElements() {
      CSkeletonElementVector *baddies = new CSkeletonElementVector;
      self->getIllegalElements(*baddies);
      return baddies;
    }

    // getSegmentByNodeIndices() and getFaceByNodeIndices() are used
    // when loading Skeleton groups from a data file.
    CSkeletonSegment *getSegmentByNodeIndices(int i, int j) {
      // It's necessary to get the Node from the index here, and pass
      // the Node to the CSkeletonMultiNodeSelectable constructor
      // instead of trying to short circuit the calculation and create
      // a constructor that takes the indices as arguments, because
      // the CSkeletonMultiNodeSelectable uses uids, not indices, and
      // they might not be the same.
      CSkeletonMultiNodeKey key(self->getNode(i), self->getNode(j));
      return self->getSegment(key);
    }

    CSkeletonFace *getFaceByNodeIndices(int i, int j, int k) {
      CSkeletonMultiNodeKey key(self->getNode(i), self->getNode(j),
				self->getNode(k));
      return self->getFace(key);
    }

  }
  %new CSkeletonFaceVector *getElementFaces(CSkeletonElement*);
  %new CSkeletonSegmentVector *getElementSegments(CSkeletonElement*);
  %new ConstCSkeletonElementSet *getElementNeighbors(CSkeletonElement*);

  CSkeletonElement *getOrientedSegmentElement(OrientedCSkeletonSegment *seg);
  CSkeletonElement *getOrientedFaceElement(OrientedCSkeletonFace *face);

  CSkeletonBoundaryMap *getPointBoundaries();
  CSkeletonBoundaryMap *getEdgeBoundaries();
  CSkeletonBoundaryMap *getFaceBoundaries();

  %new string *compare(CSkeletonBase*, double);

  bool onOuterFace(CSkeletonNodeVector *nodes);
  bool checkExteriorSegments(CSkeletonSegmentVector*);
  bool checkExteriorFaces(CSkeletonFaceVector*);

  CDeputySkeleton *deputyCopy();
  CSkeleton *completeCopy();
  CSkeleton *sheriffSkeleton();

  //FEMesh *femesh();
  void populate_femesh(FEMesh *fem, Material *mat=NULL);

  %new string *sanityCheck();

  //void destroy_meshes();
  //void destroy(PyObject*);
  //bool destroyed();
}; // class CSkeletonBase

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CSkeleton : public CSkeletonBase { 

public:
  // Creation and destruction is done entirely in C++.  The
  // constructor and destructor should *not* be swigged, so that python
  // never has ownership of a CSkeleton.

  void createPointGrid(int m, int n, int l);
  void createTetra(TetArrangement *arrangement, int m, int n, int l);
  void addNode(double doubleDIMArray[3]);
  %addmethods{
    void loadElement(PyObject *nodes) {
      vtkIdType nidxs[4];
      for(int i=0; i<4; ++i)
	nidxs[i] = PyInt_AsLong(PyTuple_GET_ITEM(nodes, (Py_ssize_t) i));
      self->createElement(VTK_TETRA,4,nidxs);
    }
    // __repr__ must be defined in the derived class, not the base
    // class, because if there's no derived class method swig will
    // generate the default __repr__, which we don't want.
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }

  int getNodeUid(int nidx);
  int getElementUid(int eidx);

  void removeBoundary(char *name);
  void renameBoundary(char *oldname, char *newname);

  CDeputySkeletonList *getDeputyList();
  void removeDeputy(CDeputySkeleton *dep);

}; // class CSkeleton

CSkeleton *newCSkeleton(CMicrostructure*, bool *boolDIMArray);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class CDeputySkeleton : public CSkeletonBase { 
public:
  // Creation and destruction is done entirely in C++.  The
  // constructor and destructor should *not* be swigged, so that python
  // never has ownership of a CDeputySkeleton.

  void moveNodeTo(CSkeletonNode *node, double doubleDIMArray[3]);
  void moveNodeBy(CSkeletonNode *node, double doubleDIMArray[3]);
  %addmethods{
    // __repr__ must be defined in the derived class, not the base
    // class, because if there's no derived class method swig will
    // generate the default __repr__, which we don't want.
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

CDeputySkeleton *newCDeputySkeleton(CSkeletonBase*);

// class DeputyProvisionalChanges {

// public:
//   DeputyProvisionalChanges(CDeputySkeleton *deputy);
//   bool illegal();
//   void removeAddedNodes();
//   double deltaE(double alpha);
//   void accept();
// };

#endif




