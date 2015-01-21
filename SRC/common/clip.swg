// -*- C++ -*-
// $RCSfile: clip.swg,v $
// $Revision: 1.1.2.6 $
// $Author: langer $
// $Date: 2013/07/19 20:24:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef CLIP_SWG
#define CLIP_SWG

%module clip
%include "common/typemaps.swg"
%extern "common/direction.swg"
%pragma(python) include="clip.spy"

%{
#include "common/clip.h"
#include "common/direction.h"
%}

%typemap(python, out) CDirection* {
  $target = $source->pythonObject();
}

class ClippingPlane {
public:
  ClippingPlane(CDirection*, double);
  ~ClippingPlane();
  CDirection *normal();
  double offset();
  void enable();
  void disable();
  bool enabled();
  void flip();
  void unflip();
  bool flipped();
  %addmethods {
    %new ClippingPlane *clone() {
      return new ClippingPlane(*self);
    }
  }
};

#endif // CLIP_SWG
