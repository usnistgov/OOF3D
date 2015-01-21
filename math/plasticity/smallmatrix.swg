// -*- C++ -*-
// $RCSfile: smallmatrix.swg,v $
// $Revision: 1.1 $
// $Author: reida $
// $Date: 2006/12/07 14:02:35 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@ctcms.nist.gov. 
 */


#ifndef SMALLMATRIX_SWG
#define SMALLMATRIX_SWG

%module smallmatrix

%{
#include "smallmatrix.h"
%}

%pragma(python) include="smallmatrix.spy"

class SmallMatrix {
public:
  SmallMatrix(int, int);
  ~SmallMatrix();
  void clear();
  int solve(SmallMatrix &);
  int rows();
  int cols();
  %addmethods {
    double getitem(int i, int j) {
      return (*self)(i,j);
    }
    void setitem(int i, int j, double v) {
      (*self)(i,j)=v;
    }
    // imul only defined for scalars.
    SmallMatrix __imul__(double x) {
      return (*self).operator*=(x);
    }
    // These two get called by the __mul__ routine in the .spy file.
    SmallMatrix multbyscalar(double x) {
      return operator*(*self, x);
    }
    SmallMatrix multbymatrix(const SmallMatrix &x) {
      return operator*(*self, x);
    }
    // Arithmetic, visible to Python.
    SmallMatrix __iadd__(const SmallMatrix &x) {
      return (*self).operator+=(x);
    }
    SmallMatrix __isub__(const SmallMatrix &x) {
      return (*self).operator-=(x);
    }
    SmallMatrix __add__(const SmallMatrix &x) {
      return operator+(*self, x);
    }
    SmallMatrix __sub__(const SmallMatrix &x) {
      return operator-(*self, x);
    }
  }
};

#endif
