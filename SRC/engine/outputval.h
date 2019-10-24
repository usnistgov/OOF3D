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

#ifndef OUTPUTVAL_H
#define OUTPUTVAL_H

class OutputVal;
class ScalarOutputVal;
class VectorOutputVal;
class OutputValue;

#include "common/coord_i.h"
#include "common/doublevec.h"
#include "common/pythonexportable.h"
#include "engine/fieldindex.h"

#include <iostream>
#include <math.h>

class SymmMatrix3;

// The OutputVal classes defined here are used to ferry values from
// the finite element mesh out to the Python output machinery. The
// classes give the output machinery the ability to decide what
// further processing is possible (eg computing components or
// invariants).

// OutputVal does not have a template parameter for the output type
// (ie, OutputVal<double>, OutputVal<SymmMatrix3> etc) because the
// templated subclasses would still have to be swigged separately, so
// there wouldn't be much effort saved.

class OutputVal : public PythonExportable<OutputVal> {
private:
  OutputVal(const OutputVal&) = delete;
protected:
  static std::string modulename_;
  int refcount;
public:
  OutputVal();
  virtual ~OutputVal();
  virtual const OutputVal &operator=(const OutputVal&) = 0;
  virtual unsigned int dim() const = 0;
  virtual OutputVal *clone() const = 0;
  virtual OutputVal *zero() const = 0;
  virtual const std::string &modulename() const { return modulename_; }
  // IO ops.
  virtual DoubleVec *value_list() const = 0;
  virtual void print(std::ostream&) const = 0;
  // getIndex converts the string representation of a component index
  // into an IndexP object that can be used to extract a component.
  virtual IndexP getIndex(const std::string&) const = 0;
  virtual IteratorP getIterator() const = 0;

  friend class OutputValue;
  friend class ArithmeticOutputValue;
};

class ArithmeticOutputVal : public OutputVal {
public:
  virtual ArithmeticOutputVal *one() const = 0;
  virtual ArithmeticOutputVal &operator+=(const ArithmeticOutputVal&) = 0;
  virtual ArithmeticOutputVal &operator-=(const ArithmeticOutputVal&) = 0;
  virtual ArithmeticOutputVal &operator*=(double) = 0;
  // Component-wise operations.
  virtual void component_pow(int) = 0;
  virtual void component_square() = 0;
  virtual void component_sqrt() = 0;
  virtual void component_abs() = 0;
  virtual double magnitude() const = 0;
  virtual double operator[](const IndexP&) const = 0;
  virtual double &operator[](const IndexP&) = 0;

  // The generic dot product a (dot) b is a.dot(b).  The double
  // dispatch routines A::dotScalar(B), A::dotVector(B), etc, compute
  // B (dot) A.
  virtual ArithmeticOutputVal *dot(const ArithmeticOutputVal&) const = 0;
  virtual ArithmeticOutputVal *dotScalar(const ScalarOutputVal&) const = 0;
  virtual ArithmeticOutputVal *dotVector(const VectorOutputVal&) const = 0;
  virtual ArithmeticOutputVal *dotSymmMatrix3(const SymmMatrix3&) const = 0;
};

class NonArithmeticOutputVal : public OutputVal {
public:
};

std::ostream &operator<<(std::ostream &, const OutputVal&);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Subclasses of ArithmeticOutputVal


class ScalarOutputVal : public ArithmeticOutputVal {
private:
  static std::string classname_;
  double val;
public:
  ScalarOutputVal() : val(0.0) {}
  ScalarOutputVal(double x) : val(x) {}
  ScalarOutputVal(const ScalarOutputVal &a) : val(a.val) {}
  virtual ~ScalarOutputVal() {}
  const ScalarOutputVal &operator=(const ScalarOutputVal&);
  virtual const ScalarOutputVal &operator=(const OutputVal&);
  virtual unsigned int dim() const { return 1; }
  virtual ScalarOutputVal *clone() const { return new ScalarOutputVal(val); }
  virtual ScalarOutputVal *zero() const { return new ScalarOutputVal(0.0); }
  virtual ScalarOutputVal *one() const { return new ScalarOutputVal(1.0); }
  virtual const std::string &classname() const { return classname_; }

