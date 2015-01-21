// -*- C++ -*-
// $RCSfile: pixelselectioncouriere.swg,v $
// $Revision: 1.4.18.2 $
// $Author: langer $
// $Date: 2011/08/25 21:38:11 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PIXELSELECTIONCOURIERE_SWG
#define PIXELSELECTIONCOURIERE_SWG

%module pixelselectioncouriere

%include "engine/typemaps.swg"
%extern "common/pixelselectioncourier.swg"

%{
#include "common/coord.h"
#include "engine/pixelselectioncouriere.h"
#include "engine/cskeleton2.h"
%}

%pragma(python) code="from ooflib.SWIG.common.pixelselectioncourier import PixelSelectionCourierPtr"


class ElementSelection : public PixelSelectionCourier {
public:
  ElementSelection(CMicrostructure*, CSkeletonElement*);
  ~ElementSelection() {}
};

class SegmentSelection : public PixelSelectionCourier {
public:
  SegmentSelection(CMicrostructure*, Coord *Point, Coord *Point);
  ~SegmentSelection() {}
};

class MaterialSelectionBase : public PixelSelectionCourier {}

class MaterialSelection : public MaterialSelectionBase {
public:
  MaterialSelection(CMicrostructure*, Material*);
  ~MaterialSelection() {}
};

class AnyMaterialSelection : public MaterialSelectionBase {
public:
  AnyMaterialSelection(CMicrostructure*);
  ~AnyMaterialSelection() {}
};

class NoMaterialSelection : public MaterialSelectionBase {
public:
  NoMaterialSelection(CMicrostructure*);
  ~NoMaterialSelection() {}
};

#endif
