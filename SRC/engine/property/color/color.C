// -*- C++ -*-
// $RCSfile: color.C,v $
// $Revision: 1.19.10.1 $
// $Author: langer $
// $Date: 2013/11/08 20:45:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#include "color.h"
#include "engine/material.h"

ColorProp::ColorProp(PyObject *reg, const std::string &nm, double g)
  : AuxiliaryProperty(nm,reg),
    cvalue_(g,g,g) // Color is gray, but object is CColor.
{
}

ColorProp::ColorProp(PyObject *reg, const std::string &nm, double g, double a)
  : AuxiliaryProperty(nm,reg),
    cvalue_(g,g,g,a)
{
}

ColorProp::ColorProp(PyObject *reg, const std::string &nm,
		     double r, double g, double b)
  : AuxiliaryProperty(nm,reg),
    cvalue_(r,g,b)
{
}
ColorProp::ColorProp(PyObject *reg, const std::string &nm,
		     double r, double g, double b, double a)
  : AuxiliaryProperty(nm,reg),
    cvalue_(r,g,b,a)
{
}

ColorProp::ColorProp(PyObject *reg, const std::string &nm, CColor &cv)
  : AuxiliaryProperty(nm,reg),
    cvalue_(cv)
{
}

ColorProp::ColorProp(PyObject *reg, const std::string &nm, CColor *cv)
  : AuxiliaryProperty(nm, reg),
    cvalue_(*cv)
{
}

