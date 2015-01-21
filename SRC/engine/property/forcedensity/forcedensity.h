// -*- C++ -*-
// $RCSfile: forcedensity.h,v $
// $Revision: 1.12.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:39 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef FORCEDENSITY_H
#define FORCEDENSITY_H

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/smallsystem.h"
#include <string>

class Cijkl;
class CSubProblem;
class Element;
class Equation;
class Flux;
class Material;
class FEMesh;
class Position;
class TwoVectorField;
class ThreeVectorField;
class SymmetricTensorFlux;
class ElementNodeIterator;

class ForceDensity : public EqnProperty {
private:
  double gx, gy;
#if DIM==3
  double gz;
#endif
public:
#if DIM==2
  ForceDensity(PyObject *reg, const std::string &name, double x, double y);
#elif DIM==3
  ForceDensity(PyObject *reg, const std::string &name, double x, double y, double z);
#endif
  virtual ~ForceDensity() {}
  virtual void precompute(FEMesh*);
  virtual void force_value(const FEMesh*, const Element*, const Equation*,
			   const MasterPosition&, double time, SmallSystem*) const;
  virtual int integration_order(const CSubProblem*, const Element*) const;
  double fdensity_x() const { return gx; }
  double fdensity_y() const { return gy; }
#if DIM==3
  double fdensity_z() const { return gz; }
#endif
  virtual bool constant_in_space() const { return true; }
};

#endif
