// -*- C++ -*-
// $RCSfile: rank3tensor.h,v $
// $Revision: 1.10.10.3 $
// $Author: fyc $
// $Date: 2014/07/28 22:15:27 $


/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

class Rank3Tensor;

#ifndef RANK3TENSOR_H
#define RANK3TENSOR_H

#include <iostream>
#include "engine/eigenvalues.h"
#include "engine/fieldindex.h"
#include "engine/outputval.h"
#include "common/pythonexportable.h"
#include "engine/symmmatrix.h"


class Cijkl; //actually, a rank 4 tensor
class DoubleVec;
class COrientation;

class Rank3Tensor : public PythonExportable<Rank3Tensor> {
private:
  // a rank 3 tensor can be thought of
  // as a group of three symmetric matrices
  // with a special set of operations

  // TODO 3.1: De-stupidize this.  nrows is the number of SymmMatrices, so
  // either stop pretending that nrows is a variable, or use a vector
  // of SymmMatrices and allow nrows to vary.

  SymmMatrix  m0;
  SymmMatrix  m1;
  SymmMatrix  m2;
  static std::string classname_;
  static std::string modulename_;


public:
  Rank3Tensor() :  m0(3), m1(3), m2(3), nrows(3) {} 
  Rank3Tensor(const Rank3Tensor&); 
  virtual ~Rank3Tensor();
  const unsigned int nrows;
  Rank3Tensor &operator=(const Rank3Tensor&);
  Rank3Tensor &operator*=(double);
  Rank3Tensor &operator/=(double);
  double &operator()(unsigned int i, unsigned int j, unsigned int k); 
  double operator()(unsigned int i, unsigned int j, unsigned int k) const;
  Rank3Tensor &operator+=(const Rank3Tensor&);
  Rank3Tensor &operator-=(const Rank3Tensor&);
  bool operator==(const Rank3Tensor&);
  bool badindex(unsigned int i) const { return i >= nrows; } 
	
  Rank3Tensor transform(const COrientation*) const; // A^T B A 
	
  friend class Debug;
  friend std::ostream& operator<<(std::ostream&, const Rank3Tensor&); 
  friend Rank3Tensor operator*(double, const Rank3Tensor&); 
  friend Rank3Tensor operator*(const Rank3Tensor&, double); 
  friend SymmMatrix operator*(const Rank3Tensor&, const DoubleVec&);
  virtual const std::string &classname() const { return classname_; }  
  virtual const std::string &modulename() const { return modulename_; } 
  friend Rank3Tensor operator/(const Rank3Tensor &A, double x); 
  double &operator()(int, const SymTensorIndex&);
  double operator()(int, const SymTensorIndex&) const;
  unsigned int size() {return nrows;}

  SymmMatrix &operator()(unsigned int i);
  SymmMatrix operator()(unsigned int i) const;
  SymmMatrix operator*(const DoubleVec&);  
  const Rank3Tensor operator +(const Rank3Tensor & A); 
};

Rank3Tensor operator*(const Cijkl&, const Rank3Tensor&); 

// for electrostriction 
Rank3Tensor operator*(const Cijkl&, const DoubleVec&);

#endif
