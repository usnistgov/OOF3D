// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include "eigen/unsupported/Eigen/SparseExtra" // for saveMarketVector
#include "common/doublevec.h"
#include "common/tostring.h"
#include <sstream>
#include <fstream>

DoubleVec DoubleVec::segment(int pos, int n) const {
  // Extract the n coeffs in the range [pos : pos+n-1]
  assert((pos+n-1) < data.size()); 
  DoubleVec part;
  part.data = data.segment(pos, n);
  return part;
} 

DoubleVec DoubleVec::subvec(int start, int end) const {
  // Extract the n coeffs in the range [start : end-1]
  assert(start<=end && end<=data.size());
  DoubleVec part;
  part.data = data.segment(start, end-start);
  return part;
}

void DoubleVec::segment_copy(int toPos, const DoubleVec& other, int pos,
			     int size)
{
  // Copy other's [pos, pos+size) to this [toPos, toPos+size)
  assert(pos >= 0 && pos + size <= other.data.size());
  assert(toPos >= 0 && toPos + size <= data.size());
  data.segment(toPos, size) = other.data.segment(pos, size);
}

DoubleVec& DoubleVec::operator+=(const DoubleVec& other) {
  data += other.data; 
  return *this;
}

DoubleVec& DoubleVec::operator-=(const DoubleVec& other) {
  data -= other.data;
  return *this;
}

DoubleVec& DoubleVec::operator*=(double alpha) {
  data *= alpha;
  return *this;
}

DoubleVec& DoubleVec::operator/=(double alpha) {
  data /= alpha;
  return *this;
}

void DoubleVec::scale(double alpha) {
  data *= alpha;
}

void DoubleVec::axpy(double alpha, const DoubleVec& x) {
  data += alpha * x.data;
}

DoubleVec DoubleVec::operator+(const DoubleVec& other) const {
  DoubleVec rst;
  rst.data = data + other.data;
  return rst;
}

DoubleVec DoubleVec::operator-(const DoubleVec& other) const {
  DoubleVec rst;
  rst.data = data - other.data;
  return rst;
}

DoubleVec DoubleVec::operator*(double alpha) const {
  DoubleVec rst;
  rst.data = data * alpha;
  return rst;
}

DoubleVec DoubleVec::operator/(double alpha) const {
  DoubleVec rst;
  rst.data = data / alpha;
  return rst;
}

// Friend method of DoubleVec, return the result of (scalar * vec)
DoubleVec operator*(double alpha, const DoubleVec& mat) {
  DoubleVec rst;
  rst.data = alpha * mat.data;
  return rst;
}

double DoubleVec::dot(const DoubleVec& other) const {
  return data.dot(other.data); 
}

double dot(const DoubleVec& x, const DoubleVec& y) {
  return x.dot(y);
}

double DoubleVec::operator*(const DoubleVec& other) const {
  return data.dot(other.data); 
}

DoubleVec::iterator DoubleVec::begin() {
  return iterator(*this);
}

DoubleVec::iterator DoubleVec::end() {
  iterator it(*this);
  it.to_end();
  return it;
}

DoubleVec::const_iterator DoubleVec::begin() const {
  return const_iterator(*this);
}

DoubleVec::const_iterator DoubleVec::end() const {
  const_iterator it(*this);
  it.to_end();
  return it;
}

const std::string DoubleVec::str() const {
  // return to_string(*this);
  std::ostringstream os;
  os << *this;
  return os.str();
}

std::ostream& operator<<(std::ostream& os, const DoubleVec& vec) {
  int n = vec.size();
  std::cerr << "****** operator<<(DoubleVec): n=" << n << std::endl;
  if(n > 0) {
    int prec = os.precision();
    os << std::setprecision(PRECISION); // PRECISION defined in printvec.h
    for(unsigned int i=0; i<n; i++) {
      os << vec.data[i];
      if((i+1)%10 == 0)
	os << std::endl;
      else
	os << " ";
    }
    os << std::setprecision(prec);
  }
  else {
    os << "(empty)";
  }
  //  os << vec.data;
  return os;
}

bool save_market_vec(const DoubleVec& vec, const std::string& filename) {
  return Eigen::saveMarketVector(vec.data, filename);
}

bool load_market_vec(DoubleVec& vec, const std::string& filename) {
  return Eigen::loadMarketVector(vec.data, filename);
}

bool save_vec(const DoubleVec& vec, const std::string& filename) {
  int precision = 13;
  std::ofstream fs(filename); 
  // floatfield set to scientific
  fs.setf(std::ios::scientific, std::ios::floatfield);
  fs.precision(precision);

  int size = vec.size();
  fs << vec.size() << std::endl;
  for (int i = 0; i < size; i++) {
    fs << vec.data[i] << std::endl;
  }
  return true;
}

bool load_vec(DoubleVec& vec, const std::string& filename) {
  std::ifstream fs(filename);
  std::string line;
  
  // Ignore the comments at the begining of file
  while (!fs.eof()) {
    std::getline(fs, line);
    // '#' is the comment flag
    if (line[0] != '#')
      break;
  }

  // extract vector size info
  int size;
  std::stringstream ss;
  ss << line;
  ss >> size;

  vec.resize(size);

  // read vector
  double val;
  for (int i = 0; i < size; i++) {
    fs >> val;
    vec.data[i] = val;
  }

  return true;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

template<typename VT, typename ET>
DoubleVecIterator<VT, ET>& DoubleVecIterator<VT, ET>::operator++() {
  assert(index + 1 <= vec.data.size());
  index += 1;
  return *this;
}

template<typename VT, typename ET>
ET& DoubleVecIterator<VT, ET>::operator*() {
  assert(!done());
  return vec.data[index];
}

template<typename VT, typename ET>
bool DoubleVecIterator<VT, ET>::operator==(const DoubleVecIterator& other) const
{
 // TODO: Is there some subtle reason that this line isn't simply
 // return &vec==&other.vec && index==other.index;  ?
  return (&vec==&other.vec && index==other.index) ? true : false;
}

template<typename VT, typename ET>
bool DoubleVecIterator<VT, ET>::operator!=(const DoubleVecIterator& other) const
{
  return (&vec==&other.vec && index!=other.index) ? true : false;
}

template<typename VT, typename ET>
bool DoubleVecIterator<VT, ET>::operator<(const DoubleVecIterator& other) const
{
  return (&vec==&other.vec && index<other.index) ? true : false;
}

template<typename VT, typename ET>
bool DoubleVecIterator<VT, ET>::done() const {
  return index < vec.data.size() ? false : true;
}

// Instantiate the DoubleVecIterator template.
template class DoubleVecIterator<DoubleVec, double>;
template class DoubleVecIterator<const DoubleVec, const double>;

