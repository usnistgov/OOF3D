// -*- C++ -*-
// $RCSfile: voxelfilter.C,v $
// $Revision: 1.1.2.6 $
// $Author: langer $
// $Date: 2014/09/17 21:26:53 $

/* This software was produced by NIST, an agency of the U.S. government,
 * and by statute is not subject to copyright in the United States.
 * Recipients of this software assume all responsibilities associated
 * with its operation, modification and maintenance. However, to
 * facilitate maintenance we ask that before distributing modified
 * versions of this software, you first contact the authors at
 * oof_manager@nist.gov. 
 */

#include <oofconfig.h>

#include "common/IO/canvaslayers.h"
#include "common/IO/oofcerr.h"
#include "common/cmicrostructure.h"
#include "common/coord.h"
#include "common/pixelgroup.h"
#include "common/voxelfilter.h"

#include <algorithm>

// VoxelFilters may need to notice when something changes in the
// Microstructure, and force their ImageCanvasLayer to redraw.
// Because switchboard callbacks are done in Python, we have to be
// able to provide a list of VoxelFilters to it.  Each VoxelFilter
// Registration indicates what signals the filter needs to catch.

SLock VoxelFilter::lock;
std::vector<VoxelFilter*> VoxelFilter::all_; // static

const std::string &VoxelFilter::modulename() const {
  static const std::string name = "ooflib.SWIG.common.voxelfilter";
  return name;
}

VoxelFilter::VoxelFilter() 
  : microstructure(0),
    canvaslayer(0)
{
  lock.acquire();
  all_.push_back(this);
  lock.release();
}

VoxelFilter::~VoxelFilter() {
  canvaslayer = 0;
  lock.acquire();
  std::vector<VoxelFilter*>::iterator i = std::find(all_.begin(), all_.end(),
						    this);
  all_.erase(i);
  lock.release();
}

void VoxelFilter::setMicrostructure(const CMicrostructure *m) {
  microstructure = m;
}

void VoxelFilter::setCanvasLayer(OOFCanvasLayerBase *layer) {
  canvaslayer = layer;
}

std::vector<VoxelFilter*> *getVoxelFilters() {
  return &VoxelFilter::all_;
}

void VoxelFilter::setModified() {
  if(canvaslayer) {
    canvaslayer->setModified();
  }
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

const std::string &AllVoxels::classname() const {
  static const std::string name("AllVoxels");
  return name;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool ActiveVoxels::includeVoxel(const ICoord &x) const {
  return microstructure->isActive(x);
}

const std::string &ActiveVoxels::classname() const {
  static const std::string name("ActiveVoxels");
  return name;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

bool SelectedVoxels::includeVoxel(const ICoord &x) const {
  return microstructure->isSelected(&x);
}

const std::string &SelectedVoxels::classname() const {
  static const std::string name("SelectedVoxels");
  return name;
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

BinaryVoxelFilter::BinaryVoxelFilter(VoxelFilter *a, VoxelFilter *b)
  : a(a), b(b)
{}

bool BinaryVoxelFilter::precompute() {
  return a->precompute() && b->precompute();
}

void BinaryVoxelFilter::postcompute() {
  a->postcompute();
  b->postcompute();
}

void BinaryVoxelFilter::setMicrostructure(const CMicrostructure *m) {
  a->setMicrostructure(m);
  b->setMicrostructure(m);
}

void BinaryVoxelFilter::setCanvasLayer(OOFCanvasLayerBase *canvaslayer) {
  VoxelFilter::setCanvasLayer(canvaslayer);
  a->setCanvasLayer(canvaslayer);
  b->setCanvasLayer(canvaslayer);
}
//=\\=//=\\=//

const std::string &VoxelIntersection::classname() const {
  static const std::string name = "VoxelIntersection";
  return name;
}

bool VoxelIntersection::includeVoxel(const ICoord &x) const {
  return a->includeVoxel(x) && b->includeVoxel(x);
}

//=\\=//=\\=//

const std::string &VoxelUnion::classname() const {
  static const std::string name = "VoxelUnion";
  return name;
}

bool VoxelUnion::includeVoxel(const ICoord &x) const {
  return a->includeVoxel(x) || b->includeVoxel(x);
}

//=\\=//=\\=//

const std::string &VoxelXor::classname() const {
  static const std::string name = "VoxelXor";
  return name;
}

bool VoxelXor::includeVoxel(const ICoord &x) const {
  bool aok = a->includeVoxel(x);
  bool bok = b->includeVoxel(x);
  return (aok && !bok) || (bok && !aok);
}

//=\\=//=\\=//

VoxelNot::VoxelNot(VoxelFilter *a)
  : a(a)
{}

const std::string &VoxelNot::classname() const {
  static const std::string name = "VoxelNot";
  return name;
}

bool VoxelNot::includeVoxel(const ICoord &x) const {
  return !a->includeVoxel(x);
}

bool VoxelNot::precompute() {
  return a->precompute();
}

void VoxelNot::postcompute() {
  a->postcompute();
}

void VoxelNot::setMicrostructure(const CMicrostructure *m) {
  a->setMicrostructure(m);
}

void VoxelNot::setCanvasLayer(OOFCanvasLayerBase *canvaslayer) {
  VoxelFilter::setCanvasLayer(canvaslayer);
  a->setCanvasLayer(canvaslayer);
}

//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//=\\=//

VoxelGroupFilter::VoxelGroupFilter(const std::string &name)
  : groupName(name)
{}

const std::string &VoxelGroupFilter::classname() const {
  static const std::string name = "VoxelGroupFilter";
  return name;
}

bool VoxelGroupFilter::precompute() {
  group = microstructure->findGroup(groupName);
  return group != 0;
}

bool VoxelGroupFilter::includeVoxel(const ICoord &x) const {
  return group->pixelInGroup(&x);
}


