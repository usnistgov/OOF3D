// -*- C++ -*-
// $RCSfile: coord.swg,v $
// $Revision: 1.13.8.5 $
// $Author: langer $
// $Date: 2014/06/12 18:48:36 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef COORD_SWG
#define COORD_SWG

%module coord
%include "common/typemaps.swg"
%{
#include <oofconfig.h>
#include "common/coord.h"
%}
%pragma(python) include="common/coord.spy"


class Position {
};
  
class Coord : public Position {
public:
#ifndef DIM_3
  Coord(double x1, double x2);
#else
  Coord(double x1, double x2, double x3);
#endif
  ~Coord();
};

%addmethods Coord {
  // This function is 'getitem', not '__getitem__', because
  // __getitem__ is defined in terms of getitem in the .spy file.
  // __getitem__ raises a Python exception if the argument is out of
  // range.
  double getitem(int i) {
    return (*self)[i];
  }
  int __len__() {
    return DIM;
  }
  Coord __mul__(double x) {
    return (*self)*x;
  }
  Coord __rmul__(double x) {
    return (*self)*x;
  }
  Coord __neg__() {
    return -(*self);
  }
  %new Coord *clone() {
    return new Coord(*self);
  }
}

double dot(Coord&, Coord&);

class ICoord {
public:
#ifndef DIM_3
  ICoord(int x, int y);
#else
	ICoord(int x, int y, int z);
#endif
};

%addmethods ICoord {
  int __getitem__(int i) {
    return (*self)[i];
  }
  int __len__() {
    return DIM;
  }
  ICoord __mul__(int x) {
    return (*self)*x;
  }
  ICoord __rmul__(int x) {
    return (*self)*x;
  }
  ICoord __neg__() {
    return -*self;
  }
  %new ICoord *clone() {
    return new ICoord(*self);
  }
}

#endif // COORD_SWG
