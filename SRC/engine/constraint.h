// -*- C++ -*-
// $RCSfile: constraint.h,v $
// $Revision: 1.5.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CONSTRAINT_H
#define CONSTRAINT_H

#include <oofconfig.h>

class Constraint {
 public:
  virtual ~Constraint() {}
  virtual void apply() const = 0;
  virtual string &name() const;
};

class ConstraintEqn : public Constraint, public Equation {
 private:
  Equation
};

#endif // CONSTRAINT_H
