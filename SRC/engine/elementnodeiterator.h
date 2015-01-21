// -*- C++ -*-
// $RCSfile: elementnodeiterator.h,v $
// $Revision: 1.15.16.6 $
// $Author: langer $
// $Date: 2014/12/14 22:49:18 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ELEMENTNODEITERATOR_H
#define ELEMENTNODEITERATOR_H

#include "common/coord_i.h"
#include "engine/element.h"
#include "engine/indextypes.h"
#include "node.h"

class Equation;
class Field;
class GaussPoint;
class MasterCoord;
class MasterPosition;
class FEMesh;
class Position;
class ProtoNode;

// The ElementNodePositionIterator is used for looping over all nodes
// (lower case) of an ElementBase or its derived classes, and is the
// base class for the specialized iterators, which loop over subsets
// of the nodes.  Classes which are also derived from ElNodeIterator
// can access the nodes themselves, not just their positions, and
// don't have "Position" in their name.  They can't be used with
// ElementLites, which don't have Nodes.

class ElementNodePositionIterator {	// for looping over all nodes
protected:
  const ElementBase &element_;
  ShapeFunctionIndex index_;	// where we are now
  int startpt;			// where we started from
  bool start;			// are we just starting?

public:
  ElementNodePositionIterator(const ElementBase&);
  ElementNodePositionIterator(const ElementNodePositionIterator&);
  virtual ~ElementNodePositionIterator() {}
  ElementNodePositionIterator &operator=(const ElementNodePositionIterator&);

  // Go to the node n farther along in the sequence
  virtual ElementNodePositionIterator &operator+=(int);	// returns *this
  // These two incrementation operators are implemented in terms of operator+=
  ElementNodePositionIterator &operator++() { return operator+=(1); }
  ElementNodePositionIterator operator+(int) const;

  virtual bool end() const;	// are we done iterating?
  virtual void set_start();	// pretend we started at the current point

  // various representations of the current point
  const ProtoNode *protonode() const;
  const MasterCoord &mastercoord() const;
  Coord position() const { return element_.position(mlistindex()); }

  bool interior() const;	// are we at an interior node?

  const ElementBase &element() const {  // over whom we're looping
    return element_; 
  }

  // mlistindex() establishes the correspondence between index of a
  // node in the iterator and the index in the element's and
  // masterelement's nodelists.  By using this virtual function, most
  // of the other functions in the ElementNodeIterator hierarchy need
  // only be defined in the base class.  It returns the index in the
  // master element corresponding to the current index_ in the
  // iterator.
  virtual int mlistindex() const;

  // miscellany
  ShapeFunctionIndex index() const { return index_; }
  virtual void print(std::ostream&) const;
};

// Classes derived from ElNodeIterator can also return the actual Node
// that they're pointing to.  Doing so requires that the ElementBase
// that they've been constructed with is actually an Element.

