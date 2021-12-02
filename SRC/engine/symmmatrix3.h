// -*- C++ -*-

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

#ifndef SYMMMATRIX3_H
#define SYMMMATRIX3_H

class SymmMatrix3;

#include <iostream>
#include <math.h>
#include "common/coord_i.h"

#include "engine/eigenvalues.h"
#include "engine/fieldindex.h"
#include "engine/outputval.h"
#include "engine/symmmatrix.h"
#include "engine/smallmatrix3.h"

#include "engine/matrix3.h"

class COrientation;
class IndexP;

class SymmMatrix3 : public Matrix3, public SymmMatrix {
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
  void operator=(const SmallMatrix3 &x) {
    // std::cerr << "Assigning sym from small." << std::endl;
    operator()(0,0) = x(0,0);
    operator()(1,1) = x(1,1);
    operator()(2,2) = x(2,2);
    operator()(0,1) = 0.5*(x(0,1)+x(1,0));
    operator()(0,2) = 0.5*(x(0,2)+x(2,0));
    operator()(1,2) = 0.5*(x(1,2)+x(2,1));
  }
  virtual OutputVal *dot(const OutputVal&) const;
  virtual OutputVal *dotScalar(const ScalarOutputVal&) const;
  virtual OutputVal *dotVector(const VectorOutputVal&) const;
  virtual OutputVal *dotSymmMatrix3(const SymmMatrix3&) const;
  virtual OutputVal *dotSmallMatrix3(const SmallMatrix3&) const;
  
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
