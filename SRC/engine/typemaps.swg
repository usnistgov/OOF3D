// -*- C++ -*-
// $RCSfile: typemaps.swg,v $
// $Revision: 1.46.2.41 $
// $Author: langer $
// $Date: 2014/11/05 16:54:35 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// TODO MER: This file has too many #include statements, which end up in
// every swig-generated C file.  This file should be broken up.

// GENERIC TYPEMAPS

// In these comments, "[x]" means a Python list of objects of type x

// DON'T ADD TYPEMAPS TO THIS FILE WITHOUT ADDING THEM TO THIS LIST
// Unnamed typemaps defined in this file:

// in           NodeVec*        [Node] -> std::vector<Node*>*
// in		MasterCoordVec* [MasterCoord] -> std::vector<MasterCoord*>*
// in		PyObjectVec*	[anything] -> std::vector<PyObject*>*
// in		SpaceIndex*	SpaceComponent -> SpaceIndex
// out          GaussPointVec*  std::vector<GaussPoint*> -> [GaussPoint]
// newfree      GaussPointVec*  deletes vector
// out		FluxVec*	std::vector<Flux*> -> [Flux derived class obj]
// out		SymmMatrix3StarVec* std::vector<SymmMatrix3*> -> [SymmMatrix3]
// out		Flux*		Flux* -> Flux derived class obj
// out		EdgeVec*	std::vector<Edge*> -> [Edge]
// out		OutputValueVec* std::vector<OutputValue>* -> [OutputVal]
// out		DOUBLELIST*	DOUBLELIST* -> [double]
// newfree      DOUBLELIST*
// out		CompoundFieldVec* std::vector<CompoundField*>* ->[CompoundField]
// out          Material*       returns original Material, not newly wrapped Ptr
// out          MaterialVec*    std::vector<Material*> -> [original Material]
// newfree      MaterialVec*    deletes std::vector
// out          MaterialSet*    std::set<Material*> -> set(original Material)
// newfree      MaterialSet*    deletes std::set
// out          NodeSet*        std::set<Node*> -> set(Node)
// newfree      NodeSet*
// in           ElementVec*    [Element] -> std::vector<Element*>*

// COMMENTED OUT: See below.
// out		MasterCoordVec* std::vector<MasterCoord*> -> [MasterCoord]
// newfree      MasterCoordVec* deletes vector


// in    CSkeletonNodeVector*  [CSkeletonNode] -> std::vector<CSkeletonNode*>*
// in    CSkeletonSegmentVector*  [CSkeletonSegment] -> std::vector<CSkeletonSegment*>*
// in    CSkeletonFaceVector* [CSkeletonFace] -> std::vector<CSkeletonFace*>*
// out   CSkeletonNodeVector*  std::vector<CSkeletonNode*>* -> [CSkeletonNode]
// out   CSkeletonFaceVector*  std::vector<CSkeletonFace*>* -> [CSkeletonFace]
// out   CSkeletonElementVector* std::vector<CSkeletonElement*>* -> [CSkeletonElement]
// out   CSkeletonSegmentVector* std::vector<CSkeletonSegment*>* -> [CSkeletonSegment]
// out   CSkeletonSelectableSet* std::set<CSkeletonSelectable*>* -> Set(CSkeletonSelectable)
// out   CSkeletonSelectableList* std::list<CSkeletonSelectable*>* -> [CSkeletonSelectable]
// in    CSkeletonSelectableList* [CSkeletonSelectable] -> std::list<CSkeletonSelectable>
// in    CSelectionTrackerVector* [CSelectionTracker] -> std::vector<CSelectionTracker*>* 
// in    CPinnedNodeTrackerVector* [CPinnedNodeTracker] -> std::vector<CPinnedNodeTracker*>* 
// in    CGroupTrackerVector* [CGroupTracker] -> std::vector<CGroupTracker*>* 
// out   CSkeletonSegmentMap* std::map<int, CSkeletonSegment*> -> [CSkeletonSegment]
// out   CSkeletonFaceMap* std::map<int, CSkeletonFace*> -> [CSkeletonFace]
// // out   CDeputySkeletonList* std::list<CDeputySkeleton*>* -> [CDeputySkeletonElement]

// TODO 3.1: Change this to a python set?  Whether or not that's a
// good idea depends on how it's used.
// out   CSkeletonElementSet* std::set<CSkeletonElement*>* -> [CSkeletonElement]
// in    CSkeletonNodeSet*  Set(CSkeletonNode) -> std::set<CSkeletonNode*>*
// out   CSkeletonNodeSet* std::set<CSkeletonNode*>* -> Set(CSkeletonNode)
// out   CSkeletonFaceSet* std::set<CSkeletonFace*>* -> Set(CSkeletonFace)
// out   CSkeletonSegmentSet* std::set<CSkeletonSegment*> -> Set(CSkeletonSegment)
// out   CSkeletonBoundaryMap* std::map<std::string, CSkeletonBoundary> -> dict[string, CSkeletonBoundary]
// out   OrientedCSkeletonSegmentSet* std::set<OrientedCSkeletonSegment*>* -> Set(OrientedCSkeletonSegment)
// out   OrientedCSkeletonFaceSet* std::set<OrientedCSkeletonFace*>* -> Set(OrientedCSkeletonFace)
// in    OrientedCSkeletonFaceSet* [OrientedCSkeletonFace] -> std::set<OrientedCSkeletonFace*>*


// Named typemaps:
// in		MasterCoord *Point	Point->MasterCoord

// Obsolete typemaps, commented out below:
// out		VecVec*		std::vector<std::vector<double>*> -> [[Float]]
// newfree      VecVec*         deletes vector
// out		DoubleStarVec*  std::vector<const double*> -> [Float]


#ifndef ENGINETYPEMAPS_SWG
#define ENGINETYPEMAPS_SWG

%include "common/typemaps.swg"


// Typemap for converting a std::vector<GaussPoint*> to a Python list
// of GaussPointPtr objects.  The vector contains new GaussPoints, so
// Python takes ownership of the objects.

%{
#include "engine/gausspoint.h"
typedef std::vector<GaussPoint*> GaussPointVec;
%}

%typemap(python,out) GaussPointVec* {
  // typemap(python,out) GaussPointVec*
  static PyObject *gaussPointClass = 0;
  static PyObject *pyOne;
  if(!gaussPointClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.gausspoint");
    gaussPointClass = PyObject_GetAttrString(module, "GaussPointPtr");
    Py_XDECREF(module);
    if(!gaussPointClass) return 0;
    pyOne = PyInt_FromLong(1);
  }
  GaussPointVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  char _ptemp[128];
  for(std::vector<GaussPoint*>::size_type i=0; i<sz; i++) {
    // Create wrapped swig object.
    SWIG_MakePtr(_ptemp, (char*)(*$source)[i], "_GaussPoint_p");
    PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
    PyObject *gp = PyObject_CallObject(gaussPointClass, swigthis);
    Py_XDECREF(swigthis);
    // Take ownership.
    PyObject_SetAttrString(gp, "thisown", pyOne);
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, gp); // Steals reference.
  }
}

