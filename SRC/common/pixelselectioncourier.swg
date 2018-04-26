// -*- C++ -*-

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PIXELSELECTIONCOURIER_SWG
#define PIXELSELECTIONCOURIER_SWG

%module pixelselectioncourier

%include "common/typemaps.swg"
%extern "common/coord.swg"

%{
#include "common/cmicrostructure.h"
#include "common/pixelselectioncourier.h"
#include "common/tostring.h"
#include "common/geometry.h"
%}

class PixelSelectionCourier {
public:
  %addmethods {
    // TODO: Putting the __repr__ here doesn't work. SWIG will
    // generate a new (and nearly useless) __repr__for each subclass
    // automatically.  This needs to be copied into each subclass to
    // prevent SWIG from redefining it.
    %new const string *__repr__() {	// for debugging
      return new std::string(to_string(*self));
    }
  }
  CMicrostructure *getMicrostructure();
};

class PointSelection : public PixelSelectionCourier {
public:
  PointSelection(CMicrostructure*, Coord *Point);
  ~PointSelection();
};

class PointlessSelection : public PixelSelectionCourier {
public:
  PointlessSelection(CMicrostructure*);
  ~PointlessSelection();
};

#ifndef DIM_3
class BrushSelection : public PixelSelectionCourier {
public:
  BrushSelection(CMicrostructure*, BrushStyle*, PointVec *PointList);
  ~BrushSelection();
};
#endif

class BoxSelection : public PixelSelectionCourier {
public:
  BoxSelection(CMicrostructure*, CRectangularPrism*);
  ~BoxSelection();
};

class CircleSelection : public PixelSelectionCourier {
public:
  CircleSelection(CMicrostructure*, Coord *Point, double);
  ~CircleSelection();
};

class EllipseSelection : public PixelSelectionCourier {
public:
  EllipseSelection(CMicrostructure*, Coord *Point, Coord *Point);
  ~EllipseSelection();
};

class GroupSelection : public PixelSelectionCourier {
public:
  GroupSelection(CMicrostructure*, PixelSet*);
  ~GroupSelection();
};

class IntersectSelection : public PixelSelectionCourier {
public:
  IntersectSelection(CMicrostructure*, PixelSet*, PixelSelectionCourier*);
  ~IntersectSelection();
  %addmethods {
    %new const string *__repr__() {
      return new std::string(to_string(*self));
    }
  }
};

class DespeckleSelection : public PixelSelectionCourier {
public:
  DespeckleSelection(CMicrostructure*, PixelSet*, int);
  ~DespeckleSelection();
};

class ElkcepsedSelection : public PixelSelectionCourier {
public:
  ElkcepsedSelection(CMicrostructure*, PixelSet*, int);
  ~ElkcepsedSelection();
};

class ExpandSelection : public PixelSelectionCourier {
public:
  ExpandSelection(CMicrostructure*, PixelSet*, double);
  ~ExpandSelection();
};

class ShrinkSelection : public PixelSelectionCourier {
public:
  ShrinkSelection(CMicrostructure*, PixelSet*, double);
  ~ShrinkSelection();
};

#endif // PIXELSELECTIONCOURIER_SWG