template <class BASE, class ITERAND>
class ElNodeIterator : public BASE {
public:
  ElNodeIterator(const ITERAND &obj) : BASE(obj) {}
  Node *node() const {
    return dynamic_cast<const Element&>(
			BASE::element()).get_nodelist()[BASE::mlistindex()];
  }
  // //Cheap way to get the nodes that are 'partnered' with the main
  // //interface element nodes. Can only be used if the Element really is
  // //an InterfaceElement, otherwise, a more sophisticated typecasting
  // //mechanism is required.  TODO 3.1: Provide a more sophisticated
  // //typecasting mechanism.
  // Node *leftnode() const {
  //   return dynamic_cast<const InterfaceElement&>(
  // 		 BASE::element()).get_leftnodelist()[BASE::mlistindex()]; 
  // }
  // Node *rightnode() const { 
  //   return dynamic_cast<const InterfaceElement&>(
  // 		 BASE::element()).get_rightnodelist()[BASE::mlistindex()];
  // }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Abstract base class for Iterators which can be used to evaluate
// shape functions.

class ElementShapeFuncIterator : public ElementNodePositionIterator {
public:
  ElementShapeFuncIterator(const ElementBase&);
  virtual int mlistindex() const = 0;
  virtual ElementShapeFuncIterator &operator+=(int) = 0;
  // shapefunctions corresponding to this node
  virtual double shapefunction(const MasterPosition&) const = 0;
  // shapefunction derivatives wrt real space coordinates
  virtual double dshapefunction(SpaceIndex, const MasterPosition&) const = 0;
  // shapefunction derivatives wrt master space coordinates
  virtual double masterderiv(SpaceIndex, const MasterPosition&) const = 0;
  virtual void print(std::ostream&) const = 0;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ElementNodeIterator 
  : public ElNodeIterator<ElementNodePositionIterator, Element>
{
public:
  ElementNodeIterator(const Element&);
  ElementNodeIterator(const ElementNodeIterator&);
  virtual ElementNodeIterator &operator+=(int);	// returns *this
  ElementNodeIterator &operator++() { return operator+=(1); } // returns *this
  ElementNodeIterator operator+(int) const; // returns new object (not *this)
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ElementMapNodePositionIterator : public ElementShapeFuncIterator {
public:
  ElementMapNodePositionIterator(const ElementBase&);
  ElementMapNodePositionIterator(const ElementMapNodePositionIterator&);
  ElementMapNodePositionIterator &operator=(
				    const ElementMapNodePositionIterator&);
  virtual ElementMapNodePositionIterator &operator+=(int);
  ElementMapNodePositionIterator operator+(int) const;
  virtual int mlistindex() const;
  // shapefunctions corresponding to this node
  virtual double shapefunction(const MasterPosition&) const;
  // shapefunction derivatives wrt real space coordinates
  virtual double dshapefunction(SpaceIndex, const MasterPosition&) const;
  // shapefunction derivatives wrt master space coordinates
  virtual double masterderiv(SpaceIndex, const MasterPosition&) const;
  virtual void print(std::ostream&) const;
};

class ElementMapNodeIterator 
  : public ElNodeIterator<ElementMapNodePositionIterator, Element>
{
public:
  ElementMapNodeIterator(const Element&);
  ElementMapNodeIterator(const ElementMapNodeIterator&);
  ElementMapNodeIterator &operator=(const ElementMapNodeIterator&);
  virtual ElementMapNodeIterator &operator+=(int);
  ElementMapNodeIterator operator+(int) const;
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ElementFuncNodePositionIterator : public ElementShapeFuncIterator {
public:
  ElementFuncNodePositionIterator(const ElementBase&);
  ElementFuncNodePositionIterator(const ElementFuncNodePositionIterator&);
  virtual ~ElementFuncNodePositionIterator() {}
  ElementFuncNodePositionIterator &operator=(
				     const ElementFuncNodePositionIterator&);
  virtual ElementFuncNodePositionIterator &operator+=(int);
  ElementFuncNodePositionIterator operator+(int) const;
  virtual int mlistindex() const;
  // shapefunctions corresponding to this node
  virtual double shapefunction(const MasterPosition&) const;
  // shapefunction derivatives wrt real space coordinates
  virtual double dshapefunction(SpaceIndex, const MasterPosition&) const;
  // shapefunction derivatives wrt master space coordinates
  virtual double masterderiv(SpaceIndex, const MasterPosition&) const;
  virtual void print(std::ostream&) const;
};

class ElementFuncNodeIterator
  : public ElNodeIterator<ElementFuncNodePositionIterator, Element>
{
protected:
  int dofsum;			// no. of dofs seen so far
public:
  ElementFuncNodeIterator(const Element&);
  ElementFuncNodeIterator(const ElementFuncNodeIterator&);
  virtual ~ElementFuncNodeIterator() {}
  ElementFuncNodeIterator &operator=(const ElementFuncNodeIterator&);
  virtual ElementFuncNodeIterator &operator+=(int);
  ElementFuncNodeIterator operator+(int) const;
  virtual void set_start();
  virtual FuncNode *funcnode() const;

  bool hasField(const Field&) const;
  bool hasEquation(const Equation&) const;
  int localindex(const Field&, const FieldIndex*) const;
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef INTERFACEELEMENTS

class InterfaceElementFuncNodeIterator : public ElementFuncNodeIterator {
private:
  Sidedness side;
public:
  InterfaceElementFuncNodeIterator(const Element&);
  InterfaceElementFuncNodeIterator(const InterfaceElementFuncNodeIterator&);
  virtual FuncNode *funcnode() const;
  virtual void print(std::ostream&) const;
};

#endif // INTERFACEELEMENTS

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// ElementExteriorNodeIterator should really be called
// "ElementExteriorFuncNodeIterator", but the name is too long to
// type.

class ElementExteriorNodePositionIterator 
  : public ElementFuncNodePositionIterator
{
public:
  ElementExteriorNodePositionIterator(const ElementBase&);
  ElementExteriorNodePositionIterator(
			      const ElementExteriorNodePositionIterator&);
  virtual ~ElementExteriorNodePositionIterator() {}
  ElementExteriorNodePositionIterator &operator=(
				 const ElementExteriorNodePositionIterator&);
  ElementExteriorNodePositionIterator operator+(int) const;
  virtual ElementExteriorNodePositionIterator &operator+=(int);
  virtual int mlistindex() const;
  virtual void print(std::ostream&) const;
};

class ElementExteriorNodeIterator 
  : public ElNodeIterator<ElementExteriorNodePositionIterator, Element>
{
public:
  ElementExteriorNodeIterator(const Element&);
  ElementExteriorNodeIterator(const ElementExteriorNodeIterator&);
  virtual ~ElementExteriorNodeIterator() {}
  ElementExteriorNodeIterator& operator=(const ElementExteriorNodeIterator&);
  ElementExteriorNodeIterator operator+(int) const;
  virtual ElementExteriorNodeIterator &operator+=(int);
  virtual void print(std::ostream&) const;
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ElementCornerNodePositionIterator : public ElementNodePositionIterator {
public:
  ElementCornerNodePositionIterator(const ElementBase&);
  ElementCornerNodePositionIterator(const ElementCornerNodePositionIterator&);
  virtual ~ElementCornerNodePositionIterator() {}
  ElementCornerNodePositionIterator &operator=(
			       const ElementCornerNodePositionIterator&);
  virtual ElementCornerNodePositionIterator &operator+=(int);
  ElementCornerNodePositionIterator operator+(int) const;
  virtual int mlistindex() const;
  ElementFuncNodePositionIterator funcnode_iterator() const;
  ElementMapNodePositionIterator mapnode_iterator() const;
  ElementExteriorNodePositionIterator exteriornode_iterator() const;
  virtual void print(std::ostream&) const;
};

class ElementCornerNodeIterator 
  : public ElNodeIterator<ElementCornerNodePositionIterator, Element>
{
public:
  ElementCornerNodeIterator(const Element&);
  ElementCornerNodeIterator(const ElementCornerNodeIterator&);
  virtual ~ElementCornerNodeIterator() {}
  ElementCornerNodeIterator &operator=(const ElementCornerNodeIterator&);
  virtual ElementCornerNodeIterator &operator+=(int);
  ElementCornerNodeIterator operator+(int) const;
  ElementFuncNodeIterator funcnode_iterator() const;
  ElementMapNodeIterator mapnode_iterator() const;
  ElementExteriorNodeIterator exteriornode_iterator() const;
  FuncNode *funcnode() const;
  virtual void print(std::ostream&) const;
};

std::ostream &operator<<(std::ostream&, const ElementNodePositionIterator&);

#endif
