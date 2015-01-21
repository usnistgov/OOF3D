// -*- C++ -*-
// $RCSfile: simpletension2.h,v $
// $Revision: 1.3.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:57 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#ifndef SIMPLETENSION2_H
#define SIMPLETENSION2_H

class SmallSystem;

#include "engine/property.h"
//#include <string>

class SimpleTension2 : public InterfaceProperty
{
private:
  double _k_left, _T_c_left, _k_right, _T_c_right;
public:
  SimpleTension2(PyObject *reg, const std::string &name,
		 double k_left, double T_c_left,
		 double k_right, double T_c_right);
  virtual ~SimpleTension2() {}
  virtual int integration_order(const CSubProblem*, const Element*) const;
  virtual bool constant_in_space() const { return true; }
  virtual void end_element(const CSubProblem*, const Element*);

  virtual void cross_reference(Material*);
  virtual void post_process(CSubProblem *, const Element *) const;
  virtual void flux_matrix(const FEMesh*, const Element*,
			   const ElementFuncNodeIterator&,
			   const Flux*, const MasterPosition&,
			   double time, SmallSystem *)
    const;
  virtual void flux_offset(const FEMesh*, const Element*, const Flux*,
			   const MasterPosition&, double time, SmallSystem*)
    const;
  virtual void output(const FEMesh*, const Element*, const PropertyOutput*,
		      const MasterPosition&, OutputVal*)
    const;
};

#endif	// SIMPLETENSION2_H
