// -*- C++ -*-
// $RCSfile: node.swg,v $
// $Revision: 1.25.6.10 $
// $Author: langer $
// $Date: 2014/09/17 17:48:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef NODE_SWG
#define NODE_SWG

%module node
%include "engine/typemaps.swg"
%extern "common/coord.swg"
%extern "engine/field.swg"
%extern "engine/pointdata.swg"
%extern "engine/IO/gridsource.swg"
%pragma(python) code="from ooflib.SWIG.engine.pointdata import PointDataPtr"

%{
#include "engine/node.h"
#include "engine/IO/gridsource.h"
%}
%pragma(python) include="engine/node.spy"

class Node {
public:
  int index();

  Coord position();

  const string &classname();
  void drawGridCell(GridSourcePtr, SimpleCellLayer*);
  // int ndof();
  // int neqn();

  %new StringVec *fieldNames();

  %addmethods {
    double __getitem__(int i) {
      return self->position()[i];
    }
    int uiIdentifier() {	// See comment in genericinfoGUI.py
      return self->index();
    }
  }
};

class FuncNode : public Node, public PointData {
public:
  Coord displaced_position(FEMesh*, double);
};

#endif // NODE_SWG