%typemap(python,newfree) GaussPointVec* {
  // typemap(python,newfree) GaussPointVec*
  delete $source;
}


// Typemap for converting a std::vector<MasterCoord*> to a List of
// MasterCoords. Python takes over ownership of the MasterCoords.
%{
#include "engine/mastercoord.h"
#include <vector>
  typedef std::vector<MasterCoord*> MasterCoordVec;
%}

// The MasterCoordVec* "out" and "newfree" typemaps are commented out
// because they don't seem to be used, and if they're not used it's
// not clear if the "out" typemap should take ownership of the
// MasterCoord*s or not.

// %typemap(python,out) MasterCoordVec* {
//   // typemap(python,out) MasterCoordVec*
//   static PyObject *masterCoordClass = 0;
//   static PyObject *pyOne = 0;
//   if(!masterCoordClass) {
//     PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.elements");
//     masterCoordClass = PyObject_GetAttrString(module, "MasterCoordPtr");
//     Py_XDECREF(module);
//     if(!masterCoordClass) return 0;
//     pyOne = PyInt_FromLong(1);
//   }
//   MasterCoordVec::size_type sz = $source->size();
//   assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
//   $target = PyList_New((Py_ssize_t) sz);
//   char _ptemp[128];
//   for(std::vector<MasterCoord*>::size_type i=0; i<sz; i++) {
//     // Create wrapped swig object
//     SWIG_MakePtr(_ptemp, (char*)(*$source)[i], "_MasterCoord_p");
//     PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
//     PyObject *mc = PyObject_CallObject(masterCoordClass, swigthis);
//     Py_XDECREF(swigthis);
//     // take ownership
//     // TODO 3.1: Check that taking ownership is the correct thing to do!
//     PyObject_SetAttrString(mc, "thisown", pyOne);
//     // put it in the list
//     PyList_SET_ITEM($target, (Py_ssize_t) i, mc);
//   }
// }

// %typemap(python, newfree) MasterCoordVec* {
//   // typemap(python, newfree) MasterCoordVec*
//   delete $source;
//}

%typemap(python, in) MasterCoordVec* (MasterCoordVec mcv) {
  // typemap(python, in) MasterCoordVec*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Error in MasterCoordVec* typemap.  Python list required.");
    return NULL;
  }
  MasterCoordVec::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
						  Py_ssize_t,
						  MasterCoordVec::size_type);
  mcv.resize(sz);
  for(MasterCoordVec::size_type i=0; i<sz; i++) {
    MasterCoord *mc;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**)&mc, "_MasterCoord_p");
    mcv[i] = mc;
  }
  $target = &mcv;
}

%{
  typedef std::vector<PyObject*> PyObjectVec;
%}

%typemap(python, in) PyObjectVec* (PyObjectVec pov) {
  // typemap(python, in) PyObjectVec*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Error in PyObjectVec* typemap.  Python list required.");
    return NULL;
  }
  PyObjectVec::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
					       Py_ssize_t,
					       PyObjectVec::size_type);
  pov.resize(sz);
  for(PyObjectVec::size_type i=0; i<sz; i++) {
    pov[i] = PyList_GET_ITEM($source, (Py_ssize_t) i);
  }
  $target = &pov;
}

// // Typemap for converting a std::vector<std::vector<double>*> to a
// // List of Lists of Floats.
// %{
//   typedef std::vector<std::vector<double>*> VecVec;
// %}

// %typemap(python, out) VecVec* {
//   // typemap(python, out) VecVec*
//   VecVec::size_type sz = $source->size();
//   assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
//   $target = PyList_New((Py_ssize_t) sz);
//   for(std::vector<std::vector<double>*>::size_type i=0; i<sz; i++) {
//     std::vector<double>::size_type dofs = (*$source)[i]->size();
//     PyObject *sublist = PyList_New((Py_ssize_t) dofs);
//     for(std::vector<double>::size_type j=0; j<dofs; j++) {
//       PyList_SET_ITEM(sublist, (Py_ssize_t) j,
// 		      PyFloat_FromDouble( (*(*$source)[i])[j] ) );
//     }
//     PyList_SET_ITEM($target, (Py_ssize_t) i, sublist);
//   }
// }

// %typemap(python, newfree) VecVec* {
//   // typemap(python, newfree) VecVec*
//   for(std::vector<std::vector<double>*>::size_type i=0;i<$source->size();i++) {
//     delete (*$source)[i];
//   }
//   delete $source;
// }

// // Typemap for converting a std::vector<double*> to a List of Floats.
// %{
//   typedef std::vector<const double*> DoubleStarVec;
// %}

// %typemap(python, out) DoubleStarVec* {
//   // typemap(python, out) DoubleStarVec*
//   DoubleStarVec::size_type sz = $source->size();
//   assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
//   $target = PyList_New((Py_ssize_t) sz);
//   for(std::vector<const double*>::size_type i=0; i<sz; i++) {
//     PyList_SET_ITEM($target, (Py_ssize_t) i,
// 		    PyFloat_FromDouble(*(*$source)[i]));
//   }
// }

// %typemap(python, newfree) DoubleStarVec* {
//   // typemap(python, newfree) DoubleStarVec*
//   for(std::vector<const double*>::size_type i=0; i<$source->size(); i++)
//     delete (*$source)[i];
//   delete $source;
// }

%{
#include "engine/symmmatrix.h"
  typedef std::vector<SymmMatrix3*> SymmMatrix3StarVec;
%}

// Convert a vector of SymmMatrix3* objects to a list of
// SymmMatrix3Ptr objects.  The ownership of the swigged objects is
// transferred to Python, so the associated newfree typemap (below)
// doesn't have to delete the members of the vector.
%typemap(python, out) SymmMatrix3StarVec* {
  // typemap(python, out) SymmMatrix3StarVec*
  static PyObject *symmMatrix3Class = 0;
  static PyObject *pyOne = 0;
  if(!symmMatrix3Class) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.symmmatrix");
    symmMatrix3Class = PyObject_GetAttrString(module, "SymmMatrix3Ptr");
    Py_XDECREF(module);
    if(!symmMatrix3Class) return 0;
    pyOne = PyInt_FromLong(1);
  }
  SymmMatrix3StarVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  char _ptemp[128];
  for(std::vector<SymmMatrix3*>::size_type i=0; i<sz; i++) {
    SWIG_MakePtr(_ptemp, (char*)((*$source)[i]), "_SymmMatrix3_p");
    PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
    PyObject *sm3 = PyObject_CallObject(symmMatrix3Class, swigthis);
    Py_XDECREF(swigthis);
     // Set SymmMatrix3Ptr.thisown = 1 to transfer ownership.
     PyObject_SetAttrString(sm3, "thisown", pyOne);

     PyList_SET_ITEM($target, (Py_ssize_t) i, sm3);
  }
}

