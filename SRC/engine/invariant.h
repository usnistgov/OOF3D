// -*- C++ -*-
// $RCSfile: invariant.h,v $
// $Revision: 1.5.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:44:27 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef INVARIANT_H
#define INVARIANT_H

class OutputVal;

class Invariant {
public:
  virtual ~Invariant() {}
  virtual double operator()(const OutputVal&) const = 0;
};

class Magnitude : public Invariant {
public:
  virtual double operator()(const OutputVal&) const;
};

class MatrixTrace : public Invariant {
public:
  virtual double operator()(const OutputVal&) const;
};

class Determinant : public Invariant {
public:
  virtual double operator()(const OutputVal&) const;
};

class SecondInvariant : public Invariant {
public:
  virtual double operator()(const OutputVal&) const;
};

class Deviator : public Invariant {
public:
  virtual double operator()(const OutputVal&) const;
};

enum EigenValueRank {MAX_EIGENVALUE, MID_EIGENVALUE, MIN_EIGENVALUE};

class Eigenvalue : public Invariant {
private:
  const EigenValueRank which_;			
public:
  Eigenvalue(EigenValueRank *w) : which_(*w) {}
  virtual double operator()(const OutputVal&) const;
};

#endif // INVARIANT_H
