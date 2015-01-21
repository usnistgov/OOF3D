// -*- C++ -*-
// $RCSfile: activearea.swg,v $
// $Revision: 1.9.18.6 $
// $Author: langer $
// $Date: 2014/09/15 15:08:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef ACTIVEAREA_SWG
#define ACTIVEAREA_SWG

%module cactivearea

%{
#include "common/activearea.h"
%}
%include "common/typemaps.swg"
%extern "common/cpixelselection.swg"
%extern "common/pixelattribute.swg"
%pragma(python) code="from ooflib.SWIG.common.cpixelselection import CPixelSelectionPtr"
%pragma(python) code="from ooflib.SWIG.common.pixelattribute import PxlAttributeRegistrationPtr"
%pragma(python) include="activearea.spy"

class ActiveArea : public CPixelSelection {
public:
  ActiveArea(ICoord *iPoint, Coord *Point, CMicrostructure*);
  ~ActiveArea();
  %new ActiveArea *clone();
  %new ActiveArea *named_clone(const char*) const;
  bool isActive(ICoord *iPoint);
  void override(bool);
  bool getOverride();
  // name() and rename() are actually in SubAttribute, which is a
  // non-swigged base class of ActiveArea.
  const string &name();
  void rename(const char*);
  void clear();

  // add_pixels is only used when loading a microstructure from a file
  // and is inefficient.  See the TODO OPT in microstructureIO.py
  void add_pixels(ICoordVec *iPointList);
};

class ActiveAreasAttributeRegistration : public PxlAttributeRegistration {
public:
  ActiveAreasAttributeRegistration();
};

// PixelAttribute and ListAttribute are not SWIG'd, so leave them out.
class ActiveAreaList {
public:
  void add(ActiveArea *aa);
  void remove(ActiveArea *aa);
  StringVec* names();
};

ActiveAreaList *areaListFromPixel(CMicrostructure*, ICoord *iPoint);


#endif // ACTIVEAREA_SWG
