/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DOUBLEVEC_H
#define DOUBLEVEC_H

#include <iostream>
#include <string>
#include "eigen/Eigen/SparseCore"

class SparseMat;
class SmallMatrix;
template<typename VT, typename ET> class DoubleVecIterator;
enum class Precond;
template<typename Derived> class IterativeSolver;
template<typename Derived> class DirectSolver;


class DoubleVec {
private:
  Eigen::VectorXd data; // N x 1 matrix

public:
  DoubleVec() = default;
  DoubleVec(int size, double val=0) { data.setConstant(size, val); }
  DoubleVec(const DoubleVec&) = default;
  DoubleVec& operator=(const DoubleVec&) = default;
  ~DoubleVec() = default;
  
  //TODO(lizhong): inline possible methods
  
  /* Vector property methods */
  
  int size() const { return data.size(); }
  void resize(int size, double val=0) { data.setConstant(size, val); }
  void zero() { data.setZero(); }
  void ones() { data.setOnes(); }
  double& operator[](int index) { return data[index]; }
  const double& operator[](int index) const { return data[index]; }
  DoubleVec segment(int pos, int n) const;
  DoubleVec subvec(int start, int end) const;
  void segment_copy(int, const DoubleVec&, int, int);

  typedef int size_type;

  /* Arithmetic operations */

  double norm() const { return data.norm(); }

  // In-place operations, using no temporaries
  DoubleVec& operator+=(const DoubleVec&);
  DoubleVec& operator-=(const DoubleVec&);
  DoubleVec& operator*=(double);
  DoubleVec& operator/=(double);
  void axpy(double alpha, const DoubleVec& x);
  void scale(double alpha);
  
  // Non-in-place, which may return a temporary object.
  DoubleVec operator+(const DoubleVec&) const;
  DoubleVec operator-(const DoubleVec&) const;
  DoubleVec operator*(double) const;
  DoubleVec operator/(double) const;
  friend DoubleVec operator*(double, const DoubleVec&);

  // dot product
  double dot(const DoubleVec&) const;
  double operator*(const DoubleVec&) const;

  // TODO(lizhong): remove this in the future, currently, it is 
  // only for compatibility with cg, bicg and etc. solvers.
  friend double dot(const DoubleVec&, const DoubleVec&);

  /* Iterators */

  friend class DoubleVecIterator<DoubleVec, double>;
  friend class DoubleVecIterator<const DoubleVec, const double>;
  typedef DoubleVecIterator<DoubleVec, double> iterator;
  typedef DoubleVecIterator<const DoubleVec, const double> const_iterator;
  iterator begin();
  iterator end();
  const_iterator begin() const;
  const_iterator end() const;

  /* Miscellaneous */

  const std::string str() const;

  friend SparseMat;
  friend SmallMatrix;
  template<typename Derived> friend class IterativeSolver;
  template<typename Derived> friend class DirectSolver;
  friend std::ostream& operator<<(std::ostream&, const DoubleVec&);
  friend bool save_market_vec(const DoubleVec&, const std::string&);
  friend bool load_market_vec(DoubleVec&, const std::string&);
  friend bool save_vec(const DoubleVec&, const std::string&);
  friend bool load_vec(DoubleVec&, const std::string&);
};

template<typename VT, typename ET>
class DoubleVecIterator {
private:
  VT& vec;
  int index;

public:
  DoubleVecIterator(VT& vec) : vec(vec), index(0) {}
  
  DoubleVecIterator& operator++();
  ET& operator*();

  bool operator==(const DoubleVecIterator&) const;
  bool operator!=(const DoubleVecIterator&) const;
  bool operator<(const DoubleVecIterator&) const;

  bool done() const;

  friend DoubleVec;
  friend std::ostream& operator<<(std::ostream& os,
    const DoubleVecIterator<VT, ET>& it) {
    return os << *it;
  }

private:
  void to_end() { index = vec.size(); }
};

#endif // DOUBLEVEC_H