  virtual ArithmeticOutputVal &operator+=(const ArithmeticOutputVal &other) {
    const ScalarOutputVal &another =
      dynamic_cast<const ScalarOutputVal&>(other);
    val += another.val;
    return *this;
  }
  virtual ArithmeticOutputVal &operator-=(const ArithmeticOutputVal &other) {
    const ScalarOutputVal &another =
      dynamic_cast<const ScalarOutputVal&>(other);
    val -= another.val;
    return *this;
  }
  virtual ArithmeticOutputVal &operator*=(double a) {
    val *= a;
    return *this;
  }
  ScalarOutputVal &operator+=(double x) {
    val += x;
    return *this;
  }
  virtual void component_pow(int p) {
    val = pow(val, p);
  }
  virtual void component_square() {
    val *= val;
  }
  virtual void component_sqrt() {
    val = sqrt(val);
  }
  virtual void component_abs() {
    val = fabs(val);
  }
  virtual ArithmeticOutputVal *dot(const ArithmeticOutputVal&) const;
  virtual ArithmeticOutputVal *dotScalar(const ScalarOutputVal&) const;
  virtual ArithmeticOutputVal *dotVector(const VectorOutputVal&) const;
  virtual ArithmeticOutputVal *dotSymmMatrix3(const SymmMatrix3&) const;

  virtual DoubleVec *value_list() const;
  virtual double magnitude() const { return fabs(val); }
  double value() const { return val; }
  double &value() { return val; }
  virtual double operator[](const IndexP&) const;
  virtual double &operator[](const IndexP&);
  virtual IndexP getIndex(const std::string&) const;
  virtual IteratorP getIterator() const;
  
  virtual void print(std::ostream&) const;
};

ScalarOutputVal operator+(const ScalarOutputVal&, const ScalarOutputVal&);
ScalarOutputVal operator-(const ScalarOutputVal&, const ScalarOutputVal&);
ScalarOutputVal operator*(const ScalarOutputVal&, double);
ScalarOutputVal operator*(double, const ScalarOutputVal&);
ScalarOutputVal operator/(ScalarOutputVal&, double);

// TODO OPT: There seems to be a lot of code duplication because Coord,
// DoubleVec, and VectorOutputVal are all almost the same thing, but
// not quite. If Coord and VectorOutputVal both contained a DoubleVec
// instead of a double*, maybe the duplication could be
// reduced. (Done, for VectorOutputVal.) For example, we don't really
// need VectorOutputVal::dot(DoubleVec&) and
// VectorOutputVal::dot(Coord&), or operator*(SymmMatrix3&, Coord&)
// and operator*(SymmMatrix&, DoubleVec&);


class VectorOutputVal : public ArithmeticOutputVal {
private:
  DoubleVec data;
  static std::string classname_;
public:
  VectorOutputVal();
  VectorOutputVal(int n);
  VectorOutputVal(const VectorOutputVal&);
  VectorOutputVal(const DoubleVec&);
  VectorOutputVal(const Coord&);
  virtual ~VectorOutputVal() {}
  virtual const VectorOutputVal &operator=(const OutputVal&);
  const VectorOutputVal &operator=(const VectorOutputVal&);
  virtual unsigned int dim() const { return size(); }
  virtual VectorOutputVal *clone() const;
  virtual VectorOutputVal *zero() const;
  virtual VectorOutputVal *one() const;
  virtual const std::string &classname() const { return classname_; }
  unsigned int size() const { return data.size(); }

  virtual ArithmeticOutputVal &operator+=(const ArithmeticOutputVal &other) {
    const VectorOutputVal &another = 
      dynamic_cast<const VectorOutputVal&>(other);
    for(unsigned int i=0; i<data.size(); i++)
      data[i] += another.data[i];
    return *this;
  }
  virtual ArithmeticOutputVal &operator-=(const ArithmeticOutputVal &other) {
    const VectorOutputVal &another = 
      dynamic_cast<const VectorOutputVal&>(other);
    for(unsigned int i=0; i<size(); i++)
      data[i] -= another.data[i];
    return *this;
  }
  virtual ArithmeticOutputVal &operator*=(double a) {
    for(unsigned int i=0; i<size(); i++)
      data[i] *= a;
    return *this;
  }

