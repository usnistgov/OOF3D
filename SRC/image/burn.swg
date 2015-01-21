// -*- C++ -*-
// $RCSfile: burn.swg,v $
// $Revision: 1.7.18.2 $
// $Author: langer $
// $Date: 2014/09/27 22:34:37 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef BURN_SWG
#define BURN_SWG

%module burn
%include "common/typemaps.swg"

%{
#include "image/burn.h"
%}
%pragma(python) include="burn.spy"

class OOFImage;

class Burner {
public:
  bool next_nearest;
};

class BasicBurner : public Burner {
public:
  BasicBurner(double lcl, double glbl, bool useL2, bool nn);
};


#endif // BURN_SWG
