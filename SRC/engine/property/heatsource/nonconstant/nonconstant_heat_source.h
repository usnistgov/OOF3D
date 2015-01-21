// -*- C++ -*-
// $RCSfile: nonconstant_heat_source.h,v $
// $Revision: 1.9.10.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:52 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef NONCONSTANT_HEAT_SOURCE_H
#define NONCONSTANT_HEAT_SOURCE_H


#include "common/coord.h"
#include "engine/property.h"
#include "engine/symmmatrix.h"
#include <string>

class Element;
class Material;
class FEMesh;
class OrientationPropBase;
class SmallSystem;
class ScalarField;
class VectorFlux;
class ElementNodeIterator;



class NonconstantHeatSource : public EqnProperty {
public:
  NonconstantHeatSource(PyObject *registry, const std::string &name);
  virtual ~NonconstantHeatSource() {};
  virtual int  integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return false; }
  virtual void force_value(const FEMesh*, const Element*, const Equation*,
			   const MasterPosition&, double time, SmallSystem *) const;
protected:
  VectorFlux *heat_flux;
  virtual double nonconst_heat_source(double x, double y, double z, double time) const = 0;
};


class TestNonconstantHeatSource : public NonconstantHeatSource {
protected:
  int testNo;
  double nonconst_heat_source_1(double x, double y, double z, double time) const;
  double nonconst_heat_source_2(double x, double y, double z, double time) const;
  double nonconst_heat_source_3(double x, double y, double z, double time) const;
  double nonconst_heat_source_4(double x, double y, double z, double time) const;
  double nonconst_heat_source_5(double x, double y, double z, double time) const;
  double nonconst_heat_source_6(double x, double y, double z, double time) const;
  double nonconst_heat_source_7(double x, double y, double z, double time) const;
  double nonconst_heat_source_8(double x, double y, double z, double time) const;
  virtual double nonconst_heat_source(double x, double y, double z, double time) const;
public:
  TestNonconstantHeatSource(PyObject *registry, const std::string &name, int testno)
    : NonconstantHeatSource( registry, name ), testNo(testno) {};
  virtual ~TestNonconstantHeatSource() {};
};

#endif
