// -*- C++ -*-
// $RCSfile: iso.C,v $
// $Revision: 1.17.18.1 $
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
#include "engine/property/elasticity/iso/iso.h"

CIsoElasticityProp::CIsoElasticityProp(PyObject *registration,
				       PyObject *self,
				       const std::string &nm, 
				       const Cijkl &c)
  : PythonNative<Property>(self),
    Elasticity(nm,registration),
    c_ijkl(c)
{
}

