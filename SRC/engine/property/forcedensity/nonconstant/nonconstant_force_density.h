// -*- C++ -*-
// $RCSfile: nonconstant_force_density.h,v $
// $Revision: 1.8.10.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:41 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef NONCONSTANT_FORCE_DENSITY_H
#define NONCONSTANT_FORCE_DENSITY_H

#include <oofconfig.h>
#include "engine/property.h"
#include "engine/smallsystem.h"
#include <string>

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
class DoubleVec;


class NonconstantForceDensity : public EqnProperty {
public:
  NonconstantForceDensity(PyObject *reg, const std::string &name);
  virtual ~NonconstantForceDensity() {}
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return false; }
  virtual void precompute(FEMesh*);
  virtual void force_value(const FEMesh*, const Element*, const Equation*,
			   const MasterPosition&, double time, SmallSystem*) const;
protected:
#if DIM==2
  TwoVectorField *displacement;
#elif DIM==3
  ThreeVectorField *displacement;
#endif
  SymmetricTensorFlux *stress_flux;

  virtual void nonconst_force_density(const Coord &coord, double time,
				      DoubleVec &result) const = 0;
  // virtual void nonconst_force_density(double x, double y, double z, double time,
  // 				      DoubleVec &result) const = 0;
};


class TestNonconstantForceDensity : public NonconstantForceDensity {
protected:
  int testNo;
  void nonconst_force_density_1(double x, double y, double z, double time,
				DoubleVec &result) const;
  void nonconst_force_density_2(double x, double y, double z, double time,
				DoubleVec &result) const;
  void nonconst_force_density_3(double x, double y, double z, double time,
				DoubleVec &result) const;
  void nonconst_force_density_4(double x, double y, double z, double time,
				DoubleVec &result) const;
  void nonconst_force_density_5(double x, double y, double z, double time,
				DoubleVec &result) const;
  virtual void nonconst_force_density(const Coord &coord, double time,
				      DoubleVec &result) const;
public:
  TestNonconstantForceDensity(PyObject *registry, const std::string &name, int testno)
    : NonconstantForceDensity( registry, name ), testNo(testno) {};
  virtual ~TestNonconstantForceDensity() {};
};

#endif
