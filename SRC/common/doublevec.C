// -*- C++ -*-
// $RCSfile: doublevec.C,v $
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
#include "common/doublevec.h"
#include "common/lock.h"
#include "common/vectormath.h"
#include "common/IO/oofcerr.h"
#include <iostream>

// This file is completely unnecessary except when debugging.  It just
// adds debugging code to the python-wrapped std::vector<double>.

#define VDEBUG DEBUG

#ifdef DEBUG
// printVecSizes and DoubleVec::total are inside DEBUG blocks and not
// VDEBUG blocks so that we don't have to change doublevec.h when
// VDEBUG changes.
#include <stdlib.h>
long DoubleVec::total = 0;

#include <set>
static std::set<DoubleVec*> allVecs;
void DoubleVec::addVec(DoubleVec *vec) {
  std::set<DoubleVec*>::iterator i = allVecs.find(vec);
  assert(i == allVecs.end());
  allVecs.insert(vec);
}

void DoubleVec::removeVec(DoubleVec *vec) {
  std::set<DoubleVec*>::iterator i = allVecs.find(vec);
  assert(i != allVecs.end());
  allVecs.erase(i);
}

void printVecSizes(const std::string &msg) {
#if VDEBUG
  static long lastsize = 0;
  long diff = DoubleVec::total  - lastsize;
  oofcerr << "**** Total of all DoubleVec sizes "<< msg << ": "
  	  << DoubleVec::total
  	  << " (" << (diff < 0? "" : "+") << diff << ") ****" << std::endl;
  lastsize = DoubleVec::total;
#endif
}

#if VDEBUG
void printAtExit() {
  printVecSizes("at exit");
  oofcerr << "**** There are " << allVecs.size() << " remaining DoubleVecs.  ****" << std::endl;
}
#endif // VDEBUG
#endif // DEBUG


DoubleVec::DoubleVec() {
#if VDEBUG
  addVec(this);
#endif
}

DoubleVec::DoubleVec(DoubleVec::size_type n)
  : std::vector<double>(n, 0.0)
{
#if VDEBUG
  static bool initialized = false;
  if(!initialized) {
    initialized = true;
    atexit(printAtExit);
  }
  addTotal(n);
  addVec(this);
#endif // VDEBUG
}

DoubleVec::DoubleVec(DoubleVec::size_type n, const double &x)
  : std::vector<double>(n, x)
{
#if VDEBUG
  addTotal(n);
  addVec(this);
#endif // VDEBUG
}

DoubleVec::DoubleVec(const std::vector<double> &vec)
  : std::vector<double>(vec)
{
#if VDEBUG
  addTotal(size());
  addVec(this);
#endif // VDEBUG
}

DoubleVec::DoubleVec(const DoubleVec &other)
  : std::vector<double>(other)
{
#if VDEBUG
  addTotal(size());
  addVec(this);
#endif // VDEBUG
}

DoubleVec &DoubleVec::operator=(const DoubleVec &other) {
#if VDEBUG
  addTotal(other.size() - size());
#endif // VDEBUG
  std::vector<double>::operator=(other);
  return *this;
}

DoubleVec::~DoubleVec() {
#if VDEBUG
  addTotal(-size());
  removeVec(this);
#endif // VDEBUG
}

void DoubleVec::clear() {
#if VDEBUG
  addTotal(-size());
#endif	// VDEBUG
  std::vector<double>::clear();
}

void DoubleVec::resize(DoubleVec::size_type n, double x) {
#if VDEBUG
  int oldsize = size();
#endif	// VDEBUG
  std::vector<double>::resize(n, x);
#if VDEBUG
  addTotal(size() - oldsize);
#endif // VDEBUG
}

void DoubleVec::push_back(const double &x) {
  std::vector<double>::push_back(x);
#if VDEBUG
  addTotal(1);
#endif // VDEBUG
}

DoubleVec::iterator DoubleVec::erase(DoubleVec::iterator it) {
#if VDEBUG
  int oldsize = size();
#endif // VDEBUG
  DoubleVec::iterator res = std::vector<double>::erase(it);
#if VDEBUG
  addTotal(size() - oldsize);
#endif	// VDEBUG
  return res;
}

DoubleVec::iterator DoubleVec::erase(DoubleVec::iterator f,
				     DoubleVec::iterator l)
{
#if VDEBUG
  int oldsize = size();
#endif // VDEBUG
  DoubleVec::iterator res = std::vector<double>::erase(f, l);
#if VDEBUG
  addTotal(size() - oldsize);
#endif	// VDEBUG
  return res;
}

void DoubleVec::pop_back() {
#if VDEBUG
  int oldsize = size();
#endif // VDEBUG
  std::vector<double>::pop_back();
#if VDEBUG
  addTotal(size() - oldsize);
#endif	// VDEBUG
}

double DoubleVec::norm() const {
  return sqrt(dot(*this, *this));
}

#ifdef DEBUG
#include <iomanip>
#include <sstream>
std::string DoubleVec::addr() const {
  std::ostringstream os;
  os << std::hex << this;
  return os.str();
}

void DoubleVec::addTotal(int n) {
  static SLock lock;
  lock.acquire();
  DoubleVec::total += n;
  lock.release();
}
#endif	// DEBUG
