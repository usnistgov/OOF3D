// -*- C++ -*-
// $RCSfile: elementnodeiterator.C,v $
// $Revision: 1.16.6.5 $
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

#include <oofconfig.h>

#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/mastercoord.h"
#include "engine/masterelement.h"
#include "engine/ooferror.h"

ElementNodePositionIterator::ElementNodePositionIterator(const ElementBase &el)
  : element_(el),
    index_(0),
    startpt(0),
    start(true)
{}

ElementNodePositionIterator::ElementNodePositionIterator(
				 const ElementNodePositionIterator &that)
  : element_(that.element_),
    index_(that.index_),
    startpt(that.startpt),
    start(that.start)
{}

ElementNodePositionIterator &
ElementNodePositionIterator::operator=(const ElementNodePositionIterator &that)
{
  if(&element_ != &that.element_)
    throw ErrProgrammingError("attempt to switch iterators in mid stream",
			      __FILE__, __LINE__);
  index_ = that.index_;
  startpt = that.startpt;
  start = that.start;
  return *this;
}

ElementNodePositionIterator &ElementNodePositionIterator::operator+=(int n) {
  start = false;
  index_ = (index_ + n) % element_.nnodes();
  return *this;
}

ElementNodePositionIterator ElementNodePositionIterator::operator+(int n) const 
{
  ElementNodePositionIterator result(*this);
  result += n;
  return result;
}

bool ElementNodePositionIterator::end() const {
  return !start && (index_ == startpt);
}

void ElementNodePositionIterator::set_start() {
  startpt = index_;
  start = true;
}

int ElementNodePositionIterator::mlistindex() const {
  return index_;
}

const ProtoNode *ElementNodePositionIterator::protonode() const {
  return element_.masterelement().protonode(mlistindex());
}

bool ElementNodePositionIterator::interior() const {
  return protonode()->nedges() == 0;
}

