// -*- C++ -*-
// $RCSfile: masterelement.swg,v $
// $Revision: 1.35.10.7 $
// $Author: langer $
// $Date: 2014/04/01 18:41:34 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MASTERELEMENT_SWG
#define MASTERELEMENT_SWG

%include "engine/typemaps.swg"

%pragma(python) include="engine/masterelement.spy"
%extern "engine/element.swg"
%extern "engine/mastercoord.swg"

%{
#include "common/tostring.h"
#include "engine/masterelement.h"
#include "engine/element.h"
typedef std::vector<MasterElement*> MasterElementList;
%}

%pragma(python) code="from ooflib.SWIG.engine.element import ElementLitePtr"
%pragma(python) code="from ooflib.SWIG.engine.element import EdgeBoundaryElementPtr"
%pragma(python) code="from ooflib.SWIG.engine.element import FaceBoundaryElementPtr"

class ProtoNode {
public:
  int index();
  bool mapping();
  bool func();
  bool corner();
  int nedges();
  int getedge(int i);
  const MasterCoord &mastercoord();
}; 

%typemap(python, out) MasterElement* {
  $target = $source->pythonObject();
}

%typemap(python, out) ElementShape* {
  $target = $source->pythonObject();
}

%typemap(python, ignore) CSkeletonElement *NONE {
  $target = 0;
}

%typemap(python, ignore) Material *NONE {
  $target = 0;
}

class MasterElement {
public:
  // int id();
  int dimension();
  const ElementShape *shape();
  MasterCoord center();
  int nnodes();
  int nmapnodes();
  int nfuncnodes();
  int ninteriorfuncnodes();
  int ninteriormapnodes_only();
  int nexteriormapnodes_only();
  int nedges();
  const string &name();
  const string &description();
  int ncorners();
  int map_order();
  int fun_order();

  //  Element *build(CSkeletonElement *NONE, Material *NONE, NodeVec*);
  FaceBoundaryElement *buildFaceBoundary(NodeVec*);
  EdgeBoundaryElement *buildEdgeBoundary(NodeVec*);
  ElementLite *buildLite(PointVec *PointList);

  %addmethods {
    const ProtoNode *get_protonode(int n) {
      return self->protonode(n);
    }
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }

  

  // Superconvergent patch recovery
  int nSCpoints();
  MasterCoord getSCpoint(int);
};

class MasterElement1D : public MasterElement {};

class MasterElement2D : public MasterElement {
public:
#ifndef DIM_3
  bool onBoundary(const MasterCoord&);
  bool onBoundary2(const MasterCoord&, const MasterCoord&);
#endif	// DIM_3
};

class TriangularMaster : public MasterElement2D {};
class QuadrilateralMaster : public MasterElement2D {};

class MasterElement3D : public MasterElement {};
class TetrahedralMaster : public MasterElement3D {};

int integration_reduction;

%new StringVec *getMasterElementNames();
MasterElement *getMasterElementByName(char*);
MasterElement *getMasterElementByShape(ElementShape*, int, int);

#endif // MASTERELEMENT_SWG
