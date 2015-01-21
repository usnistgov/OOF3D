// -*- C++ -*-
// $RCSfile: mastercoord.swg,v $
// $Revision: 1.12.10.2 $
// $Author: fyc $
// $Date: 2013/04/24 16:01:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MASTERCOORD_SWG
#define MASTERCOORD_SWG

%module mastercoord
%include "engine/typemaps.swg"

%{
#include "engine/mastercoord.h"
%}
%pragma(python) include="mastercoord.spy"

class MasterPosition {
public:
  MasterCoord mastercoord();
};

class MasterCoord : public MasterPosition {
public:
#ifndef DIM_3
  MasterCoord(double x1, double x2);
#else
  MasterCoord(double x1, double x2, double x3);
#endif
  ~MasterCoord();
  %addmethods {
    double __getitem__(int i) {
      return (*self)[i];
    }
    MasterCoord __add__(MasterCoord &other) {
      return *self + other;
    }
    MasterCoord __sub__(MasterCoord &other) {
      return *self - other;
    }
    MasterCoord __mul__(double a) {
      return a*(*self);
    }
    MasterCoord __rmul__(double a) {
      return a*(*self);
    }
    MasterCoord __div__(double a) {
      return *self/a;
    }
  }
};


#endif // MASTERCOORD_SWG

