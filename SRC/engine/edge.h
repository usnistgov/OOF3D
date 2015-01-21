// -*- C++ -*-
// $RCSfile: edge.h,v $
// $Revision: 1.19.10.5 $
// $Author: fyc $
// $Date: 2014/07/24 21:35:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef EDGE_H
#define EDGE_H

#include "engine/indextypes.h"
#include "engine/elementnodeiterator.h"
#include "engine/mastercoord.h"
#include <vector>

class EdgeGaussPoint;
class EdgeNodeIterator;
class EdgeNodePositionIterator;
class Element;
class CSubProblem;
class Field;
class Node;

// Elements are assumed to be polygonal, to have edges which 
// admit a conventional numbering in a master space which is
// known by the appropriate MasterElement class, to have nodes 
// at the corners of the polygon, and to have the property 
// that all the nodes which contribute to functions
// at an edge lie somewhere on the edge in question.
//
// These constraints might be generalized in the future if
// someday we go beyond finite elements, in which case the
// exact relation between the nodes and the edge will figure
// prominently in changes to this code.

// TODO MER: 3D The above assumptions need to be adjusted for 3D.
//
// The parent "Edge" class is a lightweight class primarily
// intended for use by the output code.  It consists of
// data about the endpoints in master space, an element pointer,
// and some methods for evaluating fields at points on the edge.
//
// The BoundaryEdge subclass is the more general object used
// by the boundaries and boundary condition classes.  
// BoundaryEdges borrow their parametricity (i.e. super, iso, or
// subparametric property) from their element.  Because the 
// boundaryedges don't own their nodes, there only needs to be one
// version of this class, and it uses the element's transformation
// machinery to do mapping.  Edges do know their starting and ending
// coordinates, and store indices to the appropriate shape
// functions, for integration purposes.  All this is added
// automatically (and invisibly to the caller) by the add_node
// routine.  The boundaryedge only collects the funcnodes.

class Edge {
protected:
  // start and end are positions in the 3D element master space.
  MasterCoord start, end, director;
  // Minimalist constructor is protected, so that only the BoundaryEdge
  // subclass can use it.  Used when you don't know the nodes at
  // construction time.
  Edge(const Element *elin) : el(elin) {}
public:
  const Element *el;
  Edge(const Element *, const FuncNode *, const FuncNode *);
  Edge(const Element*, const MasterCoord&, const MasterCoord&);
  virtual ~Edge() {}

  double lab_length();
  double master_length() const; 

  // Functions to support output to the GUI. The underscore in the
  // name is because this is meant to be called by a wrapper
  // function from Python.  The wrapper gets to be named "position".
  std::vector<Coord*>* position_(const std::vector<double>*) const;
  // Evaluate a Field at a bunch of positions along the edge.  The
  // positions are doubles between 0 and 1.
  std::vector<OutputValue>* outputFields(const FEMesh*, const Field&,
					 const std::vector<double>*) const;
//   // Evaluate a field even if it's not defined on the mesh (in which
//   // case it evaluates to zero).
//   std::vector<OutputValue>* outputFieldsAnyway(const CSubProblem*, const Field&,
// 					 const std::vector<double>*) const;
  MasterCoord startpt() const { return start; }
  MasterCoord endpt() const { return end; }
  int order();
};


// A BoundaryEdge is a heavier, less-often-used variant of an Edge.
// The BoundaryEdge has the information needed by Boundaries, in order to
// apply the various conditions -- most particularly, this includes 
// the list of FuncNodes and the node iteration machinery.
class BoundaryEdge : public Edge {
protected:
  std::vector<ElementFuncNodeIterator> nlist;
  int nfuncnodes;
  bool complete;
public:

  BoundaryEdge(const Element *elin, int n);

  virtual ~BoundaryEdge() {}

  void add_node(const ElementFuncNodeIterator&);
  
  bool edge_match(const FuncNode *, const FuncNode *);

  EdgeNodeIterator node_iterator() const;
  EdgeNodePositionIterator node_positerator() const;
  
  EdgeGaussPoint integrator(int) const;

  const Element *element() { return el; }
  const Node *startnode() { return nlist[0].node(); }
  const Node *endnode() { return nlist[nlist.size()-1].node(); }

  friend class EdgeNodeIterator;
  friend class EdgeNodePositionIterator;
  friend class EdgeGaussPoint;
};

// Derive EdgeNodeIterator from ElementNodeIteratorBase, provide
// same functionality to re-use the machinery from before.
//
// Operate on the existing node list.
// Instantiate by: ElementNodeIterator it ???
// class EdgeNodeIterator : public ElementFuncNodeIterator {
// private:
//   const BoundaryEdge *ed;
// public:
//   EdgeNodeIterator(const BoundaryEdge *edge)
//     : ed(edge),
//       ElementFuncNodeIterator(*edge->el)
//   {}
//   virtual ~EdgeNodeIterator() {}
//   EdgeNodeIterator &operator+=(int);
//   virtual ShapeFunctionIndex sf_index() const;
//   virtual const FuncNode *funcnode() const;
//   virtual int localindex(const FEMesh*, const Field&, const FieldIndex&) const;
// };  

class EdgeNodePositionIterator : public ElementShapeFuncIterator
{
protected:
  const BoundaryEdge &ed;
public:
  EdgeNodePositionIterator(const BoundaryEdge&);
  EdgeNodePositionIterator(const EdgeNodePositionIterator&);
  virtual ~EdgeNodePositionIterator() {}
  virtual bool end() const;
  EdgeNodePositionIterator &operator=(const EdgeNodePositionIterator&);
  EdgeNodePositionIterator operator+(int);
  virtual EdgeNodePositionIterator &operator+=(int);
  double fraction() const;
  virtual int mlistindex() const;
    // shapefunctions corresponding to this node
  virtual double shapefunction(const MasterPosition&) const;
  // shapefunction derivatives wrt real space coordinates
  virtual double dshapefunction(SpaceIndex, const MasterPosition&) const;
  // shapefunction derivatives wrt master space coordinates
  virtual double masterderiv(SpaceIndex, const MasterPosition&) const;
  virtual void print(std::ostream&) const;
};

class EdgeNodeIterator 
  : public ElNodeIterator<EdgeNodePositionIterator, BoundaryEdge> 
{
public:
  EdgeNodeIterator(const BoundaryEdge &edge);
  EdgeNodeIterator(const EdgeNodeIterator&);
  EdgeNodeIterator &operator=(const EdgeNodeIterator&);
  EdgeNodeIterator operator+(int);
  virtual EdgeNodeIterator &operator+=(int);
  const FuncNode *funcnode() const;
  virtual void print(std::ostream&) const;
};

#endif	// EDGE_H



