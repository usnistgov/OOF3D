/// -*- C++ -*-

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


// The "SmallMatrix" class is a general (i.e. not symmetric or
// positive-definite or anything) real-valued matrix which stores its
// data internally in column-ordered LAPACK-friendly format.  For
// maximum speed, routines which require "utility" linear-algebra
// operations should construct one of these directly.


#ifndef SMALLMATRIX3_H
#define SMALLMATRIX3_H

#include "common/doublevec.h"
#include "common/smallmatrix.h"


class SmallMatrix3 : public SmallMatrix {
public:
  SmallMatrix3();
  SmallMatrix3(const SmallMatrix3&);
  SmallMatrix3(const SmallMatrix&);
  SmallMatrix3 invert() const;
  double det() const;
  // Polar decomposition.
  std::pair<SmallMatrix3,SmallMatrix3> sqrt() const;
  // Over-ride resizing to disallow it.
  virtual void resize(unsigned int,unsigned int);
  // TODO: Logarithm, for true strain.  Also trace.
  
};


#endif	// SMALLMATRIX3_H
