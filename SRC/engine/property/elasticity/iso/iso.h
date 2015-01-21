// -*- C++ -*-
// $RCSfile: iso.h,v $
// $Revision: 1.16.18.2 $
// $Author: langer $
// $Date: 2013/11/08 20:45:30 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef ISOELASTICITY_H
#define ISOELASTICITY_H

#include "engine/property/elasticity/elasticity.h"
#include "engine/property/elasticity/cijkl.h"
#include "common/pythonexportable.h"
#include <string>

class CIsoElasticityProp 
  : public Elasticity, virtual public PythonNative<Property> 
{
private:
  Cijkl c_ijkl;
public:
  CIsoElasticityProp(PyObject *registry, PyObject *self,
		     const std::string &name, const Cijkl &c);
  virtual ~CIsoElasticityProp() {}
protected:
  virtual const Cijkl cijkl(const FEMesh*, const Element*, 
			    const MasterPosition&) const
  {
    return c_ijkl;
  }
};

#endif
