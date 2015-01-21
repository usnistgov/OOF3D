// -*- C++ -*-
// $RCSfile: heatcapacity.h,v $
// $Revision: 1.13.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:45 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef HEATCAPACITY_H
#define HEATCAPACITY_H

#include <oofconfig.h>

#include "engine/property.h"

class CSubProblem;
class Element;

class HeatCapacityProp : public EqnProperty {
private:
  double cv_;
  Field *temperature;
public:
  HeatCapacityProp(PyObject*, const std::string&, double);
  virtual ~HeatCapacityProp() {}
  virtual void precompute(FEMesh*);
  virtual void first_time_deriv_matrix(const FEMesh*,
				       const Element*,
				       const Equation*,
				       const ElementFuncNodeIterator&,
				       const MasterPosition&,
				       double time,
				       SmallSystem*) const;
  virtual int integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return true; }
};


#endif
