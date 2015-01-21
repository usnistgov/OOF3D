// -*- C++ -*-
// $RCSfile: color.h,v $
// $Revision: 1.21.10.1 $
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

#ifndef COLORPROP_H
#define COLORPROP_H

#include "engine/property.h"
#include "common/ccolor.h"
#include <string>

// Color is slightly more general than just a gray value -- for now,
// it can be initialized to either (r,g,b), or to a gray level,
// all of which are assumed to be between 0.0 and 1.0.
//   Since virtually all of the graphics is done in Python, this
// class functions primarily as a place-holder, allowing materials
// to have color properties.  Before any graphics color assignments
// are contemplated, this color should be converted to the
// appropriate GUI color object, thereby preventing a lot of
// color callbacks through SWIG.

class ColorProp : public AuxiliaryProperty {
private:
  CColor cvalue_;
public:
  ColorProp(PyObject *reg, const std::string &nm, double g);
  ColorProp(PyObject *reg, const std::string &nm, double g, double a);
  ColorProp(PyObject *reg, const std::string &nm,
	    double r, double g, double b);
  ColorProp(PyObject *reg, const std::string &nm,
	    double r, double g, double b, double a);
  ColorProp(PyObject *reg, const std::string &nm, CColor &c);
  ColorProp(PyObject *reg, const std::string &nm, CColor *c);
  virtual ~ColorProp() {}
  const CColor &color() const { return cvalue_; }

  virtual bool constant_in_space() const { return true; }
};

#endif // COLORPROP_H
