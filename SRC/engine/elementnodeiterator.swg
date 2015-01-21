// -*- C++ -*-
// $RCSfile: elementnodeiterator.swg,v $
// $Revision: 1.15.10.5 $
// $Author: langer $
// $Date: 2014/10/01 16:01:26 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ELEMENTNODEITERATOR_SWG
#define ELEMENTNODEITERATOR_SWG

%{
#include "engine/elementnodeiterator.h"
%}

%include "engine/typemaps.swg"

%pragma(python) code="from ooflib.SWIG.engine.node import *"
%extern "engine/node.swg"

// TODO OPT: Are these used in Python outside of the ElementNodeProxy
// machinery in element.spy?  Possibly in material properties that are
// implemented in Python.  I've commented out most of the swigged
// methods here, because they predate the ElementNodeProxy stuff, and
// it's not clear what's necessary.

class ElementNodePositionIterator {
public:
  ~ElementNodePositionIterator();
  bool end();
  Coord position();
  %addmethods {
    void increment() { ++*self; }
  }
};

class ElementNodeIterator : public ElementNodePositionIterator {
public:
   ~ElementNodeIterator();
  // bool end();
  Node *node();
  // Coord position();
  // Node *leftnode();
  // Node *rightnode();
  // void set_start();
  // %addmethods {
  //   void increment() {
  //     ++*self;
  //   }
  //   ElementNodeIterator next() {
  //     return *self + 1;
  //   }
  //   ElementNodeIterator __add__(int i) {
  //     return *self + i;
  //   }
  // }
};

class ElementShapeFuncIterator : public ElementNodeIterator {
public:
  double shapefunction(MasterPosition&);
  double dshapefunction(int, MasterPosition&);
};

class ElementMapNodeIterator : public ElementShapeFuncIterator {
  // %addmethods {
  //   ElementMapNodeIterator next() {
  //     return *self + 1;
  //   }
  //   ElementMapNodeIterator __add__(int i) {
  //     return *self + i;
  //   }
  // }
};

class ElementFuncNodeIterator : public ElementShapeFuncIterator {
public:
  FuncNode *funcnode();
  // %addmethods {
  //   ElementFuncNodeIterator next() {
  //     return *self + 1;
  //   }
  //   ElementFuncNodeIterator __add__(int i) {
  //     return *self + i;
  //   }
  // }
};

class ElementCornerNodeIterator : public ElementNodeIterator {
public:
  ElementFuncNodeIterator funcnode_iterator();
  // exteriornode_iterator is only used in 2D MeshInfoDisplay.drawElement
  // ElementExteriorNodeIterator exteriornode_iterator();

  // %addmethods {
  //   ElementCornerNodeIterator next() {
  //     return *self + 1;
  //   }
  //   ElementCornerNodeIterator __add__(int i) {
  //     return *self + i;
  //   }
  // }
};

class ElementFuncNodePositionIterator : public ElementNodePositionIterator {};
class ElementCornerNodePositionIterator : public ElementNodePositionIterator {};

class ElementExteriorNodeIterator : public ElementFuncNodeIterator {
public:
  // %addmethods {
  //   ElementExteriorNodeIterator next() {
  //     return *self + 1;
  //   }
  //   ElementExteriorNodeIterator __add__(int i) {
  //     return *self + 1;
  //   }
  // }
};

#endif // ELEMENTNODEITERATOR_SWG
