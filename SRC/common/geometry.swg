// -*- C++ -*-
// $RCSfile: geometry.swg,v $
// $Revision: 1.12.18.3.2.1 $
// $Author: langer $
// $Date: 2015/01/23 02:16:42 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GEOMETRY_SWG
#define GEOMETRY_SWG

%module geometry

%{
#include <oofconfig.h>
#include "common/geometry.h"
typedef class CPolygon<double, Coord> CPolygonCoord;
%}
%pragma(python) include="geometry.spy"
%include "common/typemaps.swg"


class CPolygonCoord {};

#ifndef DIM_3
class CRectangle : public CPolygonCoord {
public:
  CRectangle(const Coord&, const Coord&);
  double xmin();
  double xmax();
  double ymin();
  double ymax();
  double height();
  double width();
  void expand(double factor);
};

#else // DIM==3

class CRectangularPrism : public CPolygonCoord {
public:
  CRectangularPrism(const Coord&, const Coord&);
  double xmin();
  double xmax();
  double ymin();
  double ymax();
  double zmin();
  double zmax();
  double height();
  double width();
  double depth();
  void expand(double factor);
};

#endif	// DIM==3

// class CQuadrilateral : public CPolygonCoord {
// public:
//   CQuadrilateral(Coord *Point, Coord *Point, Coord *Point, Coord *Point);
//   bool contains(Coord *Point);
//   double area();
// };

// class CTriangle : public CPolygonCoord {
// public:
//   CTriangle(Coord *Point, Coord *Point, Coord *Point);
//   bool contains(Coord *Point);
//   double area();
// };

//double triangleArea(Coord *Point, Coord *Point, Coord *Point);

//double pixelIntersection(CPolygonCoord, ICoord *iPoint, double, double);

#endif // GEOMETRY_SWG
