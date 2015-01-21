// -*- C++ -*-
// $RCSfile: doublevec.h,v $
// $Revision: 1.1.4.6 $
// $Author: langer $
// $Date: 2014/10/15 20:53:43 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>
#include <string>

#ifndef DOUBLEVEC_H
#define DOUBLEVEC_H

// DoubleVec is just a trivial wrapper for std::vector<double>.  It
// allows std::vector<double> to be swigged, and allows debugging code
// to be attached to methods that aren't easily accessible in the base
// class.  

#include <vector>
#include <string>

class DoubleVec: public std::vector<double> {
public:
  typedef std::vector<double>::size_type size_type;
  typedef std::vector<double>::iterator iterator;
  typedef std::vector<double>::const_iterator const_iterator;
  DoubleVec();
  DoubleVec(size_type);
  DoubleVec(size_type, const double&);
  DoubleVec(const std::vector<double>&);

  template <class InputIterator>
  DoubleVec(InputIterator a, InputIterator b)
    : std::vector<double>(a, b)
  {
#ifdef DEBUG
    addVec(this);
    addTotal(size());
#endif // DEBUG
  }
  DoubleVec(const DoubleVec&);
  DoubleVec &operator=(const DoubleVec&);
  virtual ~DoubleVec();
  DoubleVec *clone() const;
  void resize(size_type n, double x=0);
  // void reserve(size_type);
  double norm() const;
  void push_back(const double&);
  void clear();
  iterator erase(iterator);
  iterator erase(iterator, iterator);
  void pop_back();
#ifdef DEBUG
  std::string addr() const;
  static long total;
  static void addTotal(int);
  static void addVec(DoubleVec*);
  static void removeVec(DoubleVec*);
#endif // DEBUG
};

#ifdef DEBUG
void printVecSizes(const std::string&);
#else
#define printVecSizes(str) /* */
#endif // DEBUG

#endif // DOUBLEVEC_H
