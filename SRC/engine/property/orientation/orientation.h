// -*- C++ -*-
// $RCSfile: orientation.h,v $
// $Revision: 1.23.10.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:22 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov.
 */

#include <oofconfig.h>

#ifndef ORIENTATION_H
#define ORIENTATION_H

#include "common/coord_i.h"
#include "common/corientation.h"
#include "engine/property.h"
#include <string>

class CMicrostructure;
class Element;
class FEMesh;
class MasterPosition;

class OrientationPropBase : public AuxiliaryProperty {
public:
  OrientationPropBase(PyObject *registry, const std::string &name)
    : AuxiliaryProperty(name, registry)
  {}
  virtual const COrientation *orientation() const = 0;
  virtual const COrientation *orientation(const FEMesh*, const Element*,
					  const MasterPosition&) const = 0;
  virtual const COrientation *orientation(const CMicrostructure*, const ICoord&)
    const = 0;
  virtual bool constant_in_space() const = 0;
};

class OrientationProp : public OrientationPropBase {
private:
  const COrientation *orient;
public:
  OrientationProp(PyObject *registry, const std::string &name,
		  const COrientation *orient);
  ~OrientationProp();
  virtual const COrientation *orientation() const { return orient; }
  virtual const COrientation *orientation(const FEMesh*, const Element*,
				    const MasterPosition&) const;
  virtual const COrientation *orientation(const CMicrostructure*, const ICoord&)
    const;
  virtual bool constant_in_space() const { return true; }
};

#endif	// ORIENTATION_H