%typemap(python, newfree) SymmMatrix3StarVec* {
  // typemap(python, newfree), SymmMatrix3StarVec*
  // Don't delete the contents of the vector, because Python owns them
  // and will delete them itself.
  delete $source;
}


%typemap(python, in) MasterCoord *Point (MasterCoord mc) {
  // typemap(python, in) MasterCoord *Point
  PyObject *xobj = PySequence_GetItem($source, 0);
  PyObject *yobj = PySequence_GetItem($source, 1);
#ifdef DIM_3
  PyObject *zobj = PySequence_GetItem($source, 2);
  if(!xobj || !yobj || !zobj) {
    PyErr_SetString(PyExc_TypeError, "Type error in MasterCoord *Point typemap.  Argument must have 0, 1, and 2 components.");
    return NULL;
  }
#else
  if(!xobj || !yobj) {
    PyErr_SetString(PyExc_TypeError, "Type error in MasterCoord *Point typemap.  Argument must have 0 and 1 components.");
    return NULL;
  }
#endif

  mc[0] = PyFloat_AsDouble(xobj);
  mc[1] = PyFloat_AsDouble(yobj);
  Py_XDECREF(xobj);
  Py_XDECREF(yobj);
#ifdef DIM_3
  mc[2] = PyFloat_AsDouble(zobj);
  Py_XDECREF(zobj);
#endif
  $target = &mc;
}



// Typemap for converting a list of nodes to a standard
// template vector.

%{
#include <vector>
#include "engine/node.h"
  typedef std::vector<Node*> NodeVec;
%}

%typemap(python, in) NodeVec * (NodeVec n) {
  // typemap(python, in) NodeVec*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "TypeError in NodeVec typemap.  Python list required.");
    return NULL;
  }
  NodeVec::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
					   Py_ssize_t,
					   NodeVec::size_type);
  n.resize(sz);
  for(NodeVec::size_type i=0; i<sz; i++) {
    Node *tnode;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void **)&tnode, "_CSkeletonNode_p");
    n[i] = tnode;
  }

  $target = &n;
}

%typemap(python, out) Node* {
  // typemap(python, out) Node*
  $target = $source->pythonObject();
  if(!$target)
    return 0;
}

///////////////////////////////

// Convert a list of Elements to a standard template vector

%{
#include "engine/element.h"
typedef std::vector<Element*> ElementVec;
%}

%typemap(python, in) ElementVec* (ElementVec evec) {
  // typemap(python, in) ElementVec*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "TypeError in ElementVec typemap.  Python list required.");
    return NULL;
  }
  ElementVec::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
					      Py_ssize_t,
					      ElementVec::size_type);
  evec.resize(sz);
  for(ElementVec::size_type i=0; i<sz; i++) {
    Element *elem;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**) &elem, "_Element_p");
    evec[i] = elem;
  }
  $target = &evec;
}

////////////////////////////////

// The CompoundFieldVec* typemap converts a std::vector of
// CompoundField*s to a Python list of CompoundFields.  It does *not*
// use the PythonExportable mechanism because the Field class uses too
// much virtual inheritance for PythonExportable to work properly.
// The typemap instead extracts Field names and calls the Python
// getField function (defined in field.spy).

%{
#include <vector>
#include "engine/field.h"
  typedef std::vector<CompoundField*> CompoundFieldVec;
%}

%typemap(python, out) CompoundFieldVec * {
  // typemap(python, out) CompoundFieldVec*
  static PyObject *getField = 0;
  if(!getField) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.field");
    getField = PyObject_GetAttrString(module, "getField");
    Py_XDECREF(module);
    if(!getField) return 0;
  }
  CompoundFieldVec::size_type sz = $source->size();
  assert((int) sz >= PY_SSIZE_T_MIN && (int) sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(std::vector<CompoundField*>::size_type i=0; i<sz; i++) {
    PyObject *arg = Py_BuildValue("(s)", (*$source)[i]->name().c_str() );
    PyObject *fldobj = PyObject_CallObject(getField, arg);
    Py_XDECREF(arg);
    arg = Py_BuildValue("O", fldobj);
    PyList_SET_ITEM($target, (Py_ssize_t) i, arg);
  }
}

%typemap(python, newfree) CompoundFieldVec * {
  // typemap(python, newfree) CompoundFieldVec*
  delete $source;
}

////////////////////////////

// Equations and Fluxes are PythonExportable, unlike Fields, so the
// typemap for vectors of them is simpler.

%{
#include <vector>
#include "engine/equation.h"
  typedef std::vector<Equation*> EquationVec;
%}

%typemap(python, out) EquationVec * {
  // typemap(python, out) EquationVec*
  EquationVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(std::vector<Equation*>::size_type i=0; i<sz; i++) {
    // pythonObject() returns a new reference and PyList_SET_ITEM steals it.
    PyObject *eqn = (*$source)[i]->pythonObject();
    if(!eqn)
      return 0;
    PyList_SET_ITEM($target, (Py_ssize_t) i, eqn);
  }
}

%typemap(python, newfree) EquationVec * {
  // typemap(python, newfree) EquationVec*
  delete $source;
}


%{
#include <vector>
#include "engine/flux.h"
  typedef std::vector<Flux*> FluxVec;
%}

%typemap(python, out) Flux* {
  // typemap(python, out) Flux*
  $target = $source->pythonObject();
  if(!$target)
    return 0;
}

%typemap(python, out) FluxVec * {
  // typemap(python, out) FluxVec*
  FluxVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(FluxVec::size_type i=0; i<sz; i++) {
    PyObject *flux = (*$source)[i]->pythonObject();
    if(!flux)
      return 0;
    PyList_SET_ITEM($target, (Py_ssize_t) i, flux);
  }
}

%typemap(python, newfree) FluxVec * {
  // typemap(python, newfree) FluxVec*
  delete $source;
}


%{
#include "engine/edge.h"
  typedef std::vector<Edge*> EdgeVec;
%}

/* Need to take the EdgeVec's out with a copy-out typemap. */
   
%typemap(python,out) EdgeVec* {
  // typemap(python, out) EdgeVec*
  // Python takes ownership of the Edges in the list, so C++ has to
  // return a vector of new Edges.
  static PyObject *edgeClass = 0;
  static PyObject *pyOne = 0;
  if(!edgeClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.edge");
    edgeClass = PyObject_GetAttrString(module, "EdgePtr");
    Py_XDECREF(module);
    if(!edgeClass) return 0;
    pyOne = PyInt_FromLong(1);
  }
  EdgeVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  char _ptemp[128];
  for(std::vector<Edge*>::size_type i=0; i<sz; i++) {
    // Create a wrapped swig EdgePtr obejct.
    SWIG_MakePtr(_ptemp, (char*)(*$source)[i], "_Edge_p");
    PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
    PyObject *edge = PyObject_CallObject(edgeClass, swigthis);
    Py_XDECREF(swigthis);
    // Take ownership.
    PyObject_SetAttrString(edge, "thisown", pyOne);
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, edge);
  }
}

