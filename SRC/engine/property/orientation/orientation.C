// -*- C++ -*-
// $RCSfile: orientation.C,v $
// $Revision: 1.24.10.1 $
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

#include <oofconfig.h>

#include "common/cmicrostructure.h"
#include "engine/property/orientation/orientation.h"

OrientationProp::OrientationProp(PyObject *registry, const std::string &nm,
				 const COrientation *orient)
  : OrientationPropBase(registry,nm),
    orient(orient)
{}

OrientationProp::~OrientationProp() {}

const COrientation *OrientationProp::orientation(const FEMesh*, const Element*,
						 const MasterPosition&) const
{
  return orient;
}

const COrientation *OrientationProp::orientation(const CMicrostructure*,
						 const ICoord &) const
{
  return orient;
}

