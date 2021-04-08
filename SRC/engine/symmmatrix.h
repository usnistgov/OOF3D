// -*- C++ -*-
// $RCSfile: symmmatrix.h,v $
// $Revision: 1.32.4.7 $
// $Author: langer $
// $Date: 2014/12/14 22:49:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>


// Symmetric matrix storage class
// may not be best for linear algebra!

class SymmMatrix;

#ifndef SYMMMATRIX_H
#define SYMMMATRIX_H

#include <iostream>
#include <math.h>
#include "common/coord_i.h"
#include "common/smallmatrix.h"
#include "engine/eigenvalues.h"
#include "engine/fieldindex.h"
#include "engine/outputval.h"

class COrientation;
class IndexP;

class SymmMatrix {
protected:
//   friend double SymmMatrix_get(SymmMatrix*, int, int);
  double **m;
  unsigned int nrows;
  void allocate();
  void free();
  virtual void copy(double**);
public:
  SymmMatrix() : m(0), nrows(0) {}
  SymmMatrix(int);		// specifies size
  SymmMatrix(const SymmMatrix&); // copy constructor
  virtual ~SymmMatrix();
  SymmMatrix &operator=(const SymmMatrix&);
  SymmMatrix &operator*=(double);
  SymmMatrix &operator/=(double);
  bool operator==(const SymmMatrix&);
  double &operator()(int i, int j);
  double operator()(int i, int j) const;
  SymmMatrix &operator+=(const SymmMatrix&);
  SymmMatrix &operator-=(const SymmMatrix&);
  void resize(unsigned int);
  unsigned int size() const { return nrows; }
  void clear(double x=0);
  int badindex(int i) const { return i < 0 || i >= int(nrows); }
	
  SymmMatrix transform(const COrientation*) const; // A^T B A
	
  friend class Debug;
  friend class SymmMatrix3;
  friend std::ostream& operator<<(std::ostream&, const SymmMatrix&);
  friend SmallMatrix operator*(const SymmMatrix&, const SymmMatrix&);
  friend SymmMatrix operator*(double, const SymmMatrix&);
  friend SymmMatrix operator*(const SymmMatrix&, double);
  friend DoubleVec operator*(const SymmMatrix&, const DoubleVec&);
};

#endif