%typemap(python,newfree) EdgeVec* {
  // typemap(python, newfree) EdgeVec*
  delete $source;
}

// The OutputValueVec typemap converts a std::vector of OutputValues
// to a list of PythonExportable OutputVal subclasses, and hands
// ownership of the objects to Python.

%{
  typedef std::vector<OutputValue> OutputValueVec;
%}

%typemap(python, out) OutputValueVec* {
  // typemap(python, out) OutputValueVec*
  static PyObject *pyOne = 0;
  if(!pyOne) {
    pyOne = PyInt_FromLong(1);
  }
  OutputValueVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(OutputValueVec::size_type i=0; i<sz; i++) {
    // Don't use valuePtr() or valueRef() here, because the OutputVals
    // copied into the Python list will outlive the OutputValues that
    // they're copied from.  valueClone() makes an independent copy.
    PyObject *obj = (*$source)[i].valueClone()->pythonObject();
    if(!obj)
      return 0;
    PyObject_SetAttrString(obj, "thisown", pyOne); // take ownership
    PyList_SET_ITEM($target, (Py_ssize_t) i, obj);
  }
}

%typemap(python, newfree) OutputValueVec* {
  // typemap(python, newfree) OutputValueVec*
  delete $source;
}

// Convert any Python Enum type (particularly a SpaceComponent) to a
// SpaceIndex.

%typemap(python, in) SpaceIndex* (SpaceIndex idx) {
  // typemap(python, in) SpaceIndex*
  PyObject *pyindex = PyObject_CallMethod($source, (char *) "index", 0);
  idx = PyInt_AsLong(pyindex);
  Py_XDECREF(pyindex);
  $target = &idx;
}

//////////

// When a Material* is returned from C++ to Python, the MaterialPtr
// that's returned isn't the same Python object as the Material that
// was created initially.  This typemap uses the Material's name and
// the MaterialManager to fetch the original Material object.

%typemap(python, out) Material* {
  // typemap(python, out) Material*
  static PyObject *getMaterial = 0;
  if(!getMaterial) {
    PyObject *module = PyImport_ImportModule("ooflib.engine.materialmanager");
    getMaterial = PyObject_GetAttrString(module, "getMaterial");
    Py_XDECREF(module);
    if(!getMaterial) return 0;
    Py_XINCREF(getMaterial);
  }
  if($source) {
    PyObject *arglist = Py_BuildValue("(s)", $source->name().c_str());
    $target = PyEval_CallObject(getMaterial, arglist); // call getMaterial()
    Py_XDECREF(arglist);
    // If the material manager can't find the Material, then we're
    // still in the process of building it.  getMaterial will have
    // raised a KeyError, which we clear, and return the unmodified
    // Material object.
    if(!$target) {
      if(PyErr_ExceptionMatches(PyExc_KeyError)) { // we got a KeyError
	PyErr_Clear();
	char _ptemp[128];
	SWIG_MakePtr(_ptemp, (char*) $source, "_Material_p");
	$target = Py_BuildValue("s", _ptemp);
      }
      else {			// we got some other error
	$target = 0;
      }
    }
  }
  else {
    Py_INCREF(Py_None);
    $target = Py_None;
  }
}

%{
  typedef std::vector<const Material*> MaterialVec;
%}

%typemap(python, out) MaterialVec* {
   // typemap(python, out) MaterialVec*
  static PyObject *getMaterial = 0;
  if(!getMaterial) {
    PyObject *module = PyImport_ImportModule("ooflib.engine.materialmanager");
    getMaterial = PyObject_GetAttrString(module, "getMaterial");
    Py_XDECREF(module);
    if(!getMaterial) return 0;
    Py_XINCREF(getMaterial);
  }
  MaterialVec::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(std::vector<const Material*>::size_type i=0; i<$source->size(); i++) {
    PyObject *name = Py_BuildValue("(s)", (*$source)[i]->name().c_str());
    PyList_SET_ITEM($target, (Py_ssize_t) i, 
		    PyEval_CallObject(getMaterial, name));
    Py_XDECREF(name);
  }
}

%typemap(python, newfree) MaterialVec* {
  // typemap(python, newfree) MaterialVec*
  delete $source;
}

%{
#include <set>
#include "engine/material.h"
#include "engine/materialset.h"
%}

%typemap(python, out) MaterialSet* {
   // typemap(python, out) MaterialSet*
  static PyObject *getMaterial = 0;
  if(!getMaterial) {
    PyObject *module = PyImport_ImportModule("ooflib.engine.materialmanager");
    getMaterial = PyObject_GetAttrString(module, "getMaterial");
    Py_XDECREF(module);
    if(!getMaterial) return 0;
    Py_XINCREF(getMaterial);
  }
  // Python 2.4 has a set() object but no API for it, so this is
  // written using generic function calls.  If we stop supporting 2.4,
  // then the commented out code should be used instead.
  static PyObject *setType = 0;
  if(!setType) {
    PyObject *module = PyImport_ImportModule("__builtin__");
    setType = PyObject_GetAttrString(module, "set");
    Py_XDECREF(module);
    if(!setType) return 0;
    Py_XINCREF(setType);
  }
  $target = PyObject_CallObject(setType, NULL);
  for(std::set<const Material*, MaterialCompare>::iterator i=$source->begin();
      i!=$source->end(); ++i) 
    {
      PyObject *name = Py_BuildValue("(s)", (*i)->name().c_str());
      PyObject *matl = PyEval_CallObject(getMaterial, name);
      Py_XDECREF(name);
      if(!matl) return 0;
      if(!PyObject_CallMethod($target, (char *) "add", (char *) "O", matl))
	return 0;
    }
  
//   $target = PySet_New(NULL);
//   for(std::set<const Material*, MaterialCompare>::iterator i=$source->begin(); i!=$source->end();
//       ++i) {
//     PyObject *name = Py_BuildValue("(s)", (*i)->name().c_str());
//     PyObject *matl = PyEval_CallObject(getMaterial, name);
//     Py_XDECREF(name);
//     if(!matl) return 0;
//     int notok = PySet_Add($target, matl);
//     Py_XDECREF(matl);
//     if(notok) return 0;
//   }
}

%typemap(python, newfree) MaterialSet* {
  // typemap(python, newfree) MaterialSet*
  delete $source;
}



%{
#include "engine/cskeletonelement.h"
#include "engine/cskeletonsegment.h"
#include "engine/cskeletonface.h"
#include "engine/cskeletonnode2.h"
#include "engine/cskeleton2.h"
#include "engine/cskeletonselectable.h"
%}

%typemap(python, out) CSkeletonBase* {
   $target = $source->pythonObject();
}

