// -*- C++ -*-
// $RCSfile: edge.C,v $
// $Revision: 1.26.10.5 $
// $Author: fyc $
// $Date: 2014/07/24 21:35:56 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/coord.h"
#include "common/tostring.h"
#include "engine/edge.h"
#include "engine/element.h"
#include "engine/elementnodeiterator.h"
#include "engine/femesh.h"
#include "engine/node.h"
#include <vector>
#include <math.h>   

// TODO MER: Edge and BoundaryEdge were written before we had
// MasterElement1D, et al, and the ability to have 1, 2, and 3D
// elements coexisting.  Do these classes duplicate each other?  Do we
// need BoundaryEdge if we can create true 1D elements?  At least, the
// integration done by BoundaryEdge should probably be done by
// MasterElement1D instead.

// Usual constructor if you're looking for an Edge object directly.
Edge::Edge(const Element *elin, const FuncNode *n0, const FuncNode *n1) :
  el(elin) {
  start = el->to_master(n0->position());
  end = el->to_master(n1->position());
  director = end - start;
}

// or this one, if you know the mastercoords of the endpoints.
Edge::Edge(const Element *elin, const MasterCoord &a, const MasterCoord &b)
  : el(elin)
{
  start = a;
  end = b;
  director = b - a;
}

// Compute the length of this edge in lab coordinates.  Note that this
// value can change when the node positions change, although this
// value does not change when the displacement field changes, i.e. it
// is the undistorted lab-frame edge length.
double Edge::lab_length() {
  Coord lab_director = el->from_master(end) - el->from_master(start);
  return sqrt(norm2(lab_director));
}

double Edge::master_length() const {
  return sqrt(norm2(director));
}


// Take a vector of doubles, each of which is a number between 0 and 
// one, and for each input value, output the corresponding real coordinate
// of the element.
std::vector<Coord*> *Edge::position_(const std::vector<double> *x) const {
  int size = x->size();
  std::vector<Coord*> *res = new std::vector<Coord*>(size);
  for(int i=0; i<size; i++) {
    // These Coords get passed out and are owned by Python:
    (*res)[i] = new Coord(el->from_master(start + (*x)[i]*director));
  }
  return res;
}

// Evaluate fields at positions along an edge, by hijacking the
// Element's field evaluator.  Given a list of edge coordinates
// between 0 and 1, return a list of lists of field components. The
// lists will be deleted by Python.

std::vector<OutputValue>*
Edge::outputFields(const FEMesh *mesh, const Field &field,
		   const std::vector<double> *positions)
  const
{
  std::vector<MasterCoord> mcpos(positions->size());
  for(std::vector<MasterCoord>::size_type i=0; i<mcpos.size(); i++)
    mcpos[i] = MasterCoord(start + (*positions)[i]*director);
  return el->outputFields(mesh, field, mcpos);
}

// std::vector<OutputValue>*
// Edge::outputFieldsAnyway(const CSubProblem *mesh, const Field &field,
// 			 const DoubleVec *positions) const
// {
//   std::vector<MasterCoord> mcpos(positions->size());
//   for(std::vector<MasterCoord>::size_type i=0; i<mcpos.size(); i++)
//     mcpos[i] = MasterCoord(start + (*positions)[i]*director);
//   return el->outputFieldsAnyway(mesh, field, mcpos);
// }

