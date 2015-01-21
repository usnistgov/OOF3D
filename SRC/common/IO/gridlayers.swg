// -*- C++ -*-
// $RCSfile: gridlayers.swg,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2014/11/25 19:20:08 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GRIDLAYERS_SWG
#define GRIDLAYERS_SWG

%module gridlayers

%include "common/typemaps.swg"
%extern "common/IO/canvaslayers.swg"
%extern "common/IO/gridsourcebase.swg"

%{
#include "common/ccolor.h"
#include "common/vtkColorLUT.h"
#include "common/IO/vtkutils.h"
#include "common/IO/gridlayers.h"
#include "common/IO/gridsourcebase.h"
%}

%extern "common/IO/canvaslayers.swg"
%pragma(python) code="from ooflib.SWIG.common.IO.canvaslayers import OOFCanvasLayerPtr"

class WireGridCanvasLayer : public OOFCanvasLayer {
public:
  WireGridCanvasLayer(GhostOOFCanvas*, const char*, GridSourcePtr);
  void set_color(const CColor&);
  void set_lineWidth(int);
};

class FilledGridCanvasLayer : public OOFCanvasLayer {
public:
  void set_lookupTable(vtkLookupTablePtr, double, double);
};

class SolidFilledGridCanvasLayer : public FilledGridCanvasLayer {
public:
  SolidFilledGridCanvasLayer(GhostOOFCanvas*, const char*, GridSourcePtr);
  void set_CellData(vtkDataArrayPtr);
};

class ContourGridCanvasLayer : public OOFCanvasLayer {
public:
  ContourGridCanvasLayer(GhostOOFCanvas*, const char*, GridSourcePtr);
  void set_pointData(vtkDoubleArrayPtr);
  void set_nContours(int, double, double);
  void set_lookupTable(vtkLookupTablePtr);
};


#endif // GRIDLAYERS_SWG
