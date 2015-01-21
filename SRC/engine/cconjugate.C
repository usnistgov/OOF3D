// -*- C++ -*-
// $RCSfile: cconjugate.C,v $
// $Revision: 1.3.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/cconjugate.h"
#include "engine/equation.h"
#include "engine/field.h"
#include "engine/fieldindex.h"

CConjugatePair::CConjugatePair(const Equation *eqn, const FieldIndex *eqncomp,
			       const Field *field, const FieldIndex *fieldcomp)
    : field_(field),
      fieldcomp_(fieldcomp),
      eqn_(eqn),
      eqncomp_(eqncomp)
{
}


bool operator==(const CConjugatePair &a, const CConjugatePair &b) {
  return (a.get_field() == b.get_field() &&
	  *a.get_field_component() == *b.get_field_component() &&
	  a.get_equation() == b.get_equation() &&
	  *a.get_equation_component() == *b.get_equation_component());
}
