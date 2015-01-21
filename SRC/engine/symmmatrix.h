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

class SymmMatrix3 : public OutputVal, public SymmMatrix {
// OutputVal is a PythonExportable class, and must be the first base
// class listed so that the PythonExportable dynamic classes work.
// This doesn't feel right...
private:
  mutable EigenValues eigenvalues; // cached
  mutable bool dirtyeigs_;	// are eigenvalues up-to-date?
  void findEigenvalues() const;
  static std::string classname_; // OutputVal is PythonExportable
  static std::string modulename_;
public:
  SymmMatrix3() : SymmMatrix(3), dirtyeigs_(true) {}
//   virtual ~SymmMatrix3();
  SymmMatrix3(double, double, double, double, double, double); // voigt order
  SymmMatrix3(const SymmMatrix3&);
  SymmMatrix3(const SymmMatrix&);
  virtual unsigned int dim() const { return 6; }
  virtual OutputVal *clone() const;
  virtual OutputVal *zero() const;
  virtual OutputVal *one() const;
  virtual const std::string &classname() const { return classname_; }
  virtual const std::string &modulename() const { return modulename_; }
  SymmMatrix3 &operator=(const SymmMatrix3 &x) {
    dirtyeigs_ = x.dirtyeigs_;
    eigenvalues = x.eigenvalues;
    return dynamic_cast<SymmMatrix3&>(SymmMatrix::operator=(x));
  }

  virtual void component_pow(int p) {
    dirtyeigs_ = true;
    double *data = m[0];
    for(int i=0;i<6;i++)  // SymmMatrix3 guaranteed to have 6 entries.
      data[i] = pow(data[i], p);
  }
  virtual void component_square() {
    dirtyeigs_ = true;
    double *data = m[0];
    for(int i=0;i<6;i++) 
      data[i] *= data[i];
  }
  virtual void component_sqrt() {
    dirtyeigs_ = true;
    double *data = m[0];
    for(int i=0;i<6;i++)
      data[i] = sqrt(data[i]);
  }
  virtual void component_abs() {
    dirtyeigs_ = true;
    double *data = m[0];
    for(int i=0;i<6;i++)
      data[i] = fabs(data[i]);
  }
  virtual DoubleVec *value_list() const;

  OutputVal &operator*=(double x) {
    dirtyeigs_ = true;
    return dynamic_cast<OutputVal&>(SymmMatrix::operator*=(x));
  }
  OutputVal &operator+=(const OutputVal &x) {
    dirtyeigs_ = true;
    const SymmMatrix3 &sm = dynamic_cast<const SymmMatrix3&>(x);
    return dynamic_cast<OutputVal&>(SymmMatrix::operator+=(sm));
  }
  OutputVal &operator-=(const OutputVal &x) {
    dirtyeigs_ = true;
    const SymmMatrix3 &sm = dynamic_cast<const SymmMatrix3&>(x);
    return dynamic_cast<OutputVal&>(SymmMatrix::operator-=(sm));
  }
  SymmMatrix3 &operator/=(double x) {
    dirtyeigs_ = true;
    return dynamic_cast<SymmMatrix3&>(SymmMatrix::operator/=(x));
  }
  SymmMatrix3 &operator+=(const SymmMatrix3 &x) {
    dirtyeigs_ = true;
    return dynamic_cast<SymmMatrix3&>(SymmMatrix::operator+=(x));
  }
  SymmMatrix3 &operator-=(const SymmMatrix3 &x) {
    dirtyeigs_ = true;
    return dynamic_cast<SymmMatrix3&>(SymmMatrix::operator-=(x));
  }
  virtual OutputVal *dot(const OutputVal&) const;
  virtual OutputVal *dotScalar(const ScalarOutputVal&) const;
  virtual OutputVal *dotVector(const VectorOutputVal&) const;
  virtual OutputVal *dotSymmMatrix3(const SymmMatrix3&) const;

  virtual double operator[](const IndexP&) const;
  virtual double &operator[](const IndexP&);
  double operator[](const SymTensorIndex&) const;
  double &operator[](const SymTensorIndex&);
  double trace() const;
  double determinant() const;
  double secondInvariant() const;
  double deviator() const;
  virtual double magnitude() const;
  double maxEigenvalue() const;
  double midEigenvalue() const;
  double minEigenvalue() const;
  double contract(const SymmMatrix3&) const;

  virtual IndexP getIndex(const std::string&) const;
  virtual IteratorP getIterator() const;
  virtual void print(std::ostream&) const;
};

SymmMatrix3 operator+(const SymmMatrix3&, const SymmMatrix3&);
SymmMatrix3 operator-(const SymmMatrix3&, const SymmMatrix3&);
SymmMatrix3 operator*(const SymmMatrix3&, double);
SymmMatrix3 operator*(double, const SymmMatrix3&);
SymmMatrix3 operator/(SymmMatrix3&, double);

#if DIM==3
Coord operator*(const SymmMatrix3&, const Coord&);
Coord operator*(const Coord&, const SymmMatrix3&);
#endif // DIM==3

OutputValue *newSymTensorOutputValue();

std::ostream& operator<<(std::ostream&, const SymmMatrix&);
// SymmMatrix3 needs operator<< to disambiguate the base class
// operators.
std::ostream& operator<<(std::ostream&, const SymmMatrix3&);



#endif
