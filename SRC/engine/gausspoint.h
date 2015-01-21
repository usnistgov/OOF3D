// -*- C++ -*-
// $RCSfile: gausspoint.h,v $
// $Revision: 1.11.18.6 $
// $Author: langer $
// $Date: 2014/12/14 22:49:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef GAUSSPOINT_H
#define GAUSSPOINT_H

class GaussPoint1;
class GaussPoint;		// used for integration
class GaussPtData;		// used privately for storing position & weight
class GaussPtTable1;
class GaussPtTable;		// used privately for storing sets of points

#include "common/coord.h"
#include "mastercoord.h"
#include <vector>
#include <iostream>

class BoundaryEdge;
class ElementBase;

// Do Gaussian integration like this:

//  ElementBase *el;
//  double sum1 = 0, sum2 = 0;
//  int order = ....; // see below
//  for(GaussPointIterator g=el->integrator(order); !g.end(); ++g) {
//
//     sum1 += f(g)*g.weight(); // IF f can be evaluated at gauss points, like
//                               // shapefunctions can
//
//     sum2 += f(g.coord())*g.weight();  // IF f can only be evaluated at
//                                         // real space coordinates  
//  }

// The MasterElement classes contain lists of GaussPtData objects
// (actually a vector of GaussPtTables).  When an Element creates a
// GaussPoint object to do an integral, the GaussPoint gets a pointer
// to the MasterElement's GaussPtData list.
//
// The weight computed by GaussPoint::weight() includes a factor of
// the determinant of the Jacobian.
//
// The parameter "order" passed to el->integrator() is the desired
// order of integration.  This depends on the polynomial degree of the
// shapefunctions and the other parts of the integrand.  The degree of
// the shapefunctions can be determined from
// Element::shapefun_degree(). So if the integrand is a linear
// function times two shape function derivatives, then order =
// 2*(degree-1)+1.  el->integrator will make sure that order >= 0.

class GaussPtData {
public:
  GaussPtData(const MasterCoord &p, double w)
    : position(p),
      weight(w)
  {}
  GaussPtData() {}		// null constructor required to make stl vector
private:
  MasterCoord position;
  double weight;
  friend class GaussPoint;
  friend class GaussPointIterator;
  friend class GaussPtTable;
  friend class ShapeFunction;
};

class GaussPoint : public Position, public MasterPosition {
public:
  virtual ~GaussPoint() {}
  double weight() const;
  int index() const; // So the cache can unambiguously identify gausspoints.
  Coord coord() const;
  virtual MasterCoord mastercoord() const;
  virtual Coord position() const {return coord(); }
  int order() const {return order_; }
  virtual double shapefunction(const ShapeFunction&, ShapeFunctionIndex)
    const;
  virtual double mdshapefunction(const ShapeFunction&, ShapeFunctionIndex,
				SpaceIndex) const;
  virtual double dshapefunction(const ElementBase*, const ShapeFunction&,
				ShapeFunctionIndex, SpaceIndex) const;
  virtual std::ostream &print(std::ostream&) const;

private:
  // Private constructor means only a GaussPointIterator can create 
  // a GaussPoint. 
  GaussPoint(const ElementBase*, MasterCoord, double, int, int); 
  const ElementBase *element;
  double weight_;
  MasterCoord position_;
  int index_;
  int order_;  // Needed by shapefunction evaluators.
  friend class ShapeFunction;
  friend class GaussPointIterator;
  friend std::ostream& operator<<(std::ostream &o, const GaussPoint&);
}; 

class GaussPointIterator {
public:
  GaussPointIterator(const ElementBase*, int);
  bool end() const;
  void operator++();
  int index() const;
  int order() const;
  GaussPoint gausspoint() const;
  GaussPoint *gausspointptr() const;
private:
  const ElementBase *element;
  const GaussPtTable &gptable;
  std::vector<GaussPtData>::size_type currentpt;
};



// Table of Gauss points for a single order of integration
class GaussPtTable {
private:
  int order_;
  std::vector<GaussPtData> gpdata;
public:
  GaussPtTable(const GaussPtTable&);
  GaussPtTable(int, int);
  const GaussPtData &operator[](int i) const { return gpdata[i]; }
  std::vector<GaussPtData>::size_type size() const { return gpdata.size(); }
  int order() const { return order_; }
  void addpoint(const MasterCoord&, double); // used by master element only
};

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Analogous classes for one dimensional integration

class GaussPtData1 {
public:
  GaussPtData1(double x, double w) : position(x), weight(w) {}
private:
  double position;
  double weight;
  friend class GaussPoint1;
  friend class GaussPtTable1;	// for debugging
};

class GaussPoint1 {
public:
  GaussPoint1(int order, double xmin, double xmax); // integrate from min to max
  bool end() const;		// are we done yet?
  void operator++();		// go to next point
  double weight() const;	// weight of this point
  double position() const;	// position in interval (min, max)
  double mposition() const;	// position in master interval (-1, 1)
  int order() const;
  static double Mmin, Mmax;	// limits of integration in master space
private:
  const GaussPtTable1 &gptable;
  std::vector<GaussPtData1>::size_type currentpt;
  double min, max;		// limits of integration in real space
};

class GaussPtTable1 {
private:
  int order_;
  std::vector<GaussPtData1> gpdata;
public:
  GaussPtTable1(int, int);
  GaussPtTable1(const GaussPtTable1&); 
  ~GaussPtTable1();
  const GaussPtData1 &operator[](int i) const { return gpdata[i]; }
  std::vector<GaussPtData1>::size_type size() const { return gpdata.size(); }
  int order() const { return order_; }
  void addpoint(double, double);
  static int n_orders();
  static int npts(int order);
};


//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

// Edge gauss-point iteration requires slightly different
// functionality.  Maps from (0,1) via the element master space to
// real space, and also makes the local real-space normal available.

class EdgeGaussPoint : public Position, public MasterPosition {
private:
  const BoundaryEdge *edge;
  GaussPoint1 gpone;
  // geometry() is only recomputed when needed, which is on the first
  // call to weight(), position(), etc after moving to the next point
  // with operator++.  weight(), position(), etc, are const functions,
  // so geometry() has to be too, and the data that it computes has to
  // be mutable.
  void geometry() const;
  mutable double gweight;
  mutable MasterCoord mhere;
  mutable Coord here;
#if DIM==2
  mutable Coord normal_;
#endif // DIM==2
  mutable Coord tangent;
  mutable bool recalculate_geometry;
public:
  EdgeGaussPoint(const BoundaryEdge* e, int order);
  virtual ~EdgeGaussPoint();
  void operator++();
  // "fraction" means how far along the edge you are, between 0 and 1.
  double fraction() const { return gpone.position(); }
  bool end() const { return gpone.end(); }
   //  int index();
  //  int order();
  virtual Coord position() const;
#if DIM==2
  Coord normal() const;
#endif // DIM==2
  virtual MasterCoord mastercoord() const;
  double weight() const;
  // Same double-dispatch trick as in GaussPoint class here.
  virtual double shapefunction(const ShapeFunction&, ShapeFunctionIndex) const;
  virtual double mdshapefunction(const ShapeFunction&, ShapeFunctionIndex,
				 SpaceIndex) const;
  virtual double dshapefunction(const ElementBase*, const ShapeFunction&,
				ShapeFunctionIndex, SpaceIndex) const;
  virtual std::ostream &print(std::ostream&) const;
};

#endif	// GAUSSPOINT_H

