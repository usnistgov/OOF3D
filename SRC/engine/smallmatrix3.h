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
#include "common/pythonexportable.h"
#include "engine/fieldindex.h"
#include "engine/outputval.h"


class SmallMatrix3 : public OutputVal, public SmallMatrix {
private:
  static std::string classname_;  // Induced by PythonExportable.
  static std::string modulename_;
public:
  SmallMatrix3();
  SmallMatrix3(const SmallMatrix3&);
  SmallMatrix3(const SmallMatrix&);
  SmallMatrix3 invert() const;
  double det() const;
  // Polar decomposition.
  std::pair<SmallMatrix3,SmallMatrix3> ch_sqrt() const;
  // Over-ride resizing to disallow it.
  virtual void resize(unsigned int,unsigned int);
  // TODO: Logarithm, for true strain.  Also trace.

  // OutputVal functionality.
  virtual unsigned int dim() const { return 9; }
  virtual OutputVal *clone() const;
  virtual OutputVal *zero() const;
  virtual OutputVal *one() const;

  virtual double operator[](const IndexP&) const;
  virtual double &operator[](const IndexP&);
  
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }

  virtual OutputVal &operator+=(const OutputVal&);
  virtual OutputVal &operator-=(const OutputVal&);
  virtual OutputVal &operator*=(double);

  SmallMatrix3 &operator+=(const SmallMatrix3&);
  SmallMatrix3 &operator-=(const SmallMatrix3&);
  
  virtual void component_pow(int);
  virtual void component_square();
  virtual void component_sqrt();
  virtual void component_abs();

  virtual DoubleVec *value_list() const;
  virtual double magnitude() const;

  // TODO: Add dotSmallMatrix3 to this set.
  virtual OutputVal *dot(const OutputVal &) const;
  virtual OutputVal *dotScalar(const ScalarOutputVal &) const;
  virtual OutputVal *dotVector(const VectorOutputVal &) const;
  virtual OutputVal *dotSymmMatrix3(const SymmMatrix3&) const;
  virtual OutputVal *dotSmallMatrix3(const SmallMatrix3&) const;

  virtual IteratorP getIterator() const; 
  virtual void print(std::ostream &) const;
  virtual IndexP getIndex(const std::string&) const;
};

// Required for disambiguation of base-class operations.
std::ostream &operator<<(std::ostream&, const SmallMatrix3&);


OutputValue *newSmallMatrix3OutputValue();

#endif	// SMALLMATRIX3_H