  virtual void component_pow(int p) {
    for(unsigned int i=0;i<size();i++)
      data[i] = pow(data[i],p);
  }
  virtual void component_square() {
    for(unsigned int i=0;i<size();i++)
      data[i] *= data[i];
  }
  virtual void component_sqrt() {
    for(unsigned int i=0;i<size();i++)
      data[i] = sqrt(data[i]);
  }
  virtual void component_abs() {
    for(unsigned int i=0; i<size(); i++)
      data[i] = fabs(data[i]);
  }

  double dot(const DoubleVec&) const;
  double dot(const Coord&) const;
  virtual ArithmeticOutputVal *dot(const ArithmeticOutputVal&) const;
  virtual ArithmeticOutputVal *dotScalar(const ScalarOutputVal&) const;
  virtual ArithmeticOutputVal *dotVector(const VectorOutputVal&) const;
  virtual ArithmeticOutputVal *dotSymmMatrix3(const SymmMatrix3&) const;

  virtual DoubleVec *value_list() const;
  const DoubleVec &value() const { return data; }
  double operator[](int i) const { return data[i]; }
  double &operator[](int i) { return data[i]; }
  virtual double operator[](const IndexP &p) const;
  virtual double &operator[](const IndexP &p);
  virtual IndexP getIndex(const std::string&) const;
  virtual IteratorP getIterator() const;
  virtual double magnitude() const;
  virtual void print(std::ostream&) const;
};

VectorOutputVal operator+(const VectorOutputVal&, const VectorOutputVal&);
VectorOutputVal operator-(const VectorOutputVal&, const VectorOutputVal&);
VectorOutputVal operator*(const VectorOutputVal&, double);
VectorOutputVal operator*(double, const VectorOutputVal&);
VectorOutputVal operator/(VectorOutputVal&, double);

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Subclasses of NonArithmeticOutputVal

// ListOutputVal is just a list of values without any specific
// structure, so the labels for its components need to be supplied
// externally.

// TODO: Use DoubleVec as in VectorOutputVal.  This uses double*
// because it was copied from OOF2, which uses double* in
// VectorOutputVal too.  OOF2 should switch to DoubleVec.

class ListOutputVal : public NonArithmeticOutputVal {
private:
  DoubleVec data;
  const std::vector<std::string> labels; 
  static std::string classname_;
public:
  ListOutputVal(const std::vector<std::string>*);
  ListOutputVal(const std::vector<std::string>*, const std::vector<double>&);
  ListOutputVal(const ListOutputVal&);
  virtual const std::string &classname() const { return classname_; }  
  virtual const ListOutputVal &operator=(const OutputVal&);
  const ListOutputVal &operator=(const ListOutputVal&);
  virtual unsigned int dim() const { return data.size(); }
  unsigned int size() const { return data.size(); }  
  virtual ListOutputVal *zero() const;
  virtual ListOutputVal *clone() const;
  double &operator[](int i) { return data[i]; }
  double operator[](int i) const { return data[i]; }
  virtual double operator[](const IndexP &p) const;
  virtual double &operator[](const IndexP &p);
  virtual IteratorP getIterator() const;
  virtual IndexP getIndex(const std::string&) const;
  virtual DoubleVec *value_list() const;
  virtual void print(std::ostream&) const;
  const std::string &label(int i) const { return labels[i]; }
  friend class ListOutputValIndex;
};

// ListOutputValIndex has to be a FieldIndex so that it can be used to
// index ListOutputVal, but it doesn't really belong in FieldIndex
// because the in_plane method doesn't make any sense for it (in 2D).
// We're over-using the FieldIndex class.

// TODO: OutputVal should use some other kind of Index, and FieldIndex
// should be derived from that.

class ListOutputValIndex : virtual public FieldIndex {
protected:
  int max_;
  int index_;
  const ListOutputVal *ov_;
public:
  ListOutputValIndex(const ListOutputVal *ov)
    : max_(ov->size()), index_(0), ov_(ov)
  {}
  ListOutputValIndex(const ListOutputVal *ov, int i)
    : max_(ov->size()), index_(i), ov_(ov)
  {}
  ListOutputValIndex(const ListOutputValIndex &o)
    : max_(o.max_), index_(o.index_), ov_(o.ov_)
  {}
  virtual FieldIndex *cloneIndex() const {
    return new ListOutputValIndex(*this);
  }
  virtual int integer() const { return index_; }
  virtual void set(const std::vector<int>*);
  virtual std::vector<int>* components() const;
  virtual void print(std::ostream &os) const;
  virtual const std::string &shortstring() const;
};


