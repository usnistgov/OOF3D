// -*- C++ -*-
// $RCSfile: materialvoxelfilter.h,v $
// $Revision: 1.1.2.3 $
// $Author: langer $
// $Date: 2014/12/14 22:49:20 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#ifndef MATERIALVOXELFILTER_H
#define MATERIALVOXELFILTER_H

#include <oofconfig.h>

#include "common/voxelfilter.h"

class Material;

class VoxelMaterialFilter : public VoxelFilter {
private:
  const std::string materialName;
  const Material *material;
  bool any;			// is materialName == "<Any>"?
public:
  VoxelMaterialFilter(const std::string&);
  const std::string &classname() const;
  const std::string &modulename() const;
  virtual bool includeVoxel(const ICoord&) const;
  virtual bool precompute();
};

#endif // MATERIALVOXELFILTER_H
