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

#include "common/IO/oofcerr.h"
#include "common/coord.h"
#include "common/doublevec.h"
#include "common/lock.h"
#include "engine/fieldindex.h"
#include "engine/ooferror.h"
#include "engine/outputval.h"
#include "engine/symmmatrix.h"
#include <map>
#include <math.h>
#include <string.h>		// for memcpy

std::string OutputVal::modulename_("ooflib.SWIG.engine.outputval");
std::string ScalarOutputVal::classname_("ScalarOutputVal");
std::string VectorOutputVal::classname_("VectorOutputVal");

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Machinery for checking for OutputVal and OutputValue memory leaks.
// This is a bit problematic.  OutputValues are not leaked and aren't
// a problem.  OutputVals are sometimes stored in Parameters for
// commands and Outputs, and will persist until the Parameters are
// reset, so counting them automatically in the test scripts is hard.
// Testing did show that the swigged clone and zero OutputVal methods
// were causing leaks, which is why the NewOutputVal typemap is used
// in outputval.swg.

// In DEBUG mode, OutputValue::count isn't incremented, but
// get_globalOutputValueCount() is still defined, and returns 0, so
// that the tests will work.
int OutputValue::count = 0;
int get_globalOutputValueCount() { return OutputValue::count; }

#ifdef DEBUG
#include <set>
std::set<OutputVal*> allOutputVals;
static int offset_ = 0;
SLock outputValueLock;
#endif // DEBUG

int get_globalOutputValCount() {
#ifdef DEBUG
  return allOutputVals.size() - offset_;
#else
  return 0;
#endif // DEBUG
}

