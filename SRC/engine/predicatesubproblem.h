// -*- C++ -*-
// $RCSfile: predicatesubproblem.h,v $
// $Revision: 1.10.2.2 $
// $Author: langer $
// $Date: 2014/01/05 03:20:03 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <iostream>

#include "common/cleverptr.h"

#ifndef PREDICATESUBPROBLEM_H
#define PREDICATESUBPROBLEM_H

// Template for SubProblems that are defined in terms of a predicate
// that chooses mesh elements.  The template parameter PRDCT is a
// callable object that takes two arguments, a const FEMesh* and a
// const Element*, and returns true if the Element is included in the
// subproblem.

template <class PRDCT> class PredicateSubProblem;
template <class PRDCT> class PredicateSubProblemElementIterator;
template <class PRDCT> class PredicateSubProblemNodeIterator;
template <class PRDCT> class PredicateSubProblemFuncNodeIterator;

#include "engine/csubproblem.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/meshiterator.h"
#include <iostream>
#include <set>

// NodeCompare is used as the Comparison operator for std::sets of
// Node*s and FuncNode*s.  It's not strictly necessary, but if it's
// not used, then the sets are ordered by the values of the Node*
// pointers, which may not be reproducible from run to run, which
// might hinder debugging.  Using NodeCompare guarantees that
// iterators over the sets of Nodes will return the same Node ordering
// each time.

struct NodeCompare {
  bool operator()(const Node* n1, const Node* n2) {
    return n1->index() < n2->index();
  }
};

template <class PRDCT>
class PredicateSubProblem : public CSubProblem {
protected:
  PRDCT predicate; // Not a reference!. PredicateSubProblem has own copy.
private:
  mutable std::set<Node*, NodeCompare> *nodes_;
  mutable std::set<FuncNode*, NodeCompare> *funcnodes_;
  std::set<Node*, NodeCompare> &nodes() const;
  std::set<FuncNode*, NodeCompare> &funcnodes() const;
public:
  PredicateSubProblem(const PRDCT &p)
    : predicate(p),
      nodes_(0),
      funcnodes_(0)
  {}
  virtual ~PredicateSubProblem();
  virtual void redefined();
  virtual ElementIterator element_iterator() const;
  virtual NodeIterator node_iterator() const;
  virtual FuncNodeIterator funcnode_iterator() const;
  virtual bool contains(const Element*) const;
  virtual bool containsNode(const Node*) const;
  friend class PredicateSubProblemElementIterator<PRDCT>;
  friend class PredicateSubProblemNodeIterator<PRDCT>;
  friend class PredicateSubProblemFuncNodeIterator<PRDCT>;
};

template <class PRDCT>
PredicateSubProblem<PRDCT>::~PredicateSubProblem() {
  if(nodes_) delete nodes_;
  if(funcnodes_) delete funcnodes_;
}

template <class PRDCT>
bool PredicateSubProblem<PRDCT>::contains(const Element *element) const {
  return predicate(mesh, element); // mesh is defined in CSubProblem
}

template <class PRDCT>
bool PredicateSubProblem<PRDCT>::containsNode(const Node *node) const {
  Node *nd = const_cast<Node*>(node);
  std::set<Node*, NodeCompare> &nds = nodes();
  std::set<Node*, NodeCompare>::iterator i=nds.find(nd);
  return i != nds.end();
}

template <class PRDCT>
void PredicateSubProblem<PRDCT>::redefined() {
  if(nodes_) delete nodes_;
  if(funcnodes_) delete funcnodes_;
  nodes_ = 0;
  funcnodes_ = 0;
}

template <class PRDCT>
std::set<Node*, NodeCompare> &PredicateSubProblem<PRDCT>::nodes() const {
  if(nodes_ == 0) {
    nodes_ = new std::set<Node*, NodeCompare>();
    for(ElementIterator
	  ei(const_cast<PredicateSubProblem<PRDCT>*>(this)->element_iterator());
	!ei.end(); ++ei)
      {
	for(ElementNodeIterator n(ei.element()->node_iterator()); !n.end(); ++n)
	  {
	    nodes_->insert(n.node());
	  }
      }
  }
  return *nodes_;
}

