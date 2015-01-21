// -*- C++ -*-
// $RCSfile: element.swg,v $
// $Revision: 1.18.2.25 $
// $Author: langer $
// $Date: 2014/09/17 17:47:56 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ELEMENTS_SWG
#define ELEMENTS_SWG

%module element
%include "engine/typemaps.swg"
%extern "common/coord.swg"
%extern "common/IO/canvaslayers.swg"
%extern "engine/csubproblem.swg"
%extern "engine/edge.swg"
%extern "engine/femesh.swg"
%extern "engine/field.swg"
%extern "engine/IO/gridsource.swg"
%extern "engine/mastercoord.swg"
%extern "engine/outputval.swg"
%pragma(python) code="from ooflib.SWIG.engine.outputval import OutputValuePtr"
%pragma(python) code="from ooflib.SWIG.engine.cskeletonelement import CSkeletonElementPtr"

%pragma(python) include="element.spy"

%{
#include "engine/element.h"
#include "engine/cskeleton2.h"
#include "engine/material.h"
#include "engine/IO/gridsource.h"
#include "common/IO/vtkutils.h"
%}

// VecVec and MasterCoordVec are typedef'd in engine/typemaps.swg
// Likewise GaussPointVec and EdgeVec.


// PythonExportable typemap for ElementData*-returning functions.
// Has the extra-special feature of noticing null-pointer returns
// and translating them to "None".

%typemap(python, out) ElementData * {
  // typemap(python, out) ElementData*
  if ($source != 0) {
    $target = $source->pythonObject();
    if(!$target)
      return 0;
  }
  else
    $target = Py_None;
}

%pragma(python) code="from ooflib.SWIG.engine.elementnodeiterator import *"
%pragma(python) code="from ooflib.SWIG.engine.gausspoint import GaussPointPtr"
%extern "engine/elementnodeiterator.swg"

class CSkeleton;
class CSkeletonElement;
class ElementFuncNodeIterator;
class ElementMapNodeIterator;
class ElementNodeIterator;
class MasterElement;
class MasterPosition;
class Material;

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Base class for data objects stored in the element.
class ElementData {
public:
  const string &name();
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ElementBase {
public:
  int dimension();
  int nnodes();
  double span();
  %new GaussPointVec* integration_points(int);
  int shapefun_degree() const;
  int dshapefun_degree() const;
  int mapfun_degree() const;
  MasterCoord center();
  int ncorners();
  int nedges();
  Coord from_master(MasterCoord *Point);
  MasterCoord to_master(Coord *Point);
};

class ElementLite : public ElementBase {
public:
  %addmethods {
    %new const string *__repr__() {
      return self->repr();
    } 
  } // addmethods
};

class Element : public ElementBase {
public:
  Material *material();
  const MasterElement &masterelement();
#ifndef DIM_3
  %new EdgeVec* perimeter();
#endif
  vtkIdListPtr getPointIds();
  void drawGridCell(GridSourcePtr, SimpleCellLayer*);

  ElementNodeIterator node_iterator();
  ElementMapNodeIterator mapnode_iterator();
  ElementFuncNodeIterator *funcnode_iterator();
  ElementCornerNodeIterator cornernode_iterator();

  ElementCornerNodePositionIterator *cornernode_positerator();
  ElementFuncNodePositionIterator *funcnode_positerator();
  CSkeletonElement *get_skeleton_element();
  Node *getSegmentNode(FEMesh*, int, int);
#ifndef DIM_3
  bool exterior(MasterCoord&, MasterCoord&);
  void set_exterior(Node&, Node&);
  void dump_exterior(); // debugging
#endif  // DIM_3

  void set_index(int);
  const int get_index() const;
  %addmethods {
    int uiIdentifier() {	// See comment in genericinfoGUI.py
      return self->get_index();
    }
  }

  // Data retrieval methods.
  int appendData(ElementData *x);
  void setData(int i, ElementData *x);
  void setDataByName(ElementData *x);
  ElementData *getData(int i);
  int getIndexByName(char *name);
  ElementData *getDataByName(char *name);

  Node* getCornerNode(int i) const;
  const string &name();
  %new StringVec* namelist();

  void refreshMaterial(const CSkeletonBase*);

  OutputValue outputField(FEMesh*, Field&, MasterPosition&);
  %new OutputValueVec *outputFields(FEMesh*, Field&, MasterCoordVec*);
  %new OutputValueVec *outputFieldDerivs(FEMesh*, Field&, SpaceIndex*,
					 MasterCoordVec*);
  // OutputValue outputFlux(FEMesh*, Flux&, MasterPosition&);
  %new OutputValueVec *outputFluxes(FEMesh*, Flux&, MasterCoordVec*);

//   void begin_material_computation(FEMesh*);
//   void end_material_computation(FEMesh*);

  %addmethods {
    %new const string *__repr__() {
      return self->repr();
    } 
  } // addmethods
};

#ifdef DIM_3
class FaceBoundaryElement : public Element {
public:
  void setFrontBulk(Element*);
  Element *getFrontBulk();
  void setBackBulk(Element*);
  Element *getBackBulk();
};
#endif // DIM_3

class EdgeBoundaryElement : public Element {

};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef DIM_3
Coord findNormal(ElementBase*, MasterPosition&);
%new OutputValueVec *findNormals(ElementBase*, MasterCoordVec*);
#endif // DIM_3

%typemap(python,out) EdgeVec*;
%typemap(python,freearg) EdgeVec*;
%typemap(python,out) ElementData*;

#endif // ELEMENTS_SWG
