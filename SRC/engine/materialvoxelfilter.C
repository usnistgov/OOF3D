// -*- C++ -*-
// $RCSfile: materialvoxelfilter.C,v $
// $Revision: 1.1.2.2 $
// $Author: langer $
// $Date: 2012/12/20 22:54:07 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "engine/materialvoxelfilter.h"
#include "engine/material.h"

VoxelMaterialFilter::VoxelMaterialFilter(const std::string &name)
  : materialName(name)
{}

const std::string &VoxelMaterialFilter::modulename() const {
  static const std::string name("ooflib.SWIG.engine.materialvoxelfilter");
  return name;
}

const std::string &VoxelMaterialFilter::classname() const {
  static const std::string name("VoxelMaterialFilter");
  return name;
}

bool VoxelMaterialFilter::precompute() {
  any = false;
  if(materialName == "<None>") {
    material = 0;
  }
  else if (materialName == "<Any>") {
    any = true;
  }
  else {
    material = getMaterial(microstructure, materialName);
  }
  return true;			// it's ok if the material==0.
}

bool VoxelMaterialFilter::includeVoxel(const ICoord &x) const {
  const Material *m = getMaterialFromPoint(microstructure, &x);
  if(any)
    return m != 0;
  return m == material;
}
