// -*- C++ -*-
// $RCSfile: orientmapproperty.h,v $
// $Revision: 1.2.26.2 $
// $Author: langer $
// $Date: 2014/12/14 22:49:23 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#ifndef ORIENTMAPPROPERTY_H
#define ORIENTMAPPROPERTY_H

#include "common/coord_i.h"
#include "engine/property.h"
#include "engine/property/orientation/orientation.h"
#include "orientationmap/orientmapdata.h"

class CMicrostructure;
class COrientation;
class Element;
class FEMesh;
class MasterPosition;

class OrientationMapProp : public OrientationPropBase {
public:
  OrientationMapProp(PyObject *registry, const std::string &name);
  ~OrientationMapProp();
  virtual const COrientation *orientation() const; // not used -- poor design?!
  virtual const COrientation *orientation(const FEMesh*, const Element*,
					  const MasterPosition&) const;
  virtual const COrientation *orientation(const CMicrostructure*, const ICoord&)
    const;
  virtual bool constant_in_space() const { return false; }
  virtual void precompute(FEMesh*);
  virtual void clear_mesh_data(FEMesh*, void*) const;
};

#endif // ORIENTMAPPROPERTY_H
