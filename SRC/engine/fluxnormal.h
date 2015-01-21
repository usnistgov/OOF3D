// -*- C++ -*-
// $RCSfile: fluxnormal.h,v $
// $Revision: 1.5.18.3 $
// $Author: langer $
// $Date: 2014/02/28 03:22:00 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */


#include <oofconfig.h>

#ifndef FLUXNORMAL_H
#define FLUXNORMAL_H

// The fluxnormal classes are used by flux boundary conditions
// to evaluate the force density while integrating along a 
// boundary.  These are the classes that contain the return value.
//
// The reason for having classes set up this way is because we
// want to keep the relationship between fluxes and equations as
// loose and generic as possible -- in principle, a flux of any
// dimension could couple in surprising ways to equations of
// any number of components, and it's the job of the equation to
// figure this out and get it right.  For the base set of equations,
// this is a trivial process, and so the structure provided here
// is quite lightweight, but it provides room for expansion.

// The fluxnormal class also has the "transform" capability -- this
// takes a new "x" axis as an argument, and changes the internal x and
// y values such that the new x and y values are the lab-frame values
// of the old x and y values, which are the values in a frame where
// the outward normal is the +x axis and the tangent direction is the
// +y axis.  The definition of "outward" is such that this is a
// right-handed system.  
//   For instance, if a vector is given by the user as (0.1, 0.0)
// in the boundary-normal coordinates, and the boundary normal direction
// is 30 degrees up from the lab x-axis, i.e. (0.866, 0.500), then
// the appropriate lab-frame value of this vector is (0.087, 0.050),
// i.e. it is of length 0.1 in the normal direction.


#include "common/coord.h"

class FluxNormal {
protected:
  int size_;
public:
  FluxNormal() {}
  FluxNormal(int s) : size_(s) {}
  virtual ~FluxNormal() {}
  //
  // Class should support some kind of generic data-reading
  // (NB not writing) path, for debugging if for nothing else.
  int size() const { return size_; }       
  virtual double operator[](int) const = 0;
#if DIM==2
  // Re-evaluate using the input "coord" object as the x axis,
  // and preserving handedness.  
  virtual void transform(const Coord &frame) {};
#endif // DIM==2
  virtual void print(std::ostream&) const = 0;
};

class VectorFluxNormal: public FluxNormal {
private:
  double val_;
public:
  VectorFluxNormal() {}
  VectorFluxNormal(double v) : FluxNormal(1), val_(v) {}
  virtual ~VectorFluxNormal() {}
  double value() const { return val_; }
  double &value() { return val_; }
  virtual double operator[](int) const;
  virtual void print(std::ostream&) const;
};

class SymTensorFluxNormal: public FluxNormal {
public:
  Coord val;
  SymTensorFluxNormal() {}
  SymTensorFluxNormal(const Coord &v) : FluxNormal(DIM), val(v) {}
  virtual ~SymTensorFluxNormal() {}
  virtual double operator[](int i) const { return val[i]; }
#if DIM==2
  virtual void transform(const Coord &frame);
#endif // DIM==2
  virtual void print(std::ostream&) const;
};

std::ostream &operator<<(std::ostream&, const FluxNormal&);

#endif
