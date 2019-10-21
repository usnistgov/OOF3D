// -*- C++ -*-

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
#include <string>

class CSubProblem;
class Element;
class Equation;
class FEMesh;
class SmallSystem;

class ForceDensity : public EqnProperty {
private:
  double gx, gy, gz;
public:
  ForceDensity(PyObject *reg, const std::string &name,
	       double x, double y, double z);
  virtual ~ForceDensity() {}
  virtual void precompute(FEMesh*);
  virtual void force_value(const FEMesh*, const Element*, const Equation*,
			   const MasterPosition&, double time, SmallSystem*)
    const;
  virtual int integration_order(const CSubProblem*, const Element*) const;
  double fdensity_x() const { return gx; }
  double fdensity_y() const { return gy; }
  double fdensity_z() const { return gz; }
  virtual bool constant_in_space() const { return true; }
  virtual void output(FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*);
};

#endif
