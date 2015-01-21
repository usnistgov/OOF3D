// -*- C++ -*-
// $RCSfile: nodalequation.h,v $
// $Revision: 1.15.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:35 $

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

// NodalEquations represent one component of an equation at a node.
// Each NodalEquation corresponds to a row of the master stiffness
// matrix.  Unlike DOFs, nodal equations do not have values.  They
// contain index data only.


class NodalEquation {
private:
  NodalEquation(int n);
  ~NodalEquation() {}
  friend class FEMesh;	// only an FEMesh can create or destroy a NodalEquation

  int index_;
public:
  int ndq_index() const { return index_; }
};

struct NodalEqnCompare {
  bool operator()(const NodalEquation *a, const NodalEquation *b) const {
    return a->ndq_index() < b->ndq_index();
  }
};

std::ostream &operator<<(std::ostream &os, const NodalEquation &neqn);
