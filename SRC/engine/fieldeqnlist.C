// -*- C++ -*-
// $RCSfile: fieldeqnlist.C,v $
// $Revision: 1.6.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:23 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/equation.h"
#include "engine/field.h"
#include "engine/fieldeqnlist.h"

// The comparison operator for FieldEqnData objects is used to
// discover if two lists of FieldEqnData objects are the same, so that
// they can be reused.

bool operator<(const FieldEqnData &a, const FieldEqnData &b) {
  if(a.order == b.order)
    return a.listed < b.listed;
  return a.order < b.order;
}

std::ostream &operator<<(std::ostream &os, const FieldEqnData &fe) {
  os << "FieldEqnData(order=" << fe.order << ", offset=" << fe.offset
     << ", listed=" << fe.listed << ")";
  return os;
}

template <> int FEWrapper<Field>::counter = 0;
template <> int FEWrapper<Equation>::counter = 0;