int Edge::order() {
  return el->mapfun_degree();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

BoundaryEdge::BoundaryEdge(const Element *elin, int n)
  : Edge(elin),
    nfuncnodes(n),
    complete(false)
{ 
//   Trace("BoundaryEdge::BoundaryEdge, nfuncnodes = " + to_string(n) );
  nlist.reserve(n);
} 


// Equality checker -- helps you to search for an edge when
// all you know are its nodes.
bool BoundaryEdge::edge_match(const FuncNode *n0, const FuncNode *n1) {
  if (nlist.empty() || nlist.size()==1)
    return false;
  return (*nlist[0].funcnode() == *n0) &&
    (*nlist[nlist.size()-1].funcnode() == *n1);
}  

// The endpoint coordinates are derived from the nodes,
// so it makes sense to add those in automatically
// when the nodes themselves are added to the edge.
//   Likewise, for the edge integration, we're going
// to need to be able to return the appropriate shape
// function index.  This is why we pass in an iterator.
void BoundaryEdge::add_node(const ElementFuncNodeIterator &in) {
  
//   Trace("BoundaryEdge::add_node: FuncNodeIterator=" + to_string(in));
  // NB Nodes *must* be passed in in order.  Take
  // both FuncNode and shapefunctionindex from the passed-in iterator.
  // Use the size of the array to detect the first and last nodes.
  if(nlist.empty()) {
    start=in.mastercoord();
  }
  if(int(nlist.size())==nfuncnodes-1) {
    end = in.mastercoord();
    director = end - start;
    complete = true;
  }
  nlist.push_back(in);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//


EdgeNodePositionIterator BoundaryEdge::node_positerator() const {
  if(!complete) {
    throw ErrProgrammingError("Cannot iterate over incomplete BoundaryEdge",
			      __FILE__, __LINE__);
  }
  return EdgeNodePositionIterator(*this);
}

EdgeNodeIterator BoundaryEdge::node_iterator() const {
  if(!complete) {
    throw ErrProgrammingError("Cannot iterate over incomplete BoundaryEdge",
			      __FILE__, __LINE__);
  }
  return EdgeNodeIterator(*this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

EdgeNodePositionIterator::EdgeNodePositionIterator(const BoundaryEdge &edge)
  : ElementShapeFuncIterator(*edge.el),
    ed(edge)
{}

EdgeNodePositionIterator::EdgeNodePositionIterator(
					   const EdgeNodePositionIterator &that)
  : ElementShapeFuncIterator(that),
    ed(that.ed)
{}

EdgeNodeIterator::EdgeNodeIterator(const BoundaryEdge &edge)
  : ElNodeIterator<EdgeNodePositionIterator, BoundaryEdge>(edge)
{}

EdgeNodeIterator::EdgeNodeIterator(const EdgeNodeIterator &that)
  : ElNodeIterator<EdgeNodePositionIterator, BoundaryEdge>(that)
{}

bool EdgeNodePositionIterator::end() const {
  return !start && index_ == startpt;
}

int EdgeNodePositionIterator::mlistindex() const {
  return ed.nlist[index_].mlistindex();
}

EdgeNodePositionIterator &
EdgeNodePositionIterator::operator=(const EdgeNodePositionIterator &that)
{
  if(&ed != &that.ed)
    throw ErrProgrammingError("Attempt to switch edge iterators in mid stream",
			      __FILE__, __LINE__);
  ElementShapeFuncIterator::operator=(that);
  return *this;
}

EdgeNodeIterator &EdgeNodeIterator::operator=(const EdgeNodeIterator &that) {
  EdgeNodePositionIterator::operator=(that);
  return *this;
}

EdgeNodePositionIterator EdgeNodePositionIterator::operator+(int n) {
  EdgeNodePositionIterator result(*this);
  result += n;
  return result;
}

EdgeNodeIterator EdgeNodeIterator::operator+(int n) {
  EdgeNodeIterator result(*this);
  result += n;
  return result;
}

EdgeNodePositionIterator &EdgeNodePositionIterator::operator+=(int n) {
  index_ = (index_ + n) % ed.nlist.size();
  start = false;  
  return *this;
}

EdgeNodeIterator &EdgeNodeIterator::operator+=(int n) {
  EdgeNodePositionIterator::operator+=(n);
  return *this;
}

const FuncNode *EdgeNodeIterator::funcnode() const
{
  return ed.nlist[index_].funcnode();
}

double EdgeNodePositionIterator::fraction() const
{
  MasterCoord pos = ed.nlist[index_].mastercoord();
  MasterCoord interval = pos - ed.startpt();
  // Positive assumption is OK because nodes come in sequence.
  return sqrt(norm2(interval))/ed.master_length();
}

double EdgeNodePositionIterator::shapefunction(const MasterPosition &p) const {
  return ed.nlist[index_].shapefunction(p);
}

// shapefunction derivatives wrt real space coordinates
double EdgeNodePositionIterator::dshapefunction(SpaceIndex i,
						const MasterPosition &p)
  const
{
  return ed.nlist[index_].dshapefunction(i, p);
}

// shapefunction derivatives wrt master space coordinates
double EdgeNodePositionIterator::masterderiv(SpaceIndex i,
					     const MasterPosition &p)
  const
{
  return ed.nlist[index_].masterderiv(i, p);
}

void EdgeNodePositionIterator::print(std::ostream &os) const {
  os << "EdgeNodePositionIterator(" << index_ << "(" << mlistindex() << "))";
}

void EdgeNodeIterator::print(std::ostream &os) const {
  os << "EdgeNodeIterator(" << index_ << "(" << mlistindex() << "), "
     << *node() << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

EdgeGaussPoint BoundaryEdge::integrator(int order) const {
  return EdgeGaussPoint(this, (order < 0 ? 0 : order));
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//
