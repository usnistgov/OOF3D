// -*- C++ -*-
// $RCSfile: boolarray.swg,v $
// $Revision: 1.5.18.2 $
// $Author: langer $
// $Date: 2014/09/27 22:33:46 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BOOLARRAY_SWG
#define BOOLARRAY_SWG

%module boolarray
%include "common/typemaps.swg"

%{
#include "common/boolarray.h"
%}

class BoolArray {
public:
  ~BoolArray();
  BoolArray clone();
  void set(ICoord *iPoint);
  void reset(ICoord *iPoint);
  bool get(ICoord *iPoint);
  void toggle(ICoord *iPoint);
  void invert();
  //%new ICoordVec *pixels(bool);
};


#endif // BOOLARRAY_SWG