%typemap(python, in) CSkeletonNodeVector* (CSkeletonNodeVector snv) {
  // typemap(python, in) CSkeletonNodeVector*
  if(!PyList_Check($source)) {
    PyErr_SetString(
	    PyExc_TypeError,
	    "Error in CSkeletonNodeVector* typemap.  Python list required.");
    return NULL;
  }
  CSkeletonNodeVector::size_type sz = Py_SAFE_DOWNCAST(
			       PyList_Size($source),
			       Py_ssize_t,
			       CSkeletonNodeVector::size_type);
  snv.resize(sz);
  for(CSkeletonNodeVector::size_type i=0; i<sz; i++) {
    CSkeletonNode *n;
    PyObject *stg = PyObject_GetAttrString(
				   PyList_GET_ITEM($source, (Py_ssize_t) i),
				   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**)&n, "_CSkeletonNode_p");
    snv[i] = n;
  }
  $target = &snv;
}

%typemap(python, in) CSkeletonSegmentVector* (CSkeletonSegmentVector snv) {
  // typemap(python, in) CSkeletonSegmentVector*
  if(!PyList_Check($source)) {
    PyErr_SetString(
	    PyExc_TypeError,
	    "Error in CSkeletonSegmentVector* typemap.  Python list required.");
    return NULL;
  }
  CSkeletonSegmentVector::size_type sz = Py_SAFE_DOWNCAST(
	  PyList_Size($source), Py_ssize_t, CSkeletonSegmentVector::size_type);
  snv.resize(sz);
  for(CSkeletonSegmentVector::size_type i=0; i<sz; i++) {
    CSkeletonSegment *n;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**)&n, "_CSkeletonSegment_p");
    snv[i] = n;
  }
  $target = &snv;
}

%typemap(python, in) CSkeletonFaceVector* (CSkeletonFaceVector sfv) {
  // typemap(python, in) CSkeletonFaceVector*
  if(!PyList_Check($source)) {
    PyErr_SetString(
	    PyExc_TypeError,
	    "Error in CSkeletonFaceVector* typemap.  Python list required.");
    return NULL;
  }
  CSkeletonFaceVector::size_type sz = Py_SAFE_DOWNCAST(
       PyList_Size($source), Py_ssize_t, CSkeletonFaceVector::size_type);
  sfv.resize(sz);
  for(CSkeletonFaceVector::size_type i=0; i<sz; i++) {
    CSkeletonFace *f;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**) &f, "_CSkeletonFace_p");
    sfv[i] = f;
  }
  $target = &sfv;
}

// Typemap for converting a CSkeletonNodeVector to a Python list
// of CSkeletonNodePtr objects.  Python takes ownership of the objects.

%typemap(python,out) CSkeletonNodeVector* {
  // typemap(python, out) CSkeletonNodeVector*
  CSkeletonNodeVector::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(CSkeletonNodeVector::size_type i=0; i<sz; i++) {
    // Create wrapped swig object.  Do NOT take ownership.
    PyObject *n = (*$source)[i]->pythonObject();
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, n); // Steals reference.
  }
}

%typemap(python,newfree) CSkeletonNodeVector* {
  // typemap(python, newfree) CSkeletonNodeVector*
  delete $source;
}

%typemap(python,out) CSkeletonFaceVector* {
  // typemap(python, out) CSkeletonFaceVector*
  CSkeletonFaceVector::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(CSkeletonFaceVector::size_type i=0; i<sz; i++) {
    // Create wrapped swig object.  Do NOT take ownership.
    PyObject *n = (*$source)[i]->pythonObject();
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, n); // Steals reference.
  }
}

%typemap(python,newfree) CSkeletonFaceVector* {
  // typemap(python, newfree) CSkeletonFaceVector*
  delete $source;
}
%typemap(python,out) CSkeletonSegmentVector* {
  // typemap(python, out) CSkeletonSegmentVector*
  CSkeletonSegmentVector::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  for(CSkeletonSegmentVector::size_type i=0; i<sz; i++) {
    // Create wrapped swig object.  Do NOT take ownership.
    PyObject *n = (*$source)[i]->pythonObject();
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, n); // Steals reference.
  }
}

%typemap(python,newfree) CSkeletonSegmentVector* {
  // typemap(python, newfree) CSkeletonSegmentVector*
  delete $source;
}


%typemap(python,out) CSkeletonElementVector* {
  CSkeletonElementVector::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  // std::cerr << "********* CSkeletonElementVector typemap: " << sz 
  // 	    << " elements *********" << std::endl;
  $target = PyList_New((Py_ssize_t) sz);
  //char _ptemp[128];
  for(CSkeletonElementVector::size_type i=0; i<sz; i++) {
    // Create wrapped swig object.  Do NOT take ownership.
    PyObject *e = (*$source)[i]->pythonObject();
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, e); // Steals reference.
  }
}

%typemap(python,newfree) CSkeletonElementVector* {
  delete $source;
}

%typemap(python,out) CSkeletonSegmentMap* {
  CSkeletonSegmentMap::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  int i = 0;
  for(CSkeletonSegmentMap::iterator it=$source->begin(); it!=$source->end();
      ++it, ++i) 
    {
      // Create wrapped swig object.
      PyObject *e = (*it).second->pythonObject();
      // TODO 3.1: This typemap doesn't seem to be used, so it's not clear
      // if it should take ownership of the Segments or not.  It
      // probably shouldn't.

      // // Take ownership
      // PyObject_SetAttrString(e, "thisown", PyInt_FromLong(1));
      // Put it in the list.
      PyList_SET_ITEM($target, (Py_ssize_t) i, e); // Steals reference.
    }
}

%typemap(python,newfree) CSkeletonSegmentMap* {
  delete $source;
}

%typemap(python,out) CSkeletonFaceMap* {
  CSkeletonFaceMap::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  //char _ptemp[128];
  int i=0;
  for(CSkeletonFaceMap::iterator it=$source->begin(); it!=$source->end();
      ++it, ++i)
    {
      // Create wrapped swig object.
      PyObject *e = (*it).second->pythonObject();
      // TODO 3.1: This typemap doesn't seem to be used, so it's not clear
      // if it should take ownership of the Faces or not.  It
      // probably shouldn't.

      // // Take ownership
      // PyObject_SetAttrString(e, "thisown", PyInt_FromLong(1));
      // Put it in the list.
      PyList_SET_ITEM($target, (Py_ssize_t) i, e); // Steals reference.
    }
}

%typemap(python,newfree) CSkeletonFaceMap* {
  // typemap(python,newfree) CSkeletonFaceMap*
  delete $source;
}

// %typemap(python,out) CSkeletonSelectableSet* {
//   CSkeletonSelectableSet::size_type sz = $source->size();
//   assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);

//   // For Python 2.4 and earlier, we build the set "manually".
//   static PyObject *setType = 0;
//   if(!setType) {
//     PyObject *module = PyImport_ImportModule("__builtin__");
//     setType = PyObject_GetAttrString(module, "set");
//     Py_XDECREF(module);
//     if(!setType) return 0;
//     Py_XINCREF(setType);
//   }
//   $target = PyObject_CallObject(setType, NULL);

//   // For Python 2.5 and later, substitute the line below for the block above.
//   // $target = PySet_New(NULL); 

