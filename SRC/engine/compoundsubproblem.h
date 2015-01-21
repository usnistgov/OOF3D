// -*- C++ -*-
// $RCSfile: compoundsubproblem.h,v $
// $Revision: 1.8.2.3 $
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

#ifndef COMPOUNDSUBPROBLEM_H
#define COMPOUNDSUBPROBLEM_H

#include "engine/predicatesubproblem.h"
#include <iostream>

class BinarySubproblemPredicate {
public:
  BinarySubproblemPredicate(CSubProblem*, CSubProblem*);
  virtual ~BinarySubproblemPredicate();
  virtual bool operator()(const FEMesh*, const Element*) const = 0;
  CSubProblem *subA;
  CSubProblem *subB;
  void updateA(CSubProblem *a_){subA = a_;}
  void updateB(CSubProblem *b_){subB = b_;}
};

class UnionSBPredicate: public BinarySubproblemPredicate {
public:
  UnionSBPredicate(CSubProblem *a, CSubProblem *b)
    : BinarySubproblemPredicate(a, b)
  {}
  virtual ~UnionSBPredicate() {}
  virtual bool operator()(const FEMesh*, const Element*) const;
};

class CUnionSubProblem: public PredicateSubProblem<UnionSBPredicate> {
protected:
  CSubProblem *subpA, *subpB;
public:
  bool consistency;
  CUnionSubProblem(CSubProblem *a, CSubProblem *b)
    : PredicateSubProblem<UnionSBPredicate>(UnionSBPredicate(a, b)),
      subpA(a),
      subpB(b)
  {}
  virtual ~CUnionSubProblem();
  virtual MaterialSet *getMaterials() const;
  void updateDependencyA(CSubProblem*);
  void updateDependencyB(CSubProblem*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class IntersectionSBPredicate: public BinarySubproblemPredicate {
public:
  IntersectionSBPredicate(CSubProblem *a, CSubProblem *b)
    : BinarySubproblemPredicate(a, b)
  {}
  virtual ~IntersectionSBPredicate() {}
  virtual bool operator()(const FEMesh*, const Element*) const;
};

class CIntersectionSubProblem:
  public PredicateSubProblem<IntersectionSBPredicate>
{
protected:
  CSubProblem *subpA, *subpB;
public:
  bool consistency;
  CIntersectionSubProblem(CSubProblem *a, CSubProblem *b)
    : PredicateSubProblem<IntersectionSBPredicate>(IntersectionSBPredicate(a,b)),
      subpA(a),
      subpB(b)
  {}
  virtual ~CIntersectionSubProblem();
  void updateDependencyA(CSubProblem*);
  void updateDependencyB(CSubProblem*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class XorSBPredicate: public BinarySubproblemPredicate {
public:
  XorSBPredicate(CSubProblem *a, CSubProblem *b)
    : BinarySubproblemPredicate(a, b)
  {}
  virtual ~XorSBPredicate() {}
  virtual bool operator()(const FEMesh*, const Element*) const;
};

class CXorSubProblem:
  public PredicateSubProblem<XorSBPredicate>
{
protected:
  CSubProblem *subpA, *subpB;
public:
  bool consistency;
  CXorSubProblem(CSubProblem *a, CSubProblem *b)
    : PredicateSubProblem<XorSBPredicate>(XorSBPredicate(a,b)),
      subpA(a),
      subpB(b)
  {}
  virtual ~CXorSubProblem();
  void updateDependencyA(CSubProblem*);
  void updateDependencyB(CSubProblem*);
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

class ComplementSBPredicate {
protected:
  CSubProblem *complement;
public:
  ComplementSBPredicate(CSubProblem*);
  virtual ~ComplementSBPredicate() {}
  bool operator()(const FEMesh*, const Element*) const;
  void update(CSubProblem *comp){complement = comp;}
};

class CComplementSubProblem: public PredicateSubProblem<ComplementSBPredicate> {
public:
  bool consistency;
  CComplementSubProblem(CSubProblem *comp)
    : PredicateSubProblem<ComplementSBPredicate>(ComplementSBPredicate(comp))
  {}
  virtual ~CComplementSubProblem();
  void updateDependency(CSubProblem*);
  //void redefine(CSubProblem *comp){predicate.update(comp);}
};

#endif // COMPOUNDSUBPROBLEM_H