class ListOutputValIterator : public ListOutputValIndex,
				   public FieldIterator
{
public:
  ListOutputValIterator(const ListOutputVal *ov)
    : ListOutputValIndex(ov)
  {}
  ListOutputValIterator(const ListOutputValIterator &o)
    : ListOutputValIndex(o)
  {}
  virtual void operator++() { index_++; }
  virtual bool end() const { return index_ == max_; }
  virtual void reset() { index_ = 0; }
  virtual int size() const { return max_; }
  virtual FieldIterator *cloneIterator() const {
    return new ListOutputValIterator(*this);
  }
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// OutputValue is a generic wrapper for the different OutputVal
// classes.  It takes ownership of the OutputVal that it's initialized
// with, handles the reference counting, and deletes the OutputVal
// when the reference count goes to zero.

class OutputValue {
protected:
  OutputVal *val;
  static int count;
public:
  OutputValue();
  OutputValue(OutputVal*);
  OutputValue(const OutputValue&);
  virtual ~OutputValue();

  unsigned int dim() const { return val->dim(); }

  // valueRef and valuePtr do *not* increment the reference count, so
  // it's important to use them only in situations in which the
  // returned reference or pointer cannot possibly outlive the
  // OutputValue.
  const OutputVal &valueRef() const { return *val; }
  const OutputVal *valuePtr() const { return val; } 
  // For situations in which the OutputVal might outlive the
  // OutputValue, use valueClone instead of valueRef or valuePtr.
  // valueClone returns a new copy of the OutputVal.  It's the calling
  // function's responsibility to see that the copy is deleted.
  OutputVal *valueClone() const { return val->clone(); }

  int nrefcount() { return (*val).refcount; } // for debugging
  friend std::ostream &operator<<(std::ostream&, const OutputValue&);
  friend int get_globalOutputValueCount();
};

class NonArithmeticOutputValue : public OutputValue {
  // This class doesn't do anything that's not already in OutputValue,
  // but all the other ArithmeticOutput* classes have a corresponding
  // NonArithmeticOutput* class, so this one should also.
public:
  NonArithmeticOutputValue() {}
  NonArithmeticOutputValue(NonArithmeticOutputVal*);
};

class ArithmeticOutputValue : public OutputValue {
public:
  ArithmeticOutputValue() {}
  ArithmeticOutputValue(ArithmeticOutputVal*);

  const ArithmeticOutputValue &operator+=(const ArithmeticOutputValue &other);
  const ArithmeticOutputValue &operator-=(const ArithmeticOutputValue &other);
  const ArithmeticOutputValue &operator *=(double x);

  // In principle, operator[](IndexP) should be defined in the base
  // classes OutputValue and OutputVal.  However, it's a bit of a pain
  // to define them for NonArithmeticOutputVals that are indexed by
  // strings, and they're not needed in C++.  They're defined in
  // Python.
  double operator[](const IndexP &p) const;
  double &operator[](const IndexP &p);
};

ArithmeticOutputValue operator*(double x, const ArithmeticOutputValue &ov);
ArithmeticOutputValue operator*(const ArithmeticOutputValue &ov, double x);
ArithmeticOutputValue operator/(const ArithmeticOutputValue &ov, double x);
ArithmeticOutputValue operator+(const ArithmeticOutputValue &a,
				const ArithmeticOutputValue &b);
ArithmeticOutputValue operator-(const ArithmeticOutputValue &a,
				const ArithmeticOutputValue &b);

std::ostream &operator<<(std::ostream&, const OutputValue&);

int get_globalOutputValueCount();
int get_globalOutputValCount();
void init_globalOutputValCount();


// TODO OPT: Energies should not be calculated by using the properties
// (each property contributing its part).  Instead, the Fluxes should
// be used.  e += Flux*Grad Field.  Need a better abstract way of
// defining Energies.

#endif // OUTPUTVAL_H
