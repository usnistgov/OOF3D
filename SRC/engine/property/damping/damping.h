// -*- C++ -*-
// $RCSfile: damping.h,v $
// $Revision: 1.3.10.4 $
// $Author: fyc $
// $Date: 2014/07/31 20:17:21 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef DAMPING_H
#define DAMPING_H

#include <oofconfig.h>

#include "engine/property.h"

class IsotropicDampingProp : public EqnProperty {
private:
  double coeff;
  Field *displacement;
public:
  IsotropicDampingProp(PyObject*, const std::string&, double);
  virtual ~IsotropicDampingProp() {}
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

// TODO 3.1: Add asymmetries?

#endif	// DAMPING_H