void init_globalOutputValCount() {
#ifdef DEBUG
  // oofcerr << "init_globalOutputValCount" << std::endl;
  outputValueLock.acquire();
  offset_ = allOutputVals.size();
  outputValueLock.release();
#endif // DEBUG
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

OutputValue::OutputValue()
  : val(nullptr)
{
#ifdef DEBUG
  outputValueLock.acquire();
  ++count;
  outputValueLock.release();
#endif // DEBUG
}

OutputValue::OutputValue(OutputVal *v)
  : val(v)
{
  ++val->refcount;
#ifdef DEBUG
  outputValueLock.acquire();
  ++count;
  outputValueLock.release();
#endif // DEBUG
}

OutputValue::OutputValue(const OutputValue &other)
  : val(other.val)
{
  ++val->refcount;
#ifdef DEBUG
  outputValueLock.acquire();
  ++count;
  outputValueLock.release();
#endif // DEBUG
}

OutputValue::~OutputValue() {
  if(--val->refcount == 0) {
    delete val;
  }
#ifdef DEBUG
  outputValueLock.acquire();
  --count;
  outputValueLock.release();
#endif // DEBUG
}

ArithmeticOutputValue::ArithmeticOutputValue(ArithmeticOutputVal *v)
  : OutputValue(v)
{}

NonArithmeticOutputValue::NonArithmeticOutputValue(NonArithmeticOutputVal *v)
  : OutputValue(v)
{}

const ArithmeticOutputValue &ArithmeticOutputValue::operator+=(
				       const ArithmeticOutputValue &other)
{
  ArithmeticOutputVal *thisval = dynamic_cast<ArithmeticOutputVal*>(val);
  const ArithmeticOutputVal *thatval =
    dynamic_cast<const ArithmeticOutputVal*>(other.val);
  *thisval += *thatval;
  return *this;
}

// Arithmetic operations on instances of ArithmeticOutputValue, the
// wrapper class.

const ArithmeticOutputValue &ArithmeticOutputValue::operator-=(
				       const ArithmeticOutputValue &other)
{
  ArithmeticOutputVal *thisval = dynamic_cast<ArithmeticOutputVal*>(val);
  const ArithmeticOutputVal *thatval =
    dynamic_cast<const ArithmeticOutputVal*>(other.val);
  *thisval -= *thatval;
  return *this;
}

const ArithmeticOutputValue &ArithmeticOutputValue::operator*=(double x) {
  ArithmeticOutputVal *thisval = dynamic_cast<ArithmeticOutputVal*>(val);
  *thisval *= x;
  return *this;
}

double ArithmeticOutputValue::operator[](const IndexP &p) const {
  const ArithmeticOutputVal *thisval =
    dynamic_cast<const ArithmeticOutputVal*>(val);
  return (*thisval)[p];
}

double &ArithmeticOutputValue::operator[](const IndexP &p) {
  ArithmeticOutputVal *thisval = dynamic_cast<ArithmeticOutputVal*>(val);
  return (*thisval)[p];
}

ArithmeticOutputValue operator*(double x, const ArithmeticOutputValue &ov) {
  ArithmeticOutputValue result(ov);
  result *= x;
  return result;
}

ArithmeticOutputValue operator*(const ArithmeticOutputValue &ov, double x) {
  ArithmeticOutputValue result(ov);
  result *= x;
  return result;
}

ArithmeticOutputValue operator/(const ArithmeticOutputValue &ov, double x) {
  ArithmeticOutputValue result(ov);
  result *= 1./x;
  return result;
}

ArithmeticOutputValue operator+(const ArithmeticOutputValue &a,
				const ArithmeticOutputValue &b)
{
  ArithmeticOutputValue result(a);
  result += b;
  return result;
}

ArithmeticOutputValue operator-(const ArithmeticOutputValue &a,
				const ArithmeticOutputValue &b)
{
  ArithmeticOutputValue result(a);
  result -= b;
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// These are here just so that debugging lines can be added if needed.

OutputVal::OutputVal() : refcount(0) {
#ifdef DEBUG
  outputValueLock.acquire();
  allOutputVals.insert(this);
  outputValueLock.release();
#endif // DEBUG
}

OutputVal::~OutputVal() {
#ifdef DEBUG
  outputValueLock.acquire();
  allOutputVals.erase(this);
  outputValueLock.release();
#endif // DEBUG
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const ScalarOutputVal &ScalarOutputVal::operator=(const OutputVal &other) {
  *this = dynamic_cast<const ScalarOutputVal&>(other);
  return *this;
}

const ScalarOutputVal &ScalarOutputVal::operator=(const ScalarOutputVal &other)
{
  val = other.val;
  return *this;
}

double ScalarOutputVal::operator[](const IndexP&) const {
  return val;
}

double &ScalarOutputVal::operator[](const IndexP&) {
  return val;
}

DoubleVec *ScalarOutputVal::value_list() const {
  return new DoubleVec(1, val);
}


IndexP ScalarOutputVal::getIndex(const std::string&) const {
  return IndexP(new ScalarFieldIndex());
}

IteratorP ScalarOutputVal::getIterator() const {
  return IteratorP(new ScalarFieldIterator());
}

ScalarOutputVal operator+(const ScalarOutputVal &a, const ScalarOutputVal &b) {
  ScalarOutputVal result(a);
  result += b;
  return result;
}

ScalarOutputVal operator-(const ScalarOutputVal &a, const ScalarOutputVal &b) {
  ScalarOutputVal result(a);
  result -= b;
  return result;
}

ScalarOutputVal operator*(const ScalarOutputVal &a, double b) {
  ScalarOutputVal result(a);
  result *= b;
  return result;
}

ScalarOutputVal operator*(double b, const ScalarOutputVal &a) {
  ScalarOutputVal result(a);
  result *= b;
  return result;
}

ScalarOutputVal operator/(const ScalarOutputVal &a, double b) {
  ScalarOutputVal result(a);
  result *= (1./b);
  return result;
}

ArithmeticOutputVal *ScalarOutputVal::dot(const ArithmeticOutputVal &ov) const
{
  return ov.dotScalar(*this);
}

ArithmeticOutputVal *ScalarOutputVal::dotScalar(const ScalarOutputVal &ov) const
{
  return new ScalarOutputVal(ov.value()*val);
}

ArithmeticOutputVal *ScalarOutputVal::dotVector(const VectorOutputVal &ov) const
{
  VectorOutputVal *result = new VectorOutputVal(ov);
  *result *= val;
  return result;
}

ArithmeticOutputVal *ScalarOutputVal::dotSymmMatrix3(const SymmMatrix3 &ov)
  const
{
  return ov.dotScalar(*this);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VectorOutputVal::VectorOutputVal()
{}

VectorOutputVal::VectorOutputVal(int n)
  : data(n, 0.0)
{}

VectorOutputVal::VectorOutputVal(const VectorOutputVal &other)
  : data(other.data)
{}

VectorOutputVal::VectorOutputVal(const DoubleVec &vec)
  : data(vec)
{}

VectorOutputVal::VectorOutputVal(const Coord &coord)
  : data(DIM)
{
  data[0] = coord[0];
  data[1] = coord[1];
  data[2] = coord[2];
}

const VectorOutputVal &VectorOutputVal::operator=(const OutputVal &other) {
  *this = dynamic_cast<const VectorOutputVal&>(other);
  return *this;
}

const VectorOutputVal &VectorOutputVal::operator=(const VectorOutputVal &other)
{
  data = other.data;
  return *this;
}

DoubleVec *VectorOutputVal::value_list() const {
  DoubleVec *res = new DoubleVec(data);
  return res;
}

VectorOutputVal *VectorOutputVal::clone() const {
  return new VectorOutputVal(*this);
}

VectorOutputVal *VectorOutputVal::zero() const {
  return new VectorOutputVal(size());
}

VectorOutputVal *VectorOutputVal::one() const {
  VectorOutputVal *won = new VectorOutputVal(size());
  for(unsigned int i=0; i<size(); i++)
    won->data[i] = 1.0;
  return won;
}

double VectorOutputVal::dot(const DoubleVec &other) const {
  assert(size() == other.size());
  double sum = 0;
  for(unsigned int i=0; i<size(); i++)
    sum += data[i]*other[i];
  return sum;
}

double VectorOutputVal::dot(const Coord &x) const {
  assert(size() == 3);
  double sum = 0;
  for(unsigned int i=0; i<3; i++)
    sum += data[i]*x[i];
  return sum;
}

ArithmeticOutputVal *VectorOutputVal::dot(const ArithmeticOutputVal &ov)
  const
{
  return ov.dotVector(*this);
}

ArithmeticOutputVal *VectorOutputVal::dotScalar(const ScalarOutputVal &ov)
  const
{
  VectorOutputVal *result = new VectorOutputVal(*this);
  *result *= ov.value();
  return result;
}

ArithmeticOutputVal *VectorOutputVal::dotVector(const VectorOutputVal &ov)
  const
{
  double d = dot(ov.data);
  return new ScalarOutputVal(d);
}

ArithmeticOutputVal *VectorOutputVal::dotSymmMatrix3(const SymmMatrix3 &ov)
  const
{
  return ov.dotVector(*this);
}

double VectorOutputVal::operator[](const IndexP &p) const {
  return data[p.integer()];
}
  
double &VectorOutputVal::operator[](const IndexP &p) {
  return data[p.integer()];
}

IndexP VectorOutputVal::getIndex(const std::string &str) const {
  // str must be "x", "y", or "z"
  return IndexP(new VectorFieldIndex(str[0] - 'x'));
}

IteratorP VectorOutputVal::getIterator() const {
  return IteratorP(new VectorFieldIterator(0, size()));
}

double VectorOutputVal::magnitude() const {
  double sum = 0.0;
  for(unsigned int i=0; i<size(); i++) {
    double x = data[i];
    sum += x*x;
  }
  return sqrt(sum);
}

VectorOutputVal operator+(const VectorOutputVal &a, const VectorOutputVal &b) {
  VectorOutputVal result(a);
  result += b;
  return result;
}

VectorOutputVal operator-(const VectorOutputVal &a, const VectorOutputVal &b) {
  VectorOutputVal result(a);
  result -= b;
  return result;
}

VectorOutputVal operator*(const VectorOutputVal &a, double b) {
  VectorOutputVal result(a);
  result *= b;
  return result;
}

VectorOutputVal operator*(double b, const VectorOutputVal &a) {
  VectorOutputVal result(a);
  result *= b;
  return result;
}

VectorOutputVal operator/(const VectorOutputVal &a, double b) {
  VectorOutputVal result(a);
  result *= (1./b);
  return result;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::string ListOutputVal::classname_("ListOutputVal");

ListOutputVal::ListOutputVal(const std::vector<std::string> *lbls)
  : data(lbls->size()),
    labels(*lbls) 
{
  for(unsigned int i=0; i<size(); i++)
    data[i] = 0.0;
}

ListOutputVal::ListOutputVal(const std::vector<std::string> *lbls,
			     const std::vector<double> &vec)
  : data(vec),
    labels(*lbls)
{
}

ListOutputVal::ListOutputVal(const ListOutputVal &other)
  : data(other.data),
    labels(other.labels)
{
}

double ListOutputVal::operator[](const IndexP &p) const {
  return data[p.integer()];
}
  
double &ListOutputVal::operator[](const IndexP &p) {
  return data[p.integer()];
}

const ListOutputVal &ListOutputVal::operator=(const OutputVal &other) {
  *this = dynamic_cast<const ListOutputVal&>(other);
  return *this;
}

const ListOutputVal &ListOutputVal::operator=(const ListOutputVal &other) {
  assert(labels == other.labels);
  data = other.data;
  return *this;
}

ListOutputVal *ListOutputVal::zero() const {
  return new ListOutputVal(&labels);
}

ListOutputVal *ListOutputVal::clone() const {
  return new ListOutputVal(*this);
}

DoubleVec *ListOutputVal::value_list() const {
  DoubleVec *res = new DoubleVec(data);
  return res;
}

IteratorP ListOutputVal::getIterator() const {
  return IteratorP(new ListOutputValIterator(this));
}

IndexP ListOutputVal::getIndex(const std::string &s) const {
  for(int i=0; i<size(); i++) {
    if(labels[i] == s)
      return IndexP(new ListOutputValIndex(this, i));
  }
  throw ErrProgrammingError("Bad index '" + s + "'", __FILE__, __LINE__);
}

void ListOutputValIndex::set(const std::vector<int> *vals) {
  assert(vals->size() == 1);
  assert((*vals)[0] < max_);
  index_ = (*vals)[0];
}

std::vector<int> *ListOutputValIndex::components() const {
  std::vector<int> *result = new std::vector<int>(1);
  (*result)[0] = index_;
  return result;
}

const std::string &ListOutputValIndex::shortstring() const {
  return ov_->labels[index_];
}

void ListOutputValIndex::print(std::ostream &os) const {
  os << "ListOutputValIndex(" << index_ << ")";
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

std::ostream &operator<<(std::ostream &os, const OutputVal &ov) {
  ov.print(os);
  return os;
}

std::ostream &operator<<(std::ostream &os, const OutputValue &value) {
  return os << *value.val;
}

void ScalarOutputVal::print(std::ostream &os) const {
  os << "ScalarOutputVal(" << val << ")";
}

void VectorOutputVal::print(std::ostream &os) const {
  os << "VectorOutputVal(";
  if(!data.empty()) {
    os << data[0];
    for(unsigned int i=1; i<size(); i++) {
      os << ", " << data[i];
    }
  }
  os << ")";
}

void ListOutputVal::print(std::ostream &os) const {
  os << "ListOutputVal(";
  if(size() > 0) {
    os << data[0];
    for(unsigned int i=1; i<size(); i++)
      os << ", " << data[i];
  }
  os << ")";
}
