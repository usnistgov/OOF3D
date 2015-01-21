// -*- C++ -*-
// $RCSfile: invariant.C,v $
// $Revision: 1.5.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:27 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/invariant.h"
#include "engine/outputval.h"
#include "engine/symmmatrix.h"

double Magnitude::operator()(const OutputVal &oval) const {
  // Don't need to do the down-cast, all OutputVal's can do magnitude.
  return oval.magnitude();
}

double MatrixTrace::operator()(const OutputVal &oval) const {
  const SymmMatrix3 &s = dynamic_cast<const SymmMatrix3&>(oval);
  return s.trace();
}

double Determinant::operator()(const OutputVal &oval) const {
  const SymmMatrix3 &s = dynamic_cast<const SymmMatrix3&>(oval);
  return s.determinant();
}

double SecondInvariant::operator()(const OutputVal &oval) const {
  const SymmMatrix3 &s = dynamic_cast<const SymmMatrix3&>(oval);
  return s.secondInvariant();
}

double Deviator::operator()(const OutputVal &oval) const {
  const SymmMatrix3 &s = dynamic_cast<const SymmMatrix3&>(oval);
  return s.deviator();
}

double Eigenvalue::operator()(const OutputVal &oval) const {
  const SymmMatrix3 &s = dynamic_cast<const SymmMatrix3&>(oval);
  switch(which_) {
  case MAX_EIGENVALUE:
    return s.maxEigenvalue();
  case MID_EIGENVALUE:
    return s.midEigenvalue();
  case MIN_EIGENVALUE:
    return s.minEigenvalue();
  }
  // NOT REACHED
  return 0.0;
}
