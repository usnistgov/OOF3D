// -*- C++ -*-
// $RCSfile: materialsubproblem.h,v $
// $Revision: 1.8.2.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:31 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef MATERIALSUBPROBLEM_H
#define MATERIALSUBPROBLEM_H

#include "engine/predicatesubproblem.h"

class Material;

class MaterialPredicate {
private:
  Material *const material;
public:
  MaterialPredicate(Material * const);
  bool operator()(const FEMesh*, const Element *element) const;
  friend class CMaterialSubProblem;
};

class CMaterialSubProblem: public PredicateSubProblem<MaterialPredicate> {
public:
  CMaterialSubProblem(Material * const mat)
    : PredicateSubProblem<MaterialPredicate>(MaterialPredicate(mat))
  {}
  virtual MaterialSet *getMaterials() const;
};

#endif // MATERIALSUBPROBLEM_H
