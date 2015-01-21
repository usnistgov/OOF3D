// -*- C++ -*-
// $RCSfile: edge.swg,v $
// $Revision: 1.23.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:43 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef EDGE_SWG
#define EDGE_SWG

%module edge
%include "engine/typemaps.swg"
%pragma(python) include="edge.spy"
%extern "engine/field.swg"
// %extern "engine/csubproblem.swg"
%extern "engine/node.swg"
%extern "engine/element.swg"

%{
#include "engine/edge.h"
%}


class Edge {
public:
  Edge(const Element *, const FuncNode*, const FuncNode*);
  ~Edge();
  %new CoordVec* position_(DoubleList*);
  %new OutputValueVec *outputFields(const FEMesh*, const Field&, DoubleList*);
//   %new OutputValueVec *outputFieldsAnyway(const CSubProblem*, const Field&,
// 					  DoubleList*);
  int order();
  MasterCoord startpt();
  MasterCoord endpt();
};

class BoundaryEdge : public Edge  {
public:
  BoundaryEdge(const Element *elin, int n);
  ~BoundaryEdge();
  bool edge_match(const FuncNode *, const FuncNode *);
  Element *element();
  Node *startnode();
  Node *endnode();
};

#endif // EDGE_SWG