//   //char _ptemp[128];
//   int i=0;
//   for(CSkeletonSelectableSet::iterator it = $source->begin(); it != $source->end(); ++it, ++i) {
//     // Create wrapped swig object.
//     PyObject *e = (*it)->pythonObject();
//     // Take ownership
//     PyObject_SetAttrString(e, "thisown", PyInt_FromLong(1));
//     // Put it in the set.

//     // Python 2.4 way, for now
//     if(!e) return 0;
//     if(!PyObject_CallMethod($target, "add", "(O)", e)) 
//       return 0;

//     // Python 2.5 way, for later
//     // PySet_Add($target, e);

//     //PyList_SET_ITEM($target, (Py_ssize_t) i, e); // Steals reference.
//   }
// }

%typemap(python,out) CSkeletonSelectableSet* {
  // typemap(python,out) CSkeletonSelectableSet*
  CSkeletonSelectableSet::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  int i=0;
  for(CSkeletonSelectableSet::iterator it=$source->begin(); it!=$source->end(); ++it, ++i) {
    // Create wrapped swig object.  Do NOT take ownership.
    PyObject *n = (*it)->pythonObject();
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, n); // Steals reference.
  }
}

%typemap(python,newfree) CSkeletonSelectableList* {
  // typemap(python,newfree) CSkeletonSelectableList*
  delete $source;
}

%typemap(python,newfree) CSkeletonSelectableSet* {
  // typemap(python,newfree) CSkeletonSelectableSet*
  delete $source;
}

%typemap(python,out) CSkeletonSelectableList* {
  // typemap(python,out) CSkeletonSelectableList*
  CSkeletonSelectableList::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  int i=0;
  for(CSkeletonSelectableList::iterator it=$source->begin(); it!=$source->end(); ++it, ++i) {
    // Create wrapped swig object.
    PyObject *n = (*it)->pythonObject();
    // This typemap isn't used, so it's hard to say if it should take
    // ownership of the CSkeletonSelectables in the list or not.  It
    // probably shouldn't.
    // // Take ownership
    // PyObject_SetAttrString(n, "thisown", PyInt_FromLong(1));
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, n); // Steals reference.
  }
}

%typemap(python,newfree) CSkeletonSelectableList* {
  delete $source;
}

%typemap(python, in) CSkeletonSelectableList* (CSkeletonSelectableList sl) {
  // typemap(python, in) CSkeletonSelectableList*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Error in CSkeletonSelectableList* typemap.  Python list required.");
    return NULL;
  }
  CSkeletonSelectableList::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
							   Py_ssize_t,
							   CSkeletonSelectableList::size_type);

  for(CSkeletonSelectableList::size_type i=0; i<sz; i++) {
    CSkeletonSelectable *s;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**)&s, "_CSkeletonSelectable_p");
    sl.push_back(s);
  }
  $target = &sl;
}

%typemap(python, in) CSelectionTrackerVector* (CSelectionTrackerVector vec) {
  // typemap(python, in) CSelectionTrackerVector*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Error in CSelectionTrackerVector typemap.  Python list required.");
    return NULL;
  }
  CSelectionTrackerVector::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
					       Py_ssize_t,
					       CSelectionTrackerVector::size_type);
  vec.resize(sz);
  for(CSelectionTrackerVector::size_type i=0; i<sz; i++) {
    CSelectionTracker *tracker;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void **)&tracker, "_CSelectionTracker_p");
    vec[i] = tracker;
  }
  $target = &vec;
}



%typemap(python, in) CPinnedNodeTrackerVector* (CPinnedNodeTrackerVector vec) {
  // typemap(python, in) CPinnedNodeTrackerVector*
  if(!PyList_Check($source)) {
    PyErr_SetString(
	    PyExc_TypeError,
	    "Error in CPinnedNodeTrackerVector typemap. Python list required.");
    return NULL;
  }
  CPinnedNodeTrackerVector::size_type sz = 
    Py_SAFE_DOWNCAST(PyList_Size($source),
		     Py_ssize_t,
		     CPinnedNodeTrackerVector::size_type);
  vec.resize(sz);
  for(CPinnedNodeTrackerVector::size_type i=0; i<sz; i++) {
    CPinnedNodeTracker *tracker;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void **)&tracker, "_CPinnedNodeTracker_p");
    vec[i] = tracker;
  }
  $target = &vec;
}




%typemap(python, in) CGroupTrackerVector* (CGroupTrackerVector vec) {
  // typemap(python, in) CGroupTrackerVector*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Error in CGroupTrackerVector typemap.  Python list required.");
    return NULL;
  }
  CGroupTrackerVector::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
					       Py_ssize_t,
					       CGroupTrackerVector::size_type);
  vec.resize(sz);
  for(CGroupTrackerVector::size_type i=0; i<sz; i++) {
    CGroupTrackerBase *tracker;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void **)&tracker, "_CGroupTrackerBase_p");
    vec[i] = tracker;
  }
  $target = &vec;
}


// %typemap(python,out) CDeputySkeletonList* {
//   CDeputySkeletonList::size_type sz = $source->size();
//   assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
//   $target = PyList_New((Py_ssize_t) sz);
//   //char _ptemp[128];
//   int i=0;
//   static PyObject *getSkeleton = 0;
//   if(!getSkeleton) {
//     PyObject *module = PyImport_ImportModule("ooflib.engine.skeletonmanager");
//     getSkeleton = PyObject_GetAttrString(module, "getSkeleton");
//     Py_XDECREF(module);
//     if(!getSkeleton) return 0;
//     Py_XINCREF(getSkeleton);
//   }
//   for(CDeputySkeletonList::iterator it = $source->begin(); it!=$source->end(); ++it, ++i) {
//     // Create wrapped swig object.
//     //PyObject *o = (*it)->pythonObject();
//     // Take ownership
//     //PyObject_SetAttrString(o, "thisown", PyInt_FromLong(1));
//     // Put it in the list.
//     //PyList_SET_ITEM($target, (Py_ssize_t) i, o); // Steals reference.

//     PyObject *arglist = Py_BuildValue("(i)", (*it)->getUid());
//     PyObject *o = PyEval_CallObject(getSkeleton, arglist); // call getSkeleton()
//     Py_XDECREF(arglist);
//     // If the skeleton manager can't find the Skeleton, then we're
//     // still in the process of building it.  getSkeleton will have
//     // raised a KeyError, which we clear, and return the unmodified
//     // Skeleton object.
//     if(!o) {
//       if(PyErr_ExceptionMatches(PyExc_KeyError)) { // we got a KeyError
// 	PyErr_Clear();
// 	o = (*it)->pythonObject();
// 	PyObject_SetAttrString($target, "thisown",  PyInt_FromLong(1));
//       }
//       else {			// we got some other error
// 	$target = 0;
//       }
//     }
//     PyList_SET_ITEM($target, (Py_ssize_t) i, o); // Steals reference.

//   }
// }

// %typemap(python,newfree) CDeputySkeletonList* {
//   delete $source;
// }

