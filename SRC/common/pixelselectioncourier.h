// -*- C++ -*-
// $RCSfile: pixelselectioncourier.h,v $
// $Revision: 1.18.8.8 $
// $Author: langer $
// $Date: 2013/07/03 20:44:32 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef PIXELSELECTIONCOURIER_H
#define PIXELSELECTIONCOURIER_H

#include "common/boolarray.h"
#include "common/coord.h"
#include "common/pixelgroup.h"
#include <set>
#include <iostream>
#include <math.h>

class CMicrostructure;
#if DIM==2
class BrushStyle;
#endif
class CSkeletonElement;

// Base class for pixel selection courier ... point, brush, circle,
// etc.  PixelSelectionCouriers are efficient ways of passing a bunch
// of pixels from Python to C++, without having to create and pass a
// list of pixels.  Basically, Python just creates a way of describing
// the set of pixels, and C++ creates a list from it, if it needs to.

class PixelSelectionCourier {
protected:
  CMicrostructure *ms;
  ICoord pixelFromPoint(const Coord&) const;
  bool done_;
public:
  PixelSelectionCourier(CMicrostructure *ms);
  virtual ~PixelSelectionCourier() {}
  virtual void start() = 0;
  virtual ICoord currentPoint() const = 0;
  virtual void next() = 0;
  bool done() const { return done_; }
  CMicrostructure *getMicrostructure() const { return ms; }
  virtual void print(std::ostream &os) const = 0;
};

class PointlessSelection : public PixelSelectionCourier {
public:
  PointlessSelection(CMicrostructure *ms);
  virtual void start() {}
  virtual void next() {}
  virtual ICoord currentPoint() const;
  virtual void print(std::ostream &) const;
};

// Point
class PointSelection : public PixelSelectionCourier {
private:
  const Coord mousepoint;
public:
  PointSelection(CMicrostructure *ms, const Coord *mp);
  virtual ~PointSelection() {}
  virtual void start() {}
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

#if DIM==2
// Brush
class BrushSelection : public PixelSelectionCourier {
private:
  BrushStyle *brush;
  const std::vector<Coord> points;
  std::vector<Coord>::const_iterator pts_iter;
  BoolArray master;
  BoolArray selected;
  BoolArray::iterator sel_iter;
  ICoord offset;
  void advance();
public:
  BrushSelection(CMicrostructure *ms, BrushStyle *brush,
		 const std::vector<Coord> *points);
  virtual ~BrushSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};
#endif	// DIM==2

// Rectangle
class BoxSelection : public PixelSelectionCourier {
private:
  ICoord ll;
  ICoord ur;
  ICoord currentpt;
public:
  BoxSelection(CMicrostructure *ms, const Coord *pt0, const Coord *pt1);
  virtual ~BoxSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Circle
class CircleSelection : public PixelSelectionCourier {
private:
  const Coord center;
  const double radius2;
  ICoord ll;
  ICoord ur;
  ICoord currentpt;
  bool interior();
  void advance();
public:
  CircleSelection(CMicrostructure *ms,
		  const Coord *c, const double r);
  virtual ~CircleSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Ellipse
class EllipseSelection : public PixelSelectionCourier {
private:
  // const Coord pt0;
  // const Coord pt1;
  ICoord ll;
  ICoord ur;
  const Coord center;
  std::vector<double> aa;
  ICoord currentpt;
  bool interior();
  void advance();
public:
  EllipseSelection(CMicrostructure *ms,
		   const Coord *ll, const Coord *ur);
  virtual ~EllipseSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Group
class GroupSelection : public PixelSelectionCourier {
private:
  const PixelSet *pgroup;
  ICoordVector::const_iterator pxl_iter;
public:
  GroupSelection(CMicrostructure *ms, const PixelSet *group);
  virtual ~GroupSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Intersect
class IntersectSelection : public PixelSelectionCourier {
private:
  const PixelSet *selpix;
  PixelSet courpix;
  PixelSelectionCourier *courier;
  ICoordVector::const_iterator sel_iter;
  ICoordVector::const_iterator cour_iter;
  void advance();
public:
  IntersectSelection(CMicrostructure *ms,
		     const PixelSet *selpix,
		     PixelSelectionCourier *courier);
  virtual ~IntersectSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();  
  virtual void print(std::ostream &os) const;
};

// Despeckle
class DespeckleSelection : public PixelSelectionCourier {
private:
  const PixelSet *pgroup;
  const int neighbors;
  BoolArray selected;
  BoolArray::iterator sel_iter;
  void advance();
public:
  DespeckleSelection(CMicrostructure *ms, const PixelSet *group,
		     const int neighbors);
  virtual ~DespeckleSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Elkcepsed
class ElkcepsedSelection : public PixelSelectionCourier {
private:
  const PixelSet *pgroup;
  const int neighbors;
  BoolArray selected;
  BoolArray::iterator sel_iter;
  void advance();
public:
  ElkcepsedSelection(CMicrostructure *ms, const PixelSet *group,
		     const int neighbors);
  virtual ~ElkcepsedSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Expand
class ExpandSelection : public PixelSelectionCourier {
private:
  const PixelSet *pgroup;
  const double radius;
  BoolArray selected;
  BoolArray::iterator sel_iter;
  void advance();
public:
  ExpandSelection(CMicrostructure *ms, const PixelSet *group,
		  const double radius);
  ~ExpandSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};

// Shrink
class ShrinkSelection : public PixelSelectionCourier {
private:
  const PixelSet *pgroup;
  const double radius;
  BoolArray selected;
  BoolArray::iterator sel_iter;
  void advance();
public:
  ShrinkSelection(CMicrostructure *ms, const PixelSet *group,
		  const double radius);
  virtual ~ShrinkSelection() {}
  virtual void start();
  virtual ICoord currentPoint() const;
  virtual void next();
  virtual void print(std::ostream &os) const;
};     

std::ostream &operator<<(std::ostream&, const PixelSelectionCourier&);

#endif // PIXELSELECTIONCOURIER_H
