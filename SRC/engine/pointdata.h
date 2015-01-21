// -*- C++ -*-
// $RCSfile: pointdata.h,v $
// $Revision: 1.4.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:40 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef POINTDATA_H
#define POINTDATA_H

// A class to which degrees of freedom and equation components can be
// attached. This class is one of the parents of both FuncNodes and
// FunctionalGaussPoints.

#include "common/coord.h"
#include "engine/equation.h"
#include "engine/field.h"
#include "engine/fieldeqnlist.h"
#include <vector>
#include <iostream>

class PointData {
public: 
  
  PointData(FEMesh*);
  virtual ~PointData() {}

  std::vector<DegreeOfFreedom*> doflist;
  std::vector<NodalEquation*> eqnlist;

  virtual Coord position() const = 0;
  
  int ndof() const { return doflist.size(); }
  int neqn() const { return eqnlist.size(); }
  
  void addField(FEMesh*, const Field&);
  void removeField(FEMesh*, const Field&);
  
  bool hasField(const Field&) const;
  // Returns the number of subproblems containing this point for which
  // the passed-in field is defined.
  int fieldDefCount(const Field&) const;
  
  void addEquation(FEMesh*, const Equation&);
  void removeEquation(FEMesh*, const Equation&);
  bool hasEquation(const Equation&) const;

  typedef FieldEqnList<Field> FieldSet;
  typedef FieldEqnList<Equation> EquationSet;
  FieldSet fieldset;
  EquationSet equationset;

  int fieldSetID() const { return fieldset.id(); }

};

  
#endif