%typemap(python,out) CSkeletonElementSet* {
  // typemap(python,out) CSkeletonElementSet* 
  CSkeletonElementSet::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz); 
  //char _ptemp[128];
  int i=0;
  for(CSkeletonElementSet::iterator it = $source->begin(); it != $source->end(); ++it, ++i) {
    // Create wrapped swig object.
    PyObject *e = (*it)->pythonObject();
    // This typemap isn't used, so it's hard to say if it should take
    // ownership of the CSkeletonElements in the set or not.  It
    // probably shouldn't.
    // // Take ownership
    // PyObject_SetAttrString(e, "thisown", PyInt_FromLong(1));
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, e); // Steals reference.
  }
}

%typemap(python,newfree) CSkeletonElementSet* {
  // typemap(python,newfree) CSkeletonElementSet*
  delete $source;
}

%typemap(python, out) CSkeletonNodeSet* {
  // typemap(python, out) CSkeletonNodeSet*
  assert((int) $source->size() >= PY_SSIZE_T_MIN &&
	 (int) $source->size() <= PY_SSIZE_T_MAX);

  // Use an OrderedSet from the utils module, instead of the builtin
  // set, because otherwise regression tests are not repeatable. 
  static PyObject *setType = 0;
  if(!setType) {
    PyObject *module = PyImport_ImportModule("ooflib.common.utils");
    setType = PyObject_GetAttrString(module, "OrderedSet");
    Py_XDECREF(module);
    if(!setType) return 0;
    Py_XINCREF(setType);
  }
  $target = PyObject_CallObject(setType, NULL);

  // If it's not necessary to use an OrderedSet, substitute the line
  // below for the block above.  This only works in Python 2.5 and
  // later.
  // $target = PySet_New(NULL); 

  for(CSkeletonNodeSet::iterator it = $source->begin(); it != $source->end();
      ++it)
    {
      // Create wrapped swig object.  Do NOT take ownership.
      PyObject *e = (*it)->pythonObject();
      if(!e) return 0;

      // Put it in the set.  (Python 2.4 way, for now)
      if(!PyObject_CallMethod($target, (char *) "add", (char *) "(O)", e)) 
	return 0;
      // Python 2.5 way, for later
      // PySet_Add($target, e);
    }
}

%typemap(python, newfree) CSkeletonNodeSet* {
  // typemap(python, newfree) CSkeletonNodeSet*
  delete $source;
}

%typemap(python, out) CSkeletonFaceSet* {
  //  typemap(python,out) CSkeletonFaceSet* 
  assert((int)$source->size() >= PY_SSIZE_T_MIN && 
	 (int)$source->size() <= PY_SSIZE_T_MAX);

  // Use an OrderedSet from the utils module, instead of the builtin
  // set, because otherwise regression tests are not repeatable. 
  static PyObject *setType = 0;
  if(!setType) {
    PyObject *module = PyImport_ImportModule("ooflib.common.utils");
    setType = PyObject_GetAttrString(module, "OrderedSet");
    Py_XDECREF(module);
    if(!setType) return 0;
    Py_XINCREF(setType);
  }
  $target = PyObject_CallObject(setType, NULL);

  // If it's not necessary to use an OrderedSet, substitute the line
  // below for the block above.  This only works in Python 2.5 and
  // later.
  // $target = PySet_New(NULL); 

  for(CSkeletonFaceSet::iterator it=$source->begin(); it!=$source->end();
      ++it) 
    {
      // Create wrapped swig object.  Do NOT take ownership
      PyObject *e = (*it)->pythonObject();
      if(!e) return 0;
      // Put it in the set.  (Python 2.4 way, for now.)
      if(!PyObject_CallMethod($target, (char *) "add", (char *) "(O)", e)) 
	return 0;
      
      // Python 2.5 way, for later
      // PySet_Add($target, e);
    }
}

%typemap(python,newfree) CSkeletonFaceSet* {
  // %typemap(python,newfree) CSkeletonFaceSet* 
  delete $source;
}
%typemap(python, out) CSkeletonSegmentSet* {
  // typemap(python,out) CSkeletonSegmentSet* 
  assert((int) $source->size() >= PY_SSIZE_T_MIN && 
	 (int) $source->size() <= PY_SSIZE_T_MAX);

  // Use an OrderedSet from the utils module, instead of the builtin
  // set, because otherwise regression tests are not repeatable. 
  static PyObject *setType = 0;
  if(!setType) {
    PyObject *module = PyImport_ImportModule("ooflib.common.utils");
    setType = PyObject_GetAttrString(module, "OrderedSet");
    Py_XDECREF(module);
    if(!setType) return 0;
    Py_XINCREF(setType);
  }
  $target = PyObject_CallObject(setType, NULL);

  // If it's not necessary to use an OrderedSet, substitute the line
  // below for the block above.  This only works in Python 2.5 and
  // later.
  // $target = PySet_New(NULL); 

  for(CSkeletonSegmentSet::iterator it=$source->begin(); it!=$source->end();
      ++it) 
    {
      // Create wrapped swig object.  Do NOT take ownership.
      PyObject *e = (*it)->pythonObject();
      if(!e) return 0;
      // Put it in the set.  (Python 2.4 way, for now.)
      if(!PyObject_CallMethod($target, (char *) "add", (char *) "(O)", e)) 
	return 0;
      // Python 2.5 way, for later
      // PySet_Add($target, e);
    }
}

%typemap(python,newfree) CSkeletonSegmentSet* {
  // %typemap(python,newfree) CSkeletonSegmentSet* 
  delete $source;
}

%typemap(python,out) CSkeletonBoundaryMap* {
  // typemap(python, out) CSkeletonBoundaryMap*
  assert((int)$source->size() >= PY_SSIZE_T_MIN && 
	 (int)$source->size() <= PY_SSIZE_T_MAX);
  $target = PyDict_New();
  for(CSkeletonBoundaryMap::iterator it=$source->begin(); it!=$source->end();
      ++it) 
    {
      // Create wrapped swig object using pythonExportable functions
      PyObject *e = (*it).second->pythonObject();
      // Put it in the dict.  This steals the reference.
      PyDict_SetItemString($target, (*it).first.c_str(), e); 
    }
}

%typemap(python,newfree) CSkeletonBoundaryMap* {
  delete $source;
}

%typemap(python,out) OrientedCSkeletonSegmentVector* {
  static PyObject *orientedSegmentClass = 0;
  static PyObject *pyOne;
  if(!orientedSegmentClass) {
    PyObject *module = PyImport_ImportModule(
				     "ooflib.SWIG.engine.cskeletonsegment");
    orientedSegmentClass = PyObject_GetAttrString(
				  module, "OrientedCSkeletonSegmentPtr");
    Py_XDECREF(module);
    if(!orientedSegmentClass) return 0;
    pyOne = PyInt_FromLong(1);
  }
  OrientedCSkeletonSegmentVector::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);
  $target = PyList_New((Py_ssize_t) sz);
  char _ptemp[128];
  for(OrientedCSkeletonSegmentVector::size_type i=0; i<sz; i++) {
    // Create wrapped swig object.  Do NOT take ownership.
    SWIG_MakePtr(_ptemp, (char*)(*$source)[i], "_OrientedCSkeletonSegment_p");
    PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
    PyObject *gp = PyObject_CallObject(orientedSegmentClass, swigthis);
    Py_XDECREF(swigthis);
    // // Take ownership
    // PyObject_SetAttrString(gp, "thisown", pyOne);
    // Put it in the list.
    PyList_SET_ITEM($target, (Py_ssize_t) i, gp); // Steals reference.
  }
}

