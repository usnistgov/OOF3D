// -*- C++ -*-
// $RCSfile: nodalequation.C,v $
// $Revision: 1.10.6.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:34 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include "nodalequation.h"

#include <iostream>

NodalEquation::NodalEquation(int n) 
  : index_(n)
{
}

std::ostream &operator<<(std::ostream &os, const NodalEquation &neqn) {
//   os << "[" << neqn.ndq_index();
//   if(neqn.is_dependent())
//     os << " dependent";
//   else
//     os << " independent";
//   os << "]";
  return os << "[" << neqn.ndq_index() << "]";
}
