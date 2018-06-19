// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


#ifndef CPIXELSELECTION_SWG
#define CPIXELSELECTION_SWG

%module cpixelselection

%{
#include "common/cmicrostructure.h"
#include "common/cpixelselection.h"
%}
%include "common/typemaps.swg"
%extern "common/pixelgroup.swg"
%extern "common/coord.swg"
%pragma(python) code="from ooflib.SWIG.common.pixelgroup import PixelGroupPtr"
%pragma(python) code="from ooflib.SWIG.common.pixelgroup import PixelSetPtr"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"
%pragma(python) code="from ooflib.SWIG.common.coord import ICoordPtr"

%pragma(python) include="cpixelselection.spy"

class CPixelSelection {
public:
  CPixelSelection(ICoord *iPoint, Coord *Point, CMicrostructure*);
  ~CPixelSelection();
  %new CPixelSelection *clone();
  const Coord size();
  const ICoord sizeInPixels();
  bool checkpixel(ICoord *iPoint);

  CMicrostructure *getMicrostructure();

  void clear(); 
  void invert();

  void select(PixelSelectionCourier*);
  void unselect(PixelSelectionCourier*);
  void toggle(PixelSelectionCourier*);
  void selectSelected(PixelSelectionCourier*);

  void clearWithoutCheck();
  void invertWithoutCheck();
  void selectWithoutCheck(PixelSelectionCourier*);
  void unselectWithoutCheck(PixelSelectionCourier*);
  void toggleWithoutCheck(PixelSelectionCourier*);

  // TODO 3.1: This should return a low-memory-use iterable object.
  // It's only used by PixelGroup._pixels_from_group via
  // PixelSelection.getSelection.  See similar TODO in pixelgroup.swg.
  ICoordVec *members();

  bool isSelected(ICoord *iPoint);
  void setFromGroup(PixelSet*);
  PixelSet *getPixelGroup();
  int len();
  bool empty();
  void getBounds(ICoord &ICoordOut, ICoord &ICoordOut);
  %addmethods {
    int __len__() {
      return self->len();
    }
  }
};

#endif // CPIXELSELECTION_SWG
