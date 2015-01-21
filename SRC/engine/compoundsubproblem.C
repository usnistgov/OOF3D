// -*- C++ -*-
// $RCSfile: compoundsubproblem.C,v $
// $Revision: 1.7.2.3 $
// $Author: fyc $
// $Date: 2014/04/18 19:59:59 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <algorithm>
#include <iterator>

#include "common/IO/oofcerr.h"
#include "engine/compoundsubproblem.h"

BinarySubproblemPredicate::BinarySubproblemPredicate(CSubProblem *a,
						     CSubProblem *b)
  : subA(a),
    subB(b)
{}

BinarySubproblemPredicate::~BinarySubproblemPredicate() {

}

//-------------

bool UnionSBPredicate::operator()(const FEMesh *mesh, const Element *el)
  const
{
  if(subA->consistency == false || subB->consistency == false){
    return false;
  }else{
    return subA->contains(el) || subB->contains(el);
  }
}

CUnionSubProblem::~CUnionSubProblem() {

}

MaterialSet *CUnionSubProblem::getMaterials() const {
  MaterialSet *matlsA = predicate.subA->getMaterials();
  MaterialSet *matlsB = predicate.subB->getMaterials();
  MaterialSet *matls = new MaterialSet();
  std::set_union(matlsA->begin(), matlsA->end(),
		 matlsB->begin(), matlsB->end(),
		 std::insert_iterator<MaterialSet>(*matls, matls->begin()
		 )
    );
  delete matlsA;
  delete matlsB;
  return matls;
}

//------------

void CUnionSubProblem::updateDependencyA(CSubProblem *n)
{
  predicate.updateA(n);
  redefined();
}

void CUnionSubProblem::updateDependencyB(CSubProblem *n)
{
  predicate.updateB(n);
  redefined();
}

//-------------

bool IntersectionSBPredicate::operator()(const FEMesh *mesh, const Element *el)
  const
{
  if(subA->consistency == false || subB->consistency == false){
    return false;
  }else{
    return subA->contains(el) && subB->contains(el);
  }
}

//------------

CIntersectionSubProblem::~CIntersectionSubProblem() {

}

void CIntersectionSubProblem::updateDependencyA(CSubProblem *n)
{
  predicate.updateA(n);
  redefined();
}

void CIntersectionSubProblem::updateDependencyB(CSubProblem *n)
{
  predicate.updateB(n);
  redefined();
}

//-------------

bool XorSBPredicate::operator()(const FEMesh *mesh, const Element *el) const {
  // bitwise xor is ok since CSubProblem::contains returns a bool.
  if(subA->consistency == false || subB->consistency == false){
    return false;
  }else{
    return subA->contains(el) ^ subB->contains(el);
  }                                               
}

//------------

CXorSubProblem::~CXorSubProblem() {
 
}

void CXorSubProblem::updateDependencyA(CSubProblem *n)
{
  predicate.updateA(n);
  redefined();
}

void CXorSubProblem::updateDependencyB(CSubProblem *n)
{
  predicate.updateB(n);
  redefined();
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

ComplementSBPredicate::ComplementSBPredicate(CSubProblem *comp)
  : complement(comp)
{}

bool ComplementSBPredicate::operator()(const FEMesh *mesh, const Element *el)
  const
{
  if(complement->consistency == false){
    return false;
  }else{
    return not complement->contains(el);
  }
}

CComplementSubProblem::~CComplementSubProblem() {

}

void CComplementSubProblem::updateDependency(CSubProblem *n)
{
  //update(ComplementSBPredicate(n));
  predicate.update(n);
  redefined();
}
