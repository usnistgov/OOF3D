// -*- C++ -*-
// $RCSfile: cconjugate.h,v $
// $Revision: 1.3.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef CCONJUGATE_H
#define CCONJUGATE_H

class Equation;
class Field;
class FieldIndex;

#include <vector>

class CConjugatePair {
private:
  const Field *field_;
  const FieldIndex *fieldcomp_;
  const Equation *eqn_;
  const FieldIndex *eqncomp_;
public:
  CConjugatePair(const Equation *eqn, const FieldIndex *eqncomp,
		 const Field *field, const FieldIndex *fieldcomp);
  const Field *get_field() const { return field_; }
  const FieldIndex *get_field_component() const { return fieldcomp_; }
  const Equation *get_equation() const { return eqn_; }
  const FieldIndex *get_equation_component() const { return eqncomp_; }
};

bool operator==(const CConjugatePair&, const CConjugatePair &b);

#endif // CCONJUGATE_H
