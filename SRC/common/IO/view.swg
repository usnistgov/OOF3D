// -*- C++ -*-
// $RCSfile: view.swg,v $
// $Revision: 1.1.2.12 $
// $Author: langer $
// $Date: 2014/07/31 18:32:48 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef VIEW_SWG
#define VIEW_SWG

%module view
%include "common/typemaps.swg"
%extern "common/coord.swg"
%extern "common/clip.swg"
%pragma(python) code="from ooflib.SWIG.common.coord import CoordPtr"
%pragma(python) code="from ooflib.SWIG.common.coord import ICoordPtr"
%pragma(python) code="from ooflib.SWIG.common.clip import ClippingPlanePtr"
%pragma(python) include="view.spy"

%{
#include "common/IO/view.h"
#include "common/coord.h"
%}

class View {
public:
  int size_x, size_y;
  Coord pos;
  Coord focal;
  Coord up;
  double angle;
  View(Coord *Point, Coord *Point, Coord *Point, double, int, int);
  ~View();
  int nClipPlanes();
  void addClipPlane(ClippingPlane&);
  void replaceClipPlane(unsigned int, ClippingPlane&);
  void removeClipPlane(unsigned int);
  void enableClipPlane(unsigned int);
  bool enabledClipPlane(unsigned int);
  void disableClipPlane(unsigned int);
  void flipClipPlane(unsigned int);
  void unflipClipPlane(unsigned int);
  void invertClipOn();
  void invertClipOff();
  bool invertedClip();
  void suppressClipOn();
  void suppressClipOff();
  bool suppressedClip();
  bool equiv(View&);
  const ClippingPlane &getClipPlane(unsigned int);
  %addmethods {
    %new View *clone() {
      return new View(*self);
    }
  }
};


#endif // VIEW_SWG