template <class PRDCT>
std::set<FuncNode*, NodeCompare> &PredicateSubProblem<PRDCT>::funcnodes() const
{
  if(funcnodes_ == 0) {
    funcnodes_ = new std::set<FuncNode*, NodeCompare>();
    for(ElementIterator
	  ei(const_cast<PredicateSubProblem<PRDCT>*>(this)->element_iterator());
	!ei.end(); ++ei)
      {
	for(CleverPtr<ElementFuncNodeIterator> n(ei.element()->
						 funcnode_iterator()); 
	    !n->end(); ++*n)
	  {
	    funcnodes_->insert(n->funcnode());
	  }
      }
  }
  return *funcnodes_;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class PRDCT>
class PredicateSubProblemElementIterator : public ElementIteratorBase {
private:
  const PredicateSubProblem<PRDCT> *subproblem;
  MeshElementIterator iter;
  int count_;
  mutable int size_;
  mutable bool size_computed_;
  bool ok(const FEMesh *mesh, const Element *elem) const {
    return subproblem->predicate(mesh, elem);
  }
public:
  PredicateSubProblemElementIterator(const PredicateSubProblem<PRDCT> *subp);
  PredicateSubProblemElementIterator(
			    const PredicateSubProblemElementIterator<PRDCT>&);
  virtual void operator++();
  virtual bool end() const { return iter.end(); }
  virtual int size() const;
  virtual int count() const { return count_; }
  virtual Element *element() const { return iter.element(); }
  virtual ElementIteratorBase *clone() const {
    return new PredicateSubProblemElementIterator<PRDCT>(*this);
  }
};

template <class PRDCT>
PredicateSubProblemElementIterator<PRDCT>::PredicateSubProblemElementIterator(
			       const PredicateSubProblem<PRDCT> *subp)
  : subproblem(subp),
    iter(subp->mesh),
    count_(0),
    size_(0),
    size_computed_(false)
{
  while(!iter.end() && !ok(subproblem->mesh, iter.element()))
    ++iter;
  if(!iter.end())
    count_++;
}

template <class PRDCT>
PredicateSubProblemElementIterator<PRDCT>::PredicateSubProblemElementIterator(
		      const PredicateSubProblemElementIterator<PRDCT> &other)
  : subproblem(other.subproblem),
    iter(*dynamic_cast<MeshElementIterator*>(other.iter.clone())),
    count_(other.count_),
    size_(other.size_),
    size_computed_(other.size_computed_)
{}

template <class PRDCT>
void PredicateSubProblemElementIterator<PRDCT>::operator++() {
  ++iter;
  while(!iter.end() && !ok(subproblem->mesh, iter.element()))
    ++iter;
  if(!iter.end())
    count_++;
}

template <class PRDCT>
int PredicateSubProblemElementIterator<PRDCT>::size() const {
  if(!size_computed_) {
    size_computed_ = true;
    size_ = 0;
    for(ElementIterator i(subproblem->mesh->element_iterator()); !i.end(); ++i){
      if(ok(subproblem->mesh, i.element()))
	 size_++;
    }
  }
  return size_;
}

template <class PRDCT>
ElementIterator PredicateSubProblem<PRDCT>::element_iterator() const {
  return ElementIterator(new PredicateSubProblemElementIterator<PRDCT>(this));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class PRDCT>
class PredicateSubProblemNodeIterator : public NodeIteratorBase {
private:
  const PredicateSubProblem<PRDCT> *const subproblem;
  std::set<Node*, NodeCompare> &nodes;
  std::set<Node*, NodeCompare>::iterator iter;
  int count_;
public:
  PredicateSubProblemNodeIterator(const PredicateSubProblem<PRDCT>*);
  virtual Node *node() const { return *iter; }
  virtual void operator++() { ++iter; ++count_; }
  virtual bool begin() const { return iter == nodes.begin(); }
  virtual bool end() const { return iter == nodes.end(); }
  virtual int size() const { return nodes.size(); }
  virtual NodeIteratorBase *clone() const {
    return new PredicateSubProblemNodeIterator<PRDCT>(*this);
  }
};

template <class PRDCT>
PredicateSubProblemNodeIterator<PRDCT>::PredicateSubProblemNodeIterator(
					const PredicateSubProblem<PRDCT> *subp)
  : subproblem(subp),
    nodes(subp->nodes()),	// creates list of nodes, if necessary
    iter(nodes.begin()),
    count_(0)
{}

template <class PRDCT>
NodeIterator PredicateSubProblem<PRDCT>::node_iterator() const {
  return NodeIterator(new PredicateSubProblemNodeIterator<PRDCT>(this));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template <class PRDCT>
class PredicateSubProblemFuncNodeIterator : public FuncNodeIteratorBase {
private:
  const PredicateSubProblem<PRDCT> *const subproblem;
  std::set<FuncNode*, NodeCompare> &funcnodes;
  std::set<FuncNode*, NodeCompare>::iterator iter;
  int count_;
public:
  PredicateSubProblemFuncNodeIterator(const PredicateSubProblem<PRDCT>*);
  virtual FuncNode *node() const { return *iter; }
  virtual void operator++() { ++iter; ++count_; }
  virtual bool begin() const { return iter == funcnodes.begin(); }
  virtual bool end() const { return iter == funcnodes.end(); }
  virtual int size() const { return funcnodes.size(); }
  int count() const { return count_; }
  virtual FuncNodeIteratorBase *clone() const {
    return new PredicateSubProblemFuncNodeIterator<PRDCT>(*this);
  }
};

template <class PRDCT>
PredicateSubProblemFuncNodeIterator<PRDCT>::PredicateSubProblemFuncNodeIterator(
					const PredicateSubProblem<PRDCT> *subp)
  : subproblem(subp),
    funcnodes(subp->funcnodes()),
    iter(funcnodes.begin()),
    count_(0)
{}

template <class PRDCT>
FuncNodeIterator PredicateSubProblem<PRDCT>::funcnode_iterator() const {
  return FuncNodeIterator(new PredicateSubProblemFuncNodeIterator<PRDCT>(this));
}

#endif // PREDICATESUBPROBLEM_H