%typemap(python,newfree) OrientedCSkeletonSegmentVector* {
  // typemap(python,newfree) OrientedsegmentVec*
  delete $source;
}



%typemap(python,out) OrientedCSkeletonSegmentSet* {
  static PyObject *orientedSegmentClass = 0;
  if(!orientedSegmentClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.cskeletonsegment");
    orientedSegmentClass = PyObject_GetAttrString(module, "OrientedCSkeletonSegmentPtr");
    Py_XDECREF(module);
    if(!orientedSegmentClass) return 0;
  }

  OrientedCSkeletonSegmentSet::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);

  // For Python 2.4 and earlier, we build the set "manually".
  static PyObject *setType = 0;
  if(!setType) {
    PyObject *module = PyImport_ImportModule("__builtin__");
    setType = PyObject_GetAttrString(module, "set");
    Py_XDECREF(module);
    if(!setType) return 0;
    Py_XINCREF(setType);
  }
  $target = PyObject_CallObject(setType, NULL);

  // For Python 2.5 and later, substitute the line below for the block above.
  // $target = PySet_New(NULL); 

  char _ptemp[128];
  for(OrientedCSkeletonSegmentSet::iterator it = $source->begin();
      it != $source->end(); ++it) 
    {
      // Create wrapped swig object.
      SWIG_MakePtr(_ptemp, (char*)(*it), "_OrientedCSkeletonSegment_p");
      PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
      PyObject *os = PyObject_CallObject(orientedSegmentClass, swigthis);
      Py_XDECREF(swigthis);
      if(!os) return 0;
      // TODO 3.1: This typemap doesn't seem to be used, so it's not clear
      // if it should take ownership of the Segments or not.  It
      // probably shouldn't.
      // // Take ownership. 
      // PyObject_SetAttrString(os, "thisown", PyInt_FromLong(1));

      // Put it in the set.  (Python 2.4 way, for now.)
      if(!PyObject_CallMethod($target, (char *) "add", (char *) "(O)", os)) 
	return 0;
      // Python 2.5 way, for later
      // PySet_Add($target, os);
    }
}

%typemap(python,newfree) OrientedCSkeletonSegmentSet* {
  delete $source;
}



%typemap(python,out) OrientedCSkeletonFaceSet* {
  static PyObject *orientedFaceClass = 0;
  if(!orientedFaceClass) {
    PyObject *module = PyImport_ImportModule("ooflib.SWIG.engine.cskeletonface");
    orientedFaceClass = PyObject_GetAttrString(module, "OrientedCSkeletonFacePtr");
    Py_XDECREF(module);
    if(!orientedFaceClass) return 0;
  }

  OrientedCSkeletonFaceSet::size_type sz = $source->size();
  assert((int)sz >= PY_SSIZE_T_MIN && (int)sz <= PY_SSIZE_T_MAX);

  // For Python 2.4 and earlier, we build the set "manually".
  static PyObject *setType = 0;
  if(!setType) {
    PyObject *module = PyImport_ImportModule("__builtin__");
    setType = PyObject_GetAttrString(module, "set");
    Py_XDECREF(module);
    if(!setType) return 0;
    Py_XINCREF(setType);
  }
  $target = PyObject_CallObject(setType, NULL);

  // For Python 2.5 and later, substitute the line below for the block above.
  // $target = PySet_New(NULL); 

  char _ptemp[128];
  for(OrientedCSkeletonFaceSet::iterator it = $source->begin();
      it != $source->end(); ++it)
    {
      // Create wrapped swig object.  Do NOT take ownership.
      SWIG_MakePtr(_ptemp, (char*)(*it), "_OrientedCSkeletonFace_p");
      PyObject *swigthis = Py_BuildValue("(s)", _ptemp);
      PyObject *os = PyObject_CallObject(orientedFaceClass, swigthis);
      Py_XDECREF(swigthis);
      if(!os) return 0;

      // Put it in the set.  (Python 2.4 way, for now.)
      if(!PyObject_CallMethod($target, (char *) "add", (char *) "(O)", os)) 
	return 0;

      // Python 2.5 way, for later
      // PySet_Add($target, os);
    }
}

%typemap(python,newfree) OrientedCSkeletonFaceSet* {
  delete $source;
}

%typemap(python, in) OrientedCSkeletonFaceSet* (OrientedCSkeletonFaceSet fs) {
  // typemap(python, in) OrientedCSkeletonFaceSet*
  if(!PyList_Check($source)) {
    PyErr_SetString(PyExc_TypeError,
		    "Error in OrientedCSkeletonFaceSet* typemap.  Python list required.");
    return NULL;
  }
  OrientedCSkeletonFaceSet::size_type sz = Py_SAFE_DOWNCAST(PyList_Size($source),
							    Py_ssize_t,
							    OrientedCSkeletonFaceSet::size_type);

  for(OrientedCSkeletonFaceSet::size_type i=0; i<sz; i++) {
    OrientedCSkeletonFace *f;
    PyObject *stg = PyObject_GetAttrString(PyList_GET_ITEM($source,
							   (Py_ssize_t) i),
					   "this");
    if(!stg)
      return NULL;
    char *str = PyString_AsString(stg);
    SWIG_GetPtr(str, (void**)&f, "_OrientedCSkeletonFace_p");
    fs.insert(f);
  }
  $target = &fs;
}


%{
  typedef std::set<Node*> NodeSet;
%}

%typemap(python, out) NodeSet* {
  // typemap(python, out) NodeSet*
  assert((int) $source->size() >= PY_SSIZE_T_MIN &&
	 (int) $source->size() <= PY_SSIZE_T_MAX);
  static PyObject *setType = 0;
  if(!setType) {
    PyObject *module = PyImport_ImportModule("ooflib.common.utils");
    setType = PyObject_GetAttrString(module, "OrderedSet");
    Py_XDECREF(module);
    if(!setType) return 0;
    Py_XINCREF(setType);
  }
  $target = PyObject_CallObject(setType, NULL);
  for(NodeSet::const_iterator n=$source->begin(); n!=$source->end(); ++n) {
    PyObject *pynode = (*n)->pythonObject();
    if(!pynode) return 0;
    if(!PyObject_CallMethod($target, (char *) "add", (char *) "(O)", pynode))
      return 0;
  }
}

%typemap(python, newfree) NodeSet* {
  // typemap(python, newfree) NodeSet*
  delete $source;
}


#endif // ENGINETYPEMAPS_SWG
