// -*- C++ -*-
// $RCSfile: rubberband3d.swg,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2014/09/27 22:34:13 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef RUBBERBAND3D_SWG
#define RUBBERBAND3D_SWG

%module rubberband
%include "common/typemaps.swg"
%{
#include "common/IO/GUI/rubberband3d.h"
%}
%extern "gfxbrushstyle.swg"

class RubberBand {};

class NoRubberBand : public RubberBand {
public:
  NoRubberBand();
};


class SpiderRubberBand : public RubberBand {
public:
  SpiderRubberBand(PointVec *PointList);
  ~SpiderRubberBand();
};


#endif // RUBBERBAND_SWG


