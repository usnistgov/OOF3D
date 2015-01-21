// -*- C++ -*-
// $RCSfile: contourcell.swg,v $
// $Revision: 1.10.18.1 $
// $Author: langer $
// $Date: 2013/11/08 20:43:15 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CONTOURCELL_SWG
#define CONTOURCELL_SWG

%module contourcell
%include "engine/typemaps.swg"

%extern "mastercoord.swg"

%{
#include "engine/contourcell.h"
%}

%pragma(python) include="engine/contourcell.spy"

class ContourCellCoord {
public:
  double x, y;
  int ix, iy;
};

class ContourCellSkeleton {
public:
  %addmethods {
  ContourCellCoord getitem(int i) {
    return self->corner[i];
  }
//   void __setitem__(int i, const MasterCoord &mc) {
//     self->corner[i] = mc;
//   }
  int __len__() { return 3; }
  }
};

#endif // CONTOURCELL_SWG