const MasterCoord &ElementNodePositionIterator::mastercoord() const {
  return protonode()->mastercoord();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Node *ElNodeIterator::node() const {
//   return dynamic_cast<Element&>(element()).nodelist[mlistindex()];
// }

// Node *ElNodeIterator::leftnode() const { 
//   return dynamic_cast<InterfaceElement&>(element()).get_leftnodelist()
//     [mlistindex()]; 
// }

// Node *ElNodeIterator::rightnode() const { 
//   return dynamic_cast<InterfaceElement&>(element()).get_rightnodelist()
//     [mlistindex()];
// }

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementNodeIterator::ElementNodeIterator(const Element &el)
  : ElNodeIterator<ElementNodePositionIterator, Element>(el)
{}

ElementNodeIterator::ElementNodeIterator(const ElementNodeIterator &that)
  : ElNodeIterator<ElementNodePositionIterator, Element>(that)
{}

ElementNodeIterator &ElementNodeIterator::operator+=(int n) {
  ElementNodePositionIterator::operator+=(n);
  return *this;
}

ElementNodeIterator ElementNodeIterator::operator+(int n) const {
  ElementNodeIterator result(*this);
  result += n;
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementShapeFuncIterator::ElementShapeFuncIterator(const ElementBase &el)
  : ElementNodePositionIterator(el)
{}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementMapNodePositionIterator::ElementMapNodePositionIterator(
						       const ElementBase &el)
  : ElementShapeFuncIterator(el)
{}

ElementMapNodePositionIterator::ElementMapNodePositionIterator(const
				       ElementMapNodePositionIterator &that)
  : ElementShapeFuncIterator(that)
{}

ElementMapNodePositionIterator &
ElementMapNodePositionIterator::operator=(
				  const ElementMapNodePositionIterator &that) 
{
  ElementShapeFuncIterator::operator=(that);
  return *this;
}

int ElementMapNodePositionIterator::mlistindex() const {
  return element_.masterelement().mapnodes[index_];
}

ElementMapNodePositionIterator &ElementMapNodePositionIterator::operator+=(
								   int n) 
{
  start = false;
  index_ = (index_ + n) % element_.nmapnodes();
  return *this;
}

ElementMapNodePositionIterator ElementMapNodePositionIterator::operator+(int n)
  const 
{
  ElementMapNodePositionIterator result(*this);
  result += n;
  return result;
}

double ElementMapNodePositionIterator::shapefunction(const MasterPosition &pos)
  const 
{
  return element_.master.mapfunction->value(index_, pos);
}

double ElementMapNodePositionIterator::dshapefunction(SpaceIndex i,
					      const MasterPosition &pos)
  const
{
  return element_.master.mapfunction->realderiv(&element_, index_, i, pos);
}

double ElementMapNodePositionIterator::masterderiv(SpaceIndex i,
					   const MasterPosition &pos) 
  const
{
  return element_.master.mapfunction->masterderiv(index_, i, pos);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementMapNodeIterator::ElementMapNodeIterator(const Element &el)
  : ElNodeIterator<ElementMapNodePositionIterator, Element>(el)
{}

ElementMapNodeIterator::ElementMapNodeIterator(const ElementMapNodeIterator &it)
  : ElNodeIterator<ElementMapNodePositionIterator, Element>(it)
{}

ElementMapNodeIterator &ElementMapNodeIterator::operator=(
					  const ElementMapNodeIterator &that)
{
  ElementMapNodePositionIterator::operator=(that);
  return *this;
}

ElementMapNodeIterator &ElementMapNodeIterator::operator+=(int n) {
  ElementMapNodePositionIterator::operator+=(n);
  return *this;
}

ElementMapNodeIterator ElementMapNodeIterator::operator+(int n) const {
  ElementMapNodeIterator result(*this);
  result += n;
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementFuncNodePositionIterator::ElementFuncNodePositionIterator(
							 const ElementBase &el)
  : ElementShapeFuncIterator(el)
{}

ElementFuncNodePositionIterator::ElementFuncNodePositionIterator(
				 const ElementFuncNodePositionIterator &that)
  : ElementShapeFuncIterator(that)
{}

ElementFuncNodePositionIterator &
ElementFuncNodePositionIterator::operator=(
				   const ElementFuncNodePositionIterator &that)
{
  ElementShapeFuncIterator::operator=(that);
  return *this;
}

int ElementFuncNodePositionIterator::mlistindex() const {
  return element_.masterelement().funcnodes[index_];
}

ElementFuncNodePositionIterator &ElementFuncNodePositionIterator::operator+=(
								     int n)
{
  ElementFuncNodePositionIterator::operator+=(n);
  return *this;
}

ElementFuncNodePositionIterator ElementFuncNodePositionIterator::operator+(
								   int n)
  const 
{
  ElementFuncNodePositionIterator result(*this);
  result += n;
  return result;
}

FuncNode *ElementFuncNodeIterator::funcnode() const {
  return dynamic_cast<FuncNode*>(node());
}

double ElementFuncNodePositionIterator::shapefunction(const MasterPosition &pos)
  const 
{
  return element_.master.shapefunction->value(index_, pos);
}

double ElementFuncNodePositionIterator::dshapefunction(SpaceIndex i,
					       const MasterPosition &pos) const
{
  return element_.master.shapefunction->realderiv(&element_, index_, i, pos);
}

double ElementFuncNodePositionIterator::masterderiv(SpaceIndex i,
					    const MasterPosition &mc) const
{
  return element_.master.shapefunction->masterderiv(index_, i, mc);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementFuncNodeIterator::ElementFuncNodeIterator(const Element &el)
  : ElNodeIterator<ElementFuncNodePositionIterator, Element>(el),
    dofsum(0)
{}

ElementFuncNodeIterator::ElementFuncNodeIterator(const
						 ElementFuncNodeIterator &that)
  : ElNodeIterator<ElementFuncNodePositionIterator, Element>(that),
    dofsum(that.dofsum)
{}

ElementFuncNodeIterator &
ElementFuncNodeIterator::operator=(const ElementFuncNodeIterator &that) {
  ElementFuncNodePositionIterator::operator=(that);
  dofsum = that.dofsum;
  return *this;
}

ElementFuncNodeIterator &ElementFuncNodeIterator::operator+=(int n) {
  start = false;
  for(int i=0; i<n; i++) {
    dofsum += funcnode()->ndof();
    index_ = (index_ + 1) % element_.nfuncnodes();
    if(index_ == startpt)	// we've wrapped around
      dofsum = 0;
  }
  return *this;
}

ElementFuncNodeIterator ElementFuncNodeIterator::operator+(int n) const {
  ElementFuncNodeIterator result(*this);
  result += n;
  return result;
}

void ElementFuncNodeIterator::set_start() {
  dofsum = 0;
  ElementFuncNodePositionIterator::set_start();
}

int ElementFuncNodeIterator::localindex(const Field &field,
					const FieldIndex *component)
  const
{
  return dofsum + field.localindex(funcnode(), *component);
}

bool ElementFuncNodeIterator::hasField(const Field &field) const {
  return funcnode()->hasField(field);
}

bool ElementFuncNodeIterator::hasEquation(const Equation &equation) const {
  return funcnode()->hasEquation(equation);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

#ifdef INTERFACEELEMENTS

InterfaceElementFuncNodeIterator::
InterfaceElementFuncNodeIterator(const Element &el) :
  ElementFuncNodeIterator(el)
{
  side = ((InterfaceElement*)&el)->side();
}

InterfaceElementFuncNodeIterator::
InterfaceElementFuncNodeIterator(const 
				 InterfaceElementFuncNodeIterator &that) :
  ElementFuncNodeIterator(that),side(that.side)
{}
  
FuncNode *InterfaceElementFuncNodeIterator::funcnode() const {
  Node *res;
  if (side==LEFT) {
    res = ((InterfaceElement*)&element_)->get_leftnodelist()[mlistindex()];
  }
  else { // side==RIGHT, obviously...
    res = ((InterfaceElement*)&element_)->get_rightnodelist()[mlistindex()];
  }
  return dynamic_cast<FuncNode*>(res);
}

#endif // INTERFACEELEMENTS

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementExteriorNodePositionIterator::ElementExteriorNodePositionIterator(
							 const ElementBase &el)
  : ElementFuncNodePositionIterator(el)
{}

ElementExteriorNodeIterator::ElementExteriorNodeIterator(const Element &el)
  : ElNodeIterator<ElementExteriorNodePositionIterator, Element>(el)
{}

ElementExteriorNodePositionIterator::ElementExteriorNodePositionIterator(
			 const ElementExteriorNodePositionIterator &that)
  : ElementFuncNodePositionIterator(that)
{}

ElementExteriorNodeIterator::ElementExteriorNodeIterator(
				      const ElementExteriorNodeIterator &that)
  : ElNodeIterator<ElementExteriorNodePositionIterator, Element>(that)
{}

ElementExteriorNodePositionIterator&
ElementExteriorNodePositionIterator::operator=(
			       const ElementExteriorNodePositionIterator &that) 
{
  ElementFuncNodePositionIterator::operator=(that);
  return *this;
}

ElementExteriorNodeIterator&
ElementExteriorNodeIterator::operator=(const ElementExteriorNodeIterator &that) 
{
  ElementExteriorNodePositionIterator::operator=(that);
  return *this;
}

int ElementExteriorNodePositionIterator::mlistindex() const {
  return element_.masterelement().exteriorfuncnodes[index_];
}

ElementExteriorNodePositionIterator &
ElementExteriorNodePositionIterator::operator+=(int n) {
  start = false;
  index_ = (index_ + n) % element_.nexteriorfuncnodes();
  return *this;
}

ElementExteriorNodeIterator &ElementExteriorNodeIterator::operator+=(int n) {
  ElementExteriorNodePositionIterator::operator+=(n);
  return *this;
}

ElementExteriorNodePositionIterator
ElementExteriorNodePositionIterator::operator+(int n) const
{
  ElementExteriorNodePositionIterator result(*this);
  result += n;
  return result;
}

ElementExteriorNodeIterator ElementExteriorNodeIterator::operator+(int n) const
{
  ElementExteriorNodeIterator result(*this);
  result += n;
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ElementCornerNodePositionIterator::ElementCornerNodePositionIterator(
						     const ElementBase &el)
  : ElementNodePositionIterator(el)
{}

ElementCornerNodeIterator::ElementCornerNodeIterator(const Element &el)
  : ElNodeIterator<ElementCornerNodePositionIterator, Element>(el)
{}

ElementCornerNodePositionIterator::ElementCornerNodePositionIterator(
			     const ElementCornerNodePositionIterator &that)
  : ElementNodePositionIterator(that)
{}

ElementCornerNodeIterator::ElementCornerNodeIterator(
			  const ElementCornerNodeIterator &that)
  : ElNodeIterator<ElementCornerNodePositionIterator, Element>(that)
{}

ElementCornerNodePositionIterator &
ElementCornerNodePositionIterator::operator=(
			     const ElementCornerNodePositionIterator &that)
{
  ElementNodePositionIterator::operator=(that);
  return *this;
}

ElementCornerNodeIterator &
ElementCornerNodeIterator::operator=(const ElementCornerNodeIterator &that) {
  ElementCornerNodePositionIterator::operator=(that);
  return *this;
}

int ElementCornerNodePositionIterator::mlistindex() const {
  return element_.masterelement().cornernodes[index_];
}

ElementCornerNodePositionIterator &
ElementCornerNodePositionIterator::operator+=(int n) {
  start = false;
  index_ = (index_ + n) % element_.ncorners();
  return *this;
}

ElementCornerNodeIterator &ElementCornerNodeIterator::operator+=(int n) {
  ElementCornerNodePositionIterator::operator+=(n);
  return *this;
}

ElementCornerNodePositionIterator 
ElementCornerNodePositionIterator::operator+(int n) const {
  ElementCornerNodePositionIterator result(*this);
  result += n;
  return result;
}

ElementCornerNodeIterator ElementCornerNodeIterator::operator+(int n) const {
  ElementCornerNodeIterator result(*this);
  result += n;
  return result;
}

ElementFuncNodePositionIterator 
ElementCornerNodePositionIterator::funcnode_iterator() const {
  // create an ElementFuncNodePositionIterator that starts at the current node
  ElementFuncNodePositionIterator fni(element_);
  const ProtoNode *pnode = protonode();
  while(fni.protonode() != pnode && !fni.end()) // ugly
    ++fni;
  if(fni.end())
    throw ErrProgrammingError("Unable to convert a cornernode to a funcnode",
			      __FILE__, __LINE__);
  fni.set_start();
  return fni;
}

ElementFuncNodeIterator ElementCornerNodeIterator::funcnode_iterator() const {
  // create an ElementFuncNodeIterator that starts at the current node
  ElementFuncNodeIterator fni(dynamic_cast<const Element&>(element_));
  const ProtoNode *pnode = protonode();
  while(fni.protonode() != pnode && !fni.end()) // ugly
    ++fni;
  if(fni.end())
    throw ErrProgrammingError("Unable to convert a cornernode to a funcnode",
			      __FILE__, __LINE__);
  fni.set_start();
  return fni;
}

ElementExteriorNodePositionIterator 
ElementCornerNodePositionIterator::exteriornode_iterator()
  const
{
  ElementExteriorNodePositionIterator eni(element_);
  const ProtoNode *pnode = protonode();
  while(eni.protonode() != pnode && !eni.end())
    ++eni;
  if(eni.end())
    throw ErrProgrammingError(
		      "Unable to convert a cornernode to an exterior node",
		      __FILE__, __LINE__);
  eni.set_start();
  return eni;
}

ElementExteriorNodeIterator ElementCornerNodeIterator::exteriornode_iterator()
  const
{
  ElementExteriorNodeIterator eni(dynamic_cast<const Element&>(element_));
  const ProtoNode *pnode = protonode();
  while(eni.protonode() != pnode && !eni.end())
    ++eni;
  if(eni.end())
    throw ErrProgrammingError(
		      "Unable to convert a cornernode to an exterior node",
		      __FILE__, __LINE__);
  eni.set_start();
  return eni;
}

ElementMapNodePositionIterator
ElementCornerNodePositionIterator::mapnode_iterator() const {
  ElementMapNodePositionIterator mni(element_);
  const ProtoNode *pnode = protonode();
  while(mni.protonode() != pnode && !mni.end())
    ++mni;
  if(mni.end())
    throw ErrProgrammingError("Unable to convert a cornernode to a map node",
			      __FILE__, __LINE__);
  mni.set_start();
  return mni;
}

ElementMapNodeIterator ElementCornerNodeIterator::mapnode_iterator() const {
  ElementMapNodeIterator mni(dynamic_cast<const Element&>(element_));
  const ProtoNode *pnode = protonode();
  while(mni.protonode() != pnode && !mni.end())
    ++mni;
  if(mni.end())
    throw ErrProgrammingError("Unable to convert a cornernode to a map node",
			      __FILE__, __LINE__);
  mni.set_start();
  return mni;
}

FuncNode *ElementCornerNodeIterator::funcnode() const {
  return dynamic_cast<FuncNode*>(node());
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

void ElementNodePositionIterator::print(std::ostream &os) const {
  os << "ElementNodePositionIterator(" << index_ << "(" << mlistindex() << "))";
}

void ElementNodeIterator::print(std::ostream &os) const {
  os << "ElementNodeIterator(" << index_ << "(" << mlistindex() << "), "
     << *node() << ")";
}

void ElementMapNodePositionIterator::print(std::ostream &os) const {
  os << "ElementMapNodePositionIterator(" << index_ << "(" << mlistindex() 
     << "))";
}

void ElementMapNodeIterator::print(std::ostream &os) const {
  os << "ElementMapNodeIterator(" << index_ << "(" << mlistindex() << "), "
     << *node() << ")";
}

void ElementFuncNodePositionIterator::print(std::ostream &os) const {
  os << "ElementFuncNodePositionIterator(" << index_ << "(" << mlistindex()
     << "))";
}

void ElementFuncNodeIterator::print(std::ostream &os) const {
  os << "ElementFuncNodeIterator(" << index_ << "(" << mlistindex() << "), "
     << *node() << ")";
}

void ElementCornerNodePositionIterator::print(std::ostream &os) const {
  os << "ElementCornerNodePositionIterator(" << index_ << "(" << mlistindex()
     << "))";
}

void ElementExteriorNodePositionIterator::print(std::ostream &os) const {
  os << "ElementExteriorNodePositionIterator(" << index_ << "(" << mlistindex()
     << "))";
}

void ElementCornerNodeIterator::print(std::ostream &os) const {
  os << "ElementCornerNodeIterator(" << index_ << "(" << mlistindex() << "), "
     << *node() << " " << mastercoord() << ")";
}

void ElementExteriorNodeIterator::print(std::ostream &os) const {
  os << "ElementExteriorNodeIterator(" << index_ << "(" << mlistindex() << "), "
     << *node() << " " << mastercoord() << ")";
}

#ifdef INTERFACEELEMENTS
void InterfaceElementFuncNodeIterator::print(std::ostream &os) const {
  os << "InterfaceElementFuncNodeIterator(" << index_ << "(" << mlistindex()
     << "), " << *funcnode() << " " << mastercoord() << ")";
}
#endif // INTERFACEELEMENTS

std::ostream &operator<<(std::ostream &os,
			 const ElementNodePositionIterator &eni)
{
  eni.print(os);
  return os;
}

