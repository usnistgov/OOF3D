// -*- C++ -*-
// $RCSfile: massdensity.h,v $
// $Revision: 1.21.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:59 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef MASSDENSITY_H
#define MASSDENSITY_H

#include "engine/property.h"
#include <string>

class CSubProblem;
class Element;
class Equation;
class MasterPosition;
class SmallSystem;
class ElementFuncNodeIterator;
class Field;

class MassDensityProp : public EqnProperty {
private:
  double rho_;
  Field *disp;
public:
  MassDensityProp(PyObject *, const std::string&, double);
  virtual ~MassDensityProp() {}
  virtual void precompute(FEMesh*);
  virtual void second_time_deriv_matrix(const FEMesh*,
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
